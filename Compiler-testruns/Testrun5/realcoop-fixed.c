// VC Script Decompiler - Python (Structured)
// enter_ip: 0x-e70

#include <inc/sc_global.h>
#include <inc/sc_def.h>

// Data segment
char str_167[] = "EndRule unsopported: %d";
char str_185[] = "US-%01d-%01d-%01d";
char str_191[] = "VC-%01d-%01d-%01d";
char str_287[] = "SPOUSTEC2";
char str_295[] = "VC-%01d-%01d-%01d";
char str_307[] = "VC-%01d-%01d-%01d";
char str_319[] = "VC-%01d-%01d-%01d";
char str_331[] = "VC-%01d-%01d-%01d";
char str_343[] = "VC-%01d-%01d-%01d";
char str_355[] = "VC-%01d-%01d-%01d";
char str_381[] = "SNIPERPOS";
char str_389[] = "VC-%01d-%01d-%01d";
char str_401[] = "VC-%01d-%01d-%01d";
char str_413[] = "VC-%01d-%01d-%01d";
char str_425[] = "VC-%01d-%01d-%01d";
char str_445[] = "SPOUSTEC4";
char str_453[] = "VC-%01d-%01d-%01d";
char str_465[] = "VC-%01d-%01d-%01d";
char str_477[] = "VC-%01d-%01d-%01d";
char str_489[] = "VC-%01d-%01d-%01d";
char str_509[] = "MAPA";
char str_516[] = "VC-%01d-%01d-%01d";
char str_528[] = "VC-%01d-%01d-%01d";
char str_540[] = "VC-%01d-%01d-%01d";
char str_552[] = "VC-%01d-%01d-%01d";
char str_650[] = "HideMap";
char str_652[] = "MAPA";
char str_661[] = "burnsphere";
char str_679[] = "burnsphere";
char str_694[] = "SPOUSTEC0";
char str_708[] = "ATTACK1";
char str_710[] = "ATTACK2";
char str_712[] = "ATTACK3";
char str_714[] = "ATTACK4";
char str_716[] = "SPOUSTEC1";
char str_754[] = "SPOUSTEC2";
char str_757[] = "SPOUSTEC2A";
char str_776[] = "SPOUSTEC3";
char str_791[] = "SPOUSTEC4";
char str_806[] = "SPOUSTEC5";
char str_815[] = " APILOT1";
char str_818[] = "PILOT2";
char str_831[] = "SPOUSTEC6";
char str_845[] = "SPOUSTEC7";
char str_893[] = "coop script wrong side: %d";
char str_935[] = "Enum, v[0]: %d   v[1]: %d  alldeath: %d";
char str_949[] = "NoEnum";
char str_969[] = "Set GPHASE_FAILED";
char str_990[] = "Set GPHASE_GAME";
char str_1001[] = "Set GPHASE_DONE";
char str_1038[] = "Set GPHASE_DONE";
char str_1082[] = "Set GPHASE_DONE";
char str_1134[] = "Set GPHASE_DONE";
char str_1186[] = "Set GPHASE_DONE";
char str_1238[] = "Set GPHASE_DONE";
char str_1290[] = "Set GPHASE_DONE";
char str_1342[] = "Set GPHASE_DONE";
char str_1394[] = "SC_MP_RestartMission";
char str_1407[] = "SC_MP_RestartMission";
char str_1521[] = "USSpawn_coop_%d";
char str_1543[] = "ATG UsBomb respawns us: %d";
char str_1554[] = "no US recover place defined!";
char str_1567[] = "VCSpawn_coop_%d";
char str_1589[] = "ATG UsBomb respawns vc: %d";
char str_1600[] = "no VC recover place defined!";

void func_28(void) {
  int local_1;
  int local_11;
  int local_18;
  int local_19;
  int local_259;
  int local_269;
  int local_3;
  int local_4;

  SC_P_IsReady(stack_tmp_0 + 1 + 147);  // 32
  while (1) {
    func_108();  // 36
    data[1] = 148;  // 41
    SC_P_IsReady(local_259);  // 47
    func_99();  // 48
    *SC_P_IsReady(local_259) = 149;  // 52
    SC_MP_EndRule_SetTimeLeft();  // 58
    *SC_MP_EndRule_SetTimeLeft() = 152;  // 62
    SC_MP_EndRule_SetTimeLeft();  // 68
    *SC_MP_EndRule_SetTimeLeft() = OUTPOSTCRATER5;  // 72
    SC_MP_EndRule_SetTimeLeft();  // 78
    *SC_MP_EndRule_SetTimeLeft() = OUTPOSTCRATER8;  // 82
    SC_MP_EndRule_SetTimeLeft();  // 88
    *SC_MP_EndRule_SetTimeLeft() = OUTPOSTCRATER11;  // 92
    SC_MP_EndRule_SetTimeLeft();  // 98
    SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 163.0);  // 105
    SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 163.0));  // 106
    if (SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 163.0))) break;  // 107
  }
    func_146();  // 115
  func_124();  // 117
  SC_P_IsReady(259.0 + data[127]);  // 123
  SC_P_ChangeWeapon();  // 127
  SRS(0, 0);  // 131
  func_137();  // 132
  if (local_3 + 1) {
    SC_P_IsReady(166u);  // 147
  }
  if (SC_P_ChangeWeapon()) {
    SC_P_IsReady(166u);  // 147
  }
    SC_P_IsReady(166u);  // 147
  SC_P_ChangeWeapon();  // 189
  SC_P_IsReady(local_1 + SC_P_ChangeWeapon());  // 192
  func_200();  // 196
  SC_P_ChangeWeapon();  // 203
  func_226();  // 212
  if (SC_P_IsReady(SC_message())) {
    SC_P_ChangeWeapon();  // 244
    SC_P_IsReady(SC_P_ChangeWeapon());  // 245
  }
  SC_message();  // 236
  SC_P_IsReady(SC_message());  // 237
  SC_MP_EndRule_SetTimeLeft();  // 253
  SC_P_ChangeWeapon();  // 256
  SC_P_IsReady(local_1);  // 264
  SC_P_IsReady((197 != &data[1]) + SC_P_IsReady(local_1));  // 267
  *SGI_CURRENTMISSION = SGF_MISSIONTIMER;  // 274
  SC_MP_LoadNextMap();  // 277
  SC_P_IsReady(local_1);  // 283
  SC_P_IsReady((202 != &data[1]) + SC_P_IsReady(local_1));  // 286
  *205 = 206;  // 293
  SC_MP_LoadNextMap();  // 296
  SC_P_IsReady(local_1);  // 302
  SC_P_IsReady((207 != &data[1]) + SC_P_IsReady(local_1));  // 305
  *210 = 211;  // 312
  SC_MP_LoadNextMap();  // 315
  SC_P_IsReady(local_1);  // 321
  SC_P_IsReady((212 != &data[1]) + SC_P_IsReady(local_1));  // 324
  *215 = 216;  // 331
  SC_MP_LoadNextMap();  // 334
  SC_P_IsReady(local_1);  // 340
  SC_P_IsReady((217 != &data[1]) + SC_P_IsReady(local_1));  // 343
  *220 = 221;  // 350
  SC_MP_LoadNextMap();  // 353
  SC_P_IsReady(local_1);  // 359
  SC_P_IsReady((222 != &data[1]) + SC_P_IsReady(local_1));  // 362
  *225 = 226;  // 369
  SC_MP_LoadNextMap();  // 372
  SC_P_IsReady(local_1);  // 378
  SC_P_IsReady((227 != &data[1]) + SC_P_IsReady(local_1));  // 381
  *230 = 231;  // 388
  SC_MP_LoadNextMap();  // 391
  SC_P_IsReady(local_1);  // 397
  SC_P_IsReady((232 != &data[1]) + SC_P_IsReady(local_1));  // 400
  *235 = 236;  // 407
  SC_MP_LoadNextMap();  // 410
  SC_P_IsReady(local_1);  // 416
  SC_P_IsReady((237 != &data[1]) + SC_P_IsReady(local_1));  // 419
  *240 = 241;  // 426
  SC_MP_LoadNextMap();  // 429
  SC_P_IsReady(local_1);  // 435
  SC_P_IsReady((242 != &data[1]) + SC_P_IsReady(local_1));  // 438
  *245 = 246;  // 445
  SC_MP_LoadNextMap();  // 448
  SC_P_IsReady(local_1);  // 454
  SC_P_IsReady((247 != &data[1]) + SC_P_IsReady(local_1));  // 457
  *250 = 251;  // 464
  SC_MP_LoadNextMap();  // 467
  SC_P_IsReady(local_1);  // 473
  SC_P_IsReady((252 != &data[1]) + SC_P_IsReady(local_1));  // 476
  *PLAYER_FREESLOT = SC_PL_AI_SIT_IFL_S1G0;  // 483
  SC_MP_LoadNextMap();  // 486
  SC_P_IsReady(local_1);  // 492
  SC_P_IsReady((257 != &data[1]) + SC_P_IsReady(local_1));  // 495
  *260 = 261;  // 502
  SC_MP_LoadNextMap();  // 505
  SC_P_IsReady(local_1);  // 511
  SC_P_IsReady((262 != &data[1]) + SC_P_IsReady(local_1));  // 514
  *265 = 266;  // 521
  SC_MP_LoadNextMap();  // 524
  SC_P_IsReady(local_1);  // 530
  SC_P_IsReady((267 != &data[1]) + SC_P_IsReady(local_1));  // 533
  *270 = 271;  // 540
  SC_MP_LoadNextMap();  // 543
  SC_P_IsReady(local_1);  // 549
  SC_P_IsReady((272 != &data[1]) + SC_P_IsReady(local_1));  // 552
  *275 = 276;  // 559
  SC_MP_LoadNextMap();  // 562
  SC_P_IsReady(local_1);  // 568
  SC_P_IsReady((277 != &data[1]) + SC_P_IsReady(local_1));  // 571
  *280 = 281;  // 578
  SC_MP_LoadNextMap();  // 581
  SC_P_IsReady(local_1);  // 587
  SC_P_IsReady((282 != &data[1]) + SC_P_IsReady(local_1));  // 590
  *285 = 286;  // 597
  SC_MP_LoadNextMap();  // 600
  SC_P_ChangeWeapon();  // 616
  SC_P_IsReady(SC_P_ChangeWeapon());  // 617
  SC_P_ChangeWeapon();  // 624
  SC_P_IsReady(SC_P_ChangeWeapon());  // 625
  SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 291);  // 629
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 291) + 292);  // 633
  SC_P_IsReady(local_18);  // 639
  *SC_P_IsReady(local_18) = 294;  // 642
  SC_P_IsReady(&data[1] + (293 != &data[1]) - 1.0);  // 646
  SC_message();  // 657
  SC_P_IsReady(SC_message());  // 658
  SC_P_ChangeWeapon();  // 665
  SC_P_IsReady(SC_P_ChangeWeapon());  // 666
  SC_MP_EndRule_SetTimeLeft();  // 675
  SC_MP_EndRule_SetTimeLeft();  // 681
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 682
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 303);  // 686
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 303) + 304);  // 690
  SC_P_IsReady(local_18);  // 696
  *SC_P_IsReady(local_18) = 306;  // 699
  SC_P_IsReady(&data[1] + (305 != &data[1]) - 1.0);  // 703
  SC_message();  // 714
  SC_P_IsReady(SC_message());  // 715
  SC_P_ChangeWeapon();  // 722
  SC_P_IsReady(SC_P_ChangeWeapon());  // 723
  SC_MP_EndRule_SetTimeLeft();  // 732
  SC_MP_EndRule_SetTimeLeft();  // 738
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 739
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 315);  // 743
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 315) + 316);  // 747
  SC_P_IsReady(local_18);  // 753
  *SC_P_IsReady(local_18) = 318;  // 756
  SC_P_IsReady(&data[1] + (317 != &data[1]) - 1.0);  // 760
  SC_message();  // 771
  SC_P_IsReady(SC_message());  // 772
  SC_P_ChangeWeapon();  // 779
  SC_P_IsReady(SC_P_ChangeWeapon());  // 780
  SC_MP_EndRule_SetTimeLeft();  // 789
  SC_MP_EndRule_SetTimeLeft();  // 795
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 796
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 327);  // 800
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 327) + 328);  // 804
  SC_P_IsReady(local_18);  // 810
  *SC_P_IsReady(local_18) = 330;  // 813
  SC_P_IsReady(&data[1] + (329 != &data[1]) - 1.0);  // 817
  SC_message();  // 828
  SC_P_IsReady(SC_message());  // 829
  SC_P_ChangeWeapon();  // 836
  SC_P_IsReady(SC_P_ChangeWeapon());  // 837
  SC_MP_EndRule_SetTimeLeft();  // 846
  SC_MP_EndRule_SetTimeLeft();  // 852
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 853
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 339);  // 857
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 339) + 340);  // 861
  SC_P_IsReady(local_18);  // 867
  *SC_P_IsReady(local_18) = 342;  // 870
  SC_P_IsReady(&data[1] + (341 != &data[1]) - 1.0);  // 874
  SC_message();  // 885
  SC_P_IsReady(SC_message());  // 886
  SC_P_ChangeWeapon();  // 893
  SC_P_IsReady(SC_P_ChangeWeapon());  // 894
  SC_MP_EndRule_SetTimeLeft();  // 903
  SC_MP_EndRule_SetTimeLeft();  // 909
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 910
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 351);  // 914
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 351) + 352);  // 918
  SC_P_IsReady(local_18);  // 924
  *SC_P_IsReady(local_18) = 354;  // 927
  SC_P_IsReady(&data[1] + (353 != &data[1]) - 1.0);  // 931
  SC_message();  // 942
  SC_P_IsReady(SC_message());  // 943
  SC_P_ChangeWeapon();  // 950
  SC_P_IsReady(SC_P_ChangeWeapon());  // 951
  SC_MP_EndRule_SetTimeLeft();  // 960
  SC_MP_EndRule_SetTimeLeft();  // 966
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 967
  SC_MP_EndRule_SetTimeLeft();  // 975
  SC_P_ChangeWeapon();  // 978
  SC_MP_EndRule_SetTimeLeft();  // 986
  SC_P_ChangeWeapon();  // 989
  SC_MP_EndRule_SetTimeLeft();  // 997
  SC_P_ChangeWeapon();  // 1000
  SC_MP_EndRule_SetTimeLeft();  // 1008
  SC_P_ChangeWeapon();  // 1011
  SC_MP_EndRule_SetTimeLeft();  // 1019
  SC_P_ChangeWeapon();  // 1022
  SC_MP_EndRule_SetTimeLeft();  // 1030
  SC_P_ChangeWeapon();  // 1033
  SC_P_ChangeWeapon();  // 1049
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1050
  SC_P_ChangeWeapon();  // 1057
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1058
  SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 385);  // 1062
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 385) + 386);  // 1066
  SC_P_IsReady(local_18);  // 1072
  *SC_P_IsReady(local_18) = 388;  // 1075
  SC_P_IsReady(&data[1] + (387 != &data[1]) - 1.0);  // 1079
  SC_message();  // 1090
  SC_P_IsReady(SC_message());  // 1091
  SC_P_ChangeWeapon();  // 1098
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1099
  SC_MP_EndRule_SetTimeLeft();  // 1108
  SC_MP_EndRule_SetTimeLeft();  // 1114
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1115
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 397);  // 1119
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 397) + 398);  // 1123
  SC_P_IsReady(local_18);  // 1129
  *SC_P_IsReady(local_18) = 400;  // 1132
  SC_P_IsReady(&data[1] + (399 != &data[1]) - 1.0);  // 1136
  SC_message();  // 1147
  SC_P_IsReady(SC_message());  // 1148
  SC_P_ChangeWeapon();  // 1155
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1156
  SC_MP_EndRule_SetTimeLeft();  // 1165
  SC_MP_EndRule_SetTimeLeft();  // 1171
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1172
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 409);  // 1176
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 409) + 410);  // 1180
  SC_P_IsReady(local_18);  // 1186
  *SC_P_IsReady(local_18) = 412;  // 1189
  SC_P_IsReady(&data[1] + (411 != &data[1]) - 1.0);  // 1193
  SC_message();  // 1204
  SC_P_IsReady(SC_message());  // 1205
  SC_P_ChangeWeapon();  // 1212
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1213
  SC_MP_EndRule_SetTimeLeft();  // 1222
  SC_MP_EndRule_SetTimeLeft();  // 1228
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1229
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 421);  // 1233
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 421) + 422);  // 1237
  SC_P_IsReady(local_18);  // 1243
  *SC_P_IsReady(local_18) = 424;  // 1246
  SC_P_IsReady(&data[1] + (423 != &data[1]) - 1.0);  // 1250
  SC_message();  // 1261
  SC_P_IsReady(SC_message());  // 1262
  SC_P_ChangeWeapon();  // 1269
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1270
  SC_MP_EndRule_SetTimeLeft();  // 1279
  SC_MP_EndRule_SetTimeLeft();  // 1285
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1286
  SC_MP_EndRule_SetTimeLeft();  // 1294
  SC_P_ChangeWeapon();  // 1297
  SC_MP_EndRule_SetTimeLeft();  // 1305
  SC_P_ChangeWeapon();  // 1308
  SC_MP_EndRule_SetTimeLeft();  // 1316
  SC_P_ChangeWeapon();  // 1319
  SC_MP_EndRule_SetTimeLeft();  // 1327
  SC_P_ChangeWeapon();  // 1330
  SC_P_ChangeWeapon();  // 1346
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1347
  SC_P_ChangeWeapon();  // 1354
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1355
  SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 449);  // 1359
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 449) + 450);  // 1363
  SC_P_IsReady(local_18);  // 1369
  *SC_P_IsReady(local_18) = 452;  // 1372
  SC_P_IsReady(&data[1] + (451 != &data[1]) - 1.0);  // 1376
  SC_message();  // 1387
  SC_P_IsReady(SC_message());  // 1388
  SC_P_ChangeWeapon();  // 1395
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1396
  SC_MP_EndRule_SetTimeLeft();  // 1405
  SC_MP_EndRule_SetTimeLeft();  // 1411
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1412
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 461);  // 1416
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 461) + 462);  // 1420
  SC_P_IsReady(local_18);  // 1426
  *SC_P_IsReady(local_18) = 464;  // 1429
  SC_P_IsReady(&data[1] + (463 != &data[1]) - 1.0);  // 1433
  SC_message();  // 1444
  SC_P_IsReady(SC_message());  // 1445
  SC_P_ChangeWeapon();  // 1452
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1453
  SC_MP_EndRule_SetTimeLeft();  // 1462
  SC_MP_EndRule_SetTimeLeft();  // 1468
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1469
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 473);  // 1473
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 473) + 474);  // 1477
  SC_P_IsReady(local_18);  // 1483
  *SC_P_IsReady(local_18) = 476;  // 1486
  SC_P_IsReady(&data[1] + (475 != &data[1]) - 1.0);  // 1490
  SC_message();  // 1501
  SC_P_IsReady(SC_message());  // 1502
  SC_P_ChangeWeapon();  // 1509
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1510
  SC_MP_EndRule_SetTimeLeft();  // 1519
  SC_MP_EndRule_SetTimeLeft();  // 1525
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1526
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 485);  // 1530
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 485) + 486);  // 1534
  SC_P_IsReady(local_18);  // 1540
  *SC_P_IsReady(local_18) = 488;  // 1543
  SC_P_IsReady(&data[1] + (487 != &data[1]) - 1.0);  // 1547
  SC_message();  // 1558
  SC_P_IsReady(SC_message());  // 1559
  SC_P_ChangeWeapon();  // 1566
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1567
  SC_MP_EndRule_SetTimeLeft();  // 1576
  SC_MP_EndRule_SetTimeLeft();  // 1582
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1583
  SC_MP_EndRule_SetTimeLeft();  // 1591
  SC_P_ChangeWeapon();  // 1594
  SC_MP_EndRule_SetTimeLeft();  // 1602
  SC_P_ChangeWeapon();  // 1605
  SC_MP_EndRule_SetTimeLeft();  // 1613
  SC_P_ChangeWeapon();  // 1616
  SC_MP_EndRule_SetTimeLeft();  // 1624
  SC_P_ChangeWeapon();  // 1627
  SC_P_ChangeWeapon();  // 1643
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1644
  SC_P_ChangeWeapon();  // 1651
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1652
  SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + SC_PL_AI_SIT_IFL_S1G1);  // 1656
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + SC_PL_AI_SIT_IFL_S1G1) + 513);  // 1660
  SC_P_IsReady(local_18);  // 1666
  *SC_P_IsReady(local_18) = 515;  // 1669
  SC_P_IsReady(&data[1] + (514 != &data[1]) - 1.0);  // 1673
  SC_message();  // 1684
  SC_P_IsReady(SC_message());  // 1685
  SC_P_ChangeWeapon();  // 1692
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1693
  SC_MP_EndRule_SetTimeLeft();  // 1702
  SC_MP_EndRule_SetTimeLeft();  // 1708
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1709
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 524);  // 1713
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 524) + 525);  // 1717
  SC_P_IsReady(local_18);  // 1723
  *SC_P_IsReady(local_18) = 527;  // 1726
  SC_P_IsReady(&data[1] + (526 != &data[1]) - 1.0);  // 1730
  SC_message();  // 1741
  SC_P_IsReady(SC_message());  // 1742
  SC_P_ChangeWeapon();  // 1749
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1750
  SC_MP_EndRule_SetTimeLeft();  // 1759
  SC_MP_EndRule_SetTimeLeft();  // 1765
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1766
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 536);  // 1770
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 536) + 537);  // 1774
  SC_P_IsReady(local_18);  // 1780
  *SC_P_IsReady(local_18) = 539;  // 1783
  SC_P_IsReady(&data[1] + (538 != &data[1]) - 1.0);  // 1787
  SC_message();  // 1798
  SC_P_IsReady(SC_message());  // 1799
  SC_P_ChangeWeapon();  // 1806
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1807
  SC_MP_EndRule_SetTimeLeft();  // 1816
  SC_MP_EndRule_SetTimeLeft();  // 1822
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1823
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 548);  // 1827
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 548) + 549);  // 1831
  SC_P_IsReady(local_18);  // 1837
  *SC_P_IsReady(local_18) = 551;  // 1840
  SC_P_IsReady(&data[1] + (550 != &data[1]) - 1.0);  // 1844
  SC_message();  // 1855
  SC_P_IsReady(SC_message());  // 1856
  SC_P_ChangeWeapon();  // 1863
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1864
  SC_MP_EndRule_SetTimeLeft();  // 1873
  SC_MP_EndRule_SetTimeLeft();  // 1879
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1880
  SC_MP_EndRule_SetTimeLeft();  // 1888
  SC_P_ChangeWeapon();  // 1891
  SC_MP_EndRule_SetTimeLeft();  // 1899
  SC_P_ChangeWeapon();  // 1902
  SC_MP_EndRule_SetTimeLeft();  // 1910
  SC_P_ChangeWeapon();  // 1913
  SC_MP_EndRule_SetTimeLeft();  // 1921
  SC_P_ChangeWeapon();  // 1924
  func_1938();  // 1929
  SC_P_IsReady(129 + data[131]);  // 1933
  SC_P_ChangeWeapon();  // 1937
  SC_P_IsReady(&data[1] + 573);  // 1945
  SC_P_IsReady(SC_P_IsReady(&data[1] + 573) + 574);  // 1949
  while (1) {
    func_2002();  // 1953
    SC_P_IsReady((SC_P_IsReady(SC_P_IsReady(&data[1] + 573) + 574) <= 575) + 576);  // 1957
    func_1993();  // 1961
    break;  // 1968 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 1970
    break;  // 1972 (always true)
    SC_P_IsReady(local_3);  // 1974
    func_1984();  // 1975
    SC_P_IsReady(SC_P_IsReady(local_3) + 578.0);  // 1982
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 578.0));  // 1983
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 578.0)) + 579.0);  // 1990
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 578.0)) + 579.0));  // 1991
    if (SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 578.0)) + 579.0))) break;  // 1992
    SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 580.0);  // 1999
    SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 580.0));  // 2000
    if (SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 580.0))) break;  // 2001
  }
  SC_P_IsReady(&data[1] + 582);  // 2011
  SC_P_IsReady(SC_P_IsReady(&data[1] + 582) + 583);  // 2015
  while (1) {
    func_2068();  // 2019
    SC_P_IsReady((SC_P_IsReady(SC_P_IsReady(&data[1] + 582) + 583) <= 584) + 585);  // 2023
    func_2059();  // 2027
    break;  // 2034 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 2036
    break;  // 2038 (always true)
    SC_P_IsReady(local_3);  // 2040
    func_2050();  // 2041
    SC_P_IsReady(SC_P_IsReady(local_3) + 587.0);  // 2048
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 587.0));  // 2049
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 587.0)) + 588.0);  // 2056
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 587.0)) + 588.0));  // 2057
    if (SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 587.0)) + 588.0))) break;  // 2058
    SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 589.0);  // 2065
    SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 589.0));  // 2066
    if (SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 589.0))) break;  // 2067
  }
  SC_P_IsReady(&data[1] + 591);  // 2084
  SC_P_IsReady(SC_P_IsReady(&data[1] + 591) + 592);  // 2088
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(&data[1] + 591) + 592) + 593);  // 2092
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(&data[1] + 591) + 592) + 593) + 594);  // 2096
  SC_MP_EndRule_SetTimeLeft();  // 2104
  func_2162();  // 2105
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 596);  // 2109
  func_2162();  // 2113
  *(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 596) <= 597) = 598;  // 2117
}
void main(void) {
  int local_17;

  func_2497();  // 2488
  SC_MP_EndRule_SetTimeLeft();  // 2496
}
void func_2497(void) {
  int local_17;

  SC_MP_EndRule_SetTimeLeft();  // 2504
  func_2514();  // 2505
  SC_MP_EndRule_SetTimeLeft();  // 2513
}
void func_2514(void) {
  int local_265;

  SC_P_IsReady(&data[256] + 660);  // 2524
  SC_P_ChangeWeapon();  // 2531
  SC_P_IsReady(SC_P_ChangeWeapon());  // 2532
  SC_MP_EndRule_SetTimeLeft();  // 2540
  func_2543();  // 2541
}
void func_2543(void) {
  int local_265;
  int local_271;

  SC_P_IsReady(stack_tmp_0 + 1 + 665);  // 2547
  while (1) {
    func_2621();  // 2551
    data[1] = 666;  // 2556
    SC_P_IsReady(local_265);  // 2562
    func_2612();  // 2563
    *SC_P_IsReady(local_265) = 667;  // 2567
    break;  // 2571 (always true)
    SC_P_ChangeWeapon();  // 2572
    break;  // 2578 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 2580
    func_2612();  // 2581
    *SC_MP_EndRule_SetTimeLeft() = 669;  // 2585
    break;  // 2590 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 2591
    *SC_MP_EndRule_SetTimeLeft() = 672;  // 2595
    break;  // 2600 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 2601
    *SC_MP_EndRule_SetTimeLeft() = 675;  // 2605
    break;  // 2610 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 2611
    SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 677.0);  // 2618
    SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 677.0));  // 2619
    if (SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 677.0))) break;  // 2620
  }
  SC_P_ChangeWeapon();  // 2636
}