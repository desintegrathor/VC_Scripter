//standard Hornster header file

#include <inc\us_equips.inc>


#define MEMBERID	SC_P_MEMBERID_MACHINEGUN
#define INIFILENAME	"ini\\players\\hornster.ini"
#define NAMENUMBER	2503
#define ICONNAME	"hornsterico"

#define PKNIFE 0						//predefined weapons - gotta change !
#define PPISTOL 22
#define PWEAPON1 17
#define PWEAPON2 0
#define WEAPSLOT1 0


void equipplayer(s_SC_P_CreateEqp *eqp, int *count){
	Equip_HORNSTER_Full(eqp,count);
}


#include "teammate.inc"

