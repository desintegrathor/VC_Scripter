"""
Global Variable Resolver

Detekuje a pojmenovává globální proměnné na základě usage patterns:
- Proměnné v _init které se ukládají do global segmentu
- data_X offsety používané napříč funkcemi (GCP/GLD/DCP)
- Globální pole - indexované přístupy
"""

from __future__ import annotations

from typing import Dict, Set, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict

from .ssa import SSAFunction, SSAInstruction
from ..disasm import opcodes


@dataclass
class GlobalUsage:
    """Sleduje použití globální proměnné."""
    offset: int  # Data segment offset
    name: str = ""  # Odvozený název (např. gRecs, gEndRule)

    # Usage statistics
    read_count: int = 0
    write_count: int = 0
    functions_used: Set[str] = field(default_factory=set)

    # Pattern indicators
    is_incremented: bool = False  # ADD/INC operace
    is_decremented: bool = False  # SUB/DEC operace
    is_compared: bool = False      # EQU/GRE/LESS operace
    is_array_base: bool = False    # Používá se s indexem (offset + i*size)
    array_element_size: Optional[int] = None  # Velikost prvku (4, 16, atd.)
    is_array_element: bool = False  # Je součástí pole (ne samostatná proměnná)
    array_base_offset: Optional[int] = None  # Offset base pole pokud is_array_element=True

    # Type hints
    possible_types: Set[str] = field(default_factory=set)  # "int", "float", "ptr", atd.

    # NEW: Header mapping (SGI constants)
    sgi_index: Optional[int] = None  # SGI constant index (1-4096)
    sgi_name: Optional[str] = None   # e.g., "SGI_MISSIONDEATHCOUNT"
    header_type: Optional[str] = None  # Type hint from headers

    # NEW: Type inference
    inferred_type: Optional[str] = None  # Aggressively inferred type
    type_confidence: float = 0.0  # Confidence (0.0-1.0)

    # NEW: Struct reconstruction
    is_struct_base: bool = False  # This global is a structure
    inferred_struct: Optional[object] = None  # InferredStruct instance (from struct_inference)
    struct_typedef: Optional[str] = None  # Generated typedef


class GlobalResolver:
    """
    Resolver pro detekci a pojmenování globálních proměnných.

    Enhanced with:
    - Type inference from instruction patterns
    - SGI constant mapping from SC_sgi/SC_ggi calls
    - Struct reconstruction support
    """

    def __init__(self, ssa_func: SSAFunction, aggressive_typing: bool = True, infer_structs: bool = True, symbol_db=None):
        self.ssa_func = ssa_func
        self.scr = ssa_func.scr
        self.globals: Dict[int, GlobalUsage] = {}  # offset -> usage
        self.resolver = getattr(ssa_func.scr, "opcode_resolver", opcodes.DEFAULT_RESOLVER)
        self.aggressive_typing = aggressive_typing
        self.infer_structs = infer_structs

        # Type inference engine (imported lazily to avoid circular imports)
        self.type_inference = None

        # Struct inference engine (imported lazily)
        self.struct_inference = None

        # Symbol database from header parser (NEW)
        self.symbol_db = symbol_db

        # SGI index → data offset mapping (built during analysis)
        self.sgi_to_offset: Dict[int, int] = {}

    def analyze(self) -> Dict[int, GlobalUsage]:
        """
        Analyzuje celou funkci a detekuje globální proměnné.

        Enhanced analysis includes:
        1. Usage pattern detection (arrays, counters, flags)
        2. SGI constant mapping (SC_sgi/SC_ggi calls)
        3. Type inference (int/float/char/pointer)
        4. Struct reconstruction (optional, via struct_inference)

        Returns:
            Dict mapující offset -> GlobalUsage
        """
        # Pattern 1: Analyzuj _init funkci pro inicializované globály
        self._analyze_init_function()

        # Pattern 2: Analyzuj všechny bloky pro GCP/GLD/DCP/DADR usage
        self._analyze_global_accesses()

        # Pattern 3: Detekuj array patterns
        self._detect_array_patterns()

        # NEW Pattern 4: Map SC_sgi/SC_ggi calls to globals
        self._map_globals_to_sgi_constants()

        # NEW Pattern 5: Infer types from instruction usage
        # FIX 4: Enable type inference for globals
        if self.aggressive_typing:
            self._infer_global_types()

        # NEW Pattern 6: Infer struct definitions from access patterns
        # NOTE: Temporarily disabled until struct_inference module is implemented
        # if self.infer_structs:
        #     self._infer_struct_definitions()

        # Pojmenuj globály podle patterns (SGI names override auto-generated)
        self._assign_names()

        return self.globals

    def _analyze_init_function(self):
        """
        Analyzuje _init funkci pro detekci globálních proměnných.

        Pattern: local_X se ukládá přes DCP do global segmentu
        Např: LCP local_0 → DCP offset → local_0 je inicializace globálky
        """
        # Najdi _init funkci (začíná na adrese 0)
        init_blocks = []
        for block_id, block in self.ssa_func.cfg.blocks.items():
            if block.start == 0:
                # Získej SSA instrukce pro tento blok
                ssa_instrs = self.ssa_func.instructions.get(block_id, [])
                init_blocks.append(ssa_instrs)

        # Procházej instrukce v _init
        for ssa_block in init_blocks:
            for i, instr in enumerate(ssa_block):
                # Hledej pattern: DCP (store to global)
                if instr.mnemonic == "DCP":
                    # Argumenty DCP: arg1 = DWORD offset, inputs[0] = hodnota
                    if instr.instruction and instr.instruction.instruction:
                        dword_offset = instr.instruction.instruction.arg1
                        byte_offset = dword_offset * 4
                        if byte_offset not in self.globals:
                            self.globals[byte_offset] = GlobalUsage(offset=byte_offset)
                        self.globals[byte_offset].write_count += 1
                        self.globals[byte_offset].functions_used.add("_init")

    def _analyze_global_accesses(self):
        """
        Analyzuje všechny bloky pro přístupy k globálům přes GCP/GLD/DCP/GADR/DADR.
        """
        for block_id, ssa_instrs in self.ssa_func.instructions.items():
            for instr in ssa_instrs:
                mnemonic = instr.mnemonic

                # GCP/GLD/GADR = read from global
                # NOTE: arg1 is DWORD offset, must convert to byte offset (* 4)
                if mnemonic in {"GCP", "GLD", "GADR"}:
                    if instr.instruction and instr.instruction.instruction:
                        dword_offset = instr.instruction.instruction.arg1
                        byte_offset = dword_offset * 4
                        if byte_offset not in self.globals:
                            self.globals[byte_offset] = GlobalUsage(offset=byte_offset)
                        self.globals[byte_offset].read_count += 1

                # DCP = write to global
                # NOTE: arg1 is DWORD offset, must convert to byte offset (* 4)
                elif mnemonic in {"DCP"}:
                    if instr.instruction and instr.instruction.instruction:
                        dword_offset = instr.instruction.instruction.arg1
                        byte_offset = dword_offset * 4
                        if byte_offset not in self.globals:
                            self.globals[byte_offset] = GlobalUsage(offset=byte_offset)
                        self.globals[byte_offset].write_count += 1

                # Detekuj operace na globálech
                elif mnemonic in {"ADD", "SUB", "INC", "DEC"}:
                    # Pokud vstup je z GCP/GLD, je to modifikace globálky
                    for inp in instr.inputs:
                        if inp.producer and hasattr(inp.producer, 'mnemonic'):
                            if inp.producer.mnemonic in {"GCP", "GLD"}:
                                if inp.producer.instruction and inp.producer.instruction.instruction:
                                    dword_offset = inp.producer.instruction.instruction.arg1
                                    byte_offset = dword_offset * 4
                                    if byte_offset in self.globals:
                                        if mnemonic in {"ADD", "INC"}:
                                            self.globals[byte_offset].is_incremented = True
                                        elif mnemonic in {"SUB", "DEC"}:
                                            self.globals[byte_offset].is_decremented = True

                elif mnemonic in {"EQU", "NEQU", "GRE", "LESS", "GREEQ", "LESSEQ",
                                   "UGRE", "ULESS", "UGEQ", "ULES"}:
                    # Detekuj porovnání globálů
                    for inp in instr.inputs:
                        if inp.producer and hasattr(inp.producer, 'mnemonic'):
                            if inp.producer.mnemonic in {"GCP", "GLD"}:
                                if inp.producer.instruction and inp.producer.instruction.instruction:
                                    dword_offset = inp.producer.instruction.instruction.arg1
                                    byte_offset = dword_offset * 4
                                    if byte_offset in self.globals:
                                        self.globals[byte_offset].is_compared = True

    def _detect_array_patterns(self):
        """
        Detekuje pattern globálních polí:
        - GADR offset + (index * element_size)
        - nebo ADD s násobením
        """
        for block_id, ssa_instrs in self.ssa_func.instructions.items():
            for i, instr in enumerate(ssa_instrs):
                # Hledej pattern: GADR base + MUL/ADD pro indexování
                if instr.mnemonic in {"ADD"}:
                    # Zkontroluj jestli jeden ze vstupů je GADR/DADR (base address)
                    # a druhý je násobek (index * size)
                    if len(instr.inputs) >= 2:
                        left = instr.inputs[0]
                        right = instr.inputs[1]

                        # Pattern: GADR/DADR + (index * size)
                        base_offset = None
                        multiplier = None

                        if left.producer and hasattr(left.producer, 'mnemonic'):
                            if left.producer.mnemonic in {"GADR", "DADR"}:
                                if left.producer.instruction and left.producer.instruction.instruction:
                                    # GADR arg1 is DWORD offset, convert to byte offset
                                    dword_offset = left.producer.instruction.instruction.arg1
                                    base_offset = dword_offset * 4

                        if right.producer and hasattr(right.producer, 'mnemonic'):
                            if right.producer.mnemonic == "MUL":
                                # Zkus extrahovat multiplier (element size)
                                if len(right.producer.inputs) >= 2:
                                    # Zkontroluj druhý operand MUL (měla by být konstanta)
                                    mul_right = right.producer.inputs[1]
                                    if mul_right.alias and mul_right.alias.startswith("data_"):
                                        try:
                                            offset_idx = int(mul_right.alias[5:])
                                            if self.scr and self.scr.data_segment:
                                                multiplier = self.scr.data_segment.get_dword(offset_idx * 4)
                                        except (ValueError, AttributeError):
                                            pass

                        # Pokud našli pattern, je to array access
                        if base_offset is not None and multiplier is not None:
                            if base_offset not in self.globals:
                                self.globals[base_offset] = GlobalUsage(offset=base_offset)
                            self.globals[base_offset].is_array_base = True
                            self.globals[base_offset].array_element_size = multiplier

        # NEW: Detect constant-offset arrays (e.g., gSideFrags[0], gSideFrags[1])
        # Pattern: Multiple accesses to consecutive offsets (offset, offset+4, offset+8)
        self._detect_constant_offset_arrays()

    def _detect_constant_offset_arrays(self):
        """
        Detect arrays accessed via constant offsets.

        Pattern: GADR base + GCP constant_offset + ADD
        Example:
            GADR 322  # &gSideFrags
            GCP 353   # 0
            ADD       # gSideFrags + 0
            DCP 4     # -> gSideFrags[0]

            GADR 322  # &gSideFrags
            GCP 355   # 4 (1 DWORD = 4 bytes)
            ADD       # gSideFrags + 4
            DCP 4     # -> gSideFrags[1]

        If we see consecutive byte offsets (N, N+4, N+8) being accessed from same base,
        mark base as is_array_base and elements as is_array_element.
        """
        from collections import defaultdict

        # Step 1: Group all potential array element accesses by base offset
        # Key: base_offset (DWORD), Value: list of byte offsets added to base
        base_to_byte_offsets = defaultdict(set)

        for block_id, ssa_instrs in self.ssa_func.instructions.items():
            i = 0
            while i < len(ssa_instrs):
                instr = ssa_instrs[i]

                # Look for pattern: GADR base_offset
                if instr.mnemonic == 'GADR' and instr.instruction:
                    base_dword_offset = instr.instruction.instruction.arg1
                    base_byte_offset = base_dword_offset * 4  # Convert to byte offset (globals dict uses byte offsets!)

                    # Check if next instruction is GCP (constant offset)
                    if i + 1 < len(ssa_instrs):
                        next_instr = ssa_instrs[i + 1]

                        # Pattern: GADR base + GCP offset + ADD
                        if next_instr.mnemonic == 'GCP' and next_instr.instruction:
                            # Get the constant value from data segment
                            const_dword_offset = next_instr.instruction.instruction.arg1

                            # Read constant value (byte offset)
                            if self.scr.data_segment and const_dword_offset < self.scr.data_segment.data_count:
                                byte_offset_bytes = self.scr.data_segment.raw_data[const_dword_offset * 4:(const_dword_offset + 1) * 4]
                                if len(byte_offset_bytes) == 4:
                                    import struct
                                    element_byte_offset = struct.unpack('<I', byte_offset_bytes)[0]

                                    # Check if followed by ADD (indicates offset calculation)
                                    if i + 2 < len(ssa_instrs):
                                        add_instr = ssa_instrs[i + 2]
                                        if add_instr.mnemonic == 'ADD':
                                            # Record this pattern: base + element_byte_offset
                                            # Use byte offset as key (consistent with rest of code)
                                            base_to_byte_offsets[base_byte_offset].add(element_byte_offset)

                i += 1

        # Step 2: Detect which bases have consecutive byte offsets (arrays)
        for base_byte_offset, element_byte_offsets in base_to_byte_offsets.items():
            if len(element_byte_offsets) < 2:
                continue  # Need at least 2 elements to be an array

            sorted_offsets = sorted(element_byte_offsets)

            # Check if offsets are consecutive multiples of 4 (int/float size)
            # Pattern: [0, 4, 8, ...] or [0, 4] or [4, 8, 12]
            consecutive_count = 1
            element_size = None

            for j in range(len(sorted_offsets) - 1):
                diff = sorted_offsets[j + 1] - sorted_offsets[j]

                if element_size is None:
                    element_size = diff

                if diff == element_size and element_size in [1, 2, 4, 8]:  # Valid element sizes
                    consecutive_count += 1
                else:
                    # Not consecutive, might be struct
                    break

            # If we found at least 2 consecutive elements, it's likely an array
            if consecutive_count >= 2 and element_size:
                # Mark base as array (using BYTE offset as key!)
                if base_byte_offset not in self.globals:
                    self.globals[base_byte_offset] = GlobalUsage(offset=base_byte_offset)

                self.globals[base_byte_offset].is_array_base = True
                self.globals[base_byte_offset].array_element_size = element_size

                # Mark individual byte offset accesses as array elements
                # Note: We don't create separate GlobalUsage entries for elements
                # They will be rendered as base[index] in expr.py

    def _map_globals_to_sgi_constants(self):
        """
        Map SC_sgi/SC_ggi calls to global variable offsets.

        Pattern:
            SC_sgi(500, value)  # Set global index 500
            SC_ggi(500)         # Get global index 500

        These indices correspond to SGI_ constants from headers.
        We track which data offset is used for each SGI index.
        """
        # Helper to get constant name from symbol_db
        def get_constant_name_for_value(value):
            if self.symbol_db:
                return self.symbol_db.get_constant_name(value)
            return None

        for block_id, ssa_instrs in self.ssa_func.instructions.items():
            for i, instr in enumerate(ssa_instrs):
                # Look for XCALL instructions
                if instr.mnemonic != 'XCALL':
                    continue

                if not instr.instruction or not instr.instruction.instruction:
                    continue

                xfn_index = instr.instruction.instruction.arg1
                if not self.scr.xfn_table:
                    continue

                # Get XFN entry
                xfn_entries = getattr(self.scr.xfn_table, 'entries', [])
                if xfn_index >= len(xfn_entries):
                    continue

                xfn_entry = xfn_entries[xfn_index]
                if not xfn_entry.name:
                    continue

                # Extract function name
                func_name = xfn_entry.name.split('(')[0] if '(' in xfn_entry.name else xfn_entry.name

                # Check if it's SC_sgi/SC_ggi/SC_sgf/SC_ggf
                if func_name not in ['SC_sgi', 'SC_ggi', 'SC_sgf', 'SC_ggf']:
                    continue

                # First argument is SGI index (should be a constant)
                if not instr.inputs or len(instr.inputs) < 1:
                    continue

                sgi_index_value = instr.inputs[0]

                # Try to extract constant value
                sgi_index = None
                if sgi_index_value.alias and sgi_index_value.alias.isdigit():
                    sgi_index = int(sgi_index_value.alias)
                elif sgi_index_value.producer_inst:
                    # Check if loaded from data segment
                    prod = sgi_index_value.producer_inst
                    if prod.mnemonic == 'GCP' and prod.instruction and prod.instruction.instruction:
                        data_offset = prod.instruction.instruction.arg1
                        byte_offset = data_offset * 4
                        if self.scr.data_segment:
                            sgi_index = self.scr.data_segment.get_dword(byte_offset)

                if sgi_index is None:
                    continue

                # Get SGI constant name from symbol_db
                sgi_name = get_constant_name_for_value(sgi_index)

                # For SC_sgi/SC_sgf, track which global offset is used
                if func_name in ['SC_sgi', 'SC_sgf']:
                    # Second argument is the value being stored
                    # The global slot corresponds to SGI index
                    # Map: SGI index → data segment offset
                    # (Assuming SC_GLOBAL_VARIABLE_MAX slots starting at offset 0)
                    estimated_offset = sgi_index * 4  # Each global is 4 bytes

                    if estimated_offset not in self.globals:
                        self.globals[estimated_offset] = GlobalUsage(offset=estimated_offset)

                    usage = self.globals[estimated_offset]
                    usage.sgi_index = sgi_index
                    usage.sgi_name = sgi_name
                    usage.write_count += 1

                # For SC_ggi/SC_ggf, also track
                elif func_name in ['SC_ggi', 'SC_ggf']:
                    estimated_offset = sgi_index * 4

                    if estimated_offset not in self.globals:
                        self.globals[estimated_offset] = GlobalUsage(offset=estimated_offset)

                    usage = self.globals[estimated_offset]
                    usage.sgi_index = sgi_index
                    usage.sgi_name = sgi_name
                    usage.read_count += 1

    def _infer_global_types(self):
        """
        Infer types for global variables using TypeInferenceEngine.

        Uses instruction patterns to aggressively infer types.
        Overrides existing type hints in aggressive mode.
        """
        # Lazy import to avoid circular dependency
        from .type_inference import TypeInferenceEngine

        # Create type inference engine
        if self.type_inference is None:
            self.type_inference = TypeInferenceEngine(self.ssa_func, aggressive=self.aggressive_typing)

        # Run two-pass type inference integration (Phase 7-01 enhancement)
        # This collects initial types from SSA values, runs dataflow propagation,
        # and writes refined types back to SSA values before we use them
        self.type_inference.integrate_with_ssa_values()

        # Get inferred types dictionary for global variable matching
        inferred_types = {name: info.final_type for name, info in self.type_inference.type_info.items() if info.final_type}

        # Match inferred types to global variables
        for block_id, ssa_instrs in self.ssa_func.instructions.items():
            for instr in ssa_instrs:
                # Look for GCP/GLD/GADR instructions (load global)
                if instr.mnemonic in ['GCP', 'GLD', 'GADR']:
                    if not instr.instruction or not instr.instruction.instruction:
                        continue

                    # GCP/GLD/GADR arg1 is DWORD offset, convert to byte offset
                    dword_offset = instr.instruction.instruction.arg1
                    byte_offset = dword_offset * 4

                    if byte_offset not in self.globals:
                        continue

                    # Get output SSA value
                    if not instr.outputs:
                        continue

                    output_value = instr.outputs[0]
                    if not output_value or not output_value.name:
                        continue

                    # Check if type was inferred for this value
                    inferred_type = inferred_types.get(output_value.name)
                    if not inferred_type:
                        continue

                    # FIX 4: Skip void* types from GCP/GLD/GADR outputs
                    # These instructions load ADDRESS of global, not the value itself
                    # So the output SSA value is a pointer, but the global is NOT a pointer
                    if inferred_type in ['void*', 'void *', 'ptr']:
                        continue

                    # Get confidence from type inference engine
                    type_info = self.type_inference.type_info.get(output_value.name)
                    confidence = 0.0
                    if type_info and type_info.evidence:
                        # Average confidence of all evidence
                        confidence = sum(ev.confidence for ev in type_info.evidence) / len(type_info.evidence)

                    # Update global usage with inferred type
                    usage = self.globals[byte_offset]

                    # In aggressive mode, always override
                    if self.aggressive_typing:
                        usage.inferred_type = inferred_type
                        usage.type_confidence = confidence
                    # In conservative mode, only set if not already set
                    elif not usage.inferred_type:
                        usage.inferred_type = inferred_type
                        usage.type_confidence = confidence

                    # FIX 4.3: Propagate type from array element to array base
                    # If this is an array element and we inferred its type,
                    # propagate the type to the base array
                    if usage.is_array_element and usage.array_base_offset is not None:
                        base_usage = self.globals.get(usage.array_base_offset)
                        if base_usage and not base_usage.inferred_type:
                            # Propagate type with slightly lower confidence
                            base_usage.inferred_type = inferred_type
                            base_usage.type_confidence = confidence * 0.9

    def _infer_struct_definitions(self):
        """
        Infer structure definitions from access patterns.

        Uses StructInferenceEngine to detect struct-like access patterns
        and generates typedef definitions.
        """
        # Lazy import to avoid circular dependency
        from .struct_inference import StructInferenceEngine

        # Create struct inference engine
        if self.struct_inference is None:
            self.struct_inference = StructInferenceEngine(self.ssa_func)

        # Analyze accesses
        self.struct_inference.analyze_accesses()

        # Infer struct definitions
        inferred_structs = self.struct_inference.infer_structs()

        # Update global usage with struct info
        for global_offset, inferred_struct in inferred_structs.items():
            if global_offset not in self.globals:
                self.globals[global_offset] = GlobalUsage(offset=global_offset)

            usage = self.globals[global_offset]
            usage.is_struct_base = True
            usage.inferred_struct = inferred_struct

            # Generate typedef
            struct_name = f"struct_{global_offset:04X}"
            if inferred_struct.possible_known_match:
                struct_name = inferred_struct.possible_known_match

            usage.struct_typedef = inferred_struct.to_typedef(struct_name)

            # If known match, update inferred type
            if inferred_struct.possible_known_match:
                usage.inferred_type = inferred_struct.possible_known_match
                usage.type_confidence = inferred_struct.confidence

    def _assign_names(self):
        """
        Přiřadí názvy globálním proměnným na základě detected patterns.

        Priority (highest first):
        0. SaveInfo names (from original source code .scr file)
        1. SGI constant names (from headers)
        2. Global pointer table indices (gGlobal0, gGlobal1, ...)
        3. Pattern-based names (arrays, counters, flags)
        4. Generic names (gVar0, gVar1, ...)
        """
        name_counters: Dict[str, int] = defaultdict(int)

        # PRIORITY 0: Build mapping from save_info section (HIGHEST PRIORITY)
        # save_info contains actual variable names from the original source code
        # Format: offset (dword), size (dwords), name
        sav_info_names = {}
        sav_info_ranges = []  # Track array/struct ranges to avoid naming elements
        if self.scr and self.scr.save_info:
            for item in self.scr.save_info.items:
                # val1 is the DWORD offset in the data segment
                dword_offset = item['val1']
                # val2 is the size in dwords
                size_dwords = item['val2']
                # Convert to byte offset for consistency with our tracking
                byte_offset = dword_offset * 4
                byte_size = size_dwords * 4
                var_name = item['name']

                # Save the range for arrays/structs (size > 1)
                if size_dwords > 1:
                    sav_info_ranges.append((byte_offset, byte_offset + byte_size, var_name))

                # Only assign name to the BASE offset, not individual elements
                sav_info_names[byte_offset] = var_name

                # Register as global if not already tracked
                if byte_offset not in self.globals:
                    self.globals[byte_offset] = GlobalUsage(offset=byte_offset)

        # Build reverse mapping: byte_offset → global_pointer_index
        gptr_offset_to_index = {}
        if self.scr and self.scr.global_pointers:
            for idx, byte_offset in enumerate(self.scr.global_pointers.offsets):
                # Global pointers table stores byte offsets, we use dword offsets
                dword_offset = byte_offset // 4
                gptr_offset_to_index[dword_offset] = idx

        for offset, usage in self.globals.items():
            # PRIORITY 0: SaveInfo names from original source (HIGHEST)
            if offset in sav_info_names:
                usage.name = sav_info_names[offset]
                continue

            # PRIORITY 1: SGI constant names
            if usage.sgi_name:
                usage.name = usage.sgi_name
                continue

            # Pokud už má název, přeskoč
            if usage.name:
                continue

            # PRIORITY 2: Global pointer table indices
            if offset in gptr_offset_to_index:
                gptr_idx = gptr_offset_to_index[offset]
                usage.name = f"gGlobal{gptr_idx}"
                continue

            # SKIP: Read-only data segment values (constants, literals)
            # If a value is never written to, it's a constant stored in data segment
            # Leave it unnamed so _render_value will show the literal value instead
            if usage.write_count == 0 and usage.read_count > 0:
                # This is a read-only constant - don't assign a name
                # Examples: TRUE, FALSE, numeric constants, string pointers
                continue

            # PRIORITY 3: Pattern-based names
            # Strategie pojmenování:
            base_name = "gVar"

            # 1. Array pattern
            if usage.is_array_base:
                if usage.array_element_size == 4:
                    base_name = "gArray"  # int array
                elif usage.array_element_size == 1:
                    base_name = "gBytes"  # byte array
                elif usage.array_element_size == 16:
                    base_name = "gStructs"  # struct array
                else:
                    base_name = "gArray"

            # 2. Counter pattern (incremented/decremented frequently)
            elif usage.is_incremented or usage.is_decremented:
                if usage.read_count > usage.write_count:
                    base_name = "gCount"
                else:
                    base_name = "gIndex"

            # 3. Flag pattern (pouze porovnávání)
            elif usage.is_compared and not (usage.is_incremented or usage.is_decremented):
                if usage.read_count > 5:
                    base_name = "gFlag"
                else:
                    base_name = "gState"

            # 4. Data pattern (více čtení než zápisů)
            elif usage.read_count > usage.write_count * 3:
                base_name = "gData"

            # Přidej číslo pokud už existuje
            count = name_counters[base_name]
            if count == 0:
                usage.name = base_name
            else:
                usage.name = f"{base_name}{count}"
            name_counters[base_name] = count + 1


def resolve_globals(ssa_func: SSAFunction, symbol_db=None) -> Dict[int, str]:
    """
    Hlavní entry point - analyzuje a pojmenovává globální proměnné.

    Args:
        ssa_func: SSA function to analyze
        symbol_db: Optional SymbolDatabase from header parser (KROK 1)

    Returns:
        Dict mapující data segment offset -> název globálky
    """
    resolver = GlobalResolver(ssa_func, symbol_db=symbol_db)
    globals_usage = resolver.analyze()

    # Vrať mapování offset -> název
    return {offset: usage.name for offset, usage in globals_usage.items() if usage.name}


def resolve_globals_with_types(ssa_func: SSAFunction, symbol_db=None) -> Dict[int, 'GlobalUsage']:
    """
    Rozšířený entry point - analyzuje globální proměnné a vrací kompletní type info.

    Args:
        ssa_func: SSA function to analyze
        symbol_db: Optional SymbolDatabase from header parser (KROK 1)

    Returns:
        Dict mapující data segment offset -> GlobalUsage (včetně inferred_type, confidence)
    """
    resolver = GlobalResolver(ssa_func, symbol_db=symbol_db)
    globals_usage = resolver.analyze()
    return globals_usage
