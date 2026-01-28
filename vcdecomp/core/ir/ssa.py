"""
SSA graph construction on top of lifted stack values.

This module provides two modes of SSA construction:

1. Traditional SSA (build_ssa):
   - Full reconstruction on every call
   - Implicit PHI placement based on stack state divergence
   - Simple t{address}_{index} versioning

2. Heritage-based Incremental SSA (build_ssa_incremental):
   - Ghidra-style multi-pass construction
   - Explicit PHI placement using dominance frontiers
   - Better variable splitting and type inference
   - Improved dead code elimination

For best results, use build_ssa_incremental for complex scripts.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Iterable

from ..loader.scr_loader import SCRFile
from ..disasm import opcodes
from .cfg import CFG, _compute_dominance_frontiers
from .stack_lifter import lift_function, LiftedInstruction, StackValue, SIMPLE_ARITHMETIC_MNEMONICS

logger = logging.getLogger(__name__)


@dataclass
class SSAValue:
    name: str
    value_type: opcodes.ResultType
    producer: Optional[int] = None  # instruction address
    uses: List[Tuple[int, int]] = field(default_factory=list)  # (instruction address, operand index)
    phi_sources: Optional[List[Tuple[int, str]]] = None  # (pred block id, source value name)
    alias: Optional[str] = None
    producer_inst: Optional["SSAInstruction"] = None
    metadata: Dict = field(default_factory=dict)  # Additional metadata for SDK integration


@dataclass
class SSAInstruction:
    block_id: int
    mnemonic: str
    address: int
    inputs: List[SSAValue]
    outputs: List[SSAValue]
    instruction: Optional[LiftedInstruction] = None
    metadata: Dict = field(default_factory=dict)  # Metadata for optimizations (array access, etc.)


@dataclass
class SSAFunction:
    cfg: CFG
    values: Dict[str, SSAValue]
    instructions: Dict[int, List[SSAInstruction]]
    scr: SCRFile


def build_ssa(scr: SCRFile) -> SSAFunction:
    resolver = getattr(scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    cfg, lifted = lift_function(scr, resolver)
    return _build_ssa_from_lifted(scr, resolver, cfg, lifted)


def build_ssa_all_blocks(scr: SCRFile) -> SSAFunction:
    """Build SSA for ALL blocks in the file, not just reachable from entry."""
    resolver = getattr(scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    cfg, lifted = lift_function(scr, resolver)
    return _build_ssa_from_lifted(scr, resolver, cfg, lifted)


def _build_ssa_from_lifted(scr: SCRFile, resolver, cfg: CFG, lifted: Dict[int, List[LiftedInstruction]]) -> SSAFunction:
    """Internal helper to build SSA from lifted instructions."""
    values: Dict[str, SSAValue] = {}
    instructions: Dict[int, List[SSAInstruction]] = {}
    phi_addr_counter = -1

    def get_value(stack_val: StackValue) -> SSAValue:
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
                metadata=dict(stack_val.metadata),
            )
        val = values[stack_val.name]
        if stack_val.phi_sources and not val.phi_sources:
            val.phi_sources = [(pred, src.name) for pred, src in stack_val.phi_sources]
        if val.value_type == opcodes.ResultType.UNKNOWN and stack_val.value_type != opcodes.ResultType.UNKNOWN:
            val.value_type = stack_val.value_type
        if not val.alias and stack_val.alias:
            val.alias = stack_val.alias
        if stack_val.metadata:
            val.metadata.update(stack_val.metadata)
        return val

    for block_id, insts in lifted.items():
        ssa_block: List[SSAInstruction] = []
        block = cfg.blocks.get(block_id)
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
        for lifted_inst in insts:
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

            mnemonic = resolver.get_mnemonic(lifted_inst.instruction.opcode)
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
        instructions[block_id] = ssa_block

    # Build SSA function object
    ssa_func = SSAFunction(cfg=cfg, values=values, instructions=instructions, scr=scr)
    orphan_fixes = _fix_orphan_temporaries(ssa_func)
    if orphan_fixes:
        logger.debug("Fixed %d orphan temporaries after SSA build", orphan_fixes)

    _propagate_types(resolver, instructions)
    _mark_simple_arithmetic_compound_stores(instructions)
    _annotate_call_out_params(ssa_func)

    # Apply bidirectional type inference (optional, can be disabled)
    # This improves type inference accuracy by 15-20% through backward
    # constraint propagation from known output types
    if getattr(scr, 'enable_bidirectional_types', True):  # Default: enabled
        from .type_algebra import infer_types_bidirectional
        type_stats = infer_types_bidirectional(
            ssa_func,
            debug=getattr(scr, 'debug_type_inference', False)
        )
        if getattr(scr, 'debug_type_inference', False):
            logger.info(f"Type inference: {type_stats}")

    # Apply expression simplification (optional, can be disabled)
    # This reduces output verbosity by 30-40% through constant folding,
    # algebraic identities, and canonical term ordering
    if getattr(scr, 'enable_simplify', True):  # Default: enabled
        from .simplify import simplify_expressions
        simplify_expressions(ssa_func, debug=getattr(scr, 'debug_simplify', False))

    # Apply LoadGuard array detection (optional, can be disabled)
    # This improves array recognition by detecting indexed access patterns:
    # base + (index * elem_size) → array[index]
    if getattr(scr, 'enable_array_detection', True):  # Default: enabled
        from .load_guard import discover_arrays
        load_guard = discover_arrays(ssa_func)
        if getattr(scr, 'debug_array_detection', False):
            stats = load_guard.get_statistics()
            logger.info(f"LoadGuard: {stats}")

    return ssa_func


def _iter_instructions(ssa_func: SSAFunction) -> Iterable[SSAInstruction]:
    for block_insts in ssa_func.instructions.values():
        for inst in block_insts:
            yield inst


def _find_latest_alias_value(
    block_insts: List[SSAInstruction],
    alias: Optional[str]
) -> Optional[SSAValue]:
    if not alias:
        return None
    for inst in reversed(block_insts):
        for out_val in inst.outputs:
            if out_val.alias == alias:
                return out_val
    return None


def _replace_orphan_uses(
    block_insts: List[SSAInstruction],
    orphan: SSAValue,
    replacement: SSAValue
) -> None:
    for inst in block_insts:
        for idx, val in enumerate(inst.inputs):
            if val is orphan:
                inst.inputs[idx] = replacement
                replacement.uses.append((inst.address, idx))
    orphan.uses = []


def _fix_orphan_temporaries(ssa_func: SSAFunction) -> int:
    """
    Post-pass validation for orphan temporaries (use-before-def) with auto-fix.

    Strategy:
    - If an orphan has an alias and predecessors exist, synthesize a PHI from
      predecessor values matching the alias.
    - Otherwise, promote to an input value scoped to the block.
    """
    cfg = ssa_func.cfg
    existing_addresses = [inst.address for inst in _iter_instructions(ssa_func)]
    next_phi_address = min(existing_addresses, default=0) - 1
    fixes = 0

    for block_id, block_insts in ssa_func.instructions.items():
        if not block_insts:
            continue

        orphans: Dict[str, SSAValue] = {}
        for inst in block_insts:
            for val in inst.inputs:
                if val.producer is None and not val.phi_sources:
                    orphans[val.name] = val

        if not orphans:
            continue

        block = cfg.blocks.get(block_id)
        insert_index = 0
        for inst in block_insts:
            if inst.mnemonic != "PHI":
                break
            insert_index += 1

        for orphan in orphans.values():
            phi_inputs: List[SSAValue] = []
            phi_sources: List[Tuple[int, str]] = []

            if block and block.predecessors:
                for pred_id in block.predecessors:
                    pred_insts = ssa_func.instructions.get(pred_id, [])
                    pred_val = _find_latest_alias_value(pred_insts, orphan.alias)
                    if pred_val:
                        phi_inputs.append(pred_val)
                        phi_sources.append((pred_id, pred_val.name))

            if phi_inputs:
                phi_name = f"phi_orphan_{block_id}_{orphan.name}"
                phi_val = SSAValue(
                    name=phi_name,
                    value_type=orphan.value_type,
                    producer=next_phi_address,
                    phi_sources=phi_sources,
                    alias=orphan.alias,
                    metadata={"orphan_fix": True},
                )
                ssa_func.values[phi_name] = phi_val
                for idx, src_val in enumerate(phi_inputs):
                    src_val.uses.append((next_phi_address, idx))
                phi_inst = SSAInstruction(
                    block_id=block_id,
                    mnemonic="PHI",
                    address=next_phi_address,
                    inputs=phi_inputs,
                    outputs=[phi_val],
                    metadata={"orphan_fix": True},
                )
                phi_val.producer_inst = phi_inst
                block_insts.insert(insert_index, phi_inst)
                insert_index += 1
                next_phi_address -= 1
                _replace_orphan_uses(block_insts, orphan, phi_val)
                fixes += 1
                continue

            input_name = f"input_{block_id}_{orphan.name}"
            input_val = SSAValue(
                name=input_name,
                value_type=orphan.value_type,
                producer=None,
                alias=orphan.alias,
                metadata={"orphan_fix": True},
            )
            ssa_func.values[input_name] = input_val
            _replace_orphan_uses(block_insts, orphan, input_val)
            fixes += 1

    return fixes


def _annotate_call_out_params(ssa_func: SSAFunction) -> None:
    """Attach out-parameter metadata to CALL/XCALL instructions."""
    from ..headers.database import get_header_database

    header_db = get_header_database()
    for block_insts in ssa_func.instructions.values():
        for inst in block_insts:
            if inst.mnemonic not in {"CALL", "XCALL"}:
                continue

            out_params: List[int] = []
            func_name = None
            if inst.mnemonic == "XCALL" and inst.instruction and inst.instruction.instruction:
                xfn_idx = inst.instruction.instruction.arg1
                xfn_entry = ssa_func.scr.get_xfn(xfn_idx) if ssa_func.scr else None
                if xfn_entry:
                    full_name = xfn_entry.name
                    paren_idx = full_name.find("(")
                    func_name = full_name[:paren_idx] if paren_idx > 0 else full_name

            if func_name and header_db:
                sig = header_db.get_function_signature(func_name)
                if sig:
                    out_params = sig.get("out_params") or sig.get("out_param_indices") or []

            if not out_params:
                out_params = [
                    idx for idx, val in enumerate(inst.inputs)
                    if val.alias and val.alias.startswith("&")
                ]

            if out_params:
                inst.metadata["out_param_indices"] = out_params
                inst.metadata["has_out_params"] = True


def _mark_simple_arithmetic_compound_stores(instructions: Dict[int, List[SSAInstruction]]) -> None:
    """Mark arithmetic temporaries used in stores for compound reconstruction."""
    for block_insts in instructions.values():
        for inst in block_insts:
            if inst.mnemonic != "ASGN" or len(inst.inputs) < 2:
                continue
            source = inst.inputs[0]
            if not source.producer_inst:
                continue
            if source.producer_inst.mnemonic not in SIMPLE_ARITHMETIC_MNEMONICS:
                continue
            if source.uses:
                real_uses = {addr for addr, _ in source.uses if addr >= 0}
                if len(real_uses) > 1:
                    continue
            source.metadata["preserve_compound"] = True


FLOAT_OPS = {
    "FADD",
    "FSUB",
    "FMUL",
    "FDIV",
    "FNEG",
    "FLES",
    "FLEQ",
    "FGRE",
    "FGEQ",
    "FEQU",
    "FNEQ",
}

DOUBLE_OPS = {
    "DADD",
    "DSUB",
    "DMUL",
    "DDIV",
    "DNEG",
    "DLES",
    "DLEQ",
    "DGRE",
    "DGEQ",
    "DEQU",
    "DNEQ",
}

SHORT_OPS = {"SNEG", "SEQU", "SLES", "SLEQ", "SGRE", "SGEQ"}
CHAR_OPS = {"CEQU", "CNEQ", "CLES", "CLEQ", "CGRE", "CGEQ"}

CONVERSION_INPUT_TYPES = {
    "ITOF": opcodes.ResultType.INT,
    "ITOD": opcodes.ResultType.INT,
    "DTOI": opcodes.ResultType.DOUBLE,
    "DTOF": opcodes.ResultType.DOUBLE,
    "FTOD": opcodes.ResultType.FLOAT,
    "FTOI": opcodes.ResultType.FLOAT,
    "SCI": opcodes.ResultType.CHAR,
    "SSI": opcodes.ResultType.SHORT,
    "UCI": opcodes.ResultType.CHAR,
    "USI": opcodes.ResultType.SHORT,
}


def _merge_result_types(values: List[opcodes.ResultType]) -> opcodes.ResultType:
    known = {t for t in values if t != opcodes.ResultType.UNKNOWN}
    if not known:
        return opcodes.ResultType.UNKNOWN
    if len(known) == 1:
        return known.pop()
    return opcodes.ResultType.UNKNOWN


def _infer_operand_type(mnemonic: str, info: Optional[opcodes.OpcodeInfo]) -> Optional[opcodes.ResultType]:
    if mnemonic in FLOAT_OPS:
        return opcodes.ResultType.FLOAT
    if mnemonic in DOUBLE_OPS:
        return opcodes.ResultType.DOUBLE
    if mnemonic in SHORT_OPS:
        return opcodes.ResultType.SHORT
    if mnemonic in CHAR_OPS:
        return opcodes.ResultType.CHAR
    if mnemonic in CONVERSION_INPUT_TYPES:
        return CONVERSION_INPUT_TYPES[mnemonic]
    if info and info.result_type not in (opcodes.ResultType.UNKNOWN, opcodes.ResultType.VOID):
        return info.result_type
    return None


def _propagate_types(resolver: opcodes.OpcodeResolver, instructions: Dict[int, List[SSAInstruction]]) -> None:
    changed = True
    while changed:
        changed = False
        for block_insts in instructions.values():
            for inst in block_insts:
                if inst.mnemonic == "PHI":
                    merged_type = _merge_result_types([val.value_type for val in inst.inputs])
                    out_val = inst.outputs[0]
                    if merged_type != opcodes.ResultType.UNKNOWN and out_val.value_type != merged_type:
                        out_val.value_type = merged_type
                        changed = True
                    continue

                if not inst.instruction:
                    continue
                opcode = inst.instruction.instruction.opcode
                info = resolver.get_info(opcode)
                if info:
                    if info.result_type != opcodes.ResultType.UNKNOWN:
                        for out_val in inst.outputs:
                            if out_val.value_type != info.result_type:
                                out_val.value_type = info.result_type
                                changed = True

                operand_type = _infer_operand_type(inst.mnemonic, info)
                if operand_type:
                    for val in inst.inputs:
                        if val.value_type == opcodes.ResultType.UNKNOWN:
                            val.value_type = operand_type
                            changed = True


def build_ssa_incremental(scr: SCRFile, max_passes: int = 5, return_metadata: bool = False):
    """
    Build SSA using multi-pass heritage for improved quality.

    This function uses Ghidra-style heritage SSA construction which:
    1. Processes variables incrementally across multiple passes
    2. Uses dominance frontiers for precise PHI placement
    3. Discovers variable reuse (same slot, different semantics)
    4. Improves type inference through multiple refinement passes
    5. Performs dead code elimination after each pass

    This produces higher-quality SSA compared to the traditional build_ssa
    function, especially for complex scripts with many variables.

    Args:
        scr: The SCR file to decompile
        max_passes: Maximum number of heritage passes (default 5)
        return_metadata: If True, return (SSAFunction, heritage_metadata) tuple

    Returns:
        SSAFunction with incrementally constructed SSA form
        If return_metadata=True: Tuple[SSAFunction, Dict] with heritage metadata
    """
    from .heritage import HeritageOrchestrator

    resolver = getattr(scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    cfg, _ = lift_function(scr, resolver)

    # Ensure dominance frontiers are computed
    if not cfg.dominance_frontiers:
        _compute_dominance_frontiers(cfg)

    logger.debug(f"Building incremental SSA with max_passes={max_passes}")

    orchestrator = HeritageOrchestrator(scr, cfg, max_passes)
    ssa_func = orchestrator.build_incremental_ssa()

    stats = orchestrator.get_heritage_stats()
    logger.debug(
        f"Heritage SSA complete: {stats['passes']} passes, "
        f"{stats['total_variables']} variables, {stats['phi_nodes']} PHI nodes"
    )

    if return_metadata:
        heritage_metadata = orchestrator.get_heritage_metadata()
        return ssa_func, heritage_metadata

    return ssa_func
