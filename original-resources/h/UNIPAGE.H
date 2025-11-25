//
//
//

#ifndef __UNIPAGE_H__
#define	__UNIPAGE_H__


//#include <inc\sc_global.h>
#include <inc\sc_def.h>



//types
typedef	char			CHAR;
typedef	unsigned short	WCHAR;
typedef	int				INT;
typedef	unsigned char	BOOL;
typedef unsigned long	DWORD;
typedef DWORD			HANDLE;


#define	NULL		0
#define	FALSE		0
#define	TRUE		1





//macros
#define CLEAR(a) ZeroMem(&a,sizeof(a))			//clear memory




//alignment
#define	UP_ALIGN_LEFT		0
#define	UP_ALIGN_RIGHT		1
#define	UP_ALIGN_CENTER		2

//text parameters flags
#define	UP_TEXT_POS			0x00000001			//x,y
#define	UP_TEXT_COLOR		0x00000002			//color
#define	UP_TEXT_STRING		0x00000004			//str
#define	UP_TEXT_SIZE		0x00000008			//w,h
#define	UP_TEXT_FLAGS		0x00000010			//flags
#define	UP_TEXT_MARGINS		0x00000020			//rect
#define	UP_TEXT_ALL			(UP_TEXT_POS | UP_TEXT_COLOR | UP_TEXT_STRING | UP_TEXT_SIZE | UP_TEXT_FLAGS | UP_TEXT_MARGINS)

//picture parameters flags
#define	UP_PICTURE_POS		0x00000001
#define	UP_PICTURE_FLAGS	0x00000002
#define	UP_PICTURE_FILE		0x00000004
#define	UP_PICTURE_ALL		(UP_PICTURE_POS | UP_PICTURE_FLAGS | UP_PICTURE_FILE)


//button parameters flags
#define	UP_BUTTON_POS		0x00000001
#define	UP_BUTTON_STRING	0x00000002
#define	UP_BUTTON_SIZE		0x00000004
#define	UP_BUTTON_BITMAP	0x00000008
#define	UP_BUTTON_FLAGS		0x00000010
#define	UP_BUTTON_ALL		(UP_BUTTON_POS | UP_BUTTON_STRING | UP_BUTTON_SIZE | UP_BUTTON_BITMAP | UP_BUTTON_FLAGS)

//button colors
#define	UP_BUTTON_COL_TEXT		0x00010000		//the following flags are used for text colors of button
#define	UP_BUTTON_COL_BACK		0x00020000		//the following flags are used for background colors of button

#define	UP_BUTTON_COL_NORMAL	0x00000001
#define	UP_BUTTON_COL_PRESSED	0x00000002
#define	UP_BUTTON_COL_HILIGHT	0x00000004



//Index definitions for universal sounding (sound events)
enum GUI_SOUND_INDEX
{
	GUI_SOUND_MENTER,							//Mouse entered into GUI object / select the item
	GUI_SOUND_MLEAVE,							//Mouse leaved the GUI object / deselect the item
	GUI_SOUND_CLICK,							//Click of the mouse or equivalent action from keyboard
	GUI_SOUND_DRAG,								//Drag the item or part of item
	GUI_SOUND_DROP,								//Drop the item
	GUI_SOUND_LASTITEM
};

//button sounds
#define	UP_BUTTON_SND_CLICK		GUI_SOUND_CLICK
#define	UP_BUTTON_SND_MLEAVE	GUI_SOUND_MLEAVE
#define	UP_BUTTON_SND_MENTER	GUI_SOUND_MENTER


//listbox styles
#define	UP_LB_STYLE_SINGLE	 2		//selection
#define	UP_LB_STYLE_EXTENDED 3

//listbox parameters flags
#define	UP_LB_POS			0x00000001
#define	UP_LB_SIZE			0x00000004
#define	UP_LB_FLAGS			0x00000010
#define	UP_LB_ALL			(UP_LB_POS | UP_LB_SIZE | UP_LB_FALGS)

//listbox messages - obsolete
#define	UP_LB_MSG_SELCHD	0x00000001
#define	UP_LB_MSG_DBLCLK	0x00000002

#define	LB_NOSEL			0xEEEEEEEE
#define	LB_ERROR			0xFFFFFFFF

//listbox colors
//...


//
#define	UP_FLAG_BORDER		0x00000001
#define	UP_FLAG_WRAP		0x00000002
#define	UP_FLAG_USEMARGINS	0x00000004

//UP_CTEXT
#define	UP_FLAG_ONNEWPAGE	0x00010000			//the element is forced to be rendered on a beginning of a new (next) page

//release flags
#define	UP_RLS_TPICS		0x00000001			//template pictures
#define	UP_RLS_TTEXTS		0x00000002			//template texts
#define	UP_RLS_CPICS		0x00000004			//continuous pictures
#define	UP_RLS_CTEXTS		0x00000008			//continuous texts
#define UP_RLS_BUTTONS		0x00000010			//buttons
#define UP_RLS_LISTBOXES	0x00000020			//listboxes
#define	UP_RLS_FONTS		0x00000100
#define	UP_RLS_COLUMNS		0x00000200


//colors
#define	UP_COL_TRANSPARENT	0x00000000


//
#define	UP_INITTEMPLATE		0
#define	UP_BUTTON_1			1
#define	UP_BUTTON_2			2




//messages passed to a up script
#define	MSG_INIT			0x00000001		//UniPage init
#define	MSG_INITFONTS		0x00000002		//init of fonts by resolution, should be called before MSG_INIT!

#define	MSG_BTN_CLICK		0x10000001		//button messages
#define	MSG_LB_SELCHD		0x10000010		//listbox messages
#define	MSG_LB_DBLCLK		0x10000011




//predefined callback button IDs
#define	BTN_PREV		1001
#define	BTN_NEXT		1002
#define	BTN_CANCEL		1004
#define	BTN_PRACTISE	1005
#define	BTN_EQUIP		1006
#define	BTN_BRIEFING	1007
#define	BTN_PLAY		1008

//callback listbox IDs
#define	LB_LB01			2001
#define	LB_LB02			2002
#define	LB_LB03			2003


/*
  //moved to sc_def.h

//status saving variables
//alc save
#define	SGI_ALC_SAVE_DOC		3100
#define	SGI_ALC_SAVE_PAGE		3101
//brief save
#define	SGI_BRIEF_SAVE_DOC		3102
#define	SGI_BRIEF_SAVE_PAGE		3103
//diary save
#define	SGI_DIARY_SAVE_DOC		3104
#define	SGI_DIARY_SAVE_PAGE		3105
*/


//Used for button colors
enum GUI_ITEM_INDEX
{
	GUI_ITEM_NORMAL = 0,								//ID to set/get color of face 
	GUI_ITEM_BACK,
	GUI_ITEM_PALEBACK,
	GUI_ITEM_BORDER,
	GUI_ITEM_SELECTED,
	GUI_ITEM_DELETED,
	GUI_ITEM_DISABLED,
	GUI_ITEM_PRESSED,
	GUI_ITEM_HILIGHTED,

	GUI_ITEM_LASTITEM								//Don't remove this line! Add new items ONLY before this line!
};


//forward declaration of classes
struct c_GUI_SystemMaster;
struct c_GUI_BasicObject;
struct c_GUI_UniPage;
struct c_GUI_Button;
struct c_GUIB_Font;
struct c_GUI_Background;


//This struct is passed to a up script every time it's executed. It contains ptr to UniPage, message ID and context params.
typedef struct _s_upInfo {
	struct c_GUI_UniPage	*up;
	DWORD			msg;
	DWORD			param1;
	DWORD			param2;
} s_upInfo; //



//UniPage column definition
typedef struct _s_upColumn
{
	int		posX;
	int		posY;
	int		width;
	int		height;
}s_upColumn; //struct _s_upColumn

//
typedef struct _s_Rect
{
	int		left;
	int		top;
	int		right;
	int		bottom;

} s_Rect; //typedef struct _s_Rect




//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Debriefing ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

typedef struct{

	float	missionTime;				//time in seconds
	DWORD	difficulty;
	DWORD	missionStatus;

	//friendly losses
	DWORD	SF;							//number of KIA
	DWORD	LLDB;
	DWORD	CIDG;
	DWORD	Heli;						//number of damaged
	DWORD	Jeep;

	//statistics
	DWORD	VC;							//x KIA
	DWORD	Gaz;						//damaged
	DWORD	Boobytrap;					//eliminated
	DWORD	Caches;						//secured
	DWORD	Tunnels;
	DWORD	Facilities;
	DWORD	Intelligence;

	//personal statistics
	DWORD	Bangs;						//x KIA
	DWORD	Defort;
	DWORD	Hornster;
	DWORD	Nhut;
	DWORD	Bronson;
	DWORD	Crocker;

}s_SC_DebriefInfo;

//


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Template-page mode ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

//structures
//font
typedef struct _s_upFont{
	CHAR	*name;
	DWORD	size;
	DWORD	weight;
	BOOL	bLoadFromStore;			//if TRUE, the name is used as filename of saved store with font resource, then other params are ignored.
	BOOL	bItalic;

	//private
	struct c_GUIB_Font	*pFont;
} s_upFont; //typedef struct _s_upFont{


//text
typedef struct _s_upText {

	INT		left;
	INT		top;
	INT		right;
	INT		bottom;
	DWORD	flags;					//see UP_TF_? flags
	DWORD	color;
	DWORD	fontID;					//Index of font (see c_GUI_UniPage::CreateFont())
	WCHAR	*str;
} s_upText; //typedef struct _s_upText {



//picture
typedef struct _s_upPicture {

	INT		x;
	INT		y;
	INT		w;
	INT		h;
	DWORD	flags;					//border etc.
	CHAR	*filename;

	//private
	struct c_GUI_Background	*pPicture;

} s_upPicture; //typedef struct _s_upPicture {



//button
typedef struct _s_upButton {

	INT		x;
	INT		y;
	INT		w;
	INT		h;
	DWORD	flags;
	WCHAR	*str;
	CHAR	*bitmap;

	DWORD	ID;						//this button ID is passed to a script

	//private
	struct c_GUI_Button	*pButton;

} s_upButton; //typedef struct _s_upButton {


//ListBox
typedef struct _s_upListBox {

	INT		x;
	INT		y;
	INT		w;
	INT		h;
	DWORD	flags;

	DWORD	ID;						//this ID is passed to a script

	//private
	struct c_GUI_ListBox *pListBox;

} s_upListBox; //typedef struct _s_upListBox {

//
typedef struct _s_uplbParams
{
	DWORD msg;
	DWORD Param1;
} s_uplbParams;	//typedef struct _s_uplbParams



//++++++++++++++++++++++++++++++++++++++++++++++++++++++ Continuous-page mode ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

//
typedef struct _s_upCText 
{
	WCHAR	*str;
	DWORD	fontID;
	DWORD	color;
	DWORD	flags;					//must begin on new page, ...
	s_Rect	rect;					//margins
//	(DWORD	alignment;)

} s_upCText; //typedef struct _s_upCText 

//
typedef struct _s_upCPicture 
{
	CHAR	*filename;
	DWORD	flags;
	DWORD	alignment;

	//private
	struct c_GUI_Background	*pCPicture;

} s_upCPicture; //typedef struct _s_upCPicture 


//
typedef struct _s_UP_GetElement 
{
	INT		nElement;				//index of element
	DWORD	data;					//element-specific data
	DWORD	column;					//index of column
} s_UP_GetElement; //struct s_UP_RenderElement 



//----------------------------------------------------------------------------------------------------------------------------------------


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Definitions +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Parse flags
#define	END				0x00000000
#define	NEXT			0xFFFFFFFF

//Font IDs
#define	TXT1			1			//normal font
#define	TXT2			2			//big bold
#define	TXT3			3			//
#define	TXT4			4
#define	TXT5			5
#define	TXT6			6
#define	TXT7			7
#define	TXT8			8
#define	TXT9			9

#define	PIC				10
#define	BACK			20


//UP element flags
#define	FLG_NEWPAGE			0x00000001		//useful for text and pictures
#define	FLG_BORDER			0x00000002		//for pictures only
#define	FLG_ALIGN_LEFT		0x00000004		//for pictures only - default setting
#define	FLG_ALIGN_RIGHT		0x00000008		//... don't combine FLG_ALIGN_*
#define	FLG_ALIGN_CENTER	0x00000010


//UP element flags (used in debriefing)
#define	SGI_01		0x00010000				//corresponds with SGI_DEBR_01 etc.
#define	SGI_02		0x00020000
#define	SGI_03		0x00040000
#define	SGI_04		0x00080000
#define	SGI_05		0x00100000
#define	SGI_06		0x00200000
#define	SGI_07		0x00400000
#define	SGI_08		0x00800000
#define	SGI_09		0x01000000


//
typedef struct _s_ListDef {
	DWORD	txtID;				//ID of item text
	DWORD	levelID;			//ID of level (od tohohle cisla levelu nahoru je tento text pritomen v seznamu)
} s_ListDef;

//
typedef struct _s_DocDef {
	DWORD	type;				//type of element (text|pic)
	char	*name;				//number of textID or filename (e.g. "#7890" | "UniPage\\pictures\\pic01.tga"); must correspond with type!
	DWORD	flags;				//type-dependent flags (e.g. FLG_NEWPAGE)
} s_DocDef;

//definition of fonts
typedef struct _s_FontDef {
	DWORD	fontID;				//ID of font (e.g. TXT1, TXT2, ...)
	DWORD	resY;				//Y-axis resolution for which is the font assigned
	char	*fontName;			//path to the font resource (e.g. "UniPage\\Fonts\\Courier.ste")
} s_FontDef;

//----------------------------------------------------------------------------------------------------------------------------------------



//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Common script functions ++++++++++++++++++++++++++++++++++++++++++++++++++++

//returns absolute value
DWORD abs(INT n)
{
	if (n > 0)
		return n;

	return -n;
}

//----------------------------------------------------------------------------------------------------------------------------------------





//functions
extern void COM_message(char *xStr,...);
extern char *UTXT_Get(DWORD id);
extern WCHAR *WTXT_Get(DWORD id);
extern void OSI_Set(char *xStr,...);
extern void SC_Debrief_Get(s_SC_DebriefInfo *info);
extern int SC_ggi(DWORD id);
extern void SC_sgi(DWORD id, int a);
extern DWORD W_WStrAnsiToUnicode( WCHAR *pDestinationWStr, char *pSourceStr );

extern void SC_SND_MusicPlay(DWORD MusicID, DWORD StartVolume);



extern void UP_ReleaseData(struct c_GUI_UniPage *up, DWORD flags);

extern int UP_CreateFont(struct c_GUI_UniPage *up, s_upFont *fnt);


//Template mode
extern int UP_CreateText(struct c_GUI_UniPage *up, s_upText *text);
extern BOOL UP_SetTextParams(struct c_GUI_UniPage *up, DWORD index, s_upText *pTextData, DWORD flags);

extern int UP_CreatePicture(struct c_GUI_UniPage *up, s_upPicture *pic);
extern BOOL UP_SetPictureParams(struct c_GUI_UniPage *up, DWORD index, s_upPicture *pPictureData, DWORD flags);

extern int UP_CreateButton(struct c_GUI_UniPage *up, s_upButton *btn);
extern BOOL UP_SetButtonParams(struct c_GUI_UniPage *up, DWORD index, s_upButton *pButtonData, DWORD flags);
extern BOOL UP_HideButton(struct c_GUI_UniPage *up, DWORD index, BOOL bHide);
extern BOOL UP_SetButtonColors(struct c_GUI_UniPage *up, DWORD index, enum GUI_ITEM_INDEX *colors, DWORD flags);
extern BOOL UP_SetButtonOnTop(struct c_GUI_UniPage *up, DWORD index);
extern BOOL UP_SetButtonSound(struct c_GUI_UniPage *up, DWORD index, DWORD sndType, DWORD sndID);



extern DWORD UP_lb_Create(struct c_GUI_UniPage *up, s_upListBox *lb, DWORD style);		//return handle to a listbox
extern DWORD UP_lb_AddString(struct c_GUI_UniPage *up, DWORD handle, char *str);
extern DWORD UP_lb_AddString(struct c_GUI_UniPage *up, DWORD handle, WCHAR *str);
extern BOOL  UP_lb_SetData(struct c_GUI_UniPage *up, DWORD handle, DWORD index, DWORD data);
extern DWORD UP_lb_GetData(struct c_GUI_UniPage *up, DWORD handle, DWORD index);
extern DWORD UP_lb_GetCurSel(struct c_GUI_UniPage *up, DWORD handle);
extern BOOL  UP_lb_SetCurSel(struct c_GUI_UniPage *up, DWORD handle, DWORD index);
extern BOOL  UP_lb_SetColor(struct c_GUI_UniPage *up, DWORD handle, DWORD index, DWORD color);
extern BOOL  UP_lb_UseItemColors(struct c_GUI_UniPage *up, DWORD handle, BOOL bUse);
extern BOOL	 UP_lb_SetHeader(struct c_GUI_UniPage *up, DWORD handle, char *str);
extern BOOL	 UP_lb_SetHeader(struct c_GUI_UniPage *up, DWORD handle, WCHAR *str);


extern BOOL UP_SetStaticBackground(struct c_GUI_UniPage *up, char *filename, DWORD flags);


//Continuous mode
extern int UP_AddText(struct c_GUI_UniPage *up, s_upCText *text);
extern int UP_AddPicture(struct c_GUI_UniPage *up, s_upCPicture *pic);
extern int UP_GetNumPages(struct c_GUI_UniPage *up);
extern int UP_ShowPage(struct c_GUI_UniPage *up, int pageNo);
extern int UP_GetVisiblePage(struct c_GUI_UniPage *up, s_UP_GetElement *se, s_UP_GetElement *ee);
extern int UP_SetVisiblePage(struct c_GUI_UniPage *up, int nElement);	//sets visible page to page which contain specified element
extern void UP_SetClippingRect(struct c_GUI_UniPage *up, s_Rect *pRect);
extern int UP_AddColumn(struct c_GUI_UniPage *up, s_upColumn *col);
extern int UP_SetColumn(struct c_GUI_UniPage *up, DWORD index, s_upColumn *col);

extern void UP_StartLevel(struct c_GUI_UniPage *up);
extern void UP_Cancel(struct c_GUI_UniPage *up);





//Misc
extern int sprintf(char *, const char *, ...);
extern void	W_WStrPrintf( WCHAR *pDest, WCHAR *pSource, ... );
//extern void* memset(void *, int, unsigned int);
extern void ZeroMem(void *, unsigned int);


#endif	//__UNIPAGE_H__

