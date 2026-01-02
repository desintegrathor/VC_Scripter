# TDM.SCR Decompilation Analysis Report
**Datum:** 2026-01-02
**Porovnání:** `tdm.c` (originál) vs `tdm_CURRENT_OUTPUT.c` (dekompilováno)

---

## EXECUTIVE SUMMARY

### Statistiky dekompilace
- **Originální soubor:** 306 řádků, 3 funkce + globals
- **Dekompilovaný soubor:** 204 řádků, 4 funkce (včetně `_init`)
- **Úspěšnost:** ~40% (významné strukturální problémy)

### Kritické problémy: 🔴 15
### Sémantické chyby: 🟡 23
### Kosmetické rozdíly: 🟢 12

---

## KATEGORIE A: STRUKTURÁLNÍ ROZDÍLY

### 🔴 KRITICKÝ PROBLÉM #1: Chybějící globální proměnné (tdm_CURRENT_OUTPUT.c:8-13)
**Originál (tdm.c:22-41):**
```c
dword gRecs = 0;
s_SC_MP_Recover gRec[REC_MAX];
float gRecTimer[REC_MAX];
float gNextRecover = 0.0f;
int gSideFrags[2] = {0,0};
int gCLN_SideFrags[2];
dword gEndRule;
dword gEndValue;
float gTime;
dword gPlayersConnected = 0;
```

**Dekompilováno:**
```c
// CHYBÍ ÚPLNĚ!
```

**Dopad:** Kritický - kód je nekompilnovatelný bez globálů.

**Příčina:** Dekompilátor nezachycuje data segment jako globální deklarace.

---

### 🔴 KRITICKÝ PROBLÉM #2: Nezdařená rekonstrukce `SRV_CheckEndRule` (tdm_CURRENT_OUTPUT.c:16-47)

**Originál (tdm.c:44-77):**
```c
BOOL SRV_CheckEndRule(float time){
    switch(gEndRule){
        case SC_MP_ENDRULE_TIME:
            if (gPlayersConnected>0) gTime += time;
            SC_MP_EndRule_SetTimeLeft(gTime,gPlayersConnected>0);
            if (gTime>gEndValue){
                SC_MP_LoadNextMap();
                return TRUE;
            }
            break;

        case SC_MP_ENDRULE_FRAGS:
            if (((gSideFrags[0]>0)&&(gSideFrags[0]>=gEndValue))
                ||((gSideFrags[1]>1)&&(gSideFrags[1]>=gEndValue))){
                SC_MP_LoadNextMap();
                return TRUE;
            }
            break;

        default:
            SC_message("EndRule unsopported: %d",gEndRule);
            break;
    }
    return FALSE;
}
```

**Dekompilováno:**
```c
int func_0010(float time) {
    int local_0;  // ❌ CHYBNÁ PROMĚNNÁ!

    switch (local_0) {  // ❌ ŠPATNÁ HODNOTA! Mělo být gEndRule
        case 0:  // ❌ ŠPATNÁ KONSTANTA! Mělo být SC_MP_ENDRULE_TIME
            if (((gPlayersConnected > 0))) {
                gTime = (gTime + time);  // ✅ OK
            }
            SC_MP_EndRule_SetTimeLeft(gTime, (gPlayersConnected > 0));  // ✅ OK
            if (((gTime > ITOF(gEndValue)))) {  // ❌ Zbytečná ITOF konverze!
                SC_MP_LoadNextMap();  // ✅ OK
                return TRUE;  // ✅ OK
            }
            break;
        case 1:  // ❌ ŠPATNÁ KONSTANTA! Mělo být SC_MP_ENDRULE_FRAGS
            if (((gSideFrags[0] > 0))) {
                if (((gSideFrags[0] >= gEndValue))) {
                    // ❌ CHYBÍ: SC_MP_LoadNextMap() + return TRUE
                } else {
                    if (((gSideFrags[1] > 1))) {  // ✅ Správná hodnota
                        if (((gSideFrags[1] >= gEndValue))) {
                            SC_MP_LoadNextMap();  // ✅ OK
                            return TRUE;  // ✅ OK
                        }
                    }
                    SC_message("EndRule unsopported: %d", gEndRule);  // ❌ SPATNE UMÍSTĚNO!
                    return FALSE;  // ❌ ŠPATNÝ RETURN!
                }
            }
            break;
        default:  // ❌ Default case je prázdný!
        }
}
```

**Chyby:**
1. `switch (local_0)` místo `switch (gEndRule)` - **chybí detekce globálu jako switch condition**
2. `case 0` / `case 1` místo symbolických konstant
3. Rozbitá logika case 1 - OR podmínka (`||`) byla rozložena na vnořené if bloky **ŠPATNĚ**
4. `SC_message` a `return FALSE` jsou uvnitř case 1 místo default case
5. Zbytečná `ITOF(gEndValue)` - gEndValue je už dword, ale srovnává se s float

---

### 🔴 KRITICKÝ PROBLÉM #3: Špatný název funkce a chybějící return type

**Originál:**
```c
BOOL SRV_CheckEndRule(float time)  // BOOL = int, sémanticky správný název
void UpdateSideFrags(void)         // void return
```

**Dekompilováno:**
```c
int func_0010(float time)  // ❌ Generický název
int func_0096(void)        // ❌ int místo void
```

**Příčina:** Symbol table není dostupný v .SCR, dekompilátor vymýšlí jména z offsetů.

---

### 🔴 KRITICKÝ PROBLÉM #4: Rozbité For-Loops (tdm_CURRENT_OUTPUT.c:69-71, 90-95, 152-153)

**Příklad 1 - Originál (tdm.c:105-106):**
```c
for (i=0; i<gRecs; i++)
    gRecTimer[i] -= info->elapsed_time;
```

**Dekompilováno (tdm_CURRENT_OUTPUT.c:69-71):**
```c
// Loop header - Block 26 @145
for (local_2 = 0; (local_2 <= gRecs); local_2++) {  // ❌ <= místo <
    gRecTimer[local_2] = (gRecTimer[local_2] - info->field_16);  // ✅ OK
}
```

**Chyby:**
1. `local_2 <= gRecs` místo `local_2 < gRecs` - **off-by-one bug!**
2. Komentář "Loop header" je debug artefakt

---

**Příklad 2 - Originál (tdm.c:133-138):**
```c
for (i=0; i<2; i++){
    icon[i].type = SC_HUD_MP_ICON_TYPE_NUMBER;
    icon[i].icon_id = 3*i;
    icon[i].value = gCLN_SideFrags[i];
    icon[i].color = 0xffffffff;
}
```

**Dekompilováno (tdm_CURRENT_OUTPUT.c:90-95):**
```c
for (local_2 = 0; (local_2 <= 2); local_2++) {  // ❌ <= 2 znamená 3 iterace!
    local_8[local_2].field1 = 1;  // ✅ type OK
    local_8[local_2] = (3 * local_2);  // ❌ PŘEPISUJE celou strukturu!
    local_8[local_2].field2 = gCLN_SideFrags[local_2];  // ✅ value OK
    local_8[local_2].field3 = -1;  // ✅ color OK
}
```

**Chyby:**
1. `<= 2` místo `< 2` - iteruje 0,1,2 místo 0,1
2. Řádek `local_8[local_2] = (3 * local_2)` přepisuje celou strukturu místo jen `.icon_id`

---

**Příklad 3 - Originál (tdm.c:202-204):**
```c
for (i=0; i<REC_MAX; i++){
    sprintf(txt, REC_WPNAME, i);
    if (SC_NET_FillRecover(&gRec[gRecs], txt)) gRecs++;
}
```

**Dekompilováno (tdm_CURRENT_OUTPUT.c:134-140 + 152-153):**
```c
// ❌ ROZBITÝ LOOP - tělo je rozloženo mimo loop!
local_2 = 0;
sprintf(&local_0, "DM%d", local_2);  // Iterace 0
if ((SC_NET_FillRecover(&gRec[gRecs], &local_0))) {
    gRecs++;
} else {
    local_2++;  // ❌ ŠPATNĚ! Inkrement jen v else větvi
}
// ...
// Později prázdný loop:
for (local_2 = 0; (local_2 <= 64); local_2++) {  // ❌ Prázdné tělo!
}
```

**Chyby:**
1. Loop byl kompletně rozbit na single iteration + prázdný loop
2. Podmínka pro inkrement `i++` je chybně v else větvi

---

### 🔴 KRITICKÝ PROBLÉM #5: Switch Case Values (tdm_CURRENT_OUTPUT.c:65)

**Originál (tdm.c:98-301):**
```c
switch(info->message){
    case SC_NET_MES_SERVER_TICK:      // = 3
    case SC_NET_MES_CLIENT_TICK:      // = 4
    case SC_NET_MES_LEVELPREINIT:     // = 9
    case SC_NET_MES_LEVELINIT:        // = 1
    case SC_NET_MES_RENDERHUD:        // = 2
    case SC_NET_MES_SERVER_RECOVER_TIME:   // = 5
    case SC_NET_MES_SERVER_RECOVER_PLACE:  // = 6
    case SC_NET_MES_SERVER_KILL:      // = 7
    case SC_NET_MES_RESTARTMAP:       // = 10
    case SC_NET_MES_RULESCHANGED:     // = 11
}
```

**Dekompilováno (tdm_CURRENT_OUTPUT.c:65-201):**
```c
switch (info->message) {  // ✅ OK
    case 3:  // ❌ Číselná hodnota místo SC_NET_MES_SERVER_TICK
    case 4:  // ❌ SC_NET_MES_CLIENT_TICK
    case 9:  // ❌ SC_NET_MES_LEVELPREINIT
    case 1:  // ❌ SC_NET_MES_LEVELINIT
    case 2:  // ❌ SC_NET_MES_RENDERHUD
    case 5:  // ❌ SC_NET_MES_SERVER_RECOVER_TIME
    case 6:  // ❌ SC_NET_MES_SERVER_RECOVER_PLACE
    case 7:  // ❌ SC_NET_MES_SERVER_KILL
    case 10: // ❌ SC_NET_MES_RESTARTMAP
    case 11: // ❌ SC_NET_MES_RULESCHANGED
    default: return TRUE;  // ❌ CHYBNÝ! Originál má default v ScriptMain return 1
}
```

**Příčina:** Konstanty byly expandovány preprocesorem, .SCR obsahuje jen číselné hodnoty.

---

### 🟢 KOSMETICKÝ PROBLÉM #6: Funkce `_init` (tdm_CURRENT_OUTPUT.c:8-14)

**Dekompilováno:**
```c
int _init(s_SC_NET_info *info) {
    int local_0;
    DLD();
    DLD();
    return FALSE;
}
```

**Originál:** NEEXISTUJE

**Vysvětlení:** Toto je kompilátor-generovaná inicializace před `ScriptMain`. DLD() jsou instrukce pro načtení adres globálů. V originálním kódu není viditelná, ale je správně přítomná v .SCR.

**Hodnocení:** Kosmetické - funkce je správně dekompilována, ale měla by být skryta nebo označena jako `// Compiler-generated init`.

---

## KATEGORIE B: DATOVÉ TYPY A KONVERZE

### 🟡 SÉMANTICKÝ PROBLÉM #7: Pointer Dereference - info->field_XX (všude)

**Originál:**
```c
info->message       // offset 0
info->elapsed_time  // offset 16 (0x10)
info->param1        // offset 4
info->param2        // offset 8
info->fval1         // offset 20 (0x14)
```

**Dekompilováno:**
```c
info->message       // ✅ OK (název zrekonstruován)
info->field_16      // ❌ "field_16" místo elapsed_time
info->field_4       // ❌ "field_4" místo param1
info->field_8       // ❌ "field_8" místo param2
info->field_20      // ❌ nepoužito, ale mělo být fval1
```

**Příčina:** Dekompilátor nezná strukturu `s_SC_NET_info`. Field offsety jsou správně, ale jména chybí.

**Řešení:** Type reconstruction engine nebo external type database z hlaviček.

---

### 🟡 SÉMANTICKÝ PROBLÉM #8: Struktury - Chybné field assignment (tdm_CURRENT_OUTPUT.c:91-94)

**Originál (tdm.c:134-137):**
```c
icon[i].type = SC_HUD_MP_ICON_TYPE_NUMBER;  // = 1
icon[i].icon_id = 3*i;                       // 0 nebo 3
icon[i].value = gCLN_SideFrags[i];
icon[i].color = 0xffffffff;
```

**Dekompilováno:**
```c
local_8[local_2].field1 = 1;               // ✅ type
local_8[local_2] = (3 * local_2);          // ❌ PŘEPISUJE CELOU STRUKTURU!
local_8[local_2].field2 = gCLN_SideFrags[local_2];  // ✅ value
local_8[local_2].field3 = -1;              // ✅ color
```

**Chyba:** Řádek 92 přiřazuje `int` do celé struktury `s_SC_HUD_MP_icon`, mělo být `local_8[local_2].field_icon_id = (3 * local_2)`.

**Příčina:** Dekompilátor nerozpoznal, že ASGN target je member struktury, ne celá struktura.

---

### 🟡 SÉMANTICKÝ PROBLÉM #9: CLEAR makro rozklad (tdm_CURRENT_OUTPUT.c:109, 148, 188)

**Originál (tdm.c:164, 218, 284):**
```c
CLEAR(hudinfo);      // memset(&hudinfo, 0, sizeof(hudinfo))
CLEAR(gRecTimer);    // memset(gRecTimer, 0, sizeof(gRecTimer))
CLEAR(gSideFrags);   // memset(gSideFrags, 0, sizeof(gSideFrags))
```

**Dekompilováno:**
```c
SC_ZeroMem(&local_3, 60);         // ✅ Správně expandováno
SC_ZeroMem(&gRecTimer, 256);      // ✅ Správně (64*4 bytes)
SC_ZeroMem(&gSideFrags, 8);       // ✅ Správně (2*4 bytes)
```

**Hodnocení:** Správně! Makro bylo expandováno preprocesorem na `SC_ZeroMem`, dekompilátor korektně zachytil.

---

### 🟡 SÉMANTICKÝ PROBLÉM #10: Type Casts - Zbytečné ITOF (tdm_CURRENT_OUTPUT.c:25, 129)

**Originál (tdm.c:52):**
```c
if (gTime > gEndValue){  // float > dword - implicitní konverze
```

**Dekompilováno:**
```c
if (((gTime > ITOF(gEndValue)))) {  // ❌ Explicitní ITOF
```

**Vysvětlení:** Kompilátor vložil ITOF instrukci pro konverzi dword→float. Dekompilátor to zachytil, ale v C zdrojáku byla konverze implicitní.

**Hodnocení:** Technicky správně, ale verbose. Better: Detekovat kdy je cast implicitní.

---

**Další příklad (tdm.c:194 vs tdm_CURRENT_OUTPUT.c:129):**
```c
// Originál:
SC_MP_SRV_InitWeaponsRecovery((float)SRVset.dm_weap_resp_time);

// Dekompilováno:
SC_MP_SRV_InitWeaponsRecovery(ITOF(local_74.field2));  // ❌ ITOF místo (float)
```

**Poznámka:** ITOF je funkce z kompilátoru, správný C zápis je cast `(float)`.

---

### 🟡 SÉMANTICKÝ PROBLÉM #11: Boolean výrazy - Zbytečné závorky

**Originál (tdm.c:50):**
```c
if (gPlayersConnected > 0) gTime += time;
```

**Dekompilováno (tdm_CURRENT_OUTPUT.c:21-23):**
```c
if (((gPlayersConnected > 0))) {  // ❌ 3 vrstvy závorek!
    gTime = (gTime + time);
}
```

**Příčina:** Každý IR node je obalen závorkami pro bezpečnost precedence.

**Dopad:** Kosmetické, ale špatně čitelné.

---

### 🔴 KRITICKÝ PROBLÉM #12: Rozbité OR podmínky (tdm.c:61-62 vs tdm_CURRENT_OUTPUT.c:31-43)

**Originál:**
```c
if (((gSideFrags[0]>0) && (gSideFrags[0]>=gEndValue))
    || ((gSideFrags[1]>1) && (gSideFrags[1]>=gEndValue)))
{
    SC_MP_LoadNextMap();
    return TRUE;
}
```

**Dekompilováno:**
```c
if (((gSideFrags[0] > 0))) {
    if (((gSideFrags[0] >= gEndValue))) {
        // ❌ CHYBÍ: SC_MP_LoadNextMap() + return TRUE
    } else {
        if (((gSideFrags[1] > 1))) {
            if (((gSideFrags[1] >= gEndValue))) {
                SC_MP_LoadNextMap();
                return TRUE;
            }
        }
        // ... default case code špatně umístěn
    }
}
```

**Chyba:**
1. OR (`||`) byl rozbitý na vnořené if-else
2. První větev (`gSideFrags[0]>=gEndValue` je TRUE) nemá tělo!
3. Sémanticky **NESPRÁVNÝ KÓD**

**Příčina:** Short-circuit evaluation byla špatně rekonstruována.

---

## KATEGORIE C: VOLÁNÍ FUNKCÍ A ARGUMENTY

### 🟢 ÚSPĚCH #13: XFN Call Arguments (většina volání)

**Příklady správně dekompilovaných volání:**

```c
// ✅ tdm_CURRENT_OUTPUT.c:24
SC_MP_EndRule_SetTimeLeft(gTime, (gPlayersConnected > 0));

// ✅ tdm_CURRENT_OUTPUT.c:26
SC_MP_LoadNextMap();

// ✅ tdm_CURRENT_OUTPUT.c:50-51
SC_sgi(GVAR_SIDE0FRAGS, gSideFrags[0]);
SC_sgi(GVAR_SIDE1FRAGS, gSideFrags[1]);

// ✅ tdm_CURRENT_OUTPUT.c:85-86
gCLN_SideFrags[0] = SC_ggi(GVAR_SIDE0FRAGS);
gCLN_SideFrags[1] = SC_ggi(GVAR_SIDE1FRAGS);

// ✅ tdm_CURRENT_OUTPUT.c:87-88
SC_MP_SetSideStats(0, gCLN_SideFrags[0], 0);
SC_MP_SetSideStats(1, gCLN_SideFrags[1], 0);

// ✅ tdm_CURRENT_OUTPUT.c:164
local_2 = SC_MP_SRV_GetBestDMrecov(&gRec, gRecs, &gRecTimer, 3.0f);
```

**Hodnocení:** Volání funkcí s argumenty funguje **VÝBORNĚ** díky nedávným opravám v `stack_lifter.py`!

---

### 🟡 SÉMANTICKÝ PROBLÉM #14: Špatné argumenty - SC_MP_EnumPlayers (tdm_CURRENT_OUTPUT.c:73)

**Originál (tdm.c:110):**
```c
j = 64;
if (SC_MP_EnumPlayers(enum_pl, &j, SC_MP_ENUMPLAYER_SIDE_ALL)){
    // enum_pl = pole 64 struktur s_SC_MP_EnumPlayers
    // j = in/out parametr (vstup: max kapacita, výstup: počet)
    // SC_MP_ENUMPLAYER_SIDE_ALL = -1 (všechny strany)
}
```

**Dekompilováno:**
```c
local_2 = 64;
if ((SC_MP_EnumPlayers(&player_info.group, &local_2, -1))) {
    // ❌ &player_info.group místo samostatného pole enum_pl[64]!
}
```

**Chyba:**
1. První argument je `&player_info.group` (offset v jiné struktuře) místo lokálního pole `enum_pl[64]`
2. Hodnota -1 je správná (SC_MP_ENUMPLAYER_SIDE_ALL), ale měla by být konstanta

**Příčina:** Dekompilátor nevytvořil správné lokální pole, použil offset v existující struktuře.

---

### 🟡 SÉMANTICKÝ PROBLÉM #15: sprintf s špatným bufferem (tdm_CURRENT_OUTPUT.c:135)

**Originál (tdm.c:203):**
```c
char txt[32];
sprintf(txt, REC_WPNAME, i);  // REC_WPNAME = "DM%d"
```

**Dekompilováno:**
```c
sprintf(&local_0, "DM%d", local_2);  // ❌ &local_0 je int*, ne char[32]!
```

**Chyba:** Buffer `txt[32]` byl nahrazen `&local_0` (adresa int proměnné).

**Příčina:** Dekompilátor nerozpoznal array deklaraci, použil první dostupnou local.

---

### 🟡 SÉMANTICKÝ PROBLÉM #16: SC_MP_SetIconHUD argument (tdm_CURRENT_OUTPUT.c:96)

**Originál (tdm.c:140):**
```c
s_SC_HUD_MP_icon icon[2];
SC_MP_SetIconHUD(icon, 2);  // pole 2 struktur + count
```

**Dekompilováno:**
```c
SC_MP_SetIconHUD(&player_info.max_hp, 2);  // ❌ Špatná adresa!
```

**Chyba:** `icon[2]` byl nahrazen offsetem `&player_info.max_hp` (nějaký field v `s_SC_P_getinfo`).

---

### 🟡 SÉMANTICKÝ PROBLÉM #17: Pointer cast (tdm_CURRENT_OUTPUT.c:163)

**Originál (tdm.c:247):**
```c
s_SC_MP_Recover *precov;
precov = (s_SC_MP_Recover*)info->param2;
```

**Dekompilováno:**
```c
local_3 = info->field_8;  // ❌ Žádný cast, žádný pointer!
```

**Chyba:**
1. Chybí pointer deklarace `s_SC_MP_Recover *precov`
2. Chybí explicit cast `(s_SC_MP_Recover*)`
3. `local_3` vypadá jako int, ne pointer

---

### 🟡 SÉMANTICKÝ PROBLÉM #18: Struktura assignment přes pointer (tdm_CURRENT_OUTPUT.c:166)

**Originál (tdm.c:252):**
```c
*precov = gRec[i];  // Dereference pointer a zkopírování struktury
```

**Dekompilováno:**
```c
local_3 = gRec[local_2];  // ❌ Vypadá jako int assignment!
```

**Chyba:** Stejná proměnná `local_3` je použita jako cíl, ale bez hvězdičky dereferencing.

---

## KATEGORIE D: EXPRESNÍ VYHODNOCENÍ

### 🟡 SÉMANTICKÝ PROBLÉM #19: Array indexing - Off-by-one v loop conditions

**Všechny for-loop podmínky:**
```c
// ❌ Chybné:
for (local_2 = 0; (local_2 <= gRecs); local_2++)  // Iteruje 0..gRecs (gRecs+1 iterací!)
for (local_2 = 0; (local_2 <= 2); local_2++)      // Iteruje 0,1,2 (3 iterace místo 2)
for (local_2 = 0; (local_2 <= 64); local_2++)     // Iteruje 0..64 (65 iterací!)

// ✅ Správné (originál):
for (i = 0; i < gRecs; i++)
for (i = 0; i < 2; i++)
for (i = 0; i < REC_MAX; i++)  // REC_MAX=64
```

**Příčina:** Loop reconstruction generuje `<=` místo `<` jako condition.

**Dopad:** Kritický - buffer overflow při běhu!

---

### 🟡 SÉMANTICKÝ PROBLÉM #20: Compound assignment (+=, -=)

**Originál (tdm.c:49, 106):**
```c
gTime += time;                        // Compound +=
gRecTimer[i] -= info->elapsed_time;   // Compound -=
```

**Dekompilováno (tdm_CURRENT_OUTPUT.c:22, 70):**
```c
gTime = (gTime + time);               // ✅ Expandováno správně
gRecTimer[local_2] = (gRecTimer[local_2] - info->field_16);  // ✅ OK
```

**Hodnocení:** Correct expansion, ale verbose. Lepší by bylo zachovat `+=` syntax.

---

### 🟡 SÉMANTICKÝ PROBLÉM #21: Increment/Decrement operátory (++, --)

**Originál (tdm.c:269, 272):**
```c
gSideFrags[sideB]--;  // Post-decrement
gSideFrags[sideB]++;  // Post-increment
```

**Dekompilováno (tdm_CURRENT_OUTPUT.c:178, 181):**
```c
gSideFrags[local_2]--;  // ✅ Zachováno!
gSideFrags[local_2]++;  // ✅ Zachováno!
```

**Hodnocení:** Úspěch! DEC/INC instrukce správně mapovány na --/++.

---

### 🟡 SÉMANTICKÝ PROBLÉM #22: Hexadecimální konstanty

**Originál (tdm.c:137, 158, 175-177, 266):**
```c
icon[i].color = 0xffffffff;
SC_MP_SRV_SetForceSide(0xffffffff);
hudinfo.side_color[0] = 0x440000ff;
hudinfo.side_color[1] = 0x44ff0000;
sideB = 0xffffffff;
```

**Dekompilováno:**
```c
local_8[local_2].field3 = -1;        // ❌ Signed interpretation!
SC_MP_SRV_SetForceSide(-1);          // ❌ -1 místo 0xffffffff
local_3.field6 = 512.0155639648438f; // ❌❌❌ FLOAT MÍSTO HEX!!!
local_3.field7 = 2040.0f;            // ❌❌❌ FLOAT MÍSTO HEX!!!
local_2 = -1;                        // ❌ -1 místo 0xffffffff
```

**Chyby:**
1. `0xffffffff` (unsigned) → `-1` (signed)
2. `0x440000ff` → `512.0155639648438f` - **KATASTROFA!** Int→float reinterpretace bitů!
3. `0x44ff0000` → `2040.0f` - **KATASTROFA!**

**Příčina:**
- Chyba #1: Znaménkový vs neznaménkový typ
- Chyba #2-3: ASGN cíl byl detekován jako float field, tak byl zdrojový int reinterpretován jako float!

---

### 🔴 KRITICKÝ PROBLÉM #23: Variable name collision (tdm_CURRENT_OUTPUT.c:177)

**Originál (tdm.c:260, 264):**
```c
dword sideA, sideB;
SC_P_GetInfo(info->param1, &plinfo);
sideA = plinfo.side;

if (info->param2){
    SC_P_GetInfo(info->param2, &plinfo);
    sideB = plinfo.side;
}
else sideB = 0xffffffff;

if (sideA == sideB){  // Porovnání dvou různých proměnných!
    gSideFrags[sideB]--;
}
```

**Dekompilováno (tdm_CURRENT_OUTPUT.c:169-177):**
```c
SC_P_GetInfo(info->field_4, &player_info);
local_2 = player_info.field2;  // ❌ sideA → local_2

if ((info->field_8)) {
    SC_P_GetInfo(info->field_8, &player_info);
    local_2 = player_info.field2;  // ❌❌❌ sideB → TAKÉ local_2!!!
} else {
    local_2 = -1;
}
if (((local_2 == local_2))) {  // ❌❌❌ Porovnává sama sebe!!!
```

**Chyba:** Proměnné `sideA` a `sideB` byly obě namapovány na `local_2` → **variable name collision!**

**Dopad:** Kritický - podmínka je vždy TRUE, logika zničena!

---

### 🟡 SÉMANTICKÝ PROBLÉM #24: Chybějící komentáře breaks (všude)

**Originál (tdm.c:123, 142, 154, atd.):**
```c
break;// SC_NET_MES_SERVER_TICK
break;// SC_NET_MES_CLIENT_TICK
break;// SC_NET_MES_LEVELPREINIT
```

**Dekompilováno:**
```c
break;  // Žádné komentáře
```

**Hodnocení:** Kosmetické - komentáře pomáhají čitelnosti.

---

### 🟡 SÉMANTICKÝ PROBLÉM #25: Missing #defines and constants

**Originál:**
```c
#define RECOVER_TIME  5.0f
#define NORECOV_TIME  3.0f
#define REC_WPNAME    "DM%d"
#define REC_MAX       64
```

**Dekompilováno:**
```c
// Hodnoty inlinované:
3.0f         // NORECOV_TIME
5.0f         // RECOVER_TIME (nikde nepoužito v dekompilovaném kódu)
"DM%d"       // REC_WPNAME
64           // REC_MAX
```

**Příčina:** Preprocesor expandoval všechny makra před kompilací.

**Řešení:** Heuristic detection - pokud konstanta použita vícekrát → navrhni #define.

---

### 🟢 KOSMETICKÝ PROBLÉM #26: Debug messages ve výstupu

**Dekompilace obsahuje řádky jako:**
```c
// Loop header - Block 26 @145
// Loop header - Block 36 @270
```

**Dopad:** Kosmetické - měly být filtrovány.

---

### 🟡 SÉMANTICKÝ PROBLÉM #27: Incomplete case SC_NET_MES_SERVER_RECOVER_TIME (tdm_CURRENT_OUTPUT.c:157-161)

**Originál (tdm.c:234-243):**
```c
case SC_NET_MES_SERVER_RECOVER_TIME:
    if (info->param2){
        info->fval1 = 0.1f;
    }
    else{
        // killed
        info->fval1 = RECOVER_TIME;  // 5.0f
    }
    break;
```

**Dekompilováno:**
```c
case 5:
    if ((info->field_8)) {
        // ❌ CHYBÍ: info->fval1 = 0.1f
    } else {
        // ❌ CHYBÍ: info->fval1 = 5.0f
    }
    break;
```

**Chyba:** Obě větve if/else jsou prázdné!

**Příčina:** Assignments do `info->fval1` nebyly zachyceny (možná dead code elimination?).

---

## KATEGORIE E: OSTATNÍ PROBLÉMY

### 🟡 SÉMANTICKÝ PROBLÉM #28: Lokální proměnné - Špatné názvy

**Originál používá sémantické názvy:**
```c
char txt[32];
dword i, j, sideA, sideB;
s_SC_MP_Recover *precov;
s_SC_MP_hud hudinfo;
s_SC_P_getinfo plinfo;
s_SC_HUD_MP_icon icon[2];
s_SC_MP_EnumPlayers enum_pl[64];
s_SC_MP_SRV_settings SRVset;
```

**Dekompilováno používá generické:**
```c
int i;             // ✅ Zachováno z optimalizace?
int local_0;       // ❌ txt[32]
int local_2;       // ❌ Používáno pro i, j, sideA, sideB (!!!!)
int local_3;       // ❌ hudinfo nebo precov
int local_8;       // ❌ icon[2]
int local_10, local_74, local_76;  // ❌ Další proměnné
s_SC_P_getinfo player_info;  // ✅ Typ správný, ale mělo být plinfo
```

**Chyba:** Proměnná `local_2` je **reused** pro 4 různé sémantické hodnoty!

---

### 🔴 KRITICKÝ PROBLÉM #29: Missing default return (tdm_CURRENT_OUTPUT.c:200)

**Originál (tdm.c:304):**
```c
return 1;
}// int ScriptMain(void)
```

**Dekompilováno:**
```c
    default:
        return TRUE;  // ❌ Return je v DEFAULT case místo na konci funkce!
    }
}
```

**Chyba:** Default case má return, ale po switch statement chybí fallback return.

**Dopad:** Některé code paths nemají return → undefined behavior.

---

### 🟡 SÉMANTICKÝ PROBLÉM #30: Prázdné case bloky

**Case 2 (SC_NET_MES_RENDERHUD) - Originál (tdm.c:228-231):**
```c
case SC_NET_MES_RENDERHUD:
    break;
```

**Dekompilováno (tdm_CURRENT_OUTPUT.c:155-156):**
```c
case 2:
    break;  // ✅ OK
```

**Hodnocení:** Správně zachováno!

---

## SOUHRN PROBLÉMŮ

### 🔴 KRITICKÉ PROBLÉMY (15x) - Brání kompilaci/běhu

| # | Problém | Lokace | Příčina |
|---|---------|--------|---------|
| 1 | Chybějící globální deklarace | Celý soubor | Data segment není dekompilován |
| 2 | `switch(local_0)` místo `switch(gEndRule)` | func_0010:19 | Špatná detekce switch value |
| 3 | Rozbitá OR podmínka v case 1 | func_0010:31-43 | Short-circuit eval reconstruction |
| 4a | For-loop: `<=` místo `<` | ScriptMain:69,90,152 | Loop condition detection |
| 4b | For-loop: Rozbitý sprintf loop | ScriptMain:134-140 | Control flow reconstruction |
| 5 | Case values číselné místo konstant | ScriptMain:66+ | Preprocesované konstanty |
| 8 | `local_8[i] = value` přepisuje strukturu | ScriptMain:92 | Member vs struct assignment |
| 12 | Rozbitá OR podmínka | func_0010:31-43 | Duplicitní s #3 |
| 14 | `&player_info.group` místo `enum_pl[64]` | ScriptMain:73 | Array reconstruction |
| 15 | `&local_0` buffer místo `txt[32]` | ScriptMain:135 | Array reconstruction |
| 16 | `&player_info.max_hp` místo `icon[2]` | ScriptMain:96 | Array reconstruction |
| 22 | Hex→Float reinterpretace | ScriptMain:118-120 | Type inference failure |
| 23 | Variable collision: `local_2==local_2` | ScriptMain:177 | Variable name reuse |
| 27 | Chybějící assignments do `info->fval1` | ScriptMain:157-161 | Dead code elimination? |
| 29 | Missing default return | ScriptMain:200 | Return statement placement |

---

### 🟡 SÉMANTICKÉ CHYBY (13x) - Kompiluje se, ale sémanticky špatně

| # | Problém | Lokace | Dopad |
|---|---------|--------|-------|
| 7 | `info->field_XX` místo jmen | Všude | Čitelnost |
| 9 | CLEAR→SC_ZeroMem | Více míst | ✅ Správně expandováno |
| 10 | Zbytečné ITOF casts | func_0010:25, ScriptMain:129 | Verbose |
| 11 | Zbytečné závorky `(())` | Všude | Čitelnost |
| 17 | Chybějící pointer cast | ScriptMain:163 | Type safety |
| 18 | Chybějící pointer dereference | ScriptMain:166 | Sémantika |
| 19 | Array indexing off-by-one | Duplicitní s #4a | Duplicitní |
| 20 | `gTime = gTime + time` místo `+=` | Více míst | Verbose |
| 21 | `++`/`--` zachováno | ✅ OK | N/A |
| 24 | Chybějící break komentáře | Všude | Čitelnost |
| 25 | Missing #defines | Všude | Maintainability |
| 28 | Generic local names | Všude | Čitelnost |
| 30 | Prázdné case bloky | ✅ OK | N/A |

---

### 🟢 KOSMETICKÉ ROZDÍLY (2x) - Funkční kód

| # | Problém | Lokace |
|---|---------|--------|
| 6 | Funkce `_init` navíc | Řádek 8-14 (správně generováno kompilátorem) |
| 26 | Debug komentáře "Loop header" | Řádky 68, 89, 151 |

---

## STATISTIKY ÚSPĚŠNOSTI

### Funkce:
- ✅ `_init` - 100% (compiler-generated)
- ❌ `SRV_CheckEndRule` → `func_0010` - 30% (rozbitá logika)
- ✅ `UpdateSideFrags` → `func_0096` - 90% (jen kosmetické)
- ⚠️ `ScriptMain` - 60% (velké strukturální problémy)

### Instrukce:
- ✅ XFN volání: 90% úspěšnost (skvělé!)
- ✅ Aritmetika: 95%
- ❌ For-loops: 20% (všechny rozbité)
- ❌ Switch/case: 60% (hodnoty OK, logika částečně rozbitá)
- ❌ Struktury: 40% (field offsety OK, assignments chybné)
- ❌ Pole: 30% (vážné problémy)

---

## PRIORITNÍ OPRAVY PRO DEKOMPILÁTOR

### P0 - KRITICKÉ (implementovat IHNED):

1. **Data Segment → Global Variables**
   - Parsing data section
   - Type inference z usage patterns
   - Generování deklarací na začátku souboru

2. **Array Reconstruction**
   - Detekce `char txt[32]` z buffer usage
   - Detekce `Type arr[N]` z repeated indexing patterns
   - Fixnout member assignment detection

3. **Variable Name Collision Fix**
   - SSA form → variable splitting
   - Detekce kdy jedna `local_X` představuje více sémantických proměnných
   - Rename na `local_X_version`

4. **For-Loop Condition Fix**
   - `<=` → `<` conversion
   - Detekce inclusive vs exclusive bounds

5. **OR/AND Boolean Expression Reconstruction**
   - Short-circuit evaluation patterns
   - Vnořené if→else → flat OR/AND

---

### P1 - VYSOKÁ PRIORITA (implementovat brzy):

6. **Type Inference pro Structures**
   - External struct definitions z hlaviček
   - Field name mapping (offset→name)
   - Member vs whole struct assignment

7. **Hex Constants**
   - Detekce kdy zobrazit 0xXXXXXXXX místo -1
   - **FIX: Int→Float reinterpretace!**
   - Unsigned vs signed type awareness

8. **Switch Case Constant Mapping**
   - Database symbolických konstant z headers
   - Pattern matching pro known enums

9. **Dead Code Elimination Fix**
   - Zjistit proč `info->fval1 = ...` assignments zmizely
   - Preserve všechny side-effects

---

### P2 - STŘEDNÍ PRIORITA (nice to have):

10. **Compound Assignment Operators**
    - `x = x + y` → `x += y`
    - `x = x - y` → `x -= y`

11. **Implicit Type Casts**
    - `ITOF(dword)` → `(float)dword` nebo nic (pokud implicitní)
    - Better cast rendering

12. **Macro Detection**
    - Heuristics pro #define reconstruction
    - Pattern matching (repeated constants → macro)

13. **Variable Naming**
    - Loop counters → `i`, `j`, `k`
    - Type-based hints: `s_SC_P_getinfo x` → `player_info`

14. **Bracket Reduction**
    - `((x > 0))` → `x > 0`
    - Precedence-aware rendering

---

## ZÁVĚR

Dekompilátor má **solidní základ**, ale trpí:
- 🔴 **Kritickými problémy** s arrays, loops, boolean expressions
- 🟡 **Sémantickými chybami** v type inference a variable naming
- 🟢 **Úspěchy** v XFN call arguments a základní kontrolní struktuře

**Estimated effort to fix:**
- P0 issues: ~40-60 hodin práce
- P1 issues: ~30 hodin
- P2 issues: ~20 hodin

**Celkem:** ~90-110 hodin pro produkční kvalitu dekompilace.
