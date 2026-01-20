"""
Unified Local Variable Type Tracker for VC Script Decompiler.

This module implements a two-pass architecture to solve the type mismatch problem
between variable declarations and usage patterns. The issue arises because:
1. ExpressionFormatter detects array/struct patterns during code generation
2. Variable collection generates declarations BEFORE knowing all usage patterns
3. Without a feedback loop, declarations don't match actual usage

Solution: LocalVariableTypeTracker coordinates:
- Pass 1: Pre-analyze SSA instructions for array/struct patterns BEFORE formatting
- Pass 2: Collect additional patterns discovered during expression formatting
- Finalization: Generate consistent declarations matching all detected usage
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Dict, Set, List, Optional, Tuple

from ..disasm import opcodes
from .ssa import SSAFunction, SSAValue, SSAInstruction
from ..structures import get_struct_by_name, get_field_at_offset, get_struct_by_size


@dataclass
class VariableUsageInfo:
    """Tracks all detected usage patterns for a single variable."""

    var_name: str
    """Canonical variable name (e.g., 'local_296', 'tmp')"""

    # Array usage patterns
    is_array: bool = False
    """Whether variable is used with array indexing: var[idx]"""

    array_element_sizes: Set[int] = field(default_factory=set)
    """Element sizes observed in MUL(idx, size) patterns"""

    max_array_index: Optional[int] = None
    """Maximum constant index observed (for static array sizing)"""

    # Struct usage patterns
    is_struct: bool = False
    """Whether variable is used with struct field access: var.field"""

    struct_type: Optional[str] = None
    """Known struct type (from field_tracker or function calls)"""

    field_offsets_accessed: Set[int] = field(default_factory=set)
    """Byte offsets accessed via .field notation"""

    min_struct_size: int = 0
    """Minimum required struct size (from highest field offset + field size)"""

    # Combined patterns
    is_struct_array: bool = False
    """Whether variable is array of structs: var[idx].field"""

    # Confidence and evidence tracking
    confidence: float = 0.0
    """Overall confidence in type detection (0.0 to 1.0)"""

    evidence_sources: List[str] = field(default_factory=list)
    """Sources of evidence: 'field_tracker', 'ssa_pattern', 'runtime', 'xcall'"""

    def update_array_evidence(self, element_size: int, index: Optional[int] = None, source: str = "unknown"):
        """Record evidence of array usage."""
        self.is_array = True
        self.array_element_sizes.add(element_size)
        if index is not None and (self.max_array_index is None or index > self.max_array_index):
            self.max_array_index = index
        if source not in self.evidence_sources:
            self.evidence_sources.append(source)
        self._recalculate_confidence()

    def update_struct_evidence(self, struct_type: Optional[str], offset: int, source: str = "unknown"):
        """Record evidence of struct field access."""
        self.is_struct = True
        self.field_offsets_accessed.add(offset)
        # Update struct type if we have better info
        if struct_type and (not self.struct_type or source == "field_tracker"):
            self.struct_type = struct_type
        # Update minimum struct size
        field_end = offset + 4  # Minimum field size
        if struct_type:
            struct_def = get_struct_by_name(struct_type)
            if struct_def:
                field_end = struct_def.size
        if field_end > self.min_struct_size:
            self.min_struct_size = field_end
        if source not in self.evidence_sources:
            self.evidence_sources.append(source)
        self._recalculate_confidence()

    def mark_struct_array(self, element_size: int, struct_type: Optional[str], source: str = "unknown"):
        """Mark as array of structs."""
        self.is_array = True
        self.is_struct_array = True
        self.array_element_sizes.add(element_size)
        if struct_type:
            self.struct_type = struct_type
        if source not in self.evidence_sources:
            self.evidence_sources.append(source)
        self._recalculate_confidence()

    def _recalculate_confidence(self):
        """Update confidence based on evidence strength."""
        # Base confidence from number of evidence sources
        base = 0.3 if len(self.evidence_sources) >= 1 else 0.0

        # Boost for field_tracker (high-confidence source)
        if "field_tracker" in self.evidence_sources:
            base = max(base, 0.8)

        # Boost for XCALL parameter inference
        if "xcall" in self.evidence_sources:
            base = max(base, 0.6)

        # Boost for multiple concordant SSA patterns
        if "ssa_pattern" in self.evidence_sources:
            base = max(base, 0.5)

        # Boost for runtime detection (during expression formatting)
        if "runtime" in self.evidence_sources:
            base = max(base, 0.5)

        # Struct type confirmation boosts confidence
        if self.struct_type:
            base = min(base + 0.2, 1.0)

        self.confidence = base


class LocalVariableTypeTracker:
    """
    Unified tracker for local variable type inference across decompilation passes.

    Coordinates between:
    - FieldAccessTracker (XCALL-based struct detection)
    - SSA pattern analysis (array indexing patterns)
    - Runtime expression formatting (discovered patterns)

    Usage:
        # Create before formatting
        tracker = LocalVariableTypeTracker(ssa_func, func_start, func_end, field_tracker)

        # Pass 1: Pre-analyze
        tracker.analyze_ssa_patterns(func_block_ids)
        tracker.import_field_tracker_results()

        # Pass 2: Set on formatter for runtime callbacks
        formatter.set_type_tracker(tracker)

        # ... formatting happens ...

        # Finalize and use for declarations
        tracker.finalize()
        var_type = tracker.resolve_type("local_296")
    """

    def __init__(
        self,
        ssa_func: SSAFunction,
        func_start: int,
        func_end: int,
        field_tracker=None,
        rename_map: Dict[str, str] = None
    ):
        """
        Initialize tracker for a specific function.

        Args:
            ssa_func: SSA function being decompiled
            func_start: Start address of function
            func_end: End address of function
            field_tracker: Optional FieldAccessTracker with XCALL-based detections
            rename_map: Optional SSA value name → final name mapping
        """
        self.ssa_func = ssa_func
        self.func_start = func_start
        self.func_end = func_end
        self.field_tracker = field_tracker
        self.rename_map = rename_map or {}

        # Main storage: variable name → usage info
        self._usage_info: Dict[str, VariableUsageInfo] = {}

        # Finalization flag
        self._finalized = False

        # Cache data segment for constant lookups
        self.data_segment = getattr(ssa_func.scr, 'data_segment', None) if ssa_func.scr else None

    def _get_or_create_info(self, var_name: str) -> VariableUsageInfo:
        """Get existing usage info or create new entry."""
        # Canonicalize name (strip & prefix, apply rename map)
        canonical = var_name.lstrip("&")
        # Apply rename map to get final name
        canonical = self.rename_map.get(canonical, canonical)

        if canonical not in self._usage_info:
            self._usage_info[canonical] = VariableUsageInfo(var_name=canonical)
        return self._usage_info[canonical]

    def get_usage_info(self, var_name: str) -> Optional[VariableUsageInfo]:
        """Get usage info for a variable (None if not tracked)."""
        canonical = var_name.lstrip("&")
        canonical = self.rename_map.get(canonical, canonical)
        return self._usage_info.get(canonical)

    # =========================================================================
    # Pass 1: Pre-analysis of SSA patterns
    # =========================================================================

    def analyze_ssa_patterns(self, func_block_ids: Set[int]):
        """
        Pre-analyze SSA instructions for array/struct patterns.

        This runs BEFORE expression formatting to detect patterns early.
        Patterns detected:
        - ADD(LADR(local_X), MUL(idx, size)) → array indexing
        - ADD(LADR(local_X), small_constant) → struct field access
        - PNT(LADR(local_X), offset) → pointer field access

        Args:
            func_block_ids: Block IDs belonging to this function
        """
        for block_id in func_block_ids:
            ssa_instrs = self.ssa_func.instructions.get(block_id, [])
            for inst in ssa_instrs:
                self._analyze_instruction(inst)

    def _analyze_instruction(self, inst: SSAInstruction):
        """Analyze single instruction for type patterns."""
        # Pattern 1: Array indexing - ADD(LADR(local_X), MUL(idx, size))
        if inst.mnemonic == "ADD" and len(inst.inputs) == 2:
            left = inst.inputs[0]
            right = inst.inputs[1]

            # Check if left is LADR of local variable
            base_var = self._extract_local_from_ladr(left)
            if base_var:
                # Check if right is MUL(idx, element_size)
                element_size, index = self._extract_mul_pattern(right)
                if element_size is not None:
                    info = self._get_or_create_info(base_var)
                    info.update_array_evidence(element_size, index, source="ssa_pattern")

                    # If element_size > 4, likely struct array
                    if element_size > 4:
                        struct_type = self._infer_struct_from_size(element_size)
                        info.mark_struct_array(element_size, struct_type, source="ssa_pattern")

                    print(f"DEBUG TypeTracker: Array pattern detected - {base_var}[*{element_size}]", file=sys.stderr)

                # Check if right is small constant (struct field offset)
                offset = self._extract_constant(right)
                if offset is not None and 0 < offset < 256:
                    # Could be struct field - check if we have struct type info
                    info = self._get_or_create_info(base_var)
                    existing_struct = info.struct_type
                    info.update_struct_evidence(existing_struct, offset, source="ssa_pattern")

        # Pattern 2: PNT instruction with offset
        if inst.mnemonic == "PNT" and len(inst.inputs) >= 1:
            base_var = self._extract_local_from_ladr(inst.inputs[0])
            if base_var and inst.instruction and inst.instruction.instruction:
                offset = inst.instruction.instruction.arg1
                info = self._get_or_create_info(base_var)
                # PNT with offset indicates struct access
                existing_struct = info.struct_type
                info.update_struct_evidence(existing_struct, offset, source="ssa_pattern")
                print(f"DEBUG TypeTracker: PNT pattern detected - {base_var}.field_{offset}", file=sys.stderr)

    def _extract_local_from_ladr(self, value: SSAValue) -> Optional[str]:
        """Extract local variable name if value comes from LADR."""
        # Check alias for &local_X pattern
        if value.alias and value.alias.startswith("&local_"):
            return value.alias[1:]  # Strip &

        # Check producer instruction
        if value.producer_inst and value.producer_inst.mnemonic == "LADR":
            if value.producer_inst.outputs:
                out = value.producer_inst.outputs[0]
                if out.alias and out.alias.startswith("&local_"):
                    return out.alias[1:]

        return None

    def _extract_mul_pattern(self, value: SSAValue) -> Tuple[Optional[int], Optional[int]]:
        """
        Extract (element_size, index) from MUL(idx, size) pattern.

        Returns (None, None) if not a MUL pattern.
        """
        if not value.producer_inst or value.producer_inst.mnemonic != "MUL":
            return None, None

        mul_inst = value.producer_inst
        if len(mul_inst.inputs) != 2:
            return None, None

        mul_left = mul_inst.inputs[0]
        mul_right = mul_inst.inputs[1]

        # Element size is typically the constant operand
        size_val = self._extract_constant(mul_right)
        if size_val is None:
            size_val = self._extract_constant(mul_left)
            index_val = self._extract_constant(mul_right)
        else:
            index_val = self._extract_constant(mul_left)

        # Validate: element_size should be positive and reasonable
        if size_val and 0 < size_val <= 256:
            return size_val, index_val

        return None, None

    def _extract_constant(self, value: SSAValue) -> Optional[int]:
        """Extract constant integer value from SSA value."""
        # Check if alias is numeric
        if value.alias:
            if value.alias.isdigit():
                return int(value.alias)
            # Check data segment reference
            if value.alias.startswith("data_") and self.data_segment:
                try:
                    offset = int(value.alias[5:])
                    return self.data_segment.get_dword(offset * 4)
                except (ValueError, AttributeError):
                    pass

        # Check constant_value attribute
        if hasattr(value, 'constant_value') and value.constant_value is not None:
            return value.constant_value

        return None

    def _infer_struct_from_size(self, size: int) -> Optional[str]:
        """Infer struct type from element size."""
        structs = get_struct_by_size(size)
        if structs and len(structs) == 1:
            return structs[0].name
        # Could add heuristics for ambiguous sizes here
        return None

    # =========================================================================
    # Import from FieldAccessTracker
    # =========================================================================

    def import_field_tracker_results(self):
        """
        Import high-confidence struct type detections from FieldAccessTracker.

        FieldAccessTracker uses XCALL argument analysis which is very reliable.
        """
        if not self.field_tracker:
            return

        for var_name, struct_type in self.field_tracker.var_struct_types.items():
            # Only process local variables
            clean_name = var_name.lstrip("&")
            if not clean_name.startswith("local_"):
                continue

            info = self._get_or_create_info(clean_name)

            # Field tracker detections are high confidence
            info.struct_type = struct_type
            info.is_struct = True
            info.confidence = max(info.confidence, 0.85)
            if "field_tracker" not in info.evidence_sources:
                info.evidence_sources.append("field_tracker")

            print(f"DEBUG TypeTracker: Imported field_tracker type - {clean_name} = {struct_type}", file=sys.stderr)

    # =========================================================================
    # Pass 2: Runtime callbacks from ExpressionFormatter
    # =========================================================================

    def record_array_usage(self, var_name: str, notation: str):
        """
        Callback when ExpressionFormatter emits array notation.

        Args:
            var_name: Base variable name (e.g., "local_296")
            notation: Full expression (e.g., "local_296[i]", "local_296[0].field")
        """
        if self._finalized:
            return

        info = self._get_or_create_info(var_name)
        # Extract element size from notation if possible (basic inference)
        info.update_array_evidence(4, None, source="runtime")  # Default element size

        # Check if this is struct array notation
        if "." in notation.split("]")[-1]:
            info.is_struct_array = True

        print(f"DEBUG TypeTracker: Runtime array usage - {notation}", file=sys.stderr)

    def record_field_usage(self, var_name: str, notation: str):
        """
        Callback when ExpressionFormatter emits field access notation.

        Args:
            var_name: Base variable name (e.g., "local_296")
            notation: Full expression (e.g., "local_296.side", "local_296[0].field")
        """
        if self._finalized:
            return

        info = self._get_or_create_info(var_name)
        # We don't have offset info here, just mark as struct
        info.is_struct = True
        if "runtime" not in info.evidence_sources:
            info.evidence_sources.append("runtime")

        print(f"DEBUG TypeTracker: Runtime field usage - {notation}", file=sys.stderr)

    # =========================================================================
    # Finalization and Type Resolution
    # =========================================================================

    def finalize(self):
        """
        Finalize type tracking after all formatting is complete.

        Resolves any ambiguities and marks tracker as read-only.
        """
        # Resolve struct array patterns
        for var_name, info in self._usage_info.items():
            # If both array and struct flags are set, it's struct array
            if info.is_array and info.is_struct:
                info.is_struct_array = True

            # If struct type unknown but is_struct, try to infer from field offsets
            if info.is_struct and not info.struct_type and info.field_offsets_accessed:
                max_offset = max(info.field_offsets_accessed)
                min_size = max_offset + 4
                possible_structs = get_struct_by_size(min_size)
                if possible_structs:
                    # Pick smallest struct that fits
                    info.struct_type = possible_structs[0].name

        self._finalized = True

        # Log final state
        print(f"DEBUG TypeTracker: Finalized with {len(self._usage_info)} tracked variables", file=sys.stderr)
        for name, info in sorted(self._usage_info.items()):
            type_str = self.resolve_type(name)
            print(f"DEBUG TypeTracker:   {name} -> {type_str} (confidence={info.confidence:.2f})", file=sys.stderr)

    def resolve_type(self, var_name: str) -> str:
        """
        Resolve final C type string for variable declaration.

        Priority order:
        1. Field tracker struct type (XCALL evidence) - highest confidence
        2. Struct array (array indexing + struct type)
        3. Plain array (array indexing without struct)
        4. Plain struct (field access with type)
        5. Unknown struct (field access without type) - emit int, not .field notation
        6. Default: int

        Args:
            var_name: Variable name to resolve

        Returns:
            C type string (e.g., "int", "s_SC_MP_EnumPlayers[64]", "c_Vector3")
        """
        info = self._usage_info.get(var_name)
        if not info:
            return "int"  # Default for unknown variables

        # Priority 0: Field tracker high-confidence struct (XCALL evidence)
        if info.struct_type and info.confidence >= 0.8:
            if info.is_struct_array or info.is_array:
                # Struct array
                size = self._estimate_array_size(info)
                return f"{info.struct_type}[{size}]"
            # Plain struct
            return info.struct_type

        # Priority 1: Struct array (both array + struct patterns)
        if info.is_struct_array:
            struct_type = info.struct_type or "dword"
            size = self._estimate_array_size(info)
            return f"{struct_type}[{size}]"

        # Priority 2: Plain array (no struct type)
        if info.is_array and not info.is_struct:
            size = self._estimate_array_size(info)
            return f"dword[{size}]"

        # Priority 3: Plain struct with known type
        if info.is_struct and info.struct_type and info.confidence >= 0.5:
            return info.struct_type

        # Priority 4: Unknown struct - DON'T emit .field notation
        # Return int to prevent invalid expressions like "int_var.field_4"
        if info.is_struct and not info.struct_type:
            return "int"

        return "int"  # Final fallback

    def _estimate_array_size(self, info: VariableUsageInfo) -> int:
        """Estimate array size from available evidence."""
        # Use max observed index + 1
        if info.max_array_index is not None:
            return info.max_array_index + 1

        # Default sizes based on struct type
        if info.struct_type:
            # Known patterns from Vietcong
            if info.struct_type == "s_SC_MP_EnumPlayers":
                return 64  # Standard player enum size
            if info.struct_type == "s_SC_FpvMapSign":
                return 64  # Map signs
            return 8  # Conservative default for struct arrays

        # Default for dword arrays
        return 16  # Conservative default

    def should_emit_array_notation(self, var_name: str) -> bool:
        """
        Check if ExpressionFormatter should emit array notation for this variable.

        Returns True only if variable is confirmed as array/struct array.
        This prevents emitting local_296[idx] when local_296 is declared as int.
        """
        info = self._usage_info.get(var_name)
        if not info:
            return False
        return info.is_array or info.is_struct_array

    def should_emit_field_notation(self, var_name: str) -> bool:
        """
        Check if ExpressionFormatter should emit field notation for this variable.

        Returns True only if variable has a known struct type.
        This prevents emitting local_296.field_4 when we don't know the struct type.
        """
        info = self._usage_info.get(var_name)
        if not info:
            return False
        return info.is_struct and info.struct_type is not None

    def get_tracked_variables(self) -> List[str]:
        """Get list of all tracked variable names."""
        return list(self._usage_info.keys())
