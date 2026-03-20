//	pure level.c
// 	Created by Shigor		2.6. 03

//includes
#include <inc\sc_global.h>
#include <inc\sc_def.h>

//variables


//functions



// ################# SCRIPT MAIN

int ScriptMain(s_SC_L_info *info){

//main loop
	switch (info->message){
   	case SC_LEV_MES_INITSCENE:
		break;

   	case SC_LEV_MES_JUSTLOADED:
	   	break;

   	case SC_LEV_MES_RELEASESCENE:
   		break;

   	case SC_LEV_MES_EVENT:
		break;

   	case SC_LEV_MES_RADIOUSED:
		break;

   	case SC_LEV_MES_SPEACHDONE:
		break;

   	case SC_LEV_MES_VIEWANIMCALLBACK:
	   	break;
  	  	
   	case SC_LEV_MES_GETMUSIC:
		break;

   	case SC_LEV_MES_MUSICDONE:   	
   		break;
   	
   	case SC_LEV_MES_POINTINTERACTINFO:
   		break;
 
  	case SC_LEV_MES_POINTINTERACT:
   		break;
    
   	case SC_LEV_MES_ARTILLERY:
   		break;
   	
   	case SC_LEV_MES_LIGHTSTICK_USED:
   		break;
   	
   	case SC_LEV_MES_LOUDSHOTCALLBACK:
   		break;
   
   	case SC_LEV_MES_STORYSKIP:
   		break;
   	
   	case SC_LEV_MES_TIME:
		break;
	}	

	return 1;
}
