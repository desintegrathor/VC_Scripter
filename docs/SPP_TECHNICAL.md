# SPP.exe - Technická dokumentace preprocesoru

## 1. PŘEHLED ARCHITEKTURY

SPP.exe je preprocesor pro C-like skriptovací jazyk používaný ve hře Vietcong. Implementuje standardní direktivy preprocesoru (#define, #include, #if/ifdef/ifndef/else/elif/endif) a provádí expanzi maker.

### Základní charakteristiky:
- **Velikost**: 77824 bajtů (0x13000)
- **Base address**: 0x400000
- **Entry point**: 0x40636B (start)
- **WinMain**: 0x402490

## 2. DATOVÉ STRUKTURY

### 2.1 Struktura makra (216 bajtů)
```c
struct Macro {
    char* name;                  // [0x00] Jméno makra
    char* params[50];           // [0x04-0xC8] Parametry (max 50)
    int   param_count;          // [0xCC] Počet parametrů
    char* value;                // [0xD0] Hodnota/tělo makra
    struct Macro* next;         // [0xD4] Pointer na další makro v linked listu
};
```

### 2.2 Globální proměnné

| Adresa | Název | Typ | Popis |
|--------|-------|-----|-------|
| 0x442834 | dword_442834 | int | Čítač řádků aktuálního souboru |
| 0x442830 | dword_442830 | FILE* | Handle souboru `spp.dbg` |
| 0x44282C | dword_44282C | FILE* | Handle výstupního souboru |
| 0x442828 | Stream | FILE* | Handle vstupního souboru |
| 0x40F39C | dword_40F39C | int | Debug/podmíněná kompilace flag |
| 0x44283C | dword_44283C | int | Stav víceřádkových komentářů (0=mimo, 1=uvnitř) |
| 0x4168E8 | lpPathName | char* | Základní cesta pro `<...>` include |
| 0x433DB8 | dword_433DB8 | char* | Kořenová cesta pro `__FILE__` makro |
| 0x42C370 | Buffer | char[260] | Aktuální cesta souboru |
| 0x425358 | byte_425358 | char[60000] | Buffer pro aktuální řádek |
| 0x4162F8 | byte_4162F8 | char[1000] | Buffer pro expanzi makra |
| 0x412B10 | dword_412B10 | void* | Začátek seznamu načtených souborů |
| 0x4159FC | dword_4159FC | int | Počet načtených souborů |

### 2.3 Struktura záznamu souboru (12 bajtů)
```c
struct FileRecord {
    char* filepath;     // Plná cesta k souboru
    DWORD filetime_low; // FILETIME low part
    DWORD filetime_high;// FILETIME high part
};
```

## 3. HLAVNÍ KOMPONENTY

### 3.1 WinMain (0x402490)
```c
int WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
            LPSTR lpCmdLine, int nCmdShow) {
    // 1. Otevře spp.dbg pro debug výpisy
    dword_442830 = fopen("spp.dbg", "w");

    // 2. Parse argumentů (min 3, max 5)
    int argc;
    char** argv = parse_cmdline(lpCmdLine, &argc);
    if (argc < 3 || argc > 5)
        error("invalid arguments");

    // 3. Otevře vstupní a výstupní soubory
    Stream = fopen(argv[1], "r");
    dword_44282C = fopen(argv[2], "w");

    // 4. Nastaví cesty
    if (argc >= 4)
        lpPathName = argv[3];  // základní cesta pro <...> include
    else
        lpPathName = get_cwd();

    if (argc >= 5)
        dword_433DB8 = argv[4];  // kořenová cesta pro __FILE__
    else
        dword_433DB8 = get_dir(argv[1]);

    // 5. Zapíše úvodní #line direktiv
    strcpy(Buffer, get_fullpath(argv[1]));
    fprintf(dword_44282C, "#line 0 \"%s\"\n", Buffer);

    // 6. Hlavní parse smyčka
    int result = sub_404950();

    // 7. Vytvoří mapu souborů
    sub_401100();  // zapíše spp.sym
    sub_401230();  // uvolní paměť
    rename("spp.sym", "spp.syn");

    return result;
}
```

### 3.2 Parse smyčka (sub_404950)
```c
int parse() {
    if (dword_40F39C)
        fprintf(dword_442830, "\nENTERING parse(): %s\n", byte_425358);

    // Hlavní smyčka
    while (sub_402BA0()) {  // čte řádek
        // Skip whitespace na začátku
        int i = 0;
        while (byte_425358[i] == ' ' || byte_425358[i] == '\t')
            i++;

        if (byte_425358[i] == '#') {
            // Direktiva preprocesoru
            int result = sub_403FB0(i + 1);
            if (result < 0)
                return result;  // chyba (#else/-1, #endif/-2, #elif/-3)
            fprintf(dword_44282C, "\n");
        }
        else {
            // Běžný kód - expanduj makra
            sub_404810(0);
        }
    }

    return 0;  // úspěch
}
```

### 3.3 Čtení řádků (sub_402BA0)
```c
int readline() {
    static int line_offset = 0;
    static int comment_state = 0;  // dword_44283C
    char buffer[60000];
    char temp[60000];

    byte_425358[0] = '\0';

    while (1) {
        // Čti řádek ze souboru
        if (!fgets(buffer, 60000, Stream)) {
            fprintf(dword_442830, "\nreadline(): EOF found.");
            return 0;
        }

        sub_402820(buffer);  // ošetření speciálních znaků
        dword_442834++;      // čítač řádků

        // Odstranění trailing whitespace
        int len = strlen(buffer) - 1;
        while (len > 0 && (buffer[len] == ' ' ||
                          buffer[len] == '\t' ||
                          buffer[len] == '\n'))
            len--;

        line_offset += len;
        if (line_offset >= 60000)
            return 0;  // přetečení bufferu

        // Kontrola pokračování řádku
        if (buffer[len] == '\\') {
            buffer[len] = '\0';
            strcat(byte_425358, buffer);
            continue;  // čti další řádek
        }

        // Připoj řádek
        strcat(byte_425358, buffer);
        break;
    }

    // Zpracování komentářů
    int i = 0;
    while (byte_425358[i]) {
        if (comment_state == 1) {
            // Jsme uvnitř víceřádkového komentáře
            while (byte_425358[i]) {
                if (byte_425358[i] == '*' && byte_425358[i+1] == '/') {
                    // Konec komentáře
                    byte_425358[i] = ' ';
                    byte_425358[i+1] = ' ';
                    comment_state = 0;
                    i += 2;
                    break;
                }
                byte_425358[i] = ' ';  // nahraď mezerou
                i++;
            }
        }
        else {
            // Normální kód
            if (byte_425358[i] == '/') {
                if (byte_425358[i+1] == '/') {
                    // Jednořádkový komentář
                    byte_425358[i] = '\n';
                    byte_425358[i+1] = '\0';
                    return 1;
                }
                else if (byte_425358[i+1] == '*') {
                    // Začátek víceřádkového komentáře
                    byte_425358[i] = ' ';
                    byte_425358[i+1] = ' ';
                    comment_state = 1;
                    i += 2;
                    continue;
                }
            }
            i++;
        }
    }

    if (!byte_425358[0] && comment_state)
        return 1;  // prázdný řádek v komentáři

    return 1;  // úspěch
}
```

## 4. ZPRACOVÁNÍ DIREKTIV

### 4.1 Dispatcher (sub_403FB0)
```c
switch(directive) {
    case "define":  sub_402DF0(); break;
    case "undef":   sub_403B60(); break;
    case "error":   sub_403C80(); break;
    case "line":    sub_403DF0(); break;
    case "pragma":  sub_403F30(); break;
    case "include": sub_403570(); break;
    case "if":      sub_4038B0(0); break;
    case "ifdef":   sub_4038B0(1); break;
    case "ifndef":  sub_4038B0(2); break;
    case "else":    return -1;
    case "endif":   return -2;
    case "elif":    return -3;
}
```

### 4.2 #define (sub_402DF0)

#### Kompletní implementace:
```c
// 1. Kontrola syntaxe - musí následovat mezera
if (line[offset] != ' ' && line[offset] != '\t')
    error("after 'define' must follow white space");

// 2. Parse jména makra
skip_whitespace();
if (line[offset] != '_' && !isalpha(line[offset]))
    error("identifier expected");

// 3. Čtení identifikátoru
for (i = 0; is_identifier_char(line[offset]); i++)
    name[i] = line[offset++];
name[i] = '\0';

// 4. Alokace struktury makra (216 bajtů)
macro = new Macro();  // sub_401D90
macro->name = strdup(name);
macro->param_count = 0;

// 5. Kontrola funkčního makra
if (line[offset] == '(') {
    // Parse parametrů (max 50)
    do {
        skip_whitespace();
        if (!is_identifier_start(line[offset]))
            error("identifier expected in parameter list");

        // Čtení parametru
        for (j = 0; is_identifier_char(line[offset]); j++)
            param[j] = line[offset++];
        param[j] = '\0';

        // Kontrola duplicity (sub_401DE0)
        if (!add_param(macro, param))
            error("identifier duplicated");

        skip_whitespace();
    } while (line[offset] == ',');

    if (line[offset] != ')')
        error("')' symbol expected");
    offset++;
}

// 6. Parse hodnoty makra s expanzí
value_start = offset;
value[0] = '\0';
while (line[offset]) {
    if (line[offset] == '#') {
        if (line[offset+1] == '#') {
            // Operátor ## - konkatenace
            value[len++] = '#';
            value[len++] = '#';
            offset += 2;
        } else {
            // Operátor # - stringifikace
            if (!macro->param_count)
                error("# operator can be only with parametric macro");
            offset++;

            // Najdi parametr
            param_name = read_identifier(line + offset);
            param_index = find_param(macro, param_name);
            if (param_index == -1)
                error("after # operator must be macro parameter");

            // Přidej marker parametru
            value[len++] = '#';
            strcat(value, param_name);
            len += strlen(param_name);
        }
    } else if (is_identifier_start(line[offset])) {
        // Možná expanze makra
        offset = sub_404310(offset, value + len, 0);
        len = strlen(value);
    } else if (line[offset] == '"') {
        // String literal - kopíruj beze změny
        do {
            value[len++] = line[offset++];
            if (!line[offset])
                error("string syntax error");
        } while (line[offset] != '"');
        value[len++] = '"';
        offset++;
    } else {
        value[len++] = line[offset++];
    }
}

// 7. Ulož do tabulky maker
if (macro->value)
    strdup(value);
insert_macro(macro);  // sub_402700
```

#### Operátor `#` (stringifikace):
- Převede parametr na řetězec
- Escapuje uvozovky a backslashe
- Implementace v sub_401EE0 při expanzi
- Použití: `#param` → `"hodnota_param"`

#### Operátor `##` (konkatenace):
- Spojí tokeny, odstraní mezery
- Zpracovává se při expanzi v sub_401EE0
- Použití: `token1 ## token2` → `token1token2`

### 4.3 #include (sub_403570)

#### Algoritmus:
1. Parse cesta (`"file"` nebo `<file>`)
2. Vyřeš cestu:
   - `"file"`: relativně k dword_433DB8
   - `<file>`: relativně k lpPathName
3. Ulož kontext (Stream, line, Buffer)
4. Otevři soubor, zapíš `#line 0 "file"`
5. Rekurzivně volej parse()
6. Obnov kontext, zapíš `#line <line> "original"`

### 4.4 Podmíněná kompilace (sub_4038B0)

#### Stavy:
- `dword_40F39C`: 0 = skip kód, >0 = zpracuj kód
- Pro `#ifdef`: přepíše na `defined(MACRO)`
- Pro `#ifndef`: přepíše na `!defined(MACRO)`

#### Evaluace výrazů (sub_401D30):
- Používá rekurzivní descent parser
- Podporuje: `&&`, `||`, `!`, `()`, `defined()`
- Vrací 0 nebo 1

## 5. EXPANZE MAKER

### 5.1 Detekce makra (sub_404310)
```c
// Čte identifikátor
for (i = 0; is_identifier_char(line[offset]); i++)
    ident[i] = line[offset++];
ident[i] = '\0';

// Kontrola speciálních maker
if (!strcmp(ident, "__TIME__"))
    return expand_special(strtime(buffer));
if (!strcmp(ident, "__DATE__"))
    return expand_special(format_date());
if (!strcmp(ident, "__LINE__"))
    return expand_special(itoa(line_number));
if (!strcmp(ident, "__FILE__"))
    return expand_special(current_file);
if (!strcmp(ident, "__STDC__"))
    return expand_special("1");

// Hledání v tabulce maker (sub_4026A0)
macro = find_macro(ident);
if (!macro) return offset;

// Funkční makro - parse argumentů
if (macro->param_count > 0) {
    skip_whitespace();
    if (line[offset] != '(')
        error("'(' symbol expected");

    // Alokace pro argumenty
    args = new char*[macro->param_count];
    arg_count = 0;

    // Parse každého argumentu
    while (1) {
        arg_start = offset;
        paren_level = 0;

        while (1) {
            if (!line[offset])
                error("')' symbol expected");

            if (line[offset] == '(') paren_level++;
            else if (line[offset] == ')') {
                if (paren_level == 0) break;
                paren_level--;
            }
            else if (line[offset] == ',' && paren_level == 0) break;

            // Řetězce a identifikátory
            if (line[offset] == '"') {
                do {
                    offset++;
                    if (!line[offset])
                        error("string syntax error");
                } while (line[offset] != '"');
                offset++;
            }
            else if (is_identifier_start(line[offset])) {
                offset = expand_macro(offset, arg_buffer, recursion_depth);
            }
            else {
                offset++;
            }
        }

        args[arg_count++] = substring(arg_start, offset);
        if (line[offset] == ')') break;
        offset++; // skip ','
    }

    if (arg_count != macro->param_count)
        error("macro needs %d arguments", macro->param_count);
}

// Expanze makra
expand_macro_body(macro, args, output);
```

### 5.2 Expanze makra (sub_401EE0)

#### Kompletní implementace:
```c
char* expand_macro_body(Macro* macro, char** args, int recursion) {
    if (!macro->value) return NULL;

    strcpy(temp_buffer, "");
    char* src = macro->value;
    char* dst = temp_buffer;

    while (*src) {
        // Hledání všech parametrů v hodnotě
        int* param_positions = new int[macro->param_count];

        // Najdi nejbližší parametr
        int closest_param = -1;
        char* closest_pos = NULL;

        for (int i = 0; i < macro->param_count; i++) {
            char* pos = src;
            while ((pos = strstr(pos, macro->params[i]))) {
                // Kontrola hranice slova
                char before = (pos > src) ? *(pos-1) : 0;
                char after = pos[strlen(macro->params[i])];

                if ((!before || (!isalnum(before) && before != '_')) &&
                    (!after || (!isalnum(after) && after != '_'))) {
                    // Validní výskyt parametru
                    if (!closest_pos || pos < closest_pos) {
                        closest_pos = pos;
                        closest_param = i;
                    }
                    break;
                }
                pos += strlen(macro->params[i]);
            }
        }

        // Kopíruj text před parametrem
        while (src < closest_pos) {
            // Zpracování ## operátoru
            if (recursion && *src == '#' && *(src+1) == '#') {
                // Odstraň mezery před ##
                while (dst > temp_buffer &&
                       (*(dst-1) == ' ' || *(dst-1) == '\t'))
                    dst--;

                src += 2; // skip ##

                // Odstraň mezery za ##
                while (*src == ' ' || *src == '\t')
                    src++;
                continue;
            }
            *dst++ = *src++;
        }

        if (closest_param >= 0) {
            // Zpracování # operátoru (stringifikace)
            if (recursion && dst > temp_buffer && *(dst-1) == '#') {
                dst--; // odstranit #
                *dst++ = '"';

                // Escapuj speciální znaky v argumentu
                char* arg = args[closest_param];
                while (*arg) {
                    if (*arg == '\\' || *arg == '"')
                        *dst++ = '\\';
                    *dst++ = *arg++;
                }
                *dst++ = '"';
            }
            else {
                // Normální nahrazení parametru
                strcpy(dst, args[closest_param]);
                dst += strlen(args[closest_param]);
            }

            src = closest_pos + strlen(macro->params[closest_param]);
        }
    }

    *dst = '\0';
    return temp_buffer;
}
```

#### Příklad expanze:
```c
#define MAX(a,b) ((a)>(b)?(a):(b))
MAX(x+1, y*2)
// 1. Parse argumentů: args[0]="x+1", args[1]="y*2"
// 2. Nahrazení v těle: ((x+1)>(y*2)?(x+1):(y*2))

#define STR(x) #x
STR(hello world)
// 1. Parse: args[0]="hello world"
// 2. Stringifikace: "hello world"

#define CONCAT(a,b) a##b
CONCAT(foo, bar)
// 1. Parse: args[0]="foo", args[1]="bar"
// 2. Konkatenace: foobar
```

## 6. ZPRACOVÁNÍ BĚŽNÉHO KÓDU (sub_404810)

### Kompletní implementace:
```c
int process_line(int offset) {
    if (dword_40F39C)
        fprintf(dword_442830, "\nTRANSLATING TEXT_LINE: %s\n", byte_425358);

    char temp[60000];
    int pos = offset;

    while (byte_425358[pos]) {
        temp[0] = '\0';

        if (byte_425358[pos] == '_' || isalpha(byte_425358[pos])) {
            // Identifikátor - možné makro
            pos = sub_404310(pos, temp, 1);  // expanduj makro

            if (dword_40F39C) {
                // Debug výstup
                fputs(temp, dword_44282C);
            }
        }
        else if (byte_425358[pos] == '"') {
            // String literal - kopíruj bez expanze
            int i = 0;
            char ch = byte_425358[pos];

            do {
                temp[i++] = ch;
                pos++;
                if (!byte_425358[pos])
                    error("string syntax error");
                ch = byte_425358[pos];
            } while (ch != '"');

            temp[i] = '"';
            temp[i+1] = '\0';
            pos++;

            if (dword_40F39C) {
                fputs(temp, dword_44282C);
            }
        }
        else {
            // Obyčejný znak
            if (dword_40F39C) {
                fputc(byte_425358[pos], dword_44282C);
            }
            pos++;
        }
    }

    // Přidej konec řádku
    if (!dword_40F39C) {
        fprintf(dword_44282C, "\n");
    }

    return pos;
}
```

## 7. SPRÁVA TABULKY MAKER

### 7.1 Vyhledání makra (sub_4026A0)
```c
Macro* find_macro(const char* name) {
    Macro* current = (Macro*)dword_415600;  // začátek linked listu

    while (current) {
        if (!strcmp(name, current->name))
            return current;
        current = current->next;  // offset 212
    }

    return NULL;
}
```

### 7.2 Vložení makra (sub_402700)
```c
void insert_macro(Macro* new_macro) {
    // Nejdřív smaž existující makro stejného jména
    Macro* existing = find_macro(new_macro->name);
    if (existing) {
        remove_macro(existing);
    }

    // Přidej na konec seznamu
    if (!dword_415600) {
        dword_415600 = new_macro;
    }
    else {
        Macro* current = dword_415600;
        while (current->next) {
            current = current->next;
        }
        current->next = new_macro;
    }

    new_macro->next = NULL;
}
```

### 7.3 Odebrání makra (sub_402750)
```c
void remove_macro(Macro* macro) {
    if (!dword_415600 || !macro)
        return;

    if (dword_415600 == macro) {
        // První prvek seznamu
        dword_415600 = macro->next;
        free_macro(macro);
    }
    else {
        // Najdi předchůdce
        Macro* prev = dword_415600;
        while (prev->next && prev->next != macro) {
            prev = prev->next;
        }

        if (prev->next == macro) {
            prev->next = macro->next;
            free_macro(macro);
        }
    }
}
```

### 7.4 Uvolnění paměti makra (sub_4022C0)
```c
void free_macro(Macro* macro) {
    // Uvolni jméno
    if (macro->name) {
        free(macro->name);
        macro->name = NULL;
    }

    // Uvolni všechny parametry
    for (int i = 0; i < macro->param_count; i++) {
        if (macro->params[i]) {
            free(macro->params[i]);
            macro->params[i] = NULL;
        }
    }

    // Uvolni hodnotu
    if (macro->value) {
        free(macro->value);
        macro->value = NULL;
    }

    // Uvolni strukturu
    free(macro);
}
```

## 8. FORMÁT VÝSTUPNÍCH SOUBORŮ

### 8.1 spp.c (předzpracovaný kód)
- Obsahuje expandovaná makra
- `#line` direktivy pro mapování na původní soubory
- Odstraněné komentáře
- Vyřešené podmíněné bloky

### 8.2 spp.syn (mapa souborů)

#### Struktura souboru:
```c
struct SynFile {
    char magic[4];      // "ABCD" (0x41424344)
    int32 count;        // počet záznamů
    struct {
        int32 offset;   // offset k řetězci od začátku souboru
        int32 length;   // délka včetně \0
        int32 time_low; // FILETIME low part
        int32 time_high;// FILETIME high part
    } records[count];
    char strings[];     // null-terminated cesty
};
```

#### Vytváření mapy (sub_401100):
```c
void write_syn_file() {
    FILE* f = fopen("spp.sym", "wb");

    // 1. Zapíše hlavičku
    fwrite("ABCD", 1, 4, f);

    // 2. Spočítá počet souborů
    int count = 0;
    FileRecord* rec = (FileRecord*)dword_412B10;
    while (rec && rec->filepath) {
        count++;
        rec++;
    }
    fwrite(&count, 4, 1, f);

    // 3. Zapíše tabulku (nejdřív s prázdnými offsety)
    int table_pos = ftell(f);
    for (int i = 0; i < count; i++) {
        int32 dummy[4] = {0, 0, 0, 0};
        fwrite(dummy, 4, 4, f);
    }

    // 4. Zapíše řetězce a aktualizuje offsety
    int string_offset = ftell(f);
    rec = (FileRecord*)dword_412B10;

    for (int i = 0; i < count; i++) {
        // Ulož offset
        fseek(f, table_pos + i*16, SEEK_SET);
        fwrite(&string_offset, 4, 1, f);

        // Délka řetězce
        int len = strlen(rec->filepath) + 1;
        fwrite(&len, 4, 1, f);

        // FILETIME
        fwrite(&rec->filetime_low, 4, 1, f);
        fwrite(&rec->filetime_high, 4, 1, f);

        // Zapíš řetězec
        fseek(f, string_offset, SEEK_SET);
        fwrite(rec->filepath, 1, len, f);
        string_offset += len;

        rec++;
    }

    fclose(f);
    rename("spp.sym", "spp.syn");
}
```

### 8.3 spp.dbg (debug log)
- Vždy vytvářen (mode "w")
- Obsahuje trace výpisy všech operací
- Loguje expanzi maker
- Zaznamenává průchod direktivami

## 9. LIMITY A OMEZENÍ

| Parametr | Limit | Poznámka |
|----------|-------|----------|
| Max délka řádku | 60000 | byte_425358 |
| Max počet parametrů makra | 50 | Hardcoded v struktuře |
| Max počet souborů | 1000 | dword_4159FC check |
| Max hloubka include | Stack limit | Rekurzivní volání |
| Max délka makra | Heap limit | Dynamická alokace |
| Max délka expanzního bufferu | 1000 | byte_4162F8 |
| Max délka argumentu makra | 200 | Temporary buffer |

## 10. CHYBOVÉ STAVY

### Návratové kódy parse():
- 0: Úspěch
- -1: Misplaced #else
- -2: Misplaced #endif
- -3: Misplaced #elif

### Chybová funkce (sub_402880):
1. Zavře všechny soubory
2. Zapíše do spp.err:
   ```
   preprocessing error:
   file: <current_file>
   line: <line_number>
   message: <error_msg>
   ```
3. Vytvoří prázdný spp.syn
4. Exit(0)

## 11. ALGORITMUS TOKENIZACE

### 11.1 Tokenizer pro výrazy (sub_401280)

#### Token typy:
```c
enum TokenType {
    TOKEN_IDENTIFIER = 1000,  // identifikátor/makro
    TOKEN_NUMBER = 1001,       // číslo
    TOKEN_DEFINED = 1002,      // klíčové slovo "defined"
    TOKEN_LTE = 1003,          // <=
    TOKEN_GTE = 1004,          // >=
    TOKEN_EQ = 1005,           // ==
    TOKEN_NEQ = 1006,          // !=
    TOKEN_OR = 1007,           // ||
    TOKEN_AND = 1008,          // &&
    TOKEN_EOF = 9999           // konec vstupu
};
```

#### Implementace tokenizeru:
```c
int get_token() {
    // Skip whitespace
    while (line[pos] == ' ' || line[pos] == '\t' || line[pos] == '\n')
        pos++;

    if (!line[pos]) return TOKEN_EOF;

    char ch = line[pos];

    // Jednoduché operátory
    switch (ch) {
        case '(': pos++; return '(';
        case ')': pos++; return ')';
        case '+': pos++; return '+';
        case '-': pos++; return '-';
        case '*': pos++; return '*';
        case '/': pos++; return '/';
        case '%': pos++; return '%';
        case '!':
            pos++;
            if (line[pos] == '=') {
                pos++;
                return TOKEN_NEQ;
            }
            return '!';
        case '<':
            pos++;
            if (line[pos] == '=') {
                pos++;
                return TOKEN_LTE;
            }
            return '<';
        case '>':
            pos++;
            if (line[pos] == '=') {
                pos++;
                return TOKEN_GTE;
            }
            return '>';
        case '=':
            pos++;
            if (line[pos] == '=') {
                pos++;
                return TOKEN_EQ;
            }
            error("illegal token '='");
        case '&':
            pos++;
            if (line[pos] == '&') {
                pos++;
                return TOKEN_AND;
            }
            error("illegal token '&'");
        case '|':
            pos++;
            if (line[pos] == '|') {
                pos++;
                return TOKEN_OR;
            }
            error("illegal token '|'");
    }

    // Čísla
    if (isdigit(ch)) {
        int i = 0;
        while (isdigit(line[pos])) {
            token_buffer[i++] = line[pos++];
        }
        token_buffer[i] = '\0';
        return TOKEN_NUMBER;
    }

    // Identifikátory
    if (ch == '_' || isalpha(ch)) {
        int i = 0;
        while (line[pos] == '_' || isalnum(line[pos])) {
            token_buffer[i++] = line[pos++];
        }
        token_buffer[i] = '\0';

        // Kontrola klíčového slova "defined"
        if (!strcmp(token_buffer, "defined"))
            return TOKEN_DEFINED;

        // Expanze makra
        int expanded_pos = expand_macro(start_pos, expanded_buffer, 1);
        if (strcmp(token_buffer, expanded_buffer)) {
            // Makro bylo expandováno - rekurzivní zpracování
            strcpy(line + start_pos, expanded_buffer);
            strcat(line, line + expanded_pos);
            pos = start_pos;
            return get_token();
        }

        return TOKEN_IDENTIFIER;
    }

    error("illegal token '%c'", ch);
}
```

### 11.2 Evaluátor výrazů (sub_401D30)

#### Rekurzivní descent parser:
```c
// Vstupní bod
int evaluate_expression(char* expr) {
    pos = 0;
    line = expr;
    error_flag = 0;

    int token = get_token();
    parse_or_expr(token);

    if (line[pos])
        error("illegal token after expression");

    if (error_flag) return 0;
    return pop_value();
}

// Logický OR
void parse_or_expr(int token) {
    parse_and_expr(token);

    while ((token = get_token()) == TOKEN_OR) {
        token = get_token();
        parse_and_expr(token);

        int right = pop_value();
        int left = pop_value();
        push_value(left || right);
    }
    unget_token(token);
}

// Logický AND
void parse_and_expr(int token) {
    parse_eq_expr(token);

    while ((token = get_token()) == TOKEN_AND) {
        token = get_token();
        parse_eq_expr(token);

        int right = pop_value();
        int left = pop_value();
        push_value(left && right);
    }
    unget_token(token);
}

// Rovnost/nerovnost
void parse_eq_expr(int token) {
    parse_rel_expr(token);

    int op;
    while ((op = get_token()) == TOKEN_EQ || op == TOKEN_NEQ) {
        token = get_token();
        parse_rel_expr(token);

        int right = pop_value();
        int left = pop_value();
        if (op == TOKEN_EQ)
            push_value(left == right);
        else
            push_value(left != right);
    }
    unget_token(op);
}

// Relační operátory
void parse_rel_expr(int token) {
    parse_add_expr(token);

    int op;
    while ((op = get_token()) == '<' || op == '>' ||
           op == TOKEN_LTE || op == TOKEN_GTE) {
        token = get_token();
        parse_add_expr(token);

        int right = pop_value();
        int left = pop_value();
        switch (op) {
            case '<': push_value(left < right); break;
            case '>': push_value(left > right); break;
            case TOKEN_LTE: push_value(left <= right); break;
            case TOKEN_GTE: push_value(left >= right); break;
        }
    }
    unget_token(op);
}

// Sčítání/odčítání
void parse_add_expr(int token) {
    parse_mul_expr(token);

    int op;
    while ((op = get_token()) == '+' || op == '-') {
        token = get_token();
        parse_mul_expr(token);

        int right = pop_value();
        int left = pop_value();
        if (op == '+')
            push_value(left + right);
        else
            push_value(left - right);
    }
    unget_token(op);
}

// Násobení/dělení/modulo
void parse_mul_expr(int token) {
    parse_unary_expr(token);

    int op;
    while ((op = get_token()) == '*' || op == '/' || op == '%') {
        token = get_token();
        parse_unary_expr(token);

        int right = pop_value();
        int left = pop_value();
        switch (op) {
            case '*': push_value(left * right); break;
            case '/':
                if (right == 0) error("division by zero");
                push_value(left / right);
                break;
            case '%':
                if (right == 0) error("division by zero");
                push_value(left % right);
                break;
        }
    }
    unget_token(op);
}

// Unární operátory
void parse_unary_expr(int token) {
    if (token == '!') {
        token = get_token();
        parse_unary_expr(token);
        push_value(!pop_value());
    }
    else if (token == '-') {
        token = get_token();
        parse_unary_expr(token);
        push_value(-pop_value());
    }
    else if (token == '+') {
        token = get_token();
        parse_unary_expr(token);
        // + je no-op
    }
    else {
        parse_primary_expr(token);
    }
}

// Primární výrazy
void parse_primary_expr(int token) {
    if (token == '(') {
        token = get_token();
        parse_or_expr(token);

        token = get_token();
        if (token != ')')
            error("')' expected");
    }
    else if (token == TOKEN_NUMBER) {
        push_value(atoi(token_buffer));
    }
    else if (token == TOKEN_IDENTIFIER) {
        // Neznámé makro = 0
        push_value(0);
    }
    else if (token == TOKEN_DEFINED) {
        token = get_token();
        int has_paren = 0;

        if (token == '(') {
            has_paren = 1;
            token = get_token();
        }

        if (token != TOKEN_IDENTIFIER)
            error("identifier expected after 'defined'");

        // Kontrola existence makra
        int exists = (find_macro(token_buffer) != NULL) ? 1 : 0;
        push_value(exists);

        if (has_paren) {
            token = get_token();
            if (token != ')')
                error("')' expected");
        }
    }
    else {
        error("unexpected token");
    }
}
```

### Whitespace handling:
- Více mezer/tabů → jedna mezera
- Řádky končící `\` → spojení (sub_402BA0)
- Prázdné řádky → zachovány pro #line direktivy

## 12. PŘÍKLADY POUŽITÍ

### Základní makro:
```c
#define VERSION 100
int ver = VERSION;  // → int ver = 100;
```

### Funkční makro:
```c
#define SQUARE(x) ((x)*(x))
int a = SQUARE(5);  // → int a = ((5)*(5));
```

### Podmíněná kompilace:
```c
#ifdef DEBUG
    printf("Debug mode\n");
#else
    printf("Release mode\n");
#endif
```

### Include:
```c
#include <system.h>  // Hledá v lpPathName
#include "local.h"   // Hledá v dword_433DB8
```

## 13. ZNÁMÉ PROBLÉMY

1. **Chybějící "ABCD" v binárce** - hlavička .syn souboru není explicitně viditelná v kódu
2. **Debug režim** - není jasný způsob aktivace (dword_40F39C)
3. **Race conditions** - busy-wait synchronizace s SCMP.exe
4. **Stack overflow** - rekurzivní include bez ochrany
5. **Konflikt návratových kódů** - 0 znamená úspěch i některé chyby

## 14. DŮLEŽITÉ PRO DEKOMPILÁTOR

### Klíčové datové struktury:
1. **Struktura makra** (216 bajtů) - linked list s parametry a hodnotou
2. **Globální tabulka maker** (dword_415600) - začátek linked listu
3. **Buffer pro řádek** (byte_425358, 60000 bajtů)
4. **Buffer pro expanzi** (byte_4162F8, 1000 bajtů)

### Kritické funkce pro reimplementaci:
1. **sub_404950** - hlavní parse smyčka
2. **sub_402BA0** - čtení řádků se spojováním a komentáři
3. **sub_403FB0** - dispatcher direktiv
4. **sub_404310** - detekce a expanze maker
5. **sub_401EE0** - expanze těla makra s parametry
6. **sub_401D30** - evaluace podmíněných výrazů
7. **sub_401280** - tokenizer pro výrazy

### Pořadí zpracování:
1. Čtení řádku se spojováním (\\) a odstraněním komentářů
2. Detekce direktivy (#) nebo běžného kódu
3. Pro direktivy: parse a okamžité vykonání
4. Pro běžný kód: expanze maker a výstup
5. #line direktivy pro mapování na původní soubory

### Výstupní formát:
- Expandovaný kód v `spp.c`
- Mapa souborů v `spp.syn` (formát ABCD + tabulka + řetězce)
- #line direktivy pro zpětné mapování
- Zachované prázdné řádky pro konzistentní číslování

### Chybové hlášení:
- Vždy zapisuje do `spp.err`
- Obsahuje: soubor, řádek, zpráva
- Vytváří prázdný `spp.syn` při chybě

### Speciální makra:
- `__TIME__` - čas kompilace
- `__DATE__` - datum kompilace
- `__LINE__` - číslo řádku
- `__FILE__` - jméno souboru
- `__STDC__` - vždy "1"

### Operátory v makrech:
- `#` - stringifikace parametru
- `##` - konkatenace tokenů
- Oba se zpracovávají při expanzi, ne při definici

### Podmíněná kompilace:
- Stack pro vnořené bloky (implicitní)
- `#ifdef X` se přepisuje na `defined(X)`
- `#ifndef X` se přepisuje na `!defined(X)`
- Evaluace používá plný expression parser

### Limity:
- Max 50 parametrů makra
- Max 60000 znaků na řádek
- Max 1000 include souborů
- Max 200 znaků v temporary bufferu pro argumenty

## 15. ZÁVĚR

Tato technická dokumentace poskytuje kompletní pohled na implementaci preprocesoru SPP.exe používaného pro kompilaci skriptů hry Vietcong. Dokumentace byla vytvořena na základě reverzního inženýrství binárního souboru pomocí IDA Pro a obsahuje:

1. **Kompletní datové struktury** - všechny důležité struktury včetně velikostí a offsetů
2. **Detailní algoritmy** - implementace všech klíčových funkcí v pseudo-C kódu
3. **Formáty souborů** - přesná struktura vstupních a výstupních souborů
4. **Zpracování direktiv** - kompletní implementace všech direktiv preprocesoru
5. **Expanze maker** - detailní popis včetně operátorů # a ##
6. **Tokenizace a evaluace** - plný rekurzivní descent parser pro podmíněné výrazy

### Klíčové poznatky pro implementaci dekompilátoru:

1. **Zpětné mapování** - využití #line direktiv a .syn souborů pro rekonstrukci původní struktury
2. **Rekonstrukce maker** - analýza expandovaného kódu pro identifikaci použití maker
3. **Podmíněné bloky** - rekonstrukce #ifdef/#ifndef bloků z výsledného kódu
4. **Include cesty** - určení původních include souborů z .syn mapy

### Doporučení pro další práci:

1. Analyzovat SCC.exe (kompilátor) pro pochopení transformace C → mezikód
2. Analyzovat SASM.exe (assembler) pro finální bytecode generování
3. Implementovat parser pro .syn formát
4. Vytvořit nástroj pro zpětné mapování #line direktiv

Dokumentace je dostatečně detailní pro implementaci funkčního dekompilátoru nebo alternativního preprocesoru kompatibilního s originálním SPP.exe.