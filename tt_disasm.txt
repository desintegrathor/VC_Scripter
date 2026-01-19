; ==========================================
; Disassembly of: decompiler_source_tests/test1/tt.scr
; Instructions: 3736
; External functions: 60
; ==========================================

; External Functions (XFN)
; ------------------------
;   [  0] SC_MP_EndRule_SetTimeLeft(float,int)void
;   [  1] SC_MP_LoadNextMap(void)void
;   [  2] SC_message(*char,...)void
;   [  3] SC_MP_SRV_GetAtgSettings(*s_SC_MP_SRV_AtgSettings)void
;   [  4] SC_ggf(unsignedlong)float
;   [  5] SC_sgi(unsignedlong,int)void
;   [  6] SC_sgf(unsignedlong,float)void
;   [  7] SC_ggi(unsignedlong)int
;   [  8] SC_DUMMY_Set_DoNotRenHier2(*void,int)void
;   [  9] SC_MP_FpvMapSign_Set(unsignedlong,*s_SC_FpvMapSign)void
;   [ 10] SC_MP_SRV_GetAutoTeamBalance(void)int
;   [ 11] SC_MP_SRV_GetTeamsNrDifference(int)int
;   [ 12] SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void
;   [ 13] SC_MP_SRV_P_SetSideClass(unsignedlong,unsignedlong,unsignedlong)int
;   [ 14] SC_MP_EnumPlayers(*s_SC_MP_EnumPlayers,*unsignedlong,unsignedlong)int
;   [ 15] rand(void)int
;   [ 16] SC_MP_RecoverPlayer(unsignedlong)void
;   [ 17] SC_MP_SetInstantRecovery(int)void
;   [ 18] SC_MP_SRV_InitGameAfterInactive(void)void
;   [ 19] SC_MP_RestartMission(void)void
;   [ 20] SC_MP_RecoverAllNoAiPlayers(void)void
;   [ 21] SC_P_GetPos(unsignedlong,*c_Vector3)void
;   [ 22] SC_IsNear3D(*c_Vector3,*c_Vector3,float)int
;   [ 23] SC_MP_GetHandleofPl(unsignedlong)unsignedlong
;   [ 24] SC_P_MP_AddPoints(unsignedlong,int)void
;   [ 25] SC_SND_PlaySound2D(unsignedlong)void
;   [ 26] SC_MP_SetSideStats(unsignedlong,int,int)void
;   [ 27] SC_MP_SetIconHUD(*s_SC_HUD_MP_icon,unsignedlong)void
;   [ 28] SC_MP_EnableBotsFromScene(int)void
;   [ 29] SC_MP_FpvMapSign_Load(*char)unsignedlong
;   [ 30] SC_MP_SRV_SetForceSide(unsignedlong)void
;   [ 31] SC_MP_SetChooseValidSides(unsignedlong)void
;   [ 32] SC_MP_SRV_SetClassLimit(unsignedlong,unsignedlong)void
;   [ 33] SC_MP_GetSRVsettings(*s_SC_MP_SRV_settings)void
;   [ 34] SC_ZeroMem(*void,unsignedlong)void
;   [ 35] SC_MP_HUD_SetTabInfo(*s_SC_MP_hud)void
;   [ 36] SC_MP_AllowStPwD(int)void
;   [ 37] SC_MP_AllowFriendlyFireOFF(int)void
;   [ 38] SC_MP_SetItemsNoDisappear(int)void
;   [ 39] sprintf(*char,*constchar,...)int
;   [ 40] SC_NOD_GetNoMessage(*void,*char)*void
;   [ 41] SC_NOD_GetPivotWorld(*void,*c_Vector3)void
;   [ 42] SC_NOD_Get(*void,*char)*void
;   [ 43] SC_MP_Gvar_SetSynchro(unsignedlong)void
;   [ 44] SC_NET_FillRecover(*s_SC_MP_Recover,*char)int
;   [ 45] SC_MP_GetRecovers(unsignedlong,*s_SC_MP_Recover,*unsignedlong)void
;   [ 46] SC_Log(unsignedlong,*char,...)void
;   [ 47] SC_GetScriptHelper(*char,*s_sphere)int
;   [ 48] SC_Wtxt(unsignedlong)*unsignedshort
;   [ 49] SC_PC_Get(void)unsignedlong
;   [ 50] SC_GameInfoW(*unsignedshort)void
;   [ 51] SC_MP_GetPlofHandle(unsignedlong)unsignedlong
;   [ 52] SC_P_GetName(unsignedlong)*char
;   [ 53] SC_AnsiToUni(*char,*unsignedshort)*unsignedshort
;   [ 54] swprintf(*unsignedshort,*unsignedshort,...)int
;   [ 55] SC_GetScreenRes(*float,*float)void
;   [ 56] SC_Fnt_GetWidthW(*unsignedshort,float)float
;   [ 57] SC_Fnt_WriteW(float,float,*unsignedshort,float,unsignedlong)void
;   [ 58] SC_MP_SRV_GetBestDMrecov(*s_SC_MP_Recover,unsignedlong,*float,float)unsignedlong
;   [ 59] SC_MP_SRV_ClearPlsStats(void)void

; Strings
; -------
;   [8476] "EndRule unsopported: %d"
;   [9752] "g\weapons\Vvh_map\icons\MPIC_USflag.BES"
;   [9792] "g\weapons\Vvh_map\icons\MPIC_VCflag.BES"
;   [9832] "g\weapons\Vvh_map\icons\MPIC_emptyflag.BES"
;   [10044] "TT_flag_%d"
;   [10068] "vlajkaUS"
;   [10088] "Vlajka VC"
;   [10108] "vlajka N"
;   [10276] "TT_%c%d_%d"
;   [10452] "TurnTable recovers #%d: att:%d  def:%d"
;   [10528] "TTS_%d"
;   [10544] "helper %s not found"
;   [10692] "'disconnected'"
;   [10768] "'disconnected'"
;   [10836] "'disconnected'"

; Code
; ----

_init:
  000: GADR     data[2085]           
  001: GCP      data[2097]            ; = 0.0f
  002: LCP      [sp+0]               
  003: DLD      [sp+4]               
  004: GCP      data[2098]            ; = 22
  005: LCP      [sp+0]               
  006: PNT      4                    
  007: DLD      [sp+4]               
  008: GCP      data[2099]            ; = 23
  009: LCP      [sp+0]               
  010: PNT      8                    
  011: DLD      [sp+4]               
  012: GCP      data[2100]            ; = 24
  013: LCP      [sp+0]               
  014: PNT      12                   
  015: DLD      [sp+4]               
  016: GCP      data[2101]            ; = 25
  017: LCP      [sp+0]               
  018: PNT      16                   
  019: DLD      [sp+4]               
  020: GCP      data[2102]            ; = 26
  021: LCP      [sp+0]               
  022: PNT      20                   
  023: DLD      [sp+4]               
  024: GCP      data[2103]            ; = 17
  025: LCP      [sp+0]               
  026: PNT      24                   
  027: DLD      [sp+4]               
  028: GCP      data[2104]            ; = 18
  029: LCP      [sp+0]               
  030: PNT      28                   
  031: DLD      [sp+4]               
  032: GCP      data[2105]            ; = 19
  033: LCP      [sp+0]               
  034: PNT      32                   
  035: DLD      [sp+4]               
  036: GCP      data[2106]            ; = 20
  037: LCP      [sp+0]               
  038: PNT      36                   
  039: DLD      [sp+4]               
  040: GCP      data[2107]            ; = 21
  041: LCP      [sp+0]               
  042: PNT      40                   
  043: DLD      [sp+4]               
  044: GCP      data[2108]            ; = 0.0f
  045: LCP      [sp+0]               
  046: PNT      44                   
  047: DLD      [sp+4]               
  048: SSP      1                    
  049: RET      0                    
func_0050:
  050: GCP      data[1957]           
  051: JMP      label_0053           
  052: JMP      label_0057           
label_0053:
  053: LCP      [sp+0]               
  054: GCP      data[2112]            ; = 0.0f
  055: EQU                           
  056: JZ       label_0082           
label_0057:
  057: GCP      data[1968]           
  058: GCP      data[2113]            ; = 0.0f
  059: GRE                           
  060: JZ       label_0067           
  061: GCP      data[1959]           
  062: LCP      [sp-4]               
  063: FADD                          
  064: GADR     data[1959]           
  065: ASGN                          
  066: SSP      1                    
label_0067:
  067: GCP      data[1959]           
  068: GCP      data[1968]           
  069: XCALL    $SC_MP_EndRule_SetTimeLeft(float,int)void ; args=2
  070: SSP      2                    
  071: GCP      data[1959]           
  072: GCP      data[1958]           
  073: ITOF                          
  074: FGRE                          
  075: JZ       label_0080           
  076: XCALL    $SC_MP_LoadNextMap(void)void ; args=0
  077: GCP      data[2114]            ; = 1
  078: LLD      [sp-3]               
  079: RET      1                    
label_0080:
  080: JMP      label_0115           
  081: JMP      label_0086           
label_0082:
  082: LCP      [sp+0]               
  083: GCP      data[2115]            ; = 2
  084: EQU                           
  085: JZ       label_0114           
label_0086:
  086: GADR     data[1960]           
  087: GCP      data[2116]            ; = 0.0f
  088: ADD                           
  089: DCP      4                    
  090: GCP      data[1958]           
  091: UGEQ                          
  092: JNZ      label_0101           
  093: GADR     data[1960]           
  094: GCP      data[2117]            ; = 4
  095: ADD                           
  096: DCP      4                    
  097: GCP      data[1958]           
  098: UGEQ                          
  099: JNZ      label_0101           
  100: JMP      label_0105           
label_0101:
  101: XCALL    $SC_MP_LoadNextMap(void)void ; args=0
  102: GCP      data[2118]            ; = 1
  103: LLD      [sp-3]               
  104: RET      1                    
label_0105:
  105: JMP      label_0115           
  106: JMP      label_0107           
label_0107:
  107: GADR     data[2119]  ; "EndRule unsopported: %d"
  108: GCP      data[1957]           
  109: GCP      data[2125]            ; = 2
  110: XCALL    $SC_message(*char,...)void ; args=4294967295
  111: SSP      2                    
  112: JMP      label_0115           
  113: JMP      label_0115           
label_0114:
  114: JMP      label_0107           
label_0115:
  115: SSP      1                    
  116: GCP      data[2126]            ; = 0.0f
  117: LLD      [sp-3]               
  118: RET      0                    
func_0119:
  119: ASP      1                    
  120: ASP      3                    
  121: LADR     [sp+1]               
  122: XCALL    $SC_MP_SRV_GetAtgSettings(*s_SC_MP_SRV_AtgSettings)void ; args=1
  123: SSP      1                    
  124: LADR     [sp+1]               
  125: PNT      4                    
  126: DCP      4                    
  127: GCP      data[2127]            ; = 1.0f
  128: FGRE                          
  129: JZ       label_0135           
  130: LADR     [sp+1]               
  131: PNT      4                    
  132: DCP      4                    
  133: LLD      [sp-3]               
  134: RET      4                    
label_0135:
  135: ASP      1                    
  136: GCP      data[2128]            ; = 400
  137: ASP      1                    
  138: XCALL    $SC_ggf(unsignedlong)float ; args=1
  139: LLD      [sp+4]               
  140: SSP      1                    
  141: LADR     [sp+0]               
  142: ASGN                          
  143: SSP      1                    
  144: LCP      [sp+0]               
  145: GCP      data[2129]            ; = 0.0f
  146: FEQU                          
  147: JZ       label_0152           
  148: GCP      data[2130]            ; = 30.0f
  149: LADR     [sp+0]               
  150: ASGN                          
  151: SSP      1                    
label_0152:
  152: LCP      [sp+0]               
  153: LLD      [sp-3]               
  154: RET      4                    
func_0155:
  155: ASP      1                    
  156: ASP      3                    
  157: LADR     [sp+1]               
  158: XCALL    $SC_MP_SRV_GetAtgSettings(*s_SC_MP_SRV_AtgSettings)void ; args=1
  159: SSP      1                    
  160: LADR     [sp+1]               
  161: PNT      4                    
  162: DCP      4                    
  163: GCP      data[2131]            ; = 1.0f
  164: FGRE                          
  165: JZ       label_0193           
  166: LADR     [sp+1]               
  167: PNT      4                    
  168: DCP      4                    
  169: GCP      data[2132]            ; = 3.0f
  170: FDIV                          
  171: LADR     [sp+0]               
  172: ASGN                          
  173: SSP      1                    
  174: LCP      [sp+0]               
  175: GCP      data[2133]            ; = 5.0f
  176: FLES                          
  177: JZ       label_0182           
  178: GCP      data[2134]            ; = 5.0f
  179: LADR     [sp+0]               
  180: ASGN                          
  181: SSP      1                    
label_0182:
  182: LCP      [sp+0]               
  183: GCP      data[2135]            ; = 10.0f
  184: FGRE                          
  185: JZ       label_0190           
  186: GCP      data[2136]            ; = 10.0f
  187: LADR     [sp+0]               
  188: ASGN                          
  189: SSP      1                    
label_0190:
  190: LCP      [sp+0]               
  191: LLD      [sp-3]               
  192: RET      4                    
label_0193:
  193: ASP      1                    
  194: GCP      data[2137]            ; = 401
  195: ASP      1                    
  196: XCALL    $SC_ggf(unsignedlong)float ; args=1
  197: LLD      [sp+4]               
  198: SSP      1                    
  199: LADR     [sp+0]               
  200: ASGN                          
  201: SSP      1                    
  202: LCP      [sp+0]               
  203: GCP      data[2138]            ; = 0.0f
  204: FEQU                          
  205: JZ       label_0210           
  206: GCP      data[2139]            ; = 10.0f
  207: LADR     [sp+0]               
  208: ASGN                          
  209: SSP      1                    
label_0210:
  210: LCP      [sp+0]               
  211: LLD      [sp-3]               
  212: RET      4                    
func_0213:
  213: ASP      1                    
  214: ASP      3                    
  215: LADR     [sp+1]               
  216: XCALL    $SC_MP_SRV_GetAtgSettings(*s_SC_MP_SRV_AtgSettings)void ; args=1
  217: SSP      1                    
  218: LADR     [sp+1]               
  219: PNT      8                    
  220: DCP      4                    
  221: GCP      data[2140]            ; = 59.0f
  222: FGRE                          
  223: JZ       label_0229           
  224: LADR     [sp+1]               
  225: PNT      8                    
  226: DCP      4                    
  227: LLD      [sp-3]               
  228: RET      4                    
label_0229:
  229: ASP      1                    
  230: GCP      data[2141]            ; = 402
  231: ASP      1                    
  232: XCALL    $SC_ggf(unsignedlong)float ; args=1
  233: LLD      [sp+4]               
  234: SSP      1                    
  235: LADR     [sp+0]               
  236: ASGN                          
  237: SSP      1                    
  238: LCP      [sp+0]               
  239: GCP      data[2142]            ; = 0.0f
  240: FEQU                          
  241: JZ       label_0246           
  242: GCP      data[2143]            ; = 480.0f
  243: LADR     [sp+0]               
  244: ASGN                          
  245: SSP      1                    
label_0246:
  246: LCP      [sp+0]               
  247: LLD      [sp-3]               
  248: RET      4                    
func_0249:
  249: GCP      data[2144]            ; = 500
  250: GADR     data[1960]           
  251: GCP      data[2145]            ; = 0.0f
  252: ADD                           
  253: DCP      4                    
  254: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  255: SSP      2                    
  256: GCP      data[2146]            ; = 501
  257: GADR     data[1960]           
  258: GCP      data[2147]            ; = 4
  259: ADD                           
  260: DCP      4                    
  261: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  262: SSP      2                    
  263: RET      0                    
func_0264:
  264: GCP      data[1971]           
  265: LCP      [sp-3]               
  266: FSUB                          
  267: GADR     data[1971]           
  268: ASGN                          
  269: SSP      1                    
  270: GCP      data[1971]           
  271: GCP      data[2148]            ; = 0.0f
  272: FLES                          
  273: JZ       label_0293           
  274: GCP      data[2149]            ; = 10.0f
  275: GADR     data[1971]           
  276: ASGN                          
  277: SSP      1                    
  278: GCP      data[2150]            ; = 504
  279: GCP      data[1972]           
  280: XCALL    $SC_sgf(unsignedlong,float)void ; args=2
  281: SSP      2                    
  282: GCP      data[2151]            ; = 505
  283: ASP      1                    
  284: GCP      data[2152]            ; = 505
  285: ASP      1                    
  286: XCALL    $SC_ggi(unsignedlong)int ; args=1
  287: LLD      [sp+1]               
  288: SSP      1                    
  289: GCP      data[2153]            ; = 1
  290: ADD                           
  291: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  292: SSP      2                    
label_0293:
  293: RET      0                    
func_0294:
  294: GCP      data[0]              
  295: GCP      data[2154]            ; = 1
  296: SUB                           
  297: GADR     data[1967]           
  298: ASGN                          
  299: SSP      1                    
  300: GCP      data[2155]            ; = 507
  301: GCP      data[1967]           
  302: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  303: SSP      2                    
  304: GCP      data[1965]           
  305: GCP      data[2156]            ; = 2
  306: MOD                           
  307: GCP      data[2157]            ; = 0.0f
  308: EQU                           
  309: JZ       label_0322           
  310: ASP      1                    
  311: ASP      1                    
  312: CALL     func_0213            
  313: LLD      [sp+0]               
  314: GADR     data[1972]           
  315: ASGN                          
  316: SSP      1                    
  317: GCP      data[1972]           
  318: GADR     data[1973]           
  319: ASGN                          
  320: SSP      1                    
  321: JMP      label_0326           
label_0322:
  322: GCP      data[1974]           
  323: GADR     data[1972]           
  324: ASGN                          
  325: SSP      1                    
label_0326:
  326: GCP      data[2158]            ; = -1.0f
  327: GADR     data[1971]           
  328: ASGN                          
  329: SSP      1                    
  330: GCP      data[2159]            ; = 0.0f
  331: CALL     func_0264            
  332: SSP      1                    
  333: RET      0                    
func_0334:
  334: LCP      [sp-4]               
  335: GCP      data[2160]            ; = 4
  336: MOD                           
  337: JMP      label_0339           
  338: JMP      label_0343           
label_0339:
  339: LCP      [sp+0]               
  340: GCP      data[2161]            ; = 0.0f
  341: EQU                           
  342: JZ       label_0344           
label_0343:
  343: JMP      label_0348           
label_0344:
  344: LCP      [sp+0]               
  345: GCP      data[2162]            ; = 3
  346: EQU                           
  347: JZ       label_0351           
label_0348:
  348: GCP      data[2163]            ; = 0.0f
  349: LLD      [sp-3]               
  350: RET      1                    
label_0351:
  351: SSP      1                    
  352: GCP      data[2164]            ; = 1
  353: LLD      [sp-3]               
  354: RET      0                    
func_0355:
  355: GCP      data[1968]           
  356: JMP      label_0358           
  357: JMP      label_0362           
label_0358:
  358: LCP      [sp+0]               
  359: GCP      data[2165]            ; = 3
  360: EQU                           
  361: JZ       label_0424           
label_0362:
  362: GADR     data[1960]           
  363: GCP      data[2166]            ; = 1
  364: GCP      data[1966]           
  365: SUB                           
  366: GCP      data[2167]            ; = 4
  367: MUL                           
  368: ADD                           
  369: DCP      4                    
  370: GADR     data[1960]           
  371: GCP      data[2168]            ; = 1
  372: GCP      data[1966]           
  373: SUB                           
  374: GCP      data[2169]            ; = 4
  375: MUL                           
  376: ADD                           
  377: DCP      4                    
  378: GCP      data[2170]            ; = 1
  379: ADD                           
  380: GADR     data[1960]           
  381: GCP      data[2171]            ; = 1
  382: GCP      data[1966]           
  383: SUB                           
  384: GCP      data[2172]            ; = 4
  385: MUL                           
  386: ADD                           
  387: ASGN                          
  388: SSP      1                    
  389: SSP      1                    
  390: CALL     func_0249            
  391: GCP      data[2173]            ; = 506
  392: GCP      data[2174]            ; = 1
  393: GCP      data[1966]           
  394: SUB                           
  395: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  396: SSP      2                    
  397: GCP      data[2175]            ; = 509
  398: GCP      data[2176]            ; = 1
  399: GCP      data[1966]           
  400: SUB                           
  401: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  402: SSP      2                    
  403: GCP      data[1965]           
  404: GCP      data[2177]            ; = 2
  405: MOD                           
  406: JZ       label_0416           
  407: GCP      data[1965]           
  408: GCP      data[1965]           
  409: GCP      data[2178]            ; = 1
  410: ADD                           
  411: GADR     data[1965]           
  412: ASGN                          
  413: SSP      1                    
  414: SSP      1                    
  415: JMP      label_0422           
label_0416:
  416: GCP      data[1965]           
  417: GCP      data[2179]            ; = 2
  418: ADD                           
  419: GADR     data[1965]           
  420: ASGN                          
  421: SSP      1                    
label_0422:
  422: JMP      label_0479           
  423: JMP      label_0428           
label_0424:
  424: LCP      [sp+0]               
  425: GCP      data[2180]            ; = 2
  426: EQU                           
  427: JZ       label_0479           
label_0428:
  428: GCP      data[2181]            ; = 509
  429: GCP      data[1966]           
  430: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  431: SSP      2                    
  432: GCP      data[1965]           
  433: GCP      data[2182]            ; = 2
  434: MOD                           
  435: JZ       label_0464           
  436: GADR     data[1960]           
  437: GCP      data[1966]           
  438: GCP      data[2183]            ; = 4
  439: MUL                           
  440: ADD                           
  441: DCP      4                    
  442: GADR     data[1960]           
  443: GCP      data[1966]           
  444: GCP      data[2184]            ; = 4
  445: MUL                           
  446: ADD                           
  447: DCP      4                    
  448: GCP      data[2185]            ; = 1
  449: ADD                           
  450: GADR     data[1960]           
  451: GCP      data[1966]           
  452: GCP      data[2186]            ; = 4
  453: MUL                           
  454: ADD                           
  455: ASGN                          
  456: SSP      1                    
  457: SSP      1                    
  458: CALL     func_0249            
  459: GCP      data[2187]            ; = 506
  460: GCP      data[1966]           
  461: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  462: SSP      2                    
  463: JMP      label_0470           
label_0464:
  464: GCP      data[1973]           
  465: GCP      data[1972]           
  466: FSUB                          
  467: GADR     data[1974]           
  468: ASGN                          
  469: SSP      1                    
label_0470:
  470: GCP      data[1965]           
  471: GCP      data[1965]           
  472: GCP      data[2188]            ; = 1
  473: ADD                           
  474: GADR     data[1965]           
  475: ASGN                          
  476: SSP      1                    
  477: SSP      1                    
  478: JMP      label_0479           
label_0479:
  479: SSP      1                    
  480: GCP      data[2189]            ; = 502
  481: GCP      data[1965]           
  482: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  483: SSP      2                    
  484: ASP      1                    
  485: GCP      data[1965]           
  486: ASP      1                    
  487: CALL     func_0334            
  488: LLD      [sp+0]               
  489: SSP      1                    
  490: GADR     data[1966]           
  491: ASGN                          
  492: SSP      1                    
  493: GCP      data[2190]            ; = 507
  494: GCP      data[2191]            ; = 6
  495: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  496: SSP      2                    
  497: RET      0                    
func_0498:
  498: ASP      1                    
  499: ASP      1                    
  500: ASP      1                    
  501: ASP      1                    
  502: ASP      1                    
  503: ASP      36                   
  504: GCP      data[2192]            ; = 0.0f
  505: LADR     [sp+4]               
  506: ASGN                          
  507: SSP      1                    
  508: GCP      data[2193]            ; = 0.0f
  509: LADR     [sp+3]               
  510: ASGN                          
  511: SSP      1                    
label_0512:
  512: LCP      [sp+3]               
  513: GCP      data[2194]            ; = 6
  514: ULES                          
  515: JZ       label_0747           
  516: GCP      data[2195]            ; = 0.0f
  517: LADR     [sp+0]               
  518: ASGN                          
  519: SSP      1                    
  520: GCP      data[2196]            ; = 0.0f
  521: LADR     [sp+1]               
  522: ASGN                          
  523: SSP      1                    
  524: GCP      data[2197]            ; = 0.0f
  525: LADR     [sp+2]               
  526: ASGN                          
  527: SSP      1                    
  528: LCP      [sp+3]               
  529: GCP      data[2198]            ; = 1
  530: ADD                           
  531: LCP      [sp-3]               
  532: EQU                           
  533: JZ       label_0568           
  534: LCP      [sp-4]               
  535: JMP      label_0537           
  536: JMP      label_0541           
label_0537:
  537: LCP      [sp+41]              
  538: GCP      data[2199]            ; = 0.0f
  539: EQU                           
  540: JZ       label_0547           
label_0541:
  541: GCP      data[2200]            ; = 1
  542: LADR     [sp+1]               
  543: ASGN                          
  544: SSP      1                    
  545: JMP      label_0566           
  546: JMP      label_0551           
label_0547:
  547: LCP      [sp+41]              
  548: GCP      data[2201]            ; = 1
  549: EQU                           
  550: JZ       label_0557           
label_0551:
  551: GCP      data[2202]            ; = 1
  552: LADR     [sp+0]               
  553: ASGN                          
  554: SSP      1                    
  555: JMP      label_0566           
  556: JMP      label_0561           
label_0557:
  557: LCP      [sp+41]              
  558: GCP      data[2203]            ; = 2
  559: EQU                           
  560: JZ       label_0566           
label_0561:
  561: GCP      data[2204]            ; = 1
  562: LADR     [sp+2]               
  563: ASGN                          
  564: SSP      1                    
  565: JMP      label_0566           
label_0566:
  566: SSP      1                    
  567: JMP      label_0576           
label_0568:
  568: LCP      [sp+3]               
  569: LCP      [sp-3]               
  570: ULES                          
  571: JZ       label_0576           
  572: GCP      data[2205]            ; = 1
  573: LADR     [sp+2]               
  574: ASGN                          
  575: SSP      1                    
label_0576:
  576: GADR     data[1984]           
  577: LCP      [sp+3]               
  578: GCP      data[2206]            ; = 12
  579: MUL                           
  580: ADD                           
  581: GCP      data[2207]            ; = 0.0f
  582: ADD                           
  583: DCP      4                    
  584: JZ       label_0601           
  585: GADR     data[1984]           
  586: LCP      [sp+3]               
  587: GCP      data[2208]            ; = 12
  588: MUL                           
  589: ADD                           
  590: GCP      data[2209]            ; = 0.0f
  591: ADD                           
  592: DCP      4                    
  593: LCP      [sp+0]               
  594: JZ       label_0596           
  595: JMP      label_0598           
label_0596:
  596: GCP      data[2210]            ; = 1
  597: JMP      label_0599           
label_0598:
  598: GCP      data[2211]            ; = 0.0f
label_0599:
  599: XCALL    $SC_DUMMY_Set_DoNotRenHier2(*void,int)void ; args=2
  600: SSP      2                    
label_0601:
  601: GADR     data[1984]           
  602: LCP      [sp+3]               
  603: GCP      data[2212]            ; = 12
  604: MUL                           
  605: ADD                           
  606: GCP      data[2213]            ; = 4
  607: ADD                           
  608: DCP      4                    
  609: JZ       label_0626           
  610: GADR     data[1984]           
  611: LCP      [sp+3]               
  612: GCP      data[2214]            ; = 12
  613: MUL                           
  614: ADD                           
  615: GCP      data[2215]            ; = 4
  616: ADD                           
  617: DCP      4                    
  618: LCP      [sp+1]               
  619: JZ       label_0621           
  620: JMP      label_0623           
label_0621:
  621: GCP      data[2216]            ; = 1
  622: JMP      label_0624           
label_0623:
  623: GCP      data[2217]            ; = 0.0f
label_0624:
  624: XCALL    $SC_DUMMY_Set_DoNotRenHier2(*void,int)void ; args=2
  625: SSP      2                    
label_0626:
  626: GADR     data[1984]           
  627: LCP      [sp+3]               
  628: GCP      data[2218]            ; = 12
  629: MUL                           
  630: ADD                           
  631: GCP      data[2219]            ; = 8
  632: ADD                           
  633: DCP      4                    
  634: JZ       label_0651           
  635: GADR     data[1984]           
  636: LCP      [sp+3]               
  637: GCP      data[2220]            ; = 12
  638: MUL                           
  639: ADD                           
  640: GCP      data[2221]            ; = 8
  641: ADD                           
  642: DCP      4                    
  643: LCP      [sp+2]               
  644: JZ       label_0646           
  645: JMP      label_0648           
label_0646:
  646: GCP      data[2222]            ; = 1
  647: JMP      label_0649           
label_0648:
  648: GCP      data[2223]            ; = 0.0f
label_0649:
  649: XCALL    $SC_DUMMY_Set_DoNotRenHier2(*void,int)void ; args=2
  650: SSP      2                    
label_0651:
  651: GCP      data[2224]            ; = 0.0f
  652: LADR     [sp+5]               
  653: LCP      [sp+4]               
  654: GCP      data[2225]            ; = 24
  655: MUL                           
  656: ADD                           
  657: ASGN                          
  658: SSP      1                    
  659: LCP      [sp+0]               
  660: JZ       label_0670           
  661: GCP      data[2109]           
  662: LADR     [sp+5]               
  663: LCP      [sp+4]               
  664: GCP      data[2226]            ; = 24
  665: MUL                           
  666: ADD                           
  667: ASGN                          
  668: SSP      1                    
  669: JMP      label_0691           
label_0670:
  670: LCP      [sp+1]               
  671: JZ       label_0681           
  672: GCP      data[2110]           
  673: LADR     [sp+5]               
  674: LCP      [sp+4]               
  675: GCP      data[2227]            ; = 24
  676: MUL                           
  677: ADD                           
  678: ASGN                          
  679: SSP      1                    
  680: JMP      label_0691           
label_0681:
  681: LCP      [sp+2]               
  682: JZ       label_0691           
  683: GCP      data[2111]           
  684: LADR     [sp+5]               
  685: LCP      [sp+4]               
  686: GCP      data[2228]            ; = 24
  687: MUL                           
  688: ADD                           
  689: ASGN                          
  690: SSP      1                    
label_0691:
  691: LADR     [sp+5]               
  692: LCP      [sp+4]               
  693: GCP      data[2229]            ; = 24
  694: MUL                           
  695: ADD                           
  696: DCP      4                    
  697: JZ       label_0738           
  698: GCP      data[2230]            ; = -1
  699: LADR     [sp+5]               
  700: LCP      [sp+4]               
  701: GCP      data[2231]            ; = 24
  702: MUL                           
  703: ADD                           
  704: PNT      4                    
  705: ASGN                          
  706: SSP      1                    
  707: GADR     data[2002]           
  708: LCP      [sp+3]               
  709: GCP      data[2232]            ; = 12
  710: MUL                           
  711: ADD                           
  712: DCP      12                   
  713: LADR     [sp+5]               
  714: LCP      [sp+4]               
  715: GCP      data[2233]            ; = 24
  716: MUL                           
  717: ADD                           
  718: PNT      12                   
  719: ASGN                          
  720: SSP      3                    
  721: GCP      data[2234]            ; = 1.0f
  722: LADR     [sp+5]               
  723: LCP      [sp+4]               
  724: GCP      data[2235]            ; = 24
  725: MUL                           
  726: ADD                           
  727: PNT      8                    
  728: ASGN                          
  729: SSP      1                    
  730: LCP      [sp+4]               
  731: LCP      [sp+4]               
  732: GCP      data[2236]            ; = 1
  733: ADD                           
  734: LADR     [sp+4]               
  735: ASGN                          
  736: SSP      1                    
  737: SSP      1                    
label_0738:
  738: LCP      [sp+3]               
  739: LCP      [sp+3]               
  740: GCP      data[2237]            ; = 1
  741: ADD                           
  742: LADR     [sp+3]               
  743: ASGN                          
  744: SSP      1                    
  745: SSP      1                    
  746: JMP      label_0512           
label_0747:
  747: LCP      [sp+4]               
  748: LADR     [sp+5]               
  749: XCALL    $SC_MP_FpvMapSign_Set(unsignedlong,*s_SC_FpvMapSign)void ; args=2
  750: SSP      2                    
  751: RET      41                   
func_0752:
  752: ASP      1                    
  753: ASP      1                    
  754: ASP      5                    
  755: ASP      1                    
  756: ASP      1                    
  757: XCALL    $SC_MP_SRV_GetAutoTeamBalance(void)int ; args=0
  758: LLD      [sp+7]               
  759: JZ       label_0761           
  760: JMP      label_0762           
label_0761:
  761: RET      7                    
label_0762:
  762: ASP      1                    
  763: GCP      data[2238]            ; = 1
  764: ASP      1                    
  765: XCALL    $SC_MP_SRV_GetTeamsNrDifference(int)int ; args=1
  766: LLD      [sp+7]               
  767: SSP      1                    
  768: LADR     [sp+0]               
  769: ASGN                          
  770: SSP      1                    
  771: LCP      [sp+0]               
  772: GCP      data[2239]            ; = 3
  773: LES                           
  774: JZ       label_0781           
  775: LCP      [sp+0]               
  776: GCP      data[2240]            ; = -3
  777: GRE                           
  778: JZ       label_0781           
  779: JMP      label_0780           
label_0780:
  780: RET      7                    
label_0781:
  781: LCP      [sp-3]               
  782: LADR     [sp+2]               
  783: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  784: SSP      2                    
  785: LADR     [sp+2]               
  786: PNT      8                    
  787: DCP      4                    
  788: GCP      data[2241]            ; = 0.0f
  789: EQU                           
  790: JZ       label_0801           
  791: LCP      [sp+0]               
  792: GCP      data[2242]            ; = 0.0f
  793: GRE                           
  794: JZ       label_0801           
  795: JMP      label_0796           
label_0796:
  796: GCP      data[2243]            ; = 1
  797: LADR     [sp+1]               
  798: ASGN                          
  799: SSP      1                    
  800: JMP      label_0818           
label_0801:
  801: LADR     [sp+2]               
  802: PNT      8                    
  803: DCP      4                    
  804: GCP      data[2244]            ; = 1
  805: EQU                           
  806: JZ       label_0817           
  807: LCP      [sp+0]               
  808: GCP      data[2245]            ; = 0.0f
  809: LES                           
  810: JZ       label_0817           
  811: JMP      label_0812           
label_0812:
  812: GCP      data[2246]            ; = 0.0f
  813: LADR     [sp+1]               
  814: ASGN                          
  815: SSP      1                    
  816: JMP      label_0818           
label_0817:
  817: RET      7                    
label_0818:
  818: ASP      1                    
  819: LCP      [sp-3]               
  820: LCP      [sp+1]               
  821: GCP      data[2247]            ; = 1
  822: GCP      data[2248]            ; = 20
  823: LCP      [sp+1]               
  824: MUL                           
  825: ADD                           
  826: ASP      1                    
  827: XCALL    $SC_MP_SRV_P_SetSideClass(unsignedlong,unsignedlong,unsignedlong)int ; args=3
  828: LLD      [sp+7]               
  829: SSP      3                    
  830: SSP      1                    
  831: GCP      data[2020]           
  832: GCP      data[2249]            ; = 64
  833: ULES                          
  834: JZ       label_0851           
  835: LCP      [sp-3]               
  836: GADR     data[2021]           
  837: GCP      data[2020]           
  838: GCP      data[2250]            ; = 4
  839: MUL                           
  840: ADD                           
  841: ASGN                          
  842: SSP      1                    
  843: GCP      data[2020]           
  844: GCP      data[2020]           
  845: GCP      data[2251]            ; = 1
  846: ADD                           
  847: GADR     data[2020]           
  848: ASGN                          
  849: SSP      1                    
  850: SSP      1                    
label_0851:
  851: RET      7                    
func_0852:
  852: ASP      1                    
  853: ASP      1                    
  854: ASP      1                    
  855: ASP      5                    
  856: ASP      256                  
  857: ASP      1                    
  858: ASP      1                    
  859: ASP      1                    
  860: ASP      1                    
  861: ASP      1                    
  862: XCALL    $SC_MP_SRV_GetAutoTeamBalance(void)int ; args=0
  863: LLD      [sp+267]             
  864: JZ       label_0866           
  865: JMP      label_0867           
label_0866:
  866: RET      267                  
label_0867:
  867: ASP      1                    
  868: GCP      data[2252]            ; = 1
  869: ASP      1                    
  870: XCALL    $SC_MP_SRV_GetTeamsNrDifference(int)int ; args=1
  871: LLD      [sp+267]             
  872: SSP      1                    
  873: LADR     [sp+0]               
  874: ASGN                          
  875: SSP      1                    
  876: LCP      [sp+0]               
  877: GCP      data[2253]            ; = 3
  878: LES                           
  879: JZ       label_0886           
  880: LCP      [sp+0]               
  881: GCP      data[2254]            ; = -3
  882: GRE                           
  883: JZ       label_0886           
  884: JMP      label_0885           
label_0885:
  885: RET      267                  
label_0886:
  886: LCP      [sp+0]               
  887: GCP      data[2255]            ; = 0.0f
  888: GRE                           
  889: JZ       label_0901           
  890: GCP      data[2256]            ; = 0.0f
  891: LADR     [sp+1]               
  892: ASGN                          
  893: SSP      1                    
  894: LCP      [sp+0]               
  895: GCP      data[2257]            ; = 2
  896: IDIV                          
  897: LADR     [sp+2]               
  898: ASGN                          
  899: SSP      1                    
  900: JMP      label_0912           
label_0901:
  901: GCP      data[2258]            ; = 1
  902: LADR     [sp+1]               
  903: ASGN                          
  904: SSP      1                    
  905: LCP      [sp+0]               
  906: NEG                           
  907: GCP      data[2259]            ; = 2
  908: IDIV                          
  909: LADR     [sp+2]               
  910: ASGN                          
  911: SSP      1                    
label_0912:
  912: GCP      data[2260]            ; = 64
  913: LADR     [sp+265]             
  914: ASGN                          
  915: SSP      1                    
  916: ASP      1                    
  917: LADR     [sp+8]               
  918: LADR     [sp+265]             
  919: LCP      [sp+1]               
  920: ASP      1                    
  921: XCALL    $SC_MP_EnumPlayers(*s_SC_MP_EnumPlayers,*unsignedlong,unsignedlong)int ; args=3
  922: LLD      [sp+267]             
  923: SSP      3                    
  924: JZ       label_1027           
  925: LCP      [sp+265]             
  926: JZ       label_0928           
  927: JMP      label_0929           
label_0928:
  928: RET      267                  
label_0929:
  929: LCP      [sp+2]               
  930: GCP      data[2261]            ; = 0.0f
  931: NEQ                           
  932: JZ       label_1027           
  933: ASP      1                    
  934: ASP      1                    
  935: XCALL    $rand(void)int        ; args=0
  936: LLD      [sp+267]             
  937: LCP      [sp+265]             
  938: MOD                           
  939: LADR     [sp+266]             
  940: ASGN                          
  941: SSP      1                    
  942: LCP      [sp+266]             
  943: LADR     [sp+264]             
  944: ASGN                          
  945: SSP      1                    
label_0946:
  946: LADR     [sp+8]               
  947: LCP      [sp+264]             
  948: GCP      data[2262]            ; = 16
  949: MUL                           
  950: ADD                           
  951: DCP      4                    
  952: GCP      data[2263]            ; = 0.0f
  953: EQU                           
  954: JNZ      label_0966           
  955: LADR     [sp+8]               
  956: LCP      [sp+264]             
  957: GCP      data[2264]            ; = 16
  958: MUL                           
  959: ADD                           
  960: PNT      8                    
  961: DCP      4                    
  962: GCP      data[2265]            ; = 0.0f
  963: EQU                           
  964: JNZ      label_0966           
  965: JMP      label_0988           
label_0966:
  966: LCP      [sp+264]             
  967: LCP      [sp+264]             
  968: GCP      data[2266]            ; = 1
  969: ADD                           
  970: LADR     [sp+264]             
  971: ASGN                          
  972: SSP      1                    
  973: SSP      1                    
  974: LCP      [sp+264]             
  975: LCP      [sp+265]             
  976: EQU                           
  977: JZ       label_0982           
  978: GCP      data[2267]            ; = 0.0f
  979: LADR     [sp+264]             
  980: ASGN                          
  981: SSP      1                    
label_0982:
  982: LCP      [sp+264]             
  983: LCP      [sp+266]             
  984: EQU                           
  985: JZ       label_0987           
  986: RET      267                  
label_0987:
  987: JMP      label_0946           
label_0988:
  988: ASP      1                    
  989: LADR     [sp+8]               
  990: LCP      [sp+264]             
  991: GCP      data[2268]            ; = 16
  992: MUL                           
  993: ADD                           
  994: DCP      4                    
  995: GCP      data[2269]            ; = 1
  996: LCP      [sp+1]               
  997: SUB                           
  998: GCP      data[2270]            ; = 1
  999: GCP      data[2271]            ; = 20
  1000: GCP      data[2272]            ; = 1
  1001: LCP      [sp+1]               
  1002: SUB                           
  1003: MUL                           
  1004: ADD                           
  1005: ASP      1                    
  1006: XCALL    $SC_MP_SRV_P_SetSideClass(unsignedlong,unsignedlong,unsignedlong)int ; args=3
  1007: LLD      [sp+267]             
  1008: SSP      3                    
  1009: SSP      1                    
  1010: GCP      data[2273]            ; = 0.0f
  1011: LADR     [sp+8]               
  1012: LCP      [sp+264]             
  1013: GCP      data[2274]            ; = 16
  1014: MUL                           
  1015: ADD                           
  1016: ASGN                          
  1017: SSP      1                    
  1018: LCP      [sp+2]               
  1019: LCP      [sp+2]               
  1020: GCP      data[2275]            ; = 1
  1021: SUB                           
  1022: LADR     [sp+2]               
  1023: ASGN                          
  1024: SSP      1                    
  1025: SSP      1                    
  1026: JMP      label_0929           
label_1027:
  1027: RET      267                  
func_1028:
  1028: ASP      256                  
  1029: ASP      1                    
  1030: ASP      1                    
  1031: ASP      1                    
  1032: GCP      data[2276]            ; = 1
  1033: ASP      1                    
  1034: ASP      1                    
  1035: GCP      data[2277]            ; = 502
  1036: ASP      1                    
  1037: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1038: LLD      [sp+261]             
  1039: SSP      1                    
  1040: ASP      1                    
  1041: CALL     func_0334            
  1042: LLD      [sp+260]             
  1043: SSP      1                    
  1044: SUB                           
  1045: LADR     [sp+257]             
  1046: ASGN                          
  1047: SSP      1                    
  1048: GCP      data[2278]            ; = 64
  1049: LADR     [sp+258]             
  1050: ASGN                          
  1051: SSP      1                    
  1052: ASP      1                    
  1053: LADR     [sp+0]               
  1054: LADR     [sp+258]             
  1055: LCP      [sp+257]             
  1056: ASP      1                    
  1057: XCALL    $SC_MP_EnumPlayers(*s_SC_MP_EnumPlayers,*unsignedlong,unsignedlong)int ; args=3
  1058: LLD      [sp+259]             
  1059: SSP      3                    
  1060: JZ       label_1096           
  1061: GCP      data[2279]            ; = 0.0f
  1062: LADR     [sp+256]             
  1063: ASGN                          
  1064: SSP      1                    
label_1065:
  1065: LCP      [sp+256]             
  1066: LCP      [sp+258]             
  1067: ULES                          
  1068: JZ       label_1096           
  1069: LADR     [sp+0]               
  1070: LCP      [sp+256]             
  1071: GCP      data[2280]            ; = 16
  1072: MUL                           
  1073: ADD                           
  1074: PNT      8                    
  1075: DCP      4                    
  1076: GCP      data[2281]            ; = 2
  1077: EQU                           
  1078: JZ       label_1087           
  1079: LADR     [sp+0]               
  1080: LCP      [sp+256]             
  1081: GCP      data[2282]            ; = 16
  1082: MUL                           
  1083: ADD                           
  1084: DCP      4                    
  1085: XCALL    $SC_MP_RecoverPlayer(unsignedlong)void ; args=1
  1086: SSP      1                    
label_1087:
  1087: LCP      [sp+256]             
  1088: LCP      [sp+256]             
  1089: GCP      data[2283]            ; = 1
  1090: ADD                           
  1091: LADR     [sp+256]             
  1092: ASGN                          
  1093: SSP      1                    
  1094: SSP      1                    
  1095: JMP      label_1065           
label_1096:
  1096: RET      259                  
ScriptMain:
  1097: ASP      8                    
  1098: ASP      1                    
  1099: ASP      1                    
  1100: ASP      1                    
  1101: ASP      1                    
  1102: ASP      1                    
  1103: ASP      1                    
  1104: ASP      15                   
  1105: ASP      256                  
  1106: ASP      9                    
  1107: ASP      1                    
  1108: ASP      1                    
  1109: ASP      2                    
  1110: ASP      1                    
  1111: ASP      12                   
  1112: ASP      3                    
  1113: ASP      1                    
  1114: ASP      64                   
  1115: ASP      32                   
  1116: ASP      1                    
  1117: ASP      1                    
  1118: ASP      5                    
  1119: LADR     [sp-4]               
  1120: DADR     0                    
  1121: DCP      4                    
  1122: JMP      label_1124           
  1123: JMP      label_1128           
label_1124:
  1124: LCP      [sp+418]             
  1125: GCP      data[2284]            ; = 3
  1126: EQU                           
  1127: JZ       label_1713           
label_1128:
  1128: ASP      1                    
  1129: LADR     [sp-4]               
  1130: DADR     16                   
  1131: DCP      4                    
  1132: ASP      1                    
  1133: CALL     func_0050            
  1134: LLD      [sp+419]             
  1135: SSP      1                    
  1136: JZ       label_1138           
  1137: JMP      label_3732           
label_1138:
  1138: GCP      data[2285]            ; = 0.0f
  1139: LADR     [sp+296]             
  1140: GCP      data[2286]            ; = 4
  1141: ADD                           
  1142: ASGN                          
  1143: LADR     [sp+296]             
  1144: GCP      data[2287]            ; = 0.0f
  1145: ADD                           
  1146: ASGN                          
  1147: SSP      1                    
  1148: GCP      data[2288]            ; = 64
  1149: LADR     [sp+12]              
  1150: ASGN                          
  1151: SSP      1                    
  1152: ASP      1                    
  1153: LADR     [sp+29]              
  1154: LADR     [sp+12]              
  1155: GCP      data[2289]            ; = -1
  1156: ASP      1                    
  1157: XCALL    $SC_MP_EnumPlayers(*s_SC_MP_EnumPlayers,*unsignedlong,unsignedlong)int ; args=3
  1158: LLD      [sp+419]             
  1159: SSP      3                    
  1160: JZ       label_1318           
  1161: LCP      [sp+12]              
  1162: GCP      data[2290]            ; = 0.0f
  1163: EQU                           
  1164: JZ       label_1191           
  1165: GADR     data[1960]           
  1166: GCP      data[2291]            ; = 0.0f
  1167: ADD                           
  1168: DCP      4                    
  1169: GADR     data[1960]           
  1170: GCP      data[2292]            ; = 4
  1171: ADD                           
  1172: DCP      4                    
  1173: ADD                           
  1174: GCP      data[2293]            ; = 0.0f
  1175: NEQ                           
  1176: JZ       label_1191           
  1177: JMP      label_1178           
label_1178:
  1178: GCP      data[2294]            ; = 0.0f
  1179: GADR     data[1960]           
  1180: GCP      data[2295]            ; = 0.0f
  1181: ADD                           
  1182: ASGN                          
  1183: SSP      1                    
  1184: GCP      data[2296]            ; = 0.0f
  1185: GADR     data[1960]           
  1186: GCP      data[2297]            ; = 4
  1187: ADD                           
  1188: ASGN                          
  1189: SSP      1                    
  1190: CALL     func_0249            
label_1191:
  1191: GCP      data[2298]            ; = 0.0f
  1192: LADR     [sp+8]               
  1193: ASGN                          
  1194: SSP      1                    
label_1195:
  1195: LCP      [sp+8]               
  1196: LCP      [sp+12]              
  1197: ULES                          
  1198: JZ       label_1242           
  1199: LADR     [sp+29]              
  1200: LCP      [sp+8]               
  1201: GCP      data[2299]            ; = 16
  1202: MUL                           
  1203: ADD                           
  1204: PNT      8                    
  1205: DCP      4                    
  1206: GCP      data[2300]            ; = 0.0f
  1207: NEQ                           
  1208: JZ       label_1233           
  1209: LADR     [sp+29]              
  1210: LCP      [sp+8]               
  1211: GCP      data[2301]            ; = 16
  1212: MUL                           
  1213: ADD                           
  1214: PNT      4                    
  1215: DCP      4                    
  1216: GCP      data[2302]            ; = 2
  1217: ULES                          
  1218: JZ       label_1233           
  1219: GCP      data[2303]            ; = 1
  1220: LADR     [sp+296]             
  1221: LADR     [sp+29]              
  1222: LCP      [sp+8]               
  1223: GCP      data[2304]            ; = 16
  1224: MUL                           
  1225: ADD                           
  1226: PNT      4                    
  1227: DCP      4                    
  1228: GCP      data[2305]            ; = 4
  1229: MUL                           
  1230: ADD                           
  1231: ASGN                          
  1232: SSP      1                    
label_1233:
  1233: LCP      [sp+8]               
  1234: LCP      [sp+8]               
  1235: GCP      data[2306]            ; = 1
  1236: ADD                           
  1237: LADR     [sp+8]               
  1238: ASGN                          
  1239: SSP      1                    
  1240: SSP      1                    
  1241: JMP      label_1195           
label_1242:
  1242: GCP      data[1981]           
  1243: LADR     [sp-4]               
  1244: DADR     16                   
  1245: DCP      4                    
  1246: FSUB                          
  1247: GADR     data[1981]           
  1248: ASGN                          
  1249: SSP      1                    
  1250: LADR     [sp+296]             
  1251: GCP      data[2307]            ; = 0.0f
  1252: ADD                           
  1253: DCP      4                    
  1254: JZ       label_1293           
  1255: LADR     [sp+296]             
  1256: GCP      data[2308]            ; = 4
  1257: ADD                           
  1258: DCP      4                    
  1259: JZ       label_1293           
  1260: JMP      label_1261           
label_1261:
  1261: GCP      data[2309]            ; = 0.0f
  1262: XCALL    $SC_MP_SetInstantRecovery(int)void ; args=1
  1263: SSP      1                    
  1264: GCP      data[1968]           
  1265: GCP      data[2310]            ; = 0.0f
  1266: EQU                           
  1267: JZ       label_1292           
  1268: GCP      data[2311]            ; = 1
  1269: GADR     data[1968]           
  1270: ASGN                          
  1271: SSP      1                    
  1272: GCP      data[2312]            ; = 0.0f
  1273: GADR     data[1982]           
  1274: ASGN                          
  1275: SSP      1                    
  1276: GCP      data[2313]            ; = 503
  1277: GCP      data[1968]           
  1278: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1279: SSP      2                    
  1280: CALL     func_0294            
  1281: XCALL    $SC_MP_SRV_InitGameAfterInactive(void)void ; args=0
  1282: GCP      data[1969]           
  1283: GCP      data[2314]            ; = 6.0f
  1284: FGRE                          
  1285: JZ       label_1288           
  1286: XCALL    $SC_MP_RestartMission(void)void ; args=0
  1287: XCALL    $SC_MP_RecoverAllNoAiPlayers(void)void ; args=0
label_1288:
  1288: GCP      data[2315]            ; = 8.0f
  1289: GADR     data[1981]           
  1290: ASGN                          
  1291: SSP      1                    
label_1292:
  1292: JMP      label_1318           
label_1293:
  1293: GCP      data[1981]           
  1294: GCP      data[2316]            ; = 0.0f
  1295: FLEQ                          
  1296: JZ       label_1318           
  1297: GCP      data[2317]            ; = 1
  1298: XCALL    $SC_MP_SetInstantRecovery(int)void ; args=1
  1299: SSP      1                    
  1300: GCP      data[1968]           
  1301: GCP      data[2318]            ; = 0.0f
  1302: GRE                           
  1303: JZ       label_1318           
  1304: GCP      data[2319]            ; = 0.0f
  1305: GADR     data[1968]           
  1306: ASGN                          
  1307: SSP      1                    
  1308: GCP      data[2320]            ; = 0.0f
  1309: GADR     data[1982]           
  1310: ASGN                          
  1311: SSP      1                    
  1312: GCP      data[2321]            ; = 503
  1313: GCP      data[1968]           
  1314: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1315: SSP      2                    
  1316: CALL     func_0852            
  1317: CALL     func_0294            
label_1318:
  1318: GCP      data[2322]            ; = 0.0f
  1319: LADR     [sp+8]               
  1320: ASGN                          
  1321: SSP      1                    
label_1322:
  1322: LCP      [sp+8]               
  1323: GCP      data[2323]            ; = 2
  1324: ULES                          
  1325: JZ       label_1411           
  1326: GCP      data[2324]            ; = 0.0f
  1327: LADR     [sp+9]               
  1328: ASGN                          
  1329: SSP      1                    
label_1330:
  1330: LCP      [sp+9]               
  1331: GCP      data[0]              
  1332: ULES                          
  1333: JZ       label_1402           
  1334: GCP      data[2325]            ; = 0.0f
  1335: LADR     [sp+10]              
  1336: ASGN                          
  1337: SSP      1                    
label_1338:
  1338: LCP      [sp+10]              
  1339: GADR     data[1]              
  1340: LCP      [sp+8]               
  1341: GCP      data[2326]            ; = 24
  1342: MUL                           
  1343: ADD                           
  1344: LCP      [sp+9]               
  1345: GCP      data[2327]            ; = 4
  1346: MUL                           
  1347: ADD                           
  1348: DCP      4                    
  1349: ULES                          
  1350: JZ       label_1393           
  1351: GADR     data[1549]           
  1352: LCP      [sp+8]               
  1353: GCP      data[2328]            ; = 768
  1354: MUL                           
  1355: ADD                           
  1356: LCP      [sp+9]               
  1357: GCP      data[2329]            ; = 128
  1358: MUL                           
  1359: ADD                           
  1360: LCP      [sp+10]              
  1361: GCP      data[2330]            ; = 4
  1362: MUL                           
  1363: ADD                           
  1364: DCP      4                    
  1365: LADR     [sp-4]               
  1366: DADR     16                   
  1367: DCP      4                    
  1368: FSUB                          
  1369: GADR     data[1549]           
  1370: LCP      [sp+8]               
  1371: GCP      data[2331]            ; = 768
  1372: MUL                           
  1373: ADD                           
  1374: LCP      [sp+9]               
  1375: GCP      data[2332]            ; = 128
  1376: MUL                           
  1377: ADD                           
  1378: LCP      [sp+10]              
  1379: GCP      data[2333]            ; = 4
  1380: MUL                           
  1381: ADD                           
  1382: ASGN                          
  1383: SSP      1                    
  1384: LCP      [sp+10]              
  1385: LCP      [sp+10]              
  1386: GCP      data[2334]            ; = 1
  1387: ADD                           
  1388: LADR     [sp+10]              
  1389: ASGN                          
  1390: SSP      1                    
  1391: SSP      1                    
  1392: JMP      label_1338           
label_1393:
  1393: LCP      [sp+9]               
  1394: LCP      [sp+9]               
  1395: GCP      data[2335]            ; = 1
  1396: ADD                           
  1397: LADR     [sp+9]               
  1398: ASGN                          
  1399: SSP      1                    
  1400: SSP      1                    
  1401: JMP      label_1330           
label_1402:
  1402: LCP      [sp+8]               
  1403: LCP      [sp+8]               
  1404: GCP      data[2336]            ; = 1
  1405: ADD                           
  1406: LADR     [sp+8]               
  1407: ASGN                          
  1408: SSP      1                    
  1409: SSP      1                    
  1410: JMP      label_1322           
label_1411:
  1411: GCP      data[1983]           
  1412: LADR     [sp-4]               
  1413: DADR     16                   
  1414: DCP      4                    
  1415: FSUB                          
  1416: GADR     data[1983]           
  1417: ASGN                          
  1418: SSP      1                    
  1419: GCP      data[1983]           
  1420: GCP      data[2337]            ; = 0.0f
  1421: FLES                          
  1422: JZ       label_1430           
  1423: ASP      1                    
  1424: ASP      1                    
  1425: CALL     func_0119            
  1426: LLD      [sp+419]             
  1427: GADR     data[1983]           
  1428: ASGN                          
  1429: SSP      1                    
label_1430:
  1430: GCP      data[1968]           
  1431: JMP      label_1433           
  1432: JMP      label_1437           
label_1433:
  1433: LCP      [sp+419]             
  1434: GCP      data[2338]            ; = 0.0f
  1435: EQU                           
  1436: JZ       label_1462           
label_1437:
  1437: GCP      data[1969]           
  1438: LADR     [sp-4]               
  1439: DADR     16                   
  1440: DCP      4                    
  1441: FADD                          
  1442: GADR     data[1969]           
  1443: ASGN                          
  1444: SSP      1                    
  1445: GCP      data[1972]           
  1446: GCP      data[2339]            ; = -10.0f
  1447: FGRE                          
  1448: JZ       label_1460           
  1449: GCP      data[2340]            ; = -10.0f
  1450: GADR     data[1972]           
  1451: ASGN                          
  1452: SSP      1                    
  1453: GCP      data[2341]            ; = -1.0f
  1454: GADR     data[1971]           
  1455: ASGN                          
  1456: SSP      1                    
  1457: GCP      data[2342]            ; = 0.0f
  1458: CALL     func_0264            
  1459: SSP      1                    
label_1460:
  1460: JMP      label_1710           
  1461: JMP      label_1466           
label_1462:
  1462: LCP      [sp+419]             
  1463: GCP      data[2343]            ; = 1
  1464: EQU                           
  1465: JZ       label_1671           
label_1466:
  1466: GCP      data[1982]           
  1467: LADR     [sp-4]               
  1468: DADR     16                   
  1469: DCP      4                    
  1470: FADD                          
  1471: GADR     data[1982]           
  1472: ASGN                          
  1473: SSP      1                    
  1474: GCP      data[1972]           
  1475: LADR     [sp-4]               
  1476: DADR     16                   
  1477: DCP      4                    
  1478: FSUB                          
  1479: GADR     data[1972]           
  1480: ASGN                          
  1481: SSP      1                    
  1482: LADR     [sp-4]               
  1483: DADR     16                   
  1484: DCP      4                    
  1485: CALL     func_0264            
  1486: SSP      1                    
  1487: GCP      data[1972]           
  1488: GCP      data[2344]            ; = 0.0f
  1489: FLEQ                          
  1490: JZ       label_1505           
  1491: GCP      data[2345]            ; = 3
  1492: GADR     data[1968]           
  1493: ASGN                          
  1494: SSP      1                    
  1495: GCP      data[2346]            ; = 503
  1496: GCP      data[1968]           
  1497: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1498: SSP      2                    
  1499: GCP      data[2347]            ; = 8.0f
  1500: GADR     data[1970]           
  1501: ASGN                          
  1502: SSP      1                    
  1503: CALL     func_0355            
  1504: JMP      label_1669           
label_1505:
  1505: GCP      data[1982]           
  1506: GCP      data[2348]            ; = 5.0f
  1507: FGRE                          
  1508: JZ       label_1669           
  1509: GCP      data[1967]           
  1510: GCP      data[2349]            ; = 0.0f
  1511: UGRE                          
  1512: JZ       label_1669           
  1513: GCP      data[2350]            ; = 0.0f
  1514: LADR     [sp+8]               
  1515: ASGN                          
  1516: SSP      1                    
label_1517:
  1517: LCP      [sp+8]               
  1518: LCP      [sp+12]              
  1519: ULES                          
  1520: JZ       label_1669           
  1521: LADR     [sp+29]              
  1522: LCP      [sp+8]               
  1523: GCP      data[2351]            ; = 16
  1524: MUL                           
  1525: ADD                           
  1526: PNT      4                    
  1527: DCP      4                    
  1528: GCP      data[1966]           
  1529: EQU                           
  1530: JZ       label_1660           
  1531: LADR     [sp+29]              
  1532: LCP      [sp+8]               
  1533: GCP      data[2352]            ; = 16
  1534: MUL                           
  1535: ADD                           
  1536: PNT      8                    
  1537: DCP      4                    
  1538: GCP      data[2353]            ; = 1
  1539: EQU                           
  1540: JZ       label_1660           
  1541: JMP      label_1542           
label_1542:
  1542: LADR     [sp+29]              
  1543: LCP      [sp+8]               
  1544: GCP      data[2354]            ; = 16
  1545: MUL                           
  1546: ADD                           
  1547: DCP      4                    
  1548: LADR     [sp+311]             
  1549: XCALL    $SC_P_GetPos(unsignedlong,*c_Vector3)void ; args=2
  1550: SSP      2                    
  1551: GCP      data[1967]           
  1552: GCP      data[2355]            ; = 1
  1553: SUB                           
  1554: LADR     [sp+9]               
  1555: ASGN                          
  1556: SSP      1                    
label_1557:
  1557: LCP      [sp+9]               
  1558: GCP      data[1967]           
  1559: ULES                          
  1560: JZ       label_1660           
  1561: ASP      1                    
  1562: LADR     [sp+311]             
  1563: GADR     data[1933]           
  1564: LCP      [sp+9]               
  1565: GCP      data[2356]            ; = 16
  1566: MUL                           
  1567: ADD                           
  1568: GADR     data[1933]           
  1569: LCP      [sp+9]               
  1570: GCP      data[2357]            ; = 16
  1571: MUL                           
  1572: ADD                           
  1573: PNT      12                   
  1574: DCP      4                    
  1575: ASP      1                    
  1576: XCALL    $SC_IsNear3D(*c_Vector3,*c_Vector3,float)int ; args=3
  1577: LLD      [sp+420]             
  1578: SSP      3                    
  1579: JZ       label_1651           
  1580: LCP      [sp+9]               
  1581: JZ       label_1615           
  1582: LCP      [sp+9]               
  1583: GADR     data[1967]           
  1584: ASGN                          
  1585: SSP      1                    
  1586: GCP      data[2358]            ; = 510
  1587: ASP      1                    
  1588: LADR     [sp+29]              
  1589: LCP      [sp+8]               
  1590: GCP      data[2359]            ; = 16
  1591: MUL                           
  1592: ADD                           
  1593: DCP      4                    
  1594: ASP      1                    
  1595: XCALL    $SC_MP_GetHandleofPl(unsignedlong)unsignedlong ; args=1
  1596: LLD      [sp+421]             
  1597: SSP      1                    
  1598: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1599: SSP      2                    
  1600: GCP      data[2360]            ; = 507
  1601: GCP      data[1967]           
  1602: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1603: SSP      2                    
  1604: CALL     func_1028            
  1605: LADR     [sp+29]              
  1606: LCP      [sp+8]               
  1607: GCP      data[2361]            ; = 16
  1608: MUL                           
  1609: ADD                           
  1610: DCP      4                    
  1611: GCP      data[2362]            ; = 1
  1612: XCALL    $SC_P_MP_AddPoints(unsignedlong,int)void ; args=2
  1613: SSP      2                    
  1614: JMP      label_1651           
label_1615:
  1615: GCP      data[2363]            ; = 2
  1616: GADR     data[1968]           
  1617: ASGN                          
  1618: SSP      1                    
  1619: GCP      data[2364]            ; = 510
  1620: ASP      1                    
  1621: LADR     [sp+29]              
  1622: LCP      [sp+8]               
  1623: GCP      data[2365]            ; = 16
  1624: MUL                           
  1625: ADD                           
  1626: DCP      4                    
  1627: ASP      1                    
  1628: XCALL    $SC_MP_GetHandleofPl(unsignedlong)unsignedlong ; args=1
  1629: LLD      [sp+421]             
  1630: SSP      1                    
  1631: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1632: SSP      2                    
  1633: GCP      data[2366]            ; = 503
  1634: GCP      data[1968]           
  1635: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1636: SSP      2                    
  1637: GCP      data[2367]            ; = 8.0f
  1638: GADR     data[1970]           
  1639: ASGN                          
  1640: SSP      1                    
  1641: CALL     func_0355            
  1642: LADR     [sp+29]              
  1643: LCP      [sp+8]               
  1644: GCP      data[2368]            ; = 16
  1645: MUL                           
  1646: ADD                           
  1647: DCP      4                    
  1648: GCP      data[2369]            ; = 2
  1649: XCALL    $SC_P_MP_AddPoints(unsignedlong,int)void ; args=2
  1650: SSP      2                    
label_1651:
  1651: LCP      [sp+9]               
  1652: LCP      [sp+9]               
  1653: GCP      data[2370]            ; = 1
  1654: ADD                           
  1655: LADR     [sp+9]               
  1656: ASGN                          
  1657: SSP      1                    
  1658: SSP      1                    
  1659: JMP      label_1557           
label_1660:
  1660: LCP      [sp+8]               
  1661: LCP      [sp+8]               
  1662: GCP      data[2371]            ; = 1
  1663: ADD                           
  1664: LADR     [sp+8]               
  1665: ASGN                          
  1666: SSP      1                    
  1667: SSP      1                    
  1668: JMP      label_1517           
label_1669:
  1669: JMP      label_1710           
  1670: JMP      label_1675           
label_1671:
  1671: LCP      [sp+419]             
  1672: GCP      data[2372]            ; = 3
  1673: EQU                           
  1674: JZ       label_1676           
label_1675:
  1675: JMP      label_1680           
label_1676:
  1676: LCP      [sp+419]             
  1677: GCP      data[2373]            ; = 2
  1678: EQU                           
  1679: JZ       label_1710           
label_1680:
  1680: GCP      data[1970]           
  1681: LADR     [sp-4]               
  1682: DADR     16                   
  1683: DCP      4                    
  1684: FSUB                          
  1685: GADR     data[1970]           
  1686: ASGN                          
  1687: SSP      1                    
  1688: GCP      data[1970]           
  1689: GCP      data[2374]            ; = 0.0f
  1690: FLES                          
  1691: JZ       label_1709           
  1692: GCP      data[2375]            ; = 0.0f
  1693: GADR     data[1969]           
  1694: ASGN                          
  1695: SSP      1                    
  1696: GCP      data[2376]            ; = 0.0f
  1697: GADR     data[1968]           
  1698: ASGN                          
  1699: SSP      1                    
  1700: GCP      data[2377]            ; = 503
  1701: GCP      data[1968]           
  1702: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  1703: SSP      2                    
  1704: CALL     func_0852            
  1705: GCP      data[2378]            ; = 1
  1706: XCALL    $SC_MP_SetInstantRecovery(int)void ; args=1
  1707: SSP      1                    
  1708: XCALL    $SC_MP_RecoverAllNoAiPlayers(void)void ; args=0
label_1709:
  1709: JMP      label_1710           
label_1710:
  1710: SSP      1                    
  1711: JMP      label_3732           
  1712: JMP      label_1717           
label_1713:
  1713: LCP      [sp+418]             
  1714: GCP      data[2379]            ; = 4
  1715: EQU                           
  1716: JZ       label_2051           
label_1717:
  1717: GCP      data[1978]           
  1718: LADR     [sp-4]               
  1719: DADR     16                   
  1720: DCP      4                    
  1721: FSUB                          
  1722: GADR     data[1978]           
  1723: ASGN                          
  1724: SSP      1                    
  1725: GCP      data[1979]           
  1726: GCP      data[2380]            ; = 0.0f
  1727: FGRE                          
  1728: JZ       label_1737           
  1729: GCP      data[1979]           
  1730: LADR     [sp-4]               
  1731: DADR     16                   
  1732: DCP      4                    
  1733: FSUB                          
  1734: GADR     data[1979]           
  1735: ASGN                          
  1736: SSP      1                    
label_1737:
  1737: GCP      data[1980]           
  1738: GCP      data[2381]            ; = 0.0f
  1739: FGRE                          
  1740: JZ       label_1749           
  1741: GCP      data[1980]           
  1742: LADR     [sp-4]               
  1743: DADR     16                   
  1744: DCP      4                    
  1745: FSUB                          
  1746: GADR     data[1980]           
  1747: ASGN                          
  1748: SSP      1                    
label_1749:
  1749: ASP      1                    
  1750: GCP      data[2382]            ; = 503
  1751: ASP      1                    
  1752: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1753: LLD      [sp+419]             
  1754: SSP      1                    
  1755: JMP      label_1757           
  1756: JMP      label_1761           
label_1757:
  1757: LCP      [sp+419]             
  1758: GCP      data[2383]            ; = 0.0f
  1759: EQU                           
  1760: JZ       label_1774           
label_1761:
  1761: ASP      1                    
  1762: GCP      data[2384]            ; = 508
  1763: ASP      1                    
  1764: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1765: LLD      [sp+420]             
  1766: SSP      1                    
  1767: GCP      data[2385]            ; = 1
  1768: SUB                           
  1769: GCP      data[2386]            ; = 2
  1770: CALL     func_0498            
  1771: SSP      2                    
  1772: JMP      label_1834           
  1773: JMP      label_1778           
label_1774:
  1774: LCP      [sp+419]             
  1775: GCP      data[2387]            ; = 1
  1776: EQU                           
  1777: JZ       label_1834           
label_1778:
  1778: GCP      data[1977]           
  1779: ASP      1                    
  1780: GCP      data[2388]            ; = 507
  1781: ASP      1                    
  1782: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1783: LLD      [sp+421]             
  1784: SSP      1                    
  1785: NEQ                           
  1786: JZ       label_1819           
  1787: ASP      1                    
  1788: GCP      data[2389]            ; = 507
  1789: ASP      1                    
  1790: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1791: LLD      [sp+420]             
  1792: SSP      1                    
  1793: GADR     data[1977]           
  1794: ASGN                          
  1795: SSP      1                    
  1796: GCP      data[1977]           
  1797: ASP      1                    
  1798: GCP      data[2390]            ; = 508
  1799: ASP      1                    
  1800: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1801: LLD      [sp+421]             
  1802: SSP      1                    
  1803: GCP      data[2391]            ; = 1
  1804: SUB                           
  1805: ULES                          
  1806: JZ       label_1819           
  1807: GCP      data[1977]           
  1808: GCP      data[2392]            ; = 0.0f
  1809: UGRE                          
  1810: JZ       label_1819           
  1811: JMP      label_1812           
label_1812:
  1812: GCP      data[2393]            ; = 5.0f
  1813: GADR     data[1978]           
  1814: ASGN                          
  1815: SSP      1                    
  1816: GCP      data[2394]            ; = 10425
  1817: XCALL    $SC_SND_PlaySound2D(unsignedlong)void ; args=1
  1818: SSP      1                    
label_1819:
  1819: ASP      1                    
  1820: ASP      1                    
  1821: GCP      data[2395]            ; = 502
  1822: ASP      1                    
  1823: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1824: LLD      [sp+421]             
  1825: SSP      1                    
  1826: ASP      1                    
  1827: CALL     func_0334            
  1828: LLD      [sp+420]             
  1829: SSP      1                    
  1830: GCP      data[1977]           
  1831: CALL     func_0498            
  1832: SSP      2                    
  1833: JMP      label_1834           
label_1834:
  1834: SSP      1                    
  1835: GCP      data[1975]           
  1836: ASP      1                    
  1837: GCP      data[2396]            ; = 505
  1838: ASP      1                    
  1839: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1840: LLD      [sp+420]             
  1841: SSP      1                    
  1842: NEQ                           
  1843: JZ       label_1863           
  1844: ASP      1                    
  1845: GCP      data[2397]            ; = 505
  1846: ASP      1                    
  1847: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1848: LLD      [sp+419]             
  1849: SSP      1                    
  1850: GADR     data[1975]           
  1851: ASGN                          
  1852: SSP      1                    
  1853: ASP      1                    
  1854: GCP      data[2398]            ; = 504
  1855: ASP      1                    
  1856: XCALL    $SC_ggf(unsignedlong)float ; args=1
  1857: LLD      [sp+419]             
  1858: SSP      1                    
  1859: GADR     data[1976]           
  1860: ASGN                          
  1861: SSP      1                    
  1862: JMP      label_1880           
label_1863:
  1863: ASP      1                    
  1864: GCP      data[2399]            ; = 503
  1865: ASP      1                    
  1866: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1867: LLD      [sp+419]             
  1868: SSP      1                    
  1869: GCP      data[2400]            ; = 1
  1870: EQU                           
  1871: JZ       label_1880           
  1872: GCP      data[1976]           
  1873: LADR     [sp-4]               
  1874: DADR     16                   
  1875: DCP      4                    
  1876: FSUB                          
  1877: GADR     data[1976]           
  1878: ASGN                          
  1879: SSP      1                    
label_1880:
  1880: GCP      data[2401]            ; = 0.0f
  1881: LADR     [sp+8]               
  1882: ASGN                          
  1883: SSP      1                    
label_1884:
  1884: LCP      [sp+8]               
  1885: GCP      data[2402]            ; = 2
  1886: ULES                          
  1887: JZ       label_1964           
  1888: ASP      1                    
  1889: GCP      data[2403]            ; = 500
  1890: LCP      [sp+8]               
  1891: ADD                           
  1892: ASP      1                    
  1893: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1894: LLD      [sp+419]             
  1895: SSP      1                    
  1896: GADR     data[1962]           
  1897: LCP      [sp+8]               
  1898: GCP      data[2404]            ; = 4
  1899: MUL                           
  1900: ADD                           
  1901: ASGN                          
  1902: SSP      1                    
  1903: LCP      [sp+8]               
  1904: GCP      data[2405]            ; = 0.0f
  1905: GADR     data[1962]           
  1906: LCP      [sp+8]               
  1907: GCP      data[2406]            ; = 4
  1908: MUL                           
  1909: ADD                           
  1910: DCP      4                    
  1911: XCALL    $SC_MP_SetSideStats(unsignedlong,int,int)void ; args=3
  1912: SSP      3                    
  1913: GCP      data[2407]            ; = 1
  1914: LADR     [sp+299]             
  1915: LCP      [sp+8]               
  1916: GCP      data[2408]            ; = 16
  1917: MUL                           
  1918: ADD                           
  1919: PNT      4                    
  1920: ASGN                          
  1921: SSP      1                    
  1922: GCP      data[2409]            ; = 3
  1923: LCP      [sp+8]               
  1924: MUL                           
  1925: LADR     [sp+299]             
  1926: LCP      [sp+8]               
  1927: GCP      data[2410]            ; = 16
  1928: MUL                           
  1929: ADD                           
  1930: ASGN                          
  1931: SSP      1                    
  1932: GADR     data[1962]           
  1933: LCP      [sp+8]               
  1934: GCP      data[2411]            ; = 4
  1935: MUL                           
  1936: ADD                           
  1937: DCP      4                    
  1938: LADR     [sp+299]             
  1939: LCP      [sp+8]               
  1940: GCP      data[2412]            ; = 16
  1941: MUL                           
  1942: ADD                           
  1943: PNT      8                    
  1944: ASGN                          
  1945: SSP      1                    
  1946: GCP      data[2413]            ; = -1140850689
  1947: LADR     [sp+299]             
  1948: LCP      [sp+8]               
  1949: GCP      data[2414]            ; = 16
  1950: MUL                           
  1951: ADD                           
  1952: PNT      12                   
  1953: ASGN                          
  1954: SSP      1                    
  1955: LCP      [sp+8]               
  1956: LCP      [sp+8]               
  1957: GCP      data[2415]            ; = 1
  1958: ADD                           
  1959: LADR     [sp+8]               
  1960: ASGN                          
  1961: SSP      1                    
  1962: SSP      1                    
  1963: JMP      label_1884           
label_1964:
  1964: GCP      data[2416]            ; = 2
  1965: LADR     [sp+11]              
  1966: ASGN                          
  1967: SSP      1                    
  1968: GCP      data[1976]           
  1969: GCP      data[2417]            ; = 0.0f
  1970: FGRE                          
  1971: JZ       label_2045           
  1972: ASP      1                    
  1973: GCP      data[2418]            ; = 503
  1974: ASP      1                    
  1975: XCALL    $SC_ggi(unsignedlong)int ; args=1
  1976: LLD      [sp+419]             
  1977: SSP      1                    
  1978: JZ       label_2045           
  1979: JMP      label_1980           
label_1980:
  1980: GCP      data[2419]            ; = -1140850689
  1981: LADR     [sp+299]             
  1982: LCP      [sp+11]              
  1983: GCP      data[2420]            ; = 16
  1984: MUL                           
  1985: ADD                           
  1986: PNT      12                   
  1987: ASGN                          
  1988: SSP      1                    
  1989: GCP      data[2421]            ; = 6
  1990: LADR     [sp+299]             
  1991: LCP      [sp+11]              
  1992: GCP      data[2422]            ; = 16
  1993: MUL                           
  1994: ADD                           
  1995: ASGN                          
  1996: SSP      1                    
  1997: ASP      1                    
  1998: GCP      data[2423]            ; = 503
  1999: ASP      1                    
  2000: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2001: LLD      [sp+419]             
  2002: SSP      1                    
  2003: GCP      data[2424]            ; = 3
  2004: EQU                           
  2005: JZ       label_2016           
  2006: GCP      data[2425]            ; = 0.0f
  2007: LADR     [sp+299]             
  2008: LCP      [sp+11]              
  2009: GCP      data[2426]            ; = 16
  2010: MUL                           
  2011: ADD                           
  2012: PNT      8                    
  2013: ASGN                          
  2014: SSP      1                    
  2015: JMP      label_2028           
label_2016:
  2016: GCP      data[1976]           
  2017: GCP      data[2427]            ; = 1065185444
  2018: FADD                          
  2019: FTOI                          
  2020: LADR     [sp+299]             
  2021: LCP      [sp+11]              
  2022: GCP      data[2428]            ; = 16
  2023: MUL                           
  2024: ADD                           
  2025: PNT      8                    
  2026: ASGN                          
  2027: SSP      1                    
label_2028:
  2028: GCP      data[2429]            ; = 2
  2029: LADR     [sp+299]             
  2030: LCP      [sp+11]              
  2031: GCP      data[2430]            ; = 16
  2032: MUL                           
  2033: ADD                           
  2034: PNT      4                    
  2035: ASGN                          
  2036: SSP      1                    
  2037: LCP      [sp+11]              
  2038: LCP      [sp+11]              
  2039: GCP      data[2431]            ; = 1
  2040: ADD                           
  2041: LADR     [sp+11]              
  2042: ASGN                          
  2043: SSP      1                    
  2044: SSP      1                    
label_2045:
  2045: LADR     [sp+299]             
  2046: LCP      [sp+11]              
  2047: XCALL    $SC_MP_SetIconHUD(*s_SC_HUD_MP_icon,unsignedlong)void ; args=2
  2048: SSP      2                    
  2049: JMP      label_3732           
  2050: JMP      label_2055           
label_2051:
  2051: LCP      [sp+418]             
  2052: GCP      data[2432]            ; = 9
  2053: EQU                           
  2054: JZ       label_2080           
label_2055:
  2055: GCP      data[2433]            ; = 499
  2056: GCP      data[2434]            ; = 9
  2057: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  2058: SSP      2                    
  2059: LADR     [sp-4]               
  2060: DADR     4                    
  2061: DCP      4                    
  2062: GADR     data[1957]           
  2063: ASGN                          
  2064: SSP      1                    
  2065: LADR     [sp-4]               
  2066: DADR     8                    
  2067: DCP      4                    
  2068: GADR     data[1958]           
  2069: ASGN                          
  2070: SSP      1                    
  2071: GCP      data[2435]            ; = 0.0f
  2072: GADR     data[1959]           
  2073: ASGN                          
  2074: SSP      1                    
  2075: GCP      data[2436]            ; = 0.0f
  2076: XCALL    $SC_MP_EnableBotsFromScene(int)void ; args=1
  2077: SSP      1                    
  2078: JMP      label_3732           
  2079: JMP      label_2084           
label_2080:
  2080: LCP      [sp+418]             
  2081: GCP      data[2437]            ; = 1
  2082: EQU                           
  2083: JZ       label_2794           
label_2084:
  2084: ASP      1                    
  2085: GADR     data[2438]  ; "g\weapons\Vvh_map\icons\MPIC_USflag.BES"
  2086: ASP      1                    
  2087: XCALL    $SC_MP_FpvMapSign_Load(*char)unsignedlong ; args=1
  2088: LLD      [sp+419]             
  2089: SSP      1                    
  2090: GADR     data[2109]           
  2091: ASGN                          
  2092: SSP      1                    
  2093: ASP      1                    
  2094: GADR     data[2448]  ; "g\weapons\Vvh_map\icons\MPIC_VCflag.BES"
  2095: ASP      1                    
  2096: XCALL    $SC_MP_FpvMapSign_Load(*char)unsignedlong ; args=1
  2097: LLD      [sp+419]             
  2098: SSP      1                    
  2099: GADR     data[2110]           
  2100: ASGN                          
  2101: SSP      1                    
  2102: ASP      1                    
  2103: GADR     data[2458]           
  2104: ASP      1                    
  2105: XCALL    $SC_MP_FpvMapSign_Load(*char)unsignedlong ; args=1
  2106: LLD      [sp+419]             
  2107: SSP      1                    
  2108: GADR     data[2111]           
  2109: ASGN                          
  2110: SSP      1                    
  2111: GCP      data[2469]            ; = -1
  2112: XCALL    $SC_MP_SRV_SetForceSide(unsignedlong)void ; args=1
  2113: SSP      1                    
  2114: GCP      data[2470]            ; = 3
  2115: XCALL    $SC_MP_SetChooseValidSides(unsignedlong)void ; args=1
  2116: SSP      1                    
  2117: GCP      data[2471]            ; = 18
  2118: GCP      data[2472]            ; = 0.0f
  2119: XCALL    $SC_MP_SRV_SetClassLimit(unsignedlong,unsignedlong)void ; args=2
  2120: SSP      2                    
  2121: GCP      data[2473]            ; = 19
  2122: GCP      data[2474]            ; = 0.0f
  2123: XCALL    $SC_MP_SRV_SetClassLimit(unsignedlong,unsignedlong)void ; args=2
  2124: SSP      2                    
  2125: GCP      data[2475]            ; = 39
  2126: GCP      data[2476]            ; = 0.0f
  2127: XCALL    $SC_MP_SRV_SetClassLimit(unsignedlong,unsignedlong)void ; args=2
  2128: SSP      2                    
  2129: LADR     [sp+285]             
  2130: XCALL    $SC_MP_GetSRVsettings(*s_SC_MP_SRV_settings)void ; args=1
  2131: SSP      1                    
  2132: GCP      data[2477]            ; = 0.0f
  2133: LADR     [sp+8]               
  2134: ASGN                          
  2135: SSP      1                    
label_2136:
  2136: LCP      [sp+8]               
  2137: GCP      data[2478]            ; = 6
  2138: ULES                          
  2139: JZ       label_2173           
  2140: LCP      [sp+8]               
  2141: GCP      data[2479]            ; = 1
  2142: ADD                           
  2143: LADR     [sp+285]             
  2144: PNT      12                   
  2145: LCP      [sp+8]               
  2146: GCP      data[2480]            ; = 4
  2147: MUL                           
  2148: ADD                           
  2149: DCP      4                    
  2150: XCALL    $SC_MP_SRV_SetClassLimit(unsignedlong,unsignedlong)void ; args=2
  2151: SSP      2                    
  2152: LCP      [sp+8]               
  2153: GCP      data[2481]            ; = 21
  2154: ADD                           
  2155: LADR     [sp+285]             
  2156: PNT      12                   
  2157: LCP      [sp+8]               
  2158: GCP      data[2482]            ; = 4
  2159: MUL                           
  2160: ADD                           
  2161: DCP      4                    
  2162: XCALL    $SC_MP_SRV_SetClassLimit(unsignedlong,unsignedlong)void ; args=2
  2163: SSP      2                    
  2164: LCP      [sp+8]               
  2165: LCP      [sp+8]               
  2166: GCP      data[2483]            ; = 1
  2167: ADD                           
  2168: LADR     [sp+8]               
  2169: ASGN                          
  2170: SSP      1                    
  2171: SSP      1                    
  2172: JMP      label_2136           
label_2173:
  2173: LADR     [sp+14]              
  2174: GCP      data[2484]            ; = 60
  2175: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  2176: SSP      2                    
  2177: GCP      data[2485]            ; = 5100
  2178: LADR     [sp+14]              
  2179: ASGN                          
  2180: SSP      1                    
  2181: GCP      data[2486]            ; = 1
  2182: LADR     [sp+14]              
  2183: PNT      40                   
  2184: GCP      data[2487]            ; = 0.0f
  2185: ADD                           
  2186: ASGN                          
  2187: SSP      1                    
  2188: GCP      data[2488]            ; = 3
  2189: LADR     [sp+14]              
  2190: PNT      40                   
  2191: GCP      data[2489]            ; = 4
  2192: ADD                           
  2193: ASGN                          
  2194: SSP      1                    
  2195: GCP      data[2490]            ; = -2147483644
  2196: LADR     [sp+14]              
  2197: PNT      40                   
  2198: GCP      data[2491]            ; = 8
  2199: ADD                           
  2200: ASGN                          
  2201: SSP      1                    
  2202: GCP      data[2492]            ; = -2147483643
  2203: LADR     [sp+14]              
  2204: PNT      40                   
  2205: GCP      data[2493]            ; = 12
  2206: ADD                           
  2207: ASGN                          
  2208: SSP      1                    
  2209: GCP      data[2494]            ; = 27
  2210: LADR     [sp+14]              
  2211: PNT      32                   
  2212: ASGN                          
  2213: SSP      1                    
  2214: GCP      data[2495]            ; = 1
  2215: LADR     [sp+14]              
  2216: PNT      4                    
  2217: ASGN                          
  2218: SSP      1                    
  2219: GCP      data[2496]            ; = 1010
  2220: LADR     [sp+14]              
  2221: PNT      16                   
  2222: GCP      data[2497]            ; = 0.0f
  2223: ADD                           
  2224: ASGN                          
  2225: SSP      1                    
  2226: GCP      data[2498]            ; = 1140850943
  2227: LADR     [sp+14]              
  2228: PNT      24                   
  2229: GCP      data[2499]            ; = 0.0f
  2230: ADD                           
  2231: ASGN                          
  2232: SSP      1                    
  2233: GCP      data[2500]            ; = 1011
  2234: LADR     [sp+14]              
  2235: PNT      16                   
  2236: GCP      data[2501]            ; = 4
  2237: ADD                           
  2238: ASGN                          
  2239: SSP      1                    
  2240: GCP      data[2502]            ; = 2040.0f
  2241: LADR     [sp+14]              
  2242: PNT      24                   
  2243: GCP      data[2503]            ; = 4
  2244: ADD                           
  2245: ASGN                          
  2246: SSP      1                    
  2247: GCP      data[2504]            ; = 1
  2248: LADR     [sp+14]              
  2249: PNT      36                   
  2250: ASGN                          
  2251: SSP      1                    
  2252: LADR     [sp+14]              
  2253: XCALL    $SC_MP_HUD_SetTabInfo(*s_SC_MP_hud)void ; args=1
  2254: SSP      1                    
  2255: GCP      data[2505]            ; = 1
  2256: XCALL    $SC_MP_AllowStPwD(int)void ; args=1
  2257: SSP      1                    
  2258: GCP      data[2506]            ; = 1
  2259: XCALL    $SC_MP_AllowFriendlyFireOFF(int)void ; args=1
  2260: SSP      1                    
  2261: GCP      data[2507]            ; = 0.0f
  2262: XCALL    $SC_MP_SetItemsNoDisappear(int)void ; args=1
  2263: SSP      1                    
  2264: LADR     [sp-4]               
  2265: DADR     8                    
  2266: DCP      4                    
  2267: JZ       label_2792           
  2268: GADR     data[1984]           
  2269: GCP      data[2508]            ; = 72
  2270: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  2271: SSP      2                    
  2272: GCP      data[2509]            ; = 0.0f
  2273: LADR     [sp+8]               
  2274: ASGN                          
  2275: SSP      1                    
label_2276:
  2276: LCP      [sp+8]               
  2277: GCP      data[2510]            ; = 6
  2278: ULES                          
  2279: JZ       label_2367           
  2280: ASP      1                    
  2281: LADR     [sp+0]               
  2282: GADR     data[2511]  ; "TT_flag_%d"
  2283: LCP      [sp+8]               
  2284: ASP      1                    
  2285: GCP      data[2514]            ; = 3
  2286: XCALL    $sprintf(*char,*constchar,...)int ; args=4294967295
  2287: LLD      [sp+419]             
  2288: SSP      3                    
  2289: SSP      1                    
  2290: ASP      1                    
  2291: GCP      data[2515]            ; = 0.0f
  2292: LADR     [sp+0]               
  2293: ASP      1                    
  2294: XCALL    $SC_NOD_GetNoMessage(*void,*char)*void ; args=2
  2295: LLD      [sp+419]             
  2296: SSP      2                    
  2297: LADR     [sp+295]             
  2298: ASGN                          
  2299: SSP      1                    
  2300: LCP      [sp+295]             
  2301: JZ       label_2358           
  2302: LCP      [sp+295]             
  2303: GADR     data[2002]           
  2304: LCP      [sp+8]               
  2305: GCP      data[2516]            ; = 12
  2306: MUL                           
  2307: ADD                           
  2308: XCALL    $SC_NOD_GetPivotWorld(*void,*c_Vector3)void ; args=2
  2309: SSP      2                    
  2310: ASP      1                    
  2311: LCP      [sp+295]             
  2312: GADR     data[2517]  ; "vlajkaUS"
  2313: ASP      1                    
  2314: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  2315: LLD      [sp+419]             
  2316: SSP      2                    
  2317: GADR     data[1984]           
  2318: LCP      [sp+8]               
  2319: GCP      data[2520]            ; = 12
  2320: MUL                           
  2321: ADD                           
  2322: GCP      data[2521]            ; = 0.0f
  2323: ADD                           
  2324: ASGN                          
  2325: SSP      1                    
  2326: ASP      1                    
  2327: LCP      [sp+295]             
  2328: GADR     data[2522]  ; "Vlajka VC"
  2329: ASP      1                    
  2330: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  2331: LLD      [sp+419]             
  2332: SSP      2                    
  2333: GADR     data[1984]           
  2334: LCP      [sp+8]               
  2335: GCP      data[2525]            ; = 12
  2336: MUL                           
  2337: ADD                           
  2338: GCP      data[2526]            ; = 4
  2339: ADD                           
  2340: ASGN                          
  2341: SSP      1                    
  2342: ASP      1                    
  2343: LCP      [sp+295]             
  2344: GADR     data[2527]  ; "vlajka N"
  2345: ASP      1                    
  2346: XCALL    $SC_NOD_Get(*void,*char)*void ; args=2
  2347: LLD      [sp+419]             
  2348: SSP      2                    
  2349: GADR     data[1984]           
  2350: LCP      [sp+8]               
  2351: GCP      data[2530]            ; = 12
  2352: MUL                           
  2353: ADD                           
  2354: GCP      data[2531]            ; = 8
  2355: ADD                           
  2356: ASGN                          
  2357: SSP      1                    
label_2358:
  2358: LCP      [sp+8]               
  2359: LCP      [sp+8]               
  2360: GCP      data[2532]            ; = 1
  2361: ADD                           
  2362: LADR     [sp+8]               
  2363: ASGN                          
  2364: SSP      1                    
  2365: SSP      1                    
  2366: JMP      label_2276           
label_2367:
  2367: LADR     [sp-4]               
  2368: DADR     4                    
  2369: DCP      4                    
  2370: JZ       label_2792           
  2371: GCP      data[2533]            ; = 500
  2372: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2373: SSP      1                    
  2374: GCP      data[2534]            ; = 501
  2375: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2376: SSP      1                    
  2377: CALL     func_0249            
  2378: GCP      data[2535]            ; = 503
  2379: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2380: SSP      1                    
  2381: GCP      data[2536]            ; = 503
  2382: GCP      data[2537]            ; = 0.0f
  2383: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  2384: SSP      2                    
  2385: GCP      data[2538]            ; = 502
  2386: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2387: SSP      1                    
  2388: GCP      data[2539]            ; = 502
  2389: GCP      data[2540]            ; = 0.0f
  2390: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  2391: SSP      2                    
  2392: GCP      data[2541]            ; = 506
  2393: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2394: SSP      1                    
  2395: GCP      data[2542]            ; = 506
  2396: GCP      data[2543]            ; = 0.0f
  2397: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  2398: SSP      2                    
  2399: GCP      data[2544]            ; = 509
  2400: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2401: SSP      1                    
  2402: GCP      data[2545]            ; = 509
  2403: GCP      data[2546]            ; = 0.0f
  2404: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  2405: SSP      2                    
  2406: GCP      data[2547]            ; = 510
  2407: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2408: SSP      1                    
  2409: GCP      data[2548]            ; = 510
  2410: GCP      data[2549]            ; = 0.0f
  2411: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  2412: SSP      2                    
  2413: GCP      data[2550]            ; = 507
  2414: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2415: SSP      1                    
  2416: GCP      data[2551]            ; = 507
  2417: GCP      data[2552]            ; = 0.0f
  2418: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  2419: SSP      2                    
  2420: GCP      data[2553]            ; = 508
  2421: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2422: SSP      1                    
  2423: GCP      data[2554]            ; = 504
  2424: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2425: SSP      1                    
  2426: GCP      data[2555]            ; = 505
  2427: XCALL    $SC_MP_Gvar_SetSynchro(unsignedlong)void ; args=1
  2428: SSP      1                    
  2429: GCP      data[2556]            ; = 504
  2430: GCP      data[2557]            ; = 0.0f
  2431: XCALL    $SC_sgf(unsignedlong,float)void ; args=2
  2432: SSP      2                    
  2433: GCP      data[2558]            ; = 505
  2434: GCP      data[2559]            ; = 0.0f
  2435: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  2436: SSP      2                    
  2437: GADR     data[1]              
  2438: GCP      data[2560]            ; = 48
  2439: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  2440: SSP      2                    
  2441: GCP      data[2561]            ; = 0.0f
  2442: LADR     [sp+10]              
  2443: ASGN                          
  2444: SSP      1                    
label_2445:
  2445: LCP      [sp+10]              
  2446: GCP      data[2562]            ; = 2
  2447: ULES                          
  2448: JZ       label_2662           
  2449: LCP      [sp+10]              
  2450: JZ       label_2456           
  2451: GCP      data[2563]            ; = 68
  2452: LADR     [sp+294]             
  2453: ASGN                          
  2454: SSP      1                    
  2455: JMP      label_2460           
label_2456:
  2456: GCP      data[2564]            ; = 65
  2457: LADR     [sp+294]             
  2458: ASGN                          
  2459: SSP      1                    
label_2460:
  2460: GCP      data[2565]            ; = 0.0f
  2461: LADR     [sp+9]               
  2462: ASGN                          
  2463: SSP      1                    
label_2464:
  2464: LCP      [sp+9]               
  2465: GCP      data[2566]            ; = 6
  2466: ULES                          
  2467: JZ       label_2653           
  2468: GCP      data[2567]            ; = 0.0f
  2469: LADR     [sp+8]               
  2470: ASGN                          
  2471: SSP      1                    
label_2472:
  2472: LCP      [sp+8]               
  2473: GCP      data[2568]            ; = 32
  2474: ULES                          
  2475: JZ       label_2560           
  2476: ASP      1                    
  2477: LADR     [sp+0]               
  2478: GADR     data[2569]  ; "TT_%c%d_%d"
  2479: LCP      [sp+294]             
  2480: LCP      [sp+9]               
  2481: LCP      [sp+8]               
  2482: ASP      1                    
  2483: GCP      data[2572]            ; = 5
  2484: XCALL    $sprintf(*char,*constchar,...)int ; args=4294967295
  2485: LLD      [sp+419]             
  2486: SSP      5                    
  2487: SSP      1                    
  2488: ASP      1                    
  2489: GADR     data[13]             
  2490: LCP      [sp+10]              
  2491: GCP      data[2573]            ; = 3072
  2492: MUL                           
  2493: ADD                           
  2494: LCP      [sp+9]               
  2495: GCP      data[2574]            ; = 512
  2496: MUL                           
  2497: ADD                           
  2498: GADR     data[1]              
  2499: LCP      [sp+10]              
  2500: GCP      data[2575]            ; = 24
  2501: MUL                           
  2502: ADD                           
  2503: LCP      [sp+9]               
  2504: GCP      data[2576]            ; = 4
  2505: MUL                           
  2506: ADD                           
  2507: DCP      4                    
  2508: GCP      data[2577]            ; = 16
  2509: MUL                           
  2510: ADD                           
  2511: LADR     [sp+0]               
  2512: ASP      1                    
  2513: XCALL    $SC_NET_FillRecover(*s_SC_MP_Recover,*char)int ; args=2
  2514: LLD      [sp+419]             
  2515: SSP      2                    
  2516: JZ       label_2551           
  2517: GADR     data[1]              
  2518: LCP      [sp+10]              
  2519: GCP      data[2578]            ; = 24
  2520: MUL                           
  2521: ADD                           
  2522: LCP      [sp+9]               
  2523: GCP      data[2579]            ; = 4
  2524: MUL                           
  2525: ADD                           
  2526: DCP      4                    
  2527: GADR     data[1]              
  2528: LCP      [sp+10]              
  2529: GCP      data[2580]            ; = 24
  2530: MUL                           
  2531: ADD                           
  2532: LCP      [sp+9]               
  2533: GCP      data[2581]            ; = 4
  2534: MUL                           
  2535: ADD                           
  2536: DCP      4                    
  2537: GCP      data[2582]            ; = 1
  2538: ADD                           
  2539: GADR     data[1]              
  2540: LCP      [sp+10]              
  2541: GCP      data[2583]            ; = 24
  2542: MUL                           
  2543: ADD                           
  2544: LCP      [sp+9]               
  2545: GCP      data[2584]            ; = 4
  2546: MUL                           
  2547: ADD                           
  2548: ASGN                          
  2549: SSP      1                    
  2550: SSP      1                    
label_2551:
  2551: LCP      [sp+8]               
  2552: LCP      [sp+8]               
  2553: GCP      data[2585]            ; = 1
  2554: ADD                           
  2555: LADR     [sp+8]               
  2556: ASGN                          
  2557: SSP      1                    
  2558: SSP      1                    
  2559: JMP      label_2472           
label_2560:
  2560: GADR     data[2085]           
  2561: LCP      [sp+10]              
  2562: GCP      data[2586]            ; = 24
  2563: MUL                           
  2564: ADD                           
  2565: LCP      [sp+9]               
  2566: GCP      data[2587]            ; = 4
  2567: MUL                           
  2568: ADD                           
  2569: DCP      4                    
  2570: JZ       label_2644           
  2571: GCP      data[2588]            ; = 32
  2572: GADR     data[1]              
  2573: LCP      [sp+10]              
  2574: GCP      data[2589]            ; = 24
  2575: MUL                           
  2576: ADD                           
  2577: LCP      [sp+9]               
  2578: GCP      data[2590]            ; = 4
  2579: MUL                           
  2580: ADD                           
  2581: DCP      4                    
  2582: SUB                           
  2583: LADR     [sp+8]               
  2584: ASGN                          
  2585: SSP      1                    
  2586: GADR     data[2085]           
  2587: LCP      [sp+10]              
  2588: GCP      data[2591]            ; = 24
  2589: MUL                           
  2590: ADD                           
  2591: LCP      [sp+9]               
  2592: GCP      data[2592]            ; = 4
  2593: MUL                           
  2594: ADD                           
  2595: DCP      4                    
  2596: GADR     data[13]             
  2597: LCP      [sp+10]              
  2598: GCP      data[2593]            ; = 3072
  2599: MUL                           
  2600: ADD                           
  2601: LCP      [sp+9]               
  2602: GCP      data[2594]            ; = 512
  2603: MUL                           
  2604: ADD                           
  2605: GADR     data[1]              
  2606: LCP      [sp+10]              
  2607: GCP      data[2595]            ; = 24
  2608: MUL                           
  2609: ADD                           
  2610: LCP      [sp+9]               
  2611: GCP      data[2596]            ; = 4
  2612: MUL                           
  2613: ADD                           
  2614: DCP      4                    
  2615: GCP      data[2597]            ; = 16
  2616: MUL                           
  2617: ADD                           
  2618: LADR     [sp+8]               
  2619: XCALL    $SC_MP_GetRecovers(unsignedlong,*s_SC_MP_Recover,*unsignedlong)void ; args=3
  2620: SSP      3                    
  2621: GADR     data[1]              
  2622: LCP      [sp+10]              
  2623: GCP      data[2598]            ; = 24
  2624: MUL                           
  2625: ADD                           
  2626: LCP      [sp+9]               
  2627: GCP      data[2599]            ; = 4
  2628: MUL                           
  2629: ADD                           
  2630: DCP      4                    
  2631: LCP      [sp+8]               
  2632: ADD                           
  2633: GADR     data[1]              
  2634: LCP      [sp+10]              
  2635: GCP      data[2600]            ; = 24
  2636: MUL                           
  2637: ADD                           
  2638: LCP      [sp+9]               
  2639: GCP      data[2601]            ; = 4
  2640: MUL                           
  2641: ADD                           
  2642: ASGN                          
  2643: SSP      1                    
label_2644:
  2644: LCP      [sp+9]               
  2645: LCP      [sp+9]               
  2646: GCP      data[2602]            ; = 1
  2647: ADD                           
  2648: LADR     [sp+9]               
  2649: ASGN                          
  2650: SSP      1                    
  2651: SSP      1                    
  2652: JMP      label_2464           
label_2653:
  2653: LCP      [sp+10]              
  2654: LCP      [sp+10]              
  2655: GCP      data[2603]            ; = 1
  2656: ADD                           
  2657: LADR     [sp+10]              
  2658: ASGN                          
  2659: SSP      1                    
  2660: SSP      1                    
  2661: JMP      label_2445           
label_2662:
  2662: GCP      data[2604]            ; = 0.0f
  2663: GADR     data[0]              
  2664: ASGN                          
  2665: SSP      1                    
  2666: GCP      data[2605]            ; = 0.0f
  2667: LADR     [sp+8]               
  2668: ASGN                          
  2669: SSP      1                    
label_2670:
  2670: LCP      [sp+8]               
  2671: GCP      data[2606]            ; = 6
  2672: ULES                          
  2673: JZ       label_2698           
  2674: GADR     data[1]              
  2675: GCP      data[2607]            ; = 0.0f
  2676: ADD                           
  2677: LCP      [sp+8]               
  2678: GCP      data[2608]            ; = 4
  2679: MUL                           
  2680: ADD                           
  2681: DCP      4                    
  2682: JZ       label_2689           
  2683: LCP      [sp+8]               
  2684: GCP      data[2609]            ; = 1
  2685: ADD                           
  2686: GADR     data[0]              
  2687: ASGN                          
  2688: SSP      1                    
label_2689:
  2689: LCP      [sp+8]               
  2690: LCP      [sp+8]               
  2691: GCP      data[2610]            ; = 1
  2692: ADD                           
  2693: LADR     [sp+8]               
  2694: ASGN                          
  2695: SSP      1                    
  2696: SSP      1                    
  2697: JMP      label_2670           
label_2698:
  2698: GCP      data[2611]            ; = 0.0f
  2699: LADR     [sp+8]               
  2700: ASGN                          
  2701: SSP      1                    
label_2702:
  2702: LCP      [sp+8]               
  2703: GCP      data[0]              
  2704: ULES                          
  2705: JZ       label_2737           
  2706: GCP      data[2612]            ; = 3
  2707: GADR     data[2613]  ; "TurnTable recovers #%d: att:%d  def:%d"
  2708: LCP      [sp+8]               
  2709: GADR     data[1]              
  2710: GCP      data[2623]            ; = 0.0f
  2711: ADD                           
  2712: LCP      [sp+8]               
  2713: GCP      data[2624]            ; = 4
  2714: MUL                           
  2715: ADD                           
  2716: DCP      4                    
  2717: GADR     data[1]              
  2718: GCP      data[2625]            ; = 24
  2719: ADD                           
  2720: LCP      [sp+8]               
  2721: GCP      data[2626]            ; = 4
  2722: MUL                           
  2723: ADD                           
  2724: DCP      4                    
  2725: GCP      data[2627]            ; = 5
  2726: XCALL    $SC_Log(unsignedlong,*char,...)void ; args=4294967295
  2727: SSP      5                    
  2728: LCP      [sp+8]               
  2729: LCP      [sp+8]               
  2730: GCP      data[2628]            ; = 1
  2731: ADD                           
  2732: LADR     [sp+8]               
  2733: ASGN                          
  2734: SSP      1                    
  2735: SSP      1                    
  2736: JMP      label_2702           
label_2737:
  2737: GADR     data[1549]           
  2738: GCP      data[2629]            ; = 1536
  2739: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  2740: SSP      2                    
  2741: GCP      data[2630]            ; = 0.0f
  2742: LADR     [sp+8]               
  2743: ASGN                          
  2744: SSP      1                    
label_2745:
  2745: LCP      [sp+8]               
  2746: GCP      data[0]              
  2747: GCP      data[2631]            ; = 1
  2748: SUB                           
  2749: ULES                          
  2750: JZ       label_2788           
  2751: ASP      1                    
  2752: LADR     [sp+0]               
  2753: GADR     data[2632]  ; "TTS_%d"
  2754: LCP      [sp+8]               
  2755: ASP      1                    
  2756: GCP      data[2634]            ; = 3
  2757: XCALL    $sprintf(*char,*constchar,...)int ; args=4294967295
  2758: LLD      [sp+419]             
  2759: SSP      3                    
  2760: SSP      1                    
  2761: ASP      1                    
  2762: LADR     [sp+0]               
  2763: GADR     data[1933]           
  2764: LCP      [sp+8]               
  2765: GCP      data[2635]            ; = 16
  2766: MUL                           
  2767: ADD                           
  2768: ASP      1                    
  2769: XCALL    $SC_GetScriptHelper(*char,*s_sphere)int ; args=2
  2770: LLD      [sp+419]             
  2771: SSP      2                    
  2772: JZ       label_2774           
  2773: JMP      label_2779           
label_2774:
  2774: GADR     data[2636]  ; "helper %s not found"
  2775: LADR     [sp+0]               
  2776: GCP      data[2641]            ; = 2
  2777: XCALL    $SC_message(*char,...)void ; args=4294967295
  2778: SSP      2                    
label_2779:
  2779: LCP      [sp+8]               
  2780: LCP      [sp+8]               
  2781: GCP      data[2642]            ; = 1
  2782: ADD                           
  2783: LADR     [sp+8]               
  2784: ASGN                          
  2785: SSP      1                    
  2786: SSP      1                    
  2787: JMP      label_2745           
label_2788:
  2788: GCP      data[2643]            ; = 508
  2789: GCP      data[0]              
  2790: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  2791: SSP      2                    
label_2792:
  2792: JMP      label_3732           
  2793: JMP      label_2798           
label_2794:
  2794: LCP      [sp+418]             
  2795: GCP      data[2644]            ; = 2
  2796: EQU                           
  2797: JZ       label_3390           
label_2798:
  2798: GCP      data[2645]            ; = 0.0f
  2799: LADR     [sp+8]               
  2800: ASGN                          
  2801: SSP      1                    
  2802: GCP      data[2646]            ; = 0.0f
  2803: LADR     [sp+314]             
  2804: ASGN                          
  2805: SSP      1                    
  2806: GCP      data[2647]            ; = 0.0f
  2807: LADR     [sp+298]             
  2808: ASGN                          
  2809: SSP      1                    
  2810: ASP      1                    
  2811: GCP      data[2648]            ; = 502
  2812: ASP      1                    
  2813: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2814: LLD      [sp+419]             
  2815: SSP      1                    
  2816: LADR     [sp+10]              
  2817: ASGN                          
  2818: SSP      1                    
  2819: GCP      data[1964]           
  2820: ASP      1                    
  2821: GCP      data[2649]            ; = 503
  2822: ASP      1                    
  2823: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2824: LLD      [sp+420]             
  2825: SSP      1                    
  2826: NEQ                           
  2827: JZ       label_2867           
  2828: ASP      1                    
  2829: GCP      data[2650]            ; = 503
  2830: ASP      1                    
  2831: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2832: LLD      [sp+419]             
  2833: SSP      1                    
  2834: GADR     data[1964]           
  2835: ASGN                          
  2836: SSP      1                    
  2837: GCP      data[1964]           
  2838: JMP      label_2840           
  2839: JMP      label_2844           
label_2840:
  2840: LCP      [sp+419]             
  2841: GCP      data[2651]            ; = 2
  2842: EQU                           
  2843: JZ       label_2845           
label_2844:
  2844: JMP      label_2849           
label_2845:
  2845: LCP      [sp+419]             
  2846: GCP      data[2652]            ; = 3
  2847: EQU                           
  2848: JZ       label_2866           
label_2849:
  2849: ASP      1                    
  2850: GCP      data[2653]            ; = 509
  2851: ASP      1                    
  2852: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2853: LLD      [sp+420]             
  2854: SSP      1                    
  2855: GCP      data[2654]            ; = 0.0f
  2856: EQU                           
  2857: JZ       label_2862           
  2858: GCP      data[2655]            ; = 11117
  2859: XCALL    $SC_SND_PlaySound2D(unsignedlong)void ; args=1
  2860: SSP      1                    
  2861: JMP      label_2865           
label_2862:
  2862: GCP      data[2656]            ; = 11116
  2863: XCALL    $SC_SND_PlaySound2D(unsignedlong)void ; args=1
  2864: SSP      1                    
label_2865:
  2865: JMP      label_2866           
label_2866:
  2866: SSP      1                    
label_2867:
  2867: GCP      data[1964]           
  2868: JMP      label_2870           
  2869: JMP      label_2874           
label_2870:
  2870: LCP      [sp+419]             
  2871: GCP      data[2657]            ; = 0.0f
  2872: EQU                           
  2873: JZ       label_2893           
label_2874:
  2874: GCP      data[1980]           
  2875: GCP      data[2658]            ; = 0.0f
  2876: FLEQ                          
  2877: JZ       label_2887           
  2878: ASP      1                    
  2879: GCP      data[2659]            ; = 1076
  2880: ASP      1                    
  2881: XCALL    $SC_Wtxt(unsignedlong)*unsignedshort ; args=1
  2882: LLD      [sp+420]             
  2883: SSP      1                    
  2884: LADR     [sp+314]             
  2885: ASGN                          
  2886: SSP      1                    
label_2887:
  2887: GCP      data[2660]            ; = 0.0f
  2888: GADR     data[1979]           
  2889: ASGN                          
  2890: SSP      1                    
  2891: JMP      label_3345           
  2892: JMP      label_2897           
label_2893:
  2893: LCP      [sp+419]             
  2894: GCP      data[2661]            ; = 1
  2895: EQU                           
  2896: JZ       label_3139           
label_2897:
  2897: GCP      data[2662]            ; = 3.0f
  2898: GADR     data[1980]           
  2899: ASGN                          
  2900: SSP      1                    
  2901: GCP      data[1979]           
  2902: GCP      data[2663]            ; = 0.0f
  2903: FEQU                          
  2904: JZ       label_2909           
  2905: GCP      data[2664]            ; = 3.0f
  2906: GADR     data[1979]           
  2907: ASGN                          
  2908: SSP      1                    
label_2909:
  2909: GCP      data[1979]           
  2910: GCP      data[2665]            ; = 0.0f
  2911: FGRE                          
  2912: JZ       label_2969           
  2913: ASP      1                    
  2914: ASP      1                    
  2915: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  2916: LLD      [sp+420]             
  2917: LADR     [sp+8]               
  2918: ASGN                          
  2919: SSP      1                    
  2920: LCP      [sp+8]               
  2921: JZ       label_2968           
  2922: LCP      [sp+8]               
  2923: LADR     [sp+413]             
  2924: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  2925: SSP      2                    
  2926: LADR     [sp+413]             
  2927: PNT      8                    
  2928: DCP      4                    
  2929: ASP      1                    
  2930: ASP      1                    
  2931: GCP      data[2666]            ; = 502
  2932: ASP      1                    
  2933: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2934: LLD      [sp+422]             
  2935: SSP      1                    
  2936: ASP      1                    
  2937: CALL     func_0334            
  2938: LLD      [sp+421]             
  2939: SSP      1                    
  2940: EQU                           
  2941: JZ       label_2952           
  2942: ASP      1                    
  2943: GCP      data[2667]            ; = 5108
  2944: ASP      1                    
  2945: XCALL    $SC_Wtxt(unsignedlong)*unsignedshort ; args=1
  2946: LLD      [sp+420]             
  2947: SSP      1                    
  2948: LADR     [sp+314]             
  2949: ASGN                          
  2950: SSP      1                    
  2951: JMP      label_2961           
label_2952:
  2952: ASP      1                    
  2953: GCP      data[2668]            ; = 5109
  2954: ASP      1                    
  2955: XCALL    $SC_Wtxt(unsignedlong)*unsignedshort ; args=1
  2956: LLD      [sp+420]             
  2957: SSP      1                    
  2958: LADR     [sp+314]             
  2959: ASGN                          
  2960: SSP      1                    
label_2961:
  2961: LCP      [sp+314]             
  2962: XCALL    $SC_GameInfoW(*unsignedshort)void ; args=1
  2963: SSP      1                    
  2964: GCP      data[2669]            ; = 0.0f
  2965: LADR     [sp+314]             
  2966: ASGN                          
  2967: SSP      1                    
label_2968:
  2968: JMP      label_3137           
label_2969:
  2969: GCP      data[1978]           
  2970: GCP      data[2670]            ; = 0.0f
  2971: FGRE                          
  2972: JZ       label_3037           
  2973: GCP      data[1977]           
  2974: GCP      data[2671]            ; = 0.0f
  2975: UGRE                          
  2976: JZ       label_3037           
  2977: JMP      label_2978           
label_2978:
  2978: ASP      1                    
  2979: ASP      1                    
  2980: GCP      data[2672]            ; = 510
  2981: ASP      1                    
  2982: XCALL    $SC_ggi(unsignedlong)int ; args=1
  2983: LLD      [sp+421]             
  2984: SSP      1                    
  2985: ASP      1                    
  2986: XCALL    $SC_MP_GetPlofHandle(unsignedlong)unsignedlong ; args=1
  2987: LLD      [sp+420]             
  2988: SSP      1                    
  2989: LADR     [sp+9]               
  2990: ASGN                          
  2991: SSP      1                    
  2992: LCP      [sp+9]               
  2993: JZ       label_3008           
  2994: ASP      1                    
  2995: ASP      1                    
  2996: LCP      [sp+9]               
  2997: ASP      1                    
  2998: XCALL    $SC_P_GetName(unsignedlong)*char ; args=1
  2999: LLD      [sp+421]             
  3000: SSP      1                    
  3001: LADR     [sp+379]             
  3002: ASP      1                    
  3003: XCALL    $SC_AnsiToUni(*char,*unsignedshort)*unsignedshort ; args=2
  3004: LLD      [sp+420]             
  3005: SSP      2                    
  3006: SSP      1                    
  3007: JMP      label_3016           
label_3008:
  3008: ASP      1                    
  3009: GADR     data[2673]  ; "'disconnected'"
  3010: LADR     [sp+379]             
  3011: ASP      1                    
  3012: XCALL    $SC_AnsiToUni(*char,*unsignedshort)*unsignedshort ; args=2
  3013: LLD      [sp+420]             
  3014: SSP      2                    
  3015: SSP      1                    
label_3016:
  3016: ASP      1                    
  3017: LADR     [sp+315]             
  3018: ASP      1                    
  3019: GCP      data[2677]            ; = 5107
  3020: ASP      1                    
  3021: XCALL    $SC_Wtxt(unsignedlong)*unsignedshort ; args=1
  3022: LLD      [sp+422]             
  3023: SSP      1                    
  3024: LADR     [sp+379]             
  3025: GCP      data[1977]           
  3026: ASP      1                    
  3027: GCP      data[2678]            ; = 4
  3028: XCALL    $swprintf(*unsignedshort,*unsignedshort,...)int ; args=4294967295
  3029: LLD      [sp+420]             
  3030: SSP      4                    
  3031: SSP      1                    
  3032: LADR     [sp+315]             
  3033: LADR     [sp+314]             
  3034: ASGN                          
  3035: SSP      1                    
  3036: JMP      label_3137           
label_3037:
  3037: ASP      1                    
  3038: ASP      1                    
  3039: XCALL    $SC_PC_Get(void)unsignedlong ; args=0
  3040: LLD      [sp+420]             
  3041: LADR     [sp+8]               
  3042: ASGN                          
  3043: SSP      1                    
  3044: LCP      [sp+8]               
  3045: JZ       label_3137           
  3046: LCP      [sp+8]               
  3047: LADR     [sp+413]             
  3048: XCALL    $SC_P_GetInfo(unsignedlong,*s_SC_P_getinfo)void ; args=2
  3049: SSP      2                    
  3050: LADR     [sp+413]             
  3051: PNT      8                    
  3052: DCP      4                    
  3053: ASP      1                    
  3054: ASP      1                    
  3055: GCP      data[2679]            ; = 502
  3056: ASP      1                    
  3057: XCALL    $SC_ggi(unsignedlong)int ; args=1
  3058: LLD      [sp+422]             
  3059: SSP      1                    
  3060: ASP      1                    
  3061: CALL     func_0334            
  3062: LLD      [sp+421]             
  3063: SSP      1                    
  3064: EQU                           
  3065: JZ       label_3102           
  3066: GCP      data[1977]           
  3067: GCP      data[2680]            ; = 1
  3068: EQU                           
  3069: JZ       label_3080           
  3070: ASP      1                    
  3071: GCP      data[2681]            ; = 5111
  3072: ASP      1                    
  3073: XCALL    $SC_Wtxt(unsignedlong)*unsignedshort ; args=1
  3074: LLD      [sp+420]             
  3075: SSP      1                    
  3076: LADR     [sp+314]             
  3077: ASGN                          
  3078: SSP      1                    
  3079: JMP      label_3101           
label_3080:
  3080: ASP      1                    
  3081: LADR     [sp+315]             
  3082: ASP      1                    
  3083: GCP      data[2682]            ; = 5110
  3084: ASP      1                    
  3085: XCALL    $SC_Wtxt(unsignedlong)*unsignedshort ; args=1
  3086: LLD      [sp+422]             
  3087: SSP      1                    
  3088: GCP      data[1977]           
  3089: GCP      data[2683]            ; = 1
  3090: SUB                           
  3091: ASP      1                    
  3092: GCP      data[2684]            ; = 3
  3093: XCALL    $swprintf(*unsignedshort,*unsignedshort,...)int ; args=4294967295
  3094: LLD      [sp+420]             
  3095: SSP      3                    
  3096: SSP      1                    
  3097: LADR     [sp+315]             
  3098: LADR     [sp+314]             
  3099: ASGN                          
  3100: SSP      1                    
label_3101:
  3101: JMP      label_3137           
label_3102:
  3102: GCP      data[1977]           
  3103: GCP      data[2685]            ; = 1
  3104: EQU                           
  3105: JZ       label_3116           
  3106: ASP      1                    
  3107: GCP      data[2686]            ; = 5113
  3108: ASP      1                    
  3109: XCALL    $SC_Wtxt(unsignedlong)*unsignedshort ; args=1
  3110: LLD      [sp+420]             
  3111: SSP      1                    
  3112: LADR     [sp+314]             
  3113: ASGN                          
  3114: SSP      1                    
  3115: JMP      label_3137           
label_3116:
  3116: ASP      1                    
  3117: LADR     [sp+315]             
  3118: ASP      1                    
  3119: GCP      data[2687]            ; = 5112
  3120: ASP      1                    
  3121: XCALL    $SC_Wtxt(unsignedlong)*unsignedshort ; args=1
  3122: LLD      [sp+422]             
  3123: SSP      1                    
  3124: GCP      data[1977]           
  3125: GCP      data[2688]            ; = 1
  3126: SUB                           
  3127: ASP      1                    
  3128: GCP      data[2689]            ; = 3
  3129: XCALL    $swprintf(*unsignedshort,*unsignedshort,...)int ; args=4294967295
  3130: LLD      [sp+420]             
  3131: SSP      3                    
  3132: SSP      1                    
  3133: LADR     [sp+315]             
  3134: LADR     [sp+314]             
  3135: ASGN                          
  3136: SSP      1                    
label_3137:
  3137: JMP      label_3345           
  3138: JMP      label_3143           
label_3139:
  3139: LCP      [sp+419]             
  3140: GCP      data[2690]            ; = 2
  3141: EQU                           
  3142: JZ       label_3251           
label_3143:
  3143: ASP      1                    
  3144: ASP      1                    
  3145: GCP      data[2691]            ; = 510
  3146: ASP      1                    
  3147: XCALL    $SC_ggi(unsignedlong)int ; args=1
  3148: LLD      [sp+421]             
  3149: SSP      1                    
  3150: ASP      1                    
  3151: XCALL    $SC_MP_GetPlofHandle(unsignedlong)unsignedlong ; args=1
  3152: LLD      [sp+420]             
  3153: SSP      1                    
  3154: LADR     [sp+9]               
  3155: ASGN                          
  3156: SSP      1                    
  3157: LCP      [sp+9]               
  3158: JZ       label_3173           
  3159: ASP      1                    
  3160: ASP      1                    
  3161: LCP      [sp+9]               
  3162: ASP      1                    
  3163: XCALL    $SC_P_GetName(unsignedlong)*char ; args=1
  3164: LLD      [sp+421]             
  3165: SSP      1                    
  3166: LADR     [sp+379]             
  3167: ASP      1                    
  3168: XCALL    $SC_AnsiToUni(*char,*unsignedshort)*unsignedshort ; args=2
  3169: LLD      [sp+420]             
  3170: SSP      2                    
  3171: SSP      1                    
  3172: JMP      label_3181           
label_3173:
  3173: ASP      1                    
  3174: GADR     data[2692]  ; "'disconnected'"
  3175: LADR     [sp+379]             
  3176: ASP      1                    
  3177: XCALL    $SC_AnsiToUni(*char,*unsignedshort)*unsignedshort ; args=2
  3178: LLD      [sp+420]             
  3179: SSP      2                    
  3180: SSP      1                    
label_3181:
  3181: LCP      [sp+10]              
  3182: GCP      data[2696]            ; = 4
  3183: MOD                           
  3184: JMP      label_3186           
  3185: JMP      label_3190           
label_3186:
  3186: LCP      [sp+420]             
  3187: GCP      data[2697]            ; = 0.0f
  3188: EQU                           
  3189: JZ       label_3196           
label_3190:
  3190: GCP      data[2698]            ; = 5101
  3191: LADR     [sp+8]               
  3192: ASGN                          
  3193: SSP      1                    
  3194: JMP      label_3225           
  3195: JMP      label_3200           
label_3196:
  3196: LCP      [sp+420]             
  3197: GCP      data[2699]            ; = 1
  3198: EQU                           
  3199: JZ       label_3206           
label_3200:
  3200: GCP      data[2700]            ; = 5103
  3201: LADR     [sp+8]               
  3202: ASGN                          
  3203: SSP      1                    
  3204: JMP      label_3225           
  3205: JMP      label_3210           
label_3206:
  3206: LCP      [sp+420]             
  3207: GCP      data[2701]            ; = 2
  3208: EQU                           
  3209: JZ       label_3216           
label_3210:
  3210: GCP      data[2702]            ; = 5102
  3211: LADR     [sp+8]               
  3212: ASGN                          
  3213: SSP      1                    
  3214: JMP      label_3225           
  3215: JMP      label_3220           
label_3216:
  3216: LCP      [sp+420]             
  3217: GCP      data[2703]            ; = 3
  3218: EQU                           
  3219: JZ       label_3225           
label_3220:
  3220: GCP      data[2704]            ; = 5104
  3221: LADR     [sp+8]               
  3222: ASGN                          
  3223: SSP      1                    
  3224: JMP      label_3225           
label_3225:
  3225: SSP      1                    
  3226: ASP      1                    
  3227: LADR     [sp+315]             
  3228: ASP      1                    
  3229: LCP      [sp+8]               
  3230: ASP      1                    
  3231: XCALL    $SC_Wtxt(unsignedlong)*unsignedshort ; args=1
  3232: LLD      [sp+422]             
  3233: SSP      1                    
  3234: LADR     [sp+379]             
  3235: ASP      1                    
  3236: GCP      data[2705]            ; = 3
  3237: XCALL    $swprintf(*unsignedshort,*unsignedshort,...)int ; args=4294967295
  3238: LLD      [sp+420]             
  3239: SSP      3                    
  3240: SSP      1                    
  3241: LADR     [sp+315]             
  3242: LADR     [sp+314]             
  3243: ASGN                          
  3244: SSP      1                    
  3245: GCP      data[2706]            ; = 0.0f
  3246: GADR     data[1979]           
  3247: ASGN                          
  3248: SSP      1                    
  3249: JMP      label_3345           
  3250: JMP      label_3255           
label_3251:
  3251: LCP      [sp+419]             
  3252: GCP      data[2707]            ; = 3
  3253: EQU                           
  3254: JZ       label_3345           
label_3255:
  3255: ASP      1                    
  3256: ASP      1                    
  3257: GCP      data[2708]            ; = 510
  3258: ASP      1                    
  3259: XCALL    $SC_ggi(unsignedlong)int ; args=1
  3260: LLD      [sp+421]             
  3261: SSP      1                    
  3262: ASP      1                    
  3263: XCALL    $SC_MP_GetPlofHandle(unsignedlong)unsignedlong ; args=1
  3264: LLD      [sp+420]             
  3265: SSP      1                    
  3266: LADR     [sp+9]               
  3267: ASGN                          
  3268: SSP      1                    
  3269: LCP      [sp+9]               
  3270: JZ       label_3285           
  3271: ASP      1                    
  3272: ASP      1                    
  3273: LCP      [sp+9]               
  3274: ASP      1                    
  3275: XCALL    $SC_P_GetName(unsignedlong)*char ; args=1
  3276: LLD      [sp+421]             
  3277: SSP      1                    
  3278: LADR     [sp+379]             
  3279: ASP      1                    
  3280: XCALL    $SC_AnsiToUni(*char,*unsignedshort)*unsignedshort ; args=2
  3281: LLD      [sp+420]             
  3282: SSP      2                    
  3283: SSP      1                    
  3284: JMP      label_3293           
label_3285:
  3285: ASP      1                    
  3286: GADR     data[2709]  ; "'disconnected'"
  3287: LADR     [sp+379]             
  3288: ASP      1                    
  3289: XCALL    $SC_AnsiToUni(*char,*unsignedshort)*unsignedshort ; args=2
  3290: LLD      [sp+420]             
  3291: SSP      2                    
  3292: SSP      1                    
label_3293:
  3293: ASP      1                    
  3294: GCP      data[2713]            ; = 506
  3295: ASP      1                    
  3296: XCALL    $SC_ggi(unsignedlong)int ; args=1
  3297: LLD      [sp+420]             
  3298: SSP      1                    
  3299: JMP      label_3301           
  3300: JMP      label_3305           
label_3301:
  3301: LCP      [sp+420]             
  3302: GCP      data[2714]            ; = 0.0f
  3303: EQU                           
  3304: JZ       label_3311           
label_3305:
  3305: GCP      data[2715]            ; = 5105
  3306: LADR     [sp+8]               
  3307: ASGN                          
  3308: SSP      1                    
  3309: JMP      label_3320           
  3310: JMP      label_3315           
label_3311:
  3311: LCP      [sp+420]             
  3312: GCP      data[2716]            ; = 1
  3313: EQU                           
  3314: JZ       label_3320           
label_3315:
  3315: GCP      data[2717]            ; = 5106
  3316: LADR     [sp+8]               
  3317: ASGN                          
  3318: SSP      1                    
  3319: JMP      label_3320           
label_3320:
  3320: SSP      1                    
  3321: ASP      1                    
  3322: LADR     [sp+315]             
  3323: ASP      1                    
  3324: LCP      [sp+8]               
  3325: ASP      1                    
  3326: XCALL    $SC_Wtxt(unsignedlong)*unsignedshort ; args=1
  3327: LLD      [sp+422]             
  3328: SSP      1                    
  3329: LADR     [sp+379]             
  3330: ASP      1                    
  3331: GCP      data[2718]            ; = 3
  3332: XCALL    $swprintf(*unsignedshort,*unsignedshort,...)int ; args=4294967295
  3333: LLD      [sp+420]             
  3334: SSP      3                    
  3335: SSP      1                    
  3336: LADR     [sp+315]             
  3337: LADR     [sp+314]             
  3338: ASGN                          
  3339: SSP      1                    
  3340: GCP      data[2719]            ; = 0.0f
  3341: GADR     data[1979]           
  3342: ASGN                          
  3343: SSP      1                    
  3344: JMP      label_3345           
label_3345:
  3345: SSP      1                    
  3346: LCP      [sp+314]             
  3347: JZ       label_3388           
  3348: LADR     [sp+411]             
  3349: LADR     [sp+412]             
  3350: XCALL    $SC_GetScreenRes(*float,*float)void ; args=2
  3351: SSP      2                    
  3352: LCP      [sp+411]             
  3353: ASP      1                    
  3354: LCP      [sp+314]             
  3355: GCP      data[2720]            ; = 1.0f
  3356: ASP      1                    
  3357: XCALL    $SC_Fnt_GetWidthW(*unsignedshort,float)float ; args=2
  3358: LLD      [sp+420]             
  3359: SSP      2                    
  3360: FSUB                          
  3361: LADR     [sp+411]             
  3362: ASGN                          
  3363: SSP      1                    
  3364: LCP      [sp+298]             
  3365: JZ       label_3375           
  3366: GCP      data[2721]            ; = 0.5f
  3367: LCP      [sp+412]             
  3368: FMUL                          
  3369: GCP      data[2722]            ; = 40.0f
  3370: FSUB                          
  3371: LADR     [sp+412]             
  3372: ASGN                          
  3373: SSP      1                    
  3374: JMP      label_3379           
label_3375:
  3375: GCP      data[2723]            ; = 15.0f
  3376: LADR     [sp+412]             
  3377: ASGN                          
  3378: SSP      1                    
label_3379:
  3379: LCP      [sp+411]             
  3380: GCP      data[2724]            ; = 0.5f
  3381: FMUL                          
  3382: LCP      [sp+412]             
  3383: LCP      [sp+314]             
  3384: GCP      data[2725]            ; = 1.0f
  3385: GCP      data[2726]            ; = -1
  3386: XCALL    $SC_Fnt_WriteW(float,float,*unsignedshort,float,unsignedlong)void ; args=5
  3387: SSP      5                    
label_3388:
  3388: JMP      label_3732           
  3389: JMP      label_3394           
label_3390:
  3390: LCP      [sp+418]             
  3391: GCP      data[2727]            ; = 5
  3392: EQU                           
  3393: JZ       label_3518           
label_3394:
  3394: LADR     [sp-4]               
  3395: DADR     8                    
  3396: DCP      4                    
  3397: JZ       label_3404           
  3398: GCP      data[2728]            ; = 0.1f
  3399: LADR     [sp-4]               
  3400: DADR     20                   
  3401: ASGN                          
  3402: SSP      1                    
  3403: JMP      label_3516           
label_3404:
  3404: GCP      data[1968]           
  3405: JMP      label_3407           
  3406: JMP      label_3411           
label_3407:
  3407: LCP      [sp+419]             
  3408: GCP      data[2729]            ; = 1
  3409: EQU                           
  3410: JZ       label_3496           
label_3411:
  3411: GCP      data[2730]            ; = 0.0f
  3412: LADR     [sp+8]               
  3413: ASGN                          
  3414: SSP      1                    
label_3415:
  3415: LCP      [sp+8]               
  3416: GCP      data[2020]           
  3417: ULES                          
  3418: JZ       label_3461           
  3419: LADR     [sp-4]               
  3420: DADR     4                    
  3421: DCP      4                    
  3422: GADR     data[2021]           
  3423: LCP      [sp+8]               
  3424: GCP      data[2731]            ; = 4
  3425: MUL                           
  3426: ADD                           
  3427: DCP      4                    
  3428: EQU                           
  3429: JZ       label_3452           
  3430: GCP      data[2020]           
  3431: GCP      data[2020]           
  3432: GCP      data[2732]            ; = 1
  3433: SUB                           
  3434: GADR     data[2020]           
  3435: ASGN                          
  3436: SSP      1                    
  3437: SSP      1                    
  3438: GADR     data[2021]           
  3439: GCP      data[2020]           
  3440: GCP      data[2733]            ; = 4
  3441: MUL                           
  3442: ADD                           
  3443: DCP      4                    
  3444: GADR     data[2021]           
  3445: LCP      [sp+8]               
  3446: GCP      data[2734]            ; = 4
  3447: MUL                           
  3448: ADD                           
  3449: ASGN                          
  3450: SSP      1                    
  3451: JMP      label_3461           
label_3452:
  3452: LCP      [sp+8]               
  3453: LCP      [sp+8]               
  3454: GCP      data[2735]            ; = 1
  3455: ADD                           
  3456: LADR     [sp+8]               
  3457: ASGN                          
  3458: SSP      1                    
  3459: SSP      1                    
  3460: JMP      label_3415           
label_3461:
  3461: LCP      [sp+8]               
  3462: GCP      data[2020]           
  3463: ULES                          
  3464: JZ       label_3471           
  3465: GCP      data[2736]            ; = 0.1f
  3466: LADR     [sp-4]               
  3467: DADR     20                   
  3468: ASGN                          
  3469: SSP      1                    
  3470: JMP      label_3494           
label_3471:
  3471: GCP      data[1983]           
  3472: ASP      1                    
  3473: ASP      1                    
  3474: CALL     func_0155            
  3475: LLD      [sp+421]             
  3476: FGRE                          
  3477: JZ       label_3484           
  3478: GCP      data[1983]           
  3479: LADR     [sp-4]               
  3480: DADR     20                   
  3481: ASGN                          
  3482: SSP      1                    
  3483: JMP      label_3494           
label_3484:
  3484: GCP      data[1983]           
  3485: ASP      1                    
  3486: ASP      1                    
  3487: CALL     func_0119            
  3488: LLD      [sp+421]             
  3489: FADD                          
  3490: LADR     [sp-4]               
  3491: DADR     20                   
  3492: ASGN                          
  3493: SSP      1                    
label_3494:
  3494: JMP      label_3515           
  3495: JMP      label_3500           
label_3496:
  3496: LCP      [sp+419]             
  3497: GCP      data[2737]            ; = 0.0f
  3498: EQU                           
  3499: JZ       label_3514           
label_3500:
  3500: GCP      data[2738]            ; = 3.0f
  3501: LADR     [sp-4]               
  3502: DADR     20                   
  3503: ASGN                          
  3504: SSP      1                    
  3505: JMP      label_3515           
  3506: JMP      label_3507           
label_3507:
  3507: GCP      data[2739]            ; = -1.0f
  3508: LADR     [sp-4]               
  3509: DADR     20                   
  3510: ASGN                          
  3511: SSP      1                    
  3512: JMP      label_3515           
  3513: JMP      label_3515           
label_3514:
  3514: JMP      label_3507           
label_3515:
  3515: SSP      1                    
label_3516:
  3516: JMP      label_3732           
  3517: JMP      label_3522           
label_3518:
  3518: LCP      [sp+418]             
  3519: GCP      data[2740]            ; = 6
  3520: EQU                           
  3521: JZ       label_3663           
label_3522:
  3522: LADR     [sp-4]               
  3523: DADR     8                    
  3524: DCP      4                    
  3525: LADR     [sp+13]              
  3526: ASGN                          
  3527: SSP      1                    
  3528: LADR     [sp-4]               
  3529: DADR     4                    
  3530: DCP      4                    
  3531: LADR     [sp+9]               
  3532: ASGN                          
  3533: SSP      1                    
  3534: GCP      data[1966]           
  3535: JZ       label_3542           
  3536: GCP      data[2741]            ; = 1
  3537: LCP      [sp+9]               
  3538: SUB                           
  3539: LADR     [sp+9]               
  3540: ASGN                          
  3541: SSP      1                    
label_3542:
  3542: LCP      [sp+9]               
  3543: JZ       label_3576           
  3544: GCP      data[1968]           
  3545: GCP      data[2742]            ; = 1
  3546: EQU                           
  3547: JZ       label_3571           
  3548: GCP      data[1967]           
  3549: GCP      data[2743]            ; = 2
  3550: ULES                          
  3551: JZ       label_3557           
  3552: GCP      data[2744]            ; = 0.0f
  3553: LADR     [sp+10]              
  3554: ASGN                          
  3555: SSP      1                    
  3556: JMP      label_3570           
label_3557:
  3557: GCP      data[1967]           
  3558: GCP      data[2745]            ; = 1
  3559: SUB                           
  3560: ASP      1                    
  3561: ASP      1                    
  3562: XCALL    $rand(void)int        ; args=0
  3563: LLD      [sp+420]             
  3564: GCP      data[2746]            ; = 2
  3565: MOD                           
  3566: SUB                           
  3567: LADR     [sp+10]              
  3568: ASGN                          
  3569: SSP      1                    
label_3570:
  3570: JMP      label_3575           
label_3571:
  3571: GCP      data[2747]            ; = 0.0f
  3572: LADR     [sp+10]              
  3573: ASGN                          
  3574: SSP      1                    
label_3575:
  3575: JMP      label_3591           
label_3576:
  3576: GCP      data[1968]           
  3577: GCP      data[2748]            ; = 1
  3578: EQU                           
  3579: JZ       label_3585           
  3580: GCP      data[1967]           
  3581: LADR     [sp+10]              
  3582: ASGN                          
  3583: SSP      1                    
  3584: JMP      label_3591           
label_3585:
  3585: GCP      data[0]              
  3586: GCP      data[2749]            ; = 1
  3587: SUB                           
  3588: LADR     [sp+10]              
  3589: ASGN                          
  3590: SSP      1                    
label_3591:
  3591: ASP      1                    
  3592: GADR     data[13]             
  3593: LCP      [sp+9]               
  3594: GCP      data[2750]            ; = 3072
  3595: MUL                           
  3596: ADD                           
  3597: LCP      [sp+10]              
  3598: GCP      data[2751]            ; = 512
  3599: MUL                           
  3600: ADD                           
  3601: GADR     data[1]              
  3602: LCP      [sp+9]               
  3603: GCP      data[2752]            ; = 24
  3604: MUL                           
  3605: ADD                           
  3606: LCP      [sp+10]              
  3607: GCP      data[2753]            ; = 4
  3608: MUL                           
  3609: ADD                           
  3610: DCP      4                    
  3611: GADR     data[1549]           
  3612: LCP      [sp+9]               
  3613: GCP      data[2754]            ; = 768
  3614: MUL                           
  3615: ADD                           
  3616: LCP      [sp+10]              
  3617: GCP      data[2755]            ; = 128
  3618: MUL                           
  3619: ADD                           
  3620: GCP      data[2756]            ; = 3.0f
  3621: ASP      1                    
  3622: XCALL    $SC_MP_SRV_GetBestDMrecov(*s_SC_MP_Recover,unsignedlong,*float,float)unsignedlong ; args=4
  3623: LLD      [sp+419]             
  3624: SSP      4                    
  3625: LADR     [sp+8]               
  3626: ASGN                          
  3627: SSP      1                    
  3628: GCP      data[2757]            ; = 3.0f
  3629: GADR     data[1549]           
  3630: LCP      [sp+9]               
  3631: GCP      data[2758]            ; = 768
  3632: MUL                           
  3633: ADD                           
  3634: LCP      [sp+10]              
  3635: GCP      data[2759]            ; = 128
  3636: MUL                           
  3637: ADD                           
  3638: LCP      [sp+8]               
  3639: GCP      data[2760]            ; = 4
  3640: MUL                           
  3641: ADD                           
  3642: ASGN                          
  3643: SSP      1                    
  3644: GADR     data[13]             
  3645: LCP      [sp+9]               
  3646: GCP      data[2761]            ; = 3072
  3647: MUL                           
  3648: ADD                           
  3649: LCP      [sp+10]              
  3650: GCP      data[2762]            ; = 512
  3651: MUL                           
  3652: ADD                           
  3653: LCP      [sp+8]               
  3654: GCP      data[2763]            ; = 16
  3655: MUL                           
  3656: ADD                           
  3657: DCP      16                   
  3658: LCP      [sp+13]              
  3659: ASGN                          
  3660: SSP      4                    
  3661: JMP      label_3732           
  3662: JMP      label_3667           
label_3663:
  3663: LCP      [sp+418]             
  3664: GCP      data[2764]            ; = 10
  3665: EQU                           
  3666: JZ       label_3700           
label_3667:
  3667: GCP      data[2765]            ; = 0.0f
  3668: GADR     data[1959]           
  3669: ASGN                          
  3670: SSP      1                    
  3671: GADR     data[1960]           
  3672: GCP      data[2766]            ; = 8
  3673: XCALL    $SC_ZeroMem(*void,unsignedlong)void ; args=2
  3674: SSP      2                    
  3675: CALL     func_0249            
  3676: GCP      data[2767]            ; = 1
  3677: XCALL    $SC_MP_SetInstantRecovery(int)void ; args=1
  3678: SSP      1                    
  3679: GCP      data[1968]           
  3680: GCP      data[2768]            ; = 0.0f
  3681: NEQ                           
  3682: JZ       label_3693           
  3683: XCALL    $SC_MP_RestartMission(void)void ; args=0
  3684: XCALL    $SC_MP_RecoverAllNoAiPlayers(void)void ; args=0
  3685: GCP      data[2769]            ; = 0.0f
  3686: GADR     data[1968]           
  3687: ASGN                          
  3688: SSP      1                    
  3689: GCP      data[2770]            ; = 503
  3690: GCP      data[1968]           
  3691: XCALL    $SC_sgi(unsignedlong,int)void ; args=2
  3692: SSP      2                    
label_3693:
  3693: GCP      data[2771]            ; = 0.0f
  3694: GADR     data[1978]           
  3695: ASGN                          
  3696: SSP      1                    
  3697: XCALL    $SC_MP_SRV_ClearPlsStats(void)void ; args=0
  3698: JMP      label_3732           
  3699: JMP      label_3704           
label_3700:
  3700: LCP      [sp+418]             
  3701: GCP      data[2772]            ; = 11
  3702: EQU                           
  3703: JZ       label_3722           
label_3704:
  3704: LADR     [sp-4]               
  3705: DADR     4                    
  3706: DCP      4                    
  3707: GADR     data[1957]           
  3708: ASGN                          
  3709: SSP      1                    
  3710: LADR     [sp-4]               
  3711: DADR     8                    
  3712: DCP      4                    
  3713: GADR     data[1958]           
  3714: ASGN                          
  3715: SSP      1                    
  3716: GCP      data[2773]            ; = 0.0f
  3717: GADR     data[1959]           
  3718: ASGN                          
  3719: SSP      1                    
  3720: JMP      label_3732           
  3721: JMP      label_3726           
label_3722:
  3722: LCP      [sp+418]             
  3723: GCP      data[2774]            ; = 7
  3724: EQU                           
  3725: JZ       label_3732           
label_3726:
  3726: LADR     [sp-4]               
  3727: DADR     4                    
  3728: DCP      4                    
  3729: CALL     func_0752            
  3730: SSP      1                    
  3731: JMP      label_3732           
label_3732:
  3732: SSP      1                    
  3733: GCP      data[2775]            ; = 1
  3734: LLD      [sp-3]               
  3735: RET      418                  
