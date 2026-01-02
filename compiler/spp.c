#line 0 "C:\Users\flori\source\repos\VC_Scripter\compiler\VCBOT5.c"
 







#line 0 "C:\Users\flori\source\repos\VC_Scripter\compiler\inc\sc_global.h"
 























	




























































































													
													
													
													
												
												
												

												
												
												





												
												










												




												
												
														





												
												



												
												












































































































































































































































											
											
												






											
											


												
												


























































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
	dword message,param1,param2;
	dword pl_id;
	void *pos;	
	float elapsed_time;
	float next_exe_time;
}s_SC_P_info;


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

	float max_vis_distance;				
	float watchfulness_zerodist;		
	float watchfulness_maxdistance;		
	float boldness;						
	float coveramount;					
	float shoot_imprecision;			
	
	BOOL extend_searchway;				
										
	float shortdistance_fight;			
										
										
	float view_angle;					
	float view_angle_near;				

	float hear_imprecision;				
	float hear_distance_mult;			
	float hear_distance_max;			

	float grenade_min_distance;			
	float grenade_timing_imprecision;	
	float grenade_throw_imprecision;	
	float grenade_sure_time;			

	float forget_enemy_mult;			
	float shoot_damage_mult;			

	BOOL disable_peace_crouch;			

	float peace_fakeenemy_run;			
	float peace_fakeenemy_phase;		

	float shoot_while_hidding;			

	float reaction_time;				
	float scout;						
	float berserk;						

	float aimtime_max;					
	float aimtime_canshoot;				
	float aimtime_rotmult;				

	float wounded_start_perc;			
	float wounded_aimtime_mult_max;		
	float wounded_shoot_imprec_plus;	

}s_SC_P_AI_props;


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
	
	float Position;				
	float Aim;					
	float Run;					
	
}s_SC_P_Ai_BattleProps;



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

	dword event_type;
	void *obj;
	void *weap_type;
	dword anim_id;
	float anim_time;
	float prev_time;
	c_Vector3 pos;
	dword cur_batch;
	dword cur_ammo;
	dword cur_phase;		
	float param1;			
							
	dword cur_bayonet;		
							
	dword weap_phase;		
	

	float step_time;		


}s_SC_WEAP_info;


typedef struct{

	dword event_type;		
	void *obj;
	void *weap_type;
	dword cur_batch;
	dword cur_ammo;
	dword cur_phase;		
	dword pl_id;			
	dword cur_bayonet;		

}s_SC_WEAP3pv_info;


typedef struct{
	dword event_type;		
	s_sphere sph;
	void *nod;
	float elapsed_time;
	float next_exe_time;	
}s_SC_ScriptHelper_info;



typedef struct{
	c_Vector3 loc;
	c_Vector3 rot;
	c_Vector3 scale;
}s_SC_NOD_transform;


typedef struct{

	void *master_nod;	

	void *steeringwheel_nod;
	float steeringwheel_max_rot;	

	float steer_max;
	float steer_speed;
	float steer_backspeed;
	float steer_curse[11];	

	float steer_max_mult_at10mpersec;
	float steer_speed_mult_at10mpersec;
	float steer_backspeed_mult_at10mpersec;
							
	float eng_max_revs;			
	float eng_freewheel_revs;	
	float eng_revs_slowdown;
	float eng_min_revs;			
	c_Vector3 eng_sound_pos;
	
	float eng_freqmult_1,eng_freqmult_revs1;
	float eng_freqmult_2,eng_freqmult_revs2;

	dword eng_snd_id;

	dword eng_val_steps;
	float *eng_Nm;	
	float *eng_kW;
	float *eng_sound_volume;

	float trns_delay;
	dword trns_gears;
	float *trns_gear;

	float brake_power;
	
}s_SC_Car_Init;


typedef struct{

	c_Vector3 body_point;		
	c_Vector3 body_vector;		
	
	float spring_tmin;			
	float spring_tmax;			
	float spring_t;				
	float spring_absorber;		
	float spring_looser;		
	float spring_rate;			
	float wheel_radius;			
	float wheel_friction;		


	float wheel_aspd;			
	BOOL wheel_with_drive;		
	BOOL steering;
	BOOL left_side;

	float wheel_fr_min;
	float wheel_fr_dspd;

	float ptc_v0_mult;
	float ptc_v1_mult;

}s_SC_Car_AddWheel;


typedef struct{
	dword function;
	dword entry_name_nr;
	dword exit_name_nr;	
	c_Vector3 entry;
	float entry_dist;
	c_Vector3 target;
	c_Vector3 view;
	float min_rx,max_rx;
	float min_rz,max_rz;

	float shoot_min_rz,shoot_max_rz;
	dword switch_3pv_anim_dir;
	
	char *stg_dir;
	BOOL can_shoot;
	BOOL disabled_for_PC;
	float rz;

}s_SC_Car_AddEntry;


typedef struct{

	dword pl_back_txt,pl_back_snd;		
	dword ra_back_txt,ra_back_snd;

	dword ra_where_ru_nr;				
	dword ra_where_ru_txt[5];			
	dword ra_where_ru_snd[5];

}s_SC_SpeachBreakProps;



typedef struct{	
	dword message,param1,param2,param3;
	float elapsed_time;	
	float fval1;
}s_SC_NET_info;

 



















  


typedef struct{
	
	dword valid_uses;					
	float use_interval;					
	float cur_interval;					
	
}s_SC_P_Ai_Grenade;



typedef struct{	
	float min_dist,max_dist;
	c_Vector3 follow_change;	
}s_SC_Ai_PlFollow;



typedef struct{	

	void *master_nod;	

	float steer_max;
	float steer_speed;
	float steer_backspeed;	
							
	float eng_max_revs;			
	float eng_freewheel_revs;	
	float eng_revs_slowdown;
	
	c_Vector3 eng_sound_pos;
	c_Vector3 drive_pos;
	
	float eng_freqmult_1,eng_freqmult_revs1;
	float eng_freqmult_2,eng_freqmult_revs2;

	dword eng_snd_id;

	float power_front,power_back;

}s_SC_Ship_Init;



typedef struct{
	
	c_Vector3 _env_normal;	
	c_Vector3 _hydI;	
	c_Vector3 _hydJ;	
	c_Vector3 _hydK;	
	float _CI;	
	float _CJ;	
	float _CK;	
	float _QR;	
	float _QI;	
	float _QJ;	
	float _QIJ;	
	float _FK;

}s_SC_PHS_IWantToFloat;

typedef struct{
	dword savename_id;
	dword description_id;
	BOOL disable_info;		
}s_SC_MissionSave;



typedef struct{
	c_Vector3 camera_pos;
	c_Vector3 camera_dir;
}s_SC_RC_info;


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

	void *master_nod;	
	dword eng_snd_id;
	dword snd2_id;
	float snd2_turndown_dist;
	float snd2_zerodist_volume;	
	dword flags;		

}s_SC_Heli_Init;



typedef struct{	
	dword weap_type;			

	dword use_info_txt_id;		
	dword exit_info_txt_id;		

	void *master_nod;			
	void *nod_base;				
	void *nod_rotate_x;			
	void *nod_rotate_z;			
	void *nod_rotate_last;		
	void *nod_fpv_camera;		
	void *nod_active_pos;		
	void *nod_muzzle;
	void *nod_entry;			
		

	float active_rad;			
	float active_dist;			

	float rotate_zmin,rotate_zmax;		
	float rotate_xmin,rotate_xmax;		
	float rotate_speed;					

	float flash_rot_step;		

	
	dword link_at;				
	void *link_ptr;				
	dword link_entry_index;		

	char *anim_dir;

}s_SC_MWP_Create;



typedef struct{

	char *sa[5];	
							

}s_SC_P_SpecAnims;


typedef struct{
	void *weap_type;			
	void *from;					
	c_Vector3 dir;				
	c_Vector3 add_rot;			
}s_SC_FlyOffCartridge;


typedef struct{
	dword text_id;
	dword status;		
}s_SC_Objective;



typedef struct{

	float	missionTime;				
	dword	difficulty;
	dword	missionStatus;

	
	dword	SF;							
	dword	LLDB;
	dword	CIDG;
	dword	Heli;						
	dword	Jeep;

	
	dword	VC;							
	dword	Gaz;						
	dword	Boobytrap;					
	dword	Caches;						
	dword	Tunnels;
	dword	Facilities;
	dword	Intelligence;

	
	dword	Bangs;						
	dword	Defort;
	dword	Hornster;
	dword	Nhut;
	dword	Bronson;
	dword	Crocker;

}s_SC_DebriefInfo;


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
	float ctf_respawntime;
}s_SC_MP_SRV_AtgSettings;



typedef struct{
	float r,g,b;
	float rad;	
	c_Vector3 pos;

	float time;
	BOOL decrease_radius;
}s_SC_light;


typedef struct{

	int   musId;			
	int   musVol;			
	float musFadeIn;		
	float musPlayTime;		
	float musFadeOut;		
	int   heliVol;			
	int   gameVol;			
	int	  natureVol;		

}s_MusicDef;

typedef struct{
	dword chats[9];
	dword radistmarks;
	dword radiomarks;
}s_SC_BombInfo;


typedef struct{
	dword intel[10];
}s_SC_P_intel;

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


typedef struct{
    float fade_in_time;
    float stay_in_time_begin;
    float stay_in_time_end;
    float fade_out_time;

    float current_time;

    dword font_id;
    dword text_id;
    dword color;

    int alignx;
    int aligny;

    int max_num_lines;
    float scale_ratio;

}s_SC_HUD_TextWrite;





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

extern BOOL SC_KeyJustPressed(dword id);			
extern BOOL SC_KeyPressed(dword id);				

extern void SC_EventImpuls(char *ev_name);
extern void SC_EventEnable(char *ev_name, BOOL enable);	

extern void SC_MissionCompleted(void);
extern void SC_MissionFailed(void);
extern void SC_MissionFailedEx(dword music_id, dword start_volume);
extern void SC_MissionDone(void);	
extern void SC_TheEnd(void);		


extern void SC_SetViewAnim(char *anm_name, dword start_frame, dword end_frame, dword callback_id);
extern void SC_SetViewAnimEx(char *anm_name, dword start_frame, dword end_frame, dword callback_id, void *nod);

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


extern void SC_SpeachRadio(dword speach_txt, dword snd_id, float *timeout);
extern void SC_SpeachRadioMes(dword speach_txt, dword snd_id, float *timeout, dword param);

extern void SC_SpeechRadio2(dword speech_txt, float *timeout);
extern void SC_SpeechRadioMes2(dword speech_txt, float *timeout, dword param);


extern void SC_Radio_Enable(dword radio_id);
extern void SC_Radio_Disable(dword radio_id);

extern BOOL SC_Radio_Get(dword *radio_id);
											

extern void SC_RadioBatch_Begin(void);
extern void SC_RadioBatch_End(void);

extern void SC_RadistBatch_Begin(void);
extern void SC_RadistBatch_End(void);

extern void SC_RadioSet2D(BOOL willbe2D);	
											
extern void SC_SpeechSet3Dto3Dincamera(BOOL incamera3D);
											
											
extern void SC_RadioSet3DButDistanceLimit(BOOL enable);											
											
											
											

extern float SC_RadioGetWillTalk(void);


extern void SC_RadioBreak_Set(s_SC_SpeachBreakProps *props);
extern void SC_RadioBreak_Get(s_SC_SpeachBreakProps *props);
extern void SC_RadioSetDist(float max_dist_subtitle_write);

extern void SC_MissionSave(s_SC_MissionSave *info);

extern void SC_DoExplosion(c_Vector3 *pos, dword type);	
														
extern void SC_ArtillerySupport(BOOL enable);
extern void SC_SetBombInfo(s_SC_BombInfo *info);

extern void SC_SetMapFpvModel(char *bes_filename);

extern dword SC_MWP_Create(s_SC_MWP_Create *info);

extern void SC_SetSceneVisibilityMult(float vis_mult, float scene_fog_mult, float bckg_fog_mult);
				

extern void SC_SetObjectScript(char *obj_name, char *script_name);

extern void SC_ClearImpossibleWayTargets(void);

extern BOOL SC_SphereIsVisible(s_sphere *sph);
extern void SC_GetPos_VecRz(void *cpos, c_Vector3 *pos, float *rz);	

extern void SC_MakeBurning(s_sphere *sph);				

extern void SC_PreloadBES(dword id, char *bes_name);	

extern void SC_SetObjectives(dword objectives, s_SC_Objective *objective, float force_display_time);
extern void SC_SetObjectivesNoSound(dword objectives, s_SC_Objective *objective, float force_display_time);
extern void SC_GetLoudShot(s_sphere *sph);

extern void SC_SetCommandMenu(dword text_id);	
												
extern float SC_GetVisibility(void);
extern float SC_GetPCZoom(void);

extern void SC_ShowHelp(dword *txt, dword texts, float time);
														
														

extern void SC_PreloadWeapon(dword type, BOOL fpv_to);
extern void SC_FadeTo(BOOL black, float time);	

extern void SC_SetAmmobagAmmo(dword ammo_type, BOOL enable);	

extern void SC_ShowMovieInfo(dword *txt);						
																
extern void SC_Debrief_Clear(void);
extern void SC_Debrief_Add(s_SC_DebriefInfo *add_info);
extern void SC_Debrief_Get(s_SC_DebriefInfo *info);

extern void SC_HUD_DisableRadar(BOOL disable);

extern void SC_HUD_TextWriterInit(s_SC_HUD_TextWrite *initdata);
extern void SC_HUD_TextWriterRelease(float fade_out_time);


extern void SC_CreateMissile(dword missile_id, dword author_pl_id, c_Vector3 *from, c_Vector3 *at);
							
							
							
							
							
							
					
extern void SC_PreloadSound(dword snd_id, BOOL is3D);	
extern void SC_FadeSoundPlayer(dword snd_player_id, float final_volume, float fade_time);


extern ushort* SC_Wtxt(dword val);				

extern dword SC_GetNearestPlayer(c_Vector3 *vec, float *dist);

extern void SC_SwitchSceneSCS(char *fname, float time);			
extern void SC_RemoveItems(s_sphere *area, dword item_type);	

extern BOOL SC_GetRndWp(s_sphere *sph, c_Vector3 *wp);			
																

extern void SC_Ai_SetShootOnHeardEnemyColTest(BOOL do_test);
extern void SC_SetMovieBorders(BOOL set_on);


extern void SC_EnableBloodWhenHit(BOOL enable); 

extern void SC_CreateLight(s_SC_light *info);

extern void SC_EnableCharacterLOD(BOOL enable);	

extern void SC_EnableObjectScriptWhileUnipage(void *master_nod, BOOL enable);
extern void SC_GetCameraPos(c_Vector3 *vec);

extern void SC_EnableQuickSave(BOOL enable); 

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

extern void SC_PC_EnableRadioBreak(BOOL enable);		


extern float SC_PC_PlayFpvAnim(char *filename);
extern float SC_PC_PlayFpvAnim2(char *filename, dword plb_id, char *eqp, char *anm);
													
													
													

extern void SC_PC_PlayFpvLooped(char *filename);	

extern void SC_PC_EnableFlashLight(BOOL enable);	

extern void SC_PC_EnableHitByAllies(BOOL enable);	
extern void SC_PC_EnablePickup(BOOL enable);		

extern void SC_PC_SetIntel(s_SC_P_intel *info);
extern void SC_PC_GetIntel(s_SC_P_intel *info);



extern dword SC_P_Create(s_SC_P_Create *info);	
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
extern void SC_P_AddAttObj(dword pl_id, char *bes_name, char *eqp_name);
extern void SC_P_GetInfo(dword pl_id, s_SC_P_getinfo *info);
extern void SC_P_DoKill(dword pl_id);

extern void SC_P_Speach(dword pl_id, dword speach_txt, dword snd_id, float *timeout);
extern void SC_P_SpeachMes(dword pl_id, dword speach_txt, dword snd_id, float *timeout, dword param);
extern void SC_P_SpeachRadio(dword pl_id, dword speach_txt, dword snd_id, float *timeout);
extern void SC_P_SetSpeachDist(dword pl_id, float max_dist_subtitle_write);

extern void SC_P_Speech2(dword pl_id, dword speech_txt, float *timeout);
extern void SC_P_SpeechMes2(dword pl_id, dword speech_txt, float *timeout, dword param);
extern void SC_P_SpeechMes3(dword pl_id, char *speech_str, float *timeout, dword param);
extern void SC_P_SpeechMes3W(dword pl_id, ushort *speech_str, float *timeout, dword param);


extern void SC_P_DoAnim(dword pl_id, char *filename);
extern void SC_P_DoAnimLooped(dword pl_id, char *filename);


extern void SC_P_SetChat(dword pl_id, float time);
extern BOOL SC_P_CanChat(dword pl_id);
extern void SC_P_SetHp(dword pl_id, float hp);
extern void SC_P_Heal(dword pl_id);
extern void SC_P_Radio_Enable(dword pl_id, dword radio_id);
extern BOOL SC_P_Radio_Used(dword pl_id, dword radio_id);
extern dword SC_P_GetBySideGroupMember(dword iside, dword igroup, dword imember);

extern void SC_P_ScriptMessage(dword pl_id, dword param1, dword param2);	
extern dword SC_P_IsInCar(dword pl_id);
extern dword SC_P_IsInCarEx(dword pl_id, dword *entry_index);
extern dword SC_P_IsInHeli(dword pl_id);
extern dword SC_P_IsInShip(dword pl_id);
extern void SC_P_Release(dword pl_id);

extern void SC_P_SetToHeli(dword pl_id, char *heli_name, dword entry_index);	
extern void SC_P_ExitHeli(dword pl_id, c_Vector3 *new_pos);
extern BOOL SC_P_HasWeapon(dword pl_id, dword weap_type);
extern void SC_P_SetToShip(dword pl_id, char *ship_name, dword entry_index);	
extern void SC_P_ExitShip(dword pl_id, c_Vector3 *new_pos);
extern void SC_P_SetToCar(dword pl_id, char *car_name, dword entry_index);	
extern void SC_P_SetToSceneMwp(dword pl_id, char *mwp_name);
extern void SC_P_ExitSceneMwp(dword pl_id);


extern BOOL SC_P_GetHasShoot(dword pl_id);		
extern dword SC_P_GetCurWeap(dword pl_id);


extern void SC_P_Recover(dword pl_id, c_Vector3 *pos, float rz);	
extern void SC_P_Recover2(dword pl_id, c_Vector3 *pos, float rz, dword phase);	


extern float SC_P_GetWillTalk(dword pl_id);	
extern BOOL SC_P_GetTalking(dword pl_id);	

extern void SC_P_EnableLonelyWolfKiller(dword pl_id, float distance);	
												
												
												
extern void SC_P_SetFaceStatus(dword pl_id, dword face_type, float time);
												
extern void SC_P_SetHandVariation(dword pl_id, dword hand_id, dword variation, float time);
												
												
												

extern void SC_P_Link3pvEqp(dword pl_id, dword slot_id, dword plb_id, char *eqp_name);	
extern void SC_P_UnLink3pvEqp(dword pl_id, dword slot_id);								

extern void SC_P_SetSpecAnims(dword pl_id, s_SC_P_SpecAnims *info);
extern void SC_P_AddAllAmmo(dword pl_id);
extern void SC_P_AddAmmoNoGrenade(dword pl_id);


extern void SC_P_ChangeWeapon(dword pl_id, dword slot_id, dword weap_type);
extern void SC_P_SetSelWeapon(dword pl_id, dword slot_id);
extern float SC_P_GetPhase(dword pl_id);     
extern void SC_P_SetPhase(dword pl_id, dword phase);     

extern float SC_P_GetDistance(dword pl_id, dword to_pl_id);
extern void SC_P_SetActive(dword pl_id, BOOL active);
extern BOOL SC_P_GetActive(dword pl_id);

extern void SC_P_SetInvisibleForAi(dword pl_id, BOOL invisible);	
extern BOOL SC_P_GetInvisibleForAi(dword pl_id);

extern void SC_P_DoHit(dword pl_id, dword area_id, float hp);
extern void SC_P_SetRadarColor(dword pl_id, dword val);	
extern void SC_P_SetNoAmmo(dword pl_id);
extern void SC_P_CloseEyes(dword pl_id, BOOL force_close);

extern void SC_P_RemoveAllSpeech(dword pl_id);	
												
extern void SC_P_RemoveAllSpeechEx(dword pl_id, BOOL include_active);
												
												
												
												

extern void SC_P_SetAmmo(dword pl_id, dword ammo_type, dword amount);

extern BOOL SC_P_UsesBinocular(dword pl_id);
extern void SC_P_EnableBinocular(dword pl_id, BOOL enable);	
extern void SC_P_EnableHeadEqpFlyOff(dword pl_id, BOOL enable);
extern void SC_P_EnableHitAnimations(dword pl_id, BOOL enable);
extern void SC_P_EnableSearchDeathBodies(dword pl_id, BOOL enable);	


extern void SC_P_WriteHealthToGlobalVar(dword pl_id, dword first_gvar);		
extern void SC_P_ReadHealthFromGlobalVar(dword pl_id, dword first_gvar);	

extern void SC_P_WriteAmmoToGlobalVar(dword pl_id, dword first_gvar, dword last_gvar);	
extern void SC_P_ReadAmmoFromGlobalVar(dword pl_id, dword first_gvar, dword last_gvar); 

extern dword SC_P_GetAmmoInWeap(dword pl_id, dword slot_id);
extern void SC_P_SetAmmoInWeap(dword pl_id, dword slot_id, dword ammo);

extern void SC_P_SetLinkedView(dword pl_id, float rz, float rx);

extern BOOL SC_P_IsInSpecStativ(dword pl_id);

extern void SC_P_DisableSpeaking(dword pl_id, BOOL disable);


extern void SC_P_Ai_SetMode(dword pl_id, dword mode);				
extern dword SC_P_Ai_GetMode(dword pl_id);				
extern void SC_P_Ai_SetBattleMode(dword pl_id, dword battlemode);	
																
extern void SC_P_Ai_SetBattleModeExt(dword pl_id, dword battlemode, c_Vector3 *param);
																
extern dword SC_P_Ai_GetBattleMode(dword pl_id);	

extern void SC_P_Ai_SetPeaceMode(dword pl_id, dword peacemode);	
extern dword SC_P_Ai_GetPeaceMode(dword pl_id);					

extern dword SC_P_Ai_GetSpecTask(dword pl_id);					


extern void SC_P_Ai_SetMoveMode(dword pl_id, dword mode);			
extern void SC_P_Ai_SetMovePos(dword pl_id, dword pos);				
extern void SC_P_Ai_EnableShooting(dword pl_id, BOOL enable);		
extern void SC_P_Ai_Go(dword pl_id, c_Vector3 *vec);
extern void SC_P_Ai_Stop(dword pl_id);
extern void SC_P_Ai_GetProps(dword pl_id, s_SC_P_AI_props *props);
extern void SC_P_Ai_SetProps(dword pl_id, s_SC_P_AI_props *props);

extern void SC_P_Ai_GetGrenateProps(dword pl_id, s_SC_P_Ai_Grenade *props);
extern void SC_P_Ai_SetGrenateProps(dword pl_id, s_SC_P_Ai_Grenade *props);

extern dword SC_P_Ai_GetEnemies(dword pl_id);
extern dword SC_P_Ai_GetSureEnemies(dword pl_id);
extern void SC_P_Ai_LookAt(dword pl_id, c_Vector3 *vec);
extern void SC_P_Ai_EnableSituationUpdate(dword pl_id, BOOL enable);

extern void SC_P_Ai_EnterCar(dword pl_id, char *car_name, dword entry_function, s_sphere *enter_pos);
				
extern void SC_P_Ai_StepOutCar(dword pl_id);
extern BOOL SC_P_Ai_KnowsAboutPl(dword pl_id, dword target_pl_id);

extern void SC_P_Ai_SetBattleProps(dword pl_id, s_SC_P_Ai_BattleProps *props);	

extern BOOL SC_P_Ai_GetShooting(dword pl_id, dword *target_pl_id);
extern float SC_P_Ai_GetDanger(dword pl_id);

extern void SC_P_Ai_SetPreferedWeaponSlot(dword pl_id, dword slot);
extern dword SC_P_Ai_GetPreferedWeaponSlot(dword pl_id);	

extern void SC_P_Ai_ShootAt(dword pl_id, c_Vector3 *pos, float time);	
extern void SC_P_Ai_ForgetEnemies(dword pl_id);	
extern void SC_P_Ai_HideYourself(dword pl_id, c_Vector3 *danger_pos, float max_walk_dist);	

extern BOOL SC_P_Ai_LookingAt(dword pl_id, c_Vector3 *pos);
extern void SC_P_Ai_ShouldLookAt(dword pl_id, c_Vector3 *pos, float time);

extern void SC_P_Ai_SetStaticMode(dword pl_id, BOOL is_static);
extern BOOL SC_P_Ai_GetStaticMode(dword pl_id);

extern void SC_P_Ai_EnterHeli(dword pl_id, char *heli_name, dword entry_function);				
extern void SC_P_Ai_StepOutHeli(dword pl_id);

extern void SC_P_Ai_Drive(dword pl_id, char *way_filename);
extern BOOL SC_P_Ai_ThrowGrenade(dword pl_id, c_Vector3 *target, float explode_time);	

extern float SC_P_Ai_GetNearestEnemyDist(dword pl_id);			
extern dword SC_P_Ai_GetNearestEnemy(dword pl_id);				

extern void SC_P_Ai_Script_WatchPlayer(dword pl_id, dword target_pl_id, float time);
																					
																					
extern void SC_P_Ai_UpdateSituation(dword pl_id, dword target_pl_id, BOOL enable_se);

extern void SC_P_Ai_GetEnemyShotAround(dword pl_id, float max_dist);			
extern void SC_P_Ai_JumpInNextFrame(dword pl_id);								

extern void SC_P_Ai_SetIgnoreFlags(dword pl_id, dword flags);					
extern dword SC_P_Ai_GetIgnoreFlags(dword pl_id);

extern void SC_P_Ai_EnableSayTo(dword pl_id, BOOL enable);						

extern void SC_P_Ai_SetPointmanBreaks(dword pl_id, float min_interval, float max_interval); 
extern void SC_P_Ai_WalkThruAIs(dword pl_id, BOOL enable);		

extern void SC_P_Ai_SetMedicIngMaxActiveDist(dword pl_id, float distance);	


extern void SC_Ai_SetFormationType(dword side, dword group, dword type);	
extern void SC_Ai_SetFormationSize(dword side, dword group, float size);	
extern void SC_Ai_SetBattleMode(dword side, dword group, dword mode);	
extern void SC_Ai_SetBattleModeExt(dword size, dword group, dword battlemode, c_Vector3 *param);
																		
extern void SC_Ai_SetPeaceMode(dword side, dword group, dword mode);	
extern void SC_Ai_SetPointRuns(dword side, dword group, BOOL runs);

extern void SC_Ai_ClearCheckPoints(dword side, dword group);
extern void SC_Ai_AddCheckPoint(dword side, dword group, c_Vector3 *vec, dword flags);			
extern BOOL SC_Ai_GetCurCheckPoint(dword side, dword group, c_Vector3 *vec);

extern void SC_Ai_SetPlFollow(dword side, dword group, dword mode, s_SC_Ai_PlFollow *follow, dword *follow_order, dword *point_order, dword players);	
extern void SC_Ai_PointStopDanger(dword side, dword group);			
extern void SC_Ai_StopDanger(dword side, dword group, float stop_time);				

extern void SC_Ai_SetStealthMode(dword side, dword group, BOOL stealth);
extern void SC_Ai_SetStealthModeOff(dword side, dword group, float agressive_time);
extern BOOL SC_Ai_GetStealthMode(dword side, dword group);

extern void SC_Ai_EnableRelaxWalk(dword side, dword group, BOOL enable);

extern dword SC_Ai_Blocker_Add(s_sphere *sph);
extern void SC_Ai_Blocker_Remove(dword blocker_id);

extern void SC_Ai_FakeEnemy_Add(dword side, dword group, c_Vector3 *fake_enemy, dword area_spheres, s_sphere *area_sphere);
			
extern void SC_Ai_FakeEnemy_Remove(dword side, dword group, c_Vector3 *fake_enemy);												

extern void SC_Ai_FakeDanger(s_sphere *sph, float time);	
															
				
extern void SC_Ai_SetGroupEnemyUpdate(dword side, dword group, BOOL enable);
																			
extern void SC_Ai_SetPointmanNormalWalking(dword side, dword group, BOOL normal);		

extern BOOL SC_P_Ai_CanSeePlayer(dword pl_id, dword target_id, float max_dist, dword need_points);
															
															
															
															


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

extern void SC_StorySkipEnable(BOOL enable);


extern BOOL SC_NET_FillRecover(s_SC_MP_Recover *recov, char *wpname);

extern void SC_GetPls(s_sphere *sph, dword *list, dword *items);
extern void SC_GetPlsInLine(c_Vector3 *pos, c_Vector3 *dir, dword *list, dword *items);

extern void SC_SetQFStep(dword step);
extern dword SC_GetQFStep(void);
extern void SC_DisplayBinocular(BOOL enable);

extern void SC_DeathCamera_Enable(BOOL enable);
												

extern void SC_Set_GoToPC_snd(dword member_id, dword peace, dword agressive, dword stealth);
extern void SC_Set_RadioMan_RunDist(float dist);
extern BOOL SC_GetScriptHelper(char *name, s_sphere *sph);
extern void SC_MissionFailedDeathPlayer(dword death_plid);


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

extern dword SC_AGS_Set(dword val);

	
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

extern void SC_FPV_AttachMagazine(BOOL render);
extern void SC_FPV_FlyOffCartridge(s_SC_FlyOffCartridge *info);




extern void SC_NOD_SetFromANM(char *anm, float time, void *nod);
extern float SC_ANM_GetFrameTime(char *anm, int frame);
extern BOOL SC_NOD_GetPosFromANM(char *anm, float time, c_Vector3 *pos);


extern float SC_DOBJ_CameraLooksAt(void *nod, float max_dist);
extern float SC_DOBJ_CameraLooksAtCollision(void *nod, float max_dist);
extern void SC_ACTIVE_Add(void *nod, float cur_dist, dword info_txt);

extern void SC_UP_Open(dword what, dword level);

extern dword SC_MANM_Create(char *filename);
extern void SC_MANM_Release(dword manm_id);
extern dword SC_MANM_GetIndex(dword manm_id, char *objname);
extern void SC_MANM_Set(dword manm_id, dword manm_index, void *nod, float time);
extern float SC_MANM_GetLength(dword manm_id, dword manm_index);



extern void SC_DUMMY_Set_DoNotRenHier(char *dummy_name, BOOL do_not_render_hiearchy);
extern void SC_DUMMY_Set_DoNotRenHier2(void *nod, BOOL do_not_render_hiearchy);



	
extern void *SC_CAR_Create(void *nod, s_SC_Car_Init *info);
extern void SC_CAR_WheelAdd(void *car, void *nod, s_SC_Car_AddWheel *info);
extern void SC_CAR_EntryAdd(void *car, s_SC_Car_AddEntry *info);
extern void SC_CAR_SetAirResistance(void *car, float a0, float a1, float a2);




extern void *SC_SHIP_Create(void *nod, s_SC_Ship_Init *info, s_SC_PHS_IWantToFloat *finfo);
extern void SC_SHIP_EntryAdd(void *ship, s_SC_Car_AddEntry *info);




extern void *SC_HELI_Create(void *nod, s_SC_Heli_Init *info);
extern void SC_HELI_EntryAdd(void *heli, s_SC_Car_AddEntry *info);
extern void SC_HELI_ChangeEntryStativ(void *heli, dword entry_index, char *stg_name);	   




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




	extern BOOL SC_MP_RecoverAiPlayer(dword pl_id, c_Vector3 *pos, float rz);	









#line 9 "C:\Users\flori\source\repos\VC_Scripter\compiler\VCBOT5.c"
#line 0 "C:\Users\flori\source\repos\VC_Scripter\compiler\inc\sc_def.h"
 



















































































































































































 






















































































































































































































































































































































































































































#line 10 "C:\Users\flori\source\repos\VC_Scripter\compiler\VCBOT5.c"






int gphase = 0;                 
int timer = 0;                  
int enemyside = 0;              
int myside = 0;                 


c_Vector3 origpos;              
c_Vector3 myflag;               
dword pl_id = 0;                
c_Vector3 enflag;               
c_Vector3 mycurflag;            
c_Vector3 encurflag;            


int enflagstat = 0;             
float tickvalue = 0.0f;         
float origz = 0.0f;             


float standingtimer = 0.0f;     
float endtimer = 0.5f;          
float orderstimer = 0.0f;       
int myorder = 0;                
int priority = 0;               


int wasenflag = 0;              
float respawntimer = 0.0f;      
float walktimer = 0.0f;         
int firstoff = 0;               
int timeblock = 0;              
int amidead = 0;                
float inittimer = 0.0f;         
int am_flag_carrier = 0;        




c_Vector3 camp_pos;                     
c_Vector3 camp_look_pos;                
float camp_timer = 0.0f;                
float camp_duration = 0.0f;             
float camp_cooldown = 0.0f;             
int is_camping = 0;                     
int camp_found = 0;                     
float camp_scan_timer = 0.0f;           




























int buddy_role = 0;       
dword buddy_partner_id = 0;             
int buddy_leader_camping = 0;           
float buddy_follow_distance = 12.0f;    
float buddy_regroup_distance = 25.0f;   





void SetupVC(s_SC_P_Create *pinfo);
void SetupUS(s_SC_P_Create *pinfo);
void CreateBot(s_SC_P_info *info);
void InitBot(s_SC_P_info *info);
int GetMoveDirection(dword player);
int CheckNearbyPlayers(c_Vector3 *pos);
int IsNear3DHelper(dword player, c_Vector3 *targetpos, float radius);
dword FindNearestEnemy(dword player);
dword FindNearestEngagedEnemy(dword player);
int IsNearFlag(dword player);
void CheckIfCarryingFlag(void);
void SetMoveSpeed(dword player);

int IsCampSpotOccupied(c_Vector3 *camp_position);
int TryFindCampSpot(dword player);
void DoCamping(dword player, float elapsed);

void ProcessBuddyMessage(int message, dword param);
int DoBuddyBehavior(dword player, float elapsed);
void DoPatrol(dword player);
void DoAttack(dword player);
int ProcessOrderExtended(s_SC_P_info *info, int order);
void MainAILoop(s_SC_P_info *info);
void SetupBattleMode(s_SC_P_info *info);
void UpdateEnemyTracking(s_SC_P_info *info);
void UpdateFlagPositions(void);
int ProcessOrder(s_SC_P_info *info, int order);
void ProcessState(s_SC_P_info *info, int state);
int ScriptMain(s_SC_P_info *info);





 











void SetupVC(s_SC_P_Create *pinfo) {
    pinfo->inifile = "Ini\\Players\\NET_VC_UNIFORM4.ini";
    pinfo->name_nr = 2506;       
    pinfo->weap_pistol = 8;      
    pinfo->weap_main1 = 23;       
    pinfo->weap_slot1 = 50;      
    myside = 1;       
    enemyside = 0;    
}

 






void SetupUS(s_SC_P_Create *pinfo) {
    pinfo->inifile = "Ini\\Players\\net_us_sf1.ini";
    pinfo->name_nr = 2499;       
    pinfo->weap_pistol = 7;      
    pinfo->weap_main1 = 1;       
    pinfo->weap_slot1 = 59;      
    myside = 0;       
    enemyside = 1;    
}





 












void CreateBot(s_SC_P_info *info) {
    s_SC_P_Create pinfo;
    s_SC_P_CreateEqp eqp[20];

    
    SC_ZeroMem(&pinfo, 156);  

    
    pinfo.type = 2;
    pinfo.side = 1;  
    pinfo.group = 0;
    pinfo.member_id = 5;

    
    SC_ZeroMem(&eqp, 80);  
    pinfo.eqp = eqp;
    pinfo.eqps = 0;
    

    
    
    if (pinfo.side != 0) {
        SetupVC(&pinfo);
    } else {
        SetupUS(&pinfo);
    }

    
    pinfo.icon_name = "nhut";
    pinfo.weap_knife = 0;
    pinfo.recover_pos = info->pos;  

    
    info->pl_id = SC_P_Create(&pinfo);
    pl_id = info->pl_id;  
    gphase = 1;  
}





 



void InitBot(s_SC_P_info *info) {
    s_SC_P_AI_props aiprops;
    int difficulty;
    void *flagnode;

    
    SC_P_GetPos(pl_id, &origpos);
    SC_P_EnableSearchDeathBodies(pl_id, 0);
    origz = SC_P_GetRot(pl_id);

    
    SC_P_Ai_SetMode(pl_id, 1);
    SC_P_Ai_EnableShooting(pl_id, 1);

    
    SC_ZeroMem(&aiprops, 128);  
    SC_P_Ai_GetProps(pl_id, &aiprops);

    
    difficulty = SC_ggi(10);

    switch (difficulty) {
        case 0:  
            aiprops.shoot_imprecision = 1.0f;
            aiprops.reaction_time = 1.2f;
            aiprops.aimtime_max = 2.0f;
            aiprops.aimtime_canshoot = 0.8f;
            break;

        case 1:  
            aiprops.shoot_imprecision = 0.7f;
            aiprops.reaction_time = 0.4f;
            aiprops.aimtime_max = 1.4f;
            aiprops.aimtime_canshoot = 0.5f;
            break;

        case 2:  
            aiprops.shoot_imprecision = 0.3f;
            aiprops.berserk = 0.3f;
            aiprops.reaction_time = 0.2f;
            aiprops.aimtime_max = 1.0f;
            aiprops.aimtime_canshoot = 0.3f;
            break;

        case 3:  
            
            
            aiprops.shoot_imprecision = 0.1f;
            aiprops.berserk = 0.3f;
            aiprops.reaction_time = 0.1f;
            break;

        
    }

    
    
    
    aiprops.shoot_imprecision *= 1.0f;    
    aiprops.max_vis_distance = 120.0f;    
    aiprops.view_angle = 3.0f;            
    aiprops.view_angle_near = 4.0f;       
    aiprops.reaction_time *= 1.0f;        
    aiprops.hear_distance_max = 120.0f;   
    aiprops.hear_imprecision = 1.0f;      

    
    aiprops.boldness = 4.0f + frnd(3.0f);           
    aiprops.scout = 0.7f + frnd(0.3f);              
    aiprops.berserk = 0.3f + frnd(0.3f);            
    aiprops.coveramount = 0.1f + frnd(0.2f);        
    aiprops.shortdistance_fight = 0.6f + frnd(0.3f); 
    aiprops.extend_searchway = 1;                 

    
    SC_P_Ai_SetProps(pl_id, &aiprops);
    SC_P_SetSpeachDist(pl_id, 30.0f);
    
    if (rand() % 4 != 0) {
        SC_P_Ai_SetBattleMode(pl_id, 5);  
    } else {
        SC_P_Ai_SetBattleMode(pl_id, 1);     
    }

    
    if (myside == 1) {
        
        flagnode = SC_NOD_Get(0, "flag_vc");
        SC_NOD_GetWorldPos(flagnode, &myflag);

        flagnode = SC_NOD_Get(0, "flag_us");
        SC_NOD_GetWorldPos(flagnode, &enflag);
    } else {
        
        flagnode = SC_NOD_Get(0, "flag_us");
        SC_NOD_GetWorldPos(flagnode, &myflag);

        flagnode = SC_NOD_Get(0, "flag_vc");
        SC_NOD_GetWorldPos(flagnode, &enflag);
    }

    
    mycurflag = myflag;
    encurflag = enflag;

    
    enflagstat = 0;
    tickvalue = 0.0f;
    gphase = 2;  
}





 








int GetMoveDirection(dword player) {
    c_Vector3 dir;
    float len;

    SC_P_GetDir(player, &dir);
    len = SC_VectorLen(&dir);

    if (len > 1.0f) {
        return 1;  
    }

    return 0;  

    
    
}

 









int CheckNearbyPlayers(c_Vector3 *pos) {
    s_sphere searchsphere;
    dword players[64];
    dword count;

    searchsphere.pos = *pos;
    searchsphere.rad = 2.0f;

    count = 64;
    SC_GetPls(&searchsphere, players, &count);

    if (count > 0) {
        return 0;  
    }
    return 1;  
}

 








int IsNear3DHelper(dword player, c_Vector3 *targetpos, float radius) {
    c_Vector3 playerpos;

    SC_P_GetPos(player, &playerpos);
    return SC_IsNear3D(&playerpos, targetpos, radius);
}

 




dword FindNearestEnemy(dword player) {
    s_sphere searchsphere;
    s_SC_P_getinfo pinfo;
    dword players[64];
    dword count;
    dword nearest;
    float mindist, dist;
    int i;
    c_Vector3 pos;

    if (!player) return 0;

    
    SC_P_GetPos(player, &pos);
    searchsphere.pos = pos;
    searchsphere.rad = 1000.0f;

    count = 64;
    SC_GetPls(&searchsphere, players, &count);

    mindist = 10000.0f;
    nearest = 0;

    for (i = 0; i < count; i++) {
        SC_P_GetInfo(players[i], &pinfo);

        
        if (pinfo.side != myside) {
            if (SC_P_IsReady(players[i]) && SC_P_GetActive(players[i])) {
                dist = SC_P_GetDistance(player, players[i]);
                if (dist < mindist) {
                    mindist = dist;
                    nearest = players[i];
                }
            }
        }
    }

    return nearest;
}

 








dword FindNearestEngagedEnemy(dword player) {
    dword target;
    float mindist, dist;
    dword nearest;
    int i;

    mindist = 10000.0f;
    nearest = 0;

    
    for (i = 0; i < 6; i++) {
        target = SC_P_GetBySideGroupMember(enemyside, 0, i);  

        if (target && SC_P_GetActive(target) && SC_P_IsReady(target)) {
            
            if (SC_P_Ai_GetEnemies(target)) {
                dist = SC_P_GetDistance(player, target);
                if (dist < mindist) {
                    mindist = dist;
                    nearest = target;
                }
            }
        }
    }

    return nearest;
}

 









int IsNearFlag(dword player) {
    s_sphere searchsphere;
    s_SC_P_getinfo pinfo;
    dword players[64];
    dword count;
    c_Vector3 pos;
    int allies;
    int i;

    
    if (tickvalue != 0.0f) {
        return 1;
    }

    SC_P_GetPos(player, &pos);

    
    if (!SC_IsNear2D(&pos, &myflag, 30.0f)) {
        return 1;  
    }

    
    searchsphere.pos = myflag;
    searchsphere.rad = 20.0f;
    count = 64;
    SC_GetPls(&searchsphere, players, &count);

    allies = 0;
    for (i = 0; i < count; i++) {
        SC_P_GetInfo(players[i], &pinfo);
        if (pinfo.side == myside) {
            if (SC_P_IsReady(players[i]) && SC_P_GetActive(players[i])) {
                allies++;
            }
        }
    }

    
    if (allies > 1) {
        return 1;
    }
    return 0;
}





 



void CheckIfCarryingFlag(void) {
    dword carrier_handle = SC_ggi(513);  
    dword carrier = SC_MP_GetPlofHandle(carrier_handle);
    am_flag_carrier = (carrier == pl_id) ? 1 : 0;
}

 



void SetMoveSpeed(dword player) {
    if (am_flag_carrier) {
        
        SC_P_Ai_SetMoveMode(player, 2);
        SC_P_Ai_SetMovePos(player, 0);
        return;
    }

    
    if (rand() % 5 != 0) {
        SC_P_Ai_SetMoveMode(player, 2);
    } else {
        SC_P_Ai_SetMoveMode(player, 0);
    }
}





 




int IsCampSpotOccupied(c_Vector3 *camp_position) {
    s_sphere searchsphere;
    s_SC_P_getinfo pinfo;
    dword players[64];
    dword count;
    int i;

    
    searchsphere.pos = *camp_position;
    searchsphere.rad = 3.0f;
    count = 64;
    SC_GetPls(&searchsphere, players, &count);

    for (i = 0; i < count; i++) {
        
        if (players[i] == pl_id) continue;

        SC_P_GetInfo(players[i], &pinfo);

        
        if (pinfo.side == myside) {
            if (SC_P_IsReady(players[i]) && SC_P_GetActive(players[i])) {
                return 1;  
            }
        }
    }

    return 0;  
}

 













int TryFindCampSpot(dword player) {
    c_Vector3 bot_pos;
    c_Vector3 waypoint_pos;
    c_Vector3 look_pos;
    void *node;
    void *look_node;
    char camp_name[32];
    char look_name[40];
    char *prefixes[3];
    int num_prefixes;
    int p, i;
    float best_dist = 10000.0f;
    float dist;
    int found_any = 0;

    
    if (camp_cooldown > 0.0f) {
        return 0;
    }

    
    if (camp_scan_timer > 0.0f) {
        return 0;  
    }

    
    camp_scan_timer = 20.0f;

    
    if ((rand() % 100) >= 15) {
        return 0;  
    }

    SC_P_GetPos(player, &bot_pos);

    
    if (myside == 1) {
        prefixes[0] = "camp_vc_";
        prefixes[1] = "camp_uni_";
        num_prefixes = 2;
    } else {
        prefixes[0] = "camp_us_";
        prefixes[1] = "camp_uni_";
        num_prefixes = 2;
    }

    
    for (p = 0; p < num_prefixes; p++) {
        for (i = 0; i < 32; i++) {
            
            sprintf(camp_name, "%s%02d", prefixes[p], i);

            
            node = SC_NOD_Get(0, camp_name);
            if (node == 0) continue;

            
            SC_NOD_GetWorldPos(node, &waypoint_pos);

            
            if (!SC_IsNear2D(&bot_pos, &waypoint_pos, 50.0f)) {
                continue;  
            }

            
            if (IsCampSpotOccupied(&waypoint_pos)) {
                continue;  
            }

            
            dist = SC_2VectorsDist(&bot_pos, &waypoint_pos);

            if (dist < best_dist) {
                
                sprintf(look_name, "%s_look", camp_name);
                look_node = SC_NOD_Get(0, look_name);

                if (look_node != 0) {
                    
                    SC_NOD_GetWorldPos(look_node, &look_pos);

                    best_dist = dist;
                    camp_pos = waypoint_pos;
                    camp_look_pos = look_pos;
                    found_any = 1;
                }
            }
        }
    }

    if (found_any) {
        
        camp_duration = 10.0f + frnd(40.0f - 10.0f);
        camp_timer = 0.0f;
        camp_found = 1;

        
        if (buddy_role == 1 && buddy_partner_id != 0) {
            SC_P_ScriptMessage(buddy_partner_id, 202, 0);
        }

        return 1;
    }

    return 0;
}

 











void DoCamping(dword player, float elapsed) {
    c_Vector3 bot_pos;
    c_Vector3 look_dir;
    float target_rot;

    
    if (camp_cooldown > 0.0f) {
        camp_cooldown -= elapsed;
        if (camp_cooldown < 0.0f) camp_cooldown = 0.0f;
    }

    
    if (!camp_found) {
        return;
    }

    SC_P_GetPos(player, &bot_pos);

    
    if (!is_camping) {
        
        if (SC_IsNear2D(&bot_pos, &camp_pos, 2.0f)) {
            
            is_camping = 1;
            camp_timer = 0.0f;

            
            SC_P_Ai_SetMoveMode(player, 0);
            SC_P_Ai_SetMovePos(player, 1);  

            
            SC_P_Ai_LookAt(player, &camp_look_pos);
        } else {
            
            
            if (SC_P_Ai_GetSureEnemies(player)) {
                
                camp_found = 0;
                is_camping = 0;
                camp_cooldown = 30.0f / 2.0f;  
            }
        }
        return;
    }

    
    camp_timer += elapsed;

    
    SC_P_Ai_ShouldLookAt(player, &camp_look_pos, 2.0f);

    
    if (SC_P_Ai_GetSureEnemies(player)) {
        
        SC_P_Ai_SetMovePos(player, 0);
        camp_found = 0;
        is_camping = 0;
        camp_cooldown = 30.0f / 2.0f;  
        return;
    }

    
    if (camp_timer >= camp_duration) {
        
        SC_P_Ai_SetMovePos(player, 0);
        camp_found = 0;
        is_camping = 0;
        camp_cooldown = 30.0f;  
    }
}





 






void ProcessBuddyMessage(int message, dword param) {
    switch (message) {
        case 200:
            
            buddy_role = 1;
            buddy_partner_id = param;
            buddy_leader_camping = 0;
            break;

        case 201:
            
            buddy_role = 2;
            buddy_partner_id = param;
            buddy_leader_camping = 0;
            break;

        case 202:
            
            buddy_leader_camping = 1;
            break;

        case 203:
            
            buddy_role = 0;
            buddy_partner_id = 0;
            buddy_leader_camping = 0;
            break;

        case 204:
            
            buddy_role = 0;
            buddy_partner_id = 0;
            break;

        case 205:
            
            buddy_role = 0;
            buddy_partner_id = 0;
            buddy_leader_camping = 0;
            break;

        case 206:
            
            buddy_role = 2;
            buddy_partner_id = param;
            buddy_leader_camping = 0;
            break;
    }
}

 











int DoBuddyBehavior(dword player, float elapsed) {
    c_Vector3 my_pos, partner_pos, follow_pos;
    s_sphere search;
    float dist;
    int found;

    
    if (buddy_role == 0) {
        return 0;
    }

    
    if (buddy_partner_id == 0 || !SC_P_IsReady(buddy_partner_id)) {
        buddy_role = 0;
        buddy_partner_id = 0;
        return 0;
    }

    
    if (buddy_role == 1) {
        return 0;  
    }

    
    if (buddy_role == 2) {
        
        if (buddy_leader_camping) {
            return 0;  
        }

        
        SC_P_GetPos(player, &my_pos);
        SC_P_GetPos(buddy_partner_id, &partner_pos);
        dist = SC_2VectorsDist(&my_pos, &partner_pos);

        
        search.pos = partner_pos;
        search.rad = 7.0f + frnd(6.0f);  

        found = SC_GetRndWp(&search, &follow_pos);

        
        if (!found) {
            search.rad = 20.0f;
            found = SC_GetRndWp(&search, &follow_pos);
        }

        
        if (!found) {
            follow_pos = partner_pos;
        }

        
        if (dist > buddy_regroup_distance) {
            SC_P_Ai_SetMoveMode(player, 2);
            SC_P_Ai_Go(player, &follow_pos);
            return 1;  
        }

        
        if (dist > buddy_follow_distance) {
            SC_P_Ai_SetMoveMode(player, 0);
            SC_P_Ai_Go(player, &follow_pos);
            return 1;  
        }

        
        return 0;
    }

    return 0;
}

 







void DoPatrol(dword player) {
    s_sphere searchsphere;
    c_Vector3 waypoint;
    int found;
    static int patrol_state = 0;  

    
    if (IsNearFlag(player)) {
        
        
        if (enflagstat != 0 && patrol_state == 0) {
            
            patrol_state = enflagstat;
            searchsphere.pos = enflag;
            searchsphere.rad = 35.0f;

            found = SC_GetRndWp(&searchsphere, &waypoint);
            SetMoveSpeed(player);

            if (found) {
                SC_P_Ai_Go(player, &waypoint);
            } else {
                SC_P_Ai_Go(player, &searchsphere.pos);
            }
        }

        
        if (enflagstat == 0) {
            patrol_state = 0;
            searchsphere.pos = enflag;
            searchsphere.rad = 30.0f;

            found = SC_GetRndWp(&searchsphere, &waypoint);
            SetMoveSpeed(player);

            if (found) {
                SC_P_Ai_Go(player, &waypoint);
            } else {
                SC_P_Ai_Go(player, &searchsphere.pos);
            }
        }
    } else {
        
        if (rand() % 10 < 7) {
            searchsphere.pos = myflag;  
            searchsphere.rad = 15.0f;

            found = SC_GetRndWp(&searchsphere, &waypoint);
            SetMoveSpeed(player);

            if (found) {
                SC_P_Ai_Go(player, &waypoint);
            } else {
                SC_P_Ai_Go(player, &searchsphere.pos);
            }
        } else {
            SC_P_Ai_HideYourself(player, &myflag, 15.0f);  
        }
    }
}

 








void DoAttack(dword player) {
    s_sphere searchsphere;
    c_Vector3 waypoint, pos;
    dword target;
    int found;

    
    
    target = FindNearestEngagedEnemy(player);

    if (target) {
        
        if (SC_P_Ai_GetEnemies(target)) {
            SC_P_GetPos(target, &pos);
            searchsphere.pos = pos;
            searchsphere.rad = 20.0f;

            SetMoveSpeed(player);
            found = SC_GetRndWp(&searchsphere, &waypoint);

            if (found) {
                SC_P_Ai_Go(player, &waypoint);
            } else {
                SC_P_Ai_Go(player, &pos);
            }
            return;
        }
    }

    
    
    if (rand() % 3 != 0) {
        
        target = FindNearestEnemy(player);
        if (target) {
            SC_P_GetPos(target, &pos);
            searchsphere.pos = pos;
            searchsphere.rad = 25.0f;

            SetMoveSpeed(player);
            found = SC_GetRndWp(&searchsphere, &waypoint);

            if (found) {
                SC_P_Ai_Go(player, &waypoint);
            } else {
                SC_P_Ai_Go(player, &pos);
            }
        }
    } else {
        
        SC_P_GetPos(player, &pos);
        searchsphere.pos = pos;
        searchsphere.rad = 20.0f;

        SetMoveSpeed(player);
        found = SC_GetRndWp(&searchsphere, &waypoint);

        
        if (found) {
            SC_P_Ai_Go(player, &waypoint);
        }
    }
}

 



void SetupBattleMode(s_SC_P_info *info) {
    int roundtime;

    SC_P_Ai_SetMode(pl_id, 1);
    
    if (rand() % 4 != 0) {
        SC_P_Ai_SetBattleMode(pl_id, 5);  
    } else {
        SC_P_Ai_SetBattleMode(pl_id, 1);     
    }
    myorder = 0;  

    
    roundtime = SC_ggi(540);  

    
    if (roundtime >= 0) {
        gphase = 3;
        SC_P_SetActive(pl_id, 1);
    } else {
        gphase = 500;  
        SC_P_SetActive(pl_id, 0);
    }
}

 











void UpdateEnemyTracking(s_SC_P_info *info) {
    dword enemies;

    
    enemies = SC_P_Ai_GetEnemies(pl_id);

    
    if (enemies == 0) {
        standingtimer += info->elapsed_time;
    }
    

    
    if (GetMoveDirection(pl_id)) {
        standingtimer = 0.0f;
    }

    
    
    if (standingtimer > endtimer) {
        standingtimer = 0.0f;
        endtimer = 0.3f + frnd(0.7f);  
        DoAttack(pl_id);
    }
}

 









void UpdateFlagPositions(void) {
    int flagstat;
    dword carrier;
    dword item;

    
    flagstat = SC_ggi(511);  

    
    
    
    if (flagstat != enflagstat) {
        switch (flagstat) {
            case 0:  
                encurflag = enflag;
                break;

            case 1:  
                carrier = SC_ggi(513);  
                carrier = SC_MP_GetPlofHandle(carrier);
                if (carrier) {
                    SC_P_GetPos(carrier, &encurflag);
                }
                break;

            case 2:  
                item = SC_Item_Find(146);  
                if (item) {
                    SC_Item_GetPos(item, &encurflag);
                }
                break;
        }
        enflagstat = flagstat;  
    }

    
    flagstat = SC_ggi(510);  

    
    
    
    if (flagstat != tickvalue) {
        switch (flagstat) {
            case 0:  
                mycurflag = myflag;
                break;

            case 1:  
                carrier = SC_ggi(512);  
                carrier = SC_MP_GetPlofHandle(carrier);
                if (carrier) {
                    SC_P_GetPos(carrier, &mycurflag);
                }
                break;

            case 2:  
                item = SC_Item_Find(145);  
                if (item) {
                    SC_Item_GetPos(item, &mycurflag);
                }
                break;
        }
        tickvalue = flagstat;  
    }
}





 









int ProcessOrder(s_SC_P_info *info, int order) {
    switch (order) {
        case 0:
        case 1:
            
            if (IsNear3DHelper(pl_id, &mycurflag, 15.0f)) {
                SC_P_Ai_SetBattleMode(pl_id, 5);  
                myorder = 7;
                SetMoveSpeed(pl_id);
                SC_P_Ai_Go(pl_id, &encurflag);
                return 1;
            } else {
                
                SetMoveSpeed(pl_id);
                SC_P_Ai_Go(pl_id, &encurflag);
                myorder = 2;
                return 1;
            }
            break;

        case 2:
            
            if (IsNear3DHelper(pl_id, &mycurflag, 30.0f)) {
                SC_P_Ai_SetBattleMode(pl_id, 5);  
                myorder = 9;
                SetMoveSpeed(pl_id);
                SC_P_Ai_Go(pl_id, &encurflag);
                return 1;
            }
            break;

        default:
            break;
    }
    return 0;
}

 







void ProcessState(s_SC_P_info *info, int state) {
    s_sphere searchsphere;
    c_Vector3 waypoint;
    int flagstat;
    int found;

    switch (state) {
        case 0:
        case 1:
            
            myorder = 1;
            if (!ProcessOrderExtended(info, state)) {
                ProcessOrder(info, state);  
            }
            break;

        case 2:  
            if (enflagstat == 0) {
                if (IsNear3DHelper(pl_id, &encurflag, 8.0f)) {
                    SC_P_Ai_SetBattleMode(pl_id, 1);
                    SC_P_Ai_SetMode(pl_id, 0);  
                    SC_P_Ai_Go(pl_id, &encurflag);
                    SetMoveSpeed(pl_id);
                    SC_P_Ai_SetMovePos(pl_id, 0);
                    myorder = 3;
                }
            }
            break;

        case 3:  
            flagstat = SC_ggi(511);
            if (flagstat == 1) {
                SC_P_Ai_SetMode(pl_id, 1);
                myorder = 1;

                if (IsNear3DHelper(pl_id, &enflag, 15.0f)) {
                    SetMoveSpeed(pl_id);
                    searchsphere.pos = encurflag;
                    searchsphere.rad = 30.0f;

                    found = SC_GetRndWp(&searchsphere, &waypoint);
                    if (found) {
                        SC_P_Ai_Go(pl_id, &waypoint);
                    } else {
                        SC_P_Ai_Go(pl_id, &searchsphere.pos);
                    }
                }
            }
            break;

        case 4:  
            flagstat = SC_ggi(510);
            if (flagstat == 0) {
                if (IsNear3DHelper(pl_id, &myflag, 8.0f)) {
                    SC_P_Ai_SetBattleMode(pl_id, 1);
                    SC_P_Ai_SetMode(pl_id, 0);  
                    SC_P_Ai_Go(pl_id, &myflag);
                    SetMoveSpeed(pl_id);
                    SC_P_Ai_SetMovePos(pl_id, 0);
                    myorder = 5;
                }
            }
            break;

        case 5:  
            flagstat = SC_ggi(510);
            if (flagstat != 0) {
                SC_P_Ai_SetMode(pl_id, 1);
                myorder = 4;
            }

            flagstat = SC_ggi(511);  
            if (flagstat != 1) {
                SC_P_Ai_SetMode(pl_id, 1);
                myorder = 1;
            }
            break;

        case 7:  
            flagstat = SC_ggi(510);
            if (flagstat != 1) {
                SC_P_Ai_SetMode(pl_id, 1);
                myorder = 1;
            }
            break;

        case 9:
        case 10:
            
            
            
            if (enflagstat == 0) {
                myorder = 1;
            } else if (enflagstat == 1) {
                myorder = 7;
            }
            

            
            if (myorder != 9) {
                if (!ProcessOrderExtended(info, state)) {
                    ProcessOrder(info, state);
                }
            }
            break;

        default:
            break;
    }
}

 









int ProcessOrderExtended(s_SC_P_info *info, int order) {
    s_sphere searchsphere;
    c_Vector3 waypoint;
    int found;
    static int internal_flag = 0;  

    switch (order) {
        case 0:
        case 2:  
            
            internal_flag = 1;
            
            if (IsNear3DHelper(pl_id, &encurflag, 30.0f)) {
                SC_P_Ai_SetBattleMode(pl_id, 5);  
                myorder = 2;
                SetMoveSpeed(pl_id);
                SC_P_Ai_Go(pl_id, &encurflag);
                return 1;
            }
            break;

        case 1:  
            
            if (internal_flag != 0) {
                
                if (IsNear3DHelper(pl_id, &enflag, 15.0f)) {
                    internal_flag = 0;  
                    SetMoveSpeed(pl_id);

                    
                    searchsphere.pos = encurflag;
                    searchsphere.rad = 30.0f;

                    found = SC_GetRndWp(&searchsphere, &waypoint);
                    if (found) {
                        SC_P_Ai_Go(pl_id, &waypoint);
                    } else {
                        SC_P_Ai_Go(pl_id, &searchsphere.pos);
                    }
                    return 0;
                }
            }
            break;

        default:
            break;
    }

    return 0;
}

 











void MainAILoop(s_SC_P_info *info) {
    float elapsed;
    int found;
    s_sphere searchsphere;
    c_Vector3 waypoint;

    
    CheckIfCarryingFlag();

    
    if (am_flag_carrier) {
        SC_P_Ai_SetMoveMode(pl_id, 2);
        SC_P_Ai_SetBattleMode(pl_id, 5);  
        SC_P_Ai_Go(pl_id, &myflag);  
        return;  
    }

    
    
     












































    
    UpdateFlagPositions();
    ProcessState(info, myorder);

    
    walktimer -= info->elapsed_time;

    switch (myorder) {
        case 0:
            
            break;

        case 1:
            
            
            if (!SC_P_Ai_GetSureEnemies(pl_id)) {
                standingtimer += info->elapsed_time;
            }

            if (GetMoveDirection(pl_id)) {
                standingtimer = 0.0f;
            }

            
            if (standingtimer > endtimer) {
                int action;
                standingtimer = 0.0f;
                endtimer = 0.3f + frnd(0.7f);  

                

                action = rand() % 10;
                if (action < 6) {
                    DoAttack(pl_id);  
                } else if (action < 9) {
                    DoPatrol(pl_id);  
                }
                
            }
            break;

        case 2:
            
            if (walktimer < 0.0f) {
                walktimer = am_flag_carrier ? 0.2f : (1.0f + frnd(1.0f));  
                if (!GetMoveDirection(pl_id)) {
                    SetMoveSpeed(pl_id);
                    SC_P_Ai_Go(pl_id, &encurflag);
                }
            }
            break;

        case 3:
            
            if (!GetMoveDirection(pl_id)) {
                SetMoveSpeed(pl_id);
                SC_P_Ai_Go(pl_id, &encurflag);
            }
            break;

        case 4:
            
            if (walktimer < 0.0f) {
                walktimer = 1.0f;  
                if (!GetMoveDirection(pl_id)) {
                    SetMoveSpeed(pl_id);
                    SC_P_Ai_Go(pl_id, &myflag);
                }
            }
            break;

        case 5:
            
            if (!GetMoveDirection(pl_id)) {
                SetMoveSpeed(pl_id);
                SC_P_Ai_Go(pl_id, &myflag);
            }
            break;

        case 6:
            
            break;

        case 7:
            
            if (walktimer < 0.0f) {
                walktimer = am_flag_carrier ? 0.2f : (0.5f + frnd(0.5f));  
                if (!GetMoveDirection(pl_id)) {
                    SetMoveSpeed(pl_id);
                    SC_P_Ai_Go(pl_id, &mycurflag);
                }
            }
            break;

        case 8:
            
            break;

        case 9:
            
            if (walktimer < 0.0f) {
                walktimer = am_flag_carrier ? 0.2f : (0.5f + frnd(0.5f));  
                if (!GetMoveDirection(pl_id)) {
                    SetMoveSpeed(pl_id);  
                    SC_P_Ai_Go(pl_id, &mycurflag);
                }
            }
            break;

        case 10:
            
            if (!GetMoveDirection(pl_id)) {
                SetMoveSpeed(pl_id);
                SC_P_Ai_Go(pl_id, &mycurflag);
            }
            break;

        default:
            break;
    }
}





 














int ScriptMain(s_SC_P_info *info) {
    int message;
    int param1;
    float elapsed;
    int gamestate;
    s_sphere searchsphere;
    dword players[64];
    dword count;
    c_Vector3 waypoint;
    int found;

    message = info->message;
    param1 = info->param1;
    elapsed = info->elapsed_time;

    switch (message) {
        case 4:  
        case 5:  
            
            enemyside = 0;
            return 1;

        case 1:  
            return 1;

        case 3:  
            return 1;

        case 7:  
            SC_MP_ScriptMessage(100, pl_id);
            gphase = 1000;
            return 1;

        case 2:  
            
            switch (param1) {
                case 100:  
                    myorder = 4;
                    SC_P_Ai_SetBattleMode(pl_id, 5);  
                    SetMoveSpeed(pl_id);
                    SC_P_Ai_Go(pl_id, &myflag);
                    SC_P_Ai_SetMode(pl_id, 1);
                    break;

                case 666:  
                    
                    
                    respawntimer = (float)info->param2;
                    if (gphase != 1000) {
                        SC_message("SOMETHING IS WRONG! Received respawntime, but not dead! %d %d", gphase, amidead);
                    } else {
                        gphase = 1001;
                    }
                    break;

                case 2000:  
                    inittimer = 0.0f;  
                    gphase = 1;
                    break;

                case 3000:  
                    
                    
                    if (info->param2 != 0) {
                        SC_P_SetActive(pl_id, 1);
                        inittimer = 0.0f;  
                        gphase = 1;
                    } else {
                        gphase = 500;
                        SC_P_SetActive(pl_id, 0);
                    }
                    break;

                case 4000:  
                    gphase = 500;
                    SC_P_SetActive(pl_id, 0);
                    
                    break;

                
                case 200:
                case 201:
                case 202:
                case 203:
                case 204:
                case 205:
                case 206:
                    ProcessBuddyMessage(param1, info->param2);
                    break;

                default:
                    break;
            }
            return 1;

        case 0:  
        default:
            break;
    }

    
    tickvalue = 0.2f;
    info->next_exe_time = tickvalue;  

    
    
    switch (gphase) {
        case 0:
            
            
            
            CreateBot(info);
            info->next_exe_time = 0.05f;
            return 1;

        case 1:
            
            
            if (!SC_P_IsReady(pl_id)) {
                info->next_exe_time = 0.05f;
                return 1;  
            }
            InitBot(info);  
            info->next_exe_time = tickvalue;
            return 1;

        case 2:
            
            SetupBattleMode(info);  
            info->next_exe_time = tickvalue;
            return 1;

        case 3:
            
            MainAILoop(info);
            break;

        case 500:
            
            
            break;

        case 1000:
            
            
            if (SC_P_IsReady(pl_id) && SC_P_GetActive(pl_id)) {
                
                myorder = 0;
                walktimer = 0.0f;
                standingtimer = 0.0f;
                am_flag_carrier = 0;
                camp_found = 0;
                is_camping = 0;
                buddy_role = 0;
                buddy_partner_id = 0;
                gphase = 1;  
            }
            break;

        case 1001:
            
            respawntimer -= elapsed;
            if (respawntimer < 0.0f) {
                
                if (CheckNearbyPlayers(&origpos)) {
                    
                    
                    SC_MP_RecoverAiPlayer(pl_id, &origpos, origz);

                    
                    myorder = 0;
                    walktimer = 0.0f;
                    standingtimer = 0.0f;
                    am_flag_carrier = 0;
                    camp_found = 0;
                    is_camping = 0;
                    buddy_role = 0;
                    inittimer = 0.0f;

                    gphase = 1;  
                }
            }
            break;

        default:
            break;
    }

    info->next_exe_time = tickvalue;
    return 1;
}





 


void _init(void) {
    
}
