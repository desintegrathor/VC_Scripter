//Master briefing H

#include <inc\sc_level.h>

//camera definitions
#define CAMERAS_COUNT			10

#define CAMERA_DioramaBase 		"g\\camanims\\camera\\Dioramabase.anm"				//camera 0
#define CAMERA_CelekMistnost 		"g\\camanims\\camera\\briefing\\BR1.anm"				//camera 1
#define CAMERA_RosenfieldDetail 		"g\\camanims\\camera\\briefing\\BR2.anm"				//camera 2
#define CAMERA_RosenfieldPoloProfil		 "g\\camanims\\camera\\briefing\\BR3.anm"				
#define CAMERA_HawkinsPoloDetail		 "g\\camanims\\camera\\briefing\\BR4.anm"

#define CAMERA_TabuleDetail1		 "g\\camanims\\camera\\briefing\\BRdet1.anm"
#define CAMERA_TabuleDetail2		 "g\\camanims\\camera\\briefing\\BRdet2.anm"
#define CAMERA_TabuleDetail3		 "g\\camanims\\camera\\briefing\\BRdet3.anm"

#define CAMERA_NastenkaMapa		 "g\\camanims\\camera\\briefing\\BRdet5.anm"
#define CAMERA_NastenkaDetail		 "g\\camanims\\camera\\briefing\\BRdet6.anm"				//camera 9


//viewanim definitions


char *cameras[CAMERAS_COUNT]={CAMERA_DioramaBase,CAMERA_CelekMistnost,CAMERA_RosenfieldDetail,CAMERA_RosenfieldPoloProfil,
	CAMERA_HawkinsPoloDetail,CAMERA_TabuleDetail1,CAMERA_TabuleDetail2,CAMERA_TabuleDetail3,CAMERA_NastenkaMapa,
	CAMERA_NastenkaDetail};


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


//who is who

#define HAWKINS 	0
#define NHUT 	1
#define CROCKER	2
#define BRONSON 	3
#define DEFORT	4
#define HORNSTER 5
#define ROSENFIELD 6
 

//definice použitelných animací


#define ANIMATIONS_COUNT 4

//první animace (index 0) je vždy "" - žádná animace

char *animations[ANIMATIONS_COUNT]={"",
	"g\\characters\\anims\\movies\\Briefing-sitting.stg",
	"g\\characters\\anims\\movies\\Briefing-standing.stg",
	"g\\characters\\anims\\movies\\S007 prestavka utierapot.stg",
};

#define HAWKINS_STATIV  		1
#define NHUT_STATIV  		1
#define CORCKER_STATIV  		1
#define BRONSON_STATIV  		1
#define DEFORT_STATIV  		1
#define HORNSTER_STATIV  		1
#define ROSENFIELD_STATIV  	2
#define TESTANIM			3

typedef struct {
	int who;					//kdo to øíká (definice HAWKINS-ROSENFIELD)
	int playeranim;				//jakou animaci pøitom pøehrává, pokud 0, pøehrává se dál defaultní stativ, jinak animace z  promìnné animations
	int what;					//co øíká - èíslo z lokalizátoru
	float pause;				//jak dlouho se má èekat než se pustí hláška
	
	int camera;				//èíslo první kamery
	int camera2;				//èíslo druhé kamery
	int camera3;				//èíslo druhé kamery (mìla by být statická, pøehrává se cyklicky až do dalšího texty),
	float cameraflip;				//za kolik sekund se mají kamery pøepnout z 1 na 2, pokud 0, nepoužívá se 
	float cameraflip2;				//za kolik sekund se mají kamery pøepnout z 2 na 3, pokud 0, nepoužívá se 
} OneLine;
