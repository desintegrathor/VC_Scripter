//
//	Universal include for Cooperative MP game. List of bombs and/or
//	list of places where players must reach can be defined using a few #defines.
//	Beny
//
//	Pridano par funkci, aby to behalo s destrukcemi aut.
//	Pridana faze EXPLODING na podporu rozsahlejsich vybuchu.
//	MAX

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\gLevel.h>
#include <inc\!max_defs_mp.h>

float gTimeBomb[NUM_BOMBS];
float gBombTimer[NUM_BOMBS];

//used for missions with VC attacking some place

//#define RECOVER_TIME	15.0f		// time to global recover
#define NORECOV_TIME	3.0f		// disable time of recoverplace after recovering someone there

#ifdef REC_WPNAME_US
	#define COOP_SIDE			SC_P_SIDE_US
	#define COOP_SIDE_INDEX		0
	#define OPP_SIDE			SC_P_SIDE_VC
	#define OPP_SIDE_INDEX		1
#endif

#ifdef REC_WPNAME_VC
	#define COOP_SIDE			SC_P_SIDE_VC
	#define COOP_SIDE_INDEX		1
	#define OPP_SIDE			SC_P_SIDE_US
	#define OPP_SIDE_INDEX		0
#endif

#ifdef MUL_REC_WPNAME_US
	#define COOP_SIDE			SC_P_SIDE_US
	#define COOP_SIDE_INDEX		0
	#define OPP_SIDE			SC_P_SIDE_VC
	#define OPP_SIDE_INDEX		1
#endif

#ifdef MUL_REC_WPNAME_VC
	#define COOP_SIDE			SC_P_SIDE_VC
	#define COOP_SIDE_INDEX		1
	#define OPP_SIDE			SC_P_SIDE_US
	#define OPP_SIDE_INDEX		0
#endif

#define REC_MAX					64

#define GPHASE_BEGIN			1
#define GPHASE_GAME				2
#define GPHASE_DONE				3
#define GPHASE_FAILED			4

#define GVAR_OPP_WON			590			//oppos team conquered the place (0/1)
#define	GVAR_OPP_ATTACK			591			//Info for opp AI players - begin attack

#ifdef FLYBY_ANIM
BOOL			flyby_playing = FALSE;
#endif

float			animtime;
float			endtime;
//
float			gNextRecover = 0.0f;
dword			gRecs = 0;
float			gRecTimer[REC_MAX];
float			gAllNoAiRecover  = 0.0f;
dword			gRecoverTime = 0;
dword			gRecoverLimit = 0;
s_SC_MP_Recover gRec[REC_MAX];

dword			gEndRule;
dword			gEndValue;
float			gTime;
float			gTimeAttack = 0.0f;
float			gShowTimer;
BOOL			bombsExploded;
dword			gPhase = GPHASE_BEGIN;
float			gPhase_timer = 5.0f;
dword			gPhase_send = 0;
dword			gRoundCount = 0;

BOOL			gValidSideCoop = FALSE;
dword			gRespawnGroup = 0;
BOOL			bRespawnGroup = FALSE;
//int				bRestart;

void set_recovers() {
	int		i;
	char	txt[32];

	gRecs = 0;

	for (i = 0; i < REC_MAX; i++) {
#ifdef REC_WPNAME_US
		sprintf(txt,REC_WPNAME_US,i);
#endif
#ifdef REC_WPNAME_VC
		sprintf(txt,REC_WPNAME_VC,i);
#endif
#ifdef MUL_REC_WPNAME_US
		sprintf(txt,MUL_REC_WPNAME_US,gRespawnGroup,i);
#endif
#ifdef MUL_REC_WPNAME_VC
		sprintf(txt,MUL_REC_WPNAME_VC,gRespawnGroup,i);
#endif
		if ( SC_NET_FillRecover(&gRec[gRecs],txt) )
			gRecs++;
	}					
#ifdef REC_WPNAME_VC
	if (gRecs == 0)	SC_message("no VC recover place defined!");
#endif
#ifdef REC_WPNAME_US
	if (gRecs == 0)	SC_message("no US recover place defined!");
#endif
#ifdef MUL_REC_WPNAME_VC
	if (gRecs == 0)	SC_message("no VC recover place defined!");
#endif
#ifdef MUL_REC_WPNAME_US
	if (gRecs == 0)	SC_message("no US recover place defined!");
#endif
}

//
dword InitEndPlaces() {
	dword	cur = 0;
	return cur;
}

void reinitAll() {
	s_SC_MP_EnumPlayers		plList[64];
	s_SC_MP_SRV_settings	SRVset;
	dword					i, num;

	CLEAR(gRecTimer);

	gNextRecover = 0.0f;
	gShowTimer = 0.0f;
	bombsExploded = FALSE;

	gTime = 0;

	gPhase = GPHASE_BEGIN;
	gPhase_timer = 5.0f;
	gPhase_send = 0;

	gValidSideCoop = FALSE;

	//
	num = 64;
	SC_MP_EnumPlayers(plList, &num, OPP_SIDE);
	for (i = 0; i < num; i++)
	{
		SC_P_ScriptMessage(plList[i].id, SCM_MP_REINIT, 0);
	}
	
	SC_MP_GetSRVsettings(&SRVset);
	gRecoverTime = SRVset.coop_respawn_time;
	gRecoverLimit = SRVset.coop_respawn_limit;

	gAllNoAiRecover  = 0.0f;
#ifdef NUM_BOMBS
	for (i=0; i<NUM_BOMBS; i++) gBombTimer[i] = BOMB_TIME[i];
#endif
	
//		SC_MP_SetInstantRecovery(TRUE);

	SC_MP_SRV_ClearPlsStats();

	SC_MP_SRV_InitGameAfterInactive();
	SC_MP_RecoverAllAiPlayers();
	SC_MP_RecoverAllNoAiPlayers();

	gRespawnGroup = 0;
	bRespawnGroup = FALSE;
	SC_sgi(GVAR_RESPAWN_GROUP, gRespawnGroup);
	set_recovers();
}

BOOL SRV_CheckEndRule(float time) {
	switch(gEndRule)
	{
	case SC_MP_ENDRULE_TIME:			
		if (gValidSideCoop) 
			gTime += time;

		SC_MP_EndRule_SetTimeLeft(gTime,gValidSideCoop);

		if (gTime>gEndValue)
		{
			SC_MP_LoadNextMap();
			return TRUE;
		}
		break;
	case SC_MP_ENDRULE_POINTS:
		if (gRoundCount >= gEndValue){
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


void SRV_CheckUpdate(void)
{

	if (gPhase_send != gPhase)
	{
		gPhase_send = gPhase;
		SC_sgi(GVAR_GPHASE,gPhase);
	}// if (gPhase_send!=gPhase)

}// void SRV_CheckUpdate(void)



//
int ScriptMain(s_SC_NET_info *info)
{
	s_SC_MP_EnumPlayers		plList[64];
	s_SC_MP_SRV_settings	SRVset;
	s_SC_MP_Recover			*precov;
	s_SC_MP_hud				hudinfo;
	s_SC_P_getinfo			plinfo;
	s_SC_HUD_MP_icon		icon[2];
	dword					i, j, sideA, sideB, num, ali;
	BOOL					valid[2];
	BOOL					alldeath, bPlaceOK;
	char					txt[32];
	ushort					*itxt;
	float					val;
	c_Vector3				vec;
	char					tmpstr[32];

	//
	switch(info->message)
	{
	case SC_NET_MES_SERVER_TICK:
		/*if ((bRestart == 1) && (gPhase == GPHASE_BEGIN)) {
			SC_sgi(GVAR_RESTART, 1);
			bRestart = 2;
		}
		if ((bRestart == 2) && (gPhase == GPHASE_GAME)) {
			SC_sgi(GVAR_RESTART, 0);
			bRestart = 0;
		}*/

		if (SRV_CheckEndRule(info->elapsed_time)) 
			break;

		//for (j=0;j<2;j++) //todle jsem nepochopil proc to tu je
		for (i=0;i<gRecs;i++)
			gRecTimer[i] -= info->elapsed_time;


		if (gRecoverTime<0xffff) {
			gNextRecover -= info->elapsed_time;
			if (gNextRecover<0.0f) 
				gNextRecover = (float)gRecoverTime;
		}// if (gRecoverTime<0xffff)
	
		if (gAllNoAiRecover>0.0f) {
			gAllNoAiRecover -= info->elapsed_time;				
			if (gAllNoAiRecover<=0.0f)
				SC_MP_RecoverAllNoAiPlayers();		
			break;
		} else {
			gAllNoAiRecover -= info->elapsed_time;
		}// if (gAllNoAiRecover>0.0f)


		//check for alive AI and players
		CLEAR(valid);			
		j = 64;
		alldeath = FALSE;

		if ( SC_MP_EnumPlayers(plList,&j,SC_MP_ENUMPLAYER_SIDE_ALL) ) {
			alldeath = TRUE;

			for (i = 0; i < j; i++) {
				if (plList[i].status==SC_MP_P_STATUS_INGAME) {
					if (plList[i].side > 1) {
						SC_message("coop script wrong side: %d",plList[i].side);
					} else {
						valid[plList[i].side] = TRUE;
					}
				}

				if ( (plList[i].side == COOP_SIDE) && (plList[i].status == SC_MP_P_STATUS_INGAME) ) alldeath = FALSE;
			}// for (i)

			SC_Log(3,"Enum, v[COOP_SIDE_INDEX]: %d| v[OPP_SIDE_INDEX]: %d| alldeath: %d",valid[COOP_SIDE_INDEX],valid[OPP_SIDE_INDEX],alldeath); //prehozeno 1-0
				
		} else {
			SC_Log(3,"NoEnum");
		}// if (SC_MP_EnumPlayers(plList,&j,SC_MP_ENUMPLAYER_SIDE_ALL))

	
		if ( (gPhase == GPHASE_GAME) && (alldeath) && (gPhase_timer < 0.0f)) {
			if (gRecoverLimit == 0) {
				// mission failed
				SC_Log(2,"Set GPHASE_FAILED");
				gPhase = GPHASE_FAILED;
				gPhase_timer = 5.0f;
			} else {
				// recover unlimited
				if ( (gRecoverTime >= 0xffff) && (gAllNoAiRecover < -5.0f)) {
					gAllNoAiRecover = 4.0f;
				}
			}

		}// if ((alldeath)&&(gRecoverTime>=0xffff))
		else
		{
			gAllNoAiRecover = 0.0f;
		}


		gValidSideCoop = valid[COOP_SIDE_INDEX]; //zmeneno


		//gPhase
		switch(gPhase)
		{
		case GPHASE_BEGIN:
			gPhase_timer -= info->elapsed_time;

			if (gPhase_timer<0.0f) {

				if ( (valid[0]) && (valid[1]) )	{
					//Init bombs
#ifdef NUM_BOMBS
					for (i = 0; i < NUM_BOMBS; i++)	{
						SC_sgi(GVAR_BOMBSTATUS__+i*2, BOMB_STATUS_INACTIVE);
						gTimeBomb[i] = gBombTimer[i];
						SC_sgf(GVAR_BOMBSTIME__+i*2, gTimeBomb[i]);
					}
#endif //NUM_BOMBS

					gTimeAttack = 0.0f;
					SC_sgi(GVAR_OPP_WON, FALSE);
					SC_sgi(GVAR_OPP_ATTACK, FALSE);
					
					SC_Log(2,"Set GPHASE_GAME");
					gPhase_timer = 5.0f;
					gPhase = GPHASE_GAME;
					gRespawnGroup = 0;
					bRespawnGroup = FALSE;
					SC_sgi(GVAR_RESPAWN_GROUP, gRespawnGroup);
					set_recovers();
				}
			}
			break;

		case GPHASE_GAME:
			gPhase_timer -= info->elapsed_time;

			if (gPhase_timer<0.0f) {
				//all VC are dead
				if (!valid[OPP_SIDE_INDEX]) { //zmeneno
					SC_Log(2,"Set GPHASE_DONE - Vc killed");
					gPhase = GPHASE_DONE;
					gPhase_timer = 8.0f;
				}// if (!valid[])

#ifdef OPP_ATTACK	//when VC attacking
				//countdown, then attack
				if (!SC_ggi(GVAR_OPP_ATTACK) && valid[COOP_SIDE_INDEX]) // zmeneno
				{
					gTimeAttack += info->elapsed_time;
					if (gTimeAttack > TIME_TOATTACK)				//dame hracovi nakej cas
					{
						SC_sgi(GVAR_OPP_ATTACK, TRUE);
					}
				}

				//VC won!
				if (SC_ggi(GVAR_OPP_WON))
				{
					gPhase = GPHASE_DONE;
					gPhase_timer = 8.0f;
				}
#endif //OPP_ATTACK

				//tickin' time bombs
#ifdef NUM_BOMBS
				for (i = 0; i < NUM_BOMBS; i++)
				{
					if ( (SC_ggi(GVAR_BOMBSTATUS__+i*2) == BOMB_STATUS_ACTIVE) && (gTimeBomb[i] > 0.0f) )
					{
						gTimeBomb[i] -= info->elapsed_time;
						SC_sgf(GVAR_BOMBSTIME__+i*2, gTimeBomb[i]);
						if (gTimeBomb[i] <= 0.0f)
						{
							SC_sgi(GVAR_BOMBSTATUS__+i*2, BOMB_STATUS_EXPLODING);
							gTimeBomb[i] = 0.0f;
						}
					}
				}

				//bombs exploded
				num = 0;
				for (i = 0; i < NUM_BOMBS; i++) {
					if ( (SC_ggi(GVAR_BOMBSTATUS__+i*2) == BOMB_STATUS_EXPLODED) ) {
						num |= (1 << i);
					}
				}

				//check if we end up the level
				//if ( (num) && ((num == BOMB_LEVELDONE_MASK) || (BOMB_LEVELDONE_MASK == 0)) )
				if ( (num) && ((num & BOMB_LEVELDONE_MASK) == BOMB_LEVELDONE_MASK) ) {
					SC_Log(2,"Set GPHASE_DONE - bombs exploded");
					gPhase = GPHASE_DONE;
					gPhase_timer = 6.0f;
				}
#endif //NUM_BOMBS

				//all alive players reached specified place
#ifdef NUM_ENDPLACES
				if (NUM_ENDPLACES > 0)
				{
					num = 64;
					SC_MP_EnumPlayers(plList, &num, COOP_SIDE);

					//go thru end-places
					if (num)
					{
						for (j = 0; j < NUM_ENDPLACES; j++)
						{
							bPlaceOK = TRUE;
							ali = 0;
							//go thru alive players
							for (i = 0; i < num; i++)
							{
								if ( (plList[i].status == SC_MP_P_STATUS_INGAME) && SC_P_IsReady(plList[i].id) )
								{
									ali++;
									SC_P_GetPos(plList[i].id, &vec);
									if ( !SC_IsNear3D(&vec, &gEndPlace[j].pos, gEndPlace[j].rad) )
									{
										bPlaceOK = FALSE;
										break;//i
									}
								}
							}//for (i)

							//
							if (ali && bPlaceOK)
							{
								SC_Log(2,"Set GPHASE_DONE - place reached");
								gPhase = GPHASE_DONE;
								gPhase_timer = 8.0f;
								break;//j
							}
						}//for (j)
					}//if (num)
				}
#endif //NUM_ENDPLACES
			}
			break;

		case GPHASE_DONE:
			gPhase_timer -= info->elapsed_time;
			if (gPhase_timer < 0.0f)
			{
				//reinitAll();
				gRoundCount++;
				if (SRV_CheckEndRule(info->elapsed_time)) break;
				SC_Log(2,"SC_MP_RestartMission");
				SC_MP_RestartMission();					//restart
				gPhase = GPHASE_BEGIN;
				gPhase_timer = 5.0f;
				gRespawnGroup = 0;
				bRespawnGroup = FALSE;
				SC_sgi(GVAR_RESPAWN_GROUP, gRespawnGroup);
				set_recovers();
				//bRestart = 1;
			}
#ifdef OPP_ATTACK
			else if ( SC_ggi(GVAR_OPP_WON) && (dwDoExplosion < NUM_EXPLOSIONS) )
			{
				GetDummyPos(dummyExpl[rand()%NUM_EXPLOSIONS], &vec);	//declared in gLevel.h
				SC_MP_SRV_DoExplosion(&vec, SC_EXPL_TYPE_MORTAR);

				if ((rand()%3)==0)
				{
					GetDummyPos(dummyExpl[rand()%NUM_EXPLOSIONS], &vec);
					SC_MP_SRV_DoExplosion(&vec, SC_EXPL_TYPE_MORTAR);
				}

				dwDoExplosion++;
			}
#endif
			break;

		case GPHASE_FAILED:
			gPhase_timer -= info->elapsed_time;
			if (gPhase_timer < 0.0f)
			{
				SC_Log(2,"SC_MP_RestartMission");
				//reinitAll();
				SC_MP_RestartMission();					//restart

				gPhase = GPHASE_BEGIN;
				gPhase_timer = 5.0f;
				gRespawnGroup = 0;
				bRespawnGroup = FALSE;
				SC_sgi(GVAR_RESPAWN_GROUP, gRespawnGroup);
				set_recovers();
				//bRestart = 1;
			}
			break;
		}// switch(gPhase)

		SRV_CheckUpdate();
		break;


	case SC_NET_MES_CLIENT_TICK:
#ifdef FLYBY_ANIM
		if (flyby_playing == TRUE) {
			animtime += info->elapsed_time;
			if ((animtime > endtime) && (!SC_P_IsReady(SC_PC_Get()))) {
				animtime=SC_ANM_GetFrameTime(FLYBY_ANIM,FLYBY_ANIM_START);
				SC_SetViewAnim(FLYBY_ANIM, FLYBY_ANIM_START, FLYBY_ANIM_END + 10, FLYBY_ANIM_CALLB);
			}
			if ( SC_P_IsReady(SC_PC_Get()) ) {
				flyby_playing = FALSE;
				SC_SetViewAnim(NULL, 0, 0, 0);
			}
		}	
#endif

		num = 0;
		
#ifdef NUM_BOMBS
		j = 0;
		for (i = 0; i < NUM_BOMBS; i++) {
			if ( (SC_ggi(GVAR_BOMBSTATUS__+i*2) == BOMB_STATUS_EXPLODED) ) {
				j |= (1 << i);
			}
		}
		if ( (j) && ((j & BOMB_LEVELDONE_MASK) == BOMB_LEVELDONE_MASK) )
			bombsExploded = TRUE;
		else
			bombsExploded = FALSE;

		for (i = 0; i < NUM_BOMBS; i++) {
			gTimeBomb[i] = SC_ggf(GVAR_BOMBSTIME__+i*2);
			if ( (SC_ggi(GVAR_BOMBSTATUS__+i*2) == BOMB_STATUS_ACTIVE) && (gTimeBomb[i] >= 0.0f) )
			{
				icon[num].type = SC_HUD_MP_ICON_TYPE_TIME;
				icon[num].icon_id = 10;
				icon[num].value = gTimeBomb[i];
				icon[num].color = 0xFFFFFFFF;
				num++;
			}
		}
		
#endif //NUM_BOMBS

		SC_MP_SetIconHUD(icon, num);
		if (gShowTimer > 0) {
			gShowTimer -= info->elapsed_time;
			itxt=SC_Wtxt(1077 + COOP_SIDE_INDEX); //zmena z 1077
			SC_GetScreenRes(&val,NULL);
			val -= SC_Fnt_GetWidthW(itxt,1);
			SC_Fnt_WriteW(val * 0.5f,15,itxt,1,0xffffffff);
		}
		break;// SC_NET_MES_CLIENT_TICK


	case SC_NET_MES_LEVELPREINIT:
		SC_sgi(GVAR_MP_MISSIONTYPE,GVAR_MP_MISSIONTYPE_COOP);
		SC_sgi(GVAR_MP_MISSIONSUBTYPE,COOP_SIDE_INDEX+1);

		gEndRule = info->param1;
		gEndValue = info->param2;
		gTime = 0.0f;
		gShowTimer = 0.0f;
		bombsExploded = FALSE;
		gRoundCount = 0;
		//bRestart = 0;

		//SC_sgi(GVAR_RESTART, 0);

		SC_MP_EnableBotsFromScene(TRUE);
		SC_MP_EnableC4weapon(TRUE);
#ifdef NUM_BOMBS
		for (i=0; i<NUM_BOMBS; i++) gBombTimer[i] = BOMB_TIME[i];
#endif

#ifdef FLYBY_ANIM
		flyby_playing = TRUE;
#endif

		break;// SC_NET_MES_LEVELPREINIT


	case SC_NET_MES_LEVELINIT:
		SC_MP_SRV_SetForceSide(COOP_SIDE_INDEX); //zmeneno
		//SC_MP_SRV_SetForceSide(0xffffffff); //zmeneno
		//SC_MP_SetChooseValidSides(0xffffffff);	//navic

		SC_MP_SRV_SetClassLimit(18,0);
		SC_MP_SRV_SetClassLimit(19,0);
		SC_MP_SRV_SetClassLimit(39,0);

		SC_MP_GetSRVsettings(&SRVset);

		for (i = 0; i < 6; i++)
		{
			if (CLASS_LIMIT_US[i] == -2) SC_MP_SRV_SetClassLimit(i+1, SRVset.atg_class_limit[i]); else SC_MP_SRV_SetClassLimit(i+1, CLASS_LIMIT_US[i]);
			if (CLASS_LIMIT_VC[i] == -2) SC_MP_SRV_SetClassLimit(i+21,SRVset.atg_class_limit[i]); else SC_MP_SRV_SetClassLimit(i+21,CLASS_LIMIT_VC[i]);
		}// for (i)

		CLEAR(hudinfo);
		hudinfo.title = 1098;

		hudinfo.sort_by[0] = SC_HUD_MP_SORTBY_KILLS;
		hudinfo.sort_by[1] = SC_HUD_MP_SORTBY_DEATHS | SC_HUD_MP_SORT_DOWNUP;
		hudinfo.sort_by[2] = SC_HUD_MP_SORTBY_PINGS | SC_HUD_MP_SORT_DOWNUP;

		hudinfo.pl_mask = SC_HUD_MP_PL_MASK_KILLS | SC_HUD_MP_PL_MASK_DEATHS;
		hudinfo.use_sides = TRUE;
		hudinfo.side_name[0] = 1010;
		hudinfo.side_color[0] = 0x440000ff;
		hudinfo.side_name[1] = 1011;
		hudinfo.side_color[1] = 0x44ff0000;
#ifdef REC_WPNAME_US
		hudinfo.disableVCside = TRUE;
#endif
#ifdef REC_WPNAME_VC
		hudinfo.disableUSside = TRUE;
#endif
#ifdef MUL_REC_WPNAME_US
		hudinfo.disableVCside = TRUE;
#endif
#ifdef MUL_REC_WPNAME_VC
		hudinfo.disableUSside = TRUE;
#endif
		hudinfo.side_mask = SC_HUD_MP_SIDE_MASK_FRAGS;
		
		SC_MP_HUD_SetTabInfo(&hudinfo);

		SC_MP_AllowStPwD(TRUE);
		SC_MP_AllowFriendlyFireOFF(TRUE);
		SC_MP_SetItemsNoDisappear(FALSE);

		SC_MP_SetChooseValidSides(OPP_SIDE_INDEX);			//zmeneno
		//
		if (info->param2)
		{
			if (info->param1)
			{
				// it's server		
				SC_MP_GetSRVsettings(&SRVset);
				gRecoverTime = SRVset.coop_respawn_time;
				gRecoverLimit = SRVset.coop_respawn_limit;

				SC_MP_SRV_InitWeaponsRecovery(-1.0f);
				
				//

				SC_MP_Gvar_SetSynchro(GVAR_GPHASE);
#ifdef OPP_ATTACK
				SC_MP_Gvar_SetSynchro(GVAR_OPP_WON);
				SC_MP_Gvar_SetSynchro(GVAR_OPP_ATTACK);
#endif
				//SC_MP_Gvar_SetSynchro(GVAR_RESTART);
#ifdef NUM_BOMBS
				for (i = 0; i < NUM_BOMBS; i++)
				{
					SC_MP_Gvar_SetSynchro(GVAR_BOMBSTIME__+i*2);
				}
#endif //NUM_BOMBS

#ifdef NUM_ENDPLACES
				InitEndPlaces();
#endif //NUM_ENDPLACES
				
				gRecs = 0;

				for (i = 0; i < REC_MAX; i++)
				{
#ifdef REC_WPNAME_US
					sprintf(txt,REC_WPNAME_US,i);
#endif
#ifdef REC_WPNAME_VC
					sprintf(txt,REC_WPNAME_VC,i);
#endif
#ifdef MUL_REC_WPNAME_US
					sprintf(txt,MUL_REC_WPNAME_US,0,i);
#endif
#ifdef MUL_REC_WPNAME_VC
					sprintf(txt,MUL_REC_WPNAME_VC,0,i);
#endif
					if ( SC_NET_FillRecover(&gRec[gRecs],txt) )
						gRecs++;
				}					
#ifdef REC_WPNAME_VC
				if (gRecs == 0)	SC_message("no VC recover place defined!");
#endif
#ifdef REC_WPNAME_US
				if (gRecs == 0)	SC_message("no US recover place defined!");
#endif
#ifdef MUL_REC_WPNAME_VC
				if (gRecs == 0)	SC_message("no VC recover place defined!");
#endif
#ifdef MUL_REC_WPNAME_US
				if (gRecs == 0)	SC_message("no US recover place defined!");
#endif


				CLEAR(gRecTimer);

				gRespawnGroup = 0;
				bRespawnGroup = FALSE;
				SC_sgi(GVAR_RESPAWN_GROUP, gRespawnGroup);

			}// if (info->param1)
		}//if (info->param2)
//---------------------------------pridano
#ifdef NUM_BOMBS
				for (i = 0; i < NUM_BOMBS; i++)
				{
					SC_MP_Gvar_SetSynchro(GVAR_BOMBSTATUS__+i*2);
					SC_sgi(GVAR_BOMBSTATUS__+i*2, BOMB_STATUS_INACTIVE);
				}
#endif //NUM_BOMBS
//---------------------------------------

		if (info->param1)
		{
#ifdef OPP_ATTACK
			dwDoExplosion = 0;
#endif

			//!!! ++ Reinit AI
			num = 64;
			SC_MP_EnumPlayers(plList, &num, OPP_SIDE);
			for (i = 0; i < num; i++) {
				SC_P_ScriptMessage(plList[i].id, SCM_MP_REINIT, 0);
			}
			//-- Reinit AI
#ifdef FLYBY_ANIM
			endtime=SC_ANM_GetFrameTime(FLYBY_ANIM,FLYBY_ANIM_END);
			animtime=SC_ANM_GetFrameTime(FLYBY_ANIM,FLYBY_ANIM_START);
			SC_SetViewAnim(FLYBY_ANIM, FLYBY_ANIM_START, FLYBY_ANIM_END + 10, FLYBY_ANIM_CALLB);
#endif
		}
		break;// SC_NET_MES_LEVELINIT


	case SC_NET_MES_RENDERHUD:
		switch(SC_ggi(GVAR_GPHASE))
		{
			case GPHASE_DONE:

				if (bombsExploded) {
					j = 1077 + COOP_SIDE_INDEX;
					break;
				}

				if (COOP_SIDE_INDEX == 0)	
					j = 1099;
				else
					j = 1049;

#ifdef OPP_ATTACK
				if (!SC_ggi(GVAR_OPP_WON))
					j = 1099;
				else
					j = 1049;		//OPP won
#endif
				break;

			case GPHASE_FAILED:
				if (COOP_SIDE_INDEX == 0)
					j = 1049;
				else
					j = 1099;
				break;

			default:
				j = 0;
				break;
		}// switch(SC_ggi(GVAR_GPHASE))

		if (j) {
			itxt = SC_Wtxt(j);
			SC_GetScreenRes(&val,NULL);

			val -= SC_Fnt_GetWidthW(itxt,1); 

			SC_Fnt_WriteW(val * 0.5f, 15, itxt, 1, 0xffffffff);
		} else {
			if (bombsExploded == TRUE) {
				bombsExploded = FALSE;
				gShowTimer = SHOW_TIME;
			}
		}

		break;


	case SC_NET_MES_SERVER_RECOVER_TIME:
		if (info->param2) {
			info->fval1 = 0.1f;
		} else {
			// killed
			SC_P_GetInfo(info->param1,&plinfo);	
							
			if (plinfo.side == COOP_SIDE) {		//zmeneno
				if (gRecoverLimit > 0) {
					if (gRecoverTime >= 0xffff) {
						info->fval1 = -1.0f;
					} else if (gRecoverTime>0) {
						info->fval1 = gNextRecover;
					} else {
						info->fval1 = 4.0f;
					}
				} else {
					info->fval1 = -1.0f;
				}
			} else {
				info->fval1 = -1.0f;
			}
		}
		break;


	case SC_NET_MES_SERVER_RECOVER_PLACE:
		if (info->param1 != 1)
		{
			SC_message("No recover for this side");
			break;
		}
		if (bRespawnGroup) {
			set_recovers();
			bRespawnGroup = FALSE;
		}
		precov = (s_SC_MP_Recover*)info->param2;

		i = SC_MP_SRV_GetBestDMrecov(gRec, gRecs, gRecTimer, NORECOV_TIME);
		
		gRecTimer[i] = NORECOV_TIME;
		*precov = gRec[i];
		break;
		

	case SC_NET_MES_MESSAGE:
			if ((info->param1==0)/*&&(info->param2==0)*/){
				SC_P_GetInfo(SC_PC_Get(),&plinfo);
				if (plinfo.side == COOP_SIDE)
					SC_sgi(GVAR_BOMBSTATUS__+info->param2*2,BOMB_STATUS_ACTIVE);
				else
					SC_sgi(GVAR_BOMBSTATUS__+info->param2*2,BOMB_STATUS_DEFUSED);
						
			}// if ((info->param1==0)&&(info->param2==0))

			if ((info->param1 == 100) && (gRespawnGroup < info->param2)) {
				bRespawnGroup = TRUE;
				gRespawnGroup = info->param2;
				SC_sgi(GVAR_RESPAWN_GROUP, gRespawnGroup);
			}

			break;


	case SC_NET_MES_SERVER_KILL:
		break;// SC_NET_MES_SERVER_KILL


	case SC_NET_MES_RESTARTMAP:
#ifdef NUM_BOMBS
		for (i = 0; i < NUM_BOMBS; i++)	SC_sgi(GVAR_BOMBSTATUS__+i*2, BOMB_STATUS_INACTIVE);
#endif //NUM_BOMBS
		reinitAll();
		//bRestart = 1;
		break;// SC_NET_MES_RESTARTMAP


	case SC_NET_MES_RULESCHANGED:			
		gEndRule = info->param1;
		gEndValue = info->param2;
		gTime = 0.0f;
		break;
		

				
	}// switch(info->message)
	

	return 1;

}// int ScriptMain(void)
