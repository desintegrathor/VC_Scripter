# VC-Script-Decompiler

Dekompilátor pro Vietcong (2003) game scripty. Převádí zkompilované `.scr` soubory (bytecode) zpět na čitelný C-like zdrojový kód.

## Základní použití

Dekompilátor je primárně **nástroj pro příkazovou řádku**. GUI je dostupné pouze pro základní náhled, ale není určené pro produkční použití.

### Dekompilace jednoho souboru

```bash
py -3 -m vcdecomp structure script.scr > output.c
```

### Dekompilace celé složky

Pro dekompilaci všech `.scr` souborů ve složce použijte standardní shell nástroje:

**Windows (PowerShell):**
```powershell
# Dekompilace všech .scr souborů v aktuální složce
Get-ChildItem *.scr | ForEach-Object {
    py -3 -m vcdecomp structure $_.FullName > "$($_.BaseName)_decompiled.c"
}

# Rekurzivně včetně podsložek
Get-ChildItem -Recurse *.scr | ForEach-Object {
    py -3 -m vcdecomp structure $_.FullName > "$($_.DirectoryName)\$($_.BaseName)_decompiled.c"
}
```

**Linux/WSL (Bash):**
```bash
# Dekompilace všech .scr souborů v aktuální složce
for file in *.scr; do
    py -3 -m vcdecomp structure "$file" > "${file%.scr}_decompiled.c"
done

# Rekurzivně včetně podsložek
find . -name "*.scr" -exec sh -c 'py -3 -m vcdecomp structure "$1" > "${1%.scr}_decompiled.c"' _ {} \;
```

## Dekompilace s dostupnou hlavičkou (SDK)

Dekompilátor automaticky používá informace z Vietcong SDK, které obsahuje signatury externích funkcí (`SC_*`). SDK data jsou součástí projektu v `vcdecomp/sdk/data/functions.json`.

### Co SDK poskytuje:
- **Názvy parametrů** externích funkcí (např. `SC_P_Create(string name, vector pos)`)
- **Typy parametrů** (int, float, string, vector, entity, ...)
- **Návratové typy** funkcí
- **Počty parametrů** pro všechny `SC_*` funkce

### Aktualizace SDK z nových scriptů

Pokud máte nové skripty, které volají dosud neznámé externí funkce, můžete SDK aktualizovat:

```bash
# Skenování složky se skripty a agregace všech XFN volání
py -3 -m vcdecomp xfn-aggregate scripts/ --format summary

# Export agregovaných signatur do SDK formátu
py -3 -m vcdecomp xfn-aggregate scripts/ --format sdk -o new_functions.json

# Sloučení s existujícím SDK
py -3 -m vcdecomp xfn-aggregate scripts/ --format sdk -o merged.json --merge-sdk
```

**Co se stane:**
1. Dekompilátor projde všechny `.scr` soubory v zadané složce
2. Extrahuje XFN tabulky (externí funkce) a jejich volání
3. Analyzuje počet předávaných parametrů
4. Vytvoří nebo aktualizuje seznam známých funkcí

**Poznámka:** SDK neobsahuje implementaci funkcí (ta je v enginu hry), pouze signatury pro lepší dekompilaci.

## Pokročilé možnosti

### Režimy dekompilace

```bash
# Ghidra-style hierarchické strukturování (výchozí, nejlepší kvalita)
py -3 -m vcdecomp structure script.scr > output.c

# Plochý režim (rychlejší, nižší kvalita)
py -3 -m vcdecomp structure --no-collapse script.scr > output.c

# Ladící výstup (pro diagnostiku problémů)
py -3 -m vcdecomp structure --debug script.scr > output.c 2> debug.log
```

### SSA režimy

```bash
# Incremental Heritage SSA (výchozí, vyšší kvalita)
py -3 -m vcdecomp structure script.scr > output.c

# Legacy SSA (rychlejší, ale méně přesné)
py -3 -m vcdecomp structure --legacy-ssa script.scr > output.c
```

### Informace o scriptu

```bash
# Zobrazit metadata (entry point, velikost, počet instrukcí)
py -3 -m vcdecomp info script.scr

# Disassembly (čitelný assembler)
py -3 -m vcdecomp disasm script.scr > output.asm

# Export globálních proměnných
py -3 -m vcdecomp symbols script.scr -o globals.json -f json
```

## GUI (pouze pro náhled)

GUI verze je **experimentální** a není určená pro produkční použití:

```bash
py -3 -m vcdecomp gui [script.scr]
```

**Omezení GUI:**
- Pomalejší než CLI
- Nedovoluje batch processing
- Neumožňuje pokročilé flagy
- Žádná podpora pro automatizaci

**Pro vážné použití vždy preferujte CLI.**

## Příklad workflow

```bash
# 1. Zjistit informace o scriptu
py -3 -m vcdecomp info mission01/LEVEL.SCR

# 2. Dekompilovat s debug výstupem
py -3 -m vcdecomp structure --debug mission01/LEVEL.SCR > LEVEL.c 2> LEVEL_debug.log

# 3. Pokud je výstup špatný, zkusit flat mode
py -3 -m vcdecomp structure --no-collapse mission01/LEVEL.SCR > LEVEL_flat.c

# 4. Agregovat XFN z celé mise
py -3 -m vcdecomp xfn-aggregate mission01/ --format summary
```

## Technické detaily

### Architektura .SCR souboru
- **Header:** Entry point, počet parametrů funkce
- **Data segment:** Konstanty, stringy (4-byte aligned, little-endian)
- **Code segment:** Instrukce (12 bajtů: opcode + 2× int32 argumenty)
- **XFN tabulka:** Externí funkce (28 bajtů/záznam)

### Instruction set
- ~150 opcodes (aritmetika, control flow, stack operace)
- Type prefixy: `C`=char, `S`=short, `I`=int, `F`=float, `D`=double
- Příklady: `IADD`, `FADD`, `PUSH`, `POP`, `JZ`, `XCALL`

### Externí funkce (SC_*)
Skripty volají 700+ engine funkcí s prefixem `SC_`:
- `SC_P_Create()` - Vytvoření hráče
- `SC_NOD_Get()` - Získání objektu
- `SC_message()` - Debug zpráva
- Kompletní seznam v `vcdecomp/sdk/data/functions.json`

## Dokumentace

- `CLAUDE.md` - Návod pro AI asistenty (kompletní reference)
- `docs/decompilation_guide.md` - Podrobný průvodce dekompilací
- `vcdecomp/core/ir/structure/README.md` - Architektura strukturálního modulu
- `vcdecomp/data/Scripting_SDK.md` - Oficiální Vietcong SDK dokumentace

## Testování

```bash
# Spustit všechny testy
py -3 -m pytest vcdecomp/tests/ -v

# Test konkrétního modulu
py -3 -m pytest vcdecomp/tests/test_structure_patterns.py -v

# End-to-end testy (kompletní dekompilace)
py -3 -m pytest vcdecomp/tests/test_end_to_end_decompilation.py -v
```

Testovací skripty s originálním zdrojovým kódem: `decompiler_source_tests/`

## Známá omezení

1. **Typy proměnných** - Ne vždy lze správně odvodit typ (zůstávají jako `dword`)
2. **Makra** - Originální makra jsou ztracena (preprocessor je expandoval)
3. **Globální proměnné** - Detekce je heuristická, může být nepřesná
4. **Komplexní smyčky** - U složitých control flow může být tělo smyčky neúplné

## Licence

Interní nástroj pro rekonstrukci Vietcong skriptů.
