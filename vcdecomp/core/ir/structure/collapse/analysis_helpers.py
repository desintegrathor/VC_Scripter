"""
Helper functions for using advanced analyses in collapse rules.

This module provides utility functions that allow collapse rules to leverage
dominator analysis, loop analysis, and spanning tree information without
directly coupling to those implementations.
"""

from __future__ import annotations

from typing import Optional, List, Set, TYPE_CHECKING

from ..blocks.hierarchy import BlockGraph, StructuredBlock, EdgeType

if TYPE_CHECKING:
    from ..analysis.dominance import DominatorAnalysis
    from ..analysis.loop_analysis import LoopAnalysis, LoopBody
    from ..analysis.irreducible import SpanningTreeAnalysis


def is_loop_header(
    block: StructuredBlock,
    loop_analysis: Optional['LoopAnalysis'] = None
) -> bool:
    """
    Check if a block is a loop header.

    Args:
        block: The block to check
        loop_analysis: Optional loop analysis (more accurate if provided)

    Returns:
        True if block is a loop header
    """
    if loop_analysis is not None:
        return loop_analysis.is_loop_header(block)

    # Fallback: Check if block has a back edge coming in
    for edge in block.in_edges:
        if edge.edge_type == EdgeType.BACK_EDGE:
            return True
    return False


def get_loop_body(
    header: StructuredBlock,
    loop_analysis: Optional['LoopAnalysis'] = None
) -> Optional[Set[int]]:
    """
    Get the loop body for a given header.

    Args:
        header: The loop header block
        loop_analysis: Optional loop analysis (more accurate if provided)

    Returns:
        Set of block IDs in the loop body, or None if not a loop
    """
    if loop_analysis is not None:
        loop = loop_analysis.get_loop_by_header(header)
        if loop is not None:
            return loop.body
        return None

    # Fallback: Simple heuristic - all blocks with back edges to header
    body = {header.block_id}
    for edge in header.in_edges:
        if edge.edge_type == EdgeType.BACK_EDGE:
            body.add(edge.source.block_id)
    return body if len(body) > 1 else None


def get_loop_tails(
    header: StructuredBlock,
    loop_analysis: Optional['LoopAnalysis'] = None
) -> List[StructuredBlock]:
    """
    Get all tail blocks for a loop (blocks with back edges to header).

    Args:
        header: The loop header block
        loop_analysis: Optional loop analysis

    Returns:
        List of tail blocks
    """
    if loop_analysis is not None:
        loop = loop_analysis.get_loop_by_header(header)
        if loop is not None:
            return loop.tails
        return []

    # Fallback: Find blocks with back edges to header
    tails = []
    for edge in header.in_edges:
        if edge.edge_type == EdgeType.BACK_EDGE:
            tails.append(edge.source)
    return tails


def get_loop_exits(
    header: StructuredBlock,
    loop_analysis: Optional['LoopAnalysis'] = None
) -> List[tuple[StructuredBlock, StructuredBlock]]:
    """
    Get all exit edges from a loop.

    Args:
        header: The loop header block
        loop_analysis: Optional loop analysis

    Returns:
        List of (source, target) tuples for exit edges
    """
    if loop_analysis is not None:
        loop = loop_analysis.get_loop_by_header(header)
        if loop is not None:
            return loop.exits
        return []

    # Fallback: Heuristic approach
    # Not accurate without proper loop body analysis
    return []


def is_loop_exit_edge(
    source: StructuredBlock,
    target: StructuredBlock,
    loop_analysis: Optional['LoopAnalysis'] = None
) -> bool:
    """
    Check if an edge is a loop exit.

    Args:
        source: Source block of the edge
        target: Target block of the edge
        loop_analysis: Optional loop analysis

    Returns:
        True if this edge exits a loop
    """
    if loop_analysis is not None:
        # Check if source is in a loop and target is not
        loop = loop_analysis.get_loop_for_block(source)
        if loop is not None:
            return target.block_id not in loop.body
        return False

    # Fallback: Check edge type
    for edge in source.out_edges:
        if edge.target == target:
            return edge.edge_type == EdgeType.LOOP_EXIT
    return False


def dominates(
    dominator: StructuredBlock,
    dominated: StructuredBlock,
    dom_analysis: Optional['DominatorAnalysis'] = None
) -> bool:
    """
    Check if one block dominates another.

    Args:
        dominator: Potential dominating block
        dominated: Potentially dominated block
        dom_analysis: Optional dominator analysis (more accurate if provided)

    Returns:
        True if dominator dominates dominated
    """
    if dom_analysis is not None:
        return dom_analysis.dominates(dominator, dominated)

    # Fallback: Very rough heuristic
    # This is not accurate - proper dominator analysis required
    return dominator.block_id <= dominated.block_id


def get_immediate_dominator(
    block: StructuredBlock,
    dom_analysis: Optional['DominatorAnalysis'] = None
) -> Optional[StructuredBlock]:
    """
    Get the immediate dominator of a block.

    Args:
        block: The block to get idom for
        dom_analysis: Optional dominator analysis (required for accurate result)

    Returns:
        The immediate dominator, or None
    """
    if dom_analysis is not None:
        return dom_analysis.get_idom(block)
    return None


def get_containing_loops(
    block: StructuredBlock,
    loop_analysis: Optional['LoopAnalysis'] = None
) -> List['LoopBody']:
    """
    Get all loops containing a block (innermost to outermost).

    Args:
        block: The block to check
        loop_analysis: Optional loop analysis

    Returns:
        List of LoopBody objects, sorted by depth
    """
    if loop_analysis is not None:
        return loop_analysis.get_containing_loops(block)
    return []


def is_irreducible_edge(
    source: StructuredBlock,
    target: StructuredBlock,
    spanning_tree: Optional['SpanningTreeAnalysis'] = None
) -> bool:
    """
    Check if an edge is irreducible.

    Args:
        source: Source block of the edge
        target: Target block of the edge
        spanning_tree: Optional spanning tree analysis

    Returns:
        True if this edge is irreducible
    """
    if spanning_tree is not None:
        return spanning_tree.is_irreducible(source, target)

    # Fallback: Check edge type
    for edge in source.out_edges:
        if edge.target == target:
            return edge.edge_type == EdgeType.IRREDUCIBLE
    return False


def get_loop_nesting_depth(
    block: StructuredBlock,
    loop_analysis: Optional['LoopAnalysis'] = None
) -> int:
    """
    Get the loop nesting depth of a block.

    Args:
        block: The block to check
        loop_analysis: Optional loop analysis

    Returns:
        Nesting depth (0 = not in loop, 1 = in one loop, etc.)
    """
    if loop_analysis is not None:
        loops = loop_analysis.get_containing_loops(block)
        return len(loops)

    # Fallback: Count back edges
    depth = 0
    visited = set()
    current = block

    # Very rough approximation
    for edge in current.in_edges:
        if edge.edge_type == EdgeType.BACK_EDGE and edge.source.block_id not in visited:
            visited.add(edge.source.block_id)
            depth += 1

    return depth
