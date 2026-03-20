
#include <inc\sc_global.h>
#include <inc\sc_def.h>

void *gCartPos;
void *muzzle_nod;

int ScriptMain(s_SC_OBJ_info *info){	
	s_SC_MWP_Create cinfo;
	s_SC_FlyOffCartridge cart;


	switch(info->event_type){
		case SC_OBJ_INFO_EVENT_INIT:						

			CLEAR(cinfo);

			cinfo.master_nod = info->master_nod;
			cinfo.weap_type = 34;
			cinfo.use_info_txt_id = 54700;
			cinfo.exit_info_txt_id = 54701;
			
			cinfo.nod_rotate_x = SC_NOD_Get(info->master_nod,"besa_lod1");
			gCartPos = SC_NOD_Get(info->master_nod,"^PTC_1");               //naboje - opravit nod
			cinfo.nod_rotate_z = SC_NOD_Get(info->master_nod,"mount");
			cinfo.nod_rotate_last = cinfo.nod_rotate_x;
			cinfo.nod_fpv_camera = SC_NOD_Get(info->master_nod,"fpv");
			muzzle_nod = SC_NOD_Get(info->master_nod,"muzzle");
			cinfo.nod_muzzle = muzzle_nod;
			cinfo.nod_entry = SC_NOD_Get(info->master_nod,"entry");
			cinfo.nod_base = SC_NOD_Get(info->master_nod,"base");
			
			cinfo.nod_active_pos = cinfo.nod_rotate_x;
			cinfo.active_rad = 0.5f;
			cinfo.active_dist = 2.0f;

			cinfo.rotate_zmin = -DEG_TO_RAD(45.0f);
			cinfo.rotate_zmax = DEG_TO_RAD(45.0f);
			cinfo.rotate_xmin = -DEG_TO_RAD(5.0f);
			cinfo.rotate_xmax = DEG_TO_RAD(20.0f);
			cinfo.rotate_speed = 0.3f;

			cinfo.flash_rot_step = 2.0f*PI/5.0f;
			
			cinfo.anim_dir = "Besa";
			
			SC_MWP_Create(&cinfo);
			
		case SC_OBJ_INFO_EVENT_JUSTLOADED:
			
			break;

		case SC_OBJ_INFO_EVENT_RELEASE:
			
			break;

		case SC_OBJ_INFO_EVENT_HIT:			
			break;

		case SC_OBJ_INFO_EVENT_DOTICK:

						
			break;

		case SC_OBJ_INFO_EVENT_MOUNTEDSHOT:

			cart.weap_type = 1;
			cart.from = gCartPos;

			cart.dir.x = -2.5f + frnd(0.2f);
			cart.dir.y = 0.0f + frnd(0.2f);
			cart.dir.z = 1.0f + frnd(0.2f);
						
			cart.add_rot.x =  frnd(15.0f);
			cart.add_rot.y =  frnd(15.0f);
			cart.add_rot.z =  frnd(15.0f);

			SC_FPV_FlyOffCartridge(&cart);
	
			SC_CreatePtc_Ext(5,muzzle_nod,0.0f,0.0f,1.5f,1.0f);
			SC_CreatePtc_Ext(174,gCartPos,0.0f,0.0f,0.6f,1.5f);

			break;

	}// switch(info->event_type)


	return FALSE;

}// int ScriptMain(s_OBJ_info *info)