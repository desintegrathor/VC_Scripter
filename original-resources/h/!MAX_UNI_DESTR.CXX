#include <inc\sc_def.h>

//spolupracuje se scriptem barelu
#define GLOBAL_NAME					"machine_destr#%d"
#define MAX_ID						32		//maximalni hodnota %d-1 (pocita se od 0) z predchozi definice

#define GVAR_BOMBSTATUS__			502		//base offset to gvars for bomb states
#define GVAR_BOMBSTIME__			503		//base offset to gvars for bomb timers

#define	BARREL_ARRAY				1789	//misto v pameti (SC_sgf(...))
#define	BARREL_COUNT				10		//pocet explozi barelu ve scene - muze byt i mene ...

#define BOMB_STATUS_STARTING		0
#define BOMB_STATUS_INACTIVE		1
#define BOMB_STATUS_ACTIVE			2
#define	BOMB_STATUS_EXPLODING		3
#define	BOMB_STATUS_EXPLODED		4
#define	BOMB_STATUS_DEFUSED			5

int		GLOBAL_ID;
int		PLACING_SIDE = -1;
int		hitcount = 0;
BOOL	exploded;
BOOL	bC4Show = FALSE;
BOOL	isSoundOn = TRUE;
BOOL	loading = FALSE;
BOOL	MULTIPLAYER = FALSE;
dword	playing = 0;
float	destrTimer[MASTERCOUNT][VERSIONS];
float	holdTimeout = 0.0, timeAfterExplosion;
float	BombTimer = EXPLOSION_TIME/*, oldBombTimer = 0.0*/;
float	soundTimeout = 0.0, hitTimeout = 0.0;
float	oldHP = 0.0;
float	removeFromM = 3.0; // pouzijese i pro nastaveni status exploded
float	delayed_expl[EXPLOSION_COUNT];
float	particle_timer[DESCOUNT];
float	particleRepeat;
int		explosionCounter = 0;
int		myExplosion[EXPLOSION_COUNT];
int		status;
float	tickingValue, tickingTimeout, tickingTimeoutG;

float	FIRETIME_loc[EXPLOSION_COUNT];
float	SMOKETIME_loc[EXPLOSION_COUNT];

BOOL	initialized = FALSE;
			

#define DEFUSING_FPV_ANIM		"g\\traps\\deploy.stg"

s_SC_NOD_transform origtran[DESCOUNT];

int getGlobalID(void *nod) {
	char	tmpstr1[64], tmpstr2[64];
	char	*str;
	int		i;

	str = SC_NOD_GetName(nod);
	sprintf(tmpstr2, "%s", str);
	for (i=0; i<MAX_ID; i++) {
		sprintf(tmpstr1,GLOBAL_NAME,i);
		if (SC_StringSame(tmpstr1,tmpstr2)) return i;
	}
	return -1;
}

float pfrnd(float x){
	float y;
	y=frnd(x);
	if (y<0) y=0-y;
	return y;
}

float g_frnd(float x){
	float y;
	y=frnd(x);
	if ((y <  0) && (y > -DELTA)) return y-DELTA;
	if ((y >= 0) && (y <  DELTA)) return y+DELTA;
	return y;
}

float gp_frnd(float x){
	float y;
	y=pfrnd(x);
	if ((y <  0) && (y > -DELTA)) return y-DELTA;
	if ((y >= 0) && (y <  DELTA)) return y+DELTA;
	return y;
}

void Hide(void *nod) {
	SC_DUMMY_Set_DoNotRenHier2(nod,TRUE);
}

void Show(void *nod) {
	SC_DUMMY_Set_DoNotRenHier2(nod,FALSE);
}

void SoundOff(char *tmpstr) {
	s_SC_NOD_transform	tran;
	char				*tmpstr2;
	void				*nod;

	if (!isSoundOn) return;
	isSoundOn = FALSE;
	
	if (GLOBAL_ID >= 0) sprintf(tmpstr2,"%s",tmpstr,GLOBAL_ID);
	else {
		SC_message("[SoundOff] GLOBAL_ID error! Value: %d",GLOBAL_ID);
		return;
	}
	nod = SC_NOD_Get(NULL,tmpstr2);

	SC_NOD_GetTransform(nod,&tran);
	tran.loc.z-=1000;
	SC_NOD_SetTransform(SC_NOD_Get(NULL,tmpstr2),&tran);
}

void SoundOn(char *tmpstr) {
	s_SC_NOD_transform	tran;
	char				*tmpstr2;
	void				*nod;

	if (isSoundOn) return;
	isSoundOn = TRUE;

	if (GLOBAL_ID >= 0) sprintf(tmpstr2,"%s",tmpstr,GLOBAL_ID);
	else {
		SC_message("[SoundOn] GLOBAL_ID error! Value: %d",GLOBAL_ID);
		return;
	}
	nod = SC_NOD_Get(NULL,tmpstr2);

	SC_NOD_GetTransform(nod,&tran);
	tran.loc.z+=1000;
	SC_NOD_GetTransform(nod,&tran);
}

void getVectorFromM(c_Vector3 *vec, int poz) {
	vec->x = SC_ggf(BARREL_ARRAY + poz*2);
	vec->y = SC_ggf(BARREL_ARRAY + poz*2 + 1);
	vec->z = 0.0;
}

void setVectorToM(c_Vector3 *vec, int poz) {
	SC_sgf(BARREL_ARRAY + poz*2,		vec->x);
	SC_sgf(BARREL_ARRAY + poz*2 + 1,	vec->y);
}

int getFreeIndex() {
	int i;
	c_Vector3 vec;

	for (i=0; i<BARREL_COUNT; i++) {
		getVectorFromM(&vec, i);
		if ((vec.x == 0.0) && (vec.y == 0.0)) return i;
	}
	return -1;
}

int addEntry(c_Vector3 *vec) {
	int i;
	i = getFreeIndex();
	if (i >= 0) setVectorToM(vec, i);
	return i;
}

void DoExplosions(s_SC_OBJ_info *info) {
	int i;
	float			tmp;
	void			*nod;
	c_Vector3		vec;
	for (i=0; i<EXPLOSION_COUNT; i++) {
		nod=SC_NOD_Get(info->master_nod,EXPLNAME[i]);
		SC_NOD_GetWorldPos(nod,&vec);
		if (status != BOMB_STATUS_EXPLODED)
			tmp = SMOKETIME_loc[i]+frnd(SMOKETIME_R[i]);
		else
			tmp = (SMOKETIME_loc[i]+frnd(SMOKETIME_R[i])) / 4.0;

		if (tmp > 0) {
			vec.z+=SMOKECOR[i];
			SC_CreatePtcVec_Ext(SMOKEPTC[i], &vec, tmp, SMOKEINTERVAL[i], SMOKESCALE[i], 0.8 + frnd(0.3));	// smoke
			vec.z-=SMOKECOR[i];
		}
		vec.z+=FIRECOR[i];
		if (status != BOMB_STATUS_EXPLODED)
			tmp = FIRETIME_loc[i]+frnd(FIRETIME_R[i]);
		else
			tmp = (FIRETIME_loc[i]+frnd(FIRETIME_R[i])) / 4.0;

		if (tmp > 0) SC_CreatePtcVec_Ext(177, &vec, tmp, FIREINTERVAL[i], FIRESCALE[i], 0.8 + frnd(0.3));	// big fire
#ifdef SOUND
		if ((SOUNDTIME_INDEX == i) && (tmp > 0)) {
			soundTimeout = tmp;
			SoundOn(SOUND);
		}
#endif
	}
}

void addDynamMain(s_SC_OBJ_info *info) {
	void			*nod;
	c_Vector3		vec;
	float			speed;
	s_SC_OBJ_dynamic doinfo;
	
	nod=SC_NOD_Get(info->master_nod,MASTERNAME[0]);
	
	CLEAR(doinfo);
	
	doinfo.rot_speed=ROTSPEED;
	speed=SPEED;

	doinfo.velocity.x=gp_frnd(1)*speed;
	doinfo.velocity.y=gp_frnd(1)*speed;
	doinfo.velocity.z=gp_frnd(1)*speed;
	
	doinfo.rot_axis.x=g_frnd(XROT);
	doinfo.rot_axis.y=g_frnd(YROT);
	doinfo.rot_axis.z=g_frnd(ZROT);

	SC_NOD_AddDynamic(info->master_nod,MASTERNAME[0],&doinfo);
}

void DoDestruction(s_SC_OBJ_info *info) {
	int				i, j;
	char			txt[32];
	void			*nod;
	c_Vector3		vec;
	float			speed;
	s_SC_OBJ_dynamic doinfo;

	particleRepeat = 0.0;

	for (i=0;i<MASTERCOUNT;i++)	{
	//i=5;
		for (j=0; j<VERSIONS; j++)
			if (!SC_StringSame(DESTRNAME_T[i][j],"")) break;

		if ((j == VERSIONS) && (SC_StringSame(DESTRNAME[i],"")))
			SC_NOD_SetDSTR(info->master_nod,MASTERNAME[i],NULL);
		else if (!SC_StringSame(DESTRNAME[i],""))
			SC_NOD_SetDSTR(info->master_nod,MASTERNAME[i],DESTRNAME[i]);
	}

	if (status != BOMB_STATUS_EXPLODED)  addDynamMain(info); //kvuli multaku !!!

	for (i=0;i<DESCOUNT;i++) {
		sprintf(txt,DESNAME,i);
		nod=SC_NOD_Get(info->master_nod,txt);
		SC_DUMMY_Set_DoNotRenHier2(nod,FALSE);

		if (status != BOMB_STATUS_EXPLODED) { //kvuli multaku !!!
			SC_NOD_SetTransform(nod,&origtran[i]);								
			
			SC_DOBJ_SetFrozenFlag(nod, FALSE);				
			
			CLEAR(doinfo);
			
			SC_NOD_GetWorldPos(info->master_nod,&vec);
			SC_NOD_GetWorldPos(nod,&doinfo.rot_axis);
			
			doinfo.rot_speed=ROTSPEED;
			speed=SPEED*(SC_2VectorsDist(&doinfo.rot_axis,&vec));

			doinfo.velocity.x=gp_frnd(1)*speed*(doinfo.rot_axis.x-vec.x);
			doinfo.velocity.y=gp_frnd(1)*speed*(doinfo.rot_axis.y-vec.y);
			doinfo.velocity.z=gp_frnd(1)*speed*(doinfo.rot_axis.z-vec.z);		
			
			doinfo.rot_axis.x=g_frnd(XROT);
			doinfo.rot_axis.y=g_frnd(YROT);
			doinfo.rot_axis.z=g_frnd(ZROT);

			SC_NOD_AddDynamic(info->master_nod,txt,&doinfo);
		}
	}

	if (status == BOMB_STATUS_EXPLODED) {
		for (i=0; i<EXPLOSION_COUNT; i++) delayed_expl[i] = EXPLDELAY[i] + 1.0; //aby se neprovedly vybuchy
		for (i=0; i<DESCOUNT; i++) particle_timer[i] = PARTICLETIME[i] + 1.0;
	}

	exploded=TRUE;
	timeAfterExplosion = 0.0;

	DoExplosions(info);

	if (status != BOMB_STATUS_EXPLODED) {
		status = BOMB_STATUS_EXPLODING;
		if ((MULTIPLAYER) && (SC_ggi(GVAR_BOMBSTATUS__ + GLOBAL_ID*2) != status)) SC_sgi(GVAR_BOMBSTATUS__ + GLOBAL_ID*2, status);
	}

#ifdef C4_NAME
	Hide(SC_NOD_Get(info->master_nod, C4_NAME));
#endif
}
//---------------------------------------------------
void InitScene(s_SC_OBJ_info *info) {
	int					i, j;
	char				txt[32];
	void				*nod;
	s_SC_NOD_transform	tran;

	BESPRELOAD_C4FPV;
	bC4Show = FALSE;

	status = BOMB_STATUS_INACTIVE;
#ifdef C4_NAME
	Hide(SC_NOD_Get(info->master_nod, C4_NAME));
#endif
#ifdef SOUND
	SoundOff(SOUND);
#endif
	loading = FALSE;
	for (i=0; i<MASTERCOUNT; i++) {
		if (!SC_StringSame(MASTERNAME[i],"")) Show(SC_NOD_Get(info->master_nod, MASTERNAME[i]));
		for (j=0; j<VERSIONS; j++)
			if (!SC_StringSame(DESTRNAME_T[i][j], "")) Hide(SC_NOD_Get(info->master_nod, DESTRNAME_T[i][j]));

		for (j=0; j<VERSIONS; j++) {
			DESTRDELAY[i][j] += frnd(DESTRDELAY[i][j]/4.0);
			destrTimer[i][j] = 0.0;
		}
	}

	for (i=0;i<DESCOUNT;i++) {
		sprintf(txt,DESNAME,i);
		nod=SC_NOD_Get(info->master_nod,txt);
		SC_DUMMY_Set_DoNotRenHier2(nod,TRUE);
		SC_DOBJ_SetFrozenFlag(nod, TRUE);				
		SC_NOD_GetTransform(nod,&origtran[i]);
		tran.loc.x		= origtran[i].loc.x;
		tran.loc.y		= origtran[i].loc.y;
		tran.loc.z		= origtran[i].loc.z;
		tran.rot.x		= origtran[i].rot.x;
		tran.rot.y		= origtran[i].rot.y;
		tran.rot.z		= origtran[i].rot.z;
		tran.scale.x	= origtran[i].scale.x;
		tran.scale.y	= origtran[i].scale.y;
		tran.scale.z	= origtran[i].scale.z;
		tran.loc.z-=10000;
		SC_NOD_SetTransform(nod,&tran);
	}

	CLEAR(delayed_expl);
	CLEAR(particle_timer);

	hitcount = 0;
	bC4Show = FALSE;
	loading = FALSE;
	if (MULTIPLAYER) exploded = TRUE; else exploded = FALSE;

	for (i=0; i<EXPLOSION_COUNT ;i++) {
		FIRETIME_loc[i] = FIRETIME[i];
		SMOKETIME_loc[i] = SMOKETIME[i];
	}
	initialized = TRUE;
}
//---------------------------------------------------
int ScriptMain(s_SC_OBJ_info *info) {
	float			val, cosF;
	s_sphere		sph;
	int				i, j;
	char			txt[32];
	void			*nod;
	dword			txt_id,pc;
	s_SC_P_getinfo	plinfo;
	//s_SC_OBJ_dynamic doinfo;
	s_SC_NOD_transform tran;
	s_SC_HUD_MP_icon icon[10];
	c_Vector3 vec,vec2,plpos;

	switch(info->event_type) {
		case SC_OBJ_INFO_EVENT_INIT:

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

			GLOBAL_ID = getGlobalID(info->master_nod);
			if ((!MULTIPLAYER) && (GLOBAL_ID == -1))  GLOBAL_ID = -2;

			InitScene(info);

			if (MULTIPLAYER) status = SC_ggi(GVAR_BOMBSTATUS__ + GLOBAL_ID*2);

			CLEAR(icon);

			return TRUE;
//----------------------------------- RELEASE ------------------------------------------
		case SC_OBJ_INFO_EVENT_RELEASE:
			for (i=0;i<DESCOUNT;i++){
				sprintf(txt,DESNAME,i);
				nod=SC_NOD_Get(info->master_nod,txt);
				tran=origtran[i];
				SC_NOD_SetTransform(nod,&tran);								
			}
#ifdef SOUND
			SoundOn(SOUND);
#endif
			return TRUE;
//----------------------------------- LOAD ---------------------------------------------
		case SC_OBJ_INFO_EVENT_JUSTLOADED:
			loading = TRUE;
			if (exploded) {
				for (j=0; j<VERSIONS; j++)
					if (!SC_StringSame(DESTRNAME_T[i][j],"")) break;

				if ((j == VERSIONS) && (SC_StringSame(DESTRNAME[i],"")))
					SC_NOD_SetDSTR(info->master_nod,MASTERNAME[i],NULL);
				else if (!SC_StringSame(DESTRNAME[i],""))
					SC_NOD_SetDSTR(info->master_nod,MASTERNAME[i],DESTRNAME[i]);

				for (i=0;i<DESCOUNT;i++){
					sprintf(txt,DESNAME,i);
					nod=SC_NOD_Get(info->master_nod,txt);
					SC_DUMMY_Set_DoNotRenHier2(nod,FALSE);
					SC_DOBJ_SetFrozenFlag(nod, FALSE);				
				}
				DoExplosions(info);
			}
#ifdef SOUND
			SoundOff(SOUND);
#endif
			loading = FALSE;
			return TRUE;
//------------------------------------ HIT ---------------------------------------------
		case SC_OBJ_INFO_EVENT_HIT:
			if ((exploded) || (status == 0)) return 0;
			if ((GLOBAL_ID == -1) || (PLACING_SIDE == -1)) return 0;

			if (info->nod != SC_NOD_Get(info->master_nod,MASTERNAME[0])) return 0;

			if ((info->hit_by==SC_OBJ_HIT_BY_EXPLOSION) && (info->new_hp_obtained - oldHP > MINHP) && (ONLYC4 == FALSE))
				hitcount++;

			if  ((hitcount >= HITS) || ((ONLYEXPLOSION == FALSE) && (ONLYC4 == FALSE) && (info->new_hp_obtained > MAXHP))) {
				if (!MULTIPLAYER) SC_MP_SetIconHUD(icon,0);
				DoDestruction(info);
			}
			oldHP = info->new_hp_obtained;
			break;
//------------------------------------- TICK -------------------------------------------
		case SC_OBJ_INFO_EVENT_DOTICK:
			if ((GLOBAL_ID == -1) || (PLACING_SIDE == -1)) return 0;

			//-----------------------------------------------------------------//
			if (MULTIPLAYER) status = SC_ggi(GVAR_BOMBSTATUS__ + GLOBAL_ID*2); //
			//-----------------------------------------------------------------//

			if ((MULTIPLAYER) && (exploded) && ((status == BOMB_STATUS_STARTING) || (status == BOMB_STATUS_INACTIVE))) {
				for (i=0; i<MASTERCOUNT; i++) SC_NOD_SetDSTR(info->master_nod,MASTERNAME[i],MASTERNAME[i]);
				if (!initialized) InitScene(info);
				exploded = FALSE;
				initialized = FALSE;
				return 1;
			}
			if ((MULTIPLAYER) && (!exploded) && ((status == BOMB_STATUS_EXPLODING) || (status == BOMB_STATUS_EXPLODED))) DoDestruction(info); //pokud se hrac logne, kdyz je kara znicena

			if (exploded) {
#ifdef SOUND
				if (soundTimeout >= 0) {
					soundTimeout -= info->time;
					if ((soundTimeout < 0) && (isSoundOn)) SoundOff(SOUND);
				}
#endif
				for (i=0; i<MASTERCOUNT; i++) {
					for (j=0; j<VERSIONS; j++) {
						if (destrTimer[i][j] <= DESTRDELAY[i][j]) {
							destrTimer[i][j] += info->time;
							if (destrTimer[i][j] > DESTRDELAY[i][j]) {
								if (j == 0) {
									if (!SC_StringSame(MASTERNAME[i],"")) Hide(SC_NOD_Get(info->master_nod, MASTERNAME[i]));
									if (!SC_StringSame(DESTRNAME[i],"")) Hide(SC_NOD_Get(info->master_nod, DESTRNAME[i]));
								} else {
									if (!SC_StringSame(DESTRNAME_T[i][j-1], "")) Hide(SC_NOD_Get(info->master_nod, DESTRNAME_T[i][j-1]));
								}
								if (!SC_StringSame(DESTRNAME_T[i][j], "")) Show(SC_NOD_Get(info->master_nod, DESTRNAME_T[i][j]));
							} //if destr >
						} // if destr <=
					} // for j
				} // for i

				pc = SC_PC_Get();
				SC_P_GetInfo(pc, &plinfo);
				if (plinfo.cur_hp > 0) {
					SC_PC_GetPos(&plpos);
					timeAfterExplosion += info->time;
					for (i=0; i<EXPLOSION_COUNT; i++) {
						nod=SC_NOD_Get(info->master_nod,EXPLNAME[i]);
						SC_NOD_GetWorldPos(nod,&vec);
						if (FIRETIME_loc[i] > 0) { //timeAfterExplosion < 
							if (SC_IsNear3D(&plpos, &vec, 2.0*sqrt(FIRESCALE[i]))) {
								hitTimeout -= info->time;
								if (hitTimeout < 0) {
									SC_P_DoHit(pc, SC_P_MESH_AREA_BODYFRONT, HITDAMAGE);
									hitTimeout = HITTIMEOUT;
								}
							}
						}
					}
				}

				particleRepeat -= info->time;

				for (i=0; i<DESCOUNT; i++) {
					if ((PARTICLE_DO[i]) && (particle_timer[i] <= PARTICLETIME[i])) {
						particle_timer[i] += info->time;
						if (particleRepeat < 0) {
							sprintf(txt,DESNAME,i);
							nod=SC_NOD_Get(info->master_nod,txt);
							SC_NOD_GetWorldPos(nod,&vec);
							SC_CreatePtcVec_Ext(17, &vec, 0.5, 0, 0.6, 2.0+frnd(0.5));
							particleRepeat = 0.1;
						}
					}
				}

				for (i=0; i<EXPLOSION_COUNT; i++) {
					if ((EXPL_DO[i] == TRUE) && (delayed_expl[i] <= EXPLDELAY[i])) {
						delayed_expl[i] += info->time;
						if (delayed_expl[i] > EXPLDELAY[i]) {
							nod=SC_NOD_Get(info->master_nod,EXPLNAME[i]);
							SC_NOD_GetWorldPos(nod,&vec);
							vec.z+=0.2;
							myExplosion[i] = addEntry(&vec);
							removeFromM = 3.0;
							SC_DoExplosion(&vec, SC_EXPL_TYPE_MORTAR);
							SC_CreatePtc(17,&vec);								// vybuch (ohen)
							SC_CreatePtcVec_Ext(182, &vec, 0, 0, 0.3, 0.5);		// mega vybuch
						}
					}
				}

				if (removeFromM >= 0) {
					removeFromM -= info->time;
					if (removeFromM < 0) {
						CLEAR(vec);
						for (j=0; j<EXPLOSION_COUNT; j++) if (EXPL_DO[j] == TRUE) setVectorToM(&vec, myExplosion[j]); 
					}
					status = BOMB_STATUS_EXPLODED;
					if ((MULTIPLAYER) && (SC_ggi(GVAR_BOMBSTATUS__ + GLOBAL_ID*2) != status)) SC_sgi(GVAR_BOMBSTATUS__ + GLOBAL_ID*2, status);
				}
				for (i=0; i<EXPLOSION_COUNT; i++) {
					if (FIRETIME_loc[i]  >= 0) FIRETIME_loc[i] -= info->time;
					if (SMOKETIME_loc[i] >= 0) SMOKETIME_loc[i] -= info->time;
				}

				return FALSE;
			}
			//if (MULTIPLAYER) break;

#ifdef C4_NAME

			holdTimeout -= info->time;

			if (status == BOMB_STATUS_ACTIVE) {
				tickingTimeout -= info->time;
				if (MULTIPLAYER) {
					if (tickingValue != SC_ggf(GVAR_BOMBSTIME__+ GLOBAL_ID*2)) {
						tickingValue  = SC_ggf(GVAR_BOMBSTIME__+ GLOBAL_ID*2);
						if (tickingValue > 10.0) tickingTimeoutG = 1.0;
						else if (tickingValue > 5.0) tickingTimeoutG = 0.5;
						else tickingTimeoutG = 0.2;
					}
				} else {
					if (tickingValue != BombTimer) {
						tickingValue  = BombTimer;
						if (tickingValue > 10.0) tickingTimeoutG = 1.0;
						else if (tickingValue > 5.0) tickingTimeoutG = 0.5;
						else tickingTimeoutG = 0.2;
					}
				}
				if (tickingTimeout < 0) {
					SC_NOD_GetWorldPos(info->master_nod, &vec);
					SC_SND_PlaySound3D(3156, &vec);
					tickingTimeout = tickingTimeoutG;
				}
			}

			if (((status == BOMB_STATUS_INACTIVE) || (status >= BOMB_STATUS_EXPLODING)) && (bC4Show == TRUE)) {
				bC4Show = FALSE;
				Hide(SC_NOD_Get(info->master_nod, C4_NAME));
			} else if ((status == BOMB_STATUS_ACTIVE) && (bC4Show == FALSE)) {
				Show(SC_NOD_Get(info->master_nod, C4_NAME));
				bC4Show = TRUE;
			}
			if ((!MULTIPLAYER) && (status == BOMB_STATUS_ACTIVE)) {
				BombTimer -= info->time;
				if (BombTimer>0) {
					icon[0].color = 0xffffffff;
					icon[0].icon_id = 10;
					icon[0].type = SC_HUD_MP_ICON_TYPE_TIME;
					icon[0].value = (int)(BombTimer+0.99f);
					SC_MP_SetIconHUD(icon, 1);
				} else {
					SC_MP_SetIconHUD(icon,0);
					DoDestruction(info);
					break;
				}
			}

			/*if ((MULTIPLAYER) && (status == BOMB_STATUS_EXPLODING)) {
				DoDestruction(info);
			}*/

			if ((status == BOMB_STATUS_INACTIVE) || (status == BOMB_STATUS_ACTIVE)) {
				nod=SC_NOD_Get(info->master_nod,EXPLNAME[0]);
				val = SC_DOBJ_CameraLooksAt(info->master_nod, C4_PLACEDIST);
				if (val < 1.0f)	{
					SC_PC_GetPos(&plpos);
					SC_NOD_GetWorldPos(info->master_nod,&vec);
					SC_NOD_GetWorldPos(nod,&vec2);
					plpos.x-=vec.x;
					plpos.y-=vec.y;
					vec2.x-=vec.x;
					vec2.y-=vec.y;
					cosF=(vec2.x*plpos.x + vec2.y*plpos.y)/(sqrt(vec2.x*vec2.x + vec2.y*vec2.y) * sqrt(plpos.x*plpos.x + plpos.y*plpos.y));
					if (cosF < 0.7) return 0;
					
					//if (plpos.z+0.2 < vec.z) return 0; //v pripade, ze je pod bednou

					SC_P_GetInfo(SC_PC_Get(),&plinfo);
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
			if ((playing) && (holdTimeout <= 0.3f)) {
				pc = SC_PC_Get();
				SC_P_GetInfo(pc, &plinfo);
				if (plinfo.cur_hp > 0) {
					SC_PC_EnableMovementAndLooking(TRUE);
					if (playing == 1) {
						SC_P_ChangeWeapon(pc,6,0);
						BombTimer = EXPLOSION_TIME;
						SC_MP_ScriptMessage(0,GLOBAL_ID);
						status = BOMB_STATUS_ACTIVE;	//na MP nema vliv, protoze v dalsim ticku se to zjisti z SC_ggi
					} else if (playing == 2) {
						SC_P_ChangeWeapon(pc,6,55);
						SC_P_SetSelWeapon(pc,6);
						SC_MP_ScriptMessage(0,GLOBAL_ID);
						status = BOMB_STATUS_DEFUSED;	//na MP nema vliv, protoze v dalsim ticku se to zjisti z SC_ggi
					}
					
				} //if (plinfo.cur_hp > 0)
				playing = 0;
			} //if (playing)
#endif
			break;
//----------------------------------- USED ---------------------------------------------
		case SC_OBJ_INFO_EVENT_USED:
			pc = SC_PC_Get();
			SC_P_GetInfo(pc,&plinfo);
			SC_PC_EnableMovementAndLooking(FALSE);
			if (plinfo.side == PLACING_SIDE){
				//Anim
				holdTimeout = FPVANIM_USEC4;	//makro
				playing = 1;
				//Fake danger
				SC_NOD_GetWorldPos(info->master_nod,&sph.pos);
				sph.rad = 10.0;
				SC_Ai_FakeDanger(&sph, 15.0);
			} else {
				holdTimeout = SC_PC_PlayFpvAnim2(DEFUSING_FPV_ANIM,0,NULL,NULL);
				playing = 2;
			}
			
			//isExploding = FALSE;
			//bCamera = FALSE;
			break;

	}// switch(info->event_type)


	return FALSE;

}// int ScriptMain(s_OBJ_info *info)
