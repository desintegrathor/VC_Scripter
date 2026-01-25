"""
LoadGuard system for array access detection.

This module implements Ghidra-inspired LoadGuard tracking for indexed
memory access patterns. It detects array accesses by recognizing the
pattern: base + (index * elem_size)

Modeled after Ghidra's heritage.cc discoverIndexedStackPointers().

Key capabilities:
- Detect indexed memory access patterns
- Extract base address, index variable, and element size
- Infer array dimensions from loop bounds
- Mark variables as arrays for proper code generation
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from ..disasm import opcodes
from .ssa import SSAFunction, SSAInstruction, SSAValue

logger = logging.getLogger(__name__)


# =============================================================================
# Data Structures
# =============================================================================

@dataclass
class IndexedAccess:
    """
    Represents a detected indexed memory access (potential array access).

    Pattern: base + (index * elem_size)
    Example bytecode:
        LADR [EBP-40]   ; base (local variable address)
        PUSH i          ; index
        IMUL 4          ; elem_size
        IADD            ; base + offset
        ASGN/DCP        ; store/load
    """
    instruction: SSAInstruction          # The ASGN or DCP instruction
    address_value: SSAValue              # The computed address (output of IADD)
    base: SSAValue                       # Base address (from LADR/LCP/GADR)
    index: SSAValue                      # Index variable
    elem_size: Optional[int]             # Element size in bytes (4 for int, 1 for char, etc.)
    access_type: str                     # "store" or "load"

    # Metadata for dimension inference
    loop_header_block: Optional[int] = None     # Block ID of containing loop header
    loop_bound_value: Optional[SSAValue] = None # Upper bound from loop condition


@dataclass
class ArrayCandidate:
    """
    A variable that has been identified as a potential array.

    Collects multiple indexed accesses to the same base to infer:
    - Array dimensions
    - Element type
    - Access patterns
    """
    base_value: SSAValue                          # The base address SSA value
    base_variable_name: Optional[str] = None      # Variable name (from LADR offset)
    base_variable_offset: Optional[int] = None    # Stack offset or data offset

    accesses: List[IndexedAccess] = field(default_factory=list)

    # Inferred properties
    element_type: opcodes.ResultType = opcodes.ResultType.UNKNOWN
    element_size: Optional[int] = None            # Most common elem_size from accesses
    dimension: Optional[int] = None               # Array size (from loop bounds)
    confidence: float = 0.0                       # Confidence score (0.0-1.0)


# =============================================================================
# Pattern Recognition
# =============================================================================

class LoadGuard:
    """
    Tracks indexed memory access patterns for array detection.

    Analyzes SSA instructions to find the pattern:
        address = base + (index * elem_size)

    Where:
    - base: Address from LADR (local) or GADR (global)
    - index: Variable or expression
    - elem_size: Constant (1, 2, 4, 8, etc.)
    """

    def __init__(self, ssa_func: SSAFunction):
        self.ssa_func = ssa_func

        # Detected indexed accesses
        self.indexed_accesses: List[IndexedAccess] = []

        # Array candidates (grouped by base address)
        self.array_candidates: Dict[str, ArrayCandidate] = {}

        # Statistics
        self.stats = {
            "total_accesses_checked": 0,
            "indexed_accesses_found": 0,
            "array_candidates": 0,
            "dimensions_inferred": 0,
        }

    def discover_indexed_accesses(self) -> List[IndexedAccess]:
        """
        Scan SSA function for indexed memory accesses.

        Looks for ASGN and DCP operations where the address operand
        is computed as: base + (index * elem_size)

        Returns:
            List of detected indexed accesses
        """
        logger.debug("LoadGuard: Discovering indexed accesses...")

        for block_id, block_insts in self.ssa_func.instructions.items():
            for inst in block_insts:
                self.stats["total_accesses_checked"] += 1

                # Check ASGN (store) instructions
                if inst.mnemonic == "ASGN" and len(inst.inputs) >= 2:
                    addr_value = inst.inputs[1]  # Second input is address

                    indexed_access = self._analyze_address_computation(
                        addr_value, inst, "store", block_id
                    )
                    if indexed_access:
                        self.indexed_accesses.append(indexed_access)
                        self.stats["indexed_accesses_found"] += 1
                        logger.debug(
                            f"  Found store: {indexed_access.base.name}"
                            f"[{indexed_access.index.name}]"
                            f" (elem_size={indexed_access.elem_size})"
                        )

                # Check DCP (load via pointer) instructions
                elif inst.mnemonic == "DCP" and len(inst.inputs) >= 1:
                    addr_value = inst.inputs[0]  # First input is address

                    indexed_access = self._analyze_address_computation(
                        addr_value, inst, "load", block_id
                    )
                    if indexed_access:
                        self.indexed_accesses.append(indexed_access)
                        self.stats["indexed_accesses_found"] += 1
                        logger.debug(
                            f"  Found load: {indexed_access.base.name}"
                            f"[{indexed_access.index.name}]"
                            f" (elem_size={indexed_access.elem_size})"
                        )

        logger.info(
            f"LoadGuard: Found {self.stats['indexed_accesses_found']} "
            f"indexed accesses out of {self.stats['total_accesses_checked']} checked"
        )

        return self.indexed_accesses

    def _analyze_address_computation(
        self,
        addr_value: SSAValue,
        access_inst: SSAInstruction,
        access_type: str,
        block_id: int
    ) -> Optional[IndexedAccess]:
        """
        Analyze if an address computation matches indexed access pattern.

        Pattern to match: base + (index * elem_size)

        SSA form:
            temp1 = index * elem_size    (IMUL with constant)
            temp2 = base + temp1          (IADD/ADD)
            use temp2 in ASGN/DCP

        Also handles variations:
            - Direct: base + index (elem_size=1 implied)
            - Reversed: (index * elem_size) + base
            - Multiple levels of IADD
        """
        if not addr_value.producer_inst:
            return None

        addr_inst = addr_value.producer_inst

        # Primary pattern: IADD (or ADD for compatibility)
        if addr_inst.mnemonic in ("IADD", "ADD"):
            return self._analyze_iadd_pattern(addr_inst, access_inst, access_type, block_id)

        # Alternative: DADR (pointer arithmetic with immediate offset)
        elif addr_inst.mnemonic == "DADR":
            return self._analyze_dadr_pattern(addr_inst, access_inst, access_type, block_id)

        return None

    def _analyze_iadd_pattern(
        self,
        iadd_inst: SSAInstruction,
        access_inst: SSAInstruction,
        access_type: str,
        block_id: int
    ) -> Optional[IndexedAccess]:
        """
        Analyze IADD instruction for indexed access pattern.

        Expected: base + (index * elem_size)
        """
        if len(iadd_inst.inputs) != 2:
            return None

        left, right = iadd_inst.inputs

        # Try left as base, right as scaled index
        result = self._try_base_and_scaled_index(
            left, right, iadd_inst, access_inst, access_type, block_id
        )
        if result:
            return result

        # Try right as base, left as scaled index (commutative)
        result = self._try_base_and_scaled_index(
            right, left, iadd_inst, access_inst, access_type, block_id
        )
        if result:
            return result

        # Fallback: Check for base + index (elem_size=1 implied)
        if self._is_base_address(left):
            return IndexedAccess(
                instruction=access_inst,
                address_value=iadd_inst.outputs[0],
                base=left,
                index=right,
                elem_size=1,  # Implied byte access
                access_type=access_type
            )
        elif self._is_base_address(right):
            return IndexedAccess(
                instruction=access_inst,
                address_value=iadd_inst.outputs[0],
                base=right,
                index=left,
                elem_size=1,
                access_type=access_type
            )

        return None

    def _try_base_and_scaled_index(
        self,
        potential_base: SSAValue,
        potential_scaled: SSAValue,
        iadd_inst: SSAInstruction,
        access_inst: SSAInstruction,
        access_type: str,
        block_id: int
    ) -> Optional[IndexedAccess]:
        """
        Try to match: potential_base + potential_scaled
        where potential_scaled = index * elem_size
        """
        # Check if left is a base address
        if not self._is_base_address(potential_base):
            return None

        # Check if right is scaled index (index * elem_size)
        if not potential_scaled.producer_inst:
            return None

        scaled_inst = potential_scaled.producer_inst

        # Look for IMUL instruction
        if scaled_inst.mnemonic in ("IMUL", "MUL"):
            if len(scaled_inst.inputs) != 2:
                return None

            mul_left, mul_right = scaled_inst.inputs

            # One operand should be constant (elem_size), other is index
            elem_size = self._get_constant_value(mul_right)
            index = mul_left

            if elem_size is None:
                # Try reversed
                elem_size = self._get_constant_value(mul_left)
                index = mul_right

            if elem_size is not None and elem_size > 0:
                return IndexedAccess(
                    instruction=access_inst,
                    address_value=iadd_inst.outputs[0],
                    base=potential_base,
                    index=index,
                    elem_size=elem_size,
                    access_type=access_type
                )

        return None

    def _analyze_dadr_pattern(
        self,
        dadr_inst: SSAInstruction,
        access_inst: SSAInstruction,
        access_type: str,
        block_id: int
    ) -> Optional[IndexedAccess]:
        """
        Analyze DADR (pointer arithmetic with immediate) for array access.

        DADR adds a constant offset to an address from stack.
        Less common for dynamic indexing, but can appear in optimized code.
        """
        # DADR pattern is less suitable for dynamic array indexing
        # (it uses immediate offset, not a variable index)
        # We'll skip this for now and focus on IMUL+IADD pattern
        return None

    def _is_base_address(self, value: SSAValue) -> bool:
        """
        Check if SSA value represents a base address.

        Base addresses come from:
        - LADR: Local variable address (stack)
        - GADR: Global variable address (data segment)
        - LCP: Load constant/parameter (could be pointer)
        - Function parameters marked as pointers
        """
        if not value.producer_inst:
            # Could be a parameter
            if value.value_type == opcodes.ResultType.POINTER:
                return True
            return False

        inst = value.producer_inst

        # Direct address operations
        if inst.mnemonic in ("LADR", "GADR"):
            return True

        # LCP with pointer type
        if inst.mnemonic == "LCP" and value.value_type == opcodes.ResultType.POINTER:
            return True

        # DADR produces pointer
        if inst.mnemonic == "DADR":
            return True

        return False

    def _get_constant_value(self, value: SSAValue) -> Optional[int]:
        """Extract constant integer value from SSA value."""
        # Check metadata
        if "constant_value" in value.metadata:
            return value.metadata["constant_value"]

        # Check if name indicates constant
        if value.name.startswith("const_"):
            try:
                return int(value.name.split("_")[1])
            except (ValueError, IndexError):
                pass

        if value.name.startswith("lit_"):
            try:
                lit_part = value.name.split("_", 1)[1]
                if lit_part.startswith("0x"):
                    return int(lit_part, 16)
                return int(lit_part)
            except (ValueError, IndexError):
                pass

        # Check producer instruction (GCP loads constant from data)
        if value.producer_inst and value.producer_inst.mnemonic == "GCP":
            # Try to get value from data segment
            # This requires access to SCR file
            pass

        return None

    def group_into_array_candidates(self) -> Dict[str, ArrayCandidate]:
        """
        Group indexed accesses by base address to identify array candidates.

        Multiple accesses to the same base address suggest an array.
        """
        for access in self.indexed_accesses:
            base_name = access.base.name

            if base_name not in self.array_candidates:
                # Create new array candidate
                candidate = ArrayCandidate(
                    base_value=access.base,
                )

                # Try to extract variable info from LADR
                if access.base.producer_inst:
                    inst = access.base.producer_inst
                    if inst.mnemonic == "LADR" and inst.instruction:
                        # LADR has stack offset as arg1
                        offset = inst.instruction.instruction.arg1
                        candidate.base_variable_offset = offset
                        candidate.base_variable_name = f"local_{offset}"
                    elif inst.mnemonic == "GADR" and inst.instruction:
                        # GADR has data offset as arg1
                        offset = inst.instruction.instruction.arg1
                        candidate.base_variable_offset = offset
                        candidate.base_variable_name = f"global_{offset}"

                self.array_candidates[base_name] = candidate
                self.stats["array_candidates"] += 1

            # Add access to candidate
            self.array_candidates[base_name].accesses.append(access)

        # Infer properties for each candidate
        for candidate in self.array_candidates.values():
            self._infer_array_properties(candidate)

        logger.info(f"LoadGuard: Identified {len(self.array_candidates)} array candidates")

        return self.array_candidates

    def _infer_array_properties(self, candidate: ArrayCandidate):
        """
        Infer array properties from access patterns.

        Properties:
        - Element size (most common elem_size)
        - Element type (from elem_size: 1=char, 2=short, 4=int/float, 8=double)
        - Dimension (from loop bounds if available)
        - Confidence score
        """
        if not candidate.accesses:
            return

        # Element size: Use most common value
        elem_sizes = [a.elem_size for a in candidate.accesses if a.elem_size]
        if elem_sizes:
            # Count occurrences
            from collections import Counter
            size_counts = Counter(elem_sizes)
            candidate.element_size = size_counts.most_common(1)[0][0]

            # Infer type from size
            if candidate.element_size == 1:
                candidate.element_type = opcodes.ResultType.CHAR
            elif candidate.element_size == 2:
                candidate.element_type = opcodes.ResultType.SHORT
            elif candidate.element_size == 4:
                # Could be int or float, default to int
                # (will be refined by type inference later)
                candidate.element_type = opcodes.ResultType.INT
            elif candidate.element_size == 8:
                candidate.element_type = opcodes.ResultType.DOUBLE

        # Confidence: Higher if multiple accesses and consistent elem_size
        num_accesses = len(candidate.accesses)
        if num_accesses >= 3:
            candidate.confidence = 0.9
        elif num_accesses == 2:
            candidate.confidence = 0.7
        else:
            candidate.confidence = 0.5

        # Check consistency
        if elem_sizes and len(set(elem_sizes)) == 1:
            # All accesses use same element size
            candidate.confidence = min(1.0, candidate.confidence + 0.1)

        logger.debug(
            f"  Array candidate {candidate.base_variable_name or candidate.base_value.name}: "
            f"elem_size={candidate.element_size}, "
            f"elem_type={candidate.element_type.name}, "
            f"accesses={num_accesses}, "
            f"confidence={candidate.confidence:.2f}"
        )

    def infer_array_dimensions(self):
        """
        Infer array dimensions from loop bounds.

        Analyzes loops that iterate over arrays:
        - for (i = 0; i < N; i++) { arr[i] = ... }

        The upper bound N gives the array dimension.

        This requires loop analysis from the CFG.
        """
        # Get loop information from CFG
        cfg = self.ssa_func.cfg

        if not hasattr(cfg, 'natural_loops') or not cfg.natural_loops:
            logger.debug("LoadGuard: No loop information available for dimension inference")
            return

        # For each array candidate
        for candidate in self.array_candidates.values():
            # Look for accesses inside loops
            for access in candidate.accesses:
                # Find which loop this access is in
                access_block = access.instruction.block_id

                for loop_info in cfg.natural_loops:
                    if access_block in loop_info.body:
                        # This access is inside a loop
                        # Try to extract loop bound
                        dimension = self._extract_loop_bound(loop_info, access.index)
                        if dimension:
                            candidate.dimension = dimension
                            self.stats["dimensions_inferred"] += 1
                            logger.debug(
                                f"  Inferred dimension {dimension} for "
                                f"{candidate.base_variable_name or candidate.base_value.name}"
                            )
                            break

    def _extract_loop_bound(self, loop_info, index_variable: SSAValue) -> Optional[int]:
        """
        Extract upper bound from loop condition.

        Looks for patterns like:
        - i < N
        - i <= N-1

        Where i is the index_variable and N is a constant.
        """
        # This requires analyzing the loop header's condition
        # For now, return None (will implement in detail later)
        return None

    def mark_arrays_in_type_system(self):
        """
        Mark identified arrays in the type system.

        Updates SSA values with array metadata for proper code generation.
        """
        for candidate in self.array_candidates.values():
            if candidate.confidence < 0.5:
                continue  # Skip low-confidence candidates

            # Mark base value as array
            base_value = candidate.base_value
            base_value.metadata["is_array"] = True
            base_value.metadata["array_elem_type"] = candidate.element_type
            base_value.metadata["array_elem_size"] = candidate.element_size

            if candidate.dimension:
                base_value.metadata["array_dimension"] = candidate.dimension

            # Mark all accesses
            for access in candidate.accesses:
                access.instruction.metadata["array_access"] = True
                access.instruction.metadata["array_base"] = base_value.name
                access.instruction.metadata["array_index"] = access.index.name
                access.instruction.metadata["array_elem_size"] = access.elem_size

        logger.info(
            f"LoadGuard: Marked {len([c for c in self.array_candidates.values() if c.confidence >= 0.5])} "
            f"arrays in type system"
        )

    def get_statistics(self) -> Dict:
        """Get LoadGuard statistics."""
        return self.stats.copy()


# =============================================================================
# Public API
# =============================================================================

def discover_arrays(ssa_func: SSAFunction) -> LoadGuard:
    """
    Discover array access patterns in SSA function.

    This is the main entry point for array detection.

    Args:
        ssa_func: SSA function to analyze

    Returns:
        LoadGuard instance with discovered arrays

    Example:
        load_guard = discover_arrays(ssa_func)

        for candidate in load_guard.array_candidates.values():
            print(f"Array: {candidate.base_variable_name}")
            print(f"  Element type: {candidate.element_type.name}")
            print(f"  Element size: {candidate.element_size}")
            print(f"  Accesses: {len(candidate.accesses)}")
    """
    load_guard = LoadGuard(ssa_func)

    # Phase 1: Discover indexed accesses
    load_guard.discover_indexed_accesses()

    # Phase 2: Group into array candidates
    load_guard.group_into_array_candidates()

    # Phase 3: Infer dimensions (if loop info available)
    load_guard.infer_array_dimensions()

    # Phase 4: Mark in type system
    load_guard.mark_arrays_in_type_system()

    return load_guard
