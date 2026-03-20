/*
useful macros and functions for level scripting - used in all level scripts;

*/


#ifndef SC_LEVELLIBRARY_H
#define SC_LEVELLIBRARY_H 

#ifndef CHECKPOINTBASE
#define CHECKPOINTBASE "point"
#endif

#ifndef ALARMCOUNT
#define ALARMCOUNT 0
#endif

#include <inc\sc_library.h>


dword gphase = 0;
dword lastorder=0;
dword pointstatus=0;
dword alarmtype=0;
dword alarmer=0;
int enemydangertext=0;
BOOL reportedcontact=FALSE;								//first contact with the enemy reported to the base?
BOOL trapfound=FALSE;									//was found trap in this level?

//dword alarms[ALARMCOUNT];								//what to do on the alarmspot - only for pointman!
//c_Vector3 alarmspot[ALARMCOUNT];

typedef struct{
	c_Vector3 spot;
	float radius;

	dword type;		//1 - generic, 2 - trap, 3 - heard something
	BOOL found;
	int next;			//next collide sphere for traps
	int validfor;		//0 for all, 1 for pc only, 2 for point only, 3 for PC and point,4 not for player
	int disabledby;
}s_alarmspot;

s_alarmspot alarms[ALARMCOUNT];

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


/*#define Savegame(name,desc)\
	{s_SC_MissionSave save;save.savename_id=name;save.description_id=desc;SC_MissionSave(&save);\
	SC_Log(3,"Saving game id %d",name);SC_Osi("Saving game id %d",name);}
*/

#define SaveGame(name,desc)\
	{s_SC_MissionSave save;save.disable_info=FALSE;save.savename_id=name;save.description_id=desc;SC_MissionSave(&save);\
	SC_Log(3,"Saving game id %d",name);SC_Osi("Saving game id %d",name);}


#define SaveGame2(name,desc)\
	{s_SC_MissionSave save;save.savename_id=name;save.description_id=desc;save.disable_info=TRUE;SC_MissionSave(&save);\
	SC_Log(3,"Saving game id %d",name);SC_Osi("Saving game id %d",name);}


#define Setlevelphase(newphase)\
	{gphase=newphase; SC_sgi(SGI_LEVELPHASE,newphase);\
	SC_Log(3,"Levelphase changed to %d",newphase);SC_Osi("Levelphase changed to %d",newphase);}

#define SetLevelPhase(newphase)\
	{gphase=newphase; SC_sgi(SGI_LEVELPHASE,newphase);\
	SC_Log(3,"Levelphase changed to %d",newphase);SC_Osi("Levelphase changed to %d",newphase);}

#define Initside(side,group,hideout)\
	{s_SC_initside initside; CLEAR(initside); initside.MaxHideOutsStatus = hideout;initside.MaxGroups = group;SC_InitSide(side,&initside);}


#define Initgroup2(side,group,players,followdist)\
	{s_SC_initgroup initgroup;\CLEAR(initgroup);initgroup.SideId = side;initgroup.GroupId=group;initgroup.MaxPlayers =players;initgroup.follow_point_max_distance=followdist;SC_InitSideGroup(&initgroup);}

#define Initgroup(side,group,players)\
	{s_SC_initgroup initgroup;\CLEAR(initgroup);initgroup.SideId = side;initgroup.GroupId=group;initgroup.MaxPlayers =players;SC_InitSideGroup(&initgroup);}

int Getorder(){
	int i=1;
	int x;
	while (i<5) {
		if (!isdead(0,0,i)){
			x=SC_P_Ai_GetPeaceMode(GetUS(i));
			if (x!=lastorder){
				lastorder=x;
				return x;
				}
			}
	}
	return 0;
}

void Initglobals(){
		SC_sgi(SGI_MISSIONDEATHCOUNT,0);
		SC_sgi(SGI_MISSIONALARM,0);
		SC_sgi(SGI_LEVELPHASE,0);
		SC_sgi(SGI_ALLYDEATHCOUNT,0);
		SC_sgi(SGI_TEAMDEATHCOUNT,0);
		SC_sgi(SGI_TEAMWIA,0);
		SC_sgi(SGI_INTELCOUNT,0);
//		SC_sgi(SGI_DIFFICULTY,2);		
		SC_sgi(SGI_CHOPPER,0);
		SC_sgi(SGI_GAMETYPE,0);
//		SC_SND_MusicPlay(SC_ggi(SGI_CURRENTMISSION)+10,100);
		SC_Log(3,"Level difficulty is %d",SC_ggi(SGI_DIFFICULTY));
}

void Setfolloworder(){
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

#define Setradioprops SetRadioProps

void SetRadioProps(){
		s_SC_SpeachBreakProps props;

		/*CLEAR(props);props.pl_back_txt = 5111;
		props.pl_back_snd = 5111;
		props.ra_back_txt = 5008;
		props.ra_back_snd = 5008;
		props.ra_where_ru_nr = 3;
		props.ra_where_ru_txt[0] = 5010;
		props.ra_where_ru_txt[1] = 5009;
		props.ra_where_ru_txt[2] = 5011;

		props.ra_where_ru_snd[0] = 5010;
		props.ra_where_ru_snd[1] = 5009;
		props.ra_where_ru_snd[1] = 5011;
		props.ra_where_ru_snd[3] = 0;
		props.ra_where_ru_snd[4] = 0;
		SC_RadioBreak_Set(&props);		*/
		//SC_PC_EnableRadioBreak(TRUE);
		SC_RadioSetDist(10.0f);
}

BOOL Reportcontact(){
	float time=2.0f;
	dword member;
	
	if (reportedcontact) return FALSE;
	member=GetUS(SC_P_MEMBERID_RADIO);
	if (!member) return FALSE;
	if (!SC_P_Ai_GetSureEnemies(member)&&!SC_ggi(SGI_MISSIONALARM))	return FALSE;
	reportedcontact=TRUE;
	SC_P_Speach(GetUS(SC_P_MEMBERID_RADIO),4010,4010,&time);
	time+=1.0f;
	SC_SpeachRadio(5013,5013,&time);
	return TRUE;
}


void Clearalarmspots(){
	int i;
		CLEAR(alarms);
		for (i=0;i<ALARMCOUNT;i++) {
			alarms[i].found=FALSE;
			alarms[i].radius=1;
			alarms[i].type=1;
			alarms[i].validfor=0;
			alarms[i].disabledby=0;
		}	   	
	
}

void Addtrap(int pos, void *trapnod){
	c_Vector3 gTinPos;
	c_Vector3 gEndOfWire;
	c_Vector3 gWireDir;
	void *nod;
	float len;

	SC_Log(3,"adding trap on pos %d",pos);
	alarms[pos].type=2;
	alarms[pos+1].type=2;
	alarms[pos].next=pos+1;
	alarms[pos+1].next=pos;
	alarms[pos].validfor=4;
	alarms[pos+1].validfor=4;

	nod = SC_NOD_Get(trapnod,"Plechovka");
	if (!nod) {
		SC_message("trap not found!!!");
		return;
	}
	SC_NOD_GetWorldPos(nod,&gTinPos);

	nod = SC_NOD_Get(trapnod,"Konec dratu");
	SC_NOD_GetWorldPos(nod,&gEndOfWire);

	gWireDir.x = gEndOfWire.x - gTinPos.x;
	gWireDir.y = gEndOfWire.y - gTinPos.y;
	gWireDir.z = gEndOfWire.z - gTinPos.z;
	len=3*SC_VectorLen(&gWireDir) * 0.25 + 0.5f;
	alarms[pos].radius = len;
	alarms[pos+1].radius = len;	
	alarms[pos].spot.x = gTinPos.x + 0.25f * gWireDir.x;
	alarms[pos].spot.y = gTinPos.y + 0.25f * gWireDir.y;
	alarms[pos].spot.z = gTinPos.z + 0.25f * gWireDir.z;	
//	SC_Log(3,"Trap on %f %f %f, radius %f",alarms[pos].spot.x,alarms[pos].spot.y,alarms[pos].spot.z,len);

	alarms[pos+1].spot.x = gTinPos.x + 0.75f * gWireDir.x;
	alarms[pos+1].spot.y = gTinPos.y + 0.75f * gWireDir.y;
	alarms[pos+1].spot.z = gTinPos.z + 0.75f * gWireDir.z;
	
}

int Removetrap(void *trapnod){
	int j;
	c_Vector3 vec;
	void *nod;
	c_Vector3 gTinPos;
	c_Vector3 gEndOfWire;
	c_Vector3 gWireDir;

	nod = SC_NOD_Get(trapnod,"Plechovka");
	if (!nod) {
		SC_message("trap not found!!!");
		return -1;
	}
	SC_NOD_GetWorldPos(nod,&gTinPos);

	nod = SC_NOD_Get(trapnod,"Konec dratu");
	SC_NOD_GetWorldPos(nod,&gEndOfWire);
	gWireDir.x = gEndOfWire.x - gTinPos.x;
	gWireDir.y = gEndOfWire.y - gTinPos.y;
	gWireDir.z = gEndOfWire.z - gTinPos.z+10000;		//because it's allready out
	vec.x = gTinPos.x + 0.25f * gWireDir.x;
	vec.y = gTinPos.y + 0.25f * gWireDir.y;
	vec.z = gTinPos.z + 0.25f * gWireDir.z;	
//	SC_Log(3,"Trying to remove Trap on %f %f %f",vec.x,vec.y,vec.z);

	for (j=0;j<ALARMCOUNT;j++){
//		if (!alarms[j].found&&(alarms[j].type==2)&&SC_IsNear3D(&alarms[j].spot,&vec,3)){
		if (SC_IsNear2D(&alarms[j].spot,&vec,1)){
			alarms[j].found=TRUE;
			alarms[j+1].found=TRUE;
			SC_Log(3,"removing trap %d",j);
			return j;
			}
	}
	//SC_message("cannot remove trap!!");
	return -1;
}

BOOL alarmvalid (int who, int what){
	//0 for all, 1 for pc only, 2 for point only, for PC and point
	switch (what){
	case 0:
		return TRUE;
	case 1:
		if (!who) return TRUE;
		break;
	case 2:
		if (who==1) return TRUE;
		break;
	case 3:
		if (who<2) return TRUE;
		break;		
	case 4:
		if (who) return TRUE;
		break;
	}
	return FALSE;
}

void pointdanger(){
	if ((SC_P_Ai_GetPeaceMode(GetUS(1))==SC_P_AI_PEACEMODE_POINT)) {
		SC_Ai_SetPeaceMode(0,0,SC_P_AI_PEACEMODE_HOLD);
		SC_Ai_PointStopDanger(0,0);
	}
}			

int Checkalarmspots(){
	int j,i;
	float time;
	dword member,x,pointm;
	c_Vector3 vec;
	
	
	
	alarmtype=0;
	pointm=pointstatus;
	for (i=0; i<6;i++){
		member=GetUS(i);
		if (SC_P_IsReady(member)){
//			if (SC_P_Ai_GetSureEnemies(member)) return FALSE;
//			if (SC_P_Ai_GetPeaceMode(member)!=SC_P_AI_PEACEMODE_POINT) return FALSE;
			SC_P_GetPos(member,&vec);
			for (j=0;j<ALARMCOUNT;j++){
				if (!alarms[j].found &&SC_IsNear3D(&alarms[j].spot,&vec,alarms[j].radius)&&alarmvalid(i,alarms[j].validfor)){
					switch (alarms[j].type){
					case 1:
						//nothing
						break;
					case 2:
						//trap - grenade and string						
						time=0;
						if (trapfound) SC_P_ScriptMessage(member,SCM_BOOBYTRAPFOUND,1);
							else SC_P_ScriptMessage(member,SCM_BOOBYTRAPFOUND,0);
						trapfound=TRUE;
						pointstatus=1;
						alarms[alarms[j].next].found=TRUE;
						break;
					case 3:				//unpassable terain
						time=0;
						if (i==1) {
							PSay(member,4062);
							pointstatus=20;
						}else PSay(member,4061);
						
						break;
					case 4:				//enemy nearby
						time=0;
						if (i==1) {
							PSay(member,enemydangertext);
							pointdanger();
							pointstatus=2;
						}
						break;
					case 5:
						//dead montagnard
						time=0;
//						if (!i) PCSay(5218)
//						else if (i==1) PSay(member,5407) else PSay(member,5307);
						if (i==2) PSay(member,4884);
						pointdanger();
						break;
					case 10:
						//punji trap
						if (trapfound) SC_P_ScriptMessage(member,SCM_BOOBYTRAPFOUND,1);
							else SC_P_ScriptMessage(member,SCM_BOOBYTRAPFOUND,0);
						trapfound=TRUE;
						pointstatus=10;
						break;
					}
					
					alarmtype=alarms[j].type;
					alarmer=i;
					if (alarmvalid (i,alarms[j].disabledby)) alarms[j].found=TRUE;
					SC_Log(3,"%d found on alarm spot %d by %d",alarmtype,j,i);
					return j;
				}
			}
		}
	}
	return -1;
}

void Resetcheckpoints(int from, int topoint){
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

void Addcheckpoints(int from, int topoint){
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

int Getpeacemode(){
	int i,p;
	for (i=1;i<6;i++) 
		if (!isdead(0,0,i)){
			p=SC_P_Ai_GetPeaceMode(GetUS(i));
			if (p!=SC_P_AI_PEACEMODE_HOLD) return p;
		}
	return SC_P_AI_PEACEMODE_HOLD;
}


void Resetpeacemode(){
		SC_Ai_SetPeaceMode(0,0,Getpeacemode());
}


#define PointTalkCheck if (SC_P_Ai_GetEnemies(info->param2)||(SC_P_GetWillTalk(SC_PC_Get())>1)||(SC_P_GetWillTalk(GetUS(1))>1)) \
		{info->param3=1;return TRUE;}


#endif
