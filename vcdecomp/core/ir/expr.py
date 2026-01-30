"""
Expression formatting utilities on top of SSA.

Turns SSA instructions into human-friendly assignments/infix expressions
as a first step toward structured, C-like output.
"""

from __future__ import annotations

import sys
import struct
import math
import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Set, Tuple

from ..disasm import opcodes
from ..constants import (
    get_constant_name,
    get_player_constant,
    get_known_constant_for_variable,
    FUNCTION_CONSTANT_CONTEXT,
)
from ..structures import (
    get_struct_by_name, get_struct_by_size, get_verified_field_name,
    infer_struct_from_function, STRUCTURES_BY_SIZE
)
from .ssa import SSAFunction, SSAInstruction, SSAValue
from .global_resolver import resolve_globals
from .constant_propagation import ConstantPropagator, ConstantValue
from .field_tracker import FieldAccessTracker
from ..headers.database import get_header_database
from .parenthesization import (
    ExpressionContext,
    needs_parens,
    is_simple_expression,
    get_operator_info,
    wrap_if_needed
)
from ..text_database import (
    should_annotate_function,
    format_text_annotation,
    get_text_database,
    StructAssignmentTracker,
    TEXT_ID_MIN,
    TEXT_ID_MAX,
)


def _strip_ssa_version_suffix(name: str) -> str:
    """
    Strip SSA version suffixes (_vN) from local variable names.

    The SSA variable renaming creates versioned names like local_0_v2, local_0_v7
    for different definitions of the same stack slot. Since the decompiled scripts
    don't have parallel control flow that would make same-named variables ambiguous,
    all versions should render as the base name (e.g., local_0).

    Also handles address-of prefix: &local_0_v3 → &local_0
    """
    if '_v' not in name:
        return name

    # Handle &prefix
    prefix = ''
    clean = name
    if clean.startswith('&'):
        prefix = '&'
        clean = clean[1:]

    # Only strip from local_N_vM and param_N_vM patterns
    if clean.startswith(('local_', 'param_')):
        # Split on _v and check that the suffix is a number
        idx = clean.rfind('_v')
        if idx > 0 and clean[idx+2:].isdigit():
            return prefix + clean[:idx]

    return name


def _is_likely_float(val: int) -> bool:
    """
    Detekuje zda je hodnota pravděpodobně IEEE 754 float konstanta.

    Heuristiky:
    - Hodnota musí být v rozumném rozsahu (ne NaN, ne Inf)
    - Float hodnota musí být "hezká" (celé číslo, nebo malý počet desetinných míst)
    - Vyloučíme hodnoty které vypadají jako adresy nebo flagy
    """
    # FIX: 0 is more commonly an integer, should not be float by heuristic
    # If 0 needs to be 0.0f, it should be determined by expected type context
    if val == 0:
        return False

    # FIXED: Narrowed range exclusion from 0-1000 to 0-10
    # This allows common whole number floats like 10.0f, 30.0f, 60.0f, 100.0f
    if 0 < val < 10:
        return False

    # Known IEEE 754 float bit patterns (common game constants)
    # These are recognized immediately without further heuristics
    KNOWN_FLOAT_PATTERNS = {
        0x3F800000,  # 1.0f
        0x3F000000,  # 0.5f
        0x40000000,  # 2.0f
        0x40400000,  # 3.0f
        0x40A00000,  # 5.0f
        0x41200000,  # 10.0f
        0x41F00000,  # 30.0f
        0x42700000,  # 60.0f
        0x42C80000,  # 100.0f
        0xBF800000,  # -1.0f
        0xC1200000,  # -10.0f
    }
    if (val & 0xFFFFFFFF) in KNOWN_FLOAT_PATTERNS:
        return True

    # Vyloučíme hodnoty které vypadají jako adresy (zarovnané na 4)
    if val > 0x10000 and val % 4 == 0 and val < 0x3F000000:
        return False

    try:
        f = struct.unpack('<f', struct.pack('<I', val & 0xFFFFFFFF))[0]

        # Nesmí být NaN nebo Inf
        if math.isnan(f) or math.isinf(f):
            return False

        # Rozumný rozsah pro herní konstanty
        if abs(f) > 1e6 or (abs(f) < 1e-6 and f != 0.0):
            return False

        # Kontrola zda je to "hezká" hodnota
        # Celá čísla nebo hodnoty s max 2 desetinnými místy
        if f == int(f):
            return True

        # Hodnoty jako 0.5, 0.25, 0.75, 1.5, etc.
        rounded = round(f, 2)
        if abs(f - rounded) < 1e-5:
            return True

        # FIXED: Expanded common_floats to include more whole number floats
        # Added: 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, 100.0 explicitly
        common_floats = {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
                        1.0, 1.1, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0,
                        10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 100.0,
                        0.05, 0.075, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65}
        if rounded in common_floats or round(f, 3) in common_floats:
            return True

    except (struct.error, OverflowError):
        return False

    return False


def _format_float(val: int) -> str:
    """Formátuje int hodnotu jako float literal."""
    f = struct.unpack('<f', struct.pack('<I', val & 0xFFFFFFFF))[0]

    # FIXED: Handle 0.0f explicitly
    if f == 0.0:
        return "0.0f"

    if f == int(f):
        return f"{int(f)}.0f"

    # FIXED: Increased precision from 4 to 6 decimal places
    rounded = round(f, 6)
    if rounded == int(rounded):
        return f"{int(rounded)}.0f"

    # FIXED: Add scientific notation for extreme values
    if abs(f) >= 1e4 or (abs(f) < 1e-3 and f != 0.0):
        return f"{f:.6e}f"

    return f"{rounded}f"


def _parse_xfn_arg_types(signature: str) -> List[str]:
    """
    Parsuje XFN signaturu a extrahuje typy argumentů.

    Příklady:
        'SC_P_Create(void*):void*' → ['void*']
        'SC_P_SetPos(int, void*):void' → ['int', 'void*']
        'SC_Log(int, char*):void' → ['int', 'char*']
    """
    paren_start = signature.find('(')
    paren_end = signature.find(')')
    if paren_start < 0 or paren_end < 0:
        return []
    args_str = signature[paren_start + 1:paren_end]
    if not args_str.strip():
        return []
    return [a.strip() for a in args_str.split(',')]


def _is_numeric_type(type_str: str) -> bool:
    """Check if type string represents a numeric type (not a string/char*)."""
    if not type_str:
        return False
    type_lower = type_str.lower().strip()
    # String types - these should render as strings
    # Handle both "char*" and "*char" formats from XFN signatures
    if type_lower in ('char*', 'string', 'const char*', '*char'):
        return False
    # Numeric and pointer types - these should NOT render as strings
    return True


INFIX_OPS: Dict[str, str] = {
    "ADD": "+",
    "SUB": "-",
    "MUL": "*",
    "DIV": "/",
    "IDIV": "/",
    "MOD": "%",
    "BA": "&",
    "BO": "|",
    "BX": "^",
    "LS": "<<",
    "RS": ">>",
    "AND": "&&",
    "OR": "||",
    "EQU": "==",
    "NEQ": "!=",
    "LES": "<",
    "LEQ": "<=",
    "GRE": ">",
    "GEQ": ">=",
    "ULES": "<",   # Unsigned less than
    "ULEQ": "<=",  # Unsigned less than or equal
    "UGRE": ">",   # Unsigned greater than
    "UGEQ": ">=",  # Unsigned greater than or equal
    "FADD": "+",
    "FSUB": "-",
    "FMUL": "*",
    "FDIV": "/",
    "FLES": "<",
    "FLEQ": "<=",
    "FGRE": ">",
    "FGEQ": ">=",
    "FEQU": "==",
    "FNEQ": "!=",
    "DADD": "+",
    "DSUB": "-",
    "DMUL": "*",
    "DDIV": "/",
    "DLES": "<",
    "DLEQ": "<=",
    "DGRE": ">",
    "DGEQ": ">=",
    "DEQU": "==",
    "DNEQ": "!=",
    "CLES": "<",
    "CLEQ": "<=",
    "CEQU": "==",
    "CNEQ": "!=",
    "SGRE": ">",
    "SLES": "<",
    "SLEQ": "<=",
    "SEQU": "==",
}

UNARY_PREFIX = {
    "NEG": "-",
    "FNEG": "-",
    "DNEG": "-",
    "BN": "~",
}

CAST_OPS = {"ITOF", "FTOI", "ITOD", "DTOI", "DTOF", "FTOD", "SCI", "SSI", "UCI", "USI"}

# Float operation mnemonics that require float operand rendering
FLOAT_OPS = {
    "FADD", "FSUB", "FMUL", "FDIV",
    "FLES", "FLEQ", "FGRE", "FGEQ", "FEQU", "FNEQ",
    "FNEG",
}

# Double operation mnemonics that require double operand rendering
DOUBLE_OPS = {
    "DADD", "DSUB", "DMUL", "DDIV",
    "DLES", "DLEQ", "DGRE", "DGEQ", "DEQU", "DNEQ",
    "DNEG",
}


def _get_operand_type_from_mnemonic(mnemonic: str) -> Optional[str]:
    """
    Get expected operand type based on instruction mnemonic.

    Float and double operations should render their operands as float/double
    literals rather than raw integers. Integer comparisons should render
    operands as integers to avoid 0.0f in conditions like "gMission_phase > 0".
    """
    if mnemonic in FLOAT_OPS:
        return "float"
    if mnemonic in DOUBLE_OPS:
        return "double"
    # Integer comparison and arithmetic operations should use int operands
    # This prevents 0 from being rendered as 0.0f in conditions like "x > 0"
    if mnemonic in {"GRE", "GEQ", "LES", "LEQ", "EQU", "NEQ",
                    "UGRE", "UGEQ", "ULES", "ULEQ",  # Unsigned comparisons
                    "ADD", "SUB", "MUL", "DIV", "IDIV", "MOD",  # Integer arithmetic
                    "BA", "BO", "BX", "LS", "RS"}:  # Bitwise operations
        return "int"
    return None


def _is_printable_ascii(s: str) -> bool:
    """
    Check if string contains only printable ASCII characters (0x20-0x7E).

    This is used to distinguish real strings from binary data that happens
    to decode as extended Latin characters (like 0xFF = 'ÿ').
    """
    return all(0x20 <= ord(c) <= 0x7E for c in s)


COMPARISON_OPS = {
    "EQU", "NEQ", "LES", "LEQ", "GRE", "GEQ",
    "ULES", "ULEQ", "UGRE", "UGEQ",  # Unsigned comparisons
    "FEQU", "FNEQ", "FLES", "FLEQ", "FGRE", "FGEQ",
    "DEQU", "DNEQ", "DLES", "DLEQ", "DGRE", "DGEQ",
    "CEQU", "CNEQ", "CLES", "CLEQ",
    "SEQU", "SLES", "SLEQ", "SGRE",
}

# Negation mapping for comparison operators (Ghidra-inspired)
# Maps each comparison to its logical negation:
# !(a < b) => (a >= b), !(a == b) => (a != b), etc.
COMPARISON_NEGATION = {
    # Integer comparisons
    "EQU": "NEQ",
    "NEQ": "EQU",
    "LES": "GEQ",
    "LEQ": "GRE",
    "GRE": "LEQ",
    "GEQ": "LES",
    # Unsigned comparisons
    "ULES": "UGEQ",
    "ULEQ": "UGRE",
    "UGRE": "ULEQ",
    "UGEQ": "ULES",
    # Float comparisons
    "FEQU": "FNEQ",
    "FNEQ": "FEQU",
    "FLES": "FGEQ",
    "FLEQ": "FGRE",
    "FGRE": "FLEQ",
    "FGEQ": "FLES",
    # Double comparisons
    "DEQU": "DNEQ",
    "DNEQ": "DEQU",
    "DLES": "DGEQ",
    "DLEQ": "DGRE",
    "DGRE": "DLEQ",
    "DGEQ": "DLES",
    # Char comparisons
    "CEQU": "CNEQ",
    "CNEQ": "CEQU",
    "CLES": "CLEQ",  # Note: No CGEQ in opcodes
    "CLEQ": "CLES",  # Approximation
    # Short comparisons
    "SEQU": "SLES",  # Approximation (no SNEQ in original set)
    "SLES": "SLEQ",  # Approximation
    "SLEQ": "SGRE",
    "SGRE": "SLEQ",
}


def negate_comparison_op(op: str) -> str:
    """
    Negate a comparison operator.

    Given a comparison operator like "LES" (<), returns its negation "GEQ" (>=).
    This follows Ghidra's negateCondition logic for flipping conditional branches.

    Args:
        op: Comparison operator mnemonic (e.g., "LES", "EQU", "FGRE")

    Returns:
        Negated operator mnemonic, or original if not a comparison

    Example:
        negate_comparison_op("LES") -> "GEQ"  # !(a < b) => (a >= b)
        negate_comparison_op("EQU") -> "NEQ"  # !(a == b) => (a != b)
    """
    return COMPARISON_NEGATION.get(op, op)


def negate_condition_expr(expr: str) -> str:
    """
    Negate a condition expression at the text level.

    Handles simple cases by wrapping in !(expr) or removing existing negation.
    For compound conditions, this provides basic negation that can be
    further optimized by simplification passes.

    Args:
        expr: Condition expression string

    Returns:
        Negated expression

    Examples:
        negate_condition_expr("a < b") -> "!(a < b)"
        negate_condition_expr("!(x)") -> "x"
        negate_condition_expr("flag") -> "!flag"
    """
    expr = expr.strip()

    # Remove existing negation: !(expr) => expr
    if expr.startswith("!(") and expr.endswith(")"):
        return expr[2:-1]
    if expr.startswith("!") and not expr[1:].startswith("="):
        # !flag => flag (but not !=)
        return expr[1:]

    # Add negation: expr => !(expr)
    # For simple expressions, wrap in !()
    if " " not in expr or expr.count(" ") <= 2:
        # Simple expression like "flag" or "a < b"
        return f"!({expr})"

    # Complex expression - wrap in !()
    return f"!({expr})"


TYPE_NAMES = {
    opcodes.ResultType.VOID: "void",
    opcodes.ResultType.INT: "int",
    opcodes.ResultType.FLOAT: "float",
    opcodes.ResultType.DOUBLE: "double",
    opcodes.ResultType.POINTER: "void*",
    opcodes.ResultType.SHORT: "short",
    opcodes.ResultType.CHAR: "char",
}


@dataclass
class FormattedExpression:
    text: str
    address: int
    mnemonic: str


class ExpressionFormatter:
    def __init__(self, ssa: SSAFunction, func_start: int = None, func_end: int = None, func_name: str = None, symbol_db=None, func_signature=None, function_bounds=None, rename_map: Dict[str, str] = None, heritage_metadata: Optional[Dict] = None):
        """
        Initialize expression formatter.

        Args:
            ssa: SSA function data
            func_start: Optional start address for function-scoped analysis
            func_end: Optional end address for function-scoped analysis
            func_name: Optional function name for struct field tracking
            symbol_db: Optional symbol database for constant/type resolution
            func_signature: Optional FunctionSignature for parameter name mapping (FÁZE 3.3)
            function_bounds: Optional dict {func_name: (start_addr, end_addr)} for CALL resolution (FÁZE 4)
            rename_map: Optional dict mapping SSA value names → final names (FIX 2 - Variable Collision Resolution)
            heritage_metadata: Optional heritage SSA metadata for improved variable resolution

        When func_start and func_end are provided, structure type detection
        is limited to blocks within that range. This ensures 100% reliable
        field access detection when local_0 is reused for different structures
        in different functions.
        """
        self.ssa = ssa
        self.symbol_db = symbol_db
        self.func_name = func_name
        self._ssa_func = ssa  # Alias for global resolver
        self.data_segment = getattr(ssa, "scr", None).data_segment if getattr(ssa, "scr", None) else None
        self._inline_cache: Dict[str, str] = {}
        self._visiting: set[str] = set()
        self._inline_visiting: set[str] = set()  # Separate set for _inline_expression cycle detection
        self._declared: Set[str] = set()
        self._store_ops = {"ASGN"}
        # Function boundaries for scoped analysis
        self._func_start = func_start
        self._func_end = func_end
        # FÁZE 3.3: Function signature for parameter name mapping
        self._func_signature = func_signature
        # FÁZE 4: Function bounds for CALL instruction resolution
        self._function_bounds = function_bounds or {}
        # FIX 2: Variable name collision resolution (SSA value name → final name)
        self._rename_map = rename_map or {}
        # Build parameter offset -> name mapping
        self._param_names = {}  # frame_base_offset (signed) -> param_name
        self._param_names_by_index = {}  # signature_index (0-based) -> param_name
        self._param_count = 0  # Number of parameters
        self._func_returns_value = False  # Whether function returns a value
        if func_signature and func_signature.param_types:
            n_params = func_signature.param_count
            self._param_count = n_params
            # Determine if function returns a value (affects stack layout)
            self._func_returns_value = (
                func_signature.return_type != "void"
            )
            for i, param_type in enumerate(func_signature.param_types):
                # Extract name from "float time" -> "time", "dword *list" -> "list"
                tokens = param_type.replace('*', ' * ').split()
                param_name = None
                for token in reversed(tokens):
                    if token != '*':
                        param_name = token.lstrip('*')
                        break
                if param_name:
                    self._param_names_by_index[i] = param_name
                    # Stack frame layout (offsets from frame base):
                    #   [sp-1], [sp-2] = reserved (return addr, frame info)
                    #   [sp-3] = return value slot (if non-void) OR last param (if void)
                    #   Parameters in REVERSE order from there:
                    #     void:     [sp-(3+n-1-i)] = param at sig_index i
                    #     non-void: [sp-(4+n-1-i)] = param at sig_index i
                    # Heritage SSA names: param_K where K = abs(frame_offset) - 3
                    base = 4 if self._func_returns_value else 3
                    frame_offset = -(base + n_params - 1 - i)
                    self._param_names[frame_offset] = param_name
        # Track variable -> structure type mapping
        self._var_struct_types: Dict[str, str] = {}
        # Track structure ranges: base_var -> (start_index, end_index, struct_name)
        # If local_0 is a 156-byte struct, local_1-local_38 are its fields
        self._struct_ranges: Dict[str, tuple] = {}  # (start_idx, end_idx, struct_name)
        # Track semantic variable names (local_X -> semantic_name)
        self._semantic_names: Dict[str, str] = {}
        # FÁZE 1.2: Track semantic names already used (prevents i==i collision)
        self._used_semantic_names: Set[str] = set()
        # Counter for disambiguation (e.g., vec, vec2, vec3)
        self._name_counters: Dict[str, int] = {}
        # Global variable names (data offset -> name)
        self._global_names: Dict[int, str] = {}
        # Global variable type information (data offset -> GlobalUsage with types)
        self._global_type_info: Dict[int, 'GlobalUsage'] = {}
        # WORKAROUND: Track recent array loads for fixing PHI aliasing issues
        # Maps instruction address -> array notation (e.g., "data_322[index]")
        self._recent_array_loads: Dict[int, str] = {}
        # Analyze function calls to infer structure types
        self._analyze_struct_types()
        # Assign semantic names to struct base variables
        self._assign_semantic_names()
        # Resolve global variable names and types
        self._resolve_global_names()
        # Initialize constant propagation
        self._constant_propagator = ConstantPropagator(ssa)
        self._constant_propagator.analyze()
        # Initialize field access tracking with function boundaries
        # This ensures struct types detected in one function don't leak to other functions
        self._field_tracker = FieldAccessTracker(ssa, func_name=func_name, func_start=func_start, func_end=func_end)
        self._field_tracker.analyze()
        # Phase 2: Transfer field tracker results to formatter's var_struct_types
        # This enables struct-typed variable declarations for locals
        new_param_types = False
        for var_name, struct_type in self._field_tracker.var_struct_types.items():
            # Only store if not already set (preserve existing mappings)
            if var_name not in self._var_struct_types:
                self._var_struct_types[var_name] = struct_type
                if var_name.startswith("param_"):
                    new_param_types = True
        # Also transfer semantic names from field tracker
        for var_name, sem_name in self._field_tracker.semantic_names.items():
            if var_name not in self._semantic_names:
                self._semantic_names[var_name] = sem_name
        # Re-run parameter name assignment if field tracker found new param struct types
        if new_param_types:
            self._assign_parameter_names()
        # Initialize header database for function signatures
        self._header_db = get_header_database()

        # Initialize SDK constant resolver for replacing magic numbers with named constants
        self._constant_resolver = None
        if self._header_db and self._header_db.sdk_db:
            try:
                from ...sdk.constant_resolver import ConstantResolver
                self._constant_resolver = ConstantResolver(self._header_db.sdk_db)
            except Exception:
                # SDK constant resolver not available, continue without it
                pass

        # LOCAL TYPE TRACKER: Unified tracker for coordinating declarations with usage
        # This is set by the orchestrator after SSA pattern analysis
        self._type_tracker = None

        # Heritage SSA metadata for improved variable resolution
        # Contains variable info and PHI placements from multi-pass heritage analysis
        self._heritage_metadata = heritage_metadata or {}
        self._heritage_vars = heritage_metadata.get("variables", {}) if heritage_metadata else {}

        # Initialize DataResolver for type-aware data segment reading
        # FIXED (Phase 1): Create DataResolver even if _global_type_info is empty
        # The DataResolver can still use heuristic float detection for constants
        if self.data_segment is not None:
            from .data_resolver import DataResolver
            self._data_resolver = DataResolver(
                self.data_segment,
                self._global_type_info,  # May be empty, that's OK
                confidence_threshold=0.70
            )
        else:
            self._data_resolver = None

        # Initialize struct assignment tracker for text annotations
        # Tracks constant assignments to struct fields (e.g., local_80.field0 = 9136)
        # Used by _format_call to annotate functions like SC_MissionSave(&local_80)
        self._struct_text_tracker = StructAssignmentTracker()

    def seed_float_opcode_types(self) -> None:
        """
        Strengthen type evidence for float opcodes before dataflow passes.

        This seeds SSA value_type with float for FADD/FSUB/FMUL/FDIV operands and
        results so downstream type inference has early, concrete evidence.
        """
        for block_insts in self._ssa_func.instructions.values():
            for inst in block_insts:
                if inst.mnemonic not in {"FADD", "FSUB", "FMUL", "FDIV"}:
                    continue
                for value in (inst.inputs or []):
                    if value and value.value_type != opcodes.ResultType.FLOAT:
                        value.value_type = opcodes.ResultType.FLOAT
                for value in (inst.outputs or []):
                    if value and value.value_type != opcodes.ResultType.FLOAT:
                        value.value_type = opcodes.ResultType.FLOAT

    def _resolve_field_name(self, base_var: str, offset: int) -> str:
        """
        Resolve field name from struct type and offset.

        Args:
            base_var: Variable name (e.g., "local_296", "enum_pl", "hudinfo")
            offset: Byte offset into the struct

        Returns:
            Field name if resolved (e.g., "side"), otherwise generic "field_N"
        """
        # Reverse lookup: semantic name -> SSA name
        # _semantic_names maps: SSA_name -> semantic_name
        # We need to find SSA_name from semantic_name
        ssa_name = base_var
        for ssa_n, sem_n in self._semantic_names.items():
            if sem_n == base_var:
                ssa_name = ssa_n
                break

        # Check if we know the struct type for this variable
        struct_type = None

        # PRIORITY 1: Check type_tracker (unified tracker)
        if self._type_tracker:
            info = self._type_tracker.get_usage_info(ssa_name)
            if info and info.struct_type:
                struct_type = info.struct_type

        # PRIORITY 2: Check field_tracker with SSA name
        if not struct_type and self._field_tracker:
            struct_type = self._field_tracker.var_struct_types.get(ssa_name)

        # PRIORITY 3: Check _var_struct_types with SSA name
        if not struct_type:
            struct_type = self._var_struct_types.get(ssa_name)

        # PRIORITY 4: Check with original name (fallback)
        if not struct_type:
            struct_type = self._var_struct_types.get(base_var)

        if not struct_type:
            return f"field_{offset}"

        # Try to resolve field name from struct definition
        field_name = get_verified_field_name(struct_type, offset)
        if field_name:
            return field_name

        # Fallback to generic notation
        return f"field_{offset}"

    def _get_heritage_type(self, var_name: str) -> Optional[str]:
        """
        Get type information from heritage metadata for a variable.

        Heritage SSA provides type information discovered through multi-pass
        analysis that may be more accurate than single-pass inference.

        Args:
            var_name: Variable name (e.g., "local_8", "param_0")

        Returns:
            Type name string if heritage has type info, None otherwise.
        """
        if not self._heritage_vars or var_name not in self._heritage_vars:
            return None

        heritage_info = self._heritage_vars[var_name]
        heritage_type = heritage_info.get("type", "UNKNOWN")

        if heritage_type == "UNKNOWN":
            return None

        # Map heritage type names to C type names
        type_map = {
            "INT": "int",
            "FLOAT": "float",
            "DOUBLE": "double",
            "POINTER": "void*",
            "CHAR": "char",
            "SHORT": "short",
        }

        return type_map.get(heritage_type, None)

    def set_type_tracker(self, tracker):
        """
        Set the LocalVariableTypeTracker for coordinating declarations with usage.

        The type tracker is used to:
        1. Check if array/field notation should be emitted
        2. Record usage patterns discovered during expression formatting

        Args:
            tracker: LocalVariableTypeTracker instance
        """
        self._type_tracker = tracker

    def _analyze_struct_types(self) -> None:
        """
        Analyze XCALL instructions to infer structure types for local variables.

        When we see patterns like:
          SC_P_Create(&local_0)  -> local_0 is s_SC_P_Create
          SC_P_Ai_GetProps(x, &local_1) -> local_1 is s_SC_P_AI_props
          SC_ZeroMem(&local_0, 156) -> local_0 might be s_SC_P_Create (156 bytes)

        When func_start and func_end are set, only analyzes blocks within that range.
        This ensures per-function structure detection for 100% reliability.
        """
        scr = getattr(self.ssa, "scr", None)
        if not scr:
            return

        cfg = self.ssa.cfg

        # Iterate over blocks, filtering by function range if specified
        for block_id, instructions in self.ssa.instructions.items():
            # If function boundaries are specified, filter blocks
            if self._func_start is not None:
                block = cfg.blocks.get(block_id) if cfg else None
                if block:
                    block_addr = block.start
                    # Skip blocks outside function range
                    if block_addr < self._func_start:
                        continue
                    if self._func_end is not None and block_addr > self._func_end:
                        continue
            for inst in instructions:
                if inst.mnemonic != "XCALL":
                    continue

                # Get function name from XFN index (same as _format_call)
                if not inst.instruction or not inst.instruction.instruction:
                    continue

                xfn_idx = inst.instruction.instruction.arg1
                xfn_entry = scr.get_xfn(xfn_idx)
                if not xfn_entry:
                    continue

                # Extract function name from signature
                full_name = xfn_entry.name
                paren_idx = full_name.find("(")
                func_name = full_name[:paren_idx] if paren_idx > 0 else full_name

                # Check for SC_ZeroMem(ptr, size) - infer from size
                if func_name == "SC_ZeroMem" and len(inst.inputs) >= 2:
                    ptr_val = inst.inputs[0]
                    size_val = inst.inputs[1]
                    size = None

                    # Get size from GCP-loaded value (data segment alias like data_X)
                    if size_val.alias and size_val.alias.startswith("data_"):
                        try:
                            offset = int(size_val.alias[5:])
                            byte_offset = offset * 4
                            if self.data_segment:
                                size = self.data_segment.get_dword(byte_offset)
                        except (ValueError, AttributeError):
                            pass

                    if size is not None:
                        # Get variable name from pointer
                        var_name = self._extract_var_from_pointer(ptr_val)
                        if var_name and size in STRUCTURES_BY_SIZE:
                            struct_names = STRUCTURES_BY_SIZE[size]
                            chosen_struct = None
                            if len(struct_names) == 1:
                                chosen_struct = struct_names[0]
                            elif "s_SC_P_Create" in struct_names:
                                # Prefer s_SC_P_Create for 156 bytes
                                chosen_struct = "s_SC_P_Create"
                            elif "s_SC_P_AI_props" in struct_names:
                                chosen_struct = "s_SC_P_AI_props"
                            if chosen_struct:
                                self._var_struct_types[var_name] = chosen_struct
                                self._register_struct_range(var_name, chosen_struct)
                    continue

                # Check for known functions with struct parameters
                struct_type = infer_struct_from_function(func_name, 0)
                if struct_type and len(inst.inputs) >= 1:
                    var_name = self._extract_var_from_pointer(inst.inputs[0])
                    if var_name:
                        self._update_struct_type(var_name, struct_type)

                # Check second parameter
                struct_type = infer_struct_from_function(func_name, 1)
                if struct_type and len(inst.inputs) >= 2:
                    var_name = self._extract_var_from_pointer(inst.inputs[1])
                    if var_name:
                        self._update_struct_type(var_name, struct_type)

    def _assign_semantic_names(self) -> None:
        """
        Assign semantic names to variables detected as structures.

        Mapping:
            s_SC_P_Create -> pinfo, pinfo2, ...
            s_SC_P_getinfo -> player_info, player_info2, ...
            s_SC_OBJ_info -> obj_info, obj_info2, ...
            c_Vector3 -> vec, vec2, vec3, ...
            s_SC_MP_hud -> hudinfo, hudinfo2, ...

        This makes code more readable:
            local_0.side -> pinfo.side
            local_5.x -> vec.x
        """
        # Struct type -> preferred semantic name
        STRUCT_TO_NAME = {
            "s_SC_P_Create": "pinfo",
            "s_SC_P_getinfo": "player_info",
            "s_SC_P_AI_props": "ai_props",
            "s_SC_OBJ_info": "obj_info",
            "s_SC_L_info": "level_info",
            "c_Vector3": "vec",
            "s_sphere": "sphere",
            "s_SC_MP_hud": "hudinfo",
            "s_SC_MP_Recover": "recover",
            "s_SC_MP_EnumPlayers": "enum_pl",
            "s_SC_MP_SRV_settings": "srv_settings",
            "s_SC_MP_SRV_AtgSettings": "atg_settings",
            "s_SC_HUD_MP_icon": "icon",
        }

        for var_name, struct_name in self._var_struct_types.items():
            if struct_name in STRUCT_TO_NAME:
                base_name = STRUCT_TO_NAME[struct_name]

                # Generate unique name with counter if needed
                count = self._name_counters.get(base_name, 0)
                if count == 0:
                    semantic_name = base_name
                else:
                    semantic_name = f"{base_name}{count + 1}"

                self._name_counters[base_name] = count + 1
                self._semantic_names[var_name] = semantic_name

        # Detect loop counters and assign i, j, k names
        self._detect_loop_counters()
        # Assign semantic names to parameters
        self._assign_parameter_names()

    def _should_use_semantic_name(self, var_name: str) -> bool:
        """Check if semantic renaming is allowed for this variable."""
        if not self._type_tracker:
            return True
        return self._type_tracker.should_use_semantic_name(var_name)

    def _detect_loop_counters(self) -> None:
        """
        Detect loop counter variables based on usage patterns.

        A loop counter typically:
        1. Is initialized to 0 or small constant
        2. Is compared with a constant/variable (LES, LEQ, GRE, GEQ)
        3. Is incremented (ADD 1 or INC)
        4. May be used as array index (MUL 4, MUL 16, etc.)

        Assigns names: i, j, k, idx, n (in order of nesting/usage)
        """
        loop_counter_names = ["i", "j", "k", "idx", "n", "m"]
        counter_index = 0

        # Track which variables are candidates for loop counters
        candidates: Dict[str, int] = {}  # var_name -> score

        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                # Pattern 1: Assignment of 0 or small constant
                # ASGN has 2 inputs: (value, address)
                if inst.mnemonic == "ASGN" and len(inst.inputs) == 2:
                    source = inst.inputs[0]  # Value being assigned
                    target = inst.inputs[1]  # Address/target
                    # Check if source is a small constant (0-10)
                    if source.alias and source.alias.startswith("data_"):
                        try:
                            offset = int(source.alias[5:])
                            if self.data_segment:
                                value = self.data_segment.get_dword(offset * 4)
                                if 0 <= value <= 10:
                                    # Target is initialized to small value
                                    if target.alias and target.alias.startswith("local_"):
                                        candidates[target.alias] = candidates.get(target.alias, 0) + 1
                        except (ValueError, AttributeError):
                            pass

                # Pattern 2: Comparison operators
                if inst.mnemonic in ("LES", "LEQ", "GRE", "GEQ", "ULES", "ULEQ"):
                    for inp in inst.inputs:
                        if inp.alias and inp.alias.startswith("local_"):
                            candidates[inp.alias] = candidates.get(inp.alias, 0) + 2

                # Pattern 3: Increment operations
                if inst.mnemonic in ("INC", "ADD"):
                    # Check for ADD with 1
                    if inst.mnemonic == "ADD" and len(inst.inputs) == 2:
                        # Check if one operand is constant 1
                        for inp in inst.inputs:
                            if inp.alias and inp.alias.startswith("local_"):
                                other_inp = inst.inputs[1] if inst.inputs[0] == inp else inst.inputs[0]
                                # Check if other input is 1
                                if other_inp.alias and other_inp.alias.startswith("data_"):
                                    try:
                                        offset = int(other_inp.alias[5:])
                                        if self.data_segment:
                                            value = self.data_segment.get_dword(offset * 4)
                                            if value == 1:
                                                candidates[inp.alias] = candidates.get(inp.alias, 0) + 3
                                    except (ValueError, AttributeError):
                                        pass
                    elif inst.mnemonic == "INC":
                        for inp in inst.inputs:
                            if inp.alias and inp.alias.startswith("local_"):
                                candidates[inp.alias] = candidates.get(inp.alias, 0) + 3

                # Pattern 4: Used in multiplication (array indexing)
                if inst.mnemonic in ("MUL", "CMUL"):
                    for inp in inst.inputs:
                        if inp.alias and inp.alias.startswith("local_"):
                            candidates[inp.alias] = candidates.get(inp.alias, 0) + 1

        # Sort candidates by score (highest first)
        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)

        # Assign names to top candidates
        for var_name, score in sorted_candidates:
            if score >= 3 and counter_index < len(loop_counter_names):  # Threshold of 3
                # Skip if already has a semantic name (struct field)
                if var_name not in self._semantic_names:
                    counter_name = loop_counter_names[counter_index]
                    self._semantic_names[var_name] = counter_name
                    counter_index += 1

        # Propagate loop counter names to variables used in array indexing
        # Pattern: Find ALL locals/params used in MUL operations (array indexing)
        # If one has a semantic name, all should have the same name
        index_vars: set[str] = set()
        semantic_index_vars: Dict[str, str] = {}  # var -> semantic_name

        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                # Find MUL operations (used for array indexing: index * element_size)
                if inst.mnemonic == "MUL" and len(inst.inputs) == 2:
                    for inp in inst.inputs:
                        if inp.alias and inp.alias.startswith("local_"):
                            index_vars.add(inp.alias)
                            if inp.alias in self._semantic_names:
                                semantic_index_vars[inp.alias] = self._semantic_names[inp.alias]

        # Propagate: if any index variable has a semantic name, give it to all index variables
        if semantic_index_vars:
            # Use the first semantic name found
            semantic_name = next(iter(semantic_index_vars.values()))
            for var in index_vars:
                if var not in self._semantic_names:
                    self._semantic_names[var] = semantic_name

        # Additional propagation: Find param_ variables used in arithmetic with loop-counter-like patterns
        # Pattern: param_X appears in FSUB/SUB with loaded values (DCP results) - likely a loop counter too
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                if inst.mnemonic in ("SUB", "FSUB", "ADD", "FADD") and len(inst.inputs) == 2:
                    for inp in inst.inputs:
                        if inp.alias and inp.alias.startswith("param_"):
                            continue

    def _assign_parameter_names(self) -> None:
        """
        Assign semantic names to function parameters based on usage.

        For parameters detected as struct pointers, use appropriate names.
        Special handling for common patterns:
        - ScriptMain param -> "info" (s_SC_NET_info*)
        - Object script param -> "obj_info" (s_SC_OBJ_info*)
        """
        # Check param variables in var_struct_types
        for var_name, struct_name in list(self._var_struct_types.items()):
            if not var_name.startswith("param_"):
                continue

            # Map parameter struct types to semantic names
            PARAM_STRUCT_TO_NAME = {
                "s_SC_NET_info": "info",
                "s_SC_OBJ_info": "info",
                "s_SC_L_info": "info",
                "s_SC_P_getinfo": "plinfo",
            }

            if struct_name in PARAM_STRUCT_TO_NAME:
                semantic_name = PARAM_STRUCT_TO_NAME[struct_name]
                self._semantic_names[var_name] = semantic_name

    def _resolve_global_names(self) -> None:
        """
        Použije global_resolver k detekci a pojmenování globálních proměnných.
        Také načte type information pro type-aware data segment reading.
        """
        try:
            from .global_resolver import resolve_globals_with_types
            # Cache the global resolution on the SSA function to avoid re-computing for every function
            # This is expensive and the results are the same for all functions in the same file
            if not hasattr(self._ssa_func, '_cached_global_type_info_bytes'):
                self._ssa_func._cached_global_type_info_bytes = resolve_globals_with_types(self._ssa_func, symbol_db=self.symbol_db)
            global_type_info_bytes = self._ssa_func._cached_global_type_info_bytes

            # Convert byte offsets to DWORD offsets for easier usage
            # GlobalResolver uses byte offsets (4, 1288, etc.), but stack_lifter generates
            # aliases like data_1, data_322 where the number is a DWORD offset
            self._global_type_info = {offset // 4: usage for offset, usage in global_type_info_bytes.items()}

            # Extract just names for backward compatibility (also convert to DWORD offsets)
            self._global_names = {offset: usage.name for offset, usage in self._global_type_info.items() if usage.name}
        except Exception as e:
            # Pokud selže global resolution, pokračuj bez něj
            import sys
            import traceback
            # print(f"\n[DEBUG expr.py:630] Global name resolution FAILED!", file=sys.stderr)
            # print(f"  Exception: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            self._global_names = {}
            self._global_type_info = {}

    def _extract_var_from_pointer(self, value: SSAValue) -> Optional[str]:
        """Extract variable name from pointer/address value."""
        # If it has an alias like &local_0, extract local_0
        if value.alias and value.alias.startswith("&"):
            return value.alias[1:]  # Remove & prefix
        # Check producer instruction
        if value.producer_inst:
            if value.producer_inst.mnemonic in {"LADR", "GADR"}:
                # Local/global address - use first output's alias
                for out in value.producer_inst.outputs:
                    if out.alias and out.alias.startswith("&"):
                        return out.alias[1:]
        return None

    def _update_struct_type(self, var_name: str, struct_name: str) -> None:
        """
        Update structure type for a variable, preferring larger structures.

        When the same variable is used for different structures in different
        functions (compiler reuses stack space), prefer the larger structure
        as it provides more complete field information.
        """
        new_struct = get_struct_by_name(struct_name)
        if not new_struct:
            return

        existing = self._var_struct_types.get(var_name)
        if existing:
            existing_struct = get_struct_by_name(existing)
            if existing_struct and existing_struct.size >= new_struct.size:
                return  # Keep existing larger structure

        self._var_struct_types[var_name] = struct_name
        self._register_struct_range(var_name, struct_name)

    def _register_struct_range(self, var_name: str, struct_name: str) -> None:
        """
        Register a structure range for field access detection.

        When local_0 is detected as a 156-byte struct (s_SC_P_Create),
        local_1 through local_38 are its fields (156 / 4 - 1 = 38 slots).
        """
        if not var_name.startswith("local_"):
            return  # Only track local variables

        struct_def = get_struct_by_name(struct_name)
        if not struct_def:
            return

        try:
            base_idx = int(var_name.split("_")[1])
        except (ValueError, IndexError):
            return

        # Calculate how many local slots this structure occupies
        slot_count = struct_def.size // 4
        if slot_count <= 1:
            return  # No fields to map

        end_idx = base_idx + slot_count - 1
        self._struct_ranges[var_name] = (base_idx, end_idx, struct_name)

    def _get_struct_field(self, base_var: str, offset: int) -> Optional[str]:
        """Get structure field name for variable at offset."""
        struct_name = self._var_struct_types.get(base_var)
        if not struct_name:
            return None
        return get_verified_field_name(struct_name, offset)

    def _get_semantic_name(self, var_name: str) -> str:
        """
        FIX (01-21): Get the semantic name for a variable, if one exists.

        This ensures struct field accesses use semantic names like atg_settings.field
        instead of local_1.field when the variable has been given a semantic name.

        Args:
            var_name: Variable name (e.g., "local_1", "&local_1")

        Returns:
            Semantic name if available (e.g., "atg_settings"), otherwise the original name
        """
        # Handle address-of prefix
        is_address = var_name.startswith("&")
        base_name = var_name[1:] if is_address else var_name

        # Check if there's a semantic name for this variable
        semantic_name = self._semantic_names.get(base_name)
        if semantic_name:
            if not self._should_use_semantic_name(base_name):
                return f"&{base_name}" if is_address else base_name
            return f"&{semantic_name}" if is_address else semantic_name

        return var_name

    def _get_field_base_name(self, base_name: str, field_name: str) -> str:
        """Return a display name for field access, using semantic name when available."""
        # First try semantic name lookup
        result = self._get_semantic_name(base_name)
        # If semantic name didn't remap, also try parameter alias remapping
        # This handles param_0 -> pinfo when the function signature names the param
        if result == base_name:
            result = self._remap_param_alias(base_name)
        return result

    def _get_struct_field_for_local(self, alias: str) -> Optional[str]:
        """
        Check if local_X is a field of a detected structure and return formatted name.

        If local_0 is s_SC_P_Create (156 bytes), then:
        - local_1 (offset 4) -> local_0.side
        - local_2 (offset 8) -> local_0.group
        etc.

        Also handles address aliases like &local_1 -> &local_0.side
        """
        # Handle both local_X and &local_X
        is_address = alias.startswith("&")
        local_alias = alias[1:] if is_address else alias

        if not local_alias.startswith("local_"):
            return None

        try:
            idx = int(local_alias.split("_")[1])
        except (ValueError, IndexError):
            return None

        # Check if this index falls within any structure range
        for base_var, (start_idx, end_idx, struct_name) in self._struct_ranges.items():
            # Check if this is the base variable itself (local_0 -> use semantic name)
            if idx == start_idx:
                # Return semantic name for base variable if available
                semantic_name = self._semantic_names.get(base_var, None)
                if semantic_name:
                    return f"&{semantic_name}" if is_address else semantic_name
                continue
            # Check if within range (field of struct)
            if start_idx < idx <= end_idx:
                # Calculate byte offset from base
                offset = (idx - start_idx) * 4
                field_name = self._resolve_field_name(base_var, offset)
                if field_name:
                    # Use semantic name if available, otherwise fallback to base_var
                    display_name = self._get_field_base_name(base_var, field_name)
                    result = f"{display_name}.{field_name}"
                    return f"&{result}" if is_address else result

        return None

    def _value_name(self, value: SSAValue) -> str:
        return value.alias or value.name

    def _can_inline(self, value: SSAValue) -> bool:
        # Allow inlining of temporary variables (t_X pattern)
        # But not user variables (local_X, data_X, param_X, etc.)
        var_name = value.alias or value.name
        if var_name:
            # Check if this is a user-visible variable that should NOT be inlined
            if (var_name.startswith("local_") or var_name.startswith("data_") or
                var_name.startswith("param_") or var_name.startswith("&")):
                # User-visible variable - don't inline
                return False
            # Temporary variables (t_X) and SSA names can be inlined

        if value.phi_sources:
            return False
        inst = value.producer_inst
        if inst is None or not inst.outputs or len(inst.outputs) != 1:
            return False
        if inst.mnemonic == "PHI":
            return False

        # Allow multi-use inlining for:
        # 1. Comparison operations (used in conditions)
        # 2. Simple operations (CAST, ADD with constants) - SSA may count uses incorrectly
        # 3. Address/pointer operations (PNT, DCP) - always inline
        if len(value.uses) != 1:
            # Always inline comparisons
            if inst.mnemonic in COMPARISON_OPS:
                pass  # Allow
            # Allow inlining simple casts and arithmetic with small operands
            elif inst.mnemonic in CAST_OPS:
                pass  # Allow - casts are simple
            elif inst.mnemonic in INFIX_OPS and len(value.uses) <= 10:
                # Allow inlining simple arithmetic if used ≤10 times
                # (SSA may count incorrectly due to dead code or loop unrolling)
                pass  # Allow
            # Always inline pointer operations (struct field access patterns)
            elif inst.mnemonic in {"PNT", "DCP"}:
                pass  # Allow - pointer expressions should always inline
            # Always inline address load operations
            elif inst.mnemonic in {"LADR", "GADR", "DADR"}:
                pass  # Allow - address expressions should always inline
            else:
                return False

        if inst.mnemonic in INFIX_OPS or inst.mnemonic in UNARY_PREFIX:
            return True
        if inst.mnemonic in CAST_OPS:
            return True
        # Comparison operations - always inline
        if inst.mnemonic in COMPARISON_OPS:
            return True
        # Address load instructions - inline by rendering alias directly
        if inst.mnemonic in {"LADR", "GADR", "DADR"}:
            return True
        # PNT (pointer arithmetic) - inline to show pointer expression
        if inst.mnemonic == "PNT":
            return True
        # DCP (dereference/load) - inline to show dereferenced value
        if inst.mnemonic == "DCP":
            return True
        # XCALL/CALL return values with single use should be inlined
        # This prevents duplicate function calls (standalone XCALL + inlined use)
        if inst.mnemonic in {"XCALL", "CALL"}:
            # Only inline if exactly 1 real use (positive addresses are actual code locations)
            real_uses = sum(1 for addr, _ in value.uses if addr >= 0)
            if real_uses == 1:
                return True
        return False

    def _load_literal(self, alias: str, value_type: opcodes.ResultType = opcodes.ResultType.UNKNOWN, expected_type_str: str = None, context: ExpressionContext = None) -> Optional[str]:
        """
        Load literal value from data segment (REFACTORED to use DataResolver).

        Args:
            alias: Data reference (e.g., 'data_322' or '&data_322')
            value_type: Opcode result type hint (legacy, mostly unused now)
            expected_type_str: Explicit type hint (from function signature)
            context: Expression context (e.g., IN_ARRAY_INDEX forces integer rendering)

        Returns:
            Formatted value string or None if not a data reference
        """
        if not self.data_segment:
            return None

        # Parse data offset from alias
        is_address, offset = self._parse_data_offset(alias)
        if offset is None:
            return None

        # Override expected_type based on context
        # Context-aware type inference: array indices MUST be integers
        if context == ExpressionContext.IN_ARRAY_INDEX and not expected_type_str:
            expected_type_str = 'int'  # Force integer rendering for array indices

        # Use DataResolver if available (Fáze 2)
        if self._data_resolver:
            return self._data_resolver.resolve_value(
                offset=offset,
                expected_type=expected_type_str,
                is_address=is_address
            )

        # Fallback to legacy logic if DataResolver not initialized
        # (This shouldn't happen normally, but provides backward compatibility)
        byte_offset = offset * 4
        val = self.data_segment.get_dword(byte_offset)

        # Simple numeric fallback
        if val > 0x7FFFFFFF:
            val = val - 0x100000000
        return str(val)

    def _parse_data_offset(self, alias: str) -> Tuple[bool, Optional[int]]:
        """
        Parse data offset from alias string.

        Args:
            alias: Data reference string (e.g., 'data_322', '&data_322')

        Returns:
            Tuple of (is_address, offset) or (False, None) if not a data reference
        """
        # Support both formats: "data_X" and "&data_X"
        is_address = alias.startswith("&data_")
        prefix_len = 6 if is_address else 5

        if not (alias.startswith("&data_") or alias.startswith("data_")):
            return False, None

        try:
            offset = int(alias[prefix_len:])
            return is_address, offset
        except ValueError:
            return False, None

    def render_value(
        self,
        value: SSAValue,
        expected_type_str: str = None,
        context: ExpressionContext = ExpressionContext.IN_EXPRESSION,
        parent_operator: Optional[str] = None
    ) -> str:
        return self._render_value(value, expected_type_str=expected_type_str, context=context, parent_operator=parent_operator)

    def _try_resolve_constant(self, value: SSAValue, int_value: int) -> Optional[str]:
        """
        Try to resolve an integer value to an SDK constant name.

        Uses context from:
        1. Value metadata (function parameter context)
        2. Variable name patterns
        3. Struct field access patterns

        Args:
            value: SSA value being rendered
            int_value: Integer value to resolve

        Returns:
            Constant name or None
        """
        if not self._constant_resolver:
            return None

        # Strategy 1: Check if value has SDK parameter context metadata
        # (This is set during XCALL processing in stack_lifter.py)
        if hasattr(value, 'metadata') and 'sdk_param_context' in value.metadata:
            func_name, param_index = value.metadata['sdk_param_context']
            const_name = self._constant_resolver.resolve_from_function_param(
                int_value, func_name, param_index
            )
            if const_name:
                return const_name

        # Strategy 2: Check if value comes from struct field access
        # e.g., info->message = 0 → SC_LEV_MES_TIME
        field_expr = self._field_tracker.get_field_expression(value)
        if field_expr and '->' in field_expr:
            # Parse "struct_var->field" or "struct_var.field"
            parts = field_expr.replace('->', '.').split('.')
            if len(parts) == 2:
                base_var, field_name = parts
                # Try to get struct type from field tracker
                struct_type = self._field_tracker.var_struct_types.get(base_var)
                if struct_type:
                    const_name = self._constant_resolver.resolve_from_struct_field(
                        int_value, struct_type, field_name
                    )
                    if const_name:
                        return const_name

        # Strategy 3: Infer from variable name in the value's alias
        if value.alias and (value.alias.startswith('local_') or value.alias.startswith('param_')):
            # Check if this variable has a semantic name
            semantic_name = self._semantic_names.get(value.alias)
            if semantic_name:
                context = self._constant_resolver.infer_context_from_variable_name(semantic_name)
                if context:
                    const_name = self._constant_resolver.resolve_constant(int_value, context)
                    if const_name:
                        return const_name

        return None

    def _find_array_load_in_chain(self, value: SSAValue, depth: int = 0) -> Optional[str]:
        """
        Recursively search for DCP(array_pattern) in the value's producer chain.
        This handles cases where array load is hidden behind PHI or other operations.
        """
        if depth > 5:  # Limit recursion
            return None

        if not value or not value.producer_inst:
            return None

        inst = value.producer_inst

        # If this is a DCP, check if it loads from an array
        if inst.mnemonic == "DCP" and len(inst.inputs) > 0:
            array_notation = self._detect_array_indexing(inst.inputs[0])
            if array_notation:
                return array_notation

        # If this is a PHI, check all inputs
        if inst.mnemonic == "PHI" and len(inst.inputs) > 0:
            for phi_input in inst.inputs:
                result = self._find_array_load_in_chain(phi_input, depth + 1)
                if result:
                    return result

        return None

    def _is_constant_array_notation(self, array_notation: str) -> bool:
        """Check if array notation uses a constant index (e.g., arr[0])."""
        if not array_notation:
            return False
        return bool(re.match(r"^.+\[\s*-?\d+\s*\]", array_notation))

    def _render_value(
        self,
        value: SSAValue,
        expected_type_str: str = None,
        context: ExpressionContext = ExpressionContext.IN_EXPRESSION,
        parent_operator: Optional[str] = None
    ) -> str:
        # CYCLE DETECTION: Prevent infinite recursion on circular PHI references
        # PHI A → PHI B → PHI A would cause unbounded recursion without this check
        # Uses the same _visiting set as _inline_expression for consistency
        if value and value.name:
            if value.name in self._visiting:
                # Cycle detected - return the variable name or alias to break the loop
                if value.alias:
                    return value.alias
                return value.name
            self._visiting.add(value.name)
        else:
            # No value or no name - can't track, proceed without cycle detection
            pass

        try:
            return self._render_value_impl(value, expected_type_str, context, parent_operator)
        finally:
            # Always remove from visiting set when done
            if value and value.name and value.name in self._visiting:
                self._visiting.discard(value.name)

    def _render_value_impl(
        self,
        value: SSAValue,
        expected_type_str: str = None,
        context: ExpressionContext = ExpressionContext.IN_EXPRESSION,
        parent_operator: Optional[str] = None
    ) -> str:
        # PRIORITY -1: Inline comparison operations when used in conditions
        # This ensures "if (tmp)" becomes "if (x > y)" instead of variable name
        if context == ExpressionContext.IN_CONDITION and value.producer_inst and value.producer_inst.mnemonic in COMPARISON_OPS:
            return self._inline_expression(value, context, parent_operator)

        # PRIORITY 0: Inline XCALL/CALL return values for nested function calls
        # This enables patterns like: SC_AnsiToUni(SC_P_GetName(x), y)
        # MUST come before rename_map check, otherwise t2998_ret gets renamed to tmp109
        # and we lose the ability to inline it
        # BUT only inline when used once (as function argument) - if result is stored
        # to a variable and reused, don't inline to avoid duplicate function calls
        if value.producer_inst and value.producer_inst.mnemonic in {"XCALL", "CALL"}:
            # Count only "real" uses (positive addresses are actual code locations,
            # negative addresses are PHI/block boundary markers from SSA construction)
            real_uses = sum(1 for addr, _ in value.uses if addr >= 0)
            if real_uses == 1:
                return self._inline_expression(value, context, parent_operator)

        # PRIORITY 1: Check if value represents struct field access (ABSOLUTE HIGHEST)
        # This MUST come before rename_map to preserve field expressions like "ai_props.watchfulness"
        # Otherwise, if rename_map contains {"t456_0": "j"}, we'd return "j" and lose field access
        field_expr = self._field_tracker.get_field_expression(value)
        if field_expr:
            return field_expr  # Return field expression (e.g., "info->master_nod", "ai_props.watchfulness_zerodist")

        # Preserve constant array loads before rename_map (e.g., dist[1] = dist[0])
        array_load = self._find_array_load_in_chain(value)
        if array_load and self._is_constant_array_notation(array_load):
            return array_load

        # PRIORITY 1.5: Preserve global names for data segment references
        if value.alias:
            if value.alias.startswith("data_"):
                try:
                    offset = int(value.alias[5:])
                    global_name = self._global_names.get(offset)
                    if global_name:
                        return global_name
                except ValueError:
                    pass
            elif value.alias.startswith("&data_"):
                try:
                    offset = int(value.alias[6:])
                    # FIX: Check if this address points to a string literal BEFORE
                    # returning a global name. GADR data[X] where data[X] is a string
                    # should render as "string" not &gVar.
                    string_literal = self._check_string_literal(value)
                    if string_literal:
                        return string_literal
                    global_name = self._global_names.get(offset)
                    if global_name:
                        return f"&{global_name}"
                except ValueError:
                    pass

        # PRIORITY 1.6: Render literals/constants directly to avoid tmp renaming
        literal_constant = self._get_literal_constant_text(
            value,
            expected_type_str=expected_type_str,
            context=context,
        )
        if literal_constant is not None:
            return literal_constant

        constant_value = self._constant_propagator.get_constant(value)
        if constant_value is not None:
            return self._format_constant_value(constant_value, expected_type_str, context)

        # Inline eval-stack copies produced by LCP
        if value.producer_inst and value.producer_inst.mnemonic == "LCP" and value.producer_inst.inputs:
            return self._render_value(
                value.producer_inst.inputs[0],
                expected_type_str=expected_type_str,
                context=context,
                parent_operator=parent_operator,
            )

        # FÁZE 3.3: Check if value is a function parameter (VERY HIGH PRIORITY)
        if value.producer_inst and value.producer_inst.mnemonic == "LCP":
            # Get the original stack offset from the instruction
            orig_instr = value.producer_inst.instruction
            if orig_instr and orig_instr.instruction:
                stack_offset = orig_instr.instruction.arg1

                # Convert unsigned to signed if necessary (two's complement)
                if stack_offset >= 0x80000000:
                    stack_offset = stack_offset - 0x100000000

                # Check if this offset corresponds to a function parameter
                if stack_offset in self._param_names:
                    param_name = self._param_names[stack_offset]
                    return param_name

        # PRIORITY 2: Check rename_map for variable collision resolution
        # Must check SSA value NAME (t123_0, t456_0), NOT alias (local_2)!
        # This allows sideA and sideB to have different names even though both have alias="local_2"
        # NOTE: This comes AFTER field_expr check to avoid losing struct field accesses
        # BUGFIX: Skip rename_map for LADR values - these produce address-of expressions (&local_X)
        # that should preserve the original variable name for proper struct type detection
        # FIX (01-20): Also skip rename_map for ADD values that are array indexing patterns
        # Pattern: ADD(GADR, MUL(...)) should be inlined as &array[index], not renamed to tmpN
        # FIX (01-21): Skip rename_map for GCP values that load constants from data segment
        # These should resolve to their actual constant values, not renamed tmpN variables
        is_ladr = value.producer_inst and value.producer_inst.mnemonic == "LADR"
        is_gcp_constant = value.producer_inst and value.producer_inst.mnemonic == "GCP" and value.alias and value.alias.startswith("data_")
        is_parametric_alias = value.alias and self._is_parametric_alias(value.alias)
        # FIX: Skip rename_map for CAST_OPS (ITOF, FTOI, etc.) - these should inline to show
        # the actual value being cast, not a temp variable like "tmp3"
        is_cast_op = value.producer_inst and value.producer_inst.mnemonic in CAST_OPS
        # FIX Issue 5: Skip rename_map for INFIX_OPS (ADD, SUB, MUL, etc.) that can be inlined
        # These should render as expressions like "gSteps - 1", not "tmp"
        # BUT: only bypass when the rename_map gives a generic temp name (tmpN, ptrN, objN).
        # If the renamed value is meaningful (local_X, param_X, gVarName), keep it.
        is_infix_op = False
        if value.producer_inst and value.producer_inst.mnemonic in INFIX_OPS:
            if self._rename_map and value.name in self._rename_map:
                renamed = self._rename_map[value.name]
                # Only bypass for generic temp names that would be less readable
                # than the inlined expression (e.g., "tmp5" → "gSteps - 1")
                # Patterns: tmpN, ptrN, objN, tNNN_ (raw SSA names), single letters (i, j, k)
                if re.match(r'^(tmp|ptr|obj)\d*$', renamed):
                    is_infix_op = True
                elif re.match(r'^t\d+_$', renamed):
                    # Raw SSA name like t290_ - bypass to inline expression
                    is_infix_op = True
                elif re.match(r'^[a-z]$', renamed):
                    is_infix_op = True
                # Otherwise keep the meaningful renamed value
            else:
                # No rename entry - will fall through to inline rendering anyway
                is_infix_op = True
        is_array_indexing = False
        if value.producer_inst and value.producer_inst.mnemonic == "ADD" and len(value.producer_inst.inputs) >= 2:
            left = value.producer_inst.inputs[0]
            right = value.producer_inst.inputs[1]
            # Check if left is GADR/DADR (global/data address) and right is MUL (index * size)
            if left.producer_inst and left.producer_inst.mnemonic in {"GADR", "DADR"}:
                if right.producer_inst and right.producer_inst.mnemonic in {"MUL", "IMUL"}:
                    is_array_indexing = True
        preserve_compound = bool(getattr(value, "metadata", {}).get("preserve_compound"))
        if (self._rename_map and value.name in self._rename_map and not is_ladr and not is_array_indexing
                and not is_gcp_constant and not preserve_compound and not is_parametric_alias and not is_cast_op
                and not is_infix_op):
            return _strip_ssa_version_suffix(self._rename_map[value.name])

        # NEW: Check if value is a string literal from data segment (VERY HIGH PRIORITY)
        string_literal = self._check_string_literal(value)
        if string_literal:
            return string_literal  # Return escaped string literal (e.g., "\"EndRule unsopported: %d\"")

        # REMOVED: Constant symbol substitution causes more problems than it solves
        # - It replaces array indices with unrelated constants (e.g., gData[1] -> gData[SCM_BOOBYTRAPFOUND])
        # - It uses singleplayer constants in multiplayer scripts
        # - The context-free matching is unreliable
        # Keep only function argument substitution via _substitute_constant()

        # PHI resolution: If value comes from PHI with single input, use that input directly
        if value.producer_inst and value.producer_inst.mnemonic == "PHI":
            phi = value.producer_inst

            # PHASE 3: Handle empty/undefined PHI nodes
            # These represent variables that are used but never assigned in all paths
            if len(phi.inputs) == 0:
                # Empty PHI - return a sensible default based on expected type
                if expected_type_str:
                    if 'float' in expected_type_str.lower() and '*' not in expected_type_str:
                        return "0.0f"  # Undefined float
                    elif '*' in expected_type_str:
                        return "0"  # NULL pointer
                # Default to 0 for undefined values
                return "0"

            if len(phi.inputs) == 1:
                # Single input PHI - use the input value directly
                return self._render_value(phi.inputs[0], expected_type_str)
            elif len(phi.inputs) > 1:
                # Multiple inputs - try to find if all inputs are the same
                rendered_inputs = [self._render_value(inp, expected_type_str) for inp in phi.inputs]
                unique_inputs = set(rendered_inputs)
                if len(unique_inputs) == 1:
                    # All inputs are the same - use that value
                    return rendered_inputs[0]

                # WORKAROUND: Broken PHI - prefer local_X or most reasonable value
                # If one input has local_X or param_X alias (not &local_X), prefer it
                for inp in phi.inputs:
                    if inp.alias and (inp.alias.startswith("local_") or inp.alias.startswith("param_")) and not inp.alias.startswith("&"):
                        return self._render_value(inp, expected_type_str)

                # Otherwise use first input
                return self._render_value(phi.inputs[0], expected_type_str)

        # Special handling for DCP (dereference/load) - derive value from input address
        if value.producer_inst and value.producer_inst.mnemonic == "DCP":
            if len(value.producer_inst.inputs) > 0:
                addr_value = value.producer_inst.inputs[0]
                # Check if the address is an array indexing pattern
                array_notation = self._detect_array_indexing(addr_value)
                if array_notation:
                    # Return array load notation instead of alias
                    return array_notation

        # Check if this value has an array load somewhere in its producer chain
        # This handles PHI nodes that wrap DCP operations
        array_load = self._find_array_load_in_chain(value)
        if array_load:
            return array_load

        if value.alias:
            # Preserve constant expressions (e.g., 8 * 60) when safely reconstructable
            if value.producer_inst and self._can_render_constant_expression(value):
                return self._inline_expression(value, context, parent_operator)

            # PRIORITY 2: Check if alias is a numeric literal that might be a float
            try:
                val = int(value.alias)

                # PRIORITY 2a: Explicit type hint takes precedence
                if expected_type_str:
                    # POINTER NULL CHECK: If expected type is a pointer and value is 0,
                    # render as "0" (NULL pointer) instead of "0.0f"
                    # This fixes cases like SC_SpeechRadio2(speech, 0) where 0 is NULL for *float
                    if '*' in expected_type_str and val == 0:
                        return "0"  # NULL pointer
                    if 'float' in expected_type_str.lower() and '*' not in expected_type_str:
                        # Only convert to float literal if NOT a pointer
                        return _format_float(val)
                    if 'int' in expected_type_str.lower() or 'dword' in expected_type_str.lower():
                        # Try SDK constant resolution before returning plain integer
                        if self._constant_resolver and self._constant_resolver.should_resolve_constant(val):
                            # Try to infer context from value metadata
                            const_name = self._try_resolve_constant(value, val)
                            if const_name:
                                return const_name
                        return str(val)

                # PRIORITY 2b: Expression context (context-aware type inference)
                # Force integer rendering in contexts where integers are required
                if context in (ExpressionContext.IN_ARRAY_INDEX,):
                    # Array indices MUST be integers in C
                    return str(val)

                # PRIORITY 2c: Check SSA value_type - if INT, render as integer
                # This prevents 0 from becoming 0.0f when the value is known to be int
                if value.value_type == opcodes.ResultType.INT:
                    # Try SDK constant resolution first
                    if self._constant_resolver and self._constant_resolver.should_resolve_constant(val):
                        const_name = self._try_resolve_constant(value, val)
                        if const_name:
                            return const_name
                    return str(val)

                # PRIORITY 2d: SDK constant resolution (before float heuristic)
                # Try to resolve small integers to named constants
                if self._constant_resolver and self._constant_resolver.should_resolve_constant(val):
                    const_name = self._try_resolve_constant(value, val)
                    if const_name:
                        return const_name

                # PRIORITY 2e: Float heuristic (fallback for general contexts)
                if _is_likely_float(val):
                    return _format_float(val)

                return str(val)
            except ValueError:
                pass

            # PRIORITY 3: Check if local_X is a field of a detected structure
            struct_field = self._get_struct_field_for_local(value.alias)
            if struct_field:
                return struct_field

            # PRIORITY 4: Check for semantic name (loop counter, struct base, etc.)
            # Handle both local_X and &local_X
            var_to_check = value.alias
            is_address_of = False
            if var_to_check.startswith("&"):
                var_to_check = var_to_check[1:]
                is_address_of = True

            if var_to_check.startswith("local_") or var_to_check.startswith("param_"):
                semantic_name = self._semantic_names.get(var_to_check)
                if semantic_name:
                    if not self._should_use_semantic_name(var_to_check):
                        return f"&{var_to_check}" if is_address_of else var_to_check
                    # FÁZE 1.2: Check uniqueness - prevent i==i collision
                    if semantic_name not in self._used_semantic_names:
                        self._used_semantic_names.add(semantic_name)
                        return f"&{semantic_name}" if is_address_of else semantic_name
                    # Name collision - fallback to var_to_check

            # PRIORITY 5: Load literal from data segment (LAST RESORT)
            # Only used if no global name was found
            literal = self._load_literal(value.alias, value.value_type, expected_type_str=expected_type_str, context=context)
            if literal is not None:
                return literal

            # PHASE 3: Check for undefined tmp variables from broken PHI chains
            # These are tmp variables that have no real definition (only PHI/LCP/GCP producers)
            # and should be replaced with a sensible default to avoid compilation errors
            if value.alias.startswith("tmp") and self._is_undefined_value(value):
                if expected_type_str:
                    if 'float' in expected_type_str.lower() and '*' not in expected_type_str:
                        return "0.0f"  # Undefined float
                    elif '*' in expected_type_str:
                        return "0"  # NULL pointer
                # Default to 0 for undefined values
                return "0"

            # FIX Issue 5: Try to inline tmp variables to their source expressions
            # Before returning the raw alias "tmp", check if we can inline the expression
            # Example: tmp = gSteps - 1 should render as "gSteps - 1" not "tmp"
            if value.alias.startswith("tmp") and self._can_inline(value):
                inlined = self._inline_expression(value, context, parent_operator)
                if inlined and inlined != value.alias:
                    return inlined

            return _strip_ssa_version_suffix(value.alias)
        if self._can_inline(value):
            return self._inline_expression(value, context, parent_operator)
        return _strip_ssa_version_suffix(value.name)

    def _is_undefined_value(self, value: SSAValue) -> bool:
        """
        PHASE 3: Check if a value is undefined (used but never assigned).

        This detects broken PHI outputs and variables from invalid SSA construction
        that would cause compilation errors if used directly.

        Returns True if the value has no real definition traceable through its
        producer chain (only PHI/LCP/GCP nodes with no real assignments).
        """
        # Track visited values to prevent infinite loops on cyclic PHI chains
        visited = set()

        def has_real_definition(val: SSAValue) -> bool:
            if val is None:
                return False
            val_id = id(val)
            if val_id in visited:
                return False  # Cyclic reference - no real definition found
            visited.add(val_id)

            if not val.producer_inst:
                # No producer instruction - check if alias is a literal
                if val.alias and (val.alias.lstrip('-').isdigit() or
                                  val.alias.startswith("data_") or
                                  val.alias.startswith("local_") or
                                  val.alias.startswith("param_")):
                    return True  # Has a known source (literal or variable)
                return False  # Unknown - undefined

            mnemonic = val.producer_inst.mnemonic

            # Real assignments that provide values
            if mnemonic in {"ASGN", "XCALL", "CALL", "ADD", "SUB", "MUL", "DIV",
                           "FADD", "FSUB", "FMUL", "FDIV",
                           "GLD", "LLD", "DCP", "LADR", "GADR",
                           "ITOF", "FTOI", "INC", "DEC", "NEG", "FNEG",
                           "EQU", "NEQ", "LES", "LEQ", "GRE", "GEQ",
                           "FLES", "FLEQ", "FGRE", "FGEQ"}:
                return True

            # PHI nodes - check if any input has a real definition
            if mnemonic == "PHI":
                for inp in val.producer_inst.inputs:
                    if has_real_definition(inp):
                        return True
                return False  # PHI with no real inputs

            # Load from stack/globals - these have real values
            if mnemonic in {"LCP", "GCP"}:
                # These load from known locations, consider as defined
                return True

            # Default: consider undefined if we can't trace a real source
            return False

        return not has_real_definition(value)

    def _is_valid_pointer(self, value: SSAValue) -> bool:
        """Check if value is a valid pointer that can be dereferenced."""
        # Has address alias (&local_X, &data_X)
        if value.alias and value.alias.startswith("&"):
            return True
        # Came from address instruction (LADR removed - it loads values, not addresses)
        if value.producer_inst:
            if value.producer_inst.mnemonic in {"GADR", "DADR", "PNT"}:
                return True
        # Has pointer type
        if value.value_type == opcodes.ResultType.POINTER:
            return True
        return False

    def _format_constant_value(
        self,
        const_val: ConstantValue,
        expected_type_str: str = None,
        context: ExpressionContext = ExpressionContext.IN_EXPRESSION,
    ) -> str:
        """Format a tracked constant into a C literal or symbol name."""
        if const_val.symbol_name:
            return const_val.symbol_name

        value = const_val.value
        if isinstance(value, float):
            return str(value)

        int_value = int(value)
        if int_value > 0x7FFFFFFF:
            int_value -= 0x100000000

        if expected_type_str:
            if '*' in expected_type_str and int_value == 0:
                return "0"
            if 'float' in expected_type_str.lower() and '*' not in expected_type_str:
                return _format_float(int_value)
            if 'double' in expected_type_str.lower() and '*' not in expected_type_str:
                return _format_float(int_value)

        if context in (ExpressionContext.IN_ARRAY_INDEX,):
            return str(int_value)

        if const_val.value_type == opcodes.ResultType.FLOAT:
            return _format_float(int_value)

        return str(int_value)

    def _check_string_literal(self, value: SSAValue) -> Optional[str]:
        """
        Check if value represents a string literal pointer from data segment.

        Returns escaped string literal if found, None otherwise.
        """
        # Need access to SCR file with data_strings
        scr = getattr(self.ssa, "scr", None)
        if not scr or not hasattr(scr, "data_strings"):
            return None

        # Check if value is &data_X (address of data)
        if value.alias and value.alias.startswith("&data_"):
            try:
                data_offset = int(value.alias[6:])  # Remove "&data_" prefix
                byte_offset = data_offset * 4

                # Check if this byte offset matches a string offset
                if byte_offset in scr.data_strings:
                    return f'"{self._escape_string(scr.data_strings[byte_offset])}"'

                # Check if value at this offset is the first 4 bytes of a string
                if byte_offset < len(scr.data_segment.raw_data) - 3:
                    import struct
                    numeric_value = struct.unpack('<I', scr.data_segment.raw_data[byte_offset:byte_offset+4])[0]

                    # Check if this value matches the beginning of any string
                    for str_offset, str_content in scr.data_strings.items():
                        if len(str_content) >= 4:
                            try:
                                first_bytes = str_content[:4].encode('ascii')
                                encoded_value = struct.unpack('<I', first_bytes)[0]
                                if numeric_value == encoded_value:
                                    return f'"{self._escape_string(str_content)}"'
                            except (ValueError, struct.error):
                                pass
            except (ValueError, struct.error):
                pass

        # Try to get the numeric value for other cases
        numeric_value = None

        # Check if value has alias with numeric content
        if value.alias:
            try:
                numeric_value = int(value.alias)
            except ValueError:
                pass

        # If no alias or not numeric, check if it's a constant from producer
        if numeric_value is None and value.producer_inst:
            inst = value.producer_inst
            # Check for PUSH with constant argument
            if inst.mnemonic == "PUSH" and len(inst.inputs) > 0:
                try:
                    numeric_value = int(inst.inputs[0].alias or inst.inputs[0].name)
                except (ValueError, AttributeError):
                    pass

        # Also check if value comes from DCP loading from data segment
        if numeric_value is None and value.producer_inst:
            inst = value.producer_inst
            if inst.mnemonic == "DCP" and len(inst.inputs) > 0:
                # DCP loads value from address, check if address is data_X
                addr = inst.inputs[0]
                if addr.alias and addr.alias.startswith("data_"):
                    try:
                        # Get the data offset and read the value
                        data_offset = int(addr.alias[5:])  # Remove "data_" prefix
                        byte_offset = data_offset * 4
                        if byte_offset < len(scr.data_segment.raw_data) - 3:
                            import struct
                            numeric_value = struct.unpack('<I', scr.data_segment.raw_data[byte_offset:byte_offset+4])[0]
                    except (ValueError, struct.error):
                        pass

        # No numeric value found
        if numeric_value is None:
            return None

        # Check all string offsets in data segment
        # String addresses are stored as data segment base + byte offset
        # The numeric value might be the actual pointer value (base + offset)
        for str_offset, str_content in scr.data_strings.items():
            # Calculate what the pointer value would be
            # In SCR files, data segment starts after header
            # For simplicity, check if numeric_value could be this string

            # Method 1: Direct offset match (offset in dwords)
            if numeric_value == str_offset:
                return f'"{self._escape_string(str_content)}"'

            # Method 2: Byte offset match (offset in bytes / 4)
            if numeric_value == str_offset // 4:
                return f'"{self._escape_string(str_content)}"'

            # Method 3: The value might encode the string address
            # Check if first 4 bytes of string match the value
            try:
                import struct
                first_bytes = str_content[:4].encode('ascii')
                if len(first_bytes) == 4:
                    encoded_value = struct.unpack('<I', first_bytes)[0]
                    if numeric_value == encoded_value:
                        return f'"{self._escape_string(str_content)}"'
            except (ValueError, struct.error):
                pass

        return None

    def _escape_string(self, s: str) -> str:
        """Escape special characters in string for C literal."""
        s = s.replace('\\', '\\\\')  # Backslash
        s = s.replace('"', '\\"')    # Double quote
        s = s.replace('\n', '\\n')   # Newline
        s = s.replace('\t', '\\t')   # Tab
        s = s.replace('\r', '\\r')   # Carriage return
        return s

    def _is_string_literal(self, rendered: str) -> bool:
        """Check if rendered value is a string literal (or address of string)."""
        # Direct string literal
        if rendered.startswith('"') and rendered.endswith('"'):
            return True
        # Address of string literal: &"text"
        if rendered.startswith('&"') and rendered.endswith('"'):
            return True
        return False

    def _is_address_expression(self, rendered: str) -> bool:
        """Check if rendered value is an address/pointer expression (valid lvalue)."""
        import re
        # String literal address is NOT a writable address (it's a string pointer value)
        if self._is_string_literal(rendered):
            return False
        # FIX #3: Float literals are NOT addresses (even though they contain '.')
        # Check this BEFORE struct field access detection
        if rendered.endswith('f') and rendered.replace('.', '').replace('-', '').replace('e', '').replace('+', '')[:-1].isdigit():
            return False
        # Function call expressions are NEVER addresses/lvalues
        # Detect: name(...) or name(...)  at top level
        if re.match(r'^[A-Za-z_]\w*\(', rendered):
            return False
        # Arithmetic expressions containing function calls are never addresses
        # e.g. "3.0f + frnd(3.0f)"
        if '(' in rendered and re.search(r'[A-Za-z_]\w*\(', rendered):
            # Contains a function call somewhere - not an address
            return False
        # Direct address reference (but not string address)
        if rendered.startswith("&"):
            return True
        # Pointer dereference
        if rendered.startswith("*"):
            return True
        # Contains address operator (complex expression like ((&local + 4) + 0))
        # But not if it's just a string address, and not inside a function call
        if "&" in rendered and not rendered.startswith('&"'):
            return True
        # Variable name (local_X, param_X, etc.) - valid lvalue
        # But NOT if it's an arithmetic expression like "local_0 - 1.0f"
        if rendered.startswith("local_") or rendered.startswith("param_"):
            # Check that this is a simple variable name, not an expression
            # containing arithmetic operators at the top level
            if re.match(r'^(?:local|param)_\w+$', rendered):
                return True
            # Could be a subscript or field access: local_0[i], local_0.field
            # But NOT "local_0 - 1.0f" where the dot is in a float literal
            if '[' in rendered:
                return True
            if '.' in rendered:
                # Check if the dot is a struct field access (local_0.field)
                # vs a float literal in an arithmetic expression (local_0 - 1.0f)
                # A field access has the dot immediately after the variable name
                if re.match(r'^(?:local|param)_\w+\.', rendered):
                    return True
                # Otherwise it's likely an expression containing floats
                return False
            # Contains arithmetic operators - this is an expression, not an lvalue
            return False
        # Struct field access (contains .) but NOT float arithmetic
        # Must look like identifier.field, not "3.0f + something"
        if "." in rendered and not rendered.startswith('"'):
            # Reject if it contains top-level arithmetic operators (+ - * /)
            # outside of brackets/parens, suggesting it's an expression not a field access
            depth = 0
            has_toplevel_arith = False
            for i, ch in enumerate(rendered):
                if ch in '([':
                    depth += 1
                elif ch in ')]':
                    depth -= 1
                elif depth == 0 and ch in '+-*/' and i > 0:
                    # Skip -> (arrow operator)
                    if ch == '-' and i + 1 < len(rendered) and rendered[i + 1] == '>':
                        continue
                    has_toplevel_arith = True
                    break
            if has_toplevel_arith:
                return False
            return True
        return False

    def _is_literal_value(self, rendered: str) -> bool:
        """Check if rendered value is a literal (string, int, or float) - not valid as lvalue."""
        # String literal
        if self._is_string_literal(rendered):
            return True
        # Float literal (ends with 'f')
        if rendered.endswith('f'):
            try:
                float(rendered[:-1])
                return True
            except ValueError:
                pass
        # Integer literal
        if rendered.isdigit() or (rendered.startswith('-') and rendered[1:].replace('.', '').isdigit()):
            return True
        return False

    def _is_valid_lvalue(self, target: str) -> bool:
        """Check if target is a valid C lvalue expression.

        Valid lvalues: variable names, array subscripts (x[i]), struct fields (x.y),
        pointer dereferences (*x), and pointer arithmetic to struct fields.
        Invalid: arithmetic expressions on non-pointer values (x - 1.0f, x / y).
        """
        if not target:
            return False
        s = target.strip()
        if not s:
            return False

        # Pointer dereference: *expr - valid lvalue
        if s.startswith('*'):
            return True

        # Check for bare arithmetic operators outside of brackets/parens
        depth_bracket = 0
        depth_paren = 0
        has_toplevel_arith = False
        has_toplevel_div = False
        has_toplevel_sub = False
        i = 0
        while i < len(s):
            ch = s[i]
            if ch == '[':
                depth_bracket += 1
            elif ch == ']':
                depth_bracket -= 1
            elif ch == '(':
                depth_paren += 1
            elif ch == ')':
                depth_paren -= 1
            elif depth_bracket == 0 and depth_paren == 0:
                if ch == '/':
                    has_toplevel_div = True
                    has_toplevel_arith = True
                elif ch == '+':
                    has_toplevel_arith = True
                elif ch == '-':
                    if i + 1 < len(s) and s[i + 1] == '>':
                        i += 1  # skip '->'
                    else:
                        has_toplevel_sub = True
                        has_toplevel_arith = True
            i += 1

        # Division at top level is never a valid lvalue (e.g., vec2.y / vec2.y)
        if has_toplevel_div:
            return False

        # Subtraction at top level is never a valid lvalue (e.g., local_0_v7 - 1.0f)
        if has_toplevel_sub:
            return False

        # Addition with pointer base (&x + offset, name + offset) is valid pointer arithmetic
        # that represents struct field or array access - allow it
        # Only reject addition without any pointer/address context
        if has_toplevel_arith and not has_toplevel_div and not has_toplevel_sub:
            # Allow: (&x) + N (pointer arithmetic for struct/array)
            # Reject: plain variable + value without address context
            pass  # Allow pointer arithmetic stores

        return True

    def _is_numeric_literal_text(self, rendered: str) -> bool:
        """Check if a rendered string is a numeric literal (int/float/hex)."""
        if self._is_string_literal(rendered):
            return False

        if re.match(r'^[+-]?0x[0-9a-fA-F]+$', rendered):
            return True

        numeric_pattern = r'^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?f?$'
        return re.match(numeric_pattern, rendered) is not None

    def _get_constant_int(self, value: SSAValue) -> Optional[int]:
        """Extract a constant integer value from an SSAValue if possible."""
        if not value:
            return None

        if value.alias:
            if value.alias.isdigit():
                return int(value.alias)
            if value.alias.startswith("data_") and self.data_segment:
                try:
                    offset = int(value.alias[5:])
                    raw_val = self.data_segment.get_dword(offset * 4)
                    if raw_val > 0x7FFFFFFF:
                        raw_val -= 0x100000000
                    return raw_val
                except (ValueError, AttributeError):
                    pass

        const_val = self._constant_propagator.get_constant(value)
        if const_val is not None:
            try:
                return int(const_val.value)
            except (TypeError, ValueError):
                return None

        return None

    def _get_literal_constant_text(
        self,
        value: SSAValue,
        expected_type_str: str = None,
        context: ExpressionContext = ExpressionContext.IN_EXPRESSION
    ) -> Optional[str]:
        """Return literal text for a value if it's a safe numeric literal."""
        if not value or not value.alias:
            return None

        alias = value.alias

        if alias.startswith("data_"):
            try:
                offset = int(alias[5:])
            except ValueError:
                return None
            if self._global_names.get(offset):
                return None
            literal = self._load_literal(alias, value.value_type, expected_type_str=expected_type_str, context=context)
            if literal is not None and self._is_numeric_literal_text(literal):
                return literal
            return None

        if alias.startswith("&"):
            return None

        if self._is_numeric_literal_text(alias):
            return alias

        return None

    def _can_render_constant_expression(self, value: SSAValue, depth: int = 0) -> bool:
        """Check if value is a pure constant expression (no variables, no side effects)."""
        if depth > 8:
            return False

        if self._get_literal_constant_text(value) is not None:
            return True

        inst = value.producer_inst
        if not inst:
            return False

        if inst.mnemonic in INFIX_OPS and len(inst.inputs) == 2:
            return all(self._can_render_constant_expression(inp, depth + 1) for inp in inst.inputs)

        if inst.mnemonic in UNARY_PREFIX and len(inst.inputs) == 1:
            return self._can_render_constant_expression(inst.inputs[0], depth + 1)

        return False

    def _detect_target_field_type(self, target: str) -> Optional[str]:
        """
        Detect the type of a struct field target for proper source rendering.

        Args:
            target: Rendered target string (e.g., "vec.z", "&local_11.field_8", "initside.y")

        Returns:
            Field type string ('float', 'int', etc.) or None if unknown
        """
        # Extract field access pattern: structname.fieldname or &structname.fieldname
        if '.' not in target:
            return None

        # Remove & prefix if present
        clean_target = target.lstrip('&')

        # Parse struct.field pattern
        parts = clean_target.rsplit('.', 1)
        if len(parts) != 2:
            return None

        struct_part, field_name = parts

        # Remove array indexing if present (e.g., "g_will_pos[i]" -> "g_will_pos")
        if '[' in struct_part:
            struct_part = struct_part.split('[')[0]

        # FLOAT FIELDS: c_Vector3 (x, y, z are all floats)
        if field_name in ('x', 'y', 'z'):
            # Check if this is a c_Vector3 type based on tracked struct types
            base_var = struct_part
            if base_var in self._var_struct_types:
                struct_type = self._var_struct_types[base_var]
                if struct_type in ('c_Vector3', 'c_vector3'):
                    return 'float'
            # Also check common variable names that are vectors
            if any(name in struct_part.lower() for name in ['vec', 'pos', 'dir', 'movdir', 'plpos', 'shot_pos']):
                return 'float'

        # FLOAT FIELDS: Generic field_N where N is 0, 4, or 8 for c_Vector3
        if field_name in ('field_0', 'field_4', 'field_8'):
            base_var = struct_part
            if base_var in self._var_struct_types:
                struct_type = self._var_struct_types[base_var]
                if struct_type in ('c_Vector3', 'c_vector3'):
                    return 'float'

        # Use structure database for known types
        from ..structures import get_struct_by_name, get_field_at_offset

        # Try to resolve struct type from our tracked types
        base_var = struct_part
        if base_var in self._var_struct_types:
            struct_type = self._var_struct_types[base_var]
            struct_def = get_struct_by_name(struct_type)
            if struct_def:
                # Find field by name
                # BUGFIX: struct_def.fields is a List[StructField], not a dict
                # BUGFIX: StructField has type_name, not type
                for f_info in struct_def.fields:
                    if f_info.name == field_name or f_info.name == field_name.replace('field_', ''):
                        # Check if field type contains 'float'
                        if 'float' in f_info.type_name.lower():
                            return 'float'
                        elif 'int' in f_info.type_name.lower() or 'dword' in f_info.type_name.lower():
                            return 'int'

        return None

    def _detect_array_indexing(self, value: SSAValue) -> Optional[str]:
        """
        Detect array indexing pattern: GADR/DADR base + (index * element_size)
        Also detects structure field access: array[index] + field_offset
        Also detects plain structure field access: &local_X + offset
        Returns notation like "array[index]" or "array[index].field" or "local_X.fieldN" if detected, None otherwise.
        """
        if not value.producer_inst:
            return None

        inst = value.producer_inst

        # Pattern 0: ADD(ADR(local_X), offset) → local_X.fieldN  (plain structure field access)
        # Or: ADD(ADD(ADR(local_X), offset1), offset2) → local_X.fieldN
        if inst.mnemonic == "ADD" and len(inst.inputs) == 2:
            left = inst.inputs[0]
            right = inst.inputs[1]

            # Check if this is nested ADD(ADD(ADR, offset1), offset2)
            total_offset = 0
            base_value = None

            # Check if left is ADD(ADR, offset)
            if left.producer_inst and left.producer_inst.mnemonic == "ADD" and len(left.producer_inst.inputs) == 2:
                inner_left = left.producer_inst.inputs[0]
                inner_right = left.producer_inst.inputs[1]

                # Check if inner_left is ADR
                if inner_left.producer_inst and inner_left.producer_inst.mnemonic in {"LADR", "GADR", "DADR"}:
                    # Get base name
                    base_name = self._render_value(inner_left)
                    if base_name.startswith("&"):
                        base_name = base_name[1:]

                        # Check if inner_right is constant offset
                        try:
                            inner_offset_str = self._render_value(inner_right)
                            inner_offset = int(inner_offset_str)

                            # Check if outer right is also constant offset
                            outer_offset_str = self._render_value(right)
                            outer_offset = int(outer_offset_str)

                            total_offset = inner_offset + outer_offset

                            # Reasonable field offset range
                            if 0 <= total_offset < 256:
                                field_name = self._resolve_field_name(base_name, total_offset)
                                # FIX (01-21): Use semantic name for struct field accesses
                                display_name = self._get_field_base_name(base_name, field_name)
                                result = f"{display_name}.{field_name}"
                                return result
                        except (ValueError, AttributeError):
                            pass

            # Check if left is PNT(ADR, pnt_offset) — struct sub-field via pointer arithmetic
            # Pattern: ADD(PNT(ADR(local_X), pnt_offset), const_offset) → local_X.field_{pnt_offset + const_offset}
            # This handles: LADR [sp+0], PNT 20, GCP 4, ADD → hudinfo.field_24
            if left.producer_inst and left.producer_inst.mnemonic == "PNT" and len(left.producer_inst.inputs) > 0:
                pnt_inst = left.producer_inst
                pnt_base = pnt_inst.inputs[0]

                # Check if PNT base is ADR
                if pnt_base.producer_inst and pnt_base.producer_inst.mnemonic in {"LADR", "GADR", "DADR"}:
                    base_name = self._render_value(pnt_base)
                    if base_name.startswith("&"):
                        base_name = base_name[1:]

                        try:
                            # Get PNT offset from instruction arg1
                            pnt_offset = 0
                            if pnt_inst.instruction and pnt_inst.instruction.instruction:
                                pnt_offset = pnt_inst.instruction.instruction.arg1

                            # Get ADD right-hand constant offset
                            outer_offset_str = self._render_value(right)
                            outer_offset = int(outer_offset_str)

                            total_offset = pnt_offset + outer_offset

                            # Reasonable field offset range
                            if 0 <= total_offset < 256:
                                field_name = self._resolve_field_name(base_name, total_offset)
                                display_name = self._get_field_base_name(base_name, field_name)
                                result = f"{display_name}.{field_name}"
                                return result
                        except (ValueError, AttributeError):
                            pass

            # Check if left is DADR(ADR, dadr_offset) — pointer with fixed offset
            # Pattern: ADD(DADR(LADR/GADR(base), dadr_offset), const_offset) → base.field_{dadr_offset + const_offset}
            if left.producer_inst and left.producer_inst.mnemonic == "DADR" and len(left.producer_inst.inputs) > 0:
                dadr_inst = left.producer_inst
                dadr_base = dadr_inst.inputs[0]
                if dadr_base.producer_inst and dadr_base.producer_inst.mnemonic in {"LADR", "GADR"}:
                    base_name = self._render_value(dadr_base)
                    if base_name.startswith("&"):
                        base_name = base_name[1:]
                    try:
                        dadr_offset = 0
                        if dadr_inst.instruction and dadr_inst.instruction.instruction:
                            dadr_offset = dadr_inst.instruction.instruction.arg1
                        outer_offset_str = self._render_value(right)
                        outer_offset = int(outer_offset_str)
                        total_offset = dadr_offset + outer_offset
                        if 0 <= total_offset < 512:
                            field_name = self._resolve_field_name(base_name, total_offset)
                            display_name = self._get_field_base_name(base_name, field_name)
                            # Use -> for pointer params, . for local structs
                            clean_base = base_name.lstrip("&")
                            if clean_base.startswith("param_") or clean_base == "info":
                                result = f"{display_name}->{field_name}"
                            else:
                                result = f"{display_name}.{field_name}"
                            return result
                    except (ValueError, AttributeError):
                        pass

            # Check if left is directly ADR (simpler pattern)
            if left.producer_inst and left.producer_inst.mnemonic in {"LADR", "GADR", "DADR"}:
                base_name = self._render_value(left)
                if base_name.startswith("&"):
                    base_name = base_name[1:]

                    # Check if right is constant offset
                    try:
                        offset_str = self._render_value(right)
                        offset = int(offset_str)

                        # Reasonable field offset range - but exclude multiplication patterns
                        if 0 < offset < 256:
                            # NEW: Check if base is a known array (skip struct field notation if it is)
                            base_is_array = False
                            if left.producer_inst.mnemonic == "GADR":
                                gadr_offset = left.producer_inst.instruction.instruction.arg1
                                if gadr_offset in self._global_type_info:
                                    base_is_array = self._global_type_info[gadr_offset].is_array_base
                            # FIX (01-20): Also check if local var has struct array type from field tracker
                            # If the variable is a struct array, we need to access element [0]
                            elif left.producer_inst.mnemonic == "LADR":
                                # Check if type_tracker or field_tracker knows this is a struct array
                                tracked_type = None
                                is_struct_array = False

                                # PRIORITY 1: Check type_tracker (unified tracker)
                                if self._type_tracker:
                                    info = self._type_tracker.get_usage_info(base_name)
                                    if info and (info.is_struct_array or (info.is_array and info.struct_type)):
                                        tracked_type = info.struct_type
                                        is_struct_array = True

                                # PRIORITY 2: Check field_tracker
                                if not tracked_type and hasattr(self, '_field_tracker') and self._field_tracker:
                                    tracked_type = self._field_tracker.get_struct_type(base_name)
                                    if tracked_type:
                                        is_struct_array = True

                                if is_struct_array and tracked_type:
                                    # If it has a struct type AND we're accessing a field offset,
                                    # it could be array[0].field - emit with [0]
                                    # Check if offset matches a known struct field
                                    struct_def = get_struct_by_name(tracked_type)
                                    if struct_def and struct_def.size > offset:
                                        field_name = get_verified_field_name(tracked_type, offset)
                                        if field_name:
                                            # Return as array[0].field for struct arrays
                                            # FIX (01-21): Use semantic name for struct field accesses
                                            display_name = self._get_field_base_name(base_name, field_name)
                                            result = f"{display_name}[0].{field_name}"
                                            if self._type_tracker:
                                                self._type_tracker.record_array_usage(base_name, result)
                                                self._type_tracker.record_field_usage(base_name, result)
                                            return result

                            # Make sure this isn't actually array indexing (check if right is MUL result OR base is array)
                            if not (right.producer_inst and right.producer_inst.mnemonic in {"MUL", "IMUL"}) and not base_is_array:
                                # FIX (01-20): Only emit struct field notation if we know the variable is a struct
                                # Otherwise we get `int_var.field_4` which won't compile
                                struct_type = None

                                # PRIORITY 1: Check type_tracker for unified type resolution
                                if self._type_tracker and self._type_tracker.should_emit_field_notation(base_name):
                                    info = self._type_tracker.get_usage_info(base_name)
                                    if info:
                                        struct_type = info.struct_type

                                # PRIORITY 2: Check field_tracker
                                if not struct_type and hasattr(self, '_field_tracker') and self._field_tracker:
                                    struct_type = self._field_tracker.get_struct_type(base_name)

                                # PRIORITY 3: Check _var_struct_types
                                if not struct_type:
                                    struct_type = self._var_struct_types.get(base_name)

                                if struct_type:
                                    field_name = self._resolve_field_name(base_name, offset)
                                    # FIX (01-21): Use semantic name for struct field accesses
                                    display_name = self._get_field_base_name(base_name, field_name)
                                    result = f"{display_name}.{field_name}"
                                    # Notify type_tracker of field usage
                                    if self._type_tracker:
                                        self._type_tracker.record_field_usage(base_name, result)
                                    return result
                                # else: fall through to other patterns or raw pointer arithmetic
                    except (ValueError, AttributeError):
                        pass

        # Pattern 1: ADD(ADD(base, index*size), field_offset) → array[index].fieldN
        # Also handles: ADD(PNT(ADD(base, index*size)), field_offset) for dereferenced pointers
        if inst.mnemonic == "ADD" and len(inst.inputs) == 2:
            left = inst.inputs[0]
            right = inst.inputs[1]


            # Check if left is array indexing (direct ADD or PNT of ADD)
            check_value = left

            # If left is PNT, look through it to find the underlying ADD
            if left.producer_inst and left.producer_inst.mnemonic == "PNT" and len(left.producer_inst.inputs) == 1:
                check_value = left.producer_inst.inputs[0]

            # Now check if we have array indexing pattern
            if check_value.producer_inst and check_value.producer_inst.mnemonic == "ADD":
                array_notation = self._detect_array_indexing(check_value)  # Recursive call
                if array_notation:
                    # Check if right is a small constant (field offset)
                    try:
                        field_offset_str = self._render_value(right)
                        field_offset = int(field_offset_str)
                        if 0 <= field_offset < 128:  # Reasonable field offset range
                            # Extract base variable from array notation (e.g., "enum_pl[0]" -> "enum_pl")
                            base_var = array_notation.split('[')[0] if '[' in array_notation else array_notation
                            field_name = self._resolve_field_name(base_var, field_offset)
                            # Return struct field access
                            result = f"{array_notation}.{field_name}"
                            return result
                    except (ValueError, AttributeError) as e:
                        pass

        # Pattern 2: ADD(base_addr, index_expr) → array[index]
        # This pattern also handles nested structure field access:
        # ADD(ADD(base, index*size), field_offset) where left side is another ADD
        if inst.mnemonic == "ADD" and len(inst.inputs) == 2:
            left = inst.inputs[0]
            right = inst.inputs[1]


            # SPECIAL CASE: Check if left is another ADD (nested structure field access)
            # Pattern: ADD(ADD(base, index*size), field_offset) → array[index].fieldN
            if left.producer_inst and left.producer_inst.mnemonic == "ADD":
                # Recursively detect array indexing in the left ADD
                array_notation = self._detect_array_indexing(left)
                if array_notation:
                    # Check if right is a small constant (field offset)
                    try:
                        field_offset_str = self._render_value(right)
                        field_offset = int(field_offset_str)
                        if 0 <= field_offset < 128:  # Reasonable field offset range
                            # Extract base variable from array notation (e.g., "enum_pl[0]" -> "enum_pl")
                            base_var = array_notation.split('[')[0] if '[' in array_notation else array_notation
                            field_name = self._resolve_field_name(base_var, field_offset)
                            # Return struct field access
                            result = f"{array_notation}.{field_name}"
                            return result
                    except (ValueError, AttributeError) as e:
                        pass

            # Check if left is a base address (GADR/DADR/LADR or &variable)
            base_name = None
            if left.alias and left.alias.startswith("&"):
                # Strip & and check for global variable name
                var_name = left.alias[1:]  # Strip &
                # Check if this is a global variable (data_XXX -> gVarName)
                if var_name.startswith("data_"):
                    try:
                        offset = int(var_name[5:])
                        global_name = self._global_names.get(offset)
                        if global_name:
                            base_name = global_name
                        else:
                            base_name = var_name
                    except ValueError:
                        base_name = var_name
                else:
                    base_name = var_name
            elif left.producer_inst and left.producer_inst.mnemonic in {"GADR", "DADR", "LADR", "LCP"}:
                base_name = self._render_value(left)
                if base_name.startswith("&"):
                    base_name = base_name[1:]

            if not base_name:
                return None

            # FIX (01-20): For LADR-based variables (locals), only generate array notation if
            # the variable is known to be an array or struct array. Otherwise, we generate
            # local_X[idx] but declare int local_X which won't compile.
            is_local_var = left.producer_inst and left.producer_inst.mnemonic == "LADR"
            if is_local_var:
                # Check if this local variable is tracked as a struct array
                is_local_array = False

                # PRIORITY 1: Check type_tracker (unified tracker - most reliable)
                if self._type_tracker and self._type_tracker.should_emit_array_notation(base_name):
                    is_local_array = True

                # PRIORITY 2: Check field_tracker (XCALL-based detection)
                if not is_local_array and hasattr(self, '_field_tracker') and self._field_tracker:
                    struct_type = self._field_tracker.get_struct_type(base_name)
                    if struct_type:
                        is_local_array = True  # Struct arrays are OK

                # PRIORITY 3: Check _var_struct_types for struct arrays
                if not is_local_array:
                    struct_type = self._var_struct_types.get(base_name)
                    if struct_type:
                        is_local_array = True

                if not is_local_array:
                    # Not a known array - skip array notation to avoid compilation errors
                    return None

            # Check if right is (index * element_size) pattern
            index_expr = None
            if right.producer_inst and right.producer_inst.mnemonic in {"MUL", "IMUL"} and len(right.producer_inst.inputs) == 2:
                # Pattern: index * size
                mul_left = right.producer_inst.inputs[0]
                mul_right = right.producer_inst.inputs[1]

                # Check if mul_right is a constant (element size like 4, 8, 16)
                size_val = self._get_constant_int(mul_right)
                if size_val is None:
                    size_val = self._get_constant_int(mul_left)

                base_element_size = None
                base_is_array = False
                if (
                    left.producer_inst
                    and left.producer_inst.mnemonic == "GADR"
                    and left.producer_inst.instruction
                    and left.producer_inst.instruction.instruction
                ):
                    gadr_offset = left.producer_inst.instruction.instruction.arg1
                    if gadr_offset in self._global_type_info:
                        global_info = self._global_type_info[gadr_offset]
                        base_is_array = global_info.is_array_base
                        base_element_size = global_info.array_element_size

                if size_val and size_val > 0 and size_val <= 256:
                    index_operand = mul_left if size_val == self._get_constant_int(mul_right) else mul_right
                    if base_is_array and base_element_size and size_val != base_element_size:
                        size_val = base_element_size
                    index_expr = self._render_value(index_operand, context=ExpressionContext.IN_ARRAY_INDEX)
                    # Fix: If index rendered as address of the base array (e.g., &g_will_pos),
                    # the SSA has wrong aliasing. Try the rename_map for a better name.
                    if index_expr:
                        stripped = index_expr.lstrip("&")
                        if stripped == base_name:
                            alt = self._rename_map.get(index_operand.name) if self._rename_map else None
                            if alt and alt != base_name and not alt.startswith("&"):
                                index_expr = alt
                            else:
                                index_expr = None  # Can't resolve valid index
                elif base_is_array and base_element_size:
                    index_operand = mul_left if self._get_constant_int(mul_right) == base_element_size else mul_right
                    index_expr = self._render_value(index_operand, context=ExpressionContext.IN_ARRAY_INDEX)
                # NOTE (01-20): Don't add first field access here. This is array indexing detection,
                # not value assignment. When we compute &array[index], the result IS a pointer to
                # the struct element, not to a field within it. First field access should only be
                # added when assigning a scalar value to a struct array element (handled elsewhere).

            # Also handle simple offset (no multiplication)
            # NEW: Only treat as array if base is marked as is_array_base
            elif right.alias or (right.producer_inst and right.producer_inst.mnemonic in {"LCP", "GCP"}):
                # Simple offset - could be array[constant]
                index_rendered = self._render_value(right, context=ExpressionContext.IN_ARRAY_INDEX)
                if right.alias and right.alias.startswith("data_") and self.data_segment:
                    try:
                        offset = int(right.alias[5:])
                        raw_val = self.data_segment.get_dword(offset * 4)
                        if raw_val > 0x7FFFFFFF:
                            raw_val = raw_val - 0x100000000
                        index_rendered = str(raw_val)
                    except (ValueError, AttributeError):
                        pass

                # Check if base is a known array from global_resolver or local tracker
                is_base_array = False
                base_element_size = 4  # default

                # Get base offset from left (GADR/alias)
                base_dword_offset = None
                if left.alias and left.alias.startswith("&data_"):
                    try:
                        base_dword_offset = int(left.alias[6:])  # Extract offset from "&data_123"
                    except ValueError:
                        pass
                elif left.producer_inst and left.producer_inst.mnemonic in {"GADR"}:
                    # GADR arg1 is DWORD offset
                    if left.producer_inst.instruction:
                        base_dword_offset = left.producer_inst.instruction.instruction.arg1

                # Check if this base is marked as array
                if base_dword_offset is not None and base_dword_offset in self._global_type_info:
                    global_info = self._global_type_info[base_dword_offset]
                    if global_info.is_array_base:
                        is_base_array = True
                        base_element_size = global_info.array_element_size or 4

                # Local array support (constant offsets)
                if not is_base_array and is_local_var and self._type_tracker:
                    info = self._type_tracker.get_usage_info(base_name)
                    if info and info.is_array:
                        is_base_array = True
                        if info.array_element_sizes:
                            base_element_size = min(info.array_element_sizes)

                # Pointer parameters (e.g., list[0]) should allow constant indexing
                if not is_base_array and left.producer_inst and left.producer_inst.mnemonic == "LCP":
                    is_base_array = True

                # If it's a number and base is an array, divide by element_size to get index
                if is_base_array:
                    try:
                        byte_offset = int(index_rendered)
                        if byte_offset % base_element_size == 0 and byte_offset >= 0 and byte_offset < 1000:
                            index_expr = str(byte_offset // base_element_size)
                    except ValueError:
                        # Not a number - use as-is
                        index_expr = index_rendered

            if index_expr:
                # Validate: index expression should not be an address of the base array
                # or contain the base name as an address (e.g., &g_will_pos[&g_will_pos])
                stripped_idx = index_expr.lstrip('&')
                if stripped_idx == base_name or index_expr == f"&{base_name}":
                    # Index resolved to the base array address - this is a misidentification.
                    # Try to use the rename_map for the index operand instead.
                    if index_expr.startswith("&") and hasattr(self, '_rename_map') and self._rename_map:
                        # Look for a rename for the index operand's SSA value
                        for inp in (right.producer_inst.inputs if right.producer_inst else []):
                            if inp.name in self._rename_map:
                                alt_name = self._rename_map[inp.name]
                                if alt_name != base_name and not alt_name.startswith("&"):
                                    index_expr = alt_name
                                    break
                        else:
                            return None  # Can't resolve valid index - skip array notation
                    else:
                        return None  # Can't resolve valid index
                result = f"{base_name}[{index_expr}]"
                # Notify type tracker of array usage (for runtime pattern collection)
                if self._type_tracker:
                    self._type_tracker.record_array_usage(base_name, result)
                return result

        return None

    def _format_pointer_target(self, value: SSAValue) -> str:
        """Format a value as assignment target (dereference if needed)."""

        # First, check if this is array indexing pattern
        array_notation = self._detect_array_indexing(value)
        if array_notation:
            # FIX (01-20): For assignment targets, if the array element is a struct,
            # we need to add the first field to make scalar assignment valid.
            # Pattern: local_5[i] = 0 → local_5[i].id = 0 (if local_5 is s_SC_FpvMapSign[])
            # BUT: Only if there's no field access already (e.g., local_296[0].side is fine)
            # Extract base variable name from array notation (e.g., "local_5[i]" -> "local_5")
            # Skip if already has field access (contains '.' after ']')
            if '.' in array_notation.split(']')[-1]:
                return array_notation  # Already has field access, don't add more
            base_var = array_notation.split('[')[0] if '[' in array_notation else None
            if base_var:
                # Check if this is a struct array (element size > 4)
                tracked_type = None
                skip_field_tracker = False

                # PRIORITY 1: Check type_tracker (unified tracker)
                if self._type_tracker:
                    info = self._type_tracker.get_usage_info(base_var)
                    if info and info.struct_type and info.confidence >= 0.7:
                        tracked_type = info.struct_type
                    if info and info.is_array and info.confidence < 0.7:
                        skip_field_tracker = True

                # PRIORITY 2: Check field_tracker
                if not tracked_type and not skip_field_tracker and hasattr(self, '_field_tracker') and self._field_tracker:
                    tracked_type = self._field_tracker.get_struct_type(base_var)

                if tracked_type:
                    # Get first field of the struct
                    first_field = get_verified_field_name(tracked_type, 0)
                    if first_field:
                        result = f"{array_notation}.{first_field}"
                        # Notify type tracker of field usage
                        if self._type_tracker:
                            self._type_tracker.record_field_usage(base_var, result)
                        return result
                else:
                    # No tracked type - check if we can infer from array indexing pattern
                    # by checking the element size (from the MUL pattern in ADD)
                    if value.producer_inst and value.producer_inst.mnemonic == "ADD":
                        add_inst = value.producer_inst
                        if len(add_inst.inputs) >= 2:
                            right = add_inst.inputs[1]
                            if right.producer_inst and right.producer_inst.mnemonic in {"MUL", "IMUL"}:
                                mul_right = right.producer_inst.inputs[1]
                                # Get element size from constant
                                size_val = self._get_constant_int(mul_right)
                                if size_val and size_val > 4:
                                    structs = get_struct_by_size(size_val)
                                    if len(structs) == 1:
                                        first_field = get_verified_field_name(structs[0].name, 0)
                                        if first_field:
                                            result = f"{array_notation}.{first_field}"
                                            # Notify type tracker of field usage
                                            if self._type_tracker:
                                                self._type_tracker.record_field_usage(base_var, result)
                                            return result
            return array_notation

        # FIX: Detect DADR(LADR(param)) pattern for struct field access
        # Pattern: LADR loads &param, DADR adds field offset
        if value.producer_inst and value.producer_inst.mnemonic == "DADR":
            dadr_inst = value.producer_inst
            if len(dadr_inst.inputs) > 0:
                base_value = dadr_inst.inputs[0]
                # Check if base is address (starts with &)
                if base_value.alias and base_value.alias.startswith("&"):
                    # Extract base name (remove &)
                    base_name = base_value.alias[1:]
                    # Get field offset from the original instruction
                    # dadr_inst.instruction is LiftedInstruction, which has .instruction (Instruction)
                    if dadr_inst.instruction and dadr_inst.instruction.instruction:
                        field_offset = dadr_inst.instruction.instruction.arg1

                        # Determine operator based on whether base is a pointer parameter or local struct
                        # Pattern LADR(&local_X) + DADR(offset) means local_X is a structure (not pointer)
                        # Pattern LADR(&param_X) + DADR(offset) means param_X is a pointer
                        field_name = self._resolve_field_name(base_name, field_offset)
                        # FIX (01-21): Use semantic name for struct field accesses
                        display_name = self._get_field_base_name(base_name, field_name)
                        clean_base = base_name.lstrip("&")
                        if clean_base.startswith("param_") or clean_base == "info":
                            # Pointer parameter: use -> (no & prefix since -> dereferences)
                            return f"{display_name}->{field_name}"
                        return f"&{display_name}.{field_name}"

        # FIX: Handle PNT instruction (pointer arithmetic) for field access
        # Pattern: PNT(base_addr, offset) → struct field access
        # Also handles chained PNTs: PNT(PNT(base_addr, off1), off2) → field at off1+off2
        # This MUST come before _render_value to avoid getting tmp names
        if value.producer_inst and value.producer_inst.mnemonic == "PNT":
            # Chase through chained PNT instructions to find base and total offset
            total_offset = 0
            current = value
            while current.producer_inst and current.producer_inst.mnemonic == "PNT":
                pnt_inst = current.producer_inst
                if not pnt_inst.instruction or not pnt_inst.instruction.instruction:
                    break
                total_offset += pnt_inst.instruction.instruction.arg1
                if not pnt_inst.inputs:
                    break
                current = pnt_inst.inputs[0]

            # Now 'current' is the base value (before any PNT) and total_offset is accumulated
            base_rendered = self._render_value(current)
            if base_rendered.startswith("&"):
                base_name = base_rendered[1:]
                # Resolve field name and return direct field access
                field_name = self._resolve_field_name(base_name, total_offset)

                # FALLBACK: If field_name is generic (field_N), try c_Vector3 ONLY when
                # the base variable has no known struct type (truly unknown struct)
                # or when the struct type IS c_Vector3. Don't apply when we know the
                # struct type is something else (e.g., s_SC_FlyOffCartridge offset 4
                # is "from" not "y").
                if field_name.startswith("field_"):
                    base_struct_type = self._var_struct_types.get(base_name)
                    if not base_struct_type and self._field_tracker:
                        base_struct_type = self._field_tracker.var_struct_types.get(base_name)
                    if not base_struct_type or base_struct_type in ('c_Vector3', 'c_vector3'):
                        if total_offset in (0, 4, 8):
                            from ..structures import get_verified_field_name as struct_field_lookup
                            vec3_field = struct_field_lookup("c_Vector3", total_offset)
                            if vec3_field:
                                field_name = vec3_field  # x, y, or z

                # FIX (01-21): Use semantic name for struct field accesses
                display_name = self._get_field_base_name(base_name, field_name)
                # Determine operator: -> for pointer params, . for local structs
                clean_base = base_name.lstrip("&")
                if clean_base.startswith("param_") or clean_base == "info":
                    return f"{display_name}->{field_name}"
                return f"{display_name}.{field_name}"

        rendered = self._render_value(value)

        # If it's an address reference, strip the & to get variable name
        if rendered.startswith("&"):
            var_name = rendered[1:]
            # FIX (01-20): For local struct assignment targets (not arrays, not already field access),
            # we need to add first field to make scalar assignment valid.
            # Pattern: hudinfo = 5100 → hudinfo.x = 5100 (if hudinfo is s_SC_MP_hud)
            if '.' not in var_name and '[' not in var_name:
                # Check if this is a known struct type
                tracked_type = None

                # Reverse lookup: semantic name -> SSA name
                # _semantic_names maps: SSA_name -> semantic_name
                # We need to find SSA_name from semantic_name
                ssa_name = var_name
                for ssa_n, sem_n in self._semantic_names.items():
                    if sem_n == var_name:
                        ssa_name = ssa_n
                        break

                # If heritage indicates this is a float, keep it as a scalar
                if self._get_heritage_type(ssa_name) == "float":
                    return var_name

                # PRIORITY 1: Check type_tracker (unified tracker) with SSA name
                if self._type_tracker:
                    info = self._type_tracker.get_usage_info(ssa_name)
                    if info and info.struct_type and not info.is_array:
                        # Plain struct (not array) - add first field
                        tracked_type = info.struct_type

                # PRIORITY 2: Check field_tracker with SSA name
                if not tracked_type and hasattr(self, '_field_tracker') and self._field_tracker:
                    tracked_type = self._field_tracker.get_struct_type(ssa_name)

                # PRIORITY 3: Check _var_struct_types with SSA name
                if not tracked_type:
                    tracked_type = self._var_struct_types.get(ssa_name)

                # PRIORITY 4: Check _var_struct_types with semantic name (fallback)
                if not tracked_type:
                    tracked_type = self._var_struct_types.get(var_name)

                if tracked_type:
                    first_field = get_verified_field_name(tracked_type, 0)
                    if first_field:
                        result = f"{var_name}.{first_field}"
                        if self._type_tracker:
                            self._type_tracker.record_field_usage(ssa_name, result)
                        return result
            return var_name

        # If it's a structure field access, use it directly
        if "." in rendered and not rendered.startswith('"'):
            return rendered

        # Don't dereference plain numbers - this would create invalid syntax like *0
        # Check if rendered is a numeric literal (int or float)
        try:
            # Check for integer
            if rendered.isdigit() or (rendered.startswith('-') and rendered[1:].isdigit()):
                return rendered
            # Check for float literal (e.g., "1.0f", "0.5f")
            if rendered.endswith('f'):
                float(rendered[:-1])
                return rendered
        except (ValueError, IndexError):
            pass

        # If it's a valid pointer, dereference it
        if self._is_valid_pointer(value):
            return f"*{rendered}"

        # Plain value (number, string) - not a valid target, return as-is
        return rendered

    def _track_text_id_assignment(self, target: str, source: str, inst: SSAInstruction) -> None:
        """Track constant assignments to local variables for text annotation.

        This enables annotation of functions like SC_MissionSave(&local_80) by
        tracking what constants were assigned to local_80's fields beforehand.

        Args:
            target: The target variable (e.g., "local_80", "local_80.field0", "local_63[0].y")
            source: The source value as string (e.g., "9136")
            inst: The SSA instruction for additional context
        """
        # Try to parse source as integer constant
        try:
            const_val = int(source)
        except ValueError:
            return

        # Check if it's in the reasonable text ID range
        if not (TEXT_ID_MIN <= const_val <= TEXT_ID_MAX):
            return

        # Extract base variable name from various patterns:
        # - local_80
        # - local_80.field0
        # - local_80.savename_id
        # - local_63[0].y
        # - local_63[0]
        base_name = target
        offset = 0

        # Handle array indexing: local_63[0].y -> local_63
        array_match = re.match(r'^(local_\d+)\[\d+\]', target)
        if array_match:
            base_name = array_match.group(1)
            # Try to extract field offset from remaining part
            remaining = target[len(array_match.group(0)):]
            if remaining.startswith('.'):
                field_part = remaining[1:]
                # Parse field as numeric offset or named field
                offset_match = re.match(r'field_?(\d+)', field_part)
                if offset_match:
                    offset = int(offset_match.group(1))
                elif field_part in ('x', 'y', 'z', 'w'):
                    # Common vector/struct fields
                    offset = {'x': 0, 'y': 1, 'z': 2, 'w': 3}[field_part]
        elif '.' in target:
            # Handle struct field access: local_80.field0
            parts = target.split('.', 1)
            base_name = parts[0]
            field_part = parts[1]

            # Try to extract numeric offset from field name
            match = re.match(r'field_?(\d+)', field_part)
            if match:
                offset = int(match.group(1))
            elif field_part in ('x', 'y', 'z', 'w'):
                offset = {'x': 0, 'y': 1, 'z': 2, 'w': 3}[field_part]

        # Only track assignments to local variables
        if not base_name.startswith('local_'):
            return

        # Track the assignment
        self._struct_text_tracker.track_assignment(base_name, const_val, offset)

    def _format_store(self, inst: SSAInstruction) -> Optional[str]:
        if inst.mnemonic not in self._store_ops:
            return None
        if len(inst.inputs) < 2:
            return None

        # Determine operand order based on aliases and producer instructions
        # Address aliases start with "&", value aliases are "data_X" or "param_X"
        alias0 = inst.inputs[0].alias or ""
        alias1 = inst.inputs[1].alias or ""

        # Check if input came from a pointer dereference (PNT) - these are targets
        prod0 = inst.inputs[0].producer_inst
        prod1 = inst.inputs[1].producer_inst
        is_pnt0 = prod0 and prod0.mnemonic == "PNT"
        is_pnt1 = prod1 and prod1.mnemonic == "PNT"

        # FÁZE 1.6 Pattern 2: Check if source comes from CALL+LLD pattern
        # If source value is from LLD, check if there's a CALL before it
        import sys
        call_expr_override = None
        source_val = inst.inputs[0]
        # Debug: print all ASGN to see what we're working with
        # print(f"DEBUG ASGN@{inst.address}: source={source_val.name}, has_producer={source_val.producer_inst is not None}", file=sys.stderr)
        if source_val.producer_inst:
            pass  # Debug print removed
            # print(f"  producer: {source_val.producer_inst.mnemonic}@{source_val.producer_inst.address}", file=sys.stderr)

        # Pattern 3: Direct XCALL->ASGN (source is t###_ret from XCALL)
        if source_val.producer_inst and source_val.producer_inst.mnemonic == "XCALL":
            # Source comes directly from XCALL return value (t###_ret pattern)
            xcall_inst = source_val.producer_inst
            call_expr = self._format_call(xcall_inst)
            if call_expr.endswith(";"):
                call_expr = call_expr[:-1].strip()
            # Strip off any "t###_ret = " prefix since we're replacing the target
            if " = " in call_expr:
                call_expr = call_expr.split(" = ", 1)[1]
            call_expr_override = call_expr

        elif source_val.producer_inst and source_val.producer_inst.mnemonic == "LLD":
            # print(f"DEBUG Pattern 2: ASGN@{inst.address} source from LLD@{source_val.producer_inst.address}", file=sys.stderr)
            # LLD loads return value - check if there's a CALL before it
            # We need to find the CALL in the block's instruction sequence
            # The CALL should be right before the LLD
            for block_id, block_instrs in self.ssa.instructions.items():
                lld_inst = source_val.producer_inst
                for i, bi in enumerate(block_instrs):
                    if bi == lld_inst and i > 0:
                        # print(f"  Found LLD at index {i} in block {block_id}", file=sys.stderr)
                        # Found LLD, check previous instructions for CALL/XCALL
                        for check_idx in range(i - 1, max(0, i - 3), -1):
                            # print(f"    check_idx={check_idx}: {block_instrs[check_idx].mnemonic}@{block_instrs[check_idx].address}", file=sys.stderr)
                            if block_instrs[check_idx].mnemonic in {"CALL", "XCALL"}:
                                # Found CALL+LLD pattern!
                                # print(f"  Found CALL/XCALL! Formatting...", file=sys.stderr)
                                call_expr = self._format_call(block_instrs[check_idx])
                                if call_expr.endswith(";"):
                                    call_expr = call_expr[:-1].strip()
                                call_expr_override = call_expr
                                # print(f"  call_expr_override={call_expr_override}", file=sys.stderr)
                                break
                        break
                if call_expr_override:
                    break

        # Determine if we should preserve numeric defaults for float-like assignments
        preserve_numeric_defaults = False
        if inst.outputs and len(inst.outputs) == 1:
            dest_value = inst.outputs[0]
            if dest_value and dest_value.name:
                heritage_type = self._get_heritage_type(dest_value.name)
                if heritage_type == "float":
                    preserve_numeric_defaults = True
        elif len(inst.inputs) >= 2:
            # Pointer assignment: ASGN(value, address) -> inspect destination base var type
            dest_name = self._extract_var_from_pointer(inst.inputs[1])
            if dest_name:
                heritage_type = self._get_heritage_type(dest_name)
                if heritage_type == "float":
                    preserve_numeric_defaults = True

        # Render both values first to analyze them
        source_val = inst.inputs[0]
        preserve_compound = bool(getattr(source_val, "metadata", {}).get("preserve_compound"))
        if call_expr_override:
            rendered0 = call_expr_override
        elif source_val.alias and self._is_parametric_alias(source_val.alias):
            # Remap param_N alias through _param_names for correct parameter ordering
            rendered0 = self._remap_param_alias(source_val.alias)
        elif preserve_compound and source_val.producer_inst:
            rendered0 = self._inline_expression(source_val)
        else:
            rendered0 = self._render_value(
                source_val,
                expected_type_str="float" if preserve_numeric_defaults else None,
            )
        rendered1 = self._render_value(inst.inputs[1])

        # Determine which operand is the target (lvalue) and which is the source (rvalue)
        # Rule: Literals cannot be lvalues, address expressions are lvalues
        is_literal0 = self._is_literal_value(rendered0)
        is_literal1 = self._is_literal_value(rendered1)
        is_addr0 = self._is_address_expression(rendered0) or alias0.startswith("&")
        is_addr1 = self._is_address_expression(rendered1) or alias1.startswith("&")

        # Decision logic:
        # Priority 1: Detect array indexing patterns - these are always targets
        # Pattern: GADR/DADR + (index * size) = ADD with GADR/DADR and MUL inputs
        def is_array_pattern(value: SSAValue) -> bool:
            """Check if value is array indexing pattern: base_addr + (index * size)"""
            if not value.producer_inst or value.producer_inst.mnemonic != "ADD":
                return False
            if len(value.producer_inst.inputs) != 2:
                return False
            array_notation = self._detect_array_indexing(value)
            if array_notation and "[" in array_notation:
                return True
            left = value.producer_inst.inputs[0]
            right = value.producer_inst.inputs[1]
            # Check if left is base address (GADR/DADR/LADR)
            is_base = left.producer_inst and left.producer_inst.mnemonic in {"GADR", "DADR", "LADR"}
            # Check if right is multiplication (index * size)
            is_mul = right.producer_inst and right.producer_inst.mnemonic in {"MUL", "IMUL"}
            return is_base and is_mul

        def is_struct_field_pattern(value: SSAValue) -> bool:
            """Check if value is struct field access: (base_addr + index*size) + field_offset
            Also handles: PNT(base + index) + offset"""
            if not value.producer_inst:
                return False
            if value.producer_inst.mnemonic != "ADD":
                return False
            if len(value.producer_inst.inputs) != 2:
                return False
            left = value.producer_inst.inputs[0]
            right = value.producer_inst.inputs[1]

            # If left is PNT, look through it to find underlying array pattern
            check_value = left
            if left.producer_inst and left.producer_inst.mnemonic == "PNT" and len(left.producer_inst.inputs) == 1:
                check_value = left.producer_inst.inputs[0]

            # Check if left (or underlying) is array indexing and right is small constant
            if is_array_pattern(check_value):
                # Check if right looks like field offset (small constant)
                try:
                    offset_str = self._render_value(right)
                    offset = int(offset_str)
                    if 0 <= offset < 128:
                        return True
                except (ValueError, AttributeError) as e:
                    pass
            return False

        is_array0 = is_array_pattern(inst.inputs[0])
        is_array1 = is_array_pattern(inst.inputs[1])
        is_struct0 = is_struct_field_pattern(inst.inputs[0])
        is_struct1 = is_struct_field_pattern(inst.inputs[1])

        # Priority 1a: If one is struct field pattern, it's the target
        if is_struct1 and not is_struct0:
            target = self._format_pointer_target(inst.inputs[1])
            source = rendered0
        elif is_struct0 and not is_struct1:
            target = self._format_pointer_target(inst.inputs[0])
            source = rendered1
        # Priority 1b: If one is array pattern, it's the target
        elif is_array1 and not is_array0:
            target = self._format_pointer_target(inst.inputs[1])
            source = rendered0
        elif is_array0 and not is_array1:
            target = self._format_pointer_target(inst.inputs[0])
            source = rendered1
        # Priority 1c: PNT result is always an address target (struct/array field write)
        # PNT (pointer arithmetic) produces a computed address that's always a write target.
        # This must come before address heuristics since PNT may render as a tmp name.
        elif is_pnt1 and not is_pnt0:
            target = self._format_pointer_target(inst.inputs[1])
            source = rendered0
        elif is_pnt0 and not is_pnt1:
            target = self._format_pointer_target(inst.inputs[0])
            source = rendered1
        # Priority 2: Standard heuristics
        # 1. If one is literal and other is address → address is target, literal is source
        # 2. If both are addresses → use alias/PNT heuristics
        # 3. If neither is address → comment out as invalid
        elif is_literal0 and is_addr1:
            # input[0] is literal (source), input[1] is address (target)
            target = self._format_pointer_target(inst.inputs[1])
            source = rendered0
        elif is_literal1 and is_addr0:
            # input[1] is literal (source), input[0] is address (target)
            target = self._format_pointer_target(inst.inputs[0])
            source = rendered1
        elif is_addr1 and not is_addr0:
            # Only input[1] is address → it's the target
            target = self._format_pointer_target(inst.inputs[1])
            source = rendered0
        elif is_addr0 and not is_addr1:
            # Only input[0] is address → it's the target
            target = self._format_pointer_target(inst.inputs[0])
            source = rendered1
        elif alias1.startswith("&") and not alias0.startswith("&"):
            # inputs[1] is target address (by alias)
            target = self._format_pointer_target(inst.inputs[1])
            source = rendered0
        else:
            # Default: inputs[0] is source (value), inputs[1] is target (address)
            # VM semantics: ASGN(value, address) stores value to address
            target = self._format_pointer_target(inst.inputs[1])
            source = rendered0

        # Skip emission if target is still not a valid lvalue
        if self._is_literal_value(target):
            # This is likely a broken store - skip it entirely
            return None

        # Validate lvalue: target must be a valid C lvalue (variable, array subscript,
        # struct field, or pointer dereference). Arithmetic expressions are NOT valid lvalues.
        if not self._is_valid_lvalue(target):
            # Emit as comment instead of invalid C code
            return f"/* invalid store: {target} = {source}; */"

        # FLOAT CONSTANT FIX: If target is a known float field (e.g., vec.x, vec.z),
        # re-render the source value with float type hint
        target_field_type = self._detect_target_field_type(target)
        if target_field_type == 'float' and not call_expr_override:
            # Re-render source with float type hint
            # Determine which input is the source based on the same logic above
            source_input = inst.inputs[0] if target == self._format_pointer_target(inst.inputs[1]) else inst.inputs[1]
            source = self._render_value(source_input, expected_type_str='float')
        elif target_field_type is None and '.' in target and not call_expr_override:
            # Unknown struct field - check if source looks like a float constant
            # and re-render with float type hint if so
            try:
                source_val = int(source)
                if _is_likely_float(source_val):
                    source_input = inst.inputs[0] if target == self._format_pointer_target(inst.inputs[1]) else inst.inputs[1]
                    source = self._render_value(source_input, expected_type_str='float')
            except ValueError:
                pass
        elif not call_expr_override:
            # FIX (01-21): Also check plain local variable assignments for float constants
            # This catches cases like: local_0 = 1106247680 (should be local_0 = 30.0f)
            try:
                source_val = int(source)
                if _is_likely_float(source_val):
                    source_input = inst.inputs[0] if target == self._format_pointer_target(inst.inputs[1]) else inst.inputs[1]
                    source = self._render_value(source_input, expected_type_str='float')
            except ValueError:
                pass

        # Expression simplification: x = x ± 1 → x++/x--
        # Match patterns: (target + 1), (target - 1), target + 1, target - 1
        import re
        # Try with parentheses first
        inc_pattern = rf"^\({re.escape(target)}\s*\+\s*1\)$"
        dec_pattern = rf"^\({re.escape(target)}\s*-\s*1\)$"
        # Try without parentheses
        inc_pattern_no_paren = rf"^{re.escape(target)}\s*\+\s*1$"
        dec_pattern_no_paren = rf"^{re.escape(target)}\s*-\s*1$"

        if re.match(inc_pattern, source) or re.match(inc_pattern_no_paren, source):
            return f"{target}++;"
        if re.match(dec_pattern, source) or re.match(dec_pattern_no_paren, source):
            return f"{target}--;"

        # Expression simplification: x = x <op> y → x <op>= y
        # FIX: Also check SSA structure for compound patterns when source is a temp variable
        # This handles cases where the source was rendered as tmpN instead of inlined
        compound_ops = {
            "+": "+=",
            "-": "-=",
            "*": "*=",
            "/": "/=",
        }

        # Map mnemonics to operators for SSA-based detection
        mnemonic_to_op = {
            "IADD": "+", "FADD": "+", "DADD": "+", "ADD": "+",
            "ISUB": "-", "FSUB": "-", "DSUB": "-", "SUB": "-",
            "IMUL": "*", "FMUL": "*", "DMUL": "*", "MUL": "*",
            "IDIV": "/", "FDIV": "/", "DDIV": "/", "DIV": "/",
        }

        # Check SSA structure for compound assignment pattern
        # Pattern: ASGN(ARITH_OP(target_load, rhs), target_addr)
        # where target_load reads from the same location as target_addr
        source_val = inst.inputs[0]
        if source_val.producer_inst and source_val.producer_inst.mnemonic in mnemonic_to_op:
            arith_inst = source_val.producer_inst
            op_symbol = mnemonic_to_op[arith_inst.mnemonic]
            if op_symbol in compound_ops and len(arith_inst.inputs) >= 2:
                left_input = arith_inst.inputs[0]
                right_input = arith_inst.inputs[1]

                # Render both operands
                left_rendered = self._render_value(left_input)
                right_rendered = self._render_value(right_input)

                # Check if left operand matches target (x = x + y -> x += y)
                if left_rendered == target:
                    return f"{target} {compound_ops[op_symbol]} {right_rendered};"

                # FIX: Check if left operand is a DCP (load) from the same address as target
                # This handles array[index]++ pattern where the load and store use same address
                if left_input.producer_inst and left_input.producer_inst.mnemonic == "DCP":
                    # Get the address that DCP loaded from
                    dcp_inst = left_input.producer_inst
                    if len(dcp_inst.inputs) > 0:
                        load_addr = dcp_inst.inputs[0]
                        # Get the address being stored to (inst.inputs[1] for ASGN)
                        store_addr = inst.inputs[1] if len(inst.inputs) > 1 else None
                        # Check if load and store address expressions are equivalent
                        if store_addr and load_addr.producer_inst and store_addr.producer_inst:
                            # Compare rendered addresses
                            load_addr_rendered = self._format_pointer_target(load_addr)
                            store_addr_rendered = self._format_pointer_target(store_addr)
                            if load_addr_rendered == store_addr_rendered:
                                # Same address - this is a compound assignment!
                                # Special case: += 1 -> ++, -= 1 -> --
                                if right_rendered == "1":
                                    if op_symbol == "+":
                                        return f"{target}++;"
                                    elif op_symbol == "-":
                                        return f"{target}--;"
                                return f"{target} {compound_ops[op_symbol]} {right_rendered};"

                # For commutative ops (+, *), check if right matches target (x = y + x -> x += y)
                if op_symbol in {"+", "*"} and right_rendered == target:
                    return f"{target} {compound_ops[op_symbol]} {left_rendered};"

                # FIX: Also check right operand for DCP from same address (commutative)
                if op_symbol in {"+", "*"} and right_input.producer_inst and right_input.producer_inst.mnemonic == "DCP":
                    dcp_inst = right_input.producer_inst
                    if len(dcp_inst.inputs) > 0:
                        load_addr = dcp_inst.inputs[0]
                        store_addr = inst.inputs[1] if len(inst.inputs) > 1 else None
                        if store_addr and load_addr.producer_inst and store_addr.producer_inst:
                            load_addr_rendered = self._format_pointer_target(load_addr)
                            store_addr_rendered = self._format_pointer_target(store_addr)
                            if load_addr_rendered == store_addr_rendered:
                                # Special case: += 1 -> ++
                                if left_rendered == "1" and op_symbol == "+":
                                    return f"{target}++;"
                                return f"{target} {compound_ops[op_symbol]} {left_rendered};"

        # Fallback: Try string-based pattern matching on rendered source
        simplified_source = source.strip()
        if simplified_source.startswith("(") and simplified_source.endswith(")"):
            simplified_source = simplified_source[1:-1].strip()

        for op_symbol, compound in compound_ops.items():
            op_regex = re.escape(op_symbol)
            left_pattern = rf"^{re.escape(target)}\s*{op_regex}\s*(.+)$"
            match = re.match(left_pattern, simplified_source)
            if match:
                rhs = match.group(1).strip()
                if rhs:
                    return f"{target} {compound} {rhs};"
            if op_symbol in {"+", "*"}:
                right_pattern = rf"^(.+)\s*{op_regex}\s*{re.escape(target)}$"
                match = re.match(right_pattern, simplified_source)
                if match:
                    rhs = match.group(1).strip()
                    if rhs:
                        return f"{target} {compound} {rhs};"

        # Track constant assignments for text annotation (struct pointer arguments)
        # Pattern: local_80.field0 = 9136 -> track for SC_MissionSave(&local_80)
        self._track_text_id_assignment(target, source, inst)

        return f"{target} = {source};"

    @staticmethod
    def _is_parametric_alias(alias: str) -> bool:
        return alias.startswith("param_") or alias.startswith("info->")

    def _remap_param_alias(self, alias: str) -> str:
        """Remap a param_N alias to the correct parameter name using _param_names.

        Heritage SSA assigns param_N where N = abs(runtime_offset) - 3.
        Runtime offset = -(N + 3). We look up _param_names[-(N+3)] which was
        populated with both entry and runtime offsets.
        """
        if not self._param_names_by_index:
            return alias

        # Handle &param_N (address-of parameter)
        is_addr_of = alias.startswith("&")
        clean_alias = alias[1:] if is_addr_of else alias

        if clean_alias.startswith("param_"):
            try:
                heritage_k = int(clean_alias[6:])
                # Heritage SSA: param_K where K = abs(frame_offset) - 3.
                # Frame offset = -(K + 3).
                # Direct lookup in _param_names (keyed by frame offset):
                frame_offset = -(heritage_k + 3)
                if frame_offset in self._param_names:
                    result = self._param_names[frame_offset]
                    return f"&{result}" if is_addr_of else result

                # Fallback: compute sig_index from heritage K.
                # Void functions:     sig_index = n_params - 1 - K
                # Non-void functions: K=0 is return slot, params at K>=1
                #                     sig_index = n_params - K
                n_params = self._param_count
                if self._func_returns_value:
                    if heritage_k == 0:
                        return alias  # K=0 is return value, not a param
                    sig_index = n_params - heritage_k
                else:
                    sig_index = n_params - 1 - heritage_k
                if 0 <= sig_index < n_params and sig_index in self._param_names_by_index:
                    result = self._param_names_by_index[sig_index]
                    return f"&{result}" if is_addr_of else result
            except ValueError:
                pass
        return alias


    def _resolve_known_constant_for_variable(self, variable_expr: str, value: int) -> Optional[str]:
        """Resolve known SDK constants by variable name context."""
        return get_known_constant_for_variable(variable_expr, value)

    def _inline_expression(
        self,
        value: SSAValue,
        context: ExpressionContext = ExpressionContext.IN_EXPRESSION,
        parent_operator: Optional[str] = None
    ) -> str:
        cache_key = value.name
        if cache_key in self._inline_cache:
            return self._inline_cache[cache_key]
        # Use _inline_visiting for inline-specific cycle detection
        # This is separate from _visiting (used by _render_value) to prevent
        # false cycle detection when _render_value calls _inline_expression
        if cache_key in self._inline_visiting:
            return value.name
        inst = value.producer_inst
        if inst is None:
            return value.name
        self._inline_visiting.add(cache_key)

        # SPECIAL CASE: Check if ADD is actually structure field access or redundant +0
        # Pattern: ADD(PNT(ADR(local_X), offset1), offset2) → &local_X.fieldN
        if inst.mnemonic == "ADD" and len(inst.inputs) == 2:
            # First check if right side is 0 (redundant +0)
            try:
                right_str = self._render_value(inst.inputs[1])
                if right_str == "0":
                    # ADD(expr, 0) → expr (identity)
                    expr = self._render_value(inst.inputs[0])
                    self._inline_visiting.remove(cache_key)
                    self._inline_cache[cache_key] = expr
                    return expr
            except:
                pass

            # Check if left is already field access: &local_X.fieldN + offset → &local_X.field(N+offset/4)
            try:
                left_str = self._render_value(inst.inputs[0])
                right_str = self._render_value(inst.inputs[1])

                # Pattern: &local_X.fieldN + offset (legacy field_N format only)
                # Note: This handles old field_N format for backward compatibility
                if left_str.startswith("&") and ".field_" in left_str:
                    import re
                    match = re.match(r'^&(\w+)\.field_(\d+)$', left_str)
                    if match:
                        base_var = match.group(1)
                        base_offset = int(match.group(2))
                        offset_add = int(right_str)

                        # Calculate new field offset (byte offset, not dword index)
                        new_offset = base_offset + offset_add
                        field_name = self._resolve_field_name(base_var, new_offset)
                        # FIX (01-21): Use semantic name for struct field accesses
                        display_name = self._get_field_base_name(base_var, field_name)
                        expr = f"&{display_name}.{field_name}"
                        self._inline_visiting.remove(cache_key)
                        self._inline_cache[cache_key] = expr
                        return expr
            except:
                pass

            # Then check for structure field access
            field_notation = self._detect_array_indexing(value)
            if field_notation:
                # This is structure field access, return address of field
                expr = f"&{field_notation}"
                self._inline_visiting.remove(cache_key)
                self._inline_cache[cache_key] = expr
                return expr

        if inst.mnemonic in INFIX_OPS and len(inst.inputs) == 2:
            # WORKAROUND: Check if input[0] is PHI with address alias but should be array load
            # This happens when SSA construction loses DCP value from stack
            # Pattern: SUB/ADD has PHI input, but preceding DCP loads from array

            # Get operator for left/right children
            current_op = INFIX_OPS[inst.mnemonic]

            # Determine expected operand type from mnemonic (float/double ops need typed operands)
            operand_type = _get_operand_type_from_mnemonic(inst.mnemonic)

            # Render left operand with context
            left_inst = inst.inputs[0].producer_inst
            left_op = INFIX_OPS.get(left_inst.mnemonic) if left_inst else None
            left_operand = self._render_value(inst.inputs[0], expected_type_str=operand_type, parent_operator=current_op)

            # Render right operand with context
            right_inst = inst.inputs[1].producer_inst
            right_op = INFIX_OPS.get(right_inst.mnemonic) if right_inst else None
            right_operand = self._render_value(inst.inputs[1], expected_type_str=operand_type, parent_operator=current_op)

            # If left operand is address-like (&param_X or &local_X) and this might be broken PHI
            if (inst.inputs[0].alias and inst.inputs[0].alias.startswith("&") and
                inst.inputs[0].producer_inst and inst.inputs[0].producer_inst.mnemonic == "PHI"):
                # Search for recent DCP with array pattern (within ~10 instructions before)
                for search_addr in range(inst.address - 1, max(0, inst.address - 15), -1):
                    if search_addr in self._recent_array_loads:
                        # Found it! Use array load instead of PHI alias
                        left_operand = self._recent_array_loads[search_addr]
                        break

            if inst.mnemonic in COMPARISON_OPS:
                left_const = self._get_constant_int(inst.inputs[0])
                right_const = self._get_constant_int(inst.inputs[1])
                if left_const is None and right_const is not None:
                    const_name = self._resolve_known_constant_for_variable(left_operand, right_const)
                    if const_name:
                        right_operand = const_name
                elif right_const is None and left_const is not None:
                    const_name = self._resolve_known_constant_for_variable(right_operand, left_const)
                    if const_name:
                        left_operand = const_name

            # FIX 3: Smart parenthesization based on operator precedence and context
            # Check if left operand needs parens
            left_needs_parens = needs_parens(
                child_expr=left_operand,
                child_operator=left_op,
                parent_operator=current_op,
                context=context,
                is_left_operand=True
            )
            left_wrapped = wrap_if_needed(left_operand, left_needs_parens)

            # Check if right operand needs parens
            right_needs_parens = needs_parens(
                child_expr=right_operand,
                child_operator=right_op,
                parent_operator=current_op,
                context=context,
                is_left_operand=False
            )
            right_wrapped = wrap_if_needed(right_operand, right_needs_parens)

            # Build expression without automatic parentheses
            expr_without_parens = f"{left_wrapped} {current_op} {right_wrapped}"

            # Check if the whole expression needs parens based on parent context
            expr_needs_parens = needs_parens(
                child_expr=expr_without_parens,
                child_operator=current_op,
                parent_operator=parent_operator,
                context=context,
                is_left_operand=True  # Conservative default
            )
            expr = wrap_if_needed(expr_without_parens, expr_needs_parens)
        elif inst.mnemonic in UNARY_PREFIX and len(inst.inputs) == 1:
            # FIX 3: Smart parenthesization for unary operators
            unary_op = UNARY_PREFIX[inst.mnemonic]
            operand = self._render_value(inst.inputs[0], parent_operator=unary_op)

            # Unary operators rarely need parens around them, but the operand might
            # For now, keep simple approach - no outer parens unless parent requires it
            expr_without_parens = f"{unary_op}{operand}"

            # Check if whole expression needs parens based on parent
            expr_needs_parens = needs_parens(
                child_expr=expr_without_parens,
                child_operator=unary_op,
                parent_operator=parent_operator,
                context=context,
                is_left_operand=True
            )
            expr = wrap_if_needed(expr_without_parens, expr_needs_parens)
        elif inst.mnemonic in {"INC", "CINC", "SINC"} and len(inst.inputs) == 1:
            # INC opcodes: render as (operand + 1)
            # This enables _format_store to detect x = x + 1 → x++ pattern
            operand = self._inline_expression(inst.inputs[0], context, parent_operator="+")
            expr_without_parens = f"{operand} + 1"
            expr_needs_parens = needs_parens(
                child_expr=expr_without_parens,
                child_operator="+",
                parent_operator=parent_operator,
                context=context,
                is_left_operand=True
            )
            expr = wrap_if_needed(expr_without_parens, expr_needs_parens)
        elif inst.mnemonic in {"DEC", "CDEC", "SDEC"} and len(inst.inputs) == 1:
            # DEC opcodes: render as (operand - 1)
            # This enables _format_store to detect x = x - 1 → x-- pattern
            operand = self._inline_expression(inst.inputs[0], context, parent_operator="-")
            expr_without_parens = f"{operand} - 1"
            expr_needs_parens = needs_parens(
                child_expr=expr_without_parens,
                child_operator="-",
                parent_operator=parent_operator,
                context=context,
                is_left_operand=True
            )
            expr = wrap_if_needed(expr_without_parens, expr_needs_parens)
        elif inst.mnemonic in CAST_OPS and len(inst.inputs) >= 1:
            # Handle type conversion operations
            arg_text = self._render_value(inst.inputs[0])
            # Check if argument needs wrapping (only for complex expressions)
            needs_wrap = not is_simple_expression(arg_text)

            if inst.mnemonic == "FTOD":
                # Float to double conversion
                expr = f"(double){wrap_if_needed(arg_text, needs_wrap)}"
            elif inst.mnemonic == "DTOF":
                # Double to float conversion
                expr = f"(float){wrap_if_needed(arg_text, needs_wrap)}"
            elif inst.mnemonic == "ITOD":
                # Int to double conversion
                expr = f"(double){wrap_if_needed(arg_text, needs_wrap)}"
            elif inst.mnemonic == "DTOI":
                # Double to int conversion
                expr = f"(int){wrap_if_needed(arg_text, needs_wrap)}"
            elif inst.mnemonic == "ITOF":
                # Int to float conversion
                expr = f"(float){wrap_if_needed(arg_text, needs_wrap)}"
            elif inst.mnemonic == "FTOI":
                # Float to int conversion
                expr = f"(int){wrap_if_needed(arg_text, needs_wrap)}"
            else:
                # Other cast operations (SCI, SSI, UCI, USI - sign/zero extension)
                expr = f"{inst.mnemonic}({arg_text})"
        # FIX #4: Handle double-precision arithmetic operations
        # These operations have 4 inputs (2 doubles = 4 dwords) but should render as binary operators
        elif inst.mnemonic in {"DMUL", "DADD", "DSUB", "DDIV"} and len(inst.inputs) >= 2:
            # Use first 2 inputs as left and right operands
            # (inputs 2-3 are high dwords, handled internally by stack)
            current_op = INFIX_OPS.get(inst.mnemonic, inst.mnemonic)
            # Double operations need double operand type for proper literal rendering
            operand_type = _get_operand_type_from_mnemonic(inst.mnemonic)
            left_operand = self._render_value(inst.inputs[0], expected_type_str=operand_type, parent_operator=current_op)
            right_operand = self._render_value(inst.inputs[1], expected_type_str=operand_type, parent_operator=current_op)

            # Apply smart parenthesization
            left_inst = inst.inputs[0].producer_inst
            left_op = INFIX_OPS.get(left_inst.mnemonic) if left_inst else None
            left_needs_parens = needs_parens(
                child_expr=left_operand,
                child_operator=left_op,
                parent_operator=current_op,
                context=context,
                is_left_operand=True
            )
            left_wrapped = wrap_if_needed(left_operand, left_needs_parens)

            right_inst = inst.inputs[1].producer_inst
            right_op = INFIX_OPS.get(right_inst.mnemonic) if right_inst else None
            right_needs_parens = needs_parens(
                child_expr=right_operand,
                child_operator=right_op,
                parent_operator=current_op,
                context=context,
                is_left_operand=False
            )
            right_wrapped = wrap_if_needed(right_operand, right_needs_parens)

            expr_without_parens = f"{left_wrapped} {current_op} {right_wrapped}"
            expr_needs_parens = needs_parens(
                child_expr=expr_without_parens,
                child_operator=current_op,
                parent_operator=parent_operator,
                context=context,
                is_left_operand=True
            )
            expr = wrap_if_needed(expr_without_parens, expr_needs_parens)
        elif inst.mnemonic == "PNT" and len(inst.inputs) >= 1:
            # PNT (pointer with offset) - render as address expression or struct field
            # The offset is stored in the instruction's arg1, NOT on the stack

            # Get offset from instruction arg1
            offset_num = 0
            if inst.instruction and inst.instruction.instruction:
                offset_num = inst.instruction.instruction.arg1

            # SPECIAL CASE 1: Check if input is array indexing and offset is field offset
            # Pattern: PNT(ADD(base, index*size), field_offset) → array[index].field_N
            if offset_num > 0 and offset_num < 128:  # Reasonable field offset range
                array_notation = self._detect_array_indexing(inst.inputs[0])
                if array_notation:
                    # Extract base variable from array notation (e.g., "enum_pl[0]" -> "enum_pl")
                    base_var = array_notation.split('[')[0] if '[' in array_notation else array_notation
                    field_name = self._resolve_field_name(base_var, offset_num)
                    # Input is array indexing, create struct field access
                    expr = f"{array_notation}.{field_name}"
                    self._inline_visiting.remove(cache_key)
                    self._inline_cache[cache_key] = expr
                    return expr

            # SPECIAL CASE 2: Check if input is plain structure field access
            # Pattern: PNT(ADD(ADR(local_X), field_offset)) → local_X.fieldN
            # This handles expressions like *(&local_13 + 32)
            if inst.inputs[0].producer_inst and inst.inputs[0].producer_inst.mnemonic == "ADD":
                add_inst = inst.inputs[0].producer_inst
                if len(add_inst.inputs) == 2:
                    left = add_inst.inputs[0]
                    right = add_inst.inputs[1]

                    # Check if left is ADR
                    if left.producer_inst and left.producer_inst.mnemonic in {"LADR", "GADR", "DADR"}:
                        base_name = self._render_value(left)
                        if base_name.startswith("&"):
                            base_name = base_name[1:]

                            # Check if right is constant offset
                            try:
                                field_offset_str = self._render_value(right)
                                field_offset = int(field_offset_str)

                                # Add PNT offset to field offset (both are byte offsets)
                                total_offset = field_offset + offset_num

                                # Reasonable field offset range
                                if 0 <= total_offset < 256:
                                    field_name = self._resolve_field_name(base_name, total_offset)
                                    # FIX (01-21): Use semantic name for struct field accesses
                                    display_name = self._get_field_base_name(base_name, field_name)
                                    expr = f"&{display_name}.{field_name}"
                                    self._inline_visiting.remove(cache_key)
                                    self._inline_cache[cache_key] = expr
                                    return expr
                            except (ValueError, AttributeError):
                                pass

            # SPECIAL CASE 3: Simple structure field access
            # Pattern: PNT(ADR(local_X), offset) → &local_X.field_N
            if inst.inputs[0].producer_inst and inst.inputs[0].producer_inst.mnemonic in {"LADR", "GADR", "DADR"}:
                base_name = self._render_value(inst.inputs[0])
                if base_name.startswith("&") and offset_num > 0:
                    base_name = base_name[1:]
                    # Simple structure field access (offset is byte offset)
                    field_name = self._resolve_field_name(base_name, offset_num)
                    # FIX (01-21): Use semantic name for struct field accesses
                    display_name = self._get_field_base_name(base_name, field_name)
                    expr = f"&{display_name}.{field_name}"
                    self._inline_visiting.remove(cache_key)
                    self._inline_cache[cache_key] = expr
                    return expr

            # Regular rendering
            base = self._render_value(inst.inputs[0])

            # Try to detect structure field access
            field_name = None
            base_var = None
            if base.startswith("&"):
                base_var = base[1:]
            elif inst.inputs[0].alias and inst.inputs[0].alias.startswith("&"):
                base_var = inst.inputs[0].alias[1:]

            if base_var and offset_num > 0:
                field_name = self._get_struct_field(base_var, offset_num)

            if field_name:
                # Render as struct field address: &base_var.field
                # FIX (01-21): Use semantic name for struct field accesses
                display_name = self._get_field_base_name(base_var, field_name)
                expr = f"&{display_name}.{field_name}"
            elif offset_num == 0:
                expr = base
            else:
                expr = f"({base} + {offset_num})"
        elif inst.mnemonic == "DCP" and len(inst.inputs) == 1:
            # DCP (dereference/load) - render as dereferenced value
            addr_value = inst.inputs[0]
            addr_rendered = self._render_value(addr_value)

            # Pattern: DCP(&local_X) → local_X (dereference of address literal)
            if addr_rendered.startswith("&"):
                expr = addr_rendered[1:]  # Remove & to get the value
            # Pattern: DCP(data_X) → data_X (implicit load from data segment)
            elif addr_value.alias and addr_value.alias.startswith("data_"):
                expr = addr_rendered  # data_X already represents the value
            # Pattern: DCP(pointer_expr) → *pointer_expr (explicit dereference)
            else:
                expr = f"(*{addr_rendered})"
        elif inst.mnemonic == "XCALL":
            # XCALL return value - inline the function call expression
            # This enables nested calls like SC_AnsiToUni(SC_P_GetName(x), ...)
            call_expr = self._format_call(inst)
            # _format_call returns "func(args);" - strip the trailing semicolon
            if call_expr.endswith(";"):
                call_expr = call_expr[:-1]
            # Also strip any assignment prefix if present (e.g., "ret = func(args)")
            if " = " in call_expr:
                call_expr = call_expr.split(" = ", 1)[1]
            expr = call_expr
        else:
            expr = value.name
        self._inline_visiting.remove(cache_key)
        self._inline_cache[cache_key] = expr
        return expr

    def _format_target(self, value: SSAValue) -> str:
        name = self._value_name(value)

        # Check for global variable (data_XXX -> gVarName or &data_XXX -> &gVarName)
        if value.alias and value.alias.startswith("data_"):
            try:
                offset = int(value.alias[5:])
                global_name = self._global_names.get(offset)
                if global_name:
                    return global_name
            except ValueError:
                pass
        elif value.alias and value.alias.startswith("&data_"):
            try:
                offset = int(value.alias[6:])
                global_name = self._global_names.get(offset)
                if global_name:
                    return f"&{global_name}"
            except ValueError:
                pass

        if value.alias and value.alias.startswith("local_"):
            # Check if this is a field of a structure
            struct_field = self._get_struct_field_for_local(value.alias)
            if struct_field:
                return struct_field
            # Check for semantic name (loop counter, etc.)
            semantic_name = self._semantic_names.get(value.alias)
            if semantic_name:
                # FÁZE 1.2: Check uniqueness - prevent i==i collision
                if semantic_name not in self._used_semantic_names:
                    self._used_semantic_names.add(semantic_name)
                    return semantic_name  # Use semantic name instead of local_X
                # Name collision - fallback to local_X
            # Regular local variable
            if name not in self._declared:
                self._declared.add(name)
                type_name = TYPE_NAMES.get(value.value_type, "int")
                return f"{type_name} {name}"
        return name

    def _format_phi(self, inst: SSAInstruction) -> str:
        target = self._format_target(inst.outputs[0]) if inst.outputs else "<tmp>"
        sources = inst.outputs[0].phi_sources or []
        formatted_sources: List[str] = []
        for pred, source_name in sources:
            # Get SSAValue by name and use _render_value to apply global names
            source_val = self.ssa.values.get(source_name)
            if source_val:
                display = self._render_value(source_val)
            else:
                display = source_name
            formatted_sources.append(f"b{pred}:{display}")
        joined = ", ".join(formatted_sources) if formatted_sources else "?"
        return f"{target} = phi({joined})"

    def _format_call(self, inst: SSAInstruction) -> str:
        # FÁZE 4: CALL - internal function call
        if inst.mnemonic == "CALL":
            func_name = "unknown_func"
            call_addr = None

            # Get target address from CALL argument
            if inst.instruction and inst.instruction.instruction:
                call_addr = inst.instruction.instruction.arg1

                # Find function name by address
                for fname, (start_addr, end_addr) in self._function_bounds.items():
                    if start_addr == call_addr:
                        func_name = fname
                        break

            # STACK MANIPULATION FIX: Use inst.inputs directly
            # The compiler uses stack manipulation (ASP/LADR/ASGN), not PUSH.
            # Arguments are extracted during SSA lifting and stored in inst.inputs.
            rendered_args = []
            for arg_val in inst.inputs:
                arg_str = self._render_value(arg_val)
                rendered_args.append(arg_str)
            args = ", ".join(rendered_args)

            # Return function call expression - note: CALL can return value!
            # Check if there's an output (return value)
            if inst.outputs:
                dest = self._format_target(inst.outputs[0])
                return f"{dest} = {func_name}({args});"
            else:
                return f"{func_name}({args});"

        # XCALL - get function name from XFN table
        if inst.mnemonic == "XCALL":
            func_name = "XCALL"
            arg_types: List[str] = []
            is_variadic = False
            fixed_param_count = 0

            if inst.instruction and inst.instruction.instruction:
                xfn_idx = inst.instruction.instruction.arg1
                xfn_entry = self.ssa.scr.get_xfn(xfn_idx) if self.ssa.scr else None
                if xfn_entry:
                    # Extract just the function name (before signature in parentheses)
                    full_name = xfn_entry.name
                    paren_idx = full_name.find("(")
                    func_name = full_name[:paren_idx] if paren_idx > 0 else full_name
                    # Parse argument types from signature for type-aware rendering
                    arg_types = _parse_xfn_arg_types(full_name)

                    # Try to get better signature from header database
                    func_sig = self._header_db.get_function_signature(func_name)
                    if func_sig:
                        if func_sig.get('parameters'):
                            # Use parsed parameter types from header (more accurate)
                            arg_types = [param[0] for param in func_sig['parameters']]
                        # Check if function is variadic
                        is_variadic = func_sig.get('is_variadic', False)
                        if is_variadic:
                            fixed_param_count = len(arg_types)

            # Determine how many arguments to render
            num_args_to_render = len(inst.inputs)
            if is_variadic and fixed_param_count > 0:
                # For variadic functions: The Vietcong compiler pushes extra metadata after variadic args
                # This metadata is typically small integer constants (stack frame info, debug data, etc.)
                #
                # Strategy: Count arguments that look like "real" user code:
                # - All fixed parameters (always include these)
                # - Variadic arguments that aren't suspicious small constants
                #
                # Heuristic to detect compiler metadata:
                # 1. If total args <= fixed + 3, likely all are real (common case: printf-style with 1-2 format args)
                # 2. Otherwise, scan variadic args and stop at first small constant that looks like metadata

                actual_input_count = len(inst.inputs)

                # New strategy: ALWAYS scan variadic args and filter metadata
                # Don't use a simple threshold - actually check each arg
                num_args_to_render = fixed_param_count  # Start with fixed params

                for i in range(fixed_param_count, actual_input_count):
                    val = inst.inputs[i]

                    # Check if this looks like compiler metadata
                    # Strategy: Look for data_X references that resolve to small constants
                    is_likely_metadata = False

                    # Check the alias/name pattern
                    val_name = getattr(val, 'alias', None) or getattr(val, 'name', '')

                    # If it's a data segment reference, try to get its value
                    if val_name.startswith('data_'):
                        # Check if we can get constant value
                        const_val = getattr(val, 'constant_value', None)

                        # Also check if this value will render as a small number
                        # by temporarily rendering it
                        try:
                            rendered = self._render_value(val)
                            # If it renders as a single-digit number, likely metadata
                            if rendered.isdigit() and len(rendered) <= 2:
                                int_val = int(rendered)
                                # Small constants (0-10) are suspicious as trailing variadic args
                                # Exception: first variadic arg could legitimately be small
                                # (e.g., SC_Log(3, "msg") where 3 is level is fixed param, not variadic)
                                if i > fixed_param_count and 0 <= int_val <= 10:
                                    is_likely_metadata = True
                        except:
                            pass

                    if is_likely_metadata:
                        # Stop here - rest is metadata
                        break

                    num_args_to_render += 1

                    # Safety limit: don't render more than 10 variadic args total
                    if num_args_to_render >= fixed_param_count + 10:
                        break

            # Render args with type-aware rendering and constant substitution
            rendered_args = []
            for i in range(num_args_to_render):
                val = inst.inputs[i]
                # Get expected type for this argument (if available)
                expected_type = arg_types[i] if i < len(arg_types) else None
                # Render with type hint to avoid "ÿ" instead of 255
                arg_str = self._render_value(val, expected_type_str=expected_type)
                # Try to substitute constants for specific functions
                # Pass rendered_args for context-aware substitution (e.g., MISSION_* when first arg is SGI_CURRENTMISSION)
                arg_str = self._substitute_constant(func_name, i, arg_str, rendered_args)
                rendered_args.append(arg_str)
            args = ", ".join(rendered_args)

            # Check if XCALL has an output (return value)
            # External functions can return values too!

            # Build text annotation for functions that display text
            text_annotation = ""
            if should_annotate_function(func_name):
                # Extract numeric arguments that could be text IDs
                text_ids = []

                for idx, val in enumerate(inst.inputs[:num_args_to_render]):
                    # Try to get the constant value from SSA value
                    const_val = getattr(val, 'constant_value', None)
                    if const_val is not None and isinstance(const_val, int):
                        text_ids.append(const_val)
                    elif hasattr(val, 'value') and isinstance(val.value, int):
                        # Direct integer value
                        text_ids.append(val.value)
                    else:
                        # Check if this is a struct pointer argument (&local_X)
                        # If so, look up tracked assignments to that struct
                        rendered_arg = rendered_args[idx] if idx < len(rendered_args) else ""
                        if rendered_arg.startswith('&'):
                            var_name = rendered_arg[1:]  # Strip the &
                            struct_ids = self._struct_text_tracker.get_text_ids_for_var(var_name)
                            text_ids.extend(struct_ids)

                if text_ids:
                    annotation = format_text_annotation(text_ids)
                    if annotation:
                        text_annotation = f"  // {annotation}"

            if inst.outputs:
                dest = self._format_target(inst.outputs[0])
                return f"{dest} = {func_name}({args});{text_annotation}"
            else:
                return f"{func_name}({args});{text_annotation}"

        args = ", ".join(self._render_value(val) for val in inst.inputs)

        if inst.outputs:
            if inst.mnemonic == "GCP":
                dest = self._format_target(inst.outputs[0])
                literal = self._render_value(inst.outputs[0])
                return f"{dest} = {literal};"
            dest = self._format_target(inst.outputs[0])
            return f"{dest} = {inst.mnemonic}({args});"
        return f"{inst.mnemonic}({args});"

    def _substitute_constant(self, func_name: str, arg_index: int, arg_str: str,
                              rendered_args: List[str] = None) -> str:
        """
        Nahradí číselnou hodnotu argumentu symbolickou konstantou.

        Args:
            func_name: Name of the function being called
            arg_index: Index of the argument (0-based)
            arg_str: The rendered argument string
            rendered_args: List of already-rendered arguments (for context-aware substitution)
        """
        # Pokus o parsování jako číslo
        try:
            value = int(arg_str)
        except ValueError:
            return arg_str

        # Kontextové nahrazení podle funkce
        if func_name in ("SC_ggi", "SC_sgi"):
            # První argument je SGI index
            if arg_index == 0:
                name = get_constant_name("SGI", value)
                if name:
                    return name
            # Druhý argument může být MISSION_* když první je SGI_CURRENTMISSION
            elif arg_index == 1 and rendered_args:
                first_arg = rendered_args[0] if rendered_args else ""
                # Check if first arg is SGI_CURRENTMISSION (200) or its symbolic name
                if first_arg == "SGI_CURRENTMISSION" or first_arg == "200":
                    name = get_constant_name("MISSION", value)
                    if name:
                        return name
        elif func_name in ("SC_ggf", "SC_sgf"):
            # První argument je SGF index
            if arg_index == 0:
                name = get_constant_name("SGI", value)
                if name:
                    return name
        elif func_name == "SC_P_Ai_SetMode":
            if arg_index == 1:
                name = get_player_constant("AI_MODE", value)
                if name:
                    return name
        elif func_name == "SC_P_Ai_SetBattleMode":
            if arg_index == 1:
                name = get_player_constant("AI_BATTLEMODE", value)
                if name:
                    return name
        elif func_name == "SC_P_Ai_SetMoveMode":
            if arg_index == 1:
                name = get_player_constant("AI_MOVEMODE", value)
                if name:
                    return name
        elif func_name == "SC_P_Ai_SetMovePos":
            if arg_index == 1:
                name = get_player_constant("AI_MOVEPOS", value)
                if name:
                    return name
        elif func_name == "S_Mes":
            # Druhý argument je message type
            if arg_index == 1:
                name = get_constant_name("SCM", value)
                if name:
                    return name

        # Boolean hodnoty (0/1) pro poslední argument některých funkcí
        if value in (0, 1) and func_name in (
            "SC_P_Ai_EnableShooting", "SC_P_EnableSearchDeathBodies",
            "SC_P_SetActive", "SC_P_Ai_EnableSearchDeathBodies"
        ):
            return "TRUE" if value == 1 else "FALSE"

        return arg_str

    def _format_infix(self, inst: SSAInstruction, operator: str) -> str:
        if len(inst.inputs) != 2 or not inst.outputs:
            return self._format_call(inst)
        lhs, rhs = inst.inputs
        dst = self._format_target(inst.outputs[0])

        return f"{dst} = {self._render_value(lhs)} {operator} {self._render_value(rhs)};"

    def _format_unary(self, inst: SSAInstruction, prefix: str) -> str:
        if len(inst.inputs) != 1 or not inst.outputs:
            return self._format_call(inst)
        operand = inst.inputs[0]
        dst = self._format_target(inst.outputs[0])
        return f"{dst} = {prefix}{self._render_value(operand)};"


def _is_degenerate_phi(inst: SSAInstruction, ssa_func: Optional[SSAFunction] = None) -> bool:
    """Check if a PHI node is degenerate and should be skipped."""
    if not inst.outputs:
        return True
    output = inst.outputs[0]
    sources = output.phi_sources or []

    # Skip PHI with no sources or single source
    if len(sources) <= 1:
        return True

    # Skip PHI where all sources resolve to the same alias (no-op)
    # phi_sources is List[Tuple[int, str]] - (pred_block_id, source_name)
    output_alias = output.alias or output.name

    # Get aliases for source values
    source_aliases = set()
    source_values = []
    for _, src_name in sources:
        if ssa_func and src_name in ssa_func.values:
            src_val = ssa_func.values[src_name]
            source_aliases.add(src_val.alias or src_name)
            source_values.append(src_val)
        else:
            source_aliases.add(src_name)
            source_values.append(None)

    # If all sources resolve to the same alias AND it matches output, skip
    if len(source_aliases) == 1:
        single_alias = source_aliases.pop()
        if single_alias == output_alias or single_alias == output.name:
            return True

    # Skip PHI if all sources are the same constant value
    # (e.g., all sources are data_X pointing to same literal)
    if len(source_aliases) == 1:
        return True  # All sources are same value

    # Skip PHI if output has no uses (dead phi)
    if not output.uses:
        return True

    # Skip PHI where one source is the output itself (loop phi with single real source)
    real_sources = set()
    for _, src_name in sources:
        if src_name != output.name:
            if ssa_func and src_name in ssa_func.values:
                src_val = ssa_func.values[src_name]
                real_sources.add(src_val.alias or src_name)
            else:
                real_sources.add(src_name)
    if len(real_sources) == 1:
        return True

    return False


# Instructions that only establish aliases and should not be emitted
ADDRESS_LOAD_OPS = {"LADR", "GADR", "DADR"}

# Constant/value loading - values are inlined via alias, no statement needed
CONST_LOAD_OPS = {"GCP", "LCP", "LLD", "GLD", "DLD"}  # Various load operations

# Stack manipulation and side-effect only instructions - no output needed
STACK_OPS = {"SSP", "ASP"}  # Stack pointer manipulation
SIDE_EFFECT_OPS = {"DCP"}   # Data copy - used for passing struct arguments

# Control flow instructions - handled by structure.py
# NOTE: RET is NOT included here - it needs to be rendered as "return <value>;"
# FÁZE 4: CALL is NOT control flow - it's a function call statement that should be rendered
CONTROL_FLOW_OPS = {"JMP", "JZ", "JNZ"}  # Jumps only (not CALL)


def format_block_expressions(ssa_func: SSAFunction, block_id: int, formatter: ExpressionFormatter = None) -> List[FormattedExpression]:
    """
    Format expressions for a block.

    Args:
        ssa_func: SSA function data
        block_id: Block ID to format
        formatter: Optional ExpressionFormatter to use. If None, creates a new one.

    When formatter is provided (e.g., from format_structured_function_named),
    it ensures consistent per-function structure detection.
    """
    instructions = ssa_func.instructions.get(block_id, [])
    if formatter is None:
        formatter = ExpressionFormatter(ssa_func)

    # FÁZE 1.6 Pattern 2: Detect CALL/XCALL + LLD + ASGN patterns
    # Build a map of CALL addresses that should be merged with assignments
    call_to_assignment = {}  # call_addr -> asgn_inst
    # Pattern 3: Direct XCALL->ASGN (XCALL produces t###_ret which is directly used in ASGN)
    xcall_to_assignment = {}  # xcall_addr -> asgn_inst
    for i, inst in enumerate(instructions):
        if inst.mnemonic == "ASGN" and len(inst.inputs) >= 2:
            # Check if the source value comes from LLD
            source_val = inst.inputs[0]
            if source_val.producer_inst and source_val.producer_inst.mnemonic == "LLD":
                # Found ASGN with LLD source - now look backwards for CALL/XCALL
                lld_idx = i - 1
                while lld_idx >= 0 and instructions[lld_idx] != source_val.producer_inst:
                    lld_idx -= 1
                if lld_idx >= 0:
                    # Found LLD, now check for CALL/XCALL before it
                    for check_idx in range(lld_idx - 1, max(0, lld_idx - 3), -1):
                        if instructions[check_idx].mnemonic in {"CALL", "XCALL"}:
                            # Found CALL+LLD+ASGN pattern!
                            call_to_assignment[instructions[check_idx].address] = inst
                            break
            # Pattern 3: Direct XCALL->ASGN (XCALL output t###_ret used directly in ASGN)
            elif source_val.producer_inst and source_val.producer_inst.mnemonic == "XCALL":
                # Found ASGN with direct XCALL source (t###_ret pattern)
                xcall_inst = source_val.producer_inst
                xcall_to_assignment[xcall_inst.address] = inst

    formatted: List[FormattedExpression] = []

    def _to_signed32(val: int) -> int:
        return val - 0x100000000 if val >= 0x80000000 else val

    def _stack_alias_from_offset(offset: int) -> str:
        signed = _to_signed32(offset)
        if signed < 0 and signed <= -3:
            # Match the stack lifter's param alias: param_N where N = abs(offset) - 3
            param_idx = abs(signed) - 3
            return f"param_{param_idx}"
        elif signed < 0:
            return f"stack_{abs(signed)}"
        return f"local_{signed}"

    for inst in instructions:
        # WORKAROUND: Track DCP with array patterns for later use
        if inst.mnemonic == "DCP" and len(inst.inputs) > 0:
            array_load = formatter._detect_array_indexing(inst.inputs[0])
            if array_load:
                formatter._recent_array_loads[inst.address] = array_load

        # Skip all PHI nodes (SSA artifacts, not part of original code)
        if inst.mnemonic == "PHI":
            continue

        # Skip address load instructions - they only establish aliases for ASGN
        if inst.mnemonic in ADDRESS_LOAD_OPS:
            continue

        # Skip constant loading - values are inlined via alias
        if inst.mnemonic in CONST_LOAD_OPS:
            # LLD/GLD can also be stores (pops=1, pushes=0) - keep those
            if inst.mnemonic in {"LLD", "GLD"} and not inst.outputs:
                pass
            else:
                continue

        # Skip stack manipulation instructions
        if inst.mnemonic in STACK_OPS:
            continue

        # Skip side-effect only instructions
        if inst.mnemonic in SIDE_EFFECT_OPS:
            continue

        # Skip control flow instructions - handled by structure.py
        if inst.mnemonic in CONTROL_FLOW_OPS:
            continue

        # Dead code elimination: Skip if output is never used
        if inst.outputs:
            has_used_output = any(len(val.uses) > 0 for val in inst.outputs)
            if (not has_used_output and
                    inst.mnemonic not in formatter._store_ops and
                    inst.mnemonic not in {"CALL", "XCALL"}):
                # Output is never used - skip this instruction (dead code)
                continue

        has_out_params = inst.metadata.get("has_out_params", False) if inst.mnemonic in {"CALL", "XCALL"} else False
        should_emit = has_out_params or not inst.outputs or not all(
            formatter._can_inline(val) for val in inst.outputs
        )
        if not should_emit:
            continue

        # Handle LLD/GLD store patterns (pops=1, pushes=0)
        if inst.mnemonic in {"LLD", "GLD"} and not inst.outputs:
            if inst.instruction and inst.instruction.instruction and inst.inputs:
                raw_offset = inst.instruction.instruction.arg1
                if inst.mnemonic == "LLD":
                    signed_offset = _to_signed32(raw_offset)
                    if signed_offset >= 0:
                        target = _stack_alias_from_offset(raw_offset)
                    else:
                        target = None
                else:
                    target = formatter._global_names.get(raw_offset, f"data_{raw_offset}")
                if target:
                    source = formatter.render_value(inst.inputs[0])
                    formatted.append(
                        FormattedExpression(text=f"{target} = {source};", address=inst.address, mnemonic=inst.mnemonic)
                    )
            continue

        store_text = formatter._format_store(inst)
        if store_text:
            formatted.append(
                FormattedExpression(text=store_text, address=inst.address, mnemonic=inst.mnemonic)
            )
            continue
        elif store_text is None and inst.mnemonic in formatter._store_ops:
            # Store instruction that couldn't be rendered - skip it entirely
            continue
        if inst.mnemonic in INFIX_OPS:
            formatted.append(
                FormattedExpression(
                    text=formatter._format_infix(inst, INFIX_OPS[inst.mnemonic]),
                    address=inst.address,
                    mnemonic=inst.mnemonic,
                )
            )
            continue
        if inst.mnemonic in UNARY_PREFIX:
            formatted.append(
                FormattedExpression(
                    text=formatter._format_unary(inst, UNARY_PREFIX[inst.mnemonic]),
                    address=inst.address,
                    mnemonic=inst.mnemonic,
                )
            )
            continue
        # Handle RET instruction
        if inst.mnemonic == "RET":
            # RET instruction: arg1 is the STACK CLEANUP SIZE (number of dwords to pop),
            # NOT the number of values returned. A function returns a value only if there's
            # an LLD [sp-3] instruction before the RET that stores to the return slot.

            # Look for LLD [sp-3] pattern in preceding instructions
            # This pattern stores a value to the return slot
            return_value = None
            inst_idx = instructions.index(inst)
            for prev_idx in range(inst_idx - 1, max(0, inst_idx - 5), -1):
                prev_inst = instructions[prev_idx]
                if prev_inst.mnemonic == "LLD":
                    # Check if this LLD stores to return slot (offset -3)
                    if prev_inst.instruction and prev_inst.instruction.instruction:
                        offset = prev_inst.instruction.instruction.arg1
                        # Convert unsigned to signed
                        if offset >= 0x80000000:
                            offset = offset - 0x100000000
                        if offset == -3:
                            # This LLD stores to return slot - find the value
                            # The value was pushed before LLD (look at prev_inst's input)
                            if prev_inst.inputs:
                                return_value = formatter.render_value(prev_inst.inputs[0])
                            break
                # Stop searching if we hit another control flow instruction
                elif prev_inst.mnemonic in {"JMP", "JZ", "JNZ", "CALL", "XCALL"}:
                    break

            if return_value:
                # Replace 0/1 with FALSE/TRUE for boolean returns
                if return_value == "1":
                    return_value = "TRUE"
                elif return_value == "0":
                    return_value = "FALSE"

                formatted.append(
                    FormattedExpression(
                        text=f"return {return_value};",
                        address=inst.address,
                        mnemonic=inst.mnemonic,
                    )
                )
            else:
                # Return void (RET 0)
                # BUGFIX (07-ERROR6): RET 0 means the function returns nothing (void).
                # Don't check scr.header.ret_size - that's for ScriptMain, not this function.
                # A void function should just have "return;" or nothing (implicit return).
                formatted.append(
                    FormattedExpression(
                            text="return;",
                            address=inst.address,
                            mnemonic=inst.mnemonic,
                        )
                    )
            continue

        # FÁZE 1.6 Pattern 2: Skip CALL/XCALL if it's part of CALL+LLD+ASGN pattern
        if inst.address in call_to_assignment:
            # This call will be merged with the assignment - don't emit standalone
            continue

        # Pattern 3: Skip XCALL if its t###_ret output is directly used in ASGN
        if inst.address in xcall_to_assignment:
            # This XCALL will be rendered by the ASGN - don't emit standalone
            continue

        formatted.append(
            FormattedExpression(
                text=formatter._format_call(inst),
                address=inst.address,
                mnemonic=inst.mnemonic,
            )
        )
    return formatted
