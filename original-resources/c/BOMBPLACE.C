//
//	BombBedna.c
//


#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include "coop\!m_defs.h"

#define	C4_NAME					"c4"
#define	EXPLOSION_SMOKE_NAME	"Event_smoke"

#define EXPLOSION_SMALL			"explosion_small"
#define EXPLOSION_BIG			"explosion_big"
#define EXPLOSION_COUNT			13	//pocet malych explozi
#define EXPLOSION_FIRE			"expl_fire_#%d"
#define	EXPLOSION_FIRE_COUNT	13
#define	EXPLOSION_STUFF			"bombplace_expl_#%d"
#define EXPLOSION_STUFF_COUNT	14

#define HIDE_PLAYER				"HidePlayer"
#define DEFUSING_FPV_ANIM		"g\\traps\\deploy.stg"
//#define PLACING_C4_3PV_ANIM		"g\\characters\\anims\\specmove\\bronson dava bombu.stg"
#define EXPLOSION_ANIM			"Levels\\RiverDale\\Data\\Dale\\forscripts\\c_explosion.anm"
#define EXPLOSION_ANIM_START	0
#define EXPLOSION_ANIM_END		900	//musi byt hodne pres, protoze vybuch trva nahodne dlouho
#define EXPLOSION_ANIM_CALLB	1

#define ROZPTYL_X				4.0
#define ROZPTYL_Y				4.0
#define ROZPTYL_Z				2.0

#define FIRST_PHASE				5
#define FIRST_PHASE_TIME		0.8
#define SECOND_PHASE_TIME		1.2
#define THIRD_PHASE_TIME		1.7


dword		playing = 0;
BOOL		bStartF = FALSE;
BOOL		bCamera = FALSE;
BOOL		bFading = FALSE;
BOOL		bC4Show = FALSE;
BOOL		isExploding = FALSE;
int			explosionCount=0;
int			explosionFireCount=0;
float		bombTimeout, holdTimeout;
//c4
c_Vector3	pos, dir, vec, plPos;

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
	SC_DoExplosion(vec, SC_EXPL_TYPE_MORTAR);
	SC_CreatePtc(17,vec);	//ohen
}

void DoExplosionBig(c_Vector3 *vec) {
	SC_DoExplosion(vec, SC_EXPL_TYPE_MORTAR);
	SC_CreatePtc(195,vec);	//ohen do strany
	SC_CreatePtc(182,vec);	//ohen do strany
#ifdef EXPLOSION_SMOKE_NAME
	SC_EventEnable(EXPLOSION_SMOKE_NAME, TRUE);
#endif
}

void ObjectUsed(s_SC_OBJ_info *info) {
	float time;
	time=SC_P_GetWillTalk(SC_PC_Get());			//set the time to the time when pc stops talking
	time+=0.1f;	
	//SC_P_Speech2(SC_PC_Get(),50918,&time);
}
//
int ScriptMain(s_SC_OBJ_info *info)
{
	dword			status;
	dword			txt_id,pc;
	s_SC_P_getinfo	plinfo;
	s_SC_P_Create	plcreate;
	
	c_Vector3	vec, plpos;
	s_sphere	sph;
	float		val, time = 0;
	dword		num;
	int			i;
	char		tmpstr[30];


	switch(info->event_type) {
	case SC_OBJ_INFO_EVENT_INIT:
		//BESPRELOAD_C4STG;
		BESPRELOAD_C4FPV;	//makro
		SC_SetViewAnim(NULL, 0, 100, EXPLOSION_ANIM_CALLB);
	
		for (i=0; i<EXPLOSION_FIRE_COUNT; i++) {
			sprintf(tmpstr, EXPLOSION_FIRE, i);
			SC_EventEnable(tmpstr,FALSE);
		}
		
		Show(OBJECT_OK);
		Hide(OBJECT_DESTR);
		
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
		explosionCount=0;
		explosionFireCount=0;
		bStartF = TRUE;
		holdTimeout = 1.0f;
				
		return TRUE;
//----------------------------------------------------
	case SC_OBJ_INFO_EVENT_USED:
		pc = SC_PC_Get();
		SC_P_GetInfo(pc,&plinfo);
		SC_PC_EnableMovement(FALSE);
		if (plinfo.side){
			holdTimeout = SC_PC_PlayFpvAnim2(DEFUSING_FPV_ANIM,0,NULL,NULL);
			playing = 2;
		} else {
			//Anim
			holdTimeout = FPVANIM_USEC4;	//makro
			ObjectUsed(info);
			playing = 1;
			//Fake danger
			SC_NOD_GetWorldPos(info->master_nod,&sph.pos);
			sph.rad = ROZPTYL_X+ROZPTYL_Y;
			SC_Ai_FakeDanger(&sph, 15.0);
		}
		
		isExploding = FALSE;
		bCamera = FALSE;
		break;
//----------------------------------------------------
	case SC_OBJ_INFO_EVENT_DOTICK:
		holdTimeout -= info->time;

		if ((bStartF) && (holdTimeout < 0)) {
			SC_FadeTo(FALSE, 1.0f);
			bStartF = FALSE;
			
		}
		if ((bFading) && (holdTimeout < 0)) {
			SC_FadeTo(TRUE, 1.0f);
			bFading = FALSE;
		}
		
		if ((playing) && (holdTimeout <= 0.3f)) {
			pc = SC_PC_Get();
			SC_P_GetInfo(pc, &plinfo);
			if (plinfo.cur_hp > 0) {
				SC_PC_EnableMovement(TRUE);
				if (playing == 1) {
					SC_P_ChangeWeapon(pc,6,0);
					SC_sgi(GVAR_BOMBSTATUS01, BOMB_STATUS_ACTIVE); // pro coop
					SC_MP_ScriptMessage(0,0);
				} else if (playing == 2) {
					SC_P_ChangeWeapon(pc,6,55);
					SC_P_SetSelWeapon(pc,6);
					SC_MP_ScriptMessage(0,0);
					//SC_sgi(GVAR_BOMBSTATUS01, BOMB_STATUS_DEFUSED);
				}
				
			} //if (plinfo.cur_hp > 0)
			playing = 0;
		} //if (playing)
	
		status = SC_ggi(GVAR_BOMBSTATUS01);
		if (((status == BOMB_STATUS_INACTIVE) || (status >= BOMB_STATUS_EXPLODING)) && (bC4Show == TRUE)) {
			bC4Show == FALSE;
			Hide(C4_NAME);
		} else if ((status == BOMB_STATUS_ACTIVE) && (bC4Show == FALSE)) {
			bC4Show == TRUE;
			Show(C4_NAME);
		}
		if ((status == BOMB_STATUS_INACTIVE) || (status == BOMB_STATUS_ACTIVE)) {
			val = SC_DOBJ_CameraLooksAt(info->master_nod, 2.0f);
			if (val < 1.0f)	{
				SC_PC_GetPos(&plpos);
				SC_NOD_GetWorldPos(info->master_nod,&vec);
				if (plpos.z+0.2 < vec.z) return 0; //v pripade, ze je pod bednou

				SC_P_GetInfo(SC_PC_Get(),&plinfo);
				SC_P_GetWeapons(SC_PC_Get(),&plcreate);
				//st = SC_ggi(GVAR_BOMBSTATUS);
				txt_id = 0;
				if (plinfo.side) {
					if (status == BOMB_STATUS_ACTIVE) txt_id = 1074;
				}
				else {
					if ((/*plcreate.weap_slot7 == 55*/SC_P_GetCurWeap(SC_PC_Get()) == 55)&&(status == BOMB_STATUS_INACTIVE))  txt_id = 1073;						
				}
						
				if (txt_id) SC_ACTIVE_Add(info->master_nod,2.0f*val,txt_id);

			}// if (val < 1.0f)
		}

		if ((status == BOMB_STATUS_EXPLODING) || (isExploding)) {
			if (!bCamera) {
			
#ifdef HIDE_PLAYER
				SC_NOD_GetWorldPos(SC_NOD_Get(NULL,OBJECT_OK), &vec);
				SC_PC_GetPos(&plPos);
				if (!SC_IsNear3D(&vec, &plPos, 20.0)) {
					SC_NOD_GetWorldPos(SC_NOD_Get(NULL,HIDE_PLAYER), &vec);
					SC_P_SetPos(SC_PC_Get(), &vec);
				}
#endif
				SC_FadeTo(TRUE, 0);
				SC_FadeTo(FALSE, 1.0f);
				
				Hide(SC_NOD_GetName(info->master_nod));

#ifdef EXPLOSION_ANIM
				SC_SetViewAnim(EXPLOSION_ANIM, EXPLOSION_ANIM_START, EXPLOSION_ANIM_END, EXPLOSION_ANIM_CALLB);
#endif
				
				bCamera = TRUE;
				holdTimeout = 2.5;
				isExploding = TRUE;
			}
		
			holdTimeout -= info->time;
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
					
				if (explosionCount < FIRST_PHASE) holdTimeout=abs(frnd(FIRST_PHASE_TIME));
					else if (explosionCount < EXPLOSION_COUNT) holdTimeout=abs(frnd(SECOND_PHASE_TIME));
						else if (explosionCount == EXPLOSION_COUNT) {
							holdTimeout=THIRD_PHASE_TIME;
						} else {
							isExploding=FALSE;
							bFading=TRUE;
							holdTimeout=4.0;
							if (status == BOMB_STATUS_EXPLODING) SC_sgi(GVAR_BOMBSTATUS01, BOMB_STATUS_EXPLODED);
							Show(OBJECT_DESTR);
							Hide(OBJECT_OK);
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
