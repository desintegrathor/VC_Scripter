Skipping orphaned block 111 at address 1155 in function func_1146 - no predecessors (unreachable code)
Skipping orphaned block 112 at address 1159 in function func_1146 - no predecessors (unreachable code)
Skipping orphaned block 113 at address 1179 in function func_1146 - no predecessors (unreachable code)
Skipping orphaned block 624 at address 4419 in function func_4376 - no predecessors (unreachable code)
Skipping orphaned block 625 at address 4423 in function func_4376 - no predecessors (unreachable code)
Skipping orphaned block 626 at address 4438 in function func_4376 - no predecessors (unreachable code)
Skipping orphaned block 627 at address 4444 in function func_4376 - no predecessors (unreachable code)
Skipping orphaned block 628 at address 4445 in function func_4376 - no predecessors (unreachable code)
Skipping orphaned block 629 at address 4457 in function func_4376 - no predecessors (unreachable code)
Skipping orphaned block 630 at address 4458 in function func_4376 - no predecessors (unreachable code)
Skipping orphaned block 631 at address 4483 in function func_4376 - no predecessors (unreachable code)
Skipping orphaned block 665 at address 4953 in function func_4948 - no predecessors (unreachable code)
Skipping orphaned block 666 at address 4957 in function func_4948 - no predecessors (unreachable code)
Skipping orphaned block 667 at address 4966 in function func_4948 - no predecessors (unreachable code)
Skipping orphaned block 735 at address 6199 in function func_6196 - no predecessors (unreachable code)
Skipping orphaned block 816 at address 6810 in function func_6804 - no predecessors (unreachable code)
Skipping orphaned block 817 at address 6814 in function func_6804 - no predecessors (unreachable code)
Skipping orphaned block 818 at address 6828 in function func_6804 - no predecessors (unreachable code)
Skipping orphaned block 819 at address 6829 in function func_6804 - no predecessors (unreachable code)
Skipping orphaned block 820 at address 6849 in function func_6804 - no predecessors (unreachable code)
Skipping orphaned block 825 at address 6879 in function func_6873 - no predecessors (unreachable code)
Skipping orphaned block 826 at address 6883 in function func_6873 - no predecessors (unreachable code)
Skipping orphaned block 827 at address 6946 in function func_6873 - no predecessors (unreachable code)
Skipping orphaned block 829 at address 6987 in function func_6984 - no predecessors (unreachable code)
Skipping orphaned block 831 at address 6992 in function func_6984 - no predecessors (unreachable code)
Skipping orphaned block 833 at address 7016 in function func_6984 - no predecessors (unreachable code)
Skipping orphaned block 835 at address 7021 in function func_6984 - no predecessors (unreachable code)
Skipping orphaned block 837 at address 7026 in function func_6984 - no predecessors (unreachable code)
Skipping orphaned block 839 at address 7031 in function func_6984 - no predecessors (unreachable code)
Skipping orphaned block 841 at address 7036 in function func_6984 - no predecessors (unreachable code)
Skipping orphaned block 845 at address 7062 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 850 at address 7131 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 859 at address 7257 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 861 at address 7286 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 863 at address 7316 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 865 at address 7426 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 867 at address 7455 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 869 at address 7484 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 871 at address 7518 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 873 at address 7563 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 877 at address 7595 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 879 at address 7658 in function func_7043 - no predecessors (unreachable code)
Skipping orphaned block 881 at address 7680 in function func_7043 - no predecessors (unreachable code)
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

    return FALSE;
}

int func_0291(int param_0) {
    c_Vector3 tmp;
    int tmp1;
    int tmp2;

    tmp = frnd(param_0);
    if (!tmp1) {
        tmp = tmp2;
    } else {
        return tmp;
    }
    return;
}

int func_0354(int param_0, int param_1, int param_2) {
    int idx;  // Auto-generated

    if (!param_2) {
        SC_P_ScriptMessage(param_2, param_0, idx);
        return FALSE;
    } else {
        SC_Log(3, "Message %d %d to unexisted player!", param_0, param_0);
        return FALSE;
    }
    return;
}

int func_0371(int param_0, int param_1) {
    int j;  // Auto-generated
    int local_0;  // Auto-generated
    int local_1;  // Auto-generated

    SC_P_GetBySideGroupMember(gVar1, param_2, param_0);
    SC_P_Ai_GetSureEnemies(j);
    if (!local_0) {
        return FALSE;
    } else {
        SC_P_GetBySideGroupMember(1, param_2, param_0);
        SC_P_Ai_GetDanger(local_1);
        return FALSE;
        return FALSE;
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
}

int func_1054(void) {
    int i;  // Auto-generated

    SC_PC_Get();
    SC_P_WriteHealthToGlobalVar(i, 95);
    return FALSE;
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

    SC_PC_GetIntel(&i);
    tmp = 0;
    return;
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

int func_3368(int param_0, int param_1) {
    int idx;  // Auto-generated

    c_Vector3 local_;
    int tmp;

    local_ = SC_NOD_Get(0, param_0);
    if (!tmp) {
        SC_NOD_GetWorldPos(local_, idx);
    } else {
        return TRUE;
    }
    return;
}

int func_4180(int param_0, int param_1, int param_2) {
    int local_3;  // Auto-generated

    SC_P_GetPos(param_3, &vec);
    SC_IsNear3D(&vec, param_2, param_0);
    return local_3;
}

int func_4376(int param_0, int param_1, int param_2) {
    int local_4;  // Auto-generated
    int player_info;  // Auto-generated

    c_Vector3 tmp2;
    c_Vector3 tmp5;
    c_Vector3 tmp6;
    c_Vector3 tmp7;
    int tmp;
    int tmp1;
    int tmp3;

    SC_P_GetInfo(param_2, &player_info);
    tmp2 = tmp1;
    SC_P_GetPos(param_2, &sphere);
    *tmp3 = 1000.0f;
    tmp5 = 32;
    SC_GetPls(&sphere, &local_4, &tmp5);
    tmp6 = 0;
    tmp7 = 0;
    return;
}

int func_4575(int param_0, int param_1) {
    c_Vector3 tmp;

    SC_P_GetPos(param_2, &vec);
    tmp = SC_2VectorsDist(param_0, &vec);
    return tmp;
}

int func_4948(int param_0) {
    c_Vector3 tmp;

    tmp = 0;
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

int func_6196(int param_0) {
    s_sphere tmp;

    goto block_736; // @6203
    return TRUE;
}

int func_6259(void) {
    int j;  // Auto-generated

    int tmp;

    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_GetPeaceMode(j);
    if (!tmp) {
        SC_Ai_SetPeaceMode(0, 0, 0);
        SC_Ai_PointStopDanger(0, 0);
    } else {
        return FALSE;
    }
    return;
}

int func_6804(void) {
    c_Vector3 tmp;

    tmp = 1;
    return;
}

int func_6873(void) {
    c_Vector3 tmp;

    tmp = 0;
    return;
}

int func_6984(int param_0) {
    c_Vector3 tmp;
    int t7001_;
    int t7010_;
    int tmp1;
    int tmp2;
    int tmp4;
    int tmp5;

    goto block_830; // @6991
    goto block_832; // @6996
    *tmp2 = 0;
    *tmp5 = 1;
    goto block_834; // @7020
    goto block_836; // @7025
    goto block_838; // @7030
    goto block_840; // @7035
    goto block_842; // @7040
    goto block_843; // @7041
    return FALSE;
}

int func_7043(int param_0) {
    c_Vector3 local_;
    c_Vector3 local_1;
    c_Vector3 local_5;
    c_Vector3 param_;
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
    int tmp10;
    int tmp100;
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
    int tmp114;
    int tmp115;
    int tmp116;
    int tmp117;
    int tmp119;
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
    int tmp132;
    int tmp133;
    int tmp14;
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
    int tmp36;
    int tmp37;
    int tmp38;
    int tmp39;
    int tmp4;
    int tmp40;
    int tmp42;
    int tmp43;
    int tmp44;
    int tmp46;
    int tmp47;
    int tmp48;
    int tmp49;
    int tmp5;
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
    int tmp84;
    int tmp85;
    int tmp86;
    int tmp87;
    int tmp89;
    int tmp90;
    int tmp91;
    int tmp92;
    int tmp94;
    int tmp95;
    int tmp96;
    int tmp97;
    int tmp98;
    int tmp99;

    SC_PC_Get();
    SC_P_GetWillTalk(local_5);
    local_ = tmp;
    goto block_846; // @7066
    if (!tmp4) {
        SC_PC_Get();
        SC_P_Speech2(local_5, tmp16, &local_);
        local_ = tmp5;
        *tmp8 = -100;
        *tmp14 = tmp12;
        rand();
        SC_PC_Get();
        SC_P_Speech2(local_5, tmp31, &local_);
        local_ = tmp22;
        SC_PC_Get();
        SC_P_Speech2(local_5, 911, &local_);
        local_ = tmp23;
        SC_PC_Get();
        func_4575(tmp25);
        SC_PC_Get();
        func_4575(tmp32, tmp26);
        SC_PC_Get();
        rand();
        SC_P_Speech2(local_5, tmp29, &local_);
        local_ = tmp30;
        *tmp34 = -100;
        *tmp40 = tmp38;
        SC_PC_Get();
        SC_P_Speech2(local_5, tmp46, &local_);
        local_ = tmp42;
        *tmp44 = -100;
        SC_PC_Get();
        SC_P_SpeechMes2(local_5, tmp51, &local_, tmp52);
        local_ = tmp47;
        *tmp49 = -100;
        SC_P_GetBySideGroupMember(tmp61, tmp62, tmp63);
        SC_P_GetPos(local_5, &local_1);
        SC_SND_PlaySound3D(tmp64, &local_1);
        local_ = tmp53;
        SC_PC_Get();
        SC_P_SpeechMes2(local_5, tmp65, &local_, tmp66);
        local_ = tmp54;
        local_ = 0.5f;
        SC_P_GetBySideGroupMember(tmp67, tmp68, tmp69);
        SC_P_Speech2(local_5, tmp70, &local_);
        local_ = tmp55;
        SC_P_GetBySideGroupMember(tmp71, tmp72, tmp73);
        SC_P_Speech2(local_5, tmp74, &local_);
        local_ = tmp56;
        SC_P_GetBySideGroupMember(tmp75, tmp76, tmp77);
        SC_P_SpeechMes2(local_5, tmp78, &local_, tmp79);
        local_ = tmp57;
        *tmp59 = -100;
        SC_PC_Get();
        SC_P_Speech2(local_5, tmp84, &local_);
        local_ = tmp80;
        *tmp82 = -100;
        SC_PC_Get();
        SC_P_Speech2(local_5, tmp89, &local_);
        local_ = tmp85;
        *tmp87 = -100;
        SC_P_GetBySideGroupMember(tmp94, tmp95, tmp96);
        SC_P_SpeechMes2(local_5, tmp97, &local_, tmp98);
        local_ = tmp90;
        *tmp92 = -100;
        *tmp100 = -100;
        SC_P_GetBySideGroupMember(tmp102, tmp103, tmp104);
        SC_P_Ai_SetMode(local_5, tmp105);
        SC_GetWp(&tmp106, &local_1);
        SC_P_GetBySideGroupMember(tmp107, tmp108, tmp109);
        SC_P_Ai_Go(local_5, &local_1);
        SC_PC_Get();
        SC_P_SpeechMes2(local_5, 932, &local_, 15);
        local_ = tmp110;
        *tmp112 = -100;
        SC_P_GetBySideGroupMember(tmp119, tmp120, tmp121);
        SC_P_GetPos(local_5, &local_1);
        SC_SND_PlaySound3D(tmp122, &local_1);
        SC_P_GetBySideGroupMember(tmp123, tmp124, tmp125);
        SC_P_GetPos(local_5, &local_1);
        SC_SND_PlaySound3D(tmp126, &local_1);
        SC_PC_Get();
        SC_P_Speech2(local_5, tmp127, &local_);
        local_ = tmp114;
        tmp115 = 1;
        *tmp117 = -100;
        SC_AGS_Set(tmp131);
        *tmp129 = -100;
        func_1223();
        *tmp133 = -100;
        return local_5;
    } else {
        SC_PC_Get();
        SC_P_Speech2(local_5, 904, &local_);
        local_ = tmp6;
    }
    return;
}Skipping orphaned block 885 at address 7702 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 886 at address 7706 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 887 at address 7716 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 888 at address 7743 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 889 at address 7746 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 890 at address 7755 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 891 at address 7759 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 892 at address 7763 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 893 at address 7773 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 894 at address 7792 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 895 at address 7793 in function func_7697 - no predecessors (unreachable code)
Skipping orphaned block 899 at address 7813 in function func_7807 - no predecessors (unreachable code)
Skipping orphaned block 906 at address 7864 in function func_7807 - no predecessors (unreachable code)
Skipping orphaned block 913 at address 7946 in function func_7807 - no predecessors (unreachable code)
Skipping orphaned block 917 at address 7997 in function func_7807 - no predecessors (unreachable code)
Skipping orphaned block 924 at address 8112 in function func_7807 - no predecessors (unreachable code)
Skipping orphaned block 957 at address 8522 in function func_7807 - no predecessors (unreachable code)
Skipping orphaned block 959 at address 8528 in function func_7807 - no predecessors (unreachable code)
Skipping orphaned block 961 at address 8654 in function func_7807 - no predecessors (unreachable code)
Skipping orphaned block 963 at address 8661 in function func_7807 - no predecessors (unreachable code)
Skipping orphaned block 965 at address 8666 in function func_7807 - no predecessors (unreachable code)
Skipping orphaned block 969 at address 8736 in function func_7807 - no predecessors (unreachable code)


int func_7697(float param_0, int param_1) {
    c_Vector3 tmp;

    tmp = 0;
    return;
}

int func_7807(float param_0) {
    int local_5;  // Auto-generated

    c_Vector3 data_1763;
    c_Vector3 local_2;
    c_Vector3 local_6;
    c_Vector3 local_9;
    c_Vector3 tmp114;
    c_Vector3 tmp2;
    c_Vector3 tmp21;
    int data_;
    int data_1757;
    int data_1758;
    int local_;
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
    int tmp125;
    int tmp126;
    int tmp127;
    int tmp128;
    int tmp129;
    int tmp13;
    int tmp130;
    int tmp131;
    int tmp132;
    int tmp133;
    int tmp134;
    int tmp135;
    int tmp136;
    int tmp14;
    int tmp15;
    int tmp16;
    int tmp17;
    int tmp18;
    int tmp19;
    int tmp20;
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

    goto block_900; // @7817
    SC_P_GetBySideGroupMember(tmp5, tmp6, tmp7);
    SC_P_IsReady(local_);
    if (!local_6) {
        func_0371(tmp3, tmp4);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Speech2(local_6, 926, &tmp2);
        tmp2 = tmp1;
        data_ = 1;
    }
    goto block_907; // @7868
    SC_P_GetBySideGroupMember(tmp9, tmp10, tmp11);
    SC_P_IsReady(local_);
    if (!local_6) {
        SC_P_GetBySideGroupMember(tmp12, tmp13, tmp14);
        func_4180(&tmp15, tmp16);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_BATTLE);
        data_ = 2;
        SC_P_GetBySideGroupMember(tmp18, tmp19, tmp20);
        SC_P_Ai_GetShooting(local_, &tmp21);
        SC_PC_Get();
        tmp2 = SC_P_GetWillTalk(local_);
        SC_PC_Get();
        SC_P_Speech2(local_6, 929, &tmp2);
        tmp2 = tmp17;
        data_ = 3;
        SC_P_GetBySideGroupMember(tmp28, tmp29, tmp30);
        SC_P_IsReady(local_);
        SC_PC_Get();
        tmp2 = SC_P_GetWillTalk(local_);
        SC_PC_Get();
        SC_P_Speech2(local_6, 927, &tmp2);
        tmp2 = tmp22;
        data_ = 100;
        tmp24 = tmp23;
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_Go(local_6, &vcrunpoint2);
        SC_PC_Get();
        SC_P_GetWillTalk(local_);
        tmp2 = tmp26;
        SC_PC_Get();
        SC_P_Speech2(local_6, 930, &tmp2);
        tmp2 = tmp27;
        data_ = 4;
        SC_P_GetBySideGroupMember(tmp31, tmp32, tmp33);
        func_4180(&tmp15, tmp34);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(local_6, SC_P_AI_MODE_BATTLE);
        data_ = 5;
        SC_P_GetBySideGroupMember(tmp38, tmp39, tmp40);
        SC_P_IsReady(local_6);
        SC_P_GetBySideGroupMember(tmp41, tmp42, tmp43);
        SC_P_IsReady(local_6);
        tmp35 = 1;
        SC_PC_Get();
        SC_P_GetWillTalk(local_6);
        tmp2 = tmp36;
        SC_PC_Get();
        SC_P_Speech2(local_5, 928, &tmp2);
        tmp2 = tmp37;
        SC_P_GetBySideGroupMember(tmp47, tmp48, tmp49);
        SC_P_IsReady(local_6);
        SC_P_GetBySideGroupMember(tmp50, tmp51, tmp52);
        SC_P_IsReady(local_6);
        SC_P_GetBySideGroupMember(tmp53, tmp54, tmp55);
        SC_P_IsReady(local_6);
        tmp44 = 1;
        SC_PC_Get();
        SC_P_GetWillTalk(local_6);
        tmp2 = tmp45;
        SC_PC_Get();
        SC_P_Speech2(local_5, 931, &tmp2);
        tmp2 = tmp46;
        func_0371(tmp60, tmp61);
        SC_P_GetBySideGroupMember(1, 1, 0);
        rand();
        SC_P_Speech2(local_5, tmp58, &tmp2);
        tmp2 = tmp59;
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        data_1757 = 100;
        func_0371(tmp66, tmp67);
        SC_P_GetBySideGroupMember(1, 1, 1);
        rand();
        SC_P_Speech2(local_5, tmp64, &tmp2);
        tmp2 = tmp65;
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_SetMode(local_5, SGI_INTELCOUNT);
        data_1757 = 100;
        func_0371(tmp72, tmp73);
        SC_P_GetBySideGroupMember(1, 1, 2);
        rand();
        SC_P_Speech2(local_5, tmp70, &tmp2);
        tmp2 = tmp71;
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_SetMode(local_5, SC_P_AI_MODE_BATTLE);
        data_1757 = 100;
        SC_P_GetBySideGroupMember(tmp77, tmp78, tmp79);
        SC_P_Ai_SetMode(local_6, tmp80);
        SC_P_GetBySideGroupMember(tmp81, tmp82, tmp83);
        SC_P_Ai_SetMode(local_6, tmp84);
        SC_P_GetBySideGroupMember(tmp85, tmp86, tmp87);
        SC_P_Ai_SetMode(local_6, tmp88);
        SC_P_GetBySideGroupMember(tmp89, tmp90, tmp91);
        SC_P_Ai_Stop(local_6);
        SC_P_GetBySideGroupMember(tmp92, tmp93, tmp94);
        SC_P_Ai_Stop(local_6);
        SC_P_GetBySideGroupMember(tmp95, tmp96, tmp97);
        SC_P_Ai_Stop(local_6);
        frnd(20.0f);
        tmp75 = tmp74;
        rand();
        data_1758 = tmp76;
        SC_P_GetBySideGroupMember(tmp99, tmp100, data_1758);
        SC_P_GetPos(local_6, &local_2);
        SC_P_GetBySideGroupMember(tmp101, tmp102, tmp103);
        SC_P_Ai_Go(local_6, &local_2);
        SC_P_GetBySideGroupMember(tmp104, tmp105, tmp106);
        SC_P_GetPos(local_6, &data_1763);
        data_1757 = 2;
        SC_P_GetBySideGroupMember(tmp111, tmp112, tmp113);
        SC_P_GetBySideGroupMember(tmp115, tmp116, data_1758);
        SC_P_GetDistance(data_1758, local_9);
        SC_P_GetBySideGroupMember(1, 1, 2);
        rand();
        SC_P_Speech2(local_, tmp109, &tmp2);
        tmp2 = tmp110;
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_Go(local_, &data_1763);
        data_1758 = 2;
        SC_P_GetBySideGroupMember(tmp118, tmp119, tmp120);
        func_4180(&data_1763, tmp121);
        rand();
        data_1758 = tmp117;
        SC_P_GetBySideGroupMember(1, 1, data_1758);
        SC_P_GetPos(local_, &local_2);
        SC_P_GetBySideGroupMember(1, 1, 2);
        SC_P_Ai_Go(local_, &local_2);
        tmp75 = tmp122;
        frnd(20.0f);
        tmp75 = tmp124;
        tmp2 = 0;
        rand();
        SC_P_GetBySideGroupMember(1, 1, tmp125);
        rand();
        SC_P_Speech2(local_6, tmp127, &tmp2);
        tmp2 = tmp128;
        tmp130 = tmp129;
        frnd(5.0f);
        tmp130 = tmp132;
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetPos(local_6, &local_2);
        SC_SND_PlaySound3D(10419, &local_2);
        tmp134 = tmp133;
        frnd(5.0f);
        tmp134 = tmp136;
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_GetPos(local_6, &local_2);
        SC_SND_PlaySound3D(10419, &local_2);
        return tmp121;
    } else {
        SC_PC_Get();
        tmp2 = SC_P_GetWillTalk(local_);
        SC_PC_Get();
        SC_P_Speech2(local_6, 927, &tmp2);
        tmp2 = tmp8;
        data_ = 100;
    }
    return;
}Skipping orphaned block 998 at address 9070 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1000 at address 9077 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1002 at address 9084 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1004 at address 9091 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1006 at address 9100 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1009 at address 9111 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1011 at address 9118 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1013 at address 9351 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1015 at address 9412 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1018 at address 9439 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1020 at address 9466 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1022 at address 9573 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1025 at address 9682 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1027 at address 9691 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1032 at address 9747 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1037 at address 9806 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1042 at address 9865 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1044 at address 9874 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1046 at address 9895 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1048 at address 9969 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1050 at address 9994 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1052 at address 10003 in function ScriptMain - no predecessors (unreachable code)
Skipping orphaned block 1055 at address 10012 in function ScriptMain - no predecessors (unreachable code)


int func_8919(void) {
    dword openablecrate;  // Auto-generated
    dword past;  // Auto-generated
    dword poklop;  // Auto-generated

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
    int local_1;  // Auto-generated
    int local_2;  // Auto-generated
    int m;  // Auto-generated

    c_Vector3 tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;

    SC_PC_Get();
    tmp = SC_P_GetWillTalk(m);
    if (!tmp4) {
    } else {
        SC_NOD_GetName(tmp2);
        SC_StringSame(local_2, "grenadebedna");
        SC_PC_Get();
        SC_P_Speech2(local_1, 923, &tmp);
        tmp = tmp3;
        tmp4 = 1;
        return &tmp4;
    }
    return;
}

int ScriptMain(s_SC_L_info *info) {
    dword param_1;  // Auto-generated

    c_Vector3 local_;
    c_Vector3 local_9;
    c_Vector3 tmp38;
    dword local_22[16];
    dword local_4[16];
    int initside;
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
    int tmp125;
    int tmp126;
    int tmp127;
    int tmp128;
    int tmp129;
    int tmp130;
    int tmp131;
    int tmp132;
    int tmp133;
    int tmp134;
    int tmp135;
    int tmp136;
    int tmp137;
    int tmp138;
    int tmp139;
    int tmp14;
    int tmp140;
    int tmp142;
    int tmp144;
    int tmp146;
    int tmp147;
    int tmp148;
    int tmp149;
    int tmp150;
    int tmp151;
    int tmp152;
    int tmp153;
    int tmp154;
    int tmp156;
    int tmp158;
    int tmp16;
    int tmp160;
    int tmp161;
    int tmp162;
    int tmp163;
    int tmp164;
    int tmp165;
    int tmp166;
    int tmp167;
    int tmp168;
    int tmp170;
    int tmp172;
    int tmp174;
    int tmp175;
    int tmp176;
    int tmp177;
    int tmp178;
    int tmp179;
    int tmp18;
    int tmp180;
    int tmp181;
    int tmp182;
    int tmp183;
    int tmp184;
    int tmp185;
    int tmp186;
    int tmp187;
    int tmp188;
    int tmp189;
    int tmp190;
    int tmp191;
    int tmp192;
    int tmp193;
    int tmp194;
    int tmp195;
    int tmp196;
    int tmp197;
    int tmp198;
    int tmp199;
    int tmp2;
    int tmp20;
    int tmp200;
    int tmp201;
    int tmp202;
    int tmp203;
    int tmp205;
    int tmp206;
    int tmp207;
    int tmp208;
    int tmp209;
    int tmp210;
    int tmp211;
    int tmp213;
    int tmp22;
    int tmp24;
    int tmp26;
    int tmp28;
    int tmp3;
    int tmp30;
    int tmp32;
    int tmp34;
    int tmp36;
    int tmp37;
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
    s_sphere param_;

    param_1->field_20 = 0.20000000298023224f;
    goto block_999; // @9074
    func_8919();
    goto block_1001; // @9081
    func_8933();
    goto block_1003; // @9088
    func_8932();
    goto block_1005; // @9095
    goto block_1007; // @9104
    func_8934(param_);
    goto block_1008; // @9108
    goto block_1010; // @9115
    goto block_1012; // @9122
    SC_sgi(tmp36, tmp37);
    SC_ZeroMem(&tmp38, tmp39);
    SC_ZeroMem(&tmp40, tmp41);
    func_5197();
    SC_DeathCamera_Enable(tmp42);
    SC_RadioSetDist(tmp43);
    SC_ZeroMem(&initside, tmp44);
    initside = 32;
    *tmp8 = 8;
    SC_InitSide(tmp45, &initside);
    SC_ZeroMem(&initside, tmp46);
    initside = 64;
    *tmp10 = 16;
    SC_InitSide(tmp47, &initside);
    SC_ZeroMem(&initside, tmp48);
    initside = 0;
    *tmp12 = 0;
    *tmp14 = 4;
    *tmp16 = 30.0f;
    SC_InitSideGroup(&initside);
    SC_ZeroMem(&initside, tmp49);
    initside = 1;
    *tmp18 = 0;
    *tmp20 = 9;
    SC_InitSideGroup(&initside);
    SC_ZeroMem(&initside, tmp50);
    initside = 1;
    *tmp22 = 1;
    *tmp24 = 16;
    SC_InitSideGroup(&initside);
    SC_ZeroMem(&initside, tmp51);
    initside = 1;
    *tmp26 = 2;
    *tmp28 = 16;
    SC_InitSideGroup(&initside);
    SC_ZeroMem(&initside, tmp52);
    initside = 1;
    *tmp30 = 3;
    *tmp32 = 9;
    SC_InitSideGroup(&initside);
    SC_Ai_SetShootOnHeardEnemyColTest(tmp53);
    SC_Ai_SetGroupEnemyUpdate(tmp54, tmp55, tmp56);
    SC_Ai_SetGroupEnemyUpdate(tmp57, tmp58, tmp59);
    SC_Ai_SetGroupEnemyUpdate(tmp60, tmp61, tmp62);
    SC_Ai_SetGroupEnemyUpdate(tmp63, tmp64, tmp65);
    tmp7 = 1;
    SC_sgi(tmp66, tmp67);
    SC_Log(tmp68, &tmp69, tmp70);
    SC_Osi(&tmp72, tmp73);
    SC_SetCommandMenu(tmp75);
    param_1->field_20 = 0.5f;
    goto block_1014; // @9355
    local_ = 1.0f;
    SC_AGS_Set(tmp77);
    SC_PC_Get();
    SC_P_SpeechMes2(initside, tmp78, &local_, tmp79);
    local_ = tmp76;
    func_4948(tmp80);
    func_4948(tmp81);
    func_4948(tmp82);
    func_6873();
    tmp7 = 2;
    SC_sgi(tmp83, tmp84);
    SC_Log(tmp85, &tmp86, tmp87);
    SC_Osi(&tmp89, tmp90);
    goto block_1016; // @9416
    SC_PC_GetPos(&local_9);
    func_7697(&local_9, tmp93);
    func_7807(&local_9, tmp95);
    goto block_1017; // @9436
    goto block_1019; // @9443
    SC_PC_Get();
    local_ = SC_P_GetWillTalk(initside);
    SC_PC_EnableMovement(tmp98);
    SC_PC_EnableRadioBreak(tmp99);
    goto block_1021; // @9470
    SC_RadioBatch_Begin();
    SC_PC_Get();
    SC_P_Speech2(initside, tmp109, &local_);
    local_ = tmp100;
    func_0291(local_, 0.30000001192092896f);
    local_ = tmp101;
    SC_SpeechRadio2(tmp110, &local_);
    func_0291(local_, 0.10000000149011612f, 0.20000000298023224f);
    local_ = tmp103;
    SC_PC_Get();
    SC_P_Speech2(initside, tmp111, &local_);
    local_ = tmp104;
    func_0291(local_, 0.30000001192092896f);
    local_ = tmp105;
    SC_SpeechRadio2(tmp112, &local_);
    func_0291(local_, 0.10000000149011612f, 0.20000000298023224f);
    local_ = tmp107;
    SC_PC_Get();
    SC_P_SpeechMes2(initside, tmp113, &local_, tmp114);
    local_ = tmp108;
    SC_RadioBatch_End();
    goto block_1023; // @9577
    SC_RadioBatch_Begin();
    SC_PC_Get();
    SC_P_Speech2(initside, tmp124, &local_);
    local_ = tmp115;
    func_0291(local_, 0.30000001192092896f);
    local_ = tmp116;
    SC_SpeechRadio2(tmp125, &local_);
    func_0291(local_, 0.10000000149011612f, 0.20000000298023224f);
    local_ = tmp118;
    SC_PC_Get();
    SC_P_Speech2(initside, tmp126, &local_);
    local_ = tmp119;
    func_0291(local_, 0.30000001192092896f);
    local_ = tmp120;
    SC_SpeechRadio2(tmp127, &local_);
    func_0291(local_, 0.10000000149011612f, 0.20000000298023224f);
    local_ = tmp122;
    SC_PC_Get();
    SC_P_SpeechMes2(initside, tmp128, &local_, tmp129);
    local_ = tmp123;
    SC_RadioBatch_End();
    goto block_1024; // @9679
    goto block_1026; // @9686
    goto block_1028; // @9695
    if (!tmp136) {
        save[tmp152] = 1;
        SC_PC_EnableMovement(1);
        *tmp156 = 0;
        initside = 9112;
        *tmp158 = 9113;
        SC_MissionSave(&initside);
        SC_Log(3, "Saving game id %d", 9112);
        SC_Osi("Saving game id %d", 9112);
        save[tmp166] = 1;
        SC_PC_EnableMovement(1);
        *tmp170 = 0;
        initside = 9114;
        *tmp172 = 9115;
        SC_MissionSave(&initside);
        SC_Log(3, "Saving game id %d", 9114);
        SC_Osi("Saving game id %d", 9114);
        SC_Radio_Enable(tmp174);
        SC_P_GetBySideGroupMember(tmp175, tmp176, tmp177);
        SC_P_GetPos(initside, &local_9);
        SC_SND_PlaySound3D(tmp178, &local_9);
        SC_P_GetBySideGroupMember(tmp179, tmp180, tmp181);
        SC_P_GetPos(initside, &local_9);
        SC_SND_PlaySound3D(tmp182, &local_9);
        SC_P_GetBySideGroupMember(tmp183, tmp184, tmp185);
        SC_P_GetPos(initside, &local_9);
        SC_SND_PlaySound3D(tmp186, &local_9);
        SC_GetWp(&tmp187, &local_9);
        SC_P_GetBySideGroupMember(tmp188, tmp189, tmp190);
        SC_P_SetPos(initside, &local_9);
        SC_GetWp(&tmp191, &local_9);
        SC_P_GetBySideGroupMember(tmp192, tmp193, tmp194);
        SC_P_SetPos(initside, &local_9);
        SC_GetWp(&tmp195, &local_9);
        SC_P_GetBySideGroupMember(tmp196, tmp197, tmp198);
        SC_P_SetPos(initside, &local_9);
        SC_Radio_Enable(tmp199);
        func_1223();
        param_1->field_12 = 0;
        tmp211 = tmp209;
        param_1->field_12 = 1;
        return TRUE;
    } else {
        save[tmp138] = 1;
        *tmp142 = 0;
        initside = 9110;
        *tmp144 = 9111;
        SC_MissionSave(&initside);
        SC_Log(3, "Saving game id %d", 9110);
        SC_Osi("Saving game id %d", 9110);
    }
    return;
}

