// Structured decompilation of decompilation_work_folder/TUNNELS01/SCRIPTS/PLAYER.SCR
// Functions: 15

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword gVar;
dword gVar1;
int gVar2;
dword gVar3;
dword gVar4;
int gVar5;
dword gVar6;
dword gVar7;
int gVar8;
dword gVar9;
int gphase;

int _init(s_SC_L_info *info) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    return 0;  // FIX (06-05): Synthesized return value
}

int func_0064(int param_0, int param_1, int param_2) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    if (!param_2) {
        SC_P_ScriptMessage(param_2, param_0, param_0);
        return 0;  // FIX (06-05): Synthesized return value
    } else {
        SC_Log(3, "Message %d %d to unexisted player!", param_0, param_0);
        return 0;  // FIX (06-05): Synthesized return value
    }
    return 0;  // FIX (06-05): Synthesized return value
}

void func_0318(void) {
    dword param_0;  // Auto-generated

    c_Vector3 local_128;
    c_Vector3 local_44;
    int i;
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
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    switch (SC_ggi(tmp34)) {
    case 255:
        param_0->field_40 = 0.0f;
        break;
    case 12:
        param_0->field_48 = 23;
        break;
    default:
        param_0->field_68 = 63;
    }
    param_0->field_40 = 29;
    param_0->field_44 = SC_ggi(102);
    if (!tmp14) {
        param_0->field_44 = 0.0f;
        param_0->field_48 = SC_ggi(103);
        SC_ggi(tmp35);
        param_0->field_48 = 25;
        param_0->field_48 = 1;
        param_0->field_48 = 0.0f;
        param_0->field_52 = 0.0f;
        param_0->field_56 = SC_ggi(105);
        param_0->field_56 = 59;
        param_0->field_56 = 0.0f;
        param_0->field_60 = 0.0f;
        param_0->field_64 = 0.0f;
        param_0->field_68 = SC_ggi(108);
        param_0->field_68 = 0.0f;
        param_0->field_72 = SC_ggi(109);
        param_0->field_72 = 0.0f;
        param_0->field_76 = 58;
        return;
    } else {
        param_0->field_44 = 7;
    }
    return;
}

int func_0593(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
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
        SC_sgi(gVar, local_0->grenade_min_distance);
        SC_sgi(gVar1, gVar2);
        SC_sgi(gVar3, local_0->grenade_timing_imprecision);
        SC_sgi(gVar4, gVar5);
        SC_sgi(gVar6, local_0->grenade_throw_imprecision);
        SC_sgi(gVar7, gVar8);
        SC_sgi(gVar9, local_0->grenade_sure_time);
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

void func_0756(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    int i;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_PC_Get();
    SC_P_ReadHealthFromGlobalVar(local_0, 95);
    return;
}

void func_0764(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
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

void func_0772(void) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    int i;
    int idx;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_PC_Get();
    SC_P_ReadAmmoFromGlobalVar(local_0, 60, 89);
    SC_ggi(90);
    if (!local_0) {
        SC_PC_Get();
        SC_ggi(90);
        SC_P_SetAmmoInWeap(2, 90, local_2);
    } else {
        SC_ggi(91);
        SC_PC_Get();
        SC_ggi(SGI_ARRIVAL_HORNSTERSPECANI);
        SC_P_SetAmmoInWeap(SGI_ARRIVAL_UNLOCKED, SGI_ARRIVAL_HORNSTERSPECANI, local_2);
        return;
    }
    return;
}

void func_0821(void) {
    int local_1;  // Auto-generated

    c_Vector3 local_128;
    c_Vector3 local_44;
    int i;
    int idx;
    int j;
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

int func_0856(int param_0, int param_1, int param_2) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    int idx;
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

int func_0993(int param_0, int param_1) {
    c_Vector3 local_1;
    c_Vector3 local_128;
    c_Vector3 local_131;
    c_Vector3 local_44;
    int enum_pl;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    SC_ggi(SGI_DIFFICULTY);
    return 0;  // FIX (06-05): Synthesized return value
}

int func_3078(int param_0, int param_1, int param_2, int param_3, int param_4) {
    c_Vector3 local_1;
    c_Vector3 local_128;
    c_Vector3 local_44;
    int ai_props2;
    int local_;
    int tmp;
    int vec;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_35;
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

int func_4086(int param_0, int param_1, int param_2, int param_3, int param_4, int param_5) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    int i;
    int local_4;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp5;
    int tmp6;
    int tmp7;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_AI_props player_info3;
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
    SC_GetPls(&sphere, &player_info3.member_id, &tmp5);
    tmp6 = 0.0f;
    tmp7 = 0.0f;
    return 0;  // FIX (06-05): Synthesized return value
}

void func_4670(int param_0, int param_1) {
    dword EOP_e_canteen01;  // Auto-generated
    dword EOP_e_pistolcase01;  // Auto-generated

    c_Vector3 local_128;
    c_Vector3 local_44;
    int t4679_;
    int t4692_;
    int tmp;
    int tmp2;
    int tmp4;
    int tmp6;
    int tmp8;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    *"G\\Equipment\\US\\bes\\EOP_e_canteen01.BES" = tmp;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\lehke_vybaveni\\EOP_e_canteen01.eqp" = tmp2;
    *"G\\Equipment\\US\\bes\\EOP_e_pistolcase01.BES" = tmp4;
    *"G\\Equipment\\US\\eqp\\CUP_bangs\\lehke_vybaveni\\EOP_e_pistolcase01.eqp" = tmp6;
    tmp8 = 2;
    return;
}

void func_7108(int param_0, int param_1) {
    c_Vector3 local_128;
    c_Vector3 local_44;
    s_SC_P_AI_props local_0;
    s_SC_P_AI_props local_3;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_39;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    func_4670(param_0, param_0);
    return;
}

int ScriptMain(s_SC_L_info *info) {
    dword default_camo;  // Auto-generated
    dword easy_camo;  // Auto-generated
    dword param_1;  // Auto-generated

    c_Vector3 local_128;
    c_Vector3 local_44;
    dword local_0[16];
    dword local_39[16];
    int create;
    int data_;
    int local_65;
    int local_66;
    int tmp;
    int tmp1;
    int tmp11;
    int tmp13;
    int tmp14;
    int tmp15;
    int tmp17;
    int tmp19;
    int tmp21;
    int tmp23;
    int tmp24;
    int tmp25;
    int tmp27;
    int tmp28;
    int tmp29;
    int tmp3;
    int tmp30;
    int tmp32;
    int tmp34;
    int tmp36;
    int tmp38;
    int tmp40;
    int tmp42;
    int tmp44;
    int tmp46;
    int tmp48;
    int tmp5;
    int tmp50;
    int tmp51;
    int tmp52;
    int tmp54;
    int tmp55;
    int tmp56;
    int tmp57;
    int tmp58;
    int tmp59;
    int tmp60;
    int tmp7;
    int tmp9;
    s_SC_P_AI_props local_3;
    s_SC_P_AI_props pinfo;
    s_SC_P_getinfo local_2;
    s_SC_P_getinfo local_40;
    s_sphere local_36;
    s_sphere local_47;

    switch (gphase) {
    case 0:
        SC_ZeroMem(&create, 156);
        SC_ZeroMem(local_39, 80);
        create = 1;
        *tmp1 = 0.0f;
        *tmp3 = 0.0f;
        *tmp5 = 0.0f;
        if (func_0993()) {
            *"ini\\players\\default_camo.ini" = tmp9;
        } else {
            *"ini\\players\\easy_camo.ini" = tmp7;
            *tmp11 = 2500;
            *tmp15 = tmp14;
            func_0318(&create);
            *tmp17 = 0.0f;
            *tmp19 = 55;
            *tmp21 = SC_ggi(102);
            if (local_0->hear_distance_mult) {
                *tmp32 = 0.0f;
                *tmp34 = 140;
                *tmp36 = 0.0f;
                *tmp38 = 51;
                func_7108(local_39, &local_65);
                local_65 = tmp40;
                local_39 = tmp42;
                *tmp44 = 4;
                local_66 = tmp46;
                data_ = 1;
            } else {
                *tmp25 = 22;
            }
        }
        break;
    case 1:
        data_ = 2;
        SC_P_SetSpeachDist(tmp56, tmp58);
        func_0772();
        func_0756();
        SC_PC_EnablePronePosition(tmp59);
        SC_PC_EnableFlashLight(tmp60);
        break;
    case 255:
        *tmp30 = 0.0f;
        break;
    case 2:
        break;
    default:
        return TRUE;
    }
    param_1->field_24 = 0.1f;
    SC_P_IsReady(tmp51);
    if (!local_66) {
    } else {
        param_1->field_24 = 0.01f;
        return TRUE;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

