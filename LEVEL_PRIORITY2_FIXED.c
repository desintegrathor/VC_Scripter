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
