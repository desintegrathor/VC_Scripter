#define RESPAWN_GROUP2_X	 45.0	//global_detect.c
#define RESPAWN_CAMP_X		 15.0	//global_detect.c
#define RESPAWN_ALL_X		-40.0	//global_detect.c
//mocal a ruiny jsou pres ScriptHelper //ruiny_detect.c //mocal_detect.c

#define B_RESPAWN_MOCAL	2000	//inicializace je v vc_hlidac.cxx !!!
#define B_RESPAWN_RUINY	2001
#define B_RESPAWN_GR2	2002
#define B_RESPAWN_GUN	2003
#define B_RETURN_BASE	2004

//#define B_INACTIVATE	2005

#define OBJECT_OK		"ivp_wooden_box_01#8"
#define OBJECT_DESTR	"ivp_wooden_box_01#8"

#define GVAR_GPHASE				500
#define GVAR_BOMBSTATUS__		502			//base offset to gvars for bomb states
#define GVAR_BOMBSTATUS01		502			//placeholders
#define GVAR_BOMBSTATUS02		503
#define GVAR_BOMBSTATUS03		504
#define GVAR_BOMBSTATUS04		505

#define GVAR_BOMBSTIME__		506			//base offset to gvars for bomb timers
#define GVAR_BOMBSTIME01		506			//timeholders
#define GVAR_BOMBSTIME02		507
#define GVAR_BOMBSTIME03		508
#define GVAR_BOMBSTIME04		509

#define GVAR_BOMBEXPLODED		510

#define SHOW_TIME				5.0f

#define BOMB_STATUS_STARTING	0
#define BOMB_STATUS_INACTIVE	1
#define BOMB_STATUS_ACTIVE		2
#define	BOMB_STATUS_EXPLODING	3
#define	BOMB_STATUS_EXPLODED	4
#define	BOMB_STATUS_DEFUSED		5
#define BOMB_STATUS_US_KILLED	6
#define BOMB_STATUS_VC_KILLED	7
#define BOMB_STATUS_DRAW		8
#define BOMB_STATUS_TIMEOUT		9

#define EASY_LIMIT	4

char *GetUSRndIni() {
	switch (rand()%6) {
		case 0: return "ini\\players\\net_us_sf1.ini"; break;
		case 1: return "ini\\players\\net_us_sf2.ini"; break;
		case 2: return "ini\\players\\net_us_sf3.ini"; break;
		case 3: return "ini\\players\\net_us_bangs.ini"; break;
		case 4: return "ini\\players\\net_us_crocker.ini"; break;
		case 5: return "ini\\players\\net_us_douglas.ini"; break;
	}
	return "net_us_sf1.ini";
}

#define	MAX_WEAPS	4
dword us_weap[MAX_WEAPS] = {1,11,17,21};

int GetUSRndWeapon()
{
	return us_weap[ rand()%MAX_WEAPS ];
}
