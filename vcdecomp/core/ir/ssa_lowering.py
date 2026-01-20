"""
SSA Lowering - Collapse versioned SSA variables to unversioned C variables.

This module transforms the rename_map from variable_renaming.py to collapse
all SSA versions of the same variable into a single unversioned name.

Example:
    Before: {"t100_0": "sideA", "t200_0": "sideB"}  # Two versions
    After:  {"t100_0": "side", "t200_0": "side"}    # One unversioned variable

Phase 4 enhancement: Uses liveness analysis to ensure only non-interfering
variables are merged. Variables that are live simultaneously cannot share
the same C variable.
"""

from __future__ import annotations
from typing import Dict, List, Set, Tuple, Optional, TYPE_CHECKING
from dataclasses import dataclass

from .variable_renaming import VariableVersion
from .ssa import SSAFunction, SSAValue
from .cfg import CFG, NaturalLoop

if TYPE_CHECKING:
    from .liveness import InterferenceGraph


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

    Phase 4 enhancement: When an InterferenceGraph is provided, the lowerer
    checks for interference before merging variables. Only non-interfering
    versions are collapsed into a single C variable.
    """

    def __init__(
        self,
        rename_map: Dict[str, str],
        variable_versions: Dict[str, List[VariableVersion]],
        cfg: CFG,
        ssa_func: SSAFunction,
        loops: List[NaturalLoop],
        interference_graph: Optional["InterferenceGraph"] = None
    ):
        """
        Initialize SSA lowerer.

        Args:
            rename_map: Current rename_map from variable_renaming
            variable_versions: Version info for each variable
            cfg: Control flow graph
            ssa_func: SSA function representation
            loops: Detected natural loops
            interference_graph: Optional interference graph for smart merging
        """
        self.rename_map = rename_map
        self.variable_versions = variable_versions
        self.cfg = cfg
        self.ssa_func = ssa_func
        self.loops = loops
        self.interference = interference_graph

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
        Choose lowered names for each base variable.

        Phase 4 enhancement: When interference graph is available, only merge
        versions that don't interfere. Interfering versions get separate names.

        Strategy:
        - Loop counters: Keep shortest name (i, j, k preferred over idx1)
        - Side values: Strip version suffix (sideA, sideB → side)
        - Temps: Strip version suffix (tmp1, tmp2 → tmp)
        - General: Use base_name if only 1 version, else strip suffix

        With interference analysis:
        - Before merging, check if versions interfere
        - If they interfere, keep separate names (sideA, sideB)
        - If they don't interfere, merge to single name (side)

        Handles collisions by adding numeric suffix.
        """
        used_names: Set[str] = set()

        # Maps to track which versions get which lowered name
        # Key: (base_name, version_num), Value: lowered_name
        self._version_to_lowered: Dict[Tuple[str, int], str] = {}

        for base_var in base_vars:
            # Check if we need interference-aware merging
            if self.interference and len(base_var.versions) > 1:
                self._choose_names_with_interference(base_var, used_names)
            else:
                # Original logic: merge all versions to single name
                self._choose_single_name(base_var, used_names)

    def _get_ssa_names_for_version(self, base_name: str, version_num: int) -> Set[str]:
        """Get all SSA value names that belong to a specific version."""
        ssa_names = set()
        for ssa_name, (vbase, vnum, _) in getattr(self, '_value_to_version_map', {}).items():
            if vbase == base_name and vnum == version_num:
                ssa_names.add(ssa_name)
        return ssa_names

    def _choose_names_with_interference(self, base_var: BaseVariable, used_names: Set[str]) -> None:
        """
        Choose names for a base variable using interference analysis.

        Groups versions by non-interference, then assigns names to each group.
        """
        # Collect all SSA names for each version
        version_ssa_names: Dict[int, Set[str]] = {}
        for version in base_var.versions:
            ssa_names = set()
            versioned_name = version.assigned_name
            if versioned_name and versioned_name in self.versioned_to_ssa:
                ssa_names = self.versioned_to_ssa[versioned_name].copy()
            version_ssa_names[version.version] = ssa_names

        # Check interference between versions
        # Two versions interfere if any of their SSA names interfere
        interfering_pairs: Set[Tuple[int, int]] = set()
        version_nums = [v.version for v in base_var.versions]

        for i, v1 in enumerate(version_nums):
            for v2 in version_nums[i+1:]:
                # Check if any SSA name from v1 interferes with any from v2
                names1 = version_ssa_names.get(v1, set())
                names2 = version_ssa_names.get(v2, set())
                for n1 in names1:
                    for n2 in names2:
                        if self.interference.interferes(n1, n2):
                            interfering_pairs.add((min(v1, v2), max(v1, v2)))
                            break
                    else:
                        continue
                    break

        # Group non-interfering versions together
        # Use greedy coloring
        groups: List[List[VariableVersion]] = []
        assigned: Set[int] = set()

        for version in base_var.versions:
            if version.version in assigned:
                continue

            # Find a group where this version doesn't interfere
            placed = False
            for group in groups:
                can_place = True
                for member in group:
                    pair = (min(version.version, member.version), max(version.version, member.version))
                    if pair in interfering_pairs:
                        can_place = False
                        break
                if can_place:
                    group.append(version)
                    assigned.add(version.version)
                    placed = True
                    break

            if not placed:
                groups.append([version])
                assigned.add(version.version)

        # Assign names to each group
        if len(groups) == 1:
            # All versions can be merged - use original merging logic
            self._choose_single_name(base_var, used_names)
        else:
            # Multiple groups - assign different names to each
            for group_idx, group in enumerate(groups):
                group_name = self._generate_group_name(base_var, group, group_idx, used_names)
                used_names.add(group_name)

                # Record which versions map to this name
                for version in group:
                    self._version_to_lowered[(base_var.base_name, version.version)] = group_name

            # Set base_var.lowered_name to first group's name (for compatibility)
            base_var.lowered_name = self._version_to_lowered.get(
                (base_var.base_name, base_var.versions[0].version),
                base_var.base_name
            )

    def _generate_group_name(self, base_var: BaseVariable, group: List[VariableVersion],
                             group_idx: int, used_names: Set[str]) -> str:
        """Generate a name for a group of non-interfering versions."""
        # Use the assigned name from the first version in the group
        if group and group[0].assigned_name:
            candidate = group[0].assigned_name
            if candidate not in used_names:
                return candidate

        # Generate a name based on semantic type
        if base_var.is_loop_counter:
            priority = ['i', 'j', 'k', 'idx', 'idx2', 'idx3']
            for p in priority:
                if p not in used_names:
                    return p
            return f"idx{group_idx + 4}"

        # For side values, use sideA, sideB, etc.
        if base_var.semantic_type == "side_value":
            side_chars = 'ABCDEFGHIJ'
            if group_idx < len(side_chars):
                candidate = f"side{side_chars[group_idx]}"
            else:
                candidate = f"side{group_idx}"
            if candidate not in used_names:
                return candidate

        # Default: use base_name with suffix
        candidate = base_var.base_name if group_idx == 0 else f"{base_var.base_name}_{group_idx}"
        counter = group_idx
        while candidate in used_names:
            counter += 1
            candidate = f"{base_var.base_name}_{counter}"
        return candidate

    def _choose_single_name(self, base_var: BaseVariable, used_names: Set[str]) -> None:
        """
        Original logic: choose a single lowered name for all versions.

        Used when there's no interference or when interference analysis is disabled.
        """
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

        # Record all versions mapping to this name
        for version in base_var.versions:
            self._version_to_lowered[(base_var.base_name, version.version)] = base_var.lowered_name

    def _build_lowered_rename_map(
        self,
        base_vars: List[BaseVariable]
    ) -> Dict[str, str]:
        """
        Build new rename_map with lowered names.

        Phase 4 enhancement: Uses _version_to_lowered for interference-aware
        naming when available.

        Args:
            base_vars: List of base variables with chosen lowered_name

        Returns:
            New rename_map: SSA value name → lowered name
        """
        # Build mapping: versioned_name → (base_var, version_num)
        versioned_to_info: Dict[str, Tuple[BaseVariable, int]] = {}
        for base_var in base_vars:
            for version in base_var.versions:
                versioned_to_info[version.assigned_name] = (base_var, version.version)

        # Transform rename_map
        lowered_map = {}
        for ssa_name, versioned_name in self.rename_map.items():
            # Handle address-of prefix
            has_address_prefix = versioned_name.startswith("&")
            clean_name = versioned_name[1:] if has_address_prefix else versioned_name

            # Look up base variable
            if clean_name in versioned_to_info:
                base_var, version_num = versioned_to_info[clean_name]

                # Phase 4: Check if we have interference-aware naming
                if hasattr(self, '_version_to_lowered') and (base_var.base_name, version_num) in self._version_to_lowered:
                    lowered = self._version_to_lowered[(base_var.base_name, version_num)]
                else:
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

        Phase 4 enhancement: When interference analysis creates multiple groups
        from a single base variable, we need to declare each group's name.

        Args:
            base_vars: Base variables with lowered names

        Returns:
            List of (type, name) tuples for declaration
        """
        # FIX #5: Build struct type inference map (versioned_name -> struct_type)
        versioned_struct_types = self._infer_struct_types_from_calls()

        declarations = []
        declared_names: Set[str] = set()  # Track to avoid duplicates

        for base_var in base_vars:
            # CRITICAL FIX (07-08): Opcode-first priority to eliminate Pattern 2
            # Check if any version has opcode-derived type (IADD→int, FADD→float)
            # These concrete types ALWAYS override struct inference
            opcode_type = None
            for version in base_var.versions:
                # Check if this SSA value has a non-UNKNOWN type
                if hasattr(version, 'ssa_value') and version.ssa_value:
                    from ..disasm import opcodes
                    if version.ssa_value.value_type != opcodes.ResultType.UNKNOWN:
                        # Import helper from variables.py
                        from .structure.analysis.variables import result_type_to_c_type
                        opcode_type = result_type_to_c_type(version.ssa_value.value_type)
                        if opcode_type:
                            break

            # Infer type from semantic type and usage
            var_type = "int"  # Default

            # Priority 1: Opcode-derived types (ABSOLUTE)
            if opcode_type and opcode_type in {"int", "float", "dword", "char", "short", "double"}:
                var_type = opcode_type
            # Priority 2: Struct types from function signatures (DISABLED - too many false positives)
            # FIX #5: Check if any version of this variable has an inferred struct type
            # First check base_name (for local_X variables that weren't renamed)
            # elif base_var.base_name in versioned_struct_types:
            #     var_type = versioned_struct_types[base_var.base_name]
            # else:
            #     # Then check versioned names
            #     for version in base_var.versions:
            #         if version.assigned_name in versioned_struct_types:
            #             var_type = versioned_struct_types[version.assigned_name]
            #             break
            # Priority 3: Float heuristic (check variable name)
            elif any("float" in base_var.lowered_name.lower() for version in base_var.versions):
                var_type = "float"

            # Phase 4: Handle multiple declarations when interference analysis
            # created multiple groups
            if hasattr(self, '_version_to_lowered'):
                # Collect all unique lowered names for this base variable
                lowered_names = set()
                for version in base_var.versions:
                    key = (base_var.base_name, version.version)
                    if key in self._version_to_lowered:
                        lowered_names.add(self._version_to_lowered[key])
                    else:
                        lowered_names.add(base_var.lowered_name)

                for name in lowered_names:
                    if name not in declared_names:
                        declarations.append((var_type, name))
                        declared_names.add(name)
            else:
                # Original behavior: single declaration per base variable
                if base_var.lowered_name not in declared_names:
                    declarations.append((var_type, base_var.lowered_name))
                    declared_names.add(base_var.lowered_name)

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
