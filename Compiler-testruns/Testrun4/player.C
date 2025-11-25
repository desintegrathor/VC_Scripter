
// Définition du bot 
// Modifiable

#include <inc\us_equips.inc>						// fichier de skins à mettre dans "Vietcong\dev\compiler\inc"

#define SIDE 			SC_P_SIDE_VC 				// SC_P_SIDE_US
#define GROUPID			0							// Groupe auquel appartient le bot

#define MEMBERID		SC_P_MEMBERID_CAPTAIN 		/* SC_P_MEMBERID_MEDIC 
													   SC_P_MEMBERID_DEMOLITION
													   SC_P_MEMBERID_RADIO
													   SC_P_MEMBERID_MACHINEGUN    */

#define INIFILENAME		"ini\\players\\****.ini"	// skin du bot
#define NAMENUMBER		2506						// nom du bot (2506 = VC)

#define PKNIFE 			0							// les armes
#define PPISTOL 		22
#define PWEAPON1 		32
#define PWEAPON2 		60
#define PWEAPONSLOT1	0

#define EQUIP_BOOL		FALSE			// doit-on équiper ce bot ? (FALSE/TRUE) Attention MAJUSCULES obligatoires !
										// si oui (TRUE) la fonction en dessous doit être remplie  
										// si non (FALSE) il faut mettre le ligne en commentaire (avec //)
void equipplayer(s_SC_P_CreateEqp *eqp, int *count){
	Equip_*****_*****(eqp,count);
}

#include "props.inc"
#include "bot.inc"

