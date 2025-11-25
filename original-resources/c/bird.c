//flying bird
//
//Shigor Birdman
//

#define ANIMATION 	"g\\camanims\\CAMERA\\ARRIVAL\\ptak arrival.anm"
#define ANISTART		1
#define ANILOOP		1623

#include <inc\sc_global.h>

s_SC_NOD_transform orig_trans;
float gtime=0;
float starttime,endtime;

int ScriptMain(s_SC_OBJ_info *info){
	s_SC_NOD_transform trans;

	switch(info->event_type){
		case SC_OBJ_INFO_EVENT_INIT:
			SC_NOD_GetTransform(info->master_nod,&orig_trans);
			starttime=SC_ANM_GetFrameTime(ANIMATION,ANISTART);
			endtime=SC_ANM_GetFrameTime(ANIMATION,ANILOOP);	
			gtime=starttime;
			SC_NOD_SetFromANM(ANIMATION,gtime,info->master_nod);			
			return TRUE;				
		
		case SC_OBJ_INFO_EVENT_JUSTLOADED:
			SC_NOD_SetFromANM(ANIMATION,gtime,info->master_nod);
			break;

		case SC_OBJ_INFO_EVENT_RELEASE:
			SC_NOD_SetTransform(info->master_nod,&orig_trans);
			break;

		case SC_OBJ_INFO_EVENT_HIT:			
			break;

		case SC_OBJ_INFO_EVENT_DOTICK:
			gtime+=info->time;
			if (gtime>endtime) gtime=starttime;
			SC_NOD_SetFromANM(ANIMATION,gtime,info->master_nod);
			break;

		case SC_OBJ_INFO_EVENT_USED:
			break;

	}// switch(info->event_type)


	return FALSE;

}// int ScriptMain(s_OBJ_info *info)
