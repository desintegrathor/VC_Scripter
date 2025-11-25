//standard NHUT header file

#include <inc\us_equips.inc>


#define MEMBERID	SC_P_MEMBERID_POINT
#define INIFILENAME	"ini\\players\\nhut.ini"
#define NAMENUMBER	2507
#define ICONNAME	"nhut"

#define PKNIFE 0						//predefined weapons - gotta change !
#define PPISTOL 22
#define PWEAPON1 11
#define PWEAPON2 0
#define WEAPSLOT1 0

void equipplayer(s_SC_P_CreateEqp *eqp, int *count){
	Equip_NHUT_Full(eqp,count);
}

#include "teammate.inc"
