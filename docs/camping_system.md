# Bot Camping System

Systém pro kempení botů na předem definovaných pozicích v mapě.

## Jak to funguje

Bot se může kdykoliv rozhodnout, že půjde kempit na některý z definovaných camp spotů (pokud zrovna nenese vlajku a nemá nepřítele). Systém má následující vlastnosti:

### Pravděpodobnost a timing
- Bot zkontroluje camp spoty **jednou za 20 sekund** (`CAMP_SCAN_INTERVAL`)
- Při kontrole má **15% šanci** že se rozhodne kempit (`CAMP_CHANCE_PERCENT`)
- Kontrola probíhá **z jakéhokoliv stavu** (kromě nesení vlajky a boje)

### Délka kempení
- Bot kempí **10-40 sekund** náhodně (konfigurovatelné přes `CAMP_MIN_DURATION` a `CAMP_MAX_DURATION`)
- Po skončení kempení má bot **30 sekundový cooldown** než může kempit znovu

### Přerušení kempení
- Pokud bot zaznamená nepřítele, **okamžitě vstane a začne bojovat**
- Cooldown po přerušení je kratší (15 sekund)

### Obsazenost
- Bot **nejde na camp spot kde už je spoluhráč** (radius 3m)
- Kontroluje se pouze vlastní tým

## Vytváření camp spotů v mapě

### Pojmenování waypointů

Každý camp spot se skládá ze **dvou waypointů**:

1. **Pozice campu** - kde bot bude stát/klečet
2. **Look target** - kam se bot bude dívat

#### Naming konvence:

```
camp_<side>_<číslo>       - pozice campu
camp_<side>_<číslo>_look  - kam se dívat
```

#### Typy camp spotů podle strany:

| Prefix | Popis | Kdo může použít |
|--------|-------|-----------------|
| `camp_vc_` | Pouze pro VC stranu | VC boti |
| `camp_us_` | Pouze pro US stranu | US boti |
| `camp_uni_` | Univerzální | Obě strany |

#### Příklady:

```
camp_vc_00        <- VC camp spot #0
camp_vc_00_look   <- kam se VC bot dívá

camp_us_01        <- US camp spot #1
camp_us_01_look   <- kam se US bot dívá

camp_uni_00       <- Univerzální camp spot #0
camp_uni_00_look  <- kam se bot dívá
```

### Maximální počet camp spotů

- **32 camp spotů na prefix** (00-31)
- Celkem tedy až 96 camp spotů na mapě (32 VC + 32 US + 32 univerzálních)

## Umístění waypointů v editoru

### Camp pozice (camp_XX_##)

1. Umísti waypoint na místo kde má bot kempit
2. Doporučené pozice:
   - Za krytem (zeď, bedna, strom)
   - Na vyvýšeném místě s dobrým výhledem
   - U vstupu do budovy
   - V rohu místnosti

### Look target (camp_XX_##_look)

1. Umísti waypoint tam **kam se má bot dívat**
2. Typicky:
   - Směrem ke vstupu/průchodu
   - Na hlavní cestu
   - Na strategický bod (vlajka, spawn)

### Vzdálenost look targetu

- Look target může být **libovolně daleko**
- Bot se otočí směrem k němu
- Doporučeno: 10-50 metrů pro přirozený pohled

## Konfigurace v kódu

Parametry jsou definované v `USBOT0_reconstructed.c`:

```c
#define MAX_CAMP_SPOTS 32           // Max camp spotů na prefix
#define CAMP_SEARCH_RADIUS 50.0f    // Jak daleko bot hledá camp spoty (m)
#define CAMP_CHECK_RADIUS 3.0f      // Radius pro kontrolu obsazenosti (m)
#define CAMP_MIN_DURATION 10.0f     // Min doba kempení (s)
#define CAMP_MAX_DURATION 40.0f     // Max doba kempení (s)
#define CAMP_COOLDOWN_TIME 30.0f    // Cooldown po kempení (s)
#define CAMP_SCAN_INTERVAL 20.0f    // Jak často kontrolovat camp spoty (s)
#define CAMP_CHANCE_PERCENT 15      // Šance na kempení při kontrole (%)
```

## Chování bota při kempení

1. **Hledání**: Bot v patrol módu zkusí najít camp spot v radiusu 50m
2. **Cesta**: Bot jde CHŮZÍ (ne běh) na camp pozici
3. **Příchod**: Když dorazí (do 2m), dřepne si
4. **Kempení**: Dívá se směrem k look targetu, zůstává v dřepu
5. **Konec**: Po uplynutí času vstane a pokračuje v normální AI
6. **Přerušení**: Při spatření nepřítele okamžitě vstane a bojuje

## Tipy pro level design

### Dobrá umístění camp spotů:

- **U vlajek** - pro defenzivní kempení
- **Na křižovatkách** - sledování více cest
- **Ve výškách** - snipeři
- **U vstupů** - past na nepřátele

### Špatná umístění:

- Na otevřeném prostranství bez krytu
- Příliš blízko spawn pointů
- V místech kde bot blokuje průchod spoluhráčům

### Balancování:

- Příliš málo camp spotů = boti nebudou moc kempit
- Příliš mnoho = boti budou trčet všude
- Doporučeno: **3-8 camp spotů na stranu** podle velikosti mapy

## Příklad rozmístění pro CTF mapu

```
                    [flag_vc]
                        |
    camp_vc_00 -------- X -------- camp_vc_01
         |                              |
         |                              |
    camp_uni_00 ================ camp_uni_01
         |                              |
         |                              |
    camp_us_00 -------- X -------- camp_us_01
                        |
                    [flag_us]
```

Každý camp spot má svůj `_look` waypoint směřující k centru/vlajce.

## Troubleshooting

### Bot nekempí vůbec
- Zkontroluj naming konvenci (malá písmena, podtržítka)
- Zkontroluj že existuje i `_look` waypoint
- Zvyš `CAMP_CHANCE_PERCENT`

### Bot kempí moc často
- Sniž `CAMP_CHANCE_PERCENT`
- Zvyš `CAMP_COOLDOWN_TIME`
- Odeber některé camp spoty

### Bot se dívá špatným směrem
- Zkontroluj pozici `_look` waypointu
- Look waypoint musí být ve směru kam se má bot dívat

### Více botů na jednom spotu
- Zvětši vzdálenost mezi camp spoty (min 6m)
- Systém kontroluje obsazenost, ale ne při současném příchodu
