#include "!m_defs.h"
//settings of difficulties 
#ifndef D0_SHOOT_PREC
#define	D0_SHOOT_PREC	1.5f
#endif

#ifndef D1_SHOOT_PREC
#define	D1_SHOOT_PREC	1.0f
#endif

#ifndef D2_SHOOT_PREC
#define	D2_SHOOT_PREC	0.3f
#endif

#ifndef D3_SHOOT_PREC
#define	D3_SHOOT_PREC	0.0f
#endif

dword	gPhase = GP_CREATE;
dword	respawner;
BOOL	bDead;
BOOL	first = TRUE; // nesmi se prenastavit po restartu

//
int ScriptMain(s_SC_P_info *info)
{
	s_SC_P_Create		pinfo;
	s_SC_P_CreateEqp	eqp[10];
	s_SC_P_AI_props		props;
	s_SC_P_getinfo		plInfo;
	c_Vector3			plPos, vec;
	dword				i, j, pl_id;
	float				rz;
	char				tmpstr[30];
//	struct s_wpPathElement wpe;

	/*if ((info->next_exe_time <= 5.0) && (SC_ggi(B_RETURN_BASE) == TRUE)) {
		info->next_exe_time = 5.0 + frnd(60.0)*SC_ggi(B_RETURN_BASE); //0 nebo 1
		return 0;
	} else if (SC_ggi(B_RETURN_BASE) == TRUE) {
		info->next_exe_time = 10.0f + frnd(20.0)*SC_ggi(B_RETURN_BASE); //0 nebo 1;
	} else {
		info->next_exe_time = 5.0f + frnd(4.0);
	}*/

	switch( info->message )
	{
	case SC_P_MES_TIME:

		switch( gPhase )
		{
		case GP_CREATE:
			CLEAR(pinfo);
			CLEAR(eqp);

			pinfo.type			= SC_P_TYPE_AI;
			pinfo.side			= SC_P_SIDE_VC;

			pinfo.group			= ID_GROUP;
			pinfo.member_id		= ID_MEMBER;

			pinfo.inifile		= GetVCRndIni();//INIFILENAME;
			pinfo.name_nr		= 2506;
			pinfo.icon_name		= "nhut";

			pinfo.weap_knife	= PKNIFE;
			pinfo.weap_pistol	= PPISTOL;

#ifdef PL_GUN1
			pinfo.weap_main1	= PL_GUN1;
#else
			pinfo.weap_main1	= GetVCRndWeapon();			//random gun
#endif
			pinfo.weap_main2	= PWEAPON2;
			pinfo.weap_slot1	= PWEAPONSLOT1;
				
			pinfo.recover_pos	= info->pos;
			
#ifdef	PL_INACTIVE
			pinfo.flags |= SC_P_CREATE_FL_INACTIVE;
#endif

			pinfo.debrief_group	= SC_P_DEBRIEFGROUP_VC;

			//set equipment
			EquipPlayer(eqp, &pinfo.eqps);
			pinfo.eqp = eqp;
			pinfo.eqps = 0;
			
			//random equipment
			//GetVCEquip(&pinfo);
			
			//create
			info->pl_id = SC_P_Create(&pinfo);

			gPhase = GP_INIT;

			break;

		case GP_INIT:
			if ( !SC_P_IsReady(info->pl_id) ) 
				return 0;

			SC_P_Ai_EnableShooting(info->pl_id, TRUE);
			SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_GOTO);
			SC_P_Ai_SetMode(info->pl_id, SC_P_AI_MODE_SCRIPT);
#ifdef RUN
			SC_P_Ai_SetMovePos(info->pl_id, SC_P_AI_MOVEPOS_STAND);
			SC_P_Ai_SetMoveMode(info->pl_id, SC_P_AI_MOVEMODE_RUN);
#else
			SC_P_Ai_SetMovePos(info->pl_id, rand()%3); //0,1,2
#endif
			
			CLEAR(props);
			//
			SC_P_Ai_GetProps(info->pl_id, &props);
							
			props.extend_searchway		= FALSE;
			props.shortdistance_fight	= 0.0f;
			props.view_angle			= PVANGLE;
			props.view_angle_near		= PVANGLENEAR;

			props.max_vis_distance	= 70;
			props.watchfulness_maxdistance = 1.0f;

			props.shoot_imprecision = 0;
			props.shoot_damage_mult = 1.2f;
			props.watchfulness_maxdistance = 1;
			props.reaction_time		= 0.01;
			props.scout				= 0.7f + frnd(0.3f);
			props.berserk			= 0.5f + frnd(0.5f);

			//set by difficulty
			switch( SC_ggi(SGI_DIFFICULTY) )
			{
			case 0:
				props.shoot_imprecision		= D0_SHOOT_PREC;		//overload previous (default) setting
				props.shoot_damage_mult		= 0.5f;
				props.grenade_throw_imprecision = 1.5f + frnd(0.5f);
				break;

			case 1:
				props.shoot_imprecision		= D1_SHOOT_PREC;
				props.shoot_damage_mult		= 1.0f;
				props.grenade_throw_imprecision = 1.0f + frnd(0.5f);
				break;

			case 2:
				props.shoot_imprecision		= D2_SHOOT_PREC;
				props.shoot_damage_mult		= 1.1f;
				props.grenade_throw_imprecision = 0.5f + frnd(0.5f);
				break;

			case 3:
				props.shoot_imprecision		= D3_SHOOT_PREC;
				props.shoot_damage_mult		= 1.2f;
				props.grenade_throw_imprecision = 0.3f + frnd(0.3f);
				break;
			}

			SC_P_Ai_SetProps(info->pl_id,&props);
			
			if (first) {
				info->next_exe_time = 5.0f + frnd(4.0);
				first = FALSE;
			} else {
				info->next_exe_time = 0.1;
			}
				
			respawner = TIMES_RESPAWN;
			bDead = FALSE;
			gPhase = 10;
			break;

		case 10:
			info->next_exe_time = 10.0f;
			if (!SC_P_GetActive(info->pl_id)) return 0;
			if (SC_P_Ai_GetSureEnemies(info->pl_id)) {
				pl_id = SC_P_Ai_GetNearestEnemy(info->pl_id);
				if (pl_id && SC_P_IsReady(pl_id)) {
					SC_P_GetPos(pl_id, &vec);
					SC_P_Ai_Go(info->pl_id, &vec);
					gPhase = 20;
				} else {
					SC_NOD_GetWorldPos(SC_NOD_Get(NULL,US_BASE_ATTACK), &vec);
					SC_P_Ai_HideYourself(info->pl_id, &vec, 10.0);	
				}
			} else {
				SC_NOD_GetWorldPos(SC_NOD_Get(NULL,US_BASE_ATTACK), &vec);
				vec.x+=5.0 - frnd(10.0);
				vec.y+=5.0 - frnd(10.0);
				vec.z+=5.0;
				SC_P_Ai_Go(info->pl_id, &vec);
			}
			break;

		case 20:
			if (rand()%2 == 0) {
				SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_ATTACKAGR);
				info->next_exe_time = 1.0f;
				gPhase = 30;
			} else {
				info->next_exe_time = 5.0f;
			}
			break;
			
		case 30:
			info->next_exe_time = 15.0f;
			pl_id = SC_P_Ai_GetNearestEnemy(info->pl_id);
			if (pl_id && SC_P_IsReady(pl_id)) {
				SC_P_GetPos(pl_id, &vec);
				vec.x+=2.0 - frnd(4.0);
				vec.y+=2.0 - frnd(4.0);
				vec.z+=3.0;
				SC_P_Ai_Go(info->pl_id, &vec);
			} else {
				SC_NOD_GetWorldPos(SC_NOD_Get(NULL,US_BASE_READY), &vec);
				vec.x+=5.0 - frnd(10.0);
				vec.y+=5.0 - frnd(10.0);
				vec.z+=5.0;
				SC_P_Ai_Go(info->pl_id, &vec);
			}
			if (SC_P_Ai_GetMode(info->pl_id) == SC_P_AI_MODE_SCRIPT) SC_P_Ai_SetMode(info->pl_id, SC_P_AI_MODE_BATTLE);
			break;

		case GP_IDLE:
			info->next_exe_time = 60.0f;
			if ((!SC_P_GetActive(info->pl_id)) || (bDead)) return 0;
			break;
			
		case 50:
			info->next_exe_time = DEATH_TIMEOUT;
			gPhase = 51;
			break;

		case 51:
			sprintf(tmpstr, "VC - Attacker Grup 2 -#%d", ID_MEMBER);
			SC_GetPos_VecRz(info->pos, &vec, &rz); // jenom rz
			SC_NOD_GetWorldPos(SC_NOD_Get(NULL,tmpstr), &vec); // a tady pozici
			SC_MP_RecoverAiPlayer(info->pl_id, &vec, rz);
			gPhase = 10;
			//SC_P_Recover(info->pl_id, &vec, rz);
			
			info->next_exe_time = 1.0f;
			
			return 1;
			break;

		}//switch( gPhase )
		
		if ((gPhase >= 10) && (SC_ggi(B_RETURN_BASE))) {
			SC_NOD_GetWorldPos(SC_NOD_Get(NULL, VC_BASE_RETREAT), &vec);
			SC_P_GetPos(info->pl_id, &plPos);
			if (!SC_IsNear2D(&vec, &plPos, 15.0))
				SC_P_Ai_Go(info->pl_id, &vec);
			else
				SC_P_Ai_Stop(info->pl_id);
		}
		
		break;	//case SC_P_MES_TIME:

	case SC_P_MES_EVENT:
		switch(info->param1)
		{
		case SCM_MP_REINIT:
			if (gPhase != GP_CREATE)
				gPhase = GP_INIT;
				info->next_exe_time = 1.0;
			break;
		}
		break;
		
	case SC_P_MES_KILLED:
		if (respawner > 0) {
			gPhase = 50;
			info->next_exe_time = 1.0;
			respawner--;
		} else {
			bDead = TRUE;
			gPhase = GP_IDLE;
		}
		break;
		
	}//switch( info->message )

	return 1;
}
