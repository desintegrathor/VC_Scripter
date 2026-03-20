#include <inc/maxovo/!max_defs.h>

#define ENABLE_IN_MODE_COUNT	1
char	*ENABLE_IN_MODE[ENABLE_IN_MODE_COUNT] =	{	"CTF"	};

int	ScriptMain_obj_control(s_SC_OBJ_info *info, ...);
int	ScriptMain_flag_ctf(s_SC_OBJ_info *info, ...);

#define		INCLUDE_COUNT					2
p_fce_main	INCLUDE_FCE_CALL[INCLUDE_COUNT];

void MAX_SRC_init_fce() {
	INCLUDE_FCE_CALL[0] = ScriptMain_obj_control;
	INCLUDE_FCE_CALL[1] = ScriptMain_flag_ctf;
}

#include <inc/maxovo/!max_extern_script.h>
#include <inc\maxovo\!max_multiplayer_object_control.cxx>
#include <inc\maxovo\!max_uni_flag_ctf.cxx>

int ScriptMain(s_SC_OBJ_info *info) {

#ifdef MAX_EXTERN_SCRIPT_H
	if ((info->message == SC_OBJ_MSG_INIT) || (info->message == SC_OBJ_MSG_JUSTLOADED)) 
		MAX_SRC_init_fce();

	MAX_SCR_run_scripts(info, &MAX_UNI_object_status);
#endif

	return TRUE;
}