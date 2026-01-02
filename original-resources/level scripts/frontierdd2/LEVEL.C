//default level.c


#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\mplevel.inc>
#include "coop\!m_defs.h"

dword gphase = 0;


int ScriptMain(s_SC_L_info *info){
	float fl;
	int i;
	s_SC_initside initside;
	s_SC_initgroup initgroup;
	c_Vector3 vec;
	char txt[32];		
	BOOL hide_weapons,hide_CTF_flags,teamgame,hideRW;
	void *c4nod;

   	info->next_exe_time  = 10.0f;

   
   switch (info->message)
   {

   case SC_LEV_MES_INITSCENE:
	   

		InitScene(info);
		// hide C4
		//c4nod = SC_NOD_GetNoMessage(NULL,"c4");
		//if (c4nod) SC_DUMMY_Set_DoNotRenHier2(c4nod,TRUE);

		SC_SetObjectScript("bombplace","Levels\\Frontier\\Data\\Frontier_vcrd\\scripts\\bombplace_vc.c");
		//SC_SwitchSceneSCS("LEVELS\\Frontier_dd2\\data\\Frontier_dd2\\forscripts\\night.scs", 0.1);

		break;


	case SC_LEV_MES_TIME:
		switch (gphase)
		{
		case 0:							//first time init
									//various inits
			CLEAR(initside);
			CLEAR(initgroup);
			
			initside.MaxHideOutsStatus = 64;		//init sides and groups
			initside.MaxGroups = 8;
			SC_InitSide(SC_P_SIDE_VC,&initside);

			initside.MaxHideOutsStatus = 64;
			initside.MaxGroups = 8;
			SC_InitSide(SC_P_SIDE_US,&initside);


			initgroup.SideId = SC_P_SIDE_VC;		//US a-team
			initgroup.GroupId = 0;
			initgroup.MaxPlayers = 64;	// nemenit !!! Erik.
			SC_InitSideGroup(&initgroup);


			//VC Groups - for COOP mode
			initgroup.SideId = SC_P_SIDE_US; //generic Vietcong
			initgroup.GroupId = 0;
			initgroup.MaxPlayers = 64;	// nemenit !!! Erik.
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 1;
			initgroup.MaxPlayers = 10;
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 2;
			initgroup.MaxPlayers = 12;
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 3;
			initgroup.MaxPlayers = 8;
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 4;
			initgroup.MaxPlayers = 6;
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 5;
			initgroup.MaxPlayers = 8;
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 6;
			initgroup.MaxPlayers = 4;
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 7;
			initgroup.MaxPlayers = 2;
			SC_InitSideGroup(&initgroup);

			gphase = 1;
			info->next_exe_time = 60.0;
			break;

		case 1:
			//SC_SwitchSceneSCS("LEVELS\\Frontier_dd2\\data\\Frontier_dd2\\forscripts\\day.scs", 120.0);
			gphase = 2;
			break;

		}// gphase switch
   		break;

	case SC_LEV_MES_RADIOUSED:
		switch(info->param1){
		}
		break;

	case SC_LEV_MES_SPEACHDONE:
		switch(info->param1)
		{
		}
		break;
	}//switch (info->message){

	return 1;

}// int ScriptMain(void)
