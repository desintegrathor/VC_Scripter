"""
Heritage orchestrator for multi-pass incremental SSA construction.

This module implements Ghidra-style heritage SSA construction where
variables are discovered and heritaged incrementally across multiple
passes. This approach improves decompilation quality by:

1. Better variable splitting - Multi-pass discovers when stack slots
   are reused for semantically different variables
2. Improved type inference - Refinement passes propagate function return
   types back to variable definitions
3. Enhanced dead code elimination - Multi-pass DCE finds temporaries
   that become unused after earlier optimizations
4. More precise PHI nodes - DF-based placement is formally correct
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from ....core.loader.scr_loader import SCRFile
from ....core.disasm import opcodes
from ..cfg import CFG, get_iterated_dominance_frontier, _compute_dominance_frontiers
from ..ssa import (
    SSAFunction, SSAValue, SSAInstruction,
    _propagate_types, _merge_result_types, _annotate_call_out_params, _fix_orphan_temporaries
)
from ..stack_lifter import (
    lift_function, lift_basic_block, LiftedInstruction, StackValue,
    _to_signed, _stack_alias_from_offset
)
from .location_map import LocationMap, HeritageRange, AddressSpace
from .rename import rename_frame_variables, RenameResult

logger = logging.getLogger(__name__)


@dataclass
class VariableInfo:
    """Information about a discovered variable."""
    name: str
    space: AddressSpace
    offset: int
    size: int
    def_blocks: Set[int] = field(default_factory=set)
    use_blocks: Set[int] = field(default_factory=set)
    value_type: opcodes.ResultType = opcodes.ResultType.UNKNOWN


@dataclass
class PhiNode:
    """A PHI node to be placed in SSA construction."""
    var_name: str
    block_id: int
    sources: List[Tuple[int, str]] = field(default_factory=list)  # (pred_id, source_name)
    result_name: Optional[str] = None
    value_type: opcodes.ResultType = field(default=opcodes.ResultType.UNKNOWN)


class HeritageOrchestrator:
    """
    Multi-pass SSA construction for improved decompilation quality.

    The heritage process works in passes:
    - Pass 0: Heritage parameters (known from function signature)
    - Pass 1: Heritage constants and obvious stack variables
    - Pass 2+: Discover and heritage remaining stack variables,
               refine types, eliminate dead code

    Each pass:
    1. Discovers new variables not yet heritaged
    2. Places PHI nodes using dominance frontiers
    3. Renames variables to SSA form
    4. Refines types through propagation
    5. Performs dead code elimination
    """

    def __init__(
        self,
        scr: SCRFile,
        cfg: CFG,
        max_passes: int = 5
    ) -> None:
        """
        Initialize the heritage orchestrator.

        Args:
            scr: The SCR file being decompiled
            cfg: Control flow graph (with dominators computed)
            max_passes: Maximum number of heritage passes
        """
        self.scr = scr
        self.cfg = cfg
        self.max_passes = max_passes
        self.resolver = getattr(scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
        from ...headers.database import get_header_database
        self.header_db = get_header_database()

        self.location_map = LocationMap()
        self.ssa_func: Optional[SSAFunction] = None
        self.pass_count = 0

        # Track variables discovered across all passes
        self._variables: Dict[str, VariableInfo] = {}

        # Lifted instructions by block (computed once, reused)
        self._lifted: Dict[int, List[LiftedInstruction]] = {}

        # PHI nodes placed during SSA construction
        self._phi_nodes: Dict[int, List[PhiNode]] = {}  # block_id -> PHI nodes

        # PHI naming counter
        self._phi_counter = 0

        # Rename pass result
        self._rename_result: Optional[RenameResult] = None

    def _lift_all_blocks(self) -> Dict[int, List[LiftedInstruction]]:
        """
        Lift all blocks in the CFG.

        This uses the existing CFG rather than creating a new one,
        which is important for consistency.
        """
        lifted: Dict[int, List[LiftedInstruction]] = {}

        def phi_name_fn(block_id: int, depth: int) -> str:
            name = f"phi_{block_id}_{depth}_{self._phi_counter}"
            self._phi_counter += 1
            return name

        # Process all blocks in order
        for block_id in sorted(self.cfg.blocks.keys()):
            lifted[block_id] = lift_basic_block(
                block_id, self.cfg, self.resolver, phi_name_fn, self.scr, self.header_db
            )

        return lifted

    def build_incremental_ssa(self) -> SSAFunction:
        """
        Build SSA using multi-pass heritage for improved quality.

        Returns:
            SSAFunction with incrementally constructed SSA form
        """
        # Ensure dominance frontiers are computed
        if not self.cfg.dominance_frontiers:
            _compute_dominance_frontiers(self.cfg)

        # Initial lifting - use the CFG we already have
        # lift_basic_block for each block in our existing CFG
        self._lifted = self._lift_all_blocks()

        # Pass 0: Heritage parameters
        logger.debug("Heritage pass 0: parameters")
        self._heritage_parameters()

        # Pass 1+: Discover and heritage stack variables
        while self.pass_count < self.max_passes:
            self.location_map.advance_pass()
            self.pass_count += 1

            logger.debug(f"Heritage pass {self.pass_count}: discovering stack variables")

            # Discover new variables not yet heritaged
            new_vars = self._discover_stack_variables()

            if not new_vars:
                logger.debug(f"Heritage converged at pass {self.pass_count}")
                break  # Convergence - no new variables discovered

            logger.debug(f"Pass {self.pass_count}: discovered {len(new_vars)} new variables")

            # Heritage the new variables (place PHIs, rename)
            self._heritage_new_variables(new_vars)

        # Renaming pass: walk dominator tree to create frame def-use chains
        param_count = getattr(self.scr.header, 'num_args', 0)
        if param_count == 0:
            param_count = self._detect_parameter_count()
        self._rename_result = rename_frame_variables(
            self.cfg, self._lifted, self._phi_nodes, self._variables,
            self.resolver, param_count=param_count,
        )

        # Build final SSA function
        self.ssa_func = self._build_final_ssa()

        # Refine SSA (type propagation, DCE)
        self._refine_ssa()

        return self.ssa_func

    def _heritage_parameters(self) -> None:
        """
        Heritage function parameters (pass 0).

        Parameters are known from the function header and are always
        heritaged in the first pass. They use negative stack offsets:
        - param_0 at [sp-4]
        - param_1 at [sp-3]
        - param_2 at [sp-2]
        - etc.

        Empirical evidence from bytecode analysis:
        - SRV_CheckEndRule(float time): uses [sp-4] for its only param
        - SetFlagStatus(attacking_side, cur_step): [sp-4] = param_0, [sp-3] = param_1
        """
        # Get parameter count from header if available
        param_count = getattr(self.scr.header, 'num_args', 0)
        if param_count == 0:
            # Try to detect from code
            param_count = self._detect_parameter_count()

        for i in range(param_count):
            offset = -(4 - i)  # param_0 at -4, param_1 at -3, param_2 at -2, etc.
            var_name = f"param_{i}"

            self.location_map.mark_heritaged(
                AddressSpace.PARAM,
                offset,
                size=4,  # Standard dword size
                var_name=var_name
            )

            # Track variable info
            self._variables[var_name] = VariableInfo(
                name=var_name,
                space=AddressSpace.PARAM,
                offset=offset,
                size=4,
                def_blocks={self.cfg.entry_block},  # Defined at entry
                use_blocks=set()  # Will be populated during discovery
            )

        logger.debug(f"Heritaged {param_count} parameters")

    def _detect_parameter_count(self) -> int:
        """
        Detect parameter count by analyzing code for parameter accesses.

        Parameter offsets: [sp-4] = param_0, [sp-3] = param_1, [sp-2] = param_2, etc.
        Formula: param_idx = offset + 4

        Returns:
            Detected number of parameters
        """
        max_param_idx = -1

        for block_id, lifted_insts in self._lifted.items():
            for inst in lifted_insts:
                mnemonic = self.resolver.get_mnemonic(inst.instruction.opcode)

                if mnemonic in {"LCP", "LLD"}:
                    offset = _to_signed(inst.instruction.arg1)
                    if offset <= -4:  # Parameter region starts at -4
                        param_idx = offset + 4  # -4→0, -3→1, -2→2, etc.
                        if param_idx >= 0:
                            max_param_idx = max(max_param_idx, param_idx)

        return max_param_idx + 1 if max_param_idx >= 0 else 0

    def _discover_stack_variables(self) -> List[VariableInfo]:
        """
        Discover stack variables not yet heritaged.

        Scans lifted instructions for stack accesses and identifies
        variables that haven't been heritaged in previous passes.

        Returns:
            List of newly discovered VariableInfo objects
        """
        new_vars: List[VariableInfo] = []
        discovered_offsets: Dict[int, VariableInfo] = {}

        for block_id, lifted_insts in self._lifted.items():
            for inst in lifted_insts:
                mnemonic = self.resolver.get_mnemonic(inst.instruction.opcode)

                # Check for stack variable accesses
                if mnemonic in {"LCP", "LLD", "LADR"}:
                    offset = _to_signed(inst.instruction.arg1)

                    if offset >= 0:  # Local variable (positive offset)
                        space = AddressSpace.STACK
                        var_name = f"local_{offset}"
                    elif offset < -2:  # Parameter (negative offset, skip return slots)
                        space = AddressSpace.PARAM
                        var_name = f"param_{abs(offset) - 3}"
                    else:
                        continue  # Return slot, skip

                    # Check if already heritaged
                    is_done, _ = self.location_map.is_heritaged(space, offset, 4)
                    if is_done:
                        continue

                    # Track or update variable info
                    if offset not in discovered_offsets:
                        var_info = VariableInfo(
                            name=var_name,
                            space=space,
                            offset=offset,
                            size=4
                        )
                        discovered_offsets[offset] = var_info
                        new_vars.append(var_info)
                    else:
                        var_info = discovered_offsets[offset]

                    # Track definition/use blocks
                    # Frame WRITE patterns:
                    #   1. LLD with outputs (store mode, pops=1) — original detection
                    #   2. LLD without outputs but positive offset (copy mode after XCALL/CALL)
                    #   3. LADR [sp+N] followed by ASGN within 3 instructions
                    # Frame READ patterns:
                    #   1. LCP [sp+N] — loads from frame to eval stack
                    #   2. Normal LLD [sp+N] with outputs (pops=0, pushes=1) — loads from frame
                    is_def = False
                    if mnemonic == "LLD" and inst.outputs:
                        # LLD store mode (pops=1) - this is a definition
                        is_def = True
                    elif mnemonic == "LLD" and not inst.outputs and offset >= 0:
                        # LLD copy mode (after XCALL/CALL, pops=0 pushes=0) - frame write
                        is_def = True
                    # NOTE: LADR+ASGN detection disabled for now — it causes too many
                    # PHI nodes to be placed, which cascades into structural regressions
                    # in the emitted code. The LLD copy-mode detection above is sufficient
                    # for the switch variable resolution use case.
                    # TODO: Re-enable when the emitter can handle the extra PHI nodes.

                    if is_def:
                        var_info.def_blocks.add(block_id)
                        if var_info.value_type == opcodes.ResultType.UNKNOWN and inst.outputs:
                            var_info.value_type = inst.outputs[0].value_type
                    else:
                        # LCP/LADR (without ASGN) loads a value - this is a use
                        var_info.use_blocks.add(block_id)
                        if var_info.value_type == opcodes.ResultType.UNKNOWN and inst.outputs:
                            for out in inst.outputs:
                                if out.value_type != opcodes.ResultType.UNKNOWN:
                                    var_info.value_type = out.value_type
                                    break

                # Check for global variable accesses
                elif mnemonic in {"GCP", "GLD", "GADR"}:
                    offset = inst.instruction.arg1
                    var_name = f"data_{offset}"

                    is_done, _ = self.location_map.is_heritaged(
                        AddressSpace.GLOBAL, offset, 4
                    )
                    if is_done:
                        continue

                    if offset not in discovered_offsets:
                        var_info = VariableInfo(
                            name=var_name,
                            space=AddressSpace.GLOBAL,
                            offset=offset,
                            size=4
                        )
                        discovered_offsets[offset] = var_info
                        new_vars.append(var_info)
                    else:
                        var_info = discovered_offsets[offset]

                    # Capture type from outputs (GCP/GLD produce typed values)
                    if var_info.value_type == opcodes.ResultType.UNKNOWN and inst.outputs:
                        for out in inst.outputs:
                            if out.value_type != opcodes.ResultType.UNKNOWN:
                                var_info.value_type = out.value_type
                                break

        return new_vars

    def _heritage_new_variables(self, new_vars: List[VariableInfo]) -> None:
        """
        Heritage newly discovered variables.

        For each variable:
        1. Mark as heritaged in location map
        2. Compute PHI node placement using dominance frontiers
        3. Place PHI nodes
        """
        for var_info in new_vars:
            # Mark as heritaged
            self.location_map.mark_heritaged(
                var_info.space,
                var_info.offset,
                var_info.size,
                var_info.name
            )

            # Store in variables map
            self._variables[var_info.name] = var_info

            # Only place PHIs if there are multiple definitions
            if len(var_info.def_blocks) > 1 or (
                var_info.def_blocks and var_info.use_blocks
            ):
                self._place_phi_nodes_for_variable(var_info)

    def _place_phi_nodes_for_variable(self, var_info: VariableInfo) -> None:
        """
        Place PHI nodes for a variable using iterated dominance frontier.

        Args:
            var_info: Variable to place PHIs for
        """
        # Compute iterated dominance frontier of definition blocks
        phi_blocks = get_iterated_dominance_frontier(
            self.cfg, var_info.def_blocks
        )

        for block_id in phi_blocks:
            if block_id not in self._phi_nodes:
                self._phi_nodes[block_id] = []

            phi = PhiNode(
                var_name=var_info.name,
                block_id=block_id,
                value_type=var_info.value_type,
            )
            self._phi_nodes[block_id].append(phi)

        logger.debug(
            f"Placed {len(phi_blocks)} PHI nodes for {var_info.name}"
        )

    def _build_final_ssa(self) -> SSAFunction:
        """
        Build the final SSA function from heritaged variables.

        Returns:
            Complete SSAFunction
        """
        values: Dict[str, SSAValue] = {}
        instructions: Dict[int, List[SSAInstruction]] = {}
        phi_addr_counter = -1

        def get_value(stack_val: StackValue) -> SSAValue:
            """Get or create SSA value for stack value."""
            if stack_val.name not in values:
                phi_sources = None
                if stack_val.phi_sources:
                    phi_sources = [(pred, src.name) for pred, src in stack_val.phi_sources]
                values[stack_val.name] = SSAValue(
                    name=stack_val.name,
                    value_type=stack_val.value_type,
                    producer=stack_val.producer.address if stack_val.producer else None,
                    phi_sources=phi_sources,
                    alias=stack_val.alias,
                )
            val = values[stack_val.name]
            # Update value with new info if available
            if stack_val.phi_sources and not val.phi_sources:
                val.phi_sources = [(pred, src.name) for pred, src in stack_val.phi_sources]
            if val.value_type == opcodes.ResultType.UNKNOWN and stack_val.value_type != opcodes.ResultType.UNKNOWN:
                val.value_type = stack_val.value_type
            if not val.alias and stack_val.alias:
                val.alias = stack_val.alias
            return val

        # Process each block
        for block_id, lifted_insts in self._lifted.items():
            ssa_block: List[SSAInstruction] = []
            block = self.cfg.blocks.get(block_id)

            # Add PHI nodes from heritage process
            if block_id in self._phi_nodes:
                for phi in self._phi_nodes[block_id]:
                    phi_addr = phi_addr_counter
                    phi_addr_counter -= 1

                    phi_value = SSAValue(
                        name=phi.result_name or f"phi_{block_id}_{phi.var_name}",
                        value_type=phi.value_type,
                        producer=phi_addr,
                        phi_sources=phi.sources if phi.sources else None
                    )
                    values[phi_value.name] = phi_value

                    phi_inputs = []
                    for pred_id, src_name in phi.sources:
                        if src_name in values:
                            src_val = values[src_name]
                            src_val.uses.append((phi_addr, len(phi_inputs)))
                            phi_inputs.append(src_val)

                    phi_inst = SSAInstruction(
                        block_id=block_id,
                        mnemonic="PHI",
                        address=phi_addr,
                        inputs=phi_inputs,
                        outputs=[phi_value],
                    )
                    phi_value.producer_inst = phi_inst
                    ssa_block.append(phi_inst)

            # Add PHI nodes from stack merging (legacy)
            if block:
                in_stack = getattr(block, "_in_stack", [])
                for phi_stack_val in in_stack:
                    if not getattr(phi_stack_val, "phi_sources", None):
                        continue
                    phi_value = get_value(phi_stack_val)
                    phi_address = phi_addr_counter
                    phi_addr_counter -= 1
                    phi_inputs: List[SSAValue] = []
                    for idx, (pred_id, src_stack_val) in enumerate(phi_stack_val.phi_sources or []):
                        src_val = get_value(src_stack_val)
                        src_val.uses.append((phi_address, idx))
                        phi_inputs.append(src_val)
                    phi_value.producer = phi_address
                    phi_inst = SSAInstruction(
                        block_id=block_id,
                        mnemonic="PHI",
                        address=phi_address,
                        inputs=phi_inputs,
                        outputs=[phi_value],
                    )
                    phi_value.producer_inst = phi_inst
                    ssa_block.append(phi_inst)

            # Convert lifted instructions to SSA instructions
            for lifted_inst in lifted_insts:
                ssa_inputs: List[SSAValue] = []
                for idx, stack_val in enumerate(lifted_inst.inputs):
                    val = get_value(stack_val)
                    val.uses.append((lifted_inst.instruction.address, idx))
                    ssa_inputs.append(val)

                ssa_outputs: List[SSAValue] = []
                for stack_val in lifted_inst.outputs:
                    val = get_value(stack_val)
                    val.producer = lifted_inst.instruction.address
                    ssa_outputs.append(val)

                mnemonic = self.resolver.get_mnemonic(lifted_inst.instruction.opcode)
                ssa_inst = SSAInstruction(
                    block_id=block_id,
                    mnemonic=mnemonic,
                    address=lifted_inst.instruction.address,
                    inputs=ssa_inputs,
                    outputs=ssa_outputs,
                    instruction=lifted_inst,
                )
                for out_val in ssa_outputs:
                    out_val.producer_inst = ssa_inst
                ssa_block.append(ssa_inst)

                # Link frame reads to their defining version from rename pass
                if self._rename_result:
                    addr = lifted_inst.instruction.address
                    read_key = (block_id, addr)
                    if read_key in self._rename_result.read_links:
                        version = self._rename_result.read_links[read_key]
                        for out_val in ssa_outputs:
                            out_val.metadata['frame_def_version'] = version

                    # Create SSA values for frame write versions so they can be looked up
                    write_key = (block_id, addr)
                    if write_key in self._rename_result.write_versions:
                        version = self._rename_result.write_versions[write_key]
                        if version not in values:
                            # For frame writes, trace back to what produced the stored value:
                            # - LLD copy-mode: prev instruction is XCALL/CALL that returned value
                            # - LADR+ASGN: the ASGN's first input is the stored value
                            source_inst = ssa_inst
                            source_addr = addr
                            if mnemonic == "LLD" and len(ssa_block) >= 2:
                                # LLD copy-mode: look at preceding instruction
                                prev_ssa = ssa_block[-2]
                                if prev_ssa.mnemonic in {"XCALL", "CALL"}:
                                    source_inst = prev_ssa
                                    source_addr = prev_ssa.address
                            elif mnemonic == "LADR":
                                # LADR+ASGN: find the ASGN and use its first input's producer
                                for later_inst in lifted_insts[lifted_insts.index(lifted_inst)+1:]:
                                    later_mn = self.resolver.get_mnemonic(later_inst.instruction.opcode)
                                    if later_mn == "ASGN" and later_inst.inputs:
                                        # ASGN inputs: [value_to_store, address]
                                        stored_val = later_inst.inputs[0]
                                        if stored_val.producer:
                                            # Find the SSA inst for the stored value's producer
                                            for prev_ssa in ssa_block:
                                                if prev_ssa.address == stored_val.producer.address:
                                                    source_inst = prev_ssa
                                                    source_addr = prev_ssa.address
                                                    break
                                        break
                                    if later_mn in {"JMP", "JZ", "JNZ", "CALL", "XCALL", "RET"}:
                                        break
                            write_val = SSAValue(
                                name=version,
                                value_type=opcodes.ResultType.UNKNOWN,
                                producer=source_addr,
                            )
                            write_val.producer_inst = source_inst

                            # Post-store global alias: if LLD copy-mode, scan ahead
                            # for GADR+ASGN pattern (same XCALL return stored to global)
                            if mnemonic == "LLD":
                                lld_idx = lifted_insts.index(lifted_inst)
                                for scan_idx in range(lld_idx + 1, min(lld_idx + 5, len(lifted_insts))):
                                    scan_inst = lifted_insts[scan_idx]
                                    scan_mn = self.resolver.get_mnemonic(scan_inst.instruction.opcode)
                                    if scan_mn == "GADR":
                                        global_offset = scan_inst.instruction.arg1
                                        write_val.metadata['global_alias_offset'] = global_offset
                                        break
                                    if scan_mn in {"JMP", "JZ", "JNZ", "CALL", "XCALL", "RET", "LCP"}:
                                        break

                            values[version] = write_val

            instructions[block_id] = ssa_block

        # Also create SSA values for PHI result versions from rename pass
        if self._rename_result:
            for (blk_id, var_name), sources in self._rename_result.phi_sources.items():
                for phi in self._phi_nodes.get(blk_id, []):
                    if phi.var_name == var_name and phi.result_name:
                        if phi.result_name not in values:
                            phi_val = SSAValue(
                                name=phi.result_name,
                                value_type=phi.value_type,
                                phi_sources=sources,
                            )
                            # Propagate global_alias_offset from PHI inputs
                            alias_offset = None
                            for _, src_name in sources:
                                if src_name in values:
                                    src_alias = values[src_name].metadata.get('global_alias_offset')
                                    if src_alias is not None:
                                        if alias_offset is None:
                                            alias_offset = src_alias
                                        elif alias_offset != src_alias:
                                            alias_offset = None  # conflicting aliases
                                            break
                            if alias_offset is not None:
                                phi_val.metadata['global_alias_offset'] = alias_offset
                            values[phi.result_name] = phi_val

        ssa_func = SSAFunction(
            cfg=self.cfg,
            values=values,
            instructions=instructions,
            scr=self.scr
        )
        _annotate_call_out_params(ssa_func)
        orphan_fixes = _fix_orphan_temporaries(ssa_func)
        if orphan_fixes:
            logger.debug("Fixed %d orphan temporaries in heritage SSA", orphan_fixes)
        return ssa_func

    def _refine_ssa(self) -> None:
        """
        Refine SSA with type propagation and dead code elimination.
        """
        if not self.ssa_func:
            return

        # Backward type propagation (infer from usage)
        self._propagate_backward_types()

        # Forward type propagation
        _propagate_types(self.resolver, self.ssa_func.instructions)

        # Dead code elimination
        self._eliminate_dead_code()

    def _propagate_backward_types(self) -> None:
        """
        Backward type propagation: infer variable types from how they're used.

        For each VariableInfo with UNKNOWN type, examine all instructions that
        use that variable and infer type from operation requirements:
        - IADD, ISUB, IMUL, etc. → INT
        - FADD, FSUB, FMUL, etc. → FLOAT
        - DADR, PNT → POINTER

        This scans ALL blocks because use_blocks may not be fully populated
        for parameters and some stack variables.
        """
        # Map mnemonic prefixes/names to required operand types
        int_ops = {
            'IADD', 'ISUB', 'IMUL', 'IDIV', 'IMOD', 'INEG', 'INC', 'DEC',
            'IGT', 'IGE', 'ILT', 'ILE', 'UGT', 'UGE', 'ULT', 'ULE',
            'ISHL', 'ISHR', 'IAND', 'IOR', 'IXOR', 'INOT',
            'ITOF', 'ITOD', 'ITOS', 'ITOC',  # INT as input
        }
        float_ops = {
            'FADD', 'FSUB', 'FMUL', 'FDIV', 'FNEG',
            'FGT', 'FGE', 'FLT', 'FLE',
            'FTOI', 'FTOD',  # FLOAT as input
        }
        double_ops = {
            'DADD', 'DSUB', 'DMUL', 'DDIV', 'DNEG',
            'DGT', 'DGE', 'DLT', 'DLE',
            'DTOI', 'DTOF',  # DOUBLE as input
        }
        pointer_ops = {'DADR', 'PNT', 'ASGN'}  # ASGN first operand is pointer

        # Build a map of variable name -> inferred type by scanning all blocks
        # This handles cases where use_blocks is incomplete
        var_inferred_type: Dict[str, opcodes.ResultType] = {}

        for block_id, lifted_insts in self._lifted.items():
            for inst in lifted_insts:
                mnemonic = self.resolver.get_mnemonic(inst.instruction.opcode)

                # Check each input for variable aliases
                for inp in inst.inputs:
                    if not inp.alias:
                        continue

                    # The alias may be the variable name directly
                    var_name = inp.alias

                    # Skip if we already inferred a type for this variable
                    if var_name in var_inferred_type:
                        continue

                    # Skip if not a tracked variable
                    if var_name not in self._variables:
                        continue

                    # Skip if variable already has a type
                    if self._variables[var_name].value_type != opcodes.ResultType.UNKNOWN:
                        continue

                    # Infer type from operation
                    inferred_type = None
                    if mnemonic in int_ops:
                        inferred_type = opcodes.ResultType.INT
                    elif mnemonic in float_ops:
                        inferred_type = opcodes.ResultType.FLOAT
                    elif mnemonic in double_ops:
                        inferred_type = opcodes.ResultType.DOUBLE
                    elif mnemonic in pointer_ops:
                        inferred_type = opcodes.ResultType.POINTER

                    if inferred_type:
                        var_inferred_type[var_name] = inferred_type
                        logger.debug(
                            f"Backward propagation: {var_name} → {inferred_type.name} "
                            f"(from {mnemonic} in block {block_id})"
                        )

        # Apply inferred types
        for var_name, inferred_type in var_inferred_type.items():
            self._variables[var_name].value_type = inferred_type

        if var_inferred_type:
            logger.debug(f"Backward propagation resolved {len(var_inferred_type)} variable types")

    def _eliminate_dead_code(self) -> None:
        """
        Eliminate dead code (unused definitions).

        A value is dead if it has no uses and is not a side-effecting
        instruction (like XCALL, stores, etc.).

        Note: This is a single-pass marking algorithm. True DCE with
        cascading removal would require removing instructions from the
        list and updating use-def chains, which is complex. For now,
        we just mark dead values and skip them during code generation.
        """
        if not self.ssa_func:
            return

        # Side-effecting mnemonics that should not be eliminated
        side_effects = {
            "RET", "JMP", "JZ", "JNZ",
            "LLD", "GLD", "DLD",  # Stores
            "SSP", "ASP",  # Stack manipulation
            "CALL", "XCALL",  # External/internal calls are side-effecting
        }

        # Single pass: mark all unused values as dead
        for block_id, ssa_insts in self.ssa_func.instructions.items():
            for inst in ssa_insts:
                if inst.mnemonic in side_effects:
                    continue

                # Check if all outputs are unused
                for out_val in inst.outputs:
                    if not out_val.uses:
                        out_val.metadata["dead"] = True

    def get_heritage_stats(self) -> Dict[str, int]:
        """
        Get statistics about the heritage process.

        Returns:
            Dictionary with counts of heritaged items
        """
        return {
            "passes": self.pass_count,
            "total_variables": len(self._variables),
            "stack_variables": len([
                v for v in self._variables.values()
                if v.space == AddressSpace.STACK
            ]),
            "parameters": len([
                v for v in self._variables.values()
                if v.space == AddressSpace.PARAM
            ]),
            "globals": len([
                v for v in self._variables.values()
                if v.space == AddressSpace.GLOBAL
            ]),
            "phi_nodes": sum(len(phis) for phis in self._phi_nodes.values()),
        }

    def get_heritage_metadata(self) -> Dict[str, any]:
        """
        Export heritage information for code emitter integration.

        This method provides metadata about discovered variables and PHI node
        placements that can be used by the code generation pipeline to produce
        improved variable names and declarations.

        Returns:
            Dictionary containing:
            - variables: Dict[name, {type, space, offset, def_blocks, use_blocks}]
            - phi_blocks: Dict[block_id, [var_names with PHIs]]
            - passes: Number of heritage passes completed
        """
        variables = {}
        for name, var in self._variables.items():
            variables[name] = {
                "type": var.value_type.name if hasattr(var.value_type, 'name') else str(var.value_type),
                "space": var.space.name,
                "offset": var.offset,
                "size": var.size,
                "def_blocks": list(var.def_blocks),
                "use_blocks": list(var.use_blocks),
            }

        phi_blocks = {}
        for block_id, phis in self._phi_nodes.items():
            phi_blocks[block_id] = [phi.var_name for phi in phis]

        return {
            "variables": variables,
            "phi_blocks": phi_blocks,
            "passes": self.pass_count,
        }
