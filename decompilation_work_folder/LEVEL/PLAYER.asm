; ==========================================
; Disassembly of: decompilation/LEVEL/PLAYER.SCR
; Instructions: 7334
; External functions: 65
; ==========================================

; External Functions (XFN)
; ------------------------
;   [  0] frnd(float)float
;   [  1] SC_P_Ai_SetMode(unsignedlong,unsignedlong)void
;   [  2] SC_P_Ai_EnableShooting(unsignedlong,int)void
;   [  3] SC_P_Ai_EnableSituationUpdate(unsignedlong,int)void
;   [  4] SC_Log(unsignedlong,*char,...)void
;   [  5] SC_P_Ai_Stop(unsignedlong)void
;   [  6] SC_P_ScriptMessage(unsignedlong,unsignedlong,unsignedlong)void
;   [  7] SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong
;   [  8] SC_P_Ai_GetSureEnemies(unsignedlong)unsignedlong
;   [  9] SC_P_Ai_GetDanger(unsignedlong)float
;   [ 10] SC_ZeroMem(*void,unsignedlong)void
;   [ 11] SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void
;   [ 12] SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void
;   [ 13] SC_ggi(unsignedlong)int
;   [ 14] SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void
;   [ 15] SC_PC_Get(void)unsignedlong
;   [ 16] SC_P_GetWeapons(unsignedlong,*s_SC_P_Create)int
;   [ 17] SC_sgi(unsignedlong,int)void
;   [ 18] SC_P_ReadHealthFromGlobalVar(unsignedlong,unsignedlong)void
;   [ 19] SC_P_WriteHealthToGlobalVar(unsignedlong,unsignedlong)void
;   [ 20] SC_P_ReadAmmoFromGlobalVar(unsignedlong,unsignedlong,unsignedlong)void
;   [ 21] SC_P_SetAmmoInWeap(unsignedlong,unsignedlong,unsignedlong)void
;   [ 22] SC_P_WriteAmmoToGlobalVar(unsignedlong,unsignedlong,unsignedlong)void
;   [ 23] SC_P_GetAmmoInWeap(unsignedlong,unsignedlong)unsignedlong
;   [ 24] SC_PC_GetIntel(*s_SC_P_intel)void
;   [ 25] SC_PC_SetIntel(*s_SC_P_intel)void
;   [ 26] SC_MissionCompleted(void)void
;   [ 27] SC_Osi(*char,...)void
;   [ 28] SC_MissionDone(void)void
;   [ 29] SC_ShowHelp(*unsignedlong,unsignedlong,float)void
;   [ 30] rand(void)int
;   [ 31] SC_P_GetPos(unsignedlong,*c_Vector3)void
;   [ 32] SC_MP_EnumPlayers(*s_SC_MP_EnumPlayers,*unsignedlong,unsignedlong)int
;   [ 33] SC_2VectorsDist(*c_Vector3,*c_Vector3)float
;   [ 34] SC_PC_GetPos(*c_Vector3)int
;   [ 35] SC_GetGroupPlayers(unsignedlong,unsignedlong)unsignedlong
;   [ 36] SC_P_IsReady(unsignedlong)int
;   [ 37] SC_P_GetActive(unsignedlong)int
;   [ 38] SC_NOD_Get(*void,*char)*void
;   [ 39] SC_NOD_GetWorldPos(*void,*c_Vector3)void
;   [ 40] SC_NOD_GetWorldRotZ(*void)float
;   [ 41] SC_P_Ai_GetPeaceMode(unsignedlong)unsignedlong
;   [ 42] SC_P_Ai_SetPeaceMode(unsignedlong,unsignedlong)void
;   [ 43] SC_DoExplosion(*c_Vector3,unsignedlong)void
;   [ 44] SC_message(*char,...)void
;   [ 45] cos(float)float
;   [ 46] sin(float)float
;   [ 47] SC_DUMMY_Set_DoNotRenHier2(*void,int)void
;   [ 48] SC_GetWp(*char,*c_Vector3)int
;   [ 49] SC_CreatePtc(unsignedlong,*c_Vector3)void
;   [ 50] SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void
;   [ 51] SC_CreatePtc_Ext(unsignedlong,*void,float,float,float,float)void
;   [ 52] SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void
;   [ 53] SC_P_Ai_SetBattleProps(unsignedlong,*s_SC_P_Ai_BattleProps)void
;   [ 54] SC_P_GetDir(unsignedlong,*c_Vector3)void
;   [ 55] SC_VectorLen(*c_Vector3)float
;   [ 56] SC_IsNear3D(*c_Vector3,*c_Vector3,float)int
;   [ 57] SC_GetPls(*s_sphere,*unsignedlong,*unsignedlong)void
;   [ 58] SC_P_SetSpecAnims(unsignedlong,*s_SC_P_SpecAnims)void
;   [ 59] SC_P_DoHit(unsignedlong,unsignedlong,float)void
;   [ 60] SC_SphereIsVisible(*s_sphere)int
;   [ 61] SC_P_Create(*s_SC_P_Create)unsignedlong
;   [ 62] SC_P_SetSpeachDist(unsignedlong,float)void
;   [ 63] SC_PC_EnablePronePosition(int)void
;   [ 64] SC_PC_EnableFlashLight(int)void

; Strings
; -------
;   [  20] "Player %d enabled"
;   [  60] "Player %d disabled"
;   [  88] "Message %d %d to unexisted player!"
;   [ 200] "È"
;   [ 212] "e"
;   [ 220] "ÿ"
;   [ 228] "f"
;   [ 236] "ÿ"
;   [ 244] "g"
;   [ 248] "È"
;   [ 260] "È"
;   [ 276] "ÿ"
;   [ 284] "h"
;   [ 288] "ÿ"
;   [ 296] "i"
;   [ 300] ";"
;   [ 304] "ÿ"
;   [ 312] "j"
;   [ 316] "ÿ"
;   [ 324] "k"
;   [ 328] "ÿ"
;   [ 336] "l"
;   [ 340] "?"
;   [ 344] "ÿ"
;   [ 352] "m"
;   [ 356] "ÿ"
;   [ 364] ":"
;   [ 368] "e"
;   [ 372] "e"
;   [ 376] "ÿ"
;   [ 380] "f"
;   [ 384] "f"
;   [ 388] "ÿ"
;   [ 392] "g"
;   [ 396] "g"
;   [ 400] "ÿ"
;   [ 404] "h"
;   [ 408] "h"
;   [ 412] "ÿ"
;   [ 416] "i"
;   [ 420] "i"
;   [ 424] "ÿ"
;   [ 428] "j"
;   [ 432] "j"
;   [ 436] "ÿ"
;   [ 440] "k"
;   [ 444] "k"
;   [ 448] "ÿ"
;   [ 452] "l"
;   [ 456] "l"
;   [ 460] "ÿ"
;   [ 464] "m"
;   [ 468] "m"
;   [ 472] "ÿ"
;   [ 476] "n"
;   [ 480] "n"
;   [ 484] "ÿ"
;   [ 488] "_"
;   [ 492] "_"
;   [ 496] "<"
;   [ 500] "Y"
;   [ 504] "Z"
;   [ 512] "Z"
;   [ 516] "["
;   [ 524] "["
;   [ 528] "<"
;   [ 532] "Y"
;   [ 536] "Z"
;   [ 544] "["
;   [ 556] "\n"
;   [ 560] "2"
;   [ 576] "\n"
;   [ 580] "2"
;   [ 592] "MISSION COMPLETE"
;   [ 622] "À@"
;   [ 638] "@A"
;   [ 658] "ÀA\n"
;   [ 668] "È"
;   [ 744] "\r"
;   [ 752] "	"
;   [ 824] "È"
;   [ 832] "\n"
;   [ 896] "\n"
;   [ 964] "\n"
;   [1004] "	"
;   [1016] "\r"
;   [1028] "	"
;   [1032] "\n"
;   [1084] "\r"
;   [1168] "\n"
;   [1256] "\n"
;   [1348] " "
;   [1352] "\r"
;   [1404] "È"
;   [1424] "\r"
;   [1428] "ini\players\poorvc.ini"
;   [1456] "ini\players\poorvc2.ini"
;   [1480] "ini\players\poorvc3.ini"
;   [1528] "\n"
;   [1532] "\r"
;   [1536] "ini\players\vcfighter2.ini"
;   [1568] "ini\players\vcfighter3.ini"
;   [1596] "ini\players\vcfighter4.ini"
;   [1624] "	"
;   [1636] "\r"
;   [1656] "ini\players\vcfighter3.ini"
;   [1684] "\n"
;   [1688] "ini\players\vcfighter2.ini"
;   [1720] "ini\players\vcfighter3.ini"
;   [1748] "ini\players\vcfighter4.ini"
;   [1804] "\r"
;   [1808] "ini\players\vcuniform1.ini"
;   [1840] "ini\players\vcuniform2.ini"
;   [1868] "ini\players\vcuniform3.ini"
;   [1920] " "
;   [1928] "ini\players\nvasoldier2.ini"
;   [1960] "ini\players\nvasoldier3.ini"
;   [1988] "ini\players\nvaofficer.ini"
;   [2016] "ini\players\default_aiviet.ini"
;   [2076] "È"
;   [2092] "&"
;   [2184] "&"
;   [2224] "	"
;   [2232] "\n"
;   [2280] "%"
;   [2288] "&"
;   [2296] "\r"
;   [2388] "#"
;   [2404] "#"
;   [2420] " "
;   [2428] "!"
;   [2436] """
;   [2520] "#"
;   [2528] "$"
;   [2540] "#"
;   [2548] " "
;   [2556] "!"
;   [2564] """
;   [2580] " "
;   [2584] "!"
;   [2592] """
;   [2600] "#"
;   [2608] "$"
;   [2616] "#"
;   [2632] " "
;   [2640] "!"
;   [2648] """
;   [2656] " "
;   [2920] "FATAL! Claymore %s not found!!!!!!"
;   [2960] "ÃõÈ?"
;   [2967] "@"
;   [2991] "A"
;   [3012] "°"
;   [3024] "°"
;   [3034] "zD"
;   [3058] "zD"
;   [3094] "zD"
;   [3112] "Æ"
;   [3120] "°"
;   [3126] "zD"
;   [3164] "Æ"
;   [3168] "±"
;   [3192] "°"
;   [3198] "zD"
;   [3216] "Æ"
;   [3224] "°"
;   [3230] "zD"
;   [3248] "Æ"
;   [3279] "?"
;   [3334] "zD "
;   [3352] "d"
;   [3374] "zD "
;   [3416] "GetMyGroup: TOO much players in group around!"
;   [3472] " "
;   [3484] "VC %d %d couldnot find anyone to lead group %d"
;   [3544] "@"
;   [3556] "@"
;   [3568] "VC %d %d moved command over group"
;   [3676] " "
;   [3824] "G\Equipment\US\eqp\CUP_bangs\velka_polni\EOP_e_..."
;   [3888] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [3932] "G\Equipment\US\eqp\CUP_bangs\velka_polni\EOP_e_..."
;   [4000] "G\Equipment\US\bes\EOP_e_knife01.BES"
;   [4044] "G\Equipment\US\eqp\CUP_bangs\velka_polni\EOP_e_..."
;   [4108] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [4156] "G\Equipment\US\eqp\CUP_bangs\velka_polni\EOP_e_..."
;   [4224] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [4268] " "
;   [4272] "G\Equipment\US\eqp\CUP_bangs\velka_polni\EOP_e_..."
;   [4336] " "
;   [4340] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [4384] "("
;   [4388] "G\Equipment\US\eqp\CUP_bangs\velka_polni\EOP_e_..."
;   [4456] "("
;   [4460] "G\Equipment\US\bes\EOP_e_maceta01.BES"
;   [4500] "0"
;   [4504] "G\Equipment\US\eqp\CUP_bangs\velka_polni\EOP_e_..."
;   [4564] "0"
;   [4568] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [4612] "8"
;   [4616] "G\Equipment\US\eqp\CUP_bangs\velka_polni\EOP_e_..."
;   [4680] "8"
;   [4688] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [4732] "G\Equipment\US\eqp\CUP_bangs\lehke_vybaveni\EOP..."
;   [4800] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [4848] "G\Equipment\US\eqp\CUP_bangs\lehke_vybaveni\EOP..."
;   [4924] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [4968] "G\Equipment\US\eqp\CUP_bronson\velka_polni\EOP_..."
;   [5036] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [5080] "G\Equipment\US\eqp\CUP_bronson\velka_polni\EOP_..."
;   [5148] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [5192] "G\Equipment\US\eqp\CUP_bronson\velka_polni\EOP_..."
;   [5264] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [5312] "G\Equipment\US\eqp\CUP_bronson\velka_polni\EOP_..."
;   [5384] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [5428] " "
;   [5432] "G\Equipment\US\eqp\CUP_bronson\velka_polni\EOP_..."
;   [5500] " "
;   [5504] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [5548] "("
;   [5552] "G\Equipment\US\eqp\CUP_bronson\velka_polni\EOP_..."
;   [5620] "("
;   [5624] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [5668] "0"
;   [5672] "G\Equipment\US\eqp\CUP_bronson\velka_polni\EOP_..."
;   [5740] "0"
;   [5744] "G\Equipment\US\bes\EOP_hat1US_v01.BES"
;   [5784] "8"
;   [5788] "G\Equipment\US\eqp\CUP_bronson\velka_polni\EOP_..."
;   [5852] "8"
;   [5860] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [5904] "G\Equipment\US\eqp\CUP_bronson\lehke_vybaveni\E..."
;   [5976] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [6024] "G\Equipment\US\eqp\CUP_bronson\lehke_vybaveni\E..."
;   [6100] "G\Equipment\US\bes\EOP_hat1US_v01.BES"
;   [6144] "G\Equipment\US\eqp\CUP_bronson\lehke_vybaveni\E..."
;   [6220] "G\Equipment\US\bes\EOP_hat4US_v01.BES"
;   [6264] "G\Equipment\US\eqp\CUP_crocker\velka_polni\EOP_..."
;   [6332] "G\Equipment\US\bes\EOP_e_bigmedicbag01.BES"
;   [6380] "G\Equipment\US\eqp\CUP_crocker\velka_polni\EOP_..."
;   [6452] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [6496] "G\Equipment\US\eqp\CUP_crocker\velka_polni\EOP_..."
;   [6564] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [6608] "G\Equipment\US\eqp\CUP_crocker\velka_polni\EOP_..."
;   [6680] "G\Equipment\US\bes\EOP_e_glasses01.BES"
;   [6720] " "
;   [6724] "G\Equipment\US\eqp\CUP_crocker\velka_polni\EOP_..."
;   [6788] " "
;   [6792] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [6836] "("
;   [6840] "G\Equipment\US\eqp\CUP_crocker\velka_polni\EOP_..."
;   [6908] "("
;   [6912] "G\Equipment\US\bes\EOP_e_medicbag01.BES"
;   [6952] "0"
;   [6956] "G\Equipment\US\eqp\CUP_crocker\velka_polni\EOP_..."
;   [7020] "0"
;   [7024] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [7068] "8"
;   [7072] "G\Equipment\US\eqp\CUP_crocker\velka_polni\EOP_..."
;   [7140] "8"
;   [7148] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [7192] "G\Equipment\US\eqp\CUP_crocker\lehke_vybaveni\E..."
;   [7264] "G\Equipment\US\bes\EOP_e_glasses01.BES"
;   [7308] "G\Equipment\US\eqp\CUP_crocker\lehke_vybaveni\E..."
;   [7380] "G\Equipment\US\bes\EOP_e_medicbag01.BES"
;   [7424] "G\Equipment\US\eqp\CUP_crocker\lehke_vybaveni\E..."
;   [7496] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [7544] "G\Equipment\US\eqp\CUP_crocker\lehke_vybaveni\E..."
;   [7620] "G\Equipment\US\bes\EOP_hat4US_v01.BES"
;   [7660] " "
;   [7664] "G\Equipment\US\eqp\CUP_crocker\lehke_vybaveni\E..."
;   [7732] " "
;   [7740] "G\Equipment\US\bes\EOP_hat2US_v01.BES"
;   [7784] "G\Equipment\US\eqp\CUP_defort\velka_polni\EOP_h..."
;   [7852] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [7896] "G\Equipment\US\eqp\CUP_defort\velka_polni\EOP_e..."
;   [7964] "G\Equipment\US\bes\EOP_e_flashlight01.BES"
;   [8012] "G\Equipment\US\eqp\CUP_defort\velka_polni\EOP_e..."
;   [8084] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [8132] "G\Equipment\US\eqp\CUP_defort\velka_polni\EOP_e..."
;   [8200] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [8244] " "
;   [8248] "G\Equipment\US\eqp\CUP_defort\velka_polni\EOP_e..."
;   [8316] " "
;   [8320] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [8364] "("
;   [8368] "G\Equipment\US\eqp\CUP_defort\velka_polni\EOP_e..."
;   [8436] "("
;   [8444] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [8488] "G\Equipment\US\eqp\CUP_defort\lehke_vybaveni\EO..."
;   [8560] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [8608] "G\Equipment\US\eqp\CUP_defort\lehke_vybaveni\EO..."
;   [8680] "G\Equipment\US\bes\EOP_hat2US_v01.BES"
;   [8724] "G\Equipment\US\eqp\CUP_defort\lehke_vybaveni\EO..."
;   [8796] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [8844] "G\Equipment\US\eqp\CUP_hornster\velka_polni\EOP..."
;   [8916] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [8960] "G\Equipment\US\eqp\CUP_hornster\velka_polni\EOP..."
;   [9028] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [9072] "G\Equipment\US\eqp\CUP_hornster\velka_polni\EOP..."
;   [9140] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [9184] "G\Equipment\US\eqp\CUP_hornster\velka_polni\EOP..."
;   [9256] "G\Equipment\US\bes\EOP_e_flashlight01.BES"
;   [9300] " "
;   [9304] "G\Equipment\US\eqp\CUP_hornster\velka_polni\EOP..."
;   [9372] " "
;   [9376] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [9420] "("
;   [9424] "G\Equipment\US\eqp\CUP_hornster\velka_polni\EOP..."
;   [9492] "("
;   [9496] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [9540] "0"
;   [9544] "G\Equipment\US\eqp\CUP_hornster\velka_polni\EOP..."
;   [9612] "0"
;   [9616] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [9660] "8"
;   [9664] "G\Equipment\US\eqp\CUP_hornster\velka_polni\EOP..."
;   [9736] "8"
;   [9744] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [9788] "G\Equipment\US\eqp\CUP_hornster\lehke_vybaveni\..."
;   [9860] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [9908] "G\Equipment\US\eqp\CUP_hornster\lehke_vybaveni\..."
;   [9988] "G\Equipment\US\bes\EOP_hat3US_v02.BES"
;   [10032] "G\Equipment\US\eqp\CUP_nhut\velka_polni\EOP_hat..."
;   [10096] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [10140] "G\Equipment\US\eqp\CUP_nhut\velka_polni\EOP_e_b..."
;   [10204] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [10248] "G\Equipment\US\eqp\CUP_nhut\velka_polni\EOP_e_c..."
;   [10312] "G\Equipment\US\bes\EOP_e_flashlight01.BES"
;   [10360] "G\Equipment\US\eqp\CUP_nhut\velka_polni\EOP_e_f..."
;   [10428] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [10472] " "
;   [10476] "G\Equipment\US\eqp\CUP_nhut\velka_polni\EOP_e_l..."
;   [10540] " "
;   [10544] "G\Equipment\US\bes\EOP_e_maceta01.BES"
;   [10584] "("
;   [10588] "G\Equipment\US\eqp\CUP_nhut\velka_polni\EOP_e_m..."
;   [10648] "("
;   [10652] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [10696] "0"
;   [10700] "G\Equipment\US\eqp\CUP_nhut\velka_polni\EOP_e_p..."
;   [10764] "0"
;   [10772] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [10816] "G\Equipment\US\eqp\CUP_nhut\lehke_vybaveni\EOP_..."
;   [10884] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [10932] "G\Equipment\US\eqp\CUP_nhut\lehke_vybaveni\EOP_..."
;   [11004] "G\Equipment\US\bes\EOP_hat3US_v02.BES"
;   [11048] "G\Equipment\US\eqp\CUP_nhut\lehke_vybaveni\EOP_..."
;   [11120] "G\Equipment\US\bes\EOP_hat4US_v02.BES"
;   [11164] "G\Equipment\US\eqp\EOP_UH14PH05_01.eqp"
;   [11208] "G\Equipment\US\bes\EOP_e_ammoboxfp01.BES"
;   [11256] "G\Equipment\US\eqp\CUP_rosenfield\lehke_vybaven..."
;   [11332] "G\Equipment\US\bes\EOP_e_ammoboxfp01.BES"
;   [11380] "G\Equipment\US\eqp\CUP_rosenfield\lehke_vybaven..."
;   [11460] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [11504] "G\Equipment\US\eqp\CUP_rosenfield\lehke_vybaven..."
;   [11580] "G\Equipment\US\bes\EOP_e_faidpouch01.BES"
;   [11624] " "
;   [11628] "G\Equipment\US\eqp\CUP_rosenfield\lehke_vybaven..."
;   [11700] " "
;   [11704] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [11748] "("
;   [11752] "G\Equipment\US\eqp\CUP_rosenfield\lehke_vybaven..."
;   [11824] "("
;   [11832] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [11876] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni\..."
;   [11948] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [11992] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni\..."
;   [12064] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [12108] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni\..."
;   [12184] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [12232] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni\..."
;   [12308] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [12352] " "
;   [12356] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni\..."
;   [12428] " "
;   [12432] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [12476] "("
;   [12480] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni\..."
;   [12552] "("
;   [12556] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [12600] "0"
;   [12604] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni\..."
;   [12676] "0"
;   [12680] "G\Equipment\US\bes\EOP_hlmt1US_v03.BES"
;   [12720] "8"
;   [12724] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni\..."
;   [12792] "8"
;   [12800] "G\Equipment\US\bes\EOP_hat1US_v01.BES"
;   [12844] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni2..."
;   [12916] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [12960] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni2..."
;   [13032] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [13076] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni2..."
;   [13148] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [13192] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni2..."
;   [13268] "G\Equipment\US\bes\EOP_e_faidpouch01.BES"
;   [13312] " "
;   [13316] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni2..."
;   [13388] " "
;   [13392] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [13436] "("
;   [13440] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni2..."
;   [13512] "("
;   [13516] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [13560] "0"
;   [13564] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni2..."
;   [13636] "0"
;   [13640] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [13684] "8"
;   [13688] "G\Equipment\US\eqp\CUP_SFgncsldr01\velka_polni2..."
;   [13764] "8"
;   [13772] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [13816] "G\Equipment\US\eqp\CUP_SFgncsldr01\lehke_vybave..."
;   [13892] "G\Equipment\US\bes\EOP_e_faidpouch01.BES"
;   [13940] "G\Equipment\US\eqp\CUP_SFgncsldr01\lehke_vybave..."
;   [14016] "G\Equipment\US\bes\EOP_hat1US_v01.BES"
;   [14060] "G\Equipment\US\eqp\CUP_SFgncsldr01\lehke_vybave..."
;   [14140] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [14184] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni\..."
;   [14256] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [14300] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni\..."
;   [14372] "G\Equipment\US\bes\EOP_e_flashlight01.BES"
;   [14420] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni\..."
;   [14496] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [14544] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni\..."
;   [14620] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [14664] " "
;   [14668] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni\..."
;   [14740] " "
;   [14744] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [14788] "("
;   [14792] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni\..."
;   [14864] "("
;   [14868] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [14912] "0"
;   [14916] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni\..."
;   [14988] "0"
;   [14992] "G\Equipment\US\bes\EOP_hlmt1US_v01.BES"
;   [15032] "8"
;   [15036] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni\..."
;   [15104] "8"
;   [15112] "G\Equipment\US\bes\EOP_e_ammoboxfp01.BES"
;   [15160] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni2..."
;   [15236] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [15280] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni2..."
;   [15352] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [15396] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni2..."
;   [15468] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [15516] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni2..."
;   [15592] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [15636] " "
;   [15640] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni2..."
;   [15712] " "
;   [15716] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [15760] "("
;   [15764] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni2..."
;   [15840] "("
;   [15844] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [15888] "0"
;   [15892] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni2..."
;   [15964] "0"
;   [15968] "G\Equipment\US\bes\EOP_hat4US_v01.BES"
;   [16008] "8"
;   [16012] "G\Equipment\US\eqp\CUP_SFgncsldr02\velka_polni2..."
;   [16080] "8"
;   [16088] "G\Equipment\US\bes\EOP_e_ammoboxfp01.BES"
;   [16136] "G\Equipment\US\eqp\CUP_SFgncsldr02\lehke_vybave..."
;   [16212] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [16256] "G\Equipment\US\eqp\CUP_SFgncsldr02\lehke_vybave..."
;   [16332] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [16380] "G\Equipment\US\eqp\CUP_SFgncsldr02\lehke_vybave..."
;   [16460] "G\Equipment\US\bes\EOP_hat4US_v01.BES"
;   [16504] "G\Equipment\US\eqp\CUP_SFgncsldr02\lehke_vybave..."
;   [16584] "G\Equipment\US\bes\EOP_e_ammoboxfp01.BES"
;   [16632] "G\Equipment\US\eqp\CUP_LLDBsldr01\lehke_vybaven..."
;   [16708] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [16752] "G\Equipment\US\eqp\CUP_LLDBsldr01\lehke_vybaven..."
;   [16828] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [16876] "G\Equipment\US\eqp\CUP_LLDBsldr01\lehke_vybaven..."
;   [16952] "G\Equipment\US\bes\EOP_hat1US_v03.BES"
;   [16996] "G\Equipment\US\eqp\CUP_LLDBsldr01\lehke_vybaven..."
;   [17072] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [17116] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni\E..."
;   [17188] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [17232] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni\E..."
;   [17304] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [17352] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni\E..."
;   [17424] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [17472] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni\E..."
;   [17548] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [17592] " "
;   [17596] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni\E..."
;   [17668] " "
;   [17672] "G\Equipment\US\bes\EOP_e_maceta01.BES"
;   [17712] "("
;   [17716] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni\E..."
;   [17784] "("
;   [17788] "G\Equipment\US\bes\EOP_hlmt1US_v03.BES"
;   [17828] "0"
;   [17832] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni\E..."
;   [17900] "0"
;   [17908] "G\Equipment\US\bes\EOP_e_faidpouch01.BES"
;   [17956] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni2\..."
;   [18032] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [18076] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni2\..."
;   [18148] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [18192] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni2\..."
;   [18264] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [18312] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni2\..."
;   [18388] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [18432] " "
;   [18436] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni2\..."
;   [18508] " "
;   [18512] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [18556] "("
;   [18560] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni2\..."
;   [18632] "("
;   [18636] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [18680] "0"
;   [18684] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni2\..."
;   [18756] "0"
;   [18760] "G\Equipment\US\bes\EOP_hat6US_v01.BES"
;   [18800] "8"
;   [18804] "G\Equipment\US\eqp\CUP_LLDBsldr01\velka_polni2\..."
;   [18872] "8"
;   [18880] "G\Equipment\US\bes\EOP_hat3US_v03.BES"
;   [18924] "G\Equipment\US\eqp\CUP_LLDBsldr02\lehke_vybaven..."
;   [18996] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [19040] "G\Equipment\US\eqp\CUP_LLDBsldr02\lehke_vybaven..."
;   [19116] "G\Equipment\US\bes\EOP_e_faidpouch01.BES"
;   [19164] "G\Equipment\US\eqp\CUP_LLDBsldr02\lehke_vybaven..."
;   [19240] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [19288] "G\Equipment\US\eqp\CUP_LLDBsldr02\lehke_vybaven..."
;   [19368] "G\Equipment\US\bes\EOP_e_flashlight01.BES"
;   [19416] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni\E..."
;   [19492] "G\Equipment\US\bes\EOP_brt1US_v01.BES"
;   [19536] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni\E..."
;   [19608] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [19652] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni\E..."
;   [19724] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [19768] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni\E..."
;   [19840] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [19880] " "
;   [19884] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni\E..."
;   [19952] " "
;   [19956] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [20000] "("
;   [20004] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni\E..."
;   [20076] "("
;   [20080] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [20124] "0"
;   [20128] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni\E..."
;   [20200] "0"
;   [20208] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [20256] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni2\..."
;   [20332] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [20376] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni2\..."
;   [20448] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [20492] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni2\..."
;   [20564] "G\Equipment\US\bes\EOP_e_faidpouch01.BES"
;   [20612] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni2\..."
;   [20688] "G\Equipment\US\bes\EOP_e_knife01.BES"
;   [20728] " "
;   [20732] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni2\..."
;   [20800] " "
;   [20804] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [20848] "("
;   [20852] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni2\..."
;   [20924] "("
;   [20928] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [20972] "0"
;   [20976] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni2\..."
;   [21048] "0"
;   [21052] "G\Equipment\US\bes\EOP_hat2US_v02.BES"
;   [21092] "8"
;   [21096] "G\Equipment\US\eqp\CUP_LLDBsldr02\velka_polni2\..."
;   [21164] "8"
;   [21172] "G\Equipment\US\bes\EOP_e_flashlight01.BES"
;   [21220] "G\Equipment\US\eqp\CUP_CIDGsldr01\lehke_vybaven..."
;   [21296] "G\Equipment\US\bes\EOP_brt1US_v01.BES"
;   [21340] "G\Equipment\US\eqp\CUP_CIDGsldr01\lehke_vybaven..."
;   [21412] "G\Equipment\US\bes\EOP_e_ammoboxfp01.BES"
;   [21460] "G\Equipment\US\eqp\CUP_CIDGsldr01\lehke_vybaven..."
;   [21536] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [21580] "G\Equipment\US\eqp\CUP_CIDGsldr01\lehke_vybaven..."
;   [21656] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [21700] " "
;   [21704] "G\Equipment\US\eqp\CUP_CIDGsldr01\lehke_vybaven..."
;   [21776] " "
;   [21784] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [21828] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni\E..."
;   [21900] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [21944] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni\E..."
;   [22016] "G\Equipment\US\bes\EOP_e_faidpouch01.BES"
;   [22064] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni\E..."
;   [22136] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [22184] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni\E..."
;   [22256] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [22300] " "
;   [22304] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni\E..."
;   [22376] " "
;   [22380] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [22424] "("
;   [22428] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni\E..."
;   [22500] "("
;   [22504] "G\Equipment\US\bes\EOP_hat2US_v02.BES"
;   [22544] "0"
;   [22548] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni\E..."
;   [22616] "0"
;   [22624] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [22668] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni2\..."
;   [22740] "G\Equipment\US\bes\EOP_e_ammoboxfp01.BES"
;   [22788] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni2\..."
;   [22864] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [22908] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni2\..."
;   [22980] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [23024] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni2\..."
;   [23100] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [23144] " "
;   [23148] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni2\..."
;   [23220] " "
;   [23224] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [23268] "("
;   [23272] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni2\..."
;   [23344] "("
;   [23348] "G\Equipment\US\bes\EOP_hat3US_v02.BES"
;   [23388] "0"
;   [23392] "G\Equipment\US\eqp\CUP_CIDGsldr01\velka_polni2\..."
;   [23460] "0"
;   [23468] "G\Equipment\US\bes\EOP_hat4US_v02.BES"
;   [23512] "G\Equipment\US\eqp\CUP_CIDGsldr02\lehke_vybaven..."
;   [23584] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [23628] "G\Equipment\US\eqp\CUP_CIDGsldr02\lehke_vybaven..."
;   [23704] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [23752] "G\Equipment\US\eqp\CUP_CIDGsldr02\lehke_vybaven..."
;   [23828] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [23876] "G\Equipment\US\eqp\CUP_CIDGsldr02\lehke_vybaven..."
;   [23956] "G\Equipment\US\bes\EOP_e_knife01.BES"
;   [24000] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni\E..."
;   [24068] "G\Equipment\US\bes\EOP_e_bigbag01.BES"
;   [24112] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni\E..."
;   [24184] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [24228] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni\E..."
;   [24300] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [24348] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni\E..."
;   [24420] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [24464] " "
;   [24468] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni\E..."
;   [24540] " "
;   [24544] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [24588] "("
;   [24592] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni\E..."
;   [24664] "("
;   [24668] "G\Equipment\US\bes\EOP_hlmt1US_v02.BES"
;   [24708] "0"
;   [24712] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni\E..."
;   [24780] "0"
;   [24788] "G\Equipment\US\bes\EOP_e_ammoboxfp01.BES"
;   [24836] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni2\..."
;   [24912] "G\Equipment\US\bes\EOP_e_canteen01.BES"
;   [24956] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni2\..."
;   [25028] "G\Equipment\US\bes\EOP_e_littlebag01.BES"
;   [25076] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni2\..."
;   [25152] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [25200] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni2\..."
;   [25276] "G\Equipment\US\bes\EOP_e_m16ammobox01.BES"
;   [25320] " "
;   [25324] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni2\..."
;   [25396] " "
;   [25400] "G\Equipment\US\bes\EOP_e_pistolcase01.BES"
;   [25444] "("
;   [25448] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni2\..."
;   [25520] "("
;   [25524] "G\Equipment\US\bes\EOP_e_shovel01.BES"
;   [25564] "0"
;   [25568] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni2\..."
;   [25636] "0"
;   [25640] "G\Equipment\US\bes\EOP_hat1US_v02.BES"
;   [25680] "8"
;   [25684] "G\Equipment\US\eqp\CUP_CIDGsldr02\velka_polni2\..."
;   [25752] "8"
;   [25772] "P"
;   [25792] "ini\players\easy_camo.ini"
;   [25820] "ini\players\default_camo.ini"
;   [25852] "Ä	"
;   [25860] "7"
;   [25864] "f"
;   [25872] "ÿ"
;   [25892] "3"

; Code
; ----

_init:
  000: RET      0                    
  001: ASP      1                    
  002: ASP      1                    
  003: LCP      [sp-4]               
  004: ASP      1                    
  005: XCALL    $frnd(float)float     ; args=1
  006: LLD      [sp+1]               
  007: SSP      1                    
  008: LADR     [sp+0]               
  009: ASGN                          
  010: SSP      1                    
  011: LCP      [sp+0]               
  012: GCP      data[0]               ; = 0
  013: FLES                          
  014: JZ       label_0020           
  015: LCP      [sp+0]               
  016: FNEG                          
  017: LADR     [sp+0]               
  018: ASGN                          
  019: SSP      1                    
label_0020:
  020: LCP      [sp+0]               
  021: LLD      [sp-3]               
  022: RET      1                    
  023: LCP      [sp-3]               
  024: GCP      data[1]               ; = 16777216
  025: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  026: SSP      2                    
  027: LCP      [sp-3]               
  028: GCP      data[2]               ; = 65536
  029: XCALL    $SC_P_Ai_EnableShooting(unsignedlong,int)void ; args=2
  030: SSP      2                    
  031: LCP      [sp-3]               
  032: GCP      data[3]               ; = 256
  033: XCALL    $SC_P_Ai_EnableSituationUpdate(unsignedlong,int)void ; args=2
  034: SSP      2                    
  035: GCP      data[4]               ; = 1
  036: GADR     data[5]              
  037: LCP      [sp-3]               
  038: GCP      data[10]              ; = 65536
  039: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  040: SSP      3                    
  041: RET      0                    
  042: LCP      [sp-3]               
  043: GCP      data[11]              ; = 256
  044: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  045: SSP      2                    
  046: LCP      [sp-3]               
  047: GCP      data[12]              ; = 1
  048: XCALL    $SC_P_Ai_EnableShooting(unsignedlong,int)void ; args=2
  049: SSP      2                    
  050: LCP      [sp-3]               
  051: GCP      data[13]              ; = 50331648
  052: XCALL    $SC_P_Ai_EnableSituationUpdate(unsignedlong,int)void ; args=2
  053: SSP      2                    
  054: LCP      [sp-3]               
  055: XCALL    $SC_P_Ai_Stop(unsignedlong)void ; args=1
  056: SSP      1                    
  057: GCP      data[14]              ; = 196608
  058: GADR     data[15]             
  059: LCP      [sp-3]               
  060: GCP      data[20]  ; "Player %d enabled" ; "Player %d enabled"
  061: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  062: SSP      3                    
  063: RET      0                    
func_0064:
  064: LCP      [sp-5]               
  065: JZ       label_0067           
  066: JMP      label_0075           
label_0067:
  067: GCP      data[21]              ; = 1702453612
  068: GADR     data[22]             
  069: LCP      [sp-4]               
  070: LCP      [sp-3]               
  071: GCP      data[31]              ; = 1818386798
  072: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  073: SSP      4                    
  074: RET      0                    
label_0075:
  075: LCP      [sp-5]               
  076: LCP      [sp-4]               
  077: LCP      [sp-3]               
  078: XCALL    $SC_P_ScriptMessage(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  079: SSP      3                    
  080: RET      0                    
  081: ASP      1                    
  082: ASP      1                    
  083: GCP      data[32]              ; = 1701601889
  084: LCP      [sp-5]               
  085: LCP      [sp-4]               
  086: ASP      1                    
  087: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  088: LLD      [sp+1]               
  089: SSP      3                    
  090: ASP      1                    
  091: XCALL    $SC_P_Ai_GetSureEnemies(unsignedlong)unsignedlong ; args=1
  092: LLD      [sp+0]               
  093: SSP      1                    
  094: JZ       label_0098           
  095: GCP      data[33]              ; = 1684368482
  096: LLD      [sp-3]               
  097: RET      0                    
label_0098:
  098: ASP      1                    
  099: ASP      1                    
  100: GCP      data[34]              ; = 6579564
  101: LCP      [sp-5]               
  102: LCP      [sp-4]               
  103: ASP      1                    
  104: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  105: LLD      [sp+1]               
  106: SSP      3                    
  107: ASP      1                    
  108: XCALL    $SC_P_Ai_GetDanger(unsignedlong)float ; args=1
  109: LLD      [sp+0]               
  110: SSP      1                    
  111: GCP      data[35]              ; = 25701
  112: FGRE                          
  113: JZ       label_0117           
  114: GCP      data[36]              ; = 100
  115: LLD      [sp-3]               
  116: RET      0                    
label_0117:
  117: GCP      data[37]              ; = 50331648
  118: LLD      [sp-3]               
  119: RET      0                    
  120: ASP      1                    
  121: LCP      [sp-4]               
  122: ASP      1                    
  123: XCALL    $SC_P_Ai_GetSureEnemies(unsignedlong)unsignedlong ; args=1
  124: LLD      [sp+0]               
  125: SSP      1                    
  126: JZ       label_0130           
  127: GCP      data[38]              ; = 196608
  128: LLD      [sp-3]               
  129: RET      0                    
label_0130:
  130: ASP      1                    
  131: LCP      [sp-4]               
  132: ASP      1                    
  133: XCALL    $SC_P_Ai_GetDanger(unsignedlong)float ; args=1
  134: LLD      [sp+0]               
  135: SSP      1                    
  136: GCP      data[39]              ; = 768
  137: FGRE                          
  138: JZ       label_0142           
  139: GCP      data[40]              ; = 3
  140: LLD      [sp-3]               
  141: RET      0                    
label_0142:
  142: GCP      data[41]              ; = 0
  143: LLD      [sp-3]               
  144: RET      0                    
  145: ASP      32                   
  146: LADR     [sp+0]               
  147: GCP      data[42]              ; = 0
  148: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  149: SSP      2                    
  150: LCP      [sp-4]               
  151: LADR     [sp+0]               
  152: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  153: SSP      2                    
  154: LCP      [sp-3]               
  155: LADR     [sp+0]               
  156: PNT      76                   
  157: ASGN                          
  158: SSP      1                    
  159: LCP      [sp-4]               
  160: LADR     [sp+0]               
  161: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  162: SSP      2                    
  163: RET      32                   
  164: ASP      32                   
  165: LADR     [sp+0]               
  166: GCP      data[43]              ; = 0
  167: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  168: SSP      2                    
  169: LCP      [sp-4]               
  170: LADR     [sp+0]               
  171: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  172: SSP      2                    
  173: LCP      [sp-3]               
  174: LADR     [sp+0]               
  175: PNT      44                   
  176: ASGN                          
  177: SSP      1                    
  178: LCP      [sp-4]               
  179: LADR     [sp+0]               
  180: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  181: SSP      2                    
  182: RET      32                   
  183: ASP      32                   
  184: LADR     [sp+0]               
  185: GCP      data[44]              ; = 0
  186: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  187: SSP      2                    
  188: LCP      [sp-4]               
  189: LADR     [sp+0]               
  190: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  191: SSP      2                    
  192: LADR     [sp+0]               
  193: PNT      20                   
  194: DCP      4                    
  195: LCP      [sp-3]               
  196: FMUL                          
  197: LADR     [sp+0]               
  198: PNT      20                   
  199: ASGN                          
  200: SSP      1                    
  201: LCP      [sp-4]               
  202: LADR     [sp+0]               
  203: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  204: SSP      2                    
  205: RET      32                   
  206: ASP      32                   
  207: LADR     [sp+0]               
  208: GCP      data[45]              ; = 0
  209: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  210: SSP      2                    
  211: LCP      [sp-4]               
  212: LADR     [sp+0]               
  213: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  214: SSP      2                    
  215: LADR     [sp+0]               
  216: PNT      72                   
  217: DCP      4                    
  218: LCP      [sp-3]               
  219: FMUL                          
  220: LADR     [sp+0]               
  221: PNT      72                   
  222: ASGN                          
  223: SSP      1                    
  224: LCP      [sp-4]               
  225: LADR     [sp+0]               
  226: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  227: SSP      2                    
  228: RET      32                   
  229: ASP      32                   
  230: LADR     [sp+0]               
  231: GCP      data[46]              ; = 0
  232: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  233: SSP      2                    
  234: LCP      [sp-4]               
  235: LADR     [sp+0]               
  236: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  237: SSP      2                    
  238: LCP      [sp-3]               
  239: JZ       label_0246           
  240: GCP      data[47]              ; = 0
  241: LADR     [sp+0]               
  242: PNT      64                   
  243: ASGN                          
  244: SSP      1                    
  245: JMP      label_0251           
label_0246:
  246: GCP      data[48]              ; = 0
  247: LADR     [sp+0]               
  248: PNT      64                   
  249: ASGN                          
  250: SSP      1                    
label_0251:
  251: LCP      [sp-4]               
  252: LADR     [sp+0]               
  253: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  254: SSP      2                    
  255: RET      32                   
  256: ASP      32                   
  257: LADR     [sp+0]               
  258: GCP      data[49]              ; = 0
  259: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  260: SSP      2                    
  261: LCP      [sp-4]               
  262: LADR     [sp+0]               
  263: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  264: SSP      2                    
  265: LCP      [sp-3]               
  266: LADR     [sp+0]               
  267: PNT      100                  
  268: ASGN                          
  269: SSP      1                    
  270: LCP      [sp-4]               
  271: LADR     [sp+0]               
  272: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  273: SSP      2                    
  274: RET      32                   
  275: ASP      1                    
  276: GCP      data[50]              ; = 0
  277: ASP      1                    
  278: XCALL    $SC_ggi(unsignedlong)int ; args=1
  279: LLD      [sp+0]               
  280: SSP      1                    
  281: LLD      [sp-3]               
  282: RET      0                    
  283: ASP      1                    
  284: GCP      data[51]              ; = 0
  285: ASP      1                    
  286: XCALL    $SC_ggi(unsignedlong)int ; args=1
  287: LLD      [sp+0]               
  288: SSP      1                    
  289: LLD      [sp-3]               
  290: RET      0                    
  291: ASP      5                    
  292: LCP      [sp-4]               
  293: LADR     [sp+0]               
  294: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  295: SSP      2                    
  296: LADR     [sp+0]               
  297: DCP      4                    
  298: LLD      [sp-3]               
  299: RET      5                    
  300: ASP      32                   
  301: LADR     [sp+0]               
  302: GCP      data[52]              ; = 0
  303: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  304: SSP      2                    
  305: LCP      [sp-4]               
  306: LADR     [sp+0]               
  307: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  308: SSP      2                    
  309: LCP      [sp-3]               
  310: LADR     [sp+0]               
  311: ASGN                          
  312: SSP      1                    
  313: LCP      [sp-4]               
  314: LADR     [sp+0]               
  315: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  316: SSP      2                    
  317: RET      32                   
func_0318:
  318: ASP      1                    
  319: GCP      data[53]              ; = 50331648
  320: ASP      1                    
  321: XCALL    $SC_ggi(unsignedlong)int ; args=1
  322: LLD      [sp+0]               
  323: SSP      1                    
  324: LADR     [sp-3]               
  325: DADR     data[40]             
  326: ASGN                          
  327: SSP      1                    
  328: LADR     [sp-3]               
  329: DADR     data[40]             
  330: DCP      4                    
  331: JZ       label_0333           
  332: JMP      label_0338           
label_0333:
  333: GCP      data[54]              ; = 196608
  334: LADR     [sp-3]               
  335: DADR     data[40]             
  336: ASGN                          
  337: SSP      1                    
label_0338:
  338: LADR     [sp-3]               
  339: DADR     data[40]             
  340: DCP      4                    
  341: GCP      data[55]              ; = 768
  342: EQU                           
  343: JZ       label_0349           
  344: GCP      data[56]              ; = 3
  345: LADR     [sp-3]               
  346: DADR     data[40]             
  347: ASGN                          
  348: SSP      1                    
label_0349:
  349: ASP      1                    
  350: GCP      data[57]              ; = 1342177280
  351: ASP      1                    
  352: XCALL    $SC_ggi(unsignedlong)int ; args=1
  353: LLD      [sp+0]               
  354: SSP      1                    
  355: LADR     [sp-3]               
  356: DADR     data[44]             
  357: ASGN                          
  358: SSP      1                    
  359: LADR     [sp-3]               
  360: DADR     data[44]             
  361: DCP      4                    
  362: JZ       label_0364           
  363: JMP      label_0369           
label_0364:
  364: GCP      data[58]              ; = 1817182208
  365: LADR     [sp-3]               
  366: DADR     data[44]             
  367: ASGN                          
  368: SSP      1                    
label_0369:
  369: LADR     [sp-3]               
  370: DADR     data[44]             
  371: DCP      4                    
  372: GCP      data[59]              ; = 1634488320
  373: EQU                           
  374: JZ       label_0380           
  375: GCP      data[60]  ; "Player %d disabled" ; "Player %d disabled"
  376: LADR     [sp-3]               
  377: DADR     data[44]             
  378: ASGN                          
  379: SSP      1                    
label_0380:
  380: ASP      1                    
  381: GCP      data[61]              ; = 1702453612
  382: ASP      1                    
  383: XCALL    $SC_ggi(unsignedlong)int ; args=1
  384: LLD      [sp+0]               
  385: SSP      1                    
  386: LADR     [sp-3]               
  387: DADR     data[48]             
  388: ASGN                          
  389: SSP      1                    
  390: LADR     [sp-3]               
  391: DADR     data[48]             
  392: DCP      4                    
  393: JZ       label_0395           
  394: JMP      label_0430           
label_0395:
  395: ASP      1                    
  396: GCP      data[62]              ; = 1919252833
  397: ASP      1                    
  398: XCALL    $SC_ggi(unsignedlong)int ; args=1
  399: LLD      [sp+0]               
  400: SSP      1                    
  401: GCP      data[63]              ; = 544367993
  402: EQU                           
  403: JZ       label_0410           
  404: GCP      data[64]              ; = 622883429
  405: LADR     [sp-3]               
  406: DADR     data[48]             
  407: ASGN                          
  408: SSP      1                    
  409: JMP      label_0430           
label_0410:
  410: ASP      1                    
  411: GCP      data[65]              ; = 1680154738
  412: ASP      1                    
  413: XCALL    $SC_ggi(unsignedlong)int ; args=1
  414: LLD      [sp+0]               
  415: SSP      1                    
  416: GCP      data[66]              ; = 543434016
  417: LES                           
  418: JZ       label_0425           
  419: GCP      data[67]              ; = 1679844389
  420: LADR     [sp-3]               
  421: DADR     data[48]             
  422: ASGN                          
  423: SSP      1                    
  424: JMP      label_0430           
label_0425:
  425: GCP      data[68]              ; = 1768169572
  426: LADR     [sp-3]               
  427: DADR     data[48]             
  428: ASGN                          
  429: SSP      1                    
label_0430:
  430: LADR     [sp-3]               
  431: DADR     data[48]             
  432: DCP      4                    
  433: GCP      data[69]              ; = 1936286752
  434: EQU                           
  435: JZ       label_0441           
  436: GCP      data[70]              ; = 1634953572
  437: LADR     [sp-3]               
  438: DADR     data[48]             
  439: ASGN                          
  440: SSP      1                    
label_0441:
  441: ASP      1                    
  442: GCP      data[71]              ; = 1650553705
  443: ASP      1                    
  444: XCALL    $SC_ggi(unsignedlong)int ; args=1
  445: LLD      [sp+0]               
  446: SSP      1                    
  447: LADR     [sp-3]               
  448: DADR     data[52]             
  449: ASGN                          
  450: SSP      1                    
  451: LADR     [sp-3]               
  452: DADR     data[52]             
  453: DCP      4                    
  454: GCP      data[72]              ; = 1818386803
  455: EQU                           
  456: JZ       label_0462           
  457: GCP      data[73]              ; = 1701601889
  458: LADR     [sp-3]               
  459: DADR     data[52]             
  460: ASGN                          
  461: SSP      1                    
label_0462:
  462: ASP      1                    
  463: GCP      data[74]              ; = 1684368482
  464: ASP      1                    
  465: XCALL    $SC_ggi(unsignedlong)int ; args=1
  466: LLD      [sp+0]               
  467: SSP      1                    
  468: LADR     [sp-3]               
  469: DADR     data[56]             
  470: ASGN                          
  471: SSP      1                    
  472: LADR     [sp-3]               
  473: DADR     data[56]             
  474: DCP      4                    
  475: JZ       label_0477           
  476: JMP      label_0482           
label_0477:
  477: GCP      data[75]              ; = 6579564
  478: LADR     [sp-3]               
  479: DADR     data[56]             
  480: ASGN                          
  481: SSP      1                    
label_0482:
  482: LADR     [sp-3]               
  483: DADR     data[56]             
  484: DCP      4                    
  485: GCP      data[76]              ; = 25701
  486: EQU                           
  487: JZ       label_0493           
  488: GCP      data[77]              ; = 50331748
  489: LADR     [sp-3]               
  490: DADR     data[56]             
  491: ASGN                          
  492: SSP      1                    
label_0493:
  493: ASP      1                    
  494: GCP      data[78]              ; = 196608
  495: ASP      1                    
  496: XCALL    $SC_ggi(unsignedlong)int ; args=1
  497: LLD      [sp+0]               
  498: SSP      1                    
  499: LADR     [sp-3]               
  500: DADR     data[60]  ; "Player %d disabled"
  501: ASGN                          
  502: SSP      1                    
  503: LADR     [sp-3]               
  504: DADR     data[60]  ; "Player %d disabled"
  505: DCP      4                    
  506: GCP      data[79]              ; = 768
  507: EQU                           
  508: JZ       label_0514           
  509: GCP      data[80]              ; = 3
  510: LADR     [sp-3]               
  511: DADR     data[60]  ; "Player %d disabled"
  512: ASGN                          
  513: SSP      1                    
label_0514:
  514: ASP      1                    
  515: GCP      data[81]              ; = 50331648
  516: ASP      1                    
  517: XCALL    $SC_ggi(unsignedlong)int ; args=1
  518: LLD      [sp+0]               
  519: SSP      1                    
  520: LADR     [sp-3]               
  521: DADR     data[64]             
  522: ASGN                          
  523: SSP      1                    
  524: LADR     [sp-3]               
  525: DADR     data[64]             
  526: DCP      4                    
  527: GCP      data[82]              ; = 196608
  528: EQU                           
  529: JZ       label_0535           
  530: GCP      data[83]              ; = 768
  531: LADR     [sp-3]               
  532: DADR     data[64]             
  533: ASGN                          
  534: SSP      1                    
label_0535:
  535: ASP      1                    
  536: GCP      data[84]              ; = 3
  537: ASP      1                    
  538: XCALL    $SC_ggi(unsignedlong)int ; args=1
  539: LLD      [sp+0]               
  540: SSP      1                    
  541: LADR     [sp-3]               
  542: DADR     data[68]             
  543: ASGN                          
  544: SSP      1                    
  545: LADR     [sp-3]               
  546: DADR     data[68]             
  547: DCP      4                    
  548: JZ       label_0550           
  549: JMP      label_0555           
label_0550:
  550: GCP      data[85]              ; = 1291845632
  551: LADR     [sp-3]               
  552: DADR     data[68]             
  553: ASGN                          
  554: SSP      1                    
label_0555:
  555: LADR     [sp-3]               
  556: DADR     data[68]             
  557: DCP      4                    
  558: GCP      data[86]              ; = 1699545088
  559: EQU                           
  560: JZ       label_0566           
  561: GCP      data[87]              ; = 1936018688
  562: LADR     [sp-3]               
  563: DADR     data[68]             
  564: ASGN                          
  565: SSP      1                    
label_0566:
  566: ASP      1                    
  567: GCP      data[88]  ; "Message %d %d to unexisted player!" ; "Message %d %d to unexisted pla"
  568: ASP      1                    
  569: XCALL    $SC_ggi(unsignedlong)int ; args=1
  570: LLD      [sp+0]               
  571: SSP      1                    
  572: LADR     [sp-3]               
  573: DADR     data[72]             
  574: ASGN                          
  575: SSP      1                    
  576: LADR     [sp-3]               
  577: DADR     data[72]             
  578: DCP      4                    
  579: GCP      data[89]              ; = 1634956133
  580: EQU                           
  581: JZ       label_0587           
  582: GCP      data[90]              ; = 1734439795
  583: LADR     [sp-3]               
  584: DADR     data[72]             
  585: ASGN                          
  586: SSP      1                    
label_0587:
  587: GCP      data[91]              ; = 1701273971
  588: LADR     [sp-3]               
  589: DADR     data[76]             
  590: ASGN                          
  591: SSP      1                    
  592: RET      0                    
func_0593:
  593: ASP      39                   
  594: ASP      1                    
  595: ASP      1                    
  596: ASP      1                    
  597: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  598: LLD      [sp+40]              
  599: LADR     [sp+0]               
  600: ASP      1                    
  601: XCALL    $SC_P_GetWeapons(unsignedlong,*s_SC_P_Create)int ; args=2
  602: LLD      [sp+39]              
  603: SSP      2                    
  604: SSP      1                    
  605: LADR     [sp+0]               
  606: PNT      40                   
  607: DCP      4                    
  608: JZ       label_0616           
  609: GCP      data[92]              ; = 543516513
  610: LADR     [sp+0]               
  611: PNT      40                   
  612: DCP      4                    
  613: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  614: SSP      2                    
  615: JMP      label_0620           
label_0616:
  616: GCP      data[93]              ; = 622880103
  617: GCP      data[94]              ; = 1680154725
  618: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  619: SSP      2                    
label_0620:
  620: LADR     [sp+0]               
  621: PNT      44                   
  622: DCP      4                    
  623: JZ       label_0631           
  624: GCP      data[95]              ; = 543434016
  625: LADR     [sp+0]               
  626: PNT      44                   
  627: DCP      4                    
  628: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  629: SSP      2                    
  630: JMP      label_0635           
label_0631:
  631: GCP      data[96]              ; = 622879781
  632: GCP      data[97]              ; = 1680154724
  633: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  634: SSP      2                    
label_0635:
  635: LADR     [sp+0]               
  636: PNT      48                   
  637: DCP      4                    
  638: JZ       label_0646           
  639: GCP      data[98]              ; = 543434016
  640: LADR     [sp+0]               
  641: PNT      48                   
  642: DCP      4                    
  643: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  644: SSP      2                    
  645: JMP      label_0650           
label_0646:
  646: GCP      data[99]              ; = 1948279845
  647: GCP      data[100]             ; = 1869881444
  648: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  649: SSP      2                    
label_0650:
  650: LADR     [sp+0]               
  651: PNT      52                   
  652: DCP      4                    
  653: JZ       label_0661           
  654: GCP      data[101]             ; = 544175136
  655: LADR     [sp+0]               
  656: PNT      52                   
  657: DCP      4                    
  658: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  659: SSP      2                    
  660: JMP      label_0665           
label_0661:
  661: GCP      data[102]             ; = 1965059956
  662: GCP      data[103]             ; = 1853169775
  663: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  664: SSP      2                    
label_0665:
  665: LADR     [sp+0]               
  666: PNT      56                   
  667: DCP      4                    
  668: JZ       label_0676           
  669: GCP      data[104]             ; = 1701737760
  670: LADR     [sp+0]               
  671: PNT      56                   
  672: DCP      4                    
  673: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  674: SSP      2                    
  675: JMP      label_0680           
label_0676:
  676: GCP      data[105]             ; = 2019913333
  677: GCP      data[106]             ; = 1769497966
  678: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  679: SSP      2                    
label_0680:
  680: LADR     [sp+0]               
  681: PNT      60                   
  682: DCP      4                    
  683: JZ       label_0691           
  684: GCP      data[107]             ; = 1936291941
  685: LADR     [sp+0]               
  686: PNT      60                   
  687: DCP      4                    
  688: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  689: SSP      2                    
  690: JMP      label_0695           
label_0691:
  691: GCP      data[108]             ; = 1953720696
  692: GCP      data[109]             ; = 1702130537
  693: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  694: SSP      2                    
label_0695:
  695: LADR     [sp+0]               
  696: PNT      64                   
  697: DCP      4                    
  698: JZ       label_0706           
  699: GCP      data[110]             ; = 1684370547
  700: LADR     [sp+0]               
  701: PNT      64                   
  702: DCP      4                    
  703: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  704: SSP      2                    
  705: JMP      label_0710           
label_0706:
  706: GCP      data[111]             ; = 543450484
  707: GCP      data[112]             ; = 1881171045
  708: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  709: SSP      2                    
label_0710:
  710: LADR     [sp+0]               
  711: PNT      68                   
  712: DCP      4                    
  713: JZ       label_0721           
  714: GCP      data[113]             ; = 1819287652
  715: LADR     [sp+0]               
  716: PNT      68                   
  717: DCP      4                    
  718: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  719: SSP      2                    
  720: JMP      label_0725           
label_0721:
  721: GCP      data[114]             ; = 1634496544
  722: GCP      data[115]             ; = 2036427888
  723: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  724: SSP      2                    
label_0725:
  725: LADR     [sp+0]               
  726: PNT      72                   
  727: DCP      4                    
  728: JZ       label_0736           
  729: GCP      data[116]             ; = 1702453612
  730: LADR     [sp+0]               
  731: PNT      72                   
  732: DCP      4                    
  733: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  734: SSP      2                    
  735: JMP      label_0740           
label_0736:
  736: GCP      data[117]             ; = 1919252833
  737: GCP      data[118]             ; = 561145209
  738: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  739: SSP      2                    
label_0740:
  740: LADR     [sp+0]               
  741: PNT      76                   
  742: DCP      4                    
  743: JZ       label_0751           
  744: GCP      data[119]             ; = 2191973
  745: LADR     [sp+0]               
  746: PNT      76                   
  747: DCP      4                    
  748: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  749: SSP      2                    
  750: JMP      label_0755           
label_0751:
  751: GCP      data[120]             ; = 8562
  752: GCP      data[121]             ; = 67108897
  753: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  754: SSP      2                    
label_0755:
  755: RET      39                   
func_0756:
  756: ASP      1                    
  757: ASP      1                    
  758: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  759: LLD      [sp+0]               
  760: GCP      data[122]             ; = 262144
  761: XCALL    $SC_P_ReadHealthFromGlobalVar(unsignedlong,unsignedlong)void ; args=2
  762: SSP      2                    
  763: RET      0                    
func_0764:
  764: ASP      1                    
  765: ASP      1                    
  766: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  767: LLD      [sp+0]               
  768: GCP      data[123]             ; = 1024
  769: XCALL    $SC_P_WriteHealthToGlobalVar(unsignedlong,unsignedlong)void ; args=2
  770: SSP      2                    
  771: RET      0                    
func_0772:
  772: ASP      1                    
  773: ASP      1                    
  774: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  775: LLD      [sp+0]               
  776: GCP      data[124]             ; = 4
  777: GCP      data[125]             ; = 16777216
  778: XCALL    $SC_P_ReadAmmoFromGlobalVar(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  779: SSP      3                    
  780: ASP      1                    
  781: GCP      data[126]             ; = 65536
  782: ASP      1                    
  783: XCALL    $SC_ggi(unsignedlong)int ; args=1
  784: LLD      [sp+0]               
  785: SSP      1                    
  786: JZ       label_0800           
  787: ASP      1                    
  788: ASP      1                    
  789: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  790: LLD      [sp+0]               
  791: GCP      data[127]             ; = 256
  792: ASP      1                    
  793: GCP      data[128]             ; = 1
  794: ASP      1                    
  795: XCALL    $SC_ggi(unsignedlong)int ; args=1
  796: LLD      [sp+2]               
  797: SSP      1                    
  798: XCALL    $SC_P_SetAmmoInWeap(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  799: SSP      3                    
label_0800:
  800: ASP      1                    
  801: GCP      data[129]             ; = 16777216
  802: ASP      1                    
  803: XCALL    $SC_ggi(unsignedlong)int ; args=1
  804: LLD      [sp+0]               
  805: SSP      1                    
  806: JZ       label_0820           
  807: ASP      1                    
  808: ASP      1                    
  809: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  810: LLD      [sp+0]               
  811: GCP      data[130]             ; = 65536
  812: ASP      1                    
  813: GCP      data[131]             ; = 256
  814: ASP      1                    
  815: XCALL    $SC_ggi(unsignedlong)int ; args=1
  816: LLD      [sp+2]               
  817: SSP      1                    
  818: XCALL    $SC_P_SetAmmoInWeap(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  819: SSP      3                    
label_0820:
  820: RET      0                    
func_0821:
  821: ASP      1                    
  822: ASP      1                    
  823: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  824: LLD      [sp+0]               
  825: GCP      data[132]             ; = 1
  826: GCP      data[133]             ; = 16777216
  827: XCALL    $SC_P_WriteAmmoToGlobalVar(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  828: SSP      3                    
  829: GCP      data[134]             ; = 65536
  830: ASP      1                    
  831: ASP      1                    
  832: ASP      1                    
  833: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  834: LLD      [sp+2]               
  835: GCP      data[135]             ; = 256
  836: ASP      1                    
  837: XCALL    $SC_P_GetAmmoInWeap(unsignedlong,unsignedlong)unsignedlong ; args=2
  838: LLD      [sp+1]               
  839: SSP      2                    
  840: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  841: SSP      2                    
  842: GCP      data[136]             ; = 1
  843: ASP      1                    
  844: ASP      1                    
  845: ASP      1                    
  846: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  847: LLD      [sp+2]               
  848: GCP      data[137]             ; = 0
  849: ASP      1                    
  850: XCALL    $SC_P_GetAmmoInWeap(unsignedlong,unsignedlong)unsignedlong ; args=2
  851: LLD      [sp+1]               
  852: SSP      2                    
  853: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  854: SSP      2                    
  855: RET      0                    
func_0856:
  856: ASP      10                   
  857: ASP      1                    
  858: LADR     [sp+0]               
  859: XCALL    $SC_PC_GetIntel(*s_SC_P_intel)void ; args=1
  860: SSP      1                    
  861: GCP      data[138]             ; = 0
  862: LADR     [sp+10]              
  863: ASGN                          
  864: SSP      1                    
label_0865:
  865: LCP      [sp+10]              
  866: GCP      data[139]             ; = 0
  867: LES                           
  868: JZ       label_0889           
  869: GCP      data[140]             ; = 1056964608
  870: LCP      [sp+10]              
  871: ADD                           
  872: LADR     [sp+0]               
  873: LCP      [sp+10]              
  874: GCP      data[141]             ; = 20905984
  875: MUL                           
  876: ADD                           
  877: DCP      4                    
  878: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  879: SSP      2                    
  880: LCP      [sp+10]              
  881: LCP      [sp+10]              
  882: GCP      data[142]             ; = 81664
  883: ADD                           
  884: LADR     [sp+10]              
  885: ASGN                          
  886: SSP      1                    
  887: SSP      1                    
  888: JMP      label_0865           
label_0889:
  889: RET      11                   
  890: ASP      10                   
  891: ASP      1                    
  892: GCP      data[143]             ; = 319
  893: LADR     [sp+10]              
  894: ASGN                          
  895: SSP      1                    
label_0896:
  896: LCP      [sp+10]              
  897: GCP      data[144]             ; = 1
  898: LES                           
  899: JZ       label_0924           
  900: ASP      1                    
  901: GCP      data[145]             ; = 0
  902: LCP      [sp+10]              
  903: ADD                           
  904: ASP      1                    
  905: XCALL    $SC_ggi(unsignedlong)int ; args=1
  906: LLD      [sp+11]              
  907: SSP      1                    
  908: LADR     [sp+0]               
  909: LCP      [sp+10]              
  910: GCP      data[146]             ; = 0
  911: MUL                           
  912: ADD                           
  913: ASGN                          
  914: SSP      1                    
  915: LCP      [sp+10]              
  916: LCP      [sp+10]              
  917: GCP      data[147]             ; = 0
  918: ADD                           
  919: LADR     [sp+10]              
  920: ASGN                          
  921: SSP      1                    
  922: SSP      1                    
  923: JMP      label_0896           
label_0924:
  924: LADR     [sp+0]               
  925: XCALL    $SC_PC_SetIntel(*s_SC_P_intel)void ; args=1
  926: SSP      1                    
  927: RET      11                   
  928: CALL     func_0593            
  929: CALL     func_0821            
  930: CALL     func_0764            
  931: XCALL    $SC_MissionCompleted(void)void ; args=0
  932: RET      0                    
  933: CALL     func_0856            
  934: CALL     func_0593            
  935: CALL     func_0821            
  936: CALL     func_0764            
  937: GADR     data[148]            
  938: GCP      data[153]             ; = 0
  939: XCALL    $SC_Osi(*char,...)void ; args=4294967295
  940: SSP      1                    
  941: XCALL    $SC_MissionDone(void)void ; args=0
  942: RET      0                    
  943: LADR     [sp-3]               
  944: GCP      data[154]             ; = 0
  945: GCP      data[155]             ; = 0
  946: XCALL    $SC_ShowHelp(*unsignedlong,unsignedlong,float)void ; args=3
  947: SSP      3                    
  948: RET      0                    
  949: ASP      2                    
  950: LCP      [sp-4]               
  951: LADR     [sp+0]               
  952: GCP      data[156]             ; = 1056964608
  953: ADD                           
  954: ASGN                          
  955: SSP      1                    
  956: LCP      [sp-3]               
  957: LADR     [sp+0]               
  958: GCP      data[157]             ; = 20905984
  959: ADD                           
  960: ASGN                          
  961: SSP      1                    
  962: LADR     [sp+0]               
  963: GCP      data[158]             ; = 81664
  964: GCP      data[159]             ; = 319
  965: XCALL    $SC_ShowHelp(*unsignedlong,unsignedlong,float)void ; args=3
  966: SSP      3                    
  967: RET      2                    
  968: ASP      3                    
  969: LCP      [sp-5]               
  970: LADR     [sp+0]               
  971: GCP      data[160]             ; = 1
  972: ADD                           
  973: ASGN                          
  974: SSP      1                    
  975: LCP      [sp-4]               
  976: LADR     [sp+0]               
  977: GCP      data[161]             ; = 0
  978: ADD                           
  979: ASGN                          
  980: SSP      1                    
  981: LCP      [sp-3]               
  982: LADR     [sp+0]               
  983: GCP      data[162]             ; = 0
  984: ADD                           
  985: ASGN                          
  986: SSP      1                    
  987: LADR     [sp+0]               
  988: GCP      data[163]             ; = 0
  989: GCP      data[164]             ; = 0
  990: XCALL    $SC_ShowHelp(*unsignedlong,unsignedlong,float)void ; args=3
  991: SSP      3                    
  992: RET      3                    
func_0993:
  993: ASP      1                    
  994: GCP      data[165]             ; = 2147483648
  995: ASP      1                    
  996: XCALL    $SC_ggi(unsignedlong)int ; args=1
  997: LLD      [sp+0]               
  998: SSP      1                    
  999: LLD      [sp-3]               
  1000: RET      0                    
  1001: ASP      1                    
  1002: ASP      1                    
  1003: ASP      1                    
  1004: XCALL    $rand(void)int        ; args=0
  1005: LLD      [sp+1]               
  1006: GCP      data[166]             ; = 8388608
  1007: MOD                           
  1008: LADR     [sp+0]               
  1009: ASGN                          
  1010: SSP      1                    
  1011: ASP      1                    
  1012: GCP      data[167]             ; = 32768
  1013: ASP      1                    
  1014: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1015: LLD      [sp+1]               
  1016: SSP      1                    
  1017: GCP      data[168]             ; = 128
  1018: GRE                           
  1019: JZ       label_1066           
  1020: LCP      [sp+0]               
  1021: GCP      data[169]             ; = 2147483648
  1022: GRE                           
  1023: JZ       label_1027           
  1024: GCP      data[170]             ; = 8388608
  1025: LLD      [sp-3]               
  1026: RET      1                    
label_1027:
  1027: LCP      [sp+0]               
  1028: GCP      data[171]             ; = 32768
  1029: GRE                           
  1030: JZ       label_1034           
  1031: GCP      data[172]             ; = 128
  1032: LLD      [sp-3]               
  1033: RET      1                    
label_1034:
  1034: LCP      [sp+0]               
  1035: GCP      data[173]             ; = 2147483648
  1036: GRE                           
  1037: JZ       label_1041           
  1038: GCP      data[174]             ; = 8388608
  1039: LLD      [sp-3]               
  1040: RET      1                    
label_1041:
  1041: LCP      [sp+0]               
  1042: GCP      data[175]             ; = 32768
  1043: GRE                           
  1044: JZ       label_1048           
  1045: GCP      data[176]             ; = 128
  1046: LLD      [sp-3]               
  1047: RET      1                    
label_1048:
  1048: LCP      [sp+0]               
  1049: GCP      data[177]             ; = 2147483648
  1050: GRE                           
  1051: JZ       label_1055           
  1052: GCP      data[178]             ; = 8388608
  1053: LLD      [sp-3]               
  1054: RET      1                    
label_1055:
  1055: LCP      [sp+0]               
  1056: GCP      data[179]             ; = 32768
  1057: GRE                           
  1058: JZ       label_1062           
  1059: GCP      data[180]             ; = 128
  1060: LLD      [sp-3]               
  1061: RET      1                    
label_1062:
  1062: GCP      data[181]             ; = 2147483648
  1063: LLD      [sp-3]               
  1064: RET      1                    
  1065: JMP      label_1111           
label_1066:
  1066: LCP      [sp+0]               
  1067: GCP      data[182]             ; = 8388608
  1068: GRE                           
  1069: JZ       label_1073           
  1070: GCP      data[183]             ; = 32768
  1071: LLD      [sp-3]               
  1072: RET      1                    
label_1073:
  1073: LCP      [sp+0]               
  1074: GCP      data[184]             ; = 128
  1075: GRE                           
  1076: JZ       label_1080           
  1077: GCP      data[185]             ; = 0
  1078: LLD      [sp-3]               
  1079: RET      1                    
label_1080:
  1080: LCP      [sp+0]               
  1081: GCP      data[186]             ; = 0
  1082: GRE                           
  1083: JZ       label_1087           
  1084: GCP      data[187]             ; = 2684354560
  1085: LLD      [sp-3]               
  1086: RET      1                    
label_1087:
  1087: LCP      [sp+0]               
  1088: GCP      data[188]             ; = 1084227584
  1089: GRE                           
  1090: JZ       label_1094           
  1091: GCP      data[189]             ; = 4235264
  1092: LLD      [sp-3]               
  1093: RET      1                    
label_1094:
  1094: LCP      [sp+0]               
  1095: GCP      data[190]             ; = 16544
  1096: GRE                           
  1097: JZ       label_1101           
  1098: GCP      data[191]             ; = 2046820416
  1099: LLD      [sp-3]               
  1100: RET      1                    
label_1101:
  1101: LCP      [sp+0]               
  1102: GCP      data[192]             ; = 1148846080
  1103: GRE                           
  1104: JZ       label_1108           
  1105: GCP      data[193]             ; = 2151971328
  1106: LLD      [sp-3]               
  1107: RET      1                    
label_1108:
  1108: GCP      data[194]             ; = 8406138
  1109: LLD      [sp-3]               
  1110: RET      1                    
label_1111:
  1111: ASP      1                    
  1112: ASP      1                    
  1113: ASP      1                    
  1114: XCALL    $rand(void)int        ; args=0
  1115: LLD      [sp+1]               
  1116: GCP      data[195]             ; = 32836
  1117: MOD                           
  1118: LADR     [sp+0]               
  1119: ASGN                          
  1120: SSP      1                    
  1121: LCP      [sp+0]               
  1122: GCP      data[196]             ; = 128
  1123: GRE                           
  1124: JZ       label_1128           
  1125: GCP      data[197]             ; = 3355443200
  1126: LLD      [sp-3]               
  1127: RET      1                    
label_1128:
  1128: LCP      [sp+0]               
  1129: GCP      data[198]             ; = 13107200
  1130: GRE                           
  1131: JZ       label_1135           
  1132: GCP      data[199]             ; = 51200
  1133: LLD      [sp-3]               
  1134: RET      1                    
label_1135:
  1135: LCP      [sp+0]               
  1136: GCP      data[200]  ; "È"      ; "È"
  1137: GRE                           
  1138: JZ       label_1142           
  1139: GCP      data[201]             ; = 117440512
  1140: LLD      [sp-3]               
  1141: RET      1                    
label_1142:
  1142: LCP      [sp+0]               
  1143: GCP      data[202]             ; = 458752
  1144: GRE                           
  1145: JZ       label_1149           
  1146: GCP      data[203]             ; = 1792
  1147: LLD      [sp-3]               
  1148: RET      1                    
label_1149:
  1149: GCP      data[204]             ; = 7
  1150: LLD      [sp-3]               
  1151: RET      1                    
  1152: ASP      1                    
  1153: ASP      1                    
  1154: ASP      1                    
  1155: XCALL    $rand(void)int        ; args=0
  1156: LLD      [sp+1]               
  1157: GCP      data[205]             ; = 2147483648
  1158: MOD                           
  1159: LADR     [sp+0]               
  1160: ASGN                          
  1161: SSP      1                    
  1162: ASP      1                    
  1163: GCP      data[206]             ; = 8388608
  1164: ASP      1                    
  1165: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1166: LLD      [sp+1]               
  1167: SSP      1                    
  1168: JMP      label_1170           
  1169: JMP      label_1174           
label_1170:
  1170: LCP      [sp+1]               
  1171: GCP      data[207]             ; = 32768
  1172: EQU                           
  1173: JZ       label_1186           
label_1174:
  1174: LCP      [sp+0]               
  1175: GCP      data[208]             ; = 128
  1176: GRE                           
  1177: JZ       label_1181           
  1178: GCP      data[209]             ; = 1694498816
  1179: LLD      [sp-3]               
  1180: RET      2                    
label_1181:
  1181: GCP      data[210]             ; = 6619136
  1182: LLD      [sp-3]               
  1183: RET      2                    
  1184: JMP      label_1721           
  1185: JMP      label_1190           
label_1186:
  1186: LCP      [sp+1]               
  1187: GCP      data[211]             ; = 25856
  1188: EQU                           
  1189: JZ       label_1191           
label_1190:
  1190: JMP      label_1195           
label_1191:
  1191: LCP      [sp+1]               
  1192: GCP      data[212]  ; "e"      ; "e"
  1193: EQU                           
  1194: JZ       label_1196           
label_1195:
  1195: JMP      label_1200           
label_1196:
  1196: LCP      [sp+1]               
  1197: GCP      data[213]             ; = 486539264
  1198: EQU                           
  1199: JZ       label_1201           
label_1200:
  1200: JMP      label_1205           
label_1201:
  1201: LCP      [sp+1]               
  1202: GCP      data[214]             ; = 1900544
  1203: EQU                           
  1204: JZ       label_1224           
label_1205:
  1205: LCP      [sp+0]               
  1206: GCP      data[215]             ; = 7424
  1207: GRE                           
  1208: JZ       label_1212           
  1209: GCP      data[216]             ; = 29
  1210: LLD      [sp-3]               
  1211: RET      2                    
label_1212:
  1212: LCP      [sp+0]               
  1213: GCP      data[217]             ; = 4278190080
  1214: GRE                           
  1215: JZ       label_1219           
  1216: GCP      data[218]             ; = 16711680
  1217: LLD      [sp-3]               
  1218: RET      2                    
label_1219:
  1219: GCP      data[219]             ; = 65280
  1220: LLD      [sp-3]               
  1221: RET      2                    
  1222: JMP      label_1721           
  1223: JMP      label_1228           
label_1224:
  1224: LCP      [sp+1]               
  1225: GCP      data[220]  ; "ÿ"      ; "ÿ"
  1226: EQU                           
  1227: JZ       label_1229           
label_1228:
  1228: JMP      label_1233           
label_1229:
  1229: LCP      [sp+1]               
  1230: GCP      data[221]             ; = 0
  1231: EQU                           
  1232: JZ       label_1259           
label_1233:
  1233: LCP      [sp+0]               
  1234: GCP      data[222]             ; = 0
  1235: GRE                           
  1236: JZ       label_1240           
  1237: GCP      data[223]             ; = 0
  1238: LLD      [sp-3]               
  1239: RET      2                    
label_1240:
  1240: LCP      [sp+0]               
  1241: GCP      data[224]             ; = 0
  1242: GRE                           
  1243: JZ       label_1247           
  1244: GCP      data[225]             ; = 1711276032
  1245: LLD      [sp-3]               
  1246: RET      2                    
label_1247:
  1247: LCP      [sp+0]               
  1248: GCP      data[226]             ; = 6684672
  1249: GRE                           
  1250: JZ       label_1254           
  1251: GCP      data[227]             ; = 26112
  1252: LLD      [sp-3]               
  1253: RET      2                    
label_1254:
  1254: GCP      data[228]  ; "f"      ; "f"
  1255: LLD      [sp-3]               
  1256: RET      2                    
  1257: JMP      label_1721           
  1258: JMP      label_1263           
label_1259:
  1259: LCP      [sp+1]               
  1260: GCP      data[229]             ; = 117440512
  1261: EQU                           
  1262: JZ       label_1296           
label_1263:
  1263: LCP      [sp+0]               
  1264: GCP      data[230]             ; = 458752
  1265: GRE                           
  1266: JZ       label_1270           
  1267: GCP      data[231]             ; = 1792
  1268: LLD      [sp-3]               
  1269: RET      2                    
label_1270:
  1270: LCP      [sp+0]               
  1271: GCP      data[232]             ; = 7
  1272: GRE                           
  1273: JZ       label_1277           
  1274: GCP      data[233]             ; = 4278190080
  1275: LLD      [sp-3]               
  1276: RET      2                    
label_1277:
  1277: LCP      [sp+0]               
  1278: GCP      data[234]             ; = 16711680
  1279: GRE                           
  1280: JZ       label_1284           
  1281: GCP      data[235]             ; = 65280
  1282: LLD      [sp-3]               
  1283: RET      2                    
label_1284:
  1284: LCP      [sp+0]               
  1285: GCP      data[236]  ; "ÿ"      ; "ÿ"
  1286: GRE                           
  1287: JZ       label_1291           
  1288: GCP      data[237]             ; = 0
  1289: LLD      [sp-3]               
  1290: RET      2                    
label_1291:
  1291: GCP      data[238]             ; = 0
  1292: LLD      [sp-3]               
  1293: RET      2                    
  1294: JMP      label_1721           
  1295: JMP      label_1300           
label_1296:
  1296: LCP      [sp+1]               
  1297: GCP      data[239]             ; = 0
  1298: EQU                           
  1299: JZ       label_1301           
label_1300:
  1300: JMP      label_1305           
label_1301:
  1301: LCP      [sp+1]               
  1302: GCP      data[240]             ; = 0
  1303: EQU                           
  1304: JZ       label_1306           
label_1305:
  1305: JMP      label_1310           
label_1306:
  1306: LCP      [sp+1]               
  1307: GCP      data[241]             ; = 1728053248
  1308: EQU                           
  1309: JZ       label_1343           
label_1310:
  1310: LCP      [sp+0]               
  1311: GCP      data[242]             ; = 6750208
  1312: GRE                           
  1313: JZ       label_1317           
  1314: GCP      data[243]             ; = 26368
  1315: LLD      [sp-3]               
  1316: RET      2                    
label_1317:
  1317: LCP      [sp+0]               
  1318: GCP      data[244]  ; "g"      ; "g"
  1319: GRE                           
  1320: JZ       label_1324           
  1321: GCP      data[245]             ; = 3355443200
  1322: LLD      [sp-3]               
  1323: RET      2                    
label_1324:
  1324: LCP      [sp+0]               
  1325: GCP      data[246]             ; = 13107200
  1326: GRE                           
  1327: JZ       label_1331           
  1328: GCP      data[247]             ; = 51200
  1329: LLD      [sp-3]               
  1330: RET      2                    
label_1331:
  1331: LCP      [sp+0]               
  1332: GCP      data[248]  ; "È"      ; "È"
  1333: GRE                           
  1334: JZ       label_1338           
  1335: GCP      data[249]             ; = 201326592
  1336: LLD      [sp-3]               
  1337: RET      2                    
label_1338:
  1338: GCP      data[250]             ; = 786432
  1339: LLD      [sp-3]               
  1340: RET      2                    
  1341: JMP      label_1721           
  1342: JMP      label_1347           
label_1343:
  1343: LCP      [sp+1]               
  1344: GCP      data[251]             ; = 3072
  1345: EQU                           
  1346: JZ       label_1348           
label_1347:
  1347: JMP      label_1352           
label_1348:
  1348: LCP      [sp+1]               
  1349: GCP      data[252]             ; = 12
  1350: EQU                           
  1351: JZ       label_1353           
label_1352:
  1352: JMP      label_1357           
label_1353:
  1353: LCP      [sp+1]               
  1354: GCP      data[253]             ; = 385875968
  1355: EQU                           
  1356: JZ       label_1376           
label_1357:
  1357: LCP      [sp+0]               
  1358: GCP      data[254]             ; = 1507328
  1359: GRE                           
  1360: JZ       label_1364           
  1361: GCP      data[255]             ; = 5888
  1362: LLD      [sp-3]               
  1363: RET      2                    
label_1364:
  1364: LCP      [sp+0]               
  1365: GCP      data[256]             ; = 23
  1366: GRE                           
  1367: JZ       label_1371           
  1368: GCP      data[257]             ; = 3355443200
  1369: LLD      [sp-3]               
  1370: RET      2                    
label_1371:
  1371: GCP      data[258]             ; = 13107200
  1372: LLD      [sp-3]               
  1373: RET      2                    
  1374: JMP      label_1721           
  1375: JMP      label_1380           
label_1376:
  1376: LCP      [sp+1]               
  1377: GCP      data[259]             ; = 51200
  1378: EQU                           
  1379: JZ       label_1420           
label_1380:
  1380: LCP      [sp+0]               
  1381: GCP      data[260]  ; "È"      ; "È"
  1382: GRE                           
  1383: JZ       label_1387           
  1384: GCP      data[261]             ; = 201326592
  1385: LLD      [sp-3]               
  1386: RET      2                    
label_1387:
  1387: LCP      [sp+0]               
  1388: GCP      data[262]             ; = 786432
  1389: GRE                           
  1390: JZ       label_1394           
  1391: GCP      data[263]             ; = 3072
  1392: LLD      [sp-3]               
  1393: RET      2                    
label_1394:
  1394: LCP      [sp+0]               
  1395: GCP      data[264]             ; = 12
  1396: GRE                           
  1397: JZ       label_1401           
  1398: GCP      data[265]             ; = 419430400
  1399: LLD      [sp-3]               
  1400: RET      2                    
label_1401:
  1401: LCP      [sp+0]               
  1402: GCP      data[266]             ; = 1638400
  1403: GRE                           
  1404: JZ       label_1408           
  1405: GCP      data[267]             ; = 6400
  1406: LLD      [sp-3]               
  1407: RET      2                    
label_1408:
  1408: LCP      [sp+0]               
  1409: GCP      data[268]             ; = 25
  1410: GRE                           
  1411: JZ       label_1415           
  1412: GCP      data[269]             ; = 16777216
  1413: LLD      [sp-3]               
  1414: RET      2                    
label_1415:
  1415: GCP      data[270]             ; = 65536
  1416: LLD      [sp-3]               
  1417: RET      2                    
  1418: JMP      label_1721           
  1419: JMP      label_1424           
label_1420:
  1420: LCP      [sp+1]               
  1421: GCP      data[271]             ; = 256
  1422: EQU                           
  1423: JZ       label_1425           
label_1424:
  1424: JMP      label_1429           
label_1425:
  1425: LCP      [sp+1]               
  1426: GCP      data[272]             ; = 1
  1427: EQU                           
  1428: JZ       label_1430           
label_1429:
  1429: JMP      label_1434           
label_1430:
  1430: LCP      [sp+1]               
  1431: GCP      data[273]             ; = 4278190080
  1432: EQU                           
  1433: JZ       label_1435           
label_1434:
  1434: JMP      label_1439           
label_1435:
  1435: LCP      [sp+1]               
  1436: GCP      data[274]             ; = 16711680
  1437: EQU                           
  1438: JZ       label_1478           
label_1439:
  1439: LCP      [sp+0]               
  1440: GCP      data[275]             ; = 65280
  1441: GRE                           
  1442: JZ       label_1446           
  1443: GCP      data[276]  ; "ÿ"      ; "ÿ"
  1444: LLD      [sp-3]               
  1445: RET      2                    
label_1446:
  1446: LCP      [sp+0]               
  1447: GCP      data[277]             ; = 0
  1448: GRE                           
  1449: JZ       label_1453           
  1450: GCP      data[278]             ; = 0
  1451: LLD      [sp-3]               
  1452: RET      2                    
label_1453:
  1453: LCP      [sp+0]               
  1454: GCP      data[279]             ; = 0
  1455: GRE                           
  1456: JZ       label_1460           
  1457: GCP      data[280]             ; = 0
  1458: LLD      [sp-3]               
  1459: RET      2                    
label_1460:
  1460: LCP      [sp+0]               
  1461: GCP      data[281]             ; = 1744830464
  1462: GRE                           
  1463: JZ       label_1467           
  1464: GCP      data[282]             ; = 6815744
  1465: LLD      [sp-3]               
  1466: RET      2                    
label_1467:
  1467: LCP      [sp+0]               
  1468: GCP      data[283]             ; = 26624
  1469: GRE                           
  1470: JZ       label_1474           
  1471: GCP      data[284]  ; "h"      ; "h"
  1472: LLD      [sp-3]               
  1473: RET      2                    
label_1474:
  1474: GCP      data[285]             ; = 4278190080
  1475: LLD      [sp-3]               
  1476: RET      2                    
  1477: JMP      label_1482           
label_1478:
  1478: LCP      [sp+1]               
  1479: GCP      data[286]             ; = 16711680
  1480: EQU                           
  1481: JZ       label_1483           
label_1482:
  1482: JMP      label_1487           
label_1483:
  1483: LCP      [sp+1]               
  1484: GCP      data[287]             ; = 65280
  1485: EQU                           
  1486: JZ       label_1488           
label_1487:
  1487: JMP      label_1492           
label_1488:
  1488: LCP      [sp+1]               
  1489: GCP      data[288]  ; "ÿ"      ; "ÿ"
  1490: EQU                           
  1491: JZ       label_1493           
label_1492:
  1492: JMP      label_1497           
label_1493:
  1493: LCP      [sp+1]               
  1494: GCP      data[289]             ; = 0
  1495: EQU                           
  1496: JZ       label_1523           
label_1497:
  1497: LCP      [sp+0]               
  1498: GCP      data[290]             ; = 0
  1499: GRE                           
  1500: JZ       label_1504           
  1501: GCP      data[291]             ; = 0
  1502: LLD      [sp-3]               
  1503: RET      2                    
label_1504:
  1504: LCP      [sp+0]               
  1505: GCP      data[292]             ; = 0
  1506: GRE                           
  1507: JZ       label_1511           
  1508: GCP      data[293]             ; = 1761607680
  1509: LLD      [sp-3]               
  1510: RET      2                    
label_1511:
  1511: LCP      [sp+0]               
  1512: GCP      data[294]             ; = 6881280
  1513: GRE                           
  1514: JZ       label_1518           
  1515: GCP      data[295]             ; = 26880
  1516: LLD      [sp-3]               
  1517: RET      2                    
label_1518:
  1518: GCP      data[296]  ; "i"      ; "i"
  1519: LLD      [sp-3]               
  1520: RET      2                    
  1521: JMP      label_1721           
  1522: JMP      label_1527           
label_1523:
  1523: LCP      [sp+1]               
  1524: GCP      data[297]             ; = 989855744
  1525: EQU                           
  1526: JZ       label_1567           
label_1527:
  1527: LCP      [sp+0]               
  1528: GCP      data[298]             ; = 3866624
  1529: GRE                           
  1530: JZ       label_1534           
  1531: GCP      data[299]             ; = 15104
  1532: LLD      [sp-3]               
  1533: RET      2                    
label_1534:
  1534: LCP      [sp+0]               
  1535: GCP      data[300]  ; ";"      ; ";"
  1536: GRE                           
  1537: JZ       label_1541           
  1538: GCP      data[301]             ; = 4278190080
  1539: LLD      [sp-3]               
  1540: RET      2                    
label_1541:
  1541: LCP      [sp+0]               
  1542: GCP      data[302]             ; = 16711680
  1543: GRE                           
  1544: JZ       label_1548           
  1545: GCP      data[303]             ; = 65280
  1546: LLD      [sp-3]               
  1547: RET      2                    
label_1548:
  1548: LCP      [sp+0]               
  1549: GCP      data[304]  ; "ÿ"      ; "ÿ"
  1550: GRE                           
  1551: JZ       label_1555           
  1552: GCP      data[305]             ; = 0
  1553: LLD      [sp-3]               
  1554: RET      2                    
label_1555:
  1555: LCP      [sp+0]               
  1556: GCP      data[306]             ; = 0
  1557: GRE                           
  1558: JZ       label_1562           
  1559: GCP      data[307]             ; = 0
  1560: LLD      [sp-3]               
  1561: RET      2                    
label_1562:
  1562: GCP      data[308]             ; = 0
  1563: LLD      [sp-3]               
  1564: RET      2                    
  1565: JMP      label_1721           
  1566: JMP      label_1571           
label_1567:
  1567: LCP      [sp+1]               
  1568: GCP      data[309]             ; = 1778384896
  1569: EQU                           
  1570: JZ       label_1572           
label_1571:
  1571: JMP      label_1576           
label_1572:
  1572: LCP      [sp+1]               
  1573: GCP      data[310]             ; = 6946816
  1574: EQU                           
  1575: JZ       label_1577           
label_1576:
  1576: JMP      label_1581           
label_1577:
  1577: LCP      [sp+1]               
  1578: GCP      data[311]             ; = 27136
  1579: EQU                           
  1580: JZ       label_1615           
label_1581:
  1581: LCP      [sp+0]               
  1582: GCP      data[312]  ; "j"      ; "j"
  1583: GRE                           
  1584: JZ       label_1588           
  1585: GCP      data[313]             ; = 4278190080
  1586: LLD      [sp-3]               
  1587: RET      2                    
label_1588:
  1588: LCP      [sp+0]               
  1589: GCP      data[314]             ; = 16711680
  1590: GRE                           
  1591: JZ       label_1595           
  1592: GCP      data[315]             ; = 65280
  1593: LLD      [sp-3]               
  1594: RET      2                    
label_1595:
  1595: LCP      [sp+0]               
  1596: GCP      data[316]  ; "ÿ"      ; "ÿ"
  1597: GRE                           
  1598: JZ       label_1602           
  1599: GCP      data[317]             ; = 0
  1600: LLD      [sp-3]               
  1601: RET      2                    
label_1602:
  1602: LCP      [sp+0]               
  1603: GCP      data[318]             ; = 0
  1604: GRE                           
  1605: JZ       label_1609           
  1606: GCP      data[319]             ; = 0
  1607: LLD      [sp-3]               
  1608: RET      2                    
label_1609:
  1609: GCP      data[320]             ; = 0
  1610: LLD      [sp-3]               
  1611: RET      2                    
  1612: JMP      label_1721           
  1613: JMP      label_1721           
  1614: JMP      label_1619           
label_1615:
  1615: LCP      [sp+1]               
  1616: GCP      data[321]             ; = 1795162112
  1617: EQU                           
  1618: JZ       label_1652           
label_1619:
  1619: LCP      [sp+0]               
  1620: GCP      data[322]             ; = 7012352
  1621: GRE                           
  1622: JZ       label_1626           
  1623: GCP      data[323]             ; = 27392
  1624: LLD      [sp-3]               
  1625: RET      2                    
label_1626:
  1626: LCP      [sp+0]               
  1627: GCP      data[324]  ; "k"      ; "k"
  1628: GRE                           
  1629: JZ       label_1633           
  1630: GCP      data[325]             ; = 4278190080
  1631: LLD      [sp-3]               
  1632: RET      2                    
label_1633:
  1633: LCP      [sp+0]               
  1634: GCP      data[326]             ; = 16711680
  1635: GRE                           
  1636: JZ       label_1640           
  1637: GCP      data[327]             ; = 65280
  1638: LLD      [sp-3]               
  1639: RET      2                    
label_1640:
  1640: LCP      [sp+0]               
  1641: GCP      data[328]  ; "ÿ"      ; "ÿ"
  1642: GRE                           
  1643: JZ       label_1647           
  1644: GCP      data[329]             ; = 0
  1645: LLD      [sp-3]               
  1646: RET      2                    
label_1647:
  1647: GCP      data[330]             ; = 0
  1648: LLD      [sp-3]               
  1649: RET      2                    
  1650: JMP      label_1721           
  1651: JMP      label_1656           
label_1652:
  1652: LCP      [sp+1]               
  1653: GCP      data[331]             ; = 0
  1654: EQU                           
  1655: JZ       label_1668           
label_1656:
  1656: LCP      [sp+0]               
  1657: GCP      data[332]             ; = 0
  1658: GRE                           
  1659: JZ       label_1663           
  1660: GCP      data[333]             ; = 1811939328
  1661: LLD      [sp-3]               
  1662: RET      2                    
label_1663:
  1663: GCP      data[334]             ; = 7077888
  1664: LLD      [sp-3]               
  1665: RET      2                    
  1666: JMP      label_1721           
  1667: JMP      label_1672           
label_1668:
  1668: LCP      [sp+1]               
  1669: GCP      data[335]             ; = 27648
  1670: EQU                           
  1671: JZ       label_1673           
label_1672:
  1672: JMP      label_1677           
label_1673:
  1673: LCP      [sp+1]               
  1674: GCP      data[336]  ; "l"      ; "l"
  1675: EQU                           
  1676: JZ       label_1678           
label_1677:
  1677: JMP      label_1682           
label_1678:
  1678: LCP      [sp+1]               
  1679: GCP      data[337]             ; = 1056964608
  1680: EQU                           
  1681: JZ       label_1721           
label_1682:
  1682: LCP      [sp+0]               
  1683: GCP      data[338]             ; = 4128768
  1684: GRE                           
  1685: JZ       label_1689           
  1686: GCP      data[339]             ; = 16128
  1687: LLD      [sp-3]               
  1688: RET      2                    
label_1689:
  1689: LCP      [sp+0]               
  1690: GCP      data[340]  ; "?"      ; "?"
  1691: GRE                           
  1692: JZ       label_1696           
  1693: GCP      data[341]             ; = 4278190080
  1694: LLD      [sp-3]               
  1695: RET      2                    
label_1696:
  1696: LCP      [sp+0]               
  1697: GCP      data[342]             ; = 16711680
  1698: GRE                           
  1699: JZ       label_1703           
  1700: GCP      data[343]             ; = 65280
  1701: LLD      [sp-3]               
  1702: RET      2                    
label_1703:
  1703: LCP      [sp+0]               
  1704: GCP      data[344]  ; "ÿ"      ; "ÿ"
  1705: GRE                           
  1706: JZ       label_1710           
  1707: GCP      data[345]             ; = 0
  1708: LLD      [sp-3]               
  1709: RET      2                    
label_1710:
  1710: LCP      [sp+0]               
  1711: GCP      data[346]             ; = 0
  1712: GRE                           
  1713: JZ       label_1717           
  1714: GCP      data[347]             ; = 0
  1715: LLD      [sp-3]               
  1716: RET      2                    
label_1717:
  1717: GCP      data[348]             ; = 0
  1718: LLD      [sp-3]               
  1719: RET      2                    
  1720: JMP      label_1721           
label_1721:
  1721: SSP      1                    
  1722: GCP      data[349]             ; = 1828716544
  1723: LLD      [sp-3]               
  1724: RET      1                    
  1725: ASP      1                    
  1726: ASP      1                    
  1727: ASP      1                    
  1728: XCALL    $rand(void)int        ; args=0
  1729: LLD      [sp+1]               
  1730: GCP      data[350]             ; = 7143424
  1731: MOD                           
  1732: LADR     [sp+0]               
  1733: ASGN                          
  1734: SSP      1                    
  1735: ASP      1                    
  1736: GCP      data[351]             ; = 27904
  1737: ASP      1                    
  1738: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1739: LLD      [sp+1]               
  1740: SSP      1                    
  1741: JMP      label_1743           
  1742: JMP      label_1747           
label_1743:
  1743: LCP      [sp+1]               
  1744: GCP      data[352]  ; "m"      ; "m"
  1745: EQU                           
  1746: JZ       label_1748           
label_1747:
  1747: JMP      label_1752           
label_1748:
  1748: LCP      [sp+1]               
  1749: GCP      data[353]             ; = 4278190080
  1750: EQU                           
  1751: JZ       label_1753           
label_1752:
  1752: JMP      label_1757           
label_1753:
  1753: LCP      [sp+1]               
  1754: GCP      data[354]             ; = 16711680
  1755: EQU                           
  1756: JZ       label_1758           
label_1757:
  1757: JMP      label_1762           
label_1758:
  1758: LCP      [sp+1]               
  1759: GCP      data[355]             ; = 65280
  1760: EQU                           
  1761: JZ       label_1781           
label_1762:
  1762: LCP      [sp+0]               
  1763: GCP      data[356]  ; "ÿ"      ; "ÿ"
  1764: GRE                           
  1765: JZ       label_1769           
  1766: GADR     data[357]            
  1767: LLD      [sp-3]               
  1768: RET      2                    
label_1769:
  1769: LCP      [sp+0]               
  1770: GCP      data[363]             ; = 14848
  1771: GRE                           
  1772: JZ       label_1776           
  1773: GADR     data[364]  ; ":"     
  1774: LLD      [sp-3]               
  1775: RET      2                    
label_1776:
  1776: GADR     data[370]            
  1777: LLD      [sp-3]               
  1778: RET      2                    
  1779: JMP      label_1999           
  1780: JMP      label_1785           
label_1781:
  1781: LCP      [sp+1]               
  1782: GCP      data[376]  ; "ÿ"      ; "ÿ"
  1783: EQU                           
  1784: JZ       label_1786           
label_1785:
  1785: JMP      label_1790           
label_1786:
  1786: LCP      [sp+1]               
  1787: GCP      data[377]             ; = 1711276032
  1788: EQU                           
  1789: JZ       label_1791           
label_1790:
  1790: JMP      label_1795           
label_1791:
  1791: LCP      [sp+1]               
  1792: GCP      data[378]             ; = 6684672
  1793: EQU                           
  1794: JZ       label_1796           
label_1795:
  1795: JMP      label_1800           
label_1796:
  1796: LCP      [sp+1]               
  1797: GCP      data[379]             ; = 26112
  1798: EQU                           
  1799: JZ       label_1801           
label_1800:
  1800: JMP      label_1805           
label_1801:
  1801: LCP      [sp+1]               
  1802: GCP      data[380]  ; "f"      ; "f"
  1803: EQU                           
  1804: JZ       label_1806           
label_1805:
  1805: JMP      label_1810           
label_1806:
  1806: LCP      [sp+1]               
  1807: GCP      data[381]             ; = 1711276032
  1808: EQU                           
  1809: JZ       label_1811           
label_1810:
  1810: JMP      label_1815           
label_1811:
  1811: LCP      [sp+1]               
  1812: GCP      data[382]             ; = 6684672
  1813: EQU                           
  1814: JZ       label_1834           
label_1815:
  1815: LCP      [sp+0]               
  1816: GCP      data[383]             ; = 26112
  1817: GRE                           
  1818: JZ       label_1822           
  1819: GADR     data[384]  ; "f"     
  1820: LLD      [sp-3]               
  1821: RET      2                    
label_1822:
  1822: LCP      [sp+0]               
  1823: GCP      data[391]             ; = 26368
  1824: GRE                           
  1825: JZ       label_1829           
  1826: GADR     data[392]  ; "g"     
  1827: LLD      [sp-3]               
  1828: RET      2                    
label_1829:
  1829: GADR     data[399]            
  1830: LLD      [sp-3]               
  1831: RET      2                    
  1832: JMP      label_1999           
  1833: JMP      label_1838           
label_1834:
  1834: LCP      [sp+1]               
  1835: GCP      data[406]             ; = 6815744
  1836: EQU                           
  1837: JZ       label_1839           
label_1838:
  1838: JMP      label_1843           
label_1839:
  1839: LCP      [sp+1]               
  1840: GCP      data[407]             ; = 26624
  1841: EQU                           
  1842: JZ       label_1844           
label_1843:
  1843: JMP      label_1848           
label_1844:
  1844: LCP      [sp+1]               
  1845: GCP      data[408]  ; "h"      ; "h"
  1846: EQU                           
  1847: JZ       label_1849           
label_1848:
  1848: JMP      label_1853           
label_1849:
  1849: LCP      [sp+1]               
  1850: GCP      data[409]             ; = 4278190080
  1851: EQU                           
  1852: JZ       label_1854           
label_1853:
  1853: JMP      label_1858           
label_1854:
  1854: LCP      [sp+1]               
  1855: GCP      data[410]             ; = 16711680
  1856: EQU                           
  1857: JZ       label_1859           
label_1858:
  1858: JMP      label_1863           
label_1859:
  1859: LCP      [sp+1]               
  1860: GCP      data[411]             ; = 65280
  1861: EQU                           
  1862: JZ       label_1864           
label_1863:
  1863: JMP      label_1868           
label_1864:
  1864: LCP      [sp+1]               
  1865: GCP      data[412]  ; "ÿ"      ; "ÿ"
  1866: EQU                           
  1867: JZ       label_1894           
label_1868:
  1868: LCP      [sp+0]               
  1869: GCP      data[413]             ; = 1761607680
  1870: GRE                           
  1871: JZ       label_1875           
  1872: GADR     data[414]            
  1873: LLD      [sp-3]               
  1874: RET      2                    
label_1875:
  1875: LCP      [sp+0]               
  1876: GCP      data[421]             ; = 4278190080
  1877: GRE                           
  1878: JZ       label_1882           
  1879: GADR     data[422]            
  1880: LLD      [sp-3]               
  1881: RET      2                    
label_1882:
  1882: LCP      [sp+0]               
  1883: GCP      data[429]             ; = 1778384896
  1884: GRE                           
  1885: JZ       label_1889           
  1886: GADR     data[430]            
  1887: LLD      [sp-3]               
  1888: RET      2                    
label_1889:
  1889: GADR     data[437]            
  1890: LLD      [sp-3]               
  1891: RET      2                    
  1892: JMP      label_1999           
  1893: JMP      label_1898           
label_1894:
  1894: LCP      [sp+1]               
  1895: GCP      data[444]  ; "k"      ; "k"
  1896: EQU                           
  1897: JZ       label_1899           
label_1898:
  1898: JMP      label_1903           
label_1899:
  1899: LCP      [sp+1]               
  1900: GCP      data[445]             ; = 4278190080
  1901: EQU                           
  1902: JZ       label_1904           
label_1903:
  1903: JMP      label_1908           
label_1904:
  1904: LCP      [sp+1]               
  1905: GCP      data[446]             ; = 16711680
  1906: EQU                           
  1907: JZ       label_1909           
label_1908:
  1908: JMP      label_1913           
label_1909:
  1909: LCP      [sp+1]               
  1910: GCP      data[447]             ; = 65280
  1911: EQU                           
  1912: JZ       label_1914           
label_1913:
  1913: JMP      label_1918           
label_1914:
  1914: LCP      [sp+1]               
  1915: GCP      data[448]  ; "ÿ"      ; "ÿ"
  1916: EQU                           
  1917: JZ       label_1919           
label_1918:
  1918: JMP      label_1923           
label_1919:
  1919: LCP      [sp+1]               
  1920: GCP      data[449]             ; = 1811939328
  1921: EQU                           
  1922: JZ       label_1924           
label_1923:
  1923: JMP      label_1928           
label_1924:
  1924: LCP      [sp+1]               
  1925: GCP      data[450]             ; = 7077888
  1926: EQU                           
  1927: JZ       label_1947           
label_1928:
  1928: LCP      [sp+0]               
  1929: GCP      data[451]             ; = 27648
  1930: GRE                           
  1931: JZ       label_1935           
  1932: GADR     data[452]  ; "l"     
  1933: LLD      [sp-3]               
  1934: RET      2                    
label_1935:
  1935: LCP      [sp+0]               
  1936: GCP      data[459]             ; = 65280
  1937: GRE                           
  1938: JZ       label_1942           
  1939: GADR     data[460]  ; "ÿ"     
  1940: LLD      [sp-3]               
  1941: RET      2                    
label_1942:
  1942: GADR     data[467]            
  1943: LLD      [sp-3]               
  1944: RET      2                    
  1945: JMP      label_1999           
  1946: JMP      label_1951           
label_1947:
  1947: LCP      [sp+1]               
  1948: GCP      data[474]             ; = 7208960
  1949: EQU                           
  1950: JZ       label_1952           
label_1951:
  1951: JMP      label_1956           
label_1952:
  1952: LCP      [sp+1]               
  1953: GCP      data[475]             ; = 28160
  1954: EQU                           
  1955: JZ       label_1957           
label_1956:
  1956: JMP      label_1961           
label_1957:
  1957: LCP      [sp+1]               
  1958: GCP      data[476]  ; "n"      ; "n"
  1959: EQU                           
  1960: JZ       label_1962           
label_1961:
  1961: JMP      label_1966           
label_1962:
  1962: LCP      [sp+1]               
  1963: GCP      data[477]             ; = 1845493760
  1964: EQU                           
  1965: JZ       label_1967           
label_1966:
  1966: JMP      label_1971           
label_1967:
  1967: LCP      [sp+1]               
  1968: GCP      data[478]             ; = 7208960
  1969: EQU                           
  1970: JZ       label_1972           
label_1971:
  1971: JMP      label_1976           
label_1972:
  1972: LCP      [sp+1]               
  1973: GCP      data[479]             ; = 28160
  1974: EQU                           
  1975: JZ       label_1977           
label_1976:
  1976: JMP      label_1981           
label_1977:
  1977: LCP      [sp+1]               
  1978: GCP      data[480]  ; "n"      ; "n"
  1979: EQU                           
  1980: JZ       label_1999           
label_1981:
  1981: LCP      [sp+0]               
  1982: GCP      data[481]             ; = 4278190080
  1983: GRE                           
  1984: JZ       label_1988           
  1985: GADR     data[482]            
  1986: LLD      [sp-3]               
  1987: RET      2                    
label_1988:
  1988: LCP      [sp+0]               
  1989: GCP      data[489]             ; = 1593835520
  1990: GRE                           
  1991: JZ       label_1995           
  1992: GADR     data[490]            
  1993: LLD      [sp-3]               
  1994: RET      2                    
label_1995:
  1995: GADR     data[497]            
  1996: LLD      [sp-3]               
  1997: RET      2                    
  1998: JMP      label_1999           
label_1999:
  1999: SSP      1                    
  2000: GADR     data[504]  ; "Z"     
  2001: LLD      [sp-3]               
  2002: RET      1                    
  2003: ASP      1                    
  2004: GCP      data[512]  ; "Z"      ; "Z"
  2005: LADR     [sp+0]               
  2006: ASGN                          
  2007: SSP      1                    
label_2008:
  2008: LCP      [sp+0]               
  2009: GCP      data[513]             ; = 1526726656
  2010: LES                           
  2011: JZ       label_2039           
  2012: GCP      data[514]             ; = 5963776
  2013: LADR     [sp-3]               
  2014: DADR     data[92]             
  2015: LCP      [sp+0]               
  2016: GCP      data[515]             ; = 23296
  2017: MUL                           
  2018: ADD                           
  2019: ASGN                          
  2020: SSP      1                    
  2021: GCP      data[516]  ; "["      ; "["
  2022: LADR     [sp-3]               
  2023: DADR     data[124]            
  2024: LCP      [sp+0]               
  2025: GCP      data[517]             ; = 16777216
  2026: MUL                           
  2027: ADD                           
  2028: ASGN                          
  2029: SSP      1                    
  2030: LCP      [sp+0]               
  2031: LCP      [sp+0]               
  2032: GCP      data[518]             ; = 65536
  2033: ADD                           
  2034: LADR     [sp+0]               
  2035: ASGN                          
  2036: SSP      1                    
  2037: SSP      1                    
  2038: JMP      label_2008           
label_2039:
  2039: ASP      1                    
  2040: GCP      data[519]             ; = 256
  2041: ASP      1                    
  2042: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2043: LLD      [sp+1]               
  2044: SSP      1                    
  2045: JMP      label_2047           
  2046: JMP      label_2051           
label_2047:
  2047: LCP      [sp+1]               
  2048: GCP      data[520]             ; = 1
  2049: EQU                           
  2050: JZ       label_2067           
label_2051:
  2051: GCP      data[521]             ; = 1526726656
  2052: LADR     [sp-3]               
  2053: DADR     data[92]             
  2054: GCP      data[522]             ; = 5963776
  2055: ADD                           
  2056: ASGN                          
  2057: SSP      1                    
  2058: GCP      data[523]             ; = 23296
  2059: LADR     [sp-3]               
  2060: DADR     data[92]             
  2061: GCP      data[524]  ; "["      ; "["
  2062: ADD                           
  2063: ASGN                          
  2064: SSP      1                    
  2065: JMP      label_2618           
  2066: JMP      label_2071           
label_2067:
  2067: LCP      [sp+1]               
  2068: GCP      data[525]             ; = 1006632960
  2069: EQU                           
  2070: JZ       label_2072           
label_2071:
  2071: JMP      label_2076           
label_2072:
  2072: LCP      [sp+1]               
  2073: GCP      data[526]             ; = 3932160
  2074: EQU                           
  2075: JZ       label_2077           
label_2076:
  2076: JMP      label_2081           
label_2077:
  2077: LCP      [sp+1]               
  2078: GCP      data[527]             ; = 15360
  2079: EQU                           
  2080: JZ       label_2082           
label_2081:
  2081: JMP      label_2086           
label_2082:
  2082: LCP      [sp+1]               
  2083: GCP      data[528]  ; "<"      ; "<"
  2084: EQU                           
  2085: JZ       label_2102           
label_2086:
  2086: GCP      data[529]             ; = 1493172224
  2087: LADR     [sp-3]               
  2088: DADR     data[92]             
  2089: GCP      data[530]             ; = 5832704
  2090: ADD                           
  2091: ASGN                          
  2092: SSP      1                    
  2093: GCP      data[531]             ; = 22784
  2094: LADR     [sp-3]               
  2095: DADR     data[92]             
  2096: GCP      data[532]  ; "Y"      ; "Y"
  2097: ADD                           
  2098: ASGN                          
  2099: SSP      1                    
  2100: JMP      label_2618           
  2101: JMP      label_2106           
label_2102:
  2102: LCP      [sp+1]               
  2103: GCP      data[533]             ; = 1509949440
  2104: EQU                           
  2105: JZ       label_2107           
label_2106:
  2106: JMP      label_2111           
label_2107:
  2107: LCP      [sp+1]               
  2108: GCP      data[534]             ; = 5898240
  2109: EQU                           
  2110: JZ       label_2134           
label_2111:
  2111: GCP      data[535]             ; = 23040
  2112: LADR     [sp-3]               
  2113: DADR     data[92]             
  2114: GCP      data[536]  ; "Z"      ; "Z"
  2115: ADD                           
  2116: ASGN                          
  2117: SSP      1                    
  2118: GCP      data[537]             ; = 33554432
  2119: LADR     [sp-3]               
  2120: DADR     data[92]             
  2121: GCP      data[538]             ; = 131072
  2122: ADD                           
  2123: ASGN                          
  2124: SSP      1                    
  2125: GCP      data[539]             ; = 512
  2126: LADR     [sp-3]               
  2127: DADR     data[92]             
  2128: GCP      data[540]             ; = 2
  2129: ADD                           
  2130: ASGN                          
  2131: SSP      1                    
  2132: JMP      label_2618           
  2133: JMP      label_2138           
label_2134:
  2134: LCP      [sp+1]               
  2135: GCP      data[541]             ; = 1526726656
  2136: EQU                           
  2137: JZ       label_2161           
label_2138:
  2138: GCP      data[542]             ; = 5963776
  2139: LADR     [sp-3]               
  2140: DADR     data[92]             
  2141: GCP      data[543]             ; = 23296
  2142: ADD                           
  2143: ASGN                          
  2144: SSP      1                    
  2145: GCP      data[544]  ; "["      ; "["
  2146: LADR     [sp-3]               
  2147: DADR     data[92]             
  2148: GCP      data[545]             ; = 16777216
  2149: ADD                           
  2150: ASGN                          
  2151: SSP      1                    
  2152: GCP      data[546]             ; = 65536
  2153: LADR     [sp-3]               
  2154: DADR     data[92]             
  2155: GCP      data[547]             ; = 256
  2156: ADD                           
  2157: ASGN                          
  2158: SSP      1                    
  2159: JMP      label_2618           
  2160: JMP      label_2165           
label_2161:
  2161: LCP      [sp+1]               
  2162: GCP      data[548]             ; = 1
  2163: EQU                           
  2164: JZ       label_2166           
label_2165:
  2165: JMP      label_2170           
label_2166:
  2166: LCP      [sp+1]               
  2167: GCP      data[549]             ; = 0
  2168: EQU                           
  2169: JZ       label_2193           
label_2170:
  2170: GCP      data[550]             ; = 0
  2171: LADR     [sp-3]               
  2172: DADR     data[92]             
  2173: GCP      data[551]             ; = 0
  2174: ADD                           
  2175: ASGN                          
  2176: SSP      1                    
  2177: GCP      data[552]             ; = 0
  2178: LADR     [sp-3]               
  2179: DADR     data[92]             
  2180: GCP      data[553]             ; = 167772160
  2181: ADD                           
  2182: ASGN                          
  2183: SSP      1                    
  2184: GCP      data[554]             ; = 655360
  2185: LADR     [sp-3]               
  2186: DADR     data[92]             
  2187: GCP      data[555]             ; = 2560
  2188: ADD                           
  2189: ASGN                          
  2190: SSP      1                    
  2191: JMP      label_2618           
  2192: JMP      label_2197           
label_2193:
  2193: LCP      [sp+1]               
  2194: GCP      data[556]  ; "\n"     ; "
"
  2195: EQU                           
  2196: JZ       label_2198           
label_2197:
  2197: JMP      label_2202           
label_2198:
  2198: LCP      [sp+1]               
  2199: GCP      data[557]             ; = 838860800
  2200: EQU                           
  2201: JZ       label_2203           
label_2202:
  2202: JMP      label_2207           
label_2203:
  2203: LCP      [sp+1]               
  2204: GCP      data[558]             ; = 3276800
  2205: EQU                           
  2206: JZ       label_2223           
label_2207:
  2207: GCP      data[559]             ; = 12800
  2208: LADR     [sp-3]               
  2209: DADR     data[92]             
  2210: GCP      data[560]  ; "2"      ; "2"
  2211: ADD                           
  2212: ASGN                          
  2213: SSP      1                    
  2214: GCP      data[561]             ; = 67108864
  2215: LADR     [sp-3]               
  2216: DADR     data[92]             
  2217: GCP      data[562]             ; = 262144
  2218: ADD                           
  2219: ASGN                          
  2220: SSP      1                    
  2221: JMP      label_2618           
  2222: JMP      label_2227           
label_2223:
  2223: LCP      [sp+1]               
  2224: GCP      data[563]             ; = 1024
  2225: EQU                           
  2226: JZ       label_2264           
label_2227:
  2227: GCP      data[564]             ; = 4
  2228: LADR     [sp-3]               
  2229: DADR     data[92]             
  2230: GCP      data[565]             ; = 16777216
  2231: ADD                           
  2232: ASGN                          
  2233: SSP      1                    
  2234: GCP      data[566]             ; = 65536
  2235: LADR     [sp-3]               
  2236: DADR     data[92]             
  2237: GCP      data[567]             ; = 256
  2238: ADD                           
  2239: ASGN                          
  2240: SSP      1                    
  2241: GCP      data[568]             ; = 1
  2242: LADR     [sp-3]               
  2243: DADR     data[92]             
  2244: GCP      data[569]             ; = 0
  2245: ADD                           
  2246: ASGN                          
  2247: SSP      1                    
  2248: GCP      data[570]             ; = 0
  2249: LADR     [sp-3]               
  2250: DADR     data[92]             
  2251: GCP      data[571]             ; = 0
  2252: ADD                           
  2253: ASGN                          
  2254: SSP      1                    
  2255: GCP      data[572]             ; = 0
  2256: LADR     [sp-3]               
  2257: DADR     data[92]             
  2258: GCP      data[573]             ; = 167772160
  2259: ADD                           
  2260: ASGN                          
  2261: SSP      1                    
  2262: JMP      label_2618           
  2263: JMP      label_2268           
label_2264:
  2264: LCP      [sp+1]               
  2265: GCP      data[574]             ; = 655360
  2266: EQU                           
  2267: JZ       label_2269           
label_2268:
  2268: JMP      label_2273           
label_2269:
  2269: LCP      [sp+1]               
  2270: GCP      data[575]             ; = 2560
  2271: EQU                           
  2272: JZ       label_2274           
label_2273:
  2273: JMP      label_2278           
label_2274:
  2274: LCP      [sp+1]               
  2275: GCP      data[576]  ; "\n"     ; "
"
  2276: EQU                           
  2277: JZ       label_2294           
label_2278:
  2278: GCP      data[577]             ; = 838860800
  2279: LADR     [sp-3]               
  2280: DADR     data[92]             
  2281: GCP      data[578]             ; = 3276800
  2282: ADD                           
  2283: ASGN                          
  2284: SSP      1                    
  2285: GCP      data[579]             ; = 12800
  2286: LADR     [sp-3]               
  2287: DADR     data[92]             
  2288: GCP      data[580]  ; "2"      ; "2"
  2289: ADD                           
  2290: ASGN                          
  2291: SSP      1                    
  2292: JMP      label_2618           
  2293: JMP      label_2298           
label_2294:
  2294: LCP      [sp+1]               
  2295: GCP      data[581]             ; = 67108864
  2296: EQU                           
  2297: JZ       label_2299           
label_2298:
  2298: JMP      label_2303           
label_2299:
  2299: LCP      [sp+1]               
  2300: GCP      data[582]             ; = 262144
  2301: EQU                           
  2302: JZ       label_2304           
label_2303:
  2303: JMP      label_2308           
label_2304:
  2304: LCP      [sp+1]               
  2305: GCP      data[583]             ; = 1024
  2306: EQU                           
  2307: JZ       label_2331           
label_2308:
  2308: GCP      data[584]             ; = 4
  2309: LADR     [sp-3]               
  2310: DADR     data[92]             
  2311: GCP      data[585]             ; = 16777216
  2312: ADD                           
  2313: ASGN                          
  2314: SSP      1                    
  2315: GCP      data[586]             ; = 65536
  2316: LADR     [sp-3]               
  2317: DADR     data[92]             
  2318: GCP      data[587]             ; = 256
  2319: ADD                           
  2320: ASGN                          
  2321: SSP      1                    
  2322: GCP      data[588]             ; = 1
  2323: LADR     [sp-3]               
  2324: DADR     data[92]             
  2325: GCP      data[589]             ; = 1291845632
  2326: ADD                           
  2327: ASGN                          
  2328: SSP      1                    
  2329: JMP      label_2618           
  2330: JMP      label_2335           
label_2331:
  2331: LCP      [sp+1]               
  2332: GCP      data[590]             ; = 1229783040
  2333: EQU                           
  2334: JZ       label_2365           
label_2335:
  2335: GCP      data[591]             ; = 1397312768
  2336: LADR     [sp-3]               
  2337: DADR     data[92]             
  2338: GCP      data[592]  ; "MISSION COMPLETE" ; "MISSION COMPLETE"
  2339: ADD                           
  2340: ASGN                          
  2341: SSP      1                    
  2342: GCP      data[593]             ; = 1230197577
  2343: LADR     [sp-3]               
  2344: DADR     data[92]             
  2345: GCP      data[594]             ; = 1330205523
  2346: ADD                           
  2347: ASGN                          
  2348: SSP      1                    
  2349: GCP      data[595]             ; = 1313818963
  2350: LADR     [sp-3]               
  2351: DADR     data[92]             
  2352: GCP      data[596]             ; = 542003017
  2353: ADD                           
  2354: ASGN                          
  2355: SSP      1                    
  2356: GCP      data[597]             ; = 1126190671
  2357: LADR     [sp-3]               
  2358: DADR     data[92]             
  2359: GCP      data[598]             ; = 1329799246
  2360: ADD                           
  2361: ASGN                          
  2362: SSP      1                    
  2363: JMP      label_2618           
  2364: JMP      label_2369           
label_2365:
  2365: LCP      [sp+1]               
  2366: GCP      data[599]             ; = 1297040160
  2367: EQU                           
  2368: JZ       label_2370           
label_2369:
  2369: JMP      label_2374           
label_2370:
  2370: LCP      [sp+1]               
  2371: GCP      data[600]             ; = 1347243843
  2372: EQU                           
  2373: JZ       label_2411           
label_2374:
  2374: GCP      data[601]             ; = 1280331087
  2375: LADR     [sp-3]               
  2376: DADR     data[92]             
  2377: GCP      data[602]             ; = 1162629197
  2378: ADD                           
  2379: ASGN                          
  2380: SSP      1                    
  2381: GCP      data[603]             ; = 1413827664
  2382: LADR     [sp-3]               
  2383: DADR     data[92]             
  2384: GCP      data[604]             ; = 1163150668
  2385: ADD                           
  2386: ASGN                          
  2387: SSP      1                    
  2388: GCP      data[605]             ; = 4543557
  2389: LADR     [sp-3]               
  2390: DADR     data[92]             
  2391: GCP      data[606]             ; = 17748
  2392: ADD                           
  2393: ASGN                          
  2394: SSP      1                    
  2395: GCP      data[607]             ; = 69
  2396: LADR     [sp-3]               
  2397: DADR     data[92]             
  2398: GCP      data[608]             ; = 0
  2399: ADD                           
  2400: ASGN                          
  2401: SSP      1                    
  2402: GCP      data[609]             ; = 16777216
  2403: LADR     [sp-3]               
  2404: DADR     data[92]             
  2405: GCP      data[610]             ; = 65536
  2406: ADD                           
  2407: ASGN                          
  2408: SSP      1                    
  2409: JMP      label_2618           
  2410: JMP      label_2415           
label_2411:
  2411: LCP      [sp+1]               
  2412: GCP      data[611]             ; = 256
  2413: EQU                           
  2414: JZ       label_2431           
label_2415:
  2415: GCP      data[612]             ; = 1
  2416: LADR     [sp-3]               
  2417: DADR     data[92]             
  2418: GCP      data[613]             ; = 16777216
  2419: ADD                           
  2420: ASGN                          
  2421: SSP      1                    
  2422: GCP      data[614]             ; = 65536
  2423: LADR     [sp-3]               
  2424: DADR     data[92]             
  2425: GCP      data[615]             ; = 256
  2426: ADD                           
  2427: ASGN                          
  2428: SSP      1                    
  2429: JMP      label_2618           
  2430: JMP      label_2435           
label_2431:
  2431: LCP      [sp+1]               
  2432: GCP      data[616]             ; = 1
  2433: EQU                           
  2434: JZ       label_2436           
label_2435:
  2435: JMP      label_2440           
label_2436:
  2436: LCP      [sp+1]               
  2437: GCP      data[617]             ; = 0
  2438: EQU                           
  2439: JZ       label_2441           
label_2440:
  2440: JMP      label_2445           
label_2441:
  2441: LCP      [sp+1]               
  2442: GCP      data[618]             ; = 0
  2443: EQU                           
  2444: JZ       label_2475           
label_2445:
  2445: GCP      data[619]             ; = 3221225472
  2446: LADR     [sp-3]               
  2447: DADR     data[92]             
  2448: GCP      data[620]             ; = 1086324736
  2449: ADD                           
  2450: ASGN                          
  2451: SSP      1                    
  2452: GCP      data[621]             ; = 4243456
  2453: LADR     [sp-3]               
  2454: DADR     data[92]             
  2455: GCP      data[622]  ; "À@"     ; "À@"
  2456: ADD                           
  2457: ASGN                          
  2458: SSP      1                    
  2459: GCP      data[623]             ; = 64
  2460: LADR     [sp-3]               
  2461: DADR     data[92]             
  2462: GCP      data[624]             ; = 0
  2463: ADD                           
  2464: ASGN                          
  2465: SSP      1                    
  2466: GCP      data[625]             ; = 67108864
  2467: LADR     [sp-3]               
  2468: DADR     data[92]             
  2469: GCP      data[626]             ; = 262144
  2470: ADD                           
  2471: ASGN                          
  2472: SSP      1                    
  2473: JMP      label_2618           
  2474: JMP      label_2479           
label_2475:
  2475: LCP      [sp+1]               
  2476: GCP      data[627]             ; = 1024
  2477: EQU                           
  2478: JZ       label_2502           
label_2479:
  2479: GCP      data[628]             ; = 4
  2480: LADR     [sp-3]               
  2481: DADR     data[92]             
  2482: GCP      data[629]             ; = 33554432
  2483: ADD                           
  2484: ASGN                          
  2485: SSP      1                    
  2486: GCP      data[630]             ; = 131072
  2487: LADR     [sp-3]               
  2488: DADR     data[92]             
  2489: GCP      data[631]             ; = 512
  2490: ADD                           
  2491: ASGN                          
  2492: SSP      1                    
  2493: GCP      data[632]             ; = 2
  2494: LADR     [sp-3]               
  2495: DADR     data[92]             
  2496: GCP      data[633]             ; = 0
  2497: ADD                           
  2498: ASGN                          
  2499: SSP      1                    
  2500: JMP      label_2618           
  2501: JMP      label_2506           
label_2502:
  2502: LCP      [sp+1]               
  2503: GCP      data[634]             ; = 0
  2504: EQU                           
  2505: JZ       label_2536           
label_2506:
  2506: GCP      data[635]             ; = 1073741824
  2507: LADR     [sp-3]               
  2508: DADR     data[92]             
  2509: GCP      data[636]             ; = 1094713344
  2510: ADD                           
  2511: ASGN                          
  2512: SSP      1                    
  2513: GCP      data[637]             ; = 4276224
  2514: LADR     [sp-3]               
  2515: DADR     data[92]             
  2516: GCP      data[638]  ; "@A"     ; "@A"
  2517: ADD                           
  2518: ASGN                          
  2519: SSP      1                    
  2520: GCP      data[639]             ; = 65
  2521: LADR     [sp-3]               
  2522: DADR     data[92]             
  2523: GCP      data[640]             ; = 0
  2524: ADD                           
  2525: ASGN                          
  2526: SSP      1                    
  2527: GCP      data[641]             ; = 67108864
  2528: LADR     [sp-3]               
  2529: DADR     data[92]             
  2530: GCP      data[642]             ; = 262144
  2531: ADD                           
  2532: ASGN                          
  2533: SSP      1                    
  2534: JMP      label_2618           
  2535: JMP      label_2540           
label_2536:
  2536: LCP      [sp+1]               
  2537: GCP      data[643]             ; = 1024
  2538: EQU                           
  2539: JZ       label_2541           
label_2540:
  2540: JMP      label_2545           
label_2541:
  2541: LCP      [sp+1]               
  2542: GCP      data[644]             ; = 4
  2543: EQU                           
  2544: JZ       label_2546           
label_2545:
  2545: JMP      label_2550           
label_2546:
  2546: LCP      [sp+1]               
  2547: GCP      data[645]             ; = 134217728
  2548: EQU                           
  2549: JZ       label_2617           
label_2550:
  2550: GCP      data[646]             ; = 524288
  2551: LADR     [sp-3]               
  2552: DADR     data[92]             
  2553: GCP      data[647]             ; = 2048
  2554: ADD                           
  2555: ASGN                          
  2556: SSP      1                    
  2557: GCP      data[648]             ; = 8
  2558: LADR     [sp-3]               
  2559: DADR     data[92]             
  2560: GCP      data[649]             ; = 50331648
  2561: ADD                           
  2562: ASGN                          
  2563: SSP      1                    
  2564: GCP      data[650]             ; = 196608
  2565: LADR     [sp-3]               
  2566: DADR     data[92]             
  2567: GCP      data[651]             ; = 768
  2568: ADD                           
  2569: ASGN                          
  2570: SSP      1                    
  2571: GCP      data[652]             ; = 3
  2572: LADR     [sp-3]               
  2573: DADR     data[92]             
  2574: GCP      data[653]             ; = 0
  2575: ADD                           
  2576: ASGN                          
  2577: SSP      1                    
  2578: JMP      label_2618           
  2579: JMP      label_2580           
label_2580:
  2580: GCP      data[654]             ; = 0
  2581: LADR     [sp-3]               
  2582: DADR     data[92]             
  2583: GCP      data[655]             ; = 3221225472
  2584: ADD                           
  2585: ASGN                          
  2586: SSP      1                    
  2587: GCP      data[656]             ; = 1103101952
  2588: LADR     [sp-3]               
  2589: DADR     data[92]             
  2590: GCP      data[657]             ; = 172081152
  2591: ADD                           
  2592: ASGN                          
  2593: SSP      1                    
  2594: GCP      data[658]  ; "ÀA\n"   ; "ÀA
"
  2595: LADR     [sp-3]               
  2596: DADR     data[92]             
  2597: GCP      data[659]             ; = 2625
  2598: ADD                           
  2599: ASGN                          
  2600: SSP      1                    
  2601: GCP      data[660]             ; = 10
  2602: LADR     [sp-3]               
  2603: DADR     data[92]             
  2604: GCP      data[661]             ; = 335544320
  2605: ADD                           
  2606: ASGN                          
  2607: SSP      1                    
  2608: GCP      data[662]             ; = 1310720
  2609: LADR     [sp-3]               
  2610: DADR     data[92]             
  2611: GCP      data[663]             ; = 5120
  2612: ADD                           
  2613: ASGN                          
  2614: SSP      1                    
  2615: JMP      label_2618           
  2616: JMP      label_2618           
label_2617:
  2617: JMP      label_2580           
label_2618:
  2618: SSP      1                    
  2619: RET      1                    
  2620: ASP      128                  
  2621: ASP      3                    
  2622: ASP      3                    
  2623: GCP      data[664]             ; = 20
  2624: ASP      1                    
  2625: ASP      1                    
  2626: ASP      1                    
  2627: GCP      data[665]             ; = 3355443200
  2628: LADR     [sp+136]             
  2629: ASGN                          
  2630: SSP      1                    
  2631: ASP      1                    
  2632: GCP      data[666]             ; = 13107200
  2633: ASP      1                    
  2634: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2635: LLD      [sp+138]             
  2636: SSP      1                    
  2637: JZ       label_2726           
  2638: LCP      [sp-5]               
  2639: LADR     [sp+131]             
  2640: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  2641: SSP      2                    
  2642: ASP      1                    
  2643: LADR     [sp+0]               
  2644: LADR     [sp+134]             
  2645: GCP      data[667]             ; = 51200
  2646: ASP      1                    
  2647: XCALL    $SC_MP_EnumPlayers(*s_SC_MP_EnumPlayers,*unsignedlong,unsignedlong)int ; args=3
  2648: LLD      [sp+138]             
  2649: SSP      3                    
  2650: SSP      1                    
  2651: LCP      [sp+134]             
  2652: JZ       label_2654           
  2653: JMP      label_2657           
label_2654:
  2654: GCP      data[668]  ; "È"      ; "È"
  2655: LLD      [sp-3]               
  2656: RET      138                  
label_2657:
  2657: GCP      data[669]             ; = 201326592
  2658: LADR     [sp+135]             
  2659: ASGN                          
  2660: SSP      1                    
label_2661:
  2661: LCP      [sp+135]             
  2662: LCP      [sp+134]             
  2663: LES                           
  2664: JZ       label_2716           
  2665: LADR     [sp+0]               
  2666: LCP      [sp+135]             
  2667: GCP      data[670]             ; = 786432
  2668: MUL                           
  2669: ADD                           
  2670: PNT      8                    
  2671: DCP      4                    
  2672: GCP      data[671]             ; = 3072
  2673: EQU                           
  2674: JZ       label_2707           
  2675: LADR     [sp+0]               
  2676: LCP      [sp+135]             
  2677: GCP      data[672]             ; = 12
  2678: MUL                           
  2679: ADD                           
  2680: DCP      4                    
  2681: LADR     [sp+128]             
  2682: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  2683: SSP      2                    
  2684: ASP      1                    
  2685: LADR     [sp+128]             
  2686: LADR     [sp+131]             
  2687: ASP      1                    
  2688: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  2689: LLD      [sp+138]             
  2690: SSP      2                    
  2691: LADR     [sp+137]             
  2692: ASGN                          
  2693: SSP      1                    
  2694: LCP      [sp+137]             
  2695: LCP      [sp+136]             
  2696: FLES                          
  2697: JZ       label_2707           
  2698: LCP      [sp+137]             
  2699: LADR     [sp+136]             
  2700: ASGN                          
  2701: SSP      1                    
  2702: LADR     [sp+128]             
  2703: DCP      12                   
  2704: LCP      [sp-4]               
  2705: ASGN                          
  2706: SSP      3                    
label_2707:
  2707: LCP      [sp+135]             
  2708: LCP      [sp+135]             
  2709: GCP      data[673]             ; = 318767104
  2710: ADD                           
  2711: LADR     [sp+135]             
  2712: ASGN                          
  2713: SSP      1                    
  2714: SSP      1                    
  2715: JMP      label_2661           
label_2716:
  2716: LCP      [sp+136]             
  2717: GCP      data[674]             ; = 1245184
  2718: FLES                          
  2719: JZ       label_2723           
  2720: GCP      data[675]             ; = 4864
  2721: LLD      [sp-3]               
  2722: RET      138                  
label_2723:
  2723: GCP      data[676]             ; = 19
  2724: LLD      [sp-3]               
  2725: RET      138                  
label_2726:
  2726: ASP      1                    
  2727: LCP      [sp-4]               
  2728: ASP      1                    
  2729: XCALL    $SC_PC_GetPos(*c_Vector3)int ; args=1
  2730: LLD      [sp+138]             
  2731: SSP      1                    
  2732: SSP      1                    
  2733: ASP      1                    
  2734: LADR     [sp+128]             
  2735: LADR     [sp+131]             
  2736: ASP      1                    
  2737: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  2738: LLD      [sp+138]             
  2739: SSP      2                    
  2740: LADR     [sp+136]             
  2741: ASGN                          
  2742: SSP      1                    
  2743: LCP      [sp+136]             
  2744: GCP      data[677]             ; = 301989888
  2745: FLES                          
  2746: JZ       label_2750           
  2747: GCP      data[678]             ; = 1179648
  2748: LLD      [sp-3]               
  2749: RET      138                  
label_2750:
  2750: GCP      data[679]             ; = 4608
  2751: LLD      [sp-3]               
  2752: RET      138                  
  2753: ASP      1                    
  2754: ASP      1                    
  2755: ASP      1                    
  2756: LCP      [sp-5]               
  2757: LCP      [sp-4]               
  2758: ASP      1                    
  2759: XCALL    $SC_GetGroupPlayers(unsignedlong,unsignedlong)unsignedlong ; args=2
  2760: LLD      [sp+2]               
  2761: SSP      2                    
  2762: LADR     [sp+1]               
  2763: ASGN                          
  2764: SSP      1                    
  2765: GCP      data[680]             ; = 18
  2766: LADR     [sp+0]               
  2767: ASGN                          
  2768: SSP      1                    
label_2769:
  2769: LCP      [sp+0]               
  2770: LCP      [sp+1]               
  2771: LES                           
  2772: JZ       label_2800           
  2773: ASP      1                    
  2774: ASP      1                    
  2775: LCP      [sp-5]               
  2776: LCP      [sp-4]               
  2777: LCP      [sp+0]               
  2778: ASP      1                    
  2779: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  2780: LLD      [sp+3]               
  2781: SSP      3                    
  2782: ASP      1                    
  2783: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  2784: LLD      [sp+2]               
  2785: SSP      1                    
  2786: JZ       label_2791           
  2787: JMP      label_2788           
label_2788:
  2788: GCP      data[681]             ; = 301989888
  2789: LLD      [sp-3]               
  2790: RET      2                    
label_2791:
  2791: LCP      [sp+0]               
  2792: LCP      [sp+0]               
  2793: GCP      data[682]             ; = 1179648
  2794: ADD                           
  2795: LADR     [sp+0]               
  2796: ASGN                          
  2797: SSP      1                    
  2798: SSP      1                    
  2799: JMP      label_2769           
label_2800:
  2800: GCP      data[683]             ; = 4608
  2801: LLD      [sp-3]               
  2802: RET      2                    
  2803: ASP      1                    
  2804: ASP      1                    
  2805: ASP      1                    
  2806: LCP      [sp-5]               
  2807: LCP      [sp-4]               
  2808: ASP      1                    
  2809: XCALL    $SC_GetGroupPlayers(unsignedlong,unsignedlong)unsignedlong ; args=2
  2810: LLD      [sp+2]               
  2811: SSP      2                    
  2812: LADR     [sp+1]               
  2813: ASGN                          
  2814: SSP      1                    
  2815: GCP      data[684]             ; = 18
  2816: LADR     [sp+0]               
  2817: ASGN                          
  2818: SSP      1                    
label_2819:
  2819: LCP      [sp+0]               
  2820: LCP      [sp+1]               
  2821: LES                           
  2822: JZ       label_2865           
  2823: ASP      1                    
  2824: ASP      1                    
  2825: LCP      [sp-5]               
  2826: LCP      [sp-4]               
  2827: LCP      [sp+0]               
  2828: ASP      1                    
  2829: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  2830: LLD      [sp+3]               
  2831: SSP      3                    
  2832: ASP      1                    
  2833: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  2834: LLD      [sp+2]               
  2835: SSP      1                    
  2836: JZ       label_2856           
  2837: JMP      label_2838           
label_2838:
  2838: ASP      1                    
  2839: ASP      1                    
  2840: LCP      [sp-5]               
  2841: LCP      [sp-4]               
  2842: LCP      [sp+0]               
  2843: ASP      1                    
  2844: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  2845: LLD      [sp+3]               
  2846: SSP      3                    
  2847: ASP      1                    
  2848: XCALL    $SC_P_GetActive(unsignedlong)int ; args=1
  2849: LLD      [sp+2]               
  2850: SSP      1                    
  2851: JZ       label_2856           
  2852: JMP      label_2853           
label_2853:
  2853: GCP      data[685]             ; = 251658240
  2854: LLD      [sp-3]               
  2855: RET      2                    
label_2856:
  2856: LCP      [sp+0]               
  2857: LCP      [sp+0]               
  2858: GCP      data[686]             ; = 983040
  2859: ADD                           
  2860: LADR     [sp+0]               
  2861: ASGN                          
  2862: SSP      1                    
  2863: SSP      1                    
  2864: JMP      label_2819           
label_2865:
  2865: GCP      data[687]             ; = 3840
  2866: LLD      [sp-3]               
  2867: RET      2                    
  2868: ASP      1                    
  2869: ASP      1                    
  2870: ASP      1                    
  2871: ASP      1                    
  2872: ASP      1                    
  2873: ASP      1                    
  2874: GCP      data[688]             ; = 15
  2875: LCP      [sp-4]               
  2876: ASP      1                    
  2877: XCALL    $SC_GetGroupPlayers(unsignedlong,unsignedlong)unsignedlong ; args=2
  2878: LLD      [sp+5]               
  2879: SSP      2                    
  2880: LADR     [sp+2]               
  2881: ASGN                          
  2882: SSP      1                    
  2883: GCP      data[689]             ; = 285212672
  2884: LADR     [sp+0]               
  2885: ASGN                          
  2886: SSP      1                    
label_2887:
  2887: LCP      [sp+0]               
  2888: LCP      [sp+2]               
  2889: LES                           
  2890: JZ       label_2945           
  2891: ASP      1                    
  2892: GCP      data[690]             ; = 1114112
  2893: LCP      [sp-4]               
  2894: LCP      [sp+0]               
  2895: ASP      1                    
  2896: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  2897: LLD      [sp+5]               
  2898: SSP      3                    
  2899: LADR     [sp+4]               
  2900: ASGN                          
  2901: SSP      1                    
  2902: LCP      [sp+4]               
  2903: JZ       label_2936           
  2904: ASP      1                    
  2905: LCP      [sp+4]               
  2906: ASP      1                    
  2907: XCALL    $SC_P_Ai_GetDanger(unsignedlong)float ; args=1
  2908: LLD      [sp+5]               
  2909: SSP      1                    
  2910: LADR     [sp+3]               
  2911: ASGN                          
  2912: SSP      1                    
  2913: LCP      [sp+3]               
  2914: GCP      data[691]             ; = 4352
  2915: FGRE                          
  2916: JZ       label_2920           
  2917: GCP      data[692]             ; = 17
  2918: LLD      [sp-3]               
  2919: RET      5                    
label_2920:
  2920: ASP      1                    
  2921: LCP      [sp+4]               
  2922: ASP      1                    
  2923: XCALL    $SC_P_Ai_GetSureEnemies(unsignedlong)unsignedlong ; args=1
  2924: LLD      [sp+5]               
  2925: SSP      1                    
  2926: LADR     [sp+1]               
  2927: ASGN                          
  2928: SSP      1                    
  2929: LCP      [sp+1]               
  2930: GCP      data[693]             ; = 436207616
  2931: GRE                           
  2932: JZ       label_2936           
  2933: GCP      data[694]             ; = 1703936
  2934: LLD      [sp-3]               
  2935: RET      5                    
label_2936:
  2936: LCP      [sp+0]               
  2937: LCP      [sp+0]               
  2938: GCP      data[695]             ; = 6656
  2939: ADD                           
  2940: LADR     [sp+0]               
  2941: ASGN                          
  2942: SSP      1                    
  2943: SSP      1                    
  2944: JMP      label_2887           
label_2945:
  2945: GCP      data[696]             ; = 26
  2946: LLD      [sp-3]               
  2947: RET      5                    
  2948: ASP      1                    
  2949: ASP      1                    
  2950: ASP      1                    
  2951: ASP      1                    
  2952: ASP      1                    
  2953: GCP      data[697]             ; = 184549376
  2954: LADR     [sp+0]               
  2955: ASGN                          
  2956: SSP      1                    
label_2957:
  2957: LCP      [sp+0]               
  2958: GCP      data[698]             ; = 720896
  2959: LES                           
  2960: JZ       label_3015           
  2961: ASP      1                    
  2962: GCP      data[699]             ; = 2816
  2963: GCP      data[700]             ; = 11
  2964: LCP      [sp+0]               
  2965: ASP      1                    
  2966: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  2967: LLD      [sp+5]               
  2968: SSP      3                    
  2969: LADR     [sp+4]               
  2970: ASGN                          
  2971: SSP      1                    
  2972: LCP      [sp+4]               
  2973: JZ       label_3006           
  2974: ASP      1                    
  2975: LCP      [sp+4]               
  2976: ASP      1                    
  2977: XCALL    $SC_P_Ai_GetDanger(unsignedlong)float ; args=1
  2978: LLD      [sp+5]               
  2979: SSP      1                    
  2980: LADR     [sp+3]               
  2981: ASGN                          
  2982: SSP      1                    
  2983: LCP      [sp+3]               
  2984: GCP      data[701]             ; = 33554432
  2985: FGRE                          
  2986: JZ       label_2990           
  2987: GCP      data[702]             ; = 131072
  2988: LLD      [sp-3]               
  2989: RET      5                    
label_2990:
  2990: ASP      1                    
  2991: LCP      [sp+4]               
  2992: ASP      1                    
  2993: XCALL    $SC_P_Ai_GetSureEnemies(unsignedlong)unsignedlong ; args=1
  2994: LLD      [sp+5]               
  2995: SSP      1                    
  2996: LADR     [sp+1]               
  2997: ASGN                          
  2998: SSP      1                    
  2999: LCP      [sp+1]               
  3000: GCP      data[703]             ; = 512
  3001: GRE                           
  3002: JZ       label_3006           
  3003: GCP      data[704]             ; = 2
  3004: LLD      [sp-3]               
  3005: RET      5                    
label_3006:
  3006: LCP      [sp+0]               
  3007: LCP      [sp+0]               
  3008: GCP      data[705]             ; = 134217728
  3009: ADD                           
  3010: LADR     [sp+0]               
  3011: ASGN                          
  3012: SSP      1                    
  3013: SSP      1                    
  3014: JMP      label_2957           
label_3015:
  3015: GCP      data[706]             ; = 524288
  3016: LLD      [sp-3]               
  3017: RET      5                    
  3018: ASP      1                    
  3019: ASP      3                    
  3020: GCP      data[707]             ; = 2048
  3021: ASP      1                    
  3022: ASP      1                    
  3023: GCP      data[708]             ; = 8
  3024: LADR     [sp+0]               
  3025: ASGN                          
  3026: SSP      1                    
label_3027:
  3027: LCP      [sp+0]               
  3028: GCP      data[709]             ; = 318767104
  3029: LES                           
  3030: JZ       label_3075           
  3031: ASP      1                    
  3032: GCP      data[710]             ; = 1245184
  3033: GCP      data[711]             ; = 4864
  3034: LCP      [sp+0]               
  3035: ASP      1                    
  3036: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3037: LLD      [sp+7]               
  3038: SSP      3                    
  3039: LADR     [sp+6]               
  3040: ASGN                          
  3041: SSP      1                    
  3042: LCP      [sp+6]               
  3043: JZ       label_3066           
  3044: LCP      [sp+6]               
  3045: LADR     [sp+1]               
  3046: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  3047: SSP      2                    
  3048: ASP      1                    
  3049: LCP      [sp-4]               
  3050: LADR     [sp+1]               
  3051: ASP      1                    
  3052: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  3053: LLD      [sp+7]               
  3054: SSP      2                    
  3055: LADR     [sp+5]               
  3056: ASGN                          
  3057: SSP      1                    
  3058: LCP      [sp+5]               
  3059: LCP      [sp+4]               
  3060: FLES                          
  3061: JZ       label_3066           
  3062: LCP      [sp+5]               
  3063: LADR     [sp+4]               
  3064: ASGN                          
  3065: SSP      1                    
label_3066:
  3066: LCP      [sp+0]               
  3067: LCP      [sp+0]               
  3068: GCP      data[712]             ; = 19
  3069: ADD                           
  3070: LADR     [sp+0]               
  3071: ASGN                          
  3072: SSP      1                    
  3073: SSP      1                    
  3074: JMP      label_3027           
label_3075:
  3075: LCP      [sp+4]               
  3076: LLD      [sp-3]               
  3077: RET      7                    
func_3078:
  3078: ASP      1                    
  3079: ASP      1                    
  3080: GCP      data[713]             ; = 50331648
  3081: LCP      [sp-4]               
  3082: ASP      1                    
  3083: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  3084: LLD      [sp+1]               
  3085: SSP      2                    
  3086: LADR     [sp+0]               
  3087: ASGN                          
  3088: SSP      1                    
  3089: LCP      [sp+0]               
  3090: GCP      data[714]             ; = 196608
  3091: NEQ                           
  3092: JZ       label_3097           
  3093: LCP      [sp+0]               
  3094: LCP      [sp-3]               
  3095: XCALL    $SC_NOD_GetWorldPos(*void,*c_Vector3)void ; args=2
  3096: SSP      2                    
label_3097:
  3097: RET      1                    
  3098: ASP      1                    
  3099: ASP      1                    
  3100: GCP      data[715]             ; = 768
  3101: LCP      [sp-4]               
  3102: ASP      1                    
  3103: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  3104: LLD      [sp+1]               
  3105: SSP      2                    
  3106: LADR     [sp+0]               
  3107: ASGN                          
  3108: SSP      1                    
  3109: LCP      [sp+0]               
  3110: GCP      data[716]             ; = 3
  3111: NEQ                           
  3112: JZ       label_3121           
  3113: ASP      1                    
  3114: LCP      [sp+0]               
  3115: ASP      1                    
  3116: XCALL    $SC_NOD_GetWorldRotZ(*void)float ; args=1
  3117: LLD      [sp+1]               
  3118: SSP      1                    
  3119: LLD      [sp-3]               
  3120: RET      1                    
label_3121:
  3121: GCP      data[717]             ; = 100663296
  3122: LLD      [sp-3]               
  3123: RET      1                    
  3124: ASP      1                    
  3125: ASP      1                    
  3126: GCP      data[718]             ; = 393216
  3127: GCP      data[719]             ; = 1536
  3128: GCP      data[720]             ; = 6
  3129: ASP      1                    
  3130: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3131: LLD      [sp+1]               
  3132: SSP      3                    
  3133: ASP      1                    
  3134: XCALL    $SC_P_Ai_GetPeaceMode(unsignedlong)unsignedlong ; args=1
  3135: LLD      [sp+0]               
  3136: SSP      1                    
  3137: GCP      data[721]             ; = 385875968
  3138: EQU                           
  3139: JZ       label_3151           
  3140: ASP      1                    
  3141: GCP      data[722]             ; = 1507328
  3142: GCP      data[723]             ; = 5888
  3143: GCP      data[724]             ; = 23
  3144: ASP      1                    
  3145: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3146: LLD      [sp+0]               
  3147: SSP      3                    
  3148: GCP      data[725]             ; = 318767104
  3149: XCALL    $SC_P_Ai_SetPeaceMode(unsignedlong,unsignedlong)void ; args=2
  3150: SSP      2                    
label_3151:
  3151: ASP      1                    
  3152: GCP      data[726]             ; = 1245184
  3153: GCP      data[727]             ; = 4864
  3154: GCP      data[728]             ; = 19
  3155: ASP      1                    
  3156: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3157: LLD      [sp+0]               
  3158: SSP      3                    
  3159: XCALL    $SC_P_Ai_Stop(unsignedlong)void ; args=1
  3160: SSP      1                    
  3161: RET      0                    
  3162: ASP      3                    
  3163: LCP      [sp-4]               
  3164: LADR     [sp+0]               
  3165: CALL     func_3078            
  3166: SSP      2                    
  3167: LADR     [sp+0]               
  3168: LCP      [sp-3]               
  3169: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3170: SSP      2                    
  3171: RET      3                    
  3172: ASP      1                    
  3173: ASP      3                    
  3174: ASP      3                    
  3175: ASP      1                    
  3176: ASP      1                    
  3177: GCP      data[729]             ; = 469762048
  3178: LCP      [sp-3]               
  3179: ASP      1                    
  3180: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  3181: LLD      [sp+8]               
  3182: SSP      2                    
  3183: LADR     [sp+7]               
  3184: ASGN                          
  3185: SSP      1                    
  3186: LCP      [sp+7]               
  3187: JZ       label_3189           
  3188: JMP      label_3194           
label_3189:
  3189: GADR     data[730]            
  3190: GCP      data[739]             ; = 3840
  3191: XCALL    $SC_message(*char,...)void ; args=4294967295
  3192: SSP      1                    
  3193: RET      8                    
label_3194:
  3194: LCP      [sp+7]               
  3195: LADR     [sp+1]               
  3196: XCALL    $SC_NOD_GetWorldPos(*void,*c_Vector3)void ; args=2
  3197: SSP      2                    
  3198: ASP      1                    
  3199: LCP      [sp+7]               
  3200: ASP      1                    
  3201: XCALL    $SC_NOD_GetWorldRotZ(*void)float ; args=1
  3202: LLD      [sp+8]               
  3203: SSP      1                    
  3204: LADR     [sp+0]               
  3205: ASGN                          
  3206: SSP      1                    
  3207: LCP      [sp+0]               
  3208: GCP      data[740]             ; = 15
  3209: FSUB                          
  3210: LADR     [sp+0]               
  3211: ASGN                          
  3212: SSP      1                    
  3213: LADR     [sp+1]               
  3214: DCP      12                   
  3215: LADR     [sp+4]               
  3216: ASGN                          
  3217: SSP      3                    
  3218: LADR     [sp+4]               
  3219: DCP      4                    
  3220: GCP      data[741]             ; = 218103808
  3221: ASP      1                    
  3222: LCP      [sp+0]               
  3223: ASP      1                    
  3224: XCALL    $cos(float)float      ; args=1
  3225: LLD      [sp+10]              
  3226: SSP      1                    
  3227: FMUL                          
  3228: FSUB                          
  3229: LADR     [sp+4]               
  3230: ASGN                          
  3231: SSP      1                    
  3232: LADR     [sp+4]               
  3233: PNT      4                    
  3234: DCP      4                    
  3235: GCP      data[742]             ; = 851968
  3236: ASP      1                    
  3237: LCP      [sp+0]               
  3238: ASP      1                    
  3239: XCALL    $sin(float)float      ; args=1
  3240: LLD      [sp+10]              
  3241: SSP      1                    
  3242: FMUL                          
  3243: FADD                          
  3244: LADR     [sp+4]               
  3245: PNT      4                    
  3246: ASGN                          
  3247: SSP      1                    
  3248: LADR     [sp+4]               
  3249: GCP      data[743]             ; = 3328
  3250: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3251: SSP      2                    
  3252: LADR     [sp+1]               
  3253: DCP      12                   
  3254: LADR     [sp+4]               
  3255: ASGN                          
  3256: SSP      3                    
  3257: LADR     [sp+4]               
  3258: DCP      4                    
  3259: GCP      data[744]  ; "\r"     ; ""
  3260: ASP      1                    
  3261: LCP      [sp+0]               
  3262: ASP      1                    
  3263: XCALL    $cos(float)float      ; args=1
  3264: LLD      [sp+10]              
  3265: SSP      1                    
  3266: FMUL                          
  3267: FSUB                          
  3268: LADR     [sp+4]               
  3269: ASGN                          
  3270: SSP      1                    
  3271: LADR     [sp+4]               
  3272: PNT      4                    
  3273: DCP      4                    
  3274: GCP      data[745]             ; = 436207616
  3275: ASP      1                    
  3276: LCP      [sp+0]               
  3277: ASP      1                    
  3278: XCALL    $sin(float)float      ; args=1
  3279: LLD      [sp+10]              
  3280: SSP      1                    
  3281: FMUL                          
  3282: FADD                          
  3283: LADR     [sp+4]               
  3284: PNT      4                    
  3285: ASGN                          
  3286: SSP      1                    
  3287: LADR     [sp+4]               
  3288: GCP      data[746]             ; = 1703936
  3289: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3290: SSP      2                    
  3291: LADR     [sp+1]               
  3292: DCP      12                   
  3293: LADR     [sp+4]               
  3294: ASGN                          
  3295: SSP      3                    
  3296: LADR     [sp+4]               
  3297: DCP      4                    
  3298: GCP      data[747]             ; = 6656
  3299: ASP      1                    
  3300: LCP      [sp+0]               
  3301: ASP      1                    
  3302: XCALL    $cos(float)float      ; args=1
  3303: LLD      [sp+10]              
  3304: SSP      1                    
  3305: FMUL                          
  3306: FSUB                          
  3307: LADR     [sp+4]               
  3308: ASGN                          
  3309: SSP      1                    
  3310: LADR     [sp+4]               
  3311: PNT      4                    
  3312: DCP      4                    
  3313: GCP      data[748]             ; = 26
  3314: ASP      1                    
  3315: LCP      [sp+0]               
  3316: ASP      1                    
  3317: XCALL    $sin(float)float      ; args=1
  3318: LLD      [sp+10]              
  3319: SSP      1                    
  3320: FMUL                          
  3321: FADD                          
  3322: LADR     [sp+4]               
  3323: PNT      4                    
  3324: ASGN                          
  3325: SSP      1                    
  3326: LADR     [sp+4]               
  3327: GCP      data[749]             ; = 150994944
  3328: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3329: SSP      2                    
  3330: LCP      [sp+7]               
  3331: GCP      data[750]             ; = 589824
  3332: XCALL    $SC_DUMMY_Set_DoNotRenHier2(*void,int)void ; args=2
  3333: SSP      2                    
  3334: RET      8                    
  3335: ASP      1                    
  3336: ASP      3                    
  3337: ASP      3                    
  3338: LCP      [sp-6]               
  3339: LADR     [sp+4]               
  3340: CALL     func_3078            
  3341: SSP      2                    
  3342: LADR     [sp+4]               
  3343: PNT      8                    
  3344: DCP      4                    
  3345: LADR     [sp+1]               
  3346: PNT      8                    
  3347: ASGN                          
  3348: SSP      1                    
  3349: GCP      data[751]             ; = 2304
  3350: LADR     [sp+0]               
  3351: ASGN                          
  3352: SSP      1                    
label_3353:
  3353: LCP      [sp+0]               
  3354: LCP      [sp-4]               
  3355: LES                           
  3356: JZ       label_3396           
  3357: LADR     [sp+4]               
  3358: DCP      4                    
  3359: ASP      1                    
  3360: LCP      [sp-3]               
  3361: ASP      1                    
  3362: XCALL    $frnd(float)float     ; args=1
  3363: LLD      [sp+8]               
  3364: SSP      1                    
  3365: FADD                          
  3366: LADR     [sp+1]               
  3367: ASGN                          
  3368: SSP      1                    
  3369: LADR     [sp+4]               
  3370: PNT      4                    
  3371: DCP      4                    
  3372: ASP      1                    
  3373: LCP      [sp-3]               
  3374: ASP      1                    
  3375: XCALL    $frnd(float)float     ; args=1
  3376: LLD      [sp+8]               
  3377: SSP      1                    
  3378: FADD                          
  3379: LADR     [sp+1]               
  3380: PNT      4                    
  3381: ASGN                          
  3382: SSP      1                    
  3383: LADR     [sp+1]               
  3384: LCP      [sp-5]               
  3385: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3386: SSP      2                    
  3387: LCP      [sp+0]               
  3388: LCP      [sp+0]               
  3389: GCP      data[752]  ; "	"      ; "	"
  3390: ADD                           
  3391: LADR     [sp+0]               
  3392: ASGN                          
  3393: SSP      1                    
  3394: SSP      1                    
  3395: JMP      label_3353           
label_3396:
  3396: RET      7                    
  3397: ASP      3                    
  3398: ASP      1                    
  3399: LCP      [sp-4]               
  3400: LADR     [sp+0]               
  3401: ASP      1                    
  3402: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  3403: LLD      [sp+3]               
  3404: SSP      2                    
  3405: SSP      1                    
  3406: LADR     [sp+0]               
  3407: LCP      [sp-3]               
  3408: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3409: SSP      2                    
  3410: RET      3                    
  3411: ASP      3                    
  3412: ASP      1                    
  3413: LCP      [sp-3]               
  3414: LADR     [sp+0]               
  3415: ASP      1                    
  3416: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  3417: LLD      [sp+3]               
  3418: SSP      2                    
  3419: SSP      1                    
  3420: GCP      data[753]             ; = 33554432
  3421: LADR     [sp+0]               
  3422: XCALL    $SC_CreatePtc(unsignedlong,*c_Vector3)void ; args=2
  3423: SSP      2                    
  3424: RET      3                    
  3425: ASP      3                    
  3426: ASP      1                    
  3427: ASP      1                    
  3428: LCP      [sp-3]               
  3429: LADR     [sp+0]               
  3430: ASP      1                    
  3431: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  3432: LLD      [sp+4]               
  3433: SSP      2                    
  3434: SSP      1                    
  3435: LADR     [sp+0]               
  3436: GCP      data[754]             ; = 131072
  3437: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3438: SSP      2                    
  3439: GCP      data[755]             ; = 512
  3440: LADR     [sp+0]               
  3441: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  3442: SSP      2                    
  3443: GCP      data[756]             ; = 2
  3444: ASP      1                    
  3445: GCP      data[757]             ; = 100663296
  3446: LCP      [sp-3]               
  3447: ASP      1                    
  3448: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  3449: LLD      [sp+5]               
  3450: SSP      2                    
  3451: GCP      data[758]             ; = 393216
  3452: GCP      data[759]             ; = 1536
  3453: GCP      data[760]             ; = 6
  3454: GCP      data[761]             ; = 318767104
  3455: XCALL    $SC_CreatePtc_Ext(unsignedlong,*void,float,float,float,float)void ; args=6
  3456: SSP      6                    
  3457: GCP      data[762]             ; = 1245184
  3458: ASP      1                    
  3459: GCP      data[763]             ; = 4864
  3460: LCP      [sp-3]               
  3461: ASP      1                    
  3462: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  3463: LLD      [sp+5]               
  3464: SSP      2                    
  3465: GCP      data[764]             ; = 19
  3466: GCP      data[765]             ; = 50331648
  3467: GCP      data[766]             ; = 196608
  3468: GCP      data[767]             ; = 768
  3469: XCALL    $SC_CreatePtc_Ext(unsignedlong,*void,float,float,float,float)void ; args=6
  3470: SSP      6                    
  3471: GCP      data[768]             ; = 3
  3472: LADR     [sp+3]               
  3473: ASGN                          
  3474: SSP      1                    
label_3475:
  3475: LCP      [sp+3]               
  3476: GCP      data[769]             ; = 100663296
  3477: LES                           
  3478: JZ       label_3530           
  3479: ASP      1                    
  3480: LCP      [sp-3]               
  3481: LADR     [sp+0]               
  3482: ASP      1                    
  3483: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  3484: LLD      [sp+4]               
  3485: SSP      2                    
  3486: SSP      1                    
  3487: LADR     [sp+0]               
  3488: DCP      4                    
  3489: ASP      1                    
  3490: GCP      data[770]             ; = 393216
  3491: ASP      1                    
  3492: XCALL    $frnd(float)float     ; args=1
  3493: LLD      [sp+5]               
  3494: SSP      1                    
  3495: FADD                          
  3496: LADR     [sp+0]               
  3497: ASGN                          
  3498: SSP      1                    
  3499: LADR     [sp+0]               
  3500: PNT      4                    
  3501: DCP      4                    
  3502: ASP      1                    
  3503: GCP      data[771]             ; = 1536
  3504: ASP      1                    
  3505: XCALL    $frnd(float)float     ; args=1
  3506: LLD      [sp+5]               
  3507: SSP      1                    
  3508: FADD                          
  3509: LADR     [sp+0]               
  3510: PNT      4                    
  3511: ASGN                          
  3512: SSP      1                    
  3513: GCP      data[772]             ; = 6
  3514: LADR     [sp+0]               
  3515: GCP      data[773]             ; = 385875968
  3516: GCP      data[774]             ; = 1507328
  3517: GCP      data[775]             ; = 5888
  3518: GCP      data[776]             ; = 23
  3519: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3520: SSP      6                    
  3521: LCP      [sp+3]               
  3522: LCP      [sp+3]               
  3523: GCP      data[777]             ; = 335544320
  3524: ADD                           
  3525: LADR     [sp+3]               
  3526: ASGN                          
  3527: SSP      1                    
  3528: SSP      1                    
  3529: JMP      label_3475           
label_3530:
  3530: RET      4                    
  3531: ASP      1                    
  3532: GCP      data[778]             ; = 1310720
  3533: LCP      [sp-3]               
  3534: XCALL    $SC_CreatePtc(unsignedlong,*c_Vector3)void ; args=2
  3535: SSP      2                    
  3536: GCP      data[779]             ; = 5120
  3537: LCP      [sp-3]               
  3538: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  3539: SSP      2                    
  3540: GCP      data[780]             ; = 20
  3541: LCP      [sp-3]               
  3542: GCP      data[781]             ; = 301989888
  3543: GCP      data[782]             ; = 1179648
  3544: GCP      data[783]             ; = 4608
  3545: GCP      data[784]             ; = 18
  3546: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3547: SSP      6                    
  3548: GCP      data[785]             ; = 234881024
  3549: LCP      [sp-3]               
  3550: GCP      data[786]             ; = 917504
  3551: GCP      data[787]             ; = 3584
  3552: GCP      data[788]             ; = 14
  3553: GCP      data[789]             ; = 268435456
  3554: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3555: SSP      6                    
  3556: RET      1                    
  3557: ASP      1                    
  3558: ASP      3                    
  3559: LADR     [sp-5]               
  3560: DADR     data[8]              
  3561: DCP      4                    
  3562: LADR     [sp+1]               
  3563: PNT      8                    
  3564: ASGN                          
  3565: SSP      1                    
  3566: GCP      data[790]             ; = 1048576
  3567: LADR     [sp+0]               
  3568: ASGN                          
  3569: SSP      1                    
label_3570:
  3570: LCP      [sp+0]               
  3571: LCP      [sp-4]               
  3572: LES                           
  3573: JZ       label_3622           
  3574: LADR     [sp-5]               
  3575: DADR     data[0]              
  3576: DCP      4                    
  3577: ASP      1                    
  3578: LCP      [sp-3]               
  3579: ASP      1                    
  3580: XCALL    $frnd(float)float     ; args=1
  3581: LLD      [sp+5]               
  3582: SSP      1                    
  3583: FADD                          
  3584: LADR     [sp+1]               
  3585: ASGN                          
  3586: SSP      1                    
  3587: LADR     [sp-5]               
  3588: DADR     data[4]              
  3589: DCP      4                    
  3590: ASP      1                    
  3591: LCP      [sp-3]               
  3592: ASP      1                    
  3593: XCALL    $frnd(float)float     ; args=1
  3594: LLD      [sp+5]               
  3595: SSP      1                    
  3596: FADD                          
  3597: LADR     [sp+1]               
  3598: PNT      4                    
  3599: ASGN                          
  3600: SSP      1                    
  3601: GCP      data[791]             ; = 4096
  3602: LADR     [sp+1]               
  3603: XCALL    $SC_CreatePtc(unsignedlong,*c_Vector3)void ; args=2
  3604: SSP      2                    
  3605: GCP      data[792]             ; = 16
  3606: LADR     [sp+1]               
  3607: GCP      data[793]             ; = 301989888
  3608: GCP      data[794]             ; = 1179648
  3609: GCP      data[795]             ; = 4608
  3610: GCP      data[796]             ; = 18
  3611: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3612: SSP      6                    
  3613: LCP      [sp+0]               
  3614: LCP      [sp+0]               
  3615: GCP      data[797]             ; = 201326592
  3616: ADD                           
  3617: LADR     [sp+0]               
  3618: ASGN                          
  3619: SSP      1                    
  3620: SSP      1                    
  3621: JMP      label_3570           
label_3622:
  3622: GCP      data[798]             ; = 786432
  3623: LCP      [sp-5]               
  3624: GCP      data[799]             ; = 3072
  3625: GCP      data[800]             ; = 12
  3626: GCP      data[801]             ; = 33554432
  3627: GCP      data[802]             ; = 131072
  3628: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3629: SSP      6                    
  3630: RET      4                    
  3631: ASP      1                    
  3632: ASP      3                    
  3633: LADR     [sp-5]               
  3634: DADR     data[8]              
  3635: DCP      4                    
  3636: LADR     [sp+1]               
  3637: PNT      8                    
  3638: ASGN                          
  3639: SSP      1                    
  3640: GCP      data[803]             ; = 512
  3641: LADR     [sp+0]               
  3642: ASGN                          
  3643: SSP      1                    
label_3644:
  3644: LCP      [sp+0]               
  3645: LCP      [sp-4]               
  3646: LES                           
  3647: JZ       label_3688           
  3648: LADR     [sp-5]               
  3649: DADR     data[0]              
  3650: DCP      4                    
  3651: ASP      1                    
  3652: LCP      [sp-3]               
  3653: ASP      1                    
  3654: XCALL    $frnd(float)float     ; args=1
  3655: LLD      [sp+5]               
  3656: SSP      1                    
  3657: FADD                          
  3658: LADR     [sp+1]               
  3659: ASGN                          
  3660: SSP      1                    
  3661: LADR     [sp-5]               
  3662: DADR     data[4]              
  3663: DCP      4                    
  3664: ASP      1                    
  3665: LCP      [sp-3]               
  3666: ASP      1                    
  3667: XCALL    $frnd(float)float     ; args=1
  3668: LLD      [sp+5]               
  3669: SSP      1                    
  3670: FADD                          
  3671: LADR     [sp+1]               
  3672: PNT      4                    
  3673: ASGN                          
  3674: SSP      1                    
  3675: GCP      data[804]             ; = 2
  3676: LADR     [sp+1]               
  3677: XCALL    $SC_CreatePtc(unsignedlong,*c_Vector3)void ; args=2
  3678: SSP      2                    
  3679: LCP      [sp+0]               
  3680: LCP      [sp+0]               
  3681: GCP      data[805]             ; = 134217728
  3682: ADD                           
  3683: LADR     [sp+0]               
  3684: ASGN                          
  3685: SSP      1                    
  3686: SSP      1                    
  3687: JMP      label_3644           
label_3688:
  3688: GCP      data[806]             ; = 524288
  3689: LCP      [sp-5]               
  3690: GCP      data[807]             ; = 2048
  3691: GCP      data[808]             ; = 8
  3692: GCP      data[809]             ; = 251658240
  3693: GCP      data[810]             ; = 983040
  3694: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3695: SSP      6                    
  3696: RET      4                    
  3697: ASP      1                    
  3698: ASP      3                    
  3699: LADR     [sp-5]               
  3700: DADR     data[8]              
  3701: DCP      4                    
  3702: LADR     [sp+1]               
  3703: PNT      8                    
  3704: ASGN                          
  3705: SSP      1                    
  3706: GCP      data[811]             ; = 3840
  3707: LADR     [sp+0]               
  3708: ASGN                          
  3709: SSP      1                    
label_3710:
  3710: LCP      [sp+0]               
  3711: LCP      [sp-4]               
  3712: LES                           
  3713: JZ       label_3754           
  3714: LADR     [sp-5]               
  3715: DADR     data[0]              
  3716: DCP      4                    
  3717: ASP      1                    
  3718: LCP      [sp-3]               
  3719: ASP      1                    
  3720: XCALL    $frnd(float)float     ; args=1
  3721: LLD      [sp+5]               
  3722: SSP      1                    
  3723: FADD                          
  3724: LADR     [sp+1]               
  3725: ASGN                          
  3726: SSP      1                    
  3727: LADR     [sp-5]               
  3728: DADR     data[4]              
  3729: DCP      4                    
  3730: ASP      1                    
  3731: LCP      [sp-3]               
  3732: ASP      1                    
  3733: XCALL    $frnd(float)float     ; args=1
  3734: LLD      [sp+5]               
  3735: SSP      1                    
  3736: FADD                          
  3737: LADR     [sp+1]               
  3738: PNT      4                    
  3739: ASGN                          
  3740: SSP      1                    
  3741: GCP      data[812]             ; = 15
  3742: LADR     [sp+1]               
  3743: XCALL    $SC_CreatePtc(unsignedlong,*c_Vector3)void ; args=2
  3744: SSP      2                    
  3745: LCP      [sp+0]               
  3746: LCP      [sp+0]               
  3747: GCP      data[813]             ; = 33554432
  3748: ADD                           
  3749: LADR     [sp+0]               
  3750: ASGN                          
  3751: SSP      1                    
  3752: SSP      1                    
  3753: JMP      label_3710           
label_3754:
  3754: RET      4                    
  3755: ASP      3                    
  3756: ASP      32                   
  3757: LADR     [sp+3]               
  3758: GCP      data[814]             ; = 131072
  3759: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  3760: SSP      2                    
  3761: LCP      [sp-3]               
  3762: LADR     [sp+3]               
  3763: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  3764: SSP      2                    
  3765: GCP      data[815]             ; = 512
  3766: LADR     [sp+3]               
  3767: PNT      76                   
  3768: ASGN                          
  3769: SSP      1                    
  3770: GCP      data[816]             ; = 2
  3771: LADR     [sp+3]               
  3772: PNT      12                   
  3773: ASGN                          
  3774: SSP      1                    
  3775: LCP      [sp-3]               
  3776: LADR     [sp+3]               
  3777: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  3778: SSP      2                    
  3779: GCP      data[817]             ; = 335544320
  3780: LADR     [sp+0]               
  3781: PNT      4                    
  3782: ASGN                          
  3783: SSP      1                    
  3784: GCP      data[818]             ; = 1310720
  3785: LADR     [sp+0]               
  3786: ASGN                          
  3787: SSP      1                    
  3788: GCP      data[819]             ; = 5120
  3789: LADR     [sp+0]               
  3790: PNT      8                    
  3791: ASGN                          
  3792: SSP      1                    
  3793: LCP      [sp-3]               
  3794: LADR     [sp+0]               
  3795: XCALL    $SC_P_Ai_SetBattleProps(unsignedlong,*s_SC_P_Ai_BattleProps)void ; args=2
  3796: SSP      2                    
  3797: RET      35                   
  3798: ASP      3                    
  3799: ASP      1                    
  3800: LCP      [sp-4]               
  3801: LADR     [sp+0]               
  3802: XCALL    $SC_P_GetDir(unsignedlong,*c_Vector3)void ; args=2
  3803: SSP      2                    
  3804: ASP      1                    
  3805: LADR     [sp+0]               
  3806: ASP      1                    
  3807: XCALL    $SC_VectorLen(*c_Vector3)float ; args=1
  3808: LLD      [sp+4]               
  3809: SSP      1                    
  3810: LADR     [sp+3]               
  3811: ASGN                          
  3812: SSP      1                    
  3813: LCP      [sp+3]               
  3814: GCP      data[820]             ; = 20
  3815: FGRE                          
  3816: JZ       label_3820           
  3817: GCP      data[821]             ; = 3355443200
  3818: LLD      [sp-3]               
  3819: RET      4                    
label_3820:
  3820: GCP      data[822]             ; = 13107200
  3821: LLD      [sp-3]               
  3822: RET      4                    
  3823: ASP      1                    
  3824: GCP      data[823]             ; = 51200
  3825: ASP      1                    
  3826: ASP      3                    
  3827: GCP      data[824]  ; "È"      ; "È"
  3828: LADR     [sp+0]               
  3829: ASGN                          
  3830: SSP      1                    
label_3831:
  3831: LCP      [sp+0]               
  3832: GCP      data[825]             ; = 16777216
  3833: LES                           
  3834: JZ       label_3887           
  3835: ASP      1                    
  3836: ASP      1                    
  3837: GCP      data[826]             ; = 65536
  3838: GCP      data[827]             ; = 256
  3839: LCP      [sp+0]               
  3840: ASP      1                    
  3841: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3842: LLD      [sp+7]               
  3843: SSP      3                    
  3844: ASP      1                    
  3845: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  3846: LLD      [sp+6]               
  3847: SSP      1                    
  3848: JZ       label_3878           
  3849: ASP      1                    
  3850: GCP      data[828]             ; = 1
  3851: GCP      data[829]             ; = 167772160
  3852: LCP      [sp+0]               
  3853: ASP      1                    
  3854: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3855: LLD      [sp+6]               
  3856: SSP      3                    
  3857: LADR     [sp+3]               
  3858: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  3859: SSP      2                    
  3860: ASP      1                    
  3861: LADR     [sp+3]               
  3862: LCP      [sp-4]               
  3863: ASP      1                    
  3864: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  3865: LLD      [sp+6]               
  3866: SSP      2                    
  3867: LADR     [sp+2]               
  3868: ASGN                          
  3869: SSP      1                    
  3870: LCP      [sp+2]               
  3871: LCP      [sp+1]               
  3872: FLES                          
  3873: JZ       label_3878           
  3874: LCP      [sp+2]               
  3875: LADR     [sp+1]               
  3876: ASGN                          
  3877: SSP      1                    
label_3878:
  3878: LCP      [sp+0]               
  3879: LCP      [sp+0]               
  3880: GCP      data[830]             ; = 655360
  3881: ADD                           
  3882: LADR     [sp+0]               
  3883: ASGN                          
  3884: SSP      1                    
  3885: SSP      1                    
  3886: JMP      label_3831           
label_3887:
  3887: LCP      [sp+1]               
  3888: LLD      [sp-3]               
  3889: RET      6                    
  3890: ASP      3                    
  3891: LCP      [sp-6]               
  3892: LADR     [sp+0]               
  3893: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  3894: SSP      2                    
  3895: ASP      1                    
  3896: LADR     [sp+0]               
  3897: LCP      [sp-5]               
  3898: LCP      [sp-4]               
  3899: ASP      1                    
  3900: XCALL    $SC_IsNear3D(*c_Vector3,*c_Vector3,float)int ; args=3
  3901: LLD      [sp+3]               
  3902: SSP      3                    
  3903: LLD      [sp-3]               
  3904: RET      3                    
  3905: ASP      3                    
  3906: ASP      1                    
  3907: LADR     [sp+0]               
  3908: ASP      1                    
  3909: XCALL    $SC_PC_GetPos(*c_Vector3)int ; args=1
  3910: LLD      [sp+3]               
  3911: SSP      1                    
  3912: SSP      1                    
  3913: ASP      1                    
  3914: LADR     [sp+0]               
  3915: LCP      [sp-5]               
  3916: LCP      [sp-4]               
  3917: ASP      1                    
  3918: XCALL    $SC_IsNear3D(*c_Vector3,*c_Vector3,float)int ; args=3
  3919: LLD      [sp+3]               
  3920: SSP      3                    
  3921: LLD      [sp-3]               
  3922: RET      3                    
  3923: ASP      32                   
  3924: LCP      [sp-7]               
  3925: JZ       label_3927           
  3926: JMP      label_3928           
label_3927:
  3927: RET      32                   
label_3928:
  3928: LADR     [sp+0]               
  3929: GCP      data[831]             ; = 2560
  3930: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  3931: SSP      2                    
  3932: LCP      [sp-7]               
  3933: LADR     [sp+0]               
  3934: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  3935: SSP      2                    
  3936: LCP      [sp-6]               
  3937: LADR     [sp+0]               
  3938: PNT      52                   
  3939: ASGN                          
  3940: SSP      1                    
  3941: LCP      [sp-5]               
  3942: LADR     [sp+0]               
  3943: PNT      56                   
  3944: ASGN                          
  3945: SSP      1                    
  3946: LCP      [sp-4]               
  3947: LADR     [sp+0]               
  3948: PNT      60                   
  3949: ASGN                          
  3950: SSP      1                    
  3951: LCP      [sp-3]               
  3952: LADR     [sp+0]               
  3953: PNT      64                   
  3954: ASGN                          
  3955: SSP      1                    
  3956: LCP      [sp-7]               
  3957: LADR     [sp+0]               
  3958: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  3959: SSP      2                    
  3960: RET      32                   
  3961: ASP      1                    
  3962: ASP      1                    
  3963: ASP      32                   
  3964: ASP      1                    
  3965: ASP      4                    
  3966: ASP      5                    
  3967: ASP      3                    
  3968: ASP      1                    
  3969: ASP      1                    
  3970: GCP      data[832]  ; "\n"     ; "
"
  3971: LADR     [sp+47]              
  3972: ASGN                          
  3973: SSP      1                    
  3974: GCP      data[833]             ; = 318767104
  3975: LADR     [sp+35]              
  3976: PNT      12                   
  3977: ASGN                          
  3978: SSP      1                    
  3979: LCP      [sp-4]               
  3980: DCP      12                   
  3981: LADR     [sp+35]              
  3982: ASGN                          
  3983: SSP      3                    
  3984: GCP      data[834]             ; = 1245184
  3985: LADR     [sp+0]               
  3986: ASGN                          
  3987: SSP      1                    
  3988: LADR     [sp+35]              
  3989: LADR     [sp+2]               
  3990: LADR     [sp+0]               
  3991: XCALL    $SC_GetPls(*s_sphere,*unsignedlong,*unsignedlong)void ; args=3
  3992: SSP      3                    
  3993: GCP      data[835]             ; = 4864
  3994: LADR     [sp+34]              
  3995: ASGN                          
  3996: SSP      1                    
  3997: GCP      data[836]             ; = 19
  3998: LADR     [sp+1]               
  3999: ASGN                          
  4000: SSP      1                    
label_4001:
  4001: LCP      [sp+1]               
  4002: LCP      [sp+0]               
  4003: LES                           
  4004: JZ       label_4083           
  4005: LADR     [sp+2]               
  4006: LCP      [sp+1]               
  4007: GCP      data[837]             ; = 436207616
  4008: MUL                           
  4009: ADD                           
  4010: DCP      4                    
  4011: LADR     [sp+39]              
  4012: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4013: SSP      2                    
  4014: LADR     [sp+39]              
  4015: PNT      8                    
  4016: DCP      4                    
  4017: LCP      [sp-5]               
  4018: EQU                           
  4019: JNZ      label_4025           
  4020: LCP      [sp-5]               
  4021: GCP      data[838]             ; = 1703936
  4022: EQU                           
  4023: JNZ      label_4025           
  4024: JMP      label_4074           
label_4025:
  4025: ASP      1                    
  4026: LADR     [sp+2]               
  4027: LCP      [sp+1]               
  4028: GCP      data[839]             ; = 6656
  4029: MUL                           
  4030: ADD                           
  4031: DCP      4                    
  4032: ASP      1                    
  4033: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  4034: LLD      [sp+49]              
  4035: SSP      1                    
  4036: JZ       label_4074           
  4037: JMP      label_4038           
label_4038:
  4038: LADR     [sp+2]               
  4039: LCP      [sp+1]               
  4040: GCP      data[840]             ; = 26
  4041: MUL                           
  4042: ADD                           
  4043: DCP      4                    
  4044: LADR     [sp+44]              
  4045: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  4046: SSP      2                    
  4047: ASP      1                    
  4048: LADR     [sp+44]              
  4049: LCP      [sp-4]               
  4050: ASP      1                    
  4051: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  4052: LLD      [sp+49]              
  4053: SSP      2                    
  4054: LADR     [sp+48]              
  4055: ASGN                          
  4056: SSP      1                    
  4057: LCP      [sp+48]              
  4058: LCP      [sp+47]              
  4059: FLES                          
  4060: JZ       label_4074           
  4061: LCP      [sp+48]              
  4062: LADR     [sp+47]              
  4063: ASGN                          
  4064: SSP      1                    
  4065: LADR     [sp+2]               
  4066: LCP      [sp+1]               
  4067: GCP      data[841]             ; = 33554432
  4068: MUL                           
  4069: ADD                           
  4070: DCP      4                    
  4071: LADR     [sp+34]              
  4072: ASGN                          
  4073: SSP      1                    
label_4074:
  4074: LCP      [sp+1]               
  4075: LCP      [sp+1]               
  4076: GCP      data[842]             ; = 131072
  4077: ADD                           
  4078: LADR     [sp+1]               
  4079: ASGN                          
  4080: SSP      1                    
  4081: SSP      1                    
  4082: JMP      label_4001           
label_4083:
  4083: LCP      [sp+34]              
  4084: LLD      [sp-3]               
  4085: RET      49                   
func_4086:
  4086: ASP      1                    
  4087: ASP      1                    
  4088: ASP      1                    
  4089: ASP      1                    
  4090: ASP      32                   
  4091: ASP      4                    
  4092: ASP      5                    
  4093: LCP      [sp-5]               
  4094: LADR     [sp+40]              
  4095: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4096: SSP      2                    
  4097: LADR     [sp+40]              
  4098: PNT      12                   
  4099: DCP      4                    
  4100: LADR     [sp+3]               
  4101: ASGN                          
  4102: SSP      1                    
  4103: LCP      [sp-5]               
  4104: LADR     [sp+36]              
  4105: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  4106: SSP      2                    
  4107: GCP      data[843]             ; = 512
  4108: LADR     [sp+36]              
  4109: PNT      12                   
  4110: ASGN                          
  4111: SSP      1                    
  4112: GCP      data[844]             ; = 2
  4113: LADR     [sp+0]               
  4114: ASGN                          
  4115: SSP      1                    
  4116: LADR     [sp+36]              
  4117: LADR     [sp+4]               
  4118: LADR     [sp+0]               
  4119: XCALL    $SC_GetPls(*s_sphere,*unsignedlong,*unsignedlong)void ; args=3
  4120: SSP      3                    
  4121: GCP      data[845]             ; = 50331648
  4122: LADR     [sp+2]               
  4123: ASGN                          
  4124: SSP      1                    
  4125: GCP      data[846]             ; = 196608
  4126: LADR     [sp+1]               
  4127: ASGN                          
  4128: SSP      1                    
label_4129:
  4129: LCP      [sp+1]               
  4130: LCP      [sp+0]               
  4131: LES                           
  4132: JZ       label_4208           
  4133: LADR     [sp+4]               
  4134: LCP      [sp+1]               
  4135: GCP      data[847]             ; = 768
  4136: MUL                           
  4137: ADD                           
  4138: DCP      4                    
  4139: LADR     [sp+40]              
  4140: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4141: SSP      2                    
  4142: LADR     [sp+40]              
  4143: PNT      8                    
  4144: DCP      4                    
  4145: GCP      data[848]             ; = 3
  4146: EQU                           
  4147: JZ       label_4199           
  4148: LADR     [sp+40]              
  4149: PNT      12                   
  4150: DCP      4                    
  4151: LCP      [sp+3]               
  4152: EQU                           
  4153: JZ       label_4199           
  4154: JMP      label_4155           
label_4155:
  4155: ASP      1                    
  4156: LADR     [sp+4]               
  4157: LCP      [sp+1]               
  4158: GCP      data[849]             ; = 67108864
  4159: MUL                           
  4160: ADD                           
  4161: DCP      4                    
  4162: ASP      1                    
  4163: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  4164: LLD      [sp+45]              
  4165: SSP      1                    
  4166: JZ       label_4199           
  4167: JMP      label_4168           
label_4168:
  4168: LADR     [sp+4]               
  4169: LCP      [sp+1]               
  4170: GCP      data[850]             ; = 262144
  4171: MUL                           
  4172: ADD                           
  4173: DCP      4                    
  4174: LCP      [sp-4]               
  4175: LCP      [sp+2]               
  4176: GCP      data[851]             ; = 1024
  4177: MUL                           
  4178: ADD                           
  4179: ASGN                          
  4180: SSP      1                    
  4181: LCP      [sp+2]               
  4182: LCP      [sp+2]               
  4183: GCP      data[852]             ; = 4
  4184: ADD                           
  4185: LADR     [sp+2]               
  4186: ASGN                          
  4187: SSP      1                    
  4188: SSP      1                    
  4189: LCP      [sp+2]               
  4190: LCP      [sp-3]               
  4191: EQU                           
  4192: JZ       label_4199           
  4193: GCP      data[853]             ; = 83886080
  4194: GADR     data[854]            
  4195: GCP      data[866]             ; = 524288
  4196: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  4197: SSP      2                    
  4198: RET      45                   
label_4199:
  4199: LCP      [sp+1]               
  4200: LCP      [sp+1]               
  4201: GCP      data[867]             ; = 2048
  4202: ADD                           
  4203: LADR     [sp+1]               
  4204: ASGN                          
  4205: SSP      1                    
  4206: SSP      1                    
  4207: JMP      label_4129           
label_4208:
  4208: LCP      [sp+2]               
  4209: LCP      [sp-3]               
  4210: ASGN                          
  4211: SSP      1                    
  4212: RET      45                   
  4213: ASP      1                    
  4214: ASP      1                    
  4215: ASP      32                   
  4216: ASP      5                    
  4217: GCP      data[868]             ; = 8
  4218: LADR     [sp+0]               
  4219: ASGN                          
  4220: SSP      1                    
  4221: LCP      [sp-3]               
  4222: LADR     [sp+2]               
  4223: LADR     [sp+0]               
  4224: CALL     func_4086            
  4225: SSP      3                    
  4226: LCP      [sp-3]               
  4227: LADR     [sp+34]              
  4228: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4229: SSP      2                    
  4230: LCP      [sp+0]               
  4231: GCP      data[869]             ; = 100663296
  4232: LES                           
  4233: JZ       label_4249           
  4234: GCP      data[870]             ; = 393216
  4235: GADR     data[871]            
  4236: LADR     [sp+34]              
  4237: PNT      12                   
  4238: DCP      4                    
  4239: LADR     [sp+34]              
  4240: PNT      16                   
  4241: DCP      4                    
  4242: LADR     [sp+34]              
  4243: PNT      12                   
  4244: DCP      4                    
  4245: GCP      data[883]             ; = 4352
  4246: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  4247: SSP      5                    
  4248: RET      39                   
label_4249:
  4249: LADR     [sp+2]               
  4250: GCP      data[884]             ; = 17
  4251: ADD                           
  4252: DCP      4                    
  4253: LCP      [sp-3]               
  4254: NEQ                           
  4255: JZ       label_4265           
  4256: LADR     [sp+2]               
  4257: GCP      data[885]             ; = 234881024
  4258: ADD                           
  4259: DCP      4                    
  4260: GCP      data[886]             ; = 917504
  4261: GCP      data[887]             ; = 3584
  4262: CALL     func_0064            
  4263: SSP      3                    
  4264: JMP      label_4273           
label_4265:
  4265: LADR     [sp+2]               
  4266: GCP      data[888]             ; = 14
  4267: ADD                           
  4268: DCP      4                    
  4269: GCP      data[889]             ; = 436207616
  4270: GCP      data[890]             ; = 1703936
  4271: CALL     func_0064            
  4272: SSP      3                    
label_4273:
  4273: GCP      data[891]             ; = 6656
  4274: GADR     data[892]            
  4275: LADR     [sp+34]              
  4276: PNT      12                   
  4277: DCP      4                    
  4278: LADR     [sp+34]              
  4279: PNT      16                   
  4280: DCP      4                    
  4281: GCP      data[901]             ; = 83886080
  4282: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  4283: SSP      4                    
  4284: RET      39                   
  4285: ASP      3                    
  4286: ASP      1                    
  4287: LCP      [sp-5]               
  4288: LADR     [sp+0]               
  4289: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  4290: SSP      2                    
  4291: ASP      1                    
  4292: LCP      [sp-4]               
  4293: LADR     [sp+0]               
  4294: ASP      1                    
  4295: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  4296: LLD      [sp+4]               
  4297: SSP      2                    
  4298: LADR     [sp+3]               
  4299: ASGN                          
  4300: SSP      1                    
  4301: LCP      [sp+3]               
  4302: LLD      [sp-3]               
  4303: RET      4                    
  4304: ASP      5                    
  4305: LADR     [sp+0]               
  4306: GCP      data[902]             ; = 327680
  4307: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  4308: SSP      2                    
  4309: GCP      data[903]             ; = 1280
  4310: LADR     [sp+0]               
  4311: GCP      data[904]             ; = 5
  4312: ADD                           
  4313: ASGN                          
  4314: SSP      1                    
  4315: GCP      data[905]             ; = 100663296
  4316: LADR     [sp+0]               
  4317: GCP      data[906]             ; = 393216
  4318: ADD                           
  4319: ASGN                          
  4320: SSP      1                    
  4321: GCP      data[907]             ; = 1536
  4322: LADR     [sp+0]               
  4323: GCP      data[908]             ; = 6
  4324: ADD                           
  4325: ASGN                          
  4326: SSP      1                    
  4327: GCP      data[909]             ; = 385875968
  4328: LADR     [sp+0]               
  4329: GCP      data[910]             ; = 1507328
  4330: ADD                           
  4331: ASGN                          
  4332: SSP      1                    
  4333: GCP      data[911]             ; = 5888
  4334: LADR     [sp+0]               
  4335: GCP      data[912]             ; = 23
  4336: ADD                           
  4337: ASGN                          
  4338: SSP      1                    
  4339: LCP      [sp-3]               
  4340: LADR     [sp+0]               
  4341: XCALL    $SC_P_SetSpecAnims(unsignedlong,*s_SC_P_SpecAnims)void ; args=2
  4342: SSP      2                    
  4343: RET      5                    
  4344: ASP      5                    
  4345: LADR     [sp+0]               
  4346: GCP      data[913]             ; = 100663296
  4347: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  4348: SSP      2                    
  4349: LCP      [sp-7]               
  4350: LADR     [sp+0]               
  4351: GCP      data[914]             ; = 393216
  4352: ADD                           
  4353: ASGN                          
  4354: SSP      1                    
  4355: LCP      [sp-6]               
  4356: LADR     [sp+0]               
  4357: GCP      data[915]             ; = 1536
  4358: ADD                           
  4359: ASGN                          
  4360: SSP      1                    
  4361: LCP      [sp-5]               
  4362: LADR     [sp+0]               
  4363: GCP      data[916]             ; = 6
  4364: ADD                           
  4365: ASGN                          
  4366: SSP      1                    
  4367: LCP      [sp-4]               
  4368: LADR     [sp+0]               
  4369: GCP      data[917]             ; = 251658240
  4370: ADD                           
  4371: ASGN                          
  4372: SSP      1                    
  4373: LCP      [sp-3]               
  4374: LADR     [sp+0]               
  4375: GCP      data[918]             ; = 983040
  4376: ADD                           
  4377: ASGN                          
  4378: SSP      1                    
  4379: LCP      [sp-8]               
  4380: LADR     [sp+0]               
  4381: XCALL    $SC_P_SetSpecAnims(unsignedlong,*s_SC_P_SpecAnims)void ; args=2
  4382: SSP      2                    
  4383: RET      5                    
  4384: ASP      1                    
  4385: ASP      1                    
  4386: ASP      1                    
  4387: ASP      1                    
  4388: ASP      32                   
  4389: GCP      data[919]             ; = 3840
  4390: LADR     [sp+0]               
  4391: ASGN                          
  4392: SSP      1                    
  4393: LCP      [sp-4]               
  4394: LADR     [sp+4]               
  4395: LADR     [sp+0]               
  4396: XCALL    $SC_GetPls(*s_sphere,*unsignedlong,*unsignedlong)void ; args=3
  4397: SSP      3                    
  4398: LCP      [sp+0]               
  4399: JZ       label_4401           
  4400: JMP      label_4402           
label_4401:
  4401: RET      36                   
label_4402:
  4402: GCP      data[920]             ; = 15
  4403: LADR     [sp+1]               
  4404: ASGN                          
  4405: SSP      1                    
label_4406:
  4406: LCP      [sp+1]               
  4407: LCP      [sp+0]               
  4408: LES                           
  4409: JZ       label_4503           
  4410: LADR     [sp+4]               
  4411: LCP      [sp+1]               
  4412: GCP      data[921]             ; = 436207616
  4413: MUL                           
  4414: ADD                           
  4415: DCP      4                    
  4416: GCP      data[922]             ; = 1703936
  4417: LCP      [sp-3]               
  4418: GCP      data[923]             ; = 6656
  4419: FDIV                          
  4420: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4421: SSP      3                    
  4422: LADR     [sp+4]               
  4423: LCP      [sp+1]               
  4424: GCP      data[924]             ; = 26
  4425: MUL                           
  4426: ADD                           
  4427: DCP      4                    
  4428: GCP      data[925]             ; = 184549376
  4429: LCP      [sp-3]               
  4430: GCP      data[926]             ; = 720896
  4431: FDIV                          
  4432: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4433: SSP      3                    
  4434: LADR     [sp+4]               
  4435: LCP      [sp+1]               
  4436: GCP      data[927]             ; = 2816
  4437: MUL                           
  4438: ADD                           
  4439: DCP      4                    
  4440: GCP      data[928]             ; = 11
  4441: LCP      [sp-3]               
  4442: GCP      data[929]             ; = 318767104
  4443: FDIV                          
  4444: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4445: SSP      3                    
  4446: LADR     [sp+4]               
  4447: LCP      [sp+1]               
  4448: GCP      data[930]             ; = 1245184
  4449: MUL                           
  4450: ADD                           
  4451: DCP      4                    
  4452: GCP      data[931]             ; = 4864
  4453: LCP      [sp-3]               
  4454: GCP      data[932]             ; = 19
  4455: FDIV                          
  4456: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4457: SSP      3                    
  4458: LADR     [sp+4]               
  4459: LCP      [sp+1]               
  4460: GCP      data[933]             ; = 117440512
  4461: MUL                           
  4462: ADD                           
  4463: DCP      4                    
  4464: GCP      data[934]             ; = 458752
  4465: LCP      [sp-3]               
  4466: GCP      data[935]             ; = 1792
  4467: FDIV                          
  4468: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4469: SSP      3                    
  4470: LADR     [sp+4]               
  4471: LCP      [sp+1]               
  4472: GCP      data[936]             ; = 7
  4473: MUL                           
  4474: ADD                           
  4475: DCP      4                    
  4476: GCP      data[937]             ; = 100663296
  4477: LCP      [sp-3]               
  4478: GCP      data[938]             ; = 393216
  4479: FDIV                          
  4480: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4481: SSP      3                    
  4482: LADR     [sp+4]               
  4483: LCP      [sp+1]               
  4484: GCP      data[939]             ; = 1536
  4485: MUL                           
  4486: ADD                           
  4487: DCP      4                    
  4488: GCP      data[940]             ; = 6
  4489: LCP      [sp-3]               
  4490: GCP      data[941]             ; = 33554432
  4491: FDIV                          
  4492: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4493: SSP      3                    
  4494: LCP      [sp+1]               
  4495: LCP      [sp+1]               
  4496: GCP      data[942]             ; = 131072
  4497: ADD                           
  4498: LADR     [sp+1]               
  4499: ASGN                          
  4500: SSP      1                    
  4501: SSP      1                    
  4502: JMP      label_4406           
label_4503:
  4503: RET      36                   
  4504: ASP      4                    
  4505: LCP      [sp-4]               
  4506: LADR     [sp+0]               
  4507: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  4508: SSP      2                    
  4509: LADR     [sp+0]               
  4510: PNT      8                    
  4511: DCP      4                    
  4512: GCP      data[943]             ; = 512
  4513: FADD                          
  4514: LADR     [sp+0]               
  4515: PNT      8                    
  4516: ASGN                          
  4517: SSP      1                    
  4518: GCP      data[944]             ; = 2
  4519: LADR     [sp+0]               
  4520: PNT      12                   
  4521: ASGN                          
  4522: SSP      1                    
  4523: ASP      1                    
  4524: LADR     [sp+0]               
  4525: ASP      1                    
  4526: XCALL    $SC_SphereIsVisible(*s_sphere)int ; args=1
  4527: LLD      [sp+4]               
  4528: SSP      1                    
  4529: LLD      [sp-3]               
  4530: RET      4                    
  4531: ASP      5                    
  4532: LCP      [sp-4]               
  4533: LADR     [sp+0]               
  4534: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4535: SSP      2                    
  4536: LADR     [sp+0]               
  4537: PNT      8                    
  4538: DCP      4                    
  4539: LLD      [sp-3]               
  4540: RET      5                    
  4541: ASP      5                    
  4542: LCP      [sp-4]               
  4543: LADR     [sp+0]               
  4544: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4545: SSP      2                    
  4546: LADR     [sp+0]               
  4547: PNT      12                   
  4548: DCP      4                    
  4549: LLD      [sp-3]               
  4550: RET      5                    
  4551: ASP      5                    
  4552: LCP      [sp-4]               
  4553: LADR     [sp+0]               
  4554: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4555: SSP      2                    
  4556: LADR     [sp+0]               
  4557: PNT      16                   
  4558: DCP      4                    
  4559: LLD      [sp-3]               
  4560: RET      5                    
  4561: GADR     data[945]            
  4562: LCP      [sp-4]               
  4563: GCP      data[955]             ; = 1792
  4564: ADD                           
  4565: ASGN                          
  4566: SSP      1                    
  4567: GADR     data[956]            
  4568: LCP      [sp-4]               
  4569: GCP      data[971]             ; = 6656
  4570: ADD                           
  4571: PNT      4                    
  4572: ASGN                          
  4573: SSP      1                    
  4574: GADR     data[972]            
  4575: LCP      [sp-4]               
  4576: GCP      data[982]             ; = 524288
  4577: ADD                           
  4578: ASGN                          
  4579: SSP      1                    
  4580: GADR     data[983]            
  4581: LCP      [sp-4]               
  4582: GCP      data[999]             ; = 512
  4583: ADD                           
  4584: PNT      4                    
  4585: ASGN                          
  4586: SSP      1                    
  4587: GADR     data[1000]           
  4588: LCP      [sp-4]               
  4589: GCP      data[1010]            ; = 1507328
  4590: ADD                           
  4591: ASGN                          
  4592: SSP      1                    
  4593: GADR     data[1011]           
  4594: LCP      [sp-4]               
  4595: GCP      data[1026]            ; = 589824
  4596: ADD                           
  4597: PNT      4                    
  4598: ASGN                          
  4599: SSP      1                    
  4600: GADR     data[1027]           
  4601: LCP      [sp-4]               
  4602: GCP      data[1038]            ; = 983040
  4603: ADD                           
  4604: ASGN                          
  4605: SSP      1                    
  4606: GADR     data[1039]           
  4607: LCP      [sp-4]               
  4608: GCP      data[1055]            ; = 2048
  4609: ADD                           
  4610: PNT      4                    
  4611: ASGN                          
  4612: SSP      1                    
  4613: GADR     data[1056]           
  4614: LCP      [sp-4]               
  4615: GCP      data[1067]            ; = 1536
  4616: ADD                           
  4617: ASGN                          
  4618: SSP      1                    
  4619: GADR     data[1068]           
  4620: LCP      [sp-4]               
  4621: GCP      data[1084]  ; "\r"    ; ""
  4622: ADD                           
  4623: PNT      4                    
  4624: ASGN                          
  4625: SSP      1                    
  4626: GADR     data[1085]           
  4627: LCP      [sp-4]               
  4628: GCP      data[1096]            ; = 18
  4629: ADD                           
  4630: ASGN                          
  4631: SSP      1                    
  4632: GADR     data[1097]           
  4633: LCP      [sp-4]               
  4634: GCP      data[1114]            ; = 524288
  4635: ADD                           
  4636: PNT      4                    
  4637: ASGN                          
  4638: SSP      1                    
  4639: GADR     data[1115]           
  4640: LCP      [sp-4]               
  4641: GCP      data[1125]            ; = 100663296
  4642: ADD                           
  4643: ASGN                          
  4644: SSP      1                    
  4645: GADR     data[1126]           
  4646: LCP      [sp-4]               
  4647: GCP      data[1141]            ; = 318767104
  4648: ADD                           
  4649: PNT      4                    
  4650: ASGN                          
  4651: SSP      1                    
  4652: GADR     data[1142]           
  4653: LCP      [sp-4]               
  4654: GCP      data[1153]            ; = 369098752
  4655: ADD                           
  4656: ASGN                          
  4657: SSP      1                    
  4658: GADR     data[1154]           
  4659: LCP      [sp-4]               
  4660: GCP      data[1170]            ; = 983040
  4661: ADD                           
  4662: PNT      4                    
  4663: ASGN                          
  4664: SSP      1                    
  4665: GCP      data[1171]            ; = 3840
  4666: LCP      [sp-3]               
  4667: ASGN                          
  4668: SSP      1                    
  4669: RET      0                    
func_4670:
  4670: GADR     data[1172]           
  4671: LCP      [sp-4]               
  4672: GCP      data[1182]            ; = 1179648
  4673: ADD                           
  4674: ASGN                          
  4675: SSP      1                    
  4676: GADR     data[1183]           
  4677: LCP      [sp-4]               
  4678: GCP      data[1199]            ; = 2816
  4679: ADD                           
  4680: PNT      4                    
  4681: ASGN                          
  4682: SSP      1                    
  4683: GADR     data[1200]           
  4684: LCP      [sp-4]               
  4685: GCP      data[1211]            ; = 1536
  4686: ADD                           
  4687: ASGN                          
  4688: SSP      1                    
  4689: GADR     data[1212]           
  4690: LCP      [sp-4]               
  4691: GCP      data[1229]            ; = 352321536
  4692: ADD                           
  4693: PNT      4                    
  4694: ASGN                          
  4695: SSP      1                    
  4696: GCP      data[1230]            ; = 1376256
  4697: LCP      [sp-3]               
  4698: ASGN                          
  4699: SSP      1                    
  4700: RET      0                    
  4701: GADR     data[1231]           
  4702: LCP      [sp-4]               
  4703: GCP      data[1241]            ; = 469762048
  4704: ADD                           
  4705: ASGN                          
  4706: SSP      1                    
  4707: GADR     data[1242]           
  4708: LCP      [sp-4]               
  4709: GCP      data[1258]            ; = 983040
  4710: ADD                           
  4711: PNT      4                    
  4712: ASGN                          
  4713: SSP      1                    
  4714: GADR     data[1259]           
  4715: LCP      [sp-4]               
  4716: GCP      data[1269]            ; = 50331648
  4717: ADD                           
  4718: ASGN                          
  4719: SSP      1                    
  4720: GADR     data[1270]           
  4721: LCP      [sp-4]               
  4722: GCP      data[1286]            ; = 917504
  4723: ADD                           
  4724: PNT      4                    
  4725: ASGN                          
  4726: SSP      1                    
  4727: GADR     data[1287]           
  4728: LCP      [sp-4]               
  4729: GCP      data[1297]            ; = 251658240
  4730: ADD                           
  4731: ASGN                          
  4732: SSP      1                    
  4733: GADR     data[1298]           
  4734: LCP      [sp-4]               
  4735: GCP      data[1315]            ; = 5888
  4736: ADD                           
  4737: PNT      4                    
  4738: ASGN                          
  4739: SSP      1                    
  4740: GADR     data[1316]           
  4741: LCP      [sp-4]               
  4742: GCP      data[1327]            ; = 512
  4743: ADD                           
  4744: ASGN                          
  4745: SSP      1                    
  4746: GADR     data[1328]           
  4747: LCP      [sp-4]               
  4748: GCP      data[1345]            ; = 536870912
  4749: ADD                           
  4750: PNT      4                    
  4751: ASGN                          
  4752: SSP      1                    
  4753: GADR     data[1346]           
  4754: LCP      [sp-4]               
  4755: GCP      data[1357]            ; = 184549376
  4756: ADD                           
  4757: ASGN                          
  4758: SSP      1                    
  4759: GADR     data[1358]           
  4760: LCP      [sp-4]               
  4761: GCP      data[1375]            ; = 1024
  4762: ADD                           
  4763: PNT      4                    
  4764: ASGN                          
  4765: SSP      1                    
  4766: GADR     data[1376]           
  4767: LCP      [sp-4]               
  4768: GCP      data[1387]            ; = 1536
  4769: ADD                           
  4770: ASGN                          
  4771: SSP      1                    
  4772: GADR     data[1388]           
  4773: LCP      [sp-4]               
  4774: GCP      data[1405]            ; = 16777216
  4775: ADD                           
  4776: PNT      4                    
  4777: ASGN                          
  4778: SSP      1                    
  4779: GADR     data[1406]           
  4780: LCP      [sp-4]               
  4781: GCP      data[1417]            ; = 100663296
  4782: ADD                           
  4783: ASGN                          
  4784: SSP      1                    
  4785: GADR     data[1418]           
  4786: LCP      [sp-4]               
  4787: GCP      data[1435]            ; = 1936876921
  4788: ADD                           
  4789: PNT      4                    
  4790: ASGN                          
  4791: SSP      1                    
  4792: GADR     data[1436]           
  4793: LCP      [sp-4]               
  4794: GCP      data[1446]            ; = 1768843566
  4795: ADD                           
  4796: ASGN                          
  4797: SSP      1                    
  4798: GADR     data[1447]           
  4799: LCP      [sp-4]               
  4800: GCP      data[1463]            ; = 1936876921
  4801: ADD                           
  4802: PNT      4                    
  4803: ASGN                          
  4804: SSP      1                    
  4805: GCP      data[1464]            ; = 1551069797
  4806: LCP      [sp-3]               
  4807: ASGN                          
  4808: SSP      1                    
  4809: RET      0                    
  4810: GADR     data[1465]           
  4811: LCP      [sp-4]               
  4812: GCP      data[1475]            ; = 1768843566
  4813: ADD                           
  4814: ASGN                          
  4815: SSP      1                    
  4816: GADR     data[1476]           
  4817: LCP      [sp-4]               
  4818: GCP      data[1493]            ; = 1987211119
  4819: ADD                           
  4820: PNT      4                    
  4821: ASGN                          
  4822: SSP      1                    
  4823: GADR     data[1494]           
  4824: LCP      [sp-4]               
  4825: GCP      data[1505]            ; = 50331648
  4826: ADD                           
  4827: ASGN                          
  4828: SSP      1                    
  4829: GADR     data[1506]           
  4830: LCP      [sp-4]               
  4831: GCP      data[1524]            ; = 8
  4832: ADD                           
  4833: PNT      4                    
  4834: ASGN                          
  4835: SSP      1                    
  4836: GADR     data[1525]           
  4837: LCP      [sp-4]               
  4838: GCP      data[1535]            ; = 1768843520
  4839: ADD                           
  4840: ASGN                          
  4841: SSP      1                    
  4842: GADR     data[1536]  ; "ini\players\vcfighter2.ini"
  4843: LCP      [sp-4]               
  4844: GCP      data[1553]            ; = 1919251560
  4845: ADD                           
  4846: PNT      4                    
  4847: ASGN                          
  4848: SSP      1                    
  4849: GCP      data[1554]            ; = 846357876
  4850: LCP      [sp-3]               
  4851: ASGN                          
  4852: SSP      1                    
  4853: RET      0                    
  4854: GADR     data[1555]           
  4855: LCP      [sp-4]               
  4856: GCP      data[1565]            ; = 1761607680
  4857: ADD                           
  4858: ASGN                          
  4859: SSP      1                    
  4860: GADR     data[1566]           
  4861: LCP      [sp-4]               
  4862: GCP      data[1582]            ; = 1751607654
  4863: ADD                           
  4864: PNT      4                    
  4865: ASGN                          
  4866: SSP      1                    
  4867: GADR     data[1583]           
  4868: LCP      [sp-4]               
  4869: GCP      data[1594]            ; = 1852375040
  4870: ADD                           
  4871: ASGN                          
  4872: SSP      1                    
  4873: GADR     data[1595]           
  4874: LCP      [sp-4]               
  4875: GCP      data[1612]            ; = 1702127719
  4876: ADD                           
  4877: PNT      4                    
  4878: ASGN                          
  4879: SSP      1                    
  4880: GADR     data[1613]           
  4881: LCP      [sp-4]               
  4882: GCP      data[1623]            ; = 2304
  4883: ADD                           
  4884: ASGN                          
  4885: SSP      1                    
  4886: GADR     data[1624]  ; "	"    
  4887: LCP      [sp-4]               
  4888: GCP      data[1640]            ; = 14
  4889: ADD                           
  4890: PNT      4                    
  4891: ASGN                          
  4892: SSP      1                    
  4893: GADR     data[1641]           
  4894: LCP      [sp-4]               
  4895: GCP      data[1651]            ; = 3840
  4896: ADD                           
  4897: ASGN                          
  4898: SSP      1                    
  4899: GADR     data[1652]           
  4900: LCP      [sp-4]               
  4901: GCP      data[1669]            ; = 1734960739
  4902: ADD                           
  4903: PNT      4                    
  4904: ASGN                          
  4905: SSP      1                    
  4906: GADR     data[1670]           
  4907: LCP      [sp-4]               
  4908: GCP      data[1680]            ; = 26990
  4909: ADD                           
  4910: ASGN                          
  4911: SSP      1                    
  4912: GADR     data[1681]           
  4913: LCP      [sp-4]               
  4914: GCP      data[1697]            ; = 1985770354
  4915: ADD                           
  4916: PNT      4                    
  4917: ASGN                          
  4918: SSP      1                    
  4919: GADR     data[1698]           
  4920: LCP      [sp-4]               
  4921: GCP      data[1709]            ; = 1852386866
  4922: ADD                           
  4923: ASGN                          
  4924: SSP      1                    
  4925: GADR     data[1710]           
  4926: LCP      [sp-4]               
  4927: GCP      data[1727]            ; = 1936876921
  4928: ADD                           
  4929: PNT      4                    
  4930: ASGN                          
  4931: SSP      1                    
  4932: GADR     data[1728]           
  4933: LCP      [sp-4]               
  4934: GCP      data[1738]            ; = 863135092
  4935: ADD                           
  4936: ASGN                          
  4937: SSP      1                    
  4938: GADR     data[1739]           
  4939: LCP      [sp-4]               
  4940: GCP      data[1755]            ; = 1936876921
  4941: ADD                           
  4942: PNT      4                    
  4943: ASGN                          
  4944: SSP      1                    
  4945: GADR     data[1756]           
  4946: LCP      [sp-4]               
  4947: GCP      data[1767]            ; = 775189093
  4948: ADD                           
  4949: ASGN                          
  4950: SSP      1                    
  4951: GADR     data[1768]           
  4952: LCP      [sp-4]               
  4953: GCP      data[1785]            ; = 352321536
  4954: ADD                           
  4955: PNT      4                    
  4956: ASGN                          
  4957: SSP      1                    
  4958: GCP      data[1786]            ; = 1376256
  4959: LCP      [sp-3]               
  4960: ASGN                          
  4961: SSP      1                    
  4962: RET      0                    
  4963: GADR     data[1787]           
  4964: LCP      [sp-4]               
  4965: GCP      data[1797]            ; = 469762048
  4966: ADD                           
  4967: ASGN                          
  4968: SSP      1                    
  4969: GADR     data[1798]           
  4970: LCP      [sp-4]               
  4971: GCP      data[1815]            ; = 1936876921
  4972: ADD                           
  4973: PNT      4                    
  4974: ASGN                          
  4975: SSP      1                    
  4976: GADR     data[1816]           
  4977: LCP      [sp-4]               
  4978: GCP      data[1826]            ; = 829256303
  4979: ADD                           
  4980: ASGN                          
  4981: SSP      1                    
  4982: GADR     data[1827]           
  4983: LCP      [sp-4]               
  4984: GCP      data[1844]            ; = 2036427888
  4985: ADD                           
  4986: PNT      4                    
  4987: ASGN                          
  4988: SSP      1                    
  4989: GADR     data[1845]           
  4990: LCP      [sp-4]               
  4991: GCP      data[1855]            ; = 1868982638
  4992: ADD                           
  4993: ASGN                          
  4994: SSP      1                    
  4995: GADR     data[1856]           
  4996: LCP      [sp-4]               
  4997: GCP      data[1873]            ; = 1702453612
  4998: ADD                           
  4999: PNT      4                    
  5000: ASGN                          
  5001: SSP      1                    
  5002: GADR     data[1874]           
  5003: LCP      [sp-4]               
  5004: GCP      data[1885]            ; = 1836216166
  5005: ADD                           
  5006: ASGN                          
  5007: SSP      1                    
  5008: GADR     data[1886]           
  5009: LCP      [sp-4]               
  5010: GCP      data[1904]            ; = 25
  5011: ADD                           
  5012: PNT      4                    
  5013: ASGN                          
  5014: SSP      1                    
  5015: GADR     data[1905]           
  5016: LCP      [sp-4]               
  5017: GCP      data[1915]            ; = 7936
  5018: ADD                           
  5019: ASGN                          
  5020: SSP      1                    
  5021: GADR     data[1916]           
  5022: LCP      [sp-4]               
  5023: GCP      data[1933]            ; = 1702453612
  5024: ADD                           
  5025: PNT      4                    
  5026: ASGN                          
  5027: SSP      1                    
  5028: GCP      data[1934]            ; = 1919252833
  5029: LCP      [sp-3]               
  5030: ASGN                          
  5031: SSP      1                    
  5032: RET      0                    
  5033: GADR     data[1935]           
  5034: LCP      [sp-4]               
  5035: GCP      data[1945]            ; = 1701405804
  5036: ADD                           
  5037: ASGN                          
  5038: SSP      1                    
  5039: GADR     data[1946]           
  5040: LCP      [sp-4]               
  5041: GCP      data[1962]            ; = 1819303017
  5042: ADD                           
  5043: PNT      4                    
  5044: ASGN                          
  5045: SSP      1                    
  5046: GADR     data[1963]           
  5047: LCP      [sp-4]               
  5048: GCP      data[1973]            ; = 1869832566
  5049: ADD                           
  5050: ASGN                          
  5051: SSP      1                    
  5052: GADR     data[1974]           
  5053: LCP      [sp-4]               
  5054: GCP      data[1990]            ; = 1819303017
  5055: ADD                           
  5056: PNT      4                    
  5057: ASGN                          
  5058: SSP      1                    
  5059: GADR     data[1991]           
  5060: LCP      [sp-4]               
  5061: GCP      data[2002]            ; = 1717989217
  5062: ADD                           
  5063: ASGN                          
  5064: SSP      1                    
  5065: GADR     data[2003]           
  5066: LCP      [sp-4]               
  5067: GCP      data[2020]            ; = 2036427888
  5068: ADD                           
  5069: PNT      4                    
  5070: ASGN                          
  5071: SSP      1                    
  5072: GADR     data[2021]           
  5073: LCP      [sp-4]               
  5074: GCP      data[2032]            ; = 1601465461
  5075: ADD                           
  5076: ASGN                          
  5077: SSP      1                    
  5078: GADR     data[2033]           
  5079: LCP      [sp-4]               
  5080: GCP      data[2049]            ; = 134217728
  5081: ADD                           
  5082: PNT      4                    
  5083: ASGN                          
  5084: SSP      1                    
  5085: GADR     data[2050]           
  5086: LCP      [sp-4]               
  5087: GCP      data[2061]            ; = 0
  5088: ADD                           
  5089: ASGN                          
  5090: SSP      1                    
  5091: GADR     data[2062]           
  5092: LCP      [sp-4]               
  5093: GCP      data[2079]            ; = 256
  5094: ADD                           
  5095: PNT      4                    
  5096: ASGN                          
  5097: SSP      1                    
  5098: GADR     data[2080]           
  5099: LCP      [sp-4]               
  5100: GCP      data[2091]            ; = 9728
  5101: ADD                           
  5102: ASGN                          
  5103: SSP      1                    
  5104: GADR     data[2092]  ; "&"    
  5105: LCP      [sp-4]               
  5106: GCP      data[2109]            ; = 83886080
  5107: ADD                           
  5108: PNT      4                    
  5109: ASGN                          
  5110: SSP      1                    
  5111: GCP      data[2110]            ; = 327680
  5112: LCP      [sp-3]               
  5113: ASGN                          
  5114: SSP      1                    
  5115: RET      0                    
  5116: GADR     data[2111]           
  5117: LCP      [sp-4]               
  5118: GCP      data[2121]            ; = 419430400
  5119: ADD                           
  5120: ASGN                          
  5121: SSP      1                    
  5122: GADR     data[2122]           
  5123: LCP      [sp-4]               
  5124: GCP      data[2139]            ; = 5888
  5125: ADD                           
  5126: PNT      4                    
  5127: ASGN                          
  5128: SSP      1                    
  5129: GADR     data[2140]           
  5130: LCP      [sp-4]               
  5131: GCP      data[2151]            ; = 1024
  5132: ADD                           
  5133: ASGN                          
  5134: SSP      1                    
  5135: GADR     data[2152]           
  5136: LCP      [sp-4]               
  5137: GCP      data[2169]            ; = 0
  5138: ADD                           
  5139: PNT      4                    
  5140: ASGN                          
  5141: SSP      1                    
  5142: GADR     data[2170]           
  5143: LCP      [sp-4]               
  5144: GCP      data[2180]            ; = 4
  5145: ADD                           
  5146: ASGN                          
  5147: SSP      1                    
  5148: GADR     data[2181]           
  5149: LCP      [sp-4]               
  5150: GCP      data[2197]            ; = 385875968
  5151: ADD                           
  5152: PNT      4                    
  5153: ASGN                          
  5154: SSP      1                    
  5155: GCP      data[2198]            ; = 1507328
  5156: LCP      [sp-3]               
  5157: ASGN                          
  5158: SSP      1                    
  5159: RET      0                    
  5160: GADR     data[2199]           
  5161: LCP      [sp-4]               
  5162: GCP      data[2210]            ; = 262144
  5163: ADD                           
  5164: ASGN                          
  5165: SSP      1                    
  5166: GADR     data[2211]           
  5167: LCP      [sp-4]               
  5168: GCP      data[2228]            ; = 11
  5169: ADD                           
  5170: PNT      4                    
  5171: ASGN                          
  5172: SSP      1                    
  5173: GADR     data[2229]           
  5174: LCP      [sp-4]               
  5175: GCP      data[2239]            ; = 0
  5176: ADD                           
  5177: ASGN                          
  5178: SSP      1                    
  5179: GADR     data[2240]           
  5180: LCP      [sp-4]               
  5181: GCP      data[2256]            ; = 23
  5182: ADD                           
  5183: PNT      4                    
  5184: ASGN                          
  5185: SSP      1                    
  5186: GADR     data[2257]           
  5187: LCP      [sp-4]               
  5188: GCP      data[2267]            ; = 1024
  5189: ADD                           
  5190: ASGN                          
  5191: SSP      1                    
  5192: GADR     data[2268]           
  5193: LCP      [sp-4]               
  5194: GCP      data[2284]            ; = 12
  5195: ADD                           
  5196: PNT      4                    
  5197: ASGN                          
  5198: SSP      1                    
  5199: GADR     data[2285]           
  5200: LCP      [sp-4]               
  5201: GCP      data[2295]            ; = 3328
  5202: ADD                           
  5203: ASGN                          
  5204: SSP      1                    
  5205: GADR     data[2296]  ; "\r"   
  5206: LCP      [sp-4]               
  5207: GCP      data[2313]            ; = 419430400
  5208: ADD                           
  5209: PNT      4                    
  5210: ASGN                          
  5211: SSP      1                    
  5212: GADR     data[2314]           
  5213: LCP      [sp-4]               
  5214: GCP      data[2325]            ; = 318767104
  5215: ADD                           
  5216: ASGN                          
  5217: SSP      1                    
  5218: GADR     data[2326]           
  5219: LCP      [sp-4]               
  5220: GCP      data[2343]            ; = 7168
  5221: ADD                           
  5222: PNT      4                    
  5223: ASGN                          
  5224: SSP      1                    
  5225: GADR     data[2344]           
  5226: LCP      [sp-4]               
  5227: GCP      data[2355]            ; = 2048
  5228: ADD                           
  5229: ASGN                          
  5230: SSP      1                    
  5231: GADR     data[2356]           
  5232: LCP      [sp-4]               
  5233: GCP      data[2373]            ; = 67108864
  5234: ADD                           
  5235: PNT      4                    
  5236: ASGN                          
  5237: SSP      1                    
  5238: GADR     data[2374]           
  5239: LCP      [sp-4]               
  5240: GCP      data[2385]            ; = 587202560
  5241: ADD                           
  5242: ASGN                          
  5243: SSP      1                    
  5244: GADR     data[2386]           
  5245: LCP      [sp-4]               
  5246: GCP      data[2403]            ; = 8960
  5247: ADD                           
  5248: PNT      4                    
  5249: ASGN                          
  5250: SSP      1                    
  5251: GADR     data[2404]  ; "#"    
  5252: LCP      [sp-4]               
  5253: GCP      data[2415]            ; = 1024
  5254: ADD                           
  5255: ASGN                          
  5256: SSP      1                    
  5257: GADR     data[2416]           
  5258: LCP      [sp-4]               
  5259: GCP      data[2434]            ; = 2228224
  5260: ADD                           
  5261: PNT      4                    
  5262: ASGN                          
  5263: SSP      1                    
  5264: GCP      data[2435]            ; = 8704
  5265: LCP      [sp-3]               
  5266: ASGN                          
  5267: SSP      1                    
  5268: RET      0                    
  5269: GADR     data[2436]  ; """    
  5270: LCP      [sp-4]               
  5271: GCP      data[2446]            ; = 1507328
  5272: ADD                           
  5273: ASGN                          
  5274: SSP      1                    
  5275: GADR     data[2447]           
  5276: LCP      [sp-4]               
  5277: GCP      data[2464]            ; = 26
  5278: ADD                           
  5279: PNT      4                    
  5280: ASGN                          
  5281: SSP      1                    
  5282: GADR     data[2465]           
  5283: LCP      [sp-4]               
  5284: GCP      data[2476]            ; = 26
  5285: ADD                           
  5286: ASGN                          
  5287: SSP      1                    
  5288: GADR     data[2477]           
  5289: LCP      [sp-4]               
  5290: GCP      data[2495]            ; = 2048
  5291: ADD                           
  5292: PNT      4                    
  5293: ASGN                          
  5294: SSP      1                    
  5295: GCP      data[2496]            ; = 8
  5296: LCP      [sp-3]               
  5297: ASGN                          
  5298: SSP      1                    
  5299: RET      0                    
  5300: GADR     data[2497]           
  5301: LCP      [sp-4]               
  5302: GCP      data[2507]            ; = 6400
  5303: ADD                           
  5304: ASGN                          
  5305: SSP      1                    
  5306: GADR     data[2508]           
  5307: LCP      [sp-4]               
  5308: GCP      data[2523]            ; = 1024
  5309: ADD                           
  5310: PNT      4                    
  5311: ASGN                          
  5312: SSP      1                    
  5313: GADR     data[2524]           
  5314: LCP      [sp-4]               
  5315: GCP      data[2534]            ; = 1900544
  5316: ADD                           
  5317: ASGN                          
  5318: SSP      1                    
  5319: GADR     data[2535]           
  5320: LCP      [sp-4]               
  5321: GCP      data[2550]            ; = 262144
  5322: ADD                           
  5323: PNT      4                    
  5324: ASGN                          
  5325: SSP      1                    
  5326: GADR     data[2551]           
  5327: LCP      [sp-4]               
  5328: GCP      data[2561]            ; = 570425344
  5329: ADD                           
  5330: ASGN                          
  5331: SSP      1                    
  5332: GADR     data[2562]           
  5333: LCP      [sp-4]               
  5334: GCP      data[2577]            ; = 536870912
  5335: ADD                           
  5336: PNT      4                    
  5337: ASGN                          
  5338: SSP      1                    
  5339: GADR     data[2578]           
  5340: LCP      [sp-4]               
  5341: GCP      data[2589]            ; = 570425344
  5342: ADD                           
  5343: ASGN                          
  5344: SSP      1                    
  5345: GADR     data[2590]           
  5346: LCP      [sp-4]               
  5347: GCP      data[2606]            ; = 2359296
  5348: ADD                           
  5349: PNT      4                    
  5350: ASGN                          
  5351: SSP      1                    
  5352: GADR     data[2607]           
  5353: LCP      [sp-4]               
  5354: GCP      data[2618]            ; = 0
  5355: ADD                           
  5356: ASGN                          
  5357: SSP      1                    
  5358: GADR     data[2619]           
  5359: LCP      [sp-4]               
  5360: GCP      data[2635]            ; = 2048
  5361: ADD                           
  5362: PNT      4                    
  5363: ASGN                          
  5364: SSP      1                    
  5365: GADR     data[2636]           
  5366: LCP      [sp-4]               
  5367: GCP      data[2646]            ; = 2228224
  5368: ADD                           
  5369: ASGN                          
  5370: SSP      1                    
  5371: GADR     data[2647]           
  5372: LCP      [sp-4]               
  5373: GCP      data[2662]            ; = 737992
  5374: ADD                           
  5375: PNT      4                    
  5376: ASGN                          
  5377: SSP      1                    
  5378: GADR     data[2663]           
  5379: LCP      [sp-4]               
  5380: GCP      data[2674]            ; = 0
  5381: ADD                           
  5382: ASGN                          
  5383: SSP      1                    
  5384: GADR     data[2675]           
  5385: LCP      [sp-4]               
  5386: GCP      data[2691]            ; = 256
  5387: ADD                           
  5388: PNT      4                    
  5389: ASGN                          
  5390: SSP      1                    
  5391: GCP      data[2692]            ; = 1
  5392: LCP      [sp-3]               
  5393: ASGN                          
  5394: SSP      1                    
  5395: RET      0                    
  5396: GADR     data[2693]           
  5397: LCP      [sp-4]               
  5398: GCP      data[2703]            ; = 0
  5399: ADD                           
  5400: ASGN                          
  5401: SSP      1                    
  5402: GADR     data[2704]           
  5403: LCP      [sp-4]               
  5404: GCP      data[2720]            ; = 0
  5405: ADD                           
  5406: PNT      4                    
  5407: ASGN                          
  5408: SSP      1                    
  5409: GADR     data[2721]           
  5410: LCP      [sp-4]               
  5411: GCP      data[2732]            ; = 1
  5412: ADD                           
  5413: ASGN                          
  5414: SSP      1                    
  5415: GADR     data[2733]           
  5416: LCP      [sp-4]               
  5417: GCP      data[2750]            ; = 65536
  5418: ADD                           
  5419: PNT      4                    
  5420: ASGN                          
  5421: SSP      1                    
  5422: GADR     data[2751]           
  5423: LCP      [sp-4]               
  5424: GCP      data[2761]            ; = 0
  5425: ADD                           
  5426: ASGN                          
  5427: SSP      1                    
  5428: GADR     data[2762]           
  5429: LCP      [sp-4]               
  5430: GCP      data[2778]            ; = 65536
  5431: ADD                           
  5432: PNT      4                    
  5433: ASGN                          
  5434: SSP      1                    
  5435: GCP      data[2779]            ; = 256
  5436: LCP      [sp-3]               
  5437: ASGN                          
  5438: SSP      1                    
  5439: RET      0                    
  5440: GADR     data[2780]           
  5441: LCP      [sp-4]               
  5442: GCP      data[2790]            ; = 393216
  5443: ADD                           
  5444: ASGN                          
  5445: SSP      1                    
  5446: GADR     data[2791]           
  5447: LCP      [sp-4]               
  5448: GCP      data[2801]            ; = 0
  5449: ADD                           
  5450: PNT      4                    
  5451: ASGN                          
  5452: SSP      1                    
  5453: GADR     data[2802]           
  5454: LCP      [sp-4]               
  5455: GCP      data[2813]            ; = 16777216
  5456: ADD                           
  5457: ASGN                          
  5458: SSP      1                    
  5459: GADR     data[2814]           
  5460: LCP      [sp-4]               
  5461: GCP      data[2832]            ; = 0
  5462: ADD                           
  5463: PNT      4                    
  5464: ASGN                          
  5465: SSP      1                    
  5466: GADR     data[2833]           
  5467: LCP      [sp-4]               
  5468: GCP      data[2844]            ; = 0
  5469: ADD                           
  5470: ASGN                          
  5471: SSP      1                    
  5472: GADR     data[2845]           
  5473: LCP      [sp-4]               
  5474: GCP      data[2864]            ; = 0
  5475: ADD                           
  5476: PNT      4                    
  5477: ASGN                          
  5478: SSP      1                    
  5479: GADR     data[2865]           
  5480: LCP      [sp-4]               
  5481: GCP      data[2875]            ; = 0
  5482: ADD                           
  5483: ASGN                          
  5484: SSP      1                    
  5485: GADR     data[2876]           
  5486: LCP      [sp-4]               
  5487: GCP      data[2894]            ; = 65536
  5488: ADD                           
  5489: PNT      4                    
  5490: ASGN                          
  5491: SSP      1                    
  5492: GADR     data[2895]           
  5493: LCP      [sp-4]               
  5494: GCP      data[2906]            ; = 0
  5495: ADD                           
  5496: ASGN                          
  5497: SSP      1                    
  5498: GADR     data[2907]           
  5499: LCP      [sp-4]               
  5500: GCP      data[2925]            ; = 1816338465
  5501: ADD                           
  5502: PNT      4                    
  5503: ASGN                          
  5504: SSP      1                    
  5505: GADR     data[2926]           
  5506: LCP      [sp-4]               
  5507: GCP      data[2937]            ; = 1869488243
  5508: ADD                           
  5509: ASGN                          
  5510: SSP      1                    
  5511: GADR     data[2938]           
  5512: LCP      [sp-4]               
  5513: GCP      data[2956]            ; = 1
  5514: ADD                           
  5515: PNT      4                    
  5516: ASGN                          
  5517: SSP      1                    
  5518: GCP      data[2957]            ; = 3271557120
  5519: LCP      [sp-3]               
  5520: ASGN                          
  5521: SSP      1                    
  5522: RET      0                    
  5523: GADR     data[2958]           
  5524: LCP      [sp-4]               
  5525: GCP      data[2968]            ; = 1073741824
  5526: ADD                           
  5527: ASGN                          
  5528: SSP      1                    
  5529: GADR     data[2969]           
  5530: LCP      [sp-4]               
  5531: GCP      data[2986]            ; = 0
  5532: ADD                           
  5533: PNT      4                    
  5534: ASGN                          
  5535: SSP      1                    
  5536: GADR     data[2987]           
  5537: LCP      [sp-4]               
  5538: GCP      data[2997]            ; = 16777216
  5539: ADD                           
  5540: ASGN                          
  5541: SSP      1                    
  5542: GADR     data[2998]           
  5543: LCP      [sp-4]               
  5544: GCP      data[3015]            ; = 768
  5545: ADD                           
  5546: PNT      4                    
  5547: ASGN                          
  5548: SSP      1                    
  5549: GADR     data[3016]           
  5550: LCP      [sp-4]               
  5551: GCP      data[3026]            ; = 0
  5552: ADD                           
  5553: ASGN                          
  5554: SSP      1                    
  5555: GADR     data[3027]           
  5556: LCP      [sp-4]               
  5557: GCP      data[3045]            ; = 2973728768
  5558: ADD                           
  5559: PNT      4                    
  5560: ASGN                          
  5561: SSP      1                    
  5562: GADR     data[3046]           
  5563: LCP      [sp-4]               
  5564: GCP      data[3057]            ; = 4487680
  5565: ADD                           
  5566: ASGN                          
  5567: SSP      1                    
  5568: GADR     data[3058]  ; "zD"   
  5569: LCP      [sp-4]               
  5570: GCP      data[3076]            ; = 6
  5571: ADD                           
  5572: PNT      4                    
  5573: ASGN                          
  5574: SSP      1                    
  5575: GADR     data[3077]           
  5576: LCP      [sp-4]               
  5577: GCP      data[3088]            ; = 177
  5578: ADD                           
  5579: ASGN                          
  5580: SSP      1                    
  5581: GADR     data[3089]           
  5582: LCP      [sp-4]               
  5583: GCP      data[3107]            ; = 319
  5584: ADD                           
  5585: PNT      4                    
  5586: ASGN                          
  5587: SSP      1                    
  5588: GADR     data[3108]           
  5589: LCP      [sp-4]               
  5590: GCP      data[3119]            ; = 45056
  5591: ADD                           
  5592: ASGN                          
  5593: SSP      1                    
  5594: GADR     data[3120]  ; "°"    
  5595: LCP      [sp-4]               
  5596: GCP      data[3138]            ; = 11616128
  5597: ADD                           
  5598: PNT      4                    
  5599: ASGN                          
  5600: SSP      1                    
  5601: GADR     data[3139]           
  5602: LCP      [sp-4]               
  5603: GCP      data[3150]            ; = 0
  5604: ADD                           
  5605: ASGN                          
  5606: SSP      1                    
  5607: GADR     data[3151]           
  5608: LCP      [sp-4]               
  5609: GCP      data[3169]            ; = 0
  5610: ADD                           
  5611: PNT      4                    
  5612: ASGN                          
  5613: SSP      1                    
  5614: GADR     data[3170]           
  5615: LCP      [sp-4]               
  5616: GCP      data[3180]            ; = 1065353216
  5617: ADD                           
  5618: ASGN                          
  5619: SSP      1                    
  5620: GADR     data[3181]           
  5621: LCP      [sp-4]               
  5622: GCP      data[3198]  ; "zD"    ; "zD"
  5623: ADD                           
  5624: PNT      4                    
  5625: ASGN                          
  5626: SSP      1                    
  5627: GCP      data[3199]            ; = 68
  5628: LCP      [sp-3]               
  5629: ASGN                          
  5630: SSP      1                    
  5631: RET      0                    
  5632: GADR     data[3200]           
  5633: LCP      [sp-4]               
  5634: GCP      data[3210]            ; = 16256
  5635: ADD                           
  5636: ASGN                          
  5637: SSP      1                    
  5638: GADR     data[3211]           
  5639: LCP      [sp-4]               
  5640: GCP      data[3228]            ; = 1148846080
  5641: ADD                           
  5642: PNT      4                    
  5643: ASGN                          
  5644: SSP      1                    
  5645: GADR     data[3229]           
  5646: LCP      [sp-4]               
  5647: GCP      data[3239]            ; = 2147483711
  5648: ADD                           
  5649: ASGN                          
  5650: SSP      1                    
  5651: GADR     data[3240]           
  5652: LCP      [sp-4]               
  5653: GCP      data[3257]            ; = 16777216
  5654: ADD                           
  5655: PNT      4                    
  5656: ASGN                          
  5657: SSP      1                    
  5658: GADR     data[3258]           
  5659: LCP      [sp-4]               
  5660: GCP      data[3268]            ; = 1063675494
  5661: ADD                           
  5662: ASGN                          
  5663: SSP      1                    
  5664: GADR     data[3269]           
  5665: LCP      [sp-4]               
  5666: GCP      data[3286]            ; = 0
  5667: ADD                           
  5668: PNT      4                    
  5669: ASGN                          
  5670: SSP      1                    
  5671: GADR     data[3287]           
  5672: LCP      [sp-4]               
  5673: GCP      data[3297]            ; = 100663296
  5674: ADD                           
  5675: ASGN                          
  5676: SSP      1                    
  5677: GADR     data[3298]           
  5678: LCP      [sp-4]               
  5679: GCP      data[3316]            ; = 0
  5680: ADD                           
  5681: PNT      4                    
  5682: ASGN                          
  5683: SSP      1                    
  5684: GADR     data[3317]           
  5685: LCP      [sp-4]               
  5686: GCP      data[3328]            ; = 1176256512
  5687: ADD                           
  5688: ASGN                          
  5689: SSP      1                    
  5690: GADR     data[3329]           
  5691: LCP      [sp-4]               
  5692: GCP      data[3347]            ; = 1024
  5693: ADD                           
  5694: PNT      4                    
  5695: ASGN                          
  5696: SSP      1                    
  5697: GADR     data[3348]           
  5698: LCP      [sp-4]               
  5699: GCP      data[3359]            ; = 1024
  5700: ADD                           
  5701: ASGN                          
  5702: SSP      1                    
  5703: GADR     data[3360]           
  5704: LCP      [sp-4]               
  5705: GCP      data[3378]            ; = 0
  5706: ADD                           
  5707: PNT      4                    
  5708: ASGN                          
  5709: SSP      1                    
  5710: GADR     data[3379]           
  5711: LCP      [sp-4]               
  5712: GCP      data[3390]            ; = 65536
  5713: ADD                           
  5714: ASGN                          
  5715: SSP      1                    
  5716: GADR     data[3391]           
  5717: LCP      [sp-4]               
  5718: GCP      data[3409]            ; = 50331648
  5719: ADD                           
  5720: PNT      4                    
  5721: ASGN                          
  5722: SSP      1                    
  5723: GADR     data[3410]           
  5724: LCP      [sp-4]               
  5725: GCP      data[3421]            ; = 1970238023
  5726: ADD                           
  5727: ASGN                          
  5728: SSP      1                    
  5729: GADR     data[3422]           
  5730: LCP      [sp-4]               
  5731: GCP      data[3441]            ; = 544436837
  5732: ADD                           
  5733: PNT      4                    
  5734: ASGN                          
  5735: SSP      1                    
  5736: GCP      data[3442]            ; = 1763734386
  5737: LCP      [sp-3]               
  5738: ASGN                          
  5739: SSP      1                    
  5740: RET      0                    
  5741: GADR     data[3443]           
  5742: LCP      [sp-4]               
  5743: GCP      data[3453]            ; = 1869766944
  5744: ADD                           
  5745: ASGN                          
  5746: SSP      1                    
  5747: GADR     data[3454]           
  5748: LCP      [sp-4]               
  5749: GCP      data[3472]  ; " "     ; " "
  5750: ADD                           
  5751: PNT      4                    
  5752: ASGN                          
  5753: SSP      1                    
  5754: GADR     data[3473]           
  5755: LCP      [sp-4]               
  5756: GCP      data[3484]            ; "VC %d %d couldnot find anyone "
  5757: ADD                           
  5758: ASGN                          
  5759: SSP      1                    
  5760: GADR     data[3485]           
  5761: LCP      [sp-4]               
  5762: GCP      data[3503]            ; = 543452777
  5763: ADD                           
  5764: PNT      4                    
  5765: ASGN                          
  5766: SSP      1                    
  5767: GADR     data[3504]           
  5768: LCP      [sp-4]               
  5769: GCP      data[3514]            ; = 1814065012
  5770: ADD                           
  5771: ASGN                          
  5772: SSP      1                    
  5773: GADR     data[3515]           
  5774: LCP      [sp-4]               
  5775: GCP      data[3533]            ; = 0
  5776: ADD                           
  5777: PNT      4                    
  5778: ASGN                          
  5779: SSP      1                    
  5780: GCP      data[3534]            ; = 0
  5781: LCP      [sp-3]               
  5782: ASGN                          
  5783: SSP      1                    
  5784: RET      0                    
  5785: GADR     data[3535]           
  5786: LCP      [sp-4]               
  5787: GCP      data[3545]            ; = 0
  5788: ADD                           
  5789: ASGN                          
  5790: SSP      1                    
  5791: GADR     data[3546]           
  5792: LCP      [sp-4]               
  5793: GCP      data[3563]            ; = 768
  5794: ADD                           
  5795: PNT      4                    
  5796: ASGN                          
  5797: SSP      1                    
  5798: GADR     data[3564]           
  5799: LCP      [sp-4]               
  5800: GCP      data[3574]            ; = 1830839333
  5801: ADD                           
  5802: ASGN                          
  5803: SSP      1                    
  5804: GADR     data[3575]           
  5805: LCP      [sp-4]               
  5806: GCP      data[3592]            ; = 544367990
  5807: ADD                           
  5808: PNT      4                    
  5809: ASGN                          
  5810: SSP      1                    
  5811: GADR     data[3593]           
  5812: LCP      [sp-4]               
  5813: GCP      data[3604]            ; = 4
  5814: ADD                           
  5815: ASGN                          
  5816: SSP      1                    
  5817: GADR     data[3605]           
  5818: LCP      [sp-4]               
  5819: GCP      data[3623]            ; = 1024
  5820: ADD                           
  5821: PNT      4                    
  5822: ASGN                          
  5823: SSP      1                    
  5824: GADR     data[3624]           
  5825: LCP      [sp-4]               
  5826: GCP      data[3635]            ; = 0
  5827: ADD                           
  5828: ASGN                          
  5829: SSP      1                    
  5830: GADR     data[3636]           
  5831: LCP      [sp-4]               
  5832: GCP      data[3654]            ; = 0
  5833: ADD                           
  5834: PNT      4                    
  5835: ASGN                          
  5836: SSP      1                    
  5837: GADR     data[3655]           
  5838: LCP      [sp-4]               
  5839: GCP      data[3666]            ; = 786432
  5840: ADD                           
  5841: ASGN                          
  5842: SSP      1                    
  5843: GADR     data[3667]           
  5844: LCP      [sp-4]               
  5845: GCP      data[3685]            ; = 0
  5846: ADD                           
  5847: PNT      4                    
  5848: ASGN                          
  5849: SSP      1                    
  5850: GADR     data[3686]           
  5851: LCP      [sp-4]               
  5852: GCP      data[3697]            ; = 16777216
  5853: ADD                           
  5854: ASGN                          
  5855: SSP      1                    
  5856: GADR     data[3698]           
  5857: LCP      [sp-4]               
  5858: GCP      data[3716]            ; = 1088421888
  5859: ADD                           
  5860: PNT      4                    
  5861: ASGN                          
  5862: SSP      1                    
  5863: GADR     data[3717]           
  5864: LCP      [sp-4]               
  5865: GCP      data[3728]            ; = 1088421888
  5866: ADD                           
  5867: ASGN                          
  5868: SSP      1                    
  5869: GADR     data[3729]           
  5870: LCP      [sp-4]               
  5871: GCP      data[3747]            ; = 1280
  5872: ADD                           
  5873: PNT      4                    
  5874: ASGN                          
  5875: SSP      1                    
  5876: GADR     data[3748]           
  5877: LCP      [sp-4]               
  5878: GCP      data[3758]            ; = 393216
  5879: ADD                           
  5880: ASGN                          
  5881: SSP      1                    
  5882: GADR     data[3759]           
  5883: LCP      [sp-4]               
  5884: GCP      data[3776]            ; = 1065353216
  5885: ADD                           
  5886: PNT      4                    
  5887: ASGN                          
  5888: SSP      1                    
  5889: GCP      data[3777]            ; = 1195343872
  5890: LCP      [sp-3]               
  5891: ASGN                          
  5892: SSP      1                    
  5893: RET      0                    
  5894: GADR     data[3778]           
  5895: LCP      [sp-4]               
  5896: GCP      data[3789]            ; = 1432122478
  5897: ADD                           
  5898: ASGN                          
  5899: SSP      1                    
  5900: GADR     data[3790]           
  5901: LCP      [sp-4]               
  5902: GCP      data[3808]            ; = 812081506
  5903: ADD                           
  5904: PNT      4                    
  5905: ASGN                          
  5906: SSP      1                    
  5907: GADR     data[3809]           
  5908: LCP      [sp-4]               
  5909: GCP      data[3819]            ; = 0
  5910: ADD                           
  5911: ASGN                          
  5912: SSP      1                    
  5913: GADR     data[3820]           
  5914: LCP      [sp-4]               
  5915: GCP      data[3837]            ; = 1902468179
  5916: ADD                           
  5917: PNT      4                    
  5918: ASGN                          
  5919: SSP      1                    
  5920: GADR     data[3838]           
  5921: LCP      [sp-4]               
  5922: GCP      data[3848]            ; = 1936158305
  5923: ADD                           
  5924: ASGN                          
  5925: SSP      1                    
  5926: GADR     data[3849]           
  5927: LCP      [sp-4]               
  5928: GCP      data[3866]            ; = 1700745295
  5929: ADD                           
  5930: PNT      4                    
  5931: ASGN                          
  5932: SSP      1                    
  5933: GADR     data[3867]           
  5934: LCP      [sp-4]               
  5935: GCP      data[3878]            ; = 1902456369
  5936: ADD                           
  5937: ASGN                          
  5938: SSP      1                    
  5939: GADR     data[3879]           
  5940: LCP      [sp-4]               
  5941: GCP      data[3897]            ; = 1432122478
  5942: ADD                           
  5943: PNT      4                    
  5944: ASGN                          
  5945: SSP      1                    
  5946: GADR     data[3898]           
  5947: LCP      [sp-4]               
  5948: GCP      data[3909]            ; = 1600479056
  5949: ADD                           
  5950: ASGN                          
  5951: SSP      1                    
  5952: GADR     data[3910]           
  5953: LCP      [sp-4]               
  5954: GCP      data[3928]            ; = 8
  5955: ADD                           
  5956: PNT      4                    
  5957: ASGN                          
  5958: SSP      1                    
  5959: GADR     data[3929]           
  5960: LCP      [sp-4]               
  5961: GCP      data[3940]            ; = 1551134309
  5962: ADD                           
  5963: ASGN                          
  5964: SSP      1                    
  5965: GADR     data[3941]           
  5966: LCP      [sp-4]               
  5967: GCP      data[3960]            ; = 1818588764
  5968: ADD                           
  5969: PNT      4                    
  5970: ASGN                          
  5971: SSP      1                    
  5972: GADR     data[3961]           
  5973: LCP      [sp-4]               
  5974: GCP      data[3972]            ; = 1347372380
  5975: ADD                           
  5976: ASGN                          
  5977: SSP      1                    
  5978: GADR     data[3973]           
  5979: LCP      [sp-4]               
  5980: GCP      data[3991]            ; = 112
  5981: ADD                           
  5982: PNT      4                    
  5983: ASGN                          
  5984: SSP      1                    
  5985: GADR     data[3992]           
  5986: LCP      [sp-4]               
  5987: GCP      data[4002]            ; = 1769304389
  5988: ADD                           
  5989: ASGN                          
  5990: SSP      1                    
  5991: GADR     data[4003]           
  5992: LCP      [sp-4]               
  5993: GCP      data[4020]            ; = 1700745295
  5994: ADD                           
  5995: PNT      4                    
  5996: ASGN                          
  5997: SSP      1                    
  5998: GCP      data[4021]            ; = 1600479056
  5999: LCP      [sp-3]               
  6000: ASGN                          
  6001: SSP      1                    
  6002: RET      0                    
  6003: GADR     data[4022]           
  6004: LCP      [sp-4]               
  6005: GCP      data[4033]            ; = 5457218
  6006: ADD                           
  6007: ASGN                          
  6008: SSP      1                    
  6009: GADR     data[4034]           
  6010: LCP      [sp-4]               
  6011: GCP      data[4052]            ; = 1551134309
  6012: ADD                           
  6013: PNT      4                    
  6014: ASGN                          
  6015: SSP      1                    
  6016: GADR     data[4053]           
  6017: LCP      [sp-4]               
  6018: GCP      data[4063]            ; = 1599100227
  6019: ADD                           
  6020: ASGN                          
  6021: SSP      1                    
  6022: GADR     data[4064]           
  6023: LCP      [sp-4]               
  6024: GCP      data[4082]            ; = 1163684206
  6025: ADD                           
  6026: PNT      4                    
  6027: ASGN                          
  6028: SSP      1                    
  6029: GADR     data[4083]           
  6030: LCP      [sp-4]               
  6031: GCP      data[4094]            ; = 825255270
  6032: ADD                           
  6033: ASGN                          
  6034: SSP      1                    
  6035: GADR     data[4095]           
  6036: LCP      [sp-4]               
  6037: GCP      data[4114]            ; = 1852140912
  6038: ADD                           
  6039: PNT      4                    
  6040: ASGN                          
  6041: SSP      1                    
  6042: GADR     data[4115]           
  6043: LCP      [sp-4]               
  6044: GCP      data[4125]            ; = 1329945715
  6045: ADD                           
  6046: ASGN                          
  6047: SSP      1                    
  6048: GADR     data[4126]           
  6049: LCP      [sp-4]               
  6050: GCP      data[4144]            ; = 1397047854
  6051: ADD                           
  6052: PNT      4                    
  6053: ASGN                          
  6054: SSP      1                    
  6055: GCP      data[4145]            ; = 5457218
  6056: LCP      [sp-3]               
  6057: ASGN                          
  6058: SSP      1                    
  6059: RET      0                    
  6060: GADR     data[4146]           
  6061: LCP      [sp-4]               
  6062: GCP      data[4157]            ; = 1970357596
  6063: ADD                           
  6064: ASGN                          
  6065: SSP      1                    
  6066: GADR     data[4158]           
  6067: LCP      [sp-4]               
  6068: GCP      data[4176]            ; = 1650413653
  6069: ADD                           
  6070: PNT      4                    
  6071: ASGN                          
  6072: SSP      1                    
  6073: GADR     data[4177]           
  6074: LCP      [sp-4]               
  6075: GCP      data[4187]            ; = 1600220012
  6076: ADD                           
  6077: ASGN                          
  6078: SSP      1                    
  6079: GADR     data[4188]           
  6080: LCP      [sp-4]               
  6081: GCP      data[4206]            ; = 1650814068
  6082: ADD                           
  6083: PNT      4                    
  6084: ASGN                          
  6085: SSP      1                    
  6086: GADR     data[4207]           
  6087: LCP      [sp-4]               
  6088: GCP      data[4218]            ; = 1572864
  6089: ADD                           
  6090: ASGN                          
  6091: SSP      1                    
  6092: GADR     data[4219]           
  6093: LCP      [sp-4]               
  6094: GCP      data[4237]            ; = 1700944979
  6095: ADD                           
  6096: PNT      4                    
  6097: ASGN                          
  6098: SSP      1                    
  6099: GADR     data[4238]           
  6100: LCP      [sp-4]               
  6101: GCP      data[4248]            ; = 909208927
  6102: ADD                           
  6103: ASGN                          
  6104: SSP      1                    
  6105: GADR     data[4249]           
  6106: LCP      [sp-4]               
  6107: GCP      data[4266]            ; = 2097152
  6108: ADD                           
  6109: PNT      4                    
  6110: ASGN                          
  6111: SSP      1                    
  6112: GCP      data[4267]            ; = 8192
  6113: LCP      [sp-3]               
  6114: ASGN                          
  6115: SSP      1                    
  6116: RET      0                    
  6117: GADR     data[4268]  ; " "    
  6118: LCP      [sp-4]               
  6119: GCP      data[4278]            ; = 1852140912
  6120: ADD                           
  6121: ASGN                          
  6122: SSP      1                    
  6123: GADR     data[4279]           
  6124: LCP      [sp-4]               
  6125: GCP      data[4296]            ; = 1936158305
  6126: ADD                           
  6127: PNT      4                    
  6128: ASGN                          
  6129: SSP      1                    
  6130: GADR     data[4297]           
  6131: LCP      [sp-4]               
  6132: GCP      data[4307]            ; = 1852600176
  6133: ADD                           
  6134: ASGN                          
  6135: SSP      1                    
  6136: GADR     data[4308]           
  6137: LCP      [sp-4]               
  6138: GCP      data[4325]            ; = 2020565615
  6139: ADD                           
  6140: PNT      4                    
  6141: ASGN                          
  6142: SSP      1                    
  6143: GADR     data[4326]           
  6144: LCP      [sp-4]               
  6145: GCP      data[4337]            ; = 1191182336
  6146: ADD                           
  6147: ASGN                          
  6148: SSP      1                    
  6149: GADR     data[4338]           
  6150: LCP      [sp-4]               
  6151: GCP      data[4355]            ; = 1551066466
  6152: ADD                           
  6153: PNT      4                    
  6154: ASGN                          
  6155: SSP      1                    
  6156: GADR     data[4356]           
  6157: LCP      [sp-4]               
  6158: GCP      data[4367]            ; = 1835884854
  6159: ADD                           
  6160: ASGN                          
  6161: SSP      1                    
  6162: GADR     data[4368]           
  6163: LCP      [sp-4]               
  6164: GCP      data[4386]            ; = 1548156928
  6165: ADD                           
  6166: PNT      4                    
  6167: ASGN                          
  6168: SSP      1                    
  6169: GADR     data[4387]           
  6170: LCP      [sp-4]               
  6171: GCP      data[4398]            ; = 1398103156
  6172: ADD                           
  6173: ASGN                          
  6174: SSP      1                    
  6175: GADR     data[4399]           
  6176: LCP      [sp-4]               
  6177: GCP      data[4417]            ; = 1802265974
  6178: ADD                           
  6179: PNT      4                    
  6180: ASGN                          
  6181: SSP      1                    
  6182: GADR     data[4418]           
  6183: LCP      [sp-4]               
  6184: GCP      data[4428]            ; = 1347372380
  6185: ADD                           
  6186: ASGN                          
  6187: SSP      1                    
  6188: GADR     data[4429]           
  6189: LCP      [sp-4]               
  6190: GCP      data[4446]            ; = 774922033
  6191: ADD                           
  6192: PNT      4                    
  6193: ASGN                          
  6194: SSP      1                    
  6195: GADR     data[4447]           
  6196: LCP      [sp-4]               
  6197: GCP      data[4457]            ; = 1191182336
  6198: ADD                           
  6199: ASGN                          
  6200: SSP      1                    
  6201: GADR     data[4458]           
  6202: LCP      [sp-4]               
  6203: GCP      data[4475]            ; = 1551066466
  6204: ADD                           
  6205: PNT      4                    
  6206: ASGN                          
  6207: SSP      1                    
  6208: GCP      data[4476]            ; = 1163686757
  6209: LCP      [sp-3]               
  6210: ASGN                          
  6211: SSP      1                    
  6212: RET      0                    
  6213: GADR     data[4477]           
  6214: LCP      [sp-4]               
  6215: GCP      data[4488]            ; = 811693157
  6216: ADD                           
  6217: ASGN                          
  6218: SSP      1                    
  6219: GADR     data[4489]           
  6220: LCP      [sp-4]               
  6221: GCP      data[4507]            ; = 1885959537
  6222: ADD                           
  6223: PNT      4                    
  6224: ASGN                          
  6225: SSP      1                    
  6226: GADR     data[4508]           
  6227: LCP      [sp-4]               
  6228: GCP      data[4518]            ; = 1886479708
  6229: ADD                           
  6230: ASGN                          
  6231: SSP      1                    
  6232: GADR     data[4519]           
  6233: LCP      [sp-4]               
  6234: GCP      data[4536]            ; = 1885299051
  6235: ADD                           
  6236: PNT      4                    
  6237: ASGN                          
  6238: SSP      1                    
  6239: GADR     data[4537]           
  6240: LCP      [sp-4]               
  6241: GCP      data[4547]            ; = 1600479056
  6242: ADD                           
  6243: ASGN                          
  6244: SSP      1                    
  6245: GADR     data[4548]           
  6246: LCP      [sp-4]               
  6247: GCP      data[4565]            ; = 1191182336
  6248: ADD                           
  6249: PNT      4                    
  6250: ASGN                          
  6251: SSP      1                    
  6252: GADR     data[4566]           
  6253: LCP      [sp-4]               
  6254: GCP      data[4577]            ; = 1432122478
  6255: ADD                           
  6256: ASGN                          
  6257: SSP      1                    
  6258: GADR     data[4578]           
  6259: LCP      [sp-4]               
  6260: GCP      data[4596]            ; = 1668050804
  6261: ADD                           
  6262: PNT      4                    
  6263: ASGN                          
  6264: SSP      1                    
  6265: GADR     data[4597]           
  6266: LCP      [sp-4]               
  6267: GCP      data[4608]            ; = 83
  6268: ADD                           
  6269: ASGN                          
  6270: SSP      1                    
  6271: GADR     data[4609]           
  6272: LCP      [sp-4]               
  6273: GCP      data[4627]            ; = 1548965212
  6274: ADD                           
  6275: PNT      4                    
  6276: ASGN                          
  6277: SSP      1                    
  6278: GADR     data[4628]           
  6279: LCP      [sp-4]               
  6280: GCP      data[4639]            ; = 1735287138
  6281: ADD                           
  6282: ASGN                          
  6283: SSP      1                    
  6284: GADR     data[4640]           
  6285: LCP      [sp-4]               
  6286: GCP      data[4658]            ; = 1700745295
  6287: ADD                           
  6288: PNT      4                    
  6289: ASGN                          
  6290: SSP      1                    
  6291: GADR     data[4659]           
  6292: LCP      [sp-4]               
  6293: GCP      data[4670]            ; = 811955041
  6294: ADD                           
  6295: ASGN                          
  6296: SSP      1                    
  6297: GADR     data[4671]           
  6298: LCP      [sp-4]               
  6299: GCP      data[4689]            ; = 1970357596
  6300: ADD                           
  6301: PNT      4                    
  6302: ASGN                          
  6303: SSP      1                    
  6304: GADR     data[4690]           
  6305: LCP      [sp-4]               
  6306: GCP      data[4700]            ; = 1650217813
  6307: ADD                           
  6308: ASGN                          
  6309: SSP      1                    
  6310: GADR     data[4701]           
  6311: LCP      [sp-4]               
  6312: GCP      data[4718]            ; = 825257573
  6313: ADD                           
  6314: PNT      4                    
  6315: ASGN                          
  6316: SSP      1                    
  6317: GCP      data[4719]            ; = 774975598
  6318: LCP      [sp-3]               
  6319: ASGN                          
  6320: SSP      1                    
  6321: RET      0                    
  6322: GADR     data[4720]           
  6323: LCP      [sp-4]               
  6324: GCP      data[4730]            ; = 1548156928
  6325: ADD                           
  6326: ASGN                          
  6327: SSP      1                    
  6328: GADR     data[4731]           
  6329: LCP      [sp-4]               
  6330: GCP      data[4748]            ; = 1130131569
  6331: ADD                           
  6332: PNT      4                    
  6333: ASGN                          
  6334: SSP      1                    
  6335: GADR     data[4749]           
  6336: LCP      [sp-4]               
  6337: GCP      data[4759]            ; = 1701600371
  6338: ADD                           
  6339: ASGN                          
  6340: SSP      1                    
  6341: GADR     data[4760]           
  6342: LCP      [sp-4]               
  6343: GCP      data[4778]            ; = 1600479056
  6344: ADD                           
  6345: PNT      4                    
  6346: ASGN                          
  6347: SSP      1                    
  6348: GADR     data[4779]           
  6349: LCP      [sp-4]               
  6350: GCP      data[4790]            ; = 1902456369
  6351: ADD                           
  6352: ASGN                          
  6353: SSP      1                    
  6354: GADR     data[4791]           
  6355: LCP      [sp-4]               
  6356: GCP      data[4809]            ; = 1432122478
  6357: ADD                           
  6358: PNT      4                    
  6359: ASGN                          
  6360: SSP      1                    
  6361: GADR     data[4810]           
  6362: LCP      [sp-4]               
  6363: GCP      data[4821]            ; = 1600479056
  6364: ADD                           
  6365: ASGN                          
  6366: SSP      1                    
  6367: GADR     data[4822]           
  6368: LCP      [sp-4]               
  6369: GCP      data[4840]            ; = 83
  6370: ADD                           
  6371: PNT      4                    
  6372: ASGN                          
  6373: SSP      1                    
  6374: GCP      data[4841]            ; = 134217728
  6375: LCP      [sp-3]               
  6376: ASGN                          
  6377: SSP      1                    
  6378: RET      0                    
  6379: GADR     data[4842]           
  6380: LCP      [sp-4]               
  6381: GCP      data[4853]            ; = 1701671017
  6382: ADD                           
  6383: ASGN                          
  6384: SSP      1                    
  6385: GADR     data[4854]           
  6386: LCP      [sp-4]               
  6387: GCP      data[4872]            ; = 1936158305
  6388: ADD                           
  6389: PNT      4                    
  6390: ASGN                          
  6391: SSP      1                    
  6392: GADR     data[4873]           
  6393: LCP      [sp-4]               
  6394: GCP      data[4883]            ; = 1633843574
  6395: ADD                           
  6396: ASGN                          
  6397: SSP      1                    
  6398: GADR     data[4884]           
  6399: LCP      [sp-4]               
  6400: GCP      data[4901]            ; = 1668050804
  6401: ADD                           
  6402: PNT      4                    
  6403: ASGN                          
  6404: SSP      1                    
  6405: GADR     data[4902]           
  6406: LCP      [sp-4]               
  6407: GCP      data[4912]            ; = 28785
  6408: ADD                           
  6409: ASGN                          
  6410: SSP      1                    
  6411: GADR     data[4913]           
  6412: LCP      [sp-4]               
  6413: GCP      data[4930]            ; = 1852140912
  6414: ADD                           
  6415: PNT      4                    
  6416: ASGN                          
  6417: SSP      1                    
  6418: GADR     data[4931]           
  6419: LCP      [sp-4]               
  6420: GCP      data[4941]            ; = 1329945715
  6421: ADD                           
  6422: ASGN                          
  6423: SSP      1                    
  6424: GADR     data[4942]           
  6425: LCP      [sp-4]               
  6426: GCP      data[4959]            ; = 21317
  6427: ADD                           
  6428: PNT      4                    
  6429: ASGN                          
  6430: SSP      1                    
  6431: GADR     data[4960]           
  6432: LCP      [sp-4]               
  6433: GCP      data[4970]            ; = 1769304389
  6434: ADD                           
  6435: ASGN                          
  6436: SSP      1                    
  6437: GADR     data[4971]           
  6438: LCP      [sp-4]               
  6439: GCP      data[4988]            ; = 1650413653
  6440: ADD                           
  6441: PNT      4                    
  6442: ASGN                          
  6443: SSP      1                    
  6444: GADR     data[4989]           
  6445: LCP      [sp-4]               
  6446: GCP      data[5000]            ; = 1634430053
  6447: ADD                           
  6448: ASGN                          
  6449: SSP      1                    
  6450: GADR     data[5001]           
  6451: LCP      [sp-4]               
  6452: GCP      data[5019]            ; = 1734435431
  6453: ADD                           
  6454: PNT      4                    
  6455: ASGN                          
  6456: SSP      1                    
  6457: GADR     data[5020]           
  6458: LCP      [sp-4]               
  6459: GCP      data[5031]            ; = 0
  6460: ADD                           
  6461: ASGN                          
  6462: SSP      1                    
  6463: GADR     data[5032]           
  6464: LCP      [sp-4]               
  6465: GCP      data[5050]            ; = 1936024156
  6466: ADD                           
  6467: PNT      4                    
  6468: ASGN                          
  6469: SSP      1                    
  6470: GCP      data[5051]            ; = 1551066466
  6471: LCP      [sp-3]               
  6472: ASGN                          
  6473: SSP      1                    
  6474: RET      0                    
  6475: GADR     data[5052]           
  6476: LCP      [sp-4]               
  6477: GCP      data[5063]            ; = 1701147758
  6478: ADD                           
  6479: ASGN                          
  6480: SSP      1                    
  6481: GADR     data[5064]           
  6482: LCP      [sp-4]               
  6483: GCP      data[5082]            ; = 1769304389
  6484: ADD                           
  6485: PNT      4                    
  6486: ASGN                          
  6487: SSP      1                    
  6488: GADR     data[5083]           
  6489: LCP      [sp-4]               
  6490: GCP      data[5093]            ; = 1902468179
  6491: ADD                           
  6492: ASGN                          
  6493: SSP      1                    
  6494: GADR     data[5094]           
  6495: LCP      [sp-4]               
  6496: GCP      data[5111]            ; = 1802265974
  6497: ADD                           
  6498: PNT      4                    
  6499: ASGN                          
  6500: SSP      1                    
  6501: GADR     data[5112]           
  6502: LCP      [sp-4]               
  6503: GCP      data[5122]            ; = 1347372380
  6504: ADD                           
  6505: ASGN                          
  6506: SSP      1                    
  6507: GADR     data[5123]           
  6508: LCP      [sp-4]               
  6509: GCP      data[5140]            ; = 28785
  6510: ADD                           
  6511: PNT      4                    
  6512: ASGN                          
  6513: SSP      1                    
  6514: GADR     data[5141]           
  6515: LCP      [sp-4]               
  6516: GCP      data[5152]            ; = 1836083573
  6517: ADD                           
  6518: ASGN                          
  6519: SSP      1                    
  6520: GADR     data[5153]           
  6521: LCP      [sp-4]               
  6522: GCP      data[5171]            ; = 1633902437
  6523: ADD                           
  6524: PNT      4                    
  6525: ASGN                          
  6526: SSP      1                    
  6527: GADR     data[5172]           
  6528: LCP      [sp-4]               
  6529: GCP      data[5182]            ; = 1397047854
  6530: ADD                           
  6531: ASGN                          
  6532: SSP      1                    
  6533: GADR     data[5183]           
  6534: LCP      [sp-4]               
  6535: GCP      data[5200]            ; = 1551134309
  6536: ADD                           
  6537: PNT      4                    
  6538: ASGN                          
  6539: SSP      1                    
  6540: GADR     data[5201]           
  6541: LCP      [sp-4]               
  6542: GCP      data[5212]            ; = 1650413653
  6543: ADD                           
  6544: ASGN                          
  6545: SSP      1                    
  6546: GADR     data[5213]           
  6547: LCP      [sp-4]               
  6548: GCP      data[5231]            ; = 1550413420
  6549: ADD                           
  6550: PNT      4                    
  6551: ASGN                          
  6552: SSP      1                    
  6553: GADR     data[5232]           
  6554: LCP      [sp-4]               
  6555: GCP      data[5243]            ; = 1701147758
  6556: ADD                           
  6557: ASGN                          
  6558: SSP      1                    
  6559: GADR     data[5244]           
  6560: LCP      [sp-4]               
  6561: GCP      data[5262]            ; = 1548156928
  6562: ADD                           
  6563: PNT      4                    
  6564: ASGN                          
  6565: SSP      1                    
  6566: GADR     data[5263]           
  6567: LCP      [sp-4]               
  6568: GCP      data[5273]            ; = 1432122478
  6569: ADD                           
  6570: ASGN                          
  6571: SSP      1                    
  6572: GADR     data[5274]           
  6573: LCP      [sp-4]               
  6574: GCP      data[5291]            ; = 1701606516
  6575: ADD                           
  6576: PNT      4                    
  6577: ASGN                          
  6578: SSP      1                    
  6579: GCP      data[5292]            ; = 1650814068
  6580: LCP      [sp-3]               
  6581: ASGN                          
  6582: SSP      1                    
  6583: RET      0                    
  6584: GADR     data[5293]           
  6585: LCP      [sp-4]               
  6586: GCP      data[5304]            ; = 0
  6587: ADD                           
  6588: ASGN                          
  6589: SSP      1                    
  6590: GADR     data[5305]           
  6591: LCP      [sp-4]               
  6592: GCP      data[5323]            ; = 1548965212
  6593: ADD                           
  6594: PNT      4                    
  6595: ASGN                          
  6596: SSP      1                    
  6597: GADR     data[5324]           
  6598: LCP      [sp-4]               
  6599: GCP      data[5334]            ; = 1869767263
  6600: ADD                           
  6601: ASGN                          
  6602: SSP      1                    
  6603: GADR     data[5335]           
  6604: LCP      [sp-4]               
  6605: GCP      data[5352]            ; = 1163684206
  6606: ADD                           
  6607: PNT      4                    
  6608: ASGN                          
  6609: SSP      1                    
  6610: GADR     data[5353]           
  6611: LCP      [sp-4]               
  6612: GCP      data[5364]            ; = 1650814068
  6613: ADD                           
  6614: ASGN                          
  6615: SSP      1                    
  6616: GADR     data[5365]           
  6617: LCP      [sp-4]               
  6618: GCP      data[5383]            ; = 1163675392
  6619: ADD                           
  6620: PNT      4                    
  6621: ASGN                          
  6622: SSP      1                    
  6623: GADR     data[5384]           
  6624: LCP      [sp-4]               
  6625: GCP      data[5394]            ; = 1398103156
  6626: ADD                           
  6627: ASGN                          
  6628: SSP      1                    
  6629: GADR     data[5395]           
  6630: LCP      [sp-4]               
  6631: GCP      data[5413]            ; = 1651469677
  6632: ADD                           
  6633: PNT      4                    
  6634: ASGN                          
  6635: SSP      1                    
  6636: GADR     data[5414]           
  6637: LCP      [sp-4]               
  6638: GCP      data[5425]            ; = 536870912
  6639: ADD                           
  6640: ASGN                          
  6641: SSP      1                    
  6642: GADR     data[5426]           
  6643: LCP      [sp-4]               
  6644: GCP      data[5444]            ; = 1700549461
  6645: ADD                           
  6646: PNT      4                    
  6647: ASGN                          
  6648: SSP      1                    
  6649: GCP      data[5445]            ; = 1902468179
  6650: LCP      [sp-3]               
  6651: ASGN                          
  6652: SSP      1                    
  6653: RET      0                    
  6654: GADR     data[5446]           
  6655: LCP      [sp-4]               
  6656: GCP      data[5456]            ; = 1936617330
  6657: ADD                           
  6658: ASGN                          
  6659: SSP      1                    
  6660: GADR     data[5457]           
  6661: LCP      [sp-4]               
  6662: GCP      data[5474]            ; = 1347372380
  6663: ADD                           
  6664: PNT      4                    
  6665: ASGN                          
  6666: SSP      1                    
  6667: GADR     data[5475]           
  6668: LCP      [sp-4]               
  6669: GCP      data[5485]            ; = 1651469677
  6670: ADD                           
  6671: ASGN                          
  6672: SSP      1                    
  6673: GADR     data[5486]           
  6674: LCP      [sp-4]               
  6675: GCP      data[5503]            ; = 1163675392
  6676: ADD                           
  6677: PNT      4                    
  6678: ASGN                          
  6679: SSP      1                    
  6680: GADR     data[5504]           
  6681: LCP      [sp-4]               
  6682: GCP      data[5515]            ; = 1548965212
  6683: ADD                           
  6684: ASGN                          
  6685: SSP      1                    
  6686: GADR     data[5516]           
  6687: LCP      [sp-4]               
  6688: GCP      data[5533]            ; = 1651469677
  6689: ADD                           
  6690: PNT      4                    
  6691: ASGN                          
  6692: SSP      1                    
  6693: GADR     data[5534]           
  6694: LCP      [sp-4]               
  6695: GCP      data[5545]            ; = 671088640
  6696: ADD                           
  6697: ASGN                          
  6698: SSP      1                    
  6699: GADR     data[5546]           
  6700: LCP      [sp-4]               
  6701: GCP      data[5563]            ; = 1548965212
  6702: ADD                           
  6703: PNT      4                    
  6704: ASGN                          
  6705: SSP      1                    
  6706: GADR     data[5564]           
  6707: LCP      [sp-4]               
  6708: GCP      data[5575]            ; = 1852797538
  6709: ADD                           
  6710: ASGN                          
  6711: SSP      1                    
  6712: GADR     data[5576]           
  6713: LCP      [sp-4]               
  6714: GCP      data[5594]            ; = 1347372380
  6715: ADD                           
  6716: PNT      4                    
  6717: ASGN                          
  6718: SSP      1                    
  6719: GADR     data[5595]           
  6720: LCP      [sp-4]               
  6721: GCP      data[5606]            ; = 1868722029
  6722: ADD                           
  6723: ASGN                          
  6724: SSP      1                    
  6725: GADR     data[5607]           
  6726: LCP      [sp-4]               
  6727: GCP      data[5625]            ; = 1970357596
  6728: ADD                           
  6729: PNT      4                    
  6730: ASGN                          
  6731: SSP      1                    
  6732: GADR     data[5626]           
  6733: LCP      [sp-4]               
  6734: GCP      data[5636]            ; = 1650217813
  6735: ADD                           
  6736: ASGN                          
  6737: SSP      1                    
  6738: GADR     data[5637]           
  6739: LCP      [sp-4]               
  6740: GCP      data[5654]            ; = 1935762284
  6741: ADD                           
  6742: PNT      4                    
  6743: ASGN                          
  6744: SSP      1                    
  6745: GCP      data[5655]            ; = 1702060387
  6746: LCP      [sp-3]               
  6747: ASGN                          
  6748: SSP      1                    
  6749: RET      0                    
  6750: GADR     data[5656]           
  6751: LCP      [sp-4]               
  6752: GCP      data[5666]            ; = 3145728
  6753: ADD                           
  6754: ASGN                          
  6755: SSP      1                    
  6756: GADR     data[5667]           
  6757: LCP      [sp-4]               
  6758: GCP      data[5684]            ; = 1700549461
  6759: ADD                           
  6760: PNT      4                    
  6761: ASGN                          
  6762: SSP      1                    
  6763: GADR     data[5685]           
  6764: LCP      [sp-4]               
  6765: GCP      data[5696]            ; = 1936617330
  6766: ADD                           
  6767: ASGN                          
  6768: SSP      1                    
  6769: GADR     data[5697]           
  6770: LCP      [sp-4]               
  6771: GCP      data[5715]            ; = 1599098693
  6772: ADD                           
  6773: PNT      4                    
  6774: ASGN                          
  6775: SSP      1                    
  6776: GADR     data[5716]           
  6777: LCP      [sp-4]               
  6778: GCP      data[5726]            ; = 1935762284
  6779: ADD                           
  6780: ASGN                          
  6781: SSP      1                    
  6782: GADR     data[5727]           
  6783: LCP      [sp-4]               
  6784: GCP      data[5744]  ; "G\Equipment\US\bes\EOP_hat1US_v01.BES" ; "G\Equipment\US\bes\EOP_hat1US_"
  6785: ADD                           
  6786: PNT      4                    
  6787: ASGN                          
  6788: SSP      1                    
  6789: GADR     data[5745]           
  6790: LCP      [sp-4]               
  6791: GCP      data[5755]            ; = 1548965212
  6792: ADD                           
  6793: ASGN                          
  6794: SSP      1                    
  6795: GADR     data[5756]           
  6796: LCP      [sp-4]               
  6797: GCP      data[5774]            ; = 774975606
  6798: ADD                           
  6799: PNT      4                    
  6800: ASGN                          
  6801: SSP      1                    
  6802: GADR     data[5775]           
  6803: LCP      [sp-4]               
  6804: GCP      data[5786]            ; = 1548156928
  6805: ADD                           
  6806: ASGN                          
  6807: SSP      1                    
  6808: GADR     data[5787]           
  6809: LCP      [sp-4]               
  6810: GCP      data[5805]            ; = 1430477936
  6811: ADD                           
  6812: PNT      4                    
  6813: ASGN                          
  6814: SSP      1                    
  6815: GADR     data[5806]           
  6816: LCP      [sp-4]               
  6817: GCP      data[5817]            ; = 1702255726
  6818: ADD                           
  6819: ASGN                          
  6820: SSP      1                    
  6821: GADR     data[5818]           
  6822: LCP      [sp-4]               
  6823: GCP      data[5836]            ; = 1429304417
  6824: ADD                           
  6825: PNT      4                    
  6826: ASGN                          
  6827: SSP      1                    
  6828: GADR     data[5837]           
  6829: LCP      [sp-4]               
  6830: GCP      data[5847]            ; = 28785
  6831: ADD                           
  6832: ASGN                          
  6833: SSP      1                    
  6834: GADR     data[5848]           
  6835: LCP      [sp-4]               
  6836: GCP      data[5865]            ; = 1701671017
  6837: ADD                           
  6838: PNT      4                    
  6839: ASGN                          
  6840: SSP      1                    
  6841: GCP      data[5866]            ; = 1852140912
  6842: LCP      [sp-3]               
  6843: ASGN                          
  6844: SSP      1                    
  6845: RET      0                    
  6846: GADR     data[5867]           
  6847: LCP      [sp-4]               
  6848: GCP      data[5877]            ; = 1329945715
  6849: ADD                           
  6850: ASGN                          
  6851: SSP      1                    
  6852: GADR     data[5878]           
  6853: LCP      [sp-4]               
  6854: GCP      data[5895]            ; = 5457218
  6855: ADD                           
  6856: PNT      4                    
  6857: ASGN                          
  6858: SSP      1                    
  6859: GADR     data[5896]           
  6860: LCP      [sp-4]               
  6861: GCP      data[5906]            ; = 1769304389
  6862: ADD                           
  6863: ASGN                          
  6864: SSP      1                    
  6865: GADR     data[5907]           
  6866: LCP      [sp-4]               
  6867: GCP      data[5925]            ; = 1919049552
  6868: ADD                           
  6869: PNT      4                    
  6870: ASGN                          
  6871: SSP      1                    
  6872: GADR     data[5926]           
  6873: LCP      [sp-4]               
  6874: GCP      data[5937]            ; = 1600482152
  6875: ADD                           
  6876: ASGN                          
  6877: SSP      1                    
  6878: GADR     data[5938]           
  6879: LCP      [sp-4]               
  6880: GCP      data[5956]            ; = 1953390947
  6881: ADD                           
  6882: PNT      4                    
  6883: ASGN                          
  6884: SSP      1                    
  6885: GADR     data[5957]           
  6886: LCP      [sp-4]               
  6887: GCP      data[5968]            ; = 7369061
  6888: ADD                           
  6889: ASGN                          
  6890: SSP      1                    
  6891: GADR     data[5969]           
  6892: LCP      [sp-4]               
  6893: GCP      data[5987]            ; = 1548965212
  6894: ADD                           
  6895: PNT      4                    
  6896: ASGN                          
  6897: SSP      1                    
  6898: GCP      data[5988]            ; = 1650217813
  6899: LCP      [sp-3]               
  6900: ASGN                          
  6901: SSP      1                    
  6902: RET      0                    
  6903: GADR     data[5989]           
  6904: LCP      [sp-4]               
  6905: GCP      data[5999]            ; = 1768972133
  6906: ADD                           
  6907: ASGN                          
  6908: SSP      1                    
  6909: GADR     data[6000]           
  6910: LCP      [sp-4]               
  6911: GCP      data[6016]            ; = 83
  6912: ADD                           
  6913: PNT      4                    
  6914: ASGN                          
  6915: SSP      1                    
  6916: GADR     data[6017]           
  6917: LCP      [sp-4]               
  6918: GCP      data[6027]            ; = 1885959537
  6919: ADD                           
  6920: ASGN                          
  6921: SSP      1                    
  6922: GADR     data[6028]           
  6923: LCP      [sp-4]               
  6924: GCP      data[6045]            ; = 1919049552
  6925: ADD                           
  6926: PNT      4                    
  6927: ASGN                          
  6928: SSP      1                    
  6929: GADR     data[6046]           
  6930: LCP      [sp-4]               
  6931: GCP      data[6056]            ; = 1701537893
  6932: ADD                           
  6933: ASGN                          
  6934: SSP      1                    
  6935: GADR     data[6057]           
  6936: LCP      [sp-4]               
  6937: GCP      data[6074]            ; = 1768972133
  6938: ADD                           
  6939: PNT      4                    
  6940: ASGN                          
  6941: SSP      1                    
  6942: GADR     data[6075]           
  6943: LCP      [sp-4]               
  6944: GCP      data[6086]            ; = 1697526064
  6945: ADD                           
  6946: ASGN                          
  6947: SSP      1                    
  6948: GADR     data[6087]           
  6949: LCP      [sp-4]               
  6950: GCP      data[6104]            ; = 1836083573
  6951: ADD                           
  6952: PNT      4                    
  6953: ASGN                          
  6954: SSP      1                    
  6955: GADR     data[6105]           
  6956: LCP      [sp-4]               
  6957: GCP      data[6116]            ; = 1163686757
  6958: ADD                           
  6959: ASGN                          
  6960: SSP      1                    
  6961: GADR     data[6117]           
  6962: LCP      [sp-4]               
  6963: GCP      data[6135]            ; = 21317
  6964: ADD                           
  6965: PNT      4                    
  6966: ASGN                          
  6967: SSP      1                    
  6968: GADR     data[6136]           
  6969: LCP      [sp-4]               
  6970: GCP      data[6147]            ; = 1885959537
  6971: ADD                           
  6972: ASGN                          
  6973: SSP      1                    
  6974: GADR     data[6148]           
  6975: LCP      [sp-4]               
  6976: GCP      data[6166]            ; = 1869767263
  6977: ADD                           
  6978: PNT      4                    
  6979: ASGN                          
  6980: SSP      1                    
  6981: GADR     data[6167]           
  6982: LCP      [sp-4]               
  6983: GCP      data[6177]            ; = 1600482152
  6984: ADD                           
  6985: ASGN                          
  6986: SSP      1                    
  6987: GADR     data[6178]           
  6988: LCP      [sp-4]               
  6989: GCP      data[6195]            ; = 1429304417
  6990: ADD                           
  6991: PNT      4                    
  6992: ASGN                          
  6993: SSP      1                    
  6994: GCP      data[6196]            ; = 1398092148
  6995: LCP      [sp-3]               
  6996: ASGN                          
  6997: SSP      1                    
  6998: RET      0                    
  6999: GADR     data[6197]           
  7000: LCP      [sp-4]               
  7001: GCP      data[6208]            ; = 0
  7002: ADD                           
  7003: ASGN                          
  7004: SSP      1                    
  7005: GADR     data[6209]           
  7006: LCP      [sp-4]               
  7007: GCP      data[6227]            ; = 1953391981
  7008: ADD                           
  7009: PNT      4                    
  7010: ASGN                          
  7011: SSP      1                    
  7012: GADR     data[6228]           
  7013: LCP      [sp-4]               
  7014: GCP      data[6238]            ; = 1347372380
  7015: ADD                           
  7016: ASGN                          
  7017: SSP      1                    
  7018: GADR     data[6239]           
  7019: LCP      [sp-4]               
  7020: GCP      data[6256]            ; = 83
  7021: ADD                           
  7022: PNT      4                    
  7023: ASGN                          
  7024: SSP      1                    
  7025: GADR     data[6257]           
  7026: LCP      [sp-4]               
  7027: GCP      data[6268]            ; = 1836083573
  7028: ADD                           
  7029: ASGN                          
  7030: SSP      1                    
  7031: GADR     data[6269]           
  7032: LCP      [sp-4]               
  7033: GCP      data[6287]            ; = 1668248163
  7034: ADD                           
  7035: PNT      4                    
  7036: ASGN                          
  7037: SSP      1                    
  7038: GADR     data[6288]           
  7039: LCP      [sp-4]               
  7040: GCP      data[6299]            ; = 1869635425
  7041: ADD                           
  7042: ASGN                          
  7043: SSP      1                    
  7044: GADR     data[6300]           
  7045: LCP      [sp-4]               
  7046: GCP      data[6318]            ; = 774975606
  7047: ADD                           
  7048: PNT      4                    
  7049: ASGN                          
  7050: SSP      1                    
  7051: GADR     data[6319]           
  7052: LCP      [sp-4]               
  7053: GCP      data[6330]            ; = 1548156928
  7054: ADD                           
  7055: ASGN                          
  7056: SSP      1                    
  7057: GADR     data[6331]           
  7058: LCP      [sp-4]               
  7059: GCP      data[6349]            ; = 1329945715
  7060: ADD                           
  7061: PNT      4                    
  7062: ASGN                          
  7063: SSP      1                    
  7064: GADR     data[6350]           
  7065: LCP      [sp-4]               
  7066: GCP      data[6361]            ; = 1667851365
  7067: ADD                           
  7068: ASGN                          
  7069: SSP      1                    
  7070: GADR     data[6362]           
  7071: LCP      [sp-4]               
  7072: GCP      data[6380]            ; "G\Equipment\US\eqp\CUP_crocker"
  7073: ADD                           
  7074: PNT      4                    
  7075: ASGN                          
  7076: SSP      1                    
  7077: GADR     data[6381]           
  7078: LCP      [sp-4]               
  7079: GCP      data[6391]            ; = 1548965212
  7080: ADD                           
  7081: ASGN                          
  7082: SSP      1                    
  7083: GADR     data[6392]           
  7084: LCP      [sp-4]               
  7085: GCP      data[6409]            ; = 1702255730
  7086: ADD                           
  7087: PNT      4                    
  7088: ASGN                          
  7089: SSP      1                    
  7090: GADR     data[6410]           
  7091: LCP      [sp-4]               
  7092: GCP      data[6420]            ; = 1163684206
  7093: ADD                           
  7094: ASGN                          
  7095: SSP      1                    
  7096: GADR     data[6421]           
  7097: LCP      [sp-4]               
  7098: GCP      data[6438]            ; = 825255777
  7099: ADD                           
  7100: PNT      4                    
  7101: ASGN                          
  7102: SSP      1                    
  7103: GCP      data[6439]            ; = 774975591
  7104: LCP      [sp-3]               
  7105: ASGN                          
  7106: SSP      1                    
  7107: RET      0                    
func_7108:
  7108: LCP      [sp-4]               
  7109: LCP      [sp-3]               
  7110: CALL     func_4670            
  7111: SSP      2                    
  7112: RET      0                    
ScriptMain:
  7113: ASP      39                   
  7114: ASP      20                   
  7115: ASP      3                    
  7116: ASP      3                    
  7117: ASP      1                    
  7118: GCP      data[6440]            ; = 1697526064
  7119: GCP      data[6441]            ; = 1902456369
  7120: EQU                           
  7121: JZ       label_7275           
  7122: LADR     [sp+0]               
  7123: GCP      data[6442]            ; = 1886479662
  7124: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  7125: SSP      2                    
  7126: LADR     [sp+39]              
  7127: GCP      data[6443]            ; = 7369061
  7128: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  7129: SSP      2                    
  7130: GCP      data[6444]            ; = 28785
  7131: LADR     [sp+0]               
  7132: ASGN                          
  7133: SSP      1                    
  7134: GCP      data[6445]            ; = 134217840
  7135: LADR     [sp+0]               
  7136: PNT      4                    
  7137: ASGN                          
  7138: SSP      1                    
  7139: GCP      data[6446]            ; = 524288
  7140: LADR     [sp+0]               
  7141: PNT      8                    
  7142: ASGN                          
  7143: SSP      1                    
  7144: GCP      data[6447]            ; = 2048
  7145: LADR     [sp+0]               
  7146: PNT      12                   
  7147: ASGN                          
  7148: SSP      1                    
  7149: ASP      1                    
  7150: ASP      1                    
  7151: CALL     func_0993            
  7152: LLD      [sp+66]              
  7153: JZ       label_7155           
  7154: JMP      label_7161           
label_7155:
  7155: GADR     data[6448]           
  7156: LADR     [sp+0]               
  7157: PNT      24                   
  7158: ASGN                          
  7159: SSP      1                    
  7160: JMP      label_7166           
label_7161:
  7161: GADR     data[6455]           
  7162: LADR     [sp+0]               
  7163: PNT      24                   
  7164: ASGN                          
  7165: SSP      1                    
label_7166:
  7166: GCP      data[6463]            ; = 1548965212
  7167: LADR     [sp+0]               
  7168: PNT      16                   
  7169: ASGN                          
  7170: SSP      1                    
  7171: LADR     [sp-4]               
  7172: DADR     data[16]             
  7173: DCP      4                    
  7174: LADR     [sp+0]               
  7175: PNT      28                   
  7176: ASGN                          
  7177: SSP      1                    
  7178: LADR     [sp+0]               
  7179: CALL     func_0318            
  7180: SSP      1                    
  7181: GCP      data[6464]            ; = 1650217813
  7182: LADR     [sp+0]               
  7183: PNT      76                   
  7184: ASGN                          
  7185: SSP      1                    
  7186: GCP      data[6465]            ; = 1700944979
  7187: LADR     [sp+0]               
  7188: PNT      72                   
  7189: ASGN                          
  7190: SSP      1                    
  7191: ASP      1                    
  7192: GCP      data[6466]            ; = 1936024156
  7193: ASP      1                    
  7194: XCALL    $SC_ggi(unsignedlong)int ; args=1
  7195: LLD      [sp+66]              
  7196: SSP      1                    
  7197: LADR     [sp+0]               
  7198: PNT      44                   
  7199: ASGN                          
  7200: SSP      1                    
  7201: LADR     [sp+0]               
  7202: PNT      44                   
  7203: DCP      4                    
  7204: JZ       label_7206           
  7205: JMP      label_7211           
label_7206:
  7206: GCP      data[6467]            ; = 1551066466
  7207: LADR     [sp+0]               
  7208: PNT      44                   
  7209: ASGN                          
  7210: SSP      1                    
label_7211:
  7211: LADR     [sp+0]               
  7212: PNT      44                   
  7213: DCP      4                    
  7214: GCP      data[6468]            ; = 1163686757
  7215: EQU                           
  7216: JZ       label_7222           
  7217: GCP      data[6469]            ; = 1329945715
  7218: LADR     [sp+0]               
  7219: PNT      44                   
  7220: ASGN                          
  7221: SSP      1                    
label_7222:
  7222: GCP      data[6470]            ; = 1347372380
  7223: LADR     [sp+0]               
  7224: PNT      48                   
  7225: ASGN                          
  7226: SSP      1                    
  7227: GCP      data[6471]            ; = 1599098693
  7228: LADR     [sp+0]               
  7229: PNT      52                   
  7230: ASGN                          
  7231: SSP      1                    
  7232: GCP      data[6472]            ; = 1700745295
  7233: LADR     [sp+0]               
  7234: PNT      56                   
  7235: ASGN                          
  7236: SSP      1                    
  7237: GCP      data[6473]            ; = 1600479056
  7238: LADR     [sp+0]               
  7239: PNT      64                   
  7240: ASGN                          
  7241: SSP      1                    
  7242: LADR     [sp+39]              
  7243: LADR     [sp+65]              
  7244: CALL     func_7108            
  7245: SSP      2                    
  7246: LCP      [sp+65]              
  7247: LADR     [sp+0]               
  7248: PNT      84                   
  7249: ASGN                          
  7250: SSP      1                    
  7251: LADR     [sp+39]              
  7252: LADR     [sp+0]               
  7253: PNT      88                   
  7254: ASGN                          
  7255: SSP      1                    
  7256: GCP      data[6474]            ; = 1667196255
  7257: LADR     [sp+0]               
  7258: PNT      36                   
  7259: ASGN                          
  7260: SSP      1                    
  7261: ASP      1                    
  7262: LADR     [sp+0]               
  7263: ASP      1                    
  7264: XCALL    $SC_P_Create(*s_SC_P_Create)unsignedlong ; args=1
  7265: LLD      [sp+66]              
  7266: SSP      1                    
  7267: LADR     [sp-4]               
  7268: DADR     data[12]             
  7269: ASGN                          
  7270: SSP      1                    
  7271: GCP      data[6475]            ; = 1633902437
  7272: GADR     data[6440]           
  7273: ASGN                          
  7274: SSP      1                    
label_7275:
  7275: GCP      data[6476]            ; = 1851876191
  7276: LADR     [sp-4]               
  7277: DADR     data[24]             
  7278: ASGN                          
  7279: SSP      1                    
  7280: ASP      1                    
  7281: LADR     [sp-4]               
  7282: DADR     data[12]             
  7283: DCP      4                    
  7284: ASP      1                    
  7285: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  7286: LLD      [sp+66]              
  7287: SSP      1                    
  7288: JZ       label_7290           
  7289: JMP      label_7298           
label_7290:
  7290: GCP      data[6477]            ; = 1953390947
  7291: LADR     [sp-4]               
  7292: DADR     data[24]             
  7293: ASGN                          
  7294: SSP      1                    
  7295: GCP      data[6478]            ; = 1702129249
  7296: LLD      [sp-3]               
  7297: RET      66                   
label_7298:
  7298: GCP      data[6440]            ; = 1697526064
  7299: JMP      label_7301           
  7300: JMP      label_7305           
label_7301:
  7301: LCP      [sp+66]              
  7302: GCP      data[6479]            ; = 1701147758
  7303: EQU                           
  7304: JZ       label_7325           
label_7305:
  7305: GCP      data[6480]            ; = 1852138868
  7306: GADR     data[6440]           
  7307: ASGN                          
  7308: SSP      1                    
  7309: LADR     [sp-4]               
  7310: DADR     data[12]             
  7311: DCP      4                    
  7312: GCP      data[6481]            ; = 812541285
  7313: XCALL    $SC_P_SetSpeachDist(unsignedlong,float)void ; args=2
  7314: SSP      2                    
  7315: CALL     func_0772            
  7316: CALL     func_0756            
  7317: GCP      data[6482]            ; = 825257573
  7318: XCALL    $SC_PC_EnablePronePosition(int)void ; args=1
  7319: SSP      1                    
  7320: GCP      data[6483]            ; = 774975598
  7321: XCALL    $SC_PC_EnableFlashLight(int)void ; args=1
  7322: SSP      1                    
  7323: JMP      label_7330           
  7324: JMP      label_7329           
label_7325:
  7325: LCP      [sp+66]              
  7326: GCP      data[6484]            ; = 1110323504
  7327: EQU                           
  7328: JZ       label_7330           
label_7329:
  7329: JMP      label_7330           
label_7330:
  7330: SSP      1                    
  7331: GCP      data[6485]            ; = 1161965105
  7332: LLD      [sp-3]               
  7333: RET      66                   
