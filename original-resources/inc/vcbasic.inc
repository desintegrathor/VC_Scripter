//basic coop VC script

#include <inc\sc_global.h>
#include <inc\sc_def.h>

#define PVANGLE			3.0f
#define PVANGLENEAR		4.0f



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




dword	gPhase = 0;



int ScriptMain(s_SC_P_info *info)
{
	s_SC_P_Create		pinfo;
	s_SC_P_CreateEqp	eqp[10];
	s_SC_P_AI_props		props;
	s_SC_P_getinfo		plInfo;
	c_Vector3			plPos;
	dword				i, j;



	info->next_exe_time = 0.5f;


	switch( info->message )
	{
	case SC_P_MES_TIME:

		switch( gPhase )
		{
		case 0:
			CLEAR(pinfo);
			CLEAR(eqp);

			pinfo.type			= SC_P_TYPE_AI;
			pinfo.side			= SC_P_SIDE_VC;

			pinfo.group		= ID_GROUP;
			pinfo.member_id		= ID_MEMBER;

			pinfo.inifile		= INIFILENAME;
			pinfo.name_nr		= 2506;
			pinfo.icon_name		= "nhut";

			pinfo.weap_knife	= PKNIFE;
			pinfo.weap_pistol	= PPISTOL;
			pinfo.weap_main1	= PWEAPON1;
			pinfo.weap_main2	= PWEAPON2;
			pinfo.weap_slot1	= PWEAPONSLOT1;
				
			pinfo.recover_pos	= info->pos;

			pinfo.debrief_group	= SC_P_DEBRIEFGROUP_VC;

			pinfo.eqps = 0;
			
			//create
			info->pl_id = SC_P_Create(&pinfo);



			gPhase = 1;

			break;

		case 1:
			if ( !SC_P_IsReady(info->pl_id) ) 
				return 0;

			SC_P_Ai_EnableShooting(info->pl_id, TRUE);

			SC_P_Ai_SetPeaceMode(info->pl_id, SC_P_AI_PEACEMODE_HOLD);
			SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_ATTACK);
			SC_P_Ai_SetMode(info->pl_id, SC_P_AI_MODE_BATTLE);
			
			CLEAR(props);

			SC_P_Ai_GetProps(info->pl_id, &props);
							
			props.extend_searchway		= FALSE;
			props.shortdistance_fight	= 0.0f;
			props.view_angle			= PVANGLE;
			props.view_angle_near		= PVANGLENEAR;

			props.shoot_imprecision = 0;
			props.shoot_damage_mult = 1.3f;
			props.watchfulness_maxdistance = 1;
			props.reaction_time		= 0.01f;
			props.scout				= 0.1f + frnd(0.1f);
			props.berserk			= 0.1f;

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
			

			gPhase = 2;
			break;

		case 2:
			break;


		}//switch( gPhase )
		break;	//case SC_P_MES_TIME:

	case SC_P_MES_EVENT:
		switch(info->param1)
		{
		case SCM_MP_REINIT:
			if (gPhase != 1)
				gPhase = 1;
			break;
		}
		break;

	}


	return 1;
}
