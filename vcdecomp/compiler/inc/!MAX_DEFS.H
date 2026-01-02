// single player defs

#define B_SNIPER_GO				2000
#define B_DANGER				2001

#define GO_TIMER				5.0f

#define	PA_NONE					0
#define	PA_WAIT					1
#define	PA_LOOP					2


char *GetUSRndIni() {
	switch (rand()%6) {
		case 0: return "ini\\players\\net_us_sf1.ini"; break;
		case 1: return "ini\\players\\net_us_sf2.ini"; break;
		case 2: return "ini\\players\\net_us_sf3.ini"; break;
		case 3: return "ini\\players\\net_us_bangs.ini"; break;
		case 4: return "ini\\players\\net_us_crocker.ini"; break;
		case 5: return "ini\\players\\net_us_douglas.ini"; break;
	}
	return "net_us_sf1.ini";
}

#define	MAX_WEAPS	4
dword us_weap[MAX_WEAPS] = {1,11,17,21};

int GetUSRndWeapon()
{
	return us_weap[ rand()%MAX_WEAPS ];
}

float abs(float num) {
	if (num > 0) return num; else return -num;
}

typedef struct {
	c_Vector3	wp;
	dword		action;
	dword		data;					//action related
	char		*anim;
}s_pendl;

void Hide(char *tmpstr) {
	SC_DUMMY_Set_DoNotRenHier(tmpstr,TRUE);
}

void Show(char *tmpstr) {
	SC_DUMMY_Set_DoNotRenHier(tmpstr,FALSE);
}