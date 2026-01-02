# Bot Buddy System

System pro kooperaci botů ve dvojicích (leader + buddy).

## Jak to funguje

Boti jsou automaticky párováni do dvojic. Jeden bot je **leader** (vede), druhý je **buddy** (následuje).

### Automatické párování

- Hlavní skript mise (`CTF4X4.c`) automaticky páruje boty **každých 5 sekund**
- Boti jsou párováni **pouze se spoluhráči** (stejná strana)
- Párování probíhá v pořadí jak jsou boti v enumeraci
- Maximálně **4 páry** současně (8 botů)

### Role

| Role | Popis | Chování |
|------|-------|---------|
| `BUDDY_ROLE_SOLO` | Sólo hráč | Normální AI - jde na vlajky sám |
| `BUDDY_ROLE_LEADER` | Vedoucí páru | Jde na vlajky, buddy ho následuje |
| `BUDDY_ROLE_BUDDY` | Následovník | Následuje leadera, pomáhá mu |

### Chování Leadera

- Leader se chová **normálně** - jde na nepřátelskou vlajku, nese ji domů
- Pokud leader **začne kempit**, pošle zprávu buddymu
- Buddy pak pokračuje sám na vlajku

### Chování Buddyho

- Buddy **následuje leadera** pokud je vzdálenost > 8m
- Pokud je vzdálenost > 25m, buddy **běží** za leaderem
- Pokud leader kempí, buddy pokračuje **sám na vlajku**
- Když leader zemře, buddy se stává **sólo** hráčem

## Párování s lidským hráčem

Pokud je v týmu **lichý počet botů** a **lidský hráč nese vlajku**:
- Jeden bot se automaticky přiřadí jako buddy k lidskému hráči
- Bot následuje hráče a pomáhá mu dostat vlajku domů

## Přerušení párování

Párování se automaticky ruší když:
- Leader nebo buddy **zemře**
- Leader nebo buddy **opustí hru**
- Hlavní skript pošle zprávu `BOT_MSG_UNPAIR`

Po zrušení párování jsou boti znovu k dispozici pro nové párování.

## Konfigurace

### V bot skriptu (`USBOT0_reconstructed.c`)

```c
float buddy_follow_distance = 8.0f;     // Vzdálenost pro následování (m)
float buddy_regroup_distance = 25.0f;   // Kdy se vrátit k partnerovi (m)
```

### V hlavním skriptu (`CTF4X4.c`)

```c
#define MAX_BUDDY_PAIRS         4       // Max párů současně
#define BUDDY_UPDATE_INTERVAL   5.0f    // Jak často párovat (s)
```

## Zprávy mezi skripty

| Zpráva | ID | Směr | Popis |
|--------|-----|------|-------|
| `BOT_MSG_BECOME_LEADER` | 200 | Mise → Bot | Jsi nový leader |
| `BOT_MSG_BECOME_BUDDY` | 201 | Mise → Bot | Jsi nový buddy |
| `BOT_MSG_LEADER_CAMPING` | 202 | Leader → Buddy | Leader začal kempit |
| `BOT_MSG_LEADER_DIED` | 203 | Mise → Buddy | Tvůj leader zemřel |
| `BOT_MSG_BUDDY_DIED` | 204 | Mise → Leader | Tvůj buddy zemřel |
| `BOT_MSG_UNPAIR` | 205 | Mise → Bot | Párování zrušeno |
| `BOT_MSG_FOLLOW_HUMAN` | 206 | Mise → Bot | Následuj lidského hráče |

## Priorita chování

Bot zpracovává akce v tomto pořadí (první má nejvyšší prioritu):

1. **Nesení vlajky** - Vlajkonoš běží přímo domů
2. **Buddy following** - Buddy následuje leadera
3. **Camping** - Bot jde na camp spot
4. **Normální AI** - Patrol, útok, obrana

## Interakce s camping systémem

- **Leader může kempit** - ale oznámí to buddymu
- **Buddy pokračuje sám** když leader kempí
- Buddy se **nepřipojí** k leaderovi na camp spotu
- Po skončení kempení se leader a buddy **automaticky nesejdou**
  - Buddy je nyní sólo a může být znovu spárován

## Příklady scénářů

### Scénář 1: Normální průběh
1. Bot A a Bot B jsou spárováni (A = leader, B = buddy)
2. Leader A jde na nepřátelskou vlajku
3. Buddy B následuje leadera A
4. Leader A sebere vlajku a běží domů
5. Buddy B běží s ním a kryje ho
6. Leader A donese vlajku - skóre!

### Scénář 2: Leader kempí
1. Bot A a Bot B jsou spárováni
2. Leader A se rozhodne kempit
3. Leader A pošle zprávu buddymu B
4. Buddy B pokračuje sám na vlajku
5. (Buddy B může být spárován s jiným sólo botem)

### Scénář 3: Leader zemře
1. Bot A a Bot B jsou spárováni
2. Leader A je zabit nepřítelem
3. Hlavní skript pošle zprávu buddymu B
4. Buddy B se stává sólo hráčem
5. Při dalším update může být spárován znovu

### Scénář 4: Lidský hráč s vlajkou
1. V US týmu jsou 3 boti a 1 člověk
2. Člověk sebere VC vlajku
3. Boti A a B jsou spárováni spolu
4. Bot C je sólo - hlavní skript ho přiřadí jako buddy k člověku
5. Bot C následuje člověka s vlajkou

## Troubleshooting

### Boti se nepárují
- Zkontroluj že `gMission_started == TRUE`
- Zkontroluj že jsou aspoň 2 živí boti na stejné straně
- Zkontroluj `gBuddyPairCount` - max 4 páry

### Buddy nenásleduje leadera
- Zkontroluj `buddy_role` a `buddy_partner_id` v botu
- Zkontroluj že leader existuje (`SC_P_IsReady`)
- Zkontroluj že `buddy_leader_camping == 0`

### Párování se neruší po smrti
- Zkontroluj že `SC_NET_MES_SERVER_KILL` handler volá `NotifyBuddyOfDeath()`

## Technické detaily

### Datové struktury v CTF4X4.c

```c
// Pole párů: [index páru][0=leader, 1=buddy]
dword gBuddyPairs[MAX_BUDDY_PAIRS][2];
int gBuddyPairCount = 0;
float gBuddyUpdateTimer = 0.0f;
```

### Datové struktury v USBOT0_reconstructed.c

```c
int buddy_role = BUDDY_ROLE_SOLO;    // Aktuální role
dword buddy_partner_id = 0;          // ID partnera
int buddy_leader_camping = 0;        // Leader kempí?
```

### Komunikace

- **Mise → Bot**: `SC_P_ScriptMessage(bot_id, message, param)`
- **Bot → Bot**: `SC_P_ScriptMessage(partner_id, message, param)`
- **Bot → Mise**: `SC_MP_ScriptMessage(message, bot_id)`
