// Structured decompilation of decompilation/TUNNELS01/SCRIPTS/LEVEL.SCR
// Functions: 28

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword gVar;
BOOL gVar1;
BOOL gVar2;
dword gVar3;
dword gVar20;
dword gVar19;
dword gVar17;
dword gVar4;
BOOL gVar5;
dword gVar6;
dword gVar7;
dword gVar8;
int gVar9;
dword gVar10;
dword gVar11;
int gVar12;
dword gVar13;
dword gVar14;
int gVar15;
dword gVar16;
dword gData;
dword gphase;
dword gVar18;

int _init(s_SC_L_info *info) {
    return FALSE;
}

int func_0291(int param, int param) {
    c_Vector3 tmp;

    tmp = frnd(param);
    if (!(tmp < 0)) {
        tmp = -tmp;
    }
    return tmp;
    SC_P_Ai_SetMode(retval, SCM_FEELDANGER);
    SC_P_Ai_EnableShooting(retval, SCM_RUN);
    SC_P_Ai_EnableSituationUpdate(retval, SCM_WARNABOUTENEMY);
    SC_Log(SCM_BOOBYTRAPFOUND, "Player %d enabled", retval);
    return FALSE;
    SC_P_Ai_SetMode(retval, SCM_ENABLE);
    SC_P_Ai_EnableShooting(retval, gVar);
    SC_P_Ai_EnableSituationUpdate(retval, 0);
    SC_P_Ai_Stop(retval);
    SC_Log(3, "Player %d disabled", retval);
    return FALSE;
}

int func_0354(int param, int param, int param) {
    if (!param_0) {
        SC_P_ScriptMessage(param_0, param, retval);
        return FALSE;
    } else {
        SC_Log(3, "Message %d %d to unexisted player!", param, retval);
        return FALSE;
    }
    return;
}

int func_0371(int param, int param, int param) {
    c_Vector3 props;

    SC_P_GetBySideGroupMember(gVar1, j, param);
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
    retval->field_40 = SC_ggi(101);
    if (!((*t619_0))) {
    } else {
        retval->field_40 = 29;
    }
    if (!((*t629_0) == 255)) {
        retval->field_40 = 0;
    }
    retval->field_44 = SC_ggi(102);
    if (!((*t650_0))) {
    } else {
        retval->field_44 = 7;
    }
    if (!((*t660_0) == 255)) {
        retval->field_44 = 0;
    }
    retval->field_48 = SC_ggi(103);
    if (!((*t681_0))) {
    } else {
        SC_ggi(SGI_CURRENTMISSION);
        retval->field_48 = 23;
        SC_ggi(SGI_CURRENTMISSION);
        retval->field_48 = 25;
        retval->field_48 = 1;
    }
    switch (gVar1) {
    case 255:
        retval->field_48 = 0;
        break;
    case 255:
        retval->field_52 = 0;
        break;
    default:
        if ((*t773_0) == 255) {
            retval->field_56 = 0;
        }
        retval->field_60 = SC_ggi(106);
        if ((*t794_0) == 255) {
            retval->field_60 = 0;
        }
        retval->field_64 = SC_ggi(107);
        if ((*t815_0) == 255) {
            retval->field_64 = 0;
        }
        retval->field_68 = SC_ggi(108);
        if ((*t836_0)) {
        } else {
            retval->field_68 = 63;
        }
        if ((*t846_0) == 255) {
            retval->field_68 = 0;
        }
        retval->field_72 = SC_ggi(109);
        if ((*t867_0) == 255) {
            retval->field_72 = PLAYER_AMMOINGUN;
        }
        retval->field_76 = PLAYER_AMMOINPISTOL;
        return FALSE;
    }
    retval->field_56 = 59;
    return;
}

int func_0883(void) {
    SC_PC_Get();
    SC_P_GetWeapons(local_40, &local_0);
    if (!i.field10) {
        SC_sgi(101, t902_0);
    } else {
        SC_sgi(101, 255);
    }
    if (!local_0.field11) {
        SC_sgi(102, t917_0);
    } else {
        SC_sgi(102, 255);
    }
    if (!local_0.field12) {
        SC_sgi(103, t932_0);
    } else {
        SC_sgi(103, 255);
    }
    if (!local_0.field13) {
        SC_sgi(PLAYER_WEAPON1, t947_0);
    } else {
        SC_sgi(PLAYER_WEAPON2, PLAYER_WEAPON3);
    }
    if (!local_0.field14) {
        SC_sgi(PLAYER_WEAPON4, t962_0);
    } else {
        SC_sgi(PLAYER_WEAPON5, PLAYER_WEAPON6);
    }
    if (!local_0.field15) {
        SC_sgi(PLAYER_WEAPON7, t977_0);
    } else {
        SC_sgi(PLAYER_WEAPON8, PLAYER_WEAPON9);
    }
    if (!local_0.field16) {
        SC_sgi(PLAYER_WEAPON10, t992_0);
    } else {
        SC_sgi(107, 255);
    }
    if (!local_0.field17) {
        SC_sgi(108, t1007_0);
    } else {
        SC_sgi(108, 255);
    }
    if (!local_0.field18) {
        SC_sgi(109, t1022_0);
    } else {
        SC_sgi(109, 255);
    }
    if (!local_0.field19) {
        SC_sgi(110, t1037_0);
    } else {
        SC_sgi(110, 255);
    }
    return t1037_0;
    SC_PC_Get();
    SC_P_ReadHealthFromGlobalVar(local_0, 95);
    return FALSE;
}

int func_1054(void) {
    c_Vector3 local_;
    c_Vector3 tmp;

    SC_PC_Get();
    SC_P_WriteHealthToGlobalVar(local_, 95);
    return FALSE;
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

int func_1111(void) {
    SC_PC_Get();
    SC_P_WriteAmmoToGlobalVar(i, 60, 89);
    SC_PC_Get();
    SC_P_GetAmmoInWeap(n, 2);
    SC_sgi(SGI_MISSIONALARM, j);
    SC_PC_Get();
    SC_P_GetAmmoInWeap(local_2, 1);
    SC_sgi(SGI_MISSIONDEATHCOUNT, local_1);
    return FALSE;
}

int func_1146(void) {
    int local_;

    SC_PC_GetIntel(&i);
    local_ = 0;
    // Loop header - Block 111 @1155
    for (local_10 = 0; (local_ ? 10); local_10 = local_ + 1) {
        if (!(local_ < 10)) break;  // exit loop @1179
        SC_sgi(50 + local_, local_0[local_]);
        local_++;
        continue;  // back to loop header @1155
    }
    return local_;
    local_ = 0;
    if (!(local_ < 10)) {
        local_0[local_] = SC_ggi(50 + local_);
        local_++;
    }
    SC_PC_SetIntel(&local_0);
    return &local_0;
    func_0883();
    func_1111();
    func_1054();
    SC_MissionCompleted();
    return FALSE;
}

int func_1223(int param, int param, int param) {
    c_Vector3 local_;
    c_Vector3 local_1;
    c_Vector3 local_128;
    c_Vector3 local_131;
    c_Vector3 local_5;
    c_Vector3 local_6;
    c_Vector3 tmp1;
    c_Vector3 tmp2;
    int local_135;
    int local_137;
    int tmp;
    int tmp3;

    func_1146();
    func_0883();
    func_1111();
    func_1054();
    SC_Osi("MISSION COMPLETE");
    SC_MissionDone();
    return FALSE;
    SC_ShowHelp(&retval, 1, 6.0f);
    return FALSE;
    local_ = param;
    local_.field1 = retval;
    SC_ShowHelp(&local_, 2, 12.0f);
    return 12.0f;
    local_ = i;
    local_.field1 = param;
    local_.field2 = retval;
    SC_ShowHelp(&local_, 3, 24.0f);
    return 24.0f;
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
    goto block_152; // @1401
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
        t2304_0[local_] = 0;
        t2313_0[local_] = 0;
        local_++;
    }
    SC_ggi(SGI_CURRENTMISSION);
    switch (SGI_CURRENTMISSION) {
    case 1:
        t2343_0 = 24;
        t2350_0 + 4 = 38;
        break;
    case 2:
        break;
    case 3:
        break;
    case 4:
        break;
    case 5:
        t2378_0 = 23;
        t2385_0 + 4 = 25;
        break;
    case 16:
        break;
    case 17:
        t2403_0 = 23;
        t2410_0 + 4 = 26;
        t2417_0 + 8 = 24;
        break;
    case 6:
        t2430_0 = 24;
        t2437_0 + 4 = 26;
        t2444_0 + 8 = 38;
        break;
    case 7:
        break;
    case 8:
        t2462_0 = 23;
        t2469_0 + 4 = 24;
        t2476_0 + 8 = 25;
        break;
    case 9:
        break;
    case 11:
        break;
    case 10:
        t2499_0 = 23;
        t2506_0 + 4 = 25;
        break;
    case 12:
        t2519_0 = 23;
        t2526_0 + 4 = 24;
        t2533_0 + 8 = 25;
        t2540_0 + 12 = 37;
        t2547_0 + 16 = 38;
        break;
    case 13:
        break;
    case 14:
        break;
    case 15:
        t2570_0 = 23;
        t2577_0 + 4 = 25;
        break;
    case 18:
        break;
    case 19:
        break;
    case 20:
        t2600_0 = 27;
        t2607_0 + 4 = 28;
        t2614_0 + 8 = 31;
        break;
    case 21:
        t2627_0 = 27;
        t2634_0 + 4 = 28;
        t2641_0 + 8 = 31;
        t2648_0 + 12 = 35;
        break;
    case 22:
        break;
    case 23:
        t2666_0 = 35;
        t2673_0 + 4 = 27;
        t2680_0 + 8 = 32;
        t2687_0 + 12 = 33;
        t2694_0 + 16 = 34;
        break;
    case 24:
        t2707_0 = 23;
        t2714_0 + 4 = 25;
        break;
    case 26:
        break;
    case 27:
        break;
    case 28:
        t2737_0 = 26;
        t2744_0 + 4 = 27;
        t2751_0 + 8 = 28;
        t2758_0 + 12 = 31;
        break;
    case 25:
        t2771_0 = 31;
        t2778_0 + 4 = 35;
        t2785_0 + 8 = 36;
        break;
    case 29:
        t2798_0 = 35;
        t2805_0 + 4 = 32;
        t2812_0 + 8 = 33;
        t2819_0 + 12 = 34;
        break;
    case 30:
        break;
    case 31:
        break;
    case 32:
        t2842_0 = 33;
        t2849_0 + 4 = 34;
        t2856_0 + 8 = 35;
        t2863_0 + 12 = 36;
        break;
    default:
        t2872_0 = 35;
        t2879_0 + 4 = 27;
        t2886_0 + 8 = 32;
        t2893_0 + 12 = 33;
        t2900_0 + 16 = 34;
        return local_1;
    }
    tmp = 100.0f;
    SC_ggi(SGI_GAMETYPE);
    if (!local_138) {
        SC_P_GetPos(param_0, &local_131);
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

int func_3368(int param, int param, int param, int param) {
    c_Vector3 i;
    c_Vector3 local_2;
    c_Vector3 local_6;
    c_Vector3 props;
    c_Vector3 tmp;
    int local_;
    int local_4;

    i = SC_NOD_Get(0, param);
    if (!(i != 0)) {
        SC_NOD_GetWorldPos(i, retval);
    }
    return retval;
    i = SC_NOD_Get(0, param);
    if (!(i != 0)) {
        SC_NOD_GetWorldRotZ(i);
        return tmp;
    } else {
        return FALSE;
    }
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_GetPeaceMode(tmp);
    if (!(i == 2)) {
        SC_P_GetBySideGroupMember(0, 0, 1);
        SC_P_Ai_SetPeaceMode(i, 0);
    }
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_Stop(i);
    return FALSE;
    func_3368(param, &i);
    SC_DoExplosion(&i, retval);
    return retval;
    local_ = SC_NOD_Get(0, retval);
    if (!local_) {
        SC_NOD_GetWorldPos(local_, &tmp);
        i = SC_NOD_GetWorldRotZ(local_);
        i = i - 1.5700000524520874f;
        local_4 = tmp;
        cos(i);
        local_4 = 2.0f - i * ai_props.shortdistance_fight;
        sin(i);
        local_4.field1 = 2.0f + i * ai_props.shortdistance_fight;
        SC_DoExplosion(&local_4, 1);
        local_4 = tmp;
        cos(i);
        local_4 = 4.0f - i * ai_props.shortdistance_fight;
        sin(i);
        local_4.field1 = 4.0f + i * ai_props.shortdistance_fight;
        SC_DoExplosion(&local_4, 2);
        local_4 = tmp;
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
    func_3368(j, &local_4);
    tmp.field2 = local_4.field2;
    i = 0;
    if (!(i < param)) {
        frnd(retval);
        tmp = retval + ai_props.shoot_imprecision;
        frnd(retval);
        tmp.field1 = retval + ai_props.shoot_imprecision;
        SC_DoExplosion(&tmp, param_0);
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
    tmp.field2 = (*t3850_0);
    i = 0;
    if (!(i < param)) {
        frnd(retval);
        tmp = retval + ai_props.watchfulness_maxdistance;
        frnd(retval);
        tmp.field1 = retval + ai_props.watchfulness_maxdistance;
        SC_CreatePtc(198, &tmp);
        SC_CreatePtcVec_Ext(177, &tmp, 5.0f, 0.0f, 1.0f, 1.0f);
        i++;
    }
    SC_CreatePtcVec_Ext(176, param_0, 1000.0f, 0.0f, 1.0f, 1.0f);
    return 1.0f;
    tmp.field2 = (*t3924_0);
    i = 0;
    if (!(i < param)) {
        frnd(retval);
        tmp = retval + ai_props.watchfulness_maxdistance;
        frnd(retval);
        tmp.field1 = retval + ai_props.watchfulness_maxdistance;
        SC_CreatePtc(198, &tmp);
        i++;
    }
    SC_CreatePtcVec_Ext(176, param_0, 1000.0f, 0.0f, 1.0f, 1.0f);
    return 1.0f;
    tmp.field2 = (*t3990_0);
    i = 0;
    if (!(i < param)) {
        frnd(retval);
        tmp = retval + ai_props.watchfulness_maxdistance;
        frnd(retval);
        tmp.field1 = retval + ai_props.watchfulness_maxdistance;
        SC_CreatePtc(198, &tmp);
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
        tmp = local_2;
        i++;
    }
    return tmp;
}

int func_4180(int param, int param, int param, int param, int param) {
    c_Vector3 local_1;
    c_Vector3 props;
    c_Vector3 tmp1;
    int local_48;
    int tmp;
    s_SC_P_getinfo local_;
    s_SC_P_getinfo plinfo;
    s_sphere sphere;

    SC_P_GetPos(param_0, &props);
    SC_IsNear3D(&props, param_0, param);
    return ai_props.boldness;
    SC_PC_GetPos(&props);
    SC_IsNear3D(&props, param_0, param);
    return ai_props.boldness;
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
    SC_GetPls(&sphere, &ai_props.watchfulness_maxdistance, &props);
    local_ = 0;
    local_1 = 0;
    if (!(local_1 < props)) {
        SC_P_GetInfo(local_2[local_1], &plinfo);
        SC_P_IsReady(local_2[local_1]);
        SC_P_GetPos(local_2[local_1], &tmp1);
        local_48 = SC_2VectorsDist(&tmp1, param);
        tmp = local_48;
        local_ = local_2[local_1];
        local_1++;
    }
    return local_;
}

int func_4376(int param, int param, int param) {
    c_Vector3 i;
    c_Vector3 local_;
    c_Vector3 local_1;
    c_Vector3 tmp;
    s_SC_P_getinfo plinfo;

    SC_P_GetInfo(k, &plinfo);
    tmp = plinfo.field3;
    SC_P_GetPos(param_0, &sphere);
    sphere.field3 = 1000.0f;
    local_ = 32;
    SC_GetPls(&sphere, &local_4, &local_);
    i = 0;
    local_1 = 0;
    // Loop header - Block 624 @4419
    for (local_1 = 0; (local_1 ? local_); local_1++) {
        if (!(local_1 < local_)) break;  // exit loop @4498
        SC_P_GetInfo(local_4[local_1], &plinfo);
        if (!plinfo.field2 == 1) {
            SC_P_IsReady(local_4[local_1]);
        } else {
            local_1++;
        }
        if (!plinfo.field3 == tmp) goto block_632; // @4489
        goto block_630; // @4458
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
    func_4376(retval, &i, &local_);
    SC_P_GetInfo(retval, &player_info2);
    if (!(local_ < 2)) {
        SC_Log(3, "VC %d %d couldnot find anyone to lead group %d", player_info2.field3, player_info2.field4, player_info2.field3);
        return 5;
    } else {
        func_0354(t4549_0, 64, 0);
        func_0354(i.field1, 64, 0);
        SC_Log(3, "VC %d %d moved command over group", player_info2.field3, player_info2.field4);
        return 4;
    }
    return;
}

int func_4575(int param, int param, int param, int param, int param, int param) {
    c_Vector3 local_;
    c_Vector3 local_0;
    c_Vector3 tmp;

    SC_P_GetPos(j, &local_0);
    tmp = SC_2VectorsDist(param, &local_0);
    return tmp;
    SC_ZeroMem(&local_0, 20);
    local_0 = 0;
    local_0.field1 = 0;
    local_0.field2 = 0;
    local_0.field3 = 0;
    local_0.field4 = 0;
    SC_P_SetSpecAnims(retval, &local_0);
    return &local_0;
    SC_ZeroMem(&local_0, 20);
    local_0 = param_0;
    local_0.field1 = param_0;
    local_0.field2 = param_0;
    local_0.field3 = param;
    local_0.field4 = retval;
    SC_P_SetSpecAnims(param, &local_0);
    return &local_0;
    local_0 = 32;
    SC_GetPls(param, &player_info.member_id, &local_0);
    if (!local_0) {
        local_ = 0;
        SC_P_DoHit(local_4[local_], 0, retval / 7.0f);
        SC_P_DoHit(local_4[local_], 1, retval / 7.0f);
        SC_P_DoHit(local_4[local_], 2, retval / 7.0f);
        SC_P_DoHit(local_4[local_], 3, retval / 7.0f);
        SC_P_DoHit(local_4[local_], 4, retval / 7.0f);
        SC_P_DoHit(local_4[local_], 5, retval / 7.0f);
        SC_P_DoHit(local_4[local_], 6, retval / 7.0f);
        local_++;
        return local_;
    } else {
        return 36;
    }
    SC_P_GetPos(param, &local_0);
    local_0.field2 = local_0.field2 + 1.0f;
    local_0.field3 = 1.0f;
    SC_SphereIsVisible(&local_0);
    return player_info.member_id;
    SC_P_GetInfo(param, &local_0);
    return local_0.field2;
    SC_P_GetInfo(param, &local_0);
    return local_0.field3;
    SC_P_GetInfo(param, &local_0);
    return local_0.field4;
    local_0 = 0;
    if (!(local_0 < objcount)) {
        local_0++;
    }
    objcount = 0;
    return &objcount;
    local_0 = 0;
    if (!(local_0 < objcount)) {
        SC_Log(1, "Duplicite objective added - %d", retval);
        return 3;
        local_0++;
    }
    Objectives[objcount] = retval;
    Objectives[objcount].field1 = 0;
    objcount++;
    SC_SetObjectives(objcount, &Objectives, 6.0f);
    return 6.0f;
}

int func_4948(int param, int param) {
    c_Vector3 local_;
    c_Vector3 local_1;
    c_Vector3 tmp;

    local_ = 0;
    // Loop header - Block 665 @4953
    for (local_0 = 0; (local_ ? 0); local_0 = local_ + 1) {
        if (!(local_ < objcount)) break;  // exit loop @4982
        if (!Objectives[local_] == retval) {
            SC_Log(1, "Duplicite objective added - %d", retval);
            return 3;
        } else {
            local_++;
        }
    }
    Objectives[objcount] = retval;
    Objectives[objcount].field1 = 0;
    objcount++;
    SC_SetObjectivesNoSound(objcount, &Objectives, 6.0f);
    return 6.0f;
    local_ = 0;
    if (!(local_ < objcount)) {
        Objectives[local_].field1 = 2;
        SC_SetObjectives(objcount, &Objectives, 6.0f);
        return 6.0f;
        local_++;
    }
    return local_;
    local_ = 0;
    if (!(local_ < objcount)) {
        Objectives[local_].field1 = 1;
        local_++;
    }
    SC_SetObjectives(objcount, &Objectives, 6.0f);
    return 6.0f;
    local_ = 0;
    if (!(local_ < objcount)) {
        return (*Objectives[local_].field1);
        local_++;
    }
    if (!(local_ < 5)) {
        SC_P_GetBySideGroupMember(0, 0, local_);
        SC_P_IsReady(tmp);
        SC_P_GetBySideGroupMember(0, 0, local_);
        local_1 = SC_P_Ai_GetPeaceMode(tmp);
        lastorder = local_1;
        return local_1;
    }
    return FALSE;
}

int func_5197(int param, int param) {
    c_Vector3 local_;
    c_Vector3 local_0;
    c_Vector3 local_6;
    c_Vector3 tmp1;
    dword local_30[16];
    dword local_36[16];
    int local_10;
    int local_11;
    int tmp;
    int tmp2;

    SC_sgi(SGI_MISSIONDEATHCOUNT, 0);
    SC_sgi(SGI_MISSIONALARM, 0);
    SC_sgi(SGI_LEVELPHASE, 0);
    SC_sgi(SGI_ALLYDEATHCOUNT, 0);
    SC_sgi(SGI_TEAMDEATHCOUNT, 0);
    SC_sgi(SGI_TEAMWIA, 0);
    SC_sgi(SGI_INTELCOUNT, 0);
    SC_sgi(SGI_CHOPPER, 0);
    SC_sgi(SGI_GAMETYPE, 0);
    SC_ggi(SGI_DIFFICULTY);
    SC_Log("Level difficulty is %d", 10, vec.z);
    return FALSE;
    SC_ZeroMem(&local_0, 120);
    SC_ZeroMem(&local_30, 24);
    SC_ZeroMem(&local_36, 24);
    local_0 = 0;
    local_0.field5 = 5.0f;
    local_0.field10 = 1.5f;
    local_0.field15 = 1.5f;
    local_0.field20 = 2.0f;
    tmp = 0;
    if (!(tmp < 5)) {
        local_0[tmp].field1 = local_0[tmp] + 1.0f;
        local_0[tmp].field2 = frnd(0.5f);
        (local_0[tmp].field2 + 4) = frnd(0.5f);
        (local_0[tmp].field2 + 8) = 0;
        tmp++;
    }
    local_30 = 1;
    local_30.field1 = 4;
    local_30.field2 = 5;
    local_30.field3 = 2;
    local_30.field4 = 3;
    local_36 = 1;
    local_36.field1 = 5;
    local_36.field2 = 3;
    local_36.field3 = 4;
    local_36.field4 = 2;
    SC_Ai_SetPlFollow(0, 0, 0, &local_0, &local_30, &local_36, 5);
    local_0 = 0;
    local_0.field5 = 4.0f;
    local_0.field10 = 1.5f;
    local_0.field15 = 1.5f;
    local_0.field20 = 1.5f;
    local_0.field25 = 2.0f;
    tmp = 0;
    if (!(tmp < 6)) {
        local_0[tmp].field1 = local_0[tmp] + 1.0f;
        local_0[tmp].field2 = frnd(0.20000000298023224f);
        (local_0[tmp].field2 + 4) = frnd(0.20000000298023224f);
        (local_0[tmp].field2 + 8) = 0;
        local_36[tmp] = 0;
        tmp++;
    }
    local_30 = 0;
    local_30.field1 = 1;
    local_30.field2 = 4;
    local_30.field3 = 5;
    local_30.field4 = 2;
    local_30.field5 = 3;
    SC_Ai_SetPlFollow(0, 0, 1, &local_0, &local_30, &local_36, 6);
    return 6;
    SC_RadioSetDist(10.0f);
    return 10.0f;
    if (!reportedcontact) {
        return FALSE;
    } else {
        local_ = SC_P_GetBySideGroupMember(0, 0, 4);
        return FALSE;
        SC_P_Ai_GetSureEnemies(local_);
        SC_ggi(SGI_MISSIONALARM);
        return FALSE;
        reportedcontact = 1;
        SC_P_GetBySideGroupMember(0, 0, 4);
        SC_P_Speach(vec.z, 4010, 4010, &local_0);
        local_0 = local_0 + 1.0f;
        SC_SpeachRadio(5013, 5013, &local_0);
        return TRUE;
    }
    SC_ZeroMem(&Objectives, 0);
    local_0 = 0;
    if (!(local_0 < 0)) {
        Objectives[local_0].field5 = 0;
        Objectives[local_0].field3 = 1.0f;
        Objectives[local_0].field4 = 1;
        Objectives[local_0].field7 = 0;
        Objectives[local_0].field8 = 0;
        local_0++;
    }
    return local_0;
    SC_Log(3, "adding trap on pos %d", param);
    Objectives[param].field4 = 2;
    Objectives[(param + 1)].field4 = 2;
    Objectives[param].field6 = param + 1;
    Objectives[(param + 1)].field6 = param;
    Objectives[param].field7 = 4;
    Objectives[(param + 1)].field7 = 4;
    tmp1 = SC_NOD_Get(retval, "Plechovka");
    if (!tmp1) {
        SC_NOD_GetWorldPos(tmp1, &local_0);
        tmp1 = SC_NOD_Get(retval, "Konec dratu");
        SC_NOD_GetWorldPos(tmp1, &vec2);
        local_6 = vec2 - local_0;
        local_6.field1 = vec2.field1 - local_0.field1;
        local_6.field2 = vec2.field2 - local_0.field2;
        SC_VectorLen(&local_6);
        t5888_0 = FTOD((&local_6) * local_12);
        t5891_0 = DMUL(1077936128, t5888_0, t5888_1, (*0));
        t5894_0 = DADD(&vec2, t5891_0, t5891_1, (*0));
        local_10 = t5895_0;
        Objectives[param].field3 = local_10;
        Objectives[(param + 1)].field3 = local_10;
        Objectives[param] = local_0 + 0.25f * local_6;
        Objectives[param].field1 = local_0.field1 + 0.25f * local_6.field1;
        Objectives[param].field2 = local_0.field2 + 0.25f * local_6.field2;
        Objectives[(param + 1)] = local_0 + 0.75f * local_6;
        Objectives[(param + 1)].field1 = local_0.field1 + 0.75f * local_6.field1;
        Objectives[(param + 1)].field2 = local_0.field2 + 0.75f * local_6.field2;
        return Objectives[(param + 1)].field2;
    } else {
        SC_message("trap not found!!!");
        return TRUE;
    }
    tmp2 = SC_NOD_Get(param, "Plechovka");
    if (!tmp2) {
        SC_NOD_GetWorldPos(tmp2, &vec2.z);
        tmp2 = SC_NOD_Get(param, "Konec dratu");
        SC_NOD_GetWorldPos(tmp2, &vec4);
        local_11 = vec4 - vec2.z;
        local_11.field1 = vec4.field1 - vec2.z.field1;
        local_11.field2 = vec4.field2 - vec2.z.field2 + 10000.0f;
        local_ = vec2.z + 0.25f * local_11;
        local_.field1 = vec2.z.field1 + 0.25f * local_11.field1;
        local_.field2 = vec2.z.field2 + 0.25f * local_11.field2;
        local_0 = 0;
        SC_IsNear2D(&Objectives[local_0], &local_, 1.0f);
        Objectives[local_0].field5 = 1;
        Objectives[(local_0 + 1)].field5 = 1;
        SC_Log(3, "removing trap %d", local_0);
        return local_0;
        local_0++;
        return -1;
    } else {
        SC_message("trap not found!!!");
        return -1;
    }
    return;
}

int func_6196(int param, int param) {
    goto block_736; // @6203
    if (!(local_0 == 0)) {
        return TRUE;
    } else {
        return TRUE;
        return TRUE;
        return TRUE;
        return TRUE;
        return FALSE;
    }
    return;
}

int func_6259(int param, int param) {
    c_Vector3 i;
    c_Vector3 idx;
    c_Vector3 local_;
    c_Vector3 local_2;
    c_Vector3 local_9;
    c_Vector3 tmp;
    c_Vector3 tmp1;
    int tmp2;

    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_GetPeaceMode(i);
    if (!(idx == 2)) {
        SC_Ai_SetPeaceMode(0, 0, 0);
        SC_Ai_PointStopDanger(0, 0);
    }
    return FALSE;
    alarmtype = 0;
    tmp = pointstatus;
    i = 0;
    if (!(i < 6)) {
        local_ = SC_P_GetBySideGroupMember(0, 0, i);
        SC_P_IsReady(local_);
        SC_P_GetPos(local_, &tmp1);
        idx = 0;
        SC_IsNear3D(&Objectives[idx], &tmp1, t6360_0);
        func_6196(t6375_0);
        local_2 = 0;
        SC_P_ScriptMessage(local_, 4, 1);
        SC_P_ScriptMessage(local_, 4, 0);
        trapfound = 1;
        pointstatus = 1;
        Objectives[(*Objectives[idx].field6)].field5 = 1;
        local_2 = 0;
        SC_P_Speech2(local_, 4062, &local_2);
        local_2 = local_2 + 0.10000000149011612f;
        pointstatus = 20;
        SC_P_Speech2(local_, 4061, &local_2);
        local_2 = local_2 + 0.10000000149011612f;
        local_2 = 0;
        SC_P_Speech2(local_, enemydangertext, &local_2);
        local_2 = local_2 + 0.10000000149011612f;
        func_6259();
        pointstatus = 2;
        local_2 = 0;
        SC_P_Speech2(local_, 4884, &local_2);
        local_2 = local_2 + 0.10000000149011612f;
        func_6259();
        SC_P_ScriptMessage(local_, 4, 1);
        SC_P_ScriptMessage(local_, 4, 0);
        trapfound = 1;
        pointstatus = 10;
        alarmtype = (*Objectives[idx].field4);
        alarmer = i;
        func_6196((*Objectives[idx].field8));
        Objectives[idx].field5 = 1;
        SC_Log(3, "%d found on alarm spot %d by %d", alarmtype, idx, i);
        return idx;
        idx++;
        i++;
    }
    switch (pointstatus) {
    case 1:
        break;
    case 2:
        break;
    case 3:
        break;
    case 4:
        break;
    case 5:
        break;
    case 10:
        break;
    default:
    }
    return -1;
    if (!(param < retval)) {
        retval++;
        SC_Ai_ClearCheckPoints(0, 0);
        idx = param;
        sprintf(&i, "point", idx);
        SC_GetWp(&i, &local_9);
        SC_Ai_AddCheckPoint(0, 0, &local_9, 0);
        idx++;
    } else {
        retval--;
        SC_Ai_ClearCheckPoints(0, 0);
        idx = param;
        sprintf(&i, "point", idx);
        SC_GetWp(&i, &local_9);
        SC_Ai_AddCheckPoint(0, 0, &local_9, 0);
        idx--;
    }
    return idx;
    retval++;
    idx = param;
    if (!(idx < retval)) {
        sprintf(&i, "point", idx);
        SC_GetWp(&i, &local_9);
        SC_Ai_AddCheckPoint(0, 0, &local_9, 0);
        idx++;
    }
    return idx;
}

int func_6804(void) {
    c_Vector3 local_;
    c_Vector3 local_1;
    c_Vector3 tmp;

    local_ = 1;
    // Loop header - Block 816 @6810
    for (local_0 = 1; (local_ ? 6); local_0 = local_ + 1) {
        if (!(local_ < 6)) break;  // exit loop @6861
        SC_P_GetBySideGroupMember(0, 0, local_);
        SC_P_IsReady(tmp);
        if (!local_2) {
        } else {
            local_++;
        }
        SC_P_GetBySideGroupMember(0, 0, local_);
        local_1 = SC_P_Ai_GetPeaceMode(tmp);
        if (!(local_1 != 0)) {
            return local_1;
        } else {
        }
    }
    return FALSE;
    func_6804(0, 0);
    SC_Ai_SetPeaceMode(0, 0, local_2);
    return FALSE;
}

int func_6873(void) {
    c_Vector3 local_;
    c_Vector3 tmp;
    int tmp1;

    local_ = 0;
    // Loop header - Block 825 @6879
    for (local_0 = 0; (local_ ? 14); local_0 = local_ + 1) {
        if (!(local_ < 14)) break;  // exit loop @6946
        AP[local_].field6 = 0;
        sprintf(&tmp, "ACTIVEPLACE#%d", local_);
        func_3368(&tmp, &AP[local_]);
        AP[local_].field3 = 2.0f;
        AP[local_].field4 = 0;
        AP[local_].field5 = -1.0f;
        local_++;
        continue;  // back to loop header @6879
    }
    AP.field5 = 30.0f;
    AP.field7.field5 = 15.0f;
    AP.field49.field6 = -100;
    SC_GetWp("WayPoint113", &vcrunpoint);
    SC_GetWp("WayPoint#33", &vcrunpoint2);
    return tmp1;
}

int func_6984(int param) {
    switch (local_0) {
    case 0:
        break;
    case 1:
        AP[retval].field4 = 0;
        AP[retval].field6 = 1;
        break;
    case 2:
        break;
    default:
    }
    if (!(local_0 == 4)) {
    } else {
        return FALSE;
    }
    return;
}

int func_7043(int param) {
    c_Vector3 local_;
    c_Vector3 local_1;
    c_Vector3 local_5;
    int tmp;

    SC_PC_Get();
    SC_P_GetWillTalk(local_5);
    local_ = local_4 + 0.20000000298023224f;
    switch (vcgroup2) {
    case 0:
        if ((*AP[retval].field6) == 0) {
            SC_PC_Get();
            SC_P_Speech2(local_5, 903, &local_);
            local_ = local_ + 0.10000000149011612f;
        } else {
            SC_PC_Get();
            SC_P_Speech2(local_5, 904, &local_);
            local_ = local_ + 0.10000000149011612f;
        }
        AP[retval].field6 = -100;
        AP[retval].field4 = (*AP[retval].field5);
        break;
    case 1:
        if ((*AP[retval].field6) == 0) {
            rand();
            if ((local_5 % 2)) {
                SC_PC_Get();
                SC_P_Speech2(local_5, 905, &local_);
                local_ = local_ + 0.10000000149011612f;
            } else {
                SC_PC_Get();
                SC_P_Speech2(local_5, 911, &local_);
                local_ = local_ + 0.10000000149011612f;
            }
        } else {
            SC_PC_Get();
            func_4575(&AP[retval]);
            SC_PC_Get();
            func_4575(tmp, &AP.field49);
            if (&AP.field49 < local_6) {
                SC_PC_Get();
                rand();
                SC_P_Speech2(local_5, 908 + tmp % 3, &local_);
                local_ = local_ + 0.10000000149011612f;
            }
        }
        AP[retval].field6 = -100;
        AP[retval].field4 = (*AP[retval].field5);
        break;
    case 2:
        SC_PC_Get();
        SC_P_Speech2(local_5, 906, &local_);
        local_ = local_ + 0.10000000149011612f;
        AP[retval].field6 = -100;
        break;
    case 3:
        SC_PC_Get();
        SC_P_SpeechMes2(local_5, 907, &local_, 11);
        local_ = local_ + 0.10000000149011612f;
        AP[retval].field6 = -100;
        break;
    case 4:
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(local_5, &local_1);
        SC_SND_PlaySound3D(2060, &local_1);
        local_ = local_ + 0.10000000149011612f;
        SC_PC_Get();
        SC_P_SpeechMes2(local_5, 912, &local_, 12);
        local_ = local_ + 0.10000000149011612f;
        local_ = 0.5f;
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Speech2(local_5, 913, &local_);
        local_ = local_ + 0.10000000149011612f;
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_Speech2(local_5, 914, &local_);
        local_ = local_ + 0.10000000149011612f;
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SpeechMes2(local_5, 915, &local_, 13);
        local_ = local_ + 0.10000000149011612f;
        AP[retval].field6 = -100;
        break;
    case 5:
        SC_PC_Get();
        SC_P_Speech2(local_5, 921, &local_);
        local_ = local_ + 0.10000000149011612f;
        AP[retval].field6 = -100;
        break;
    case 6:
        SC_PC_Get();
        SC_P_Speech2(local_5, 922, &local_);
        local_ = local_ + 0.10000000149011612f;
        AP[retval].field6 = -100;
        break;
    case 8:
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_SpeechMes2(local_5, 924, &local_, 14);
        local_ = local_ + 0.10000000149011612f;
        AP[retval].field6 = -100;
        break;
    case 9:
        AP[retval].field6 = -100;
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_PEACE);
        SC_GetWp("WayPoint113", &local_1);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_Go(local_5, &local_1);
        break;
    case 10:
        if (vcgroup2) {
            SC_PC_Get();
            SC_P_SpeechMes2(local_5, 932, &local_, 15);
            local_ = local_ + 0.10000000149011612f;
            AP[retval].field6 = -100;
        }
        break;
    case 11:
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetPos(local_5, &local_1);
        SC_SND_PlaySound3D(10419, &local_1);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_GetPos(local_5, &local_1);
        SC_SND_PlaySound3D(10419, &local_1);
        SC_PC_Get();
        SC_P_Speech2(local_5, 944, &local_);
        local_ = local_ + 0.10000000149011612f;
        vcdiggers = 1;
        AP[retval].field6 = -100;
        break;
    case 13:
        SC_AGS_Set(1);
        AP[retval].field6 = -100;
        break;
    case 12:
        func_1223();
        AP[retval].field6 = -100;
        break;
    default:
        return local_5;
    }
    return;
}

int func_7697(float time, int param) {
    c_Vector3 local_;

    local_ = 0;
    // Loop header - Block 885 @7702
    for (local_0 = 0; (local_ ? 14); local_0 = local_ + 1) {
        if (!(local_ < 14)) break;  // exit loop @7755
        if (!(*AP[local_].field4) > 0) {
            func_6984(local_);
        } else {
            local_++;
        }
        AP[local_].field4 = (*AP[local_].field4) - retval;
        if (!(*AP[local_].field4) < 0) goto block_889; // @7746
    }
    local_ = 0;
    // Loop header - Block 891 @7759
    for (local_0 = 0; (local_ ? 14); local_0 = local_ + 1) {
        if (!(local_ < 14)) break;  // exit loop @7806
        if (!(*AP[local_].field6) != -100) {
            func_7043(local_);
            return local_;
        } else {
            local_++;
        }
        SC_IsNear3D(time, &AP[local_], t7786_0);
        if (!local_1) goto block_896; // @7797
    }
    return local_;
}

int func_7807(float time) {
    c_Vector3 local_;
    c_Vector3 local_2;
    c_Vector3 local_5;
    c_Vector3 local_6;
    c_Vector3 local_9;
    c_Vector3 tmp;
    c_Vector3 tmp1;
    int local_7;

    switch (vc1stat) {
    case 0:
        SC_P_GetBySideGroupMember(1, 0, 0);
        if (!SC_P_IsReady(local_7)) break;
        if (!func_0371(0, 0)) break;
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Speech2(local_6, 926, &local_);
        local_ = local_ + 0.10000000149011612f;
        vc1stat = 1;
        break;
    case 1:
        SC_P_GetBySideGroupMember(1, 0, 0);
        if (SC_P_IsReady(local_7)) {
        } else {
            SC_PC_Get();
            local_ = SC_P_GetWillTalk(local_7);
            SC_PC_Get();
            SC_P_Speech2(local_6, 927, &local_);
            local_ = local_ + 0.10000000149011612f;
            vc1stat = 100;
        }
        SC_P_GetBySideGroupMember(1, 0, 0);
        if (func_4180(&vcrunpoint, 5.0f)) {
            SC_P_GetBySideGroupMember(1, 0, 0);
            SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_BATTLE);
            vc1stat = 2;
        }
        break;
    case 2:
        SC_P_GetBySideGroupMember(1, 0, 0);
        if (SC_P_Ai_GetShooting(local_7, &tmp)) {
            SC_PC_Get();
            local_ = SC_P_GetWillTalk(local_7);
            SC_PC_Get();
            SC_P_Speech2(local_6, 929, &local_);
            local_ = local_ + 0.10000000149011612f;
            vc1stat = 3;
        }
        break;
    case 3:
        SC_P_GetBySideGroupMember(1, 0, 0);
        if (SC_P_IsReady(local_7)) {
        } else {
            SC_PC_Get();
            local_ = SC_P_GetWillTalk(local_7);
            SC_PC_Get();
            SC_P_Speech2(local_6, 927, &local_);
            local_ = local_ + 0.10000000149011612f;
            vc1stat = 100;
        }
        vc1timer = vc1timer + retval;
        if (vc1timer > 3.0f) {
            SC_P_GetBySideGroupMember(1, 0, 0);
            SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_PEACE);
            SC_P_GetBySideGroupMember(1, 0, 0);
            SC_P_Ai_Go(local_6, &vcrunpoint2);
            SC_PC_Get();
            SC_P_GetWillTalk(local_7);
            local_ = local_6 + 0.20000000298023224f;
            SC_PC_Get();
            SC_P_Speech2(local_6, 930, &local_);
            local_ = local_ + 0.10000000149011612f;
            vc1stat = 4;
        }
        break;
    case 4:
        SC_P_GetBySideGroupMember(1, 0, 0);
        if (func_4180(&vcrunpoint, 5.0f)) {
            SC_P_GetBySideGroupMember(1, 0, 0);
            SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_BATTLE);
            vc1stat = 5;
        }
        break;
    default:
        if (vcgroup2) {
        } else {
            SC_P_GetBySideGroupMember(1, 0, 5);
            if (SC_P_IsReady(local_6)) {
            } else {
                SC_P_GetBySideGroupMember(1, 0, 4);
                if (SC_P_IsReady(local_6)) {
                } else {
                    SC_P_GetBySideGroupMember(1, 0, 0);
                    if (SC_P_IsReady(local_6)) {
                    } else {
                        vcgroup2 = 1;
                        SC_PC_Get();
                        SC_P_GetWillTalk(local_6);
                        local_ = local_5 + 0.5f;
                        SC_PC_Get();
                        SC_P_Speech2(local_5, 931, &local_);
                        local_ = local_ + 0.10000000149011612f;
                    }
                }
            }
        }
        if (vcdiggers != 100 && local_5) {
            SC_P_GetBySideGroupMember(1, 1, 0);
            rand();
            SC_P_Speech2(local_5, 947 + local_7 % 2, &local_);
            local_ = local_ + 0.10000000149011612f;
            SC_P_GetBySideGroupMember(1, 1, 0);
            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
            SC_P_GetBySideGroupMember(1, 1, 1);
            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
            SC_P_GetBySideGroupMember(1, 1, 2);
            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
            vcdiggers = 100;
        }
        if (vcdiggers != 100 && local_5) {
            SC_P_GetBySideGroupMember(1, 1, 1);
            rand();
            SC_P_Speech2(local_5, 947 + local_7 % 2, &local_);
            local_ = local_ + 0.10000000149011612f;
            SC_P_GetBySideGroupMember(1, 1, 0);
            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
            SC_P_GetBySideGroupMember(1, 1, 1);
            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
            SC_P_GetBySideGroupMember(1, 1, 2);
            SC_P_Ai_SetMode(local_5, SGI_INTELCOUNT);
            vcdiggers = 100;
        }
        if (vcdiggers != 100 && local_5) {
            SC_P_GetBySideGroupMember(1, 1, 2);
            rand();
            SC_P_Speech2(local_5, 947 + local_7 % 2, &local_);
            local_ = local_ + 0.10000000149011612f;
            SC_P_GetBySideGroupMember(1, 1, 0);
            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
            SC_P_GetBySideGroupMember(1, 1, 1);
            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
            SC_P_GetBySideGroupMember(1, 1, 2);
            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
            vcdiggers = 100;
        }
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_Stop(local_6);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_Stop(local_6);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_Stop(local_6);
        frnd(20.0f);
        vcdiggertimer = 20.0f + local_7;
        rand();
        diggertarget = local_6 % 2;
        SC_P_GetBySideGroupMember(1, 1, diggertarget);
        SC_P_GetPos(local_6, &local_2);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_Go(local_6, &local_2);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_GetPos(local_6, &diggerstart);
        vcdiggers = 2;
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_GetBySideGroupMember(1, 1, diggertarget);
        SC_P_GetDistance(diggertarget, local_9);
        if (local_7 < 3.0f) {
            SC_P_GetBySideGroupMember(1, 1, 2);
            rand();
            SC_P_Speech2(local_7, 945 + local_9 % 2, &local_);
            local_ = local_ + 0.10000000149011612f;
            SC_P_GetBySideGroupMember(1, 1, 2);
            SC_P_Ai_Go(local_7, &diggerstart);
            diggertarget = 2;
        }
        SC_P_GetBySideGroupMember(1, 1, 2);
        if (func_4180(&diggerstart, 3.0f)) {
            rand();
            diggertarget = local_7 % 2;
            SC_P_GetBySideGroupMember(1, 1, diggertarget);
            SC_P_GetPos(local_7, &local_2);
            SC_P_GetBySideGroupMember(1, 1, 2);
            SC_P_Ai_Go(local_7, &local_2);
        }
        vcdiggertimer = vcdiggertimer - retval;
        if (vcdiggertimer < 0) {
            frnd(20.0f);
            vcdiggertimer = 20.0f + local_7;
            local_ = 0;
            rand();
            SC_P_GetBySideGroupMember(1, 1, local_9 % 2);
            rand();
            SC_P_Speech2(local_6, 939 + tmp1 % 3, &local_);
            local_ = local_ + 0.10000000149011612f;
        }
        vc1digtimer = vc1digtimer - retval;
        if (vc1digtimer < 0) {
            frnd(5.0f);
            vc1digtimer = 5.0f + local_7;
            SC_P_GetBySideGroupMember(1, 1, 0);
            SC_P_GetPos(local_6, &local_2);
            SC_SND_PlaySound3D(10419, &local_2);
        }
        vc2digtimer = vc2digtimer - retval;
        if (vc2digtimer < 0) {
            frnd(5.0f);
            vc2digtimer = 5.0f + local_7;
            SC_P_GetBySideGroupMember(1, 1, 1);
            SC_P_GetPos(local_6, &local_2);
            SC_SND_PlaySound3D(10419, &local_2);
        }
        return &local_2;
    }
    SC_P_GetBySideGroupMember(1, 0, 1);
    SC_P_IsReady(local_6);
    if (!local_5) {
    } else {
        SC_P_GetBySideGroupMember(1, 0, 2);
        SC_P_IsReady(local_6);
        vcgroup1 = 1;
        SC_PC_Get();
        SC_P_GetWillTalk(local_6);
        local_ = local_5 + 0.5f;
        SC_PC_Get();
        SC_P_Speech2(local_5, 928, &local_);
        local_ = local_ + 0.10000000149011612f;
    }
    switch (vc1stat) {
    case 0:
        break;
    case 1:
        break;
    case 2:
        break;
    default:
    }
    switch (vc1stat) {
    case 0:
        break;
    case 1:
        break;
    case 2:
        break;
    default:
    }
    return;
}

int func_8919(void) {
    SC_SetObjectScript("grenadebedna", "levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\openablecrate.c");
    SC_SetObjectScript("n_poklop_01", "levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\poklop.c");
    SC_SetObjectScript("d_past_04_01", "levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\past.c");
    return FALSE;
}

int func_8932(void) {
    return FALSE;
}

int func_8933(void) {
    return FALSE;
}

int func_8934(void) {
    c_Vector3 local_;
    c_Vector3 tmp;

    SC_PC_Get();
    tmp = SC_P_GetWillTalk(local_);
    if (!crateuse) {
    } else {
        SC_NOD_GetName(t8954_0);
        SC_StringSame(local_, "grenadebedna");
        SC_PC_Get();
        SC_P_Speech2(local_1, 923, &tmp);
        tmp = tmp + 0.10000000149011612f;
        crateuse = 1;
        return &crateuse;
    }
    if (!doorsuse) {
    } else {
        SC_NOD_GetName(t8992_0);
        SC_StringSame(local_, "n_poklop_01");
        SC_PC_Get();
        SC_P_Speech2(local_1, 938, &tmp);
        tmp = tmp + 0.10000000149011612f;
        doorsuse = 1;
        return &doorsuse;
    }
    SC_NOD_GetName((*t9026_0));
    SC_StringSame(local_, "granat_v_plechovce2#3");
    if (!local_1) {
        SC_PC_Get();
        SC_P_Speech2(local_1, 925, &tmp);
        tmp = tmp + 0.10000000149011612f;
        return &tmp;
    } else {
        return "n_poklop_01";
    }
    return;
}

int ScriptMain(s_SC_L_info *info) {
    c_Vector3 local_;
    c_Vector3 local_9;
    c_Vector3 tmp;
    dword local_22[16];
    dword local_4[16];
    int initside;
    int tmp1;

    param_0->field_20 = 0.20000000298023224f;
    switch (gphase) {
    case 7:
        func_8919();
        break;
    case 11:
        func_8933();
        break;
    case 8:
        func_8932();
        break;
    case 4:
        break;
    case 0:
        SC_sgi(SGI_CURRENTMISSION, 9);
        SC_ZeroMem(&tmp, 8);
        SC_ZeroMem(&tmp1, 20);
        func_5197();
        SC_DeathCamera_Enable(0);
        SC_RadioSetDist(10.0f);
        SC_ZeroMem(&initside, 8);
        initside = 32;
        initside.field1 = 8;
        SC_InitSide(0, &initside);
        SC_ZeroMem(&initside, 8);
        initside = 64;
        initside.field1 = 16;
        SC_InitSide(1, &initside);
        SC_ZeroMem(&initside, 20);
        initside = 0;
        initside.field1 = 0;
        initside.field2 = 4;
        initside.field4 = 30.0f;
        SC_InitSideGroup(&initside);
        SC_ZeroMem(&initside, 20);
        initside = 1;
        initside.field1 = 0;
        initside.field2 = 9;
        SC_InitSideGroup(&initside);
        SC_ZeroMem(&initside, 20);
        initside = 1;
        initside.field1 = 1;
        initside.field2 = 16;
        SC_InitSideGroup(&initside);
        SC_ZeroMem(&initside, 20);
        initside = 1;
        initside.field1 = 2;
        initside.field2 = 16;
        SC_InitSideGroup(&initside);
        SC_ZeroMem(&initside, 20);
        initside = 1;
        initside.field1 = 3;
        initside.field2 = 9;
        SC_InitSideGroup(&initside);
        SC_Ai_SetShootOnHeardEnemyColTest(1);
        SC_Ai_SetGroupEnemyUpdate(1, 0, 0);
        SC_Ai_SetGroupEnemyUpdate(1, 1, 0);
        SC_Ai_SetGroupEnemyUpdate(1, 2, 0);
        SC_Ai_SetGroupEnemyUpdate(1, 3, 0);
        gphase = 1;
        SC_sgi(SGI_LEVELPHASE, 1);
        SC_Log(3, "Levelphase changed to %d", 1);
        SC_Osi("Levelphase changed to %d", 1);
        SC_SetCommandMenu(2009);
        param_0->field_20 = 0.5f;
        local_ = 1.0f;
        SC_AGS_Set(0);
        SC_PC_Get();
        SC_P_SpeechMes2(initside, 900, &local_, 1);
        local_ = local_ + 0.10000000149011612f;
        func_4948(901);
        func_4948(902);
        func_4948(1475);
        func_6873();
        gphase = 2;
        SC_sgi(SGI_LEVELPHASE, 2);
        SC_Log(3, "Levelphase changed to %d", 2);
        SC_Osi("Levelphase changed to %d", 2);
        SC_PC_GetPos(&local_9);
        func_7697(&local_9, info->elapsed_time);
        func_7807(&local_9, info->elapsed_time);
        break;
    case 1:
        SC_PC_Get();
        local_ = SC_P_GetWillTalk(initside);
        SC_PC_EnableMovement(0);
        SC_PC_EnableRadioBreak(1);
        SC_RadioBatch_Begin();
        SC_PC_Get();
        SC_P_Speech2(initside, 916, &local_);
        local_ = local_ + 0.10000000149011612f;
        func_0291(local_, 0.30000001192092896f);
        local_ = 0.30000001192092896f + local_23;
        SC_SpeechRadio2(917, &local_);
        func_0291(local_, 0.10000000149011612f, 0.20000000298023224f);
        local_ = 0.10000000149011612f + 0.20000000298023224f + local_24;
        SC_PC_Get();
        SC_P_Speech2(initside, 918, &local_);
        local_ = local_ + 0.10000000149011612f;
        func_0291(local_, 0.30000001192092896f);
        local_ = 0.30000001192092896f + local_23;
        SC_SpeechRadio2(919, &local_);
        func_0291(local_, 0.10000000149011612f, 0.20000000298023224f);
        local_ = 0.10000000149011612f + 0.20000000298023224f + local_24;
        SC_PC_Get();
        SC_P_SpeechMes2(initside, 920, &local_, 2);
        local_ = local_ + 0.10000000149011612f;
        SC_RadioBatch_End();
        SC_RadioBatch_Begin();
        SC_PC_Get();
        SC_P_Speech2(initside, 933, &local_);
        local_ = local_ + 0.10000000149011612f;
        func_0291(local_, 0.30000001192092896f);
        local_ = 0.30000001192092896f + local_23;
        SC_SpeechRadio2(934, &local_);
        func_0291(local_, 0.10000000149011612f, 0.20000000298023224f);
        local_ = 0.10000000149011612f + 0.20000000298023224f + local_24;
        SC_PC_Get();
        SC_P_Speech2(initside, 935, &local_);
        local_ = local_ + 0.10000000149011612f;
        func_0291(local_, 0.30000001192092896f);
        local_ = 0.30000001192092896f + local_23;
        SC_SpeechRadio2(936, &local_);
        func_0291(local_, 0.10000000149011612f, 0.20000000298023224f);
        local_ = 0.10000000149011612f + 0.20000000298023224f + local_24;
        SC_PC_Get();
        SC_P_SpeechMes2(initside, 937, &local_, 3);
        local_ = local_ + 0.10000000149011612f;
        SC_RadioBatch_End();
        break;
    default:
        if (save[info->param1]) {
        } else {
            save[info->param1] = 1;
            initside.field2 = 0;
            initside = 9110;
            initside.field1 = 9111;
            SC_MissionSave(&initside);
            SC_Log(3, "Saving game id %d", 9110);
            SC_Osi("Saving game id %d", 9110);
        }
        if (save[info->param1]) {
        } else {
            save[info->param1] = 1;
            SC_PC_EnableMovement(1);
            initside.field2 = 0;
            initside = 9112;
            initside.field1 = 9113;
            SC_MissionSave(&initside);
            SC_Log(3, "Saving game id %d", 9112);
            SC_Osi("Saving game id %d", 9112);
        }
        if (save[info->param1]) {
        } else {
            save[info->param1] = 1;
            SC_PC_EnableMovement(1);
            initside.field2 = 0;
            initside = 9114;
            initside.field1 = 9115;
            SC_MissionSave(&initside);
            SC_Log(3, "Saving game id %d", 9114);
            SC_Osi("Saving game id %d", 9114);
        }
        SC_Radio_Enable(1);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(initside, &local_9);
        SC_SND_PlaySound3D(2055, &local_9);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(initside, &local_9);
        SC_SND_PlaySound3D(2060, &local_9);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_GetPos(initside, &local_9);
        SC_SND_PlaySound3D(2070, &local_9);
        SC_GetWp("WayPoint53", &local_9);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(initside, &local_9);
        SC_GetWp("WayPoint#9", &local_9);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_SetPos(initside, &local_9);
        SC_GetWp("WayPoint57", &local_9);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(initside, &local_9);
        SC_Radio_Enable(2);
        func_1223();
        if (info->param1 >= 20) {
            param_0->field_12 = 0;
        } else {
            info->param2 = music[info->param1];
            param_0->field_12 = 1;
        }
        return TRUE;
    }
    if (!(local_21 == 51)) {
    }
    switch (gphase) {
    case 0:
        break;
    case 1:
        break;
    case 2:
        break;
    default:
    }
    switch (gphase) {
    case 1:
        break;
    case 2:
        break;
    default:
    }
    switch (gphase) {
    case 1:
        break;
    case 2:
        break;
    case 3:
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
    case 100:
        break;
    default:
    }
    if (!(local_20 == 15)) {
    }
    return;
}

