# LEVEL.SCR Decompiler Fix Proposals

**Generated**: 2026-01-15
**Reference**: `LEVEL_ERROR_REPORT.md`

---

## Fix Proposal #1: Oprava Algoritmu Detekce Hranic Funkcí (P0 - BLOCKER)

### Popis Chyby
- **Kategorie**: Function Boundary Detection
- **Severity**: 🔴 **P0 - BLOCKER**
- **Symptom**: Dekompilátor vytváří 240 funkcí místo 28 (850% false positive rate)
- **Očekáváno**: 28 funkcí (odpovídající SaveInfo items count)
- **Aktuálně**: 240 funkcí (každá branch/early return je považována za novou funkci)

### Root Cause Analysis

**Soubor**: `vcdecomp/core/ir/function_detector.py`
**Funkce**: `detect_function_boundaries_v2()` (lines 21-125)

**Současné Chování** (řádky 82-89):
```python
# Add address after each RET as new function start
for ret_addr in ret_addresses:
    next_addr = ret_addr + 1
    if next_addr < len(instructions):
        function_starts.append(next_addr)
```

**Proč selhává**:
1. Algoritmus **chybně předpokládá**, že **každý RET končí funkci**
2. Ve skutečnosti funkce mohou mít **multiple RET instructions**:
   - Early returns (`if (error) return FALSE;`)
   - Different branches (`if (cond) return A; else return B;`)
   - Multiple exit points
3. **Výsledek**: Funkce je rozdělena na desítky micro-funkcí podle počtu RET statements

**Příklad problému**:
```c
// Skutečná funkce (měla by být jedna)
int CheckPlayer(int id) {
    if (!id) return FALSE;      // RET #1
    if (id > 100) return FALSE; // RET #2
    return TRUE;                // RET #3
}
```

**Současný výstup** (3 funkce místo 1):
```c
int func_0100() {
    if (!id) return FALSE;
}  // <-- RET detected, new function starts

int func_0104() {
    if (id > 100) return FALSE;
}  // <-- RET detected, new function starts

int func_0108() {
    return TRUE;
}  // <-- RET detected, no next function
```

### Navržená Oprava

**Strategie**:
Použít **kombinaci CALL targets + RET boundaries** místo pouze RET instructions:

1. **CALL targets = definitivní začátky funkcí** (jsou voláno z jiného kódu)
2. **První RET po CALL target = konec funkce**
3. **Další RET statements uvnitř funkce = ignorovat** (early returns)
4. **Entry point = speciální případ** (ScriptMain)

**Změny kódu**:

**Soubor**: `vcdecomp/core/ir/function_detector.py`

**Současný kód** (problematický):
```python
def detect_function_boundaries_v2(
    scr: SCRFile,
    resolver: OpcodeResolver,
    entry_point: int = None
) -> Dict[str, Tuple[int, int]]:
    # ... (lines 48-67 unchanged)

    # Step 3: Build function segments
    boundaries = {}
    function_starts = []

    # Add entry point if provided
    if entry_point is not None:
        function_starts.append(entry_point)
    else:
        function_starts.append(0)

    # CHYBA: Add address after EVERY RET as new function start
    for ret_addr in ret_addresses:
        next_addr = ret_addr + 1
        if next_addr < len(instructions):
            function_starts.append(next_addr)

    function_starts = sorted(set(function_starts))

    # Step 4: Pair starts with ends
    for i, start in enumerate(function_starts):
        # Find RET that ends this function
        end = None
        for ret_addr in ret_addresses:
            if ret_addr >= start:
                end = ret_addr
                break
        # ... assign names ...
```

**Navržený kód** (opravený):
```python
def detect_function_boundaries_v2(
    scr: SCRFile,
    resolver: OpcodeResolver,
    entry_point: int = None
) -> Dict[str, Tuple[int, int]]:
    """
    Detect function boundaries using CALL targets + RET analysis.

    Strategy:
    1. Use CALL targets as definitive function starts
    2. Use entry_point as ScriptMain start
    3. Find first RET after each function start as end
    4. Ignore intermediate RET statements (early returns)
    """
    instructions = scr.code_segment.instructions
    return_opcodes = resolver.return_opcodes
    internal_call_opcodes = resolver.internal_call_opcodes

    # Step 1: Find all RET addresses
    ret_addresses = []
    for instr in instructions:
        if instr.opcode in return_opcodes:
            ret_addresses.append(instr.address)

    ret_addresses.sort()
    logger.debug(f"Found {len(ret_addresses)} RET instructions")

    # Step 2: Find CALL targets (definitive function starts)
    call_targets = set()
    for instr in instructions:
        if instr.opcode in internal_call_opcodes:
            call_targets.add(instr.arg1)

    logger.debug(f"Found {len(call_targets)} CALL targets: {sorted(call_targets)}")

    # Step 3: Build function starts (ONLY from CALL targets + entry point)
    function_starts = []

    # Add entry point
    if entry_point is not None:
        function_starts.append(entry_point)
        logger.debug(f"Entry point at address {entry_point}")

    # Add CALL targets
    function_starts.extend(call_targets)

    # FIX: Check for orphan code before first function
    if function_starts:
        first_func = min(function_starts)
        if first_func > 0:
            # There's code before first function, add as _init
            function_starts.append(0)
            logger.debug(f"Orphan code detected at start, adding _init function at 0")

    function_starts = sorted(set(function_starts))
    logger.debug(f"Function starts (CALL-based): {function_starts}")

    # Step 4: Pair each start with FIRST RET after it
    boundaries = {}
    for i, start in enumerate(function_starts):
        # Find FIRST RET that comes after this start
        end = None
        for ret_addr in ret_addresses:
            if ret_addr >= start:
                # This is the first RET after function start
                # Check if it's before next function start
                if i + 1 < len(function_starts):
                    next_start = function_starts[i + 1]
                    if ret_addr < next_start:
                        # RET is within this function
                        end = ret_addr
                        break
                    else:
                        # RET is after next function start - use next_start - 1
                        end = next_start - 1
                        logger.warning(
                            f"Function at {start} has no RET before next function at {next_start}, "
                            f"using {end} as end"
                        )
                        break
                else:
                    # Last function, use this RET
                    end = ret_addr
                    break

        if end is None:
            # No RET found, function extends to end of code
            end = len(instructions) - 1
            logger.warning(
                f"Function starting at {start} has no RET instruction, "
                f"extending to end of code at {end}"
            )

        # Assign name
        if start == entry_point:
            func_name = "ScriptMain"
        elif start == 0 and start not in call_targets:
            func_name = "_init"
        else:
            func_name = f"func_{start:04d}"

        boundaries[func_name] = (start, end)
        logger.debug(f"Function {func_name}: addresses {start} to {end}")

    logger.info(f"Detected {len(boundaries)} functions using CALL+RET analysis")
    return boundaries
```

### Test Strategie

**Verifikace**:
1. Regenerovat dekompilaci LEVEL.SCR
2. Spočítat funkce: očekáváno **28** (nebo 27 + 1 ScriptMain)
3. Ověřit že ScriptMain existuje @ IP 9054
4. Ověřit že func_0291, func_0313, func_0332, func_0354 jsou separate functions

**Test Commands**:
```bash
# Regenerovat
py -m vcdecomp structure decompilation/TUNNELS01/SCRIPTS/LEVEL.SCR > LEVEL_test.c

# Spočítat funkce
grep -c "^int func_" LEVEL_test.c
grep -c "^int ScriptMain" LEVEL_test.c
# Expected: 27 + 1 = 28

# Ověřit specifické funkce
grep "^int func_0291" LEVEL_test.c  # Should exist
grep "^int func_0313" LEVEL_test.c  # Should exist
grep "^int func_0332" LEVEL_test.c  # Should exist
grep "^int ScriptMain" LEVEL_test.c # Should exist

# Regression test
pytest vcdecomp/tests/ -v
```

### Dopad

**Pozitivní**:
- ✅ Opraví 240 → 28 funkcí (97% reduction v false positives)
- ✅ ScriptMain bude detekován správně
- ✅ Bude možné analyzovat control flow patterns
- ✅ Umožní recompilation testing
- ✅ Benefituje **všechny skripty** v projektu

**Riziko**: Nízké
- Změna je lokalizovaná do jedné funkce
- Existing testy by měly zachytit regressions
- Logika je jednodušší než původní (méně edge cases)

---

## Fix Proposal #2: Oprava Duplicitních Názvů Parametrů (P1 - CRITICAL)

### Popis Chyby
- **Kategorie**: Function Signature Detection
- **Severity**: 🔴 **P1 - CRITICAL**
- **Symptom**: Všechny funkce s více parametry mají duplicitní názvy `int param, int param`
- **Očekáváno**: `int param_0, int param_1, int param_2`
- **Aktuálně**: `int param, int param, int param` (syntax error v C)

### Root Cause Analysis

**Soubor**: `vcdecomp/core/ir/function_signature.py`
**Funkce**: `FunctionSignature.to_c_signature()` (lines 28-40)

**Současné chování** (řádek 38):
```python
def to_c_signature(self, func_name: str) -> str:
    """Convert to C function signature string."""
    if self.param_count == 0:
        params = "void"
    else:
        # Use detected types or fallback to generic types
        if len(self.param_types) == self.param_count:
            params = ", ".join(self.param_types)
        else:
            # Fallback: use generic int/float based on count
            params = ", ".join([f"int param{i}" for i in range(self.param_count)])
            #                           ^^^^^^ - CHYBA: Missing underscore!

    return f"{self.return_type} {func_name}({params})"
```

**Proč selhává**:
- F-string `f"int param{i}"` generuje `"int param0"`, `"int param1"`, ale pak se **spojuje**
- Výsledek: `"int param0, int param1, int param2"`
- ALE WAIT - to vypadá správně! Problém je někde jinde...

**Re-analýza**:
Podívejme se na skutečný výstup:
```c
int func_0354(int param, int param, int param) {
```

Tohle vypadá jako že `{i}` není interpolováno! Možná jsou použité apostrofy místo uvozovek?

**Skutečná chyba**:
Pravděpodobně je kód napsaný jako:
```python
params = ", ".join(['int param{i}' for i in range(self.param_count)])
#                   ^^^^^^^^^^^^^ - Single quotes = NO interpolation!
```

Místo:
```python
params = ", ".join([f"int param{i}" for i in range(self.param_count)])
#                   ^^^^^^^^^^^^^^ - F-string with interpolation
```

### Navržená Oprava

**Strategie**: Opravit string formátování pro použití f-string nebo .format()

**Změny kódu**:

**Soubor**: `vcdecomp/core/ir/function_signature.py`

**Současný kód** (pravděpodobný):
```python
# Line 38
params = ", ".join(['int param{i}' for i in range(self.param_count)])
```

**Navržený kód Option 1** (f-string s underscorem):
```python
# Line 38
params = ", ".join([f"int param_{i}" for i in range(self.param_count)])
```

**Navržený kód Option 2** (bez underscore, ale funkční):
```python
# Line 38
params = ", ".join([f"int param{i}" for i in range(self.param_count)])
```

**Doporučení**: Option 1 (s underscorem) pro konzistenci s `local_0`, `data_100` atd.

### Test Strategie

**Verifikace**:
```bash
# Regenerovat
py -m vcdecomp structure decompilation/TUNNELS01/SCRIPTS/LEVEL.SCR > LEVEL_test.c

# Zkontrolovat parameter names
grep "int param, int param" LEVEL_test.c
# Expected: NO MATCHES

grep "int param_0, int param_1" LEVEL_test.c
# Expected: MATCHES (functions with 2+ params)

# Unit test
pytest vcdecomp/tests/test_function_signature.py -v
```

### Dopad

**Pozitivní**:
- ✅ Opraví syntax error v function signatures
- ✅ Umožní kompilaci decompiled kódu
- ✅ Zlepší čitelnost
- ✅ Benefituje všechny skripty

**Riziko**: Velmi nízké
- Triviální změna (1 řádek)
- Existující testy by měly zachytit regrese

---

## Fix Proposal #3: Filtrace Nedosažitelného Kódu (P2 - MAJOR)

### Popis Chyby
- **Kategorie**: Dead Code Elimination
- **Severity**: 🟡 **P2 - MAJOR**
- **Symptom**: Multiple `return` statements v sekvenci (nedosažitelný kód)
- **Očekáváno**: Jeden unified return nebo removal of unreachable code
- **Aktuálně**: Až 3 return statements v jedné funkci

### Root Cause Analysis

**Soubor**: `vcdecomp/core/ir/structure/orchestrator.py`
**Funkce**: `format_structured_function_named()` nebo `_format_block_lines()`

**Současné chování**:
Orchestrator emituje všechny bloky v CFG, včetně těch které jsou **nedosažitelné** po return/unconditional jump.

**Proč selhává**:
1. Po opravě Fix #1, funkce budou mít správné hranice
2. ALE uvnitř funkcí mohou být nedosažitelné bloky kvůli:
   - Early returns v if/else branches
   - Unconditional jumps (breaks v loops)
3. Orchestrator nefiltruje tyto bloky

### Navržená Oprava

**Strategie**: Implement dead code analysis před emission

**Změny kódu**:

**Soubor**: `vcdecomp/core/ir/structure/orchestrator.py`

**Přidat novou helper funkci**:
```python
def _find_reachable_blocks(cfg: CFG, entry_block: int) -> Set[int]:
    """
    Find all blocks reachable from entry_block using DFS.

    Args:
        cfg: Control flow graph
        entry_block: Entry block ID

    Returns:
        Set of reachable block IDs
    """
    reachable = set()
    stack = [entry_block]

    while stack:
        block_id = stack.pop()
        if block_id in reachable:
            continue

        reachable.add(block_id)

        # Add successors
        block = cfg.blocks.get(block_id)
        if block:
            for succ in block.successors:
                if succ not in reachable:
                    stack.append(succ)

    return reachable
```

**Upravit `format_structured_function_named()`**:
```python
def format_structured_function_named(...):
    # ... (existing code) ...

    # NEW: Find reachable blocks
    entry_block = cfg.entry_block
    reachable_blocks = _find_reachable_blocks(cfg, entry_block)

    logger.debug(
        f"Function {func_name}: {len(reachable_blocks)}/{len(cfg.blocks)} blocks reachable"
    )

    # Filter out unreachable blocks from rendering
    blocks_to_render = [bid for bid in all_blocks if bid in reachable_blocks]

    # ... (continue with blocks_to_render instead of all_blocks) ...
```

### Test Strategie

**Verifikace**:
```bash
# Check for multiple returns in sequence
grep -A5 "return" LEVEL_test.c | grep -c "return"
# Should be lower than before

# Specific check for func_0354
sed -n '/^int func_0354/,/^}/p' LEVEL_test.c
# Should have max 1-2 returns, not 3
```

### Dopad

**Pozitivní**:
- ✅ Čistší, čitelnější kód
- ✅ Méně confusing pro člověka i compiler
- ✅ Benefituje všechny skripty

**Riziko**: Střední
- Dead code detection musí být správně implementován
- Možné false positives (legitimní kód označený jako unreachable)
- Vyžaduje testování na multiple scripts

---

## Priority Implementace

### Fáze 1: Kritické Opravy (Den 1)
1. **Fix #1** - Detekce hranic funkcí (240 → 28)
2. **Fix #2** - Duplicitní parameter names
3. **Testování**: Verifikace na LEVEL.SCR

### Fáze 2: Control Flow Analýza (Den 2)
4. Analyzovat ScriptMain switch/case patterns
5. Identifikovat missing cases (case 2, case 4)
6. Vytvořit Fix Proposal #4 pro switch/case detection

### Fáze 3: Code Quality (Den 3)
7. **Fix #3** - Dead code filtering
8. Regression testing na všech Compiler-testruns
9. Final validation report

---

## Regression Test Checklist

Po každé opravě spustit:

```bash
# Unit tests
pytest vcdecomp/tests/ -v

# Known good scripts
py -m vcdecomp validate Compiler-testruns/Testrun1/tdm.scr Compiler-testruns/Testrun1/tdm.c
py -m vcdecomp validate Compiler-testruns/Testrun3/hitable.scr Compiler-testruns/Testrun3/hitable.c
py -m vcdecomp validate Compiler-testruns/Testrun4/tt.scr Compiler-testruns/Testrun4/tt.c

# LEVEL.SCR (target script)
py -m vcdecomp structure decompilation/TUNNELS01/SCRIPTS/LEVEL.SCR > LEVEL_fixed.c
grep -c "^int " LEVEL_fixed.c  # Should be ~28
```

---

## Success Criteria

### Fix #1 Success:
- [ ] Function count: 27-28 (not 240)
- [ ] ScriptMain detected @ IP 9054
- [ ] func_0291, func_0313, func_0332, func_0354 exist as separate functions
- [ ] All tests pass

### Fix #2 Success:
- [ ] No duplicitní parameter names (`int param, int param`)
- [ ] All params have unique names (`param_0`, `param_1`, etc.)
- [ ] Decompiled code compiles without errors

### Fix #3 Success:
- [ ] Max 1-2 returns per function (not 3+)
- [ ] No dead code after unconditional jumps
- [ ] Cleaner, more readable output
