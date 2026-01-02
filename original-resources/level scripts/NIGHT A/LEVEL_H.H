//
//	Level_h.h
//


#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\gLevel_h.h>


//
#define	DA_NONE					0
#define	DA_OZRALEC_WAKEUP		1
#define	DA_OZRALEC_CHCANIEND	2
#define	DA_KUACOTOBYLO			3


//bino
#define	CAM_ANIM		"G\\camanims\\CAMERA\\NIGHT\\dalekohled.anm"
#define	TM_CAM_START	0
#define	TM_CAM_END		1380

#define	TM_KEC01		698
#define	TM_KEC02		1008
#define	TM_KEC03		1230
#define	TM_KEC04		1380

//pris death
#define	CAM_ANIM02		"G\\camanims\\camera\\Night\\Zajatec.anm"
#define	TM_CAM_START02	0
#define	TM_CAM_END02	300

//napalm 1
#define	CAM_ANIM03		"G\\camanims\\CAMERA\\NIGHT\\Nightnap1.anm"
#define	TM_CAM_START03	0
#define	TM_CAM_END03	172

//napalm 2
#define	CAM_ANIM04		"G\\camanims\\CAMERA\\NIGHT\\Nightnap2.anm"
#define	TM_CAM_START04	173
#define	TM_CAM_END04	500




//gPhase of PLAYER
#define	GP_CREATE		0
#define	GP_INIT			1
#define	GP_DO_WPPATH	3
#define	GP_END_WPPATH	4
#define	GP_WAIT_WPPATH	100
#define	GP_IDLE			101

#define	GP_PENDL_FWD	102
#define	GP_PENDL_BCK	103
#define	GP_PENDL_RND	104
#define	GP_PENDL		105


#define	GP_RNDWAIT		106
#define	GP_CHECKENEMY	107
#define	GP_HAUNT		108
#define	GP_WAKEUP		109

#define	GP_ACT_WAIT		110

#define	GP_JDUSEVYCHCAT	111
#define	GP_KILLPRIS		112
#define	GP_KURVACOTOBYLO	113
#define	GP_PRISKILLED	114
#define	GP_ENEMYTEST	115
#define	GP_DEJVEDET		116
#define	GP_IMPROVE		117



//gi
/*
#define	SGI_ALARM01		4001			//ve vesnici
//#define	SGI_ALARM02		4002
//#define	SGI_ALARM03		4003
#define	SGI_HELI01GO	4004
//#define	SGI_HELILOADED	4005
//#define	SGI_NUM_VC2_DEAD 4006
#define	SGI_PRISFREE	4007
#define	SGI_HWIZD		4008
#define	SGI_BRONSONOK	4009

#define	SGI_CURKECGROUP	4021
#define	SGI_CURKEC		4022
#define	SGI_CURPLAYER	4023
#define	SGI_BOMBALARM	4024
#define	SGI_IGNORE_LSC	4025
#define	SGI_LSC			4026
#define	SGI_HLIDACALARM	4027

#define	SGI_BRONSN_R	4030		//ready to action?
#define	SGI_DEFORT_R	4031
#define	SGI_HORNST_R	4032

#define	SGI_NAPALM		4033
#define	SGI_NHUTCOOP	4034
#define	SGI_HELIFULL	4035		//when SCM_HELILOADED recevied
*/


//messages
#define	SCM_ATTACK		200				//u templu
#define	SCM_ENABLEUPDATE 201				//u templu
#define	SCM_GOTO		202
#define	SCM_REQUEST		203
#define	SCM_PRISOUT		204
#define	SCM_HELILOADED	205
#define	SCM_TELEPORTFORANIM	207
#define	SCM_ENABLEMAPSPEECH		208
#define	SCM_PRISONPOINT	209
#define	SCM_HELIIN		210



//Groups
#define	GR_US_0			0				//player's group
#define	GR_US_1			1				//
#define	GR_US_4			4				//pilots

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




//
#define	PA_NONE			0
#define	PA_WAIT			1
#define	PA_CHCANI		2
#define	PA_CHCANIEND	3

struct s_pendlDef {
	c_Vector3	wp;
	dword		action;
	dword		data;					//action related
}; //struct s_pendlDef {


//
struct s_spchDef {
	dword	speechId;
	dword	memberId;
}; //struct s_spchDef {

//
struct s_SpeechGroup {
	dword	numSpeeches;
	struct	s_spchDef pSpeeches[10];
}; //struct s_SpeechDefs {

//
struct s_Kecy {
	dword	numGroups;
	struct s_SpeechGroup pGroups[10];
}; //struct s_Kecy {


//
//	++ speech defs

struct s_Kecy	kecy = {

	4,				//numGroups
	{
		{6, {	1500, 0,  
			  	1501, 1,  
			  	1502, 1,  
			  	1503, 1,  
			  	1504, 0,  
			  	1505, 0, 
				0, 0, 
				0, 0, 
				0, 0, 
				0, 0, 
			}, 
		}, 
		{5, {	1506, 1,  
				1507, 2,  
				1508, 1,  
				1509, 2,  
				1510, 1, 
				0, 0, 
				0, 0, 
				0, 0, 
				0, 0, 
				0, 0, 
			},
		}, 
		{6, {	1511, 1,  
				1512, 2,  
				1513, 1,  
				1514, 2,  
				1515, 0,  
				1516, 2, 
				0, 0, 
				0, 0, 
				0, 0, 
				0, 0, 
			}, 
		},
		{7, {	1517, 1,  
				1518, 0,  
				1519, 2,  
				1520, 1,  
				1521, 2,  
				1522, 0,  
 				1523, 2, 
				0, 0, 
				0, 0, 
				0, 0, 
			}, 
		}, 
	}
};

//	-- speech defs
//


//
#define	_GP(side, group, member) SC_P_GetBySideGroupMember(side, group, member)


//this macro creates ID of player for WayPoint-path system
#define	AImake_ID(GroupID, MemberID) (GroupID*1000 + MemberID)





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

float fAbs(float f)
{
	return (f < 0) ? -f : f;
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


//
dword GetMyUS(dword id)
{
	return SC_P_GetBySideGroupMember(SC_P_SIDE_US, GR_US_0, id);
}

//This function outs a random speech from specified group. See VSS\Vietkong\GenericSpeech.doc
dword PointSpeech(dword SpGroup, float *time)
{
	dword	spchID;
//	float	time = 0;

	//p0x[0] means the number of elements in array
	dword	p01[] = {3,  5410, 5411, 5412};
	dword	p02[] = {3,  5415, 5416, 5417};
	dword	p03[] = {3,  5420, 5421, 5422};
	dword	p04[] = {3,  5425, 5426, 5427};
	dword	p05[] = {3,  5430, 5431, 5432};
	dword	p06[] = {3,  5435, 5436, 5437};
	dword	p07[] = {3,  5440, 5441, 5442};


	switch( SpGroup )
	{
	case 1:				//(agreement)
		spchID = p01[ (rand() % p01[0])+1 ];
		SC_P_Speech2(GetMyUS(SC_P_MEMBERID_POINT), spchID, time);
		return spchID;

	case 2:				//(detecting boobytrap)
		spchID = p02[ (rand() % p02[0])+1 ];
		SC_P_Speech2(GetMyUS(SC_P_MEMBERID_POINT), spchID, time);
		return spchID;

	case 3:				//(waits for disarming the trap)
		spchID = p03[ (rand() % p03[0])+1 ];
		SC_P_Speech2(GetMyUS(SC_P_MEMBERID_POINT), spchID, time);
		return spchID;

	case 4:				//(waits for disarming next traps)
		spchID = p04[ (rand() % p04[0])+1 ];
		SC_P_Speech2(GetMyUS(SC_P_MEMBERID_POINT), spchID, time);
		return spchID;

	case 5:				//(waits when VC near)
		spchID = p05[ (rand() % p05[0])+1 ];
		SC_P_Speech2(GetMyUS(SC_P_MEMBERID_POINT), spchID, time);
		return spchID;

	case 6:				//(waits when VC around)
		spchID = p06[ (rand() % p06[0])+1 ];
		SC_P_Speech2(GetMyUS(SC_P_MEMBERID_POINT), spchID, time);
		return spchID;

	case 7:				//(aggressive agreement)
		spchID = p07[ (rand() % p07[0])+1 ];
		SC_P_Speech2(GetMyUS(SC_P_MEMBERID_POINT), spchID, time);
		return spchID;
	}

	return 0;
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
		if (eq>16) return 26;
		if (eq>12) return 15;
		if (eq>8) return 6;
		if (eq>4) return 19;
		return 2;
		break;
	case MISSION_TUNNELS:
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
		if (eq>13) return 2;
		if (eq>11) return 15;
		if (eq>7) return 18;
		if (eq>4) return 23;
		if (eq>1) return 6;
		return 14;
		break;
		
	}
	return 2;
}

char *GetVCCampaignIni(){
	int eq;
	eq=rand()%20;

	switch(SC_ggi(SGI_CURRENTMISSION)){
	case MISSION_MEDPATROL:
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
		if (eq>13) return "ini\\players\\vcfighter2.ini";
		if (eq>6) return "ini\\players\\vcfighter3.ini";
		return "ini\\players\\vcfighter4.ini";
		break;
	case MISSION_TUNNELS:
	case MISSION_BIGRIVER:
	case MISSION_NIGHT:
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
		if (eq>13) return "ini\\players\\vcuniform1.ini";
		if (eq>6) return "ini\\players\\vcuniform2.ini";
		return "ini\\players\\vcuniform3.ini";
		break;		
	case MISSION_NVABASE:
	case MISSION_UNDERGROUND:
	case MISSION_PILOT:
	case MISSION_BIGVALLEYCHOPPER:
	case MISSION_BASECAMPDEFEAT:
	case MISSION_BASECAMPDEFEAT2:
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
		pinfo->aeg_valid_head_bes[0]=26;
		pinfo->aeg_valid_head_bes[1]=27;
		pinfo->aeg_valid_head_bes[2]=28;
		pinfo->aeg_valid_head_bes[3]=31;
		break;
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
		pinfo->aeg_valid_head_bes[0]=33;
		pinfo->aeg_valid_head_bes[1]=34;
		pinfo->aeg_valid_head_bes[2]=35;
		pinfo->aeg_valid_head_bes[3]=36;
		break;
	}
}

