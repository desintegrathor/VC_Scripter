
int GetTeamPeaceMode(){
	int i,p;
	for (i=1;i<6;i++) 
		if (!isdead(0,0,i)){
			p=SC_P_Ai_GetPeaceMode(GetUS(i));
			if (p!=SC_P_AI_PEACEMODE_HOLD) return p;
		}
	return SC_P_AI_PEACEMODE_HOLD;
}


void ResetTeamPeaceMode(){
		SC_Ai_SetPeaceMode(0,0,Getpeacemode());
}


