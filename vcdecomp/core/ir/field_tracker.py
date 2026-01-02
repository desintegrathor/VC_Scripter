"""
Field Access Tracker for VC Script Decompiler.

Tracks struct field accesses through temporary values and reconstructs
proper field expressions like `info->master_nod` instead of `t33_0`.

Pattern detection:
    PNT(param_0, 4) → temp1       # pointer + offset
    DCP(temp1) → t33_0             # dereference
    → t33_0 represents param_0.master_nod (field at offset 4)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set

from ..disasm import opcodes
from .ssa import SSAFunction, SSAValue, SSAInstruction
from ..structures import get_field_at_offset, get_struct_by_name


# Known function signatures: func_name → (struct_type, param_index)
KNOWN_FUNCTION_SIGNATURES: Dict[str, tuple] = {
    "ScriptMain": ("s_SC_OBJ_info", 0),
    "_init": ("s_SC_OBJ_info", 0),
}


@dataclass
class FieldAccess:
    """Represents a struct field access."""

    base_var: str
    """Base variable name (e.g., 'param_0', 'local_0')"""

    struct_type: str
    """Structure type name (e.g., 's_SC_OBJ_info')"""

    field_offset: int
    """Byte offset into the structure"""

    field_name: Optional[str] = None
    """Field name if known (e.g., 'master_nod')"""

    is_pointer: bool = False
    """True if accessing through pointer (-> vs .)"""


class FieldAccessTracker:
    """
    Tracks struct field accesses through SSA instructions.

    Detects patterns:
    1. Direct access: local_0 is struct, local_1 is local_0.field
    2. Pointer arithmetic + deref: PNT(param_0, offset) → DCP → field
    3. Propagation through temporaries

    Usage:
        tracker = FieldAccessTracker(ssa_func, "ScriptMain")
        tracker.analyze()
        expr = tracker.get_field_expression(some_value)
        if expr:
            print(expr)  # "info->master_nod"
    """

    def __init__(self, ssa_func: SSAFunction, func_name: str = None):
        self.ssa = ssa_func
        self.scr = ssa_func.scr
        self.func_name = func_name or "ScriptMain"

        # SSA value name → FieldAccess
        self.field_map: Dict[str, FieldAccess] = {}

        # Variable name → struct type (e.g., param_0 → s_SC_OBJ_info)
        self.var_struct_types: Dict[str, str] = {}

        # Semantic names for base variables (param_0 → info)
        self.semantic_names: Dict[str, str] = {}

    def analyze(self):
        """Main analysis entry point - runs all tracking passes."""
        self._detect_param_structs()
        self._track_pnt_dcp_pattern()
        # _propagate_through_temps() is implicitly handled by _track_pnt_dcp_pattern

    def get_field_expression(self, value: SSAValue) -> Optional[str]:
        """
        Returns field expression for SSA value if it represents a struct field access.

        Args:
            value: SSA value to check

        Returns:
            Field expression like "info->master_nod" if known, else None
        """
        field_access = self.field_map.get(value.name)
        if not field_access:
            return None

        # Get semantic name for base variable (param_0 → info)
        base_name = self.semantic_names.get(field_access.base_var, field_access.base_var)

        # Get field name
        field_name = field_access.field_name
        if not field_name:
            # Fallback: show offset
            field_name = f"field_{field_access.field_offset}"

        # Choose operator: -> for pointers, . for values
        operator = "->" if field_access.is_pointer else "."

        return f"{base_name}{operator}{field_name}"

    # =========================================================================
    # Internal analysis methods
    # =========================================================================

    def _detect_param_structs(self):
        """
        Detect parameter structure types from function signatures.

        For entry point functions (ScriptMain, _init), automatically detects
        the correct structure type based on script type detection.
        """
        # Check if this is an entry point function
        if self.func_name not in ("ScriptMain", "_init"):
            # Not an entry point, check static signatures
            signature = KNOWN_FUNCTION_SIGNATURES.get(self.func_name)
            if signature:
                struct_type, param_index = signature
                param_var = f"param_{param_index}"
                self.var_struct_types[param_var] = struct_type
                self.semantic_names[param_var] = "info"
            return

        # For entry point functions, use automatic script type detection
        from ..script_type_detector import detect_script_type
        struct_type = detect_script_type(self.scr)
        param_index = 0  # Entry points always have param_0

        # Map param_X to detected struct type
        param_var = f"param_{param_index}"
        self.var_struct_types[param_var] = struct_type

        # Assign semantic name (param_0 → info)
        self.semantic_names[param_var] = "info"

    def _track_pnt_dcp_pattern(self):
        """
        Track PNT (pointer + offset) followed by DCP (dereference) pattern.

        Pattern:
            LADR param_0        → address of param_0
            DADR 4              → add offset 4
            PNT                 → pointer arithmetic result
            DCP                 → dereference
            → result is param_0->field_at_offset_4

        This detects field accesses through pointers.
        """
        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                # Look for DCP instructions (dereference)
                if inst.mnemonic != "DCP":
                    continue

                if not inst.inputs or not inst.outputs:
                    continue

                # Get the address being dereferenced
                addr_value = inst.inputs[0]

                # Check if address comes from PNT (pointer arithmetic)
                if not addr_value.producer_inst:
                    continue

                producer = addr_value.producer_inst

                # Pattern 1: Direct PNT instruction
                if producer.mnemonic == "PNT":
                    field_access = self._analyze_pnt_instruction(producer)
                    if field_access and inst.outputs:
                        # Map output of DCP to field access
                        self.field_map[inst.outputs[0].name] = field_access
                    continue

                # Pattern 2: DADR followed by earlier pointer
                # (LADR loads address, DADR adds offset, result used in DCP)
                if producer.mnemonic == "DADR":
                    field_access = self._analyze_dadr_chain(producer)
                    if field_access and inst.outputs:
                        self.field_map[inst.outputs[0].name] = field_access
                    continue

    def _analyze_pnt_instruction(self, pnt_inst: SSAInstruction) -> Optional[FieldAccess]:
        """
        Analyze PNT instruction to extract field access info.

        PNT has two inputs: base pointer + offset
        Returns FieldAccess if valid struct field access detected.
        """
        if len(pnt_inst.inputs) < 2:
            return None

        base_value = pnt_inst.inputs[0]
        offset_value = pnt_inst.inputs[1]

        # Get base variable name (param_0, local_0, etc.)
        base_var = base_value.alias if base_value.alias else base_value.name

        # Check if base is a known struct
        struct_type = self.var_struct_types.get(base_var)
        if not struct_type:
            return None

        # Get offset value
        offset = self._get_constant_value(offset_value)
        if offset is None:
            return None

        # Lookup field at this offset
        field_name = get_field_at_offset(struct_type, offset)

        return FieldAccess(
            base_var=base_var,
            struct_type=struct_type,
            field_offset=offset,
            field_name=field_name,
            is_pointer=True,  # PNT is pointer arithmetic
        )

    def _analyze_dadr_chain(self, dadr_inst: SSAInstruction) -> Optional[FieldAccess]:
        """
        Analyze DADR chain to extract field access.

        Pattern:
            LADR &param_0  → address of param_0
            DADR 4         → add offset 4
            → represents &(param_0[4]) or param_0 + 4 (pointer arithmetic)

        When dereferenced: DCP(result) → param_0->field_at_offset_4
        """
        # DADR instruction contains offset in arg1
        if not dadr_inst.instruction or not dadr_inst.instruction.instruction:
            return None

        offset = dadr_inst.instruction.instruction.arg1

        # Find base address (input to DADR)
        if not dadr_inst.inputs:
            return None

        addr_value = dadr_inst.inputs[0]

        # Check if address comes from LADR (load address of local/param)
        if not addr_value.producer_inst:
            return None

        if addr_value.producer_inst.mnemonic != "LADR":
            return None

        # LADR output has alias like "&param_0" or "&local_0"
        # Extract base variable from alias
        if not addr_value.alias:
            return None

        # Remove & prefix to get base variable name
        alias_str = addr_value.alias
        if not alias_str.startswith("&"):
            return None

        base_var = alias_str[1:]  # Remove '&' prefix: "&param_0" → "param_0"

        # Check if base is a known struct
        struct_type = self.var_struct_types.get(base_var)
        if not struct_type:
            return None

        # Lookup field at this offset
        field_name = get_field_at_offset(struct_type, offset)

        return FieldAccess(
            base_var=base_var,
            struct_type=struct_type,
            field_offset=offset,
            field_name=field_name,
            is_pointer=True,  # Dereferencing pointer
        )

    def _get_constant_value(self, value: SSAValue) -> Optional[int]:
        """
        Get constant integer value from SSA value.

        Checks:
        - GCP/LCP loads from data segment
        - Immediate values in instruction arguments
        - Literal aliases
        """
        # Check if value has literal alias
        if value.alias and value.alias.isdigit():
            return int(value.alias)

        # Check if value comes from GCP (data segment load)
        if value.producer_inst and value.producer_inst.mnemonic == "GCP":
            inst = value.producer_inst
            if inst.instruction and inst.instruction.instruction:
                data_offset = inst.instruction.instruction.arg1
                byte_offset = data_offset * 4
                if self.scr.data_segment:
                    return self.scr.data_segment.get_dword(byte_offset)

        # Check if value comes from immediate push or similar
        # (This could be extended based on opcode patterns)

        return None
