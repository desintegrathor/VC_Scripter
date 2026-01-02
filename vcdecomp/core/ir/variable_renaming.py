"""
Variable Renaming - P0.4 Fix

Detekuje kdy jedna local_X proměnná je použita pro více sémantických účelů
a rozdělí ji na více pojmenovaných proměnných (sideA, sideB, i, j, tmp, ...).
"""

from __future__ import annotations
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict

from .ssa import SSAFunction, SSAValue


@dataclass
class VariableVersion:
    """Představuje jednu verzi proměnné (např. local_2 version 0, 1, 2)."""
    base_name: str  # "local_2"
    version: int    # 0, 1, 2, ...
    first_def: int  # Address prvního přiřazení
    last_use: int   # Address posledního použití
    semantic_type: str = "general"  # loop_counter, side_value, temp, general
    assigned_name: str = ""  # Finální pojmenování (i, sideA, tmp1, ...)


class VariableRenamer:
    """
    Analyzuje SSA funkci a detekuje kdy local_X proměnná potřebuje splitting.

    Approach:
    1. Analyzuj každé přiřazení do local_X
    2. Zjisti zda je to "nová" definice (předchozí use byl dávno) → nová version
    3. Každé verzi přiřaď sémantický typ
    4. Vygeneruj nové jméno podle typu
    """

    def __init__(self, ssa_func: SSAFunction, func_block_ids: Set[int]):
        self.ssa_func = ssa_func
        self.func_block_ids = func_block_ids

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

    def analyze_and_rename(self) -> Dict[str, str]:
        """
        Hlavní entry point.

        Returns:
            Dict mapující původní alias (local_2) → nový název (sideA, i, tmp)
        """
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
                        if var_name in ('local_10', 'local_11', 'local_12'):
                            import sys
                            print(f"[DEBUG LOAD INIT] @{addr} {inst.mnemonic} is_address_for_write={is_address_for_write}", file=sys.stderr)
                            sys.stderr.flush()

                        if inst.mnemonic == 'LADR':
                            # Find next instruction
                            next_inst = None
                            for future_inst in ssa_instrs:
                                if future_inst.address == addr + 1:
                                    next_inst = future_inst
                                    break

                            import sys
                            if next_inst:
                                mnem = str(next_inst.mnemonic).strip()
                                is_asgn_check = (mnem == 'ASGN')
                                if var_name in ('local_10', 'local_11', 'local_12'):
                                    print(f"[DEBUG LADR] @{addr} mnem={repr(mnem)} is_asgn={is_asgn_check}", file=sys.stderr)
                                    sys.stderr.flush()

                                # Check if next is ASGN
                                import sys
                                print(f"[DEBUG LADR BEFORE IF] @{addr} is_asgn_check={is_asgn_check}", file=sys.stderr)
                                sys.stderr.flush()
                                if is_asgn_check:
                                    print(f"[DEBUG LADR] → ENTERED is_asgn_check block @{addr}", file=sys.stderr)
                                    sys.stderr.flush()
                                    # This LADR is for write, not read
                                    is_address_for_write = True
                                    if var_name in ('local_10', 'local_11', 'local_12'):
                                        print(f"[DEBUG LADR] → SKIP last_use (is write)", file=sys.stderr)
                                        sys.stderr.flush()
                            else:
                                if var_name in ('local_10', 'local_11', 'local_12'):
                                    print(f"[DEBUG LADR] @{addr} next=NONE", file=sys.stderr)

                        if var_name in ('local_10', 'local_11', 'local_12'):
                            import sys
                            print(f"[DEBUG LOAD] @{addr} BEFORE last_use check, is_address_for_write={is_address_for_write}", file=sys.stderr)
                            sys.stderr.flush()

                        if not is_address_for_write:
                            # Update last_use for this version (true READ)
                            if var_name in self.variable_versions and version < len(self.variable_versions[var_name]):
                                self.variable_versions[var_name][version].last_use = addr
                                import sys
                                if var_name in ('local_10', 'local_11', 'local_12'):
                                    print(f"[DEBUG LOAD] → UPDATE last_use={addr}", file=sys.stderr)
                                    sys.stderr.flush()

                        if var_name in ('local_10', 'local_11', 'local_12'):
                            import sys
                            print(f"[DEBUG LOAD] @{addr} BEFORE continue", file=sys.stderr)
                            sys.stderr.flush()

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

                    var_name = self._extract_local_name(addr_value)

                    import sys
                    if var_name and var_name in ('local_10', 'local_11', 'local_12'):
                        print(f"[DEBUG ASGN] @{addr} ASGN to {var_name}, inputs={[(inp.name, inp.alias) for inp in inst.inputs]}, current_version={current_version.get(var_name, 0)}", file=sys.stderr)

                    if var_name:
                        # This is an assignment to local_X
                        version = current_version[var_name]

                        # Check if we need new version
                        if var_name in last_assignment:
                            import sys
                            if var_name in ('local_10', 'local_11', 'local_12'):
                                print(f"[DEBUG ASGN CHECK] {var_name}: last_assignment={last_assignment[var_name]}, last_use={last_use.get(var_name, 'NONE')}, addr={addr}", file=sys.stderr)
                            if var_name in last_use and last_use[var_name] > last_assignment[var_name]:
                                version += 1
                                current_version[var_name] = version
                                import sys
                                if var_name in ('local_10', 'local_11', 'local_12'):
                                    print(f"[DEBUG ASGN CHECK] → NEW VERSION {version}", file=sys.stderr)

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

        # Jen local_ proměnné
        if not var_name.startswith("local_"):
            return None

        return var_name

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

                import sys
                print(f"[DEBUG PHI ALL] @{inst.address} PHI {phi_output.name} (alias={phi_output.alias}), var_name={phi_var_name}, inputs={[(inp.name, inp.alias) for inp in inst.inputs]}", file=sys.stderr)

                if not phi_var_name:
                    continue

                # Determine which version this PHI represents
                chosen_version = self._resolve_phi_version(inst, phi_var_name)

                if chosen_version is not None:
                    # Map PHI output to chosen version
                    original_alias = phi_output.alias or ""
                    self.value_to_version[phi_output.name] = (phi_var_name, chosen_version, original_alias)

                    import sys
                    print(f"[DEBUG PHI] {phi_var_name}: PHI {phi_output.name} → version {chosen_version}, inputs={[inp.name for inp in inst.inputs]}", file=sys.stderr)

    def _resolve_phi_version(self, phi_inst, var_name: str) -> Optional[int]:
        """
        Determine which version a PHI node should map to using semantic heuristics.

        Heuristics (in order of priority):
        1. If one input is from constant assignment (-1, 0, etc.), pick the other
        2. If inputs have different semantic types, pick higher priority:
           side_value > loop_counter > temp > general
        3. Otherwise, pick first input

        Returns:
            Version number (0, 1, 2, ...) or None if cannot determine
        """
        # Collect input mappings
        input_mappings = []
        for inp in phi_inst.inputs:
            mapping = self.value_to_version.get(inp.name)
            if mapping:
                base_name, version_num, alias = mapping
                if base_name == var_name:  # Same variable
                    input_mappings.append((inp, version_num))

        if not input_mappings:
            return None

        if len(input_mappings) == 1:
            # Only one input maps to this variable
            return input_mappings[0][1]

        # Heuristic 1: Check for constant producers
        non_constant_versions = []
        import sys
        for inp, version_num in input_mappings:
            # Check if this input comes from constant assignment
            print(f"[DEBUG PHI RESOLVE] {var_name} v{version_num}: inp={inp.name}, producer={inp.producer_inst.mnemonic if inp.producer_inst else None}", file=sys.stderr)
            if inp.producer_inst:
                # GCP/LCP/ICP = constant load
                if inp.producer_inst.mnemonic in {'GCP', 'LCP', 'ICP', 'FCP', 'DCP'}:
                    # Check if it loads a small constant value (heuristic for -1, 0, 1, etc.)
                    # Skip this version (it's likely the constant branch)
                    print(f"[DEBUG PHI RESOLVE]   SKIPPING constant producer {inp.producer_inst.mnemonic}", file=sys.stderr)
                    continue
            non_constant_versions.append(version_num)
            print(f"[DEBUG PHI RESOLVE]   KEEPING version {version_num}", file=sys.stderr)

        if non_constant_versions:
            # Return first non-constant version
            return non_constant_versions[0]

        # Heuristic 2: Pick version with highest semantic priority
        # (Will be applied AFTER _infer_semantic_types, so this is backup)
        # For now, just return first version
        return input_mappings[0][1]

    def _infer_semantic_types(self):
        """
        Inferuje sémantický typ pro každou verzi proměnné.

        Heuristiky:
        - Použita v for-loop jako counter → loop_counter
        - Přiřazena z .side fieldu → side_value
        - Použita jen 1-2x → temp
        - První dvě verze v blízké vzdálenosti → pravděpodobně sideA/sideB pattern
        """
        for var_name, versions in self.variable_versions.items():
            # FIX P0.4.2: REMOVED overly aggressive special case
            # Old logic assumed "2 versions close together = sideA/sideB" which caused false positives
            # Now we rely on proper pattern matching in _guess_semantic_type()

            for ver in versions:
                # Check semantic type from usage patterns (even for single-version vars!)
                ver.semantic_type = self._guess_semantic_type(var_name, ver)

    def _guess_semantic_type(self, var_name: str, ver: VariableVersion) -> str:
        """
        Hádej sémantický typ z usage patterns.

        Detekované typy:
        - loop_counter: Inkrementováno/dekrementováno v loop
        - side_value: Přiřazeno z .side nebo .field2 struktury
        - temp: Použito jen 1-2x
        - general: Default
        """
        # Prozkoumej instrukce mezi first_def a last_use
        uses = []
        mnemonics_used = []

        for block_id in self.func_block_ids:
            ssa_instrs = self.ssa_func.instructions.get(block_id, [])
            for inst in ssa_instrs:
                if ver.first_def <= inst.address <= ver.last_use:
                    # Check zda používá tuto proměnnou
                    for inp in inst.inputs:
                        if self._extract_local_name(inp) == var_name:
                            uses.append(inst)
                            mnemonics_used.append(inst.mnemonic)

        # Pattern 1: Loop counter detection
        if "INC" in mnemonics_used or "DEC" in mnemonics_used:
            return "loop_counter"

        # Pattern 2: Side value detection (player_info.field2 → side)
        # MUST check BEFORE temp check! Many side values are used sparingly.
        # For ASGN-based assignments, check the VALUE being assigned (inputs[0])
        # For other assignments, check instructions near first_def
        import sys
        for block_id in self.func_block_ids:
            ssa_instrs = self.ssa_func.instructions.get(block_id, [])
            for ssa_inst in ssa_instrs:
                # If this is the ASGN that created this version, check instructions nearby
                # to detect if value comes from struct field access
                if ssa_inst.mnemonic == 'ASGN' and ssa_inst.address == ver.first_def:
                    # Check instructions before ASGN for DCP/DLD loading from .side field
                    # Pattern: LADR &player_info → PNT +8 → DCP → LADR &local_10 → ASGN
                    for ssa_inst2 in ssa_instrs:
                        # Check instructions within 5 addresses before ASGN
                        if ssa_inst.address - 5 <= ssa_inst2.address < ssa_inst.address:
                            # Look for struct access in ALL nearby instructions
                            for val in ssa_inst2.outputs + ssa_inst2.inputs:
                                if hasattr(val, 'alias') and val.alias:
                                    # FIX P0.4.2: Remove hardcoded variable names, use only field patterns
                                    if any(pattern in val.alias for pattern in ['.side', '.field2', '.field_2']):
                                        return "side_value"

                # Check instructions AT or NEAR first_def (within 3 instructions)
                if abs(ssa_inst.address - ver.first_def) <= 3:
                    # Pattern 1: DCP/DLD instruction that produces the value
                    if ssa_inst.mnemonic in {'DCP', 'DLD', 'ILD', 'CLD', 'SLD'}:
                        # FIX P0.4.2: Check previous instruction to distinguish:
                        # - PNT (struct.field) → TRUE side value
                        # - DADR (pointer->field) → FALSE POSITIVE, skip
                        prev_inst = None
                        for prev_candidate in ssa_instrs:
                            if prev_candidate.address == ssa_inst.address - 1:
                                prev_inst = prev_candidate
                                break

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
                            for val in ssa_inst.outputs + ssa_inst.inputs:
                                if hasattr(val, 'alias') and val.alias:
                                    alias = val.alias
                                    # Be MORE SPECIFIC - only exact field patterns with dots
                                    if any(pattern in alias for pattern in ['.side', '.field2', '.field_2']):
                                        return "side_value"

                    # Pattern 2: Check if instruction has inputs from struct field
                    for output in ssa_inst.outputs:
                        extracted_name = self._extract_local_name(output)
                        if extracted_name == var_name or (extracted_name and extracted_name.replace('&', '') == var_name):
                            # This instruction produces our variable
                            # Check its inputs for side-related aliases
                            if ssa_inst.inputs:
                                for inp in ssa_inst.inputs:
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
                # Generate name based on semantic type, or keep original for "general" type
                if ver.semantic_type == "general" and len(versions) == 1:
                    ver.assigned_name = var_name
                else:
                    ver.assigned_name = self._generate_name(ver)

    def _generate_name(self, ver: VariableVersion) -> str:
        """Vygeneruj pojmenování pro verzi."""
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
