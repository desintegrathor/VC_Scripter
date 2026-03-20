//
//	Global Level_h.h
//	This file is appointed for new levels (included in level packs and datadisc)
//	by Beny
//


//We don't want to include any other .h in scripts
#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\mplevel.inc>



// + + + ---------------------------------------------------------------------
// + + + Common
// + + + ---------------------------------------------------------------------


//gPhase of PLAYER
#define	GP_CREATE		0
#define	GP_INIT			1
//--->									//values from 10 to 99999 are reserved for level-depended use
#define	GP_SNIPE		100000			//sniper's shot
#define	GP_GOTO			100001			//goto somewhere
#define	GP_WAIT			100002			//wait for something
#define	GP_PENDL_FWD	100003			//go forward through the pendl path
#define	GP_PENDL_BCK	100004			//go backward through the pendl path
#define	GP_HAUNT		100005			//go to player's pos
#define	GP_ENEMYSPOTTED	100006			//we have found enemy at this time
#define	GP_ACTIVATEPL	100007			//we're waiting for some condition to make player active
#define	GP_DELAY		100008			//used for misc delays
#define	GP_FOLLOW		100009			//follow someone (usually follow pc)
#define	GP_ATTACK		100010			//crush the player
#define	GP_RECOVER		100011			//recover player (usually after SCM_RECOVER)
#define	GP_RETREAT		100012			//retreat somewhere
#define	GP_DO			100013			//do something
#define	GP_ENTERHELI	100014			//enter heli
#define	GP_EXITHELI		100015			//exit heli
#define	GP_BEGINATTACK	100016			//begin attack (used in coop)
#define	GP_DESTROY		100017			//destroy something
//...
#define	GP_IDLE			1000000			//idle state

//Groups
#define	GR_US_0			0				//player's group
#define	GR_US_1			1				//usually Rosenfield and other soldiers
#define	GR_US_2			2				//usually pilots

#define	GR_VC_0			0				//
#define	GR_VC_1			1				//
#define	GR_VC_2			2				//
#define	GR_VC_3			3				//
#define	GR_VC_4			4				//
#define	GR_VC_5			5				//
#define	GR_VC_6			6				//
#define	GR_VC_7			7				//
#define	GR_VC_8			8				//
#define	GR_VC_9			9				//
#define	GR_VC_10		10				//


//special calls (for SC_Set_GoToPC_snd())
#define SP_CALL_LIM1	10452
#define SP_CALL_LIM2	10453
#define SP_CALL_LIM3	10454
#define SP_CALL_NGUYEN1	10455
#define SP_CALL_NGUYEN2	10456
#define SP_CALL_NGUYEN3	10457


//weap
#define	PL_GUN_RND		0xFFFFFFFF		//generate a random gun (used for AI create)

//
struct s_pendlDef {
	c_Vector3	wp;
	dword		action;
	dword		data;					//action related
}; //struct s_pendlDef {




//macros
//get player
#define	_GP(side, group, member) SC_P_GetBySideGroupMember(side, group, member)
#define	_GPVC(group, member) SC_P_GetBySideGroupMember(SC_P_SIDE_VC, group, member)
#define	_GPUS(group, member) SC_P_GetBySideGroupMember(SC_P_SIDE_US, group, member)
//get player of player's team
#define	_GPT(member) SC_P_GetBySideGroupMember(SC_P_SIDE_US, GR_US_0, member)

//team members
#define	idPoint		_GPT(SC_P_MEMBERID_POINT)
#define	idMedic		_GPT(SC_P_MEMBERID_MEDIC)
#define	idDemol		_GPT(SC_P_MEMBERID_DEMOLITION)
#define	idRadio		_GPT(SC_P_MEMBERID_RADIO)
#define	idMachin	_GPT(SC_P_MEMBERID_MACHINEGUN)
#define	idPlayer	SC_PC_Get()




//
BOOL GetDummyPos(char *name, c_Vector3 *vec)
{
	void *mobj;

	mobj = SC_NOD_Get(NULL, name);
	if (mobj == NULL)
		return FALSE;

	SC_NOD_GetWorldPos(mobj, vec);
	return TRUE;
}

//
float fAbs(float f)
{
	return (f < 0) ? -f : f;
}


//is group dead?
int IsGroupAlmostDead(int SideID, int GroupID, int Tolerance)
{
	int		i, num, cur = 0;

	num = SC_GetGroupPlayers(SideID, GroupID);
	for (i = 0; i < num; i++) 
	{
		if ( SC_P_IsReady( SC_P_GetBySideGroupMember(SideID, GroupID, i) ) )
			cur++;
	}

	if (cur <= Tolerance )
		return TRUE;

	return FALSE;
}

//
BOOL IsVCAlive(int GroupID, int MemberID)
{
	return SC_P_IsReady( SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GroupID, MemberID) );
}

//
dword GetNumAliveVC(int GroupID)
{
	int		i, num, cur = 0;

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GroupID);
	for (i = 0; i < num; i++) 
	{
		if ( SC_P_IsReady( SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GroupID, i) ) )
			cur++;
	}

	return cur;
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




// + + + ---------------------------------------------------------------------
// + + + Single game
// + + + ---------------------------------------------------------------------


//
BOOL HeliIsEveryoneOut(dword GroupID)
{
	dword	i, num;

	num = SC_GetGroupPlayers(SC_P_SIDE_US, GroupID);
	for (i = 0; i < num; i++)
	{
		if ( SC_P_IsInHeli(SC_P_GetBySideGroupMember(SC_P_SIDE_US, GroupID, i)) )
			return FALSE;
	}

	return TRUE;
}

//
BOOL HeliIsEverybodyIn(dword GroupID)
{
	dword	i, num, pl;

	num = SC_GetGroupPlayers(SC_P_SIDE_US, GroupID);
	for (i = 0; i < num; i++)
	{
		pl = SC_P_GetBySideGroupMember(SC_P_SIDE_US, GroupID, i);

		if ( !SC_P_IsInHeli(pl) && SC_P_IsReady(pl) )
			return FALSE;
	}

	return TRUE;
}



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
		if (SC_ggi(SGI_CURRENTMISSION)>49){			//ADDON
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





void SetRadioProps()
{
	s_SC_SpeachBreakProps	props;

	CLEAR(props);
	
	props.pl_back_txt = 5111;
	props.pl_back_snd = 5111;
	props.ra_back_txt = 5008;
	props.ra_back_snd = 5008;
	props.ra_where_ru_nr = 3;
	props.ra_where_ru_txt[0] = 5010;
	props.ra_where_ru_txt[1] = 5009;
	props.ra_where_ru_txt[2] = 5011;

	props.ra_where_ru_snd[0] = 5010;
	props.ra_where_ru_snd[1] = 5009;
	props.ra_where_ru_snd[1] = 5011;
	props.ra_where_ru_snd[3] = 0;
	props.ra_where_ru_snd[4] = 0;

	SC_RadioBreak_Set(&props);		
	SC_RadioSetDist(10.0f);
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

//ADDON DEFINITIONS - replace with correct one!!!


	case MISSION_BOMBERPILOT:
		if (eq>14) return 15;
		if (eq>10) return 23;
		if (eq>5) return 6;
		return 13;			//MISSING TOKAREV ID
		break;
	case MISSION_JARAI:
	case MISSION_HANGINGBRIDGE:
		if (eq>14) return 15;
		if (eq>10) return 23;
		if (eq>5) return 6;
		return 13;			//MISSING TOKAREV ID

		break;
	case MISSION_MINEFACTORY:
		if (eq>14) return 15;
		if (eq>10) return 23;
		if (eq>5) return 6;
		return 13;			//MISSING TOKAREV ID
		break;
	case MISSION_BASEATTACK:
		if (eq>14) return 2;
		if (eq>10) return 23;
		if (eq>5) return 5;
		return 13;			//MISSING TOKAREV ID
		break;
	case MISSION_DEATHVALLEYA:
	case MISSION_DEATHVALLEYB:
	case MISSION_NVACAMP:
		if (eq>13) return 2;
		if (eq>11) return 15;
		if (eq>7) return 18;
		if (eq>4) return 23;
		return 6;
		break;


		
	}
	return 2;
}



// + + + ---------------------------------------------------------------------
// + + + Movie system
// + + + ---------------------------------------------------------------------


//commands
#define	CMD_END				0			//end of movie (no params)
#define	CMD_NEXT			1			//next movie chunk (no params)
#define	CMD_WAIT			2			//wait some time (Param2: time)
#define	CMD_BLOCKEND		3			//switches to next block immediately when all commands from current block are marked as CMD_DONE
#define	CMD_PL_ANIM			10			//player animation (Param1: player; Param2: anim)
#define	CMD_PL_STATIV		11			//set spec anim - stativ (Param1: player; Param2: anim)
#define	CMD_PL_SPEECH		12			//say something (Param1: player; Param2: speech id)
#define	CMD_PL_TELE			13			//teleport player (Param1: player; Param2: dummy)
#define	CMD_PL_LOOKATPL		14			//look at other player (Param1: player; Param2: target player)
#define	CMD_PL_LOOKATPOS	15			//look at pos (Param1: player; Param2: dummy)
#define	CMD_PL_CLOSEEYES	16			//close/open eyes (Param1: player; Param2: 1 = close | 0 = open)
#define	CMD_R_SPEECH		30			//radio speech (Param2: speech id)
#define	CMD_AGS_SET			31			//adjust music via AGS (Param2: SetAGS() param)
#define	CMD_SND_PLAY2D		32			//play 2D snd (Param2: snd id)
#define	CMD_CAM_SET			33			//set camera animation (Param1: 0 = cam anim is played in frame range <0; 10000> || time range maked by #macro TM(); Param2: camAnim)
#define	CMD_TITLE			34			//show/hide title (Param2: 0 = hide title || 1 = show title defined by variable called movieInfo[])
#define	CMD_FAUNA_ALERT		35			//do fauna alert (Param2: dummy)
#define	CMD_FADE			36			//fade screen (Param1: 0 = from black to normal | 1 = fade to black; Param2 = time*100 (e.g. 352 = 3.52s))
#define	CMD_DONE			0xFFFFFFFF	//(internal command, don't use)

//players
#define	pCaptain		0
#define	pPoint			1
#define	pMedic			2
#define	pDemol			3
#define	pRadio			4
#define	pMachine		5

//#macros to translate two signed shorts to unsigned long and back (used to make a camera-anim time in movie definiton)
#define	TM(s, e)		(dword)((((dword)(short)s) << 16) | (unsigned short)(short)e)
#define	TMLO(se)		(short)((dword)se & 0xFFFF)
#define	TMHI(se)		(short)(((dword)se >> 16) & 0xFFFF)

//movie definition
typedef struct _s_MovieDef {
	float	fTimer;			//cas od zacatku
	dword	Cmd;			//command to perform
	dword	param1;			//cmd-specific param
	dword	param2;			//cmd-specific param
} s_MovieDef;




// + + + ---------------------------------------------------------------------
// + + + Multiplayer game
// + + + ---------------------------------------------------------------------


//Random VC weapons
#define	MAX_WEAPS	10
dword vc_weap[MAX_WEAPS] = {2,6,8,9,14,15,18,23,26,28};

int GetVCRndWeapon()
{
	return vc_weap[ rand()%MAX_WEAPS ];
}


//Random VC Inis
#define	MAX_INIS	9
char *vc_ini[] = {		"ini\\players\\poorvc.ini", 
						"ini\\players\\poorvc2.ini", 
						"ini\\players\\poorvc3.ini",
						"ini\\players\\vcfighter2.ini", 
						"ini\\players\\vcfighter3.ini", 
						"ini\\players\\vcfighter4.ini", 
						"ini\\players\\vcuniform3.ini", 
						"ini\\players\\nvaofficer.ini", 
						"ini\\players\\default_aiviet.ini"	};


char *GetVCRndIni()
{
	return vc_ini[ rand()%MAX_INIS ];
}
