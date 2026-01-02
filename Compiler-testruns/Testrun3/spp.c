#line 0 "C:\Users\flori\source\repos\VC_Scripter\Compiler-testruns\Testrun3\hitable.c"






#line 0 "C:\Users\flori\source\repos\VC_Scripter\Compiler-testruns\Testrun3\inc\sc_global.h"
 























	




























































































													
													
													
													
												
												
												

												
												
												





												
												










												




												
												
														





												
												



												
												












































































































































































































































											
											
												






											
											


												
												


























































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

extern void SC_SpeechSet3Dto3Dincamera(BOOL incamera3D);
											
											

extern void SC_DoExplosion(c_Vector3 *pos, dword type);	
														

extern dword SC_MWP_Create(s_SC_MWP_Create *info);

extern void SC_SetObjectScript(char *obj_name, char *script_name);

extern void SC_GetPos_VecRz(void *cpos, c_Vector3 *pos, float *rz);	

extern void SC_PreloadBES(dword id, char *bes_name);	

extern void SC_PreloadWeapon(dword type, BOOL fpv_to);
extern void SC_FadeTo(BOOL black, float time);	

					
extern void SC_PreloadSound(dword snd_id, BOOL is3D);	
extern void SC_FadeSoundPlayer(dword snd_player_id, float final_volume, float fade_time);

extern ushort* SC_Wtxt(dword val);				

extern dword SC_GetNearestPlayer(c_Vector3 *vec, float *dist);

extern void SC_SetMovieBorders(BOOL set_on);

extern void SC_CreateLight(s_SC_light *info);

extern void SC_GetCameraPos(c_Vector3 *vec);

extern void SC_Fauna_DoSoundAlert(c_Vector3 *pos);
extern void SC_Fauna_KillThemAll(s_sphere *sph);



extern BOOL SC_PC_GetPos(c_Vector3 *pos);
extern dword SC_PC_Get(void);

extern void SC_PC_SetControl(BOOL user_control);				
extern void SC_PC_EnableMovementAndLooking(BOOL enable);	
extern void SC_PC_EnableMovement(BOOL enable);				
extern void SC_PC_EnablePronePosition(BOOL enable);			

extern void SC_PC_EnableWeaponsUsing(BOOL enable);			



extern dword SC_P_Create(s_SC_P_Create *info);	
extern BOOL SC_P_IsReady(dword pl_id);					
extern char *SC_P_GetName(dword pl_id);

extern void SC_P_GetPos(dword pl_id, c_Vector3 *pos);
extern float SC_P_GetRot(dword pl_id);
extern void SC_P_GetInfo(dword pl_id, s_SC_P_getinfo *info);

extern dword SC_P_GetBySideGroupMember(dword iside, dword igroup, dword imember);

extern void SC_P_ScriptMessage(dword pl_id, dword param1, dword param2);	

extern void SC_P_SetFaceStatus(dword pl_id, dword face_type, float time);
												
extern void SC_P_SetHandVariation(dword pl_id, dword hand_id, dword variation, float time);
												
												
												

extern float SC_P_GetDistance(dword pl_id, dword to_pl_id);



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

extern float SC_P_Ai_GetNearestEnemyDist(dword pl_id);			
extern dword SC_P_Ai_GetNearestEnemy(dword pl_id);				

extern void SC_P_Ai_Script_WatchPlayer(dword pl_id, dword target_pl_id, float time);
																					
																					
extern void SC_P_Ai_UpdateSituation(dword pl_id, dword target_pl_id, BOOL enable_se);

extern void SC_P_Ai_GetEnemyShotAround(dword pl_id, float max_dist);			

extern void SC_P_Ai_SetIgnoreFlags(dword pl_id, dword flags);					
extern dword SC_P_Ai_GetIgnoreFlags(dword pl_id);

extern void SC_P_Ai_EnableSayTo(dword pl_id, BOOL enable);						

extern void SC_P_Ai_SetPointmanBreaks(dword pl_id, float min_interval, float max_interval); 
extern void SC_P_Ai_WalkThruAIs(dword pl_id, BOOL enable);		

extern void SC_P_Ai_SetMedicIngMaxActiveDist(dword pl_id, float distance);	


extern void SC_Ai_SetBattleMode(dword side, dword group, dword mode);	
extern void SC_Ai_SetBattleModeExt(dword size, dword group, dword battlemode, c_Vector3 *param);
																		
extern void SC_Ai_SetPeaceMode(dword side, dword group, dword mode);	
extern void SC_Ai_SetPointRuns(dword side, dword group, BOOL runs);

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

extern void SC_DisplayBinocular(BOOL enable);

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


extern float SC_DOBJ_CameraLooksAt(void *nod, float max_dist);
extern float SC_DOBJ_CameraLooksAtCollision(void *nod, float max_dist);
extern void SC_ACTIVE_Add(void *nod, float cur_dist, dword info_txt);


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








#line 7 "C:\Users\flori\source\repos\VC_Scripter\Compiler-testruns\Testrun3\hitable.c"
#line 0 "C:\Users\flori\source\repos\VC_Scripter\Compiler-testruns\Testrun3\inc\sc_def.h"
 



















































































































































































 






















































































































































































































































































































































































































































#line 8 "C:\Users\flori\source\repos\VC_Scripter\Compiler-testruns\Testrun3\hitable.c"



int ScriptMain(s_SC_OBJ_info *info){

	switch(info->event_type){
		case 3:

			return 1;	
			

		case 7:
			break;

		case 5:
			break;

		case 1:			
			SC_LevScr_Event(52,(dword)info->master_nod);
			break;

		case 4:
			break;

		case 6:
			break;

	}


	return 0;

}
