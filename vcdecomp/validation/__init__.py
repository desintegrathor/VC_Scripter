"""
Validation module for recompilation and bytecode comparison.

This module provides tools to:
- Compile decompiled source code using original Pterodon compiler tools
- Compare bytecode of original and recompiled .SCR files
- Generate validation reports
"""

from .compiler_wrapper import (
    BaseCompiler,
    SCMPWrapper,
    SPPWrapper,
    SCCWrapper,
    SASMWrapper,
)
from .compilation_types import (
    CompilationResult,
    CompilationError,
    CompilationStage,
    ErrorSeverity,
)
from .bytecode_compare import (
    BytecodeComparator,
    ComparisonResult,
    SectionComparison,
    Difference,
    DifferenceType,
    DifferenceSeverity,
)
from .difference_types import (
    DifferenceCategory,
    DifferenceCategorizer,
    CategorizedDifference,
    DifferenceSummary,
    categorize_differences,
    get_summary,
    filter_by_category,
    filter_by_severity,
    get_semantic_differences,
    get_cosmetic_differences,
)
from .validation_types import (
    ValidationResult,
    ValidationVerdict,
)
from .validator import (
    ValidationOrchestrator,
)
from .report_generator import (
    ReportGenerator,
    ANSIColors,
)
from .cache import (
    ValidationCache,
    CacheEntry,
    CacheStatistics,
)
from .regression import (
    RegressionBaseline,
    RegressionComparator,
    RegressionReport,
    RegressionItem,
    RegressionStatus,
    BaselineEntry,
)

__all__ = [
    'BaseCompiler',
    'SCMPWrapper',
    'SPPWrapper',
    'SCCWrapper',
    'SASMWrapper',
    'CompilationResult',
    'CompilationError',
    'CompilationStage',
    'ErrorSeverity',
    'BytecodeComparator',
    'ComparisonResult',
    'SectionComparison',
    'Difference',
    'DifferenceType',
    'DifferenceSeverity',
    'DifferenceCategory',
    'DifferenceCategorizer',
    'CategorizedDifference',
    'DifferenceSummary',
    'categorize_differences',
    'get_summary',
    'filter_by_category',
    'filter_by_severity',
    'get_semantic_differences',
    'get_cosmetic_differences',
    'ValidationResult',
    'ValidationVerdict',
    'ValidationOrchestrator',
    'ReportGenerator',
    'ANSIColors',
    'ValidationCache',
    'CacheEntry',
    'CacheStatistics',
    'RegressionBaseline',
    'RegressionComparator',
    'RegressionReport',
    'RegressionItem',
    'RegressionStatus',
    'BaselineEntry',
]
