// multi player defs

//#define BOMBSCOUNT				2
//#define ONLYONE

#define SHOW_TIME				5.0

#define GVAR_GPHASE				500

#define GVAR_BOMBSTATUS__		502			//base offset to gvars for bomb states
#define GVAR_BOMBSTIME__		503			//base offset to gvars for bomb timers

#define GVAR_RESTART			550			//sem server da 1 pokud se provadi restart
#define GVAR_RESPAWN_GROUP		551			//sem se dava cislo skupiny respawnu

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
#define BOMB_STATUS_OFF			10
#define BOMB_STATUS_PLACING		11