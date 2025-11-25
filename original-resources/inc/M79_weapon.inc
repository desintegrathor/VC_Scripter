
#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\tmg\utils.h>
#include <inc\tmg\math.h>
#include <inc\tmg\weapons\M79.h>


void *ptc[2];
void *nod[5];
void *wnod;

int i;

dword ammo;
void *MainProjectile;
void *Projectile;
c_Vector3 ProjectileDir;
s_SC_OBJ_dynamic Dyn;

#define SPEED				25.0f

dword manm[3];

BOOL gclear=TRUE;

int ScriptMain(s_SC_WEAP_info *info){
	s_SC_FlyOffCartridge cart;
	s_SC_NOD_transform trans;
	c_Vector3 p1, p2, vec;
	char txt[32];

	switch(info->event_type){


		case SC_WEAP_EVENTTYPE_INIT:
		
				manm[0] = SC_MANM_Create("G\\WEAPONS\\VVH_M79\\fpv\\M79_reload.manm");
				if (!manm[0]) SC_message("M79_reload.manm not found");
				
				manm[1] = SC_MANM_Create("G\\WEAPONS\\VVH_M79\\fpv\\M79_shooting.manm");
				if (!manm[1]) SC_message("M79_shooting.manm not found");
				
				manm[2] = SC_MANM_Create("G\\WEAPONS\\VVH_M79\\fpv\\M79_reload_lie.manm");
				if (!manm[2]) SC_message("M79_reload_lie.manm not found");
				
				//wnod = info->obj;
				ptc[0] = SC_NOD_Get(info->obj,"^PTC_01");
				if (!ptc[0]) SC_message("m79: Dummy ^PTC_01 not found");
					
				ptc[1] = SC_NOD_Get(info->obj,"^PTC_02");
				if (!ptc[1]) SC_message("m79: Dummy ^PTC_02 not found");
				
				nod[0] = SC_NOD_Get(info->obj,"Hlaven");
				nod[1] = SC_NOD_Get(info->obj,"naboj_prazdny");
				nod[2] = SC_NOD_Get(info->obj,"Pojistka");
				nod[3] = SC_NOD_Get(info->obj,"Kohoutek");
				nod[4] = SC_NOD_Get(info->obj,"naboj_plny");
				MainProjectile = SC_NOD_GetNoMessage_Entity("M79_Projectile_0");
				Projectile = SC_NOD_GetNoMessage(MainProjectile, "Sphere01");
				break;
				
		case SC_WEAP_EVENTTYPE_RELEASE:

				for (i=0;i<3;i++) 
					if (manm[i]){
						SC_MANM_Release(manm[i]);
						manm[i] = 0;
					}

				break;
		
		case SC_WEAP_EVENTTYPE_SET:

				switch(info->anim_id){

					case SC_WEAP_INFO_ANIM_ID_RELOAD:// reload
						
		  				if ((info->prev_time<0.21)&&(info->anim_time>=0.21)) SC_SND_PlaySound3D(10916,NULL);
		  				if ((info->prev_time<1.20)&&(info->anim_time>=1.20)) SC_SND_PlaySound3D(10917,NULL);
		  				if ((info->prev_time<1.60)&&(info->anim_time>=1.60)) SC_SND_PlaySound3D(10273,NULL);
		  				if ((info->prev_time<1.65)&&(info->anim_time>=1.65)) {
		  					cart.weap_type = info->weap_type;
							cart.from = nod[1];

							cart.dir.x = 0.0f + frnd(0.0f);
							cart.dir.y = 0.0f + frnd(0.0f);
							cart.dir.z = 0.0f + frnd(0.0f);
								
							cart.add_rot.x =  frnd(10.0f);
							cart.add_rot.y =  frnd(10.0f);
							cart.add_rot.z =  frnd(10.0f);

							SC_FPV_FlyOffCartridge(&cart);
		  				}
		  				if ((info->prev_time<2.50)&&(info->anim_time>=2.50)) SC_SND_PlaySound3D(10393,NULL);
		  				if ((info->prev_time<3.15)&&(info->anim_time>=3.15)) SC_SND_PlaySound3D(10394,NULL);
		  				if ((info->prev_time<3.23)&&(info->anim_time>=3.23)) SC_SND_PlaySound3D(10915,NULL);

						if (info->cur_phase != 2){
							SC_MANM_Set(manm[0],0,nod[0],info->anim_time);
							SC_MANM_Set(manm[0],1,nod[1],info->anim_time);
							SC_MANM_Set(manm[0],2,nod[2],info->anim_time);
												
							if ((info->prev_time<0.65)&&(info->anim_time>=0.65)) {
								SC_SND_PlaySound3D(10392,NULL);
								SC_CreatePtc_Ext(5,ptc[1],0.0f,0.0f,0.8f,1.0f);
							}
						
			  									
							gclear=TRUE;
						}
						else{
							SC_MANM_Set(manm[2],0,nod[0],info->anim_time);
							SC_MANM_Set(manm[2],1,nod[1],info->anim_time);
							SC_MANM_Set(manm[2],2,nod[2],info->anim_time);
												
							if ((info->prev_time<0.65)&&(info->anim_time>=0.65)) {
								SC_SND_PlaySound3D(10392,NULL);
								SC_CreatePtc_Ext(5,ptc[1],0.0f,0.0f,0.8f,1.0f);
							}
						
							gclear=TRUE;
						}													
						break;

					case SC_WEAP_INFO_ANIM_ID_SHOOT:
						
						SC_MANM_Set(manm[1],0,nod[3],info->anim_time);
						
						if ((info->prev_time<=0.0f)&&(info->anim_time>=0.0f)){				
							SC_CreatePtc_Ext(5,ptc[0],0.05f,0.015f,1.0f,1.0f);
							SC_NOD_GetTransform(ptc[0], &trans);
							SC_NOD_GetWorldPos(ptc[0], &p1);
							SC_NOD_GetWorldPos(ptc[1], &p2);
							//vec = VectorCross(&p2, &p1);
							vec = VectorEquation(&p2, &p1);
							vec = VectorNormalize(&vec);
							trans.loc.x = p1.x + (vec.x * 0.5f);
							trans.loc.y = p1.y + (vec.y * 0.5f);
							trans.loc.z = p1.z + (vec.z * 0.5f);
							trans.rot.x = vec.x;
							trans.rot.y = vec.y;
							trans.rot.z = vec.z;
							//SC_NOD_SetTransform(MainProjectile, &trans);
							
							
							//sprintf(txt, "X: %f Y: %f Z: %f", vec.x, vec.y, vec.z);
							//ammo = SC_Item_Create2(59, &info->pos, &trans.rot);
       					//SC_message(txt);
       					//SC_DOBJ_SetFrozenFlag(Projectile, FALSE);
       					
       					SC_sgf(GVAR_M79_AMMO_DIR_X, vec.x);
       					SC_sgf(GVAR_M79_AMMO_DIR_Y, vec.y);
       					SC_sgf(GVAR_M79_AMMO_DIR_Z, vec.z);
       					SC_sgf(GVAR_M79_AMMO_POS_X, trans.loc.x);
       					SC_sgf(GVAR_M79_AMMO_POS_Y, trans.loc.y);
       					SC_sgf(GVAR_M79_AMMO_POS_Z, trans.loc.z);
       					SC_sgi(GVAR_M79_AMMO_STATUS, M79_STATUS_FIRED);
       					/*Dyn.velocity.x = vec.x * SPEED;
							Dyn.velocity.y = vec.y * SPEED;
							Dyn.velocity.z = vec.z * SPEED;
							Dyn.rot_speed = 0.0f;
							Dyn.rot_axis.x = 0.0f;
							Dyn.rot_axis.y = 0.0f;
							Dyn.rot_axis.z = 1.0f;
							SC_DOBJ_SetFrozenFlag(Projectile, FALSE);
							SC_NOD_AddDynamic(MainProjectile, "Sphere01", &Dyn);
							*/
							gclear=TRUE;
						}

						break;
						
					case SC_WEAP_INFO_ANIM_ID_HIDE:
						if ((info->prev_time<0.1)&&(info->anim_time>=0.1)) SC_SND_PlaySound3D(10958,NULL);
						break;
						
					case SC_WEAP_INFO_ANIM_ID_TAKE:
					
						if ((info->prev_time<0.1)&&(info->anim_time>=0.1)) SC_SND_PlaySound3D(10272,NULL);

						break;

					default:
						
						if (gclear){
							gclear=FALSE;
							SC_MANM_Set(manm[0],0,nod[0],0);
							SC_MANM_Set(manm[0],1,nod[1],0);
							SC_MANM_Set(manm[0],2,nod[2],0);
							
							SC_MANM_Set(manm[1],0,nod[3],0);
						}
							
						
						break;

				}// switch(info->anim_id)


			break;// SC_WEAP_EVENTTYPE_SET

	}// switch(info->event_type)
				

	return 0;

}// int ScriptMain(s_SC_WEAP_info *info)
