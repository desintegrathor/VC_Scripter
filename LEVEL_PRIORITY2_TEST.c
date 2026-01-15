// Structured decompilation of decompilation/TUNNELS01/SCRIPTS/LEVEL.scr
// Functions: 240

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

int func_0291(int param) {
    c_Vector3 tmp;
    int tmp1;
    int tmp2;

    tmp = frnd(param);
    if (!tmp1) {
        tmp = tmp2;
    } else {
        return tmp;
    }
    return;
}

int func_0313(int param) {
    int idx;  // Auto-generated

    SC_P_Ai_SetMode(idx, SCM_FEELDANGER);
    SC_P_Ai_EnableShooting(param_0, SCM_RUN);
    SC_P_Ai_EnableSituationUpdate(param_0, SCM_WARNABOUTENEMY);
    SC_Log(SCM_BOOBYTRAPFOUND, "Player %d enabled", param_0);
    return FALSE;
}

int func_0332(int param) {
    int idx;  // Auto-generated

    SC_P_Ai_SetMode(idx, SCM_ENABLE);
    SC_P_Ai_EnableShooting(param_0, gVar);
    SC_P_Ai_EnableSituationUpdate(param_0, 0);
    SC_P_Ai_Stop(param_0);
    SC_Log(3, "Player %d disabled", param_0);
    return FALSE;
}

int func_0354(int param, int param, int param) {
    int idx;  // Auto-generated

    if (!param_2) {
        SC_P_ScriptMessage(param_2, param, idx);
        return FALSE;
    } else {
        SC_Log(3, "Message %d %d to unexisted player!", param, param_0);
        return FALSE;
    }
    return;
}

int func_0365(int param, int param, int param) {
    int idx;  // Auto-generated

    SC_P_ScriptMessage(param_2, param, idx);
    return FALSE;
}

int func_0371(int param, int param) {
    int j;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    SC_P_GetBySideGroupMember(gVar1, param_2, param);
    SC_P_Ai_GetSureEnemies(j);
    if (!local_0) {
        return FALSE;
    } else {
        SC_P_GetBySideGroupMember(1, param_2, param);
        SC_P_Ai_GetDanger(local_1);
        return FALSE;
        return FALSE;
    }
    return;
}

int func_0388(int param, int param) {
    int j;  // Auto-generated

    int tmp;

    SC_P_GetBySideGroupMember(1, param_2, param);
    SC_P_Ai_GetDanger(j);
    if (!tmp) {
        return FALSE;
    } else {
        return FALSE;
    }
    return;
}

int func_0407(void) {
    return FALSE;
}

int func_0410(int param) {
    int local_0;  // Auto-generated

    SC_P_Ai_GetSureEnemies(param);
    if (!local_0) {
        return FALSE;
    } else {
        SC_P_Ai_GetDanger(param);
        return FALSE;
        return FALSE;
    }
    return;
}

int func_0420(int param) {
    int tmp;

    SC_P_Ai_GetDanger(param);
    if (!tmp) {
        return FALSE;
    } else {
        return FALSE;
    }
    return;
}

int func_0432(void) {
    return FALSE;
}

int func_0435(int param, int param) {
    int ai_props;  // Auto-generated
    int k;  // Auto-generated

    int tmp;

    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(param, &ai_props);
    *tmp = k;
    SC_P_Ai_SetProps(param, &ai_props);
    return &ai_props;
}

int func_0454(int param, int param) {
    int ai_props;  // Auto-generated
    int k;  // Auto-generated

    int tmp;

    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(param, &ai_props);
    *tmp = k;
    SC_P_Ai_SetProps(param, &ai_props);
    return &ai_props;
}

int func_0473(float time, int param) {
    int ai_props;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(time, &ai_props);
    *tmp3 = tmp2;
    SC_P_Ai_SetProps(time, &ai_props);
    return &ai_props;
}

int func_0496(float time, int param) {
    int ai_props;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(time, &ai_props);
    *tmp3 = tmp2;
    SC_P_Ai_SetProps(time, &ai_props);
    return &ai_props;
}

int func_0519(int param, int param) {
    int ai_props;  // Auto-generated

    int tmp;
    int tmp2;

    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(param, &ai_props);
    if (!param_0) {
        *tmp = 5.0f;
        SC_P_Ai_SetProps(param, &ai_props);
        return &ai_props;
    } else {
        *tmp2 = 1000.0f;
    }
    return;
}

int func_0546(int param, int param) {
    int ai_props;  // Auto-generated
    int k;  // Auto-generated

    int tmp;

    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(param, &ai_props);
    *tmp = k;
    SC_P_Ai_SetProps(param, &ai_props);
    return &ai_props;
}

int func_0565(void) {
    SC_ggi(SGI_CURRENTMISSION);
    return FALSE;
}

int func_0573(void) {
    SC_ggi(SGI_CHOPPER);
    return FALSE;
}

int func_0581(int param) {
    int player_info;  // Auto-generated

    int tmp;

    SC_P_GetInfo(param, &player_info);
    return tmp;
}

int func_0590(int param, int param) {
    int k;  // Auto-generated

    c_Vector3 props;

    SC_ZeroMem(&props, 128);
    SC_P_Ai_GetProps(param, &props);
    props = k;
    SC_P_Ai_SetProps(param, &props);
    return &props;
}

int func_0608(void) {
    dword param_0;  // Auto-generated

    int tmp;
    int tmp11;
    int tmp13;
    int tmp14;
    int tmp15;
    int tmp17;
    int tmp18;
    int tmp19;
    int tmp2;
    int tmp20;
    int tmp22;
    int tmp24;
    int tmp25;
    int tmp26;
    int tmp27;
    int tmp29;
    int tmp3;
    int tmp30;
    int tmp32;
    int tmp34;
    int tmp35;
    int tmp36;
    int tmp37;
    int tmp38;
    int tmp39;
    int tmp4;
    int tmp41;
    int tmp43;
    int tmp44;
    int tmp45;
    int tmp46;
    int tmp48;
    int tmp50;
    int tmp51;
    int tmp52;
    int tmp54;
    int tmp55;
    int tmp56;
    int tmp57;
    int tmp59;
    int tmp6;
    int tmp61;
    int tmp62;
    int tmp63;
    int tmp64;
    int tmp66;
    int tmp68;
    int tmp69;
    int tmp7;
    int tmp70;
    int tmp71;
    int tmp73;
    int tmp75;
    int tmp76;
    int tmp77;
    int tmp79;
    int tmp8;
    int tmp80;
    int tmp81;
    int tmp82;
    int tmp84;
    int tmp86;
    int tmp87;
    int tmp88;
    int tmp89;
    int tmp9;
    int tmp91;

    param_0->field_40 = SC_ggi(101);
    if (!tmp3) {
        param_0->field_40 = 0;
        param_0->field_44 = SC_ggi(102);
        param_0->field_44 = 7;
        param_0->field_44 = 0;
        param_0->field_48 = SC_ggi(103);
        SC_ggi(tmp34);
        param_0->field_48 = 23;
        SC_ggi(tmp35);
        param_0->field_48 = 25;
        param_0->field_48 = 1;
        param_0->field_48 = 0;
        param_0->field_52 = SC_ggi(104);
        param_0->field_52 = 0;
        param_0->field_56 = SC_ggi(105);
        param_0->field_56 = 59;
        param_0->field_56 = 0;
        param_0->field_60 = SC_ggi(106);
        param_0->field_60 = 0;
        param_0->field_64 = SC_ggi(107);
        param_0->field_64 = 0;
        param_0->field_68 = SC_ggi(108);
        param_0->field_68 = 63;
        param_0->field_68 = 0;
        param_0->field_72 = SC_ggi(109);
        param_0->field_72 = PLAYER_AMMOINGUN;
        param_0->field_76 = PLAYER_AMMOINPISTOL;
        return FALSE;
    } else {
        param_0->field_40 = 29;
    }
    return;
}

int func_0883(void) {
    int i;  // Auto-generated
    int local_40;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp14;
    int tmp15;
    int tmp16;
    int tmp17;
    int tmp18;
    int tmp19;
    int tmp2;
    int tmp20;
    int tmp21;
    int tmp22;
    int tmp23;
    int tmp24;
    int tmp25;
    int tmp26;
    int tmp27;
    int tmp28;
    int tmp29;
    int tmp3;
    int tmp30;
    int tmp31;
    int tmp32;
    int tmp33;
    int tmp34;
    int tmp35;
    int tmp36;
    int tmp37;
    int tmp38;
    int tmp39;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;

    SC_PC_Get();
    SC_P_GetWeapons(local_40, &i);
    if (!tmp1) {
        SC_sgi(101, tmp3);
        SC_sgi(102, tmp7);
        SC_sgi(102, 255);
        SC_sgi(103, tmp11);
        SC_sgi(103, 255);
        SC_sgi(PLAYER_WEAPON1, tmp15);
        SC_sgi(PLAYER_WEAPON2, PLAYER_WEAPON3);
        SC_sgi(PLAYER_WEAPON4, tmp19);
        SC_sgi(PLAYER_WEAPON5, PLAYER_WEAPON6);
        SC_sgi(PLAYER_WEAPON7, tmp23);
        SC_sgi(PLAYER_WEAPON8, PLAYER_WEAPON9);
        SC_sgi(PLAYER_WEAPON10, tmp27);
        SC_sgi(107, 255);
        SC_sgi(108, tmp31);
        SC_sgi(108, 255);
        SC_sgi(109, tmp35);
        SC_sgi(109, 255);
        SC_sgi(110, tmp39);
        SC_sgi(110, 255);
        return 39;
    } else {
        SC_sgi(101, 255);
    }
    return;
}Skipping orphaned block 139 at address 1356 in function func_1355 - no predecessors (unreachable code)
Skipping orphaned block 162 at address 1460 in function func_1442 - no predecessors (unreachable code)
Skipping orphaned block 167 at address 1476 in function func_1474 - no predecessors (unreachable code)
Skipping orphaned block 180 at address 1514 in function func_1512 - no predecessors (unreachable code)


int func_1046(void) {
    int i;  // Auto-generated

    SC_PC_Get();
    SC_P_ReadHealthFromGlobalVar(i, 95);
    return FALSE;
}

int func_1054(void) {
    int i;  // Auto-generated

    SC_PC_Get();
    SC_P_WriteHealthToGlobalVar(i, 95);
    return FALSE;
}

int func_1062(void) {
    int local_0;  // Auto-generated
    int local_2;  // Auto-generated
    int m;  // Auto-generated

    SC_PC_Get();
    SC_P_ReadAmmoFromGlobalVar(local_0, 60, 89);
    SC_ggi(90);
    if (!local_0) {
        SC_PC_Get();
        SC_ggi(90);
        SC_P_SetAmmoInWeap(2, 90, m);
    } else {
        SC_ggi(91);
        SC_PC_Get();
        SC_ggi(91);
        SC_P_SetAmmoInWeap(1, 91, local_2);
        return FALSE;
    }
    return;
}

int func_1111(void) {
    int i;  // Auto-generated
    int j;  // Auto-generated
    int local_1;  // Auto-generated
    int local_2;  // Auto-generated
    int m;  // Auto-generated

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

int func_1146(void) {
    int i;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;

    SC_PC_GetIntel(&i);
    tmp = 0;
    if (!tmp1) {
        SC_sgi(tmp2, tmp5);
        tmp = tmp6;
    }
    return 11;
}

int func_1180(void) {
    int local_0;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp6;

    tmp = 0;
    if (!tmp1) {
        local_0[tmp] = SC_ggi(tmp2);
        tmp = tmp6;
    }
    SC_PC_SetIntel(&local_0);
    return &local_0;
}

int func_1218(void) {
    func_0883();
    func_1111();
    func_1054();
    SC_MissionCompleted();
    return FALSE;
}

int func_1223(void) {
    func_1146();
    func_0883();
    func_1111();
    func_1054();
    SC_Osi("MISSION COMPLETE");
    SC_MissionDone();
    return FALSE;
}

int func_1233(void) {
    int idx;  // Auto-generated

    SC_ShowHelp(&idx, 1, 6.0f);
    return FALSE;
}

int func_1239(int param, int param) {
    int idx;  // Auto-generated
    dword local_0;  // Auto-generated

    int tmp;
    int tmp2;

    tmp = param;
    local_0.field1 = idx;
    SC_ShowHelp(&local_0, 2, 12.0f);
    return 12.0f;
}

int func_1258(int param, int param, int param) {
    dword i;  // Auto-generated
    int idx;  // Auto-generated
    dword local_0;  // Auto-generated

    int tmp;
    int tmp2;
    int tmp4;

    param_2 = tmp;
    i.field1 = param;
    local_0.field2 = idx;
    SC_ShowHelp(&local_0, 3, 24.0f);
    return 24.0f;
}

int func_1283(void) {
    SC_ggi(SGI_DIFFICULTY);
    return FALSE;
}

int func_1291(void) {
    c_Vector3 tmp1;
    int tmp;
    int tmp2;
    int tmp3;

    rand();
    tmp1 = tmp;
    SC_ggi(SGI_CURRENTMISSION);
    if (!tmp2) {
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
    return;
}

int func_1317(void) {
    int tmp;

    if (!tmp) {
        return 15;
    } else {
        return 26;
        return 2;
        return 19;
        return 6;
        return 23;
    }
    return;
}

int func_1324(void) {
    int tmp;

    if (!tmp) {
        return 26;
    } else {
        return 2;
        return 19;
        return 6;
        return 23;
    }
    return;
}

int func_1331(void) {
    int tmp;

    if (!tmp) {
        return 2;
    } else {
        return 19;
        return 6;
        return 23;
    }
    return;
}

int func_1338(void) {
    int tmp;

    if (!tmp) {
        return 19;
    } else {
        return 6;
        return 23;
    }
    return;
}

int func_1345(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 23;
    }
    return;
}

int func_1352(void) {
    return 23;
}

int func_1355(void) {
    int tmp;

    goto block_152; // @1401
    return 28;
}

int func_1363(void) {
    int tmp;

    if (!tmp) {
        return 15;
    } else {
        return 26;
        return 2;
        return 19;
        return 6;
        return 23;
    }
    return;
}

int func_1370(void) {
    int tmp;

    if (!tmp) {
        return 26;
    } else {
        return 2;
        return 19;
        return 6;
        return 23;
    }
    return;
}

int func_1377(void) {
    int tmp;

    if (!tmp) {
        return 2;
    } else {
        return 19;
        return 6;
        return 23;
    }
    return;
}

int func_1384(void) {
    int tmp;

    if (!tmp) {
        return 19;
    } else {
        return 6;
        return 23;
    }
    return;
}

int func_1391(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 23;
    }
    return;
}

int func_1398(void) {
    return 23;
}

int func_1401(void) {
    c_Vector3 tmp1;
    int tmp;
    int tmp2;

    rand();
    tmp1 = tmp;
    if (!tmp2) {
        return 14;
    } else {
        return 18;
        return 2;
        return 15;
        return 2;
    }
    return;
}

int func_1418(void) {
    int tmp;

    if (!tmp) {
        return 18;
    } else {
        return 2;
        return 15;
        return 2;
    }
    return;
}

int func_1425(void) {
    int tmp;

    if (!tmp) {
        return 2;
    } else {
        return 15;
        return 2;
    }
    return;
}

int func_1432(void) {
    int tmp;

    if (!tmp) {
        return 15;
    } else {
        return 2;
    }
    return;
}

int func_1439(void) {
    return 2;
}

int func_1442(void) {
    c_Vector3 tmp1;
    c_Vector3 tmp4;
    int tmp;
    int tmp2;
    int tmp3;
    int tmp5;

    rand();
    tmp1 = tmp;
    SC_ggi(tmp3);
    goto block_163; // @1464
    if (!tmp5) {
        return 19;
    } else {
        return 26;
    }
    return;
}

int func_1471(void) {
    c_Vector3 tmp1;
    int tmp;

    return 26;
}

int func_1474(void) {
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;

    goto block_168; // @1480
    switch (local_1) {
    case 3:
        break;
    case 4:
        break;
    case 5:
        if (tmp4) {
            return 26;
        } else {
            return 6;
        }
        break;
    default:
        if (local_0 > 14) {
            return 26;
        } else {
            if (local_0 > 10) {
                return 19;
            } else {
                if (local_0 > 5) {
                    return 6;
                } else {
                    return 23;
                }
            }
        }
    }
    return;
}

int func_1502(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 19;
    }
    return;
}

int func_1509(void) {
    return 19;
}

int func_1512(void) {
    int tmp;
    int tmp1;
    int tmp2;

    goto block_181; // @1518
    goto block_183; // @1523
    if (!tmp1) {
        return 26;
        return 19;
        return 6;
        return 23;
    } else {
        return 26;
        return 19;
        return 6;
        return 23;
        return 25;
        return 26;
        return 15;
        return 6;
        return 19;
        return 2;
        return 8;
        return 9;
        return 10;
        return 2;
        return 15;
        return 19;
        return 6;
        return 26;
        return 18;
        return 2;
        return 15;
        return 19;
        return 6;
        return 26;
        return 23;
        return 2;
        return 15;
        return 23;
        return 18;
        return 2;
        return 19;
        return 6;
        return 23;
        return 26;
        return 21;
        return 2;
        return 15;
        return 23;
        return 6;
        return 18;
        return 2;
        return 15;
        return 18;
        return 23;
        return 6;
        return 2;
        return 14;
        return 2;
        return 15;
        return 18;
        return 23;
        return 6;
        return 14;
        return 2;
    }
    return;
}Skipping orphaned block 191 at address 1549 in function func_1547 - no predecessors (unreachable code)
Skipping orphaned block 202 at address 1586 in function func_1584 - no predecessors (unreachable code)
Skipping orphaned block 217 at address 1633 in function func_1631 - no predecessors (unreachable code)
Skipping orphaned block 228 at address 1666 in function func_1664 - no predecessors (unreachable code)
Skipping orphaned block 241 at address 1710 in function func_1708 - no predecessors (unreachable code)
Skipping orphaned block 260 at address 1768 in function func_1767 - no predecessors (unreachable code)


int func_1530(void) {
    int tmp;

    if (!tmp) {
        return 19;
    } else {
        return 6;
        return 23;
    }
    return;
}

int func_1537(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 23;
    }
    return;
}

int func_1544(void) {
    return 23;
}

int func_1547(void) {
    int tmp;
    int tmp1;

    goto block_192; // @1553
    if (!tmp1) {
        return 26;
    } else {
        return 19;
        return 6;
        return 23;
        return 25;
    }
    return;
}

int func_1560(void) {
    int tmp;

    if (!tmp) {
        return 19;
    } else {
        return 6;
        return 23;
        return 25;
    }
    return;
}

int func_1567(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 23;
        return 25;
    }
    return;
}

int func_1574(void) {
    int tmp;

    if (!tmp) {
        return 23;
    } else {
        return 25;
    }
    return;
}

int func_1581(void) {
    return 25;
}

int func_1584(void) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    goto block_203; // @1590
    switch (local_1) {
    case 8:
        break;
    case 10:
        if (tmp3) {
            return 26;
        } else {
            if (i > 12) {
                return 15;
            } else {
                if (local_0 > 8) {
                    return 6;
                } else {
                    if (local_0 > 4) {
                        return 19;
                    } else {
                        return 2;
                    }
                }
            }
        }
        break;
    default:
        if (local_0 > 13) {
            return 8;
        } else {
            if (local_0 > 6) {
                return 9;
            } else {
                return 10;
            }
        }
    }
    return;
}

int func_1607(void) {
    int tmp;

    if (!tmp) {
        return 15;
    } else {
        return 6;
        return 19;
        return 2;
    }
    return;
}

int func_1614(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 19;
        return 2;
    }
    return;
}

int func_1621(void) {
    int tmp;

    if (!tmp) {
        return 19;
    } else {
        return 2;
    }
    return;
}

int func_1628(void) {
    return 2;
}

int func_1631(void) {
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    goto block_218; // @1637
    switch (local_1) {
    case 11:
        break;
    case 23:
        if (tmp3) {
            return 8;
        } else {
            return 9;
        }
        break;
    default:
        if (local_0 > 15) {
            return 2;
        } else {
            if (local_0 > 11) {
                return 15;
            } else {
                if (local_0 > 8) {
                    return 19;
                } else {
                    if (local_0 > 4) {
                        return 6;
                    } else {
                        if (local_0 > 1) {
                            return 26;
                        } else {
                            return 18;
                        }
                    }
                }
            }
        }
    }
    return;
}

int func_1654(void) {
    int tmp;

    if (!tmp) {
        return 9;
    } else {
        return 10;
    }
    return;
}

int func_1661(void) {
    return 10;
}

int func_1664(void) {
    int tmp;
    int tmp1;

    goto block_229; // @1670
    if (!tmp1) {
        return 2;
    } else {
        return 15;
        return 19;
        return 6;
        return 26;
        return 18;
    }
    return;
}

int func_1677(void) {
    int tmp;

    if (!tmp) {
        return 15;
    } else {
        return 19;
        return 6;
        return 26;
        return 18;
    }
    return;
}

int func_1684(void) {
    int tmp;

    if (!tmp) {
        return 19;
    } else {
        return 6;
        return 26;
        return 18;
    }
    return;
}

int func_1691(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 26;
        return 18;
    }
    return;
}

int func_1698(void) {
    int tmp;

    if (!tmp) {
        return 26;
    } else {
        return 18;
    }
    return;
}

int func_1705(void) {
    return 18;
}

int func_1708(void) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;

    goto block_242; // @1714
    switch (local_1) {
    case 14:
        break;
    case 15:
        break;
    case 18:
        if (tmp4) {
            return 2;
        } else {
            if (i > 11) {
                return 15;
            } else {
                if (local_0 > 8) {
                    return 19;
                } else {
                    if (local_0 > 5) {
                        return 6;
                    } else {
                        if (local_0 > 2) {
                            return 26;
                        } else {
                            return 23;
                        }
                    }
                }
            }
        }
        break;
    default:
        if (local_0 > 14) {
            return 2;
        } else {
            if (local_0 > 10) {
                return 15;
            } else {
                if (local_0 > 4) {
                    return 23;
                } else {
                    return 18;
                }
            }
        }
    }
    return;
}

int func_1736(void) {
    int tmp;

    if (!tmp) {
        return 15;
    } else {
        return 19;
        return 6;
        return 26;
        return 23;
    }
    return;
}

int func_1743(void) {
    int tmp;

    if (!tmp) {
        return 19;
    } else {
        return 6;
        return 26;
        return 23;
    }
    return;
}

int func_1750(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 26;
        return 23;
    }
    return;
}

int func_1757(void) {
    int tmp;

    if (!tmp) {
        return 26;
    } else {
        return 23;
    }
    return;
}

int func_1764(void) {
    return 23;
}

int func_1767(void) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;

    goto block_261; // @1772
    switch (local_1) {
    case 20:
        break;
    case 21:
        break;
    case 22:
        if (tmp4) {
            return 2;
        } else {
            if (i > 10) {
                return 15;
            } else {
                if (local_0 > 4) {
                    return 23;
                } else {
                    return 18;
                }
            }
        }
        break;
    default:
        if (local_0 > 15) {
            return 2;
        } else {
            if (local_0 > 11) {
                return 19;
            } else {
                if (local_0 > 8) {
                    return 6;
                } else {
                    if (local_0 > 4) {
                        return 23;
                    } else {
                        if (local_0 > 1) {
                            return 26;
                        } else {
                            return 21;
                        }
                    }
                }
            }
        }
    }
    return;
}

int func_1794(void) {
    int tmp;

    if (!tmp) {
        return 15;
    } else {
        return 23;
        return 18;
    }
    return;
}

Skipping orphaned block 275 at address 1813 in function func_1811 - no predecessors (unreachable code)
Skipping orphaned block 288 at address 1857 in function func_1855 - no predecessors (unreachable code)
Skipping orphaned block 303 at address 1905 in function func_1902 - no predecessors (unreachable code)
Skipping orphaned block 314 at address 1942 in function func_1940 - no predecessors (unreachable code)
Skipping orphaned block 319 at address 1958 in function func_1956 - no predecessors (unreachable code)
Skipping orphaned block 338 at address 2033 in function func_2015 - no predecessors (unreachable code)
Skipping orphaned block 351 at address 2071 in function func_2069 - no predecessors (unreachable code)
int func_1801(void) {
    int tmp;

    if (!tmp) {
        return 23;
    } else {
        return 18;
    }
    return;
}

int func_1808(void) {
    return 18;
}

int func_1811(void) {
    int tmp;
    int tmp1;

    goto block_276; // @1817
    if (!tmp1) {
        return 2;
    } else {
        return 19;
        return 6;
        return 23;
        return 26;
        return 21;
    }
    return;
}

int func_1824(void) {
    int tmp;

    if (!tmp) {
        return 19;
    } else {
        return 6;
        return 23;
        return 26;
        return 21;
    }
    return;
}

int func_1831(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 23;
        return 26;
        return 21;
    }
    return;
}

int func_1838(void) {
    int tmp;

    if (!tmp) {
        return 23;
    } else {
        return 26;
        return 21;
    }
    return;
}

int func_1845(void) {
    int tmp;

    if (!tmp) {
        return 26;
    } else {
        return 21;
    }
    return;
}

int func_1852(void) {
    return 21;
}

int func_1855(void) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    goto block_289; // @1861
    switch (local_1) {
    case 27:
        break;
    case 28:
        if (tmp3) {
            return 2;
        } else {
            if (i > 10) {
                return 15;
            } else {
                if (local_0 > 7) {
                    return 23;
                } else {
                    if (local_0 > 3) {
                        return 6;
                    } else {
                        return 18;
                    }
                }
            }
        }
        break;
    default:
        if (local_0 > 14) {
            return 2;
        } else {
            if (local_0 > 11) {
                return 15;
            } else {
                if (local_0 > 8) {
                    return 18;
                } else {
                    if (local_0 > 3) {
                        return 23;
                    } else {
                        return 6;
                    }
                }
            }
        }
    }
    return;
}

int func_1878(void) {
    int tmp;

    if (!tmp) {
        return 15;
    } else {
        return 23;
        return 6;
        return 18;
    }
    return;
}

int func_1885(void) {
    int tmp;

    if (!tmp) {
        return 23;
    } else {
        return 6;
        return 18;
    }
    return;
}

int func_1892(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 18;
    }
    return;
}

int func_1899(void) {
    return 18;
}

int func_1902(void) {
    int tmp;
    int tmp1;

    goto block_304; // @1909
    if (!tmp1) {
        return 2;
    } else {
        return 15;
        return 18;
        return 23;
        return 6;
    }
    return;
}

int func_1916(void) {
    int tmp;

    if (!tmp) {
        return 15;
    } else {
        return 18;
        return 23;
        return 6;
    }
    return;
}

int func_1923(void) {
    int tmp;

    if (!tmp) {
        return 18;
    } else {
        return 23;
        return 6;
    }
    return;
}

int func_1930(void) {
    int tmp;

    if (!tmp) {
        return 23;
    } else {
        return 6;
    }
    return;
}

int func_1937(void) {
    return 6;
}

int func_1940(void) {
    int tmp;
    int tmp1;

    goto block_315; // @1946
    if (!tmp1) {
        return 2;
    } else {
        return 14;
    }
    return;
}

int func_1953(void) {
    return 14;
}

int func_1956(void) {
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    goto block_322; // @1967
    if (!tmp1) {
    } else {
        return 2;
    }
    if (!tmp3) {
        return 2;
    } else {
        return 15;
        return 18;
        return 23;
        return 6;
        return 14;
    }
    return;
}

int func_1979(void) {
    int tmp;

    if (!tmp) {
        return 15;
    } else {
        return 18;
        return 23;
        return 6;
        return 14;
    }
    return;
}

int func_1986(void) {
    int tmp;

    if (!tmp) {
        return 18;
    } else {
        return 23;
        return 6;
        return 14;
    }
    return;
}

int func_1993(void) {
    int tmp;

    if (!tmp) {
        return 23;
    } else {
        return 6;
        return 14;
    }
    return;
}

int func_2000(void) {
    int tmp;

    if (!tmp) {
        return 6;
    } else {
        return 14;
    }
    return;
}

int func_2007(void) {
    return 14;
}

int func_2010(void) {
    goto block_336; // @2011
    return 2;
}

int func_2015(void) {
    dword default_aiviet;  // Auto-generated
    dword nvaofficer;  // Auto-generated
    dword nvasoldier2;  // Auto-generated
    dword nvasoldier3;  // Auto-generated
    dword poorvc;  // Auto-generated
    dword poorvc2;  // Auto-generated
    dword poorvc3;  // Auto-generated
    dword vcfighter2;  // Auto-generated
    dword vcfighter3;  // Auto-generated
    dword vcfighter4;  // Auto-generated
    dword vcuniform1;  // Auto-generated
    dword vcuniform2;  // Auto-generated
    dword vcuniform3;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp1;
    int tmp;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;

    rand();
    tmp1 = tmp;
    SC_ggi(tmp3);
    goto block_341; // @2042
    if (!tmp4) {
    } else {
        return "ini\\players\\poorvc.ini";
        return "ini\\players\\poorvc2.ini";
        return "ini\\players\\poorvc3.ini";
        return "ini\\players\\vcfighter2.ini";
        return "ini\\players\\vcfighter3.ini";
        return "ini\\players\\vcfighter4.ini";
        return "ini\\players\\vcfighter3.ini";
        return "ini\\players\\vcfighter2.ini";
        return "ini\\players\\vcfighter3.ini";
        return "ini\\players\\vcfighter4.ini";
        return "ini\\players\\vcuniform1.ini";
        return "ini\\players\\vcuniform2.ini";
        return "ini\\players\\vcuniform3.ini";
        return "ini\\players\\nvasoldier2.ini";
        return "ini\\players\\nvasoldier3.ini";
        return "ini\\players\\nvaofficer.ini";
        return "ini\\players\\default_aiviet.ini";
    }
    return;
}

int func_2059(void) {
    dword poorvc2;  // Auto-generated
    dword poorvc3;  // Auto-generated

    c_Vector3 tmp1;
    int tmp;
    int tmp2;

    if (!tmp2) {
        return "ini\\players\\poorvc2.ini";
    } else {
        return "ini\\players\\poorvc3.ini";
    }
    return;
}

int func_2066(void) {
    dword poorvc3;  // Auto-generated

    c_Vector3 tmp1;
    int tmp;

    return "ini\\players\\poorvc3.ini";
}

int func_2069(void) {
    dword default_aiviet;  // Auto-generated
    dword nvaofficer;  // Auto-generated
    dword nvasoldier2;  // Auto-generated
    dword nvasoldier3;  // Auto-generated
    dword vcfighter2;  // Auto-generated
    dword vcfighter3;  // Auto-generated
    dword vcfighter4;  // Auto-generated
    dword vcuniform1;  // Auto-generated
    dword vcuniform2;  // Auto-generated
    dword vcuniform3;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;

    goto block_354; // @2080
    if (!tmp1) {
    } else {
        return "ini\\players\\vcfighter2.ini";
        return "ini\\players\\vcfighter3.ini";
        return "ini\\players\\vcfighter4.ini";
        return "ini\\players\\vcfighter3.ini";
        return "ini\\players\\vcfighter2.ini";
        return "ini\\players\\vcfighter3.ini";
        return "ini\\players\\vcfighter4.ini";
        return "ini\\players\\vcuniform1.ini";
        return "ini\\players\\vcuniform2.ini";
        return "ini\\players\\vcuniform3.ini";
        return "ini\\players\\nvasoldier2.ini";
        return "ini\\players\\nvasoldier3.ini";
        return "ini\\players\\nvaofficer.ini";
        return "ini\\players\\default_aiviet.ini";
    }
    return;
}Skipping orphaned block 370 at address 2124 in function func_2122 - no predecessors (unreachable code)
Skipping orphaned block 391 at address 2184 in function func_2182 - no predecessors (unreachable code)
Skipping orphaned block 410 at address 2237 in function func_2235 - no predecessors (unreachable code)
Skipping orphaned block 434 at address 2337 in function func_2293 - no predecessors (unreachable code)


int func_2112(void) {
    dword vcfighter3;  // Auto-generated
    dword vcfighter4;  // Auto-generated

    int tmp;

    if (!tmp) {
        return "ini\\players\\vcfighter3.ini";
    } else {
        return "ini\\players\\vcfighter4.ini";
    }
    return;
}

int func_2119(void) {
    dword vcfighter4;  // Auto-generated

    return "ini\\players\\vcfighter4.ini";
}

int func_2122(void) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated
    dword vcfighter2;  // Auto-generated
    dword vcfighter3;  // Auto-generated
    dword vcfighter4;  // Auto-generated
    dword vcuniform1;  // Auto-generated
    dword vcuniform2;  // Auto-generated
    dword vcuniform3;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;

    goto block_371; // @2128
    switch (local_1) {
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
        if (tmp7) {
            return "ini\\players\\vcfighter3.ini";
        } else {
            if (i > 10) {
                return "ini\\players\\vcfighter2.ini";
            } else {
                if (local_0 > 5) {
                    return "ini\\players\\vcfighter3.ini";
                } else {
                    return "ini\\players\\vcfighter4.ini";
                }
            }
        }
        break;
    default:
        if (local_0 > 13) {
            return "ini\\players\\vcuniform1.ini";
        } else {
            if (local_0 > 6) {
                return "ini\\players\\vcuniform2.ini";
            } else {
                return "ini\\players\\vcuniform3.ini";
            }
        }
    }
    return;
}

int func_2165(void) {
    dword vcfighter2;  // Auto-generated
    dword vcfighter3;  // Auto-generated
    dword vcfighter4;  // Auto-generated

    int tmp;

    if (!tmp) {
        return "ini\\players\\vcfighter2.ini";
    } else {
        return "ini\\players\\vcfighter3.ini";
        return "ini\\players\\vcfighter4.ini";
    }
    return;
}

int func_2172(void) {
    dword vcfighter3;  // Auto-generated
    dword vcfighter4;  // Auto-generated

    int tmp;

    if (!tmp) {
        return "ini\\players\\vcfighter3.ini";
    } else {
        return "ini\\players\\vcfighter4.ini";
    }
    return;
}

int func_2179(void) {
    dword vcfighter4;  // Auto-generated

    return "ini\\players\\vcfighter4.ini";
}

int func_2182(void) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated
    dword nvaofficer;  // Auto-generated
    dword nvasoldier2;  // Auto-generated
    dword nvasoldier3;  // Auto-generated
    dword vcuniform1;  // Auto-generated
    dword vcuniform2;  // Auto-generated
    dword vcuniform3;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;

    goto block_392; // @2188
    switch (local_1) {
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
        if (tmp7) {
            return "ini\\players\\vcuniform1.ini";
        } else {
            if (i > 6) {
                return "ini\\players\\vcuniform2.ini";
            } else {
                return "ini\\players\\vcuniform3.ini";
            }
        }
        break;
    default:
        if (local_0 > 12) {
            return "ini\\players\\nvasoldier2.ini";
        } else {
            if (local_0 > 4) {
                return "ini\\players\\nvasoldier3.ini";
            } else {
                return "ini\\players\\nvaofficer.ini";
            }
        }
    }
    return;
}

int func_2225(void) {
    dword vcuniform2;  // Auto-generated
    dword vcuniform3;  // Auto-generated

    int tmp;

    if (!tmp) {
        return "ini\\players\\vcuniform2.ini";
    } else {
        return "ini\\players\\vcuniform3.ini";
    }
    return;
}

int func_2232(void) {
    dword vcuniform3;  // Auto-generated

    return "ini\\players\\vcuniform3.ini";
}

int func_2235(void) {
    dword default_aiviet;  // Auto-generated
    dword nvaofficer;  // Auto-generated
    dword nvasoldier2;  // Auto-generated
    dword nvasoldier3;  // Auto-generated

    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;

    goto block_413; // @2246
    if (!tmp1) {
    } else {
        return "ini\\players\\nvasoldier2.ini";
        return "ini\\players\\nvasoldier3.ini";
        return "ini\\players\\nvaofficer.ini";
        return "ini\\players\\default_aiviet.ini";
    }
    return;
}

int func_2278(void) {
    dword nvaofficer;  // Auto-generated
    dword nvasoldier3;  // Auto-generated

    int tmp;

    if (!tmp) {
        return "ini\\players\\nvasoldier3.ini";
    } else {
        return "ini\\players\\nvaofficer.ini";
    }
    return;
}

int func_2285(void) {
    dword nvaofficer;  // Auto-generated

    return "ini\\players\\nvaofficer.ini";
}

int func_2288(void) {
    dword default_aiviet;  // Auto-generated

    goto block_429; // @2289
    return "ini\\players\\default_aiviet.ini";
}

int func_2293(void) {
    c_Vector3 local_;
    c_Vector3 local_1;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp100;
    int tmp101;
    int tmp103;
    int tmp104;
    int tmp106;
    int tmp107;
    int tmp108;
    int tmp11;
    int tmp110;
    int tmp111;
    int tmp113;
    int tmp114;
    int tmp116;
    int tmp117;
    int tmp119;
    int tmp12;
    int tmp120;
    int tmp121;
    int tmp122;
    int tmp124;
    int tmp125;
    int tmp127;
    int tmp128;
    int tmp13;
    int tmp130;
    int tmp131;
    int tmp133;
    int tmp134;
    int tmp136;
    int tmp137;
    int tmp138;
    int tmp140;
    int tmp141;
    int tmp143;
    int tmp144;
    int tmp145;
    int tmp146;
    int tmp147;
    int tmp149;
    int tmp15;
    int tmp150;
    int tmp152;
    int tmp153;
    int tmp155;
    int tmp156;
    int tmp158;
    int tmp159;
    int tmp16;
    int tmp160;
    int tmp162;
    int tmp163;
    int tmp165;
    int tmp166;
    int tmp168;
    int tmp169;
    int tmp170;
    int tmp172;
    int tmp173;
    int tmp175;
    int tmp176;
    int tmp178;
    int tmp179;
    int tmp18;
    int tmp181;
    int tmp182;
    int tmp183;
    int tmp184;
    int tmp185;
    int tmp187;
    int tmp188;
    int tmp19;
    int tmp190;
    int tmp191;
    int tmp193;
    int tmp194;
    int tmp196;
    int tmp197;
    int tmp199;
    int tmp2;
    int tmp20;
    int tmp200;
    int tmp202;
    int tmp203;
    int tmp205;
    int tmp206;
    int tmp208;
    int tmp209;
    int tmp21;
    int tmp22;
    int tmp23;
    int tmp25;
    int tmp26;
    int tmp28;
    int tmp29;
    int tmp3;
    int tmp30;
    int tmp31;
    int tmp33;
    int tmp34;
    int tmp36;
    int tmp37;
    int tmp39;
    int tmp40;
    int tmp41;
    int tmp43;
    int tmp44;
    int tmp46;
    int tmp47;
    int tmp49;
    int tmp5;
    int tmp50;
    int tmp51;
    int tmp52;
    int tmp54;
    int tmp55;
    int tmp57;
    int tmp58;
    int tmp6;
    int tmp60;
    int tmp61;
    int tmp62;
    int tmp63;
    int tmp64;
    int tmp66;
    int tmp67;
    int tmp69;
    int tmp7;
    int tmp70;
    int tmp71;
    int tmp73;
    int tmp74;
    int tmp76;
    int tmp77;
    int tmp79;
    int tmp80;
    int tmp82;
    int tmp83;
    int tmp85;
    int tmp86;
    int tmp87;
    int tmp88;
    int tmp89;
    int tmp9;
    int tmp91;
    int tmp92;
    int tmp94;
    int tmp95;
    int tmp96;
    int tmp97;
    int tmp98;

    local_ = 0;
    if (!tmp) {
        tmp1[local_] = 0;
        tmp5[local_] = 0;
        local_ = tmp9;
    }
    SC_ggi(tmp11);
    tmp13 = 24;
    tmp16 = 38;
    goto block_437; // @2361
    if (!tmp18) {
    } else {
        tmp23 = 23;
        tmp26 = 25;
        tmp31 = 23;
        tmp34 = 26;
        tmp37 = 24;
        tmp41 = 24;
        tmp44 = 26;
        tmp47 = 38;
        tmp52 = 23;
        tmp55 = 24;
        tmp58 = 25;
        tmp64 = 23;
        tmp67 = 25;
        tmp71 = 23;
        tmp74 = 24;
        tmp77 = 25;
        tmp80 = 37;
        tmp83 = 38;
        tmp89 = 23;
        tmp92 = 25;
        tmp98 = 27;
        tmp101 = 28;
        tmp104 = 31;
        tmp108 = 27;
        tmp111 = 28;
        tmp114 = 31;
        tmp117 = 35;
        tmp122 = 35;
        tmp125 = 27;
        tmp128 = 32;
        tmp131 = 33;
        tmp134 = 34;
        tmp138 = 23;
        tmp141 = 25;
        tmp147 = 26;
        tmp150 = 27;
        tmp153 = 28;
        tmp156 = 31;
        tmp160 = 31;
        tmp163 = 35;
        tmp166 = 36;
        tmp170 = 35;
        tmp173 = 32;
        tmp176 = 33;
        tmp179 = 34;
        tmp185 = 33;
        tmp188 = 34;
        tmp191 = 35;
        tmp194 = 36;
        tmp197 = 35;
        tmp200 = 27;
        tmp203 = 32;
        tmp206 = 33;
        tmp209 = 34;
        return local_1;
    }
    return;
}Skipping orphaned block 518 at address 3059 in function func_3043 - no predecessors (unreachable code)
Skipping orphaned block 523 at address 3090 in function func_3081 - no predecessors (unreachable code)
Skipping orphaned block 525 at address 3109 in function func_3093 - no predecessors (unreachable code)
Skipping orphaned block 532 at address 3155 in function func_3146 - no predecessors (unreachable code)
Skipping orphaned block 534 at address 3177 in function func_3158 - no predecessors (unreachable code)
Skipping orphaned block 541 at address 3235 in function func_3226 - no predecessors (unreachable code)
Skipping orphaned block 543 at address 3247 in function func_3238 - no predecessors (unreachable code)
Skipping orphaned block 550 at address 3305 in function func_3296 - no predecessors (unreachable code)


int func_2910(int param) {
    int local_128;  // Auto-generated
    int local_134;  // Auto-generated
    int local_135;  // Auto-generated
    int local_136;  // Auto-generated
    int local_138;  // Auto-generated

    int tmp;

    tmp = 100.0f;
    SC_ggi(SGI_GAMETYPE);
    if (!local_138) {
        SC_P_GetPos(param_2, &vec);
        SC_MP_EnumPlayers(&enum_pl, &local_134, 0);
        return FALSE;
        local_135 = 0;
    } else {
        SC_PC_GetPos(param);
        local_136 = SC_2VectorsDist(&local_128, &vec);
        return TRUE;
        return FALSE;
    }
    return;
}

int func_2947(int param) {
    c_Vector3 local_;
    c_Vector3 tmp1;
    int local_137;
    int side;
    int side2;
    int side3;
    int side4;
    int sideB;
    int tmp;
    int tmp10;
    int tmp11;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    s_sphere tmp9;

    tmp = 0;
    if (!tmp2) {
        SC_P_GetPos(tmp5, &local_);
        local_137 = SC_2VectorsDist(&local_, &tmp1);
        tmp7 = local_137;
        tmp9 = tmp8;
        tmp = tmp10;
    }
    if (!tmp11) {
        return TRUE;
    } else {
        return FALSE;
    }
    return;
}

int func_3013(void) {
    c_Vector3 tmp;
    c_Vector3 tmp1;

    return FALSE;
}

int func_3016(int param) {
    int local_128;  // Auto-generated
    int local_131;  // Auto-generated

    int tmp;
    int tmp1;

    SC_PC_GetPos(param);
    tmp = SC_2VectorsDist(&local_128, &local_131);
    if (!tmp1) {
        return TRUE;
    } else {
        return FALSE;
    }
    return;
}

int func_3040(void) {
    return FALSE;
}

int func_3043(int param, int param) {
    int local_0;  // Auto-generated
    int local_2;  // Auto-generated
    int local_3;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp;
    int tmp1;

    tmp = SC_GetGroupPlayers(param_2, param);
    local_ = 0;
    SC_P_GetBySideGroupMember(param_2, param, local_);
    SC_P_IsReady(local_3);
    if (!local_2) {
        return FALSE;
    } else {
        SC_P_GetBySideGroupMember(param_2, param, local_);
        SC_P_IsReady(local_3);
        local_0++;
        return TRUE;
    }
    return;
}

int func_3081(void) {
    c_Vector3 tmp1;
    int tmp;

    tmp1 = tmp;
    goto block_518; // @3059
    return;
}

int func_3093(int param, int param) {
    int local_0;  // Auto-generated
    int local_2;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp;
    c_Vector3 tmp1;
    int param_;
    int tmp2;
    s_sphere param_1;

    tmp = SC_GetGroupPlayers(param_, param_1);
    local_ = 0;
    SC_P_GetBySideGroupMember(param_, param_1, local_);
    SC_P_IsReady(tmp1);
    if (!local_2) {
        SC_P_GetBySideGroupMember(param_, param_1, local_);
        SC_P_GetActive(tmp1);
        return FALSE;
    } else {
        local_0++;
    }
    return;
}

int func_3146(void) {
    c_Vector3 tmp2;
    c_Vector3 tmp4;
    int tmp;
    int tmp5;
    s_sphere tmp1;

    tmp2 = tmp5;
    goto block_525; // @3109
    return;
}

int func_3158(int param) {
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp;
    c_Vector3 tmp2;
    int local_4;
    int tmp1;
    int tmp3;

    tmp = SC_GetGroupPlayers(1, param);
    local_ = 0;
    local_4 = SC_P_GetBySideGroupMember(1, param, local_);
    if (!local_4) {
        tmp2 = SC_P_Ai_GetDanger(local_4);
        return TRUE;
        local_1 = SC_P_Ai_GetSureEnemies(local_4);
        return TRUE;
    } else {
        local_0++;
    }
    return;
}

int func_3210(void) {
    int i;  // Auto-generated
    int k;  // Auto-generated
    int local_0;  // Auto-generated
    int local_3;  // Auto-generated
    int local_4;  // Auto-generated

    c_Vector3 tmp1;
    int tmp;
    int tmp2;

    tmp1 = SC_P_Ai_GetSureEnemies(tmp);
    if (!tmp2) {
        return TRUE;
    } else {
        local_4 = SC_P_GetBySideGroupMember(1, k, i);
        local_3 = SC_P_Ai_GetDanger(local_4);
        return TRUE;
        tmp1 = SC_P_Ai_GetSureEnemies(tmp);
        local_0++;
        return FALSE;
    }
    return;
}

int func_3226(void) {
    c_Vector3 tmp2;
    int tmp;
    int tmp1;

    tmp2 = tmp1;
    goto block_534; // @3177
    return;
}

int func_3238(void) {
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp1;
    int local_4;
    int tmp;
    int tmp2;

    local_ = 1;
    local_4 = SC_P_GetBySideGroupMember(0, 0, local_);
    if (!local_4) {
        tmp1 = SC_P_Ai_GetDanger(local_4);
        return TRUE;
        local_1 = SC_P_Ai_GetSureEnemies(local_4);
        return TRUE;
    } else {
        local_0++;
    }
    return;
}

int func_3280(void) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated
    int local_3;  // Auto-generated
    int local_4;  // Auto-generated

    c_Vector3 tmp1;
    int tmp;
    int tmp2;

    tmp1 = SC_P_Ai_GetSureEnemies(tmp);
    if (!tmp2) {
        return TRUE;
    } else {
        local_4 = SC_P_GetBySideGroupMember(0, 0, i);
        local_3 = SC_P_Ai_GetDanger(local_4);
        return TRUE;
        tmp1 = SC_P_Ai_GetSureEnemies(tmp);
        local_0++;
        return FALSE;
    }
    return;
}

int func_3296(void) {
    c_Vector3 tmp2;
    int tmp;
    int tmp1;

    tmp2 = tmp1;
    goto block_543; // @3247
    return;
}

int func_3308(int param) {
    c_Vector3 local_;
    c_Vector3 local_5;
    c_Vector3 tmp;
    c_Vector3 tmp1;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    s_sphere tmp2;

    tmp = 0;
    if (!tmp3) {
        local_ = SC_P_GetBySideGroupMember(0, 0, tmp);
        SC_P_GetPos(local_, &tmp1);
        local_5 = SC_2VectorsDist(tmp2, &tmp1);
        tmp5 = local_5;
        tmp = tmp6;
    }
    return tmp5;
}

int func_3368(int param, int param) {
    int idx;  // Auto-generated

    c_Vector3 local_;
    int tmp;

    local_ = SC_NOD_Get(0, param);
    if (!tmp) {
        SC_NOD_GetWorldPos(local_, idx);
    } else {
        return TRUE;
    }
    return;
}

int func_3388(int param) {
    int j;  // Auto-generated

    c_Vector3 local_;
    int tmp;

    local_ = SC_NOD_Get(0, param);
    if (!tmp) {
        SC_NOD_GetWorldRotZ(local_);
        return j;
    } else {
        return FALSE;
    }
    return;
}

int func_3411(void) {
    return FALSE;
}

int func_3414(void) {
    int j;  // Auto-generated
    int local_0;  // Auto-generated

    int tmp;

    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_GetPeaceMode(j);
    if (!tmp) {
        SC_P_GetBySideGroupMember(0, 0, 1);
        SC_P_Ai_SetPeaceMode(local_0, 0);
    } else {
        SC_P_GetBySideGroupMember(0, 0, 1);
        SC_P_Ai_Stop(local_0);
        return FALSE;
    }
    return;
}

int func_3452(int param, int param) {
    int i;  // Auto-generated
    int idx;  // Auto-generated
    int local_0;  // Auto-generated

    func_3368(param, &i);
    SC_DoExplosion(&local_0, idx);
    return param_0;
}

int func_3462(int param) {
    int idx;  // Auto-generated
    int j;  // Auto-generated
    float local_0;  // Auto-generated
    int local_1;  // Auto-generated
    int local_10;  // Auto-generated
    dword local_4;  // Auto-generated
    int local_7;  // Auto-generated
    int m;  // Auto-generated

    int tmp;

    tmp = SC_NOD_Get(0, idx);
    if (!tmp) {
        SC_NOD_GetWorldPos(local_7, &j);
        local_0 = SC_NOD_GetWorldRotZ(local_7);
        local_0 = local_0 - 1.5700000524520874f;
        local_4 = local_1;
        cos(local_0);
        local_4 = 2.0f - local_0 * m;
        sin(local_0);
        local_4.field1 = 2.0f + local_0 * local_10;
        SC_DoExplosion(&local_4, 1);
        local_4 = local_1;
        cos(local_0);
        local_4 = 4.0f - local_0 * local_10;
        sin(local_0);
        local_4.field1 = 4.0f + local_0 * local_10;
        SC_DoExplosion(&local_4, 2);
        local_4 = local_1;
        cos(local_0);
        local_4 = 8.0f - local_0 * local_10;
        sin(local_0);
        local_4.field1 = 8.0f + local_0 * local_10;
        SC_DoExplosion(&local_4, 3);
        SC_DUMMY_Set_DoNotRenHier2(local_7, 1);
        return TRUE;
    } else {
        SC_message("FATAL! Claymore %s not found!!!!!!");
        return TRUE;
    }
    return;
}

int func_3484(void) {
    int local_7;  // Auto-generated

    c_Vector3 local_;
    int local_4;
    int tmp;
    int tmp1;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp14;
    int tmp15;
    int tmp16;
    int tmp17;
    int tmp18;
    int tmp19;
    int tmp2;
    int tmp21;
    int tmp22;
    int tmp23;
    int tmp24;
    int tmp25;
    int tmp26;
    int tmp27;
    int tmp28;
    int tmp29;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;

    SC_NOD_GetWorldPos(local_7, &vec);
    local_ = SC_NOD_GetWorldRotZ(local_7);
    local_ = tmp;
    local_4 = tmp1;
    cos(local_);
    local_4 = tmp4;
    sin(local_);
    *tmp9 = tmp8;
    SC_DoExplosion(&local_4, 1);
    local_4 = tmp11;
    cos(local_);
    local_4 = tmp14;
    sin(local_);
    *tmp19 = tmp18;
    SC_DoExplosion(&local_4, 2);
    local_4 = tmp21;
    cos(local_);
    local_4 = tmp24;
    sin(local_);
    *tmp29 = tmp28;
    SC_DoExplosion(&local_4, 3);
    SC_DUMMY_Set_DoNotRenHier2(local_7, 1);
    return TRUE;
}

int func_3625(int param, int param, int param, int param) {
    float idx;  // Auto-generated
    int local_4;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp;
    int side;
    int side2;
    int sideB;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp9;

    func_3368(param_3, &local_4);
    *side2 = sideB;
    tmp = 0;
    if (!tmp1) {
        frnd(idx);
        local_ = tmp3;
        frnd(param_0);
        *tmp7 = tmp6;
        SC_DoExplosion(&local_, param_2);
        tmp = tmp9;
    }
    return 7;
}

int func_3687(int param, int param) {
    int i;  // Auto-generated
    int idx;  // Auto-generated
    int local_0;  // Auto-generated

    SC_GetWp(param, &i);
    SC_DoExplosion(&local_0, idx);
    return param_0;
}

int func_3701(int param) {
    int i;  // Auto-generated
    int idx;  // Auto-generated
    int local_0;  // Auto-generated

    SC_GetWp(idx, &i);
    SC_CreatePtc(176, &local_0);
    return &local_0;
}

int func_3715(int param) {
    int idx;  // Auto-generated
    int local_5;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp9;

    SC_GetWp(idx, &local_);
    SC_DoExplosion(&local_, 3);
    SC_SND_PlaySound3D(2965, &local_);
    SC_NOD_Get(0, param_0);
    SC_CreatePtc_Ext(param_0, local_5, 1000.0f, 0.0f, 1.0f, 1.0f);
    SC_NOD_Get(0, param_0);
    SC_CreatePtc_Ext(param_0, local_5, 1000.0f, 0.0f, 1.0f, 1.0f);
    tmp = 0;
    if (!tmp1) {
        SC_GetWp(param_0, &local_);
        frnd(5.0f);
        local_ = tmp3;
        frnd(5.0f);
        *tmp7 = tmp6;
        SC_CreatePtcVec_Ext(177, &local_, 1000.0f, 0.0f, 1.0f, 1.0f);
        tmp = tmp9;
    }
    return 4;
}

int func_3821(int param) {
    int idx;  // Auto-generated

    SC_CreatePtc(198, idx);
    SC_SND_PlaySound3D(2965, param_0);
    SC_CreatePtcVec_Ext(176, param_0, 1000.0f, 0.0f, 1.0f, 1.0f);
    SC_CreatePtcVec_Ext(177, param_0, 5.0f, 0.0f, 1.0f, 1.0f);
    return 1.0f;
}

int func_3847(int param, int param, int param) {
    float idx;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp4;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp14;
    int tmp2;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;

    *tmp2 = tmp1;
    tmp4 = 0;
    if (!tmp5) {
        frnd(idx);
        local_ = tmp8;
        frnd(param_0);
        *tmp12 = tmp11;
        SC_CreatePtc(198, &local_);
        SC_CreatePtcVec_Ext(177, &local_, 5.0f, 0.0f, 1.0f, 1.0f);
        tmp4 = tmp14;
    }
    SC_CreatePtcVec_Ext(176, param_2, 1000.0f, 0.0f, 1.0f, 1.0f);
    return 1.0f;
}

int func_3921(int param, int param, int param) {
    float idx;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp4;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp14;
    int tmp2;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;

    *tmp2 = tmp1;
    tmp4 = 0;
    if (!tmp5) {
        frnd(idx);
        local_ = tmp8;
        frnd(param_0);
        *tmp12 = tmp11;
        SC_CreatePtc(198, &local_);
        tmp4 = tmp14;
    }
    SC_CreatePtcVec_Ext(176, param_2, 1000.0f, 0.0f, 1.0f, 1.0f);
    return 1.0f;
}

int func_3987(int param, int param) {
    float idx;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp4;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp14;
    int tmp2;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;

    *tmp2 = tmp1;
    tmp4 = 0;
    if (!tmp5) {
        frnd(idx);
        local_ = tmp8;
        frnd(param_0);
        *tmp12 = tmp11;
        SC_CreatePtc(198, &local_);
        tmp4 = tmp14;
    }
    return 4;
}

int func_4045(int param) {
    int ai_props;  // Auto-generated
    int idx;  // Auto-generated

    c_Vector3 battleprops;
    int tmp;
    int tmp2;
    int tmp4;
    int tmp6;

    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(idx, &ai_props);
    *tmp = 1;
    *tmp2 = 4.0f;
    SC_P_Ai_SetProps(param_0, &ai_props);
    *tmp4 = 0.8999999761581421f;
    battleprops = 0.30000001192092896f;
    *tmp6 = 0.5f;
    SC_P_Ai_SetBattleProps(param_0, &battleprops);
    return &battleprops;
}

int func_4088(int param) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated

    c_Vector3 tmp;
    int tmp1;

    SC_P_GetDir(param, &i);
    tmp = SC_VectorLen(&local_0);
    if (!tmp1) {
        return TRUE;
    } else {
        return FALSE;
    }
    return;
}

int func_4110(void) {
    return FALSE;
}

int func_4113(int param) {
    int local_7;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 local_2;
    c_Vector3 local_6;
    c_Vector3 tmp2;
    c_Vector3 tmp6;
    int tmp;
    int tmp1;
    int tmp4;
    int tmp5;
    int tmp7;
    s_sphere tmp3;

    local_ = 0;
    if (!tmp4) {
        SC_P_GetBySideGroupMember(0, 0, local_);
        SC_P_IsReady(local_7);
        SC_P_GetBySideGroupMember(tmp, tmp1, local_);
        SC_P_GetPos(local_6, &tmp2);
        local_2 = SC_2VectorsDist(&tmp2, tmp3);
        tmp6 = local_2;
        local_ = tmp7;
    }
    return tmp6;
}

int func_4180(int param, int param, int param) {
    int local_3;  // Auto-generated

    SC_P_GetPos(param_3, &vec);
    SC_IsNear3D(&vec, param_2, param);
    return local_3;
}

int func_4195(int param, int param) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated
    int local_3;  // Auto-generated

    SC_PC_GetPos(&i);
    SC_IsNear3D(&local_0, param_2, param);
    return local_3;
}

int func_4213(int param) {
    int i;  // Auto-generated
    int idx;  // Auto-generated
    dword local_0;  // Auto-generated

    if (!param_4) {
        SC_ZeroMem(&i, 128);
        SC_P_Ai_GetProps(param_4, &local_0);
        local_0.field13 = param_3;
        local_0.field14 = param_2;
        local_0.field15 = param;
        local_0.field16 = idx;
        SC_P_Ai_SetProps(param_4, &local_0);
        return &local_0;
    } else {
        return 32;
    }
    return;
}

int func_4218(int param, int param, int param, int param, int param) {
    int ai_props;  // Auto-generated
    int k;  // Auto-generated

    int tmp;
    int tmp2;
    int tmp4;
    int tmp6;

    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(param_4, &ai_props);
    param_3 = tmp;
    param_2 = tmp2;
    *tmp4 = param;
    *tmp6 = k;
    SC_P_Ai_SetProps(param_4, &ai_props);
    return &ai_props;
}

int func_4251(int param, int param) {
    int m;  // Auto-generated
    int player_info;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 tmp4;
    c_Vector3 tmp5;
    int local_48;
    int side;
    int side2;
    int sideB;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp14;
    int tmp15;
    int tmp16;
    int tmp17;
    int tmp18;
    int tmp19;
    int tmp20;
    int tmp21;
    int tmp22;
    int tmp3;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_P_getinfo local_34;
    s_sphere sphere;
    s_sphere tmp6;

    tmp = 10000.0f;
    *tmp1 = 1000.0f;
    sphere = tmp3;
    local_ = 32;
    SC_GetPls(&sphere, &m, &local_);
    local_34 = 0;
    tmp4 = 0;
    if (!tmp7) {
        SC_P_GetInfo(tmp10, &player_info);
        SC_P_IsReady(tmp14);
        SC_P_GetPos(tmp17, &tmp5);
        local_48 = SC_2VectorsDist(&tmp5, tmp6);
        tmp = local_48;
        local_34 = tmp21;
        tmp4 = tmp22;
    }
    return local_34;
}Skipping orphaned block 624 at address 4419 in function func_4376 - no predecessors (unreachable code)
Skipping orphaned block 633 at address 4498 in function func_4489 - no predecessors (unreachable code)
Skipping orphaned block 659 at address 4888 in function func_4883 - no predecessors (unreachable code)
Skipping orphaned block 663 at address 4917 in function func_4908 - no predecessors (unreachable code)
Skipping orphaned block 665 at address 4953 in function func_4948 - no predecessors (unreachable code)
Skipping orphaned block 669 at address 4982 in function func_4973 - no predecessors (unreachable code)
Skipping orphaned block 671 at address 5018 in function func_5013 - no predecessors (unreachable code)
Skipping orphaned block 677 at address 5066 in function func_5057 - no predecessors (unreachable code)


int func_4376(int param, int param, int param) {
    int local_4;  // Auto-generated
    int m;  // Auto-generated
    int player_info;  // Auto-generated

    c_Vector3 i;
    c_Vector3 local_;
    c_Vector3 local_1;
    c_Vector3 tmp2;
    int side;
    int side2;
    int sideB;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp14;
    int tmp15;
    int tmp16;
    int tmp17;
    int tmp18;
    int tmp19;
    int tmp21;
    int tmp22;
    int tmp3;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;

    SC_P_GetInfo(param_2, &player_info);
    tmp2 = tmp1;
    SC_P_GetPos(param_2, &sphere);
    *tmp3 = 1000.0f;
    local_ = 32;
    SC_GetPls(&sphere, &local_4, &local_);
    i = 0;
    local_1 = 0;
    SC_P_GetInfo(tmp8, &player_info);
    if (!side2) {
        SC_P_IsReady(tmp14);
    } else {
        local_1++;
    }
    if (!tmp11) goto block_632; // @4489
    goto block_630; // @4458
    tmp19 = tmp17;
    i = tmp21;
    if (!tmp22) {
        SC_Log(3, "GetMyGroup: TOO much players in group around!");
        return 2;
    } else {
        tmp19 = tmp17;
        i = tmp21;
        param_0 = m;
        return param_0;
    }
    return;
}

int func_4489(int param) {
    c_Vector3 tmp;
    c_Vector3 tmp2;
    c_Vector3 tmp3;
    int tmp1;

    tmp2 = tmp1;
    goto block_624; // @4419
    return;
}

int func_4503(int param) {
    dword local_2;  // Auto-generated
    dword player_info;  // Auto-generated

    c_Vector3 local_;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;

    local_ = 32;
    func_4376(param_0, &local_2, &local_);
    SC_P_GetInfo(param_0, &player_info);
    if (!tmp) {
        SC_Log(3, "VC %d %d couldnot find anyone to lead group %d", tmp2, tmp4, tmp6);
        return 5;
    } else {
        func_0354(local_2, 64, 0);
        func_0354(local_2.field1, 64, 0);
        SC_Log(3, "VC %d %d moved command over group", player_info.field3, player_info.field4);
        return 4;
    }
    return;
}

int func_4539(int param) {
    int tmp;
    int tmp1;
    int tmp10;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;

    if (!tmp2) {
        func_0354(tmp4, 64, 0);
        SC_Log(3, "VC %d %d moved command over group", tmp8, tmp10);
        return 4;
    } else {
        func_0354(tmp6, 64, 0);
    }
    return;
}

int func_4575(int param, int param) {
    c_Vector3 tmp;

    SC_P_GetPos(param_2, &vec);
    tmp = SC_2VectorsDist(param, &vec);
    return tmp;
}

int func_4594(int param) {
    int i;  // Auto-generated
    int idx;  // Auto-generated
    dword local_0;  // Auto-generated

    int tmp;
    int tmp2;
    int tmp4;
    int tmp6;
    int tmp8;

    SC_ZeroMem(&i, 20);
    tmp = 0;
    local_0.field1 = 0;
    local_0.field2 = 0;
    local_0.field3 = 0;
    local_0.field4 = 0;
    SC_P_SetSpecAnims(idx, &local_0);
    return &local_0;
}

int func_4634(int param, int param, int param, int param, int param, int param) {
    int i;  // Auto-generated
    int idx;  // Auto-generated
    dword local_0;  // Auto-generated

    int tmp;
    int tmp2;
    int tmp4;
    int tmp6;
    int tmp8;

    SC_ZeroMem(&i, 20);
    param_4 = tmp;
    param_3 = tmp2;
    param_2 = tmp4;
    local_0.field3 = param;
    local_0.field4 = idx;
    SC_P_SetSpecAnims(param, &local_0);
    return &local_0;
}

int func_4674(int param) {
    int local_1;  // Auto-generated
    int local_4;  // Auto-generated

    c_Vector3 local_;

    local_ = 32;
    SC_GetPls(param, &local_4, &local_);
    if (!local_) {
        local_1 = 0;
    } else {
        return 36;
    }
    return;
}

int func_4692(int param) {
    c_Vector3 tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp14;
    int tmp15;
    int tmp16;
    int tmp17;
    int tmp18;
    int tmp19;
    int tmp2;
    int tmp20;
    int tmp21;
    int tmp22;
    int tmp23;
    int tmp24;
    int tmp25;
    int tmp26;
    int tmp27;
    int tmp28;
    int tmp29;
    int tmp3;
    int tmp30;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;

    tmp = 0;
    if (!tmp1) {
        SC_P_DoHit(tmp4, 0, tmp5);
        SC_P_DoHit(tmp8, 1, tmp9);
        SC_P_DoHit(tmp12, 2, tmp13);
        SC_P_DoHit(tmp16, 3, tmp17);
        SC_P_DoHit(tmp20, 4, tmp21);
        SC_P_DoHit(tmp24, 5, tmp25);
        SC_P_DoHit(tmp28, 6, tmp29);
        tmp = tmp30;
    }
    return 36;
}

int func_4794(int param) {
    int local_4;  // Auto-generated

    int side;
    int side2;
    int sideB;
    int tmp;
    int tmp2;

    SC_P_GetPos(param, &vec);
    *tmp = side2;
    *tmp2 = 1.0f;
    SC_SphereIsVisible(&vec);
    return local_4;
}

int func_4821(int param) {
    int player_info;  // Auto-generated

    int side;
    int sideB;

    SC_P_GetInfo(param, &player_info);
    return sideB;
}

int func_4831(int param) {
    int player_info;  // Auto-generated

    int tmp;
    int tmp1;

    SC_P_GetInfo(param, &player_info);
    return tmp1;
}

int func_4841(int param) {
    int player_info;  // Auto-generated

    int tmp;
    int tmp1;

    SC_P_GetInfo(param, &player_info);
    return tmp1;
}

int func_4851(void) {
    c_Vector3 tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;

    tmp = 0;
    if (!tmp1) {
        tmp = tmp6;
    }
    tmp7 = 0;
    return &tmp7;
}

int func_4883(int param) {
    int idx;  // Auto-generated
    int local_0;  // Auto-generated

    c_Vector3 local_;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;

    local_ = 0;
    if (!tmp4) {
        SC_Log(1, "Duplicite objective added - %d", idx);
        return 3;
    } else {
        local_0++;
        Objectives[objcount] = param_0;
        Objectives[objcount].field1 = 0;
        objcount++;
        SC_SetObjectives(objcount, &Objectives, 6.0f);
        return 6.0f;
    }
    return;
}

int func_4908(int param) {
    c_Vector3 tmp1;
    int tmp;
    int tmp10;
    int tmp2;
    int tmp3;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp9;

    tmp1 = tmp;
    goto block_659; // @4888
    return;
}

int func_4948(int param) {
    int idx;  // Auto-generated
    int local_0;  // Auto-generated

    c_Vector3 local_;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;

    local_ = 0;
    if (!tmp4) {
        SC_Log(1, "Duplicite objective added - %d", idx);
        return 3;
    } else {
        local_0++;
        Objectives[objcount] = param_0;
        Objectives[objcount].field1 = 0;
        objcount++;
        SC_SetObjectivesNoSound(objcount, &Objectives, 6.0f);
        return 6.0f;
    }
    return;
}

int func_4973(int param) {
    c_Vector3 tmp1;
    int tmp;
    int tmp10;
    int tmp2;
    int tmp3;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp9;

    tmp1 = tmp;
    goto block_665; // @4953
    return;
}

int func_5013(int param) {
    int local_0;  // Auto-generated

    c_Vector3 local_;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;

    local_ = 0;
    if (!tmp4) {
        *tmp12 = 2;
        SC_SetObjectives(objcount, &Objectives, 6.0f);
        return 6.0f;
    } else {
        local_0++;
    }
    if (!tmp9) goto block_676; // @5057
    return;
}

int func_5057(void) {
    c_Vector3 tmp1;
    int tmp;

    tmp1 = tmp;
    goto block_671; // @5018
    return;
}

int func_5067(int param) {
    c_Vector3 tmp;
    int tmp1;
    int tmp10;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;

    tmp = 0;
    if (!tmp1) {
        *tmp8 = 1;
        tmp = tmp10;
    }
    SC_SetObjectives(objcount, &Objectives, 6.0f);
    return 6.0f;
}Skipping orphaned block 685 at address 5114 in function func_5109 - no predecessors (unreachable code)
Skipping orphaned block 689 at address 5145 in function func_5136 - no predecessors (unreachable code)
Skipping orphaned block 690 at address 5147 in function func_5136 - no predecessors (unreachable code)
Skipping orphaned block 696 at address 5194 in function func_5193 - no predecessors (unreachable code)
Error: type object 'ExpressionContext' has no attribute 'CAST'
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\__main__.py", line 1024, in <module>
    main()
    ~~~~^^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\__main__.py", line 311, in main
    cmd_structure(args)
    ~~~~~~~~~~~~~^^^^^^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\__main__.py", line 560, in cmd_structure
    text = format_structured_function_named(ssa_func, func_name, func_start, func_end, function_bounds=func_bounds)
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\structure\orchestrator.py", line 588, in format_structured_function_named
    lines.extend(_format_block_lines(
                 ~~~~~~~~~~~~~~~~~~~^
        ssa_func, body_block_id, base_indent + "    ", formatter,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        block_to_if, visited_ifs, emitted_blocks, cfg, start_to_block, resolver
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ))
    ^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\structure\emit\block_formatter.py", line 251, in _format_block_lines
    expressions = format_block_expressions(ssa_func, block_id, formatter=formatter)
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\expr.py", line 2473, in format_block_expressions
    store_text = formatter._format_store(inst)
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\expr.py", line 1602, in _format_store
    rendered0 = call_expr_override if call_expr_override else self._render_value(inst.inputs[0])
                                                              ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\expr.py", line 1069, in _render_value
    return self._inline_expression(value, context, parent_operator)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\flori\source\repos\VC_Scripter\vcdecomp\core\ir\expr.py", line 1883, in _inline_expression
    arg_text = self._render_value(inst.inputs[0], context=ExpressionContext.CAST)
                                                          ^^^^^^^^^^^^^^^^^^^^^^
AttributeError: type object 'ExpressionContext' has no attribute 'CAST'


int func_5109(int param) {
    int local_0;  // Auto-generated

    c_Vector3 local_;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;

    local_ = 0;
    if (!tmp4) {
        return tmp8;
    } else {
        local_0++;
    }
    return;
}

int func_5136(void) {
    int local_2;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 local_1;
    c_Vector3 tmp3;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp4;
    int tmp5;
    int tmp6;

    local_ = tmp;
    goto block_685; // @5114
    SC_P_GetBySideGroupMember(0, 0, local_);
    SC_P_IsReady(tmp3);
    if (!local_2) {
        SC_P_GetBySideGroupMember(tmp1, tmp2, local_);
        local_1 = SC_P_Ai_GetPeaceMode(tmp3);
        tmp6 = local_1;
        return local_1;
    }
    return;
}

int func_5193(void) {
    c_Vector3 tmp2;
    c_Vector3 tmp3;
    int tmp;
    int tmp1;

    goto block_690; // @5147
    return;
}

int func_5197(void) {
    int m;  // Auto-generated

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
    SC_Log("Level difficulty is %d", 10, m);
    return FALSE;
}

int func_5245(void) {
    int i;  // Auto-generated
    dword local_0;  // Auto-generated
    int local_43;  // Auto-generated

    dword local_30[16];
    dword local_36[16];
    int tmp;
    int tmp10;
    int tmp100;
    int tmp102;
    int tmp104;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp14;
    int tmp15;
    int tmp16;
    int tmp17;
    int tmp18;
    int tmp2;
    int tmp20;
    int tmp21;
    int tmp22;
    int tmp24;
    int tmp25;
    int tmp26;
    int tmp27;
    int tmp29;
    int tmp30;
    int tmp31;
    int tmp32;
    int tmp34;
    int tmp35;
    int tmp37;
    int tmp39;
    int tmp4;
    int tmp41;
    int tmp43;
    int tmp45;
    int tmp47;
    int tmp49;
    int tmp51;
    int tmp53;
    int tmp55;
    int tmp57;
    int tmp59;
    int tmp6;
    int tmp61;
    int tmp63;
    int tmp65;
    int tmp67;
    int tmp68;
    int tmp69;
    int tmp70;
    int tmp71;
    int tmp72;
    int tmp73;
    int tmp74;
    int tmp76;
    int tmp77;
    int tmp78;
    int tmp8;
    int tmp80;
    int tmp81;
    int tmp82;
    int tmp83;
    int tmp85;
    int tmp86;
    int tmp87;
    int tmp88;
    int tmp90;
    int tmp91;
    int tmp93;
    int tmp94;
    int tmp96;
    int tmp98;

    SC_ZeroMem(&i, 120);
    SC_ZeroMem(&local_30, 24);
    SC_ZeroMem(&local_36, 24);
    tmp = 0;
    local_0.field5 = 5.0f;
    local_0.field10 = 1.5f;
    local_0.field15 = 1.5f;
    local_0.field20 = 2.0f;
    tmp10 = 0;
    if (!tmp11) {
        *tmp18 = tmp15;
        local_43 = tmp22;
        local_43 = tmp27;
        *tmp32 = 0;
        tmp10 = tmp34;
    }
    tmp35 = 1;
    local_30.field1 = 4;
    local_30.field2 = 5;
    local_30.field3 = 2;
    local_30.field4 = 3;
    tmp45 = 1;
    local_36.field1 = 5;
    local_36.field2 = 3;
    local_36.field3 = 4;
    local_36.field4 = 2;
    SC_Ai_SetPlFollow(0, 0, 0, &local_0, &local_30, &local_36, 5);
    tmp55 = 0;
    local_0.field5 = 4.0f;
    local_0.field10 = 1.5f;
    local_0.field15 = 1.5f;
    local_0.field20 = 1.5f;
    local_0.field25 = 2.0f;
    tmp10 = 0;
    if (!tmp67) {
        *tmp74 = tmp71;
        local_43 = tmp78;
        local_43 = tmp83;
        *tmp88 = 0;
        local_36[tmp10] = 0;
        tmp10 = tmp93;
    }
    tmp94 = 0;
    local_30.field1 = 1;
    local_30.field2 = 4;
    local_30.field3 = 5;
    local_30.field4 = 2;
    local_30.field5 = 3;
    SC_Ai_SetPlFollow(0, 0, 1, &local_0, &local_30, &local_36, 6);
    return 6;
}

int func_5594(void) {
    SC_RadioSetDist(10.0f);
    return 10.0f;
}

int func_5599(void) {
    int i;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated
    int m;  // Auto-generated

    if (!reportedcontact) {
        return FALSE;
    } else {
        local_1 = SC_P_GetBySideGroupMember(0, 0, 4);
        return FALSE;
        SC_P_Ai_GetSureEnemies(local_1);
        SC_ggi(SGI_MISSIONALARM);
        return FALSE;
        reportedcontact = 1;
        SC_P_GetBySideGroupMember(0, 0, 4);
        SC_P_Speach(m, 4010, 4010, &i);
        local_0 = local_0 + 1.0f;
        SC_SpeachRadio(5013, 5013, &local_0);
        return TRUE;
    }
    return;
}

int func_5606(void) {
    int i;  // Auto-generated
    int j;  // Auto-generated
    int local_0;  // Auto-generated
    int m;  // Auto-generated

    c_Vector3 tmp;

    tmp = SC_P_GetBySideGroupMember(0, 0, 4);
    if (!tmp) {
        SC_P_Ai_GetSureEnemies(j);
        SC_ggi(SGI_MISSIONALARM);
        return FALSE;
        reportedcontact = 1;
        SC_P_GetBySideGroupMember(0, 0, 4);
        SC_P_Speach(m, 4010, 4010, &i);
        local_0 = local_0 + 1.0f;
        SC_SpeachRadio(5013, 5013, &local_0);
        return TRUE;
    } else {
        return FALSE;
    }
    return;
}

int func_5623(void) {
    int j;  // Auto-generated
    int local_2;  // Auto-generated

    SC_P_Ai_GetSureEnemies(j);
    if (!local_2) {
    } else {
        SC_ggi(SGI_MISSIONALARM);
        return FALSE;
    }
    return;
}

int func_5642(void) {
    int m;  // Auto-generated

    c_Vector3 tmp3;
    int tmp;
    int tmp1;
    int tmp2;

    tmp1 = 1;
    SC_P_GetBySideGroupMember(0, 0, 4);
    SC_P_Speach(m, 4010, 4010, &tmp3);
    tmp3 = tmp2;
    SC_SpeachRadio(5013, 5013, &tmp3);
    return TRUE;
}

int func_5673(void) {
    c_Vector3 tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp14;
    int tmp15;
    int tmp16;
    int tmp18;
    int tmp19;
    int tmp2;
    int tmp20;
    int tmp22;
    int tmp3;
    int tmp4;
    int tmp6;
    int tmp7;
    int tmp8;

    SC_ZeroMem(&Objectives, 0);
    tmp = 0;
    if (!tmp1) {
        *tmp4 = 0;
        *tmp8 = 1.0f;
        *tmp12 = 1;
        *tmp16 = 0;
        *tmp20 = 0;
        tmp = tmp22;
    }
    return TRUE;
}

