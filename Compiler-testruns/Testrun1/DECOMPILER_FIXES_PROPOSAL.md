# Návrh oprav dekompilátoru VC-Script
**Datum:** 2026-01-02
**Založeno na:** Analýza TDM.SCR dekompilace

---

## PRIORITY OPRAV

### P0 - KRITICKÉ (Implementovat IHNED)

---

## P0.1 - Data Segment → Global Variables Reconstruction

### Problém
Dekompilovaný kód neobsahuje žádné globální proměnné, ačkoliv originál má 10+ globálů.

### Současný stav
```c
// tdm_CURRENT_OUTPUT.c - CHYBÍ VŠECHNY GLOBÁLY!
#include <inc\sc_global.h>
#include <inc\sc_def.h>

int _init(s_SC_NET_info *info) {
    // ...
}
```

### Očekávaný výstup
```c
#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables from data segment
dword gRecs;
s_SC_MP_Recover gRec[64];
float gRecTimer[64];
float gNextRecover;
int gSideFrags[2];
int gCLN_SideFrags[2];
dword gEndRule;
dword gEndValue;
float gTime;
dword gPlayersConnected;
```

### Implementační kroky

**1. Rozšířit SCR loader o data segment parsing**

Soubor: `vcdecomp/core/loader.py`

```python
class SCRFile:
    def __init__(self, path):
        # ... existing code ...
        self.data_segment = []
        self.global_ptrs = []

    def parse_data_segment(self, data, offset, size):
        """Parse data segment and extract constants."""
        self.data_segment = []
        pos = offset

        while pos < offset + size:
            # Try to identify data type
            value_bytes = data[pos:pos+4]

            # Check if it's a string
            if self._is_string_start(data, pos):
                string_val, string_len = self._extract_string(data, pos)
                self.data_segment.append({
                    'offset': pos,
                    'type': 'string',
                    'value': string_val,
                    'size': string_len
                })
                pos += string_len
                # Align to 4 bytes
                pos = (pos + 3) & ~3
            else:
                # Try int/float
                int_val = struct.unpack('<i', value_bytes)[0]
                float_val = struct.unpack('<f', value_bytes)[0]

                self.data_segment.append({
                    'offset': pos,
                    'type': 'dword',  # Will be refined later
                    'int_value': int_val,
                    'float_value': float_val,
                    'size': 4
                })
                pos += 4

    def parse_global_pointers(self, data, offset, count):
        """Parse global pointer table."""
        self.global_ptrs = []
        for i in range(count):
            ptr_offset = offset + i * 4
            ptr_value = struct.unpack('<I', data[ptr_offset:ptr_offset+4])[0]
            self.global_ptrs.append({
                'index': i,
                'data_offset': ptr_value
            })
```

**2. Type inference z usage patterns**

Soubor: `vcdecomp/core/analysis/global_analyzer.py` (NOVÝ)

```python
class GlobalVariableAnalyzer:
    """Analyzes instruction patterns to infer global variable types."""

    def __init__(self, scr_file, instructions):
        self.scr = scr_file
        self.instructions = instructions
        self.globals = {}  # offset -> GlobalVar

    def analyze(self):
        """Main analysis entry point."""
        # Step 1: Collect all GLD/GCP/GST references
        global_accesses = self._collect_global_accesses()

        # Step 2: Infer types from instruction usage
        for offset, accesses in global_accesses.items():
            var_type = self._infer_type(offset, accesses)
            is_array, array_size = self._detect_array(offset, accesses)

            self.globals[offset] = GlobalVariable(
                offset=offset,
                type=var_type,
                is_array=is_array,
                array_size=array_size,
                name=self._generate_name(offset, var_type)
            )

        return self.globals

    def _collect_global_accesses(self):
        """Find all instructions that access globals."""
        accesses = {}  # offset -> list of (instr, context)

        for instr in self.instructions:
            if instr.mnemonic == 'GLD':  # Global load
                offset = instr.arg1
                if offset not in accesses:
                    accesses[offset] = []
                accesses[offset].append(('load', instr))

            elif instr.mnemonic == 'GCP':  # Global copy pointer
                offset = instr.arg1
                if offset not in accesses:
                    accesses[offset] = []
                accesses[offset].append(('address', instr))

            elif instr.mnemonic == 'GST':  # Global store
                offset = instr.arg1
                if offset not in accesses:
                    accesses[offset] = []
                accesses[offset].append(('store', instr))

        return accesses

    def _infer_type(self, offset, accesses):
        """Infer variable type from usage patterns."""
        type_votes = {'int': 0, 'float': 0, 'dword': 0, 'pointer': 0}

        for access_type, instr in accesses:
            # Check what happens AFTER load
            if access_type == 'load':
                next_instr = self._get_next_consumer(instr)
                if next_instr:
                    if next_instr.mnemonic.startswith('F'):  # FADD, FMUL, etc.
                        type_votes['float'] += 2
                    elif next_instr.mnemonic.startswith('I'):  # IADD, IMUL, etc.
                        type_votes['int'] += 2
                    elif next_instr.mnemonic in ['ADD', 'SUB', 'MUL']:
                        type_votes['dword'] += 1

            # Check if address is taken
            elif access_type == 'address':
                type_votes['pointer'] += 3  # Likely array or passed to function

            # Check what is STORED
            elif access_type == 'store':
                prev_instr = self._get_producer(instr)
                if prev_instr:
                    if prev_instr.mnemonic.startswith('F'):
                        type_votes['float'] += 2
                    elif prev_instr.mnemonic.startswith('I'):
                        type_votes['int'] += 2

        # Check data segment value
        data_entry = self.scr.get_data_at_offset(offset)
        if data_entry and data_entry['type'] == 'string':
            return 'char*'

        # Return highest voted type
        if type_votes['pointer'] > 0:
            return 'dword'  # Will be refined to specific pointer type
        elif type_votes['float'] > type_votes['int']:
            return 'float'
        elif type_votes['int'] > type_votes['dword']:
            return 'int'
        else:
            return 'dword'

    def _detect_array(self, offset, accesses):
        """Detect if global is an array based on access patterns."""
        # Pattern 1: GCP + offset arithmetic
        has_indexed_access = False
        max_index = 0

        for access_type, instr in accesses:
            if access_type == 'address':
                # Check if there's ADD/MUL after GCP
                consumers = self._get_consumers(instr.output)
                for consumer in consumers:
                    if consumer.mnemonic in ['ADD', 'MUL', 'IMUL']:
                        has_indexed_access = True
                        # Try to extract constant index
                        if consumer.mnemonic == 'ADD' and self._is_constant(consumer.arg2):
                            index = consumer.arg2 // 4  # Assuming 4-byte elements
                            max_index = max(max_index, index)

        if has_indexed_access and max_index > 0:
            return True, max_index + 1

        # Pattern 2: Multiple consecutive GLD/GST at offset+4, offset+8, etc.
        offsets_accessed = set()
        for access_type, instr in accesses:
            offsets_accessed.add(instr.arg1)

        if len(offsets_accessed) > 1:
            offsets_sorted = sorted(offsets_accessed)
            stride = offsets_sorted[1] - offsets_sorted[0]
            if stride in [4, 8, 12, 16]:  # Common element sizes
                array_size = len(offsets_sorted)
                return True, array_size

        return False, 0

    def _generate_name(self, offset, var_type):
        """Generate meaningful variable name."""
        # Check if offset matches known globals from headers
        # (This would require external knowledge base)

        # For now, use data_ prefix
        return f"data_{offset}"
```

**3. Integrace do dekompilátoru**

Soubor: `vcdecomp/__main__.py`

```python
def decompile_structure(scr_path, variant='auto'):
    # ... existing code ...

    # NEW: Analyze global variables
    from vcdecomp.core.analysis.global_analyzer import GlobalVariableAnalyzer
    global_analyzer = GlobalVariableAnalyzer(scr_file, instructions)
    globals = global_analyzer.analyze()

    # Generate global declarations
    output = []
    output.append("// Global variables from data segment")
    for offset, gvar in sorted(globals.items()):
        if gvar.is_array:
            output.append(f"{gvar.type} {gvar.name}[{gvar.array_size}];")
        else:
            output.append(f"{gvar.type} {gvar.name};")
    output.append("")

    # ... continue with function decompilation ...
```

### Test case
```python
# tests/test_global_detection.py
def test_detect_float_global():
    # gTime: GLD + FADD usage
    assert analyzer.infer_type(offset=0x100) == 'float'

def test_detect_array():
    # gRecTimer[64]: GCP + indexed access
    is_array, size = analyzer.detect_array(offset=0x200)
    assert is_array == True
    assert size == 64
```

### Odhadovaný čas: 12-15 hodin

---

## P0.2 - For-Loop Condition Fix (< vs <=)

### Problém
Všechny for-loop podmínky generují `<=` místo `<`, což způsobuje off-by-one bugs.

### Současný stav
```c
// CHYBNÉ: Iteruje 0..gRecs (gRecs+1 iterací!)
for (local_2 = 0; (local_2 <= gRecs); local_2++) {
    gRecTimer[local_2] = ...;  // Buffer overrun!
}
```

### Očekávaný výstup
```c
// SPRÁVNÉ:
for (i = 0; i < gRecs; i++) {
    gRecTimer[i] = ...;
}
```

### Příčina
Soubor: `vcdecomp/core/ir/structure.py`, metoda `_detect_for_loop()`

Pravděpodobně:
```python
def _detect_for_loop(self, block):
    # ...
    condition_op = condition_instr.mnemonic  # např. "JZ", "JNZ"

    # BUG: Používá <= pro všechny případy
    if condition_op == 'JNZ':
        loop_condition = f"{counter} <= {limit}"  # ❌ CHYBNÉ!
```

### Implementační kroky

**1. Analyzovat bytecode pattern**

```
Typický for-loop bytecode:
    IPUSH 0          // i = 0
    IASGN local_2

loop_start:
    IGLD local_2     // Načti i
    IGLD limit       // Načti limit (např. gRecs)
    ICMP             // Porovnej i vs limit
    JZ end_loop      // Skoč pokud i >= limit  →  tedy podmínka je i < limit

    // loop body

    IGLD local_2     // i++
    INC
    IASGN local_2
    JMP loop_start

end_loop:
```

**Klíčové zjištění:**
- `JZ end_loop` po `ICMP` znamená: "jump if comparison is ZERO (i >= limit)"
- Tedy podmínka pokračování je: `i < limit` (negace JZ podmínky)

**2. Opravit detection logic**

Soubor: `vcdecomp/core/ir/structure.py`

```python
def _detect_for_loop(self, block):
    """Detect for-loop pattern from block structure."""

    # Find loop components
    init_instr = self._find_loop_init(block)  # i = 0
    condition_instr = self._find_loop_condition(block)  # ICMP + JZ/JNZ
    increment_instr = self._find_loop_increment(block)  # INC/DEC

    if not all([init_instr, condition_instr, increment_instr]):
        return None

    # Extract counter variable
    counter_var = init_instr.target

    # Extract limit
    limit_expr = self._extract_limit(condition_instr)

    # CRITICAL: Determine comparison operator
    comparison_op = self._determine_comparison_op(condition_instr)

    return ForLoop(
        counter=counter_var,
        init_value=init_instr.value,
        condition=f"{counter_var} {comparison_op} {limit_expr}",
        increment=increment_instr
    )

def _determine_comparison_op(self, condition_instr):
    """
    Determine correct comparison operator for loop.

    Patterns:
    - ICMP + JZ  → i >= limit, so continue condition is: i < limit
    - ICMP + JNZ → i < limit, so continue condition is: i < limit (same!)
    - Wait, need to check jump direction!
    """
    cmp_instr = condition_instr.prev  # The actual ICMP
    jump_instr = condition_instr      # JZ/JNZ

    # Check if jump goes FORWARD (exit) or BACKWARD (continue)
    jump_target = jump_instr.target_block_id
    current_block_id = jump_instr.block_id

    is_forward_jump = jump_target > current_block_id

    if jump_instr.mnemonic == 'JZ':
        # Jump if ZERO (i >= limit)
        if is_forward_jump:
            # JZ forward → exit when i >= limit → continue while i < limit
            return '<'
        else:
            # JZ backward → continue when i >= limit (weird, but possible)
            return '>='

    elif jump_instr.mnemonic == 'JNZ':
        # Jump if NOT ZERO (i < limit)
        if is_forward_jump:
            # JNZ forward → exit when i < limit → continue while i >= limit
            return '>='
        else:
            # JNZ backward → continue when i < limit
            return '<'

    # Default fallback
    return '<'

def _extract_limit(self, condition_instr):
    """Extract loop limit from comparison instruction."""
    # The limit is the second operand of ICMP
    cmp_instr = self._find_previous_by_type(condition_instr, 'CMP')

    if cmp_instr and len(cmp_instr.inputs) >= 2:
        limit_value = cmp_instr.inputs[1]

        # Check if limit is a constant or variable
        if isinstance(limit_value, ConstantValue):
            return str(limit_value.value)
        elif isinstance(limit_value, GlobalVariable):
            return limit_value.name
        else:
            return self._render_value(limit_value)

    return "UNKNOWN"
```

**3. Test cases**

```python
# tests/test_loop_conditions.py

def test_for_loop_less_than():
    """Test: for (i=0; i<N; i++)"""
    code = """
    IPUSH 0
    IASGN local_0
    IGLD local_0
    IGLD N
    ICMP
    JZ end
    ...
    """
    loop = detect_for_loop(parse(code))
    assert loop.condition == "local_0 < N"

def test_for_loop_less_equal():
    """Test: for (i=0; i<=N; i++)"""
    code = """
    IPUSH 0
    IASGN local_0
    IGLD local_0
    IGLD N
    ICMP
    INC     # Result++
    JZ end  # Jump if result==0 (i > N)
    ...
    """
    loop = detect_for_loop(parse(code))
    assert loop.condition == "local_0 <= N"
```

### Odhadovaný čas: 6-8 hodin

---

## P0.3 - Array Reconstruction

### Problém
Lokální pole jako `char txt[32]`, `s_SC_HUD_MP_icon icon[2]` nejsou správně detekovány.

### Současný stav
```c
sprintf(&local_0, "DM%d", i);  // ❌ &local_0 je int*, ne char[32]
```

### Očekávaný výstup
```c
char txt[32];
sprintf(txt, "DM%d", i);
```

### Implementační kroky

**1. Detekce alloca/stack space patterns**

Soubor: `vcdecomp/core/ir/stack_lifter.py`

```python
class LocalArrayDetector:
    """Detects local arrays from stack allocation patterns."""

    def analyze_function(self, func_instrs):
        """Find all local arrays in function."""
        arrays = {}

        # Pattern 1: ASP (adjust stack pointer) at function start
        for i, instr in enumerate(func_instrs[:10]):  # Check first 10 instrs
            if instr.mnemonic == 'ASP':
                stack_size = abs(instr.arg1)
                # This creates stack space, likely for locals
                arrays.update(self._analyze_stack_usage(
                    func_instrs,
                    stack_size
                ))
                break

        # Pattern 2: LCP (local copy pointer) usage
        for instr in func_instrs:
            if instr.mnemonic == 'LCP':
                offset = instr.arg1
                # Check how this pointer is used
                array_info = self._infer_array_from_usage(instr, func_instrs)
                if array_info:
                    arrays[offset] = array_info

        return arrays

    def _infer_array_from_usage(self, lcp_instr, all_instrs):
        """Infer array type/size from how LCP result is used."""
        ptr_value = lcp_instr.output

        # Find all uses of this pointer
        uses = [instr for instr in all_instrs if ptr_value in instr.inputs]

        for use in uses:
            # Pattern: sprintf(ptr, ...) → char array
            if use.mnemonic == 'XCALL' and 'sprintf' in str(use):
                return LocalArray(
                    offset=lcp_instr.arg1,
                    type='char',
                    size=32,  # Default buffer size
                    name=f"txt_{lcp_instr.arg1}"
                )

            # Pattern: SC_ZeroMem(ptr, N) → array of size N
            elif use.mnemonic == 'XCALL' and 'ZeroMem' in str(use):
                if len(use.inputs) >= 2:
                    size = use.inputs[1]
                    if isinstance(size, ConstantValue):
                        return LocalArray(
                            offset=lcp_instr.arg1,
                            type='byte',
                            size=size.value,
                            name=f"arr_{lcp_instr.arg1}"
                        )

            # Pattern: Struct member access → struct array
            elif use.mnemonic in ['ASGN', 'DLD'] and self._is_struct_member(use):
                struct_type, count = self._infer_struct_array(use, all_instrs)
                if struct_type:
                    return LocalArray(
                        offset=lcp_instr.arg1,
                        type=struct_type,
                        size=count,
                        name=f"{struct_type.lower()}_{lcp_instr.arg1}"
                    )

        return None

    def _is_struct_member(self, instr):
        """Check if instruction accesses struct member."""
        # Look for pattern: ptr + constant_offset
        if instr.mnemonic == 'DLD':  # Dword load
            if len(instr.inputs) > 0:
                addr_expr = instr.inputs[0]
                # Check if addr_expr is (base + offset)
                if isinstance(addr_expr, BinaryOp) and addr_expr.op == '+':
                    if isinstance(addr_expr.right, ConstantValue):
                        # Offset like +4, +8, +12 suggests struct member
                        return True
        return False

    def _infer_struct_array(self, instr, all_instrs):
        """Infer struct type and array count from access patterns."""
        # Find all accesses to this base pointer
        base_ptr = instr.inputs[0].left  # The pointer before +offset

        accesses = []
        for other in all_instrs:
            if other.mnemonic in ['DLD', 'ASGN'] and base_ptr in str(other.inputs):
                # Extract offset
                if isinstance(other.inputs[0], BinaryOp):
                    offset = other.inputs[0].right.value
                    accesses.append(offset)

        if not accesses:
            return None, 0

        # Determine struct size (largest offset + 4)
        struct_size = max(accesses) + 4

        # Try to match against known structs
        known_structs = {
            16: 's_SC_HUD_MP_icon',  # Example
            28: 's_SC_MP_Recover',
            # ... more from headers
        }

        struct_type = known_structs.get(struct_size, f'struct_size{struct_size}')

        # Count how many struct instances (array size)
        # Pattern: access at offset 0, struct_size, 2*struct_size, etc.
        unique_bases = set(off // struct_size for off in accesses)
        array_count = len(unique_bases)

        return struct_type, array_count
```

**2. Generování deklarací**

Soubor: `vcdecomp/core/ir/expr.py`

```python
class CExpressionRenderer:
    def __init__(self, function, local_arrays):
        self.function = function
        self.local_arrays = local_arrays  # offset -> LocalArray

    def render_function(self):
        output = []

        # Function signature
        output.append(f"{self.function.return_type} {self.function.name}(...) {{")

        # Local variable declarations
        output.extend(self._generate_local_declarations())
        output.append("")

        # Function body
        # ...

        return "\\n".join(output)

    def _generate_local_declarations(self):
        """Generate declarations for all local variables and arrays."""
        decls = []

        # Arrays first
        for offset, array in sorted(self.local_arrays.items()):
            decls.append(f"    {array.type} {array.name}[{array.size}];")

        # Then regular locals
        for local_var in self.function.locals:
            if local_var.offset not in self.local_arrays:  # Skip already declared arrays
                decls.append(f"    {local_var.type} {local_var.name};")

        return decls

    def _render_value(self, value):
        """Render a value, handling array names."""
        if isinstance(value, PointerValue):
            # Check if this pointer points to local array
            if value.is_local and value.offset in self.local_arrays:
                # Return array name WITHOUT &
                return self.local_arrays[value.offset].name

        # ... existing rendering logic ...
```

### Test case
```python
def test_detect_char_array_sprintf():
    code = """
    LCP -32          # char txt[32]
    PUSH "DM%d"
    PUSH i
    XCALL sprintf
    """
    arrays = detect_arrays(parse(code))
    assert arrays[-32].type == 'char'
    assert arrays[-32].size == 32
```

### Odhadovaný čas: 10-12 hodin

---

## P0.4 - Variable Name Collision Fix

### Problém
Jedna proměnná `local_2` je použita pro 4 různé sémantické účely:
- Loop counter `i`
- Temporary `j`
- `sideA`
- `sideB`

Výsledek: `if (local_2 == local_2)` - porovnává sama sebe!

### Současný stav
```c
local_2 = player_info.field2;  // sideA
if ((info->field_8)) {
    local_2 = player_info.field2;  // ❌ Přepíše sideA → sideB
}
if (((local_2 == local_2))) {  // ❌ VŽDY TRUE!
```

### Očekávaný výstup
```c
sideA = player_info.field2;
if ((info->field_8)) {
    sideB = player_info.field2;
}
if (sideA == sideB) {  // ✅ Správné porovnání
```

### Implementační kroky

**1. Implementovat SSA (Static Single Assignment) form**

Soubor: `vcdecomp/core/ir/ssa.py` (NOVÝ)

```python
class SSAConverter:
    """Converts IR to SSA form where each variable is assigned exactly once."""

    def convert_to_ssa(self, ir_blocks):
        """Transform IR to SSA form."""
        self.var_versions = {}  # var_name -> current_version
        self.phi_nodes = {}     # block_id -> list of PHI nodes

        # Insert PHI nodes at merge points
        self._insert_phi_nodes(ir_blocks)

        # Rename variables
        self._rename_variables(ir_blocks)

        return ir_blocks

    def _rename_variables(self, blocks):
        """Rename each assignment to create unique version."""
        for block in blocks:
            for instr in block.instructions:
                # Rename inputs (use current versions)
                for i, input_val in enumerate(instr.inputs):
                    if isinstance(input_val, Variable):
                        versioned = self._get_current_version(input_val.name)
                        instr.inputs[i] = versioned

                # Rename output (create new version)
                if instr.output:
                    new_version = self._create_new_version(instr.output.name)
                    instr.output = new_version

    def _get_current_version(self, var_name):
        """Get current SSA version of variable."""
        if var_name not in self.var_versions:
            self.var_versions[var_name] = 0
        return f"{var_name}_{self.var_versions[var_name]}"

    def _create_new_version(self, var_name):
        """Create new SSA version for assignment."""
        if var_name not in self.var_versions:
            self.var_versions[var_name] = 0
        else:
            self.var_versions[var_name] += 1
        return f"{var_name}_{self.var_versions[var_name]}"
```

**2. Detekce kdy version split je potřeba**

```python
class VariableLifetimeAnalyzer:
    """Analyze when a local variable needs splitting."""

    def analyze(self, ssa_ir):
        """Detect variables that should be split into separate names."""
        split_vars = {}  # var_base -> list of version ranges

        for var_base, max_version in ssa_ir.var_versions.items():
            if max_version <= 0:
                continue  # Single version, no split needed

            # Analyze lifetime ranges for each version
            lifetimes = []
            for version in range(max_version + 1):
                var_name = f"{var_base}_{version}"
                first_def, last_use = self._find_lifetime(ssa_ir, var_name)

                lifetimes.append({
                    'version': version,
                    'first_def': first_def,
                    'last_use': last_use,
                    'semantic_type': self._infer_semantic_type(ssa_ir, var_name)
                })

            # Check if lifetimes overlap → need split
            if self._lifetimes_overlap(lifetimes):
                split_vars[var_base] = lifetimes

        return split_vars

    def _lifetimes_overlap(self, lifetimes):
        """Check if any lifetime ranges overlap."""
        for i, lt1 in enumerate(lifetimes):
            for lt2 in lifetimes[i+1:]:
                if (lt1['first_def'] <= lt2['last_use'] and
                    lt2['first_def'] <= lt1['last_use']):
                    return True  # Overlap found
        return False

    def _infer_semantic_type(self, ssa_ir, var_name):
        """Infer semantic purpose of variable version."""
        # Check usage patterns
        uses = ssa_ir.find_all_uses(var_name)

        # Pattern: Used as loop counter
        if any(self._is_loop_counter(use) for use in uses):
            return 'loop_counter'

        # Pattern: Stores player side
        if any('side' in str(use).lower() for use in uses):
            return 'side_value'

        # Pattern: Temporary computation
        if len(uses) <= 2:
            return 'temporary'

        return 'general'
```

**3. Semantic renaming**

```python
class SemanticRenamer:
    """Rename variables to semantic names based on usage."""

    SEMANTIC_NAMES = {
        'loop_counter': ['i', 'j', 'k', 'idx'],
        'side_value': ['sideA', 'sideB', 'side'],
        'temporary': ['tmp', 'temp'],
    }

    def rename(self, split_vars, ssa_ir):
        """Apply semantic names to split variables."""
        final_names = {}
        name_counters = {}  # semantic_type -> counter

        for var_base, versions in split_vars.items():
            for version_info in versions:
                var_ssa = f"{var_base}_{version_info['version']}"
                semantic_type = version_info['semantic_type']

                # Get next available name for this semantic type
                if semantic_type not in name_counters:
                    name_counters[semantic_type] = 0

                names_list = self.SEMANTIC_NAMES.get(semantic_type, ['local'])
                idx = name_counters[semantic_type] % len(names_list)
                base_name = names_list[idx]

                # Add suffix if needed
                if name_counters[semantic_type] >= len(names_list):
                    suffix = name_counters[semantic_type] // len(names_list)
                    final_name = f"{base_name}{suffix}"
                else:
                    final_name = base_name

                final_names[var_ssa] = final_name
                name_counters[semantic_type] += 1

        return final_names
```

### Test case
```python
def test_variable_split():
    code = """
    local_2 = value1  # Version 0 → sideA
    ...
    local_2 = value2  # Version 1 → sideB
    ...
    if (local_2_0 == local_2_1)  # Should become: if (sideA == sideB)
    """
    renamed = apply_ssa_and_rename(parse(code))
    assert 'sideA' in renamed
    assert 'sideB' in renamed
    assert 'sideA == sideB' in renamed
```

### Odhadovaný čas: 14-16 hodin

---

## P0.5 - Boolean Expression Reconstruction (OR/AND)

### Problém
Kompilátor rozložil `(A && B) || (C && D)` na vnořené if-else bloky.
Dekompilátor to nerekonstruuje zpět.

### Současný stav
```c
if (((gSideFrags[0] > 0))) {
    if (((gSideFrags[0] >= gEndValue))) {
        // ❌ CHYBÍ TĚLO!
    } else {
        if (((gSideFrags[1] > 1))) {
            if (((gSideFrags[1] >= gEndValue))) {
                SC_MP_LoadNextMap();
                return TRUE;
            }
        }
    }
}
```

### Očekávaný výstup
```c
if (((gSideFrags[0] > 0) && (gSideFrags[0] >= gEndValue))
    || ((gSideFrags[1] > 1) && (gSideFrags[1] >= gEndValue)))
{
    SC_MP_LoadNextMap();
    return TRUE;
}
```

### Implementační kroky

**1. Detekce short-circuit patterns**

Soubor: `vcdecomp/core/ir/structure.py`

```python
class BooleanExpressionReconstructor:
    """Reconstructs complex boolean expressions from control flow."""

    def reconstruct_if_condition(self, if_block):
        """Try to merge nested if-else into single boolean expression."""

        # Pattern 1: AND (if A { if B { body } })
        if self._is_and_pattern(if_block):
            conditions = self._extract_and_conditions(if_block)
            return BooleanExpr('AND', conditions)

        # Pattern 2: OR (if A { body } else { if B { body } })
        if self._is_or_pattern(if_block):
            conditions = self._extract_or_conditions(if_block)
            return BooleanExpr('OR', conditions)

        # Pattern 3: Complex (A && B) || (C && D)
        if self._is_complex_pattern(if_block):
            return self._reconstruct_complex(if_block)

        # Fallback: single condition
        return if_block.condition

    def _is_and_pattern(self, block):
        """Check if block matches: if A { if B { body } }"""
        if not block.true_branch:
            return False

        true_body = block.true_branch.instructions

        # True branch should have exactly one if-statement
        if len(true_body) == 1 and isinstance(true_body[0], IfBlock):
            # And no else branch on outer if
            if not block.false_branch:
                return True

        return False

    def _extract_and_conditions(self, block):
        """Extract all conditions from AND pattern."""
        conditions = [block.condition]

        current = block.true_branch.instructions[0]
        while isinstance(current, IfBlock) and not current.false_branch:
            conditions.append(current.condition)
            if current.true_branch:
                current = current.true_branch.instructions[0]
            else:
                break

        return conditions

    def _is_or_pattern(self, block):
        """Check if block matches: if A { body } else { if B { body } }"""
        if not block.false_branch:
            return False

        false_body = block.false_branch.instructions

        # False branch should have exactly one if-statement
        if len(false_body) == 1 and isinstance(false_body[0], IfBlock):
            # Check if true bodies are identical
            if self._same_body(block.true_branch, false_body[0].true_branch):
                return True

        return False

    def _extract_or_conditions(self, block):
        """Extract all conditions from OR pattern."""
        conditions = [block.condition]

        target_body = block.true_branch
        current = block.false_branch.instructions[0]

        while isinstance(current, IfBlock):
            if self._same_body(current.true_branch, target_body):
                conditions.append(current.condition)
                if current.false_branch:
                    current = current.false_branch.instructions[0]
                else:
                    break
            else:
                break

        return conditions

    def _reconstruct_complex(self, block):
        """Reconstruct complex expression like (A && B) || (C && D)."""
        # This is the TDM.C case!

        # Outer structure: if A { if B { MISSING } else { if C { if D { body } } } }
        # This should be: (A && B) || (C && D)

        outer_cond = block.condition  # A

        if not isinstance(block.true_branch.instructions[0], IfBlock):
            return None

        inner_if = block.true_branch.instructions[0]
        second_cond = inner_if.condition  # B

        # Check if inner_if has empty true branch but populated false branch
        if not inner_if.true_branch and inner_if.false_branch:
            # Empty true = A && B is NOT satisfied
            # Now check false branch for alternative

            alt_block = inner_if.false_branch.instructions[0]
            if isinstance(alt_block, IfBlock):
                third_cond = alt_block.condition  # C

                if isinstance(alt_block.true_branch.instructions[0], IfBlock):
                    fourth_cond = alt_block.true_branch.instructions[0].condition  # D

                    # Found pattern: (A && B) || (C && D)
                    return BooleanExpr('OR', [
                        BooleanExpr('AND', [outer_cond, second_cond]),
                        BooleanExpr('AND', [third_cond, fourth_cond])
                    ])

        return None

    def _same_body(self, body1, body2):
        """Check if two code blocks are identical."""
        if not body1 or not body2:
            return False

        # Compare instruction sequences
        instrs1 = body1.instructions
        instrs2 = body2.instructions

        if len(instrs1) != len(instrs2):
            return False

        for i1, i2 in zip(instrs1, instrs2):
            if not self._same_instruction(i1, i2):
                return False

        return True

    def _same_instruction(self, instr1, instr2):
        """Check if two instructions are equivalent."""
        return (instr1.mnemonic == instr2.mnemonic and
                str(instr1.inputs) == str(instr2.inputs))
```

**2. Rendering**

```python
class BooleanExpr:
    def __init__(self, op, operands):
        self.op = op  # 'AND', 'OR', 'NOT'
        self.operands = operands  # list of conditions or BooleanExpr

    def render(self):
        if self.op == 'AND':
            parts = [self._render_operand(op) for op in self.operands]
            return f"({' && '.join(parts)})"

        elif self.op == 'OR':
            parts = [self._render_operand(op) for op in self.operands]
            return f"({' || '.join(parts)})"

        elif self.op == 'NOT':
            return f"!({self._render_operand(self.operands[0])})"

    def _render_operand(self, operand):
        if isinstance(operand, BooleanExpr):
            return operand.render()
        else:
            return str(operand)
```

### Test case
```python
def test_reconstruct_or_and():
    code = """
    if A:
        if B:
            # empty
        else:
            if C:
                if D:
                    return TRUE
    """
    expr = reconstruct_boolean(parse(code))
    assert expr.render() == "((A && B) || (C && D))"
```

### Odhadovaný čas: 12-14 hodin

---

## CELKOVÝ ODHAD P0 OPRAV

| Úkol | Čas (hodiny) |
|------|--------------|
| P0.1 - Global variables | 12-15 |
| P0.2 - Loop conditions | 6-8 |
| P0.3 - Array reconstruction | 10-12 |
| P0.4 - Variable collision | 14-16 |
| P0.5 - Boolean expressions | 12-14 |
| **CELKEM** | **54-65 hodin** |

---

## POZNÁMKY K IMPLEMENTACI

### Testování
Pro každou opravu:
1. Napsat unit testy s jednoduchými případy
2. Otestovat na TDM.SCR
3. Otestovat na dalších skriptech z `script-folders/`

### Prioritní pořadí implementace
1. **P0.2 Loop conditions** - Nejjednodušší, rychlý win
2. **P0.1 Global variables** - Nutné pro kompilaci
3. **P0.3 Array reconstruction** - Navazuje na P0.1
4. **P0.4 Variable collision** - Kritické pro správnost
5. **P0.5 Boolean expressions** - Nejkomplexnější

### Nástroje
- Vizualizace CFG (Control Flow Graph) pomůže s P0.5
- SSA vizualizace pomůže s P0.4
- IR dump pro debugging všech oprav

---

**Další kroky:** Pokračovat s P1 prioritami (Type Inference, Hex Constants, atd.)
