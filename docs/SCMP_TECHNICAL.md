# SCMP.EXE - Důkladná technická analýza

## Metadata binárního souboru
- **Cesta**: `vc-script-sdk096\compiler\scmp.exe`
- **Velikost**: 192 KB (0x30000 bajtů)
- **MD5**: `3f7320e96929d56446888a0cab29af09`
- **SHA256**: `e67108a3006b3d94e3c7529b764f7a5236ac71685393f4769bdc3a456582f16f`
- **CRC32**: `0xB5CB4B2E`
- **Base address**: `0x400000`
- **Entry point**: `0x405360` (start)

## Architektura programu

### Hlavní komponenty
1. **Orchestrátor pipeline** - řídí 3-fázovou kompilaci
2. **Správce pracovního adresáře** - dynamicky mění CWD
3. **Parser/Writer .syn/.cmp formátu** - mapování symbolů
4. **Error handler** - vytváří `spp.err` a `vm.syn`

## Detailní analýza funkcí

### WinMain (0x401A70) - Hlavní funkce
**Návratové hodnoty**:
- `0` - úspěch (POZOR: také při chybě WinExec!)
- `-1` - špatný počet parametrů (méně než 4)
- `-2` - chyba v spp.exe
- `-3` - chyba v scc.exe
- `-4` - chyba v sasm.exe

**Logický tok**:
1. Parsuje příkazovou řádku pomocí `sub_401220`
2. Kontroluje počet argumentů (max 5, odmítá 6+)
3. Ukládá původní CWD, přepne na adresář s scmp.exe
4. Maže všechny dočasné soubory před kompilací
5. Spouští 3-fázovou pipeline
6. Na konci vytváří/maže `.cmp` soubor (mapa symbolů)
7. Vždy vytváří prázdný `vm.syn` v původním CWD

### sub_401220 (0x401220) - Parser příkazové řádky
**Implementační detaily**:
- Parsuje `GetCommandLineA()` na jednotlivé argumenty
- Správně zpracovává uvozovky (") - text v uvozovkách = 1 argument
- Odstraňuje trailing whitespace (mezery 0x20 a tabulátory 0x09)
- Vrací: počet argumentů a pole ukazatelů na argumenty
- Alokuje paměť pomocí malloc

### sub_401990 (0x401990) - Spouštění externích programů
**Parametry**:
- `lpCmdLine` - příkazová řádka
- `uCmdShow` - vždy 5 (SW_SHOW)
- `lpFileName` - soubor k čekání/mazání
- `a4` - režim (1=čekej na soubor, 0=maž soubor)

**Chování**:
- Používá `WinExec()` (legacy Win16 API!)
- Pokud `a4=1`: busy-wait dokud se neobjeví soubor, pak ho načte
- Pokud `a4=0`: busy-wait dokud se nepodaří smazat soubor
- Vrací 0 při chybě WinExec (hodnota <= 0x1F)

### sub_4016E0 (0x4016E0) - Loader .syn formátu
**Struktura načítaných dat**:
```c
typedef struct {
    char* string;    // ukazatel na řetězec
    int   value1;    // první hodnota
    int   value2;    // druhá hodnota
} SynEntry;
```

**Proces načítání**:
1. Kontroluje hlavičku "ABCD" (4 bajty)
2. Čte počet záznamů (4 bajty)
3. Alokuje paměť pro tabulku offsetů (16B * počet)
4. Alokuje paměť pro výsledné pole (12B * (počet+1))
5. Pro každý záznam:
   - Seekuje na offset uvedený v tabulce
   - Alokuje a načítá řetězec
   - Ukládá hodnoty do výsledného pole
6. Ukončuje pole NULL záznamem

### sub_4014D0 (0x4014D0) - Writer .cmp formátu
**Zápis souboru**:
1. Zapíše hlavičku "ABCD"
2. Spočítá záznamy (hledá NULL terminátor)
3. Zapíše počet záznamů
4. Alokuje dočasnou tabulku offsetů
5. Rezervuje místo pro tabulku (fseek)
6. Pro každý záznam:
   - Získá aktuální pozici (ftell)
   - Zapíše řetězec na konec souboru
   - Ukládá offset do tabulky
7. Vrátí se a zapíše tabulku offsetů

### sub_401050 (0x401050) - Wrapper pro fopen s CWD
**Funkcionalita**:
- Rozdělí cestu na adresář a jméno souboru
- Dočasně změní CWD na cílový adresář
- Otevře soubor
- Vrátí původní CWD
- Používá se pro otevírání souborů s relativními cestami

### sub_401180 (0x401180) - Error handler
**Akce při chybě**:
1. Zapíše chybovou zprávu do `spp.err`
2. Vytvoří prázdný `vm.syn`
3. Ukončí program s kódem 0 (exit)

## Formát .syn/.cmp souboru

### Binární struktura
```
Offset  Size    Description
0x00    4       Magic "ABCD" (0x44434241 little-endian)
0x04    4       Počet záznamů (uint32_t)
0x08    16*n    Tabulka záznamů:
                  +0x00: offset řetězce (uint32_t)
                  +0x04: délka řetězce včetně \0 (uint32_t)
                  +0x08: hodnota 1 (uint32_t)
                  +0x0C: hodnota 2 (uint32_t)
0x08+16*n ...   Data řetězců (null-terminated)
```

### Příklad struktury v paměti
```c
// Tabulka na disku (16B per záznam)
struct SynFileEntry {
    uint32_t offset;    // 0x00: offset k řetězci
    uint32_t length;    // 0x04: délka včetně \0
    uint32_t value1;    // 0x08: první hodnota
    uint32_t value2;    // 0x0C: druhá hodnota
};

// Struktura v paměti po načtení (12B per záznam)
struct SynMemEntry {
    char*    string;    // 0x00: pointer na řetězec
    uint32_t value1;    // 0x04: první hodnota
    uint32_t value2;    // 0x08: druhá hodnota
};
```

## Pipeline kompilace

### Fáze 1: Preprocessor (spp.exe)
```
spp.exe "source.c" "spp.c"
```
- Vstup: Zdrojový C-like skript
- Výstup: `spp.c` (předzpracovaný kód), `spp.syn` (mapa symbolů)
- Synchronizace: čeká na vytvoření `spp.syn`, pak ho načte

### Fáze 2: Kompilátor (scc.exe)
```
scc.exe "spp.c" "sasm.sca" "output.scr" ["output.h"]
```
- Vstup: Předzpracovaný kód
- Výstup: `sasm.sca` (assembly kód), vytváří `scc.syn`
- Synchronizace: maže `scc.syn` až je hotový

### Fáze 3: Assembler (sasm.exe)
```
sasm.exe "sasm.sca" "output.scr" ["output.h"]
```
- Vstup: Assembly kód
- Výstup: `output.scr` (bytecode), `output.h` (header)
- Synchronizace: maže `sasm.syn` až je hotový

## Kritické problémy a omezení

### 1. Race Conditions
- **Problém**: Busy-wait bez proper synchronizace
- **Riziko**: Child proces může být stále v procesu zápisu když parent začne číst
- **Dopad**: Možné částečné načtení nebo poškození dat

### 2. Konflikt návratových kódů
- **Problém**: Vrací 0 jak při úspěchu, tak při chybě WinExec
- **Dopad**: Nelze spolehlivě detekovat některé chyby

### 3. Legacy API
- **WinExec**: Zastaralé od Windows 95, mělo by používat CreateProcess
- **Omezení**: Max 32KB příkazová řádka, žádná kontrola nad procesy

### 4. Pracovní adresář
- **Změna CWD**: Může způsobit problémy v multi-threaded prostředí
- **Předpoklad**: Všechny .exe musí být ve stejném adresáři

### 5. Hardcoded názvy souborů
- **Dočasné soubory**: Pevné názvy bez randomizace
- **Riziko**: Kolize při paralelním běhu více instancí

## Dočasné soubory

### Mazané před kompilací
- `spp.err`, `spp.dbg`, `spp.c`, `spp.syn`
- `scc.err`, `scc.dbg`
- `sasm.sca`, `sasm.err`, `sasm.dbg`

### Synchronizační soubory
- `spp.syn` - čeká na vytvoření, pak načte
- `scc.syn` - čeká až lze smazat
- `sasm.syn` - čeká až lze smazat

### Výstupní soubory
- `vm.syn` - vždy vytvoří prázdný v původním CWD
- `*.cmp` - mapa symbolů (přejmenovaný .scr na .cmp)

## Důležité adresy a konstanty

### Globální proměnné
- `0x42BC5C (dword_42BC5C)` - pointer na načtenou .syn mapu
- `0x42BC78 (dword_42BC78)` - major version OS
- `0x42BC74 (dword_42BC74)` - minor version OS

### Magic hodnoty
- `0x1F` - hranice pro detekci chyby WinExec
- `0x10` - MB_ICONERROR pro MessageBox
- `5` - SW_SHOW pro WinExec
- `"ABCD"` - magic string pro .syn/.cmp formát

## Doporučení pro dekompilátor

### Parser .syn/.cmp formátu
1. Implementovat robustní parser s kontrolou hlavičky
2. Validovat offsety proti velikosti souboru
3. Ošetřit chybějící null-terminátory

### Mapování symbolů
1. .cmp soubor obsahuje mapování původních názvů
2. Hodnoty value1/value2 pravděpodobně obsahují:
   - Offsety v bytecode
   - Typy symbolů (funkce/proměnná/konstanta)
   - Původní čísla řádků

### Error handling
1. Kontrolovat existenci .err souborů pro detekci chyb
2. Parser pro error messages v .err souborech

### Kompatibilita
1. Zachovat podporu pro 4 i 5 argumentů
2. Respektovat debug flag (5. argument)
3. Emulovat vytváření vm.syn pro kompatibilitu

## Závěr
SCMP.exe je orchestrátor 3-fázové kompilace s primitivní synchronizací přes soubory. Hlavní funkcí je spouštění child procesů, správa pracovního adresáře a zpracování mapovacích souborů .syn/.cmp. Pro dekompilátor je klíčové pochopit formát .cmp souborů, které obsahují mapování mezi původními názvy a zkompilovaným bytecode.