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
  int stack_tmp_0;

  SC_P_IsReady(stack_tmp_0 + 1 + 147);  // 32
}
void func_99(void) {
}
void func_108(void) {
  int stack_tmp_0;

  func_124();  // 117
}
void func_124(void) {
  int32_t local_1;
  int local_3;

  SC_P_ChangeWeapon();  // 127
  SRS(0, 0);  // 131
  func_137();  // 132
  if (local_3 + 1) {
    SC_P_IsReady(166u);  // 147
  }
    SC_P_IsReady(166u);  // 147
  if (!(1)) {
    SC_P_IsReady(166u);  // 147
  }
  SC_P_IsReady(local_1);  // 157
}
void func_177(void) {
}
void func_200(void) {
}
void func_226(void) {
}
void func_1938(void) {
  SC_P_IsReady(&data[1] + 573);  // 1945
  SC_P_IsReady(SC_P_IsReady(&data[1] + 573) + 574);  // 1949
}
void func_1984(void) {
}
void func_1993(void) {
}
void func_2002(void) {
}
void func_2050(void) {
}
void func_2059(void) {
}
void func_2068(void) {
}
void func_2153(void) {
}
void func_2162(void) {
}
void func_2170(void) {
  int local_270;
  int32_t stack_tmp_0;

  SC_P_IsReady(stack_tmp_0);  // 2172
  SC_P_IsReady(&data[5] + 609);  // 2184
  SC_P_IsReady(SC_P_IsReady(&data[5] + 609) + 610);  // 2188
  SC_P_ChangeWeapon();  // 2195
}
void func_2310(void) {
}
void func_2342(void) {
}
void func_2393(void) {
}
void func_2411(void) {
}
void func_2416(void) {
}
void main(void) {
  int32_t local_265;

  func_2497();  // 2488
  SC_MP_EndRule_SetTimeLeft();  // 2496
  SC_MP_EndRule_SetTimeLeft();  // 2504
  func_2514();  // 2505
  SC_MP_EndRule_SetTimeLeft();  // 2513
  SC_P_IsReady(&data[256] + 660);  // 2524
  SC_P_ChangeWeapon();  // 2531
  SC_P_IsReady(local_265);  // 2532
  SC_P_IsReady(1329u);  // 2547
}
void func_2612(void) {
}
void func_2621(void) {
  int local_271;

  SC_P_ChangeWeapon();  // 2636
}
void func_2717(void) {
  int32_t local_265;

  SC_P_IsReady(&data[256] + 693);  // 2727
  SC_P_ChangeWeapon();  // 2734
  SC_P_IsReady(local_265);  // 2735
  SC_P_IsReady(1395u);  // 2750
}
void func_2802(void) {
  SC_P_IsReady(705 + data[129]);  // 2805
}
void func_2815(void) {
  int32_t local_277;

  SC_P_IsReady(&data[256] + 707);  // 2829
  SC_P_ChangeWeapon();  // 2836
  SC_P_IsReady(local_277);  // 2837
  SC_P_ChangeWeapon();  // 2844
  SC_P_IsReady(local_277);  // 2845
  SC_P_ChangeWeapon();  // 2852
  SC_P_IsReady(local_277);  // 2853
  SC_P_ChangeWeapon();  // 2860
  SC_P_IsReady(local_277);  // 2861
  SC_P_ChangeWeapon();  // 2868
  SC_P_IsReady(local_277);  // 2869
  SC_P_IsReady(1439u);  // 2884
}
void func_3021(void) {
  SC_P_IsReady(751 + data[129]);  // 3024
}
void func_3034(void) {
  int32_t local_268;

  SC_P_IsReady(&data[256] + 753);  // 3045
  SC_P_ChangeWeapon();  // 3052
  SC_P_IsReady(local_268);  // 3053
  SC_P_ChangeWeapon();  // 3060
  SC_P_IsReady(local_268);  // 3061
  SC_P_IsReady(1521u);  // 3076
}
void func_3130(void) {
  SC_P_IsReady(769 + data[129]);  // 3133
  SC_MP_EndRule_SetTimeLeft();  // 3141
  func_3155();  // 3142
}
void func_3151(void) {
  SC_P_IsReady(773 + data[129]);  // 3154
}
void func_3164(void) {
  int32_t local_265;

  SC_P_IsReady(&data[256] + 775);  // 3174
  SC_P_ChangeWeapon();  // 3181
  SC_P_IsReady(local_265);  // 3182
  SC_P_IsReady(1559u);  // 3197
}
void func_3251(void) {
  SC_P_IsReady(788 + data[129]);  // 3254
}
void func_3264(void) {
  int32_t local_265;

  SC_P_IsReady(&data[256] + 790);  // 3274
  SC_P_ChangeWeapon();  // 3281
  SC_P_IsReady(local_265);  // 3282
  SC_P_IsReady(1589u);  // 3297
}
void func_3351(void) {
  SC_P_IsReady(803 + data[129]);  // 3354
}
void func_3364(void) {
  int32_t local_271;

  SC_P_IsReady(&data[256] + 805);  // 3376
  SC_P_ChangeWeapon();  // 3383
  SC_P_IsReady(local_271);  // 3384
  SC_P_IsReady(1619u);  // 3399
}
void func_3491(void) {
  SC_P_IsReady(828 + data[129]);  // 3494
}
void func_3504(void) {
  int32_t local_265;

  SC_P_IsReady(&data[256] + 830);  // 3514
  SC_P_ChangeWeapon();  // 3521
  SC_P_IsReady(local_265);  // 3522
  SC_P_IsReady(1669u);  // 3537
}
void func_3586(void) {
  SC_P_IsReady(842 + data[129]);  // 3589
}
void func_3599(void) {
  int32_t local_265;

  SC_P_IsReady(&data[256] + 844);  // 3609
  SC_P_ChangeWeapon();  // 3616
  SC_P_IsReady(local_265);  // 3617
  SC_P_IsReady(1697u);  // 3632
}
void func_3681(void) {
  SC_P_IsReady(856 + data[129]);  // 3684
}
void func_3694(void) {
  int32_t local_345;

  SC_P_IsReady(local_345);  // 3756
  func_3759();  // 3757
}
void func_3759(void) {
  int stack_tmp_295;

  SC_P_IsReady(stack_tmp_295 + 865);  // 3762
}
void func_3814(void) {
}
void func_3823(void) {
  int local_345;

  func_3844();  // 3826
  SC_P_IsReady((void*)data[4] + data[124]);  // 3834
  func_3844();  // 3838
  SC_P_IsReady((char*)876 % 133 + data[124]);  // 3843
  SRS(0, 0);  // 3846
  func_3863();  // 3847
  SC_P_IsReady((void*)data[4] + data[135]);  // 3855
  func_3861();  // 3859
  if (!(1)) {
    SC_P_IsReady((void*)data[4] + data[135]);  // 3870
  }
  SC_P_ChangeWeapon();  // 3874
  SC_P_IsReady(1015u);  // 3878
  SC_P_IsReady(SC_P_IsReady(1015u) + 881);  // 3882
  SC_MP_EndRule_SetTimeLeft();  // 3890
  func_4156();  // 3891
  SC_P_IsReady(local_345 + 883);  // 3895
  SC_P_IsReady(SC_P_IsReady(local_345 + 883) + 884);  // 3899
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_345 + 883) + 884) + 885);  // 3903
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_345 + 883) + 884) + 885) + 886);  // 3907
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_345 + 883) + 884) + 885) + 886) + 887);  // 3911
  SC_P_IsReady((&data[1] != &data[1]) + local_345);  // 3918
  SC_P_IsReady((&data[1] != &data[1]) + local_345);  // 3925
  SC_P_IsReady(SC_P_IsReady((&data[1] != &data[1]) + local_345) + 888);  // 3929
}
void func_3966(void) {
}
void func_3980(void) {
}
void func_4013(void) {
}
void func_4046(void) {
}
void func_4089(void) {
}
void func_4132(void) {
}
void func_4141(void) {
}
void func_4156(void) {
  SC_P_ChangeWeapon();  // 4160
}
void func_4178(void) {
}
void func_4186(void) {
}
void func_4194(void) {
}
void func_4259(void) {
  if ((char*)978) {
    SC_P_IsReady(979 + data[135]);  // 4271
  } else {
    SC_P_IsReady(979 + data[135]);  // 4271
  }
  SC_P_IsReady(980 + data[135]);  // 4276
  SC_P_ChangeWeapon();  // 4330
  SC_P_IsReady(995 + data[130]);  // 4334
  SC_P_IsReady(996 + data[129]);  // 4338
}
void func_4339(void) {
  int stack_tmp_0;

  if (stack_tmp_0) {
    SC_P_IsReady((void*)data[4] + data[130]);  // 4352
    func_4376();  // 4356
    func_4363();  // 4361
  }
}
void func_4363(void) {
  SC_P_ChangeWeapon();  // 4367
  SC_P_IsReady(SGI_LEVPILOT_S1G5 + data[129]);  // 4371
  SC_P_IsReady(1007 + data[130]);  // 4375
}
void func_4424(void) {
}
void func_4446(void) {
  SC_P_ChangeWeapon();  // 4450
  SC_P_IsReady(1043 + data[129]);  // 4454
  SC_P_IsReady(1044 + data[130]);  // 4458
}
void func_4512(void) {
}
void func_4534(void) {
  SC_P_ChangeWeapon();  // 4538
  SC_P_IsReady(1087 + data[129]);  // 4542
  SC_P_IsReady(1088 + data[130]);  // 4546
}
void func_4612(void) {
}
void func_4634(void) {
  SC_P_ChangeWeapon();  // 4638
  SC_P_IsReady(1139 + data[129]);  // 4642
  SC_P_IsReady(1140 + data[130]);  // 4646
}
void func_4712(void) {
}
void func_4734(void) {
  SC_P_ChangeWeapon();  // 4738
  SC_P_IsReady(1191 + data[129]);  // 4742
  SC_P_IsReady(1192 + data[130]);  // 4746
}
void func_4812(void) {
}
void func_4834(void) {
  SC_P_ChangeWeapon();  // 4838
  SC_P_IsReady(1243 + data[129]);  // 4842
  SC_P_IsReady(1244 + data[130]);  // 4846
}
void func_4912(void) {
}
void func_4934(void) {
  SC_P_ChangeWeapon();  // 4938
  SC_P_IsReady(1295 + data[129]);  // 4942
  SC_P_IsReady(1296 + data[130]);  // 4946
}
void func_5012(void) {
}
void func_5034(void) {
  SC_P_ChangeWeapon();  // 5038
  SC_P_IsReady(1347 + data[129]);  // 5042
  SC_P_IsReady(1348 + data[130]);  // 5046
}
void func_5112(void) {
}
void func_5146(void) {
  int stack_tmp_0;

  if (stack_tmp_0) {
    SC_P_IsReady((void*)data[4] + data[130]);  // 5159
    SC_P_IsReady(SC_P_IsReady((void*)data[4] + data[130]) + 1404);  // 5163
    func_5182();  // 5167
  }
  SC_P_ChangeWeapon();  // 5172
  SC_P_IsReady(1414 + data[129]);  // 5177
  SC_P_IsReady(1415 + data[130]);  // 5181
}
void func_5182(void) {
  int32_t local_345;
  int stack_tmp_0;

  if (stack_tmp_0) {
    SC_P_IsReady(stack_tmp_0);  // 5183
  } else {
    SC_P_IsReady(stack_tmp_0);  // 5183
  }
  SC_P_IsReady(local_345);  // 5199
  func_5206();  // 5200
  SC_P_IsReady(SC_P_IsReady(local_345));  // 5203
}
void func_5206(void) {
  int stack_tmp_0;

  SC_P_ChangeWeapon();  // 5215
  SC_P_IsReady(data[4] + data[125]);  // 5221
  SC_P_IsReady(data[4] + data[126]);  // 5227
  SC_P_IsReady(1421 + data[127]);  // 5231
  SC_P_IsReady(SC_P_IsReady(1421 + data[127]));  // 5234
}
void func_5237(void) {
}
void func_5391(void) {
  int32_t stack_tmp_0;

  SC_P_IsReady(stack_tmp_0);  // 5393
  SC_P_ChangeWeapon();  // 5397
  SC_P_ChangeWeapon();  // 5401
  SC_P_ChangeWeapon();  // 5405
  SC_P_IsReady(1477u);  // 5408
  SC_P_IsReady(SC_P_IsReady(1477u) + 1481);  // 5412
}
void func_5450(void) {
  int stack_tmp_271;

  SC_P_ChangeWeapon();  // 5453
  SC_P_IsReady(stack_tmp_271 + 1489);  // 5457
}
void func_5641(void) {
}
void func_5650(void) {
  SC_P_IsReady(data[0] + (1534.0 | data[4]));  // 5658
  *data[4] = 1539;  // 5668
  SC_MP_EndRule_SetTimeLeft();  // 5672
}
void func_5704(void) {
}
void func_5763(void) {
}
void func_5772(void) {
  SC_P_IsReady(data[0] + (1580.0 | data[4]));  // 5780
  *data[4] = 1585;  // 5790
  SC_MP_EndRule_SetTimeLeft();  // 5794
}
void func_5826(void) {
  int32_t local_345;

  SC_P_ChangeWeapon();  // 5829
  func_5874();  // 5833
  SC_P_IsReady(data[4] + 1610);  // 5837
  SC_MP_EndRule_SetTimeLeft();  // 5845
  SC_P_IsReady(local_345);  // 5846
  SC_P_IsReady(SC_P_IsReady(local_345) + 1612);  // 5850
}
void func_5874(void) {
  int32_t local_345;
  int stack_tmp_0;
  int stack_tmp_294;

}
void func_5898(void) {
}
void func_5914(void) {
  int stack_tmp_0;

  SC_P_IsReady(stack_tmp_0);  // 5915
}
void func_5952(void) {
  int local_4;
  int stack_tmp_0;

  if (stack_tmp_0) {
    func_5968();  // 5961
    SC_P_IsReady(local_4 - local_4 + data[4] - 1631);  // 5966
  }
}
void func_5968(void) {
  SC_P_ChangeWeapon();  // 5973
}
void func_6095(void) {
}
void func_6101(void) {
}
void func_6159(void) {
}
void func_6180(void) {
  int32_t stack_tmp_0;

  SC_P_IsReady(stack_tmp_0);  // 6180
}