#include <inc\sc_global.h>
#include <inc\sc_def.h>
#include <inc\!max_defs_mp.h>

BOOL	isActive = TRUE;

int ScriptMain(s_SC_ScriptHelper_info *info) {
	int i, j;
	dword pl_id;
	c_Vector3 vec;
	s_SC_MP_EnumPlayers enum_pl[64];
	dword num;

	info->next_exe_time = 1.0;

	switch(info->event_type) {
	case SC_SCRHELPER_EVENTTYPE_INIT:
		isActive = TRUE;
		break;

	case SC_SCRHELPER_EVENTTYPE_RELEASE:
		break;

	case SC_SCRHELPER_EVENTTYPE_TIMETICK:
		if ((!isActive) && (SC_ggi(GVAR_RESPAWN_GROUP) == 0)) isActive = TRUE;
		if (isActive) {
			num = 64;
			i = 0;
			if (SC_MP_EnumPlayers(enum_pl, &num, SC_MP_ENUMPLAYER_SIDE_ALL)) {
				for (j=0; j<num; j++) {
					if (enum_pl[j].status != SC_MP_P_STATUS_INGAME) continue;
					SC_P_GetPos(enum_pl[j].id, &vec);
					if (SC_2VectorsDist(&info->sph.pos, &vec) < info->sph.rad) {
						if (enum_pl[j].side == OPP_SIDE) return 0;
						i++;
					}
				}
				if (i > 0) {
					isActive = FALSE;
					SC_MP_ScriptMessage(100, GROUP_NUMBER);
				}
			}
		}
		break;

	}// switch(info->event_type)
	return FALSE;

}// int ScriptMain(s_OBJ_info *info)