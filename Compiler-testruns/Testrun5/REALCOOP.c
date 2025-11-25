/*
	SqBaker-JARAI REAL-COOP script test 10 version
*/

#include <inc\sc_global.h>
#include <inc\sc_def.h>

//#define SGI_CHOPPERPULASKI		14
//#define SGI_CHOPPERRESTART		15
//#define SGI_CHOPPERPULASKIRESTART	16

#define COOP_MODE 1
#define REAL_MODE 2
#define GAME_MODE 2  //universal script for COOP and REAL - just change
#define EXPLORE_MODE FALSE		//VC cannot shoot - special testing mode


#define ENABLE_MOVING 	TRUE
#define DISABLE_MOVING 	FALSE

#define GVAR_GPHASE				500
#define GVAR_CHOPPER				501

#define NORECOV_TIME	3.0f		// disable time of recoverplace after recovering someone there




#define REC_MAX_ALTERNATIVES	1    // num of alternate respawn areas (for all - US and VC)

#define REC_WPNAME_US	"USSpawn_coop_%d"  //alternativy "USSpawn_coop_101","USSpawn_coop_201"
#define REC_WPNAME_VC	"VCSpawn_coop_%d"  //100x alternative + 1x respawnpoint (max.12)
#define REC_MAX			12

#define REC_USHUMAN		12   // 12   max number of...
#define REC_VCHUMAN		2    // 2
#define REC_USAI		7    //!!!!!!
#define REC_VCAI		40   //!!!!!!





dword gRecs[2] = {0,0};
s_SC_MP_Recover gRec[2][REC_MAX];
float gRecTimer[2][REC_MAX];



float gNextRecover = 0.0f;

dword gEndRule;
dword gEndValue;
float gTime;

#define GPHASE_BEGIN			1
#define GPHASE_GAME			2
#define GPHASE_DONE			3
#define GPHASE_FAILED			4
#define GPHASE_GAME1			991 /////// phases for controlling game - UH landing, VC respawn etc.
#define GPHASE_GAME2			992
#define GPHASE_GAME3			993
#define GPHASE_GAME4			994
#define GPHASE_GAME5			995
#define GPHASE_GAME6			996
#define GPHASE_GAME7			997



extern void SC_P_SetPos(dword pl_id, c_Vector3 *pos);
extern void SC_P_SetActive(dword pl_id, BOOL active);
extern BOOL SC_P_GetActive(dword pl_id);
extern void SC_P_Recover(dword pl_id, c_Vector3 *pos, float rz);
extern void SC_Ai_SetShootOnHeardEnemyColTest(BOOL do_test);
extern void SC_P_ChangeWeapon(dword pl_id, dword slot_id, dword weap_type);
extern void SC_PC_EnableFlashLight(BOOL enable); 
//extern void SC_SetMapFpvModel(char *bes_filename);
extern void SC_P_DoHit(dword pl_id, dword area_id, float hp);
extern BOOL SC_MP_RecoverAiPlayer(dword pl_id, c_Vector3 *pos, float rz);
//
extern void SC_SetViewAnim(char *anm_name, dword start_frame, dword end_frame, dword callback_id); 
//animation of Jarai attack




float				g_Mortar_Time = 0.0f;		// Moter interval Timer


dword gPhase = GPHASE_BEGIN;
float gPhase_timer = 5.0f;
dword gPhase_send = 0;

BOOL gValidSide0 = FALSE;

dword gRecoverTime = 0;
dword gRecoverLimit = 0;

float gAllNoAiRecover  = 0.0f;



	
char	txt[32],*itxt;




void Explore_gamemode(void) {
	dword i,j,k;
	s_SC_MP_EnumPlayers		enum_pl[64];


	j=64;

	if (!SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i=1; i<j; i++){    //0-64
		if (SC_P_IsReady(enum_pl[i].id)){   
			//SC_P_Ai_EnableShooting(enum_pl[i].id, FALSE);  //did't work - game crashed
			SC_P_ChangeWeapon(enum_pl[i].id, 1, NULL);
			SC_P_ChangeWeapon(enum_pl[i].id, 2, NULL);
			SC_P_ChangeWeapon(enum_pl[i].id, 3, NULL);
			SC_P_ChangeWeapon(enum_pl[i].id, 4, NULL);
			SC_P_ChangeWeapon(enum_pl[i].id, 5, NULL);



		}//endif

	}//endfor


}//end of Explore_gamemode




BOOL SRV_CheckEndRule(float time){

	switch(gEndRule){
		case SC_MP_ENDRULE_TIME:			

			if (gValidSide0) gTime += time;
			SC_MP_EndRule_SetTimeLeft(gTime,gValidSide0);

			if (gTime>gEndValue){
				SC_MP_LoadNextMap();
				return TRUE;
			}

			break;

		default:
			SC_message("EndRule unsopported: %d",gEndRule);
			break;

	}// switch(gEndRule)

	return FALSE;

}// void SRV_CheckEndRule(float time)


int SRV_Random(int max)			// Random number generation
{
	int a;

	a = (int)(frnd(1.0f) * 32767.0f) % max;
	if(a<0)
		return -a+1;
	else
		return a+1;
}//int SRV_Random(int max)

BOOL SC_GetDummyPos(char *name, c_Vector3 *vec)
{
	void *mobj;

	mobj = SC_NOD_Get(NULL, name);
	if (mobj == NULL)
		return FALSE;

	SC_NOD_GetWorldPos(mobj, vec);
	return TRUE;
}




void Presun_hrace(int strana, int skupina, int hrac, int umisteni){
	//int umisteni;
	c_Vector3	teleportpos;
	char 	nazev[30]; 
	
	
	//umisteni = SRV_Random(poc_mist);

	if (strana == 0){
		sprintf(nazev,"US-%01d-%01d-%01d", skupina, hrac, umisteni); // alternativy "US-1-6-101", "US-1-6-201","US-1-6-301"
	}
	else{
		sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	}




	SC_GetDummyPos(nazev, &teleportpos);
	SC_P_SetPos(SC_P_GetBySideGroupMember(strana,skupina,hrac), &teleportpos);

}

void Presuny1(int alter){
	int RND_misto;

	RND_misto = SRV_Random(5); 
	Presun_hrace(1,1,1,RND_misto+100*alter);//kamper1
	RND_misto = SRV_Random(5);
	Presun_hrace(1,2,1,RND_misto+100*alter);//kamper2

	RND_misto = SRV_Random(1);
	Presun_hrace(1,5,1,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,5,2,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,5,3,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,5,4,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,6,1,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,6,2,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,6,3,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,6,4,RND_misto+100*alter);

	RND_misto = SRV_Random(1);
	Presun_hrace(1,8,1,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,8,2,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,8,3,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,8,4,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,9,1,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,9,2,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,9,3,RND_misto+100*alter);
	RND_misto = SRV_Random(1);
	Presun_hrace(1,9,4,RND_misto+100*alter);





} //Presuny1


void Presuny2(int alter){
	int RND_misto;
	int skupina, hrac, umisteni;
	c_Vector3 respawnpos;
	c_Vector3 attackpos;
	char 	nazev[30]; 


	sprintf(nazev,"SPOUSTEC2");
	SC_GetDummyPos(nazev, &attackpos);



	skupina = 1;
	hrac = 1;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);


	skupina = 2;
	hrac = 1;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	skupina = 5;
	hrac = 1;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	skupina = 5;
	hrac = 2;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	skupina = 5;
	hrac = 3;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	skupina = 5;
	hrac = 4;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);


	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,1,1), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,2,1), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,5,1), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,5,2), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,5,3), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,5,4), &attackpos);




} //Presuny2

void Presuny3(int alter){
	int RND_misto;
	int skupina, hrac, umisteni;
	c_Vector3 respawnpos;
	c_Vector3 attackpos;
	char 	nazev[30]; 


	sprintf(nazev,"SNIPERPOS");
	SC_GetDummyPos(nazev, &attackpos);



	skupina = 6;
	hrac = 1;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);


	skupina = 6;
	hrac = 2;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	skupina = 6;
	hrac = 3;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	skupina = 6;
	hrac = 4;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	


	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,6,1), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,6,2), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,6,3), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,6,4), &attackpos);





} //Presuny3

void Presuny4(int alter){
	int RND_misto;
	int skupina, hrac, umisteni;
	c_Vector3 respawnpos;
	c_Vector3 attackpos;
	char 	nazev[30]; 


	sprintf(nazev,"SPOUSTEC4");
	SC_GetDummyPos(nazev, &attackpos);



	skupina = 8;
	hrac = 1;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);


	skupina = 8;
	hrac = 2;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	skupina = 8;
	hrac = 3;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	skupina = 8;
	hrac = 4;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	


	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,8,1), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,8,2), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,8,3), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,8,4), &attackpos);





} //Presuny4

void Presuny5(int alter){
	int RND_misto;
	int skupina, hrac, umisteni;
	c_Vector3 respawnpos;
	c_Vector3 attackpos;
	char 	nazev[30]; 


	sprintf(nazev,"MAPA");
	SC_GetDummyPos(nazev, &attackpos);



	skupina = 9;
	hrac = 1;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);


	skupina = 9;
	hrac = 2;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	skupina = 9;
	hrac = 3;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	skupina = 9;
	hrac = 4;
	umisteni = SRV_Random(1)+100*alter;
	sprintf(nazev,"VC-%01d-%01d-%01d", skupina, hrac, umisteni);
	SC_GetDummyPos(nazev, &respawnpos);
	SC_MP_RecoverAiPlayer(SC_P_GetBySideGroupMember(1,skupina,hrac), &respawnpos, 0.0f);

	


	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,9,1), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,9,2), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,9,3), &attackpos);
	SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,9,4), &attackpos);





} //Presuny5

void SRV_CheckUpdate(void){

	if (gPhase_send!=gPhase){

		gPhase_send = gPhase;

		SC_sgi(GVAR_GPHASE,gPhase);

	}// if (gPhase_send!=gPhase)

}// void SRV_CheckUpdate(void)







dword Spocti_US_AI(void){ //spocte zivy USAI
	dword i,j;
	dword zivyUS;	

	zivyUS = 0;
	for (i=1; i<20; i++){
		for (j=1; j<20; j++){

			if (SC_P_IsReady(SC_P_GetBySideGroupMember(0,i,j))){
				zivyUS++;	
			}
		}

	}
	return zivyUS;

}//Spocti_US_AI



dword Spocti_VC_AI(void){ //spocte zivy VCAI
	dword i,j;
	dword zivyVC;	

	zivyVC = 0;
	for (i=0; i<20; i++){
		for (j=0; j<20; j++){

			if (SC_P_IsReady(SC_P_GetBySideGroupMember(1,i,j))){
				zivyVC++;	
			}
		}

	}
	return zivyVC;

}//Spocti_VC_AI



void Check_BALANCE(void){  		// pri pripojenych 2 VC zabrani po restartu mapy znovu pripojit za VC tretimu hraci, 					// nefunfuje pri prvnim vyberu
	int val;
	dword side,nr_to_change;
	s_SC_P_getinfo info;
	s_SC_MP_EnumPlayers enum_pl[64];
	dword i,j,k;
	dword poc_us, poc_vc;

	side = 0;
	j = 64;
	poc_us = 0;
	poc_vc = 0;

	if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)){	

		for (i=0; i<65; i++){
			if ((enum_pl[i].side==0)&&((enum_pl[i].status==SC_MP_P_STATUS_INGAME)||(enum_pl[i].status==SC_MP_P_STATUS_INGAMEDEATH))) poc_us++;
		}//for

	}//if

	
	if (poc_us>REC_USAI){
		SC_MP_SetChooseValidSides(3);
	}
	else{
		SC_MP_SetChooseValidSides(1);
	}// if(poc_us...


}// void Check_BALANCE(dword pl_handle)


void Dizejbluj_VC(void){
	s_SC_P_getinfo info;
	s_SC_MP_EnumPlayers enum_pl[64];
	dword i,j,k;
	dword side;
	s_SC_P_getinfo plinfo;



	side = 1;
	j = 64;


	SC_P_GetInfo(SC_PC_Get(),&plinfo);
	if (plinfo.side==1){


		if (gPhase < 991){ //gPhase game1
			SC_PC_EnableMovement(FALSE);


			SC_P_ChangeWeapon(SC_PC_Get(), 1, NULL);
			SC_P_ChangeWeapon(SC_PC_Get(), 2, NULL);
			SC_P_ChangeWeapon(SC_PC_Get(), 3, NULL);
			SC_P_ChangeWeapon(SC_PC_Get(), 4, NULL);
			SC_P_ChangeWeapon(SC_PC_Get(), 5, NULL);
			SC_P_ChangeWeapon(SC_PC_Get(), 6, NULL);
			SC_P_ChangeWeapon(SC_PC_Get(), 7, NULL);
			SC_P_ChangeWeapon(SC_PC_Get(), 8, NULL);
			SC_P_ChangeWeapon(SC_PC_Get(), 9, NULL);

			


		}
		else {
			SC_PC_EnableMovement(TRUE);
		}//end of else

	}//if (plinfo.side==1)	


}//Dizejbluj_VC





void HiddenVC(int ref_side, int ref_group, int ref_pl_id, float ref_diameter){
	dword i, j;
	dword ref_PLAYER_nr, ref_AI_nr;
	float distance;
	
		ref_AI_nr = SC_P_GetBySideGroupMember(ref_side, ref_group, ref_pl_id);  //cislo VC AI
		if (!SC_P_IsReady(ref_AI_nr)) return;

			distance = SC_P_Ai_GetNearestEnemyDist(ref_AI_nr);  //zjisteni vzdalenosti

			if (distance < ref_diameter){
				//navrat do boje
				SC_P_Ai_SetMode(ref_AI_nr, SC_P_AI_MODE_BATTLE);
				SC_Ai_SetStealthMode(ref_side, ref_group, FALSE);
				SC_P_Ai_EnableShooting(ref_AI_nr, TRUE);
				SC_P_Ai_SetStaticMode(ref_AI_nr, FALSE);
				//SC_P_Ai_SetMovePos(ref_AI_nr, 0);

			}
			else {
				//znehybneni
				SC_P_Ai_SetMode(ref_AI_nr, SC_P_AI_MODE_SCRIPT);
				SC_Ai_SetStealthMode(ref_side, ref_group, TRUE);
				SC_P_Ai_SetMovePos(ref_AI_nr, 2); // 2 = lie
				SC_P_Ai_EnableShooting(ref_AI_nr, FALSE);
				SC_P_Ai_SetStaticMode(ref_AI_nr, TRUE);

			}//endofelse


	

}//endofHiddenVC



void VesnicaniJarai(int ref_side, int ref_group, int ref_pl_id, float ref_diameter, BOOL hecanmove){
	dword i, j;
	dword ref_PLAYER_nr, ref_AI_nr;
	float distance;
	c_Vector3 jaraipos;
	//s_SC_MP_EnumPlayers		enum_pl[64];


		j=64;
		ref_AI_nr = SC_P_GetBySideGroupMember(ref_side, ref_group, ref_pl_id);  //cislo VC AI


		if (!SC_P_IsReady(ref_AI_nr)) return;


			if (SC_P_Ai_GetEnemies(ref_AI_nr)>0){
				if (hecanmove == ENABLE_MOVING) SC_P_Ai_SetStaticMode(ref_AI_nr, FALSE);
				SC_P_Ai_SetMode(ref_AI_nr, SC_P_AI_MODE_BATTLE);  
			//vidi nepritele a zacne bojovat
				return;
			}//end of if getenemies
		
			SC_P_Ai_SetMode(ref_AI_nr, SC_P_AI_MODE_SCRIPT);
			//sprintf(txt,"Jaraipos_%d",ref_pl_id);	
			//SC_GetDummyPos(txt, &jaraipos);		
			//SC_P_Ai_Go(SC_P_GetBySideGroupMember(ref_side,ref_group,ref_pl_id), &jaraipos);
			SC_P_Ai_SetStaticMode(ref_AI_nr, TRUE);
			//if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)){	

				//for (i=0; i<64; i++){
					//distance=20.0f;
					//if (SC_P_IsReady(enum_pl[i].id)&&(enum_pl[i].side=0))   distance=SC_P_GetDistance(ref_AI_nr, enum_pl[i].id);
			
					//if (distance < ref_diameter ){
						SC_P_Ai_SetMovePos(ref_AI_nr, 0); 
					//}		
					//else {
					//	SC_P_Ai_SetMovePos(ref_AI_nr, 2);//1
					//}

				//}//end of for



			//}//endif enumplayers
	
		
}//endofVesnicaniJarai

void Hide_Handmap(void){
	c_Vector3 startpos;
	c_Vector3 mappos;
	c_Vector3 playerpos;
	dword player_id;
	dword villager_id;
	s_SC_P_getinfo plinfo;
	dword ref_HUMAN_nr;	




	SC_P_GetInfo(SC_PC_Get(),&plinfo);
	ref_HUMAN_nr = SC_P_GetBySideGroupMember(plinfo.side, plinfo.group, plinfo.member_id);
	SC_P_GetPos(ref_HUMAN_nr, &playerpos);

	SC_GetDummyPos("HideMap", &startpos);
	SC_GetDummyPos("MAPA", &mappos);

	//villager_id=SC_P_GetBySideGroupMember(0, 1, 2); //Jarai chief
	//SC_P_GetPos(villager_id, &villagerpos);
	

	if (SC_IsNear2D(&playerpos, &startpos, 10.0f)){
		SC_P_ChangeWeapon(SC_PC_Get(), 9, NULL);
	}// je blizko startu




	if (SC_IsNear2D(&playerpos, &mappos, 2.0f)){
		SC_P_ChangeWeapon(SC_PC_Get(), 9, 58); //nevim co ma za cislo handmapa, 58???

		
	}// je blizko stolu

		





}//end of Hide_Handmap

void Burn_Sphere(void){			/////////////    Ohniste - not working properly, see new version
	c_Vector3 fireplacepos;
	c_Vector3 playerpos;

	dword i,j;
	float distance;
	s_SC_MP_EnumPlayers		enum_pl[64];

	j=64;

	SC_GetDummyPos("burnsphere", &fireplacepos);
	if (!SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i=0; i<j; i++){    //0-64
		if (SC_P_IsReady(enum_pl[i].id)){   
		 //if (!enum_pl[i].group_id==1) return;
		 SC_P_GetPos(enum_pl[i].id,&playerpos);
				
		 if (SC_IsNear2D( &playerpos, &fireplacepos, 0.3f )){
			
			SC_P_DoHit(enum_pl[i].id, SC_P_MESH_AREA_BODYFRONT, 0.1f); // ******DODELAT************
			SC_P_DoHit(enum_pl[i].id, SC_P_MESH_AREA_LEFTLEG, 0.1f);   // ****NEFUNGUJE PRO MP*****
			SC_P_DoHit(enum_pl[i].id, SC_P_MESH_AREA_RIGHTLEG, 0.1f);

 		 }//end of if isnear		
		}//end of isready

	}//end of for



}//end of Burn_Sphere

void Burn_Sphere2(void){			/////////////    Ohniste
	c_Vector3 fireplacepos;
	c_Vector3 playerpos;
	s_SC_P_getinfo plinfo;
	dword ref_HUMAN_nr;	
	dword i,j;
	float distance;
	s_SC_MP_EnumPlayers		enum_pl[64];




	SC_P_GetInfo(SC_PC_Get(),&plinfo);
	ref_HUMAN_nr = SC_P_GetBySideGroupMember(plinfo.side, plinfo.group, plinfo.member_id);
	SC_P_GetPos(ref_HUMAN_nr, &playerpos);

	SC_GetDummyPos("burnsphere", &fireplacepos);
	


	if (SC_P_IsReady(enum_pl[i].id)){   
				
		 if (SC_IsNear2D( &playerpos, &fireplacepos, 0.3f )){
			
			SC_P_DoHit(enum_pl[i].id, SC_P_MESH_AREA_BODYFRONT, 0.1f); // ******DODELAT************
			SC_P_DoHit(enum_pl[i].id, SC_P_MESH_AREA_LEFTLEG, 0.1f);   // ****NEFUNGUJE PRO MP*****
			SC_P_DoHit(enum_pl[i].id, SC_P_MESH_AREA_RIGHTLEG, 0.1f);

 		 }//end of if isnear		
	}//end of isready





}//end of Burn_Sphere2

void Spoustec0(int alternativa){			/////////////    HUEY START
	c_Vector3 spoustec0pos;
	c_Vector3 playerpos;

	dword i,j;
	float distance;
	s_SC_MP_EnumPlayers		enum_pl[64];

	j=64;

	SC_GetDummyPos("SPOUSTEC0", &spoustec0pos);
	if (!SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i=0; i<j; i++){    //0-64
		if (SC_P_IsReady(enum_pl[i].id)){   
		 //if (!enum_pl[i].group_id==1) return;
		 SC_P_GetPos(enum_pl[i].id,&playerpos);
				
		 if (SC_IsNear2D( &playerpos, &spoustec0pos, 10.0f )&&(enum_pl[i].side==0)){
			
			/////////////////////////////////////////////
			/////////////////////////////////////////////
			//SC_sgi(SGI_CHOPPER,2); //spusteni vrtulniku - nahradit zmenou faze
			/////////////////////////////////////////////
			/////////////////////////////////////////////

			Presuny1(alternativa); //teleport VC posadky na sva mista			
			if (EXPLORE_MODE==TRUE) Explore_gamemode();  //EXPLORE GAME MODE = VC CANNOT SHOOT
			
			/////////////////////
			/////////////////////
			/////////////////////

			gPhase = GPHASE_GAME1;
			//gPhase = GPHASE_GAME6; //only for test of the endphase

 		 }//end of if isnear		
		}//end of isready

	}//end of for



}//end of Spoustec


void Spoustec1(int alternativa){			/////////////    VC JARAI ATTACK
	c_Vector3 spoustec1pos;
	c_Vector3 playerpos;
	c_Vector3 utokpos1;
	c_Vector3 utokpos2;
	c_Vector3 utokpos3;
	c_Vector3 utokpos4;
	dword i,j;
	float distance;
	s_SC_MP_EnumPlayers		enum_pl[64];

	j=64;
	SC_GetDummyPos("ATTACK1", &utokpos1);
	SC_GetDummyPos("ATTACK2", &utokpos2);
	SC_GetDummyPos("ATTACK3", &utokpos3);
	SC_GetDummyPos("ATTACK4", &utokpos4);
	SC_GetDummyPos("SPOUSTEC1", &spoustec1pos);
	if (!SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i=0; i<j; i++){    //0-64
		if (SC_P_IsReady(enum_pl[i].id)&&(enum_pl[i].side==0)){   
		 //if (!enum_pl[i].group_id==1) return;
		 SC_P_GetPos(enum_pl[i].id,&playerpos);
				
		 if (SC_IsNear2D( &playerpos, &spoustec1pos, 10.0f )){
			
			
			/////////////////////
			/////////////////////
			/////////////////////

			SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,5,1), &utokpos1);
			SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,5,2), &utokpos2);
			SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,5,3), &utokpos3);
			SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,5,4), &utokpos4);
			SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,6,1), &utokpos1);
			SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,6,2), &utokpos2);
			SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,6,3), &utokpos3);
			SC_P_Ai_Go(SC_P_GetBySideGroupMember(1,6,4), &utokpos4);

			if (EXPLORE_MODE==TRUE) Explore_gamemode();  //EXPLORE GAME MODE = VC CANNOT SHOOT			
			/////////////////////
			/////////////////////
			/////////////////////

			gPhase = GPHASE_GAME2;
			
			

 		 }//end of if isnear		
		}//end of isready

	}//end of for



}//end of Spoustec1




void Spoustec2(int alternativa){			/////////////    zatim prazdne
	c_Vector3 spoustec2pos;
	c_Vector3 spoustec2Apos;  //2nd alternative
	c_Vector3 playerpos;

	dword i,j;
	float distance;
	s_SC_MP_EnumPlayers		enum_pl[64];

	j=64;

	SC_GetDummyPos("SPOUSTEC2", &spoustec2pos);
	SC_GetDummyPos("SPOUSTEC2A", &spoustec2Apos);
	if (!SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i=0; i<j; i++){    //0-64
		if (SC_P_IsReady(enum_pl[i].id)&&(enum_pl[i].side==0)){   
		 //if (!enum_pl[i].group_id==1) return;
		 SC_P_GetPos(enum_pl[i].id,&playerpos);
				
		 if (SC_IsNear2D( &playerpos, &spoustec2pos, 10.0f )){
			
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			//Obsluha spoustece//
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////

			Presuny2(alternativa+1);
			if (EXPLORE_MODE==TRUE) Explore_gamemode();  //EXPLORE GAME MODE = VC CANNOT SHOOT
			/////////////////////
			/////////////////////
			/////////////////////

			gPhase = GPHASE_GAME3;

 		 }//end of if isnear	

		 if (SC_IsNear2D( &playerpos, &spoustec2Apos, 8.0f )){
			
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			//Obsluha spoustece//
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////

			Presuny2(alternativa+20);
			if (EXPLORE_MODE==TRUE) Explore_gamemode();  //EXPLORE GAME MODE = VC CANNOT SHOOT
			/////////////////////
			/////////////////////
			/////////////////////

			gPhase = GPHASE_GAME3;

 		 }//end of if isnear	
		}//end of isready

	}//end of for



}//end of Spoustec2



void Spoustec3(int alternativa){			/////////////    zatim prazdne
	c_Vector3 spoustec3pos;
	c_Vector3 playerpos;

	dword i,j;
	float distance;
	s_SC_MP_EnumPlayers		enum_pl[64];

	j=64;

	SC_GetDummyPos("SPOUSTEC3", &spoustec3pos);
	if (!SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i=0; i<j; i++){    //0-64
		if (SC_P_IsReady(enum_pl[i].id)&&(enum_pl[i].side==0)){   
		 //if (!enum_pl[i].group_id==1) return;
		 SC_P_GetPos(enum_pl[i].id,&playerpos);
				
		 if (SC_IsNear2D( &playerpos, &spoustec3pos, 10.0f )){
			
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			//Obsluha spoustece//
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////

			Presuny3(alternativa+2);
			if (EXPLORE_MODE==TRUE) Explore_gamemode();  //EXPLORE GAME MODE = VC CANNOT SHOOT
			/////////////////////
			/////////////////////
			/////////////////////

			gPhase = GPHASE_GAME4;

 		 }//end of if isnear		
		}//end of isready

	}//end of for



}//end of Spoustec3


void Spoustec4(int alternativa){			/////////////    zatim prazdne
	c_Vector3 spoustec4pos;
	c_Vector3 playerpos;

	dword i,j;
	float distance;
	s_SC_MP_EnumPlayers		enum_pl[64];

	j=64;

	SC_GetDummyPos("SPOUSTEC4", &spoustec4pos);
	if (!SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i=0; i<j; i++){    //0-64
		if (SC_P_IsReady(enum_pl[i].id)&&(enum_pl[i].side==0)){   
		 //if (!enum_pl[i].group_id==1) return;
		 SC_P_GetPos(enum_pl[i].id,&playerpos);
				
		 if (SC_IsNear2D( &playerpos, &spoustec4pos, 10.0f )){
			
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			//Obsluha spoustece//
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////

			Presuny4(alternativa+3);
			if (EXPLORE_MODE==TRUE) Explore_gamemode();  //EXPLORE GAME MODE = VC CANNOT SHOOT
			/////////////////////
			/////////////////////
			/////////////////////

			gPhase = GPHASE_GAME5;

 		 }//end of if isnear		
		}//end of isready

	}//end of for



}//end of Spoustec4


void Spoustec5(int alternativa){			/////////////    zatim prazdne
	c_Vector3 spoustec5pos;
	c_Vector3 playerpos;
	c_Vector3 pilot1pos;
	c_Vector3 pilot2pos;

	dword i,j;
	float distance;
	s_SC_MP_EnumPlayers		enum_pl[64];

	j=64;

	SC_GetDummyPos("SPOUSTEC5", &spoustec5pos);
	if (!SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i=0; i<j; i++){    //0-64
		if (SC_P_IsReady(enum_pl[i].id)&&(enum_pl[i].side==0)){   
		 //if (!enum_pl[i].group_id==1) return;
		 SC_P_GetPos(enum_pl[i].id,&playerpos);
				
		 if (SC_IsNear2D( &playerpos, &spoustec5pos, 10.0f )){
			
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			//Obsluha spoustece//
			/////////////////////
			/////////////////////
			/////////////////////
			SC_GetDummyPos("PILOT1", &pilot1pos);
			SC_GetDummyPos("PILOT2", &pilot2pos);
			SC_P_Ai_Go(SC_P_GetBySideGroupMember(0,2,1), &pilot1pos);
			SC_P_Ai_Go(SC_P_GetBySideGroupMember(0,2,2), &pilot2pos);

			Presuny5(alternativa+4);
			if (EXPLORE_MODE==TRUE) Explore_gamemode();  //EXPLORE GAME MODE = VC CANNOT SHOOT
			/////////////////////
			/////////////////////
			/////////////////////

			gPhase = GPHASE_GAME6;

 		 }//end of if isnear		
		}//end of isready

	}//end of for



}//end of Spoustec5


void Spoustec6(int alternativa){			/////////////    zatim prazdne
	c_Vector3 spoustec6pos;
	c_Vector3 playerpos;






	dword i,j;
	float distance;
	s_SC_MP_EnumPlayers		enum_pl[64];




	j=64;

	SC_GetDummyPos("SPOUSTEC6", &spoustec6pos);
	if (!SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i=0; i<j; i++){    //0-64
		if (SC_P_IsReady(enum_pl[i].id)&&(enum_pl[i].side==0)){   
		 //if (!enum_pl[i].group_id==1) return;
		 SC_P_GetPos(enum_pl[i].id,&playerpos);
				
		 if (SC_IsNear2D( &playerpos, &spoustec6pos, 10.0f )){
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			//Obsluha spoustece//
			/////////////////////
			/////////////////////
			/////////////////////
			if (EXPLORE_MODE==TRUE) Explore_gamemode();  //EXPLORE GAME MODE = VC CANNOT SHOOT
			/////////////////////
			/////////////////////
			/////////////////////

			gPhase = GPHASE_GAME7;

 		 }//end of if isnear		
		}//end of isready

	}//end of for



}//end of Spoustec6

void Spoustec7(int alternativa){			/////////////    zatim prazdne
	c_Vector3 spoustec7pos;
	c_Vector3 playerpos;






	dword i,j;
	float distance;
	s_SC_MP_EnumPlayers		enum_pl[64];




	j=64;

	SC_GetDummyPos("SPOUSTEC7", &spoustec7pos);
	if (!SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)) return;

	for (i=0; i<j; i++){    //0-64
		if (SC_P_IsReady(enum_pl[i].id)&&(enum_pl[i].side==0)){   
		 //if (!enum_pl[i].group_id==1) return;
		 SC_P_GetPos(enum_pl[i].id,&playerpos);
				
		 if (SC_IsNear2D( &playerpos, &spoustec7pos, 8.0f )){
			/////////////////////
			/////////////////////
			/////////////////////
			/////////////////////
			//Obsluha spoustece//
			/////////////////////
			/////////////////////
			/////////////////////
			if (EXPLORE_MODE==TRUE) Explore_gamemode();  //EXPLORE GAME MODE = VC CANNOT SHOOT
			/////////////////////
			/////////////////////
			/////////////////////

			gPhase = GPHASE_DONE;

 		 }//end of if isnear		
		}//end of isready

	}//end of for



}//end of Spoustec7

int ScriptMain(s_SC_NET_info *info)
{
	s_SC_MP_EnumPlayers		enum_pl[64];
	s_SC_MP_SRV_settings	SRVset;
	c_Vector3 rcpos,pcpos;
	s_SC_MP_Recover *precov;
	s_SC_MP_hud		hudinfo;
	s_SC_P_getinfo	plinfo;
	//void *nod;
	c_Vector3 vec;
	dword	i, j, sideA, sideB, num;
	BOOL	valid[2];
	BOOL	alldeath;
	BOOL 	prevtickalldeath;
	BOOL	radiomanstat = FALSE;
	BOOL 	teamdead = FALSE;
	BOOL hrac_i  = FALSE;
	BOOL hracvehre = FALSE;
	BOOL asponjeden;
	BOOL vcstat;
	BOOL vcstatpom;
	BOOL presunuto = FALSE;
	BOOL 	posilyaktiv;
	//BOOL REC_presunVC = FALSE;
	char	txt[32],*itxt;
	ushort *witxt;
	float	val;
	c_Vector3	plPos;
	c_Vector3	teleportpos;

	dword 	aktivace = 0;
	dword	pocetzivychUScelkove;
	dword	pocetzivychVCcelkove;
	dword	pocetUScelkove;
	dword	pocetVCcelkove;
	dword	pocetzivychUSAI;
	dword	pocetzivychVCAI;
	dword   zpozdeni;
	dword 	zpozdeni2;

	dword zpozdeni_hlidek;

	int 	alternativa; //alternativa respawn mista - generovana nahodne 


	BOOL aktivator1, aktivator2, aktivator3;

	//
	switch(info->message)
	{
		case SC_NET_MES_SERVER_TICK:	
			
			if (SRV_CheckEndRule(info->elapsed_time)) break;

			for (j=0;j<2;j++)
			for (i=0;i<gRecs[j];i++)    //gRecs
				gRecTimer[j][i] -= info->elapsed_time;


			if (gRecoverTime<0xffff){
				gNextRecover -= info->elapsed_time;
				if (gNextRecover<0.0f) gNextRecover = (float)gRecoverTime;
			}// if (gRecoverTime<0xffff)
			

		
			if (gAllNoAiRecover>0.0f){
				gAllNoAiRecover -= info->elapsed_time;				
				if (gAllNoAiRecover<=0.0f)
					SC_MP_RecoverAllNoAiPlayers();		
								
				break;
			}// if (gAllNoAiRecover>0.0f)
			else{
				gAllNoAiRecover -= info->elapsed_time;
			}


			CLEAR(valid);			
			j = 64;
			alldeath = FALSE;

			if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)){				

				alldeath = TRUE;
				pocetzivychUScelkove = 0;
				pocetzivychVCcelkove = 0;
				pocetUScelkove = 0;
				pocetVCcelkove = 0;
				pocetzivychUSAI = Spocti_US_AI();
				pocetzivychVCAI = Spocti_VC_AI();

				
				for (i=0;i<j;i++){
					if (enum_pl[i].status==SC_MP_P_STATUS_INGAME){
						if (enum_pl[i].side>1) SC_message("coop script wrong side: %d",enum_pl[i].side);
						else{
							valid[enum_pl[i].side] = TRUE;
						}
					}

					if ((enum_pl[i].side==0)&&(enum_pl[i].status==SC_MP_P_STATUS_INGAME)){
						alldeath = FALSE;
						pocetzivychUScelkove++;
					}

					if ((enum_pl[i].side==1)&&(enum_pl[i].status==SC_MP_P_STATUS_INGAME)){
						alldeath = FALSE;
						pocetzivychVCcelkove++;
					}


					if   ((enum_pl[i].side==0)
					   &&((enum_pl[i].status==SC_MP_P_STATUS_INGAMEDEATH)
				           ||(enum_pl[i].status==SC_MP_P_STATUS_INGAME))){
						alldeath = FALSE;
						pocetUScelkove++;
					}

					if   ((enum_pl[i].side==1)
					   &&((enum_pl[i].status==SC_MP_P_STATUS_INGAMEDEATH)
					   ||(enum_pl[i].status==SC_MP_P_STATUS_INGAME))){
						alldeath = FALSE;
						pocetVCcelkove++;
					}

				}// for (i)

				SC_Log(3,"Enum, v[0]: %d   v[1]: %d  alldeath: %d",valid[0],valid[1],alldeath);
					
			}// if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL))
			else SC_Log(3,"NoEnum");

			

			if ((pocetzivychUScelkove == pocetzivychUSAI)
			   &&(prevtickalldeath == TRUE)) {
				alldeath = TRUE;
				prevtickalldeath = FALSE;
			}
			
			if (pocetzivychUScelkove == pocetzivychUSAI) prevtickalldeath = TRUE;
			if (pocetUScelkove == REC_USAI) prevtickalldeath = FALSE;
			



			if (((gPhase==GPHASE_GAME)
				||(gPhase==GPHASE_GAME1)
				||(gPhase==GPHASE_GAME2)
				||(gPhase==GPHASE_GAME3)
				||(gPhase==GPHASE_GAME4)
				||(gPhase==GPHASE_GAME5)
				||(gPhase==GPHASE_GAME6)
				||(gPhase==GPHASE_GAME7))&&(alldeath)&&(gPhase_timer<0.0f)){
				
				if (gRecoverLimit==0){
					// mission failed
					SC_Log(2,"Set GPHASE_FAILED");
					gPhase = GPHASE_FAILED;
					gPhase_timer = 5.0f;
				}
				else {
					// recover unlimited
					if ((gRecoverTime>=0xffff)&&(gAllNoAiRecover<-5.0f)){
						gAllNoAiRecover = 4.0f;					
					}
				}

			}// if ((alldeath)&&(gRecoverTime>=0xffff))
			else gAllNoAiRecover = 0.0f;


			gValidSide0 = valid[0];






			switch(gPhase){
				case GPHASE_BEGIN:

					gPhase_timer -= info->elapsed_time;
					


					//if (presunuto == FALSE){
					//	Presuny(alternativa);  //random VC respawn
					//	presunuto = TRUE;
					//}



					//SC_sgi(SGI_CHOPPER,1);   //poc.podm.vrtulniku  1=stay, 2=fly
					//SC_sgi(SGI_CHOPPERPULASKI,2);

					asponjeden = FALSE;
					hracvehre = FALSE;
					prevtickalldeath = FALSE;
				
					

					if (gPhase_timer<0.0f)
					if ((valid[0])&&(valid[1])){
						SC_Log(2,"Set GPHASE_GAME");
						gPhase_timer = 5.0f;
						gPhase = GPHASE_GAME;						
					}



					break;
				case GPHASE_GAME:
					

					gPhase_timer -= info->elapsed_time;

					if (gPhase_timer<0.0f)   ////////////////// disable MISSION DONE if all VC KIA
					if (!valid[1]){
						SC_Log(2,"Set GPHASE_DONE");
						gPhase = GPHASE_DONE;
						gPhase_timer = 10.0f;
					}// if (!valid[1])

//////////////////////////////////// ovladani botu - specialni funkce

					

					Spoustec0(alternativa);////////HUEY START////doresit////
					

					//HiddenVC(1, 1, 1, 6.0f);
					//HiddenVC(1, 2, 1, 6.0f);
					//HiddenVC(1, 3, 1, 6.0f);
					//HiddenVC(1, 4, 1, 12.0f);
					VesnicaniJarai(0, 1, 1, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 2, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 3, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 4, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 5, 4.0f, ENABLE_MOVING);
					Burn_Sphere();

					SC_ggi(GVAR_GPHASE); //checking huey script status

					break;

				case GPHASE_GAME1:
					gPhase_timer -= info->elapsed_time;

					if (gPhase_timer<0.0f)
					if (!valid[1]){
						SC_Log(2,"Set GPHASE_DONE");
						gPhase = GPHASE_DONE;
						gPhase_timer = 10.0f;
					}// if (!valid[1])

					
					Spoustec1(alternativa);////////JARAI ATTACK//////////////////

					HiddenVC(1, 1, 1, 6.0f);
					HiddenVC(1, 2, 1, 6.0f);
					//HiddenVC(1, 3, 1, 6.0f);
					//HiddenVC(1, 4, 1, 12.0f);
					VesnicaniJarai(0, 1, 1, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 2, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 3, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 4, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 5, 4.0f, ENABLE_MOVING);
					Burn_Sphere();

					break;

				case GPHASE_GAME2:
					gPhase_timer -= info->elapsed_time;

					if (gPhase_timer<0.0f)
					if (!valid[1]){
						SC_Log(2,"Set GPHASE_DONE");
						gPhase = GPHASE_DONE;
						gPhase_timer = 10.0f;
					}// if (!valid[1])
			
					Spoustec2(alternativa);	
					

					
					//////////////////////////////////////////////
					//////////////////////////////////////////////
					HiddenVC(1, 1, 1, 6.0f);
					HiddenVC(1, 2, 1, 6.0f);
					HiddenVC(1, 3, 1, 6.0f);  //dva VC u mostu
					HiddenVC(1, 4, 1, 12.0f);
					VesnicaniJarai(0, 1, 1, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 2, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 3, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 4, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 5, 4.0f, ENABLE_MOVING);
					Burn_Sphere();
					//////////////////////////////////////////////
					//////////////////////////////////////////////

					break;

				case GPHASE_GAME3:
					gPhase_timer -= info->elapsed_time;

					if (gPhase_timer<0.0f)
					if (!valid[1]){
						SC_Log(2,"Set GPHASE_DONE");
						gPhase = GPHASE_DONE;
						gPhase_timer = 10.0f;
					}// if (!valid[1])
			
					Spoustec3(alternativa);					

					HiddenVC(1, 1, 1, 6.0f);
					HiddenVC(1, 2, 1, 6.0f);
					HiddenVC(1, 3, 1, 6.0f);  
					HiddenVC(1, 4, 1, 12.0f);
					VesnicaniJarai(0, 1, 1, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 2, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 3, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 4, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 5, 4.0f, ENABLE_MOVING);
					Burn_Sphere();

					break;

				case GPHASE_GAME4:
					gPhase_timer -= info->elapsed_time;

					if (gPhase_timer<0.0f)
					if (!valid[1]){
						SC_Log(2,"Set GPHASE_DONE");
						gPhase = GPHASE_DONE;
						gPhase_timer = 10.0f;
					}// if (!valid[1])
			
					Spoustec4(alternativa);					


					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					HiddenVC(1, 1, 1, 6.0f);
					HiddenVC(1, 2, 1, 6.0f);
					HiddenVC(1, 3, 1, 6.0f);  
					HiddenVC(1, 4, 1, 6.0f);
					VesnicaniJarai(0, 1, 1, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 2, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 3, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 4, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 5, 4.0f, ENABLE_MOVING);
					Burn_Sphere();				

					break;

				case GPHASE_GAME5:
					gPhase_timer -= info->elapsed_time;

					if (gPhase_timer<0.0f)
					if (!valid[1]){
						SC_Log(2,"Set GPHASE_DONE");
						gPhase = GPHASE_DONE;
						gPhase_timer = 10.0f;
					}// if (!valid[1])
			
					Spoustec5(alternativa);					


					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					HiddenVC(1, 1, 1, 6.0f);
					HiddenVC(1, 2, 1, 6.0f);
					HiddenVC(1, 3, 1, 6.0f); 
					HiddenVC(1, 4, 1, 6.0f);
					VesnicaniJarai(0, 1, 1, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 2, 4.0f, DISABLE_MOVING);
					VesnicaniJarai(0, 1, 3, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 4, 4.0f, ENABLE_MOVING);	
					VesnicaniJarai(0, 1, 5, 4.0f, ENABLE_MOVING);				
					Burn_Sphere();
					break;


				case GPHASE_GAME6:
					gPhase_timer -= info->elapsed_time;

					if (gPhase_timer<0.0f)
					if (!valid[1]){
						SC_Log(2,"Set GPHASE_DONE");
						gPhase = GPHASE_DONE;
						gPhase_timer = 10.0f;
					}// if (!valid[1])
			
					Spoustec6(alternativa);					


					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					/////////SPECIAL//FUNCTIONS///////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					HiddenVC(1, 1, 1, 6.0f);
					HiddenVC(1, 2, 1, 6.0f);
					HiddenVC(1, 3, 1, 6.0f);  
					HiddenVC(1, 4, 1, 6.0f);
					VesnicaniJarai(0, 1, 1, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 2, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 3, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 4, 4.0f, ENABLE_MOVING);	
					VesnicaniJarai(0, 1, 5, 4.0f, ENABLE_MOVING);				
					Burn_Sphere();
					break;

				case GPHASE_GAME7:
					gPhase_timer -= info->elapsed_time;

					if (gPhase_timer<0.0f)
					if (!valid[1]){
						SC_Log(2,"Set GPHASE_DONE");
						gPhase = GPHASE_DONE;
						gPhase_timer = 10.0f;
					}// if (!valid[1])
			
					Spoustec7(alternativa);  //handled by  heliscript					


					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					/////////SPECIAL//FUNCTIONS///////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					//////////////////////////////////
					HiddenVC(1, 1, 1, 6.0f);
					HiddenVC(1, 2, 1, 6.0f);
					HiddenVC(1, 3, 1, 6.0f);  
					HiddenVC(1, 4, 1, 6.0f);
					VesnicaniJarai(0, 1, 1, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 2, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 3, 4.0f, ENABLE_MOVING);
					VesnicaniJarai(0, 1, 4, 4.0f, ENABLE_MOVING);	
					VesnicaniJarai(0, 1, 5, 4.0f, ENABLE_MOVING);				
					Burn_Sphere();

					//SC_ggi(GVAR_GPHASE); //checking huey script status					

					break;


				case GPHASE_DONE:
					gPhase_timer -= info->elapsed_time;


					

					prevtickalldeath = FALSE;
					if (gPhase_timer<0.0f){

						SC_Log(2,"SC_MP_RestartMission");
						SC_MP_RestartMission();					//restart
						gPhase = GPHASE_BEGIN;
						gPhase_timer = 10.0f; 
					}
					

					


					break;



				case GPHASE_FAILED:

					gPhase_timer -= info->elapsed_time;

					
					prevtickalldeath = FALSE;
					

					if (gPhase_timer<0.0f){

						SC_Log(2,"SC_MP_RestartMission");
						SC_MP_RestartMission();					//restart
						gPhase = GPHASE_BEGIN;
						gPhase_timer = 20.0f;
					}
					
					break;
			}// switch(gPhase)

			SRV_CheckUpdate();

			break;

		case SC_NET_MES_CLIENT_TICK:

			if (SC_P_IsReady(SC_PC_Get())) {
				SC_PC_EnableFlashLight(TRUE); 
				Hide_Handmap();
				Dizejbluj_VC();
				//Burn_Sphere2(); not working on client
			}

			break;// SC_NET_MES_CLIENT_TICK


		case SC_NET_MES_LEVELPREINIT:

			SC_sgi(GVAR_MP_MISSIONTYPE,GVAR_MP_MISSIONTYPE_COOP);
			//SC_sgi(GVAR_MP_MISSIONTYPE,GVAR_MP_MISSIONTYPE_ATG);

			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;

			SC_MP_EnableBotsFromScene(TRUE);

			break;// SC_NET_MES_LEVELPREINIT

		case SC_NET_MES_LEVELINIT:

			//SC_MP_Gvar_SetSynchro(SGI_CHOPPER);  ////////////////?????????????????///////////////
			//SC_MP_Gvar_SetSynchro(SGI_CHOPPERPULASKI);
			//SC_MP_Gvar_SetSynchro(SGI_CHOPPERRESTART);	

			//SC_sgi(SGI_CHOPPERRESTART,1);
			//SC_sgi(SGI_CHOPPERPULASKIRESTART,1);	
			//SC_sgi(SGI_CHOPPER,0);  //vsechno jen pomoci chopper, kvuli trafficu	

			//////////////REAL////////////
		       if (GAME_MODE==REAL_MODE) {

			SC_MP_SRV_SetForceSide(0xffffffff);
			SC_MP_SetChooseValidSides(3); 

			


			// Enable soldiers and disable DM classes
			SC_MP_SRV_SetClassLimit(1, 12); // US Soldier
			SC_MP_SRV_SetClassLimit(3,0); //sniper			
			SC_MP_SRV_SetClassLimit(18,0); //pilot?
			SC_MP_SRV_SetClassLimit(19, 0); // US DM

			SC_MP_SRV_SetClassLimit(39, 0); // VC DM
			SC_MP_SRV_SetClassLimit(21, 2); // VC Soldier  2x
			SC_MP_SRV_SetClassLimit(22, 0); 
			SC_MP_SRV_SetClassLimit(23, 0);
			SC_MP_SRV_SetClassLimit(24, 0);
			SC_MP_SRV_SetClassLimit(25, 0);
			SC_MP_SRV_SetClassLimit(26, 0);


			CLEAR(hudinfo);
			hudinfo.title = 1098;

			hudinfo.sort_by[0] = SC_HUD_MP_SORTBY_KILLS;
			hudinfo.sort_by[1] = SC_HUD_MP_SORTBY_DEATHS | SC_HUD_MP_SORT_DOWNUP;
			hudinfo.sort_by[2] = SC_HUD_MP_SORTBY_PINGS | SC_HUD_MP_SORT_DOWNUP;

			hudinfo.pl_mask = SC_HUD_MP_PL_MASK_CLASS; 
					//SC_HUD_MP_PL_MASK_KILLS | SC_HUD_MP_PL_MASK_DEATHS | SC_HUD_MP_PL_MASK_CLASS;
			hudinfo.use_sides = TRUE;
			hudinfo.side_name[0] = 1010;
			hudinfo.side_color[0] = 0x440000ff;
			hudinfo.side_name[1] = 1011;
			hudinfo.side_color[1] = 0x4400ff00;

			hudinfo.disableVCside = FALSE; //TRUE
			hudinfo.disableUSside = FALSE;  //smazat cely radek

			hudinfo.side_mask = SC_HUD_MP_SIDE_MASK_FRAGS;
			

			SC_MP_HUD_SetTabInfo(&hudinfo);

			SC_MP_AllowStPwD(TRUE);
			SC_MP_AllowFriendlyFireOFF(TRUE);
			SC_MP_SetItemsNoDisappear(TRUE);
			SC_MP_EnableC4weapon(TRUE);

			
 
 
		       }//end of real mode
			
		       else { //////////COOP////////
		       //if (GAME_MODE==COOP_MODE) {
			  

			SC_MP_SRV_SetForceSide(0);


			SC_MP_SRV_SetClassLimit(18,0);
			SC_MP_SRV_SetClassLimit(19,0);
			SC_MP_SRV_SetClassLimit(39,0);

			SC_MP_GetSRVsettings(&SRVset);

			for (i=0;i<6;i++){
				SC_MP_SRV_SetClassLimit(i+1,SRVset.atg_class_limit[i]);
				SC_MP_SRV_SetClassLimit(i+21,SRVset.atg_class_limit[i]);
			}// for (i)


			CLEAR(hudinfo);
			hudinfo.title = 1098;

			hudinfo.sort_by[0] = SC_HUD_MP_SORTBY_KILLS;
			hudinfo.sort_by[1] = SC_HUD_MP_SORTBY_DEATHS | SC_HUD_MP_SORT_DOWNUP;
			hudinfo.sort_by[2] = SC_HUD_MP_SORTBY_PINGS | SC_HUD_MP_SORT_DOWNUP;

			hudinfo.pl_mask = SC_HUD_MP_PL_MASK_KILLS | SC_HUD_MP_PL_MASK_DEATHS | SC_HUD_MP_PL_MASK_CLASS;
			hudinfo.use_sides = TRUE;
			hudinfo.side_name[0] = 1010;
			hudinfo.side_color[0] = 0x440000ff;
			hudinfo.side_name[1] = 1011;
			hudinfo.side_color[1] = 0x44ff0000;
			hudinfo.disableVCside = TRUE;

			hudinfo.side_mask = SC_HUD_MP_SIDE_MASK_FRAGS;
			

			SC_MP_HUD_SetTabInfo(&hudinfo);

			SC_MP_AllowStPwD(TRUE);
			SC_MP_AllowFriendlyFireOFF(TRUE);
			SC_MP_SetItemsNoDisappear(TRUE);
			SC_MP_EnableC4weapon(TRUE);

			SC_MP_SetChooseValidSides(1);


		       }//end of coop mode




			








			alternativa = SRV_Random(REC_MAX_ALTERNATIVES);

			//SC_MP_SetChooseValidSides(1);

			if (info->param2){

				if (info->param1){
					// it's server		

					SC_MP_GetSRVsettings(&SRVset);
					gRecoverTime = SRVset.coop_respawn_time;
					//gRecoverLimit = SRVset.coop_respawn_limit;
					gRecoverLimit = 0;

					SC_MP_SRV_InitWeaponsRecovery(600.0f);    //10 minut to weapons respawn                                 //1.0f
					
					SC_MP_Gvar_SetSynchro(GVAR_GPHASE);					
					
					CLEAR(gRecs);

					for (i=100*alternativa;i<(REC_MAX+100*alternativa);i++){		
						sprintf(txt,REC_WPNAME_US,i);			
						if (SC_NET_FillRecover(&gRec[0][gRecs[0]],txt)) gRecs[0]++;					
					}					

#if _GE_VERSION_ >= 133
					i = REC_MAX - gRecs[0];
					SC_MP_GetRecovers(SC_MP_RESPAWN_ATG_US,&gRec[0][gRecs[0]],&i);
					gRecs[0] += i;
#endif

					SC_Log(3,"ATG UsBomb respawns us: %d",gRecs[0]);


					if (gRecs[0]==0) SC_message("no US recover place defined!");

					for (i=0+100*alternativa;i<(REC_MAX+100*alternativa);i++){		
						sprintf(txt,REC_WPNAME_VC,i);			
						if (SC_NET_FillRecover(&gRec[1][gRecs[1]],txt)) gRecs[1]++;
					}					

#if _GE_VERSION_ >= 133
					i = REC_MAX - gRecs[1];
					SC_MP_GetRecovers(SC_MP_RESPAWN_ATG_VC,&gRec[1][gRecs[1]],&i);
					gRecs[1] += i;
#endif

					SC_Log(3,"ATG UsBomb respawns vc: %d",gRecs[0]);


					if (gRecs[1]==0) SC_message("no VC recover place defined!");	

					CLEAR(gRecTimer);

				}// if (info->param1)
			}//if (info->param2)

			if (info->param1)
			{
				//!!! ++ Reinit AI - NEW
				num = 64;
				SC_MP_EnumPlayers(enum_pl, &num, SC_P_SIDE_VC);
				for (i = 0; i < num; i++)
				{
					SC_P_ScriptMessage(enum_pl[i].id, SCM_MP_REINIT, 0);
				}
				//-- Reinit AI - NEW

			}
			break;// SC_NET_MES_LEVELINIT


		case SC_NET_MES_RENDERHUD:

			switch(SC_ggi(GVAR_GPHASE)){

				case GPHASE_DONE:
					j = 1099;
					break;
				case GPHASE_FAILED:
					j = 1049;
					break;

				default:j = 0;break;

			}// switch(SC_ggi(GVAR_GPHASE))

			if (j){
							
				witxt = SC_Wtxt(j);
				SC_GetScreenRes(&val,NULL);

				val -= SC_Fnt_GetWidthW(witxt,1); 

				SC_Fnt_WriteW(val * 0.5f,15,witxt,1,0xffffffff);

			}// if (j)


			break;

		case SC_NET_MES_SERVER_RECOVER_TIME:

			if (info->param2){
					info->fval1 = 0.1f;
			}
			else{
				// killed

				SC_P_GetInfo(info->param1,&plinfo);	
								
				if (plinfo.side==0){					

					if (gRecoverLimit>0){
						
						if (gRecoverTime>=0xffff) info->fval1 = -1.0f;
						else
						if (gRecoverTime>0) info->fval1 = gNextRecover;
							else info->fval1 = 4.0f;						
					}
					else info->fval1 = -1.0f;
								
				}
				else info->fval1 = -1.0f;
				
			}

			break;


		case SC_NET_MES_SERVER_RECOVER_PLACE:
			
			precov = (s_SC_MP_Recover*)info->param2;

			i = SC_MP_SRV_GetBestDMrecov(gRec[info->param1],gRecs[info->param1],gRecTimer[info->param1],NORECOV_TIME);
			
			gRecTimer[info->param1][i] = NORECOV_TIME;
			*precov = gRec[info->param1][i];
						
			break;
			

		case SC_NET_MES_SERVER_KILL:


			break;// SC_NET_MES_SERVER_KILL


		case SC_NET_MES_RESTARTMAP:


			CLEAR(gRecTimer);

			gNextRecover = 0.0f;

			gTime = 0;

			gPhase = GPHASE_BEGIN;
			gPhase_timer = 5.0f; //5
			gPhase_send = 0;

			gValidSide0 = FALSE;

			SC_MP_GetSRVsettings(&SRVset);
			gRecoverTime = SRVset.coop_respawn_time;
			//gRecoverLimit = SRVset.coop_respawn_limit;
			gRecoverLimit = 0;

			gAllNoAiRecover  = 0.0f;
					

			SC_MP_SRV_ClearPlsStats();

			SC_MP_SRV_InitGameAfterInactive();
			SC_MP_RecoverAllAiPlayers();
			SC_MP_RecoverAllNoAiPlayers();
			
			//SC_sgi(SGI_CHOPPERRESTART,1);
			//SC_sgi(SGI_CHOPPERPULASKIRESTART,1);
			//SC_sgi(SGI_CHOPPER,0);  //vsechno jen pomoci chopper, kvuli trafficu
			
			prevtickalldeath = FALSE;




			break;// SC_NET_MES_RESTARTMAP

		case SC_NET_MES_RULESCHANGED:

			
			gEndRule = info->param1;
			gEndValue = info->param2;
			gTime = 0.0f;
			break;
			

					
	}// switch(info->message)
	

	return 1;

}// int ScriptMain(void)
