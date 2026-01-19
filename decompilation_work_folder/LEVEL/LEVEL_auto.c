// Structured decompilation of decompilation/LEVEL/LEVEL.SCR
// Functions: 28

void _init(void) {
    // Block 0 @0
    DLD();
    t6_0 = PNT(local_0);
    DLD();
    t10_0 = PNT(local_0);
    DLD();
    t14_0 = PNT(local_0);
    DLD();
    t18_0 = PNT(local_0);
    DLD();
    t22_0 = PNT(local_0);
    DLD();
    t26_0 = PNT(local_0);
    DLD();
    t30_0 = PNT(local_0);
    DLD();
    t34_0 = PNT(local_0);
    DLD();
    t38_0 = PNT(local_0);
    DLD();
    t42_0 = PNT(local_0);
    DLD();
    t46_0 = PNT(local_0);
    DLD();
    t50_0 = PNT(local_0);
    DLD();
    t54_0 = PNT(local_0);
    DLD();
    t58_0 = PNT(local_0);
    DLD();
    t62_0 = PNT(local_0);
    DLD();
    t66_0 = PNT(local_0);
    DLD();
    t70_0 = PNT(local_0);
    DLD();
    t74_0 = PNT(local_0);
    DLD();
    t78_0 = PNT(local_0);
    DLD();
    t82_0 = PNT(local_0);
    DLD();
    t86_0 = PNT(local_0);
    DLD();
    t90_0 = PNT(local_0);
    DLD();
    t94_0 = PNT(local_0);
    DLD();
    t98_0 = PNT(local_0);
    DLD();
    t102_0 = PNT(local_0);
    DLD();
    t106_0 = PNT(local_0);
    DLD();
    t110_0 = PNT(local_0);
    DLD();
    t114_0 = PNT(local_0);
    DLD();
    t118_0 = PNT(local_0);
    DLD();
    t122_0 = PNT(local_0);
    DLD();
    t126_0 = PNT(local_0);
    DLD();
    t130_0 = PNT(local_0);
    DLD();
    t134_0 = PNT(local_0);
    DLD();
    t138_0 = PNT(local_0);
    DLD();
    t142_0 = PNT(local_0);
    DLD();
    t146_0 = PNT(local_0);
    DLD();
    t150_0 = PNT(local_0);
    DLD();
    t154_0 = PNT(local_0);
    DLD();
    t158_0 = PNT(local_0);
    DLD();
    t162_0 = PNT(local_0);
    DLD();
    t166_0 = PNT(local_0);
    DLD();
    t170_0 = PNT(local_0);
    DLD();
    t174_0 = PNT(local_0);
    DLD();
    t178_0 = PNT(local_0);
    DLD();
    t182_0 = PNT(local_0);
    DLD();
    t186_0 = PNT(local_0);
    DLD();
    t190_0 = PNT(local_0);
    DLD();
    t194_0 = PNT(local_0);
    DLD();
    t198_0 = PNT(local_0);
    DLD();
    t202_0 = PNT(local_0);
    DLD();
    t206_0 = PNT(local_0);
    DLD();
    t210_0 = PNT(local_0);
    DLD();
    t214_0 = PNT(local_0);
    DLD();
    t218_0 = PNT(local_0);
    DLD();
    t222_0 = PNT(local_0);
    DLD();
    t226_0 = PNT(local_0);
    DLD();
    t230_0 = PNT(local_0);
    DLD();
    t234_0 = PNT(local_0);
    DLD();
    t238_0 = PNT(local_0);
    DLD();
    t242_0 = PNT(local_0);
    DLD();
    t246_0 = PNT(local_0);
    DLD();
    t250_0 = PNT(local_0);
    DLD();
    t254_0 = PNT(local_0);
    DLD();
    DLD();
    t263_0 = PNT(local_0);
    DLD();
    t267_0 = PNT(local_0);
    DLD();
    t271_0 = PNT(local_0);
    DLD();
    t275_0 = PNT(local_0);
    DLD();
    t279_0 = PNT(local_0);
    DLD();
    t283_0 = PNT(local_0);
    DLD();
    t287_0 = PNT(local_0);
    DLD();
    return;
}

void func_0291(void) {
    // Block 1 @291
    frnd(param_2);
    local_0 = param_2;
    if (!((local_0 < 0))) goto block_3; // @310
    // Block 2 @305
    local_0 = (-local_0);
    // Block 3 @310
    return;
    // Block 4 @313
    SC_P_Ai_SetMode(param_1, SC_P_AI_MODE_BATTLE);
    SC_P_Ai_EnableShooting(param_1, TRUE);
    SC_P_Ai_EnableSituationUpdate(param_1, 1);
    SC_Log(2036427856, param_1, 3);
    return;
    // Block 5 @332
    SC_P_Ai_SetMode(param_1, SC_P_AI_MODE_PEACE);
    SC_P_Ai_EnableShooting(param_1, FALSE);
    SC_P_Ai_EnableSituationUpdate(param_1, 0);
    SC_P_Ai_Stop(param_1);
    SC_Log(2036427856, param_1, 3);
    return;
}

void func_0354(void) {
    // Block 6 @354
    if (!(param_3)) goto block_8; // @357
    // Block 7 @356
    goto block_9; // @365
    // Block 8 @357
    SC_Log(1936942413, param_2, param_1, 4);
    return;
    // Block 9 @365
    SC_P_ScriptMessage(param_3, param_2, param_1);
    return;
}

void func_0371(void) {
    // Block 10 @371
    SC_P_GetBySideGroupMember(1, param_3, param_2);
    SC_P_Ai_GetSureEnemies(param_2);
    if (!(param_2)) goto block_12; // @388
    // Block 11 @385
    return;
    // Block 12 @388
    SC_P_GetBySideGroupMember(1, param_3, param_2);
    SC_P_Ai_GetDanger(param_2);
    if (!((param_2 > 0.5f))) goto block_14; // @407
    // Block 13 @404
    return;
    // Block 14 @407
    return;
    // Block 15 @410
    SC_P_Ai_GetSureEnemies(param_2);
    if (!(param_2)) goto block_17; // @420
    // Block 16 @417
    return;
    // Block 17 @420
    SC_P_Ai_GetDanger(param_2);
    if (!((param_2 > 0.5f))) goto block_19; // @432
    // Block 18 @429
    return;
    // Block 19 @432
    return;
    // Block 20 @435
    SC_ZeroMem(&local_0, 128);
    SC_P_Ai_GetProps(param_2, &local_0);
    local_0.disable_peace_crouch = param_1;
    SC_P_Ai_SetProps(param_2, &local_0);
    return;
    // Block 21 @454
    SC_ZeroMem(&local_0, 128);
    SC_P_Ai_GetProps(param_2, &local_0);
    local_0.hear_distance_mult = param_1;
    SC_P_Ai_SetProps(param_2, &local_0);
    return;
    // Block 22 @473
    SC_ZeroMem(&local_0, 128);
    SC_P_Ai_GetProps(param_2, &local_0);
    local_0.shoot_imprecision = (&local_0 * param_1);
    SC_P_Ai_SetProps(param_2, &local_0);
    return;
    // Block 23 @496
    SC_ZeroMem(&local_0, 128);
    SC_P_Ai_GetProps(param_2, &local_0);
    local_0.shoot_damage_mult = (&local_0 * param_1);
    SC_P_Ai_SetProps(param_2, &local_0);
    return;
    // Block 24 @519
    SC_ZeroMem(&local_0, 128);
    SC_P_Ai_GetProps(param_2, &local_0);
    if (!(param_1)) goto block_26; // @536
    // Block 25 @530
    local_0.grenade_sure_time = 5.0f;
    goto block_27; // @541
    // Block 26 @536
    local_0.grenade_sure_time = 1000.0f;
    // Block 27 @541
    SC_P_Ai_SetProps(param_2, &local_0);
    return;
    // Block 28 @546
    SC_ZeroMem(&local_0, 128);
    SC_P_Ai_GetProps(param_2, &local_0);
    local_0.berserk = param_1;
    SC_P_Ai_SetProps(param_2, &local_0);
    return;
    // Block 29 @565
    SC_ggi(SGI_CURRENTMISSION);
    return;
    // Block 30 @573
    SC_ggi(SGI_CHOPPER);
    return;
    // Block 31 @581
    SC_P_GetInfo(param_2, &local_0);
    return;
    // Block 32 @590
    SC_ZeroMem(&local_0, 128);
    SC_P_Ai_GetProps(param_2, &local_0);
    local_0 = param_1;
    SC_P_Ai_SetProps(param_2, &local_0);
    return;
    // Block 33 @608
    SC_ggi(101);
    param_1 = 1;
    if (!(&param_1)) goto block_35; // @623
    // Block 34 @622
    goto block_36; // @628
    // Block 35 @623
    param_1 = 1;
    // Block 36 @628
    if (!((&param_1 == 255))) goto block_38; // @639
    // Block 37 @634
    param_1 = 1;
    // Block 38 @639
    SC_ggi(102);
    param_1 = 128;
    if (!(&param_1)) goto block_40; // @654
    // Block 39 @653
    goto block_41; // @659
    // Block 40 @654
    param_1 = 128;
    // Block 41 @659
    if (!((&param_1 == 255))) goto block_43; // @670
    // Block 42 @665
    param_1 = 128;
    // Block 43 @670
    SC_ggi(103);
    param_1 = 1148846080;
    if (!(&param_1)) goto block_45; // @685
    // Block 44 @684
    goto block_50; // @720
    // Block 45 @685
    SC_ggi(SGI_CURRENTMISSION);
    if (!((200 == 12))) goto block_47; // @700
    // Block 46 @694
    param_1 = 1148846080;
    goto block_50; // @720
    // Block 47 @700
    SC_ggi(SGI_CURRENTMISSION);
    if (!((200 < 12))) goto block_49; // @715
    // Block 48 @709
    param_1 = 1148846080;
    goto block_50; // @720
    // Block 49 @715
    param_1 = 1148846080;
    // Block 50 @720
    if (!((&param_1 == 255))) goto block_52; // @731
    // Block 51 @726
    param_1 = 1148846080;
    // Block 52 @731
    SC_ggi(104);
    param_1 = 128;
    if (!((&param_1 == 255))) goto block_54; // @752
    // Block 53 @747
    param_1 = 128;
    // Block 54 @752
    SC_ggi(105);
    param_1 = 0;
    if (!(&param_1)) goto block_56; // @767
    // Block 55 @766
    goto block_57; // @772
    // Block 56 @767
    param_1 = 0;
    // Block 57 @772
    if (!((&param_1 == 255))) goto block_59; // @783
    // Block 58 @778
    param_1 = 0;
    // Block 59 @783
    SC_ggi(106);
    param_1 = 0;
    if (!((&param_1 == 255))) goto block_61; // @804
    // Block 60 @799
    param_1 = 0;
    // Block 61 @804
    SC_ggi(107);
    param_1 = 23;
    if (!((&param_1 == 255))) goto block_63; // @825
    // Block 62 @820
    param_1 = 23;
    // Block 63 @825
    SC_ggi(108);
    param_1 = 1;
    if (!(&param_1)) goto block_65; // @840
    // Block 64 @839
    goto block_66; // @845
    // Block 65 @840
    param_1 = 1;
    // Block 66 @845
    if (!((&param_1 == 255))) goto block_68; // @856
    // Block 67 @851
    param_1 = 1;
    // Block 68 @856
    SC_ggi(109);
    param_1 = 255;
    if (!((&param_1 == 255))) goto block_70; // @877
    // Block 69 @872
    param_1 = 255;
    // Block 70 @877
    param_1 = 255;
    return;
}

void func_0883(void) {
    // Block 71 @883
    SC_PC_Get();
    SC_P_GetWeapons();
    if (!(&local_0)) goto block_73; // @906
    // Block 72 @899
    SC_sgi();
    goto block_74; // @910
    // Block 73 @906
    SC_sgi(101, 255);
    // Block 74 @910
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    if (!(255)) goto block_76; // @921
    // Block 75 @914
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    SC_sgi(phi_74_0_14, 102);
    goto block_77; // @925
    // Block 76 @921
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    SC_sgi(102, 255);
    // Block 77 @925
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    if (!(255)) goto block_79; // @936
    // Block 78 @929
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    SC_sgi(phi_77_1_16, 103);
    goto block_80; // @940
    // Block 79 @936
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    SC_sgi(103, 255);
    // Block 80 @940
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    if (!(255)) goto block_82; // @951
    // Block 81 @944
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    SC_sgi(phi_80_2_18, 104);
    goto block_83; // @955
    // Block 82 @951
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    SC_sgi(104, 255);
    // Block 83 @955
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    if (!(255)) goto block_85; // @966
    // Block 84 @959
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    SC_sgi(phi_83_3_20, 105);
    goto block_86; // @970
    // Block 85 @966
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    SC_sgi(105, 255);
    // Block 86 @970
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    if (!(255)) goto block_88; // @981
    // Block 87 @974
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    SC_sgi(phi_86_4_22, 106);
    goto block_89; // @985
    // Block 88 @981
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    SC_sgi(106, 255);
    // Block 89 @985
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    if (!(255)) goto block_91; // @996
    // Block 90 @989
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    SC_sgi(phi_89_5_24, 107);
    goto block_92; // @1000
    // Block 91 @996
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    SC_sgi(107, 255);
    // Block 92 @1000
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    phi_92_6_26 = phi(b90:data_110, b91:data_111)
    if (!(255)) goto block_94; // @1011
    // Block 93 @1004
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    phi_92_6_26 = phi(b90:data_110, b91:data_111)
    SC_sgi(phi_92_6_26, 108);
    goto block_95; // @1015
    // Block 94 @1011
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    phi_92_6_26 = phi(b90:data_110, b91:data_111)
    SC_sgi(108, 255);
    // Block 95 @1015
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    phi_92_6_26 = phi(b90:data_110, b91:data_111)
    phi_95_7_28 = phi(b93:data_113, b94:data_114)
    if (!(255)) goto block_97; // @1026
    // Block 96 @1019
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    phi_92_6_26 = phi(b90:data_110, b91:data_111)
    phi_95_7_28 = phi(b93:data_113, b94:data_114)
    SC_sgi(phi_95_7_28, 109);
    goto block_98; // @1030
    // Block 97 @1026
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    phi_92_6_26 = phi(b90:data_110, b91:data_111)
    phi_95_7_28 = phi(b93:data_113, b94:data_114)
    SC_sgi(109, 255);
    // Block 98 @1030
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    phi_92_6_26 = phi(b90:data_110, b91:data_111)
    phi_95_7_28 = phi(b93:data_113, b94:data_114)
    phi_98_8_30 = phi(b96:data_116, b97:data_117)
    if (!(255)) goto block_100; // @1041
    // Block 99 @1034
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    phi_92_6_26 = phi(b90:data_110, b91:data_111)
    phi_95_7_28 = phi(b93:data_113, b94:data_114)
    phi_98_8_30 = phi(b96:data_116, b97:data_117)
    SC_sgi(phi_98_8_30, 110);
    goto block_101; // @1045
    // Block 100 @1041
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    phi_92_6_26 = phi(b90:data_110, b91:data_111)
    phi_95_7_28 = phi(b93:data_113, b94:data_114)
    phi_98_8_30 = phi(b96:data_116, b97:data_117)
    SC_sgi(110, 255);
    // Block 101 @1045
    phi_74_0_14 = phi(b72:data_92, b73:data_93)
    phi_77_1_16 = phi(b75:data_95, b76:data_96)
    phi_80_2_18 = phi(b78:data_98, b79:data_99)
    phi_83_3_20 = phi(b81:data_101, b82:data_102)
    phi_86_4_22 = phi(b84:data_104, b85:data_105)
    phi_89_5_24 = phi(b88:data_108, b87:data_107)
    phi_92_6_26 = phi(b90:data_110, b91:data_111)
    phi_95_7_28 = phi(b93:data_113, b94:data_114)
    phi_98_8_30 = phi(b96:data_116, b97:data_117)
    return;
    // Block 102 @1046
    SC_PC_Get();
    SC_P_ReadHealthFromGlobalVar();
    return;
}

void func_1054(void) {
    // Block 103 @1054
    SC_PC_Get();
    SC_P_WriteHealthToGlobalVar();
    return;
    // Block 104 @1062
    SC_PC_Get();
    SC_P_ReadAmmoFromGlobalVar();
    SC_ggi(90);
    if (!(90)) goto block_106; // @1090
    // Block 105 @1077
    SC_PC_Get();
    SC_ggi(90);
    SC_P_SetAmmoInWeap(89, 2, 90);
    // Block 106 @1090
    SC_ggi(91);
    if (!(91)) goto block_108; // @1110
    // Block 107 @1097
    SC_PC_Get();
    SC_ggi(91);
    SC_P_SetAmmoInWeap(90, 1, 91);
    // Block 108 @1110
    return;
}

void func_1111(void) {
    // Block 109 @1111
    SC_PC_Get();
    SC_P_WriteAmmoToGlobalVar();
    SC_PC_Get();
    SC_P_GetAmmoInWeap(90, 2);
    SC_sgi(90, 2);
    SC_PC_Get();
    SC_P_GetAmmoInWeap(91, 1);
    SC_sgi(91, 1);
    return;
}

void func_1146(void) {
    // Block 110 @1146
    SC_PC_GetIntel(&local_0);
    local_10 = 0;
    // Loop header - Block 111 @1155
    while (true) {  // loop body: blocks [111, 112]
        // Block 111 @1155
        if (!((local_10 < 10))) break;  // exit loop @1179
        // Block 112 @1159
        SC_sgi(&local_0, (50 + local_10));
        local_10 = (local_10 + 1);
        continue;  // back to loop header @1155
    }
    // Block 113 @1179
    return;
    // Block 114 @1180
    local_10 = 0;
    // Block 115 @1186
    if (!((local_10 < 10))) goto block_117; // @1214
    // Block 116 @1190
    t1193_0 = 50 + local_10;
    SC_ggi(t1193_0);
    (&local_0 + (local_10 * 4)) = t1193_0;
    local_10 = (local_10 + 1);
    goto block_115; // @1186
    // Block 117 @1214
    SC_PC_SetIntel(&local_0);
    return;
    // Block 118 @1218
    SC_MissionCompleted();
    return;
}

void func_1223(void) {
    // Block 119 @1223
    SC_Osi(&"MISSION COMPLETE", 1);
    SC_MissionDone();
    return;
    // Block 120 @1233
    SC_ShowHelp(&param_1, 1, 6.0f);
    return;
    // Block 121 @1239
    param_2 = (&local_0 + 0);
    param_1 = (&local_0 + 4);
    SC_ShowHelp(&local_0, 2, 12.0f);
    return;
    // Block 122 @1258
    param_3 = (&local_0 + 0);
    param_2 = (&local_0 + 4);
    param_1 = (&local_0 + 8);
    SC_ShowHelp(&local_0, 3, 24.0f);
    return;
    // Block 123 @1283
    SC_ggi(SGI_DIFFICULTY);
    return;
    // Block 124 @1291
    rand();
    local_0 = (unknown_124_1297_1 % 20);
    SC_ggi(SGI_CURRENTMISSION);
    if (!((200 > 12))) goto block_139; // @1356
    // Block 125 @1310
    if (!((local_0 > 19))) goto block_127; // @1317
    // Block 126 @1314
    return;
    // Block 127 @1317
    if (!((local_0 > 18))) goto block_129; // @1324
    // Block 128 @1321
    return;
    // Block 129 @1324
    if (!((local_0 > 17))) goto block_131; // @1331
    // Block 130 @1328
    return;
    // Block 131 @1331
    if (!((local_0 > 11))) goto block_133; // @1338
    // Block 132 @1335
    return;
    // Block 133 @1338
    if (!((local_0 > 8))) goto block_135; // @1345
    // Block 134 @1342
    return;
    // Block 135 @1345
    if (!((local_0 > 3))) goto block_137; // @1352
    // Block 136 @1349
    return;
    // Block 137 @1352
    return;
    // Block 138 @1355
    goto block_152; // @1401
    // Block 139 @1356
    if (!((local_0 > 19))) goto block_141; // @1363
    // Block 140 @1360
    return;
    // Block 141 @1363
    if (!((local_0 > 16))) goto block_143; // @1370
    // Block 142 @1367
    return;
    // Block 143 @1370
    if (!((local_0 > 13))) goto block_145; // @1377
    // Block 144 @1374
    return;
    // Block 145 @1377
    if (!((local_0 > 9))) goto block_147; // @1384
    // Block 146 @1381
    return;
    // Block 147 @1384
    if (!((local_0 > 6))) goto block_149; // @1391
    // Block 148 @1388
    return;
    // Block 149 @1391
    if (!((local_0 > 3))) goto block_151; // @1398
    // Block 150 @1395
    return;
    // Block 151 @1398
    return;
    // Block 152 @1401
    rand();
    local_0 = (unknown_152_1407_1 % 20);
    if (!((local_0 > 18))) goto block_154; // @1418
    // Block 153 @1415
    return;
    // Block 154 @1418
    if (!((local_0 > 16))) goto block_156; // @1425
    // Block 155 @1422
    return;
    // Block 156 @1425
    if (!((local_0 > 12))) goto block_158; // @1432
    // Block 157 @1429
    return;
    // Block 158 @1432
    if (!((local_0 > 8))) goto block_160; // @1439
    // Block 159 @1436
    return;
    // Block 160 @1439
    return;
    // Block 161 @1442
    rand();
    local_0 = (unknown_161_1448_1 % 20);
    SC_ggi(SGI_CURRENTMISSION);
    goto block_163; // @1464
    // Block 162 @1460
    if (!((local_1 == 1))) goto block_167; // @1476
    // Block 163 @1464
    if (!((local_0 > 10))) goto block_165; // @1471
    // Block 164 @1468
    return;
    // Block 165 @1471
    return;
    // Block 166 @1474
    goto block_168; // @1480
    // Block 167 @1476
    if (!((local_1 == 2))) goto block_169; // @1481
    // Block 168 @1480
    goto block_170; // @1485
    // Block 169 @1481
    if (!((local_1 == 3))) goto block_171; // @1486
    // Block 170 @1485
    goto block_172; // @1490
    // Block 171 @1486
    if (!((local_1 == 4))) goto block_173; // @1491
    // Block 172 @1490
    goto block_174; // @1495
    // Block 173 @1491
    if (!((local_1 == 5))) goto block_180; // @1514
    // Block 174 @1495
    if (!((local_0 > 12))) goto block_176; // @1502
    // Block 175 @1499
    return;
    // Block 176 @1502
    if (!((local_0 > 8))) goto block_178; // @1509
    // Block 177 @1506
    return;
    // Block 178 @1509
    return;
    // Block 179 @1512
    goto block_181; // @1518
    // Block 180 @1514
    if (!((local_1 == 16))) goto block_182; // @1519
    // Block 181 @1518
    goto block_183; // @1523
    // Block 182 @1519
    if (!((local_1 == 17))) goto block_191; // @1549
    // Block 183 @1523
    if (!((local_0 > 14))) goto block_185; // @1530
    // Block 184 @1527
    return;
    // Block 185 @1530
    if (!((local_0 > 10))) goto block_187; // @1537
    // Block 186 @1534
    return;
    // Block 187 @1537
    if (!((local_0 > 5))) goto block_189; // @1544
    // Block 188 @1541
    return;
    // Block 189 @1544
    return;
    // Block 190 @1547
    goto block_192; // @1553
    // Block 191 @1549
    if (!((local_1 == 6))) goto block_202; // @1586
    // Block 192 @1553
    if (!((local_0 > 15))) goto block_194; // @1560
    // Block 193 @1557
    return;
    // Block 194 @1560
    if (!((local_0 > 11))) goto block_196; // @1567
    // Block 195 @1564
    return;
    // Block 196 @1567
    if (!((local_0 > 7))) goto block_198; // @1574
    // Block 197 @1571
    return;
    // Block 198 @1574
    if (!((local_0 > 2))) goto block_200; // @1581
    // Block 199 @1578
    return;
    // Block 200 @1581
    return;
    // Block 201 @1584
    goto block_203; // @1590
    // Block 202 @1586
    if (!((local_1 == 7))) goto block_204; // @1591
    // Block 203 @1590
    goto block_205; // @1595
    // Block 204 @1591
    if (!((local_1 == 8))) goto block_206; // @1596
    // Block 205 @1595
    goto block_207; // @1600
    // Block 206 @1596
    if (!((local_1 == 10))) goto block_217; // @1633
    // Block 207 @1600
    if (!((local_0 > 16))) goto block_209; // @1607
    // Block 208 @1604
    return;
    // Block 209 @1607
    if (!((local_0 > 12))) goto block_211; // @1614
    // Block 210 @1611
    return;
    // Block 211 @1614
    if (!((local_0 > 8))) goto block_213; // @1621
    // Block 212 @1618
    return;
    // Block 213 @1621
    if (!((local_0 > 4))) goto block_215; // @1628
    // Block 214 @1625
    return;
    // Block 215 @1628
    return;
    // Block 216 @1631
    goto block_218; // @1637
    // Block 217 @1633
    if (!((local_1 == 9))) goto block_219; // @1638
    // Block 218 @1637
    goto block_220; // @1642
    // Block 219 @1638
    if (!((local_1 == 11))) goto block_221; // @1643
    // Block 220 @1642
    goto block_222; // @1647
    // Block 221 @1643
    if (!((local_1 == 23))) goto block_228; // @1666
    // Block 222 @1647
    if (!((local_0 > 13))) goto block_224; // @1654
    // Block 223 @1651
    return;
    // Block 224 @1654
    if (!((local_0 > 6))) goto block_226; // @1661
    // Block 225 @1658
    return;
    // Block 226 @1661
    return;
    // Block 227 @1664
    goto block_229; // @1670
    // Block 228 @1666
    if (!((local_1 == 12))) goto block_241; // @1710
    // Block 229 @1670
    if (!((local_0 > 15))) goto block_231; // @1677
    // Block 230 @1674
    return;
    // Block 231 @1677
    if (!((local_0 > 11))) goto block_233; // @1684
    // Block 232 @1681
    return;
    // Block 233 @1684
    if (!((local_0 > 8))) goto block_235; // @1691
    // Block 234 @1688
    return;
    // Block 235 @1691
    if (!((local_0 > 4))) goto block_237; // @1698
    // Block 236 @1695
    return;
    // Block 237 @1698
    if (!((local_0 > 1))) goto block_239; // @1705
    // Block 238 @1702
    return;
    // Block 239 @1705
    return;
    // Block 240 @1708
    goto block_242; // @1714
    // Block 241 @1710
    if (!((local_1 == 13))) goto block_243; // @1715
    // Block 242 @1714
    goto block_244; // @1719
    // Block 243 @1715
    if (!((local_1 == 14))) goto block_245; // @1720
    // Block 244 @1719
    goto block_246; // @1724
    // Block 245 @1720
    if (!((local_1 == 15))) goto block_247; // @1725
    // Block 246 @1724
    goto block_248; // @1729
    // Block 247 @1725
    if (!((local_1 == 18))) goto block_260; // @1768
    // Block 248 @1729
    if (!((local_0 > 15))) goto block_250; // @1736
    // Block 249 @1733
    return;
    // Block 250 @1736
    if (!((local_0 > 11))) goto block_252; // @1743
    // Block 251 @1740
    return;
    // Block 252 @1743
    if (!((local_0 > 8))) goto block_254; // @1750
    // Block 253 @1747
    return;
    // Block 254 @1750
    if (!((local_0 > 5))) goto block_256; // @1757
    // Block 255 @1754
    return;
    // Block 256 @1757
    if (!((local_0 > 2))) goto block_258; // @1764
    // Block 257 @1761
    return;
    // Block 258 @1764
    return;
    // Block 259 @1767
    goto block_261; // @1772
    // Block 260 @1768
    if (!((local_1 == 19))) goto block_262; // @1773
    // Block 261 @1772
    goto block_263; // @1777
    // Block 262 @1773
    if (!((local_1 == 20))) goto block_264; // @1778
    // Block 263 @1777
    goto block_265; // @1782
    // Block 264 @1778
    if (!((local_1 == 21))) goto block_266; // @1783
    // Block 265 @1782
    goto block_267; // @1787
    // Block 266 @1783
    if (!((local_1 == 22))) goto block_275; // @1813
    // Block 267 @1787
    if (!((local_0 > 14))) goto block_269; // @1794
    // Block 268 @1791
    return;
    // Block 269 @1794
    if (!((local_0 > 10))) goto block_271; // @1801
    // Block 270 @1798
    return;
    // Block 271 @1801
    if (!((local_0 > 4))) goto block_273; // @1808
    // Block 272 @1805
    return;
    // Block 273 @1808
    return;
    // Block 274 @1811
    goto block_276; // @1817
    // Block 275 @1813
    if (!((local_1 == 24))) goto block_288; // @1857
    // Block 276 @1817
    if (!((local_0 > 15))) goto block_278; // @1824
    // Block 277 @1821
    return;
    // Block 278 @1824
    if (!((local_0 > 11))) goto block_280; // @1831
    // Block 279 @1828
    return;
    // Block 280 @1831
    if (!((local_0 > 8))) goto block_282; // @1838
    // Block 281 @1835
    return;
    // Block 282 @1838
    if (!((local_0 > 4))) goto block_284; // @1845
    // Block 283 @1842
    return;
    // Block 284 @1845
    if (!((local_0 > 1))) goto block_286; // @1852
    // Block 285 @1849
    return;
    // Block 286 @1852
    return;
    // Block 287 @1855
    goto block_289; // @1861
    // Block 288 @1857
    if (!((local_1 == 26))) goto block_290; // @1862
    // Block 289 @1861
    goto block_291; // @1866
    // Block 290 @1862
    if (!((local_1 == 27))) goto block_292; // @1867
    // Block 291 @1866
    goto block_293; // @1871
    // Block 292 @1867
    if (!((local_1 == 28))) goto block_303; // @1905
    // Block 293 @1871
    if (!((local_0 > 14))) goto block_295; // @1878
    // Block 294 @1875
    return;
    // Block 295 @1878
    if (!((local_0 > 10))) goto block_297; // @1885
    // Block 296 @1882
    return;
    // Block 297 @1885
    if (!((local_0 > 7))) goto block_299; // @1892
    // Block 298 @1889
    return;
    // Block 299 @1892
    if (!((local_0 > 3))) goto block_301; // @1899
    // Block 300 @1896
    return;
    // Block 301 @1899
    return;
    // Block 302 @1902
    goto block_304; // @1909
    // Block 303 @1905
    if (!((local_1 == 29))) goto block_314; // @1942
    // Block 304 @1909
    if (!((local_0 > 14))) goto block_306; // @1916
    // Block 305 @1913
    return;
    // Block 306 @1916
    if (!((local_0 > 11))) goto block_308; // @1923
    // Block 307 @1920
    return;
    // Block 308 @1923
    if (!((local_0 > 8))) goto block_310; // @1930
    // Block 309 @1927
    return;
    // Block 310 @1930
    if (!((local_0 > 3))) goto block_312; // @1937
    // Block 311 @1934
    return;
    // Block 312 @1937
    return;
    // Block 313 @1940
    goto block_315; // @1946
    // Block 314 @1942
    if (!((local_1 == 25))) goto block_319; // @1958
    // Block 315 @1946
    if (!((local_0 > 2))) goto block_317; // @1953
    // Block 316 @1950
    return;
    // Block 317 @1953
    return;
    // Block 318 @1956
    goto block_320; // @1962
    // Block 319 @1958
    if (!((local_1 == 30))) goto block_321; // @1963
    // Block 320 @1962
    goto block_322; // @1967
    // Block 321 @1963
    if (!((local_1 == 31))) goto block_323; // @1968
    // Block 322 @1967
    goto block_324; // @1972
    // Block 323 @1968
    if (!((local_1 == 32))) goto block_336; // @2011
    // Block 324 @1972
    if (!((local_0 > 13))) goto block_326; // @1979
    // Block 325 @1976
    return;
    // Block 326 @1979
    if (!((local_0 > 11))) goto block_328; // @1986
    // Block 327 @1983
    return;
    // Block 328 @1986
    if (!((local_0 > 7))) goto block_330; // @1993
    // Block 329 @1990
    return;
    // Block 330 @1993
    if (!((local_0 > 4))) goto block_332; // @2000
    // Block 331 @1997
    return;
    // Block 332 @2000
    if (!((local_0 > 1))) goto block_334; // @2007
    // Block 333 @2004
    return;
    // Block 334 @2007
    return;
    // Block 335 @2010
    goto block_336; // @2011
    // Block 336 @2011
    return;
    // Block 337 @2015
    rand();
    local_0 = (unknown_337_2021_1 % 20);
    SC_ggi(SGI_CURRENTMISSION);
    goto block_339; // @2037
    // Block 338 @2033
    if (!((local_1 == 1))) goto block_340; // @2038
    // Block 339 @2037
    goto block_341; // @2042
    // Block 340 @2038
    if (!((local_1 == 16))) goto block_342; // @2043
    // Block 341 @2042
    goto block_343; // @2047
    // Block 342 @2043
    if (!((local_1 == 17))) goto block_344; // @2048
    // Block 343 @2047
    goto block_345; // @2052
    // Block 344 @2048
    if (!((local_1 == 6))) goto block_351; // @2071
    // Block 345 @2052
    if (!((local_0 > 13))) goto block_347; // @2059
    // Block 346 @2056
    return;
    // Block 347 @2059
    if (!((local_0 > 6))) goto block_349; // @2066
    // Block 348 @2063
    return;
    // Block 349 @2066
    return;
    // Block 350 @2069
    goto block_352; // @2075
    // Block 351 @2071
    if (!((local_1 == 2))) goto block_353; // @2076
    // Block 352 @2075
    goto block_354; // @2080
    // Block 353 @2076
    if (!((local_1 == 3))) goto block_355; // @2081
    // Block 354 @2080
    goto block_356; // @2085
    // Block 355 @2081
    if (!((local_1 == 4))) goto block_357; // @2086
    // Block 356 @2085
    goto block_358; // @2090
    // Block 357 @2086
    if (!((local_1 == 5))) goto block_359; // @2091
    // Block 358 @2090
    goto block_360; // @2095
    // Block 359 @2091
    if (!((local_1 == 7))) goto block_361; // @2096
    // Block 360 @2095
    goto block_362; // @2100
    // Block 361 @2096
    if (!((local_1 == 8))) goto block_363; // @2101
    // Block 362 @2100
    goto block_364; // @2105
    // Block 363 @2101
    if (!((local_1 == 10))) goto block_370; // @2124
    // Block 364 @2105
    if (!((local_0 > 13))) goto block_366; // @2112
    // Block 365 @2109
    return;
    // Block 366 @2112
    if (!((local_0 > 6))) goto block_368; // @2119
    // Block 367 @2116
    return;
    // Block 368 @2119
    return;
    // Block 369 @2122
    goto block_371; // @2128
    // Block 370 @2124
    if (!((local_1 == 9))) goto block_372; // @2129
    // Block 371 @2128
    goto block_373; // @2133
    // Block 372 @2129
    if (!((local_1 == 11))) goto block_374; // @2134
    // Block 373 @2133
    goto block_375; // @2138
    // Block 374 @2134
    if (!((local_1 == 12))) goto block_376; // @2139
    // Block 375 @2138
    goto block_377; // @2143
    // Block 376 @2139
    if (!((local_1 == 13))) goto block_378; // @2144
    // Block 377 @2143
    goto block_379; // @2148
    // Block 378 @2144
    if (!((local_1 == 14))) goto block_380; // @2149
    // Block 379 @2148
    goto block_381; // @2153
    // Block 380 @2149
    if (!((local_1 == 15))) goto block_382; // @2154
    // Block 381 @2153
    goto block_383; // @2158
    // Block 382 @2154
    if (!((local_1 == 24))) goto block_391; // @2184
    // Block 383 @2158
    if (!((local_0 > 15))) goto block_385; // @2165
    // Block 384 @2162
    return;
    // Block 385 @2165
    if (!((local_0 > 10))) goto block_387; // @2172
    // Block 386 @2169
    return;
    // Block 387 @2172
    if (!((local_0 > 5))) goto block_389; // @2179
    // Block 388 @2176
    return;
    // Block 389 @2179
    return;
    // Block 390 @2182
    goto block_392; // @2188
    // Block 391 @2184
    if (!((local_1 == 18))) goto block_393; // @2189
    // Block 392 @2188
    goto block_394; // @2193
    // Block 393 @2189
    if (!((local_1 == 19))) goto block_395; // @2194
    // Block 394 @2193
    goto block_396; // @2198
    // Block 395 @2194
    if (!((local_1 == 20))) goto block_397; // @2199
    // Block 396 @2198
    goto block_398; // @2203
    // Block 397 @2199
    if (!((local_1 == 21))) goto block_399; // @2204
    // Block 398 @2203
    goto block_400; // @2208
    // Block 399 @2204
    if (!((local_1 == 26))) goto block_401; // @2209
    // Block 400 @2208
    goto block_402; // @2213
    // Block 401 @2209
    if (!((local_1 == 27))) goto block_403; // @2214
    // Block 402 @2213
    goto block_404; // @2218
    // Block 403 @2214
    if (!((local_1 == 28))) goto block_410; // @2237
    // Block 404 @2218
    if (!((local_0 > 13))) goto block_406; // @2225
    // Block 405 @2222
    return;
    // Block 406 @2225
    if (!((local_0 > 6))) goto block_408; // @2232
    // Block 407 @2229
    return;
    // Block 408 @2232
    return;
    // Block 409 @2235
    goto block_411; // @2241
    // Block 410 @2237
    if (!((local_1 == 22))) goto block_412; // @2242
    // Block 411 @2241
    goto block_413; // @2246
    // Block 412 @2242
    if (!((local_1 == 23))) goto block_414; // @2247
    // Block 413 @2246
    goto block_415; // @2251
    // Block 414 @2247
    if (!((local_1 == 25))) goto block_416; // @2252
    // Block 415 @2251
    goto block_417; // @2256
    // Block 416 @2252
    if (!((local_1 == 29))) goto block_418; // @2257
    // Block 417 @2256
    goto block_419; // @2261
    // Block 418 @2257
    if (!((local_1 == 30))) goto block_420; // @2262
    // Block 419 @2261
    goto block_421; // @2266
    // Block 420 @2262
    if (!((local_1 == 31))) goto block_422; // @2267
    // Block 421 @2266
    goto block_423; // @2271
    // Block 422 @2267
    if (!((local_1 == 32))) goto block_429; // @2289
    // Block 423 @2271
    if (!((local_0 > 12))) goto block_425; // @2278
    // Block 424 @2275
    return;
    // Block 425 @2278
    if (!((local_0 > 4))) goto block_427; // @2285
    // Block 426 @2282
    return;
    // Block 427 @2285
    return;
    // Block 428 @2288
    goto block_429; // @2289
    // Block 429 @2289
    return;
    // Block 430 @2293
    local_0 = 0;
    // Block 431 @2298
    if (!((local_0 < 8))) goto block_433; // @2329
    // Block 432 @2302
    param_1 = (&"e" + (local_0 * 4));
    param_1 = (&"<" + (local_0 * 4));
    local_0 = (local_0 + 1);
    goto block_431; // @2298
    // Block 433 @2329
    SC_ggi(SGI_CURRENTMISSION);
    goto block_435; // @2341
    // Block 434 @2337
    if (!((local_1 == 1))) goto block_436; // @2357
    // Block 435 @2341
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    goto block_437; // @2361
    // Block 436 @2357
    if (!((local_1 == 2))) goto block_438; // @2362
    // Block 437 @2361
    goto block_439; // @2366
    // Block 438 @2362
    if (!((local_1 == 3))) goto block_440; // @2367
    // Block 439 @2366
    goto block_441; // @2371
    // Block 440 @2367
    if (!((local_1 == 4))) goto block_442; // @2372
    // Block 441 @2371
    goto block_443; // @2376
    // Block 442 @2372
    if (!((local_1 == 5))) goto block_444; // @2392
    // Block 443 @2376
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    goto block_445; // @2396
    // Block 444 @2392
    if (!((local_1 == 16))) goto block_446; // @2397
    // Block 445 @2396
    goto block_447; // @2401
    // Block 446 @2397
    if (!((local_1 == 17))) goto block_448; // @2424
    // Block 447 @2401
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    goto block_449; // @2428
    // Block 448 @2424
    if (!((local_1 == 6))) goto block_450; // @2451
    // Block 449 @2428
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    goto block_451; // @2455
    // Block 450 @2451
    if (!((local_1 == 7))) goto block_452; // @2456
    // Block 451 @2455
    goto block_453; // @2460
    // Block 452 @2456
    if (!((local_1 == 8))) goto block_454; // @2483
    // Block 453 @2460
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    goto block_455; // @2487
    // Block 454 @2483
    if (!((local_1 == 9))) goto block_456; // @2488
    // Block 455 @2487
    goto block_457; // @2492
    // Block 456 @2488
    if (!((local_1 == 11))) goto block_458; // @2493
    // Block 457 @2492
    goto block_459; // @2497
    // Block 458 @2493
    if (!((local_1 == 10))) goto block_460; // @2513
    // Block 459 @2497
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    goto block_461; // @2517
    // Block 460 @2513
    if (!((local_1 == 12))) goto block_462; // @2554
    // Block 461 @2517
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    param_1 = (&"e" + 12);
    param_1 = (&"e" + 16);
    goto block_463; // @2558
    // Block 462 @2554
    if (!((local_1 == 13))) goto block_464; // @2559
    // Block 463 @2558
    goto block_465; // @2563
    // Block 464 @2559
    if (!((local_1 == 14))) goto block_466; // @2564
    // Block 465 @2563
    goto block_467; // @2568
    // Block 466 @2564
    if (!((local_1 == 15))) goto block_468; // @2584
    // Block 467 @2568
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    goto block_469; // @2588
    // Block 468 @2584
    if (!((local_1 == 18))) goto block_470; // @2589
    // Block 469 @2588
    goto block_471; // @2593
    // Block 470 @2589
    if (!((local_1 == 19))) goto block_472; // @2594
    // Block 471 @2593
    goto block_473; // @2598
    // Block 472 @2594
    if (!((local_1 == 20))) goto block_474; // @2621
    // Block 473 @2598
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    goto block_475; // @2625
    // Block 474 @2621
    if (!((local_1 == 21))) goto block_476; // @2655
    // Block 475 @2625
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    param_1 = (&"e" + 12);
    goto block_477; // @2659
    // Block 476 @2655
    if (!((local_1 == 22))) goto block_478; // @2660
    // Block 477 @2659
    goto block_479; // @2664
    // Block 478 @2660
    if (!((local_1 == 23))) goto block_480; // @2701
    // Block 479 @2664
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    param_1 = (&"e" + 12);
    param_1 = (&"e" + 16);
    goto block_481; // @2705
    // Block 480 @2701
    if (!((local_1 == 24))) goto block_482; // @2721
    // Block 481 @2705
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    goto block_483; // @2725
    // Block 482 @2721
    if (!((local_1 == 26))) goto block_484; // @2726
    // Block 483 @2725
    goto block_485; // @2730
    // Block 484 @2726
    if (!((local_1 == 27))) goto block_486; // @2731
    // Block 485 @2730
    goto block_487; // @2735
    // Block 486 @2731
    if (!((local_1 == 28))) goto block_488; // @2765
    // Block 487 @2735
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    param_1 = (&"e" + 12);
    goto block_489; // @2769
    // Block 488 @2765
    if (!((local_1 == 25))) goto block_490; // @2792
    // Block 489 @2769
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    goto block_491; // @2796
    // Block 490 @2792
    if (!((local_1 == 29))) goto block_492; // @2826
    // Block 491 @2796
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    param_1 = (&"e" + 12);
    goto block_493; // @2830
    // Block 492 @2826
    if (!((local_1 == 30))) goto block_494; // @2831
    // Block 493 @2830
    goto block_495; // @2835
    // Block 494 @2831
    if (!((local_1 == 31))) goto block_496; // @2836
    // Block 495 @2835
    goto block_497; // @2840
    // Block 496 @2836
    if (!((local_1 == 32))) goto block_499; // @2907
    // Block 497 @2840
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    param_1 = (&"e" + 12);
    goto block_498; // @2870
    // Block 498 @2870
    param_1 = (&"e" + 0);
    param_1 = (&"e" + 4);
    param_1 = (&"e" + 8);
    param_1 = (&"e" + 12);
    param_1 = (&"e" + 16);
    goto block_500; // @2908
    // Block 499 @2907
    goto block_498; // @2870
    // Block 500 @2908
    return;
    // Block 501 @2910
    local_32.z = 100.0f;
    SC_ggi(SGI_GAMETYPE);
    if (!(11)) goto block_514; // @3016
    // Block 502 @2928
    SC_P_GetPos(param_3, &local_131);
    SC_MP_EnumPlayers(&local_0, &local_134, 0);
    if (!(local_134)) goto block_504; // @2944
    // Block 503 @2943
    goto block_505; // @2947
    // Block 504 @2944
    return;
    // Block 505 @2947
    local_135 = 0;
    // Block 506 @2951
    if (!((local_135 < local_134))) goto block_511; // @3006
    // Block 507 @2955
    if (!((0 == 1))) goto block_510; // @2997
    // Block 508 @2965
    SC_P_GetPos(&local_134, &local_32);
    SC_2VectorsDist(&local_32, &local_131);
    local_131 = &local_137;
    if (!((local_137 < local_32.z))) goto block_510; // @2997
    // Block 509 @2988
    local_32.z = local_137;
    local_32 = param_2;
    // Block 510 @2997
    local_135 = (local_135 + 1);
    goto block_506; // @2951
    // Block 511 @3006
    if (!((local_32.z < 100.0f))) goto block_513; // @3013
    // Block 512 @3010
    return;
    // Block 513 @3013
    return;
    // Block 514 @3016
    SC_PC_GetPos(param_2);
    SC_2VectorsDist(&local_32, &local_131);
    local_131 = &local_32.z;
    if (!((local_32.z < 100.0f))) goto block_516; // @3040
    // Block 515 @3037
    return;
    // Block 516 @3040
    return;
    // Block 517 @3043
    SC_GetGroupPlayers(param_3, param_2);
    local_1 = param_2;
    local_0 = 0;
    // Block 518 @3059
    if (!((local_0 < local_1))) goto block_523; // @3090
    // Block 519 @3063
    SC_P_GetBySideGroupMember(param_3, param_2, local_0);
    SC_P_IsReady(local_0);
    if (!(local_0)) goto block_522; // @3081
    // Block 520 @3077
    goto block_521; // @3078
    // Block 521 @3078
    return;
    // Block 522 @3081
    local_0 = (local_0 + 1);
    goto block_518; // @3059
    // Block 523 @3090
    return;
    // Block 524 @3093
    SC_GetGroupPlayers(param_3, param_2);
    local_1 = param_2;
    local_0 = 0;
    // Block 525 @3109
    if (!((local_0 < local_1))) goto block_532; // @3155
    // Block 526 @3113
    SC_P_GetBySideGroupMember(param_3, param_2, local_0);
    SC_P_IsReady(local_0);
    if (!(local_0)) goto block_531; // @3146
    // Block 527 @3127
    goto block_528; // @3128
    // Block 528 @3128
    SC_P_GetBySideGroupMember(param_3, param_2, local_0);
    SC_P_GetActive(local_0);
    if (!(local_0)) goto block_531; // @3146
    // Block 529 @3142
    goto block_530; // @3143
    // Block 530 @3143
    return;
    // Block 531 @3146
    local_0 = (local_0 + 1);
    goto block_525; // @3109
    // Block 532 @3155
    return;
    // Block 533 @3158
    SC_GetGroupPlayers(1, param_2);
    local_1.y = param_2;
    local_0 = 0;
    // Block 534 @3177
    if (!((local_0 < local_1.y))) goto block_541; // @3235
    // Block 535 @3181
    SC_P_GetBySideGroupMember(1, param_2, local_0);
    local_1 = local_0;
    if (!(local_1)) goto block_540; // @3226
    // Block 536 @3194
    SC_P_Ai_GetDanger(local_1);
    local_1.z = local_1;
    if (!((local_1.z > 2.0f))) goto block_538; // @3210
    // Block 537 @3207
    return;
    // Block 538 @3210
    SC_P_Ai_GetSureEnemies(local_1);
    local_1 = local_1;
    if (!((local_1 > 0))) goto block_540; // @3226
    // Block 539 @3223
    return;
    // Block 540 @3226
    local_0 = (local_0 + 1);
    goto block_534; // @3177
    // Block 541 @3235
    return;
    // Block 542 @3238
    local_0 = 1;
    // Block 543 @3247
    if (!((local_0 < 6))) goto block_550; // @3305
    // Block 544 @3251
    SC_P_GetBySideGroupMember(0, 0, local_0);
    local_1 = local_0;
    if (!(local_1)) goto block_549; // @3296
    // Block 545 @3264
    SC_P_Ai_GetDanger(local_1);
    local_1.z = local_1;
    if (!((local_1.z > 2.0f))) goto block_547; // @3280
    // Block 546 @3277
    return;
    // Block 547 @3280
    SC_P_Ai_GetSureEnemies(local_1);
    local_1 = local_1;
    if (!((local_1 > 0))) goto block_549; // @3296
    // Block 548 @3293
    return;
    // Block 549 @3296
    local_0 = (local_0 + 1);
    goto block_543; // @3247
    // Block 550 @3305
    return;
    // Block 551 @3308
    local_0 = 0;
    // Block 552 @3317
    if (!((local_0 < 6))) goto block_557; // @3365
    // Block 553 @3321
    SC_P_GetBySideGroupMember(0, 0, local_0);
    local_6 = local_0;
    if (!(local_6)) goto block_556; // @3356
    // Block 554 @3334
    SC_P_GetPos(local_6, &local_1);
    SC_2VectorsDist(param_2, &local_1);
    local_1 = &local_5;
    if (!((local_5 < local_1))) goto block_556; // @3356
    // Block 555 @3352
    local_1 = local_5;
    // Block 556 @3356
    local_0 = (local_0 + 1);
    goto block_552; // @3317
    // Block 557 @3365
    return;
}

void func_3368(void) {
    // Block 558 @3368
    SC_NOD_Get(0, param_2);
    local_0 = param_2;
    if (!((local_0 != 0))) goto block_560; // @3387
    // Block 559 @3383
    SC_NOD_GetWorldPos(local_0, param_1);
    // Block 560 @3387
    return;
    // Block 561 @3388
    SC_NOD_Get(0, param_2);
    local_0 = param_2;
    if (!((local_0 != 0))) goto block_563; // @3411
    // Block 562 @3403
    SC_NOD_GetWorldRotZ(local_0);
    return;
    // Block 563 @3411
    return;
    // Block 564 @3414
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_GetPeaceMode(1);
    if (!((1 == 2))) goto block_566; // @3441
    // Block 565 @3430
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_SetPeaceMode(1, 0);
    // Block 566 @3441
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_Stop(1);
    return;
    // Block 567 @3452
    SC_DoExplosion(&local_0, param_1);
    return;
    // Block 568 @3462
    SC_NOD_Get(0, param_1);
    local_3.coveramount = param_1;
    if (!(local_3.coveramount)) goto block_570; // @3479
    // Block 569 @3478
    goto block_571; // @3484
    // Block 570 @3479
    SC_message(&"FATAL! Claymore %s not found!!!!!!", 1);
    return;
    // Block 571 @3484
    SC_NOD_GetWorldPos(local_3.coveramount, &local_1);
    SC_NOD_GetWorldRotZ(local_3.coveramount);
    local_0 = local_3.coveramount;
    local_0 = (local_0 - 1.57f);
    local_1 = &local_1;
    cos(local_0);
    local_1 = (local_3.coveramount - (2.0f * local_0));
    sin(local_0);
    local_1.y = (0 + (2.0f * local_0));
    SC_DoExplosion(&local_1, 1);
    local_1 = 1;
    cos(local_0);
    local_1 = (&local_1 - (4.0f * local_0));
    sin(local_0);
    local_1.y = (unknown_571_3572_1 + (4.0f * local_0));
    SC_DoExplosion(&local_1, 2);
    local_1 = 2;
    cos(local_0);
    local_1 = (&local_1 - (8.0f * local_0));
    sin(local_0);
    local_1.y = (unknown_571_3611_1 + (8.0f * local_0));
    SC_DoExplosion(&local_1, 3);
    SC_DUMMY_Set_DoNotRenHier2(local_3.coveramount, 1);
    return;
    // Block 572 @3625
    local_1 = &local_1.z;
    local_0 = 0;
    // Block 573 @3643
    if (!((local_0 < param_2))) goto block_575; // @3686
    // Block 574 @3647
    frnd(param_1);
    local_1 = (param_4 + param_1);
    frnd(param_1);
    local_1.y = (unknown_574_3668_1 + param_1);
    SC_DoExplosion(&local_1, param_3);
    local_0 = (local_0 + 1);
    goto block_573; // @3643
    // Block 575 @3686
    return;
    // Block 576 @3687
    SC_GetWp(param_2, &local_0);
    SC_DoExplosion(&local_0, param_1);
    return;
    // Block 577 @3701
    SC_GetWp(param_1, &local_0);
    SC_CreatePtc(176, &local_0);
    return;
    // Block 578 @3715
    SC_GetWp(param_1, &local_0);
    SC_DoExplosion(&local_0, 3);
    SC_SND_PlaySound3D(2965, &local_0);
    SC_NOD_Get(0, param_1);
    SC_CreatePtc_Ext(0, param_1, 1000.0f, 0.0f, 1.0f, 1.0f);
    SC_NOD_Get(0, param_1);
    SC_CreatePtc_Ext(0, param_1, 1000.0f, 0.0f, 1.0f, 1.0f);
    local_1.z = 0;
    // Block 579 @3765
    if (!((local_1.z < 6))) goto block_581; // @3820
    // Block 580 @3769
    SC_GetWp(param_1, &local_0);
    frnd(5.0f);
    local_0 = (&local_0 + 5.0f);
    frnd(5.0f);
    *(&local_0 + 4) = (param_1 + 5.0f);
    SC_CreatePtcVec_Ext(177, &local_0, 1000.0f, 0.0f, 1.0f, 1.0f);
    local_1.z = (local_1.z + 1);
    goto block_579; // @3765
    // Block 581 @3820
    return;
    // Block 582 @3821
    SC_CreatePtc(198, param_1);
    SC_SND_PlaySound3D(2965, param_1);
    SC_CreatePtcVec_Ext(176, param_1, 1000.0f, 0.0f, 1.0f, 1.0f);
    SC_CreatePtcVec_Ext(177, param_1, 5.0f, 0.0f, 1.0f, 1.0f);
    return;
    // Block 583 @3847
    param_3 = &local_1.z;
    local_0 = 0;
    // Block 584 @3860
    if (!((local_0 < param_2))) goto block_586; // @3912
    // Block 585 @3864
    frnd(param_1);
    local_1 = (&param_3 + param_1);
    frnd(param_1);
    local_1.y = (&param_3 + param_1);
    SC_CreatePtc(198, &local_1);
    SC_CreatePtcVec_Ext(177, &local_1, 5.0f, 0.0f, 1.0f, 1.0f);
    local_0 = (local_0 + 1);
    goto block_584; // @3860
    // Block 586 @3912
    SC_CreatePtcVec_Ext(176, param_3, 1000.0f, 0.0f, 1.0f, 1.0f);
    return;
    // Block 587 @3921
    param_3 = &local_1.z;
    local_0 = 0;
    // Block 588 @3934
    if (!((local_0 < param_2))) goto block_590; // @3978
    // Block 589 @3938
    frnd(param_1);
    local_1 = (&param_3 + param_1);
    frnd(param_1);
    local_1.y = (&param_3 + param_1);
    SC_CreatePtc(198, &local_1);
    local_0 = (local_0 + 1);
    goto block_588; // @3934
    // Block 590 @3978
    SC_CreatePtcVec_Ext(176, param_3, 1000.0f, 0.0f, 1.0f, 1.0f);
    return;
    // Block 591 @3987
    param_3 = &local_1.z;
    local_0 = 0;
    // Block 592 @4000
    if (!((local_0 < param_2))) goto block_594; // @4044
    // Block 593 @4004
    frnd(param_1);
    local_1 = (&param_3 + param_1);
    frnd(param_1);
    local_1.y = (&param_3 + param_1);
    SC_CreatePtc(198, &local_1);
    local_0 = (local_0 + 1);
    goto block_592; // @4000
    // Block 594 @4044
    return;
    // Block 595 @4045
    SC_ZeroMem(&local_1.z, 128);
    SC_P_Ai_GetProps(param_1, &local_1.z);
    (&local_1.z + 76) = 1;
    (&local_1.z + 12) = 4.0f;
    SC_P_Ai_SetProps(param_1, &local_1.z);
    *(&local_0 + 4) = 0.9f;
    local_0 = 0.3f;
    *(&local_0 + 8) = 0.5f;
    SC_P_Ai_SetBattleProps(param_1, &local_0);
    return;
    // Block 596 @4088
    SC_P_GetDir(param_2, &local_0);
    SC_VectorLen(&local_0);
    local_0 = &local_1.z;
    if (!((local_1.z > 1.0f))) goto block_598; // @4110
    // Block 597 @4107
    return;
    // Block 598 @4110
    return;
    // Block 599 @4113
    local_0 = 0;
    // Block 600 @4121
    if (!((local_0 < 6))) goto block_605; // @4177
    // Block 601 @4125
    SC_P_GetBySideGroupMember(0, 0, local_0);
    SC_P_IsReady(local_0);
    if (!(local_0)) goto block_604; // @4168
    // Block 602 @4139
    SC_P_GetBySideGroupMember(0, 0, local_0);
    SC_P_GetPos(local_0, &local_1.z);
    SC_2VectorsDist(&local_1.z, param_2);
    local_1.y = param_2;
    if (!((local_1.y < local_1))) goto block_604; // @4168
    // Block 603 @4164
    local_1 = local_1.y;
    // Block 604 @4168
    local_0 = (local_0 + 1);
    goto block_600; // @4121
    // Block 605 @4177
    return;
}

void func_4180(void) {
    // Block 606 @4180
    SC_P_GetPos(param_4, &local_0);
    SC_IsNear3D(&local_0, param_3, param_2);
    return;
    // Block 607 @4195
    SC_PC_GetPos(&local_0);
    SC_IsNear3D(&local_0, param_3, param_2);
    return;
    // Block 608 @4213
    if (!(param_5)) goto block_610; // @4217
    // Block 609 @4216
    goto block_611; // @4218
    // Block 610 @4217
    return;
    // Block 611 @4218
    SC_ZeroMem(&local_0, 128);
    SC_P_Ai_GetProps(param_5, &local_0);
    local_0.grenade_min_distance = param_4;
    local_0.grenade_timing_imprecision = param_3;
    local_0.grenade_throw_imprecision = param_2;
    local_0.grenade_sure_time = param_1;
    SC_P_Ai_SetProps(param_5, &local_0);
    return;
    // Block 612 @4251
    local_47 = 10000.0f;
    local_35.rad = 1000.0f;
    local_35 = unknown_612_4272_1;
    local_0 = 32;
    SC_GetPls(&local_35, &local_0.watchfulness_maxdistance, &local_0);
    local_34 = 0;
    local_0.watchfulness_zerodist = 0;
    // Block 613 @4291
    if (!((local_0.watchfulness_zerodist < local_0))) goto block_622; // @4373
    // Block 614 @4295
    SC_P_GetInfo(&local_0, &local_39);
    if (((&local_39 == param_3))) goto block_617; // @4315
    // Block 615 @4310
    if (((param_3 == 100))) goto block_617; // @4315
    // Block 616 @4314
    goto block_621; // @4364
    // Block 617 @4315
    SC_P_IsReady(&local_0);
    if (!(&local_0)) goto block_621; // @4364
    // Block 618 @4327
    goto block_619; // @4328
    // Block 619 @4328
    SC_P_GetPos(&local_0.watchfulness_maxdistance, &local_0.hear_distance_mult);
    SC_2VectorsDist(&local_0.hear_distance_mult, param_2);
    local_0.hear_distance_max = param_2;
    if (!((local_0.hear_distance_max < local_47))) goto block_621; // @4364
    // Block 620 @4351
    local_47 = local_0.hear_distance_max;
    local_0.hear_distance_mult = &local_34;
    // Block 621 @4364
    local_0.watchfulness_zerodist = (local_0.watchfulness_zerodist + 1);
    goto block_613; // @4291
    // Block 622 @4373
    return;
}

void func_4376(void) {
    // Block 623 @4376
    SC_P_GetInfo(param_3, &local_10);
    local_10 = &local_3;
    SC_P_GetPos(param_3, &local_9);
    local_9.rad = 1000.0f;
    local_0 = 32;
    SC_GetPls(&local_9, &local_1, &local_0);
    local_2 = 0;
    local_1 = 0;
    // Loop header - Block 624 @4419
    while (true) {  // loop body: blocks [624, 625, 626, 627, 628, 629, 630, 632]
        // Block 624 @4419
        if (!((local_1 < local_0))) break;  // exit loop @4498
        // Block 625 @4423
        SC_P_GetInfo(&local_0, &local_10);
        if (!((&local_10 == 1))) goto block_632; // @4489
        // Block 626 @4438
        if (!((&local_0 == local_3))) goto block_632; // @4489
        // Block 627 @4444
        goto block_628; // @4445
        // Block 628 @4445
        SC_P_IsReady(&local_1);
        if (!(&local_1)) goto block_632; // @4489
        // Block 629 @4457
        goto block_630; // @4458
        // Block 630 @4458
        local_9 = (param_2 + (local_2 * 4));
        local_2 = (local_2 + 1);
        if (!((local_2 == param_1))) goto block_632; // @4489
    }
    // Block 631 @4483
    SC_Log(1299473735, 2);
    return;
    // Block 632 @4489
    local_1 = (local_1 + 1);
    continue;  // back to loop header @4419
    // Block 633 @4498
    local_2 = param_1;
    return;
    // Block 634 @4503
    local_0 = 32;
    SC_P_GetInfo(param_1, &local_34);
    if (!((local_0 < 2))) goto block_636; // @4539
    // Block 635 @4524
    SC_Log(param_1, &local_34, 3, &"VC %d %d couldnot find anyone to lead group %d", 5);
    return;
    // Block 636 @4539
    if (!((&local_34 != param_1))) goto block_638; // @4555
    // Block 637 @4546
    goto block_639; // @4563
    // Block 638 @4555
    // Block 639 @4563
    phi_639_5_771 = phi(b637:data_887, b638:data_890)
    SC_Log(phi_639_5_771, 3, 622871382, 4);
    return;
}

void func_4575(void) {
    // Block 640 @4575
    SC_P_GetPos(param_3, &local_0);
    SC_2VectorsDist(param_2, &local_0);
    local_0 = &local_0.group;
    return;
    // Block 641 @4594
    SC_ZeroMem(&local_0, 20);
    (&local_0 + 0) = 0;
    (&local_0 + 4) = 0;
    (&local_0 + 8) = 0;
    (&local_0 + 12) = 0;
    (&local_0 + 16) = 0;
    SC_P_SetSpecAnims(param_1, &local_0);
    return;
    // Block 642 @4634
    SC_ZeroMem(&local_0, 20);
    param_5 = (&local_0 + 0);
    param_4 = (&local_0 + 4);
    param_3 = (&local_0 + 8);
    param_2 = (&local_0 + 12);
    param_1 = (&local_0 + 16);
    SC_P_SetSpecAnims(param_6, &local_0);
    return;
    // Block 643 @4674
    local_0 = 32;
    SC_GetPls(param_2, &local_0.max_hp, &local_0);
    if (!(local_0)) goto block_645; // @4691
    // Block 644 @4690
    goto block_646; // @4692
    // Block 645 @4691
    return;
    // Block 646 @4692
    local_0.max_hp = 0;
    // Block 647 @4696
    if (!((local_0.max_hp < local_0))) goto block_649; // @4793
    // Block 648 @4700
    t4709_0 = param_1 / 7.0f;
    SC_P_DoHit(&local_0, 0, t4709_0);
    t4721_0 = param_1 / 7.0f;
    SC_P_DoHit(t4709_0, 1, t4721_0);
    t4733_0 = param_1 / 7.0f;
    SC_P_DoHit(t4721_0, 2, t4733_0);
    t4745_0 = param_1 / 7.0f;
    SC_P_DoHit(t4733_0, 3, t4745_0);
    t4757_0 = param_1 / 7.0f;
    SC_P_DoHit(t4745_0, 4, t4757_0);
    t4769_0 = param_1 / 7.0f;
    SC_P_DoHit(t4757_0, 5, t4769_0);
    SC_P_DoHit(t4769_0, 6, (param_1 / 7.0f));
    local_0.max_hp = (local_0.max_hp + 1);
    goto block_647; // @4696
    // Block 649 @4793
    return;
    // Block 650 @4794
    SC_P_GetPos(param_2, &local_0);
    local_0.side = (&local_0 + 1.0f);
    local_0.group = 1.0f;
    SC_SphereIsVisible(&local_0);
    return;
    // Block 651 @4821
    SC_P_GetInfo(param_2, &local_0);
    return;
    // Block 652 @4831
    SC_P_GetInfo(param_2, &local_0);
    return;
    // Block 653 @4841
    SC_P_GetInfo(param_2, &local_0);
    return;
    // Block 654 @4851
    local_0 = 0;
    // Block 655 @4856
    if (!((local_0 < 0))) goto block_657; // @4878
    // Block 656 @4860
    local_0 = (local_0 + 1);
    goto block_655; // @4856
    // Block 657 @4878
    // STORE: 0 = 0;
    return;
    // Block 658 @4883
    local_0 = 0;
    // Block 659 @4888
    if (!((local_0 < 0))) goto block_663; // @4917
    // Block 660 @4892
    if (!((unknown_660_4899_1 == param_1))) goto block_662; // @4908
    // Block 661 @4901
    SC_Log(1819309380, param_1, 3);
    return;
    // Block 662 @4908
    local_0 = (local_0 + 1);
    goto block_659; // @4888
    // Block 663 @4917
    param_1 = (0 + (0 * 8));
    *((0 + (0 * 8)) + 4) = 0;
    // STORE: 0 = (0 + 1);
    SC_SetObjectives(0, 0, 6.0f);
    return;
}

void func_4948(void) {
    // Block 664 @4948
    local_0 = 0;
    // Loop header - Block 665 @4953
    while (true) {  // loop body: blocks [665, 666, 668]
        // Block 665 @4953
        if (!((local_0 < 0))) break;  // exit loop @4982
        // Block 666 @4957
        if (!((unknown_666_4964_1 == param_1))) goto block_668; // @4973
    }
    // Block 667 @4966
    SC_Log(1819309380, param_1, 3);
    return;
    // Block 668 @4973
    local_0 = (local_0 + 1);
    continue;  // back to loop header @4953
    // Block 669 @4982
    param_1 = (0 + (0 * 8));
    *((0 + (0 * 8)) + 4) = 0;
    // STORE: 0 = (0 + 1);
    SC_SetObjectivesNoSound(0, 0, 6.0f);
    return;
    // Block 670 @5013
    local_0 = 0;
    // Block 671 @5018
    if (!((local_0 < 0))) goto block_677; // @5066
    // Block 672 @5022
    if (!((unknown_672_5029_1 == param_1))) goto block_676; // @5057
    // Block 673 @5031
    if (!((unknown_673_5039_1 == 0))) goto block_676; // @5057
    // Block 674 @5041
    goto block_675; // @5042
    // Block 675 @5042
    *((0 + (local_0 * 8)) + 4) = 2;
    SC_SetObjectives(0, 0, 6.0f);
    return;
    // Block 676 @5057
    local_0 = (local_0 + 1);
    goto block_671; // @5018
    // Block 677 @5066
    return;
    // Block 678 @5067
    local_0 = 0;
    // Block 679 @5072
    if (!((local_0 < 0))) goto block_683; // @5103
    // Block 680 @5076
    if (!((unknown_680_5083_1 == param_1))) goto block_682; // @5094
    // Block 681 @5085
    *((0 + (local_0 * 8)) + 4) = 1;
    // Block 682 @5094
    local_0 = (local_0 + 1);
    goto block_679; // @5072
    // Block 683 @5103
    SC_SetObjectives(0, 0, 6.0f);
    return;
    // Block 684 @5109
    local_0 = 0;
    // Block 685 @5114
    if (!((local_0 < 0))) goto block_689; // @5145
    // Block 686 @5118
    if (!((unknown_686_5125_1 == param_2))) goto block_688; // @5136
    // Block 687 @5127
    return;
    // Block 688 @5136
    local_0 = (local_0 + 1);
    goto block_685; // @5114
    // Block 689 @5145
    // Block 690 @5147
    if (!((local_0 < 5))) goto block_696; // @5194
    // Block 691 @5151
    SC_P_GetBySideGroupMember(0, 0, local_0);
    SC_P_IsReady(local_0);
    if (!(local_0)) goto block_695; // @5193
    // Block 692 @5165
    goto block_693; // @5166
    // Block 693 @5166
    SC_P_GetBySideGroupMember(0, 0, local_0);
    SC_P_Ai_GetPeaceMode(local_0);
    local_1 = local_0;
    if (!((local_1 != 0))) goto block_695; // @5193
    // Block 694 @5186
    local_1 = 0;
    return;
    // Block 695 @5193
    goto block_690; // @5147
    // Block 696 @5194
    return;
}

void func_5197(void) {
    // Block 697 @5197
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
    SC_Log(1702257996, 10, 3);
    return;
    // Block 698 @5245
    SC_ZeroMem(&local_0, 120);
    SC_ZeroMem(&local_30, 24);
    SC_ZeroMem(&local_9, 24);
    (&local_0 + 0) = 0;
    (&local_0 + 20) = 5.0f;
    (&local_0 + 40) = 1.5f;
    (&local_0 + 60) = 1.5f;
    (&local_0 + 80) = 2.0f;
    local_42 = 0;
    // Block 699 @5295
    if (!((local_42 < 5))) goto block_701; // @5363
    // Block 700 @5299
    *((&local_0 + (local_42 * 20)) + 4) = (24 + 1.0f);
    frnd(0.5f);
    *((&local_0 + (local_42 * 20)) + 8) = 0.5f;
    frnd(0.5f);
    *(((&local_0 + (local_42 * 20)) + 8) + 4) = 0.5f;
    *(((&local_0 + (local_42 * 20)) + 8) + 8) = 0;
    local_42 = (local_42 + 1);
    goto block_699; // @5295
    // Block 701 @5363
    (&local_30 + 0) = 1;
    (&local_30 + 4) = 4;
    (&local_30 + 8) = 5;
    (&local_30 + 12) = 2;
    (&local_30 + 16) = 3;
    (&local_9 + 0) = 1;
    (&local_9 + 4) = 5;
    (&local_9 + 8) = 3;
    (&local_9 + 12) = 4;
    (&local_9 + 16) = 2;
    SC_Ai_SetPlFollow(0, 0, 0, &local_0, &local_30, &local_9, 5);
    (&local_0 + 0) = 0;
    (&local_0 + 20) = 4.0f;
    (&local_0 + 40) = 1.5f;
    (&local_0 + 60) = 1.5f;
    (&local_0 + 80) = 1.5f;
    (&local_0 + 100) = 2.0f;
    local_42 = 0;
    // Block 702 @5472
    if (!((local_42 < 6))) goto block_704; // @5548
    // Block 703 @5476
    *((&local_0 + (local_42 * 20)) + 4) = (5 + 1.0f);
    frnd(0.2f);
    *((&local_0 + (local_42 * 20)) + 8) = 0.2f;
    frnd(0.2f);
    *(((&local_0 + (local_42 * 20)) + 8) + 4) = 0.2f;
    *(((&local_0 + (local_42 * 20)) + 8) + 8) = 0;
    (&local_9 + (local_42 * 4)) = 0;
    local_42 = (local_42 + 1);
    goto block_702; // @5472
    // Block 704 @5548
    (&local_30 + 0) = 0;
    (&local_30 + 4) = 1;
    (&local_30 + 8) = 4;
    (&local_30 + 12) = 5;
    (&local_30 + 16) = 2;
    (&local_30 + 20) = 3;
    SC_Ai_SetPlFollow(0, 0, 1, &local_0, &local_30, &local_9, 6);
    return;
    // Block 705 @5594
    SC_RadioSetDist(10.0f);
    return;
    // Block 706 @5599
    if (!(0)) goto block_708; // @5606
    // Block 707 @5603
    return;
    // Block 708 @5606
    SC_P_GetBySideGroupMember(0, 0, 4);
    local_0.y = 4;
    if (!(local_0.y)) goto block_710; // @5620
    // Block 709 @5619
    goto block_711; // @5623
    // Block 710 @5620
    return;
    // Block 711 @5623
    SC_P_Ai_GetSureEnemies(local_0.y);
    if (!(local_0.y)) goto block_713; // @5631
    // Block 712 @5630
    goto block_716; // @5642
    // Block 713 @5631
    SC_ggi(SGI_MISSIONALARM);
    if (!(2)) goto block_715; // @5639
    // Block 714 @5638
    goto block_716; // @5642
    // Block 715 @5639
    return;
    // Block 716 @5642
    // STORE: 0 = 1;
    SC_P_GetBySideGroupMember(0, 0, 4);
    SC_P_Speach(4, 4010, 4010, &local_0);
    local_0 = (local_0 + 1.0f);
    SC_SpeachRadio(5013, 5013, &local_0);
    return;
    // Block 717 @5673
    SC_ZeroMem(0, 0);
    local_0 = 0;
    // Block 718 @5682
    if (!((local_0 < 0))) goto block_720; // @5740
    // Block 719 @5686
    *((0 + (local_0 * 36)) + 20) = 0;
    // STORE: 1.0f = ((0 + (local_0 * 36)) + 12);
    *((0 + (local_0 * 36)) + 16) = 1;
    *((0 + (local_0 * 36)) + 28) = 0;
    *((0 + (local_0 * 36)) + 32) = 0;
    local_0 = (local_0 + 1);
    goto block_718; // @5682
    // Block 720 @5740
    return;
    // Block 721 @5741
    SC_Log(1768186977, param_2, 3);
    *((0 + (param_2 * 36)) + 16) = 2;
    *((0 + ((param_2 + 1) * 36)) + 16) = 2;
    *((0 + (param_2 * 36)) + 24) = (param_2 + 1);
    param_2 = ((0 + ((param_2 + 1) * 36)) + 24);
    *((0 + (param_2 * 36)) + 28) = 4;
    *((0 + ((param_2 + 1) * 36)) + 28) = 4;
    SC_NOD_Get(param_1, &"Plechovka");
    local_9 = &"Plechovka";
    if (!(local_9)) goto block_723; // @5827
    // Block 722 @5826
    goto block_724; // @5832
    // Block 723 @5827
    SC_message(&"trap not found!!!", 1);
    return;
    // Block 724 @5832
    SC_NOD_GetWorldPos(local_9, &local_0);
    SC_NOD_Get(param_1, &"Konec dratu");
    local_9 = &"Konec dratu";
    SC_NOD_GetWorldPos(local_9, &local_2.y);
    local_5.y = (local_9 - &local_2.y);
    (&local_5.y + 4) = (&local_0 - param_1);
    (&local_5.y + 8) = (param_1 - local_9);
    SC_VectorLen(&local_5.y);
    t5888_0 = FTOD((3.0f * &local_5.y));
    t5891_0 = DMUL(param_2, 3, t5888_0, t5888_1);
    t5894_0 = DADD(3, &"adding trap on pos %d", t5891_0, t5891_1);
    local_10 = t5895_0;
    local_10 = ((0 + (param_2 * 36)) + 12);
    local_10 = ((0 + ((param_2 + 1) * 36)) + 12);
    (unknown_724_5925_1 + (unknown_724_5924_1 * 1048576000)) = (0 + (param_2 * 36));
    *((0 + (param_2 * 36)) + 4) = (unknown_724_5941_1 + (unknown_724_5940_1 * 1048576000));
    *((0 + (param_2 * 36)) + 8) = (unknown_724_5958_1 + (unknown_724_5957_1 * 1048576000));
    (unknown_724_5973_1 + (unknown_724_5972_1 * 0.75f)) = (0 + ((param_2 + 1) * 36));
    (unknown_724_5991_1 + (unknown_724_5990_1 * 0.75f)) = ((0 + ((param_2 + 1) * 36)) + 4);
    (unknown_724_6010_1 + (unknown_724_6009_1 * 0.75f)) = ((0 + ((param_2 + 1) * 36)) + 8);
    return;
    // Block 725 @6022
    SC_NOD_Get(param_2, &"Plechovka");
    local_0.y = &"Plechovka";
    if (!(local_0.y)) goto block_727; // @6041
    // Block 726 @6040
    goto block_728; // @6048
    // Block 727 @6041
    SC_message(&"trap not found!!!", 1);
    return;
    // Block 728 @6048
    SC_NOD_GetWorldPos(local_0.y, &local_3.z);
    SC_NOD_Get(param_2, 1701736267);
    local_0.y = 1701736267;
    SC_NOD_GetWorldPos(local_0.y, &local_0.z);
    local_11 = (local_0.y - &local_0.z);
    *(&local_11 + 4) = (&local_3.z - param_2);
    *(&local_11 + 8) = ((param_2 - local_0.y) + 10000.0f);
    local_0.y = (unknown_728_6104_1 + (unknown_728_6103_1 * 1048576000));
    (&local_0.y + 4) = (unknown_728_6116_1 + (unknown_728_6115_1 * 1048576000));
    (&local_0.y + 8) = (unknown_728_6129_1 + (unknown_728_6128_1 * 1048576000));
    local_0 = 0;
    // Block 729 @6138
    if (!((local_0 < 0))) goto block_733; // @6193
    // Block 730 @6142
    SC_IsNear2D((0 + (local_0 * 36)), &local_0.y, 1.0f);
    if (!(1.0f)) goto block_732; // @6184
    // Block 731 @6155
    *((0 + (local_0 * 36)) + 20) = 1;
    *((0 + ((local_0 + 1) * 36)) + 20) = 1;
    SC_Log(1869440370, local_0, 3);
    return;
    // Block 732 @6184
    local_0 = (local_0 + 1);
    goto block_729; // @6138
    // Block 733 @6193
    return;
}

void func_6196(void) {
    // Block 734 @6196
    goto block_736; // @6203
    // Block 735 @6199
    if (!((local_0 == 0))) goto block_738; // @6207
    // Block 736 @6203
    return;
    // Block 737 @6206
    goto block_739; // @6211
    // Block 738 @6207
    if (!((local_0 == 1))) goto block_743; // @6219
    // Block 739 @6211
    if (!(param_3)) goto block_741; // @6214
    // Block 740 @6213
    goto block_742; // @6217
    // Block 741 @6214
    return;
    // Block 742 @6217
    goto block_744; // @6223
    // Block 743 @6219
    if (!((local_0 == 2))) goto block_747; // @6232
    // Block 744 @6223
    if (!((param_3 == 1))) goto block_746; // @6230
    // Block 745 @6227
    return;
    // Block 746 @6230
    goto block_748; // @6236
    // Block 747 @6232
    if (!((local_0 == 3))) goto block_751; // @6245
    // Block 748 @6236
    if (!((param_3 < 2))) goto block_750; // @6243
    // Block 749 @6240
    return;
    // Block 750 @6243
    goto block_752; // @6249
    // Block 751 @6245
    if (!((local_0 == 4))) goto block_755; // @6255
    // Block 752 @6249
    if (!(param_3)) goto block_754; // @6254
    // Block 753 @6251
    return;
    // Block 754 @6254
    goto block_755; // @6255
    // Block 755 @6255
    return;
}

void func_6259(void) {
    // Block 756 @6259
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_GetPeaceMode(1);
    if (!((1 == 2))) goto block_758; // @6284
    // Block 757 @6275
    SC_Ai_SetPeaceMode(0, 0, 0);
    SC_Ai_PointStopDanger(0, 0);
    // Block 758 @6284
    return;
    // Block 759 @6285
    // STORE: 0 = 0;
    local_5 = 0;
    local_1 = 0;
    // Block 760 @6304
    if (!((local_1 < 6))) goto block_801; // @6633
    // Block 761 @6308
    SC_P_GetBySideGroupMember(0, 0, local_1);
    local_3 = local_1;
    SC_P_IsReady(local_3);
    if (!(local_3)) goto block_800; // @6624
    // Block 762 @6326
    SC_P_GetPos(local_3, &local_6);
    local_0 = 0;
    // Block 763 @6334
    if (!((local_0 < 0))) goto block_800; // @6624
    // Block 764 @6338
    if (!(&local_6)) goto block_766; // @6347
    // Block 765 @6346
    goto block_799; // @6615
    // Block 766 @6347
    t6352_0 = 0 + (local_0 * 36);
    SC_IsNear3D(local_3, t6352_0, &local_6);
    if (!(&local_6)) goto block_799; // @6615
    // Block 767 @6366
    goto block_768; // @6367
    // Block 768 @6367
    if (!(local_1)) goto block_799; // @6615
    // Block 769 @6381
    goto block_770; // @6382
    // Block 770 @6382
    goto block_772; // @6395
    // Block 771 @6391
    if (!((local_9 == 1))) goto block_773; // @6397
    // Block 772 @6395
    goto block_774; // @6401
    // Block 773 @6397
    if (!((local_9 == 2))) goto block_778; // @6443
    // Block 774 @6401
    local_2 = 0;
    if (!(0)) goto block_776; // @6413
    // Block 775 @6407
    SC_P_ScriptMessage(local_3, 4, 1);
    goto block_777; // @6418
    // Block 776 @6413
    SC_P_ScriptMessage(local_3, 4, 0);
    // Block 777 @6418
    phi_777_5_789 = phi(b776:data_1322, b775:data_1320)
    phi_777_6_790 = phi(b776:data_1323, b775:data_1321)
    // STORE: 0 = 1;
    // STORE: 0 = 1;
    *((1 + (0 * 36)) + 20) = phi_777_6_790;
    goto block_779; // @6447
    // Block 778 @6443
    if (!((local_9 == 3))) goto block_783; // @6484
    // Block 779 @6447
    local_2 = 0;
    if (!((local_1 == 1))) goto block_781; // @6471
    // Block 780 @6455
    SC_P_Speech2(local_3, 4062, &local_2);
    local_2 = (local_2 + 0.1f);
    // STORE: 0 = 20;
    goto block_782; // @6482
    // Block 781 @6471
    SC_P_Speech2(local_3, 4061, &local_2);
    local_2 = (local_2 + 0.1f);
    // Block 782 @6482
    phi_782_7_798 = phi(b780:data_1332, b781:data_1335)
    goto block_784; // @6488
    // Block 783 @6484
    if (!((local_9 == 4))) goto block_787; // @6514
    // Block 784 @6488
    local_2 = 0;
    if (!((local_1 == 1))) goto block_786; // @6512
    // Block 785 @6496
    SC_P_Speech2(local_3, 0, &local_2);
    local_2 = (local_2 + 0.1f);
    // STORE: 0 = 2;
    // Block 786 @6512
    goto block_788; // @6518
    // Block 787 @6514
    if (!((local_9 == 5))) goto block_791; // @6540
    // Block 788 @6518
    local_2 = 0;
    if (!((local_1 == 2))) goto block_790; // @6537
    // Block 789 @6526
    SC_P_Speech2(local_3, 4884, &local_2);
    local_2 = (local_2 + 0.1f);
    // Block 790 @6537
    goto block_792; // @6544
    // Block 791 @6540
    if (!((local_9 == 10))) goto block_796; // @6566
    // Block 792 @6544
    if (!(0)) goto block_794; // @6552
    // Block 793 @6546
    SC_P_ScriptMessage(local_3, 4, 1);
    goto block_795; // @6557
    // Block 794 @6552
    SC_P_ScriptMessage(local_3, 4, 0);
    // Block 795 @6557
    phi_795_16_843 = phi(b793:data_1348, b794:data_1350)
    phi_795_17_844 = phi(b793:data_1349, b794:data_1351)
    // STORE: 0 = 1;
    // STORE: 0 = 10;
    goto block_796; // @6566
    // Block 796 @6566
    // STORE: 0 = phi_796_17_862;
    local_1 = 0;
    if (!(local_1)) goto block_798; // @6604
    // Block 797 @6595
    *((0 + (local_0 * 36)) + 20) = 1;
    // Block 798 @6604
    SC_Log(1713398821, 0, local_0, local_1, 5);
    return;
    // Block 799 @6615
    local_0 = (local_0 + 1);
    goto block_763; // @6334
    // Block 800 @6624
    local_1 = (local_1 + 1);
    goto block_760; // @6304
    // Block 801 @6633
    return;
    // Block 802 @6636
    if (!((param_2 < param_1))) goto block_807; // @6697
    // Block 803 @6643
    param_1 = (param_1 + 1);
    SC_Ai_ClearCheckPoints(0, 0);
    local_0 = param_2;
    // Block 804 @6659
    if (!((local_0 < param_1))) goto block_806; // @6696
    // Block 805 @6663
    sprintf(&"point", local_0, 3);
    SC_GetWp(&local_1, &local_9);
    SC_Ai_AddCheckPoint(0, 0, &local_9, 0);
    local_0 = (local_0 + 1);
    goto block_804; // @6659
    // Block 806 @6696
    goto block_810; // @6750
    // Block 807 @6697
    param_1 = (param_1 - 1);
    SC_Ai_ClearCheckPoints(0, 0);
    local_0 = param_2;
    // Block 808 @6713
    if (!((local_0 > param_1))) goto block_810; // @6750
    // Block 809 @6717
    sprintf(&"point", local_0, 3);
    SC_GetWp(&local_1, &local_9);
    SC_Ai_AddCheckPoint(0, 0, &local_9, 0);
    local_0 = (local_0 - 1);
    goto block_808; // @6713
    // Block 810 @6750
    return;
    // Block 811 @6751
    param_1 = (param_1 + 1);
    local_0 = param_2;
    // Block 812 @6766
    if (!((local_0 < param_1))) goto block_814; // @6803
    // Block 813 @6770
    sprintf(&"point", local_0, 3);
    SC_GetWp(&local_1, &local_9);
    SC_Ai_AddCheckPoint(0, 0, &local_9, 0);
    local_0 = (local_0 + 1);
    goto block_812; // @6766
    // Block 814 @6803
    return;
}

void func_6804(void) {
    // Block 815 @6804
    local_0 = 1;
    // Loop header - Block 816 @6810
    while (true) {  // loop body: blocks [816, 817, 818, 819, 821]
        // Block 816 @6810
        if (!((local_0 < 6))) break;  // exit loop @6861
        // Block 817 @6814
        SC_P_GetBySideGroupMember(0, 0, local_0);
        SC_P_IsReady(local_0);
        if (!(local_0)) goto block_821; // @6852
        // Block 818 @6828
        goto block_819; // @6829
        // Block 819 @6829
        SC_P_GetBySideGroupMember(0, 0, local_0);
        SC_P_Ai_GetPeaceMode(local_0);
        local_1 = local_0;
        if (!((local_1 != 0))) goto block_821; // @6852
    }
    // Block 820 @6849
    return;
    // Block 821 @6852
    local_0 = (local_0 + 1);
    continue;  // back to loop header @6810
    // Block 822 @6861
    return;
    // Block 823 @6864
    SC_Ai_SetPeaceMode();
    return;
}

void func_6873(void) {
    // Block 824 @6873
    local_0 = 0;
    // Loop header - Block 825 @6879
    while (true) {  // loop body: blocks [825, 826]
        // Block 825 @6879
        if (!((local_0 < 14))) break;  // exit loop @6946
        // Block 826 @6883
        *((0 + (local_0 * 28)) + 24) = 0;
        sprintf(&"ACTIVEPLACE#%d", local_0, 3);
        t6907_0 = 0 + (local_0 * 28);
        // STORE: 2.0f = ((0 + (local_0 * 28)) + 12);
        *((0 + (local_0 * 28)) + 16) = 0;
        // STORE: -1.0f = ((0 + (local_0 * 28)) + 20);
        local_0 = (local_0 + 1);
        continue;  // back to loop header @6879
    }
    // Block 827 @6946
    // STORE: 30.0f = ((0 + 0) + 20);
    // STORE: 15.0f = ((0 + 28) + 20);
    *((0 + 196) + 24) = -100;
    SC_GetWp(&"WayPoint113", 0);
    SC_GetWp(&"WayPoint#33", 0);
    return;
}

void func_6984(void) {
    // Block 828 @6984
    goto block_830; // @6991
    // Block 829 @6987
    if (!((local_0 == 0))) goto block_831; // @6992
    // Block 830 @6991
    goto block_832; // @6996
    // Block 831 @6992
    if (!((local_0 == 1))) goto block_833; // @7016
    // Block 832 @6996
    *((0 + (param_1 * 28)) + 16) = 0;
    *((0 + (param_1 * 28)) + 24) = 1;
    goto block_834; // @7020
    // Block 833 @7016
    if (!((local_0 == 2))) goto block_835; // @7021
    // Block 834 @7020
    goto block_836; // @7025
    // Block 835 @7021
    if (!((local_0 == 3))) goto block_837; // @7026
    // Block 836 @7025
    goto block_838; // @7030
    // Block 837 @7026
    if (!((local_0 == 4))) goto block_839; // @7031
    // Block 838 @7030
    goto block_840; // @7035
    // Block 839 @7031
    if (!((local_0 == 5))) goto block_841; // @7036
    // Block 840 @7035
    goto block_842; // @7040
    // Block 841 @7036
    if (!((local_0 == 6))) goto block_843; // @7041
    // Block 842 @7040
    goto block_843; // @7041
    // Block 843 @7041
    return;
}

void func_7043(void) {
    // Block 844 @7043
    SC_PC_Get();
    SC_P_GetWillTalk();
    local_0 = (unknown_844_7055_1 + 0.2f);
    goto block_846; // @7066
    // Block 845 @7062
    if (!((local_1 == 0))) goto block_850; // @7131
    // Block 846 @7066
    if (!((param_1 == 0))) goto block_848; // @7091
    // Block 847 @7076
    SC_PC_Get();
    SC_P_Speech2();
    local_0 = (local_0 + 0.1f);
    goto block_849; // @7105
    // Block 848 @7091
    SC_PC_Get();
    SC_P_Speech2();
    local_0 = (local_0 + 0.1f);
    // Block 849 @7105
    phi_849_0_880 = phi(b848:data_1812, b847:data_1810)
    *((0 + (param_1 * 28)) + 24) = -100;
    local_0 = ((0 + (param_1 * 28)) + 16);
    goto block_851; // @7135
    // Block 850 @7131
    if (!((local_1 == 1))) goto block_859; // @7257
    // Block 851 @7135
    if (!((phi_851_0_882 == 0))) goto block_856; // @7182
    // Block 852 @7145
    rand();
    if (!((unknown_852_7150_1 % 2))) goto block_854; // @7167
    // Block 853 @7152
    SC_PC_Get();
    SC_P_Speech2();
    local_0 = (local_0 + 0.1f);
    goto block_855; // @7181
    // Block 854 @7167
    SC_PC_Get();
    SC_P_Speech2();
    local_0 = (local_0 + 0.1f);
    // Block 855 @7181
    phi_855_0_883 = phi(b853:data_1822, b854:data_1824)
    goto block_858; // @7231
    // Block 856 @7182
    SC_PC_Get();
    SC_PC_Get();
    if (!(((0 + (param_1 * 28)) < (0 + 196)))) goto block_858; // @7231
    // Block 857 @7210
    SC_PC_Get();
    rand();
    SC_P_Speech2();
    local_0 = (local_0 + 0.1f);
    // Block 858 @7231
    phi_858_0_885 = phi(b857:t7221_0, b855:phi_855_0_883)
    *((0 + (param_1 * 28)) + 24) = -100;
    local_0 = ((0 + (param_1 * 28)) + 16);
    goto block_860; // @7261
    // Block 859 @7257
    if (!((local_1 == 2))) goto block_861; // @7286
    // Block 860 @7261
    SC_PC_Get();
    SC_P_Speech2(phi_860_0_887, 906, &local_0);
    local_0 = (local_0 + 0.1f);
    *((0 + (param_1 * 28)) + 24) = -100;
    goto block_862; // @7290
    // Block 861 @7286
    if (!((local_1 == 3))) goto block_863; // @7316
    // Block 862 @7290
    SC_PC_Get();
    SC_P_SpeechMes2(&local_0, 907, &local_0, 11);
    local_0 = (local_0 + 0.1f);
    *((0 + (param_1 * 28)) + 24) = -100;
    goto block_864; // @7320
    // Block 863 @7316
    if (!((local_1 == 4))) goto block_865; // @7426
    // Block 864 @7320
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_GetPos(0, &local_1);
    SC_SND_PlaySound3D(2060, &local_1);
    local_0 = (local_0 + 0.1f);
    SC_PC_Get();
    SC_P_SpeechMes2(&local_1, 912, &local_0, 12);
    local_0 = (local_0 + 0.1f);
    local_0 = 0.5f;
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_Speech2(0, 913, &local_0);
    local_0 = (local_0 + 0.1f);
    SC_P_GetBySideGroupMember(1, 0, 1);
    SC_P_Speech2(1, 914, &local_0);
    local_0 = (local_0 + 0.1f);
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_SpeechMes2(0, 915, &local_0, 13);
    local_0 = (local_0 + 0.1f);
    *((0 + (param_1 * 28)) + 24) = -100;
    goto block_866; // @7430
    // Block 865 @7426
    if (!((local_1 == 5))) goto block_867; // @7455
    // Block 866 @7430
    SC_PC_Get();
    SC_P_Speech2(13, 921, &local_0);
    local_0 = (local_0 + 0.1f);
    *((0 + (param_1 * 28)) + 24) = -100;
    goto block_868; // @7459
    // Block 867 @7455
    if (!((local_1 == 6))) goto block_869; // @7484
    // Block 868 @7459
    SC_PC_Get();
    SC_P_Speech2(&local_0, 922, &local_0);
    local_0 = (local_0 + 0.1f);
    *((0 + (param_1 * 28)) + 24) = -100;
    goto block_870; // @7488
    // Block 869 @7484
    if (!((local_1 == 8))) goto block_871; // @7518
    // Block 870 @7488
    SC_P_GetBySideGroupMember(1, 0, 1);
    SC_P_SpeechMes2(1, 924, &local_0, 14);
    local_0 = (local_0 + 0.1f);
    *((0 + (param_1 * 28)) + 24) = -100;
    goto block_872; // @7522
    // Block 871 @7518
    if (!((local_1 == 9))) goto block_873; // @7563
    // Block 872 @7522
    *((0 + (param_1 * 28)) + 24) = -100;
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_Ai_SetMode(0, SC_P_AI_MODE_PEACE);
    SC_GetWp(&"WayPoint113", &local_1);
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_Ai_Go(0, &local_1);
    goto block_874; // @7567
    // Block 873 @7563
    if (!((local_1 == 10))) goto block_877; // @7595
    // Block 874 @7567
    if (!(0)) goto block_876; // @7593
    // Block 875 @7569
    SC_PC_Get();
    SC_P_SpeechMes2(&local_1, 932, &local_0, 15);
    local_0 = (local_0 + 0.1f);
    *((0 + (param_1 * 28)) + 24) = -100;
    // Block 876 @7593
    goto block_878; // @7599
    // Block 877 @7595
    if (!((local_1 == 11))) goto block_879; // @7658
    // Block 878 @7599
    SC_P_GetBySideGroupMember(1, 1, 0);
    SC_P_GetPos(0, &local_1);
    SC_SND_PlaySound3D(10419, &local_1);
    SC_P_GetBySideGroupMember(1, 1, 1);
    SC_P_GetPos(1, &local_1);
    SC_SND_PlaySound3D(10419, &local_1);
    SC_PC_Get();
    SC_P_Speech2(&local_1, 944, &local_0);
    local_0 = (local_0 + 0.1f);
    // STORE: 0 = 1;
    *((0 + (param_1 * 28)) + 24) = -100;
    goto block_880; // @7662
    // Block 879 @7658
    if (!((local_1 == 13))) goto block_881; // @7680
    // Block 880 @7662
    SC_AGS_Set(1);
    *((0 + (param_1 * 28)) + 24) = -100;
    goto block_882; // @7684
    // Block 881 @7680
    if (!((local_1 == 12))) goto block_883; // @7695
    // Block 882 @7684
    *((0 + (param_1 * 28)) + 24) = -100;
    goto block_883; // @7695
    // Block 883 @7695
    return;
}

void func_7697(void) {
    // Block 884 @7697
    local_0 = 0;
    // Loop header - Block 885 @7702
    while (true) {  // loop body: blocks [885, 886, 887, 888, 889]
        // Block 885 @7702
        if (!((local_0 < 14))) break;  // exit loop @7755
        // Block 886 @7706
        if (!((unknown_886_7714_1 > 0))) goto block_889; // @7746
        // Block 887 @7716
        *((0 + (local_0 * 28)) + 16) = (unknown_887_7724_1 - param_1);
        if (!((unknown_887_7741_1 < 0))) goto block_889; // @7746
        // Block 888 @7743
        // Block 889 @7746
        local_0 = (local_0 + 1);
        continue;  // back to loop header @7702
    }
    // Block 890 @7755
    local_0 = 0;
    // Loop header - Block 891 @7759
    while (true) {  // loop body: blocks [891, 892, 893, 896]
        // Block 891 @7759
        if (!((local_0 < 14))) break;  // exit loop @7806
        // Block 892 @7763
        if (!((unknown_892_7771_1 != -100))) goto block_896; // @7797
        // Block 893 @7773
        SC_IsNear3D();
        if (!((0 + (local_0 * 28)))) goto block_896; // @7797
    }
    // Block 894 @7792
    goto block_895; // @7793
    // Block 895 @7793
    return;
    // Block 896 @7797
    local_0 = (local_0 + 1);
    continue;  // back to loop header @7759
    // Block 897 @7806
    return;
}

void func_7807(void) {
    // Block 898 @7807
    goto block_900; // @7817
    // Block 899 @7813
    if (!((local_5 == 0))) goto block_906; // @7864
    // Block 900 @7817
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_IsReady(0);
    if (!(0)) goto block_905; // @7863
    // Block 901 @7831
    goto block_902; // @7832
    // Block 902 @7832
    if (!(0)) goto block_905; // @7863
    // Block 903 @7840
    goto block_904; // @7841
    // Block 904 @7841
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_Speech2(0, 926, &local_0);
    local_0 = (local_0 + 0.1f);
    // STORE: 0 = 1;
    // Block 905 @7863
    goto block_907; // @7868
    // Block 906 @7864
    if (!((local_5 == 1))) goto block_913; // @7946
    // Block 907 @7868
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_IsReady(0);
    if (!(0)) goto block_909; // @7883
    // Block 908 @7882
    goto block_910; // @7913
    // Block 909 @7883
    SC_PC_Get();
    SC_P_GetWillTalk(0);
    local_0 = 0;
    SC_PC_Get();
    SC_P_Speech2(1, 927, &local_0);
    local_0 = (local_0 + 0.1f);
    // STORE: 0 = 100;
    // Block 910 @7913
    phi_910_11_1371 = phi(b908:data_1966, b909:data_1968)
    SC_P_GetBySideGroupMember(1, 0, 0);
    if (!(5.0f)) goto block_912; // @7944
    // Block 911 @7929
    phi_910_11_1371 = phi(b908:data_1966, b909:data_1968)
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_Ai_SetMode(0, SC_P_AI_MODE_BATTLE);
    // STORE: 0 = 2;
    // Block 912 @7944
    phi_910_11_1371 = phi(b908:data_1966, b909:data_1968)
    goto block_914; // @7950
    // Block 913 @7946
    if (!((local_5 == 2))) goto block_917; // @7997
    // Block 914 @7950
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_Ai_GetShooting(0, &local_1);
    if (!(&local_1)) goto block_916; // @7995
    // Block 915 @7965
    SC_PC_Get();
    SC_P_GetWillTalk(0);
    local_0 = 0;
    SC_PC_Get();
    SC_P_Speech2(0, 929, &local_0);
    local_0 = (local_0 + 0.1f);
    // STORE: 0 = 3;
    // Block 916 @7995
    phi_916_23_1398 = phi(b914:data_1983, b915:data_1984)
    goto block_918; // @8001
    // Block 917 @7997
    if (!((local_5 == 3))) goto block_924; // @8112
    // Block 918 @8001
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_IsReady(0);
    if (!(0)) goto block_920; // @8016
    // Block 919 @8015
    goto block_921; // @8046
    // Block 920 @8016
    SC_PC_Get();
    SC_P_GetWillTalk(0);
    local_0 = 0;
    SC_PC_Get();
    SC_P_Speech2(1, 927, &local_0);
    local_0 = (local_0 + 0.1f);
    // STORE: 0 = 100;
    // Block 921 @8046
    phi_921_26_1425 = phi(b920:data_1991, b919:data_1989)
    // STORE: 0 = (0 + param_1);
    if (!((0 > 3.0f))) goto block_923; // @8110
    // Block 922 @8056
    phi_921_26_1425 = phi(b920:data_1991, b919:data_1989)
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_Ai_SetMode(0, SC_P_AI_MODE_PEACE);
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_Ai_Go(0, 0);
    SC_PC_Get();
    SC_P_GetWillTalk(0);
    local_0 = (0 + 0.2f);
    SC_PC_Get();
    SC_P_Speech2(0, 930, &local_0);
    local_0 = (local_0 + 0.1f);
    // STORE: 0 = 4;
    // Block 923 @8110
    phi_921_26_1425 = phi(b920:data_1991, b919:data_1989)
    goto block_925; // @8116
    // Block 924 @8112
    if (!((local_5 == 4))) goto block_928; // @8148
    // Block 925 @8116
    SC_P_GetBySideGroupMember(1, 0, 0);
    if (!(5.0f)) goto block_927; // @8147
    // Block 926 @8132
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_Ai_SetMode(0, SC_P_AI_MODE_BATTLE);
    // STORE: 0 = 5;
    // Block 927 @8147
    goto block_928; // @8148
    // Block 928 @8148
    if (!(0)) goto block_930; // @8152
    // Block 929 @8151
    goto block_935; // @8214
    // Block 930 @8152
    SC_P_GetBySideGroupMember(1, 0, 1);
    SC_P_IsReady(1);
    if (!(1)) goto block_932; // @8167
    // Block 931 @8166
    goto block_935; // @8214
    // Block 932 @8167
    SC_P_GetBySideGroupMember(1, 0, 2);
    SC_P_IsReady(2);
    if (!(2)) goto block_934; // @8182
    // Block 933 @8181
    goto block_935; // @8214
    // Block 934 @8182
    // STORE: 0 = 1;
    SC_PC_Get();
    SC_P_GetWillTalk(0);
    local_0 = (0 + 0.5f);
    SC_PC_Get();
    SC_P_Speech2(1, 928, &local_0);
    local_0 = (local_0 + 0.1f);
    // Block 935 @8214
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    if (!(0)) goto block_937; // @8217
    // Block 936 @8216
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    goto block_944; // @8294
    // Block 937 @8217
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    SC_P_GetBySideGroupMember(1, 0, 5);
    SC_P_IsReady(5);
    if (!(5)) goto block_939; // @8232
    // Block 938 @8231
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    goto block_944; // @8294
    // Block 939 @8232
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    SC_P_GetBySideGroupMember(1, 0, 4);
    SC_P_IsReady(4);
    if (!(4)) goto block_941; // @8247
    // Block 940 @8246
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    goto block_944; // @8294
    // Block 941 @8247
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_IsReady(0);
    if (!(0)) goto block_943; // @8262
    // Block 942 @8261
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    goto block_944; // @8294
    // Block 943 @8262
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    // STORE: 0 = 1;
    SC_PC_Get();
    SC_P_GetWillTalk(0);
    local_0 = (0 + 0.5f);
    SC_PC_Get();
    SC_P_Speech2(1, 931, &local_0);
    local_0 = (local_0 + 0.1f);
    // Block 944 @8294
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    if (!((0 != 100))) goto block_948; // @8369
    // Block 945 @8298
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    if (!(0)) goto block_948; // @8369
    // Block 946 @8306
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    goto block_947; // @8307
    // Block 947 @8307
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    SC_P_GetBySideGroupMember(1, 1, 0);
    rand();
    t8322_0 = 0 + (947 % 2);
    SC_P_Speech2(1, t8322_0, &local_0);
    local_0 = (local_0 + 0.1f);
    SC_P_GetBySideGroupMember(1, 1, 0);
    SC_P_Ai_SetMode(0, SC_P_AI_MODE_BATTLE);
    SC_P_GetBySideGroupMember(1, 1, 1);
    SC_P_Ai_SetMode(1, SC_P_AI_MODE_BATTLE);
    SC_P_GetBySideGroupMember(1, 1, 2);
    SC_P_Ai_SetMode(2, SC_P_AI_MODE_BATTLE);
    // STORE: 0 = 100;
    // Block 948 @8369
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    if (!((0 != 100))) goto block_952; // @8444
    // Block 949 @8373
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    if (!(1)) goto block_952; // @8444
    // Block 950 @8381
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    goto block_951; // @8382
    // Block 951 @8382
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    SC_P_GetBySideGroupMember(1, 1, 1);
    rand();
    t8397_0 = 1 + (947 % 2);
    SC_P_Speech2(1, t8397_0, &local_0);
    local_0 = (local_0 + 0.1f);
    SC_P_GetBySideGroupMember(1, 1, 0);
    SC_P_Ai_SetMode(0, SC_P_AI_MODE_BATTLE);
    SC_P_GetBySideGroupMember(1, 1, 1);
    SC_P_Ai_SetMode(1, SC_P_AI_MODE_BATTLE);
    SC_P_GetBySideGroupMember(1, 1, 2);
    SC_P_Ai_SetMode(2, SC_P_AI_MODE_BATTLE);
    // STORE: 0 = 100;
    // Block 952 @8444
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    if (!((0 != 100))) goto block_956; // @8519
    // Block 953 @8448
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    if (!(2)) goto block_956; // @8519
    // Block 954 @8456
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    goto block_955; // @8457
    // Block 955 @8457
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    SC_P_GetBySideGroupMember(1, 1, 2);
    rand();
    t8472_0 = 2 + (947 % 2);
    SC_P_Speech2(1, t8472_0, &local_0);
    local_0 = (local_0 + 0.1f);
    SC_P_GetBySideGroupMember(1, 1, 0);
    SC_P_Ai_SetMode(0, SC_P_AI_MODE_BATTLE);
    SC_P_GetBySideGroupMember(1, 1, 1);
    SC_P_Ai_SetMode(1, SC_P_AI_MODE_BATTLE);
    SC_P_GetBySideGroupMember(1, 1, 2);
    SC_P_Ai_SetMode(2, SC_P_AI_MODE_BATTLE);
    // STORE: 0 = 100;
    // Block 956 @8519
    phi_935_48_1525 = phi(b933:data_2020, b934:data_2024)
    phi_944_55_1532 = phi(b942:data_2033, b943:data_2037)
    goto block_958; // @8526
    // Block 957 @8522
    if (!((local_5 == 0))) goto block_959; // @8528
    // Block 958 @8526
    goto block_960; // @8532
    // Block 959 @8528
    if (!((local_5 == 1))) goto block_961; // @8654
    // Block 960 @8532
    SC_P_GetBySideGroupMember(1, 1, 0);
    SC_P_Ai_SetMode(0, SC_P_AI_MODE_PEACE);
    SC_P_GetBySideGroupMember(1, 1, 1);
    SC_P_Ai_SetMode(1, SC_P_AI_MODE_PEACE);
    SC_P_GetBySideGroupMember(1, 1, 2);
    SC_P_Ai_SetMode(2, SC_P_AI_MODE_PEACE);
    SC_P_GetBySideGroupMember(1, 1, 0);
    SC_P_Ai_Stop(0);
    SC_P_GetBySideGroupMember(1, 1, 1);
    SC_P_Ai_Stop(1);
    SC_P_GetBySideGroupMember(1, 1, 2);
    SC_P_Ai_Stop(2);
    frnd(20.0f);
    (25.0f + 20.0f) = 0;
    rand();
    // STORE: 0 = (2 % 2);
    SC_P_GetBySideGroupMember(1, 1, 0);
    SC_P_GetPos(0, &local_2);
    SC_P_GetBySideGroupMember(1, 1, 2);
    SC_P_Ai_Go(2, &local_2);
    SC_P_GetBySideGroupMember(1, 1, 2);
    SC_P_GetPos(2, 0);
    // STORE: 0 = 2;
    goto block_962; // @8658
    // Block 961 @8654
    if (!((local_5 == 2))) goto block_980; // @8917
    // Block 962 @8658
    goto block_964; // @8665
    // Block 963 @8661
    if (!((local_6 == 0))) goto block_965; // @8666
    // Block 964 @8665
    goto block_966; // @8670
    // Block 965 @8666
    if (!((local_6 == 1))) goto block_969; // @8736
    // Block 966 @8670
    SC_P_GetBySideGroupMember(1, 1, 2);
    SC_P_GetBySideGroupMember(1, 1, 0);
    SC_P_GetDistance(1, 0);
    if (!((0 < 3.0f))) goto block_968; // @8734
    // Block 967 @8694
    SC_P_GetBySideGroupMember(1, 1, 2);
    rand();
    t8709_0 = 2 + (945 % 2);
    SC_P_Speech2(1, t8709_0, &local_0);
    local_0 = (local_0 + 0.1f);
    SC_P_GetBySideGroupMember(1, 1, 2);
    SC_P_Ai_Go(2, 0);
    // STORE: 0 = 2;
    // Block 968 @8734
    goto block_970; // @8740
    // Block 969 @8736
    if (!((local_6 == 2))) goto block_973; // @8788
    // Block 970 @8740
    SC_P_GetBySideGroupMember(1, 1, 2);
    if (!(3.0f)) goto block_972; // @8787
    // Block 971 @8756
    rand();
    // STORE: 0 = (0 % 2);
    SC_P_GetBySideGroupMember(1, 1, 0);
    SC_P_GetPos(0, &local_2);
    SC_P_GetBySideGroupMember(1, 1, 2);
    SC_P_Ai_Go(2, &local_2);
    // Block 972 @8787
    phi_972_158_2391 = phi(b970:&data_1763, b971:data_2165)
    goto block_973; // @8788
    // Block 973 @8788
    // STORE: 0 = (0 - param_1);
    if (!((0 < 0))) goto block_975; // @8844
    // Block 974 @8799
    frnd(20.0f);
    (25.0f + 20.0f) = 0;
    local_0 = 0;
    rand();
    t8822_0 = 1 % 2;
    SC_P_GetBySideGroupMember(&local_2, 1, t8822_0);
    rand();
    t8834_0 = t8822_0 + (939 % 3);
    SC_P_Speech2(1, t8834_0, &local_0);
    local_0 = (local_0 + 0.1f);
    // Block 975 @8844
    // STORE: 0 = (0 - param_1);
    if (!((0 < 0))) goto block_977; // @8880
    // Block 976 @8854
    frnd(5.0f);
    (5.0f + 5.0f) = 0;
    SC_P_GetBySideGroupMember(1, 1, 0);
    SC_P_GetPos(0, &local_2);
    SC_SND_PlaySound3D(10419, &local_2);
    // Block 977 @8880
    // STORE: 0 = (0 - param_1);
    if (!((0 < 0))) goto block_979; // @8916
    // Block 978 @8890
    frnd(5.0f);
    (5.0f + 5.0f) = 0;
    SC_P_GetBySideGroupMember(1, 1, 1);
    SC_P_GetPos(1, &local_2);
    SC_SND_PlaySound3D(10419, &local_2);
    // Block 979 @8916
    goto block_980; // @8917
    // Block 980 @8917
    return;
}

void func_8919(void) {
    // Block 981 @8919
    SC_SetObjectScript(&"grenadebedna", &"levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\openablecr...");
    SC_SetObjectScript(&"n_poklop_01", &"levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\poklop.c");
    SC_SetObjectScript(&"d_past_04_01", &"levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\past.c");
    return;
}

void func_8932(void) {
    // Block 982 @8932
    return;
}

void func_8933(void) {
    // Block 983 @8933
    return;
}

void func_8934(void) {
    // Block 984 @8934
    SC_PC_Get();
    SC_P_GetWillTalk();
    local_0 = unknown_984_8945_1;
    if (!(0)) goto block_986; // @8950
    // Block 985 @8949
    goto block_989; // @8985
    // Block 986 @8950
    SC_NOD_GetName(&param_1);
    SC_StringSame(&param_1, &"grenadebedna");
    if (!(&"grenadebedna")) goto block_989; // @8985
    // Block 987 @8965
    goto block_988; // @8966
    // Block 988 @8966
    SC_PC_Get();
    SC_P_Speech2(&param_1, 923, &local_0);
    local_0 = (local_0 + 0.1f);
    // STORE: 0 = 1;
    return;
    // Block 989 @8985
    if (!(0)) goto block_991; // @8988
    // Block 990 @8987
    goto block_994; // @9023
    // Block 991 @8988
    SC_NOD_GetName(&param_1);
    SC_StringSame(&param_1, &"n_poklop_01");
    if (!(&"n_poklop_01")) goto block_994; // @9023
    // Block 992 @9003
    goto block_993; // @9004
    // Block 993 @9004
    SC_PC_Get();
    SC_P_Speech2(&param_1, 938, &local_0);
    local_0 = (local_0 + 0.1f);
    // STORE: 0 = 1;
    return;
    // Block 994 @9023
    SC_NOD_GetName(&param_1);
    SC_StringSame(&param_1, &"granat_v_plechovce2#3");
    if (!(&"granat_v_plechovce2#3")) goto block_996; // @9053
    // Block 995 @9038
    SC_PC_Get();
    SC_P_Speech2(&param_1, 925, &local_0);
    local_0 = (local_0 + 0.1f);
    return;
    // Block 996 @9053
    return;
}

void ScriptMain(void) {
    // Block 997 @9054
    param_2 = 3;
    goto block_999; // @9074
    // Block 998 @9070
    if (!((local_5 == 7))) goto block_1000; // @9077
    // Block 999 @9074
    goto block_1001; // @9081
    // Block 1000 @9077
    if (!((local_5 == 11))) goto block_1002; // @9084
    // Block 1001 @9081
    goto block_1003; // @9088
    // Block 1002 @9084
    if (!((local_5 == 8))) goto block_1004; // @9091
    // Block 1003 @9088
    goto block_1005; // @9095
    // Block 1004 @9091
    if (!((local_5 == 4))) goto block_1009; // @9111
    // Block 1005 @9095
    goto block_1007; // @9104
    // Block 1006 @9100
    if (!((local_21 == 51))) goto block_1008; // @9108
    // Block 1007 @9104
    goto block_1008; // @9108
    // Block 1008 @9108
    goto block_1010; // @9115
    // Block 1009 @9111
    if (!((local_5 == 0))) goto block_1018; // @9439
    // Block 1010 @9115
    goto block_1012; // @9122
    // Block 1011 @9118
    if (!((local_21 == 0))) goto block_1013; // @9351
    // Block 1012 @9122
    SC_sgi(SGI_CURRENTMISSION, 9);
    SC_ZeroMem(&local_2, 8);
    SC_ZeroMem(&local_1, 20);
    SC_DeathCamera_Enable(0);
    SC_RadioSetDist(10.0f);
    SC_ZeroMem(&local_22, 8);
    local_22 = 32;
    *(&local_22 + 4) = 8;
    SC_InitSide(0, &local_22);
    SC_ZeroMem(&local_22, 8);
    local_22 = 64;
    *(&local_22 + 4) = 16;
    SC_InitSide(1, &local_22);
    SC_ZeroMem(&local_22, 20);
    local_22 = 0;
    *(&local_22 + 4) = 0;
    *(&local_22 + 8) = 4;
    *(&local_22 + 16) = 30.0f;
    SC_InitSideGroup(&local_22);
    SC_ZeroMem(&local_22, 20);
    local_22 = 1;
    *(&local_22 + 4) = 0;
    *(&local_22 + 8) = 9;
    SC_InitSideGroup(&local_22);
    SC_ZeroMem(&local_22, 20);
    local_22 = 1;
    *(&local_22 + 4) = 1;
    *(&local_22 + 8) = 16;
    SC_InitSideGroup(&local_22);
    SC_ZeroMem(&local_22, 20);
    local_22 = 1;
    *(&local_22 + 4) = 2;
    *(&local_22 + 8) = 16;
    SC_InitSideGroup(&local_22);
    SC_ZeroMem(&local_22, 20);
    local_22 = 1;
    *(&local_22 + 4) = 3;
    *(&local_22 + 8) = 9;
    SC_InitSideGroup(&local_22);
    SC_Ai_SetShootOnHeardEnemyColTest(1);
    SC_Ai_SetGroupEnemyUpdate(1, 0, 0);
    SC_Ai_SetGroupEnemyUpdate(1, 1, 0);
    SC_Ai_SetGroupEnemyUpdate(1, 2, 0);
    SC_Ai_SetGroupEnemyUpdate(1, 3, 0);
    // STORE: 0 = 1;
    SC_sgi(SGI_LEVELPHASE, 1);
    SC_Log(1702257996, 1, 3);
    SC_Osi(&"Levelphase changed to %d", 1, 2);
    SC_SetCommandMenu(2009);
    param_2 = 3;
    goto block_1014; // @9355
    // Block 1013 @9351
    if (!((local_21 == 1))) goto block_1015; // @9412
    // Block 1014 @9355
    local_1 = 1.0f;
    SC_AGS_Set(0);
    SC_PC_Get();
    SC_P_SpeechMes2(0, 900, &local_1, 1);
    local_1 = (local_1 + 0.1f);
    // STORE: 0 = 2;
    SC_sgi(SGI_LEVELPHASE, 2);
    SC_Log(1702257996, 2, 3);
    SC_Osi(&"Levelphase changed to %d", 2, 2);
    goto block_1016; // @9416
    // Block 1015 @9412
    if (!((local_21 == 2))) goto block_1017; // @9436
    // Block 1016 @9416
    SC_PC_GetPos(&local_9);
    goto block_1017; // @9436
    // Block 1017 @9436
    goto block_1019; // @9443
    // Block 1018 @9439
    if (!((local_5 == 1))) goto block_1025; // @9682
    // Block 1019 @9443
    SC_PC_Get();
    SC_P_GetWillTalk(&param_2);
    param_2 = &local_1;
    SC_PC_EnableMovement(0);
    SC_PC_EnableRadioBreak(1);
    goto block_1021; // @9470
    // Block 1020 @9466
    if (!((local_21 == 1))) goto block_1022; // @9573
    // Block 1021 @9470
    SC_RadioBatch_Begin();
    SC_PC_Get();
    SC_P_Speech2(&param_2, 916, &local_1);
    local_1 = (local_1 + 0.1f);
    local_1 = (local_1 + 0.3f);
    SC_SpeechRadio2(917, &local_1);
    local_1 = (local_1 + (0.1f + 0.2f));
    SC_PC_Get();
    SC_P_Speech2(&local_1, 918, &local_1);
    local_1 = (local_1 + 0.1f);
    local_1 = (local_1 + 0.3f);
    SC_SpeechRadio2(919, &local_1);
    local_1 = (local_1 + (0.1f + 0.2f));
    SC_PC_Get();
    SC_P_SpeechMes2(&local_1, 920, &local_1, 2);
    local_1 = (local_1 + 0.1f);
    SC_RadioBatch_End();
    goto block_1023; // @9577
    // Block 1022 @9573
    if (!((local_21 == 2))) goto block_1024; // @9679
    // Block 1023 @9577
    SC_RadioBatch_Begin();
    SC_PC_Get();
    SC_P_Speech2(2, 933, &local_1);
    local_1 = (local_1 + 0.1f);
    local_1 = (local_1 + 0.3f);
    SC_SpeechRadio2(934, &local_1);
    local_1 = (local_1 + (0.1f + 0.2f));
    SC_PC_Get();
    SC_P_Speech2(&local_1, 935, &local_1);
    local_1 = (local_1 + 0.1f);
    local_1 = (local_1 + 0.3f);
    SC_SpeechRadio2(936, &local_1);
    local_1 = (local_1 + (0.1f + 0.2f));
    SC_PC_Get();
    SC_P_SpeechMes2(&local_1, 937, &local_1, 3);
    local_1 = (local_1 + 0.1f);
    SC_RadioBatch_End();
    goto block_1024; // @9679
    // Block 1024 @9679
    goto block_1026; // @9686
    // Block 1025 @9682
    if (!((local_5 == 2))) goto block_1055; // @10012
    // Block 1026 @9686
    goto block_1028; // @9695
    // Block 1027 @9691
    if (!((local_21 == 1))) goto block_1032; // @9747
    // Block 1028 @9695
    if (!(&param_2)) goto block_1030; // @9705
    // Block 1029 @9704
    goto block_1031; // @9745
    // Block 1030 @9705
    (0 + (&param_2 * 4)) = 1;
    *(&local_22 + 8) = 0;
    local_22 = 9110;
    *(&local_22 + 4) = 9111;
    SC_MissionSave(&local_22);
    SC_Log(1769365843, 9110, 3);
    SC_Osi(&"Saving game id %d", 9110, 2);
    // Block 1031 @9745
    goto block_1033; // @9751
    // Block 1032 @9747
    if (!((local_21 == 2))) goto block_1037; // @9806
    // Block 1033 @9751
    if (!(2)) goto block_1035; // @9761
    // Block 1034 @9760
    goto block_1036; // @9804
    // Block 1035 @9761
    (0 + (&param_2 * 4)) = 1;
    SC_PC_EnableMovement(1);
    *(&local_22 + 8) = 0;
    local_22 = 9112;
    *(&local_22 + 4) = 9113;
    SC_MissionSave(&local_22);
    SC_Log(1769365843, 9112, 3);
    SC_Osi(&"Saving game id %d", 9112, 2);
    // Block 1036 @9804
    goto block_1038; // @9810
    // Block 1037 @9806
    if (!((local_21 == 3))) goto block_1042; // @9865
    // Block 1038 @9810
    if (!(2)) goto block_1040; // @9820
    // Block 1039 @9819
    goto block_1041; // @9863
    // Block 1040 @9820
    (0 + (&param_2 * 4)) = 1;
    SC_PC_EnableMovement(1);
    *(&local_22 + 8) = 0;
    local_22 = 9114;
    *(&local_22 + 4) = 9115;
    SC_MissionSave(&local_22);
    SC_Log(1769365843, 9114, 3);
    SC_Osi(&"Saving game id %d", 9114, 2);
    // Block 1041 @9863
    goto block_1043; // @9869
    // Block 1042 @9865
    if (!((local_21 == 11))) goto block_1044; // @9874
    // Block 1043 @9869
    SC_Radio_Enable(1);
    goto block_1045; // @9878
    // Block 1044 @9874
    if (!((local_21 == 12))) goto block_1046; // @9895
    // Block 1045 @9878
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_GetPos(0, &local_9);
    SC_SND_PlaySound3D(2055, &local_9);
    goto block_1047; // @9899
    // Block 1046 @9895
    if (!((local_21 == 13))) goto block_1048; // @9969
    // Block 1047 @9899
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_GetPos(0, &local_9);
    SC_SND_PlaySound3D(2060, &local_9);
    SC_P_GetBySideGroupMember(1, 0, 1);
    SC_P_GetPos(1, &local_9);
    SC_SND_PlaySound3D(2070, &local_9);
    SC_GetWp(&"WayPoint53", &local_9);
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_SetPos(0, &local_9);
    SC_GetWp(&"WayPoint#9", &local_9);
    SC_P_GetBySideGroupMember(1, 0, 1);
    SC_P_SetPos(1, &local_9);
    goto block_1049; // @9973
    // Block 1048 @9969
    if (!((local_21 == 14))) goto block_1050; // @9994
    // Block 1049 @9973
    SC_GetWp(&"WayPoint57", &local_9);
    SC_P_GetBySideGroupMember(1, 0, 0);
    SC_P_SetPos(0, &local_9);
    goto block_1051; // @9998
    // Block 1050 @9994
    if (!((local_21 == 15))) goto block_1052; // @10003
    // Block 1051 @9998
    SC_Radio_Enable(2);
    goto block_1053; // @10007
    // Block 1052 @10003
    if (!((local_21 == 100))) goto block_1054; // @10009
    // Block 1053 @10007
    goto block_1054; // @10009
    // Block 1054 @10009
    goto block_1056; // @10016
    // Block 1055 @10012
    if (!((local_5 == 15))) goto block_1060; // @10047
    // Block 1056 @10016
    t10020_0 = UGEQ(&param_2, 20);
    if (!(t10020_0)) goto block_1058; // @10028
    // Block 1057 @10022
    param_2 = 0;
    goto block_1059; // @10046
    // Block 1058 @10028
    param_2 = 2;
    param_2 = 0;
    // Block 1059 @10046
    phi_1059_167_5087 = phi(b1057:data_2520, b1058:data_2526)
    goto block_1060; // @10047
    // Block 1060 @10047
    return;
}

