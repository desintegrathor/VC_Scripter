//
//	BombBedna.c
//

#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\!max_defs_mp.h>

int			PLACING_SIDE = -1;
BOOL		MULTIPLAYER;
dword		playing = 0;
BOOL		bStartF = FALSE;
BOOL		bCamera = FALSE;
BOOL		bFading = FALSE;
BOOL		bC4Show = FALSE;
BOOL		isExploding = FALSE;
BOOL		explosionDone = FALSE;
int			explosionCount=0;
int			explosionFireCount=0;
float		bombTimeout, holdTimeout;
float		tickingValue, tickingTimeout, tickingTimeoutG;
//c4
c_Vector3	pos, dir, vec, plPos;

#if _GE_VERSION_ >= 138
dword g_FPV_BombZone = 0;
#define	MAX_FPV 10
s_SC_FpvMapSign fpv_list[MAX_FPV];
#endif

float abs(float cislo) {
	if (cislo < 0) return -cislo; else return cislo;
}

void Hide(char *tmpstr) {
	SC_DUMMY_Set_DoNotRenHier(tmpstr,TRUE);
}

void Show(char *tmpstr) {
	SC_DUMMY_Set_DoNotRenHier(tmpstr,FALSE);
}

void DoExplosion(c_Vector3 *vec) {
	//SC_MP_SRV_DoExplosion(vec, SC_EXPL_TYPE_MORTAR);
	SC_DoExplosion(vec, SC_EXPL_TYPE_MORTAR);
	//vec->z+=1.0;
	//SC_CreatePtc(17,vec);	//ohen
	//SC_CreatePtcVec_Ext(17, &vec, 0.5, 0, 0.6, 2.0+frnd(0.5)); 
}

void DoExplosionBig(c_Vector3 *vec) {
	SC_DoExplosion(vec, SC_EXPL_TYPE_MORTAR);
	SC_CreatePtc(195,vec);	//ohen do strany
	//SC_CreatePtcVec_Ext(182, vec, 0, 0, 1.0, 0.5);
#ifdef EXPLOSION_SMOKE_NAME
	SC_EventEnable(EXPLOSION_SMOKE_NAME, TRUE);
#endif
}

/*void ObjectUsed(s_SC_OBJ_info *info) {
	float time;
	time=SC_P_GetWillTalk(SC_PC_Get());			//set the time to the time when pc stops talking
	time+=0.1f;	
	//SC_P_Speech2(SC_PC_Get(),50918,&time);
}*/

void InitScene(s_SC_OBJ_info *info) {
	int			i;
	c_Vector3	vec;
	char		tmpstr[30];

	BESPRELOAD_C4FPV;	//makro
		Hide(C4_NAME);
		SC_SetViewAnim(NULL, 0, 100, EXPLOSION_ANIM_CALLB);
	
		for (i=0; i<EXPLOSION_FIRE_COUNT; i++) {
			sprintf(tmpstr, EXPLOSION_FIRE, i);
			SC_EventEnable(tmpstr,FALSE);
		}

		SC_NOD_GetWorldPos(info->master_nod, &vec);
		vec.z += 0.2f;

#if _GE_VERSION_ >= 138
		g_FPV_BombZone = SC_MP_FpvMapSign_Load("g\\weapons\\Vvh_map\\icons\\MPIC_bombingzone.BES");
		fpv_list[BOMB_NR].id = g_FPV_BombZone;
		fpv_list[BOMB_NR].color = 0xffffffff;
		fpv_list[BOMB_NR].pos = vec;
		fpv_list[BOMB_NR].scale = 1.0f;				

		SC_MP_FpvMapSign_Set(BOMB_NR+1,fpv_list);
#endif
		
#ifdef OBJECT_OK
		Show(OBJECT_OK);
#endif
#ifdef OBJECT_DESTR
		Hide(OBJECT_DESTR);
#endif
		
		Show(SC_NOD_GetName(info->master_nod));
				
		for (i=0; i<EXPLOSION_STUFF_COUNT; i++) {
			sprintf(tmpstr, EXPLOSION_STUFF, i);
			Show(tmpstr);
		}
#ifdef EXPLOSION_SMOKE_NAME
		SC_EventEnable(EXPLOSION_SMOKE_NAME, FALSE);
#endif

		playing = 0;
		bCamera = FALSE;
		bFading = FALSE;
		bC4Show = FALSE;
		isExploding = FALSE;
		explosionDone = FALSE;
		explosionCount=0;
		explosionFireCount=0;
		bStartF = TRUE;
		holdTimeout = 1.0f;
}
//
int ScriptMain(s_SC_OBJ_info *info)
{
	dword			status;
	dword			txt_id,pc;
	s_SC_P_getinfo	plinfo;
	//s_SC_P_Create	plcreate;
	
	c_Vector3	vec, plpos;
	s_sphere	sph;
	float		val, time = 0;
	dword		num;
	int			i;
	char		tmpstr[30];

//----------------------------------------------------
	switch(info->event_type) {
	case SC_OBJ_INFO_EVENT_INIT:
		//BESPRELOAD_C4STG;

MULTIPLAYER = FALSE;
		switch(SC_ggi(GVAR_MP_MISSIONTYPE)) {
		case 0:
#ifndef GAME_VC
			PLACING_SIDE = SC_P_SIDE_US;
#else
			PLACING_SIDE = SC_P_SIDE_VC;
#endif
			break;

		case GVAR_MP_MISSIONTYPE_ATG:
			switch(SC_ggi(GVAR_MP_MISSIONSUBTYPE)) {
			case 1:
				PLACING_SIDE = SC_P_SIDE_US;
				break;
			case 2:
				PLACING_SIDE = SC_P_SIDE_VC;
				break;
			default:
				PLACING_SIDE = -1;
				break;
			} //SC_ggi(GVAR_MP_MISSIONSUBTYPE)

			MULTIPLAYER = TRUE;
			break;

		case GVAR_MP_MISSIONTYPE_COOP:
			switch(SC_ggi(GVAR_MP_MISSIONSUBTYPE)) {
			case 1:
				PLACING_SIDE = SC_P_SIDE_US;
				break;
			case 2:
				PLACING_SIDE = SC_P_SIDE_VC;
				break;
			default:
				PLACING_SIDE = -1;
				break;
			} //SC_ggi(GVAR_MP_MISSIONSUBTYPE)

			MULTIPLAYER = TRUE;
			break;

		} //SC_ggi(GVAR_MP_MISSIONTYPE)

		InitScene(info);
		CLEAR(fpv_list);
				
		return TRUE;
//----------------------------------------------------
	case SC_OBJ_INFO_EVENT_USED:
		pc = SC_PC_Get();
		SC_P_GetInfo(pc,&plinfo);

		SC_PC_EnableMovementAndLooking(FALSE);

		if (plinfo.side != PLACING_SIDE) {
			holdTimeout = SC_PC_PlayFpvAnim2(DEFUSING_FPV_ANIM,0,NULL,NULL);
			playing = 2;
		} else {
#ifdef ONLYONE
			for (i=0; i<BOMBSCOUNT; i++) {
				if (i == BOMB_NR)
					SC_sgi(GVAR_BOMBSTATUS__+i*2,BOMB_STATUS_PLACING);
				else 
					if (SC_ggi(GVAR_BOMBSTATUS__+i*2) <= BOMB_STATUS_INACTIVE)
						SC_sgi(GVAR_BOMBSTATUS__+i*2, BOMB_STATUS_OFF);		
			}
#else
			SC_sgi(GVAR_BOMBSTATUS__+BOMB_NR*2,BOMB_STATUS_PLACING);
#endif
			//Anim
			holdTimeout = FPVANIM_USEC4;	//makro
			//ObjectUsed(info);
			playing = 1;
			//Fake danger
			SC_NOD_GetWorldPos(info->master_nod,&sph.pos);
			sph.rad = ROZPTYL_X+ROZPTYL_Y;
			SC_Ai_FakeDanger(&sph, 15.0);
		}
		
		isExploding = FALSE;
		explosionDone = FALSE;
		bCamera = FALSE;
		break;
//----------------------------------------------------
	case SC_OBJ_INFO_EVENT_DOTICK:

		status = SC_ggi(GVAR_BOMBSTATUS__+BOMB_NR*2);
		if (status == BOMB_STATUS_OFF) return 0;

		if (SC_ggi(GVAR_BOMBSTATUS__+BOMB_NR*2) == BOMB_STATUS_ACTIVE) {
			tickingTimeout -= info->time;
			if (tickingValue != SC_ggf(GVAR_BOMBSTIME__+BOMB_NR*2)) {
				tickingValue  = SC_ggf(GVAR_BOMBSTIME__+BOMB_NR*2);
				if (tickingValue > 10.0) tickingTimeoutG = 1.0;
				else if (tickingValue > 5.0) tickingTimeoutG = 0.5;
				else tickingTimeoutG = 0.2;
			}
			if (tickingTimeout < 0) {
				SC_NOD_GetWorldPos(info->master_nod, &vec);
				SC_SND_PlaySound3D(3156, &vec);
				tickingTimeout = tickingTimeoutG;
			}
		}

		holdTimeout -= info->time;

		if ((bStartF) && (holdTimeout < 0)) {
			SC_FadeTo(FALSE, 1.0f);
			bStartF = FALSE;
		}
		if ((bFading) && (holdTimeout < 0)) {
#ifndef ONLYONE
			for (i=0; i<BOMBSCOUNT; i++) 
				if (SC_ggi(GVAR_BOMBSTATUS__+i*2) != BOMB_STATUS_EXPLODED) break;
			
			if (i >= BOMBSCOUNT)
#endif
			SC_FadeTo(TRUE, 1.0f);
			bFading = FALSE;
		}
		
		if ((playing) && (holdTimeout <= 0.3f)) {
			if (bCamera) {
				playing = FALSE;
				return 0;
			}

			pc = SC_PC_Get();
			SC_P_GetInfo(pc, &plinfo);

			if (plinfo.cur_hp > 0) {
				SC_PC_EnableMovementAndLooking(TRUE);
				if (playing == 1) {
					if (status != BOMB_STATUS_PLACING) {
						playing = 0;
						return 0;
					}

					SC_P_ChangeWeapon(pc,6,0);
					SC_MP_ScriptMessage(0,BOMB_NR);
				} else if (playing == 2) {
					SC_P_ChangeWeapon(pc,6,55);
					SC_P_SetSelWeapon(pc,6);
					SC_MP_ScriptMessage(0,BOMB_NR);
				}
				
			} else {
				SC_sgi(GVAR_BOMBSTATUS__+BOMB_NR*2,BOMB_STATUS_INACTIVE);
#ifdef ONLYONE
				for (i=0; i<BOMBSCOUNT; i++) {
					if ((i != BOMB_NR) && (SC_ggi(GVAR_BOMBSTATUS__+i*2) == BOMB_STATUS_OFF))
						SC_sgi(GVAR_BOMBSTATUS__+i*2,BOMB_STATUS_INACTIVE);
				}
#endif
			}//if (plinfo.cur_hp > 0)
			playing = 0;
			
		} //if (playing)
	
		if ((bCamera) && ((status == BOMB_STATUS_INACTIVE) || (status == BOMB_STATUS_STARTING))) {
			InitScene(info);
		}
		if (((status == BOMB_STATUS_INACTIVE) || (status == BOMB_STATUS_EXPLODING) || (status == BOMB_STATUS_EXPLODED) || (status == BOMB_STATUS_DEFUSED)) && (bC4Show == TRUE)) {
			bC4Show = FALSE;
			Hide(C4_NAME);
		} else if ((status == BOMB_STATUS_ACTIVE) && (bC4Show == FALSE)) {
			bC4Show = TRUE;
			Show(C4_NAME);
		}
		if ((status == BOMB_STATUS_INACTIVE) || (status == BOMB_STATUS_ACTIVE)) {
			if (SC_PC_Get() == 0) return 0; //pri restartu a tak ruzne ...
			val = SC_DOBJ_CameraLooksAt(info->master_nod, 2.0f);
			if (val < 1.0f)	{
				SC_PC_GetPos(&plpos);
				SC_NOD_GetWorldPos(info->master_nod,&vec);
#ifdef BOMB_HIGH_LIMIT
				if (plpos.z+BOMB_HIGH_LIMIT < vec.z) return 0; //v pripade, ze je pod bednou
#endif

				SC_P_GetInfo(SC_PC_Get(),&plinfo);
				//SC_P_GetWeapons(SC_PC_Get(),&plcreate);
				txt_id = 0;
				if (plinfo.side == PLACING_SIDE) {
					if ((SC_P_GetCurWeap(SC_PC_Get()) == 55)&&(status == BOMB_STATUS_INACTIVE))  txt_id = 1073;
				}
				else {
					if (status == BOMB_STATUS_ACTIVE) txt_id = 1074;
				}
						
				if (txt_id) SC_ACTIVE_Add(info->master_nod,2.0f*val,txt_id);

			}// if (val < 1.0f)
		}

		if ((!explosionDone) && ((status == BOMB_STATUS_EXPLODING) || (isExploding))) {
			if (!bCamera) {
			
#ifdef HIDE_PLAYER
				//SC_NOD_GetWorldPos(SC_NOD_Get(NULL,OBJECT_OK), &vec);
				if (SC_PC_Get() != 0) { //pri restartu a tak ruzne ...
					SC_NOD_GetWorldPos(info->master_nod, &vec);
					SC_PC_GetPos(&plPos);
					if (!SC_IsNear3D(&vec, &plPos, 20.0)) {
						SC_NOD_GetWorldPos(SC_NOD_Get(NULL,HIDE_PLAYER), &vec);
						SC_P_SetPos(SC_PC_Get(), &vec);
					}
				}
#endif
				
				Hide(SC_NOD_GetName(info->master_nod));

#ifdef EXPLOSION_ANIM
				SC_FadeTo(TRUE, 0);
				SC_FadeTo(FALSE, 1.0f);
				SC_SetViewAnim(EXPLOSION_ANIM, EXPLOSION_ANIM_START, EXPLOSION_ANIM_END, EXPLOSION_ANIM_CALLB);
				holdTimeout = 2.5;
#else
				holdTimeout = 0.1;
#endif
				
				bCamera = TRUE;
				isExploding = TRUE;
			}
		
			//holdTimeout -= info->time;
			if (holdTimeout < 0) {
				explosionCount++;
				if (explosionCount > EXPLOSION_COUNT + 1) return 0;
				
				if (explosionFireCount < EXPLOSION_FIRE_COUNT) {
					sprintf(tmpstr, EXPLOSION_FIRE, explosionFireCount++);
					SC_EventEnable(tmpstr,TRUE);
				}
				
				if (explosionCount <= EXPLOSION_COUNT) {
					SC_NOD_GetWorldPos(SC_NOD_Get(NULL,EXPLOSION_SMALL), &vec);
#ifdef ROZPTYL_X
					vec.x+=frnd(ROZPTYL_X);
#endif
#ifdef ROZPTYL_Y
					vec.y+=frnd(ROZPTYL_Y);
#endif
#ifdef ROZPTYL_Z
					vec.z+=frnd(ROZPTYL_Z);
#endif
				} else {
					SC_NOD_GetWorldPos(SC_NOD_Get(NULL,EXPLOSION_BIG), &vec);
				}
				if (explosionCount <= EXPLOSION_COUNT) DoExplosion(&vec);
					else DoExplosionBig(&vec);
					
				if (explosionCount <= FIRST_PHASE) holdTimeout=FIRST_PHASE_TIME/* + frnd(FIRST_PHASE_TIME)/4.0*/;
					else if (explosionCount < EXPLOSION_COUNT) holdTimeout=SECOND_PHASE_TIME/* + frnd(SECOND_PHASE_TIME)/4.0*/;
						else if (explosionCount == EXPLOSION_COUNT) {
							holdTimeout=THIRD_PHASE_TIME;
						} else {
							isExploding = FALSE;
							explosionDone = TRUE;
							bFading=TRUE;
							holdTimeout=4.0;
							if (status == BOMB_STATUS_EXPLODING) SC_sgi(GVAR_BOMBSTATUS__+BOMB_NR*2, BOMB_STATUS_EXPLODED);
#ifdef OBJECT_DESTR
							Show(OBJECT_DESTR);
#endif
#ifdef OBJECT_OK
							Hide(OBJECT_OK);
#endif
							for (i=0; i<EXPLOSION_STUFF_COUNT; i++) {
								sprintf(tmpstr, EXPLOSION_STUFF, i);
								Hide(tmpstr);
							}
							Hide(SC_NOD_GetName(info->master_nod));
						}
				if (holdTimeout < 0.3) holdTimeout=0.3;
			}
		}
		
		break;

	}// switch(info->event_type)
	return FALSE;

}// int ScriptMain(s_OBJ_info *info)
