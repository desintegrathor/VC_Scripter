
#include <inc\sc_global.h>
#include <inc\sc_def.h>

void *car;

int ScriptMain(s_SC_OBJ_info *info){
	void *nod,*susp,*wheel;	
	s_SC_Car_AddWheel winfo;
	s_SC_Car_Init cinfo;
	s_SC_Car_AddEntry einfo;
	float fl_arr1[8];
	float fl_arr2[8];
	float fl_arr3[6];
	float fl_arr4[8];
	float ride_height;
	dword i;

	switch(info->event_type){
		case SC_OBJ_INFO_EVENT_INIT:			

			nod = SC_NOD_Get(info->master_nod,"gaz_interier");
			
			cinfo.master_nod = info->master_nod;
			
			cinfo.steeringwheel_nod = SC_NOD_Get(info->master_nod,"volant_LOD01");
			cinfo.steeringwheel_max_rot = 1.5f;

			cinfo.steer_max = 0.4f;	
			cinfo.steer_speed = 1.5f;
			cinfo.steer_backspeed = 5.0f;
			
			cinfo.steer_max_mult_at10mpersec = 0.6f;
			cinfo.steer_speed_mult_at10mpersec = 0.4f;
			cinfo.steer_backspeed_mult_at10mpersec = 1.0f;

			cinfo.steer_curse[0] = 0.0f;
			cinfo.steer_curse[1] = 0.05f;
			cinfo.steer_curse[2] = 0.1;
			cinfo.steer_curse[3] = 0.2f;
			cinfo.steer_curse[4] = 0.3f;
			cinfo.steer_curse[5] = 0.5f;
			cinfo.steer_curse[6] = 0.7f;
			cinfo.steer_curse[7] = 0.8f;
			cinfo.steer_curse[8] = 0.9f;
			cinfo.steer_curse[9] = 0.95f;
			cinfo.steer_curse[10] = 1.0f;
			
			cinfo.brake_power = 3500.0f;

			cinfo.eng_max_revs = 3000;
			cinfo.eng_freewheel_revs = 600;
			cinfo.eng_revs_slowdown = 900.0f;
			cinfo.eng_min_revs = 1800.0f;
			cinfo.eng_val_steps = 7;
			cinfo.eng_Nm = fl_arr1;	
			cinfo.eng_kW = fl_arr2;

			fl_arr1[0] = 450;
			fl_arr1[1] = 460;
			fl_arr1[2] = 470;
			fl_arr1[3] = 480;
			fl_arr1[4] = 490;
			fl_arr1[5] = 500;
			fl_arr1[6] = 490;			

			for (i=0;i<8;i++)
				fl_arr1[i] *= 0.4f;

			fl_arr2[0] = 35;
			fl_arr2[1] = 40;
			fl_arr2[2] = 50;
			fl_arr2[3] = 55;
			fl_arr2[4] = 60;
			fl_arr2[5] = 50;
			fl_arr2[6] = 40;
			

			for (i=0;i<8;i++)
				fl_arr2[i] *= 0.5f;

			cinfo.trns_delay = 1.2f;
			cinfo.trns_gears = 4;
			cinfo.trns_gear = fl_arr3;
			
			fl_arr3[0] = -4.5f;
			fl_arr3[1] = 4.3f;
			fl_arr3[2] = 2.5f;
			fl_arr3[3] = 1.3f;
			fl_arr3[4] = 0.9f;
			fl_arr3[5] = 0.5f;

			// apply final ratio
			for (i=0;i<cinfo.trns_gears;i++)
					cinfo.trns_gear[i] *= 5.5f;

			

			susp = SC_NOD_Get(info->master_nod,"enginesound");
			SC_NOD_GetPosInOtherSpace(nod,susp,&cinfo.eng_sound_pos);

		
			// engine sound

			cinfo.eng_snd_id = 1900;

			cinfo.eng_freqmult_revs1 = 400;
			cinfo.eng_freqmult_revs2 = 3000;
			cinfo.eng_freqmult_1 = 0.5f;
			cinfo.eng_freqmult_2 = 2.0f;
			cinfo.eng_sound_volume = fl_arr4;

			fl_arr4[0] = 1.0f;
			fl_arr4[1] = 1.0f;
			fl_arr4[2] = 1.0f;
			fl_arr4[3] = 1.0f;
			fl_arr4[4] = 1.0f;
			fl_arr4[5] = 1.0f;
			fl_arr4[6] = 1.0f;			



			car = SC_CAR_Create(nod,&cinfo);

			// init wheels
			
			
			winfo.body_vector.x = 0.0f;
			winfo.body_vector.y = 0.0f;
			winfo.body_vector.z = -1.0f;
			
			winfo.spring_tmin = 0.05f;
			winfo.spring_tmax = 0.15f;
			winfo.spring_t = 0.15f;

/*
			winfo.spring_tmin = 1.1f;
			winfo.spring_tmax = 2.52f;
			winfo.spring_t = 0.2f;
*/
			winfo.spring_absorber = 1.0f;
			winfo.spring_looser = 3.0f;
			winfo.spring_rate = 55000.0f;
			winfo.wheel_radius = 0.40f;

			winfo.wheel_fr_min = 2.0f;
			winfo.wheel_fr_dspd =0.05*3.14f;

			winfo.wheel_friction =10.0f;
			winfo.wheel_aspd = 0;
			winfo.wheel_with_drive =TRUE;
			winfo.steering = TRUE;

			winfo.left_side = TRUE;
			
			ride_height = 0.2f;
			
//predni napravy

			winfo.ptc_v0_mult = 1.0f;
			winfo.ptc_v1_mult = 1.0f;
		//leva
			susp = SC_NOD_Get(info->master_nod,"zaves_LF");
			SC_NOD_GetPosInOtherSpace(nod,susp,&winfo.body_point);
			wheel = SC_NOD_Get(info->master_nod,"wheel_FL_LOD01");
			winfo.spring_tmin = 0.10f - ride_height;
			winfo.spring_tmax = 0.25f - ride_height;
			winfo.spring_t = 0.15f - ride_height;
			winfo.spring_rate = 43000.0f;
			winfo.spring_looser = 5.0f;
			winfo.spring_absorber = 0.5f;
			SC_CAR_WheelAdd(car,wheel,&winfo);
		
		//prava	
			winfo.left_side = FALSE;
			
			susp = SC_NOD_Get(info->master_nod,"zaves_RF");
			SC_NOD_GetPosInOtherSpace(nod,susp,&winfo.body_point);
			wheel = SC_NOD_Get(info->master_nod,"wheel_FR_LOD01");
			winfo.spring_tmin = 0.10f - ride_height;
			winfo.spring_tmax = 0.25f - ride_height;
			winfo.spring_t = 0.15f - ride_height;
			winfo.spring_rate = 43000.0f;
			winfo.spring_looser = 5.0f;
			winfo.spring_absorber = 0.5f;
			SC_CAR_WheelAdd(car,wheel,&winfo);

//zadni napravy
			winfo.ptc_v0_mult = 1.0f;
			winfo.ptc_v1_mult = 2.5f;
		//leva
			winfo.left_side = TRUE;
			winfo.steering = FALSE;
			winfo.wheel_with_drive = TRUE;

			susp = SC_NOD_Get(info->master_nod,"zaves_LR");
			SC_NOD_GetPosInOtherSpace(nod,susp,&winfo.body_point);
			wheel = SC_NOD_Get(info->master_nod,"wheel_RL_LOD01");
			winfo.spring_tmin = 0.10f - ride_height;
			winfo.spring_tmax = 0.25f - ride_height;
			winfo.spring_t = 0.15f - ride_height;
			winfo.spring_rate = 43000.0f;
			winfo.spring_looser = 5.0f;
			winfo.spring_absorber = 0.5f;
			SC_CAR_WheelAdd(car,wheel,&winfo);
			
		//prava	
			winfo.left_side = FALSE;
			winfo.wheel_with_drive = TRUE;

			susp = SC_NOD_Get(info->master_nod,"zaves_RR");
			SC_NOD_GetPosInOtherSpace(nod,susp,&winfo.body_point);
			wheel = SC_NOD_Get(info->master_nod,"wheel_RR_LOD01");
			winfo.spring_tmin = 0.10f - ride_height;
			winfo.spring_tmax = 0.25f - ride_height;
			winfo.spring_t = 0.15f - ride_height;
			winfo.spring_rate = 43000.0f;
			winfo.spring_looser = 5.0f;
			winfo.spring_absorber = 0.5f;
			SC_CAR_WheelAdd(car,wheel,&winfo);

// init driver

			CLEAR(einfo);

			susp = SC_NOD_Get(info->master_nod,"entry");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.entry);

			susp = SC_NOD_Get(info->master_nod,"pos");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.target);

			susp = SC_NOD_Get(info->master_nod,"view");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.view);

			einfo.entry_dist = 1.0f;
			einfo.entry_name_nr = 2105;
			einfo.exit_name_nr = 2107;
			einfo.function = SC_CAR_ENTRY_FUNC_DRIVER;
			einfo.stg_dir = "M151_1";
			einfo.can_shoot = FALSE;


			einfo.min_rx = DEG_TO_RAD(-40.0f);
			einfo.max_rx = DEG_TO_RAD(60.0f);
			einfo.min_rz = DEG_TO_RAD(-120.0f);
			einfo.max_rz = DEG_TO_RAD(120.0f);
					
			SC_CAR_EntryAdd(car,&einfo);
/*			
// init spolujezdec
			susp = SC_NOD_Get(info->master_nod,"pasentry");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.entry);

			susp = SC_NOD_Get(info->master_nod,"paspos");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.target);

			susp = SC_NOD_Get(info->master_nod,"pasview");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.view);

			einfo.entry_dist = 1.0f;
			einfo.entry_name_nr = 2106;
			einfo.exit_name_nr = 2107;
			einfo.function = SC_CAR_ENTRY_FUNC_SEAT;
			einfo.stg_dir = "M151_2";
			einfo.can_shoot = TRUE;

			einfo.min_rz = -DEG_TO_RAD(120.0f);
			einfo.max_rz = DEG_TO_RAD(120.0f);			
			einfo.min_rx = -DEG_TO_RAD(50.0f);
			einfo.max_rx = DEG_TO_RAD(50.0f);			

			einfo.shoot_min_rz = DEG_TO_RAD(-30.0f);
			einfo.shoot_max_rz = DEG_TO_RAD(155.0f);
			einfo.min_rz = einfo.shoot_min_rz;
			einfo.max_rz = einfo.shoot_max_rz;

			einfo.switch_3pv_anim_dir = 5;
					
			SC_CAR_EntryAdd(car,&einfo);

// init spolujezdec vzdu vpravo
			susp = SC_NOD_Get(info->master_nod,"pas2entry");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.entry);

			susp = SC_NOD_Get(info->master_nod,"pas2pos");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.target);

			susp = SC_NOD_Get(info->master_nod,"pas2view");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.view);

			einfo.entry_dist = 1.0f;
			einfo.entry_name_nr = 2106;
			einfo.exit_name_nr = 2107;
			einfo.function = SC_CAR_ENTRY_FUNC_SEAT;
			einfo.stg_dir = "M151_4";
			einfo.can_shoot = TRUE;

			einfo.min_rz = -DEG_TO_RAD(120.0f);
			einfo.max_rz = DEG_TO_RAD(120.0f);			
			einfo.min_rx = -DEG_TO_RAD(50.0f);
			einfo.max_rx = DEG_TO_RAD(50.0f);			

			einfo.shoot_min_rz = DEG_TO_RAD(-269.0f);
			einfo.shoot_max_rz = DEG_TO_RAD(90.0f);
			einfo.min_rz = einfo.shoot_min_rz;
			einfo.max_rz = einfo.shoot_max_rz;

			einfo.switch_3pv_anim_dir = 3;
			

			SC_CAR_EntryAdd(car,&einfo);
			
// init spolujezdec vzdu vlevo
			susp = SC_NOD_Get(info->master_nod,"pas3entry");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.entry);

			susp = SC_NOD_Get(info->master_nod,"pas3pos");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.target);

			susp = SC_NOD_Get(info->master_nod,"pas3view");
			SC_NOD_GetPosInOtherSpace(nod,susp,&einfo.view);

			einfo.entry_dist = 1.0f;
			einfo.entry_name_nr = 2106;
			einfo.exit_name_nr = 2107;
			einfo.function = SC_CAR_ENTRY_FUNC_SEAT;
			einfo.stg_dir = "M151_3";
			einfo.can_shoot = TRUE;

			einfo.shoot_min_rz = DEG_TO_RAD(-90.0f);
			einfo.shoot_max_rz = DEG_TO_RAD(269.0f);
			einfo.min_rz = einfo.shoot_min_rz;
			einfo.max_rz = einfo.shoot_max_rz;

			einfo.switch_3pv_anim_dir = 7;
			
			SC_CAR_EntryAdd(car,&einfo);

			SC_CAR_SetAirResistance(car,10.0f,5.0f,20.0f);
*/
			break;
	}// switch(info->event_type)
	

	return FALSE;

}// int ScriptMain(s_OBJ_info *info)