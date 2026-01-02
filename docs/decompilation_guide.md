# Instrukce pro dekompilaci a rekonstrukci VC skriptů

## Přehled nástrojů

### 1. vcdecomp (Python dekompilátor)
Náš vlastní dekompilátor pro .SCR soubory Vietcongu.

**Základní příkazy:**
```bash
# Informace o skriptu
python -m vcdecomp info script.SCR

# Disassembly (nejdůležitější!)
python -m vcdecomp disasm script.SCR > script.asm

# Automatická dekompilace (surová, ale užitečná)
python -m vcdecomp structure script.SCR > script.c

# CFG (control flow graph)
python -m vcdecomp cfg script.SCR

# GUI pro vizualizaci
python -m vcdecomp gui script.SCR
```

### 2. Originální kompilátor (pro ověření)
```bash
# Kompilace C -> SCR
scmp.exe source.c output.scr header.h
```

---

## Postup dekompilace

### Krok 1: Základní analýza
```bash
python -m vcdecomp info script.SCR
```
Zjistíš:
- Počet instrukcí
- Počet funkcí
- Počet externích funkcí (XFN)
- Entry point

### Krok 2: Vytvoř disassembly
```bash
python -m vcdecomp disasm script.SCR > script.asm
```
**Toto je NEJDŮLEŽITĚJŠÍ soubor!** Obsahuje:
- Seznam externích funkcí s prototypy
- Seznam stringů
- Kompletní instrukce pro každou funkci

### Krok 3: Vytvoř surovou dekompilaci
```bash
python -m vcdecomp structure script.SCR > script.c
```
Toto je základ pro rekonstrukci, ale:
- ⚠️ Proměnné jsou pojmenované `local_X`, `param_X`
- ⚠️ Některé hodnoty konstant jsou ŠPATNĚ zobrazené
- ⚠️ Control flow může být nepřesný

---

## Postup rekonstrukce

### Krok 1: Identifikuj globální proměnné
Z disassembly najdi `GADR data[X]` instrukce - to jsou globální proměnné.

**Příklad mapování:**
| data[X] | Typ | Název | Popis |
|---------|-----|-------|-------|
| data[1] | int | gphase | State machine |
| data[3] | int | myside | Strana bota |
| data[12] | dword | pl_id | Player ID |

### Krok 2: Identifikuj funkce
Z disassembly:
```
func_0001:
  001: GADR     data[26]    ; První instrukce
  ...
  034: RET      0           ; Return
func_0035:
  035: ...                   ; Další funkce
```

### Krok 3: Analyzuj každou funkci
Pro každou funkci:

1. **Najdi parametry**: `LADR [sp-3]` = první parametr
2. **Najdi lokální proměnné**: `ASP X` = alokace X dwords
3. **Najdi volání funkcí**: `CALL func_XXXX` nebo `XCALL $název`
4. **Rekonstruuj logiku** podle instrukcí

### Krok 4: Pojmenuj konstanty
Použij `sc_global.h` pro konstanty:
- `SC_P_TYPE_AI = 2`
- `SC_P_SIDE_US = 0`
- `SC_P_SIDE_VC = 1`
- `SC_P_AI_MODE_BATTLE = 1`
- `SGI_DIFFICULTY = 10`

---

## Klíčové instrukce

| Instrukce | Význam |
|-----------|--------|
| `ASP X` | Alokuj X dwords na stacku |
| `SSP X` | Uvolni X dwords ze stacku |
| `GCP data[X]` | Push konstanta z data segmentu |
| `GADR data[X]` | Push adresa globální proměnné |
| `LADR [sp+X]` | Push adresa lokální proměnné |
| `LADR [sp-X]` | Push adresa parametru |
| `LCP [sp+X]` | Load hodnota lokální proměnné |
| `DCP X` | Dereference pointer (X = velikost) |
| `PNT X` | Pointer offset (struktura) |
| `ASGN` | Assignment (pop hodnotu, pop adresu, ulož) |
| `XCALL $func` | Volání externí funkce |
| `CALL func_X` | Volání interní funkce |
| `JZ label` | Jump if zero |
| `JMP label` | Unconditional jump |
| `RET X` | Return, uvolni X dwords |

---

## Ověření rekonstrukce

### 1. Porovnej velikost
```bash
# Zkompiluj rekonstrukci
scmp.exe reconstructed.c test.scr header.h

# Porovnej velikost
dir original.SCR    # např. 38 KB
dir test.scr        # mělo by být ~stejné
```

### 2. Ověř klíčové funkce
Pro každou funkci porovnej:
- Počet instrukcí
- Volané funkce
- Logiku podmínek

---

## Časté chyby

### 1. Špatné hodnoty konstant
Dekompilátor ukazuje `; = 0` pro mnoho konstant.
**Řešení:** Čti přímo data segment nebo ověř proti disassembly.

### 2. Parametry funkcí
Pokud funkce používá `LADR [sp-3]`, bere parametr!
```c
// ŠPATNĚ:
void SetupVC(void) { ... }

// SPRÁVNĚ:
void SetupVC(s_SC_P_Create *pinfo) { ... }
```

### 3. Podmínky
`JZ` = Jump if Zero = `if (value == 0) goto label`
```c
// Disasm: JZ label_X
// SPRÁVNĚ:
if (value != 0) {
    // kód před label_X
}
```

### 4. Switch/case
Kompilátor generuje jump tabulky. Hledej sekvenci:
```
JMP label_X
JMP label_Y
label_X:
  LCP [sp+N]
  GCP data[M]
  EQU
  JZ label_next
```

---

## Mapování globálních proměnných (USBOT0)

| Data offset | Název | Typ | Popis |
|-------------|-------|-----|-------|
| data[1] | gphase | int | State machine fáze |
| data[3] | myside | int | Strana bota (0=US, 1=VC) |
| data[4] | enemyside | int | Nepřátelská strana |
| data[8] | origpos | c_Vector3 | Původní pozice |
| data[11] | myflag | c_Vector3 | Pozice vlastní vlajky |
| data[12] | pl_id | dword | Player ID bota |
| data[14] | enflag | c_Vector3 | Pozice nepřátelské vlajky |
| data[17] | mycurflag | c_Vector3 | Aktuální pozice vlastní vlajky |
| data[20] | encurflag | c_Vector3 | Aktuální pozice nepř. vlajky |
| data[23] | enflagstat | int | Stav nepřátelské vlajky |
| data[24] | myflagstat | int | Stav vlastní vlajky |
| data[25] | origz | float | Původní Z rotace |
| data[118] | standingtimer | float | Timer pro stání |
| data[119] | endtimer | float | Koncový timer |
| data[120] | orderstimer | float | Timer pro rozkazy |
| data[121] | myorder | int | Aktuální rozkaz |
| data[122] | priority | int | Priorita |

---

## Mapování konstant

### AI Modes
- `1` → `SC_P_AI_MODE_BATTLE`
- `0` → `SC_P_AI_MODE_SCRIPT`

### Battle Modes
- `0` → `SC_P_AI_BATTLEMODE_HOLD`
- `1` → `SC_P_AI_BATTLEMODE_ATTACK`

### SGI konstanty
- `SC_ggi(10)` → `SC_ggi(SGI_DIFFICULTY)`

### Difficulty hodnoty
- `0` → Easy
- `1` → Medium
- `2` → Hard
- `3` → Vietcong

### Float konstanty v AI props
- `1.0f` - shoot_imprecision (Easy)
- `0.7f` - shoot_imprecision (Medium)
- `0.3f` - shoot_imprecision (Hard)
- `0.1f` - shoot_imprecision (Vietcong)

---

## Důležité soubory

| Soubor | Popis |
|--------|-------|
| `compiler/inc/sc_global.h` | Hlavičky a struktury |
| `docs/Scripting_SDK.txt` | Oficiální SDK dokumentace |
| `decompilation/USBOT0.asm` | Příklad disassembly |
| `decompilation/USBOT0_reconstructed.c` | Příklad rekonstrukce |

---

## Tipy

1. **Začni od jednoduchých funkcí** - `_init`, `SetupVC`, `SetupUS`
2. **Používej SDK dokumentaci** pro prototypy externích funkcí
3. **Kontroluj offsety struktur** - např. `s_SC_P_Create.side` je na offsetu 4
4. **Kompiluj průběžně** - ověřuj že kód jde zkompilovat
5. **Porovnávej velikost** - pokud je moc malá, něco chybí

---

## Příklad: Kompletní workflow

```bash
# 1. Získej info
python -m vcdecomp info USBOT0.SCR

# 2. Vytvoř disassembly
python -m vcdecomp disasm USBOT0.SCR > USBOT0.asm

# 3. Vytvoř základní dekompilaci
python -m vcdecomp structure USBOT0.SCR > USBOT0.c

# 4. Rekonstruuj ručně (čti asm, pojmenuj proměnné)
# ... editace souboru ...

# 5. Zkompiluj a ověř
scmp.exe USBOT0_reconstructed.c test.scr header.h
dir test.scr   # Porovnej velikost s originálem
```

---

*Tento dokument byl vytvořen na základě zkušeností s dekompilací USBOT0.SCR.*
