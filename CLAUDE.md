# Základní prompt pro Claude agenty - VC Script Decompiler

## Co je tento projekt?
**VC-Script-Decompiler** je nástroj pro dekompilaci zkompilovaných skriptů (.SCR) hry Vietcong (2003) zpět do původního C-like zdrojového kódu. Skripty používají proprietární jazyk podobný C s externími funkcemi pro interakci s herním enginem.


## Kompilační řetězec (originální nástroje Pterodon)
Kompilace probíhá ve 4 krocích:
```
.c → [SCMP] → [SPP] → [SCC] → [SASM] → .scr
```

1. **SPP.exe** - Preprocesor (zpracovává #include, #define, makra)
   - Vstup: .c → Výstup: spp.c (předzpracovaný kód)
2. **SCC.exe** - Kompilátor (překládá C kód na assembler)
   - Vstup: spp.c → Výstup: sasm.sca (textový assembler)
3. **SASM.exe** - Assembler (převádí na binární bytecode)
   - Vstup: sasm.sca → Výstup: .scr (finální bytecode)
4. **SCMP.exe** - Orchestrátor (řídí celý proces)

## Struktura .SCR souboru
```
1. Header - entry point, parametry
2. Data segment - konstanty, stringy (4-byte aligned)
3. Global pointers - offsety globálních proměnných
4. Code segment - instrukce (12 bajtů každá: opcode + 2 argumenty)
5. XFN tabulka - externí funkce (28 bajtů/záznam)
```

## Instrukční sada (150 opcodes)
- **Aritmetika**: ADD, SUB, MUL, DIV, MOD, NEG, INC, DEC
- **Typy**: C=char, S=short, I=int, F=float, D=double (prefix)
- **Skoky**: JMP, JZ, JNZ, CALL, RET, XCALL (externí volání)
- **Stack**: PUSH, POP, ASP, SSP, LCP, GCP, LLD, GLD
- **Konverze**: CTOI, ITOF, FTOD, atd.
- **Bitové**: LS, RS, BA, BX, BO, BN

## Struktura projektu

### Důležité složky:
- **docs/** - Technická dokumentace (ČTĚTE NEJDŘÍVE!)
  - `SPP_TECHNICAL.md` - Analýza preprocesoru
  - `SCC_TECHNICAL_ANALYSIS.md` - Analýza kompilátoru
  - `SASM_TECHNICAL_ANALYSIS.md` - Analýza assembleru
  - `Scripting_SDK.txt` - Oficiální SDK (380KB!)

- **original-resources/** - Originální nástroje a hlavičky
  - `compiler/` - EXE soubory (spp.exe, scc.exe, sasm.exe, scmp.exe)
  - `h/` - Hlavní hlavičky (sc_global.h, sc_def.h)
  - `inc/` - Include soubory (us_equips.inc, vc_equips.inc)

- **Compiler-testruns/** - Testovací kompilace
  - Obsahuje .c zdrojové kódy a jejich .scr výstupy
  - Meziprodukty kompilace (.sca, .syn, .dbg)

- **script-folders/** - Kompletní herní mise
  - Desítky .SCR souborů tvořících funkční celky
  - Někdy obsahují zapomenuté .H soubory

- **vcdecomp/** - Plánovaný Python dekompilátor (ZAČÍNÁME OD ZAČÁTKU!)
  - Bude obsahovat moduly pro dekompilaci
  - Struktura bude navržena na základě dokumentace

### Klíčové soubory:
- `sc_global.h` - Hlavní hlavička s definicemi engine funkcí
- `sc_def.h` - Základní definice a konstanty

## Skriptovací jazyk Vietcong

### Syntaxe:
- C-like jazyk s preprocesorem
- Typy: void, char, short, int, float, double, string
- Struktury, ukazatele, pole
- Externí funkce s prefixem SC_*

### Příklady externích funkcí:
```c
SC_P_Create(name, side);           // Vytvoření hráče
SC_NOD_Get(name);                   // Získání objektu
SC_SND_PlaySound3D(sound, pos);     // 3D zvuk
SC_message(text);                   // Debug výpis
SC_GameMessage(player, text);       // Zpráva hráči
```

## Aktuální stav projektu

### Dokumentace (HOTOVO):
- ✅ Kompletní dokumentace kompilačního řetězce (tisíce řádků analýz!)
- ✅ Reverse engineering všech 4 nástrojů (SPP, SCC, SASM, SCMP)
- ✅ Mapování všech 150 opcodes a instrukcí
- ✅ Pochopení formátu .SCR a všech jeho sekcí
- ✅ Analýza datových struktur a algoritmů kompilátoru



### TODO - Implementace dekompilátoru:
- ❌ Návrh architektury dekompilátoru
- ❌ Loader pro .SCR soubory
- ❌ IR (Intermediate Representation) systém
- ❌ Rekonstrukce výrazů a příkazů
- ❌ Rekonstrukce vysokoúrovňových konstrukcí (if/else, switch/case, cykly)
- ❌ Type inference (určení typů z instrukcí)
- ❌ Mapování XFN funkcí na prototypy
- ❌ Rekonstrukce původních maker
- ❌ Optimalizace redundantního kódu
- ❌ GUI pro dekompilátor
- ❌ Testy pro všechny instrukce

## Dostupné nástroje

1. **IDA Pro** - Připojitelný přes MCP server
   - Pro analýzu kompilátorů nebo engine
   - Vyžádejte si připojení: "připoj ida-pro-mcp"

2. **Originální kompilátory** - V original-resources/compiler/
   - Pro testování a ověření dekompilace
   - Lze spustit přes SCMP.exe pro kompilaci testovacích skriptů

## Jak pracovat s projektem

### Pro analýzu:
1. Přečtěte dokumentaci v docs/
2. Prostudujte testovací běhy v Compiler-testruns/
3. Podívejte se na příklady skriptů v script-folders/

### Pro vývoj dekompilátoru:
1. Začněte s návrhem architektury na základě dokumentace
2. Implementujte loader pro .SCR soubory jako první krok
3. Testujte na jednoduchých skriptech z Compiler-testruns/
4. Postupně přidávejte funkcionality podle TODO listu

### Pro reverse engineering:
1. Použijte IDA Pro přes MCP
2. Analyzujte .exe soubory v original-resources/compiler/
3. Dokumentujte nové nálezy

## Technické výzvy

1. **Switch/case rekonstrukce** - Kompilátor generuje jump tabulky
2. **Type inference** - Určení typů z instrukcí (CMUL vs FMUL)
3. **Makra** - Jsou expandována preprocesorem, těžko rekonstruovatelná
4. **Optimalizace** - Kompilátor generuje redundantní kód
5. **XFN mapování** - 700+ externích funkcí, ne všechny zdokumentované

## Důležité poznámky

- Projekt používá little-endian formát
- Všechny offsety v datech jsou 4-byte aligned
- Instrukce jsou vždy 12 bajtů (opcode + 2x int argument)
- Stringy v data segmentu jsou null-terminated
- Stack roste směrem dolů (jako x86)

## Kontakt a zdroje

- Git repozitář obsahuje veškerou dokumentaci
- Pro hlubší analýzu použijte IDA Pro
- SDK dokumentace je v docs/Scripting_SDK.txt





### Instrukce pro dekompilaci skriptů
Instrukce pro workflow dekompilace je v docs/decompilation_guide.md
Oficiální SDK je v docs/Scripting_SDK.txt
Hlavičkové soubory (některé byly vždy použity ke kompilaci) jsou k nahlédnutí v compiler/inc


---
*Tento dokument je základním vstupním bodem pro Claude agenty pracující na VC-Script-Decompiler projektu.*