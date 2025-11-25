//default level.c


#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\mplevel.inc>

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
		c4nod = SC_NOD_GetNoMessage(NULL,"c4");
		if (c4nod) SC_DUMMY_Set_DoNotRenHier2(c4nod,TRUE);

		switch(SC_ggi(GVAR_MP_MISSIONTYPE)){

			case GVAR_MP_MISSIONTYPE_ATG:		   
				switch(SC_ggi(GVAR_MP_MISSIONSUBTYPE)){
					case 1:SC_SetObjectScript("bombplace","ini\\multiplayer\\scripts\\atg_dobj.c");break;
					case 2:SC_SetObjectScript("bombplace","ini\\multiplayer\\scripts\\bomb_dobj_vc.c");break;
				}// switch(SC_ggi(GVAR_MP_MISSIONTYPE))
				
				break;

		} //switch(SC_ggi(GVAR_MP_MISSIONTYPE))

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
			SC_InitSide(SC_P_SIDE_US,&initside);

			initside.MaxHideOutsStatus = 64;
			initside.MaxGroups = 8;
			SC_InitSide(SC_P_SIDE_VC,&initside);


			initgroup.SideId = SC_P_SIDE_US;		//US a-team
			initgroup.GroupId = 0;
			initgroup.MaxPlayers = 64;	// nemenit !!! Erik.
			SC_InitSideGroup(&initgroup);


			//VC Groups - for COOP mode
			initgroup.SideId = SC_P_SIDE_VC; //generic Vietcong
			initgroup.GroupId = 0;
			initgroup.MaxPlayers = 64;	// nemenit !!! Erik.
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 1;
			initgroup.MaxPlayers = 8;
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 2;
			initgroup.MaxPlayers = 6;
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 3;
			initgroup.MaxPlayers = 6;
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 4;
			initgroup.MaxPlayers = 6;
			SC_InitSideGroup(&initgroup);

			initgroup.GroupId = 5;
			initgroup.MaxPlayers = 8;
			SC_InitSideGroup(&initgroup);

			
			gphase = 1;
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
