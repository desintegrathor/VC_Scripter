//usable.c
//
//Shigor Birdman
//
//simple DO script - sends predefined message to level after player uses the item, parameter is pointer to master nod of DO

#include <inc\sc_global.h>
#include <inc\sc_def.h>

#define LEV_MESSAGE 		SCM_OBJECTUSED		//message which will be sent to level.c, if 0 no message will be sent
#define INTERACTTEXT		0				//what text will be shown after the system string "Press USE to..."
#define USETIMES			1				//how many times it is possible to use the item, -1 means without restriction
#define USEDISTANCE		2				//how near must player be to use the item

int used=0;

int ScriptMain(s_SC_OBJ_info *info){
	float val;


	switch(info->event_type){
		case SC_OBJ_INFO_EVENT_INIT:
			return TRUE;				

		case SC_OBJ_INFO_EVENT_JUSTLOADED:
			break;

		case SC_OBJ_INFO_EVENT_RELEASE:
			break;

		case SC_OBJ_INFO_EVENT_HIT:			
			break;

		case SC_OBJ_INFO_EVENT_DOTICK:
			if (used==USETIMES) return FALSE;
			val = SC_DOBJ_CameraLooksAt(info->master_nod,USEDISTANCE);
			if (val<1.0f){
				SC_ACTIVE_Add(info->master_nod,2.0f*val,INTERACTTEXT);
				return FALSE;
			}			
			break;

		case SC_OBJ_INFO_EVENT_USED:
			if (used>-1) used++;
			SC_LevScr_Event(LEV_MESSAGE,(dword)info->master_nod);
			break;

	}// switch(info->event_type)


	return FALSE;

}// int ScriptMain(s_OBJ_info *info)
