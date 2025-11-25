//standard player script

#include <inc\us_equips.inc>

dword gphase = 0;

void equipplayer(s_SC_P_CreateEqp *eqp, int *count){
	Equip_BANGS_Full(eqp,count);
}

int ScriptMain(s_SC_P_info *info){
	s_SC_P_Create pinfo;
	s_SC_P_CreateEqp eqp[10];
	c_Vector3 vec,pl_pos;
	float time;
	int eqpcount;

	if (info->message!=SC_P_MES_TIME) return FALSE;	
	if (gphase==0){				

		CLEAR(pinfo);CLEAR(eqp);
		pinfo.type = SC_P_TYPE_PC;
		pinfo.side = SC_P_SIDE_US;
		pinfo.group = 0;
		pinfo.member_id = SC_P_MEMBERID_CAPTAIN;
		pinfo.inifile = "ini\\players\\default_camo.ini";
		pinfo.name_nr = 2500;
		
		pinfo.weap_knife = 0;
		pinfo.weap_pistol = 7;
		pinfo.weap_main1 = 23;
		pinfo.weap_main2 = 4;
		pinfo.weap_slot1 = 59;
		
		pinfo.recover_pos = info->pos;				
		equipplayer(eqp,&eqpcount); 
		pinfo.eqps = eqpcount; 
		pinfo.eqp=eqp;  
		info->pl_id = SC_P_Create(&pinfo);		
		gphase = 1;
	}
	info->next_exe_time = 0.1f;	

	if (!SC_P_IsReady(info->pl_id)){
		info->next_exe_time = 0.01f;
		return 1;		
	}

	switch(gphase){
	case 1:
		gphase = 2;
		SC_P_SetSpeachDist(info->pl_id, 20.0f);
		break;

	}// switch(gphase)
		
	return 1;

}// int ScriptMain(s_SC_P_info *info)