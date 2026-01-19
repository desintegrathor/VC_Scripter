// Structured decompilation of decompilation/LEVEL/LEVEL.SCR
// Functions: 28

int _init(s_SC_OBJ_info *info) {
    // Block 0 @0
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    DLD();
    return FALSE;
}

int func_0291(s_SC_OBJ_info *info) {
    // Block 1 @291
    frnd(j);
    local_0 = j;
    if (!((i < 0))) {
        // Block 3 @310
        return i;
    } else {
        // Block 2 @305
        local_0 = (-i);
    }
    // Block 4 @313
    SC_P_Ai_SetMode(retval, SC_P_AI_MODE_BATTLE);
    SC_P_Ai_EnableShooting(retval, TRUE);
    SC_P_Ai_EnableSituationUpdate(retval, 1);
    SC_Log(2036427856, retval, SCM_WARNABOUTENEMY);
    return FALSE;
    // Block 5 @332
    SC_P_Ai_SetMode(retval, SC_P_AI_MODE_PEACE);
    SC_P_Ai_EnableShooting(retval, FALSE);
    SC_P_Ai_EnableSituationUpdate(retval, 0);
    SC_P_Ai_Stop(retval);
    SC_Log(2036427856, retval, SCM_WARNABOUTENEMY);
    return FALSE;
}

int func_0354(s_SC_OBJ_info *info) {
    // Block 6 @354
    if (!(j)) {
        // Block 8 @357
        SC_Log(1936942413, j, retval, SCM_BOOBYTRAPFOUND);
        return FALSE;
    } else {
        // Block 7 @356
        // Block 9 @365
        SC_P_ScriptMessage(j, j, retval);
        return FALSE;
    }
}

int func_0371(s_SC_OBJ_info *info) {
    // Block 10 @371
    SC_P_GetBySideGroupMember(1, i, i);
    SC_P_Ai_GetSureEnemies(i);
    if (!(i)) {
        // Block 12 @388
        SC_P_GetBySideGroupMember(1, i, i);
        SC_P_Ai_GetDanger(i);
        // Block 13 @404
        return FALSE;
        // Block 14 @407
        return FALSE;
    } else {
        // Block 11 @385
        return FALSE;
    }
    // Block 15 @410
    SC_P_Ai_GetSureEnemies(i);
    if (!(i)) {
        // Block 17 @420
        SC_P_Ai_GetDanger(i);
        // Block 18 @429
        return FALSE;
        // Block 19 @432
        return FALSE;
    } else {
        // Block 16 @417
        return FALSE;
    }
    // Block 20 @435
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(i, &ai_props);
    ai_props.field19 = retval;
    SC_P_Ai_SetProps(i, &ai_props);
    return &ai_props;
    // Block 21 @454
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(i, &ai_props);
    ai_props.field11 = retval;
    SC_P_Ai_SetProps(i, &ai_props);
    return &ai_props;
    // Block 22 @473
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(i, &ai_props);
    ai_props.field5 = (t484_0 * retval);
    SC_P_Ai_SetProps(i, &ai_props);
    return &ai_props;
    // Block 23 @496
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(i, &ai_props);
    ai_props.field18 = (t507_0 * retval);
    SC_P_Ai_SetProps(i, &ai_props);
    return &ai_props;
    // Block 24 @519
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(i, &ai_props);
    if (!(retval)) {
        // Block 26 @536
        ai_props.field16 = 1000.0f;
    } else {
        // Block 25 @530
        ai_props.field16 = 5.0f;
    }
    // Block 27 @541
    SC_P_Ai_SetProps(i, &ai_props);
    return &ai_props;
    // Block 28 @546
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(i, &ai_props);
    ai_props.field25 = retval;
    SC_P_Ai_SetProps(i, &ai_props);
    return &ai_props;
    // Block 29 @565
    SC_ggi(SGI_CURRENTMISSION);
    return FALSE;
    // Block 30 @573
    SC_ggi(SCM_HEARDSOMETHING);
    return FALSE;
    // Block 31 @581
    SC_P_GetInfo(i, &ai_props);
    return t587_0;
    // Block 32 @590
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(i, &ai_props);
    ai_props = retval;
    SC_P_Ai_SetProps(i, &ai_props);
    return &ai_props;
    // Block 33 @608
    SC_ggi(101);
    *t615_0 = 101;
    if (!(t620_0)) {
        // Block 35 @623
        *t625_0 = SCM_RUNANDKILL;
    } else {
        // Block 34 @622
    }
    // Block 36 @628
    if (!((t630_0 == 255))) {
        // Block 38 @639
        SC_ggi(102);
        *t646_0 = 102;
        // Block 39 @653
        // Block 40 @654
        *t656_0 = SCM_HEARDSOMETHING;
        // Block 41 @659
        // Block 42 @665
        *t667_0 = 0;
        // Block 43 @670
        SC_ggi(103);
        *t677_0 = 103;
        // Block 44 @684
        // Block 45 @685
        SC_ggi(SGI_CURRENTMISSION);
        // Block 46 @694
        *t696_0 = SCM_RETREAT;
        // Block 47 @700
        SC_ggi(SGI_CURRENTMISSION);
        // Block 48 @709
        *t711_0 = SCM_STARTWALK;
        // Block 49 @715
        *t717_0 = 1;
        // Block 50 @720
        // Block 51 @726
        *t728_0 = 0;
        // Block 52 @731
        SC_ggi(104);
        *t738_0 = 104;
        // Block 53 @747
        *t749_0 = 0;
        // Block 54 @752
        SC_ggi(105);
        *t759_0 = 105;
        // Block 55 @766
        // Block 56 @767
        *t769_0 = SCM_DISABLEINTERACTION;
        // Block 57 @772
        // Block 58 @778
        *t780_0 = 0;
        // Block 59 @783
        SC_ggi(106);
        *t790_0 = 106;
        // Block 60 @799
        *t801_0 = 0;
        // Block 61 @804
        SC_ggi(107);
        *t811_0 = 107;
        // Block 62 @820
        *t822_0 = 0;
        // Block 63 @825
        SC_ggi(108);
        *t832_0 = 108;
        // Block 64 @839
        // Block 65 @840
        *t842_0 = SCM_RADIOCOM;
        // Block 66 @845
        // Block 67 @851
        *t853_0 = 0;
        // Block 68 @856
        SC_ggi(109);
        *t863_0 = 109;
        // Block 69 @872
        *t874_0 = 0;
        // Block 70 @877
        *t879_0 = SCM_ENABLEINTERACTION;
        return FALSE;
    } else {
        // Block 37 @634
        *t636_0 = 0;
    }
}

int func_0883(s_SC_OBJ_info *info) {
    // Block 71 @883
    SC_PC_Get();
    SC_P_GetWeapons();
    if (!(t897_0)) {
        // Block 73 @906
        SC_sgi(101, 255);
    } else {
        // Block 72 @899
        SC_sgi(101, t902_0);
    }
    // Block 74 @910
    if (!(t912_0)) {
        // Block 76 @921
        SC_sgi(102, 255);
    } else {
        // Block 75 @914
        SC_sgi(102, t917_0);
    }
    // Block 77 @925
    if (!(t927_0)) {
        // Block 79 @936
        SC_sgi(103, 255);
    } else {
        // Block 78 @929
        SC_sgi(103, t932_0);
    }
    // Block 80 @940
    if (!(t942_0)) {
        // Block 82 @951
        SC_sgi(104, 255);
    } else {
        // Block 81 @944
        SC_sgi(104, t947_0);
    }
    // Block 83 @955
    if (!(t957_0)) {
        // Block 85 @966
        SC_sgi(105, 255);
    } else {
        // Block 84 @959
        SC_sgi(105, t962_0);
    }
    // Block 86 @970
    if (!(t972_0)) {
        // Block 88 @981
        SC_sgi(106, 255);
    } else {
        // Block 87 @974
        SC_sgi(106, t977_0);
    }
    // Block 89 @985
    if (!(t987_0)) {
        // Block 91 @996
        SC_sgi(107, 255);
    } else {
        // Block 90 @989
        SC_sgi(107, t992_0);
    }
    // Block 92 @1000
    if (!(t1002_0)) {
        // Block 94 @1011
        SC_sgi(108, 255);
    } else {
        // Block 93 @1004
        SC_sgi(108, t1007_0);
    }
    // Block 95 @1015
    if (!(t1017_0)) {
        // Block 97 @1026
        SC_sgi(109, 255);
    } else {
        // Block 96 @1019
        SC_sgi(109, t1022_0);
    }
    // Block 98 @1030
    if (!(t1032_0)) {
        // Block 100 @1041
        SC_sgi(110, 255);
    } else {
        // Block 99 @1034
        SC_sgi(110, t1037_0);
    }
    // Block 101 @1045
    return t1037_0;
    // Block 102 @1046
    SC_PC_Get();
    SC_P_ReadHealthFromGlobalVar();
    return FALSE;
}

int func_1054(s_SC_OBJ_info *info) {
    // Block 103 @1054
    SC_PC_Get();
    SC_P_WriteHealthToGlobalVar();
    return FALSE;
    // Block 104 @1062
    SC_PC_Get();
    SC_P_ReadAmmoFromGlobalVar();
    SC_ggi(90);
    if (!(90)) {
        // Block 106 @1090
        SC_ggi(91);
        // Block 107 @1097
        SC_PC_Get();
        SC_ggi(91);
        SC_P_SetAmmoInWeap(90, 1, 91);
        // Block 108 @1110
        return FALSE;
    } else {
        // Block 105 @1077
        SC_PC_Get();
        SC_ggi(90);
        SC_P_SetAmmoInWeap(89, SCM_RUN, 90);
    }
}

int func_1111(s_SC_OBJ_info *info) {
    // Block 109 @1111
    SC_PC_Get();
    SC_P_WriteAmmoToGlobalVar();
    SC_PC_Get();
    SC_P_GetAmmoInWeap(90, SCM_RUN);
    SC_sgi(90, SCM_RUN);
    SC_PC_Get();
    SC_P_GetAmmoInWeap(91, 1);
    SC_sgi(91, 1);
    return FALSE;
}

int func_1146(s_SC_OBJ_info *info) {
    // Block 110 @1146
    SC_PC_GetIntel(&local_0);
    local_2 = 0;
    // Block 111 @1155
    if (!((idx < SCM_DISABLE))) {
        // Block 113 @1179
        return idx;
    } else {
        // Block 111 @1155
        // Block 112 @1159
        SC_sgi((SCM_CAREFULLASSAULT + idx), t1167_0);
        local_2 = (idx + 1);
    }
    // Block 114 @1180
    local_2 = 0;
    // Block 115 @1186
    if (!((idx < SCM_DISABLE))) {
        // Block 117 @1214
        SC_PC_SetIntel(&local_0);
        return &local_0;
    } else {
        // Block 115 @1186
        // Block 116 @1190
        SC_ggi((SCM_CAREFULLASSAULT + idx));
        (&local_0 + (idx * SCM_BOOBYTRAPFOUND)) = (SCM_CAREFULLASSAULT + idx);
        local_2 = (idx + 1);
    }
    // Block 118 @1218
    SC_MissionCompleted();
    return FALSE;
}

int func_1223(s_SC_OBJ_info *info) {
    // Block 119 @1223
    SC_Osi(&"MISSION COMPLETE", 1);
    SC_MissionDone();
    return FALSE;
    // Block 120 @1233
    SC_ShowHelp(&retval, 1, 6.0f);
    return FALSE;
    // Block 121 @1239
    local_0[0] = i;
    local_0[SCM_BOOBYTRAPFOUND] = retval;
    SC_ShowHelp(&vec2, SCM_RUN, 12.0f);
    return 12.0f;
    // Block 122 @1258
    local_0[0] = i;
    local_0[SCM_BOOBYTRAPFOUND] = i;
    local_0[SCM_SETGPHASE] = retval;
    SC_ShowHelp(&vec2, SCM_WARNABOUTENEMY, 24.0f);
    return 24.0f;
    // Block 123 @1283
    SC_ggi(SCM_DISABLE);
    return FALSE;
    // Block 124 @1291
    rand();
    vec2 = (unknown_124_1297_1 % SCM_DISARMTRAP);
    SC_ggi(SGI_CURRENTMISSION);
    if (!((SGI_CURRENTMISSION > SCM_TELEPORT))) {
        // Block 139 @1356
        // Block 140 @1360
        return SCM_HUNTER;
        // Block 141 @1363
        // Block 142 @1367
        return SCM_TIMEDRUN;
        // Block 143 @1370
        // Block 144 @1374
        return SCM_CHECKBODY;
        // Block 145 @1377
        // Block 146 @1381
        return SCM_RUN;
        // Block 147 @1384
        // Block 148 @1388
        return SCM_EXPLODETRAP;
        // Block 149 @1391
        // Block 150 @1395
        return SCM_CREATE;
        // Block 151 @1398
        return SCM_RETREAT;
    } else {
        // Block 125 @1310
        // Block 126 @1314
        return SCM_INITTRAP;
        // Block 127 @1317
        // Block 128 @1321
        return SCM_TIMEDRUN;
        // Block 129 @1324
        // Block 130 @1328
        return SCM_CHECKBODY;
        // Block 131 @1331
        // Block 132 @1335
        return SCM_RUN;
        // Block 133 @1338
        // Block 134 @1342
        return SCM_EXPLODETRAP;
        // Block 135 @1345
        // Block 136 @1349
        return SCM_CREATE;
        // Block 137 @1352
        return SCM_RETREAT;
    }
    // Block 138 @1355
    goto block_152; // @1401
    // Block 152 @1401
    rand();
    vec2 = (unknown_152_1407_1 % SCM_DISARMTRAP);
    if (!((vec2 > SCM_INITTRAP))) {
        // Block 154 @1418
        // Block 155 @1422
        return SCM_INITTRAP;
        // Block 156 @1425
        // Block 157 @1429
        return SCM_RUN;
        // Block 158 @1432
        // Block 159 @1436
        return SCM_TIMEDRUN;
        // Block 160 @1439
        return SCM_RUN;
    } else {
        // Block 153 @1415
        return SCM_CONFIRM;
    }
    // Block 161 @1442
    rand();
    vec2 = (unknown_161_1448_1 % SCM_DISARMTRAP);
    SC_ggi(SGI_CURRENTMISSION);
    goto block_163; // @1464
    switch (vec2) {
    case 1:
        // Block 163 @1464
        // Block 165 @1471
        return SCM_CHECKBODY;
    case 2:
        // Block 168 @1480
        break;
    case 3:
        // Block 170 @1485
        break;
    case 4:
        // Block 172 @1490
        break;
    case 5:
        // Block 174 @1495
        // Block 175 @1499
        return SCM_CHECKBODY;
        // Block 176 @1502
        // Block 177 @1506
        return SCM_CREATE;
        // Block 178 @1509
        return SCM_EXPLODETRAP;
    case 16:
        // Block 181 @1518
        break;
    case 17:
        // Block 183 @1523
        // Block 184 @1527
        return SCM_CHECKBODY;
        // Block 185 @1530
        // Block 186 @1534
        return SCM_EXPLODETRAP;
        // Block 187 @1537
        // Block 188 @1541
        return SCM_CREATE;
        // Block 189 @1544
        return SCM_RETREAT;
    case 6:
        // Block 192 @1553
        // Block 193 @1557
        return SCM_CHECKBODY;
        // Block 194 @1560
        // Block 195 @1564
        return SCM_EXPLODETRAP;
        // Block 196 @1567
        // Block 197 @1571
        return SCM_CREATE;
        // Block 198 @1574
        // Block 199 @1578
        return SCM_RETREAT;
        // Block 200 @1581
        return SCM_STARTWALK;
    case 7:
        // Block 203 @1590
        break;
    case 8:
        // Block 205 @1595
        break;
    case 10:
        // Block 207 @1600
        // Block 208 @1604
        return SCM_CHECKBODY;
        // Block 209 @1607
        // Block 210 @1611
        return SCM_TIMEDRUN;
        // Block 211 @1614
        // Block 212 @1618
        return SCM_CREATE;
        // Block 213 @1621
        // Block 214 @1625
        return SCM_EXPLODETRAP;
        // Block 215 @1628
        return SCM_RUN;
    case 9:
        // Block 218 @1637
        break;
    case 11:
        // Block 220 @1642
        break;
    case 23:
        // Block 222 @1647
        // Block 223 @1651
        return SCM_SETGPHASE;
        // Block 224 @1654
        // Block 225 @1658
        return SCM_ONWAYPOINT;
        // Block 226 @1661
        return SCM_DISABLE;
    case 12:
        // Block 229 @1670
        // Block 230 @1674
        return SCM_RUN;
        // Block 231 @1677
        // Block 232 @1681
        return SCM_TIMEDRUN;
        // Block 233 @1684
        // Block 234 @1688
        return SCM_EXPLODETRAP;
        // Block 235 @1691
        // Block 236 @1695
        return SCM_CREATE;
        // Block 237 @1698
        // Block 238 @1702
        return SCM_CHECKBODY;
        // Block 239 @1705
        return SCM_INITTRAP;
    case 13:
        // Block 242 @1714
        break;
    case 14:
        // Block 244 @1719
        break;
    case 15:
        // Block 246 @1724
        break;
    case 18:
        // Block 248 @1729
        // Block 249 @1733
        return SCM_RUN;
        // Block 250 @1736
        // Block 251 @1740
        return SCM_TIMEDRUN;
        // Block 252 @1743
        // Block 253 @1747
        return SCM_EXPLODETRAP;
        // Block 254 @1750
        // Block 255 @1754
        return SCM_CREATE;
        // Block 256 @1757
        // Block 257 @1761
        return SCM_CHECKBODY;
        // Block 258 @1764
        return SCM_RETREAT;
    case 19:
        // Block 261 @1772
        break;
    case 20:
        // Block 263 @1777
        break;
    case 21:
        // Block 265 @1782
        break;
    case 22:
        // Block 267 @1787
        // Block 268 @1791
        return SCM_RUN;
        // Block 269 @1794
        // Block 270 @1798
        return SCM_TIMEDRUN;
        // Block 271 @1801
        // Block 272 @1805
        return SCM_RETREAT;
        // Block 273 @1808
        return SCM_INITTRAP;
    case 24:
        // Block 276 @1817
        // Block 277 @1821
        return SCM_RUN;
        // Block 278 @1824
        // Block 279 @1828
        return SCM_EXPLODETRAP;
        // Block 280 @1831
        // Block 281 @1835
        return SCM_CREATE;
        // Block 282 @1838
        // Block 283 @1842
        return SCM_RETREAT;
        // Block 284 @1845
        // Block 285 @1849
        return SCM_CHECKBODY;
        // Block 286 @1852
        return SCM_TEAMKIA;
    case 26:
        // Block 289 @1861
        break;
    case 27:
        // Block 291 @1866
        break;
    case 28:
        // Block 293 @1871
        // Block 294 @1875
        return SCM_RUN;
        // Block 295 @1878
        // Block 296 @1882
        return SCM_TIMEDRUN;
        // Block 297 @1885
        // Block 298 @1889
        return SCM_RETREAT;
        // Block 299 @1892
        // Block 300 @1896
        return SCM_CREATE;
        // Block 301 @1899
        return SCM_INITTRAP;
    case 29:
        // Block 304 @1909
        // Block 305 @1913
        return SCM_RUN;
        // Block 306 @1916
        // Block 307 @1920
        return SCM_TIMEDRUN;
        // Block 308 @1923
        // Block 309 @1927
        return SCM_INITTRAP;
        // Block 310 @1930
        // Block 311 @1934
        return SCM_RETREAT;
        // Block 312 @1937
        return SCM_CREATE;
    case 25:
        // Block 315 @1946
        // Block 316 @1950
        return SCM_RUN;
        // Block 317 @1953
        return SCM_CONFIRM;
    case 30:
        // Block 320 @1962
        break;
    case 31:
        // Block 322 @1967
        break;
    case 32:
        // Block 324 @1972
        // Block 325 @1976
        return SCM_RUN;
        // Block 326 @1979
        // Block 327 @1983
        return SCM_TIMEDRUN;
        // Block 328 @1986
        // Block 329 @1990
        return SCM_INITTRAP;
        // Block 330 @1993
        // Block 331 @1997
        return SCM_RETREAT;
        // Block 332 @2000
        // Block 333 @2004
        return SCM_CREATE;
        // Block 334 @2007
        return SCM_CONFIRM;
    default:
        // Block 336 @2011
        return SCM_RUN;
    }
    // Block 164 @1468
    return SCM_EXPLODETRAP;
    // Block 166 @1474
    goto block_168; // @1480
    // Block 179 @1512
    goto block_181; // @1518
    // Block 190 @1547
    goto block_192; // @1553
    // Block 201 @1584
    goto block_203; // @1590
    // Block 216 @1631
    goto block_218; // @1637
    // Block 227 @1664
    goto block_229; // @1670
    // Block 240 @1708
    goto block_242; // @1714
    // Block 259 @1767
    goto block_261; // @1772
    // Block 274 @1811
    goto block_276; // @1817
    // Block 287 @1855
    goto block_289; // @1861
    // Block 302 @1902
    goto block_304; // @1909
    // Block 313 @1940
    goto block_315; // @1946
    // Block 318 @1956
    goto block_320; // @1962
    // Block 335 @2010
    goto block_336; // @2011
    // Block 337 @2015
    rand();
    vec2 = (unknown_337_2021_1 % SCM_DISARMTRAP);
    SC_ggi(SGI_CURRENTMISSION);
    goto block_339; // @2037
    switch (vec2) {
    case 1:
        // Block 339 @2037
        break;
    case 16:
        // Block 341 @2042
        break;
    case 17:
        // Block 343 @2047
        break;
    case 6:
        // Block 345 @2052
        // Block 347 @2059
        // Block 348 @2063
        return &"ini\\players\\poorvc2.ini";
        // Block 349 @2066
        return &"ini\\players\\poorvc3.ini";
    case 2:
        // Block 352 @2075
        break;
    case 3:
        // Block 354 @2080
        break;
    case 4:
        // Block 356 @2085
        break;
    case 5:
        // Block 358 @2090
        break;
    case 7:
        // Block 360 @2095
        break;
    case 8:
        // Block 362 @2100
        break;
    case 10:
        // Block 364 @2105
        // Block 365 @2109
        return &"ini\\players\\vcfighter2.ini";
        // Block 366 @2112
        // Block 367 @2116
        return &"ini\\players\\vcfighter3.ini";
        // Block 368 @2119
        return &"ini\\players\\vcfighter4.ini";
    case 9:
        // Block 371 @2128
        break;
    case 11:
        // Block 373 @2133
        break;
    case 12:
        // Block 375 @2138
        break;
    case 13:
        // Block 377 @2143
        break;
    case 14:
        // Block 379 @2148
        break;
    case 15:
        // Block 381 @2153
        break;
    case 24:
        // Block 383 @2158
        // Block 384 @2162
        return &"ini\\players\\vcfighter3.ini";
        // Block 385 @2165
        // Block 386 @2169
        return &"ini\\players\\vcfighter2.ini";
        // Block 387 @2172
        // Block 388 @2176
        return &"ini\\players\\vcfighter3.ini";
        // Block 389 @2179
        return &"ini\\players\\vcfighter4.ini";
    case 18:
        // Block 392 @2188
        break;
    case 19:
        // Block 394 @2193
        break;
    case 20:
        // Block 396 @2198
        break;
    case 21:
        // Block 398 @2203
        break;
    case 26:
        // Block 400 @2208
        break;
    case 27:
        // Block 402 @2213
        break;
    case 28:
        // Block 404 @2218
        // Block 405 @2222
        return &"ini\\players\\vcuniform1.ini";
        // Block 406 @2225
        // Block 407 @2229
        return &"ini\\players\\vcuniform2.ini";
        // Block 408 @2232
        return &"ini\\players\\vcuniform3.ini";
    case 22:
        // Block 411 @2241
        break;
    case 23:
        // Block 413 @2246
        break;
    case 25:
        // Block 415 @2251
        break;
    case 29:
        // Block 417 @2256
        break;
    case 30:
        // Block 419 @2261
        break;
    case 31:
        // Block 421 @2266
        break;
    case 32:
        // Block 423 @2271
        // Block 424 @2275
        return &"ini\\players\\nvasoldier2.ini";
        // Block 425 @2278
        // Block 426 @2282
        return &"ini\\players\\nvasoldier3.ini";
        // Block 427 @2285
        return &"ini\\players\\nvaofficer.ini";
    default:
        // Block 429 @2289
        return &"ini\\players\\default_aiviet.ini";
    }
    // Block 346 @2056
    return &"ini\\players\\poorvc.ini";
    // Block 350 @2069
    goto block_352; // @2075
    // Block 369 @2122
    goto block_371; // @2128
    // Block 390 @2182
    goto block_392; // @2188
    // Block 409 @2235
    goto block_411; // @2241
    // Block 428 @2288
    goto block_429; // @2289
    // Block 430 @2293
    vec2 = 0;
    // Block 431 @2298
    if (!((vec2 < SCM_SETGPHASE))) {
        // Block 433 @2329
        SC_ggi(SGI_CURRENTMISSION);
        // Block 435 @2341
        t2343_0[0] = SCM_PANICRUN;
        t2350_0[SCM_BOOBYTRAPFOUND] = SCM_SHOOTING;
        // Block 437 @2361
        // Block 439 @2366
        // Block 441 @2371
        // Block 443 @2376
        t2378_0[0] = SCM_RETREAT;
        t2385_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        // Block 445 @2396
        // Block 447 @2401
        t2403_0[0] = SCM_RETREAT;
        t2410_0[SCM_BOOBYTRAPFOUND] = SCM_CHECKBODY;
        t2417_0[SCM_SETGPHASE] = SCM_PANICRUN;
        // Block 449 @2428
        t2430_0[0] = SCM_PANICRUN;
        t2437_0[SCM_BOOBYTRAPFOUND] = SCM_CHECKBODY;
        t2444_0[SCM_SETGPHASE] = SCM_SHOOTING;
        // Block 451 @2455
        // Block 453 @2460
        t2462_0[0] = SCM_RETREAT;
        t2469_0[SCM_BOOBYTRAPFOUND] = SCM_PANICRUN;
        t2476_0[SCM_SETGPHASE] = SCM_STARTWALK;
        // Block 455 @2487
        // Block 457 @2492
        // Block 459 @2497
        t2499_0[0] = SCM_RETREAT;
        t2506_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        // Block 461 @2517
        t2519_0[0] = SCM_RETREAT;
        t2526_0[SCM_BOOBYTRAPFOUND] = SCM_PANICRUN;
        t2533_0[SCM_SETGPHASE] = SCM_STARTWALK;
        t2540_0[SCM_TELEPORT] = SCM_WALKATWP;
        t2547_0[SCM_WALK] = SCM_SHOOTING;
        // Block 463 @2558
        // Block 465 @2563
        // Block 467 @2568
        t2570_0[0] = SCM_RETREAT;
        t2577_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        // Block 469 @2588
        // Block 471 @2593
        // Block 473 @2598
        t2600_0[0] = SCM_GETBACK;
        t2607_0[SCM_BOOBYTRAPFOUND] = SCM_HUNTER;
        t2614_0[SCM_SETGPHASE] = SCM_STARTPATROL;
        // Block 475 @2625
        t2627_0[0] = SCM_GETBACK;
        t2634_0[SCM_BOOBYTRAPFOUND] = SCM_HUNTER;
        t2641_0[SCM_SETGPHASE] = SCM_STARTPATROL;
        t2648_0[SCM_TELEPORT] = SCM_WALK;
        // Block 477 @2659
        // Block 479 @2664
        t2666_0[0] = SCM_WALK;
        t2673_0[SCM_BOOBYTRAPFOUND] = SCM_GETBACK;
        t2680_0[SCM_SETGPHASE] = SCM_MORTARLAND;
        t2687_0[SCM_TELEPORT] = SCM_STARTMORTARFIRE;
        t2694_0[SCM_WALK] = SCM_STARTASSAULT;
        // Block 481 @2705
        t2707_0[0] = SCM_RETREAT;
        t2714_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        // Block 483 @2725
        // Block 485 @2730
        // Block 487 @2735
        t2737_0[0] = SCM_CHECKBODY;
        t2744_0[SCM_BOOBYTRAPFOUND] = SCM_GETBACK;
        t2751_0[SCM_SETGPHASE] = SCM_HUNTER;
        t2758_0[SCM_TELEPORT] = SCM_STARTPATROL;
        // Block 489 @2769
        t2771_0[0] = SCM_STARTPATROL;
        t2778_0[SCM_BOOBYTRAPFOUND] = SCM_WALK;
        t2785_0[SCM_SETGPHASE] = SCM_RUNATWP;
        // Block 491 @2796
        t2798_0[0] = SCM_WALK;
        t2805_0[SCM_BOOBYTRAPFOUND] = SCM_MORTARLAND;
        t2812_0[SCM_SETGPHASE] = SCM_STARTMORTARFIRE;
        t2819_0[SCM_TELEPORT] = SCM_STARTASSAULT;
        // Block 493 @2830
        // Block 495 @2835
        // Block 497 @2840
        t2842_0[0] = SCM_STARTMORTARFIRE;
        t2849_0[SCM_BOOBYTRAPFOUND] = SCM_STARTASSAULT;
        t2856_0[SCM_SETGPHASE] = SCM_WALK;
        t2863_0[SCM_TELEPORT] = SCM_RUNATWP;
        // Block 498 @2870
        t2872_0[0] = SCM_WALK;
        t2879_0[SCM_BOOBYTRAPFOUND] = SCM_GETBACK;
        t2886_0[SCM_SETGPHASE] = SCM_MORTARLAND;
        t2893_0[SCM_TELEPORT] = SCM_STARTMORTARFIRE;
        t2900_0[SCM_WALK] = SCM_STARTASSAULT;
        // Block 500 @2908
        return SGI_CURRENTMISSION;
    } else {
        // Block 431 @2298
        // Block 432 @2302
        (t2304_0 + (vec2 * SCM_BOOBYTRAPFOUND)) = 0;
        (t2313_0 + (vec2 * SCM_BOOBYTRAPFOUND)) = 0;
        vec2++;
    }
    switch (vec2) {
    case 1:
        // Block 435 @2341
        t2343_0[0] = SCM_PANICRUN;
        t2350_0[SCM_BOOBYTRAPFOUND] = SCM_SHOOTING;
        break;
    case 2:
        // Block 437 @2361
        break;
    case 3:
        // Block 439 @2366
        break;
    case 4:
        // Block 441 @2371
        break;
    case 5:
        // Block 443 @2376
        t2378_0[0] = SCM_RETREAT;
        t2385_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        break;
    case 16:
        // Block 445 @2396
        break;
    case 17:
        // Block 447 @2401
        t2403_0[0] = SCM_RETREAT;
        t2410_0[SCM_BOOBYTRAPFOUND] = SCM_CHECKBODY;
        t2417_0[SCM_SETGPHASE] = SCM_PANICRUN;
        break;
    case 6:
        // Block 449 @2428
        t2430_0[0] = SCM_PANICRUN;
        t2437_0[SCM_BOOBYTRAPFOUND] = SCM_CHECKBODY;
        t2444_0[SCM_SETGPHASE] = SCM_SHOOTING;
        break;
    case 7:
        // Block 451 @2455
        break;
    case 8:
        // Block 453 @2460
        t2462_0[0] = SCM_RETREAT;
        t2469_0[SCM_BOOBYTRAPFOUND] = SCM_PANICRUN;
        t2476_0[SCM_SETGPHASE] = SCM_STARTWALK;
        break;
    case 9:
        // Block 455 @2487
        break;
    case 11:
        // Block 457 @2492
        break;
    case 10:
        // Block 459 @2497
        t2499_0[0] = SCM_RETREAT;
        t2506_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        break;
    case 12:
        // Block 461 @2517
        t2519_0[0] = SCM_RETREAT;
        t2526_0[SCM_BOOBYTRAPFOUND] = SCM_PANICRUN;
        t2533_0[SCM_SETGPHASE] = SCM_STARTWALK;
        t2540_0[SCM_TELEPORT] = SCM_WALKATWP;
        t2547_0[SCM_WALK] = SCM_SHOOTING;
        break;
    case 13:
        // Block 463 @2558
        break;
    case 14:
        // Block 465 @2563
        break;
    case 15:
        // Block 467 @2568
        t2570_0[0] = SCM_RETREAT;
        t2577_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        break;
    case 18:
        // Block 469 @2588
        break;
    case 19:
        // Block 471 @2593
        break;
    case 20:
        // Block 473 @2598
        t2600_0[0] = SCM_GETBACK;
        t2607_0[SCM_BOOBYTRAPFOUND] = SCM_HUNTER;
        t2614_0[SCM_SETGPHASE] = SCM_STARTPATROL;
        break;
    case 21:
        // Block 475 @2625
        t2627_0[0] = SCM_GETBACK;
        t2634_0[SCM_BOOBYTRAPFOUND] = SCM_HUNTER;
        t2641_0[SCM_SETGPHASE] = SCM_STARTPATROL;
        t2648_0[SCM_TELEPORT] = SCM_WALK;
        break;
    case 22:
        // Block 477 @2659
        break;
    case 23:
        // Block 479 @2664
        t2666_0[0] = SCM_WALK;
        t2673_0[SCM_BOOBYTRAPFOUND] = SCM_GETBACK;
        t2680_0[SCM_SETGPHASE] = SCM_MORTARLAND;
        t2687_0[SCM_TELEPORT] = SCM_STARTMORTARFIRE;
        t2694_0[SCM_WALK] = SCM_STARTASSAULT;
        break;
    case 24:
        // Block 481 @2705
        t2707_0[0] = SCM_RETREAT;
        t2714_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        break;
    case 26:
        // Block 483 @2725
        break;
    case 27:
        // Block 485 @2730
        break;
    case 28:
        // Block 487 @2735
        t2737_0[0] = SCM_CHECKBODY;
        t2744_0[SCM_BOOBYTRAPFOUND] = SCM_GETBACK;
        t2751_0[SCM_SETGPHASE] = SCM_HUNTER;
        t2758_0[SCM_TELEPORT] = SCM_STARTPATROL;
        break;
    case 25:
        // Block 489 @2769
        t2771_0[0] = SCM_STARTPATROL;
        t2778_0[SCM_BOOBYTRAPFOUND] = SCM_WALK;
        t2785_0[SCM_SETGPHASE] = SCM_RUNATWP;
        break;
    case 29:
        // Block 491 @2796
        t2798_0[0] = SCM_WALK;
        t2805_0[SCM_BOOBYTRAPFOUND] = SCM_MORTARLAND;
        t2812_0[SCM_SETGPHASE] = SCM_STARTMORTARFIRE;
        t2819_0[SCM_TELEPORT] = SCM_STARTASSAULT;
        break;
    case 30:
        // Block 493 @2830
        break;
    case 31:
        // Block 495 @2835
        break;
    case 32:
        // Block 497 @2840
        t2842_0[0] = SCM_STARTMORTARFIRE;
        t2849_0[SCM_BOOBYTRAPFOUND] = SCM_STARTASSAULT;
        t2856_0[SCM_SETGPHASE] = SCM_WALK;
        t2863_0[SCM_TELEPORT] = SCM_RUNATWP;
        break;
    default:
        // Block 499 @2907
    }
    // Block 501 @2910
    vec.z = 100.0f;
    SC_ggi(SCM_ENABLE);
    if (!(SCM_ENABLE)) {
        // Block 514 @3016
        SC_PC_GetPos(i);
        SC_2VectorsDist(&vec, &vec);
        vec.z = &vec;
        // Block 515 @3037
        return TRUE;
        // Block 516 @3040
        return FALSE;
    } else {
        // Block 502 @2928
        SC_P_GetPos(i, &vec);
        SC_MP_EnumPlayers(&vec2, &vec.y, 0);
        // Block 503 @2943
        // Block 504 @2944
        return FALSE;
        // Block 505 @2947
        vec.y = 0;
        // Block 506 @2951
        // Block 507 @2955
        // Block 508 @2965
        SC_P_GetPos(t2970_0, &vec);
        SC_2VectorsDist(&vec, &vec);
        vec.z = &vec;
        // Block 509 @2988
        vec.z = vec.z;
        i = t2993_0;
        // Block 510 @2997
        vec.y++;
        // Block 511 @3006
        // Block 512 @3010
        return TRUE;
        // Block 513 @3013
        return FALSE;
    }
    // Block 517 @3043
    SC_GetGroupPlayers(i, i);
    vec2 = i;
    vec2 = 0;
    // Block 518 @3059
    if (!((vec2 < vec2))) {
        // Block 523 @3090
        return TRUE;
    } else {
        // Block 518 @3059
        // Block 519 @3063
        SC_P_GetBySideGroupMember(i, i, vec2);
        SC_P_IsReady(vec2);
        // Block 520 @3077
        // Block 521 @3078
        return FALSE;
        // Block 522 @3081
        vec2++;
    }
    // Block 524 @3093
    SC_GetGroupPlayers(i, i);
    vec2 = i;
    vec2 = 0;
    // Block 525 @3109
    if (!((vec2 < vec2))) {
        // Block 532 @3155
        return TRUE;
    } else {
        // Block 525 @3109
        // Block 526 @3113
        SC_P_GetBySideGroupMember(i, i, vec2);
        SC_P_IsReady(vec2);
        // Block 527 @3127
        // Block 528 @3128
        SC_P_GetBySideGroupMember(i, i, vec2);
        SC_P_GetActive(vec2);
        // Block 529 @3142
        // Block 530 @3143
        return FALSE;
        // Block 531 @3146
        vec2++;
    }
    // Block 533 @3158
    SC_GetGroupPlayers(1, i);
    vec2 = i;
    vec2 = 0;
    // Block 534 @3177
    if (!((vec2 < vec2))) {
        // Block 541 @3235
        return FALSE;
    } else {
        // Block 534 @3177
        // Block 535 @3181
        SC_P_GetBySideGroupMember(1, i, vec2);
        vec2.y = vec2;
        // Block 536 @3194
        SC_P_Ai_GetDanger(vec2.y);
        vec2 = vec2.y;
        // Block 537 @3207
        return TRUE;
        // Block 538 @3210
        SC_P_Ai_GetSureEnemies(vec2.y);
        vec2 = vec2.y;
        // Block 539 @3223
        return TRUE;
        // Block 540 @3226
        vec2++;
    }
    // Block 542 @3238
    vec2 = 1;
    // Block 543 @3247
    if (!((vec2 < SCM_CREATE))) {
        // Block 550 @3305
        return FALSE;
    } else {
        // Block 543 @3247
        // Block 544 @3251
        SC_P_GetBySideGroupMember(0, 0, vec2);
        vec2.y = vec2;
        // Block 545 @3264
        SC_P_Ai_GetDanger(vec2.y);
        vec2 = vec2.y;
        // Block 546 @3277
        return TRUE;
        // Block 547 @3280
        SC_P_Ai_GetSureEnemies(vec2.y);
        vec2 = vec2.y;
        // Block 548 @3293
        return TRUE;
        // Block 549 @3296
        vec2++;
    }
    // Block 551 @3308
    vec2 = 0;
    // Block 552 @3317
    if (!((vec2 < SCM_CREATE))) {
        // Block 557 @3365
        return vec2.y;
    } else {
        // Block 552 @3317
        // Block 553 @3321
        SC_P_GetBySideGroupMember(0, 0, vec2);
        vec2.y = vec2;
        // Block 554 @3334
        SC_P_GetPos(vec2.y, &vec2);
        SC_2VectorsDist(i, &vec2);
        vec2.y = &vec2;
        // Block 555 @3352
        vec2.y = vec2.y;
        // Block 556 @3356
        vec2++;
    }
}

int func_3368(s_SC_OBJ_info *info) {
    // Block 558 @3368
    SC_NOD_Get(0, i);
    ai_props = i;
    if (!((ai_props != 0))) {
        // Block 560 @3387
        return retval;
    } else {
        // Block 559 @3383
        SC_NOD_GetWorldPos(ai_props, retval);
    }
    // Block 561 @3388
    SC_NOD_Get(0, i);
    ai_props = i;
    if (!((ai_props != 0))) {
        // Block 563 @3411
        return FALSE;
    } else {
        // Block 562 @3403
        SC_NOD_GetWorldRotZ(ai_props);
        return ai_props;
    }
    // Block 564 @3414
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_GetPeaceMode(1);
    if (!((1 == SCM_RUN))) {
        // Block 566 @3441
        SC_P_GetBySideGroupMember(0, 0, 1);
        SC_P_Ai_Stop(1);
        return FALSE;
    } else {
        // Block 565 @3430
        SC_P_GetBySideGroupMember(0, 0, 1);
        SC_P_Ai_SetPeaceMode(1, 0);
    }
    // Block 567 @3452
    SC_DoExplosion(&ai_props, retval);
    return retval;
    // Block 568 @3462
    SC_NOD_Get(0, retval);
    ai_props.watchfulness_zerodist = retval;
    if (!(ai_props.watchfulness_zerodist)) {
        // Block 570 @3479
        SC_message(&"FATAL! Claymore %s not found!!!!!!", 1);
        return TRUE;
    } else {
        // Block 569 @3478
        // Block 571 @3484
        SC_NOD_GetWorldPos(ai_props.watchfulness_zerodist, &ai_props);
        SC_NOD_GetWorldRotZ(ai_props.watchfulness_zerodist);
        ai_props = ai_props.watchfulness_zerodist;
        ai_props = (ai_props - 1.57f);
        ai_props.watchfulness_zerodist = t3504_0;
        cos(ai_props);
        ai_props.watchfulness_zerodist = (t3509_0 - (2.0f * ai_props));
        sin(ai_props);
        ai_props.watchfulness_zerodist.field1 = (t3524_0 + (2.0f * ai_props));
        SC_DoExplosion(&ai_props.watchfulness_zerodist, 1);
        ai_props.watchfulness_zerodist = t3543_0;
        cos(ai_props);
        ai_props.watchfulness_zerodist = (t3548_0 - (4.0f * ai_props));
        sin(ai_props);
        ai_props.watchfulness_zerodist.field1 = (t3563_0 + (4.0f * ai_props));
        SC_DoExplosion(&ai_props.watchfulness_zerodist, SCM_RUN);
        ai_props.watchfulness_zerodist = t3582_0;
        cos(ai_props);
        ai_props.watchfulness_zerodist = (t3587_0 - (8.0f * ai_props));
        sin(ai_props);
        ai_props.watchfulness_zerodist.field1 = (t3602_0 + (8.0f * ai_props));
        SC_DoExplosion(&ai_props.watchfulness_zerodist, SCM_WARNABOUTENEMY);
        SC_DUMMY_Set_DoNotRenHier2(ai_props.watchfulness_zerodist, 1);
        return TRUE;
    }
    // Block 572 @3625
    ai_props.field2 = t3634_0;
    ai_props = 0;
    // Block 573 @3643
    if (!((ai_props < i))) {
        // Block 575 @3686
        return ai_props;
    } else {
        // Block 573 @3643
        // Block 574 @3647
        frnd(retval);
        ai_props = (t3648_0 + retval);
        frnd(retval);
        ai_props.field1 = (t3661_0 + retval);
        SC_DoExplosion(&ai_props, i);
        ai_props++;
    }
    // Block 576 @3687
    SC_GetWp(i, &ai_props);
    SC_DoExplosion(&ai_props, retval);
    return retval;
    // Block 577 @3701
    SC_GetWp(retval, &ai_props);
    SC_CreatePtc(176, &ai_props);
    return &ai_props;
    // Block 578 @3715
    SC_GetWp(retval, &ai_props);
    SC_DoExplosion(&ai_props, SCM_WARNABOUTENEMY);
    SC_SND_PlaySound3D(2965, &ai_props);
    SC_NOD_Get(0, retval);
    SC_CreatePtc_Ext(0, retval, 1000.0f, 0.0f, 1.0f, 1.0f);
    SC_NOD_Get(0, retval);
    SC_CreatePtc_Ext(0, retval, 1000.0f, 0.0f, 1.0f, 1.0f);
    ai_props = 0;
    // Block 579 @3765
    if (!((ai_props < SCM_CREATE))) {
        // Block 581 @3820
        return ai_props;
    } else {
        // Block 579 @3765
        // Block 580 @3769
        SC_GetWp(retval, &ai_props);
        frnd(5.0f);
        ai_props = (t3778_0 + 5.0f);
        frnd(5.0f);
        ai_props.field1 = (t3791_0 + 5.0f);
        SC_CreatePtcVec_Ext(177, &ai_props, 1000.0f, 0.0f, 1.0f, 1.0f);
        ai_props++;
    }
    // Block 582 @3821
    SC_CreatePtc(198, retval);
    SC_SND_PlaySound3D(2965, retval);
    SC_CreatePtcVec_Ext(176, retval, 1000.0f, 0.0f, 1.0f, 1.0f);
    SC_CreatePtcVec_Ext(177, retval, 5.0f, 0.0f, 1.0f, 1.0f);
    return 1.0f;
    // Block 583 @3847
    ai_props.field2 = t3851_0;
    ai_props = 0;
    // Block 584 @3860
    if (!((ai_props < i))) {
        // Block 586 @3912
        SC_CreatePtcVec_Ext(176, i, 1000.0f, 0.0f, 1.0f, 1.0f);
        return 1.0f;
    } else {
        // Block 584 @3860
        // Block 585 @3864
        frnd(retval);
        ai_props = (t3866_0 + retval);
        frnd(retval);
        ai_props.field1 = (t3879_0 + retval);
        SC_CreatePtc(198, &ai_props);
        SC_CreatePtcVec_Ext(177, &ai_props, 5.0f, 0.0f, 1.0f, 1.0f);
        ai_props++;
    }
    // Block 587 @3921
    ai_props.field2 = t3925_0;
    ai_props = 0;
    // Block 588 @3934
    if (!((ai_props < i))) {
        // Block 590 @3978
        SC_CreatePtcVec_Ext(176, i, 1000.0f, 0.0f, 1.0f, 1.0f);
        return 1.0f;
    } else {
        // Block 588 @3934
        // Block 589 @3938
        frnd(retval);
        ai_props = (t3940_0 + retval);
        frnd(retval);
        ai_props.field1 = (t3953_0 + retval);
        SC_CreatePtc(198, &ai_props);
        ai_props++;
    }
    // Block 591 @3987
    ai_props.field2 = t3991_0;
    ai_props = 0;
    // Block 592 @4000
    if (!((ai_props < i))) {
        // Block 594 @4044
        return ai_props;
    } else {
        // Block 592 @4000
        // Block 593 @4004
        frnd(retval);
        ai_props = (t4006_0 + retval);
        frnd(retval);
        ai_props.field1 = (t4019_0 + retval);
        SC_CreatePtc(198, &ai_props);
        ai_props++;
    }
    // Block 595 @4045
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(retval, &ai_props);
    ai_props.field19 = 1;
    ai_props.field3 = 4.0f;
    SC_P_Ai_SetProps(retval, &ai_props);
    ai_props.field1 = 0.9f;
    ai_props = 0.3f;
    ai_props.field2 = 0.5f;
    SC_P_Ai_SetBattleProps(retval, &ai_props);
    return &ai_props;
    // Block 596 @4088
    SC_P_GetDir(i, &ai_props);
    SC_VectorLen(&ai_props);
    ai_props = &ai_props;
    if (!((ai_props > 1.0f))) {
        // Block 598 @4110
        return FALSE;
    } else {
        // Block 597 @4107
        return TRUE;
    }
    // Block 599 @4113
    ai_props = 0;
    // Block 600 @4121
    if (!((ai_props < SCM_CREATE))) {
        // Block 605 @4177
        return ai_props;
    } else {
        // Block 600 @4121
        // Block 601 @4125
        SC_P_GetBySideGroupMember(0, 0, ai_props);
        SC_P_IsReady(ai_props);
        // Block 602 @4139
        SC_P_GetBySideGroupMember(0, 0, ai_props);
        SC_P_GetPos(ai_props, &ai_props);
        SC_2VectorsDist(&ai_props, i);
        ai_props = i;
        // Block 603 @4164
        ai_props = ai_props;
        // Block 604 @4168
        ai_props++;
    }
}

int func_4180(s_SC_OBJ_info *info) {
    // Block 606 @4180
    SC_P_GetPos(i, &ai_props);
    SC_IsNear3D(&ai_props, i, i);
    return i;
    // Block 607 @4195
    SC_PC_GetPos(&ai_props);
    SC_IsNear3D(&ai_props, i, i);
    return i;
    // Block 608 @4213
    if (!(i)) {
        // Block 610 @4217
        return 32;
    } else {
        // Block 609 @4216
        // Block 611 @4218
        SC_ZeroMem(&ai_props, 128);
        SC_P_Ai_GetProps(i, &ai_props);
        ai_props.field13 = i;
        ai_props.field14 = i;
        ai_props.field15 = i;
        ai_props.field16 = retval;
        SC_P_Ai_SetProps(i, &ai_props);
        return &ai_props;
    }
    // Block 612 @4251
    ai_props.hear_distance_mult = 10000.0f;
    ai_props.view_angle.field3 = 1000.0f;
    ai_props.view_angle = t4270_0;
    ai_props = SCM_MORTARLAND;
    SC_GetPls(&ai_props.view_angle, &ai_props, &ai_props);
    ai_props.view_angle = 0;
    ai_props = 0;
    // Block 613 @4291
    if (!((ai_props < ai_props))) {
        // Block 622 @4373
        return ai_props.view_angle;
    } else {
        // Block 613 @4291
        // Block 614 @4295
        SC_P_GetInfo(t4300_0, &ai_props.view_angle_near);
        // Block 615 @4310
        // Block 616 @4314
        // Block 617 @4315
        SC_P_IsReady(t4321_0);
        // Block 618 @4327
        // Block 619 @4328
        SC_P_GetPos(t4333_0, &ai_props.hear_distance_mult);
        SC_2VectorsDist(&ai_props.hear_distance_mult, i);
        ai_props.hear_distance_max = i;
        // Block 620 @4351
        ai_props.hear_distance_mult = ai_props.hear_distance_max;
        ai_props.view_angle = t4360_0;
        // Block 621 @4364
        ai_props++;
    }
}

int func_4376(s_SC_OBJ_info *info) {
    // Block 623 @4376
    SC_P_GetInfo(j, &player_info);
    local_0 = t4389_0;
    SC_P_GetPos(j, &sphere);
    sphere.field3 = 1000.0f;
    local_0 = SCM_MORTARLAND;
    SC_GetPls(&sphere, &local_1, &local_0);
    local_0 = 0;
    local_0 = 0;
    // Block 624 @4419
    if (!((i < i))) {
        // Block 633 @4498
        retval = i;
        return retval;
    } else {
        // Block 624 @4419
        // Block 625 @4423
        SC_P_GetInfo(t4428_0, &player_info);
        // Block 626 @4438
        // Block 627 @4444
        // Block 628 @4445
        SC_P_IsReady(t4451_0);
        // Block 629 @4457
        // Block 630 @4458
        (j + (i * SCM_BOOBYTRAPFOUND)) = t4463_0;
        local_0 = (i + 1);
        // Block 631 @4483
        SC_Log(1299473735, SCM_RUN);
        return SCM_RUN;
        // Block 632 @4489
        local_0 = (i + 1);
    }
    // Block 634 @4503
    local_0 = SCM_MORTARLAND;
    SC_P_GetInfo(retval, &player_info2);
    if (!((i < SCM_RUN))) {
        // Block 636 @4539
        // Block 637 @4546
        // Block 638 @4555
        // Block 639 @4563
        SC_Log(622871382, t4567_0, t4570_0, SCM_BOOBYTRAPFOUND);
        return SCM_BOOBYTRAPFOUND;
    } else {
        // Block 635 @4524
        SC_Log(622871382, t4528_0, t4531_0, t4534_0, SCM_TAUNTRUNNER);
        return SCM_TAUNTRUNNER;
    }
}

int func_4575(s_SC_OBJ_info *info) {
    // Block 640 @4575
    SC_P_GetPos(i, &player_info);
    SC_2VectorsDist(i, &player_info);
    player_info = &player_info;
    return player_info;
    // Block 641 @4594
    SC_ZeroMem(&player_info, SCM_DISARMTRAP);
    local_0[0] = 0;
    local_0[SCM_BOOBYTRAPFOUND] = 0;
    local_0[SCM_SETGPHASE] = 0;
    local_0[SCM_TELEPORT] = 0;
    local_0[SCM_WALK] = 0;
    SC_P_SetSpecAnims(retval, &player_info);
    return &player_info;
    // Block 642 @4634
    SC_ZeroMem(&player_info, SCM_DISARMTRAP);
    local_0[0] = i;
    local_0[SCM_BOOBYTRAPFOUND] = i;
    local_0[SCM_SETGPHASE] = i;
    local_0[SCM_TELEPORT] = i;
    local_0[SCM_WALK] = retval;
    SC_P_SetSpecAnims(param_1, &player_info);
    return &player_info;
    // Block 643 @4674
    player_info = SCM_MORTARLAND;
    SC_GetPls(i, &player_info.max_hp, &player_info);
    if (!(player_info)) {
        // Block 645 @4691
        return 36;
    } else {
        // Block 644 @4690
        // Block 646 @4692
        player_info = 0;
        // Block 647 @4696
        // Block 648 @4700
        SC_P_DoHit(t4705_0, 0, (retval / 7.0f));
        SC_P_DoHit(t4717_0, 1, (retval / 7.0f));
        SC_P_DoHit(t4729_0, SCM_RUN, (retval / 7.0f));
        SC_P_DoHit(t4741_0, SCM_WARNABOUTENEMY, (retval / 7.0f));
        SC_P_DoHit(t4753_0, SCM_BOOBYTRAPFOUND, (retval / 7.0f));
        SC_P_DoHit(t4765_0, SCM_TAUNTRUNNER, (retval / 7.0f));
        SC_P_DoHit(t4777_0, SCM_CREATE, (retval / 7.0f));
        player_info++;
        // Block 649 @4793
        return player_info;
    }
    // Block 650 @4794
    SC_P_GetPos(i, &player_info);
    player_info.field2 = (t4801_0 + 1.0f);
    player_info.field3 = 1.0f;
    SC_SphereIsVisible(&player_info);
    return &player_info;
    // Block 651 @4821
    SC_P_GetInfo(i, &player_info);
    return t4828_0;
    // Block 652 @4831
    SC_P_GetInfo(i, &player_info);
    return t4838_0;
    // Block 653 @4841
    SC_P_GetInfo(i, &player_info);
    return t4848_0;
    // Block 654 @4851
    player_info = 0;
    // Block 655 @4856
    if (!((player_info < 0))) {
        // Block 657 @4878
        return FALSE;
    } else {
        // Block 655 @4856
        // Block 656 @4860
        player_info++;
    }
    // Block 658 @4883
    player_info = 0;
    // Block 659 @4888
    if (!((player_info < 0))) {
        // Block 663 @4917
        (0 + (0 * SCM_SETGPHASE)) = retval;
        *((0 + (0 * SCM_SETGPHASE)) + 4) = 0;
        SC_SetObjectives(0, 0, 6.0f);
        return 6.0f;
    } else {
        // Block 659 @4888
        // Block 660 @4892
        // Block 661 @4901
        SC_Log(1819309380, retval, SCM_WARNABOUTENEMY);
        return SCM_WARNABOUTENEMY;
        // Block 662 @4908
        player_info++;
    }
}

int func_4948(s_SC_OBJ_info *info) {
    // Block 664 @4948
    local_0 = 0;
    // Block 665 @4953
    if (!((i < 0))) {
        // Block 669 @4982
        (0 + (0 * SCM_SETGPHASE)) = retval;
        *((0 + (0 * SCM_SETGPHASE)) + 4) = 0;
        SC_SetObjectivesNoSound(0, 0, 6.0f);
        return 6.0f;
    } else {
        // Block 665 @4953
        // Block 666 @4957
        // Block 667 @4966
        SC_Log(1819309380, retval, SCM_WARNABOUTENEMY);
        return SCM_WARNABOUTENEMY;
        // Block 668 @4973
        local_0 = (i + 1);
    }
    // Block 670 @5013
    local_0 = 0;
    // Block 671 @5018
    if (!((i < 0))) {
        // Block 677 @5066
        return i;
    } else {
        // Block 671 @5018
        // Block 672 @5022
        // Block 673 @5031
        // Block 674 @5041
        // Block 675 @5042
        *((0 + (i * SCM_SETGPHASE)) + 4) = SCM_RUN;
        SC_SetObjectives(0, 0, 6.0f);
        return 6.0f;
        // Block 676 @5057
        local_0 = (i + 1);
    }
    // Block 678 @5067
    local_0 = 0;
    // Block 679 @5072
    if (!((i < 0))) {
        // Block 683 @5103
        SC_SetObjectives(0, 0, 6.0f);
        return 6.0f;
    } else {
        // Block 679 @5072
        // Block 680 @5076
        // Block 681 @5085
        *((0 + (i * SCM_SETGPHASE)) + 4) = 1;
        // Block 682 @5094
        local_0 = (i + 1);
    }
    // Block 684 @5109
    local_0 = 0;
    // Block 685 @5114
    if (!((i < 0))) {
        // Block 689 @5145
        // Block 690 @5147
        // Block 691 @5151
        SC_P_GetBySideGroupMember(0, 0, i);
        SC_P_IsReady(i);
        // Block 692 @5165
        // Block 693 @5166
        SC_P_GetBySideGroupMember(0, 0, i);
        SC_P_Ai_GetPeaceMode(i);
        local_0 = i;
        // Block 694 @5186
        return i;
        // Block 695 @5193
        // Block 696 @5194
        return FALSE;
    } else {
        // Block 685 @5114
        // Block 686 @5118
        // Block 687 @5127
        return t5133_0;
        // Block 688 @5136
        local_0 = (i + 1);
    }
}

int func_5197(s_SC_OBJ_info *info) {
    // Block 697 @5197
    SC_sgi(SGI_MISSIONDEATHCOUNT, 0);
    SC_sgi(SCM_RUN, 0);
    SC_sgi(SCM_CREATE, 0);
    SC_sgi(SCM_BOOBYTRAPFOUND, 0);
    SC_sgi(SCM_WARNABOUTENEMY, 0);
    SC_sgi(SCM_SETGPHASE, 0);
    SC_sgi(SGI_INTELCOUNT, 0);
    SC_sgi(SCM_HEARDSOMETHING, 0);
    SC_sgi(SCM_ENABLE, 0);
    SC_ggi(SCM_DISABLE);
    SC_Log(1702257996, SCM_DISABLE, SCM_WARNABOUTENEMY);
    return FALSE;
    // Block 698 @5245
    SC_ZeroMem(&vec, 120);
    SC_ZeroMem(&local_7, SCM_PANICRUN);
    SC_ZeroMem(&local_9, SCM_PANICRUN);
    local_0[0] = 0;
    local_0[SCM_DISARMTRAP] = 5.0f;
    local_0[SCM_WPPATH_BEGIN] = 1.5f;
    local_0[SCM_PLAYERINTERACTION] = 1.5f;
    local_0[SCM_INFO] = 2.0f;
    local_10 = 0;
    // Block 699 @5295
    if (!((j < SCM_TAUNTRUNNER))) {
        // Block 701 @5363
        local_7[0] = 1;
        local_7[SCM_BOOBYTRAPFOUND] = SCM_BOOBYTRAPFOUND;
        local_7[SCM_SETGPHASE] = SCM_TAUNTRUNNER;
        local_7[SCM_TELEPORT] = SCM_RUN;
        local_7[SCM_WALK] = SCM_WARNABOUTENEMY;
        local_9[0] = 1;
        local_9[SCM_BOOBYTRAPFOUND] = SCM_TAUNTRUNNER;
        local_9[SCM_SETGPHASE] = SCM_WARNABOUTENEMY;
        local_9[SCM_TELEPORT] = SCM_BOOBYTRAPFOUND;
        local_9[SCM_WALK] = SCM_RUN;
        SC_Ai_SetPlFollow(0, 0, 0, &vec, &local_7, &local_9, SCM_TAUNTRUNNER);
        local_0[0] = 0;
        local_0[SCM_DISARMTRAP] = 4.0f;
        local_0[SCM_WPPATH_BEGIN] = 1.5f;
        local_0[SCM_PLAYERINTERACTION] = 1.5f;
        local_0[SCM_INFO] = 1.5f;
        vec.field25 = 2.0f;
        local_10 = 0;
        // Block 702 @5472
        // Block 703 @5476
        *((&vec + (j * SCM_DISARMTRAP)) + 4) = (t5481_0 + 1.0f);
        frnd(0.2f);
        *((&vec + (j * SCM_DISARMTRAP)) + 8) = 0.2f;
        frnd(0.2f);
        *(((&vec + (j * SCM_DISARMTRAP)) + 8) + 4) = 0.2f;
        *(((&vec + (j * SCM_DISARMTRAP)) + 8) + 8) = 0;
        (&local_9 + (j * SCM_BOOBYTRAPFOUND)) = 0;
        local_10 = (j + 1);
        // Block 704 @5548
        local_7[0] = 0;
        local_7[SCM_BOOBYTRAPFOUND] = 1;
        local_7[SCM_SETGPHASE] = SCM_BOOBYTRAPFOUND;
        local_7[SCM_TELEPORT] = SCM_TAUNTRUNNER;
        local_7[SCM_WALK] = SCM_RUN;
        local_7[SCM_DISARMTRAP] = SCM_WARNABOUTENEMY;
        SC_Ai_SetPlFollow(0, 0, 1, &vec, &local_7, &local_9, SCM_CREATE);
        return SCM_CREATE;
    } else {
        // Block 699 @5295
        // Block 700 @5299
        *((&vec + (j * SCM_DISARMTRAP)) + 4) = (t5304_0 + 1.0f);
        frnd(0.5f);
        *((&vec + (j * SCM_DISARMTRAP)) + 8) = 0.5f;
        frnd(0.5f);
        *(((&vec + (j * SCM_DISARMTRAP)) + 8) + 4) = 0.5f;
        *(((&vec + (j * SCM_DISARMTRAP)) + 8) + 8) = 0;
        local_10 = (j + 1);
    }
    // Block 705 @5594
    SC_RadioSetDist(10.0f);
    return 10.0f;
    // Block 706 @5599
    if (!(0)) {
        // Block 708 @5606
        SC_P_GetBySideGroupMember(0, 0, SCM_BOOBYTRAPFOUND);
        vec = SCM_BOOBYTRAPFOUND;
        // Block 709 @5619
        // Block 710 @5620
        return FALSE;
        // Block 711 @5623
        SC_P_Ai_GetSureEnemies(vec);
        // Block 712 @5630
        // Block 713 @5631
        SC_ggi(SCM_RUN);
        // Block 714 @5638
        // Block 715 @5639
        return FALSE;
        // Block 716 @5642
        SC_P_GetBySideGroupMember(0, 0, SCM_BOOBYTRAPFOUND);
        SC_P_Speach(SCM_BOOBYTRAPFOUND, 4010, 4010, &vec);
        vec = (vec + 1.0f);
        SC_SpeachRadio(5013, 5013, &vec);
        return TRUE;
    } else {
        // Block 707 @5603
        return FALSE;
    }
    // Block 717 @5673
    SC_ZeroMem(0, 0);
    vec = 0;
    // Block 718 @5682
    if (!((vec < 0))) {
        // Block 720 @5740
        return vec;
    } else {
        // Block 718 @5682
        // Block 719 @5686
        *((0 + (vec * SCM_RUNATWP)) + 20) = 0;
        *((0 + (vec * SCM_RUNATWP)) + 16) = 1;
        *((0 + (vec * SCM_RUNATWP)) + 28) = 0;
        *((0 + (vec * SCM_RUNATWP)) + 32) = 0;
        vec++;
    }
    // Block 721 @5741
    SC_Log(1768186977, i, SCM_WARNABOUTENEMY);
    *((0 + (i * SCM_RUNATWP)) + 16) = SCM_RUN;
    *((0 + ((i + 1) * SCM_RUNATWP)) + 16) = SCM_RUN;
    *((0 + (i * SCM_RUNATWP)) + 24) = (i + 1);
    *((0 + ((i + 1) * SCM_RUNATWP)) + 24) = i;
    *((0 + (i * SCM_RUNATWP)) + 28) = SCM_BOOBYTRAPFOUND;
    *((0 + ((i + 1) * SCM_RUNATWP)) + 28) = SCM_BOOBYTRAPFOUND;
    SC_NOD_Get(retval, &"Plechovka");
    vec.z = &"Plechovka";
    if (!(vec.z)) {
        // Block 723 @5827
        SC_message(&"trap not found!!!", 1);
        return TRUE;
    } else {
        // Block 722 @5826
        // Block 724 @5832
        SC_NOD_GetWorldPos(vec.z, &vec);
        SC_NOD_Get(retval, &"Konec dratu");
        vec.z = &"Konec dratu";
        SC_NOD_GetWorldPos(vec.z, &vec);
        vec.y = (t5851_0 - t5853_0);
        vec.y.field1 = (t5860_0 - t5863_0);
        vec.y.field2 = (t5871_0 - t5874_0);
        SC_VectorLen(&vec.y);
        t5888_0 = FTOD((3.0f * &vec.y));
        t5891_0 = DMUL(&vec, t5888_0, t5888_1, t5890_0);
        t5894_0 = DADD(vec.z, t5891_0, t5891_1, t5893_0);
        vec.z = t5895_0;
        vec.z = ((0 + (i * SCM_RUNATWP)) + 12);
        vec.z = ((0 + ((i + 1) * SCM_RUNATWP)) + 12);
        (0 + (i * SCM_RUNATWP)) = (t5920_0 + (1048576000 * t5923_0));
        *((0 + (i * SCM_RUNATWP)) + 4) = (t5935_0 + (1048576000 * t5939_0));
        *((0 + (i * SCM_RUNATWP)) + 8) = (t5952_0 + (1048576000 * t5956_0));
        (0 + ((i + 1) * SCM_RUNATWP)) = (t5968_0 + (0.75f * t5971_0));
        (t5985_0 + (0.75f * t5989_0)) = ((0 + ((i + 1) * SCM_RUNATWP)) + 4);
        (t6004_0 + (0.75f * t6008_0)) = ((0 + ((i + 1) * SCM_RUNATWP)) + 8);
        return ((0 + ((i + 1) * SCM_RUNATWP)) + 8);
    }
    // Block 725 @6022
    SC_NOD_Get(i, &"Plechovka");
    vec.y = &"Plechovka";
    if (!(vec.y)) {
        // Block 727 @6041
        SC_message(&"trap not found!!!", 1);
        return -1;
    } else {
        // Block 726 @6040
        // Block 728 @6048
        SC_NOD_GetWorldPos(vec.y, &vec.y);
        SC_NOD_Get(i, 1701736267);
        vec.y = 1701736267;
        SC_NOD_GetWorldPos(vec.y, &vec.z);
        vec.z = (t6067_0 - t6069_0);
        vec.z.field1 = (t6076_0 - t6079_0);
        vec.z.field2 = ((t6087_0 - t6090_0) + 10000.0f);
        vec = (t6099_0 + (1048576000 * t6102_0));
        vec.field1 = (t6110_0 + (1048576000 * t6114_0));
        vec.field2 = (t6123_0 + (1048576000 * t6127_0));
        vec = 0;
        // Block 729 @6138
        // Block 730 @6142
        SC_IsNear2D((0 + (vec * SCM_RUNATWP)), &vec, 1.0f);
        // Block 731 @6155
        *((0 + (vec * SCM_RUNATWP)) + 20) = 1;
        *((0 + ((vec + 1) * SCM_RUNATWP)) + 20) = 1;
        SC_Log(1869440370, vec, SCM_WARNABOUTENEMY);
        return vec;
        // Block 732 @6184
        vec++;
        // Block 733 @6193
        return -1;
    }
}

int func_6196(s_SC_OBJ_info *info) {
    // Block 734 @6196
    goto block_736; // @6203
    switch (i) {
    case 0:
        // Block 736 @6203
        return TRUE;
    case 1:
        // Block 739 @6211
        // Block 741 @6214
        return TRUE;
    case 2:
        // Block 744 @6223
        // Block 745 @6227
        return TRUE;
        // Block 746 @6230
    case 3:
        // Block 748 @6236
        // Block 749 @6240
        return TRUE;
        // Block 750 @6243
    case 4:
        // Block 752 @6249
        // Block 753 @6251
        return TRUE;
        // Block 754 @6254
    default:
        // Block 755 @6255
        return FALSE;
    }
    // Block 737 @6206
    goto block_739; // @6211
    // Block 740 @6213
    goto block_742; // @6217
    // Block 742 @6217
    goto block_744; // @6223
}

int func_6259(s_SC_OBJ_info *info) {
    // Block 756 @6259
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_GetPeaceMode(1);
    if (!((1 == SCM_RUN))) {
        // Block 758 @6284
        return FALSE;
    } else {
        // Block 757 @6275
        SC_Ai_SetPeaceMode(0, 0, 0);
        SC_Ai_PointStopDanger(0, 0);
    }
    // Block 759 @6285
    vec = 0;
    local_0 = 0;
    // Block 760 @6304
    if (!((i < SCM_CREATE))) {
        // Block 801 @6633
        return -1;
    } else {
        // Block 760 @6304
        // Block 761 @6308
        SC_P_GetBySideGroupMember(0, 0, i);
        local_0 = i;
        SC_P_IsReady(i);
        // Block 762 @6326
        SC_P_GetPos(i, &vec);
        local_0 = 0;
        // Block 763 @6334
        // Block 764 @6338
        // Block 765 @6346
        // Block 766 @6347
        SC_IsNear3D((0 + (i * SCM_RUNATWP)), &vec, t6360_0);
        // Block 767 @6366
        // Block 768 @6367
        // Block 769 @6381
        // Block 770 @6382
        // Block 772 @6395
        // Block 774 @6401
        local_0 = 0;
        // Block 775 @6407
        SC_P_ScriptMessage(i, SCM_BOOBYTRAPFOUND, 1);
        // Block 776 @6413
        SC_P_ScriptMessage(i, SCM_BOOBYTRAPFOUND, 0);
        // Block 777 @6418
        *((0 + (t6434_0 * SCM_RUNATWP)) + 20) = 1;
        // Block 779 @6447
        local_0 = 0;
        // Block 780 @6455
        SC_P_Speech2(i, 4062, &local_0);
        local_0 = (i + 0.1f);
        // Block 781 @6471
        SC_P_Speech2(i, 4061, &local_0);
        local_0 = (i + 0.1f);
        // Block 782 @6482
        // Block 784 @6488
        local_0 = 0;
        // Block 785 @6496
        SC_P_Speech2(i, 0, &local_0);
        local_0 = (i + 0.1f);
        // Block 786 @6512
        // Block 788 @6518
        local_0 = 0;
        // Block 789 @6526
        SC_P_Speech2(i, 4884, &local_0);
        local_0 = (i + 0.1f);
        // Block 790 @6537
        // Block 792 @6544
        // Block 793 @6546
        SC_P_ScriptMessage(i, SCM_BOOBYTRAPFOUND, 1);
        // Block 794 @6552
        SC_P_ScriptMessage(i, SCM_BOOBYTRAPFOUND, 0);
        // Block 795 @6557
        // Block 796 @6566
        // Block 797 @6595
        *((0 + (i * SCM_RUNATWP)) + 20) = 1;
        // Block 798 @6604
        SC_Log(1713398821, 0, i, i, SCM_TAUNTRUNNER);
        return i;
        // Block 799 @6615
        local_0 = (i + 1);
        // Block 800 @6624
        local_0 = (i + 1);
    }
    switch (vec.y) {
    case 1:
        // Block 772 @6395
        break;
    case 2:
        // Block 774 @6401
        local_0 = 0;
        // Block 775 @6407
        SC_P_ScriptMessage(i, SCM_BOOBYTRAPFOUND, 1);
        // Block 777 @6418
        *((0 + (t6434_0 * SCM_RUNATWP)) + 20) = 1;
        break;
    case 3:
        // Block 779 @6447
        local_0 = 0;
        // Block 780 @6455
        SC_P_Speech2(i, 4062, &local_0);
        local_0 = (i + 0.1f);
        // Block 781 @6471
        SC_P_Speech2(i, 4061, &local_0);
        local_0 = (i + 0.1f);
        // Block 782 @6482
        break;
    case 4:
        // Block 784 @6488
        local_0 = 0;
        // Block 785 @6496
        SC_P_Speech2(i, 0, &local_0);
        local_0 = (i + 0.1f);
        // Block 786 @6512
        break;
    case 5:
        // Block 788 @6518
        local_0 = 0;
        // Block 789 @6526
        SC_P_Speech2(i, 4884, &local_0);
        local_0 = (i + 0.1f);
        // Block 790 @6537
        break;
    case 10:
        // Block 792 @6544
        // Block 793 @6546
        SC_P_ScriptMessage(i, SCM_BOOBYTRAPFOUND, 1);
        // Block 794 @6552
        SC_P_ScriptMessage(i, SCM_BOOBYTRAPFOUND, 0);
        // Block 795 @6557
        break;
    default:
        // Block 796 @6566
        // Block 797 @6595
        *((0 + (i * SCM_RUNATWP)) + 20) = 1;
        // Block 798 @6604
        SC_Log(1713398821, 0, i, i, SCM_TAUNTRUNNER);
        return i;
    }
    // Block 802 @6636
    if (!((j < retval))) {
        // Block 807 @6697
        retval--;
        SC_Ai_ClearCheckPoints(0, 0);
        local_0 = j;
        // Block 808 @6713
        // Block 809 @6717
        sprintf(&"point", i, SCM_WARNABOUTENEMY);
        SC_GetWp(&local_0, &vec.y);
        SC_Ai_AddCheckPoint(0, 0, &vec.y, 0);
        local_0 = (i - 1);
    } else {
        // Block 803 @6643
        retval++;
        SC_Ai_ClearCheckPoints(0, 0);
        local_0 = j;
        // Block 804 @6659
        // Block 805 @6663
        sprintf(&"point", i, SCM_WARNABOUTENEMY);
        SC_GetWp(&local_0, &vec.y);
        SC_Ai_AddCheckPoint(0, 0, &vec.y, 0);
        local_0 = (i + 1);
        // Block 806 @6696
    }
    // Block 811 @6751
    retval++;
    local_0 = j;
    // Block 812 @6766
    if (!((i < retval))) {
        // Block 814 @6803
        return i;
    } else {
        // Block 812 @6766
        // Block 813 @6770
        sprintf(&"point", i, SCM_WARNABOUTENEMY);
        SC_GetWp(&local_0, &vec.y);
        SC_Ai_AddCheckPoint(0, 0, &vec.y, 0);
        local_0 = (i + 1);
    }
}

int func_6804(s_SC_OBJ_info *info) {
    // Block 815 @6804
    local_0 = 1;
    // Block 816 @6810
    if (!((i < SCM_CREATE))) {
        // Block 822 @6861
        return FALSE;
    } else {
        // Block 816 @6810
        // Block 817 @6814
        SC_P_GetBySideGroupMember(0, 0, i);
        SC_P_IsReady(i);
        // Block 818 @6828
        // Block 819 @6829
        SC_P_GetBySideGroupMember(0, 0, i);
        SC_P_Ai_GetPeaceMode(i);
        local_0 = i;
        // Block 820 @6849
        return i;
        // Block 821 @6852
        local_0 = (i + 1);
    }
    // Block 823 @6864
    SC_Ai_SetPeaceMode();
    return FALSE;
}

int func_6873(s_SC_OBJ_info *info) {
    // Block 824 @6873
    local_0 = 0;
    // Block 825 @6879
    if (!((i < SCM_CONFIRM))) {
        // Block 827 @6946
        data_1634[0].field5 = 30.0f;
        data_1634[SCM_HUNTER].field5 = 15.0f;
        data_1634[49].field6 = -100;
        SC_GetWp(&"WayPoint113", 0);
        SC_GetWp(&"WayPoint#33", 0);
        return FALSE;
    } else {
        // Block 825 @6879
        // Block 826 @6883
        *((0 + (i * SCM_HUNTER)) + 24) = 0;
        sprintf(&"ACTIVEPLACE#%d", i, SCM_WARNABOUTENEMY);
        *((0 + (i * SCM_HUNTER)) + 16) = 0;
        local_0 = (i + 1);
    }
}

int func_6984(s_SC_OBJ_info *info) {
    // Block 828 @6984
    goto block_830; // @6991
    switch (i) {
    case 0:
        // Block 830 @6991
        break;
    case 1:
        // Block 832 @6996
        *((0 + (retval * SCM_HUNTER)) + 16) = 0;
        *((0 + (retval * SCM_HUNTER)) + 24) = 1;
        break;
    default:
        // Block 833 @7016
        // Block 835 @7021
        // Block 836 @7025
        // Block 837 @7026
        // Block 838 @7030
        // Block 839 @7031
        // Block 840 @7035
        // Block 841 @7036
        // Block 842 @7040
        // Block 843 @7041
        return FALSE;
    }
}

int func_7043(s_SC_OBJ_info *info) {
    // Block 844 @7043
    SC_PC_Get();
    SC_P_GetWillTalk();
    vec = (unknown_844_7055_1 + 0.2f);
    goto block_846; // @7066
    switch (vec.y) {
    case 0:
        // Block 846 @7066
        // Block 847 @7076
        SC_PC_Get();
        SC_P_Speech2(retval, 903, &vec);
        vec = (vec + 0.1f);
        // Block 849 @7105
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        *((0 + (retval * SCM_HUNTER)) + 16) = t7120_0;
        break;
    case 1:
        // Block 851 @7135
        // Block 852 @7145
        rand();
        // Block 853 @7152
        SC_PC_Get();
        SC_P_Speech2(904, 905, &vec);
        vec = (vec + 0.1f);
        // Block 854 @7167
        SC_PC_Get();
        SC_P_Speech2(904, 911, &vec);
        vec = (vec + 0.1f);
        // Block 855 @7181
        // Block 856 @7182
        SC_PC_Get();
        SC_PC_Get();
        // Block 857 @7210
        SC_PC_Get();
        rand();
        SC_P_Speech2(904, (&vec + (908 % SCM_WARNABOUTENEMY)), &vec);
        vec = (vec + 0.1f);
        // Block 858 @7231
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        *((0 + (retval * SCM_HUNTER)) + 16) = t7246_0;
        break;
    case 2:
        // Block 860 @7261
        SC_PC_Get();
        SC_P_Speech2(&vec, 906, &vec);
        vec = (vec + 0.1f);
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        break;
    case 3:
        // Block 862 @7290
        SC_PC_Get();
        SC_P_SpeechMes2(&vec, 907, &vec, SCM_ENABLE);
        vec = (vec + 0.1f);
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        break;
    case 4:
        // Block 864 @7320
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2060, &vec);
        vec = (vec + 0.1f);
        SC_PC_Get();
        SC_P_SpeechMes2(&vec, 912, &vec, SCM_TELEPORT);
        vec = (vec + 0.1f);
        vec = 0.5f;
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Speech2(0, 913, &vec);
        vec = (vec + 0.1f);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_Speech2(1, 914, &vec);
        vec = (vec + 0.1f);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SpeechMes2(0, 915, &vec, SCM_REMOVE);
        vec = (vec + 0.1f);
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        break;
    case 5:
        // Block 866 @7430
        SC_PC_Get();
        SC_P_Speech2(SCM_REMOVE, 921, &vec);
        vec = (vec + 0.1f);
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        break;
    case 6:
        // Block 868 @7459
        SC_PC_Get();
        SC_P_Speech2(&vec, 922, &vec);
        vec = (vec + 0.1f);
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        break;
    case 8:
        // Block 870 @7488
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_SpeechMes2(1, 924, &vec, SCM_CONFIRM);
        vec = (vec + 0.1f);
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        break;
    case 9:
        // Block 872 @7522
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(0, SC_P_AI_MODE_PEACE);
        SC_GetWp(&"WayPoint113", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_Go(0, &vec);
        break;
    case 10:
        // Block 874 @7567
        // Block 875 @7569
        SC_PC_Get();
        SC_P_SpeechMes2(&vec, 932, &vec, SCM_TIMEDRUN);
        vec = (vec + 0.1f);
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        // Block 876 @7593
        break;
    case 11:
        // Block 878 @7599
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(10419, &vec);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_GetPos(1, &vec);
        SC_SND_PlaySound3D(10419, &vec);
        SC_PC_Get();
        SC_P_Speech2(&vec, 944, &vec);
        vec = (vec + 0.1f);
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        break;
    case 13:
        // Block 880 @7662
        SC_AGS_Set(1);
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        break;
    case 12:
        // Block 882 @7684
        *((0 + (retval * SCM_HUNTER)) + 24) = -100;
        break;
    default:
        // Block 883 @7695
        return TRUE;
    }
    // Block 848 @7091
    SC_PC_Get();
    SC_P_Speech2(retval, 904, &vec);
    vec = (vec + 0.1f);
}

int func_7697(s_SC_OBJ_info *info) {
    // Block 884 @7697
    local_0 = 0;
    // Block 885 @7702
    if (!((i < SCM_CONFIRM))) {
        // Block 890 @7755
        local_0 = 0;
        // Block 891 @7759
        // Block 892 @7763
        // Block 893 @7773
        SC_IsNear3D(j, (0 + (i * SCM_HUNTER)), t7786_0);
        // Block 894 @7792
        // Block 895 @7793
        return i;
        // Block 896 @7797
        local_0 = (i + 1);
        // Block 897 @7806
        return i;
    } else {
        // Block 885 @7702
        // Block 886 @7706
        // Block 887 @7716
        *((0 + (i * SCM_HUNTER)) + 16) = (t7722_0 - retval);
        // Block 888 @7743
        // Block 889 @7746
        local_0 = (i + 1);
    }
}

int func_7807(s_SC_OBJ_info *info) {
    // Block 898 @7807
    goto block_900; // @7817
    switch (vec.y) {
    case 0:
        // Block 900 @7817
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_IsReady(0);
        // Block 901 @7831
        // Block 902 @7832
        // Block 903 @7840
        // Block 904 @7841
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Speech2(0, 926, &vec);
        vec = (vec + 0.1f);
        break;
    case 1:
        // Block 907 @7868
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_IsReady(0);
        // Block 908 @7882
        // Block 909 @7883
        SC_PC_Get();
        SC_P_GetWillTalk(0);
        vec = 0;
        SC_PC_Get();
        SC_P_Speech2(1, 927, &vec);
        vec = (vec + 0.1f);
        // Block 910 @7913
        SC_P_GetBySideGroupMember(1, 0, 0);
        // Block 911 @7929
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(0, SC_P_AI_MODE_BATTLE);
        // Block 912 @7944
        break;
    case 2:
        // Block 914 @7950
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_GetShooting(0, &vec);
        // Block 915 @7965
        SC_PC_Get();
        SC_P_GetWillTalk(0);
        vec = 0;
        SC_PC_Get();
        SC_P_Speech2(0, 929, &vec);
        vec = (vec + 0.1f);
        // Block 916 @7995
        break;
    case 3:
        // Block 918 @8001
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_IsReady(0);
        // Block 919 @8015
        // Block 920 @8016
        SC_PC_Get();
        SC_P_GetWillTalk(0);
        vec = 0;
        SC_PC_Get();
        SC_P_Speech2(1, 927, &vec);
        vec = (vec + 0.1f);
        // Block 921 @8046
        // Block 922 @8056
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(0, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_Go(0, 0);
        SC_PC_Get();
        SC_P_GetWillTalk(0);
        vec = (0 + 0.2f);
        SC_PC_Get();
        SC_P_Speech2(0, 930, &vec);
        vec = (vec + 0.1f);
        // Block 923 @8110
        break;
    case 4:
        // Block 925 @8116
        SC_P_GetBySideGroupMember(1, 0, 0);
        // Block 926 @8132
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_Ai_SetMode(0, SC_P_AI_MODE_BATTLE);
        // Block 927 @8147
        break;
    default:
        // Block 928 @8148
        // Block 929 @8151
        // Block 930 @8152
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_IsReady(1);
        // Block 931 @8166
        // Block 932 @8167
        SC_P_GetBySideGroupMember(1, 0, SCM_RUN);
        SC_P_IsReady(SCM_RUN);
        // Block 933 @8181
        // Block 934 @8182
        SC_PC_Get();
        SC_P_GetWillTalk(0);
        vec = (0 + 0.5f);
        SC_PC_Get();
        SC_P_Speech2(1, 928, &vec);
        vec = (vec + 0.1f);
        // Block 935 @8214
        // Block 936 @8216
        // Block 937 @8217
        SC_P_GetBySideGroupMember(1, 0, SCM_TAUNTRUNNER);
        SC_P_IsReady(SCM_TAUNTRUNNER);
        // Block 938 @8231
        // Block 939 @8232
        SC_P_GetBySideGroupMember(1, 0, SCM_BOOBYTRAPFOUND);
        SC_P_IsReady(SCM_BOOBYTRAPFOUND);
        // Block 940 @8246
        // Block 941 @8247
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_IsReady(0);
        // Block 942 @8261
        // Block 943 @8262
        SC_PC_Get();
        SC_P_GetWillTalk(0);
        vec = (0 + 0.5f);
        SC_PC_Get();
        SC_P_Speech2(1, 931, &vec);
        vec = (vec + 0.1f);
        // Block 944 @8294
        // Block 945 @8298
        // Block 946 @8306
        // Block 947 @8307
        SC_P_GetBySideGroupMember(1, 1, 0);
        rand();
        SC_P_Speech2(1, (0 + (947 % SCM_RUN)), &vec);
        vec = (vec + 0.1f);
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(0, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(1, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_SetMode(SCM_RUN, SC_P_AI_MODE_BATTLE);
        // Block 948 @8369
        // Block 949 @8373
        // Block 950 @8381
        // Block 951 @8382
        SC_P_GetBySideGroupMember(1, 1, 1);
        rand();
        SC_P_Speech2(1, (1 + (947 % SCM_RUN)), &vec);
        vec = (vec + 0.1f);
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(0, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(1, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_SetMode(SCM_RUN, SC_P_AI_MODE_BATTLE);
        // Block 952 @8444
        // Block 953 @8448
        // Block 954 @8456
        // Block 955 @8457
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        rand();
        SC_P_Speech2(1, (SCM_RUN + (947 % SCM_RUN)), &vec);
        vec = (vec + 0.1f);
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(0, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(1, SC_P_AI_MODE_BATTLE);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_SetMode(SCM_RUN, SC_P_AI_MODE_BATTLE);
        // Block 956 @8519
        // Block 958 @8526
        // Block 960 @8532
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(0, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(1, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_SetMode(SCM_RUN, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_Stop(0);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_Stop(1);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_Stop(SCM_RUN);
        frnd(20.0f);
        (25.0f + 20.0f) = 0;
        rand();
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetPos(0, &vec);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_Go(SCM_RUN, &vec);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_GetPos(SCM_RUN, 0);
        // Block 962 @8658
        // Block 964 @8665
        // Block 966 @8670
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetDistance(1, 0);
        // Block 967 @8694
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        rand();
        SC_P_Speech2(1, (SCM_RUN + (945 % SCM_RUN)), &vec);
        vec = (vec + 0.1f);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_Go(SCM_RUN, 0);
        // Block 968 @8734
        // Block 970 @8740
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        // Block 971 @8756
        rand();
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetPos(0, &vec);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_Go(SCM_RUN, &vec);
        // Block 972 @8787
        // Block 973 @8788
        // Block 974 @8799
        frnd(20.0f);
        (25.0f + 20.0f) = 0;
        vec = 0;
        rand();
        SC_P_GetBySideGroupMember(&vec, 1, (1 % SCM_RUN));
        rand();
        SC_P_Speech2(1, ((1 % SCM_RUN) + (939 % SCM_WARNABOUTENEMY)), &vec);
        vec = (vec + 0.1f);
        // Block 975 @8844
        // Block 976 @8854
        frnd(5.0f);
        (5.0f + 5.0f) = 0;
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(10419, &vec);
        // Block 977 @8880
        // Block 978 @8890
        frnd(5.0f);
        (5.0f + 5.0f) = 0;
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_GetPos(1, &vec);
        SC_SND_PlaySound3D(10419, &vec);
        // Block 979 @8916
        // Block 980 @8917
        return &vec;
    }
    // Block 905 @7863
    goto block_907; // @7868
    switch (vec.y) {
    case 0:
        // Block 958 @8526
        break;
    case 1:
        // Block 960 @8532
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_SetMode(0, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_SetMode(1, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_SetMode(SCM_RUN, SC_P_AI_MODE_PEACE);
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_Ai_Stop(0);
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_Ai_Stop(1);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_Stop(SCM_RUN);
        frnd(20.0f);
        (25.0f + 20.0f) = 0;
        rand();
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetPos(0, &vec);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_Go(SCM_RUN, &vec);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_GetPos(SCM_RUN, 0);
        break;
    case 2:
        // Block 962 @8658
        break;
    default:
        // Block 980 @8917
        return &vec;
    }
    switch (vec.y) {
    case 0:
        // Block 964 @8665
        break;
    case 1:
        // Block 966 @8670
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetDistance(1, 0);
        // Block 967 @8694
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        rand();
        SC_P_Speech2(1, (SCM_RUN + (945 % SCM_RUN)), &vec);
        vec = (vec + 0.1f);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_Go(SCM_RUN, 0);
        break;
    case 2:
        // Block 970 @8740
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        // Block 971 @8756
        rand();
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetPos(0, &vec);
        SC_P_GetBySideGroupMember(1, 1, SCM_RUN);
        SC_P_Ai_Go(SCM_RUN, &vec);
        // Block 972 @8787
        break;
    default:
        // Block 973 @8788
        // Block 974 @8799
        frnd(20.0f);
        (25.0f + 20.0f) = 0;
        vec = 0;
        rand();
        SC_P_GetBySideGroupMember(&vec, 1, (1 % SCM_RUN));
        rand();
        SC_P_Speech2(1, ((1 % SCM_RUN) + (939 % SCM_WARNABOUTENEMY)), &vec);
        vec = (vec + 0.1f);
        // Block 975 @8844
        // Block 976 @8854
        frnd(5.0f);
        (5.0f + 5.0f) = 0;
        SC_P_GetBySideGroupMember(1, 1, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(10419, &vec);
        // Block 977 @8880
        // Block 978 @8890
        frnd(5.0f);
        (5.0f + 5.0f) = 0;
        SC_P_GetBySideGroupMember(1, 1, 1);
        SC_P_GetPos(1, &vec);
        SC_SND_PlaySound3D(10419, &vec);
        // Block 979 @8916
        // Block 980 @8917
        return &vec;
    }
}

int func_8919(s_SC_OBJ_info *info) {
    // Block 981 @8919
    SC_SetObjectScript(&"grenadebedna", &"levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\openablecr...");
    SC_SetObjectScript(&"n_poklop_01", &"levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\poklop.c");
    SC_SetObjectScript(&"d_past_04_01", &"levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\past.c");
    return FALSE;
}

int func_8932(s_SC_OBJ_info *info) {
    // Block 982 @8932
    return FALSE;
}

int func_8933(s_SC_OBJ_info *info) {
    // Block 983 @8933
    return FALSE;
}

int func_8934(s_SC_OBJ_info *info) {
    // Block 984 @8934
    SC_PC_Get();
    SC_P_GetWillTalk();
    local_0 = unknown_984_8945_1;
    if (!(0)) {
        // Block 986 @8950
        SC_NOD_GetName(t8954_0);
        SC_StringSame(t8954_0, &"grenadebedna");
        // Block 987 @8965
        // Block 988 @8966
        SC_PC_Get();
        SC_P_Speech2(t8954_0, 923, &local_0);
        local_0 = (i + 0.1f);
        return FALSE;
    } else {
        // Block 985 @8949
    }
    // Block 989 @8985
    if (!(0)) {
        // Block 991 @8988
        SC_NOD_GetName(t8992_0);
        SC_StringSame(t8992_0, &"n_poklop_01");
        // Block 992 @9003
        // Block 993 @9004
        SC_PC_Get();
        SC_P_Speech2(t8992_0, 938, &local_0);
        local_0 = (i + 0.1f);
        return FALSE;
    } else {
        // Block 990 @8987
    }
    // Block 994 @9023
    SC_NOD_GetName(t9027_0);
    SC_StringSame(t9027_0, &"granat_v_plechovce2#3");
    if (!(&"granat_v_plechovce2#3")) {
        // Block 996 @9053
        return t8992_0;
    } else {
        // Block 995 @9038
        SC_PC_Get();
        SC_P_Speech2(t9027_0, 925, &local_0);
        local_0 = (i + 0.1f);
        return &local_0;
    }
}

int ScriptMain(s_SC_OBJ_info *info) {
    // Block 997 @9054
    goto block_999; // @9074
    switch (local_5) {
    case 7:
        // Block 999 @9074
        break;
    case 11:
        // Block 1001 @9081
        break;
    case 8:
        // Block 1003 @9088
        break;
    case 4:
        // Block 1005 @9095
        break;
    case 0:
        // Block 1010 @9115
        // Block 1012 @9122
        SC_sgi(SGI_CURRENTMISSION, SCM_ONWAYPOINT);
        SC_ZeroMem(&local_0, SCM_SETGPHASE);
        SC_ZeroMem(&local_1, SCM_DISARMTRAP);
        SC_DeathCamera_Enable(0);
        SC_RadioSetDist(10.0f);
        SC_ZeroMem(&local_5, SCM_SETGPHASE);
        local_5 = SCM_MORTARLAND;
        local_5.field1 = SCM_SETGPHASE;
        SC_InitSide(0, &local_5);
        SC_ZeroMem(&local_5, SCM_SETGPHASE);
        local_5 = SCM_YOUARECOMMANDER;
        local_5.field1 = SCM_WALK;
        SC_InitSide(1, &local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 0;
        local_5.field1 = 0;
        local_5.field2 = SCM_BOOBYTRAPFOUND;
        local_5.field4 = 30.0f;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = 0;
        local_5.field2 = SCM_ONWAYPOINT;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = 1;
        local_5.field2 = SCM_WALK;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = SCM_RUN;
        local_5.field2 = SCM_WALK;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = SCM_WARNABOUTENEMY;
        local_5.field2 = SCM_ONWAYPOINT;
        SC_InitSideGroup(&local_5);
        SC_Ai_SetShootOnHeardEnemyColTest(1);
        SC_Ai_SetGroupEnemyUpdate(1, 0, 0);
        SC_Ai_SetGroupEnemyUpdate(1, 1, 0);
        SC_Ai_SetGroupEnemyUpdate(1, SCM_RUN, 0);
        SC_Ai_SetGroupEnemyUpdate(1, SCM_WARNABOUTENEMY, 0);
        SC_sgi(SCM_CREATE, 1);
        SC_Log(1702257996, 1, SCM_WARNABOUTENEMY);
        SC_Osi(&"Levelphase changed to %d", 1, SCM_RUN);
        SC_SetCommandMenu(2009);
        // Block 1014 @9355
        local_0 = 1.0f;
        SC_AGS_Set(0);
        SC_PC_Get();
        SC_P_SpeechMes2(0, 900, &local_0, 1);
        local_0 = (i + 0.1f);
        SC_sgi(SCM_CREATE, SCM_RUN);
        SC_Log(1702257996, SCM_RUN, SCM_WARNABOUTENEMY);
        SC_Osi(&"Levelphase changed to %d", SCM_RUN, SCM_RUN);
        // Block 1016 @9416
        SC_PC_GetPos(&vec);
        // Block 1017 @9436
        break;
    case 1:
        // Block 1019 @9443
        SC_PC_Get();
        SC_P_GetWillTalk(info->hit_by);
        local_0 = info->hit_by;
        SC_PC_EnableMovement(0);
        SC_PC_EnableRadioBreak(1);
        // Block 1021 @9470
        SC_RadioBatch_Begin();
        SC_PC_Get();
        SC_P_Speech2(info->master_nod, 916, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(917, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_Speech2(&local_0, 918, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(919, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_SpeechMes2(&local_0, 920, &local_0, SCM_RUN);
        local_0 = (i + 0.1f);
        SC_RadioBatch_End();
        // Block 1023 @9577
        SC_RadioBatch_Begin();
        SC_PC_Get();
        SC_P_Speech2(SCM_RUN, 933, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(934, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_Speech2(&local_0, 935, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(936, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_SpeechMes2(&local_0, 937, &local_0, SCM_WARNABOUTENEMY);
        local_0 = (i + 0.1f);
        SC_RadioBatch_End();
        // Block 1024 @9679
        // Block 1026 @9686
        // Block 1028 @9695
        // Block 1029 @9704
        // Block 1030 @9705
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        local_5.field2 = 0;
        local_5 = 9110;
        local_5.field1 = 9111;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9110, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9110, SCM_RUN);
        // Block 1031 @9745
        // Block 1033 @9751
        // Block 1034 @9760
        // Block 1035 @9761
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9112;
        local_5.field1 = 9113;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9112, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9112, SCM_RUN);
        // Block 1036 @9804
        // Block 1038 @9810
        // Block 1039 @9819
        // Block 1040 @9820
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9114;
        local_5.field1 = 9115;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9114, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9114, SCM_RUN);
        // Block 1041 @9863
        // Block 1043 @9869
        SC_Radio_Enable(1);
        // Block 1045 @9878
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2055, &vec);
        // Block 1047 @9899
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2060, &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_GetPos(1, &vec);
        SC_SND_PlaySound3D(2070, &vec);
        SC_GetWp(&"WayPoint53", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        SC_GetWp(&"WayPoint#9", &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_SetPos(1, &vec);
        // Block 1049 @9973
        SC_GetWp(&"WayPoint57", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        // Block 1051 @9998
        SC_Radio_Enable(SCM_RUN);
        // Block 1053 @10007
        // Block 1054 @10009
        // Block 1056 @10016
        // Block 1057 @10022
        *t10024_0 = 0;
        // Block 1058 @10028
        info->nod = t10035_0;
        *t10043_0 = 1;
        // Block 1059 @10046
        // Block 1060 @10047
        return TRUE;
    default:
        // Block 1025 @9682
        // Block 1026 @9686
        // Block 1028 @9695
        // Block 1029 @9704
        // Block 1030 @9705
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        local_5.field2 = 0;
        local_5 = 9110;
        local_5.field1 = 9111;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9110, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9110, SCM_RUN);
        // Block 1031 @9745
        // Block 1033 @9751
        // Block 1034 @9760
        // Block 1035 @9761
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9112;
        local_5.field1 = 9113;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9112, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9112, SCM_RUN);
        // Block 1036 @9804
        // Block 1038 @9810
        // Block 1039 @9819
        // Block 1040 @9820
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9114;
        local_5.field1 = 9115;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9114, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9114, SCM_RUN);
        // Block 1041 @9863
        // Block 1043 @9869
        SC_Radio_Enable(1);
        // Block 1045 @9878
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2055, &vec);
        // Block 1047 @9899
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2060, &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_GetPos(1, &vec);
        SC_SND_PlaySound3D(2070, &vec);
        SC_GetWp(&"WayPoint53", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        SC_GetWp(&"WayPoint#9", &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_SetPos(1, &vec);
        // Block 1049 @9973
        SC_GetWp(&"WayPoint57", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        // Block 1051 @9998
        SC_Radio_Enable(SCM_RUN);
        // Block 1053 @10007
        // Block 1054 @10009
        // Block 1055 @10012
        // Block 1056 @10016
        // Block 1057 @10022
        *t10024_0 = 0;
        // Block 1058 @10028
        info->nod = t10035_0;
        *t10043_0 = 1;
        // Block 1059 @10046
        // Block 1060 @10047
        return TRUE;
    }
    // Block 1006 @9100
    if (!((local_5 == SCM_OBJECTUSED))) {
        // Block 1008 @9108
        // Block 1010 @9115
        // Block 1012 @9122
        SC_sgi(SGI_CURRENTMISSION, SCM_ONWAYPOINT);
        SC_ZeroMem(&local_0, SCM_SETGPHASE);
        SC_ZeroMem(&local_1, SCM_DISARMTRAP);
        SC_DeathCamera_Enable(0);
        SC_RadioSetDist(10.0f);
        SC_ZeroMem(&local_5, SCM_SETGPHASE);
        local_5 = SCM_MORTARLAND;
        local_5.field1 = SCM_SETGPHASE;
        SC_InitSide(0, &local_5);
        SC_ZeroMem(&local_5, SCM_SETGPHASE);
        local_5 = SCM_YOUARECOMMANDER;
        local_5.field1 = SCM_WALK;
        SC_InitSide(1, &local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 0;
        local_5.field1 = 0;
        local_5.field2 = SCM_BOOBYTRAPFOUND;
        local_5.field4 = 30.0f;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = 0;
        local_5.field2 = SCM_ONWAYPOINT;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = 1;
        local_5.field2 = SCM_WALK;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = SCM_RUN;
        local_5.field2 = SCM_WALK;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = SCM_WARNABOUTENEMY;
        local_5.field2 = SCM_ONWAYPOINT;
        SC_InitSideGroup(&local_5);
        SC_Ai_SetShootOnHeardEnemyColTest(1);
        SC_Ai_SetGroupEnemyUpdate(1, 0, 0);
        SC_Ai_SetGroupEnemyUpdate(1, 1, 0);
        SC_Ai_SetGroupEnemyUpdate(1, SCM_RUN, 0);
        SC_Ai_SetGroupEnemyUpdate(1, SCM_WARNABOUTENEMY, 0);
        SC_sgi(SCM_CREATE, 1);
        SC_Log(1702257996, 1, SCM_WARNABOUTENEMY);
        SC_Osi(&"Levelphase changed to %d", 1, SCM_RUN);
        SC_SetCommandMenu(2009);
        // Block 1014 @9355
        local_0 = 1.0f;
        SC_AGS_Set(0);
        SC_PC_Get();
        SC_P_SpeechMes2(0, 900, &local_0, 1);
        local_0 = (i + 0.1f);
        SC_sgi(SCM_CREATE, SCM_RUN);
        SC_Log(1702257996, SCM_RUN, SCM_WARNABOUTENEMY);
        SC_Osi(&"Levelphase changed to %d", SCM_RUN, SCM_RUN);
        // Block 1016 @9416
        SC_PC_GetPos(&vec);
        // Block 1017 @9436
        // Block 1019 @9443
        SC_PC_Get();
        SC_P_GetWillTalk(info->hit_by);
        local_0 = info->hit_by;
        SC_PC_EnableMovement(0);
        SC_PC_EnableRadioBreak(1);
        // Block 1021 @9470
        SC_RadioBatch_Begin();
        SC_PC_Get();
        SC_P_Speech2(info->master_nod, 916, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(917, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_Speech2(&local_0, 918, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(919, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_SpeechMes2(&local_0, 920, &local_0, SCM_RUN);
        local_0 = (i + 0.1f);
        SC_RadioBatch_End();
        // Block 1023 @9577
        SC_RadioBatch_Begin();
        SC_PC_Get();
        SC_P_Speech2(SCM_RUN, 933, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(934, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_Speech2(&local_0, 935, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(936, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_SpeechMes2(&local_0, 937, &local_0, SCM_WARNABOUTENEMY);
        local_0 = (i + 0.1f);
        SC_RadioBatch_End();
        // Block 1024 @9679
        // Block 1026 @9686
        // Block 1028 @9695
        // Block 1029 @9704
        // Block 1030 @9705
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        local_5.field2 = 0;
        local_5 = 9110;
        local_5.field1 = 9111;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9110, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9110, SCM_RUN);
        // Block 1031 @9745
        // Block 1033 @9751
        // Block 1034 @9760
        // Block 1035 @9761
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9112;
        local_5.field1 = 9113;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9112, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9112, SCM_RUN);
        // Block 1036 @9804
        // Block 1038 @9810
        // Block 1039 @9819
        // Block 1040 @9820
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9114;
        local_5.field1 = 9115;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9114, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9114, SCM_RUN);
        // Block 1041 @9863
        // Block 1043 @9869
        SC_Radio_Enable(1);
        // Block 1045 @9878
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2055, &vec);
        // Block 1047 @9899
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2060, &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_GetPos(1, &vec);
        SC_SND_PlaySound3D(2070, &vec);
        SC_GetWp(&"WayPoint53", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        SC_GetWp(&"WayPoint#9", &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_SetPos(1, &vec);
        // Block 1049 @9973
        SC_GetWp(&"WayPoint57", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        // Block 1051 @9998
        SC_Radio_Enable(SCM_RUN);
        // Block 1053 @10007
        // Block 1054 @10009
        // Block 1056 @10016
        // Block 1057 @10022
        *t10024_0 = 0;
        // Block 1058 @10028
        info->nod = t10035_0;
        *t10043_0 = 1;
        // Block 1059 @10046
        // Block 1060 @10047
        return TRUE;
    } else {
        // Block 1007 @9104
    }
    switch (local_5) {
    case 0:
        // Block 1012 @9122
        SC_sgi(SGI_CURRENTMISSION, SCM_ONWAYPOINT);
        SC_ZeroMem(&local_0, SCM_SETGPHASE);
        SC_ZeroMem(&local_1, SCM_DISARMTRAP);
        SC_DeathCamera_Enable(0);
        SC_RadioSetDist(10.0f);
        SC_ZeroMem(&local_5, SCM_SETGPHASE);
        local_5 = SCM_MORTARLAND;
        local_5.field1 = SCM_SETGPHASE;
        SC_InitSide(0, &local_5);
        SC_ZeroMem(&local_5, SCM_SETGPHASE);
        local_5 = SCM_YOUARECOMMANDER;
        local_5.field1 = SCM_WALK;
        SC_InitSide(1, &local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 0;
        local_5.field1 = 0;
        local_5.field2 = SCM_BOOBYTRAPFOUND;
        local_5.field4 = 30.0f;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = 0;
        local_5.field2 = SCM_ONWAYPOINT;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = 1;
        local_5.field2 = SCM_WALK;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = SCM_RUN;
        local_5.field2 = SCM_WALK;
        SC_InitSideGroup(&local_5);
        SC_ZeroMem(&local_5, SCM_DISARMTRAP);
        local_5 = 1;
        local_5.field1 = SCM_WARNABOUTENEMY;
        local_5.field2 = SCM_ONWAYPOINT;
        SC_InitSideGroup(&local_5);
        SC_Ai_SetShootOnHeardEnemyColTest(1);
        SC_Ai_SetGroupEnemyUpdate(1, 0, 0);
        SC_Ai_SetGroupEnemyUpdate(1, 1, 0);
        SC_Ai_SetGroupEnemyUpdate(1, SCM_RUN, 0);
        SC_Ai_SetGroupEnemyUpdate(1, SCM_WARNABOUTENEMY, 0);
        SC_sgi(SCM_CREATE, 1);
        SC_Log(1702257996, 1, SCM_WARNABOUTENEMY);
        SC_Osi(&"Levelphase changed to %d", 1, SCM_RUN);
        SC_SetCommandMenu(2009);
        break;
    case 1:
        // Block 1014 @9355
        local_0 = 1.0f;
        SC_AGS_Set(0);
        SC_PC_Get();
        SC_P_SpeechMes2(0, 900, &local_0, 1);
        local_0 = (i + 0.1f);
        SC_sgi(SCM_CREATE, SCM_RUN);
        SC_Log(1702257996, SCM_RUN, SCM_WARNABOUTENEMY);
        SC_Osi(&"Levelphase changed to %d", SCM_RUN, SCM_RUN);
        break;
    case 2:
        // Block 1016 @9416
        SC_PC_GetPos(&vec);
        break;
    default:
        // Block 1017 @9436
        // Block 1019 @9443
        SC_PC_Get();
        SC_P_GetWillTalk(info->hit_by);
        local_0 = info->hit_by;
        SC_PC_EnableMovement(0);
        SC_PC_EnableRadioBreak(1);
        // Block 1021 @9470
        SC_RadioBatch_Begin();
        SC_PC_Get();
        SC_P_Speech2(info->master_nod, 916, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(917, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_Speech2(&local_0, 918, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(919, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_SpeechMes2(&local_0, 920, &local_0, SCM_RUN);
        local_0 = (i + 0.1f);
        SC_RadioBatch_End();
        // Block 1023 @9577
        SC_RadioBatch_Begin();
        SC_PC_Get();
        SC_P_Speech2(SCM_RUN, 933, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(934, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_Speech2(&local_0, 935, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(936, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_SpeechMes2(&local_0, 937, &local_0, SCM_WARNABOUTENEMY);
        local_0 = (i + 0.1f);
        SC_RadioBatch_End();
        // Block 1024 @9679
        // Block 1026 @9686
        // Block 1028 @9695
        // Block 1029 @9704
        // Block 1030 @9705
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        local_5.field2 = 0;
        local_5 = 9110;
        local_5.field1 = 9111;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9110, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9110, SCM_RUN);
        // Block 1031 @9745
        // Block 1033 @9751
        // Block 1034 @9760
        // Block 1035 @9761
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9112;
        local_5.field1 = 9113;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9112, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9112, SCM_RUN);
        // Block 1036 @9804
        // Block 1038 @9810
        // Block 1039 @9819
        // Block 1040 @9820
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9114;
        local_5.field1 = 9115;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9114, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9114, SCM_RUN);
        // Block 1041 @9863
        // Block 1043 @9869
        SC_Radio_Enable(1);
        // Block 1045 @9878
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2055, &vec);
        // Block 1047 @9899
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2060, &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_GetPos(1, &vec);
        SC_SND_PlaySound3D(2070, &vec);
        SC_GetWp(&"WayPoint53", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        SC_GetWp(&"WayPoint#9", &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_SetPos(1, &vec);
        // Block 1049 @9973
        SC_GetWp(&"WayPoint57", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        // Block 1051 @9998
        SC_Radio_Enable(SCM_RUN);
        // Block 1053 @10007
        // Block 1054 @10009
        // Block 1056 @10016
        // Block 1057 @10022
        *t10024_0 = 0;
        // Block 1058 @10028
        info->nod = t10035_0;
        *t10043_0 = 1;
        // Block 1059 @10046
        // Block 1060 @10047
        return TRUE;
    }
    switch (local_5) {
    case 1:
        // Block 1021 @9470
        SC_RadioBatch_Begin();
        SC_PC_Get();
        SC_P_Speech2(info->master_nod, 916, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(917, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_Speech2(&local_0, 918, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(919, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_SpeechMes2(&local_0, 920, &local_0, SCM_RUN);
        local_0 = (i + 0.1f);
        SC_RadioBatch_End();
        break;
    case 2:
        // Block 1023 @9577
        SC_RadioBatch_Begin();
        SC_PC_Get();
        SC_P_Speech2(SCM_RUN, 933, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(934, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_Speech2(&local_0, 935, &local_0);
        local_0 = (i + 0.1f);
        local_0 = (i + 0.3f);
        SC_SpeechRadio2(936, &local_0);
        local_0 = (i + (0.1f + 0.2f));
        SC_PC_Get();
        SC_P_SpeechMes2(&local_0, 937, &local_0, SCM_WARNABOUTENEMY);
        local_0 = (i + 0.1f);
        SC_RadioBatch_End();
        break;
    default:
        // Block 1024 @9679
        // Block 1026 @9686
        // Block 1028 @9695
        // Block 1029 @9704
        // Block 1030 @9705
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        local_5.field2 = 0;
        local_5 = 9110;
        local_5.field1 = 9111;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9110, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9110, SCM_RUN);
        // Block 1031 @9745
        // Block 1033 @9751
        // Block 1034 @9760
        // Block 1035 @9761
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9112;
        local_5.field1 = 9113;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9112, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9112, SCM_RUN);
        // Block 1036 @9804
        // Block 1038 @9810
        // Block 1039 @9819
        // Block 1040 @9820
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9114;
        local_5.field1 = 9115;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9114, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9114, SCM_RUN);
        // Block 1041 @9863
        // Block 1043 @9869
        SC_Radio_Enable(1);
        // Block 1045 @9878
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2055, &vec);
        // Block 1047 @9899
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2060, &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_GetPos(1, &vec);
        SC_SND_PlaySound3D(2070, &vec);
        SC_GetWp(&"WayPoint53", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        SC_GetWp(&"WayPoint#9", &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_SetPos(1, &vec);
        // Block 1049 @9973
        SC_GetWp(&"WayPoint57", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        // Block 1051 @9998
        SC_Radio_Enable(SCM_RUN);
        // Block 1053 @10007
        // Block 1054 @10009
        // Block 1056 @10016
        // Block 1057 @10022
        *t10024_0 = 0;
        // Block 1058 @10028
        info->nod = t10035_0;
        *t10043_0 = 1;
        // Block 1059 @10046
        // Block 1060 @10047
        return TRUE;
    }
    switch (local_5) {
    case 1:
        // Block 1028 @9695
        // Block 1030 @9705
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        local_5.field2 = 0;
        local_5 = 9110;
        local_5.field1 = 9111;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9110, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9110, SCM_RUN);
        // Block 1031 @9745
        break;
    case 2:
        // Block 1033 @9751
        // Block 1034 @9760
        // Block 1035 @9761
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9112;
        local_5.field1 = 9113;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9112, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9112, SCM_RUN);
        // Block 1036 @9804
        break;
    case 3:
        // Block 1038 @9810
        // Block 1039 @9819
        // Block 1040 @9820
        (0 + (info->master_nod * SCM_BOOBYTRAPFOUND)) = 1;
        SC_PC_EnableMovement(1);
        local_5.field2 = 0;
        local_5 = 9114;
        local_5.field1 = 9115;
        SC_MissionSave(&local_5);
        SC_Log(1769365843, 9114, SCM_WARNABOUTENEMY);
        SC_Osi(&"Saving game id %d", 9114, SCM_RUN);
        // Block 1041 @9863
        break;
    case 11:
        // Block 1043 @9869
        SC_Radio_Enable(1);
        break;
    case 12:
        // Block 1045 @9878
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2055, &vec);
        break;
    case 13:
        // Block 1047 @9899
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_GetPos(0, &vec);
        SC_SND_PlaySound3D(2060, &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_GetPos(1, &vec);
        SC_SND_PlaySound3D(2070, &vec);
        SC_GetWp(&"WayPoint53", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        SC_GetWp(&"WayPoint#9", &vec);
        SC_P_GetBySideGroupMember(1, 0, 1);
        SC_P_SetPos(1, &vec);
        break;
    case 14:
        // Block 1049 @9973
        SC_GetWp(&"WayPoint57", &vec);
        SC_P_GetBySideGroupMember(1, 0, 0);
        SC_P_SetPos(0, &vec);
        break;
    case 15:
        // Block 1051 @9998
        SC_Radio_Enable(SCM_RUN);
        break;
    case 100:
        // Block 1053 @10007
        break;
    default:
        // Block 1054 @10009
        // Block 1056 @10016
        // Block 1057 @10022
        *t10024_0 = 0;
        // Block 1058 @10028
        info->nod = t10035_0;
        *t10043_0 = 1;
        // Block 1059 @10046
        // Block 1060 @10047
        return TRUE;
    }
}

