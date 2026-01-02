//
//	Coop.c	-- BP
//	Beny
//


#include <inc\gLevel.h>

//definiton for End rule: Bomb exploded
//#define		BOMB_TIME				30.0f
//#define		BOMB_LEVELDONE_MASK		0x00000001
//#define		NUM_BOMBS				1

//float		gTimeBomb[NUM_BOMBS];
//float		gBombTimer[NUM_BOMBS] = {BOMB_TIME};

//definiton for End rule: Alive players reached some place (LZ etc.)
//#define		NUM_ENDPLACES			1
//s_sphere	gEndPlace[NUM_ENDPLACES];

dword InitEndPlaces()
{
	dword	cur = 0;


//	GetDummyPos("EndPlace", &gEndPlace[cur].pos);
//	gEndPlace[cur++].rad = 30.0f;

//	GetDummyPos("", &gEndPlace[cur].pos);
//	gEndPlace[cur++].rad = 10.0f;

	return cur;
}




//#include	<inc\CoopBomb.inc>
#include "..\..\..\..\..\ini\Multiplayer\scripts\Coop_Uni.inc"
