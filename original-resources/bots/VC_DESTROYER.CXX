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
BOOL	bDead;

//
int ScriptMain(s_SC_P_info *info)
{
	s_SC_P_Create		pinfo;
	s_SC_P_CreateEqp	eqp[10];
	s_SC_P_AI_props		props;
	s_SC_P_getinfo		plInfo;
	c_Vector3			plPos, vec;
	dword				i, j, pl_id;
//	struct s_wpPathElement wpe;

	if ((info->next_exe_time <= 5.0) && (SC_ggi(B_RETURN_BASE) == TRUE)) {
		info->next_exe_time = frnd(60.0)*SC_ggi(B_RETURN_BASE); //0 nebo 1
		return 0;
	} else if (SC_ggi(B_RETURN_BASE) == TRUE) {
		info->next_exe_time = 10.0f + frnd(20.0)*SC_ggi(B_RETURN_BASE); //0 nebo 1;
	} else {
		info->next_exe_time = 5.0f;
	}

	switch( info->message )	{
	case SC_P_MES_TIME:

		switch( gPhase ) {
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
			
			//create
			info->pl_id = SC_P_Create(&pinfo);

			gPhase = GP_INIT;

			break;

		case GP_INIT:
			if ( !SC_P_IsReady(info->pl_id) ) 
				return 0;

			SC_P_Ai_EnableShooting(info->pl_id, TRUE);

			SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_ATTACK);
			SC_P_Ai_SetMode(info->pl_id, SC_P_AI_MODE_BATTLE);
			
			CLEAR(props);

			//
			SC_P_Ai_GetProps(info->pl_id, &props);
							
			props.extend_searchway		= FALSE;
			props.shortdistance_fight	= 0.0f;
			props.view_angle			= PVANGLE;
			props.view_angle_near		= PVANGLENEAR;

			props.shoot_imprecision = 0;
			props.shoot_damage_mult = 1.2f;
			props.watchfulness_maxdistance = 1;
			props.reaction_time		= 0.01;
			props.scout				= 0.0;
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
			gPhase = 10;
			bDead = FALSE;
			break;


		case 10:
			if (!SC_P_GetActive(info->pl_id)) return 0;
			if ( SC_P_Ai_GetSureEnemies(info->pl_id) )
			{
				pl_id = SC_P_Ai_GetNearestEnemy(info->pl_id);
				if (pl_id && SC_P_IsReady(pl_id))
				{
					SC_P_GetPos(pl_id, &vec);
					SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_ATTACKAGR);
					SC_P_Ai_Go(info->pl_id, &vec);

					gPhase = GP_IDLE;
				}
				else
				{
					SC_P_Ai_ForgetEnemies(info->pl_id);
				}
			}
			break;

		case GP_IDLE:
			info->next_exe_time = 60.0f;
			if ((!SC_P_GetActive(info->pl_id)) || (bDead)) return 0;
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

	case SC_P_MES_KILLED:
		bDead = TRUE;
		gPhase = GP_IDLE;
		break;

	case SC_P_MES_EVENT:
		switch(info->param1)
		{
		case SCM_MP_REINIT:
			if (gPhase != GP_CREATE)
				gPhase = GP_INIT;
			break;
		}
		break;

	}//switch( info->message )

	return 1;
}
