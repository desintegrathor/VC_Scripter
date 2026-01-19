; ==========================================
; Disassembly of: decompilation_work_folder/TUNNELS01/SCRIPTS/LEVEL.SCR
; Instructions: 10051
; External functions: 97
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
;   [ 61] SC_SetObjectives(unsignedlong,*s_SC_Objective,float)void
;   [ 62] SC_SetObjectivesNoSound(unsignedlong,*s_SC_Objective,float)void
;   [ 63] SC_Ai_SetPlFollow(unsignedlong,unsignedlong,unsignedlong,*s_SC_Ai_PlFollow,*unsignedlong,*unsignedlong,unsignedlong)void
;   [ 64] SC_RadioSetDist(float)void
;   [ 65] SC_P_Speach(unsignedlong,unsignedlong,unsignedlong,*float)void
;   [ 66] SC_SpeachRadio(unsignedlong,unsignedlong,*float)void
;   [ 67] SC_IsNear2D(*c_Vector3,*c_Vector3,float)int
;   [ 68] SC_Ai_SetPeaceMode(unsignedlong,unsignedlong,unsignedlong)void
;   [ 69] SC_Ai_PointStopDanger(unsignedlong,unsignedlong)void
;   [ 70] SC_P_Speech2(unsignedlong,unsignedlong,*float)void
;   [ 71] SC_Ai_ClearCheckPoints(unsignedlong,unsignedlong)void
;   [ 72] sprintf(*char,*constchar,...)int
;   [ 73] SC_Ai_AddCheckPoint(unsignedlong,unsignedlong,*c_Vector3,unsignedlong)void
;   [ 74] SC_P_GetWillTalk(unsignedlong)float
;   [ 75] SC_P_SpeechMes2(unsignedlong,unsignedlong,*float,unsignedlong)void
;   [ 76] SC_P_Ai_Go(unsignedlong,*c_Vector3)void
;   [ 77] SC_AGS_Set(unsignedlong)unsignedlong
;   [ 78] SC_P_Ai_GetShooting(unsignedlong,*unsignedlong)int
;   [ 79] SC_P_GetDistance(unsignedlong,unsignedlong)float
;   [ 80] SC_SetObjectScript(*char,*char)void
;   [ 81] SC_NOD_GetName(*void)*char
;   [ 82] SC_StringSame(*char,*char)int
;   [ 83] SC_DeathCamera_Enable(int)void
;   [ 84] SC_InitSide(unsignedlong,*s_SC_initside)void
;   [ 85] SC_InitSideGroup(*s_SC_initgroup)void
;   [ 86] SC_Ai_SetShootOnHeardEnemyColTest(int)void
;   [ 87] SC_Ai_SetGroupEnemyUpdate(unsignedlong,unsignedlong,int)void
;   [ 88] SC_SetCommandMenu(unsignedlong)void
;   [ 89] SC_PC_EnableMovement(int)void
;   [ 90] SC_PC_EnableRadioBreak(int)void
;   [ 91] SC_RadioBatch_Begin(void)void
;   [ 92] SC_SpeechRadio2(unsignedlong,*float)void
;   [ 93] SC_RadioBatch_End(void)void
;   [ 94] SC_MissionSave(*s_SC_MissionSave)void
;   [ 95] SC_Radio_Enable(unsignedlong)void
;   [ 96] SC_P_SetPos(unsignedlong,*c_Vector3)void

; Strings
; -------
;   [  20] "Player %d enabled"
;   [  60] "Player %d disabled"
;   [  88] "Message %d %d to unexisted player!"
;   [ 592] "MISSION COMPLETE"
;   [1428] "ini\players\poorvc.ini"
;   [1456] "ini\players\poorvc2.ini"
;   [1480] "ini\players\poorvc3.ini"
;   [1536] "ini\players\vcfighter2.ini"
;   [1568] "ini\players\vcfighter3.ini"
;   [1596] "ini\players\vcfighter4.ini"
;   [1656] "ini\players\vcfighter3.ini"
;   [1688] "ini\players\vcfighter2.ini"
;   [1720] "ini\players\vcfighter3.ini"
;   [1748] "ini\players\vcfighter4.ini"
;   [1808] "ini\players\vcuniform1.ini"
;   [1840] "ini\players\vcuniform2.ini"
;   [1868] "ini\players\vcuniform3.ini"
;   [1928] "ini\players\nvasoldier2.ini"
;   [1960] "ini\players\nvasoldier3.ini"
;   [1988] "ini\players\nvaofficer.ini"
;   [2016] "ini\players\default_aiviet.ini"
;   [2920] "FATAL! Claymore %s not found!!!!!!"
;   [3416] "GetMyGroup: TOO much players in group around!"
;   [3484] "VC %d %d couldnot find anyone to lead group %d"
;   [3568] "VC %d %d moved command over group"
;   [3928] "Duplicite objective added - %d"
;   [4000] "Duplicite objective added - %d"
;   [4236] "Level difficulty is %d"
;   [4768] "adding trap on pos %d"
;   [4852] "Plechovka"
;   [4864] "trap not found!!!"
;   [4888] "Konec dratu"
;   [4992] "Plechovka"
;   [5004] "trap not found!!!"
;   [5100] "removing trap %d"
;   [5436] "%d found on alarm spot %d by %d"
;   [5496] "point"
;   [5536] "point"
;   [5568] "point"
;   [7080] "ACTIVEPLACE#%d"
;   [7156] "WayPoint113"
;   [7168] "WayPoint#33"
;   [7600] "WayPoint113"
;   [8776] "grenadebedna"
;   [8792] "levels\LIK_Tunnels\data\Tunnels01\scripts\opena..."
;   [8852] "n_poklop_01"
;   [8864] "levels\LIK_Tunnels\data\Tunnels01\scripts\poklop.c"
;   [8916] "d_past_04_01"
;   [8932] "levels\LIK_Tunnels\data\Tunnels01\scripts\past.c"
;   [8984] "grenadebedna"
;   [9012] "n_poklop_01"
;   [9036] "granat_v_plechovce2#3"
;   [9312] "Levelphase changed to %d"
;   [9348] "Levelphase changed to %d"
;   [9444] "Levelphase changed to %d"
;   [9480] "Levelphase changed to %d"
;   [9696] "Saving game id %d"
;   [9724] "Saving game id %d"
;   [9788] "Saving game id %d"
;   [9816] "Saving game id %d"
;   [9880] "Saving game id %d"
;   [9908] "Saving game id %d"
;   [10000] "WayPoint53"
;   [10024] "WayPoint#9"
;   [10052] "WayPoint57"

; Code
; ----

_init:
  000: GADR     data[1410]           
  001: GCP      data[1570]            ; = 0.0f
  002: LCP      [sp+0]               
  003: DLD      [sp+4]               
  004: GCP      data[1571]            ; = 0.0f
  005: LCP      [sp+0]               
  006: PNT      4                    
  007: DLD      [sp+4]               
  008: GCP      data[1572]            ; = 0.0f
  009: LCP      [sp+0]               
  010: PNT      8                    
  011: DLD      [sp+4]               
  012: GCP      data[1573]            ; = 0.0f
  013: LCP      [sp+0]               
  014: PNT      12                   
  015: DLD      [sp+4]               
  016: GCP      data[1574]            ; = 0.0f
  017: LCP      [sp+0]               
  018: PNT      16                   
  019: DLD      [sp+4]               
  020: GCP      data[1575]            ; = 100
  021: LCP      [sp+0]               
  022: PNT      20                   
  023: DLD      [sp+4]               
  024: GCP      data[1576]            ; = 100
  025: LCP      [sp+0]               
  026: PNT      24                   
  027: DLD      [sp+4]               
  028: GCP      data[1577]            ; = 100
  029: LCP      [sp+0]               
  030: PNT      28                   
  031: DLD      [sp+4]               
  032: GCP      data[1578]            ; = 0.0f
  033: LCP      [sp+0]               
  034: PNT      32                   
  035: DLD      [sp+4]               
  036: GCP      data[1579]            ; = 0.0f
  037: LCP      [sp+0]               
  038: PNT      36                   
  039: DLD      [sp+4]               
  040: GCP      data[1580]            ; = 0.0f
  041: LCP      [sp+0]               
  042: PNT      40                   
  043: DLD      [sp+4]               
  044: GCP      data[1581]            ; = 0.0f
  045: LCP      [sp+0]               
  046: PNT      44                   
  047: DLD      [sp+4]               
  048: GCP      data[1582]            ; = 0.0f
  049: LCP      [sp+0]               
  050: PNT      48                   
  051: DLD      [sp+4]               
  052: GCP      data[1583]            ; = 100
  053: LCP      [sp+0]               
  054: PNT      52                   
  055: DLD      [sp+4]               
  056: GCP      data[1584]            ; = 100
  057: LCP      [sp+0]               
  058: PNT      56                   
  059: DLD      [sp+4]               
  060: GCP      data[1585]            ; = 100
  061: LCP      [sp+0]               
  062: PNT      60                   
  063: DLD      [sp+4]               
  064: GCP      data[1586]            ; = -1
  065: LCP      [sp+0]               
  066: PNT      64                   
  067: DLD      [sp+4]               
  068: GCP      data[1587]            ; = 0.0f
  069: LCP      [sp+0]               
  070: PNT      68                   
  071: DLD      [sp+4]               
  072: GCP      data[1588]            ; = 0.0f
  073: LCP      [sp+0]               
  074: PNT      72                   
  075: DLD      [sp+4]               
  076: GCP      data[1589]            ; = 0.0f
  077: LCP      [sp+0]               
  078: PNT      76                   
  079: DLD      [sp+4]               
  080: GCP      data[1590]            ; = 0.0f
  081: LCP      [sp+0]               
  082: PNT      80                   
  083: DLD      [sp+4]               
  084: GCP      data[1591]            ; = -1
  085: LCP      [sp+0]               
  086: PNT      84                   
  087: DLD      [sp+4]               
  088: GCP      data[1592]            ; = -1
  089: LCP      [sp+0]               
  090: PNT      88                   
  091: DLD      [sp+4]               
  092: GCP      data[1593]            ; = 100
  093: LCP      [sp+0]               
  094: PNT      92                   
  095: DLD      [sp+4]               
  096: GCP      data[1594]            ; = 45
  097: LCP      [sp+0]               
  098: PNT      96                   
  099: DLD      [sp+4]               
  100: GCP      data[1595]            ; = 100
  101: LCP      [sp+0]               
  102: PNT      100                  
  103: DLD      [sp+4]               
  104: GCP      data[1596]            ; = 1.0f
  105: LCP      [sp+0]               
  106: PNT      104                  
  107: DLD      [sp+4]               
  108: GCP      data[1597]            ; = 5.0f
  109: LCP      [sp+0]               
  110: PNT      108                  
  111: DLD      [sp+4]               
  112: GCP      data[1598]            ; = 0.0f
  113: LCP      [sp+0]               
  114: PNT      112                  
  115: DLD      [sp+4]               
  116: GCP      data[1599]            ; = 10
  117: LCP      [sp+0]               
  118: PNT      116                  
  119: DLD      [sp+4]               
  120: GCP      data[1600]            ; = 10
  121: LCP      [sp+0]               
  122: PNT      120                  
  123: DLD      [sp+4]               
  124: GCP      data[1601]            ; = 100
  125: LCP      [sp+0]               
  126: PNT      124                  
  127: DLD      [sp+4]               
  128: GCP      data[1602]            ; = 28
  129: LCP      [sp+0]               
  130: PNT      128                  
  131: DLD      [sp+4]               
  132: GCP      data[1603]            ; = 90
  133: LCP      [sp+0]               
  134: PNT      132                  
  135: DLD      [sp+4]               
  136: GCP      data[1604]            ; = 0.0f
  137: LCP      [sp+0]               
  138: PNT      136                  
  139: DLD      [sp+4]               
  140: GCP      data[1605]            ; = 10.0f
  141: LCP      [sp+0]               
  142: PNT      140                  
  143: DLD      [sp+4]               
  144: GCP      data[1606]            ; = 0.0f
  145: LCP      [sp+0]               
  146: PNT      144                  
  147: DLD      [sp+4]               
  148: GCP      data[1607]            ; = 0.0f
  149: LCP      [sp+0]               
  150: PNT      148                  
  151: DLD      [sp+4]               
  152: GCP      data[1608]            ; = 0.0f
  153: LCP      [sp+0]               
  154: PNT      152                  
  155: DLD      [sp+4]               
  156: GCP      data[1609]            ; = 100
  157: LCP      [sp+0]               
  158: PNT      156                  
  159: DLD      [sp+4]               
  160: GCP      data[1610]            ; = -1
  161: LCP      [sp+0]               
  162: PNT      160                  
  163: DLD      [sp+4]               
  164: GCP      data[1611]            ; = 0.0f
  165: LCP      [sp+0]               
  166: PNT      164                  
  167: DLD      [sp+4]               
  168: GCP      data[1612]            ; = 0.0f
  169: LCP      [sp+0]               
  170: PNT      168                  
  171: DLD      [sp+4]               
  172: GCP      data[1613]            ; = 0.0f
  173: LCP      [sp+0]               
  174: PNT      172                  
  175: DLD      [sp+4]               
  176: GCP      data[1614]            ; = 0.0f
  177: LCP      [sp+0]               
  178: PNT      176                  
  179: DLD      [sp+4]               
  180: GCP      data[1615]            ; = -1
  181: LCP      [sp+0]               
  182: PNT      180                  
  183: DLD      [sp+4]               
  184: GCP      data[1616]            ; = -1
  185: LCP      [sp+0]               
  186: PNT      184                  
  187: DLD      [sp+4]               
  188: GCP      data[1617]            ; = 100
  189: LCP      [sp+0]               
  190: PNT      188                  
  191: DLD      [sp+4]               
  192: GCP      data[1618]            ; = -1
  193: LCP      [sp+0]               
  194: PNT      192                  
  195: DLD      [sp+4]               
  196: GCP      data[1619]            ; = 0.0f
  197: LCP      [sp+0]               
  198: PNT      196                  
  199: DLD      [sp+4]               
  200: GCP      data[1620]            ; = 0.0f
  201: LCP      [sp+0]               
  202: PNT      200                  
  203: DLD      [sp+4]               
  204: GCP      data[1621]            ; = 0.0f
  205: LCP      [sp+0]               
  206: PNT      204                  
  207: DLD      [sp+4]               
  208: GCP      data[1622]            ; = 0.0f
  209: LCP      [sp+0]               
  210: PNT      208                  
  211: DLD      [sp+4]               
  212: GCP      data[1623]            ; = -1
  213: LCP      [sp+0]               
  214: PNT      212                  
  215: DLD      [sp+4]               
  216: GCP      data[1624]            ; = -1
  217: LCP      [sp+0]               
  218: PNT      216                  
  219: DLD      [sp+4]               
  220: GCP      data[1625]            ; = 100
  221: LCP      [sp+0]               
  222: PNT      220                  
  223: DLD      [sp+4]               
  224: GCP      data[1626]            ; = -1
  225: LCP      [sp+0]               
  226: PNT      224                  
  227: DLD      [sp+4]               
  228: GCP      data[1627]            ; = 0.0f
  229: LCP      [sp+0]               
  230: PNT      228                  
  231: DLD      [sp+4]               
  232: GCP      data[1628]            ; = 0.0f
  233: LCP      [sp+0]               
  234: PNT      232                  
  235: DLD      [sp+4]               
  236: GCP      data[1629]            ; = 0.0f
  237: LCP      [sp+0]               
  238: PNT      236                  
  239: DLD      [sp+4]               
  240: GCP      data[1630]            ; = 0.0f
  241: LCP      [sp+0]               
  242: PNT      240                  
  243: DLD      [sp+4]               
  244: GCP      data[1631]            ; = -1
  245: LCP      [sp+0]               
  246: PNT      244                  
  247: DLD      [sp+4]               
  248: GCP      data[1632]            ; = -1
  249: LCP      [sp+0]               
  250: PNT      248                  
  251: DLD      [sp+4]               
  252: GCP      data[1633]            ; = 100
  253: LCP      [sp+0]               
  254: PNT      252                  
  255: DLD      [sp+4]               
  256: SSP      1                    
  257: GADR     data[1732]           
  258: GCP      data[1740]            ; = 0.0f
  259: LCP      [sp+0]               
  260: DLD      [sp+4]               
  261: GCP      data[1741]            ; = 0.0f
  262: LCP      [sp+0]               
  263: PNT      4                    
  264: DLD      [sp+4]               
  265: GCP      data[1742]            ; = 0.0f
  266: LCP      [sp+0]               
  267: PNT      8                    
  268: DLD      [sp+4]               
  269: GCP      data[1743]            ; = 0.0f
  270: LCP      [sp+0]               
  271: PNT      12                   
  272: DLD      [sp+4]               
  273: GCP      data[1744]            ; = 0.0f
  274: LCP      [sp+0]               
  275: PNT      16                   
  276: DLD      [sp+4]               
  277: GCP      data[1745]            ; = 0.0f
  278: LCP      [sp+0]               
  279: PNT      20                   
  280: DLD      [sp+4]               
  281: GCP      data[1746]            ; = 0.0f
  282: LCP      [sp+0]               
  283: PNT      24                   
  284: DLD      [sp+4]               
  285: GCP      data[1747]            ; = 0.0f
  286: LCP      [sp+0]               
  287: PNT      28                   
  288: DLD      [sp+4]               
  289: SSP      1                    
  290: RET      0                    
func_0291:
  291: ASP      1                    
  292: ASP      1                    
  293: LCP      [sp-4]               
  294: ASP      1                    
  295: XCALL    $frnd(float)float     ; args=1
  296: LLD      [sp+1]               
  297: SSP      1                    
  298: LADR     [sp+0]               
  299: ASGN                          
  300: SSP      1                    
  301: LCP      [sp+0]               
  302: GCP      data[0]               ; = 0.0f
  303: FLES                          
  304: JZ       label_0310           
  305: LCP      [sp+0]               
  306: FNEG                          
  307: LADR     [sp+0]               
  308: ASGN                          
  309: SSP      1                    
label_0310:
  310: LCP      [sp+0]               
  311: LLD      [sp-3]               
  312: RET      1                    
  313: LCP      [sp-3]               
  314: GCP      data[1]               ; = 1
  315: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  316: SSP      2                    
  317: LCP      [sp-3]               
  318: GCP      data[2]               ; = 1
  319: XCALL    $SC_P_Ai_EnableShooting(unsignedlong,int)void ; args=2
  320: SSP      2                    
  321: LCP      [sp-3]               
  322: GCP      data[3]               ; = 1
  323: XCALL    $SC_P_Ai_EnableSituationUpdate(unsignedlong,int)void ; args=2
  324: SSP      2                    
  325: GCP      data[4]               ; = 3
  326: GADR     data[5]  ; "Player %d enabled"
  327: LCP      [sp-3]               
  328: GCP      data[10]              ; = 3
  329: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  330: SSP      3                    
  331: RET      0                    
  332: LCP      [sp-3]               
  333: GCP      data[11]              ; = 0.0f
  334: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  335: SSP      2                    
  336: LCP      [sp-3]               
  337: GCP      data[12]              ; = 0.0f
  338: XCALL    $SC_P_Ai_EnableShooting(unsignedlong,int)void ; args=2
  339: SSP      2                    
  340: LCP      [sp-3]               
  341: GCP      data[13]              ; = 0.0f
  342: XCALL    $SC_P_Ai_EnableSituationUpdate(unsignedlong,int)void ; args=2
  343: SSP      2                    
  344: LCP      [sp-3]               
  345: XCALL    $SC_P_Ai_Stop(unsignedlong)void ; args=1
  346: SSP      1                    
  347: GCP      data[14]              ; = 3
  348: GADR     data[15]  ; "Player %d disabled"
  349: LCP      [sp-3]               
  350: GCP      data[20]              ; = 3
  351: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  352: SSP      3                    
  353: RET      0                    
func_0354:
  354: LCP      [sp-5]               
  355: JZ       label_0357           
  356: JMP      label_0365           
label_0357:
  357: GCP      data[21]              ; = 3
  358: GADR     data[22]  ; "Message %d %d to unexisted player!"
  359: LCP      [sp-4]               
  360: LCP      [sp-3]               
  361: GCP      data[31]              ; = 4
  362: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  363: SSP      4                    
  364: RET      0                    
label_0365:
  365: LCP      [sp-5]               
  366: LCP      [sp-4]               
  367: LCP      [sp-3]               
  368: XCALL    $SC_P_ScriptMessage(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  369: SSP      3                    
  370: RET      0                    
func_0371:
  371: ASP      1                    
  372: ASP      1                    
  373: GCP      data[32]              ; = 1
  374: LCP      [sp-5]               
  375: LCP      [sp-4]               
  376: ASP      1                    
  377: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  378: LLD      [sp+1]               
  379: SSP      3                    
  380: ASP      1                    
  381: XCALL    $SC_P_Ai_GetSureEnemies(unsignedlong)unsignedlong ; args=1
  382: LLD      [sp+0]               
  383: SSP      1                    
  384: JZ       label_0388           
  385: GCP      data[33]              ; = 1
  386: LLD      [sp-3]               
  387: RET      0                    
label_0388:
  388: ASP      1                    
  389: ASP      1                    
  390: GCP      data[34]              ; = 1
  391: LCP      [sp-5]               
  392: LCP      [sp-4]               
  393: ASP      1                    
  394: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  395: LLD      [sp+1]               
  396: SSP      3                    
  397: ASP      1                    
  398: XCALL    $SC_P_Ai_GetDanger(unsignedlong)float ; args=1
  399: LLD      [sp+0]               
  400: SSP      1                    
  401: GCP      data[35]              ; = 0.5f
  402: FGRE                          
  403: JZ       label_0407           
  404: GCP      data[36]              ; = 1
  405: LLD      [sp-3]               
  406: RET      0                    
label_0407:
  407: GCP      data[37]              ; = 0.0f
  408: LLD      [sp-3]               
  409: RET      0                    
  410: ASP      1                    
  411: LCP      [sp-4]               
  412: ASP      1                    
  413: XCALL    $SC_P_Ai_GetSureEnemies(unsignedlong)unsignedlong ; args=1
  414: LLD      [sp+0]               
  415: SSP      1                    
  416: JZ       label_0420           
  417: GCP      data[38]              ; = 1
  418: LLD      [sp-3]               
  419: RET      0                    
label_0420:
  420: ASP      1                    
  421: LCP      [sp-4]               
  422: ASP      1                    
  423: XCALL    $SC_P_Ai_GetDanger(unsignedlong)float ; args=1
  424: LLD      [sp+0]               
  425: SSP      1                    
  426: GCP      data[39]              ; = 0.5f
  427: FGRE                          
  428: JZ       label_0432           
  429: GCP      data[40]              ; = 1
  430: LLD      [sp-3]               
  431: RET      0                    
label_0432:
  432: GCP      data[41]              ; = 0.0f
  433: LLD      [sp-3]               
  434: RET      0                    
  435: ASP      32                   
  436: LADR     [sp+0]               
  437: GCP      data[42]              ; = 128
  438: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  439: SSP      2                    
  440: LCP      [sp-4]               
  441: LADR     [sp+0]               
  442: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  443: SSP      2                    
  444: LCP      [sp-3]               
  445: LADR     [sp+0]               
  446: PNT      76                   
  447: ASGN                          
  448: SSP      1                    
  449: LCP      [sp-4]               
  450: LADR     [sp+0]               
  451: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  452: SSP      2                    
  453: RET      32                   
  454: ASP      32                   
  455: LADR     [sp+0]               
  456: GCP      data[43]              ; = 128
  457: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  458: SSP      2                    
  459: LCP      [sp-4]               
  460: LADR     [sp+0]               
  461: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  462: SSP      2                    
  463: LCP      [sp-3]               
  464: LADR     [sp+0]               
  465: PNT      44                   
  466: ASGN                          
  467: SSP      1                    
  468: LCP      [sp-4]               
  469: LADR     [sp+0]               
  470: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  471: SSP      2                    
  472: RET      32                   
  473: ASP      32                   
  474: LADR     [sp+0]               
  475: GCP      data[44]              ; = 128
  476: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  477: SSP      2                    
  478: LCP      [sp-4]               
  479: LADR     [sp+0]               
  480: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  481: SSP      2                    
  482: LADR     [sp+0]               
  483: PNT      20                   
  484: DCP      4                    
  485: LCP      [sp-3]               
  486: FMUL                          
  487: LADR     [sp+0]               
  488: PNT      20                   
  489: ASGN                          
  490: SSP      1                    
  491: LCP      [sp-4]               
  492: LADR     [sp+0]               
  493: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  494: SSP      2                    
  495: RET      32                   
  496: ASP      32                   
  497: LADR     [sp+0]               
  498: GCP      data[45]              ; = 128
  499: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  500: SSP      2                    
  501: LCP      [sp-4]               
  502: LADR     [sp+0]               
  503: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  504: SSP      2                    
  505: LADR     [sp+0]               
  506: PNT      72                   
  507: DCP      4                    
  508: LCP      [sp-3]               
  509: FMUL                          
  510: LADR     [sp+0]               
  511: PNT      72                   
  512: ASGN                          
  513: SSP      1                    
  514: LCP      [sp-4]               
  515: LADR     [sp+0]               
  516: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  517: SSP      2                    
  518: RET      32                   
  519: ASP      32                   
  520: LADR     [sp+0]               
  521: GCP      data[46]              ; = 128
  522: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  523: SSP      2                    
  524: LCP      [sp-4]               
  525: LADR     [sp+0]               
  526: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  527: SSP      2                    
  528: LCP      [sp-3]               
  529: JZ       label_0536           
  530: GCP      data[47]              ; = 5.0f
  531: LADR     [sp+0]               
  532: PNT      64                   
  533: ASGN                          
  534: SSP      1                    
  535: JMP      label_0541           
label_0536:
  536: GCP      data[48]              ; = 1000.0f
  537: LADR     [sp+0]               
  538: PNT      64                   
  539: ASGN                          
  540: SSP      1                    
label_0541:
  541: LCP      [sp-4]               
  542: LADR     [sp+0]               
  543: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  544: SSP      2                    
  545: RET      32                   
  546: ASP      32                   
  547: LADR     [sp+0]               
  548: GCP      data[49]              ; = 128
  549: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  550: SSP      2                    
  551: LCP      [sp-4]               
  552: LADR     [sp+0]               
  553: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  554: SSP      2                    
  555: LCP      [sp-3]               
  556: LADR     [sp+0]               
  557: PNT      100                  
  558: ASGN                          
  559: SSP      1                    
  560: LCP      [sp-4]               
  561: LADR     [sp+0]               
  562: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  563: SSP      2                    
  564: RET      32                   
  565: ASP      1                    
  566: GCP      data[50]              ; = 200
  567: ASP      1                    
  568: XCALL    $SC_ggi(unsignedlong)int ; args=1
  569: LLD      [sp+0]               
  570: SSP      1                    
  571: LLD      [sp-3]               
  572: RET      0                    
  573: ASP      1                    
  574: GCP      data[51]              ; = 7
  575: ASP      1                    
  576: XCALL    $SC_ggi(unsignedlong)int ; args=1
  577: LLD      [sp+0]               
  578: SSP      1                    
  579: LLD      [sp-3]               
  580: RET      0                    
  581: ASP      5                    
  582: LCP      [sp-4]               
  583: LADR     [sp+0]               
  584: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  585: SSP      2                    
  586: LADR     [sp+0]               
  587: DCP      4                    
  588: LLD      [sp-3]               
  589: RET      5                    
  590: ASP      32                   
  591: LADR     [sp+0]               
  592: GCP      data[52]              ; = 128
  593: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  594: SSP      2                    
  595: LCP      [sp-4]               
  596: LADR     [sp+0]               
  597: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  598: SSP      2                    
  599: LCP      [sp-3]               
  600: LADR     [sp+0]               
  601: ASGN                          
  602: SSP      1                    
  603: LCP      [sp-4]               
  604: LADR     [sp+0]               
  605: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  606: SSP      2                    
  607: RET      32                   
  608: ASP      1                    
  609: GCP      data[53]              ; = 101
  610: ASP      1                    
  611: XCALL    $SC_ggi(unsignedlong)int ; args=1
  612: LLD      [sp+0]               
  613: SSP      1                    
  614: LADR     [sp-3]               
  615: DADR     40                   
  616: ASGN                          
  617: SSP      1                    
  618: LADR     [sp-3]               
  619: DADR     40                   
  620: DCP      4                    
  621: JZ       label_0623           
  622: JMP      label_0628           
label_0623:
  623: GCP      data[54]              ; = 29
  624: LADR     [sp-3]               
  625: DADR     40                   
  626: ASGN                          
  627: SSP      1                    
label_0628:
  628: LADR     [sp-3]               
  629: DADR     40                   
  630: DCP      4                    
  631: GCP      data[55]              ; = 255
  632: EQU                           
  633: JZ       label_0639           
  634: GCP      data[56]              ; = 0.0f
  635: LADR     [sp-3]               
  636: DADR     40                   
  637: ASGN                          
  638: SSP      1                    
label_0639:
  639: ASP      1                    
  640: GCP      data[57]              ; = 102
  641: ASP      1                    
  642: XCALL    $SC_ggi(unsignedlong)int ; args=1
  643: LLD      [sp+0]               
  644: SSP      1                    
  645: LADR     [sp-3]               
  646: DADR     44                   
  647: ASGN                          
  648: SSP      1                    
  649: LADR     [sp-3]               
  650: DADR     44                   
  651: DCP      4                    
  652: JZ       label_0654           
  653: JMP      label_0659           
label_0654:
  654: GCP      data[58]              ; = 7
  655: LADR     [sp-3]               
  656: DADR     44                   
  657: ASGN                          
  658: SSP      1                    
label_0659:
  659: LADR     [sp-3]               
  660: DADR     44                   
  661: DCP      4                    
  662: GCP      data[59]              ; = 255
  663: EQU                           
  664: JZ       label_0670           
  665: GCP      data[60]              ; = 0.0f
  666: LADR     [sp-3]               
  667: DADR     44                   
  668: ASGN                          
  669: SSP      1                    
label_0670:
  670: ASP      1                    
  671: GCP      data[61]              ; = 103
  672: ASP      1                    
  673: XCALL    $SC_ggi(unsignedlong)int ; args=1
  674: LLD      [sp+0]               
  675: SSP      1                    
  676: LADR     [sp-3]               
  677: DADR     48                   
  678: ASGN                          
  679: SSP      1                    
  680: LADR     [sp-3]               
  681: DADR     48                   
  682: DCP      4                    
  683: JZ       label_0685           
  684: JMP      label_0720           
label_0685:
  685: ASP      1                    
  686: GCP      data[62]              ; = 200
  687: ASP      1                    
  688: XCALL    $SC_ggi(unsignedlong)int ; args=1
  689: LLD      [sp+0]               
  690: SSP      1                    
  691: GCP      data[63]              ; = 12
  692: EQU                           
  693: JZ       label_0700           
  694: GCP      data[64]              ; = 23
  695: LADR     [sp-3]               
  696: DADR     48                   
  697: ASGN                          
  698: SSP      1                    
  699: JMP      label_0720           
label_0700:
  700: ASP      1                    
  701: GCP      data[65]              ; = 200
  702: ASP      1                    
  703: XCALL    $SC_ggi(unsignedlong)int ; args=1
  704: LLD      [sp+0]               
  705: SSP      1                    
  706: GCP      data[66]              ; = 12
  707: LES                           
  708: JZ       label_0715           
  709: GCP      data[67]              ; = 25
  710: LADR     [sp-3]               
  711: DADR     48                   
  712: ASGN                          
  713: SSP      1                    
  714: JMP      label_0720           
label_0715:
  715: GCP      data[68]              ; = 1
  716: LADR     [sp-3]               
  717: DADR     48                   
  718: ASGN                          
  719: SSP      1                    
label_0720:
  720: LADR     [sp-3]               
  721: DADR     48                   
  722: DCP      4                    
  723: GCP      data[69]              ; = 255
  724: EQU                           
  725: JZ       label_0731           
  726: GCP      data[70]              ; = 0.0f
  727: LADR     [sp-3]               
  728: DADR     48                   
  729: ASGN                          
  730: SSP      1                    
label_0731:
  731: ASP      1                    
  732: GCP      data[71]              ; = 104
  733: ASP      1                    
  734: XCALL    $SC_ggi(unsignedlong)int ; args=1
  735: LLD      [sp+0]               
  736: SSP      1                    
  737: LADR     [sp-3]               
  738: DADR     52                   
  739: ASGN                          
  740: SSP      1                    
  741: LADR     [sp-3]               
  742: DADR     52                   
  743: DCP      4                    
  744: GCP      data[72]              ; = 255
  745: EQU                           
  746: JZ       label_0752           
  747: GCP      data[73]              ; = 0.0f
  748: LADR     [sp-3]               
  749: DADR     52                   
  750: ASGN                          
  751: SSP      1                    
label_0752:
  752: ASP      1                    
  753: GCP      data[74]              ; = 105
  754: ASP      1                    
  755: XCALL    $SC_ggi(unsignedlong)int ; args=1
  756: LLD      [sp+0]               
  757: SSP      1                    
  758: LADR     [sp-3]               
  759: DADR     56                   
  760: ASGN                          
  761: SSP      1                    
  762: LADR     [sp-3]               
  763: DADR     56                   
  764: DCP      4                    
  765: JZ       label_0767           
  766: JMP      label_0772           
label_0767:
  767: GCP      data[75]              ; = 59
  768: LADR     [sp-3]               
  769: DADR     56                   
  770: ASGN                          
  771: SSP      1                    
label_0772:
  772: LADR     [sp-3]               
  773: DADR     56                   
  774: DCP      4                    
  775: GCP      data[76]              ; = 255
  776: EQU                           
  777: JZ       label_0783           
  778: GCP      data[77]              ; = 0.0f
  779: LADR     [sp-3]               
  780: DADR     56                   
  781: ASGN                          
  782: SSP      1                    
label_0783:
  783: ASP      1                    
  784: GCP      data[78]              ; = 106
  785: ASP      1                    
  786: XCALL    $SC_ggi(unsignedlong)int ; args=1
  787: LLD      [sp+0]               
  788: SSP      1                    
  789: LADR     [sp-3]               
  790: DADR     60                   
  791: ASGN                          
  792: SSP      1                    
  793: LADR     [sp-3]               
  794: DADR     60                   
  795: DCP      4                    
  796: GCP      data[79]              ; = 255
  797: EQU                           
  798: JZ       label_0804           
  799: GCP      data[80]              ; = 0.0f
  800: LADR     [sp-3]               
  801: DADR     60                   
  802: ASGN                          
  803: SSP      1                    
label_0804:
  804: ASP      1                    
  805: GCP      data[81]              ; = 107
  806: ASP      1                    
  807: XCALL    $SC_ggi(unsignedlong)int ; args=1
  808: LLD      [sp+0]               
  809: SSP      1                    
  810: LADR     [sp-3]               
  811: DADR     64                   
  812: ASGN                          
  813: SSP      1                    
  814: LADR     [sp-3]               
  815: DADR     64                   
  816: DCP      4                    
  817: GCP      data[82]              ; = 255
  818: EQU                           
  819: JZ       label_0825           
  820: GCP      data[83]              ; = 0.0f
  821: LADR     [sp-3]               
  822: DADR     64                   
  823: ASGN                          
  824: SSP      1                    
label_0825:
  825: ASP      1                    
  826: GCP      data[84]              ; = 108
  827: ASP      1                    
  828: XCALL    $SC_ggi(unsignedlong)int ; args=1
  829: LLD      [sp+0]               
  830: SSP      1                    
  831: LADR     [sp-3]               
  832: DADR     68                   
  833: ASGN                          
  834: SSP      1                    
  835: LADR     [sp-3]               
  836: DADR     68                   
  837: DCP      4                    
  838: JZ       label_0840           
  839: JMP      label_0845           
label_0840:
  840: GCP      data[85]              ; = 63
  841: LADR     [sp-3]               
  842: DADR     68                   
  843: ASGN                          
  844: SSP      1                    
label_0845:
  845: LADR     [sp-3]               
  846: DADR     68                   
  847: DCP      4                    
  848: GCP      data[86]              ; = 255
  849: EQU                           
  850: JZ       label_0856           
  851: GCP      data[87]              ; = 0.0f
  852: LADR     [sp-3]               
  853: DADR     68                   
  854: ASGN                          
  855: SSP      1                    
label_0856:
  856: ASP      1                    
  857: GCP      data[88]              ; = 109
  858: ASP      1                    
  859: XCALL    $SC_ggi(unsignedlong)int ; args=1
  860: LLD      [sp+0]               
  861: SSP      1                    
  862: LADR     [sp-3]               
  863: DADR     72                   
  864: ASGN                          
  865: SSP      1                    
  866: LADR     [sp-3]               
  867: DADR     72                   
  868: DCP      4                    
  869: GCP      data[89]              ; = 255
  870: EQU                           
  871: JZ       label_0877           
  872: GCP      data[90]              ; = 0.0f
  873: LADR     [sp-3]               
  874: DADR     72                   
  875: ASGN                          
  876: SSP      1                    
label_0877:
  877: GCP      data[91]              ; = 58
  878: LADR     [sp-3]               
  879: DADR     76                   
  880: ASGN                          
  881: SSP      1                    
  882: RET      0                    
func_0883:
  883: ASP      39                   
  884: ASP      1                    
  885: ASP      1                    
  886: ASP      1                    
  887: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  888: LLD      [sp+40]              
  889: LADR     [sp+0]               
  890: ASP      1                    
  891: XCALL    $SC_P_GetWeapons(unsignedlong,*s_SC_P_Create)int ; args=2
  892: LLD      [sp+39]              
  893: SSP      2                    
  894: SSP      1                    
  895: LADR     [sp+0]               
  896: PNT      40                   
  897: DCP      4                    
  898: JZ       label_0906           
  899: GCP      data[92]              ; = 101
  900: LADR     [sp+0]               
  901: PNT      40                   
  902: DCP      4                    
  903: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  904: SSP      2                    
  905: JMP      label_0910           
label_0906:
  906: GCP      data[93]              ; = 101
  907: GCP      data[94]              ; = 255
  908: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  909: SSP      2                    
label_0910:
  910: LADR     [sp+0]               
  911: PNT      44                   
  912: DCP      4                    
  913: JZ       label_0921           
  914: GCP      data[95]              ; = 102
  915: LADR     [sp+0]               
  916: PNT      44                   
  917: DCP      4                    
  918: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  919: SSP      2                    
  920: JMP      label_0925           
label_0921:
  921: GCP      data[96]              ; = 102
  922: GCP      data[97]              ; = 255
  923: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  924: SSP      2                    
label_0925:
  925: LADR     [sp+0]               
  926: PNT      48                   
  927: DCP      4                    
  928: JZ       label_0936           
  929: GCP      data[98]              ; = 103
  930: LADR     [sp+0]               
  931: PNT      48                   
  932: DCP      4                    
  933: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  934: SSP      2                    
  935: JMP      label_0940           
label_0936:
  936: GCP      data[99]              ; = 103
  937: GCP      data[100]             ; = 255
  938: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  939: SSP      2                    
label_0940:
  940: LADR     [sp+0]               
  941: PNT      52                   
  942: DCP      4                    
  943: JZ       label_0951           
  944: GCP      data[101]             ; = 104
  945: LADR     [sp+0]               
  946: PNT      52                   
  947: DCP      4                    
  948: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  949: SSP      2                    
  950: JMP      label_0955           
label_0951:
  951: GCP      data[102]             ; = 104
  952: GCP      data[103]             ; = 255
  953: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  954: SSP      2                    
label_0955:
  955: LADR     [sp+0]               
  956: PNT      56                   
  957: DCP      4                    
  958: JZ       label_0966           
  959: GCP      data[104]             ; = 105
  960: LADR     [sp+0]               
  961: PNT      56                   
  962: DCP      4                    
  963: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  964: SSP      2                    
  965: JMP      label_0970           
label_0966:
  966: GCP      data[105]             ; = 105
  967: GCP      data[106]             ; = 255
  968: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  969: SSP      2                    
label_0970:
  970: LADR     [sp+0]               
  971: PNT      60                   
  972: DCP      4                    
  973: JZ       label_0981           
  974: GCP      data[107]             ; = 106
  975: LADR     [sp+0]               
  976: PNT      60                   
  977: DCP      4                    
  978: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  979: SSP      2                    
  980: JMP      label_0985           
label_0981:
  981: GCP      data[108]             ; = 106
  982: GCP      data[109]             ; = 255
  983: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  984: SSP      2                    
label_0985:
  985: LADR     [sp+0]               
  986: PNT      64                   
  987: DCP      4                    
  988: JZ       label_0996           
  989: GCP      data[110]             ; = 107
  990: LADR     [sp+0]               
  991: PNT      64                   
  992: DCP      4                    
  993: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  994: SSP      2                    
  995: JMP      label_1000           
label_0996:
  996: GCP      data[111]             ; = 107
  997: GCP      data[112]             ; = 255
  998: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  999: SSP      2                    
label_1000:
  1000: LADR     [sp+0]               
  1001: PNT      68                   
  1002: DCP      4                    
  1003: JZ       label_1011           
  1004: GCP      data[113]             ; = 108
  1005: LADR     [sp+0]               
  1006: PNT      68                   
  1007: DCP      4                    
  1008: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1009: SSP      2                    
  1010: JMP      label_1015           
label_1011:
  1011: GCP      data[114]             ; = 108
  1012: GCP      data[115]             ; = 255
  1013: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1014: SSP      2                    
label_1015:
  1015: LADR     [sp+0]               
  1016: PNT      72                   
  1017: DCP      4                    
  1018: JZ       label_1026           
  1019: GCP      data[116]             ; = 109
  1020: LADR     [sp+0]               
  1021: PNT      72                   
  1022: DCP      4                    
  1023: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1024: SSP      2                    
  1025: JMP      label_1030           
label_1026:
  1026: GCP      data[117]             ; = 109
  1027: GCP      data[118]             ; = 255
  1028: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1029: SSP      2                    
label_1030:
  1030: LADR     [sp+0]               
  1031: PNT      76                   
  1032: DCP      4                    
  1033: JZ       label_1041           
  1034: GCP      data[119]             ; = 110
  1035: LADR     [sp+0]               
  1036: PNT      76                   
  1037: DCP      4                    
  1038: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1039: SSP      2                    
  1040: JMP      label_1045           
label_1041:
  1041: GCP      data[120]             ; = 110
  1042: GCP      data[121]             ; = 255
  1043: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1044: SSP      2                    
label_1045:
  1045: RET      39                   
  1046: ASP      1                    
  1047: ASP      1                    
  1048: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  1049: LLD      [sp+0]               
  1050: GCP      data[122]             ; = 95
  1051: XCALL    $SC_P_ReadHealthFromGlobalVar(unsignedlong,unsignedlong)void ; args=2
  1052: SSP      2                    
  1053: RET      0                    
func_1054:
  1054: ASP      1                    
  1055: ASP      1                    
  1056: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  1057: LLD      [sp+0]               
  1058: GCP      data[123]             ; = 95
  1059: XCALL    $SC_P_WriteHealthToGlobalVar(unsignedlong,unsignedlong)void ; args=2
  1060: SSP      2                    
  1061: RET      0                    
  1062: ASP      1                    
  1063: ASP      1                    
  1064: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  1065: LLD      [sp+0]               
  1066: GCP      data[124]             ; = 60
  1067: GCP      data[125]             ; = 89
  1068: XCALL    $SC_P_ReadAmmoFromGlobalVar(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  1069: SSP      3                    
  1070: ASP      1                    
  1071: GCP      data[126]             ; = 90
  1072: ASP      1                    
  1073: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1074: LLD      [sp+0]               
  1075: SSP      1                    
  1076: JZ       label_1090           
  1077: ASP      1                    
  1078: ASP      1                    
  1079: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  1080: LLD      [sp+0]               
  1081: GCP      data[127]             ; = 2
  1082: ASP      1                    
  1083: GCP      data[128]             ; = 90
  1084: ASP      1                    
  1085: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1086: LLD      [sp+2]               
  1087: SSP      1                    
  1088: XCALL    $SC_P_SetAmmoInWeap(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  1089: SSP      3                    
label_1090:
  1090: ASP      1                    
  1091: GCP      data[129]             ; = 91
  1092: ASP      1                    
  1093: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1094: LLD      [sp+0]               
  1095: SSP      1                    
  1096: JZ       label_1110           
  1097: ASP      1                    
  1098: ASP      1                    
  1099: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  1100: LLD      [sp+0]               
  1101: GCP      data[130]             ; = 1
  1102: ASP      1                    
  1103: GCP      data[131]             ; = 91
  1104: ASP      1                    
  1105: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1106: LLD      [sp+2]               
  1107: SSP      1                    
  1108: XCALL    $SC_P_SetAmmoInWeap(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  1109: SSP      3                    
label_1110:
  1110: RET      0                    
func_1111:
  1111: ASP      1                    
  1112: ASP      1                    
  1113: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  1114: LLD      [sp+0]               
  1115: GCP      data[132]             ; = 60
  1116: GCP      data[133]             ; = 89
  1117: XCALL    $SC_P_WriteAmmoToGlobalVar(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  1118: SSP      3                    
  1119: GCP      data[134]             ; = 90
  1120: ASP      1                    
  1121: ASP      1                    
  1122: ASP      1                    
  1123: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  1124: LLD      [sp+2]               
  1125: GCP      data[135]             ; = 2
  1126: ASP      1                    
  1127: XCALL    $SC_P_GetAmmoInWeap(unsignedlong,unsignedlong)unsignedlong ; args=2
  1128: LLD      [sp+1]               
  1129: SSP      2                    
  1130: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1131: SSP      2                    
  1132: GCP      data[136]             ; = 91
  1133: ASP      1                    
  1134: ASP      1                    
  1135: ASP      1                    
  1136: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  1137: LLD      [sp+2]               
  1138: GCP      data[137]             ; = 1
  1139: ASP      1                    
  1140: XCALL    $SC_P_GetAmmoInWeap(unsignedlong,unsignedlong)unsignedlong ; args=2
  1141: LLD      [sp+1]               
  1142: SSP      2                    
  1143: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1144: SSP      2                    
  1145: RET      0                    
func_1146:
  1146: ASP      10                   
  1147: ASP      1                    
  1148: LADR     [sp+0]               
  1149: XCALL    $SC_PC_GetIntel(*s_SC_P_intel)void ; args=1
  1150: SSP      1                    
  1151: GCP      data[138]             ; = 0.0f
  1152: LADR     [sp+10]              
  1153: ASGN                          
  1154: SSP      1                    
label_1155:
  1155: LCP      [sp+10]              
  1156: GCP      data[139]             ; = 10
  1157: LES                           
  1158: JZ       label_1179           
  1159: GCP      data[140]             ; = 50
  1160: LCP      [sp+10]              
  1161: ADD                           
  1162: LADR     [sp+0]               
  1163: LCP      [sp+10]              
  1164: GCP      data[141]             ; = 4
  1165: MUL                           
  1166: ADD                           
  1167: DCP      4                    
  1168: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1169: SSP      2                    
  1170: LCP      [sp+10]              
  1171: LCP      [sp+10]              
  1172: GCP      data[142]             ; = 1
  1173: ADD                           
  1174: LADR     [sp+10]              
  1175: ASGN                          
  1176: SSP      1                    
  1177: SSP      1                    
  1178: JMP      label_1155           
label_1179:
  1179: RET      11                   
  1180: ASP      10                   
  1181: ASP      1                    
  1182: GCP      data[143]             ; = 0.0f
  1183: LADR     [sp+10]              
  1184: ASGN                          
  1185: SSP      1                    
label_1186:
  1186: LCP      [sp+10]              
  1187: GCP      data[144]             ; = 10
  1188: LES                           
  1189: JZ       label_1214           
  1190: ASP      1                    
  1191: GCP      data[145]             ; = 50
  1192: LCP      [sp+10]              
  1193: ADD                           
  1194: ASP      1                    
  1195: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1196: LLD      [sp+11]              
  1197: SSP      1                    
  1198: LADR     [sp+0]               
  1199: LCP      [sp+10]              
  1200: GCP      data[146]             ; = 4
  1201: MUL                           
  1202: ADD                           
  1203: ASGN                          
  1204: SSP      1                    
  1205: LCP      [sp+10]              
  1206: LCP      [sp+10]              
  1207: GCP      data[147]             ; = 1
  1208: ADD                           
  1209: LADR     [sp+10]              
  1210: ASGN                          
  1211: SSP      1                    
  1212: SSP      1                    
  1213: JMP      label_1186           
label_1214:
  1214: LADR     [sp+0]               
  1215: XCALL    $SC_PC_SetIntel(*s_SC_P_intel)void ; args=1
  1216: SSP      1                    
  1217: RET      11                   
  1218: CALL     func_0883            
  1219: CALL     func_1111            
  1220: CALL     func_1054            
  1221: XCALL    $SC_MissionCompleted(void)void ; args=0
  1222: RET      0                    
func_1223:
  1223: CALL     func_1146            
  1224: CALL     func_0883            
  1225: CALL     func_1111            
  1226: CALL     func_1054            
  1227: GADR     data[148]  ; "MISSION COMPLETE"
  1228: GCP      data[153]             ; = 1
  1229: XCALL    $SC_Osi(*char,...)void ; args=4294967295
  1230: SSP      1                    
  1231: XCALL    $SC_MissionDone(void)void ; args=0
  1232: RET      0                    
  1233: LADR     [sp-3]               
  1234: GCP      data[154]             ; = 1
  1235: GCP      data[155]             ; = 6.0f
  1236: XCALL    $SC_ShowHelp(*unsignedlong,unsignedlong,float)void ; args=3
  1237: SSP      3                    
  1238: RET      0                    
  1239: ASP      2                    
  1240: LCP      [sp-4]               
  1241: LADR     [sp+0]               
  1242: GCP      data[156]             ; = 0.0f
  1243: ADD                           
  1244: ASGN                          
  1245: SSP      1                    
  1246: LCP      [sp-3]               
  1247: LADR     [sp+0]               
  1248: GCP      data[157]             ; = 4
  1249: ADD                           
  1250: ASGN                          
  1251: SSP      1                    
  1252: LADR     [sp+0]               
  1253: GCP      data[158]             ; = 2
  1254: GCP      data[159]             ; = 12.0f
  1255: XCALL    $SC_ShowHelp(*unsignedlong,unsignedlong,float)void ; args=3
  1256: SSP      3                    
  1257: RET      2                    
  1258: ASP      3                    
  1259: LCP      [sp-5]               
  1260: LADR     [sp+0]               
  1261: GCP      data[160]             ; = 0.0f
  1262: ADD                           
  1263: ASGN                          
  1264: SSP      1                    
  1265: LCP      [sp-4]               
  1266: LADR     [sp+0]               
  1267: GCP      data[161]             ; = 4
  1268: ADD                           
  1269: ASGN                          
  1270: SSP      1                    
  1271: LCP      [sp-3]               
  1272: LADR     [sp+0]               
  1273: GCP      data[162]             ; = 8
  1274: ADD                           
  1275: ASGN                          
  1276: SSP      1                    
  1277: LADR     [sp+0]               
  1278: GCP      data[163]             ; = 3
  1279: GCP      data[164]             ; = 24.0f
  1280: XCALL    $SC_ShowHelp(*unsignedlong,unsignedlong,float)void ; args=3
  1281: SSP      3                    
  1282: RET      3                    
  1283: ASP      1                    
  1284: GCP      data[165]             ; = 10
  1285: ASP      1                    
  1286: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1287: LLD      [sp+0]               
  1288: SSP      1                    
  1289: LLD      [sp-3]               
  1290: RET      0                    
  1291: ASP      1                    
  1292: ASP      1                    
  1293: ASP      1                    
  1294: XCALL    $rand(void)int        ; args=0
  1295: LLD      [sp+1]               
  1296: GCP      data[166]             ; = 20
  1297: MOD                           
  1298: LADR     [sp+0]               
  1299: ASGN                          
  1300: SSP      1                    
  1301: ASP      1                    
  1302: GCP      data[167]             ; = 200
  1303: ASP      1                    
  1304: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1305: LLD      [sp+1]               
  1306: SSP      1                    
  1307: GCP      data[168]             ; = 12
  1308: GRE                           
  1309: JZ       label_1356           
  1310: LCP      [sp+0]               
  1311: GCP      data[169]             ; = 19
  1312: GRE                           
  1313: JZ       label_1317           
  1314: GCP      data[170]             ; = 18
  1315: LLD      [sp-3]               
  1316: RET      1                    
label_1317:
  1317: LCP      [sp+0]               
  1318: GCP      data[171]             ; = 18
  1319: GRE                           
  1320: JZ       label_1324           
  1321: GCP      data[172]             ; = 15
  1322: LLD      [sp-3]               
  1323: RET      1                    
label_1324:
  1324: LCP      [sp+0]               
  1325: GCP      data[173]             ; = 17
  1326: GRE                           
  1327: JZ       label_1331           
  1328: GCP      data[174]             ; = 26
  1329: LLD      [sp-3]               
  1330: RET      1                    
label_1331:
  1331: LCP      [sp+0]               
  1332: GCP      data[175]             ; = 11
  1333: GRE                           
  1334: JZ       label_1338           
  1335: GCP      data[176]             ; = 2
  1336: LLD      [sp-3]               
  1337: RET      1                    
label_1338:
  1338: LCP      [sp+0]               
  1339: GCP      data[177]             ; = 8
  1340: GRE                           
  1341: JZ       label_1345           
  1342: GCP      data[178]             ; = 19
  1343: LLD      [sp-3]               
  1344: RET      1                    
label_1345:
  1345: LCP      [sp+0]               
  1346: GCP      data[179]             ; = 3
  1347: GRE                           
  1348: JZ       label_1352           
  1349: GCP      data[180]             ; = 6
  1350: LLD      [sp-3]               
  1351: RET      1                    
label_1352:
  1352: GCP      data[181]             ; = 23
  1353: LLD      [sp-3]               
  1354: RET      1                    
  1355: JMP      label_1401           
label_1356:
  1356: LCP      [sp+0]               
  1357: GCP      data[182]             ; = 19
  1358: GRE                           
  1359: JZ       label_1363           
  1360: GCP      data[183]             ; = 28
  1361: LLD      [sp-3]               
  1362: RET      1                    
label_1363:
  1363: LCP      [sp+0]               
  1364: GCP      data[184]             ; = 16
  1365: GRE                           
  1366: JZ       label_1370           
  1367: GCP      data[185]             ; = 15
  1368: LLD      [sp-3]               
  1369: RET      1                    
label_1370:
  1370: LCP      [sp+0]               
  1371: GCP      data[186]             ; = 13
  1372: GRE                           
  1373: JZ       label_1377           
  1374: GCP      data[187]             ; = 26
  1375: LLD      [sp-3]               
  1376: RET      1                    
label_1377:
  1377: LCP      [sp+0]               
  1378: GCP      data[188]             ; = 9
  1379: GRE                           
  1380: JZ       label_1384           
  1381: GCP      data[189]             ; = 2
  1382: LLD      [sp-3]               
  1383: RET      1                    
label_1384:
  1384: LCP      [sp+0]               
  1385: GCP      data[190]             ; = 6
  1386: GRE                           
  1387: JZ       label_1391           
  1388: GCP      data[191]             ; = 19
  1389: LLD      [sp-3]               
  1390: RET      1                    
label_1391:
  1391: LCP      [sp+0]               
  1392: GCP      data[192]             ; = 3
  1393: GRE                           
  1394: JZ       label_1398           
  1395: GCP      data[193]             ; = 6
  1396: LLD      [sp-3]               
  1397: RET      1                    
label_1398:
  1398: GCP      data[194]             ; = 23
  1399: LLD      [sp-3]               
  1400: RET      1                    
label_1401:
  1401: ASP      1                    
  1402: ASP      1                    
  1403: ASP      1                    
  1404: XCALL    $rand(void)int        ; args=0
  1405: LLD      [sp+1]               
  1406: GCP      data[195]             ; = 20
  1407: MOD                           
  1408: LADR     [sp+0]               
  1409: ASGN                          
  1410: SSP      1                    
  1411: LCP      [sp+0]               
  1412: GCP      data[196]             ; = 18
  1413: GRE                           
  1414: JZ       label_1418           
  1415: GCP      data[197]             ; = 14
  1416: LLD      [sp-3]               
  1417: RET      1                    
label_1418:
  1418: LCP      [sp+0]               
  1419: GCP      data[198]             ; = 16
  1420: GRE                           
  1421: JZ       label_1425           
  1422: GCP      data[199]             ; = 18
  1423: LLD      [sp-3]               
  1424: RET      1                    
label_1425:
  1425: LCP      [sp+0]               
  1426: GCP      data[200]             ; = 12
  1427: GRE                           
  1428: JZ       label_1432           
  1429: GCP      data[201]             ; = 2
  1430: LLD      [sp-3]               
  1431: RET      1                    
label_1432:
  1432: LCP      [sp+0]               
  1433: GCP      data[202]             ; = 8
  1434: GRE                           
  1435: JZ       label_1439           
  1436: GCP      data[203]             ; = 15
  1437: LLD      [sp-3]               
  1438: RET      1                    
label_1439:
  1439: GCP      data[204]             ; = 2
  1440: LLD      [sp-3]               
  1441: RET      1                    
  1442: ASP      1                    
  1443: ASP      1                    
  1444: ASP      1                    
  1445: XCALL    $rand(void)int        ; args=0
  1446: LLD      [sp+1]               
  1447: GCP      data[205]             ; = 20
  1448: MOD                           
  1449: LADR     [sp+0]               
  1450: ASGN                          
  1451: SSP      1                    
  1452: ASP      1                    
  1453: GCP      data[206]             ; = 200
  1454: ASP      1                    
  1455: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1456: LLD      [sp+1]               
  1457: SSP      1                    
  1458: JMP      label_1460           
  1459: JMP      label_1464           
label_1460:
  1460: LCP      [sp+1]               
  1461: GCP      data[207]             ; = 1
  1462: EQU                           
  1463: JZ       label_1476           
label_1464:
  1464: LCP      [sp+0]               
  1465: GCP      data[208]             ; = 10
  1466: GRE                           
  1467: JZ       label_1471           
  1468: GCP      data[209]             ; = 19
  1469: LLD      [sp-3]               
  1470: RET      2                    
label_1471:
  1471: GCP      data[210]             ; = 26
  1472: LLD      [sp-3]               
  1473: RET      2                    
  1474: JMP      label_2011           
  1475: JMP      label_1480           
label_1476:
  1476: LCP      [sp+1]               
  1477: GCP      data[211]             ; = 2
  1478: EQU                           
  1479: JZ       label_1481           
label_1480:
  1480: JMP      label_1485           
label_1481:
  1481: LCP      [sp+1]               
  1482: GCP      data[212]             ; = 3
  1483: EQU                           
  1484: JZ       label_1486           
label_1485:
  1485: JMP      label_1490           
label_1486:
  1486: LCP      [sp+1]               
  1487: GCP      data[213]             ; = 4
  1488: EQU                           
  1489: JZ       label_1491           
label_1490:
  1490: JMP      label_1495           
label_1491:
  1491: LCP      [sp+1]               
  1492: GCP      data[214]             ; = 5
  1493: EQU                           
  1494: JZ       label_1514           
label_1495:
  1495: LCP      [sp+0]               
  1496: GCP      data[215]             ; = 12
  1497: GRE                           
  1498: JZ       label_1502           
  1499: GCP      data[216]             ; = 26
  1500: LLD      [sp-3]               
  1501: RET      2                    
label_1502:
  1502: LCP      [sp+0]               
  1503: GCP      data[217]             ; = 8
  1504: GRE                           
  1505: JZ       label_1509           
  1506: GCP      data[218]             ; = 6
  1507: LLD      [sp-3]               
  1508: RET      2                    
label_1509:
  1509: GCP      data[219]             ; = 19
  1510: LLD      [sp-3]               
  1511: RET      2                    
  1512: JMP      label_2011           
  1513: JMP      label_1518           
label_1514:
  1514: LCP      [sp+1]               
  1515: GCP      data[220]             ; = 16
  1516: EQU                           
  1517: JZ       label_1519           
label_1518:
  1518: JMP      label_1523           
label_1519:
  1519: LCP      [sp+1]               
  1520: GCP      data[221]             ; = 17
  1521: EQU                           
  1522: JZ       label_1549           
label_1523:
  1523: LCP      [sp+0]               
  1524: GCP      data[222]             ; = 14
  1525: GRE                           
  1526: JZ       label_1530           
  1527: GCP      data[223]             ; = 26
  1528: LLD      [sp-3]               
  1529: RET      2                    
label_1530:
  1530: LCP      [sp+0]               
  1531: GCP      data[224]             ; = 10
  1532: GRE                           
  1533: JZ       label_1537           
  1534: GCP      data[225]             ; = 19
  1535: LLD      [sp-3]               
  1536: RET      2                    
label_1537:
  1537: LCP      [sp+0]               
  1538: GCP      data[226]             ; = 5
  1539: GRE                           
  1540: JZ       label_1544           
  1541: GCP      data[227]             ; = 6
  1542: LLD      [sp-3]               
  1543: RET      2                    
label_1544:
  1544: GCP      data[228]             ; = 23
  1545: LLD      [sp-3]               
  1546: RET      2                    
  1547: JMP      label_2011           
  1548: JMP      label_1553           
label_1549:
  1549: LCP      [sp+1]               
  1550: GCP      data[229]             ; = 6
  1551: EQU                           
  1552: JZ       label_1586           
label_1553:
  1553: LCP      [sp+0]               
  1554: GCP      data[230]             ; = 15
  1555: GRE                           
  1556: JZ       label_1560           
  1557: GCP      data[231]             ; = 26
  1558: LLD      [sp-3]               
  1559: RET      2                    
label_1560:
  1560: LCP      [sp+0]               
  1561: GCP      data[232]             ; = 11
  1562: GRE                           
  1563: JZ       label_1567           
  1564: GCP      data[233]             ; = 19
  1565: LLD      [sp-3]               
  1566: RET      2                    
label_1567:
  1567: LCP      [sp+0]               
  1568: GCP      data[234]             ; = 7
  1569: GRE                           
  1570: JZ       label_1574           
  1571: GCP      data[235]             ; = 6
  1572: LLD      [sp-3]               
  1573: RET      2                    
label_1574:
  1574: LCP      [sp+0]               
  1575: GCP      data[236]             ; = 2
  1576: GRE                           
  1577: JZ       label_1581           
  1578: GCP      data[237]             ; = 23
  1579: LLD      [sp-3]               
  1580: RET      2                    
label_1581:
  1581: GCP      data[238]             ; = 25
  1582: LLD      [sp-3]               
  1583: RET      2                    
  1584: JMP      label_2011           
  1585: JMP      label_1590           
label_1586:
  1586: LCP      [sp+1]               
  1587: GCP      data[239]             ; = 7
  1588: EQU                           
  1589: JZ       label_1591           
label_1590:
  1590: JMP      label_1595           
label_1591:
  1591: LCP      [sp+1]               
  1592: GCP      data[240]             ; = 8
  1593: EQU                           
  1594: JZ       label_1596           
label_1595:
  1595: JMP      label_1600           
label_1596:
  1596: LCP      [sp+1]               
  1597: GCP      data[241]             ; = 10
  1598: EQU                           
  1599: JZ       label_1633           
label_1600:
  1600: LCP      [sp+0]               
  1601: GCP      data[242]             ; = 16
  1602: GRE                           
  1603: JZ       label_1607           
  1604: GCP      data[243]             ; = 26
  1605: LLD      [sp-3]               
  1606: RET      2                    
label_1607:
  1607: LCP      [sp+0]               
  1608: GCP      data[244]             ; = 12
  1609: GRE                           
  1610: JZ       label_1614           
  1611: GCP      data[245]             ; = 15
  1612: LLD      [sp-3]               
  1613: RET      2                    
label_1614:
  1614: LCP      [sp+0]               
  1615: GCP      data[246]             ; = 8
  1616: GRE                           
  1617: JZ       label_1621           
  1618: GCP      data[247]             ; = 6
  1619: LLD      [sp-3]               
  1620: RET      2                    
label_1621:
  1621: LCP      [sp+0]               
  1622: GCP      data[248]             ; = 4
  1623: GRE                           
  1624: JZ       label_1628           
  1625: GCP      data[249]             ; = 19
  1626: LLD      [sp-3]               
  1627: RET      2                    
label_1628:
  1628: GCP      data[250]             ; = 2
  1629: LLD      [sp-3]               
  1630: RET      2                    
  1631: JMP      label_2011           
  1632: JMP      label_1637           
label_1633:
  1633: LCP      [sp+1]               
  1634: GCP      data[251]             ; = 9
  1635: EQU                           
  1636: JZ       label_1638           
label_1637:
  1637: JMP      label_1642           
label_1638:
  1638: LCP      [sp+1]               
  1639: GCP      data[252]             ; = 11
  1640: EQU                           
  1641: JZ       label_1643           
label_1642:
  1642: JMP      label_1647           
label_1643:
  1643: LCP      [sp+1]               
  1644: GCP      data[253]             ; = 23
  1645: EQU                           
  1646: JZ       label_1666           
label_1647:
  1647: LCP      [sp+0]               
  1648: GCP      data[254]             ; = 13
  1649: GRE                           
  1650: JZ       label_1654           
  1651: GCP      data[255]             ; = 8
  1652: LLD      [sp-3]               
  1653: RET      2                    
label_1654:
  1654: LCP      [sp+0]               
  1655: GCP      data[256]             ; = 6
  1656: GRE                           
  1657: JZ       label_1661           
  1658: GCP      data[257]             ; = 9
  1659: LLD      [sp-3]               
  1660: RET      2                    
label_1661:
  1661: GCP      data[258]             ; = 10
  1662: LLD      [sp-3]               
  1663: RET      2                    
  1664: JMP      label_2011           
  1665: JMP      label_1670           
label_1666:
  1666: LCP      [sp+1]               
  1667: GCP      data[259]             ; = 12
  1668: EQU                           
  1669: JZ       label_1710           
label_1670:
  1670: LCP      [sp+0]               
  1671: GCP      data[260]             ; = 15
  1672: GRE                           
  1673: JZ       label_1677           
  1674: GCP      data[261]             ; = 2
  1675: LLD      [sp-3]               
  1676: RET      2                    
label_1677:
  1677: LCP      [sp+0]               
  1678: GCP      data[262]             ; = 11
  1679: GRE                           
  1680: JZ       label_1684           
  1681: GCP      data[263]             ; = 15
  1682: LLD      [sp-3]               
  1683: RET      2                    
label_1684:
  1684: LCP      [sp+0]               
  1685: GCP      data[264]             ; = 8
  1686: GRE                           
  1687: JZ       label_1691           
  1688: GCP      data[265]             ; = 19
  1689: LLD      [sp-3]               
  1690: RET      2                    
label_1691:
  1691: LCP      [sp+0]               
  1692: GCP      data[266]             ; = 4
  1693: GRE                           
  1694: JZ       label_1698           
  1695: GCP      data[267]             ; = 6
  1696: LLD      [sp-3]               
  1697: RET      2                    
label_1698:
  1698: LCP      [sp+0]               
  1699: GCP      data[268]             ; = 1
  1700: GRE                           
  1701: JZ       label_1705           
  1702: GCP      data[269]             ; = 26
  1703: LLD      [sp-3]               
  1704: RET      2                    
label_1705:
  1705: GCP      data[270]             ; = 18
  1706: LLD      [sp-3]               
  1707: RET      2                    
  1708: JMP      label_2011           
  1709: JMP      label_1714           
label_1710:
  1710: LCP      [sp+1]               
  1711: GCP      data[271]             ; = 13
  1712: EQU                           
  1713: JZ       label_1715           
label_1714:
  1714: JMP      label_1719           
label_1715:
  1715: LCP      [sp+1]               
  1716: GCP      data[272]             ; = 14
  1717: EQU                           
  1718: JZ       label_1720           
label_1719:
  1719: JMP      label_1724           
label_1720:
  1720: LCP      [sp+1]               
  1721: GCP      data[273]             ; = 15
  1722: EQU                           
  1723: JZ       label_1725           
label_1724:
  1724: JMP      label_1729           
label_1725:
  1725: LCP      [sp+1]               
  1726: GCP      data[274]             ; = 18
  1727: EQU                           
  1728: JZ       label_1768           
label_1729:
  1729: LCP      [sp+0]               
  1730: GCP      data[275]             ; = 15
  1731: GRE                           
  1732: JZ       label_1736           
  1733: GCP      data[276]             ; = 2
  1734: LLD      [sp-3]               
  1735: RET      2                    
label_1736:
  1736: LCP      [sp+0]               
  1737: GCP      data[277]             ; = 11
  1738: GRE                           
  1739: JZ       label_1743           
  1740: GCP      data[278]             ; = 15
  1741: LLD      [sp-3]               
  1742: RET      2                    
label_1743:
  1743: LCP      [sp+0]               
  1744: GCP      data[279]             ; = 8
  1745: GRE                           
  1746: JZ       label_1750           
  1747: GCP      data[280]             ; = 19
  1748: LLD      [sp-3]               
  1749: RET      2                    
label_1750:
  1750: LCP      [sp+0]               
  1751: GCP      data[281]             ; = 5
  1752: GRE                           
  1753: JZ       label_1757           
  1754: GCP      data[282]             ; = 6
  1755: LLD      [sp-3]               
  1756: RET      2                    
label_1757:
  1757: LCP      [sp+0]               
  1758: GCP      data[283]             ; = 2
  1759: GRE                           
  1760: JZ       label_1764           
  1761: GCP      data[284]             ; = 26
  1762: LLD      [sp-3]               
  1763: RET      2                    
label_1764:
  1764: GCP      data[285]             ; = 23
  1765: LLD      [sp-3]               
  1766: RET      2                    
  1767: JMP      label_1772           
label_1768:
  1768: LCP      [sp+1]               
  1769: GCP      data[286]             ; = 19
  1770: EQU                           
  1771: JZ       label_1773           
label_1772:
  1772: JMP      label_1777           
label_1773:
  1773: LCP      [sp+1]               
  1774: GCP      data[287]             ; = 20
  1775: EQU                           
  1776: JZ       label_1778           
label_1777:
  1777: JMP      label_1782           
label_1778:
  1778: LCP      [sp+1]               
  1779: GCP      data[288]             ; = 21
  1780: EQU                           
  1781: JZ       label_1783           
label_1782:
  1782: JMP      label_1787           
label_1783:
  1783: LCP      [sp+1]               
  1784: GCP      data[289]             ; = 22
  1785: EQU                           
  1786: JZ       label_1813           
label_1787:
  1787: LCP      [sp+0]               
  1788: GCP      data[290]             ; = 14
  1789: GRE                           
  1790: JZ       label_1794           
  1791: GCP      data[291]             ; = 2
  1792: LLD      [sp-3]               
  1793: RET      2                    
label_1794:
  1794: LCP      [sp+0]               
  1795: GCP      data[292]             ; = 10
  1796: GRE                           
  1797: JZ       label_1801           
  1798: GCP      data[293]             ; = 15
  1799: LLD      [sp-3]               
  1800: RET      2                    
label_1801:
  1801: LCP      [sp+0]               
  1802: GCP      data[294]             ; = 4
  1803: GRE                           
  1804: JZ       label_1808           
  1805: GCP      data[295]             ; = 23
  1806: LLD      [sp-3]               
  1807: RET      2                    
label_1808:
  1808: GCP      data[296]             ; = 18
  1809: LLD      [sp-3]               
  1810: RET      2                    
  1811: JMP      label_2011           
  1812: JMP      label_1817           
label_1813:
  1813: LCP      [sp+1]               
  1814: GCP      data[297]             ; = 24
  1815: EQU                           
  1816: JZ       label_1857           
label_1817:
  1817: LCP      [sp+0]               
  1818: GCP      data[298]             ; = 15
  1819: GRE                           
  1820: JZ       label_1824           
  1821: GCP      data[299]             ; = 2
  1822: LLD      [sp-3]               
  1823: RET      2                    
label_1824:
  1824: LCP      [sp+0]               
  1825: GCP      data[300]             ; = 11
  1826: GRE                           
  1827: JZ       label_1831           
  1828: GCP      data[301]             ; = 19
  1829: LLD      [sp-3]               
  1830: RET      2                    
label_1831:
  1831: LCP      [sp+0]               
  1832: GCP      data[302]             ; = 8
  1833: GRE                           
  1834: JZ       label_1838           
  1835: GCP      data[303]             ; = 6
  1836: LLD      [sp-3]               
  1837: RET      2                    
label_1838:
  1838: LCP      [sp+0]               
  1839: GCP      data[304]             ; = 4
  1840: GRE                           
  1841: JZ       label_1845           
  1842: GCP      data[305]             ; = 23
  1843: LLD      [sp-3]               
  1844: RET      2                    
label_1845:
  1845: LCP      [sp+0]               
  1846: GCP      data[306]             ; = 1
  1847: GRE                           
  1848: JZ       label_1852           
  1849: GCP      data[307]             ; = 26
  1850: LLD      [sp-3]               
  1851: RET      2                    
label_1852:
  1852: GCP      data[308]             ; = 21
  1853: LLD      [sp-3]               
  1854: RET      2                    
  1855: JMP      label_2011           
  1856: JMP      label_1861           
label_1857:
  1857: LCP      [sp+1]               
  1858: GCP      data[309]             ; = 26
  1859: EQU                           
  1860: JZ       label_1862           
label_1861:
  1861: JMP      label_1866           
label_1862:
  1862: LCP      [sp+1]               
  1863: GCP      data[310]             ; = 27
  1864: EQU                           
  1865: JZ       label_1867           
label_1866:
  1866: JMP      label_1871           
label_1867:
  1867: LCP      [sp+1]               
  1868: GCP      data[311]             ; = 28
  1869: EQU                           
  1870: JZ       label_1905           
label_1871:
  1871: LCP      [sp+0]               
  1872: GCP      data[312]             ; = 14
  1873: GRE                           
  1874: JZ       label_1878           
  1875: GCP      data[313]             ; = 2
  1876: LLD      [sp-3]               
  1877: RET      2                    
label_1878:
  1878: LCP      [sp+0]               
  1879: GCP      data[314]             ; = 10
  1880: GRE                           
  1881: JZ       label_1885           
  1882: GCP      data[315]             ; = 15
  1883: LLD      [sp-3]               
  1884: RET      2                    
label_1885:
  1885: LCP      [sp+0]               
  1886: GCP      data[316]             ; = 7
  1887: GRE                           
  1888: JZ       label_1892           
  1889: GCP      data[317]             ; = 23
  1890: LLD      [sp-3]               
  1891: RET      2                    
label_1892:
  1892: LCP      [sp+0]               
  1893: GCP      data[318]             ; = 3
  1894: GRE                           
  1895: JZ       label_1899           
  1896: GCP      data[319]             ; = 6
  1897: LLD      [sp-3]               
  1898: RET      2                    
label_1899:
  1899: GCP      data[320]             ; = 18
  1900: LLD      [sp-3]               
  1901: RET      2                    
  1902: JMP      label_2011           
  1903: JMP      label_2011           
  1904: JMP      label_1909           
label_1905:
  1905: LCP      [sp+1]               
  1906: GCP      data[321]             ; = 29
  1907: EQU                           
  1908: JZ       label_1942           
label_1909:
  1909: LCP      [sp+0]               
  1910: GCP      data[322]             ; = 14
  1911: GRE                           
  1912: JZ       label_1916           
  1913: GCP      data[323]             ; = 2
  1914: LLD      [sp-3]               
  1915: RET      2                    
label_1916:
  1916: LCP      [sp+0]               
  1917: GCP      data[324]             ; = 11
  1918: GRE                           
  1919: JZ       label_1923           
  1920: GCP      data[325]             ; = 15
  1921: LLD      [sp-3]               
  1922: RET      2                    
label_1923:
  1923: LCP      [sp+0]               
  1924: GCP      data[326]             ; = 8
  1925: GRE                           
  1926: JZ       label_1930           
  1927: GCP      data[327]             ; = 18
  1928: LLD      [sp-3]               
  1929: RET      2                    
label_1930:
  1930: LCP      [sp+0]               
  1931: GCP      data[328]             ; = 3
  1932: GRE                           
  1933: JZ       label_1937           
  1934: GCP      data[329]             ; = 23
  1935: LLD      [sp-3]               
  1936: RET      2                    
label_1937:
  1937: GCP      data[330]             ; = 6
  1938: LLD      [sp-3]               
  1939: RET      2                    
  1940: JMP      label_2011           
  1941: JMP      label_1946           
label_1942:
  1942: LCP      [sp+1]               
  1943: GCP      data[331]             ; = 25
  1944: EQU                           
  1945: JZ       label_1958           
label_1946:
  1946: LCP      [sp+0]               
  1947: GCP      data[332]             ; = 2
  1948: GRE                           
  1949: JZ       label_1953           
  1950: GCP      data[333]             ; = 2
  1951: LLD      [sp-3]               
  1952: RET      2                    
label_1953:
  1953: GCP      data[334]             ; = 14
  1954: LLD      [sp-3]               
  1955: RET      2                    
  1956: JMP      label_2011           
  1957: JMP      label_1962           
label_1958:
  1958: LCP      [sp+1]               
  1959: GCP      data[335]             ; = 30
  1960: EQU                           
  1961: JZ       label_1963           
label_1962:
  1962: JMP      label_1967           
label_1963:
  1963: LCP      [sp+1]               
  1964: GCP      data[336]             ; = 31
  1965: EQU                           
  1966: JZ       label_1968           
label_1967:
  1967: JMP      label_1972           
label_1968:
  1968: LCP      [sp+1]               
  1969: GCP      data[337]             ; = 32
  1970: EQU                           
  1971: JZ       label_2011           
label_1972:
  1972: LCP      [sp+0]               
  1973: GCP      data[338]             ; = 13
  1974: GRE                           
  1975: JZ       label_1979           
  1976: GCP      data[339]             ; = 2
  1977: LLD      [sp-3]               
  1978: RET      2                    
label_1979:
  1979: LCP      [sp+0]               
  1980: GCP      data[340]             ; = 11
  1981: GRE                           
  1982: JZ       label_1986           
  1983: GCP      data[341]             ; = 15
  1984: LLD      [sp-3]               
  1985: RET      2                    
label_1986:
  1986: LCP      [sp+0]               
  1987: GCP      data[342]             ; = 7
  1988: GRE                           
  1989: JZ       label_1993           
  1990: GCP      data[343]             ; = 18
  1991: LLD      [sp-3]               
  1992: RET      2                    
label_1993:
  1993: LCP      [sp+0]               
  1994: GCP      data[344]             ; = 4
  1995: GRE                           
  1996: JZ       label_2000           
  1997: GCP      data[345]             ; = 23
  1998: LLD      [sp-3]               
  1999: RET      2                    
label_2000:
  2000: LCP      [sp+0]               
  2001: GCP      data[346]             ; = 1
  2002: GRE                           
  2003: JZ       label_2007           
  2004: GCP      data[347]             ; = 6
  2005: LLD      [sp-3]               
  2006: RET      2                    
label_2007:
  2007: GCP      data[348]             ; = 14
  2008: LLD      [sp-3]               
  2009: RET      2                    
  2010: JMP      label_2011           
label_2011:
  2011: SSP      1                    
  2012: GCP      data[349]             ; = 2
  2013: LLD      [sp-3]               
  2014: RET      1                    
  2015: ASP      1                    
  2016: ASP      1                    
  2017: ASP      1                    
  2018: XCALL    $rand(void)int        ; args=0
  2019: LLD      [sp+1]               
  2020: GCP      data[350]             ; = 20
  2021: MOD                           
  2022: LADR     [sp+0]               
  2023: ASGN                          
  2024: SSP      1                    
  2025: ASP      1                    
  2026: GCP      data[351]             ; = 200
  2027: ASP      1                    
  2028: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2029: LLD      [sp+1]               
  2030: SSP      1                    
  2031: JMP      label_2033           
  2032: JMP      label_2037           
label_2033:
  2033: LCP      [sp+1]               
  2034: GCP      data[352]             ; = 1
  2035: EQU                           
  2036: JZ       label_2038           
label_2037:
  2037: JMP      label_2042           
label_2038:
  2038: LCP      [sp+1]               
  2039: GCP      data[353]             ; = 16
  2040: EQU                           
  2041: JZ       label_2043           
label_2042:
  2042: JMP      label_2047           
label_2043:
  2043: LCP      [sp+1]               
  2044: GCP      data[354]             ; = 17
  2045: EQU                           
  2046: JZ       label_2048           
label_2047:
  2047: JMP      label_2052           
label_2048:
  2048: LCP      [sp+1]               
  2049: GCP      data[355]             ; = 6
  2050: EQU                           
  2051: JZ       label_2071           
label_2052:
  2052: LCP      [sp+0]               
  2053: GCP      data[356]             ; = 13
  2054: GRE                           
  2055: JZ       label_2059           
  2056: GADR     data[357]  ; "ini\players\poorvc.ini"
  2057: LLD      [sp-3]               
  2058: RET      2                    
label_2059:
  2059: LCP      [sp+0]               
  2060: GCP      data[363]             ; = 6
  2061: GRE                           
  2062: JZ       label_2066           
  2063: GADR     data[364]  ; "ini\players\poorvc2.ini"
  2064: LLD      [sp-3]               
  2065: RET      2                    
label_2066:
  2066: GADR     data[370]  ; "ini\players\poorvc3.ini"
  2067: LLD      [sp-3]               
  2068: RET      2                    
  2069: JMP      label_2289           
  2070: JMP      label_2075           
label_2071:
  2071: LCP      [sp+1]               
  2072: GCP      data[376]             ; = 2
  2073: EQU                           
  2074: JZ       label_2076           
label_2075:
  2075: JMP      label_2080           
label_2076:
  2076: LCP      [sp+1]               
  2077: GCP      data[377]             ; = 3
  2078: EQU                           
  2079: JZ       label_2081           
label_2080:
  2080: JMP      label_2085           
label_2081:
  2081: LCP      [sp+1]               
  2082: GCP      data[378]             ; = 4
  2083: EQU                           
  2084: JZ       label_2086           
label_2085:
  2085: JMP      label_2090           
label_2086:
  2086: LCP      [sp+1]               
  2087: GCP      data[379]             ; = 5
  2088: EQU                           
  2089: JZ       label_2091           
label_2090:
  2090: JMP      label_2095           
label_2091:
  2091: LCP      [sp+1]               
  2092: GCP      data[380]             ; = 7
  2093: EQU                           
  2094: JZ       label_2096           
label_2095:
  2095: JMP      label_2100           
label_2096:
  2096: LCP      [sp+1]               
  2097: GCP      data[381]             ; = 8
  2098: EQU                           
  2099: JZ       label_2101           
label_2100:
  2100: JMP      label_2105           
label_2101:
  2101: LCP      [sp+1]               
  2102: GCP      data[382]             ; = 10
  2103: EQU                           
  2104: JZ       label_2124           
label_2105:
  2105: LCP      [sp+0]               
  2106: GCP      data[383]             ; = 13
  2107: GRE                           
  2108: JZ       label_2112           
  2109: GADR     data[384]  ; "ini\players\vcfighter2.ini"
  2110: LLD      [sp-3]               
  2111: RET      2                    
label_2112:
  2112: LCP      [sp+0]               
  2113: GCP      data[391]             ; = 6
  2114: GRE                           
  2115: JZ       label_2119           
  2116: GADR     data[392]  ; "ini\players\vcfighter3.ini"
  2117: LLD      [sp-3]               
  2118: RET      2                    
label_2119:
  2119: GADR     data[399]  ; "ini\players\vcfighter4.ini"
  2120: LLD      [sp-3]               
  2121: RET      2                    
  2122: JMP      label_2289           
  2123: JMP      label_2128           
label_2124:
  2124: LCP      [sp+1]               
  2125: GCP      data[406]             ; = 9
  2126: EQU                           
  2127: JZ       label_2129           
label_2128:
  2128: JMP      label_2133           
label_2129:
  2129: LCP      [sp+1]               
  2130: GCP      data[407]             ; = 11
  2131: EQU                           
  2132: JZ       label_2134           
label_2133:
  2133: JMP      label_2138           
label_2134:
  2134: LCP      [sp+1]               
  2135: GCP      data[408]             ; = 12
  2136: EQU                           
  2137: JZ       label_2139           
label_2138:
  2138: JMP      label_2143           
label_2139:
  2139: LCP      [sp+1]               
  2140: GCP      data[409]             ; = 13
  2141: EQU                           
  2142: JZ       label_2144           
label_2143:
  2143: JMP      label_2148           
label_2144:
  2144: LCP      [sp+1]               
  2145: GCP      data[410]             ; = 14
  2146: EQU                           
  2147: JZ       label_2149           
label_2148:
  2148: JMP      label_2153           
label_2149:
  2149: LCP      [sp+1]               
  2150: GCP      data[411]             ; = 15
  2151: EQU                           
  2152: JZ       label_2154           
label_2153:
  2153: JMP      label_2158           
label_2154:
  2154: LCP      [sp+1]               
  2155: GCP      data[412]             ; = 24
  2156: EQU                           
  2157: JZ       label_2184           
label_2158:
  2158: LCP      [sp+0]               
  2159: GCP      data[413]             ; = 15
  2160: GRE                           
  2161: JZ       label_2165           
  2162: GADR     data[414]  ; "ini\players\vcfighter3.ini"
  2163: LLD      [sp-3]               
  2164: RET      2                    
label_2165:
  2165: LCP      [sp+0]               
  2166: GCP      data[421]             ; = 10
  2167: GRE                           
  2168: JZ       label_2172           
  2169: GADR     data[422]  ; "ini\players\vcfighter2.ini"
  2170: LLD      [sp-3]               
  2171: RET      2                    
label_2172:
  2172: LCP      [sp+0]               
  2173: GCP      data[429]             ; = 5
  2174: GRE                           
  2175: JZ       label_2179           
  2176: GADR     data[430]  ; "ini\players\vcfighter3.ini"
  2177: LLD      [sp-3]               
  2178: RET      2                    
label_2179:
  2179: GADR     data[437]  ; "ini\players\vcfighter4.ini"
  2180: LLD      [sp-3]               
  2181: RET      2                    
  2182: JMP      label_2289           
  2183: JMP      label_2188           
label_2184:
  2184: LCP      [sp+1]               
  2185: GCP      data[444]             ; = 18
  2186: EQU                           
  2187: JZ       label_2189           
label_2188:
  2188: JMP      label_2193           
label_2189:
  2189: LCP      [sp+1]               
  2190: GCP      data[445]             ; = 19
  2191: EQU                           
  2192: JZ       label_2194           
label_2193:
  2193: JMP      label_2198           
label_2194:
  2194: LCP      [sp+1]               
  2195: GCP      data[446]             ; = 20
  2196: EQU                           
  2197: JZ       label_2199           
label_2198:
  2198: JMP      label_2203           
label_2199:
  2199: LCP      [sp+1]               
  2200: GCP      data[447]             ; = 21
  2201: EQU                           
  2202: JZ       label_2204           
label_2203:
  2203: JMP      label_2208           
label_2204:
  2204: LCP      [sp+1]               
  2205: GCP      data[448]             ; = 26
  2206: EQU                           
  2207: JZ       label_2209           
label_2208:
  2208: JMP      label_2213           
label_2209:
  2209: LCP      [sp+1]               
  2210: GCP      data[449]             ; = 27
  2211: EQU                           
  2212: JZ       label_2214           
label_2213:
  2213: JMP      label_2218           
label_2214:
  2214: LCP      [sp+1]               
  2215: GCP      data[450]             ; = 28
  2216: EQU                           
  2217: JZ       label_2237           
label_2218:
  2218: LCP      [sp+0]               
  2219: GCP      data[451]             ; = 13
  2220: GRE                           
  2221: JZ       label_2225           
  2222: GADR     data[452]  ; "ini\players\vcuniform1.ini"
  2223: LLD      [sp-3]               
  2224: RET      2                    
label_2225:
  2225: LCP      [sp+0]               
  2226: GCP      data[459]             ; = 6
  2227: GRE                           
  2228: JZ       label_2232           
  2229: GADR     data[460]  ; "ini\players\vcuniform2.ini"
  2230: LLD      [sp-3]               
  2231: RET      2                    
label_2232:
  2232: GADR     data[467]  ; "ini\players\vcuniform3.ini"
  2233: LLD      [sp-3]               
  2234: RET      2                    
  2235: JMP      label_2289           
  2236: JMP      label_2241           
label_2237:
  2237: LCP      [sp+1]               
  2238: GCP      data[474]             ; = 22
  2239: EQU                           
  2240: JZ       label_2242           
label_2241:
  2241: JMP      label_2246           
label_2242:
  2242: LCP      [sp+1]               
  2243: GCP      data[475]             ; = 23
  2244: EQU                           
  2245: JZ       label_2247           
label_2246:
  2246: JMP      label_2251           
label_2247:
  2247: LCP      [sp+1]               
  2248: GCP      data[476]             ; = 25
  2249: EQU                           
  2250: JZ       label_2252           
label_2251:
  2251: JMP      label_2256           
label_2252:
  2252: LCP      [sp+1]               
  2253: GCP      data[477]             ; = 29
  2254: EQU                           
  2255: JZ       label_2257           
label_2256:
  2256: JMP      label_2261           
label_2257:
  2257: LCP      [sp+1]               
  2258: GCP      data[478]             ; = 30
  2259: EQU                           
  2260: JZ       label_2262           
label_2261:
  2261: JMP      label_2266           
label_2262:
  2262: LCP      [sp+1]               
  2263: GCP      data[479]             ; = 31
  2264: EQU                           
  2265: JZ       label_2267           
label_2266:
  2266: JMP      label_2271           
label_2267:
  2267: LCP      [sp+1]               
  2268: GCP      data[480]             ; = 32
  2269: EQU                           
  2270: JZ       label_2289           
label_2271:
  2271: LCP      [sp+0]               
  2272: GCP      data[481]             ; = 12
  2273: GRE                           
  2274: JZ       label_2278           
  2275: GADR     data[482]  ; "ini\players\nvasoldier2.ini"
  2276: LLD      [sp-3]               
  2277: RET      2                    
label_2278:
  2278: LCP      [sp+0]               
  2279: GCP      data[489]             ; = 4
  2280: GRE                           
  2281: JZ       label_2285           
  2282: GADR     data[490]  ; "ini\players\nvasoldier3.ini"
  2283: LLD      [sp-3]               
  2284: RET      2                    
label_2285:
  2285: GADR     data[497]  ; "ini\players\nvaofficer.ini"
  2286: LLD      [sp-3]               
  2287: RET      2                    
  2288: JMP      label_2289           
label_2289:
  2289: SSP      1                    
  2290: GADR     data[504]  ; "ini\players\default_aiviet.ini"
  2291: LLD      [sp-3]               
  2292: RET      1                    
  2293: ASP      1                    
  2294: GCP      data[512]             ; = 0.0f
  2295: LADR     [sp+0]               
  2296: ASGN                          
  2297: SSP      1                    
label_2298:
  2298: LCP      [sp+0]               
  2299: GCP      data[513]             ; = 8
  2300: LES                           
  2301: JZ       label_2329           
  2302: GCP      data[514]             ; = 0.0f
  2303: LADR     [sp-3]               
  2304: DADR     92                   
  2305: LCP      [sp+0]               
  2306: GCP      data[515]             ; = 4
  2307: MUL                           
  2308: ADD                           
  2309: ASGN                          
  2310: SSP      1                    
  2311: GCP      data[516]             ; = 0.0f
  2312: LADR     [sp-3]               
  2313: DADR     124                  
  2314: LCP      [sp+0]               
  2315: GCP      data[517]             ; = 4
  2316: MUL                           
  2317: ADD                           
  2318: ASGN                          
  2319: SSP      1                    
  2320: LCP      [sp+0]               
  2321: LCP      [sp+0]               
  2322: GCP      data[518]             ; = 1
  2323: ADD                           
  2324: LADR     [sp+0]               
  2325: ASGN                          
  2326: SSP      1                    
  2327: SSP      1                    
  2328: JMP      label_2298           
label_2329:
  2329: ASP      1                    
  2330: GCP      data[519]             ; = 200
  2331: ASP      1                    
  2332: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2333: LLD      [sp+1]               
  2334: SSP      1                    
  2335: JMP      label_2337           
  2336: JMP      label_2341           
label_2337:
  2337: LCP      [sp+1]               
  2338: GCP      data[520]             ; = 1
  2339: EQU                           
  2340: JZ       label_2357           
label_2341:
  2341: GCP      data[521]             ; = 24
  2342: LADR     [sp-3]               
  2343: DADR     92                   
  2344: GCP      data[522]             ; = 0.0f
  2345: ADD                           
  2346: ASGN                          
  2347: SSP      1                    
  2348: GCP      data[523]             ; = 38
  2349: LADR     [sp-3]               
  2350: DADR     92                   
  2351: GCP      data[524]             ; = 4
  2352: ADD                           
  2353: ASGN                          
  2354: SSP      1                    
  2355: JMP      label_2908           
  2356: JMP      label_2361           
label_2357:
  2357: LCP      [sp+1]               
  2358: GCP      data[525]             ; = 2
  2359: EQU                           
  2360: JZ       label_2362           
label_2361:
  2361: JMP      label_2366           
label_2362:
  2362: LCP      [sp+1]               
  2363: GCP      data[526]             ; = 3
  2364: EQU                           
  2365: JZ       label_2367           
label_2366:
  2366: JMP      label_2371           
label_2367:
  2367: LCP      [sp+1]               
  2368: GCP      data[527]             ; = 4
  2369: EQU                           
  2370: JZ       label_2372           
label_2371:
  2371: JMP      label_2376           
label_2372:
  2372: LCP      [sp+1]               
  2373: GCP      data[528]             ; = 5
  2374: EQU                           
  2375: JZ       label_2392           
label_2376:
  2376: GCP      data[529]             ; = 23
  2377: LADR     [sp-3]               
  2378: DADR     92                   
  2379: GCP      data[530]             ; = 0.0f
  2380: ADD                           
  2381: ASGN                          
  2382: SSP      1                    
  2383: GCP      data[531]             ; = 25
  2384: LADR     [sp-3]               
  2385: DADR     92                   
  2386: GCP      data[532]             ; = 4
  2387: ADD                           
  2388: ASGN                          
  2389: SSP      1                    
  2390: JMP      label_2908           
  2391: JMP      label_2396           
label_2392:
  2392: LCP      [sp+1]               
  2393: GCP      data[533]             ; = 16
  2394: EQU                           
  2395: JZ       label_2397           
label_2396:
  2396: JMP      label_2401           
label_2397:
  2397: LCP      [sp+1]               
  2398: GCP      data[534]             ; = 17
  2399: EQU                           
  2400: JZ       label_2424           
label_2401:
  2401: GCP      data[535]             ; = 23
  2402: LADR     [sp-3]               
  2403: DADR     92                   
  2404: GCP      data[536]             ; = 0.0f
  2405: ADD                           
  2406: ASGN                          
  2407: SSP      1                    
  2408: GCP      data[537]             ; = 26
  2409: LADR     [sp-3]               
  2410: DADR     92                   
  2411: GCP      data[538]             ; = 4
  2412: ADD                           
  2413: ASGN                          
  2414: SSP      1                    
  2415: GCP      data[539]             ; = 24
  2416: LADR     [sp-3]               
  2417: DADR     92                   
  2418: GCP      data[540]             ; = 8
  2419: ADD                           
  2420: ASGN                          
  2421: SSP      1                    
  2422: JMP      label_2908           
  2423: JMP      label_2428           
label_2424:
  2424: LCP      [sp+1]               
  2425: GCP      data[541]             ; = 6
  2426: EQU                           
  2427: JZ       label_2451           
label_2428:
  2428: GCP      data[542]             ; = 24
  2429: LADR     [sp-3]               
  2430: DADR     92                   
  2431: GCP      data[543]             ; = 0.0f
  2432: ADD                           
  2433: ASGN                          
  2434: SSP      1                    
  2435: GCP      data[544]             ; = 26
  2436: LADR     [sp-3]               
  2437: DADR     92                   
  2438: GCP      data[545]             ; = 4
  2439: ADD                           
  2440: ASGN                          
  2441: SSP      1                    
  2442: GCP      data[546]             ; = 38
  2443: LADR     [sp-3]               
  2444: DADR     92                   
  2445: GCP      data[547]             ; = 8
  2446: ADD                           
  2447: ASGN                          
  2448: SSP      1                    
  2449: JMP      label_2908           
  2450: JMP      label_2455           
label_2451:
  2451: LCP      [sp+1]               
  2452: GCP      data[548]             ; = 7
  2453: EQU                           
  2454: JZ       label_2456           
label_2455:
  2455: JMP      label_2460           
label_2456:
  2456: LCP      [sp+1]               
  2457: GCP      data[549]             ; = 8
  2458: EQU                           
  2459: JZ       label_2483           
label_2460:
  2460: GCP      data[550]             ; = 23
  2461: LADR     [sp-3]               
  2462: DADR     92                   
  2463: GCP      data[551]             ; = 0.0f
  2464: ADD                           
  2465: ASGN                          
  2466: SSP      1                    
  2467: GCP      data[552]             ; = 24
  2468: LADR     [sp-3]               
  2469: DADR     92                   
  2470: GCP      data[553]             ; = 4
  2471: ADD                           
  2472: ASGN                          
  2473: SSP      1                    
  2474: GCP      data[554]             ; = 25
  2475: LADR     [sp-3]               
  2476: DADR     92                   
  2477: GCP      data[555]             ; = 8
  2478: ADD                           
  2479: ASGN                          
  2480: SSP      1                    
  2481: JMP      label_2908           
  2482: JMP      label_2487           
label_2483:
  2483: LCP      [sp+1]               
  2484: GCP      data[556]             ; = 9
  2485: EQU                           
  2486: JZ       label_2488           
label_2487:
  2487: JMP      label_2492           
label_2488:
  2488: LCP      [sp+1]               
  2489: GCP      data[557]             ; = 11
  2490: EQU                           
  2491: JZ       label_2493           
label_2492:
  2492: JMP      label_2497           
label_2493:
  2493: LCP      [sp+1]               
  2494: GCP      data[558]             ; = 10
  2495: EQU                           
  2496: JZ       label_2513           
label_2497:
  2497: GCP      data[559]             ; = 23
  2498: LADR     [sp-3]               
  2499: DADR     92                   
  2500: GCP      data[560]             ; = 0.0f
  2501: ADD                           
  2502: ASGN                          
  2503: SSP      1                    
  2504: GCP      data[561]             ; = 25
  2505: LADR     [sp-3]               
  2506: DADR     92                   
  2507: GCP      data[562]             ; = 4
  2508: ADD                           
  2509: ASGN                          
  2510: SSP      1                    
  2511: JMP      label_2908           
  2512: JMP      label_2517           
label_2513:
  2513: LCP      [sp+1]               
  2514: GCP      data[563]             ; = 12
  2515: EQU                           
  2516: JZ       label_2554           
label_2517:
  2517: GCP      data[564]             ; = 23
  2518: LADR     [sp-3]               
  2519: DADR     92                   
  2520: GCP      data[565]             ; = 0.0f
  2521: ADD                           
  2522: ASGN                          
  2523: SSP      1                    
  2524: GCP      data[566]             ; = 24
  2525: LADR     [sp-3]               
  2526: DADR     92                   
  2527: GCP      data[567]             ; = 4
  2528: ADD                           
  2529: ASGN                          
  2530: SSP      1                    
  2531: GCP      data[568]             ; = 25
  2532: LADR     [sp-3]               
  2533: DADR     92                   
  2534: GCP      data[569]             ; = 8
  2535: ADD                           
  2536: ASGN                          
  2537: SSP      1                    
  2538: GCP      data[570]             ; = 37
  2539: LADR     [sp-3]               
  2540: DADR     92                   
  2541: GCP      data[571]             ; = 12
  2542: ADD                           
  2543: ASGN                          
  2544: SSP      1                    
  2545: GCP      data[572]             ; = 38
  2546: LADR     [sp-3]               
  2547: DADR     92                   
  2548: GCP      data[573]             ; = 16
  2549: ADD                           
  2550: ASGN                          
  2551: SSP      1                    
  2552: JMP      label_2908           
  2553: JMP      label_2558           
label_2554:
  2554: LCP      [sp+1]               
  2555: GCP      data[574]             ; = 13
  2556: EQU                           
  2557: JZ       label_2559           
label_2558:
  2558: JMP      label_2563           
label_2559:
  2559: LCP      [sp+1]               
  2560: GCP      data[575]             ; = 14
  2561: EQU                           
  2562: JZ       label_2564           
label_2563:
  2563: JMP      label_2568           
label_2564:
  2564: LCP      [sp+1]               
  2565: GCP      data[576]             ; = 15
  2566: EQU                           
  2567: JZ       label_2584           
label_2568:
  2568: GCP      data[577]             ; = 23
  2569: LADR     [sp-3]               
  2570: DADR     92                   
  2571: GCP      data[578]             ; = 0.0f
  2572: ADD                           
  2573: ASGN                          
  2574: SSP      1                    
  2575: GCP      data[579]             ; = 25
  2576: LADR     [sp-3]               
  2577: DADR     92                   
  2578: GCP      data[580]             ; = 4
  2579: ADD                           
  2580: ASGN                          
  2581: SSP      1                    
  2582: JMP      label_2908           
  2583: JMP      label_2588           
label_2584:
  2584: LCP      [sp+1]               
  2585: GCP      data[581]             ; = 18
  2586: EQU                           
  2587: JZ       label_2589           
label_2588:
  2588: JMP      label_2593           
label_2589:
  2589: LCP      [sp+1]               
  2590: GCP      data[582]             ; = 19
  2591: EQU                           
  2592: JZ       label_2594           
label_2593:
  2593: JMP      label_2598           
label_2594:
  2594: LCP      [sp+1]               
  2595: GCP      data[583]             ; = 20
  2596: EQU                           
  2597: JZ       label_2621           
label_2598:
  2598: GCP      data[584]             ; = 27
  2599: LADR     [sp-3]               
  2600: DADR     92                   
  2601: GCP      data[585]             ; = 0.0f
  2602: ADD                           
  2603: ASGN                          
  2604: SSP      1                    
  2605: GCP      data[586]             ; = 28
  2606: LADR     [sp-3]               
  2607: DADR     92                   
  2608: GCP      data[587]             ; = 4
  2609: ADD                           
  2610: ASGN                          
  2611: SSP      1                    
  2612: GCP      data[588]             ; = 31
  2613: LADR     [sp-3]               
  2614: DADR     92                   
  2615: GCP      data[589]             ; = 8
  2616: ADD                           
  2617: ASGN                          
  2618: SSP      1                    
  2619: JMP      label_2908           
  2620: JMP      label_2625           
label_2621:
  2621: LCP      [sp+1]               
  2622: GCP      data[590]             ; = 21
  2623: EQU                           
  2624: JZ       label_2655           
label_2625:
  2625: GCP      data[591]             ; = 27
  2626: LADR     [sp-3]               
  2627: DADR     92                   
  2628: GCP      data[592]             ; = 0.0f
  2629: ADD                           
  2630: ASGN                          
  2631: SSP      1                    
  2632: GCP      data[593]             ; = 28
  2633: LADR     [sp-3]               
  2634: DADR     92                   
  2635: GCP      data[594]             ; = 4
  2636: ADD                           
  2637: ASGN                          
  2638: SSP      1                    
  2639: GCP      data[595]             ; = 31
  2640: LADR     [sp-3]               
  2641: DADR     92                   
  2642: GCP      data[596]             ; = 8
  2643: ADD                           
  2644: ASGN                          
  2645: SSP      1                    
  2646: GCP      data[597]             ; = 35
  2647: LADR     [sp-3]               
  2648: DADR     92                   
  2649: GCP      data[598]             ; = 12
  2650: ADD                           
  2651: ASGN                          
  2652: SSP      1                    
  2653: JMP      label_2908           
  2654: JMP      label_2659           
label_2655:
  2655: LCP      [sp+1]               
  2656: GCP      data[599]             ; = 22
  2657: EQU                           
  2658: JZ       label_2660           
label_2659:
  2659: JMP      label_2664           
label_2660:
  2660: LCP      [sp+1]               
  2661: GCP      data[600]             ; = 23
  2662: EQU                           
  2663: JZ       label_2701           
label_2664:
  2664: GCP      data[601]             ; = 35
  2665: LADR     [sp-3]               
  2666: DADR     92                   
  2667: GCP      data[602]             ; = 0.0f
  2668: ADD                           
  2669: ASGN                          
  2670: SSP      1                    
  2671: GCP      data[603]             ; = 27
  2672: LADR     [sp-3]               
  2673: DADR     92                   
  2674: GCP      data[604]             ; = 4
  2675: ADD                           
  2676: ASGN                          
  2677: SSP      1                    
  2678: GCP      data[605]             ; = 32
  2679: LADR     [sp-3]               
  2680: DADR     92                   
  2681: GCP      data[606]             ; = 8
  2682: ADD                           
  2683: ASGN                          
  2684: SSP      1                    
  2685: GCP      data[607]             ; = 33
  2686: LADR     [sp-3]               
  2687: DADR     92                   
  2688: GCP      data[608]             ; = 12
  2689: ADD                           
  2690: ASGN                          
  2691: SSP      1                    
  2692: GCP      data[609]             ; = 34
  2693: LADR     [sp-3]               
  2694: DADR     92                   
  2695: GCP      data[610]             ; = 16
  2696: ADD                           
  2697: ASGN                          
  2698: SSP      1                    
  2699: JMP      label_2908           
  2700: JMP      label_2705           
label_2701:
  2701: LCP      [sp+1]               
  2702: GCP      data[611]             ; = 24
  2703: EQU                           
  2704: JZ       label_2721           
label_2705:
  2705: GCP      data[612]             ; = 23
  2706: LADR     [sp-3]               
  2707: DADR     92                   
  2708: GCP      data[613]             ; = 0.0f
  2709: ADD                           
  2710: ASGN                          
  2711: SSP      1                    
  2712: GCP      data[614]             ; = 25
  2713: LADR     [sp-3]               
  2714: DADR     92                   
  2715: GCP      data[615]             ; = 4
  2716: ADD                           
  2717: ASGN                          
  2718: SSP      1                    
  2719: JMP      label_2908           
  2720: JMP      label_2725           
label_2721:
  2721: LCP      [sp+1]               
  2722: GCP      data[616]             ; = 26
  2723: EQU                           
  2724: JZ       label_2726           
label_2725:
  2725: JMP      label_2730           
label_2726:
  2726: LCP      [sp+1]               
  2727: GCP      data[617]             ; = 27
  2728: EQU                           
  2729: JZ       label_2731           
label_2730:
  2730: JMP      label_2735           
label_2731:
  2731: LCP      [sp+1]               
  2732: GCP      data[618]             ; = 28
  2733: EQU                           
  2734: JZ       label_2765           
label_2735:
  2735: GCP      data[619]             ; = 26
  2736: LADR     [sp-3]               
  2737: DADR     92                   
  2738: GCP      data[620]             ; = 0.0f
  2739: ADD                           
  2740: ASGN                          
  2741: SSP      1                    
  2742: GCP      data[621]             ; = 27
  2743: LADR     [sp-3]               
  2744: DADR     92                   
  2745: GCP      data[622]             ; = 4
  2746: ADD                           
  2747: ASGN                          
  2748: SSP      1                    
  2749: GCP      data[623]             ; = 28
  2750: LADR     [sp-3]               
  2751: DADR     92                   
  2752: GCP      data[624]             ; = 8
  2753: ADD                           
  2754: ASGN                          
  2755: SSP      1                    
  2756: GCP      data[625]             ; = 31
  2757: LADR     [sp-3]               
  2758: DADR     92                   
  2759: GCP      data[626]             ; = 12
  2760: ADD                           
  2761: ASGN                          
  2762: SSP      1                    
  2763: JMP      label_2908           
  2764: JMP      label_2769           
label_2765:
  2765: LCP      [sp+1]               
  2766: GCP      data[627]             ; = 25
  2767: EQU                           
  2768: JZ       label_2792           
label_2769:
  2769: GCP      data[628]             ; = 31
  2770: LADR     [sp-3]               
  2771: DADR     92                   
  2772: GCP      data[629]             ; = 0.0f
  2773: ADD                           
  2774: ASGN                          
  2775: SSP      1                    
  2776: GCP      data[630]             ; = 35
  2777: LADR     [sp-3]               
  2778: DADR     92                   
  2779: GCP      data[631]             ; = 4
  2780: ADD                           
  2781: ASGN                          
  2782: SSP      1                    
  2783: GCP      data[632]             ; = 36
  2784: LADR     [sp-3]               
  2785: DADR     92                   
  2786: GCP      data[633]             ; = 8
  2787: ADD                           
  2788: ASGN                          
  2789: SSP      1                    
  2790: JMP      label_2908           
  2791: JMP      label_2796           
label_2792:
  2792: LCP      [sp+1]               
  2793: GCP      data[634]             ; = 29
  2794: EQU                           
  2795: JZ       label_2826           
label_2796:
  2796: GCP      data[635]             ; = 35
  2797: LADR     [sp-3]               
  2798: DADR     92                   
  2799: GCP      data[636]             ; = 0.0f
  2800: ADD                           
  2801: ASGN                          
  2802: SSP      1                    
  2803: GCP      data[637]             ; = 32
  2804: LADR     [sp-3]               
  2805: DADR     92                   
  2806: GCP      data[638]             ; = 4
  2807: ADD                           
  2808: ASGN                          
  2809: SSP      1                    
  2810: GCP      data[639]             ; = 33
  2811: LADR     [sp-3]               
  2812: DADR     92                   
  2813: GCP      data[640]             ; = 8
  2814: ADD                           
  2815: ASGN                          
  2816: SSP      1                    
  2817: GCP      data[641]             ; = 34
  2818: LADR     [sp-3]               
  2819: DADR     92                   
  2820: GCP      data[642]             ; = 12
  2821: ADD                           
  2822: ASGN                          
  2823: SSP      1                    
  2824: JMP      label_2908           
  2825: JMP      label_2830           
label_2826:
  2826: LCP      [sp+1]               
  2827: GCP      data[643]             ; = 30
  2828: EQU                           
  2829: JZ       label_2831           
label_2830:
  2830: JMP      label_2835           
label_2831:
  2831: LCP      [sp+1]               
  2832: GCP      data[644]             ; = 31
  2833: EQU                           
  2834: JZ       label_2836           
label_2835:
  2835: JMP      label_2840           
label_2836:
  2836: LCP      [sp+1]               
  2837: GCP      data[645]             ; = 32
  2838: EQU                           
  2839: JZ       label_2907           
label_2840:
  2840: GCP      data[646]             ; = 33
  2841: LADR     [sp-3]               
  2842: DADR     92                   
  2843: GCP      data[647]             ; = 0.0f
  2844: ADD                           
  2845: ASGN                          
  2846: SSP      1                    
  2847: GCP      data[648]             ; = 34
  2848: LADR     [sp-3]               
  2849: DADR     92                   
  2850: GCP      data[649]             ; = 4
  2851: ADD                           
  2852: ASGN                          
  2853: SSP      1                    
  2854: GCP      data[650]             ; = 35
  2855: LADR     [sp-3]               
  2856: DADR     92                   
  2857: GCP      data[651]             ; = 8
  2858: ADD                           
  2859: ASGN                          
  2860: SSP      1                    
  2861: GCP      data[652]             ; = 36
  2862: LADR     [sp-3]               
  2863: DADR     92                   
  2864: GCP      data[653]             ; = 12
  2865: ADD                           
  2866: ASGN                          
  2867: SSP      1                    
  2868: JMP      label_2908           
  2869: JMP      label_2870           
label_2870:
  2870: GCP      data[654]             ; = 35
  2871: LADR     [sp-3]               
  2872: DADR     92                   
  2873: GCP      data[655]             ; = 0.0f
  2874: ADD                           
  2875: ASGN                          
  2876: SSP      1                    
  2877: GCP      data[656]             ; = 27
  2878: LADR     [sp-3]               
  2879: DADR     92                   
  2880: GCP      data[657]             ; = 4
  2881: ADD                           
  2882: ASGN                          
  2883: SSP      1                    
  2884: GCP      data[658]             ; = 32
  2885: LADR     [sp-3]               
  2886: DADR     92                   
  2887: GCP      data[659]             ; = 8
  2888: ADD                           
  2889: ASGN                          
  2890: SSP      1                    
  2891: GCP      data[660]             ; = 33
  2892: LADR     [sp-3]               
  2893: DADR     92                   
  2894: GCP      data[661]             ; = 12
  2895: ADD                           
  2896: ASGN                          
  2897: SSP      1                    
  2898: GCP      data[662]             ; = 34
  2899: LADR     [sp-3]               
  2900: DADR     92                   
  2901: GCP      data[663]             ; = 16
  2902: ADD                           
  2903: ASGN                          
  2904: SSP      1                    
  2905: JMP      label_2908           
  2906: JMP      label_2908           
label_2907:
  2907: JMP      label_2870           
label_2908:
  2908: SSP      1                    
  2909: RET      1                    
  2910: ASP      128                  
  2911: ASP      3                    
  2912: ASP      3                    
  2913: GCP      data[664]             ; = 32
  2914: ASP      1                    
  2915: ASP      1                    
  2916: ASP      1                    
  2917: GCP      data[665]             ; = 100.0f
  2918: LADR     [sp+136]             
  2919: ASGN                          
  2920: SSP      1                    
  2921: ASP      1                    
  2922: GCP      data[666]             ; = 11
  2923: ASP      1                    
  2924: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2925: LLD      [sp+138]             
  2926: SSP      1                    
  2927: JZ       label_3016           
  2928: LCP      [sp-5]               
  2929: LADR     [sp+131]             
  2930: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  2931: SSP      2                    
  2932: ASP      1                    
  2933: LADR     [sp+0]               
  2934: LADR     [sp+134]             
  2935: GCP      data[667]             ; = 0.0f
  2936: ASP      1                    
  2937: XCALL    $SC_MP_EnumPlayers(*s_SC_MP_EnumPlayers,*unsignedlong,unsignedlong)int ; args=3
  2938: LLD      [sp+138]             
  2939: SSP      3                    
  2940: SSP      1                    
  2941: LCP      [sp+134]             
  2942: JZ       label_2944           
  2943: JMP      label_2947           
label_2944:
  2944: GCP      data[668]             ; = 0.0f
  2945: LLD      [sp-3]               
  2946: RET      138                  
label_2947:
  2947: GCP      data[669]             ; = 0.0f
  2948: LADR     [sp+135]             
  2949: ASGN                          
  2950: SSP      1                    
label_2951:
  2951: LCP      [sp+135]             
  2952: LCP      [sp+134]             
  2953: LES                           
  2954: JZ       label_3006           
  2955: LADR     [sp+0]               
  2956: LCP      [sp+135]             
  2957: GCP      data[670]             ; = 16
  2958: MUL                           
  2959: ADD                           
  2960: PNT      8                    
  2961: DCP      4                    
  2962: GCP      data[671]             ; = 1
  2963: EQU                           
  2964: JZ       label_2997           
  2965: LADR     [sp+0]               
  2966: LCP      [sp+135]             
  2967: GCP      data[672]             ; = 16
  2968: MUL                           
  2969: ADD                           
  2970: DCP      4                    
  2971: LADR     [sp+128]             
  2972: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  2973: SSP      2                    
  2974: ASP      1                    
  2975: LADR     [sp+128]             
  2976: LADR     [sp+131]             
  2977: ASP      1                    
  2978: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  2979: LLD      [sp+138]             
  2980: SSP      2                    
  2981: LADR     [sp+137]             
  2982: ASGN                          
  2983: SSP      1                    
  2984: LCP      [sp+137]             
  2985: LCP      [sp+136]             
  2986: FLES                          
  2987: JZ       label_2997           
  2988: LCP      [sp+137]             
  2989: LADR     [sp+136]             
  2990: ASGN                          
  2991: SSP      1                    
  2992: LADR     [sp+128]             
  2993: DCP      12                   
  2994: LCP      [sp-4]               
  2995: ASGN                          
  2996: SSP      3                    
label_2997:
  2997: LCP      [sp+135]             
  2998: LCP      [sp+135]             
  2999: GCP      data[673]             ; = 1
  3000: ADD                           
  3001: LADR     [sp+135]             
  3002: ASGN                          
  3003: SSP      1                    
  3004: SSP      1                    
  3005: JMP      label_2951           
label_3006:
  3006: LCP      [sp+136]             
  3007: GCP      data[674]             ; = 100.0f
  3008: FLES                          
  3009: JZ       label_3013           
  3010: GCP      data[675]             ; = 1
  3011: LLD      [sp-3]               
  3012: RET      138                  
label_3013:
  3013: GCP      data[676]             ; = 0.0f
  3014: LLD      [sp-3]               
  3015: RET      138                  
label_3016:
  3016: ASP      1                    
  3017: LCP      [sp-4]               
  3018: ASP      1                    
  3019: XCALL    $SC_PC_GetPos(*c_Vector3)int ; args=1
  3020: LLD      [sp+138]             
  3021: SSP      1                    
  3022: SSP      1                    
  3023: ASP      1                    
  3024: LADR     [sp+128]             
  3025: LADR     [sp+131]             
  3026: ASP      1                    
  3027: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  3028: LLD      [sp+138]             
  3029: SSP      2                    
  3030: LADR     [sp+136]             
  3031: ASGN                          
  3032: SSP      1                    
  3033: LCP      [sp+136]             
  3034: GCP      data[677]             ; = 100.0f
  3035: FLES                          
  3036: JZ       label_3040           
  3037: GCP      data[678]             ; = 1
  3038: LLD      [sp-3]               
  3039: RET      138                  
label_3040:
  3040: GCP      data[679]             ; = 0.0f
  3041: LLD      [sp-3]               
  3042: RET      138                  
  3043: ASP      1                    
  3044: ASP      1                    
  3045: ASP      1                    
  3046: LCP      [sp-5]               
  3047: LCP      [sp-4]               
  3048: ASP      1                    
  3049: XCALL    $SC_GetGroupPlayers(unsignedlong,unsignedlong)unsignedlong ; args=2
  3050: LLD      [sp+2]               
  3051: SSP      2                    
  3052: LADR     [sp+1]               
  3053: ASGN                          
  3054: SSP      1                    
  3055: GCP      data[680]             ; = 0.0f
  3056: LADR     [sp+0]               
  3057: ASGN                          
  3058: SSP      1                    
label_3059:
  3059: LCP      [sp+0]               
  3060: LCP      [sp+1]               
  3061: LES                           
  3062: JZ       label_3090           
  3063: ASP      1                    
  3064: ASP      1                    
  3065: LCP      [sp-5]               
  3066: LCP      [sp-4]               
  3067: LCP      [sp+0]               
  3068: ASP      1                    
  3069: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3070: LLD      [sp+3]               
  3071: SSP      3                    
  3072: ASP      1                    
  3073: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  3074: LLD      [sp+2]               
  3075: SSP      1                    
  3076: JZ       label_3081           
  3077: JMP      label_3078           
label_3078:
  3078: GCP      data[681]             ; = 0.0f
  3079: LLD      [sp-3]               
  3080: RET      2                    
label_3081:
  3081: LCP      [sp+0]               
  3082: LCP      [sp+0]               
  3083: GCP      data[682]             ; = 1
  3084: ADD                           
  3085: LADR     [sp+0]               
  3086: ASGN                          
  3087: SSP      1                    
  3088: SSP      1                    
  3089: JMP      label_3059           
label_3090:
  3090: GCP      data[683]             ; = 1
  3091: LLD      [sp-3]               
  3092: RET      2                    
  3093: ASP      1                    
  3094: ASP      1                    
  3095: ASP      1                    
  3096: LCP      [sp-5]               
  3097: LCP      [sp-4]               
  3098: ASP      1                    
  3099: XCALL    $SC_GetGroupPlayers(unsignedlong,unsignedlong)unsignedlong ; args=2
  3100: LLD      [sp+2]               
  3101: SSP      2                    
  3102: LADR     [sp+1]               
  3103: ASGN                          
  3104: SSP      1                    
  3105: GCP      data[684]             ; = 0.0f
  3106: LADR     [sp+0]               
  3107: ASGN                          
  3108: SSP      1                    
label_3109:
  3109: LCP      [sp+0]               
  3110: LCP      [sp+1]               
  3111: LES                           
  3112: JZ       label_3155           
  3113: ASP      1                    
  3114: ASP      1                    
  3115: LCP      [sp-5]               
  3116: LCP      [sp-4]               
  3117: LCP      [sp+0]               
  3118: ASP      1                    
  3119: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3120: LLD      [sp+3]               
  3121: SSP      3                    
  3122: ASP      1                    
  3123: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  3124: LLD      [sp+2]               
  3125: SSP      1                    
  3126: JZ       label_3146           
  3127: JMP      label_3128           
label_3128:
  3128: ASP      1                    
  3129: ASP      1                    
  3130: LCP      [sp-5]               
  3131: LCP      [sp-4]               
  3132: LCP      [sp+0]               
  3133: ASP      1                    
  3134: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3135: LLD      [sp+3]               
  3136: SSP      3                    
  3137: ASP      1                    
  3138: XCALL    $SC_P_GetActive(unsignedlong)int ; args=1
  3139: LLD      [sp+2]               
  3140: SSP      1                    
  3141: JZ       label_3146           
  3142: JMP      label_3143           
label_3143:
  3143: GCP      data[685]             ; = 0.0f
  3144: LLD      [sp-3]               
  3145: RET      2                    
label_3146:
  3146: LCP      [sp+0]               
  3147: LCP      [sp+0]               
  3148: GCP      data[686]             ; = 1
  3149: ADD                           
  3150: LADR     [sp+0]               
  3151: ASGN                          
  3152: SSP      1                    
  3153: SSP      1                    
  3154: JMP      label_3109           
label_3155:
  3155: GCP      data[687]             ; = 1
  3156: LLD      [sp-3]               
  3157: RET      2                    
  3158: ASP      1                    
  3159: ASP      1                    
  3160: ASP      1                    
  3161: ASP      1                    
  3162: ASP      1                    
  3163: ASP      1                    
  3164: GCP      data[688]             ; = 1
  3165: LCP      [sp-4]               
  3166: ASP      1                    
  3167: XCALL    $SC_GetGroupPlayers(unsignedlong,unsignedlong)unsignedlong ; args=2
  3168: LLD      [sp+5]               
  3169: SSP      2                    
  3170: LADR     [sp+2]               
  3171: ASGN                          
  3172: SSP      1                    
  3173: GCP      data[689]             ; = 0.0f
  3174: LADR     [sp+0]               
  3175: ASGN                          
  3176: SSP      1                    
label_3177:
  3177: LCP      [sp+0]               
  3178: LCP      [sp+2]               
  3179: LES                           
  3180: JZ       label_3235           
  3181: ASP      1                    
  3182: GCP      data[690]             ; = 1
  3183: LCP      [sp-4]               
  3184: LCP      [sp+0]               
  3185: ASP      1                    
  3186: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3187: LLD      [sp+5]               
  3188: SSP      3                    
  3189: LADR     [sp+4]               
  3190: ASGN                          
  3191: SSP      1                    
  3192: LCP      [sp+4]               
  3193: JZ       label_3226           
  3194: ASP      1                    
  3195: LCP      [sp+4]               
  3196: ASP      1                    
  3197: XCALL    $SC_P_Ai_GetDanger(unsignedlong)float ; args=1
  3198: LLD      [sp+5]               
  3199: SSP      1                    
  3200: LADR     [sp+3]               
  3201: ASGN                          
  3202: SSP      1                    
  3203: LCP      [sp+3]               
  3204: GCP      data[691]             ; = 2.0f
  3205: FGRE                          
  3206: JZ       label_3210           
  3207: GCP      data[692]             ; = 1
  3208: LLD      [sp-3]               
  3209: RET      5                    
label_3210:
  3210: ASP      1                    
  3211: LCP      [sp+4]               
  3212: ASP      1                    
  3213: XCALL    $SC_P_Ai_GetSureEnemies(unsignedlong)unsignedlong ; args=1
  3214: LLD      [sp+5]               
  3215: SSP      1                    
  3216: LADR     [sp+1]               
  3217: ASGN                          
  3218: SSP      1                    
  3219: LCP      [sp+1]               
  3220: GCP      data[693]             ; = 0.0f
  3221: GRE                           
  3222: JZ       label_3226           
  3223: GCP      data[694]             ; = 1
  3224: LLD      [sp-3]               
  3225: RET      5                    
label_3226:
  3226: LCP      [sp+0]               
  3227: LCP      [sp+0]               
  3228: GCP      data[695]             ; = 1
  3229: ADD                           
  3230: LADR     [sp+0]               
  3231: ASGN                          
  3232: SSP      1                    
  3233: SSP      1                    
  3234: JMP      label_3177           
label_3235:
  3235: GCP      data[696]             ; = 0.0f
  3236: LLD      [sp-3]               
  3237: RET      5                    
  3238: ASP      1                    
  3239: ASP      1                    
  3240: ASP      1                    
  3241: ASP      1                    
  3242: ASP      1                    
  3243: GCP      data[697]             ; = 1
  3244: LADR     [sp+0]               
  3245: ASGN                          
  3246: SSP      1                    
label_3247:
  3247: LCP      [sp+0]               
  3248: GCP      data[698]             ; = 6
  3249: LES                           
  3250: JZ       label_3305           
  3251: ASP      1                    
  3252: GCP      data[699]             ; = 0.0f
  3253: GCP      data[700]             ; = 0.0f
  3254: LCP      [sp+0]               
  3255: ASP      1                    
  3256: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3257: LLD      [sp+5]               
  3258: SSP      3                    
  3259: LADR     [sp+4]               
  3260: ASGN                          
  3261: SSP      1                    
  3262: LCP      [sp+4]               
  3263: JZ       label_3296           
  3264: ASP      1                    
  3265: LCP      [sp+4]               
  3266: ASP      1                    
  3267: XCALL    $SC_P_Ai_GetDanger(unsignedlong)float ; args=1
  3268: LLD      [sp+5]               
  3269: SSP      1                    
  3270: LADR     [sp+3]               
  3271: ASGN                          
  3272: SSP      1                    
  3273: LCP      [sp+3]               
  3274: GCP      data[701]             ; = 2.0f
  3275: FGRE                          
  3276: JZ       label_3280           
  3277: GCP      data[702]             ; = 1
  3278: LLD      [sp-3]               
  3279: RET      5                    
label_3280:
  3280: ASP      1                    
  3281: LCP      [sp+4]               
  3282: ASP      1                    
  3283: XCALL    $SC_P_Ai_GetSureEnemies(unsignedlong)unsignedlong ; args=1
  3284: LLD      [sp+5]               
  3285: SSP      1                    
  3286: LADR     [sp+1]               
  3287: ASGN                          
  3288: SSP      1                    
  3289: LCP      [sp+1]               
  3290: GCP      data[703]             ; = 0.0f
  3291: GRE                           
  3292: JZ       label_3296           
  3293: GCP      data[704]             ; = 1
  3294: LLD      [sp-3]               
  3295: RET      5                    
label_3296:
  3296: LCP      [sp+0]               
  3297: LCP      [sp+0]               
  3298: GCP      data[705]             ; = 1
  3299: ADD                           
  3300: LADR     [sp+0]               
  3301: ASGN                          
  3302: SSP      1                    
  3303: SSP      1                    
  3304: JMP      label_3247           
label_3305:
  3305: GCP      data[706]             ; = 0.0f
  3306: LLD      [sp-3]               
  3307: RET      5                    
  3308: ASP      1                    
  3309: ASP      3                    
  3310: GCP      data[707]             ; = 10000.0f
  3311: ASP      1                    
  3312: ASP      1                    
  3313: GCP      data[708]             ; = 0.0f
  3314: LADR     [sp+0]               
  3315: ASGN                          
  3316: SSP      1                    
label_3317:
  3317: LCP      [sp+0]               
  3318: GCP      data[709]             ; = 6
  3319: LES                           
  3320: JZ       label_3365           
  3321: ASP      1                    
  3322: GCP      data[710]             ; = 0.0f
  3323: GCP      data[711]             ; = 0.0f
  3324: LCP      [sp+0]               
  3325: ASP      1                    
  3326: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3327: LLD      [sp+7]               
  3328: SSP      3                    
  3329: LADR     [sp+6]               
  3330: ASGN                          
  3331: SSP      1                    
  3332: LCP      [sp+6]               
  3333: JZ       label_3356           
  3334: LCP      [sp+6]               
  3335: LADR     [sp+1]               
  3336: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  3337: SSP      2                    
  3338: ASP      1                    
  3339: LCP      [sp-4]               
  3340: LADR     [sp+1]               
  3341: ASP      1                    
  3342: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  3343: LLD      [sp+7]               
  3344: SSP      2                    
  3345: LADR     [sp+5]               
  3346: ASGN                          
  3347: SSP      1                    
  3348: LCP      [sp+5]               
  3349: LCP      [sp+4]               
  3350: FLES                          
  3351: JZ       label_3356           
  3352: LCP      [sp+5]               
  3353: LADR     [sp+4]               
  3354: ASGN                          
  3355: SSP      1                    
label_3356:
  3356: LCP      [sp+0]               
  3357: LCP      [sp+0]               
  3358: GCP      data[712]             ; = 1
  3359: ADD                           
  3360: LADR     [sp+0]               
  3361: ASGN                          
  3362: SSP      1                    
  3363: SSP      1                    
  3364: JMP      label_3317           
label_3365:
  3365: LCP      [sp+4]               
  3366: LLD      [sp-3]               
  3367: RET      7                    
func_3368:
  3368: ASP      1                    
  3369: ASP      1                    
  3370: GCP      data[713]             ; = 0.0f
  3371: LCP      [sp-4]               
  3372: ASP      1                    
  3373: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  3374: LLD      [sp+1]               
  3375: SSP      2                    
  3376: LADR     [sp+0]               
  3377: ASGN                          
  3378: SSP      1                    
  3379: LCP      [sp+0]               
  3380: GCP      data[714]             ; = 0.0f
  3381: NEQ                           
  3382: JZ       label_3387           
  3383: LCP      [sp+0]               
  3384: LCP      [sp-3]               
  3385: XCALL    $SC_NOD_GetWorldPos(*void,*c_Vector3)void ; args=2
  3386: SSP      2                    
label_3387:
  3387: RET      1                    
  3388: ASP      1                    
  3389: ASP      1                    
  3390: GCP      data[715]             ; = 0.0f
  3391: LCP      [sp-4]               
  3392: ASP      1                    
  3393: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  3394: LLD      [sp+1]               
  3395: SSP      2                    
  3396: LADR     [sp+0]               
  3397: ASGN                          
  3398: SSP      1                    
  3399: LCP      [sp+0]               
  3400: GCP      data[716]             ; = 0.0f
  3401: NEQ                           
  3402: JZ       label_3411           
  3403: ASP      1                    
  3404: LCP      [sp+0]               
  3405: ASP      1                    
  3406: XCALL    $SC_NOD_GetWorldRotZ(*void)float ; args=1
  3407: LLD      [sp+1]               
  3408: SSP      1                    
  3409: LLD      [sp-3]               
  3410: RET      1                    
label_3411:
  3411: GCP      data[717]             ; = 0.0f
  3412: LLD      [sp-3]               
  3413: RET      1                    
  3414: ASP      1                    
  3415: ASP      1                    
  3416: GCP      data[718]             ; = 0.0f
  3417: GCP      data[719]             ; = 0.0f
  3418: GCP      data[720]             ; = 1
  3419: ASP      1                    
  3420: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3421: LLD      [sp+1]               
  3422: SSP      3                    
  3423: ASP      1                    
  3424: XCALL    $SC_P_Ai_GetPeaceMode(unsignedlong)unsignedlong ; args=1
  3425: LLD      [sp+0]               
  3426: SSP      1                    
  3427: GCP      data[721]             ; = 2
  3428: EQU                           
  3429: JZ       label_3441           
  3430: ASP      1                    
  3431: GCP      data[722]             ; = 0.0f
  3432: GCP      data[723]             ; = 0.0f
  3433: GCP      data[724]             ; = 1
  3434: ASP      1                    
  3435: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3436: LLD      [sp+0]               
  3437: SSP      3                    
  3438: GCP      data[725]             ; = 0.0f
  3439: XCALL    $SC_P_Ai_SetPeaceMode(unsignedlong,unsignedlong)void ; args=2
  3440: SSP      2                    
label_3441:
  3441: ASP      1                    
  3442: GCP      data[726]             ; = 0.0f
  3443: GCP      data[727]             ; = 0.0f
  3444: GCP      data[728]             ; = 1
  3445: ASP      1                    
  3446: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  3447: LLD      [sp+0]               
  3448: SSP      3                    
  3449: XCALL    $SC_P_Ai_Stop(unsignedlong)void ; args=1
  3450: SSP      1                    
  3451: RET      0                    
  3452: ASP      3                    
  3453: LCP      [sp-4]               
  3454: LADR     [sp+0]               
  3455: CALL     func_3368            
  3456: SSP      2                    
  3457: LADR     [sp+0]               
  3458: LCP      [sp-3]               
  3459: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3460: SSP      2                    
  3461: RET      3                    
  3462: ASP      1                    
  3463: ASP      3                    
  3464: ASP      3                    
  3465: ASP      1                    
  3466: ASP      1                    
  3467: GCP      data[729]             ; = 0.0f
  3468: LCP      [sp-3]               
  3469: ASP      1                    
  3470: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  3471: LLD      [sp+8]               
  3472: SSP      2                    
  3473: LADR     [sp+7]               
  3474: ASGN                          
  3475: SSP      1                    
  3476: LCP      [sp+7]               
  3477: JZ       label_3479           
  3478: JMP      label_3484           
label_3479:
  3479: GADR     data[730]  ; "FATAL! Claymore %s not found!!!!!!"
  3480: GCP      data[739]             ; = 1
  3481: XCALL    $SC_message(*char,...)void ; args=4294967295
  3482: SSP      1                    
  3483: RET      8                    
label_3484:
  3484: LCP      [sp+7]               
  3485: LADR     [sp+1]               
  3486: XCALL    $SC_NOD_GetWorldPos(*void,*c_Vector3)void ; args=2
  3487: SSP      2                    
  3488: ASP      1                    
  3489: LCP      [sp+7]               
  3490: ASP      1                    
  3491: XCALL    $SC_NOD_GetWorldRotZ(*void)float ; args=1
  3492: LLD      [sp+8]               
  3493: SSP      1                    
  3494: LADR     [sp+0]               
  3495: ASGN                          
  3496: SSP      1                    
  3497: LCP      [sp+0]               
  3498: GCP      data[740]             ; = 1070134723
  3499: FSUB                          
  3500: LADR     [sp+0]               
  3501: ASGN                          
  3502: SSP      1                    
  3503: LADR     [sp+1]               
  3504: DCP      12                   
  3505: LADR     [sp+4]               
  3506: ASGN                          
  3507: SSP      3                    
  3508: LADR     [sp+4]               
  3509: DCP      4                    
  3510: GCP      data[741]             ; = 2.0f
  3511: ASP      1                    
  3512: LCP      [sp+0]               
  3513: ASP      1                    
  3514: XCALL    $cos(float)float      ; args=1
  3515: LLD      [sp+10]              
  3516: SSP      1                    
  3517: FMUL                          
  3518: FSUB                          
  3519: LADR     [sp+4]               
  3520: ASGN                          
  3521: SSP      1                    
  3522: LADR     [sp+4]               
  3523: PNT      4                    
  3524: DCP      4                    
  3525: GCP      data[742]             ; = 2.0f
  3526: ASP      1                    
  3527: LCP      [sp+0]               
  3528: ASP      1                    
  3529: XCALL    $sin(float)float      ; args=1
  3530: LLD      [sp+10]              
  3531: SSP      1                    
  3532: FMUL                          
  3533: FADD                          
  3534: LADR     [sp+4]               
  3535: PNT      4                    
  3536: ASGN                          
  3537: SSP      1                    
  3538: LADR     [sp+4]               
  3539: GCP      data[743]             ; = 1
  3540: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3541: SSP      2                    
  3542: LADR     [sp+1]               
  3543: DCP      12                   
  3544: LADR     [sp+4]               
  3545: ASGN                          
  3546: SSP      3                    
  3547: LADR     [sp+4]               
  3548: DCP      4                    
  3549: GCP      data[744]             ; = 4.0f
  3550: ASP      1                    
  3551: LCP      [sp+0]               
  3552: ASP      1                    
  3553: XCALL    $cos(float)float      ; args=1
  3554: LLD      [sp+10]              
  3555: SSP      1                    
  3556: FMUL                          
  3557: FSUB                          
  3558: LADR     [sp+4]               
  3559: ASGN                          
  3560: SSP      1                    
  3561: LADR     [sp+4]               
  3562: PNT      4                    
  3563: DCP      4                    
  3564: GCP      data[745]             ; = 4.0f
  3565: ASP      1                    
  3566: LCP      [sp+0]               
  3567: ASP      1                    
  3568: XCALL    $sin(float)float      ; args=1
  3569: LLD      [sp+10]              
  3570: SSP      1                    
  3571: FMUL                          
  3572: FADD                          
  3573: LADR     [sp+4]               
  3574: PNT      4                    
  3575: ASGN                          
  3576: SSP      1                    
  3577: LADR     [sp+4]               
  3578: GCP      data[746]             ; = 2
  3579: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3580: SSP      2                    
  3581: LADR     [sp+1]               
  3582: DCP      12                   
  3583: LADR     [sp+4]               
  3584: ASGN                          
  3585: SSP      3                    
  3586: LADR     [sp+4]               
  3587: DCP      4                    
  3588: GCP      data[747]             ; = 8.0f
  3589: ASP      1                    
  3590: LCP      [sp+0]               
  3591: ASP      1                    
  3592: XCALL    $cos(float)float      ; args=1
  3593: LLD      [sp+10]              
  3594: SSP      1                    
  3595: FMUL                          
  3596: FSUB                          
  3597: LADR     [sp+4]               
  3598: ASGN                          
  3599: SSP      1                    
  3600: LADR     [sp+4]               
  3601: PNT      4                    
  3602: DCP      4                    
  3603: GCP      data[748]             ; = 8.0f
  3604: ASP      1                    
  3605: LCP      [sp+0]               
  3606: ASP      1                    
  3607: XCALL    $sin(float)float      ; args=1
  3608: LLD      [sp+10]              
  3609: SSP      1                    
  3610: FMUL                          
  3611: FADD                          
  3612: LADR     [sp+4]               
  3613: PNT      4                    
  3614: ASGN                          
  3615: SSP      1                    
  3616: LADR     [sp+4]               
  3617: GCP      data[749]             ; = 3
  3618: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3619: SSP      2                    
  3620: LCP      [sp+7]               
  3621: GCP      data[750]             ; = 1
  3622: XCALL    $SC_DUMMY_Set_DoNotRenHier2(*void,int)void ; args=2
  3623: SSP      2                    
  3624: RET      8                    
  3625: ASP      1                    
  3626: ASP      3                    
  3627: ASP      3                    
  3628: LCP      [sp-6]               
  3629: LADR     [sp+4]               
  3630: CALL     func_3368            
  3631: SSP      2                    
  3632: LADR     [sp+4]               
  3633: PNT      8                    
  3634: DCP      4                    
  3635: LADR     [sp+1]               
  3636: PNT      8                    
  3637: ASGN                          
  3638: SSP      1                    
  3639: GCP      data[751]             ; = 0.0f
  3640: LADR     [sp+0]               
  3641: ASGN                          
  3642: SSP      1                    
label_3643:
  3643: LCP      [sp+0]               
  3644: LCP      [sp-4]               
  3645: LES                           
  3646: JZ       label_3686           
  3647: LADR     [sp+4]               
  3648: DCP      4                    
  3649: ASP      1                    
  3650: LCP      [sp-3]               
  3651: ASP      1                    
  3652: XCALL    $frnd(float)float     ; args=1
  3653: LLD      [sp+8]               
  3654: SSP      1                    
  3655: FADD                          
  3656: LADR     [sp+1]               
  3657: ASGN                          
  3658: SSP      1                    
  3659: LADR     [sp+4]               
  3660: PNT      4                    
  3661: DCP      4                    
  3662: ASP      1                    
  3663: LCP      [sp-3]               
  3664: ASP      1                    
  3665: XCALL    $frnd(float)float     ; args=1
  3666: LLD      [sp+8]               
  3667: SSP      1                    
  3668: FADD                          
  3669: LADR     [sp+1]               
  3670: PNT      4                    
  3671: ASGN                          
  3672: SSP      1                    
  3673: LADR     [sp+1]               
  3674: LCP      [sp-5]               
  3675: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3676: SSP      2                    
  3677: LCP      [sp+0]               
  3678: LCP      [sp+0]               
  3679: GCP      data[752]             ; = 1
  3680: ADD                           
  3681: LADR     [sp+0]               
  3682: ASGN                          
  3683: SSP      1                    
  3684: SSP      1                    
  3685: JMP      label_3643           
label_3686:
  3686: RET      7                    
  3687: ASP      3                    
  3688: ASP      1                    
  3689: LCP      [sp-4]               
  3690: LADR     [sp+0]               
  3691: ASP      1                    
  3692: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  3693: LLD      [sp+3]               
  3694: SSP      2                    
  3695: SSP      1                    
  3696: LADR     [sp+0]               
  3697: LCP      [sp-3]               
  3698: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3699: SSP      2                    
  3700: RET      3                    
  3701: ASP      3                    
  3702: ASP      1                    
  3703: LCP      [sp-3]               
  3704: LADR     [sp+0]               
  3705: ASP      1                    
  3706: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  3707: LLD      [sp+3]               
  3708: SSP      2                    
  3709: SSP      1                    
  3710: GCP      data[753]             ; = 176
  3711: LADR     [sp+0]               
  3712: XCALL    $SC_CreatePtc(unsignedlong,*c_Vector3)void ; args=2
  3713: SSP      2                    
  3714: RET      3                    
  3715: ASP      3                    
  3716: ASP      1                    
  3717: ASP      1                    
  3718: LCP      [sp-3]               
  3719: LADR     [sp+0]               
  3720: ASP      1                    
  3721: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  3722: LLD      [sp+4]               
  3723: SSP      2                    
  3724: SSP      1                    
  3725: LADR     [sp+0]               
  3726: GCP      data[754]             ; = 3
  3727: XCALL    $SC_DoExplosion(*c_Vector3,unsignedlong)void ; args=2
  3728: SSP      2                    
  3729: GCP      data[755]             ; = 2965
  3730: LADR     [sp+0]               
  3731: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  3732: SSP      2                    
  3733: GCP      data[756]             ; = 176
  3734: ASP      1                    
  3735: GCP      data[757]             ; = 0.0f
  3736: LCP      [sp-3]               
  3737: ASP      1                    
  3738: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  3739: LLD      [sp+5]               
  3740: SSP      2                    
  3741: GCP      data[758]             ; = 1000.0f
  3742: GCP      data[759]             ; = 0.0f
  3743: GCP      data[760]             ; = 1.0f
  3744: GCP      data[761]             ; = 1.0f
  3745: XCALL    $SC_CreatePtc_Ext(unsignedlong,*void,float,float,float,float)void ; args=6
  3746: SSP      6                    
  3747: GCP      data[762]             ; = 177
  3748: ASP      1                    
  3749: GCP      data[763]             ; = 0.0f
  3750: LCP      [sp-3]               
  3751: ASP      1                    
  3752: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  3753: LLD      [sp+5]               
  3754: SSP      2                    
  3755: GCP      data[764]             ; = 1000.0f
  3756: GCP      data[765]             ; = 0.0f
  3757: GCP      data[766]             ; = 1.0f
  3758: GCP      data[767]             ; = 1.0f
  3759: XCALL    $SC_CreatePtc_Ext(unsignedlong,*void,float,float,float,float)void ; args=6
  3760: SSP      6                    
  3761: GCP      data[768]             ; = 0.0f
  3762: LADR     [sp+3]               
  3763: ASGN                          
  3764: SSP      1                    
label_3765:
  3765: LCP      [sp+3]               
  3766: GCP      data[769]             ; = 6
  3767: LES                           
  3768: JZ       label_3820           
  3769: ASP      1                    
  3770: LCP      [sp-3]               
  3771: LADR     [sp+0]               
  3772: ASP      1                    
  3773: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  3774: LLD      [sp+4]               
  3775: SSP      2                    
  3776: SSP      1                    
  3777: LADR     [sp+0]               
  3778: DCP      4                    
  3779: ASP      1                    
  3780: GCP      data[770]             ; = 5.0f
  3781: ASP      1                    
  3782: XCALL    $frnd(float)float     ; args=1
  3783: LLD      [sp+5]               
  3784: SSP      1                    
  3785: FADD                          
  3786: LADR     [sp+0]               
  3787: ASGN                          
  3788: SSP      1                    
  3789: LADR     [sp+0]               
  3790: PNT      4                    
  3791: DCP      4                    
  3792: ASP      1                    
  3793: GCP      data[771]             ; = 5.0f
  3794: ASP      1                    
  3795: XCALL    $frnd(float)float     ; args=1
  3796: LLD      [sp+5]               
  3797: SSP      1                    
  3798: FADD                          
  3799: LADR     [sp+0]               
  3800: PNT      4                    
  3801: ASGN                          
  3802: SSP      1                    
  3803: GCP      data[772]             ; = 177
  3804: LADR     [sp+0]               
  3805: GCP      data[773]             ; = 1000.0f
  3806: GCP      data[774]             ; = 0.0f
  3807: GCP      data[775]             ; = 1.0f
  3808: GCP      data[776]             ; = 1.0f
  3809: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3810: SSP      6                    
  3811: LCP      [sp+3]               
  3812: LCP      [sp+3]               
  3813: GCP      data[777]             ; = 1
  3814: ADD                           
  3815: LADR     [sp+3]               
  3816: ASGN                          
  3817: SSP      1                    
  3818: SSP      1                    
  3819: JMP      label_3765           
label_3820:
  3820: RET      4                    
  3821: ASP      1                    
  3822: GCP      data[778]             ; = 198
  3823: LCP      [sp-3]               
  3824: XCALL    $SC_CreatePtc(unsignedlong,*c_Vector3)void ; args=2
  3825: SSP      2                    
  3826: GCP      data[779]             ; = 2965
  3827: LCP      [sp-3]               
  3828: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  3829: SSP      2                    
  3830: GCP      data[780]             ; = 176
  3831: LCP      [sp-3]               
  3832: GCP      data[781]             ; = 1000.0f
  3833: GCP      data[782]             ; = 0.0f
  3834: GCP      data[783]             ; = 1.0f
  3835: GCP      data[784]             ; = 1.0f
  3836: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3837: SSP      6                    
  3838: GCP      data[785]             ; = 177
  3839: LCP      [sp-3]               
  3840: GCP      data[786]             ; = 5.0f
  3841: GCP      data[787]             ; = 0.0f
  3842: GCP      data[788]             ; = 1.0f
  3843: GCP      data[789]             ; = 1.0f
  3844: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3845: SSP      6                    
  3846: RET      1                    
  3847: ASP      1                    
  3848: ASP      3                    
  3849: LADR     [sp-5]               
  3850: DADR     8                    
  3851: DCP      4                    
  3852: LADR     [sp+1]               
  3853: PNT      8                    
  3854: ASGN                          
  3855: SSP      1                    
  3856: GCP      data[790]             ; = 0.0f
  3857: LADR     [sp+0]               
  3858: ASGN                          
  3859: SSP      1                    
label_3860:
  3860: LCP      [sp+0]               
  3861: LCP      [sp-4]               
  3862: LES                           
  3863: JZ       label_3912           
  3864: LADR     [sp-5]               
  3865: DADR     0                    
  3866: DCP      4                    
  3867: ASP      1                    
  3868: LCP      [sp-3]               
  3869: ASP      1                    
  3870: XCALL    $frnd(float)float     ; args=1
  3871: LLD      [sp+5]               
  3872: SSP      1                    
  3873: FADD                          
  3874: LADR     [sp+1]               
  3875: ASGN                          
  3876: SSP      1                    
  3877: LADR     [sp-5]               
  3878: DADR     4                    
  3879: DCP      4                    
  3880: ASP      1                    
  3881: LCP      [sp-3]               
  3882: ASP      1                    
  3883: XCALL    $frnd(float)float     ; args=1
  3884: LLD      [sp+5]               
  3885: SSP      1                    
  3886: FADD                          
  3887: LADR     [sp+1]               
  3888: PNT      4                    
  3889: ASGN                          
  3890: SSP      1                    
  3891: GCP      data[791]             ; = 198
  3892: LADR     [sp+1]               
  3893: XCALL    $SC_CreatePtc(unsignedlong,*c_Vector3)void ; args=2
  3894: SSP      2                    
  3895: GCP      data[792]             ; = 177
  3896: LADR     [sp+1]               
  3897: GCP      data[793]             ; = 5.0f
  3898: GCP      data[794]             ; = 0.0f
  3899: GCP      data[795]             ; = 1.0f
  3900: GCP      data[796]             ; = 1.0f
  3901: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3902: SSP      6                    
  3903: LCP      [sp+0]               
  3904: LCP      [sp+0]               
  3905: GCP      data[797]             ; = 1
  3906: ADD                           
  3907: LADR     [sp+0]               
  3908: ASGN                          
  3909: SSP      1                    
  3910: SSP      1                    
  3911: JMP      label_3860           
label_3912:
  3912: GCP      data[798]             ; = 176
  3913: LCP      [sp-5]               
  3914: GCP      data[799]             ; = 1000.0f
  3915: GCP      data[800]             ; = 0.0f
  3916: GCP      data[801]             ; = 1.0f
  3917: GCP      data[802]             ; = 1.0f
  3918: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3919: SSP      6                    
  3920: RET      4                    
  3921: ASP      1                    
  3922: ASP      3                    
  3923: LADR     [sp-5]               
  3924: DADR     8                    
  3925: DCP      4                    
  3926: LADR     [sp+1]               
  3927: PNT      8                    
  3928: ASGN                          
  3929: SSP      1                    
  3930: GCP      data[803]             ; = 0.0f
  3931: LADR     [sp+0]               
  3932: ASGN                          
  3933: SSP      1                    
label_3934:
  3934: LCP      [sp+0]               
  3935: LCP      [sp-4]               
  3936: LES                           
  3937: JZ       label_3978           
  3938: LADR     [sp-5]               
  3939: DADR     0                    
  3940: DCP      4                    
  3941: ASP      1                    
  3942: LCP      [sp-3]               
  3943: ASP      1                    
  3944: XCALL    $frnd(float)float     ; args=1
  3945: LLD      [sp+5]               
  3946: SSP      1                    
  3947: FADD                          
  3948: LADR     [sp+1]               
  3949: ASGN                          
  3950: SSP      1                    
  3951: LADR     [sp-5]               
  3952: DADR     4                    
  3953: DCP      4                    
  3954: ASP      1                    
  3955: LCP      [sp-3]               
  3956: ASP      1                    
  3957: XCALL    $frnd(float)float     ; args=1
  3958: LLD      [sp+5]               
  3959: SSP      1                    
  3960: FADD                          
  3961: LADR     [sp+1]               
  3962: PNT      4                    
  3963: ASGN                          
  3964: SSP      1                    
  3965: GCP      data[804]             ; = 198
  3966: LADR     [sp+1]               
  3967: XCALL    $SC_CreatePtc(unsignedlong,*c_Vector3)void ; args=2
  3968: SSP      2                    
  3969: LCP      [sp+0]               
  3970: LCP      [sp+0]               
  3971: GCP      data[805]             ; = 1
  3972: ADD                           
  3973: LADR     [sp+0]               
  3974: ASGN                          
  3975: SSP      1                    
  3976: SSP      1                    
  3977: JMP      label_3934           
label_3978:
  3978: GCP      data[806]             ; = 176
  3979: LCP      [sp-5]               
  3980: GCP      data[807]             ; = 1000.0f
  3981: GCP      data[808]             ; = 0.0f
  3982: GCP      data[809]             ; = 1.0f
  3983: GCP      data[810]             ; = 1.0f
  3984: XCALL    $SC_CreatePtcVec_Ext(unsignedlong,*c_Vector3,float,float,float,float)void ; args=6
  3985: SSP      6                    
  3986: RET      4                    
  3987: ASP      1                    
  3988: ASP      3                    
  3989: LADR     [sp-5]               
  3990: DADR     8                    
  3991: DCP      4                    
  3992: LADR     [sp+1]               
  3993: PNT      8                    
  3994: ASGN                          
  3995: SSP      1                    
  3996: GCP      data[811]             ; = 0.0f
  3997: LADR     [sp+0]               
  3998: ASGN                          
  3999: SSP      1                    
label_4000:
  4000: LCP      [sp+0]               
  4001: LCP      [sp-4]               
  4002: LES                           
  4003: JZ       label_4044           
  4004: LADR     [sp-5]               
  4005: DADR     0                    
  4006: DCP      4                    
  4007: ASP      1                    
  4008: LCP      [sp-3]               
  4009: ASP      1                    
  4010: XCALL    $frnd(float)float     ; args=1
  4011: LLD      [sp+5]               
  4012: SSP      1                    
  4013: FADD                          
  4014: LADR     [sp+1]               
  4015: ASGN                          
  4016: SSP      1                    
  4017: LADR     [sp-5]               
  4018: DADR     4                    
  4019: DCP      4                    
  4020: ASP      1                    
  4021: LCP      [sp-3]               
  4022: ASP      1                    
  4023: XCALL    $frnd(float)float     ; args=1
  4024: LLD      [sp+5]               
  4025: SSP      1                    
  4026: FADD                          
  4027: LADR     [sp+1]               
  4028: PNT      4                    
  4029: ASGN                          
  4030: SSP      1                    
  4031: GCP      data[812]             ; = 198
  4032: LADR     [sp+1]               
  4033: XCALL    $SC_CreatePtc(unsignedlong,*c_Vector3)void ; args=2
  4034: SSP      2                    
  4035: LCP      [sp+0]               
  4036: LCP      [sp+0]               
  4037: GCP      data[813]             ; = 1
  4038: ADD                           
  4039: LADR     [sp+0]               
  4040: ASGN                          
  4041: SSP      1                    
  4042: SSP      1                    
  4043: JMP      label_4000           
label_4044:
  4044: RET      4                    
  4045: ASP      3                    
  4046: ASP      32                   
  4047: LADR     [sp+3]               
  4048: GCP      data[814]             ; = 128
  4049: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  4050: SSP      2                    
  4051: LCP      [sp-3]               
  4052: LADR     [sp+3]               
  4053: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  4054: SSP      2                    
  4055: GCP      data[815]             ; = 1
  4056: LADR     [sp+3]               
  4057: PNT      76                   
  4058: ASGN                          
  4059: SSP      1                    
  4060: GCP      data[816]             ; = 4.0f
  4061: LADR     [sp+3]               
  4062: PNT      12                   
  4063: ASGN                          
  4064: SSP      1                    
  4065: LCP      [sp-3]               
  4066: LADR     [sp+3]               
  4067: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  4068: SSP      2                    
  4069: GCP      data[817]             ; = 0.9f
  4070: LADR     [sp+0]               
  4071: PNT      4                    
  4072: ASGN                          
  4073: SSP      1                    
  4074: GCP      data[818]             ; = 0.3f
  4075: LADR     [sp+0]               
  4076: ASGN                          
  4077: SSP      1                    
  4078: GCP      data[819]             ; = 0.5f
  4079: LADR     [sp+0]               
  4080: PNT      8                    
  4081: ASGN                          
  4082: SSP      1                    
  4083: LCP      [sp-3]               
  4084: LADR     [sp+0]               
  4085: XCALL    $SC_P_Ai_SetBattleProps(unsignedlong,*s_SC_P_Ai_BattleProps)void ; args=2
  4086: SSP      2                    
  4087: RET      35                   
  4088: ASP      3                    
  4089: ASP      1                    
  4090: LCP      [sp-4]               
  4091: LADR     [sp+0]               
  4092: XCALL    $SC_P_GetDir(unsignedlong,*c_Vector3)void ; args=2
  4093: SSP      2                    
  4094: ASP      1                    
  4095: LADR     [sp+0]               
  4096: ASP      1                    
  4097: XCALL    $SC_VectorLen(*c_Vector3)float ; args=1
  4098: LLD      [sp+4]               
  4099: SSP      1                    
  4100: LADR     [sp+3]               
  4101: ASGN                          
  4102: SSP      1                    
  4103: LCP      [sp+3]               
  4104: GCP      data[820]             ; = 1.0f
  4105: FGRE                          
  4106: JZ       label_4110           
  4107: GCP      data[821]             ; = 1
  4108: LLD      [sp-3]               
  4109: RET      4                    
label_4110:
  4110: GCP      data[822]             ; = 0.0f
  4111: LLD      [sp-3]               
  4112: RET      4                    
  4113: ASP      1                    
  4114: GCP      data[823]             ; = 9999.0f
  4115: ASP      1                    
  4116: ASP      3                    
  4117: GCP      data[824]             ; = 0.0f
  4118: LADR     [sp+0]               
  4119: ASGN                          
  4120: SSP      1                    
label_4121:
  4121: LCP      [sp+0]               
  4122: GCP      data[825]             ; = 6
  4123: LES                           
  4124: JZ       label_4177           
  4125: ASP      1                    
  4126: ASP      1                    
  4127: GCP      data[826]             ; = 0.0f
  4128: GCP      data[827]             ; = 0.0f
  4129: LCP      [sp+0]               
  4130: ASP      1                    
  4131: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  4132: LLD      [sp+7]               
  4133: SSP      3                    
  4134: ASP      1                    
  4135: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  4136: LLD      [sp+6]               
  4137: SSP      1                    
  4138: JZ       label_4168           
  4139: ASP      1                    
  4140: GCP      data[828]             ; = 0.0f
  4141: GCP      data[829]             ; = 0.0f
  4142: LCP      [sp+0]               
  4143: ASP      1                    
  4144: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  4145: LLD      [sp+6]               
  4146: SSP      3                    
  4147: LADR     [sp+3]               
  4148: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  4149: SSP      2                    
  4150: ASP      1                    
  4151: LADR     [sp+3]               
  4152: LCP      [sp-4]               
  4153: ASP      1                    
  4154: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  4155: LLD      [sp+6]               
  4156: SSP      2                    
  4157: LADR     [sp+2]               
  4158: ASGN                          
  4159: SSP      1                    
  4160: LCP      [sp+2]               
  4161: LCP      [sp+1]               
  4162: FLES                          
  4163: JZ       label_4168           
  4164: LCP      [sp+2]               
  4165: LADR     [sp+1]               
  4166: ASGN                          
  4167: SSP      1                    
label_4168:
  4168: LCP      [sp+0]               
  4169: LCP      [sp+0]               
  4170: GCP      data[830]             ; = 1
  4171: ADD                           
  4172: LADR     [sp+0]               
  4173: ASGN                          
  4174: SSP      1                    
  4175: SSP      1                    
  4176: JMP      label_4121           
label_4177:
  4177: LCP      [sp+1]               
  4178: LLD      [sp-3]               
  4179: RET      6                    
func_4180:
  4180: ASP      3                    
  4181: LCP      [sp-6]               
  4182: LADR     [sp+0]               
  4183: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  4184: SSP      2                    
  4185: ASP      1                    
  4186: LADR     [sp+0]               
  4187: LCP      [sp-5]               
  4188: LCP      [sp-4]               
  4189: ASP      1                    
  4190: XCALL    $SC_IsNear3D(*c_Vector3,*c_Vector3,float)int ; args=3
  4191: LLD      [sp+3]               
  4192: SSP      3                    
  4193: LLD      [sp-3]               
  4194: RET      3                    
  4195: ASP      3                    
  4196: ASP      1                    
  4197: LADR     [sp+0]               
  4198: ASP      1                    
  4199: XCALL    $SC_PC_GetPos(*c_Vector3)int ; args=1
  4200: LLD      [sp+3]               
  4201: SSP      1                    
  4202: SSP      1                    
  4203: ASP      1                    
  4204: LADR     [sp+0]               
  4205: LCP      [sp-5]               
  4206: LCP      [sp-4]               
  4207: ASP      1                    
  4208: XCALL    $SC_IsNear3D(*c_Vector3,*c_Vector3,float)int ; args=3
  4209: LLD      [sp+3]               
  4210: SSP      3                    
  4211: LLD      [sp-3]               
  4212: RET      3                    
  4213: ASP      32                   
  4214: LCP      [sp-7]               
  4215: JZ       label_4217           
  4216: JMP      label_4218           
label_4217:
  4217: RET      32                   
label_4218:
  4218: LADR     [sp+0]               
  4219: GCP      data[831]             ; = 128
  4220: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  4221: SSP      2                    
  4222: LCP      [sp-7]               
  4223: LADR     [sp+0]               
  4224: XCALL    $SC_P_Ai_GetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  4225: SSP      2                    
  4226: LCP      [sp-6]               
  4227: LADR     [sp+0]               
  4228: PNT      52                   
  4229: ASGN                          
  4230: SSP      1                    
  4231: LCP      [sp-5]               
  4232: LADR     [sp+0]               
  4233: PNT      56                   
  4234: ASGN                          
  4235: SSP      1                    
  4236: LCP      [sp-4]               
  4237: LADR     [sp+0]               
  4238: PNT      60                   
  4239: ASGN                          
  4240: SSP      1                    
  4241: LCP      [sp-3]               
  4242: LADR     [sp+0]               
  4243: PNT      64                   
  4244: ASGN                          
  4245: SSP      1                    
  4246: LCP      [sp-7]               
  4247: LADR     [sp+0]               
  4248: XCALL    $SC_P_Ai_SetProps(unsignedlong,*s_SC_P_AI_props)void ; args=2
  4249: SSP      2                    
  4250: RET      32                   
  4251: ASP      1                    
  4252: ASP      1                    
  4253: ASP      32                   
  4254: ASP      1                    
  4255: ASP      4                    
  4256: ASP      5                    
  4257: ASP      3                    
  4258: ASP      1                    
  4259: ASP      1                    
  4260: GCP      data[832]             ; = 10000.0f
  4261: LADR     [sp+47]              
  4262: ASGN                          
  4263: SSP      1                    
  4264: GCP      data[833]             ; = 1000.0f
  4265: LADR     [sp+35]              
  4266: PNT      12                   
  4267: ASGN                          
  4268: SSP      1                    
  4269: LCP      [sp-4]               
  4270: DCP      12                   
  4271: LADR     [sp+35]              
  4272: ASGN                          
  4273: SSP      3                    
  4274: GCP      data[834]             ; = 32
  4275: LADR     [sp+0]               
  4276: ASGN                          
  4277: SSP      1                    
  4278: LADR     [sp+35]              
  4279: LADR     [sp+2]               
  4280: LADR     [sp+0]               
  4281: XCALL    $SC_GetPls(*s_sphere,*unsignedlong,*unsignedlong)void ; args=3
  4282: SSP      3                    
  4283: GCP      data[835]             ; = 0.0f
  4284: LADR     [sp+34]              
  4285: ASGN                          
  4286: SSP      1                    
  4287: GCP      data[836]             ; = 0.0f
  4288: LADR     [sp+1]               
  4289: ASGN                          
  4290: SSP      1                    
label_4291:
  4291: LCP      [sp+1]               
  4292: LCP      [sp+0]               
  4293: LES                           
  4294: JZ       label_4373           
  4295: LADR     [sp+2]               
  4296: LCP      [sp+1]               
  4297: GCP      data[837]             ; = 4
  4298: MUL                           
  4299: ADD                           
  4300: DCP      4                    
  4301: LADR     [sp+39]              
  4302: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4303: SSP      2                    
  4304: LADR     [sp+39]              
  4305: PNT      8                    
  4306: DCP      4                    
  4307: LCP      [sp-5]               
  4308: EQU                           
  4309: JNZ      label_4315           
  4310: LCP      [sp-5]               
  4311: GCP      data[838]             ; = 100
  4312: EQU                           
  4313: JNZ      label_4315           
  4314: JMP      label_4364           
label_4315:
  4315: ASP      1                    
  4316: LADR     [sp+2]               
  4317: LCP      [sp+1]               
  4318: GCP      data[839]             ; = 4
  4319: MUL                           
  4320: ADD                           
  4321: DCP      4                    
  4322: ASP      1                    
  4323: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  4324: LLD      [sp+49]              
  4325: SSP      1                    
  4326: JZ       label_4364           
  4327: JMP      label_4328           
label_4328:
  4328: LADR     [sp+2]               
  4329: LCP      [sp+1]               
  4330: GCP      data[840]             ; = 4
  4331: MUL                           
  4332: ADD                           
  4333: DCP      4                    
  4334: LADR     [sp+44]              
  4335: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  4336: SSP      2                    
  4337: ASP      1                    
  4338: LADR     [sp+44]              
  4339: LCP      [sp-4]               
  4340: ASP      1                    
  4341: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  4342: LLD      [sp+49]              
  4343: SSP      2                    
  4344: LADR     [sp+48]              
  4345: ASGN                          
  4346: SSP      1                    
  4347: LCP      [sp+48]              
  4348: LCP      [sp+47]              
  4349: FLES                          
  4350: JZ       label_4364           
  4351: LCP      [sp+48]              
  4352: LADR     [sp+47]              
  4353: ASGN                          
  4354: SSP      1                    
  4355: LADR     [sp+2]               
  4356: LCP      [sp+1]               
  4357: GCP      data[841]             ; = 4
  4358: MUL                           
  4359: ADD                           
  4360: DCP      4                    
  4361: LADR     [sp+34]              
  4362: ASGN                          
  4363: SSP      1                    
label_4364:
  4364: LCP      [sp+1]               
  4365: LCP      [sp+1]               
  4366: GCP      data[842]             ; = 1
  4367: ADD                           
  4368: LADR     [sp+1]               
  4369: ASGN                          
  4370: SSP      1                    
  4371: SSP      1                    
  4372: JMP      label_4291           
label_4373:
  4373: LCP      [sp+34]              
  4374: LLD      [sp-3]               
  4375: RET      49                   
func_4376:
  4376: ASP      1                    
  4377: ASP      1                    
  4378: ASP      1                    
  4379: ASP      1                    
  4380: ASP      32                   
  4381: ASP      4                    
  4382: ASP      5                    
  4383: LCP      [sp-5]               
  4384: LADR     [sp+40]              
  4385: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4386: SSP      2                    
  4387: LADR     [sp+40]              
  4388: PNT      12                   
  4389: DCP      4                    
  4390: LADR     [sp+3]               
  4391: ASGN                          
  4392: SSP      1                    
  4393: LCP      [sp-5]               
  4394: LADR     [sp+36]              
  4395: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  4396: SSP      2                    
  4397: GCP      data[843]             ; = 1000.0f
  4398: LADR     [sp+36]              
  4399: PNT      12                   
  4400: ASGN                          
  4401: SSP      1                    
  4402: GCP      data[844]             ; = 32
  4403: LADR     [sp+0]               
  4404: ASGN                          
  4405: SSP      1                    
  4406: LADR     [sp+36]              
  4407: LADR     [sp+4]               
  4408: LADR     [sp+0]               
  4409: XCALL    $SC_GetPls(*s_sphere,*unsignedlong,*unsignedlong)void ; args=3
  4410: SSP      3                    
  4411: GCP      data[845]             ; = 0.0f
  4412: LADR     [sp+2]               
  4413: ASGN                          
  4414: SSP      1                    
  4415: GCP      data[846]             ; = 0.0f
  4416: LADR     [sp+1]               
  4417: ASGN                          
  4418: SSP      1                    
label_4419:
  4419: LCP      [sp+1]               
  4420: LCP      [sp+0]               
  4421: LES                           
  4422: JZ       label_4498           
  4423: LADR     [sp+4]               
  4424: LCP      [sp+1]               
  4425: GCP      data[847]             ; = 4
  4426: MUL                           
  4427: ADD                           
  4428: DCP      4                    
  4429: LADR     [sp+40]              
  4430: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4431: SSP      2                    
  4432: LADR     [sp+40]              
  4433: PNT      8                    
  4434: DCP      4                    
  4435: GCP      data[848]             ; = 1
  4436: EQU                           
  4437: JZ       label_4489           
  4438: LADR     [sp+40]              
  4439: PNT      12                   
  4440: DCP      4                    
  4441: LCP      [sp+3]               
  4442: EQU                           
  4443: JZ       label_4489           
  4444: JMP      label_4445           
label_4445:
  4445: ASP      1                    
  4446: LADR     [sp+4]               
  4447: LCP      [sp+1]               
  4448: GCP      data[849]             ; = 4
  4449: MUL                           
  4450: ADD                           
  4451: DCP      4                    
  4452: ASP      1                    
  4453: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  4454: LLD      [sp+45]              
  4455: SSP      1                    
  4456: JZ       label_4489           
  4457: JMP      label_4458           
label_4458:
  4458: LADR     [sp+4]               
  4459: LCP      [sp+1]               
  4460: GCP      data[850]             ; = 4
  4461: MUL                           
  4462: ADD                           
  4463: DCP      4                    
  4464: LCP      [sp-4]               
  4465: LCP      [sp+2]               
  4466: GCP      data[851]             ; = 4
  4467: MUL                           
  4468: ADD                           
  4469: ASGN                          
  4470: SSP      1                    
  4471: LCP      [sp+2]               
  4472: LCP      [sp+2]               
  4473: GCP      data[852]             ; = 1
  4474: ADD                           
  4475: LADR     [sp+2]               
  4476: ASGN                          
  4477: SSP      1                    
  4478: SSP      1                    
  4479: LCP      [sp+2]               
  4480: LCP      [sp-3]               
  4481: EQU                           
  4482: JZ       label_4489           
  4483: GCP      data[853]             ; = 3
  4484: GADR     data[854]            
  4485: GCP      data[866]             ; = 2
  4486: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  4487: SSP      2                    
  4488: RET      45                   
label_4489:
  4489: LCP      [sp+1]               
  4490: LCP      [sp+1]               
  4491: GCP      data[867]             ; = 1
  4492: ADD                           
  4493: LADR     [sp+1]               
  4494: ASGN                          
  4495: SSP      1                    
  4496: SSP      1                    
  4497: JMP      label_4419           
label_4498:
  4498: LCP      [sp+2]               
  4499: LCP      [sp-3]               
  4500: ASGN                          
  4501: SSP      1                    
  4502: RET      45                   
  4503: ASP      1                    
  4504: ASP      1                    
  4505: ASP      32                   
  4506: ASP      5                    
  4507: GCP      data[868]             ; = 32
  4508: LADR     [sp+0]               
  4509: ASGN                          
  4510: SSP      1                    
  4511: LCP      [sp-3]               
  4512: LADR     [sp+2]               
  4513: LADR     [sp+0]               
  4514: CALL     func_4376            
  4515: SSP      3                    
  4516: LCP      [sp-3]               
  4517: LADR     [sp+34]              
  4518: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4519: SSP      2                    
  4520: LCP      [sp+0]               
  4521: GCP      data[869]             ; = 2
  4522: LES                           
  4523: JZ       label_4539           
  4524: GCP      data[870]             ; = 3
  4525: GADR     data[871]            
  4526: LADR     [sp+34]              
  4527: PNT      12                   
  4528: DCP      4                    
  4529: LADR     [sp+34]              
  4530: PNT      16                   
  4531: DCP      4                    
  4532: LADR     [sp+34]              
  4533: PNT      12                   
  4534: DCP      4                    
  4535: GCP      data[883]             ; = 5
  4536: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  4537: SSP      5                    
  4538: RET      39                   
label_4539:
  4539: LADR     [sp+2]               
  4540: GCP      data[884]             ; = 0.0f
  4541: ADD                           
  4542: DCP      4                    
  4543: LCP      [sp-3]               
  4544: NEQ                           
  4545: JZ       label_4555           
  4546: LADR     [sp+2]               
  4547: GCP      data[885]             ; = 0.0f
  4548: ADD                           
  4549: DCP      4                    
  4550: GCP      data[886]             ; = 64
  4551: GCP      data[887]             ; = 0.0f
  4552: CALL     func_0354            
  4553: SSP      3                    
  4554: JMP      label_4563           
label_4555:
  4555: LADR     [sp+2]               
  4556: GCP      data[888]             ; = 4
  4557: ADD                           
  4558: DCP      4                    
  4559: GCP      data[889]             ; = 64
  4560: GCP      data[890]             ; = 0.0f
  4561: CALL     func_0354            
  4562: SSP      3                    
label_4563:
  4563: GCP      data[891]             ; = 3
  4564: GADR     data[892]  ; "VC %d %d moved command over group"
  4565: LADR     [sp+34]              
  4566: PNT      12                   
  4567: DCP      4                    
  4568: LADR     [sp+34]              
  4569: PNT      16                   
  4570: DCP      4                    
  4571: GCP      data[901]             ; = 4
  4572: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  4573: SSP      4                    
  4574: RET      39                   
func_4575:
  4575: ASP      3                    
  4576: ASP      1                    
  4577: LCP      [sp-5]               
  4578: LADR     [sp+0]               
  4579: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  4580: SSP      2                    
  4581: ASP      1                    
  4582: LCP      [sp-4]               
  4583: LADR     [sp+0]               
  4584: ASP      1                    
  4585: XCALL    $SC_2VectorsDist(*c_Vector3,*c_Vector3)float ; args=2
  4586: LLD      [sp+4]               
  4587: SSP      2                    
  4588: LADR     [sp+3]               
  4589: ASGN                          
  4590: SSP      1                    
  4591: LCP      [sp+3]               
  4592: LLD      [sp-3]               
  4593: RET      4                    
  4594: ASP      5                    
  4595: LADR     [sp+0]               
  4596: GCP      data[902]             ; = 20
  4597: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  4598: SSP      2                    
  4599: GCP      data[903]             ; = 0.0f
  4600: LADR     [sp+0]               
  4601: GCP      data[904]             ; = 0.0f
  4602: ADD                           
  4603: ASGN                          
  4604: SSP      1                    
  4605: GCP      data[905]             ; = 0.0f
  4606: LADR     [sp+0]               
  4607: GCP      data[906]             ; = 4
  4608: ADD                           
  4609: ASGN                          
  4610: SSP      1                    
  4611: GCP      data[907]             ; = 0.0f
  4612: LADR     [sp+0]               
  4613: GCP      data[908]             ; = 8
  4614: ADD                           
  4615: ASGN                          
  4616: SSP      1                    
  4617: GCP      data[909]             ; = 0.0f
  4618: LADR     [sp+0]               
  4619: GCP      data[910]             ; = 12
  4620: ADD                           
  4621: ASGN                          
  4622: SSP      1                    
  4623: GCP      data[911]             ; = 0.0f
  4624: LADR     [sp+0]               
  4625: GCP      data[912]             ; = 16
  4626: ADD                           
  4627: ASGN                          
  4628: SSP      1                    
  4629: LCP      [sp-3]               
  4630: LADR     [sp+0]               
  4631: XCALL    $SC_P_SetSpecAnims(unsignedlong,*s_SC_P_SpecAnims)void ; args=2
  4632: SSP      2                    
  4633: RET      5                    
  4634: ASP      5                    
  4635: LADR     [sp+0]               
  4636: GCP      data[913]             ; = 20
  4637: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  4638: SSP      2                    
  4639: LCP      [sp-7]               
  4640: LADR     [sp+0]               
  4641: GCP      data[914]             ; = 0.0f
  4642: ADD                           
  4643: ASGN                          
  4644: SSP      1                    
  4645: LCP      [sp-6]               
  4646: LADR     [sp+0]               
  4647: GCP      data[915]             ; = 4
  4648: ADD                           
  4649: ASGN                          
  4650: SSP      1                    
  4651: LCP      [sp-5]               
  4652: LADR     [sp+0]               
  4653: GCP      data[916]             ; = 8
  4654: ADD                           
  4655: ASGN                          
  4656: SSP      1                    
  4657: LCP      [sp-4]               
  4658: LADR     [sp+0]               
  4659: GCP      data[917]             ; = 12
  4660: ADD                           
  4661: ASGN                          
  4662: SSP      1                    
  4663: LCP      [sp-3]               
  4664: LADR     [sp+0]               
  4665: GCP      data[918]             ; = 16
  4666: ADD                           
  4667: ASGN                          
  4668: SSP      1                    
  4669: LCP      [sp-8]               
  4670: LADR     [sp+0]               
  4671: XCALL    $SC_P_SetSpecAnims(unsignedlong,*s_SC_P_SpecAnims)void ; args=2
  4672: SSP      2                    
  4673: RET      5                    
  4674: ASP      1                    
  4675: ASP      1                    
  4676: ASP      1                    
  4677: ASP      1                    
  4678: ASP      32                   
  4679: GCP      data[919]             ; = 32
  4680: LADR     [sp+0]               
  4681: ASGN                          
  4682: SSP      1                    
  4683: LCP      [sp-4]               
  4684: LADR     [sp+4]               
  4685: LADR     [sp+0]               
  4686: XCALL    $SC_GetPls(*s_sphere,*unsignedlong,*unsignedlong)void ; args=3
  4687: SSP      3                    
  4688: LCP      [sp+0]               
  4689: JZ       label_4691           
  4690: JMP      label_4692           
label_4691:
  4691: RET      36                   
label_4692:
  4692: GCP      data[920]             ; = 0.0f
  4693: LADR     [sp+1]               
  4694: ASGN                          
  4695: SSP      1                    
label_4696:
  4696: LCP      [sp+1]               
  4697: LCP      [sp+0]               
  4698: LES                           
  4699: JZ       label_4793           
  4700: LADR     [sp+4]               
  4701: LCP      [sp+1]               
  4702: GCP      data[921]             ; = 4
  4703: MUL                           
  4704: ADD                           
  4705: DCP      4                    
  4706: GCP      data[922]             ; = 0.0f
  4707: LCP      [sp-3]               
  4708: GCP      data[923]             ; = 7.0f
  4709: FDIV                          
  4710: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4711: SSP      3                    
  4712: LADR     [sp+4]               
  4713: LCP      [sp+1]               
  4714: GCP      data[924]             ; = 4
  4715: MUL                           
  4716: ADD                           
  4717: DCP      4                    
  4718: GCP      data[925]             ; = 1
  4719: LCP      [sp-3]               
  4720: GCP      data[926]             ; = 7.0f
  4721: FDIV                          
  4722: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4723: SSP      3                    
  4724: LADR     [sp+4]               
  4725: LCP      [sp+1]               
  4726: GCP      data[927]             ; = 4
  4727: MUL                           
  4728: ADD                           
  4729: DCP      4                    
  4730: GCP      data[928]             ; = 2
  4731: LCP      [sp-3]               
  4732: GCP      data[929]             ; = 7.0f
  4733: FDIV                          
  4734: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4735: SSP      3                    
  4736: LADR     [sp+4]               
  4737: LCP      [sp+1]               
  4738: GCP      data[930]             ; = 4
  4739: MUL                           
  4740: ADD                           
  4741: DCP      4                    
  4742: GCP      data[931]             ; = 3
  4743: LCP      [sp-3]               
  4744: GCP      data[932]             ; = 7.0f
  4745: FDIV                          
  4746: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4747: SSP      3                    
  4748: LADR     [sp+4]               
  4749: LCP      [sp+1]               
  4750: GCP      data[933]             ; = 4
  4751: MUL                           
  4752: ADD                           
  4753: DCP      4                    
  4754: GCP      data[934]             ; = 4
  4755: LCP      [sp-3]               
  4756: GCP      data[935]             ; = 7.0f
  4757: FDIV                          
  4758: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4759: SSP      3                    
  4760: LADR     [sp+4]               
  4761: LCP      [sp+1]               
  4762: GCP      data[936]             ; = 4
  4763: MUL                           
  4764: ADD                           
  4765: DCP      4                    
  4766: GCP      data[937]             ; = 5
  4767: LCP      [sp-3]               
  4768: GCP      data[938]             ; = 7.0f
  4769: FDIV                          
  4770: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4771: SSP      3                    
  4772: LADR     [sp+4]               
  4773: LCP      [sp+1]               
  4774: GCP      data[939]             ; = 4
  4775: MUL                           
  4776: ADD                           
  4777: DCP      4                    
  4778: GCP      data[940]             ; = 6
  4779: LCP      [sp-3]               
  4780: GCP      data[941]             ; = 7.0f
  4781: FDIV                          
  4782: XCALL    $SC_P_DoHit(unsignedlong,unsignedlong,float)void ; args=3
  4783: SSP      3                    
  4784: LCP      [sp+1]               
  4785: LCP      [sp+1]               
  4786: GCP      data[942]             ; = 1
  4787: ADD                           
  4788: LADR     [sp+1]               
  4789: ASGN                          
  4790: SSP      1                    
  4791: SSP      1                    
  4792: JMP      label_4696           
label_4793:
  4793: RET      36                   
  4794: ASP      4                    
  4795: LCP      [sp-4]               
  4796: LADR     [sp+0]               
  4797: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  4798: SSP      2                    
  4799: LADR     [sp+0]               
  4800: PNT      8                    
  4801: DCP      4                    
  4802: GCP      data[943]             ; = 1.0f
  4803: FADD                          
  4804: LADR     [sp+0]               
  4805: PNT      8                    
  4806: ASGN                          
  4807: SSP      1                    
  4808: GCP      data[944]             ; = 1.0f
  4809: LADR     [sp+0]               
  4810: PNT      12                   
  4811: ASGN                          
  4812: SSP      1                    
  4813: ASP      1                    
  4814: LADR     [sp+0]               
  4815: ASP      1                    
  4816: XCALL    $SC_SphereIsVisible(*s_sphere)int ; args=1
  4817: LLD      [sp+4]               
  4818: SSP      1                    
  4819: LLD      [sp-3]               
  4820: RET      4                    
  4821: ASP      5                    
  4822: LCP      [sp-4]               
  4823: LADR     [sp+0]               
  4824: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4825: SSP      2                    
  4826: LADR     [sp+0]               
  4827: PNT      8                    
  4828: DCP      4                    
  4829: LLD      [sp-3]               
  4830: RET      5                    
  4831: ASP      5                    
  4832: LCP      [sp-4]               
  4833: LADR     [sp+0]               
  4834: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4835: SSP      2                    
  4836: LADR     [sp+0]               
  4837: PNT      12                   
  4838: DCP      4                    
  4839: LLD      [sp-3]               
  4840: RET      5                    
  4841: ASP      5                    
  4842: LCP      [sp-4]               
  4843: LADR     [sp+0]               
  4844: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  4845: SSP      2                    
  4846: LADR     [sp+0]               
  4847: PNT      16                   
  4848: DCP      4                    
  4849: LLD      [sp-3]               
  4850: RET      5                    
  4851: ASP      1                    
  4852: GCP      data[974]             ; = 0.0f
  4853: LADR     [sp+0]               
  4854: ASGN                          
  4855: SSP      1                    
label_4856:
  4856: LCP      [sp+0]               
  4857: GCP      data[973]            
  4858: LES                           
  4859: JZ       label_4878           
  4860: GADR     data[953]            
  4861: LCP      [sp+0]               
  4862: GCP      data[975]             ; = 8
  4863: MUL                           
  4864: ADD                           
  4865: DCP      4                    
  4866: GCP      data[976]             ; = 0.0f
  4867: EQU                           
  4868: SSP      1                    
  4869: LCP      [sp+0]               
  4870: LCP      [sp+0]               
  4871: GCP      data[977]             ; = 1
  4872: ADD                           
  4873: LADR     [sp+0]               
  4874: ASGN                          
  4875: SSP      1                    
  4876: SSP      1                    
  4877: JMP      label_4856           
label_4878:
  4878: GCP      data[978]             ; = 0.0f
  4879: GADR     data[973]            
  4880: ASGN                          
  4881: SSP      1                    
  4882: RET      1                    
  4883: ASP      1                    
  4884: GCP      data[979]             ; = 0.0f
  4885: LADR     [sp+0]               
  4886: ASGN                          
  4887: SSP      1                    
label_4888:
  4888: LCP      [sp+0]               
  4889: GCP      data[973]            
  4890: LES                           
  4891: JZ       label_4917           
  4892: GADR     data[953]            
  4893: LCP      [sp+0]               
  4894: GCP      data[980]             ; = 8
  4895: MUL                           
  4896: ADD                           
  4897: DCP      4                    
  4898: LCP      [sp-3]               
  4899: EQU                           
  4900: JZ       label_4908           
  4901: GCP      data[981]             ; = 1
  4902: GADR     data[982]  ; "Duplicite objective added - %d"
  4903: LCP      [sp-3]               
  4904: GCP      data[990]             ; = 3
  4905: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  4906: SSP      3                    
  4907: RET      1                    
label_4908:
  4908: LCP      [sp+0]               
  4909: LCP      [sp+0]               
  4910: GCP      data[991]             ; = 1
  4911: ADD                           
  4912: LADR     [sp+0]               
  4913: ASGN                          
  4914: SSP      1                    
  4915: SSP      1                    
  4916: JMP      label_4888           
label_4917:
  4917: LCP      [sp-3]               
  4918: GADR     data[953]            
  4919: GCP      data[973]            
  4920: GCP      data[992]             ; = 8
  4921: MUL                           
  4922: ADD                           
  4923: ASGN                          
  4924: SSP      1                    
  4925: GCP      data[993]             ; = 0.0f
  4926: GADR     data[953]            
  4927: GCP      data[973]            
  4928: GCP      data[994]             ; = 8
  4929: MUL                           
  4930: ADD                           
  4931: PNT      4                    
  4932: ASGN                          
  4933: SSP      1                    
  4934: GCP      data[973]            
  4935: GCP      data[973]            
  4936: GCP      data[995]             ; = 1
  4937: ADD                           
  4938: GADR     data[973]            
  4939: ASGN                          
  4940: SSP      1                    
  4941: SSP      1                    
  4942: GCP      data[973]            
  4943: GADR     data[953]            
  4944: GCP      data[996]             ; = 6.0f
  4945: XCALL    $SC_SetObjectives(unsignedlong,*s_SC_Objective,float)void ; args=3
  4946: SSP      3                    
  4947: RET      1                    
func_4948:
  4948: ASP      1                    
  4949: GCP      data[997]             ; = 0.0f
  4950: LADR     [sp+0]               
  4951: ASGN                          
  4952: SSP      1                    
label_4953:
  4953: LCP      [sp+0]               
  4954: GCP      data[973]            
  4955: LES                           
  4956: JZ       label_4982           
  4957: GADR     data[953]            
  4958: LCP      [sp+0]               
  4959: GCP      data[998]             ; = 8
  4960: MUL                           
  4961: ADD                           
  4962: DCP      4                    
  4963: LCP      [sp-3]               
  4964: EQU                           
  4965: JZ       label_4973           
  4966: GCP      data[999]             ; = 1
  4967: GADR     data[1000]  ; "Duplicite objective added - %d"
  4968: LCP      [sp-3]               
  4969: GCP      data[1008]            ; = 3
  4970: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  4971: SSP      3                    
  4972: RET      1                    
label_4973:
  4973: LCP      [sp+0]               
  4974: LCP      [sp+0]               
  4975: GCP      data[1009]            ; = 1
  4976: ADD                           
  4977: LADR     [sp+0]               
  4978: ASGN                          
  4979: SSP      1                    
  4980: SSP      1                    
  4981: JMP      label_4953           
label_4982:
  4982: LCP      [sp-3]               
  4983: GADR     data[953]            
  4984: GCP      data[973]            
  4985: GCP      data[1010]            ; = 8
  4986: MUL                           
  4987: ADD                           
  4988: ASGN                          
  4989: SSP      1                    
  4990: GCP      data[1011]            ; = 0.0f
  4991: GADR     data[953]            
  4992: GCP      data[973]            
  4993: GCP      data[1012]            ; = 8
  4994: MUL                           
  4995: ADD                           
  4996: PNT      4                    
  4997: ASGN                          
  4998: SSP      1                    
  4999: GCP      data[973]            
  5000: GCP      data[973]            
  5001: GCP      data[1013]            ; = 1
  5002: ADD                           
  5003: GADR     data[973]            
  5004: ASGN                          
  5005: SSP      1                    
  5006: SSP      1                    
  5007: GCP      data[973]            
  5008: GADR     data[953]            
  5009: GCP      data[1014]            ; = 6.0f
  5010: XCALL    $SC_SetObjectivesNoSound(unsignedlong,*s_SC_Objective,float)void ; args=3
  5011: SSP      3                    
  5012: RET      1                    
  5013: ASP      1                    
  5014: GCP      data[1015]            ; = 0.0f
  5015: LADR     [sp+0]               
  5016: ASGN                          
  5017: SSP      1                    
label_5018:
  5018: LCP      [sp+0]               
  5019: GCP      data[973]            
  5020: LES                           
  5021: JZ       label_5066           
  5022: GADR     data[953]            
  5023: LCP      [sp+0]               
  5024: GCP      data[1016]            ; = 8
  5025: MUL                           
  5026: ADD                           
  5027: DCP      4                    
  5028: LCP      [sp-3]               
  5029: EQU                           
  5030: JZ       label_5057           
  5031: GADR     data[953]            
  5032: LCP      [sp+0]               
  5033: GCP      data[1017]            ; = 8
  5034: MUL                           
  5035: ADD                           
  5036: PNT      4                    
  5037: DCP      4                    
  5038: GCP      data[1018]            ; = 0.0f
  5039: EQU                           
  5040: JZ       label_5057           
  5041: JMP      label_5042           
label_5042:
  5042: GCP      data[1019]            ; = 2
  5043: GADR     data[953]            
  5044: LCP      [sp+0]               
  5045: GCP      data[1020]            ; = 8
  5046: MUL                           
  5047: ADD                           
  5048: PNT      4                    
  5049: ASGN                          
  5050: SSP      1                    
  5051: GCP      data[973]            
  5052: GADR     data[953]            
  5053: GCP      data[1021]            ; = 6.0f
  5054: XCALL    $SC_SetObjectives(unsignedlong,*s_SC_Objective,float)void ; args=3
  5055: SSP      3                    
  5056: RET      1                    
label_5057:
  5057: LCP      [sp+0]               
  5058: LCP      [sp+0]               
  5059: GCP      data[1022]            ; = 1
  5060: ADD                           
  5061: LADR     [sp+0]               
  5062: ASGN                          
  5063: SSP      1                    
  5064: SSP      1                    
  5065: JMP      label_5018           
label_5066:
  5066: RET      1                    
  5067: ASP      1                    
  5068: GCP      data[1023]            ; = 0.0f
  5069: LADR     [sp+0]               
  5070: ASGN                          
  5071: SSP      1                    
label_5072:
  5072: LCP      [sp+0]               
  5073: GCP      data[973]            
  5074: LES                           
  5075: JZ       label_5103           
  5076: GADR     data[953]            
  5077: LCP      [sp+0]               
  5078: GCP      data[1024]            ; = 8
  5079: MUL                           
  5080: ADD                           
  5081: DCP      4                    
  5082: LCP      [sp-3]               
  5083: EQU                           
  5084: JZ       label_5094           
  5085: GCP      data[1025]            ; = 1
  5086: GADR     data[953]            
  5087: LCP      [sp+0]               
  5088: GCP      data[1026]            ; = 8
  5089: MUL                           
  5090: ADD                           
  5091: PNT      4                    
  5092: ASGN                          
  5093: SSP      1                    
label_5094:
  5094: LCP      [sp+0]               
  5095: LCP      [sp+0]               
  5096: GCP      data[1027]            ; = 1
  5097: ADD                           
  5098: LADR     [sp+0]               
  5099: ASGN                          
  5100: SSP      1                    
  5101: SSP      1                    
  5102: JMP      label_5072           
label_5103:
  5103: GCP      data[973]            
  5104: GADR     data[953]            
  5105: GCP      data[1028]            ; = 6.0f
  5106: XCALL    $SC_SetObjectives(unsignedlong,*s_SC_Objective,float)void ; args=3
  5107: SSP      3                    
  5108: RET      1                    
  5109: ASP      1                    
  5110: GCP      data[1029]            ; = 0.0f
  5111: LADR     [sp+0]               
  5112: ASGN                          
  5113: SSP      1                    
label_5114:
  5114: LCP      [sp+0]               
  5115: GCP      data[973]            
  5116: LES                           
  5117: JZ       label_5145           
  5118: GADR     data[953]            
  5119: LCP      [sp+0]               
  5120: GCP      data[1030]            ; = 8
  5121: MUL                           
  5122: ADD                           
  5123: DCP      4                    
  5124: LCP      [sp-4]               
  5125: EQU                           
  5126: JZ       label_5136           
  5127: GADR     data[953]            
  5128: LCP      [sp+0]               
  5129: GCP      data[1031]            ; = 8
  5130: MUL                           
  5131: ADD                           
  5132: PNT      4                    
  5133: DCP      4                    
  5134: LLD      [sp-3]               
  5135: RET      1                    
label_5136:
  5136: LCP      [sp+0]               
  5137: LCP      [sp+0]               
  5138: GCP      data[1032]            ; = 1
  5139: ADD                           
  5140: LADR     [sp+0]               
  5141: ASGN                          
  5142: SSP      1                    
  5143: SSP      1                    
  5144: JMP      label_5114           
label_5145:
  5145: GCP      data[1033]            ; = 1
  5146: ASP      1                    
label_5147:
  5147: LCP      [sp+0]               
  5148: GCP      data[1034]            ; = 5
  5149: LES                           
  5150: JZ       label_5194           
  5151: ASP      1                    
  5152: ASP      1                    
  5153: GCP      data[1035]            ; = 0.0f
  5154: GCP      data[1036]            ; = 0.0f
  5155: LCP      [sp+0]               
  5156: ASP      1                    
  5157: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  5158: LLD      [sp+3]               
  5159: SSP      3                    
  5160: ASP      1                    
  5161: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  5162: LLD      [sp+2]               
  5163: SSP      1                    
  5164: JZ       label_5193           
  5165: JMP      label_5166           
label_5166:
  5166: ASP      1                    
  5167: ASP      1                    
  5168: GCP      data[1037]            ; = 0.0f
  5169: GCP      data[1038]            ; = 0.0f
  5170: LCP      [sp+0]               
  5171: ASP      1                    
  5172: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  5173: LLD      [sp+3]               
  5174: SSP      3                    
  5175: ASP      1                    
  5176: XCALL    $SC_P_Ai_GetPeaceMode(unsignedlong)unsignedlong ; args=1
  5177: LLD      [sp+2]               
  5178: SSP      1                    
  5179: LADR     [sp+1]               
  5180: ASGN                          
  5181: SSP      1                    
  5182: LCP      [sp+1]               
  5183: GCP      data[946]            
  5184: NEQ                           
  5185: JZ       label_5193           
  5186: LCP      [sp+1]               
  5187: GADR     data[946]            
  5188: ASGN                          
  5189: SSP      1                    
  5190: LCP      [sp+1]               
  5191: LLD      [sp-3]               
  5192: RET      2                    
label_5193:
  5193: JMP      label_5147           
label_5194:
  5194: GCP      data[1039]            ; = 0.0f
  5195: LLD      [sp-3]               
  5196: RET      2                    
func_5197:
  5197: GCP      data[1040]            ; = 1
  5198: GCP      data[1041]            ; = 0.0f
  5199: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  5200: SSP      2                    
  5201: GCP      data[1042]            ; = 2
  5202: GCP      data[1043]            ; = 0.0f
  5203: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  5204: SSP      2                    
  5205: GCP      data[1044]            ; = 6
  5206: GCP      data[1045]            ; = 0.0f
  5207: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  5208: SSP      2                    
  5209: GCP      data[1046]            ; = 4
  5210: GCP      data[1047]            ; = 0.0f
  5211: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  5212: SSP      2                    
  5213: GCP      data[1048]            ; = 3
  5214: GCP      data[1049]            ; = 0.0f
  5215: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  5216: SSP      2                    
  5217: GCP      data[1050]            ; = 8
  5218: GCP      data[1051]            ; = 0.0f
  5219: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  5220: SSP      2                    
  5221: GCP      data[1052]            ; = 2081
  5222: GCP      data[1053]            ; = 0.0f
  5223: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  5224: SSP      2                    
  5225: GCP      data[1054]            ; = 7
  5226: GCP      data[1055]            ; = 0.0f
  5227: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  5228: SSP      2                    
  5229: GCP      data[1056]            ; = 11
  5230: GCP      data[1057]            ; = 0.0f
  5231: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  5232: SSP      2                    
  5233: GCP      data[1058]            ; = 3
  5234: GADR     data[1059]  ; "Level difficulty is %d"
  5235: ASP      1                    
  5236: GCP      data[1065]            ; = 10
  5237: ASP      1                    
  5238: XCALL    $SC_ggi(unsignedlong)int ; args=1
  5239: LLD      [sp+2]               
  5240: SSP      1                    
  5241: GCP      data[1066]            ; = 3
  5242: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  5243: SSP      3                    
  5244: RET      0                    
  5245: ASP      30                   
  5246: ASP      6                    
  5247: ASP      6                    
  5248: ASP      1                    
  5249: LADR     [sp+0]               
  5250: GCP      data[1067]            ; = 120
  5251: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  5252: SSP      2                    
  5253: LADR     [sp+30]              
  5254: GCP      data[1068]            ; = 24
  5255: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  5256: SSP      2                    
  5257: LADR     [sp+36]              
  5258: GCP      data[1069]            ; = 24
  5259: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  5260: SSP      2                    
  5261: GCP      data[1070]            ; = 0.0f
  5262: LADR     [sp+0]               
  5263: GCP      data[1071]            ; = 0.0f
  5264: ADD                           
  5265: ASGN                          
  5266: SSP      1                    
  5267: GCP      data[1072]            ; = 5.0f
  5268: LADR     [sp+0]               
  5269: GCP      data[1073]            ; = 20
  5270: ADD                           
  5271: ASGN                          
  5272: SSP      1                    
  5273: GCP      data[1074]            ; = 1.5f
  5274: LADR     [sp+0]               
  5275: GCP      data[1075]            ; = 40
  5276: ADD                           
  5277: ASGN                          
  5278: SSP      1                    
  5279: GCP      data[1076]            ; = 1.5f
  5280: LADR     [sp+0]               
  5281: GCP      data[1077]            ; = 60
  5282: ADD                           
  5283: ASGN                          
  5284: SSP      1                    
  5285: GCP      data[1078]            ; = 2.0f
  5286: LADR     [sp+0]               
  5287: GCP      data[1079]            ; = 80
  5288: ADD                           
  5289: ASGN                          
  5290: SSP      1                    
  5291: GCP      data[1080]            ; = 0.0f
  5292: LADR     [sp+42]              
  5293: ASGN                          
  5294: SSP      1                    
label_5295:
  5295: LCP      [sp+42]              
  5296: GCP      data[1081]            ; = 5
  5297: LES                           
  5298: JZ       label_5363           
  5299: LADR     [sp+0]               
  5300: LCP      [sp+42]              
  5301: GCP      data[1082]            ; = 20
  5302: MUL                           
  5303: ADD                           
  5304: DCP      4                    
  5305: GCP      data[1083]            ; = 1.0f
  5306: FADD                          
  5307: LADR     [sp+0]               
  5308: LCP      [sp+42]              
  5309: GCP      data[1084]            ; = 20
  5310: MUL                           
  5311: ADD                           
  5312: PNT      4                    
  5313: ASGN                          
  5314: SSP      1                    
  5315: ASP      1                    
  5316: GCP      data[1085]            ; = 0.5f
  5317: ASP      1                    
  5318: XCALL    $frnd(float)float     ; args=1
  5319: LLD      [sp+43]              
  5320: SSP      1                    
  5321: LADR     [sp+0]               
  5322: LCP      [sp+42]              
  5323: GCP      data[1086]            ; = 20
  5324: MUL                           
  5325: ADD                           
  5326: PNT      8                    
  5327: ASGN                          
  5328: SSP      1                    
  5329: ASP      1                    
  5330: GCP      data[1087]            ; = 0.5f
  5331: ASP      1                    
  5332: XCALL    $frnd(float)float     ; args=1
  5333: LLD      [sp+43]              
  5334: SSP      1                    
  5335: LADR     [sp+0]               
  5336: LCP      [sp+42]              
  5337: GCP      data[1088]            ; = 20
  5338: MUL                           
  5339: ADD                           
  5340: PNT      8                    
  5341: PNT      4                    
  5342: ASGN                          
  5343: SSP      1                    
  5344: GCP      data[1089]            ; = 0.0f
  5345: LADR     [sp+0]               
  5346: LCP      [sp+42]              
  5347: GCP      data[1090]            ; = 20
  5348: MUL                           
  5349: ADD                           
  5350: PNT      8                    
  5351: PNT      8                    
  5352: ASGN                          
  5353: SSP      1                    
  5354: LCP      [sp+42]              
  5355: LCP      [sp+42]              
  5356: GCP      data[1091]            ; = 1
  5357: ADD                           
  5358: LADR     [sp+42]              
  5359: ASGN                          
  5360: SSP      1                    
  5361: SSP      1                    
  5362: JMP      label_5295           
label_5363:
  5363: GCP      data[1092]            ; = 1
  5364: LADR     [sp+30]              
  5365: GCP      data[1093]            ; = 0.0f
  5366: ADD                           
  5367: ASGN                          
  5368: SSP      1                    
  5369: GCP      data[1094]            ; = 4
  5370: LADR     [sp+30]              
  5371: GCP      data[1095]            ; = 4
  5372: ADD                           
  5373: ASGN                          
  5374: SSP      1                    
  5375: GCP      data[1096]            ; = 5
  5376: LADR     [sp+30]              
  5377: GCP      data[1097]            ; = 8
  5378: ADD                           
  5379: ASGN                          
  5380: SSP      1                    
  5381: GCP      data[1098]            ; = 2
  5382: LADR     [sp+30]              
  5383: GCP      data[1099]            ; = 12
  5384: ADD                           
  5385: ASGN                          
  5386: SSP      1                    
  5387: GCP      data[1100]            ; = 3
  5388: LADR     [sp+30]              
  5389: GCP      data[1101]            ; = 16
  5390: ADD                           
  5391: ASGN                          
  5392: SSP      1                    
  5393: GCP      data[1102]            ; = 1
  5394: LADR     [sp+36]              
  5395: GCP      data[1103]            ; = 0.0f
  5396: ADD                           
  5397: ASGN                          
  5398: SSP      1                    
  5399: GCP      data[1104]            ; = 5
  5400: LADR     [sp+36]              
  5401: GCP      data[1105]            ; = 4
  5402: ADD                           
  5403: ASGN                          
  5404: SSP      1                    
  5405: GCP      data[1106]            ; = 3
  5406: LADR     [sp+36]              
  5407: GCP      data[1107]            ; = 8
  5408: ADD                           
  5409: ASGN                          
  5410: SSP      1                    
  5411: GCP      data[1108]            ; = 4
  5412: LADR     [sp+36]              
  5413: GCP      data[1109]            ; = 12
  5414: ADD                           
  5415: ASGN                          
  5416: SSP      1                    
  5417: GCP      data[1110]            ; = 2
  5418: LADR     [sp+36]              
  5419: GCP      data[1111]            ; = 16
  5420: ADD                           
  5421: ASGN                          
  5422: SSP      1                    
  5423: GCP      data[1112]            ; = 0.0f
  5424: GCP      data[1113]            ; = 0.0f
  5425: GCP      data[1114]            ; = 0.0f
  5426: LADR     [sp+0]               
  5427: LADR     [sp+30]              
  5428: LADR     [sp+36]              
  5429: GCP      data[1115]            ; = 5
  5430: XCALL    $SC_Ai_SetPlFollow(unsignedlong,unsignedlong,unsignedlong,*s_SC_Ai_PlFollow,*unsignedlong,*unsignedlong,unsignedlong)void ; args=7
  5431: SSP      7                    
  5432: GCP      data[1116]            ; = 0.0f
  5433: LADR     [sp+0]               
  5434: GCP      data[1117]            ; = 0.0f
  5435: ADD                           
  5436: ASGN                          
  5437: SSP      1                    
  5438: GCP      data[1118]            ; = 4.0f
  5439: LADR     [sp+0]               
  5440: GCP      data[1119]            ; = 20
  5441: ADD                           
  5442: ASGN                          
  5443: SSP      1                    
  5444: GCP      data[1120]            ; = 1.5f
  5445: LADR     [sp+0]               
  5446: GCP      data[1121]            ; = 40
  5447: ADD                           
  5448: ASGN                          
  5449: SSP      1                    
  5450: GCP      data[1122]            ; = 1.5f
  5451: LADR     [sp+0]               
  5452: GCP      data[1123]            ; = 60
  5453: ADD                           
  5454: ASGN                          
  5455: SSP      1                    
  5456: GCP      data[1124]            ; = 1.5f
  5457: LADR     [sp+0]               
  5458: GCP      data[1125]            ; = 80
  5459: ADD                           
  5460: ASGN                          
  5461: SSP      1                    
  5462: GCP      data[1126]            ; = 2.0f
  5463: LADR     [sp+0]               
  5464: GCP      data[1127]            ; = 100
  5465: ADD                           
  5466: ASGN                          
  5467: SSP      1                    
  5468: GCP      data[1128]            ; = 0.0f
  5469: LADR     [sp+42]              
  5470: ASGN                          
  5471: SSP      1                    
label_5472:
  5472: LCP      [sp+42]              
  5473: GCP      data[1129]            ; = 6
  5474: LES                           
  5475: JZ       label_5548           
  5476: LADR     [sp+0]               
  5477: LCP      [sp+42]              
  5478: GCP      data[1130]            ; = 20
  5479: MUL                           
  5480: ADD                           
  5481: DCP      4                    
  5482: GCP      data[1131]            ; = 1.0f
  5483: FADD                          
  5484: LADR     [sp+0]               
  5485: LCP      [sp+42]              
  5486: GCP      data[1132]            ; = 20
  5487: MUL                           
  5488: ADD                           
  5489: PNT      4                    
  5490: ASGN                          
  5491: SSP      1                    
  5492: ASP      1                    
  5493: GCP      data[1133]            ; = 0.2f
  5494: ASP      1                    
  5495: XCALL    $frnd(float)float     ; args=1
  5496: LLD      [sp+43]              
  5497: SSP      1                    
  5498: LADR     [sp+0]               
  5499: LCP      [sp+42]              
  5500: GCP      data[1134]            ; = 20
  5501: MUL                           
  5502: ADD                           
  5503: PNT      8                    
  5504: ASGN                          
  5505: SSP      1                    
  5506: ASP      1                    
  5507: GCP      data[1135]            ; = 0.2f
  5508: ASP      1                    
  5509: XCALL    $frnd(float)float     ; args=1
  5510: LLD      [sp+43]              
  5511: SSP      1                    
  5512: LADR     [sp+0]               
  5513: LCP      [sp+42]              
  5514: GCP      data[1136]            ; = 20
  5515: MUL                           
  5516: ADD                           
  5517: PNT      8                    
  5518: PNT      4                    
  5519: ASGN                          
  5520: SSP      1                    
  5521: GCP      data[1137]            ; = 0.0f
  5522: LADR     [sp+0]               
  5523: LCP      [sp+42]              
  5524: GCP      data[1138]            ; = 20
  5525: MUL                           
  5526: ADD                           
  5527: PNT      8                    
  5528: PNT      8                    
  5529: ASGN                          
  5530: SSP      1                    
  5531: GCP      data[1139]            ; = 0.0f
  5532: LADR     [sp+36]              
  5533: LCP      [sp+42]              
  5534: GCP      data[1140]            ; = 4
  5535: MUL                           
  5536: ADD                           
  5537: ASGN                          
  5538: SSP      1                    
  5539: LCP      [sp+42]              
  5540: LCP      [sp+42]              
  5541: GCP      data[1141]            ; = 1
  5542: ADD                           
  5543: LADR     [sp+42]              
  5544: ASGN                          
  5545: SSP      1                    
  5546: SSP      1                    
  5547: JMP      label_5472           
label_5548:
  5548: GCP      data[1142]            ; = 0.0f
  5549: LADR     [sp+30]              
  5550: GCP      data[1143]            ; = 0.0f
  5551: ADD                           
  5552: ASGN                          
  5553: SSP      1                    
  5554: GCP      data[1144]            ; = 1
  5555: LADR     [sp+30]              
  5556: GCP      data[1145]            ; = 4
  5557: ADD                           
  5558: ASGN                          
  5559: SSP      1                    
  5560: GCP      data[1146]            ; = 4
  5561: LADR     [sp+30]              
  5562: GCP      data[1147]            ; = 8
  5563: ADD                           
  5564: ASGN                          
  5565: SSP      1                    
  5566: GCP      data[1148]            ; = 5
  5567: LADR     [sp+30]              
  5568: GCP      data[1149]            ; = 12
  5569: ADD                           
  5570: ASGN                          
  5571: SSP      1                    
  5572: GCP      data[1150]            ; = 2
  5573: LADR     [sp+30]              
  5574: GCP      data[1151]            ; = 16
  5575: ADD                           
  5576: ASGN                          
  5577: SSP      1                    
  5578: GCP      data[1152]            ; = 3
  5579: LADR     [sp+30]              
  5580: GCP      data[1153]            ; = 20
  5581: ADD                           
  5582: ASGN                          
  5583: SSP      1                    
  5584: GCP      data[1154]            ; = 0.0f
  5585: GCP      data[1155]            ; = 0.0f
  5586: GCP      data[1156]            ; = 1
  5587: LADR     [sp+0]               
  5588: LADR     [sp+30]              
  5589: LADR     [sp+36]              
  5590: GCP      data[1157]            ; = 6
  5591: XCALL    $SC_Ai_SetPlFollow(unsignedlong,unsignedlong,unsignedlong,*s_SC_Ai_PlFollow,*unsignedlong,*unsignedlong,unsignedlong)void ; args=7
  5592: SSP      7                    
  5593: RET      43                   
  5594: ASP      15                   
  5595: GCP      data[1158]            ; = 10.0f
  5596: XCALL    $SC_RadioSetDist(float)void ; args=1
  5597: SSP      1                    
  5598: RET      15                   
  5599: GCP      data[1159]            ; = 2.0f
  5600: ASP      1                    
  5601: GCP      data[951]            
  5602: JZ       label_5606           
  5603: GCP      data[1160]            ; = 0.0f
  5604: LLD      [sp-3]               
  5605: RET      2                    
label_5606:
  5606: ASP      1                    
  5607: GCP      data[1161]            ; = 0.0f
  5608: GCP      data[1162]            ; = 0.0f
  5609: GCP      data[1163]            ; = 4
  5610: ASP      1                    
  5611: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  5612: LLD      [sp+2]               
  5613: SSP      3                    
  5614: LADR     [sp+1]               
  5615: ASGN                          
  5616: SSP      1                    
  5617: LCP      [sp+1]               
  5618: JZ       label_5620           
  5619: JMP      label_5623           
label_5620:
  5620: GCP      data[1164]            ; = 0.0f
  5621: LLD      [sp-3]               
  5622: RET      2                    
label_5623:
  5623: ASP      1                    
  5624: LCP      [sp+1]               
  5625: ASP      1                    
  5626: XCALL    $SC_P_Ai_GetSureEnemies(unsignedlong)unsignedlong ; args=1
  5627: LLD      [sp+2]               
  5628: SSP      1                    
  5629: JZ       label_5631           
  5630: JMP      label_5642           
label_5631:
  5631: ASP      1                    
  5632: GCP      data[1165]            ; = 2
  5633: ASP      1                    
  5634: XCALL    $SC_ggi(unsignedlong)int ; args=1
  5635: LLD      [sp+2]               
  5636: SSP      1                    
  5637: JZ       label_5639           
  5638: JMP      label_5642           
label_5639:
  5639: GCP      data[1166]            ; = 0.0f
  5640: LLD      [sp-3]               
  5641: RET      2                    
label_5642:
  5642: GCP      data[1167]            ; = 1
  5643: GADR     data[951]            
  5644: ASGN                          
  5645: SSP      1                    
  5646: ASP      1                    
  5647: GCP      data[1168]            ; = 0.0f
  5648: GCP      data[1169]            ; = 0.0f
  5649: GCP      data[1170]            ; = 4
  5650: ASP      1                    
  5651: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  5652: LLD      [sp+2]               
  5653: SSP      3                    
  5654: GCP      data[1171]            ; = 4010
  5655: GCP      data[1172]            ; = 4010
  5656: LADR     [sp+0]               
  5657: XCALL    $SC_P_Speach(unsignedlong,unsignedlong,unsignedlong,*float)void ; args=4
  5658: SSP      4                    
  5659: LCP      [sp+0]               
  5660: GCP      data[1173]            ; = 1.0f
  5661: FADD                          
  5662: LADR     [sp+0]               
  5663: ASGN                          
  5664: SSP      1                    
  5665: GCP      data[1174]            ; = 5013
  5666: GCP      data[1175]            ; = 5013
  5667: LADR     [sp+0]               
  5668: XCALL    $SC_SpeachRadio(unsignedlong,unsignedlong,*float)void ; args=3
  5669: SSP      3                    
  5670: GCP      data[1176]            ; = 1
  5671: LLD      [sp-3]               
  5672: RET      2                    
  5673: ASP      1                    
  5674: GADR     data[953]            
  5675: GCP      data[1177]            ; = 0.0f
  5676: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  5677: SSP      2                    
  5678: GCP      data[1178]            ; = 0.0f
  5679: LADR     [sp+0]               
  5680: ASGN                          
  5681: SSP      1                    
label_5682:
  5682: LCP      [sp+0]               
  5683: GCP      data[1179]            ; = 0.0f
  5684: LES                           
  5685: JZ       label_5740           
  5686: GCP      data[1180]            ; = 0.0f
  5687: GADR     data[953]            
  5688: LCP      [sp+0]               
  5689: GCP      data[1181]            ; = 36
  5690: MUL                           
  5691: ADD                           
  5692: PNT      20                   
  5693: ASGN                          
  5694: SSP      1                    
  5695: GCP      data[1182]            ; = 1.0f
  5696: GADR     data[953]            
  5697: LCP      [sp+0]               
  5698: GCP      data[1183]            ; = 36
  5699: MUL                           
  5700: ADD                           
  5701: PNT      12                   
  5702: ASGN                          
  5703: SSP      1                    
  5704: GCP      data[1184]            ; = 1
  5705: GADR     data[953]            
  5706: LCP      [sp+0]               
  5707: GCP      data[1185]            ; = 36
  5708: MUL                           
  5709: ADD                           
  5710: PNT      16                   
  5711: ASGN                          
  5712: SSP      1                    
  5713: GCP      data[1186]            ; = 0.0f
  5714: GADR     data[953]            
  5715: LCP      [sp+0]               
  5716: GCP      data[1187]            ; = 36
  5717: MUL                           
  5718: ADD                           
  5719: PNT      28                   
  5720: ASGN                          
  5721: SSP      1                    
  5722: GCP      data[1188]            ; = 0.0f
  5723: GADR     data[953]            
  5724: LCP      [sp+0]               
  5725: GCP      data[1189]            ; = 36
  5726: MUL                           
  5727: ADD                           
  5728: PNT      32                   
  5729: ASGN                          
  5730: SSP      1                    
  5731: LCP      [sp+0]               
  5732: LCP      [sp+0]               
  5733: GCP      data[1190]            ; = 1
  5734: ADD                           
  5735: LADR     [sp+0]               
  5736: ASGN                          
  5737: SSP      1                    
  5738: SSP      1                    
  5739: JMP      label_5682           
label_5740:
  5740: RET      1                    
  5741: ASP      3                    
  5742: ASP      3                    
  5743: ASP      3                    
  5744: ASP      1                    
  5745: ASP      1                    
  5746: GCP      data[1191]            ; = 3
  5747: GADR     data[1192]  ; "adding trap on pos %d"
  5748: LCP      [sp-4]               
  5749: GCP      data[1198]            ; = 3
  5750: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  5751: SSP      3                    
  5752: GCP      data[1199]            ; = 2
  5753: GADR     data[953]            
  5754: LCP      [sp-4]               
  5755: GCP      data[1200]            ; = 36
  5756: MUL                           
  5757: ADD                           
  5758: PNT      16                   
  5759: ASGN                          
  5760: SSP      1                    
  5761: GCP      data[1201]            ; = 2
  5762: GADR     data[953]            
  5763: LCP      [sp-4]               
  5764: GCP      data[1202]            ; = 1
  5765: ADD                           
  5766: GCP      data[1203]            ; = 36
  5767: MUL                           
  5768: ADD                           
  5769: PNT      16                   
  5770: ASGN                          
  5771: SSP      1                    
  5772: LCP      [sp-4]               
  5773: GCP      data[1204]            ; = 1
  5774: ADD                           
  5775: GADR     data[953]            
  5776: LCP      [sp-4]               
  5777: GCP      data[1205]            ; = 36
  5778: MUL                           
  5779: ADD                           
  5780: PNT      24                   
  5781: ASGN                          
  5782: SSP      1                    
  5783: LCP      [sp-4]               
  5784: GADR     data[953]            
  5785: LCP      [sp-4]               
  5786: GCP      data[1206]            ; = 1
  5787: ADD                           
  5788: GCP      data[1207]            ; = 36
  5789: MUL                           
  5790: ADD                           
  5791: PNT      24                   
  5792: ASGN                          
  5793: SSP      1                    
  5794: GCP      data[1208]            ; = 4
  5795: GADR     data[953]            
  5796: LCP      [sp-4]               
  5797: GCP      data[1209]            ; = 36
  5798: MUL                           
  5799: ADD                           
  5800: PNT      28                   
  5801: ASGN                          
  5802: SSP      1                    
  5803: GCP      data[1210]            ; = 4
  5804: GADR     data[953]            
  5805: LCP      [sp-4]               
  5806: GCP      data[1211]            ; = 1
  5807: ADD                           
  5808: GCP      data[1212]            ; = 36
  5809: MUL                           
  5810: ADD                           
  5811: PNT      28                   
  5812: ASGN                          
  5813: SSP      1                    
  5814: ASP      1                    
  5815: LCP      [sp-3]               
  5816: GADR     data[1213]  ; "Plechovka"
  5817: ASP      1                    
  5818: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  5819: LLD      [sp+11]              
  5820: SSP      2                    
  5821: LADR     [sp+9]               
  5822: ASGN                          
  5823: SSP      1                    
  5824: LCP      [sp+9]               
  5825: JZ       label_5827           
  5826: JMP      label_5832           
label_5827:
  5827: GADR     data[1216]  ; "trap not found!!!"
  5828: GCP      data[1221]            ; = 1
  5829: XCALL    $SC_message(*char,...)void ; args=4294967295
  5830: SSP      1                    
  5831: RET      11                   
label_5832:
  5832: LCP      [sp+9]               
  5833: LADR     [sp+0]               
  5834: XCALL    $SC_NOD_GetWorldPos(*void,*c_Vector3)void ; args=2
  5835: SSP      2                    
  5836: ASP      1                    
  5837: LCP      [sp-3]               
  5838: GADR     data[1222]  ; "Konec dratu"
  5839: ASP      1                    
  5840: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  5841: LLD      [sp+11]              
  5842: SSP      2                    
  5843: LADR     [sp+9]               
  5844: ASGN                          
  5845: SSP      1                    
  5846: LCP      [sp+9]               
  5847: LADR     [sp+3]               
  5848: XCALL    $SC_NOD_GetWorldPos(*void,*c_Vector3)void ; args=2
  5849: SSP      2                    
  5850: LADR     [sp+3]               
  5851: DCP      4                    
  5852: LADR     [sp+0]               
  5853: DCP      4                    
  5854: FSUB                          
  5855: LADR     [sp+6]               
  5856: ASGN                          
  5857: SSP      1                    
  5858: LADR     [sp+3]               
  5859: PNT      4                    
  5860: DCP      4                    
  5861: LADR     [sp+0]               
  5862: PNT      4                    
  5863: DCP      4                    
  5864: FSUB                          
  5865: LADR     [sp+6]               
  5866: PNT      4                    
  5867: ASGN                          
  5868: SSP      1                    
  5869: LADR     [sp+3]               
  5870: PNT      8                    
  5871: DCP      4                    
  5872: LADR     [sp+0]               
  5873: PNT      8                    
  5874: DCP      4                    
  5875: FSUB                          
  5876: LADR     [sp+6]               
  5877: PNT      8                    
  5878: ASGN                          
  5879: SSP      1                    
  5880: GCP      data[1225]            ; = 3.0f
  5881: ASP      1                    
  5882: LADR     [sp+6]               
  5883: ASP      1                    
  5884: XCALL    $SC_VectorLen(*c_Vector3)float ; args=1
  5885: LLD      [sp+12]              
  5886: SSP      1                    
  5887: FMUL                          
  5888: FTOD                          
  5889: GADR     data[1226]           
  5890: DCP      8                    
  5891: DMUL                          
  5892: GADR     data[1228]           
  5893: DCP      8                    
  5894: DADD                          
  5895: DTOF                          
  5896: LADR     [sp+10]              
  5897: ASGN                          
  5898: SSP      1                    
  5899: LCP      [sp+10]              
  5900: GADR     data[953]            
  5901: LCP      [sp-4]               
  5902: GCP      data[1230]            ; = 36
  5903: MUL                           
  5904: ADD                           
  5905: PNT      12                   
  5906: ASGN                          
  5907: SSP      1                    
  5908: LCP      [sp+10]              
  5909: GADR     data[953]            
  5910: LCP      [sp-4]               
  5911: GCP      data[1231]            ; = 1
  5912: ADD                           
  5913: GCP      data[1232]            ; = 36
  5914: MUL                           
  5915: ADD                           
  5916: PNT      12                   
  5917: ASGN                          
  5918: SSP      1                    
  5919: LADR     [sp+0]               
  5920: DCP      4                    
  5921: GCP      data[1233]            ; = 1048576000
  5922: LADR     [sp+6]               
  5923: DCP      4                    
  5924: FMUL                          
  5925: FADD                          
  5926: GADR     data[953]            
  5927: LCP      [sp-4]               
  5928: GCP      data[1234]            ; = 36
  5929: MUL                           
  5930: ADD                           
  5931: ASGN                          
  5932: SSP      1                    
  5933: LADR     [sp+0]               
  5934: PNT      4                    
  5935: DCP      4                    
  5936: GCP      data[1235]            ; = 1048576000
  5937: LADR     [sp+6]               
  5938: PNT      4                    
  5939: DCP      4                    
  5940: FMUL                          
  5941: FADD                          
  5942: GADR     data[953]            
  5943: LCP      [sp-4]               
  5944: GCP      data[1236]            ; = 36
  5945: MUL                           
  5946: ADD                           
  5947: PNT      4                    
  5948: ASGN                          
  5949: SSP      1                    
  5950: LADR     [sp+0]               
  5951: PNT      8                    
  5952: DCP      4                    
  5953: GCP      data[1237]            ; = 1048576000
  5954: LADR     [sp+6]               
  5955: PNT      8                    
  5956: DCP      4                    
  5957: FMUL                          
  5958: FADD                          
  5959: GADR     data[953]            
  5960: LCP      [sp-4]               
  5961: GCP      data[1238]            ; = 36
  5962: MUL                           
  5963: ADD                           
  5964: PNT      8                    
  5965: ASGN                          
  5966: SSP      1                    
  5967: LADR     [sp+0]               
  5968: DCP      4                    
  5969: GCP      data[1239]            ; = 1061158912
  5970: LADR     [sp+6]               
  5971: DCP      4                    
  5972: FMUL                          
  5973: FADD                          
  5974: GADR     data[953]            
  5975: LCP      [sp-4]               
  5976: GCP      data[1240]            ; = 1
  5977: ADD                           
  5978: GCP      data[1241]            ; = 36
  5979: MUL                           
  5980: ADD                           
  5981: ASGN                          
  5982: SSP      1                    
  5983: LADR     [sp+0]               
  5984: PNT      4                    
  5985: DCP      4                    
  5986: GCP      data[1242]            ; = 1061158912
  5987: LADR     [sp+6]               
  5988: PNT      4                    
  5989: DCP      4                    
  5990: FMUL                          
  5991: FADD                          
  5992: GADR     data[953]            
  5993: LCP      [sp-4]               
  5994: GCP      data[1243]            ; = 1
  5995: ADD                           
  5996: GCP      data[1244]            ; = 36
  5997: MUL                           
  5998: ADD                           
  5999: PNT      4                    
  6000: ASGN                          
  6001: SSP      1                    
  6002: LADR     [sp+0]               
  6003: PNT      8                    
  6004: DCP      4                    
  6005: GCP      data[1245]            ; = 1061158912
  6006: LADR     [sp+6]               
  6007: PNT      8                    
  6008: DCP      4                    
  6009: FMUL                          
  6010: FADD                          
  6011: GADR     data[953]            
  6012: LCP      [sp-4]               
  6013: GCP      data[1246]            ; = 1
  6014: ADD                           
  6015: GCP      data[1247]            ; = 36
  6016: MUL                           
  6017: ADD                           
  6018: PNT      8                    
  6019: ASGN                          
  6020: SSP      1                    
  6021: RET      11                   
  6022: ASP      1                    
  6023: ASP      3                    
  6024: ASP      1                    
  6025: ASP      3                    
  6026: ASP      3                    
  6027: ASP      3                    
  6028: ASP      1                    
  6029: LCP      [sp-4]               
  6030: GADR     data[1248]  ; "Plechovka"
  6031: ASP      1                    
  6032: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  6033: LLD      [sp+14]              
  6034: SSP      2                    
  6035: LADR     [sp+4]               
  6036: ASGN                          
  6037: SSP      1                    
  6038: LCP      [sp+4]               
  6039: JZ       label_6041           
  6040: JMP      label_6048           
label_6041:
  6041: GADR     data[1251]  ; "trap not found!!!"
  6042: GCP      data[1256]            ; = 1
  6043: XCALL    $SC_message(*char,...)void ; args=4294967295
  6044: SSP      1                    
  6045: GCP      data[1257]            ; = -1
  6046: LLD      [sp-3]               
  6047: RET      14                   
label_6048:
  6048: LCP      [sp+4]               
  6049: LADR     [sp+5]               
  6050: XCALL    $SC_NOD_GetWorldPos(*void,*c_Vector3)void ; args=2
  6051: SSP      2                    
  6052: ASP      1                    
  6053: LCP      [sp-4]               
  6054: GADR     data[1258]           
  6055: ASP      1                    
  6056: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  6057: LLD      [sp+14]              
  6058: SSP      2                    
  6059: LADR     [sp+4]               
  6060: ASGN                          
  6061: SSP      1                    
  6062: LCP      [sp+4]               
  6063: LADR     [sp+8]               
  6064: XCALL    $SC_NOD_GetWorldPos(*void,*c_Vector3)void ; args=2
  6065: SSP      2                    
  6066: LADR     [sp+8]               
  6067: DCP      4                    
  6068: LADR     [sp+5]               
  6069: DCP      4                    
  6070: FSUB                          
  6071: LADR     [sp+11]              
  6072: ASGN                          
  6073: SSP      1                    
  6074: LADR     [sp+8]               
  6075: PNT      4                    
  6076: DCP      4                    
  6077: LADR     [sp+5]               
  6078: PNT      4                    
  6079: DCP      4                    
  6080: FSUB                          
  6081: LADR     [sp+11]              
  6082: PNT      4                    
  6083: ASGN                          
  6084: SSP      1                    
  6085: LADR     [sp+8]               
  6086: PNT      8                    
  6087: DCP      4                    
  6088: LADR     [sp+5]               
  6089: PNT      8                    
  6090: DCP      4                    
  6091: FSUB                          
  6092: GCP      data[1261]            ; = 10000.0f
  6093: FADD                          
  6094: LADR     [sp+11]              
  6095: PNT      8                    
  6096: ASGN                          
  6097: SSP      1                    
  6098: LADR     [sp+5]               
  6099: DCP      4                    
  6100: GCP      data[1262]            ; = 1048576000
  6101: LADR     [sp+11]              
  6102: DCP      4                    
  6103: FMUL                          
  6104: FADD                          
  6105: LADR     [sp+1]               
  6106: ASGN                          
  6107: SSP      1                    
  6108: LADR     [sp+5]               
  6109: PNT      4                    
  6110: DCP      4                    
  6111: GCP      data[1263]            ; = 1048576000
  6112: LADR     [sp+11]              
  6113: PNT      4                    
  6114: DCP      4                    
  6115: FMUL                          
  6116: FADD                          
  6117: LADR     [sp+1]               
  6118: PNT      4                    
  6119: ASGN                          
  6120: SSP      1                    
  6121: LADR     [sp+5]               
  6122: PNT      8                    
  6123: DCP      4                    
  6124: GCP      data[1264]            ; = 1048576000
  6125: LADR     [sp+11]              
  6126: PNT      8                    
  6127: DCP      4                    
  6128: FMUL                          
  6129: FADD                          
  6130: LADR     [sp+1]               
  6131: PNT      8                    
  6132: ASGN                          
  6133: SSP      1                    
  6134: GCP      data[1265]            ; = 0.0f
  6135: LADR     [sp+0]               
  6136: ASGN                          
  6137: SSP      1                    
label_6138:
  6138: LCP      [sp+0]               
  6139: GCP      data[1266]            ; = 0.0f
  6140: LES                           
  6141: JZ       label_6193           
  6142: ASP      1                    
  6143: GADR     data[953]            
  6144: LCP      [sp+0]               
  6145: GCP      data[1267]            ; = 36
  6146: MUL                           
  6147: ADD                           
  6148: LADR     [sp+1]               
  6149: GCP      data[1268]            ; = 1.0f
  6150: ASP      1                    
  6151: XCALL    $SC_IsNear2D(*c_Vector3,*c_Vector3,float)int ; args=3
  6152: LLD      [sp+14]              
  6153: SSP      3                    
  6154: JZ       label_6184           
  6155: GCP      data[1269]            ; = 1
  6156: GADR     data[953]            
  6157: LCP      [sp+0]               
  6158: GCP      data[1270]            ; = 36
  6159: MUL                           
  6160: ADD                           
  6161: PNT      20                   
  6162: ASGN                          
  6163: SSP      1                    
  6164: GCP      data[1271]            ; = 1
  6165: GADR     data[953]            
  6166: LCP      [sp+0]               
  6167: GCP      data[1272]            ; = 1
  6168: ADD                           
  6169: GCP      data[1273]            ; = 36
  6170: MUL                           
  6171: ADD                           
  6172: PNT      20                   
  6173: ASGN                          
  6174: SSP      1                    
  6175: GCP      data[1274]            ; = 3
  6176: GADR     data[1275]  ; "removing trap %d"
  6177: LCP      [sp+0]               
  6178: GCP      data[1280]            ; = 3
  6179: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  6180: SSP      3                    
  6181: LCP      [sp+0]               
  6182: LLD      [sp-3]               
  6183: RET      14                   
label_6184:
  6184: LCP      [sp+0]               
  6185: LCP      [sp+0]               
  6186: GCP      data[1281]            ; = 1
  6187: ADD                           
  6188: LADR     [sp+0]               
  6189: ASGN                          
  6190: SSP      1                    
  6191: SSP      1                    
  6192: JMP      label_6138           
label_6193:
  6193: GCP      data[1282]            ; = -1
  6194: LLD      [sp-3]               
  6195: RET      14                   
func_6196:
  6196: LCP      [sp-4]               
  6197: JMP      label_6199           
  6198: JMP      label_6203           
label_6199:
  6199: LCP      [sp+0]               
  6200: GCP      data[1283]            ; = 0.0f
  6201: EQU                           
  6202: JZ       label_6207           
label_6203:
  6203: GCP      data[1284]            ; = 1
  6204: LLD      [sp-3]               
  6205: RET      1                    
  6206: JMP      label_6211           
label_6207:
  6207: LCP      [sp+0]               
  6208: GCP      data[1285]            ; = 1
  6209: EQU                           
  6210: JZ       label_6219           
label_6211:
  6211: LCP      [sp-5]               
  6212: JZ       label_6214           
  6213: JMP      label_6217           
label_6214:
  6214: GCP      data[1286]            ; = 1
  6215: LLD      [sp-3]               
  6216: RET      1                    
label_6217:
  6217: JMP      label_6255           
  6218: JMP      label_6223           
label_6219:
  6219: LCP      [sp+0]               
  6220: GCP      data[1287]            ; = 2
  6221: EQU                           
  6222: JZ       label_6232           
label_6223:
  6223: LCP      [sp-5]               
  6224: GCP      data[1288]            ; = 1
  6225: EQU                           
  6226: JZ       label_6230           
  6227: GCP      data[1289]            ; = 1
  6228: LLD      [sp-3]               
  6229: RET      1                    
label_6230:
  6230: JMP      label_6255           
  6231: JMP      label_6236           
label_6232:
  6232: LCP      [sp+0]               
  6233: GCP      data[1290]            ; = 3
  6234: EQU                           
  6235: JZ       label_6245           
label_6236:
  6236: LCP      [sp-5]               
  6237: GCP      data[1291]            ; = 2
  6238: LES                           
  6239: JZ       label_6243           
  6240: GCP      data[1292]            ; = 1
  6241: LLD      [sp-3]               
  6242: RET      1                    
label_6243:
  6243: JMP      label_6255           
  6244: JMP      label_6249           
label_6245:
  6245: LCP      [sp+0]               
  6246: GCP      data[1293]            ; = 4
  6247: EQU                           
  6248: JZ       label_6255           
label_6249:
  6249: LCP      [sp-5]               
  6250: JZ       label_6254           
  6251: GCP      data[1294]            ; = 1
  6252: LLD      [sp-3]               
  6253: RET      1                    
label_6254:
  6254: JMP      label_6255           
label_6255:
  6255: SSP      1                    
  6256: GCP      data[1295]            ; = 0.0f
  6257: LLD      [sp-3]               
  6258: RET      0                    
func_6259:
  6259: ASP      1                    
  6260: ASP      1                    
  6261: GCP      data[1296]            ; = 0.0f
  6262: GCP      data[1297]            ; = 0.0f
  6263: GCP      data[1298]            ; = 1
  6264: ASP      1                    
  6265: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  6266: LLD      [sp+1]               
  6267: SSP      3                    
  6268: ASP      1                    
  6269: XCALL    $SC_P_Ai_GetPeaceMode(unsignedlong)unsignedlong ; args=1
  6270: LLD      [sp+0]               
  6271: SSP      1                    
  6272: GCP      data[1299]            ; = 2
  6273: EQU                           
  6274: JZ       label_6284           
  6275: GCP      data[1300]            ; = 0.0f
  6276: GCP      data[1301]            ; = 0.0f
  6277: GCP      data[1302]            ; = 0.0f
  6278: XCALL    $SC_Ai_SetPeaceMode(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  6279: SSP      3                    
  6280: GCP      data[1303]            ; = 0.0f
  6281: GCP      data[1304]            ; = 0.0f
  6282: XCALL    $SC_Ai_PointStopDanger(unsignedlong,unsignedlong)void ; args=2
  6283: SSP      2                    
label_6284:
  6284: RET      0                    
  6285: ASP      1                    
  6286: ASP      1                    
  6287: ASP      1                    
  6288: ASP      1                    
  6289: ASP      1                    
  6290: ASP      1                    
  6291: ASP      3                    
  6292: GCP      data[1305]            ; = 0.0f
  6293: GADR     data[948]            
  6294: ASGN                          
  6295: SSP      1                    
  6296: GCP      data[947]            
  6297: LADR     [sp+5]               
  6298: ASGN                          
  6299: SSP      1                    
  6300: GCP      data[1306]            ; = 0.0f
  6301: LADR     [sp+1]               
  6302: ASGN                          
  6303: SSP      1                    
label_6304:
  6304: LCP      [sp+1]               
  6305: GCP      data[1307]            ; = 6
  6306: LES                           
  6307: JZ       label_6633           
  6308: ASP      1                    
  6309: GCP      data[1308]            ; = 0.0f
  6310: GCP      data[1309]            ; = 0.0f
  6311: LCP      [sp+1]               
  6312: ASP      1                    
  6313: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  6314: LLD      [sp+9]               
  6315: SSP      3                    
  6316: LADR     [sp+3]               
  6317: ASGN                          
  6318: SSP      1                    
  6319: ASP      1                    
  6320: LCP      [sp+3]               
  6321: ASP      1                    
  6322: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  6323: LLD      [sp+9]               
  6324: SSP      1                    
  6325: JZ       label_6624           
  6326: LCP      [sp+3]               
  6327: LADR     [sp+6]               
  6328: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  6329: SSP      2                    
  6330: GCP      data[1310]            ; = 0.0f
  6331: LADR     [sp+0]               
  6332: ASGN                          
  6333: SSP      1                    
label_6334:
  6334: LCP      [sp+0]               
  6335: GCP      data[1311]            ; = 0.0f
  6336: LES                           
  6337: JZ       label_6624           
  6338: GADR     data[953]            
  6339: LCP      [sp+0]               
  6340: GCP      data[1312]            ; = 36
  6341: MUL                           
  6342: ADD                           
  6343: PNT      20                   
  6344: DCP      4                    
  6345: JZ       label_6347           
  6346: JMP      label_6615           
label_6347:
  6347: ASP      1                    
  6348: GADR     data[953]            
  6349: LCP      [sp+0]               
  6350: GCP      data[1313]            ; = 36
  6351: MUL                           
  6352: ADD                           
  6353: LADR     [sp+6]               
  6354: GADR     data[953]            
  6355: LCP      [sp+0]               
  6356: GCP      data[1314]            ; = 36
  6357: MUL                           
  6358: ADD                           
  6359: PNT      12                   
  6360: DCP      4                    
  6361: ASP      1                    
  6362: XCALL    $SC_IsNear3D(*c_Vector3,*c_Vector3,float)int ; args=3
  6363: LLD      [sp+9]               
  6364: SSP      3                    
  6365: JZ       label_6615           
  6366: JMP      label_6367           
label_6367:
  6367: ASP      1                    
  6368: LCP      [sp+1]               
  6369: GADR     data[953]            
  6370: LCP      [sp+0]               
  6371: GCP      data[1315]            ; = 36
  6372: MUL                           
  6373: ADD                           
  6374: PNT      28                   
  6375: DCP      4                    
  6376: ASP      1                    
  6377: CALL     func_6196            
  6378: LLD      [sp+9]               
  6379: SSP      2                    
  6380: JZ       label_6615           
  6381: JMP      label_6382           
label_6382:
  6382: GADR     data[953]            
  6383: LCP      [sp+0]               
  6384: GCP      data[1316]            ; = 36
  6385: MUL                           
  6386: ADD                           
  6387: PNT      16                   
  6388: DCP      4                    
  6389: JMP      label_6391           
  6390: JMP      label_6395           
label_6391:
  6391: LCP      [sp+9]               
  6392: GCP      data[1317]            ; = 1
  6393: EQU                           
  6394: JZ       label_6397           
label_6395:
  6395: JMP      label_6566           
  6396: JMP      label_6401           
label_6397:
  6397: LCP      [sp+9]               
  6398: GCP      data[1318]            ; = 2
  6399: EQU                           
  6400: JZ       label_6443           
label_6401:
  6401: GCP      data[1319]            ; = 0.0f
  6402: LADR     [sp+2]               
  6403: ASGN                          
  6404: SSP      1                    
  6405: GCP      data[952]            
  6406: JZ       label_6413           
  6407: LCP      [sp+3]               
  6408: GCP      data[1320]            ; = 4
  6409: GCP      data[1321]            ; = 1
  6410: XCALL    $SC_P_ScriptMessage(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  6411: SSP      3                    
  6412: JMP      label_6418           
label_6413:
  6413: LCP      [sp+3]               
  6414: GCP      data[1322]            ; = 4
  6415: GCP      data[1323]            ; = 0.0f
  6416: XCALL    $SC_P_ScriptMessage(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  6417: SSP      3                    
label_6418:
  6418: GCP      data[1324]            ; = 1
  6419: GADR     data[952]            
  6420: ASGN                          
  6421: SSP      1                    
  6422: GCP      data[1325]            ; = 1
  6423: GADR     data[947]            
  6424: ASGN                          
  6425: SSP      1                    
  6426: GCP      data[1326]            ; = 1
  6427: GADR     data[953]            
  6428: GADR     data[953]            
  6429: LCP      [sp+0]               
  6430: GCP      data[1327]            ; = 36
  6431: MUL                           
  6432: ADD                           
  6433: PNT      24                   
  6434: DCP      4                    
  6435: GCP      data[1328]            ; = 36
  6436: MUL                           
  6437: ADD                           
  6438: PNT      20                   
  6439: ASGN                          
  6440: SSP      1                    
  6441: JMP      label_6566           
  6442: JMP      label_6447           
label_6443:
  6443: LCP      [sp+9]               
  6444: GCP      data[1329]            ; = 3
  6445: EQU                           
  6446: JZ       label_6484           
label_6447:
  6447: GCP      data[1330]            ; = 0.0f
  6448: LADR     [sp+2]               
  6449: ASGN                          
  6450: SSP      1                    
  6451: LCP      [sp+1]               
  6452: GCP      data[1331]            ; = 1
  6453: EQU                           
  6454: JZ       label_6471           
  6455: LCP      [sp+3]               
  6456: GCP      data[1332]            ; = 4062
  6457: LADR     [sp+2]               
  6458: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  6459: SSP      3                    
  6460: LCP      [sp+2]               
  6461: GCP      data[1333]            ; = 0.1f
  6462: FADD                          
  6463: LADR     [sp+2]               
  6464: ASGN                          
  6465: SSP      1                    
  6466: GCP      data[1334]            ; = 20
  6467: GADR     data[947]            
  6468: ASGN                          
  6469: SSP      1                    
  6470: JMP      label_6482           
label_6471:
  6471: LCP      [sp+3]               
  6472: GCP      data[1335]            ; = 4061
  6473: LADR     [sp+2]               
  6474: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  6475: SSP      3                    
  6476: LCP      [sp+2]               
  6477: GCP      data[1336]            ; = 0.1f
  6478: FADD                          
  6479: LADR     [sp+2]               
  6480: ASGN                          
  6481: SSP      1                    
label_6482:
  6482: JMP      label_6566           
  6483: JMP      label_6488           
label_6484:
  6484: LCP      [sp+9]               
  6485: GCP      data[1337]            ; = 4
  6486: EQU                           
  6487: JZ       label_6514           
label_6488:
  6488: GCP      data[1338]            ; = 0.0f
  6489: LADR     [sp+2]               
  6490: ASGN                          
  6491: SSP      1                    
  6492: LCP      [sp+1]               
  6493: GCP      data[1339]            ; = 1
  6494: EQU                           
  6495: JZ       label_6512           
  6496: LCP      [sp+3]               
  6497: GCP      data[950]             ; = 0.0f
  6498: LADR     [sp+2]               
  6499: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  6500: SSP      3                    
  6501: LCP      [sp+2]               
  6502: GCP      data[1340]            ; = 0.1f
  6503: FADD                          
  6504: LADR     [sp+2]               
  6505: ASGN                          
  6506: SSP      1                    
  6507: CALL     func_6259            
  6508: GCP      data[1341]            ; = 2
  6509: GADR     data[947]            
  6510: ASGN                          
  6511: SSP      1                    
label_6512:
  6512: JMP      label_6566           
  6513: JMP      label_6518           
label_6514:
  6514: LCP      [sp+9]               
  6515: GCP      data[1342]            ; = 5
  6516: EQU                           
  6517: JZ       label_6540           
label_6518:
  6518: GCP      data[1343]            ; = 0.0f
  6519: LADR     [sp+2]               
  6520: ASGN                          
  6521: SSP      1                    
  6522: LCP      [sp+1]               
  6523: GCP      data[1344]            ; = 2
  6524: EQU                           
  6525: JZ       label_6537           
  6526: LCP      [sp+3]               
  6527: GCP      data[1345]            ; = 4884
  6528: LADR     [sp+2]               
  6529: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  6530: SSP      3                    
  6531: LCP      [sp+2]               
  6532: GCP      data[1346]            ; = 0.1f
  6533: FADD                          
  6534: LADR     [sp+2]               
  6535: ASGN                          
  6536: SSP      1                    
label_6537:
  6537: CALL     func_6259            
  6538: JMP      label_6566           
  6539: JMP      label_6544           
label_6540:
  6540: LCP      [sp+9]               
  6541: GCP      data[1347]            ; = 10
  6542: EQU                           
  6543: JZ       label_6566           
label_6544:
  6544: GCP      data[952]            
  6545: JZ       label_6552           
  6546: LCP      [sp+3]               
  6547: GCP      data[1348]            ; = 4
  6548: GCP      data[1349]            ; = 1
  6549: XCALL    $SC_P_ScriptMessage(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  6550: SSP      3                    
  6551: JMP      label_6557           
label_6552:
  6552: LCP      [sp+3]               
  6553: GCP      data[1350]            ; = 4
  6554: GCP      data[1351]            ; = 0.0f
  6555: XCALL    $SC_P_ScriptMessage(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  6556: SSP      3                    
label_6557:
  6557: GCP      data[1352]            ; = 1
  6558: GADR     data[952]            
  6559: ASGN                          
  6560: SSP      1                    
  6561: GCP      data[1353]            ; = 10
  6562: GADR     data[947]            
  6563: ASGN                          
  6564: SSP      1                    
  6565: JMP      label_6566           
label_6566:
  6566: SSP      1                    
  6567: GADR     data[953]            
  6568: LCP      [sp+0]               
  6569: GCP      data[1354]            ; = 36
  6570: MUL                           
  6571: ADD                           
  6572: PNT      16                   
  6573: DCP      4                    
  6574: GADR     data[948]            
  6575: ASGN                          
  6576: SSP      1                    
  6577: LCP      [sp+1]               
  6578: GADR     data[949]            
  6579: ASGN                          
  6580: SSP      1                    
  6581: ASP      1                    
  6582: LCP      [sp+1]               
  6583: GADR     data[953]            
  6584: LCP      [sp+0]               
  6585: GCP      data[1355]            ; = 36
  6586: MUL                           
  6587: ADD                           
  6588: PNT      32                   
  6589: DCP      4                    
  6590: ASP      1                    
  6591: CALL     func_6196            
  6592: LLD      [sp+9]               
  6593: SSP      2                    
  6594: JZ       label_6604           
  6595: GCP      data[1356]            ; = 1
  6596: GADR     data[953]            
  6597: LCP      [sp+0]               
  6598: GCP      data[1357]            ; = 36
  6599: MUL                           
  6600: ADD                           
  6601: PNT      20                   
  6602: ASGN                          
  6603: SSP      1                    
label_6604:
  6604: GCP      data[1358]            ; = 3
  6605: GADR     data[1359]  ; "%d found on alarm spot %d by %d"
  6606: GCP      data[948]            
  6607: LCP      [sp+0]               
  6608: LCP      [sp+1]               
  6609: GCP      data[1367]            ; = 5
  6610: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  6611: SSP      5                    
  6612: LCP      [sp+0]               
  6613: LLD      [sp-3]               
  6614: RET      9                    
label_6615:
  6615: LCP      [sp+0]               
  6616: LCP      [sp+0]               
  6617: GCP      data[1368]            ; = 1
  6618: ADD                           
  6619: LADR     [sp+0]               
  6620: ASGN                          
  6621: SSP      1                    
  6622: SSP      1                    
  6623: JMP      label_6334           
label_6624:
  6624: LCP      [sp+1]               
  6625: LCP      [sp+1]               
  6626: GCP      data[1369]            ; = 1
  6627: ADD                           
  6628: LADR     [sp+1]               
  6629: ASGN                          
  6630: SSP      1                    
  6631: SSP      1                    
  6632: JMP      label_6304           
label_6633:
  6633: GCP      data[1370]            ; = -1
  6634: LLD      [sp-3]               
  6635: RET      9                    
  6636: ASP      1                    
  6637: ASP      8                    
  6638: ASP      3                    
  6639: LCP      [sp-4]               
  6640: LCP      [sp-3]               
  6641: LES                           
  6642: JZ       label_6697           
  6643: LCP      [sp-3]               
  6644: LCP      [sp-3]               
  6645: GCP      data[1371]            ; = 1
  6646: ADD                           
  6647: LADR     [sp-3]               
  6648: ASGN                          
  6649: SSP      1                    
  6650: SSP      1                    
  6651: GCP      data[1372]            ; = 0.0f
  6652: GCP      data[1373]            ; = 0.0f
  6653: XCALL    $SC_Ai_ClearCheckPoints(unsignedlong,unsignedlong)void ; args=2
  6654: SSP      2                    
  6655: LCP      [sp-4]               
  6656: LADR     [sp+0]               
  6657: ASGN                          
  6658: SSP      1                    
label_6659:
  6659: LCP      [sp+0]               
  6660: LCP      [sp-3]               
  6661: LES                           
  6662: JZ       label_6696           
  6663: ASP      1                    
  6664: LADR     [sp+1]               
  6665: GADR     data[1374]  ; "point"
  6666: LCP      [sp+0]               
  6667: ASP      1                    
  6668: GCP      data[1376]            ; = 3
  6669: XCALL    $sprintf(*char,*constchar,...)int ; args=4294967295
  6670: LLD      [sp+12]              
  6671: SSP      3                    
  6672: SSP      1                    
  6673: ASP      1                    
  6674: LADR     [sp+1]               
  6675: LADR     [sp+9]               
  6676: ASP      1                    
  6677: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  6678: LLD      [sp+12]              
  6679: SSP      2                    
  6680: SSP      1                    
  6681: GCP      data[1377]            ; = 0.0f
  6682: GCP      data[1378]            ; = 0.0f
  6683: LADR     [sp+9]               
  6684: GCP      data[1379]            ; = 0.0f
  6685: XCALL    $SC_Ai_AddCheckPoint(unsignedlong,unsignedlong,*c_Vector3,unsignedlong)void ; args=4
  6686: SSP      4                    
  6687: LCP      [sp+0]               
  6688: LCP      [sp+0]               
  6689: GCP      data[1380]            ; = 1
  6690: ADD                           
  6691: LADR     [sp+0]               
  6692: ASGN                          
  6693: SSP      1                    
  6694: SSP      1                    
  6695: JMP      label_6659           
label_6696:
  6696: JMP      label_6750           
label_6697:
  6697: LCP      [sp-3]               
  6698: LCP      [sp-3]               
  6699: GCP      data[1381]            ; = 1
  6700: SUB                           
  6701: LADR     [sp-3]               
  6702: ASGN                          
  6703: SSP      1                    
  6704: SSP      1                    
  6705: GCP      data[1382]            ; = 0.0f
  6706: GCP      data[1383]            ; = 0.0f
  6707: XCALL    $SC_Ai_ClearCheckPoints(unsignedlong,unsignedlong)void ; args=2
  6708: SSP      2                    
  6709: LCP      [sp-4]               
  6710: LADR     [sp+0]               
  6711: ASGN                          
  6712: SSP      1                    
label_6713:
  6713: LCP      [sp+0]               
  6714: LCP      [sp-3]               
  6715: GRE                           
  6716: JZ       label_6750           
  6717: ASP      1                    
  6718: LADR     [sp+1]               
  6719: GADR     data[1384]  ; "point"
  6720: LCP      [sp+0]               
  6721: ASP      1                    
  6722: GCP      data[1386]            ; = 3
  6723: XCALL    $sprintf(*char,*constchar,...)int ; args=4294967295
  6724: LLD      [sp+12]              
  6725: SSP      3                    
  6726: SSP      1                    
  6727: ASP      1                    
  6728: LADR     [sp+1]               
  6729: LADR     [sp+9]               
  6730: ASP      1                    
  6731: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  6732: LLD      [sp+12]              
  6733: SSP      2                    
  6734: SSP      1                    
  6735: GCP      data[1387]            ; = 0.0f
  6736: GCP      data[1388]            ; = 0.0f
  6737: LADR     [sp+9]               
  6738: GCP      data[1389]            ; = 0.0f
  6739: XCALL    $SC_Ai_AddCheckPoint(unsignedlong,unsignedlong,*c_Vector3,unsignedlong)void ; args=4
  6740: SSP      4                    
  6741: LCP      [sp+0]               
  6742: LCP      [sp+0]               
  6743: GCP      data[1390]            ; = 1
  6744: SUB                           
  6745: LADR     [sp+0]               
  6746: ASGN                          
  6747: SSP      1                    
  6748: SSP      1                    
  6749: JMP      label_6713           
label_6750:
  6750: RET      12                   
  6751: ASP      1                    
  6752: ASP      8                    
  6753: ASP      3                    
  6754: LCP      [sp-3]               
  6755: LCP      [sp-3]               
  6756: GCP      data[1391]            ; = 1
  6757: ADD                           
  6758: LADR     [sp-3]               
  6759: ASGN                          
  6760: SSP      1                    
  6761: SSP      1                    
  6762: LCP      [sp-4]               
  6763: LADR     [sp+0]               
  6764: ASGN                          
  6765: SSP      1                    
label_6766:
  6766: LCP      [sp+0]               
  6767: LCP      [sp-3]               
  6768: LES                           
  6769: JZ       label_6803           
  6770: ASP      1                    
  6771: LADR     [sp+1]               
  6772: GADR     data[1392]  ; "point"
  6773: LCP      [sp+0]               
  6774: ASP      1                    
  6775: GCP      data[1394]            ; = 3
  6776: XCALL    $sprintf(*char,*constchar,...)int ; args=4294967295
  6777: LLD      [sp+12]              
  6778: SSP      3                    
  6779: SSP      1                    
  6780: ASP      1                    
  6781: LADR     [sp+1]               
  6782: LADR     [sp+9]               
  6783: ASP      1                    
  6784: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  6785: LLD      [sp+12]              
  6786: SSP      2                    
  6787: SSP      1                    
  6788: GCP      data[1395]            ; = 0.0f
  6789: GCP      data[1396]            ; = 0.0f
  6790: LADR     [sp+9]               
  6791: GCP      data[1397]            ; = 0.0f
  6792: XCALL    $SC_Ai_AddCheckPoint(unsignedlong,unsignedlong,*c_Vector3,unsignedlong)void ; args=4
  6793: SSP      4                    
  6794: LCP      [sp+0]               
  6795: LCP      [sp+0]               
  6796: GCP      data[1398]            ; = 1
  6797: ADD                           
  6798: LADR     [sp+0]               
  6799: ASGN                          
  6800: SSP      1                    
  6801: SSP      1                    
  6802: JMP      label_6766           
label_6803:
  6803: RET      12                   
func_6804:
  6804: ASP      1                    
  6805: ASP      1                    
  6806: GCP      data[1399]            ; = 1
  6807: LADR     [sp+0]               
  6808: ASGN                          
  6809: SSP      1                    
label_6810:
  6810: LCP      [sp+0]               
  6811: GCP      data[1400]            ; = 6
  6812: LES                           
  6813: JZ       label_6861           
  6814: ASP      1                    
  6815: ASP      1                    
  6816: GCP      data[1401]            ; = 0.0f
  6817: GCP      data[1402]            ; = 0.0f
  6818: LCP      [sp+0]               
  6819: ASP      1                    
  6820: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  6821: LLD      [sp+3]               
  6822: SSP      3                    
  6823: ASP      1                    
  6824: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  6825: LLD      [sp+2]               
  6826: SSP      1                    
  6827: JZ       label_6852           
  6828: JMP      label_6829           
label_6829:
  6829: ASP      1                    
  6830: ASP      1                    
  6831: GCP      data[1403]            ; = 0.0f
  6832: GCP      data[1404]            ; = 0.0f
  6833: LCP      [sp+0]               
  6834: ASP      1                    
  6835: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  6836: LLD      [sp+3]               
  6837: SSP      3                    
  6838: ASP      1                    
  6839: XCALL    $SC_P_Ai_GetPeaceMode(unsignedlong)unsignedlong ; args=1
  6840: LLD      [sp+2]               
  6841: SSP      1                    
  6842: LADR     [sp+1]               
  6843: ASGN                          
  6844: SSP      1                    
  6845: LCP      [sp+1]               
  6846: GCP      data[1405]            ; = 0.0f
  6847: NEQ                           
  6848: JZ       label_6852           
  6849: LCP      [sp+1]               
  6850: LLD      [sp-3]               
  6851: RET      2                    
label_6852:
  6852: LCP      [sp+0]               
  6853: LCP      [sp+0]               
  6854: GCP      data[1406]            ; = 1
  6855: ADD                           
  6856: LADR     [sp+0]               
  6857: ASGN                          
  6858: SSP      1                    
  6859: SSP      1                    
  6860: JMP      label_6810           
label_6861:
  6861: GCP      data[1407]            ; = 0.0f
  6862: LLD      [sp-3]               
  6863: RET      2                    
  6864: GCP      data[1408]            ; = 0.0f
  6865: GCP      data[1409]            ; = 0.0f
  6866: ASP      1                    
  6867: ASP      1                    
  6868: CALL     func_6804            
  6869: LLD      [sp+2]               
  6870: XCALL    $SC_Ai_SetPeaceMode(unsignedlong,unsignedlong,unsignedlong)void ; args=3
  6871: SSP      3                    
  6872: RET      0                    
func_6873:
  6873: ASP      1                    
  6874: ASP      16                   
  6875: GCP      data[1766]            ; = 0.0f
  6876: LADR     [sp+0]               
  6877: ASGN                          
  6878: SSP      1                    
label_6879:
  6879: LCP      [sp+0]               
  6880: GCP      data[1767]            ; = 14
  6881: LES                           
  6882: JZ       label_6946           
  6883: GCP      data[1768]            ; = 0.0f
  6884: GADR     data[1634]           
  6885: LCP      [sp+0]               
  6886: GCP      data[1769]            ; = 28
  6887: MUL                           
  6888: ADD                           
  6889: PNT      24                   
  6890: ASGN                          
  6891: SSP      1                    
  6892: ASP      1                    
  6893: LADR     [sp+1]               
  6894: GADR     data[1770]  ; "ACTIVEPLACE#%d"
  6895: LCP      [sp+0]               
  6896: ASP      1                    
  6897: GCP      data[1774]            ; = 3
  6898: XCALL    $sprintf(*char,*constchar,...)int ; args=4294967295
  6899: LLD      [sp+17]              
  6900: SSP      3                    
  6901: SSP      1                    
  6902: LADR     [sp+1]               
  6903: GADR     data[1634]           
  6904: LCP      [sp+0]               
  6905: GCP      data[1775]            ; = 28
  6906: MUL                           
  6907: ADD                           
  6908: CALL     func_3368            
  6909: SSP      2                    
  6910: GCP      data[1776]            ; = 2.0f
  6911: GADR     data[1634]           
  6912: LCP      [sp+0]               
  6913: GCP      data[1777]            ; = 28
  6914: MUL                           
  6915: ADD                           
  6916: PNT      12                   
  6917: ASGN                          
  6918: SSP      1                    
  6919: GCP      data[1778]            ; = 0.0f
  6920: GADR     data[1634]           
  6921: LCP      [sp+0]               
  6922: GCP      data[1779]            ; = 28
  6923: MUL                           
  6924: ADD                           
  6925: PNT      16                   
  6926: ASGN                          
  6927: SSP      1                    
  6928: GCP      data[1780]            ; = -1.0f
  6929: GADR     data[1634]           
  6930: LCP      [sp+0]               
  6931: GCP      data[1781]            ; = 28
  6932: MUL                           
  6933: ADD                           
  6934: PNT      20                   
  6935: ASGN                          
  6936: SSP      1                    
  6937: LCP      [sp+0]               
  6938: LCP      [sp+0]               
  6939: GCP      data[1782]            ; = 1
  6940: ADD                           
  6941: LADR     [sp+0]               
  6942: ASGN                          
  6943: SSP      1                    
  6944: SSP      1                    
  6945: JMP      label_6879           
label_6946:
  6946: GCP      data[1783]            ; = 30.0f
  6947: GADR     data[1634]           
  6948: GCP      data[1784]            ; = 0.0f
  6949: ADD                           
  6950: PNT      20                   
  6951: ASGN                          
  6952: SSP      1                    
  6953: GCP      data[1785]            ; = 15.0f
  6954: GADR     data[1634]           
  6955: GCP      data[1786]            ; = 28
  6956: ADD                           
  6957: PNT      20                   
  6958: ASGN                          
  6959: SSP      1                    
  6960: GCP      data[1787]            ; = -100
  6961: GADR     data[1634]           
  6962: GCP      data[1788]            ; = 196
  6963: ADD                           
  6964: PNT      24                   
  6965: ASGN                          
  6966: SSP      1                    
  6967: ASP      1                    
  6968: GADR     data[1789]  ; "WayPoint113"
  6969: GADR     data[1750]           
  6970: ASP      1                    
  6971: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  6972: LLD      [sp+17]              
  6973: SSP      2                    
  6974: SSP      1                    
  6975: ASP      1                    
  6976: GADR     data[1792]  ; "WayPoint#33"
  6977: GADR     data[1753]           
  6978: ASP      1                    
  6979: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  6980: LLD      [sp+17]              
  6981: SSP      2                    
  6982: SSP      1                    
  6983: RET      17                   
func_6984:
  6984: LCP      [sp-3]               
  6985: JMP      label_6987           
  6986: JMP      label_6991           
label_6987:
  6987: LCP      [sp+0]               
  6988: GCP      data[1795]            ; = 0.0f
  6989: EQU                           
  6990: JZ       label_6992           
label_6991:
  6991: JMP      label_6996           
label_6992:
  6992: LCP      [sp+0]               
  6993: GCP      data[1796]            ; = 1
  6994: EQU                           
  6995: JZ       label_7016           
label_6996:
  6996: GCP      data[1797]            ; = 0.0f
  6997: GADR     data[1634]           
  6998: LCP      [sp-3]               
  6999: GCP      data[1798]            ; = 28
  7000: MUL                           
  7001: ADD                           
  7002: PNT      16                   
  7003: ASGN                          
  7004: SSP      1                    
  7005: GCP      data[1799]            ; = 1
  7006: GADR     data[1634]           
  7007: LCP      [sp-3]               
  7008: GCP      data[1800]            ; = 28
  7009: MUL                           
  7010: ADD                           
  7011: PNT      24                   
  7012: ASGN                          
  7013: SSP      1                    
  7014: JMP      label_7041           
  7015: JMP      label_7020           
label_7016:
  7016: LCP      [sp+0]               
  7017: GCP      data[1801]            ; = 2
  7018: EQU                           
  7019: JZ       label_7021           
label_7020:
  7020: JMP      label_7025           
label_7021:
  7021: LCP      [sp+0]               
  7022: GCP      data[1802]            ; = 3
  7023: EQU                           
  7024: JZ       label_7026           
label_7025:
  7025: JMP      label_7030           
label_7026:
  7026: LCP      [sp+0]               
  7027: GCP      data[1803]            ; = 4
  7028: EQU                           
  7029: JZ       label_7031           
label_7030:
  7030: JMP      label_7035           
label_7031:
  7031: LCP      [sp+0]               
  7032: GCP      data[1804]            ; = 5
  7033: EQU                           
  7034: JZ       label_7036           
label_7035:
  7035: JMP      label_7040           
label_7036:
  7036: LCP      [sp+0]               
  7037: GCP      data[1805]            ; = 6
  7038: EQU                           
  7039: JZ       label_7041           
label_7040:
  7040: JMP      label_7041           
label_7041:
  7041: SSP      1                    
  7042: RET      0                    
func_7043:
  7043: ASP      1                    
  7044: ASP      3                    
  7045: ASP      1                    
  7046: ASP      1                    
  7047: ASP      1                    
  7048: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7049: LLD      [sp+5]               
  7050: ASP      1                    
  7051: XCALL    $SC_P_GetWillTalk(unsignedlong)float ; args=1
  7052: LLD      [sp+4]               
  7053: SSP      1                    
  7054: GCP      data[1806]            ; = 0.2f
  7055: FADD                          
  7056: LADR     [sp+0]               
  7057: ASGN                          
  7058: SSP      1                    
  7059: LCP      [sp-3]               
  7060: JMP      label_7062           
  7061: JMP      label_7066           
label_7062:
  7062: LCP      [sp+4]               
  7063: GCP      data[1807]            ; = 0.0f
  7064: EQU                           
  7065: JZ       label_7131           
label_7066:
  7066: GADR     data[1634]           
  7067: LCP      [sp-3]               
  7068: GCP      data[1808]            ; = 28
  7069: MUL                           
  7070: ADD                           
  7071: PNT      24                   
  7072: DCP      4                    
  7073: GCP      data[1809]            ; = 0.0f
  7074: EQU                           
  7075: JZ       label_7091           
  7076: ASP      1                    
  7077: ASP      1                    
  7078: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7079: LLD      [sp+5]               
  7080: GCP      data[1810]            ; = 903
  7081: LADR     [sp+0]               
  7082: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7083: SSP      3                    
  7084: LCP      [sp+0]               
  7085: GCP      data[1811]            ; = 0.1f
  7086: FADD                          
  7087: LADR     [sp+0]               
  7088: ASGN                          
  7089: SSP      1                    
  7090: JMP      label_7105           
label_7091:
  7091: ASP      1                    
  7092: ASP      1                    
  7093: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7094: LLD      [sp+5]               
  7095: GCP      data[1812]            ; = 904
  7096: LADR     [sp+0]               
  7097: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7098: SSP      3                    
  7099: LCP      [sp+0]               
  7100: GCP      data[1813]            ; = 0.1f
  7101: FADD                          
  7102: LADR     [sp+0]               
  7103: ASGN                          
  7104: SSP      1                    
label_7105:
  7105: GCP      data[1814]            ; = -100
  7106: GADR     data[1634]           
  7107: LCP      [sp-3]               
  7108: GCP      data[1815]            ; = 28
  7109: MUL                           
  7110: ADD                           
  7111: PNT      24                   
  7112: ASGN                          
  7113: SSP      1                    
  7114: GADR     data[1634]           
  7115: LCP      [sp-3]               
  7116: GCP      data[1816]            ; = 28
  7117: MUL                           
  7118: ADD                           
  7119: PNT      20                   
  7120: DCP      4                    
  7121: GADR     data[1634]           
  7122: LCP      [sp-3]               
  7123: GCP      data[1817]            ; = 28
  7124: MUL                           
  7125: ADD                           
  7126: PNT      16                   
  7127: ASGN                          
  7128: SSP      1                    
  7129: JMP      label_7695           
  7130: JMP      label_7135           
label_7131:
  7131: LCP      [sp+4]               
  7132: GCP      data[1818]            ; = 1
  7133: EQU                           
  7134: JZ       label_7257           
label_7135:
  7135: GADR     data[1634]           
  7136: LCP      [sp-3]               
  7137: GCP      data[1819]            ; = 28
  7138: MUL                           
  7139: ADD                           
  7140: PNT      24                   
  7141: DCP      4                    
  7142: GCP      data[1820]            ; = 0.0f
  7143: EQU                           
  7144: JZ       label_7182           
  7145: ASP      1                    
  7146: ASP      1                    
  7147: XCALL    $rand(void)int        ; args=0
  7148: LLD      [sp+5]               
  7149: GCP      data[1821]            ; = 2
  7150: MOD                           
  7151: JZ       label_7167           
  7152: ASP      1                    
  7153: ASP      1                    
  7154: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7155: LLD      [sp+5]               
  7156: GCP      data[1822]            ; = 905
  7157: LADR     [sp+0]               
  7158: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7159: SSP      3                    
  7160: LCP      [sp+0]               
  7161: GCP      data[1823]            ; = 0.1f
  7162: FADD                          
  7163: LADR     [sp+0]               
  7164: ASGN                          
  7165: SSP      1                    
  7166: JMP      label_7181           
label_7167:
  7167: ASP      1                    
  7168: ASP      1                    
  7169: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7170: LLD      [sp+5]               
  7171: GCP      data[1824]            ; = 911
  7172: LADR     [sp+0]               
  7173: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7174: SSP      3                    
  7175: LCP      [sp+0]               
  7176: GCP      data[1825]            ; = 0.1f
  7177: FADD                          
  7178: LADR     [sp+0]               
  7179: ASGN                          
  7180: SSP      1                    
label_7181:
  7181: JMP      label_7231           
label_7182:
  7182: ASP      1                    
  7183: ASP      1                    
  7184: ASP      1                    
  7185: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7186: LLD      [sp+6]               
  7187: GADR     data[1634]           
  7188: LCP      [sp-3]               
  7189: GCP      data[1826]            ; = 28
  7190: MUL                           
  7191: ADD                           
  7192: ASP      1                    
  7193: CALL     func_4575            
  7194: LLD      [sp+5]               
  7195: SSP      2                    
  7196: ASP      1                    
  7197: ASP      1                    
  7198: ASP      1                    
  7199: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7200: LLD      [sp+7]               
  7201: GADR     data[1634]           
  7202: GCP      data[1827]            ; = 196
  7203: ADD                           
  7204: ASP      1                    
  7205: CALL     func_4575            
  7206: LLD      [sp+6]               
  7207: SSP      2                    
  7208: FLES                          
  7209: JZ       label_7231           
  7210: ASP      1                    
  7211: ASP      1                    
  7212: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7213: LLD      [sp+5]               
  7214: GCP      data[1828]            ; = 908
  7215: ASP      1                    
  7216: ASP      1                    
  7217: XCALL    $rand(void)int        ; args=0
  7218: LLD      [sp+7]               
  7219: GCP      data[1829]            ; = 3
  7220: MOD                           
  7221: ADD                           
  7222: LADR     [sp+0]               
  7223: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7224: SSP      3                    
  7225: LCP      [sp+0]               
  7226: GCP      data[1830]            ; = 0.1f
  7227: FADD                          
  7228: LADR     [sp+0]               
  7229: ASGN                          
  7230: SSP      1                    
label_7231:
  7231: GCP      data[1831]            ; = -100
  7232: GADR     data[1634]           
  7233: LCP      [sp-3]               
  7234: GCP      data[1832]            ; = 28
  7235: MUL                           
  7236: ADD                           
  7237: PNT      24                   
  7238: ASGN                          
  7239: SSP      1                    
  7240: GADR     data[1634]           
  7241: LCP      [sp-3]               
  7242: GCP      data[1833]            ; = 28
  7243: MUL                           
  7244: ADD                           
  7245: PNT      20                   
  7246: DCP      4                    
  7247: GADR     data[1634]           
  7248: LCP      [sp-3]               
  7249: GCP      data[1834]            ; = 28
  7250: MUL                           
  7251: ADD                           
  7252: PNT      16                   
  7253: ASGN                          
  7254: SSP      1                    
  7255: JMP      label_7695           
  7256: JMP      label_7261           
label_7257:
  7257: LCP      [sp+4]               
  7258: GCP      data[1835]            ; = 2
  7259: EQU                           
  7260: JZ       label_7286           
label_7261:
  7261: ASP      1                    
  7262: ASP      1                    
  7263: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7264: LLD      [sp+5]               
  7265: GCP      data[1836]            ; = 906
  7266: LADR     [sp+0]               
  7267: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7268: SSP      3                    
  7269: LCP      [sp+0]               
  7270: GCP      data[1837]            ; = 0.1f
  7271: FADD                          
  7272: LADR     [sp+0]               
  7273: ASGN                          
  7274: SSP      1                    
  7275: GCP      data[1838]            ; = -100
  7276: GADR     data[1634]           
  7277: LCP      [sp-3]               
  7278: GCP      data[1839]            ; = 28
  7279: MUL                           
  7280: ADD                           
  7281: PNT      24                   
  7282: ASGN                          
  7283: SSP      1                    
  7284: JMP      label_7695           
  7285: JMP      label_7290           
label_7286:
  7286: LCP      [sp+4]               
  7287: GCP      data[1840]            ; = 3
  7288: EQU                           
  7289: JZ       label_7316           
label_7290:
  7290: ASP      1                    
  7291: ASP      1                    
  7292: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7293: LLD      [sp+5]               
  7294: GCP      data[1841]            ; = 907
  7295: LADR     [sp+0]               
  7296: GCP      data[1842]            ; = 11
  7297: XCALL    $SC_P_SpeechMes2(unsignedlong,unsignedlong,*float,unsignedlong)void ; args=4
  7298: SSP      4                    
  7299: LCP      [sp+0]               
  7300: GCP      data[1843]            ; = 0.1f
  7301: FADD                          
  7302: LADR     [sp+0]               
  7303: ASGN                          
  7304: SSP      1                    
  7305: GCP      data[1844]            ; = -100
  7306: GADR     data[1634]           
  7307: LCP      [sp-3]               
  7308: GCP      data[1845]            ; = 28
  7309: MUL                           
  7310: ADD                           
  7311: PNT      24                   
  7312: ASGN                          
  7313: SSP      1                    
  7314: JMP      label_7695           
  7315: JMP      label_7320           
label_7316:
  7316: LCP      [sp+4]               
  7317: GCP      data[1846]            ; = 4
  7318: EQU                           
  7319: JZ       label_7426           
label_7320:
  7320: ASP      1                    
  7321: GCP      data[1847]            ; = 1
  7322: GCP      data[1848]            ; = 0.0f
  7323: GCP      data[1849]            ; = 0.0f
  7324: ASP      1                    
  7325: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7326: LLD      [sp+5]               
  7327: SSP      3                    
  7328: LADR     [sp+1]               
  7329: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  7330: SSP      2                    
  7331: GCP      data[1850]            ; = 2060
  7332: LADR     [sp+1]               
  7333: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  7334: SSP      2                    
  7335: LCP      [sp+0]               
  7336: GCP      data[1851]            ; = 0.1f
  7337: FADD                          
  7338: LADR     [sp+0]               
  7339: ASGN                          
  7340: SSP      1                    
  7341: ASP      1                    
  7342: ASP      1                    
  7343: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7344: LLD      [sp+5]               
  7345: GCP      data[1852]            ; = 912
  7346: LADR     [sp+0]               
  7347: GCP      data[1853]            ; = 12
  7348: XCALL    $SC_P_SpeechMes2(unsignedlong,unsignedlong,*float,unsignedlong)void ; args=4
  7349: SSP      4                    
  7350: LCP      [sp+0]               
  7351: GCP      data[1854]            ; = 0.1f
  7352: FADD                          
  7353: LADR     [sp+0]               
  7354: ASGN                          
  7355: SSP      1                    
  7356: GCP      data[1855]            ; = 0.5f
  7357: LADR     [sp+0]               
  7358: ASGN                          
  7359: SSP      1                    
  7360: ASP      1                    
  7361: GCP      data[1856]            ; = 1
  7362: GCP      data[1857]            ; = 0.0f
  7363: GCP      data[1858]            ; = 0.0f
  7364: ASP      1                    
  7365: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7366: LLD      [sp+5]               
  7367: SSP      3                    
  7368: GCP      data[1859]            ; = 913
  7369: LADR     [sp+0]               
  7370: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7371: SSP      3                    
  7372: LCP      [sp+0]               
  7373: GCP      data[1860]            ; = 0.1f
  7374: FADD                          
  7375: LADR     [sp+0]               
  7376: ASGN                          
  7377: SSP      1                    
  7378: ASP      1                    
  7379: GCP      data[1861]            ; = 1
  7380: GCP      data[1862]            ; = 0.0f
  7381: GCP      data[1863]            ; = 1
  7382: ASP      1                    
  7383: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7384: LLD      [sp+5]               
  7385: SSP      3                    
  7386: GCP      data[1864]            ; = 914
  7387: LADR     [sp+0]               
  7388: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7389: SSP      3                    
  7390: LCP      [sp+0]               
  7391: GCP      data[1865]            ; = 0.1f
  7392: FADD                          
  7393: LADR     [sp+0]               
  7394: ASGN                          
  7395: SSP      1                    
  7396: ASP      1                    
  7397: GCP      data[1866]            ; = 1
  7398: GCP      data[1867]            ; = 0.0f
  7399: GCP      data[1868]            ; = 0.0f
  7400: ASP      1                    
  7401: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7402: LLD      [sp+5]               
  7403: SSP      3                    
  7404: GCP      data[1869]            ; = 915
  7405: LADR     [sp+0]               
  7406: GCP      data[1870]            ; = 13
  7407: XCALL    $SC_P_SpeechMes2(unsignedlong,unsignedlong,*float,unsignedlong)void ; args=4
  7408: SSP      4                    
  7409: LCP      [sp+0]               
  7410: GCP      data[1871]            ; = 0.1f
  7411: FADD                          
  7412: LADR     [sp+0]               
  7413: ASGN                          
  7414: SSP      1                    
  7415: GCP      data[1872]            ; = -100
  7416: GADR     data[1634]           
  7417: LCP      [sp-3]               
  7418: GCP      data[1873]            ; = 28
  7419: MUL                           
  7420: ADD                           
  7421: PNT      24                   
  7422: ASGN                          
  7423: SSP      1                    
  7424: JMP      label_7695           
  7425: JMP      label_7430           
label_7426:
  7426: LCP      [sp+4]               
  7427: GCP      data[1874]            ; = 5
  7428: EQU                           
  7429: JZ       label_7455           
label_7430:
  7430: ASP      1                    
  7431: ASP      1                    
  7432: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7433: LLD      [sp+5]               
  7434: GCP      data[1875]            ; = 921
  7435: LADR     [sp+0]               
  7436: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7437: SSP      3                    
  7438: LCP      [sp+0]               
  7439: GCP      data[1876]            ; = 0.1f
  7440: FADD                          
  7441: LADR     [sp+0]               
  7442: ASGN                          
  7443: SSP      1                    
  7444: GCP      data[1877]            ; = -100
  7445: GADR     data[1634]           
  7446: LCP      [sp-3]               
  7447: GCP      data[1878]            ; = 28
  7448: MUL                           
  7449: ADD                           
  7450: PNT      24                   
  7451: ASGN                          
  7452: SSP      1                    
  7453: JMP      label_7695           
  7454: JMP      label_7459           
label_7455:
  7455: LCP      [sp+4]               
  7456: GCP      data[1879]            ; = 6
  7457: EQU                           
  7458: JZ       label_7484           
label_7459:
  7459: ASP      1                    
  7460: ASP      1                    
  7461: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7462: LLD      [sp+5]               
  7463: GCP      data[1880]            ; = 922
  7464: LADR     [sp+0]               
  7465: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7466: SSP      3                    
  7467: LCP      [sp+0]               
  7468: GCP      data[1881]            ; = 0.1f
  7469: FADD                          
  7470: LADR     [sp+0]               
  7471: ASGN                          
  7472: SSP      1                    
  7473: GCP      data[1882]            ; = -100
  7474: GADR     data[1634]           
  7475: LCP      [sp-3]               
  7476: GCP      data[1883]            ; = 28
  7477: MUL                           
  7478: ADD                           
  7479: PNT      24                   
  7480: ASGN                          
  7481: SSP      1                    
  7482: JMP      label_7695           
  7483: JMP      label_7488           
label_7484:
  7484: LCP      [sp+4]               
  7485: GCP      data[1884]            ; = 8
  7486: EQU                           
  7487: JZ       label_7518           
label_7488:
  7488: ASP      1                    
  7489: GCP      data[1885]            ; = 1
  7490: GCP      data[1886]            ; = 0.0f
  7491: GCP      data[1887]            ; = 1
  7492: ASP      1                    
  7493: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7494: LLD      [sp+5]               
  7495: SSP      3                    
  7496: GCP      data[1888]            ; = 924
  7497: LADR     [sp+0]               
  7498: GCP      data[1889]            ; = 14
  7499: XCALL    $SC_P_SpeechMes2(unsignedlong,unsignedlong,*float,unsignedlong)void ; args=4
  7500: SSP      4                    
  7501: LCP      [sp+0]               
  7502: GCP      data[1890]            ; = 0.1f
  7503: FADD                          
  7504: LADR     [sp+0]               
  7505: ASGN                          
  7506: SSP      1                    
  7507: GCP      data[1891]            ; = -100
  7508: GADR     data[1634]           
  7509: LCP      [sp-3]               
  7510: GCP      data[1892]            ; = 28
  7511: MUL                           
  7512: ADD                           
  7513: PNT      24                   
  7514: ASGN                          
  7515: SSP      1                    
  7516: JMP      label_7695           
  7517: JMP      label_7522           
label_7518:
  7518: LCP      [sp+4]               
  7519: GCP      data[1893]            ; = 9
  7520: EQU                           
  7521: JZ       label_7563           
label_7522:
  7522: GCP      data[1894]            ; = -100
  7523: GADR     data[1634]           
  7524: LCP      [sp-3]               
  7525: GCP      data[1895]            ; = 28
  7526: MUL                           
  7527: ADD                           
  7528: PNT      24                   
  7529: ASGN                          
  7530: SSP      1                    
  7531: ASP      1                    
  7532: GCP      data[1896]            ; = 1
  7533: GCP      data[1897]            ; = 0.0f
  7534: GCP      data[1898]            ; = 0.0f
  7535: ASP      1                    
  7536: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7537: LLD      [sp+5]               
  7538: SSP      3                    
  7539: GCP      data[1899]            ; = 0.0f
  7540: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  7541: SSP      2                    
  7542: ASP      1                    
  7543: GADR     data[1900]  ; "WayPoint113"
  7544: LADR     [sp+1]               
  7545: ASP      1                    
  7546: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  7547: LLD      [sp+5]               
  7548: SSP      2                    
  7549: SSP      1                    
  7550: ASP      1                    
  7551: GCP      data[1903]            ; = 1
  7552: GCP      data[1904]            ; = 0.0f
  7553: GCP      data[1905]            ; = 0.0f
  7554: ASP      1                    
  7555: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7556: LLD      [sp+5]               
  7557: SSP      3                    
  7558: LADR     [sp+1]               
  7559: XCALL    $SC_P_Ai_Go(unsignedlong,*c_Vector3)void ; args=2
  7560: SSP      2                    
  7561: JMP      label_7695           
  7562: JMP      label_7567           
label_7563:
  7563: LCP      [sp+4]               
  7564: GCP      data[1906]            ; = 10
  7565: EQU                           
  7566: JZ       label_7595           
label_7567:
  7567: GCP      data[1762]           
  7568: JZ       label_7593           
  7569: ASP      1                    
  7570: ASP      1                    
  7571: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7572: LLD      [sp+5]               
  7573: GCP      data[1907]            ; = 932
  7574: LADR     [sp+0]               
  7575: GCP      data[1908]            ; = 15
  7576: XCALL    $SC_P_SpeechMes2(unsignedlong,unsignedlong,*float,unsignedlong)void ; args=4
  7577: SSP      4                    
  7578: LCP      [sp+0]               
  7579: GCP      data[1909]            ; = 0.1f
  7580: FADD                          
  7581: LADR     [sp+0]               
  7582: ASGN                          
  7583: SSP      1                    
  7584: GCP      data[1910]            ; = -100
  7585: GADR     data[1634]           
  7586: LCP      [sp-3]               
  7587: GCP      data[1911]            ; = 28
  7588: MUL                           
  7589: ADD                           
  7590: PNT      24                   
  7591: ASGN                          
  7592: SSP      1                    
label_7593:
  7593: JMP      label_7695           
  7594: JMP      label_7599           
label_7595:
  7595: LCP      [sp+4]               
  7596: GCP      data[1912]            ; = 11
  7597: EQU                           
  7598: JZ       label_7658           
label_7599:
  7599: ASP      1                    
  7600: GCP      data[1913]            ; = 1
  7601: GCP      data[1914]            ; = 1
  7602: GCP      data[1915]            ; = 0.0f
  7603: ASP      1                    
  7604: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7605: LLD      [sp+5]               
  7606: SSP      3                    
  7607: LADR     [sp+1]               
  7608: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  7609: SSP      2                    
  7610: GCP      data[1916]            ; = 10419
  7611: LADR     [sp+1]               
  7612: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  7613: SSP      2                    
  7614: ASP      1                    
  7615: GCP      data[1917]            ; = 1
  7616: GCP      data[1918]            ; = 1
  7617: GCP      data[1919]            ; = 1
  7618: ASP      1                    
  7619: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7620: LLD      [sp+5]               
  7621: SSP      3                    
  7622: LADR     [sp+1]               
  7623: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  7624: SSP      2                    
  7625: GCP      data[1920]            ; = 10419
  7626: LADR     [sp+1]               
  7627: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  7628: SSP      2                    
  7629: ASP      1                    
  7630: ASP      1                    
  7631: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7632: LLD      [sp+5]               
  7633: GCP      data[1921]            ; = 944
  7634: LADR     [sp+0]               
  7635: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7636: SSP      3                    
  7637: LCP      [sp+0]               
  7638: GCP      data[1922]            ; = 0.1f
  7639: FADD                          
  7640: LADR     [sp+0]               
  7641: ASGN                          
  7642: SSP      1                    
  7643: GCP      data[1923]            ; = 1
  7644: GADR     data[1757]           
  7645: ASGN                          
  7646: SSP      1                    
  7647: GCP      data[1924]            ; = -100
  7648: GADR     data[1634]           
  7649: LCP      [sp-3]               
  7650: GCP      data[1925]            ; = 28
  7651: MUL                           
  7652: ADD                           
  7653: PNT      24                   
  7654: ASGN                          
  7655: SSP      1                    
  7656: JMP      label_7695           
  7657: JMP      label_7662           
label_7658:
  7658: LCP      [sp+4]               
  7659: GCP      data[1926]            ; = 13
  7660: EQU                           
  7661: JZ       label_7680           
label_7662:
  7662: ASP      1                    
  7663: GCP      data[1927]            ; = 1
  7664: ASP      1                    
  7665: XCALL    $SC_AGS_Set(unsignedlong)unsignedlong ; args=1
  7666: LLD      [sp+5]               
  7667: SSP      1                    
  7668: SSP      1                    
  7669: GCP      data[1928]            ; = -100
  7670: GADR     data[1634]           
  7671: LCP      [sp-3]               
  7672: GCP      data[1929]            ; = 28
  7673: MUL                           
  7674: ADD                           
  7675: PNT      24                   
  7676: ASGN                          
  7677: SSP      1                    
  7678: JMP      label_7695           
  7679: JMP      label_7684           
label_7680:
  7680: LCP      [sp+4]               
  7681: GCP      data[1930]            ; = 12
  7682: EQU                           
  7683: JZ       label_7695           
label_7684:
  7684: CALL     func_1223            
  7685: GCP      data[1931]            ; = -100
  7686: GADR     data[1634]           
  7687: LCP      [sp-3]               
  7688: GCP      data[1932]            ; = 28
  7689: MUL                           
  7690: ADD                           
  7691: PNT      24                   
  7692: ASGN                          
  7693: SSP      1                    
  7694: JMP      label_7695           
label_7695:
  7695: SSP      1                    
  7696: RET      4                    
func_7697:
  7697: ASP      1                    
  7698: GCP      data[1933]            ; = 0.0f
  7699: LADR     [sp+0]               
  7700: ASGN                          
  7701: SSP      1                    
label_7702:
  7702: LCP      [sp+0]               
  7703: GCP      data[1934]            ; = 14
  7704: LES                           
  7705: JZ       label_7755           
  7706: GADR     data[1634]           
  7707: LCP      [sp+0]               
  7708: GCP      data[1935]            ; = 28
  7709: MUL                           
  7710: ADD                           
  7711: PNT      16                   
  7712: DCP      4                    
  7713: GCP      data[1936]            ; = 0.0f
  7714: FGRE                          
  7715: JZ       label_7746           
  7716: GADR     data[1634]           
  7717: LCP      [sp+0]               
  7718: GCP      data[1937]            ; = 28
  7719: MUL                           
  7720: ADD                           
  7721: PNT      16                   
  7722: DCP      4                    
  7723: LCP      [sp-3]               
  7724: FSUB                          
  7725: GADR     data[1634]           
  7726: LCP      [sp+0]               
  7727: GCP      data[1938]            ; = 28
  7728: MUL                           
  7729: ADD                           
  7730: PNT      16                   
  7731: ASGN                          
  7732: SSP      1                    
  7733: GADR     data[1634]           
  7734: LCP      [sp+0]               
  7735: GCP      data[1939]            ; = 28
  7736: MUL                           
  7737: ADD                           
  7738: PNT      16                   
  7739: DCP      4                    
  7740: GCP      data[1940]            ; = 0.0f
  7741: FLES                          
  7742: JZ       label_7746           
  7743: LCP      [sp+0]               
  7744: CALL     func_6984            
  7745: SSP      1                    
label_7746:
  7746: LCP      [sp+0]               
  7747: LCP      [sp+0]               
  7748: GCP      data[1941]            ; = 1
  7749: ADD                           
  7750: LADR     [sp+0]               
  7751: ASGN                          
  7752: SSP      1                    
  7753: SSP      1                    
  7754: JMP      label_7702           
label_7755:
  7755: GCP      data[1942]            ; = 0.0f
  7756: LADR     [sp+0]               
  7757: ASGN                          
  7758: SSP      1                    
label_7759:
  7759: LCP      [sp+0]               
  7760: GCP      data[1943]            ; = 14
  7761: LES                           
  7762: JZ       label_7806           
  7763: GADR     data[1634]           
  7764: LCP      [sp+0]               
  7765: GCP      data[1944]            ; = 28
  7766: MUL                           
  7767: ADD                           
  7768: PNT      24                   
  7769: DCP      4                    
  7770: GCP      data[1945]            ; = -100
  7771: NEQ                           
  7772: JZ       label_7797           
  7773: ASP      1                    
  7774: LCP      [sp-4]               
  7775: GADR     data[1634]           
  7776: LCP      [sp+0]               
  7777: GCP      data[1946]            ; = 28
  7778: MUL                           
  7779: ADD                           
  7780: GADR     data[1634]           
  7781: LCP      [sp+0]               
  7782: GCP      data[1947]            ; = 28
  7783: MUL                           
  7784: ADD                           
  7785: PNT      12                   
  7786: DCP      4                    
  7787: ASP      1                    
  7788: XCALL    $SC_IsNear3D(*c_Vector3,*c_Vector3,float)int ; args=3
  7789: LLD      [sp+1]               
  7790: SSP      3                    
  7791: JZ       label_7797           
  7792: JMP      label_7793           
label_7793:
  7793: LCP      [sp+0]               
  7794: CALL     func_7043            
  7795: SSP      1                    
  7796: RET      1                    
label_7797:
  7797: LCP      [sp+0]               
  7798: LCP      [sp+0]               
  7799: GCP      data[1948]            ; = 1
  7800: ADD                           
  7801: LADR     [sp+0]               
  7802: ASGN                          
  7803: SSP      1                    
  7804: SSP      1                    
  7805: JMP      label_7759           
label_7806:
  7806: RET      1                    
func_7807:
  7807: GCP      data[1951]            ; = 0.1f
  7808: ASP      1                    
  7809: ASP      3                    
  7810: GCP      data[1756]           
  7811: JMP      label_7813           
  7812: JMP      label_7817           
label_7813:
  7813: LCP      [sp+5]               
  7814: GCP      data[1952]            ; = 0.0f
  7815: EQU                           
  7816: JZ       label_7864           
label_7817:
  7817: ASP      1                    
  7818: ASP      1                    
  7819: GCP      data[1953]            ; = 1
  7820: GCP      data[1954]            ; = 0.0f
  7821: GCP      data[1955]            ; = 0.0f
  7822: ASP      1                    
  7823: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7824: LLD      [sp+7]               
  7825: SSP      3                    
  7826: ASP      1                    
  7827: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  7828: LLD      [sp+6]               
  7829: SSP      1                    
  7830: JZ       label_7863           
  7831: JMP      label_7832           
label_7832:
  7832: ASP      1                    
  7833: GCP      data[1956]            ; = 0.0f
  7834: GCP      data[1957]            ; = 0.0f
  7835: ASP      1                    
  7836: CALL     func_0371            
  7837: LLD      [sp+6]               
  7838: SSP      2                    
  7839: JZ       label_7863           
  7840: JMP      label_7841           
label_7841:
  7841: ASP      1                    
  7842: GCP      data[1958]            ; = 1
  7843: GCP      data[1959]            ; = 0.0f
  7844: GCP      data[1960]            ; = 0.0f
  7845: ASP      1                    
  7846: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7847: LLD      [sp+6]               
  7848: SSP      3                    
  7849: GCP      data[1961]            ; = 926
  7850: LADR     [sp+0]               
  7851: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7852: SSP      3                    
  7853: LCP      [sp+0]               
  7854: GCP      data[1962]            ; = 0.1f
  7855: FADD                          
  7856: LADR     [sp+0]               
  7857: ASGN                          
  7858: SSP      1                    
  7859: GCP      data[1963]            ; = 1
  7860: GADR     data[1756]           
  7861: ASGN                          
  7862: SSP      1                    
label_7863:
  7863: JMP      label_7868           
label_7864:
  7864: LCP      [sp+5]               
  7865: GCP      data[1964]            ; = 1
  7866: EQU                           
  7867: JZ       label_7946           
label_7868:
  7868: ASP      1                    
  7869: ASP      1                    
  7870: GCP      data[1965]            ; = 1
  7871: GCP      data[1966]            ; = 0.0f
  7872: GCP      data[1967]            ; = 0.0f
  7873: ASP      1                    
  7874: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7875: LLD      [sp+7]               
  7876: SSP      3                    
  7877: ASP      1                    
  7878: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  7879: LLD      [sp+6]               
  7880: SSP      1                    
  7881: JZ       label_7883           
  7882: JMP      label_7913           
label_7883:
  7883: ASP      1                    
  7884: ASP      1                    
  7885: ASP      1                    
  7886: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7887: LLD      [sp+7]               
  7888: ASP      1                    
  7889: XCALL    $SC_P_GetWillTalk(unsignedlong)float ; args=1
  7890: LLD      [sp+6]               
  7891: SSP      1                    
  7892: LADR     [sp+0]               
  7893: ASGN                          
  7894: SSP      1                    
  7895: ASP      1                    
  7896: ASP      1                    
  7897: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7898: LLD      [sp+6]               
  7899: GCP      data[1968]            ; = 927
  7900: LADR     [sp+0]               
  7901: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7902: SSP      3                    
  7903: LCP      [sp+0]               
  7904: GCP      data[1969]            ; = 0.1f
  7905: FADD                          
  7906: LADR     [sp+0]               
  7907: ASGN                          
  7908: SSP      1                    
  7909: GCP      data[1970]            ; = 100
  7910: GADR     data[1756]           
  7911: ASGN                          
  7912: SSP      1                    
label_7913:
  7913: ASP      1                    
  7914: ASP      1                    
  7915: GCP      data[1971]            ; = 1
  7916: GCP      data[1972]            ; = 0.0f
  7917: GCP      data[1973]            ; = 0.0f
  7918: ASP      1                    
  7919: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7920: LLD      [sp+7]               
  7921: SSP      3                    
  7922: GADR     data[1750]           
  7923: GCP      data[1974]            ; = 5.0f
  7924: ASP      1                    
  7925: CALL     func_4180            
  7926: LLD      [sp+6]               
  7927: SSP      3                    
  7928: JZ       label_7944           
  7929: ASP      1                    
  7930: GCP      data[1975]            ; = 1
  7931: GCP      data[1976]            ; = 0.0f
  7932: GCP      data[1977]            ; = 0.0f
  7933: ASP      1                    
  7934: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7935: LLD      [sp+6]               
  7936: SSP      3                    
  7937: GCP      data[1978]            ; = 1
  7938: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  7939: SSP      2                    
  7940: GCP      data[1979]            ; = 2
  7941: GADR     data[1756]           
  7942: ASGN                          
  7943: SSP      1                    
label_7944:
  7944: JMP      label_8148           
  7945: JMP      label_7950           
label_7946:
  7946: LCP      [sp+5]               
  7947: GCP      data[1980]            ; = 2
  7948: EQU                           
  7949: JZ       label_7997           
label_7950:
  7950: ASP      1                    
  7951: ASP      1                    
  7952: GCP      data[1981]            ; = 1
  7953: GCP      data[1982]            ; = 0.0f
  7954: GCP      data[1983]            ; = 0.0f
  7955: ASP      1                    
  7956: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  7957: LLD      [sp+7]               
  7958: SSP      3                    
  7959: LADR     [sp+1]               
  7960: ASP      1                    
  7961: XCALL    $SC_P_Ai_GetShooting(unsignedlong,*unsignedlong)int ; args=2
  7962: LLD      [sp+6]               
  7963: SSP      2                    
  7964: JZ       label_7995           
  7965: ASP      1                    
  7966: ASP      1                    
  7967: ASP      1                    
  7968: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7969: LLD      [sp+7]               
  7970: ASP      1                    
  7971: XCALL    $SC_P_GetWillTalk(unsignedlong)float ; args=1
  7972: LLD      [sp+6]               
  7973: SSP      1                    
  7974: LADR     [sp+0]               
  7975: ASGN                          
  7976: SSP      1                    
  7977: ASP      1                    
  7978: ASP      1                    
  7979: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  7980: LLD      [sp+6]               
  7981: GCP      data[1984]            ; = 929
  7982: LADR     [sp+0]               
  7983: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  7984: SSP      3                    
  7985: LCP      [sp+0]               
  7986: GCP      data[1985]            ; = 0.1f
  7987: FADD                          
  7988: LADR     [sp+0]               
  7989: ASGN                          
  7990: SSP      1                    
  7991: GCP      data[1986]            ; = 3
  7992: GADR     data[1756]           
  7993: ASGN                          
  7994: SSP      1                    
label_7995:
  7995: JMP      label_8148           
  7996: JMP      label_8001           
label_7997:
  7997: LCP      [sp+5]               
  7998: GCP      data[1987]            ; = 3
  7999: EQU                           
  8000: JZ       label_8112           
label_8001:
  8001: ASP      1                    
  8002: ASP      1                    
  8003: GCP      data[1988]            ; = 1
  8004: GCP      data[1989]            ; = 0.0f
  8005: GCP      data[1990]            ; = 0.0f
  8006: ASP      1                    
  8007: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8008: LLD      [sp+7]               
  8009: SSP      3                    
  8010: ASP      1                    
  8011: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  8012: LLD      [sp+6]               
  8013: SSP      1                    
  8014: JZ       label_8016           
  8015: JMP      label_8046           
label_8016:
  8016: ASP      1                    
  8017: ASP      1                    
  8018: ASP      1                    
  8019: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  8020: LLD      [sp+7]               
  8021: ASP      1                    
  8022: XCALL    $SC_P_GetWillTalk(unsignedlong)float ; args=1
  8023: LLD      [sp+6]               
  8024: SSP      1                    
  8025: LADR     [sp+0]               
  8026: ASGN                          
  8027: SSP      1                    
  8028: ASP      1                    
  8029: ASP      1                    
  8030: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  8031: LLD      [sp+6]               
  8032: GCP      data[1991]            ; = 927
  8033: LADR     [sp+0]               
  8034: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  8035: SSP      3                    
  8036: LCP      [sp+0]               
  8037: GCP      data[1992]            ; = 0.1f
  8038: FADD                          
  8039: LADR     [sp+0]               
  8040: ASGN                          
  8041: SSP      1                    
  8042: GCP      data[1993]            ; = 100
  8043: GADR     data[1756]           
  8044: ASGN                          
  8045: SSP      1                    
label_8046:
  8046: GCP      data[1759]           
  8047: LCP      [sp-3]               
  8048: FADD                          
  8049: GADR     data[1759]           
  8050: ASGN                          
  8051: SSP      1                    
  8052: GCP      data[1759]           
  8053: GCP      data[1994]            ; = 3.0f
  8054: FGRE                          
  8055: JZ       label_8110           
  8056: ASP      1                    
  8057: GCP      data[1995]            ; = 1
  8058: GCP      data[1996]            ; = 0.0f
  8059: GCP      data[1997]            ; = 0.0f
  8060: ASP      1                    
  8061: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8062: LLD      [sp+6]               
  8063: SSP      3                    
  8064: GCP      data[1998]            ; = 0.0f
  8065: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8066: SSP      2                    
  8067: ASP      1                    
  8068: GCP      data[1999]            ; = 1
  8069: GCP      data[2000]            ; = 0.0f
  8070: GCP      data[2001]            ; = 0.0f
  8071: ASP      1                    
  8072: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8073: LLD      [sp+6]               
  8074: SSP      3                    
  8075: GADR     data[1753]           
  8076: XCALL    $SC_P_Ai_Go(unsignedlong,*c_Vector3)void ; args=2
  8077: SSP      2                    
  8078: ASP      1                    
  8079: ASP      1                    
  8080: ASP      1                    
  8081: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  8082: LLD      [sp+7]               
  8083: ASP      1                    
  8084: XCALL    $SC_P_GetWillTalk(unsignedlong)float ; args=1
  8085: LLD      [sp+6]               
  8086: SSP      1                    
  8087: GCP      data[2002]            ; = 0.2f
  8088: FADD                          
  8089: LADR     [sp+0]               
  8090: ASGN                          
  8091: SSP      1                    
  8092: ASP      1                    
  8093: ASP      1                    
  8094: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  8095: LLD      [sp+6]               
  8096: GCP      data[2003]            ; = 930
  8097: LADR     [sp+0]               
  8098: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  8099: SSP      3                    
  8100: LCP      [sp+0]               
  8101: GCP      data[2004]            ; = 0.1f
  8102: FADD                          
  8103: LADR     [sp+0]               
  8104: ASGN                          
  8105: SSP      1                    
  8106: GCP      data[2005]            ; = 4
  8107: GADR     data[1756]           
  8108: ASGN                          
  8109: SSP      1                    
label_8110:
  8110: JMP      label_8148           
  8111: JMP      label_8116           
label_8112:
  8112: LCP      [sp+5]               
  8113: GCP      data[2006]            ; = 4
  8114: EQU                           
  8115: JZ       label_8148           
label_8116:
  8116: ASP      1                    
  8117: ASP      1                    
  8118: GCP      data[2007]            ; = 1
  8119: GCP      data[2008]            ; = 0.0f
  8120: GCP      data[2009]            ; = 0.0f
  8121: ASP      1                    
  8122: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8123: LLD      [sp+7]               
  8124: SSP      3                    
  8125: GADR     data[1750]           
  8126: GCP      data[2010]            ; = 5.0f
  8127: ASP      1                    
  8128: CALL     func_4180            
  8129: LLD      [sp+6]               
  8130: SSP      3                    
  8131: JZ       label_8147           
  8132: ASP      1                    
  8133: GCP      data[2011]            ; = 1
  8134: GCP      data[2012]            ; = 0.0f
  8135: GCP      data[2013]            ; = 0.0f
  8136: ASP      1                    
  8137: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8138: LLD      [sp+6]               
  8139: SSP      3                    
  8140: GCP      data[2014]            ; = 1
  8141: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8142: SSP      2                    
  8143: GCP      data[2015]            ; = 5
  8144: GADR     data[1756]           
  8145: ASGN                          
  8146: SSP      1                    
label_8147:
  8147: JMP      label_8148           
label_8148:
  8148: SSP      1                    
  8149: GCP      data[1761]           
  8150: JZ       label_8152           
  8151: JMP      label_8214           
label_8152:
  8152: ASP      1                    
  8153: ASP      1                    
  8154: GCP      data[2016]            ; = 1
  8155: GCP      data[2017]            ; = 0.0f
  8156: GCP      data[2018]            ; = 1
  8157: ASP      1                    
  8158: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8159: LLD      [sp+6]               
  8160: SSP      3                    
  8161: ASP      1                    
  8162: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  8163: LLD      [sp+5]               
  8164: SSP      1                    
  8165: JZ       label_8167           
  8166: JMP      label_8214           
label_8167:
  8167: ASP      1                    
  8168: ASP      1                    
  8169: GCP      data[2019]            ; = 1
  8170: GCP      data[2020]            ; = 0.0f
  8171: GCP      data[2021]            ; = 2
  8172: ASP      1                    
  8173: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8174: LLD      [sp+6]               
  8175: SSP      3                    
  8176: ASP      1                    
  8177: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  8178: LLD      [sp+5]               
  8179: SSP      1                    
  8180: JZ       label_8182           
  8181: JMP      label_8214           
label_8182:
  8182: GCP      data[2022]            ; = 1
  8183: GADR     data[1761]           
  8184: ASGN                          
  8185: SSP      1                    
  8186: ASP      1                    
  8187: ASP      1                    
  8188: ASP      1                    
  8189: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  8190: LLD      [sp+6]               
  8191: ASP      1                    
  8192: XCALL    $SC_P_GetWillTalk(unsignedlong)float ; args=1
  8193: LLD      [sp+5]               
  8194: SSP      1                    
  8195: GCP      data[2023]            ; = 0.5f
  8196: FADD                          
  8197: LADR     [sp+0]               
  8198: ASGN                          
  8199: SSP      1                    
  8200: ASP      1                    
  8201: ASP      1                    
  8202: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  8203: LLD      [sp+5]               
  8204: GCP      data[2024]            ; = 928
  8205: LADR     [sp+0]               
  8206: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  8207: SSP      3                    
  8208: LCP      [sp+0]               
  8209: GCP      data[2025]            ; = 0.1f
  8210: FADD                          
  8211: LADR     [sp+0]               
  8212: ASGN                          
  8213: SSP      1                    
label_8214:
  8214: GCP      data[1762]           
  8215: JZ       label_8217           
  8216: JMP      label_8294           
label_8217:
  8217: ASP      1                    
  8218: ASP      1                    
  8219: GCP      data[2026]            ; = 1
  8220: GCP      data[2027]            ; = 0.0f
  8221: GCP      data[2028]            ; = 5
  8222: ASP      1                    
  8223: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8224: LLD      [sp+6]               
  8225: SSP      3                    
  8226: ASP      1                    
  8227: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  8228: LLD      [sp+5]               
  8229: SSP      1                    
  8230: JZ       label_8232           
  8231: JMP      label_8294           
label_8232:
  8232: ASP      1                    
  8233: ASP      1                    
  8234: GCP      data[2029]            ; = 1
  8235: GCP      data[2030]            ; = 0.0f
  8236: GCP      data[2031]            ; = 4
  8237: ASP      1                    
  8238: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8239: LLD      [sp+6]               
  8240: SSP      3                    
  8241: ASP      1                    
  8242: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  8243: LLD      [sp+5]               
  8244: SSP      1                    
  8245: JZ       label_8247           
  8246: JMP      label_8294           
label_8247:
  8247: ASP      1                    
  8248: ASP      1                    
  8249: GCP      data[2032]            ; = 1
  8250: GCP      data[2033]            ; = 0.0f
  8251: GCP      data[2034]            ; = 0.0f
  8252: ASP      1                    
  8253: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8254: LLD      [sp+6]               
  8255: SSP      3                    
  8256: ASP      1                    
  8257: XCALL    $SC_P_IsReady(unsignedlong)int ; args=1
  8258: LLD      [sp+5]               
  8259: SSP      1                    
  8260: JZ       label_8262           
  8261: JMP      label_8294           
label_8262:
  8262: GCP      data[2035]            ; = 1
  8263: GADR     data[1762]           
  8264: ASGN                          
  8265: SSP      1                    
  8266: ASP      1                    
  8267: ASP      1                    
  8268: ASP      1                    
  8269: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  8270: LLD      [sp+6]               
  8271: ASP      1                    
  8272: XCALL    $SC_P_GetWillTalk(unsignedlong)float ; args=1
  8273: LLD      [sp+5]               
  8274: SSP      1                    
  8275: GCP      data[2036]            ; = 0.5f
  8276: FADD                          
  8277: LADR     [sp+0]               
  8278: ASGN                          
  8279: SSP      1                    
  8280: ASP      1                    
  8281: ASP      1                    
  8282: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  8283: LLD      [sp+5]               
  8284: GCP      data[2037]            ; = 931
  8285: LADR     [sp+0]               
  8286: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  8287: SSP      3                    
  8288: LCP      [sp+0]               
  8289: GCP      data[2038]            ; = 0.1f
  8290: FADD                          
  8291: LADR     [sp+0]               
  8292: ASGN                          
  8293: SSP      1                    
label_8294:
  8294: GCP      data[1757]           
  8295: GCP      data[2039]            ; = 100
  8296: NEQ                           
  8297: JZ       label_8369           
  8298: ASP      1                    
  8299: GCP      data[2040]            ; = 1
  8300: GCP      data[2041]            ; = 0.0f
  8301: ASP      1                    
  8302: CALL     func_0371            
  8303: LLD      [sp+5]               
  8304: SSP      2                    
  8305: JZ       label_8369           
  8306: JMP      label_8307           
label_8307:
  8307: ASP      1                    
  8308: GCP      data[2042]            ; = 1
  8309: GCP      data[2043]            ; = 1
  8310: GCP      data[2044]            ; = 0.0f
  8311: ASP      1                    
  8312: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8313: LLD      [sp+5]               
  8314: SSP      3                    
  8315: GCP      data[2045]            ; = 947
  8316: ASP      1                    
  8317: ASP      1                    
  8318: XCALL    $rand(void)int        ; args=0
  8319: LLD      [sp+7]               
  8320: GCP      data[2046]            ; = 2
  8321: MOD                           
  8322: ADD                           
  8323: LADR     [sp+0]               
  8324: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  8325: SSP      3                    
  8326: LCP      [sp+0]               
  8327: GCP      data[2047]            ; = 0.1f
  8328: FADD                          
  8329: LADR     [sp+0]               
  8330: ASGN                          
  8331: SSP      1                    
  8332: ASP      1                    
  8333: GCP      data[2048]            ; = 1
  8334: GCP      data[2049]            ; = 1
  8335: GCP      data[2050]            ; = 0.0f
  8336: ASP      1                    
  8337: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8338: LLD      [sp+5]               
  8339: SSP      3                    
  8340: GCP      data[2051]            ; = 1
  8341: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8342: SSP      2                    
  8343: ASP      1                    
  8344: GCP      data[2052]            ; = 1
  8345: GCP      data[2053]            ; = 1
  8346: GCP      data[2054]            ; = 1
  8347: ASP      1                    
  8348: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8349: LLD      [sp+5]               
  8350: SSP      3                    
  8351: GCP      data[2055]            ; = 1
  8352: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8353: SSP      2                    
  8354: ASP      1                    
  8355: GCP      data[2056]            ; = 1
  8356: GCP      data[2057]            ; = 1
  8357: GCP      data[2058]            ; = 2
  8358: ASP      1                    
  8359: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8360: LLD      [sp+5]               
  8361: SSP      3                    
  8362: GCP      data[2059]            ; = 1
  8363: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8364: SSP      2                    
  8365: GCP      data[2060]            ; = 100
  8366: GADR     data[1757]           
  8367: ASGN                          
  8368: SSP      1                    
label_8369:
  8369: GCP      data[1757]           
  8370: GCP      data[2061]            ; = 100
  8371: NEQ                           
  8372: JZ       label_8444           
  8373: ASP      1                    
  8374: GCP      data[2062]            ; = 1
  8375: GCP      data[2063]            ; = 1
  8376: ASP      1                    
  8377: CALL     func_0371            
  8378: LLD      [sp+5]               
  8379: SSP      2                    
  8380: JZ       label_8444           
  8381: JMP      label_8382           
label_8382:
  8382: ASP      1                    
  8383: GCP      data[2064]            ; = 1
  8384: GCP      data[2065]            ; = 1
  8385: GCP      data[2066]            ; = 1
  8386: ASP      1                    
  8387: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8388: LLD      [sp+5]               
  8389: SSP      3                    
  8390: GCP      data[2067]            ; = 947
  8391: ASP      1                    
  8392: ASP      1                    
  8393: XCALL    $rand(void)int        ; args=0
  8394: LLD      [sp+7]               
  8395: GCP      data[2068]            ; = 2
  8396: MOD                           
  8397: ADD                           
  8398: LADR     [sp+0]               
  8399: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  8400: SSP      3                    
  8401: LCP      [sp+0]               
  8402: GCP      data[2069]            ; = 0.1f
  8403: FADD                          
  8404: LADR     [sp+0]               
  8405: ASGN                          
  8406: SSP      1                    
  8407: ASP      1                    
  8408: GCP      data[2070]            ; = 1
  8409: GCP      data[2071]            ; = 1
  8410: GCP      data[2072]            ; = 0.0f
  8411: ASP      1                    
  8412: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8413: LLD      [sp+5]               
  8414: SSP      3                    
  8415: GCP      data[2073]            ; = 1
  8416: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8417: SSP      2                    
  8418: ASP      1                    
  8419: GCP      data[2074]            ; = 1
  8420: GCP      data[2075]            ; = 1
  8421: GCP      data[2076]            ; = 1
  8422: ASP      1                    
  8423: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8424: LLD      [sp+5]               
  8425: SSP      3                    
  8426: GCP      data[2077]            ; = 1
  8427: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8428: SSP      2                    
  8429: ASP      1                    
  8430: GCP      data[2078]            ; = 1
  8431: GCP      data[2079]            ; = 1
  8432: GCP      data[2080]            ; = 2
  8433: ASP      1                    
  8434: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8435: LLD      [sp+5]               
  8436: SSP      3                    
  8437: GCP      data[2081]            ; = 1
  8438: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8439: SSP      2                    
  8440: GCP      data[2082]            ; = 100
  8441: GADR     data[1757]           
  8442: ASGN                          
  8443: SSP      1                    
label_8444:
  8444: GCP      data[1757]           
  8445: GCP      data[2083]            ; = 100
  8446: NEQ                           
  8447: JZ       label_8519           
  8448: ASP      1                    
  8449: GCP      data[2084]            ; = 1
  8450: GCP      data[2085]            ; = 2
  8451: ASP      1                    
  8452: CALL     func_0371            
  8453: LLD      [sp+5]               
  8454: SSP      2                    
  8455: JZ       label_8519           
  8456: JMP      label_8457           
label_8457:
  8457: ASP      1                    
  8458: GCP      data[2086]            ; = 1
  8459: GCP      data[2087]            ; = 1
  8460: GCP      data[2088]            ; = 2
  8461: ASP      1                    
  8462: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8463: LLD      [sp+5]               
  8464: SSP      3                    
  8465: GCP      data[2089]            ; = 947
  8466: ASP      1                    
  8467: ASP      1                    
  8468: XCALL    $rand(void)int        ; args=0
  8469: LLD      [sp+7]               
  8470: GCP      data[2090]            ; = 2
  8471: MOD                           
  8472: ADD                           
  8473: LADR     [sp+0]               
  8474: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  8475: SSP      3                    
  8476: LCP      [sp+0]               
  8477: GCP      data[2091]            ; = 0.1f
  8478: FADD                          
  8479: LADR     [sp+0]               
  8480: ASGN                          
  8481: SSP      1                    
  8482: ASP      1                    
  8483: GCP      data[2092]            ; = 1
  8484: GCP      data[2093]            ; = 1
  8485: GCP      data[2094]            ; = 0.0f
  8486: ASP      1                    
  8487: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8488: LLD      [sp+5]               
  8489: SSP      3                    
  8490: GCP      data[2095]            ; = 1
  8491: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8492: SSP      2                    
  8493: ASP      1                    
  8494: GCP      data[2096]            ; = 1
  8495: GCP      data[2097]            ; = 1
  8496: GCP      data[2098]            ; = 1
  8497: ASP      1                    
  8498: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8499: LLD      [sp+5]               
  8500: SSP      3                    
  8501: GCP      data[2099]            ; = 1
  8502: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8503: SSP      2                    
  8504: ASP      1                    
  8505: GCP      data[2100]            ; = 1
  8506: GCP      data[2101]            ; = 1
  8507: GCP      data[2102]            ; = 2
  8508: ASP      1                    
  8509: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8510: LLD      [sp+5]               
  8511: SSP      3                    
  8512: GCP      data[2103]            ; = 1
  8513: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8514: SSP      2                    
  8515: GCP      data[2104]            ; = 100
  8516: GADR     data[1757]           
  8517: ASGN                          
  8518: SSP      1                    
label_8519:
  8519: GCP      data[1757]           
  8520: JMP      label_8522           
  8521: JMP      label_8526           
label_8522:
  8522: LCP      [sp+5]               
  8523: GCP      data[2105]            ; = 0.0f
  8524: EQU                           
  8525: JZ       label_8528           
label_8526:
  8526: JMP      label_8917           
  8527: JMP      label_8532           
label_8528:
  8528: LCP      [sp+5]               
  8529: GCP      data[2106]            ; = 1
  8530: EQU                           
  8531: JZ       label_8654           
label_8532:
  8532: ASP      1                    
  8533: GCP      data[2107]            ; = 1
  8534: GCP      data[2108]            ; = 1
  8535: GCP      data[2109]            ; = 0.0f
  8536: ASP      1                    
  8537: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8538: LLD      [sp+6]               
  8539: SSP      3                    
  8540: GCP      data[2110]            ; = 0.0f
  8541: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8542: SSP      2                    
  8543: ASP      1                    
  8544: GCP      data[2111]            ; = 1
  8545: GCP      data[2112]            ; = 1
  8546: GCP      data[2113]            ; = 1
  8547: ASP      1                    
  8548: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8549: LLD      [sp+6]               
  8550: SSP      3                    
  8551: GCP      data[2114]            ; = 0.0f
  8552: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8553: SSP      2                    
  8554: ASP      1                    
  8555: GCP      data[2115]            ; = 1
  8556: GCP      data[2116]            ; = 1
  8557: GCP      data[2117]            ; = 2
  8558: ASP      1                    
  8559: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8560: LLD      [sp+6]               
  8561: SSP      3                    
  8562: GCP      data[2118]            ; = 0.0f
  8563: XCALL    $SC_P_Ai_SetMode(unsignedlong,unsignedlong)void ; args=2
  8564: SSP      2                    
  8565: ASP      1                    
  8566: GCP      data[2119]            ; = 1
  8567: GCP      data[2120]            ; = 1
  8568: GCP      data[2121]            ; = 0.0f
  8569: ASP      1                    
  8570: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8571: LLD      [sp+6]               
  8572: SSP      3                    
  8573: XCALL    $SC_P_Ai_Stop(unsignedlong)void ; args=1
  8574: SSP      1                    
  8575: ASP      1                    
  8576: GCP      data[2122]            ; = 1
  8577: GCP      data[2123]            ; = 1
  8578: GCP      data[2124]            ; = 1
  8579: ASP      1                    
  8580: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8581: LLD      [sp+6]               
  8582: SSP      3                    
  8583: XCALL    $SC_P_Ai_Stop(unsignedlong)void ; args=1
  8584: SSP      1                    
  8585: ASP      1                    
  8586: GCP      data[2125]            ; = 1
  8587: GCP      data[2126]            ; = 1
  8588: GCP      data[2127]            ; = 2
  8589: ASP      1                    
  8590: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8591: LLD      [sp+6]               
  8592: SSP      3                    
  8593: XCALL    $SC_P_Ai_Stop(unsignedlong)void ; args=1
  8594: SSP      1                    
  8595: GCP      data[2128]            ; = 25.0f
  8596: ASP      1                    
  8597: GCP      data[2129]            ; = 20.0f
  8598: ASP      1                    
  8599: XCALL    $frnd(float)float     ; args=1
  8600: LLD      [sp+7]               
  8601: SSP      1                    
  8602: FADD                          
  8603: GADR     data[1760]           
  8604: ASGN                          
  8605: SSP      1                    
  8606: ASP      1                    
  8607: ASP      1                    
  8608: XCALL    $rand(void)int        ; args=0
  8609: LLD      [sp+6]               
  8610: GCP      data[2130]            ; = 2
  8611: MOD                           
  8612: GADR     data[1758]           
  8613: ASGN                          
  8614: SSP      1                    
  8615: ASP      1                    
  8616: GCP      data[2131]            ; = 1
  8617: GCP      data[2132]            ; = 1
  8618: GCP      data[1758]           
  8619: ASP      1                    
  8620: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8621: LLD      [sp+6]               
  8622: SSP      3                    
  8623: LADR     [sp+2]               
  8624: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  8625: SSP      2                    
  8626: ASP      1                    
  8627: GCP      data[2133]            ; = 1
  8628: GCP      data[2134]            ; = 1
  8629: GCP      data[2135]            ; = 2
  8630: ASP      1                    
  8631: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8632: LLD      [sp+6]               
  8633: SSP      3                    
  8634: LADR     [sp+2]               
  8635: XCALL    $SC_P_Ai_Go(unsignedlong,*c_Vector3)void ; args=2
  8636: SSP      2                    
  8637: ASP      1                    
  8638: GCP      data[2136]            ; = 1
  8639: GCP      data[2137]            ; = 1
  8640: GCP      data[2138]            ; = 2
  8641: ASP      1                    
  8642: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8643: LLD      [sp+6]               
  8644: SSP      3                    
  8645: GADR     data[1763]           
  8646: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  8647: SSP      2                    
  8648: GCP      data[2139]            ; = 2
  8649: GADR     data[1757]           
  8650: ASGN                          
  8651: SSP      1                    
  8652: JMP      label_8917           
  8653: JMP      label_8658           
label_8654:
  8654: LCP      [sp+5]               
  8655: GCP      data[2140]            ; = 2
  8656: EQU                           
  8657: JZ       label_8917           
label_8658:
  8658: GCP      data[1758]           
  8659: JMP      label_8661           
  8660: JMP      label_8665           
label_8661:
  8661: LCP      [sp+6]               
  8662: GCP      data[2141]            ; = 0.0f
  8663: EQU                           
  8664: JZ       label_8666           
label_8665:
  8665: JMP      label_8670           
label_8666:
  8666: LCP      [sp+6]               
  8667: GCP      data[2142]            ; = 1
  8668: EQU                           
  8669: JZ       label_8736           
label_8670:
  8670: ASP      1                    
  8671: ASP      1                    
  8672: GCP      data[2143]            ; = 1
  8673: GCP      data[2144]            ; = 1
  8674: GCP      data[2145]            ; = 2
  8675: ASP      1                    
  8676: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8677: LLD      [sp+8]               
  8678: SSP      3                    
  8679: ASP      1                    
  8680: GCP      data[2146]            ; = 1
  8681: GCP      data[2147]            ; = 1
  8682: GCP      data[1758]           
  8683: ASP      1                    
  8684: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8685: LLD      [sp+9]               
  8686: SSP      3                    
  8687: ASP      1                    
  8688: XCALL    $SC_P_GetDistance(unsignedlong,unsignedlong)float ; args=2
  8689: LLD      [sp+7]               
  8690: SSP      2                    
  8691: GCP      data[2148]            ; = 3.0f
  8692: FLES                          
  8693: JZ       label_8734           
  8694: ASP      1                    
  8695: GCP      data[2149]            ; = 1
  8696: GCP      data[2150]            ; = 1
  8697: GCP      data[2151]            ; = 2
  8698: ASP      1                    
  8699: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8700: LLD      [sp+7]               
  8701: SSP      3                    
  8702: GCP      data[2152]            ; = 945
  8703: ASP      1                    
  8704: ASP      1                    
  8705: XCALL    $rand(void)int        ; args=0
  8706: LLD      [sp+9]               
  8707: GCP      data[2153]            ; = 2
  8708: MOD                           
  8709: ADD                           
  8710: LADR     [sp+0]               
  8711: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  8712: SSP      3                    
  8713: LCP      [sp+0]               
  8714: GCP      data[2154]            ; = 0.1f
  8715: FADD                          
  8716: LADR     [sp+0]               
  8717: ASGN                          
  8718: SSP      1                    
  8719: ASP      1                    
  8720: GCP      data[2155]            ; = 1
  8721: GCP      data[2156]            ; = 1
  8722: GCP      data[2157]            ; = 2
  8723: ASP      1                    
  8724: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8725: LLD      [sp+7]               
  8726: SSP      3                    
  8727: GADR     data[1763]           
  8728: XCALL    $SC_P_Ai_Go(unsignedlong,*c_Vector3)void ; args=2
  8729: SSP      2                    
  8730: GCP      data[2158]            ; = 2
  8731: GADR     data[1758]           
  8732: ASGN                          
  8733: SSP      1                    
label_8734:
  8734: JMP      label_8788           
  8735: JMP      label_8740           
label_8736:
  8736: LCP      [sp+6]               
  8737: GCP      data[2159]            ; = 2
  8738: EQU                           
  8739: JZ       label_8788           
label_8740:
  8740: ASP      1                    
  8741: ASP      1                    
  8742: GCP      data[2160]            ; = 1
  8743: GCP      data[2161]            ; = 1
  8744: GCP      data[2162]            ; = 2
  8745: ASP      1                    
  8746: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8747: LLD      [sp+8]               
  8748: SSP      3                    
  8749: GADR     data[1763]           
  8750: GCP      data[2163]            ; = 3.0f
  8751: ASP      1                    
  8752: CALL     func_4180            
  8753: LLD      [sp+7]               
  8754: SSP      3                    
  8755: JZ       label_8787           
  8756: ASP      1                    
  8757: ASP      1                    
  8758: XCALL    $rand(void)int        ; args=0
  8759: LLD      [sp+7]               
  8760: GCP      data[2164]            ; = 2
  8761: MOD                           
  8762: GADR     data[1758]           
  8763: ASGN                          
  8764: SSP      1                    
  8765: ASP      1                    
  8766: GCP      data[2165]            ; = 1
  8767: GCP      data[2166]            ; = 1
  8768: GCP      data[1758]           
  8769: ASP      1                    
  8770: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8771: LLD      [sp+7]               
  8772: SSP      3                    
  8773: LADR     [sp+2]               
  8774: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  8775: SSP      2                    
  8776: ASP      1                    
  8777: GCP      data[2167]            ; = 1
  8778: GCP      data[2168]            ; = 1
  8779: GCP      data[2169]            ; = 2
  8780: ASP      1                    
  8781: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8782: LLD      [sp+7]               
  8783: SSP      3                    
  8784: LADR     [sp+2]               
  8785: XCALL    $SC_P_Ai_Go(unsignedlong,*c_Vector3)void ; args=2
  8786: SSP      2                    
label_8787:
  8787: JMP      label_8788           
label_8788:
  8788: SSP      1                    
  8789: GCP      data[1760]           
  8790: LCP      [sp-3]               
  8791: FSUB                          
  8792: GADR     data[1760]           
  8793: ASGN                          
  8794: SSP      1                    
  8795: GCP      data[1760]           
  8796: GCP      data[2170]            ; = 0.0f
  8797: FLES                          
  8798: JZ       label_8844           
  8799: GCP      data[2171]            ; = 25.0f
  8800: ASP      1                    
  8801: GCP      data[2172]            ; = 20.0f
  8802: ASP      1                    
  8803: XCALL    $frnd(float)float     ; args=1
  8804: LLD      [sp+7]               
  8805: SSP      1                    
  8806: FADD                          
  8807: GADR     data[1760]           
  8808: ASGN                          
  8809: SSP      1                    
  8810: GCP      data[2173]            ; = 0.0f
  8811: LADR     [sp+0]               
  8812: ASGN                          
  8813: SSP      1                    
  8814: ASP      1                    
  8815: GCP      data[2174]            ; = 1
  8816: GCP      data[2175]            ; = 1
  8817: ASP      1                    
  8818: ASP      1                    
  8819: XCALL    $rand(void)int        ; args=0
  8820: LLD      [sp+9]               
  8821: GCP      data[2176]            ; = 2
  8822: MOD                           
  8823: ASP      1                    
  8824: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8825: LLD      [sp+6]               
  8826: SSP      3                    
  8827: GCP      data[2177]            ; = 939
  8828: ASP      1                    
  8829: ASP      1                    
  8830: XCALL    $rand(void)int        ; args=0
  8831: LLD      [sp+8]               
  8832: GCP      data[2178]            ; = 3
  8833: MOD                           
  8834: ADD                           
  8835: LADR     [sp+0]               
  8836: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  8837: SSP      3                    
  8838: LCP      [sp+0]               
  8839: GCP      data[2179]            ; = 0.1f
  8840: FADD                          
  8841: LADR     [sp+0]               
  8842: ASGN                          
  8843: SSP      1                    
label_8844:
  8844: GCP      data[1949]           
  8845: LCP      [sp-3]               
  8846: FSUB                          
  8847: GADR     data[1949]           
  8848: ASGN                          
  8849: SSP      1                    
  8850: GCP      data[1949]           
  8851: GCP      data[2180]            ; = 0.0f
  8852: FLES                          
  8853: JZ       label_8880           
  8854: GCP      data[2181]            ; = 5.0f
  8855: ASP      1                    
  8856: GCP      data[2182]            ; = 5.0f
  8857: ASP      1                    
  8858: XCALL    $frnd(float)float     ; args=1
  8859: LLD      [sp+7]               
  8860: SSP      1                    
  8861: FADD                          
  8862: GADR     data[1949]           
  8863: ASGN                          
  8864: SSP      1                    
  8865: ASP      1                    
  8866: GCP      data[2183]            ; = 1
  8867: GCP      data[2184]            ; = 1
  8868: GCP      data[2185]            ; = 0.0f
  8869: ASP      1                    
  8870: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8871: LLD      [sp+6]               
  8872: SSP      3                    
  8873: LADR     [sp+2]               
  8874: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  8875: SSP      2                    
  8876: GCP      data[2186]            ; = 10419
  8877: LADR     [sp+2]               
  8878: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  8879: SSP      2                    
label_8880:
  8880: GCP      data[1950]           
  8881: LCP      [sp-3]               
  8882: FSUB                          
  8883: GADR     data[1950]           
  8884: ASGN                          
  8885: SSP      1                    
  8886: GCP      data[1950]           
  8887: GCP      data[2187]            ; = 0.0f
  8888: FLES                          
  8889: JZ       label_8916           
  8890: GCP      data[2188]            ; = 5.0f
  8891: ASP      1                    
  8892: GCP      data[2189]            ; = 5.0f
  8893: ASP      1                    
  8894: XCALL    $frnd(float)float     ; args=1
  8895: LLD      [sp+7]               
  8896: SSP      1                    
  8897: FADD                          
  8898: GADR     data[1950]           
  8899: ASGN                          
  8900: SSP      1                    
  8901: ASP      1                    
  8902: GCP      data[2190]            ; = 1
  8903: GCP      data[2191]            ; = 1
  8904: GCP      data[2192]            ; = 1
  8905: ASP      1                    
  8906: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  8907: LLD      [sp+6]               
  8908: SSP      3                    
  8909: LADR     [sp+2]               
  8910: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  8911: SSP      2                    
  8912: GCP      data[2193]            ; = 10419
  8913: LADR     [sp+2]               
  8914: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  8915: SSP      2                    
label_8916:
  8916: JMP      label_8917           
label_8917:
  8917: SSP      1                    
  8918: RET      5                    
func_8919:
  8919: GADR     data[2194]  ; "grenadebedna"
  8920: GADR     data[2198]           
  8921: XCALL    $SC_SetObjectScript(*char,*char)void ; args=2
  8922: SSP      2                    
  8923: GADR     data[2213]  ; "n_poklop_01"
  8924: GADR     data[2216]           
  8925: XCALL    $SC_SetObjectScript(*char,*char)void ; args=2
  8926: SSP      2                    
  8927: GADR     data[2229]  ; "d_past_04_01"
  8928: GADR     data[2233]           
  8929: XCALL    $SC_SetObjectScript(*char,*char)void ; args=2
  8930: SSP      2                    
  8931: RET      0                    
func_8932:
  8932: RET      0                    
func_8933:
  8933: RET      0                    
func_8934:
  8934: ASP      1                    
  8935: ASP      1                    
  8936: ASP      1                    
  8937: ASP      1                    
  8938: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  8939: LLD      [sp+2]               
  8940: ASP      1                    
  8941: XCALL    $SC_P_GetWillTalk(unsignedlong)float ; args=1
  8942: LLD      [sp+1]               
  8943: SSP      1                    
  8944: LADR     [sp+0]               
  8945: ASGN                          
  8946: SSP      1                    
  8947: GCP      data[1748]           
  8948: JZ       label_8950           
  8949: JMP      label_8985           
label_8950:
  8950: ASP      1                    
  8951: ASP      1                    
  8952: LADR     [sp-3]               
  8953: DADR     8                    
  8954: DCP      4                    
  8955: ASP      1                    
  8956: XCALL    $SC_NOD_GetName(*void)*char ; args=1
  8957: LLD      [sp+2]               
  8958: SSP      1                    
  8959: GADR     data[2246]  ; "grenadebedna"
  8960: ASP      1                    
  8961: XCALL    $SC_StringSame(*char,*char)int ; args=2
  8962: LLD      [sp+1]               
  8963: SSP      2                    
  8964: JZ       label_8985           
  8965: JMP      label_8966           
label_8966:
  8966: ASP      1                    
  8967: ASP      1                    
  8968: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  8969: LLD      [sp+1]               
  8970: GCP      data[2250]            ; = 923
  8971: LADR     [sp+0]               
  8972: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  8973: SSP      3                    
  8974: LCP      [sp+0]               
  8975: GCP      data[2251]            ; = 0.1f
  8976: FADD                          
  8977: LADR     [sp+0]               
  8978: ASGN                          
  8979: SSP      1                    
  8980: GCP      data[2252]            ; = 1
  8981: GADR     data[1748]           
  8982: ASGN                          
  8983: SSP      1                    
  8984: RET      1                    
label_8985:
  8985: GCP      data[1749]           
  8986: JZ       label_8988           
  8987: JMP      label_9023           
label_8988:
  8988: ASP      1                    
  8989: ASP      1                    
  8990: LADR     [sp-3]               
  8991: DADR     8                    
  8992: DCP      4                    
  8993: ASP      1                    
  8994: XCALL    $SC_NOD_GetName(*void)*char ; args=1
  8995: LLD      [sp+2]               
  8996: SSP      1                    
  8997: GADR     data[2253]  ; "n_poklop_01"
  8998: ASP      1                    
  8999: XCALL    $SC_StringSame(*char,*char)int ; args=2
  9000: LLD      [sp+1]               
  9001: SSP      2                    
  9002: JZ       label_9023           
  9003: JMP      label_9004           
label_9004:
  9004: ASP      1                    
  9005: ASP      1                    
  9006: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  9007: LLD      [sp+1]               
  9008: GCP      data[2256]            ; = 938
  9009: LADR     [sp+0]               
  9010: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  9011: SSP      3                    
  9012: LCP      [sp+0]               
  9013: GCP      data[2257]            ; = 0.1f
  9014: FADD                          
  9015: LADR     [sp+0]               
  9016: ASGN                          
  9017: SSP      1                    
  9018: GCP      data[2258]            ; = 1
  9019: GADR     data[1749]           
  9020: ASGN                          
  9021: SSP      1                    
  9022: RET      1                    
label_9023:
  9023: ASP      1                    
  9024: ASP      1                    
  9025: LADR     [sp-3]               
  9026: DADR     8                    
  9027: DCP      4                    
  9028: ASP      1                    
  9029: XCALL    $SC_NOD_GetName(*void)*char ; args=1
  9030: LLD      [sp+2]               
  9031: SSP      1                    
  9032: GADR     data[2259]  ; "granat_v_plechovce2#3"
  9033: ASP      1                    
  9034: XCALL    $SC_StringSame(*char,*char)int ; args=2
  9035: LLD      [sp+1]               
  9036: SSP      2                    
  9037: JZ       label_9053           
  9038: ASP      1                    
  9039: ASP      1                    
  9040: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  9041: LLD      [sp+1]               
  9042: GCP      data[2265]            ; = 925
  9043: LADR     [sp+0]               
  9044: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  9045: SSP      3                    
  9046: LCP      [sp+0]               
  9047: GCP      data[2266]            ; = 0.1f
  9048: FADD                          
  9049: LADR     [sp+0]               
  9050: ASGN                          
  9051: SSP      1                    
  9052: RET      1                    
label_9053:
  9053: RET      1                    
ScriptMain:
  9054: ASP      1                    
  9055: GCP      data[2267]            ; = 0.0f
  9056: ASP      2                    
  9057: ASP      5                    
  9058: ASP      3                    
  9059: ASP      8                    
  9060: GCP      data[2268]            ; = 0.2f
  9061: LADR     [sp-4]               
  9062: DADR     20                   
  9063: ASGN                          
  9064: SSP      1                    
  9065: LADR     [sp-4]               
  9066: DADR     0                    
  9067: DCP      4                    
  9068: JMP      label_9070           
  9069: JMP      label_9074           
label_9070:
  9070: LCP      [sp+20]              
  9071: GCP      data[2269]            ; = 7
  9072: EQU                           
  9073: JZ       label_9077           
label_9074:
  9074: CALL     func_8919            
  9075: JMP      label_10047          
  9076: JMP      label_9081           
label_9077:
  9077: LCP      [sp+20]              
  9078: GCP      data[2270]            ; = 11
  9079: EQU                           
  9080: JZ       label_9084           
label_9081:
  9081: CALL     func_8933            
  9082: JMP      label_10047          
  9083: JMP      label_9088           
label_9084:
  9084: LCP      [sp+20]              
  9085: GCP      data[2271]            ; = 8
  9086: EQU                           
  9087: JZ       label_9091           
label_9088:
  9088: CALL     func_8932            
  9089: JMP      label_10047          
  9090: JMP      label_9095           
label_9091:
  9091: LCP      [sp+20]              
  9092: GCP      data[2272]            ; = 4
  9093: EQU                           
  9094: JZ       label_9111           
label_9095:
  9095: LADR     [sp-4]               
  9096: DADR     4                    
  9097: DCP      4                    
  9098: JMP      label_9100           
  9099: JMP      label_9104           
label_9100:
  9100: LCP      [sp+21]              
  9101: GCP      data[2273]            ; = 51
  9102: EQU                           
  9103: JZ       label_9108           
label_9104:
  9104: LCP      [sp-4]               
  9105: CALL     func_8934            
  9106: SSP      1                    
  9107: JMP      label_9108           
label_9108:
  9108: SSP      1                    
  9109: JMP      label_10047          
  9110: JMP      label_9115           
label_9111:
  9111: LCP      [sp+20]              
  9112: GCP      data[2274]            ; = 0.0f
  9113: EQU                           
  9114: JZ       label_9439           
label_9115:
  9115: GCP      data[945]            
  9116: JMP      label_9118           
  9117: JMP      label_9122           
label_9118:
  9118: LCP      [sp+21]              
  9119: GCP      data[2275]            ; = 0.0f
  9120: EQU                           
  9121: JZ       label_9351           
label_9122:
  9122: GCP      data[2276]            ; = 200
  9123: GCP      data[2277]            ; = 9
  9124: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  9125: SSP      2                    
  9126: LADR     [sp+2]               
  9127: GCP      data[2278]            ; = 8
  9128: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  9129: SSP      2                    
  9130: LADR     [sp+4]               
  9131: GCP      data[2279]            ; = 20
  9132: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  9133: SSP      2                    
  9134: CALL     func_5197            
  9135: GCP      data[2280]            ; = 0.0f
  9136: XCALL    $SC_DeathCamera_Enable(int)void ; args=1
  9137: SSP      1                    
  9138: GCP      data[2281]            ; = 10.0f
  9139: XCALL    $SC_RadioSetDist(float)void ; args=1
  9140: SSP      1                    
  9141: ASP      2                    
  9142: LADR     [sp+22]              
  9143: GCP      data[2282]            ; = 8
  9144: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  9145: SSP      2                    
  9146: GCP      data[2283]            ; = 32
  9147: LADR     [sp+22]              
  9148: ASGN                          
  9149: SSP      1                    
  9150: GCP      data[2284]            ; = 8
  9151: LADR     [sp+22]              
  9152: PNT      4                    
  9153: ASGN                          
  9154: SSP      1                    
  9155: GCP      data[2285]            ; = 0.0f
  9156: LADR     [sp+22]              
  9157: XCALL    $SC_InitSide(unsignedlong,*s_SC_initside)void ; args=2
  9158: SSP      2                    
  9159: SSP      2                    
  9160: ASP      2                    
  9161: LADR     [sp+22]              
  9162: GCP      data[2286]            ; = 8
  9163: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  9164: SSP      2                    
  9165: GCP      data[2287]            ; = 64
  9166: LADR     [sp+22]              
  9167: ASGN                          
  9168: SSP      1                    
  9169: GCP      data[2288]            ; = 16
  9170: LADR     [sp+22]              
  9171: PNT      4                    
  9172: ASGN                          
  9173: SSP      1                    
  9174: GCP      data[2289]            ; = 1
  9175: LADR     [sp+22]              
  9176: XCALL    $SC_InitSide(unsignedlong,*s_SC_initside)void ; args=2
  9177: SSP      2                    
  9178: SSP      2                    
  9179: ASP      5                    
  9180: LADR     [sp+22]              
  9181: GCP      data[2290]            ; = 20
  9182: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  9183: SSP      2                    
  9184: GCP      data[2291]            ; = 0.0f
  9185: LADR     [sp+22]              
  9186: ASGN                          
  9187: SSP      1                    
  9188: GCP      data[2292]            ; = 0.0f
  9189: LADR     [sp+22]              
  9190: PNT      4                    
  9191: ASGN                          
  9192: SSP      1                    
  9193: GCP      data[2293]            ; = 4
  9194: LADR     [sp+22]              
  9195: PNT      8                    
  9196: ASGN                          
  9197: SSP      1                    
  9198: GCP      data[2294]            ; = 30.0f
  9199: LADR     [sp+22]              
  9200: PNT      16                   
  9201: ASGN                          
  9202: SSP      1                    
  9203: LADR     [sp+22]              
  9204: XCALL    $SC_InitSideGroup(*s_SC_initgroup)void ; args=1
  9205: SSP      1                    
  9206: SSP      5                    
  9207: ASP      5                    
  9208: LADR     [sp+22]              
  9209: GCP      data[2295]            ; = 20
  9210: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  9211: SSP      2                    
  9212: GCP      data[2296]            ; = 1
  9213: LADR     [sp+22]              
  9214: ASGN                          
  9215: SSP      1                    
  9216: GCP      data[2297]            ; = 0.0f
  9217: LADR     [sp+22]              
  9218: PNT      4                    
  9219: ASGN                          
  9220: SSP      1                    
  9221: GCP      data[2298]            ; = 9
  9222: LADR     [sp+22]              
  9223: PNT      8                    
  9224: ASGN                          
  9225: SSP      1                    
  9226: LADR     [sp+22]              
  9227: XCALL    $SC_InitSideGroup(*s_SC_initgroup)void ; args=1
  9228: SSP      1                    
  9229: SSP      5                    
  9230: ASP      5                    
  9231: LADR     [sp+22]              
  9232: GCP      data[2299]            ; = 20
  9233: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  9234: SSP      2                    
  9235: GCP      data[2300]            ; = 1
  9236: LADR     [sp+22]              
  9237: ASGN                          
  9238: SSP      1                    
  9239: GCP      data[2301]            ; = 1
  9240: LADR     [sp+22]              
  9241: PNT      4                    
  9242: ASGN                          
  9243: SSP      1                    
  9244: GCP      data[2302]            ; = 16
  9245: LADR     [sp+22]              
  9246: PNT      8                    
  9247: ASGN                          
  9248: SSP      1                    
  9249: LADR     [sp+22]              
  9250: XCALL    $SC_InitSideGroup(*s_SC_initgroup)void ; args=1
  9251: SSP      1                    
  9252: SSP      5                    
  9253: ASP      5                    
  9254: LADR     [sp+22]              
  9255: GCP      data[2303]            ; = 20
  9256: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  9257: SSP      2                    
  9258: GCP      data[2304]            ; = 1
  9259: LADR     [sp+22]              
  9260: ASGN                          
  9261: SSP      1                    
  9262: GCP      data[2305]            ; = 2
  9263: LADR     [sp+22]              
  9264: PNT      4                    
  9265: ASGN                          
  9266: SSP      1                    
  9267: GCP      data[2306]            ; = 16
  9268: LADR     [sp+22]              
  9269: PNT      8                    
  9270: ASGN                          
  9271: SSP      1                    
  9272: LADR     [sp+22]              
  9273: XCALL    $SC_InitSideGroup(*s_SC_initgroup)void ; args=1
  9274: SSP      1                    
  9275: SSP      5                    
  9276: ASP      5                    
  9277: LADR     [sp+22]              
  9278: GCP      data[2307]            ; = 20
  9279: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  9280: SSP      2                    
  9281: GCP      data[2308]            ; = 1
  9282: LADR     [sp+22]              
  9283: ASGN                          
  9284: SSP      1                    
  9285: GCP      data[2309]            ; = 3
  9286: LADR     [sp+22]              
  9287: PNT      4                    
  9288: ASGN                          
  9289: SSP      1                    
  9290: GCP      data[2310]            ; = 9
  9291: LADR     [sp+22]              
  9292: PNT      8                    
  9293: ASGN                          
  9294: SSP      1                    
  9295: LADR     [sp+22]              
  9296: XCALL    $SC_InitSideGroup(*s_SC_initgroup)void ; args=1
  9297: SSP      1                    
  9298: SSP      5                    
  9299: GCP      data[2311]            ; = 1
  9300: XCALL    $SC_Ai_SetShootOnHeardEnemyColTest(int)void ; args=1
  9301: SSP      1                    
  9302: GCP      data[2312]            ; = 1
  9303: GCP      data[2313]            ; = 0.0f
  9304: GCP      data[2314]            ; = 0.0f
  9305: XCALL    $SC_Ai_SetGroupEnemyUpdate(unsignedlong,unsignedlong,int)void ; args=3
  9306: SSP      3                    
  9307: GCP      data[2315]            ; = 1
  9308: GCP      data[2316]            ; = 1
  9309: GCP      data[2317]            ; = 0.0f
  9310: XCALL    $SC_Ai_SetGroupEnemyUpdate(unsignedlong,unsignedlong,int)void ; args=3
  9311: SSP      3                    
  9312: GCP      data[2318]            ; = 1
  9313: GCP      data[2319]            ; = 2
  9314: GCP      data[2320]            ; = 0.0f
  9315: XCALL    $SC_Ai_SetGroupEnemyUpdate(unsignedlong,unsignedlong,int)void ; args=3
  9316: SSP      3                    
  9317: GCP      data[2321]            ; = 1
  9318: GCP      data[2322]            ; = 3
  9319: GCP      data[2323]            ; = 0.0f
  9320: XCALL    $SC_Ai_SetGroupEnemyUpdate(unsignedlong,unsignedlong,int)void ; args=3
  9321: SSP      3                    
  9322: GCP      data[2324]            ; = 1
  9323: GADR     data[945]            
  9324: ASGN                          
  9325: SSP      1                    
  9326: GCP      data[2325]            ; = 6
  9327: GCP      data[2326]            ; = 1
  9328: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  9329: SSP      2                    
  9330: GCP      data[2327]            ; = 3
  9331: GADR     data[2328]  ; "Levelphase changed to %d"
  9332: GCP      data[2335]            ; = 1
  9333: GCP      data[2336]            ; = 3
  9334: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  9335: SSP      3                    
  9336: GADR     data[2337]  ; "Levelphase changed to %d"
  9337: GCP      data[2344]            ; = 1
  9338: GCP      data[2345]            ; = 2
  9339: XCALL    $SC_Osi(*char,...)void ; args=4294967295
  9340: SSP      2                    
  9341: GCP      data[2346]            ; = 2009
  9342: XCALL    $SC_SetCommandMenu(unsignedlong)void ; args=1
  9343: SSP      1                    
  9344: GCP      data[2347]            ; = 0.5f
  9345: LADR     [sp-4]               
  9346: DADR     20                   
  9347: ASGN                          
  9348: SSP      1                    
  9349: JMP      label_9436           
  9350: JMP      label_9355           
label_9351:
  9351: LCP      [sp+21]              
  9352: GCP      data[2348]            ; = 1
  9353: EQU                           
  9354: JZ       label_9412           
label_9355:
  9355: GCP      data[2349]            ; = 1.0f
  9356: LADR     [sp+1]               
  9357: ASGN                          
  9358: SSP      1                    
  9359: ASP      1                    
  9360: GCP      data[2350]            ; = 0.0f
  9361: ASP      1                    
  9362: XCALL    $SC_AGS_Set(unsignedlong)unsignedlong ; args=1
  9363: LLD      [sp+22]              
  9364: SSP      1                    
  9365: SSP      1                    
  9366: ASP      1                    
  9367: ASP      1                    
  9368: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  9369: LLD      [sp+22]              
  9370: GCP      data[2351]            ; = 900
  9371: LADR     [sp+1]               
  9372: GCP      data[2352]            ; = 1
  9373: XCALL    $SC_P_SpeechMes2(unsignedlong,unsignedlong,*float,unsignedlong)void ; args=4
  9374: SSP      4                    
  9375: LCP      [sp+1]               
  9376: GCP      data[2353]            ; = 0.1f
  9377: FADD                          
  9378: LADR     [sp+1]               
  9379: ASGN                          
  9380: SSP      1                    
  9381: GCP      data[2354]            ; = 901
  9382: CALL     func_4948            
  9383: SSP      1                    
  9384: GCP      data[2355]            ; = 902
  9385: CALL     func_4948            
  9386: SSP      1                    
  9387: GCP      data[2356]            ; = 1475
  9388: CALL     func_4948            
  9389: SSP      1                    
  9390: CALL     func_6873            
  9391: GCP      data[2357]            ; = 2
  9392: GADR     data[945]            
  9393: ASGN                          
  9394: SSP      1                    
  9395: GCP      data[2358]            ; = 6
  9396: GCP      data[2359]            ; = 2
  9397: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  9398: SSP      2                    
  9399: GCP      data[2360]            ; = 3
  9400: GADR     data[2361]  ; "Levelphase changed to %d"
  9401: GCP      data[2368]            ; = 2
  9402: GCP      data[2369]            ; = 3
  9403: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  9404: SSP      3                    
  9405: GADR     data[2370]  ; "Levelphase changed to %d"
  9406: GCP      data[2377]            ; = 2
  9407: GCP      data[2378]            ; = 2
  9408: XCALL    $SC_Osi(*char,...)void ; args=4294967295
  9409: SSP      2                    
  9410: JMP      label_9436           
  9411: JMP      label_9416           
label_9412:
  9412: LCP      [sp+21]              
  9413: GCP      data[2379]            ; = 2
  9414: EQU                           
  9415: JZ       label_9436           
label_9416:
  9416: ASP      1                    
  9417: LADR     [sp+9]               
  9418: ASP      1                    
  9419: XCALL    $SC_PC_GetPos(*c_Vector3)int ; args=1
  9420: LLD      [sp+22]              
  9421: SSP      1                    
  9422: SSP      1                    
  9423: LADR     [sp+9]               
  9424: LADR     [sp-4]               
  9425: DADR     16                   
  9426: DCP      4                    
  9427: CALL     func_7697            
  9428: SSP      2                    
  9429: LADR     [sp+9]               
  9430: LADR     [sp-4]               
  9431: DADR     16                   
  9432: DCP      4                    
  9433: CALL     func_7807            
  9434: SSP      2                    
  9435: JMP      label_9436           
label_9436:
  9436: SSP      1                    
  9437: JMP      label_10047          
  9438: JMP      label_9443           
label_9439:
  9439: LCP      [sp+20]              
  9440: GCP      data[2380]            ; = 1
  9441: EQU                           
  9442: JZ       label_9682           
label_9443:
  9443: ASP      1                    
  9444: ASP      1                    
  9445: ASP      1                    
  9446: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  9447: LLD      [sp+22]              
  9448: ASP      1                    
  9449: XCALL    $SC_P_GetWillTalk(unsignedlong)float ; args=1
  9450: LLD      [sp+21]              
  9451: SSP      1                    
  9452: LADR     [sp+1]               
  9453: ASGN                          
  9454: SSP      1                    
  9455: GCP      data[2381]            ; = 0.0f
  9456: XCALL    $SC_PC_EnableMovement(int)void ; args=1
  9457: SSP      1                    
  9458: GCP      data[2382]            ; = 1
  9459: XCALL    $SC_PC_EnableRadioBreak(int)void ; args=1
  9460: SSP      1                    
  9461: LADR     [sp-4]               
  9462: DADR     4                    
  9463: DCP      4                    
  9464: JMP      label_9466           
  9465: JMP      label_9470           
label_9466:
  9466: LCP      [sp+21]              
  9467: GCP      data[2383]            ; = 1
  9468: EQU                           
  9469: JZ       label_9573           
label_9470:
  9470: XCALL    $SC_RadioBatch_Begin(void)void ; args=0
  9471: ASP      1                    
  9472: ASP      1                    
  9473: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  9474: LLD      [sp+22]              
  9475: GCP      data[2384]            ; = 916
  9476: LADR     [sp+1]               
  9477: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  9478: SSP      3                    
  9479: LCP      [sp+1]               
  9480: GCP      data[2385]            ; = 0.1f
  9481: FADD                          
  9482: LADR     [sp+1]               
  9483: ASGN                          
  9484: SSP      1                    
  9485: LCP      [sp+1]               
  9486: ASP      1                    
  9487: GCP      data[2386]            ; = 0.3f
  9488: ASP      1                    
  9489: CALL     func_0291            
  9490: LLD      [sp+23]              
  9491: SSP      1                    
  9492: FADD                          
  9493: LADR     [sp+1]               
  9494: ASGN                          
  9495: SSP      1                    
  9496: GCP      data[2387]            ; = 917
  9497: LADR     [sp+1]               
  9498: XCALL    $SC_SpeechRadio2(unsignedlong,*float)void ; args=2
  9499: SSP      2                    
  9500: LCP      [sp+1]               
  9501: GCP      data[2388]            ; = 0.1f
  9502: ASP      1                    
  9503: GCP      data[2389]            ; = 0.2f
  9504: ASP      1                    
  9505: CALL     func_0291            
  9506: LLD      [sp+24]              
  9507: SSP      1                    
  9508: FADD                          
  9509: FADD                          
  9510: LADR     [sp+1]               
  9511: ASGN                          
  9512: SSP      1                    
  9513: ASP      1                    
  9514: ASP      1                    
  9515: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  9516: LLD      [sp+22]              
  9517: GCP      data[2390]            ; = 918
  9518: LADR     [sp+1]               
  9519: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  9520: SSP      3                    
  9521: LCP      [sp+1]               
  9522: GCP      data[2391]            ; = 0.1f
  9523: FADD                          
  9524: LADR     [sp+1]               
  9525: ASGN                          
  9526: SSP      1                    
  9527: LCP      [sp+1]               
  9528: ASP      1                    
  9529: GCP      data[2392]            ; = 0.3f
  9530: ASP      1                    
  9531: CALL     func_0291            
  9532: LLD      [sp+23]              
  9533: SSP      1                    
  9534: FADD                          
  9535: LADR     [sp+1]               
  9536: ASGN                          
  9537: SSP      1                    
  9538: GCP      data[2393]            ; = 919
  9539: LADR     [sp+1]               
  9540: XCALL    $SC_SpeechRadio2(unsignedlong,*float)void ; args=2
  9541: SSP      2                    
  9542: LCP      [sp+1]               
  9543: GCP      data[2394]            ; = 0.1f
  9544: ASP      1                    
  9545: GCP      data[2395]            ; = 0.2f
  9546: ASP      1                    
  9547: CALL     func_0291            
  9548: LLD      [sp+24]              
  9549: SSP      1                    
  9550: FADD                          
  9551: FADD                          
  9552: LADR     [sp+1]               
  9553: ASGN                          
  9554: SSP      1                    
  9555: ASP      1                    
  9556: ASP      1                    
  9557: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  9558: LLD      [sp+22]              
  9559: GCP      data[2396]            ; = 920
  9560: LADR     [sp+1]               
  9561: GCP      data[2397]            ; = 2
  9562: XCALL    $SC_P_SpeechMes2(unsignedlong,unsignedlong,*float,unsignedlong)void ; args=4
  9563: SSP      4                    
  9564: LCP      [sp+1]               
  9565: GCP      data[2398]            ; = 0.1f
  9566: FADD                          
  9567: LADR     [sp+1]               
  9568: ASGN                          
  9569: SSP      1                    
  9570: XCALL    $SC_RadioBatch_End(void)void ; args=0
  9571: JMP      label_9679           
  9572: JMP      label_9577           
label_9573:
  9573: LCP      [sp+21]              
  9574: GCP      data[2399]            ; = 2
  9575: EQU                           
  9576: JZ       label_9679           
label_9577:
  9577: XCALL    $SC_RadioBatch_Begin(void)void ; args=0
  9578: ASP      1                    
  9579: ASP      1                    
  9580: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  9581: LLD      [sp+22]              
  9582: GCP      data[2400]            ; = 933
  9583: LADR     [sp+1]               
  9584: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  9585: SSP      3                    
  9586: LCP      [sp+1]               
  9587: GCP      data[2401]            ; = 0.1f
  9588: FADD                          
  9589: LADR     [sp+1]               
  9590: ASGN                          
  9591: SSP      1                    
  9592: LCP      [sp+1]               
  9593: ASP      1                    
  9594: GCP      data[2402]            ; = 0.3f
  9595: ASP      1                    
  9596: CALL     func_0291            
  9597: LLD      [sp+23]              
  9598: SSP      1                    
  9599: FADD                          
  9600: LADR     [sp+1]               
  9601: ASGN                          
  9602: SSP      1                    
  9603: GCP      data[2403]            ; = 934
  9604: LADR     [sp+1]               
  9605: XCALL    $SC_SpeechRadio2(unsignedlong,*float)void ; args=2
  9606: SSP      2                    
  9607: LCP      [sp+1]               
  9608: GCP      data[2404]            ; = 0.1f
  9609: ASP      1                    
  9610: GCP      data[2405]            ; = 0.2f
  9611: ASP      1                    
  9612: CALL     func_0291            
  9613: LLD      [sp+24]              
  9614: SSP      1                    
  9615: FADD                          
  9616: FADD                          
  9617: LADR     [sp+1]               
  9618: ASGN                          
  9619: SSP      1                    
  9620: ASP      1                    
  9621: ASP      1                    
  9622: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  9623: LLD      [sp+22]              
  9624: GCP      data[2406]            ; = 935
  9625: LADR     [sp+1]               
  9626: XCALL    $SC_P_Speech2(unsignedlong,unsignedlong,*float)void ; args=3
  9627: SSP      3                    
  9628: LCP      [sp+1]               
  9629: GCP      data[2407]            ; = 0.1f
  9630: FADD                          
  9631: LADR     [sp+1]               
  9632: ASGN                          
  9633: SSP      1                    
  9634: LCP      [sp+1]               
  9635: ASP      1                    
  9636: GCP      data[2408]            ; = 0.3f
  9637: ASP      1                    
  9638: CALL     func_0291            
  9639: LLD      [sp+23]              
  9640: SSP      1                    
  9641: FADD                          
  9642: LADR     [sp+1]               
  9643: ASGN                          
  9644: SSP      1                    
  9645: GCP      data[2409]            ; = 936
  9646: LADR     [sp+1]               
  9647: XCALL    $SC_SpeechRadio2(unsignedlong,*float)void ; args=2
  9648: SSP      2                    
  9649: LCP      [sp+1]               
  9650: GCP      data[2410]            ; = 0.1f
  9651: ASP      1                    
  9652: GCP      data[2411]            ; = 0.2f
  9653: ASP      1                    
  9654: CALL     func_0291            
  9655: LLD      [sp+24]              
  9656: SSP      1                    
  9657: FADD                          
  9658: FADD                          
  9659: LADR     [sp+1]               
  9660: ASGN                          
  9661: SSP      1                    
  9662: ASP      1                    
  9663: ASP      1                    
  9664: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  9665: LLD      [sp+22]              
  9666: GCP      data[2412]            ; = 937
  9667: LADR     [sp+1]               
  9668: GCP      data[2413]            ; = 3
  9669: XCALL    $SC_P_SpeechMes2(unsignedlong,unsignedlong,*float,unsignedlong)void ; args=4
  9670: SSP      4                    
  9671: LCP      [sp+1]               
  9672: GCP      data[2414]            ; = 0.1f
  9673: FADD                          
  9674: LADR     [sp+1]               
  9675: ASGN                          
  9676: SSP      1                    
  9677: XCALL    $SC_RadioBatch_End(void)void ; args=0
  9678: JMP      label_9679           
label_9679:
  9679: SSP      1                    
  9680: JMP      label_10047          
  9681: JMP      label_9686           
label_9682:
  9682: LCP      [sp+20]              
  9683: GCP      data[2415]            ; = 2
  9684: EQU                           
  9685: JZ       label_10012          
label_9686:
  9686: LADR     [sp-4]               
  9687: DADR     4                    
  9688: DCP      4                    
  9689: JMP      label_9691           
  9690: JMP      label_9695           
label_9691:
  9691: LCP      [sp+21]              
  9692: GCP      data[2416]            ; = 1
  9693: EQU                           
  9694: JZ       label_9747           
label_9695:
  9695: GADR     data[1732]           
  9696: LADR     [sp-4]               
  9697: DADR     4                    
  9698: DCP      4                    
  9699: GCP      data[2417]            ; = 4
  9700: MUL                           
  9701: ADD                           
  9702: DCP      4                    
  9703: JZ       label_9705           
  9704: JMP      label_9745           
label_9705:
  9705: GCP      data[2418]            ; = 1
  9706: GADR     data[1732]           
  9707: LADR     [sp-4]               
  9708: DADR     4                    
  9709: DCP      4                    
  9710: GCP      data[2419]            ; = 4
  9711: MUL                           
  9712: ADD                           
  9713: ASGN                          
  9714: SSP      1                    
  9715: ASP      3                    
  9716: GCP      data[2420]            ; = 0.0f
  9717: LADR     [sp+22]              
  9718: PNT      8                    
  9719: ASGN                          
  9720: SSP      1                    
  9721: GCP      data[2421]            ; = 9110
  9722: LADR     [sp+22]              
  9723: ASGN                          
  9724: SSP      1                    
  9725: GCP      data[2422]            ; = 9111
  9726: LADR     [sp+22]              
  9727: PNT      4                    
  9728: ASGN                          
  9729: SSP      1                    
  9730: LADR     [sp+22]              
  9731: XCALL    $SC_MissionSave(*s_SC_MissionSave)void ; args=1
  9732: SSP      1                    
  9733: GCP      data[2423]            ; = 3
  9734: GADR     data[2424]  ; "Saving game id %d"
  9735: GCP      data[2429]            ; = 9110
  9736: GCP      data[2430]            ; = 3
  9737: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  9738: SSP      3                    
  9739: GADR     data[2431]  ; "Saving game id %d"
  9740: GCP      data[2436]            ; = 9110
  9741: GCP      data[2437]            ; = 2
  9742: XCALL    $SC_Osi(*char,...)void ; args=4294967295
  9743: SSP      2                    
  9744: SSP      3                    
label_9745:
  9745: JMP      label_10009          
  9746: JMP      label_9751           
label_9747:
  9747: LCP      [sp+21]              
  9748: GCP      data[2438]            ; = 2
  9749: EQU                           
  9750: JZ       label_9806           
label_9751:
  9751: GADR     data[1732]           
  9752: LADR     [sp-4]               
  9753: DADR     4                    
  9754: DCP      4                    
  9755: GCP      data[2439]            ; = 4
  9756: MUL                           
  9757: ADD                           
  9758: DCP      4                    
  9759: JZ       label_9761           
  9760: JMP      label_9804           
label_9761:
  9761: GCP      data[2440]            ; = 1
  9762: GADR     data[1732]           
  9763: LADR     [sp-4]               
  9764: DADR     4                    
  9765: DCP      4                    
  9766: GCP      data[2441]            ; = 4
  9767: MUL                           
  9768: ADD                           
  9769: ASGN                          
  9770: SSP      1                    
  9771: GCP      data[2442]            ; = 1
  9772: XCALL    $SC_PC_EnableMovement(int)void ; args=1
  9773: SSP      1                    
  9774: ASP      3                    
  9775: GCP      data[2443]            ; = 0.0f
  9776: LADR     [sp+22]              
  9777: PNT      8                    
  9778: ASGN                          
  9779: SSP      1                    
  9780: GCP      data[2444]            ; = 9112
  9781: LADR     [sp+22]              
  9782: ASGN                          
  9783: SSP      1                    
  9784: GCP      data[2445]            ; = 9113
  9785: LADR     [sp+22]              
  9786: PNT      4                    
  9787: ASGN                          
  9788: SSP      1                    
  9789: LADR     [sp+22]              
  9790: XCALL    $SC_MissionSave(*s_SC_MissionSave)void ; args=1
  9791: SSP      1                    
  9792: GCP      data[2446]            ; = 3
  9793: GADR     data[2447]  ; "Saving game id %d"
  9794: GCP      data[2452]            ; = 9112
  9795: GCP      data[2453]            ; = 3
  9796: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  9797: SSP      3                    
  9798: GADR     data[2454]  ; "Saving game id %d"
  9799: GCP      data[2459]            ; = 9112
  9800: GCP      data[2460]            ; = 2
  9801: XCALL    $SC_Osi(*char,...)void ; args=4294967295
  9802: SSP      2                    
  9803: SSP      3                    
label_9804:
  9804: JMP      label_10009          
  9805: JMP      label_9810           
label_9806:
  9806: LCP      [sp+21]              
  9807: GCP      data[2461]            ; = 3
  9808: EQU                           
  9809: JZ       label_9865           
label_9810:
  9810: GADR     data[1732]           
  9811: LADR     [sp-4]               
  9812: DADR     4                    
  9813: DCP      4                    
  9814: GCP      data[2462]            ; = 4
  9815: MUL                           
  9816: ADD                           
  9817: DCP      4                    
  9818: JZ       label_9820           
  9819: JMP      label_9863           
label_9820:
  9820: GCP      data[2463]            ; = 1
  9821: GADR     data[1732]           
  9822: LADR     [sp-4]               
  9823: DADR     4                    
  9824: DCP      4                    
  9825: GCP      data[2464]            ; = 4
  9826: MUL                           
  9827: ADD                           
  9828: ASGN                          
  9829: SSP      1                    
  9830: GCP      data[2465]            ; = 1
  9831: XCALL    $SC_PC_EnableMovement(int)void ; args=1
  9832: SSP      1                    
  9833: ASP      3                    
  9834: GCP      data[2466]            ; = 0.0f
  9835: LADR     [sp+22]              
  9836: PNT      8                    
  9837: ASGN                          
  9838: SSP      1                    
  9839: GCP      data[2467]            ; = 9114
  9840: LADR     [sp+22]              
  9841: ASGN                          
  9842: SSP      1                    
  9843: GCP      data[2468]            ; = 9115
  9844: LADR     [sp+22]              
  9845: PNT      4                    
  9846: ASGN                          
  9847: SSP      1                    
  9848: LADR     [sp+22]              
  9849: XCALL    $SC_MissionSave(*s_SC_MissionSave)void ; args=1
  9850: SSP      1                    
  9851: GCP      data[2469]            ; = 3
  9852: GADR     data[2470]  ; "Saving game id %d"
  9853: GCP      data[2475]            ; = 9114
  9854: GCP      data[2476]            ; = 3
  9855: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  9856: SSP      3                    
  9857: GADR     data[2477]  ; "Saving game id %d"
  9858: GCP      data[2482]            ; = 9114
  9859: GCP      data[2483]            ; = 2
  9860: XCALL    $SC_Osi(*char,...)void ; args=4294967295
  9861: SSP      2                    
  9862: SSP      3                    
label_9863:
  9863: JMP      label_10009          
  9864: JMP      label_9869           
label_9865:
  9865: LCP      [sp+21]              
  9866: GCP      data[2484]            ; = 11
  9867: EQU                           
  9868: JZ       label_9874           
label_9869:
  9869: GCP      data[2485]            ; = 1
  9870: XCALL    $SC_Radio_Enable(unsignedlong)void ; args=1
  9871: SSP      1                    
  9872: JMP      label_10009          
  9873: JMP      label_9878           
label_9874:
  9874: LCP      [sp+21]              
  9875: GCP      data[2486]            ; = 12
  9876: EQU                           
  9877: JZ       label_9895           
label_9878:
  9878: ASP      1                    
  9879: GCP      data[2487]            ; = 1
  9880: GCP      data[2488]            ; = 0.0f
  9881: GCP      data[2489]            ; = 0.0f
  9882: ASP      1                    
  9883: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  9884: LLD      [sp+22]              
  9885: SSP      3                    
  9886: LADR     [sp+9]               
  9887: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  9888: SSP      2                    
  9889: GCP      data[2490]            ; = 2055
  9890: LADR     [sp+9]               
  9891: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  9892: SSP      2                    
  9893: JMP      label_10009          
  9894: JMP      label_9899           
label_9895:
  9895: LCP      [sp+21]              
  9896: GCP      data[2491]            ; = 13
  9897: EQU                           
  9898: JZ       label_9969           
label_9899:
  9899: ASP      1                    
  9900: GCP      data[2492]            ; = 1
  9901: GCP      data[2493]            ; = 0.0f
  9902: GCP      data[2494]            ; = 0.0f
  9903: ASP      1                    
  9904: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  9905: LLD      [sp+22]              
  9906: SSP      3                    
  9907: LADR     [sp+9]               
  9908: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  9909: SSP      2                    
  9910: GCP      data[2495]            ; = 2060
  9911: LADR     [sp+9]               
  9912: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  9913: SSP      2                    
  9914: ASP      1                    
  9915: GCP      data[2496]            ; = 1
  9916: GCP      data[2497]            ; = 0.0f
  9917: GCP      data[2498]            ; = 1
  9918: ASP      1                    
  9919: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  9920: LLD      [sp+22]              
  9921: SSP      3                    
  9922: LADR     [sp+9]               
  9923: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  9924: SSP      2                    
  9925: GCP      data[2499]            ; = 2070
  9926: LADR     [sp+9]               
  9927: XCALL    $SC_SND_PlaySound3D(unsignedlong,*c_Vector3)void ; args=2
  9928: SSP      2                    
  9929: ASP      1                    
  9930: GADR     data[2500]  ; "WayPoint53"
  9931: LADR     [sp+9]               
  9932: ASP      1                    
  9933: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  9934: LLD      [sp+22]              
  9935: SSP      2                    
  9936: SSP      1                    
  9937: ASP      1                    
  9938: GCP      data[2503]            ; = 1
  9939: GCP      data[2504]            ; = 0.0f
  9940: GCP      data[2505]            ; = 0.0f
  9941: ASP      1                    
  9942: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  9943: LLD      [sp+22]              
  9944: SSP      3                    
  9945: LADR     [sp+9]               
  9946: XCALL    $SC_P_SetPos(unsignedlong,*c_Vector3)void ; args=2
  9947: SSP      2                    
  9948: ASP      1                    
  9949: GADR     data[2506]  ; "WayPoint#9"
  9950: LADR     [sp+9]               
  9951: ASP      1                    
  9952: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  9953: LLD      [sp+22]              
  9954: SSP      2                    
  9955: SSP      1                    
  9956: ASP      1                    
  9957: GCP      data[2509]            ; = 1
  9958: GCP      data[2510]            ; = 0.0f
  9959: GCP      data[2511]            ; = 1
  9960: ASP      1                    
  9961: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  9962: LLD      [sp+22]              
  9963: SSP      3                    
  9964: LADR     [sp+9]               
  9965: XCALL    $SC_P_SetPos(unsignedlong,*c_Vector3)void ; args=2
  9966: SSP      2                    
  9967: JMP      label_10009          
  9968: JMP      label_9973           
label_9969:
  9969: LCP      [sp+21]              
  9970: GCP      data[2512]            ; = 14
  9971: EQU                           
  9972: JZ       label_9994           
label_9973:
  9973: ASP      1                    
  9974: GADR     data[2513]  ; "WayPoint57"
  9975: LADR     [sp+9]               
  9976: ASP      1                    
  9977: XCALL    $SC_GetWp(*char,*c_Vector3)int ; args=2
  9978: LLD      [sp+22]              
  9979: SSP      2                    
  9980: SSP      1                    
  9981: ASP      1                    
  9982: GCP      data[2516]            ; = 1
  9983: GCP      data[2517]            ; = 0.0f
  9984: GCP      data[2518]            ; = 0.0f
  9985: ASP      1                    
  9986: XCALL    $SC_P_GetBySideGroupMember(unsignedlong,unsignedlong,unsignedlong)unsignedlong ; args=3
  9987: LLD      [sp+22]              
  9988: SSP      3                    
  9989: LADR     [sp+9]               
  9990: XCALL    $SC_P_SetPos(unsignedlong,*c_Vector3)void ; args=2
  9991: SSP      2                    
  9992: JMP      label_10009          
  9993: JMP      label_9998           
label_9994:
  9994: LCP      [sp+21]              
  9995: GCP      data[2519]            ; = 15
  9996: EQU                           
  9997: JZ       label_10003          
label_9998:
  9998: GCP      data[2520]            ; = 2
  9999: XCALL    $SC_Radio_Enable(unsignedlong)void ; args=1
  10000: SSP      1                    
  10001: JMP      label_10009          
  10002: JMP      label_10007          
label_10003:
  10003: LCP      [sp+21]              
  10004: GCP      data[2521]            ; = 100
  10005: EQU                           
  10006: JZ       label_10009          
label_10007:
  10007: CALL     func_1223            
  10008: JMP      label_10009          
label_10009:
  10009: SSP      1                    
  10010: JMP      label_10047          
  10011: JMP      label_10016          
label_10012:
  10012: LCP      [sp+20]              
  10013: GCP      data[2522]            ; = 15
  10014: EQU                           
  10015: JZ       label_10047          
label_10016:
  10016: LADR     [sp-4]               
  10017: DADR     4                    
  10018: DCP      4                    
  10019: GCP      data[2523]            ; = 20
  10020: UGEQ                          
  10021: JZ       label_10028          
  10022: GCP      data[2524]            ; = 0.0f
  10023: LADR     [sp-4]               
  10024: DADR     12                   
  10025: ASGN                          
  10026: SSP      1                    
  10027: JMP      label_10046          
label_10028:
  10028: GADR     data[1410]           
  10029: LADR     [sp-4]               
  10030: DADR     4                    
  10031: DCP      4                    
  10032: GCP      data[2525]            ; = 32
  10033: MUL                           
  10034: ADD                           
  10035: DCP      32                   
  10036: LADR     [sp-4]               
  10037: DADR     8                    
  10038: DCP      4                    
  10039: ASGN                          
  10040: SSP      8                    
  10041: GCP      data[2526]            ; = 1
  10042: LADR     [sp-4]               
  10043: DADR     12                   
  10044: ASGN                          
  10045: SSP      1                    
label_10046:
  10046: JMP      label_10047          
label_10047:
  10047: SSP      1                    
  10048: GCP      data[2527]            ; = 1
  10049: LLD      [sp-3]               
  10050: RET      20                   
