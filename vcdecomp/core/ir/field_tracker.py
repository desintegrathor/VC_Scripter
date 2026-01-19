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
# NOTE: ScriptMain and _init use automatic script type detection,
# so they are NOT listed here. Only add non-entry-point functions here.
KNOWN_FUNCTION_SIGNATURES: Dict[str, tuple] = {
    # Example: "custom_callback": ("s_custom_struct", 0),
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
        self._detect_local_structs()  # NEW: Detect local struct types from function calls
        self._propagate_struct_types()  # NEW: Propagate struct types through assignments
        self._track_pnt_dcp_pattern()

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
        # Strip & prefix if present (PNT uses &local_X but we want local_X)
        base_var = field_access.base_var.lstrip("&")
        base_name = self.semantic_names.get(base_var, base_var)

        # Get field name
        field_name = field_access.field_name
        if not field_name:
            # Fallback: show offset
            field_name = f"field_{field_access.field_offset}"

        # Choose operator: -> for pointers, . for values
        operator = "->" if field_access.is_pointer else "."

        # DEBUG: Log field access mapping
        import sys
        print(f"DEBUG FieldTracker: {value.name} → {base_name}{operator}{field_name} (offset={field_access.field_offset}, struct={field_access.struct_type})", file=sys.stderr)

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

        # DEBUG: Log detected struct type
        import sys
        print(f"DEBUG FieldTracker: {self.func_name} param_0 detected as {struct_type}", file=sys.stderr)

    def _detect_local_structs(self):
        """
        Detect local struct types from function calls with address-of patterns.

        Pattern: XCALL SC_MP_SRV_GetAtgSettings(&local_1)
        → local_1 should be typed as s_SC_MP_SRV_AtgSettings

        Looks for XCALL instructions and checks if arguments are LADR of local variables.
        Then infers struct type from the function signature.
        """
        import sys
        from ..structures import FUNCTION_STRUCT_PARAMS

        for block_id, instructions in self.ssa.instructions.items():
            for i, inst in enumerate(instructions):
                # Look for XCALL (external function call) instructions
                if inst.mnemonic == "XCALL" and inst.instruction:
                    # Get the XFN entry from the instruction
                    lifted_inst = inst.instruction
                    if not hasattr(lifted_inst, 'instruction'):
                        continue

                    raw_inst = lifted_inst.instruction
                    xfn = self.scr.get_xfn(raw_inst.arg1)

                    if not xfn or not xfn.name:
                        continue

                    func_name_with_sig = xfn.name
                    # Strip signature to get bare function name: "SC_Foo(int,float)void" → "SC_Foo"
                    paren_idx = func_name_with_sig.find("(")
                    func_name = func_name_with_sig[:paren_idx] if paren_idx > 0 else func_name_with_sig

                    # DEBUG: Log all function names
                    if "GetAtgSettings" in func_name or "GetInfo" in func_name:
                        print(f"DEBUG FieldTracker: Checking func_name='{func_name}' (from '{func_name_with_sig}')", file=sys.stderr)

                    # Check if this function has known struct parameters
                    param_map = FUNCTION_STRUCT_PARAMS.get(func_name)
                    if not param_map:
                        continue

                    # DEBUG: Log when we find a known function
                    print(f"DEBUG FieldTracker: Found known function {func_name}, scanning for LADR", file=sys.stderr)

                    # Look backwards for LADR instructions (load address) before the call
                    # Stack is built backwards: last parameter is closest to XCALL
                    # For func(arg0, arg1), stack is: PUSH arg0, PUSH arg1, XCALL
                    # So we scan backwards: i-1 = arg1 (param index 1), i-2 = arg0 (param index 0)

                    # Collect LADR instructions working backwards from XCALL
                    ladr_instructions = []
                    j = i - 1
                    while j >= 0 and len(ladr_instructions) < 10:  # Max 10 params
                        prev_inst = instructions[j]
                        if prev_inst.mnemonic == "LADR" and prev_inst.outputs:
                            ladr_instructions.append((j, prev_inst))
                        elif prev_inst.mnemonic == "XCALL":
                            # Stop at another XCALL (different function call)
                            break
                        j -= 1

                    # Map LADR positions to parameter indices
                    # ladr_instructions[0] is closest to XCALL (last parameter)
                    # If we have 2 LADRs: [0] = param 1, [1] = param 0
                    for ladr_idx, (inst_pos, ladr_inst) in enumerate(ladr_instructions):
                        # Parameter index is reversed from LADR position
                        # ladr_idx 0 (last LADR before XCALL) = highest param index
                        param_idx = len(ladr_instructions) - 1 - ladr_idx

                        # Check if this parameter index has a known struct type
                        struct_type = param_map.get(param_idx)
                        if not struct_type:
                            continue

                        # The LADR output is &local_X, get the base variable
                        addr_var = ladr_inst.outputs[0].alias or ladr_inst.outputs[0].name

                        # Remove & prefix if present
                        if addr_var.startswith("&"):
                            base_var = addr_var[1:]
                        else:
                            base_var = addr_var

                        # Mark this variable as having the detected struct type
                        # We need to track BOTH local_1 and &local_1 because:
                        # - local_1 is the actual variable
                        # - &local_1 is used in PNT (pointer arithmetic) instructions
                        if base_var not in self.var_struct_types:
                            self.var_struct_types[base_var] = struct_type
                            self.var_struct_types[f"&{base_var}"] = struct_type
                            # DON'T set semantic name for local variables - use the variable name as-is
                            # (semantic names are only for parameters like param_0 → "info")
                            print(f"DEBUG FieldTracker: {base_var} detected as {struct_type} (from {func_name}, param {param_idx})", file=sys.stderr)

    def _propagate_struct_types(self):
        """
        Propagate struct types through assignments and copies.

        If local_1 = param_0 and param_0 is s_SC_NET_info,
        then local_1 should also be tracked as s_SC_NET_info.

        Handles patterns:
        - ASGN: local = param  (assignment)
        - SSP/LLD: stack operations that copy values
        """
        import sys

        # Iterate until no new types are found (fixed-point iteration)
        changed = True
        iterations = 0
        while changed and iterations < 10:  # Max 10 iterations to prevent infinite loops
            changed = False
            iterations += 1

            for block_id, instructions in self.ssa.instructions.items():
                for inst in instructions:
                    # Pattern 1: ASGN instruction (value1 = value2)
                    if inst.mnemonic == "ASGN" and len(inst.inputs) >= 1 and inst.outputs:
                        source = inst.inputs[0]
                        target = inst.outputs[0]

                        # Get source variable name
                        source_var = source.alias if source.alias else source.name
                        target_var = target.alias if target.alias else target.name

                        # If source has known struct type, propagate to target
                        if source_var in self.var_struct_types:
                            if target_var not in self.var_struct_types:
                                self.var_struct_types[target_var] = self.var_struct_types[source_var]
                                self.semantic_names[target_var] = self.semantic_names.get(source_var, "info")
                                print(f"DEBUG Propagate: {target_var} = {source_var} ({self.var_struct_types[source_var]})", file=sys.stderr)
                                changed = True

                    # Pattern 2: LADR instruction (load address of variable)
                    # LADR creates &param_0 from param_0
                    if inst.mnemonic == "LADR" and inst.outputs:
                        target = inst.outputs[0]
                        target_var = target.alias if target.alias else target.name

                        # Remove & prefix if present
                        if target_var.startswith("&"):
                            base_var = target_var[1:]
                            if base_var in self.var_struct_types:
                                if target_var not in self.var_struct_types:
                                    self.var_struct_types[target_var] = self.var_struct_types[base_var]
                                    self.semantic_names[target_var] = self.semantic_names.get(base_var, "info")
                                    print(f"DEBUG Propagate LADR: {target_var} → {self.var_struct_types[base_var]}", file=sys.stderr)
                                    changed = True

        print(f"DEBUG Propagate: Completed in {iterations} iterations, tracking {len(self.var_struct_types)} struct variables", file=sys.stderr)

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
        import sys
        dcp_count = 0
        pnt_found = 0
        dadr_found = 0

        for block_id, instructions in self.ssa.instructions.items():
            for inst in instructions:
                # Look for DCP instructions (dereference)
                if inst.mnemonic != "DCP":
                    continue

                dcp_count += 1
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
                    pnt_found += 1
                    field_access = self._analyze_pnt_instruction(producer)
                    if field_access and inst.outputs:
                        # Map output of DCP to field access
                        self.field_map[inst.outputs[0].name] = field_access
                        print(f"DEBUG FieldTracker: Found PNT pattern: {inst.outputs[0].name} = {field_access.base_var}.field at offset {field_access.field_offset}", file=sys.stderr)
                    continue

                # Pattern 2: DADR followed by earlier pointer
                # (LADR loads address, DADR adds offset, result used in DCP)
                if producer.mnemonic == "DADR":
                    dadr_found += 1
                    field_access = self._analyze_dadr_chain(producer)
                    if field_access and inst.outputs:
                        self.field_map[inst.outputs[0].name] = field_access
                        print(f"DEBUG FieldTracker: Found DADR pattern: {inst.outputs[0].name} = {field_access.base_var}.field at offset {field_access.field_offset}", file=sys.stderr)
                    continue

        print(f"DEBUG FieldTracker: Scanned {dcp_count} DCP instructions, found {pnt_found} PNT patterns, {dadr_found} DADR patterns", file=sys.stderr)

    def _analyze_pnt_instruction(self, pnt_inst: SSAInstruction) -> Optional[FieldAccess]:
        """
        Analyze PNT instruction to extract field access info.

        PNT takes 1 input (base pointer) and offset in arg1
        Pattern: PNT(base_ptr, immediate_offset)
        Returns FieldAccess if valid struct field access detected.
        """
        import sys

        if not pnt_inst.inputs:
            print(f"DEBUG PNT: Rejected - no inputs", file=sys.stderr)
            return None

        base_value = pnt_inst.inputs[0]

        # Get base variable name (param_0, local_0, etc.)
        base_var = base_value.alias if base_value.alias else base_value.name

        # Check if base is a known struct
        struct_type = self.var_struct_types.get(base_var)
        if not struct_type:
            print(f"DEBUG PNT: Rejected - base_var '{base_var}' not in var_struct_types {list(self.var_struct_types.keys())}", file=sys.stderr)
            return None

        # Get offset from instruction arg1 (PNT uses immediate offset)
        if not pnt_inst.instruction or not pnt_inst.instruction.instruction:
            print(f"DEBUG PNT: Rejected - no instruction data", file=sys.stderr)
            return None

        offset = pnt_inst.instruction.instruction.arg1

        # Lookup field at this offset
        field_name = get_field_at_offset(struct_type, offset)

        print(f"DEBUG PNT: SUCCESS - base={base_var}, struct={struct_type}, offset={offset}, field={field_name}", file=sys.stderr)

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
