/*
useful macros and functions for scripting;

*/

#ifndef SC_LIBRARY_H
#define SC_LIBRARY_H 

#include <inc\sc_global.h>
#include <inc\sc_def.h>

#define DT(debugtext) {SC_Log(3,debugtext);SC_Osi(debugtext);}

#define nextex(time) info->next_exe_time=time

#define isdead(idside, idgroup, idmember) \
	!SC_P_IsReady(SC_P_GetBySideGroupMember(idside,idgroup,idmember))

#define GetVC(gr,mid) SC_P_GetBySideGroupMember(1,gr,mid)

#define GetUS(mid) SC_P_GetBySideGroupMember(0,0,mid)
#define GetUS2(gr,mid) SC_P_GetBySideGroupMember(0,gr,mid)

#define GetGunner SC_P_GetBySideGroupMember(0,0,SC_P_MEMBERID_MACHINEGUN)
#define GetRadist SC_P_GetBySideGroupMember(0,0,SC_P_MEMBERID_RADIO)
#define GetMedic SC_P_GetBySideGroupMember(0,0,SC_P_MEMBERID_MEDIC)
#define GetPoint SC_P_GetBySideGroupMember(0,0,SC_P_MEMBERID_POINT)
#define GetDemo SC_P_GetBySideGroupMember(0,0,SC_P_MEMBERID_DEMOLITION)


#define PCSay(what) {SC_P_Speech2(SC_PC_Get(),what,&time);time+=0.1f;}
#define PCSayM(what,mes) {SC_P_SpeechMes2(SC_PC_Get(),what,&time,mes);time+=0.1f;}
#define Radist(what) {SC_P_Speech2(GetUS(SC_P_MEMBERID_RADIO),what,&time);time+=0.1f;}
#define RadistM(what,mes) {SC_P_SpeechMes2(GetUS(SC_P_MEMBERID_RADIO),what,&time,mes);time+=0.1f;}
#define Point(what) {SC_P_Speech2(GetUS(SC_P_MEMBERID_POINT),what,&time);time+=0.1f;}
#define PointM(what,mes) {SC_P_SpeechMes2(GetUS(SC_P_MEMBERID_POINT),what,&time,mes);time+=0.1f;}
#define Medic(what) {SC_P_Speech2(GetUS(SC_P_MEMBERID_MEDIC),what,&time);time+=0.1f;}
#define MedicM(what,mes) {SC_P_SpeechMes2(GetUS(SC_P_MEMBERID_MEDIC),what,&time,mes);time+=0.1f;}
#define Gunner(what) {SC_P_Speech2(GetUS(SC_P_MEMBERID_MACHINEGUN),what,&time);time+=0.1f;}
#define GunnerM(what,mes) {SC_P_SpeechMes2(GetUS(SC_P_MEMBERID_MACHINEGUN),what,&time,mes);time+=0.1f;}
#define Demoman(what) {SC_P_Speech2(GetUS(SC_P_MEMBERID_DEMOLITION),what,&time);time+=0.1f;}
#define DemomanM(what,mes) {SC_P_SpeechMes2(GetUS(SC_P_MEMBERID_DEMOLITION),what,&time,mes);time+=0.1f;}

#define PCTalkTime SC_P_GetWillTalk(SC_PC_Get())
#define PointTalkTime SC_P_GetWillTalk(GetUS(SC_P_MEMBERID_POINT))
#define MedicTalkTime SC_P_GetWillTalk(GetUS(SC_P_MEMBERID_MEDIC))
#define RadistTalkTime SC_P_GetWillTalk(GetUS(SC_P_MEMBERID_RADIO))
#define GunnerTalkTime SC_P_GetWillTalk(GetUS(SC_P_MEMBERID_MACHINEGUN))
#define DemoTalkTime SC_P_GetWillTalk(GetUS(SC_P_MEMBERID_DEMOLITION))



//#define Radio(what) {SC_SpeechRadio2(what,&time);time+=0.1f;}
//#define RadioM(what,mes) {SC_SpeechRadioMes2(what,&time,mes);time+=0.1f;}

float frandom(float max){
	float x; 
	x=frnd(max); 
	if (x<0) x=-x; 
	return x;
}


#define Radio(what) {time+=frandom(0.3f); SC_SpeechRadio2(what,&time);time+=0.1f+frandom(0.2f);}
#define RadioM(what,mes) {time+=frandom(0.3f); SC_SpeechRadioMes2(what,&time,mes);time+=0.1f+frandom(0.2f);}


#define MSay(what) {SC_P_Speech2(member,what,&time);time+=0.1f;}
#define MSayM(what,mes) {SC_P_SpeechMes2(member,what,&time,mes);time+=0.1f;}
#define PSay(who, what) {SC_P_Speech2(who,what,&time);time+=0.1f;}
#define PSayM(who, what,mes) {SC_P_SpeechMes2(who,what,&time,mes);time+=0.1f;}


#define P_Run(pl_id,where) S_Mes(pl_id,SCM_RUN,where)
#define P_RunAndKill(pl_id,flags) S_Mes(pl_id,SCM_RUNANDKILL,flags)
#define P_Panicrun(pl_id) S_Mes(pl_id,SCM_PANICRUN,0)
#define P_TimedRun(pl_id,where) S_Mes(pl_id,SCM_TIMEDRUN,where)
#define P_Teleport(pl_id,where) S_Mes(pl_id,SCM_TELEPORT,where)
#define P_Retreat(pl_id) S_Mes(pl_id,SCM_RETREAT,0)
#define P_Retreat2(pl_id) S_Mes(pl_id,SCM_RETREAT,1)
#define P_Startwalk(pl_id) S_Mes(pl_id,SCM_STARTWALK,0)
#define P_Startpatrol(pl_id) S_Mes(pl_id,SCM_STARTPATROL,0)
#define P_Hunter(pl_id) S_Mes(pl_id,SCM_HUNTER,0)
#define P_RunAt(pl_id,where) S_Mes(pl_id,SCM_RUNATWP,where);
#define P_WalkAt(pl_id,where) S_Mes(pl_id,SCM_WALKATWP,where);

/*
#define P_Enable(pl_id) S_Mes(pl_id,SCM_ENABLE,0)
#define P_Disable(pl_id) S_Mes(pl_id,SCM_DISABLE,0)
*/

#define P_Remove(pl_id) SC_LevScr_Event(SCM_REMOVE,pl_id);

#define P_Crouch(pl_id) SC_P_Ai_SetMovePos(pl_id, SC_P_AI_MOVEPOS_CROUCH);
#define P_Stand(pl_id) SC_P_Ai_SetMovePos(pl_id, SC_P_AI_MOVEPOS_STAND);

#define P_CrouchRun(pl_id) SC_P_Ai_SetMovePos(pl_id, SC_P_AI_MOVEPOS_CROUCH); SC_P_Ai_SetMoveMode(pl_id, SC_P_AI_MOVEMODE_RUN)
#define P_StandRun(pl_id) SC_P_Ai_SetMovePos(pl_id, SC_P_AI_MOVEPOS_STAND); SC_P_Ai_SetMoveMode(pl_id, SC_P_AI_MOVEMODE_RUN)
#define P_StandWalk(pl_id) SC_P_Ai_SetMovePos(pl_id, SC_P_AI_MOVEPOS_STAND); SC_P_Ai_SetMoveMode(pl_id, SC_P_AI_MOVEMODE_WALK)


#define P_Battle(pl_id) SC_P_Ai_SetMode(pl_id, SC_P_AI_MODE_BATTLE);
#define P_Script(pl_id) SC_P_Ai_SetMode(pl_id, SC_P_AI_MODE_SCRIPT);

#define Pmode_Attack(pl_id) SC_P_Ai_SetBattleMode(pl_id,SC_P_AI_BATTLEMODE_ATTACK);
#define Pmode_Hold(pl_id) SC_P_Ai_SetBattleMode(pl_id,SC_P_AI_BATTLEMODE_HOLD);
#define Pmode_Retreat(pl_id) SC_P_Ai_SetBattleMode(pl_id,SC_P_AI_BATTLEMODE_RETREAT);

#define VCSenemy(group,member) SC_P_Ai_GetSureEnemies(SC_P_GetBySideGroupMember(1,group,member))
#define VCenemy(group,member) SC_P_Ai_GetEnemies(SC_P_GetBySideGroupMember(1,group,member))


#define Setalarm(val) SC_sgi(SGI_MISSIONALARM,val)

#define SetAlarm(val) SC_sgi(SGI_MISSIONALARM,val)
#define GetAlarm SC_ggi(SGI_MISSIONALARM)


#define MAXSHOOTDIST 100

#define AttackPC(pl_id) {dword amember;c_Vector3 xvec,xvec2;\
	SC_PC_GetPos(&xvec);SC_P_GetPos(pl_id,&xvec2);\
	if (SC_IsNear3D(&xvec, &xvec2, MAXSHOOTDIST)&&SC_P_Ai_KnowsAboutPl(pl_id,SC_PC_Get())&&!SC_P_Ai_GetShooting(pl_id,&amember))\
				SC_P_Ai_ShootAt(pl_id, &xvec, 1.0f);else SC_P_Ai_ShouldLookAt(pl_id,&xvec,5.0f);}

#define LookatPC(pl_id) {c_Vector3 xvec;\				
	SC_PC_GetPos(&xvec);SC_P_Ai_LookAt(pl_id,&xvec);}


void P_Enable(dword pl_id) {
	SC_P_Ai_SetMode(pl_id,SC_P_AI_MODE_BATTLE);
	SC_P_Ai_EnableShooting(pl_id, TRUE);
	SC_P_Ai_EnableSituationUpdate(pl_id,TRUE);
	SC_Log(3,"Player %d enabled",pl_id);
}

void P_Disable(dword pl_id) {
	SC_P_Ai_SetMode(pl_id,SC_P_AI_MODE_SCRIPT);
	SC_P_Ai_EnableShooting(pl_id, FALSE);
	SC_P_Ai_EnableSituationUpdate(pl_id,FALSE);
	SC_P_Ai_Stop(pl_id);
	SC_Log(3,"Player %d disabled",pl_id);
}

void S_Mes(dword pl_id, dword  what,dword what2){
	if (!pl_id) {
		SC_Log(3,"Message %d %d to unexisted player!",what, what2);
		return;
	}
	SC_P_ScriptMessage(pl_id,what,what2);
}

BOOL VCdanger(int group,int member) {
	if (VCSenemy(group,member)) return TRUE;
	if (SC_P_Ai_GetDanger(SC_P_GetBySideGroupMember(1,group,member))>0.5f) return TRUE;
	return FALSE;
}

#define P_Indanger P_InDanger
BOOL P_InDanger(dword pl_id){
	if (SC_P_Ai_GetSureEnemies(pl_id)) return TRUE;
	if (SC_P_Ai_GetDanger(pl_id)>0.5f) return TRUE;
	return FALSE;
}

BOOL P_InDanger2(dword pl_id){
	if (SC_P_Ai_GetEnemies(pl_id)) return TRUE;
	if (SC_P_Ai_GetDanger(pl_id)>0) return TRUE;
	return FALSE;
}


void P_Enablecrouch(dword pl_id, BOOL enable){
	s_SC_P_AI_props props;
	CLEAR(props);
	SC_P_Ai_GetProps(pl_id,&props);
	props.disable_peace_crouch=enable;
	SC_P_Ai_SetProps(pl_id,&props);
}

void P_SetBerserk(dword member,float multi){
	s_SC_P_AI_props props;
	CLEAR(props);
	SC_P_Ai_GetProps(member,&props);
	props.berserk=multi;
	SC_P_Ai_SetProps(member,&props);
}
void P_Sethear(dword member,float multi){
	s_SC_P_AI_props props;
	CLEAR(props);
	SC_P_Ai_GetProps(member,&props);
	props.hear_distance_mult=multi;
	SC_P_Ai_SetProps(member,&props);
}

void P_Setmarksman(dword member,float multi){
	s_SC_P_AI_props props;
	CLEAR(props);
	SC_P_Ai_GetProps(member,&props);
	props.shoot_imprecision*=multi;
	SC_P_Ai_SetProps(member,&props);
}

void P_Setdamage(dword member,float multi){
	s_SC_P_AI_props props;
	CLEAR(props);
	SC_P_Ai_GetProps(member,&props);
	props.shoot_damage_mult*=multi;
	SC_P_Ai_SetProps(member,&props);
}

void P_EnableGrenadeUse(dword member,BOOL stat){
	s_SC_P_AI_props props;
	CLEAR(props);
	SC_P_Ai_GetProps(member,&props);
	if (stat) props.grenade_sure_time=5;
	else props.grenade_sure_time=1000;
	SC_P_Ai_SetProps(member,&props);

}

void P_Berserk(dword pl_id, float val) {
	s_SC_P_AI_props props;
	CLEAR(props);
	SC_P_Ai_GetProps(pl_id,&props);
	props.berserk=val;
	SC_P_Ai_SetProps(pl_id,&props);
}

int Getcurrentmission(){
	return SC_ggi(SGI_CURRENTMISSION);
}

int Getchopper(){
	return SC_ggi(SGI_CHOPPER);
}

float  P_Health(dword pl_id){
	 s_SC_P_getinfo ginfo;
	 SC_P_GetInfo(pl_id, &ginfo);
	 return ginfo.cur_hp;
}

void P_Visibility(dword pl_id, float visibility){
	s_SC_P_AI_props props;
	CLEAR(props);
	SC_P_Ai_GetProps(pl_id,&props);
	props.max_vis_distance=visibility;
	SC_P_Ai_SetProps(pl_id,&props);
}

#define Setplayerweapons SetPlayerWeapons				//for back compatibility
#define Saveplayerweapons SavePlayerWeapons		

void SetPlayerWeapons(s_SC_P_Create *weap){
	weap->weap_knife=SC_ggi(PLAYER_WEAPON1); 
	if (!weap->weap_knife) weap->weap_knife=29;

	if (weap->weap_knife==PLAYER_FREESLOT) weap->weap_knife=0;
	
	weap->weap_pistol=SC_ggi(PLAYER_WEAPON2); 	
	if (!weap->weap_pistol) weap->weap_pistol=7;
	if (weap->weap_pistol==PLAYER_FREESLOT) weap->weap_pistol=0;


	weap->weap_main1=SC_ggi(PLAYER_WEAPON3);
	
	if (!weap->weap_main1) {
		if (SC_ggi(SGI_CURRENTMISSION)>49){			//ADDON
			if (SC_ggi(SGI_CURRENTMISSION)>58){
				weap->weap_main1=32;
			} else 
			weap->weap_main1=24;
		} else
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

void SavePlayerWeapons(){
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



void SetPlayerHealth(){
	SC_P_ReadHealthFromGlobalVar(SC_PC_Get(),PLAYER_HEALTHSTART);
}

void SavePlayerHealth(){
	SC_P_WriteHealthToGlobalVar(SC_PC_Get(),PLAYER_HEALTHSTART);
}

void SetPlayerAmmo(){
	SC_P_ReadAmmoFromGlobalVar(SC_PC_Get(),PLAYER_AMMOSTART,PLAYER_AMMOLAST);
	if (SC_ggi(PLAYER_AMMOINGUN)) SC_P_SetAmmoInWeap(SC_PC_Get(),2,SC_ggi(PLAYER_AMMOINGUN));
	if (SC_ggi(PLAYER_AMMOINPISTOL)) SC_P_SetAmmoInWeap(SC_PC_Get(),1,SC_ggi(PLAYER_AMMOINPISTOL));
}

void SavePlayerAmmo(){
	SC_P_WriteAmmoToGlobalVar(SC_PC_Get(),PLAYER_AMMOSTART,PLAYER_AMMOLAST);
	SC_sgi(PLAYER_AMMOINGUN,SC_P_GetAmmoInWeap(SC_PC_Get(),2));
	SC_sgi(PLAYER_AMMOINPISTOL,SC_P_GetAmmoInWeap(SC_PC_Get(),1));
}

void SavePlayerIntel(){
	s_SC_P_intel intel;
	int i;
	
	SC_PC_GetIntel(&intel);
	for (i=0;i<SC_P_INTEL_MAX;i++){
		SC_sgi(PLAYER_INTELSTART+i,intel.intel[i]);
	}
}

void SetPlayerIntel(){
	s_SC_P_intel intel;
	int i;
	
	for (i=0;i<SC_P_INTEL_MAX;i++){
		intel.intel[i]=SC_ggi(PLAYER_INTELSTART+i); 
	}
	SC_PC_SetIntel(&intel);
}

#define Nextmission NextMission

void NextMission(){				
	SavePlayerWeapons();
	SavePlayerAmmo();
	SavePlayerHealth();
	SC_MissionCompleted();
	//SC_UP_Open(8, SC_ggi(SGI_CURRENTMISSION));
}

void NextMission2(){				
	SavePlayerIntel();
	SavePlayerWeapons();
	SavePlayerAmmo();
	SavePlayerHealth();
	SC_Osi("MISSION COMPLETE");
	SC_MissionDone();
}

void ShowHelp(dword helpid){
	SC_ShowHelp(&helpid,1,HELP_TIME);
}

void ShowHelp2(dword helpid,dword helpid2){
	dword helps[2];
	helps[0]=helpid;
	helps[1]=helpid2;
	SC_ShowHelp(helps,2,HELP_TIME*2);		// is timing correct?
}

void ShowHelp3(dword helpid,dword helpid2, dword helpid3){
	dword helps[3];
	helps[0]=helpid;
	helps[1]=helpid2;
	helps[2]=helpid3;
	SC_ShowHelp(helps,3, HELP_TIME*4);		// is timing correct?
}


int Diffic(){
	return SC_ggi(SGI_DIFFICULTY);
}

int getVCweapon(){
	int eq;
	eq=rand()%20;
	
	if (SC_ggi(SGI_CURRENTMISSION)>12){
	//	SC_Log(3,"Found weapon %d for later levels",eq);
		if (eq>19) return 18;
		if (eq>18) return 15;
		if (eq>17) return 26;
		if (eq>11) return 2;
		if (eq>8) return 19;
		if (eq>3) return 6;
		return 23;
	} else {
	//	SC_Log(3,"Found weapon %d for basic levels",eq);
		if (eq>19) return 28;
		if (eq>16) return 15;
		if (eq>13) return 26;
		if (eq>9) return 2;
		if (eq>6) return 19;
		if (eq>3) return 6;
		return 23;		
		}

}

int getVClongrangeweapon(){
	int eq;
	eq=rand()%20;
	if (eq>18) return 14;
	if (eq>16) return 18;
	if (eq>12) return 2;
	if (eq>8) return 15;
	return 2;
		
}

int GetVCCampaignWeapon(){
	int eq;
	eq=rand()%20;

	switch(SC_ggi(SGI_CURRENTMISSION)){
	case MISSION_MEDPATROL:
		if (eq>10) return 19;
		return 26;
		break;
	case MISSION_3CANYONSFIRST:
	case MISSION_3CANYONSA:
	case MISSION_3CANYONSB:
	case MISSION_BAHNARFIRST:
	//case MISSION_COLLECTORS:
		if (eq>12) return 26;
		if (eq>8) return 6;
		//if (eq>3) 
		return 19;
		//return 10;
		break;
	case MISSION_BIGVALLEY:
	case MISSION_OUTPOST:
		if (eq>14) return 26;
		if (eq>10) return 19;
		if (eq>5) return 6;
		return 23;
		break;
	case MISSION_BASECAMPFIRST:
		if (eq>15) return 26;
		if (eq>11) return 19;
		if (eq>7) return 6;
		if (eq>2) return 23;
		return 25;
		break;
	case MISSION_FRENCHROUTEA:
	case MISSION_FRENCHROUTEB:
	case MISSION_ARROYO:
		if (eq>16) return 26;
		if (eq>12) return 15;
		if (eq>8) return 6;
		if (eq>4) return 19;
		return 2;
		break;
	case MISSION_TUNNELS:
	case MISSION_TUNNELS2:
	case MISSION_UNDERGROUND:
		if (eq>13) return 8;
		if (eq>6) return 9;
		return 10;
		break;
	case MISSION_BIGRIVER:
		if (eq>15) return 2;
		if (eq>11) return 15;
		if (eq>8) return 19;
		if (eq>4) return 6;
		if (eq>1) return 26;
		return 18;
		break;
	case MISSION_NIGHT:
	case MISSION_NIGHT_B:
	case MISSION_AMBUSH:
	case MISSION_RADIORELAY:
		if (eq>15) return 2;
		if (eq>11) return 15;
		if (eq>8) return 19;
		if (eq>5) return 6;
		if (eq>2) return 26;
		return 23;
	case MISSION_CRASHFLIGHT:
	case MISSION_CRASH:
	case MISSION_CONQUEST:
	case MISSION_NVABASE:
		if (eq>14) return 2;
		if (eq>10) return 15;
		if (eq>4) return 23;
		return 18;
		break;
	case MISSION_ESCAPE:
		if (eq>15) return 2;
		if (eq>11) return 19;
		if (eq>8) return 6;
		if (eq>4) return 23;
		if (eq>1) return 26;
		return 21;
		break;
	case MISSION_STREAM:
	case MISSION_BAHNARRAZEDA:
	case MISSION_BAHNARRAZEDB:
		if (eq>14) return 2;
		if (eq>10) return 15;
		if (eq>7) return 23;
		if (eq>3) return 6;
		return 18;
		break;
/*	case MISSION_JARAIEVAC:
		if (eq>14) return 2;
		if (eq>11) return 15;
		if (eq>8) return 18;
		if (eq>4) return 23;
		if (eq>2) return 6;
		return 14;*/
		break;
//	case MISSION_OUTPOSTEVAC:
	case MISSION_BIGVALLEYCHOPPER:
		if (eq>14) return 2;
		if (eq>11) return 15;
		if (eq>8) return 18;
		if (eq>3) return 23;
		return 6;
		break;
	case MISSION_PILOT:
		if (eq>2) return 2;
		return 14;
		break;
	case MISSION_BASECAMPDEFEAT:
	case MISSION_BASECAMPDEFEAT2:
	case MISSION_BASECAMPDEFEAT3:
		if (eq>13) return 2;
		if (eq>11) return 15;
		if (eq>7) return 18;
		if (eq>4) return 23;
		if (eq>1) return 6;
		return 14;
		break;

//ADDON DEFINITIONS


	case MISSION_BOMBERPILOT:
		if (eq>14) return 15;
		if (eq>6) return 26;
		return 19;			
		break;
	
	case MISSION_JARAI:
	case MISSION_HANGINGBRIDGE:
		if (eq>14) return 15;
		if (eq>10) return 23;
		if (eq>5) return 6;
		return 13;			

		break;
	case MISSION_MINEFACTORY:
		if (eq>14) return 15;
		if (eq>10) return 23;
		if (eq>5) return 2;
		return 13;			
		break;
	case MISSION_BASEATTACK:
		if (eq>9) return 2;
		if (eq>5) return 5;
		return 13;			
		break;
	case MISSION_DEATHVALLEYA:
	case MISSION_DEATHVALLEYB:
	case MISSION_NVACAMP:
		if (eq>10) return 2;
		if (eq>7) return 18;
		return 13;
		break;


		
	}
	return 2;
}

char *GetVCCampaignIni(){
	int eq;
	eq=rand()%20;

	switch(SC_ggi(SGI_CURRENTMISSION)){
	case MISSION_MEDPATROL:
	//case MISSION_COLLECTORS:
	case MISSION_BIGVALLEY:
	case MISSION_OUTPOST:
	case MISSION_BASECAMPFIRST:
		if (eq>13) return "ini\\players\\poorvc.ini";
		if (eq>6) return "ini\\players\\poorvc2.ini";
		return "ini\\players\\poorvc3.ini";
		break;
	case MISSION_3CANYONSFIRST:
	case MISSION_3CANYONSA:
	case MISSION_3CANYONSB:
	case MISSION_BAHNARFIRST:
	case MISSION_FRENCHROUTEA:
	case MISSION_FRENCHROUTEB:
	case MISSION_ARROYO:
		if (eq>13) return "ini\\players\\vcfighter2.ini";
		if (eq>6) return "ini\\players\\vcfighter3.ini";
		return "ini\\players\\vcfighter4.ini";
		break;
	case MISSION_TUNNELS:
	case MISSION_TUNNELS2:
	case MISSION_BIGRIVER:
	case MISSION_NIGHT:
	case MISSION_NIGHT_B:
	case MISSION_AMBUSH:
	case MISSION_ESCAPE:
		if (eq>15) return "ini\\players\\vcfighter3.ini";
		if (eq>10) return "ini\\players\\vcfighter2.ini";
		if (eq>5) return "ini\\players\\vcfighter3.ini";
		return "ini\\players\\vcfighter4.ini";
		break;
	case MISSION_RADIORELAY:
	case MISSION_CRASHFLIGHT:
	case MISSION_CRASH:
	case MISSION_CONQUEST:
	case MISSION_STREAM:
	case MISSION_BAHNARRAZEDA:
	case MISSION_BAHNARRAZEDB:
	//case MISSION_JARAIEVAC:
		if (eq>13) return "ini\\players\\vcuniform1.ini";
		if (eq>6) return "ini\\players\\vcuniform2.ini";
		return "ini\\players\\vcuniform3.ini";
		break;		
	case MISSION_NVABASE:
	case MISSION_UNDERGROUND:
//	case MISSION_OUTPOSTEVAC:
	case MISSION_PILOT:
	case MISSION_BIGVALLEYCHOPPER:
	case MISSION_BASECAMPDEFEAT:
	case MISSION_BASECAMPDEFEAT2:
	case MISSION_BASECAMPDEFEAT3:
		if (eq>12) return "ini\\players\\nvasoldier2.ini";
		if (eq>4) return "ini\\players\\nvasoldier3.ini";
		return "ini\\players\\nvaofficer.ini";
		break;		


//ADDON DEFINITIONS


	case MISSION_BOMBERPILOT:
		if (eq>15) return "ini\\players\\vcfighter2.ini";
		if (eq>10) return "ini\\players\\vcfighter3.ini";
		if (eq>5) return "ini\\players\\vcfighter4.ini";
		return "ini\\players\\vcfighter5.ini";
		break;
	case MISSION_JARAI:
	case MISSION_HANGINGBRIDGE:
		if (eq>15) return "ini\\players\\poorvc.ini";
		if (eq>10) return "ini\\players\\poorvc2.ini";
		if (eq>5) return "ini\\players\\poorvc3.ini";
		return "ini\\players\\poorvc4.ini";
		break;
	case MISSION_MINEFACTORY:
		if (eq>15) return "ini\\players\\vcuniform1.ini";
		if (eq>10) return "ini\\players\\vcuniform2.ini";
		if (eq>5) return "ini\\players\\vcuniform3.ini";
		return "ini\\players\\vcuniform4.ini";
		break;
	case MISSION_BASEATTACK:
		if (eq>15) return "ini\\players\\vcuniform1.ini";
		if (eq>10) return "ini\\players\\vcuniform2.ini";
		if (eq>5) return "ini\\players\\vcuniform3.ini";
		return "ini\\players\\vcuniform4.ini";
		break;
	case MISSION_DEATHVALLEYA:
	case MISSION_DEATHVALLEYB:
	case MISSION_NVACAMP:
		if (eq>12) return "ini\\players\\nvasoldier2.ini";
		if (eq>4) return "ini\\players\\nvasoldier3.ini";
		return "ini\\players\\nvaofficer.ini";
		break;




		
	}
	return "ini\\players\\default_aiviet.ini";
}

void GetVCEquip(s_SC_P_Create *pinfo){
	int i;
	
	for (i=0;i<SC_P_CREATE_AEG_VALID_MAX;i++){
		pinfo->aeg_valid_head_bes[i]=0;
		pinfo->aeg_valid_body_bes[i]=0;
	}
	switch(SC_ggi(SGI_CURRENTMISSION)){
	case MISSION_MEDPATROL:
		pinfo->aeg_valid_head_bes[0]=24;
		pinfo->aeg_valid_head_bes[1]=38;
		break;
	case MISSION_3CANYONSFIRST:
	case MISSION_3CANYONSA:
	case MISSION_3CANYONSB:
	case MISSION_BAHNARFIRST:
		pinfo->aeg_valid_head_bes[0]=23;
		pinfo->aeg_valid_head_bes[1]=25;
		break;
/*	case MISSION_COLLECTORS:
		pinfo->aeg_valid_head_bes[0]=23;
		pinfo->aeg_valid_head_bes[1]=26;
		break;*/
	case MISSION_BIGVALLEY:
	case MISSION_OUTPOST:
		pinfo->aeg_valid_head_bes[0]=23;
		pinfo->aeg_valid_head_bes[1]=26;
		pinfo->aeg_valid_head_bes[2]=24;
		break;
	case MISSION_BASECAMPFIRST:
		pinfo->aeg_valid_head_bes[0]=24;
		pinfo->aeg_valid_head_bes[1]=26;
		pinfo->aeg_valid_head_bes[2]=38;
		break;
	case MISSION_FRENCHROUTEA:
	case MISSION_FRENCHROUTEB:
		pinfo->aeg_valid_head_bes[0]=23;
		pinfo->aeg_valid_head_bes[1]=24;
		pinfo->aeg_valid_head_bes[2]=25;
		break;
	case MISSION_TUNNELS:
	case MISSION_TUNNELS2:
	case MISSION_ARROYO:
		pinfo->aeg_valid_head_bes[0]=23;
		pinfo->aeg_valid_head_bes[1]=25;
		break;
	case MISSION_BIGRIVER:
		pinfo->aeg_valid_head_bes[0]=23;
		pinfo->aeg_valid_head_bes[1]=24;
		pinfo->aeg_valid_head_bes[2]=25;
		pinfo->aeg_valid_head_bes[3]=37;
		pinfo->aeg_valid_head_bes[4]=38;
		break;
	case MISSION_NIGHT:
	case MISSION_NIGHT_B:
	case MISSION_AMBUSH:
		pinfo->aeg_valid_head_bes[0]=23;
		pinfo->aeg_valid_head_bes[1]=25;
		break;
	case MISSION_RADIORELAY:
	case MISSION_CRASHFLIGHT:
	case MISSION_CRASH:
		pinfo->aeg_valid_head_bes[0]=27;
		pinfo->aeg_valid_head_bes[1]=28;
		pinfo->aeg_valid_head_bes[2]=31;
		break;
	case MISSION_CONQUEST:
		pinfo->aeg_valid_head_bes[0]=27;
		pinfo->aeg_valid_head_bes[1]=28;
		pinfo->aeg_valid_head_bes[2]=31;
		pinfo->aeg_valid_head_bes[3]=35;
		break;
	case MISSION_NVABASE:
	case MISSION_UNDERGROUND:
		pinfo->aeg_valid_head_bes[0]=35;
		pinfo->aeg_valid_head_bes[1]=27;
		pinfo->aeg_valid_head_bes[2]=32;
		pinfo->aeg_valid_head_bes[3]=33;
		pinfo->aeg_valid_head_bes[4]=34;
		break;
	case MISSION_ESCAPE:
		pinfo->aeg_valid_head_bes[0]=23;
		pinfo->aeg_valid_head_bes[1]=25;
		break;
	case MISSION_STREAM:
	case MISSION_BAHNARRAZEDA:
	case MISSION_BAHNARRAZEDB:
	//case MISSION_JARAIEVAC:
		pinfo->aeg_valid_head_bes[0]=26;
		pinfo->aeg_valid_head_bes[1]=27;
		pinfo->aeg_valid_head_bes[2]=28;
		pinfo->aeg_valid_head_bes[3]=31;
		break;
	/*case MISSION_OUTPOSTEVAC:
		pinfo->aeg_valid_head_bes[0]=32;
		pinfo->aeg_valid_head_bes[1]=33;
		pinfo->aeg_valid_head_bes[2]=35;
		pinfo->aeg_valid_head_bes[3]=36;
		break;*/
	case MISSION_PILOT:
		pinfo->aeg_valid_head_bes[0]=31;
		pinfo->aeg_valid_head_bes[1]=35;
		pinfo->aeg_valid_head_bes[2]=36;
		break;
	case MISSION_BIGVALLEYCHOPPER:
		pinfo->aeg_valid_head_bes[0]=35;
		pinfo->aeg_valid_head_bes[1]=32;
		pinfo->aeg_valid_head_bes[2]=33;
		pinfo->aeg_valid_head_bes[3]=34;
		break;
	case MISSION_BASECAMPDEFEAT:
	case MISSION_BASECAMPDEFEAT2:
	case MISSION_BASECAMPDEFEAT3:
		pinfo->aeg_valid_head_bes[0]=33;
		pinfo->aeg_valid_head_bes[1]=34;
		pinfo->aeg_valid_head_bes[2]=35;
		pinfo->aeg_valid_head_bes[3]=36;
		break;

//ADDON DEFINITIONS


	case MISSION_BOMBERPILOT:
		pinfo->aeg_valid_head_bes[0]=23;
		pinfo->aeg_valid_head_bes[1]=25;
		break;
	case MISSION_JARAI:
	case MISSION_HANGINGBRIDGE:
		pinfo->aeg_valid_head_bes[0]=24;
		pinfo->aeg_valid_head_bes[1]=38;
		break;
	case MISSION_MINEFACTORY:
		pinfo->aeg_valid_head_bes[0]=26;
		pinfo->aeg_valid_head_bes[1]=27;
		pinfo->aeg_valid_head_bes[2]=28;
		pinfo->aeg_valid_head_bes[3]=31;
		break;
		break;
	case MISSION_BASEATTACK:
		pinfo->aeg_valid_head_bes[0]=26;
		pinfo->aeg_valid_head_bes[1]=27;
		pinfo->aeg_valid_head_bes[2]=28;
		pinfo->aeg_valid_head_bes[3]=31;
		break;
		break;
	case MISSION_DEATHVALLEYA:
	case MISSION_DEATHVALLEYB:
	case MISSION_NVACAMP:
		pinfo->aeg_valid_head_bes[0]=33;
		pinfo->aeg_valid_head_bes[1]=34;
		pinfo->aeg_valid_head_bes[2]=35;
		pinfo->aeg_valid_head_bes[3]=36;
		break;




	default:
		pinfo->aeg_valid_head_bes[0]=35;
		pinfo->aeg_valid_head_bes[1]=27;
		pinfo->aeg_valid_head_bes[2]=32;
		pinfo->aeg_valid_head_bes[3]=33;
		pinfo->aeg_valid_head_bes[4]=34;
		break;
	}
}



#define MAXDETECTDIST  100

//changed only for SP game

#define GetNearestHumanPos(pl_id, mpos)	SC_PC_GetPos(mpos)

/*BOOL GetNearestHumanPos(dword pl_id, c_Vector3 *mpos){
	s_SC_MP_EnumPlayers pllist[32];	
	c_Vector3 vec,mvec;
	int pls=32,i;
	float dist,nd;
	
	dist=MAXDETECTDIST;
	if (SC_ggi(SGI_GAMETYPE)){
		SC_P_GetPos(pl_id,&mvec);
		SC_MP_EnumPlayers(pllist,&pls,0);
		if (!pls) return FALSE;
		//SC_Log(3,"Detecting %d enemies",pls);
		for (i=0;i<pls;i++) 
			if (pllist[i].status==SC_MP_P_STATUS_INGAME){				
				SC_P_GetPos(pllist[i].id,&vec);
				nd=SC_2VectorsDist(&vec,&mvec);
				//SC_Log(3,"Player %s has distance %f",pllist[i].name,nd);
				if (nd<dist){
					dist=nd;
					*mpos=vec;
					//SC_Log(3,"Saving pos %f,%f,%f",mpos->x,mpos->y,mpos->z);
				}
		}
		if (dist<MAXDETECTDIST) return TRUE;
		return FALSE;
	}
	SC_PC_GetPos(mpos);
	dist=SC_2VectorsDist(&vec,&mvec);
	//SC_Log(3,"Singleplayer gethuman");
	if (dist<MAXDETECTDIST) return TRUE;
	return FALSE;
}
*/


#define Groupdead GroupDead

BOOL GroupDead(int side, int group){
	int i, num;

	num=SC_GetGroupPlayers(side, group);
	for (i=0;i<num;i++) 
	{
		if (!isdead(side, group,i)) return FALSE;
	}

	return TRUE;
}

//counts inactives as dead
BOOL GroupDead2(int side, int group){
	int i, num;

	num=SC_GetGroupPlayers(side, group);
	for (i=0;i<num;i++) 
	{
		if (!isdead(side, group,i)&&SC_P_GetActive(SC_P_GetBySideGroupMember(side,group,i))) return FALSE;
		
	}

	return TRUE;
}


#define Groupindanger GroupInDanger

BOOL GroupInDanger(int group){
	int i, j, num;
	float x;
	dword member;
	num=SC_GetGroupPlayers(1, group);
	for (i=0;i<num;i++) {
			member=GetVC(group,i);
			if (member){
				x=SC_P_Ai_GetDanger(member);
				//SC_Log(3,"danger is %f",x);
				if (x>2) return TRUE;
				j=SC_P_Ai_GetSureEnemies(member);
				//SC_Log(3,"Enemies is %f",j);
				if (j>0) return TRUE;
				
			}
		}		
	return FALSE;
}

#define Teamindanger TeamInDanger 
BOOL TeamInDanger (){
	int i, j, num;
	float x;
	dword member;
	for (i=1;i<6;i++) {
			member=GetUS(i);
			if (member){
				x=SC_P_Ai_GetDanger(member);
				//SC_Log(3,"danger is %f",x);
				if (x>2) return TRUE;
				j=SC_P_Ai_GetSureEnemies(member);
				//SC_Log(3,"Enemies is %f",j);
				if (j>0) return TRUE;
				
			}
		}		
	return FALSE;
}

float TeamNear(c_Vector3 *where){
	int i;
	c_Vector3 vec;
	float maxdist=10000;
	float dist;
	dword member;
	
	for (i=0;i<6;i++) {
		member=GetUS(i);
		if (member){
			SC_P_GetPos(member,&vec);
			dist=SC_2VectorsDist(where,&vec);	
			if (dist<maxdist) maxdist=dist;
		}
	}
	return maxdist;
}

int NearestTeamMember(){		//returns ID of nearest team member to PC
	int i;
	c_Vector3 vec;
	float maxdist=10000;
	float dist;
	dword member;
	int rval=-1;
	
	for (i=1;i<6;i++) {
		member=GetUS(i);
		if (member){
			dist=SC_P_GetDistance(SC_PC_Get(),member);
			if (dist<maxdist) {
				maxdist=dist;
				rval=i;
			}
		}
	}
	return rval;

}


void NOD_Pos(char *name,c_Vector3 *where){
	void *nod;
	nod=SC_NOD_Get(NULL,name);
	if (nod!=NULL) SC_NOD_GetWorldPos(nod,where);
}

float NOD_Rot(char *name){
	void *nod;
	nod=SC_NOD_Get(NULL,name);
	if (nod!=NULL) return SC_NOD_GetWorldRotZ(nod);
	return 0;
}

void StopPoint(){
	if (SC_P_Ai_GetPeaceMode(GetUS(1))==SC_P_AI_PEACEMODE_POINT) SC_P_Ai_SetPeaceMode(GetUS(1),SC_P_AI_PEACEMODE_HOLD);
	SC_P_Ai_Stop(GetUS(1));
}

void NOD_Explosion(char *name,int explotype){
	c_Vector3 vec;
	NOD_Pos(name,&vec);
	SC_DoExplosion(&vec,explotype);	
}

void Claymore(char *name){
					float rot;
					c_Vector3 vec,vec2;
					void *nod;
					
					nod=SC_NOD_Get(NULL,name);
					if (!nod) {
						SC_message("FATAL! Claymore %s not found!!!!!!");
						return;
					}
					SC_NOD_GetWorldPos(nod,&vec);
					rot=SC_NOD_GetWorldRotZ(nod);
					
					rot-=1.57f;
					vec2=vec;
					vec2.x-=2*cos(rot);
					vec2.y+=2*sin(rot);
					SC_DoExplosion(&vec2,1);
					vec2=vec;
					vec2.x-=4*cos(rot);
					vec2.y+=4*sin(rot);
					SC_DoExplosion(&vec2,2);
					vec2=vec;
					vec2.x-=8*cos(rot);
					vec2.y+=8*sin(rot);
					SC_DoExplosion(&vec2,3);
					SC_DUMMY_Set_DoNotRenHier2(nod,TRUE);
}

void NOD_ClusterExplosion(char *name,int explotype,int count, float radius){
	int i;
	c_Vector3 vec2;
	c_Vector3 vec;

	NOD_Pos(name,&vec);
	vec2.z=vec.z;
	for (i=0;i<count;i++){
		vec2.x=vec.x+frnd(radius);
		vec2.y=vec.y+frnd(radius);
		SC_DoExplosion(&vec2,explotype);	
	}
}

void WP_Explosion(char *name,int explotype){
	c_Vector3 vec;
	SC_GetWp(name,&vec);
	SC_DoExplosion(&vec,explotype);	
}

void WP_Smoke(char *name){
	c_Vector3 vec;
	SC_GetWp(name,&vec);
	SC_CreatePtc(176,&vec);
}

void WP_Bomb_Effect(char *name){
	c_Vector3 vec;
	int i;
	
	SC_GetWp(name,&vec);
	SC_DoExplosion(&vec,3);	
	//SC_CreatePtc(176,&vec);
	SC_SND_PlaySound3D(2965,&vec);
	SC_CreatePtc_Ext(176,SC_NOD_Get(NULL,name),1000,0,1,1);
	SC_CreatePtc_Ext(177,SC_NOD_Get(NULL,name),1000,0,1,1);
	for (i=0;i<6;i++){
		SC_GetWp(name,&vec);
		vec.x+=frnd(5);
		vec.y+=frnd(5);
		SC_CreatePtcVec_Ext(177,&vec,1000,0,1,1);
	}	
}

void Bomb_Effect(c_Vector3 *vec){
	int i;
	SC_CreatePtc(198,vec);	
	SC_SND_PlaySound3D(2965,vec);
	SC_CreatePtcVec_Ext(176,vec,1000,0,1,1);
	SC_CreatePtcVec_Ext(177,vec,5,0,1,1);
}

void ClusterBomb_Effect(c_Vector3 *vec,int size, float radius){
	int i;
	c_Vector3 vec2;

	//SC_SND_PlaySound3D(2965,vec);
	vec2.z=vec->z;
	for (i=0;i<size;i++){
		vec2.x=vec->x+frnd(radius);
		vec2.y=vec->y+frnd(radius);
		SC_CreatePtc(198,&vec2);
		SC_CreatePtcVec_Ext(177,&vec2,5,0,1,1);
	}
	SC_CreatePtcVec_Ext(176,vec,1000,0,1,1);
}

void ClusterBomb_EffectNF(c_Vector3 *vec,int size, float radius){
	int i;
	c_Vector3 vec2;

	//SC_SND_PlaySound3D(2965,vec);
	vec2.z=vec->z;
	for (i=0;i<size;i++){
		vec2.x=vec->x+frnd(radius);
		vec2.y=vec->y+frnd(radius);
		SC_CreatePtc(198,&vec2);
		//SC_CreatePtcVec_Ext(177,&vec2,5,0,1,1);
	}
	SC_CreatePtcVec_Ext(176,vec,1000,0,1,1);
}

void ClusterBomb_EffectNP(c_Vector3 *vec,int size, float radius){
	int i;
	c_Vector3 vec2;

	vec2.z=vec->z;
	for (i=0;i<size;i++){
		vec2.x=vec->x+frnd(radius);
		vec2.y=vec->y+frnd(radius);
		SC_CreatePtc(198,&vec2);
	}
}



void P_MakeTrenchFighter(dword pl_id){
	s_SC_P_Ai_BattleProps bprops;
	s_SC_P_AI_props props;
	CLEAR(props);
	SC_P_Ai_GetProps(pl_id,&props);
	props.disable_peace_crouch=TRUE;
	props.boldness=4;
	SC_P_Ai_SetProps(pl_id,&props);
	bprops.Aim=0.9f;
	bprops.Position=0.3f;
	bprops.Run=0.5f;
	SC_P_Ai_SetBattleProps(pl_id,&bprops);
}

BOOL P_IsMoving(dword pl_id){
	c_Vector3 pos;
	float len;
	
	SC_P_GetDir(pl_id,&pos);
	len = SC_VectorLen(&pos);
	if (len>1.0f) return TRUE;
	return FALSE;
}

float TeamDist(c_Vector3 *target){
	int i;
	float dist=9999;
	float dst;
	c_Vector3 vec;
	
	for (i=0;i<6;i++) 
		if (SC_P_IsReady(GetUS(i))){
			SC_P_GetPos(GetUS(i),&vec);	
			dst=SC_2VectorsDist(&vec,target);
			if (dst<dist) dist=dst;
		}
	return dist;
}


BOOL TeamWithPC(float maxdist){
	int i;
	
	for (i=1;i<6;i++) 
		if (SC_P_IsReady(GetUS(i))){
			if (SC_P_GetDistance(SC_PC_Get(),GetUS(i))>maxdist) return FALSE;
		}
	return TRUE;

}

BOOL PCInContact(float maxdist){
	int i,j;
	dword list[64];
	s_sphere sph;
	s_SC_P_getinfo pinfo;
	c_Vector3 vec;
	float dist,dist2;
	
	SC_PC_GetPos(&sph.pos);
	sph.rad=maxdist;
	i=32;
	SC_GetPls(&sph,list,&i);
	
	for (j=0;j<i;j++) {
		SC_P_GetInfo(list[j],&pinfo);
		if ((pinfo.side==1)&&(P_InDanger(list[j]))&&(SC_P_IsReady(list[j]))){
			return TRUE;
		}
	}


	return FALSE;
}


#define SetMovieTxt(id1,id2,id3) {dword movtext[3]={id1,id2,id3};SC_ShowMovieInfo(movtext);}

BOOL P_Near(dword pl, c_Vector3 *vec, float dist){
	c_Vector3 vec2;
	SC_P_GetPos(pl,&vec2);
	return SC_IsNear3D(&vec2,vec,dist);
}

BOOL PC_Near(c_Vector3 *vec, float dist){
	c_Vector3 vec2;
	SC_PC_GetPos(&vec2);
	return SC_IsNear3D(&vec2,vec,dist);
}

void P_SetGrenadeProps(dword pl_id,float mindist,float timing,float imprec,float suretime){
	s_SC_P_AI_props props;
	if (!pl_id) return;
	CLEAR(props);
	SC_P_Ai_GetProps(pl_id,&props);
	props.grenade_min_distance=mindist;			// minimal distance to throw grenade at (default: 10.0f)
	props.grenade_timing_imprecision=timing;	// random max + in sec						(default: 0.5f)
	props.grenade_throw_imprecision=imprec;	// 0 - totally exact, 1 - normal		(default: 1.0f)
	props.grenade_sure_time=suretime;			// how long player makes sure about valid situation to throw grenade (default: 5.0f sec)
	SC_P_Ai_SetProps(pl_id,&props);
}

dword GetNearestPlayer(int side,c_Vector3 *place){
	int i,j;
	dword list[32],saved;
	s_sphere sph;
	s_SC_P_getinfo pinfo;
	c_Vector3 vec;
	float dist,dist2;
	
	
	dist=10000;

	sph.rad=1000;
	sph.pos=*place;
	i=32;
	SC_GetPls(&sph,list,&i);
	saved=0;
	
	for (j=0;j<i;j++) {
		SC_P_GetInfo(list[j],&pinfo);
		if (((pinfo.side==side)||(side==100))&&(SC_P_IsReady(list[j]))){
			SC_P_GetPos(list[j],&vec);
			dist2=SC_2VectorsDist(&vec,place);
			if (dist2<dist){
				dist=dist2;
				saved=list[j];
			}
		}
	}
	return saved;

}

dword GetNearestPlayerToPlayer(dword player, int side){
	int i,j;
	dword list[32],saved;
	s_sphere sph;
	s_SC_P_getinfo pinfo;
	c_Vector3 vec;
	float dist,dist2;
	
	
	if (!player) return 0;
	dist=10000;

	sph.rad=1000;
	SC_P_GetPos(player,&vec);
	sph.pos=vec;
	i=32;
	SC_GetPls(&sph,list,&i);
	saved=0;
	
	for (j=0;j<i;j++) {
		SC_P_GetInfo(list[j],&pinfo);
		if (((pinfo.side==side)||(side==100))&&(SC_P_IsReady(list[j]))){
			SC_P_GetPos(list[j],&vec);
			dist2=SC_P_GetDistance(player,list[j]);
			if (dist2<dist){
				dist=dist2;
				saved=list[j];
			}
		}
	}
	return saved;

}

dword GetNearestPlayer2(int side,float maxdist, c_Vector3 *place){
	int i,j;
	dword list[32],saved;
	s_sphere sph;
	s_SC_P_getinfo pinfo;
	c_Vector3 vec;
	float dist,dist2;
	
	
	dist=maxdist;

	sph.rad=maxdist;
	sph.pos=*place;
	i=32;
	SC_GetPls(&sph,list,&i);
	saved=0;
	
	for (j=0;j<i;j++) {
		SC_P_GetInfo(list[j],&pinfo);
		if (((pinfo.side==side)||(side==100))&&(SC_P_IsReady(list[j]))){
			SC_P_GetPos(list[j],&vec);
			dist2=SC_2VectorsDist(&vec,place);
			if (dist2<dist){
				dist=dist2;
				saved=list[j];
			}
		}
	}
	return saved;

}


void GetMyGroup(dword pl_id,dword *savelist,dword *count){
	int i,j,listpos,groupid;
	dword list[32];
	s_sphere sph;
	s_SC_P_getinfo pinfo;
		
	SC_P_GetInfo(pl_id,&pinfo);
	groupid=pinfo.group;

	SC_P_GetPos(pl_id,&sph.pos);
	sph.rad=1000;	
	i=32;
	SC_GetPls(&sph,list,&i);
	listpos=0;
	
	for (j=0;j<i;j++) {
		SC_P_GetInfo(list[j],&pinfo);
		if ((pinfo.side==1)&&(pinfo.group==groupid)&&(SC_P_IsReady(list[j]))){
			savelist[listpos]=list[j];
			listpos++;
			if (listpos==count) {
				SC_Log(3,"GetMyGroup: TOO much players in group around!");
				return;
			}
		}
	}
	*count=listpos;
}

void FindNextCommander(dword pl_id){
	int i,j;
	dword list[32];
	s_SC_P_getinfo pinfo;
	
	i=32;
	
	GetMyGroup(pl_id,list,&i);
	SC_P_GetInfo(pl_id,&pinfo);
	
	if (i<2) {
		SC_Log(3,"VC %d %d couldnot find anyone to lead group %d",pinfo.group,pinfo.member_id,pinfo.group);
		return;
	}
	if (list[0]!=pl_id) {
		S_Mes(list[0],SCM_YOUARECOMMANDER,0);
	} else {
		S_Mes(list[1],SCM_YOUARECOMMANDER,0);
	}
	SC_Log(3,"VC %d %d moved command over group",pinfo.group,pinfo.member_id);	
}

float P_GetDistFrom(dword pl_id,c_Vector3 *vec){
	c_Vector3 vec2;
	float x;
	SC_P_GetPos(pl_id,&vec2);
	x = SC_2VectorsDist(vec,&vec2);
	//SC_Log(3,"Dist from is %f",x);
	return x;
}

void P_ClearSpecAnim(dword pl_id){
			s_SC_P_SpecAnims specanim;
			CLEAR(specanim);
			specanim.sa[0]=NULL;
			specanim.sa[1]=NULL;
			specanim.sa[2]=NULL;
			specanim.sa[3]=NULL;
			specanim.sa[4]=NULL;
			SC_P_SetSpecAnims(pl_id,&specanim);	
}


void P_SetSpecAnim(dword pl_id, char *A1,char *A2,char *A3,char *A4,char *A5){
			s_SC_P_SpecAnims specanim;
			CLEAR(specanim);
			specanim.sa[0]=A1;
			specanim.sa[1]=A2;
			specanim.sa[2]=A3;
			specanim.sa[3]=A4;
			specanim.sa[4]=A5;
			SC_P_SetSpecAnims(pl_id,&specanim);	
}

void Killing_Sphere(s_sphere *sph,float damage){
	int i,j,listpos,groupid;
	dword list[32];
	i=32;
	SC_GetPls(sph,list,&i);
	if (!i) return;
	for (j=0;j<i;j++) {
		SC_P_DoHit(list[j],SC_P_MESH_AREA_BODYFRONT,damage/7);
		SC_P_DoHit(list[j],SC_P_MESH_AREA_BODYBACK,damage/7);
		SC_P_DoHit(list[j],SC_P_MESH_AREA_LEFTARM,damage/7);
		SC_P_DoHit(list[j],SC_P_MESH_AREA_RIGHTARM,damage/7);
		SC_P_DoHit(list[j],SC_P_MESH_AREA_LEFTLEG,damage/7);
		SC_P_DoHit(list[j],SC_P_MESH_AREA_RIGHTLEG,damage/7);
		SC_P_DoHit(list[j],SC_P_MESH_AREA_HEAD,damage/7);
	}
}

BOOL P_IsVisible(dword pl_id){
	s_sphere sph;
	
	SC_P_GetPos(pl_id,&sph.pos);
	sph.pos.z+=1;
	sph.rad=1;
	return SC_SphereIsVisible(&sph);
}

int P_GetSide(dword pl_id){
	 s_SC_P_getinfo ginfo;
	 SC_P_GetInfo(pl_id, &ginfo);
	 return ginfo.side;	
}

int P_GetGroup(dword pl_id){
	 s_SC_P_getinfo ginfo;
	 SC_P_GetInfo(pl_id, &ginfo);
	 return ginfo.group;	
}

int P_GetMember(dword pl_id){
	 s_SC_P_getinfo ginfo;
	 SC_P_GetInfo(pl_id, &ginfo);
	 return ginfo.member_id;	
}


#define P_SetStealth(pl_id,val) SC_Ai_SetStealthMode(P_GetSide(pl_id),P_GetGroup(pl_id), val)	

#define P_ShootAt(pl_id, place, time) SC_P_AddAllAmmo(pl_id); P_SetStealth(pl_id,FALSE); SC_P_Ai_ShootAt(pl_id,place,time);

BOOL PC_InHelper(char *name){
	s_sphere 		sph;
	
	SC_GetScriptHelper(name,&sph);
	return P_Near(SC_PC_Get(),&sph.pos,sph.rad);	
}


void SetGNDprops(s_SC_P_AI_props *props){
	//props.grenade_min_distance;			// minimal distance to throw grenade at (default: 10.0f)
	props->grenade_timing_imprecision=1.5f;	// random max + in sec						(default: 0.5f)
	props->grenade_throw_imprecision=2.0f;	
}

#endif
