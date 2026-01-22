"""
Constant Propagation Engine for VC Script Decompiler.

Trackuje konstanty across SSA instructions a mapuje je na symbolické názvy.

Příklad:
    GCP data_5  → načte hodnotu 52 z data segmentu
    52 → SCM_OBJECTDESTROYED (lookup v constants.py)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, List

from ..disasm import opcodes
from .ssa import SSAFunction, SSAValue, SSAInstruction
from ..constants import SCM_CONSTANTS, SGI_CONSTANTS, BESID_CONSTANTS
from ..headers.database import get_header_database


@dataclass
class ConstantValue:
    """Tracked constant value with optional symbolic name."""

    value: int | float
    """Numeric value of the constant"""

    source: str
    """Source of constant: 'data_segment', 'literal', 'immediate'"""

    symbol_name: Optional[str] = None
    """Symbolic name if known (e.g., 'SCM_OBJECTDESTROYED')"""

    value_type: opcodes.ResultType = opcodes.ResultType.INT
    """Type of the constant"""


class ConstantPropagator:
    """
    Tracks constant values through SSA graph.

    Detects:
    1. GCP/LCP loads from data segment → lookup in constants.py
    2. Immediate values in instructions (PUSH, arithmetic with literals)
    3. Propagation through PHI nodes (if all sources are same constant)
    4. Propagation through ASGN and simple arithmetic

    Usage:
        propagator = ConstantPropagator(ssa_func)
        propagator.analyze()
        const = propagator.get_constant(some_ssa_value)
        if const and const.symbol_name:
            print(const.symbol_name)  # "SCM_OBJECTDESTROYED"
    """

    def __init__(self, ssa_func: SSAFunction):
        self.ssa = ssa_func
        self.scr = ssa_func.scr

        # Value name → ConstantValue
        self.constants: Dict[str, ConstantValue] = {}

        # Data segment offset (in dwords) → symbolic constant name
        self.data_constants: Dict[int, str] = {}

        # Tracked literal values: value → symbol name
        self.literal_map: Dict[int, str] = {}

        # Load header database for comprehensive constant lookup
        self._header_db = get_header_database()

    def analyze(self):
        """Main analysis entry point - runs all constant tracking passes."""
        self._build_literal_map()
        self._scan_data_segment()
        self._track_gcp_loads()
        self._track_lcp_loads()
        self._track_immediate_values()
        self._propagate_through_phi()

    def get_constant(self, value: SSAValue) -> Optional[ConstantValue]:
        """
        Returns ConstantValue if the SSA value represents a known constant.

        Args:
            value: SSA value to check

        Returns:
            ConstantValue with symbol_name if known, else None
        """
        return self.constants.get(value.name)

    # =========================================================================
    # Internal analysis methods
    # =========================================================================

    def _build_literal_map(self):
        """Build reverse lookup: value → symbol for all constants from header database."""
        # First, load from hardcoded constants (backwards compatibility)
        for value, name in SCM_CONSTANTS.items():
            # Skip 0 and 1 - they are used as FALSE/TRUE booleans
            if value in (0, 1):
                continue
            self.literal_map[value] = name

        for value, name in SGI_CONSTANTS.items():
            if value not in self.literal_map and value not in (0, 1):
                self.literal_map[value] = name

        for value, name in BESID_CONSTANTS.items():
            if value not in self.literal_map and value not in (0, 1):
                self.literal_map[value] = name

        # Now load ALL constants from header database (437 from SC_DEF.H + 270 from SC_GLOBAL.H)
        # This will add many more constants like MISSION_*, SC_P_*, etc.
        for const_name, const_data in self._header_db.constants.items():
            value_str = const_data.get('value', '')
            try:
                # Parse value (handle hex and decimal)
                if value_str.startswith('0x'):
                    value = int(value_str, 16)
                else:
                    value = int(value_str)

                # Skip 0 and 1 (boolean values)
                if value in (0, 1):
                    continue

                # Add to map (header constants can override hardcoded ones if present)
                # Prioritize by prefix: SCM > SGI > others
                prefix = const_data.get('prefix', '')
                if prefix == 'SCM' or value not in self.literal_map:
                    self.literal_map[value] = const_name

            except (ValueError, TypeError):
                # Not a numeric constant (e.g., macro expression)
                pass

    def _scan_data_segment(self):
        """
        Scan data segment and map dword offsets to symbolic constants.

        For each 4-byte value in data segment:
        - Read the value
        - Look it up in literal_map (SCM/SGI/BESID constants)
        - Store offset → symbol mapping
        """
        data_seg = self.scr.data_segment
        if not data_seg or not data_seg.raw_data:
            return

        # Iterate through data segment in 4-byte chunks
        for offset in range(0, len(data_seg.raw_data), 4):
            if offset + 4 > len(data_seg.raw_data):
                break

            value = data_seg.get_dword(offset)

            # Check if this value is a known constant
            symbol = self.literal_map.get(value)
            if symbol:
                # Store mapping: data_X → symbol
                dword_index = offset // 4
                self.data_constants[dword_index] = symbol

    def _track_gcp_loads(self):
        """
        Track GCP (Global Constant Pointer) loads from data segment.

        Pattern:
            GCP <offset> → loads from data_segment[offset]

        If data_segment[offset] contains a known constant value,
        mark the output SSA value as that constant.
        """
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                if inst.mnemonic != "GCP":
                    continue

                # GCP has no inputs, pushes value from data segment
                if not inst.outputs:
                    continue

                # Get the data segment offset from instruction arg1
                if not inst.instruction or not inst.instruction.instruction:
                    continue

                data_offset = inst.instruction.instruction.arg1

                # Check if we have a symbolic constant at this offset
                symbol = self.data_constants.get(data_offset)

                # Get the actual value from data segment
                byte_offset = data_offset * 4
                value = self.scr.data_segment.get_dword(byte_offset)

                # Create ConstantValue
                const_val = ConstantValue(
                    value=value,
                    source="data_segment",
                    symbol_name=symbol,  # May be None if not recognized
                    value_type=inst.outputs[0].value_type,
                )

                # Store for this SSA value
                self._register_constant(inst.outputs[0], const_val)

    def _track_lcp_loads(self):
        """
        Track LCP (stack/parameter) loads that resolve to constants.

        LCP values can become constants when:
        - The loaded stack slot is a merged PHI of constant values
        - The alias itself is a numeric literal
        """
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                if inst.mnemonic != "LCP":
                    continue

                if not inst.outputs:
                    continue

                value = inst.outputs[0]
                if value.name in self.constants:
                    continue

                const_val = self._resolve_constant_from_alias(value)
                if const_val is None:
                    const_val = self._resolve_constant_from_phi_sources(value)

                if const_val is not None:
                    self._register_constant(value, const_val)

    def _track_immediate_values(self):
        """
        Track immediate constant values from instruction arguments.

        Some instructions embed constants directly in their arguments
        rather than loading from data segment.

        Examples:
            PUSH 1  → immediate constant 1
            IADD 5  → immediate constant 5
        """
        # This could be extended, but most constants come from GCP
        # For now, we focus on GCP as that's the main pattern
        for value in self.ssa.values.values():
            if value.name in self.constants:
                continue
            const_val = self._resolve_constant_from_alias(value)
            if const_val is not None:
                self._register_constant(value, const_val)

    def _propagate_through_phi(self):
        """
        Propagate constants through PHI nodes.

        If all inputs to a PHI node are the same constant,
        the PHI output is also that constant.

        Example:
            phi = PHI(const1, const2)
            if const1 == const2 == 52 (SCM_OBJECTDESTROYED)
            then phi is also 52 (SCM_OBJECTDESTROYED)
        """
        changed = True
        iterations = 0
        max_iterations = 10  # Prevent infinite loops

        while changed and iterations < max_iterations:
            changed = False
            iterations += 1

            for block_id, instructions in self.ssa.instructions.items():
                for inst in instructions:
                    if inst.mnemonic != "PHI":
                        continue

                    if not inst.outputs or not inst.inputs:
                        continue

                    # Check if output is already a known constant
                    if inst.outputs[0].name in self.constants:
                        continue

                    # Get constants from all inputs
                    input_constants: List[Optional[ConstantValue]] = []
                    for inp in inst.inputs:
                        input_constants.append(self.constants.get(inp.name))

                    # If any input is not a constant, PHI is not constant
                    if None in input_constants:
                        continue

                    # Check if all constants have the same value
                    first_const = input_constants[0]
                    if all(c.value == first_const.value for c in input_constants):
                        # All inputs are same constant → propagate to output
                        const_val = ConstantValue(
                            value=first_const.value,
                            source="phi_propagation",
                            symbol_name=first_const.symbol_name,
                            value_type=inst.outputs[0].value_type,
                        )
                        self._register_constant(inst.outputs[0], const_val)
                        changed = True

    def _register_constant(self, value: SSAValue, const_val: ConstantValue) -> None:
        """Register a constant for an SSA value and annotate the value."""
        self.constants[value.name] = const_val
        setattr(value, "constant_value", const_val.value)
        if const_val.symbol_name:
            setattr(value, "constant_symbol", const_val.symbol_name)

    def _resolve_constant_from_alias(self, value: SSAValue) -> Optional[ConstantValue]:
        """Resolve a constant from a numeric alias on the SSA value."""
        if not value.alias:
            return None

        parsed = self._parse_numeric_literal(value.alias)
        if parsed is None:
            return None

        symbol = self.literal_map.get(parsed)
        return ConstantValue(
            value=parsed,
            source="literal",
            symbol_name=symbol,
            value_type=value.value_type,
        )

    def _resolve_constant_from_phi_sources(self, value: SSAValue) -> Optional[ConstantValue]:
        """Resolve constant value from PHI sources if all sources are same constant."""
        if not value.phi_sources:
            return None

        constants: List[ConstantValue] = []
        for _, src_name in value.phi_sources:
            src_val = self.ssa.values.get(src_name)
            if not src_val:
                return None
            const_val = self.constants.get(src_val.name)
            if const_val is None:
                return None
            constants.append(const_val)

        if not constants:
            return None

        first = constants[0]
        if all(c.value == first.value for c in constants):
            return ConstantValue(
                value=first.value,
                source="phi_propagation",
                symbol_name=first.symbol_name,
                value_type=value.value_type,
            )
        return None

    def _parse_numeric_literal(self, text: str) -> Optional[int]:
        """Parse numeric literal text into an int if possible."""
        try:
            if text.startswith(("0x", "0X")):
                return int(text, 16)
            if text.isdigit() or (text.startswith("-") and text[1:].isdigit()):
                return int(text)
        except (ValueError, TypeError):
            return None
        return None
