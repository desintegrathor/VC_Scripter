"""
Stack-based VM lifting utilities.

Converts sequences of instructions into pseudo-register operations
by tracking the evaluation stack.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Set, Tuple, Callable
import logging

from ..loader.scr_loader import Instruction, SCRFile
from ..disasm import opcodes
from .cfg import CFG, build_cfg, BasicBlock

logger = logging.getLogger(__name__)


SIMPLE_ARITHMETIC_MNEMONICS = {
    "ADD",
    "SUB",
    "IADD",
    "ISUB",
    "FADD",
    "FSUB",
    "DADD",
    "DSUB",
    "CADD",
    "CSUB",
    "SADD",
    "SSUB",
    "INC",
    "DEC",
}


def _to_signed(val: int) -> int:
    return val - 0x100000000 if val >= 0x80000000 else val


def _stack_alias_from_offset(offset: int) -> str:
    signed = _to_signed(offset)
    if signed < 0:
        # Parameters: [sp-4]=param_0, [sp-3]=param_1, [sp-2]=param_2, etc.
        # Note: [sp-3] is SECOND parameter when there are 2+ params
        # The slot at [sp-4] is always the first parameter (param_0)
        #
        # Empirical evidence from bytecode analysis:
        # - SRV_CheckEndRule(float time): uses [sp-4] for its only param
        # - SetFlagStatus(attacking_side, cur_step): uses [sp-4] for param_0, [sp-3] for param_1
        #
        # Formula: param_idx = offset + 4
        # - offset -4 → param_0
        # - offset -3 → param_1
        # - offset -2 → param_2
        param_idx = signed + 4  # -4→0, -3→1, -2→2, etc.
        if param_idx < 0:
            # Offsets below -4 are not valid parameters
            # They might be something else (return address, saved frame, etc.)
            return f"stack_{abs(signed)}"
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


def _is_xcall_return_copy(
    instr: Instruction,
    prev_instr: Optional[Instruction],
    stack: List,
    resolver: opcodes.OpcodeResolver,
    scr: Optional["SCRFile"]
) -> bool:
    """
    Detect LLD [sp+X] after XCALL with return value pattern.

    When LLD immediately follows an XCALL that returns a value, the LLD is copying
    the return value from eval stack to a local variable WITHOUT consuming it.
    In this case, LLD should have pops=0, pushes=0 (copy, not load).

    Pattern:
        XCALL $func_with_return_value
        LLD [sp+X]  ; X > 0, copies ret val to local_X

    The return value stays on eval stack for potential use as argument to next call.
    """
    if not prev_instr:
        return False

    mnemonic = resolver.get_mnemonic(instr.opcode)
    if mnemonic != "LLD":
        return False

    prev_mnemonic = resolver.get_mnemonic(prev_instr.opcode)
    if prev_mnemonic != "XCALL":
        return False

    # Check if the previous XCALL returns a value
    if not scr:
        return False

    xfn_idx = prev_instr.arg1
    returns_value, _ = _get_xcall_return_info(xfn_idx, scr)
    if not returns_value:
        return False

    # Check offset is positive (local variable, not return slot)
    offset = _to_signed(instr.arg1)
    if offset < 0:
        return False

    # Stack should have the return value on it
    return len(stack) > 0


def _get_xcall_return_info(
    xfn_idx: int,
    scr: Optional["SCRFile"],
    sdk_db: Optional[object] = None
) -> Tuple[bool, "opcodes.ResultType"]:
    """
    Determine if an XCALL returns a value and its type.

    Uses XFN table's ret_size field (primary) and SDK database (secondary).

    Args:
        xfn_idx: Index into XFN table
        scr: SCRFile containing XFN table
        sdk_db: Optional SDK database for precise type info

    Returns:
        (returns_value, result_type) tuple
    """
    if not scr:
        return False, opcodes.ResultType.UNKNOWN

    xfn_entry = scr.get_xfn(xfn_idx)
    if not xfn_entry:
        return False, opcodes.ResultType.UNKNOWN

    # Primary: XFN table's ret_size (0 = void, >0 = returns value)
    if xfn_entry.ret_size == 0:
        return False, opcodes.ResultType.VOID

    # Function returns a value - determine type
    result_type = opcodes.ResultType.INT  # Default for non-void

    # Secondary: SDK database for precise type info
    if sdk_db:
        get_sig = getattr(sdk_db, 'get_function_signature', None)
        if get_sig:
            sig = get_sig(xfn_entry.name)
            if sig:
                ret_type = getattr(sig, 'return_type', None)
                if ret_type:
                    if ret_type == "float":
                        result_type = opcodes.ResultType.FLOAT
                    elif ret_type.endswith("*"):
                        result_type = opcodes.ResultType.POINTER

    return True, result_type


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


def _infer_type_from_opcode(mnemonic: str, resolver: opcodes.OpcodeResolver) -> opcodes.ResultType:
    """
    Infer result type from opcode mnemonic using opcode patterns.

    This provides initial type hints during SSA construction, which will be
    refined later by type_inference.py dataflow analysis.

    Args:
        mnemonic: Instruction mnemonic (e.g., 'FADD', 'IADD')
        resolver: OpcodeResolver for looking up instruction info

    Returns:
        ResultType enum value based on opcode evidence
    """
    # Float operations - high confidence
    float_ops = {
        'FADD', 'FSUB', 'FMUL', 'FDIV', 'FNEG',
        'FEQ', 'FNE', 'FGT', 'FGE', 'FLT', 'FLE',
        'FSIN', 'FCOS', 'FTAN', 'FSQRT', 'FABS',
    }
    if mnemonic in float_ops:
        return opcodes.ResultType.FLOAT

    # Integer operations - high confidence
    int_ops = {
        'IADD', 'ISUB', 'IMUL', 'IDIV', 'IMOD', 'INEG',
        'IEQ', 'INE', 'IGT', 'IGE', 'ILT', 'ILE',
        'INC', 'DEC',
    }
    if mnemonic in int_ops:
        return opcodes.ResultType.INT

    # Character operations
    char_ops = {
        'CADD', 'CSUB', 'CMUL', 'CDIV',
        'CEQ', 'CNE', 'CGT', 'CGE', 'CLT', 'CLE',
    }
    if mnemonic in char_ops:
        return opcodes.ResultType.CHAR

    # Short operations
    short_ops = {
        'SADD', 'SSUB', 'SMUL', 'SDIV',
        'SEQ', 'SNE', 'SGT', 'SGE', 'SLT', 'SLE',
    }
    if mnemonic in short_ops:
        return opcodes.ResultType.SHORT

    # Double operations
    double_ops = {
        'DADD', 'DSUB', 'DMUL', 'DDIV', 'DNEG',
        'DEQ', 'DNE', 'DGT', 'DGE', 'DLT', 'DLE',
    }
    if mnemonic in double_ops:
        return opcodes.ResultType.DOUBLE

    # Type conversion opcodes - explicit output type (99% confidence)
    conversions = {
        'ITOF': opcodes.ResultType.FLOAT,
        'FTOI': opcodes.ResultType.INT,
        'FTOD': opcodes.ResultType.DOUBLE,
        'DTOF': opcodes.ResultType.FLOAT,
        'ITOD': opcodes.ResultType.DOUBLE,
        'DTOI': opcodes.ResultType.INT,
        'CTOI': opcodes.ResultType.INT,
        'ITOC': opcodes.ResultType.CHAR,
        'STOI': opcodes.ResultType.INT,
        'ITOS': opcodes.ResultType.SHORT,
    }
    if mnemonic in conversions:
        return conversions[mnemonic]

    # Comparison operations return int (boolean)
    comparison_ops = {
        'FCL', 'FEQ', 'FNE', 'FGT', 'FGE', 'FLT', 'FLE',
        'ICL', 'IEQ', 'INE', 'IGT', 'IGE', 'ILT', 'ILE',
        'CEQ', 'CNE', 'CGT', 'CGE', 'CLT', 'CLE',
        'SEQ', 'SNE', 'SGT', 'SGE', 'SLT', 'SLE',
        'DEQ', 'DNE', 'DGT', 'DGE', 'DLT', 'DLE',
        'LES', 'GRE', 'EQL', 'NEQ',
    }
    if mnemonic in comparison_ops:
        return opcodes.ResultType.INT

    # Pointer operations
    pointer_ops = {'LADR', 'GADR', 'DADR', 'PNT'}
    if mnemonic in pointer_ops:
        return opcodes.ResultType.POINTER

    # Default to UNKNOWN for ambiguous operations (GCP, LCP, DCP without context)
    return opcodes.ResultType.UNKNOWN


@dataclass
class StackValue:
    name: str
    producer: Optional[Instruction] = None
    value_type: opcodes.ResultType = opcodes.ResultType.UNKNOWN
    phi_sources: Optional[List[Tuple[int, "StackValue"]]] = None
    alias: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


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
    prev_instr: Optional[Instruction] = None

    for instr in instructions:
        info = resolver.get_info(instr.opcode)

        # FÁZE 1.6: Handle context-dependent LLD behavior
        # LLD has multiple usage patterns:
        # 1. LLD [sp-3] with value on stack = store to return slot (pops=1, pushes=0)
        # 2. LLD [sp+X] after XCALL with return = copy ret val to local (pops=0, pushes=0)
        # 3. LLD [sp+offset] normal = load from stack offset to eval stack (pops=0, pushes=1)
        if _is_return_value_store(instr, stack, resolver):
            pops, pushes = 1, 0  # Store pattern for function return
        elif _is_xcall_return_copy(instr, prev_instr, stack, resolver, scr):
            pops, pushes = 0, 0  # Copy pattern - ret val stays on stack
            logger.info(f"LLD {instr.arg1} after XCALL: copy pattern (pops=0, pushes=0)")
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
        mnemonic = resolver.get_mnemonic(instr.opcode)

        for idx in range(pushes):
            # Prefer opcode-based type inference over generic result_type
            inferred_type = _infer_type_from_opcode(mnemonic, resolver)

            # Fallback to info.result_type if inference returns UNKNOWN
            if inferred_type == opcodes.ResultType.UNKNOWN and info:
                result_type = info.result_type
            else:
                result_type = inferred_type

            alias = inferred_alias if idx == 0 else None
            metadata = {}
            if mnemonic in SIMPLE_ARITHMETIC_MNEMONICS:
                metadata["simple_arithmetic"] = True

            stack_val = StackValue(
                name=f"t{instr.address}_{idx}",
                producer=instr,
                value_type=result_type,
                alias=alias,
                metadata=metadata,
            )

            # Log type assignment for debugging
            if result_type != opcodes.ResultType.UNKNOWN:
                logger.info(f"Stack lifter assigned type {result_type.name} to {stack_val.name} based on opcode {mnemonic}")

            stack.append(stack_val)
            outputs.append(stack_val)

        # Special handling for XCALL and CALL: capture stack values as arguments
        # IMPORTANT: Snapshot must be captured BEFORE return value is pushed!
        if mnemonic == "XCALL" and stack:
            # XCALL consumes arguments from stack - capture BEFORE return value is added
            instr._xcall_stack_snapshot = stack.copy()  # type: ignore[attr-defined]
        elif mnemonic == "CALL" and stack:
            # CALL also consumes arguments from stack (similar pattern)
            instr._call_stack_snapshot = stack.copy()  # type: ignore[attr-defined]

        # Special handling: XCALL return values
        # XCALL opcode has pushes=0 but external functions CAN return values.
        # Check XFN table's ret_size to determine if we should create an output.
        if mnemonic == "XCALL" and scr:
            xfn_idx = instr.arg1
            returns_value, ret_type = _get_xcall_return_info(xfn_idx, scr)

            if returns_value:
                xfn_entry = scr.get_xfn(xfn_idx)
                func_name = xfn_entry.name if xfn_entry else f"xfn_{xfn_idx}"
                ret_value = StackValue(
                    name=f"t{instr.address}_ret",
                    producer=instr,
                    value_type=ret_type,
                    alias=None,
                )
                stack.append(ret_value)
                outputs.append(ret_value)
                logger.info(f"XCALL {func_name} returns value, created output {ret_value.name}")


        lifted.append(LiftedInstruction(instruction=instr, inputs=inputs, outputs=outputs))
        prev_instr = instr  # Track for next iteration

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


def _simulate_eval_stack_depth(lifted: List[LiftedInstruction],
                                call_idx: int,
                                resolver: opcodes.OpcodeResolver) -> int:
    """
    Simulate eval stack depth before CALL instruction using precise opcode semantics.

    This function tracks the evaluation stack (NOT the frame stack) by simulating
    push/pop operations from the last basic block boundary up to the CALL.

    Key insight: CALL arguments are on the eval stack, while ASP-allocated locals
    are in frame slots. We must distinguish between these two.

    Returns:
        Number of values on eval stack before CALL (= argument count)
    """
    depth = 0
    lookback = 15  # Wide enough for complex expressions

    for j in range(max(0, call_idx - lookback), call_idx):
        inst = lifted[j]
        opcode = inst.instruction.opcode
        mnem = resolver.get_mnemonic(opcode)

        # Reset at basic block boundaries (control flow instructions)
        if mnem in {"JZ", "JNZ", "JMP", "CALL", "XCALL", "RET"}:
            depth = 0
            continue

        # Get opcode info to determine stack effect
        opcode_info = resolver.get_info(opcode)
        if opcode_info:
            # Apply stack effect: depth += (pushes - pops)
            # Note: ASP/SSP have pops=0, pushes=0 (they don't affect eval stack)
            depth -= opcode_info.pops
            depth += opcode_info.pushes
            depth = max(0, depth)  # Stack depth never goes negative

    return depth


def _find_ssp_after_call(lifted: List[LiftedInstruction],
                         call_idx: int,
                         resolver: opcodes.OpcodeResolver) -> Optional[int]:
    """
    Find SSP immediately after CALL (within 3 instructions).

    Returns:
        SSP value if found and reliable, None otherwise.

    SSP is unreliable if there's an LLD/GLD/DLD before it, indicating
    local variable cleanup is included in the SSP value.
    """
    for j in range(call_idx + 1, min(call_idx + 4, len(lifted))):
        mnem = resolver.get_mnemonic(lifted[j].instruction.opcode)

        # Stop at control flow boundaries
        if mnem in {"CALL", "XCALL", "RET", "JZ", "JNZ", "JMP"}:
            return None

        # Found SSP
        if mnem == "SSP":
            # Check if there's LLD before SSP (indicates local var cleanup)
            if j > call_idx + 1:
                prev_mnem = resolver.get_mnemonic(lifted[j-1].instruction.opcode)
                if prev_mnem in {"LLD", "GLD", "DLD"}:
                    # SSP includes local cleanup, unreliable
                    return None

            return lifted[j].instruction.arg1

    return None


def _assign_call_arguments(lifted: List[LiftedInstruction], resolver: opcodes.OpcodeResolver, scr: Optional["SCRFile"] = None) -> None:
    """
    Post-process lifted instructions to assign CALL arguments from stack snapshots.

    Uses hybrid approach combining three methods:
    1. Precise eval stack depth simulation (primary)
    2. SSP after CALL (cross-validation)
    3. Stack snapshot size (constraint)

    This implementation fixes the critical issue where functions with 3+ arguments
    were incorrectly detected as void functions.

    Algorithm:
    - Simulate eval stack depth using opcode pops/pushes metadata
    - Cross-validate with SSP if available
    - Use minimum of both for conservative estimate
    - Constrain by stack snapshot size
    """
    for i, inst in enumerate(lifted):
        mnemonic = resolver.get_mnemonic(inst.instruction.opcode)
        if mnemonic != "CALL":
            continue

        # Get stack snapshot captured during lifting
        stack_snapshot = getattr(inst.instruction, "_call_stack_snapshot", None)
        if not stack_snapshot:
            continue

        # Method 1: Precise eval stack simulation
        stack_depth = _simulate_eval_stack_depth(lifted, i, resolver)

        # Method 2: SSP cross-validation
        ssp_value = _find_ssp_after_call(lifted, i, resolver)

        # Method 3: Determine arg count using hybrid approach
        if ssp_value is not None and stack_depth > 0:
            # Both available - use minimum (conservative)
            arg_count = min(ssp_value, stack_depth)
        elif stack_depth > 0:
            # Only stack depth - use it
            arg_count = stack_depth
        elif ssp_value is not None:
            # Only SSP - use it (but might be unreliable)
            arg_count = ssp_value
        else:
            # Neither available - assume 0 args (void function)
            arg_count = 0

        # Validate against snapshot size
        arg_count = min(arg_count, len(stack_snapshot))

        # Assign arguments from stack snapshot
        if arg_count > 0:
            inst.inputs = stack_snapshot[-arg_count:]
        else:
            inst.inputs = []


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


def lift_function_heritage(
    scr: SCRFile,
    resolver: Optional[opcodes.OpcodeResolver] = None,
    space_filter: Optional[Set[str]] = None
) -> Tuple[CFG, Dict[int, List[LiftedInstruction]]]:
    """
    Lift function with optional filtering by address space.

    This variant of lift_function supports heritage-based SSA construction
    by allowing filtering of which address spaces to process. This enables
    incremental lifting where parameters are processed first, then stack
    variables, then globals.

    Args:
        scr: SCR file to lift
        resolver: Opcode resolver (optional)
        space_filter: Optional set of address spaces to include.
                      Valid values: "stack", "param", "global"
                      If None, all spaces are included.

    Returns:
        Tuple of (CFG, lifted instructions by block)
    """
    resolver = resolver or getattr(scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    cfg = build_cfg(scr, resolver)
    lifted: Dict[int, List[LiftedInstruction]] = {}
    phi_counter = 0

    def phi_name_fn(block_id: int, depth: int) -> str:
        nonlocal phi_counter
        name = f"phi_{block_id}_{depth}_{phi_counter}"
        phi_counter += 1
        return name

    # Process ALL blocks in the CFG
    order = sorted(cfg.blocks.keys())
    for block_id in order:
        block_lifted = lift_basic_block(block_id, cfg, resolver, phi_name_fn, scr)

        # Apply space filter if provided
        if space_filter is not None:
            filtered = []
            for inst in block_lifted:
                mnemonic = resolver.get_mnemonic(inst.instruction.opcode)
                include = _should_include_instruction(mnemonic, inst.instruction, space_filter)
                if include:
                    filtered.append(inst)
            lifted[block_id] = filtered
        else:
            lifted[block_id] = block_lifted

    return cfg, lifted


def _should_include_instruction(
    mnemonic: str,
    instruction: Instruction,
    space_filter: Set[str]
) -> bool:
    """
    Determine if an instruction should be included based on space filter.

    Args:
        mnemonic: Instruction mnemonic
        instruction: The instruction
        space_filter: Set of address spaces to include

    Returns:
        True if instruction operates on an included address space
    """
    # Stack operations (local variables)
    stack_ops = {"LCP", "LLD", "LADR"}
    if mnemonic in stack_ops:
        offset = _to_signed(instruction.arg1)
        if offset >= 0:  # Local stack variable
            return "stack" in space_filter
        elif offset < -2:  # Parameter
            return "param" in space_filter
        else:  # Return slot
            return "stack" in space_filter

    # Global operations
    global_ops = {"GCP", "GLD", "GADR"}
    if mnemonic in global_ops:
        return "global" in space_filter

    # All other instructions are always included
    return True


def collect_variable_definitions(
    lifted: Dict[int, List[LiftedInstruction]],
    resolver: opcodes.OpcodeResolver
) -> Dict[str, Set[int]]:
    """
    Collect definition sites for each variable.

    This information is used for PHI node placement in SSA construction.
    A variable is defined when:
    - LLD stores to a stack slot
    - GLD stores to a global
    - PHI at block entry merges values

    Args:
        lifted: Lifted instructions by block ID
        resolver: Opcode resolver

    Returns:
        Dictionary mapping variable names to sets of block IDs where defined
    """
    var_defs: Dict[str, Set[int]] = {}

    for block_id, insts in lifted.items():
        for inst in insts:
            mnemonic = resolver.get_mnemonic(inst.instruction.opcode)

            # LLD stores to stack variable
            if mnemonic == "LLD":
                offset = _to_signed(inst.instruction.arg1)
                if offset >= 0:
                    var_name = f"local_{offset}"
                elif offset < -2:
                    var_name = f"param_{abs(offset) - 3}"
                else:
                    continue  # Return slot

                if var_name not in var_defs:
                    var_defs[var_name] = set()
                var_defs[var_name].add(block_id)

            # GLD stores to global variable
            elif mnemonic == "GLD":
                offset = inst.instruction.arg1
                var_name = f"data_{offset}"

                if var_name not in var_defs:
                    var_defs[var_name] = set()
                var_defs[var_name].add(block_id)

    return var_defs


def collect_variable_uses(
    lifted: Dict[int, List[LiftedInstruction]],
    resolver: opcodes.OpcodeResolver
) -> Dict[str, Set[int]]:
    """
    Collect use sites for each variable.

    A variable is used when:
    - LCP loads from a stack slot
    - GCP loads from a global
    - LADR/GADR takes address of variable

    Args:
        lifted: Lifted instructions by block ID
        resolver: Opcode resolver

    Returns:
        Dictionary mapping variable names to sets of block IDs where used
    """
    var_uses: Dict[str, Set[int]] = {}

    for block_id, insts in lifted.items():
        for inst in insts:
            mnemonic = resolver.get_mnemonic(inst.instruction.opcode)

            # LCP/LADR loads/references stack variable
            if mnemonic in {"LCP", "LADR"}:
                offset = _to_signed(inst.instruction.arg1)
                if offset >= 0:
                    var_name = f"local_{offset}"
                elif offset < -2:
                    var_name = f"param_{abs(offset) - 3}"
                else:
                    continue

                if var_name not in var_uses:
                    var_uses[var_name] = set()
                var_uses[var_name].add(block_id)

            # GCP/GADR loads/references global variable
            elif mnemonic in {"GCP", "GADR"}:
                offset = inst.instruction.arg1
                var_name = f"data_{offset}"

                if var_name not in var_uses:
                    var_uses[var_name] = set()
                var_uses[var_name].add(block_id)

    return var_uses
