//standard Crocker header file

#include <inc\us_equips.inc>


#define MEMBERID	SC_P_MEMBERID_MEDIC
#define INIFILENAME	"ini\\players\\crocker.ini"
#define NAMENUMBER	2505
#define ICONNAME	"crocker"

#define PKNIFE 0						//predefined weapons - gotta change !
#define PPISTOL 22
#define PWEAPON1 32
#define PWEAPON2 62
#define WEAPSLOT1 0


void equipplayer(s_SC_P_CreateEqp *eqp, int *count){
	Equip_CROCKER_Full(eqp,count);
}



#include "teammate.inc"

