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

  func_1();  // 32
  while (1) {
    xfn_108();  // 36
    data[1] = 148;  // 41
    func_1();  // 47
    xfn_99();  // 48
    *local_259 = 149;  // 52
    func_3();  // 58
    *OUTPOSTCRATERBASE = 152;  // 62
    func_3();  // 68
    *153 = OUTPOSTCRATER5;  // 72
    func_3();  // 78
    *OUTPOSTCRATER6 = OUTPOSTCRATER8;  // 82
    func_3();  // 88
    *OUTPOSTCRATER9 = OUTPOSTCRATER11;  // 92
    func_3();  // 98
    func_1();  // 105
    func_1();  // 106
    break;  // 107 (always true)
  }
    xfn_146();  // 115
  xfn_124();  // 117
  func_1();  // 123
  func_2();  // 127
  SRS(0, 0);  // 131
  xfn_137();  // 132
  if (local_3 + 1) {
    func_1();  // 147
  }
    func_1();  // 147
  if (!(1)) {
    func_1();  // 147
  }
  func_2();  // 189
  func_1();  // 192
  xfn_200();  // 196
  func_2();  // 203
  xfn_226();  // 212
  if (local_11) {
    func_2();  // 244
    func_1();  // 245
  }
  func_5();  // 236
  func_1();  // 237
  func_3();  // 253
  func_2();  // 256
  func_1();  // 264
  func_1();  // 267
  *SGI_CURRENTMISSION = SGF_MISSIONTIMER;  // 274
  func_4();  // 277
  func_1();  // 283
  func_1();  // 286
  *205 = 206;  // 293
  func_4();  // 296
  func_1();  // 302
  func_1();  // 305
  *210 = 211;  // 312
  func_4();  // 315
  func_1();  // 321
  func_1();  // 324
  *215 = 216;  // 331
  func_4();  // 334
  func_1();  // 340
  func_1();  // 343
  *220 = 221;  // 350
  func_4();  // 353
  func_1();  // 359
  func_1();  // 362
  *225 = 226;  // 369
  func_4();  // 372
  func_1();  // 378
  func_1();  // 381
  *230 = 231;  // 388
  func_4();  // 391
  func_1();  // 397
  func_1();  // 400
  *235 = 236;  // 407
  func_4();  // 410
  func_1();  // 416
  func_1();  // 419
  *240 = 241;  // 426
  func_4();  // 429
  func_1();  // 435
  func_1();  // 438
  *245 = 246;  // 445
  func_4();  // 448
  func_1();  // 454
  func_1();  // 457
  *250 = 251;  // 464
  func_4();  // 467
  func_1();  // 473
  func_1();  // 476
  *PLAYER_FREESLOT = SC_PL_AI_SIT_IFL_S1G0;  // 483
  func_4();  // 486
  func_1();  // 492
  func_1();  // 495
  *260 = 261;  // 502
  func_4();  // 505
  func_1();  // 511
  func_1();  // 514
  *265 = 266;  // 521
  func_4();  // 524
  func_1();  // 530
  func_1();  // 533
  *270 = 271;  // 540
  func_4();  // 543
  func_1();  // 549
  func_1();  // 552
  *275 = 276;  // 559
  func_4();  // 562
  func_1();  // 568
  func_1();  // 571
  *280 = 281;  // 578
  func_4();  // 581
  func_1();  // 587
  func_1();  // 590
  *285 = 286;  // 597
  func_4();  // 600
  func_2();  // 616
  func_1();  // 617
  func_2();  // 624
  func_1();  // 625
  func_1();  // 629
  func_1();  // 633
  func_1();  // 639
  *local_18 = 294;  // 642
  func_1();  // 646
  func_5();  // 657
  func_1();  // 658
  func_2();  // 665
  func_1();  // 666
  func_3();  // 675
  func_3();  // 681
  func_1();  // 682
  func_1();  // 686
  func_1();  // 690
  func_1();  // 696
  *local_18 = 306;  // 699
  func_1();  // 703
  func_5();  // 714
  func_1();  // 715
  func_2();  // 722
  func_1();  // 723
  func_3();  // 732
  func_3();  // 738
  func_1();  // 739
  func_1();  // 743
  func_1();  // 747
  func_1();  // 753
  *local_18 = 318;  // 756
  func_1();  // 760
  func_5();  // 771
  func_1();  // 772
  func_2();  // 779
  func_1();  // 780
  func_3();  // 789
  func_3();  // 795
  func_1();  // 796
  func_1();  // 800
  func_1();  // 804
  func_1();  // 810
  *local_18 = 330;  // 813
  func_1();  // 817
  func_5();  // 828
  func_1();  // 829
  func_2();  // 836
  func_1();  // 837
  func_3();  // 846
  func_3();  // 852
  func_1();  // 853
  func_1();  // 857
  func_1();  // 861
  func_1();  // 867
  *local_18 = 342;  // 870
  func_1();  // 874
  func_5();  // 885
  func_1();  // 886
  func_2();  // 893
  func_1();  // 894
  func_3();  // 903
  func_3();  // 909
  func_1();  // 910
  func_1();  // 914
  func_1();  // 918
  func_1();  // 924
  *local_18 = 354;  // 927
  func_1();  // 931
  func_5();  // 942
  func_1();  // 943
  func_2();  // 950
  func_1();  // 951
  func_3();  // 960
  func_3();  // 966
  func_1();  // 967
  func_3();  // 975
  func_2();  // 978
  func_3();  // 986
  func_2();  // 989
  func_3();  // 997
  func_2();  // 1000
  func_3();  // 1008
  func_2();  // 1011
  func_3();  // 1019
  func_2();  // 1022
  func_3();  // 1030
  func_2();  // 1033
  func_2();  // 1049
  func_1();  // 1050
  func_2();  // 1057
  func_1();  // 1058
  func_1();  // 1062
  func_1();  // 1066
  func_1();  // 1072
  *local_18 = 388;  // 1075
  func_1();  // 1079
  func_5();  // 1090
  func_1();  // 1091
  func_2();  // 1098
  func_1();  // 1099
  func_3();  // 1108
  func_3();  // 1114
  func_1();  // 1115
  func_1();  // 1119
  func_1();  // 1123
  func_1();  // 1129
  *local_18 = 400;  // 1132
  func_1();  // 1136
  func_5();  // 1147
  func_1();  // 1148
  func_2();  // 1155
  func_1();  // 1156
  func_3();  // 1165
  func_3();  // 1171
  func_1();  // 1172
  func_1();  // 1176
  func_1();  // 1180
  func_1();  // 1186
  *local_18 = 412;  // 1189
  func_1();  // 1193
  func_5();  // 1204
  func_1();  // 1205
  func_2();  // 1212
  func_1();  // 1213
  func_3();  // 1222
  func_3();  // 1228
  func_1();  // 1229
  func_1();  // 1233
  func_1();  // 1237
  func_1();  // 1243
  *local_18 = 424;  // 1246
  func_1();  // 1250
  func_5();  // 1261
  func_1();  // 1262
  func_2();  // 1269
  func_1();  // 1270
  func_3();  // 1279
  func_3();  // 1285
  func_1();  // 1286
  func_3();  // 1294
  func_2();  // 1297
  func_3();  // 1305
  func_2();  // 1308
  func_3();  // 1316
  func_2();  // 1319
  func_3();  // 1327
  func_2();  // 1330
  func_2();  // 1346
  func_1();  // 1347
  func_2();  // 1354
  func_1();  // 1355
  func_1();  // 1359
  func_1();  // 1363
  func_1();  // 1369
  *local_18 = 452;  // 1372
  func_1();  // 1376
  func_5();  // 1387
  func_1();  // 1388
  func_2();  // 1395
  func_1();  // 1396
  func_3();  // 1405
  func_3();  // 1411
  func_1();  // 1412
  func_1();  // 1416
  func_1();  // 1420
  func_1();  // 1426
  *local_18 = 464;  // 1429
  func_1();  // 1433
  func_5();  // 1444
  func_1();  // 1445
  func_2();  // 1452
  func_1();  // 1453
  func_3();  // 1462
  func_3();  // 1468
  func_1();  // 1469
  func_1();  // 1473
  func_1();  // 1477
  func_1();  // 1483
  *local_18 = 476;  // 1486
  func_1();  // 1490
  func_5();  // 1501
  func_1();  // 1502
  func_2();  // 1509
  func_1();  // 1510
  func_3();  // 1519
  func_3();  // 1525
  func_1();  // 1526
  func_1();  // 1530
  func_1();  // 1534
  func_1();  // 1540
  *local_18 = 488;  // 1543
  func_1();  // 1547
  func_5();  // 1558
  func_1();  // 1559
  func_2();  // 1566
  func_1();  // 1567
  func_3();  // 1576
  func_3();  // 1582
  func_1();  // 1583
  func_3();  // 1591
  func_2();  // 1594
  func_3();  // 1602
  func_2();  // 1605
  func_3();  // 1613
  func_2();  // 1616
  func_3();  // 1624
  func_2();  // 1627
  func_2();  // 1643
  func_1();  // 1644
  func_2();  // 1651
  func_1();  // 1652
  func_1();  // 1656
  func_1();  // 1660
  func_1();  // 1666
  *local_18 = 515;  // 1669
  func_1();  // 1673
  func_5();  // 1684
  func_1();  // 1685
  func_2();  // 1692
  func_1();  // 1693
  func_3();  // 1702
  func_3();  // 1708
  func_1();  // 1709
  func_1();  // 1713
  func_1();  // 1717
  func_1();  // 1723
  *local_18 = 527;  // 1726
  func_1();  // 1730
  func_5();  // 1741
  func_1();  // 1742
  func_2();  // 1749
  func_1();  // 1750
  func_3();  // 1759
  func_3();  // 1765
  func_1();  // 1766
  func_1();  // 1770
  func_1();  // 1774
  func_1();  // 1780
  *local_18 = 539;  // 1783
  func_1();  // 1787
  func_5();  // 1798
  func_1();  // 1799
  func_2();  // 1806
  func_1();  // 1807
  func_3();  // 1816
  func_3();  // 1822
  func_1();  // 1823
  func_1();  // 1827
  func_1();  // 1831
  func_1();  // 1837
  *local_18 = 551;  // 1840
  func_1();  // 1844
  func_5();  // 1855
  func_1();  // 1856
  func_2();  // 1863
  func_1();  // 1864
  func_3();  // 1873
  func_3();  // 1879
  func_1();  // 1880
  func_3();  // 1888
  func_2();  // 1891
  func_3();  // 1899
  func_2();  // 1902
  func_3();  // 1910
  func_2();  // 1913
  func_3();  // 1921
  func_2();  // 1924
  xfn_1938();  // 1929
  func_1();  // 1933
  func_2();  // 1937
  func_1();  // 1945
  func_1();  // 1949
  while (1) {
    xfn_2002();  // 1953
    func_1();  // 1957
    xfn_1993();  // 1961
    break;  // 1968 (always true)
    func_3();  // 1970
    break;  // 1972 (always true)
    func_1();  // 1974
    xfn_1984();  // 1975
    func_1();  // 1982
    func_1();  // 1983
    func_1();  // 1990
    func_1();  // 1991
    if (local_3 + 578.0 + 579.0) break;  // 1992
    func_1();  // 1999
    func_1();  // 2000
    if (local_4 + 580.0) break;  // 2001
  }
  func_1();  // 2011
  func_1();  // 2015
  while (1) {
    xfn_2068();  // 2019
    func_1();  // 2023
    xfn_2059();  // 2027
    break;  // 2034 (always true)
    func_3();  // 2036
    break;  // 2038 (always true)
    func_1();  // 2040
    xfn_2050();  // 2041
    func_1();  // 2048
    func_1();  // 2049
    func_1();  // 2056
    func_1();  // 2057
    if (local_3 + 587.0 + 588.0) break;  // 2058
    func_1();  // 2065
    func_1();  // 2066
    if (local_4 + 589.0) break;  // 2067
  }
  func_1();  // 2084
  func_1();  // 2088
  func_1();  // 2092
  func_1();  // 2096
  func_3();  // 2104
  xfn_2162();  // 2105
  func_1();  // 2109
  xfn_2162();  // 2113
  *(local_269 + 596 <= 597) = 598;  // 2117
}
void main(void) {
  int local_17;

  xfn_2497();  // 2488
  func_3();  // 2496
}
void func_2497(void) {
  int local_17;

  func_3();  // 2504
  xfn_2514();  // 2505
  func_3();  // 2513
}
void func_2514(void) {
  int local_265;

  func_1();  // 2524
  func_2();  // 2531
  func_1();  // 2532
  func_3();  // 2540
  xfn_2543();  // 2541
}
void func_2543(void) {
  int local_265;
  int local_271;

  func_1();  // 2547
  while (1) {
    xfn_2621();  // 2551
    data[1] = 666;  // 2556
    func_1();  // 2562
    xfn_2612();  // 2563
    *local_265 = 667;  // 2567
    break;  // 2571 (always true)
    func_2();  // 2572
    break;  // 2578 (always true)
    func_3();  // 2580
    xfn_2612();  // 2581
    *local_265 = 669;  // 2585
    break;  // 2590 (always true)
    func_3();  // 2591
    *670 = 672;  // 2595
    break;  // 2600 (always true)
    func_3();  // 2601
    *673 = 675;  // 2605
    break;  // 2610 (always true)
    func_3();  // 2611
    func_1();  // 2618
    func_1();  // 2619
    break;  // 2620 (always true)
  }
  func_2();  // 2636
}