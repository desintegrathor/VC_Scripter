// Structured decompilation of decompiler_source_tests/test3/LEVEL.SCR
// Functions: 10

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Global variables
dword gVar;
int gphase;
int g_dialog;
dword g_will_group[4];
int g_dochange;
int g_final_enter_timer;
dword g_will_pos[12];
dword g_vill_visited[4];
int g_pilot_phase;
int g_pilot_timer;
dword g_pilot_vill_nr;
int g_showinfo_timer;
int g_trashes_enabled;
dword gShot_pos[3];
int gEndTimer;
int gPilotCommTime;
dword g_save[2];
dword g_music[2];
int gStartMusicTime;

int _init(s_SC_L_info *info) {
    c_Vector3 local_11;
    int j;
    int side;
    int side2;
    int side3;
    int side4;
    int side5;
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
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_MP_EnumPlayers local_0;

    return 0;  // FIX (06-05): Synthesized return value
}

int func_0292(void) {
    c_Vector3 local_11;
    c_Vector3 vec;
    dword local_2[16];
    int tmp;
    int tmp2;
    s_SC_MP_EnumPlayers j;
    s_SC_MP_EnumPlayers local_0;

    SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0.0f);
    SC_ZeroMem(&vec, 12);
    *tmp = -20000.0f;
    tmp2 = 0.0f;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0355(void) {
    c_Vector3 local_11;
    int k;
    int tmp;
    s_SC_MP_EnumPlayers local_0;

    tmp = 0.0f;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0448(int param_0, int param_1) {
    c_Vector3 local_11;
    int j;
    s_SC_MP_EnumPlayers local_0;

    SC_P_GetBySideGroupMember(2, 0.0f, 1);
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0511(int param_0, int param_1) {
    c_Vector3 local_11;
    dword local_3[16];
    int idx;
    int tmp;
    s_SC_MP_EnumPlayers local_0;
    s_SC_MP_EnumPlayers vec;

    SC_P_GetPos(param_0, &vec);
    SC_ZeroMem(local_3, 8);
    tmp = 0.0f;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0612(float param_0) {
    c_Vector3 vec;
    int data_;
    int j;
    int local_;
    int local_10;
    int local_11;
    int local_12;
    int local_13;
    int local_14;
    int local_2;
    int local_4;
    int local_7;
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
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_MP_EnumPlayers local_0;

    switch (param_1) {
    case 0:
        SC_PC_GetPos(&local_4);
        tmp1 = 0.0f;
        break;
    case 1:
        tmp4 = tmp3;
        if (tmp5) {
            data_ = 2;
            SC_PC_Get();
            func_0511(local_, &local_2);
            rand();
            tmp10 = tmp9;
            func_0448();
            SC_P_ScriptMessage(local_, 0.0f, tmp10);
            frnd(30.0f);
            tmp4 = tmp11;
            rand();
            SC_SpeechRadio2(tmp15, 0.0f);
            func_0448();
            SC_HUD_RadarShowPlayer(local_, -16711936);
        }
        return tmp20;
    case 2:
        tmp4 = tmp17;
        if (tmp18) {
            data_ = 1;
            frnd(10.0f);
            tmp4 = tmp19;
            tmp10 = 255;
            func_0448();
            SC_P_ScriptMessage(local_, 0.0f, tmp10);
            SC_HUD_RadarShowPlayer(0.0f, 0.0f);
        } else {
            SC_PC_GetPos(&local_4);
            func_0448();
            SC_P_GetPos(local_, &local_7);
            if (SC_IsNear2D(&local_4, &local_7, tmp20)) {
                data_ = 4;
                tmp4 = 0.0f;
                SC_SetSideAlly(1, 2, -1.0f);
                SC_sgi(SGI_LEVELPHASE, 2);
            }
        }
        break;
    case 4:
        SC_ggi(tmp28);
        if (tmp22) {
        } else {
            tmp4 = tmp23;
            if (tmp24) {
                tmp4 = 1.5f;
                func_0448();
                SC_PC_Get();
                local_10 = SC_P_GetDistance(local_13, tmp27);
                if (tmp25) {
                    SC_PC_GetPos(&local_7);
                    func_0448();
                    SC_P_Ai_Go(local_, &local_7);
                } else {
                    if (tmp26) {
                        func_0448();
                        SC_P_Ai_Stop(local_);
                    }
                }
            }
        }
        break;
    default:
    }
    return 0;  // FIX (06-05): Synthesized return value
}

void func_0985(int param_0) {
    c_Vector3 local_11;
    s_SC_MP_EnumPlayers local_0;

    SC_P_Ai_SetMoveMode(param_0, SC_P_AI_MOVEMODE_SNEAK);
    SC_P_Ai_SetMovePos(param_0, 0.0f);
    return;
}

int func_0994(int param_0) {
    c_Vector3 local_11;
    int j;
    int k;
    int local_;
    int tmp;
    s_SC_MP_EnumPlayers local_0;

    tmp = param_0;
    local_ = SC_NOD_Get(0, "maj_uh-1d_vreck");
    if (!local_) {
        SC_DUMMY_Set_DoNotRenHier2(local_, 1);
    } else {
        return TRUE;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_1021(void) {
    c_Vector3 local_11;
    int local_;
    int local_256;
    int local_257;
    int tmp;
    s_SC_MP_EnumPlayers enum_pl[64];

    local_ = 64;
    SC_sgi(SGI_DEBR_01, 0.0f);
    SC_sgi(SGI_REWARD_PILOT, 1);
    SC_MP_EnumPlayers(enum_pl, &local_, 1);
    if (!local_257) {
        SC_sgi(SGI_DEBR_01, -1);
        SC_sgi(SGI_REWARD_PILOT, 0.0f);
    } else {
        return 257;
    }
    if (!tmp) goto block_91; // @1056
    return 0;  // FIX (06-05): Synthesized return value
}

int ScriptMain(s_SC_L_info *info) {
    int c;  // Auto-generated
    dword heli1;  // Auto-generated
    dword heli2;  // Auto-generated
    dword heli3;  // Auto-generated
    dword ivq_kopac;  // Auto-generated
    int local_89;  // Auto-generated
    dword map_ricefield;  // Auto-generated
    dword param_1;  // Auto-generated
    int ricefield;  // Auto-generated

    c_Vector3 local_11;
    c_Vector3 vec;
    float j;
    int data_;
    int data_225;
    int data_266;
    int i;
    int idx;
    int initgroup;
    int initside;
    int k;
    int local_;
    int local_17;
    int local_2;
    int local_22;
    int local_23;
    int local_24;
    int local_25;
    int local_26;
    int local_27;
    int local_4;
    int local_63;
    int local_67;
    int local_80;
    int local_83;
    int local_87;
    int local_88;
    int local_90;
    int local_91;
    int m;
    int missionsave;
    int n;
    int player_info;
    int plinfo;
    int t2409_;
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
    int tmp13;
    int tmp131;
    int tmp133;
    int tmp134;
    int tmp135;
    int tmp136;
    int tmp137;
    int tmp138;
    int tmp139;
    int tmp140;
    int tmp141;
    int tmp142;
    int tmp144;
    int tmp146;
    int tmp148;
    int tmp149;
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
    int tmp169;
    int tmp17;
    int tmp170;
    int tmp171;
    int tmp172;
    int tmp174;
    int tmp175;
    int tmp176;
    int tmp177;
    int tmp178;
    int tmp179;
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
    int tmp19;
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
    int tmp204;
    int tmp205;
    int tmp206;
    int tmp207;
    int tmp209;
    int tmp21;
    int tmp210;
    int tmp211;
    int tmp212;
    int tmp213;
    int tmp214;
    int tmp215;
    int tmp216;
    int tmp217;
    int tmp218;
    int tmp219;
    int tmp22;
    int tmp220;
    int tmp221;
    int tmp222;
    int tmp223;
    int tmp224;
    int tmp225;
    int tmp226;
    int tmp227;
    int tmp228;
    int tmp229;
    int tmp23;
    int tmp230;
    int tmp231;
    int tmp232;
    int tmp233;
    int tmp234;
    int tmp235;
    int tmp236;
    int tmp237;
    int tmp238;
    int tmp239;
    int tmp240;
    int tmp241;
    int tmp243;
    int tmp244;
    int tmp245;
    int tmp246;
    int tmp247;
    int tmp248;
    int tmp249;
    int tmp25;
    int tmp251;
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
    int tmp45;
    int tmp46;
    int tmp47;
    int tmp48;
    int tmp5;
    int tmp50;
    int tmp52;
    int tmp53;
    int tmp54;
    int tmp55;
    int tmp56;
    int tmp57;
    int tmp58;
    int tmp59;
    int tmp60;
    int tmp61;
    int tmp62;
    int tmp63;
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
    s_SC_MP_EnumPlayers local_0;
    s_SC_P_getinfo local_75;

    switch (info->message) {
    case 0:
        local_ = func_0448();
        if (local_ && tmp4) {
            SC_MissionFailed();
            return TRUE;
        }
        param_1->field_20 = 0.2f;
        if (tmp7) {
            local_0 = data_;
            data_ = tmp10;
            if (tmp11 && tmp12) {
                tmp13 = 0.0f;
                local_63.field1 = 3490;
                local_63.field2 = 3491;
                SC_ShowMovieInfo(&local_63);
            }
            if (tmp19 && tmp20) {
                SC_ShowMovieInfo(0);
            }
        }
        break;
    case 1:
        break;
    case 2:
        break;
    case 4:
        break;
    case 20:
        SC_sgi(tmp209, tmp210);
        SC_RadioBatch_Begin();
        local_0 = 0.0f;
        local_22 = SC_P_GetBySideGroupMember(tmp211, tmp212, tmp213);
        SC_P_Speech2(local_22, tmp214, &local_0);
        local_0 = tmp202;
        SC_SpeechRadio2(tmp215, &local_0);
        local_0 = tmp203;
        SC_P_Speech2(local_22, tmp216, &local_0);
        local_0 = tmp204;
        SC_SpeechRadio2(tmp217, &local_0);
        local_0 = tmp205;
        SC_P_SpeechMes2(local_22, tmp218, &local_0, tmp219);
        tmp155 = tmp206;
        param_1->field_20 = 0.1f;
        SC_RadioBatch_End();
        break;
    case 11:
        SC_message(&tmp225);
        if (tmp224) {
            tmp155 = 3.0f;
        }
        break;
    case 3:
        break;
    case 10:
        func_0994(tmp232);
        break;
    case 7:
        SC_SetObjectScript("heli1", "levels\\ricefield\\data\\pilot\\scripts\\heli1.c");
        SC_SetObjectScript("heli2", "levels\\ricefield\\data\\pilot\\scripts\\heli2.c");
        SC_SetObjectScript("heli3", "levels\\ricefield\\data\\pilot\\scripts\\heli3.c");
        SC_Item_Preload(147);
        SC_SetMapFpvModel("g\\weapons\\Vvh_map\\map_ricefield.bes");
        SC_sgi(SGI_CURRENTMISSION, 25);
        SC_PreloadBES(1, "Levels\\Ricefield\\data\\Pilot\\objects\\ivq_kopac.bes");
        tmp61 = 0.2f;
        break;
    case 667:
        break;
    case 15:
        if (tmp240) {
            param_1->field_12 = 0.0f;
        } else {
            tmp249 = tmp247;
            param_1->field_12 = 1;
        }
        break;
    default:
    }
    initside = 32;
    *tmp23 = 4;
    SC_InitSide(0.0f, &initside);
    initgroup = 0.0f;
    *tmp25 = 0.0f;
    *tmp27 = 16;
    *tmp29 = 100.0f;
    SC_InitSideGroup(&initgroup);
    initgroup = 0.0f;
    *tmp31 = 1;
    *tmp33 = 2;
    *tmp35 = 100.0f;
    SC_InitSideGroup(&initgroup);
    initgroup = 0.0f;
    *tmp37 = 2;
    *tmp39 = 16;
    *tmp41 = 100.0f;
    SC_InitSideGroup(&initgroup);
    *tmp43 = 12;
    SC_InitSide(1, &initside);
    i = 0.0f;
    i = SC_ggi(tmp66);
    if (!tmp47) {
    } else {
        local_22 = SC_P_GetBySideGroupMember(tmp52, tmp53, tmp54);
        SC_P_IsReady(local_22);
        g_save[0.0f] = 1;
        missionsave = 9136;
        *tmp50 = 9137;
        SC_MissionSave(&missionsave);
    }
    if (!tmp56) {
    } else {
        tmp61 = tmp60;
        tmp63 = 1;
        SC_AGS_Set(0.0f);
    }
    local_0 = 0.5f;
    SC_SpeechRadio2(3400, &local_0);
    local_0 = tmp68;
    SC_SpeechRadio2(3401, &local_0);
    local_0 = tmp69;
    SC_SpeechRadio2(3402, &local_0);
    local_0 = tmp70;
    SC_SpeechRadio2(3403, &local_0);
    local_0 = tmp71;
    SC_SpeechRadio2(3404, &local_0);
    local_0 = tmp72;
    data_225 = 1;
    SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
    if (!tmp74) {
    } else {
        tmp75 = SC_P_GetBySideGroupMember(0.0f, 0.0f, 2);
        local_25 = SC_P_GetBySideGroupMember(0.0f, 0.0f, 5);
        tmp76 = SC_P_GetBySideGroupMember(0.0f, 0.0f, 4);
        local_0 = 3.0f;
        SC_P_Speech2(tmp75, 3420, &local_0);
        local_0 = 3.2f;
        SC_P_Speech2(local_25, 3421, &local_0);
        data_225 = 2;
    }
    switch (info->param3) {
    case 2:
        SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
        if (tmp78) {
        } else {
            local_26 = SC_P_GetBySideGroupMember(0.0f, 2, 1);
            local_0 = 1.0f;
            SC_P_Speech2(local_26, 3422, &local_0);
            local_0 = tmp79;
            SC_P_GetBySideGroupMember(0.0f, 0.0f, 0.0f);
            SC_P_Speech2(local_91, 3423, &local_0);
            local_0 = tmp80;
            SC_P_Speech2(local_26, 3422, &local_0);
            local_0 = tmp81;
            SC_SpeechRadio2(3416, &local_0);
            local_0 = tmp82;
            SC_SpeechRadio2(3417, &local_0);
            local_0 = tmp83;
            SC_SpeechRadio2(tmp112, &local_0);
            local_0 = tmp84;
            SC_P_Speech2(local_26, tmp113, &local_0);
            local_0 = tmp85;
            local_2 = tmp86;
            SC_P_GetBySideGroupMember(tmp114, tmp115, tmp116);
            SC_P_Speech2(local_91, tmp117, &local_2);
            local_2 = tmp87;
            SC_P_Speech2(local_25, tmp118, &local_0);
            SC_SpeechRadio2(tmp119, &local_0);
            local_0 = tmp88;
            SC_SpeechRadio2(tmp120, &local_0);
            local_0 = tmp89;
            SC_SpeechRadio2(tmp121, &local_0);
            local_0 = tmp90;
            SC_SpeechRadio2(tmp122, &local_0);
            local_0 = tmp91;
            SC_SpeechRadio2(tmp123, &local_0);
            local_0 = tmp92;
            SC_SpeechRadio2(tmp124, &local_0);
            local_0 = tmp93;
            data_225 = 3;
        }
        break;
    case 3:
        SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
        if (tmp95) {
        } else {
            local_0 = 0.0f;
            SC_SpeechRadio2(3440, &local_0);
            local_0 = tmp96;
            SC_SpeechRadio2(3441, &local_0);
            local_0 = tmp97;
            SC_SpeechRadio2(3442, &local_0);
            local_0 = tmp98;
            SC_SpeechRadio2(3443, &local_0);
            local_0 = tmp99;
            SC_SpeechRadio2(3444, &local_0);
            local_0 = tmp100;
            SC_SpeechRadio2(3445, &local_0);
            local_0 = tmp101;
            SC_SpeechRadio2(3446, &local_0);
            local_0 = tmp102;
            data_225 = 4;
        }
        break;
    case 4:
        SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
        if (tmp104) {
        } else {
            data_225 = 5;
            local_26 = SC_P_GetBySideGroupMember(0.0f, 2, 1);
            local_22 = SC_P_GetBySideGroupMember(0.0f, 0.0f, 0.0f);
            local_0 = 0.0f;
            SC_P_Speech2(local_26, 3447, &local_0);
            local_0 = tmp105;
            SC_P_Speech2(local_22, 3448, &local_0);
            local_0 = tmp106;
            SC_P_Speech2(local_26, 3449, &local_0);
            local_0 = tmp107;
            param_1->field_20 = tmp108;
            SC_P_Speech2(local_22, 3450, &local_0);
        }
        break;
    case 5:
        SC_PC_EnableExit(1);
        data_225 = 6;
        break;
    default:
    }
    if (!tmp126) {
        func_0292();
        func_0355();
        tmp126 = 0.0f;
        g_save[1] = 1;
        missionsave = 9138;
        *tmp131 = 9139;
        SC_MissionSave(&missionsave);
    }
    func_0612(tmp134);
    func_0612(tmp137);
    local_22 = SC_P_GetBySideGroupMember(0.0f, 0.0f, 0.0f);
    if (!local_) {
        SC_P_GetActive(local_);
    } else {
    }
    if (!local_22) goto block_187; // @2418
    SC_P_IsReady(local_);
    if (!local_90) {
        SC_P_IsReady(local_22);
        tmp138 = SC_P_GetDistance(local_, local_22);
        SC_sgi(SGI_LEVELPHASE, 3);
        local_0 = 0.0f;
        SC_P_Speech2(local_22, 3451, &local_0);
        local_0 = tmp140;
        SC_P_Speech2(local_, 3452, &local_0);
        local_0 = tmp141;
        SC_P_Speech2(local_22, 3453, &local_0);
        local_0 = tmp142;
        tmp144 = 3471;
        *tmp146 = 2;
        SC_SetObjectives(1, &local_83, 0.0f);
    }
    SC_Radio_Enable(20);
    SC_PC_EnableRadioBreak(1);
    SC_sgi(SGI_LEVELPHASE, 4);
    switch (local_89) {
    case 4:
    case 5:
        if (tmp151) {
            tmp155 = tmp154;
        } else {
            func_0612(tmp157);
            SC_P_GetPos(local_, &tmp180);
            i = 0.0f;
        }
    case 6:
        if (tmp161) {
            i = 2;
            tmp165 = tmp164;
            SC_P_IsInHeli(local_);
            SC_P_SetToHeli(local_, "heli2", 3);
            func_0985(local_);
            SC_P_Ai_EnterHeli(local_, "heli2", 4);
            param_1->field_20 = 4.0f;
            i = tmp169;
            local_22 = SC_P_GetBySideGroupMember(0.0f, 0.0f, 0.0f);
            SC_P_IsInHeli(local_22);
            i = tmp170;
            SC_sgi(SGI_LEVELPHASE, 8);
            SC_AGS_Set(1);
            param_1->field_20 = 0.1f;
            tmp174 = 15.0f;
        } else {
            if (tmp175) {
                tmp174 = tmp178;
                if (tmp179) {
                    func_1021();
                    SC_TheEnd();
                    SC_sgi(SGI_LEVELPHASE, 9);
                }
            }
        }
        break;
    }
    SC_ggi(SGI_LEVPILOT_JUSTLOADEDVALUE);
    SC_sgi(SGI_LEVPILOT_JUSTLOADEDVALUE, tmp236);
    func_0994(g_trashes_enabled);
    return 0;  // FIX (06-05): Synthesized return value
}

