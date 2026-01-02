"""
Structured output experiments.

Tries to recognize control flow patterns:
- Trivial if/else regions (single-block branches)
- Loops (while/do-while patterns using back edge detection)
- Switch/case statements (equality comparisons with constants)
Prints block contents using the expression formatter.
"""

from __future__ import annotations

from typing import Dict, Set, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

from ..disasm import opcodes
from .ssa import SSAFunction
from .expr import format_block_expressions, FormattedExpression, ExpressionFormatter
from .cfg import CFG, NaturalLoop, find_all_loops, find_loops_in_function, dominates
from ...parsing.symbol_db import SymbolDatabase
from .parenthesization import ExpressionContext, is_simple_expression

# Configuration: Show block comments for debugging
SHOW_BLOCK_COMMENTS = False  # Set to True to show "// Block X @addr" comments


def _load_symbol_db() -> Optional[SymbolDatabase]:
    """Load symbol database from compiler/symbol_db.json if available."""
    try:
        # Try to find symbol_db.json in compiler directory
        current = Path(__file__).parent
        while current.parent != current:  # Walk up until root
            symbol_db_path = current / "compiler" / "symbol_db.json"
            if symbol_db_path.exists():
                return SymbolDatabase.load(symbol_db_path)
            current = current.parent
        return None
    except Exception:
        return None


@dataclass
class CaseInfo:
    """Information about one case in a switch statement."""
    value: int                  # Case constant value
    block_id: int              # Block ID for this case body (entry point)
    body_blocks: Set[int] = None  # All blocks in this case body
    has_break: bool = True     # Whether case ends with break (vs fall-through)

    def __post_init__(self):
        if self.body_blocks is None:
            self.body_blocks = {self.block_id}


@dataclass
class SwitchPattern:
    """Detected switch/case pattern."""
    test_var: str              # Variable being tested (e.g., "local_0", "i")
    header_block: int          # Block ID where switch starts
    cases: List[CaseInfo]      # List of cases (value -> block)
    default_block: Optional[int] = None  # Default case block (or None)
    default_body_blocks: Set[int] = None  # All blocks in default body
    exit_block: Optional[int] = None     # Common exit point after switch
    all_blocks: Set[int] = None          # All blocks belonging to this switch

    def __post_init__(self):
        if self.all_blocks is None:
            self.all_blocks = {self.header_block}
            self.all_blocks.update(c.block_id for c in self.cases)
            if self.default_block is not None:
                self.all_blocks.add(self.default_block)
        if self.default_body_blocks is None and self.default_block is not None:
            self.default_body_blocks = {self.default_block}


def _build_start_map(cfg) -> Dict[int, int]:
    return {block.start: block_id for block_id, block in cfg.blocks.items()}


def _dominates(cfg, a: int, b: int) -> bool:
    if a == b:
        return True
    current = b
    idom = cfg.idom
    while current in idom:
        parent = idom[current]
        if parent == a:
            return True
        if parent == current:
            break
        current = parent
    return False


def _format_block_lines_filtered(
    ssa_func: SSAFunction,
    block_id: int,
    indent: str,
    formatter: ExpressionFormatter,
    skip_var: str,
    block_to_if: Optional[Dict[int, IfElsePattern]] = None,
    visited_ifs: Optional[Set[int]] = None,
    emitted_blocks: Optional[Set[int]] = None,
    cfg: Optional[CFG] = None,
    start_to_block: Optional[Dict[int, int]] = None,
    resolver: Optional[opcodes.OpcodeResolver] = None,
    # FÁZE 1.3: Early return/break pattern detection
    early_returns: Optional[Dict[int, tuple]] = None
) -> List[str]:
    """
    Format block expressions but skip the last assignment to a specific variable.

    Used to suppress loop initialization when it's duplicated in for-loop header.
    """
    # Get all expressions for this block
    expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)

    # Find the last assignment to skip_var
    last_assignment_idx = -1
    for i in range(len(expressions) - 1, -1, -1):
        expr = expressions[i]
        text = expr.text.strip().rstrip(';')  # Remove trailing semicolon
        # Check if this expression assigns to skip_var
        # Pattern: "skip_var = ..." or "skip_var++" or "skip_var--" or "++skip_var" or "--skip_var"
        if (text.startswith(f"{skip_var} =") or
            text == f"{skip_var}++" or text == f"{skip_var}--" or
            text == f"++{skip_var}" or text == f"--{skip_var}"):
            last_assignment_idx = i
            break

    # Filter out the last assignment
    if last_assignment_idx >= 0:
        filtered_expressions = expressions[:last_assignment_idx] + expressions[last_assignment_idx + 1:]
    else:
        filtered_expressions = expressions

    return [f"{indent}{expr.text}" for expr in filtered_expressions]


def _format_block_lines(
    ssa_func: SSAFunction,
    block_id: int,
    indent: str,
    formatter: ExpressionFormatter = None,
    # FIX 3B: New params for recursive structure detection
    block_to_if: Optional[Dict[int, IfElsePattern]] = None,
    visited_ifs: Optional[Set[int]] = None,
    emitted_blocks: Optional[Set[int]] = None,
    cfg: Optional[CFG] = None,
    start_to_block: Optional[Dict[int, int]] = None,
    resolver: Optional[opcodes.OpcodeResolver] = None,
    # FÁZE 1.3: Early return/break pattern detection
    early_returns: Optional[Dict[int, tuple]] = None
) -> List[str]:
    """
    Format expressions for a block, with optional recursive structure detection.

    Args:
        ssa_func: SSA function data
        block_id: Block ID to format
        indent: Indentation string
        formatter: Optional ExpressionFormatter to use. If None, creates a new one.
        block_to_if: Map of block IDs to if/else patterns (for recursive detection)
        visited_ifs: Set of if/else headers already rendered (for recursive detection)
        emitted_blocks: Set of blocks already rendered (for recursive detection)
        cfg: Control flow graph (for recursive detection)
        start_to_block: Map of instruction addresses to block IDs (for recursive detection)
        resolver: Opcode resolver (for recursive detection)
        early_returns: Map of block IDs to early return patterns (FÁZE 1.3)

    When formatter is provided, uses it for consistent per-function structure detection.
    When recursive params are provided, can detect and render nested if/else structures.
    """
    # FÁZE 1.1: Check if block already emitted - skip to prevent duplication
    if emitted_blocks is not None and block_id in emitted_blocks:
        return []  # Already rendered, don't duplicate

    # FÁZE 1.3: Check if this block is an early return/break pattern
    if early_returns and block_id in early_returns:
        header_block, exit_block, continue_block, is_negated = early_returns[block_id]

        # Extract condition from SSA
        ssa_block = ssa_func.instructions.get(block_id, [])
        block = cfg.blocks[block_id]
        cond_text = None

        if block.instructions:
            last_instr = block.instructions[-1]

            # FÁZE 1.6: Special check - if there's CALL/XCALL + LLD immediately before JZ,
            # use the function call as the condition instead of the input value
            func_call_cond = None
            jz_index = None
            for idx, inst in enumerate(ssa_block):
                if inst.address == last_instr.address:
                    jz_index = idx
                    break

            if jz_index is not None and jz_index >= 2:
                # Check if pattern is: CALL/XCALL, LLD, (SSP), JZ
                # LLD should be 1-2 instructions before JZ
                import sys
                # print(f"DEBUG early_return block {block_id}: jz_index={jz_index}, checking for CALL+LLD", file=sys.stderr)
                for check_idx in range(jz_index - 1, max(0, jz_index - 3), -1):
                    check_inst = ssa_block[check_idx]
                    # print(f"  check_idx={check_idx}: {check_inst.mnemonic}@{check_inst.address}", file=sys.stderr)
                    if check_inst.mnemonic == "LLD":
                        # print(f"  Found LLD at {check_idx}", file=sys.stderr)
                        # Found LLD, now check if there's CALL/XCALL before it
                        for call_idx in range(check_idx - 1, max(0, check_idx - 3), -1):
                            call_inst = ssa_block[call_idx]
                            # print(f"    call_idx={call_idx}: {call_inst.mnemonic}@{call_inst.address}", file=sys.stderr)
                            if call_inst.mnemonic in {"CALL", "XCALL"}:
                                # Found CALL + LLD pattern! Use this as condition
                                # print(f"  Found CALL/XCALL at {call_idx}! Formatting...", file=sys.stderr)
                                # print(f"  CALL inputs: {[inp.name for inp in call_inst.inputs]}", file=sys.stderr)
                                try:
                                    call_expr = formatter._format_call(call_inst)
                                    # print(f"  Formatted: {call_expr}", file=sys.stderr)
                                    if call_expr.endswith(";"):
                                        call_expr = call_expr[:-1].strip()
                                    func_call_cond = call_expr
                                    # print(f"  func_call_cond set to: {func_call_cond}", file=sys.stderr)
                                except Exception as e:
                                    # print(f"  Exception formatting: {e}", file=sys.stderr)
                                    import traceback
                                    traceback.print_exc(file=sys.stderr)
                                break
                        break

            # Extract condition from SSA
            for ssa_inst in ssa_block:
                if ssa_inst.address == last_instr.address and ssa_inst.inputs:
                    cond_value = ssa_inst.inputs[0]

                    if func_call_cond:
                        # Use function call as condition
                        cond_expr = func_call_cond
                    else:
                        # FÁZE 1.6: Check if condition value comes from function call
                        func_call = _trace_value_to_function_call(ssa_func, cond_value, formatter)
                        if func_call:
                            cond_expr = func_call
                        else:
                            # FIX 3: Pass IN_CONDITION context
                            cond_expr = formatter.render_value(cond_value, context=ExpressionContext.IN_CONDITION)
                            # Only use SSA name if rendered as pure number
                            if cond_expr.lstrip('-').isdigit():
                                alias = cond_value.alias or cond_value.name
                                if alias and not alias.startswith("data_"):
                                    cond_expr = alias

                    # FIX 3: Smart negation - only add parens if needed
                    if is_negated:
                        if is_simple_expression(cond_expr):
                            cond_text = f"!{cond_expr}"
                        else:
                            cond_text = f"!({cond_expr})"
                    else:
                        cond_text = cond_expr
                    break

        if cond_text is None:
            cond_text = f"cond_{block_id}"

        lines = []
        # Render header statements (excluding the conditional jump)
        expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)
        if expressions:
            # Filter out the last expression (conditional jump)
            for expr in expressions[:-1]:
                lines.append(f"{indent}{expr.text}")

        # Render early return/break
        lines.append(f"{indent}if ({cond_text}) break;")

        # Mark blocks as emitted
        emitted_blocks.add(block_id)
        emitted_blocks.add(exit_block)
        # Don't add continue_block - it will be rendered normally after this

        return lines

    # FIX 3B: Check if this block is an if/else header - render recursively
    if (block_to_if and visited_ifs is not None and emitted_blocks is not None and
        block_id in block_to_if and block_id == block_to_if[block_id].header_block and
        block_id not in visited_ifs and cfg and start_to_block and resolver):
        return _render_if_else_recursive(
            block_to_if[block_id], indent, ssa_func, formatter,
            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
            early_returns
        )

    # Regular block formatting
    expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)
    return [f"{indent}{expr.text}" for expr in expressions]


def _is_control_flow_only(ssa_block: List, resolver: opcodes.OpcodeResolver) -> bool:
    """
    Check if block contains only control flow instructions (no visible statements).

    Args:
        ssa_block: List of SSA instructions in the block
        resolver: Opcode resolver for checking instruction types

    Returns:
        True if block has only jumps/returns (empty from user perspective)
    """
    if not ssa_block:
        return True

    for inst in ssa_block:
        # PHI nodes are synthetic SSA instructions, not user code - skip them
        if inst.mnemonic == "PHI":
            continue

        # Get opcode from underlying instruction: SSAInstruction -> LiftedInstruction -> Instruction
        if inst.instruction and inst.instruction.instruction:
            opcode = inst.instruction.instruction.opcode
            # If any instruction is NOT a control flow instruction, block has content
            if not (resolver.is_jump(opcode) or resolver.is_return(opcode)):
                return False

    return True


def _render_if_else_recursive(
    if_pattern: IfElsePattern,
    indent: str,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    block_to_if: Dict[int, IfElsePattern],
    visited_ifs: Set[int],
    emitted_blocks: Set[int],
    cfg: CFG,
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver,
    # FÁZE 1.3: Early return/break pattern detection
    early_returns: Optional[Dict[int, tuple]] = None
) -> List[str]:
    """
    Recursively render if/else with nested structures.

    This allows if/else patterns to be properly nested inside other structures
    like switch cases.

    Args:
        if_pattern: The if/else pattern to render
        indent: Current indentation
        ssa_func: SSA function data
        formatter: Expression formatter
        block_to_if: Map of block IDs to if/else patterns
        visited_ifs: Set to track rendered if/else headers
        emitted_blocks: Set to track rendered blocks
        cfg: Control flow graph
        start_to_block: Address to block ID map
        resolver: Opcode resolver

    Returns:
        List of rendered lines
    """
    lines = []
    ssa_blocks = ssa_func.instructions

    # Mark this if/else as visited
    visited_ifs.add(if_pattern.header_block)

    # Get header block
    header_block = cfg.blocks[if_pattern.header_block]

    # NEW: Check if this is a compound condition pattern
    compound = getattr(if_pattern, 'compound', None)
    if compound is not None:
        # This is a compound condition (AND/OR chain)
        # Render using _combine_conditions helper
        cond_text = _combine_conditions(
            compound.conditions,
            compound.operator,
            preserve_style=True  # Match original formatting
        )

        # Mark all involved blocks as emitted to prevent duplicate rendering
        for involved_block in compound.involved_blocks:
            emitted_blocks.add(involved_block)

        # Render the if statement with compound condition
        lines.append(f"{indent}if ({cond_text}) {{")

        # Render true body
        true_block_lines = _format_block_lines(
            ssa_func, compound.true_target, indent + "    ", formatter,
            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
            early_returns
        )
        lines.extend(true_block_lines)

        # Mark TRUE body as emitted to prevent duplication
        emitted_blocks.add(compound.true_target)

        lines.append(f"{indent}}}")

        return lines

    # Extract condition from SSA (simple if/else case)
    cond_text = None
    ssa_block = ssa_blocks.get(if_pattern.header_block, [])

    # FÁZE 1.6: Check if there's CALL/XCALL + LLD immediately before JZ/JNZ
    func_call_cond = None
    if header_block.instructions:
        last_instr = header_block.instructions[-1]
        jz_index = None
        for idx, inst in enumerate(ssa_block):
            if inst.address == last_instr.address:
                jz_index = idx
                break

        if jz_index is not None and jz_index >= 2:
            # Check if pattern is: CALL/XCALL, LLD, (SSP), JZ/JNZ
            for check_idx in range(jz_index - 1, max(0, jz_index - 3), -1):
                check_inst = ssa_block[check_idx]
                if check_inst.mnemonic == "LLD":
                    # Found LLD, now check if there's CALL/XCALL before it
                    for call_idx in range(check_idx - 1, max(0, check_idx - 3), -1):
                        call_inst = ssa_block[call_idx]
                        if call_inst.mnemonic in {"CALL", "XCALL"}:
                            # Found CALL + LLD pattern! Use this as condition
                            try:
                                call_expr = formatter._format_call(call_inst)
                                if call_expr.endswith(";"):
                                    call_expr = call_expr[:-1].strip()
                                func_call_cond = call_expr
                            except Exception:
                                pass
                            break
                    break

    if header_block.instructions:
        last_instr = header_block.instructions[-1]
        mnemonic = resolver.get_mnemonic(last_instr.opcode)
        for ssa_inst in ssa_block:
            if ssa_inst.address == last_instr.address and ssa_inst.inputs:
                cond_value = ssa_inst.inputs[0]

                # FÁZE 1.6: Use function call if detected
                if func_call_cond:
                    cond_expr = func_call_cond
                else:
                    # FIX 3: Pass IN_CONDITION context
                    cond_expr = formatter.render_value(cond_value, context=ExpressionContext.IN_CONDITION)
                    # Only use SSA name if rendered as pure number
                    if cond_expr.lstrip('-').isdigit():
                        alias = cond_value.alias or cond_value.name
                        if alias and not alias.startswith("data_"):
                            cond_expr = alias
                # FÁZE 3 FIX: NO negation needed - we already swapped true/false branches
                # in _detect_if_else_pattern based on JZ vs JNZ semantics
                # FIX 3: No hardcoded parens - expression already has them if needed
                cond_text = cond_expr
                break
    if cond_text is None:
        cond_text = f"cond_{if_pattern.header_block}"

    # Render header block statements (excluding conditional jump)
    # Only add comment if block has actual statements
    if SHOW_BLOCK_COMMENTS and not _is_control_flow_only(ssa_block, resolver):
        lines.append(f"{indent}// Block {if_pattern.header_block} @{header_block.start}")

    # Get header statements (excluding the conditional jump)
    header_lines = _format_block_lines(
        ssa_func, if_pattern.header_block, indent, formatter,
        None, None, None, None, None, None,  # Disable recursion for header itself
        early_returns
    )
    # Remove last line if it's the conditional jump
    if header_lines and ("goto" in header_lines[-1] or "if (" in header_lines[-1]):
        header_lines = header_lines[:-1]

    # FÁZE 1.6: If we detected a function call as condition, remove the call statement
    # from header_lines to avoid duplication
    if func_call_cond and header_lines:
        # The last statement might be the function call - check and remove if so
        for i in range(len(header_lines) - 1, -1, -1):
            line = header_lines[i].strip()
            # Check if line contains XCALL or CALL by looking for known patterns
            if (line.startswith("SC_") or line.startswith("func_")) and line.endswith(";"):
                # This is likely the function call statement
                header_lines = header_lines[:i] + header_lines[i+1:]
                break

    lines.extend(header_lines)

    # Render if statement
    lines.append(f"{indent}if ({cond_text}) {{")

    # Render true branch (recursively)
    true_body_sorted = sorted(if_pattern.true_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
    for body_block_id in true_body_sorted:
        # FÁZE 1.1: Skip already emitted blocks
        if body_block_id in emitted_blocks:
            continue
        body_block = cfg.blocks.get(body_block_id)
        if body_block:
            # Recursive call - will detect nested if/else
            ssa_block = ssa_blocks.get(body_block_id, [])
            if not _is_control_flow_only(ssa_block, resolver):
                if SHOW_BLOCK_COMMENTS: lines.append(f"{indent}    // Block {body_block_id} @{body_block.start}")
            lines.extend(_format_block_lines(
                ssa_func, body_block_id, indent + "    ", formatter,
                block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                early_returns
            ))

            # DEAD CODE ELIMINATION: Stop if block ends with return
            if body_block.instructions:
                last_instr = body_block.instructions[-1]
                if resolver.is_return(last_instr.opcode):
                    break  # Remaining blocks are unreachable

    # Render false branch if exists
    if if_pattern.false_body:
        lines.append(f"{indent}}} else {{")

        # Render false branch (recursively)
        false_body_sorted = sorted(if_pattern.false_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
        for body_block_id in false_body_sorted:
            # FÁZE 1.1: Skip already emitted blocks
            if body_block_id in emitted_blocks:
                continue
            body_block = cfg.blocks.get(body_block_id)
            if body_block:
                # Recursive call - will detect nested if/else
                ssa_block = ssa_blocks.get(body_block_id, [])
                if not _is_control_flow_only(ssa_block, resolver):
                    if SHOW_BLOCK_COMMENTS: lines.append(f"{indent}    // Block {body_block_id} @{body_block.start}")
                lines.extend(_format_block_lines(
                    ssa_func, body_block_id, indent + "    ", formatter,
                    block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                    early_returns
                ))

                # DEAD CODE ELIMINATION: Stop if block ends with return
                if body_block.instructions:
                    last_instr = body_block.instructions[-1]
                    if resolver.is_return(last_instr.opcode):
                        break  # Remaining blocks are unreachable

    lines.append(f"{indent}}}")

    # Mark all blocks as emitted
    emitted_blocks.add(if_pattern.header_block)
    emitted_blocks.update(if_pattern.true_body)
    emitted_blocks.update(if_pattern.false_body)

    return lines


def format_structured_function(ssa_func: SSAFunction) -> str:
    cfg = ssa_func.cfg
    resolver = getattr(ssa_func.scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    start_to_block = _build_start_map(cfg)
    visited: Set[int] = set()
    lines: List[str] = []
    # Load symbol database for global variable name resolution
    symbol_db = _load_symbol_db()

    # FIX 2: Variable name collision resolution (simplified for legacy function)
    # Note: This function is likely deprecated, main function is format_structured_function_v3
    from .variable_renaming import VariableRenamer
    all_block_ids = set(cfg.blocks.keys()) if cfg and cfg.blocks else set()
    renamer = VariableRenamer(ssa_func, all_block_ids)
    rename_map = renamer.analyze_and_rename()

    formatter = ExpressionFormatter(ssa_func, symbol_db=symbol_db, rename_map=rename_map)
    ssa_blocks = ssa_func.instructions

    def process(block_id: int, indent: str = "    ") -> None:
        if block_id in visited:
            lines.append(f"{indent}// goto block {block_id}")
            return
        block = cfg.blocks.get(block_id)
        if not block:
            lines.append(f"{indent}// missing block {block_id}")
            return

        visited.add(block_id)
        lines.append(f"{indent}// Block {block_id}")
        lines.extend(_format_block_lines(ssa_func, block_id, indent))

        if not block.instructions:
            return

        last_instr = block.instructions[-1]
        opcode = last_instr.opcode
        if resolver.is_conditional_jump(opcode):
            true_block = start_to_block.get(last_instr.arg1)
            fallthrough_addr = last_instr.address + 1
            false_block = start_to_block.get(fallthrough_addr)
            if (
                true_block is not None
                and false_block is not None
                and len(block.successors) == 2
                and cfg.blocks[true_block].predecessors == {block_id}
                and cfg.blocks[false_block].predecessors == {block_id}
            ):
                cond_text = None
                ssa_block = ssa_blocks.get(block_id, [])
                for ssa_inst in ssa_block:
                    if ssa_inst.address == last_instr.address and ssa_inst.inputs:
                        cond_value = ssa_inst.inputs[0]
                        # FIX 3: Pass IN_CONDITION context
                        cond_expr = formatter.render_value(cond_value, context=ExpressionContext.IN_CONDITION)
                        # If condition renders as just a number, use SSA name instead
                        if cond_expr.lstrip('-').isdigit():
                            cond_expr = cond_value.alias or cond_value.name
                        mnemonic = resolver.get_mnemonic(opcode)
                        # FIX 3: Smart negation
                        if mnemonic == "JZ":
                            if is_simple_expression(cond_expr):
                                cond_text = f"!{cond_expr}"
                            else:
                                cond_text = f"!({cond_expr})"
                        elif mnemonic == "JNZ":
                            cond_text = cond_expr
                        else:
                            cond_text = cond_expr
                        break
                if cond_text is None:
                    cond_text = f"cond_block_{block_id}"
                lines.append(f"{indent}if ({cond_text}) {{")
                process(true_block, indent + "    ")
                lines.append(f"{indent}}} else {{")
                process(false_block, indent + "    ")
                lines.append(f"{indent}}}")
                return

        # Default: follow successors sequentially
        for succ in sorted(block.successors):
            if succ is None:
                continue
            if _dominates(cfg, succ, block_id) and succ != block_id:
                lines.append(f"{indent}while (/* loop to block {succ} */) {{")
                if succ in visited:
                    lines.append(f"{indent}    // loop body already emitted")
                else:
                    process(succ, indent + "    ")
                lines.append(f"{indent}}}")
            else:
                process(succ, indent)

    lines.append("void function_entry(void) {")
    process(cfg.entry_block)
    lines.append("}")
    return "\n".join(lines)


def _get_loop_for_block(block_id: int, loops: List[NaturalLoop]) -> Optional[NaturalLoop]:
    """Find the innermost loop containing this block."""
    containing_loops = [l for l in loops if block_id in l.body]
    if not containing_loops:
        return None
    # Return the smallest (innermost) loop
    return min(containing_loops, key=lambda l: len(l.body))


def _is_back_edge_target(cfg: CFG, source: int, target: int, loops: List[NaturalLoop]) -> bool:
    """Check if edge source→target is a back edge (target is loop header containing source)."""
    for loop in loops:
        if loop.header == target and source in loop.body:
            return True
    return False


@dataclass
class IfElsePattern:
    """Detected if/else pattern."""
    header_block: int              # Block with conditional jump
    true_block: int                # Block to execute if condition is true
    false_block: int               # Block to execute if condition is false
    merge_block: Optional[int]     # Block where both branches merge (None if no merge)
    true_body: Set[int] = None     # All blocks in true branch
    false_body: Set[int] = None    # All blocks in false branch

    def __post_init__(self):
        if self.true_body is None:
            self.true_body = {self.true_block}
        if self.false_body is None:
            self.false_body = {self.false_block}


@dataclass
class CompoundCondition:
    """
    Represents a compound logical condition (AND/OR of multiple tests).

    Used to reconstruct short-circuit evaluation patterns like:
    - (A && B)
    - (A || B)
    - ((A && B) || (C && D))

    Conditions can be:
    - Simple strings (rendered condition expressions)
    - Nested CompoundCondition objects (for complex nesting)
    """
    operator: str                          # "&&" or "||"
    conditions: List                       # List[Union[str, CompoundCondition]]
    true_target: int                       # Block to execute if TRUE
    false_target: int                      # Block to execute if FALSE
    involved_blocks: Set[int] = None      # All blocks involved in this compound condition

    def __post_init__(self):
        if self.involved_blocks is None:
            self.involved_blocks = set()


@dataclass
class ForLoopInfo:
    """Detected for-loop pattern."""
    var: str                       # Loop variable for display (e.g., "i")
    init: str                      # Initialization expression (e.g., "0")
    condition: str                 # Loop condition (e.g., "i < gRecs")
    increment: str                 # Increment expression (e.g., "i++")
    init_var: str = ""            # Original initialization variable (e.g., "local_2") for filtering


def _render_blocks_with_loops(
    block_ids: List[int],
    indent: str,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    cfg: CFG,
    func_loops: List,
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver,
    block_to_if: Dict[int, Any],
    visited_ifs: Set[int],
    emitted_blocks: Set[int],
    global_map: Optional[Dict[int, str]] = None,
    # FÁZE 1.3: Early return/break pattern detection
    early_returns: Optional[Dict[int, tuple]] = None
) -> List[str]:
    """
    Render a sequence of blocks with loop detection support.

    Used for rendering switch case bodies where loops may be present.
    """
    lines: List[str] = []
    processed_in_loop: Set[int] = set()

    # Track which blocks have for-loops as successors and what variable to skip
    skip_last_assignment: Dict[int, str] = {}  # block_id -> variable_name to skip

    # Pre-scan to identify blocks that need initialization skipped
    for body_block_id in block_ids:
        # Check if this block is a loop header
        for loop in func_loops:
            if loop.header == body_block_id:
                # Try to detect for-loop pattern
                for_info = _detect_for_loop(loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map)
                if for_info:
                    # Mark predecessor blocks to skip initialization
                    header_block = cfg.blocks.get(loop.header)
                    if header_block:
                        for pred_id in header_block.predecessors:
                            if pred_id not in loop.body and pred_id in block_ids:
                                # This predecessor should skip assignment to loop variable
                                skip_last_assignment[pred_id] = for_info.init_var
                break

    for body_block_id in block_ids:
        # Skip if already processed as part of a loop
        if body_block_id in processed_in_loop:
            continue

        body_block = cfg.blocks.get(body_block_id)
        if not body_block:
            continue

        # Check if this block is a loop header
        header_loop = None
        for loop in func_loops:
            if loop.header == body_block_id:
                header_loop = loop
                break

        # FÁZE 3.2 FIX: Loop headers take precedence over emitted_blocks
        # Even if a loop header was marked as emitted (e.g., as part of if/else body),
        # we should render it as a loop instead
        if not header_loop:
            # Not a loop header - check if already emitted as part of if/else
            if body_block_id in emitted_blocks:
                continue

        if header_loop:
            # Render loop
            lines.append(f"{indent}// Loop header - Block {body_block_id} @{body_block.start}")

            # Try to detect for-loop pattern
            for_info = _detect_for_loop(header_loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map)
            if for_info:
                lines.append(f"{indent}for ({for_info.var} = {for_info.init}; {for_info.condition}; {for_info.increment}) {{")
            else:
                lines.append(f"{indent}while (true) {{  // loop body: blocks {sorted(header_loop.body)}")

            # Render loop body blocks
            loop_body_sorted = sorted(header_loop.body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
            for loop_body_id in loop_body_sorted:
                loop_body_block = cfg.blocks.get(loop_body_id)
                if loop_body_block:
                    ssa_block = ssa_func.instructions.get(loop_body_id, [])
                    if not _is_control_flow_only(ssa_block, resolver):
                        if SHOW_BLOCK_COMMENTS: lines.append(f"{indent}    // Block {loop_body_id} @{loop_body_block.start}")

                    # FÁZE 3.2 FIX: For for-loops, skip increment in back edge block
                    # Back edge block contains the increment and jumps back to header
                    # Identify back edge block: has loop header as successor
                    skip_var = None
                    if for_info:
                        # Check if this block jumps back to header (back edge)
                        if header_loop.header in loop_body_block.successors:
                            skip_var = for_info.var  # Skip increment for loop variable

                    if skip_var:
                        # Filter out increment assignment
                        block_lines = _format_block_lines_filtered(
                            ssa_func, loop_body_id, indent + "    ", formatter, skip_var,
                            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                            early_returns
                        )
                        lines.extend(block_lines)
                    else:
                        lines.extend(_format_block_lines(
                            ssa_func, loop_body_id, indent + "    ", formatter,
                            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                            early_returns
                        ))

            lines.append(f"{indent}}}")

            # Mark all loop body blocks as processed
            processed_in_loop.update(header_loop.body)
        else:
            # Regular block - render normally
            ssa_block = ssa_func.instructions.get(body_block_id, [])
            if not _is_control_flow_only(ssa_block, resolver):
                if SHOW_BLOCK_COMMENTS: lines.append(f"{indent}// Block {body_block_id} @{body_block.start}")

            # Check if we need to skip last assignment in this block
            if body_block_id in skip_last_assignment:
                skip_var = skip_last_assignment[body_block_id]
                # Render expressions but filter out the last assignment to skip_var
                block_lines = _format_block_lines_filtered(
                    ssa_func, body_block_id, indent, formatter, skip_var,
                    block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                    early_returns
                )
                lines.extend(block_lines)
            else:
                lines.extend(_format_block_lines(
                    ssa_func, body_block_id, indent, formatter,
                    block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver,
                    early_returns
                ))

            # DEAD CODE ELIMINATION: Check if block terminates execution
            # If block ends with return, stop rendering remaining blocks (they're unreachable)
            if body_block and body_block.instructions:
                last_instr = body_block.instructions[-1]
                if resolver.is_return(last_instr.opcode):
                    # Stop iteration - all following blocks are unreachable
                    break

    return lines


def _detect_for_loop(
    loop: NaturalLoop,
    cfg: CFG,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    global_map: Optional[Dict[int, str]] = None
) -> Optional[ForLoopInfo]:
    """
    Detect for-loop pattern in a natural loop.

    Pattern:
    1. Predecessor of header has initialization (i = 0)
    2. Header has conditional jump testing loop variable (i < N)
    3. Last block in body has increment (i++)

    Returns:
        ForLoopInfo if pattern matches, None otherwise
    """
    # Get header block
    header_block = cfg.blocks.get(loop.header)
    if not header_block or not header_block.instructions:
        return None

    # Step 1: Find initialization in predecessor blocks
    # Look for assignments immediately before loop entry
    predecessors = [p for p in header_block.predecessors if p not in loop.body]
    if not predecessors:
        return None

    init_var = None
    init_value = None

    # Check predecessors for initialization pattern
    # Pattern 1: Direct assignment (inst has outputs)
    # Pattern 2: ASGN instruction (inputs=[value, &target])
    for pred_id in predecessors:
        pred_ssa_block = ssa_func.instructions.get(pred_id, [])
        # Look for assignments like: local_2 = 0, i = 0
        for inst in reversed(pred_ssa_block):  # Check from end backwards
            # Pattern 1: Direct output (e.g., local_2 = 0)
            if inst.outputs and len(inst.outputs) == 1:
                var_name = inst.outputs[0].alias or inst.outputs[0].name
                if var_name and not var_name.startswith("data_") and not var_name.startswith("&"):
                    # Found potential init variable
                    init_var = var_name
                    # Get initialization value from instruction
                    if inst.inputs and len(inst.inputs) > 0:
                        init_value = formatter.render_value(inst.inputs[0])
                    else:
                        init_value = "0"  # Default
                    break
            # Pattern 2: ASGN instruction (inputs=[value, &target])
            elif inst.mnemonic == "ASGN" and len(inst.inputs) >= 2:
                target = inst.inputs[1]
                target_name = target.alias or target.name
                # Extract variable name from &local_2 → local_2
                if target_name and target_name.startswith("&"):
                    var_name = target_name[1:]  # Strip & prefix
                    if var_name and not var_name.startswith("data_"):
                        # Found potential init variable
                        init_var = var_name
                        # Get initialization value from first input
                        init_value = formatter.render_value(inst.inputs[0])
                        break
        if init_var:
            break

    if not init_var:
        return None

    # Step 2: Extract condition from header's conditional jump
    last_instr = header_block.instructions[-1]
    if not resolver.is_conditional_jump(last_instr.opcode):
        return None

    # Get condition from SSA
    condition_text = None
    header_ssa_block = ssa_func.instructions.get(loop.header, [])

    # Find the comparison instruction (the one that produces the condition value)
    for ssa_inst in header_ssa_block:
        if ssa_inst.address == last_instr.address and ssa_inst.inputs:
            cond_value = ssa_inst.inputs[0]

            # Find the instruction that produced this value
            for compare_inst in header_ssa_block:
                if compare_inst.outputs and any(out.name == cond_value.name for out in compare_inst.outputs):
                    # This is the comparison instruction - manually render it
                    if compare_inst.inputs and len(compare_inst.inputs) >= 2:
                        left = formatter.render_value(compare_inst.inputs[0])
                        right_val = compare_inst.inputs[1]

                        # FIX: If right operand is a data segment reference, resolve to global name or constant
                        right_alias = right_val.alias or right_val.name
                        if right_alias and right_alias.startswith("data_"):
                            # This is a data segment reference
                            offset = int(right_alias[5:])  # Extract offset from "data_123"
                            if global_map and offset in global_map:
                                # Known global variable name
                                right = global_map[offset]
                            else:
                                # FÁZE 2.1: Try to resolve as constant from data segment
                                scr = getattr(ssa_func, 'scr', None)
                                if scr and hasattr(scr, 'data_segment'):
                                    try:
                                        # Read 4-byte integer from data segment
                                        import struct
                                        data_seg = scr.data_segment
                                        # CRITICAL FIX: offset is in DWORD units, not bytes!
                                        # data_383 means 383rd DWORD (4-byte word)
                                        byte_offset = offset * 4
                                        if byte_offset < len(data_seg.raw_data):
                                            bytes_data = data_seg.raw_data[byte_offset:byte_offset+4]
                                            if len(bytes_data) == 4:
                                                const_value = struct.unpack('<I', bytes_data)[0]
                                                # Use constant value if it looks reasonable for loop bound
                                                if 0 <= const_value < 10000:
                                                    right = str(const_value)
                                                else:
                                                    right = right_alias
                                            else:
                                                right = right_alias
                                        else:
                                            right = right_alias
                                    except:
                                        # Fallback to data_X if resolution fails
                                        right = right_alias
                                else:
                                    # Fallback to data_X if no data segment available
                                    right = right_alias
                        else:
                            right = formatter.render_value(right_val)

                        # Map mnemonic to operator
                        op_map = {
                            "ULES": "<=", "UGTS": ">", "UGES": ">=", "ULSS": "<",
                            "IEQS": "==", "INES": "!=",
                            "CESS": "<", "CGTS": ">", "CGES": ">=", "CLES": "<=",
                            "CEQS": "==", "CNES": "!=",
                            "SESS": "<", "SGTS": ">", "SGES": ">=", "SLES": "<=",
                            "SEQS": "==", "SNES": "!=",
                            "IESS": "<", "IGTS": ">", "IGES": ">=", "ILES": "<=",
                        }
                        op = op_map.get(compare_inst.mnemonic, "?")

                        # P0.2 FIX: Analyze jump direction to correct loop conditions
                        # Problem: Compiler generates <= for < in some cases (off-by-one bug)
                        # Solution: Check if jump exits loop (forward) or continues (backward)
                        jump_instr = ssa_inst  # The JZ/JNZ instruction
                        jump_target = last_instr.arg1  # Target address of jump

                        # Determine if jump exits loop or continues loop
                        # If jump goes FORWARD (to higher address) → likely exit condition
                        # If jump goes BACKWARD (to lower address) → likely loop continuation
                        is_forward_jump = jump_target > last_instr.address

                        # For-loops typically have pattern: JZ forward (exit when condition false)
                        # So if bytecode has ULES (<=) and JZ forward, we need to normalize:
                        # - ULES + JZ forward = exit when (i <= limit) is FALSE = continue when (i > limit)
                        # - But wait, that's inverted! Let's check the jump mnemonic

                        # Actually, the condition in bytecode represents when to EXIT the loop
                        # For standard for-loops: continue while (i < N), exit when NOT (i < N)
                        # Compiler generates: compare i vs N, JZ exit_label (jump if i >= N)
                        # So bytecode comparison is "i >= N" (exit condition)
                        # We want to display: "i < N" (continue condition)

                        # Heuristic for for-loops:
                        # If operator is <= and it looks like a standard loop bound check,
                        # convert to < (the original source likely used <)
                        if op in ["<=", ">="]:
                            # Check if this is a standard loop pattern (counter vs constant/variable)
                            # Pattern: local_X <= N where local_X starts at 0
                            if init_value in ["0", "0x0", "0x00000000"]:
                                # Loop starts at 0, likely should be < not <=
                                if op == "<=":
                                    op = "<"
                                    # Note: We're making an educated guess that the original
                                    # source used < and the compiler generated <=
                                    # This is a common pattern in VC Script compiler
                                elif op == ">=":
                                    op = ">"

                        cond_expr = f"({left} {op} {right})"

                        # Check if condition involves our loop variable (check both name and any aliases)
                        # For example, local_2 might be rendered as "i" due to aliasing
                        involves_loop_var = init_var in cond_expr
                        # Also check if any of the inputs have the init_var as their base
                        if not involves_loop_var:
                            for inp in compare_inst.inputs:
                                inp_name = inp.alias or inp.name
                                # Strip & prefix if present
                                if inp_name and inp_name.startswith("&"):
                                    inp_name = inp_name[1:]
                                if inp_name == init_var:
                                    involves_loop_var = True
                                    break
                        if involves_loop_var:
                            condition_text = cond_expr
                    break
            break

    if not condition_text:
        return None

    # Step 3: Find increment at end of loop body
    # Look in blocks that jump back to header (back edges)
    # Pattern 1: Direct increment (inst has outputs with init_var name)
    # Pattern 2: ASGN instruction (inputs=[value, &init_var])
    increment_text = None
    for back_edge in loop.back_edges:
        source_id = back_edge.source
        target_id = back_edge.target
        if target_id == loop.header:
            # This block jumps back to header - check for increment
            source_ssa_block = ssa_func.instructions.get(source_id, [])
            for inst in reversed(source_ssa_block):
                # Pattern 1: Direct output (e.g., i = i + 1)
                if inst.outputs and len(inst.outputs) == 1:
                    var_name = inst.outputs[0].alias or inst.outputs[0].name
                    if var_name == init_var:
                        # Found assignment to loop variable
                        # Check if it's increment pattern: i = i + 1
                        if inst.mnemonic in {"IADD", "CADD", "SADD"}:
                            # Simple increment
                            increment_text = f"{init_var}++"
                        elif inst.inputs:
                            # Generic assignment - render it
                            inc_expr = formatter.render_value(inst.inputs[0]) if inst.inputs else "?"
                            if f"{init_var} + 1" in inc_expr or f"({init_var} + 1)" == inc_expr:
                                increment_text = f"{init_var}++"
                            else:
                                increment_text = f"{init_var} = {inc_expr}"
                        break
                # Pattern 2: ASGN instruction (inputs=[value, &target])
                elif inst.mnemonic == "ASGN" and len(inst.inputs) >= 2:
                    target = inst.inputs[1]
                    target_name = target.alias or target.name
                    # Extract variable name from &local_2 → local_2
                    if target_name and target_name.startswith("&"):
                        var_name = target_name[1:]  # Strip & prefix
                        if var_name == init_var:
                            # Found assignment to loop variable
                            # Render the increment expression
                            inc_expr = formatter.render_value(inst.inputs[0])
                            # Check for i+1 pattern
                            if f"{init_var} + 1" in inc_expr or f"({init_var} + 1)" == inc_expr:
                                increment_text = f"{init_var}++"
                            else:
                                increment_text = f"{init_var} = {inc_expr}"
                            break
            if increment_text:
                break

    if not increment_text:
        return None

    # Successfully detected for-loop pattern
    # Extract the actual variable name from condition if it's different from init_var
    # Condition is like "(i <= gData28)" - extract the left operand
    import re
    display_var = init_var
    match = re.match(r'\((\w+)\s*[<>=!]+', condition_text)
    if match:
        cond_var = match.group(1)
        if cond_var != init_var:
            # Use the variable name from condition (it's the aliased form)
            display_var = cond_var
            # Also update increment to use display_var
            increment_text = increment_text.replace(init_var, display_var)

    return ForLoopInfo(
        var=display_var,
        init=init_value,
        condition=condition_text,
        increment=increment_text,
        init_var=init_var
    )


def _find_if_body_blocks(cfg: CFG, entry: int, stop_blocks: Set[int], resolver: opcodes.OpcodeResolver) -> Set[int]:
    """
    Find all blocks belonging to an if branch using BFS.
    Similar to _find_case_body_blocks but for if/else branches.
    """
    body_blocks: Set[int] = set()
    worklist = [entry]
    visited: Set[int] = set()

    while worklist:
        block_id = worklist.pop(0)

        if block_id in visited:
            continue

        # Stop at barriers (merge point, other branches, etc.)
        if block_id in stop_blocks and block_id != entry:
            continue

        visited.add(block_id)
        body_blocks.add(block_id)

        # Get block
        block = cfg.blocks.get(block_id)
        if block and block.instructions:
            last_instr = block.instructions[-1]
            if resolver.is_return(last_instr.opcode):
                continue  # Don't follow after return

        # Add successors to worklist
        if block:
            for succ in block.successors:
                if succ not in visited:
                    worklist.append(succ)

    return body_blocks


def _find_common_successor(cfg: CFG, block_a: int, block_b: int) -> Optional[int]:
    """
    Find the immediate common successor (merge point) of two blocks.
    Returns the first block that is reachable from both branches.
    """
    # Get all successors of both blocks (BFS)
    def get_all_successors(start: int, max_depth: int = 20) -> Set[int]:
        visited = set()
        worklist = [(start, 0)]
        while worklist:
            block_id, depth = worklist.pop(0)
            if depth > max_depth or block_id in visited:
                continue
            visited.add(block_id)
            block = cfg.blocks.get(block_id)
            if block:
                for succ in block.successors:
                    worklist.append((succ, depth + 1))
        return visited

    succs_a = get_all_successors(block_a)
    succs_b = get_all_successors(block_b)

    # Find common successors
    common = succs_a & succs_b
    if not common:
        return None

    # Return the one with smallest address (closest merge point)
    candidates = [(bid, cfg.blocks[bid].start) for bid in common if bid in cfg.blocks]
    if not candidates:
        return None

    return min(candidates, key=lambda x: x[1])[0]


def _is_jmp_after_jz(
    block: BasicBlock,
    resolver: opcodes.OpcodeResolver
) -> Optional[int]:
    """
    Check if block ends with pattern: JZ target1; JMP target2

    This pattern indicates short-circuit evaluation:
    - If condition is FALSE, jump to target1 (next condition in OR, or exit)
    - If condition is TRUE, jump to target2 (true body)

    Returns:
        target2 (the JMP destination) if pattern matches, None otherwise
    """
    if not block or not block.instructions or len(block.instructions) < 2:
        return None

    last = block.instructions[-1]
    second_last = block.instructions[-2]

    # Check for: conditional jump followed by unconditional jump
    if (resolver.is_conditional_jump(second_last.opcode) and
        resolver.get_mnemonic(last.opcode) == "JMP"):
        return last.arg1  # The TRUE target

    return None


def _find_all_jz_targets(
    cfg: CFG,
    block_id: int,
    resolver: opcodes.OpcodeResolver
) -> Set[int]:
    """
    Find all JZ/JNZ targets within a block (for AND detection).

    In short-circuit AND evaluation, multiple conditions in sequence all
    jump to the same FALSE exit point:
        if (!cond1) goto exit;
        if (!cond2) goto exit;
        if (!cond3) goto exit;
        goto body;
    This is: if (cond1 && cond2 && cond3) body;

    Returns:
        Set of target addresses for all conditional jumps in the block
    """
    block = cfg.blocks.get(block_id)
    if not block:
        return set()

    targets = set()
    for instr in block.instructions:
        if resolver.is_conditional_jump(instr.opcode):
            targets.add(instr.arg1)

    return targets


def _find_common_true_target(
    cfg: CFG,
    blocks: List[int],
    resolver: opcodes.OpcodeResolver
) -> Optional[int]:
    """
    Find if multiple blocks all JMP to the same TRUE target (OR detection).

    In short-circuit OR evaluation, multiple condition groups all jump to
    the same TRUE body:
        if (cond1) goto body;
        if (cond2) goto body;
        if (cond3) goto body;
        goto exit;
    This is: if (cond1 || cond2 || cond3) body;

    Returns:
        The common target address if found, None otherwise
    """
    true_targets = []

    for block_id in blocks:
        block = cfg.blocks.get(block_id)
        if not block:
            continue

        jmp_target = _is_jmp_after_jz(block, resolver)
        if jmp_target is not None:
            true_targets.append(jmp_target)

    # Check if all jump to same target
    if len(true_targets) >= 2 and len(set(true_targets)) == 1:
        return true_targets[0]  # All jump to same target = OR pattern

    return None


def _extract_condition_from_block(
    block_id: int,
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter,
    cfg: CFG,
    resolver: opcodes.OpcodeResolver
) -> Optional[str]:
    """
    Extract condition expression from a block ending with conditional jump.

    Finds the JZ/JNZ instruction in the block and extracts its condition
    from the corresponding SSA instruction.

    Args:
        block_id: Block ID to extract condition from
        ssa_func: SSA function containing the block
        formatter: Expression formatter for rendering
        cfg: Control flow graph
        resolver: Opcode resolver

    Returns:
        Rendered condition expression, or None if not found/not applicable
    """
    from .parenthesization import ExpressionContext

    block = cfg.blocks.get(block_id)
    if not block or not block.instructions:
        return None

    # Find the last conditional jump in the block
    for instr in reversed(block.instructions):
        if resolver.is_conditional_jump(instr.opcode):
            # Found conditional jump, now find corresponding SSA instruction
            ssa_block = ssa_func.instructions.get(block_id, [])

            for ssa_inst in ssa_block:
                if ssa_inst.address == instr.address and ssa_inst.inputs:
                    cond_value = ssa_inst.inputs[0]
                    cond_expr = formatter.render_value(
                        cond_value,
                        context=ExpressionContext.IN_CONDITION
                    )

                    # If renders as just a number, use SSA name/alias instead
                    if cond_expr.lstrip('-').isdigit():
                        alias = cond_value.alias or cond_value.name
                        if alias and not alias.startswith("data_"):
                            cond_expr = alias

                    return cond_expr
            break

    return None


# Keep old function name for backward compatibility (used in other places)
def _extract_condition_expr(
    ssa_func: SSAFunction,
    block_id: int,
    instr_address: int,
    formatter: ExpressionFormatter,
    resolver: opcodes.OpcodeResolver
) -> Optional[str]:
    """Legacy wrapper - calls _extract_condition_from_block."""
    from .cfg import CFG as _  # Import to get type
    # We don't have CFG here, so just do the old implementation
    from .parenthesization import ExpressionContext

    ssa_block = ssa_func.instructions.get(block_id, [])

    for ssa_inst in ssa_block:
        if ssa_inst.address == instr_address and ssa_inst.inputs:
            cond_value = ssa_inst.inputs[0]
            cond_expr = formatter.render_value(
                cond_value,
                context=ExpressionContext.IN_CONDITION
            )

            # If renders as just a number, use SSA name/alias instead
            if cond_expr.lstrip('-').isdigit():
                alias = cond_value.alias or cond_value.name
                if alias and not alias.startswith("data_"):
                    cond_expr = alias

            return cond_expr

    return None


def _combine_conditions(
    conditions: List,  # List[Union[str, CompoundCondition]]
    operator: str,
    preserve_style: bool = True
) -> str:
    """
    Combine multiple conditions with && or || operators.

    Applies proper parenthesization to match original code style.

    Args:
        conditions: List of condition strings or CompoundCondition objects
        operator: "&&" or "||"
        preserve_style: If True, add extra parentheses to match original style

    Returns:
        Combined condition expression
    """
    if len(conditions) == 0:
        return "true"
    if len(conditions) == 1:
        cond = conditions[0]
        if isinstance(cond, CompoundCondition):
            return _combine_conditions(cond.conditions, cond.operator, preserve_style)
        return str(cond)

    # Render each condition
    rendered = []
    for cond in conditions:
        if isinstance(cond, CompoundCondition):
            # Recursively render compound conditions
            sub_expr = _combine_conditions(cond.conditions, cond.operator, preserve_style)
            # Wrap in parentheses for clarity (matches original style)
            rendered.append(f"({sub_expr})")
        else:
            rendered.append(str(cond))

    # Combine with operator
    if operator == "||":
        # OR style: (A && B) || (C && D)
        # CompoundConditions already wrapped above
        combined = f" {operator} ".join(rendered)
    else:
        # AND style: A && B && C
        # Don't add extra parentheses for simple AND
        combined = f" {operator} ".join(rendered)

    return combined


def _detect_early_return_pattern(
    cfg: CFG,
    block_id: int,
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver,
    switch_exit_block: Optional[int] = None
) -> Optional[tuple]:
    """
    Detect early return/break pattern.

    Pattern:
    - Block ends with conditional jump (JZ/JNZ)
    - One branch contains only JMP to exit point (return/break)
    - Other branch continues with normal code

    This should be rendered as:
        if (condition) break;  // or return
        // continue without nesting

    Returns:
        (condition_value, exit_branch, continue_branch, is_negated) or None
        where is_negated=True if condition should be negated for "if (cond) exit"
    """
    block = cfg.blocks.get(block_id)
    if not block or not block.instructions:
        return None

    last_instr = block.instructions[-1]
    if not resolver.is_conditional_jump(last_instr.opcode):
        return None

    # Get true (jump target) and false (fallthrough) branches
    true_addr = last_instr.arg1
    false_addr = last_instr.address + 1
    true_block = start_to_block.get(true_addr)
    false_block = start_to_block.get(false_addr)

    if true_block is None or false_block is None:
        return None

    # Check if one branch is just JMP to exit
    def is_exit_jump(bid: int) -> bool:
        """Check if block is just unconditional JMP to exit point."""
        b = cfg.blocks.get(bid)
        if not b or not b.instructions:
            return False
        # Block should have exactly 1 instruction (JMP)
        if len(b.instructions) != 1:
            return False
        instr = b.instructions[0]
        mnem = resolver.get_mnemonic(instr.opcode)
        if mnem != "JMP":
            return False
        # Jump target should be exit point (outside current scope)
        # For switch cases, check if jumping to switch exit
        if switch_exit_block is not None:
            jump_target = start_to_block.get(instr.arg1)
            return jump_target == switch_exit_block
        return True

    mnemonic = resolver.get_mnemonic(last_instr.opcode)

    # Check which branch is the exit
    if is_exit_jump(true_block):
        # True branch exits, false continues
        # For JZ: condition is false -> exits, so render as "if (cond) continue" = "if (!cond) exit"
        # For JNZ: condition is true -> exits, so render as "if (cond) exit"
        is_negated = (mnemonic == "JZ")
        return (block_id, true_block, false_block, is_negated)
    elif is_exit_jump(false_block):
        # False branch exits, true continues
        # For JZ: condition is true -> exits, so render as "if (!cond) exit"
        # For JNZ: condition is false -> exits, so render as "if (cond) continue" = "if (!cond) exit"
        is_negated = (mnemonic == "JNZ")
        return (block_id, false_block, true_block, is_negated)

    return None


def _trace_value_to_function_call(
    ssa_func: SSAFunction,
    value: "SSAValue",
    formatter: "ExpressionFormatter",
    max_depth: int = 5
) -> Optional[str]:
    """
    FÁZE 1.6: Trace a value back to its producer to check if it's a function call result.

    Pattern to detect:
    - XCALL/CALL instruction
    - Followed by LLD [sp+307] (load return value)
    - Value used in condition or assignment

    Returns:
        Function call expression (e.g., "SC_MP_EnumPlayers(...)") if found, None otherwise
    """
    if not value or max_depth <= 0:
        return None

    # DEBUG
    import sys
    # print(f"DEBUG _trace_value_to_function_call: value={value.name}, has_producer={value.producer_inst is not None}", file=sys.stderr)

    # Check if this value came from LLD instruction
    if not value.producer_inst:
        return None

    producer = value.producer_inst
    # print(f"DEBUG producer: mnemonic={producer.mnemonic}, addr={producer.address}", file=sys.stderr)

    # Pattern: LLD [sp+307] loads return value from stack
    # This is the standard return value slot after CALL/XCALL
    if producer.mnemonic == "LLD":
        # Check if LLD is loading from sp+307 (return value slot)
        if producer.instruction and producer.instruction.instruction:
            load_offset = producer.instruction.instruction.arg1
            # sp+307 is the return value slot (stack pointer + 307 * 4 bytes typically)
            # But we also need to check if there's a recent CALL/XCALL before this LLD

            # Look backwards in the same block for CALL/XCALL
            block_id = producer.block_id
            block_instructions = ssa_func.instructions.get(block_id, [])

            # Find the LLD instruction index
            lld_index = None
            for idx, inst in enumerate(block_instructions):
                if inst.address == producer.address:
                    lld_index = idx
                    break

            if lld_index is None:
                return None

            # Look backwards for CALL/XCALL (should be immediately before or within a few instructions)
            for idx in range(lld_index - 1, max(0, lld_index - 5), -1):
                prev_inst = block_instructions[idx]
                if prev_inst.mnemonic in {"CALL", "XCALL"}:
                    # Found the function call! Format it using the expression formatter
                    # The formatter already knows how to render CALL/XCALL with arguments
                    try:
                        from .expr import format_instruction
                        call_expr = format_instruction(prev_inst, formatter)
                        # Extract just the call part (remove semicolon if present)
                        if call_expr.endswith(";"):
                            call_expr = call_expr[:-1].strip()
                        return call_expr
                    except:
                        # Fallback: just return a placeholder
                        if prev_inst.mnemonic == "XCALL":
                            return f"func_{prev_inst.address}(...)"
                        else:
                            return f"func_{prev_inst.address}(...)"

    # If not direct LLD, check if value came from PHI that might wrap LLD
    if producer.mnemonic == "PHI" and len(producer.inputs) == 1:
        # Single-input PHI, trace through it
        return _trace_value_to_function_call(ssa_func, producer.inputs[0], formatter, max_depth - 1)

    return None


def _collect_and_chain(
    start_block_id: int,
    cfg: CFG,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    visited: Set[int]
) -> Tuple[List[int], Optional[int], Optional[int]]:
    """
    Collect blocks forming an AND chain by following fallthrough paths.

    An AND chain is a sequence of blocks where:
    1. Each block ends with JZ jumping to the same FALSE target
    2. Blocks are connected via fallthrough (sequential addresses)
    3. Final block in chain has a fallthrough to JMP block (TRUE target)

    Example CFG structure:
        Block A: cond1; JZ false_target  → fallthrough to B
        Block B: cond2; JZ false_target  → fallthrough to C
        Block C: JMP true_target

    This represents: if (cond1 && cond2) goto true_target else goto false_target

    Args:
        start_block_id: Block ID to start from
        cfg: Control flow graph
        resolver: Opcode resolver
        start_to_block: Address to block ID mapping
        visited: Set of already visited blocks (to prevent infinite loops)

    Returns:
        Tuple of (chain_blocks, true_target, false_target):
        - chain_blocks: List of block IDs in the AND chain
        - true_target: Block ID to jump to when all conditions are TRUE
        - false_target: Block ID to jump to when any condition is FALSE
        Returns ([], None, None) if no AND chain detected
    """
    if start_block_id in visited:
        return ([], None, None)

    visited.add(start_block_id)

    block = cfg.blocks.get(start_block_id)
    if not block or not block.instructions:
        return ([], None, None)

    last_instr = block.instructions[-1]
    mnemonic = resolver.get_mnemonic(last_instr.opcode)

    # Block must end with conditional jump (JZ/JNZ) to be part of AND chain
    if not resolver.is_conditional_jump(last_instr.opcode):
        return ([], None, None)

    # This is the first block in potential AND chain
    chain_blocks = [start_block_id]
    false_target_addr = last_instr.arg1  # Where to go if condition fails
    false_target = start_to_block.get(false_target_addr)

    # Follow fallthrough path to find more conditions or TRUE target
    fallthrough_addr = last_instr.address + 1
    fallthrough_block_id = start_to_block.get(fallthrough_addr)

    if not fallthrough_block_id:
        return (chain_blocks, None, false_target)

    fallthrough_block = cfg.blocks.get(fallthrough_block_id)
    if not fallthrough_block or not fallthrough_block.instructions:
        return (chain_blocks, None, false_target)

    # Check if fallthrough block is just a JMP (end of AND chain, this is TRUE target)
    if len(fallthrough_block.instructions) == 1:
        ft_last = fallthrough_block.instructions[-1]
        if resolver.get_mnemonic(ft_last.opcode) == "JMP":
            # This JMP is where we go if all conditions pass
            true_target = start_to_block.get(ft_last.arg1)
            return (chain_blocks, true_target, false_target)

    # Check if fallthrough block is another condition in the AND chain
    ft_last_instr = fallthrough_block.instructions[-1]
    if resolver.is_conditional_jump(ft_last_instr.opcode):
        # Check if it jumps to the SAME false target
        if ft_last_instr.arg1 == false_target_addr:
            # It's part of the AND chain! Recursively collect the rest
            rest_chain, true_target, _ = _collect_and_chain(
                fallthrough_block_id, cfg, resolver, start_to_block, visited
            )
            if rest_chain:
                chain_blocks.extend(rest_chain)
                return (chain_blocks, true_target, false_target)

    # Fallthrough doesn't continue the AND chain
    return (chain_blocks, None, false_target)


def _detect_short_circuit_pattern(
    cfg: CFG,
    header_block_id: int,
    resolver: opcodes.OpcodeResolver,
    start_to_block: Dict[int, int],
    ssa_func: SSAFunction,
    formatter: ExpressionFormatter
) -> Optional[CompoundCondition]:
    """
    Detect short-circuit && and || patterns using multi-block analysis.

    NEW IMPLEMENTATION: Follows fallthrough chains across multiple blocks
    to detect AND chains, then identifies OR by finding multiple branches
    jumping to the same TRUE target.

    Patterns detected:
    1. Simple AND: Block A → Block B → JMP (conditions in separate blocks)
    2. Simple OR: Multiple blocks with different conditions jumping to same target
    3. Combined: (AND) OR (AND) - multiple AND chains to same TRUE target

    Args:
        cfg: Control flow graph
        header_block_id: Starting block to analyze
        resolver: Opcode resolver
        start_to_block: Mapping from addresses to block IDs
        ssa_func: SSA function for condition extraction
        formatter: Expression formatter

    Returns:
        CompoundCondition if pattern detected, None otherwise
    """
    # Step 1: Try to collect an AND chain starting from this block
    visited = set()
    and_blocks, true_target, false_target = _collect_and_chain(
        header_block_id, cfg, resolver, start_to_block, visited
    )

    # No AND chain detected
    if not and_blocks:
        return None

    # Step 2: Extract conditions from each block in the AND chain
    and_conditions = []
    for block_id in and_blocks:
        cond = _extract_condition_from_block(
            block_id, ssa_func, formatter, cfg, resolver
        )
        if cond:
            and_conditions.append(cond)

    if not and_conditions:
        return None

    # Step 3: Create AND compound (or single condition if len==1)
    if len(and_conditions) > 1:
        and_compound = CompoundCondition(
            operator="&&",
            conditions=and_conditions,
            true_target=true_target if true_target is not None else -1,
            false_target=false_target if false_target is not None else -1,
            involved_blocks=set(and_blocks)
        )
    else:
        # Single condition - might still be part of OR
        and_compound = and_conditions[0]  # Just the string

    # Step 4: Check if false_target leads to another OR branch
    if false_target is None or true_target is None:
        # No clear targets, return what we have
        if isinstance(and_compound, CompoundCondition):
            return and_compound
        return None

    # Step 5: Recursively check if false_target is start of another AND chain
    # that jumps to the SAME true_target (indicating OR)
    next_branch = _detect_short_circuit_pattern(
        cfg, false_target, resolver, start_to_block, ssa_func, formatter
    )

    # Step 6: If next branch jumps to same TRUE target, combine with OR
    if next_branch and next_branch.true_target == true_target:
        # Build OR compound
        or_conditions = []
        or_involved_blocks = set()

        # Add first AND branch
        if isinstance(and_compound, CompoundCondition):
            or_conditions.append(and_compound)
            or_involved_blocks.update(and_compound.involved_blocks)
        else:
            or_conditions.append(and_compound)
            or_involved_blocks.update(and_blocks)

        # Add second AND branch (or more if recursively nested)
        or_conditions.append(next_branch)
        or_involved_blocks.update(next_branch.involved_blocks)

        return CompoundCondition(
            operator="||",
            conditions=or_conditions,
            true_target=true_target,
            false_target=next_branch.false_target,  # Use last branch's false target
            involved_blocks=or_involved_blocks
        )

    # No OR detected, return the AND compound
    if isinstance(and_compound, CompoundCondition):
        return and_compound

    # Single condition, not compound
    return None


def _detect_if_else_pattern(
    cfg: CFG,
    block_id: int,
    start_to_block: Dict[int, int],
    resolver: opcodes.OpcodeResolver,
    visited_ifs: Set[int],
    func_loops: Optional[List] = None,
    context_stop_blocks: Optional[Set[int]] = None,
    ssa_func: Optional[SSAFunction] = None,
    formatter: Optional = None  # ExpressionFormatter
) -> Optional[IfElsePattern]:
    """
    Detect if/else pattern starting at block_id.

    Pattern:
    - Block ends with conditional jump (JZ/JNZ)
    - Has exactly 2 successors (true and false branches)
    - Branches may or may not merge at a common successor

    NOTE: If ssa_func and formatter are provided, will attempt to detect
    compound conditions (AND/OR chains) before falling back to simple if/else.

    Args:
        cfg: Control flow graph
        block_id: Block to check
        start_to_block: Address to block ID mapping
        resolver: Opcode resolver
        visited_ifs: Set of already processed if patterns
        func_loops: List of loops in function (optional, to avoid misdetecting loop headers)
        context_stop_blocks: Blocks to stop at (for switch case analysis)
        ssa_func: SSA function (optional, for compound condition detection)
        formatter: Expression formatter (optional, for compound condition detection)
    """
    if block_id in visited_ifs:
        return None

    # NEW: Try to detect compound conditions first (if we have SSA/formatter available)
    # This must be done BEFORE simple if/else detection to avoid breaking up compound patterns
    if ssa_func is not None and formatter is not None:
        compound = _detect_short_circuit_pattern(
            cfg, block_id, resolver, start_to_block, ssa_func, formatter
        )
        if compound:
            # Convert CompoundCondition to IfElsePattern for compatibility
            # Mark all involved blocks as visited to prevent re-processing
            for involved_block in compound.involved_blocks:
                visited_ifs.add(involved_block)

            # Create IfElsePattern representing the compound condition
            # We'll use a special marker to indicate this is compound
            if_pattern = IfElsePattern(
                header_block=block_id,
                true_block=compound.true_target,
                false_block=compound.false_target,
                merge_block=-1  # Will be determined later
            )
            # Store compound info in the pattern for later rendering
            # We'll use a custom attribute (Python allows this)
            if_pattern.compound = compound  # type: ignore
            return if_pattern

    # FÁZE 3.2 FIX: Don't detect loop headers as if/else
    # Loop headers have back edges and should be handled by loop detection instead
    if func_loops:
        for loop in func_loops:
            if loop.header == block_id:
                return None  # This is a loop header, not an if/else

    block = cfg.blocks.get(block_id)
    if not block or not block.instructions:
        return None

    last_instr = block.instructions[-1]
    if not resolver.is_conditional_jump(last_instr.opcode):
        return None

    # FÁZE 2C: Allow 1 or 2 successors (1 = if-without-else, 2 = if/else)
    if len(block.successors) < 1 or len(block.successors) > 2:
        return None

    # Get true and false blocks
    # CRITICAL FIX: JZ vs JNZ have opposite semantics!
    # JZ (Jump if Zero) = jump when condition is FALSE (zero)
    #   -> arg1 is FALSE branch, fallthrough is TRUE branch
    # JNZ (Jump if Not Zero) = jump when condition is TRUE (not zero)
    #   -> arg1 is TRUE branch, fallthrough is FALSE branch

    mnemonic = resolver.get_mnemonic(last_instr.opcode)
    jump_addr = last_instr.arg1
    fallthrough_addr = last_instr.address + 1

    if mnemonic == "JZ":
        # JZ: jump target is FALSE branch, fallthrough is TRUE branch
        true_addr = fallthrough_addr
        false_addr = jump_addr
    elif mnemonic == "JNZ":
        # JNZ: jump target is TRUE branch, fallthrough is FALSE branch
        true_addr = jump_addr
        false_addr = fallthrough_addr
    else:
        # Other conditional jumps - assume JZ behavior (most common)
        true_addr = fallthrough_addr
        false_addr = jump_addr

    true_block = start_to_block.get(true_addr)
    if true_block is None:
        return None

    # For if-without-else, false branch might not exist (just fallthrough to merge)
    false_block = start_to_block.get(false_addr)

    # If only 1 successor, this is if-without-else (jump target is true branch, no false branch)
    if len(block.successors) == 1:
        false_block = None  # No else branch

    # Find merge point (common successor)
    # For if-without-else, merge point is the fallthrough (false_block will be None)
    if false_block is not None:
        merge_block = _find_common_successor(cfg, true_block, false_block)
    else:
        # If-without-else: merge point is the next block after jump
        merge_block = start_to_block.get(false_addr)

    # Find all blocks in each branch
    # CRITICAL FIX: Exclude the other branch from body detection to prevent overlap
    stop_blocks = {merge_block} if merge_block else set()

    # BUG FIX #4: Add context stop blocks (e.g., switch case boundaries)
    if context_stop_blocks:
        stop_blocks.update(context_stop_blocks)

    # For true branch, exclude false branch entry to prevent crossing
    true_stop = stop_blocks | {false_block} if false_block else stop_blocks
    true_body = _find_if_body_blocks(cfg, true_block, true_stop, resolver)

    # For false branch, exclude true branch entry to prevent crossing
    if false_block:
        # CRITICAL FIX: If false_block IS the merge point, there's no else branch
        if false_block == merge_block:
            false_body = set()
        else:
            # FÁZE 3.1 FIX: Check if false_block is "empty" (just unconditional JMP)
            # This happens when compiler optimizes: if (cond) { return; }
            # The false branch is just "JMP to merge", not actual else code
            false_block_obj = cfg.blocks.get(false_block)
            is_empty_false = False

            if false_block_obj and false_block_obj.instructions:
                # Check if first instruction is unconditional JMP
                first_instr = false_block_obj.instructions[0]
                if resolver.get_mnemonic(first_instr.opcode) == "JMP":
                    # Empty false branch - just jumps to merge point
                    is_empty_false = True

            if is_empty_false:
                false_body = set()
            else:
                false_stop = stop_blocks | {true_block}
                false_body = _find_if_body_blocks(cfg, false_block, false_stop, resolver)
    else:
        false_body = set()

    visited_ifs.add(block_id)

    return IfElsePattern(
        header_block=block_id,
        true_block=true_block,
        false_block=false_block,
        merge_block=merge_block,
        true_body=true_body,
        false_body=false_body
    )


def _find_case_body_blocks(cfg: CFG, case_entry: int, stop_blocks: Set[int], resolver: opcodes.OpcodeResolver) -> Set[int]:
    """
    Find all blocks belonging to a case body using BFS.

    Args:
        cfg: Control flow graph
        case_entry: Entry block of the case
        stop_blocks: Blocks where we should stop (other case entries, exit, default)
        resolver: Opcode resolver

    Returns:
        Set of all block IDs in the case body
    """
    body_blocks: Set[int] = set()
    worklist = [case_entry]
    visited: Set[int] = set()

    while worklist:
        block_id = worklist.pop(0)

        # Skip if already visited
        if block_id in visited:
            continue

        # Stop at barriers (other cases, exit, etc.)
        if block_id in stop_blocks and block_id != case_entry:
            continue

        visited.add(block_id)
        body_blocks.add(block_id)

        # Get block and check if it ends with return
        block = cfg.blocks.get(block_id)
        if block and block.instructions:
            last_instr = block.instructions[-1]
            if resolver.is_return(last_instr.opcode):
                continue  # Don't follow after return

        # Add successors to worklist
        if block:
            for succ in block.successors:
                if succ not in visited:
                    worklist.append(succ)

    return body_blocks


def _trace_value_to_global(value, formatter: ExpressionFormatter, visited=None) -> Optional[str]:
    """
    Trace an SSA value back to its global variable source.

    If value comes from GCP/GLD (load from global), return the global variable name.
    Otherwise return None.

    Pattern:
        GCP/GLD offset -> produces value with alias local_X
        We want to return the global name for that offset instead.

    Also handles indirection through stack:
        GCP offset -> stack -> LCP -> value
        In this case, LCP loads from stack where GCP stored the value.
    """
    if not value:
        return None

    # Prevent infinite recursion
    if visited is None:
        visited = set()
    if id(value) in visited:
        return None
    visited.add(id(value))

    # Check if value itself is a data_X alias (direct global reference)
    if value.alias and value.alias.startswith("data_"):
        try:
            offset = int(value.alias[5:])
            if hasattr(formatter, '_global_names'):
                global_name = formatter._global_names.get(offset)
                if global_name:
                    return global_name
        except ValueError:
            pass

    if not value.producer_inst:
        return None

    producer = value.producer_inst

    # Check if producer is GCP or GLD (global load)
    if producer.mnemonic in {"GCP", "GLD"}:
        if producer.instruction and producer.instruction.instruction:
            dword_offset = producer.instruction.instruction.arg1
            # Check if formatter has global name for this offset
            if hasattr(formatter, '_global_names'):
                global_name = formatter._global_names.get(dword_offset)
                if global_name:
                    return global_name

    # CRITICAL FIX: Check if producer is LCP (load from stack)
    # Pattern: GCP -> stack push -> LCP -> value
    # In this case, we need to trace through PHI or find the value's source
    elif producer.mnemonic == "LCP":
        # LCP loads from stack - the value might have been stored by GCP earlier
        # Try to find the source through PHI sources
        if value.phi_sources:
            for _, phi_source in value.phi_sources:
                global_name = _trace_value_to_global(phi_source, formatter, visited)
                if global_name:
                    return global_name

    # Check if producer is DCP (load from memory via pointer)
    # Pattern: GADR global -> DCP -> value
    # This happens when global is loaded via pointer dereference
    elif producer.mnemonic == "DCP":
        if len(producer.inputs) > 0:
            addr_value = producer.inputs[0]
            # Trace the address - might be GADR
            if addr_value.producer_inst and addr_value.producer_inst.mnemonic == "GADR":
                if addr_value.producer_inst.instruction and addr_value.producer_inst.instruction.instruction:
                    dword_offset = addr_value.producer_inst.instruction.instruction.arg1
                    if hasattr(formatter, '_global_names'):
                        global_name = formatter._global_names.get(dword_offset)
                        if global_name:
                            return global_name

    # Check if producer is PHI (merge point) - trace through inputs
    elif producer.mnemonic == "PHI":
        # Try to find global source from any PHI input
        for inp in producer.inputs:
            global_name = _trace_value_to_global(inp, formatter, visited)
            if global_name:
                return global_name

    return None


def _trace_value_to_parameter(value, formatter: ExpressionFormatter, ssa_func: SSAFunction) -> Optional[str]:
    """
    Trace an SSA value back to its parameter source.

    If value comes from LCP (load from stack parameter), return the parameter field access.
    Otherwise return None.

    Pattern:
        LCP [sp+offset] -> produces value
        We want to return the parameter field access for that offset.

    For ScriptMain(s_SC_NET_info *info):
        LCP [sp+306] = info->message (offset 0 in s_SC_NET_info)
        LCP [sp+310] = info->param1  (offset 4 in s_SC_NET_info)
        etc.
    """
    if not value:
        return None

    if not value.producer_inst:
        return None

    producer = value.producer_inst

    # Check if producer is LCP (load from stack/parameter)
    if producer.mnemonic == "LCP":
        if producer.instruction and producer.instruction.instruction:
            stack_offset = producer.instruction.instruction.arg1

            # Heuristic: if offset is in range 306-326, likely s_SC_NET_info parameter
            # This is a common pattern in VC scripts for ScriptMain function
            # Map common offsets seen in tdm.scr
            field_map = {
                306: "message",      # offset 0
                310: "param1",       # offset 4
                314: "param2",       # offset 8
                318: "param3",       # offset 12
                322: "elapsed_time", # offset 16
                326: "fval1",        # offset 20
            }

            field_name = field_map.get(stack_offset)
            if field_name:
                # Default parameter name for ScriptMain
                param_name = "info"

                # Try to get better parameter name from function signature
                if hasattr(formatter, '_func_signature') and formatter._func_signature:
                    func_sig = formatter._func_signature
                    if func_sig.param_types:
                        # Check if any parameter mentions s_SC_NET_info
                        for param_type in func_sig.param_types:
                            if 's_SC_NET_info' in param_type:
                                # Extract parameter name from "s_SC_NET_info *info"
                                parts = param_type.split()
                                if parts:
                                    param_name = parts[-1]
                                break

                return f"{param_name}->{field_name}"

            # Fallback: check if this is a simple parameter load
            # Parameters are typically at positive stack offsets in VC compiler
            # Try to use parameter name mapping if available
            if hasattr(formatter, '_param_names'):
                param_name = formatter._param_names.get(stack_offset)
                if param_name:
                    return param_name

    return None


def _find_switch_variable_from_nearby_gcp(
    ssa_func: SSAFunction,
    current_block_id: int,
    var_value,
    formatter: ExpressionFormatter,
    func_block_ids: Set[int]
) -> Optional[str]:
    """
    Heuristic to find switch variable when normal tracing fails.

    Pattern: Compiler generates code like:
        Block 1: GCP data[X]  # Load global variable
                 JMP Block 2
        Block 2: LCP [sp+0]   # Load from stack (but value didn't propagate through CFG)
                 ...
                 EQU          # Compare in switch

    We look for GCP instructions in SSA blocks (which preserve correct mnemonics)
    to find the first global variable load - this is likely the switch variable.
    """
    import sys

    # Search through SSA instructions (which have correct mnemonics)
    ssa_blocks = ssa_func.instructions  # Dict[block_id, List[SSAInstruction]]

    # Find the FIRST (earliest) GCP/GLD instruction in the entire function
    # that loads a global variable - this is likely the switch variable
    gcp_candidates = []

    # Collect all GCP/GLD from all SSA blocks in function
    for block_id in func_block_ids:
        if block_id not in ssa_blocks:
            continue

        ssa_instrs = ssa_blocks[block_id]
        for ssa_instr in ssa_instrs:
            if ssa_instr.mnemonic in {'GCP', 'GLD'}:
                # Found a global load!
                # Get the dword offset from instruction
                if hasattr(ssa_instr, 'instruction') and hasattr(ssa_instr.instruction, 'instruction'):
                    dword_offset = ssa_instr.instruction.instruction.arg1

                    if hasattr(formatter, '_global_names'):
                        global_name = formatter._global_names.get(dword_offset)
                        if global_name:
                            # Record this as candidate with instruction address
                            gcp_candidates.append((ssa_instr.address, global_name, dword_offset))

    # If we found any GCP, use the FIRST one (earliest in function)
    if gcp_candidates:
        # Sort by instruction address (earliest first)
        gcp_candidates.sort(key=lambda x: x[0])
        # Return the first global variable name
        return gcp_candidates[0][1]

    return None


def _detect_switch_patterns(
    ssa_func: SSAFunction,
    func_block_ids: Set[int],
    formatter: ExpressionFormatter,
    start_to_block: Dict[int, int]
) -> List[SwitchPattern]:
    """
    Detect switch/case patterns in the function.

    A switch pattern consists of:
    1. Multiple consecutive blocks testing the SAME variable
    2. Each test is an equality comparison (EQU) with a constant
    3. Each test jumps to different case bodies on match
    4. All tests share a common exit point

    Pattern example:
        Block A: if (var == 0) goto case_0; else goto Block B
        Block B: if (var == 1) goto case_1; else goto Block C
        Block C: if (var == 2) goto case_2; else goto default
    """
    cfg = ssa_func.cfg
    resolver = getattr(ssa_func.scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    ssa_blocks = ssa_func.instructions
    switches: List[SwitchPattern] = []
    processed_blocks: Set[int] = set()

    # Iterate through blocks looking for switch headers
    for block_id in func_block_ids:
        if block_id in processed_blocks:
            continue

        block = cfg.blocks.get(block_id)
        if not block or not block.instructions:
            continue

        # Start collecting potential switch cases
        test_var = None
        cases: List[CaseInfo] = []
        chain_blocks: List[int] = []
        current_block = block_id

        # Follow the chain of equality tests
        while current_block is not None and current_block in func_block_ids:
            if current_block in processed_blocks:
                break

            curr_block_obj = cfg.blocks.get(current_block)
            if not curr_block_obj or not curr_block_obj.instructions:
                break

            last_instr = curr_block_obj.instructions[-1]
            opcode = last_instr.opcode

            # Must be conditional jump
            if not resolver.is_conditional_jump(opcode):
                break


            # Get SSA instructions for this block
            ssa_block = ssa_blocks.get(current_block, [])

            # Find the condition (should be EQU comparison)
            # JZ/JNZ takes the result of EQU as input, so we need to find the EQU that produces the condition
            found_equ = False

            # Find the JZ/JNZ instruction in SSA
            jump_ssa = None
            for ssa_inst in ssa_block:
                if ssa_inst.address == last_instr.address:
                    jump_ssa = ssa_inst
                    break

            if jump_ssa and len(jump_ssa.inputs) > 0:
                # The condition value is the first input to JZ/JNZ
                condition_value = jump_ssa.inputs[0]

                # Find the producer of this condition (should be EQU)
                equ_inst = None
                for ssa_inst in ssa_block:
                    if any(out.name == condition_value.name for out in ssa_inst.outputs):
                        equ_inst = ssa_inst
                        break

                if equ_inst and equ_inst.mnemonic == "EQU" and len(equ_inst.inputs) >= 2:
                    var_value = equ_inst.inputs[0]
                    const_value = equ_inst.inputs[1]

                    # Get variable name - try to trace back to parameter first, then global
                    var_name = _trace_value_to_parameter(var_value, formatter, ssa_func)
                    if not var_name:
                        var_name = _trace_value_to_global(var_value, formatter)

                    # CRITICAL FIX for Switch Variable Tracking:
                    # If normal tracing failed, use heuristic to find switch variable
                    # from nearby GCP instructions. This is needed because compiler generates
                    # code where global is loaded once at function entry but not properly
                    # propagated through CFG to switch comparison blocks.
                    if not var_name:
                        # Look for GCP in SSA blocks - works for all iterations, not just first
                        # IMPORTANT: Pass SSA function, not CFG, to get correct mnemonics
                        var_name = _find_switch_variable_from_nearby_gcp(
                            ssa_func, current_block, var_value, formatter, func_block_ids
                        )

                    if not var_name:
                        # Fall back to regular rendering if neither parameter nor global
                        var_name = formatter.render_value(var_value)

                    # Check if first switch or same variable
                    if test_var is None:
                        test_var = var_name
                    elif test_var != var_name:
                        # Different variable, not part of switch
                        # Don't process this block, break the loop
                        break

                    # Same variable (or first case), try to extract constant value
                    case_val = None
                    if const_value.alias and const_value.alias.startswith("data_"):
                        try:
                            offset = int(const_value.alias[5:])
                            if ssa_func.scr and ssa_func.scr.data_segment:
                                case_val = ssa_func.scr.data_segment.get_dword(offset * 4)
                        except (ValueError, AttributeError):
                            pass

                    if case_val is not None:
                            # This is a valid case!
                            # Determine which successor is the case body
                            # JZ means jump if zero (condition false), so arg1 is NOT the case
                            # JNZ means jump if not zero (condition true), so arg1 IS the case
                            mnemonic = resolver.get_mnemonic(opcode)
                            if mnemonic == "JNZ":
                                case_block = last_instr.arg1
                            else:  # JZ
                                # Fall-through is the case body
                                case_block = last_instr.address + 1

                            # Convert address to block ID
                            case_block_id = None
                            for bid, b in cfg.blocks.items():
                                if b.start == case_block:
                                    case_block_id = bid
                                    break

                            if case_block_id is not None:
                                cases.append(CaseInfo(value=case_val, block_id=case_block_id))
                                chain_blocks.append(current_block)
                                found_equ = True

                                # Find next block in chain
                                if mnemonic == "JNZ":
                                    # Fall-through is next test
                                    next_addr = last_instr.address + 1
                                else:  # JZ
                                    # Jump target is next test
                                    next_addr = last_instr.arg1

                                # Find next block
                                next_block = None
                                for bid, b in cfg.blocks.items():
                                    if b.start == next_addr:
                                        next_block = bid
                                        break
                                current_block = next_block
                            else:
                                pass  # Case block ID not found

            if not found_equ:
                break

        # If we found at least 2 cases, it's a switch
        if len(cases) >= 2:

            # Find the exit block - common successor of all case blocks
            # For now, we'll use a simple heuristic: find the most common successor
            # that is not part of the switch itself
            all_case_blocks = {case.block_id for case in cases}
            exit_candidates: Dict[int, int] = {}  # block_id -> count

            for case in cases:
                # Find successors of the case block
                case_block = cfg.blocks.get(case.block_id)
                if case_block:
                    for succ in case_block.successors:
                        if succ not in all_case_blocks and succ not in chain_blocks:
                            exit_candidates[succ] = exit_candidates.get(succ, 0) + 1

            # The exit block is the one referenced by most cases
            exit_block = None
            if exit_candidates:
                exit_block = max(exit_candidates.items(), key=lambda x: x[1])[0]

                # FÁZE 1.3 FIX: If exit block is just a JMP, follow it to find the real exit
                exit_blk = cfg.blocks.get(exit_block)
                if exit_blk and exit_blk.instructions and len(exit_blk.instructions) == 1:
                    instr = exit_blk.instructions[0]
                    mnem = resolver.get_mnemonic(instr.opcode)
                    if mnem == "JMP":
                        # Follow the JMP to find real exit
                        real_exit = start_to_block.get(instr.arg1)
                        if real_exit is not None:
                            exit_block = real_exit

            # Collect all blocks belonging to the switch (initially just chain and case entries)
            all_blocks = set(chain_blocks)
            all_blocks.update(all_case_blocks)
            if current_block is not None:
                all_blocks.add(current_block)  # default block

            # Find body blocks for each case using graph traversal
            # Build stop blocks: all case entries + exit + default
            stop_blocks = all_case_blocks.copy()
            # BUG FIX: Add chain blocks (test blocks) to prevent BFS from crossing into next case test
            stop_blocks.update(chain_blocks)
            if exit_block is not None:
                stop_blocks.add(exit_block)
            if current_block is not None:
                stop_blocks.add(current_block)

            # For each case, find all blocks in its body
            for case in cases:
                case.body_blocks = _find_case_body_blocks(
                    cfg, case.block_id, stop_blocks, resolver
                )
                # BUG FIX #3: Add this case's body to stop_blocks so next cases don't cross into it
                stop_blocks.update(case.body_blocks)
                # Update all_blocks to include all case body blocks
                all_blocks.update(case.body_blocks)

            # Also find body blocks for default case if present
            default_body = None
            if current_block is not None:
                default_body = _find_case_body_blocks(
                    cfg, current_block, stop_blocks, resolver
                )
                all_blocks.update(default_body)

            switch = SwitchPattern(
                test_var=test_var,
                header_block=block_id,
                cases=cases,
                default_block=current_block,  # Last block in chain is default
                default_body_blocks=default_body,
                exit_block=exit_block,
                all_blocks=all_blocks,
            )
            switches.append(switch)
            processed_blocks.update(chain_blocks)

    return switches


def _collect_local_variables(ssa_func: SSAFunction, func_block_ids: Set[int], formatter) -> List[str]:
    """
    Collect local variable declarations for a function.

    Returns list of declaration strings like "int i", "float local_2", etc.
    """
    from collections import defaultdict

    # Track variable names and their types
    var_types: Dict[str, str] = {}

    # P0.3: Track local arrays detected from usage patterns
    local_arrays: Dict[str, Tuple[str, int]] = {}  # var_name -> (element_type, size)

    def process_value(value, default_type="int"):
        """Process a value to extract variable names and types."""
        if not value:
            return

        var_name = value.alias or value.name
        if not var_name:
            return

        # Strip & prefix to get actual variable name
        is_addr_of = var_name.startswith("&")
        if is_addr_of:
            var_name = var_name[1:]

        # Only process local variables (local_X, i, j, etc.)
        # Skip parameters (param_X, info), globals (data_X, gVar), SSA temps (tX_X), and PHI values
        if var_name.startswith("param_") or var_name.startswith("data_") or var_name == "info":
            return
        if var_name.startswith("t") and "_" in var_name:  # Skip tX_X temps
            return
        if var_name.startswith("phi_"):  # Skip PHI nodes (SSA internals)
            return
        if var_name.startswith("gData") or var_name.startswith("gVar"):  # Skip globals
            return

        # Check if variable has semantic name (i, player_info, etc.)
        display_name = var_name
        if var_name.startswith("local_"):
            semantic_name = formatter._semantic_names.get(var_name)
            if semantic_name:
                display_name = semantic_name

        # Don't re-declare if we already have this variable
        if display_name in var_types:
            return

        # Determine type from instruction or value type
        var_type = default_type

        # Check if this is a structure variable (has field access)
        if var_name.startswith("local_"):
            # Check if formatter knows this is a struct
            struct_info = formatter._struct_ranges.get(var_name)
            if struct_info:
                # struct_info is a tuple like (start, end, 'struct_name')
                # Extract just the struct name
                if isinstance(struct_info, tuple) and len(struct_info) >= 3:
                    var_type = struct_info[2]
                else:
                    var_type = str(struct_info)
            else:
                # Infer from value type
                if value.value_type == opcodes.ResultType.FLOAT:
                    var_type = "float"
                elif value.value_type == opcodes.ResultType.DOUBLE:
                    var_type = "double"
                # Don't use void* unless we're sure it's a pointer
                # Most POINTER types in SSA are actually int addresses
                else:
                    var_type = default_type
        else:
            # Simple variables (i, j, etc.)
            if value.value_type == opcodes.ResultType.FLOAT:
                var_type = "float"
            elif value.value_type == opcodes.ResultType.DOUBLE:
                var_type = "double"
            else:
                var_type = default_type

        # Store variable type
        var_types[display_name] = var_type

    # P0.3: First pass - detect local arrays from usage patterns
    for block_id in func_block_ids:
        ssa_instrs = ssa_func.instructions.get(block_id, [])
        for inst in ssa_instrs:
            # Pattern 1: sprintf(&local_X, ...) → char array
            if inst.mnemonic == "XCALL" and inst.inputs:
                # Get function name from XFN table
                call_name = None
                if inst.instruction and inst.instruction.instruction:
                    xfn_idx = inst.instruction.instruction.arg1
                    xfn_entry = ssa_func.scr.get_xfn(xfn_idx) if ssa_func.scr else None
                    if xfn_entry:
                        full_name = xfn_entry.name
                        paren_idx = full_name.find("(")
                        call_name = full_name[:paren_idx] if paren_idx > 0 else full_name

                if call_name == "sprintf" and len(inst.inputs) >= 1:
                    # First argument is buffer
                    buffer_arg = inst.inputs[0]
                    buf_name = buffer_arg.alias or buffer_arg.name
                    if buf_name and buf_name.startswith("&local_"):
                        var_name = buf_name[1:]  # Strip &
                        local_arrays[var_name] = ("char", 32)  # Default buffer size

            # Pattern 2: SC_ZeroMem(&local_X, size) → byte array
            if inst.mnemonic == "XCALL" and inst.inputs and inst.mnemonic == "XCALL":
                # Get function name from XFN table
                call_name = None
                if inst.instruction and inst.instruction.instruction:
                    xfn_idx = inst.instruction.instruction.arg1
                    xfn_entry = ssa_func.scr.get_xfn(xfn_idx) if ssa_func.scr else None
                    if xfn_entry:
                        full_name = xfn_entry.name
                        paren_idx = full_name.find("(")
                        call_name = full_name[:paren_idx] if paren_idx > 0 else full_name

                if call_name and "ZeroMem" in call_name and len(inst.inputs) >= 2:
                    # First arg is buffer, second is size
                    buffer_arg = inst.inputs[0]
                    size_arg = inst.inputs[1]

                    buf_name = buffer_arg.alias or buffer_arg.name
                    # Skip globals
                    if buf_name and buf_name.startswith("&local_"):
                        var_name = buf_name[1:]  # Strip &
                        # Try to get constant size
                        size = 64  # Default
                        if hasattr(size_arg, 'constant_value'):
                            size = size_arg.constant_value
                        elif size_arg.producer_inst and size_arg.producer_inst.mnemonic in ["IPUSH", "PUSH"]:
                            # Size is a constant
                            if size_arg.producer_inst.instruction:
                                size = size_arg.producer_inst.instruction.instruction.arg1

                        # Infer element type from size
                        if size == 60 or size == 156:  # Known struct sizes
                            # This is likely a struct, keep as int for now
                            pass
                        elif size >= 8:
                            # Likely an array
                            element_type = "dword"
                            array_size = size // 4
                            local_arrays[var_name] = (element_type, array_size)

    # Process all instructions in function blocks
    for block_id in func_block_ids:
        ssa_instrs = ssa_func.instructions.get(block_id, [])
        for inst in ssa_instrs:
            # Check outputs (variables being assigned)
            for output in inst.outputs:
                process_value(output, default_type="int")

            # Check inputs (variables being read) - these might be address-of operations
            for inp in inst.inputs:
                process_value(inp, default_type="int")

    # P0.3: Generate declarations (arrays first, then regular variables)
    declarations = []

    # First, declare arrays
    for var_name in sorted(var_types.keys()):
        if var_name in local_arrays:
            element_type, array_size = local_arrays[var_name]
            declarations.append(f"{element_type} {var_name}[{array_size}]")

    # Then, declare regular variables (skip arrays)
    for var_name in sorted(var_types.keys()):
        if var_name not in local_arrays:
            var_type = var_types[var_name]
            declarations.append(f"{var_type} {var_name}")

    return declarations


def format_structured_function_named(ssa_func: SSAFunction, func_name: str, entry_addr: int, end_addr: int = None, function_bounds=None) -> str:
    """
    Format structured output for a specific function with custom name and entry point.

    Args:
        ssa_func: SSA function data
        func_name: Name of the function
        entry_addr: Entry address of the function
        end_addr: End address of the function (optional, for linear output mode)
        function_bounds: Optional dict {func_name: (start_addr, end_addr)} for CALL resolution (FÁZE 4)

    Uses per-function ExpressionFormatter with function boundaries for 100% reliable
    structure field detection. This ensures local_0 in different functions correctly
    maps to different structure types.
    """
    cfg = ssa_func.cfg
    resolver = getattr(ssa_func.scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
    start_to_block = _build_start_map(cfg)
    lines: List[str] = []
    # Load symbol database for global variable name resolution
    symbol_db = _load_symbol_db()

    # FÁZE 3.3: Detect function signature to get parameter names
    from .function_signature import detect_function_signature
    func_sig = detect_function_signature(ssa_func, entry_addr, end_addr)

    # Find the entry block for this function
    entry_block = start_to_block.get(entry_addr)
    if entry_block is None:
        return f"// Function {func_name} at {entry_addr} - entry block not found"

    # Find blocks in this function (MOVED UP - needed for VariableRenamer)
    func_block_ids: Set[int] = set()
    for block_id, block in cfg.blocks.items():
        if block.start >= entry_addr:
            if end_addr is None or block.start <= end_addr:
                func_block_ids.add(block_id)

    # FIX 2: Variable name collision resolution
    # Run variable renaming BEFORE creating formatter to detect and resolve collisions
    from .variable_renaming import VariableRenamer
    renamer = VariableRenamer(ssa_func, func_block_ids)
    rename_map = renamer.analyze_and_rename()

    # Create per-function formatter with function boundaries for accurate structure detection
    # FÁZE 3.3: Pass parameter info for correct aliasing
    # FÁZE 4: Pass function_bounds for CALL resolution
    # FIX 2: Pass rename_map for variable collision resolution
    formatter = ExpressionFormatter(ssa_func, func_start=entry_addr, func_end=end_addr, func_name=func_name, symbol_db=symbol_db, func_signature=func_sig, function_bounds=function_bounds, rename_map=rename_map)
    ssa_blocks = ssa_func.instructions

    # Detect loops in this function using local dominator computation
    func_loops = find_loops_in_function(cfg, func_block_ids, entry_block)

    # Resolve global variables for better naming in for-loop conditions
    from .global_resolver import resolve_globals
    global_map = resolve_globals(ssa_func)

    # Detect switch/case patterns
    switch_patterns = _detect_switch_patterns(ssa_func, func_block_ids, formatter, start_to_block)

    # Build map: block_id -> switch pattern (for quick lookup)
    block_to_switch: Dict[int, SwitchPattern] = {}
    for switch in switch_patterns:
        for block_id in switch.all_blocks:
            block_to_switch[block_id] = switch

    # FÁZE 2A: Removed if/else pre-detection - now done during rendering
    # This allows detection to work correctly after switch emission modifies CFG structure
    block_to_if: Dict[int, IfElsePattern] = {}  # Will be populated during rendering
    visited_ifs: Set[int] = set()               # Track visited if patterns

    # Track which loop headers we've seen
    emitted_loop_headers: Set[int] = set()

    # Determine function signature using bytecode analysis
    from .function_signature import get_function_signature_string
    scr = ssa_func.scr

    # Get complete signature (handles both entry points and internal functions)
    signature = get_function_signature_string(
        ssa_func,
        func_name,
        entry_addr,
        end_addr,
        scr_header_enter_size=scr.header.enter_size
    )

    lines.append(f"{signature} {{")

    # Collect local variable declarations
    local_vars = _collect_local_variables(ssa_func, func_block_ids, formatter)
    if local_vars:
        for var_decl in sorted(local_vars):
            lines.append(f"    {var_decl};")
        lines.append("")  # Empty line after declarations

    # Linear output mode: output all blocks in address range
    func_blocks = []
    for block_id, block in cfg.blocks.items():
        if block.start >= entry_addr:
            if end_addr is None or block.start <= end_addr:
                func_blocks.append((block.start, block_id, block))

    # Sort by address
    func_blocks.sort(key=lambda x: x[0])

    # Track active loops (stack for nesting)
    active_loops: List[NaturalLoop] = []

    # Find which loops each block belongs to (for proper scope tracking)
    block_to_loops: Dict[int, List[NaturalLoop]] = {}
    for block_id in func_block_ids:
        block_to_loops[block_id] = [l for l in func_loops if block_id in l.body]
        # Sort by size (smallest/innermost first)
        block_to_loops[block_id].sort(key=lambda l: len(l.body))

    emitted_switches: Set[int] = set()  # Track which switches we've rendered
    emitted_ifs: Set[int] = set()       # Track which if/else patterns we've rendered
    emitted_blocks: Set[int] = set()    # Track all blocks we've rendered

    for idx, (addr, block_id, block) in enumerate(func_blocks):
        # Skip blocks that have already been rendered
        if block_id in emitted_blocks:
            continue

        # Skip blocks that are part of a switch pattern (except header)
        if block_id in block_to_switch:
            switch = block_to_switch[block_id]
            # If this is not the header, and we've already emitted the switch, skip it
            if block_id != switch.header_block and switch.header_block in emitted_switches:
                continue
            # If this is a switch block but not the header, skip for now
            if block_id != switch.header_block:
                continue

        # FÁZE 2B: Runtime if/else detection (moved from pre-processing)
        # Try to detect if/else pattern if not already known and not part of switch
        # NEW: Pass ssa_func and formatter for compound condition detection
        if block_id not in block_to_if and block_id not in block_to_switch:
            if_pattern = _detect_if_else_pattern(cfg, block_id, start_to_block, resolver, visited_ifs, func_loops, ssa_func=ssa_func, formatter=formatter)
            if if_pattern:
                # Register this pattern
                block_to_if[if_pattern.header_block] = if_pattern
                for body_block_id in if_pattern.true_body:
                    if body_block_id not in block_to_if:
                        block_to_if[body_block_id] = if_pattern
                for body_block_id in if_pattern.false_body:
                    if body_block_id not in block_to_if:
                        block_to_if[body_block_id] = if_pattern

        # Skip blocks that are part of an if/else pattern (except header)
        if block_id in block_to_if:
            if_pattern = block_to_if[block_id]
            # If this is not the header, and we've already emitted the if, skip it
            if block_id != if_pattern.header_block and if_pattern.header_block in emitted_ifs:
                continue
            # If this is an if body block but not the header, skip for now
            if block_id != if_pattern.header_block:
                continue

        # Check if we need to close any loops (block is not in their body)
        loops_to_close = []
        for loop in active_loops:
            if block_id not in loop.body:
                loops_to_close.append(loop)
        for loop in loops_to_close:
            active_loops.remove(loop)
            indent = "    " + "    " * len(active_loops)
            lines.append(f"{indent}}}")

        # Check if this is a switch header
        if block_id in block_to_switch and block_id == block_to_switch[block_id].header_block:
            switch = block_to_switch[block_id]
            base_indent = "    " + "    " * len(active_loops)

            # Render switch statement
            lines.append(f"{base_indent}switch ({switch.test_var}) {{")
            for case in switch.cases:
                lines.append(f"{base_indent}case {case.value}:")
                # Render all blocks in case body (sorted by address) with loop support
                case_body_sorted = sorted(case.body_blocks, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
                case_start_line = len(lines)  # Track where case body starts

                # FÁZE 3: Detect if/else patterns in case body BEFORE rendering
                # FÁZE 3.2 FIX: Pass func_loops to avoid misdetecting loop headers
                # BUG FIX #4: Build stop blocks from other cases to prevent if/else from crossing case boundaries
                case_stop_blocks = set()
                for other_case in switch.cases:
                    if other_case.value != case.value:
                        case_stop_blocks.update(other_case.body_blocks)
                if switch.default_body_blocks:
                    case_stop_blocks.update(switch.default_body_blocks)
                if switch.exit_block:
                    case_stop_blocks.add(switch.exit_block)

                # NEW FIX: Detect compound conditions FIRST (highest priority)
                # Then detect early returns, but skip blocks that are part of compound patterns
                compound_blocks = set()  # Blocks involved in compound conditions

                for body_block_id in case_body_sorted:
                    if body_block_id not in block_to_if:
                        temp_visited = set()
                        # Try compound detection first
                        if_pattern = _detect_if_else_pattern(cfg, body_block_id, start_to_block, resolver, temp_visited, func_loops, context_stop_blocks=case_stop_blocks, ssa_func=ssa_func, formatter=formatter)
                        if if_pattern and hasattr(if_pattern, 'compound'):
                            # Compound pattern detected - mark all involved blocks
                            compound_blocks.update(if_pattern.compound.involved_blocks)
                            block_to_if[body_block_id] = if_pattern

                # FÁZE 1.3: Detect early return/break patterns AFTER compound detection
                # Skip blocks that are part of compound patterns
                early_returns: Dict[int, tuple] = {}
                for body_block_id in case_body_sorted:
                    if body_block_id not in compound_blocks:
                        early_ret = _detect_early_return_pattern(cfg, body_block_id, start_to_block, resolver, switch.exit_block)
                        if early_ret:
                            early_returns[body_block_id] = early_ret

                # Now detect regular if/else patterns (not compound, not early return)
                for body_block_id in case_body_sorted:
                    if body_block_id not in block_to_if and body_block_id not in early_returns:
                        temp_visited = set()
                        # Regular if/else detection (compound already done above)
                        if_pattern = _detect_if_else_pattern(cfg, body_block_id, start_to_block, resolver, temp_visited, func_loops, context_stop_blocks=case_stop_blocks, ssa_func=ssa_func, formatter=formatter)
                        if if_pattern:
                            block_to_if[body_block_id] = if_pattern

                # FIX 3A: Use _render_blocks_with_loops to support loops in case bodies
                # FÁZE 1.3: Pass early_returns for early return/break detection
                case_lines = _render_blocks_with_loops(
                    case_body_sorted,
                    base_indent + "    ",
                    ssa_func,
                    formatter,
                    cfg,
                    func_loops,
                    start_to_block,
                    resolver,
                    block_to_if,
                    visited_ifs,
                    emitted_blocks,
                    global_map,
                    early_returns
                )
                lines.extend(case_lines)

                # Check if last line is a return statement - if so, don't add break
                has_return = False
                for i in range(len(lines) - 1, case_start_line - 1, -1):
                    line = lines[i].strip()
                    if line and not line.startswith("//"):  # Skip empty lines and comments
                        if line.startswith("return"):
                            has_return = True
                        break

                if case.has_break and not has_return:
                    lines.append(f"{base_indent}    break;")
            if switch.default_block is not None and switch.default_body_blocks:
                lines.append(f"{base_indent}default:")
                # Render all blocks in default body (sorted by address) with loop support
                default_body_sorted = sorted(switch.default_body_blocks, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)

                # FÁZE 3: Detect if/else patterns in default body BEFORE rendering
                # FÁZE 3.2 FIX: Pass func_loops to avoid misdetecting loop headers
                for body_block_id in default_body_sorted:
                    if body_block_id not in block_to_if:
                        temp_visited = set()
                        # FIX: Pass ssa_func and formatter for compound condition detection
                        if_pattern = _detect_if_else_pattern(cfg, body_block_id, start_to_block, resolver, temp_visited, func_loops, ssa_func=ssa_func, formatter=formatter)
                        if if_pattern:
                            block_to_if[body_block_id] = if_pattern

                # FIX 3A: Use _render_blocks_with_loops to support loops in default body
                default_lines = _render_blocks_with_loops(
                    default_body_sorted,
                    base_indent + "    ",
                    ssa_func,
                    formatter,
                    cfg,
                    func_loops,
                    start_to_block,
                    resolver,
                    block_to_if,
                    visited_ifs,
                    emitted_blocks,
                    global_map
                )
                lines.extend(default_lines)
            lines.append(f"{base_indent}}}")
            emitted_switches.add(block_id)

            # FIX 1A: Mark all switch blocks as emitted to prevent re-rendering
            emitted_blocks.update(switch.all_blocks)
            if switch.exit_block is not None:
                emitted_blocks.add(switch.exit_block)

            # FIX 3C: Skip next block if it's unreachable connector after switch
            if idx + 1 < len(func_blocks):
                next_addr, next_block_id, next_block = func_blocks[idx + 1]
                next_block_obj = cfg.blocks.get(next_block_id)
                next_ssa_block = ssa_blocks.get(next_block_id, [])

                # If next block is just a connector (no statements, only control flow)
                if next_block_obj and _is_control_flow_only(next_ssa_block, resolver):
                    # Check if it's jumping to already-emitted block
                    if next_block_obj.instructions:
                        last = next_block_obj.instructions[-1]
                        if resolver.is_jump(last.opcode):
                            target = start_to_block.get(last.arg1, -1)
                            if target in emitted_blocks:
                                # Skip this connector block
                                emitted_blocks.add(next_block_id)

            continue

        # Check if this is an if/else header
        if block_id in block_to_if and block_id == block_to_if[block_id].header_block:
            if_pattern = block_to_if[block_id]
            base_indent = "    " + "    " * len(active_loops)

            # Get condition from SSA
            cond_text = None
            ssa_block = ssa_blocks.get(block_id, [])
            block_obj = cfg.blocks[block_id]
            if block_obj.instructions:
                last_instr = block_obj.instructions[-1]
                mnemonic = resolver.get_mnemonic(last_instr.opcode)
                for ssa_inst in ssa_block:
                    if ssa_inst.address == last_instr.address and ssa_inst.inputs:
                        cond_value = ssa_inst.inputs[0]
                        # FIX 3: Pass IN_CONDITION context to avoid redundant parentheses
                        cond_expr = formatter.render_value(cond_value, context=ExpressionContext.IN_CONDITION)
                        # Only use SSA name if rendered as pure number
                        if cond_expr.lstrip('-').isdigit():
                            alias = cond_value.alias or cond_value.name
                            if alias and not alias.startswith("data_"):
                                cond_expr = alias

                        # FIX 3: Smart negation - only add parens if needed
                        if mnemonic == "JZ":
                            # JZ means "jump if zero" = jump if false, so negate condition
                            if is_simple_expression(cond_expr):
                                cond_text = f"!{cond_expr}"
                            else:
                                cond_text = f"!({cond_expr})"
                        elif mnemonic == "JNZ":
                            # JNZ means "jump if not zero" = jump if true, use as-is
                            cond_text = cond_expr
                        else:
                            cond_text = cond_expr
                        break
            if cond_text is None:
                cond_text = f"cond_{block_id}"

            # Render header block (without the conditional jump)
            if SHOW_BLOCK_COMMENTS: lines.append(f"{base_indent}// Block {block_id} @{block_obj.start}")
            # Format block but exclude last instruction (conditional jump)
            # FIX 3B: Disable recursion for header - pass None for recursive params
            header_lines = _format_block_lines(
                ssa_func, block_id, base_indent, formatter,
                None, None, None, None, None, None
            )
            # Remove last line if it's the conditional jump
            if header_lines and ("goto" in header_lines[-1] or "if (" in header_lines[-1]):
                header_lines = header_lines[:-1]
            lines.extend(header_lines)

            # Render if statement
            lines.append(f"{base_indent}if ({cond_text}) {{")

            # Render true branch
            true_body_sorted = sorted(if_pattern.true_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
            for body_block_id in true_body_sorted:
                body_block = cfg.blocks.get(body_block_id)
                if body_block:
                    # FIX 3C: Only add comment if block has actual statements
                    ssa_block = ssa_blocks.get(body_block_id, [])
                    if not _is_control_flow_only(ssa_block, resolver):
                        if SHOW_BLOCK_COMMENTS: lines.append(f"{base_indent}    // Block {body_block_id} @{body_block.start}")
                    # FIX 3B: Pass recursive params for nested if/else detection
                    lines.extend(_format_block_lines(
                        ssa_func, body_block_id, base_indent + "    ", formatter,
                        block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver
                    ))

            # Check if false branch is non-empty
            if if_pattern.false_body:
                lines.append(f"{base_indent}}} else {{")

                # Render false branch
                false_body_sorted = sorted(if_pattern.false_body, key=lambda bid: cfg.blocks[bid].start if bid in cfg.blocks else 9999999)
                for body_block_id in false_body_sorted:
                    body_block = cfg.blocks.get(body_block_id)
                    if body_block:
                        # FIX 3C: Only add comment if block has actual statements
                        ssa_block = ssa_blocks.get(body_block_id, [])
                        if not _is_control_flow_only(ssa_block, resolver):
                            if SHOW_BLOCK_COMMENTS: lines.append(f"{base_indent}    // Block {body_block_id} @{body_block.start}")
                        # FIX 3B: Pass recursive params for nested if/else detection
                        lines.extend(_format_block_lines(
                            ssa_func, body_block_id, base_indent + "    ", formatter,
                            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver
                        ))

            lines.append(f"{base_indent}}}")
            emitted_ifs.add(block_id)
            # Mark all blocks as emitted
            emitted_blocks.add(block_id)  # Header
            emitted_blocks.update(if_pattern.true_body)  # True branch
            emitted_blocks.update(if_pattern.false_body)  # False branch
            continue

        # Check if this block is a loop header we haven't opened yet
        header_loop = None
        for loop in func_loops:
            if loop.header == block_id and block_id not in emitted_loop_headers:
                header_loop = loop
                break

        if header_loop:
            emitted_loop_headers.add(block_id)  # Track by header ID, not loop object
            active_loops.append(header_loop)
            indent = "    " + "    " * (len(active_loops) - 1)
            lines.append(f"{indent}// Loop header - Block {block_id} @{addr}")

            # FIX 3A: Try to detect for-loop pattern
            for_info = _detect_for_loop(header_loop, cfg, ssa_func, formatter, resolver, start_to_block, global_map)
            if for_info:
                lines.append(f"{indent}for ({for_info.var} = {for_info.init}; {for_info.condition}; {for_info.increment}) {{")
            else:
                lines.append(f"{indent}while (true) {{  // loop body: blocks {sorted(header_loop.body)}")

        # Calculate current indentation based on active loops
        base_indent = "    " + "    " * len(active_loops)

        # FIX 3C: Only add comment if block has actual statements
        ssa_block = ssa_blocks.get(block_id, [])
        if not _is_control_flow_only(ssa_block, resolver):
            if SHOW_BLOCK_COMMENTS: lines.append(f"{base_indent}// Block {block_id} @{addr}")
        # FIX 3B: Pass recursive params for nested if/else detection
        lines.extend(_format_block_lines(
            ssa_func, block_id, base_indent, formatter,
            block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver
        ))

        if block.instructions:
            last_instr = block.instructions[-1]
            opcode = last_instr.opcode
            mnemonic = resolver.get_mnemonic(opcode)

            # Show control flow
            # NOTE: RET is now handled in expr.py, so we don't add extra return here
            if False and resolver.is_return(opcode):
                lines.append(f"{base_indent}return;")
            elif resolver.is_jump(opcode):
                target = last_instr.arg1
                target_block = start_to_block.get(target, -1)

                # FIX 1B: Skip goto if jumping into a switch that will be rendered next
                # This handles both direct header jumps AND jumps to first case block
                is_switch_header_jump = False
                if target_block in block_to_switch:
                    target_switch = block_to_switch[target_block]

                    # Check if the switch header will be rendered next
                    # (target might be header itself OR a case block within the switch)
                    if idx + 1 < len(func_blocks):
                        next_addr, next_block_id, next_block = func_blocks[idx + 1]

                        # If next block is the switch header, skip goto
                        if next_block_id == target_switch.header_block:
                            is_switch_header_jump = True

                # Check if this is a back edge (continue) or loop exit (break)
                is_back_edge = _is_back_edge_target(cfg, block_id, target_block, func_loops)
                containing_loop = _get_loop_for_block(block_id, func_loops)
                is_loop_exit = (containing_loop and
                               target_block not in containing_loop.body and
                               target_block in containing_loop.exits)

                if resolver.is_conditional_jump(opcode):
                    # Get condition from SSA
                    cond_text = None
                    ssa_block = ssa_blocks.get(block_id, [])
                    for ssa_inst in ssa_block:
                        if ssa_inst.address == last_instr.address and ssa_inst.inputs:
                            cond_value = ssa_inst.inputs[0]
                            # FIX 3: Pass IN_CONDITION context
                            cond_expr = formatter.render_value(cond_value, context=ExpressionContext.IN_CONDITION)
                            # Only use SSA name if rendered as pure number AND has meaningful alias
                            # Skip data_ aliases as they should be resolved to actual values
                            if cond_expr.lstrip('-').isdigit():
                                alias = cond_value.alias or cond_value.name
                                # Keep numeric value for data_ references (already resolved)
                                # Use alias only for local_/param_ variables
                                if alias and not alias.startswith("data_"):
                                    cond_expr = alias
                            # FIX 3: Smart negation
                            if mnemonic == "JZ":
                                if is_simple_expression(cond_expr):
                                    cond_text = f"!{cond_expr}"
                                else:
                                    cond_text = f"!({cond_expr})"
                            elif mnemonic == "JNZ":
                                cond_text = cond_expr
                            else:
                                cond_text = cond_expr
                            break
                    if cond_text is None:
                        cond_text = f"cond_{block_id}"

                    # FIX 1B: Skip rendering if jumping to switch header
                    if not is_switch_header_jump:
                        if is_back_edge:
                            lines.append(f"{base_indent}if ({cond_text}) continue;  // back to loop header @{target}")
                        elif is_loop_exit:
                            lines.append(f"{base_indent}if ({cond_text}) break;  // exit loop @{target}")
                        else:
                            lines.append(f"{base_indent}if ({cond_text}) goto block_{target_block}; // @{target}")
                else:
                    # Unconditional jump
                    # FIX 1B: Skip rendering if jumping to switch header
                    if not is_switch_header_jump:
                        # FIX 3C: Skip goto if target is already emitted (unreachable code)
                        if target_block not in emitted_blocks:
                            if is_back_edge:
                                lines.append(f"{base_indent}continue;  // back to loop header @{target}")
                            elif is_loop_exit:
                                lines.append(f"{base_indent}break;  // exit loop @{target}")
                            else:
                                lines.append(f"{base_indent}goto block_{target_block}; // @{target}")

    # Close any remaining active loops
    while active_loops:
        active_loops.pop()
        indent = "    " + "    " * len(active_loops)
        lines.append(f"{indent}}}")

    lines.append("}")
    return "\n".join(lines)
