#include <inc\sc_global.h>
#include <inc\sc_def.h>

#define GGROUP 0

dword gphase = 0;

int ScriptMain(s_SC_P_info *info){
	s_SC_P_Create pinfo;
	s_SC_P_CreateEqp eqp[10];
	
		
	if (info->message!=SC_P_MES_TIME) return FALSE;

	info->next_exe_time = 0.2f;	

	if (gphase==0){				

		CLEAR(pinfo);pinfo.type = SC_P_TYPE_AI;
		pinfo.side = SC_P_SIDE_VC;
		pinfo.group = GGROUP;
		pinfo.member_id = MEMBERID;
		pinfo.inifile = INIFILENAME;
		pinfo.name_nr = 2506;
		pinfo.icon_name = "nhut";


		pinfo.weap_knife = 0;
		pinfo.weap_pistol = 0;
		pinfo.weap_main1 = PWEAPON1;
		pinfo.weap_main2 = PWEAPON2;
		pinfo.weap_slot1=PSLOT1;


		pinfo.recover_pos = info->pos;						
		CLEAR(eqp);
		pinfo.eqps = 0; 
		pinfo.eqp=eqp;  		

		pinfo.debrief_group=SC_P_DEBRIEFGROUP_VC;		


		gphase = 1;
	}// if (gphase==0)
	
	
	if (!SC_P_IsReady(info->pl_id)) {
		info->next_exe_time=0.05f;
		return 0;
	}
	
	
	switch(gphase){
	case 1:		

			SC_P_Ai_SetMode(info->pl_id,SC_P_AI_MODE_BATTLE);
			SC_P_Ai_EnableShooting(info->pl_id,TRUE);	
			SC_P_SetSpeachDist(info->pl_id,30);
			gphase = 2;
			break;
	case 2:
			break;			
	
	}
	return 1;
}
