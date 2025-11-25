# SASM.EXE - Důkladná technická analýza pro dekompilátor

## 1. Přehled

SASM.EXE je poslední část kompilačního řetězce Vietcong skriptů, který provádí:
- Assembler: Převod `.sca` (assembler source) na binární instrukce
- Linker: Sestavení finálního `.scr` souboru s všemi sekcemi

### Základní informace
- **Velikost**: 0x1d000 bytes (118,784 bytes)
- **Entry point**: 0x409042 (start)
- **Main function**: WinMain@16 (0x404B40)
- **MD5**: 78c33e5888fd0b586b62369a41df3b3d

## 2. Architektura programu

### 2.1 Hlavní flow
```
WinMain (0x404B40)
  ├─ Parse arguments (argc 3-4)
  ├─ Open sasm.dbg pro debug log
  ├─ Call sub_401FF0 (main compiler)
  └─ Create empty sasm.syn

sub_401FF0 (Main compiler pipeline)
  ├─ sub_401000: Open input .sca file
  ├─ sub_404DA0: Initialize
  ├─ sub_4030C0: Parse/load AST
  ├─ sub_401270: Process
  ├─ sub_4016B0: Generate code segment & metadata
  ├─ sub_401FC0: Process code
  ├─ sub_4012D0: Generate data segment
  ├─ sub_4019B0: Generate XFN table
  ├─ sub_401AF0: Generate global pointers
  └─ sub_401CC0: Write final .scr file
```

### 2.2 Klíčové datové struktury

#### Globální proměnné
- **0x41D5B4**: AST root - linked list instrukcí
- **0x41D5D0**: XFN list - externí funkce
- **0x41D620**: Data segment list - konstanty
- **0x41D5B0**: Enter array - vstupní parametry
- **0x41D5A4**: Return size list - návratové hodnoty
- **0x41D5D8**: Symbol table
- **0x41D350**: Debug file handle (sasm.dbg)

## 3. Formát instrukcí

### 3.1 Struktura instrukce (12 bytes)
```c
struct Instruction {
    uint32_t opcode;  // 0x00: Opcode (0-149)
    uint32_t arg1;    // 0x04: První argument
    uint32_t arg2;    // 0x08: Druhý argument
};
```

### 3.2 Kódování opcode
- AST obsahuje raw hodnoty začínající od 258
- Finální opcode = raw_value - 258
- Rozsah: 0-149 (150 instrukcí)

### 3.3 Kódování argumentů
- **Literály**: Přímá hodnota (atoi pro integery)
- **Labely**: label_index (ukazatel na instrukci)
- **Float literály**: Speciální handling přes sub_407C50
- **Odkazy na data**: Offset v data segmentu

## 4. Kompletní tabulka instrukcí

### Základní aritmetika a logika (0-26)
| ID | Mnemonic | Popis | Argumenty |
|----|----------|-------|-----------|
| 0 | CALL | Volání interní funkce | label, - |
| 1 | RET | Návrat z funkce | ret_count, - |
| 2 | LCP | Load constant/parameter | index, - |
| 3 | GCP | Load global constant | offset, - |
| 4 | LLD | Load local data | offset, - |
| 5 | GLD | Load global data | offset, - |
| 6 | ASP | Add to stack pointer | count, - |
| 7 | SSP | Set stack pointer | value, - |
| 8 | INC | Increment | -, - |
| 9 | DEC | Decrement | -, - |
| 10 | ADD | Integer add | -, - |
| 11 | SUB | Integer subtract | -, - |
| 12 | NEG | Integer negate | -, - |
| 13 | MUL | Integer multiply | -, - |
| 14 | DIV | Integer divide | -, - |
| 15 | LES | Integer less than | -, - |
| 16 | LEQ | Integer less equal | -, - |
| 17 | GRE | Integer greater | -, - |
| 18 | GEQ | Integer greater equal | -, - |
| 19 | EQU | Integer equal | -, - |
| 20 | NEQ | Integer not equal | -, - |
| 21 | AND | Logical AND | -, - |
| 22 | OR | Logical OR | -, - |
| 23 | NOT | Logical NOT | -, - |
| 24 | JMP | Unconditional jump | label, - |
| 25 | JZ | Jump if zero | label, - |
| 26 | JNZ | Jump if not zero | label, - |

### Float operace (27-38)
| ID | Mnemonic | Popis |
|----|----------|-------|
| 27 | FADD | Float add |
| 28 | FSUB | Float subtract |
| 29 | FNEG | Float negate |
| 30 | FMUL | Float multiply |
| 31 | FDIV | Float divide |
| 32 | FINV | Float inverse |
| 33 | FLES | Float less than |
| 34 | FLEQ | Float less equal |
| 35 | FGRE | Float greater |
| 36 | FGEQ | Float greater equal |
| 37 | FEQU | Float equal |
| 38 | FNEQ | Float not equal |

### Adresování a pointery (39-45)
| ID | Mnemonic | Popis |
|----|----------|-------|
| 39 | LADR | Load local address |
| 40 | GADR | Load global address |
| 41 | DADR | Load data address |
| 42 | PNT | Pointer dereference |
| 43 | DCP | Data constant push |
| 44 | DLD | Data load |
| 45 | ASGN | Assignment to address |

### Char operace (46-58)
| ID | Mnemonic | Popis |
|----|----------|-------|
| 46 | CINC | Char increment |
| 47 | CDEC | Char decrement |
| 48 | CADD | Char add |
| 49 | CSUB | Char subtract |
| 50 | CNEG | Char negate |
| 51 | CMUL | Char multiply |
| 52 | CDIV | Char divide |
| 53 | CLES | Char less than |
| 54 | CLEQ | Char less equal |
| 55 | CGRE | Char greater |
| 56 | CGEQ | Char greater equal |
| 57 | CEQU | Char equal |
| 58 | CNEQ | Char not equal |

### Short operace (59-71)
| ID | Mnemonic | Popis |
|----|----------|-------|
| 59 | SINC | Short increment |
| 60 | SDEC | Short decrement |
| 61 | SADD | Short add |
| 62 | SSUB | Short subtract |
| 63 | SNEG | Short negate |
| 64 | SMUL | Short multiply |
| 65 | SDIV | Short divide |
| 66 | SLES | Short less than |
| 67 | SLEQ | Short less equal |
| 68 | SGRE | Short greater |
| 69 | SGEQ | Short greater equal |
| 70 | SEQU | Short equal |
| 71 | SNEQ | Short not equal |

### Double operace (72-83)
| ID | Mnemonic | Popis |
|----|----------|-------|
| 72 | DADD | Double add |
| 73 | DSUB | Double subtract |
| 74 | DNEG | Double negate |
| 75 | DMUL | Double multiply |
| 76 | DDIV | Double divide |
| 77 | DINV | Double inverse |
| 78 | DLES | Double less than |
| 79 | DLEQ | Double less equal |
| 80 | DGRE | Double greater |
| 81 | DGEQ | Double greater equal |
| 82 | DEQU | Double equal |
| 83 | DNEQ | Double not equal |

### Typové konverze (84-103)
| ID | Mnemonic | Popis |
|----|----------|-------|
| 84 | CTOS | Char to short |
| 85 | CTOI | Char to int |
| 86 | CTOF | Char to float |
| 87 | CTOD | Char to double |
| 88 | STOC | Short to char |
| 89 | STOI | Short to int |
| 90 | STOF | Short to float |
| 91 | STOD | Short to double |
| 92 | ITOC | Int to char |
| 93 | ITOS | Int to short |
| 94 | ITOF | Int to float |
| 95 | ITOD | Int to double |
| 96 | FTOC | Float to char |
| 97 | FTOS | Float to short |
| 98 | FTOI | Float to int |
| 99 | FTOD | Float to double |
| 100 | DTOC | Double to char |
| 101 | DTOS | Double to short |
| 102 | DTOI | Double to int |
| 103 | DTOF | Double to float |

### Speciální a bitové operace (104-137)
| ID | Mnemonic | Popis |
|----|----------|-------|
| 104 | GDM | Get data member |
| 105 | FDM | Free data member |
| 106 | CBN | Char bitwise NOT |
| 107 | SBN | Short bitwise NOT |
| 108 | BN | Int bitwise NOT |
| 109 | CMOD | Char modulo |
| 110 | SMOD | Short modulo |
| 111 | MOD | Int modulo |
| 112 | CLS | Char left shift |
| 113 | SLS | Short left shift |
| 114 | LS | Int left shift |
| 115 | CRS | Char right shift |
| 116 | SRS | Short right shift |
| 117 | RS | Int right shift |
| 118 | CBA | Char bitwise AND |
| 119 | SBA | Short bitwise AND |
| 120 | BA | Int bitwise AND |
| 121 | CBX | Char bitwise XOR |
| 122 | SBX | Short bitwise XOR |
| 123 | BX | Int bitwise XOR |
| 124 | CBO | Char bitwise OR |
| 125 | SBO | Short bitwise OR |
| 126 | BO | Int bitwise OR |
| 127 | IDIV | Integer division |
| 128 | SCS | Set carry status |
| 129 | SCI | Set carry int |
| 130 | SSI | Set status int |
| 131 | UCS | Unset carry status |
| 132 | UCI | Unset carry int |
| 133 | USI | Unset status int |
| 134 | PCALL | Pointer call |
| 135 | CFA | Call function address |
| 136 | XCALL | External call (XFN) |
| 137 | ITRPT | Interrupt |

### Unsigned porovnání (138-149)
| ID | Mnemonic | Popis |
|----|----------|-------|
| 138 | UCLES | Unsigned char less |
| 139 | USLES | Unsigned short less |
| 140 | ULES | Unsigned int less |
| 141 | UCLEQ | Unsigned char less equal |
| 142 | USLEQ | Unsigned short less equal |
| 143 | ULEQ | Unsigned int less equal |
| 144 | UCGRE | Unsigned char greater |
| 145 | USGRE | Unsigned short greater |
| 146 | UGRE | Unsigned int greater |
| 147 | UCGEQ | Unsigned char greater equal |
| 148 | USGEQ | Unsigned short greater equal |
| 149 | UGEQ | Unsigned int greater equal |

## 5. Struktura výstupního .SCR souboru

### 5.1 Header
```c
struct SCRHeader {
    uint32_t enter_size;     // Počet vstupních parametrů
    uint32_t enter_ip;       // Entry point (index instrukce nebo -2)
    uint32_t ret_size;       // Počet návratových hodnot
    uint32_t enter_array[enter_size];  // Typy parametrů
};
```

### 5.2 Data segment
```c
struct DataSegment {
    uint32_t data_count;     // Počet 32-bit slov
    uint32_t data[data_count]; // Data (4-byte aligned)
};
```

### 5.3 Global pointers
```c
struct GlobalPointers {
    uint32_t gptr_count;     // Počet globálních pointerů
    uint32_t gptr_offsets[gptr_count]; // Offsety v data segmentu
};
```

### 5.4 Code segment
```c
struct CodeSegment {
    uint32_t code_count;     // Počet instrukcí
    Instruction code[code_count]; // Instrukce (12 bytes each)
};
```

### 5.5 External functions (XFN)
```c
struct XFNTable {
    uint32_t xfn_count;      // Počet externích funkcí
    struct XFN {             // 28 bytů (7 dwords) na záznam
        uint32_t name_ptr;   // [+0x00] Pointer na jméno funkce (string)
        uint32_t reserved1;  // [+0x04] Vždy 0
        uint32_t field1;     // [+0x08] Z dword_41D5D0[4] (možná ret_size)
        uint32_t field2;     // [+0x0C] Z dword_41D5D0[8] (možná arg_count)
        uint32_t field3;     // [+0x10] Z dword_41D5D0[12] (možná arg_type)
        uint32_t field4;     // [+0x14] Z dword_41D5D0[16]
        uint32_t last_flag;  // [+0x18] 0, kromě posledního záznamu (=1)
    } xfn[xfn_count];
    char xfn_names[];        // Jména funkcí (null-terminated)
};
```

**Detaily implementace** (z analýzy sub_4019B0 a sub_401CC0):
- XFN seznam je během kompilace uložen v globální linked list `dword_41D5D0`
- Každý záznam v linked listu má 7 polí, které se kopírují do výstupního .scr
- sub_4019B0 prochází linked list a vytváří pole XFN struktur (28 bytes each)
- Poslední záznam má `last_flag` nastaven na 1 (řádek 53 v sub_4019B0)
- sub_401CC0 zapisuje XFN tabulku na offset v .scr souboru:
  - Nejprve počet XFN (4 bytes)
  - Pak pole XFN struktur (28 * xfn_count bytes)
  - Následně jména funkcí jako null-terminated strings v pořadí záznamů

**Použití v runtime**: Instrukce XCALL (opcode 136) používá XFN tabulku pro volání externích funkcí.
Index do XFN tabulky je typicky v arg1 instrukce XCALL.

### 5.6 Save info (optional)
```c
char magic[9] = "sav_info";
uint32_t sav_count;          // Počet save položek
struct SaveItem {
    char name[];             // Null-terminated string
    uint32_t val1;          // Hodnota 1
    uint32_t val2;          // Hodnota 2
} items[sav_count];
```

## 6. Klíčové funkce pro dekompilátor

### 6.1 sub_403260 - Lexer (tokenizátor)
- **Funkce**: Lexikální analyzátor pro .sca soubory - hlavní scanner
- **Implementace**: DFA-based state machine
- **Návratové hodnoty**:
  - **0**: EOF (case 176)
  - **35**: # (case 3)
  - **36**: $ (case 4)
  - **61**: = (case 5)
  - **63**: ? (case 2)
  - **64**: @ (case 6)
  - **258-363**: Základní instrukce (cases 7-112, CALL až BO)
  - **364-393**: Rozšířené instrukce (cases 116-145)
  - **394**: XCALL (case 113) - speciální pro externí volání
  - **395-407**: Další instrukce (cases 149-161)
  - **408-409**: Speciální tokeny (cases 114-115)
  - **410-412**: Dodatečné tokeny (cases 146-148)
  - **413**: Identifikátor (case 162)
  - **414**: Číselný literál - hex (case 163) nebo octal (case 164)
  - **415**: Float literál (case 170)

- **Zpracování čísel**:
  - **Hex čísla** (case 163): Prefix 0x, parsuje zpětně od konce
  - **Octal čísla** (case 164): Parsuje číslice 0-7
  - **Float čísla** (case 170): Volá sub_4048F0

- **State machine tabulky**:
  - **0x4123F0**: Character class lookup (256*4 bytes)
  - **0x4127F0**: State transition table
  - **0x4128C0**: State base offsets
  - **0x412BD0**: Backup states
  - **0x412EE0**: Next state table
  - **0x413380**: Accept state table
  - **0x4120E8**: Token type table

- **Buffer management**:
  - **dword_41D58C**: Current position
  - **dword_41D580**: Token start
  - **byte_41D574**: Saved character
  - **ElementSize**: Token length

### 6.2 sub_4030C0 - Parser helper
- **Funkce**: Vytváří AST uzly pro hlavní parser
- **Struktura AST uzlu** (24 bytes, vytvářeno v sub_402F00):
  ```c
  struct ASTNode {
      uint32_t type;       // [+0x00] Typ uzlu (instrukce/direktiva)
      uint32_t child1;     // [+0x04] První operand/potomek
      uint32_t child2;     // [+0x08] Druhý operand/potomek
      uint32_t child3;     // [+0x0C] Třetí operand/potomek
      uint32_t next;       // [+0x10] Další sourozenec (linked list)
      uint32_t reserved;   // [+0x14] Reserved (vždy 0)
  };
  ```
- **Speciální typ 259 (0x103)**: Root node programu
- **Globální linked list**: Uzly se propojují přes pole `next`

### 6.3 sub_404DA0 - Hlavní parsing loop
- **Funkce**: Koordinuje lexer a parser, vytváří kompletní AST
- **Velikost**: 0x2774 bytes (velmi komplexní)
- **Volá**:
  - sub_403260 (lexer) pro získání tokenů
  - sub_4030C0 a další pro vytváření AST uzlů
- **Switch statement**: Zpracovává různé typy tokenů a vytváří odpovídající AST uzly

### 6.4 sub_401270 - Preprocessing
- **Funkce**: Preprocessing před generováním kódu
- **Zpracovává**: Makra, konstanty, symboly

### 6.5 sub_4016B0 - Generování kódu
- Zpracovává AST a generuje instrukce
- Hledá @ScriptMain entry point
- Konvertuje AST uzly na binární instrukce
- Provádí offset calculation pro labely

### 6.2 sub_4012D0 - Data segment
- Zpracovává konstanty různých typů (char, short, int, float, double, string)
- Provádí 4-byte alignment
- Podporuje escape sekvence v char literálech

### 6.3 sub_4019B0 - Externí funkce (XFN)
- Sestavuje tabulku externích funkcí
- Generuje 28-bytové záznamy (7 dwords)
- Kopíruje data z dword_41D5D0 linked list
- Debug výpis: `%03d : %s %p %d %d %d %d %d`
- Poslední záznam má nastaven flag (offset 0x18) na 1

### 6.4 sub_401AF0 - Globální pointery
- Identifikuje globální proměnné
- Kontroluje 4-byte alignment
- Generuje offset tabulku

## 7. Speciální případy a omezení

### 7.1 Entry point
- Hledá symbol "@ScriptMain"
- Pokud neexistuje, kompilace selže
- Index je uložen jako enter_ip

### 7.2 Float handling
- Speciální kód 0x18A (394) pro XCALL s float argumenty
- Funkce sub_407C50 pro float konverzi

### 7.3 Debug výstup
- sasm.dbg obsahuje detailní trace
- Vypisuje všechny sekce (code, data, XFN, gptr)
- Format: `%03d : MNEMONIC arg1, arg2`

## 8. Důležité konstanty

- **Opcode offset**: 258 (0x102)
- **Max opcodes**: 150
- **Instruction size**: 12 bytes
- **Special XCALL code**: 0x18A (394)

## 9. Kompletní pipeline kompilace

### Přehled procesu
1. **Lexická analýza** (sub_403260):
   - Čte .sca soubor znak po znaku
   - DFA-based tokenizer s 176 stavy
   - Vrací tokeny (258-415) pro instrukce, identifikátory, literály

2. **Syntaktická analýza** (sub_404DA0 + helpers):
   - Hlavní loop volá lexer pro tokeny
   - Vytváří AST uzly (24 bytes each) přes sub_402F00
   - Propojuje uzly do stromu přes linked list

3. **Generování kódu** (sub_4016B0):
   - Prochází AST a generuje 12-byte instrukce
   - Resolvuje labely a skoky
   - Hledá @ScriptMain entry point

4. **Sestavení dat** (sub_4012D0):
   - Zpracovává konstanty všech typů
   - 4-byte alignment
   - Vytváří data segment

5. **Externí funkce** (sub_4019B0):
   - Extrahuje XFN z globální linked list
   - Vytváří 28-byte záznamy
   - Připojuje jména funkcí

6. **Zápis SCR** (sub_401CC0):
   - Zapisuje všechny sekce v pořadí
   - Připojuje sav_info pokud existuje

## 10. Doporučení pro dekompilátor

1. **Parsování SCR**:
   - Číst header pro získání metadat
   - Dekódovat instrukce (opcode + 2 argumenty)
   - Rekonstruovat control flow z jump instrukcí
   - Mapovat XFN indexy na jména funkcí

2. **Rekonstrukce typů**:
   - Analyzovat typové instrukce (C*, S*, F*, D*)
   - Sledovat stack pro type inference

3. **Identifikace funkcí**:
   - CALL/RET páry
   - XCALL pro externí volání
   - Entry points z enter_ip

4. **Data flow analýza**:
   - LCP/GCP pro konstanty
   - LLD/GLD pro proměnné
   - LADR/GADR/DADR pro adresy

5. **Optimalizace**:
   - Rozpoznat vzory (např. INC+JNZ = for loop)
   - Sloučit typové konverze
   - Identifikovat switch statements

## 10. Formát vstupního .SCA souboru

### 10.1 Struktura
.SCA (Script Assembler) je textový formát assembleru:
```asm
; Komentáře začínají středníkem
@label:             ; Definice labelu
    CALL @function  ; Instrukce s labelem
    LCP 5          ; Instrukce s literálem
    RET 1          ; Návrat

@ScriptMain:       ; Povinný entry point
    ; Kód skriptu
```

### 10.2 Podporované formáty čísel
- **Decimální**: 123
- **Hexadecimální**: 0x7B nebo $7B
- **Oktální**: 0173
- **Float**: 3.14

### 10.3 Direktivy
- **@symbol**: Definice labelu/symbolu
- **#define**: Definice konstanty
- **extern**: Deklarace externí funkce

## 11. Lexer detaily

### 11.1 Token hodnoty (přesné mapování ze sub_403260)
Lexer vrací následující tokeny podle case hodnot ve switch:
- **0**: EOF (case 176)
- **35**: `#` hash (case 3)
- **36**: `$` dollar (case 4)
- **61**: `=` equals (case 5)
- **63**: `?` question (case 2)
- **64**: `@` at sign (case 6)
- **258-363**: Instrukce 0-105 (cases 7-112) - CALL až BO
- **364-393**: Instrukce 106-135 (cases 116-145)
- **394**: XCALL - instrukce 136 (case 113)
- **395-407**: Instrukce 137-149 (cases 149-161)
- **408-409**: Speciální tokeny (cases 114-115)
- **410-412**: Dodatečné tokeny (cases 146-148)
- **413**: Identifikátor/symbol (case 162)
- **414**: Číselný literál - hex/octal (cases 163-164, 165-169)
- **415**: Float literál (case 170)

### 11.2 DFA tabulky
Lexer používá několik tabulek pro state machine:
- **0x4123F0**: Character class table (256 entries)
- **0x4127F0**: State transition table
- **0x4128C0**: State base offsets
- **0x412EE0**: Next state table
- **0x413380**: Accept state table

### 11.3 Buffer management
- **0x41D588**: Input buffer (16KB default)
- **0x41D58C**: Current position
- **0x41D580**: Token start
- **ElementSize**: Token length

## 12. Závěr

SASM.EXE je relativně jednoduchý assembler/linker s pevně danou instrukční sadou. Pro úspěšnou dekompilaci je klíčové:
- Správně parsovat 12-bytové instrukce
- Rekonstruovat control flow graph
- Provést type inference na základě instrukcí
- Identifikovat vysokoúrovňové konstrukty (loops, conditions, switches)

Tato analýza poskytuje kompletní základ pro implementaci dekompilátoru.