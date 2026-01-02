"""
Stack-based VM lifting utilities.

Converts sequences of instructions into pseudo-register operations
by tracking the evaluation stack.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple, Callable

from ..loader.scr_loader import Instruction, SCRFile
from ..disasm import opcodes
from .cfg import CFG, build_cfg, BasicBlock


def _to_signed(val: int) -> int:
    return val - 0x100000000 if val >= 0x80000000 else val


def _stack_alias_from_offset(offset: int) -> str:
    signed = _to_signed(offset)
    if signed < 0:
        # Special case: -3 is return value slot
        if signed == -3:
            return "retval"
        # Parameters: -4=param_0, -8=param_1, -12=param_2, etc.
        param_idx = (abs(signed) - 4) // 4
        return f"param_{param_idx}"
    # FIX 2: Use BYTE offset, not dword index!
    # Compiler uses byte-level addressing (offset 8, 9, 10, 11, ...)
    # NOT dword-aligned (0, 4, 8, 12, ...)
    # This prevents collisions like offset 8,9,10,11 all mapping to local_2
    return f"local_{signed}"


def _is_return_value_store(instr: Instruction, stack: List, resolver: opcodes.OpcodeResolver) -> bool:
    """
    Detect LLD [sp-3] pattern used to store return values before RET.
    In this context, LLD should pop a value from stack (pops=1, pushes=0).
    Otherwise, LLD loads from stack offset and pushes to eval stack (pops=0, pushes=1).
    """
    mnemonic = resolver.get_mnemonic(instr.opcode)
    if mnemonic != "LLD":
        return False
    offset = _to_signed(instr.arg1)
    # LLD [sp-3] with values on stack = store to return value slot
    return offset == -3 and len(stack) > 0


def _derive_alias(instr: Instruction, resolver: opcodes.OpcodeResolver) -> Optional[str]:
    mnemonic = resolver.get_mnemonic(instr.opcode)

    # LCP/LLD: Load value from stack offset
    if mnemonic in {"LCP", "LLD"}:
        return _stack_alias_from_offset(instr.arg1)

    # LADR: Load address of stack variable - add & prefix
    if mnemonic == "LADR":
        base = _stack_alias_from_offset(instr.arg1)
        return f"&{base}"

    # GCP/GLD: Load value from data segment
    if mnemonic in {"GCP", "GLD"}:
        return f"data_{instr.arg1}"

    # GADR: Load address from data segment
    if mnemonic == "GADR":
        return f"&data_{instr.arg1}"

    # DADR: Pointer arithmetic - no static alias, derives from stack input
    # DADR pops address from stack, adds offset, pushes result
    # Alias will be derived from the input value's alias during lifting
    return None


@dataclass
class StackValue:
    name: str
    producer: Optional[Instruction] = None
    value_type: opcodes.ResultType = opcodes.ResultType.UNKNOWN
    phi_sources: Optional[List[Tuple[int, "StackValue"]]] = None
    alias: Optional[str] = None


@dataclass
class LiftedInstruction:
    instruction: Instruction
    inputs: List[StackValue]
    outputs: List[StackValue]


def _infer_phi_type(candidates: Sequence[StackValue]) -> opcodes.ResultType:
    """Best-effort type inference for phi nodes based on incoming values."""
    types = {val.value_type for val in candidates if val.value_type != opcodes.ResultType.UNKNOWN}
    if len(types) == 1:
        return types.pop()
    return opcodes.ResultType.UNKNOWN


def _merge_stacks(
    pred_states: Sequence[Tuple[int, List[StackValue]]],
    block: BasicBlock,
    phi_name_fn: Callable[[int, int], str],
) -> List[StackValue]:
    if not pred_states:
        return []

    lengths = {len(state) for _, state in pred_states}
    max_len = max(lengths) if lengths else 0

    merged: List[StackValue] = []
    for depth in range(max_len):
        candidates: List[Tuple[int, StackValue]] = []
        for pred_id, state in pred_states:
            if depth < len(state):
                candidates.append((pred_id, state[depth]))

        if not candidates:
            continue

        names = {val.name for _, val in candidates}
        if len(names) == 1 and len(candidates) == len(pred_states):
            merged.append(candidates[0][1])
            continue

        alias_candidates = {val.alias for _, val in candidates if val.alias}
        alias = alias_candidates.pop() if len(alias_candidates) == 1 else None
        phi_value = StackValue(
            name=phi_name_fn(block.block_id, depth),
            producer=None,
            value_type=_infer_phi_type([val for _, val in candidates]),
            phi_sources=candidates,
            alias=alias,
        )
        merged.append(phi_value)

    return merged


def lift_basic_block(block_id: int, cfg: CFG, resolver: Optional[opcodes.OpcodeResolver] = None, phi_name_fn: Optional[Callable[[int, int], str]] = None, scr: Optional["SCRFile"] = None) -> List[LiftedInstruction]:
    block = cfg.get_block(block_id)
    instructions = block.instructions
    if not instructions:
        return []

    resolver = resolver or opcodes.DEFAULT_RESOLVER
    predecessor_states: List[Tuple[int, List[StackValue]]] = []
    # gather outgoing stack states from predecessors if available
    for pred_id in block.predecessors:
        pred_block = cfg.get_block(pred_id)
        state = getattr(pred_block, "_out_stack", None)
        if state is not None:
            predecessor_states.append((pred_id, state))
    if not predecessor_states or block_id == cfg.entry_block:
        stack: List[StackValue] = []
    else:
        merge_fn = phi_name_fn or (lambda b, d: f"phi_{b}_{d}")
        stack = _merge_stacks(predecessor_states, block, merge_fn)
    block._in_stack = stack.copy()  # type: ignore[attr-defined]
    lifted: List[LiftedInstruction] = []

    for instr in instructions:
        info = resolver.get_info(instr.opcode)

        # FÁZE 1.6: Handle context-dependent LLD behavior
        # LLD has two usage patterns:
        # 1. LLD [sp-3] with value on stack = store to return slot (pops=1, pushes=0)
        # 2. LLD [sp+offset] = load from stack offset to eval stack (pops=0, pushes=1)
        if _is_return_value_store(instr, stack, resolver):
            pops, pushes = 1, 0  # Store pattern
        else:
            pops = info.pops if info else 0
            pushes = info.pushes if info else 0

        inputs: List[StackValue] = []
        for pop_idx in range(pops):
            if stack:
                inputs.insert(0, stack.pop())
            else:
                fake_name = f"unknown_{block.block_id}_{instr.address}_{pop_idx}"
                fake = StackValue(name=fake_name, producer=None, value_type=opcodes.ResultType.UNKNOWN)
                inputs.insert(0, fake)

        outputs: List[StackValue] = []
        inferred_alias = _derive_alias(instr, resolver)
        for idx in range(pushes):
            result_type = info.result_type if info else opcodes.ResultType.UNKNOWN
            alias = inferred_alias if idx == 0 else None
            stack_val = StackValue(
                name=f"t{instr.address}_{idx}",
                producer=instr,
                value_type=result_type,
                alias=alias,
            )
            stack.append(stack_val)
            outputs.append(stack_val)

        # Special handling for XCALL and CALL: capture stack values as arguments
        mnemonic = resolver.get_mnemonic(instr.opcode)
        if mnemonic == "XCALL" and stack:
            # XCALL consumes arguments from stack - we'll capture current stack state
            # The actual arg count will be determined by SSP after XCALL
            # For now, store stack snapshot for later processing
            instr._xcall_stack_snapshot = stack.copy()  # type: ignore[attr-defined]
        elif mnemonic == "CALL" and stack:
            # CALL also consumes arguments from stack (similar pattern)
            # Arguments are pushed via ASP/LADR/value/ASGN sequences, but end up on eval stack
            instr._call_stack_snapshot = stack.copy()  # type: ignore[attr-defined]

        lifted.append(LiftedInstruction(instruction=instr, inputs=inputs, outputs=outputs))

    # Post-process: find XCALL+SSP pairs and assign arguments
    _assign_xcall_arguments(lifted, resolver, scr)
    # Post-process: find CALL patterns and assign arguments
    _assign_call_arguments(lifted, resolver, scr)

    block._out_stack = stack  # type: ignore[attr-defined]
    return lifted


def _assign_xcall_arguments(lifted: List[LiftedInstruction], resolver: opcodes.OpcodeResolver, scr: Optional["SCRFile"] = None) -> None:
    """Post-process lifted instructions to assign XCALL arguments from stack snapshots."""
    for i, inst in enumerate(lifted):
        mnemonic = resolver.get_mnemonic(inst.instruction.opcode)
        if mnemonic != "XCALL":
            continue

        # Get stack snapshot captured during lifting
        stack_snapshot = getattr(inst.instruction, "_xcall_stack_snapshot", None)
        if not stack_snapshot:
            continue

        # Try to get arg count from XFN table first
        arg_count = 0
        is_variadic = False
        if scr:
            xfn_idx = inst.instruction.arg1
            xfn_entry = scr.get_xfn(xfn_idx)
            if xfn_entry:
                if xfn_entry.arg_count != 0xFFFFFFFF:  # Not variadic
                    arg_count = xfn_entry.arg_count
                else:
                    is_variadic = True

        # For variadic functions or missing XFN, use SSP after XCALL
        if arg_count == 0:
            for j in range(i + 1, min(i + 3, len(lifted))):
                next_mnemonic = resolver.get_mnemonic(lifted[j].instruction.opcode)
                if next_mnemonic == "SSP":
                    ssp_arg = lifted[j].instruction.arg1
                    if ssp_arg > 0:
                        arg_count = ssp_arg
                    break

        # REMOVED: Flawed variadic string detection logic
        # The compiler pushes arguments in left-to-right order, then pushes 1 metadata value
        # before XCALL. We need to skip this metadata value.

        # Assign XCALL inputs: skip the metadata value at stack top
        #
        # Stack layout before XCALL FOR VARIADIC FUNCTIONS:
        #   [..., arg0, arg1, arg2, ..., argN-1, metadata]
        #
        # SSP after XCALL says to remove N arguments (not including metadata)
        # So we need stack[-(N+1):-1] to get [arg0, ..., argN-1]
        #
        # FOR NON-VARIADIC FUNCTIONS: No metadata, just take last N values
        #   [..., arg0, arg1, ..., argN-1]
        # So we need stack[-N:]
        #
        if arg_count > 0:
            if is_variadic and len(stack_snapshot) > arg_count:
                # Variadic: skip metadata value at top
                args = stack_snapshot[-(arg_count + 1):-1]
                inst.inputs = args
            elif len(stack_snapshot) >= arg_count:
                # Non-variadic OR edge case: take last N values
                args = stack_snapshot[-arg_count:]
                inst.inputs = args


def _assign_call_arguments(lifted: List[LiftedInstruction], resolver: opcodes.OpcodeResolver, scr: Optional["SCRFile"] = None) -> None:
    """
    Post-process lifted instructions to assign CALL arguments from stack snapshots.

    CALL pattern analysis from bytecode:

    func_0010(info->field_16):
        ASP 1          ; Allocate stack slot
        LADR [sp-4]    ; Address on eval stack
        DADR 16        ; Modified address on eval stack
        DCP 4          ; VALUE on eval stack ← THIS IS THE ARGUMENT
        ASP 1          ; Stack cleanup
        CALL func_0010 ; Argument is on eval stack

    func_0096():  (no arguments)
        <prev operation leaves value on eval stack>
        SSP 1          ; Clean up that value
        CALL func_0096 ; No arguments!

    Key insight: Look for values PRODUCED RECENTLY (last 1-3 instructions before CALL).
    Old values on stack are leftovers, not arguments.
    """
    for i, inst in enumerate(lifted):
        mnemonic = resolver.get_mnemonic(inst.instruction.opcode)
        if mnemonic != "CALL":
            continue

        # Get stack snapshot captured during lifting
        stack_snapshot = getattr(inst.instruction, "_call_stack_snapshot", None)
        if not stack_snapshot:
            continue

        # Find values that were pushed to stack in the last few instructions before CALL
        # These are likely arguments
        recent_values = []  # Use list instead of set since StackValue is not hashable
        for j in range(max(0, i - 6), i):  # Look back 6 instructions
            prev_inst = lifted[j]
            prev_mnemonic = resolver.get_mnemonic(prev_inst.instruction.opcode)

            # Stop at control flow (new basic block starts, can't be same argument chain)
            if prev_mnemonic in {"JZ", "JNZ", "JMP", "JE", "JNE"}:
                recent_values.clear()  # Reset - arguments must be after control flow
                continue

            # Stop at previous CALL/XCALL (separate operation)
            if prev_mnemonic in {"CALL", "XCALL"}:
                recent_values.clear()
                continue

            # SSP before CALL means values are being REMOVED, not added for arguments
            if prev_mnemonic == "SSP":
                recent_values.clear()  # Values removed = no arguments follow
                continue

            # Track values produced by this instruction
            if prev_inst.outputs:
                for out_val in prev_inst.outputs:
                    if out_val not in recent_values:  # Avoid duplicates
                        recent_values.append(out_val)

        # Extract arguments: stack values that were produced recently
        # Maintain order from stack (last pushed = rightmost argument)
        args = []
        for stack_val in stack_snapshot:
            if stack_val in recent_values:
                args.append(stack_val)

        # Assign arguments to CALL
        if args:
            inst.inputs = args


def lift_function(scr: SCRFile, resolver: Optional[opcodes.OpcodeResolver] = None) -> Tuple[CFG, Dict[int, List[LiftedInstruction]]]:
    resolver = resolver or getattr(scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    cfg = build_cfg(scr, resolver)
    lifted: Dict[int, List[LiftedInstruction]] = {}
    phi_counter = 0

    def phi_name_fn(block_id: int, depth: int) -> str:
        nonlocal phi_counter
        name = f"phi_{block_id}_{depth}_{phi_counter}"
        phi_counter += 1
        return name

    # Process ALL blocks in the CFG, not just reachable from entry
    # This ensures we don't lose data when entry point detection is complex
    order = sorted(cfg.blocks.keys())
    for block_id in order:
        lifted[block_id] = lift_basic_block(block_id, cfg, resolver, phi_name_fn, scr)
    return cfg, lifted
