#define WEAPON_M16		1
#define WEAPON_AK47		2
#define WEAPON_SCORPION	3
#define WEAPON_M1		4
#define WEAPON_DP2		5
#define WEAPON_PPS41		6
#define WEAPON_M1911		7
#define WEAPON_TOKAREV		8
#define WEAPON_MAKAROV		9
#define WEAPON_REVOLVER	10
#define WEAPON_REMMINGTON	11
#define WEAPON_WINCHESTER	12
#define WEAPON_TOKAREVSVT	13
#define WEAPON_DRAGUNOV	14
#define WEAPON_SIMONOV		15
#define WEAPON_TOKAREVSNIPER	16
#define WEAPON_M60		17
#define WEAPON_DEGTAREV	18
#define WEAPON_USM3		19
#define WEAPON_THOMPSON	21
#define WEAPON_SW39		22
#define WEAPON_PPS43		23
#define WEAPON_M14		24
#define WEAPON_M1CARABINE	25
#define WEAPON_MOSIN		26
#define WEAPON_M79		27
#define WEAPON_SHOTGUN		28
#define WEAPON_M14SNIPER	31
#define WEAPON_STEN		32
#define WEAPON_MACHETTE	33

#define INI21			"ini\\players\\vcfighter2.ini"
#define INI22			"ini\\players\\vcfighter3.ini"
#define INI23			"ini\\players\\vcfighter4.ini"
#define INI24			"ini\\players\\nvaofficer.ini"
#define INI25			"ini\\players\\nvasoldier2.ini"
#define INI26			"ini\\players\\nvasoldier3.ini"
#define INI27			"ini\\players\\poorvc.ini"
#define INI28			"ini\\players\\poorvc2.ini"
#define INI29			"ini\\players\\poorvc3.ini"
#define INI30			"ini\\players\\vcuniform1.ini"
#define INI31			"ini\\players\\vcuniform2.ini"
#define INI32			"ini\\players\\vcuniform3.ini"
#define INI67			"ini\\players\\nvacolonel.ini"
#define INI68			"ini\\players\\poorvc4.ini"
#define INI69			"ini\\players\\vcfighter5.ini"
#define INI70			"ini\\players\\vcuniform4.ini"
#define INI71			"ini\\players\\nvasoldier4.ini"


void Set_VC_BOMB23_1(s_SC_P_Create *info){
	info->inifile=INI23;
	info->weap_main1=WEAPON_PPS41;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohlmt1VC_CAMO.bes";
    info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH02_01.eqp";
	
	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-1\\EOP_e_mgznpouch01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-1\\EOP_e_canteen01_0.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-1\\EOP_e_canteen01.eqp";

	info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-1\\EOP_e_bigbag01VC.eqp";
	
	info->eqps=5;
}

void Set_VC_BOMB23_2(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_DP2;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH03_01.eqp";

    info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-2\\EOP_e_canteen01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-2\\EOP_e_bigbag01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-2\\EOP_e_mgznpouch01VC.eqp";

    info->eqps=4;
}

void Set_VC_BOMB23_3(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_M1CARABINE;
  
    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohat1VC.bes";
    info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH15_01.eqp";

    info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_shovel01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-3\\EOP_e_shovel01.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-3\\EOP_e_m16ammobox01_0.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-3\\EOP_e_m16ammobox01.eqp";

	info->eqp[4].bes = "G\\EQUIPMENT\\Us\\vybaveni2\\EOP_e_canteen01.bes";
	info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-3\\EOP_e_canteen01.eqp";

	info->eqp[5].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes ";
	info->eqp[5].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-3\\EOP_e_bigbag01VC.eqp";

    info->eqps=6;
}

void Set_VC_BOMB23_4(s_SC_P_Create *info){
 info->inifile=INI23;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohlmt1VC_CAMO.bes";
    info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH02_01.eqp";

    info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_shovel01.bes ";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-4\\EOP_e_shovel01.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-4\\EOP_e_m16ammobox01_0.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-4\\EOP_e_m16ammobox01.eqp";

	info->eqp[4].bes = "G\\EQUIPMENT\\Us\\vybaveni2\\EOP_e_canteen01.bes";
	info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-4\\EOP_e_canteen01.eqp";

	info->eqp[5].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes ";
	info->eqp[5].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-4\\EOP_e_bigbag01VC.eqp";

    info->eqps=6;
}

void Set_VC_BOMB23_5(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_PPS41;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH03_01.eqp";

    info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-5\\EOP_e_canteen01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-5\\EOP_e_bigbag01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-5\\EOP_e_mgznpouch01VC.eqp";

    info->eqps=4;
}


void Set_VC_BOMB23_sniper(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_TOKAREVSNIPER;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH03_01.eqp";

    info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-5\\EOP_e_canteen01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-5\\EOP_e_bigbag01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-5\\EOP_e_mgznpouch01VC.eqp";

    info->eqps=4;
}

void Set_VC_BOMB23_6(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_M1CARABINE;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohat1VC.bes";
    info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH15_01.eqp";

    info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_littlebag01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-6\\EOP_e_littlebag01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes ";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-6\\EOP_e_m16ammobox01_0.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-6\\EOP_e_bigbag01VC.eqp";

	info->eqp[4].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\BOMB23-6\\EOP_e_canteen01.eqp";

    info->eqps=5;

}

void Set_VC_BOMB21_1(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-1\\EOP_e_bigbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-1\\EOP_e_canteen01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_littlebag01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-1\\EOP_e_littlebag01.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-1\\EOP_e_m16ammobox01.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohlmt1VC_CAMO.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH02_01.eqp";

    info->eqps=5;

}

void Set_VC_BOMB21_2(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_PPS41;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-2\\EOP_e_mgznpouch01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_shovel01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-2\\EOP_e_shovel01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-2\\EOP_e_bigbag01VC.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-2\\EOP_e_canteen01.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH03_01.eqp";

    info->eqps=5;

}

void Set_VC_BOMB21_3(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_PPS41;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-3\\EOP_e_mdclbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-3\\EOP_e_mgznpouch01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-3\\EOP_e_canteen01VC.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-3\\EOP_e_bigbag01VC.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohat1VC.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH15_01.eqp";

    info->eqps=5;

}

void Set_VC_BOMB21_4(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_DP2;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-4\\EOP_e_mgznpouch01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-4\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-4\\EOP_e_bigbag01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohlmt1VC_CAMO.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH02_01.eqp";

    info->eqps=4;
}

void Set_VC_BOMB21_5(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_M1CARABINE;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-5\\EOP_e_bigbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-5\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-5\\EOP_e_canteen01VC_0.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-5\\EOP_e_m16ammobox01.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH03_01.eqp";

    info->eqps=5;
}

void Set_VC_BOMB21_6(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-6\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-6\\EOP_e_bigbag01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-6\\EOP_e_m16ammobox01.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\BOMB21-6\\EOP_e_m16ammobox01_0.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=5;
}

void Set_VC_BOMB69_1(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_M1CARABINE;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-1\\EOP_e_bigbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-1\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-1\\EOP_e_canteen01VC_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH03_01.eqp";

    info->eqps=4;

}

void Set_VC_BOMB69_2(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-2\\EOP_e_canteen01_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-2\\EOP_e_canteen01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-2\\EOP_e_bigbag01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohat1VC.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH15_01.eqp";

    info->eqps=4;

}

void Set_VC_BOMB69_3(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_M1CARABINE;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-3\\EOP_e_bigbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-3\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-3\\EOP_e_mdclbag01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH04_01.eqp";

    info->eqps=4;

}

void Set_VC_BOMB69_4(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_shovel01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-4\\EOP_e_shovel01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-4\\EOP_e_bigbag01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-4\\EOP_e_canteen01VC.eqp";
 
    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohlmt1VC_CAMO.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH02_01.eqp";

    info->eqps=4;

}

void Set_VC_BOMB69_5(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_M1CARABINE;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-5\\EOP_e_canteen01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-5\\EOP_e_bigbag01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohat1VC.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH15_01.eqp";

    info->eqps=3;
}

void Set_VC_BOMB69_6(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_littlebag01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-6\\EOP_e_littlebag01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-6\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\BOMB69-6\\EOP_e_bigbag01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH03_01.eqp";

    info->eqps=4;

}

void Set_VC_BOMB30_1(s_SC_P_Create *info){
    info->inifile=INI30;
	info->weap_main1=WEAPON_M1911;
  
    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\BOMB30_1\\EOP_e_ammoboxfp01_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\BOMB30_1\\EOP_e_ammoboxfp01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\BOMB30_1\\EOP_e_pistolcase01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOQ_ksiltovkaVC.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH09_01.eqp";

    info->eqps=4;

}

void Set_VC_JAR23_1(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_PPS41;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-1\\EOP_e_canteen01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-1\\EOP_e_canteen01_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-1\\EOP_e_mgznpouch01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohlmt1VC_CAMO.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH02_01.eqp";

    info->eqps=4;

}

void Set_VC_JAR23_2(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_DP2;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-2\\EOP_e_canteen01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-2\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-2\\EOP_e_mgznpouch01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH03_01.eqp";

    info->eqps=4;
    
}

void Set_VC_JAR23_3(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-3\\EOP_e_m16ammobox01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-3\\EOP_e_m16ammobox01_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_littlebag01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-3\\EOP_e_littlebag01.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-3\\EOP_e_canteen01_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohat1VC.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH15_01.eqp";

    info->eqps=4;

}

void Set_VC_JAR23_4(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_PPS43;
 
    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-4\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-4\\EOP_e_m16ammobox01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\JAR23-4\\EOP_e_m16ammobox01_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohlmt1VC_CAMO.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH02_01.eqp";

    info->eqps=3;

}

void Set_VC_JAR21_1(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_PPS41;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\JAR21-1\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\JAR21-1\\EOP_e_mdclbag01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\JAR21-1\\EOP_e_mgznpouch01VC.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH03_01.eqp";

    info->eqps=3;
}

void Set_VC_JAR21_2(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_DP2;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\JAR21-2\\EOP_e_mgznpouch01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\JAR21-2\\EOP_e_mgznpouch01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\JAR21-2\\EOP_e_canteen01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=4;

}

void Set_VC_JAR21_3(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_PPS43;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\JAR21-3\\EOP_e_mdclbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\JAR21-3\\EOP_e_m16ammobox01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\JAR21-3\\EOP_e_canteen01VC_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";
    
    info->eqps=4;
}

void Set_VC_JAR69_1(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\JAR69-1\\EOP_e_canteen01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\JAR69-1\\EOP_e_canteen01_0.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=3;
}

void Set_VC_JAR69_2(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\JAR69-2\\EOP_e_canteen01VC_0.eqp";

    info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohlmt1VC_CAMO.bes";
    info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH02_01.eqp";

    info->eqps=2;

}

void Set_VC_HAN23_1(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-1\\EOP_e_m16ammobox01_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-1\\EOP_e_m16ammobox01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-1\\EOP_e_canteen01_0.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-1\\EOP_e_canteen01.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH04_01.eqp";

    info->eqps=5;
}

void Set_VC_HAN30_1(s_SC_P_Create *info){
    info->inifile=INI30;
	info->weap_main1=WEAPON_DP2;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\HAN30-1\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\HAN30-1\\EOP_e_mgznpouch01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\HAN30-1\\EOP_e_mgznpouch01VC_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH04_01.eqp";

    info->eqps=4;
    
}

void Set_VC_HAN21_1(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_TOKAREVSVT;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\HAN21-1\\EOP_e_m16ammobox01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\HAN21-1\\EOP_e_m16ammobox01_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\HAN21-1\\EOP_e_canteen01VC_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=4;

}

void Set_VC_HAN23_2(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-2\\EOP_e_m16ammobox01_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-2\\EOP_e_m16ammobox01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-2\\EOP_e_canteen01_0.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-2\\EOP_e_canteen01.eqp";

	info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-2\\EOP_e_bigbag01VC.eqp";

    info->eqp[5].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohat1VC.bes";
    info->eqp[5].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH15_01.eqp";

    info->eqps=5;

}

void Set_VC_HAN23_3(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_M1CARABINE;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-3\\EOP_e_m16ammobox01_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-3\\EOP_e_m16ammobox01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-3\\EOP_e_canteen01_0.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-3\\EOP_e_bigbag01VC.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohlmt1VC_CAMO.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH02_01.eqp";

    info->eqps=5;
}

void Set_VC_HAN23_4(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_PPS41;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-4\\EOP_e_mgznpouch01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-4\\EOP_e_mgznpouch01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-4\\EOP_e_canteen01_0.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-4\\EOP_e_bigbag01VC.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH03_01.eqp";

    info->eqps=5;

}

void Set_VC_HAN23_5(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_DP2;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-5\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-5\\EOP_e_canteen01VC_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-5\\EOP_e_bigbag01VC.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\HAN23-5\\EOP_e_mgznpouch01VC.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohat1VC.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH15_01.eqp";

    info->eqps=5;

}

void Set_VC_HAN21_2(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_PPS41;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\HAN21-2\\EOP_e_bigbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\HAN21-2\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\HAN21-2\\EOP_e_mgznpouch01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH03_01.eqp";

    info->eqps=4;
    
}

void Set_VC_HAN69_1(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\HAN69-1\\EOP_e_bigbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\HAN69-1\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\HAN69-1\\EOP_e_canteen01VC_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohat1VC.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH15_01.eqp";

    info->eqps=4;
    
}

void Set_VC_HAN69_2(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_MOSIN;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_bigbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\HAN69-2\\EOP_e_bigbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\HAN69-2\\EOP_e_canteen01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\HAN69-2\\EOP_e_canteen01_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH03_01.eqp";

    info->eqps=4;

}

void Set_VC_HAN30_2(s_SC_P_Create *info){
    info->inifile=INI30;
	info->weap_main1=WEAPON_M1911;
  
    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\HAN30-2\\EOP_e_ammoboxfp01_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\HAN30-2\\EOP_e_ammoboxfp01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\HAN30-2\\EOP_e_pistolcase01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOQ_ksiltovkaVC.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH09_01.eqp";

    info->eqps=4;

}

void Set_VC_HAN21_3(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_DP2;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\HAN21-3\\EOP_e_mgznpouch01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\HAN21-3\\EOP_e_canteen01VC_0.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohlmt1VC_CAMO.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH02_01.eqp";

    info->eqps=3;
    
}

void Set_VC_HAN21_4(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_TOKAREVSVT;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\HAN21-4\\EOP_e_canteen01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\HAN21-4\\EOP_e_m16ammobox01.eqp";

    info->eqps=2;

}

void Set_VC_HAN31_1(s_SC_P_Create *info){
    info->inifile=INI31;
	info->weap_main1=WEAPON_PPS43;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\HAN31-1\\EOP_e_m16ammobox01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\HAN31-1\\EOP_e_canteen01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=3;

}

void Set_VC_HAN31_2(s_SC_P_Create *info){
    info->inifile=INI31;
	info->weap_main1=WEAPON_TOKAREVSVT;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\HAN31-2\\EOP_e_canteen01_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\HAN31-2\\EOP_e_canteen01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\HAN31-2\\EOP_e_m16ammobox01.eqp";

    info->eqps=3;
}

void Set_VC_HAN31_3(s_SC_P_Create *info){
    info->inifile=INI31;
	info->weap_main1=WEAPON_PPS43;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\HAN31-3\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_littlebag01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\HAN31-3\\EOP_e_littlebag01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\HAN31-3\\EOP_e_m16ammobox01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=4;
}

void Set_VC_HAN70_1(s_SC_P_Create *info){
    info->inifile=INI70;
	info->weap_main1=WEAPON_TOKAREVSVT;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\HAN70-1\\EOP_e_mgznpouch01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\HAN70-1\\EOP_e_canteen01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH04_01.eqp";

    info->eqps=3;
}

void Set_VC_HAN70_2(s_SC_P_Create *info){
    info->inifile=INI70;
	info->weap_main1=WEAPON_PPS43;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\HAN70-2\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\HAN70-2\\EOP_e_mdclbag01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\HAN70-2\\EOP_e_mgznpouch01VC.eqp";

    info->eqps=3;

}

void Set_VC_HAN70_3(s_SC_P_Create *info){
    info->inifile=INI70;
	info->weap_main1=WEAPON_TOKAREVSVT;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\HAN70-3\\EOP_e_m16ammobox01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\HAN70-3\\EOP_e_m16ammobox01_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\HAN70-3\\EOP_e_canteen01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH04_01.eqp";

    info->eqps=3;

}

void Set_VC_MIN30_1(s_SC_P_Create *info){
    info->inifile=INI30;
	info->weap_main1=WEAPON_M1911;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\MIN30-1\\EOP_e_ammoboxfp01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\MIN30-1\\EOP_e_pistolcase01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\MIN30-1\\EOP_e_ammoboxfp01_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOQ_ksiltovkaVC.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH09_01.eqp";

    info->eqps=4;
    
}

void Set_VC_MIN24_1(s_SC_P_Create *info){
    info->inifile=INI24;
	info->weap_main1=WEAPON_MAKAROV;
}

void Set_VC_MIN25_1(s_SC_P_Create *info){
    info->inifile=INI25;
	info->weap_main1=WEAPON_MAKAROV;

   
}
 
void Set_VC_MIN70_1(s_SC_P_Create *info){
    info->inifile=INI70;
	info->weap_main1=WEAPON_MAKAROV;

}

void Set_VC_MIN21_1(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\MIN21-1\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\MIN21-1\\EOP_e_canteen01VC_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\MIN21-1\\EOP_e_m16ammobox01_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH03_01.eqp";

    info->eqps=4;

}

void Set_VC_MIN21_1Sniper(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_DRAGUNOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\MIN21-1\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\MIN21-1\\EOP_e_canteen01VC_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\MIN21-1\\EOP_e_m16ammobox01_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH03_01.eqp";

    info->eqps=4;

}

void Set_VC_MIN21_2(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_TOKAREVSVT;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\MIN21-2\\EOP_e_canteen01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\MIN21-2\\EOP_e_m16ammobox01_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\MIN21-2\\EOP_e_m16ammobox01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=4;
}

void Set_VC_MIN32_1(s_SC_P_Create *info){
    info->inifile=INI32;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC03\\MIN32-1\\EOP_e_canteen01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC03\\MIN32-1\\EOP_e_canteen01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH03_01.eqp";

    info->eqps=2;

}

void Set_VC_MIN32_1Sniper(s_SC_P_Create *info){
    info->inifile=INI32;
	info->weap_main1=WEAPON_TOKAREVSNIPER;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC03\\MIN32-1\\EOP_e_canteen01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC03\\MIN32-1\\EOP_e_canteen01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH03_01.eqp";

    info->eqps=2;

}

void Set_VC_MIN32_2(s_SC_P_Create *info){
    info->inifile=INI32;
	info->weap_main1=WEAPON_TOKAREVSVT;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC03\\MIN32-2\\EOP_e_mdclbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC03\\MIN32-2\\EOP_e_canteen01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH04_01.eqp";
    
    info->eqps=2;

}

void Set_VC_MIN71_1(s_SC_P_Create *info){
    info->inifile=INI71;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes ";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\MIN71-1\\EOP_e_mdclbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\MIN71-1\\EOP_e_canteen01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH03_01.eqp";

    info->eqps=3;

}

void Set_VC_MIN71_1Sniper(s_SC_P_Create *info){
    info->inifile=INI71;
	info->weap_main1=WEAPON_TOKAREVSNIPER;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes ";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\MIN71-1\\EOP_e_mdclbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\MIN71-1\\EOP_e_canteen01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH03_01.eqp";

    info->eqps=3;

}

void Set_VC_MIN71_2(s_SC_P_Create *info){
    info->inifile=INI71;
	info->weap_main1=WEAPON_TOKAREVSVT;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\MIN71-2\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\MIN71-2\\EOP_e_canteen01VC_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\MIN71-2\\EOP_e_mdclbag01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH04_01.eqp";

    info->eqps=4;

}

void Set_VC_BAS25_1(s_SC_P_Create *info){
    info->inifile=INI25;
	info->weap_main1=WEAPON_M1911;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\BAS25-1\\EOP_e_ammoboxfp01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\BAS25-1\\EOP_e_ammoboxfp01_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\BAS25-1\\EOP_e_canteen01VC.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\BAS25-1\\EOP_e_pistolcase01.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOQ_ksiltovkaVC.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH09_01.eqp";

    info->eqps=5;
}

void Set_VC_BAS25_2(s_SC_P_Create *info){
    info->inifile=INI25;
	info->weap_main1=WEAPON_MAKAROV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\BAS25-2\\EOP_e_ammoboxfp01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\BAS25-2\\EOP_e_ammoboxfp01_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\BAS25-2\\EOP_e_canteen01VC.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\BAS25-2\\EOP_e_canteen01VC_0.eqp";

	info->eqp[4].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\BAS25-2\\EOP_e_pistolcase01.eqp";

    info->eqp[5].bes = "G\\EQUIPMENT\\Vc\\bes\\EOQ_ksiltovkaVC.bes";
    info->eqp[5].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH09_01.eqp";

    info->eqps=6;
    
}

void Set_VC_BAS26_1(s_SC_P_Create *info){
    info->inifile=INI26;
	info->weap_main1=WEAPON_AK47;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier03\\BAS26-1\\EOP_e_canteen01VC.eqp";

    info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH04_01.eqp";

    info->eqps=2;
   
}

void Set_VC_BAS26_2(s_SC_P_Create *info){
    info->inifile=INI26;
	info->weap_main1=WEAPON_AK47;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier03\\BAS26-2\\EOP_e_canteen01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier03\\BAS26-2\\EOP_e_canteen01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet1VC_CAMO.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH06_01.eqp";

    info->eqps=3;
}

void Set_VC_BAS31_1(s_SC_P_Create *info){
    info->inifile=INI31;
	info->weap_main1=WEAPON_DEGTAREV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-1\\EOP_e_mgznpouch01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-1\\EOP_e_mdclbag01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-1\\EOP_e_canteen01VC.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=4;

}

void Set_VC_BAS31_2(s_SC_P_Create *info){
    info->inifile=INI31;
	info->weap_main1=WEAPON_TOKAREVSNIPER;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-2\\EOP_e_mdclbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-2\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-2\\EOP_e_m16ammobox01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet1VC_CAMO.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH06_01.eqp";

    info->eqps=3;

}

void Set_VC_BAS31_3(s_SC_P_Create *info){
    info->inifile=INI31;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_vc_radioear01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-3\\EOP_vc_radioear01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOJ_vc_radio_3pv.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-3\\EOJ_vc_radio_3pv.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-3\\EOP_e_mdclbag01VC.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-3\\EOP_e_canteen01VC.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=5;

}

void Set_VC_BAS32_1(s_SC_P_Create *info){
    info->inifile=INI32;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC03\\BAS32-1\\EOP_e_canteen01VC.eqp";

    info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet1VC_CAMO.bes";
    info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH06_01.eqp";

    info->eqps=2;

}

void Set_VC_BAS32_2(s_SC_P_Create *info){
    info->inifile=INI32;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC03\\BAS32-2\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC03\\BAS32-2\\EOP_e_mdclbag01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH04_01.eqp";

    info->eqps=3;
}

void Set_VC_BAS71_1(s_SC_P_Create *info){
    info->inifile=INI71;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\BAS71-1\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\BAS71-1\\EOP_e_canteen01VC_0.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet1VC_CAMO.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH06_01.eqp";

    info->eqps=3;
}

void Set_VC_BAS71_2(s_SC_P_Create *info){
    info->inifile=INI71;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\BAS71-2\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\BAS71-2\\EOP_e_mdclbag01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH04_01.eqp";

    info->eqps=3;

}

void Set_VC_BAS30_1(s_SC_P_Create *info){
    info->inifile=INI31;
	info->weap_main1=WEAPON_MAKAROV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\BAS30-1\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\BAS30-1\\EOP_e_pistolcase01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\BAS30-1\\EOP_e_ammoboxfp01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet1VC_CAMO.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH06_01.eqp";

    info->eqps=4;
    
}

void Set_VC_BAS31_4(s_SC_P_Create *info){
    info->inifile=INI31;
	info->weap_main1=WEAPON_MAKAROV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-4\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-4\\EOP_e_pistolcase01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\BAS31-4\\EOP_e_ammoboxfp01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=4;
}


void Set_VC_KAM31_1(s_SC_P_Create *info){
    info->inifile=INI31;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\KAM31-1\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\KAM31-1\\EOP_e_pistolcase01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\KAM31-1\\EOP_e_ammoboxfp01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet2VC_CAMO.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH14_01.eqp";

    info->eqps=4;

}

void Set_VC_KAM31_2(s_SC_P_Create *info){
    info->inifile=INI31;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\KAM31-2\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC02\\KAM31-2\\EOP_e_mgznpouch01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=3;
}

void Set_VC_KAM30_1(s_SC_P_Create *info){
    info->inifile=INI30;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\KAM30-1\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\KAM30-1\\EOP_e_mdclbag01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet2VC.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH13_01.eqp";

    info->eqps=3;

}

void Set_VC_KAM30_2(s_SC_P_Create *info){
    info->inifile=INI30;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\KAM30-2\\EOP_e_canteen01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC01\\KAM30-2\\EOP_e_canteen01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet2VC_CAMO.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH14_01.eqp";

    info->eqps=3;

}

void Set_VC_KAM_Radist(s_SC_P_Create *info){
    info->inifile=INI71;
	info->weap_main1=WEAPON_MAKAROV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_VC_ears.BES";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\EOP_VC_ears01.eqp";

    info->eqps=1;

}
void Set_VC_KAM71_1(s_SC_P_Create *info){
    info->inifile=INI71;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\KAM71-1\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\KAM71-1\\EOP_e_canteen01VC_0.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet1VC.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH05_01.eqp";

    info->eqps=3;

}

void Set_VC_KAM71_2(s_SC_P_Create *info){
    info->inifile=INI71;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\KAM71-2\\EOP_e_canteen01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\KAM71-2\\EOP_e_mdclbag01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet1VC_CAMO.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH06_01.eqp";

    info->eqps=3;
}

void Set_VC_KAM26_1(s_SC_P_Create *info){
    info->inifile=INI26;
	info->weap_main1=WEAPON_AK47;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier03\\KAM26-1\\EOP_e_mdclbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier03\\KAM26-1\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier03\\KAM26-1\\EOP_e_canteen01VC_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet1VC_CAMO.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH06_01.eqp";

    info->eqps=4;

}

void Set_VC_KAM26_2(s_SC_P_Create *info){
    info->inifile=INI26;
	info->weap_main1=WEAPON_AK47;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier03\\KAM26-2\\EOP_e_canteen01VC.eqp";

    info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet1VC.bes";
    info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH07PH05_01.eqp";

    info->eqps=2;
}

void Set_VC_KAM71_3(s_SC_P_Create *info){
    info->inifile=INI71;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\KAM71-3\\EOP_e_canteen01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\KAM71-3\\EOP_e_canteen01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet2VC.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH13_01.eqp";

    info->eqps=3;
}

void Set_VC_KAM71_4(s_SC_P_Create *info){
    info->inifile=INI71;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mdclbag01VC.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\KAM71-4\\EOP_e_mdclbag01VC.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier04\\KAM71-4\\EOP_e_canteen01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_helmet2VC_CAMO.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH14_01.eqp";

    info->eqps=3;
}

void Set_VC_KAM25_1(s_SC_P_Create *info){
    info->inifile=INI25;
	info->weap_main1=WEAPON_M1911;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\KAM25-1\\EOP_e_ammoboxfp01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\KAM25-1\\EOP_e_pistolcase01.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\KAM25-1\\EOP_e_ammoboxfp01_0.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAsoldier02\\KAM25-1\\EOP_e_canteen01VC.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOQ_ksiltovkaVC.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_EOP_VH08PH09_01.eqp";

    info->eqps=5;

}

void Set_VC_KAM24_1(s_SC_P_Create *info){
    info->inifile=INI24;
    info->weap_main1=WEAPON_MAKAROV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOQ_ksiltovkaVC.bes";
    info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH09_01.eqp"; 

    info->eqps=1;
    
}

void Set_VC_KAM70_1(s_SC_P_Create *info){
    info->inifile=INI70;
    info->weap_main1=WEAPON_MAKAROV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\KAM70-1\\EOP_e_pistolcase01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\KAM70-1\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_uniformVC04\\KAM70-1\\EOP_e_ammoboxfp01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOQ_ksiltovkaVC.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH09_01.eqp"; 

    info->eqps=4;
}

void Set_VC_KAM23_1(s_SC_P_Create *info){
    info->inifile=INI23;
	info->weap_main1=WEAPON_PPS41;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_mgznpouch01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\KAM23-1\\EOP_e_mgznpouch01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\KAM23-1\\EOP_e_canteen01VC.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC04\\KAM23-1\\EOP_e_canteen01VC_0.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_bmbohat1VC.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH08PH15_01.eqp";

    info->eqps=4;
}

void Set_VC_KAM21_1(s_SC_P_Create *info){
    info->inifile=INI21;
	info->weap_main1=WEAPON_SIMONOV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\KAM21-1\\EOP_e_canteen01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_canteen01_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\KAM21-1\\EOP_e_canteen01_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_m16ammobox01.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC02\\KAM21-1\\EOP_e_m16ammobox01.eqp";

    info->eqp[3].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_KHKI.bes";
    info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH06PH04_01.eqp";

    info->eqps=4;
}

void Set_VC_KAM69_1(s_SC_P_Create *info){
    info->inifile=INI69;
	info->weap_main1=WEAPON_M1;

    info->eqp[0].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC_0.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\KAM69-1\\EOP_e_canteen01VC_0.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_blckpjmsVC05\\KAM69-1\\EOP_e_canteen01VC.eqp";

    info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_hat1VC_BLCK.bes";
    info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH11PH03_01.eqp";

    info->eqps=3;
}

void Set_VC_KAM67_1(s_SC_P_Create *info){
    info->inifile=INI67;
    info->weap_main1=WEAPON_MAKAROV;

    info->eqp[0].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01.bes";
	info->eqp[0].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAcolonel\\KAM67-1\\EOP_e_ammoboxfp01.eqp";

	info->eqp[1].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_ammoboxfp01_0.bes";
	info->eqp[1].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAcolonel\\KAM67-1\\EOP_e_ammoboxfp01_0.eqp";

	info->eqp[2].bes = "G\\EQUIPMENT\\Vc\\bes\\EOP_e_canteen01VC.bes";
	info->eqp[2].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAcolonel\\KAM67-1\\EOP_e_canteen01VC.eqp";

	info->eqp[3].bes = "G\\EQUIPMENT\\Us\\bes\\EOP_e_pistolcase01.bes";
	info->eqp[3].eqp = "G\\EQUIPMENT\\Vc\\eqp\\CVP_NVAcolonel\\KAM67-1\\EOP_e_pistolcase01.eqp";

    info->eqp[4].bes = "G\\EQUIPMENT\\Vc\\bes\\EOQ_ksiltovkaVC.bes";
    info->eqp[4].eqp = "G\\EQUIPMENT\\Vc\\eqp\\EOP_VH10PH09_01.eqp";

    info->eqps=5;

}



//funkce pro vygenerování obecného panáka (speciální se nepoèítají)
/*param:		0	1	2	3	4	5	6	7
BOMBERPILOT 	obecny	kulomet	sniper	dustojnik
JARAI		obecny	kulomet	kulomet2
HANGING	hlidka 	walkers	dustojnik	most 	kulomet	sniper
MINEFACTORY	velitel	poradci	vojaci	sniper
BASEATTACK	dustojnik	vojaci	snipers	minomety
DV/NVA		obecny	hlidka	tabornici	dustojnici	stopari	plukovnik	obsluha	radista
*/

void Set_FISTALPHA_VC(s_SC_P_Create *info, int param){
	int eq=999;
	


	switch(SC_ggi(SGI_CURRENTMISSION)){

	case MISSION_BOMBERPILOT:
		switch (param){
		case 0:			
		
		eq=rand()%17;
		switch (eq){
		case 0:
			Set_VC_BOMB23_1(info);
			break;
		case 1:
			Set_VC_BOMB69_6(info);
			break;
		case 2:
			Set_VC_BOMB23_3(info);
			break;
		case 3:
			Set_VC_BOMB23_4(info);
			break;
		case 4:
			Set_VC_BOMB23_5(info);
			break;
		case 5:
			Set_VC_BOMB23_6(info);
			break;
		case 6:
			Set_VC_BOMB21_1(info);
			break;
		case 7:
			Set_VC_BOMB21_2(info);
			break;
		case 8:
			Set_VC_BOMB21_3(info);
			break;
		case 9:
			Set_VC_BOMB21_4(info);
			break;
		case 10:
			Set_VC_BOMB21_5(info);
			break;
		case 11:
			Set_VC_BOMB21_6(info);
			break;
		case 12:
			Set_VC_BOMB69_1(info);
			break;
		case 13:
			Set_VC_BOMB69_2(info);
			break;
		case 14:
			Set_VC_BOMB69_3(info);
			break;
		case 15:
			Set_VC_BOMB69_4(info);
			break;
		case 16:
			Set_VC_BOMB69_5(info);
			break;
		}
			break;
		case 1:
			Set_VC_BOMB23_2(info);
			break;
		case 2:
			Set_VC_BOMB23_sniper(info);
			break;			
		case 3:
			Set_VC_BOMB30_1(info);
			break;
		}

		break;	

	case MISSION_JARAI:
		if (param==1){		//kulometcik
			Set_VC_JAR23_2(info);
			SC_Log(3,"Equipped VC for the mission %d, enemytype %d with variant %d",SC_ggi(SGI_CURRENTMISSION),param,eq);
			return;
		}
		if (param==2){		//kulometcik verze 2
			Set_VC_BOMB21_2(info);
			SC_Log(3,"Equipped VC for the mission %d, enemytype %d with variant %d",SC_ggi(SGI_CURRENTMISSION),param,eq);
			return;
		}

		eq=rand()%7;
		switch (eq){
		case 0:
			Set_VC_JAR23_1(info);
			break;
		case 1:
			Set_VC_JAR23_3(info);
			break;
		case 2:
			Set_VC_JAR23_4(info);
			break;
		case 3:
			Set_VC_JAR21_1(info);
			break;
		case 4:
			Set_VC_JAR21_3(info);
			break;
		case 5:
			Set_VC_JAR69_1(info);
			break;
		case 6:
			Set_VC_JAR69_2(info);
			break;
		}
		break;
		
	case MISSION_HANGINGBRIDGE:
		switch (param){
		case 0:			//hlidka
			eq=rand()%3;
			switch (eq){
			case 0:
				Set_VC_HAN23_1(info);
				break;
			case 1:
				Set_VC_HAN30_1(info);
				break;
			case 2:
				Set_VC_HAN21_1(info);
				break;			
			}
			break;
		case 1:			//walkers
			eq=rand()%7;
			switch (eq){
			case 0:
				Set_VC_HAN23_2(info);
				break;
			case 1:
				Set_VC_HAN23_3(info);
				break;
			case 2:
				Set_VC_HAN23_4(info);
				break;
			case 3:
				Set_VC_HAN23_5(info);
				break;
			case 4:
				Set_VC_HAN21_2(info);
				break;
			case 5:
				Set_VC_HAN69_1(info);
				break;
			case 6:
				Set_VC_HAN69_2(info);
				break;
			}
			break;
		case 2:			//officer
			Set_VC_HAN30_2(info);
			break;
		case 3:			//bridge force
			eq=rand()%7;
			switch (eq){
			case 0:
				Set_VC_HAN70_2(info);
				break;
			case 1:
				Set_VC_HAN21_4(info);
				break;
			case 2:
				Set_VC_HAN31_1(info);
				break;
			case 3:
				Set_VC_HAN31_2(info);
				break;
			case 4:
				Set_VC_HAN31_3(info);
				break;
			case 5:
				Set_VC_HAN70_1(info);
				break;
			case 6:
				Set_VC_HAN70_2(info);
				break;
			}
			break;
		case 4:			//mg
			Set_VC_HAN21_3(info);
			break;
		case 5:
			Set_VC_HAN70_3(info);
			break;
		}
		break;

	case MISSION_MINEFACTORY:
		switch (param){
		case 0:			//velitel
			Set_VC_MIN30_1(info);
			break;
		case 1:			//poradci
			eq=rand()%3;
			switch (eq){
			case 0:
				Set_VC_MIN24_1(info);
				break;
			case 1:
				Set_VC_MIN25_1(info);
				break;
			case 2:
				Set_VC_MIN70_1(info);
				break;
			}
			break;
		case 2:			//vojaci
			eq=rand()%6;
			switch (eq){
			case 0:
				Set_VC_MIN21_1(info);
				break;
			case 1:
				Set_VC_MIN21_2(info);
				break;
			case 2:
				Set_VC_MIN32_1(info);
				break;
			case 3:
				Set_VC_MIN32_2(info);
				break;
			case 4:
				Set_VC_MIN71_1(info);
				break;
			case 5:
				Set_VC_MIN71_2(info);
				break;
			}
			break;
		case 3:
			eq=rand()%3;
			switch (eq){
			case 0:
				Set_VC_MIN21_1Sniper(info);
				break;
			case 1:
				Set_VC_MIN32_1Sniper(info);
				break;
			case 2:
				Set_VC_MIN71_1Sniper(info);
				break;
			}
			break;
		}
		break;

	case MISSION_BASEATTACK:
		switch (param){
		case 0:			//officers
			eq=rand()%2;
			if (eq) Set_VC_BAS25_1(info);
			 else Set_VC_BAS25_2(info);
			break;
		case 1:			//soldiers
			eq=rand()%8;
			switch (eq){
			case 0:
				Set_VC_BAS26_1(info);
				break;
			case 1:
				Set_VC_BAS26_2(info);
				break;
			case 2:
				Set_VC_BAS31_1(info);
				break;
			case 3:
				Set_VC_BAS31_3(info);
				break;
			case 4:
				Set_VC_BAS32_1(info);
				break;
			case 5:
				Set_VC_BAS32_2(info);
				break;
			case 6:
				Set_VC_BAS71_1(info);
				break;
			case 7:
				Set_VC_BAS71_2(info);
				break;
			}
			break;		
		case 2:			//snipers
			Set_VC_BAS31_2(info);
			break;		
		case 3:			//mortars
			eq=rand()%2;
			if (eq) Set_VC_BAS30_1(info);
			 else Set_VC_BAS31_4(info);
			break;		
		}
		break;

	case MISSION_DEATHVALLEYA:
	case MISSION_DEATHVALLEYB:
	case MISSION_NVACAMP:
		switch (param){
		case 0:
			eq=rand()%10;
			switch (eq){
			case 0:
				Set_VC_KAM26_1(info);
				break;
			case 1:
				Set_VC_KAM26_2(info);
				break;
			case 2:
				Set_VC_KAM71_3(info);
				break;
			case 3:
				Set_VC_KAM71_4(info);
				break;
			case 4:
				Set_VC_KAM71_1(info);
				break;
			case 5:
			 	Set_VC_KAM71_2(info);
				break;
			case 6:
				Set_VC_KAM31_1(info);
				break;
			case 7:
				Set_VC_KAM31_2(info);
				break;
			case 8:
				Set_VC_KAM30_1(info);
				break;
			case 9:
				Set_VC_KAM30_2(info);
				break;
			}
			break;
		case 1:			//hlidka
			eq=rand()%2;
			if (eq) Set_VC_KAM71_1(info);
			 else Set_VC_KAM71_2(info);
			break;
		case 2:			//tabornici
			eq=rand()%4;
			switch (eq){
			case 0:
				Set_VC_KAM26_1(info);
				break;
			case 1:
				Set_VC_KAM26_2(info);
				break;
			case 2:
				Set_VC_KAM71_3(info);
				break;
			case 3:
				Set_VC_KAM71_4(info);
				break;
			}
			break;
		case 3:			//dustonici
			eq=rand()%3;
			switch (eq){
			case 0:
				Set_VC_KAM24_1(info);
				break;
			case 1:
				Set_VC_KAM25_1(info);
				break;
			case 2:
				Set_VC_KAM70_1(info);
				break;
			}
			break;
		case 4:			//stopari
			eq=rand()%3;
			switch (eq){
			case 0:
				Set_VC_KAM23_1(info);
				break;
			case 1:
				Set_VC_KAM21_1(info);
				break;
			case 2:
				Set_VC_KAM69_1(info);
				break;
			}
			break;
		case 5:			//velitel
			Set_VC_KAM67_1(info);
			break;
		case 6:			//obsluha
			eq=rand()%4;
			switch (eq){
			case 0:
				Set_VC_KAM31_1(info);
				break;
			case 1:
				Set_VC_KAM31_2(info);
				break;
			case 2:
				Set_VC_KAM30_1(info);
				break;
			case 3:
				Set_VC_KAM30_2(info);
				break;
			}
			break;
		case 7:
			Set_VC_KAM_Radist(info);
			break;
		}		
		break;
	}
	SC_Log(3,"Equipped VC for the mission %d, enemytype %d with variant %d",SC_ggi(SGI_CURRENTMISSION),param,eq);
}

