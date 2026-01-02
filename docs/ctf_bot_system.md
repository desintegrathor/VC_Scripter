# CTF 6v6 Bot System

AI bot system for 6v6 Capture The Flag multiplayer mode.

## Scripts Overview

| Script | Count | Purpose |
|--------|-------|---------|
| CTF6X6.c | 1 | Main level script - game logic |
| USBOT0-5.c | 6 | AI bots for US side |
| VCBOT0-5.c | 6 | AI bots for VC side |

---

## Map Setup Guide

### Step 1: Prepare Player Entities
1. Open your map in the editor
2. **Remove all existing player entities** (from coop or other modes)
3. Add **6 player entities for each side** (12 total)

### Step 2: Assign Scripts
- US side: assign `USBOT0.scr` through `USBOT5.scr`
- VC side: assign `VCBOT0.scr` through `VCBOT5.scr`

### Step 3: Waypoint Network
Bots need waypoints to navigate. To import from another version of the map:

1. Open source map (Quick Fight or Singleplayer version)
2. Select all waypoints
3. **Save Selected** → creates .sce file
4. Open your multiplayer .sco map
5. **Merge** → select the .sce file

**IMPORTANT:** When asked about assigning objects to sectors, choose **NO**!
Waypoints must remain in "World sector" or they won't work.

### Step 4: Required Nodes
Your map needs these named nodes:
- `flag_us` - US flag position
- `flag_vc` - VC flag position

### Step 5: Optional Camp Spots
Add camping waypoints for more tactical bot behavior:
- `camp_us_XX` + `camp_us_XX_look` - US camping spots
- `camp_vc_XX` + `camp_vc_XX_look` - VC camping spots
- `camp_uni_XX` + `camp_uni_XX_look` - Universal spots (both sides)

Where XX = 00-31 (max 32 spots per side)

Example: camp_uni_01       bots from both sides consider camping there
         camp_uni_01_look  the camping bot looks in this direction while camped

---

## How the System Works

### Game Flow
1. Round starts when both teams have at least 1 player
2. 8-second grace period for players to load
3. Bots pursue enemy flag, defend own flag
4. First team to **3 points** wins the round

### Flag States
| State | Value | Description |
|-------|-------|-------------|
| INBASE | 0 | Flag at home base |
| ONPLAYER | 1 | Flag being carried by enemy |
| ONGROUND | 2 | Flag dropped (30s until return) |

### Bot Respawn
Dead bots respawn in waves to maintain team balance.

**How it works:**
- Respawn wave every **~30 seconds** (configurable via `GetRecovTime()`)
- Message "Reinforcements spawning!" appears when wave triggers
- Only respawns bots if team is below maximum (6 bots per side)
- Formula: `bots_to_spawn = 6 - human_players - alive_bots`
- Human players (alive or dead) always reserve their slot - bots don't replace them

**Respawn points:**
- `USSpawn0` - `USSpawn15` for US side
- `VCSpawn0` - `VCSpawn15` for VC side
- Alternative naming: `rec_us_XX` and `rec_vc_XX` (XX = 00-15)
- Or editor-placed CTF respawn entities
- System picks spawn point furthest from enemies

### Buddy System
Bots automatically pair up into leader-buddy teams for coordinated attacks.

**Roles:**
| Role | Behavior |
|------|----------|
| Solo | Normal AI - pursues flags independently |
| Leader | Goes for enemy flag, buddy follows him |
| Buddy | Follows leader, provides cover fire |

**How it works:**
- Main script pairs bots every **5 seconds** (max 4 pairs = 8 bots)
- Buddy follows leader at **8-12m distance**
- If distance > **25m**, buddy runs to catch up
- If leader **camps**, buddy continues alone to enemy flag
- If leader **dies**, buddy becomes solo (available for new pairing)
- If human player carries flag, a solo bot may follow them as buddy

**Priority:** Flag carrying > Buddy following > Camping > Normal AI

### Camping Behavior
- 15% chance every 20 seconds to camp
- Camps for 10-40 seconds
- 30-second cooldown after camping
- Aborts if enemy spotted

---

## Customization Tips

### Change Team Size
In `CTF6X6.c`, modify the respawn function to change max bots per side.
Default: 6 bots per team.

### Adjust Difficulty
Bot AI properties are set in `InitBot()`. Key values:
```c
SC_AI_SetInaccuracyMin(ai_prop, 0.3);  // Lower = more accurate
SC_AI_SetInaccuracyMax(ai_prop, 0.5);
SC_AI_SetReactionTime(ai_prop, 0.2);   // Lower = faster reaction
```

Difficulty levels:
| Level | Inaccuracy | Reaction Time |
|-------|------------|---------------|
| Easy | 1.0 | 1.2s |
| Medium | 0.6 | 0.6s |
| Hard | 0.3 | 0.2s |
| Vietnam | 0.1 | 0.0s |



### Adjust Camping Probability
In bot scripts, modify:
```c
#define CAMP_CHANCE_PERCENT 15    // % chance to camp
#define CAMP_SCAN_INTERVAL 20.0   // Check every N seconds
#define CAMP_MIN_DURATION 10.0    // Minimum camp time
#define CAMP_MAX_DURATION 40.0    // Maximum camp time
```


## Troubleshooting

**Bots don't move:**
- Check waypoint network exists
- Ensure waypoints are in "World sector"

**Bots ignore flags:**
- Verify `flag_us` and `flag_vc` nodes exist
- Check node names are exact (case sensitive)

**Bots don't respawn:**
- Main script must be running (CTF6X6.scr assigned to level)
- Check if RecoverAllDeadAi() is being called

**Bots don't camp:**
- Add camp waypoints with correct naming
- Camping is probabilistic (15% chance)
