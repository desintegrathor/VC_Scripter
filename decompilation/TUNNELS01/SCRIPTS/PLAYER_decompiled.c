// Structured decompilation of decompilation/TUNNELS01/SCRIPTS/PLAYER.SCR
// Functions: 15

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword gVar;
BOOL gVar1;
dword gVar2;
BOOL gVar3;
dword gVar4;
dword gVar5;
int gVar6;
dword gVar7;
dword gVar8;
int gVar9;
dword gVar10;
dword gVar11;
int gVar12;
dword gVar13;
dword gphase;

int _init(s_SC_L_info *info) {
    s_SC_P_Create tmp;

    return FALSE;
    tmp = frnd(param);
    if (!(tmp < 0)) {
        tmp = -tmp;
    }
    return tmp;
    SC_P_Ai_SetMode(retval, SCM_FEELDANGER);
    SC_P_Ai_EnableShooting(retval, SCM_RUN);
    SC_P_Ai_EnableSituationUpdate(retval, 1);
    SC_Log(gVar, "Player %d enabled", retval);
    return FALSE;
    SC_P_Ai_SetMode(retval, SCM_ENABLE);
    SC_P_Ai_EnableShooting(retval, gVar1);
    SC_P_Ai_EnableSituationUpdate(retval, 0);
    SC_P_Ai_Stop(retval);
    SC_Log(3, "Player %d disabled", retval);
    return FALSE;
}

int func_0064(int param, int param, int param) {
    s_SC_P_Create props;

    if (!param_0) {
        SC_P_ScriptMessage(param_0, param, retval);
        return FALSE;
    } else {
        SC_Log(3, "Message %d %d to unexisted player!", param, retval);
        return FALSE;
    }
    SC_P_GetBySideGroupMember(1, param_0, param);
    SC_P_Ai_GetSureEnemies(ai_props.watchfulness_zerodist);
    if (!props) {
        return FALSE;
    } else {
        SC_P_GetBySideGroupMember(1, param_0, param);
        SC_P_Ai_GetDanger(ai_props.watchfulness_zerodist);
        return FALSE;
        return FALSE;
    }
    SC_P_Ai_GetSureEnemies(param);
    if (!props) {
        return FALSE;
    } else {
        SC_P_Ai_GetDanger(param);
        return FALSE;
        return FALSE;
    }
    SC_ZeroMem(&props, 128);
    SC_P_Ai_GetProps(param, &props);
    props.field19 = retval;
    SC_P_Ai_SetProps(param, &props);
    return &props;
    SC_ZeroMem(&props, 128);
    SC_P_Ai_GetProps(param, &props);
    props.field11 = retval;
    SC_P_Ai_SetProps(param, &props);
    return &props;
    SC_ZeroMem(&props, 128);
    SC_P_Ai_GetProps(param, &props);
    props.field5 = props.field5 * retval;
    SC_P_Ai_SetProps(param, &props);
    return &props;
    SC_ZeroMem(&props, 128);
    SC_P_Ai_GetProps(param, &props);
    props.field18 = props.field18 * retval;
    SC_P_Ai_SetProps(param, &props);
    return &props;
    SC_ZeroMem(&props, 128);
    SC_P_Ai_GetProps(param, &props);
    if (!retval) {
        props.field16 = 5.0f;
    } else {
        props.field16 = 1000.0f;
    }
    SC_P_Ai_SetProps(param, &props);
    return &props;
    SC_ZeroMem(&props, 128);
    SC_P_Ai_GetProps(param, &props);
    props.field25 = retval;
    SC_P_Ai_SetProps(param, &props);
    return &props;
    SC_ggi(SGI_CURRENTMISSION);
    return FALSE;
    SC_ggi(SGI_CHOPPER);
    return FALSE;
    SC_P_GetInfo(param, &props);
    return props;
    SC_ZeroMem(&props, 128);
    SC_P_Ai_GetProps(param, &props);
    props = retval;
    SC_P_Ai_SetProps(param, &props);
    return &props;
}

int func_0318(void) {
    retval->field_40 = SC_ggi(101);
    if (!((*t329_0))) {
    } else {
        retval->field_40 = 29;
    }
    if (!((*t339_0) == 255)) {
        retval->field_40 = 0;
    }
    retval->field_44 = SC_ggi(102);
    if (!((*t360_0))) {
    } else {
        retval->field_44 = 7;
    }
    if (!((*t370_0) == 255)) {
        retval->field_44 = 0;
    }
    retval->field_48 = SC_ggi(103);
    if (!((*t391_0))) {
    } else {
        SC_ggi(SGI_CURRENTMISSION);
        retval->field_48 = 23;
        SC_ggi(SGI_CURRENTMISSION);
        retval->field_48 = 25;
        retval->field_48 = 1;
    }
    switch (PLAYER_AMMOINGUN) {
    case 255:
        retval->field_48 = 0;
        break;
    case 255:
        retval->field_52 = 0;
        break;
    default:
        if ((*t483_0) == 255) {
            retval->field_56 = 0;
        }
        retval->field_60 = SC_ggi(106);
        if ((*t504_0) == 255) {
            retval->field_60 = 0;
        }
        retval->field_64 = SC_ggi(107);
        if ((*t525_0) == 255) {
            retval->field_64 = 0;
        }
        retval->field_68 = SC_ggi(108);
        if ((*t546_0)) {
        } else {
            retval->field_68 = 63;
        }
        if ((*t556_0) == 255) {
            retval->field_68 = 0;
        }
        retval->field_72 = SC_ggi(109);
        if ((*t577_0) == 255) {
            retval->field_72 = PLAYER_AMMOINGUN;
        }
        retval->field_76 = PLAYER_AMMOINPISTOL;
        return FALSE;
    }
    retval->field_56 = 59;
    return;
}

int func_0593(void) {
    SC_PC_Get();
    SC_P_GetWeapons(local_40, &local_0);
    if (!i.field10) {
        SC_sgi(101, t612_0);
    } else {
        SC_sgi(101, 255);
    }
    if (!local_0.field11) {
        SC_sgi(102, t627_0);
    } else {
        SC_sgi(102, 255);
    }
    if (!local_0.field12) {
        SC_sgi(103, t642_0);
    } else {
        SC_sgi(103, 255);
    }
    if (!local_0.field13) {
        SC_sgi(PLAYER_WEAPON1, t657_0);
    } else {
        SC_sgi(PLAYER_WEAPON2, PLAYER_WEAPON3);
    }
    if (!local_0.field14) {
        SC_sgi(PLAYER_WEAPON4, t672_0);
    } else {
        SC_sgi(PLAYER_WEAPON5, PLAYER_WEAPON6);
    }
    if (!local_0.field15) {
        SC_sgi(PLAYER_WEAPON7, t687_0);
    } else {
        SC_sgi(PLAYER_WEAPON8, PLAYER_WEAPON9);
    }
    if (!local_0.field16) {
        SC_sgi(PLAYER_WEAPON10, t702_0);
    } else {
        SC_sgi(107, 255);
    }
    if (!local_0.field17) {
        SC_sgi(108, t717_0);
    } else {
        SC_sgi(108, 255);
    }
    if (!local_0.field18) {
        SC_sgi(109, t732_0);
    } else {
        SC_sgi(109, 255);
    }
    if (!local_0.field19) {
        SC_sgi(110, t747_0);
    } else {
        SC_sgi(110, 255);
    }
    return t747_0;
}

int func_0756(void) {
    SC_PC_Get();
    SC_P_ReadHealthFromGlobalVar(i, 95);
    return FALSE;
}

int func_0764(void) {
    SC_PC_Get();
    SC_P_WriteHealthToGlobalVar(i, 95);
    return FALSE;
}

int func_0772(void) {
    int tmp;
    s_SC_P_Create local_;

    SC_PC_Get();
    SC_P_ReadAmmoFromGlobalVar(local_, 60, 89);
    SC_ggi(90);
    if (!local_) {
        SC_PC_Get();
        SC_ggi(90);
        SC_P_SetAmmoInWeap(2, 90, tmp);
    }
    SC_ggi(91);
    if (!local_) {
        SC_PC_Get();
        SC_ggi(91);
        SC_P_SetAmmoInWeap(1, 91, tmp);
    }
    return FALSE;
}

int func_0821(void) {
    SC_PC_Get();
    SC_P_WriteAmmoToGlobalVar(i, 60, 89);
    SC_PC_Get();
    SC_P_GetAmmoInWeap(m, 2);
    SC_sgi(SGI_MISSIONALARM, j);
    SC_PC_Get();
    SC_P_GetAmmoInWeap(local_2, 1);
    SC_sgi(SGI_MISSIONDEATHCOUNT, local_1);
    return FALSE;
}

int func_0856(int param, int param, int param) {
    int local_;

    SC_PC_GetIntel(&i);
    local_ = 0;
    // Loop header - Block 111 @865
    for (local_10 = 0; (local_ ? 10); local_10 = local_ + 1) {
        if (!(local_ < 10)) break;  // exit loop @889
        SC_sgi(50 + local_, local_0[local_]);
        local_++;
        continue;  // back to loop header @865
    }
    return local_;
    local_ = 0;
    if (!(local_ < 10)) {
        local_0[local_] = SC_ggi(50 + local_);
        local_++;
    }
    SC_PC_SetIntel(&local_0);
    return &local_0;
    func_0593();
    func_0821();
    func_0764();
    SC_MissionCompleted();
    return FALSE;
    func_0856();
    func_0593();
    func_0821();
    func_0764();
    SC_Osi("MISSION COMPLETE");
    SC_MissionDone();
    return FALSE;
    SC_ShowHelp(&retval, 1, 6.0f);
    return FALSE;
    local_0 = param;
    local_0.field1 = retval;
    SC_ShowHelp(&local_0, 2, 12.0f);
    return 12.0f;
    local_0 = idx;
    local_0.field1 = param;
    local_0.field2 = retval;
    SC_ShowHelp(&local_0, 3, 24.0f);
    return 24.0f;
}

int func_0993(int param, int param) {
    c_Vector3 local_1;
    c_Vector3 local_128;
    c_Vector3 local_131;
    c_Vector3 tmp1;
    int local_135;
    int local_137;
    int local_5;
    int local_6;
    int tmp;
    int tmp2;
    int tmp3;
    s_SC_P_Create local_;

    SC_ggi(SGI_DIFFICULTY);
    return FALSE;
    rand();
    local_ = local_1 % 20;
    SC_ggi(SGI_CURRENTMISSION);
    if (!(local_1 > 12)) {
        return 18;
        return 15;
        return 26;
        return 2;
        return 19;
        return 6;
        return 23;
    } else {
        return 28;
        return 15;
        return 26;
        return 2;
        return 19;
        return 6;
        return 23;
    }
    goto block_152; // @1111
    rand();
    local_ = local_1 % 20;
    if (!(local_ > 18)) {
        return 14;
    } else {
        return 18;
        return 2;
        return 15;
        return 2;
    }
    rand();
    local_ = local_1 % 20;
    SC_ggi(SGI_CURRENTMISSION);
    switch (SGI_CURRENTMISSION) {
    case 1:
        if (local_ > 10) {
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
        if (local_ > 12) {
            return 26;
        } else {
            if (local_ > 8) {
                return 6;
            } else {
                return 19;
            }
        }
    case 16:
        break;
    case 17:
        if (local_ > 14) {
            return 26;
        } else {
            if (local_ > 10) {
                return 19;
            } else {
                if (local_ > 5) {
                    return 6;
                } else {
                    return 23;
                }
            }
        }
    case 6:
        if (local_ > 15) {
            return 26;
        } else {
            if (local_ > 11) {
                return 19;
            } else {
                if (local_ > 7) {
                    return 6;
                } else {
                    if (local_ > 2) {
                        return 23;
                    } else {
                        return 25;
                    }
                }
            }
        }
    case 7:
        break;
    case 8:
        break;
    case 10:
        if (local_ > 16) {
            return 26;
        } else {
            if (local_ > 12) {
                return 15;
            } else {
                if (local_ > 8) {
                    return 6;
                } else {
                    if (local_ > 4) {
                        return 19;
                    } else {
                        return 2;
                    }
                }
            }
        }
    case 9:
        break;
    case 11:
        break;
    case 23:
        if (local_ > 13) {
            return 8;
        } else {
            if (local_ > 6) {
                return 9;
            } else {
                return 10;
            }
        }
    case 12:
        if (local_ > 15) {
            return 2;
        } else {
            if (local_ > 11) {
                return 15;
            } else {
                if (local_ > 8) {
                    return 19;
                } else {
                    if (local_ > 4) {
                        return 6;
                    } else {
                        if (local_ > 1) {
                            return 26;
                        } else {
                            return 18;
                        }
                    }
                }
            }
        }
    case 13:
        break;
    case 14:
        break;
    case 15:
        break;
    case 18:
        if (local_ > 15) {
            return 2;
        } else {
            if (local_ > 11) {
                return 15;
            } else {
                if (local_ > 8) {
                    return 19;
                } else {
                    if (local_ > 5) {
                        return 6;
                    } else {
                        if (local_ > 2) {
                            return 26;
                        } else {
                            return 23;
                        }
                    }
                }
            }
        }
    case 19:
        break;
    case 20:
        break;
    case 21:
        break;
    case 22:
        if (local_ > 14) {
            return 2;
        } else {
            if (local_ > 10) {
                return 15;
            } else {
                if (local_ > 4) {
                    return 23;
                } else {
                    return 18;
                }
            }
        }
    case 24:
        if (local_ > 15) {
            return 2;
        } else {
            if (local_ > 11) {
                return 19;
            } else {
                if (local_ > 8) {
                    return 6;
                } else {
                    if (local_ > 4) {
                        return 23;
                    } else {
                        if (local_ > 1) {
                            return 26;
                        } else {
                            return 21;
                        }
                    }
                }
            }
        }
    case 26:
        break;
    case 27:
        break;
    case 28:
        if (local_ > 14) {
            return 2;
        } else {
            if (local_ > 10) {
                return 15;
            } else {
                if (local_ > 7) {
                    return 23;
                } else {
                    if (local_ > 3) {
                        return 6;
                    } else {
                        return 18;
                    }
                }
            }
        }
    case 29:
        if (local_ > 14) {
            return 2;
        } else {
            if (local_ > 11) {
                return 15;
            } else {
                if (local_ > 8) {
                    return 18;
                } else {
                    if (local_ > 3) {
                        return 23;
                    } else {
                        return 6;
                    }
                }
            }
        }
    case 25:
        if (local_ > 2) {
            return 2;
        } else {
            return 14;
        }
    case 30:
        break;
    case 31:
        break;
    case 32:
        if (local_ > 13) {
            return 2;
        } else {
            if (local_ > 11) {
                return 15;
            } else {
                if (local_ > 7) {
                    return 18;
                } else {
                    if (local_ > 4) {
                        return 23;
                    } else {
                        if (local_ > 1) {
                            return 6;
                        } else {
                            return 14;
                        }
                    }
                }
            }
        }
    default:
        return 2;
    }
    rand();
    local_ = local_1 % 20;
    SC_ggi(SGI_CURRENTMISSION);
    switch (SGI_CURRENTMISSION) {
    case 1:
        break;
    case 16:
        break;
    case 17:
        break;
    case 6:
        if (local_ > 13) {
            return "ini\\players\\poorvc.ini";
        } else {
            if (local_ > 6) {
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
        break;
    case 10:
        if (local_ > 13) {
            return "ini\\players\\vcfighter2.ini";
        } else {
            if (local_ > 6) {
                return "ini\\players\\vcfighter3.ini";
            } else {
                return "ini\\players\\vcfighter4.ini";
            }
        }
    case 9:
        break;
    case 11:
        break;
    case 12:
        break;
    case 13:
        break;
    case 14:
        break;
    case 15:
        break;
    case 24:
        if (local_ > 15) {
            return "ini\\players\\vcfighter3.ini";
        } else {
            if (local_ > 10) {
                return "ini\\players\\vcfighter2.ini";
            } else {
                if (local_ > 5) {
                    return "ini\\players\\vcfighter3.ini";
                } else {
                    return "ini\\players\\vcfighter4.ini";
                }
            }
        }
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
        if (local_ > 13) {
            return "ini\\players\\vcuniform1.ini";
        } else {
            if (local_ > 6) {
                return "ini\\players\\vcuniform2.ini";
            } else {
                return "ini\\players\\vcuniform3.ini";
            }
        }
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
        break;
    case 32:
        if (local_ > 12) {
            return "ini\\players\\nvasoldier2.ini";
        } else {
            if (local_ > 4) {
                return "ini\\players\\nvasoldier3.ini";
            } else {
                return "ini\\players\\nvaofficer.ini";
            }
        }
    default:
        return "ini\\players\\default_aiviet.ini";
    }
    local_ = 0;
    if (!(local_ < 8)) {
        t2014_0[local_] = 0;
        t2023_0[local_] = 0;
        local_++;
    }
    SC_ggi(SGI_CURRENTMISSION);
    switch (SGI_CURRENTMISSION) {
    case 1:
        t2053_0 = 24;
        t2060_0 + 4 = 38;
        break;
    case 2:
        break;
    case 3:
        break;
    case 4:
        break;
    case 5:
        t2088_0 = 23;
        t2095_0 + 4 = 25;
        break;
    case 16:
        break;
    case 17:
        t2113_0 = 23;
        t2120_0 + 4 = 26;
        t2127_0 + 8 = 24;
        break;
    case 6:
        t2140_0 = 24;
        t2147_0 + 4 = 26;
        t2154_0 + 8 = 38;
        break;
    case 7:
        break;
    case 8:
        t2172_0 = 23;
        t2179_0 + 4 = 24;
        t2186_0 + 8 = 25;
        break;
    case 9:
        break;
    case 11:
        break;
    case 10:
        t2209_0 = 23;
        t2216_0 + 4 = 25;
        break;
    case 12:
        t2229_0 = 23;
        t2236_0 + 4 = 24;
        t2243_0 + 8 = 25;
        t2250_0 + 12 = 37;
        t2257_0 + 16 = 38;
        break;
    case 13:
        break;
    case 14:
        break;
    case 15:
        t2280_0 = 23;
        t2287_0 + 4 = 25;
        break;
    case 18:
        break;
    case 19:
        break;
    case 20:
        t2310_0 = 27;
        t2317_0 + 4 = 28;
        t2324_0 + 8 = 31;
        break;
    case 21:
        t2337_0 = 27;
        t2344_0 + 4 = 28;
        t2351_0 + 8 = 31;
        t2358_0 + 12 = 35;
        break;
    case 22:
        break;
    case 23:
        t2376_0 = 35;
        t2383_0 + 4 = 27;
        t2390_0 + 8 = 32;
        t2397_0 + 12 = 33;
        t2404_0 + 16 = 34;
        break;
    case 24:
        t2417_0 = 23;
        t2424_0 + 4 = 25;
        break;
    case 26:
        break;
    case 27:
        break;
    case 28:
        t2447_0 = 26;
        t2454_0 + 4 = 27;
        t2461_0 + 8 = 28;
        t2468_0 + 12 = 31;
        break;
    case 25:
        t2481_0 = 31;
        t2488_0 + 4 = 35;
        t2495_0 + 8 = 36;
        break;
    case 29:
        t2508_0 = 35;
        t2515_0 + 4 = 32;
        t2522_0 + 8 = 33;
        t2529_0 + 12 = 34;
        break;
    case 30:
        break;
    case 31:
        break;
    case 32:
        t2552_0 = 33;
        t2559_0 + 4 = 34;
        t2566_0 + 8 = 35;
        t2573_0 + 12 = 36;
        break;
    default:
        t2582_0 = 35;
        t2589_0 + 4 = 27;
        t2596_0 + 8 = 32;
        t2603_0 + 12 = 33;
        t2610_0 + 16 = 34;
        return local_1;
    }
    tmp = 100.0f;
    SC_ggi(SGI_GAMETYPE);
    if (!local_138) {
        SC_P_GetPos(j, &local_131);
        SC_MP_EnumPlayers(&local_, &local_134, 0);
        return FALSE;
        local_135 = 0;
        SC_P_GetPos(local_0[local_135], &local_128);
        local_137 = SC_2VectorsDist(&local_128, &local_131);
        tmp = local_137;
        local_128 = param;
        local_135++;
        return TRUE;
        return FALSE;
    } else {
        SC_PC_GetPos(param);
        tmp = SC_2VectorsDist(&local_128, &local_131);
        return TRUE;
        return FALSE;
    }
    local_1 = SC_GetGroupPlayers(param_0, param);
    local_ = 0;
    if (!(local_ < local_1)) {
        SC_P_GetBySideGroupMember(param_0, param, local_);
        SC_P_IsReady(tmp1);
        return FALSE;
        local_++;
    }
    return TRUE;
    local_1 = SC_GetGroupPlayers(param_0, param);
    local_ = 0;
    if (!(local_ < local_1)) {
        SC_P_GetBySideGroupMember(param_0, param, local_);
        SC_P_IsReady(tmp1);
        SC_P_GetBySideGroupMember(param_0, param, local_);
        SC_P_GetActive(tmp1);
        return FALSE;
        local_++;
    }
    return TRUE;
    tmp2 = SC_GetGroupPlayers(1, param);
    local_ = 0;
    if (!(local_ < tmp2)) {
        tmp3 = SC_P_GetBySideGroupMember(1, param, local_);
        tmp1 = SC_P_Ai_GetDanger(tmp3);
        return TRUE;
        local_1 = SC_P_Ai_GetSureEnemies(tmp3);
        return TRUE;
        local_++;
    }
    return FALSE;
    local_ = 1;
    if (!(local_ < 6)) {
        tmp3 = SC_P_GetBySideGroupMember(0, 0, local_);
        tmp1 = SC_P_Ai_GetDanger(tmp3);
        return TRUE;
        local_1 = SC_P_Ai_GetSureEnemies(tmp3);
        return TRUE;
        local_++;
    }
    return FALSE;
    local_ = 0;
    if (!(local_ < 6)) {
        local_6 = SC_P_GetBySideGroupMember(0, 0, local_);
        SC_P_GetPos(local_6, &local_1);
        local_5 = SC_2VectorsDist(param, &local_1);
        tmp3 = local_5;
        local_++;
    }
    return tmp3;
}

int func_3078(int param, int param, int param, int param, int param) {
    c_Vector3 local_1;
    c_Vector3 props;
    c_Vector3 tmp1;
    int local_;
    int local_2;
    int local_4;
    int local_48;
    int local_6;
    int tmp;
    s_SC_P_Create i;
    s_SC_P_getinfo local_34;
    s_SC_P_getinfo plinfo;
    s_sphere sphere;

    i = SC_NOD_Get(0, param);
    if (!(i != 0)) {
        SC_NOD_GetWorldPos(i, retval);
    }
    return retval;
    i = SC_NOD_Get(0, param);
    if (!(i != 0)) {
        SC_NOD_GetWorldRotZ(i);
        return local_1;
    } else {
        return FALSE;
    }
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_GetPeaceMode(local_1);
    if (!(i == 2)) {
        SC_P_GetBySideGroupMember(0, 0, 1);
        SC_P_Ai_SetPeaceMode(i, 0);
    }
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_Stop(i);
    return FALSE;
    func_3078(param, &i);
    SC_DoExplosion(&i, retval);
    return retval;
    local_ = SC_NOD_Get(0, retval);
    if (!local_) {
        SC_NOD_GetWorldPos(local_, &local_1);
        i = SC_NOD_GetWorldRotZ(local_);
        i = i - 1.5700000524520874f;
        local_4 = local_1;
        cos(i);
        local_4 = 2.0f - i * ai_props.shortdistance_fight;
        sin(i);
        local_4.field1 = 2.0f + i * ai_props.shortdistance_fight;
        SC_DoExplosion(&local_4, 1);
        local_4 = local_1;
        cos(i);
        local_4 = 4.0f - i * ai_props.shortdistance_fight;
        sin(i);
        local_4.field1 = 4.0f + i * ai_props.shortdistance_fight;
        SC_DoExplosion(&local_4, 2);
        local_4 = local_1;
        cos(i);
        local_4 = 8.0f - i * ai_props.shortdistance_fight;
        sin(i);
        local_4.field1 = 8.0f + i * ai_props.shortdistance_fight;
        SC_DoExplosion(&local_4, 3);
        SC_DUMMY_Set_DoNotRenHier2(local_, 1);
        return TRUE;
    } else {
        SC_message("FATAL! Claymore %s not found!!!!!!");
        return TRUE;
    }
    func_3078(param_0, &local_4);
    local_1.field2 = local_4.field2;
    i = 0;
    if (!(i < param)) {
        frnd(retval);
        local_1 = retval + ai_props.shoot_imprecision;
        frnd(retval);
        local_1.field1 = retval + ai_props.shoot_imprecision;
        SC_DoExplosion(&local_1, param_0);
        i++;
    }
    return i;
    SC_GetWp(param, &i);
    SC_DoExplosion(&i, retval);
    return retval;
    SC_GetWp(retval, &i);
    SC_CreatePtc(176, &i);
    return &i;
    SC_GetWp(retval, &i);
    SC_DoExplosion(&i, 3);
    SC_SND_PlaySound3D(2965, &i);
    SC_NOD_Get(0, retval);
    SC_CreatePtc_Ext(retval, ai_props.watchfulness_maxdistance, 1000.0f, 0.0f, 1.0f, 1.0f);
    SC_NOD_Get(0, retval);
    SC_CreatePtc_Ext(retval, ai_props.watchfulness_maxdistance, 1000.0f, 0.0f, 1.0f, 1.0f);
    props = 0;
    if (!(props < 6)) {
        SC_GetWp(retval, &i);
        frnd(5.0f);
        i = 5.0f + ai_props.watchfulness_maxdistance;
        frnd(5.0f);
        i.field1 = 5.0f + ai_props.watchfulness_maxdistance;
        SC_CreatePtcVec_Ext(177, &i, 1000.0f, 0.0f, 1.0f, 1.0f);
        props++;
    }
    return props;
    SC_CreatePtc(198, retval);
    SC_SND_PlaySound3D(2965, retval);
    SC_CreatePtcVec_Ext(176, retval, 1000.0f, 0.0f, 1.0f, 1.0f);
    SC_CreatePtcVec_Ext(177, retval, 5.0f, 0.0f, 1.0f, 1.0f);
    return 1.0f;
    local_1.field2 = (*t3560_0);
    i = 0;
    if (!(i < param)) {
        frnd(retval);
        local_1 = retval + ai_props.watchfulness_maxdistance;
        frnd(retval);
        local_1.field1 = retval + ai_props.watchfulness_maxdistance;
        SC_CreatePtc(198, &local_1);
        SC_CreatePtcVec_Ext(177, &local_1, 5.0f, 0.0f, 1.0f, 1.0f);
        i++;
    }
    SC_CreatePtcVec_Ext(176, param_0, 1000.0f, 0.0f, 1.0f, 1.0f);
    return 1.0f;
    local_1.field2 = (*t3634_0);
    i = 0;
    if (!(i < param)) {
        frnd(retval);
        local_1 = retval + ai_props.watchfulness_maxdistance;
        frnd(retval);
        local_1.field1 = retval + ai_props.watchfulness_maxdistance;
        SC_CreatePtc(198, &local_1);
        i++;
    }
    SC_CreatePtcVec_Ext(176, param_0, 1000.0f, 0.0f, 1.0f, 1.0f);
    return 1.0f;
    local_1.field2 = (*t3700_0);
    i = 0;
    if (!(i < param)) {
        frnd(retval);
        local_1 = retval + ai_props.watchfulness_maxdistance;
        frnd(retval);
        local_1.field1 = retval + ai_props.watchfulness_maxdistance;
        SC_CreatePtc(198, &local_1);
        i++;
    }
    return i;
    SC_ZeroMem(&props, 128);
    SC_P_Ai_GetProps(retval, &props);
    props.field19 = 1;
    props.field3 = 4.0f;
    SC_P_Ai_SetProps(retval, &props);
    i.field1 = 0.8999999761581421f;
    i = 0.30000001192092896f;
    i.field2 = 0.5f;
    SC_P_Ai_SetBattleProps(retval, &i);
    return &i;
    SC_P_GetDir(param, &i);
    props = SC_VectorLen(&i);
    if (!props > 1.0f) {
        return TRUE;
    } else {
        return FALSE;
    }
    i = 0;
    if (!(i < 6)) {
        SC_P_GetBySideGroupMember(0, 0, i);
        SC_P_IsReady(local_);
        SC_P_GetBySideGroupMember(0, 0, i);
        SC_P_GetPos(local_6, &props);
        local_2 = SC_2VectorsDist(&props, param);
        local_1 = local_2;
        props = i + 1;
    }
    return local_1;
    SC_P_GetPos(param_0, &props);
    SC_IsNear3D(&props, param_0, param);
    return props;
    SC_PC_GetPos(&props);
    SC_IsNear3D(&props, param_0, param);
    return props;
    if (!param_0) {
        SC_ZeroMem(&props, 128);
        SC_P_Ai_GetProps(param_0, &props);
        props.field13 = param_0;
        props.field14 = param_0;
        props.field15 = param;
        props.field16 = retval;
        SC_P_Ai_SetProps(param_0, &props);
        return &props;
    } else {
        return 32;
    }
    tmp = 10000.0f;
    sphere.field3 = 1000.0f;
    sphere = (*param);
    props = 32;
    SC_GetPls(&sphere, &local_2, &props);
    local_34 = 0;
    local_1 = 0;
    if (!(local_1 < props)) {
        SC_P_GetInfo(local_2[local_1], &plinfo);
        SC_P_IsReady(local_2[local_1]);
        SC_P_GetPos(local_2[local_1], &tmp1);
        local_48 = SC_2VectorsDist(&tmp1, param);
        tmp = local_48;
        local_34 = local_2[local_1];
        local_1++;
    }
    return local_34;
}

int func_4086(int param, int param, int param, int param, int param, int param) {
    c_Vector3 local_1;
    c_Vector3 tmp;
    int i;
    s_SC_P_Create local_;
    s_SC_P_getinfo plinfo;

    SC_P_GetInfo(k, &plinfo);
    tmp = plinfo.field3;
    SC_P_GetPos(param_0, &sphere);
    sphere.field3 = 1000.0f;
    local_ = 32;
    SC_GetPls(&sphere, &player_info3.member_id, &local_);
    i = 0;
    local_1 = 0;
    // Loop header - Block 624 @4129
    for (local_1 = 0; (local_1 ? local_); local_1++) {
        if (!(local_1 < local_)) break;  // exit loop @4208
        SC_P_GetInfo(local_4[local_1], &plinfo);
        if (!plinfo.field2 == 1) {
            SC_P_IsReady(local_4[local_1]);
        } else {
            local_1++;
        }
        if (!plinfo.field3 == tmp) goto block_632; // @4199
        goto block_630; // @4168
        local_4[local_1] = param + i * 4;
        i++;
        if (!(i == retval)) {
            SC_Log(3, "GetMyGroup: TOO much players in group around!");
            return 2;
        } else {
        }
    }
    retval = i;
    return retval;
    local_ = 32;
    func_4086(retval, &i, &local_);
    SC_P_GetInfo(retval, &player_info2);
    if (!(local_ < 2)) {
        SC_Log(3, "VC %d %d couldnot find anyone to lead group %d", player_info2.field3, player_info2.field4, player_info2.field3);
        return 5;
    } else {
        func_0064(t4259_0, 64, 0);
        func_0064(i.field1, 64, 0);
        SC_Log(3, "VC %d %d moved command over group", player_info2.field3, player_info2.field4);
        return 4;
    }
    SC_P_GetPos(param_0, &local_);
    tmp = SC_2VectorsDist(param, &local_);
    return tmp;
    SC_ZeroMem(&local_, 20);
    local_ = 0;
    local_.field1 = 0;
    local_.field2 = 0;
    local_.field3 = 0;
    local_.field4 = 0;
    SC_P_SetSpecAnims(retval, &local_);
    return &local_;
    SC_ZeroMem(&local_, 20);
    local_ = param_0;
    local_.field1 = param_0;
    local_.field2 = param_0;
    local_.field3 = param;
    local_.field4 = retval;
    SC_P_SetSpecAnims(param, &local_);
    return &local_;
    local_ = 32;
    SC_GetPls(param, &player_info3.member_id, &local_);
    if (!local_) {
        local_1 = 0;
        SC_P_DoHit(local_4[local_1], 0, retval / 7.0f);
        SC_P_DoHit(local_4[local_1], 1, retval / 7.0f);
        SC_P_DoHit(local_4[local_1], 2, retval / 7.0f);
        SC_P_DoHit(local_4[local_1], 3, retval / 7.0f);
        SC_P_DoHit(local_4[local_1], 4, retval / 7.0f);
        SC_P_DoHit(local_4[local_1], 5, retval / 7.0f);
        SC_P_DoHit(local_4[local_1], 6, retval / 7.0f);
        local_1++;
        return local_1;
    } else {
        return 36;
    }
    SC_P_GetPos(param, &local_);
    local_.field2 = local_.field2 + 1.0f;
    local_.field3 = 1.0f;
    SC_SphereIsVisible(&local_);
    return player_info3.member_id;
    SC_P_GetInfo(param, &local_);
    return local_.field2;
    SC_P_GetInfo(param, &local_);
    return local_.field3;
    SC_P_GetInfo(param, &local_);
    return local_.field4;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_bigbag01.eqp" = param;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_bigbag01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_knife01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_knife01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_littlebag01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_m16ammobox01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_m16ammobox01_0.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_maceta01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_maceta01.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\velka_polni\\EOP_e_pistolcase01.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
}

int func_4670(int param, int param) {
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 8 + 4);
    retval = 2;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_bigbag01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_canteen01_0.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_littlebag01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_m16ammobox01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_m16ammobox01_0.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_e_pistolcase01.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat1US_v01.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\velka_polni\\EOP_hat1US_v01.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\lehke_vybaveni\\EOP_e_canteen01_0.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat1US_v01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_bronson\\lehke_vybaveni\\EOP_hat1US_v01.eqp" = (param + 16 + 4);
    retval = 3;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_hat4US_v01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_hat4US_v01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_bigmedicbag01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_bigmedicbag01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_canteen01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_canteen01_0.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_glasses01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_glasses01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_m16ammobox01_0.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_medicbag01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_medicbag01.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\velka_polni\\EOP_e_pistolcase01.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_glasses01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\lehke_vybaveni\\EOP_e_glasses01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_medicbag01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\lehke_vybaveni\\EOP_e_medicbag01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat4US_v01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_crocker\\lehke_vybaveni\\EOP_hat4US_v01.eqp" = (param + 32 + 4);
    retval = 5;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_hat2US_v01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_hat2US_v01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_e_flashlight01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_e_littlebag01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_e_m16ammobox01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_defort\\velka_polni\\EOP_e_pistolcase01.eqp" = (param + 40 + 4);
    retval = 6;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_defort\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_defort\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat2US_v01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_defort\\lehke_vybaveni\\EOP_hat2US_v01.eqp" = (param + 16 + 4);
    retval = 3;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_pistolcase01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_bigbag01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_canteen01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_canteen01_0.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_flashlight01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_littlebag01.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_m16ammobox01.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_hornster\\velka_polni\\EOP_e_m16ammobox01_0.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_hornster\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_hornster\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 8 + 4);
    retval = 2;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_hat3US_v02.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_hat3US_v02.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_bigbag01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_canteen01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_flashlight01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_littlebag01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_maceta01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_maceta01.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_nhut\\velka_polni\\EOP_e_pistolcase01.eqp" = (param + 48 + 4);
    retval = 7;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_nhut\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_nhut\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat3US_v02.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_nhut\\lehke_vybaveni\\EOP_hat3US_v02.eqp" = (param + 16 + 4);
    retval = 3;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_hat4US_v02.BES" = param;
    *"G\\Equipment\\US\\eqp\\EOP_UH14PH05_01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_rosenfield\\lehke_vybaveni\\EOP_e_ammoboxfp01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_rosenfield\\lehke_vybaveni\\EOP_e_ammoboxfp01_0.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_rosenfield\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_rosenfield\\lehke_vybaveni\\EOP_e_faidpouch01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_rosenfield\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 40 + 4);
    retval = 6;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_bigbag01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_canteen01_0.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_littlebag01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_m16ammobox01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_m16ammobox01_0.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_e_m16ammobox01_1.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hlmt1US_v03.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni\\EOP_hlmt1US_v03.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_hat1US_v01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_hat1US_v01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_bigbag01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_canteen01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_canteen01_0.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_faidpouch01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_littlebag01.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_m16ammobox01.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\velka_polni2\\EOP_e_m16ammobox01_0.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\lehke_vybaveni\\EOP_e_canteen01_0.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\lehke_vybaveni\\EOP_e_faidpouch01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat1US_v01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr01\\lehke_vybaveni\\EOP_hat1US_v01.eqp" = (param + 16 + 4);
    retval = 3;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_bigbag01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_flashlight01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_m16ammobox01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_m16ammobox01_0.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_m16ammobox01_1.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_e_m16ammobox01_2.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hlmt1US_v01.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni\\EOP_hlmt1US_v01.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_ammoboxfp01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_bigbag01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_canteen01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_littlebag01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_m16ammobox01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_m16ammobox01_0.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_e_pistolcase01.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat4US_v01.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\velka_polni2\\EOP_hat4US_v01.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\lehke_vybaveni\\EOP_e_ammoboxfp01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat4US_v01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_SFgncsldr02\\lehke_vybaveni\\EOP_hat4US_v01.eqp" = (param + 24 + 4);
    retval = 4;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\lehke_vybaveni\\EOP_e_ammoboxfp01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat1US_v03.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\lehke_vybaveni\\EOP_hat1US_v03.eqp" = (param + 24 + 4);
    retval = 4;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_bigbag01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_littlebag01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_m16ammobox01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_m16ammobox01_0.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_maceta01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_e_maceta01.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hlmt1US_v03.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni\\EOP_hlmt1US_v03.eqp" = (param + 48 + 4);
    retval = 7;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_faidpouch01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_bigbag01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_canteen01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_littlebag01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_m16ammobox01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_m16ammobox01_0.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_e_pistolcase01.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat6US_v01.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr01\\velka_polni2\\EOP_hat6US_v01.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_hat3US_v03.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\lehke_vybaveni\\EOP_hat3US_v03.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\lehke_vybaveni\\EOP_e_faidpouch01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\lehke_vybaveni\\EOP_e_littlebag01.eqp" = (param + 24 + 4);
    retval = 4;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_flashlight01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_brt1US_v01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_brt1US_v01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_bigbag01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_canteen01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_canteen01_0.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_m16ammobox01.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni\\EOP_e_m16ammobox01_0.eqp" = (param + 48 + 4);
    retval = 7;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_m16ammobox01_0.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_bigbag01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_canteen01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_faidpouch01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_knife01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_knife01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_littlebag01.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_e_m16ammobox01.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat2US_v02.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_LLDBsldr02\\velka_polni2\\EOP_hat2US_v02.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_flashlight01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\lehke_vybaveni\\EOP_e_flashlight01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_brt1US_v01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\lehke_vybaveni\\EOP_brt1US_v01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\lehke_vybaveni\\EOP_e_ammoboxfp01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 32 + 4);
    retval = 5;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_bigbag01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_faidpouch01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_faidpouch01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_littlebag01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_m16ammobox01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_e_m16ammobox01_0.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat2US_v02.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni\\EOP_hat2US_v02.eqp" = (param + 48 + 4);
    retval = 7;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_bigbag01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_ammoboxfp01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_canteen01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_canteen01_0.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_m16ammobox01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_e_m16ammobox01_0.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat3US_v02.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr01\\velka_polni2\\EOP_hat3US_v02.eqp" = (param + 48 + 4);
    retval = 7;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_hat4US_v02.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\lehke_vybaveni\\EOP_hat4US_v02.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\lehke_vybaveni\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\lehke_vybaveni\\EOP_e_littlebag01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = (param + 24 + 4);
    retval = 4;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_knife01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_knife01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_bigbag01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_bigbag01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_canteen01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_littlebag01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_m16ammobox01.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_e_m16ammobox01_0.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hlmt1US_v02.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni\\EOP_hlmt1US_v02.eqp" = (param + 48 + 4);
    retval = 7;
    return FALSE;
    *"G\\Equipment\\US\\bes\\EOP_e_ammoboxfp01.BES" = param;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_ammoboxfp01.eqp" = (param + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = param + 8;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_canteen01.eqp" = (param + 8 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_littlebag01.BES" = param + 16;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_littlebag01.eqp" = (param + 16 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 24;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_m16ammobox01.eqp" = (param + 24 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_m16ammobox01.BES" = param + 32;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_m16ammobox01_0.eqp" = (param + 32 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = param + 40;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_pistolcase01.eqp" = (param + 40 + 4);
    *"G\\Equipment\\US\\bes\\EOP_e_shovel01.BES" = param + 48;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_e_shovel01.eqp" = (param + 48 + 4);
    *"G\\Equipment\\US\\bes\\EOP_hat1US_v02.BES" = param + 56;
    *"G\\Equipment\\US\\eqp\\CUP_CIDGsldr02\\velka_polni2\\EOP_hat1US_v02.eqp" = (param + 56 + 4);
    retval = 8;
    return FALSE;
}

int func_7108(int param, int param) {
    func_4670(param, retval);
    return FALSE;
}

int ScriptMain(s_SC_L_info *info) {
    dword local_39[16];
    int tmp;
    s_SC_P_Create create;
    s_SC_P_getinfo local_;

    if (!(gphase == 0)) {
        SC_ZeroMem(&create, 156);
        SC_ZeroMem(&local_, 80);
        create = 1;
        create.field1 = 0;
        create.field2 = 0;
        create.field3 = 0;
        func_0993();
        create.field6 = "ini\\players\\easy_camo.ini";
        create.field6 = "ini\\players\\default_camo.ini";
        create.field4 = 2500;
        create.field7 = info->elapsed_time;
        func_0318(&create);
        create.field19 = 0;
        create.field18 = 55;
        create.field11 = SC_ggi(102);
        create.field11 = 22;
        create.field11 = 0;
        create.field12 = 0;
        create.field13 = 140;
        create.field14 = 0;
        create.field16 = 51;
        func_7108(&local_, &tmp);
        create.field21 = tmp;
        create.field22 = &local_;
        create.field9 = 4;
        local_66 = t7268_0;
        gphase = 1;
    }
    param_0->field_24 = 0.10000000149011612f;
    SC_P_IsReady(info->param3);
    if (!local_66) {
        gphase = 2;
        SC_P_SetSpeachDist(info->param3, 20.0f);
        func_0772();
        func_0756();
        SC_PC_EnablePronePosition(0);
        SC_PC_EnableFlashLight(1);
        return TRUE;
    } else {
        param_0->field_24 = 1008981770;
        return TRUE;
    }
    switch (gphase) {
    case 1:
        break;
    case 2:
        break;
    default:
    }
    return;
}

