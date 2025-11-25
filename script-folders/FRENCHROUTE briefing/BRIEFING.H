#define CURRENTMISSION	MISSION_FRENCHROUTEA

//Movie Text Definiton	- definice textu kter˝ se zobrazÌ p¯i z·bÏru na diorama

#define MovieText1		0
#define MovieText2		0
#define MovieText3		0

#define MovieTextTime	3.5f			//kolik sekund bude zobrazen˝ movie text - pozor, aù se nezaËne p¯ekr˝vat se samotn˝m briefingem!


//briefing definitions

#define BRIEFINGLINES		26					//kolik textov˝ch ¯·dek celkem


OneLine Briefing[BRIEFINGLINES]={
//		kdo, jak· animace		co, s jak˝m zpoûdÏnÌm	kamera1,kamera2,kamera3		p¯epnutÌ z 1 na 2, p¯epnutÌ z 2 na 3

		HAWKINS,0,		8573,0,			C_Hawk,0,0,			0,0,
		ROSENFIELD,0,		8574,2,			C_Rosen,C_Tabule3,C_Tabule2,	2,2,
		HAWKINS,TESTANIM,	8575,0,			C_Hawk,0,0,			0,0,
		HORNSTER,0,		8576,0,			C_Celek,0,0,			0,0,
		BRONSON,0,		8577,0,			C_Celek,0,0,			0,0,
		HORNSTER,0,		8578,0,			C_Celek,0,0,			0,0,
		BRONSON,0,		8579,0,			C_Celek,0,0,			0,0,
		DEFORT,0,		8580,0,			C_Celek,0,0,			0,0,
		HORNSTER,0,		8581,0,			C_Celek,0,0,			0,0,
		ROSENFIELD,0,		8582,0,			C_Rosen,0,0,			0,0,
		ROSENFIELD,0,		8583,0,			C_Rosen,0,0,			0,0,
		HAWKINS,0,		8584,0,			C_Hawk,0,0,			0,0,
		DEFORT,0,		8585,0,			C_Celek,0,0,			0,0,
		CROCKER,0,		8586,0,			C_Celek,0,0,			0,0,
		ROSENFIELD,0,		8587,0,			C_Mapa,0,0,			0,0,
		HAWKINS,0,		8588,0,			C_Hawk,0,0,			0,0,
		ROSENFIELD,0,		8589,0,			C_Rosen,0,0,			0,0,
		ROSENFIELD,0,		8590,0,			C_Tabule1,0,0,			0,0,
		HAWKINS,0,		8591,0,			C_Hawk,0,0,			0,0,
		ROSENFIELD,0,		8592,0,			C_Rosen,0,0,			0,0,
		ROSENFIELD,0,		8593,0,			C_Rosen2,0,0,			0,0,
		HAWKINS,0,		8594,0,			C_Hawk,0,0,			0,0,
		ROSENFIELD,0,		8595,0,			C_Rosen2,0,0,			0,0,
		HORNSTER,0,		8596,0,			C_Celek,0,0,			0,0,
		BRONSON,0,		8597,0,			C_Celek,0,0,			0,0,
		ROSENFIELD,0,		8598,0,			C_Rosen2,0,0,			0,0
};



