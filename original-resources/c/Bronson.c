//standard bronson header file

#include <inc\us_equips.inc>


#define MEMBERID	SC_P_MEMBERID_DEMOLITION
#define INIFILENAME	"ini\\players\\bronson.ini"
#define NAMENUMBER	2501
#define ICONNAME	"bronson"

#define PKNIFE 0						//predefined weapons - gotta change !
#define PPISTOL 22
#define PWEAPON1 32
#define PWEAPON2 61
#define WEAPSLOT1 0


void equipplayer(s_SC_P_CreateEqp *eqp, int *count){
	Equip_BRONSON_Full(eqp,count);
}

#include "teammate.inc"