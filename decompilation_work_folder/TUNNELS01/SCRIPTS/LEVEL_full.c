// Structured decompilation of decompilation_work_folder/TUNNELS01/SCRIPTS/LEVEL.SCR
// Functions: 28

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword gVar;
dword gVar1;
dword gVar2;
int gVar3;
dword gVar4;
dword gVar5;
int gVar6;
dword gVar7;
dword gVar8;
int gVar9;
dword gVar10;
int gphase;

int _init(s_SC_L_info *info) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int i;
    int side;
    int side2;
    int side3;
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
    int tmp40;
    int tmp41;
    int tmp42;
    int tmp43;
    int tmp44;
    int tmp45;
    int tmp46;
    int tmp47;
    int tmp48;
    int tmp49;
    int tmp5;
    int tmp50;
    int tmp51;
    int tmp52;
    int tmp53;
    int tmp54;
    int tmp55;
    int tmp56;
    int tmp57;
    int tmp58;
    int tmp59;
    int tmp6;
    int tmp60;
    int tmp61;
    int tmp62;
    int tmp63;
    int tmp64;
    int tmp65;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    return 0;  // FIX (06-05): Synthesized return value
}

int func_0291(int param_0, int param_1) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    float i;
    int j;
    int tmp;
    int tmp1;
    int tmp2;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    tmp = frnd(param_0);
    if (!tmp1) {
        tmp = tmp2;
    } else {
        return tmp;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

void func_0354(int param_0, int param_1, int param_2) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    if (!param_2) {
        SC_P_ScriptMessage(param_2, param_0, param_0);
        return;
    } else {
        SC_Log(3, "Message %d %d to unexisted player!", param_0, param_0);
        return;
    }
    return;
}

int func_0371(int param_0, int param_1, int param_2) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int ai_props;
    int i;
    int tmp;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_P_GetBySideGroupMember(gVar, param_2, param_0);
    SC_P_Ai_GetSureEnemies(ai_props.watchfulness_zerodist);
    if (!ai_props) {
        return 0;  // FIX (06-05): Synthesized return value
    } else {
        SC_P_GetBySideGroupMember(1, param_2, param_0);
        SC_P_Ai_GetDanger(ai_props.watchfulness_zerodist);
        return 0;  // FIX (06-05): Synthesized return value
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0883(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int local_39;
    int local_40;
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
    s_SC_P_AI_props i;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_sphere local_36;
    s_sphere local_47;

    SC_PC_Get();
    SC_P_GetWeapons(local_40, &local_0);
    if (!local_0->hear_imprecision) {
        SC_sgi(101, local_0->hear_imprecision);
        SC_sgi(102, local_0->hear_distance_mult);
        SC_sgi(102, 255);
        SC_sgi(103, local_0->hear_distance_max);
        SC_sgi(103, 255);
        SC_sgi(gVar1, local_0->grenade_min_distance);
        SC_sgi(gVar2, gVar3);
        SC_sgi(gVar4, local_0->grenade_timing_imprecision);
        SC_sgi(gVar5, gVar6);
        SC_sgi(gVar7, local_0->grenade_throw_imprecision);
        SC_sgi(gVar8, gVar9);
        SC_sgi(gVar10, local_0->grenade_sure_time);
        SC_sgi(107, 255);
        SC_sgi(108, local_0->forget_enemy_mult);
        SC_sgi(108, 255);
        SC_sgi(109, local_0->shoot_damage_mult);
        SC_sgi(109, 255);
        SC_sgi(110, local_0->disable_peace_crouch);
        SC_sgi(110, 255);
        return 39;
    } else {
        SC_sgi(101, 255);
    }
    return 0;  // FIX (06-05): Synthesized return value
}

void func_1054(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int i;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_PC_Get();
    SC_P_WriteHealthToGlobalVar(local_0, 95);
    return;
}

void func_1111(void) {
    int local_1;  // Auto-generated

    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int i;
    int j;
    int m;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_PC_Get();
    SC_P_WriteAmmoToGlobalVar(local_0, 60, 89);
    SC_PC_Get();
    SC_P_GetAmmoInWeap(local_2, 2);
    SC_sgi(SGI_MISSIONALARM, local_1);
    SC_PC_Get();
    SC_P_GetAmmoInWeap(local_2, 1);
    SC_sgi(SGI_MISSIONDEATHCOUNT, local_1);
    return;
}

int func_1146(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int m;
    int tmp;
    s_SC_P_AI_props i;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_PC_GetIntel(&local_0);
    tmp = 0.0f;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_1223(int param_0, int param_1, int param_2) {
    c_Vector3 local_1;
    c_Vector3 local_128;
    c_Vector3 local_131;
    c_Vector3 local_44;
    c_Vector3 local_8;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    func_1146();
    func_0883();
    func_1111();
    func_1054();
    SC_Osi("MISSION COMPLETE");
    SC_MissionDone();
    return 0;  // FIX (06-05): Synthesized return value
}

int func_3368(int param_0, int param_1, int param_2, int param_3) {
    c_Vector3 local_1;
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int i;
    int local_;
    int tmp;
    int vec;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    local_ = SC_NOD_Get(0, param_0);
    if (!tmp) {
        SC_NOD_GetWorldPos(local_, param_0);
    } else {
        return TRUE;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_4180(int param_0, int param_1, int param_2, int param_3, int param_4) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int local_3;
    s_SC_P_AI_props ai_props;
    s_SC_P_AI_props local_0;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_35;
    s_sphere local_36;
    s_sphere local_47;

    SC_P_GetPos(param_3, &ai_props);
    SC_IsNear3D(&ai_props, param_2, param_0);
    return ai_props.boldness;
}

int func_4376(int param_0, int param_1, int param_2) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int j;
    int local_4;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp5;
    int tmp6;
    int tmp7;
    s_SC_P_AI_props i;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_34;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_SC_P_getinfo m;
    s_SC_P_getinfo player_info;
    s_sphere local_36;
    s_sphere local_47;
    s_sphere sphere;

    SC_P_GetInfo(param_2, &player_info);
    tmp2 = local_40->group;
    SC_P_GetPos(param_2, &sphere);
    *tmp3 = 1000.0f;
    tmp5 = 32;
    SC_GetPls(&sphere, &local_4, &tmp5);
    tmp6 = 0.0f;
    tmp7 = 0.0f;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_4575(int param_0, int param_1, int param_2, int param_3, int param_4, int param_5) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int local_3;
    int local_4;
    int tmp;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props player_info;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_P_GetPos(param_2, &player_info);
    tmp = SC_2VectorsDist(param_0, &player_info);
    return tmp;
}

int func_4948(int param_0, int param_1) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int tmp;
    s_SC_P_AI_props i;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    tmp = 0.0f;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_5197(int param_0, int param_1) {
    dword vec;  // Auto-generated
    int z;  // Auto-generated

    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_5;
    c_Vector3 local_8;
    int n;
    s_SC_NET_info local_30;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_sgi(SGI_LEVBASE_GROUP0, SGI_LEVBASE_GROUP1);
    SC_sgi(SGI_LEVBASE_GROUP2, 0.0f);
    SC_sgi(SGI_LEVELPHASE, 0.0f);
    SC_sgi(SGI_ALLYDEATHCOUNT, 0.0f);
    SC_sgi(SGI_TEAMDEATHCOUNT, 0.0f);
    SC_sgi(SGI_LEVBASE_CLAYOUT1, SGI_LEVBASE_CLAYOUT2);
    SC_sgi(SGI_LEVBASE_CLAYOUT3, SGI_LEVBASE_CLAYOUT4);
    SC_sgi(SGI_LEVBASE_CLAYIN1, SGI_LEVBASE_CLAYIN2);
    SC_sgi(SGI_LEVBASE_CLAYIN3, SGI_LEVBASE_CLAYIN4);
    SC_ggi(SGI_DIFFICULTY);
    SC_Log("Level difficulty is %d", 10, vec.z);
    return 0;  // FIX (06-05): Synthesized return value
}

int func_6196(int param_0, int param_1) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int i;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    switch (param_0) {
    case 0:
        return TRUE;
    case 1:
        if (param_2) break;
        return TRUE;
    case 2:
        if (tmp4) {
            return TRUE;
        }
        break;
    case 3:
        if (tmp6) {
            return TRUE;
        }
        break;
    case 4:
        if (param_2) {
            return TRUE;
        }
        break;
    default:
        return 0;  // FIX (06-05): Synthesized return value
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_6259(int param_0, int param_1) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_6;
    c_Vector3 local_8;
    int i;
    int j;
    int tmp;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    switch (SC_P_Ai_GetPeaceMode(j)) {
    case 2:
        SC_Ai_SetPeaceMode(0.0f, 0.0f, 0.0f);
        SC_Ai_PointStopDanger(0.0f, 0.0f);
        break;
    default:
        return 0;  // FIX (06-05): Synthesized return value
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_6804(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int tmp;
    s_SC_P_AI_props i;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    tmp = 1;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_6873(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int tmp;
    s_SC_P_AI_props i;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    tmp = 0.0f;
    return 0;  // FIX (06-05): Synthesized return value
}

void func_6984(int param_0) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int i;
    int t7001_;
    int t7010_;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp6;
    int tmp7;
    int tmp9;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    switch (local_0) {
    case 0:
        break;
    case 1:
        *tmp4 = 0.0f;
        *tmp7 = 1;
        break;
    case 2:
        break;
    case 3:
        break;
    case 4:
        break;
    case 5:
        break;
    case 6:
        break;
    default:
        return;
    }
    return;
}

int func_7043(int param_0) {
    c_Vector3 local_1;
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    c_Vector3 vec;
    float i;
    float local_4;
    int local_;
    int local_5;
    int local_6;
    int local_7;
    int param_;
    int t7070_;
    int t7110_;
    int t7118_;
    int t7125_;
    int t7139_;
    int t7236_;
    int t7244_;
    int t7251_;
    int t7280_;
    int t7310_;
    int t7420_;
    int t7449_;
    int t7478_;
    int t7512_;
    int t7527_;
    int t7589_;
    int t7652_;
    int t7674_;
    int t7690_;
    int tmp;
    int tmp1;
    int tmp100;
    int tmp101;
    int tmp102;
    int tmp103;
    int tmp104;
    int tmp105;
    int tmp106;
    int tmp107;
    int tmp108;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp14;
    int tmp15;
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
    int tmp37;
    int tmp38;
    int tmp39;
    int tmp4;
    int tmp40;
    int tmp41;
    int tmp43;
    int tmp44;
    int tmp45;
    int tmp46;
    int tmp48;
    int tmp49;
    int tmp5;
    int tmp50;
    int tmp51;
    int tmp53;
    int tmp54;
    int tmp55;
    int tmp56;
    int tmp57;
    int tmp58;
    int tmp59;
    int tmp6;
    int tmp60;
    int tmp62;
    int tmp63;
    int tmp64;
    int tmp65;
    int tmp67;
    int tmp68;
    int tmp69;
    int tmp7;
    int tmp70;
    int tmp72;
    int tmp73;
    int tmp74;
    int tmp75;
    int tmp77;
    int tmp78;
    int tmp79;
    int tmp8;
    int tmp81;
    int tmp82;
    int tmp83;
    int tmp84;
    int tmp86;
    int tmp87;
    int tmp88;
    int tmp89;
    int tmp9;
    int tmp90;
    int tmp92;
    int tmp93;
    int tmp94;
    int tmp96;
    int tmp97;
    int tmp98;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    switch (param_0) {
    case 0:
        if (tmp5) {
            SC_PC_Get();
            SC_P_Speech2(local_5, 903, &local_);
            local_ = tmp6;
            *tmp9 = -100;
            *tmp15 = tmp13;
        } else {
            SC_PC_Get();
            SC_P_Speech2(local_5, 904, &local_);
            local_ = tmp7;
        }
        break;
    default:
        if (tmp21) {
            rand();
            if (tmp22) {
                SC_PC_Get();
                SC_P_Speech2(local_5, tmp32, &local_);
                local_ = tmp23;
                *tmp35 = -100;
                *tmp41 = tmp39;
                return tmp108;
            } else {
                SC_PC_Get();
                SC_P_Speech2(local_5, 911, &local_);
                local_ = tmp24;
            }
        } else {
            SC_PC_Get();
            func_4575(tmp26);
            SC_PC_Get();
            func_4575(tmp33, tmp27);
            if (tmp28) {
                SC_PC_Get();
                rand();
                SC_P_Speech2(local_5, tmp30, &local_);
                local_ = tmp31;
            } else {
            }
        }
    }
    if (!tmp43) {
        SC_PC_Get();
        SC_P_Speech2(local_5, 906, &local_);
        local_ = tmp44;
        *tmp46 = -100;
    } else {
        SC_PC_Get();
        SC_P_SpeechMes2(local_5, 907, &local_, 11);
        local_ = tmp49;
        *tmp51 = -100;
        SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
        SC_P_GetPos(local_5, &vec);
        SC_SND_PlaySound3D(2060, &vec);
        local_ = tmp54;
        SC_PC_Get();
        SC_P_SpeechMes2(local_5, 912, &local_, 12);
        local_ = tmp55;
        local_ = 0.5f;
        SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
        SC_P_Speech2(local_5, 913, &local_);
        local_ = tmp56;
        SC_P_GetBySideGroupMember(tmp100, tmp101, tmp102);
        SC_P_Speech2(local_5, tmp103, &local_);
        local_ = tmp57;
        SC_P_GetBySideGroupMember(tmp104, tmp105, tmp106);
        SC_P_SpeechMes2(local_5, tmp107, &local_, tmp108);
        local_ = tmp58;
        *tmp60 = -100;
        SC_PC_Get();
        SC_P_Speech2(local_5, 921, &local_);
        local_ = tmp63;
        *tmp65 = -100;
        SC_PC_Get();
        SC_P_Speech2(local_5, 922, &local_);
        local_ = tmp68;
        *tmp70 = -100;
        SC_P_GetBySideGroupMember(1, 0.0f, 1);
        SC_P_SpeechMes2(local_5, 924, &local_, 14);
        local_ = tmp73;
        *tmp75 = -100;
        *tmp79 = -100;
        SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
        SC_P_Ai_SetMode(local_5, 0.0f);
        SC_GetWp("WayPoint113", &vec);
        SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
        SC_P_Ai_Go(local_5, &vec);
        SC_PC_Get();
        SC_P_SpeechMes2(local_5, 932, &local_, 15);
        local_ = tmp82;
        *tmp84 = -100;
        SC_P_GetBySideGroupMember(1, 1, 0.0f);
        SC_P_GetPos(local_5, &vec);
        SC_SND_PlaySound3D(10419, &vec);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_GetPos(local_5, &vec);
        SC_SND_PlaySound3D(10419, &vec);
        SC_PC_Get();
        SC_P_Speech2(local_5, 944, &local_);
        local_ = tmp87;
        tmp88 = 1;
        *tmp90 = -100;
        SC_AGS_Set(1);
        *tmp94 = -100;
        func_1223();
        *tmp98 = -100;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_7697(float param_0, int param_1) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    int tmp;
    s_SC_P_AI_props i;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    tmp = 0.0f;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_7807(float param_0) {
    int local_1;  // Auto-generated

    c_Vector3 local_128;
    c_Vector3 local_44;
    float i;
    float local_5;
    float local_7;
    int data_;
    int data_1757;
    int data_1758;
    int data_1763;
    int j;
    int local_;
    int local_6;
    int local_8;
    int local_9;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp100;
    int tmp101;
    int tmp102;
    int tmp103;
    int tmp104;
    int tmp105;
    int tmp106;
    int tmp107;
    int tmp108;
    int tmp109;
    int tmp11;
    int tmp110;
    int tmp111;
    int tmp112;
    int tmp113;
    int tmp114;
    int tmp115;
    int tmp116;
    int tmp117;
    int tmp118;
    int tmp119;
    int tmp12;
    int tmp120;
    int tmp121;
    int tmp122;
    int tmp123;
    int tmp124;
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
    int tmp40;
    int tmp41;
    int tmp42;
    int tmp43;
    int tmp44;
    int tmp45;
    int tmp46;
    int tmp47;
    int tmp48;
    int tmp49;
    int tmp5;
    int tmp50;
    int tmp51;
    int tmp52;
    int tmp53;
    int tmp54;
    int tmp55;
    int tmp56;
    int tmp57;
    int tmp58;
    int tmp59;
    int tmp6;
    int tmp60;
    int tmp61;
    int tmp62;
    int tmp63;
    int tmp64;
    int tmp65;
    int tmp66;
    int tmp67;
    int tmp68;
    int tmp69;
    int tmp7;
    int tmp70;
    int tmp71;
    int tmp72;
    int tmp73;
    int tmp74;
    int tmp75;
    int tmp76;
    int tmp77;
    int tmp78;
    int tmp79;
    int tmp8;
    int tmp80;
    int tmp81;
    int tmp82;
    int tmp83;
    int tmp84;
    int tmp85;
    int tmp86;
    int tmp87;
    int tmp88;
    int tmp89;
    int tmp9;
    int tmp90;
    int tmp91;
    int tmp92;
    int tmp93;
    int tmp94;
    int tmp95;
    int tmp96;
    int tmp97;
    int tmp98;
    int tmp99;
    int vcrunpoint2;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_SC_P_getinfo vec;
    s_sphere local_36;
    s_sphere local_47;

    switch (param_0) {
    case 0:
        SC_P_GetBySideGroupMember(tmp7, tmp8, tmp9);
        if (!SC_P_IsReady(local_)) break;
        if (!func_0371(tmp4, tmp5)) break;
        SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
        SC_P_Speech2(local_6, 926, &tmp3);
        tmp3 = tmp2;
        data_ = 1;
        break;
    case 1:
        SC_P_GetBySideGroupMember(tmp21, tmp22, tmp23);
        if (SC_P_IsReady(local_)) {
            SC_P_GetBySideGroupMember(tmp24, tmp25, tmp26);
            if (func_4180(&tmp27, tmp28)) {
                SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
                SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_BATTLE);
                data_ = 2;
            }
            if (tmp29) {
            } else {
                SC_P_GetBySideGroupMember(tmp32, tmp33, tmp34);
                if (SC_P_IsReady(local_6)) {
                } else {
                    SC_P_GetBySideGroupMember(tmp35, tmp36, tmp37);
                    if (SC_P_IsReady(local_6)) {
                        if (tmp38) {
                        } else {
                            SC_P_GetBySideGroupMember(tmp41, tmp42, tmp43);
                            if (SC_P_IsReady(local_6)) {
                            } else {
                                SC_P_GetBySideGroupMember(tmp44, tmp45, tmp46);
                                if (SC_P_IsReady(local_6)) {
                                } else {
                                    SC_P_GetBySideGroupMember(tmp47, tmp48, tmp49);
                                    if (SC_P_IsReady(local_6)) {
                                        if (tmp50 && local_5) {
                                            SC_P_GetBySideGroupMember(1, 1, 0.0f);
                                            rand();
                                            SC_P_Speech2(local_5, tmp52, &tmp3);
                                            tmp3 = tmp53;
                                            SC_P_GetBySideGroupMember(1, 1, 0.0f);
                                            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
                                            SC_P_GetBySideGroupMember(1, 1, 1);
                                            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
                                            SC_P_GetBySideGroupMember(1, 1, 2);
                                            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
                                            data_1757 = 100;
                                        }
                                        if (tmp56 && local_5) {
                                            SC_P_GetBySideGroupMember(1, 1, 1);
                                            rand();
                                            SC_P_Speech2(local_5, tmp58, &tmp3);
                                            tmp3 = tmp59;
                                            SC_P_GetBySideGroupMember(1, 1, 0.0f);
                                            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
                                            SC_P_GetBySideGroupMember(1, 1, 1);
                                            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
                                            SC_P_GetBySideGroupMember(1, 1, 2);
                                            SC_P_Ai_SetMode(local_5, SGI_INTELCOUNT);
                                            data_1757 = 100;
                                        }
                                        if (tmp62 && local_5) {
                                            SC_P_GetBySideGroupMember(1, 1, 2);
                                            rand();
                                            SC_P_Speech2(local_5, tmp64, &tmp3);
                                            tmp3 = tmp65;
                                            SC_P_GetBySideGroupMember(1, 1, 0.0f);
                                            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
                                            SC_P_GetBySideGroupMember(1, 1, 1);
                                            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
                                            SC_P_GetBySideGroupMember(1, 1, 2);
                                            SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
                                            data_1757 = 100;
                                        }
                                        if (tmp68) {
                                        } else {
                                            if (tmp69) {
                                                SC_P_GetBySideGroupMember(1, tmp98, tmp99);
                                                SC_P_Ai_SetMode(local_6, 0.0f);
                                                SC_P_GetBySideGroupMember(tmp100, tmp101, 1);
                                                SC_P_Ai_SetMode(local_6, tmp102);
                                                SC_P_GetBySideGroupMember(tmp103, tmp104, tmp105);
                                                SC_P_Ai_SetMode(local_6, tmp106);
                                                SC_P_GetBySideGroupMember(tmp107, tmp108, tmp109);
                                                SC_P_Ai_Stop(local_6);
                                                SC_P_GetBySideGroupMember(tmp110, tmp111, tmp112);
                                                SC_P_Ai_Stop(local_6);
                                                SC_P_GetBySideGroupMember(tmp113, tmp114, tmp115);
                                                SC_P_Ai_Stop(local_6);
                                                frnd(20.0f);
                                                tmp71 = tmp70;
                                                rand();
                                                data_1758 = tmp72;
                                                SC_P_GetBySideGroupMember(tmp117, tmp118, data_1758);
                                                SC_P_GetPos(local_6, &local_2);
                                                SC_P_GetBySideGroupMember(tmp119, tmp120, tmp121);
                                                SC_P_Ai_Go(local_6, &local_2);
                                                SC_P_GetBySideGroupMember(tmp122, tmp123, tmp124);
                                                SC_P_GetPos(local_6, &data_1763);
                                                data_1757 = 2;
                                            } else {
                                                if (tmp73) {
                                                    if (tmp74) {
                                                    } else {
                                                        if (tmp75) {
                                                            SC_P_GetBySideGroupMember(1, 1, 2);
                                                            SC_P_GetBySideGroupMember(1, 1, data_1758);
                                                            SC_P_GetDistance(data_1758, local_9);
                                                            if (tmp76) {
                                                                SC_P_GetBySideGroupMember(1, 1, 2);
                                                                rand();
                                                                SC_P_Speech2(local_, tmp78, &tmp3);
                                                                tmp3 = tmp79;
                                                                SC_P_GetBySideGroupMember(1, 1, 2);
                                                                SC_P_Ai_Go(local_, &data_1763);
                                                                data_1758 = 2;
                                                            }
                                                        } else {
                                                            if (tmp80) {
                                                                SC_P_GetBySideGroupMember(1, 1, 2);
                                                                if (func_4180(&data_1763, 3.0f)) {
                                                                    rand();
                                                                    data_1758 = tmp81;
                                                                    SC_P_GetBySideGroupMember(1, 1, data_1758);
                                                                    SC_P_GetPos(local_, &local_2);
                                                                    SC_P_GetBySideGroupMember(1, 1, 2);
                                                                    SC_P_Ai_Go(local_, &local_2);
                                                                }
                                                            }
                                                        }
                                                        tmp71 = tmp83;
                                                        if (tmp84) {
                                                            frnd(20.0f);
                                                            tmp71 = tmp85;
                                                            tmp3 = 0.0f;
                                                            rand();
                                                            SC_P_GetBySideGroupMember(1, 1, tmp86);
                                                            rand();
                                                            SC_P_Speech2(local_6, tmp88, &tmp3);
                                                            tmp3 = tmp89;
                                                        } else {
                                                            tmp91 = tmp90;
                                                            if (tmp92) {
                                                                frnd(5.0f);
                                                                tmp91 = tmp93;
                                                                SC_P_GetBySideGroupMember(1, 1, 0.0f);
                                                                SC_P_GetPos(local_6, &local_2);
                                                                SC_SND_PlaySound3D(10419, &local_2);
                                                            } else {
                                                                tmp95 = tmp94;
                                                                if (tmp96) {
                                                                    frnd(5.0f);
                                                                    tmp95 = tmp97;
                                                                    SC_P_GetBySideGroupMember(1, 1, 1);
                                                                    SC_P_GetPos(local_6, &local_2);
                                                                    SC_SND_PlaySound3D(10419, &local_2);
                                                                }
                                                                return &data_1763;
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    } else {
                                        tmp38 = SGI_HELIFULL;
                                        SC_PC_Get();
                                        SC_P_GetWillTalk(local_6);
                                        tmp3 = tmp39;
                                        SC_PC_Get();
                                        SC_P_Speech2(local_5, 931, &tmp3);
                                        tmp3 = tmp40;
                                    }
                                }
                            }
                        }
                    } else {
                        tmp29 = SGI_PILOTPOS;
                        SC_PC_Get();
                        SC_P_GetWillTalk(local_6);
                        tmp3 = tmp30;
                        SC_PC_Get();
                        SC_P_Speech2(local_5, SGI_C4_PLANTED, &tmp3);
                        tmp3 = tmp31;
                    }
                }
            }
        } else {
            SC_PC_Get();
            tmp3 = SC_P_GetWillTalk(local_);
            SC_PC_Get();
            SC_P_Speech2(local_6, 927, &tmp3);
            tmp3 = tmp10;
            data_ = 100;
        }
        break;
    case 2:
        SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
        if (SC_P_Ai_GetShooting(local_, &local_1)) {
            SC_PC_Get();
            tmp3 = SC_P_GetWillTalk(local_);
            SC_PC_Get();
            SC_P_Speech2(local_6, 929, &tmp3);
            tmp3 = tmp12;
            data_ = 3;
        }
        break;
    case 3:
        SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
        if (SC_P_IsReady(local_)) {
            tmp16 = tmp15;
            if (tmp17) {
                SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
                SC_P_Ai_SetMode(local_6, 0.0f);
                SC_P_GetBySideGroupMember(1, SGI_BYTHEAMMO, SGI_MF_HELIGO);
                SC_P_Ai_Go(local_6, &vcrunpoint2);
                SC_PC_Get();
                SC_P_GetWillTalk(local_);
                tmp3 = tmp18;
                SC_PC_Get();
                SC_P_Speech2(local_6, SGI_NUM_C4, &tmp3);
                tmp3 = tmp19;
                data_ = SGI_TEAM2LEFT;
            }
        } else {
            SC_PC_Get();
            tmp3 = SC_P_GetWillTalk(local_);
            SC_PC_Get();
            SC_P_Speech2(local_6, 927, &tmp3);
            tmp3 = tmp14;
            data_ = 100;
        }
        break;
    case 4:
        SC_P_GetBySideGroupMember(SGI_ACTIVATE_VC, SGI_TESTGREN, SGI_CLOSEDOORS);
        if (func_4180(&tmp27, SGI_INTRO)) {
            SC_P_GetBySideGroupMember(SGI_DOORSDSTR, SGI_UNDERFUCKIT, SGI_BP_ALARM03);
            SC_P_Ai_SetMode(local_6, SGI_BP_ALARM04);
            data_ = SGI_BP_ALARM05;
        }
        break;
    default:
    }
    return 0;  // FIX (06-05): Synthesized return value
}

void func_8919(void) {
    dword openablecrate;  // Auto-generated
    dword past;  // Auto-generated
    dword poklop;  // Auto-generated

    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_SetObjectScript("grenadebedna", "levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\openablecrate.c");
    SC_SetObjectScript("n_poklop_01", "levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\poklop.c");
    SC_SetObjectScript("d_past_04_01", "levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\past.c");
    return;
}

void func_8932(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    return;
}

void func_8933(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    return;
}

int func_8934(void) {
    int local_1;  // Auto-generated

    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    float i;
    int j;
    int local_;
    int m;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp12;
    int tmp13;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_PC_Get();
    tmp = SC_P_GetWillTalk(local_);
    if (!tmp4) {
    } else {
        SC_NOD_GetName(tmp2);
        SC_StringSame(local_, &tmp5);
        SC_PC_Get();
        SC_P_Speech2(local_1, 923, &tmp);
        tmp = tmp3;
        tmp4 = 1;
        return &tmp4;
    }
    if (!tmp9) {
    } else {
        SC_NOD_GetName(tmp7);
        SC_StringSame(local_, &tmp10);
        SC_PC_Get();
        SC_P_Speech2(local_1, 938, &tmp);
        tmp = tmp8;
        tmp9 = 1;
        return &tmp9;
    }
    SC_NOD_GetName(tmp12);
    SC_StringSame(local_, "granat_v_plechovce2#3");
    if (!local_1) {
        SC_PC_Get();
        SC_P_Speech2(local_1, 925, &tmp);
        tmp = tmp13;
        return &tmp;
    } else {
        return &tmp10;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int ScriptMain(s_SC_L_info *info) {
    dword param_1;  // Auto-generated

    c_Vector3 local_128;
    c_Vector3 local_44;
    c_Vector3 local_8;
    dword local_22[16];
    dword local_2[16];
    dword local_4[16];
    float j;
    float local_23;
    float local_24;
    int initside;
    int local_;
    int local_20;
    int local_21;
    int local_9;
    int param_;
    int tmp;
    int tmp10;
    int tmp100;
    int tmp101;
    int tmp102;
    int tmp103;
    int tmp104;
    int tmp105;
    int tmp106;
    int tmp107;
    int tmp108;
    int tmp109;
    int tmp11;
    int tmp110;
    int tmp111;
    int tmp112;
    int tmp113;
    int tmp114;
    int tmp116;
    int tmp118;
    int tmp12;
    int tmp120;
    int tmp121;
    int tmp122;
    int tmp123;
    int tmp124;
    int tmp125;
    int tmp126;
    int tmp127;
    int tmp128;
    int tmp129;
    int tmp13;
    int tmp131;
    int tmp133;
    int tmp135;
    int tmp136;
    int tmp137;
    int tmp138;
    int tmp139;
    int tmp14;
    int tmp140;
    int tmp141;
    int tmp142;
    int tmp143;
    int tmp144;
    int tmp146;
    int tmp148;
    int tmp15;
    int tmp150;
    int tmp151;
    int tmp152;
    int tmp153;
    int tmp154;
    int tmp155;
    int tmp156;
    int tmp157;
    int tmp158;
    int tmp159;
    int tmp160;
    int tmp161;
    int tmp162;
    int tmp163;
    int tmp164;
    int tmp165;
    int tmp166;
    int tmp167;
    int tmp168;
    int tmp169;
    int tmp17;
    int tmp170;
    int tmp171;
    int tmp173;
    int tmp174;
    int tmp175;
    int tmp176;
    int tmp177;
    int tmp178;
    int tmp179;
    int tmp181;
    int tmp19;
    int tmp2;
    int tmp21;
    int tmp23;
    int tmp25;
    int tmp27;
    int tmp29;
    int tmp3;
    int tmp31;
    int tmp33;
    int tmp35;
    int tmp37;
    int tmp39;
    int tmp4;
    int tmp41;
    int tmp43;
    int tmp44;
    int tmp45;
    int tmp46;
    int tmp47;
    int tmp48;
    int tmp49;
    int tmp5;
    int tmp50;
    int tmp51;
    int tmp52;
    int tmp53;
    int tmp54;
    int tmp55;
    int tmp56;
    int tmp57;
    int tmp58;
    int tmp59;
    int tmp6;
    int tmp60;
    int tmp61;
    int tmp62;
    int tmp63;
    int tmp64;
    int tmp65;
    int tmp66;
    int tmp67;
    int tmp68;
    int tmp69;
    int tmp7;
    int tmp70;
    int tmp71;
    int tmp72;
    int tmp73;
    int tmp74;
    int tmp75;
    int tmp76;
    int tmp77;
    int tmp78;
    int tmp79;
    int tmp8;
    int tmp80;
    int tmp81;
    int tmp82;
    int tmp83;
    int tmp84;
    int tmp85;
    int tmp86;
    int tmp87;
    int tmp88;
    int tmp89;
    int tmp9;
    int tmp90;
    int tmp91;
    int tmp92;
    int tmp93;
    int tmp94;
    int tmp95;
    int tmp96;
    int tmp97;
    int tmp98;
    int tmp99;
    int vec;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_SC_P_getinfo m;
    s_sphere local_36;
    s_sphere local_47;

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
        break;
    case 51:
        func_8934(param_);
        break;
    case 1:
        SC_PC_Get();
        local_ = SC_P_GetWillTalk(initside);
        SC_PC_EnableMovement(tmp81);
        SC_PC_EnableRadioBreak(tmp82);
        break;
    case 2:
        break;
    case 15:
        if (tmp170) {
            param_1->field_12 = 0.0f;
        } else {
            tmp179 = tmp177;
            param_1->field_12 = 1;
        }
        break;
    case 3:
        if (tmp140) {
        } else {
            save[tmp142] = 1;
            SC_PC_EnableMovement(1);
            *tmp146 = 0.0f;
            initside = 9114;
            *tmp148 = 9115;
            SC_MissionSave(&initside);
            SC_Log(3, "Saving game id %d", 9114);
            SC_Osi("Saving game id %d", 9114);
        }
        break;
    case 12:
        SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
        SC_P_GetPos(initside, &local_9);
        SC_SND_PlaySound3D(2055, &local_9);
        break;
    case 13:
        SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
        SC_P_GetPos(initside, &local_9);
        SC_SND_PlaySound3D(2060, &local_9);
        SC_P_GetBySideGroupMember(1, tmp156, tmp157);
        SC_P_GetPos(initside, &local_9);
        SC_SND_PlaySound3D(tmp158, &local_9);
        SC_GetWp(&tmp159, &local_9);
        SC_P_GetBySideGroupMember(tmp160, tmp161, tmp162);
        SC_P_SetPos(initside, &local_9);
        SC_GetWp(&tmp163, &local_9);
        SC_P_GetBySideGroupMember(tmp164, tmp165, tmp166);
        SC_P_SetPos(initside, &local_9);
        break;
    case 14:
        SC_GetWp("WayPoint57", &local_9);
        SC_P_GetBySideGroupMember(1, 0.0f, 0.0f);
        SC_P_SetPos(initside, &local_9);
        break;
    default:
        SC_Radio_Enable(2);
    }
    SC_sgi(SGI_CURRENTMISSION, 9);
    SC_ZeroMem(local_2, 8);
    SC_ZeroMem(local_4, 20);
    func_5197();
    SC_DeathCamera_Enable(0);
    SC_RadioSetDist(10.0f);
    SC_ZeroMem(&initside, 8);
    initside = 32;
    *tmp15 = 8;
    SC_InitSide(0.0f, &initside);
    SC_ZeroMem(&initside, 8);
    initside = 64;
    *tmp17 = 16;
    SC_InitSide(1, &initside);
    SC_ZeroMem(&initside, 20);
    initside = 0.0f;
    *tmp19 = 0.0f;
    *tmp21 = 4;
    *tmp23 = 30.0f;
    SC_InitSideGroup(&initside);
    SC_ZeroMem(&initside, tmp50);
    initside = 1;
    *tmp25 = 0.0f;
    *tmp27 = 9;
    SC_InitSideGroup(&initside);
    SC_ZeroMem(&initside, tmp51);
    initside = 1;
    *tmp29 = 1;
    *tmp31 = 16;
    SC_InitSideGroup(&initside);
    SC_ZeroMem(&initside, tmp52);
    initside = 1;
    *tmp33 = 2;
    *tmp35 = 16;
    SC_InitSideGroup(&initside);
    SC_ZeroMem(&initside, tmp53);
    initside = 1;
    *tmp37 = 3;
    *tmp39 = 9;
    SC_InitSideGroup(&initside);
    SC_Ai_SetShootOnHeardEnemyColTest(tmp54);
    SC_Ai_SetGroupEnemyUpdate(tmp55, tmp56, tmp57);
    SC_Ai_SetGroupEnemyUpdate(tmp58, tmp59, tmp60);
    SC_Ai_SetGroupEnemyUpdate(tmp61, tmp62, tmp63);
    SC_Ai_SetGroupEnemyUpdate(tmp64, tmp65, tmp66);
    tmp14 = 1;
    SC_sgi(tmp67, tmp68);
    SC_Log(tmp69, &tmp70, tmp71);
    SC_Osi(&tmp73, tmp74);
    SC_SetCommandMenu(tmp76);
    param_1->field_20 = 0.5f;
    goto block_1097; // @9436
    local_ = 1.0f;
    SC_AGS_Set(0.0f);
    SC_PC_Get();
    SC_P_SpeechMes2(initside, 900, &local_, 1);
    local_ = tmp44;
    func_4948(901);
    func_4948(902);
    func_4948(1475);
    func_6873();
    tmp14 = 2;
    SC_sgi(SGI_LEVELPHASE, 2);
    SC_Log(3, "Levelphase changed to %d", 2);
    SC_Osi("Levelphase changed to %d", 2);
    goto block_1097; // @9436
    SC_PC_GetPos(&local_9);
    func_7697(&local_9, tmp47);
    func_7807(&local_9, tmp49);
    block_1097:
    SC_RadioBatch_Begin();
    SC_PC_Get();
    SC_P_Speech2(initside, 916, &local_);
    local_ = tmp83;
    func_0291(local_, 0.3f);
    local_ = tmp84;
    SC_SpeechRadio2(917, &local_);
    func_0291(local_, 0.1f, 0.2f);
    local_ = tmp86;
    SC_PC_Get();
    SC_P_Speech2(initside, 918, &local_);
    local_ = tmp87;
    func_0291(local_, 0.3f);
    local_ = tmp88;
    SC_SpeechRadio2(919, &local_);
    func_0291(local_, 0.1f, 0.2f);
    local_ = tmp90;
    SC_PC_Get();
    SC_P_SpeechMes2(initside, 920, &local_, 2);
    local_ = tmp91;
    SC_RadioBatch_End();
    goto block_1107; // @9679
    SC_RadioBatch_Begin();
    SC_PC_Get();
    SC_P_Speech2(initside, 933, &local_);
    local_ = tmp93;
    func_0291(local_, 0.3f);
    local_ = tmp94;
    SC_SpeechRadio2(934, &local_);
    func_0291(local_, 0.1f, 0.2f);
    local_ = tmp96;
    SC_PC_Get();
    SC_P_Speech2(initside, 935, &local_);
    local_ = tmp97;
    func_0291(local_, 0.3f);
    local_ = tmp98;
    SC_SpeechRadio2(936, &local_);
    func_0291(local_, 0.1f, 0.2f);
    local_ = tmp100;
    SC_PC_Get();
    SC_P_SpeechMes2(initside, 937, &local_, 3);
    local_ = tmp101;
    SC_RadioBatch_End();
    block_1107:
    if (!tmp110) {
    } else {
        save[tmp112] = 1;
        *tmp116 = 0.0f;
        initside = 9110;
        *tmp118 = 9111;
        SC_MissionSave(&initside);
        SC_Log(3, "Saving game id %d", 9110);
        SC_Osi("Saving game id %d", 9110);
    }
    if (!tmp125) {
    } else {
        save[tmp127] = 1;
        SC_PC_EnableMovement(1);
        *tmp131 = 0.0f;
        initside = 9112;
        *tmp133 = 9113;
        SC_MissionSave(&initside);
        SC_Log(3, "Saving game id %d", 9112);
        SC_Osi("Saving game id %d", 9112);
    }
    SC_Radio_Enable(1);
    if (!tmp155) {
        func_1223();
    }
    return 0;  // FIX (06-05): Synthesized return value
}

