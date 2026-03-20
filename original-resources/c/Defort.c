//standard defort header file

#include <inc\us_equips.inc>


#define MEMBERID	SC_P_MEMBERID_RADIO
#define INIFILENAME	"ini\\players\\defort.ini"
#define NAMENUMBER	2502
#define ICONNAME	"defort"

#define PKNIFE 0						//predefined weapons - gotta change !
#define PPISTOL 22
#define PWEAPON1 32
#define PWEAPON2 60
#define WEAPSLOT1 0


void equipplayer(s_SC_P_CreateEqp *eqp, int *count){
	Equip_DEFORT_Full(eqp,count);
}


#include "teammate.inc"

