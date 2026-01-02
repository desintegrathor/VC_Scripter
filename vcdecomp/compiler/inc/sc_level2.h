/*
useful macros and functions for level scripting - used in all level scripts;
version 2.0 for Vietcong Addon
*/


#ifndef SC_LEVELLIBRARY2_H
#define SC_LEVELLIBRARY2_H 

#include <inc\sc_library.h>


//standard variables in all level scripts
dword gphase = 0;			//general phase of the level, stored in GVAR SGI_LEVELPHASE
dword pointstatus=0;		//pointman's status


//Objectives handling
s_SC_Objective Objectives [10];
int objcount=0;

#define Show_Obj SC_SetObjectives(objcount,Objectives,OBJECTIVES_TIME)
#define Show_ObjNS SC_SetObjectivesNoSound(objcount,Objectives,OBJECTIVES_TIME)

void Clear_Objectives(){
	int i;
	for (i=0;i<objcount;i++) Objectives[i].text_id==0;
	objcount=0;
}

void Add_Obj(dword textid){
	int i;
	for (i=0;i<objcount;i++) if (Objectives[i].text_id==textid) {
		SC_Log(1,"Duplicite objective added - %d",textid);
		return;
	}
	Objectives[objcount].text_id=textid;
	Objectives[objcount].status=SC_OBJECTIVE_STATUS_VALID;
	objcount++;
	Show_Obj;
}

void Add_ObjNS(dword textid){
	int i;
	for (i=0;i<objcount;i++) if (Objectives[i].text_id==textid) {
		SC_Log(1,"Duplicite objective added - %d",textid);
		return;
	}
	Objectives[objcount].text_id=textid;
	Objectives[objcount].status=SC_OBJECTIVE_STATUS_VALID;
	objcount++;
	Show_ObjNS;
}

void Complete_Obj(dword textid){
	int i;
	for (i=0;i<objcount;i++) {
		if ((Objectives[i].text_id==textid)&&(Objectives[i].status==SC_OBJECTIVE_STATUS_VALID)){
			Objectives[i].status=SC_OBJECTIVE_STATUS_COMPLETE;
			Show_Obj;		 
			return;
		}
	}	
}

void Fail_Obj(dword textid){
	int i;
	for (i=0;i<objcount;i++) if (Objectives[i].text_id==textid) Objectives[i].status=SC_OBJECTIVE_STATUS_FAILED;
	Show_Obj;
}

int Get_Obj_Stat(dword textid){
	int i;
	for (i=0;i<objcount;i++) if (Objectives[i].text_id==textid) return Objectives[i].status;
	return 0;
}


// Savegame macros

#ifndef SAVEGAMECOUNT
#define SAVEGAMECOUNT	1
#endif

BOOL savegame[SAVEGAMECOUNT];


#define SaveGame(name,desc)\
	{s_SC_MissionSave save;save.disable_info=FALSE;save.savename_id=name;save.description_id=desc;SC_MissionSave(&save);\
	SC_Log(3,"Saving game id %d",name);SC_Osi("Saving game id %d",name);}


#define SaveGame2(name,desc)\
	{s_SC_MissionSave save;save.savename_id=name;save.description_id=desc;save.disable_info=TRUE;SC_MissionSave(&save);\
	SC_Log(3,"Saving game id %d",name);SC_Osi("Saving game id %d",name);}


// sets level phase 
#define SetLevelPhase(newphase)\
	{gphase=newphase; SC_sgi(SGI_LEVELPHASE,newphase);\
	SC_Log(3,"Levelphase changed to %d",newphase);SC_Osi("Levelphase changed to %d",newphase);}

//initialization macros

#define InitSide(side,group,hideout)\
	{s_SC_initside initside; CLEAR(initside); initside.MaxHideOutsStatus = hideout;initside.MaxGroups = group;SC_InitSide(side,&initside);}

#define InitGroup2(side,group,players,followdist)\
	{s_SC_initgroup initgroup;\CLEAR(initgroup);initgroup.SideId = side;initgroup.GroupId=group;initgroup.MaxPlayers =players;initgroup.follow_point_max_distance=followdist;SC_InitSideGroup(&initgroup);}

#define InitGroup(side,group,players)\
	{s_SC_initgroup initgroup;\CLEAR(initgroup);initgroup.SideId = side;initgroup.GroupId=group;initgroup.MaxPlayers =players;SC_InitSideGroup(&initgroup);}

//sets inital global variables
void InitGlobals(){
		int i;
		for (i=0;i<SAVEGAMECOUNT;i++) savegame[i]=FALSE;
		Clear_Objectives();
		
		SC_sgi(SGI_MISSIONDEATHCOUNT,0);
		SC_sgi(SGI_MISSIONALARM,0);
		SC_sgi(SGI_LEVELPHASE,0);
		SC_sgi(SGI_ALLYDEATHCOUNT,0);
		SC_sgi(SGI_INTELCOUNT,0);
		SC_sgi(SGI_CHOPPER,0);
		SC_sgi(SGI_GAMETYPE,0);
		SC_Log(3,"Level difficulty is %d",SC_ggi(SGI_DIFFICULTY));
}

//sets standard follow order for team with six players
void SetFollowOrder(){
		s_SC_Ai_PlFollow follow[6];
		dword follow_order[6];
		dword point_order[6];	
		int i;
		
		CLEAR(follow);
		CLEAR(follow_order);
		CLEAR(point_order);
		follow[0].min_dist = 0.0f;
		follow[1].min_dist = 5.0f;
		follow[2].min_dist = 1.5f;
		follow[3].min_dist = 1.5f;
		follow[4].min_dist = 2.0f;

		for (i=0;i<5;i++){			
			follow[i].max_dist = follow[i].min_dist + 1.0f;
			follow[i].follow_change.x = frnd(0.5f);
			follow[i].follow_change.y = frnd(0.5f);
			follow[i].follow_change.z = 0.0f;							
		}

		// set follow props

		follow_order[0] = SC_P_MEMBERID_POINT;
		follow_order[1] = SC_P_MEMBERID_RADIO;
		follow_order[2] = SC_P_MEMBERID_MACHINEGUN;			
		follow_order[3] = SC_P_MEMBERID_MEDIC;
		follow_order[4] = SC_P_MEMBERID_DEMOLITION;

		point_order[0] = SC_P_MEMBERID_POINT;
		point_order[1] = SC_P_MEMBERID_MACHINEGUN;
		point_order[2] = SC_P_MEMBERID_DEMOLITION;
		point_order[3] = SC_P_MEMBERID_RADIO;
		point_order[4] = SC_P_MEMBERID_MEDIC;				
		
		SC_Ai_SetPlFollow(0,0,0,follow,follow_order,point_order,5);
		follow[0].min_dist = 0.0f;
		follow[1].min_dist = 4.0f;
		follow[2].min_dist = 1.5f;
		follow[3].min_dist = 1.5f;
		follow[4].min_dist = 1.5f;
		follow[5].min_dist = 2.0f;

		for (i=0;i<6;i++){			
			follow[i].max_dist = follow[i].min_dist + 1.0f;
			follow[i].follow_change.x = frnd(0.2f);
			follow[i].follow_change.y = frnd(0.2f);
			follow[i].follow_change.z = 0.0f;							

			point_order[i] = SC_P_MEMBERID_CAPTAIN;
		}


		// set follow props

		follow_order[0] = SC_P_MEMBERID_CAPTAIN;
		follow_order[1] = SC_P_MEMBERID_POINT;			
		follow_order[2] = SC_P_MEMBERID_RADIO;
		follow_order[3] = SC_P_MEMBERID_MACHINEGUN;
		follow_order[4] = SC_P_MEMBERID_MEDIC;
		follow_order[5] = SC_P_MEMBERID_DEMOLITION;

		
		SC_Ai_SetPlFollow(0,0,1,follow,follow_order,point_order,6);
}

//sets radio properties, now only sets hearable distance for the radio speech
void SetRadioProps(){
		SC_RadioSetDist(10.0f);
}


//setting of pointmans path

//setting basename of pointmans waypoints
#ifndef CHECKPOINTBASE
#define CHECKPOINTBASE "point%d"
#endif

void ResetCheckPoints(int from, int topoint){
	int j;
	char txt[32];
	c_Vector3 vec;
	
	if (from<topoint){
		topoint++;
		SC_Ai_ClearCheckPoints(SC_P_SIDE_US,0);			//initialization of pointmans road
		for (j=from;j<topoint;j++){		
			sprintf(txt,CHECKPOINTBASE,j);			
			SC_GetWp(txt,&vec);
			SC_Ai_AddCheckPoint(SC_P_SIDE_US,0,&vec,0);
		}
	} else {
		topoint--;
		SC_Ai_ClearCheckPoints(SC_P_SIDE_US,0);			//initialization of pointmans road
		for (j=from;j>topoint;j--){		
			sprintf(txt,CHECKPOINTBASE,j);			
			SC_GetWp(txt,&vec);
			SC_Ai_AddCheckPoint(SC_P_SIDE_US,0,&vec,0);
		}
	
	}

}

void AddCheckPoints(int from, int topoint){
	int j;
	char txt[32];
	c_Vector3 vec;
	
	topoint++;
		for (j=from;j<topoint;j++){		
			sprintf(txt,CHECKPOINTBASE,j);
			SC_GetWp(txt,&vec);
			SC_Ai_AddCheckPoint(SC_P_SIDE_US,0,&vec,0);
	}

}


//macro to check, if pointman can be "used"
#define PointTalkCheck if (SC_P_Ai_GetEnemies(info->param2)||(SC_P_GetWillTalk(SC_PC_Get())>1)||(SC_P_GetWillTalk(GetUS(1))>1)) \
		{info->param3=1;return TRUE;}

#endif
