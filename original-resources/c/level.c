//	main level.c
//	simple level script
// 	Created by Shigor		14.1. 04
//WARNING - all texts used here are just random numbers...


//master definitions

//how many save games are there in the level?
#define SAVEGAMECOUNT		5

//unique numeric mission identifier  - see sc_def.h
#define MISSION_IDENTIFICATOR	0

//set the base of the name for the pointman path
#define CHECKPOINTBASE "POINTMANPATH#%d"


//includes
#include "sc_level.h"			//macros only for the level, includes sc_def and sc_global.h

//variables

float timer;
c_Vector3 levelexit;

//functions


//scene initialization - DO scripts initialization, BES preloads, also can be used for getting initial position of the objects
//		warning - this callback is also initialized after loading the save game, but the variables will be than rewritten to the saved state! 
void InitScene(){
	//	SC_SetObjectScript("d_past_04_01","levels\\LIK_Tunnels\\data\\Tunnels01\\scripts\\past.c");
	//	place initialization of all object scripts - name and fullpath to the script!
	
	
	//	BESPRELOAD_HANDAXE;
	//	place all preload macros from the sc_def.h for the special equipment here
}

//level initialization in the first time tick

void Levelnit(s_SC_L_info *info){
	s_SC_initside initside;
	s_SC_initgroup initgroup;
	
	SC_sgi(SGI_CURRENTMISSION,MISSION_IDENTIFICATOR);		//initialization of the global variable with the mission identifier
		
	CLEAR(initside);
	CLEAR(initgroup);
	
	InitGlobals();			//initialize various global variables, clear objectives etc - see sc_level.h
	SetRadioProps();			//sets radio properties, only the visibility of the subtitles
		
	InitSide(0,8,32);			//initialization of the US SIDE
	InitSide(1,16,64);			//initialization of the VC SIDE

	InitGroup2(0,0,6,30)			//team initialization, with follow distance 30 meters

	InitGroup(1,0,16);			//vietcong generic group initialization

	SC_FadeTo(TRUE,0);		//blackout the screen until the rest of the game initializes
	
	//do some other initialization here
	//for example taking positions of important places in the level
	SC_GetWp("WayPoint#100",&levelexit);
	
	SC_ArtillerySupport(FALSE);		//disable arty support
	SC_Ai_EnableRelaxWalk(0,0,FALSE);	//disable relaxed walk for the team
	SetFollowOrder();			//set standard follow order
	
	ResetCheckPoints(1,10);		//set the pointman path from the waypoint "POINTMANPATH1" to "POINTMANPATH10" including
	
	SetLevelPhase(1);			//switch level phase to 1 (both globalvar and local gphase)
	nextex(0.5f);			//set next execution time to 0.5 seconds
}

//scene release	- place all release stuff here (releasing of the waypoint blockers etc)
void ReleaseScene(){
}

//after load call	- this call will be executed after loading the game from the saved state, use for creating blockers etc.
void LoadedScene(){
}

//object was used with interaction
void ObjectUsed(s_SC_L_info *info){
	char *objectname;
	float time;
	
	objectname = SC_NOD_GetName((void*)info->param2);	//objectname will contain engine name of the calling nod
	time=SC_P_GetWillTalk(SC_PC_Get());			//set the time to the time when pc stops talking
	time+=0.1f;					//add small delay here
	if (SC_StringSame(objectname,"someobject")){
		//do something, for instance comment using
		SC_P_Speech2(SC_PC_Get(),5666,&time);
	} else
	if (SC_StringSame(objectname,"someotherobject")){
		//do something, for instance comment using
		SC_P_Speech2(SC_PC_Get(),5666,&time);
	}
}

//object was destroyed 
void ObjectDestroyed(s_SC_L_info *info){
	char *objectname;
	float time;
	
	objectname = SC_NOD_GetName((void*)info->param2);	//objectname will contain engine name of the calling nod
	time=SC_P_GetWillTalk(SC_PC_Get());			//set the time to the time when pc stops talking
	time+=0.1f;					//add small delay here
	if (SC_StringSame(objectname,"someobject")){
		//do something, for instance comment using
		SC_P_Speech2(SC_PC_Get(),5666,&time);
	} else
	if (SC_StringSame(objectname,"someotherobject")){
		//do something, for instance comment using
		SC_P_Speech2(SC_PC_Get(),5666,&time);
	}
}

//level script received a message
void LevelEvent(s_SC_L_info *info){
	//switch according the type of the message (used defined!)
	switch (info->param1){
		case SCM_OBJECTUSED:
			ObjectUsed(info);		   		
		break;
		case SCM_OBJECTDESTROYED:
			ObjectDestroyed(info);
		break;
		default:
		break;
	}
}

//simple function which will return true if all three VC from the group 0 are dead
BOOL AllCongsDead(){
	int i;
	for (i=0;i<2;i++)
	if (SC_P_IsReady(SC_P_GetBySideGroupMember(1,0,i))) return FALSE;
	return TRUE;
}


//this is the first time tick after the initialization of the game - you can do some initializations here
void FirstTimeTick(s_SC_L_info *info){
	float time;
	
	SC_FadeTo(FALSE,0.5f);		//unfade the screen from blackness.
					//do some chitchat 
	
	time=1;
	SC_RadioBatch_Begin();			//start radio comm
	SC_P_Speech2(SC_PC_Get(),50939,&time);	//player says 50939
	time+=0.5f;				//small delay
	SC_SpeechRadio2(50940,&time);		//radio says 50940
	time+=0.5f;				//small delay
	SC_P_SpeechMes2(SC_PC_Get(),50939,&time,1);//player says 50939, after finishing speech script will receive speech callback 2
	SC_RadioBatch_End();	
	SetLevelPhase(2);
}


//LEVEL time tick
void TimeTick(s_SC_L_info *info){
	float time;
	c_Vector3 vec;
	
	
	switch (gphase){
	case 1:
		if (!SC_PC_Get()) return;		//if the player object was not initialized, something is wrong, return!
						//you may also want to detect other created players
		FirstTimeTick(info);
		break;
	case 2:					//now the game begun and is initialized... do what you want
						//let's say you want the level with three congs, after all are dead
						//player will say something, which will enable radio communication
						//after radio communication he may exit the level
		if (AllCongsDead()){
			timer=5;			//they are all dead, so wait few seconds...
			SetLevelPhase(3);
		}
		break;
	case 3:
		timer-=info->elapsed_time;
		if (timer<0){
			//timer elapsed, so say something.
			time=SC_P_GetWillTalk(SC_PC_Get());		//set the time to the time when pc stops talking
			SC_P_SpeechMes2(SC_PC_Get(),50939,&time,12);
				//player says 50939, after finishing speech script will receive speech callback 2
			SetLevelPhase(4);
		}
		break;
	case 4:				//script waits until player finished radio comm.
		break;
	case 5:				//player can now exit the level
		SC_PC_GetPos(&vec);	//get players position
		if (SC_IsNear2D(&vec,&levelexit,3)){		//is player maximum 3 meters from the level exit?
			SetLevelPhase(100);
			SC_MissionDone();			//end mission
		}
		break;
	}
}

//Loud shot callback - for the SC_GetLoudShot() function
void LoudShotCallback(s_SC_L_info *info){
}

// RADIO USAGE
void RadioUsed(int param){
	float time;
	
	time=SC_P_GetWillTalk(SC_PC_Get());		//set the time to the time when pc stops talking
	
	//param contains id of the radio communication
	switch(param){
	case 2:						//radio communication number 2 (enabled with SC_Radio_Enable(2);
		SC_RadioBatch_Begin();			//start radio comm
		SC_P_Speech2(SC_PC_Get(),50939,&time);	//player says 50939
		time+=0.5f;				//small delay
		SC_SpeechRadio2(50940,&time);		//radio says 50940
		time+=0.5f;				//small delay
		SC_P_SpeechMes2(SC_PC_Get(),50939,&time,2);//player says 50939, after finishing speech script will receive speech callback 2
		SC_RadioBatch_End();
		break;
	}
}

//Callback after playng speech
void SpeechDone(int param){
	//param contains id of the speech finished
	
	switch(param){
	case 1:			//this is the end of the radio comm 1 (from the first time tick
				//save the game - warning, after load this call will beexecuted again, so be sure to handle this situation
		if (!savegame[param]) {		
			savegame[param]=TRUE;	//this save is now used, want be repeated
						//add some objectives
			Add_Obj(54183);
			Add_Obj(54184);
			SaveGame(54201,54202);
		}
		break;
	case 2:			//this is the end of the radio comm 2 (see RadioUsed()
				//save the game - warning, after load this call will beexecuted again, so be sure to handle this situation
		if (!savegame[param]) {		
			savegame[param]=TRUE;	//this save is now used, want be repeated
			SetLevelPhase(5);		//for example, do what you want here
			SaveGame(54201,54202);
		}
		break;
	case 12:			//callback from the timetick - player said something, so for example enable the radio usage
		SC_Radio_Enable(2);
		Complete_Obj(54183);	//complete some objective
		break;
	case 99:
		SC_Ai_SetPeaceMode(0,0,SC_P_AI_PEACEMODE_POINT);				
		break;
	default:
		break;
	}
}

//callback after finishing camere animation
void ViewAniCallback(int param){
	switch(param){
	case 1:
		break;
	}
}

//pointman interaction - geting info about what interaction text to show
BOOL PointInteractInfo(s_SC_L_info *info){
	PointTalkCheck;			//check if poitman can talk at all
	   switch (info->param1){
		case 0:
			info->param3=2115;			//to let pointman lead the team
			break;
		case 1:
			info->param3=2118;			//to stop the pointman
			break;
		case 2:
			info->param3=2119;			//to talk with the pointman
			break;
	   }
	return TRUE;
}

//interaction with the pointman
BOOL PointInteract(s_SC_L_info *info){
	c_Vector3 vec;
   	float time;

	PointTalkCheck;				//check if poitman can talk at all
	
   	
   	time=SC_P_GetWillTalk(SC_PC_Get());		//set the time to the time when pc stops talking
   	
   	switch (info->param1){
	case 0:  					//pointman is in hold or follow mode - lead the team!
		SC_P_Speech2(SC_PC_Get(),51005,&time);	//pc gives order
		time+=0.5f;
		SC_P_SpeechMes2(info->param2,5410 + rand()%5,&time,99);		//pointman responds with some random talk, finished with callback 99
		break;
	case 1:   		
	   	SC_Ai_SetPeaceMode(0,0,SC_P_AI_PEACEMODE_HOLD);  	//HOLD!
  		break;
  	case 2:						//pointman is leading, but stays on the place
		if (SC_Ai_GetCurCheckPoint(0,0,&vec)) 		//path is defined, so he is waiting for the others
			switch (rand()%4){
			case 0:
				SC_P_Speech2(info->param2,5404,&time);
				break;
			case 1:
				SC_P_Speech2(info->param2,5408,&time);
				break;
			case 2:
				SC_P_Speech2(info->param2,5409,&time);
				break;
			case 3:
				SC_P_Speech2(info->param2,5418,&time);
				break;
			}
			/*
				else DoSomeThing();
				this means Pointman has no defined path
			*/
		break;
   	}
	return TRUE;
}

//artilerry usage callback, param is center of the bombardment
void ArtilleryCallback(c_Vector3 *param){
}

//lightstick used by player callback
void LightStickUsed(){
}

//story skip was enabled and called
void StorySkip(){
}

// ################# SCRIPT MAIN

int ScriptMain(s_SC_L_info *info){

//main loop
switch (info->message){
   case SC_LEV_MES_INITSCENE:
	InitScene();
	break;

   case SC_LEV_MES_JUSTLOADED:
   	LoadedScene();
   	break;

   case SC_LEV_MES_RELEASESCENE:
   	ReleaseScene();
   	break;

   case SC_LEV_MES_EVENT:
	LevelEvent(info);
	break;

   case SC_LEV_MES_RADIOUSED:
	RadioUsed(info->param1);
	break;

   case SC_LEV_MES_SPEACHDONE:
	SpeechDone(info->param1);
	break;

   case SC_LEV_MES_VIEWANIMCALLBACK:
   	ViewAniCallback(info->param1);
   	break;
   	
  	
   case SC_LEV_MES_GETMUSIC:	
	break;

   case SC_LEV_MES_MUSICDONE:   	
   	break;
   	
   case SC_LEV_MES_POINTINTERACTINFO:
   	PointInteractInfo(info);
   	break;
 
  case SC_LEV_MES_POINTINTERACT:
   	PointInteract(info);
   	break;
    
   case SC_LEV_MES_ARTILLERY:
   	ArtilleryCallback(&(info->param4));
   	break;
   	
   case SC_LEV_MES_LIGHTSTICK_USED:
   	LightStickUsed();
   	break;
   	
   case SC_LEV_MES_LOUDSHOTCALLBACK:
   	LoudShotCallback(info);
   	break;
   
   case SC_LEV_MES_STORYSKIP:
   	StorySkip();
   	break;
   	
   case SC_LEV_MES_TIME:
	if (!gphase) Levelnit(info);
		else TimeTick(info);
	break;

}	
	return 1;
}
