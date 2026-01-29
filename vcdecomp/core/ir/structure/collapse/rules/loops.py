"""
Loop collapse rules.

This module contains rules for collapsing while, do-while, and infinite loop patterns.
"""

from __future__ import annotations

from typing import Optional

from .base import CollapseRule
from ..analysis_helpers import (
    is_loop_header,
    get_loop_body,
    get_loop_tails,
    dominates,
)
from ...blocks.hierarchy import (
    BlockType,
    EdgeType,
    BlockGraph,
    StructuredBlock,
    BlockWhileDo,
    BlockDoWhile,
    BlockInfLoop,
    BlockEdge,
)


class RuleBlockWhileDo(CollapseRule):
    """
    Collapse while loop pattern.

    Pattern:
        header <--back-- body
        header --exit--> after

    Where header is loop condition and body loops back.

    Result:
        BlockWhileDo(header, body)
    """

    def __init__(self):
        super().__init__("BlockWhileDo")

    def _resolve_components(
        self,
        graph: BlockGraph,
        block: StructuredBlock
    ) -> Optional[tuple[StructuredBlock, StructuredBlock, int]]:
        loop_analysis = getattr(graph, "loop_analysis", None)
        dom_analysis = getattr(graph, "dom_analysis", None)
        loop_body = get_loop_body(block, loop_analysis) if loop_analysis else None

        body_block = None
        exit_block = None
        body_edge_index = -1

        if loop_body:
            for i, edge in enumerate(block.out_edges):
                if edge.target.block_id in loop_body and edge.target != block:
                    if body_block is not None:
                        return None
                    body_block = edge.target
                    body_edge_index = i
                elif edge.target != block:
                    exit_block = edge.target

            if body_block is None or exit_block is None:
                return None

            if exit_block.block_id in loop_body:
                return None

            if dom_analysis and not dominates(block, body_block, dom_analysis):
                return None

            tails = get_loop_tails(block, loop_analysis)
            if not tails:
                return None

            return body_block, exit_block, body_edge_index

        # Fallback to local back-edge detection
        body_block = None
        exit_block = None
        body_edge_index = -1
        for edge in block.in_edges:
            if edge.edge_type == EdgeType.BACK_EDGE:
                body_block = edge.source
                break

        if body_block is None:
            return None

        for i, edge in enumerate(block.out_edges):
            if edge.target == body_block:
                if block.is_goto_out(i):
                    return None
                body_edge_index = i
            elif edge.target != block:
                exit_block = edge.target

        if exit_block is None:
            return None

        return body_block, exit_block, body_edge_index

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        loop_analysis = getattr(graph, "loop_analysis", None)
        if loop_analysis and not is_loop_header(block, loop_analysis):
            return False

        # Header must have exactly two successors (condition + exit)
        if len(block.out_edges) != 2:
            return False

        resolved = self._resolve_components(graph, block)
        if resolved is None:
            return False
        body_block, _, _ = resolved

        # Body should have single successor back to header
        if not body_block.has_single_successor():
            return False
        if body_block.get_single_successor() != block:
            return False

        # Body should have single predecessor (the header)
        if not body_block.has_single_predecessor():
            return False

        return True

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        resolved = self._resolve_components(graph, block)
        if resolved is None:
            return None
        body_block, exit_block, body_edge_index = resolved

        # Create while block
        while_block = BlockWhileDo(
            block_type=BlockType.WHILE_DO,
            block_id=graph._allocate_block_id(),
            condition_block=block,
            body_block=body_block,
        )

        # Ghidra: negate condition if body is on false branch (index 1)
        # while (cond) { body } means cond should be true to enter body
        # If bytecode has false branch going to body, we need to negate
        if body_edge_index == 1:
            while_block.negate_condition()

        # Update covered blocks
        while_block.covered_blocks = block.covered_blocks | body_block.covered_blocks

        # Register in structured_map for emitter access (don't overwrite inner blocks)
        if hasattr(graph, 'structured_map'):
            for cfg_id in while_block.covered_blocks:
                if cfg_id not in graph.structured_map:
                    graph.structured_map[cfg_id] = while_block

        # Set parent references
        block.parent = while_block
        body_block.parent = while_block

        # Redirect incoming edges (excluding back edge from body)
        for edge in block.in_edges:
            if edge.source != body_block and not edge.source.is_collapsed:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=while_block,
                    edge_type=edge.edge_type
                )
                while_block.in_edges.append(new_edge)
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[i] = new_edge

        # Create edge to exit
        exit_edge = BlockEdge(source=while_block, target=exit_block, edge_type=EdgeType.NORMAL)
        while_block.out_edges.append(exit_edge)

        # Update exit's in_edges
        exit_block.in_edges = [e for e in exit_block.in_edges if e.source != block]
        exit_block.in_edges.append(exit_edge)

        # Add while_block, remove old blocks
        graph.blocks[while_block.block_id] = while_block
        if graph.entry_block == block:
            graph.entry_block = while_block

        graph.remove_block(block)
        graph.remove_block(body_block)

        return while_block


class RuleBlockDoWhile(CollapseRule):
    """
    Collapse do-while loop pattern.

    Pattern:
        body --> cond --back--> body
        cond --exit--> after

    Where condition is at the bottom.

    Result:
        BlockDoWhile(body, cond)
    """

    def __init__(self):
        super().__init__("BlockDoWhile")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        loop_analysis = getattr(graph, "loop_analysis", None)
        dom_analysis = getattr(graph, "dom_analysis", None)
        if loop_analysis and not is_loop_header(block, loop_analysis):
            return False

        # This block is the body - should have single successor (condition)
        if not block.has_single_successor():
            return False

        cond = block.get_single_successor()
        if cond is None or cond.is_collapsed:
            return False

        # Condition must have two successors
        if len(cond.out_edges) != 2:
            return False

        # One of condition's successors should be back to body (this block)
        has_back_to_body = False
        for edge in cond.out_edges:
            if edge.target == block and edge.edge_type == EdgeType.BACK_EDGE:
                has_back_to_body = True
                break

        if not has_back_to_body:
            return False

        if loop_analysis:
            loop_body = get_loop_body(block, loop_analysis)
            if loop_body is None or cond.block_id not in loop_body:
                return False
            if dom_analysis and not dominates(block, cond, dom_analysis):
                return False

        # Condition should have single predecessor (body)
        if not cond.has_single_predecessor():
            return False

        return True

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        cond = block.get_single_successor()
        if cond is None:
            return None

        # Find exit block and back edge index
        exit_block = None
        back_edge_index = -1
        for i, edge in enumerate(cond.out_edges):
            if edge.target == block and edge.edge_type == EdgeType.BACK_EDGE:
                back_edge_index = i
            elif edge.target != block:
                exit_block = edge.target

        if exit_block is None:
            return None

        # Create do-while block
        dowhile_block = BlockDoWhile(
            block_type=BlockType.DO_WHILE,
            block_id=graph._allocate_block_id(),
            body_block=block,
            condition_block=cond,
        )

        # Ghidra: negate condition if back edge is on false branch (index 1)
        # do { body } while (cond) means cond should be true to loop back
        # If bytecode has false branch looping back, we need to negate
        if back_edge_index == 1:
            dowhile_block.negate_condition()

        # Update covered blocks
        dowhile_block.covered_blocks = block.covered_blocks | cond.covered_blocks

        # Register in structured_map for emitter access (don't overwrite inner blocks)
        if hasattr(graph, 'structured_map'):
            for cfg_id in dowhile_block.covered_blocks:
                if cfg_id not in graph.structured_map:
                    graph.structured_map[cfg_id] = dowhile_block

        # Set parent references
        block.parent = dowhile_block
        cond.parent = dowhile_block

        # Redirect incoming edges to body (now to dowhile)
        for edge in block.in_edges:
            if edge.source != cond and not edge.source.is_collapsed:
                new_edge = BlockEdge(
                    source=edge.source,
                    target=dowhile_block,
                    edge_type=edge.edge_type
                )
                dowhile_block.in_edges.append(new_edge)
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[i] = new_edge

        # Create edge to exit
        exit_edge = BlockEdge(source=dowhile_block, target=exit_block, edge_type=EdgeType.NORMAL)
        dowhile_block.out_edges.append(exit_edge)

        # Update exit's in_edges
        exit_block.in_edges = [e for e in exit_block.in_edges if e.source != cond]
        exit_block.in_edges.append(exit_edge)

        # Add dowhile_block, remove old blocks
        graph.blocks[dowhile_block.block_id] = dowhile_block
        if graph.entry_block == block:
            graph.entry_block = dowhile_block

        graph.remove_block(block)
        graph.remove_block(cond)

        return dowhile_block


class RuleBlockInfLoop(CollapseRule):
    """
    Collapse infinite loop (while(1) or for(;;)).

    Pattern:
        bl --> bl  (single exit loops back to itself)

    Result:
        BlockInfLoop(bl)

    Ghidra preconditions from ruleBlockInfLoop():
    - bl->sizeOut() == 1 (single exit)
    - !bl->isGotoOut(0) (exit is not unstructured)
    - bl->getOut(0) == bl (block loops to itself)
    """

    def __init__(self):
        super().__init__("BlockInfLoop")

    def matches(self, graph: BlockGraph, block: StructuredBlock) -> bool:
        # Block must have exactly one successor
        if not block.has_single_successor():
            return False

        successor = block.get_single_successor()

        # Must loop back to itself
        if successor != block:
            return False

        # Edge must not be marked as goto/irreducible
        for edge in block.out_edges:
            if edge.target == block:
                if edge.edge_type in (EdgeType.GOTO_EDGE, EdgeType.IRREDUCIBLE):
                    return False

        return True

    def apply(self, graph: BlockGraph, block: StructuredBlock) -> Optional[StructuredBlock]:
        # Create infinite loop wrapping this block
        inf_loop = BlockInfLoop(
            block_type=BlockType.INF_LOOP,
            block_id=graph._allocate_block_id(),
            body_block=block,
        )

        # Update covered blocks
        inf_loop.covered_blocks = set(block.covered_blocks)

        # Register in structured_map for emitter access (don't overwrite inner blocks)
        if hasattr(graph, 'structured_map'):
            for cfg_id in inf_loop.covered_blocks:
                if cfg_id not in graph.structured_map:
                    graph.structured_map[cfg_id] = inf_loop

        # Set parent
        block.parent = inf_loop

        # Redirect incoming edges to inf_loop (skip self-loop)
        for edge in block.in_edges:
            if edge.source != block:  # Skip self-loop
                new_edge = BlockEdge(
                    source=edge.source,
                    target=inf_loop,
                    edge_type=edge.edge_type
                )
                inf_loop.in_edges.append(new_edge)
                # Update source's out_edges
                for i, out_edge in enumerate(edge.source.out_edges):
                    if out_edge.target == block:
                        edge.source.out_edges[i] = new_edge

        # InfLoop has no outgoing edges (it's infinite)
        # Break statements would need separate handling

        # Add to graph, remove old block
        graph.blocks[inf_loop.block_id] = inf_loop
        if graph.entry_block == block:
            graph.entry_block = inf_loop

        graph.remove_block(block)

        return inf_loop
