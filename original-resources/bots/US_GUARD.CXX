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
BOOL	bAnimLooped = FALSE;
int		wpi = 0;
float	holdTimeout = 0.0;

//
int ScriptMain(s_SC_P_info *info)
{
	s_SC_P_Create		pinfo;
	s_SC_P_CreateEqp	eqp[10];
	s_SC_P_AI_props		props;
	s_SC_P_getinfo		plInfo;
	c_Vector3			plPos, vec, vec2;
	dword				i, j, pl_id;
	s_SC_MP_EnumPlayers enum_pl[64];
	dword				num;
	float				dist, olddist;
	float				goTimer;
	int					player;

//	struct s_wpPathElement wpe;

	info->next_exe_time = 5.0f;

	switch( info->message )	{
	case SC_P_MES_TIME:

		switch( gPhase ) {
		case GP_CREATE:
			//if (ID_MEMBER != 0) return 0;
			CLEAR(pinfo);
			CLEAR(eqp);

			pinfo.type			= SC_P_TYPE_AI;
			pinfo.side			= SC_P_SIDE_US;

			pinfo.group			= ID_GROUP;
			pinfo.member_id		= ID_MEMBER;
#ifdef INIFILENAME
			pinfo.inifile		= INIFILENAME;
#else
			pinfo.inifile		= GetUSRndIni();
#endif
			pinfo.name_nr		= 2499;
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
			//pinfo.flags |= SC_P_CREATE_FL_CROUCH;

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
			SC_P_Ai_SetMoveMode(info->pl_id, SC_P_AI_MOVEMODE_WALK);
			SC_P_Ai_SetMovePos(info->pl_id, SC_P_AI_MOVEPOS_STAND);
			SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_HOLD);
			SC_P_Ai_SetMode(info->pl_id, SC_P_AI_MODE_SCRIPT);
			
			CLEAR(props);

			//
			SC_P_Ai_GetProps(info->pl_id, &props);
			
			props.max_vis_distance	= 40.0;

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

			//props.hear_imprecision		= 1.0;				// 0 - absolute hearing, 1 - average hering, 5 - bad hearing
			//props.hear_distance_mult	= 1.0;			// 0.5 - half, 1 - normal, 2 - two-times better
			//props.hear_distance_max		= 200.0;

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

			gPhase = GP_IDLE;
			bDead = FALSE;
			wpi = 0;
			goTimer = 0;
			SC_sgi(B_DANGER, FALSE);
#ifdef MAX_WPS
			DefinePendl();
#endif
			break;


		case GP_IDLE:
			info->next_exe_time = 3.0f;
			if (SC_P_Ai_GetBattleMode(info->pl_id) != SC_P_AI_BATTLEMODE_RETREAT) SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_RETREAT);
			if ((bDead) || (SC_P_Ai_GetMode(info->pl_id) == SC_P_AI_MODE_BATTLE)) return 0;
			//if (SC_P_Ai_GetSureEnemies(info->pl_id))
			if ((SC_P_Ai_GetNearestEnemyDist(info->pl_id) < 20.0) || (SC_P_Ai_GetDanger(info->pl_id) > 0) || (SC_ggi(B_DANGER) == TRUE)) {
				if (bAnimLooped) {
					bAnimLooped = FALSE;
					SC_P_DoAnimLooped(info->pl_id, NULL);
				}
				//SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_HOLD);
				SC_P_Ai_GetProps(info->pl_id,&props);
				props.max_vis_distance	= 150.0;
				props.hear_imprecision		= 1.0;				// 0 - absolute hearing, 1 - average hering, 5 - bad hearing
				props.hear_distance_mult	= 2.0;			// 0.5 - half, 1 - normal, 2 - two-times better
				props.hear_distance_max		= 200.0;
				SC_P_Ai_SetProps(info->pl_id,&props);
				SC_P_Ai_SetMode(info->pl_id, SC_P_AI_MODE_BATTLE);
				SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_RETREAT);
				CLEAR(vec2);
				SC_P_GetPos(info->pl_id, &plPos);
				if (SC_MP_EnumPlayers(enum_pl, &num, SC_P_SIDE_VC)) {
					for (j=0; j<num; j++) {
						SC_P_GetPos(enum_pl[j].id, &vec);
						if ((dist = SC_2VectorsDist(&vec2, &vec)) < olddist) {
							olddist = dist;
							vec2.x = vec.x;
							vec2.y = vec.y;
							vec2.z = vec.z;
						}
					}
					SC_P_Ai_HideYourself(info->pl_id, &vec2, 5.0);
				}
			}
#ifdef MAX_WPS
			holdTimeout -= info->elapsed_time;
			if (holdTimeout > 0) return 0;
			if (SC_P_Ai_GetMode(info->pl_id) == SC_P_AI_MODE_BATTLE) return 0;
			SC_P_GetPos(info->pl_id, &vec);
			if (SC_IsNear3D(&vec, &pendlPath[wpi].wp, 1.0f)) {
				switch(pendlPath[wpi].action) {
				case PA_NONE:
					SC_P_DoAnimLooped(info->pl_id, NULL);
					if (wpi < MAX_WPS-1) 
						SC_P_Ai_Go(info->pl_id, &pendlPath[wpi+1].wp);
					else
						SC_P_Ai_Go(info->pl_id, &pendlPath[0].wp);

					break;

				case PA_WAIT:
					SC_P_Ai_Stop(info->pl_id);
					if (pendlPath[wpi].anim != NULL) SC_P_DoAnim(info->pl_id, pendlPath[wpi].anim);
					holdTimeout=pendlPath[wpi].data +frnd(pendlPath[wpi].data/4.0);
					bAnimLooped = TRUE;
					break;

				case PA_LOOP:
					SC_P_Ai_Stop(info->pl_id);
					vec.x = pendlPath[wpi].wp.x;
					vec.y = pendlPath[wpi].wp.y;
					vec.z = pendlPath[wpi].wp.z /*+ pendlPath[wpi].data*/;
					SC_P_SetPos(info->pl_id, &vec);
					if (pendlPath[wpi].anim != NULL) SC_P_DoAnimLooped(info->pl_id, pendlPath[wpi].anim);
					bAnimLooped = TRUE;
					holdTimeout=/*abs(frnd(pendlPath[wpi].data/2.0)) + */(pendlPath[wpi].data);
					break;
				}
				if (wpi < MAX_WPS-1) wpi++; else wpi=0;
			} else {
				//goTimer -= info->elapsed_time;
				SC_P_Ai_Go(info->pl_id, &pendlPath[wpi].wp);
				//if (goTimer < 0) {
					if (bAnimLooped) {
						bAnimLooped = FALSE;
						SC_P_DoAnimLooped(info->pl_id, NULL);
					}
				//	goTimer = GO_TIMER;
				//}
			}
#endif
			
			break;

		}//switch( gPhase )
		
		break;	//case SC_P_MES_TIME:

	case SC_P_MES_HIT:
		if (bAnimLooped) {
			bAnimLooped = FALSE;
			SC_P_DoAnimLooped(info->pl_id, NULL);
		}
		props.max_vis_distance	= 150.0;
		SC_P_Ai_SetProps(info->pl_id,&props);
		SC_P_Ai_SetMode(info->pl_id, SC_P_AI_MODE_BATTLE);
		SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_RETREAT);

		CLEAR(vec2);
		SC_P_GetPos(info->pl_id, &plPos);
		if (SC_MP_EnumPlayers(enum_pl, &num, SC_P_SIDE_VC)) {
			for (j=0; j<num; j++) {
				SC_P_GetPos(enum_pl[j].id, &vec);
				if ((dist = SC_2VectorsDist(&vec2, &vec)) < olddist) {
					olddist = dist;
					vec2.x = vec.x;
					vec2.y = vec.y;
					vec2.z = vec.z;
				}
			}
			SC_P_Ai_HideYourself(info->pl_id, &vec2, 5.0);
		}

		SC_sgi(B_DANGER, TRUE);
		break;

	case SC_P_MES_KILLED:
		if (bAnimLooped) {
			bAnimLooped = FALSE;
			SC_P_DoAnimLooped(info->pl_id, NULL);
		}
		bDead = TRUE;
		gPhase = GP_IDLE;
		SC_sgi(B_DANGER, TRUE);
		break;

	case SC_P_MES_EVENT:
		switch(info->param1)
		{
		case SCM_MP_REINIT:
			if (gPhase != GP_CREATE)
				info->next_exe_time = 1.0f;
				gPhase = GP_INIT;
			break;
		}
		break;

	}//switch( info->message )

	return 1;
}
