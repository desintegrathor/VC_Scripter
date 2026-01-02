/*
*	sc_global.h
*
*	Ptero-Engine-II : Main script include file, defines extern engine functions 
*	
*	M.Janacek 18.7.2001
*/



// DO NOT CHANGE THIS FILE AS IT IS ALREADY COMPILED WITH THE GAME ENGINE 
// and changing of defines, structures and functions would cause problems



#ifndef SC_GLOBAL_H
#define SC_GLOBAL_H 


#define _GE_VERSION_		158			// game engine version to compile for


// number of global variables accesed by SC_sgi, SC_ggi, SC_sgf ,SC_ggf and SC_MP_Gvar_SetSynchro functions
#define SC_GLOBAL_VARIABLE_MAX			4096
	

// values for s_SC_P_Create::type
#define SC_P_TYPE_PC					1
#define SC_P_TYPE_AI					2


// values for s_SC_P_Create::side
#define SC_P_SIDE_US					0
#define SC_P_SIDE_VC					1
#define SC_P_SIDE_NEUTRAL				2


// values for SC_P_Ai_SetMode
#define SC_P_AI_MODE_SCRIPT				0
#define SC_P_AI_MODE_BATTLE				1

// values for SC_P_Ai_SetBattleMode and SC_P_Ai_SetBattleModeExt
#define SC_P_AI_BATTLEMODE_HOLD					0
#define SC_P_AI_BATTLEMODE_ATTACK				1
#define SC_P_AI_BATTLEMODE_RETREAT				2
#define SC_P_AI_BATTLEMODE_GOTO					3
#define SC_P_AI_BATTLEMODE_FOLLOW				4
#define SC_P_AI_BATTLEMODE_ATTACKAGR			5

// values for SC_Ai_SetPeaceMode
#define SC_P_AI_PEACEMODE_HOLD					0
#define SC_P_AI_PEACEMODE_FOLLOW				1
#define SC_P_AI_PEACEMODE_POINT					2
#define SC_P_AI_PEACEMODE_SEARCHDEATHBODIES		3


// values for SC_P_Ai_SetMoveMode
#define SC_P_AI_MOVEMODE_WALK			0
#define SC_P_AI_MOVEMODE_AIM			1
#define SC_P_AI_MOVEMODE_RUN			2

// values for SC_P_Ai_SetMovePos
#define SC_P_AI_MOVEPOS_STAND			0
#define SC_P_AI_MOVEPOS_CROUCH			1
#define SC_P_AI_MOVEPOS_LIE				2


// values for s_SC_P_Create::member_id
#define SC_P_MEMBERID_CAPTAIN			0
#define SC_P_MEMBERID_POINT				1
#define SC_P_MEMBERID_MEDIC				2
#define SC_P_MEMBERID_DEMOLITION		3
#define SC_P_MEMBERID_RADIO				4
#define SC_P_MEMBERID_MACHINEGUN		5

#define SC_P_MEMBERID_NR				6		// number of member ids


// flags for s_SC_P_Create::flags
#define SC_P_CREATE_FL_MP_RECOVER		1			// player is recovered by multiplayer script
#define SC_P_CREATE_FL_DISABLE_EQPGEN	2			// disble automatic equipment generation when eqps==0
#define SC_P_CREATE_FL_CROUCH			4			// player is created crouching
#define SC_P_CREATE_FL_INACTIVE			8			// create player as inactive
#define SC_P_CREATE_FL_FORCESELSLOT		16			// flags for PC only - player will be created with selected weapon in slot info.force_sel_slot


#define SC_P_INTEL_MAX		10

#define SC_AI_CP_FL_NOSKIP				1

#define SC_AI_FOLLOWMODE_POINT			0
#define SC_AI_FOLLOWMODE_FOLLOW			1


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

#define SC_CAR_ENTRY_FUNC_ENTER				0
#define SC_CAR_ENTRY_FUNC_DRIVER			1
#define SC_CAR_ENTRY_FUNC_SEAT				2


// values for s_SC_WEAP_info::anim_id
#define SC_WEAP_INFO_ANIM_ID_UNDEFINED				0
#define SC_WEAP_INFO_ANIM_ID_RELOAD					1
#define SC_WEAP_INFO_ANIM_ID_SHOOT					2
#define SC_WEAP_INFO_ANIM_ID_CHANGEMODE				3
#define SC_WEAP_INFO_ANIM_ID_TAKE					4
#define SC_WEAP_INFO_ANIM_ID_HIDE					5
#define SC_WEAP_INFO_ANIM_ID_GRENATETHROWUP			6
#define SC_WEAP_INFO_ANIM_ID_GRENATETHROWDOWN		7
#define SC_WEAP_INFO_ANIM_ID_GRENADE_PREPAREUP		8
#define SC_WEAP_INFO_ANIM_ID_GRENADE_PREPAREDOWN	9
#define SC_WEAP_INFO_ANIM_ID_BORING1				10
#define SC_WEAP_INFO_ANIM_ID_BORING2				11
#define SC_WEAP_INFO_ANIM_ID_BORING3				12
#define SC_WEAP_INFO_ANIM_ID_DROP					13
#define SC_WEAP_INFO_ANIM_ID_BAYONET_SHOW			14
#define SC_WEAP_INFO_ANIM_ID_BAYONET_HIDE			15
#define SC_WEAP_INFO_ANIM_ID_BAYONET_USE			16


// values for s_SC_WEAP_info::event_type
#define SC_WEAP_EVENTTYPE_SET					1
#define SC_WEAP_EVENTTYPE_INIT					2
#define SC_WEAP_EVENTTYPE_RELEASE				3
#define SC_WEAP_EVENTTYPE_VALIDATEANIM			4
#define SC_WEAP_EVENTTYPE_GETANIMTIME			5

#define SC_MPW_LINK_AT_NONE						0
#define SC_MPW_LINK_AT_HELI						1


// values for SC_P_SetHandVariation
#define SC_P_HAND_LEFT							0
#define SC_P_HAND_RIGHT							1

// values for SC_P_SetHandVariation
#define SC_P_HANDVAR_DEFAULT					0
#define SC_P_HANDVAR_COUNT1						1
#define SC_P_HANDVAR_COUNT2						2
#define SC_P_HANDVAR_COUNT3						3
#define SC_P_HANDVAR_COUNT4						4
#define SC_P_HANDVAR_COUNT5						5
#define SC_P_HANDVAR_PALM						6
#define SC_P_HANDVAR_FIST						7
#define SC_P_HANDVAR_OK							8
#define SC_P_HANDVAR_FUCK						9
#define SC_P_HANDVAR_ARSCH						10


#define SC_PRELOAD_BES_MAXID					64

#define SC_P_LINK3PV_MAX						4


// indexses for s_SC_P_SpecAnims::sa
#define SC_PL_SA_STATIV				0
#define SC_PL_SA_ENEMYSPOTTED		1
#define SC_PL_SA_WALK				2
#define SC_PL_SA_RUN				3
#define SC_PL_SA_DEATH				4

#define SC_PL_SA_MAX				5


// values for s_SC_WEAP3pv_info::event_type
#define SC_WEAP3PV_EVENTTYPE_INIT				0
#define SC_WEAP3PV_EVENTTYPE_SHOT				1
#define SC_WEAP3PV_EVENTTYPE_RELOAD				2
#define SC_WEAP3PV_EVENTTYPE_SETBAYONET			3


// values for s_SC_Objective::status
#define SC_OBJECTIVE_STATUS_VALID				0
#define SC_OBJECTIVE_STATUS_FAILED				1
#define SC_OBJECTIVE_STATUS_COMPLETE			2

#define SC_P_CREATE_AEG_VALID_MAX				8


#define SC_P_RADARCOLOR_DISABLE					0xff000000
#define SC_P_RADARCOLOR_DEFAULT					0xfe000000


// values for s_SC_P_Create::debrief_group
#define SC_P_DEBRIEFGROUP_UNDEFINED				0
#define SC_P_DEBRIEFGROUP_SF					1
#define SC_P_DEBRIEFGROUP_LLDB					2
#define SC_P_DEBRIEFGROUP_CIDG					3
#define SC_P_DEBRIEFGROUP_CIVIL					4
#define SC_P_DEBRIEFGROUP_VC					5

#define SC_DEBRIEF_STATUS_INPROGRESS			0
#define SC_DEBRIEF_STATUS_COMPLETED				1
#define SC_DEBRIEF_STATUS_FAILED				2

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
#define SC_PL_AI_SIT_IFL_CAR				0x01					// ignore all players in cars
#define SC_PL_AI_SIT_IFL_HELI				0x02					// ignore all players in heli
#define SC_PL_AI_SIT_IFL_SHIP				0x04					// ignore all players in ship
#define SC_PL_AI_SIT_IFL_MWP				0x08					// ignore all players in using mwp

#define SC_PL_AI_SIT_IFL_S0G0				0x10					// ignore all players side 0, group 0 
#define SC_PL_AI_SIT_IFL_S0G1				0x20
#define SC_PL_AI_SIT_IFL_S0G2				0x40
#define SC_PL_AI_SIT_IFL_S0G3				0x80

#define SC_PL_AI_SIT_IFL_S1G0				0x0100
#define SC_PL_AI_SIT_IFL_S1G1				0x0200
#define SC_PL_AI_SIT_IFL_S1G2				0x0400
#define SC_PL_AI_SIT_IFL_S1G3				0x0800

#define SC_PL_AI_SIT_IFL_S2G0				0x1000
#define SC_PL_AI_SIT_IFL_S2G1				0x2000
#define SC_PL_AI_SIT_IFL_S2G2				0x4000
#define SC_PL_AI_SIT_IFL_S2G3				0x8000


#define SC_PL_AI_SPEC_TASK_NONE					0
#define SC_PL_AI_SPEC_TASK_HEAL					1
#define SC_PL_AI_SPEC_TASK_HEALMYSELF			2
#define SC_PL_AI_SPEC_TASK_AMMO					3
#define SC_PL_AI_SPEC_TASK_GOTOPC				4

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



//#define SND_PLAY_PL_FL_NOKILLSTOP				0x01			// obsolete


#define SC_HELI_INIT_FL_DISABLE_GROUNDDUST		1


// values for s_SC_ScriptHelper_info::event_type
#define SC_SCRHELPER_EVENTTYPE_INIT			1
#define SC_SCRHELPER_EVENTTYPE_RELEASE		2
#define SC_SCRHELPER_EVENTTYPE_TIMETICK		3



// values for s_SC_P_info::message
#define SC_P_MES_TIME				0
#define SC_P_MES_HIT				1
											// param1 is pl_id of shooter, but CAN BE 0 in some special cases !
											//		- TEST IT FOR 0 EVERYTIME YOU USE IT
												
#define SC_P_MES_EVENT				2
#define SC_P_MES_DOANIMEND			3
#define SC_P_MES_INTERACT_GETTEXT	4		// return value in param1, if zero, no interaction possible
#define SC_P_MES_INTERACT_DO		5		// interaction was enabled and pc used it
#define SC_P_MES_DROPOUTCAR			6
#define SC_P_MES_KILLED				7
											// param1 is pl_id of shooter, but CAN BE 0 in some special cases !
											//		- TEST IT FOR 0 EVERYTIME YOU USE IT
#define SC_P_MES_SHOTAROUNDCALLBACK	8		// param1 is shooter pl_id
#define SC_P_MES_GOTOPC				9		// when script sets param1 to
												//	1  - no implicit calling process is made and PC's voice is heard
												//	2  - no implicit calling process is made and PC's voice is not heard

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
	dword debrief_group;	// SC_P_DEBRIEFGROUP_xxxx
	char *inifile;
	void *recover_pos;	
	char *icon_name;

	dword flags;		// SC_P_CREATE_FL_

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

	dword force_sel_slot;	// valid when SC_P_CREATE_FL_FORCESELSLOT

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

	float max_vis_distance;				// how far can see
	float watchfulness_zerodist;		// how he can recognize enemies at near distance
	float watchfulness_maxdistance;		// how he can recognize enemies at maximum distance
	float boldness;						// odvaha - 0.5- very low, 1 - low, 2-medium, 4-high,10-suicide - ma vliv na vykukovani z krytu kdyz okolo litaj kulky
	float coveramount;					// normal 0.2 - jak daleko se maximalne bezi schovat vuci vzdalenost nejblizsiho EN
	float shoot_imprecision;			// 0 - absolutely exact aim, 1 - very bad aiming, default is 0.2
	
	BOOL extend_searchway;				// FALSE - do not use (recommended for enemies)
										// TRUE - use extended searchway (recommended for player's group)
	float shortdistance_fight;			// 0 - do not use
										// 1 - use as much as possible
										// - computing very expensive, use 0.2 (in average) for enemies, 1 for player's group
	float view_angle;					// 2.5f is default, for allies is recommended 4.7 (1.5*PI)
	float view_angle_near;				// 3.5f is default, for allies is recommended 6 (nearly 2*PI)

	float hear_imprecision;				// 0 - absolute hearing, 1 - average hering, 5 - bad hearing
	float hear_distance_mult;			// 0.5 - half, 1 - normal, 2 - two-times better
	float hear_distance_max;			// default is 1000.0f

	float grenade_min_distance;			// minimal distance to throw grenade at (default: 10.0f)
	float grenade_timing_imprecision;	// random max + in sec						(default: 0.5f)
	float grenade_throw_imprecision;	// 0 - totally exact, 1 - normal		(default: 1.0f)
	float grenade_sure_time;			// how long player makes sure about valid situation to throw grenade (default: 5.0f sec)

	float forget_enemy_mult;			// how fast ai forgots enemies , 1.0f default, 2.0f - 2times faster, 0.5f - 2times slower
	float shoot_damage_mult;			// multiple of the damage player causes

	BOOL disable_peace_crouch;			// when TRUE, player never crouches in peace mode (except crouching bellow obstacles when moving) 

	float peace_fakeenemy_run;			// 0 - walk, 1 - run, 0.3 70%walk, 30%run, default 1.0f
	float peace_fakeenemy_phase;		// 0 - stand, 1 - crouch, default 0.5f

	float shoot_while_hidding;			// 0-1	(0-never, 1-ever), default is 0.3f

	float reaction_time;				// used when spotting first enemy, default is 0.0f for side 0, and 1.0f for the rest
	float scout;						// if AI going to check spotted first enemies (0-never, 1 - ever), default is 0.0f
	float berserk;						// if AI is in Attack mode - if attack withouot hidding himself (0-never, 1- ever), default is 0.0f

	float aimtime_max;					// maximalni cas pro zamireni, default 0.7f
	float aimtime_canshoot;				// hodnota 'casu', pod kterou jiz muze strilet, default 0.1f
	float aimtime_rotmult;				// nasobitel otoceni, default 0.5f

	float wounded_start_perc;			// hodnota hp/max_hp pri ktere se zacina uplatnovat zhorsovani mireni
	float wounded_aimtime_mult_max;		// hodnota nasobku zamirovaciho casu pri hp==0
	float wounded_shoot_imprec_plus;	// hodnota zvetseni shoot_imprecision pri hp==0

}s_SC_P_AI_props;


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
	// pri zmene nezapomen na c_GAM_player::Save()	
	float Position;				// 0-1  (0-stand allways, 1-crouch always)
	float Aim;					// 0-1  (0-never, 1-ever) - remeber: while aiming, the movement is slowed down
	float Run;					// 0-1  (0-walk allways, 1-run always)
	// pri zmene nezapomen na c_GAM_player::Save()
}s_SC_P_Ai_BattleProps;



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

	dword event_type;
	void *obj;
	void *weap_type;
	dword anim_id;
	float anim_time;
	float prev_time;
	c_Vector3 pos;
	dword cur_batch;
	dword cur_ammo;
	dword cur_phase;		// 0 - stand, 1 - crouch, 2 - lie
	float param1;			// SC_WEAP_EVENTTYPE_VALIDATEANIM:  in: fps of animation
							//									out: time of animation
	dword cur_bayonet;		// & 0x80000000 - is or isn't set
							// & 0x7fffffff - number of hits to someplayer
	dword weap_phase;		// for multi-phased weapons ( claymore for example )
	
#if _GE_VERSION_ >= 137
	float step_time;		// valid for SC_WEAP_EVENTTYPE_SET from v1.37
#endif

}s_SC_WEAP_info;


typedef struct{

	dword event_type;		// SC_WEAP3PV_EVENTTYPE_xxxx
	void *obj;
	void *weap_type;
	dword cur_batch;
	dword cur_ammo;
	dword cur_phase;		// 0 - stand, 1 - crouch, 2 - lie
	dword pl_id;			// pl_id - valid for
	dword cur_bayonet;		// the same value as in s_SC_WEAP_info cur_bayonet

}s_SC_WEAP3pv_info;


typedef struct{
	dword event_type;		// SC_SCRHELPER_EVENTTYPE_xxxx
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

	void *master_nod;	// name of object is used for save/load

	void *steeringwheel_nod;
	float steeringwheel_max_rot;	// max rotation, must be adjucted according to driver animation

	float steer_max;
	float steer_speed;
	float steer_backspeed;
	float steer_curse[11];	// index 'x' - real steer angle when steer is (x * 0.1)

	float steer_max_mult_at10mpersec;
	float steer_speed_mult_at10mpersec;
	float steer_backspeed_mult_at10mpersec;
							
	float eng_max_revs;			// max otacky za minutu
	float eng_freewheel_revs;	// otacky motoru pri volnobehu
	float eng_revs_slowdown;
	float eng_min_revs;			// minimalni pouzitelne otacky motoru (pouziva automaticka spojka)
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

	c_Vector3 body_point;		// bod na karoserii kde je upevnen zaves kola (v souradnicich karoserie)
	c_Vector3 body_vector;		// vektor pruzeni kola (od body_point do stredu kola)
	//c_Vector3 wheel_axis;		// osa kolem ktere rotuje kolo, ukazuje ven z auta
	float spring_tmin;			// velikost maximalne ztlaceneho tlumice
	float spring_tmax;			// velikost maximalne natazeneho tlumice
	float spring_t;				// aktualni nastaveni tlumice
	float spring_absorber;		// maximalni zpetna rychlost kola (tlumeni)
	float spring_looser;		// brzdeni tlumeni (napr. 2.0)
	float spring_rate;			// tuhost pruziny, //float rate=(obj->weight*gravity.Length()/(obj->spring_tmax[i]-((obj->spring_tmax[i]+obj->spring_tmin[i])*3.0f/4.0f)))/obj->wheels;
	float wheel_radius;			// polomer kola
	float wheel_friction;		// treni (max zrychleni m/s)
//	float wheel_a0;				//										5
//	float wheel_a1;				//										10			
	float wheel_aspd;			// rychlost rotace kola rad/sec
	BOOL wheel_with_drive;		// jestli ma nahon, if true - pouziva se wheel_aspd, jinak je rychlost kola dopocitana automaticky
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
	dword switch_3pv_anim_dir;//1-forward,3-right,5-back,7-left
	
	char *stg_dir;
	BOOL can_shoot;
	BOOL disabled_for_PC;
	float rz;

}s_SC_Car_AddEntry;


typedef struct{

	dword pl_back_txt,pl_back_snd;		// message player says when usign radio after break
	dword ra_back_txt,ra_back_snd;

	dword ra_where_ru_nr;				// how many messages is filled in ra_where_ru_txt and ra_where_ru_snd
	dword ra_where_ru_txt[5];			// message radio says when player breaks communication, [0] for the first time, then random ([1],[ra_where_ru_nr-1])
	dword ra_where_ru_snd[5];

}s_SC_SpeachBreakProps;



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
	// pri zmene nezapomen na c_GAM_player::Save()
	dword valid_uses;					// default is 100
	float use_interval;					// default is 30.0f	
	float cur_interval;					// default is 0.0f	 - is decreasing by engine when valid_uses>0
	// pri zmene nezapomen na c_GAM_player::Save()
}s_SC_P_Ai_Grenade;



typedef struct{	
	float min_dist,max_dist;
	c_Vector3 follow_change;	
}s_SC_Ai_PlFollow;



typedef struct{	

	void *master_nod;	// name of object is used for save/load

	float steer_max;
	float steer_speed;
	float steer_backspeed;	
							
	float eng_max_revs;			// max otacky za minutu
	float eng_freewheel_revs;	// otacky motoru pri volnobehu
	float eng_revs_slowdown;
	
	c_Vector3 eng_sound_pos;
	c_Vector3 drive_pos;
	
	float eng_freqmult_1,eng_freqmult_revs1;
	float eng_freqmult_2,eng_freqmult_revs2;

	dword eng_snd_id;

	float power_front,power_back;

}s_SC_Ship_Init;



typedef struct{
	
	c_Vector3 _env_normal;	// watter level normalized normal vector
	c_Vector3 _hydI;	// direction vector, where your boot will have front
	c_Vector3 _hydJ;	// direction vector, where your boot will have starboard
	c_Vector3 _hydK;	// direction vector to the sky
	float _CI;	// fluid drag coefficient in _hydI direction
	float _CJ;	// fluid drag coefficient in _hydJ direction
	float _CK;	// fluid drag coefficient in _hydK direction
	float _QR;	// angular speed of boot stabilizing rotation
	float _QI;	// angular acceleration to get stabilizing rotation in hydI direction
	float _QJ;	// angular acceleration to get stabilizing rotation in hydJ direction
	float _QIJ;	// angular acceleration to get stabilizing rotation in whole plane [hydI,hydJ]
	float _FK;// fluid drag coefficient for boot rotation in _hydK axis

}s_SC_PHS_IWantToFloat;

typedef struct{
	dword savename_id;
	dword description_id;
	BOOL disable_info;		// TRUE - do not write info about game save on the screen
}s_SC_MissionSave;



typedef struct{
	c_Vector3 camera_pos;
	c_Vector3 camera_dir;
}s_SC_RC_info;


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

	void *master_nod;	// name of object is used for save/load
	dword eng_snd_id;
	dword snd2_id;
	float snd2_turndown_dist;
	float snd2_zerodist_volume;	// 1 - full volume, 0 - absolute zero velomu
	dword flags;		// SC_HELI_INIT_FL_xxxx

}s_SC_Heli_Init;



typedef struct{	
	dword weap_type;			// id of weapon type from weap.txt

	dword use_info_txt_id;		// text to be displayer when looking at
	dword exit_info_txt_id;		// text to be displayer when using it

	void *master_nod;			// it's name is used for scene mwp identification
	void *nod_base;				// base of weapon ( AI uses for recognizing position in scene)
	void *nod_rotate_x;			// dummy to rotate up/down
	void *nod_rotate_z;			// dummy to rotate left/right
	void *nod_rotate_last;		// nod_rotate_x of nod_rotate_y (the one, which is 'lower' in hiearchy) (for camera movement)
	void *nod_fpv_camera;		// place, where camera is places
	void *nod_active_pos;		// center of detection sphere ( used for interaction)
	void *nod_muzzle;
	void *nod_entry;			// centre of 3pv animation
		

	float active_rad;			// radius of detection sphere
	float active_dist;			// max distance of detection sphere from camera when

	float rotate_zmin,rotate_zmax;		// limit angles
	float rotate_xmin,rotate_xmax;		// limit angles
	float rotate_speed;					// 1.0f - the same as player rotation speed

	float flash_rot_step;		// 0 means all rotations possible, value bigger then PI means no rotation possible

	// for use on heli
	dword link_at;				// SC_MPW_LINK_AT_xxxx
	void *link_ptr;				// ptr at heli/car/ship
	dword link_entry_index;		// which entry has this mwp

	char *anim_dir;

}s_SC_MWP_Create;



typedef struct{

	char *sa[SC_PL_SA_MAX];	// indexes are SC_PL_SA_xxx
							// filenames are relativ to G\CHARACTERS\Anims\specmove\
							// NULL means no special animation

}s_SC_P_SpecAnims;


typedef struct{
	void *weap_type;			// type of weapon ( for cartridge model ) - can by ptr at c_tweap ( used for weapons), of just tweap_id ( used for mounted weapons)
	void *from;					// start nod
	c_Vector3 dir;				// untransformed direction to fly off	
	c_Vector3 add_rot;			// change in rotation per second
}s_SC_FlyOffCartridge;


typedef struct{
	dword text_id;
	dword status;		// SC_OBJECTIVE_STATUS_xxxxxx
}s_SC_Objective;



typedef struct{

	float	missionTime;				//time in seconds
	dword	difficulty;
	dword	missionStatus;

	//friendly losses
	dword	SF;							//number of KIA
	dword	LLDB;
	dword	CIDG;
	dword	Heli;						//number of damaged
	dword	Jeep;

	//statistics
	dword	VC;							//x KIA
	dword	Gaz;						//damaged
	dword	Boobytrap;					//eliminated
	dword	Caches;						//secured
	dword	Tunnels;
	dword	Facilities;
	dword	Intelligence;

	//personal statistics
	dword	Bangs;						//x KIA
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

	int   musId;			//id of music to play; if 0, currently playing music is adjusted; if -1 no changes of music are done.
	int   musVol;			//volume of music
	float musFadeIn;		//music fade IN time
	float musPlayTime;		//how long is music playing with full volume (musVol)
	float musFadeOut;		//music fade OUT time
	int   heliVol;			//volume of heli player; the heli player is faded tho this value after musFadeIn time; if -1, no action is taken;
	int   gameVol;			//volume of game player; the game player is faded tho this value after musFadeIn time; if -1, no action is taken;
	int	  natureVol;		//volume of nature player

}s_MusicDef;

typedef struct{
	dword chats[9];
	dword radistmarks;
	dword radiomarks;
}s_SC_BombInfo;


typedef struct{
	dword intel[SC_P_INTEL_MAX];
}s_SC_P_intel;

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

extern BOOL SC_KeyJustPressed(dword id);			// uses DirectInput codes
extern BOOL SC_KeyPressed(dword id);				// uses DirectInput codes

extern void SC_EventImpuls(char *ev_name);
extern void SC_EventEnable(char *ev_name, BOOL enable);	// enable/disable the event

extern void SC_MissionCompleted(void);
extern void SC_MissionFailed(void);
extern void SC_MissionFailedEx(dword music_id, dword start_volume);
extern void SC_MissionDone(void);	// directly switches to next mission
extern void SC_TheEnd(void);		// used on the end of the game

//extern void SC_SetView(char *anm_name, float time);	// removed
extern void SC_SetViewAnim(char *anm_name, dword start_frame, dword end_frame, dword callback_id);
extern void SC_SetViewAnimEx(char *anm_name, dword start_frame, dword end_frame, dword callback_id, void *nod);

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


extern void SC_SpeachRadio(dword speach_txt, dword snd_id, float *timeout);
extern void SC_SpeachRadioMes(dword speach_txt, dword snd_id, float *timeout, dword param);

extern void SC_SpeechRadio2(dword speech_txt, float *timeout);
extern void SC_SpeechRadioMes2(dword speech_txt, float *timeout, dword param);


extern void SC_Radio_Enable(dword radio_id);
extern void SC_Radio_Disable(dword radio_id);

extern BOOL SC_Radio_Get(dword *radio_id);// no radio is active - returns FALSE
											// some radio is active - returns TRUE and fills *radio_id

extern void SC_RadioBatch_Begin(void);
extern void SC_RadioBatch_End(void);

extern void SC_RadistBatch_Begin(void);
extern void SC_RadistBatch_End(void);

extern void SC_RadioSet2D(BOOL willbe2D);	// TRUE - from this moment all inserted SC_SpeechRadio... will be in 2D
											// default is FALSE
extern void SC_SpeechSet3Dto3Dincamera(BOOL incamera3D);
											// TRUE - all 3D speech will be played in camera ( useful for briefings)
											// default is FALSE
extern void SC_RadioSet3DButDistanceLimit(BOOL enable);											
											// default is FALSE
											
											

extern float SC_RadioGetWillTalk(void);


extern void SC_RadioBreak_Set(s_SC_SpeachBreakProps *props);
extern void SC_RadioBreak_Get(s_SC_SpeachBreakProps *props);
extern void SC_RadioSetDist(float max_dist_subtitle_write);

extern void SC_MissionSave(s_SC_MissionSave *info);

extern void SC_DoExplosion(c_Vector3 *pos, dword type);	// for server only in MP
														// type is SC_EXPL_TYPE_xxxx
extern void SC_ArtillerySupport(BOOL enable);
extern void SC_SetBombInfo(s_SC_BombInfo *info);

extern void SC_SetMapFpvModel(char *bes_filename);

extern dword SC_MWP_Create(s_SC_MWP_Create *info);

extern void SC_SetSceneVisibilityMult(float vis_mult, float scene_fog_mult, float bckg_fog_mult);
				// 1.0f - default visibility, 2.0f - twotimes bigger visibility

extern void SC_SetObjectScript(char *obj_name, char *script_name);

extern void SC_ClearImpossibleWayTargets(void);

extern BOOL SC_SphereIsVisible(s_sphere *sph);
extern void SC_GetPos_VecRz(void *cpos, c_Vector3 *pos, float *rz);	// pos or rz can be NULL

extern void SC_MakeBurning(s_sphere *sph);				// sets on fire everything in sphere (objects and players)

extern void SC_PreloadBES(dword id, char *bes_name);	// preload, max id is from interval [1,SC_PRELOAD_BES_MAXID]

extern void SC_SetObjectives(dword objectives, s_SC_Objective *objective, float force_display_time);
extern void SC_SetObjectivesNoSound(dword objectives, s_SC_Objective *objective, float force_display_time);
extern void SC_GetLoudShot(s_sphere *sph);

extern void SC_SetCommandMenu(dword text_id);	// 0 - means CommandMenu enabled
												// !=0 - this text is written
extern float SC_GetVisibility(void);
extern float SC_GetPCZoom(void);

extern void SC_ShowHelp(dword *txt, dword texts, float time);
														// texts = 0.0f = hide window
														// time = 0.0f - forever

extern void SC_PreloadWeapon(dword type, BOOL fpv_to);
extern void SC_FadeTo(BOOL black, float time);	// time==0.0f - immediatelly

extern void SC_SetAmmobagAmmo(dword ammo_type, BOOL enable);	// ammo_type viz weap.txt

extern void SC_ShowMovieInfo(dword *txt);						// txt[0],txt[1],txt[2] - show 3 lines of info
																// txt==NULL - disable it
extern void SC_Debrief_Clear(void);
extern void SC_Debrief_Add(s_SC_DebriefInfo *add_info);
extern void SC_Debrief_Get(s_SC_DebriefInfo *info);

extern void SC_HUD_DisableRadar(BOOL disable);

extern void SC_HUD_TextWriterInit(s_SC_HUD_TextWrite *initdata);
extern void SC_HUD_TextWriterRelease(float fade_out_time);


extern void SC_CreateMissile(dword missile_id, dword author_pl_id, c_Vector3 *from, c_Vector3 *at);
							// NEFUNGUJE SITOVE, STRELA NEDAVA DAMAGE
							// missile_id - id of missile from weap.txt
							// author_pl_id - pl_id of author
							//				- can be NULL, but then AI do not take notice of this missile
							// from - start position of the missile
							// at - target - used for direction, sizeof trajectory depends on missile_id
					
extern void SC_PreloadSound(dword snd_id, BOOL is3D);	// preloads sound
extern void SC_FadeSoundPlayer(dword snd_player_id, float final_volume, float fade_time);// final_volume 0 - off, 1 - full volume

//extern char* SC_Utxt(dword val);				// obsolete
extern ushort* SC_Wtxt(dword val);				// get texts from texts database

extern dword SC_GetNearestPlayer(c_Vector3 *vec, float *dist);

extern void SC_SwitchSceneSCS(char *fname, float time);			// switch scene settings
extern void SC_RemoveItems(s_sphere *area, dword item_type);	// valid in single player only

extern BOOL SC_GetRndWp(s_sphere *sph, c_Vector3 *wp);			// returns	- TRUE - found random wp in sphere
																//			- FALSE - no wp found

extern void SC_Ai_SetShootOnHeardEnemyColTest(BOOL do_test);
extern void SC_SetMovieBorders(BOOL set_on);


extern void SC_EnableBloodWhenHit(BOOL enable); // default is TRUE ( function written just for tutorial )

extern void SC_CreateLight(s_SC_light *info);

extern void SC_EnableCharacterLOD(BOOL enable);	// default is TRUE, use FALSE for briefings and other noingame special situations

extern void SC_EnableObjectScriptWhileUnipage(void *master_nod, BOOL enable);
extern void SC_GetCameraPos(c_Vector3 *vec);

extern void SC_EnableQuickSave(BOOL enable); // default is TRUE

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

extern void SC_PC_EnableRadioBreak(BOOL enable);		// default value is FALSE


extern float SC_PC_PlayFpvAnim(char *filename);
extern float SC_PC_PlayFpvAnim2(char *filename, dword plb_id, char *eqp, char *anm);
													// bes - object to link - index to PreLoadBes  ( SC_PreloadBES )
													// eqp - how to link
													// anm - animation of object, can be NULL

extern void SC_PC_PlayFpvLooped(char *filename);	// fpv animation to play looped, use NULL to stop fpv animation

extern void SC_PC_EnableFlashLight(BOOL enable);	// default is FALSE

extern void SC_PC_EnableHitByAllies(BOOL enable);	// default is FALSE
extern void SC_PC_EnablePickup(BOOL enable);		// default is TRUE

extern void SC_PC_SetIntel(s_SC_P_intel *info);
extern void SC_PC_GetIntel(s_SC_P_intel *info);

// player

extern dword SC_P_Create(s_SC_P_Create *info);	// returns player_id
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

extern void SC_P_SetToHeli(dword pl_id, char *heli_name, dword entry_index);	// entry_index is < 0 , entries-1 >
extern void SC_P_ExitHeli(dword pl_id, c_Vector3 *new_pos);
extern BOOL SC_P_HasWeapon(dword pl_id, dword weap_type);
extern void SC_P_SetToShip(dword pl_id, char *ship_name, dword entry_index);	// entry_index is < 0 , entries-1 >
extern void SC_P_ExitShip(dword pl_id, c_Vector3 *new_pos);
extern void SC_P_SetToCar(dword pl_id, char *car_name, dword entry_index);	// entry_index is < 0 , entries-1 >
extern void SC_P_SetToSceneMwp(dword pl_id, char *mwp_name);
extern void SC_P_ExitSceneMwp(dword pl_id);


extern BOOL SC_P_GetHasShoot(dword pl_id);		// returns TRUE when player shot from the last function call
extern dword SC_P_GetCurWeap(dword pl_id);


extern void SC_P_Recover(dword pl_id, c_Vector3 *pos, float rz);	// valid for singleplayer only!
extern void SC_P_Recover2(dword pl_id, c_Vector3 *pos, float rz, dword phase);	// phase 0 - stand, 1-crouch


extern float SC_P_GetWillTalk(dword pl_id);	// returns time in sec, when player will finish his last buffered speech
extern BOOL SC_P_GetTalking(dword pl_id);	// returns TRUE if player is talking right now

extern void SC_P_EnableLonelyWolfKiller(dword pl_id, float distance);	// if nearest ally is farrer from player then distance 
												//   -> enemies shoots quite accurately 
												//	0.0f means disabled
												// has sense of PC only...
extern void SC_P_SetFaceStatus(dword pl_id, dword face_type, float time);
												// changes players face for selected time
extern void SC_P_SetHandVariation(dword pl_id, dword hand_id, dword variation, float time);
												// hand_id - SC_P_HAND_xxxx
												// variation - SC_P_HANDVAR_xxxx
												// time - how long variation will be used, after this time returns to SC_P_HANDVAR_DEFAULT

extern void SC_P_Link3pvEqp(dword pl_id, dword slot_id, dword plb_id, char *eqp_name);	// slot_id is [0,SC_P_LINK3PV_MAX-1]
extern void SC_P_UnLink3pvEqp(dword pl_id, dword slot_id);								// slot_id is [0,SC_P_LINK3PV_MAX-1]

extern void SC_P_SetSpecAnims(dword pl_id, s_SC_P_SpecAnims *info);
extern void SC_P_AddAllAmmo(dword pl_id);
extern void SC_P_AddAmmoNoGrenade(dword pl_id);


extern void SC_P_ChangeWeapon(dword pl_id, dword slot_id, dword weap_type);
extern void SC_P_SetSelWeapon(dword pl_id, dword slot_id);
extern float SC_P_GetPhase(dword pl_id);     // 0-stand, 1-crouch, 2-lie
extern void SC_P_SetPhase(dword pl_id, dword phase);     // 0-stand, 1-crouch ( lie is not supported )

extern float SC_P_GetDistance(dword pl_id, dword to_pl_id);
extern void SC_P_SetActive(dword pl_id, BOOL active);
extern BOOL SC_P_GetActive(dword pl_id);

extern void SC_P_SetInvisibleForAi(dword pl_id, BOOL invisible);	// default is FALSE
extern BOOL SC_P_GetInvisibleForAi(dword pl_id);

extern void SC_P_DoHit(dword pl_id, dword area_id, float hp);
extern void SC_P_SetRadarColor(dword pl_id, dword val);	// val is SC_P_RADARCOLOR_xxxxx or RGB color
extern void SC_P_SetNoAmmo(dword pl_id);
extern void SC_P_CloseEyes(dword pl_id, BOOL force_close);

extern void SC_P_RemoveAllSpeech(dword pl_id);	// when pl_id is 0, all speech is removed
												// when pl_id is 1, radio speech is removed
extern void SC_P_RemoveAllSpeechEx(dword pl_id, BOOL include_active);
												// include_active  - TRUE - removes also already active ( running ) speech
												//					 FALSE - same as SC_P_RemoveAllSpeech()
												// when pl_id is 0, all speech is removed
												// when pl_id is 1, radio speech is removed

extern void SC_P_SetAmmo(dword pl_id, dword ammo_type, dword amount);

extern BOOL SC_P_UsesBinocular(dword pl_id);
extern void SC_P_EnableBinocular(dword pl_id, BOOL enable);	// default value is TRUE
extern void SC_P_EnableHeadEqpFlyOff(dword pl_id, BOOL enable);// defaul value is TRUE
extern void SC_P_EnableHitAnimations(dword pl_id, BOOL enable);// defaul value is TRUE
extern void SC_P_EnableSearchDeathBodies(dword pl_id, BOOL enable);	// default value is TRUE


extern void SC_P_WriteHealthToGlobalVar(dword pl_id, dword first_gvar);		// uses 2 global variable
extern void SC_P_ReadHealthFromGlobalVar(dword pl_id, dword first_gvar);	// uses 2 global variable

extern void SC_P_WriteAmmoToGlobalVar(dword pl_id, dword first_gvar, dword last_gvar);	// 30 gvars is minimum
extern void SC_P_ReadAmmoFromGlobalVar(dword pl_id, dword first_gvar, dword last_gvar); // 30 gvars is minimum

extern dword SC_P_GetAmmoInWeap(dword pl_id, dword slot_id);
extern void SC_P_SetAmmoInWeap(dword pl_id, dword slot_id, dword ammo);

extern void SC_P_SetLinkedView(dword pl_id, float rz, float rx);

extern BOOL SC_P_IsInSpecStativ(dword pl_id);

extern void SC_P_DisableSpeaking(dword pl_id, BOOL disable);

// ai
extern void SC_P_Ai_SetMode(dword pl_id, dword mode);				// values SC_P_AI_MODE_xxxxx
extern dword SC_P_Ai_GetMode(dword pl_id);				// returns SC_P_AI_MODE_xxxxx
extern void SC_P_Ai_SetBattleMode(dword pl_id, dword battlemode);	
																// battlemode is SC_P_AI_BATTLEMODE_xxxx, 
extern void SC_P_Ai_SetBattleModeExt(dword pl_id, dword battlemode, c_Vector3 *param);
																// param is valid for SC_P_AI_BATTLEMODE_GOTO only
extern dword SC_P_Ai_GetBattleMode(dword pl_id);	

extern void SC_P_Ai_SetPeaceMode(dword pl_id, dword peacemode);	// values SC_P_AI_PEACEMODE_xxxx
extern dword SC_P_Ai_GetPeaceMode(dword pl_id);					// values SC_P_AI_PEACEMODE_xxxx

extern dword SC_P_Ai_GetSpecTask(dword pl_id);					// returns SC_PL_AI_SPEC_TASK_xxxx


extern void SC_P_Ai_SetMoveMode(dword pl_id, dword mode);			// values SC_P_AI_MOVEMODE_xxxx
extern void SC_P_Ai_SetMovePos(dword pl_id, dword pos);				// values SC_P_AI_MOVEPOS_xxxx
extern void SC_P_Ai_EnableShooting(dword pl_id, BOOL enable);		// FALSE or TRUE to disable or enable shooting
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
				// enter_pos - position where is possible to enter the car, NULL = everywhere
extern void SC_P_Ai_StepOutCar(dword pl_id);
extern BOOL SC_P_Ai_KnowsAboutPl(dword pl_id, dword target_pl_id);

extern void SC_P_Ai_SetBattleProps(dword pl_id, s_SC_P_Ai_BattleProps *props);	// NULL means engine default algorithms(results differ depends on battle situation)

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
extern BOOL SC_P_Ai_ThrowGrenade(dword pl_id, c_Vector3 *target, float explode_time);	// time to explode after drop

extern float SC_P_Ai_GetNearestEnemyDist(dword pl_id);			// returns FLT_MAX if no enemy found
extern dword SC_P_Ai_GetNearestEnemy(dword pl_id);				// returns 0 if no enemy found

extern void SC_P_Ai_Script_WatchPlayer(dword pl_id, dword target_pl_id, float time);// target_pl_id - when 0 - stop it
																					// time - when 0.0f - forever 
																					//		( must be stopped by functuion calling with target_pl_id=0)																					
extern void SC_P_Ai_UpdateSituation(dword pl_id, dword target_pl_id, BOOL enable_se);

extern void SC_P_Ai_GetEnemyShotAround(dword pl_id, float max_dist);			// causes SC_P_MES_SHOTAROUNDCALLBACK
extern void SC_P_Ai_JumpInNextFrame(dword pl_id);								// AI will press jump in next frame...

extern void SC_P_Ai_SetIgnoreFlags(dword pl_id, dword flags);					// use SC_PL_AI_SIT_IFL_xxxx
extern dword SC_P_Ai_GetIgnoreFlags(dword pl_id);

extern void SC_P_Ai_EnableSayTo(dword pl_id, BOOL enable);						// default value is TRUE

extern void SC_P_Ai_SetPointmanBreaks(dword pl_id, float min_interval, float max_interval); // if max_interval==0.0f, breaks are disabled
extern void SC_P_Ai_WalkThruAIs(dword pl_id, BOOL enable);		// enables switching of other AIs when walking thru, default is FALSE

extern void SC_P_Ai_SetMedicIngMaxActiveDist(dword pl_id, float distance);	// default is 0 that means no limit


extern void SC_Ai_SetFormationType(dword side, dword group, dword type);	// SC_AI_FORMTYPE_xxxx
extern void SC_Ai_SetFormationSize(dword side, dword group, float size);	// 1.0 - standart
extern void SC_Ai_SetBattleMode(dword side, dword group, dword mode);	// SC_P_AI_BATTLEMODE_xxxx
extern void SC_Ai_SetBattleModeExt(dword size, dword group, dword battlemode, c_Vector3 *param);
																		// param is valid for SC_P_AI_BATTLEMODE_GOTO only
extern void SC_Ai_SetPeaceMode(dword side, dword group, dword mode);	// SC_P_AI_PEACEMODE_xxxx
extern void SC_Ai_SetPointRuns(dword side, dword group, BOOL runs);

extern void SC_Ai_ClearCheckPoints(dword side, dword group);
extern void SC_Ai_AddCheckPoint(dword side, dword group, c_Vector3 *vec, dword flags);			// flags: SC_AI_CP_FL_xxxx
extern BOOL SC_Ai_GetCurCheckPoint(dword side, dword group, c_Vector3 *vec);

extern void SC_Ai_SetPlFollow(dword side, dword group, dword mode, s_SC_Ai_PlFollow *follow, dword *follow_order, dword *point_order, dword players);	//formation is SC_AI_FOLLOWMODE_xxxx
extern void SC_Ai_PointStopDanger(dword side, dword group);			// points reacts fast, the rest with delay
extern void SC_Ai_StopDanger(dword side, dword group, float stop_time);				// all reacts very fast (used when user shoot in peace mode f.e.)

extern void SC_Ai_SetStealthMode(dword side, dword group, BOOL stealth);
extern void SC_Ai_SetStealthModeOff(dword side, dword group, float agressive_time);
extern BOOL SC_Ai_GetStealthMode(dword side, dword group);

extern void SC_Ai_EnableRelaxWalk(dword side, dword group, BOOL enable);

extern dword SC_Ai_Blocker_Add(s_sphere *sph);
extern void SC_Ai_Blocker_Remove(dword blocker_id);

extern void SC_Ai_FakeEnemy_Add(dword side, dword group, c_Vector3 *fake_enemy, dword area_spheres, s_sphere *area_sphere);
			// when fake_enemy==NULL, area_spheres==0 and area_sphere==NULL, it's a general danger (AI moves thru hideouts without hidding)
extern void SC_Ai_FakeEnemy_Remove(dword side, dword group, c_Vector3 *fake_enemy);												

extern void SC_Ai_FakeDanger(s_sphere *sph, float time);	// AI players move out of the sphere, time is live time of this danger
															// handy for heli LZ, drop explosives,...
				
extern void SC_Ai_SetGroupEnemyUpdate(dword side, dword group, BOOL enable);// enable - TRUE - player in this groups informs themselves about enemies
																			// default is TRUE
extern void SC_Ai_SetPointmanNormalWalking(dword side, dword group, BOOL normal);		// default is normal==FALSE

extern BOOL SC_P_Ai_CanSeePlayer(dword pl_id, dword target_id, float max_dist, dword need_points);
															// pl_id - AI who is looking
															// target_id - player to test his visibility
															// max_dist - maximum distance to check to ( it's also limited by scene visibility and AI visibility settings)
															// need_points - 11 areas of target_id i checked, need_points says how many of them must be visible to succeed

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

extern void SC_StorySkipEnable(BOOL enable);

//extern void SC_NET_AddRecover(dword side, char *wpname);
extern BOOL SC_NET_FillRecover(s_SC_MP_Recover *recov, char *wpname);

extern void SC_GetPls(s_sphere *sph, dword *list, dword *items);
extern void SC_GetPlsInLine(c_Vector3 *pos, c_Vector3 *dir, dword *list, dword *items);

extern void SC_SetQFStep(dword step);
extern dword SC_GetQFStep(void);
extern void SC_DisplayBinocular(BOOL enable);

extern void SC_DeathCamera_Enable(BOOL enable);// default is TRUE
												// use FALSE in tunnels for example

extern void SC_Set_GoToPC_snd(dword member_id, dword peace, dword agressive, dword stealth);
extern void SC_Set_RadioMan_RunDist(float dist);// 0 is default and means no limit
extern BOOL SC_GetScriptHelper(char *name, s_sphere *sph);
extern void SC_MissionFailedDeathPlayer(dword death_plid);// make Mission failed and camera looks at defined player

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

extern dword SC_AGS_Set(dword val);

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

	// for fpv weapons
extern void *SC_NOD_Get(void *master_obj, char *obj_name);
extern void *SC_NOD_GetNoMessage(void *master_obj, char *obj_name);
extern void *SC_NOD_GetNoMessage_Entity(char *obj_name);

extern void SC_NOD_GetTransform(void *obj,s_SC_NOD_transform *trans);			
extern void SC_NOD_SetTransform(void *obj,s_SC_NOD_transform *trans);
extern void SC_NOD_Hide(void *obj, BOOL hide);

extern void SC_NOD_GetPosInOtherSpace(void *other_nod, void *nod, c_Vector3 *vec);

extern void SC_FPV_AttachMagazine(BOOL render);
extern void SC_FPV_FlyOffCartridge(s_SC_FlyOffCartridge *info);


// other objects functions

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


// scene rendering
extern void SC_DUMMY_Set_DoNotRenHier(char *dummy_name, BOOL do_not_render_hiearchy);
extern void SC_DUMMY_Set_DoNotRenHier2(void *nod, BOOL do_not_render_hiearchy);


// cars
	
extern void *SC_CAR_Create(void *nod, s_SC_Car_Init *info);
extern void SC_CAR_WheelAdd(void *car, void *nod, s_SC_Car_AddWheel *info);
extern void SC_CAR_EntryAdd(void *car, s_SC_Car_AddEntry *info);
extern void SC_CAR_SetAirResistance(void *car, float a0, float a1, float a2);


// ships

extern void *SC_SHIP_Create(void *nod, s_SC_Ship_Init *info, s_SC_PHS_IWantToFloat *finfo);
extern void SC_SHIP_EntryAdd(void *ship, s_SC_Car_AddEntry *info);


// helis

extern void *SC_HELI_Create(void *nod, s_SC_Heli_Init *info);
extern void SC_HELI_EntryAdd(void *heli, s_SC_Car_AddEntry *info);
extern void SC_HELI_ChangeEntryStativ(void *heli, dword entry_index, char *stg_name);	   

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


#if _GE_VERSION_ >= 158
	extern BOOL SC_MP_RecoverAiPlayer(dword pl_id, c_Vector3 *pos, float rz);	// if pos==NULL, the default respawn place is used
#endif 



#endif //#ifndef SC_GLOBAL_H



