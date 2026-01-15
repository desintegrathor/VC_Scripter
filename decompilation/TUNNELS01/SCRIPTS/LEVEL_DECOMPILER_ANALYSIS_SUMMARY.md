# LEVEL.SCR Decompiler Analysis - Executive Summary

**Datum**: 2026-01-15
**Skript**: `decompilation/TUNNELS01/SCRIPTS/LEVEL.SCR` (138KB, 10,051 instrukcí)
**Cíl**: Identifikace chyb dekompilátoru a návrh konkrétních oprav

---

## Klíčová Zjištění

### 🔴 Kritická Chyba: Explozivní Počet Funkcí

**Problém**: Dekompilátor vytváří **240 funkcí** místo skutečných **28 funkcí** (850% false positive rate)

**Root Cause**: `vcdecomp/core/ir/function_detector.py:82-89`
- Algoritmus **chybně vytváří novou funkci po KAŽDÉM RET instruction**
- Funkce s multiple returns (early returns, branches) jsou rozděleny na desítky micro-funkcí
- ScriptMain (@ IP 9054) není detekován jako entry point

**Dopad**: Kompletně nečitelný výstup, znemožňuje další analýzy a recompilation testing

---

## Identifikované Chyby (Priority)

### P0 - Blocker (Blokují Všechno Ostatní)

#### #1A: Detekce Hranic Funkcí
- **Symptom**: 240 funkcí vs. 28 očekávaných
- **Soubor**: `vcdecomp/core/ir/function_detector.py`
- **Funkce**: `detect_function_boundaries_v2()` (lines 82-89)
- **Fix**: Používat CALL targets + první RET po každém CALL, ignorovat intermediate RET statements

#### #1B: ScriptMain Entry Point
- **Symptom**: ScriptMain není detekován (funkce chybí)
- **Soubor**: `vcdecomp/core/ir/function_detector.py`
- **Fix**: Zajistit že funkce s `entry_point` (IP 9054) je pojmenována ScriptMain

### P1 - Critical

#### #2A: Duplicitní Názvy Parametrů
- **Symptom**: `int param, int param, int param` (syntax error)
- **Očekáváno**: `int param_0, int param_1, int param_2`
- **Soubor**: `vcdecomp/core/ir/function_signature.py`
- **Funkce**: `FunctionSignature.to_c_signature()` (line 38)
- **Fix**: Opravit string formatting na `f"int param_{i}"`

### P2 - Major

#### #3A: Nedosažitelný Kód
- **Symptom**: Multiple return statements v sekvenci (až 3x return v jedné funkci)
- **Soubor**: `vcdecomp/core/ir/structure/orchestrator.py`
- **Fix**: Implementovat dead code analysis (reachability analysis z entry_block)

### P3 - Minor

#### #5A: Auto-generated Variable Names
- **Symptom**: Mnoho proměnných má komentář `// Auto-generated` místo smysluplných názvů
- **Soubor**: `vcdecomp/core/ir/variable_renaming.py`
- **Fix**: Inference z usage patterns (optional)

---

## Navržené Opravy

### Fix #1: Algoritmus Detekce Funkcí (P0)

**Strategie**: Kombinace CALL targets + RET analysis

**Klíčová změna**:
```python
# PŘED (chybné):
for ret_addr in ret_addresses:
    next_addr = ret_addr + 1
    if next_addr < len(instructions):
        function_starts.append(next_addr)  # <-- Každý RET = nová funkce!

# PO (správné):
# Use only CALL targets + entry_point as function starts
function_starts = []
if entry_point is not None:
    function_starts.append(entry_point)
function_starts.extend(call_targets)

# For each start, find FIRST RET after it (ignore intermediate RETs)
for start in function_starts:
    end = first_ret_after(start)  # Not ALL rets
```

**Očekávaný výsledek**: 27-28 funkcí (snížení z 240)

### Fix #2: Parameter Names (P1)

**Klíčová změna**:
```python
# PŘED:
params = ", ".join(['int param{i}' for i in range(self.param_count)])
#                   ^^^^^^^^^^^^^^ - No f-string!

# PO:
params = ", ".join([f"int param_{i}" for i in range(self.param_count)])
#                   ^^^^^^^^^^^^^^^^ - F-string with index
```

**Očekávaný výsledek**: `int param_0, int param_1, int param_2`

### Fix #3: Dead Code Filtering (P2)

**Strategie**: Reachability analysis before emission

**Klíčová změna**:
```python
# Add to orchestrator.py
def _find_reachable_blocks(cfg, entry_block):
    # DFS to find all reachable blocks
    ...

# In format_structured_function_named():
reachable_blocks = _find_reachable_blocks(cfg, entry_block)
blocks_to_render = [bid for bid in all_blocks if bid in reachable_blocks]
```

**Očekávaný výsledek**: Max 1-2 returns per function (not 3+)

---

## Vytvořené Dokumenty

### 1. `LEVEL_ERROR_REPORT.md` (Detailní Report Chyb)
- Kompletní seznam všech identifikovaných chyb
- Evidence (line numbers, code snippets)
- Kategorizace podle severity (P0, P1, P2, P3)
- Trasování do zdrojového kódu dekompilátoru

### 2. `LEVEL_FIX_PROPOSALS.md` (Návrhy Oprav)
- Detailní fix proposal pro každou chybu
- Root cause analysis
- Code snippets (před/po)
- Test strategie
- Impact assessment

### 3. `LEVEL_new_decompiled.c` (Současný Výstup)
- Nová dekompilace LEVEL.SCR pro porovnání
- Zobrazuje všechny identifikované problémy

### 4. `LEVEL_new_disasm.asm` (Ground Truth)
- Disassembly pro validaci
- Referenční výstup pro porovnání

### 5. `LEVEL_info.txt` (Statistiky)
- Script info (10,051 instrukcí, 97 XFN funkcí)
- Entry point @ IP 9054
- SaveInfo items: 28 (= skutečný počet funkcí)

---

## Implementační Plán

### Fáze 1: Kritické Opravy (Den 1)
1. ✅ Provést analýzu a identifikovat chyby
2. ✅ Vytvořit ERROR_REPORT.md
3. ✅ Vytvořit FIX_PROPOSALS.md
4. ⏭️ Implementovat Fix #1 (hranice funkcí)
5. ⏭️ Implementovat Fix #2 (parameter names)
6. ⏭️ Testovat na LEVEL.SCR

### Fáze 2: Control Flow Analýza (Den 2)
7. ⏭️ Po opravě #1, analyzovat ScriptMain switch/case
8. ⏭️ Identifikovat missing cases (case 2, case 4)
9. ⏭️ Vytvořit Fix Proposal #4 pro switch patterns

### Fáze 3: Code Quality (Den 3)
10. ⏭️ Implementovat Fix #3 (dead code)
11. ⏭️ Regression testing na všech Compiler-testruns
12. ⏭️ Final validation report

---

## Test Commands

### Po Fix #1 (Hranice Funkcí):
```bash
py -m vcdecomp structure decompilation/TUNNELS01/SCRIPTS/LEVEL.SCR > LEVEL_test.c
grep -c "^int func_" LEVEL_test.c       # Expected: ~27
grep -c "^int ScriptMain" LEVEL_test.c  # Expected: 1
```

### Po Fix #2 (Parameter Names):
```bash
grep "int param, int param" LEVEL_test.c     # Expected: 0 matches
grep "int param_0, int param_1" LEVEL_test.c # Expected: >0 matches
```

### Po Fix #3 (Dead Code):
```bash
# Check function for multiple returns
sed -n '/^int func_0354/,/^}/p' LEVEL_test.c
# Expected: Max 1-2 returns
```

### Regression Tests:
```bash
pytest vcdecomp/tests/ -v
py -m vcdecomp validate Compiler-testruns/Testrun1/tdm.scr Compiler-testruns/Testrun1/tdm.c
py -m vcdecomp validate Compiler-testruns/Testrun3/hitable.scr Compiler-testruns/Testrun3/hitable.c
```

---

## Success Criteria

### ✅ Analýza Dokončena
- [x] Nová dekompilace vygenerována
- [x] Chyby identifikovány a kategorizovány
- [x] Root causes trasovány do zdrojového kódu
- [x] Fix proposals vytvořeny s code snippets
- [x] Dokumentace kompletní

### ⏭️ Implementace (Next Steps)
- [ ] Fix #1: Detekce hranic funkcí (240 → 28)
- [ ] Fix #2: Parameter names (param → param_0)
- [ ] Fix #3: Dead code filtering
- [ ] Switch/case analysis (po Fix #1)
- [ ] Recompilation testing

---

## Závěr

Analýza LEVEL.SCR odhalila **kritickou chybu** v algoritmu detekce hranic funkcí v `function_detector.py`, která způsobuje 850% false positive rate (240 vs 28 funkcí).

**Root cause** je jasný: algoritmus vytváří novou funkci po **každém RET instruction**, místo použití **CALL targets** jako definitivních začátků funkcí.

**Navržená oprava** je přímočará: použít CALL targets + entry_point jako function starts, a pro každý start najít **první RET** (nikoliv všechny RET).

Další identifikované chyby (duplicitní parameter names, dead code) jsou sekundární a snadno opravitelné po vyřešení primárního problému.

**Doporučení**: Implementovat Fix #1 jako **nejvyšší prioritu**, poté Fix #2, a nakonec pokračovat s analýzou control flow patterns v ScriptMain.
