
// mplevel.inc 

void DisableBedny(void){
	dword i;
	char txt[256];
	void *nod,*chi;

	for (i=0;i<100;i++){

		sprintf(txt,"bedna%d",i);
		
		nod = SC_NOD_GetNoMessage_Entity(txt);
		if (nod){					
			SC_NOD_SetDSTR(nod,"Bedna_dlouha",NULL);

			chi = SC_NOD_GetNoMessage(nod,"Bedna_dlouha_viko");
			if (chi) SC_NOD_SetDSTR(nod,"Bedna_dlouha_viko",NULL);
		}
	

	}// for (i)


}// void DisableBedny(void)


void DisableRW(void){
	dword i;
	char txt[32];
	void *nod;

	for (i=0;i<20;i++){

		sprintf(txt,"W%c_flag",'A'+i);
		
		nod = SC_NOD_GetNoMessage_Entity(txt);
		if (nod){					
			SC_DUMMY_Set_DoNotRenHier2(nod,TRUE);
		}	

	}// for (i)

}// void DisableRW(void)


void DisableTT(void){
	dword i;
	char txt[32];
	void *nod;	

	for (i=0;i<20;i++){

		sprintf(txt,"TT_flag_%d",i);
		
		nod = SC_NOD_GetNoMessage_Entity(txt);
		if (nod){					
			SC_DUMMY_Set_DoNotRenHier2(nod,TRUE);
		}	

	}// for (i)

}// void DisableRW(void)


void SetAmmoBoxes(char *name, BOOL enable){
	dword i;
	char txt[256];
	void *nod,*chi;


	if (!SC_MP_GetAmmoBoxesEnabled()) enable = FALSE;

	for (i=0;i<10;i++){

		sprintf(txt,"%s%d",name,i);
		
		nod = SC_NOD_GetNoMessage_Entity(txt);
		if (nod){

			if (enable){
				SC_SetObjectScript(txt,"Ini\\Multiplayer\\scripts\\addammo_dobj.c");
			}// if (enable)
			else{
				SC_NOD_SetDSTR(nod,"Bedna_Kratka",NULL);
			}

		}// if (nod)
	
	}// for (i)

}// void SetAmmoBoxes(char *name, BOOL enable)


void InitScene(s_SC_L_info *info){
	BOOL hide_weapons,hide_CTF_flags,teamgame,hideRW,hideTT;
	void *nod;
   	   
	hide_weapons = TRUE;
	hide_CTF_flags = TRUE;
	teamgame = TRUE;
	hideRW = TRUE;
	hideTT = TRUE;

	switch(SC_ggi(GVAR_MP_MISSIONTYPE)){

		case GVAR_MP_MISSIONTYPE_RW:
				hideRW = FALSE;
				break;

		case GVAR_MP_MISSIONTYPE_ATG:		   					
				break;

		case GVAR_MP_MISSIONTYPE_CTF:
				hide_CTF_flags = FALSE;
				break;

		case GVAR_MP_MISSIONTYPE_CTR:
		case GVAR_MP_MISSIONTYPE_LMS:
		case GVAR_MP_MISSIONTYPE_DM:
				teamgame = FALSE;
				hide_weapons = FALSE;
				break;

		case GVAR_MP_MISSIONTYPE_TDM:
				hide_weapons = FALSE;
				break;

		case GVAR_MP_MISSIONTYPE_TT:
				hideTT = FALSE;
				break;


	}// switch(SC_ggi(GVAR_MP_MISSIONTYPE))

	SC_MP_SetTeamGame(teamgame);

	if (hide_weapons){
		SC_MP_SRV_InitWeaponsRecovery(-1.0f);
		DisableBedny();
	}// if (hide_weapons)

	if (hide_CTF_flags){
		nod = SC_NOD_GetNoMessage_Entity("flag_us");
		if (nod) SC_DUMMY_Set_DoNotRenHier2(nod,TRUE);

		nod = SC_NOD_GetNoMessage_Entity("flag_vc");
		if (nod) SC_DUMMY_Set_DoNotRenHier2(nod,TRUE);

		SetAmmoBoxes("AmmoboxCTF",FALSE);
	}// if (hide_CTF_flags)
	else{
		SetAmmoBoxes("AmmoboxCTF",TRUE);
	}

	if (hideRW){
		DisableRW();
		SetAmmoBoxes("AmmoboxRW",FALSE);
	}// if (hideRW)
	else
		SetAmmoBoxes("AmmoboxRW",TRUE);


	if (hideTT) DisableTT();
			

}// void InitScene(s_SC_L_info *info)
