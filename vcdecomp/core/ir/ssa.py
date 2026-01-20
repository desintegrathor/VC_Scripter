"""
SSA graph construction on top of lifted stack values.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ..loader.scr_loader import SCRFile
from ..disasm import opcodes
from .cfg import CFG
from .stack_lifter import lift_function, LiftedInstruction, StackValue


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
    cfg, _ = lift_function(scr, resolver)

    # Lift ALL blocks, not just reachable ones
    from .stack_lifter import lift_basic_block
    lifted: Dict[int, List[LiftedInstruction]] = {}
    phi_counter = 0

    def phi_name_fn(block_id: int, depth: int) -> str:
        nonlocal phi_counter
        name = f"phi_{block_id}_{depth}_{phi_counter}"
        phi_counter += 1
        return name

    # Process ALL blocks in the CFG
    for block_id in sorted(cfg.blocks.keys()):
        lifted[block_id] = lift_basic_block(block_id, cfg, resolver, phi_name_fn, scr)

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
            )
        val = values[stack_val.name]
        if stack_val.phi_sources and not val.phi_sources:
            val.phi_sources = [(pred, src.name) for pred, src in stack_val.phi_sources]
        if val.value_type == opcodes.ResultType.UNKNOWN and stack_val.value_type != opcodes.ResultType.UNKNOWN:
            val.value_type = stack_val.value_type
        if not val.alias and stack_val.alias:
            val.alias = stack_val.alias
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

    _propagate_types(resolver, instructions)

    return SSAFunction(cfg=cfg, values=values, instructions=instructions, scr=scr)


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
