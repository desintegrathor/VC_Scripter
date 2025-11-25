/*
*	sc_def.h
*	Ptero-Engine-II : Global script definitions
*/



#ifndef SC_DEF_H
#define SC_DEF_H 

//messages to individual scripts, last 66
#define SCM_FEELDANGER							1
#define SCM_RUN									2
#define SCM_WARNABOUTENEMY							3
#define SCM_BOOBYTRAPFOUND							4
#define SCM_TAUNTRUNNER							5
#define SCM_CREATE								6
#define SCM_HEARDSOMETHING							7
#define SCM_SETGPHASE								8
#define SCM_ONWAYPOINT							9
#define SCM_DISABLE								10
#define SCM_ENABLE								11
#define SCM_TELEPORT								12
#define SCM_CONFIRM								14			//yes a bla bla bla....
#define SCM_TIMEDRUN								15
#define SCM_WALK								16
#define SCM_BATTLEWALK								17
#define SCM_BATTLERUN								22
#define SCM_RETREAT								23
#define SCM_PANICRUN								24
#define SCM_STARTWALK							25
#define SCM_CHECKBODY							26
#define SCM_GETBACK							27
#define SCM_HUNTER							28
#define SCM_RUNANDKILL							29
#define SCM_PLAYANIM							30
#define SCM_STARTPATROL							31
#define SCM_STARTMORTARFIRE						33
#define SCM_STARTASSAULT						34
#define SCM_WALK								35
#define SCM_RUNATWP								36
#define SCM_WALKATWP							37
#define SCM_SHOOTING							38
#define SCM_PATHWALK							39

#define	SCM_WPPATH_BEGIN						40
#define	SCM_WPPATH_CONTINUE						41
#define	SCM_WPPATH_END							42

#define SCM_RUNWITHMORTAR						43
#define SCM_SAPPERATTACK						44
#define SCM_SUPPORTSAPPER						46
#define SCM_EXITCAR							47		//or heli
#define SCM_CHANGETARGET						49
#define SCM_CAREFULLASSAULT						50
#define SCM_DONE							53		//player finished task, info->param2  - pl_id
#define SCM_ENTERCAR							54		//info->param2 - entryfunction
#define SCM_THROWSMOKE							55		//info->param2 - id of waypoint - "WayPointxxx"
#define SCM_KAMIKADZE							57		//starts kamikadze run
#define SCM_ENABLEINTERACTION						58		//info->param2 - Id of string shown to player
#define SCM_DISABLEINTERACTION						59
#define SCM_EXITHELI							62
#define SCM_RADIOCOM							63		//starts or ends radio communication - playing of anim
#define SCM_YOUARECOMMANDER						64
#define SCM_GROUPRETREAT						65
#define SCM_NEWCOMMANDER						66		//param2 is memberid of new group commander

#define	SCM_GOTO								70		//param2 = id specifying where to go
#define	SCM_CANUSEMAP							71		//param2 = id specifying which speech to say
#define	SCM_DO									72		//param2 - specifies what to do
#define	SCM_SETPHASE							73		//sets gPhase to param2
#define	SCM_HELIIN								74		//message to player's team - enter heli
#define	SCM_HELIOUT								75		//message to player's team - leave heli
#define	SCM_FIRE								76		//e.g. when we need mortar-team to work
#define	SCM_RECOVER								77		//ressurection of player, param2 - if FALSE, player is recovered immediately, otherwise he is not recovered until he is in player's view
#define	SCM_HELILOADED							78		//heli is full, all members in
#define	SCM_HELIEMPTY							79		//all players left heli
#define	SCM_INFO								80		//info player about param2

//level messages
#define SCM_REMOVE								13
#define SCM_INITTRAP								18
#define SCM_EXPLODETRAP								19
#define SCM_DISARMTRAP								20
#define SCM_TEAMKIA								21
#define SCM_MORTARLAND								32
#define SCM_EXPLOSIVEPLANTED							45
#define SCM_MORTARPLACED							48		//mortar infantry reports it's on the deignated place
#define SCM_OBJECTUSED								51		//info->param2 - master_nod of object
#define SCM_OBJECTDESTROYED							52		//info->param2 - master_nod of object
#define SCM_SMOKETHROWED							56		//info->param2 - player finished smokethrow
#define SCM_PLAYERINTERACTION							60		//info->param2 - id of interacted player 
#define SCM_TRAPACTIVATED							61		//info->param2 - id of hit player 

//multiplayer messages
#define	SCM_MP_REINIT								777		//used in cooperative for AI reinit




//global vars

#define SGI_MISSIONDEATHCOUNT							1			//stores count of death enemy in mission
#define SGI_MISSIONALARM								2			//is enemy alarmed?
#define SGI_TEAMDEATHCOUNT							3			//teammates deathcount (right now including wounded too)
#define SGI_ALLYDEATHCOUNT							4			//Allies deathcount
#define SGI_GROUPDEATHCOUNT							5			//deathcount of one specific important group
#define SGI_LEVELPHASE								6			//gphase of level.c
#define SGI_CHOPPER								7			//Chopper control
#define SGI_TEAMWIA								8			//teammates wounded
#define SGI_DIFFICULTY								10
#define SGI_GAMETYPE								11			//0 normal, 1 coop mutliplayer
#define SGI_C4COUNT								12			//for missions, where it's possible use C4 on multiple places		- usable only for singleplayer!!!!
#define SGF_C4TIMER								13			//timer to c4 explosion

#define SGI_INTELBASE								2000			//2000-2080 reserved for intel status in level
#define SGI_INTELCOUNT								2081			//number of intel in the game

#define SC_COMPLETEINTELCOUNT							80			//number of intel's in the game


// campaing mode

#define PLAYER_INTELSTART						50
#define PLAYER_INTELEND							59

#define PLAYER_AMMOSTART						60
#define PLAYER_AMMOLAST						89		//30 gv reserved for campaing mode - ammo
#define PLAYER_AMMOINGUN						90
#define PLAYER_AMMOINPISTOL						91

#define PLAYER_HEALTHSTART						95		//2 gv reserved for health status
#define PLAYER_HEALTHEND						96

#define PLAYER_WEAPON1							101
#define PLAYER_WEAPON2							102
#define PLAYER_WEAPON3							103
#define PLAYER_WEAPON4							104
#define PLAYER_WEAPON5							105
#define PLAYER_WEAPON6							106
#define PLAYER_WEAPON7							107
#define PLAYER_WEAPON8							108
#define PLAYER_WEAPON9							109
#define PLAYER_WEAPON10						110

#define PLAYER_FREESLOT							0xff			//player has nothing in this slot

//arrival - are doors to PC bunker unlocked???
#define SGI_ARRIVAL_UNLOCKED					130
#define SGI_ARRIVAL_HORNSTERSPECANI				131
//Medic Patrol setting  - is player driving the jeep?
#define SGI_MEDPATROL_DRIVING					140

#define SGI_TUNNELS_C4UNUSED					141



//craters in outpost
#define OUTPOSTCRATERBASE					150
#define OUTPOSTCRATER4						154
#define OUTPOSTCRATER5						155
#define OUTPOSTCRATER6						156
#define OUTPOSTCRATER7						157
#define OUTPOSTCRATER8						158
#define OUTPOSTCRATER9						159
#define OUTPOSTCRATER10						160
#define OUTPOSTCRATER11						161

#define SGI_CURRENTMISSION							200
#define SGF_MISSIONTIMER								201

// defines for Ricefields / Pilot
#define SGI_LEVPILOT_S1G0						1000
//#define SGI_LEVPILOT_S1G0C						1001
#define SGI_LEVPILOT_S1G1						1002
#define SGI_LEVPILOT_S1G2						1003
#define SGI_LEVPILOT_S1G3						1004
#define SGI_LEVPILOT_S1G4						1005
#define SGI_LEVPILOT_S1G5						1006

/*
#define SGI_LEVPILOT_WILL1						1010
#define SGI_LEVPILOT_WILL2						1011
#define SGI_LEVPILOT_WILL3						1012
#define SGI_LEVPILOT_WILL4						1013
*/

#define SGI_LEVPILOT_EVACVILLID					1020
#define SGI_LEVPILOT_HELI3_ATTACK				1021
#define SGI_LEVPILOT_JUSTLOADEDVALUE			1022

//defines for Big Valley Chopper flight
#define SGI_LEVBCHOPPER_SYNCHRO						1030

//defines for basecamp final
#define SGI_LEVBASE_GROUP0					1040
#define SGI_LEVBASE_GROUP1					1041
#define SGI_LEVBASE_GROUP2					1042

#define SGI_LEVBASE_CLAYOUT1					1050
#define SGI_LEVBASE_CLAYOUT2					1051
#define SGI_LEVBASE_CLAYOUT3					1052
#define SGI_LEVBASE_CLAYOUT4					1053
#define SGI_LEVBASE_CLAYIN1					1054
#define SGI_LEVBASE_CLAYIN2					1055
#define SGI_LEVBASE_CLAYIN3					1056
#define SGI_LEVBASE_CLAYIN4					1057

#define SGI_REWARD_MEDIC					3000
#define SGI_REWARD_3CANYONS					3001
#define SGI_REWARD_BASECAMP					3002
#define SGI_REWARD_FRENCHROUTE				3003
#define SGI_REWARD_NIGHT					3004
#define SGI_REWARD_AMBUSH					3005
#define SGI_REWARD_OUTPOST					3006
#define SGI_REWARD_CRASHFLIGHT				3007
#define SGI_REWARD_PILOT					3008
#define SGI_REWARD_STREAM					3009
#define SGI_REWARD_LASTBASECAMP				3010
// added by Erik
#define SGI_REWARD_RADIORELAY				3011
#define SGI_REWARD_BIGVALLEYCHOPPER			3012


#define SGI_MUSICRADIO_DEFCOMMENT_FIRST		4000
#define SGI_MUSICRADIO_DEFCOMMENT_LAST		4015
#define SGI_MUSICRADIO_MUSIC_FIRST			4020
#define SGI_MUSICRADIO_MUSIC_LAST			4049
#define SGI_MUSICRADIO_MAKESWITCHON			4050
#define SGF_MUSICRADIO_VOLUME				4051			// is used, when >0.0f

// values: 0 - nothing happens, 1 attack has started, 2 wire was destroyed, 3 fence was destroyed 4 bridge was laid


//++++++++++++++

//COMMON
#define	SGI_HELI01GO	2050
#define	SGI_ALARM01		2051

//countdown icons
#define	NUM_SGF_CNTDOWN		5				//up to 5 countdown timers
#define	_SGF_CNTDOWN_BASE	2060
#define	SGF_CNTDOWN00		2060			//placeholder
#define	SGF_CNTDOWN01		2061			//placeholder
#define	SGF_CNTDOWN02		2062			//placeholder
#define	SGF_CNTDOWN03		2063			//placeholder
#define	SGF_CNTDOWN04		2064			//placeholder



//Ambush
#define	SGI_DOLOOP		2234			//informs heli that should do loop
#define	SGI_HELIAMP		2235			//heli loudspeaker
#define	SGI_BIGGROUP01	2001
#define	SGI_HELIFORSURR	2002
#define	SGI_HFSLANDED	2003
#define	SGI_HFS_GOAWAY	2004
#define	SGI_AM_HELI1xGO	2005

//Night B
#define	SGI_GO_NOSIC	2000
//#define	SGI_HELI01GO	2001
#define	SGI_EVERYIN		2002
#define	SGI_ENTERHELI	2003
#define	SGI_OUTOFHELI	2004
#define	SGI_CHAJDAIN	2005
//#define	SGI_ALARM01		2006

//Night A (Papa Oscar Whiskey)
//#define	SGI_ALARM01		2001			//ve vesnici
//#define	SGI_HELI01GO	2004
#define	SGI_PRISFREE	2007
#define	SGI_HWIZD		2008
#define	SGI_BRONSONOK	2009
#define	SGI_CURKECGROUP	2021
#define	SGI_CURKEC		2022
#define	SGI_CURPLAYER	2023
#define	SGI_BOMBALARM	2024
#define	SGI_IGNORE_LSC	2025
#define	SGI_LSC			2026
#define	SGI_HLIDACALARM	2027
#define	SGI_BRONSN_R	2030		//ready to action?
#define	SGI_DEFORT_R	2031
#define	SGI_HORNST_R	2032
#define	SGI_NAPALM		2033
#define	SGI_NHUTCOOP	2034
#define	SGI_HELIFULL	2035		//when SCM_HELILOADED recevied
#define	SGI_KILLMARV	2036

//NVA base
#define	SGI_USPRISONER	2000
#define	SGI_FOUNDEXIT	2001
#define	SGI_CANTALK		2002
#define	SGI_CAMANIM01	2003
#define	SGI_CAMANIMEND01 2004
#define	SGI_AADESTR1	2005
#define	SGI_AADESTR2	2006
#define	SGI_NVA_HELI1xGO	2007
#define	SGI_NVA_FANTOM1xGO	2008

//3 canyons B
//#define	SGI_ALARM01		2001			//granat na lavce
#define	SGI_CB_HELI1xGO	2002

//RadioRelay
#define	SGI_HELIATEND	2000			//if TRUE, Heli01 goes for US_0
#define	SGI_MINDEAD		2001			//when minometcici are dead, set to TRUE
#define	SGI_USEFLARES	2002
#define	SGI_SOUMRAK		2003			//uz se setmelo?
#define	SGI_SENDATTDONE	2004			//if TRUE, vc_wps can send SCM_ATTACKDONE

//Basecamp Night
#define	SGI_BYTHEAMMO	2000
#define	SGI_BRONSONINT	2001
#define	SGI_DOORSOUT	2002
#define	SGI_UROSENPOLE	2003
#define	SGF_USKECTMR	2005			///
#define	SGI_VYRESAMMO	2004			//see Rosenfield.c
#define	SGI_ROZAKEC		2006
#define	SGI_NOKILLER	2007
#define	SGI_C4PLANTED	2008
#define	SGI_SEZAM		2009
#define	SGI_RAKETKA		2010

//Escape
//#define	SGI_ALARM01		2001			//ve vesnici
#define	SGI_ALARM02		2002
#define	SGI_ALARM03		2003
//#define	SGI_HELI01GO	2004
#define	SGI_MISSIONOK	2005
#define	SGI_NUM_VC2_DEAD 2006
#define	SGI_JETOMAGOR	2007
#define	SGF_SAYSOMETHING 2008
#define	SGI_CANSAY		2009




//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++  Datadisc defines  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Common
#define	SGI_PHASE		2222

//BomberPilot
#define	SGI_G01_ACT		2001		//guard groups
#define	SGI_G02_ACT		2002
#define	SGI_G03_ACT		2003
#define	SGI_G04_ACT		2004
#define	SGI_G05_ACT		2005

#define	SGI_ALP_01		2006		//Activation Lines Passed
#define	SGI_ALP_11		2007
#define	SGI_ALP_02		2008
#define	SGI_ALP_12		2009
#define	SGI_ALP_22		2009
#define	SGI_ALP_03		2010

#define	SGI_BP_ALARM01	2011
#define	SGI_BP_ALARM02	2012
#define	SGI_BP_ALARM03	2013
#define	SGI_BP_ALARM04	2014
#define	SGI_BP_ALARM05	2015

#define	SGI_PILOTWAKE	2020
#define	SGI_PILOTFOUND	2021
#define	SGI_PILOTPOS	2022
#define	SGI_PILOTSTATE	2023
#define	SGI_C4_PLANTED	2024
#define	SGI_R2_STATUS	2025
#define	SGI_RADIO_LZ	2026
#define	SGI_BOXCOMMENT	2027
#define	SGI_VC4_TALKING	2028
#define	SGI_HIDEITEMS	2029
#define	SGI_USEDLZ		2030
#define	SGI_CROCKERE	2031



//DEATHVALLEY
#define	SGI_DV_BOMB1	2200
#define	SGI_DV_BOMB2	2201
#define	SGI_DV_ALARMER	2202
#define 	SGF_DV_ALARMX	2203
#define 	SGF_DV_ALARMY	2204
#define 	SGF_DV_ALARMZ	2205
//JARAI
#define	SGI_JARAI_TREE	2210




//BaseAttack
#define	SGI_MIN01		2001
#define	SGI_MIN02		2002
#define	SGI_MIN03		2003
#define	SGI_VC0_PHASE	2004
#define	SGI_DONTSHOOT	2005
#define	SGI_DESTROY_TER	2006

//MineFucktory
#define	SGI_MF_HELIGO	2001
#define	SGI_GRENUSED	2002
#define	SGI_NUM_C4		2003
#define	SGI_INTELFOUND	2004
#define	SGI_TEAM2LEFT	2005
#define	SGI_ACT_VC5		2006
#define	SGI_ACTIVATE_VC	2007
#define	SGI_TESTGREN	2008
#define	SGI_CLOSEDOORS	2009
#define	SGI_INTRO		2010
#define	SGI_DOORSDSTR	2011
#define	SGI_UNDERFUCKIT	2012


//---------------------------------------------------------  Datadisc defines  -------------------------------------------------------------

// +++ Fist Alpha Coop +++
#define	SGI_A2_PASS		3333			//player(s) pased line dmPassA-dmPassB
// --- Fist Alpha Coop ---









//++ Unipage debriefing control values
#define	SGI_DEBR_01		3501
#define	SGI_DEBR_02		3502
#define	SGI_DEBR_03		3503
#define	SGI_DEBR_04		3504
#define	SGI_DEBR_05		3505
#define	SGI_DEBR_06		3506
#define	SGI_DEBR_07		3507
#define	SGI_DEBR_08		3508
#define	SGI_DEBR_09		3509

#define	DEBR_DONTSHOW	0xFFFFFFFF
//--

//++

//status-saving variables
//alc save
#define	SGI_ALC_SAVE_DOC		3600
#define	SGI_ALC_SAVE_PAGE		3601
//brief save
#define	SGI_BRIEF_SAVE_DOC		3602
#define	SGI_BRIEF_SAVE_PAGE		3603
//diary save
#define	SGI_DIARY_SAVE_DOC		3604
#define	SGI_DIARY_SAVE_PAGE		3605

//--

//special handler of Play btn in Briefing
#define	SGI_RV_BRIEF			3610


//DEBRIEFING INFORMATIONS

//WARNING!!!!! - zero result means show the text, use 1 to disable debrief text
// now it uses SGI_DEBR_0x values

#define SGI_DEBRIEF_MEDIC_VARA				SGI_DEBR_01
#define SGI_DEBRIEF_MEDIC_VARB				SGI_DEBR_02
#define SGI_DEBRIEF_MEDIC_VARC				SGI_DEBR_03

#define SGI_DEBRIEF_3CANYON_NOCACHE			SGI_DEBR_02
#define SGI_DEBRIEF_3CANYON_SOMECACHE			SGI_DEBR_01
#define SGI_DEBRIEF_3CANYON_WOUNDEDFOUND		SGI_DEBR_03
#define SGI_DEBRIEF_3CANYON_WOUNDEDNOTFOUND		SGI_DEBR_04
#define SGI_DEBRIEF_3CANYON_REWARDED			SGI_DEBR_05
#define SGI_DEBRIEF_BASECAMP_REWARDED		SGI_DEBR_01
#define SGI_DEBRIEF_FRENCHROUTE_REWARDED		SGI_DEBR_01
#define SGI_DEBRIEF_NIGHT_REWARDED			SGI_DEBR_01
#define SGI_DEBRIEF_AMBUSH_REWARDED			SGI_DEBR_01
#define SGI_DEBRIEF_OUTPOST_REWARDED			SGI_DEBR_01
#define SGI_DEBRIEF_RELAY_REWARDED			SGI_DEBR_01
#define SGI_DEBRIEF_NVA_MAPSFOUND			SGI_DEBR_01
#define SGI_DEBRIEF_NVA_REWARDED			SGI_DEBR_02
#define SGI_DEBRIEF_PILOT_REWARDED			SGI_DEBR_01
#define SGI_DEBRIEF_BRIDGE_REWARDED			SGI_DEBR_01
#define SGI_DEBRIEF_FINALBASECAMP_REWARDED		SGI_DEBR_01





//only for back compatibility!!!!!!

#define MISSION_COLLECTORS				6				//now unused
#define MISSION_ROAD					7				//now unused
#define MISSION_JARAIEVAC				28				//now unused
#define MISSION_OUTPOSTEVAC				29				//now unused

#define MISSION_BASECAMPARRIVAL				0
#define MISSION_MEDPATROL				1
#define MISSION_3CANYONSFIRST				2
#define MISSION_3CANYONSA				3
#define MISSION_3CANYONSB				4
#define MISSION_BAHNARFIRST				5
#define MISSION_BASECAMPFIRST				6
#define MISSION_FRENCHROUTE				7				//for back compatibility
#define MISSION_FRENCHROUTEA				7
#define MISSION_FRENCHROUTEB				8
#define MISSION_TUNNELS					9
#define MISSION_ARROYO					10
#define MISSION_TUNNELS2					11
#define MISSION_BIGRIVER					12
#define MISSION_NIGHT					13
#define MISSION_NIGHT_B					14
#define MISSION_AMBUSH					15
#define MISSION_BIGVALLEY					16
#define MISSION_OUTPOST					17
#define MISSION_RADIORELAY				18
#define MISSION_CRASHFLIGHT				19
#define MISSION_CRASH					20
#define MISSION_CONQUEST				21
#define MISSION_NVABASE					22
#define MISSION_UNDERGROUND				23
#define MISSION_ESCAPE					24
#define MISSION_PILOT					25
#define MISSION_STREAM					26
#define MISSION_BAHNARRAZEDA				27
#define MISSION_BAHNARRAZEDB				28
#define MISSION_BIGVALLEYCHOPPER			29
#define MISSION_BASECAMPDEFEAT				30
#define MISSION_BASECAMPDEFEAT2			31
#define MISSION_BASECAMPDEFEAT3			32


//DEFINES FOR ADDON MISSIONS

#define MISSION_BOMBERPILOT				50
#define MISSION_PLEIKU					51
#define MISSION_JARAI					52
#define MISSION_HANGINGBRIDGE			53
#define MISSION_NUIPEK					54
#define MISSION_MINEFACTORY				55
#define MISSION_NUIPEK2					56
#define MISSION_BASEATTACK				57
#define MISSION_NUIPEK3					58
#define MISSION_DEATHVALLEYA				59
#define MISSION_DEATHVALLEYB				60
#define MISSION_NVACAMP					61



//identifiers for bes-preloading
#define BESID_KNIFE					1		//SC_PreloadBES(BESID_KNIFE, "g\\weapons\\Vvh_Knife\\VvH_Knife_fpv.bes");
#define BESID_CLACKER					2		//SC_PreloadBES(BESID_CLACKER, "g\\weapons\\VvH_Switch\\VvH_switch_fpv.bes");
#define BESID_SMOKE3PV					3		//SC_PreloadBES(BESID_SMOKE3PV, "G\Weapons\VvH_Grenade_Smoke\VvH_Grenade_Smoke_stg.bes");
#define BESID_SMOKEFPV					4		//SC_PreloadBES(BESID_SMOKEFPV, "G\Weapons\VvH_Grenade_Smoke\VvH_Grenade_Smoke_fpv.bes");
#define BESID_C4FPV					5		//SC_PreloadBES(BESID_C4FPV, "g\\weapons\\Vvh_C4\\VvH_C4_fpv.bes");
#define BESID_C4STG					6		//SC_PreloadBES(BESID_C4STG, "g\\weapons\\Vvh_C4\\Vvh_C4_stg.BES");
#define BESID_HANDAXE					7	
#define BESID_PICKAXE					8
#define BESID_PIPE					9
#define BESID_BEERS					10
#define BESID_RADIOEAR					11
#define BESID_BINOCULAR					12
#define BESID_STIRRER					13
#define BESID_WINE					14
#define BESID_SHOVEL					15
#define BESID_HAMMER					16
#define BESID_MACHETTE					17
#define BESID_NAILS					18
#define BESID_CANTEEN					19
#define BESID_WOOD					20
#define BESID_NOTEBOOK					21
#define BESID_GUITAR					22
#define BESID_PENCIL					23
#define BESID_HARMONY					24


//bes preloading macros
#define BESPRELOAD_KNIFE 	SC_PreloadBES(BESID_KNIFE, "g\\weapons\\Vvh_Knife\\VvH_Knife_fpv.bes")
#define BESPRELOAD_CLACKER	SC_PreloadBES(BESID_CLACKER, "g\\weapons\\VvH_Switch\\VvH_switch_fpv.bes")
#define BESPRELOAD_SMOKE3PV	SC_PreloadBES(BESID_SMOKE3PV, "G\Weapons\VvH_Grenade_Smoke\VvH_Grenade_Smoke_stg.bes")
#define BESPRELOAD_SMOKEFPV	SC_PreloadBES(BESID_SMOKEFPV, "G\Weapons\VvH_Grenade_Smoke\VvH_Grenade_Smoke_fpv.bes")
#define BESPRELOAD_C4FPV	SC_PreloadBES(BESID_C4FPV, "g\\weapons\\Vvh_C4\\VvH_C4_fpv.bes")
#define BESPRELOAD_C4STG	SC_PreloadBES(BESID_C4STG, "g\\weapons\\Vvh_C4\\Vvh_C4_stg.BES")
#define BESPRELOAD_HANDAXE	SC_PreloadBES(BESID_HANDAXE, "g\\items\\v - pracovni nastroje\\ivg_sekera.bes")
#define BESPRELOAD_PICKAXE	SC_PreloadBES(BESID_PICKAXE, "g\\items\\v - pracovni nastroje\\ivq_kopac.bes")
#define BESPRELOAD_PIPE		SC_PreloadBES(BESID_PIPE, "g\\equipment\\us\\IUC_dymka.BES")
#define BESPRELOAD_BEERS	SC_PreloadBES(BESID_BEERS, "g\\equipment\\us\\caseofbeer\\IUJ_basapiv.BES")
#define BESPRELOAD_RADIOEAR	SC_PreloadBES(BESID_RADIOEAR, "g\\equipment\\us\\bes\\EOP_e_radioear01.BES")
#define BESPRELOAD_BINOCULAR	SC_PreloadBES(BESID_BINOCULAR, "g\\weapons\\VvH_Binoculars\\VvH_Binoculars_3pv.BES")
#define BESPRELOAD_STIRRER	SC_PreloadBES(BESID_STIRRER, "g\\items\\v - pracovni nastroje\\IVT_Varecka.bes")
#define BESPRELOAD_WINE		SC_PreloadBES(BESID_WINE, "g\\items\\v - nadoby\\ivk_dzban.bes")
#define BESPRELOAD_SHOVEL	SC_PreloadBES(BESID_SHOVEL, "g\\items\\us\\IUZ_Shovel_01.BES")
#define BESPRELOAD_HAMMER	SC_PreloadBES(BESID_HAMMER, "g\\items\\us\\IUZ_hammer_01.BES")
#define BESPRELOAD_MACHETTE	SC_PreloadBES(BESID_MACHETTE, "g\\items\\us\\IUZ_Machette_low_01.BES")
#define BESPRELOAD_NAILS	SC_PreloadBES(BESID_NAILS, "g\\items\\us\\IUK_Nail01.BES")
#define BESPRELOAD_CANTEEN	SC_PreloadBES(BESID_CANTEEN, "g\\items\\us\\IUZ_Canteen_low_01.BES")
#define BESPRELOAD_WOOD	SC_PreloadBES(BESID_WOOD, "g\\items\\us\\IUZ_traverse_snuff.BES")
#define BESPRELOAD_NOTEBOOK	SC_PreloadBES(BESID_NOTEBOOK, "g\\items\\us\\IUZ_note_book_01.BES")
#define BESPRELOAD_GUITAR	SC_PreloadBES(BESID_GUITAR, "g\\items\\us\\IUZ_quitar_01_01.BES")
#define BESPRELOAD_PENCIL	SC_PreloadBES(BESID_PENCIL, "g\\items\\U - DROBNOSTI\\IUC_tuzka1.BES")
#define BESPRELOAD_HARMONY	SC_PreloadBES(BESID_HARMONY, "g\\items\\US\\IOP_harmonica.BES")

//FPV ANIMATIONS MACROS
#define FPVANIM_USEC4		SC_PC_PlayFpvAnim2("g\\weapons\\Vvh_C4\\Movement\\c-4.stg",BESID_C4FPV,"g\\weapons\\Vvh_C4\\Eqp\\VvH_C4_fpv.eqp",NULL);SC_SND_PlaySound2D(10963)
#define FPVANIM_KNIFESWING	SC_PC_PlayFpvAnim2("g\\weapons\\VvH_Knife\\Movement\\sek.stg",BESID_KNIFE,"g\\weapons\\VvH_Knife\\Eqp\\VvH_Knife_fpv.eqp",NULL)
//#define FPVANIM_TRAPDISARM	SC_PC_PlayFpvAnim2("g\\traps\\deploy.stg",0,NULL,NULL)
#define FPVANIM_TRAPDISARM 	SC_Log(3,"Trying to play disarm trap anim");

#define OBJECTIVES_TIME					6.0f
#define HELP_TIME					6.0f

#define CAMPAIGN_GUN					9999		//player script generates weapon according to the mission

#endif
//#ifndef SC_DEF_H
