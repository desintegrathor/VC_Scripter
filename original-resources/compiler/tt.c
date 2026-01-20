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
float g_final_enter_timer;
dword g_will_pos[12];
dword g_vill_visited[4];
int g_pilot_phase;
float g_pilot_timer;
dword g_pilot_vill_nr;
float g_showinfo_timer;
int g_trashes_enabled;
dword gShot_pos[3];
float gEndTimer;
float gPilotCommTime;
dword g_save[2];
dword g_music[2];
float gStartMusicTime;

int _init(s_SC_L_info *info) {
    c_Vector3 j;
    c_Vector3 local_0;
    c_Vector3 local_11;
    c_Vector3 local_2;
    c_Vector3 local_7;
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
    s_SC_P_getinfo local_75;

    return 0;  // FIX (06-05): Synthesized return value
}

int func_0292(void) {
    int t321_ret;  // Auto-generated
    int t332_ret;  // Auto-generated
    int z;  // Auto-generated

    c_Vector3 j;
    c_Vector3 local_0;
    c_Vector3 local_11;
    c_Vector3 local_2;
    c_Vector3 local_7;
    c_Vector3 vec;
    int i;
    int k;
    int local_;
    int tmp;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    s_SC_P_getinfo local_75;

    SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0);
    SC_ZeroMem(&local_2, 12);
    local_2.z = -20000.0f;
    i = 0;
    // Loop header - Block 2 @312
    for (i = 0; (i < 16); i = tmp8) {
        if (!tmp5) break;  // exit loop @354
        t321_ret = SC_P_GetBySideGroupMember(tmp2, tmp3, i);
        local_ = SC_P_GetBySideGroupMember(tmp2, tmp3, i);
        if (!local_) {
            SC_P_SetActive(local_, tmp4);
            SC_P_SetPos(local_, &local_2);
        } else {
            i = tmp8;
        }
        t332_ret = SC_P_IsReady(local_);
        if (!SC_P_IsReady(local_)) goto block_7; // @345
    }
    return i;
}

int func_0355(void) {
    int t383_ret;  // Auto-generated
    int t426_ret;  // Auto-generated

    c_Vector3 j;
    c_Vector3 local_0;
    c_Vector3 local_11;
    c_Vector3 local_7;
    int i;
    int idx;
    int k;
    int local_;
    int local_2;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_P_getinfo local_75;

    i = 0;
    // Loop header - Block 10 @362
    for (i = 0; (i < 12); i = tmp6) {
        if (!tmp) break;  // exit loop @413
        if (!tmp1) {
            idx = 0;
        } else {
            i = tmp6;
        }
        // Loop header - Block 13 @374
        for (idx = 0; (idx < 16); idx = tmp5) {
            if (!tmp3) break;  // exit loop @404
            t383_ret = SC_P_GetBySideGroupMember(1, i, idx);
            local_ = SC_P_GetBySideGroupMember(1, i, idx);
            if (!local_) {
                SC_P_SetActive(local_, tmp2);
            } else {
                idx = tmp5;
            }
        }
    }
    i = 0;
    // Loop header - Block 19 @417
    for (i = 0; (i < 16); i = tmp11) {
        if (!tmp9) break;  // exit loop @447
        t426_ret = SC_P_GetBySideGroupMember(3, tmp7, i);
        local_ = SC_P_GetBySideGroupMember(3, tmp7, i);
        if (!local_) {
            SC_P_SetActive(local_, tmp8);
        } else {
            i = tmp11;
        }
    }
    return i;
}

int func_0448(int param_0, int param_1) {
    int t453_ret;  // Auto-generated

    c_Vector3 j;
    c_Vector3 local_0;
    c_Vector3 local_11;
    c_Vector3 local_2;
    c_Vector3 local_7;
    int tmp;
    s_SC_P_getinfo local_75;

    t453_ret = SC_P_GetBySideGroupMember(2, 0, 1);
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0511(int param_0, int param_1) {
    c_Vector3 local_0;
    c_Vector3 local_11;
    c_Vector3 local_2;
    c_Vector3 local_7;
    c_Vector3 vec;
    dword local_3[16];
    float t539_ret;
    int i;
    int k;
    int local_;
    int local_5;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp12;
    int tmp13;
    int tmp14;
    int tmp16;
    int tmp18;
    int tmp2;
    int tmp20;
    int tmp21;
    int tmp22;
    int tmp23;
    int tmp25;
    int tmp27;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_P_getinfo local_75;

    SC_P_GetPos(param_0, &tmp);
    SC_ZeroMem(local_3, 8);
    i = 0;
    // Loop header - Block 32 @527
    for (i = 0; (i < 4); i = tmp27) {
        if (!tmp1) break;  // exit loop @611
        t539_ret = SC_2VectorsDist(&tmp, tmp3);
        local_ = SC_2VectorsDist(&tmp, tmp3);
        if (!tmp7) {
            local_3.field_4 = tmp9;
            tmp14 = tmp13;
            local_ = tmp16;
            tmp18 = i;
        } else {
        }
        local_ = tmp23;
        tmp25 = i;
        i = tmp27;
        continue;  // back to loop header @527
    }
    return i;
}

int func_0612(float param_0) {
    int t625_ret;  // Auto-generated
    int t654_ret;  // Auto-generated
    float t729_ret;  // Auto-generated
    int t759_ret;  // Auto-generated
    int t767_ret;  // Auto-generated
    float t790_ret;  // Auto-generated
    int t804_ret;  // Auto-generated
    float t843_ret;  // Auto-generated
    int t870_ret;  // Auto-generated
    int t886_ret;  // Auto-generated
    int t916_ret;  // Auto-generated
    int t944_ret;  // Auto-generated
    int t960_ret;  // Auto-generated

    c_Vector3 j;
    c_Vector3 local_0;
    c_Vector3 local_2;
    c_Vector3 local_7;
    c_Vector3 vec;
    float t947_ret;
    int data_;
    int data_258;
    int i;
    int k;
    int local_;
    int local_1;
    int local_10;
    int local_11;
    int local_12;
    int local_13;
    int local_4;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
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
    int tmp8;
    int tmp9;
    s_SC_P_getinfo local_75;

    switch (g_pilot_phase) {
    case 0:
        t625_ret = SC_PC_GetPos(&local_);
        i = 0;
        break;
    case 1:
        tmp25 = tmp28;
        if (tmp29) {
            data_ = 2;
            t759_ret = SC_PC_Get();
            func_0511(SC_PC_Get(), &tmp43);
            t767_ret = rand();
            data_258 = tmp35;
            func_0448();
            SC_P_ScriptMessage(local_12, tmp44, data_258);
            t790_ret = frnd(30.0f);
            tmp25 = tmp37;
            t804_ret = rand();
            SC_SpeechRadio2(tmp42, tmp46);
            func_0448();
            SC_HUD_RadarShowPlayer(local_12, tmp47);
        }
        return tmp60;
    case 2:
        tmp25 = tmp49;
        if (tmp50) {
            data_ = 1;
            t843_ret = frnd(10.0f);
            tmp25 = tmp52;
            data_258 = 255;
            func_0448();
            SC_P_ScriptMessage(local_12, 0, data_258);
            SC_HUD_RadarShowPlayer(0, 0);
        } else {
            t870_ret = SC_PC_GetPos(&local_);
            func_0448(SC_PC_GetPos(&local_));
            t886_ret = SC_IsNear2D(&local_, &local_7, tmp55);
            if (t886_ret = SC_IsNear2D(&local_, &local_7, tmp55)) {
                data_ = 4;
                tmp25 = 0;
                SC_SetSideAlly(tmp56, tmp57, tmp58);
                SC_sgi(tmp59, tmp60);
            }
        }
        break;
    case 4:
        t916_ret = SC_ggi(tmp72);
        if (tmp63) {
        } else {
            tmp25 = tmp64;
            if (tmp65) {
                tmp25 = 1069547520;
                func_0448();
                t944_ret = SC_PC_Get();
                t947_ret = SC_P_GetDistance(tmp71, SC_PC_Get());
                local_10 = SC_P_GetDistance(tmp71, SC_PC_Get());
                if (tmp68) {
                    t960_ret = SC_PC_GetPos(&local_7);
                    func_0448(SC_PC_GetPos(&local_7));
                    SC_P_Ai_Go(local_12, &local_7);
                } else {
                    if (tmp70) {
                        func_0448();
                        SC_P_Ai_Stop(local_12);
                    }
                }
            }
        }
        break;
    default:
        break;
    }
    if (!tmp6) {
    } else {
        t654_ret = SC_IsNear2D(tmp8, &local_, tmp2);
    }
    g_vill_visited[i] = 1;
    i = tmp13;
    local_1 = 0;
    i = 0;
    // Loop header - Block 48 @683
    for (i = 0; (i < 3); i = tmp19) {
        if (!tmp14) break;  // exit loop @711
        if (!tmp17) {
            local_1 = tmp18;
        } else {
            i = tmp19;
        }
    }
    if (!tmp20) {
        data_ = 1;
        t729_ret = frnd(10.0f);
        tmp25 = tmp24;
    } else {
    }
    if (!tmp22) goto block_56; // @736
    return 0;  // FIX (06-05): Synthesized return value
}

void func_0985(int param_0) {
    c_Vector3 j;
    c_Vector3 local_0;
    c_Vector3 local_11;
    c_Vector3 local_2;
    c_Vector3 local_7;
    s_SC_P_getinfo local_75;

    SC_P_Ai_SetMoveMode(param_0, SC_P_AI_MOVEMODE_RUN);
    SC_P_Ai_SetMovePos(param_0, SC_P_AI_MOVEPOS_STAND);
    return;
}

int func_0994(int param_0) {
    int t1003_ret;  // Auto-generated

    c_Vector3 j;
    c_Vector3 local_0;
    c_Vector3 local_11;
    c_Vector3 local_2;
    c_Vector3 local_7;
    int local_;
    int tmp;
    int tmp1;
    s_SC_P_getinfo local_75;

    tmp = param_0;
    t1003_ret = SC_NOD_Get(0, "maj_uh-1d_vreck");
    local_ = SC_NOD_Get(0, "maj_uh-1d_vreck");
    if (!local_) {
        SC_DUMMY_Set_DoNotRenHier2(local_, 1);
    }
    return TRUE;
}

int func_1021(void) {
    int t1040_ret;  // Auto-generated

    c_Vector3 enum_pl;
    c_Vector3 local_0;
    c_Vector3 local_11;
    c_Vector3 local_2;
    c_Vector3 local_7;
    int local_;
    int local_256;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    s_SC_P_getinfo local_75;

    local_ = 64;
    SC_sgi(SGI_DEBR_01, 0);
    SC_sgi(SGI_REWARD_PILOT, 1);
    t1040_ret = SC_MP_EnumPlayers(&enum_pl, &local_, 1);
    if (!SC_MP_EnumPlayers(&enum_pl, &local_, 1)) {
        SC_sgi(tmp2, tmp3);
        SC_sgi(tmp4, tmp5);
    } else {
        return tmp5;
    }
    if (!tmp1) goto block_91; // @1056
    return 0;  // FIX (06-05): Synthesized return value
}

int ScriptMain(s_SC_L_info *info) {
    int c;  // Auto-generated
    int d;  // Auto-generated
    dword heli1;  // Auto-generated
    dword heli2;  // Auto-generated
    dword heli3;  // Auto-generated
    dword ivq_kopac;  // Auto-generated
    dword map_ricefield;  // Auto-generated
    dword param_1;  // Auto-generated
    int ricefield;  // Auto-generated
    int t1544_ret;  // Auto-generated
    int t1556_ret;  // Auto-generated
    int t1618_ret;  // Auto-generated
    int t1635_ret;  // Auto-generated
    int t1700_ret;  // Auto-generated
    int t1785_ret;  // Auto-generated
    int t1797_ret;  // Auto-generated
    int t1808_ret;  // Auto-generated
    int t1819_ret;  // Auto-generated
    int t1856_ret;  // Auto-generated
    int t1868_ret;  // Auto-generated
    int t1894_ret;  // Auto-generated
    int t1970_ret;  // Auto-generated
    int t2061_ret;  // Auto-generated
    int t2155_ret;  // Auto-generated
    int t2171_ret;  // Auto-generated
    int t2182_ret;  // Auto-generated
    int t2311_ret;  // Auto-generated
    int t2325_ret;  // Auto-generated
    int t2333_ret;  // Auto-generated
    int t2341_ret;  // Auto-generated
    int t2576_ret;  // Auto-generated
    int t2622_ret;  // Auto-generated
    int t2664_ret;  // Auto-generated
    int t2673_ret;  // Auto-generated
    int t2696_ret;  // Auto-generated
    int t2766_ret;  // Auto-generated
    int t2941_ret;  // Auto-generated
    int y;  // Auto-generated
    int z;  // Auto-generated

    c_Vector3 j;
    c_Vector3 local_0;
    c_Vector3 local_11;
    c_Vector3 local_2;
    c_Vector3 local_7;
    c_Vector3 vec;
    char local_67[32];
    float t2350_ret;
    float t2484_ret;
    float t2542_ret;
    int data_;
    int data_225;
    int data_266;
    int data_268;
    int i;
    int idx;
    int initgroup;
    int initside;
    int k;
    int local_;
    int local_17;
    int local_22;
    int local_23;
    int local_24;
    int local_25;
    int local_26;
    int local_27;
    int local_4;
    int local_43;
    int local_63;
    int local_80;
    int local_83;
    int local_87;
    int local_88;
    int local_89;
    int local_90;
    int missionsave;
    int objective;
    int plfollow;
    int plinfo;
    int side;
    int side2;
    int sideB;
    int t1463_;
    int t1481_;
    int t2409_;
    int t2523_;
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
    int tmp136;
    int tmp138;
    int tmp139;
    int tmp140;
    int tmp141;
    int tmp142;
    int tmp143;
    int tmp144;
    int tmp145;
    int tmp146;
    int tmp147;
    int tmp148;
    int tmp149;
    int tmp15;
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
    int tmp172;
    int tmp173;
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
    int tmp208;
    int tmp209;
    int tmp21;
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
    int tmp231;
    int tmp233;
    int tmp234;
    int tmp235;
    int tmp236;
    int tmp237;
    int tmp238;
    int tmp239;
    int tmp24;
    int tmp240;
    int tmp241;
    int tmp242;
    int tmp243;
    int tmp244;
    int tmp245;
    int tmp246;
    int tmp247;
    int tmp249;
    int tmp251;
    int tmp253;
    int tmp254;
    int tmp255;
    int tmp256;
    int tmp257;
    int tmp258;
    int tmp259;
    int tmp26;
    int tmp260;
    int tmp261;
    int tmp262;
    int tmp263;
    int tmp264;
    int tmp265;
    int tmp266;
    int tmp267;
    int tmp268;
    int tmp269;
    int tmp270;
    int tmp271;
    int tmp272;
    int tmp273;
    int tmp274;
    int tmp275;
    int tmp277;
    int tmp278;
    int tmp279;
    int tmp28;
    int tmp280;
    int tmp281;
    int tmp282;
    int tmp283;
    int tmp284;
    int tmp285;
    int tmp286;
    int tmp287;
    int tmp288;
    int tmp290;
    int tmp292;
    int tmp293;
    int tmp294;
    int tmp295;
    int tmp296;
    int tmp297;
    int tmp298;
    int tmp299;
    int tmp3;
    int tmp30;
    int tmp301;
    int tmp303;
    int tmp304;
    int tmp305;
    int tmp306;
    int tmp307;
    int tmp308;
    int tmp309;
    int tmp310;
    int tmp311;
    int tmp312;
    int tmp313;
    int tmp314;
    int tmp315;
    int tmp316;
    int tmp317;
    int tmp318;
    int tmp319;
    int tmp32;
    int tmp321;
    int tmp322;
    int tmp323;
    int tmp324;
    int tmp325;
    int tmp326;
    int tmp327;
    int tmp328;
    int tmp330;
    int tmp331;
    int tmp332;
    int tmp333;
    int tmp334;
    int tmp335;
    int tmp336;
    int tmp337;
    int tmp338;
    int tmp339;
    int tmp34;
    int tmp340;
    int tmp341;
    int tmp342;
    int tmp343;
    int tmp344;
    int tmp345;
    int tmp346;
    int tmp347;
    int tmp348;
    int tmp349;
    int tmp350;
    int tmp351;
    int tmp352;
    int tmp353;
    int tmp354;
    int tmp355;
    int tmp356;
    int tmp357;
    int tmp358;
    int tmp359;
    int tmp36;
    int tmp360;
    int tmp361;
    int tmp362;
    int tmp364;
    int tmp365;
    int tmp366;
    int tmp367;
    int tmp368;
    int tmp369;
    int tmp370;
    int tmp371;
    int tmp372;
    int tmp373;
    int tmp374;
    int tmp375;
    int tmp376;
    int tmp377;
    int tmp378;
    int tmp379;
    int tmp38;
    int tmp380;
    int tmp381;
    int tmp382;
    int tmp383;
    int tmp384;
    int tmp385;
    int tmp386;
    int tmp387;
    int tmp388;
    int tmp389;
    int tmp390;
    int tmp391;
    int tmp392;
    int tmp393;
    int tmp394;
    int tmp395;
    int tmp396;
    int tmp397;
    int tmp399;
    int tmp4;
    int tmp40;
    int tmp400;
    int tmp401;
    int tmp402;
    int tmp403;
    int tmp404;
    int tmp405;
    int tmp407;
    int tmp42;
    int tmp44;
    int tmp46;
    int tmp47;
    int tmp49;
    int tmp5;
    int tmp51;
    int tmp53;
    int tmp54;
    int tmp56;
    int tmp58;
    int tmp60;
    int tmp62;
    int tmp64;
    int tmp66;
    int tmp68;
    int tmp7;
    int tmp70;
    int tmp72;
    int tmp74;
    int tmp76;
    int tmp77;
    int tmp78;
    int tmp79;
    int tmp8;
    int tmp80;
    int tmp81;
    int tmp83;
    int tmp84;
    int tmp86;
    int tmp87;
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
    s_SC_P_getinfo local_75;
    s_SC_P_getinfo player_info;

    switch (info->message) {
    case 0:
        local_ = func_0448();
        if (local_ && tmp4) {
            SC_MissionFailed();
            return TRUE;
        }
        &param_1.field_20 = 0.2f;
        if (tmp7) {
            local_0 = data_;
            data_ = tmp10;
            if (tmp11 && tmp12) {
                tmp13 = 0;
                local_63.field_4 = 3490;
                local_63.field_8 = 3491;
                SC_ShowMovieInfo(&local_63);
            }
            if (tmp19 && tmp20) {
                SC_ShowMovieInfo(tmp21);
            }
        }
        if (tmp22) {
            initside = 32;
            initside.y = 4;
            SC_InitSide(0, &initside);
            initgroup = 0;
            initgroup.y = 0.0f;
            initgroup.z = 16;
            initgroup.field_12 = 100.0f;
            SC_InitSideGroup(&initgroup);
            initgroup = 0;
            initgroup.y = 1;
            initgroup.z = 2;
            initgroup.field_12 = 100.0f;
            SC_InitSideGroup(&initgroup);
            initgroup = 0;
            initgroup.y = 2;
            initgroup.z = 16;
            initgroup.field_12 = 100.0f;
            SC_InitSideGroup(&initgroup);
            initside.y = 12;
            SC_InitSide(1, &initside);
            i = 0;
        } else {
            if (tmp128) {
                t1618_ret = SC_ggi(tmp154);
                i = SC_ggi(tmp154);
                if (tmp131) {
                } else {
                    t1635_ret = SC_P_GetBySideGroupMember(tmp138, tmp139, tmp140);
                    local_22 = SC_P_GetBySideGroupMember(tmp138, tmp139, tmp140);
                    if (local_22 && SC_P_IsReady(local_22)) {
                        g_save[0] = 1;
                        missionsave = 9136;
                        missionsave.y = 9137;
                        SC_MissionSave(&missionsave);
                    }
                }
                if (tmp142) {
                } else {
                    if (tmp143 && tmp148) {
                        tmp149 = 1;
                        t1700_ret = SC_AGS_Set(tmp152);
                    }
                }
                if (tmp153) {
                    if (tmp155) {
                        local_0 = 1056964608;
                        SC_SpeechRadio2(3400, &local_0);
                        local_0 = tmp156;
                        SC_SpeechRadio2(3401, &local_0);
                        local_0 = tmp157;
                        SC_SpeechRadio2(3402, &local_0);
                        local_0 = tmp158;
                        SC_SpeechRadio2(3403, &local_0);
                        local_0 = tmp159;
                        SC_SpeechRadio2(3404, &local_0);
                        local_0 = tmp160;
                        data_225 = 1;
                    } else {
                        if (tmp161) {
                            t1785_ret = SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
                            if (tmp163) {
                            } else {
                                t1797_ret = SC_P_GetBySideGroupMember(0, 0, 2);
                                tmp165 = SC_P_GetBySideGroupMember(0, 0, 2);
                                t1808_ret = SC_P_GetBySideGroupMember(0, 0, 5);
                                local_25 = SC_P_GetBySideGroupMember(0, 0, 5);
                                t1819_ret = SC_P_GetBySideGroupMember(0, 0, 4);
                                tmp168 = SC_P_GetBySideGroupMember(0, 0, 4);
                                local_0 = 1077936128;
                                SC_P_Speech2(tmp165, 3420, &local_0);
                                local_0 = 1078774989;
                                SC_P_Speech2(local_25, 3421, &local_0);
                                data_225 = 2;
                            }
                        } else {
                            if (tmp169) {
                                t1856_ret = SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
                                if (tmp171) {
                                } else {
                                    t1868_ret = SC_P_GetBySideGroupMember(0, 2, 1);
                                    local_26 = SC_P_GetBySideGroupMember(0, 2, 1);
                                    local_0 = 1065353216;
                                    SC_P_Speech2(local_26, 3422, &local_0);
                                    local_0 = tmp173;
                                    t1894_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                                    SC_P_Speech2(SC_P_GetBySideGroupMember(0, 0, 0), 3423, &local_0);
                                    local_0 = tmp175;
                                    SC_P_Speech2(local_26, 3422, &local_0);
                                    local_0 = tmp176;
                                    SC_SpeechRadio2(3416, &local_0);
                                    local_0 = tmp177;
                                    SC_SpeechRadio2(3417, &local_0);
                                    local_0 = tmp178;
                                    SC_SpeechRadio2(tmp212, &local_0);
                                    local_0 = tmp179;
                                    SC_P_Speech2(local_26, tmp213, &local_0);
                                    local_0 = tmp180;
                                    local_2 = tmp181;
                                    t1970_ret = SC_P_GetBySideGroupMember(tmp214, tmp215, tmp216);
                                    SC_P_Speech2(SC_P_GetBySideGroupMember(tmp214, tmp215, tmp216), tmp217, &local_2);
                                    local_2 = tmp183;
                                    SC_P_Speech2(local_25, tmp218, &local_0);
                                    SC_SpeechRadio2(tmp219, &local_0);
                                    local_0 = tmp184;
                                    SC_SpeechRadio2(tmp220, &local_0);
                                    local_0 = tmp185;
                                    SC_SpeechRadio2(tmp221, &local_0);
                                    local_0 = tmp186;
                                    SC_SpeechRadio2(tmp222, &local_0);
                                    local_0 = tmp187;
                                    SC_SpeechRadio2(tmp223, &local_0);
                                    local_0 = tmp188;
                                    SC_SpeechRadio2(tmp224, &local_0);
                                    local_0 = tmp189;
                                    data_225 = 3;
                                }
                            } else {
                                if (tmp190) {
                                    t2061_ret = SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
                                    if (tmp192) {
                                    } else {
                                        local_0 = 0;
                                        SC_SpeechRadio2(3440, &local_0);
                                        local_0 = tmp193;
                                        SC_SpeechRadio2(3441, &local_0);
                                        local_0 = tmp194;
                                        SC_SpeechRadio2(3442, &local_0);
                                        local_0 = tmp195;
                                        SC_SpeechRadio2(3443, &local_0);
                                        local_0 = tmp196;
                                        SC_SpeechRadio2(3444, &local_0);
                                        local_0 = tmp197;
                                        SC_SpeechRadio2(3445, &local_0);
                                        local_0 = tmp198;
                                        SC_SpeechRadio2(3446, &local_0);
                                        local_0 = tmp199;
                                        data_225 = 4;
                                    }
                                } else {
                                    if (tmp200) {
                                        t2155_ret = SC_ggi(SGI_LEVPILOT_HELI3_ATTACK);
                                        if (tmp202) {
                                        } else {
                                            data_225 = 5;
                                            t2171_ret = SC_P_GetBySideGroupMember(0, 2, 1);
                                            local_26 = SC_P_GetBySideGroupMember(0, 2, 1);
                                            t2182_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                                            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
                                            local_0 = 0;
                                            SC_P_Speech2(local_26, 3447, &local_0);
                                            local_0 = tmp205;
                                            SC_P_Speech2(local_22, 3448, &local_0);
                                            local_0 = tmp206;
                                            SC_P_Speech2(local_26, 3449, &local_0);
                                            local_0 = tmp207;
                                            &param_1.field_20 = tmp208;
                                            SC_P_Speech2(local_22, 3450, &local_0);
                                        }
                                    } else {
                                        if (tmp211) {
                                            SC_PC_EnableExit(1);
                                            data_225 = 6;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else {
                    if (tmp225) {
                        if (tmp226) {
                            func_0292();
                            func_0355();
                            tmp226 = 0;
                            if (tmp228) {
                            } else {
                                g_save[1] = 1;
                                missionsave = 9138;
                                missionsave.y = 9139;
                                SC_MissionSave(&missionsave);
                            }
                        }
                        func_0612(tmp234);
                    } else {
                        if (tmp235) {
                            func_0612(tmp237);
                            t2311_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                            local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
                            if (local_ && local_22) {
                                t2325_ret = SC_P_GetActive(local_);
                                if (t2325_ret = SC_P_GetActive(local_)) {
                                    t2333_ret = SC_P_IsReady(local_);
                                    if (t2333_ret = SC_P_IsReady(local_)) {
                                        t2341_ret = SC_P_IsReady(local_22);
                                        if (t2341_ret = SC_P_IsReady(local_22)) {
                                            t2350_ret = SC_P_GetDistance(local_, local_22);
                                            tmp243 = SC_P_GetDistance(local_, local_22);
                                            if (tmp244) {
                                                SC_sgi(tmp253, tmp254);
                                                local_0 = 0;
                                                SC_P_Speech2(local_22, tmp255, &local_0);
                                                local_0 = tmp245;
                                                SC_P_Speech2(local_, tmp256, &local_0);
                                                local_0 = tmp246;
                                                SC_P_Speech2(local_22, tmp257, &local_0);
                                                local_0 = tmp247;
                                                tmp249 = 3471;
                                                *tmp251 = 2;
                                                SC_SetObjectives(tmp258, &objective, tmp259);
                                            }
                                        }
                                    }
                                }
                            }
                        } else {
                            if (tmp260) {
                                SC_Radio_Enable(20);
                                SC_PC_EnableRadioBreak(1);
                                SC_sgi(SGI_LEVELPHASE, 4);
                            } else {
                                if (tmp261) {
                                } else {
                                    if (tmp262) {
                                        if (tmp263) {
                                            tmp267 = tmp266;
                                        } else {
                                            func_0612(tmp269);
                                            SC_P_GetPos(local_, &local_11);
                                            i = 0;
                                        }
                                    } else {
                                        if (tmp309) {
                                            func_0612(tmp311);
                                        } else {
                                            if (tmp312) {
                                                i = 2;
                                                tmp316 = tmp315;
                                                t2622_ret = SC_P_IsInHeli(local_);
                                                if (t2622_ret = SC_P_IsInHeli(local_)) {
                                                    i = tmp322;
                                                } else {
                                                    if (tmp318) {
                                                        SC_P_SetToHeli(local_, "heli2", 3);
                                                    } else {
                                                        func_0985(local_);
                                                        SC_P_Ai_EnterHeli(local_, "heli2", tmp321);
                                                        &param_1.field_20 = 4.0f;
                                                    }
                                                }
                                                t2664_ret = SC_P_GetBySideGroupMember(0, 0, 0);
                                                local_22 = SC_P_GetBySideGroupMember(0, 0, 0);
                                                t2673_ret = SC_P_IsInHeli(local_22);
                                                if (t2673_ret = SC_P_IsInHeli(local_22)) {
                                                    i = tmp325;
                                                }
                                                if (tmp326) {
                                                    SC_sgi(tmp331, tmp332);
                                                    t2696_ret = SC_AGS_Set(tmp333);
                                                    &param_1.field_20 = 0.1f;
                                                    tmp330 = 1097859072;
                                                }
                                            } else {
                                                if (tmp334) {
                                                    tmp330 = tmp337;
                                                    if (tmp338) {
                                                        func_1021();
                                                        SC_TheEnd();
                                                        SC_sgi(tmp339, tmp340);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        // Loop header - Block 111 @1272
        for (i = 0; (i < 12); i = tmp53) {
            initgroup = 1;
            initgroup.y = i;
            initgroup.z = 16;
            initgroup.field_12 = 100.0f;
            SC_InitSideGroup(&initgroup);
        }
        initside = 2;
        initside.y = 2;
        SC_InitSide(tmp90, &initside);
        initgroup = 2;
        initgroup.y = 0.0f;
        initgroup.z = 1;
        initgroup.field_12 = 100.0f;
        SC_InitSideGroup(&initgroup);
        initgroup = 2;
        initgroup.y = 1;
        initgroup.z = 20;
        initgroup.field_12 = 0.0f;
        SC_InitSideGroup(&initgroup);
        SC_SetSideAlly(tmp91, tmp92, tmp93);
        SC_SetSideAlly(tmp94, tmp95, tmp96);
        initside = 2;
        initside.y = 1;
        SC_InitSide(tmp97, &initside);
        initgroup = 3;
        initgroup.y = 0.0f;
        initgroup.z = 16;
        initgroup.field_12 = 0.0f;
        SC_InitSideGroup(&initgroup);
        SC_SetSideAlly(tmp98, tmp99, tmp100);
        SC_SetSideAlly(tmp101, tmp102, tmp103);
        SC_SetSideAlly(tmp104, tmp105, tmp106);
        func_0994(tmp107);
        tmp23 = 1;
        SC_sgi(tmp108, tmp109);
        SC_sgi(tmp110, tmp111);
        SC_sgi(tmp112, tmp113);
        SC_sgi(tmp114, tmp115);
        SC_sgi(tmp76, tmp116);
        i = 0;
        // Loop header - Block 114 @1455
        for (i = 0; (i < 4); i = tmp89) {
            SC_ZeroMem(tmp79, 12);
            local_43[i] = 1069547520;
            *tmp84 = 1084227584;
            local_63[i] = i;
        }
        i = 0;
        // Loop header - Block 117 @1506
        for (i = 0; (i < 10); i = tmp119) {
            SC_Ai_SetPlFollow(1, i, 0, &plfollow, &local_63, &local_63, tmp117);
        }
        i = 0;
        // Loop header - Block 120 @1532
        for (i = 0; (i < 4); i = tmp127) {
            t1544_ret = sprintf(&tmp120, "WP_will%d", tmp122);
            t1556_ret = SC_GetWp(&tmp120, tmp125);
        }
        SC_sgi(SGI_LEVELPHASE, 0);
        SC_sgi(SGI_LEVPILOT_HELI3_ATTACK, 0);
        SC_sgi(SGI_LEVPILOT_JUSTLOADEDVALUE, 0);
        SC_RadioSetDist(10.0f);
        SC_ZeroMem(&data_266, tmp341);
        SC_ZeroMem(&data_268, tmp342);
        SC_ArtillerySupport(tmp343);
        SC_SetViewAnim(&tmp344, tmp345, tmp346, tmp347);
        SC_FadeTo(tmp348, tmp349);
        SC_FadeTo(tmp350, tmp351);
        // Loop header - Block 199 @2472
        for (i = 0; (i < 4); i = tmp304) {
            t2484_ret = SC_2VectorsDist(&local_11, tmp272);
            if (tmp274) {
                SC_sgi(tmp305, tmp306);
                SC_sgi(tmp307, i);
                local_11.z = side2;
                local_17 = tmp281;
                local_17.y = tmp287;
                local_17.z = 0.0f;
                t2542_ret = SC_VectorLen(&local_17);
                local_0 = tmp293;
                local_17 = tmp295;
                local_17.y = tmp298;
                local_17.z = 7.0f;
                t2576_ret = SC_Item_Create2(tmp308, &local_11, &local_17);
            } else {
                i = tmp304;
            }
        }
        break;
    case 1:
        if (tmp355) {
            SC_sgi(tmp364, tmp365);
            SC_RadioBatch_Begin();
            local_0 = 0;
            t2766_ret = SC_P_GetBySideGroupMember(tmp366, tmp367, tmp368);
            local_22 = SC_P_GetBySideGroupMember(tmp366, tmp367, tmp368);
            SC_P_Speech2(local_22, tmp369, &local_0);
            local_0 = tmp357;
            SC_SpeechRadio2(tmp370, &local_0);
            local_0 = tmp358;
            SC_P_Speech2(local_22, tmp371, &local_0);
            local_0 = tmp359;
            SC_SpeechRadio2(tmp372, &local_0);
            local_0 = tmp360;
            SC_P_SpeechMes2(local_22, tmp373, &local_0, tmp374);
            tmp267 = tmp361;
            &param_1.field_20 = 0.1f;
            SC_RadioBatch_End();
        }
        break;
    case 2:
        if (tmp378) {
            SC_message(&tmp380);
            if (tmp379) {
                tmp267 = 1077936128;
            }
        }
        break;
    case 4:
        if (tmp385) {
            func_0994(tmp387);
        } else {
            if (tmp386) {
            }
        }
        break;
    case 3:
        break;
    case 7:
        SC_SetObjectScript("heli1", "levels\\ricefield\\data\\pilot\\scripts\\heli1.c");
        SC_SetObjectScript("heli2", "levels\\ricefield\\data\\pilot\\scripts\\heli2.c");
        SC_SetObjectScript("heli3", "levels\\ricefield\\data\\pilot\\scripts\\heli3.c");
        SC_Item_Preload(147);
        SC_SetMapFpvModel("g\\weapons\\Vvh_map\\map_ricefield.bes");
        SC_sgi(SGI_CURRENTMISSION, 25);
        SC_PreloadBES(1, "Levels\\Ricefield\\data\\Pilot\\objects\\ivq_kopac.bes");
        tmp147 = 1045220557;
        break;
    case 11:
        t2941_ret = SC_ggi(SGI_LEVPILOT_JUSTLOADEDVALUE);
        SC_sgi(SGI_LEVPILOT_JUSTLOADEDVALUE, tmp392);
        func_0994(g_trashes_enabled);
        break;
    case 15:
        if (tmp396) {
            &param_1.field_12 = 0.0f;
        } else {
            tmp405 = tmp403;
            &param_1.field_12 = 1;
        }
        break;
    default:
        break;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

