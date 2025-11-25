//#define _TEST

/*
	Eric multiplayer script - ATG - NVA base
*/

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\!max_defs_mp.h>

#define NORECOV_TIME	3.0f		// disable time of recoverplace after recovering someone there

#define REC_MAX			64

#ifdef US_PLACING
	#define COOP_SIDE			SC_P_SIDE_US
	#define COOP_SIDE_INDEX		0
	#define OPP_SIDE			SC_P_SIDE_VC
	#define OPP_SIDE_INDEX		1
	#define GVAR_SIDE_COOP_POINTS			500
	#define GVAR_SIDE_OPP_POINTS			501
#else
	#define COOP_SIDE			SC_P_SIDE_VC
	#define COOP_SIDE_INDEX		1
	#define OPP_SIDE			SC_P_SIDE_US
	#define OPP_SIDE_INDEX		0
	#define GVAR_SIDE_COOP_POINTS			501
	#define GVAR_SIDE_OPP_POINTS			500
#endif

#define GVAR_MISSIONTIME				520
#define GVAR_MISSIONTIME_UPDATE			521

#define GVAR_BOMBPLAYER					530

#define BOMB_TIMER_UPDATE			5.0f
#define BOMB_AFTER_EXPLODE_TIMER	5.0f

dword gRecs[2] = {0,0};
s_SC_MP_Recover gRec[2][REC_MAX];
float gRecTimer[2][REC_MAX];

//c_Vector3 gBombWorldPos;

int gSidePoints[2] = {0,0};

int gCLN_SidePoints[2];

//void *gC4nod;

dword gBombStatus[BOMBSCOUNT]; // !!!!!!!!!!!!!
float gBombTimer[BOMBSCOUNT];
float gAfterExplodeTimer[BOMBSCOUNT];

float gMissionTime = 0;
float gMissionTime_update = 0;

float gCLN_MissionTime = 0;
dword gCLN_MissionTimePrevID = 0;

float gUpdate_BombTimer[BOMBSCOUNT];
float gRecv_BombTimer[BOMBSCOUNT];

float gCLN_BombTimer[BOMBSCOUNT];
dword gCLN_BombStatus[BOMBSCOUNT];

float gStartTimer;
float gRestartTimer;
float gShowTimer;
float setBombPlayer;

BOOL gInstantRecover = FALSE;
BOOL usExploded;
BOOL scoreUpdated = FALSE;
BOOL setBomb = FALSE;
BOOL warningSound = FALSE;
BOOL showInfoBomb = FALSE;

dword gEndRule;
dword gEndValue;
float gTime;

/*#if _GE_VERSION_ >= 138
dword g_FPV_BombZone = 0;
#endif*/


BOOL SRV_CheckEndRule(float time){
	int i;

	switch(gEndRule){
		case SC_MP_ENDRULE_TIME:
			
			for (i=0; i<BOMBSCOUNT; i++) if (gBombStatus[i]!=BOMB_STATUS_STARTING) continue;
			if (i <= BOMBSCOUNT) {	//nejaka neni starting
				gTime += time;
				SC_MP_EndRule_SetTimeLeft(gTime, TRUE);
			} else {
				SC_MP_EndRule_SetTimeLeft(gTime, FALSE);
			}

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

void UpdateSidePoints(void){
	SC_sgi(GVAR_SIDE_COOP_POINTS,gSidePoints[COOP_SIDE_INDEX]);
	SC_sgi(GVAR_SIDE_OPP_POINTS,gSidePoints[OPP_SIDE_INDEX]);
}// void UpdateSidePoints(void)


void SRV_CheckTimer(float time){
	int i,k;

	for (i=0; i<BOMBSCOUNT; i++) {
		if (gBombStatus[i]==BOMB_STATUS_ACTIVE){

			gBombTimer[i] -= time;

			if (gBombTimer[i]<=0.0f){
				// explosion
				// SC_DoExplosion(&gBombWorldPos,SC_EXPL_TYPE_MORTAR);
				gBombStatus[i] = BOMB_STATUS_EXPLODING;
				SC_sgi(GVAR_BOMBSTATUS__+i*2,gBombStatus[i]);	
				gAfterExplodeTimer[i] = BOMB_AFTER_EXPLODE_TIMER;
				for (k=0; k<BOMBSCOUNT; k++) {
					if ((SC_ggi(GVAR_BOMBSTATUS__+k*2) != BOMB_STATUS_EXPLODING) && (SC_ggi(GVAR_BOMBSTATUS__+k*2) != BOMB_STATUS_EXPLODED)) {
						if (!scoreUpdated) {
							gSidePoints[COOP_SIDE_INDEX]++;
							UpdateSidePoints();
							scoreUpdated = TRUE;
						}
					}
				}

			}
			else{
				gUpdate_BombTimer[i] -= time;
				if (gUpdate_BombTimer[i]<=0.0f){
					gUpdate_BombTimer[i] = BOMB_TIMER_UPDATE;
					SC_sgf(GVAR_BOMBSTIME__+i*2,gBombTimer[i]);
				}
			}

		}// if (gBombStatus==BOMB_STATUS_ACTIVE)
	}

}// void SRV_CheckTimer(float time)


void SRV_InstantRecover(BOOL valid){
	gInstantRecover = valid;
	SC_MP_SetInstantRecovery(valid);
}// void SRV_InstantRecover(BOOL valid)

void SRV_UpdateMissionTime(float time){

	gMissionTime_update -= time;
	if (gMissionTime_update<0.0f){

		gMissionTime_update = 10.0f;

		SC_sgf(GVAR_MISSIONTIME,gMissionTime);
		SC_sgi(GVAR_MISSIONTIME_UPDATE,SC_ggi(GVAR_MISSIONTIME_UPDATE)+1);		
	}// if (gMissionTime_update<0.0f)
}



void Check_ABL(void){
	int val;
	dword side,nr_to_change;
	s_SC_P_getinfo info;
	s_SC_MP_EnumPlayers enum_pl[64];
	dword i,j,k;


	if (!SC_MP_SRV_GetAutoTeamBalance()) return;

	val = SC_MP_SRV_GetTeamsNrDifference(TRUE);

	if ((val<3)&&(val>-3)) return;	// no big difference

	if (val>0){
		side = 0;
		nr_to_change = val/2;
	}
	else{
		side = 1;
		nr_to_change = -val/2;
	}

	// find nr_to_change players of beste players of side 0
	j = 64;

	if (SC_MP_EnumPlayers(enum_pl,&j,side)){				

		if (!j) return;
		
		while(nr_to_change!=0){

			k = rand()%j;
			i = k;

			while(
				(enum_pl[i].id==0)
				||(enum_pl[i].status==SC_MP_P_STATUS_NOTINGAME)){

				i++;
				if (i==j) i = 0;
				if (i==k) return;	// no valid found
			}						

			SC_MP_SRV_P_SetSideClass(enum_pl[i].id,1-side,1 + 20*(1-side));
			enum_pl[i].id = 0;

			nr_to_change--;

		}// while(nr_to_change!=0)
							
	}// if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL))



}// void Check_ABL(dword pl_handle)




int ScriptMain(s_SC_NET_info *info){
	char					txt[32];
	char					*p_txt;
	ushort					wtxt[128],wtxt1[64],wtxt2[64];
	dword					i,j,k,side,text_id;
	dword					pl_id, pl_id_bomb;
	s_SC_MP_Recover			*precov;
	s_SC_MP_hud				hudinfo;
	float					val, valy;
	void					*nod;
	s_SC_MP_EnumPlayers		enum_pl[64];
	BOOL					valid[2],active;
	s_SC_HUD_MP_icon		icon[10];
	s_SC_MP_SRV_settings	SRVset;
	s_SC_MP_SRV_AtgSettings atgset;
	s_SC_P_getinfo			plinfo;
	s_SC_P_Create			plcreate;
/*#if _GE_VERSION_ >= 138
	s_SC_FpvMapSign fpv_list[2];
#endif*/

	switch(info->message){
		
		case SC_NET_MES_SERVER_TICK:	

			if (SRV_CheckEndRule(info->elapsed_time)) break;

			for (j=0;j<2;j++)
				for (i=0;i<gRecs[j];i++)
					gRecTimer[j][i] -= info->elapsed_time;

			CLEAR(valid);			
			j = 64;

			if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)){				

				if ((j==0)&&((gSidePoints[0]+gSidePoints[1])!=0)){
					gSidePoints[0] = 0;
					gSidePoints[1] = 0;
					UpdateSidePoints();
				}// if ((side[0]+side[1])==0)

				for (i=0;i<j;i++)
					if (enum_pl[i].status==SC_MP_P_STATUS_INGAME) valid[enum_pl[i].side] = TRUE;
#ifdef _TEST
				valid[0] = TRUE; //jenom na test
				valid[1] = TRUE; //jenom na test
#endif
					
			}// if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL))

			gStartTimer += info->elapsed_time;

			if (gMissionTime>0){	//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				gMissionTime -= info->elapsed_time;
				SRV_UpdateMissionTime(info->elapsed_time);

				if (gMissionTime<0.0f){
					for (i=0; i<BOMBSCOUNT; i++) {
						gBombStatus[i] = BOMB_STATUS_TIMEOUT;
						SC_sgi(GVAR_BOMBSTATUS__+i*2,gBombStatus[i]);
						gAfterExplodeTimer[i] = BOMB_AFTER_EXPLODE_TIMER;
					}
					if (!scoreUpdated) {
						gSidePoints[OPP_SIDE_INDEX]++;
						UpdateSidePoints();
						scoreUpdated = TRUE;
					}
				}// if (gMissionTime<0.0f)

			}// gMissionTime

			if (setBombPlayer > 0.0) {
				setBombPlayer -= info->elapsed_time;
				if (setBombPlayer <= 0.0) {
					j = 64;

					if (SC_MP_EnumPlayers(enum_pl,&j,COOP_SIDE)) {
						if (j) {
							k = rand()%j;
							SC_sgi(GVAR_BOMBPLAYER, SC_MP_GetHandleofPl(enum_pl[k].id));
						}
					}
				}
			}

			SRV_InstantRecover(FALSE);
			for (i=0; i<BOMBSCOUNT; i++) {
				j = SC_ggi(GVAR_BOMBSTATUS__+i*2);
				
				switch(gBombStatus[i]){

					case BOMB_STATUS_STARTING:					

							if (i==0) gRestartTimer += info->elapsed_time;	//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

							if ((valid[0])&&(valid[1])) {

								if (gRestartTimer>10.0f) {
									Check_ABL();
									SC_MP_SRV_InitGameAfterInactive();
									SC_MP_RestartMission();
									gRestartTimer = 0.0f;
									scoreUpdated = FALSE;
								} else {
									gBombStatus[i] = BOMB_STATUS_INACTIVE;
									SC_sgi(GVAR_BOMBSTATUS__+i*2,BOMB_STATUS_INACTIVE);
									gStartTimer = 0.0f;

									SC_MP_SRV_GetAtgSettings(&atgset);

									if (atgset.ATG_round_time>29.0f)
										gMissionTime = atgset.ATG_round_time;
									else
										gMissionTime = 240.0f;

									SRV_UpdateMissionTime(1000);

									setBombPlayer = 0.5;
								}

							}// if ((valid[0])&&(valid[1]))


							SRV_InstantRecover(TRUE);						

							break;// BOMB_STATUS_STARTING
							
					case BOMB_STATUS_DEFUSED:
						if (!scoreUpdated) {
							gAfterExplodeTimer[i] = BOMB_AFTER_EXPLODE_TIMER;
							gSidePoints[OPP_SIDE_INDEX]++;
							UpdateSidePoints();
							SC_sgi(GVAR_BOMBPLAYER, 0);
							scoreUpdated = TRUE;
						}
						
					case BOMB_STATUS_EXPLODED:
					case BOMB_STATUS_US_KILLED:
					case BOMB_STATUS_VC_KILLED:
					case BOMB_STATUS_DRAW:
					case BOMB_STATUS_TIMEOUT:
							
							if (gAfterExplodeTimer[i] >= 0.0) gAfterExplodeTimer[i] -= info->elapsed_time;	//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#ifdef ONLYONE
							if (gAfterExplodeTimer[i] < 0.0f) {
#else
							for (k=0; k<BOMBSCOUNT; k++) 
								if ((SC_ggi(GVAR_BOMBSTATUS__+k*2) != BOMB_STATUS_EXPLODED) || (gAfterExplodeTimer[k] >= 0.0f)) break;

							if (k >= BOMBSCOUNT) {
#endif
								Check_ABL();
								SC_MP_RestartMission();
								for (k=0; k<BOMBSCOUNT; k++) {
									gBombStatus[k] = BOMB_STATUS_STARTING;
									SC_sgi(GVAR_BOMBSTATUS__+k*2,BOMB_STATUS_STARTING);
								}
								SC_sgi(GVAR_BOMBPLAYER, 0);
								gRestartTimer = 0.0f;
								//gShowTimer = 0.0f;
								setBombPlayer = 0.0f;
								showInfoBomb = FALSE;
								setBomb = FALSE;
								scoreUpdated = FALSE;
								warningSound = FALSE;
							}// if (gAfterExplodeTimer<=0.0f)
							else{
								if (j!=gBombStatus[i]) SC_sgi(GVAR_BOMBSTATUS__+i*2,gBombStatus[i]);
							}

							break;

					default:
							if ((gStartTimer>5.0f) && ((gBombStatus[i]==BOMB_STATUS_INACTIVE) || ((gBombStatus[i]==BOMB_STATUS_ACTIVE) && (gBombTimer[i] > BOMB_AFTER_EXPLODE_TIMER - 1.0)))){
								if ((!valid[0])&&(!valid[1])){
									// draw																		
									gBombStatus[i] = BOMB_STATUS_DRAW;
									SC_sgi(GVAR_BOMBSTATUS__+i*2,gBombStatus[i]);
									gAfterExplodeTimer[i] = BOMB_AFTER_EXPLODE_TIMER;								
									break;
								}

								if (!valid[0]) {
									gBombStatus[i] = BOMB_STATUS_US_KILLED;
									SC_sgi(GVAR_BOMBSTATUS__+i*2,gBombStatus[i]);
									gAfterExplodeTimer[i] = BOMB_AFTER_EXPLODE_TIMER;
									if (!scoreUpdated) {
										gSidePoints[1]++;
										UpdateSidePoints();
										scoreUpdated = TRUE;
									}
									break;
								}

								if (!valid[1]) {
									gBombStatus[i] = BOMB_STATUS_VC_KILLED;
									SC_sgi(GVAR_BOMBSTATUS__+i*2,gBombStatus[i]);
									gAfterExplodeTimer[i] = BOMB_AFTER_EXPLODE_TIMER;
									if (!scoreUpdated) {
										gSidePoints[0]++;
										UpdateSidePoints();
										scoreUpdated = TRUE;
									}
									break;
								}

							}// if (gStartTimer>5.0f) ...

							if (gBombStatus[i] != j){
								gBombStatus[i] = j;
								if (gBombStatus[i]==BOMB_STATUS_ACTIVE){
									gBombTimer[i] = BOMB_TIME[i];
									gUpdate_BombTimer[i] = 0.0f;
								}
							}					
						break;

				}// switch(gBombStatus)
			}

						
			SRV_CheckTimer(info->elapsed_time);
			
			break;

		case SC_NET_MES_CLIENT_TICK:

			gCLN_SidePoints[COOP_SIDE_INDEX] = SC_ggi(GVAR_SIDE_COOP_POINTS);
			gCLN_SidePoints[OPP_SIDE_INDEX] = SC_ggi(GVAR_SIDE_OPP_POINTS);

			SC_MP_SetSideStats(COOP_SIDE_INDEX,0,gCLN_SidePoints[COOP_SIDE_INDEX]);
			SC_MP_SetSideStats(OPP_SIDE_INDEX,0,gCLN_SidePoints[OPP_SIDE_INDEX]);

			if (gCLN_MissionTimePrevID!= SC_ggi(GVAR_MISSIONTIME_UPDATE)){
				gCLN_MissionTimePrevID = SC_ggi(GVAR_MISSIONTIME_UPDATE);
				gCLN_MissionTime = SC_ggf(GVAR_MISSIONTIME);
			}
			else{
				gCLN_MissionTime -= info->elapsed_time;
			}


			for (i=0;i<2;i++){
				icon[i].color = 0xbbffffff;				
				icon[i].type = SC_HUD_MP_ICON_TYPE_NUMBER;
				icon[i].icon_id = 3*i;
				icon[i].value = gCLN_SidePoints[i];
			}

			for (j=0; j<BOMBSCOUNT; j++) 
				gCLN_BombStatus[j] = SC_ggi(GVAR_BOMBSTATUS__+j*2);

			i = 2;

			for (j=0; j<BOMBSCOUNT; j++) {
				if ((gCLN_MissionTime>0.0f) 
					&&((gCLN_BombStatus[j]==BOMB_STATUS_INACTIVE)||(gCLN_BombStatus[j]==BOMB_STATUS_ACTIVE)||(gCLN_BombStatus[j]==BOMB_STATUS_PLACING))
					) {
					icon[i].color = 0xbbffffff;
					icon[i].icon_id = 6;
					icon[i].value = (int)(gCLN_MissionTime+0.99f);					
					icon[i].type = SC_HUD_MP_ICON_TYPE_TIME;
					i++;
					break;
				}
			}

			if (gShowTimer > 0) {
				gShowTimer -= info->elapsed_time;
				text_id=1077+COOP_SIDE_INDEX;
				SC_GetScreenRes(&val,NULL);
				val -= SC_Fnt_GetWidthW(SC_Wtxt(text_id),1);
				SC_Fnt_WriteW(val * 0.5f,15,SC_Wtxt(text_id),1,0xffffffff);
			}

			if (showInfoBomb) {
				//showInfoBomb -= info->elapsed_time;

				pl_id = SC_PC_Get();
				pl_id_bomb = SC_ggi(GVAR_BOMBPLAYER);
				if ((pl_id != 0) && (pl_id_bomb != 0)) {
					SC_P_GetInfo(pl_id,&plinfo);
					if (plinfo.side == COOP_SIDE) {
						//SC_GetScreenRes(&val,&valy);

						SC_P_GetWeapons(pl_id,&plcreate);
						if (plcreate.weap_slot7 == 55) text_id = 2; else text_id = 1;

						if (text_id == 1) {
							SC_AnsiToUni("Player %s has the bomb.",wtxt1);
							p_txt = SC_P_GetName(SC_MP_GetPlofHandle(pl_id_bomb));

							if (p_txt != NULL) {
								SC_AnsiToUni(p_txt, wtxt2);
								swprintf(wtxt, wtxt1, wtxt2);
								SC_GameInfoW(wtxt);
								showInfoBomb = FALSE;
							}
						} else {
							SC_AnsiToUni("You have the bomb.", wtxt);
							SC_GameInfoW(wtxt);
							showInfoBomb = FALSE;
						}
					}
				}
			}
			
			for (j=0; j<BOMBSCOUNT; j++) {
				switch(gCLN_BombStatus[j]){

					case BOMB_STATUS_STARTING:
							active = FALSE;
							setBomb = FALSE;
							gRecv_BombTimer[j] = gCLN_BombTimer[j] = 0.0f;
							break;
					case BOMB_STATUS_INACTIVE:
							active = FALSE;
							gRecv_BombTimer[j] = gCLN_BombTimer[j] = 0.0f;
							pl_id_bomb = (dword)SC_ggi(GVAR_BOMBPLAYER);
							if ((!setBomb) && (pl_id_bomb != 0)) {
								//k = 64;
								//SC_MP_EnumPlayers(enum_pl,&k,0);
								pl_id = SC_PC_Get();
								if (pl_id != 0) {
									if (SC_MP_GetHandleofPl(pl_id) == pl_id_bomb)
										SC_P_ChangeWeapon(pl_id,6,55);
									else
										SC_P_ChangeWeapon(pl_id,6,0);
								
									setBomb = TRUE;
									showInfoBomb = TRUE;
								}
							}
							break;
					case BOMB_STATUS_EXPLODED:				
							active = FALSE;
#ifdef ONLYONE
							usExploded = TRUE;
#else
							for (k=0; k<BOMBSCOUNT; k++) 
								if (SC_ggi(GVAR_BOMBSTATUS__+k*2) != BOMB_STATUS_EXPLODED) break;

							if (k >= BOMBSCOUNT) usExploded = TRUE;
#endif
							gRecv_BombTimer[j] = gCLN_BombTimer[j] = 0.0f;
							break;

					case BOMB_STATUS_ACTIVE:
						if (!warningSound) {
							pl_id = SC_PC_Get();
							if (pl_id != 0) {
								SC_P_GetInfo(pl_id,&plinfo);
								if (plinfo.side == OPP_SIDE) {
									warningSound = TRUE;
									SC_SND_PlaySound2D(10425);
								}
							}
						}

						val = SC_ggf(GVAR_BOMBSTIME__+j*2);
						if (val!=gRecv_BombTimer[j]){
							gCLN_BombTimer[j] = val;
							gRecv_BombTimer[j] = val;
						}

						gCLN_BombTimer[j] -= info->elapsed_time;

						icon[i].color = 0xffffffff;
						icon[i].icon_id = 10;
						if (gCLN_BombTimer[j] > 0) icon[i].value = (int)(gCLN_BombTimer[j]+0.99f);
							else icon[i].value = 0;
						icon[i].type = SC_HUD_MP_ICON_TYPE_TIME;
						i++;

						active = TRUE;					
						break;
					default:
						active = FALSE;
						break;

				}// switch(gCLN_BombStatus)
			}

			//SC_DUMMY_Set_DoNotRenHier2(gC4nod,!active);
			
			SC_MP_SetIconHUD(icon,i);

			break;// SC_NET_MES_CLIENT_TICK


		case SC_NET_MES_LEVELPREINIT:
			SC_sgi(GVAR_MP_MISSIONTYPE,GVAR_MP_MISSIONTYPE_ATG);
			SC_sgi(GVAR_MP_MISSIONSUBTYPE,COOP_SIDE_INDEX+1);

			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;

			SC_MP_EnableBotsFromScene(FALSE);

			SC_MP_EnableC4weapon(TRUE);
			
			usExploded = FALSE;
			gShowTimer = 0.0f;

			break;// SC_NET_MES_LEVELPREINIT

		case SC_NET_MES_LEVELINIT:

		/*#if _GE_VERSION_ >= 138
			g_FPV_BombZone = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_bombingzone.BES");
		#endif*/

			SC_MP_SRV_SetForceSide(0xffffffff);
			SC_MP_SetChooseValidSides(3);

			SC_MP_SRV_SetClassLimit(18,0);
			SC_MP_SRV_SetClassLimit(19,0);
			SC_MP_SRV_SetClassLimit(39,0);

			SC_MP_GetSRVsettings(&SRVset);

			for (i = 0; i < 6; i++)	{
				if (CLASS_LIMIT_US[i] == -2) SC_MP_SRV_SetClassLimit(i+1, SRVset.atg_class_limit[i]); else SC_MP_SRV_SetClassLimit(i+1, CLASS_LIMIT_US[i]);
				if (CLASS_LIMIT_VC[i] == -2) SC_MP_SRV_SetClassLimit(i+21,SRVset.atg_class_limit[i]); else SC_MP_SRV_SetClassLimit(i+21,CLASS_LIMIT_VC[i]);
			}// for (i)

			CLEAR(hudinfo);
			hudinfo.title = 1072;
			hudinfo.sort_by[0] = SC_HUD_MP_SORTBY_KILLS;
			hudinfo.sort_by[1] = SC_HUD_MP_SORTBY_DEATHS | SC_HUD_MP_SORT_DOWNUP;
			hudinfo.sort_by[2] = SC_HUD_MP_SORTBY_PINGS | SC_HUD_MP_SORT_DOWNUP;

			hudinfo.pl_mask = SC_HUD_MP_PL_MASK_CLASS | SC_HUD_MP_PL_MASK_KILLS | SC_HUD_MP_PL_MASK_DEATHS;
			hudinfo.use_sides = TRUE;
			hudinfo.side_name[0] = 1010;
			hudinfo.side_color[0] = 0x440000ff;
			hudinfo.side_name[1] = 1011;
			hudinfo.side_color[1] = 0x44ff0000;

			hudinfo.side_mask = SC_HUD_MP_SIDE_MASK_POINTS;
			
			SC_MP_HUD_SetTabInfo(&hudinfo);					

			for (i=0; i<BOMBSCOUNT; i++) {
				SC_sgi(GVAR_BOMBSTATUS__+i*2,BOMB_STATUS_STARTING);
				SC_MP_Gvar_SetSynchro(GVAR_BOMBSTATUS__+i*2);
			}
			gRestartTimer = 0.0f;
			setBombPlayer = 0.0f;
			showInfoBomb = FALSE;
			setBomb = FALSE;
			warningSound = FALSE;
			scoreUpdated = FALSE;

			//gC4nod = SC_NOD_Get(NULL,"c4");
			/*if (gC4nod){
				SC_NOD_GetWorldPos(gC4nod,&gBombWorldPos);
				gBombWorldPos.z += 0.2f;

#if _GE_VERSION_ >= 138
				fpv_list[0].id = g_FPV_BombZone;
				fpv_list[0].color = 0xffffffff;
				fpv_list[0].pos = gBombWorldPos;
				fpv_list[0].scale = 1.0f;				

				SC_MP_FpvMapSign_Set(1,fpv_list);
#endif

			}
			else {
				SC_message("c4 not found");
				CLEAR(gBombWorldPos);
			}*/


			SC_MP_AllowStPwD(TRUE);
			SC_MP_AllowFriendlyFireOFF(TRUE);
			SC_MP_SetItemsNoDisappear(TRUE);

			if (info->param2){

				if (info->param1){
					// it's server		
					SC_MP_Gvar_SetSynchro(GVAR_BOMBPLAYER);

					SC_MP_Gvar_SetSynchro(GVAR_SIDE_COOP_POINTS);
					SC_MP_Gvar_SetSynchro(GVAR_SIDE_OPP_POINTS);

					for (i=0; i<BOMBSCOUNT; i++)
						SC_MP_Gvar_SetSynchro(GVAR_BOMBSTIME__+i*2);
					
					SC_MP_Gvar_SetSynchro(GVAR_MISSIONTIME);	
					SC_MP_Gvar_SetSynchro(GVAR_MISSIONTIME_UPDATE);

					
					UpdateSidePoints();
					
					CLEAR(gRecs);
				

					for (i=0;i<REC_MAX;i++){		
						sprintf(txt,REC_WPNAME_US,i);			
						if (SC_NET_FillRecover(&gRec[0][gRecs[0]],txt)) gRecs[0]++;					
					}					

#if _GE_VERSION_ >= 133
					i = REC_MAX - gRecs[0];
					SC_MP_GetRecovers(SC_MP_RESPAWN_ATG_US,&gRec[0][gRecs[0]],&i);
					gRecs[0] += i;
#endif

					SC_Log(3,"ATG UsBomb respawns us: %d",gRecs[0]);


					if (gRecs[0]==0) SC_message("no US recover place defined!");

					for (i=0;i<REC_MAX;i++){		
						sprintf(txt,REC_WPNAME_VC,i);			
						if (SC_NET_FillRecover(&gRec[1][gRecs[1]],txt)) gRecs[1]++;
					}					

#if _GE_VERSION_ >= 133
					i = REC_MAX - gRecs[1];
					SC_MP_GetRecovers(SC_MP_RESPAWN_ATG_VC,&gRec[1][gRecs[1]],&i);
					gRecs[1] += i;
#endif

					SC_Log(3,"ATG UsBomb respawns vc: %d",gRecs[0]);

					if (gRecs[1]==0) SC_message("no VC recover place defined!");					

					CLEAR(gRecTimer);

				}// if (info->param1)

			}//if (info->param2)

			SC_sgi(GVAR_BOMBPLAYER, 0);

			break;// SC_NET_MES_LEVELINIT


		case SC_NET_MES_RENDERHUD:
			for (i=0; i<BOMBSCOUNT; i++) {
				switch(SC_ggi(GVAR_BOMBSTATUS__+i*2)) {
				//switch (gBombStatus) {
					case BOMB_STATUS_STARTING:	text_id = 1076;break;													
					case BOMB_STATUS_EXPLODED:
#ifdef ONLYONE
						text_id = 1077+COOP_SIDE_INDEX;
#else
						for (j=0; j<BOMBSCOUNT; j++) 
							if (SC_ggi(GVAR_BOMBSTATUS__+j*2) != BOMB_STATUS_EXPLODED) break;
						if (j >= BOMBSCOUNT) text_id = 1077+COOP_SIDE_INDEX; else text_id=0;
#endif
						break;
					case BOMB_STATUS_DEFUSED:	text_id = 9999;break;
					case BOMB_STATUS_US_KILLED:	text_id = 1079;break;
					case BOMB_STATUS_VC_KILLED:	text_id = 1080;break;
					case BOMB_STATUS_DRAW:		text_id = 1082;break;				
					case BOMB_STATUS_TIMEOUT:	text_id = 451;break;				
					default:					text_id = 0;break;
				}

				if (text_id) {
					SC_GetScreenRes(&val,NULL);
					
					//if ((gBombStatus==BOMB_STATUS_EXPLODING) || (gBombStatus==BOMB_STATUS_EXPLODED)) valY = 100; else valY = 15;
					if (text_id == 9999) {
						if (COOP_SIDE_INDEX == 0) {
							val -= SC_Fnt_GetWidth("Vietcong win. Bomb defused.",1);
							SC_Fnt_Write(val * 0.5f,15,"Vietcong win. Bomb defused.",1,0xffffffff);
						} else {
							val -= SC_Fnt_GetWidth("US Army win. Bomb defused.",1);
							SC_Fnt_Write(val * 0.5f,15,"US Army win. Bomb defused.",1,0xffffffff);
						}
					} else {
						val -= SC_Fnt_GetWidthW(SC_Wtxt(text_id),1);
						SC_Fnt_WriteW(val * 0.5f,15,SC_Wtxt(text_id),1,0xffffffff);
					}
				} else {
					if (usExploded == TRUE) {
						usExploded = FALSE;
						gShowTimer = SHOW_TIME;
					}
				}
			}
			
			break;

		case SC_NET_MES_SERVER_RECOVER_TIME:

			SC_MP_SRV_GetAtgSettings(&atgset);
			for (i=0; i<BOMBSCOUNT; i++) {
				if (((gBombStatus[i]==BOMB_STATUS_INACTIVE)||(gBombStatus[i]==BOMB_STATUS_ACTIVE))&&((gMissionTime+10.0f)<atgset.ATG_round_time)){
					info->fval1 = SC_NET_SERVER_RECTIME_ENDOFROUND;
				} else if (info->param2){
						info->fval1 = 0.1f;
				} else {
					// killed
					if (gInstantRecover) info->fval1 = 2.0f;
						else info->fval1 = -1.0f;
				}
			}

			break;

		case SC_NET_MES_SERVER_RECOVER_PLACE:
			
			precov = (s_SC_MP_Recover*)info->param2;

			i = SC_MP_SRV_GetBestDMrecov(gRec[info->param1],gRecs[info->param1],gRecTimer[info->param1],NORECOV_TIME);
			
			gRecTimer[info->param1][i] = NORECOV_TIME;
			*precov = gRec[info->param1][i];
						
			break;
			

		case SC_NET_MES_SERVER_KILL:


			break;// SC_NET_MES_SERVER_KILL

		case SC_NET_MES_MESSAGE:

			if ((info->param1==0)/*&&(info->param2==0)*/){

				SC_P_GetInfo(SC_PC_Get(),&plinfo);

				if (plinfo.side == OPP_SIDE){				
					SC_sgi(GVAR_BOMBSTATUS__+info->param2*2,BOMB_STATUS_DEFUSED);
				} else {
#ifdef ONLYONE
					for (i=0; i<BOMBSCOUNT; i++) {
						if (i == info->param2)
							SC_sgi(GVAR_BOMBSTATUS__+i*2,BOMB_STATUS_ACTIVE);
						else 
							if (SC_ggi(GVAR_BOMBSTATUS__+i*2) <= BOMB_STATUS_INACTIVE)
								SC_sgi(GVAR_BOMBSTATUS__+i*2, BOMB_STATUS_OFF);		

					}
#else
					SC_sgi(GVAR_BOMBSTATUS__+info->param2*2,BOMB_STATUS_ACTIVE);
#endif
				}
						
			}// if ((info->param1==0)&&(info->param2==0))

			break;


		case SC_NET_MES_RESTARTMAP:
			showInfoBomb = FALSE;
			SC_sgi(GVAR_BOMBPLAYER, 0);
			for (i=0; i<BOMBSCOUNT; i++) {
				SC_sgi(GVAR_BOMBSTATUS__+i*2,BOMB_STATUS_STARTING);
				gBombStatus[i] = BOMB_STATUS_STARTING;
				gBombTimer[i] = 0.0f;
				gUpdate_BombTimer[i] = 0.0f;
				gRecv_BombTimer[i] = 0.0f;
				gAfterExplodeTimer[i] = 0.0f;
			}

			CLEAR(gSidePoints);			
			UpdateSidePoints();
			
			scoreUpdated = FALSE;

			gStartTimer = 0.0f;
			gRestartTimer = 0.0f;
			gShowTimer = 0.0f;
			setBombPlayer = 0.0f;
			
			setBomb = FALSE;
			warningSound = FALSE;

			gInstantRecover = TRUE;

			gTime = 0;

			SRV_InstantRecover(TRUE);	
			SC_MP_SRV_ClearPlsStats();

			SC_MP_SRV_InitGameAfterInactive();
			SC_MP_RecoverAllNoAiPlayers();			

			break;// SC_NET_MES_RESTARTMAP

		case SC_NET_MES_RULESCHANGED:			
			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;
			break;

					
	}// switch(info->message)
	

	return 1;

}// int ScriptMain(void)
