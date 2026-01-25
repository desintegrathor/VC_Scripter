"""
Hierarchical block structure for control flow representation.

This package provides Ghidra-style hierarchical block types for representing
structured control flow after pattern collapse.
"""

from .hierarchy import (
    BlockType,
    EdgeType,
    StructuredBlock,
    BlockBasic,
    BlockList,
    BlockIf,
    BlockWhileDo,
    BlockDoWhile,
    BlockInfLoop,
    BlockSwitch,
    BlockGoto,
    BlockGraph,
    BlockEdge,
    SwitchCase,
)

__all__ = [
    "BlockType",
    "EdgeType",
    "StructuredBlock",
    "BlockBasic",
    "BlockList",
    "BlockIf",
    "BlockWhileDo",
    "BlockDoWhile",
    "BlockInfLoop",
    "BlockSwitch",
    "BlockGoto",
    "BlockGraph",
    "BlockEdge",
    "SwitchCase",
]
