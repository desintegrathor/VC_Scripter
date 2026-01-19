// Structured decompilation of decompilation/LEVEL/PLAYER.SCR
// Functions: 15

int _init(s_SC_OBJ_info *info) {
    // Block 0 @0
    return FALSE;
    // Block 1 @1
    frnd(idx);
    local_0 = idx;
    if (!((i < 0))) {
        // Block 3 @20
        return i;
    } else {
        // Block 2 @15
        local_0 = (-i);
    }
    // Block 4 @23
    SC_P_Ai_SetMode(retval, SC_P_AI_MODE_BATTLE);
    SC_P_Ai_EnableShooting(retval, TRUE);
    SC_P_Ai_EnableSituationUpdate(retval, 1);
    SC_Log(2036427856, retval, SCM_WARNABOUTENEMY);
    return FALSE;
    // Block 5 @42
    SC_P_Ai_SetMode(retval, SC_P_AI_MODE_PEACE);
    SC_P_Ai_EnableShooting(retval, FALSE);
    SC_P_Ai_EnableSituationUpdate(retval, 0);
    SC_P_Ai_Stop(retval);
    SC_Log(2036427856, retval, SCM_WARNABOUTENEMY);
    return FALSE;
}

int func_0064(s_SC_OBJ_info *info) {
    // Block 6 @64
    if (!(k)) {
        // Block 8 @67
        SC_Log(1936942413, k, retval, SCM_BOOBYTRAPFOUND);
        return FALSE;
    } else {
        // Block 7 @66
        // Block 9 @75
        SC_P_ScriptMessage(k, k, retval);
        return FALSE;
    }
    // Block 10 @81
    SC_P_GetBySideGroupMember(1, k, k);
    SC_P_Ai_GetSureEnemies(k);
    if (!(k)) {
        // Block 12 @98
        SC_P_GetBySideGroupMember(1, k, k);
        SC_P_Ai_GetDanger(k);
        // Block 13 @114
        return FALSE;
        // Block 14 @117
        return FALSE;
    } else {
        // Block 11 @95
        return FALSE;
    }
    // Block 15 @120
    SC_P_Ai_GetSureEnemies(k);
    if (!(k)) {
        // Block 17 @130
        SC_P_Ai_GetDanger(k);
        // Block 18 @139
        return FALSE;
        // Block 19 @142
        return FALSE;
    } else {
        // Block 16 @127
        return FALSE;
    }
    // Block 20 @145
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(k, &ai_props);
    ai_props.field19 = retval;
    SC_P_Ai_SetProps(k, &ai_props);
    return &ai_props;
    // Block 21 @164
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(k, &ai_props);
    ai_props.field11 = retval;
    SC_P_Ai_SetProps(k, &ai_props);
    return &ai_props;
    // Block 22 @183
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(k, &ai_props);
    ai_props.field5 = (t194_0 * retval);
    SC_P_Ai_SetProps(k, &ai_props);
    return &ai_props;
    // Block 23 @206
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(k, &ai_props);
    ai_props.field18 = (t217_0 * retval);
    SC_P_Ai_SetProps(k, &ai_props);
    return &ai_props;
    // Block 24 @229
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(k, &ai_props);
    if (!(retval)) {
        // Block 26 @246
        ai_props.field16 = 1000.0f;
    } else {
        // Block 25 @240
        ai_props.field16 = 5.0f;
    }
    // Block 27 @251
    SC_P_Ai_SetProps(k, &ai_props);
    return &ai_props;
    // Block 28 @256
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(k, &ai_props);
    ai_props.field25 = retval;
    SC_P_Ai_SetProps(k, &ai_props);
    return &ai_props;
    // Block 29 @275
    SC_ggi(SGI_CURRENTMISSION);
    return FALSE;
    // Block 30 @283
    SC_ggi(SCM_HEARDSOMETHING);
    return FALSE;
    // Block 31 @291
    SC_P_GetInfo(k, &ai_props);
    return t297_0;
    // Block 32 @300
    SC_ZeroMem(&ai_props, 128);
    SC_P_Ai_GetProps(k, &ai_props);
    ai_props = retval;
    SC_P_Ai_SetProps(k, &ai_props);
    return &ai_props;
}

int func_0318(s_SC_OBJ_info *info) {
    // Block 33 @318
    SC_ggi(101);
    *t325_0 = 101;
    if (!(t330_0)) {
        // Block 35 @333
        *t335_0 = SCM_RUNANDKILL;
    } else {
        // Block 34 @332
    }
    // Block 36 @338
    if (!((t340_0 == 255))) {
        // Block 38 @349
        SC_ggi(102);
        *t356_0 = 102;
        // Block 39 @363
        // Block 40 @364
        *t366_0 = SCM_HEARDSOMETHING;
        // Block 41 @369
        // Block 42 @375
        *t377_0 = 0;
        // Block 43 @380
        SC_ggi(103);
        *t387_0 = 103;
        // Block 44 @394
        // Block 45 @395
        SC_ggi(SGI_CURRENTMISSION);
        // Block 46 @404
        *t406_0 = SCM_RETREAT;
        // Block 47 @410
        SC_ggi(SGI_CURRENTMISSION);
        // Block 48 @419
        *t421_0 = SCM_STARTWALK;
        // Block 49 @425
        *t427_0 = 1;
        // Block 50 @430
        // Block 51 @436
        *t438_0 = 0;
        // Block 52 @441
        SC_ggi(104);
        *t448_0 = 104;
        // Block 53 @457
        *t459_0 = 0;
        // Block 54 @462
        SC_ggi(105);
        *t469_0 = 105;
        // Block 55 @476
        // Block 56 @477
        *t479_0 = SCM_DISABLEINTERACTION;
        // Block 57 @482
        // Block 58 @488
        *t490_0 = 0;
        // Block 59 @493
        SC_ggi(106);
        *t500_0 = 106;
        // Block 60 @509
        *t511_0 = 0;
        // Block 61 @514
        SC_ggi(107);
        *t521_0 = 107;
        // Block 62 @530
        *t532_0 = 0;
        // Block 63 @535
        SC_ggi(108);
        *t542_0 = 108;
        // Block 64 @549
        // Block 65 @550
        *t552_0 = SCM_RADIOCOM;
        // Block 66 @555
        // Block 67 @561
        *t563_0 = 0;
        // Block 68 @566
        SC_ggi(109);
        *t573_0 = 109;
        // Block 69 @582
        *t584_0 = 0;
        // Block 70 @587
        *t589_0 = SCM_ENABLEINTERACTION;
        return FALSE;
    } else {
        // Block 37 @344
        *t346_0 = 0;
    }
}

int func_0593(s_SC_OBJ_info *info) {
    // Block 71 @593
    SC_PC_Get();
    SC_P_GetWeapons();
    if (!(t607_0)) {
        // Block 73 @616
        SC_sgi(101, 255);
    } else {
        // Block 72 @609
        SC_sgi(101, t612_0);
    }
    // Block 74 @620
    if (!(t622_0)) {
        // Block 76 @631
        SC_sgi(102, 255);
    } else {
        // Block 75 @624
        SC_sgi(102, t627_0);
    }
    // Block 77 @635
    if (!(t637_0)) {
        // Block 79 @646
        SC_sgi(103, 255);
    } else {
        // Block 78 @639
        SC_sgi(103, t642_0);
    }
    // Block 80 @650
    if (!(t652_0)) {
        // Block 82 @661
        SC_sgi(104, 255);
    } else {
        // Block 81 @654
        SC_sgi(104, t657_0);
    }
    // Block 83 @665
    if (!(t667_0)) {
        // Block 85 @676
        SC_sgi(105, 255);
    } else {
        // Block 84 @669
        SC_sgi(105, t672_0);
    }
    // Block 86 @680
    if (!(t682_0)) {
        // Block 88 @691
        SC_sgi(106, 255);
    } else {
        // Block 87 @684
        SC_sgi(106, t687_0);
    }
    // Block 89 @695
    if (!(t697_0)) {
        // Block 91 @706
        SC_sgi(107, 255);
    } else {
        // Block 90 @699
        SC_sgi(107, t702_0);
    }
    // Block 92 @710
    if (!(t712_0)) {
        // Block 94 @721
        SC_sgi(108, 255);
    } else {
        // Block 93 @714
        SC_sgi(108, t717_0);
    }
    // Block 95 @725
    if (!(t727_0)) {
        // Block 97 @736
        SC_sgi(109, 255);
    } else {
        // Block 96 @729
        SC_sgi(109, t732_0);
    }
    // Block 98 @740
    if (!(t742_0)) {
        // Block 100 @751
        SC_sgi(110, 255);
    } else {
        // Block 99 @744
        SC_sgi(110, t747_0);
    }
    // Block 101 @755
    return t747_0;
}

int func_0756(s_SC_OBJ_info *info) {
    // Block 102 @756
    SC_PC_Get();
    SC_P_ReadHealthFromGlobalVar();
    return FALSE;
}

int func_0764(s_SC_OBJ_info *info) {
    // Block 103 @764
    SC_PC_Get();
    SC_P_WriteHealthToGlobalVar();
    return FALSE;
}

int func_0772(s_SC_OBJ_info *info) {
    // Block 104 @772
    SC_PC_Get();
    SC_P_ReadAmmoFromGlobalVar();
    SC_ggi(90);
    if (!(90)) {
        // Block 106 @800
        SC_ggi(91);
        // Block 107 @807
        SC_PC_Get();
        SC_ggi(91);
        SC_P_SetAmmoInWeap(90, 1, 91);
        // Block 108 @820
        return FALSE;
    } else {
        // Block 105 @787
        SC_PC_Get();
        SC_ggi(90);
        SC_P_SetAmmoInWeap(89, SCM_RUN, 90);
    }
}

int func_0821(s_SC_OBJ_info *info) {
    // Block 109 @821
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

int func_0856(s_SC_OBJ_info *info) {
    // Block 110 @856
    SC_PC_GetIntel(&local_0);
    local_2 = 0;
    // Block 111 @865
    if (!((j < SCM_DISABLE))) {
        // Block 113 @889
        return j;
    } else {
        // Block 111 @865
        // Block 112 @869
        SC_sgi((SCM_CAREFULLASSAULT + j), t877_0);
        local_2 = (j + 1);
    }
    // Block 114 @890
    local_2 = 0;
    // Block 115 @896
    if (!((j < SCM_DISABLE))) {
        // Block 117 @924
        SC_PC_SetIntel(&local_0);
        return &local_0;
    } else {
        // Block 115 @896
        // Block 116 @900
        SC_ggi((SCM_CAREFULLASSAULT + j));
        (&local_0 + (j * SCM_BOOBYTRAPFOUND)) = (SCM_CAREFULLASSAULT + j);
        local_2 = (j + 1);
    }
    // Block 118 @928
    SC_MissionCompleted();
    return FALSE;
    // Block 119 @933
    SC_Osi(&"MISSION COMPLETE", 1);
    SC_MissionDone();
    return FALSE;
    // Block 120 @943
    SC_ShowHelp(&retval, 1, 6.0f);
    return FALSE;
    // Block 121 @949
    local_0[0] = idx;
    local_0[SCM_BOOBYTRAPFOUND] = retval;
    SC_ShowHelp(&local_0, SCM_RUN, 12.0f);
    return 12.0f;
    // Block 122 @968
    local_0[0] = idx;
    local_0[SCM_BOOBYTRAPFOUND] = idx;
    local_0[SCM_SETGPHASE] = retval;
    SC_ShowHelp(&local_0, SCM_WARNABOUTENEMY, 24.0f);
    return 24.0f;
}

int func_0993(s_SC_OBJ_info *info) {
    // Block 123 @993
    SC_ggi(SCM_DISABLE);
    return FALSE;
    // Block 124 @1001
    rand();
    vec2 = (unknown_124_1007_1 % SCM_DISARMTRAP);
    SC_ggi(SGI_CURRENTMISSION);
    if (!((SGI_CURRENTMISSION > SCM_TELEPORT))) {
        // Block 139 @1066
        // Block 140 @1070
        return SCM_HUNTER;
        // Block 141 @1073
        // Block 142 @1077
        return SCM_TIMEDRUN;
        // Block 143 @1080
        // Block 144 @1084
        return SCM_CHECKBODY;
        // Block 145 @1087
        // Block 146 @1091
        return SCM_RUN;
        // Block 147 @1094
        // Block 148 @1098
        return SCM_EXPLODETRAP;
        // Block 149 @1101
        // Block 150 @1105
        return SCM_CREATE;
        // Block 151 @1108
        return SCM_RETREAT;
    } else {
        // Block 125 @1020
        // Block 126 @1024
        return SCM_INITTRAP;
        // Block 127 @1027
        // Block 128 @1031
        return SCM_TIMEDRUN;
        // Block 129 @1034
        // Block 130 @1038
        return SCM_CHECKBODY;
        // Block 131 @1041
        // Block 132 @1045
        return SCM_RUN;
        // Block 133 @1048
        // Block 134 @1052
        return SCM_EXPLODETRAP;
        // Block 135 @1055
        // Block 136 @1059
        return SCM_CREATE;
        // Block 137 @1062
        return SCM_RETREAT;
    }
    // Block 138 @1065
    goto block_152; // @1111
    // Block 152 @1111
    rand();
    vec2 = (unknown_152_1117_1 % SCM_DISARMTRAP);
    if (!((vec2 > SCM_INITTRAP))) {
        // Block 154 @1128
        // Block 155 @1132
        return SCM_INITTRAP;
        // Block 156 @1135
        // Block 157 @1139
        return SCM_RUN;
        // Block 158 @1142
        // Block 159 @1146
        return SCM_TIMEDRUN;
        // Block 160 @1149
        return SCM_RUN;
    } else {
        // Block 153 @1125
        return SCM_CONFIRM;
    }
    // Block 161 @1152
    rand();
    vec2 = (unknown_161_1158_1 % SCM_DISARMTRAP);
    SC_ggi(SGI_CURRENTMISSION);
    goto block_163; // @1174
    switch (vec2) {
    case 1:
        // Block 163 @1174
        // Block 165 @1181
        return SCM_CHECKBODY;
    case 2:
        // Block 168 @1190
        break;
    case 3:
        // Block 170 @1195
        break;
    case 4:
        // Block 172 @1200
        break;
    case 5:
        // Block 174 @1205
        // Block 175 @1209
        return SCM_CHECKBODY;
        // Block 176 @1212
        // Block 177 @1216
        return SCM_CREATE;
        // Block 178 @1219
        return SCM_EXPLODETRAP;
    case 16:
        // Block 181 @1228
        break;
    case 17:
        // Block 183 @1233
        // Block 184 @1237
        return SCM_CHECKBODY;
        // Block 185 @1240
        // Block 186 @1244
        return SCM_EXPLODETRAP;
        // Block 187 @1247
        // Block 188 @1251
        return SCM_CREATE;
        // Block 189 @1254
        return SCM_RETREAT;
    case 6:
        // Block 192 @1263
        // Block 193 @1267
        return SCM_CHECKBODY;
        // Block 194 @1270
        // Block 195 @1274
        return SCM_EXPLODETRAP;
        // Block 196 @1277
        // Block 197 @1281
        return SCM_CREATE;
        // Block 198 @1284
        // Block 199 @1288
        return SCM_RETREAT;
        // Block 200 @1291
        return SCM_STARTWALK;
    case 7:
        // Block 203 @1300
        break;
    case 8:
        // Block 205 @1305
        break;
    case 10:
        // Block 207 @1310
        // Block 208 @1314
        return SCM_CHECKBODY;
        // Block 209 @1317
        // Block 210 @1321
        return SCM_TIMEDRUN;
        // Block 211 @1324
        // Block 212 @1328
        return SCM_CREATE;
        // Block 213 @1331
        // Block 214 @1335
        return SCM_EXPLODETRAP;
        // Block 215 @1338
        return SCM_RUN;
    case 9:
        // Block 218 @1347
        break;
    case 11:
        // Block 220 @1352
        break;
    case 23:
        // Block 222 @1357
        // Block 223 @1361
        return SCM_SETGPHASE;
        // Block 224 @1364
        // Block 225 @1368
        return SCM_ONWAYPOINT;
        // Block 226 @1371
        return SCM_DISABLE;
    case 12:
        // Block 229 @1380
        // Block 230 @1384
        return SCM_RUN;
        // Block 231 @1387
        // Block 232 @1391
        return SCM_TIMEDRUN;
        // Block 233 @1394
        // Block 234 @1398
        return SCM_EXPLODETRAP;
        // Block 235 @1401
        // Block 236 @1405
        return SCM_CREATE;
        // Block 237 @1408
        // Block 238 @1412
        return SCM_CHECKBODY;
        // Block 239 @1415
        return SCM_INITTRAP;
    case 13:
        // Block 242 @1424
        break;
    case 14:
        // Block 244 @1429
        break;
    case 15:
        // Block 246 @1434
        break;
    case 18:
        // Block 248 @1439
        // Block 249 @1443
        return SCM_RUN;
        // Block 250 @1446
        // Block 251 @1450
        return SCM_TIMEDRUN;
        // Block 252 @1453
        // Block 253 @1457
        return SCM_EXPLODETRAP;
        // Block 254 @1460
        // Block 255 @1464
        return SCM_CREATE;
        // Block 256 @1467
        // Block 257 @1471
        return SCM_CHECKBODY;
        // Block 258 @1474
        return SCM_RETREAT;
    case 19:
        // Block 261 @1482
        break;
    case 20:
        // Block 263 @1487
        break;
    case 21:
        // Block 265 @1492
        break;
    case 22:
        // Block 267 @1497
        // Block 268 @1501
        return SCM_RUN;
        // Block 269 @1504
        // Block 270 @1508
        return SCM_TIMEDRUN;
        // Block 271 @1511
        // Block 272 @1515
        return SCM_RETREAT;
        // Block 273 @1518
        return SCM_INITTRAP;
    case 24:
        // Block 276 @1527
        // Block 277 @1531
        return SCM_RUN;
        // Block 278 @1534
        // Block 279 @1538
        return SCM_EXPLODETRAP;
        // Block 280 @1541
        // Block 281 @1545
        return SCM_CREATE;
        // Block 282 @1548
        // Block 283 @1552
        return SCM_RETREAT;
        // Block 284 @1555
        // Block 285 @1559
        return SCM_CHECKBODY;
        // Block 286 @1562
        return SCM_TEAMKIA;
    case 26:
        // Block 289 @1571
        break;
    case 27:
        // Block 291 @1576
        break;
    case 28:
        // Block 293 @1581
        // Block 294 @1585
        return SCM_RUN;
        // Block 295 @1588
        // Block 296 @1592
        return SCM_TIMEDRUN;
        // Block 297 @1595
        // Block 298 @1599
        return SCM_RETREAT;
        // Block 299 @1602
        // Block 300 @1606
        return SCM_CREATE;
        // Block 301 @1609
        return SCM_INITTRAP;
    case 29:
        // Block 304 @1619
        // Block 305 @1623
        return SCM_RUN;
        // Block 306 @1626
        // Block 307 @1630
        return SCM_TIMEDRUN;
        // Block 308 @1633
        // Block 309 @1637
        return SCM_INITTRAP;
        // Block 310 @1640
        // Block 311 @1644
        return SCM_RETREAT;
        // Block 312 @1647
        return SCM_CREATE;
    case 25:
        // Block 315 @1656
        // Block 316 @1660
        return SCM_RUN;
        // Block 317 @1663
        return SCM_CONFIRM;
    case 30:
        // Block 320 @1672
        break;
    case 31:
        // Block 322 @1677
        break;
    case 32:
        // Block 324 @1682
        // Block 325 @1686
        return SCM_RUN;
        // Block 326 @1689
        // Block 327 @1693
        return SCM_TIMEDRUN;
        // Block 328 @1696
        // Block 329 @1700
        return SCM_INITTRAP;
        // Block 330 @1703
        // Block 331 @1707
        return SCM_RETREAT;
        // Block 332 @1710
        // Block 333 @1714
        return SCM_CREATE;
        // Block 334 @1717
        return SCM_CONFIRM;
    default:
        // Block 336 @1721
        return SCM_RUN;
    }
    // Block 164 @1178
    return SCM_EXPLODETRAP;
    // Block 166 @1184
    goto block_168; // @1190
    // Block 179 @1222
    goto block_181; // @1228
    // Block 190 @1257
    goto block_192; // @1263
    // Block 201 @1294
    goto block_203; // @1300
    // Block 216 @1341
    goto block_218; // @1347
    // Block 227 @1374
    goto block_229; // @1380
    // Block 240 @1418
    goto block_242; // @1424
    // Block 259 @1477
    goto block_261; // @1482
    // Block 274 @1521
    goto block_276; // @1527
    // Block 287 @1565
    goto block_289; // @1571
    // Block 302 @1612
    goto block_304; // @1619
    // Block 313 @1650
    goto block_315; // @1656
    // Block 318 @1666
    goto block_320; // @1672
    // Block 335 @1720
    goto block_336; // @1721
    // Block 337 @1725
    rand();
    vec2 = (unknown_337_1731_1 % SCM_DISARMTRAP);
    SC_ggi(SGI_CURRENTMISSION);
    goto block_339; // @1747
    switch (vec2) {
    case 1:
        // Block 339 @1747
        break;
    case 16:
        // Block 341 @1752
        break;
    case 17:
        // Block 343 @1757
        break;
    case 6:
        // Block 345 @1762
        // Block 347 @1769
        // Block 348 @1773
        return &"ini\\players\\poorvc2.ini";
        // Block 349 @1776
        return &"ini\\players\\poorvc3.ini";
    case 2:
        // Block 352 @1785
        break;
    case 3:
        // Block 354 @1790
        break;
    case 4:
        // Block 356 @1795
        break;
    case 5:
        // Block 358 @1800
        break;
    case 7:
        // Block 360 @1805
        break;
    case 8:
        // Block 362 @1810
        break;
    case 10:
        // Block 364 @1815
        // Block 365 @1819
        return &"ini\\players\\vcfighter2.ini";
        // Block 366 @1822
        // Block 367 @1826
        return &"ini\\players\\vcfighter3.ini";
        // Block 368 @1829
        return &"ini\\players\\vcfighter4.ini";
    case 9:
        // Block 371 @1838
        break;
    case 11:
        // Block 373 @1843
        break;
    case 12:
        // Block 375 @1848
        break;
    case 13:
        // Block 377 @1853
        break;
    case 14:
        // Block 379 @1858
        break;
    case 15:
        // Block 381 @1863
        break;
    case 24:
        // Block 383 @1868
        // Block 384 @1872
        return &"ini\\players\\vcfighter3.ini";
        // Block 385 @1875
        // Block 386 @1879
        return &"ini\\players\\vcfighter2.ini";
        // Block 387 @1882
        // Block 388 @1886
        return &"ini\\players\\vcfighter3.ini";
        // Block 389 @1889
        return &"ini\\players\\vcfighter4.ini";
    case 18:
        // Block 392 @1898
        break;
    case 19:
        // Block 394 @1903
        break;
    case 20:
        // Block 396 @1908
        break;
    case 21:
        // Block 398 @1913
        break;
    case 26:
        // Block 400 @1918
        break;
    case 27:
        // Block 402 @1923
        break;
    case 28:
        // Block 404 @1928
        // Block 405 @1932
        return &"ini\\players\\vcuniform1.ini";
        // Block 406 @1935
        // Block 407 @1939
        return &"ini\\players\\vcuniform2.ini";
        // Block 408 @1942
        return &"ini\\players\\vcuniform3.ini";
    case 22:
        // Block 411 @1951
        break;
    case 23:
        // Block 413 @1956
        break;
    case 25:
        // Block 415 @1961
        break;
    case 29:
        // Block 417 @1966
        break;
    case 30:
        // Block 419 @1971
        break;
    case 31:
        // Block 421 @1976
        break;
    case 32:
        // Block 423 @1981
        // Block 424 @1985
        return &"ini\\players\\nvasoldier2.ini";
        // Block 425 @1988
        // Block 426 @1992
        return &"ini\\players\\nvasoldier3.ini";
        // Block 427 @1995
        return &"ini\\players\\nvaofficer.ini";
    default:
        // Block 429 @1999
        return &"ini\\players\\default_aiviet.ini";
    }
    // Block 346 @1766
    return &"ini\\players\\poorvc.ini";
    // Block 350 @1779
    goto block_352; // @1785
    // Block 369 @1832
    goto block_371; // @1838
    // Block 390 @1892
    goto block_392; // @1898
    // Block 409 @1945
    goto block_411; // @1951
    // Block 428 @1998
    goto block_429; // @1999
    // Block 430 @2003
    vec2 = 0;
    // Block 431 @2008
    if (!((vec2 < SCM_SETGPHASE))) {
        // Block 433 @2039
        SC_ggi(SGI_CURRENTMISSION);
        // Block 435 @2051
        t2053_0[0] = SCM_PANICRUN;
        t2060_0[SCM_BOOBYTRAPFOUND] = SCM_SHOOTING;
        // Block 437 @2071
        // Block 439 @2076
        // Block 441 @2081
        // Block 443 @2086
        t2088_0[0] = SCM_RETREAT;
        t2095_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        // Block 445 @2106
        // Block 447 @2111
        t2113_0[0] = SCM_RETREAT;
        t2120_0[SCM_BOOBYTRAPFOUND] = SCM_CHECKBODY;
        t2127_0[SCM_SETGPHASE] = SCM_PANICRUN;
        // Block 449 @2138
        t2140_0[0] = SCM_PANICRUN;
        t2147_0[SCM_BOOBYTRAPFOUND] = SCM_CHECKBODY;
        t2154_0[SCM_SETGPHASE] = SCM_SHOOTING;
        // Block 451 @2165
        // Block 453 @2170
        t2172_0[0] = SCM_RETREAT;
        t2179_0[SCM_BOOBYTRAPFOUND] = SCM_PANICRUN;
        t2186_0[SCM_SETGPHASE] = SCM_STARTWALK;
        // Block 455 @2197
        // Block 457 @2202
        // Block 459 @2207
        t2209_0[0] = SCM_RETREAT;
        t2216_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        // Block 461 @2227
        t2229_0[0] = SCM_RETREAT;
        t2236_0[SCM_BOOBYTRAPFOUND] = SCM_PANICRUN;
        t2243_0[SCM_SETGPHASE] = SCM_STARTWALK;
        t2250_0[SCM_TELEPORT] = SCM_WALKATWP;
        t2257_0[SCM_WALK] = SCM_SHOOTING;
        // Block 463 @2268
        // Block 465 @2273
        // Block 467 @2278
        t2280_0[0] = SCM_RETREAT;
        t2287_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        // Block 469 @2298
        // Block 471 @2303
        // Block 473 @2308
        t2310_0[0] = SCM_GETBACK;
        t2317_0[SCM_BOOBYTRAPFOUND] = SCM_HUNTER;
        t2324_0[SCM_SETGPHASE] = SCM_STARTPATROL;
        // Block 475 @2335
        t2337_0[0] = SCM_GETBACK;
        t2344_0[SCM_BOOBYTRAPFOUND] = SCM_HUNTER;
        t2351_0[SCM_SETGPHASE] = SCM_STARTPATROL;
        t2358_0[SCM_TELEPORT] = SCM_WALK;
        // Block 477 @2369
        // Block 479 @2374
        t2376_0[0] = SCM_WALK;
        t2383_0[SCM_BOOBYTRAPFOUND] = SCM_GETBACK;
        t2390_0[SCM_SETGPHASE] = SCM_MORTARLAND;
        t2397_0[SCM_TELEPORT] = SCM_STARTMORTARFIRE;
        t2404_0[SCM_WALK] = SCM_STARTASSAULT;
        // Block 481 @2415
        t2417_0[0] = SCM_RETREAT;
        t2424_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        // Block 483 @2435
        // Block 485 @2440
        // Block 487 @2445
        t2447_0[0] = SCM_CHECKBODY;
        t2454_0[SCM_BOOBYTRAPFOUND] = SCM_GETBACK;
        t2461_0[SCM_SETGPHASE] = SCM_HUNTER;
        t2468_0[SCM_TELEPORT] = SCM_STARTPATROL;
        // Block 489 @2479
        t2481_0[0] = SCM_STARTPATROL;
        t2488_0[SCM_BOOBYTRAPFOUND] = SCM_WALK;
        t2495_0[SCM_SETGPHASE] = SCM_RUNATWP;
        // Block 491 @2506
        t2508_0[0] = SCM_WALK;
        t2515_0[SCM_BOOBYTRAPFOUND] = SCM_MORTARLAND;
        t2522_0[SCM_SETGPHASE] = SCM_STARTMORTARFIRE;
        t2529_0[SCM_TELEPORT] = SCM_STARTASSAULT;
        // Block 493 @2540
        // Block 495 @2545
        // Block 497 @2550
        t2552_0[0] = SCM_STARTMORTARFIRE;
        t2559_0[SCM_BOOBYTRAPFOUND] = SCM_STARTASSAULT;
        t2566_0[SCM_SETGPHASE] = SCM_WALK;
        t2573_0[SCM_TELEPORT] = SCM_RUNATWP;
        // Block 498 @2580
        t2582_0[0] = SCM_WALK;
        t2589_0[SCM_BOOBYTRAPFOUND] = SCM_GETBACK;
        t2596_0[SCM_SETGPHASE] = SCM_MORTARLAND;
        t2603_0[SCM_TELEPORT] = SCM_STARTMORTARFIRE;
        t2610_0[SCM_WALK] = SCM_STARTASSAULT;
        // Block 500 @2618
        return SGI_CURRENTMISSION;
    } else {
        // Block 431 @2008
        // Block 432 @2012
        (t2014_0 + (vec2 * SCM_BOOBYTRAPFOUND)) = 0;
        (t2023_0 + (vec2 * SCM_BOOBYTRAPFOUND)) = 0;
        vec2++;
    }
    switch (vec2) {
    case 1:
        // Block 435 @2051
        t2053_0[0] = SCM_PANICRUN;
        t2060_0[SCM_BOOBYTRAPFOUND] = SCM_SHOOTING;
        break;
    case 2:
        // Block 437 @2071
        break;
    case 3:
        // Block 439 @2076
        break;
    case 4:
        // Block 441 @2081
        break;
    case 5:
        // Block 443 @2086
        t2088_0[0] = SCM_RETREAT;
        t2095_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        break;
    case 16:
        // Block 445 @2106
        break;
    case 17:
        // Block 447 @2111
        t2113_0[0] = SCM_RETREAT;
        t2120_0[SCM_BOOBYTRAPFOUND] = SCM_CHECKBODY;
        t2127_0[SCM_SETGPHASE] = SCM_PANICRUN;
        break;
    case 6:
        // Block 449 @2138
        t2140_0[0] = SCM_PANICRUN;
        t2147_0[SCM_BOOBYTRAPFOUND] = SCM_CHECKBODY;
        t2154_0[SCM_SETGPHASE] = SCM_SHOOTING;
        break;
    case 7:
        // Block 451 @2165
        break;
    case 8:
        // Block 453 @2170
        t2172_0[0] = SCM_RETREAT;
        t2179_0[SCM_BOOBYTRAPFOUND] = SCM_PANICRUN;
        t2186_0[SCM_SETGPHASE] = SCM_STARTWALK;
        break;
    case 9:
        // Block 455 @2197
        break;
    case 11:
        // Block 457 @2202
        break;
    case 10:
        // Block 459 @2207
        t2209_0[0] = SCM_RETREAT;
        t2216_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        break;
    case 12:
        // Block 461 @2227
        t2229_0[0] = SCM_RETREAT;
        t2236_0[SCM_BOOBYTRAPFOUND] = SCM_PANICRUN;
        t2243_0[SCM_SETGPHASE] = SCM_STARTWALK;
        t2250_0[SCM_TELEPORT] = SCM_WALKATWP;
        t2257_0[SCM_WALK] = SCM_SHOOTING;
        break;
    case 13:
        // Block 463 @2268
        break;
    case 14:
        // Block 465 @2273
        break;
    case 15:
        // Block 467 @2278
        t2280_0[0] = SCM_RETREAT;
        t2287_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        break;
    case 18:
        // Block 469 @2298
        break;
    case 19:
        // Block 471 @2303
        break;
    case 20:
        // Block 473 @2308
        t2310_0[0] = SCM_GETBACK;
        t2317_0[SCM_BOOBYTRAPFOUND] = SCM_HUNTER;
        t2324_0[SCM_SETGPHASE] = SCM_STARTPATROL;
        break;
    case 21:
        // Block 475 @2335
        t2337_0[0] = SCM_GETBACK;
        t2344_0[SCM_BOOBYTRAPFOUND] = SCM_HUNTER;
        t2351_0[SCM_SETGPHASE] = SCM_STARTPATROL;
        t2358_0[SCM_TELEPORT] = SCM_WALK;
        break;
    case 22:
        // Block 477 @2369
        break;
    case 23:
        // Block 479 @2374
        t2376_0[0] = SCM_WALK;
        t2383_0[SCM_BOOBYTRAPFOUND] = SCM_GETBACK;
        t2390_0[SCM_SETGPHASE] = SCM_MORTARLAND;
        t2397_0[SCM_TELEPORT] = SCM_STARTMORTARFIRE;
        t2404_0[SCM_WALK] = SCM_STARTASSAULT;
        break;
    case 24:
        // Block 481 @2415
        t2417_0[0] = SCM_RETREAT;
        t2424_0[SCM_BOOBYTRAPFOUND] = SCM_STARTWALK;
        break;
    case 26:
        // Block 483 @2435
        break;
    case 27:
        // Block 485 @2440
        break;
    case 28:
        // Block 487 @2445
        t2447_0[0] = SCM_CHECKBODY;
        t2454_0[SCM_BOOBYTRAPFOUND] = SCM_GETBACK;
        t2461_0[SCM_SETGPHASE] = SCM_HUNTER;
        t2468_0[SCM_TELEPORT] = SCM_STARTPATROL;
        break;
    case 25:
        // Block 489 @2479
        t2481_0[0] = SCM_STARTPATROL;
        t2488_0[SCM_BOOBYTRAPFOUND] = SCM_WALK;
        t2495_0[SCM_SETGPHASE] = SCM_RUNATWP;
        break;
    case 29:
        // Block 491 @2506
        t2508_0[0] = SCM_WALK;
        t2515_0[SCM_BOOBYTRAPFOUND] = SCM_MORTARLAND;
        t2522_0[SCM_SETGPHASE] = SCM_STARTMORTARFIRE;
        t2529_0[SCM_TELEPORT] = SCM_STARTASSAULT;
        break;
    case 30:
        // Block 493 @2540
        break;
    case 31:
        // Block 495 @2545
        break;
    case 32:
        // Block 497 @2550
        t2552_0[0] = SCM_STARTMORTARFIRE;
        t2559_0[SCM_BOOBYTRAPFOUND] = SCM_STARTASSAULT;
        t2566_0[SCM_SETGPHASE] = SCM_WALK;
        t2573_0[SCM_TELEPORT] = SCM_RUNATWP;
        break;
    default:
        // Block 499 @2617
    }
    // Block 501 @2620
    vec.z = 100.0f;
    SC_ggi(SCM_ENABLE);
    if (!(SCM_ENABLE)) {
        // Block 514 @2726
        SC_PC_GetPos(k);
        SC_2VectorsDist(&vec, &vec);
        vec.z = &vec;
        // Block 515 @2747
        return TRUE;
        // Block 516 @2750
        return FALSE;
    } else {
        // Block 502 @2638
        SC_P_GetPos(k, &vec);
        SC_MP_EnumPlayers(&vec2, &vec.y, 0);
        // Block 503 @2653
        // Block 504 @2654
        return FALSE;
        // Block 505 @2657
        vec.y = 0;
        // Block 506 @2661
        // Block 507 @2665
        // Block 508 @2675
        SC_P_GetPos(t2680_0, &vec);
        SC_2VectorsDist(&vec, &vec);
        vec.z = &vec;
        // Block 509 @2698
        vec.z = vec.z;
        k = t2703_0;
        // Block 510 @2707
        vec.y++;
        // Block 511 @2716
        // Block 512 @2720
        return TRUE;
        // Block 513 @2723
        return FALSE;
    }
    // Block 517 @2753
    SC_GetGroupPlayers(k, k);
    vec2 = k;
    vec2 = 0;
    // Block 518 @2769
    if (!((vec2 < vec2))) {
        // Block 523 @2800
        return TRUE;
    } else {
        // Block 518 @2769
        // Block 519 @2773
        SC_P_GetBySideGroupMember(k, k, vec2);
        SC_P_IsReady(vec2);
        // Block 520 @2787
        // Block 521 @2788
        return FALSE;
        // Block 522 @2791
        vec2++;
    }
    // Block 524 @2803
    SC_GetGroupPlayers(k, k);
    vec2 = k;
    vec2 = 0;
    // Block 525 @2819
    if (!((vec2 < vec2))) {
        // Block 532 @2865
        return TRUE;
    } else {
        // Block 525 @2819
        // Block 526 @2823
        SC_P_GetBySideGroupMember(k, k, vec2);
        SC_P_IsReady(vec2);
        // Block 527 @2837
        // Block 528 @2838
        SC_P_GetBySideGroupMember(k, k, vec2);
        SC_P_GetActive(vec2);
        // Block 529 @2852
        // Block 530 @2853
        return FALSE;
        // Block 531 @2856
        vec2++;
    }
    // Block 533 @2868
    SC_GetGroupPlayers(1, k);
    vec2 = k;
    vec2 = 0;
    // Block 534 @2887
    if (!((vec2 < vec2))) {
        // Block 541 @2945
        return FALSE;
    } else {
        // Block 534 @2887
        // Block 535 @2891
        SC_P_GetBySideGroupMember(1, k, vec2);
        vec2.y = vec2;
        // Block 536 @2904
        SC_P_Ai_GetDanger(vec2.y);
        vec2 = vec2.y;
        // Block 537 @2917
        return TRUE;
        // Block 538 @2920
        SC_P_Ai_GetSureEnemies(vec2.y);
        vec2 = vec2.y;
        // Block 539 @2933
        return TRUE;
        // Block 540 @2936
        vec2++;
    }
    // Block 542 @2948
    vec2 = 1;
    // Block 543 @2957
    if (!((vec2 < SCM_CREATE))) {
        // Block 550 @3015
        return FALSE;
    } else {
        // Block 543 @2957
        // Block 544 @2961
        SC_P_GetBySideGroupMember(0, 0, vec2);
        vec2.y = vec2;
        // Block 545 @2974
        SC_P_Ai_GetDanger(vec2.y);
        vec2 = vec2.y;
        // Block 546 @2987
        return TRUE;
        // Block 547 @2990
        SC_P_Ai_GetSureEnemies(vec2.y);
        vec2 = vec2.y;
        // Block 548 @3003
        return TRUE;
        // Block 549 @3006
        vec2++;
    }
    // Block 551 @3018
    vec2 = 0;
    // Block 552 @3027
    if (!((vec2 < SCM_CREATE))) {
        // Block 557 @3075
        return vec2.y;
    } else {
        // Block 552 @3027
        // Block 553 @3031
        SC_P_GetBySideGroupMember(0, 0, vec2);
        vec2.y = vec2;
        // Block 554 @3044
        SC_P_GetPos(vec2.y, &vec2);
        SC_2VectorsDist(k, &vec2);
        vec2.y = &vec2;
        // Block 555 @3062
        vec2.y = vec2.y;
        // Block 556 @3066
        vec2++;
    }
}

int func_3078(s_SC_OBJ_info *info) {
    // Block 558 @3078
    SC_NOD_Get(0, k);
    ai_props = k;
    if (!((ai_props != 0))) {
        // Block 560 @3097
        return retval;
    } else {
        // Block 559 @3093
        SC_NOD_GetWorldPos(ai_props, retval);
    }
    // Block 561 @3098
    SC_NOD_Get(0, k);
    ai_props = k;
    if (!((ai_props != 0))) {
        // Block 563 @3121
        return FALSE;
    } else {
        // Block 562 @3113
        SC_NOD_GetWorldRotZ(ai_props);
        return ai_props;
    }
    // Block 564 @3124
    SC_P_GetBySideGroupMember(0, 0, 1);
    SC_P_Ai_GetPeaceMode(1);
    if (!((1 == SCM_RUN))) {
        // Block 566 @3151
        SC_P_GetBySideGroupMember(0, 0, 1);
        SC_P_Ai_Stop(1);
        return FALSE;
    } else {
        // Block 565 @3140
        SC_P_GetBySideGroupMember(0, 0, 1);
        SC_P_Ai_SetPeaceMode(1, 0);
    }
    // Block 567 @3162
    SC_DoExplosion(&ai_props, retval);
    return retval;
    // Block 568 @3172
    SC_NOD_Get(0, retval);
    ai_props.watchfulness_zerodist = retval;
    if (!(ai_props.watchfulness_zerodist)) {
        // Block 570 @3189
        SC_message(&"FATAL! Claymore %s not found!!!!!!", 1);
        return TRUE;
    } else {
        // Block 569 @3188
        // Block 571 @3194
        SC_NOD_GetWorldPos(ai_props.watchfulness_zerodist, &ai_props);
        SC_NOD_GetWorldRotZ(ai_props.watchfulness_zerodist);
        ai_props = ai_props.watchfulness_zerodist;
        ai_props = (ai_props - 1.57f);
        ai_props.watchfulness_zerodist = t3214_0;
        cos(ai_props);
        ai_props.watchfulness_zerodist = (t3219_0 - (2.0f * ai_props));
        sin(ai_props);
        ai_props.watchfulness_zerodist.field1 = (t3234_0 + (2.0f * ai_props));
        SC_DoExplosion(&ai_props.watchfulness_zerodist, 1);
        ai_props.watchfulness_zerodist = t3253_0;
        cos(ai_props);
        ai_props.watchfulness_zerodist = (t3258_0 - (4.0f * ai_props));
        sin(ai_props);
        ai_props.watchfulness_zerodist.field1 = (t3273_0 + (4.0f * ai_props));
        SC_DoExplosion(&ai_props.watchfulness_zerodist, SCM_RUN);
        ai_props.watchfulness_zerodist = t3292_0;
        cos(ai_props);
        ai_props.watchfulness_zerodist = (t3297_0 - (8.0f * ai_props));
        sin(ai_props);
        ai_props.watchfulness_zerodist.field1 = (t3312_0 + (8.0f * ai_props));
        SC_DoExplosion(&ai_props.watchfulness_zerodist, SCM_WARNABOUTENEMY);
        SC_DUMMY_Set_DoNotRenHier2(ai_props.watchfulness_zerodist, 1);
        return TRUE;
    }
    // Block 572 @3335
    ai_props.field2 = t3344_0;
    ai_props = 0;
    // Block 573 @3353
    if (!((ai_props < k))) {
        // Block 575 @3396
        return ai_props;
    } else {
        // Block 573 @3353
        // Block 574 @3357
        frnd(retval);
        ai_props = (t3358_0 + retval);
        frnd(retval);
        ai_props.field1 = (t3371_0 + retval);
        SC_DoExplosion(&ai_props, k);
        ai_props++;
    }
    // Block 576 @3397
    SC_GetWp(k, &ai_props);
    SC_DoExplosion(&ai_props, retval);
    return retval;
    // Block 577 @3411
    SC_GetWp(retval, &ai_props);
    SC_CreatePtc(176, &ai_props);
    return &ai_props;
    // Block 578 @3425
    SC_GetWp(retval, &ai_props);
    SC_DoExplosion(&ai_props, SCM_WARNABOUTENEMY);
    SC_SND_PlaySound3D(2965, &ai_props);
    SC_NOD_Get(0, retval);
    SC_CreatePtc_Ext(0, retval, 1000.0f, 0.0f, 1.0f, 1.0f);
    SC_NOD_Get(0, retval);
    SC_CreatePtc_Ext(0, retval, 1000.0f, 0.0f, 1.0f, 1.0f);
    ai_props = 0;
    // Block 579 @3475
    if (!((ai_props < SCM_CREATE))) {
        // Block 581 @3530
        return ai_props;
    } else {
        // Block 579 @3475
        // Block 580 @3479
        SC_GetWp(retval, &ai_props);
        frnd(5.0f);
        ai_props = (t3488_0 + 5.0f);
        frnd(5.0f);
        ai_props.field1 = (t3501_0 + 5.0f);
        SC_CreatePtcVec_Ext(177, &ai_props, 1000.0f, 0.0f, 1.0f, 1.0f);
        ai_props++;
    }
    // Block 582 @3531
    SC_CreatePtc(198, retval);
    SC_SND_PlaySound3D(2965, retval);
    SC_CreatePtcVec_Ext(176, retval, 1000.0f, 0.0f, 1.0f, 1.0f);
    SC_CreatePtcVec_Ext(177, retval, 5.0f, 0.0f, 1.0f, 1.0f);
    return 1.0f;
    // Block 583 @3557
    ai_props.field2 = t3561_0;
    ai_props = 0;
    // Block 584 @3570
    if (!((ai_props < k))) {
        // Block 586 @3622
        SC_CreatePtcVec_Ext(176, k, 1000.0f, 0.0f, 1.0f, 1.0f);
        return 1.0f;
    } else {
        // Block 584 @3570
        // Block 585 @3574
        frnd(retval);
        ai_props = (t3576_0 + retval);
        frnd(retval);
        ai_props.field1 = (t3589_0 + retval);
        SC_CreatePtc(198, &ai_props);
        SC_CreatePtcVec_Ext(177, &ai_props, 5.0f, 0.0f, 1.0f, 1.0f);
        ai_props++;
    }
    // Block 587 @3631
    ai_props.field2 = t3635_0;
    ai_props = 0;
    // Block 588 @3644
    if (!((ai_props < k))) {
        // Block 590 @3688
        SC_CreatePtcVec_Ext(176, k, 1000.0f, 0.0f, 1.0f, 1.0f);
        return 1.0f;
    } else {
        // Block 588 @3644
        // Block 589 @3648
        frnd(retval);
        ai_props = (t3650_0 + retval);
        frnd(retval);
        ai_props.field1 = (t3663_0 + retval);
        SC_CreatePtc(198, &ai_props);
        ai_props++;
    }
    // Block 591 @3697
    ai_props.field2 = t3701_0;
    ai_props = 0;
    // Block 592 @3710
    if (!((ai_props < k))) {
        // Block 594 @3754
        return ai_props;
    } else {
        // Block 592 @3710
        // Block 593 @3714
        frnd(retval);
        ai_props = (t3716_0 + retval);
        frnd(retval);
        ai_props.field1 = (t3729_0 + retval);
        SC_CreatePtc(198, &ai_props);
        ai_props++;
    }
    // Block 595 @3755
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
    // Block 596 @3798
    SC_P_GetDir(k, &ai_props);
    SC_VectorLen(&ai_props);
    ai_props = &ai_props;
    if (!((ai_props > 1.0f))) {
        // Block 598 @3820
        return FALSE;
    } else {
        // Block 597 @3817
        return TRUE;
    }
    // Block 599 @3823
    ai_props = 0;
    // Block 600 @3831
    if (!((ai_props < SCM_CREATE))) {
        // Block 605 @3887
        return ai_props;
    } else {
        // Block 600 @3831
        // Block 601 @3835
        SC_P_GetBySideGroupMember(0, 0, ai_props);
        SC_P_IsReady(ai_props);
        // Block 602 @3849
        SC_P_GetBySideGroupMember(0, 0, ai_props);
        SC_P_GetPos(ai_props, &ai_props);
        SC_2VectorsDist(&ai_props, k);
        ai_props = k;
        // Block 603 @3874
        ai_props = ai_props;
        // Block 604 @3878
        ai_props++;
    }
    // Block 606 @3890
    SC_P_GetPos(k, &ai_props);
    SC_IsNear3D(&ai_props, k, k);
    return k;
    // Block 607 @3905
    SC_PC_GetPos(&ai_props);
    SC_IsNear3D(&ai_props, k, k);
    return k;
    // Block 608 @3923
    if (!(k)) {
        // Block 610 @3927
        return 32;
    } else {
        // Block 609 @3926
        // Block 611 @3928
        SC_ZeroMem(&ai_props, 128);
        SC_P_Ai_GetProps(k, &ai_props);
        ai_props.field13 = k;
        ai_props.field14 = k;
        ai_props.field15 = k;
        ai_props.field16 = retval;
        SC_P_Ai_SetProps(k, &ai_props);
        return &ai_props;
    }
    // Block 612 @3961
    ai_props.hear_distance_mult = 10000.0f;
    ai_props.view_angle.field3 = 1000.0f;
    ai_props.view_angle = t3980_0;
    ai_props = SCM_MORTARLAND;
    SC_GetPls(&ai_props.view_angle, &ai_props, &ai_props);
    ai_props.view_angle = 0;
    ai_props = 0;
    // Block 613 @4001
    if (!((ai_props < ai_props))) {
        // Block 622 @4083
        return ai_props.view_angle;
    } else {
        // Block 613 @4001
        // Block 614 @4005
        SC_P_GetInfo(t4010_0, &ai_props.view_angle_near);
        // Block 615 @4020
        // Block 616 @4024
        // Block 617 @4025
        SC_P_IsReady(t4031_0);
        // Block 618 @4037
        // Block 619 @4038
        SC_P_GetPos(t4043_0, &ai_props.hear_distance_mult);
        SC_2VectorsDist(&ai_props.hear_distance_mult, k);
        ai_props.hear_distance_max = k;
        // Block 620 @4061
        ai_props.hear_distance_mult = ai_props.hear_distance_max;
        ai_props.view_angle = t4070_0;
        // Block 621 @4074
        ai_props++;
    }
}

int func_4086(s_SC_OBJ_info *info) {
    // Block 623 @4086
    SC_P_GetInfo(k, &player_info);
    player_info3 = t4099_0;
    SC_P_GetPos(k, &sphere);
    sphere.field3 = 1000.0f;
    player_info3 = SCM_MORTARLAND;
    SC_GetPls(&sphere, &player_info3.max_hp, &player_info3);
    player_info3 = 0;
    player_info3 = 0;
    // Block 624 @4129
    if (!((player_info3 < player_info3))) {
        // Block 633 @4208
        retval = player_info3;
        return retval;
    } else {
        // Block 624 @4129
        // Block 625 @4133
        SC_P_GetInfo(t4138_0, &player_info);
        // Block 626 @4148
        // Block 627 @4154
        // Block 628 @4155
        SC_P_IsReady(t4161_0);
        // Block 629 @4167
        // Block 630 @4168
        (k + (player_info3 * SCM_BOOBYTRAPFOUND)) = t4173_0;
        player_info3++;
        // Block 631 @4193
        SC_Log(1299473735, SCM_RUN);
        return SCM_RUN;
        // Block 632 @4199
        player_info3++;
    }
    // Block 634 @4213
    player_info3 = SCM_MORTARLAND;
    SC_P_GetInfo(retval, &player_info2);
    if (!((player_info3 < SCM_RUN))) {
        // Block 636 @4249
        // Block 637 @4256
        // Block 638 @4265
        // Block 639 @4273
        SC_Log(622871382, t4277_0, t4280_0, SCM_BOOBYTRAPFOUND);
        return SCM_BOOBYTRAPFOUND;
    } else {
        // Block 635 @4234
        SC_Log(622871382, t4238_0, t4241_0, t4244_0, SCM_TAUNTRUNNER);
        return SCM_TAUNTRUNNER;
    }
    // Block 640 @4285
    SC_P_GetPos(k, &player_info3);
    SC_2VectorsDist(k, &player_info3);
    player_info3 = &player_info3;
    return player_info3;
    // Block 641 @4304
    SC_ZeroMem(&player_info3, SCM_DISARMTRAP);
    local_0[0] = 0;
    local_0[SCM_BOOBYTRAPFOUND] = 0;
    local_0[SCM_SETGPHASE] = 0;
    local_0[SCM_TELEPORT] = 0;
    local_0[SCM_WALK] = 0;
    SC_P_SetSpecAnims(retval, &player_info3);
    return &player_info3;
    // Block 642 @4344
    SC_ZeroMem(&player_info3, SCM_DISARMTRAP);
    local_0[0] = k;
    local_0[SCM_BOOBYTRAPFOUND] = k;
    local_0[SCM_SETGPHASE] = k;
    local_0[SCM_TELEPORT] = k;
    local_0[SCM_WALK] = retval;
    SC_P_SetSpecAnims(param_1, &player_info3);
    return &player_info3;
    // Block 643 @4384
    player_info3 = SCM_MORTARLAND;
    SC_GetPls(k, &player_info3.max_hp, &player_info3);
    if (!(player_info3)) {
        // Block 645 @4401
        return 36;
    } else {
        // Block 644 @4400
        // Block 646 @4402
        player_info3 = 0;
        // Block 647 @4406
        // Block 648 @4410
        SC_P_DoHit(t4415_0, 0, (retval / 7.0f));
        SC_P_DoHit(t4427_0, 1, (retval / 7.0f));
        SC_P_DoHit(t4439_0, SCM_RUN, (retval / 7.0f));
        SC_P_DoHit(t4451_0, SCM_WARNABOUTENEMY, (retval / 7.0f));
        SC_P_DoHit(t4463_0, SCM_BOOBYTRAPFOUND, (retval / 7.0f));
        SC_P_DoHit(t4475_0, SCM_TAUNTRUNNER, (retval / 7.0f));
        SC_P_DoHit(t4487_0, SCM_CREATE, (retval / 7.0f));
        player_info3++;
        // Block 649 @4503
        return player_info3;
    }
    // Block 650 @4504
    SC_P_GetPos(k, &player_info3);
    player_info3.field2 = (t4511_0 + 1.0f);
    player_info3.field3 = 1.0f;
    SC_SphereIsVisible(&player_info3);
    return &player_info3;
    // Block 651 @4531
    SC_P_GetInfo(k, &player_info3);
    return t4538_0;
    // Block 652 @4541
    SC_P_GetInfo(k, &player_info3);
    return t4548_0;
    // Block 653 @4551
    SC_P_GetInfo(k, &player_info3);
    return t4558_0;
    // Block 654 @4561
    retval = SCM_SETGPHASE;
    return FALSE;
}

int func_4670(s_SC_OBJ_info *info) {
    // Block 655 @4670
    retval = SCM_RUN;
    return FALSE;
    // Block 656 @4701
    retval = SCM_SETGPHASE;
    return FALSE;
    // Block 657 @4810
    retval = SCM_WARNABOUTENEMY;
    return FALSE;
    // Block 658 @4854
    retval = SCM_SETGPHASE;
    return FALSE;
    // Block 659 @4963
    retval = SCM_TAUNTRUNNER;
    return FALSE;
    // Block 660 @5033
    retval = SCM_CREATE;
    return FALSE;
    // Block 661 @5116
    retval = SCM_WARNABOUTENEMY;
    return FALSE;
    // Block 662 @5160
    retval = SCM_SETGPHASE;
    return FALSE;
    // Block 663 @5269
    retval = SCM_RUN;
    return FALSE;
    // Block 664 @5300
    retval = SCM_HEARDSOMETHING;
    return FALSE;
    // Block 665 @5396
    retval = SCM_WARNABOUTENEMY;
    return FALSE;
    // Block 666 @5440
    retval = SCM_CREATE;
    return FALSE;
    // Block 667 @5523
    retval = SCM_SETGPHASE;
    return FALSE;
    // Block 668 @5632
    retval = SCM_SETGPHASE;
    return FALSE;
    // Block 669 @5741
    retval = SCM_WARNABOUTENEMY;
    return FALSE;
    // Block 670 @5785
    retval = SCM_SETGPHASE;
    return FALSE;
    // Block 671 @5894
    retval = SCM_SETGPHASE;
    return FALSE;
    // Block 672 @6003
    retval = SCM_BOOBYTRAPFOUND;
    return FALSE;
    // Block 673 @6060
    retval = SCM_BOOBYTRAPFOUND;
    return FALSE;
    // Block 674 @6117
    retval = SCM_HEARDSOMETHING;
    return FALSE;
    // Block 675 @6213
    retval = SCM_SETGPHASE;
    return FALSE;
    // Block 676 @6322
    retval = SCM_BOOBYTRAPFOUND;
    return FALSE;
    // Block 677 @6379
    retval = SCM_HEARDSOMETHING;
    return FALSE;
    // Block 678 @6475
    retval = SCM_SETGPHASE;
    return FALSE;
    // Block 679 @6584
    retval = SCM_TAUNTRUNNER;
    return FALSE;
    // Block 680 @6654
    retval = SCM_HEARDSOMETHING;
    return FALSE;
    // Block 681 @6750
    retval = SCM_HEARDSOMETHING;
    return FALSE;
    // Block 682 @6846
    retval = SCM_BOOBYTRAPFOUND;
    return FALSE;
    // Block 683 @6903
    retval = SCM_HEARDSOMETHING;
    return FALSE;
    // Block 684 @6999
    retval = SCM_SETGPHASE;
    return FALSE;
}

int func_7108(s_SC_OBJ_info *info) {
    // Block 685 @7108
    return FALSE;
}

int ScriptMain(s_SC_OBJ_info *info) {
    // Block 686 @7113
    if (!((0 == 0))) {
        // Block 697 @7275
        SC_P_IsReady(info->new_hp_obtained);
        // Block 698 @7289
        // Block 699 @7290
        return TRUE;
        // Block 700 @7298
        // Block 702 @7305
        SC_P_SetSpeachDist(info->new_hp_obtained, 20.0f);
        SC_PC_EnablePronePosition(0);
        SC_PC_EnableFlashLight(1);
        // Block 704 @7329
        // Block 705 @7330
        return TRUE;
    } else {
        // Block 687 @7122
        SC_ZeroMem(&pinfo, 156);
        SC_ZeroMem(&pinfo.flags, SCM_INFO);
        pinfo = 1;
        pinfo.field1 = 0;
        pinfo.field2 = 0;
        pinfo.field3 = 0;
        // Block 688 @7154
        // Block 689 @7155
        pinfo.field6 = &"ini\\players\\easy_camo.ini";
        // Block 690 @7161
        pinfo.field6 = &"ini\\players\\default_camo.ini";
        // Block 691 @7166
        pinfo.field4 = 2500;
        pinfo.field7 = info->hit_by;
        pinfo.field19 = 0;
        pinfo.field18 = SCM_THROWSMOKE;
        SC_ggi(102);
        pinfo.field11 = 102;
        // Block 692 @7205
        // Block 693 @7206
        pinfo.field11 = SCM_BATTLERUN;
        // Block 694 @7211
        // Block 695 @7217
        pinfo.field11 = 0;
        // Block 696 @7222
        pinfo.field12 = 0;
        pinfo.field13 = 140;
        pinfo.field14 = 0;
        pinfo.field16 = SCM_OBJECTUSED;
        pinfo.field21 = pinfo.weap_slot7;
        pinfo.field22 = &pinfo.flags;
        pinfo.field9 = SCM_BOOBYTRAPFOUND;
        SC_P_Create(&pinfo);
        pinfo = t7268_0;
    }
    switch (pinfo.weap_slot7) {
    case 1:
        // Block 702 @7305
        SC_P_SetSpeachDist(info->new_hp_obtained, 20.0f);
        SC_PC_EnablePronePosition(0);
        SC_PC_EnableFlashLight(1);
        break;
    case 2:
        // Block 704 @7329
        break;
    default:
        // Block 705 @7330
        return TRUE;
    }
}

