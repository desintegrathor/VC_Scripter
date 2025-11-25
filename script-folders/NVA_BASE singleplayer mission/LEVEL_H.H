//
//	Level_h.h
//


#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\gLevel_h.h>




#define	TM_CAM_START	0
#define	TM_CAM_END		800
#define	CAM_ANIM	"G\\camanims\\CAMERA\\NVA\\NVACAM.anm"		//fade in: 193-294




//gPhase of PLAYER
#define	GP_CREATE		0
#define	GP_INIT			1
#define	GP_DO_WPPATH	3
#define	GP_END_WPPATH	4
#define	GP_WAIT_WPPATH	100
#define	GP_IDLE			101
#define	GP_PENDL		102



//Groups
#define	GR_US_0			0				//player's group
#define	GR_US_1			1				//
#define	GR_US_2			2				//
#define	GR_US_3			3				//
#define	GR_US_4			4				//

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
#define	SCE_FIRSTKEC	1000
#define	SCE_FOUNDEXIT	1001
#define	SCE_HASINTEL	1002
#define	SCE_POWS		1003

//
#define	SCM_SETACTIVE	1001
#define	SCM_APPEAR		1002
#define	SCM_RADIODONE	1003
#define	SCM_TELEPORT	1004


/*/
#define	SGI_USPRISONER	4000
#define	SGI_FOUNDEXIT	4001
#define	SGI_CANTALK		4002
#define	SGI_CAMANIM01	4003
#define	SGI_CAMANIMEND01 4004
#define	SGI_AADESTR1	4005
#define	SGI_AADESTR2	4006
*/

//Actions
#define	ACT_NONE		0x00000000		//stop on wp and do nothing

#define	ACT_STOP		0x00000001		//stop on this wp
#define	ACT_RUN			0x00000002		//run to next wp
#define	ACT_WALK		0x00000004		//walk to next wp

#define	ACT_STAND		0x00000010		//stand
#define	ACT_CROUCH		0x00000020		//crouch
#define	ACT_LIE			0x00000040		//lie

#define	ACT_SHOOT		0x00000100		//shoot on specified position
#define	ACT_CMD			0x00000200		//send command to other AI



//Defines a WayPoint-path element.
struct s_wpPathElement {

	char		*wpName;				//WayPoint name
	dword		action;					//action to take on this wp
//	float		wait;					//number of seconds to start action
	c_Vector3	shoot;					//location to shoot to (ACT_SHOOT must be specified)

	dword		cmd;					//command to send to other AI (consists of ACT_??? flags; ACT_CMD must be specified)
	dword		numAI;					//number of members in s_wpPathElement.ai[]
	dword		ai[4];					//IDs of AI that will receive cmd

}; //struct s_wpPathElement {


//this macro creates ID of player for WayPoint-path system
#define	AImake_ID(GroupID, MemberID) (GroupID*1000 + MemberID)

//
#define	_GP(side, group, member) SC_P_GetBySideGroupMember(side, group, member)

//
#define	_ALIVE(group, member) SC_P_IsReady( SC_P_GetBySideGroupMember(SC_P_SIDE_VC, group, member) )


//
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
BOOL GetDummyPos(char *name, c_Vector3 *vec)
{
	void *mobj;

	mobj = SC_NOD_Get(NULL, name);
	if (mobj == NULL)
		return FALSE;

	SC_NOD_GetWorldPos(mobj, vec);
	return TRUE;
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
		return "ini\\players\\nvasoldier2.ini";
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

void EquipPlayerVC(s_SC_P_CreateEqp *eqp, int *count)
{
	dword	rnd;


	*count = 0;

	rnd = rand() % 2;
	eqp[0].bes = (rnd) ? "G\\EQUIPMENT\\VC\\bes\\EOP_e_mgznpouch01VC.BES" : "G\\EQUIPMENT\\VC\\bes\\EOP_e_mdclbag01VC.BES";
	eqp[0].eqp = (rnd) ? "G\\EQUIPMENT\\VC\\eqp\\CVP_blckpjmsVC02\\vybaveni2\\EOP_e_mgznpouch01VC.eqp" : "G\\EQUIPMENT\\VC\\eqp\\CVP_blckpjmsVC02\\medic\\EOP_e_mdclbag01VC.eqp";
	*count++;

	rnd = rand() % 5;
	eqp[1].bes = (rnd) ? "G\\EQUIPMENT\\VC\\bes\\EOP_e_canteen01VC.BES" : NULL;
	eqp[1].eqp = (rnd) ? "G\\EQUIPMENT\\VC\\eqp\\CVP_blckpjmsVC02\\vybaveni1\\EOP_e_canteen01VC.eqp" : NULL;

	if (rnd)
		*count++;
}

