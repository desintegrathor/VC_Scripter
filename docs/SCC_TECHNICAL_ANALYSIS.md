# SCC.EXE - Technická analýza kompilátoru

## Přehled

SCC.exe je třetí část kompilačního řetězce pro Vietcong skripty. Překládá preprocessovaný C-like kód (`.spp`) na assemblerový mezikód (`.sca`).

**Základní informace:**
- MD5: `8be57d8a06cd18dfd156cdd9094b2c1d`
- SHA256: `96daa829b23b9ca34b543b5cf0616c617c7f86baa749c03bcfc054915b818790`
- Velikost: 0x35000 bajtů
- Báze: 0x400000

## Architektura kompilátoru

### 1. Hlavní komponenty

#### WinMain (0x40BE00)
Hlavní vstupní bod s následujícím workflow:

1. **Parsování argumentů**
   - Očekává 4-5 argumentů
   - `argv[1]`: vstupní `.spp` soubor
   - `argv[2]`: výstupní `.sca` soubor
   - `argv[3]`: dočasný header soubor (smazán po kompilaci)
   - `argv[4]`: volitelné "dbg" pro debug mód

2. **Inicializace**
   - Otevření debug logu `scc.dbg`
   - Načtení vstupního souboru

3. **Kompilační fáze**
   - `sub_40C0A0()`: Parser a lexer - vytvoření IR
   - `sub_409B10()`: Generování `.sca` struktury
   - `sub_414470()`: Debug výpis generovaného kódu
   - `sub_401DF0()`: Vytvoření `.sd_` debug souboru (pokud dbg=1)

4. **Finalizace**
   - Vytvoření synchronizačního souboru `scc.syn`

### 2. Internal Representation (IR)

#### Hlavní IR struktura (0x4385A0)
Centrální datová struktura obsahující kompletní reprezentaci programu.

#### Typy symbolů (a1[1] v sub_404540)
- **0**: Neznámý/neplatný symbol
- **1**: Proměnná/data
- **2**: Funkce/procedura
- **5**: Jump label

#### Typy proměnných (a1[8])
- **20 (0x14)**: Globální proměnná
- **21 (0x15)**: Statická proměnná
- **22 (0x16)**: Externí proměnná/funkce

#### Datové typy (pro sub_41BC70)
- **0**: Neplatný typ
- **1**: void/žádný typ
- **2**: char (1 bajt, signed)
- **3**: unsigned char (1 bajt)
- **4**: short (2 bajty, signed)
- **5**: unsigned short (2 bajty)
- **6**: int (4 bajty, signed)
- **7**: unsigned int (4 bajty)
- **8**: long (4 bajty, signed)
- **9**: unsigned long (4 bajty)
- **10 (0x0A)**: float (4 bajty)
- **11 (0x0B)**: double (8 bajtů)
- **12 (0x0C)**: string/char*
- **13 (0x0D)**: pole/array
- **16 (0x10)**: struktura
- **17 (0x11)**: union
- **18 (0x12)**: speciální typ

### 3. Generátory kódu

#### sub_4098C0 - Hlavní generátor
Iteruje přes IR uzly a volá specifické generátory podle typu uzlu.

#### sub_404540 - Generátor funkcí (Detailní analýza)
Největší a nejkomplexnější funkce kompilátoru (0x103A bajtů = 4154 bajtů!).

**Zpracování různých typů symbolů** (`switch(a1[1])`):

**Case 0 - Neznámý symbol:**
- Vyvolá chybu "translateSymbol() - unknown symbol type"

**Case 1 - Globální/statické proměnné:**
- Generuje `$name=offset` pro proměnnou
- Pro typ 20 (globální): generuje kompletní inicializaci
- Pro typ 21 (statická): zapisuje do `sav_file.scc`
- Pro typ 22 (externí): pouze deklarace

**Case 2 - Definice funkcí:**
Nejsložitější část - zpracování kompletních funkcí:

1. **Rozpoznání speciálních funkcí:**
   - `ScriptMain` - vstupní bod programu
   - Externí funkce (typ 22) - generuje XFN instrukce

2. **Generování hlavičky funkce:**
   ```asm
   @function_name        ; function 'name'
   IN N                  ; vstupní parametry
   OUT M                 ; výstupní hodnoty
   ```

3. **Alokace parametrů:**
   - Iteruje přes parametry v IR
   - Pro každý parametr generuje: `$param=offset ; parameter 'name'`
   - Stack offset začíná na -2, každý parametr posune o -(velikost/4)

4. **Generování návratové proměnné:**
   - Pokud funkce vrací hodnotu: `$return=offset ; return variable`

5. **Zpracování lokálních proměnných:**
   - Detekce neznámých typů proměnných
   - Kontrola varargs funkcí (`sub_4029B0`)

6. **Generování těla funkce:**
   - Volá `sub_404470()` pro generování instrukcí těla

7. **Generování epilogu:**
   - Pro funkce s explicitním return: `RET N`
   - Kontrola, zda všechny cesty vrací hodnotu
   - Debug informace o řádcích zdrojového kódu

**Speciální zpracování ScriptMain:**
```asm
IN 0/1              ; podle parametrů
OUT 0/1             ; podle návratového typu
```
Generuje také komentáře do header souboru s prototypem.

**Externí funkce (XFN):**
Pro externí funkce generuje speciální XFN záznam:
```
XFN "name(params)" param_count return_size byte_size flags
$name=id
```
Zapisuje také `#define` do header souboru.

**Case 5 - Jump labely:**
- Generuje: `@label ; jump label 'name'`
- Automaticky přiřazuje jméno pokud chybí

#### sub_403360 - Generátor globálních přístupů
Zpracovává přístupy ke globálním proměnným a konstantám:
- Typy 0x0D, 0x10, 0x11: speciální handlery pro string/float/int
- Generuje sekvenci: `_ldb`, `GADR <global>`, operace, `_lde`

#### sub_403750 - Stack alokátor
Generuje instrukce pro alokaci místa na stacku:
- Typy 2-8: `ASP 1` (1 slovo)
- Typ 9: `ASP 2` (2 slova)
- Typ 16: dynamická alokace podle velikosti

#### sub_402DA0 - Generátor datových operací
Zpracovává různé datové typy:
- Numerické typy (2-9): int8, uint8, int16, uint16, int32, uint32
- Typ 10 (0x0A): float
- Typ 11 (0x0B): double
- Typ 12 (0x0C): string

#### sub_4029D0 - Generátor literálů
Převádí konstanty na assemblerové instrukce:
- `?0xNc`: char literál
- `?0xNs`: short literál
- `?0xNi`: int literál
- `?Nf`: float literál
- `?Nd`: double literál
- `?string`: string literál s escape sekvencemi

## Instrukční sada

### Stack Management
- `ASP N` - Alokace N slov na stacku (Allocate Stack Pointer)
- `SSP N` - Dealokace N slov ze stacku (Subtract Stack Pointer)

### Data Operations
- `?#N` - Rezervace N bajtů v datovém segmentu
- `_ldb` - Začátek načítání dat (Load Begin)
- `_lde` - Konec načítání dat (Load End)
- `GADR <name>` - Načtení adresy globální proměnné
- `DLD N` - Načtení N bajtů dat (Data Load)
- `DCP` - Kopírování dat (Data Copy)

### Control Flow
- `CALL <label>` - Volání lokální funkce
- `XCALL <id>` - Volání externí funkce
- `RET N` - Návrat z funkce s N slovy na stacku
- `JZ/JNZ` - Podmíněné skoky

### Funkce a proměnné
- `IN N` - Deklarace N vstupních parametrů
- `OUT N` - Deklarace N výstupních hodnot
- `$name=offset` - Definice proměnné/labelu

## Globální proměnné kompilátoru

| Adresa | Název | Účel |
|--------|-------|------|
| 0x438210 | dword_438210 | Handle výstupního `.sca` souboru |
| 0x438214 | dword_438214 | Handle header souboru |
| 0x438218 | dword_438218 | Handle `sav_file.scc` |
| 0x43821C | dword_43821C | Pointer na hlavní IR strukturu |
| 0x438220 | dword_438220 | Aktuální index v IR |
| 0x438228 | dword_438228 | Offset v kódovém segmentu |
| 0x43822C | dword_43822C | Return proměnná |
| 0x438234 | dword_438234 | Offset v datovém segmentu |
| 0x438238 | dword_438238 | Kontext lokálních proměnných |
| 0x438260 | dword_438260 | Čítač externích funkcí |

## Výstupní formáty

### .sca soubor (Script Assembler)
Textový assemblerový soubor s instrukcemi ve formátu:
```
; This script assembler code was produced from
; script C source code by using 'scc.exe' script ANSI C compiler.

@function_name      ; function 'name'
    IN 1            ; vstupní parametry
    OUT 0           ; výstupní hodnoty
    $var=offset     ; lokální proměnné
    ASP 2           ; alokace stacku
    ...instrukce...
    RET 0           ; návrat
```

### .sd_ soubor (Debug info)
Binární soubor generovaný funkcí `sub_401DF0` obsahující:
- Header (52 bajtů)
- Seznam struktur (16 bajtů každá)
- Datový segment
- Kódový segment
- Tabulka externích funkcí
- SAV informace

### sav_file.scc
Mezisoubor obsahující dodatečné informace pro další fáze kompilace.

## Chybové hlášky

Kompilátor generuje různé chybové hlášky pro diagnostiku:
- `"send me input .C file and output .SCA file and output .H file."` - špatný počet parametrů
- `"cannot open input file."` - nelze otevřít vstupní soubor
- `"translateSymbol() - unknown symbol type."` - neznámý typ symbolu v IR
- `"initializer type mismatch."` - nesoulad typů při inicializaci
- `"unknown variable type."` - neznámý typ proměnné
- `"string illegal escape."` - neplatná escape sekvence v řetězci
- `"not all paths returns value."` - ne všechny cesty funkcí vrací hodnotu

## Optimalizace a speciality

1. **Zarovnání dat**: Všechna data jsou zarovnána na 4-bajtové hranice
2. **Stack slots**: Stack je organizován po slovech (4 bajty)
3. **Escape sekvence**: Podporované: `\n`, `\r`, `\t`, `\f`, `\v`, `\\`
4. **Debug symboly**: Generovány pouze s parametrem `dbg`

## Stack Frame Management

Analýza `sub_404540` odhaluje přesnou organizaci stack frame:

### Offset Layout
```
-N    ... lokální proměnné (rostou směrem dolů)
-2    ... první parametr
-3    ... druhý parametr
...
0     ... stack base
+1    ... return address
```

### Pravidla alokace:
- Parametry začínají na offsetu **-2**
- Každý parametr zabírá `(size + 3) / 4` slov
- Návratová hodnota (pokud existuje) je alokována před parametry
- Lokální proměnné jsou alokovány dynamicky během generování těla

### Speciální případy:
- **Varargs funkce** - detekované pomocí `sub_4029B0`
- **Externí funkce** - generují XFN instrukce místo normálního kódu
- **ScriptMain** - speciální handling vstupního bodu

## Doporučení pro dekompilátor

Pro správnou dekompilaci je potřeba:

1. **Parsovat .sca formát** - textový assembler s instrukcemi
2. **Rekonstruovat typy** z ASP/SSP instrukcí a datových operací
   - ASP 1 = char/short/int/float
   - ASP 2 = double
   - ASP N = struktura/pole
3. **Sledovat stack frame** - IN/OUT parametry a lokální proměnné
   - Offsety začínají na -2 pro parametry
   - Lokální proměnné rostou směrem dolů
4. **Mapovat externí funkce** přes XFN instrukce
   - Parsovat signaturu funkce z XFN záznamu
   - Mapovat na známé externí funkce
5. **Rekonstruovat řídící tok** z jump instrukcí a labelů
   - @ prefixuje všechny labely a funkce
   - JZ/JNZ pro podmíněné skoky
6. **Dekódovat literály** z ? instrukcí zpět na původní hodnoty
   - ?0xNc = char, ?0xNs = short, ?0xNi = int
   - ?Nf = float, ?Nd = double
   - ?string = řetězec s escape sekvencemi

## Závěr

SCC.exe je dobře strukturovaný kompilátor s jasně oddělenými fázemi:
- Lexer/Parser → IR generování
- IR optimalizace
- Code generation → assembler výstup

Použití textového meziformátu (.sca) umožňuje snadné ladění a pochopení generovaného kódu. Pro vytvoření dekompilátoru je klíčové správné pochopení IR struktur a mapování instrukcí zpět na vyšší úroveň abstrakce.