# LEVEL.SCR Decompiler Error Report

**Generated**: 2026-01-15
**Script**: `decompilation/TUNNELS01/SCRIPTS/LEVEL.SCR`
**Size**: 138,279 bytes (10,051 instructions)

## Executive Summary

Nová dekompilace LEVEL.SCR odhalila **kritické chyby** v dekompilátoru, které způsobují nesprávnou detekci hranic funkcí a control flow patterns:

### Kritická Statistika

| Metrika | Disassembly (Expected) | Decompiled (Actual) | Status |
|---------|----------------------|-------------------|--------|
| **Počet funkcí** | 28 | 240 | ❌ **KRITICKÁ CHYBA** (+212 falešných) |
| **Entry point** | ScriptMain @ IP 9054 | Chybí! | ❌ **KRITICKÁ CHYBA** |
| **Instrukce** | 10,051 | 10,051 | ✅ OK |
| **XFN funkce** | 97 | 97 | ✅ OK |

### Závažnost Problémů

- **P0 - Blocker**: Detekce hranic funkcí zcela selhává (240 vs 28 funkcí)
- **P1 - Critical**: ScriptMain není detekován jako entry point
- **P1 - Critical**: Duplicitní názvy parametrů ve všech funkcích
- **P2 - Major**: Nedosažitelný kód po return statements
- **P2 - Major**: Switch/case patterns (analýza vyžaduje najít ScriptMain)

---

## Kategorie 1: Kritická Chyba - Detekce Hranic Funkcí

### Problém #1A: Explozi​vní Počet Funkcí (240 vs 28)

**Severity**: 🔴 **P0 - BLOCKER**

**Symptom**:
- Dekompilátor vytváří **240 funkcí** místo skutečných **28 funkcí**
- To znamená **+212 falešných funkcí** (850% false positive rate!)

**Root Cause Hypothesis**:
Dekompilátor pravděpodobně vytváří novou funkci pro **každý blok kódu** místo detekce skutečných hranic funkcí podle:
- CALL target addresses
- RET instruction boundaries
- Entry point markers

**Dopad**:
- Kompletně nečitelný výstup
- Nemožné určit strukturu programu
- Znemožňuje recompilation testing
- Blokuje všechny další analýzy

**Evidence**:
```
LEVEL_new_decompiled.c: Lines 1-2:
// Functions: 240

grep -c "^int func_" LEVEL_new_decompiled.c
→ 207 functions

LEVEL_info.txt: Lines 123-125:
--- Save Info ---
Items: 28
```

Skutečný počet funkcí je **28** (ze Save Info), ne 240!

**Trasování do kódu**:
- **Soubor**: `vcdecomp/core/disasm/disassembler.py`
- **Funkce**: `_analyze_labels()` (lines 58-131)
- **Problém**:
  - Řádky 82-84: Vytváří funkce pouze z `call_targets`
  - Nechybí logika pro **detekci skutečných hranic** funkcí
  - Možná vytváří funkce z **label targets** (JMP cíle) místo jen CALL targets

### Problém #1B: Chybějící ScriptMain Entry Point

**Severity**: 🔴 **P0 - BLOCKER**

**Symptom**:
```bash
grep -c "^int ScriptMain" LEVEL_new_decompiled.c
→ 0  # CHYBÍ!
```

**Očekáváno**:
```c
int ScriptMain(s_SC_L_info *info) {
    // Entry point @ IP 9054
    ...
}
```

**Aktuálně**:
Funkce ScriptMain není vůbec generována, pravděpodobně je rozdělena na multiple `func_XXXX` funkce.

**Root Cause**:
- **Soubor**: `vcdecomp/core/disasm/disassembler.py`
- **Funkce**: `_analyze_labels()` (lines 86-123)
- **Problém**:
  - Řádky 86-88: Detekuje ScriptMain z `header.enter_ip`
  - Ale enter_ip = 9054 je pravděpodobně **uvnitř jiné funkce** podle současné (špatné) detekce
  - Funkce na IP 9054 je pojmenována jako `func_9054` místo `ScriptMain`

---

## Kategorie 2: Chyby Function Signatures

### Problém #2A: Duplicitní Názvy Parametrů

**Severity**: 🔴 **P1 - CRITICAL**

**Symptom**:
Všechny funkce s více parametry mají duplicitní názvy `int param, int param, int param` místo `param_0, param_1, param_2`.

**Evidence**:
```c
LEVEL_new_decompiled.c:67
int func_0354(int param, int param, int param) {
                     ^^^^^^       ^^^^^^       ^^^^^^
```

```c
LEVEL_new_decompiled.c:80
int func_0365(int param, int param, int param) {
```

```c
LEVEL_new_decompiled.c:87
int func_0371(int param, int param) {
```

**Očekáváno**:
```c
int func_0354(int param_0, int param_1, int param_2) {
```

**Root Cause**:
- **Soubor**: `vcdecomp/core/ir/function_signature.py`
- **Funkce**: `detect_function_signature()` (lines 43-80)
- **Problém**:
  - Řádek 38: Fallback kód generuje `"int param{i}"` ale **bez subscript indexu**
  - Mělo by být `f"int param_{i}"` nebo `f"int param{i}"`
  - Aktuálně vrací stejný string `"int param"` pro všechny parametry

**Oprava**:
```python
# Současný kód (řádek 38):
params = ", ".join([f"int param{i}" for i in range(self.param_count)])

# Mělo by být:
params = ", ".join([f"int param_{i}" for i in range(self.param_count)])
```

---

## Kategorie 3: Nedosažitelný Kód (Dead Code)

### Problém #3A: Multiple Return Statements v Sekvenci

**Severity**: 🟡 **P2 - MAJOR**

**Symptom**:
Funkce obsahují více `return` statements v řadě, což je nedosažitelný kód.

**Evidence**:
```c
LEVEL_new_decompiled.c:67-78
int func_0354(int param, int param, int param) {
    int idx;  // Auto-generated

    if (!param_2) {
        SC_P_ScriptMessage(param_2, param, idx);
        return FALSE;  // <-- První return
    } else {
        SC_Log(3, "Message %d %d to unexisted player!", param, param_0);
        return FALSE;  // <-- Druhý return
    }
    return;  // <-- TŘETÍ RETURN - NEDOSAŽITELNÝ!
}
```

```c
LEVEL_new_decompiled.c:94-100
    if (!local_0) {
        return FALSE;
    } else {
        SC_P_GetBySideGroupMember(1, param_2, param);
        SC_P_Ai_GetDanger(local_1);
        return FALSE;  // <-- Return v else
        return FALSE;  // <-- DUPLIKÁT - NEDOSAŽITELNÝ!
    }
```

**Root Cause**:
- **Soubor**: `vcdecomp/core/ir/structure/orchestrator.py`
- **Funkce**: `format_structured_function_named()` nebo `_format_block_lines()`
- **Problém**:
  - Nefiltruje nedosažitelný kód po return
  - Emituje všechny bloky i když jsou nedosažitelné

**Očekáváno**:
```c
int func_0354(int param_0, int param_1, int param_2) {
    if (!param_2) {
        SC_P_ScriptMessage(param_2, param_1, param_0);
    } else {
        SC_Log(3, "Message %d %d to unexisted player!", param_1, param_0);
    }
    return FALSE;  // <-- Jeden unified return
}
```

---

## Kategorie 4: Control Flow Patterns (Vyžaduje Opravu Funkcí)

**Status**: ⏸️ **BLOKOVÁNO**

Analýza switch/case patterns v ScriptMain není možná, dokud není opravena detekce hranic funkcí (#1A, #1B).

**Důvod**:
- ScriptMain není detekován jako samostatná funkce
- Pravděpodobně je rozdělen na multiple `func_XXXX` funkce
- Nelze analyzovat switch structure bez správné funkce

**Akce**:
Po opravě Problému #1A a #1B:
1. Najít ScriptMain @ IP 9054
2. Analyzovat switch/case pokrytí
3. Identifikovat chybějící cases (case 2, case 4 z předchozí analýzy)

---

## Kategorie 5: Variable Naming Issues

### Problém #5A: Auto-generated Comments

**Severity**: 🟢 **P3 - MINOR**

**Symptom**:
Mnoho proměnných má komentář `// Auto-generated` místo smysluplných názvů.

**Evidence**:
```c
LEVEL_new_decompiled.c:47-48
int func_0313(int param) {
    int idx;  // Auto-generated
```

**Očekáváno**:
Buď odvozené názvy (např. `player_id`, `target`, `result`) nebo číslované (`local_0`, `local_1`).

**Root Cause**:
- **Soubor**: `vcdecomp/core/ir/variable_renaming.py`
- **Problém**: Generuje placeholder názvy `idx`, `j`, `local_0` s komentářem `// Auto-generated`

**Dopad**: Nízký (kosmetické), ale snižuje čitelnost.

---

## Souhrn Priorit Oprav

### P0 - Kritické (BLOKUJÍ všechno ostatní)

1. **[#1A] Opravit detekci hranic funkcí** → Snížit 240 na 28 funkcí
   - Soubor: `vcdecomp/core/disasm/disassembler.py`
   - Funkce: `_analyze_labels()`
   - Akce: Přehodnotit logiku vytváření funkcí, používat **pouze CALL targety + RET boundaries**

2. **[#1B] Opravit detekci ScriptMain** → Najít entry point @ IP 9054
   - Soubor: `vcdecomp/core/disasm/disassembler.py`
   - Funkce: `_analyze_labels()` (lines 86-123)
   - Akce: Zajistit že funkce s `enter_ip` je pojmenována ScriptMain

### P1 - Vysoká

3. **[#2A] Opravit duplicitní názvy parametrů** → `param` → `param_0`, `param_1`
   - Soubor: `vcdecomp/core/ir/function_signature.py`
   - Funkce: `FunctionSignature.to_c_signature()` (line 28-40)
   - Akce: Přidat index do parametru names (`param_{i}`)

### P2 - Střední

4. **[#3A] Filtrovat nedosažitelný kód** → Odstranit multiple returns
   - Soubor: `vcdecomp/core/ir/structure/orchestrator.py`
   - Funkce: `format_structured_function_named()` nebo dead code analysis
   - Akce: Detekovat nedosažitelné bloky po return/unconditional jump

### P3 - Nízká

5. **[#5A] Vylepšit naming proměnných** → Smysluplnější názvy
   - Soubor: `vcdecomp/core/ir/variable_renaming.py`
   - Akce: Inference z usage patterns

---

## Next Steps

1. **Okamžitě**: Opravit #1A (hranice funkcí) - blokuje vše ostatní
2. **Poté**: Opravit #1B (ScriptMain detection)
3. **Poté**: Opravit #2A (parameter names) - jednoduché, vysoký impact
4. **Poté**: Analyzovat control flow patterns v ScriptMain
5. **Poté**: Opravit #3A (dead code filtering)
6. **Volitelné**: #5A (variable naming improvements)

---

## Test Commands

```bash
# Po každé opravě - regenerovat dekompilaci
py -m vcdecomp structure decompilation/TUNNELS01/SCRIPTS/LEVEL.SCR > LEVEL_test.c

# Spočítat funkce
grep -c "^int func_" LEVEL_test.c
grep -c "^int ScriptMain" LEVEL_test.c
# Expected: 27 func_* + 1 ScriptMain = 28 total

# Zkontrolovat parameter names
grep "int param, int param" LEVEL_test.c
# Expected: no matches

# Regression test
pytest vcdecomp/tests/ -v
```
