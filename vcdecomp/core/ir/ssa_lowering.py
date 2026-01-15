"""
SSA Lowering - Collapse versioned SSA variables to unversioned C variables.

This module transforms the rename_map from variable_renaming.py to collapse
all SSA versions of the same variable into a single unversioned name.

Example:
    Before: {"t100_0": "sideA", "t200_0": "sideB"}  # Two versions
    After:  {"t100_0": "side", "t200_0": "side"}    # One unversioned variable
"""

from __future__ import annotations
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass

from .variable_renaming import VariableVersion
from .ssa import SSAFunction, SSAValue
from .cfg import CFG, NaturalLoop


@dataclass
class BaseVariable:
    """
    Represents a base variable before SSA versioning.

    Attributes:
        base_name: Original stack name (e.g., "local_2")
        versions: All SSA versions of this variable
        lowered_name: Final unversioned name for C output
        semantic_type: Most common semantic type among versions
        is_loop_counter: Special handling for loop counters
    """
    base_name: str
    versions: List[VariableVersion]
    lowered_name: str
    semantic_type: str
    is_loop_counter: bool


@dataclass
class LoweringResult:
    """
    Result of SSA lowering process.

    Attributes:
        lowered_rename_map: Updated rename_map with collapsed names
        variable_declarations: List of (type, name) for function locals
        version_tracking: Maps SSA names to (base_name, version_num)
        phi_resolutions: Maps PHI node names to lowered variable names
    """
    lowered_rename_map: Dict[str, str]
    variable_declarations: List[Tuple[str, str]]
    version_tracking: Dict[str, Tuple[str, int]]
    phi_resolutions: Dict[str, str]


class SSALowerer:
    """
    Lowers SSA form to unversioned variables suitable for C output.

    The lowering process:
    1. Groups all SSA versions by base variable name
    2. Chooses a single lowered name for each base variable
    3. Updates rename_map to use lowered names
    4. Handles special cases: loop counters, PHI nodes, address-of
    """

    def __init__(
        self,
        rename_map: Dict[str, str],
        variable_versions: Dict[str, List[VariableVersion]],
        cfg: CFG,
        ssa_func: SSAFunction,
        loops: List[NaturalLoop]
    ):
        """
        Initialize SSA lowerer.

        Args:
            rename_map: Current rename_map from variable_renaming
            variable_versions: Version info for each variable
            cfg: Control flow graph
            ssa_func: SSA function representation
            loops: Detected natural loops
        """
        self.rename_map = rename_map
        self.variable_versions = variable_versions
        self.cfg = cfg
        self.ssa_func = ssa_func
        self.loops = loops

        # Build reverse mapping: versioned_name → SSA value names
        self.versioned_to_ssa: Dict[str, Set[str]] = {}
        for ssa_name, versioned_name in rename_map.items():
            if versioned_name not in self.versioned_to_ssa:
                self.versioned_to_ssa[versioned_name] = set()
            self.versioned_to_ssa[versioned_name].add(ssa_name)

    def lower(self) -> LoweringResult:
        """
        Main entry point for SSA lowering.

        Returns:
            LoweringResult with lowered rename_map and metadata
        """
        # Step 1: Build base variables
        base_vars = self._build_base_variables()

        # Step 2: Choose lowered names
        self._choose_lowered_names(base_vars)

        # Step 3: Build lowered rename_map
        lowered_rename_map = self._build_lowered_rename_map(base_vars)

        # Step 4: Generate variable declarations
        var_decls = self._generate_declarations(base_vars)

        # Step 5: Build tracking info
        version_tracking = self._build_version_tracking(base_vars)
        phi_resolutions = self._resolve_phi_nodes(base_vars, lowered_rename_map)

        return LoweringResult(
            lowered_rename_map=lowered_rename_map,
            variable_declarations=var_decls,
            version_tracking=version_tracking,
            phi_resolutions=phi_resolutions
        )

    def _build_base_variables(self) -> List[BaseVariable]:
        """
        Group all versions by base variable name.

        Returns:
            List of BaseVariable objects, one per base variable
        """
        base_vars = []

        for base_name, versions in self.variable_versions.items():
            if not versions:
                continue

            # Determine predominant semantic type
            type_counts = {}
            for v in versions:
                sem_type = v.semantic_type or "general"
                type_counts[sem_type] = type_counts.get(sem_type, 0) + 1

            predominant_type = max(type_counts.items(), key=lambda x: x[1])[0]
            is_loop_counter = predominant_type == "loop_counter"

            # For now, lowered_name will be set in next step
            base_var = BaseVariable(
                base_name=base_name,
                versions=versions,
                lowered_name="",  # To be filled
                semantic_type=predominant_type,
                is_loop_counter=is_loop_counter
            )
            base_vars.append(base_var)

        return base_vars

    def _choose_lowered_names(self, base_vars: List[BaseVariable]) -> None:
        """
        Choose a single lowered name for each base variable.

        Strategy:
        - Loop counters: Keep shortest name (i, j, k preferred over idx1)
        - Side values: Strip version suffix (sideA, sideB → side)
        - Temps: Strip version suffix (tmp1, tmp2 → tmp)
        - General: Use base_name if only 1 version, else strip suffix

        Handles collisions by adding numeric suffix.
        """
        used_names: Set[str] = set()

        for base_var in base_vars:
            candidate_names = set()

            # Collect all assigned names from versions
            for version in base_var.versions:
                name = version.assigned_name
                if not name:
                    continue

                # Add original name
                candidate_names.add(name)

                # Add de-versioned variants
                # Pattern 1: sideA, sideB → side
                if len(name) > 1 and name[-1].isupper():
                    candidate_names.add(name[:-1])

                # Pattern 2: side2, side3 → side
                if len(name) > 1 and name[-1].isdigit():
                    # Strip all trailing digits
                    base = name.rstrip('0123456789')
                    if base:
                        candidate_names.add(base)

                # Pattern 3: local_8_v1 → local_8
                if '_v' in name:
                    parts = name.split('_v')
                    if len(parts) == 2 and parts[1].isdigit():
                        candidate_names.add(parts[0])

            # Special handling for loop counters
            if base_var.is_loop_counter:
                # Prefer i, j, k, then idx, then longer names
                priority = ['i', 'j', 'k', 'idx', 'idx2', 'idx3']
                for p in priority:
                    if p in candidate_names and p not in used_names:
                        base_var.lowered_name = p
                        used_names.add(p)
                        break

            # Choose best candidate
            if not base_var.lowered_name:
                # Sort by: shortest first, then alphabetically
                sorted_candidates = sorted(
                    candidate_names,
                    key=lambda n: (len(n), n)
                )

                for candidate in sorted_candidates:
                    if candidate not in used_names:
                        base_var.lowered_name = candidate
                        used_names.add(candidate)
                        break

            # Fallback: use base_name with collision resolution
            if not base_var.lowered_name:
                candidate = base_var.base_name
                counter = 1
                while candidate in used_names:
                    candidate = f"{base_var.base_name}_{counter}"
                    counter += 1
                base_var.lowered_name = candidate
                used_names.add(candidate)

    def _build_lowered_rename_map(
        self,
        base_vars: List[BaseVariable]
    ) -> Dict[str, str]:
        """
        Build new rename_map with lowered names.

        Args:
            base_vars: List of base variables with chosen lowered_name

        Returns:
            New rename_map: SSA value name → lowered name
        """
        # Build mapping: versioned_name → base_var
        versioned_to_base: Dict[str, BaseVariable] = {}
        for base_var in base_vars:
            for version in base_var.versions:
                versioned_to_base[version.assigned_name] = base_var

        # Transform rename_map
        lowered_map = {}
        for ssa_name, versioned_name in self.rename_map.items():
            # Handle address-of prefix
            has_address_prefix = versioned_name.startswith("&")
            clean_name = versioned_name[1:] if has_address_prefix else versioned_name

            # Look up base variable
            if clean_name in versioned_to_base:
                base_var = versioned_to_base[clean_name]
                lowered = base_var.lowered_name

                # Restore address prefix if needed
                if has_address_prefix:
                    lowered = "&" + lowered

                lowered_map[ssa_name] = lowered
            else:
                # Not a versioned variable (might be global, param, etc.)
                lowered_map[ssa_name] = versioned_name

        return lowered_map

    def _generate_declarations(
        self,
        base_vars: List[BaseVariable]
    ) -> List[Tuple[str, str]]:
        """
        Generate variable declarations for function scope.

        Args:
            base_vars: Base variables with lowered names

        Returns:
            List of (type, name) tuples for declaration
        """
        # FIX #5: Build struct type inference map (versioned_name -> struct_type)
        versioned_struct_types = self._infer_struct_types_from_calls()

        declarations = []

        for base_var in base_vars:
            # Infer type from semantic type and usage
            var_type = "int"  # Default

            # FIX #5: Check if any version of this variable has an inferred struct type
            # First check base_name (for local_X variables that weren't renamed)
            if base_var.base_name in versioned_struct_types:
                var_type = versioned_struct_types[base_var.base_name]
            else:
                # Then check versioned names
                for version in base_var.versions:
                    if version.assigned_name in versioned_struct_types:
                        var_type = versioned_struct_types[version.assigned_name]
                        break

            # Check if any version has float type
            if var_type == "int" and any("float" in base_var.lowered_name.lower() for version in base_var.versions):
                var_type = "float"

            declarations.append((var_type, base_var.lowered_name))

        return declarations

    def _build_version_tracking(
        self,
        base_vars: List[BaseVariable]
    ) -> Dict[str, Tuple[str, int]]:
        """
        Build tracking map: SSA value name → (base_name, version_num).

        Useful for debugging and validation.
        """
        tracking = {}

        for base_var in base_vars:
            for version in base_var.versions:
                # Find all SSA names using this version
                versioned_name = version.assigned_name
                if versioned_name in self.versioned_to_ssa:
                    for ssa_name in self.versioned_to_ssa[versioned_name]:
                        tracking[ssa_name] = (base_var.base_name, version.version)

        return tracking

    def _resolve_phi_nodes(
        self,
        base_vars: List[BaseVariable],
        lowered_rename_map: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Resolve PHI nodes to lowered variable names.

        Args:
            base_vars: Base variables
            lowered_rename_map: Already built lowered map

        Returns:
            Mapping: PHI node SSA name → lowered variable name
        """
        phi_resolutions = {}

        # Iterate through rename_map looking for PHI nodes
        for ssa_name, lowered_name in lowered_rename_map.items():
            if "phi_" in ssa_name:
                # This is a PHI node - record its resolution
                phi_resolutions[ssa_name] = lowered_name

        return phi_resolutions

    def _infer_struct_types_from_calls(self) -> Dict[str, str]:
        """
        Infer struct types for variables based on function call patterns.

        Scans all XCALL instructions and maps variables to struct types based on
        function parameter signatures.

        Returns:
            Mapping: lowered variable name → struct type
        """
        from ..structures import infer_struct_from_function

        inferred_types: Dict[str, str] = {}

        # PRIORITY 2: Map common struct sizes from SC_ZeroMem
        STRUCT_SIZE_MAP = {
            128: "s_SC_P_AI_props",
            156: "s_SC_P_info",
            36: "c_Vector3",
            # Add more mappings as needed
        }

        # Iterate through all blocks in the function
        for block in self.cfg.blocks.values():
            ssa_instrs = self.ssa_func.instructions.get(block.block_id, [])

            for inst in ssa_instrs:
                # Look for XCALL instructions (external function calls)
                if inst.mnemonic != "XCALL" or not inst.inputs:
                    continue

                # Get function name from XFN table
                call_name = None
                if inst.instruction and inst.instruction.instruction:
                    xfn_idx = inst.instruction.instruction.arg1
                    xfn_entry = self.ssa_func.scr.get_xfn(xfn_idx) if self.ssa_func.scr else None
                    if xfn_entry:
                        full_name = xfn_entry.name
                        paren_idx = full_name.find("(")
                        call_name = full_name[:paren_idx] if paren_idx > 0 else full_name

                if not call_name:
                    continue

                # PRIORITY 2: Special handling for SC_ZeroMem to infer struct type from size
                if call_name == "SC_ZeroMem" and len(inst.inputs) >= 2:
                    # SC_ZeroMem(&struct, size) - arg0 is struct pointer, arg1 is size
                    var_name = inst.inputs[0].alias or inst.inputs[0].name
                    size_value = inst.inputs[1].alias or inst.inputs[1].name

                    if var_name and var_name.startswith("&"):
                        var_name = var_name[1:]

                    # Try to extract size as integer constant
                    try:
                        size = int(size_value)
                        if size in STRUCT_SIZE_MAP:
                            inferred_types[var_name] = STRUCT_SIZE_MAP[size]
                    except (ValueError, TypeError):
                        pass  # Size is not a constant, skip

                # Check each argument to see if it's a struct pointer parameter
                for arg_idx, arg_value in enumerate(inst.inputs):
                    # Infer struct type from function signature
                    struct_type = infer_struct_from_function(call_name, arg_idx)
                    if not struct_type:
                        continue

                    # Extract variable name from alias (which is already renamed)
                    var_name = arg_value.alias or arg_value.name
                    if not var_name:
                        continue

                    # Strip & prefix if present
                    if var_name.startswith("&"):
                        var_name = var_name[1:]

                    # Store the struct type using the versioned variable name
                    # This will be the name AFTER variable renaming but BEFORE SSA lowering
                    # e.g., "SRVset", "hudinfo", "plinfo"
                    inferred_types[var_name] = struct_type

        return inferred_types
