//Master briefing H 2

#include <inc\sc_level.h>

//COMMANDS

#define SAY	0			//øekni
#define CAMERA	1			//pøepni kameru
#define PLAYANIM	2			//zahrej animaci panáka
#define SETSTATIV 3			//pøepni stativ panáka na animaci x





//camera definitions
#define CAMERAS_COUNT			39

#define CAMERA_DioramaBase 		"g\\camanims\\camera\\Dioramabase.anm"				//camera 0
#define CAMERA_CelekMistnost 		"g\\camanims\\camera\\briefing\\BR1.anm"				//camera 1
#define CAMERA_RosenfieldDetail 		"g\\camanims\\camera\\briefing\\BR2.anm"				//camera 2
#define CAMERA_RosenfieldPoloProfil		 "g\\camanims\\camera\\briefing\\BR3.anm"				
#define CAMERA_HawkinsPoloDetail		 "g\\camanims\\camera\\briefing\\BR4.anm"

//#define CAMERA_Hornster			"g\\camanims\\camera\\briefing\\BR1.anm"
//#define CAMERA_Defort			"g\\camanims\\camera\\briefing\\BR1.anm"
//#define CAMERA_Bronson			"g\\camanims\\camera\\briefing\\BR1.anm"
//#define CAMERA_Hawkins			"g\\camanims\\camera\\briefing\\BR1.anm"
//#define CAMERA_Nhut			"g\\camanims\\camera\\briefing\\BR1.anm"

#define CAMERA_Hornster			"g\\camanims\\camera\\briefing\\br4hornster.anm"
#define CAMERA_Defort			"g\\camanims\\camera\\briefing\\br5defort.anm"
#define CAMERA_Bronson			"g\\camanims\\camera\\briefing\\br6bronson.anm"
#define CAMERA_Hawkins			"g\\camanims\\camera\\briefing\\br7Hawkins.anm"
#define CAMERA_Nhut			"g\\camanims\\camera\\briefing\\br8nhut.anm"

#define CAMERA_TabuleDetail1		 "g\\camanims\\camera\\briefing\\BRdet1.anm"
#define CAMERA_TabuleDetail2		 "g\\camanims\\camera\\briefing\\BRdet2.anm"
#define CAMERA_TabuleDetail3		 "g\\camanims\\camera\\briefing\\BRdet3.anm"

#define CAMERA_NastenkaMapa		 "g\\camanims\\camera\\briefing\\BRdet5.anm"
#define CAMERA_NastenkaDetail		 "g\\camanims\\camera\\briefing\\BRdet6.anm"				//camera 9
#define CAMERA_NastenkaDetail2		 "g\\camanims\\camera\\briefing\\BRdet4.anm"				
#define CAMERA_NastenkaDetail2		 "g\\camanims\\camera\\briefing\\BRdet6.anm"				
//#define CAMERA_NastenkaDetail3		 "g\\camanims\\camera\\briefing\\BRdet7.anm"				
#define CAMERA_NastenkaDetail3		 "g\\camanims\\camera\\briefing\\BRdet6.anm"				
#define CAMERA_AllFront			"g\\camanims\\camera\\briefing\\BRallfront.anm"
#define CAMERA_AllNd			"g\\camanims\\camera\\briefing\\BRallND.anm"
#define CAMERA_Hawk3c			"g\\camanims\\camera\\briefing\\3CanHawkins.anm"
#define CAMERA_Hawk3cZM			"g\\camanims\\camera\\briefing\\3CanHawkinsZM.anm"
#define CAMERA_Crocker			"g\\camanims\\camera\\briefing\\BR9Crocker.anm"
#define CAMERA_AllFrontTR			"g\\camanims\\camera\\briefing\\BRallfrontTR.anm"
#define CAMERA_NhutZM			"g\\camanims\\camera\\briefing\\BR8NhutZM.anm"
#define CAMERA_3canyonsmap		"g\\camanims\\camera\\briefing\\3Canmap1.anm"
#define CAMERA_3canyonsmap2		"g\\camanims\\camera\\briefing\\3Canmap2.anm"
#define CAMERA_3canyonsmap3		"g\\camanims\\camera\\briefing\\3Canmap3.anm"
#define CAMERA_RosenZM			"g\\camanims\\camera\\briefing\\BRrosenZM.anm"
#define CAMERA_RRmap1			"g\\camanims\\camera\\briefing\\RRmap1.anm"
#define CAMERA_DefToHorn			"g\\camanims\\camera\\briefing\\BRDefToHorn.anm"
#define CAMERA_BronsToHorn		"g\\camanims\\camera\\briefing\\BRBronsToHorn.anm"
#define CAMERA_RosenZM			"g\\camanims\\camera\\briefing\\BRrosenZM.anm"	
#define CAMERA_HawkToHorn		"g\\camanims\\camera\\briefing\\BRHawkToHorn.anm"							
#define CAMERA_Hornview			"g\\camanims\\camera\\briefing\\Hornview.anm"	
#define CAMERA_HawkZM			"g\\camanims\\camera\\briefing\\BRHawkZM.anm"	
#define CAMERA_Nightmap1			"g\\camanims\\camera\\briefing\\Nightmap1.anm"
#define CAMERA_Nightmap2			"g\\camanims\\camera\\briefing\\Nightmap2.anm"
#define CAMERA_Nightmap3			"g\\camanims\\camera\\briefing\\Nightmap3.anm"
#define CAMERA_Strmap1			"g\\camanims\\camera\\briefing\\STRmap1.anm"

//viewanim definitions


char cameras[CAMERAS_COUNT][50]={CAMERA_DioramaBase,CAMERA_CelekMistnost,CAMERA_RosenfieldDetail,CAMERA_RosenfieldPoloProfil,
	CAMERA_HawkinsPoloDetail,CAMERA_TabuleDetail1,CAMERA_TabuleDetail2,CAMERA_TabuleDetail3,CAMERA_NastenkaMapa,
	CAMERA_NastenkaDetail,CAMERA_Hornster,CAMERA_Defort,CAMERA_Bronson,CAMERA_Hawkins,CAMERA_Nhut,
	CAMERA_NastenkaDetail2,CAMERA_NastenkaDetail3,CAMERA_AllFront,CAMERA_AllNd,CAMERA_Hawk3c,CAMERA_Hawk3cZM,
	CAMERA_Crocker,CAMERA_AllFrontTR,CAMERA_NhutZM,CAMERA_3canyonsmap,CAMERA_3canyonsmap2,CAMERA_3canyonsmap3,
	CAMERA_RosenZM,CAMERA_RRmap1,CAMERA_DefToHorn,CAMERA_BronsToHorn,CAMERA_RosenZM,CAMERA_HawkToHorn,
	CAMERA_Hornview,CAMERA_HawkZM,CAMERA_Nightmap1,CAMERA_Nightmap2,CAMERA_Nightmap3,CAMERA_Strmap1
	};


//definice pro systém a pro zadávání
#define C_Diorama	0
#define C_Celek	1
#define C_Rosen	2
#define C_Rosen2	3
#define C_Hawk	4
#define C_Tabule1	5
#define C_Tabule2	6
#define C_Tabule3	7
#define C_Mapa	8
#define C_NDetail	9
#define C_Hornster	10
#define C_Defort	11
#define C_Bronson	12
#define C_Hawkins	13
#define C_Nhut	14

#define C_NDetail2	15
#define C_NDetail3	16

#define C_AllFront	17
#define C_AllND	18
#define C_Hawk3c	19
#define C_Hawk3cZM	20
#define C_Crocker		21
#define C_AllFrontTR	22
#define C_NhutZM		23
#define C_3CanonsMap	24
#define C_3CanonsMap2	25
#define C_3CanonsMap3	26
#define C_RosenZM	27
#define C_RRmap1	28
#define C_DefToHorn	29
#define C_BronsToHorn	30
#define C_RosenZM	31
#define C_HawkToHorn	32
#define C_Hornview	33
#define C_HawkZM		34
#define C_Nightmap1	35
#define C_Nightmap2	36
#define C_Nightmap3	37
#define C_Strmap1		38
//who is who

#define HAWKINS 	0
#define NHUT 	1
#define CROCKER	2
#define BRONSON 	3
#define DEFORT	4
#define HORNSTER 5
#define ROSENFIELD 6
 

//definice použitelných animací


#define ANIMATIONS_COUNT 27

//první animace (index 0) je vždy "" - žádná animace

char animations[ANIMATIONS_COUNT][80]={"",
	"g\\characters\\anims\\movies\\Briefing-sitting.stg",
	"g\\characters\\anims\\movies\\Briefing-standing.stg",
	"g\\characters\\anims\\movies\\S007 prestavka utierapot.stg",
	"g\\characters\\anims\\movies\\BRhwak.stg",
	"g\\characters\\anims\\movies\\BRhwak zdravi.stg",
	"g\\characters\\anims\\movies\\BRrosen stat.stg",
	"g\\characters\\anims\\movies\\BRrosen ukayuje hawka.stg",
	"g\\characters\\anims\\movies\\BRrosen ukazuje na mapu.stg",
	"g\\characters\\anims\\movies\\BRnhut zdravi sediac.stg",	
	"g\\characters\\anims\\movies\\BR_Bronson kratka rec.stg",
	"g\\characters\\anims\\movies\\BR_Crocker kratka mluva.stg",
	"g\\characters\\anims\\movies\\BR_Defort kratka rec.stg",
	"g\\characters\\anims\\movies\\BR_Hawkings kratka mluva.stg",
	"g\\characters\\anims\\movies\\BR_Hornster kratka rec.stg",
	"g\\characters\\anims\\movies\\BR_Nhut kratka mluva.stg",
	"g\\characters\\anims\\movies\\BR_Rosenfield kratka mluva.stg",
	"g\\characters\\anims\\movies\\BR_BronsonOTOC.stg",	
	"g\\characters\\anims\\movies\\BR_CrockerOTOC.stg",
	"g\\characters\\anims\\movies\\BR_DefortOTOC.stg",
	"g\\characters\\anims\\movies\\BR_CrockerREST.stg",
	"g\\characters\\anims\\movies\\BR_DefortREST.stg",
	"g\\characters\\anims\\movies\\BR_NhutREST.stg",
	"g\\characters\\anims\\movies\\BR_NhutREST2.stg",
	"g\\characters\\anims\\movies\\BR_RosenHawkotocka.stg"	,		
	"g\\characters\\anims\\movies\\BR_Hawknarosenotocka.stg"	
	};



#define HAWKINS_STATIV  		1
#define NHUT_STATIV  		1
#define CORCKER_STATIV  	1
#define BRONSON_STATIV  		1
#define DEFORT_STATIV  		1
#define HORNSTER_STATIV  	1
#define ROSENFIELD_STATIV  	2
#define TESTANIM			3
#define BRHWAK			4
#define BRHWAKZDRAVI		5
#define BRROSENSTAT		6
#define BRROSENUKAZUJEHAWKA	7
#define BRROSENUKAZUJEMAPU	8
#define BRNHUTZDRAVISEDI	9
#define BRONSONSRTSPK		10
#define CROCKERSRTSPK		11
#define DEFORTSRTSPK		12
#define HAWKINSSRTSPK		13
#define HORNSTERSRTSPK	14
#define NHUTSRTSPK		15
#define ROSENFIELDSRTSPK	16
#define BRONSONOTOC		17
#define CROCKEROTOC		18
#define DEFORTOTOC		19
#define CROCKERREST		20
#define DEFORTREST		21
#define NHUTREST		22
#define NHUTREST2		23
#define ROSOTOC		24
#define HAWKOTOC		25

typedef struct {
	float timer;
	int command;
	int param1;
	int param2;
} OneLine;
