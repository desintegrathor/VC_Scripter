/*
	Eric multiplayer script - TT - TurnTable
*/

#include <inc\sc_MPglobal.h>


#define NORECOV_TIME					3.0f

// defines uf used global variables
#define GVAR_SIDE0POINTS				500
#define GVAR_SIDE1POINTS				501
#define GVAR_MAINPHASE					502
#define GVAR_GAMEPHASE					503
#define GVAR_MISSIONTIME				504
#define GVAR_MISSIONTIME_UPDATE			505
#define GVAR_LASTSCORES					506
#define GVAR_CURSTEP					507
#define GVAR_STEPS						508
#define GVAR_LASTWIN					509
#define GVAR_SCORING_PLAYER				510



#define STEP_MAX		6				// maximum of attacking steps
#define REC_MAX			32				// maximum of recovers around one flag


// values for gMission_phase
#define MISSION_PHASE_NOACTIVE			0
#define MISSION_PHASE_INGAME			1
#define MISSION_PHASE_WIN_ATTACKERS		2
#define MISSION_PHASE_WIN_DEFENDERS		3



dword gSteps = 0;				// number of steps
dword gRecs[2][STEP_MAX];		// 0-Attackers, 1-Defenders
s_SC_MP_Recover gRec[2][STEP_MAX][REC_MAX];
float gRecTimer[2][STEP_MAX][REC_MAX];

s_sphere gStepSwitch[STEP_MAX];	// switches to the next attack step

dword gEndRule;
dword gEndValue;
float gTime;
dword gSidePoints[2];
dword gCLN_SidePoints[2];
dword gCLN_gamephase;

dword gMainPhase = 0;
dword gAttackingSide = 0;
dword gCurStep = 0;
BOOL gMission_phase = MISSION_PHASE_NOACTIVE;
float gNoActiveTime = 0.0f;
float gPhaseTimer;

float gMissionTime_update = 10.0f;
float gMissionTime;
float gMissionTimeToBeat;

dword gCLN_MissionTimePrevID;
float gCLN_MissionTime;
dword gCLN_CurStep;
float gCLN_ShowInfo = 0.0f;
float gCLN_ShowStartInfo = 0.0f;
float gCLN_ShowWaitingInfo = 0.0f;

float gMission_starting_timer = 0.0f;
float gMission_afterstart_time = 0.0f;


float gNextRecover = 0.0f;

void *gFlagNod[STEP_MAX][3];
c_Vector3 gFlagPos[STEP_MAX];

dword abl_lists = 0;
dword abl_list[64];


#if _GE_VERSION_ >= 133
dword gRespawn_id[2][STEP_MAX] = {
	{0,SC_MP_RESPAWN_TT_ATT_1,SC_MP_RESPAWN_TT_ATT_2,SC_MP_RESPAWN_TT_ATT_3,SC_MP_RESPAWN_TT_ATT_4,SC_MP_RESPAWN_TT_ATT_5},
	{SC_MP_RESPAWN_TT_DEF_0,SC_MP_RESPAWN_TT_DEF_1,SC_MP_RESPAWN_TT_DEF_2,SC_MP_RESPAWN_TT_DEF_3,SC_MP_RESPAWN_TT_DEF_4,0}
};
#endif


#if _GE_VERSION_ >= 138
dword g_FPV_UsFlag = 0;
dword g_FPV_VcFlag = 0;
dword g_FPV_NeFlag = 0;
#endif


BOOL SRV_CheckEndRule(float time){
	// function that checks end rule, running on server only

	switch(gEndRule){
		case SC_MP_ENDRULE_TIME:

			// increase game time when the game is active only
			if (gMission_phase>MISSION_PHASE_NOACTIVE) gTime += time;

			// set time left to engine that will send it to clients time to time
			SC_MP_EndRule_SetTimeLeft(gTime,gMission_phase);

			if (gTime>gEndValue){
				// timelimit reached, load next map...
				SC_MP_LoadNextMap();
				return TRUE;
			}

			break;

		case SC_MP_ENDRULE_POINTS:

			if ((gSidePoints[0]>=gEndValue)||(gSidePoints[1]>=gEndValue)){
				// end rule points reached
				SC_MP_LoadNextMap();
				return TRUE;
			}

			break;

		default:			
			SC_message("EndRule unsupported: %d",gEndRule);
			break;

	}// switch(gEndRule)

	return FALSE;

}// void SRV_CheckEndRule(float time)


float GetRecovTime(void){
	// gets respawn time set by level.c, if not set (0) use default (30)
	//   every level using this TT script can have different respawn settings
	float val;
	s_SC_MP_SRV_AtgSettings set;

	SC_MP_SRV_GetAtgSettings(&set);

	if (set.tt_respawntime>1.0f){
		return set.tt_respawntime;
	}	

	val = SC_ggf(400);
	if (val==0) val = 30;
	return val;
}
	
float GetRecovLimitTime(void){
	// gets respawn time limit set by level.c
	float val;
	s_SC_MP_SRV_AtgSettings set;

	SC_MP_SRV_GetAtgSettings(&set);

	if (set.tt_respawntime>1.0f){
		val = set.tt_respawntime/3;
		if (val<5.0f) val = 5.0f;
		if (val>10.0f) val = 10.0f;
		return val;
	}	

	val = SC_ggf(401);
	if (val==0) val = 10;
	return val;
}

float GetTimeLimit(void){
	// gets game time limit set by level.c
	float val;
	s_SC_MP_SRV_AtgSettings set;

	SC_MP_SRV_GetAtgSettings(&set);

	if (set.tt_timelimit>59.0f){
		return set.tt_timelimit;
	}

	val = SC_ggf(402);
	if (val==0) val = 8*60;
	return val;
}


void UpdateSidePoints(void){
	// update global variables when some side scores
	SC_sgi(GVAR_SIDE0POINTS,gSidePoints[0]);
	SC_sgi(GVAR_SIDE1POINTS,gSidePoints[1]);
}// void UpdateSidePoints(void)


void SRV_UpdateMissionTime(float time){
	// check updating of mission time to clients

	gMissionTime_update -= time;
	if (gMissionTime_update<0.0f){

		gMissionTime_update = 10.0f;

		SC_sgf(GVAR_MISSIONTIME,gMissionTime);
		SC_sgi(GVAR_MISSIONTIME_UPDATE,SC_ggi(GVAR_MISSIONTIME_UPDATE)+1);		
	}// if (gMissionTime_update<0.0f)
}


void ResetMission(void){
	// reset mission, it's used when the round is ended

	gCurStep = gSteps-1;

	SC_sgi(GVAR_CURSTEP,gCurStep);

	if ((gMainPhase%2)==0)
		gMissionTime = GetTimeLimit();
	else 
		gMissionTime = gMissionTimeToBeat;

	gMissionTime_update = -1.0;					
	SRV_UpdateMissionTime(0.0f);	

}// void ResetMission(void)

dword GetAttackingSide(dword main_phase){
	// returns attacking side (0-US or 1-VC) depending on main_phase

	switch(main_phase%4){
		case 0:
		case 3:return 0;			
	}// switch(main_phase%4)

	return 1;

}// dword GetAttackingSide(dword main_phase)

void RoundEnd(void){
	// is called when round ends
	// depending on gMission_phase and gMainPhase chooses the next progress


	switch(gMission_phase){

		case MISSION_PHASE_WIN_DEFENDERS:
			gSidePoints[1-gAttackingSide]++;
			UpdateSidePoints();

			SC_sgi(GVAR_LASTSCORES,1-gAttackingSide);
			SC_sgi(GVAR_LASTWIN,1-gAttackingSide);			

			if (gMainPhase % 2) gMainPhase++;
				else gMainPhase+=2;
			
			break;

		case MISSION_PHASE_WIN_ATTACKERS:

			SC_sgi(GVAR_LASTWIN,gAttackingSide);

			if (gMainPhase % 2){
				gSidePoints[gAttackingSide]++;
				UpdateSidePoints();
				SC_sgi(GVAR_LASTSCORES,gAttackingSide);
			}
			else
				gMissionTimeToBeat = GetTimeLimit() - gMissionTime;

			gMainPhase++;

			break;

	}// switch(gMission_phase)

	SC_sgi(GVAR_MAINPHASE,gMainPhase);

	gAttackingSide = GetAttackingSide(gMainPhase);


	SC_sgi(GVAR_CURSTEP,STEP_MAX);

}// void RoundEnd(void)



void SetFlagStatus(dword attacking_side, dword cur_step){
	// sets flags visibility depending on current game status

	BOOL us,vc,ne;
	dword i,flags;
#if _GE_VERSION_ >= 138
	s_SC_FpvMapSign fpv_list[STEP_MAX];
#endif


	flags = 0;

	for (i=0;i<STEP_MAX;i++){

		us = FALSE;
		vc = FALSE;
		ne = FALSE;

		if ((i+1)==cur_step){

			switch(attacking_side){
				case 0:
					vc = TRUE;
					break;
				case 1:
					us = TRUE;
					break;
				case 2:
					ne = TRUE;
					break;

			}// switch(attacking_side)

		}
		else
		if (i<cur_step){
			ne = TRUE;
		}

		if (gFlagNod[i][0]) SC_DUMMY_Set_DoNotRenHier2(gFlagNod[i][0],!us);				
		if (gFlagNod[i][1]) SC_DUMMY_Set_DoNotRenHier2(gFlagNod[i][1],!vc);				
		if (gFlagNod[i][2]) SC_DUMMY_Set_DoNotRenHier2(gFlagNod[i][2],!ne);				


		fpv_list[flags].id = 0;
		if (us) fpv_list[flags].id = g_FPV_UsFlag;
		else
		if (vc) fpv_list[flags].id = g_FPV_VcFlag;
		else
		if (ne) fpv_list[flags].id = g_FPV_NeFlag;

		if (fpv_list[flags].id){
			fpv_list[flags].color = 0xffffffff;
			fpv_list[flags].pos = gFlagPos[i];
			fpv_list[flags].scale = 1.0f;				
			flags++;
		}


	}// for (i=0;i<STEP_MAX;i++)

	SC_MP_FpvMapSign_Set(flags,fpv_list);

}// void SetFlagStatus(dword attacking_side, dword cur_step)


void Check_ABL(dword pl_handle){
	// checking autobalance
	int val;
	dword to_change;
	s_SC_P_getinfo info;

	if (!SC_MP_SRV_GetAutoTeamBalance()) return;

	val = SC_MP_SRV_GetTeamsNrDifference(TRUE);

	if ((val<3)&&(val>-3)) return;	// no big difference

	SC_P_GetInfo(pl_handle,&info);	

	if ((info.side==0)&&(val>0)) to_change = 1;
	else
	if ((info.side==1)&&(val<0)) to_change = 0;
	else
		return;

	SC_MP_SRV_P_SetSideClass(pl_handle,to_change,1 + 20*to_change);

	if (abl_lists<64){
		abl_list[abl_lists] = pl_handle;
		abl_lists++;
	}

}// void Check_ABL(dword pl_handle)


void Check_ABL_Restart(void){
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



}// void Check_ABL_Restart(void)



void RecoverDeathDefenders(void){
#if _GE_VERSION_ >= 136
	s_SC_MP_EnumPlayers enum_pl[64];
	dword i,side,pls;

	side = 1-GetAttackingSide(SC_ggi(GVAR_MAINPHASE));

	pls = 64;

	if (SC_MP_EnumPlayers(enum_pl,&pls,side)){

		for (i=0;i<pls;i++)
			if (enum_pl[i].status==SC_MP_P_STATUS_INGAMEDEATH){
				SC_MP_RecoverPlayer(enum_pl[i].id);
			}

	}// if (SC_MP_EnumPlayers(enum_pl,&pls,side))

#endif
}// void RecoverDeathDefenders(void)



int ScriptMain(s_SC_NET_info *info){
	char txt[32];
	dword i,j,k,icons,pls;
	s_SC_MP_Recover *precov;
	s_SC_MP_hud hudinfo;
	s_SC_MP_EnumPlayers enum_pl[64];
	s_SC_MP_SRV_settings SRVset;
	char side_char;
	void *nod;
	BOOL side[2],in_middle;
	s_SC_HUD_MP_icon icon[3];
	c_Vector3 pos;
	ushort *witxt,wtxt[128],wtxt2[64];
	float val,valy;
	s_SC_P_getinfo plinfo;


	switch(info->message){
		
		case SC_NET_MES_SERVER_TICK:	
			// server tick, this part of the code is executed on server side only ( dedicated and no-dedicated too)

			if (SRV_CheckEndRule(info->elapsed_time)) break;

			
			side[0] = side[1] = FALSE;
			
			pls = 64;

			// enumerate players
			if (SC_MP_EnumPlayers(enum_pl,&pls,SC_MP_ENUMPLAYER_SIDE_ALL)){				

				// no players found, clear score
				if ((pls==0)&&((gSidePoints[0]+gSidePoints[1])!=0)){
					gSidePoints[0] = 0;
					gSidePoints[1] = 0;
					UpdateSidePoints();
				}// if ((side[0]+side[1])==0)
				

				// check if there are players of both sides
				for (i=0;i<pls;i++)
					if (enum_pl[i].status!=SC_MP_P_STATUS_NOTINGAME){
						
						if (enum_pl[i].side<2) side[enum_pl[i].side] = TRUE;
						
					}// if (enum_pl[i].status==SC_MP_P_STATUS_INGAME)

				gMission_starting_timer -= info->elapsed_time;

				if ((side[0])&&(side[1])){					

					SC_MP_SetInstantRecovery(FALSE);

					if (gMission_phase==MISSION_PHASE_NOACTIVE){												
						// start the game !
						gMission_phase = MISSION_PHASE_INGAME;										

						gMission_afterstart_time = 0.0f;
						SC_sgi(GVAR_GAMEPHASE,gMission_phase);
						ResetMission();						
						SC_MP_SRV_InitGameAfterInactive();

						if (gNoActiveTime>6.0f){
							SC_MP_RestartMission();							
							SC_MP_RecoverAllNoAiPlayers();
						}

						gMission_starting_timer = 8.0f;
					}
				}// if ((side[0])&&(side[1]))
				else{

					if (gMission_starting_timer<=0.0f){

						SC_MP_SetInstantRecovery(TRUE);

						if (gMission_phase>MISSION_PHASE_NOACTIVE){							
							// make the game inactive - no both sides are present
							gMission_phase = MISSION_PHASE_NOACTIVE;
							gMission_afterstart_time = 0.0f;
							SC_sgi(GVAR_GAMEPHASE,gMission_phase);
							Check_ABL_Restart();
							ResetMission();
						}

					}

				}// else if ((side[0])&&(side[1]))

			}// if (SC_MP_EnumPlayers(enum_pl,&pls,SC_MP_ENUMPLAYER_SIDE_ALL))
							
						
			
			// update timers for respawn points
			for (i=0;i<2;i++)
			for (j=0;j<gSteps;j++)
				for (k=0;k<gRecs[i][j];k++)
					gRecTimer[i][j][k] -= info->elapsed_time;


			gNextRecover -= info->elapsed_time;
			if (gNextRecover<0.0f) gNextRecover = GetRecovTime(); 

			switch(gMission_phase){

				case MISSION_PHASE_NOACTIVE:

						gNoActiveTime += info->elapsed_time;

						if (gMissionTime>-10.0f){
							gMissionTime = -10.0f;
							gMissionTime_update = -1.0;					
							SRV_UpdateMissionTime(0.0f);
						}

						break;

				case MISSION_PHASE_INGAME:
			
						gMission_afterstart_time += info->elapsed_time;

						gMissionTime -= info->elapsed_time;
						SRV_UpdateMissionTime(info->elapsed_time);

						if (gMissionTime<=0.0f){	
							// mission time left, defenders win
							gMission_phase = MISSION_PHASE_WIN_DEFENDERS;
							SC_sgi(GVAR_GAMEPHASE,gMission_phase);
							gPhaseTimer = 8.0f;
							RoundEnd();
						}
						else					
						if (gMission_afterstart_time>5.0f){
							// check for the next step_area ( next flags captured by attackers)
							
							if (gCurStep>0)
							for (i=0;i<pls;i++)
								if (((enum_pl[i].side==gAttackingSide)
									&&(enum_pl[i].status==SC_MP_P_STATUS_INGAME))){																		
										// it's attacker

										SC_P_GetPos(enum_pl[i].id,&pos);

										//for (j=0;j<gCurStep;j++)										
										for (j=gCurStep-1;j<gCurStep;j++)
											if (SC_IsNear3D(&pos,&gStepSwitch[j].pos,gStepSwitch[j].rad)){
												// some attacker is near to the flag
												if (j){								
													// it's not the last one
													gCurStep = j;
													SC_sgi(GVAR_SCORING_PLAYER,SC_MP_GetHandleofPl(enum_pl[i].id));
													SC_sgi(GVAR_CURSTEP,gCurStep);													
													RecoverDeathDefenders();
												}
												else{
													// mission done, attacker reaches the final flag																
													gMission_phase = MISSION_PHASE_WIN_ATTACKERS;
													SC_sgi(GVAR_SCORING_PLAYER,SC_MP_GetHandleofPl(enum_pl[i].id));
													SC_sgi(GVAR_GAMEPHASE,gMission_phase);													
													gPhaseTimer = 8.0f;
													RoundEnd();
												}
											}

									}

						}// if (gMission_afterstart_time>5.0f)

						break;// MISSION_PHASE_INGAME

					case MISSION_PHASE_WIN_DEFENDERS:
					case MISSION_PHASE_WIN_ATTACKERS:
						// short time at the end of the round

						gPhaseTimer -= info->elapsed_time;
						if (gPhaseTimer<0.0f){							
							gNoActiveTime = 0.0f;
							gMission_phase = MISSION_PHASE_NOACTIVE;
							SC_sgi(GVAR_GAMEPHASE,gMission_phase);
							Check_ABL_Restart();
							SC_MP_SetInstantRecovery(TRUE);
							SC_MP_RecoverAllNoAiPlayers();													
						}

						break;

			}// switch(gMission_phase)

			break;

		case SC_NET_MES_CLIENT_TICK:
			// client tick, this part is executed on client only ( including client on no-dedicated server)

			gCLN_ShowInfo -= info->elapsed_time;						
			if (gCLN_ShowStartInfo>0.0f) gCLN_ShowStartInfo -= info->elapsed_time;
			if (gCLN_ShowWaitingInfo>0.0f) gCLN_ShowWaitingInfo -= info->elapsed_time;
			

			// set flags rendering
			switch(SC_ggi(GVAR_GAMEPHASE)){
				case MISSION_PHASE_NOACTIVE:
					SetFlagStatus(SC_ggi(GVAR_STEPS)-1,2);
					break;
				case MISSION_PHASE_INGAME:
					
					if (gCLN_CurStep!=SC_ggi(GVAR_CURSTEP)){

						gCLN_CurStep = SC_ggi(GVAR_CURSTEP);						

						if ((gCLN_CurStep<(SC_ggi(GVAR_STEPS)-1))&&(gCLN_CurStep>0)){
							// set info about attackers reaching the flag
							gCLN_ShowInfo = 5.0f;	
							SC_SND_PlaySound2D(10425);							
						}
					}

					SetFlagStatus(GetAttackingSide(SC_ggi(GVAR_MAINPHASE)),gCLN_CurStep);

					break;
			}// switch(SC_ggi(GVAR_GAMEPHASE))		


			// check for mission time update
			if (gCLN_MissionTimePrevID!=SC_ggi(GVAR_MISSIONTIME_UPDATE)){
				gCLN_MissionTimePrevID = SC_ggi(GVAR_MISSIONTIME_UPDATE);
				gCLN_MissionTime = SC_ggf(GVAR_MISSIONTIME);
			}
			else{
				if (SC_ggi(GVAR_GAMEPHASE)==MISSION_PHASE_INGAME)
					gCLN_MissionTime -= info->elapsed_time;
				
			}

			// update HUD info - icons at left top corner
			
			for (i=0;i<2;i++){

				gCLN_SidePoints[i] = SC_ggi(GVAR_SIDE0POINTS+i);			
				SC_MP_SetSideStats(i,0,gCLN_SidePoints[i]);
										

				icon[i].type = SC_HUD_MP_ICON_TYPE_NUMBER;
				icon[i].icon_id = 3*i;
				icon[i].value = gCLN_SidePoints[i];
				icon[i].color = 0xbbffffff;

			}// for (i)

			icons = 2;

			if ((gCLN_MissionTime>0.0f)&&(SC_ggi(GVAR_GAMEPHASE))){
				icon[icons].color = 0xbbffffff;
				icon[icons].icon_id = 6;
									
				if (SC_ggi(GVAR_GAMEPHASE)==MISSION_PHASE_WIN_DEFENDERS)
					icon[icons].value = 0;					
				else
					icon[icons].value = (int)(gCLN_MissionTime+0.99f);					

				icon[icons].type = SC_HUD_MP_ICON_TYPE_TIME;
				icons++;
			}

			SC_MP_SetIconHUD(icon,icons);


			break;// SC_NET_MES_CLIENT_TICK

		case SC_NET_MES_LEVELPREINIT:
			// is called before level.c SC_LEV_MES_INITSCENE is called
			// use it for set gametype and some basic setting that has to be done before scene initialization

			SC_sgi(GVAR_MP_MISSIONTYPE,GVAR_MP_MISSIONTYPE_TT);

			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;

			SC_MP_EnableBotsFromScene(FALSE);

			//SC_MP_SetSpectatorCameras('T');		// this function is supported from v1.33

			break;// SC_NET_MES_LEVELPREINIT

		case SC_NET_MES_LEVELINIT:
			// initialization

		#if _GE_VERSION_ >= 138
			g_FPV_UsFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_USflag.BES");
			g_FPV_VcFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_VCflag.BES");
			g_FPV_NeFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_emptyflag.BES");
		#endif

			
			SC_MP_SRV_SetForceSide(0xffffffff);
			SC_MP_SetChooseValidSides(3);

			// set class limits depending on server settings and perhaps on script preferences too
			SC_MP_SRV_SetClassLimit(18,0);
			SC_MP_SRV_SetClassLimit(19,0);
			SC_MP_SRV_SetClassLimit(39,0);

			SC_MP_GetSRVsettings(&SRVset);

			for (i=0;i<6;i++){
				SC_MP_SRV_SetClassLimit(i+1,SRVset.atg_class_limit[i]);
				SC_MP_SRV_SetClassLimit(i+21,SRVset.atg_class_limit[i]);
			}// for (i)


			// set 'TAB' windows appearance

			CLEAR(hudinfo);
			hudinfo.title = 5100;
			
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

			// set some MP attributes
			SC_MP_AllowStPwD(TRUE);
			SC_MP_AllowFriendlyFireOFF(TRUE);

			SC_MP_SetItemsNoDisappear(FALSE);
			

			if (info->param2){	// TRUE means initialization for the first time


				// find flags in the scene
				CLEAR(gFlagNod);

				for (i=0;i<STEP_MAX;i++){

					sprintf(txt,"TT_flag_%d",i);

					nod = SC_NOD_GetNoMessage(NULL,txt);

					
					
				
					if (nod){
						SC_NOD_GetPivotWorld(nod,&gFlagPos[i]);
						gFlagNod[i][0] = SC_NOD_Get(nod,"vlajkaUS");
						gFlagNod[i][1] = SC_NOD_Get(nod,"Vlajka VC");
						gFlagNod[i][2] = SC_NOD_Get(nod,"vlajka N");
					}// if (nod)

				}// for (i=0;i<STEP_MAX;i++)


				if (info->param1){	// TRUE means it's a server
					
					// set used global variables network synchronization ( for those that require it )
					
					SC_MP_Gvar_SetSynchro(GVAR_SIDE0POINTS);
					SC_MP_Gvar_SetSynchro(GVAR_SIDE1POINTS);
					UpdateSidePoints();

					SC_MP_Gvar_SetSynchro(GVAR_GAMEPHASE);
					SC_sgi(GVAR_GAMEPHASE,0);

					SC_MP_Gvar_SetSynchro(GVAR_MAINPHASE);
					SC_sgi(GVAR_MAINPHASE,0);

					SC_MP_Gvar_SetSynchro(GVAR_LASTSCORES);
					SC_sgi(GVAR_LASTSCORES,0);

					SC_MP_Gvar_SetSynchro(GVAR_LASTWIN);
					SC_sgi(GVAR_LASTWIN,0);

					SC_MP_Gvar_SetSynchro(GVAR_SCORING_PLAYER);
					SC_sgi(GVAR_SCORING_PLAYER,0);			
				

					SC_MP_Gvar_SetSynchro(GVAR_CURSTEP);
					SC_sgi(GVAR_CURSTEP,0);

					SC_MP_Gvar_SetSynchro(GVAR_STEPS);
					

					SC_MP_Gvar_SetSynchro(GVAR_MISSIONTIME);
					SC_MP_Gvar_SetSynchro(GVAR_MISSIONTIME_UPDATE);
					SC_sgf(GVAR_MISSIONTIME,0.0f);
					SC_sgi(GVAR_MISSIONTIME_UPDATE,0);		


					// find respawn points					
					CLEAR(gRecs);

					for (k=0;k<2;k++){

						if (k) side_char = 'D';
							else side_char = 'A';

						for (j=0;j<STEP_MAX;j++){

							for (i=0;i<REC_MAX;i++){

								sprintf(txt,"TT_%c%d_%d",side_char,j,i);
								
								if (SC_NET_FillRecover(&gRec[k][j][gRecs[k][j]],txt)){
									gRecs[k][j]++;								
								}
							}//for (i) - for all recovers on current step
							

#if _GE_VERSION_ >= 133
							if (gRespawn_id[k][j]){
								i = REC_MAX - gRecs[k][j];
								SC_MP_GetRecovers(gRespawn_id[k][j],&gRec[k][j][gRecs[k][j]],&i);
								gRecs[k][j] += i;								
							}
#endif


						}// for (j) - steps

					}// for (k)				
					
					gSteps = 0;

					for (i=0;i<STEP_MAX;i++)
						if (gRecs[0][i]) gSteps = i+1;
							

					for (i=0;i<gSteps;i++)
						SC_Log(3,"TurnTable recovers #%d: att:%d  def:%d",i,gRecs[0][i],gRecs[1][i]);

					CLEAR(gRecTimer);


					// find script helpers for flags capturing

					for (i=0;i<gSteps-1;i++){

						sprintf(txt,"TTS_%d",i);

						if (!SC_GetScriptHelper(txt,&gStepSwitch[i])){
							SC_message("helper %s not found",txt);
						}

					}

					SC_sgi(GVAR_STEPS,gSteps);

				}// if (info->param1)

			}//if (info->param2)

			break;// SC_NET_MES_LEVELINIT


		case SC_NET_MES_RENDERHUD:

			// is called on every client in every frame - enables rendering some on screen info

			i = 0;
			witxt = NULL;
			in_middle = FALSE;

			k = SC_ggi(GVAR_MAINPHASE);

			if (gCLN_gamephase!=SC_ggi(GVAR_GAMEPHASE)){
				gCLN_gamephase = SC_ggi(GVAR_GAMEPHASE);
				switch(gCLN_gamephase){
					case MISSION_PHASE_WIN_ATTACKERS:
					case MISSION_PHASE_WIN_DEFENDERS:
						if (SC_ggi(GVAR_LASTWIN)==0) SC_SND_PlaySound2D(11117);
							else SC_SND_PlaySound2D(11116);
						break;					
				}
			}

			// write info about game status

			switch(gCLN_gamephase){

				case MISSION_PHASE_NOACTIVE:// waiting for players
					if (gCLN_ShowWaitingInfo<=0.0f)					
						witxt = SC_Wtxt(1076);

					gCLN_ShowStartInfo = 0.0f;
					break;

				case MISSION_PHASE_INGAME:

					gCLN_ShowWaitingInfo = 3.0f;

					if (gCLN_ShowStartInfo==0.0f){
						gCLN_ShowStartInfo = 3.0f;
					}

					if (gCLN_ShowStartInfo>0.0f){

						i = SC_PC_Get();
						if (i){
							SC_P_GetInfo(i,&plinfo);

							if (plinfo.side==GetAttackingSide(SC_ggi(GVAR_MAINPHASE)))
								witxt = SC_Wtxt(5108);
							else
								witxt = SC_Wtxt(5109);

							SC_GameInfoW(witxt);
							witxt = NULL;
						}					

					}
					else					
					if ((gCLN_ShowInfo>0.0f)&&(gCLN_CurStep>0)){

						j = SC_MP_GetPlofHandle(SC_ggi(GVAR_SCORING_PLAYER));
						if (j){						
							SC_AnsiToUni(SC_P_GetName(j),wtxt2);
						}
						else
							SC_AnsiToUni("'disconnected'",wtxt2);

						swprintf(wtxt,SC_Wtxt(5107),wtxt2,gCLN_CurStep);
						witxt = wtxt;
					}
					else{
						// write attack/defend info						

						i = SC_PC_Get();
						if (i){
							SC_P_GetInfo(i,&plinfo);

							if (plinfo.side==GetAttackingSide(SC_ggi(GVAR_MAINPHASE))){
								if (gCLN_CurStep==1){
									witxt = SC_Wtxt(5111);
								}
								else{
									swprintf(wtxt,SC_Wtxt(5110),gCLN_CurStep-1);
									witxt = wtxt;
								}
							}
							else{
								if (gCLN_CurStep==1){
									witxt = SC_Wtxt(5113);
								}
								else{
									swprintf(wtxt,SC_Wtxt(5112),gCLN_CurStep-1);
									witxt = wtxt;
								}
							}
								
						}// if (i)

					}
					
					break;

				case MISSION_PHASE_WIN_ATTACKERS:
					// US attackers win and scores - 5101
					// VC attackers win and scores - 5102

					// US attackers win, VC have to beat their time now ! - 5103
					// VC attackers win, US have to beat their time now ! - 5104

					j = SC_MP_GetPlofHandle(SC_ggi(GVAR_SCORING_PLAYER));
					if (j){						
						SC_AnsiToUni(SC_P_GetName(j),wtxt2);
					}
					else
						SC_AnsiToUni("'disconnected'",wtxt2);
					
					switch(k%4){
						case 0:i = 5101;break;
						case 1:i = 5103;break;
						case 2:i = 5102;break;
						case 3:i = 5104;break;
					}// switch(k%4)
					

					swprintf(wtxt,SC_Wtxt(i),wtxt2);
					witxt = wtxt;
					gCLN_ShowStartInfo = 0.0f;
					break;

				case MISSION_PHASE_WIN_DEFENDERS:
					// US defenders win and scores - 5105
					// VC defenders win and scores - 5106

					j = SC_MP_GetPlofHandle(SC_ggi(GVAR_SCORING_PLAYER));
					if (j){						
						SC_AnsiToUni(SC_P_GetName(j),wtxt2);
					}
					else
						SC_AnsiToUni("'disconnected'",wtxt2);


					switch(SC_ggi(GVAR_LASTSCORES)){
						case 0:i = 5105;break;
						case 1:i = 5106;break;
					}

					swprintf(wtxt,SC_Wtxt(i),wtxt2);
					witxt = wtxt;	
					gCLN_ShowStartInfo = 0.0f;

					break;

			}// switch(SC_ggi(GVAR_GAMEPHASE))
			
				
			if (witxt){
				
				SC_GetScreenRes(&val,&valy);

				val -= SC_Fnt_GetWidthW(witxt,1); 

				if (in_middle) valy = 0.5f * valy - 40.0f;
					else valy = 15;

				SC_Fnt_WriteW(val * 0.5f,valy,witxt,1,0xffffffff);

			}//if (i)


			break;

		case SC_NET_MES_SERVER_RECOVER_TIME:
			// game engine asks server for time to respawn selected player

			if (info->param2){
				// player just connects to the game, respawn immediatelly
				info->fval1 = 0.1f;
			}
			else{
				// player is killed
				switch(gMission_phase){

					case MISSION_PHASE_INGAME:

						// check if he is not autobalanced
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
						break;

					case MISSION_PHASE_NOACTIVE:
						info->fval1 = 3.0f;
						break;

					default:
						// do not respawn
						info->fval1 = -1.0f;
						break;
				}// switch(gMission_phase)

			}

			break;

		case SC_NET_MES_SERVER_RECOVER_PLACE:
			// game engine asks for place where to recover some player

			precov = (s_SC_MP_Recover*)info->param2;

			j = info->param1; // side
			if (gAttackingSide) j = 1-j;
				
			if (j){
				// defenders
				if (gMission_phase==MISSION_PHASE_INGAME){
					if (gCurStep<2) k = 0;
						else k = gCurStep-1-rand()%2;
				}
				else k = 0;

			}
			else{
				// attackers
				if (gMission_phase==MISSION_PHASE_INGAME){
					k = gCurStep;
				}
				else k = gSteps-1;
			}			

			i = SC_MP_SRV_GetBestDMrecov(gRec[j][k],gRecs[j][k],gRecTimer[j][k],NORECOV_TIME);
			
			gRecTimer[j][k][i] = NORECOV_TIME;
			*precov = gRec[j][k][i];
															
			break;



		case SC_NET_MES_RESTARTMAP:
			// command restart map came

			gTime = 0;

			CLEAR(gSidePoints);			
			UpdateSidePoints();			

			SC_MP_SetInstantRecovery(TRUE);

			if (gMission_phase!=MISSION_PHASE_NOACTIVE){
				SC_MP_RestartMission();							
				SC_MP_RecoverAllNoAiPlayers();			
				gMission_phase = MISSION_PHASE_NOACTIVE;				
				SC_sgi(GVAR_GAMEPHASE,gMission_phase);				
			}

			gCLN_ShowInfo = 0.0f;
			SC_MP_SRV_ClearPlsStats();

			break;// SC_NET_MES_RESTARTMAP

		case SC_NET_MES_RULESCHANGED:
			// command change end rule came
			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;
			break;

		case SC_NET_MES_SERVER_KILL:
			// some player is killed, check autobalance
			Check_ABL(info->param1);			
			break;// SC_NET_MES_SERVER_KILL
			

	}// switch(info->message)
	


	return 1;

}// int ScriptMain(void)
