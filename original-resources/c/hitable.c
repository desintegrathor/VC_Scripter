//hitable.c
//
//Shigor Birdman
//
//simple DO script - sends predefined message to level after receiving hit, parameter is pointer to master nod of DO

#include <inc\sc_global.h>
#include <inc\sc_def.h>

#define LEV_MESSAGE SCM_OBJECTDESTROYED			//message which will be sent to level.c

int ScriptMain(s_SC_OBJ_info *info){

	switch(info->event_type){
		case SC_OBJ_INFO_EVENT_INIT:

			return TRUE;	
			

		case SC_OBJ_INFO_EVENT_JUSTLOADED:
			break;

		case SC_OBJ_INFO_EVENT_RELEASE:
			break;

		case SC_OBJ_INFO_EVENT_HIT:			
			SC_LevScr_Event(LEV_MESSAGE,(dword)info->master_nod);
			break;

		case SC_OBJ_INFO_EVENT_DOTICK:
			break;

		case SC_OBJ_INFO_EVENT_USED:
			break;

	}// switch(info->event_type)


	return FALSE;

}// int ScriptMain(s_OBJ_info *info)
