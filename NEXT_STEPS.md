# Další Kroky - VC Script Decompiler

Tento dokument popisuje, čím by se mělo pokračovat po implementaci 4 kritických oprav dekompilátoru.

## Implementované Opravy (2026-01-14)

✅ **FIX #1**: Oprava RET instrukce handling v CFG (`cfg.py`)
✅ **FIX #2**: Oprava mapování stack proměnných (`stack_lifter.py`) - `[sp-3]` → `param_0`
✅ **FIX #3**: Validace deklarací proměnných (`orchestrator.py`) - auto-generování chybějících deklarací
✅ **FIX #4**: Podpora double-precision operací (`expr.py`) - FTOD, DMUL, DADD, atd.

## Hlavní Zbývající Problém: Nedosažitelný Kód po RET

### Popis Problému

Dekompilátor stále generuje nedosažitelný kód po `return` příkazech. Příklad z `LEVEL_decompiled.c`:

```c
int func_0291(int param, int param) {
    tmp = frnd(param);
    if (!(tmp < 0)) {
        tmp = -tmp;
    } else {
        return tmp;
    }
    SC_P_Ai_SetMode(idx, SCM_FEELDANGER);      // NEDOSAŽITELNÉ
    SC_P_Ai_EnableShooting(param_0, SCM_RUN);  // NEDOSAŽITELNÉ
    return FALSE;                               // NEDOSAŽITELNÉ
    SC_P_Ai_SetMode(param_0, SCM_ENABLE);      // NEDOSAŽITELNÉ
    // ... další nedosažitelný kód
}
```

### Příčina

Assembly `LEVEL_disasm.asm` ukazuje, že tyto bloky jsou **ODDĚLENÉ FUNKCE**, ne jedna funkce:

```asm
; FUNKCE 1: adresy 291-312
291: ...
312: RET 0           ; Konec funkce 1

; FUNKCE 2: adresy 313-331
313: ...
331: RET 0           ; Konec funkce 2

; FUNKCE 3: adresy 332-353
332: ...
353: RET 0           ; Konec funkce 3
```

Dekompilátor je však interpretuje jako **jednu funkci s nedosažitelným kódem**.

## Priorita 1: Detekce Hranic Funkcí

### Co Implementovat

**Nový modul**: `vcdecomp/core/ir/function_detector.py`

```python
"""
Detekce hranic funkcí na základě RET instrukcí a call graph analýzy.

Klíčové funkce:
- detect_function_boundaries() - najde všechny funkce v .scr souboru
- split_at_ret_instructions() - rozdělí kód podle RET instrukcí
- validate_function_entry_points() - ověří, že každá funkce má platný entry point
"""
```

### Algoritmus

1. **Najdi všechny RET instrukce** v kódu
2. **Vytvoř kandidáty na funkce**:
   - Každý úsek mezi CALL targety a následným RET je funkce
   - Každý úsek mezi RET a dalším RET (pokud má predecessory) je funkce
3. **Validuj hranice**:
   - Funkce musí mít alespoň jeden predecessor (CALL nebo jump)
   - Funkce nesmí začínat uprostřed basic bloku
4. **Vybuduj funkční mapu**:
   ```python
   {
       "func_0291": (start=291, end=312),
       "func_0313": (start=313, end=331),
       "func_0332": (start=332, end=353),
   }
   ```

### Soubory k Úpravě

**1. `vcdecomp/__main__.py`** (lines ~180-220)
```python
# PŘED:
functions = detect_functions(scr, resolver)

# PO:
from .core.ir.function_detector import detect_function_boundaries_v2
functions = detect_function_boundaries_v2(scr, resolver)
```

**2. `vcdecomp/core/ir/function_signature.py`**
- Aktualizovat `detect_functions()` aby respektovala RET hranice
- Nebo vytvořit novou funkci `detect_functions_v2()`

**3. `vcdecomp/core/ir/structure/orchestrator.py`**
- Upravit `format_structured_function_named()` aby renderovala pouze bloky patřící dané funkci
- Přidat validaci: nesmí renderovat bloky bez predecessorů (orphaned blocks)

### Testovací Strategie

**Test Case 1**: `LEVEL.scr` funkce 291-353
```python
def test_separate_functions_after_ret():
    """Test že RET instrukce správně oddělují funkce"""
    functions = detect_function_boundaries_v2(scr, resolver)

    # Očekávané: 3 samostatné funkce
    assert "func_0291" in functions
    assert functions["func_0291"] == (291, 312)

    assert "func_0313" in functions
    assert functions["func_0313"] == (313, 331)

    assert "func_0332" in functions
    assert functions["func_0332"] == (332, 353)
```

**Test Case 2**: Dekompilovaný výstup nesmí obsahovat nedosažitelný kód
```python
def test_no_unreachable_code_after_ret():
    """Test že po return není nedosažitelný kód"""
    output = decompile_structure(scr)

    lines = output.split('\n')
    for i, line in enumerate(lines):
        if 'return' in line and not line.strip().startswith('//'):
            # Po return nesmí být další kód (kromě komentářů a })
            remaining = lines[i+1:]
            for next_line in remaining:
                stripped = next_line.strip()
                if stripped and stripped != '}' and not stripped.startswith('//'):
                    assert False, f"Unreachable code after return: {next_line}"
                if stripped == '}':
                    break  # Konec funkce je OK
```

## Priorita 2: Oprava Undefined Proměnných

### Zbývající Problémy

I po FIX #2 a FIX #3 jsou stále některé proměnné undefined:

```c
SC_P_Ai_SetMode(idx, SCM_FEELDANGER);           // 'idx' undefined
SC_P_Ai_GetSureEnemies(ai_props.watchfulness);  // 'ai_props' undefined
if (!i.field10) {                                // 'i' undefined
```

### Příčina

1. **`idx`** - Pravděpodobně chyba v parameter mappingu nebo SSA lowering
2. **`ai_props`** - Struktura která nebyla správně detekována
3. **`i`** - SSA temporary která nebyla správně převedena na deklaraci

### Řešení

**Krok 1**: Debug logging pro sledování proměnných
```python
# Přidat do orchestrator.py před renderingem
import logging
logger = logging.getLogger(__name__)

for line in lines:
    # Scan for undefined variables
    matches = re.findall(r'\b([a-zA-Z_]\w*)\b', line)
    for var in matches:
        if var not in declared_vars and needs_declaration(var):
            logger.warning(f"Undefined variable: {var} in line: {line}")
```

**Krok 2**: Rozšířit FIX #3 aby pokryl více případů
```python
# orchestrator.py - rozšířit auto-deklarace
if needs_declaration:
    # Pokus o odvození typu ze způsobu použití
    if '.field' in line and var in line:
        # Struktura - zkus najít typ z usage patterns
        var_type = infer_struct_type_from_usage(var, lines)
    elif var.startswith('idx'):
        var_type = "int"  # Index je obvykle int
    else:
        var_type = "int"  # Default
```

## Priorita 3: Update Regression Baselines

### Proč

FIX #2 změnila naming z `retval` (undefined) na `param_0` (správně). Testy regression selhávají protože baseline obsahuje starý (špatný) výstup.

### Kroky

```bash
# 1. Regeneruj baselines s novými opravami
cd C:\Users\flori\source\repos\VC_Scripter
py -m vcdecomp structure Compiler-testruns/Testrun1/tdm.scr > tests/baselines/tdm_baseline.c
py -m vcdecomp structure Compiler-testruns/Testrun1/hitable.scr > tests/baselines/hitable_baseline.c

# 2. Zkontroluj že nové baselines jsou lepší (méně undefined variables)
grep -c "retval" tests/baselines/tdm_baseline.c  # Mělo by být 0
grep -c "param_" tests/baselines/tdm_baseline.c  # Mělo by být > 0

# 3. Spusť testy znovu
py -m pytest vcdecomp/tests/test_regression_baseline.py -v
```

## Priorita 4: Validace Kompilovatelnosti

### Cíl

Ověřit že dekompilovaný kód lze zkompilovat původním kompilátorem `SCMP.exe`.

### Implementace

```bash
# Test s LEVEL.scr
cd C:\Users\flori\source\repos\VC_Scripter

# 1. Dekompiluj
py -m vcdecomp structure decompilation/TUNNELS01/SCRIPTS/LEVEL.scr > LEVEL_FIXED.c

# 2. Zkompiluj původním kompilátorem
cd original-resources/compiler
./scmp.exe ../../LEVEL_FIXED.c LEVEL_RECOMPILED.scr sc_global.h

# 3. Porovnej bytecode
cd ../..
py -m vcdecomp validate decompilation/TUNNELS01/SCRIPTS/LEVEL.scr LEVEL_RECOMPILED.scr
```

### Očekávané Výsledky

- **Semantic differences**: 0 (chování se musí shodovat)
- **Non-semantic differences**: Přijatelné (jiné alokace registrů, pořadí instrukcí)

## Priorita 5: Oprava Double Operations (Doplnění)

### Zbývající Případy

FIX #4 implementovala základní double operace, ale mohly by chybět edge cases:

1. **DNEG** (double negation) - Je v UNARY_PREFIX ale možná potřebuje speciální handling
2. **Porovnání doubles** (DLES, DLEQ, DGRE, DGEQ, DEQU, DNEQ) - Jsou v INFIX_OPS a měly by fungovat
3. **Double konstanty** - Mohly by se renderovat špatně

### Test

Vytvoř test soubor který používá všechny double operace a zkontroluj výstup:

```c
// test_doubles.c (zkompilovat do .scr)
double test_doubles(double a, double b) {
    double c = (double)1.5;          // FTOD nebo ITOD
    double d = a + b;                // DADD
    double e = a * b;                // DMUL
    double f = a - b;                // DSUB
    double g = a / b;                // DDIV
    double h = -a;                   // DNEG

    if (a > b) return 1.0;           // DGRE
    if (a == b) return 2.0;          // DEQU

    return (float)d;                 // DTOF
}
```

## Časový Plán

### Týden 1 (Priorita 1)
- [ ] Implementovat `function_detector.py`
- [ ] Aktualizovat `__main__.py` aby používal nový detector
- [ ] Napsat testy pro detekci hranic funkcí
- [ ] Testovat na LEVEL.scr

### Týden 2 (Priorita 2-3)
- [ ] Debug undefined variables (`idx`, `ai_props`, `i`)
- [ ] Rozšířit auto-deklarace v orchestrator.py
- [ ] Regenerovat regression baselines
- [ ] Ověřit že všechny testy projdou

### Týden 3 (Priorita 4-5)
- [ ] Implementovat validaci kompilovatelnosti
- [ ] Testovat double operations edge cases
- [ ] Dokumentovat zbývající problémy

## Metriky Úspěchu

Po dokončení všech priorit by měly být splněny tyto podmínky:

✅ **Žádný nedosažitelný kód** - Funkce správně oddělené podle RET instrukcí
✅ **Žádné undefined proměnné** - Všechny proměnné deklarované před použitím
✅ **100% testů projde** - Včetně regression testů s novými baselines
✅ **Kompilovatelný výstup** - Dekompilovaný kód lze zkompilovat SCMP.exe
✅ **Validní bytecode** - Rekompilovaný .scr má shodnou sémantiku s originálem

## Reference

- **Implementační plán**: `C:\Users\flori\.claude\plans\jolly-discovering-stream.md`
- **Analýza chyb**: Provedena Explore agentem (agent ID: acd0269)
- **Test případy**: `decompilation\TUNNELS01\SCRIPTS\LEVEL.scr` (funkce 291-353)
- **Disassembly**: `decompilation\TUNNELS01\SCRIPTS\LEVEL_disasm.asm` (správný referenční výstup)
