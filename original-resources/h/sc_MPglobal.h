/*
*	sc_MPglobal.h
*
*	Ptero-Engine-II : Main script include file for the multiplayer scripting, defines extern engine functions 
 	DO NOT CHANGE THIS FILE!!!
*/


#ifndef SC_GLOBAL_H
#define SC_GLOBAL_H 


#define _GE_VERSION_		138			// game engine version to compile for


// number of global variables accesed by SC_sgi, SC_ggi, SC_sgf ,SC_ggf and SC_MP_Gvar_SetSynchro functions
#define SC_GLOBAL_VARIABLE_MAX			4096
	

// values for s_SC_P_Create::type
#define SC_P_TYPE_PC					1
#define SC_P_TYPE_AI					2


// values for s_SC_P_Create::side
#define SC_P_SIDE_US					0
#define SC_P_SIDE_VC					1
#define SC_P_SIDE_NEUTRAL				2



// values for s_SC_OBJ_info::event_type
#define SC_OBJ_INFO_EVENT_HIT					1
#define SC_OBJ_INFO_EVENT_SET					2
#define SC_OBJ_INFO_EVENT_INIT					3
#define SC_OBJ_INFO_EVENT_DOTICK				4
#define SC_OBJ_INFO_EVENT_RELEASE				5
#define SC_OBJ_INFO_EVENT_USED					6
#define SC_OBJ_INFO_EVENT_JUSTLOADED			7
#define SC_OBJ_INFO_EVENT_MOUNTEDSHOT			8

// values for s_SC_OBJ_info::hit_by
#define SC_OBJ_HIT_BY_MISSILE					1
#define SC_OBJ_HIT_BY_EXPLOSION					2
#define SC_OBJ_HIT_BY_MISSILE_PC				3


// value for s_SC_L_info::message
#define SC_LEV_MES_TIME						0
#define SC_LEV_MES_RADIOUSED				1
#define SC_LEV_MES_SPEACHDONE				2
#define SC_LEV_MES_VIEWANIMCALLBACK			3		// info->param1 includes callback_id defined in SC_SetViewAnim()
#define SC_LEV_MES_EVENT					4
#define SC_LEV_MES_POINTINTERACT			5		// info->param1 includes status of pointman
													// 0 - hold or follow mode (default action is 'command point')
													// 1 - moves as a point (default action is 'command stop')
													// 2 - moves as a point, but waits for the rest of the team (default action is nothing)
													// info->param2 includes pl_id of pointman
												// return value from the script:
												//		TRUE - script solved the situation - engine do nothing
												//		FALSE - script ignored the situation  engine do default action
#define SC_LEV_MES_POINTINTERACTINFO		6
												// same as SC_LEV_MES_POINTINTERACT
												// game asks script for text to be displayed when looking at pointman
												// text id is filled into info->param3

#define SC_LEV_MES_INITSCENE				7	// is called just after scene loaded ( new start or load gamesave)
#define SC_LEV_MES_RELEASESCENE				8
#define SC_LEV_MES_ARTILLERY				9	//	param4 is center
#define SC_LEV_MES_LOUDSHOTCALLBACK			10	// callback for SC_GetLoudShot()
												// param1 - pl_id of player who has shot
												// param4 - position of the shot
#define SC_LEV_MES_JUSTLOADED				11
#define SC_LEV_MES_MUSICDONE				12	// param1 - music id
#define SC_LEV_MES_LIGHTSTICK_USED			13
#define SC_LEV_MES_STORYSKIP				14
#define SC_LEV_MES_GETMUSIC					15


// values for s_SC_NET_info::message
#define SC_NET_MES_UNDEFINED				0
#define SC_NET_MES_LEVELINIT				1	// param1 - TRUE - server, FALSE - client
												// param2 - TRUE - first time, FALSE - reinit
#define SC_NET_MES_RENDERHUD				2	// param1 - TRUE when dedicated server
#define SC_NET_MES_SERVER_TICK				3
#define SC_NET_MES_CLIENT_TICK				4
#define SC_NET_MES_SERVER_RECOVER_TIME		5	// param1 - pl_id hrace
												// param2 - just_connected									
												// OUT: info->fval1 - time to recover, 
														// use SC_NET_SERVER_RECTIME_xxx for special cases
		#define SC_NET_SERVER_RECTIME_NEVER			-1.0f
		#define SC_NET_SERVER_RECTIME_ENDOFROUND	-10.0f


#define SC_NET_MES_SERVER_RECOVER_PLACE		6	// param1 - side
												// OUT: param2 - s_SC_MP_Recover *
												// param3 - pl_id
#define SC_NET_MES_SERVER_KILL				7	// param1 - who is killed, param2 - who killed him
#define SC_NET_MES_MESSAGE					8
#define SC_NET_MES_LEVELPREINIT				9	// mission preinit ( level is not loaded yet)
												// param1 - end rule
												// param2 - end value
#define SC_NET_MES_RESTARTMAP				10	// clears statisticks, end_rule and recovers players
#define SC_NET_MES_RULESCHANGED				11	// information about endrule change


// values for s_SC_SOUND_info::message
#define SC_SOUND_MESSAGE_INIT				1



#define SC_MP_P_STATUS_NOTINGAME			0
#define SC_MP_P_STATUS_INGAME				1
#define SC_MP_P_STATUS_INGAMEDEATH			2

#define SC_MP_ENUMPLAYER_SIDE_ALL			0xffffffff


#define SC_EXPL_TYPE_GRENADE				1
#define SC_EXPL_TYPE_M72					2
#define SC_EXPL_TYPE_MORTAR					3

#define SC_PRELOAD_BES_MAXID					64

#define SC_P_LINK3PV_MAX						4

#define SC_P_RADARCOLOR_DISABLE					0xff000000
#define SC_P_RADARCOLOR_DEFAULT					0xfe000000

#define SC_P_MESH_AREA_BODYFRONT			0
#define SC_P_MESH_AREA_BODYBACK				1
#define SC_P_MESH_AREA_LEFTARM				2
#define SC_P_MESH_AREA_RIGHTARM				3
#define SC_P_MESH_AREA_LEFTLEG				4
#define SC_P_MESH_AREA_RIGHTLEG				5
#define SC_P_MESH_AREA_HEAD					6


// values for s_SC_MP_hud 
#define SC_HUD_MP_PL_MASK_COUNT				6
#define SC_HUD_MP_PL_MASK_CLASS				0x01
#define SC_HUD_MP_PL_MASK_POINTS			0x02
#define SC_HUD_MP_PL_MASK_FRAGS				0x04
#define SC_HUD_MP_PL_MASK_KILLS				0x08
#define SC_HUD_MP_PL_MASK_DEATHS			0x10
#define SC_HUD_MP_PL_MASK_PINGS				0x20

#define SC_HUD_MP_SIDE_MASK_POINTS			0x01
#define SC_HUD_MP_SIDE_MASK_FRAGS			0x02

#define SC_HUD_MP_SORTBY_NONE				0
#define SC_HUD_MP_SORTBY_POINTS				1
#define SC_HUD_MP_SORTBY_FRAGS				2
#define SC_HUD_MP_SORTBY_KILLS				3
#define SC_HUD_MP_SORTBY_DEATHS				4
#define SC_HUD_MP_SORTBY_PINGS	    		5
#define SC_HUD_MP_SORT_DOWNUP				0x80000000

// MP end rules
#define SC_MP_ENDRULE_TIME					0
#define SC_MP_ENDRULE_FRAGS					1
#define SC_MP_ENDRULE_POINTS				2



// do not change these values! 
#define SC_SNDPLAYER_GAME			0
#define SC_SNDPLAYER_SPEECH			1
#define SC_SNDPLAYER_HELI			2
#define SC_SNDPLAYER_BEEP			3
#define SC_SNDPLAYER_NATURE			5
#define SC_SNDPLAYER_SCRIPT0		6
#define SC_SNDPLAYER_SCRIPT1		7

// do not change these values! 



// do not change these values! 

// global variable id for storing current MP mission type
#define GVAR_MP_MISSIONTYPE							499
#define GVAR_MP_MISSIONSUBTYPE						498

// predefined values, use some other for own MP missiontypes
#define GVAR_MP_MISSIONTYPE_DM						1
#define GVAR_MP_MISSIONTYPE_TDM						2
#define GVAR_MP_MISSIONTYPE_ATG						3
#define GVAR_MP_MISSIONTYPE_LMS						4
#define GVAR_MP_MISSIONTYPE_CTF						5
#define GVAR_MP_MISSIONTYPE_CTR						6
#define GVAR_MP_MISSIONTYPE_COOP					7
#define GVAR_MP_MISSIONTYPE_RW						8
#define GVAR_MP_MISSIONTYPE_TT						9



// defines of pre-defined respawn type for MP
#define SC_MP_RESPAWN_ALL			0
#define SC_MP_RESPAWN_DM			1
#define SC_MP_RESPAWN_WA			3
#define SC_MP_RESPAWN_WB			4
#define SC_MP_RESPAWN_WC			5
#define SC_MP_RESPAWN_WD			6
#define SC_MP_RESPAWN_WE			7
#define SC_MP_RESPAWN_WF			8

#define SC_MP_RESPAWN_CTF_US		9
#define SC_MP_RESPAWN_COOP			10
#define SC_MP_RESPAWN_ATG_US		11
#define SC_MP_RESPAWN_ATG_PILOT		12
#define SC_MP_RESPAWN_RW_US			13

#define SC_MP_RESPAWN_CTF_VC		14
#define SC_MP_RESPAWN_ATG_VC		15
#define SC_MP_RESPAWN_RW_VC			16

#define SC_MP_RESPAWN_TT_DEF_0		17
#define SC_MP_RESPAWN_TT_DEF_1		18
#define SC_MP_RESPAWN_TT_DEF_2		19
#define SC_MP_RESPAWN_TT_DEF_3		20
#define SC_MP_RESPAWN_TT_DEF_4		21
#define SC_MP_RESPAWN_TT_ATT_1		22
#define SC_MP_RESPAWN_TT_ATT_2		23
#define SC_MP_RESPAWN_TT_ATT_3		24
#define SC_MP_RESPAWN_TT_ATT_4		25
#define SC_MP_RESPAWN_TT_ATT_5		26


#define SC_P_CREATE_AEG_VALID_MAX				8




// variable types definition and some general defines


#ifndef _PTEN_


	#define FALSE		0
	#define TRUE		1

	#define NULL		0


	#define FLT_MAX         3.402823466e+38F

	#define PI			3.141592654f

	#define CLEAR(a) SC_ZeroMem(&a,sizeof(a))

	#define RAD_TO_DEG(a)				(a*57.2957795131f)
	#define DEG_TO_RAD(a)				(a*0.0174532925199f)

	typedef unsigned int dword;	

	typedef unsigned short ushort;	


	typedef int BOOL;
	
	typedef struct {
		float x,y,z;
	}c_Vector3;// struct c_Vector3
	
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

#endif 
	// #ifndef _PTEN_


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
	dword weap_main2;	// second weapon or special kid (medbag, ammo, radio)
	dword weap_slot1;	// usually for medkit

	dword weap_slot6;
	dword weap_slot7;
	dword weap_slot8;
	dword weap_slot9;
	dword weap_slot10;	

	dword force_sel_slot;	

	dword eqps;
	s_SC_P_CreateEqp *eqp;

	dword aeg_valid_head_bes[SC_P_CREATE_AEG_VALID_MAX];
	dword aeg_valid_body_bes[SC_P_CREATE_AEG_VALID_MAX];

}s_SC_P_Create;


typedef struct{	
	dword message,param1,param2,param3;
	float elapsed_time;
	float next_exe_time;
	c_Vector3 param4;
}s_SC_L_info;

typedef struct{

	dword MaxHideOutsStatus;			// how much HDs is in occupied database
	dword MaxGroups;

}s_SC_initside;

typedef struct{

	dword SideId;
	dword GroupId;
	dword MaxPlayers;

	float NoHoldFireDistance;			// when enemy is closer than this distance, shoot at him
	float follow_point_max_distance;
	
}s_SC_initgroup;


typedef struct{

	float cur_hp,max_hp;
	dword side;
	dword group;
	dword member_id;
	
}s_SC_P_getinfo;


typedef struct{

	dword event_type;		// SC_OBJ_INFO_EVENT_xxxx
	void *master_nod;
	void *nod;	
	float new_hp_obtained;
	dword hit_by;			// value is SC_OBJ_HIT_BY_xxxx
	c_Vector3 *world_pos;
	c_Vector3 *world_dir;
	float time;				// for SC_OBJ_INFO_EVENT_DOTICK

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

/*

SC_NET_MES_LEVELINIT
	param1 - 0 - client only
			 1 - client & server
	param2 - 0 - restart mission
			 1 - first init

SC_NET_MES_SERVER_RECOVER_TIME
	param1 - pl_id
	param2 - 0 - player has been killed
			 1 - just connected to the game


#define SC_NET_MES_SERVER_RECOVER_PLACE		6
	param1 - player side
	param2 - (s_SC_MP_Recover *) - point at structure to be filled
	param3 - pl_id

*/
  



typedef struct{

	dword id;
	dword side;
	dword status;	// is valid on server only, SC_MP_P_STATUS_xxxx
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



#define SC_HUD_MP_ICON_TYPE_NONE		0
#define SC_HUD_MP_ICON_TYPE_NUMBER		1
#define SC_HUD_MP_ICON_TYPE_TIME		2

typedef struct{
	dword icon_id;  // index to 2D array of icons (while icon_id is > then first dim of array, then skip one line of array )
	dword type;     // tells how member value must be interpreted: SC_HUD_MP_ICON_TYPE_xxxxx
	int value;	    // 4 bytes which represents value to show
	dword color;	// ARGB color for icon and value
}s_SC_HUD_MP_icon;


typedef struct{
	dword message;		// SC_SOUND_MESSAGE_
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


#if _GE_VERSION_ >= 138

typedef struct{
	dword id;	
	dword color;
	float scale;
	c_Vector3 pos;
}s_SC_FpvMapSign;

#endif

// global integer variables
extern void SC_sgi(dword id, int a);
extern int SC_ggi(dword id);

// global float variables
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


extern void SC_message(char *txt,...);				// displays message box
extern void SC_Log(dword level, char *txt, ...);	// write to the log file, level 0 - fatal error, 1 - error, 2 - warning, 3 - info
extern void SC_Osi(char *txt,...);					// write text on the screen (left bottom corner)

extern BOOL SC_StringSame(char *a, char *b);

extern void SC_EventImpuls(char *ev_name);
extern void SC_EventEnable(char *ev_name, BOOL enable);	// enable/disable the event


extern void SC_SetMissileTrace(dword color, float alpha);

extern void SC_CreatePtc(dword id, c_Vector3 *vec);
extern void SC_CreatePtc_Ext(dword id, void *nod, float time, float interval, float scale, float time_mult);
					// creates particle in nod, but subeffects are in world space
extern void SC_CreatePtcVec_Ext(dword id, c_Vector3 *vec, float time, float interval, float scale, float time_mult);
extern void SC_CreatePtcInNodSpace_Ext(dword id, void *nod, float time, float interval, float scale, float time_mult);
					// all particle is in nod space ( better for flames f.e.)
						// id - id of particle
						// nod - position
						// time - time to play this particle (0 only once)
						// interval - interval between 2 particles (0 means interval defined in particle)
						// scale - scale of particle

extern ushort *SC_AnsiToUni(char *src, ushort *dest);

extern void SC_Fnt_Write(float x, float y, char *txt, float scale, dword color);
extern float SC_Fnt_GetWidth(char *txt, float scale);

extern void SC_Fnt_WriteW(float x, float y, ushort *txt, float scale, dword color);
extern float SC_Fnt_GetWidthW(ushort *txt, float scale);


extern void SC_GetScreenRes(float *width, float *height);


extern void SC_RadioSetDist(float max_dist_subtitle_write);

extern void SC_DoExplosion(c_Vector3 *pos, dword type);	// for server only in MP
														// type is SC_EXPL_TYPE_xxxx
extern void SC_ArtillerySupport(BOOL enable);
extern void SC_SetMapFpvModel(char *bes_filename);

extern void SC_SetSceneVisibilityMult(float vis_mult, float scene_fog_mult, float bckg_fog_mult);
				// 1.0f - default visibility, 2.0f - twotimes bigger visibility

extern void SC_SetObjectScript(char *obj_name, char *script_name);

extern BOOL SC_SphereIsVisible(s_sphere *sph);
extern void SC_GetPos_VecRz(void *cpos, c_Vector3 *pos, float *rz);	// pos or rz can be NULL

extern void SC_MakeBurning(s_sphere *sph);				// sets on fire everything in sphere (objects and players)

extern void SC_PreloadBES(dword id, char *bes_name);	// preload, max id is from interval [1,SC_PRELOAD_BES_MAXID]

extern void SC_GetLoudShot(s_sphere *sph);

extern float SC_GetVisibility(void);
extern float SC_GetPCZoom(void);

extern void SC_PreloadWeapon(dword type, BOOL fpv_to);
extern void SC_FadeTo(BOOL black, float time);	// time==0.0f - immediatelly

extern void SC_ShowMovieInfo(dword *txt);						// txt[0],txt[1],txt[2] - show 3 lines of info
																// txt==NULL - disable it
extern void SC_HUD_DisableRadar(BOOL disable);

					
extern void SC_PreloadSound(dword snd_id, BOOL is3D);	// preloads sound
extern void SC_FadeSoundPlayer(dword snd_player_id, float final_volume, float fade_time);// final_volume 0 - off, 1 - full volume

extern ushort* SC_Wtxt(dword val);				// get texts from texts database

extern dword SC_GetNearestPlayer(c_Vector3 *vec, float *dist);

extern void SC_SwitchSceneSCS(char *fname, float time);			// switch scene settings

extern BOOL SC_GetRndWp(s_sphere *sph, c_Vector3 *wp);			// returns	- TRUE - found random wp in sphere
																//			- FALSE - no wp found

extern void SC_GetCameraPos(c_Vector3 *vec);

extern void SC_GetSystemTime(s_SC_systime *info);

extern void SC_Fauna_DoSoundAlert(c_Vector3 *pos);
extern void SC_Fauna_KillThemAll(s_sphere *sph);



// PC
extern BOOL SC_PC_GetPos(c_Vector3 *pos);
extern dword SC_PC_Get(void);

extern void SC_PC_SetControl(BOOL user_control);				// FALSE - camera is not set in PC and PC cannot be controlled
extern void SC_PC_EnableMovementAndLooking(BOOL enable);	// FALSE - camera is set in PC and PC cannot be controlled
extern void SC_PC_EnableMovement(BOOL enable);				// FALSE - player cannot move , but can look around)
extern void SC_PC_EnablePronePosition(BOOL enable);			// default is TRUE, use FALSE to disable lieing ( in tunnels f.e.)

extern void SC_PC_EnableWeaponsUsing(BOOL enable);			// default is TRUE, use FALSE to disable shooting, weapons, change, reload, mode changing

extern void SC_PC_EnableExit(BOOL enable);				// default value is TRUE
extern void SC_PC_EnableEnter(BOOL enable);				// default value is TRUE

extern float SC_PC_PlayFpvAnim(char *filename);
extern float SC_PC_PlayFpvAnim2(char *filename, dword plb_id, char *eqp, char *anm);
													// bes - object to link - index to PreLoadBes  ( SC_PreloadBES )
													// eqp - how to link
													// anm - animation of object, can be NULL

extern void SC_PC_PlayFpvLooped(char *filename);	// fpv animation to play looped, use NULL to stop fpv animation

extern void SC_PC_EnableFlashLight(BOOL enable);	// default is FALSE


// player

extern BOOL SC_P_IsReady(dword pl_id);					// returns whether player is ready (is created and recovered, but death)
extern char *SC_P_GetName(dword pl_id);
extern void SC_P_ChangeSideGroupMemId(dword pl_id, dword side, dword group, dword mem_id);
extern void SC_P_SetForceClassName(dword pl_id, dword name_nr);

extern BOOL SC_P_GetWeapons(dword pl_id, s_SC_P_Create *info);	// only weap_xxxx members are valid



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

extern BOOL SC_P_GetHasShoot(dword pl_id);		// returns TRUE when player shot from the last function call
extern dword SC_P_GetCurWeap(dword pl_id);


extern void SC_P_Link3pvEqp(dword pl_id, dword slot_id, dword plb_id, char *eqp_name);	// slot_id is [0,SC_P_LINK3PV_MAX-1]
extern void SC_P_UnLink3pvEqp(dword pl_id, dword slot_id);								// slot_id is [0,SC_P_LINK3PV_MAX-1]

extern void SC_P_AddAllAmmo(dword pl_id);
extern void SC_P_AddAmmoNoGrenade(dword pl_id);


extern void SC_P_ChangeWeapon(dword pl_id, dword slot_id, dword weap_type);
extern void SC_P_SetSelWeapon(dword pl_id, dword slot_id);
extern float SC_P_GetPhase(dword pl_id);     // 0-stand, 1-crouch, 2-lie
extern void SC_P_SetPhase(dword pl_id, dword phase);     // 0-stand, 1-crouch ( lie is not supported )

extern float SC_P_GetDistance(dword pl_id, dword to_pl_id);

extern void SC_P_DoHit(dword pl_id, dword area_id, float hp);
extern void SC_P_SetRadarColor(dword pl_id, dword val);	// val is SC_P_RADARCOLOR_xxxxx or RGB color
extern void SC_P_SetNoAmmo(dword pl_id);
extern void SC_P_CloseEyes(dword pl_id, BOOL force_close);

extern void SC_P_SetAmmo(dword pl_id, dword ammo_type, dword amount);

extern BOOL SC_P_UsesBinocular(dword pl_id);
extern void SC_P_EnableBinocular(dword pl_id, BOOL enable);	// default value is TRUE

// level stuff
extern BOOL SC_GetWp(char *wpname, c_Vector3 *vec);

extern void SC_SetSideAlly(dword s1, dword s2, float status);	// 0 - neutral, 1 - ally, -1 - enemy
extern void SC_InitSide(dword id, s_SC_initside *init);
extern void SC_InitSideGroup(s_SC_initgroup *info);
extern dword SC_GetGroupPlayers(dword side, dword group);

extern dword SC_Item_Create(dword id, c_Vector3 *vec);						// returns 'netid' of item
extern dword SC_Item_Create2(dword id, c_Vector3 *vec, c_Vector3 *movdir);	// returns 'netid' of item
extern void SC_Item_Preload(dword id);
extern BOOL SC_Item_GetPos(dword netid, c_Vector3 *pos);
extern void SC_SRV_Item_Release(dword netid);
extern dword SC_Item_Find(dword item_type);			// returns net_id, 0 when not found

extern void SC_LevScr_Event(dword param1, dword param2);

extern BOOL SC_NET_FillRecover(s_SC_MP_Recover *recov, char *wpname);

extern void SC_GetPls(s_sphere *sph, dword *list, dword *items);
extern void SC_GetPlsInLine(c_Vector3 *pos, c_Vector3 *dir, dword *list, dword *items);

extern void SC_DisplayBinocular(BOOL enable);

extern BOOL SC_GetScriptHelper(char *name, s_sphere *sph);

// sound
extern BOOL SC_SND_SetEnvironment(dword env1_id, dword env2_id, float env_ratio);

extern void SC_SND_Ambient_Play(dword snd_id);
extern void SC_SND_Ambient_Stop(void);

extern void SC_SND_PlaySound3D(dword snd_id, c_Vector3 *pos);
extern void SC_SND_PlaySound3Dex(dword snd_id, c_Vector3 *pos, float *timeout);
extern void SC_SND_PlaySound2D(dword snd_id);

#if _GE_VERSION_ >= 136
extern void SC_SND_PlaySound3Dlink(dword snd_id, void *nod, float *timeout);	// timeout can be NULL, 
																				// otherwise - IN : delay before sound is played
																				//			   OUT: IN + sound length
#endif



extern void SC_SND_PlaySound3Dpl(dword snd_id, dword pl_id, dword flags);// flags SND_PLAY_PL_FL_xxxx
			// play sound linked to player


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

	// for dynamics
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

// other objects functions

extern void SC_NOD_SetFromANM(char *anm, float time, void *nod);
extern float SC_ANM_GetFrameTime(char *anm, int frame);
extern BOOL SC_NOD_GetPosFromANM(char *anm, float time, c_Vector3 *pos);


extern float SC_DOBJ_CameraLooksAt(void *nod, float max_dist);
extern float SC_DOBJ_CameraLooksAtCollision(void *nod, float max_dist);
extern void SC_ACTIVE_Add(void *nod, float cur_dist, dword info_txt);

// scene rendering
extern void SC_DUMMY_Set_DoNotRenHier(char *dummy_name, BOOL do_not_render_hiearchy);
extern void SC_DUMMY_Set_DoNotRenHier2(void *nod, BOOL do_not_render_hiearchy);



// Multiplayer scripting


extern BOOL SC_MP_EnumPlayers(s_SC_MP_EnumPlayers *list, dword *items, dword side);	
			// *items : IN - size of list array
			//			OUT - number of players filled
			//			side - side_id or SC_MP_ENUMPLAYER_SIDE_ALL

extern void SC_MP_RestartMission(void);

extern void SC_MP_P_SetRecoverTime(dword pl_id, float time);
extern dword SC_MP_P_GetAfterRecoverSide(dword pl_id);	// returns side of player after his respawn

extern dword SC_MP_P_GetClass(dword pl_id);
extern dword SC_MP_P_GetAfterRecoverClass(dword pl_id);

extern void SC_MP_AddPlayerScript(char *filename);	// filename is *.c name of the script

extern void SC_MP_SRV_SetForceSide(dword side);
extern void SC_MP_SRV_SetClassLimit(dword class_id, dword limit);
extern void SC_MP_SRV_SetClassLimitsForDM(void);


extern dword SC_MP_SRV_GetBestDMrecov(s_SC_MP_Recover *list, dword items, float *no_recov_time, float max_recov_time);


extern void SC_MP_SRV_InitWeaponsRecovery(float time);	// 0 - recover immediatelly, >0 - recover after time, <0 - hide items

extern void SC_MP_HUD_SetTabInfo(s_SC_MP_hud *info);
extern void SC_MP_HUD_SelectPl(dword pl_id, dword color);

extern void SC_GameInfo(dword text_id, char *text);	// if text_id==0, text is used
extern void SC_GameInfoW(ushort *text);
extern void SC_P_MP_AddPoints(dword pl_id, int val);

extern dword SC_MP_GetMaxPointsPl(int *points);
extern dword SC_MP_GetMaxFragsPl(int *frags);

extern dword SC_MP_GetHandleofPl(dword pl_id);
extern dword SC_MP_GetPlofHandle(dword pl_handle);

extern void SC_HUD_RadarShowPlayer(dword pl_id, dword color);
extern void SC_HUD_RadarShowPos(c_Vector3 *vec, dword color);
extern void SC_MP_SRV_P_SetObtainedDamageMult(dword pl_id, float mult);	// 1-normal, 0.5-has 2x 'more HP',
extern void SC_MP_SetSideStats(dword side, int frags, int points);
extern void SC_MP_ScriptMessage(dword param1, dword param2);	// send SC_NET_MES_MESSAGE to mp script
extern void SC_MP_AllowStPwD(BOOL enable);		// Switch to Players when Death
extern void SC_MP_AllowFriendlyFireOFF(BOOL enable);		// set TRUE for TeamBased Games, FALSE for others ( DM, CTR, LMS )
extern void SC_MP_SetIconHUD(s_SC_HUD_MP_icon *icon, dword icons);
extern void SC_MP_SetInstantRecovery(BOOL enable);
extern void SC_MP_SetItemsNoDisappear(BOOL nodisappear);
extern void SC_MP_EnableBotsFromScene(BOOL enable);			// default value when starting mission is FALSE
extern void SC_MP_SetChooseValidSides(dword mask);			// 1 - us, 2 - nva
extern void SC_MP_EnableC4weapon(BOOL enable);				// calling with TRUE for ATG bombing gametypes

extern void SC_MP_LoadNextMap(void);
extern void SC_MP_SetTeamGame(BOOL teamgame);
extern void SC_MP_RecoverAllNoAiPlayers(void);					// for MP only, valid on server only
extern void SC_MP_RecoverAllAiPlayers(void);					// for MP only, valid on server only

extern void SC_MP_EndRule_SetTimeLeft(float val, BOOL counting);				// set's info about time left
extern void SC_MP_GetSRVsettings(s_SC_MP_SRV_settings *info);	// returns setting of server for various game types
extern BOOL SC_MP_SRV_P_SetSideClass(dword pl_id, dword side, dword class_id);

extern BOOL SC_MP_SRV_GetAutoTeamBalance(void);
extern int SC_MP_SRV_GetTeamsNrDifference(BOOL after_respawn);
extern void SC_MP_SRV_DoExplosion(c_Vector3 *pos, dword type);

extern void SC_MP_SRV_ClearPlsStats(void);
extern void SC_MP_SRV_InitGameAfterInactive(void);

extern BOOL SC_MP_GetAmmoBoxesEnabled(void);
extern void SC_MP_SRV_GetAtgSettings(s_SC_MP_SRV_AtgSettings *info);


#if _GE_VERSION_ >= 133
	extern void SC_MP_SetSpectatorCameras(char character);
	extern void SC_MP_GetRecovers(dword type, s_SC_MP_Recover *list, dword *items);// items is a size of list and after function end it contains number of recovers stored there
#endif

#if _GE_VERSION_ >= 136
	extern void SC_MP_RecoverPlayer(dword pl_id);
#endif

#if _GE_VERSION_ >= 138
	extern dword SC_MP_FpvMapSign_Load(char *fname);
	extern BOOL SC_MP_FpvMapSign_Unload(dword id);
	extern void SC_MP_FpvMapSign_Set(dword signs, s_SC_FpvMapSign *list);	
#endif


//gvars imported from sc_def.h

#define SGI_LEVELPHASE								6			//gphase of level.c
#define SGI_DIFFICULTY								10











#endif 
//#ifndef SC_GLOBAL_H



