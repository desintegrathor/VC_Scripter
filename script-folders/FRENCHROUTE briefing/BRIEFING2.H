#define CURRENTMISSION	MISSION_FRENCHROUTEA


//Movie Text Definiton	- definice textu kter˝ se zobrazÌ p¯i z·bÏru na diorama

#define MovieText1		8814
#define MovieText2		8815
#define MovieText3		0

#define MovieTextTime	7.5f			//kolik sekund bude zobrazen˝ movie text - pozor, aù se nezaËne p¯ekr˝vat se samotn˝m briefingem!


//briefing definitions


#define BRIEFINGLINES		75				//kolik ¯·dek celkem


OneLine Briefing[BRIEFINGLINES]={
//	Ëas		rozkaz 				param1				param2(ËÌslo textu nebo jmÈno animace
//			(SAY, CAMERA,PLAYANIM)		(kdo, kter· kamera) 

	0,		CAMERA,			C_Hawk,				0,
	1.6f,		PLAYANIM,			NHUT,				NHUTREST,
	0,		SAY,				HAWKINS,			8573,
	
	0.8f,		CAMERA,			C_RosenZM,				0,
	0.8f,		PLAYANIM,			ROSENFIELD,			ROSENFIELDSRTSPK,
	0,		SAY,				ROSENFIELD,			8574,
	
	1,		CAMERA,			C_Hawk,				0,
	0.5f,		SAY,				HAWKINS,			8575,
	
	0,		CAMERA,			C_HawkToHorn,			0,
	0.7f,		PLAYANIM,			BRONSON,			BRONSONOTOC,
	2,		CAMERA,			C_Hornster,			0,
	4,		PLAYANIM,			BRONSON,			BRONSONOTOC,
	0,		SAY,				HORNSTER,			8576,
	
	0,		CAMERA,			C_Bronson,			0,
	0,		SAY,				BRONSON,			8577,
	
	0.2f,		PLAYANIM,			BRONSON,			BRONSONOTOC,
	0,		CAMERA,			C_BronsToHorn,			0,
	0,		SAY,				HORNSTER,			8578,

	0.3f,		PLAYANIM,			BRONSON,			BRONSONSRTSPK,
	0,		SAY,				BRONSON,			8579,	

	0,		PLAYANIM,			DEFORT,			DEFORTOTOC,
	1,		CAMERA,			C_Defort,			0,
	0,		SAY,				DEFORT,				8580,	

	0,		CAMERA,			C_Hornster,			0,
	0,		PLAYANIM,			HORNSTER,			HORNSTERSRTSPK,
	0,		SAY,				HORNSTER,			8581,

	0,		CAMERA,			C_Rosen,				0,
	0,		SAY,				ROSENFIELD,			8582,

	0,		SAY,				ROSENFIELD,			8583,

	0,		CAMERA,			C_Hawk,				0,
	0,		SAY,				HAWKINS,			8584,

	1,		CAMERA,			C_Defort,				0,
	1,		PLAYANIM,			DEFORT,			DEFORTOTOC,
	0,		SAY,				DEFORT,				8585,	

	0,		CAMERA,			C_Crocker,				0,
	
	0,		SAY,				CROCKER,			8586,	

	0.8f,		CAMERA,			C_RRmap1,				0,
	0,		SAY,				ROSENFIELD,			8587,

	1,		CAMERA,			C_Hawk,				0,
	0,		SAY,				HAWKINS,			8588,

	1,		CAMERA,			C_Rosen,				0,
	3,		CAMERA,			C_AllFrontTR,			0,
	5,		PLAYANIM,			NHUT,				NHUTREST2,
	0,		SAY,				ROSENFIELD,			8589,

	0,		CAMERA,			C_HawkZM,			0,
	0,		SAY,				ROSENFIELD,			8590,

	0.5f,		PLAYANIM,			HAWKINS,			HAWKINSSRTSPK,
	0,		SAY,				HAWKINS,			8591,

	1,		CAMERA,			C_Rosen,				0,
	0,		SAY,				ROSENFIELD,			8592,

	0,		CAMERA,			C_Rosen,			0,
	0,		SAY,				ROSENFIELD,			8593,

	0.5f,		CAMERA,			C_Hawk,				0,
	0,		SAY,				HAWKINS,			8594,

	1,		CAMERA,			C_Rosen,			0,
	0,		SAY,				ROSENFIELD,			8595,

	0,		CAMERA,			C_Hornster,			0,
	3.5f,		PLAYANIM,			BRONSON,			BRONSONOTOC,
	4,		CAMERA,			C_Bronson,			0,
	4.5f,		PLAYANIM,			HORNSTER,			HORNSTERSRTSPK,
	0,		SAY,				HORNSTER,			8596,
	
	0.5f,		PLAYANIM,			BRONSON,			BRONSONSRTSPK,
	0,		SAY,				BRONSON,			8597,

	0,		CAMERA,			C_Celek,			0,
	1,		PLAYANIM,			ROSENFIELD,			ROSENFIELDSRTSPK,
	0,		SAY,				ROSENFIELD,			8598

};




#define HIDEBOOTS