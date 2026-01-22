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

    # Name source tracking (07-03 enhancement)
    source: str = ""  # Source of name: "save_info", "SGI_constant", "SGI_runtime", "global_pointer_table", "synthetic", "read_only_constant"

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
    array_strides: Optional[List[int]] = None  # Stride constants for multi-dimensional arrays
    array_dimensions: Optional[List[int]] = None  # Dimension sizes for multi-dimensional arrays

    # SaveInfo metadata
    saveinfo_size_dwords: Optional[int] = None  # Size in dwords from save_info (if available)

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

    # NEW: Data segment initializer (string representation)
    initializer: Optional[str] = None


class GlobalResolver:
    """
    Resolver pro detekci a pojmenování globálních proměnných.

    Enhanced with:
    - Type inference from instruction patterns
    - SGI constant mapping from SC_sgi/SC_ggi calls
    - Struct reconstruction support
    """

    def __init__(self, ssa_func: SSAFunction, aggressive_typing: bool = False, infer_structs: bool = True, symbol_db=None):
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

        # Header database for function signature heuristics
        from ..headers.database import get_header_database
        self.header_db = get_header_database()

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

        # NEW Pattern 3b: Detect multi-dimensional array patterns
        self._detect_multidim_array_patterns()

        # NEW Pattern 4: Map SC_sgi/SC_ggi calls to globals
        self._map_globals_to_sgi_constants()

        # NEW Pattern 5: Infer types from instruction usage
        # Disabled by default: global typing is limited to header/SDK signatures.

        # NEW Pattern 6: Infer struct definitions from access patterns
        # NOTE: Temporarily disabled until struct_inference module is implemented
        # if self.infer_structs:
        #     self._infer_struct_definitions()

        # NEW Pattern 7: Infer struct types from XCALL arguments
        self._analyze_xcall_struct_args()

        # NEW Pattern 8: Header/SDK signature-based type hints from calls
        self._apply_call_type_hints()

        # NEW Pattern 9: Validate array element sizes against inferred types
        self._validate_array_element_sizes()

        # Pojmenuj globály podle patterns (SGI names override auto-generated)
        self._assign_names()

        # Finalize array dimension inference (requires SaveInfo size)
        self._finalize_array_dimensions()

        # Populate initializers from data segment (after types are inferred)
        self._apply_data_segment_initializers()

        # Propagate global types back to SSA values for reads/writes
        self._propagate_global_types_to_ssa()

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

    def _get_constant_value(self, value) -> Optional[int]:
        """Extract constant integer value from an SSAValue if possible."""
        if value is None:
            return None

        if hasattr(value, "constant_value") and value.constant_value is not None:
            return value.constant_value

        if value.alias and value.alias.isdigit():
            return int(value.alias)

        if value.alias and value.alias.startswith("data_"):
            try:
                offset_idx = int(value.alias[5:])
                if self.scr and self.scr.data_segment:
                    return self.scr.data_segment.get_dword(offset_idx * 4)
            except (ValueError, AttributeError):
                return None

        return None

    def _extract_stride_constants(self, value) -> List[int]:
        """
        Extract stride constants from a flattened index expression.

        Pattern: ADD(MUL(idx, stride), rest) where rest may contain another ADD/MUL chain.
        Returns stride constants in outer-to-inner order.
        """
        if not value or not value.producer_inst:
            return []

        inst = value.producer_inst
        if inst.mnemonic != "ADD" or len(inst.inputs) < 2:
            return []

        left, right = inst.inputs[0], inst.inputs[1]
        for candidate, remainder in ((left, right), (right, left)):
            if candidate.producer_inst and candidate.producer_inst.mnemonic in {"MUL", "IMUL"}:
                mul_inst = candidate.producer_inst
                if len(mul_inst.inputs) < 2:
                    continue
                stride = self._get_constant_value(mul_inst.inputs[1])
                if stride is None:
                    stride = self._get_constant_value(mul_inst.inputs[0])
                if stride is None:
                    continue
                return [stride] + self._extract_stride_constants(remainder)

        return []

    def _detect_multidim_array_patterns(self):
        """
        Detect multi-dimensional global array indexing patterns.

        Pattern: ADD(GADR base, MUL(flat_index, element_size))
        where flat_index is composed of nested ADD/MUL with stride constants.
        """
        for block_id, ssa_instrs in self.ssa_func.instructions.items():
            for instr in ssa_instrs:
                if instr.mnemonic != "ADD" or len(instr.inputs) < 2:
                    continue

                left, right = instr.inputs[0], instr.inputs[1]
                if not left.producer_inst or left.producer_inst.mnemonic != "GADR":
                    continue

                gadr_inst = left.producer_inst
                if not gadr_inst.instruction or not gadr_inst.instruction.instruction:
                    continue

                base_dword_offset = gadr_inst.instruction.instruction.arg1
                base_byte_offset = base_dword_offset * 4

                if not right.producer_inst or right.producer_inst.mnemonic not in {"MUL", "IMUL"}:
                    continue

                mul_inst = right.producer_inst
                if len(mul_inst.inputs) < 2:
                    continue

                element_size = self._get_constant_value(mul_inst.inputs[1])
                index_expr = mul_inst.inputs[0]
                if element_size is None:
                    element_size = self._get_constant_value(mul_inst.inputs[0])
                    index_expr = mul_inst.inputs[1]

                if not element_size:
                    continue

                stride_constants = self._extract_stride_constants(index_expr)
                if not stride_constants:
                    continue

                if base_byte_offset not in self.globals:
                    self.globals[base_byte_offset] = GlobalUsage(offset=base_byte_offset)

                usage = self.globals[base_byte_offset]
                usage.is_array_base = True
                usage.array_element_size = element_size
                usage.array_strides = stride_constants

    def _finalize_array_dimensions(self) -> None:
        """
        Finalize multi-dimensional array sizes using stride constants and SaveInfo sizes.
        """
        for usage in self.globals.values():
            if not usage.array_strides or not usage.array_element_size:
                continue

            all_strides = usage.array_strides + [usage.array_element_size]
            dims = []
            valid = True
            for i, stride in enumerate(usage.array_strides):
                denom = all_strides[i + 1]
                if denom <= 0 or stride % denom != 0:
                    valid = False
                    break
                dims.append(stride // denom)

            if not valid:
                continue

            # Use SaveInfo size to compute outer dimension if available
            if usage.saveinfo_size_dwords:
                total_elements = (usage.saveinfo_size_dwords * 4) // usage.array_element_size
                if total_elements:
                    product = 1
                    for dim in dims:
                        product *= dim
                    if product and total_elements % product == 0:
                        outer_dim = total_elements // product
                        dims = [outer_dim] + dims

            if len(dims) >= 2:
                usage.array_dimensions = dims

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

    def _analyze_xcall_struct_args(self):
        """
        Analyze XCALL arguments to infer struct types for global arrays.

        When a global array element is passed to a function expecting a typed pointer
        (e.g., SC_IsNear3D expects c_Vector3*), infer the global's element type.

        Pattern detected:
            GADR data[X] + (index * size) → passed to XCALL arg expecting struct*
        """
        from ..headers.database import get_header_database

        header_db = get_header_database()

        for block_id, ssa_instrs in self.ssa_func.instructions.items():
            for instr in ssa_instrs:
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

                # Get struct parameter mapping for this function from headers/SDK signatures
                param_map = {}
                header_sig = header_db.get_function_signature(func_name) if header_db else None
                if header_sig and header_sig.get("parameters"):
                    for idx, param in enumerate(header_sig["parameters"]):
                        if not param or len(param) < 1:
                            continue
                        param_type = param[0].strip()
                        if param_type.endswith("*"):
                            base_type = param_type.replace("*", "").strip()
                            if base_type.startswith(("s_SC_", "s_", "c_")):
                                param_map[idx] = base_type
                if not param_map:
                    continue

                # Check each argument
                for arg_idx, expected_type in param_map.items():
                    if arg_idx >= len(instr.inputs):
                        continue

                    arg_value = instr.inputs[arg_idx]

                    # Look for pattern: ADD(GADR, MUL(...)) - global array element address
                    if not arg_value.producer_inst:
                        continue

                    prod = arg_value.producer_inst
                    if prod.mnemonic != 'ADD' or len(prod.inputs) < 2:
                        continue

                    left = prod.inputs[0]
                    right = prod.inputs[1]

                    # Check if left is GADR (global address)
                    if not left.producer_inst or left.producer_inst.mnemonic != 'GADR':
                        continue

                    # Get global offset from GADR
                    gadr_inst = left.producer_inst
                    if not gadr_inst.instruction or not gadr_inst.instruction.instruction:
                        continue

                    dword_offset = gadr_inst.instruction.instruction.arg1
                    byte_offset = dword_offset * 4

                    # Check if right is MUL (index * element_size)
                    element_size = None
                    if right.producer_inst and right.producer_inst.mnemonic == 'MUL':
                        mul_inst = right.producer_inst
                        if len(mul_inst.inputs) >= 2:
                            size_input = mul_inst.inputs[1]
                            # Try to get constant size
                            if size_input.alias and size_input.alias.startswith("data_"):
                                try:
                                    size_offset = int(size_input.alias[5:])
                                    if self.scr.data_segment:
                                        element_size = self.scr.data_segment.get_dword(size_offset * 4)
                                except (ValueError, AttributeError):
                                    pass

                    # Update global usage with inferred struct type
                    if byte_offset not in self.globals:
                        self.globals[byte_offset] = GlobalUsage(offset=byte_offset)

                    usage = self.globals[byte_offset]

                    # Set the array element type based on function parameter expectation
                    if expected_type:
                        self._apply_header_type_hint(usage, expected_type, 0.9)
                        usage.is_array_base = True
                        if element_size:
                            usage.array_element_size = element_size

    def _infer_global_types(self):
        """
        Infer types for global variables using TypeInferenceEngine.

        Uses instruction patterns to aggressively infer types.
        Overrides existing type hints in aggressive mode.

        CRITICAL FIX (07-03): Added validation logging for DWORD-to-BYTE conversion
        and assertions for alignment checks.
        """
        import logging
        logger = logging.getLogger(__name__)

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
                # Look for GCP/GLD/GADR/GST instructions (global access)
                if instr.mnemonic in ['GCP', 'GLD', 'GADR', 'GST']:
                    if not instr.instruction or not instr.instruction.instruction:
                        continue

                    # CRITICAL: GADR/GCP arg1 is DWORD offset, globals dict uses BYTE offset
                    dword_offset = instr.instruction.instruction.arg1
                    byte_offset = dword_offset * 4

                    # Validation logging for offset conversion
                    logger.debug(f"Global access: opcode={instr.mnemonic}, dword_offset={dword_offset}, byte_offset={byte_offset}")

                    # Alignment assertion - global byte offset must be 4-byte aligned
                    assert byte_offset % 4 == 0, f"Global byte offset {byte_offset} must be 4-byte aligned (dword_offset={dword_offset})"

                    if byte_offset not in self.globals:
                        continue

                    # Get output SSA value (for load operations GCP/GLD/GADR)
                    # For GST (store), we'd need to look at input values instead
                    if instr.mnemonic in ['GCP', 'GLD', 'GADR']:
                        if not instr.outputs:
                            continue

                        output_value = instr.outputs[0]
                        if not output_value or not output_value.name:
                            continue

                        # Check if type was inferred for this value
                        inferred_type = inferred_types.get(output_value.name)
                        if not inferred_type:
                            continue

                        # FIX 4: Skip void* types only for GADR outputs (address of global)
                        if instr.mnemonic == 'GADR' and inferred_type in ['void*', 'void *', 'ptr']:
                            continue

                        # Get confidence from type inference engine
                        type_info = self.type_inference.type_info.get(output_value.name)
                        confidence = 0.0
                        if type_info and type_info.evidence:
                            # Average confidence of all evidence
                            confidence = sum(ev.confidence for ev in type_info.evidence) / len(type_info.evidence)

                        # Update global usage with inferred type
                        usage = self.globals[byte_offset]

                        # Only update type if:
                        # 1. No type set yet, OR
                        # 2. New type has higher confidence (aggressive mode), OR
                        # 3. Types are same (update confidence)
                        should_update = (
                            not usage.inferred_type or
                            confidence > usage.type_confidence or
                            inferred_type == usage.inferred_type
                        )

                        if should_update:
                            usage.inferred_type = inferred_type
                            usage.type_confidence = max(confidence, usage.type_confidence)
                            logger.debug(f"Global {byte_offset}: type={inferred_type} (confidence={usage.type_confidence:.2f})")

                        # FIX 4.3: Propagate type from array element to array base
                        # Only propagate when the type is confirmed from headers/SDK.
                        if usage.is_array_element and usage.array_base_offset is not None and usage.header_type:
                            base_usage = self.globals.get(usage.array_base_offset)
                            if base_usage and not base_usage.inferred_type:
                                # Propagate type with slightly lower confidence
                                base_usage.inferred_type = inferred_type
                                base_usage.type_confidence = confidence * 0.9

                    elif instr.mnemonic == 'GST':
                        # For store operations, infer type from input value
                        if not instr.inputs:
                            continue

                        input_value = instr.inputs[0]
                        if not input_value or not input_value.name:
                            continue

                        inferred_type = inferred_types.get(input_value.name)
                        if not inferred_type:
                            continue

                        # Get confidence
                        type_info = self.type_inference.type_info.get(input_value.name)
                        confidence = 0.0
                        if type_info and type_info.evidence:
                            confidence = sum(ev.confidence for ev in type_info.evidence) / len(type_info.evidence)

                        usage = self.globals[byte_offset]

                        # Only update type if confidence is higher
                        should_update = (
                            not usage.inferred_type or
                            confidence > usage.type_confidence or
                            inferred_type == usage.inferred_type
                        )

                        if should_update:
                            usage.inferred_type = inferred_type
                            usage.type_confidence = max(confidence, usage.type_confidence)
                            logger.debug(f"Global {byte_offset}: type={inferred_type} from GST (confidence={usage.type_confidence:.2f})")

                # ASGN stores value to address - infer global type from stored value
                if instr.mnemonic == 'ASGN':
                    # Pattern: FADD/FSUB/... → GADR global_offset → ASGN
                    # The ASGN stores typed value to global
                    if len(instr.inputs) < 2:
                        continue

                    # Check if target is a global address (from GADR)
                    target_value = instr.inputs[1] if len(instr.inputs) > 1 else instr.inputs[0]
                    source_value = instr.inputs[0] if len(instr.inputs) > 1 else None

                    if not target_value or not source_value:
                        continue

                    # Check if target is from GADR (global address)
                    if target_value.producer_inst and target_value.producer_inst.mnemonic == 'GADR':
                        gadr_inst = target_value.producer_inst
                        if gadr_inst.instruction and gadr_inst.instruction.instruction:
                            dword_offset = gadr_inst.instruction.instruction.arg1
                            global_byte_offset = dword_offset * 4

                            if global_byte_offset not in self.globals:
                                continue

                            # Check if source has inferred type
                            inferred_type = inferred_types.get(source_value.name)
                            if not inferred_type:
                                # Check source's producer instruction for float ops
                                if source_value.producer_inst:
                                    src_mnemonic = source_value.producer_inst.mnemonic
                                    if src_mnemonic in {'FADD', 'FSUB', 'FMUL', 'FDIV', 'FNEG', 'frnd', 'ITOF'}:
                                        inferred_type = 'float'
                                    elif src_mnemonic in {'IADD', 'ISUB', 'IMUL', 'IDIV'}:
                                        inferred_type = 'int'

                            if not inferred_type:
                                continue

                            # Get confidence
                            type_info = self.type_inference.type_info.get(source_value.name)
                            confidence = 0.9  # High confidence for ASGN pattern
                            if type_info and type_info.evidence:
                                confidence = sum(ev.confidence for ev in type_info.evidence) / len(type_info.evidence)

                            usage = self.globals[global_byte_offset]

                            # Only update type if confidence is higher
                            should_update = (
                                not usage.inferred_type or
                                confidence > usage.type_confidence or
                                inferred_type == usage.inferred_type
                            )

                            if should_update:
                                usage.inferred_type = inferred_type
                                usage.type_confidence = max(confidence, usage.type_confidence)
                                logger.debug(f"Global {global_byte_offset}: type={inferred_type} from ASGN (confidence={usage.type_confidence:.2f})")

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

    def _resolve_sgi_constants(self):
        """
        Resolve SGI constants from header database.

        Maps global variable offsets to SGI constant names from headers.
        SGI constants are game engine globals defined in sc_def.h.

        Returns:
            Dict[int, str] - mapping byte_offset -> SGI constant name
        """
        import logging
        logger = logging.getLogger(__name__)

        sgi_mapping = {}

        # Get header database
        from ..headers.database import get_header_database
        header_db = get_header_database()

        # Get all SGI/SGF/GVAR constants
        sgi_constants = header_db.get_constants_by_prefix('SGI')
        sgf_constants = header_db.get_constants_by_prefix('SGF')
        gvar_constants = header_db.get_constants_by_prefix('GVAR')

        all_constants = {}
        all_constants.update(sgi_constants)
        all_constants.update(sgf_constants)
        all_constants.update(gvar_constants)

        if not all_constants:
            logger.debug("No SGI/SGF/GVAR constants found in header database")
            return sgi_mapping

        # Build mapping from SGI index to constant name
        # SGI constants are defined like: #define SGI_MISSIONDEATHCOUNT 1
        for const_name, const_data in all_constants.items():
            value_str = const_data.get('value', '')
            try:
                # Parse SGI index
                if value_str.startswith('0x'):
                    sgi_index = int(value_str, 16)
                else:
                    sgi_index = int(value_str)

                # SGI index maps to byte offset (each global is 4 bytes)
                # NOTE: This assumes SGI constants are sequential starting at offset 0
                # The actual mapping might be different based on engine implementation
                byte_offset = sgi_index * 4

                # Only map if this offset exists in our globals
                if byte_offset in self.globals:
                    sgi_mapping[byte_offset] = const_name
                    logger.debug(f"SGI mapping: offset {byte_offset} -> {const_name} (index {sgi_index})")

            except (ValueError, TypeError):
                # Skip non-integer constants
                logger.debug(f"Skipping non-integer SGI constant: {const_name} = {value_str}")
                continue

        return sgi_mapping

    def _assign_names(self):
        """
        Přiřadí názvy globálním proměnným na základě detected patterns.

        Priority (highest first):
        0. SaveInfo names (from original source code .scr file)
        1. SGI constant names (from headers)
        2. Global pointer table indices (gGlobal0, gGlobal1, ...)
        3. Pattern-based names (arrays, counters, flags)
        4. Generic names (gVar0, gVar1, ...)

        ENHANCEMENT (07-03): Added comprehensive save_info and SGI constant integration
        with source tracking for debugging.
        """
        import logging
        logger = logging.getLogger(__name__)

        name_counters: Dict[str, int] = defaultdict(int)

        # PRIORITY 1 PRE-PROCESSING: Build SGI constant mapping from headers
        sgi_constant_names = self._resolve_sgi_constants()

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

                self.globals[byte_offset].saveinfo_size_dwords = size_dwords

                logger.info(f"Global {byte_offset}: name from save_info: {var_name}")

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
                usage.source = "save_info"
                logger.debug(f"Global {offset}: assigned name '{usage.name}' from save_info")
                continue

            # PRIORITY 1: SGI constant names from headers
            if offset in sgi_constant_names:
                usage.name = sgi_constant_names[offset]
                usage.source = "SGI_constant"
                logger.info(f"Global {offset}: assigned name '{usage.name}' from SGI constant")
                continue

            # PRIORITY 1b: SGI names from runtime detection (SC_sgi/SC_ggi calls)
            if usage.sgi_name:
                usage.name = usage.sgi_name
                usage.source = "SGI_runtime"
                logger.info(f"Global {offset}: assigned name '{usage.name}' from runtime SGI detection")
                continue

            # Pokud už má název, přeskoč
            if usage.name:
                continue

            # PRIORITY 2: Global pointer table indices
            if offset in gptr_offset_to_index:
                gptr_idx = gptr_offset_to_index[offset]
                usage.name = f"gGlobal{gptr_idx}"
                usage.source = "global_pointer_table"
                logger.debug(f"Global {offset}: assigned name '{usage.name}' from global pointer table")
                continue

            # SKIP: Read-only data segment values (constants, literals)
            # If a value is never written to, it's a constant stored in data segment
            # Leave it unnamed so _render_value will show the literal value instead
            if usage.write_count == 0 and usage.read_count > 0:
                # This is a read-only constant - don't assign a name
                # Examples: TRUE, FALSE, numeric constants, string pointers
                usage.source = "read_only_constant"
                logger.debug(f"Global {offset}: skipped naming (read-only constant)")
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
            usage.source = "synthetic"
            logger.debug(f"Global {offset}: assigned synthetic name '{usage.name}'")

    def _apply_struct_size_hints(self) -> None:
        """
        Apply struct type hints based on element size and name heuristics.

        Uses known struct sizes from headers/SDK to avoid emitting generic dword.
        """
        from ..structures import get_struct_by_size

        name_hints = {
            "recover": "s_SC_MP_Recover",
            "rec": "s_SC_MP_Recover",
            "sphere": "s_sphere",
            "vec": "c_Vector3",
            "vector": "c_Vector3",
        }

        for usage in self.globals.values():
            if usage.inferred_type or not usage.array_element_size:
                continue

            candidates = get_struct_by_size(usage.array_element_size)
            if not candidates:
                continue

            if len(candidates) == 1:
                usage.inferred_type = candidates[0].name
                usage.type_confidence = max(usage.type_confidence, 0.6)
                continue

            if usage.name:
                name_lower = usage.name.lower()
                for hint, struct_name in name_hints.items():
                    if hint in name_lower:
                        for candidate in candidates:
                            if candidate.name == struct_name:
                                usage.inferred_type = candidate.name
                                usage.type_confidence = max(usage.type_confidence, 0.6)
                                break
                        if usage.inferred_type:
                            break

    def _apply_call_type_hints(self) -> None:
        """
        Apply heuristics for BOOL and c_Vector3 globals based on function call usage.
        """
        for block_id, instructions in self.ssa_func.instructions.items():
            for inst in instructions:
                if inst.mnemonic != "XCALL":
                    continue
                if not inst.instruction or not inst.instruction.instruction:
                    continue

                xfn_index = inst.instruction.instruction.arg1
                xfn_entry = self.ssa_func.scr.get_xfn(xfn_index) if self.ssa_func.scr else None
                if not xfn_entry or not xfn_entry.name:
                    continue

                func_name = xfn_entry.name.split("(")[0]
                params = []
                return_type = None
                func_sig = self.header_db.get_function_signature(func_name) if self.header_db else None
                if func_sig:
                    params = func_sig.get("parameters") or []
                    return_type = func_sig.get("return_type")
                else:
                    continue

                for idx, value in enumerate(inst.inputs):
                    if not value:
                        continue

                    param_type = None
                    if idx < len(params):
                        param_type = params[idx][0]

                    if param_type not in {
                        "BOOL",
                        "c_Vector3",
                        "c_Vector3 *",
                        "c_Vector3*",
                        "c_vector3",
                        "c_vector3 *",
                        "c_vector3*",
                    }:
                        continue

                    global_usage, is_array_access, element_size = self._get_global_usage_from_value(value)
                    if not global_usage:
                        continue

                    if param_type == "BOOL":
                        self._apply_header_type_hint(global_usage, "BOOL", 0.9)
                        self._apply_bool_usage(global_usage, is_array_access, element_size)
                    else:
                        self._apply_header_type_hint(global_usage, "c_Vector3", 0.85)
                        global_usage.is_struct_base = True
                        if is_array_access:
                            global_usage.is_array_base = True
                        global_usage.array_element_size = global_usage.array_element_size or element_size or 12

                if return_type == "BOOL":
                    for out_val in inst.outputs or []:
                        global_usage, is_array_access, element_size = self._get_global_usage_from_value(out_val)
                        if global_usage:
                            self._apply_header_type_hint(global_usage, "BOOL", 0.9)
                            self._apply_bool_usage(global_usage, is_array_access, element_size)

    def _apply_header_type_hint(self, usage: GlobalUsage, inferred_type: str, confidence: float) -> None:
        usage.header_type = inferred_type
        self._update_usage_type(usage, inferred_type, confidence)

    def _update_usage_type(self, usage: GlobalUsage, inferred_type: str, confidence: float) -> None:
        if not usage.inferred_type or confidence >= usage.type_confidence:
            usage.inferred_type = inferred_type
            usage.type_confidence = max(usage.type_confidence, confidence)

    def _apply_bool_usage(
        self,
        usage: GlobalUsage,
        is_array_access: bool,
        element_size: Optional[int],
    ) -> None:
        self._update_usage_type(usage, "BOOL", 0.9)
        if is_array_access or (usage.saveinfo_size_dwords and usage.saveinfo_size_dwords > 1) or usage.array_dimensions:
            usage.is_array_base = True
            usage.array_element_size = usage.array_element_size or element_size or 4

    def _get_global_usage_from_value(self, value) -> Tuple[Optional[GlobalUsage], bool, Optional[int]]:
        if not value:
            return None, False, None

        if value.alias:
            alias = value.alias
            if alias.startswith("&"):
                alias = alias[1:]
            if alias.startswith("data_"):
                try:
                    dword_offset = int(alias[5:])
                except ValueError:
                    return None, False, None
                byte_offset = dword_offset * 4
                return self.globals.get(byte_offset), False, None

        if not value.producer_inst:
            return None, False, None

        producer = value.producer_inst
        if producer.mnemonic in {"GCP", "GLD", "GADR"}:
            if producer.instruction and producer.instruction.instruction:
                dword_offset = producer.instruction.instruction.arg1
                byte_offset = dword_offset * 4
                return self.globals.get(byte_offset), False, None
            return None, False, None

        if producer.mnemonic == "ADD" and len(producer.inputs) >= 2:
            left, right = producer.inputs[0], producer.inputs[1]
            base_inst = None
            offset_val = None
            if left.producer_inst and left.producer_inst.mnemonic == "GADR":
                base_inst = left.producer_inst
                offset_val = right
            elif right.producer_inst and right.producer_inst.mnemonic == "GADR":
                base_inst = right.producer_inst
                offset_val = left

            if base_inst and base_inst.instruction and base_inst.instruction.instruction:
                dword_offset = base_inst.instruction.instruction.arg1
                byte_offset = dword_offset * 4
                element_size = None
                if offset_val and offset_val.producer_inst and offset_val.producer_inst.mnemonic in {"MUL", "IMUL"}:
                    mul_inst = offset_val.producer_inst
                    if len(mul_inst.inputs) >= 2:
                        element_size = self._get_constant_value(mul_inst.inputs[1])
                        if element_size is None:
                            element_size = self._get_constant_value(mul_inst.inputs[0])
                return self.globals.get(byte_offset), True, element_size

        return None, False, None

    def _get_type_size(self, type_name: Optional[str]) -> Optional[int]:
        if not type_name:
            return None

        base_type = type_name.replace("*", "").strip()
        if base_type in {"c_Vector3", "c_vector3"}:
            return 12

        from ..structures import get_struct_by_name

        struct_def = get_struct_by_name(base_type)
        if struct_def:
            return struct_def.size

        type_sizes = {
            "char": 1,
            "short": 2,
            "int": 4,
            "float": 4,
            "double": 8,
            "dword": 4,
            "BOOL": 4,
        }
        return type_sizes.get(base_type)

    def _validate_array_element_sizes(self) -> None:
        """
        Ensure array base globals have an element size consistent with inferred types.
        """
        for usage in self.globals.values():
            if not usage.is_array_base:
                continue

            expected_size = self._get_type_size(usage.inferred_type or usage.header_type)
            if not expected_size:
                continue

            if usage.array_element_size is None:
                usage.array_element_size = expected_size
                continue

            if usage.array_element_size == expected_size:
                continue

            if usage.saveinfo_size_dwords:
                total_bytes = usage.saveinfo_size_dwords * 4
                if total_bytes % expected_size == 0:
                    usage.array_element_size = expected_size
                    continue

            if expected_size and (usage.array_element_size <= 4 or usage.array_element_size > expected_size):
                usage.array_element_size = expected_size

    def _apply_condition_type_hints(self) -> None:
        """
        Infer BOOL globals when used in conditional jumps.
        """
        condition_ops = {"JZ", "JNZ"}
        compare_ops = {"EQU", "NEQU", "GRE", "LESS", "GREEQ", "LESSEQ", "UGRE", "ULESS", "UGEQ", "ULES"}

        for block_id, instructions in self.ssa_func.instructions.items():
            for inst in instructions:
                if inst.mnemonic not in condition_ops:
                    continue

                for value in inst.inputs:
                    if not value:
                        continue

                    usage, is_array_access, element_size = self._get_global_usage_from_value(value)
                    if usage:
                        self._apply_bool_usage(usage, is_array_access, element_size)
                        continue

                    if not value.producer_inst or value.producer_inst.mnemonic not in compare_ops:
                        continue

                    for compare_input in value.producer_inst.inputs:
                        usage, is_array_access, element_size = self._get_global_usage_from_value(compare_input)
                        if usage:
                            self._apply_bool_usage(usage, is_array_access, element_size)

    def _apply_data_segment_initializers(self) -> None:
        if not self.scr or not self.scr.data_segment:
            return

        data_segment = self.scr.data_segment
        from .data_resolver import DataResolver
        from ...parsing.data_segment_initializers import build_initializer
        from ..structures import get_struct_by_name

        type_info_dwords = {offset // 4: usage for offset, usage in self.globals.items()}
        data_resolver = DataResolver(data_segment, type_info_dwords, confidence_threshold=0.70)

        for byte_offset, usage in self.globals.items():
            if usage.initializer:
                continue
            if byte_offset >= len(data_segment.raw_data):
                continue

            element_type = usage.inferred_type or "dword"
            element_size = usage.array_element_size

            struct_def = get_struct_by_name(element_type)
            if struct_def and not element_size:
                element_size = struct_def.size

            if element_type in {"c_Vector3", "c_vector3"}:
                element_size = element_size or 12
            elif element_size is None:
                type_sizes = {
                    "char": 1,
                    "short": 2,
                    "int": 4,
                    "float": 4,
                    "double": 8,
                    "dword": 4,
                    "BOOL": 4,
                }
                element_size = type_sizes.get(element_type, 4)

            if element_type in {"int", "float", "dword", "BOOL"}:
                element_size = 4

            element_count = 1
            if usage.saveinfo_size_dwords:
                total_bytes = usage.saveinfo_size_dwords * 4
                if element_size and element_size > 0 and total_bytes % element_size == 0:
                    element_count = total_bytes // element_size
            elif usage.array_dimensions:
                element_count = 1
                for dim in usage.array_dimensions:
                    element_count *= dim
            elif usage.is_array_base:
                continue

            initializer = build_initializer(
                data_segment,
                data_resolver,
                byte_offset=byte_offset,
                element_type=element_type,
                element_size=element_size,
                element_count=element_count,
            )

            if not initializer and element_count > 1 and element_size:
                total_bytes = element_size * element_count
                if byte_offset + total_bytes <= len(data_segment.raw_data):
                    block = data_segment.raw_data[byte_offset:byte_offset + total_bytes]
                    if block and all(b == 0 for b in block):
                        candidate_offset = byte_offset + total_bytes
                        candidate_usage = self.globals.get(candidate_offset)
                        if not candidate_usage or (
                            not candidate_usage.name
                            and not candidate_usage.saveinfo_size_dwords
                            and candidate_usage.write_count == 0
                        ):
                            initializer = build_initializer(
                                data_segment,
                                data_resolver,
                                byte_offset=candidate_offset,
                                element_type=element_type,
                                element_size=element_size,
                                element_count=element_count,
                            )

            if initializer:
                usage.initializer = initializer

    def _propagate_global_types_to_ssa(self) -> None:
        """
        Propagate inferred global types back into SSA values for read/write operations.
        """
        if not self.type_inference:
            return

        from .type_inference import TypeEvidence, TypeSource

        for block_id, ssa_instrs in self.ssa_func.instructions.items():
            for instr in ssa_instrs:
                if instr.mnemonic in {"GCP", "GLD", "GADR"}:
                    if not instr.instruction or not instr.instruction.instruction:
                        continue
                    dword_offset = instr.instruction.instruction.arg1
                    byte_offset = dword_offset * 4
                    usage = self.globals.get(byte_offset)
                    if not usage or not usage.inferred_type:
                        continue

                    if not instr.outputs:
                        continue

                    inferred_type = usage.inferred_type
                    if instr.mnemonic == "GADR" and not inferred_type.endswith("*"):
                        inferred_type = f"{inferred_type} *"

                    for out_val in instr.outputs:
                        if not out_val or not out_val.name:
                            continue
                        info = self.type_inference._get_or_create_type_info(out_val.name)
                        info.add_evidence(TypeEvidence(
                            confidence=max(usage.type_confidence, 0.8),
                            source=TypeSource.ASSIGNMENT,
                            inferred_type=inferred_type,
                            reason=f"Loaded from global {usage.name or byte_offset}"
                        ))

                if instr.mnemonic == "ASGN" and len(instr.inputs) >= 2:
                    target_value = instr.inputs[1]
                    source_value = instr.inputs[0]
                    if not target_value or not source_value:
                        continue
                    if not target_value.producer_inst or target_value.producer_inst.mnemonic != "GADR":
                        continue
                    gadr_inst = target_value.producer_inst
                    if not gadr_inst.instruction or not gadr_inst.instruction.instruction:
                        continue
                    dword_offset = gadr_inst.instruction.instruction.arg1
                    byte_offset = dword_offset * 4
                    usage = self.globals.get(byte_offset)
                    if not usage or not usage.inferred_type:
                        continue

                    if source_value.name:
                        info = self.type_inference._get_or_create_type_info(source_value.name)
                        info.add_evidence(TypeEvidence(
                            confidence=max(usage.type_confidence, 0.8),
                            source=TypeSource.ASSIGNMENT,
                            inferred_type=usage.inferred_type,
                            reason=f"Stored to global {usage.name or byte_offset}"
                        ))

        inferred_types = self.type_inference._resolve_all_types()
        self.type_inference._update_ssa_value_types(inferred_types)


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
