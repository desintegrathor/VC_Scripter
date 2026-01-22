"""
Variable Renaming - P0.4 Fix

Detekuje kdy jedna local_X proměnná je použita pro více sémantických účelů
a rozdělí ji na více pojmenovaných proměnných (sideA, sideB, i, j, tmp, ...).
"""

from __future__ import annotations
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import re

from .ssa import SSAFunction, SSAValue


@dataclass
class VariableVersion:
    """Představuje jednu verzi proměnné (např. local_2 version 0, 1, 2)."""
    base_name: str  # "local_2"
    version: int    # 0, 1, 2, ...
    first_def: int  # Address prvního přiřazení
    last_use: int   # Address posledního použití
    semantic_type: str = "general"  # loop_counter, side_value, temp, general, struct_value
    assigned_name: str = ""  # Finální pojmenování (i, sideA, tmp1, ...)
    struct_type: Optional[str] = None  # FIX #5 Phase 2: Detected struct type (e.g., "s_SC_MP_SRV_settings")


def extract_struct_name_from_type(struct_type: str) -> str:
    """
    Generate a short variable name from a struct type.

    FIX #5 Phase 2: Generate meaningful names from struct types.

    Examples:
        s_SC_MP_SRV_settings → SRVset
        s_SC_MP_EnumPlayers → enum_pl
        s_SC_HUD_MP_icon → icon
        s_SC_P_getinfo → plinfo
        s_SC_MP_hud → hudinfo

    Args:
        struct_type: Full struct type name

    Returns:
        Short variable name
    """
    if not struct_type:
        return ""

    # Remove s_ prefix if present
    if struct_type.startswith("s_"):
        struct_type = struct_type[2:]

    # Remove SC_ prefix if present
    if struct_type.startswith("SC_"):
        struct_type = struct_type[3:]

    # Pattern 1: MP_SRV_settings → SRVset
    if "_SRV_settings" in struct_type:
        return "SRVset"

    # Pattern 2: MP_EnumPlayers → enum_pl
    if "EnumPlayers" in struct_type:
        return "enum_pl"

    # Pattern 3: HUD_MP_icon → icon
    if "icon" in struct_type.lower():
        return "icon"

    # Pattern 4: P_getinfo → plinfo (player info)
    if "P_getinfo" in struct_type:
        return "plinfo"

    # Pattern 5: MP_hud → hudinfo
    if struct_type == "MP_hud":
        return "hudinfo"

    # Pattern 6: MP_Recover → precov (pointer to recovery)
    if "Recover" in struct_type:
        return "precov"

    # Fallback: Use last component and lowercase
    # Example: MP_Some_Type → type
    parts = struct_type.split('_')
    if len(parts) > 0:
        last_part = parts[-1].lower()
        if len(last_part) > 2:
            return last_part

    # Final fallback: use whole thing lowercase
    return struct_type.lower()[:8]  # Limit to 8 chars


class VariableRenamer:
    """
    Analyzuje SSA funkci a detekuje kdy local_X proměnná potřebuje splitting.

    Approach:
    1. Analyzuj každé přiřazení do local_X
    2. Zjisti zda je to "nová" definice (předchozí use byl dávno) → nová version
    3. Každé verzi přiřaď sémantický typ
    4. Vygeneruj nové jméno podle typu
    """

    def __init__(self, ssa_func: SSAFunction, func_block_ids: Set[int], type_engine=None, heritage_metadata: Optional[Dict] = None):
        self.ssa_func = ssa_func
        self.func_block_ids = func_block_ids
        self.type_engine = type_engine  # Optional TypeInferenceEngine for PHI resolution
        self.heritage_metadata = heritage_metadata  # Optional heritage SSA metadata for improved naming

        # Trackování verzí
        self.variable_versions: Dict[str, List[VariableVersion]] = defaultdict(list)

        # Mapování SSA value → version + original alias
        # value.name → (base_name, version, original_alias)
        self.value_to_version: Dict[str, Tuple[str, int, str]] = {}

        # Semantic name counters
        self.name_counters = {
            'loop_counter': 0,  # i, j, k
            'side_value': 0,    # sideA, sideB
            'temp': 0,          # tmp, tmp1, tmp2
        }

        # Heritage variable info (extracted from heritage_metadata)
        self._heritage_vars: Dict[str, Dict] = {}
        if heritage_metadata and "variables" in heritage_metadata:
            self._heritage_vars = heritage_metadata["variables"]

        # Pre-built indices for O(1) lookups (built in _build_indices)
        self._mnemonic_index: Dict[str, List] = {}
        self._value_uses: Dict[str, List[Tuple]] = {}
        self._var_instructions: Dict[str, List] = {}
        self._addr_index: Dict[int, Any] = {}

    def _build_indices(self):
        """
        Build O(1) lookup indices for all analysis methods.

        This replaces O(n²) patterns where we iterate over all blocks for each variable.
        Instead, we build indices ONCE in O(n) time, then use O(1) lookups during analysis.

        Indices built:
        - _mnemonic_index: mnemonic → list of SSAInstructions (for finding all PNT, XCALL, INC, etc.)
        - _value_uses: SSA value name → list of (instruction, input_index) tuples
        - _var_instructions: variable name → list of instructions that use/define it
        - _addr_index: address → SSAInstruction (for O(1) lookup by address)
        """
        self._mnemonic_index = defaultdict(list)
        self._value_uses = defaultdict(list)
        self._var_instructions = defaultdict(list)
        self._addr_index = {}

        for block_id in self.func_block_ids:
            for inst in self.ssa_func.instructions.get(block_id, []):
                # Index by mnemonic
                self._mnemonic_index[inst.mnemonic].append(inst)

                # Index by address
                self._addr_index[inst.address] = inst

                # Index by input value name and variable name
                for i, inp in enumerate(inst.inputs):
                    if inp.name:
                        self._value_uses[inp.name].append((inst, i))
                    var_name = self._extract_local_name(inp)
                    if var_name:
                        self._var_instructions[var_name].append(inst)

                # Also index outputs for completeness
                for output in inst.outputs:
                    var_name = self._extract_local_name(output)
                    if var_name:
                        self._var_instructions[var_name].append(inst)

    def analyze_and_rename(self) -> Dict[str, str]:
        """
        Hlavní entry point.

        Returns:
            Dict mapující původní alias (local_2) → nový název (sideA, i, tmp)
        """
        # Krok 0: Build indices ONCE for O(1) lookups in analysis methods
        # This replaces O(n²) patterns with O(n) build + O(1) lookups
        self._build_indices()

        # Krok 1: Detekuj verze proměnných
        self._detect_variable_versions()

        # Krok 1.5: FIX P0.4.3: Track PHI node outputs
        self._track_phi_nodes()

        # Krok 2: Přiřaď sémantické typy verzím
        self._infer_semantic_types()

        # Krok 3: Vygeneruj finální jména
        self._assign_final_names()

        # Krok 4: Vytvoř mapování pro rendering
        return self._build_rename_map()

    def _detect_variable_versions(self):
        """
        Detekuje kdy local_X potřebuje splitting.

        Heuristika: Pokud mezi dvěma assignments do local_X je use local_X,
        pak druhý assignment vytváří novou verzi.
        """
        # Track poslední assignment pro každou proměnnou
        last_assignment: Dict[str, int] = {}  # var_name → address
        last_use: Dict[str, int] = {}  # var_name → address
        current_version: Dict[str, int] = defaultdict(int)  # var_name → version number

        # Procházej bloky v topologickém pořadí
        for block_id in sorted(self.func_block_ids):
            ssa_instrs = self.ssa_func.instructions.get(block_id, [])

            # Build address-to-instruction index for O(1) lookup of next instruction
            addr_to_inst = {inst.address: inst for inst in ssa_instrs}

            for inst in ssa_instrs:
                addr = inst.address

                # Check inputs (uses)
                for inp in inst.inputs:
                    var_name = self._extract_local_name(inp)
                    if var_name:
                        # FIX P0.4.3: Address values (&local_X) are NOT uses of the variable!
                        # Using address for write (ASGN) is not a USE of the value
                        if inp.alias and inp.alias.startswith("&"):
                            # This is an address, not a value - skip last_use update
                            continue
                        last_use[var_name] = addr

                # Check outputs (assignments)
                # CRITICAL FIX: Distinguish between LOAD and STORE operations
                # LCP/LLD/LADR are LOAD ops - they read from variables (USES), don't write (ASSIGNMENTS)
                # LADR loads ADDRESS of variable (doesn't modify the variable itself)
                # But we still need to track them in value_to_version for rename_map!
                is_load_op = inst.mnemonic in {'LCP', 'LLD', 'LADR', 'GCP', 'GLD', 'GADR'}

                for output in inst.outputs:
                    var_name = self._extract_local_name(output)
                    if not var_name:
                        continue

                    if is_load_op:
                        # LOAD operation - just map to current version, don't create new version!
                        version = current_version.get(var_name, 0)
                        # Track mapping for rename_map (include original alias)
                        original_alias = output.alias or ""
                        self.value_to_version[output.name] = (var_name, version, original_alias)

                        # FIX P0.4.3: LADR followed by ASGN is NOT a USE, it's getting address for WRITE!
                        # Only update last_use if this is truly a READ operation
                        # Check next instruction to see if it's ASGN
                        is_address_for_write = False

                        if inst.mnemonic == 'LADR':
                            # Find next instruction using index for O(1) lookup
                            next_inst = addr_to_inst.get(addr + 1)

                            if next_inst:
                                mnem = str(next_inst.mnemonic).strip()
                                is_asgn_check = (mnem == 'ASGN')

                                # Check if next is ASGN
                                if is_asgn_check:
                                    # This LADR is for write, not read
                                    is_address_for_write = True

                        if not is_address_for_write:
                            # Update last_use for this version (true READ)
                            if var_name in self.variable_versions and version < len(self.variable_versions[var_name]):
                                self.variable_versions[var_name][version].last_use = addr

                        continue  # Skip version creation

                    # STORE operation - this is a real assignment
                    version = current_version[var_name]

                    # Check zda potřebujeme novou verzi
                    if var_name in last_assignment:
                        # Už byla přiřazena dříve
                        # Zjisti zda mezi last_assignment a teď byl nějaký use
                        if var_name in last_use and last_use[var_name] > last_assignment[var_name]:
                            # Byla použita po posledním přiřazení → vytvoř novou verzi
                            version += 1
                            current_version[var_name] = version

                    # Záznam verze
                    if version >= len(self.variable_versions[var_name]):
                        # Vytvoř novou verzi
                        self.variable_versions[var_name].append(
                            VariableVersion(
                                base_name=var_name,
                                version=version,
                                first_def=addr,
                                last_use=addr  # Bude updated později
                            )
                        )
                    else:
                        # Update existující verze
                        self.variable_versions[var_name][version].last_use = addr

                    # Trackuj mapování (include original alias)
                    original_alias = output.alias or ""
                    self.value_to_version[output.name] = (var_name, version, original_alias)

                    # Update last_assignment
                    last_assignment[var_name] = addr

                # FIX 3: Track ASGN instructions (memory stores via address)
                # Pattern: value, LADR [sp+X] → ASGN
                # Stack before ASGN: [..., value, &local_X]
                # ASGN pops: first &local_X (address), then value
                # Due to insert(0) in stack_lifter, inputs are REVERSED:
                #   inputs[0] = value (last popped)
                #   inputs[1] = address (first popped)
                if inst.mnemonic == 'ASGN' and len(inst.inputs) >= 2:
                    # Second input is the address (from LADR/DADR)
                    addr_value = inst.inputs[1]
                    value_input = inst.inputs[0]

                    var_name = self._extract_local_name(addr_value)

                    if var_name:
                        # This is an assignment to local_X
                        version = current_version[var_name]

                        # Check if we need new version
                        if var_name in last_assignment:
                            if var_name in last_use and last_use[var_name] > last_assignment[var_name]:
                                version += 1
                                current_version[var_name] = version

                        # Record version
                        if version >= len(self.variable_versions[var_name]):
                            # FIX P0.4.3: ASGN is ASSIGNMENT not USE - don't set last_use to current addr
                            # last_use will be set by actual LOAD operations (LCP/LLD)
                            self.variable_versions[var_name].append(
                                VariableVersion(
                                    base_name=var_name,
                                    version=version,
                                    first_def=addr,
                                    last_use=addr  # Initial value, will be updated by LOADs
                                )
                            )
                        else:
                            # FIX P0.4.3: Don't update last_use for ASGN - it's not a USE!
                            # last_use is only updated by LOAD operations
                            pass

                        # Map the ADDRESS value to this version too
                        # This allows rendering "*&local_10" → "local_10" with renaming
                        original_alias = addr_value.alias or ""
                        self.value_to_version[addr_value.name] = (var_name, version, original_alias)

                        # Map XCALL/CALL return temporaries to the assigned local version.
                        # This keeps call results (t*_ret) aligned with the local variable
                        # in conditions and subsequent uses (e.g., pl = SC_P_GetBySideGroupMember(...)).
                        if value_input and value_input.name:
                            if value_input.producer_inst and value_input.producer_inst.mnemonic in {"XCALL", "CALL"}:
                                original_value_alias = value_input.alias or ""
                                self.value_to_version[value_input.name] = (var_name, version, original_value_alias)

                        # Update last_assignment
                        last_assignment[var_name] = addr

    def _extract_local_name(self, value: SSAValue) -> Optional[str]:
        """Extrahuj jméno local proměnné z SSAValue."""
        if not value:
            return None

        var_name = value.alias or value.name
        if not var_name:
            return None

        # Strip & prefix
        if var_name.startswith("&"):
            var_name = var_name[1:]

        # PRIORITY 2 FIX: Expand to handle SSA temporaries and data references
        # Accept: local_X, t*_*, data_*, param_* patterns
        if var_name.startswith("local_"):
            return var_name
        elif var_name.startswith("t") and "_" in var_name:
            # Handle tXXX_X pattern (SSA temporaries)
            parts = var_name.split("_")
            if len(parts) >= 2 and parts[0][1:].isdigit():
                return var_name
        elif var_name.startswith("data_"):
            # Handle data segment references
            return var_name
        elif var_name.startswith("param_"):
            # Handle parameter references (though these are usually handled differently)
            return var_name

        return None

    def _track_phi_nodes(self):
        """
        FIX P0.4.3: Track PHI node outputs in value_to_version map.

        Problem: PHI nodes create new SSA values (phi_687_0_123) that merge
        multiple versions (sideB, side6). Without tracking, rendering falls back
        to alias which maps to wrong version.

        Solution: For each PHI node, determine which version it represents using
        semantic heuristics and add mapping to value_to_version.
        """
        for block_id in sorted(self.func_block_ids):
            ssa_instrs = self.ssa_func.instructions.get(block_id, [])

            for inst in ssa_instrs:
                if inst.mnemonic != 'PHI':
                    continue

                if not inst.outputs or not inst.inputs:
                    continue

                phi_output = inst.outputs[0]
                phi_var_name = self._extract_local_name(phi_output)


                if not phi_var_name:
                    continue

                # Determine which version this PHI represents
                chosen_version = self._resolve_phi_version(inst, phi_var_name)

                if chosen_version is not None:
                    # Map PHI output to chosen version
                    original_alias = phi_output.alias or ""
                    self.value_to_version[phi_output.name] = (phi_var_name, chosen_version, original_alias)


    def _detect_struct_types(self):
        """
        FIX #5 Phase 2: Detect struct types from XCALL function arguments.

        Analyzes XCALL instructions to determine which variables are passed to functions
        expecting specific struct types. Sets struct_type field on VariableVersion.

        Example:
            SC_MP_GetSRVsettings(&tmp31) → tmp31 is s_SC_MP_SRV_settings → name it "SRVset"
        """
        if not self.ssa_func.scr or not self.ssa_func.scr.xfn_table:
            return

        xfn_entries = getattr(self.ssa_func.scr.xfn_table, 'entries', [])
        if not xfn_entries:
            return

        # Scan all XCALL instructions
        for block_id in self.func_block_ids:
            ssa_instrs = self.ssa_func.instructions.get(block_id, [])
            for inst in ssa_instrs:
                if inst.mnemonic != 'XCALL':
                    continue

                # Get XFN index from instruction
                if not inst.instruction or not inst.instruction.instruction:
                    continue

                xfn_index = inst.instruction.instruction.arg1
                if xfn_index >= len(xfn_entries):
                    continue

                xfn_entry = xfn_entries[xfn_index]
                if not xfn_entry.name or '(' not in xfn_entry.name:
                    continue

                # Parse function signature to extract parameter types
                # Format: "SC_MP_GetSRVsettings(*s_SC_MP_SRV_settings)void"
                func_signature = xfn_entry.name
                self._parse_and_apply_signature(inst, func_signature)

    def _parse_and_apply_signature(self, inst, func_signature: str):
        """
        Parse function signature and apply struct types to variables.

        FIX #5 Phase 2: Improved to only mark the SPECIFIC SSA value used in the call,
        not all versions of the variable.

        Args:
            inst: XCALL SSA instruction
            func_signature: Full signature like "SC_MP_GetSRVsettings(*s_SC_MP_SRV_settings)void"
        """
        # Extract parameter types from signature
        # Format: FuncName(type1,type2,...)returntype
        if '(' not in func_signature or ')' not in func_signature:
            return

        # Extract parameter list
        params_start = func_signature.index('(') + 1
        params_end = func_signature.index(')')
        params_str = func_signature[params_start:params_end]

        if not params_str:
            return

        # Split parameters
        param_types = [p.strip() for p in params_str.split(',')]

        # Match XCALL inputs to parameter types
        # Note: XCALL inputs may be in reverse order depending on calling convention
        for i, input_val in enumerate(inst.inputs):
            if not input_val or not input_val.name:
                continue

            # Determine parameter index (may need to reverse)
            param_idx = i if i < len(param_types) else len(param_types) - 1

            if param_idx >= len(param_types):
                continue

            param_type = param_types[param_idx]
            normalized_param_type = param_type.replace(" ", "")

            # Check if parameter is a struct pointer (starts with * and contains s_)
            if normalized_param_type.startswith('*') and 's_' in normalized_param_type:
                # Extract struct name: "*s_SC_MP_SRV_settings" → "s_SC_MP_SRV_settings"
                struct_type = normalized_param_type[1:]  # Remove * prefix

                # FIX #5 Phase 2: Map this specific SSA value to the struct type
                # Store it in value_to_version with struct type info
                # We'll check this later when assigning names
                if input_val.name in self.value_to_version:
                    var_name, version_num, orig_alias = self.value_to_version[input_val.name]

                    # Find the specific version and mark it
                    if var_name in self.variable_versions:
                        for ver in self.variable_versions[var_name]:
                            if ver.version == version_num:
                                # Only set struct_type if not already set or if this is more specific
                                if not ver.struct_type:
                                    ver.struct_type = struct_type
                                break

    def _resolve_phi_version(self, phi_inst, var_name: str) -> Optional[int]:
        """
        Determine which version a PHI node should map to.

        Resolution priority:
        1. Type confidence from TypeInferenceEngine (if available)
           - Prefer inputs with higher type confidence (>0.5 threshold)
        2. Semantic heuristics (fallback):
           a. Skip constant producers (GCP/LCP/ICP/FCP/DCP)
           b. Pick first non-constant version

        Returns:
            Version number (0, 1, 2, ...) or None if cannot determine
        """
        # Collect input mappings with SSA value names for type lookup
        input_mappings = []
        for inp in phi_inst.inputs:
            mapping = self.value_to_version.get(inp.name)
            if mapping:
                base_name, version_num, alias = mapping
                if base_name == var_name:  # Same variable
                    input_mappings.append((inp, version_num, inp.name))

        if not input_mappings:
            return None

        if len(input_mappings) == 1:
            # Only one input maps to this variable
            return input_mappings[0][1]

        # Priority 1: Use type confidence if TypeInferenceEngine is available
        if self.type_engine:
            scored_inputs = []
            for inp, version_num, ssa_name in input_mappings:
                confidence = self.type_engine.get_confidence(ssa_name)
                scored_inputs.append((confidence, version_num, ssa_name))

            # Sort by confidence (descending)
            scored_inputs.sort(reverse=True, key=lambda x: x[0])

            # If best input has confidence > 0.5, use it
            if scored_inputs and scored_inputs[0][0] > 0.5:
                return scored_inputs[0][1]

        # Fallback: Semantic heuristics
        # Heuristic 1: Check for constant producers
        non_constant_versions = []
        for inp, version_num, ssa_name in input_mappings:
            # Check if this input comes from constant assignment
            if inp.producer_inst:
                # GCP/LCP/ICP = constant load
                if inp.producer_inst.mnemonic in {'GCP', 'LCP', 'ICP', 'FCP', 'DCP'}:
                    # Skip this version (it's likely the constant branch)
                    continue
            non_constant_versions.append(version_num)

        if non_constant_versions:
            # Return first non-constant version
            return non_constant_versions[0]

        # Last resort: return first version
        return input_mappings[0][1]

    def _infer_semantic_types(self):
        """
        Inferuje sémantický typ pro každou verzi proměnné.

        Heuristiky:
        - Použita v for-loop jako counter → loop_counter
        - Přiřazena z .side fieldu → side_value
        - Použita jen 1-2x → temp
        - První dvě verze v blízké vzdálenosti → pravděpodobně sideA/sideB pattern
        - FIX #5 Phase 2: Passed to function expecting struct → struct_value

        NOTE: Performance is now O(n) thanks to pre-built indices in _build_indices().
        The old O(n²) workaround that skipped analysis for large functions has been removed.
        """
        # First pass: Detect struct types from function calls
        self._detect_struct_types()

        for var_name, versions in self.variable_versions.items():
            # FIX P0.4.2: REMOVED overly aggressive special case
            # Old logic assumed "2 versions close together = sideA/sideB" which caused false positives
            # Now we rely on proper pattern matching in _guess_semantic_type()

            for ver in versions:
                # Check semantic type from usage patterns (even for single-version vars!)
                # Now efficient for all function sizes thanks to pre-built indices
                ver.semantic_type = self._guess_semantic_type(var_name, ver)

    def _is_used_in_field_access(self, ssa_value_name: str) -> bool:
        """
        Check if SSA value is used in pointer+offset (PNT) operations, indicating struct field access.

        This is used to PROTECT struct variables from being renamed to short names like 'i', 'j'.
        If a variable is used for field access (e.g., ai_props.watchfulness), it should keep
        its semantic name to maintain code readability.

        Uses pre-built _mnemonic_index for O(1) lookup of PNT instructions instead of
        iterating over all blocks.

        Args:
            ssa_value_name: SSA value name to check (e.g., "t456_0")

        Returns:
            True if this value is used as base pointer in PNT operations
        """
        # Use mnemonic index to get only PNT instructions - O(1) lookup
        for inst in self._mnemonic_index.get('PNT', []):
            # PNT (pointer + offset) indicates struct field access
            # Check if this value is the base pointer (first input)
            if inst.inputs and len(inst.inputs) > 0:
                base_input = inst.inputs[0]
                # Check both name and alias
                if base_input.name == ssa_value_name or base_input.alias == ssa_value_name:
                    return True
        return False

    def _is_asp_allocated_counter(self, var_name: str, ver: VariableVersion) -> bool:
        """
        Detect ASP-based loop counter pattern.

        Pattern:
            ASP 1       ; Allocate 1 stack slot for counter
            ...
            INC local_X ; Increment counter
            JLT loop    ; Loop while less than

        This pattern is common when the compiler allocates a loop counter
        using ASP instruction instead of using pre-existing local variables.

        Uses pre-built indices for O(1) lookups instead of iterating over all blocks.

        Args:
            var_name: Variable name to check
            ver: Variable version

        Returns:
            True if this appears to be an ASP-allocated loop counter
        """
        asp_found = False
        inc_dec_found = False
        comparison_found = False

        # Check ASP instructions near first_def using mnemonic index
        for inst in self._mnemonic_index.get('ASP', []):
            if ver.first_def - 10 <= inst.address <= ver.first_def:
                asp_found = True
                break

        # Check INC/DEC of this variable using mnemonic index
        for mnemonic in ('INC', 'DEC'):
            for inst in self._mnemonic_index.get(mnemonic, []):
                for output in inst.outputs:
                    if self._extract_local_name(output) == var_name:
                        inc_dec_found = True
                        break
                if inc_dec_found:
                    break
            if inc_dec_found:
                break

        # Check comparison operations using var_instructions index
        comparison_mnemonics = {'ULE', 'UGE', 'ULT', 'UGT', 'ILE', 'IGE', 'ILT', 'IGT', 'EQU', 'NEQ'}
        for inst in self._var_instructions.get(var_name, []):
            if inst.mnemonic in comparison_mnemonics:
                comparison_found = True
                break

        # ASP + (INC/DEC) + comparison = likely loop counter
        return asp_found and inc_dec_found and comparison_found

    def _guess_semantic_type(self, var_name: str, ver: VariableVersion) -> str:
        """
        Hádej sémantický typ z usage patterns.

        Detekované typy:
        - struct_value: Passed to function expecting specific struct type (FIX #5 Phase 2)
        - loop_counter: Inkrementováno/dekrementováno v loop
        - side_value: Přiřazeno z .side nebo .field2 struktury
        - temp: Použito jen 1-2x
        - general: Default

        Uses pre-built indices for O(1) lookups instead of O(n²) iteration.
        """
        # FIX #5 Phase 2: Check if struct type was detected
        if ver.struct_type:
            return "struct_value"

        # NEW: PROTECT variables used in field access from being renamed to short names
        # Check if any SSA name in this version is used as base pointer in PNT operations
        # Find all SSA names that belong to this version
        for ssa_name, (vname, vnum, _) in self.value_to_version.items():
            if vname == var_name and vnum == ver.version:
                if self._is_used_in_field_access(ssa_name):
                    # This variable is used for struct field access (e.g., ai_props.watchfulness)
                    # Return struct_value to prevent renaming to 'i', 'j', 'k'
                    return "struct_value"

        # NEW: Check for ASP-based loop counter pattern
        if self._is_asp_allocated_counter(var_name, ver):
            return "loop_counter"

        # Collect uses of this variable using pre-built index - O(uses) instead of O(blocks × instructions)
        uses = []
        mnemonics_used = []

        for inst in self._var_instructions.get(var_name, []):
            # Skip PHI nodes for mnemonic analysis (they don't represent real operations)
            if inst.mnemonic == 'PHI':
                continue

            # For versioned variables, check if this is the right version
            # by checking if address is in reasonable range
            # (after first_def, allowing for negative last_use from PHI)
            if inst.address >= ver.first_def or (ver.last_use < 0 and inst.address >= 0):
                uses.append(inst)
                mnemonics_used.append(inst.mnemonic)

        # Pattern 1: Loop counter detection
        # Check for INC/DEC instructions
        if "INC" in mnemonics_used or "DEC" in mnemonics_used:
            return "loop_counter"

        # FIX #5 Phase 2: Also detect ADD/SUB pattern (i = i + 1)
        # Loop counters are characterized by:
        # 1. Used in ADD/SUB operation
        # 2. Used in comparison operation (ULE, UGE, etc.)
        # 3. Short lifetime (typical for loop counters)
        has_add_sub = any(m in mnemonics_used for m in {"ADD", "SUB", "IADD", "ISUB"})
        has_comparison = any(m in mnemonics_used for m in {"ULE", "UGE", "ULT", "UGT", "ILE", "IGE", "ILT", "IGT", "EQU", "NEQ", "ULES", "UGES", "ULTS", "UGTS"})

        if has_add_sub and has_comparison:
            # Very likely a loop counter
            return "loop_counter"

        # FIX #5 Phase 2: Alternative - detect variables used only in tight loops
        # If a variable is used in ADD and then immediately in comparison, it's likely a loop counter
        if has_add_sub and len(uses) <= 10:
            # Check if this variable is modified within its own lifetime (classic loop counter pattern)
            # Variable is loaded, incremented, stored back, and compared - all in small range
            address_range = ver.last_use - ver.first_def if ver.last_use > ver.first_def else 0
            if address_range < 50 and has_comparison:
                # Tight loop with comparison - likely loop counter
                return "loop_counter"

        # Pattern 2: Side value detection (player_info.field2 → side)
        # MUST check BEFORE temp check! Many side values are used sparingly.
        # Use addr_index for O(1) lookup of instructions near first_def
        first_def_inst = self._addr_index.get(ver.first_def)
        if first_def_inst and first_def_inst.mnemonic == 'ASGN':
            # Check instructions before ASGN for DCP/DLD loading from .side field
            # Pattern: LADR &player_info → PNT +8 → DCP → LADR &local_10 → ASGN
            for offset in range(1, 6):  # Check 5 addresses before ASGN
                nearby_inst = self._addr_index.get(ver.first_def - offset)
                if nearby_inst:
                    # Look for struct access in ALL nearby instructions
                    for val in nearby_inst.outputs + nearby_inst.inputs:
                        if hasattr(val, 'alias') and val.alias:
                            # FIX P0.4.2: Remove hardcoded variable names, use only field patterns
                            if any(pattern in val.alias for pattern in ['.side', '.field2', '.field_2']):
                                return "side_value"

        # Check instructions AT or NEAR first_def (within 3 instructions)
        for offset in range(-3, 4):
            inst_at_offset = self._addr_index.get(ver.first_def + offset)
            if not inst_at_offset:
                continue

            # Pattern 1: DCP/DLD instruction that produces the value
            if inst_at_offset.mnemonic in {'DCP', 'DLD', 'ILD', 'CLD', 'SLD'}:
                # FIX P0.4.2: Check previous instruction to distinguish:
                # - PNT (struct.field) → TRUE side value
                # - DADR (pointer->field) → FALSE POSITIVE, skip
                prev_inst = self._addr_index.get(inst_at_offset.address - 1)

                # Only detect as side_value if preceded by PNT (struct field access)
                if prev_inst and prev_inst.mnemonic == 'PNT':
                    # FIX P0.4.2: PNT + offset pattern = struct field access
                    # Check if PNT has offset argument typical for .side/.field2 (offset 8)
                    # Pattern: LADR &player_info → PNT +8 → DCP → ASGN
                    pnt_offset = None
                    if prev_inst.instruction and hasattr(prev_inst.instruction, 'instruction'):
                        pnt_offset = prev_inst.instruction.instruction.arg1
                    # Common field offsets: 8 (.side, .field2), 0 (first field), 4, 12, etc.
                    # For now, accept offset 8 as strong indicator of side/field2
                    if pnt_offset == 8:
                        return "side_value"
                elif prev_inst and prev_inst.mnemonic == 'DADR':
                    # This is pointer->field access (FALSE POSITIVE - skip)
                    pass
                else:
                    # No clear previous instruction or other pattern - check carefully
                    for val in inst_at_offset.outputs + inst_at_offset.inputs:
                        if hasattr(val, 'alias') and val.alias:
                            alias = val.alias
                            # Be MORE SPECIFIC - only exact field patterns with dots
                            if any(pattern in alias for pattern in ['.side', '.field2', '.field_2']):
                                return "side_value"

            # Pattern 2: Check if instruction has inputs from struct field
            for output in inst_at_offset.outputs:
                extracted_name = self._extract_local_name(output)
                if extracted_name == var_name or (extracted_name and extracted_name.replace('&', '') == var_name):
                    # This instruction produces our variable
                    # Check its inputs for side-related aliases
                    if inst_at_offset.inputs:
                        for inp in inst_at_offset.inputs:
                            if hasattr(inp, 'alias') and inp.alias:
                                # FIX P0.4.2: Remove generic 'side' substring check
                                # Use only specific field patterns with dots
                                if '.side' in inp.alias or '.field2' in inp.alias or '.field_2' in inp.alias:
                                    return "side_value"

        # Pattern 3: Temp variable (used sparingly)
        if len(uses) <= 2:
            return "temp"

        return "general"

    def _assign_final_names(self):
        """Přiřadí finální jména verzím podle sémantického typu."""
        for var_name, versions in self.variable_versions.items():
            # Always use semantic type to generate names
            # Even single-version variables can be side_value, loop_counter, etc.
            for ver in versions:
                # Heritage SSA: Check if heritage metadata provides a preferred name
                heritage_name = self._get_heritage_name(var_name, ver)
                if heritage_name:
                    ver.assigned_name = heritage_name
                # Generate name based on semantic type, or keep original for "general" type
                elif ver.semantic_type == "general" and len(versions) == 1:
                    ver.assigned_name = var_name
                else:
                    ver.assigned_name = self._generate_name(ver)

    def _get_heritage_name(self, var_name: str, ver: VariableVersion) -> Optional[str]:
        """
        Get variable name from heritage metadata if available.

        Heritage SSA provides better variable discovery through multi-pass analysis.
        This method checks if a heritage-discovered name should be used instead of
        the generic naming scheme.

        Args:
            var_name: Original variable name (e.g., "local_8")
            ver: VariableVersion with semantic type info

        Returns:
            Heritage-derived name if available and appropriate, None otherwise.
        """
        if not self._heritage_vars:
            return None

        # Check if heritage has info for this variable
        if var_name not in self._heritage_vars:
            return None

        heritage_info = self._heritage_vars[var_name]
        heritage_type = heritage_info.get("type", "UNKNOWN")
        heritage_space = heritage_info.get("space", "STACK")

        # For parameters, heritage provides better tracking
        if heritage_space == "PARAM":
            # Use param_N naming which is clearer
            return f"param_{abs(heritage_info.get('offset', 0)) - 3}"

        # If heritage detected specific type, use that to generate better name
        if heritage_type != "UNKNOWN":
            # Generate type-based names for stack variables
            if heritage_space == "STACK":
                if heritage_type == "FLOAT":
                    return self._generate_heritage_float_name()
                elif heritage_type == "POINTER":
                    return self._generate_heritage_pointer_name()
                # INT and other types: let semantic analysis decide
                # by returning None

        return None

    def _generate_heritage_float_name(self) -> str:
        """
        Generate a name for a heritage-detected float variable.

        Returns names like: f, f1, f2, time, dist, etc.
        """
        # Use a counter for float variables if not already initialized
        if not hasattr(self, '_heritage_float_counter'):
            self._heritage_float_counter = 0

        idx = self._heritage_float_counter
        self._heritage_float_counter += 1

        float_names = ['f', 'f1', 'f2', 'f3']
        if idx < len(float_names):
            return float_names[idx]
        return f"f{idx}"

    def _generate_heritage_pointer_name(self) -> str:
        """
        Generate a name for a heritage-detected pointer variable.

        Returns names like: ptr, ptr1, obj, etc.
        """
        # Use a counter for pointer variables if not already initialized
        if not hasattr(self, '_heritage_ptr_counter'):
            self._heritage_ptr_counter = 0

        idx = self._heritage_ptr_counter
        self._heritage_ptr_counter += 1

        ptr_names = ['ptr', 'ptr1', 'ptr2', 'obj']
        if idx < len(ptr_names):
            return ptr_names[idx]
        return f"ptr{idx}"

    def _generate_name(self, ver: VariableVersion) -> str:
        """Vygeneruj pojmenování pro verzi."""
        # FIX #5 Phase 2: Handle struct_value type first
        if ver.semantic_type == "struct_value" and ver.struct_type:
            # Generate name from struct type
            base_name = extract_struct_name_from_type(ver.struct_type)
            # Check if we need a numeric suffix (multiple variables of same struct type)
            # For now, just return the base name
            return base_name

        if ver.semantic_type == "loop_counter":
            # i, j, k
            counter_names = ['i', 'j', 'k']
            idx = self.name_counters['loop_counter']
            self.name_counters['loop_counter'] += 1
            if idx < len(counter_names):
                return counter_names[idx]
            else:
                return f"idx{idx - len(counter_names)}"

        elif ver.semantic_type == "side_value":
            # sideA, sideB
            side_names = ['sideA', 'sideB']
            idx = self.name_counters['side_value']
            self.name_counters['side_value'] += 1
            if idx < len(side_names):
                return side_names[idx]
            else:
                return f"side{idx}"

        elif ver.semantic_type == "temp":
            # tmp, tmp1, tmp2
            idx = self.name_counters['temp']
            self.name_counters['temp'] += 1
            if idx == 0:
                return "tmp"
            else:
                return f"tmp{idx}"

        else:
            # general → ponechej base_name s version suffix
            if ver.version == 0:
                return ver.base_name
            else:
                return f"{ver.base_name}_v{ver.version}"

    def _build_rename_map(self) -> Dict[str, str]:
        """
        Vytvoř mapování SSA value names → finální jména.

        KRITICKÉ: Musíme mapovat SSA value NAMES (t123_0, t456_0), ne aliasy!
        Aliasy jsou stejné pro obě hodnoty (local_2), SSA names jsou unikátní.

        DŮLEŽITÉ: Zachovává & prefix pro address values!
        Pokud originální alias byl "&local_10" a přejmenujeme na "side4",
        výsledek bude "&side4", ne "side4".

        Returns:
            Dict: SSA value name → finální jméno
            Například: {
                "t123_0": "sideA",     # První přiřazení do local_2
                "t124_0": "sideA",     # Další použití stejné verze
                "t456_0": "sideB",     # Druhá verze local_2
                "t457_0": "sideB",     # Použití druhé verze
                "t659_0": "&side4",    # Address of local_10 → address of side4
            }
        """
        rename_map = {}

        # Projdi všechny SSA values a najdi jejich verzi
        for value_name, (base_name, version_num, original_alias) in self.value_to_version.items():
            # Najdi VariableVersion objekt pro tuto verzi
            if base_name in self.variable_versions:
                versions = self.variable_versions[base_name]
                for ver in versions:
                    if ver.version == version_num:
                        # Mapuj SSA value name → finální jméno
                        new_name = ver.assigned_name

                        # FIX P0.4.1: Preserve & prefix for address values!
                        # If original alias was "&local_10", result should be "&side4"
                        if original_alias.startswith("&"):
                            new_name = "&" + new_name

                        rename_map[value_name] = new_name
                        break

        return rename_map
