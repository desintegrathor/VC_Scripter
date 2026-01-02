//
//	Global Level_h.h
//	by Beny
//


//We don't want to include any other .h






void SetPlayerWeapons(s_SC_P_Create *weap)
{
	weap->weap_knife=SC_ggi(PLAYER_WEAPON1); 
	if (!weap->weap_knife) weap->weap_knife=29;

	if (weap->weap_knife==PLAYER_FREESLOT) weap->weap_knife=0;
	
	weap->weap_pistol=SC_ggi(PLAYER_WEAPON2); 	
	if (!weap->weap_pistol) weap->weap_pistol=7;
	if (weap->weap_pistol==PLAYER_FREESLOT) weap->weap_pistol=0;


	weap->weap_main1=SC_ggi(PLAYER_WEAPON3);
	
	if (!weap->weap_main1) {
				
		if (SC_ggi(SGI_CURRENTMISSION)==MISSION_BIGRIVER) weap->weap_main1=23;
			else if (SC_ggi(SGI_CURRENTMISSION)<12) weap->weap_main1=25; 
				else weap->weap_main1=1;
	}
	
	if (weap->weap_main1==PLAYER_FREESLOT) weap->weap_main1=0;
	
	weap->weap_main2=SC_ggi(PLAYER_WEAPON4);
	if (weap->weap_main2==PLAYER_FREESLOT) weap->weap_main2=0;

	weap->weap_slot1=SC_ggi(PLAYER_WEAPON5);
	if (!weap->weap_slot1) weap->weap_slot1=59;
	if (weap->weap_slot1==PLAYER_FREESLOT) weap->weap_slot1=0;

	weap->weap_slot6=SC_ggi(PLAYER_WEAPON6);
	if (weap->weap_slot6==PLAYER_FREESLOT) weap->weap_slot6=0;

	weap->weap_slot7=SC_ggi(PLAYER_WEAPON7);
	if (weap->weap_slot7==PLAYER_FREESLOT) weap->weap_slot7=0;

	weap->weap_slot8=SC_ggi(PLAYER_WEAPON8);
	if (!weap->weap_slot8) weap->weap_slot8=63;
	if (weap->weap_slot8==PLAYER_FREESLOT) weap->weap_slot8=0;

	weap->weap_slot9=SC_ggi(PLAYER_WEAPON9);
	if (weap->weap_slot9==PLAYER_FREESLOT) weap->weap_slot9=0;
	
	weap->weap_slot10=58;
}

void SavePlayerWeapons()
{
	s_SC_P_Create info;

	SC_P_GetWeapons(SC_PC_Get(), &info);
	if (info.weap_knife) SC_sgi(PLAYER_WEAPON1,info.weap_knife);
		else SC_sgi(PLAYER_WEAPON1,PLAYER_FREESLOT);
	if (info.weap_pistol) SC_sgi(PLAYER_WEAPON2,info.weap_pistol);
		else SC_sgi(PLAYER_WEAPON2,PLAYER_FREESLOT);
	if (info.weap_main1) SC_sgi(PLAYER_WEAPON3,info.weap_main1);
		else SC_sgi(PLAYER_WEAPON3,PLAYER_FREESLOT);
	if (info.weap_main2) SC_sgi(PLAYER_WEAPON4,info.weap_main2);
		else SC_sgi(PLAYER_WEAPON4,PLAYER_FREESLOT);
	if (info.weap_slot1) SC_sgi(PLAYER_WEAPON5,info.weap_slot1);
		else SC_sgi(PLAYER_WEAPON5,PLAYER_FREESLOT);
	if (info.weap_slot6) SC_sgi(PLAYER_WEAPON6,info.weap_slot6);
		else SC_sgi(PLAYER_WEAPON6,PLAYER_FREESLOT);
	if (info.weap_slot7) SC_sgi(PLAYER_WEAPON7,info.weap_slot7);
		else SC_sgi(PLAYER_WEAPON7,PLAYER_FREESLOT);
	if (info.weap_slot8) SC_sgi(PLAYER_WEAPON8,info.weap_slot8);
		else SC_sgi(PLAYER_WEAPON8,PLAYER_FREESLOT);
	if (info.weap_slot9) SC_sgi(PLAYER_WEAPON9,info.weap_slot9);
		else SC_sgi(PLAYER_WEAPON9,PLAYER_FREESLOT);
	if (info.weap_slot10)	SC_sgi(PLAYER_WEAPON10,info.weap_slot10);
		else SC_sgi(PLAYER_WEAPON10,PLAYER_FREESLOT);
}



void SetPlayerHealth()
{
	SC_P_ReadHealthFromGlobalVar(SC_PC_Get(),PLAYER_HEALTHSTART);
}

void SavePlayerHealth()
{
	SC_P_WriteHealthToGlobalVar(SC_PC_Get(),PLAYER_HEALTHSTART);
}

void SetPlayerAmmo()
{
	SC_P_ReadAmmoFromGlobalVar(SC_PC_Get(),PLAYER_AMMOSTART,PLAYER_AMMOLAST);
	if (SC_ggi(PLAYER_AMMOINGUN)) SC_P_SetAmmoInWeap(SC_PC_Get(),2,SC_ggi(PLAYER_AMMOINGUN));
	if (SC_ggi(PLAYER_AMMOINPISTOL)) SC_P_SetAmmoInWeap(SC_PC_Get(),1,SC_ggi(PLAYER_AMMOINPISTOL));
}

void SavePlayerAmmo()
{
	SC_P_WriteAmmoToGlobalVar(SC_PC_Get(),PLAYER_AMMOSTART,PLAYER_AMMOLAST);
	SC_sgi(PLAYER_AMMOINGUN,SC_P_GetAmmoInWeap(SC_PC_Get(),2));
	SC_sgi(PLAYER_AMMOINPISTOL,SC_P_GetAmmoInWeap(SC_PC_Get(),1));
}

void SavePlayerIntel()
{
	s_SC_P_intel intel;
	int i;
	
	SC_PC_GetIntel(&intel);
	for (i=0;i<SC_P_INTEL_MAX;i++){
		SC_sgi(PLAYER_INTELSTART+i,intel.intel[i]);
	}
}

void SetPlayerIntel()
{
	s_SC_P_intel intel;
	int i;
	
	for (i=0;i<SC_P_INTEL_MAX;i++){
		intel.intel[i]=SC_ggi(PLAYER_INTELSTART+i); 
	}
	SC_PC_SetIntel(&intel);
}



//
void SavePlayerStatus(BOOL bCompleted)
{
	SavePlayerWeapons();
	SavePlayerAmmo();
	SavePlayerHealth();
	SavePlayerIntel();

	if (bCompleted)
		SC_MissionCompleted();
	else
		SC_MissionDone();
}

void SetPlayerStatus()
{
	SetPlayerHealth();
	SetPlayerAmmo();
	SetPlayerIntel();
}
