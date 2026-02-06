"""
Hierarchical code emitter for structured blocks.

This module provides a code emitter that walks the hierarchical block
structure and generates C-like code. It handles all block types:
- BlockBasic: Emit original block's statements
- BlockList: Emit components in sequence
- BlockIf: Emit if-else structure
- BlockWhileDo/BlockDoWhile: Emit loop structure
- BlockSwitch: Emit switch-case structure
- BlockGoto: Emit goto statement
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, TYPE_CHECKING, Any
import logging

from ..blocks.hierarchy import (
    BlockType,
    EdgeType,
    StructuredBlock,
    BlockBasic,
    BlockList,
    BlockIf,
    BlockWhileDo,
    BlockDoWhile,
    BlockInfLoop,
    BlockCondition,
    BlockSwitch,
    BlockGoto,
    BlockGraph,
    SwitchCase,
)
from ..analysis.condition import render_condition, _find_condition_jump
from ..analysis.boolean_match import simplify_boolean_expression
from ....constants import get_known_constant_for_variable

if TYPE_CHECKING:
    from .....disasm import opcodes
    from ....ssa import SSAFunction
    from ..emit.expression_formatter import ExpressionFormatter

logger = logging.getLogger(__name__)


class HierarchicalCodeEmitter:
    """
    Emits C-like code from a hierarchical block structure.

    Walks the collapsed block tree and generates properly indented code
    for each structure type.
    """

    def __init__(
        self,
        graph: BlockGraph,
        ssa_func: "SSAFunction",
        formatter: "ExpressionFormatter",
        resolver: "opcodes.OpcodeResolver",
        global_map: Optional[Dict[int, str]] = None,
        start_to_block: Optional[Dict[int, int]] = None,
        func_loops: Optional[List] = None,
        func_block_ids: Optional[Set[int]] = None,
    ):
        self.graph = graph
        self.ssa_func = ssa_func
        self.formatter = formatter
        self.resolver = resolver
        self.global_map = global_map or {}
        self.start_to_block = start_to_block or {}
        self.cfg = ssa_func.cfg
        self.func_loops = func_loops or []
        self.func_block_ids = func_block_ids or set(self.cfg.blocks.keys())

        # Track emitted blocks to avoid duplication
        self.emitted_blocks: Set[int] = set()

        # For-loop increment suppression: variable names whose last assignment
        # should be filtered out of body blocks (set during for-loop emission)
        self._for_loop_skip_vars: Set[str] = set()

        # Label counter for goto targets
        self.label_counter = 0
        self.block_labels: Dict[int, str] = {}

    def emit(self, indent: str = "    ") -> List[str]:
        """
        Emit code for the root block structure.

        Args:
            indent: Base indentation

        Returns:
            List of code lines
        """
        # Initialize loop header map for loop detection during emit
        self._loop_header_map: Dict[int, object] = {}
        for loop in self.func_loops:
            self._loop_header_map[loop.header] = loop
        self._emitted_as_loop_body: Set[int] = set()

        if self.graph.root is None:
            return ["    // No root block"]

        return self._emit_block(self.graph.root, indent)

    def _collect_covered_blocks(self) -> Set[int]:
        """
        Collect all CFG block IDs that are covered by collapsed structures.

        This walks the structured block tree and collects all original_block_id
        values from BasicBlocks that are nested inside structures like switch
        cases. These blocks should NOT be emitted as separate labeled blocks.

        Returns:
            Set of CFG block IDs covered by structures
        """
        covered = set()

        def walk_block(block: StructuredBlock):
            """Recursively collect covered blocks from a structure."""
            if block is None:
                return

            # Add covered_blocks from the structure itself
            if block.covered_blocks:
                covered.update(block.covered_blocks)

            # Handle specific block types
            if isinstance(block, BlockBasic):
                if block.original_block_id >= 0:
                    covered.add(block.original_block_id)
            elif isinstance(block, BlockList):
                for comp in block.components:
                    walk_block(comp)
            elif isinstance(block, BlockIf):
                walk_block(block.condition_block)
                walk_block(block.true_block)
                walk_block(block.false_block)
            elif isinstance(block, BlockWhileDo):
                walk_block(block.condition_block)
                walk_block(block.body_block)
            elif isinstance(block, BlockDoWhile):
                walk_block(block.body_block)
                walk_block(block.condition_block)
            elif isinstance(block, BlockInfLoop):
                walk_block(block.body_block)
            elif isinstance(block, BlockCondition):
                walk_block(block.first_condition)
                walk_block(block.second_condition)
            elif isinstance(block, BlockSwitch):
                walk_block(block.header_block)
                for case in block.cases:
                    walk_block(case.body_block)
                if block.default_case:
                    walk_block(block.default_case.body_block)
            elif isinstance(block, BlockGoto):
                walk_block(block.wrapped_block)

        # Walk from root
        if self.graph.root is not None:
            walk_block(self.graph.root)

        # ALSO walk all blocks in graph.blocks (may include disconnected structures)
        # This catches blocks that got collapsed but aren't reachable from root.
        # IMPORTANT: Only walk blocks that are NOT uncollapsed top-level blocks.
        # Uncollapsed blocks should remain available for emission, not be marked
        # as covered. Only blocks that are children of collapsed structures
        # (e.g., switch case bodies) should be considered covered.
        uncollapsed_set = set(id(b) for b in self.graph.get_uncollapsed_blocks())
        for block in self.graph.blocks.values():
            if id(block) not in uncollapsed_set:
                walk_block(block)

        return covered

    def _compute_needed_labels(self) -> Set[int]:
        """
        Compute which CFG block IDs are actual goto targets.

        A block needs a label only if there's a BlockGoto pointing to it.
        Blocks that are merely uncollapsed but have no gotos targeting them
        should not be emitted as labeled blocks (they're orphaned).

        Returns:
            Set of CFG block IDs that need labels (are goto targets)
        """
        needed = set()

        def find_goto_targets(block: StructuredBlock):
            """Recursively find all goto targets in a structure."""
            if block is None:
                return

            if isinstance(block, BlockGoto):
                # This block has a goto - its target needs a label
                if block.goto_target is not None:
                    if isinstance(block.goto_target, BlockBasic):
                        needed.add(block.goto_target.original_block_id)
                    elif hasattr(block.goto_target, 'covered_blocks') and block.goto_target.covered_blocks:
                        # Target is a collapsed structure - add its entry block
                        needed.add(min(block.goto_target.covered_blocks))
                # Also walk the wrapped block
                find_goto_targets(block.wrapped_block)
            elif isinstance(block, BlockList):
                for comp in block.components:
                    find_goto_targets(comp)
            elif isinstance(block, BlockIf):
                find_goto_targets(block.condition_block)
                find_goto_targets(block.true_block)
                find_goto_targets(block.false_block)
            elif isinstance(block, BlockWhileDo):
                find_goto_targets(block.condition_block)
                find_goto_targets(block.body_block)
            elif isinstance(block, BlockDoWhile):
                find_goto_targets(block.body_block)
                find_goto_targets(block.condition_block)
            elif isinstance(block, BlockInfLoop):
                find_goto_targets(block.body_block)
            elif isinstance(block, BlockCondition):
                find_goto_targets(block.first_condition)
                find_goto_targets(block.second_condition)
            elif isinstance(block, BlockSwitch):
                find_goto_targets(block.header_block)
                for case in block.cases:
                    find_goto_targets(case.body_block)
                if block.default_case:
                    find_goto_targets(block.default_case.body_block)

        # Walk from root to find all gotos
        if self.graph.root is not None:
            find_goto_targets(self.graph.root)

        # Also check all blocks in graph (for disconnected gotos)
        for block in self.graph.blocks.values():
            find_goto_targets(block)

        return needed

    def emit_function(self, indent: str = "    ") -> List[str]:
        """
        Emit code for the entire function by walking all blocks.

        This method handles partially collapsed graphs where some blocks
        remain uncollapsed. It emits the root structure first, then any
        remaining uncollapsed blocks in address order.

        Args:
            indent: Base indentation

        Returns:
            List of code lines
        """
        lines = []

        # Build a map of loop headers to their natural loops
        self._loop_header_map: Dict[int, object] = {}
        for loop in self.func_loops:
            self._loop_header_map[loop.header] = loop

        # Track which blocks are emitted as part of a loop
        self._emitted_as_loop_body: Set[int] = set()

        # Collect all blocks covered by the collapsed structure (switch cases, etc.)
        # These should NOT be emitted as separate labeled blocks.
        # IMPORTANT: Compute this BEFORE any emission pass so that both the
        # uncollapsed-block loop and the final CFG-block loop can use it to
        # prevent double-emission and stray labeled blocks.
        covered_by_structure = self._collect_covered_blocks()

        # Compute which blocks are actual goto targets (need labels)
        # Orphaned blocks without gotos targeting them should not be emitted
        needed_labels = self._compute_needed_labels()

        # First, emit the root structure
        if self.graph.root is not None:
            lines.extend(self._emit_block(self.graph.root, indent))

        # Dead code elimination: check if the root structure ends with a return.
        # If so, subsequent unlabeled blocks are unreachable dead code.
        _root_ends_with_return = False
        for _rl in reversed(lines):
            _stripped = _rl.strip()
            if not _stripped or _stripped.startswith("//"):
                continue
            if _stripped == "return;" or _stripped.startswith("return "):
                _root_ends_with_return = True
            break

        # LOOP RESCUE PASS: Detect loops whose headers were emitted during
        # root emission but whose body blocks were NOT emitted. This happens
        # when the collapse engine doesn't fully collapse a loop into a
        # BlockWhileDo/BlockDoWhile, so the header gets emitted as a plain
        # BlockBasic but the body blocks are orphaned.
        for loop in self.func_loops:
            # Dead code elimination: skip loop rescue if root ends with return
            if _root_ends_with_return:
                break
            header_emitted = loop.header in self.emitted_blocks
            if not header_emitted:
                continue
            # Check if any body block (excluding header) was emitted
            body_without_header = loop.body - {loop.header}
            body_emitted = any(
                bid in self.emitted_blocks or bid in self._emitted_as_loop_body
                for bid in body_without_header
            )
            if body_emitted:
                continue  # Body was already emitted, no rescue needed
            # Check that body blocks actually exist and aren't covered by structures
            body_available = body_without_header - covered_by_structure
            if not body_available:
                continue
            # Rescue: emit this loop's body via _try_emit_natural_loop
            # We need to un-mark the header first so it can be re-processed
            self.emitted_blocks.discard(loop.header)
            loop_lines = self._try_emit_natural_loop(loop, indent)
            if loop_lines is not None:
                lines.extend(loop_lines)
            else:
                # Couldn't detect loop pattern - re-mark header and emit body blocks directly
                self.emitted_blocks.add(loop.header)
                # Emit body blocks as flat code inside a while(1) wrapper
                body_sorted = sorted(
                    body_available,
                    key=lambda bid: self.cfg.blocks[bid].start if bid in self.cfg.blocks else 9999999
                )
                if body_sorted:
                    lines.append(f"{indent}/* loop body (rescue) */")
                    for body_id in body_sorted:
                        if body_id not in self.emitted_blocks:
                            body_lines = self._emit_basic_by_id(body_id, indent)
                            lines.extend(body_lines)
                            self._emitted_as_loop_body.add(body_id)

            # Then, emit any remaining uncollapsed blocks in address order
        uncollapsed = self.graph.get_uncollapsed_blocks()

        # Filter out root and already emitted blocks
        remaining = []
        for block in uncollapsed:
            if block == self.graph.root:
                continue
            if isinstance(block, BlockBasic):
                if block.original_block_id in self.emitted_blocks:
                    continue
                if block.original_block_id in self._emitted_as_loop_body:
                    continue
                # Skip blocks covered by collapsed structures
                if block.original_block_id in covered_by_structure:
                    continue
            else:
                # For structured blocks (BlockList, BlockIf, etc.), check if
                # all their covered_blocks are already emitted or covered.
                # This prevents duplicate emission of blocks that were rendered
                # inside switch case bodies or other structures.
                if hasattr(block, 'covered_blocks') and block.covered_blocks:
                    all_covered = all(
                        bid in self.emitted_blocks
                        or bid in self._emitted_as_loop_body
                        or bid in covered_by_structure
                        for bid in block.covered_blocks
                    )
                    if all_covered:
                        continue
            remaining.append(block)

        # Sort by original block address
        def get_block_addr(block):
            if isinstance(block, BlockBasic):
                cfg_block = self.cfg.blocks.get(block.original_block_id)
                if cfg_block:
                    return cfg_block.start
            return 9999999

        remaining.sort(key=get_block_addr)

        # Emit remaining blocks - check for loop headers first
        for block in remaining:
            # Dead code elimination: skip remaining uncollapsed blocks
            # if root ends with return and block has no goto label
            if _root_ends_with_return:
                if isinstance(block, BlockBasic) and block.original_block_id not in needed_labels:
                    continue

            if isinstance(block, BlockBasic):
                block_id = block.original_block_id

                # Skip if already emitted
                if block_id in self.emitted_blocks or block_id in self._emitted_as_loop_body:
                    continue

                # Check if this is a loop header
                if block_id in self._loop_header_map:
                    loop = self._loop_header_map[block_id]
                    loop_lines = self._try_emit_natural_loop(loop, indent)
                    if loop_lines is not None:
                        lines.extend(loop_lines)
                        continue

                # Not a loop - emit as labeled block
                if block_id not in self.block_labels:
                    self.block_labels[block_id] = f"block_{block_id}"

                lines.append(f"{self.block_labels[block_id]}:")
                lines.extend(self._emit_basic(block, indent))

        # Finally, emit any CFG blocks that weren't reached through the graph
        # (e.g., blocks removed during switch collapse)
        # Only iterate through blocks that belong to this function
        func_blocks_sorted = sorted(
            [bid for bid in self.func_block_ids if bid in self.cfg.blocks],
            key=lambda bid: self.cfg.blocks[bid].start
        )

        for block_id in func_blocks_sorted:
            if block_id in self.emitted_blocks or block_id in self._emitted_as_loop_body:
                continue

            # PRIORITY: Check if this is a loop header FIRST, before covered_by_structure
            # filtering. Loop headers may be "covered" by the collapse engine but their
            # body blocks weren't properly emitted, so we need to detect and emit them here.
            # HOWEVER: Only rescue loops whose body blocks are NOT already covered by
            # structures (switch cases, etc.). If covered, they were already emitted.
            failed_headers = getattr(self, '_failed_loop_headers', set())
            if block_id in self._loop_header_map and block_id not in failed_headers:
                loop = self._loop_header_map[block_id]
                # Check if this loop's body blocks are already covered/emitted
                # by a parent structure (e.g., rendered inside a switch case body)
                body_without_header = loop.body - {loop.header}
                body_already_covered = body_without_header and all(
                    bid in self.emitted_blocks
                    or bid in self._emitted_as_loop_body
                    or bid in covered_by_structure
                    for bid in body_without_header
                )
                if not body_already_covered:
                    loop_lines = self._try_emit_natural_loop(loop, indent)
                    if loop_lines is not None:
                        lines.extend(loop_lines)
                        continue
                else:
                    # Pattern detection failed - mark so body blocks are emitted flat
                    if not hasattr(self, '_failed_loop_headers'):
                        self._failed_loop_headers = set()
                    self._failed_loop_headers = getattr(self, '_failed_loop_headers', set())
                    self._failed_loop_headers.add(block_id)
                    # Fall through to normal emission for this header block

            # Skip blocks covered by collapsed structures (e.g., switch case bodies)
            # BUT don't skip blocks that are part of loops with failed pattern detection -
            # these need to be emitted as flat statements to avoid losing code.
            if block_id in covered_by_structure:
                failed_headers_set = getattr(self, '_failed_loop_headers', set())
                is_in_failed_loop = False
                if failed_headers_set:
                    for loop in self.func_loops:
                        if loop.header in failed_headers_set and block_id in loop.body:
                            is_in_failed_loop = True
                            break
                if not is_in_failed_loop:
                    continue

            # Check if this block is part of a loop whose header was already emitted
            # as part of a successfully detected loop pattern.
            # This prevents duplicate emission when loop body blocks appear in func_blocks_sorted
            # after the loop has already been emitted via its header.
            skip_as_loop_body = False
            for loop in self.func_loops:
                if loop.header in self.emitted_blocks and block_id in loop.body:
                    # Only skip if the loop was SUCCESSFULLY emitted (not a failed pattern)
                    if loop.header not in failed_headers:
                        skip_as_loop_body = True
                        self._emitted_as_loop_body.add(block_id)
                        break
            if skip_as_loop_body:
                continue

            # Skip orphaned blocks that have no gotos targeting them AND no real content.
            # Blocks with actual statements should still be emitted even without goto targets,
            # as they may contain code that wasn't collapsed into structures.
            if block_id not in needed_labels:
                # Dead code elimination: if the function already ends with a return,
                # skip unlabeled (unreachable) blocks
                if _root_ends_with_return:
                    self.emitted_blocks.add(block_id)
                    continue
                # Check if block has actual statements (not just control flow)
                ssa_instrs = self.ssa_func.instructions.get(block_id, [])
                from ..utils.helpers import _is_control_flow_only
                if _is_control_flow_only(ssa_instrs, self.resolver):
                    # Truly empty - skip it
                    self.emitted_blocks.add(block_id)
                    continue
                # Has content - emit it even without goto target (will be unlabeled)

            # Emit block - only add label if gotos target it
            if block_id in needed_labels:
                if block_id not in self.block_labels:
                    self.block_labels[block_id] = f"block_{block_id}"
                lines.append(f"{self.block_labels[block_id]}:")
            lines.extend(self._emit_basic_by_id(block_id, indent))

        # Post-processing: Dead code elimination
        # Find the last return statement at brace depth 0 (function body level).
        # Returns inside nested blocks (if/else, switch, while) must NOT trigger
        # truncation — their enclosing closing braces are syntactically required.
        last_toplevel_return_idx = -1
        brace_depth = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            brace_depth += stripped.count('{') - stripped.count('}')
            if (stripped == "return;" or stripped.startswith("return ")) and brace_depth == 0:
                last_toplevel_return_idx = i
        if last_toplevel_return_idx >= 0 and last_toplevel_return_idx < len(lines) - 1:
            # Check if anything after the return is a labeled block (goto target)
            has_labeled = any(
                lines[j].strip().endswith(":")
                for j in range(last_toplevel_return_idx + 1, len(lines))
                if lines[j].strip()
            )
            if not has_labeled:
                lines = lines[:last_toplevel_return_idx + 1]

        return lines

    def _emit_basic_by_id(self, block_id: int, indent: str) -> List[str]:
        """Emit a basic block's statements by CFG block ID."""
        lines = []

        if block_id in self.emitted_blocks:
            return lines

        # NOTE: Loop detection removed from here to prevent duplicate emission.
        # Loop headers are detected and emitted in emit_function() which is the
        # single canonical code path for loop detection.

        self.emitted_blocks.add(block_id)

        cfg_block = self.cfg.blocks.get(block_id)
        if cfg_block is None:
            return [f"{indent}// Block {block_id} not found"]

        # Get statements for this block
        from ..emit.code_emitter import _render_block_statements

        block_lines = _render_block_statements(
            self.ssa_func,
            block_id,
            self.formatter,
            self.resolver,
            self.global_map,
        )

        for line in block_lines:
            lines.append(f"{indent}{line}")

        return lines

    def _try_emit_natural_loop(self, loop, indent: str) -> Optional[List[str]]:
        """
        Try to emit a natural loop as a for/while/do-while loop.

        This handles loops that weren't collapsed by the rules but can
        still be emitted as structured loops using pattern detection.
        """
        from ..patterns.loops import _detect_for_loop, _detect_while_loop, _detect_do_while_loop

        # Try for-loop detection first
        for_info = _detect_for_loop(
            loop,
            self.cfg,
            self.ssa_func,
            self.formatter,
            self.resolver,
            self.start_to_block,
            self.global_map
        )

        if for_info:
            return self._emit_natural_for_loop(loop, for_info, indent)

        # Try while-loop detection
        while_info = _detect_while_loop(
            loop,
            self.cfg,
            self.ssa_func,
            self.formatter,
            self.resolver,
            self.start_to_block,
            self.global_map
        )

        if while_info:
            return self._emit_natural_while_loop(loop, while_info, indent)

        # Try do-while detection
        do_while_info = _detect_do_while_loop(
            loop,
            self.cfg,
            self.ssa_func,
            self.formatter,
            self.resolver,
            self.start_to_block,
            self.global_map
        )

        if do_while_info:
            return self._emit_natural_do_while_loop(loop, do_while_info, indent)

        return None

    def _try_emit_nested_loop(self, block_id: int, indent: str, outer_loop) -> Optional[List[str]]:
        """
        Check if a body block is an inner loop header and emit it as a nested loop.

        When emitting the body of a structured loop, any body block that is itself
        a loop header must be emitted as a nested loop structure, not as flat statements.

        Returns emitted lines if successful, None if block is not a loop header or
        detection failed.
        """
        if block_id not in self._loop_header_map:
            return None

        inner_loop = self._loop_header_map[block_id]

        # Don't try to recurse on the same loop (header == outer header)
        if inner_loop.header == outer_loop.header:
            return None

        # Temporarily remove inner loop's blocks from emitted sets so
        # _try_emit_natural_loop can process them
        inner_blocks = set(inner_loop.body)
        removed_emitted = inner_blocks & self.emitted_blocks
        removed_loop_body = inner_blocks & self._emitted_as_loop_body
        self.emitted_blocks -= inner_blocks
        self._emitted_as_loop_body -= inner_blocks

        try:
            result = self._try_emit_natural_loop(inner_loop, indent)
            if result is not None:
                # Success - inner loop blocks stay marked as emitted
                # (they were re-added by the recursive call's pre-marking)
                return result
            else:
                # Detection failed - restore the marks so flat emission works
                self.emitted_blocks |= removed_emitted
                self._emitted_as_loop_body |= removed_loop_body
                return None
        except Exception:
            # On any error, restore marks
            self.emitted_blocks |= removed_emitted
            self._emitted_as_loop_body |= removed_loop_body
            return None

    def _emit_natural_for_loop(self, loop, for_info, indent: str) -> List[str]:
        """Emit a natural loop as a for loop."""
        lines = []

        # Mark header and all body blocks as emitted FIRST to prevent duplicates
        # This prevents other code paths from re-detecting this loop
        self._emitted_as_loop_body.add(loop.header)
        self.emitted_blocks.add(loop.header)
        for body_id in loop.body:
            self._emitted_as_loop_body.add(body_id)
            self.emitted_blocks.add(body_id)

        lines.append(f"{indent}for ({for_info.var} = {for_info.init}; "
                    f"{for_info.condition}; {for_info.increment}) {{")

        # Emit body blocks (excluding header)
        # Note: We already marked everything as emitted above, so we iterate
        # through body blocks directly without skipping
        body_blocks = sorted(
            [bid for bid in loop.body if bid != loop.header],
            key=lambda bid: self.cfg.blocks[bid].start if bid in self.cfg.blocks else 9999999
        )

        # Emit body blocks with control flow awareness
        body_set = set(loop.body)
        emitted_in_body = set()
        for body_id in body_blocks:
            if body_id in emitted_in_body:
                continue
            # Skip the increment block if it's a separate block
            # (typically the block that jumps back to header)
            is_back_edge_source = any(
                be.source == body_id and be.target == loop.header
                for be in loop.back_edges
            )
            if is_back_edge_source:
                # This block contains the increment - emit non-increment statements only
                body_lines = self._emit_body_block_without_increment(body_id, indent + "    ", for_info)
                lines.extend(body_lines)
                emitted_in_body.add(body_id)
            else:
                # Check if this body block is an inner loop header
                nested_lines = self._try_emit_nested_loop(body_id, indent + "    ", loop)
                if nested_lines is not None:
                    lines.extend(nested_lines)
                    # Mark all inner loop blocks as emitted in this body
                    inner_loop = self._loop_header_map[body_id]
                    for bid in inner_loop.body:
                        emitted_in_body.add(bid)
                    continue

                # Check if this block has a conditional branch to other body blocks
                cond_lines = self._try_emit_body_block_with_condition(
                    body_id, body_set, emitted_in_body, loop, for_info, indent + "    "
                )
                if cond_lines is not None:
                    lines.extend(cond_lines)
                else:
                    # Regular body block - emit directly
                    body_lines = self._emit_body_block_by_id(body_id, indent + "    ", force=True)
                    lines.extend(body_lines)
                    emitted_in_body.add(body_id)

        lines.append(f"{indent}}}")
        return lines

    def _emit_body_block_by_id(self, block_id: int, indent: str, force: bool = False) -> List[str]:
        """
        Emit a body block's statements by CFG block ID.

        Args:
            block_id: The CFG block ID to emit
            indent: The indentation string
            force: If True, emit even if block is in emitted_blocks (used for loop bodies
                   that were pre-marked to prevent duplicate detection, but still need content)
        """
        lines = []

        # Skip if already emitted, unless force=True (for loop bodies)
        if not force and block_id in self.emitted_blocks:
            return lines

        cfg_block = self.cfg.blocks.get(block_id)
        if cfg_block is None:
            return lines

        # Get statements for this block
        from ..emit.code_emitter import _render_block_statements

        block_lines = _render_block_statements(
            self.ssa_func,
            block_id,
            self.formatter,
            self.resolver,
            self.global_map,
        )

        for line in block_lines:
            lines.append(f"{indent}{line}")

        return lines

    def _emit_body_block_without_increment(self, block_id: int, indent: str, for_info) -> List[str]:
        """Emit a body block, filtering out the increment statement."""
        lines = []

        cfg_block = self.cfg.blocks.get(block_id)
        if cfg_block is None:
            return lines

        # Get statements for this block
        from ..emit.code_emitter import _render_block_statements

        block_lines = _render_block_statements(
            self.ssa_func,
            block_id,
            self.formatter,
            self.resolver,
            self.global_map,
        )

        # Filter out increment statement
        # Build comprehensive patterns that account for SSA variable renaming:
        # The for_info.var may differ from the rendered variable name in the body
        # (e.g., for_info.var="local_20" but body renders "obj = obj + 1")
        inc_patterns = set()
        # Patterns using the display variable name
        inc_patterns.add(f"{for_info.var}++")
        inc_patterns.add(f"{for_info.var}--")
        if for_info.increment:
            inc_patterns.add(for_info.increment)
        inc_patterns.add(f"{for_info.var} = {for_info.var} + 1")
        inc_patterns.add(f"{for_info.var} = ({for_info.var} + 1)")
        # Patterns using the init_var (original SSA variable name, may differ)
        if hasattr(for_info, 'init_var') and for_info.init_var and for_info.init_var != for_info.var:
            inc_patterns.add(f"{for_info.init_var}++")
            inc_patterns.add(f"{for_info.init_var}--")
            inc_patterns.add(f"{for_info.init_var} = {for_info.init_var} + 1")
            inc_patterns.add(f"{for_info.init_var} = ({for_info.init_var} + 1)")
            # Cross-name patterns: LHS uses raw name, RHS uses display name
            # e.g., "local_45 = i + 1" when init_var=local_45, var=i
            inc_patterns.add(f"{for_info.init_var} = {for_info.var} + 1")
            inc_patterns.add(f"{for_info.init_var} = ({for_info.var} + 1)")
            inc_patterns.add(f"{for_info.init_var} = {for_info.var} - 1")
            inc_patterns.add(f"{for_info.init_var} = ({for_info.var} - 1)")
        # Discard empty patterns
        inc_patterns.discard("")

        # Also build a regex to catch renamed increments like "obj = obj + 1"
        # where "obj" is the SSA-renamed form of the loop counter.
        # Since this method is ONLY called for back-edge source blocks (the
        # increment block), a self-referential assignment "X = X + 1" or "X++"
        # in this block is very likely the loop increment statement.
        import re
        _inc_re = re.compile(r'^(\w+)\s*=\s*\(?\s*\1\s*\+\s*1\.?0?f?\s*\)?;?$')
        _pp_re = re.compile(r'^(\w+)\+\+;?$')
        _dec_re = re.compile(r'^(\w+)\s*=\s*\(?\s*\1\s*-\s*1\.?0?f?\s*\)?;?$')
        _mm_re = re.compile(r'^(\w+)--;?$')

        for line in block_lines:
            stripped = line.strip().rstrip(';').strip()
            is_increment = any(pat in line for pat in inc_patterns)
            # Fallback: regex match for self-referential increment/decrement
            # patterns in the back-edge block. This catches cases where SSA
            # renaming changed the variable name (e.g., "obj = obj + 1" when
            # the for-clause says "local_20++").
            if not is_increment:
                m = _inc_re.match(stripped) or _pp_re.match(stripped) or _dec_re.match(stripped) or _mm_re.match(stripped)
                if m:
                    is_increment = True
            if not is_increment:
                lines.append(f"{indent}{line}")

        return lines

    def _try_emit_body_block_with_condition(
        self, block_id: int, body_set: set, emitted_in_body: set,
        loop, for_info, indent: str
    ) -> Optional[List[str]]:
        """
        Try to emit a body block that ends with a conditional branch as an if/else.

        If the block has a conditional jump and at least one target is inside the loop body,
        emit as if(...){...} [else {...}] instead of flat blocks.

        Returns lines if handled, None otherwise.
        """
        cfg_block = self.cfg.blocks.get(block_id)
        if cfg_block is None:
            return None

        # Check if block has exactly 2 successors (conditional branch)
        successors = list(cfg_block.successors)
        if len(successors) != 2:
            return None

        # Both successors should be in the loop body (or one is the loop header/exit)
        true_id, false_id = successors[0], successors[1]

        # At least one target must be in the body set and not yet emitted
        true_in_body = true_id in body_set and true_id != loop.header
        false_in_body = false_id in body_set and false_id != loop.header

        if not true_in_body and not false_in_body:
            return None

        # Extract the condition from this block
        cond_result = render_condition(
            self.ssa_func, block_id, self.formatter, self.cfg, self.resolver
        )
        condition_text = cond_result.text if cond_result else None
        if not condition_text or condition_text == "true":
            return None

        lines = []

        # Emit this block's statements first (excluding the branch)
        from ..emit.code_emitter import _render_block_statements
        block_lines = _render_block_statements(
            self.ssa_func, block_id, self.formatter, self.resolver, self.global_map
        )
        for line in block_lines:
            lines.append(f"{indent}{line}")
        emitted_in_body.add(block_id)

        # Determine which blocks go in if-body vs else-body
        # The "true" branch is taken when condition is true (JZ: false_id is the fall-through)
        # We need to check the actual jump instruction
        cond_jump = _find_condition_jump(self.cfg.blocks[block_id], self.resolver)
        if cond_jump:
            # JZ jumps to target when condition is ZERO (false)
            # So: JZ target → if(cond) { fall-through } else { target }
            jump_target = cond_jump.arg1 if hasattr(cond_jump, 'arg1') else None
            if jump_target is not None:
                # Find which successor corresponds to the jump target
                for sid in successors:
                    if sid in self.cfg.blocks and self.cfg.blocks[sid].start == jump_target:
                        false_id = sid
                        true_id = [s for s in successors if s != sid][0]
                        break

        # Collect blocks that belong to the true branch
        # (blocks between true_id and the merge point, within the loop body)
        true_blocks = self._collect_branch_blocks(true_id, false_id, body_set, loop, emitted_in_body)
        false_blocks = self._collect_branch_blocks(false_id, true_id, body_set, loop, emitted_in_body)

        # Emit if statement
        if true_blocks:
            lines.append(f"{indent}if ({condition_text}) {{")
            for bid in true_blocks:
                if bid not in emitted_in_body:
                    # Check for nested loop first
                    nested = self._try_emit_nested_loop(bid, indent + "    ", loop)
                    if nested is not None:
                        lines.extend(nested)
                        inner_loop = self._loop_header_map[bid]
                        for inner_bid in inner_loop.body:
                            emitted_in_body.add(inner_bid)
                        continue
                    is_back_edge = any(
                        be.source == bid and be.target == loop.header
                        for be in loop.back_edges
                    )
                    if is_back_edge and for_info:
                        bl = self._emit_body_block_without_increment(bid, indent + "    ", for_info)
                    else:
                        bl = self._emit_body_block_by_id(bid, indent + "    ", force=True)
                    lines.extend(bl)
                    emitted_in_body.add(bid)
            lines.append(f"{indent}}}")

            # Emit else block if it has unique blocks
            if false_blocks:
                # Check that false blocks aren't already covered
                unvisited_false = [b for b in false_blocks if b not in emitted_in_body]
                if unvisited_false:
                    lines[-1] = f"{indent}}} else {{"
                    for bid in unvisited_false:
                        # Check for nested loop first
                        nested = self._try_emit_nested_loop(bid, indent + "    ", loop)
                        if nested is not None:
                            lines.extend(nested)
                            inner_loop = self._loop_header_map[bid]
                            for inner_bid in inner_loop.body:
                                emitted_in_body.add(inner_bid)
                            continue
                        is_back_edge = any(
                            be.source == bid and be.target == loop.header
                            for be in loop.back_edges
                        )
                        if is_back_edge and for_info:
                            bl = self._emit_body_block_without_increment(bid, indent + "    ", for_info)
                        else:
                            bl = self._emit_body_block_by_id(bid, indent + "    ", force=True)
                        lines.extend(bl)
                        emitted_in_body.add(bid)
                    lines.append(f"{indent}}}")
        elif false_blocks:
            # Only false branch has blocks - negate condition
            neg_cond = simplify_boolean_expression(f"!({condition_text})")
            lines.append(f"{indent}if ({neg_cond}) {{")
            for bid in false_blocks:
                if bid not in emitted_in_body:
                    # Check for nested loop first
                    nested = self._try_emit_nested_loop(bid, indent + "    ", loop)
                    if nested is not None:
                        lines.extend(nested)
                        inner_loop = self._loop_header_map[bid]
                        for inner_bid in inner_loop.body:
                            emitted_in_body.add(inner_bid)
                        continue
                    bl = self._emit_body_block_by_id(bid, indent + "    ", force=True)
                    lines.extend(bl)
                    emitted_in_body.add(bid)
            lines.append(f"{indent}}}")

        return lines if lines else None

    def _collect_branch_blocks(
        self, start_id: int, other_branch_id: int, body_set: set, loop, emitted: set
    ) -> List[int]:
        """
        Collect blocks reachable from start_id within the loop body,
        stopping at the other branch, loop header, or already-emitted blocks.
        Returns sorted list of block IDs.
        """
        if start_id not in body_set or start_id == loop.header or start_id in emitted:
            return []

        collected = []
        visited = set()
        worklist = [start_id]

        while worklist:
            bid = worklist.pop(0)
            if bid in visited or bid == loop.header or bid == other_branch_id:
                continue
            if bid not in body_set:
                continue
            if bid in emitted:
                continue
            visited.add(bid)
            collected.append(bid)

            # Follow successors within the loop body
            cfg_block = self.cfg.blocks.get(bid)
            if cfg_block:
                for succ in cfg_block.successors:
                    if succ not in visited and succ in body_set and succ != loop.header:
                        worklist.append(succ)

        # Sort by address
        collected.sort(
            key=lambda bid: self.cfg.blocks[bid].start if bid in self.cfg.blocks else 9999999
        )
        return collected

    def _emit_natural_while_loop(self, loop, while_info, indent: str) -> List[str]:
        """Emit a natural loop as a while loop."""
        lines = []

        # Mark header and all body blocks as emitted FIRST to prevent duplicates
        self._emitted_as_loop_body.add(loop.header)
        self.emitted_blocks.add(loop.header)
        for body_id in loop.body:
            self._emitted_as_loop_body.add(body_id)
            self.emitted_blocks.add(body_id)

        lines.append(f"{indent}while ({while_info.condition}) {{")

        # Emit body blocks (excluding header which is the condition)
        body_blocks = sorted(
            [bid for bid in while_info.body_blocks if bid != loop.header],
            key=lambda bid: self.cfg.blocks[bid].start if bid in self.cfg.blocks else 9999999
        )

        for body_id in body_blocks:
            # Check if this body block is an inner loop header
            nested_lines = self._try_emit_nested_loop(body_id, indent + "    ", loop)
            if nested_lines is not None:
                lines.extend(nested_lines)
                continue
            # Emit body block by ID, force=True because pre-marked as emitted
            body_lines = self._emit_body_block_by_id(body_id, indent + "    ", force=True)
            lines.extend(body_lines)

        lines.append(f"{indent}}}")
        return lines

    def _emit_natural_do_while_loop(self, loop, do_while_info, indent: str) -> List[str]:
        """Emit a natural loop as a do-while loop."""
        lines = []

        # Mark header and all body blocks as emitted FIRST to prevent duplicates
        for body_id in loop.body:
            self._emitted_as_loop_body.add(body_id)
            self.emitted_blocks.add(body_id)

        lines.append(f"{indent}do {{")

        # Emit body blocks (excluding condition block at the end)
        body_blocks = sorted(
            [bid for bid in do_while_info.body_blocks if bid != do_while_info.condition_block],
            key=lambda bid: self.cfg.blocks[bid].start if bid in self.cfg.blocks else 9999999
        )

        for body_id in body_blocks:
            # Check if this body block is an inner loop header
            nested_lines = self._try_emit_nested_loop(body_id, indent + "    ", loop)
            if nested_lines is not None:
                lines.extend(nested_lines)
                continue
            # Emit body block by ID, force=True because pre-marked as emitted
            body_lines = self._emit_body_block_by_id(body_id, indent + "    ", force=True)
            lines.extend(body_lines)

        lines.append(f"{indent}}} while ({do_while_info.condition});")
        return lines

    def _emit_block(self, block: StructuredBlock, indent: str) -> List[str]:
        """Dispatch to appropriate emitter based on block type."""
        if isinstance(block, BlockList):
            return self._emit_list(block, indent)
        elif isinstance(block, BlockIf):
            return self._emit_if(block, indent)
        elif isinstance(block, BlockWhileDo):
            return self._emit_while_do(block, indent)
        elif isinstance(block, BlockDoWhile):
            return self._emit_do_while(block, indent)
        elif isinstance(block, BlockInfLoop):
            return self._emit_inf_loop(block, indent)
        elif isinstance(block, BlockCondition):
            return self._emit_condition(block, indent)
        elif isinstance(block, BlockSwitch):
            return self._emit_switch(block, indent)
        elif isinstance(block, BlockGoto):
            return self._emit_goto(block, indent)
        elif isinstance(block, BlockBasic):
            return self._emit_basic(block, indent)
        else:
            return [f"{indent}// Unknown block type: {block.block_type}"]

    def _emit_basic(self, block: BlockBasic, indent: str) -> List[str]:
        """Emit a basic block's statements."""
        lines = []
        block_id = block.original_block_id

        if block_id in self.emitted_blocks:
            return lines

        # If this is a loop header with failed pattern detection, try to emit
        # the entire loop structure as flat statements including body blocks.
        failed_headers = getattr(self, '_failed_loop_headers', set())
        if block_id in self._loop_header_map and block_id not in failed_headers:
            # This block is a loop header that hasn't failed yet - attempt
            # pattern detection and structured emission
            loop = self._loop_header_map[block_id]
            loop_lines = self._try_emit_natural_loop(loop, indent)
            if loop_lines is not None:
                return loop_lines
            # Pattern detection failed - mark as failed and fall through to flat emission
            if not hasattr(self, '_failed_loop_headers'):
                self._failed_loop_headers = set()
            self._failed_loop_headers.add(block_id)

        self.emitted_blocks.add(block_id)

        cfg_block = self.cfg.blocks.get(block_id)
        if cfg_block is None:
            return [f"{indent}// Block {block_id} not found"]

        # Get statements for this block
        from ..emit.code_emitter import _render_block_statements

        block_lines = _render_block_statements(
            self.ssa_func,
            block_id,
            self.formatter,
            self.resolver,
            self.global_map,
        )

        # Filter out for-loop increment assignments from body blocks
        if self._for_loop_skip_vars:
            filtered = []
            for line in block_lines:
                stripped = line.strip().rstrip(';')
                skip = False
                for skip_var in self._for_loop_skip_vars:
                    if (stripped.startswith(f"{skip_var} =") or
                        stripped == f"{skip_var}++" or stripped == f"{skip_var}--" or
                        stripped == f"++{skip_var}" or stripped == f"--{skip_var}"):
                        skip = True
                        break
                if not skip:
                    filtered.append(line)
            block_lines = filtered

        for line in block_lines:
            lines.append(f"{indent}{line}")

        return lines

    def _emit_list(self, block: BlockList, indent: str) -> List[str]:
        """Emit a sequential list of blocks."""
        lines = []

        for component in block.components:
            component_lines = self._emit_block(component, indent)
            lines.extend(component_lines)
            # Dead code elimination: stop emitting after unconditional return
            for cl in reversed(component_lines):
                stripped = cl.strip()
                if not stripped or stripped.startswith("//"):
                    continue
                if stripped == "return;" or stripped.startswith("return "):
                    return lines
                break

        return lines

    def _is_empty_branch(self, branch: Optional[StructuredBlock]) -> bool:
        """Check if a branch block would produce zero visible statements.

        Used to detect boolean PHI diamonds where both branches only contain
        GCP constant loads consumed by a PHI node (no user-visible code).
        """
        if branch is None:
            return True
        if isinstance(branch, BlockBasic):
            block_id = branch.original_block_id
            if block_id < 0:
                return True
            from ..emit.code_emitter import _render_block_statements
            stmts = _render_block_statements(
                self.ssa_func, block_id, self.formatter, self.resolver, self.global_map
            )
            return len(stmts) == 0
        if isinstance(branch, BlockList):
            # A BlockList is empty if all its components are empty
            return all(self._is_empty_branch(comp) for comp in branch.components)
        return False

    def _emit_if(self, block: BlockIf, indent: str) -> List[str]:
        """Emit an if-then-else structure."""
        lines = []

        # Skip empty if/else diamonds (boolean PHI patterns).
        # When both branches produce zero statements (only GCP constants for PHI + JMP),
        # the diamond was consumed by _detect_boolean_phi() in the expression renderer.
        if self._is_empty_branch(block.true_block) and self._is_empty_branch(block.false_block):
            # Mark all covered blocks as emitted so they don't appear elsewhere
            if block.true_block is not None:
                for bid in block.true_block.covered_blocks:
                    self.emitted_blocks.add(bid)
            if block.false_block is not None:
                for bid in block.false_block.covered_blocks:
                    self.emitted_blocks.add(bid)
            # Still emit condition block statements (LCP etc.) if any
            if block.condition_block is not None:
                for bid in block.condition_block.covered_blocks:
                    self.emitted_blocks.add(bid)
                cond_lines = self._emit_block(block.condition_block, indent)
                if cond_lines:
                    # Filter out the if/goto line that _emit_block may produce
                    filtered = [l for l in cond_lines
                                if not l.lstrip().startswith("if (") and not l.lstrip().startswith("if(")
                                and not l.lstrip().startswith("goto ")]
                    lines.extend(filtered)
            return lines

        # Get condition
        condition = block.condition_expr
        if condition is None and block.condition_block is not None:
            # Check if condition_block is a combined condition (AND/OR)
            if isinstance(block.condition_block, BlockCondition):
                condition = self._extract_combined_condition(block.condition_block)
            else:
                # Check if condition_block is a BlockList containing a BlockCondition
                # This happens when the collapse engine partially collapses an AND/OR
                # chain but wraps it in a BlockList with other statement blocks.
                embedded_cond = self._find_embedded_condition(block.condition_block)
                if embedded_cond is not None:
                    condition = self._extract_combined_condition(embedded_cond)
                else:
                    # Determine negation based on condition_negated flag.
                    # When condition_negated=True, branches were swapped, so emit
                    # condition without negation (the swap handles semantic negation).
                    # When condition_negated=False, let render_condition auto-detect.
                    if block.condition_negated:
                        condition = self._extract_condition(block.condition_block, negate=False)
                    else:
                        condition = self._extract_condition(block.condition_block, negate=None)

        if condition is None:
            condition = "/* condition */"

        # Emit condition block statements (before the if)
        if block.condition_block is not None:
            cond_lines = self._emit_block(block.condition_block, indent)
            if cond_lines:
                # _emit_block for basic blocks doesn't emit jumps, so keep statements.
                last_line = cond_lines[-1].lstrip()
                if last_line.startswith("if (") or last_line.startswith("if(") or last_line.startswith("goto "):
                    cond_lines = cond_lines[:-1]
                lines.extend(cond_lines)

        # Emit if header
        lines.append(f"{indent}if ({condition}) {{")

        # Emit true branch
        if block.true_block is not None:
            lines.extend(self._emit_block(block.true_block, indent + "    "))

        # Emit else branch if present
        if block.has_else() and block.false_block is not None:
            lines.append(f"{indent}}} else {{")
            lines.extend(self._emit_block(block.false_block, indent + "    "))

        lines.append(f"{indent}}}")

        return lines

    def _emit_while_do(self, block: BlockWhileDo, indent: str) -> List[str]:
        """Emit a while loop structure."""
        lines = []

        # Get condition
        condition = block.condition_expr
        if condition is None and block.condition_block is not None:
            if isinstance(block.condition_block, BlockCondition):
                condition = self._extract_combined_condition(block.condition_block)
            else:
                embedded_cond = self._find_embedded_condition(block.condition_block)
                if embedded_cond is not None:
                    condition = self._extract_combined_condition(embedded_cond)
                else:
                    condition = self._extract_condition(block.condition_block)

        if condition is None:
            condition = "/* condition */"

        # Check if this is a for loop (already detected by collapse rules)
        skip_var = None
        if block.is_for_loop:
            init = block.for_init or ""
            incr = block.for_increment or ""
            lines.append(f"{indent}for ({init}; {condition}; {incr}) {{")
            # Extract loop variable from init (e.g., "local_10 = 0" -> "local_10")
            if "=" in init:
                skip_var = init.split("=")[0].strip()
        else:
            # Try to detect for-loop pattern at emit time (matching flat pattern mode)
            for_info = self._try_detect_for_loop(block)
            if for_info:
                lines.append(f"{indent}for ({for_info.var} = {for_info.init}; "
                           f"{for_info.condition}; {for_info.increment}) {{")
                skip_var = for_info.init_var or for_info.var
                # Emit body with increment suppression
                if block.body_block is not None:
                    self._for_loop_skip_vars.add(skip_var)
                    lines.extend(self._emit_block(block.body_block, indent + "    "))
                    self._for_loop_skip_vars.discard(skip_var)
                lines.append(f"{indent}}}")
                return lines

            # Fallback: emit as while loop
            lines.append(f"{indent}while ({condition}) {{")

        # Emit body (with increment suppression for for-loops)
        if block.body_block is not None:
            if skip_var:
                self._for_loop_skip_vars.add(skip_var)
            lines.extend(self._emit_block(block.body_block, indent + "    "))
            if skip_var:
                self._for_loop_skip_vars.discard(skip_var)

        lines.append(f"{indent}}}")

        return lines

    def _try_detect_for_loop(self, block: BlockWhileDo):
        """
        Try to detect for-loop pattern at emit time.

        This bridges the gap between collapse rules (which only identify while
        structure) and flat pattern detection (which identifies for loops).
        """
        # Get the header block ID from the condition block
        if not isinstance(block.condition_block, BlockBasic):
            return None

        header_id = block.condition_block.original_block_id

        # Find the NaturalLoop for this header
        matching_loop = None
        for loop in self.func_loops:
            if loop.header == header_id:
                matching_loop = loop
                break

        if matching_loop is None:
            return None

        # Use the existing for-loop detection logic
        from ..patterns.loops import _detect_for_loop
        for_info = _detect_for_loop(
            matching_loop,
            self.cfg,
            self.ssa_func,
            self.formatter,
            self.resolver,
            self.start_to_block,
            self.global_map
        )

        return for_info

    def _emit_do_while(self, block: BlockDoWhile, indent: str) -> List[str]:
        """Emit a do-while loop structure."""
        lines = []

        # Get condition
        condition = block.condition_expr
        if condition is None and block.condition_block is not None:
            if isinstance(block.condition_block, BlockCondition):
                condition = self._extract_combined_condition(block.condition_block)
            else:
                embedded_cond = self._find_embedded_condition(block.condition_block)
                if embedded_cond is not None:
                    condition = self._extract_combined_condition(embedded_cond)
                else:
                    condition = self._extract_condition(block.condition_block)

        if condition is None:
            condition = "/* condition */"

        lines.append(f"{indent}do {{")

        # Emit body
        if block.body_block is not None:
            lines.extend(self._emit_block(block.body_block, indent + "    "))

        lines.append(f"{indent}}} while ({condition});")

        return lines

    def _emit_inf_loop(self, block: BlockInfLoop, indent: str) -> List[str]:
        """Emit an infinite loop structure."""
        lines = []

        lines.append(f"{indent}while (1) {{")

        # Emit body
        if block.body_block is not None:
            lines.extend(self._emit_block(block.body_block, indent + "    "))

        lines.append(f"{indent}}}")

        return lines

    def _emit_condition(self, block: BlockCondition, indent: str) -> List[str]:
        """
        Emit a combined boolean condition (AND/OR).

        BlockCondition represents a short-circuit boolean expression like:
            cond1 || cond2  or  cond1 && cond2

        The actual condition rendering happens in the parent structure
        (BlockIf, BlockWhileDo, etc.) that uses this condition. Here we
        just emit any statements from the condition blocks themselves.
        """
        lines = []

        # Emit statements from first condition block
        if block.first_condition is not None:
            lines.extend(self._emit_block(block.first_condition, indent))

        # Emit statements from second condition block
        if block.second_condition is not None:
            lines.extend(self._emit_block(block.second_condition, indent))

        return lines

    def _extract_combined_condition(self, block: BlockCondition) -> str:
        """
        Extract the combined condition expression from a BlockCondition.

        Returns a string like "cond1 || cond2" or "cond1 && cond2".
        """
        operator = " || " if block.is_or else " && "

        # Sub-conditions in combined expressions must be rendered as positive
        # (raw tested values) with negate=False. The JZ auto-negation (negate=None)
        # is only correct for standalone if-statements, not combined booleans.
        # The AND/OR structure itself encodes the short-circuit branching semantics.

        # Get condition from first block
        cond1 = None
        if block.first_condition is not None:
            cond1 = self._extract_condition(block.first_condition, negate=False)

        # Get condition from second block
        cond2 = None
        if block.second_condition is not None:
            if isinstance(block.second_condition, BlockCondition):
                # Recursive combined condition
                cond2 = self._extract_combined_condition(block.second_condition)
            else:
                cond2 = self._extract_condition(block.second_condition, negate=False)

        if cond1 and cond2:
            combined = f"({cond1}{operator}{cond2})"
        elif cond1:
            combined = cond1
        elif cond2:
            combined = cond2
        else:
            combined = "true"

        return simplify_boolean_expression(combined)

    def _find_embedded_condition(self, block: StructuredBlock) -> Optional[BlockCondition]:
        """Find a BlockCondition embedded inside a BlockList or other container.

        When the collapse engine partially collapses an AND/OR chain, the result
        may be wrapped in a BlockList alongside statement blocks. This method
        searches for the BlockCondition component.
        """
        if isinstance(block, BlockCondition):
            return block
        if isinstance(block, BlockList):
            for comp in block.components:
                if isinstance(comp, BlockCondition):
                    return comp
                # Recurse into nested BlockLists
                if isinstance(comp, BlockList):
                    found = self._find_embedded_condition(comp)
                    if found is not None:
                        return found
        return None

    def _try_extract_and_or_chain(self, block: StructuredBlock, negate: Optional[bool]) -> Optional[str]:
        """Extract compound AND/OR condition by walking the CFG.

        When an AND/OR chain isn't collapsed into a BlockCondition (e.g., the
        condition_block is a non-basic structured block), walk the underlying
        CFG blocks to detect short-circuit chains:
          - AND: consecutive JZ blocks jumping to the same false target
          - OR:  consecutive JNZ blocks jumping to the same true target
        """
        cfg_ids = sorted(block.covered_blocks) if hasattr(block, 'covered_blocks') else []
        if not cfg_ids:
            return None

        # Find the first CFG block that has a conditional jump
        start_cfg_id = None
        for bid in cfg_ids:
            cfg_block = self.cfg.blocks.get(bid)
            if cfg_block and _find_condition_jump(cfg_block, self.resolver):
                start_cfg_id = bid
                break
        if start_cfg_id is None:
            return None

        # Walk forward through condition chain
        chain = []  # List of (block_id, mnemonic, jump_target)
        current = start_cfg_id
        shared_target = None
        visited = set()

        while current is not None and current not in visited and len(chain) < 10:
            visited.add(current)
            cfg_block = self.cfg.blocks.get(current)
            if cfg_block is None:
                break
            jump = _find_condition_jump(cfg_block, self.resolver)
            if jump is None:
                break

            mnemonic = self.resolver.get_mnemonic(jump.opcode)
            jump_target = jump.arg1

            chain.append((current, mnemonic, jump_target))

            if shared_target is None:
                shared_target = jump_target
            elif jump_target != shared_target:
                # Chain broken — different targets
                break

            # Follow fallthrough to next condition block
            fallthrough_id = None
            for succ_id in cfg_block.successors:
                if succ_id != jump_target and succ_id in cfg_ids:
                    fallthrough_id = succ_id
                    break
            current = fallthrough_id

        if len(chain) < 2:
            return None

        # Render each condition with negate=False (raw tested value)
        # The AND/OR structure itself encodes the short-circuit semantics
        conditions = []
        for bid, mnemonic, _ in chain:
            cond = render_condition(
                self.ssa_func, bid, self.formatter, self.cfg,
                self.resolver, negate=False
            )
            if cond and cond.text and cond.text != "true":
                conditions.append(cond.text)

        if len(conditions) < 2:
            return None

        # JZ chain = AND (all jump to false target when condition is false)
        # JNZ chain = OR (all jump to true target when condition is true)
        is_and = chain[0][1] == "JZ"
        operator = " && " if is_and else " || "
        combined = "(" + operator.join(conditions) + ")"

        # Apply negation if branches were swapped
        if negate:
            combined = f"!{combined}"

        return simplify_boolean_expression(combined)

    def _has_structured_children(self, block: StructuredBlock) -> bool:
        """Check if a block or any of its children is a non-basic structured block (switch, loop, etc.)."""
        if isinstance(block, (BlockSwitch, BlockWhileDo, BlockDoWhile)):
            return True
        if isinstance(block, BlockList):
            for child in block.components:
                if self._has_structured_children(child):
                    return True
        if isinstance(block, BlockIf):
            if block.true_block and self._has_structured_children(block.true_block):
                return True
            if block.false_block and self._has_structured_children(block.false_block):
                return True
        return False

    def _emit_switch(self, block: BlockSwitch, indent: str) -> List[str]:
        """Emit a switch-case structure."""
        lines = []

        test_var = block.test_var or "/* var */"

        # Emit header block statements if present
        if block.header_block is not None:
            header_lines = self._emit_block(block.header_block, indent)
            lines.extend(header_lines)

        # Mark switch header/dispatch blocks as emitted to prevent stray labels later.
        all_case_ids: Set[int] = set()
        for case in block.cases:
            if case.body_block_ids:
                all_case_ids.update(case.body_block_ids)
        if block.default_case and block.default_case.body_block_ids:
            all_case_ids.update(block.default_case.body_block_ids)

        # Heuristic: switch exit block(s) are successors outside all case bodies
        exit_ids: Set[int] = set()
        for bid in all_case_ids:
            cfg_block = self.cfg.blocks.get(bid)
            if not cfg_block:
                continue
            for succ in getattr(cfg_block, "successors", []):
                if succ not in all_case_ids:
                    exit_ids.add(succ)
        header_only = set(block.covered_blocks or []) - all_case_ids
        if header_only:
            # Don't suppress blocks that end in return (likely switch exit).
            filtered_header = set()
            for bid in header_only:
                cfg_block = self.cfg.blocks.get(bid)
                if cfg_block and cfg_block.instructions:
                    last_instr = cfg_block.instructions[-1]
                    if self.resolver.is_return(last_instr.opcode):
                        continue
                filtered_header.add(bid)
            if filtered_header:
                self.emitted_blocks.update(filtered_header)

        lines.append(f"{indent}switch ({test_var}) {{")

        # Emit cases
        for case in block.cases:
            case_value = case.value
            if isinstance(case_value, int) and block.test_var:
                const_name = get_known_constant_for_variable(block.test_var, case_value)
                if const_name:
                    case_value = const_name
            lines.append(f"{indent}case {case_value}:")

            # If this case falls through to another case, skip body and break
            if case.fall_through_to is not None:
                continue

            # Prefer structured body_block when it contains nested switches or loops;
            # fall back to flat-mode rendering for case bodies with if/else structure.
            if case.body_block is not None and self._has_structured_children(case.body_block):
                lines.extend(self._emit_block(case.body_block, indent + "    "))
                # Emit any body blocks NOT covered by the structured body_block
                if case.body_block_ids:
                    covered = getattr(case.body_block, 'covered_blocks', None) or set()
                    uncovered = sorted(
                        set(case.body_block_ids) - covered - set(exit_ids) - self.emitted_blocks,
                        key=lambda bid: self.cfg.blocks[bid].start if bid in self.cfg.blocks else 9999999
                    )
                    if uncovered:
                        # Build stop blocks: other cases + exit + already-covered blocks
                        case_stop_blocks: Set[int] = set(covered)
                        for other_case in block.cases:
                            if other_case is not case and other_case.body_block_ids:
                                case_stop_blocks.update(other_case.body_block_ids)
                        if block.default_case and block.default_case.body_block_ids:
                            case_stop_blocks.update(block.default_case.body_block_ids)
                        lines.extend(self._emit_flat_block_section(
                            uncovered, case_stop_blocks, indent + "    ", exit_ids
                        ))
                    self.emitted_blocks.update(set(case.body_block_ids) - set(exit_ids))
            elif case.body_block_ids:
                lines.extend(self._emit_switch_case_body_flat(case, block, exit_ids, indent + "    "))
            elif case.body_block is not None:
                lines.extend(self._emit_block(case.body_block, indent + "    "))
            if case.has_break:
                lines.append(f"{indent}    break;")

        # Emit default case
        if block.default_case is not None:
            lines.append(f"{indent}default:")
            if block.default_case.body_block_ids:
                lines.extend(self._emit_switch_case_body_flat(block.default_case, block, exit_ids, indent + "    "))
            elif block.default_case.body_block is not None:
                lines.extend(self._emit_block(block.default_case.body_block, indent + "    "))
            if block.default_case.has_break:
                lines.append(f"{indent}    break;")

        lines.append(f"{indent}}}")

        return lines

    def _emit_switch_case_body_by_ids(self, body_block_ids: Set[int], indent: str) -> List[str]:
        """
        Emit switch case body using CFG block IDs.

        This is a fallback for when body_block is None but we have the list of
        CFG block IDs that make up the case body.
        """
        lines = []

        # Sort blocks by start address
        sorted_block_ids = sorted(
            body_block_ids,
            key=lambda bid: self.cfg.blocks[bid].start if bid in self.cfg.blocks else 9999999
        )

        for block_id in sorted_block_ids:
            if block_id in self.emitted_blocks:
                continue

            self.emitted_blocks.add(block_id)

            from ..emit.code_emitter import _render_block_statements

            block_lines = _render_block_statements(
                self.ssa_func,
                block_id,
                self.formatter,
                self.resolver,
                self.global_map,
            )

            for line in block_lines:
                lines.append(f"{indent}{line}")

        return lines

    def _emit_switch_case_body_flat(
        self,
        case: SwitchCase,
        switch_block: BlockSwitch,
        exit_ids: Set[int],
        indent: str
    ) -> List[str]:
        """
        Emit switch case body using flat-mode block rendering with if/else detection.
        This preserves conditional structure inside cases when collapse is incomplete.

        Before doing flat rendering, checks if any body_block_ids correspond to
        already-collapsed structured blocks (BlockSwitch, BlockWhileDo, etc.) in the
        graph. Those are emitted structurally; remaining IDs use flat rendering.
        """
        if not case.body_block_ids:
            return []

        from ..emit.code_emitter import _render_blocks_with_loops
        from ..patterns.if_else import _detect_if_else_pattern

        # Sort blocks by address
        case_body_sorted = sorted(
            case.body_block_ids,
            key=lambda bid: self.cfg.blocks[bid].start if bid in self.cfg.blocks else 9999999
        )

        # Identify CFG block IDs that map to already-collapsed structured blocks
        # (e.g., an inner switch or loop that was collapsed before the outer switch).
        # These should be emitted via the structured path, not flat if/else detection.
        #
        # We use the graph's structured_map which was populated during collapse.
        # This maps CFG IDs to their enclosing structured blocks (BlockSwitch, etc.)
        structured_blocks_by_cfg_id: Dict[int, StructuredBlock] = {}
        structured_cfg_ids: Set[int] = set()
        body_id_set = set(case_body_sorted)
        structured_map = getattr(self.graph, 'structured_map', {})

        # Find structured blocks whose covered IDs overlap with this case body.
        # Skip the switch_block itself and any block that IS the switch being emitted
        # (to prevent infinite recursion).
        current_switch_id = id(switch_block)
        seen_structs: Set[int] = set()  # Track by id() to avoid duplicates
        for bid in case_body_sorted:
            if bid in structured_cfg_ids:
                continue
            struct_block = structured_map.get(bid)
            if struct_block is None:
                continue
            if id(struct_block) in seen_structs:
                continue
            # Skip if this IS the current switch (prevent recursion)
            if id(struct_block) == current_switch_id:
                continue
            overlap = struct_block.covered_blocks & body_id_set
            if not overlap:
                continue
            seen_structs.add(id(struct_block))
            # Map the first overlapping bid (by address) to this structured block
            first_bid = min(overlap, key=lambda b: self.cfg.blocks[b].start if b in self.cfg.blocks else 9999999)
            structured_blocks_by_cfg_id[first_bid] = struct_block
            structured_cfg_ids.update(overlap)

        # Filter out structured block IDs from the flat rendering list
        flat_body_sorted = [bid for bid in case_body_sorted if bid not in structured_cfg_ids]

        # Build stop blocks from other cases/default to prevent leakage.
        # Also include structured_cfg_ids so flat if/else detection doesn't
        # walk into inner switches/loops (they'll be emitted separately).
        case_stop_blocks: Set[int] = set(structured_cfg_ids)
        for other_case in switch_block.cases:
            if other_case is not case and other_case.body_block_ids:
                case_stop_blocks.update(other_case.body_block_ids)
        if switch_block.default_case and switch_block.default_case.body_block_ids:
            case_stop_blocks.update(switch_block.default_case.body_block_ids)

        lines: List[str] = []

        # Emit blocks in address order, interleaving structured and flat sections
        emitted_structured: Set[int] = set()  # Track which structured block IDs were emitted
        flat_section: List[int] = []

        def flush_flat_section():
            """Emit accumulated flat blocks."""
            nonlocal flat_section
            if not flat_section:
                return []
            result = self._emit_flat_block_section(
                flat_section, case_stop_blocks, indent, exit_ids
            )
            flat_section = []
            return result

        for bid in case_body_sorted:
            if bid in structured_cfg_ids:
                # This bid belongs to a structured block
                struct_block = structured_blocks_by_cfg_id.get(bid)
                if struct_block is not None and id(struct_block) not in emitted_structured:
                    # Flush any pending flat blocks first
                    lines.extend(flush_flat_section())
                    # Emit the structured block (it will mark its own blocks as emitted internally)
                    lines.extend(self._emit_block(struct_block, indent))
                    emitted_structured.add(id(struct_block))
                # else: skip (already emitted or covered by another structured block)
            else:
                flat_section.append(bid)

        # Flush remaining flat blocks
        lines.extend(flush_flat_section())

        # Prevent residual case blocks from being emitted later as labels,
        # but don't suppress the switch exit block(s) if present.
        # Don't mark blocks handled by inner structured blocks - let those blocks
        # manage their own emitted_blocks tracking.
        to_mark = set(case.body_block_ids) - set(exit_ids) - structured_cfg_ids
        self.emitted_blocks.update(to_mark)
        return lines

    def _emit_flat_block_section(
        self,
        block_ids: List[int],
        case_stop_blocks: Set[int],
        indent: str,
        switch_exit_ids: Optional[Set[int]] = None,
    ) -> List[str]:
        """Emit a section of flat (non-structured) blocks with if/else detection."""
        if not block_ids:
            return []

        from ..emit.code_emitter import _render_blocks_with_loops
        from ..patterns.if_else import _detect_if_else_pattern, _detect_early_return_pattern

        # Detect early return/break patterns (conditional break inside switch case)
        early_returns: Dict[int, tuple] = {}
        if switch_exit_ids:
            for body_block_id in block_ids:
                for exit_id in switch_exit_ids:
                    early_ret = _detect_early_return_pattern(
                        self.cfg,
                        body_block_id,
                        self.start_to_block,
                        self.resolver,
                        switch_exit_block=exit_id,
                    )
                    if early_ret:
                        early_returns[body_block_id] = early_ret
                        break

        # Detect if/else patterns within this section
        block_to_if: Dict[int, Any] = {}
        visited_ifs: Set[int] = set()
        for body_block_id in block_ids:
            if body_block_id in block_to_if:
                continue
            # Skip blocks already detected as early returns
            if body_block_id in early_returns:
                continue
            temp_visited: Set[int] = set()
            if_pattern = _detect_if_else_pattern(
                self.cfg,
                body_block_id,
                self.start_to_block,
                self.resolver,
                temp_visited,
                self.func_loops,
                context_stop_blocks=case_stop_blocks,
                ssa_func=self.ssa_func,
                formatter=self.formatter,
            )
            if if_pattern:
                block_to_if[body_block_id] = if_pattern

        return _render_blocks_with_loops(
            block_ids,
            indent,
            self.ssa_func,
            self.formatter,
            self.cfg,
            self.func_loops,
            self.start_to_block,
            self.resolver,
            block_to_if,
            visited_ifs,
            self.emitted_blocks,
            self.global_map,
            early_returns=early_returns if early_returns else None,
            switch_exit_ids=switch_exit_ids,
        )

    def _emit_goto(self, block: BlockGoto, indent: str) -> List[str]:
        """Emit a goto statement."""
        lines = []

        # Emit wrapped block
        if block.wrapped_block is not None:
            lines.extend(self._emit_block(block.wrapped_block, indent))

        # Emit goto
        if block.goto_target is not None:
            target_id = None
            if isinstance(block.goto_target, BlockBasic):
                target_id = block.goto_target.original_block_id

            if target_id is not None:
                # Suppress goto when the target is the function exit/epilogue block
                # that will be emitted as the next remaining block anyway.
                # This avoids: "goto block_N; return 0;" → just "return 0;"
                if self._is_function_epilogue_block(target_id):
                    return lines
                # Inline the target block instead of emitting a goto when the
                # target is a terminal block (ends with RET, no successors) that
                # hasn't been emitted yet. This handles switch exit blocks that
                # contain real code (e.g., struct field assignment + return).
                if self._can_inline_goto_target(target_id):
                    lines.extend(self._emit_basic_by_id(target_id, indent))
                    return lines
                if target_id not in self.block_labels:
                    self.block_labels[target_id] = f"block_{target_id}"
                lines.append(f"{indent}goto {self.block_labels[target_id]};")
            else:
                label = block.target_label or f"label_{self.label_counter}"
                self.label_counter += 1
                lines.append(f"{indent}goto {label};")

        return lines

    def _can_inline_goto_target(self, block_id: int) -> bool:
        """
        Check if a goto target block can be inlined instead of using a goto.

        A block can be inlined when:
        1. It hasn't been emitted yet
        2. It's a terminal block (no successors, ends with RET)
        """
        if block_id in self.emitted_blocks:
            return False
        cfg_block = self.cfg.blocks.get(block_id)
        if not cfg_block:
            return False
        # Must be a terminal block (no successors)
        if getattr(cfg_block, 'successors', None):
            return False
        # Must end with RET
        if not cfg_block.instructions:
            return False
        last_instr = cfg_block.instructions[-1]
        if not self.resolver.is_return(last_instr.opcode):
            return False
        return True


    def _is_function_epilogue_block(self, block_id: int) -> bool:
        """Check if a block is a function epilogue (only RET + stack cleanup)."""
        cfg_block = self.cfg.blocks.get(block_id)
        if not cfg_block:
            return False
        # Check that this block has no successors (it's a terminal block)
        if getattr(cfg_block, 'successors', None):
            return False
        # Check that the last instruction is RET
        if not cfg_block.instructions:
            return False
        last_instr = cfg_block.instructions[-1]
        if not self.resolver.is_return(last_instr.opcode):
            return False
        # Check that the block only contains stack ops, constants, and RET
        # (i.e., function epilogue pattern: SSP, GCP, LLD, RET)
        for instr in cfg_block.instructions:
            mnemonic = self.resolver.get_mnemonic(instr.opcode)
            if mnemonic not in ('SSP', 'GCP', 'LLD', 'GLD', 'RET', 'LCP', 'PUSH'):
                return False
        return True

    def _extract_condition(
        self,
        block: StructuredBlock,
        negate: Optional[bool] = None
    ) -> Optional[str]:
        """
        Extract condition expression from a block.

        Args:
            block: The block containing the conditional jump
            negate: If specified, overrides the auto-detection of negation.
                    True = apply ! prefix, False = no prefix, None = auto-detect from JZ/JNZ

        Returns:
            The rendered condition expression, or None if not applicable
        """
        if not isinstance(block, BlockBasic):
            if isinstance(block, BlockList):
                candidate = self._find_condition_block_in_list(block)
                if candidate is None:
                    # Fallback: try to detect uncollapsed AND/OR chain via CFG walk
                    return self._try_extract_and_or_chain(block, negate)
                block = candidate
            else:
                # Fallback: try to detect uncollapsed AND/OR chain via CFG walk
                return self._try_extract_and_or_chain(block, negate)

        cfg_block_id = block.original_block_id
        cfg = self.cfg

        # Use render_condition to get the condition
        # Pass negate to override auto-detection when branches were swapped
        cond_render = render_condition(
            self.ssa_func,
            cfg_block_id,
            self.formatter,
            cfg,
            self.resolver,
            negate=negate,
        )

        return cond_render.text if cond_render else None

    def _find_condition_block_in_list(self, block_list: BlockList) -> Optional[BlockBasic]:
        """Find the last basic block in a list that ends with a conditional jump."""
        for component in reversed(block_list.components):
            if isinstance(component, BlockBasic):
                cfg_block = self.cfg.blocks.get(component.original_block_id)
                if cfg_block and _find_condition_jump(cfg_block, self.resolver):
                    return component
            if isinstance(component, BlockList):
                nested = self._find_condition_block_in_list(component)
                if nested is not None:
                    return nested
        return None
