//basic bot script
//Pas de modification ici

#include <inc\sc_global.h>
#include <inc\sc_def.h>

dword	gPhase = 0;

int ScriptMain(s_SC_P_info *info)
{
	s_SC_P_Create		pinfo;
	s_SC_P_CreateEqp	eqp[10];
	s_SC_P_AI_props		props;
	s_SC_P_getinfo		plInfo;
	c_Vector3			plPos;
	dword				i, j;
	int 				eqpcount;

	info->next_exe_time = 0.5f;


	switch( info->message )
	{
	case SC_P_MES_TIME:

		switch( gPhase )
		{
		case 0:					// gPhase = 0 -> Création du bot
			CLEAR(pinfo);
			CLEAR(eqp);

			// préparation du player
			pinfo.type			= SC_P_TYPE_AI;			// type AI 
			pinfo.side			= SIDE;					// équipe : SC_P_SIDE_VC ou SC_P_SIDE_US

			pinfo.group			= GROUPID;				// groupe du l'AI, paramétrable dans le player.c et dans le level.c
			pinfo.member_id		= MEMBERID;				// classe spécial d'un bot

			pinfo.inifile		= INIFILENAME;			// skin du bot
			pinfo.name_nr		= NAMENUMBER;			// nom du bot

			pinfo.weap_knife	= PKNIFE;				// emplacement du couteau
			pinfo.weap_pistol	= PPISTOL;				// emplacement du pistolet
			pinfo.weap_main1	= PWEAPON1;				// emplacement arme principale
			pinfo.weap_main2	= PWEAPON2;				// emplacement arme secondaire
			pinfo.weap_slot1	= PWEAPONSLOT1;			// emplacement pour les équipements spéciaux
														// slot dispo : pinfo.weap_slot6, 7, 8, 9 & 10	
				
			pinfo.recover_pos	= info->pos;			// point de respawn

			pinfo.debrief_group	= SC_P_DEBRIEFGROUP_VC;		// Pour contabiliser les différents tués dans le debrifing du solo
			
			pinfo.eqps = 0;
			if (EQUIP_BOOL) {
				pinfo.flags = SC_P_CREATE_FL_DISABLE_EQPGEN;	// desactive l'auto équipement si eqps=0
				equipplayer(eqp,&eqpcount);						// préparation de l'équipement
				pinfo.eqps = eqpcount;							// stockage du nombre d'équipements 
				pinfo.eqp = eqp;								// stockage de l'équipement
			}
			
			// création du player + son équipement + ses armes
			info->pl_id = SC_P_Create(&pinfo);			

			// fin de la création
			gPhase = 1;
			break;

		case 1:				// gPhase = 1 -> Modification des caractéristiques du bot
			if ( !SC_P_IsReady(info->pl_id) ) 
				return 0;

			SC_P_Ai_EnableShooting(info->pl_id, TRUE);							// le bot peut tirer

			SC_P_Ai_SetPeaceMode(info->pl_id, SC_P_AI_PEACEMODE_HOLD);			// lorsque que le bot sera en "PeaceMode", il restera sur place
			SC_P_Ai_SetBattleMode(info->pl_id, SC_P_AI_BATTLEMODE_ATTACK);		// lorsque que le bot sera en "BattleMode", il attaquera l'ennemi
			SC_P_Ai_SetMode(info->pl_id, SC_P_AI_MODE_BATTLE);					// le bot est controlé par le script "Battle"
			
			CLEAR(props);

			SC_P_Ai_GetProps(info->pl_id, &props);				// recup des propriétés du bot
							
			props.extend_searchway		= FALSE;				// pour le solo
			props.shortdistance_fight	= 0.0f;					// calcul du temp que me la balle à atteindre sa cible ? gourement en ressource
			props.view_angle			= B_PVANGLE;				// angle de vision du bot
			props.view_angle_near		= B_PVANGLENEAR;			// 			"			  de près

			props.max_vis_distance = B_MAXVISU;					// Distance max à laquelle un bot peut voir
			props.hear_imprecision = B_HEARPREC;				// Qualité d'écoute du bot : 0 tout, 1 beaucoup, ... , 4 sourd comme un pot
			props.hear_distance_max = B_HEARDIST;				// Distance max à laquelle un bot peu entendre
			props.peace_fakeenemy_run = B_RUN;					// Lorsque le bot voie un ennemis : 0 marche, 1 cours, 0.5 50/50
			props.peace_fakeenemy_phase = B_PHASE;				// 		" pour debout/accroupi
			
			props.watchfulness_maxdistance = 1;								// le bot sait reconnaitre les ennemis des anims de loin 
			props.reaction_time		= 0.01f;								// temps de réaction après le premier impact que le bot reçoit
			props.scout				= B_SCOUT + frnd(B_SCOUT_A);			// le bot avance-t-il vers l'ennemis : 0 jamais, 1 toujours
			props.berserk			= B_BERSERK + frnd(B_BERSERK_A);		// % de chance que le bot attaque sans couverture : 0 jamais, 1 toujours


			switch( SC_ggi(SGI_DIFFICULTY) )					// en fonction de la difficulté du serveur : 
			{
			case 0:		// Facile
				props.shoot_imprecision		= 1.5f;						// tir : 0 précis, 1 défaut, 2 imprécis				
				props.shoot_damage_mult		= 0.5f;						// mutliplicateur des dommages que font subir le bot 
				props.grenade_throw_imprecision = 1.5f + frnd(0.5f);	// précision du lancement de grenade : 0 parfait, 1 bon, 2 moyen
				break;

			case 1:		// Normal
				props.shoot_imprecision		= 1.0f;
				props.shoot_damage_mult		= 1.0f;
				props.grenade_throw_imprecision = 1.0f + frnd(0.5f);
				break;

			case 2:		// Difficile
				props.shoot_imprecision		= 0.3f;
				props.shoot_damage_mult		= 1.1f;
				props.grenade_throw_imprecision = 0.5f + frnd(0.5f);
				break;

			case 3:		// Vietnam
				props.shoot_imprecision		= 0.0f;
				props.shoot_damage_mult		= 1.2f;
				props.grenade_throw_imprecision = 0.3f + frnd(0.3f);
				break;
			}

			SC_P_Ai_SetProps(info->pl_id,&props);				// injection des props dans le bot
			
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
