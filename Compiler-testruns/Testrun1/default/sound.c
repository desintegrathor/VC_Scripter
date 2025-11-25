
#include <inc\sc_global.h>

int ScriptMain(s_SC_SOUND_info *info){

	switch(info->message){

		case SC_SOUND_MESSAGE_INIT:

			//SC_SND_SetHearableRatio(0.85f);
			//SC_SND_Ambient_Play(617);

			break;

	}// switch(info->message)

    return 1;


}// int ScriptMain(s_SC_SOUND_info *info)
