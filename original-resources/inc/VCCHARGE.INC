#include <inc\sc_library.h>

//charger

//required functions from master c:
//initplayer - just before creating 
//dotick(float time)
//parameters - SPAWN_INSCRIPT, SPAWN_INACTIVE, SPAWN_CROUCHED, NOGRENADE (disables using grenade except for script throw)


//initial settings

c_Vector3 initialplace,wirebombplace,bridgeplace,grenadetarget,entrypoint;

void InitTargets(){
	char txt[64];
	
	SC_GetWp(INITIALPLACE,&initialplace);
	SC_GetWp(ENTRYPOINT,&entrypoint);	
	sprintf(txt,"Bombwire-%d",TARGETNUMBER);
	SC_GetWp(txt,&wirebombplace);
	sprintf(txt,"Placedesk-%d",TARGETNUMBER);
	SC_GetWp(txt,&bridgeplace);
	sprintf(txt,"Blowfence-%d",TARGETNUMBER);
	SC_GetWp(txt,&grenadetarget);
}



#ifndef INIFILENAME
#define INIFILENAME "ini\\players\\default_aiviet.ini" 
#endif

#ifndef AUTOEQUIP
dword Autoequip_Head[SC_P_CREATE_AEG_VALID_MAX]={0,0,0,0,0,0,0,0};
dword Autoequip_Body[SC_P_CREATE_AEG_VALID_MAX]={0,0,0,0,0,0,0,0};
#endif

#ifndef PMARKSMAN
#define PMARKSMAN 0.8f
#endif
#ifndef PVANGLE
#define PVANGLE 3.0f
#endif
#ifndef PVANGLENEAR
#define PVANGLENEAR 4.0f
#endif

#ifndef PKNIFE
#define PKNIFE 0						
#endif

#ifndef PPISTOL
#define PPISTOL 10
#endif

#ifndef PWEAPON1
#define PWEAPON1 1000
#endif

#ifndef PWEAPON2
#define PWEAPON2 0
#endif

#ifndef PSLOT1
#define PSLOT1 0
#endif

#ifndef MINIMDIF
#define MINIMDIF 0
#endif

#ifndef BATTLE_VIS
#define BATTLE_VIS 50
#define PEACE_VIS 40
#endif

#ifndef REACTIONTIME
#define REACTIONTIME 0
#endif

#ifndef SCOUT
#define SCOUT 0.0f;
#endif 

#ifndef MAXHEAR
#define MAXHEAR 1000
#endif 

#ifndef AMICOMMANDER
#define AMICOMMANDER FALSE
#endif

#define SAPPERANIM "g\\characters\\anims\\movies\\S021 C4 pokladani.stg"
#define THROWANIM "g\\characters\\anims\\A941_grnd_up_0.stg"
#define THROWANIM2 "g\\characters\\anims\\A942_grnd_up_1.stg"

#define RUNPRECISSION 2

#define initorders InitOrders

#ifndef RUNPOINTCNT
#define RUNPOINTCNT 1
c_Vector3 runpoints[1];
void InitOrders(){
}
#endif

#ifndef RUNTO
#define RUNTO 0
#endif

#ifndef LASTRUN
#define LASTRUN RUNPOINTCNT
#endif


float battle_vis=BATTLE_VIS;
float peace_vis=PEACE_VIS;
BOOL amidead=FALSE;		//is player dead?
BOOL setbattle=FALSE;		//after hit set player to the battle mode?
c_Vector3 orig_pos;		//original position of player
BOOL amicommander=AMICOMMANDER;		//am i commander of my group?
int mycommander=0;
int runto=RUNTO;
int lastrun=LASTRUN;
float runtimer=0;

int gphase=0;
int myorders=0;			//parameters for speacial jobs

int mygun; //to delete after respawn


float respawntimer=0,bombtimer=0;
BOOL moving=FALSE;

void MakeFreeAi(dword pl_id){		//change player to normal free player, NEED to add> end of anims and other bullshits
	P_Battle(pl_id);
	P_Visibility(pl_id,battle_vis);
	gphase=10;
}

void CreatePlayer(s_SC_P_info *info){
	s_SC_P_Create pinfo;s_SC_P_CreateEqp eqp[10];
	int eqpcount,i;

		CLEAR(pinfo);pinfo.type = SC_P_TYPE_AI;
		pinfo.side = SC_P_SIDE_VC;
		pinfo.group = GGROUP;
		pinfo.member_id = MEMBERID;
		if (SC_StringSame(INIFILENAME,"ini\\players\\default_aiviet.ini")){
			pinfo.inifile = GetVCCampaignIni();
		} else 	pinfo.inifile = INIFILENAME;
		pinfo.name_nr = 2506;pinfo.icon_name = "nhut";
				

		pinfo.weap_knife = PKNIFE;
		pinfo.weap_pistol = PPISTOL;
		switch (PWEAPON1){
		case 1000: 
			mygun = getVCweapon(); 
			break;
		case 2000: 
			mygun = getVClongrangeweapon(); 
			break;
		case CAMPAIGN_GUN: 
			mygun = GetVCCampaignWeapon();
			break;
		default:
			mygun = PWEAPON1;
			break;
		}
		pinfo.weap_main1=mygun;
		pinfo.weap_main2 = PWEAPON2;
		pinfo.weap_slot1=PSLOT1;
		if ((Diffic()==3)&&(!(rand()%3))) pinfo.weap_slot1=59;
		//pinfo.weap_slot1=59;
		pinfo.recover_pos = info->pos;						
		CLEAR(eqp);
		
		pinfo.eqps = 0; 
		pinfo.eqp=NULL;  		
		for (i=0;i<SC_P_CREATE_AEG_VALID_MAX;i++){
			pinfo.aeg_valid_head_bes[i]=Autoequip_Head[i];
			pinfo.aeg_valid_body_bes[i]=Autoequip_Body[i];
		}
		GetVCEquip(&pinfo);

		pinfo.debrief_group=SC_P_DEBRIEFGROUP_VC;		

		#ifdef SPAWN_CROUCHED
		pinfo.flags|=SC_P_CREATE_FL_CROUCH;
		#endif
		#ifdef SPAWN_INACTIVE
		pinfo.flags|=SC_P_CREATE_FL_INACTIVE;
		#endif

		info->pl_id = SC_P_Create(&pinfo);
		if (MEMBERID) amicommander=FALSE; else amicommander=TRUE;
		InitTargets();
		SC_Log(3,"Created VC %d %d",GGROUP,MEMBERID);		
		//SC_message("Created");
		gphase = 1;
}

void FirstTimeInit(dword pl_id){
	float modif;
	s_SC_P_AI_props props;
	s_SC_P_SpecAnims specanim;
	
			SC_P_GetPos(pl_id,&orig_pos);
			SC_P_Ai_SetMode(pl_id,SC_P_AI_MODE_SCRIPT);
			
			SC_P_Ai_EnableShooting(pl_id,TRUE);
			

			CLEAR(props);SC_P_Ai_GetProps(pl_id,&props);
							
			props.scout=0.8f;
			switch(Diffic()){
			case 0:
				modif=1.0f;
				props.shoot_damage_mult = 0.7f;
				break;
			case 1:
				modif=0.5f;
				break;
			case 2:
				modif=0.2f;
				props.shoot_damage_mult = 1.1f;
				break;
			case 3:
				modif=0.0f;
				props.shoot_damage_mult = 1.3f;
				break;
			}
			props.shoot_imprecision = PMARKSMAN*modif;
			props.extend_searchway = FALSE;
			props.shortdistance_fight = 0.0f;props.max_vis_distance=PEACE_VIS;
			props.view_angle = PVANGLE;
			props.view_angle_near = PVANGLENEAR;
			props.reaction_time=REACTIONTIME;
			props.scout=SCOUT;
			props.hear_distance_max=MAXHEAR;

			#ifdef NOGRENADE
				props.grenade_sure_time=10000;
			#endif

					
			SC_P_SetSpeachDist(pl_id,30);

			SC_Log(3,"Reseted VC %d %d",GGROUP,MEMBERID);		
			gphase = 2;
}

void SendOthers(dword pl_id){
	int i,j;
	dword list[32];
	s_SC_P_getinfo pinfo;
	
	i=32;
	
	GetMyGroup(pl_id,list,&i);
	for (j=0;j<i;j++) if (list[j]!=pl_id) {
		S_Mes(list[j],SCM_RUN,2);
	}
	SC_sgi(SGI_LEVBASE_GROUP0+GGROUP,1);
		
}

void MoveCommand(dword pl_id){	
	c_Vector3 vec2;
	int i,j;
	float dist=100000,dx;
	dword list[32],chosen;
	s_SC_P_getinfo pinfo;
	
	i=32;
	
	SC_Log(3,"Moving command");
	GetMyGroup(pl_id,list,&i);
	
	chosen=pl_id;
	
	for (j=0;j<i;j++) if (list[j]!=pl_id) {
		SC_P_GetInfo(list[j],&pinfo);
		if (pinfo.member_id!=8){
			SC_P_GetPos(list[j],&vec2);
			dx=SC_2VectorsDist(&wirebombplace,&vec2);
			if (dx<dist){
				dist=dx;
				chosen=list[j];
			}
		}	
	}
	if (chosen==pl_id){
		SC_Log(2,"Error! VC %d %d cannot found new leader!!!",GGROUP,MEMBERID);
	} else{
		amicommander=FALSE;
		//S_Mes(chosen,SCM_YOUARECOMMANDER,0);
		switch(gphase){
				case 2:			//run to place bomb
				case 5:
				case 6:				
				case 10:			
				case 11:
				case 12:
				case 13:
					S_Mes(chosen,SCM_RUN,3);
					break;				
				case 15:			//run to throw grenade
				case 16:
				case 17:
					S_Mes(chosen,SCM_RUN,4);
					break;
			
			
		}
	}
}

int ScriptMain(s_SC_P_info *info){
	int i;
	s_SC_P_getinfo ginfo;
	char txt[256];
	dword member;
	s_SC_NOD_transform tran;
	c_Vector3 vec;
	
	info->next_exe_time=0.1f;
	
	switch (info->message){
	case SC_P_MES_KILLED:
		SC_sgi(SGI_MISSIONDEATHCOUNT,SC_ggi(SGI_MISSIONDEATHCOUNT)+1);
		SC_Log(3,"VC %d %d died in gphase %d. Mission deathcount %d",GGROUP,MEMBERID,gphase,SC_ggi(SGI_MISSIONDEATHCOUNT));
		if ((gphase<18)&&amicommander&&(gphase!=12)&&(gphase!=13)) {
			MoveCommand(info->pl_id);
		}
		amidead=TRUE;
		respawntimer=10;
		//info->next_exe_time=100000.0f;
		break;		
	case SC_P_MES_HIT:
		if (setbattle) MakeFreeAi(info->pl_id);
		break;
	case SC_P_MES_DOANIMEND:
		if (!SC_P_IsReady(info->pl_id)) return 1;
		SC_Log(3,"VC %d %d finishing animation in gphase %d",GGROUP,MEMBERID,gphase);
		switch (gphase){
		case 11:							//placing of the bomb
			SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
			SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
			SC_P_Ai_Go(info->pl_id,&initialplace);
			bombtimer=3;
			gphase=12;
			break;
		case 16:							//second part of grenade throwing
			SC_P_DoAnim(info->pl_id,THROWANIM2);
			gphase=17;
			break;
		case 17:							//throwing of the grenade
			{	c_Vector3 movdir;
				SC_P_GetPos(info->pl_id,&vec);
				vec.z+=1;
				movdir.z=grenadetarget.z-vec.z+1;
				movdir.y=grenadetarget.y-vec.y;
				movdir.x=grenadetarget.x-vec.x;
				movdir.x*=1.5f;
				movdir.y*=1.5f;
				SC_Item_Create2(148,&vec,&movdir);
				bombtimer=1;
									//send order to bridger
				S_Mes(GetVC(GGROUP,8),SCM_RUN,1);
				P_Battle(info->pl_id);
				SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
				SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
				SC_P_Ai_Go(info->pl_id,&initialplace);
				//gphase=18;				
			}
			break;
		case 22:							//placing of the bridge
			sprintf(txt,"Most-%d",TARGETNUMBER);
/*			SC_NOD_GetTransform(SC_NOD_Get(NULL,txt),&tran);
			tran.loc.z+=1000;
			SC_NOD_SetTransform(SC_NOD_Get(NULL,txt),&tran);*/
			SC_LevScr_Event(SCM_OBJECTUSED,(dword)SC_NOD_Get(NULL,txt));
			SC_P_Ai_Go(info->pl_id,&entrypoint);
			SendOthers(info->pl_id);
			
			gphase=25;
			break;
		}
		break;
	case SC_P_MES_INTERACT_GETTEXT:
	case SC_P_MES_INTERACT_DO:
		return 1;
		break;
	case SC_P_MES_EVENT:
		SC_Log(3,"VC %d %d received order %d %d",GGROUP,MEMBERID,info->param1,info->param2);
		switch(info->param1){
		case SCM_RUN:
		     switch(info->param2){
			case 0:			//just go for it!
				if (gphase<5){
					P_Script(info->pl_id);
					SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
					SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
					SC_P_Ai_Go(info->pl_id,&initialplace);
					gphase=5;
				} else SC_message("Error! VC %d %d has stupid order!",GGROUP,MEMBERID);
				break;
			case 1:			//bridger, go vith bridge!
				bombtimer=1;
				gphase=18;
				break;
			case 2:			//bridge on place, gogogo!
				P_Script(info->pl_id);
				SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
				SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
				SC_P_Ai_Go(info->pl_id,&entrypoint);
				gphase=25;
				break;
			case 3:			//you are new commander, run to place bomb!
				amicommander=TRUE;
				P_Script(info->pl_id);
				SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
				SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
				SC_P_Ai_Go(info->pl_id,&wirebombplace);
				gphase=10;
				break;
			case 4:			//you are new commander, run to thow grenade!
				amicommander=TRUE;
				P_Script(info->pl_id);
				SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
				SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
				SC_P_Ai_Go(info->pl_id,&wirebombplace);
				gphase=15;
				break;
		     	}
			break;
		case SCM_YOUARECOMMANDER:
			amicommander=TRUE;
			SC_Log(3,"%d %d is now commander of group %d",GGROUP,MEMBERID,GGROUP);
			break;			
		case SCM_NEWCOMMANDER:
			mycommander=info->param2;
			break;
		}		
		break;
	case SC_P_MES_TIME:
		if (amidead){
			if ((gphase==12)||(gphase==13)){
				bombtimer-=info->elapsed_time;
				if (bombtimer<0){
					SC_DoExplosion(&wirebombplace,2);
					gphase=15;				
					MoveCommand(info->pl_id);
				}
				return 1;
			}
			respawntimer-=info->elapsed_time;
			if ((respawntimer<0)&&(SC_P_GetDistance(SC_PC_Get(),info->pl_id)>10)){
				s_sphere sph;
				SC_P_GetPos(info->pl_id,&sph.pos);
				sph.rad=2;
				SC_RemoveItems(&sph,mygun);
				amidead=FALSE;
				SC_P_Recover(info->pl_id,&orig_pos,0);
				if (SC_ggi(SGI_LEVBASE_GROUP0+GGROUP)){
					P_Script(info->pl_id);
					SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
					SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
					SC_P_Ai_Go(info->pl_id,&initialplace);
					SC_Log(3,"VC %d %d respawning from phase %d to %d",GGROUP,MEMBERID,gphase,24);
					gphase=24;					
				} else
				switch(gphase){
				case 2:			//run for initial place
				case 5:
				case 6:				
					P_Script(info->pl_id);
					SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
					SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
					SC_P_Ai_Go(info->pl_id,&initialplace);
					SC_Log(3,"VC %d %d respawning from phase %d to %d",GGROUP,MEMBERID,gphase,5);
					gphase=5;					
					break;
				case 10:
				case 11:
				case 12:
				case 13:
				case 15:
				case 16:
				case 17:
					if (amicommander) {
						SC_message("Error, VC %d %d shouldn't be commander performing task %d!",GGROUP,MEMBERID,gphase);
					}
					P_Script(info->pl_id);
					SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
					SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
					SC_P_Ai_Go(info->pl_id,&initialplace);
					SC_Log(3,"VC %d %d respawning from phase %d to %d",GGROUP,MEMBERID,gphase,5);
					gphase=5;					
					break;
				case 18:
				case 20:
				case 22:
					P_Script(info->pl_id);
					SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
					SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
					SC_P_Ai_Go(info->pl_id,&bridgeplace);				
					SC_Log(3,"VC %d %d respawning from phase %d to %d",GGROUP,MEMBERID,gphase,20);
					gphase=20;
					break;
				case 24:
				case 25:
				case 50:
					P_Script(info->pl_id);
					SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
					SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
					SC_P_Ai_Go(info->pl_id,&initialplace);
					SC_Log(3,"VC %d %d respawning from phase %d to %d",GGROUP,MEMBERID,gphase,24);
					gphase=24;					
					break;
				}
			}
			return 1;
		}

		if (!SC_P_IsReady(info->pl_id)&&(gphase==1)) {
			info->next_exe_time=0.05f;
			return 0;
		}	
		
		switch (gphase){
		case 0:
			CreatePlayer(info);
			//SC_message("created exit");
			break;
		case 1:
			FirstTimeInit(info->pl_id);
			break;
		case 2:							//standard idle cycle
			break;
		case 5:							//running for initial place
			SC_P_GetPos(info->pl_id,&vec);
			if (SC_IsNear3D(&vec,&initialplace,2)){
				if (amicommander){
					SC_P_Ai_Go(info->pl_id,&wirebombplace);
					gphase=10;
				} else {
					SC_P_Ai_Stop(info->pl_id);
					SC_P_Ai_SetMovePos(info->pl_id, SC_P_AI_MOVEPOS_LIE);
					P_Battle(info->pl_id);
					gphase=6;
				}
			}			
			break;
		case 6:							//just waiting for others to do their work
			if (SC_ggi(SGI_LEVBASE_GROUP0+GGROUP)){
					P_Script(info->pl_id);
					SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
					SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
					SC_P_Ai_Go(info->pl_id,&entrypoint);
					gphase=24;					
			} 
			break;
		case 10:							//moving to place the bomb
			SC_P_GetPos(info->pl_id,&vec);
			if (SC_IsNear3D(&vec,&wirebombplace,1.5f)){
				SC_P_Ai_Stop(info->pl_id);
				SC_P_DoAnim(info->pl_id, SAPPERANIM);
				gphase=11;
			}
			break;
		case 11:							//waiting for anim to end
			break;
		case 12:							//runing for cover
			SC_P_GetPos(info->pl_id,&vec);
			if (SC_IsNear3D(&vec,&initialplace,2)){
					SC_P_Ai_SetMovePos(info->pl_id, SC_P_AI_MOVEPOS_LIE);
					P_Battle(info->pl_id);
			}			
		case 13:							//waiting for bomb to explode on place	- STUPID!!!!
			bombtimer-=info->elapsed_time;
			if (bombtimer<0){
				SC_DoExplosion(&wirebombplace,2);
				P_Script(info->pl_id);
				SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
				SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
				SC_P_Ai_Go(info->pl_id,&wirebombplace);
				gphase=15;				
			}
			break;
		case 15:
			SC_P_GetPos(info->pl_id,&vec);
			if (SC_IsNear3D(&vec,&wirebombplace,2)){
				/*c_Vector3 movdir;
				SC_P_GetPos(info->pl_id,&vec);
				vec.z+=1;
				movdir.z=grenadetarget.z-vec.z+1;
				movdir.y=grenadetarget.y-vec.y;
				movdir.x=grenadetarget.x-vec.x;
				movdir.x*=1.5f;
				movdir.y*=1.5f;
				SC_Item_Create2(148,&vec,&movdir);
				//SC_DoExplosion(&grenadetarget,2);
				bombtimer=1;
				gphase=17;*/
				SC_P_Ai_Stop(info->pl_id);
				SC_P_DoAnim(info->pl_id,THROWANIM);
				gphase=16;				
			}
			break;
		case 16:								//throwing the grenade	- unused
			break;
		case 17:								//throwing the grenade	- unused
			break;
		case 18:
			bombtimer-=info->elapsed_time;
			if (bombtimer<0){
				P_Script(info->pl_id);
				SC_P_Ai_SetMoveMode(info->pl_id,SC_P_AI_MOVEMODE_RUN);
				SC_P_Ai_SetMovePos(info->pl_id,SC_P_AI_MOVEPOS_STAND);
				SC_P_Ai_Go(info->pl_id,&bridgeplace);				
				gphase=20;
			}			
			break;
		case 20:							//runing to place the bridge
			SC_P_GetPos(info->pl_id,&vec);
			if (SC_IsNear3D(&vec,&bridgeplace,1)){
					SC_P_Ai_Stop(info->pl_id);
					SC_P_DoAnim(info->pl_id, SAPPERANIM);
					gphase=22;
			}
			break;
		case 22:							//waiting to the end of bridgeplacing			
			break;
		case 24:							//repeated running to initplace
			SC_P_GetPos(info->pl_id,&vec);
			if (SC_IsNear3D(&vec,&initialplace,2)){
				SC_P_Ai_Go(info->pl_id,&entrypoint);
				gphase=25;
			}
			break;
		case 25:							//running to the entrypoint
			SC_P_GetPos(info->pl_id,&vec);
			if (SC_IsNear3D(&vec,&entrypoint,2)||(SC_P_Ai_GetNearestEnemyDist(info->pl_id)<5)){
				P_Battle(info->pl_id);
				gphase=50;
			}		
			break;
		case 50:
			info->next_exe_time=5+frnd(3);
			if (!P_Indanger(info->pl_id)&&!P_IsMoving(info->pl_id)){
				if (GetNearestHumanPos(info->pl_id,&vec)){
					Pmode_Attack(info->pl_id);
					moving=TRUE;
					SC_P_Ai_Go(info->pl_id, &vec);
					vec.x+=frnd(10);
					vec.y+=frnd(10);
				} else {
					member=SC_P_Ai_GetNearestEnemy(info->pl_id);
					if (member){
						SC_P_GetPos(member,&vec);
						Pmode_Attack(info->pl_id);
						moving=TRUE;
						SC_P_Ai_Go(info->pl_id, &vec);
						vec.x+=frnd(10);
						vec.y+=frnd(10);
					}
					
				}
			} else if (moving&&(rand()%2)) {
				moving=FALSE;
				SC_P_Ai_Stop(info->pl_id);
			}
			break;
		}
		//SC_message("aftertimer");
		break;
	}
	//SC_message("before exit");
	return -1;
}