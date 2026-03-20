/*
*	level.c
*
*	Ptero-Engine-II Script : Pilot
*	
*	M.Janacek 1.7.2002
*/


#include <inc\sc_global.h>
#include <inc\sc_def.h>

#include "sound.inc"

// SGI_LEVELPHASE
//	0 - mission start
//	1 - player out of heli
//	2 - pilot found
//	3 - welcome said
//	4 - extraction radio enabled
//	5 - extraction comm done
//	6 - waiting for heli
//	7 - enter possible
//	8 - pilot and pc in heli - fly out !


#define PILOT_PH_DISABLED				0
#define PILOT_PH_NOACTIVE				1
#define PILOT_PH_ACTIVE					2
#define PILOT_PH_FOUND					4


dword gphase = 0;
dword g_dialog = 0;
dword g_will_group[4] = {3,2,1,4};
BOOL g_dochange = TRUE;
float g_final_enter_timer = 0.0f;

c_Vector3 g_will_pos[4];
BOOL g_vill_visited[4] = {FALSE,FALSE,FALSE,FALSE};
dword g_pilot_phase = PILOT_PH_DISABLED;	// PILOT_PH_xxxx
float g_pilot_timer = 0.0f;
dword g_pilot_vill_nr = 0xff;

float g_showinfo_timer = 0.0f;
BOOL g_trashes_enabled = FALSE;

c_Vector3 gShot_pos;
//float gShot_timer;

float gEndTimer;

float gPilotCommTime = 0.0f;

BOOL g_save[2];
BOOL g_music[2];
float gStartMusicTime = 0.0f;

void DisapearAttackers(void){
	dword i,pl;
	c_Vector3 pos;

	SC_sgi(SGI_LEVPILOT_HELI3_ATTACK,0);

	CLEAR(pos);
	pos.z = -20000;

	for (i=0;i<16;i++){

		pl = SC_P_GetBySideGroupMember(1,9,i);

		if ((pl)&&(SC_P_IsReady(pl))){
			// remove no-death players
			SC_P_SetActive(pl,FALSE);
			SC_P_SetPos(pl,&pos);
		}

	}// for (i)

}// void DisapearAttackers(void)

void ActivatePatrolsAndSnipers(void){
	dword i,j,pl;

	for (j=0;j<12;j++)
		if (j!=9)	// attackers
			for (i=0;i<16;i++){

				pl = SC_P_GetBySideGroupMember(1,j,i);

				if (pl) SC_P_SetActive(pl,TRUE);
			}// for (i)

	// villagers and paesants
	for (j=0;j<16;j++){
		pl = SC_P_GetBySideGroupMember(3,0,j);
		if (pl) SC_P_SetActive(pl,TRUE);
	}// for (i)


}// void ActivatePatrolsAndSnipers(void)

dword GetPilot(void){
	return SC_P_GetBySideGroupMember(SC_P_SIDE_NEUTRAL,0,1);
}

dword GetGroupMembers(dword group_id, dword max_players){
	dword i,ret,pl;

	ret = 0;

	for (i=0;i<max_players;i++){
		pl = SC_P_GetBySideGroupMember(1,group_id,i);		
		if (SC_P_IsReady(pl)) ret++;		
	}//for (i)

	return ret;

}// dword GetGroupMembers(dword group_id, dword max_players)


void GetFarestWills(dword pl_id, dword *list){
	c_Vector3 pos;
	float dist[2],val;
	dword i;


	SC_P_GetPos(pl_id,&pos);
	CLEAR(dist);

	for (i=0;i<4;i++){
		val = SC_2VectorsDist(&pos,&g_will_pos[i]);
		if (val>dist[0]){

			dist[1] = dist[0];
			list[1] = list[0];

			dist[0] = val;
			list[0] = i;
		}
		else
		if (val>dist[1]){
			dist[1] = val;
			list[1] = i;
		}

	}// for (i)	

}
	
	

void DoTick_Willages(float time){
	dword i,w;	
	dword list[2];
	c_Vector3 pl_pos,vec;
	float dist;

	
	// check villages visit

	if (g_pilot_phase==PILOT_PH_DISABLED){

		SC_PC_GetPos(&pl_pos);

		for (i=0;i<4;i++)
			if (!g_vill_visited[i]){

				if (SC_IsNear2D(&g_will_pos[i],&pl_pos,80.0f)){
					g_vill_visited[i] = TRUE;					
				}

			}// for (i=0;i<4;i++) if (!g_vill_visited[i])


		w = 0;
		for (i=0;i<3;i++)
			if (g_vill_visited[i]) w++;

		if ((w>1)&&(g_vill_visited[3])){
		//if (w>0){
			// 2 villages and vill4 is visited			
			g_pilot_phase = PILOT_PH_NOACTIVE;
			g_pilot_timer = 30 + frnd(10.0f);
		}

	}// if (g_pilot_phase==PILOT_PH_DISABLED){


	switch(g_pilot_phase){

		case PILOT_PH_NOACTIVE:
			g_pilot_timer -= time;
			if (g_pilot_timer<=0.0f){
				g_pilot_phase = PILOT_PH_ACTIVE;
				GetFarestWills(SC_PC_Get(),list);
				
				g_pilot_vill_nr = list[rand()%2];												

				SC_P_ScriptMessage(GetPilot(),0,g_pilot_vill_nr);	

				g_pilot_timer = 210.0f + frnd(30.0f);

				SC_SpeechRadio2(3463 + 2*g_pilot_vill_nr + rand()%2,NULL);

				SC_HUD_RadarShowPlayer(GetPilot(),0xff00ff00);

			}
			break;// case PILOT_PH_NOACTIVE

		case PILOT_PH_ACTIVE:

			g_pilot_timer -= time;

			if (g_pilot_timer<0.0f){

				g_pilot_phase = PILOT_PH_NOACTIVE;
				g_pilot_timer = 30 + frnd(10.0f);				

				g_pilot_vill_nr = 0xff;				

				SC_P_ScriptMessage(GetPilot(),0,g_pilot_vill_nr);	

				SC_HUD_RadarShowPlayer(0,0);

			}// if (g_pilot_timer<0.0f)
			else{

				// check found him

				SC_PC_GetPos(&pl_pos);

				SC_P_GetPos(GetPilot(),&vec);
				
				if (SC_IsNear2D(&pl_pos,&vec,50.0f)){					
					g_pilot_phase = PILOT_PH_FOUND;
					g_pilot_timer = 0.0f;

					SC_SetSideAlly(SC_P_SIDE_VC,SC_P_SIDE_NEUTRAL,-1.0f);
					SC_sgi(SGI_LEVELPHASE,2);					

				}

			}

			break;// case PILOT_PH_ACTIVE



		case PILOT_PH_FOUND:

				if (SC_ggi(SGI_LEVELPHASE)>5) break;

				g_pilot_timer -= time;
				if (g_pilot_timer<=0.0f){

					g_pilot_timer = 1.5f;
							
					dist = SC_P_GetDistance(GetPilot(),SC_PC_Get());

					if (dist>15){
						SC_PC_GetPos(&vec);					
						SC_P_Ai_Go(GetPilot(),&vec);
					}
					else
						if (dist<8) SC_P_Ai_Stop(GetPilot());
				

				}// if (g_pilot_timer<=0.0f)				

				break;// case PILOT_PH_FOUND:


	}// switch(g_pilot_phase)

	//SC_Osi("phase: %d  timer: %2.2f vill: %d",g_pilot_phase,g_pilot_timer,g_pilot_vill_nr);

}// void DoTick_Willages(float time)


void SetPlRun(dword pl_id){

	SC_P_Ai_SetMoveMode(pl_id,SC_P_AI_MOVEMODE_RUN);
	SC_P_Ai_SetMovePos(pl_id,SC_P_AI_MOVEPOS_STAND);

}// void SetPlRun(dword pl_id)


void ShowTrashes(BOOL enable){
	void *nod;

	g_trashes_enabled = enable;

	nod = SC_NOD_Get(NULL,"maj_uh-1d_vreck");

	if (nod) SC_DUMMY_Set_DoNotRenHier2(nod,!enable);

/*
	SC_EventEnable("Event#10",enable);	
	SC_EventEnable("Event#9",enable);	
	SC_EventEnable("Event#5",enable);	
	SC_EventEnable("Event#15",enable);	
	SC_EventEnable("Event#7",enable);	
	SC_EventEnable("Event#14",enable);	
	SC_EventEnable("Event#11",enable);	
	SC_EventEnable("Event#4",enable);	
	SC_EventEnable("Event#12",enable);	
	SC_EventEnable("Event#8",enable);	
	SC_EventEnable("Event#3",enable);	
	SC_EventEnable("Event#6",enable);	
	SC_EventEnable("Event#13",enable);	
	SC_EventEnable("Event#16",enable);	
	SC_EventEnable("Event#17",enable);	
	SC_EventEnable("Event#19",enable);	
	SC_EventEnable("Event#18",enable);	
	SC_EventEnable("Event#1",enable);	
	SC_EventEnable("Event#2",enable);	
*/

}// void ShowTrashes(BOOL enable)




void DecideReward(void){
	s_SC_MP_EnumPlayers list[64];
	dword items;

	items = 64;
	
	SC_sgi(SGI_DEBRIEF_PILOT_REWARDED,0);
	SC_sgi(SGI_REWARD_PILOT,1);
	

	if (SC_MP_EnumPlayers(list,&items,1)){
		if (items>0){
			SC_sgi(SGI_DEBRIEF_PILOT_REWARDED,DEBR_DONTSHOW);
			SC_sgi(SGI_REWARD_PILOT,0);
		}
	}
}


int ScriptMain(s_SC_L_info *info){
	float fl,dist,fl2;
	int intik;
	s_SC_initside initside;
	s_SC_initgroup initgroup;
	c_Vector3 vec,plpos,movdir;
	dword i,pl,pc,pilot,crocker,hornster,pilot_h1,defort;
	s_SC_SpeachBreakProps props;	
	s_SC_Ai_PlFollow fol[4];
	dword fol_ord[4];
	char txt[32];
	s_SC_P_getinfo plinfo;
	s_SC_MissionSave savinfo;	
	s_SC_Objective objective[2];

	AdjustGameSound(info->elapsed_time);

	switch(info->message){

		case SC_LEV_MES_TIME:


			pilot = GetPilot();
			

			if (pilot){
				SC_P_GetInfo(pilot,&plinfo);
				if (plinfo.cur_hp<=0.0f){
					SC_MissionFailed();
					break;
				}
			}

			info->next_exe_time  = 0.2f;


			if (g_showinfo_timer<11.0f){

				fl = g_showinfo_timer;
				g_showinfo_timer += info->elapsed_time;

				if ((fl<4.0f)&&(g_showinfo_timer>=4.0f)){

					fol_ord[0] = 0;
					fol_ord[1] = 3490;//"17.12. 1967 8:00";
					fol_ord[2] = 3491;//"Ricefields around Khe Bana river";
					SC_ShowMovieInfo(fol_ord);
				}

				if ((fl<10.5f)&&(g_showinfo_timer>=10.5f)){
					SC_ShowMovieInfo(NULL);
				}
			}//if (g_showinfo_timer<11.0f)
						

			switch(gphase){

			case 0:

				//SC_SetMapFpvModel("G\\WEAPONS\\Vvh_map\\VvH_map_fpv_conq.bes");				

				initside.MaxHideOutsStatus = 32;
				initside.MaxGroups = 4;
				SC_InitSide(SC_P_SIDE_US,&initside);

				initgroup.SideId = SC_P_SIDE_US;
				initgroup.GroupId = 0;
				initgroup.MaxPlayers = 16;
				initgroup.NoHoldFireDistance = 100.0f;
				SC_InitSideGroup(&initgroup);

				initgroup.SideId = SC_P_SIDE_US;
				initgroup.GroupId = 1;				// pulaski
				initgroup.MaxPlayers = 2;
				initgroup.NoHoldFireDistance = 100.0f;
				SC_InitSideGroup(&initgroup);

				initgroup.SideId = SC_P_SIDE_US;
				initgroup.GroupId = 2;				// all helis crew
				initgroup.MaxPlayers = 16;
				initgroup.NoHoldFireDistance = 100.0f;
				SC_InitSideGroup(&initgroup);

				initside.MaxGroups = 12;
				SC_InitSide(1,&initside);

				for (i=0;i<12;i++){
					initgroup.SideId = SC_P_SIDE_VC;
					initgroup.GroupId = i;
					initgroup.MaxPlayers = 16;
					initgroup.NoHoldFireDistance = 100.0f;
					SC_InitSideGroup(&initgroup);
				}


				initside.MaxHideOutsStatus = 2;
				initside.MaxGroups = 2;
				SC_InitSide(SC_P_SIDE_NEUTRAL,&initside);

				
				initgroup.SideId = SC_P_SIDE_NEUTRAL;
				initgroup.GroupId = 0;
				initgroup.MaxPlayers = 1;
				initgroup.NoHoldFireDistance = 100.0f;
				SC_InitSideGroup(&initgroup);

				initgroup.SideId = SC_P_SIDE_NEUTRAL;
				initgroup.GroupId = 1;
				initgroup.MaxPlayers = 20;
				initgroup.NoHoldFireDistance = 0.0f;
				SC_InitSideGroup(&initgroup);

				SC_SetSideAlly(SC_P_SIDE_US,SC_P_SIDE_NEUTRAL,1.0f);
				SC_SetSideAlly(SC_P_SIDE_VC,SC_P_SIDE_NEUTRAL,1.0f);

				
				initside.MaxHideOutsStatus = 2;
				initside.MaxGroups = 1;
				SC_InitSide(3,&initside);
				
				initgroup.SideId = 3;
				initgroup.GroupId = 0;
				initgroup.MaxPlayers = 16;
				initgroup.NoHoldFireDistance = 0.0f;
				SC_InitSideGroup(&initgroup);

				SC_SetSideAlly(SC_P_SIDE_US,3,0.0f);
				SC_SetSideAlly(SC_P_SIDE_VC,3,1.0f);
				SC_SetSideAlly(SC_P_SIDE_NEUTRAL,3,0.0f);


				ShowTrashes(FALSE);

				gphase = 1;
				

				SC_sgi(SGI_LEVPILOT_S1G0,0);								
				SC_sgi(SGI_LEVPILOT_S1G1,0);
				SC_sgi(SGI_LEVPILOT_S1G2,0);
				SC_sgi(SGI_LEVPILOT_S1G3,0);
				SC_sgi(SGI_LEVPILOT_S1G4,0);
				
				
				for (i=0;i<4;i++){
					CLEAR(fol[i].follow_change);
					fol[i].min_dist = 1.5f;
					fol[i].max_dist = 5.0f;

					fol_ord[i] = i;
				}

				for (i=0;i<10;i++)
					SC_Ai_SetPlFollow(1,i,SC_AI_FOLLOWMODE_POINT,fol,fol_ord,fol_ord,4);

				for (i=0;i<4;i++){
					sprintf(txt,"WP_will%d",i+1);
					SC_GetWp(txt,&g_will_pos[i]);
				}
				


				SC_sgi(SGI_LEVELPHASE,0);

				SC_sgi(SGI_LEVPILOT_HELI3_ATTACK,0);

				SC_sgi(SGI_LEVPILOT_JUSTLOADEDVALUE,0);

				SC_RadioSetDist(10.0f);				

				CLEAR(g_save);
				CLEAR(g_music);

				

				SC_ArtillerySupport(FALSE);	

				SC_SetViewAnim("g\\camanims\\CAMERA\\Pilot_in.anm",0,350,0);

				SC_FadeTo(TRUE, 0);
				SC_FadeTo(FALSE, 3.0f);


				break;
			case 1:				

				i = SC_ggi(SGI_LEVELPHASE);



				if (!g_save[0]){
					pc = SC_P_GetBySideGroupMember(0,0,0);
					if ((pc)&&(SC_P_IsReady(pc))){						
						g_save[0] = TRUE;
						savinfo.savename_id = 9136;
						savinfo.description_id = 9137;
						SC_MissionSave(&savinfo);
											

					}
				}
				
				
				if (!g_music[0]){

					if (gStartMusicTime>0.0f){
						gStartMusicTime -= info->elapsed_time;
						if (gStartMusicTime<=0.0f){					
							g_music[0] = TRUE;
							SetAGS(AGS_LEVBEGIN);
						}
					}					
				}

				switch(i){

					case 0:
						// in heli
						switch(g_dialog){

							// first dialog
							case 0:
																			
								fl = 0.5f;

								SC_SpeechRadio2(3400,&fl);fl += 0.3f;
								SC_SpeechRadio2(3401,&fl);fl += 0.3f;
								SC_SpeechRadio2(3402,&fl);fl += 0.5f;
								SC_SpeechRadio2(3403,&fl);fl += 0.3f;
								SC_SpeechRadio2(3404,&fl);fl += 0.5f;

								g_dialog = 1;

								break;

							case 1:
								// wait for hit to heli3
								if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK)<1) break;

								crocker = SC_P_GetBySideGroupMember(0,0,SC_P_MEMBERID_MEDIC); 							
								hornster = SC_P_GetBySideGroupMember(0,0,SC_P_MEMBERID_MACHINEGUN); 								
								defort = SC_P_GetBySideGroupMember(0,0,SC_P_MEMBERID_RADIO); 

								fl = 3.0f;
								SC_P_Speech2(crocker,3420,&fl);
								fl = 3.2f;
								SC_P_Speech2(hornster,3421,&fl);

								g_dialog = 2;									
								break;

							case 2:
								if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK)<2) break;

								pilot_h1 = SC_P_GetBySideGroupMember(0,2,1); 

								fl = 1.0f;
								SC_P_Speech2(pilot_h1,3422,&fl);fl += 0.3f;
								SC_P_Speech2(SC_P_GetBySideGroupMember(0,0,0),3423,&fl);fl += 0.4f;								

								SC_P_Speech2(pilot_h1,3422,&fl);fl += 0.3f;


								SC_SpeechRadio2(3416,&fl);fl += 0.5f;
								SC_SpeechRadio2(3417,&fl);fl += 0.5f;
								SC_SpeechRadio2(3418,&fl);fl += 0.5f;

								SC_P_Speech2(pilot_h1,3419,&fl);fl += 2.0f;							

								fl2 = fl - 1.2f;
								SC_P_Speech2(SC_P_GetBySideGroupMember(0,0,0),3430,&fl2);fl2 += 1.5f;
								SC_P_Speech2(hornster,3431,&fl);

								SC_SpeechRadio2(3424,&fl);fl += 0.5f;								
								SC_SpeechRadio2(3425,&fl);fl += 0.5f;
								SC_SpeechRadio2(3426,&fl);fl += 0.5f;
								SC_SpeechRadio2(3427,&fl);fl += 0.5f;
								SC_SpeechRadio2(3428,&fl);fl += 0.5f;
								SC_SpeechRadio2(3429,&fl);fl += 0.5f;

								g_dialog = 3;
								break;

							case 3:
								if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK)<3) break;
								
								fl = 0.0f;
								SC_SpeechRadio2(3440,&fl);fl += 0.5f;
								SC_SpeechRadio2(3441,&fl);fl += 0.5f;
								SC_SpeechRadio2(3442,&fl);fl += 0.5f;
								SC_SpeechRadio2(3443,&fl);fl += 0.5f;
								SC_SpeechRadio2(3444,&fl);fl += 0.5f;
								SC_SpeechRadio2(3445,&fl);fl += 0.5f;
								SC_SpeechRadio2(3446,&fl);fl += 0.5f;
								
								g_dialog = 4;

								break;

							case 4:
								if (SC_ggi(SGI_LEVPILOT_HELI3_ATTACK)<4) break;
								
								g_dialog = 5;

								pilot_h1 = SC_P_GetBySideGroupMember(0,2,1); 
								pc = SC_P_GetBySideGroupMember(0,0,0);

								fl = 0.0f;
								SC_P_Speech2(pilot_h1,3447,&fl);fl += 0.3f;
								SC_P_Speech2(pc,3448,&fl);fl += 0.6f;
								SC_P_Speech2(pilot_h1,3449,&fl);fl += 0.3f;
								info->next_exe_time  = fl-1.0f; 
								SC_P_Speech2(pc,3450,&fl);

								break;

							case 5:
								SC_PC_EnableExit(TRUE);
								g_dialog = 6;
								break;
								

						}// switch(g_dialog)
						



						break;

					case 1:
						// searching for pilot

						if (g_dochange){
							DisapearAttackers();
							ActivatePatrolsAndSnipers();
							g_dochange = FALSE;

							if (!g_save[1]){
								g_save[1] = TRUE;
								savinfo.savename_id = 9138;
								savinfo.description_id = 9139;
								SC_MissionSave(&savinfo);						
							}

						}

						DoTick_Willages(info->elapsed_time);

						break;


					case 2:

						DoTick_Willages(info->elapsed_time);

						// pilot found						;
						pc = SC_P_GetBySideGroupMember(0,0,0);

						if ((pilot)&&(pc)
							&&(SC_P_GetActive(pilot))
							&&(SC_P_IsReady(pilot))
							&&(SC_P_IsReady(pc))){

							dist = SC_P_GetDistance(pilot,pc);
							if (dist<10.0f){
								SC_sgi(SGI_LEVELPHASE,3);

								fl = 0.0f;
								SC_P_Speech2(pc,3451,&fl);fl+=1.6f;
								SC_P_Speech2(pilot,3452,&fl);fl+=0.5f;
								SC_P_Speech2(pc,3453,&fl);

								info->next_exe_time = fl;								

								objective[0].text_id = 3471;
								objective[0].status = SC_OBJECTIVE_STATUS_COMPLETE;

								//objective[1].text_id = 3472;
								//objective[1].status = SC_OBJECTIVE_STATUS_VALID;

								SC_SetObjectives(1,objective,0.0f);


							}

						}

						break;// case 2

					case 3:
						SC_Radio_Enable(20);
						SC_PC_EnableRadioBreak(TRUE);
						SC_sgi(SGI_LEVELPHASE,4);
						break;
					case 4:
						// waiting for pc uses radio
						break;
					case 5:
						// waiting to pilot reaches some village

						if (gPilotCommTime>0.0f){
							gPilotCommTime -= info->elapsed_time;
							break;
						}

						DoTick_Willages(info->elapsed_time);
						
						SC_P_GetPos(pilot,&vec);

						for (i=0;i<4;i++){
							if (SC_2VectorsDist(&vec,&g_will_pos[i])<40.0f){
								SC_sgi(SGI_LEVELPHASE,6);
								SC_sgi(SGI_LEVPILOT_EVACVILLID,i);
								
								vec.z += 1.5f;

								movdir.x = g_will_pos[i].x - vec.x;
								movdir.y = g_will_pos[i].y - vec.y;
								movdir.z = 0.0f;
								fl = SC_VectorLen(&movdir) / 10.0f;	// 5.0f is xy speed								

								movdir.x /= fl;
								movdir.y /= fl;
								movdir.z = 7.0f;
								
								SC_Item_Create2(147,&vec,&movdir);

								// run heli
								break;
							}

						}// for (i)

						break;
					case 6:
						// waiting for heli
						DoTick_Willages(info->elapsed_time);
						break;

					case 7:
						// enter enabled						
						i = 2;	
						
						g_final_enter_timer += info->elapsed_time;

						if (!SC_P_IsInHeli(pilot)){

							if (g_final_enter_timer>30.0f) SC_P_SetToHeli(pilot,"heli2",3);
							else{
								SetPlRun(pilot);								
								SC_P_Ai_EnterHeli(pilot,"heli2",SC_CAR_ENTRY_FUNC_SEAT+2);							
								info->next_exe_time = 4.0f;
							}
						}
						else i--;						


						pc = SC_P_GetBySideGroupMember(0,0,0);
						if (SC_P_IsInHeli(pc)) i--;

						if (i==0){
							SC_sgi(SGI_LEVELPHASE,8);							
							SetAGS(AGS_LEVEND);							
							info->next_exe_time = 0.1f;	// mission succ timer							
							gEndTimer = 15;
						}				

						break;

					case 8:

						gEndTimer -= info->elapsed_time;
						if (gEndTimer<0.0f){
							DecideReward();							
							SC_MissionCompleted();
							SC_sgi(SGI_LEVELPHASE,9);
						}
						break;


				}// switch(SC_ggi(SGI_LEVELPHASE))
				
				break;


			}// switch(gphase)

			break;// SC_LEV_MES_TIME

		case SC_LEV_MES_RADIOUSED:

			switch(info->param1){

				case 20:

					SC_sgi(SGI_LEVELPHASE,5);
															
					SC_RadioBatch_Begin();
					fl = 0.0f;

					pc = SC_P_GetBySideGroupMember(0,0,0);

					SC_P_Speech2(pc,3454,&fl);fl += 1.3f;
					SC_SpeechRadio2(3455,&fl);fl += 0.5f;
					SC_P_Speech2(pc,3456,&fl);fl += 0.7f;
					SC_SpeechRadio2(3461,&fl);fl += 0.5f;
					SC_P_SpeechMes2(pc,3457,&fl,11);

					gPilotCommTime = fl + 3.0f;

					info->next_exe_time = 0.1f;

					SC_RadioBatch_End();

					break;

			}// switch(info->param1)

			break;// SC_LEV_MES_RADIOUSED

		case SC_LEV_MES_SPEACHDONE:

			switch(info->param1){
				case 11:
					SC_message("Break");
					if (gPilotCommTime>3.0f)
							gPilotCommTime = 3.0f;
					break;
			}// switch(info->param1)

			break;


		case SC_LEV_MES_EVENT:

				switch(info->param1){
					case 10:
						ShowTrashes(TRUE);
						break;
					case 667:
						// some sniper has shot
						/*
						if (SC_ggi(SGI_DIFFICULTY)<2){
							gShot_timer = 1.5f;
							SC_Log(0,"Set shoot timer");
							SC_P_GetPos(info->param2,&gShot_pos);
						}
						*/
						break;
				}// switch(info->param1)

				break;

		case SC_LEV_MES_VIEWANIMCALLBACK:

				//info->param1
				//SC_message("view callback %d",info->param1);

				break;

		case SC_LEV_MES_INITSCENE:

				SC_SetObjectScript("heli1","levels\\ricefield\\data\\pilot\\scripts\\heli1.c");
				SC_SetObjectScript("heli2","levels\\ricefield\\data\\pilot\\scripts\\heli2.c");
				SC_SetObjectScript("heli3","levels\\ricefield\\data\\pilot\\scripts\\heli3.c");

				SC_Item_Preload(147);	// smoke grenade
										
				SC_SetMapFpvModel("g\\weapons\\Vvh_map\\map_ricefield.bes");
				
				SC_sgi(SGI_CURRENTMISSION, MISSION_PILOT);
				
				SC_PreloadBES(1,"Levels\\Ricefield\\data\\Pilot\\objects\\ivq_kopac.bes");

				gStartMusicTime = 0.2f;

				break;

		case SC_LEV_MES_JUSTLOADED:		
				SC_sgi(SGI_LEVPILOT_JUSTLOADEDVALUE,SC_ggi(SGI_LEVPILOT_JUSTLOADEDVALUE) + 1);
				ShowTrashes(g_trashes_enabled);
				break;
	
		case SC_LEV_MES_GETMUSIC:

				if (info->param1>= MAX_MUSICS){
					info->param3 = 0;
				}
				else{					
					*((s_MusicDef*)info->param2) = music[info->param1];
					info->param3 = 1;
				}
				break;

	}// switch(info->message)

	/*
	if (gShot_timer>0.0f){

		if (info->elapsed_time<0.1f) gShot_timer -= 0.5f*info->elapsed_time;

		if ((gShot_timer<0.0f)||(gShot_timer>1.0f)) SC_HUD_RadarShowPos(NULL,0);
		else{			
			i = (dword)((0.5f*gShot_timer) * 255.0f);	
			i <<= 24;
			i+= 0xff0000;
			SC_HUD_RadarShowPos(&gShot_pos,i);
		}

		info->next_exe_time = 0.01f;

	}// if (gShot_timer>0.0f)
	*/

	return 1;

}// int ScriptMain(void)






