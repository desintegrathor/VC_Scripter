#line 0 "C:\Users\flori\source\repos\VC_Scripter\original-resources\compiler\tt.c"
 



#line 0 "C:\Users\flori\source\repos\VC_Scripter\original-resources\compiler\inc\sc_MPglobal.h"
 
















	




































													
													
													
													
												
												
												

												
												
												





												
												










												




												
												
														





												
												



												
												

























































































































































	typedef unsigned int dword;	

	typedef unsigned short ushort;	


	typedef int BOOL;
	
	typedef struct {
		float x,y,z;
	}c_Vector3;
	
	typedef struct{
		c_Vector3 pos;
		float rad;
	}s_sphere;


	extern int sprintf(char *, const char *, ...);
	extern int swprintf(ushort *, ushort*, ...);
	extern int rand(void);
	extern float frnd(float max);
	extern float sqrt(float val);
	extern float fmod(float a, float b);

	extern float sin(float a);
	extern float cos(float a);
	extern float atan2(float y, float x);


	


typedef struct{	
	char *bes;
	char *eqp;
}s_SC_P_CreateEqp;

typedef struct{	
	dword type;
	dword side;
	dword group;
	dword member_id;
	dword name_nr;
	dword debrief_group;	
	char *inifile;
	void *recover_pos;	
	char *icon_name;

	dword flags;		

	dword weap_knife;
	dword weap_pistol;
	dword weap_main1;
	dword weap_main2;	
	dword weap_slot1;	

	dword weap_slot6;
	dword weap_slot7;
	dword weap_slot8;
	dword weap_slot9;
	dword weap_slot10;	

	dword force_sel_slot;	

	dword eqps;
	s_SC_P_CreateEqp *eqp;

	dword aeg_valid_head_bes[8];
	dword aeg_valid_body_bes[8];

}s_SC_P_Create;


typedef struct{	
	dword message,param1,param2,param3;
	float elapsed_time;
	float next_exe_time;
	c_Vector3 param4;
}s_SC_L_info;

typedef struct{

	dword MaxHideOutsStatus;			
	dword MaxGroups;

}s_SC_initside;

typedef struct{

	dword SideId;
	dword GroupId;
	dword MaxPlayers;

	float NoHoldFireDistance;			
	float follow_point_max_distance;
	
}s_SC_initgroup;


typedef struct{

	float cur_hp,max_hp;
	dword side;
	dword group;
	dword member_id;
	
}s_SC_P_getinfo;


typedef struct{

	dword event_type;		
	void *master_nod;
	void *nod;	
	float new_hp_obtained;
	dword hit_by;			
	c_Vector3 *world_pos;
	c_Vector3 *world_dir;
	float time;				

}s_SC_OBJ_info;


typedef struct{
	c_Vector3 velocity;	
	float rot_speed;
	c_Vector3 rot_axis;
}s_SC_OBJ_dynamic;

typedef struct{
	c_Vector3 loc;
	c_Vector3 rot;
	c_Vector3 scale;
}s_SC_NOD_transform;



typedef struct{	
	dword message,param1,param2,param3;
	float elapsed_time;	
	float fval1;
}s_SC_NET_info;

 



















  



typedef struct{

	dword id;
	dword side;
	dword status;	
	char *name;

}s_SC_MP_EnumPlayers;



typedef struct{
	c_Vector3 pos;
	float rz;
}s_SC_MP_Recover;



typedef struct{

	dword title;
	BOOL use_sides;
	BOOL disableUSside;
	BOOL disableVCside;

	dword side_name[2];
	dword side_color[2];

	dword pl_mask;
	dword side_mask;
	dword sort_by[5];

}s_SC_MP_hud;







typedef struct{
	dword icon_id;  
	dword type;     
	int value;	    
	dword color;	
}s_SC_HUD_MP_icon;


typedef struct{
	dword message;		
}s_SC_SOUND_info;


typedef struct{
	dword coop_respawn_time;
	dword coop_respawn_limit;
	dword dm_weap_resp_time;
	dword atg_class_limit[6];
}s_SC_MP_SRV_settings;


typedef struct{
	float ATG_round_time;
	float tt_respawntime;
	float tt_timelimit;
}s_SC_MP_SRV_AtgSettings;




typedef struct{
	int hours;
	int minutes;
	int seconds;
	int msec;	
}s_SC_systime;




typedef struct{
	dword id;	
	dword color;
	float scale;
	c_Vector3 pos;
}s_SC_FpvMapSign;




extern void SC_sgi(dword id, int a);
extern int SC_ggi(dword id);


extern void SC_sgf(dword id, float a);
extern float SC_ggf(dword id);

extern void SC_MP_Gvar_SetSynchro(dword id);


extern void SC_ZeroMem(void *ptr, dword size);
extern float SC_GetLineDist(c_Vector3 *pos, c_Vector3 *line_a, c_Vector3 *line_b);
extern float SC_GetLineDistXY(c_Vector3 *pos, c_Vector3 *line_a, c_Vector3 *line_b);

extern BOOL SC_IsNear2D(c_Vector3 *a, c_Vector3 *b, float dist);
extern BOOL SC_IsNear3D(c_Vector3 *a, c_Vector3 *b, float dist);

extern float SC_2VectorsDist(c_Vector3 *a, c_Vector3 *b);

extern float SC_VectorLen(c_Vector3 *vec);
extern float SC_VectorLen2(c_Vector3 *vec);


extern void SC_message(char *txt,...);				
extern void SC_Log(dword level, char *txt, ...);	
extern void SC_Osi(char *txt,...);					

extern BOOL SC_StringSame(char *a, char *b);

extern void SC_EventImpuls(char *ev_name);
extern void SC_EventEnable(char *ev_name, BOOL enable);	


extern void SC_SetMissileTrace(dword color, float alpha);

extern void SC_CreatePtc(dword id, c_Vector3 *vec);
extern void SC_CreatePtc_Ext(dword id, void *nod, float time, float interval, float scale, float time_mult);
					
extern void SC_CreatePtcVec_Ext(dword id, c_Vector3 *vec, float time, float interval, float scale, float time_mult);
extern void SC_CreatePtcInNodSpace_Ext(dword id, void *nod, float time, float interval, float scale, float time_mult);
					
						
						
						
						
						

extern ushort *SC_AnsiToUni(char *src, ushort *dest);

extern void SC_Fnt_Write(float x, float y, char *txt, float scale, dword color);
extern float SC_Fnt_GetWidth(char *txt, float scale);

extern void SC_Fnt_WriteW(float x, float y, ushort *txt, float scale, dword color);
extern float SC_Fnt_GetWidthW(ushort *txt, float scale);


extern void SC_GetScreenRes(float *width, float *height);


extern void SC_RadioSetDist(float max_dist_subtitle_write);

extern void SC_DoExplosion(c_Vector3 *pos, dword type);	
														
extern void SC_ArtillerySupport(BOOL enable);
extern void SC_SetMapFpvModel(char *bes_filename);

extern void SC_SetSceneVisibilityMult(float vis_mult, float scene_fog_mult, float bckg_fog_mult);
				

extern void SC_SetObjectScript(char *obj_name, char *script_name);

extern BOOL SC_SphereIsVisible(s_sphere *sph);
extern void SC_GetPos_VecRz(void *cpos, c_Vector3 *pos, float *rz);	

extern void SC_MakeBurning(s_sphere *sph);				

extern void SC_PreloadBES(dword id, char *bes_name);	

extern void SC_GetLoudShot(s_sphere *sph);

extern float SC_GetVisibility(void);
extern float SC_GetPCZoom(void);

extern void SC_PreloadWeapon(dword type, BOOL fpv_to);
extern void SC_FadeTo(BOOL black, float time);	

extern void SC_ShowMovieInfo(dword *txt);						
																
extern void SC_HUD_DisableRadar(BOOL disable);

					
extern void SC_PreloadSound(dword snd_id, BOOL is3D);	
extern void SC_FadeSoundPlayer(dword snd_player_id, float final_volume, float fade_time);

extern ushort* SC_Wtxt(dword val);				

extern dword SC_GetNearestPlayer(c_Vector3 *vec, float *dist);

extern void SC_SwitchSceneSCS(char *fname, float time);			

extern BOOL SC_GetRndWp(s_sphere *sph, c_Vector3 *wp);			
																

extern void SC_GetCameraPos(c_Vector3 *vec);

extern void SC_GetSystemTime(s_SC_systime *info);

extern void SC_Fauna_DoSoundAlert(c_Vector3 *pos);
extern void SC_Fauna_KillThemAll(s_sphere *sph);




extern BOOL SC_PC_GetPos(c_Vector3 *pos);
extern dword SC_PC_Get(void);

extern void SC_PC_SetControl(BOOL user_control);				
extern void SC_PC_EnableMovementAndLooking(BOOL enable);	
extern void SC_PC_EnableMovement(BOOL enable);				
extern void SC_PC_EnablePronePosition(BOOL enable);			

extern void SC_PC_EnableWeaponsUsing(BOOL enable);			

extern void SC_PC_EnableExit(BOOL enable);				
extern void SC_PC_EnableEnter(BOOL enable);				

extern float SC_PC_PlayFpvAnim(char *filename);
extern float SC_PC_PlayFpvAnim2(char *filename, dword plb_id, char *eqp, char *anm);
													
													
													

extern void SC_PC_PlayFpvLooped(char *filename);	

extern void SC_PC_EnableFlashLight(BOOL enable);	




extern BOOL SC_P_IsReady(dword pl_id);					
extern char *SC_P_GetName(dword pl_id);
extern void SC_P_ChangeSideGroupMemId(dword pl_id, dword side, dword group, dword mem_id);
extern void SC_P_SetForceClassName(dword pl_id, dword name_nr);

extern BOOL SC_P_GetWeapons(dword pl_id, s_SC_P_Create *info);	



extern void SC_P_GetPos(dword pl_id, c_Vector3 *pos);
extern void SC_P_SetPos(dword pl_id, c_Vector3 *pos);
extern void SC_P_SetRot(dword pl_id, float rz);
extern float SC_P_GetRot(dword pl_id);

extern void SC_P_GetHeadPos(dword pl_id, c_Vector3 *pos);

extern void SC_P_GetDir(dword pl_id, c_Vector3 *dir);
extern void SC_P_GetInfo(dword pl_id, s_SC_P_getinfo *info);
extern void SC_P_DoKill(dword pl_id);

extern void SC_P_SetHp(dword pl_id, float hp);
extern void SC_P_Heal(dword pl_id);

extern dword SC_P_GetBySideGroupMember(dword iside, dword igroup, dword imember);

extern BOOL SC_P_HasWeapon(dword pl_id, dword weap_type);

extern BOOL SC_P_GetHasShoot(dword pl_id);		
extern dword SC_P_GetCurWeap(dword pl_id);


extern void SC_P_Link3pvEqp(dword pl_id, dword slot_id, dword plb_id, char *eqp_name);	
extern void SC_P_UnLink3pvEqp(dword pl_id, dword slot_id);								

extern void SC_P_AddAllAmmo(dword pl_id);
extern void SC_P_AddAmmoNoGrenade(dword pl_id);


extern void SC_P_ChangeWeapon(dword pl_id, dword slot_id, dword weap_type);
extern void SC_P_SetSelWeapon(dword pl_id, dword slot_id);
extern float SC_P_GetPhase(dword pl_id);     
extern void SC_P_SetPhase(dword pl_id, dword phase);     

extern float SC_P_GetDistance(dword pl_id, dword to_pl_id);

extern void SC_P_DoHit(dword pl_id, dword area_id, float hp);
extern void SC_P_SetRadarColor(dword pl_id, dword val);	
extern void SC_P_SetNoAmmo(dword pl_id);
extern void SC_P_CloseEyes(dword pl_id, BOOL force_close);

extern void SC_P_SetAmmo(dword pl_id, dword ammo_type, dword amount);

extern BOOL SC_P_UsesBinocular(dword pl_id);
extern void SC_P_EnableBinocular(dword pl_id, BOOL enable);	


extern BOOL SC_GetWp(char *wpname, c_Vector3 *vec);

extern void SC_SetSideAlly(dword s1, dword s2, float status);	
extern void SC_InitSide(dword id, s_SC_initside *init);
extern void SC_InitSideGroup(s_SC_initgroup *info);
extern dword SC_GetGroupPlayers(dword side, dword group);

extern dword SC_Item_Create(dword id, c_Vector3 *vec);						
extern dword SC_Item_Create2(dword id, c_Vector3 *vec, c_Vector3 *movdir);	
extern void SC_Item_Preload(dword id);
extern BOOL SC_Item_GetPos(dword netid, c_Vector3 *pos);
extern void SC_SRV_Item_Release(dword netid);
extern dword SC_Item_Find(dword item_type);			

extern void SC_LevScr_Event(dword param1, dword param2);

extern BOOL SC_NET_FillRecover(s_SC_MP_Recover *recov, char *wpname);

extern void SC_GetPls(s_sphere *sph, dword *list, dword *items);
extern void SC_GetPlsInLine(c_Vector3 *pos, c_Vector3 *dir, dword *list, dword *items);

extern void SC_DisplayBinocular(BOOL enable);

extern BOOL SC_GetScriptHelper(char *name, s_sphere *sph);


extern BOOL SC_SND_SetEnvironment(dword env1_id, dword env2_id, float env_ratio);

extern void SC_SND_Ambient_Play(dword snd_id);
extern void SC_SND_Ambient_Stop(void);

extern void SC_SND_PlaySound3D(dword snd_id, c_Vector3 *pos);
extern void SC_SND_PlaySound3Dex(dword snd_id, c_Vector3 *pos, float *timeout);
extern void SC_SND_PlaySound2D(dword snd_id);


extern void SC_SND_PlaySound3Dlink(dword snd_id, void *nod, float *timeout);	
																				
																				




extern void SC_SND_PlaySound3Dpl(dword snd_id, dword pl_id, dword flags);
			


extern void SC_SND_PlaySound3DSpec(dword snd_id, c_Vector3 *pos, dword spec_id);
extern void SC_SND_PlaySound3DexSpec(dword snd_id, c_Vector3 *pos, float *timeout, dword spec_id);
extern void SC_SND_PlaySound2DSpec(dword snd_id, dword spec_id);

extern void SC_SND_SetHearableRatio(float Ratio);
extern void SC_SND_CreateCurveSound(char *anm_filename, dword snd_id, float max_play_dist, BOOL apply_env_volume);

extern float SC_SND_GetSoundLen(dword snd_id);

extern void SC_SND_PlayMusic(dword music_id);
extern void SC_SND_MusicPlay(dword MusicID, dword StartVolume );
extern void SC_SND_MusicStop(dword MusicID );
extern void SC_SND_MusicStopFade(dword MusicID, dword Time );
extern void SC_SND_MusicFadeVolume(dword MusicID, dword Volume, dword Time );

	
extern void SC_NOD_SetDSTR(void *nod, char *obj_name, char *dstr_name);
extern void SC_NOD_ResetDSTR(void *nod, char *obj_name);
extern char *SC_NOD_GetName(void *nod);
extern void SC_NOD_GetPivotWorld(void *nod,c_Vector3 *vec);
extern void SC_NOD_Detach(void *nod, char *name);
extern void SC_NOD_AddDynamic(void *master_nod, char *name, s_SC_OBJ_dynamic *info);

extern void SC_NOD_GetWorldPos(void *nod, c_Vector3 *pos);
extern float SC_NOD_GetWorldRotZ(void *nod);
extern BOOL SC_NOD_GetCollision(void *master_nod, char *name, BOOL clear_it);
extern BOOL SC_NOD_GetCollision2(void *nod, BOOL clear_it);

extern BOOL SC_DOBJ_IsBurning(void *nod, float perc);
extern BOOL SC_DOBJ_IsBurning2(void *nod);
extern void SC_DOBJ_StopBurning(void *nod, BOOL enable_future_burning);
extern void SC_NOD_GetDummySph(void *master_nod, char *dummy_name, s_sphere *sph);
extern void SC_DOBJ_ClearDamagedHP(void *nod);

extern void SC_DOBJ_BurnCreateBlockers(void *nod, s_sphere *sph, dword items);

extern void SC_DOBJ_SetFrozenFlag(void *nod, BOOL frozen);

extern void *SC_NOD_Get(void *master_obj, char *obj_name);
extern void *SC_NOD_GetNoMessage(void *master_obj, char *obj_name);
extern void *SC_NOD_GetNoMessage_Entity(char *obj_name);

extern void SC_NOD_GetTransform(void *obj,s_SC_NOD_transform *trans);			
extern void SC_NOD_SetTransform(void *obj,s_SC_NOD_transform *trans);
extern void SC_NOD_Hide(void *obj, BOOL hide);

extern void SC_NOD_GetPosInOtherSpace(void *other_nod, void *nod, c_Vector3 *vec);



extern void SC_NOD_SetFromANM(char *anm, float time, void *nod);
extern float SC_ANM_GetFrameTime(char *anm, int frame);
extern BOOL SC_NOD_GetPosFromANM(char *anm, float time, c_Vector3 *pos);


extern float SC_DOBJ_CameraLooksAt(void *nod, float max_dist);
extern float SC_DOBJ_CameraLooksAtCollision(void *nod, float max_dist);
extern void SC_ACTIVE_Add(void *nod, float cur_dist, dword info_txt);


extern void SC_DUMMY_Set_DoNotRenHier(char *dummy_name, BOOL do_not_render_hiearchy);
extern void SC_DUMMY_Set_DoNotRenHier2(void *nod, BOOL do_not_render_hiearchy);






extern BOOL SC_MP_EnumPlayers(s_SC_MP_EnumPlayers *list, dword *items, dword side);	
			
			
			

extern void SC_MP_RestartMission(void);

extern void SC_MP_P_SetRecoverTime(dword pl_id, float time);
extern dword SC_MP_P_GetAfterRecoverSide(dword pl_id);	

extern dword SC_MP_P_GetClass(dword pl_id);
extern dword SC_MP_P_GetAfterRecoverClass(dword pl_id);

extern void SC_MP_AddPlayerScript(char *filename);	

extern void SC_MP_SRV_SetForceSide(dword side);
extern void SC_MP_SRV_SetClassLimit(dword class_id, dword limit);
extern void SC_MP_SRV_SetClassLimitsForDM(void);


extern dword SC_MP_SRV_GetBestDMrecov(s_SC_MP_Recover *list, dword items, float *no_recov_time, float max_recov_time);


extern void SC_MP_SRV_InitWeaponsRecovery(float time);	

extern void SC_MP_HUD_SetTabInfo(s_SC_MP_hud *info);
extern void SC_MP_HUD_SelectPl(dword pl_id, dword color);

extern void SC_GameInfo(dword text_id, char *text);	
extern void SC_GameInfoW(ushort *text);
extern void SC_P_MP_AddPoints(dword pl_id, int val);

extern dword SC_MP_GetMaxPointsPl(int *points);
extern dword SC_MP_GetMaxFragsPl(int *frags);

extern dword SC_MP_GetHandleofPl(dword pl_id);
extern dword SC_MP_GetPlofHandle(dword pl_handle);

extern void SC_HUD_RadarShowPlayer(dword pl_id, dword color);
extern void SC_HUD_RadarShowPos(c_Vector3 *vec, dword color);
extern void SC_MP_SRV_P_SetObtainedDamageMult(dword pl_id, float mult);	
extern void SC_MP_SetSideStats(dword side, int frags, int points);
extern void SC_MP_ScriptMessage(dword param1, dword param2);	
extern void SC_MP_AllowStPwD(BOOL enable);		
extern void SC_MP_AllowFriendlyFireOFF(BOOL enable);		
extern void SC_MP_SetIconHUD(s_SC_HUD_MP_icon *icon, dword icons);
extern void SC_MP_SetInstantRecovery(BOOL enable);
extern void SC_MP_SetItemsNoDisappear(BOOL nodisappear);
extern void SC_MP_EnableBotsFromScene(BOOL enable);			
extern void SC_MP_SetChooseValidSides(dword mask);			
extern void SC_MP_EnableC4weapon(BOOL enable);				

extern void SC_MP_LoadNextMap(void);
extern void SC_MP_SetTeamGame(BOOL teamgame);
extern void SC_MP_RecoverAllNoAiPlayers(void);					
extern void SC_MP_RecoverAllAiPlayers(void);					

extern void SC_MP_EndRule_SetTimeLeft(float val, BOOL counting);				
extern void SC_MP_GetSRVsettings(s_SC_MP_SRV_settings *info);	
extern BOOL SC_MP_SRV_P_SetSideClass(dword pl_id, dword side, dword class_id);

extern BOOL SC_MP_SRV_GetAutoTeamBalance(void);
extern int SC_MP_SRV_GetTeamsNrDifference(BOOL after_respawn);
extern void SC_MP_SRV_DoExplosion(c_Vector3 *pos, dword type);

extern void SC_MP_SRV_ClearPlsStats(void);
extern void SC_MP_SRV_InitGameAfterInactive(void);

extern BOOL SC_MP_GetAmmoBoxesEnabled(void);
extern void SC_MP_SRV_GetAtgSettings(s_SC_MP_SRV_AtgSettings *info);



	extern void SC_MP_SetSpectatorCameras(char character);
	extern void SC_MP_GetRecovers(dword type, s_SC_MP_Recover *list, dword *items);



	extern void SC_MP_RecoverPlayer(dword pl_id);



	extern dword SC_MP_FpvMapSign_Load(char *fname);
	extern BOOL SC_MP_FpvMapSign_Unload(dword id);
	extern void SC_MP_FpvMapSign_Set(dword signs, s_SC_FpvMapSign *list);	
























#line 5 "C:\Users\flori\source\repos\VC_Scripter\original-resources\compiler\tt.c"































dword gSteps = 0;				
dword gRecs[2][6];		
s_SC_MP_Recover gRec[2][6][32];
float gRecTimer[2][6][32];

s_sphere gStepSwitch[6];	

dword gEndRule;
dword gEndValue;
float gTime;
dword gSidePoints[2];
dword gCLN_SidePoints[2];
dword gCLN_gamephase;

dword gMainPhase = 0;
dword gAttackingSide = 0;
dword gCurStep = 0;
BOOL gMission_phase = 0;
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

void *gFlagNod[6][3];
c_Vector3 gFlagPos[6];

dword abl_lists = 0;
dword abl_list[64];



dword gRespawn_id[2][6] = {
	{0,22,23,24,25,26},
	{17,18,19,20,21,0}
};




dword g_FPV_UsFlag = 0;
dword g_FPV_VcFlag = 0;
dword g_FPV_NeFlag = 0;



BOOL SRV_CheckEndRule(float time){
	

	switch(gEndRule){
		case 0:

			
			if (gMission_phase>0) gTime += time;

			
			SC_MP_EndRule_SetTimeLeft(gTime,gMission_phase);

			if (gTime>gEndValue){
				
				SC_MP_LoadNextMap();
				return 1;
			}

			break;

		case 2:

			if ((gSidePoints[0]>=gEndValue)||(gSidePoints[1]>=gEndValue)){
				
				SC_MP_LoadNextMap();
				return 1;
			}

			break;

		default:			
			SC_message("EndRule unsupported: %d",gEndRule);
			break;

	}

	return 0;

}


float GetRecovTime(void){
	
	
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
	
	SC_sgi(500,gSidePoints[0]);
	SC_sgi(501,gSidePoints[1]);
}


void SRV_UpdateMissionTime(float time){
	

	gMissionTime_update -= time;
	if (gMissionTime_update<0.0f){

		gMissionTime_update = 10.0f;

		SC_sgf(504,gMissionTime);
		SC_sgi(505,SC_ggi(505)+1);		
	}
}


void ResetMission(void){
	

	gCurStep = gSteps-1;

	SC_sgi(507,gCurStep);

	if ((gMainPhase%2)==0)
		gMissionTime = GetTimeLimit();
	else 
		gMissionTime = gMissionTimeToBeat;

	gMissionTime_update = -1.0;					
	SRV_UpdateMissionTime(0.0f);	

}

dword GetAttackingSide(dword main_phase){
	

	switch(main_phase%4){
		case 0:
		case 3:return 0;			
	}

	return 1;

}

void RoundEnd(void){
	
	


	switch(gMission_phase){

		case 3:
			gSidePoints[1-gAttackingSide]++;
			UpdateSidePoints();

			SC_sgi(506,1-gAttackingSide);
			SC_sgi(509,1-gAttackingSide);			

			if (gMainPhase % 2) gMainPhase++;
				else gMainPhase+=2;
			
			break;

		case 2:

			SC_sgi(509,gAttackingSide);

			if (gMainPhase % 2){
				gSidePoints[gAttackingSide]++;
				UpdateSidePoints();
				SC_sgi(506,gAttackingSide);
			}
			else
				gMissionTimeToBeat = GetTimeLimit() - gMissionTime;

			gMainPhase++;

			break;

	}

	SC_sgi(502,gMainPhase);

	gAttackingSide = GetAttackingSide(gMainPhase);


	SC_sgi(507,6);

}



void SetFlagStatus(dword attacking_side, dword cur_step){
	

	BOOL us,vc,ne;
	dword i,flags;

	s_SC_FpvMapSign fpv_list[6];



	flags = 0;

	for (i=0;i<6;i++){

		us = 0;
		vc = 0;
		ne = 0;

		if ((i+1)==cur_step){

			switch(attacking_side){
				case 0:
					vc = 1;
					break;
				case 1:
					us = 1;
					break;
				case 2:
					ne = 1;
					break;

			}

		}
		else
		if (i<cur_step){
			ne = 1;
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


	}

	SC_MP_FpvMapSign_Set(flags,fpv_list);

}


void Check_ABL(dword pl_handle){
	
	int val;
	dword to_change;
	s_SC_P_getinfo info;

	if (!SC_MP_SRV_GetAutoTeamBalance()) return;

	val = SC_MP_SRV_GetTeamsNrDifference(1);

	if ((val<3)&&(val>-3)) return;	

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

}


void Check_ABL_Restart(void){
	int val;
	dword side,nr_to_change;
	s_SC_P_getinfo info;
	s_SC_MP_EnumPlayers enum_pl[64];
	dword i,j,k;


	if (!SC_MP_SRV_GetAutoTeamBalance()) return;

	val = SC_MP_SRV_GetTeamsNrDifference(1);

	if ((val<3)&&(val>-3)) return;	

	if (val>0){
		side = 0;
		nr_to_change = val/2;
	}
	else{
		side = 1;
		nr_to_change = -val/2;
	}
	

	
	

	j = 64;

	if (SC_MP_EnumPlayers(enum_pl,&j,side)){				

		if (!j) return;
		
		while(nr_to_change!=0){

			k = rand()%j;
			i = k;

			while(
				(enum_pl[i].id==0)
				||(enum_pl[i].status==0)){

				i++;
				if (i==j) i = 0;
				if (i==k) return;	
			}						

			SC_MP_SRV_P_SetSideClass(enum_pl[i].id,1-side,1 + 20*(1-side));
			enum_pl[i].id = 0;

			nr_to_change--;

		}
							
	}



}



void RecoverDeathDefenders(void){

	s_SC_MP_EnumPlayers enum_pl[64];
	dword i,side,pls;

	side = 1-GetAttackingSide(SC_ggi(502));

	pls = 64;

	if (SC_MP_EnumPlayers(enum_pl,&pls,side)){

		for (i=0;i<pls;i++)
			if (enum_pl[i].status==2){
				SC_MP_RecoverPlayer(enum_pl[i].id);
			}

	}


}



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
		
		case 3:	
			

			if (SRV_CheckEndRule(info->elapsed_time)) break;

			
			side[0] = side[1] = 0;
			
			pls = 64;

			
			if (SC_MP_EnumPlayers(enum_pl,&pls,0xffffffff)){				

				
				if ((pls==0)&&((gSidePoints[0]+gSidePoints[1])!=0)){
					gSidePoints[0] = 0;
					gSidePoints[1] = 0;
					UpdateSidePoints();
				}
				

				
				for (i=0;i<pls;i++)
					if (enum_pl[i].status!=0){
						
						if (enum_pl[i].side<2) side[enum_pl[i].side] = 1;
						
					}

				gMission_starting_timer -= info->elapsed_time;

				if ((side[0])&&(side[1])){					

					SC_MP_SetInstantRecovery(0);

					if (gMission_phase==0){												
						
						gMission_phase = 1;										

						gMission_afterstart_time = 0.0f;
						SC_sgi(503,gMission_phase);
						ResetMission();						
						SC_MP_SRV_InitGameAfterInactive();

						if (gNoActiveTime>6.0f){
							SC_MP_RestartMission();							
							SC_MP_RecoverAllNoAiPlayers();
						}

						gMission_starting_timer = 8.0f;
					}
				}
				else{

					if (gMission_starting_timer<=0.0f){

						SC_MP_SetInstantRecovery(1);

						if (gMission_phase>0){							
							
							gMission_phase = 0;
							gMission_afterstart_time = 0.0f;
							SC_sgi(503,gMission_phase);
							Check_ABL_Restart();
							ResetMission();
						}

					}

				}

			}
							
						
			
			
			for (i=0;i<2;i++)
			for (j=0;j<gSteps;j++)
				for (k=0;k<gRecs[i][j];k++)
					gRecTimer[i][j][k] -= info->elapsed_time;


			gNextRecover -= info->elapsed_time;
			if (gNextRecover<0.0f) gNextRecover = GetRecovTime(); 

			switch(gMission_phase){

				case 0:

						gNoActiveTime += info->elapsed_time;

						if (gMissionTime>-10.0f){
							gMissionTime = -10.0f;
							gMissionTime_update = -1.0;					
							SRV_UpdateMissionTime(0.0f);
						}

						break;

				case 1:
			
						gMission_afterstart_time += info->elapsed_time;

						gMissionTime -= info->elapsed_time;
						SRV_UpdateMissionTime(info->elapsed_time);

						if (gMissionTime<=0.0f){	
							
							gMission_phase = 3;
							SC_sgi(503,gMission_phase);
							gPhaseTimer = 8.0f;
							RoundEnd();
						}
						else					
						if (gMission_afterstart_time>5.0f){
							
							
							if (gCurStep>0)
							for (i=0;i<pls;i++)
								if (((enum_pl[i].side==gAttackingSide)
									&&(enum_pl[i].status==1))){																		
										

										SC_P_GetPos(enum_pl[i].id,&pos);

										
										for (j=gCurStep-1;j<gCurStep;j++)
											if (SC_IsNear3D(&pos,&gStepSwitch[j].pos,gStepSwitch[j].rad)){
												
												if (j){								
													
													gCurStep = j;
													SC_sgi(510,SC_MP_GetHandleofPl(enum_pl[i].id));
													SC_sgi(507,gCurStep);													
													RecoverDeathDefenders();
												}
												else{
													
													gMission_phase = 2;
													SC_sgi(510,SC_MP_GetHandleofPl(enum_pl[i].id));
													SC_sgi(503,gMission_phase);													
													gPhaseTimer = 8.0f;
													RoundEnd();
												}
											}

									}

						}

						break;

					case 3:
					case 2:
						

						gPhaseTimer -= info->elapsed_time;
						if (gPhaseTimer<0.0f){							
							gNoActiveTime = 0.0f;
							gMission_phase = 0;
							SC_sgi(503,gMission_phase);
							Check_ABL_Restart();
							SC_MP_SetInstantRecovery(1);
							SC_MP_RecoverAllNoAiPlayers();													
						}

						break;

			}

			break;

		case 4:
			

			gCLN_ShowInfo -= info->elapsed_time;						
			if (gCLN_ShowStartInfo>0.0f) gCLN_ShowStartInfo -= info->elapsed_time;
			if (gCLN_ShowWaitingInfo>0.0f) gCLN_ShowWaitingInfo -= info->elapsed_time;
			

			
			switch(SC_ggi(503)){
				case 0:
					SetFlagStatus(SC_ggi(508)-1,2);
					break;
				case 1:
					
					if (gCLN_CurStep!=SC_ggi(507)){

						gCLN_CurStep = SC_ggi(507);						

						if ((gCLN_CurStep<(SC_ggi(508)-1))&&(gCLN_CurStep>0)){
							
							gCLN_ShowInfo = 5.0f;	
							SC_SND_PlaySound2D(10425);							
						}
					}

					SetFlagStatus(GetAttackingSide(SC_ggi(502)),gCLN_CurStep);

					break;
			}


			
			if (gCLN_MissionTimePrevID!=SC_ggi(505)){
				gCLN_MissionTimePrevID = SC_ggi(505);
				gCLN_MissionTime = SC_ggf(504);
			}
			else{
				if (SC_ggi(503)==1)
					gCLN_MissionTime -= info->elapsed_time;
				
			}

			
			
			for (i=0;i<2;i++){

				gCLN_SidePoints[i] = SC_ggi(500+i);			
				SC_MP_SetSideStats(i,0,gCLN_SidePoints[i]);
										

				icon[i].type = 1;
				icon[i].icon_id = 3*i;
				icon[i].value = gCLN_SidePoints[i];
				icon[i].color = 0xbbffffff;

			}

			icons = 2;

			if ((gCLN_MissionTime>0.0f)&&(SC_ggi(503))){
				icon[icons].color = 0xbbffffff;
				icon[icons].icon_id = 6;
									
				if (SC_ggi(503)==3)
					icon[icons].value = 0;					
				else
					icon[icons].value = (int)(gCLN_MissionTime+0.99f);					

				icon[icons].type = 2;
				icons++;
			}

			SC_MP_SetIconHUD(icon,icons);


			break;

		case 9:
			
			

			SC_sgi(499,9);

			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;

			SC_MP_EnableBotsFromScene(0);

			

			break;

		case 1:
			


			g_FPV_UsFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_USflag.BES");
			g_FPV_VcFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_VCflag.BES");
			g_FPV_NeFlag = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_emptyflag.BES");


			
			SC_MP_SRV_SetForceSide(0xffffffff);
			SC_MP_SetChooseValidSides(3);

			
			SC_MP_SRV_SetClassLimit(18,0);
			SC_MP_SRV_SetClassLimit(19,0);
			SC_MP_SRV_SetClassLimit(39,0);

			SC_MP_GetSRVsettings(&SRVset);

			for (i=0;i<6;i++){
				SC_MP_SRV_SetClassLimit(i+1,SRVset.atg_class_limit[i]);
				SC_MP_SRV_SetClassLimit(i+21,SRVset.atg_class_limit[i]);
			}


			

			SC_ZeroMem(&hudinfo,sizeof(hudinfo));
			hudinfo.title = 5100;
			
			hudinfo.sort_by[0] = 3;
			hudinfo.sort_by[1] = 4 | 0x80000000;
			hudinfo.sort_by[2] = 5 | 0x80000000;


			hudinfo.pl_mask = 0x01 | 0x08 | 0x10;
			hudinfo.use_sides = 1;
			hudinfo.side_name[0] = 1010;
			hudinfo.side_color[0] = 0x440000ff;
			hudinfo.side_name[1] = 1011;
			hudinfo.side_color[1] = 0x44ff0000;

			hudinfo.side_mask = 0x01;
			
			SC_MP_HUD_SetTabInfo(&hudinfo);

			
			SC_MP_AllowStPwD(1);
			SC_MP_AllowFriendlyFireOFF(1);

			SC_MP_SetItemsNoDisappear(0);
			

			if (info->param2){	


				
				SC_ZeroMem(&gFlagNod,sizeof(gFlagNod));

				for (i=0;i<6;i++){

					sprintf(txt,"TT_flag_%d",i);

					nod = SC_NOD_GetNoMessage(0,txt);

					
					
				
					if (nod){
						SC_NOD_GetPivotWorld(nod,&gFlagPos[i]);
						gFlagNod[i][0] = SC_NOD_Get(nod,"vlajkaUS");
						gFlagNod[i][1] = SC_NOD_Get(nod,"Vlajka VC");
						gFlagNod[i][2] = SC_NOD_Get(nod,"vlajka N");
					}

				}


				if (info->param1){	
					
					
					
					SC_MP_Gvar_SetSynchro(500);
					SC_MP_Gvar_SetSynchro(501);
					UpdateSidePoints();

					SC_MP_Gvar_SetSynchro(503);
					SC_sgi(503,0);

					SC_MP_Gvar_SetSynchro(502);
					SC_sgi(502,0);

					SC_MP_Gvar_SetSynchro(506);
					SC_sgi(506,0);

					SC_MP_Gvar_SetSynchro(509);
					SC_sgi(509,0);

					SC_MP_Gvar_SetSynchro(510);
					SC_sgi(510,0);			
				

					SC_MP_Gvar_SetSynchro(507);
					SC_sgi(507,0);

					SC_MP_Gvar_SetSynchro(508);
					

					SC_MP_Gvar_SetSynchro(504);
					SC_MP_Gvar_SetSynchro(505);
					SC_sgf(504,0.0f);
					SC_sgi(505,0);		


					
					SC_ZeroMem(&gRecs,sizeof(gRecs));

					for (k=0;k<2;k++){

						if (k) side_char = 'D';
							else side_char = 'A';

						for (j=0;j<6;j++){

							for (i=0;i<32;i++){

								sprintf(txt,"TT_%c%d_%d",side_char,j,i);
								
								if (SC_NET_FillRecover(&gRec[k][j][gRecs[k][j]],txt)){
									gRecs[k][j]++;								
								}
							}
							


							if (gRespawn_id[k][j]){
								i = 32 - gRecs[k][j];
								SC_MP_GetRecovers(gRespawn_id[k][j],&gRec[k][j][gRecs[k][j]],&i);
								gRecs[k][j] += i;								
							}



						}

					}
					
					gSteps = 0;

					for (i=0;i<6;i++)
						if (gRecs[0][i]) gSteps = i+1;
							

					for (i=0;i<gSteps;i++)
						SC_Log(3,"TurnTable recovers #%d: att:%d  def:%d",i,gRecs[0][i],gRecs[1][i]);

					SC_ZeroMem(&gRecTimer,sizeof(gRecTimer));


					

					for (i=0;i<gSteps-1;i++){

						sprintf(txt,"TTS_%d",i);

						if (!SC_GetScriptHelper(txt,&gStepSwitch[i])){
							SC_message("helper %s not found",txt);
						}

					}

					SC_sgi(508,gSteps);

				}

			}

			break;


		case 2:

			

			i = 0;
			witxt = 0;
			in_middle = 0;

			k = SC_ggi(502);

			if (gCLN_gamephase!=SC_ggi(503)){
				gCLN_gamephase = SC_ggi(503);
				switch(gCLN_gamephase){
					case 2:
					case 3:
						if (SC_ggi(509)==0) SC_SND_PlaySound2D(11117);
							else SC_SND_PlaySound2D(11116);
						break;					
				}
			}

			

			switch(gCLN_gamephase){

				case 0:
					if (gCLN_ShowWaitingInfo<=0.0f)					
						witxt = SC_Wtxt(1076);

					gCLN_ShowStartInfo = 0.0f;
					break;

				case 1:

					gCLN_ShowWaitingInfo = 3.0f;

					if (gCLN_ShowStartInfo==0.0f){
						gCLN_ShowStartInfo = 3.0f;
					}

					if (gCLN_ShowStartInfo>0.0f){

						i = SC_PC_Get();
						if (i){
							SC_P_GetInfo(i,&plinfo);

							if (plinfo.side==GetAttackingSide(SC_ggi(502)))
								witxt = SC_Wtxt(5108);
							else
								witxt = SC_Wtxt(5109);

							SC_GameInfoW(witxt);
							witxt = 0;
						}					

					}
					else					
					if ((gCLN_ShowInfo>0.0f)&&(gCLN_CurStep>0)){

						j = SC_MP_GetPlofHandle(SC_ggi(510));
						if (j){						
							SC_AnsiToUni(SC_P_GetName(j),wtxt2);
						}
						else
							SC_AnsiToUni("'disconnected'",wtxt2);

						swprintf(wtxt,SC_Wtxt(5107),wtxt2,gCLN_CurStep);
						witxt = wtxt;
					}
					else{
						

						i = SC_PC_Get();
						if (i){
							SC_P_GetInfo(i,&plinfo);

							if (plinfo.side==GetAttackingSide(SC_ggi(502))){
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
								
						}

					}
					
					break;

				case 2:
					
					

					
					

					j = SC_MP_GetPlofHandle(SC_ggi(510));
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
					}
					

					swprintf(wtxt,SC_Wtxt(i),wtxt2);
					witxt = wtxt;
					gCLN_ShowStartInfo = 0.0f;
					break;

				case 3:
					
					

					j = SC_MP_GetPlofHandle(SC_ggi(510));
					if (j){						
						SC_AnsiToUni(SC_P_GetName(j),wtxt2);
					}
					else
						SC_AnsiToUni("'disconnected'",wtxt2);


					switch(SC_ggi(506)){
						case 0:i = 5105;break;
						case 1:i = 5106;break;
					}

					swprintf(wtxt,SC_Wtxt(i),wtxt2);
					witxt = wtxt;	
					gCLN_ShowStartInfo = 0.0f;

					break;

			}
			
				
			if (witxt){
				
				SC_GetScreenRes(&val,&valy);

				val -= SC_Fnt_GetWidthW(witxt,1); 

				if (in_middle) valy = 0.5f * valy - 40.0f;
					else valy = 15;

				SC_Fnt_WriteW(val * 0.5f,valy,witxt,1,0xffffffff);

			}


			break;

		case 5:
			

			if (info->param2){
				
				info->fval1 = 0.1f;
			}
			else{
				
				switch(gMission_phase){

					case 1:

						
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

					case 0:
						info->fval1 = 3.0f;
						break;

					default:
						
						info->fval1 = -1.0f;
						break;
				}

			}

			break;

		case 6:
			

			precov = (s_SC_MP_Recover*)info->param2;

			j = info->param1; 
			if (gAttackingSide) j = 1-j;
				
			if (j){
				
				if (gMission_phase==1){
					if (gCurStep<2) k = 0;
						else k = gCurStep-1-rand()%2;
				}
				else k = 0;

			}
			else{
				
				if (gMission_phase==1){
					k = gCurStep;
				}
				else k = gSteps-1;
			}			

			i = SC_MP_SRV_GetBestDMrecov(gRec[j][k],gRecs[j][k],gRecTimer[j][k],3.0f);
			
			gRecTimer[j][k][i] = 3.0f;
			*precov = gRec[j][k][i];
															
			break;



		case 10:
			

			gTime = 0;

			SC_ZeroMem(&gSidePoints,sizeof(gSidePoints));			
			UpdateSidePoints();			

			SC_MP_SetInstantRecovery(1);

			if (gMission_phase!=0){
				SC_MP_RestartMission();							
				SC_MP_RecoverAllNoAiPlayers();			
				gMission_phase = 0;				
				SC_sgi(503,gMission_phase);				
			}

			gCLN_ShowInfo = 0.0f;
			SC_MP_SRV_ClearPlsStats();

			break;

		case 11:
			
			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;
			break;

		case 7:
			
			Check_ABL(info->param1);			
			break;
			

	}
	


	return 1;

}
