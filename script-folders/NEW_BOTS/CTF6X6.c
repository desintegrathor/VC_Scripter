/*
	Eric multiplayer script - CTF 4x4 (with bot support)

	Reconstructed from CTF4X4.scr decompilation
	Based on original CTF.c structure
*/

#include <inc\sc_global.h>
#include <inc\sc_def.h>


#define NORECOV_TIME			3.0f		// disable time of recoverplace after recovering someone there

#define ONGROUND_MAXTIME		30.0f

#define MIN_PLAYERS_PER_TEAM	6			// Minimum players per team (bots fill the gaps)

#define REC_WPNAME_US	"USSpawn%d"
#define REC_WPNAME_VC	"VCSpawn%d"
#define REC_MAX			64



#define GVAR_SIDE0POINTS				500
#define GVAR_SIDE1POINTS				501

#define GVAR_FLAGSTATUS					510
#define GVAR_ONPLAYER					512
#define GVAR_INFO						514
#define GVAR_GAMERUNS					516
#define GVAR_SCOREPL					517
#define GVAR_LAST						519

// Bot count global vars (4x4 specific)
#define GVAR_BOTCOUNT_US				540
#define GVAR_BOTCOUNT_VC				541

// Killstreak sync (4x4 specific)
#define GVAR_KILLSTREAK_PLAYER			542

// Bot message IDs (4x4 specific)
#define BOT_MSG_REINIT					2000	// Bot re-initialization
#define BOT_MSG_FLAG_PICKUP				100		// Bot picked up flag

// ============================================================================
// BUDDY SYSTEM - Constants
// ============================================================================
#define MAX_BUDDY_PAIRS					4		// Max buddy pairs (8 bots = 4 pairs)
#define BUDDY_UPDATE_INTERVAL			5.0f	// How often to check for unpaired bots

// Buddy system messages (sent to bots via SC_P_ScriptMessage)
#define BOT_MSG_BECOME_LEADER			200		// You are now leader (param = buddy_id)
#define BOT_MSG_BECOME_BUDDY			201		// You are now buddy (param = leader_id)
#define BOT_MSG_LEADER_CAMPING			202		// Leader started camping - continue alone
#define BOT_MSG_LEADER_DIED				203		// Your leader died
#define BOT_MSG_BUDDY_DIED				204		// Your buddy died
#define BOT_MSG_UNPAIR					205		// Pairing cancelled
#define BOT_MSG_FOLLOW_HUMAN			206		// Follow this human player (param = human_id)


#define FLAG_PH_INBASE					0
#define FLAG_PH_ONPLAYER				1
#define FLAG_PH_ONGROUND				2


#define PRELOADBES_FLAG_US			1
#define PRELOADBES_FLAG_VC			2

#define INFO_FL_STOLEN				1
#define INFO_FL_DROPPED				2
#define INFO_FL_RETURNED			3
#define INFO_SCORE					4

// Killstreak info values (10+, flag events 1-4 have priority)
#define INFO_STREAK_ONROLL			10
#define INFO_STREAK_RAMPAGE			11
#define INFO_STREAK_UNSTOPPABLE		12
#define INFO_STREAK_GODLIKE			13

// Killstreak thresholds
#define STREAK_ONROLL				3
#define STREAK_RAMPAGE				5
#define STREAK_UNSTOPPABLE			7
#define STREAK_GODLIKE				10


BOOL gMission_started = FALSE;
float gMission_afterstart_time = 0.0f;

float gMission_starting_timer = 0.0f;
dword gRecs[2] = {0,0};
s_SC_MP_Recover gRec[2][REC_MAX];
float gRecTimer[2][REC_MAX];

float gNextRecover = 0.0f;

int gSidePoints[2] = {0,0};

int gCLN_SidePoints[2];

float gCLN_HelpInfo_timer = 0.0f;
ushort gCLN_HelpInfo[256];

dword gEndRule;
dword gEndValue;
float gTime;

dword abl_lists = 0;
dword abl_list[64];

#if _GE_VERSION_ >= 138
dword g_FPV_UsFlag = 0;
dword g_FPV_VcFlag = 0;
#endif


void *gFlagNod[2];
c_Vector3 gOrigFlagPos[2];
dword gFlagPhase[2] = {FLAG_PH_INBASE,FLAG_PH_INBASE};		// FLAG_PH_
dword gFlagOnPlayer_handle[2] = {0,0};	// handle of player
dword gInfo[2] = {0,0};		// INFO_xxxxx
dword gKillstreaks[64];			// Killstreak count per player slot

// ============================================================================
// BUDDY SYSTEM - Global variables
// ============================================================================
// Buddy pairs: [pair_index][0] = leader handle, [pair_index][1] = buddy handle
dword gBuddyPairs[MAX_BUDDY_PAIRS][2];
int gBuddyPairCount = 0;
float gBuddyUpdateTimer = 0.0f;

dword gOnGroundNetID[2] = {0,0};
float gOnGroundTimer[2] = {0,0};

dword gInfoLastScorePlayer[2] = {0,0};
dword gSend_InfoLastScorePlayer[2] = {0,0};

dword gSend_FlagPhase[2];
dword gSend_FlagOnPlayer[2];
dword gSend_Info[2];


dword gCLN_FlagPhase[2];
dword gCLN_FlagOnPlayer[2];
dword gCLN_Info[2];

dword gCLN_eqp_pl_handle[2] = {0,0};

float gCLN_MyFlagTimer = 0.0f;


char *gEQP_name[2] = {
			{"G\\WEAPONS\\Vvh_flag\\eqp\\Vvh_flag_US_3pv.eqp"},
			{"G\\WEAPONS\\Vvh_flag\\eqp\\Vvh_flag_VC_3pv.eqp"}
	};


// Client tick - update radar colors for players
void CLN_UpdateRadarColors(void){
	dword i, pc;
	s_SC_P_getinfo pc_info, pl_info;
	s_SC_MP_EnumPlayers enum_pl[64];
	dword count = 64;

	pc = SC_PC_Get();
	if (!pc) return;

	SC_P_GetInfo(pc, &pc_info);

	if (SC_MP_EnumPlayers(enum_pl, &count, SC_MP_ENUMPLAYER_SIDE_ALL)){
		for (i = 0; i < count; i++){
			if (enum_pl[i].status == SC_MP_P_STATUS_INGAME){
				if (enum_pl[i].side == pc_info.side){
					SC_P_SetRadarColor(enum_pl[i].id, 0x440000ff); // blue for allies
				} else {
					SC_P_SetRadarColor(enum_pl[i].id, 0x44ff0000); // red for enemies
				}

				// Force class name for bots (member_id != 0 means AI player)
				SC_P_GetInfo(enum_pl[i].id, &pl_info);
				if (pl_info.member_id != 0){
					SC_P_SetForceClassName(enum_pl[i].id, 1100);
				}
			}
		}
	}
}


// Custom GetNearestPlayer implementation for 4x4 mode
dword GetNearestPlayer(c_Vector3 *pos, float *out_dist){
	dword list[64];
	dword count = 64;
	dword i;
	dword nearest = 0;
	float min_dist = 10000.0f;
	float dist;
	c_Vector3 pl_pos;
	s_sphere sph;
	s_SC_P_getinfo info;

	sph.pos = *pos;
	sph.rad = 1000.0f;

	SC_GetPls(&sph, list, &count);

	for (i = 0; i < count; i++){
		SC_P_GetInfo(list[i], &info);
		if (!SC_P_IsReady(list[i])) continue;
		if (!SC_P_GetActive(list[i])) continue;

		SC_P_GetPos(list[i], &pl_pos);
		dist = SC_2VectorsDist(pos, &pl_pos);

		if (dist < min_dist){
			min_dist = dist;
			nearest = list[i];
		}
	}

	*out_dist = min_dist;
	return nearest;
}


// ============================================================================
// BUDDY SYSTEM - Functions
// ============================================================================

/*
 * IsBotInPair - Check if a bot (by handle) is already in a buddy pair
 * Returns: pair index (0-3) if found, -1 if not in any pair
 */
int IsBotInPair(dword bot_handle){
	int i;
	for (i = 0; i < gBuddyPairCount; i++){
		if (gBuddyPairs[i][0] == bot_handle || gBuddyPairs[i][1] == bot_handle){
			return i;
		}
	}
	return -1;
}

/*
 * RemoveBuddyPair - Remove a pair by index and notify both bots
 */
void RemoveBuddyPair(int pair_index){
	dword leader_id, buddy_id;
	int i;

	if (pair_index < 0 || pair_index >= gBuddyPairCount) return;

	// Get player IDs from handles
	leader_id = SC_MP_GetPlofHandle(gBuddyPairs[pair_index][0]);
	buddy_id = SC_MP_GetPlofHandle(gBuddyPairs[pair_index][1]);

	// Notify bots about unpairing
	if (leader_id) SC_P_ScriptMessage(leader_id, BOT_MSG_UNPAIR, 0);
	if (buddy_id) SC_P_ScriptMessage(buddy_id, BOT_MSG_UNPAIR, 0);

	// Remove pair by shifting array
	for (i = pair_index; i < gBuddyPairCount - 1; i++){
		gBuddyPairs[i][0] = gBuddyPairs[i + 1][0];
		gBuddyPairs[i][1] = gBuddyPairs[i + 1][1];
	}
	gBuddyPairCount--;
}

/*
 * NotifyBuddyOfDeath - Called when a bot dies, notify their partner
 */
void NotifyBuddyOfDeath(dword dead_handle){
	int pair_index = IsBotInPair(dead_handle);
	dword partner_id;

	if (pair_index < 0) return;

	// Find partner and notify them
	if (gBuddyPairs[pair_index][0] == dead_handle){
		// Dead was leader - notify buddy
		partner_id = SC_MP_GetPlofHandle(gBuddyPairs[pair_index][1]);
		if (partner_id) SC_P_ScriptMessage(partner_id, BOT_MSG_LEADER_DIED, 0);
	} else {
		// Dead was buddy - notify leader
		partner_id = SC_MP_GetPlofHandle(gBuddyPairs[pair_index][0]);
		if (partner_id) SC_P_ScriptMessage(partner_id, BOT_MSG_BUDDY_DIED, 0);
	}

	// Remove the pair
	RemoveBuddyPair(pair_index);
}

/*
 * UpdateBuddyPairs - Main buddy system logic, called every SERVER_TICK
 *
 * Logic:
 * 1. Clean up invalid pairs (dead/disconnected players)
 * 2. Find unpaired bots on same side
 * 3. Create new pairs (same side only!)
 * 4. Optionally pair bot with human flag carrier
 */
void UpdateBuddyPairs(float elapsed){
	dword i, j, count;
	s_SC_MP_EnumPlayers enum_pl[64];
	s_SC_P_getinfo info;
	dword solo_bots_us[8], solo_bots_vc[8];
	int solo_count_us = 0, solo_count_vc = 0;
	dword human_flag_carrier[2] = {0, 0};  // [0]=US flag carrier, [1]=VC flag carrier
	dword leader_id, buddy_id;     // For cleanup loop
	dword bot_handle;              // For enumeration loop
	dword leader, buddy;           // For pairing loops
	dword solo_bot;                // For human flag carrier

	// Update timer
	gBuddyUpdateTimer -= elapsed;
	if (gBuddyUpdateTimer > 0.0f) return;
	gBuddyUpdateTimer = BUDDY_UPDATE_INTERVAL;

	// Step 1: Clean up invalid pairs
	for (i = gBuddyPairCount; i > 0; i--){
		leader_id = SC_MP_GetPlofHandle(gBuddyPairs[i-1][0]);
		buddy_id = SC_MP_GetPlofHandle(gBuddyPairs[i-1][1]);

		// Check if both are still valid and alive
		if (!leader_id || !buddy_id ||
			!SC_P_IsReady(leader_id) || !SC_P_IsReady(buddy_id)){
			RemoveBuddyPair(i - 1);
		}
	}

	// Step 2: Enumerate all players
	count = 64;
	if (!SC_MP_EnumPlayers(enum_pl, &count, SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i = 0; i < count; i++){
		if (enum_pl[i].status != SC_MP_P_STATUS_INGAME) continue;

		SC_P_GetInfo(enum_pl[i].id, &info);

		// Track human flag carriers (for optional buddy-to-human pairing)
		if (info.member_id == 0){
			// Human player - check if carrying enemy flag
			if (enum_pl[i].side == 0 && gFlagOnPlayer_handle[1] == SC_MP_GetHandleofPl(enum_pl[i].id)){
				human_flag_carrier[0] = enum_pl[i].id;  // US human has VC flag
			}
			if (enum_pl[i].side == 1 && gFlagOnPlayer_handle[0] == SC_MP_GetHandleofPl(enum_pl[i].id)){
				human_flag_carrier[1] = enum_pl[i].id;  // VC human has US flag
			}
			continue;  // Skip humans for bot pairing
		}

		// Bot player - check if already paired
		bot_handle = SC_MP_GetHandleofPl(enum_pl[i].id);
		if (IsBotInPair(bot_handle) >= 0) continue;

		// Bot is unpaired - add to solo list by side
		if (enum_pl[i].side == 0 && solo_count_us < 8){
			solo_bots_us[solo_count_us++] = enum_pl[i].id;
		}
		if (enum_pl[i].side == 1 && solo_count_vc < 8){
			solo_bots_vc[solo_count_vc++] = enum_pl[i].id;
		}
	}

	// Step 3: Pair solo bots on US side
	for (i = 0; i + 1 < solo_count_us && gBuddyPairCount < MAX_BUDDY_PAIRS; i += 2){
		leader = solo_bots_us[i];
		buddy = solo_bots_us[i + 1];

		// Create pair
		gBuddyPairs[gBuddyPairCount][0] = SC_MP_GetHandleofPl(leader);
		gBuddyPairs[gBuddyPairCount][1] = SC_MP_GetHandleofPl(buddy);
		gBuddyPairCount++;

		// Notify bots
		SC_P_ScriptMessage(leader, BOT_MSG_BECOME_LEADER, buddy);
		SC_P_ScriptMessage(buddy, BOT_MSG_BECOME_BUDDY, leader);
	}

	// Step 4: Pair solo bots on VC side
	for (i = 0; i + 1 < solo_count_vc && gBuddyPairCount < MAX_BUDDY_PAIRS; i += 2){
		leader = solo_bots_vc[i];
		buddy = solo_bots_vc[i + 1];

		// Create pair
		gBuddyPairs[gBuddyPairCount][0] = SC_MP_GetHandleofPl(leader);
		gBuddyPairs[gBuddyPairCount][1] = SC_MP_GetHandleofPl(buddy);
		gBuddyPairCount++;

		// Notify bots
		SC_P_ScriptMessage(leader, BOT_MSG_BECOME_LEADER, buddy);
		SC_P_ScriptMessage(buddy, BOT_MSG_BECOME_BUDDY, leader);
	}

	// Step 5: If there's a solo bot and human flag carrier on same side, pair them
	// Solo bot becomes buddy to the human
	if (solo_count_us % 2 == 1 && human_flag_carrier[0]){
		solo_bot = solo_bots_us[solo_count_us - 1];
		SC_P_ScriptMessage(solo_bot, BOT_MSG_FOLLOW_HUMAN, human_flag_carrier[0]);
	}
	if (solo_count_vc % 2 == 1 && human_flag_carrier[1]){
		solo_bot = solo_bots_vc[solo_count_vc - 1];
		SC_P_ScriptMessage(solo_bot, BOT_MSG_FOLLOW_HUMAN, human_flag_carrier[1]);
	}
}

/*
 * NotifyBuddyOfCamping - Called when leader starts camping
 * Buddy should continue alone to the flag
 */
void NotifyBuddyOfCamping(dword leader_handle){
	int pair_index = IsBotInPair(leader_handle);
	dword buddy_id;

	if (pair_index < 0) return;
	if (gBuddyPairs[pair_index][0] != leader_handle) return;  // Only leader can trigger this

	buddy_id = SC_MP_GetPlofHandle(gBuddyPairs[pair_index][1]);
	if (buddy_id){
		SC_P_ScriptMessage(buddy_id, BOT_MSG_LEADER_CAMPING, 0);
	}
}


BOOL SRV_CheckEndRule(float time){

	switch(gEndRule){
		case SC_MP_ENDRULE_TIME:

			if (gMission_started) gTime += time;
			SC_MP_EndRule_SetTimeLeft(gTime,gMission_started);

			if (gTime>gEndValue){
				SC_MP_LoadNextMap();
				return TRUE;
			}

			break;

		case SC_MP_ENDRULE_POINTS:

			if ((gSidePoints[0]>=gEndValue)||(gSidePoints[1]>=gEndValue)){
				SC_MP_LoadNextMap();
				return TRUE;
			}

			break;

		default:
			SC_message("EndRule unsopported: %d",gEndRule);
			break;

	}// switch(gEndRule)

	return FALSE;

}// void SRV_CheckEndRule(float time)


float GetRecovTime(void){
	float val;

	val = SC_ggf(400);
	if (val==0) val = 30.0f;
	return val;
}

float GetRecovLimitTime(void){
	float val;

	val = SC_ggf(401);
	if (val==0){
		val = 10.0f;
	}

	return val;
}

void UpdateSidePoints(void){
	SC_sgi(GVAR_SIDE0POINTS,gSidePoints[0]);
	SC_sgi(GVAR_SIDE1POINTS,gSidePoints[1]);
}// void UpdateSidePoints(void)


void SRV_ChechSendStatus(void){
	dword i;

	for (i=0;i<2;i++){

		if (gFlagPhase[i]!=gSend_FlagPhase[i]){
			gSend_FlagPhase[i] = gFlagPhase[i];
			SC_sgi(GVAR_FLAGSTATUS+i,gSend_FlagPhase[i]);
		}


		if (gSend_FlagOnPlayer[i]!=gFlagOnPlayer_handle[i]){
			gSend_FlagOnPlayer[i] = gFlagOnPlayer_handle[i];
			SC_sgi(GVAR_ONPLAYER+i,gFlagOnPlayer_handle[i]);
		}

		if (gInfoLastScorePlayer[i]!=gSend_InfoLastScorePlayer[i]){
			gSend_InfoLastScorePlayer[i] = gInfoLastScorePlayer[i];
			SC_sgi(GVAR_SCOREPL+i,gSend_InfoLastScorePlayer[i]);
		}

		if (gSend_Info[i]!=gInfo[i]){
			gSend_Info[i] = gInfo[i];
			SC_sgi(GVAR_INFO+i,gSend_Info[i]);
		}// if (gInfo[i]!=gSend_Info[i])

	}// for (i)

}// void SRV_ChechSendStatus(void)


void CLN_SetOnPlayerEqp(dword side, dword onplayer){
	dword handle,plid,pc;
	s_SC_P_getinfo pl_info;

	handle = SC_MP_GetHandleofPl(onplayer);

	if (handle!=gCLN_eqp_pl_handle[side]){

		// need change
		if (gCLN_eqp_pl_handle[side]){

			plid = SC_MP_GetPlofHandle(gCLN_eqp_pl_handle[side]);
			if (plid) SC_P_UnLink3pvEqp(plid,0);
		}

		gCLN_eqp_pl_handle[side] = handle;

		if (handle){
			SC_P_Link3pvEqp(onplayer,0,PRELOADBES_FLAG_US+side,gEQP_name[side]);
		}

		pc = SC_PC_Get();
		if (pc){
			SC_P_GetInfo(pc,&pl_info);
			if (pl_info.side!=side){

				if (onplayer){
					gCLN_HelpInfo_timer = 5.0f;
					swprintf(gCLN_HelpInfo,SC_Wtxt(1130),SC_P_GetName(onplayer));
				}
			}
		}


	}//if (handle!=gCLN_eqp_pl_handle[side])

}// void CLN_SetOnPlayerEqp(dword side, dword onplayer)



void ResetMission(void){
	dword i;


	for (i=0;i<2;i++){

		switch(gFlagPhase[i]){

			case FLAG_PH_INBASE:
					break;
			case FLAG_PH_ONGROUND:
					gInfo[i] = INFO_FL_RETURNED;
					gFlagPhase[i] = FLAG_PH_INBASE;
					SC_SRV_Item_Release(gOnGroundNetID[i]);
					gOnGroundNetID[i] = 0;
					break;
			case FLAG_PH_ONPLAYER:
					gFlagOnPlayer_handle[i] = 0;
					gFlagPhase[i] = FLAG_PH_INBASE;
					gInfo[i] = INFO_FL_RETURNED;
					break;

		}// switch(gFlagPhase[i])


	}// for (i)

}// void ResetMission(void)


// Check_ABL disabled for 4x4 mode
void Check_ABL(dword pl_handle){
	// Auto-balance disabled in 4x4 bot mode
}


// Recover dead/sleeping AI bots to fill teams up to MIN_PLAYERS_PER_TEAM
// Counts ALL human players (alive + dead) to determine bot slots
void RecoverAllDeadAi(void){
	dword i, count, side;
	s_SC_MP_EnumPlayers enum_pl[64];
	s_SC_P_getinfo info;
	dword human_count[2] = {0, 0};
	dword alive_bots[2] = {0, 0};
	dword bots_to_recover[2];

	count = 64;
	if (SC_MP_EnumPlayers(enum_pl, &count, SC_MP_ENUMPLAYER_SIDE_ALL)){
		// First pass: count players per side
		for (i = 0; i < count; i++){
			side = enum_pl[i].side;
			if (side >= 2) continue;

			SC_P_GetInfo(enum_pl[i].id, &info);

			// Handle NOTINGAME players
			if (enum_pl[i].status == SC_MP_P_STATUS_NOTINGAME){
				// Don't count NOTINGAME humans - they might be counted elsewhere
				// (e.g., still as INGAMEDEATH on old side while switching)
				// AI not in game - will be recovered below if needed
				continue;
			}

			// Count ALL human players (alive or dead) - they occupy a slot
			// Dead humans will respawn, so they still "reserve" their slot
			if (info.member_id == 0){
				human_count[side]++;
			}

			// Count only ALIVE BOTS (not humans, not dead bots)
			if (info.member_id != 0 && enum_pl[i].status == SC_MP_P_STATUS_INGAME){
				alive_bots[side]++;
			}
		}

		// Calculate how many bots to recover per side
		// max_bots = how many bot slots are available (4 - humans)
		// bots_to_recover = how many bots are missing (max_bots - alive_bots)
		for (i = 0; i < 2; i++){
			dword max_bots = (human_count[i] >= MIN_PLAYERS_PER_TEAM) ? 0 : (MIN_PLAYERS_PER_TEAM - human_count[i]);
			bots_to_recover[i] = (alive_bots[i] < max_bots) ? (max_bots - alive_bots[i]) : 0;
		}

		// Second pass: recover dead/sleeping bots up to the limit
		for (i = 0; i < count; i++){
			side = enum_pl[i].side;
			if (side >= 2) continue;

			// Check for dead or sleeping bots (NOTINGAME = not yet spawned)
			if (enum_pl[i].status == SC_MP_P_STATUS_INGAMEDEATH ||
				enum_pl[i].status == SC_MP_P_STATUS_NOTINGAME){

				if (bots_to_recover[side] > 0){
					// SC_MP_RecoverAiPlayer returns TRUE only for AI players
					if (SC_MP_RecoverAiPlayer(enum_pl[i].id, NULL, 0.0f)){
						bots_to_recover[side]--;
					}
				}
			}
		}
	}
}


// Get killstreak slot from player handle (simple hash)
dword GetStreakSlot(dword pl_handle){
	return pl_handle & 63;
}

// Set killstreak info (flag events have priority)
void SetKillstreakInfo(dword info_value, dword killer_handle){
	// Flag events (1-4) have priority - don't overwrite
	if (gInfo[0] >= INFO_FL_STOLEN && gInfo[0] <= INFO_SCORE) return;

	gInfo[0] = info_value;
	SC_sgi(GVAR_KILLSTREAK_PLAYER, killer_handle);
}

// Check killstreak milestone and set info
void CheckKillstreak(dword killer_handle, dword streak){
	if (streak == STREAK_GODLIKE){
		SetKillstreakInfo(INFO_STREAK_GODLIKE, killer_handle);
	}
	else if (streak == STREAK_UNSTOPPABLE){
		SetKillstreakInfo(INFO_STREAK_UNSTOPPABLE, killer_handle);
	}
	else if (streak == STREAK_RAMPAGE){
		SetKillstreakInfo(INFO_STREAK_RAMPAGE, killer_handle);
	}
	else if (streak == STREAK_ONROLL){
		SetKillstreakInfo(INFO_STREAK_ONROLL, killer_handle);
	}
}


int ScriptMain(s_SC_NET_info *info){
	char txt[128],*itxt;
	ushort wtxt[128],wtxt2[64],*witxt;
	dword i,j,pl_id,pl_val;
	s_SC_MP_Recover *precov;
	s_SC_MP_hud hudinfo;
	s_SC_P_getinfo plinfo;
	void *nod;
	c_Vector3 vec,vec2;
	BOOL valid,inbase;
	float pl_dist;
	s_SC_HUD_MP_icon icon[2];
	s_SC_MP_EnumPlayers enum_pl[64];
	BOOL side[2];
	s_SC_MP_SRV_settings SRVset;
	float val,valy;

#if _GE_VERSION_ >= 138
	s_SC_FpvMapSign fpv_list[2];
#endif

	switch(info->message){

		case SC_NET_MES_SERVER_TICK:

			if (SRV_CheckEndRule(info->elapsed_time)) break;



			side[0] = side[1] = FALSE;
			j = 64;

			if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)){


				if ((j==0)&&((gSidePoints[0]+gSidePoints[1])!=0)){
					gSidePoints[0] = 0;
					gSidePoints[1] = 0;
					UpdateSidePoints();
				}// if ((side[0]+side[1])==0)

				for (i=0;i<j;i++)
					if (enum_pl[i].status!=SC_MP_P_STATUS_NOTINGAME){

						if (enum_pl[i].side<2) side[enum_pl[i].side] = TRUE;

					}// if (enum_pl[i].status==SC_MP_P_STATUS_INGAME)

				gMission_starting_timer -= info->elapsed_time;

				if ((side[0])&&(side[1])){

					SC_MP_SetInstantRecovery(FALSE);

					if (!gMission_started){
						gMission_started = TRUE;
						gMission_afterstart_time = 0.0f;
						SC_sgi(GVAR_GAMERUNS,gMission_started);
						ResetMission();
						SC_MP_SRV_InitGameAfterInactive();
						SC_MP_RecoverAllNoAiPlayers();
						RecoverAllDeadAi();  // 4x4: Recover only needed AI players
						gMission_starting_timer = 8.0f;
					}
				}// if ((side[0])&&(side[1]))
				else{

					if (gMission_starting_timer<=0.0f){

						SC_MP_SetInstantRecovery(TRUE);

						if (gMission_started){
							gMission_started = FALSE;
							gMission_afterstart_time = 0.0f;
							SC_sgi(GVAR_GAMERUNS,gMission_started);
							ResetMission();
						}

					}

				}// else if ((side[0])&&(side[1]))

			}// if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL))

			for (j=0;j<2;j++)
			for (i=0;i<gRecs[j];i++)
				gRecTimer[j][i] -= info->elapsed_time;


			gNextRecover -= info->elapsed_time;
			if (gNextRecover < 0.0f){
				gNextRecover = GetRecovTime();

				// Oživit mrtvé AI ve stejné vlně jako lidi
				if (gMission_started){
					RecoverAllDeadAi();
					sprintf(txt, "Reinforcements spawning!");
					SC_GameInfoW(SC_AnsiToUni(txt, wtxt));
				}
			}

			if (gMission_started){


				for (i=0;i<2;i++){

					valid = FALSE;

					switch(gFlagPhase[i]){

						case FLAG_PH_INBASE:
	in_base:
								vec = gOrigFlagPos[i];
								valid = TRUE;
								break;
						case FLAG_PH_ONGROUND:
								if (SC_Item_GetPos(gOnGroundNetID[i],&vec)) valid = TRUE;
									else gOnGroundTimer[i] = 0.0f;

								gOnGroundTimer[i] -= info->elapsed_time;
								if (gOnGroundTimer[i]<0.0f){
									gInfo[i] = INFO_FL_RETURNED;
									gFlagPhase[i] = FLAG_PH_INBASE;

									SC_SRV_Item_Release(gOnGroundNetID[i]);
									gOnGroundNetID[i] = 0;

									valid = FALSE;
								}// if (gOnGroundTimer[i]<0.0f)

								break;
						case FLAG_PH_ONPLAYER:

								pl_id = SC_MP_GetPlofHandle(gFlagOnPlayer_handle[i]);

								if (!pl_id){
									gFlagOnPlayer_handle[i] = 0;
									gFlagPhase[i] = FLAG_PH_INBASE;
									goto in_base;
								}// if (!pl_id)


								SC_P_GetInfo(pl_id,&plinfo);

								if (plinfo.side==i){
									gFlagOnPlayer_handle[i] = 0;
									gFlagPhase[i] = FLAG_PH_INBASE;
									goto in_base;
								}

								SC_P_GetPos(pl_id,&vec);

								if (gFlagPhase[1-i]==FLAG_PH_INBASE){

									vec2 = gOrigFlagPos[1-i];

									if (SC_IsNear3D(&vec,&vec2,1.5f)){
										SC_P_MP_AddPoints(pl_id,1);
										gSidePoints[1-i]++;
										UpdateSidePoints();

										gInfo[i] = INFO_SCORE;
										gInfoLastScorePlayer[i] = gFlagOnPlayer_handle[i];

										gFlagPhase[i] = FLAG_PH_INBASE;
										gFlagOnPlayer_handle[i] = 0;

									}

								}// if (gFlagPhase[1-i]==FLAG_PH_INBASE)

								break;

					}// switch(gFlagPhase[i])


					gMission_afterstart_time += info->elapsed_time;


					if ((gMission_afterstart_time>5.0f)&&(valid)){

						j = GetNearestPlayer(&vec,&pl_dist);

						if ((j)&&(pl_dist<1.5f)){

							SC_P_GetInfo(j,&plinfo);

							switch(gFlagPhase[i]){

								case FLAG_PH_INBASE:
										if (plinfo.side!=i){
											gInfo[i] = INFO_FL_STOLEN;
											gFlagPhase[i] = FLAG_PH_ONPLAYER;
											gFlagOnPlayer_handle[i] = SC_MP_GetHandleofPl(j);

											// Notify bot about flag pickup (member_id != 0 means AI player)
											if (plinfo.member_id != 0){
												SC_P_ScriptMessage(j, BOT_MSG_FLAG_PICKUP, 0);
											}
										}
										break;
								case FLAG_PH_ONGROUND:

										if (plinfo.side!=i){
											gInfo[i] = INFO_FL_STOLEN;
											gFlagPhase[i] = FLAG_PH_ONPLAYER;
											gFlagOnPlayer_handle[i] = SC_MP_GetHandleofPl(j);

											// Notify bot about flag pickup (member_id != 0 means AI player)
											if (plinfo.member_id != 0){
												SC_P_ScriptMessage(j, BOT_MSG_FLAG_PICKUP, 0);
											}
										}
										else{
											gInfo[i] = INFO_FL_RETURNED;
											gFlagPhase[i] = FLAG_PH_INBASE;
										}

										SC_SRV_Item_Release(gOnGroundNetID[i]);
										gOnGroundNetID[i] = 0;
										break;

							}// switch(gFlagPhase[i])


						}// if ((j)&&(pl_dist<1.0f))

					}// if (valid)

				}// for (i) - for both flags

				// BUDDY SYSTEM: Update buddy pairs
				UpdateBuddyPairs(info->elapsed_time);

			}// if (gMission_started)


			SRV_ChechSendStatus();

			break;

		case SC_NET_MES_CLIENT_TICK:

			CLN_UpdateRadarColors();

			if (gCLN_HelpInfo_timer>0.0f){
				gCLN_HelpInfo_timer -= info->elapsed_time;
			}

			pl_id = SC_PC_Get();

			for (i=0;i<2;i++){

				gCLN_SidePoints[i] = SC_ggi(GVAR_SIDE0POINTS+i);
				SC_MP_SetSideStats(i,0,gCLN_SidePoints[i]);

				gCLN_FlagPhase[i] = SC_ggi(GVAR_FLAGSTATUS+i);
				gCLN_FlagOnPlayer[i] = SC_MP_GetPlofHandle(SC_ggi(GVAR_ONPLAYER+i));

				j = SC_ggi(GVAR_INFO+i);
				if (j!=gCLN_Info[i]){
					gCLN_Info[i] = j;

					switch(j){
						case INFO_FL_STOLEN:
								swprintf(wtxt,SC_AnsiToUni("%s %s",wtxt2),SC_Wtxt(1010+i),SC_Wtxt(1067));
								// play sound
								if (gCLN_FlagOnPlayer[i]==SC_PC_Get()){
									SC_SND_PlaySound2D(10424);
								}
								else{
									SC_SND_PlaySound2D(10425);
								}

								break;
						case INFO_FL_DROPPED:swprintf(wtxt,SC_AnsiToUni("%s %s",wtxt2),SC_Wtxt(1010+i),SC_Wtxt(1068));break;
						case INFO_FL_RETURNED:swprintf(wtxt,SC_AnsiToUni("%s %s",wtxt2),SC_Wtxt(1010+i),SC_Wtxt(1069));break;
						case INFO_SCORE:
								// improve message, add player name

								pl_val = SC_ggi(GVAR_SCOREPL+i);
								pl_val = SC_MP_GetPlofHandle(pl_val);

								if (pl_val)
									swprintf(wtxt,SC_AnsiToUni("%s (%S) %s",wtxt2),SC_Wtxt(1011-i),SC_P_GetName(pl_val),SC_Wtxt(1070));
								else
									swprintf(wtxt,SC_AnsiToUni("%s %s",wtxt2),SC_Wtxt(1011-i),SC_Wtxt(1070));

								// play sound
								SC_SND_PlaySound2D(11116+i);
								break;

						// Killstreak messages
						case INFO_STREAK_ONROLL:
								pl_val = SC_MP_GetPlofHandle(SC_ggi(GVAR_KILLSTREAK_PLAYER));
								if (pl_val)
									swprintf(wtxt,SC_AnsiToUni("%S is ON A ROLL!",wtxt2),SC_P_GetName(pl_val));
								else
									SC_AnsiToUni("ON A ROLL!", wtxt);
								break;
						case INFO_STREAK_RAMPAGE:
								pl_val = SC_MP_GetPlofHandle(SC_ggi(GVAR_KILLSTREAK_PLAYER));
								if (pl_val)
									swprintf(wtxt,SC_AnsiToUni("%S is on a RAMPAGE!",wtxt2),SC_P_GetName(pl_val));
								else
									SC_AnsiToUni("RAMPAGE!", wtxt);
								break;
						case INFO_STREAK_UNSTOPPABLE:
								pl_val = SC_MP_GetPlofHandle(SC_ggi(GVAR_KILLSTREAK_PLAYER));
								if (pl_val)
									swprintf(wtxt,SC_AnsiToUni("%S is UNSTOPPABLE!",wtxt2),SC_P_GetName(pl_val));
								else
									SC_AnsiToUni("UNSTOPPABLE!", wtxt);
								break;
						case INFO_STREAK_GODLIKE:
								pl_val = SC_MP_GetPlofHandle(SC_ggi(GVAR_KILLSTREAK_PLAYER));
								if (pl_val)
									swprintf(wtxt,SC_AnsiToUni("%S is GODLIKE!",wtxt2),SC_P_GetName(pl_val));
								else
									SC_AnsiToUni("GODLIKE!", wtxt);
								break;
					}// switch(j)

					SC_GameInfoW(wtxt);

				}// if (j!=gCLNd_Info[i])


				if ((pl_id)&&(gCLN_FlagOnPlayer[i]==pl_id)){

					 gCLN_MyFlagTimer += info->elapsed_time;
					 while (gCLN_MyFlagTimer > 1.0f) gCLN_MyFlagTimer -= 1.0f;

					 if (gCLN_MyFlagTimer>0.5f) icon[i].color = (dword)(511.0f * (gCLN_MyFlagTimer-0.5f));
						else icon[i].color = (dword)(511.0f * (0.5f-gCLN_MyFlagTimer));

					icon[i].color <<= 24;

					icon[i].color += 0x00ffffff;

				}
				else
					icon[i].color = 0xffffffff;


				icon[i].type = SC_HUD_MP_ICON_TYPE_NUMBER;
				icon[i].icon_id = 3*i;
				icon[i].value = gCLN_SidePoints[i];

				j = 0;

				switch(gCLN_FlagPhase[i]){

					case FLAG_PH_INBASE:
						inbase = TRUE;
						break;
					case FLAG_PH_ONPLAYER:
						icon[i].icon_id+=1;
						inbase = FALSE;
						j = gCLN_FlagOnPlayer[i];
						break;

					case FLAG_PH_ONGROUND:
						icon[i].icon_id+=2;
						inbase = FALSE;
						break;

				}// switch(gCLN_FlagPhase[i])

				CLN_SetOnPlayerEqp(i,j);

				SC_DUMMY_Set_DoNotRenHier2(gFlagNod[i],!inbase);

			}// for (i)

			SC_MP_SetIconHUD(icon,2);


		#if _GE_VERSION_ >= 138

			fpv_list[0].color = 0xffffffff;
			fpv_list[0].scale = 1.0f;
			fpv_list[0].id = g_FPV_UsFlag;
			fpv_list[0].pos = gOrigFlagPos[0];

			fpv_list[1].color = 0xffffffff;
			fpv_list[1].scale = 1.0f;
			fpv_list[1].id = g_FPV_VcFlag;
			fpv_list[1].pos = gOrigFlagPos[1];


			SC_MP_FpvMapSign_Set(2,fpv_list);
		#endif

			break;// SC_NET_MES_CLIENT_TICK


		case SC_NET_MES_LEVELPREINIT:
			SC_sgi(GVAR_MP_MISSIONTYPE,GVAR_MP_MISSIONTYPE_CTF);

			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;

			// 4x4: Initialize bot counts
			SC_sgi(GVAR_BOTCOUNT_US, MIN_PLAYERS_PER_TEAM);
			SC_sgi(GVAR_BOTCOUNT_VC, MIN_PLAYERS_PER_TEAM);

			SC_MP_EnableBotsFromScene(TRUE);  // 4x4: Enable bots

			break;// SC_NET_MES_LEVELPREINIT

		case SC_NET_MES_LEVELINIT:


		#if _GE_VERSION_ >= 138
			g_FPV_UsFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_USflag.BES");
			g_FPV_VcFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_VCflag.BES");
		#endif

			// 4x4: Set command menu for bot control
			SC_SetCommandMenu(2909);

			SC_MP_SRV_SetForceSide(0xffffffff);
			SC_MP_SetChooseValidSides(3);


			SC_MP_SRV_SetClassLimit(18,0);
			SC_MP_SRV_SetClassLimit(19,0);
			SC_MP_SRV_SetClassLimit(39,0);

			SC_MP_GetSRVsettings(&SRVset);

			for (i=0;i<6;i++){
				SC_MP_SRV_SetClassLimit(i+1,SRVset.atg_class_limit[i]);
				SC_MP_SRV_SetClassLimit(i+21,SRVset.atg_class_limit[i]);
			}// for (i)


			CLEAR(hudinfo);
			hudinfo.title = 1071;

			hudinfo.sort_by[0] = SC_HUD_MP_SORTBY_POINTS;
			hudinfo.sort_by[1] = SC_HUD_MP_SORTBY_KILLS;
			hudinfo.sort_by[2] = SC_HUD_MP_SORTBY_DEATHS | SC_HUD_MP_SORT_DOWNUP;
			hudinfo.sort_by[3] = SC_HUD_MP_SORTBY_PINGS | SC_HUD_MP_SORT_DOWNUP;


			hudinfo.pl_mask = SC_HUD_MP_PL_MASK_CLASS | SC_HUD_MP_PL_MASK_POINTS | SC_HUD_MP_PL_MASK_KILLS | SC_HUD_MP_PL_MASK_DEATHS;
			hudinfo.use_sides = TRUE;
			hudinfo.side_name[0] = 1010;
			hudinfo.side_color[0] = 0x440000ff;
			hudinfo.side_name[1] = 1011;
			hudinfo.side_color[1] = 0x44ff0000;

			hudinfo.side_mask = SC_HUD_MP_SIDE_MASK_POINTS;


			SC_MP_HUD_SetTabInfo(&hudinfo);

			SC_MP_AllowStPwD(TRUE);
			SC_MP_AllowFriendlyFireOFF(TRUE);

			SC_MP_SetItemsNoDisappear(FALSE);

			gMission_started = FALSE;

			if (info->param2){

				// preload flag items
				SC_Item_Preload(145);
				SC_Item_Preload(146);

				// preload flag eqp items
				SC_PreloadBES(PRELOADBES_FLAG_US,"G\\WEAPONS\\Vvh_flag\\Vvh_flag_US_3pv.BES");
				SC_PreloadBES(PRELOADBES_FLAG_VC,"G\\WEAPONS\\Vvh_flag\\Vvh_flag_VC_3pv.BES");


				nod = SC_NOD_Get(NULL,"flag_us");
				if (!nod) SC_message("US flag not found 01");
				gFlagNod[0] = SC_NOD_Get(nod,"Vlajka US");
				if (!gFlagNod[0]) SC_message("VC flag not found 01");
				SC_NOD_GetWorldPos(nod,&gOrigFlagPos[0]);

				nod = SC_NOD_Get(NULL,"flag_vc");
				if (!nod) SC_message("VC flag not found 01");
				gFlagNod[1] = SC_NOD_Get(nod,"Vlajka VC");
				if (!gFlagNod[1]) SC_message("VC flag not found 02");
				SC_NOD_GetWorldPos(nod,&gOrigFlagPos[1]);


				if (info->param1){
					// it's server

					SC_Log(3,"difficulty setting is %d",SC_ggi(SGI_DIFFICULTY));

					// 4x4: Set bot counts
					SC_sgi(GVAR_BOTCOUNT_US, MIN_PLAYERS_PER_TEAM);
					SC_sgi(GVAR_BOTCOUNT_VC, MIN_PLAYERS_PER_TEAM);

					SC_MP_Gvar_SetSynchro(GVAR_SIDE0POINTS);
					SC_MP_Gvar_SetSynchro(GVAR_SIDE1POINTS);
					UpdateSidePoints();

					SC_MP_Gvar_SetSynchro(GVAR_GAMERUNS);
					SC_sgi(GVAR_GAMERUNS,0);


					for (i=0;i<2;i++){
						SC_MP_Gvar_SetSynchro(GVAR_FLAGSTATUS+i);
						SC_sgi(GVAR_FLAGSTATUS+i,FLAG_PH_INBASE);

						SC_MP_Gvar_SetSynchro(GVAR_ONPLAYER+i);
						SC_sgi(GVAR_ONPLAYER+i,0);

						SC_MP_Gvar_SetSynchro(GVAR_INFO+i);
						SC_sgi(GVAR_ONPLAYER+i,0);

						SC_MP_Gvar_SetSynchro(GVAR_SCOREPL+i);
						SC_sgi(GVAR_SCOREPL+i,0);

					}

					// Killstreak sync
					SC_MP_Gvar_SetSynchro(GVAR_KILLSTREAK_PLAYER);
					SC_sgi(GVAR_KILLSTREAK_PLAYER, 0);
					CLEAR(gKillstreaks);


					CLEAR(gRecs);

					for (i=0;i<REC_MAX;i++){
						sprintf(txt,REC_WPNAME_US,i);
						if (SC_NET_FillRecover(&gRec[0][gRecs[0]],txt)) gRecs[0]++;
					}

#if _GE_VERSION_ >= 133
					i = REC_MAX - gRecs[0];
					SC_MP_GetRecovers(SC_MP_RESPAWN_CTF_US,&gRec[0][gRecs[0]],&i);
					gRecs[0] += i;
#endif

					SC_Log(3,"CTF respawns us: %d",gRecs[0]);

					if (gRecs[0]==0) SC_message("no US recover place defined!");

					for (i=0;i<REC_MAX;i++){
						sprintf(txt,REC_WPNAME_VC,i);
						if (SC_NET_FillRecover(&gRec[1][gRecs[1]],txt)) gRecs[1]++;
					}

#if _GE_VERSION_ >= 133
					i = REC_MAX - gRecs[1];
					SC_MP_GetRecovers(SC_MP_RESPAWN_CTF_VC,&gRec[1][gRecs[1]],&i);
					gRecs[1] += i;
#endif

					SC_Log(3,"CTF respawns vc: %d",gRecs[1]);


					if (gRecs[1]==0) SC_message("no VC recover place defined!");

					CLEAR(gRecTimer);

				}// if (info->param1)

			}//if (info->param2)


			break;// SC_NET_MES_LEVELINIT


		case SC_NET_MES_RENDERHUD:

			witxt = NULL;

			if (SC_ggi(GVAR_GAMERUNS)){
				if (gCLN_HelpInfo_timer>0.0f){
					witxt = gCLN_HelpInfo;
				}
			}
			else{
				witxt = SC_Wtxt(101);
			}


			if (witxt){

				SC_GetScreenRes(&val,&valy);

				val -= SC_Fnt_GetWidthW(witxt,1);
				valy = 15;

				SC_Fnt_WriteW(val * 0.5f,valy,witxt,1,0xffffffff);

			}//if (i)

			break;

		case SC_NET_MES_SERVER_RECOVER_TIME:


			if (info->param2){
					info->fval1 = 0.1f;
			}
			else{
				// killed
				if (gMission_started){

						for (i=0;i<abl_lists;i++)
							if (info->param1==abl_list[i]){
								abl_lists--;
								abl_list[i] = abl_list[abl_lists];
								break;
							}

						if (i<abl_lists){
							info->fval1 = 0.1f;
						}
						else{
							if (gNextRecover>GetRecovLimitTime()) info->fval1 = gNextRecover;
								else info->fval1 = gNextRecover + GetRecovTime();
						}
				}
				else info->fval1 = 3.0f;

			}

			break;

		case SC_NET_MES_SERVER_RECOVER_PLACE:

			precov = (s_SC_MP_Recover*)info->param2;

			i = SC_MP_SRV_GetBestDMrecov(gRec[info->param1],gRecs[info->param1],gRecTimer[info->param1],NORECOV_TIME);

			gRecTimer[info->param1][i] = NORECOV_TIME;
			*precov = gRec[info->param1][i];

			break;


		case SC_NET_MES_SERVER_KILL:

			for (i=0;i<2;i++){
				pl_id = SC_MP_GetPlofHandle(gFlagOnPlayer_handle[i]);

				if (info->param1==pl_id){
					// killed player with flag

					gInfo[i] = INFO_FL_DROPPED;

					SC_P_GetPos(pl_id,&vec);
					vec.z += 0.6f;
					gOnGroundNetID[i] = SC_Item_Create(145+i,&vec);

					gOnGroundTimer[i] = ONGROUND_MAXTIME;

					gFlagPhase[i] = FLAG_PH_ONGROUND;
					gFlagOnPlayer_handle[i] = 0;

				}// if (info->param1==pl_id)
			}// for (i)

			// Killstreak tracking
			if (info->param2){  // param2 = killer (can be 0 for suicide/environment)
				dword killer_handle = SC_MP_GetHandleofPl(info->param2);
				dword slot = GetStreakSlot(killer_handle);
				gKillstreaks[slot]++;
				CheckKillstreak(killer_handle, gKillstreaks[slot]);
			}

			// Reset killstreak for dead player
			{
				dword dead_handle = SC_MP_GetHandleofPl(info->param1);
				dword slot = GetStreakSlot(dead_handle);
				gKillstreaks[slot] = 0;

				// BUDDY SYSTEM: Notify partner about death
				NotifyBuddyOfDeath(dead_handle);
			}

			Check_ABL(info->param1);

			break;// SC_NET_MES_SERVER_KILL

		case SC_NET_MES_RESTARTMAP:

			CLEAR(gSidePoints);
			UpdateSidePoints();

			gMission_afterstart_time = 0.0f;
			gMission_starting_timer = 0.0f;

			gTime = 0;

			SC_MP_SetInstantRecovery(TRUE);

			if (gMission_started){
				gMission_started = FALSE;
				SC_sgi(GVAR_GAMERUNS,gMission_started);
			}

			SC_MP_SRV_ClearPlsStats();

			// Reset killstreaks
			CLEAR(gKillstreaks);
			SC_sgi(GVAR_KILLSTREAK_PLAYER, 0);

			// Reset buddy pairs
			CLEAR(gBuddyPairs);
			gBuddyPairCount = 0;

			break;// SC_NET_MES_RESTARTMAP

		case SC_NET_MES_RULESCHANGED:
			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;
			break;

	}// switch(info->message)


	return 1;

}// int ScriptMain(void)
