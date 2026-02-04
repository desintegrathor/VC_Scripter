// Structured decompilation of DEFORT.SCR
// Functions: 51

#include "LEVEL_H.H"
#include <inc\sc_level.h>

void GetVCEquip(s_SC_P_Create * pinfo) {
    pinfo->field_40 = SC_ggi(PLAYER_WEAPON1);
    if (! tmp4) {
        pinfo->field_40 = 29;
    } else {
    }
    if (tmp8 == 255) {
        pinfo->field_40 = 0;
    }
    pinfo->field_44 = SC_ggi(PLAYER_WEAPON2);
    if (! tmp16) {
        pinfo->field_44 = 7;
    } else {
    }
    if (tmp20 == 255) {
        pinfo->field_44 = 0;
    }
    pinfo->field_48 = SC_ggi(PLAYER_WEAPON3);
    if (! tmp28) {
        if (SC_ggi(SGI_CURRENTMISSION) != 12) {
            if (SC_ggi(SGI_CURRENTMISSION) >= 12) {
                pinfo->field_48 = 1;
            } else {
                pinfo->field_48 = 25;
            }
        } else {
            pinfo->field_48 = 23;
        }
    } else {
    }
    if (tmp40 == 255) {
        pinfo->field_48 = 0;
    }
    pinfo->field_52 = SC_ggi(PLAYER_WEAPON4);
    if (tmp48 == 255) {
        pinfo->field_52 = 0;
    }
    pinfo->field_56 = SC_ggi(PLAYER_WEAPON5);
    if (! tmp56) {
        pinfo->field_56 = 59;
    } else {
    }
    if (tmp60 == 255) {
        pinfo->field_56 = 0;
    }
    pinfo->field_60 = SC_ggi(PLAYER_WEAPON6);
    if (tmp68 == 255) {
        pinfo->field_60 = 0;
    }
    pinfo->field_64 = SC_ggi(PLAYER_WEAPON7);
    if (tmp76 == 255) {
        pinfo->field_64 = 0;
    }
    pinfo->field_68 = SC_ggi(PLAYER_WEAPON8);
    if (! tmp84) {
        pinfo->field_68 = 63;
    } else {
    }
    if (tmp88 == 255) {
        pinfo->field_68 = 0;
    }
    pinfo->field_72 = SC_ggi(PLAYER_WEAPON9);
    if (tmp96 == 255) {
        pinfo->field_72 = 0;
    }
    pinfo->field_76 = 58;
    return;
}

void func_0276(void) {
    s_SC_P_Create pinfo;

    t280_ret = SC_PC_Get();
    t284_ret = SC_P_GetWeapons(t280_ret, &pinfo);
    if (! pinfo.weap_knife) {
        SC_sgi(PLAYER_WEAPON1, 255);
    } else {
        SC_sgi(PLAYER_WEAPON1, pinfo.weap_knife);
    }
    if (! pinfo.weap_pistol) {
        SC_sgi(PLAYER_WEAPON2, 255);
    } else {
        SC_sgi(PLAYER_WEAPON2, pinfo.weap_pistol);
    }
    if (! pinfo.weap_main1) {
        SC_sgi(PLAYER_WEAPON3, 255);
    } else {
        SC_sgi(PLAYER_WEAPON3, pinfo.weap_main1);
    }
    if (! pinfo.weap_main2) {
        SC_sgi(PLAYER_WEAPON4, 255);
    } else {
        SC_sgi(PLAYER_WEAPON4, pinfo.weap_main2);
    }
    if (! pinfo.weap_slot1) {
        SC_sgi(PLAYER_WEAPON5, 255);
    } else {
        SC_sgi(PLAYER_WEAPON5, pinfo.weap_slot1);
    }
    if (! pinfo.weap_slot6) {
        SC_sgi(PLAYER_WEAPON6, 255);
    } else {
        SC_sgi(PLAYER_WEAPON6, pinfo.weap_slot6);
    }
    if (! pinfo.weap_slot7) {
        SC_sgi(PLAYER_WEAPON7, 255);
    } else {
        SC_sgi(PLAYER_WEAPON7, pinfo.weap_slot7);
    }
    if (! pinfo.weap_slot8) {
        SC_sgi(PLAYER_WEAPON8, 255);
    } else {
        SC_sgi(PLAYER_WEAPON8, pinfo.weap_slot8);
    }
    if (! pinfo.weap_slot9) {
        SC_sgi(PLAYER_WEAPON9, 255);
    } else {
        SC_sgi(PLAYER_WEAPON9, pinfo.weap_slot9);
    }
    if (! pinfo.weap_slot10) {
        SC_sgi(PLAYER_WEAPON10, 255);
    } else {
        SC_sgi(PLAYER_WEAPON10, pinfo.weap_slot10);
    }
    return;
}

void func_0439(void) {
    t441_ret = SC_PC_Get();
    SC_P_ReadHealthFromGlobalVar(t441_ret, 95);
    return;
}

void func_0447(void) {
    t449_ret = SC_PC_Get();
    SC_P_WriteHealthToGlobalVar(t449_ret, 95);
    return;
}

void func_0455(void) {
    t457_ret = SC_PC_Get();
    SC_P_ReadAmmoFromGlobalVar(t457_ret, 60, 89);
    if (SC_ggi(PLAYER_AMMOINGUN)) {
        t472_ret = SC_PC_Get();
        t478_ret = SC_ggi(PLAYER_AMMOINGUN);
        SC_P_SetAmmoInWeap(t472_ret, 2, SC_ggi(PLAYER_AMMOINGUN));
    }
    if (SC_ggi(PLAYER_AMMOINPISTOL)) {
        t492_ret = SC_PC_Get();
        t498_ret = SC_ggi(PLAYER_AMMOINPISTOL);
        SC_P_SetAmmoInWeap(t492_ret, 1, SC_ggi(PLAYER_AMMOINPISTOL));
    }
    return;
}

void func_0504(void) {
    t506_ret = SC_PC_Get();
    SC_P_WriteAmmoToGlobalVar(t506_ret, 60, 89);
    t516_ret = SC_PC_Get();
    t520_ret = SC_P_GetAmmoInWeap(t516_ret, 2);
    SC_sgi(PLAYER_AMMOINGUN, t520_ret);
    t529_ret = SC_PC_Get();
    SC_sgi(PLAYER_AMMOINPISTOL, SC_P_GetAmmoInWeap(t529_ret, 1));
    return;
}

void func_0539(void) {
    s_SC_P_intel j[10];

    SC_PC_GetIntel(&j);
    local_10 = 0;
    for (local_10 = 0; local_10 < 10; local_10++) {
        SC_sgi(50 + tmp, t560_);
    }
    return;
}

void func_0573(void) {
    local_10 = 0;
    for (local_10 = 0; local_10 < 10; local_10++) {
        local_0[tmp].intel = SC_ggi(50 + tmp);
    }
    SC_PC_SetIntel(&local_0);
    return;
}

void func_0611(int param_0) {
    func_0276();
    func_0504();
    func_0447();
    func_0539();
    if (! param_0) {
        SC_MissionDone();
    } else {
        SC_MissionCompleted();
    }
    return;
}

void func_0621(void) {
    func_0439();
    func_0455();
    func_0573();
    return;
}

void SetRadioProps(void) {
    s_SC_SpeachBreakProps hudinfo;

    SC_ZeroMem(&hudinfo, 60);
    hudinfo.ra_where_ru_nr = 5111;
    hudinfo.ra_where_ru_txt = 5111;
    hudinfo.z = 5008;
    hudinfo.field_12 = 5008;
    hudinfo.field_16 = 3;
    hudinfo.field_20 = 5010;
    hudinfo.ra_where_ru_snd = 5009;
    hudinfo.field_28 = 5011;
    hudinfo.field_40 = 5010;
    hudinfo.field_44 = 5009;
    hudinfo.field_44 = 5011;
    hudinfo.field_52 = 0;
    hudinfo.field_56 = 0;
    SC_RadioBreak_Set(&hudinfo);
    SC_RadioSetDist(10.0f);
    return;
}

int IsGroupAlmostDead(int SideID, int GroupID, int Tolerance) {
    int local_1;

    local_1 = SC_GetGroupPlayers(SideID, GroupID);
    local_0 = 0;
    for (local_0 = 0; local_0 < local_1; local_0++) {
        t744_ret = SC_P_GetBySideGroupMember(SideID, GroupID, GroupID);
        if (SC_P_IsReady(t744_ret)) {
            local_2++;
        }
    }
    if (local_2 > Tolerance) {
        return FALSE;
    } else {
        return TRUE;
}

BOOL GetDummyPos(char * name, c_Vector3 * vec) {
    void* local_0;

    local_0 = SC_NOD_Get(0, name);
    if (local_0 != 0) {
        SC_NOD_GetWorldPos(local_0, vec);
        return TRUE;
    } else {
        return FALSE;
}

int func_0804(void) {
    int local_1;

    local_0 = rand() % 20;
    t817_ret = SC_ggi(SGI_CURRENTMISSION);
    switch (local_1) {
    case 1:
        if (tmp3 > 10) {
            return 19;
        } else {
            return 26;
        }
        break;
    case 2:
        break;
    case 3:
        break;
    case 4:
        break;
    case 5:
        if (tmp3 > 12) {
            return 26;
        } else {
            if (tmp3 > 8) {
                return 6;
            } else {
                return 19;
            }
        }
        break;
    case 16:
        break;
    case 17:
        if (tmp3 > 14) {
            return 26;
        } else {
            if (tmp3 > 10) {
                return 19;
            } else {
                if (tmp3 > 5) {
                    return 6;
                } else {
                    return 23;
                }
            }
        }
        break;
    case 6:
        if (tmp3 > 15) {
            return 26;
        } else {
            if (tmp3 > 11) {
                return 19;
            } else {
                if (tmp3 > 7) {
                    return 6;
                } else {
                    if (tmp3 > 2) {
                        return 23;
                    } else {
                        return 25;
                    }
                }
            }
        }
        break;
    case 7:
        break;
    case 8:
        if (tmp3 > 16) {
            return 26;
        } else {
            if (tmp3 > 12) {
                return 15;
            } else {
                if (tmp3 > 8) {
                    return 6;
                } else {
                    if (tmp3 > 4) {
                        return 19;
                    } else {
                        return 2;
                    }
                }
            }
        }
        break;
    case 9:
        break;
    case 23:
        if (tmp3 > 13) {
            return 8;
        } else {
            if (tmp3 > 6) {
                return 9;
            } else {
                return 10;
            }
        }
        break;
    case 12:
        if (tmp3 > 15) {
            return 2;
        } else {
            if (tmp3 > 11) {
                return 15;
            } else {
                if (tmp3 > 8) {
                    return 19;
                } else {
                    if (tmp3 > 4) {
                        return 6;
                    } else {
                        if (tmp3 > 1) {
                            return 26;
                        } else {
                            return 18;
                        }
                    }
                }
            }
        }
        break;
    case 13:
        break;
    case 15:
        break;
    case 18:
        if (tmp3 > 15) {
            return 2;
        } else {
            if (tmp3 > 11) {
                return 15;
            } else {
                if (tmp3 > 8) {
                    return 19;
                } else {
                    if (tmp3 > 5) {
                        return 6;
                    } else {
                        if (tmp3 > 2) {
                            return 26;
                        } else {
                            return 23;
                        }
                    }
                }
            }
        }
        break;
    case 19:
        break;
    case 20:
        break;
    case 21:
        break;
    case 22:
        if (tmp3 > 14) {
            return 2;
        } else {
            if (tmp3 > 10) {
                return 15;
            } else {
                if (tmp3 > 4) {
                    return 23;
                } else {
                    return 18;
                }
            }
        }
        break;
    case 24:
        if (tmp3 > 15) {
            return 2;
        } else {
            if (tmp3 > 11) {
                return 19;
            } else {
                if (tmp3 > 8) {
                    return 6;
                } else {
                    if (tmp3 > 4) {
                        return 23;
                    } else {
                        if (tmp3 > 1) {
                            return 26;
                        } else {
                            return 21;
                        }
                    }
                }
            }
        }
        break;
    case 26:
        break;
    case 27:
        break;
    case 28:
        if (tmp3 > 14) {
            return 2;
        } else {
            if (tmp3 > 10) {
                return 15;
            } else {
                if (tmp3 > 7) {
                    return 23;
                } else {
                    if (tmp3 > 3) {
                        return 6;
                    } else {
                        return 18;
                    }
                }
            }
        }
        break;
    case 29:
        if (tmp3 > 14) {
            return 2;
        } else {
            if (tmp3 > 11) {
                return 15;
            } else {
                if (tmp3 > 8) {
                    return 18;
                } else {
                    if (tmp3 > 3) {
                        return 23;
                    } else {
                        return 6;
                    }
                }
            }
        }
        break;
    case 25:
        if (tmp3 > 2) {
            return 2;
        } else {
            return 14;
        }
        break;
    case 30:
        break;
    case 31:
        if (tmp3 > 13) {
            return 2;
        } else {
            if (tmp3 > 11) {
                return 15;
            } else {
                if (tmp3 > 7) {
                    return 18;
                } else {
                    if (tmp3 > 4) {
                        return 23;
                    } else {
                        if (tmp3 > 1) {
                            return 6;
                        } else {
                            return 14;
                        }
                    }
                }
            }
        }
        break;
    }
block_283:
    return 2;
}

int func_1356(void) {
    int local_1;

    local_0 = rand() % 20;
    t1369_ret = SC_ggi(SGI_CURRENTMISSION);
    switch (local_1) {
    case 1:
        break;
    case 16:
        break;
    case 17:
        break;
    case 6:
        if (tmp3 > 13) {
            return "ini\\players\\poorvc.ini";
        } else {
            if (tmp3 > 6) {
                return "ini\\players\\poorvc2.ini";
            } else {
                return "ini\\players\\poorvc3.ini";
            }
        }
        break;
    case 2:
        break;
    case 3:
        break;
    case 4:
        break;
    case 5:
        break;
    case 7:
        break;
    case 8:
        if (tmp3 > 13) {
            return "ini\\players\\vcfighter2.ini";
        } else {
            if (tmp3 > 6) {
                return "ini\\players\\vcfighter3.ini";
            } else {
                return "ini\\players\\vcfighter4.ini";
            }
        }
        break;
    case 9:
        break;
    case 12:
        break;
    case 13:
        break;
    case 15:
        break;
    case 24:
        if (tmp3 > 15) {
            return "ini\\players\\vcfighter3.ini";
        } else {
            if (tmp3 > 10) {
                return "ini\\players\\vcfighter2.ini";
            } else {
                if (tmp3 > 5) {
                    return "ini\\players\\vcfighter3.ini";
                } else {
                    return "ini\\players\\vcfighter4.ini";
                }
            }
        }
        break;
    case 18:
        break;
    case 19:
        break;
    case 20:
        break;
    case 21:
        break;
    case 26:
        break;
    case 27:
        break;
    case 28:
        if (tmp3 > 13) {
            return "ini\\players\\vcuniform1.ini";
        } else {
            if (tmp3 > 6) {
                return "ini\\players\\vcuniform2.ini";
            } else {
                return "ini\\players\\vcuniform3.ini";
            }
        }
        break;
    case 22:
        break;
    case 23:
        break;
    case 25:
        break;
    case 29:
        break;
    case 30:
        break;
    case 31:
        if (tmp3 > 12) {
            return "ini\\players\\nvasoldier2.ini";
        } else {
            if (tmp3 > 4) {
                return "ini\\players\\nvasoldier3.ini";
            } else {
                return "ini\\players\\nvasoldier2.ini";
            }
        }
        break;
    }
block_373:
    return "ini\\players\\default_aiviet.ini";
}

void func_1614(void) {
    int local_1;

    local_0 = 0;
    switch (SC_ggi(SGI_CURRENTMISSION)) {
    case 1:
        param_0->field_92 = 24;
        param_0->field_96 = 38;
        break;
    case 2:
        break;
    default:
        switch (local_1) {
        case 3:
            break;
        case 4:
            break;
        case 5:
            param_0->field_92 = 23;
            param_0->field_96 = 25;
            break;
        case 6:
            param_0->field_92 = 24;
            param_0->field_96 = 26;
            param_0->field_100 = 38;
            break;
        case 7:
            break;
        case 8:
            param_0->field_92 = 23;
            param_0->field_96 = 24;
            param_0->field_100 = 25;
            break;
        case 9:
            param_0->field_92 = 23;
            param_0->field_96 = 25;
            break;
        case 12:
            param_0->field_92 = 23;
            param_0->field_96 = 24;
            param_0->field_100 = 25;
            param_0->field_104 = 37;
            param_0->field_108 = 38;
            break;
        case 16:
            break;
        case 17:
            param_0->field_92 = 23;
            param_0->field_96 = 26;
            param_0->field_100 = 24;
            break;
        }
        switch (local_1) {
        case 13:
            break;
        case 15:
            param_0->field_92 = 23;
            param_0->field_96 = 25;
            break;
        case 18:
            break;
        case 19:
            break;
        case 20:
            param_0->field_92 = 27;
            param_0->field_96 = 28;
            param_0->field_100 = 31;
            break;
        case 21:
            param_0->field_92 = 27;
            param_0->field_96 = 28;
            param_0->field_100 = 31;
            param_0->field_104 = 35;
            break;
        case 22:
            break;
        case 23:
            param_0->field_92 = 35;
            param_0->field_96 = 27;
            param_0->field_100 = 32;
            param_0->field_104 = 33;
            param_0->field_108 = 34;
            break;
        case 24:
            param_0->field_92 = 23;
            param_0->field_96 = 25;
            break;
        case 26:
            break;
        }
        switch (local_1) {
        case 25:
            param_0->field_92 = 31;
            param_0->field_96 = 35;
            param_0->field_100 = 36;
            break;
        case 27:
            break;
        case 28:
            param_0->field_92 = 26;
            param_0->field_96 = 27;
            param_0->field_100 = 28;
            param_0->field_104 = 31;
            break;
        case 29:
            param_0->field_92 = 35;
            param_0->field_96 = 32;
            param_0->field_100 = 33;
            param_0->field_104 = 34;
            break;
        case 30:
            break;
        case 31:
            param_0->field_92 = 33;
            param_0->field_96 = 34;
            param_0->field_100 = 35;
            param_0->field_104 = 36;
            break;
        }
        break;
    }
block_450:
    return;
}

void EquipPlayerVC(s_SC_P_CreateEqp * eqp, int * count) {
    dword* tmp4;

    count = 0;
    local_0 = rand() % 2;
    if (! local_0) {
    } else {
    }
    eqp[0] = "G\\EQUIPMENT\\VC\\bes\\EOP_e_mgznpouch01VC.BES";
    if (! local_0) {
    } else {
    }
    *tmp4 = "G\\EQUIPMENT\\VC\\eqp\\CVP_blckpjmsVC02\\medic\\EOP_e_mdclbag01VC.eqp";
    count[1] = &param_0;
    local_0 = rand() % 5;
    if (! local_0) {
    } else {
    }
    eqp[2] = "G\\EQUIPMENT\\VC\\bes\\EOP_e_canteen01VC.BES";
    if (! local_0) {
    } else {
    }
    eqp[2].y = "G\\EQUIPMENT\\VC\\eqp\\CVP_blckpjmsVC02\\vybaveni1\\EOP_e_canteen01VC.eqp";
    if (local_0) {
        count[1] = &param_0;
    }
    return;
}

void func_2258(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_bigbag01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_knife01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_knife01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_littlebag01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_m16ammobox01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_m16ammobox01_0.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_maceta01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_maceta01.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_pistolcase01.eqp";
    param_1 = 8;
    return;
}

void func_2367(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_bangs\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_bangs\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_1 = 2;
    return;
}

void func_2398(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_bigbag01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_canteen01_0.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_littlebag01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_m16ammobox01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_m16ammobox01_0.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_pistolcase01.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_hat1US_v01.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_hat1US_v01.eqp";
    param_1 = 8;
    return;
}

void func_2507(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_bronson\\lehke_vybaveni\\EOP_e_canteen01_0.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_bronson\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_hat1US_v01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_bronson\\lehke_vybaveni\\EOP_hat1US_v01.eqp";
    param_1 = 3;
    return;
}

void func_2551(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_hat4US_v01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_hat4US_v01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_bigmedicbag01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_bigmedicbag01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_canteen01_0.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_glasses01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_glasses01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_m16ammobox01_0.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_medicbag01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_medicbag01.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_pistolcase01.eqp";
    param_1 = 8;
    return;
}

void func_2660(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_crocker\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_glasses01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\lehke_vybaveni\\EOP_e_glasses01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_medicbag01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\lehke_vybaveni\\EOP_e_medicbag01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_hat4US_v01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_crocker\\lehke_vybaveni\\EOP_hat4US_v01.eqp";
    param_1 = 5;
    return;
}

void func_2730(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_hat2US_v01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_hat2US_v01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_e_flashlight01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_e_littlebag01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_e_m16ammobox01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_e_pistolcase01.eqp";
    param_1 = 6;
    return;
}

void func_2813(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_defort\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_defort\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_hat2US_v01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_defort\\lehke_vybaveni\\EOP_hat2US_v01.eqp";
    param_1 = 3;
    return;
}

void func_2857(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_pistolcase01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_bigbag01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_canteen01_0.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_flashlight01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_littlebag01.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_m16ammobox01.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_m16ammobox01_0.eqp";
    param_1 = 8;
    return;
}

void func_2966(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_hornster\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_hornster\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_1 = 2;
    return;
}

void func_2997(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_hat3US_v02.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_hat3US_v02.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_bigbag01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_flashlight01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_littlebag01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_maceta01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_maceta01.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_pistolcase01.eqp";
    param_1 = 7;
    return;
}

void func_3093(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_nhut\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_nhut\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_hat3US_v02.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_nhut\\lehke_vybaveni\\EOP_hat3US_v02.eqp";
    param_1 = 3;
    return;
}

void func_3137(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_hat4US_v02.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\EOP_UH14PH05_01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_rosenfield\\lehke_vybaveni\\EOP_e_ammoboxfp01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_rosenfield\\lehke_vybaveni\\EOP_e_ammoboxfp01_0.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_rosenfield\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_rosenfield\\lehke_vybaveni\\EOP_e_faidpouch01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_rosenfield\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_1 = 6;
    return;
}

void func_3220(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_bigbag01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_canteen01_0.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_littlebag01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_m16ammobox01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_m16ammobox01_0.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_m16ammobox01_1.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_hlmt1US_v03.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_hlmt1US_v03.eqp";
    param_1 = 8;
    return;
}

void func_3329(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_hat1US_v01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_hat1US_v01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_bigbag01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_canteen01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_canteen01_0.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_faidpouch01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_littlebag01.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_m16ammobox01.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_m16ammobox01_0.eqp";
    param_1 = 8;
    return;
}

void func_3438(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\lehke_vybaveni\\EOP_e_canteen01_0.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\lehke_vybaveni\\EOP_e_faidpouch01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_hat1US_v01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\lehke_vybaveni\\EOP_hat1US_v01.eqp";
    param_1 = 3;
    return;
}

void func_3482(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_bigbag01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_flashlight01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_m16ammobox01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_m16ammobox01_0.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_m16ammobox01_1.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_m16ammobox01_2.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_hlmt1US_v01.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_hlmt1US_v01.eqp";
    param_1 = 8;
    return;
}

void func_3591(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_ammoboxfp01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_bigbag01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_canteen01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_littlebag01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_m16ammobox01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_m16ammobox01_0.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_pistolcase01.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_hat4US_v01.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_hat4US_v01.eqp";
    param_1 = 8;
    return;
}

void func_3700(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\lehke_vybaveni\\EOP_e_ammoboxfp01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_hat4US_v01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\lehke_vybaveni\\EOP_hat4US_v01.eqp";
    param_1 = 4;
    return;
}

void func_3757(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\lehke_vybaveni\\EOP_e_ammoboxfp01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_hat1US_v03.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\lehke_vybaveni\\EOP_hat1US_v03.eqp";
    param_1 = 4;
    return;
}

void func_3814(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_bigbag01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_littlebag01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_m16ammobox01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_m16ammobox01_0.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_maceta01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_maceta01.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_hlmt1US_v03.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_hlmt1US_v03.eqp";
    param_1 = 7;
    return;
}

void func_3910(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_faidpouch01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_bigbag01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_canteen01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_littlebag01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_m16ammobox01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_m16ammobox01_0.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_pistolcase01.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_hat6US_v01.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_hat6US_v01.eqp";
    param_1 = 8;
    return;
}

void func_4019(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_hat3US_v03.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\lehke_vybaveni\\EOP_hat3US_v03.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\lehke_vybaveni\\EOP_e_faidpouch01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\lehke_vybaveni\\EOP_e_littlebag01.eqp";
    param_1 = 4;
    return;
}

void func_4076(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_flashlight01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_brt1US_v01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_brt1US_v01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_bigbag01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_canteen01_0.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_m16ammobox01.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_m16ammobox01_0.eqp";
    param_1 = 7;
    return;
}

void func_4172(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_m16ammobox01_0.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_bigbag01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_canteen01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_faidpouch01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_knife01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_knife01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_littlebag01.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_m16ammobox01.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_hat2US_v02.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_hat2US_v02.eqp";
    param_1 = 8;
    return;
}

void func_4281(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\lehke_vybaveni\\EOP_e_flashlight01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_brt1US_v01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\lehke_vybaveni\\EOP_brt1US_v01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\lehke_vybaveni\\EOP_e_ammoboxfp01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_1 = 5;
    return;
}

void func_4351(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_bigbag01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_faidpouch01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_littlebag01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_m16ammobox01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_m16ammobox01_0.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_hat2US_v02.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_hat2US_v02.eqp";
    param_1 = 7;
    return;
}

void func_4447(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_bigbag01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_ammoboxfp01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_canteen01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_canteen01_0.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_m16ammobox01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_m16ammobox01_0.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_hat3US_v02.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_hat3US_v02.eqp";
    param_1 = 7;
    return;
}

void func_4543(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_hat4US_v02.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\lehke_vybaveni\\EOP_hat4US_v02.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\lehke_vybaveni\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\lehke_vybaveni\\EOP_e_littlebag01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\lehke_vybaveni\\EOP_e_pistolcase01.eqp";
    param_1 = 4;
    return;
}

void func_4600(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_knife01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_knife01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_bigbag01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_canteen01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_littlebag01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_m16ammobox01.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_m16ammobox01_0.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_hlmt1US_v02.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_hlmt1US_v02.eqp";
    param_1 = 7;
    return;
}

void func_4696(int param_0, int param_1) {
    dword* tmp2;

    param_0[0] = "G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES";
    *tmp2 = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_ammoboxfp01.eqp";
    param_0[2] = "G\\Equipment\\US\\bes\\EOP_e_canteen01.BES";
    param_0[2]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_canteen01.eqp";
    param_0[4] = "G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES";
    param_0[4]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_littlebag01.eqp";
    param_0[6] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[6]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_m16ammobox01.eqp";
    param_0[8] = "G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES";
    param_0[8]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_m16ammobox01_0.eqp";
    param_0[10] = "G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES";
    param_0[10]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_pistolcase01.eqp";
    param_0[12] = "G\\Equipment\\US\\bes\\EOP_e_shovel01.BES";
    param_0[12]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_shovel01.eqp";
    param_0[14] = "G\\Equipment\\US\\bes\\EOP_hat1US_v02.BES";
    param_0[14]->y = "G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_hat1US_v02.eqp";
    param_1 = 8;
    return;
}

void func_4805(int param_0, int param_1) {
    dword* tmp8;

    param_0[0] = "G\\Equipment\\vc\\EOP_m16ammobox01.BES";
    param_0[2] = "G\\Equipment\\vc\\EOP_m16ammobox01.BES";
    param_0[4] = "G\\Equipment\\us\\EOP_canteen01.BES";
    param_0[6] = "G\\Equipment\\us\\EOP_helmet01_plechhelma.BES";
    *tmp8 = "G\\Equipment\\vc\\EOP_m16ammobox01position01.eqp";
    param_0[2]->y = "G\\Equipment\\vc\\EOP_m16ammobox01position06.eqp";
    param_0[4]->y = "G\\Equipment\\us\\EOP_canteen01position01.eqp";
    param_0[6]->y = "G\\Equipment\\us\\EOP_plech_defort_aza.eqp";
    param_1 = 4;
    return;
}

int ScriptMain(s_SC_L_info *info) {
    dword local_39[20];
    s_SC_P_AI_props ai_props;
    int local_100;
    int local_97;
    int local_98;
    int local_99;
    s_SC_P_Create pinfo;
    BOOL t4987_ret;
    int vCampPos;
    int vDummyDefort;
    c_Vector3 vec2;
    c_Vector3 vec3;

    switch (local_98) {
    case 0:
        if (local_99 == 0) {
            SC_ZeroMem(&pinfo, 156);
            SC_ZeroMem(&local_39, 80);
            pinfo.type = 2;
            pinfo.side = 0;
            pinfo.group = 0;
            pinfo.member_id = 4;
            pinfo.inifile = "ini\\players\\defort.ini";
            pinfo.name_nr = 2502;
            pinfo.icon_name = "defort";
            pinfo.weap_knife = 0;
            pinfo.weap_pistol = 22;
            pinfo.weap_main1 = 25;
            pinfo.weap_main2 = 60;
            pinfo.recover_pos = info->elapsed_time;
            pinfo.flags = 4;
            pinfo.debrief_group = 1;
            func_2730(&local_39, tmp32);
            pinfo.eqp = &local_39;
            info->param3 = SC_P_Create(&pinfo);
            t4987_ret = SC_GetWp("WayPoint161", &vCampPos);
            t4995_ret = GetDummyPos(t4987_ret, "DummyDefort", &vDummyDefort);
            gPhase = 1;
            info->param4 = 0.2f;
        } else {
            if (local_99 == 1) {
                if (SC_P_IsReady(info->param3)) {
                    SC_P_Ai_EnableShooting(info->param3, TRUE);
                    SC_P_Ai_SetMovePos(info->param3, SC_P_AI_MOVEPOS_CROUCH);
                    SC_P_Ai_SetMoveMode(info->param3, SC_P_AI_MOVEMODE_RUN);
                    SC_P_Ai_SetPeaceMode(info->param3, 1);
                    SC_P_Ai_SetBattleMode(info->param3, 4);
                    SC_P_Ai_SetMode(info->param3, SC_P_AI_MODE_BATTLE);
                    SC_P_EnableSearchDeathBodies(info->param3, FALSE);
                    SC_ZeroMem(&ai_props, 128);
                    SC_P_Ai_GetProps(info->param3, &ai_props);
                    ai_props.shoot_imprecision = 0.2f;
                    ai_props.extend_searchway = 1;
                    ai_props.shortdistance_fight = 1.0f;
                    ai_props.view_angle = 3.14f;
                    ai_props.view_angle_near = 6.2f;
                    ai_props.max_vis_distance = 30.0f;
                    ai_props.hear_distance_max = 30.0f;
                    ai_props.shoot_while_hidding = 1.0f;
                    ai_props.aimtime_max = 0.5f;
                    SC_P_Ai_SetProps(info->param3, &ai_props);
                    SC_P_SetSpeachDist(info->param3, 20.0f);
                    info->param4 = 0.5f;
                    gPhase = 2;
                } else {
                    return FALSE;
                }
            } else {
            }
        }
        switch (local_99) {
        case 2:
            SC_P_GetPos(info->param3, &vec2);
            t5160_ret = GetDummyPos("Radio1", &vec3);
            if (! (SC_IsNear3D( & vec2, & vec3, 32.0f))) break;
            SC_LevScr_Event(1000, 0);
            SC_P_Ai_SetPeaceMode(info->param3, 0);
            SC_P_Ai_SetBattleMode(info->param3, SC_P_AI_BATTLEMODE_HOLD);
            gPhase = 10;
            break;
        case 10:
            SC_P_GetPos(info->param3, &vec2);
            if (SC_IsNear3D( & vCampPos, & vec2, 4.5f)) {
                SC_P_Ai_SetPeaceMode(info->param3, 0);
                SC_P_Ai_SetBattleMode(info->param3, SC_P_AI_BATTLEMODE_HOLD);
                SC_P_Ai_SetStaticMode(info->param3, 1);
                fKTimer = 60.0f;
                gPhase = 20;
            } else {
                if (! (SC_IsNear3D( & vDummyDefort, & vec2, 30.0f))) break;
                if (goTimer > 0.0f) break;
                SC_P_Ai_SetMovePos(info->param3, SC_P_AI_MOVEPOS_CROUCH);
                SC_P_Ai_SetMoveMode(info->param3, SC_P_AI_MOVEMODE_WALK);
                SC_P_Ai_SetPeaceMode(info->param3, 0);
                SC_P_Ai_SetBattleModeExt(info->param3, 3, &vDummyDefort);
                SC_P_Ai_Go(info->param3, &vDummyDefort);
                goTimer = 5.0f;
            }
            break;
        case 20:
            t5309_ret = SC_P_GetBySideGroupMember(0, 0, 4);
            t5317_ret = SC_P_GetBySideGroupMember(1, 0, 0);
            if (SC_P_Ai_KnowsAboutPl(t5309_ret, t5317_ret)) {
                if (!bPssst) {
                    t5333_ret = SC_P_GetBySideGroupMember(0, 0, 4);
                    SC_P_Speech2(t5333_ret, 3325, &local_97);  // 3325: "Check that gook out, he ain't seen us."
                    bPssst = 1;
                }
            }
            t5350_ret = SC_P_GetBySideGroupMember(1, 0, 0);
            if (SC_P_GetHasShoot(t5350_ret)) {
                if (!bDoorman) {
                    t5366_ret = SC_P_GetBySideGroupMember(0, 0, 4);
                    SC_P_Speech2(t5366_ret, 3326, &local_97);  // 3326: "Shit, over there!"
                    bDoorman = 1;
                }
            }
            t5383_ret = SC_P_GetBySideGroupMember(1, 0, 0);
            if (SC_P_Ai_GetDanger(t5383_ret) > 0.4f) {
                if (!bSoudruh) {
                    t5401_ret = SC_P_GetBySideGroupMember(1, 0, 0);
                    SC_P_Speech2(t5401_ret, 3327, &local_97);
                    bSoudruh = 1;
                }
            }
            if (! bPssst) break;
            if (! bDoorman) break;
            if (! bSoudruh) break;
            gPhase = 100;
            break;
        case 30:
            SC_P_GetPos(info->param3, &vec2);
            t5439_ret = SC_PC_GetPos(&vec3);
            if (SC_IsNear3D( & vec2, & vec3, 5.0f)) {
                fKTimer -= info->next_exe_time;
                if (fKTimer < 0.0f) {
                    local_97 = 0;
                    SC_P_Speech2(info->param3, 3335, &local_97);  // 3335: "This is a good spot. Any fucker shows his head and bang, it�s gone."
                    t5476_0 = FTOD(local_97);
                    t5479_0 = DADD(SC_PC_GetPos(&vec3), t5476_0, t5476_1, tmp111);
                    local_97 = (float)t5479_0;
                    t5486_ret = SC_PC_Get();
                    SC_P_Speech2(t5486_ret, 3336, &local_97);  // 3336: "Gimme the horn."
                    fKTimer = 60.0f;
                }
            } else {
                fKTimer = 60.0f;
            }
            break;
        case 100:
            info->param4 = 1.0f;
            break;
        }
        break;
    case 1:
        switch (local_98) {
        case 2:
            switch (local_99) {
            case 1003:
                if (local_100 == 30) {
                    gPhase = 30;
                    fKTimer = 10.0f;
                }
                break;
            case 1004:
                if (local_100 == 70) {
                    t5567_ret = GetDummyPos("DefortTele", &vec3);
                    SC_P_SetPos(info->param3, &vec3);
                    SC_P_Ai_SetMode(info->param3, SC_P_AI_MODE_PEACE);
                    t5588_ret = SC_PC_Get();
                    SC_P_Ai_Script_WatchPlayer(info->param3, t5588_ret, 0.0f);
                    SC_P_Ai_SetMovePos(info->param3, SC_P_AI_MOVEPOS_STAND);
                    SC_P_Ai_GetProps(info->param3, &ai_props);
                    ai_props.disable_peace_crouch = 1;
                    SC_P_Ai_SetProps(info->param3, &ai_props);
                    gPhase = 100;
                }
                break;
            }
        case 1:
            SC_P_Heal(info->param3);
            break;
        }
        break;
    case 2:
        switch (local_98) {
        case 2:
            switch (local_99) {
            case 1003:
                break;
            case 1004:
                break;
            }
        case 1:
            break;
        }
        break;
    }
block_578:
    return TRUE;
}
