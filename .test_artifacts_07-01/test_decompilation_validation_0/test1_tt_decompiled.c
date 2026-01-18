#include <inc\sc_global.h>
#include <inc\sc_def.h>

int _init(s_SC_NET_info *info) {
    int n;
    int side;
    int sideB;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;

    return FALSE;
}

int func_0050(float param_0) {
    int data_;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;

    goto block_3; // @57
    block_3:
    if (!tmp1) {
        data_ = tmp2;
    } else {
        SC_MP_EndRule_SetTimeLeft(data_, tmp5);
        SC_MP_LoadNextMap();
        return TRUE;
        SC_MP_LoadNextMap();
        return TRUE;
        SC_message("EndRule unsopported: %d", tmp);
        return FALSE;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0119(void) {
    int local_1;  // Auto-generated

    int idx;
    int m;
    int n;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp6;
    s_SC_MP_EnumPlayers tmp5;

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!tmp2) {
        return tmp4;
    } else {
        tmp5 = SC_ggf(400);
        tmp5 = 1106247680;
        return tmp5;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0155(void) {
    int local_1;  // Auto-generated

    int idx;
    int m;
    int n;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_MP_EnumPlayers tmp6;

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!tmp2) {
        tmp6 = tmp5;
        tmp6 = 1084227584;
        tmp6 = 1092616192;
        return tmp6;
    } else {
        tmp6 = SC_ggf(401);
        tmp6 = 1092616192;
        return tmp6;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0213(void) {
    int local_1;  // Auto-generated

    int idx;
    int m;
    int n;
    int side;
    int side2;
    int side3;
    int side4;
    int sideB;
    int tmp1;
    s_SC_MP_EnumPlayers tmp;

    SC_MP_SRV_GetAtgSettings(&local_1);
    if (!side2) {
        return side4;
    } else {
        tmp = SC_ggf(402);
        tmp = 1139802112;
        return tmp;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0249(void) {
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    SC_sgi(GVAR_SIDE0FRAGS, tmp1);
    SC_sgi(GVAR_SIDE1FRAGS, tmp3);
    return FALSE;
}

int func_0264(float param_0) {
    int idx;
    int tmp;
    int tmp1;
    int tmp2;
    int tmp3;

    tmp1 = tmp;
    if (!tmp2) {
        tmp1 = 1092616192;
        SC_sgf(504, gMissionTime);
        SC_ggi(505);
        SC_sgi(505, tmp3);
    } else {
        return FALSE;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0334(int param_0) {
    int tmp;

    goto block_46; // @343
    block_46:
    goto block_48; // @348
    block_48:
    return FALSE;
}

int func_0498(int param_0, int param_1) {
    int idx;
    int m;
    int tmp;
    int tmp1;

    tmp = 0;
    tmp1 = 0;
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0752(int param_0) {
    int idx;
    int local_1;
    int local_7;
    int n;
    int side;
    int side2;
    int side3;
    int side4;
    int side5;
    int sideB;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp11;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    s_SC_MP_EnumPlayers local_;
    s_SC_P_getinfo player_info;

    SC_MP_SRV_GetAutoTeamBalance();
    if (!local_7) {
        local_ = SC_MP_SRV_GetTeamsNrDifference(1);
        return 7;
        SC_P_GetInfo(param_0, &player_info);
        local_1 = 1;
        local_1 = 0;
        return 7;
        SC_MP_SRV_P_SetSideClass(param_0, local_1, tmp5);
        abl_list[tmp11] = param_0;
        tmp11 = tmp10;
        return 7;
    } else {
        return 7;
    }
    return 0;  // FIX (06-05): Synthesized return value
}

int func_0852(void) {
    int idx;
    int k;
    int local_1;
    int local_265;
    int local_266;
    int local_267;
    int tmp;
    int tmp1;
    int tmp10;
    int tmp2;
    int tmp3;
    int tmp4;
    int tmp5;
    int tmp6;
    int tmp7;
    int tmp8;
    int tmp9;
    s_SC_MP_EnumPlayers enum_pl;
    s_SC_MP_EnumPlayers local_;
    s_SC_P_getinfo local_2;

    SC_MP_SRV_GetAutoTeamBalance();
    if (!local_267) {
        local_ = SC_MP_SRV_GetTeamsNrDifference(tmp6);
        return 267;
        local_1 = 0;
        local_2 = tmp3;
        local_1 = 1;
        local_2 = tmp5;
        local_265 = 64;
        SC_MP_EnumPlayers(&enum_pl, &local_265, local_1);
        return 267;
        rand();
        tmp9 = tmp8;
        tmp10 = tmp9;
        return local_2;
    } else {
        return 267;
    }
    return 0;  // FIX (06-05): Synthesized return value
}