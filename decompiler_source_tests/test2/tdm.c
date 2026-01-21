/*
	Eric multiplayer script - TDM
*/

#include <inc\sc_global.h>
#include <inc\sc_def.h>


#define RECOVER_TIME	5.0f		// time to recover player after killed
#define NORECOV_TIME	3.0f		// disable time of recoverplace after recovering someone there


#define REC_WPNAME		"DM%d"
#define REC_MAX			64


#define GVAR_SIDE0FRAGS				500
#define GVAR_SIDE1FRAGS				501



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

	}// switch(gEndRule)

	return FALSE;

}// void SRV_CheckEndRule(float time)




void UpdateSideFrags(void){
	SC_sgi(GVAR_SIDE0FRAGS,gSideFrags[0]);
	SC_sgi(GVAR_SIDE1FRAGS,gSideFrags[1]);
}


int ScriptMain(s_SC_NET_info *info){
	char txt[32];
	dword i,j,sideA,sideB;
	s_SC_MP_Recover *precov;
	s_SC_MP_hud hudinfo;
	s_SC_P_getinfo plinfo;
	s_SC_HUD_MP_icon icon[2];
	s_SC_MP_EnumPlayers enum_pl[64];
	s_SC_MP_SRV_settings SRVset;

	switch(info->message){
		
		case SC_NET_MES_SERVER_TICK:	
			
			if (SRV_CheckEndRule(info->elapsed_time)) break;

			
			for (i=0;i<gRecs;i++)
				gRecTimer[i] -= info->elapsed_time;


			j = 64;
			if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)){

				if ((j==0)&&((gSideFrags[0]+gSideFrags[1])!=0)){
					gSideFrags[0] = 0;
					gSideFrags[1] = 0;
					UpdateSideFrags();
				}// if ((side[0]+side[1])==0)

			}// if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL))

			gPlayersConnected = j;


			break;

		case SC_NET_MES_CLIENT_TICK:

			gCLN_SideFrags[0] = SC_ggi(GVAR_SIDE0FRAGS);
			gCLN_SideFrags[1] = SC_ggi(GVAR_SIDE1FRAGS);

			SC_MP_SetSideStats(0,gCLN_SideFrags[0],0);
			SC_MP_SetSideStats(1,gCLN_SideFrags[1],0);

			for (i=0;i<2;i++){
				icon[i].type = SC_HUD_MP_ICON_TYPE_NUMBER;
				icon[i].icon_id = 3*i;
				icon[i].value = gCLN_SideFrags[i];
				icon[i].color = 0xffffffff;
			}

			SC_MP_SetIconHUD(icon,2);

			break;// SC_NET_MES_CLIENT_TICK


		case SC_NET_MES_LEVELPREINIT:
			SC_sgi(GVAR_MP_MISSIONTYPE,GVAR_MP_MISSIONTYPE_TDM);

			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;

			SC_MP_EnableBotsFromScene(FALSE);

			break;// SC_NET_MES_LEVELPREINIT

		case SC_NET_MES_LEVELINIT:
			
			SC_MP_SRV_SetForceSide(0xffffffff);
			SC_MP_SetChooseValidSides(3);

			SC_MP_SRV_SetClassLimitsForDM();


			CLEAR(hudinfo);
			hudinfo.title = 1051;
			
			hudinfo.sort_by[0] = SC_HUD_MP_SORTBY_FRAGS;
			hudinfo.sort_by[1] = SC_HUD_MP_SORTBY_KILLS;
			hudinfo.sort_by[2] = SC_HUD_MP_SORTBY_DEATHS | SC_HUD_MP_SORT_DOWNUP;
			hudinfo.sort_by[3] = SC_HUD_MP_SORTBY_PINGS | SC_HUD_MP_SORT_DOWNUP;

			hudinfo.pl_mask = SC_HUD_MP_PL_MASK_FRAGS | SC_HUD_MP_PL_MASK_KILLS | SC_HUD_MP_PL_MASK_DEATHS;
			hudinfo.use_sides = TRUE;
			hudinfo.side_name[0] = 1010;
			hudinfo.side_color[0] = 0x440000ff;
			hudinfo.side_name[1] = 1011;
			hudinfo.side_color[1] = 0x44ff0000;

			hudinfo.side_mask = SC_HUD_MP_SIDE_MASK_FRAGS;
			

			SC_MP_HUD_SetTabInfo(&hudinfo);

			SC_MP_AllowStPwD(TRUE);
			SC_MP_AllowFriendlyFireOFF(TRUE);
			SC_MP_SetItemsNoDisappear(FALSE);

			if (info->param2){

				if (info->param1){
					// it's server		

					SC_MP_GetSRVsettings(&SRVset);
					SC_MP_SRV_InitWeaponsRecovery((float)SRVset.dm_weap_resp_time);
					
					SC_MP_Gvar_SetSynchro(GVAR_SIDE0FRAGS);
					SC_MP_Gvar_SetSynchro(GVAR_SIDE1FRAGS);
					UpdateSideFrags();
					
					gRecs = 0;

					for (i=0;i<REC_MAX;i++){		
						sprintf(txt,REC_WPNAME,i);			
						if (SC_NET_FillRecover(&gRec[gRecs],txt)) gRecs++;
					}					

#if _GE_VERSION_ >= 133

					i = REC_MAX - gRecs;
					SC_MP_GetRecovers(SC_MP_RESPAWN_DM,&gRec[gRecs],&i);
					gRecs += i;
#endif
					SC_Log(3,"TDM respawns: %d",gRecs);


					if (gRecs==0) SC_message("no recover place defined!");

					CLEAR(gRecTimer);					

				}// if (info->param1)

			}//if (info->param2)


			break;// SC_NET_MES_LEVELINIT


		case SC_NET_MES_RENDERHUD:


			break;

		case SC_NET_MES_SERVER_RECOVER_TIME:

			if (info->param2){
					info->fval1 = 0.1f;
			}
			else{
				// killed
				info->fval1 = RECOVER_TIME;
			}

			break;

		case SC_NET_MES_SERVER_RECOVER_PLACE:
			
			precov = (s_SC_MP_Recover*)info->param2;

			i = SC_MP_SRV_GetBestDMrecov(gRec,gRecs,gRecTimer,NORECOV_TIME);
			
			gRecTimer[i] = NORECOV_TIME;
			*precov = gRec[i];
						
			break;
			

		case SC_NET_MES_SERVER_KILL:

			SC_P_GetInfo(info->param1,&plinfo);		
			sideA = plinfo.side;

			if (info->param2){
				SC_P_GetInfo(info->param2,&plinfo);		
				sideB = plinfo.side;
			}
			else sideB = 0xffffffff;

			if (sideA==sideB){
				gSideFrags[sideB]--;
			}
			else{
				if (sideB!=0xffffffff) gSideFrags[sideB]++;					
			}

			UpdateSideFrags();
			

			break;// SC_NET_MES_SERVER_KILL

		case SC_NET_MES_RESTARTMAP:

			gTime = 0;

			CLEAR(gSideFrags);
			UpdateSideFrags();

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
