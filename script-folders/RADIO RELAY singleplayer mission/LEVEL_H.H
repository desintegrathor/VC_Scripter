//
//	Level_h.h
//


#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\gLevel_h.h>




//heli animation - beginning of level
#define HELI_ANIM		"g\\camanims\\RadioRelay01.anm"

//heli times
#define	TM_START		0
#define	TM_LOOP1_BEGIN	651
#define	TM_LOOP1_END	1519
#define	TM_LOOP2_BEGIN	1953
#define	TM_LOOP2_END	3255
#define	TM_LAND			4445
#define	TM_END			6000

#define	CAM1_ANIM		"G\\camanims\\CAMERA\\RADIO_RELAY\\RadiorRel_C0.anm"
#define	TM_CAM1_START	0
#define	TM_CAM1_END		180

#define	CAM2_ANIM		"G\\camanims\\CAMERA\\RADIO_RELAY\\RadioRel_C1.anm"
#define	TM_CAM2_START	181
#define	TM_CAM2_END		400



//End of level
#define	HELI_ANIM2		"g\\camanims\\radiorelayheli02.anm"
#define	TM_START2		0
#define	TM_LAND2		2980
#define	TM_END2			4858
#define	TM_CHECK2		2830

//cam11
#define	CAM11_ANIM		"G\\camanims\\CAMERA\\RADIO_RELAY\\Radiocam_out01.anm"
#define	TM_CAM11_START	2980
#define	TM_CAM11_END	3111
//cam12
#define	CAM12_ANIM		"G\\camanims\\CAMERA\\RADIO_RELAY\\Radiocam_out02.anm"
#define	TM_CAM12_START	3111	
#define	TM_CAM12_END	3449

#define	TM_MISCOMPLETED	4.0f


//Camanim of RR destruction, when Mission Failed
#define	CAM3_ANIM		"G\\camanims\\CAMERA\\RADIO_RELAY\\Radio_crash.anm"
#define	TM_CAM3_START	0
#define	TM_CAM3_END		500
#define	TM_CAM3_EXPL	40
#define	TM_CAM3_FADE	400




//gPhase of PLAYER
#define	GP_CREATE		0
#define	GP_INIT			1
#define	GP_DO_WPPATH	3
#define	GP_END_WPPATH	4
#define	GP_IDLE			100
#define	GP_WAIT_WPPATH	101
#define	GP_RETREAT		102
#define	GP_HIDE			103
#define	GP_RETREATING	104
#define	GP_RECOVER		105
#define	GP_SNIPE		106
#define	GP_GOTOPL		107
#define	GP_ATTACK		108				//goto POS_ATTACK
#define	GP_DESTROY_RR	109				//destroy RR in camanim
#define	GP_SHOOTON_RR	110



//messages
#define	SCM_HELIOUT		50
#define	SCM_HELIIN		51
#define	SCM_ATTACK		52				//send from heli to VC
#define	SCM_BATTLEMODE	53				//switch AI to battle
#define	SCM_ENABLEUPDATE 54				//enable situation update
#define	SCM_RECOVER		55				//recover if dead
#define	SCM_SAY			56				//player says next message; param2 contains new gPhase
#define	SCM_IMNEAR		57				//send by VC to US. param2 is id of location. used for texts.
#define	SCM_ATTACKDONE	60				//AI reached the AttackPos (see GP_ATTACK)
#define	SCM_MORTARFIRE	61
#define	SCM_MINDEAD		62
#define	SCM_SETKILLER	63
#define	SCM_SETNORMAL	64
#define	SCM_DESTROY_RR	65
#define	SCM_LLAMA		66

//events
#define	EVT_VC_ATTACK	1
#define	EVT_VC_NOTYET	2				//don't attack for xx seconds


//SGI
/*
#define	SGI_HELIATEND	4000			//if TRUE, Heli01 goes for US_0
#define	SGI_MINDEAD		4001			//when minometcici are dead, set to TRUE
#define	SGI_USEFLARES	4002
#define	SGI_SOUMRAK		4003			//uz se setmelo?
*/


//Groups
#define	GR_US_0			0				//player's group
#define	GR_US_1			1				//US on Radio Relay hill
#define	GR_US_2			2				//pilots

#define	GR_VC_0			0				//minomet
#define	GR_VC_1			1				//first wave
#define	GR_VC_2			2				//v lesiku za minometem
#define	GR_VC_3			3				//3 na kopci
#define	GR_VC_4			4				//2 na kopci
#define	GR_VC_5			5				//2 na kopci
#define	GR_VC_6			6				//2 na kopci
#define	GR_VC_7			7				//2 na kopci
#define	GR_VC_8			8				//3 na kopci
#define	GR_VC_9			9				//
#define	GR_VC_10		10				//snipers












//Actions
#define	ACT_NONE		0x00000000		//Stop on wp and do nothing

#define	ACT_STOP		0x00000001		//Stop on this wp		.
#define	ACT_RUN			0x00000002		//Run to next wp		. only one of these flags can be specified
#define	ACT_WALK		0x00000004		//Walk to next wp		.

#define	ACT_STAND		0x00000010		//Stand					.
#define	ACT_CROUCH		0x00000020		//Crouch				. only one of these flags can be specified
#define	ACT_LIE			0x00000040		//Lie					.

#define	ACT_SHOOT		0x00000100		//Shoot on specified position
#define	ACT_CMD			0x00000200		//Send command to other AI 
#define	ACT_EVENT		0x00000400		//Event for level script
#define	ACT_DOSCRIPT	0x00000800		//Calls the DoScript(dword doScriptParam) function. Uses the s_wpPathElement.doScript param to identify what to do.


//Events - see ACT_EVENT
#define	ACE_DIST0		1000			//informs level script about AI
#define	ACE_DIST1		1001
#define	ACE_DIST2		1002
#define	ACE_DIST3		1003
#define	ACE_DIST4		1004


//Defines a WayPoint-path element.
struct s_wpPathElement {

//	char		*wpName;				//WayPoint name
	c_Vector3	wpPos;					//position to go to
	dword		action;					//action to take on this wp
	float		wait;					//number of seconds to start action
	c_Vector3	shoot;					//location to shoot to (ACT_SHOOT must be specified)

	dword		cmd;					//command to send to other AI (consists of ACT_??? flags; ACT_CMD must be specified)
	dword		numAI;					//number of members in s_wpPathElement.ai[]
	dword		ai[4];					//IDs of AI that will receive cmd

	dword		evParam1;				//parameter for Level script when ACT_EVENT is specified
	dword		doScript;				//id of script to do (see DoScript())
//	dword		evParam2;

}; //struct s_wpPathElement {


//this macro creates ID of player for WayPoint-path system
#define	AImake_ID(GroupID, MemberID) (GroupID*1000 + MemberID)

//
#define	_GP(side, group, member) SC_P_GetBySideGroupMember(side, group, member)
#define	_GPUS0(member) SC_P_GetBySideGroupMember(SC_P_SIDE_US, GR_US_0, member)


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


//recover dead VC
dword VC_RecoverDead()
{
	dword	pl_id, num, i;
	c_Vector3	vec;


	//send command to all AI
	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_1);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_1, i);
		SC_P_ScriptMessage( pl_id, SCM_RECOVER, FALSE);
	}
	
	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_2);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_2, i);
		SC_P_ScriptMessage( pl_id, SCM_RECOVER, FALSE);
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_3);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_3, i);
		SC_P_ScriptMessage( pl_id, SCM_RECOVER, FALSE);
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_4);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_4, i);
		SC_P_ScriptMessage( pl_id, SCM_RECOVER, FALSE);
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_5);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_5, i);
		SC_P_ScriptMessage( pl_id, SCM_RECOVER, FALSE);
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_6);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_6, i);
		SC_P_ScriptMessage( pl_id, SCM_RECOVER, FALSE);
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_7);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_7, i);
		SC_P_ScriptMessage( pl_id, SCM_RECOVER, FALSE);
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_8);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_8, i);
		SC_P_ScriptMessage( pl_id, SCM_RECOVER, FALSE);
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_9);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_9, i);
		SC_P_ScriptMessage( pl_id, SCM_RECOVER, FALSE);
	}

	
	//snipers
	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_10);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_10, i);
		SC_P_ScriptMessage( pl_id, SCM_RECOVER, FALSE);
	}

	return 0;
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
dword NumAliveMembers(int SideID, int GroupID)
{
	int		i, num, cur = 0;

	num = SC_GetGroupPlayers(SideID, GroupID);
	for (i = 0; i < num; i++) 
	{
		if ( SC_P_IsReady( SC_P_GetBySideGroupMember(SideID, GroupID, i) ) )
			cur++;
	}

	return cur;
}


//get amount of enemies (except of minomet)
dword RR_GetNumVC()
{
	dword	num = 0;

	//
	num += SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_1);
	num += SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_2);
	num += SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_3);
	num += SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_4);
	num += SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_5);
	num += SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_6);
	num += SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_7);
	num += SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_8);
	num += SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_9);
	num += SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_10);

	return num;
}

//
dword RR_GetCurrentVC()
{
	dword	pl_id, i, num, current = 0;
	c_Vector3	vec;


	//send command to all AI
	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_1);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_1, i);
		if ( SC_P_IsReady( pl_id ) )
			current++;
	}
	
	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_2);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_2, i);
		if ( SC_P_IsReady( pl_id ) )
			current++;
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_3);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_3, i);
		if ( SC_P_IsReady( pl_id ) )
			current++;
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_4);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_4, i);
		if ( SC_P_IsReady( pl_id ) )
			current++;
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_5);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_5, i);
		if ( SC_P_IsReady( pl_id ) )
			current++;
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_6);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_6, i);
		if ( SC_P_IsReady( pl_id ) )
			current++;
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_7);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_7, i);
		if ( SC_P_IsReady( pl_id ) )
			current++;
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_8);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_8, i);
		if ( SC_P_IsReady( pl_id ) )
			current++;
	}

	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_9);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_9, i);
		if ( SC_P_IsReady( pl_id ) )
			current++;
	}

	//snipers
	num = SC_GetGroupPlayers(SC_P_SIDE_VC, GR_VC_10);
	for (i = 0; i < num; i++)
	{
		pl_id = SC_P_GetBySideGroupMember(SC_P_SIDE_VC, GR_VC_10, i);
		if ( SC_P_IsReady( pl_id ) )
			current++;
	}

	return current;
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
