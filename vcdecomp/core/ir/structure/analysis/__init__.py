"""
Analysis package for control flow analysis.

This package contains modules for analyzing control flow graphs, conditions,
value tracing, and variable collection.
"""

from .flow import (
    _get_loop_for_block,
    _is_back_edge_target,
    _find_if_body_blocks,
    _find_common_successor,
    _is_jmp_after_jz,
    _find_all_jz_targets,
    _find_common_true_target,
    _find_case_body_blocks,
)

from .condition import (
    ConditionRender,
    _extract_condition_from_block,
    _extract_condition_expr,
    _combine_conditions,
    _collect_and_chain,
    _collect_or_chain,
    render_condition,
)

from .value_trace import (
    _trace_value_to_function_call,
    _trace_value_to_global,
    _trace_value_to_parameter,
    _find_switch_variable_from_nearby_gcp,
)

from .variables import (
    _collect_local_variables,
)

from .dominance import (
    DominatorAnalysis,
    compute_dominators,
)

from .irreducible import (
    SpanningTreeAnalysis,
    SpanningEdgeType,
    detect_irreducible_edges,
)

from .loop_analysis import (
    LoopBody,
    LoopAnalysis,
    analyze_loops,
)

__all__ = [
    # Flow analysis
    "_get_loop_for_block",
    "_is_back_edge_target",
    "_find_if_body_blocks",
    "_find_common_successor",
    "_is_jmp_after_jz",
    "_find_all_jz_targets",
    "_find_common_true_target",
    "_find_case_body_blocks",
    # Condition analysis
    "ConditionRender",
    "_extract_condition_from_block",
    "_extract_condition_expr",
    "_combine_conditions",
    "_collect_and_chain",
    "_collect_or_chain",
    "render_condition",
    # Value tracing
    "_trace_value_to_function_call",
    "_trace_value_to_global",
    "_trace_value_to_parameter",
    "_find_switch_variable_from_nearby_gcp",
    # Variable collection
    "_collect_local_variables",
    # Dominator analysis
    "DominatorAnalysis",
    "compute_dominators",
    # Irreducible edge detection
    "SpanningTreeAnalysis",
    "SpanningEdgeType",
    "detect_irreducible_edges",
    # Loop analysis
    "LoopBody",
    "LoopAnalysis",
    "analyze_loops",
]
