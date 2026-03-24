"""
Dominator-tree renaming pass for frame-stack variables.

Implements Ghidra-style SSA renaming (heritage.cc:renameRecurse) to create
explicit def-use chains between frame writes (LLD copy-mode, LADR+ASGN)
and frame reads (LCP, normal LLD).

The renaming walks the dominator tree depth-first, maintaining a per-offset
stack of version names. Each frame write pushes a new version; each frame
read records a link to the current top version.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from ....core.disasm import opcodes
from ..cfg import CFG
from ..stack_lifter import LiftedInstruction, _to_signed

logger = logging.getLogger(__name__)


@dataclass
class RenameResult:
    """Output of the renaming pass."""
    # Heritage PHI sources: (block_id, var_name) -> [(pred_id, version_name)]
    phi_sources: Dict[Tuple[int, str], List[Tuple[int, str]]] = field(default_factory=dict)
    # LCP/LLD-read linkage: (block_id, inst_address) -> defining_version_name
    read_links: Dict[Tuple[int, int], str] = field(default_factory=dict)
    # Frame write records: (block_id, inst_address) -> version_name
    write_versions: Dict[Tuple[int, int], str] = field(default_factory=dict)
    # Version -> source instruction address (for tracing what was written)
    write_source_addr: Dict[str, int] = field(default_factory=dict)


class FrameVariableStack:
    """Per-offset stack of version names, mimicking Ghidra's VariableStack."""

    def __init__(self):
        self._stacks: Dict[int, List[str]] = {}

    def push(self, offset: int, version_name: str) -> None:
        if offset not in self._stacks:
            self._stacks[offset] = []
        self._stacks[offset].append(version_name)

    def top(self, offset: int) -> Optional[str]:
        stack = self._stacks.get(offset)
        if stack:
            return stack[-1]
        return None

    def pop(self, offset: int) -> None:
        stack = self._stacks.get(offset)
        if stack:
            stack.pop()

    def snapshot(self) -> Dict[int, int]:
        """Save stack depths for later restore."""
        return {offset: len(stack) for offset, stack in self._stacks.items()}

    def restore(self, snap: Dict[int, int]) -> None:
        """Restore stack depths from snapshot."""
        for offset, stack in self._stacks.items():
            target_depth = snap.get(offset, 0)
            while len(stack) > target_depth:
                stack.pop()


def _is_frame_write_lld(inst: LiftedInstruction, resolver: opcodes.OpcodeResolver) -> Optional[int]:
    """Check if instruction is an LLD copy-mode frame write. Returns offset or None."""
    mnemonic = resolver.get_mnemonic(inst.instruction.opcode)
    if mnemonic != "LLD":
        return None
    offset = _to_signed(inst.instruction.arg1)
    if offset < 0:
        return None
    # Copy mode: no outputs (pops=0, pushes=0)
    if not inst.outputs:
        return offset
    return None


def _is_frame_write_ladr_asgn(
    inst_idx: int,
    lifted_insts: List[LiftedInstruction],
    resolver: opcodes.OpcodeResolver,
) -> Optional[int]:
    """Check if instruction at inst_idx is LADR [sp+N] followed by ASGN. Returns offset or None."""
    inst = lifted_insts[inst_idx]
    mnemonic = resolver.get_mnemonic(inst.instruction.opcode)
    if mnemonic != "LADR":
        return None
    offset = _to_signed(inst.instruction.arg1)
    if offset < 0:
        return None
    # Look for ASGN within next 3 instructions
    for j in range(inst_idx + 1, min(inst_idx + 4, len(lifted_insts))):
        later = lifted_insts[j]
        later_mn = resolver.get_mnemonic(later.instruction.opcode)
        if later_mn == "ASGN":
            return offset
        # Stop if we hit control flow or another address load
        if later_mn in {"JMP", "JZ", "JNZ", "CALL", "XCALL", "RET", "LADR", "GADR"}:
            break
    return None


def _is_frame_read_lcp(inst: LiftedInstruction, resolver: opcodes.OpcodeResolver) -> Optional[int]:
    """Check if instruction is LCP [sp+N] frame read. Returns offset or None."""
    mnemonic = resolver.get_mnemonic(inst.instruction.opcode)
    if mnemonic != "LCP":
        return None
    offset = _to_signed(inst.instruction.arg1)
    if offset >= 0:
        return offset
    return None


def _is_frame_read_lld(inst: LiftedInstruction, resolver: opcodes.OpcodeResolver) -> Optional[int]:
    """Check if instruction is normal LLD [sp+N] (has outputs = read). Returns offset or None."""
    mnemonic = resolver.get_mnemonic(inst.instruction.opcode)
    if mnemonic != "LLD":
        return None
    offset = _to_signed(inst.instruction.arg1)
    if offset < 0:
        return None
    # Normal mode: has outputs (pops=0, pushes=1)
    if inst.outputs:
        return offset
    return None


def rename_frame_variables(
    cfg: CFG,
    lifted: Dict[int, List[LiftedInstruction]],
    phi_nodes: Dict[int, list],  # block_id -> List[PhiNode]
    variables: Dict[str, object],  # var_name -> VariableInfo
    resolver: opcodes.OpcodeResolver,
    param_count: int = 0,
) -> RenameResult:
    """
    Dominator-tree renaming pass for frame-stack variables.

    Walks the dominator tree depth-first, maintaining a per-offset version
    stack. Creates def-use links between frame writes and reads.
    """
    result = RenameResult()
    var_stack = FrameVariableStack()
    version_counter = [0]

    def next_version(offset: int) -> str:
        version_counter[0] += 1
        return f"frame_{offset}_v{version_counter[0]}"

    # Initialize parameter versions
    for i in range(param_count):
        param_offset = -(4 - i)  # param_0 at -4, param_1 at -3, etc.
        version = f"param_{i}_v0"
        var_stack.push(param_offset, version)

    # Find entry block
    if not cfg.blocks:
        return result
    entry_id = min(cfg.blocks.keys())
    if hasattr(cfg, 'dom_tree') and cfg.dom_tree is not None:
        # Find root of dominator tree (node that dominates all others)
        # It's the node whose idom is itself
        if hasattr(cfg, 'idom') and cfg.idom:
            for node, parent in cfg.idom.items():
                if node == parent:
                    entry_id = node
                    break

    def rename_recurse(block_id: int):
        snap = var_stack.snapshot()
        writes_in_block: List[int] = []  # offsets written, for tracking

        # 1. Process heritage PHI nodes at block start
        for phi in phi_nodes.get(block_id, []):
            # Determine offset from var_name
            offset = _var_name_to_offset(phi.var_name)
            if offset is None:
                continue
            version = f"phi_{block_id}_{phi.var_name}"
            var_stack.push(offset, version)
            writes_in_block.append(offset)
            # Store the PHI result version
            phi.result_name = version

        # 2. Process instructions in order
        block_insts = lifted.get(block_id, [])
        for i, inst in enumerate(block_insts):
            addr = inst.instruction.address

            # Frame WRITE: LLD copy-mode
            write_offset = _is_frame_write_lld(inst, resolver)
            if write_offset is not None:
                version = next_version(write_offset)
                var_stack.push(write_offset, version)
                writes_in_block.append(write_offset)
                result.write_versions[(block_id, addr)] = version
                result.write_source_addr[version] = addr
                continue

            # Frame WRITE: LADR [sp+N] + ASGN
            write_offset = _is_frame_write_ladr_asgn(i, block_insts, resolver)
            if write_offset is not None:
                version = next_version(write_offset)
                var_stack.push(write_offset, version)
                writes_in_block.append(write_offset)
                result.write_versions[(block_id, addr)] = version
                result.write_source_addr[version] = addr
                continue

            # Frame READ: LCP [sp+N]
            read_offset = _is_frame_read_lcp(inst, resolver)
            if read_offset is not None:
                current = var_stack.top(read_offset)
                if current:
                    result.read_links[(block_id, addr)] = current
                continue

            # Frame READ: normal LLD [sp+N] (has outputs)
            read_offset = _is_frame_read_lld(inst, resolver)
            if read_offset is not None:
                current = var_stack.top(read_offset)
                if current:
                    result.read_links[(block_id, addr)] = current
                continue

        # 3. Populate PHI inputs in successor blocks
        if block_id in cfg.blocks:
            for succ_id in cfg.blocks[block_id].successors:
                for phi in phi_nodes.get(succ_id, []):
                    offset = _var_name_to_offset(phi.var_name)
                    if offset is None:
                        continue
                    current = var_stack.top(offset)
                    if current:
                        phi.sources.append((block_id, current))
                        # Also record in result for reference
                        key = (succ_id, phi.var_name)
                        if key not in result.phi_sources:
                            result.phi_sources[key] = []
                        result.phi_sources[key].append((block_id, current))

        # 4. Recurse to dominated children
        for child_id in cfg.dom_tree.get(block_id, []):
            rename_recurse(child_id)

        # 5. Restore stack state
        var_stack.restore(snap)

    # Run the renaming
    if hasattr(cfg, 'dom_tree') and cfg.dom_tree:
        rename_recurse(entry_id)

    logger.debug(
        f"Rename pass: {len(result.write_versions)} frame writes, "
        f"{len(result.read_links)} frame reads linked, "
        f"{sum(len(v) for v in result.phi_sources.values())} PHI sources populated"
    )

    return result


def _var_name_to_offset(var_name: str) -> Optional[int]:
    """Convert variable name to frame offset."""
    if var_name.startswith("local_"):
        try:
            return int(var_name[6:])
        except ValueError:
            return None
    if var_name.startswith("param_"):
        try:
            idx = int(var_name[6:])
            return -(4 - idx)  # param_0 at -4, param_1 at -3
        except ValueError:
            return None
    return None
