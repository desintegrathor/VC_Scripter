
#include <inc\sc_global.h>
#include <inc\sc_def.h>

void *ptc[2];
void *bodak;


int ScriptMain(s_SC_WEAP3pv_info *info){	
	s_SC_FlyOffCartridge cart;
	c_Vector3 vec;

	switch(info->event_type){

		case SC_WEAP3PV_EVENTTYPE_INIT:
						
				ptc[0] = SC_NOD_Get(info->obj,"^PTC_01");
				ptc[1] = SC_NOD_Get(info->obj,"^PTC_02");
				/*
				bodak = SC_NOD_Get(info->obj,"bodak_lod1");
				
				if (info->cur_bayonet & 0x80000000){
				  SC_NOD_Hide(bodak,FALSE);
			   }
			   else
				  SC_NOD_Hide(bodak,TRUE);
				*/
				break;

		case SC_WEAP3PV_EVENTTYPE_RELOAD:

				//SC_NOD_GetPivotWorld(ptc[0],&vec);		
				//SC_SND_PlaySound3D(2573,&vec);
				SC_SND_PlaySound3Dpl(10392, info->pl_id, 0);
				break;

		case SC_WEAP3PV_EVENTTYPE_SHOT:
			
			SC_CreatePtc_Ext(5,ptc[0],0.0f,0.0f,1.0f,1.0f);
			SC_CreatePtc_Ext(174,ptc[1],0.0f,0.0f,0.6f,1.5f);

			cart.weap_type = info->weap_type;							
			cart.from = ptc[1];

			cart.dir.x = 1.3f + frnd(0.3f);
			cart.dir.y = 0.0f + frnd(0.2f);
			cart.dir.z = 1.2f + frnd(0.3f);
								
			cart.add_rot.x =  frnd(10.0f);
			cart.add_rot.y =  frnd(10.0f);
			cart.add_rot.z =  frnd(10.0f);
	
			SC_FPV_FlyOffCartridge(&cart);
			
		break;
		
		case SC_WEAP3PV_EVENTTYPE_SETBAYONET:
			/*
			if (info->cur_bayonet & 0x80000000){
//				SC_SND_PlaySound3Dpl(10272,info->pl_id,0);
//				SC_SND_PlaySound3Dpl(4110,info->pl_id,0);
				SC_NOD_Hide(bodak,FALSE);
			}
			else
//				SC_SND_PlaySound3Dpl(10272,info->pl_id,0);
//				SC_SND_PlaySound3Dpl(4111,info->pl_id,0);
				SC_NOD_Hide(bodak,TRUE);
			*/
			break;
				

	}// switch(info->event_type)
				

	return 0;

}// int ScriptMain(s_SC_WEAP_info *info)
