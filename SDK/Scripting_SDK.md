# INTRODUCTION

This document contains all information about scripting in the PteroEngine for the games Vietcong and Vietcong Fist Alpha you need for creating your own scripts, and also describes few other modding possibilities.

But first, be warned: pteroscripts are based on the standard ANSI C language. They essentialy ARE the ANSI C with the big library exported from the game engine used for the controlling of the game behavior. I won't teach you here how to do standard C codes - if you never did this before, go buy some book about standard C syntax, or download some tutorial from the web - there should be no problem at finding something like this, as C and it's more advanced version C++ are used everywhere and almost for everything. **Note:** javascript and other script languages are based on the C syntax, so this may be a starter for you.

You won't need any hi-tech coder skills, just basic knowledge about C syntax and coding and some text editor. Everything else is included in the Vietcong.

**Note:** this document focuses on the scripts and only touches other spheres of possible modifications. I plan to update this document as often as possible and I will try to improve parts of it which are not clear enough for you.

Check http://www.pterodon.com for new updates.

If you have any questions or problems, post them at Pterodon forum (https://forum.pterodon.cz/index.php) or at the Gathering Forum (http://www.gathering.com/forums/index.php - I have a special thread there in the Beta Map Editor section for the scripts), or send me a mail at shigor@volny.cz.

**Note:** this version is for the 1.60 version of the Vietcong and Fist Alpha - although most of the features can be used for older version, I STRONGLY recommed you upgrade your version. Also unless stated specifically, all future patch above 1.60 version should be compatible with this SDK.


# BASICS OF THE SCRIPTS


## What are the scripts?

Scripts are used to modify and control most of the aspects of the game. They are written in a C like code, which is then compiled and interpreted by the game engine.


## Basic overview of the PteroEngine

Pteroengine contains many types of the scene and game entities, which you can control with the scripts.


### PteroEngine entities

*Scene entities*

Graphical entities are the "stones" from which the game levels are built. You will usually work only with weapon scripts, dynamic objects like helicopters, various clickable object etc., but you will sometimes need to hide or show various pieces of GFX according to the game progress. Pteroengine contains *set of functions for the work with the GFX entities* usable from anywhere in the any script and has also specific type of the object script. Automatically generated animals (birds, butterflies etc) are also in this group.

*SOUND entities*

Sound in the Pteroengine is quite complex. Scripts have access to the *set of functions for working with the sound*, but most of the ingame nature sound (animals, etc) is done by EVENT entities editable in the editor. There is also *specific type of script for the sound settings*, used for setting ambient sounds etc.

*HELPER entities*

Helper entities contain the dummy object which can be used by scripts to get specific position and rotation at any place at the scene. They are also used to link various objects together. There is also specific helper entity called the script helper. It can be used to define spheres in the level, either for player detection, getting the exact position etc. They can have their *own scripts*.

At the uppermost level of the hierarchy, all gfx, sound and helper entities are known as a NODs. Most of the functions accepts the pointer to the NOD as it's main parameter. If you want to work with some object as with dynamic object, it MUST be marked as such in the scene else the game will probably crash.

*GAME entities*

There are two important types of the game entities for the script writer.

*Waypoints* are used to define the path for the AI. Pteroengine contains functions for controlling of the movement, disabling various waypoints etc. Waypoints are most commonly used object for getting the position for the AI or checking the position of the player, as those are the places you can be sure they are accessible by the players.

*Players* are objects used to create the players in the game - either the AI controlled, or controlled by the human player. You can adjust standard recovery position for the player and his initial z rotation in the editor and assign a script to him.

Scripts work with players with pointers to the player in the main memory. Some of the functions are designed to work with generic player (like SC_P_SetPos), some of them only with the players with artificial intelligence (like SC_P_Ai_SetMode) and some of them are working directly with the human player (like SC_PC_GetPos). If you'll call the SC_P_Ai function for the human player, the game will crash! For more information about the AI in the game, refer to the chapter *Overview of the Artificial Intelligence in the PteroEngine.*


### Execution of the scripts

Game engine executes the scripts according their type and the situation, which can be initialization of the scene, it's release, at various callback functions (for example when the speech playing is finished or when the dynamic object was hit) and periodically at the time specified (*level* and *player* scripts) or at each frame rendering (*dynamic objects scripts*). For the exact specification see the detailed description of given type of the script.

In the settings dialog (CTRL+E) there is a possibility to switching of the players and level scripts - useful when you need just to test the scene or try to walk around it. But don't forget to switch them on again!


## Types of the scripts

There are several types of the script. Every script MUST contain the *int ScriptMain()* function. Exact parameters for the every type of the script is specified at the detailed description of the script type.

Most important script (well, it's arguable ;o) is the *Level Script*. It's called at the initialization and release of the scene, at the time specified and during the various callbacks. It also defines a lot of things for other entities, like player sides and groups etc. The level script is usually used to coordinate game during the whole level. Think about it as a master script controlling all others :o). Every game scene MUST have a level script else it won't be executed (unless you specifically disabled execution of the level script in the settings dialog (CTRL+E)). *For detailed description see here.*

*Player script* is the heart of the players in the game. Sometime it just contains information needed to create the player entity in the game, sometimes it contains much more code specific to the mission (it's all up to script writer). *For detailed description see here*.

*Dynamic object script* is the script for anything physical that moves, can be clicked upon, players can ride in etc. Somewhat specific types of the dynamic object scripts are *car scripts*, *ship scripts* and *helicopter scripts*. *For detailed description see here*.

*Sound script* is called just once - after the execution of the level and it is used to set various sound stuff like setting the ambient sounds etc - it's for the comfort of the sound and script designers, so the sound designer can change the sound stuff without bothering the script writer. *For detailed description see here.*

*Multiplayer script* is used to coordinate the multiplayer games, it has code for both the server and the client. *For detailed description see here*.

*Weapon script* is used to handle the sounds and animations of the weapons, both for the FPV (holded by the player) and 3PV view (generic weapon in the game). *For detailed description see here*.

*Script helper script* is a script which can be added to any script helper to simplify the scripting of the game - you can for example prepare simple script for "killsphere", which kills anyone entering the script helper and assign it to various helpers in the level. *For detailed description see here*.

*Unipage scripts* are used to create various text documents, like briefings, debriefings, weapon cards etc. *For detailed description see here*.


### Coordination of the scripts and communication between them

Every object and player has it's own script, so there's a need to communicate between them. Most common way to do so is the use of the *game global variables*. Level script and player's script can receive message using the specialized functions (`SC_P_ScriptMessage` for the player script and `SC_LevScr_Event` for the level script).


## Adding the scripts to the game

*Level* and *sound* scripts are added automatically - they just need to be in the correct place, which is the scripts directory for the current level (so the path to the scripts is something like levels/stream/data/stream/scripts) or at the dev/UniPage_Scripts (guess what goes there - yes, unipages).

The *multiplayer scripts* are usually placed in the ini/multiplayer/scripts directory, but they can be anywhere, as the path to the script is defined in the map definition file. For user maps they should be placed in the script subdirectory of the level.

*Weapon scripts* are at the directory with the weapon models and are too loaded automatically.

*Object scripts* can either have their scripts at the same place where the .bes file containing the object exists (the .c file must have same name as the object, for example if there's an object called box.bes in one directory and there's also a file called box.c, it will be loaded automatically), or there is a possibility to assign any object script to any object in the level.c during the initialization of the scene using the `SC_SetObjectScript` function. This is usually used for the objects which need specific scripts for the specific levels, like helicopter script. In this case the script can be located anywhere, you just have to assign correct path to it.

*Player scripts* are usually located in the scripts directory for the current level and they are assigned by hand in the editor - click on the player and at the properties tab assign the correct script. Alternatively there is a possibility to create and execute other player scripts directly from the running script.

*Script helper scripts* can be located anywhere - same as player scripts, choose the helper, click on his properties and assign the correct script.


## Writing your own scripts

You can use any text editor you like for the writing of the scripts, including the windows notepad.exe, but I recommend you use some editor with programming features, like showing the source code using the C color convention or editor designed especially for the C programming, like very good editor included in Microsoft Visual Studio. Very good choice is shareware editor called Ultraedit (available at the http://www.ultraedit.com). The source code in the file .c is compiled to the .scr file, which is then used by the game, so every time you finish the writing or modifying of the script you should try to compile it first before trying it in the game - having uncompilable scripts in the game scene may cause crashes. Ultraedit and other similar programs allows the definition of the tool for compiling, so it's good idea set the compiler as one of these tools.


## Include files and headers

There is one standard include file called sc_global.h in the dev/compiler/inc directory. It contains all exported functions, definition and structures from the engine to the script for normal scripts. DO NOT ALTER THIS FILE! Unipages has one special header UniPage.h.

There is also one include file which should be shared by all scripts called sc_def.h. It contains definitions valid for all scripts - especially definitions of the *global variables*.

You can use the header or include files as much as you wish to. It is often useful and efficient way to do the scripts - prepare some libraries or standard include files and then just change some parameters for them. For example if you have 30 Vietnamese superkillers in the level, create include file called vcsuperkiller.inc and place all the code there. Then include it in every script for each killer and just change some parameters. So the superkiller11.c will look just like this:


```c
#define MEMBERID 11
#define GROUP 0
#define WEAPON 2
#include "vcsuperkiller.inc"
```

You will save a lot of time when the need to change something in the vcsuperkillers behavior arises. You'll just change the include file and all is done. Comparing to manually rewriting every of 30 scripts just because you decided the VC shouldn't be so precise with their guns it's lightning fast.

There are few useful include files already prepared. For the list of them *see here*.


## Using the script compiler

The script compiler is located at the DEV/COMPILER directory of the Vietcong. It consist of four programs - scmp.exe, spp.exe, scc.exe and sasm.exe. You can compile any script by executing the scmp.exe with three parameters: name of your script, name for the compiled script and name for the header file. I am using simple .bat file for the test compilings called the compile.bat:


```c
"scmp" "%1" "test.scr" "test.h" if exist spp.err uedit32 spp.err if exist scc.err uedit32 scc.err if exist sasm.err uedit32 sasm.err
```

Batch file calls the compiler and tells him to save the finished script in the test.scr (as I don't need the compiled script file yet, I just need to try if it's compilable). Compiling process is the same as with any standard C compiler. SCMP calls the preprocessor spp.exe, which prepares the .c for the actual compiler scc. SCC produces the assembler like code, which is then compiled into the .SCR file readable by pteroengine script system. If any of those three programs encounter an error, it creates error file and batch file automatically opens it in my favorite editor, so I can see where I missed the semicolon or forget the correct syntax for some function.

There can be only one running instance of the compiler at one time, as the programs are transmiting data between themselves using the temporary files in this directory. So executing a compiler while it already runs (either when the game compiles the scripts before running the game level, or if the compiler wasn't yet finished with compiling of the previous scripts) will probably made the compiler report error.

Everytime this happens, press the ctrl+alt+delete and look at the running processes - if there's any scmp.exe or any other compiler file running, kill it. The delete any temporary files in the compiler directory, leaving just the .exe files and any files you added there personally. Then try to compile the file again.

Script compiler creates a .scr file, which contains a compiled script, a .cmp file used to store information about source files (so the game won't compile all scripts every time the level is executed unless the source files changed).


## Using the ingame debugger

Pteroengine contains simple yet helpful ingame script debugger. Once the level is executed, any time you press the CTRL+F12, you will pause the game and open the list of all runing scripts. Use the cursor keys to select the script you want to look into and press enter. The debugger will then open the selected .c file. In the left window you'll see the source code, in the right window you can define variables to watch. Switching between the windows is done by pressing the TAB.

*Source code window*

You can add the breakpoints at any place by just left click of the mouse, or by positioning the current line with cursor keys and pressing the SPACE. When you'll exit the debugger by pressing the ESC key, the debugger will pop up once the script will reach the breakpoint. Pressing the enter key will open the list of all source files included in the script - headers and includes, so you can switch to other part of the code. For other possibilities of the debugger press F1 - you'll get short online help.

*Variables window*

By pressing the enter you can change or add the name of the variable - you cannot enter the array members or variables inside the structure here - just the master variable. You can then use INS and DEL key to expand the data structure. Pressing F4 will give you a chance to change the value of the variable. Press F1 to show the help for other functions. The value of the variables will be shown only if the debugger was popped up by a breakpoint!

Debugger creates a .sdb file in the directory of the running script which contains debug information - placement of the breakpoints etc. If the debugger starts to behave weirdly, try to delete all sdb files in the current directory, it should help.


# Directory structure


## G

Directory G contains all gfx used generic for all levels. It's subdirectories are:

*Characters* - this directory contains character models

*Weapons* - this is the directory for all weapon models

And also many more used only to help keep data organized.


## INI

This directory contains many initialization and data files. Important subdirectories are:

*PLAYER* - ini files for players

*MULTIPLAYER/MAPS* - contains definition of the maps

*MULTIPLAYER/PLAYER/ACCESORIES* - contains file default.txt used for definition of the accesories for the MP game

*MULTIPLAYER/SCRIPTS/* - contains default MP scripts

*TXT -* contains text data, for more see here.

In the subdirectory INI there are few all important files:

*Campaign.txt* which specifies the campaign for the singleplayer mode.

*Eqp.txt* - data for the automatic item generation for the players

*Items.txt* and *items2.txt* (from the FA) containg the definition of items which can be placed in the map or picked by player

*Mp.txt* - containg class definitions for the MP

*Ptc.txt -* incredible complicated text document describing the particles, do not expect any documentation about this

*Qf.txt and qf2.txt* - quick fight definition files

*Speech.txt* - definition of the generic speech for the players

*Weap.txt and weap2.txt -* definition of the weapons


## LEVELS

This is actual directory for the levels - each level has it's own directory here.


## SND

This directory is used for storing the sounds, most important are files for defining the sounds, physics sounds and music.

*Xsound.txt* - definition file for the sounds in the game

*Music.txt* - definition for the music in the game


# Addon (mod) creation

If you want to make a complete mod, or change something the map editor doesn't allow, you must create a modification aka mod, or addon, call it what you will (for example, Fist Alpha is a mod too). When creating the mod, just copy/modify files to normal directory structure. These data can be accesed only from the editor. When you feel the addon is complete, use editor function to create the CBF file out of this. Addons are stored in the directory ADDONS. Create subdirectory named like your mod and place there:

All cbf files, mod picture (bmp file with resolution 290x196 named addonname.bmp) and mod ini file named addonname.ini.

Ini file should contain line

ADDON_NAME=Full name of your mod

Files in the actual addon are accesed by the engine as they would be placed in the normal directory structure.

NOTE: do not try to connect to the MP game with modified data - you will be kicked for cheating as your data doesn't match server's. When playing modified game, all players must have same data.


# Multiplayer map definition

Multiplayer map definition is placed in the TX3 files located in the directory ini/multiplayer/maps. Each tx3 file is one map which can contain many more missions. Format is simple. Every command starts with the ` sign (tilde), valid commands are `map, `screenshot, `mission, `desc, `scene, `script,`time, `points and `players.

First specify the name of the map and it's screenshot like this:

`map MYSUPERMAP

- The name of the map

`screenshot g\textures\thumbs\myscreenshot.bmp

- path to the screenshot

Then specify all sub missions for the specified map:

`mission MYMISSION

- the name of the submission, usually just "CTF", "DM" etc...

`desc #9390 #9390 #9390

- the text id for overall description, for the US mission text and VC mission text

`scene Levels\MYSUPERPAM\mysupermap.sco

- the path to the scene

`script ini\multiplayer\scriprs\mympscript.c

- the path to the control script

`time 5:00 90:00 30:00

- default time parameters

`points 1 100 15

- default point parameters

`players 20

-default scritp parameters

The types of the MP script already included in the Vietcong are:

*ini\multiplayer\scripts\pilot.c* - save the pilot

*ini\multiplayer\scripts\tt.c* - turn table

*ini\multiplayer\scripts\ctf.c* - capture the flag

*ini\multiplayer\scripts\dm.c* - deathmatch

*ini\multiplayer\scripts\tdm.c* - team death match

*ini\multiplayer\scripts\lms.c* - last man standing

*ini\multiplayer\scripts\rw.c* - real war

*ini\multiplayer\scripts\coop.c* - cooperative game (note, there must be also mp ai scripts for the players prepared for the mission!)

Description of the multiplayer scripts is here.

Use this ONLY if you are doing complete mod - for mere maps it's better to use editor function "finalize MP map".


# Overview of the Artificial Intelligence in the PteroEngineII


## Path finding

AI in Vietcong uses net of waypoints to navigate through the obstacles. Waypoint marks the place the AI can use for walking through. Warning - pathfinding can take a lot of computer time and slow the game down - unless you cannot do it otherwise, never send AI on a long path, rather divide it's path to smaller sections. If the waypoint is marked as a no shortcut, AI knows it MUST go through this place, it is useful around small object AI can see through, but cannot walk (like bush) - keep in mind that AI uses the waypoint grid mostly as a reference, it won't walk exactly on the waypoints and paths unless instructed to do so. Waypoint can also be marked as a hideout - it means that this place is useful for hiding (behind boulders etc). Battle AI needs those hideouts to work correctly!


## Script AI

When the AI is set to the script mode, it won't walk, change position or do anything else except shooting if it sees some target which can be hit without moving or rotating and if the shooting is enabled. This setting expects the script will handle everything - useful for the cut scenes and/or special situations which system AI cannot handle.


## Battle AI

When the AI is set to the battle mode, it moves and fights as it sees fit according to the settings. AI will try to shoot anything in the range, it will change positions (if the AI is set to the attack mode, it will look for closer hideouts to attack the enemy, if in retreat mode, it will be trying to disengage from the fight). If there are no usable hideouts around, AI can even lie down (but battle AI cannot crawl!). There are few specific types of tasks AI will do (they are mostly tied to the player team): special jobs are for the medic and engineer, who will try to heal and add ammo anyone around who needs it, radioman will run to the player if the radio is enabled.


## Battle AI in the peace mode

If the AI is set to the battle mode and there are no enemies around, it will behave as specified by it's peace mode setting - either hold position (unless in special static animation it will sit down eventually), follow the leader of the group or in the case of specified pointman it will go forward according to the set route.


## Stealth mode

Stealth mode (by default enabled only for the players team) means all the engine interaction texts will be in a whispered mode and more importantly, the AI will not shoot until PC starts to shoot, or the enemy discovers the team - they will just try to hide, aim, but not shoot.


## Sides and groups

Vietcong allows definition of various sides and their status - if they are enemies, allies or neutrals. Side 0 is reserved for the US side, side 1 for the Vietcong. There can be more sides (for instance representing villagers, who can at first neutral and then they start to be aggressive toward the side who will attack them).

Groups are what their name suggests - the group of cooperating players. AI in the same group inform each other about each enemy they spot.


# Game global variables

Global variables are stored in the array with the size of 4096. Each variable is long four bytes and they can be accessed either as a double word or a float number. These variables are same for all the scripts and they are used for the cooperation of scripts and also for storing various information about the game and especially about the campaign. Variables accessed directly by the engine are defined in the sc_def.h file:

SGI_DIFFICULTY (value 10) contains the game difficulty set in the game.

Other global variables are used for the storing info for the debriefing, etc. All used global variables should be defined in the sc_def.h with the naming convection SGI_variable for the integer/dword variable and SGF_variable for the float variables. For the set of functions working with the global variables *see here*.

Note: global variables are also used to coordinate the game in the multiplayer game. SC_MP_Gvar_SetSynchro function is used to set which global variables are synchronized - everytime the synchronized global variable changes on one machine, it changes on all machines.

More about using global variables see in the *Creating the campaign*.


# Game texts and speech

Game texts are stored in the directory ini/txt in the directory of the language (ame for the US version). Text file contains #text_id_number: and #ame text. (#ame is the identifier for the language). Texts are from the range of 0-9999 (for the original Vietcong) and from the 50000-56000 (for the Fist Alpha) . As most of them are already used, you must be careful to not use the already used ID! Best way is to use the editor function texts/log space which will log the empty places to the text files.

If the text should be used for the speech, there must be also correct sound file attached. These are located in the directory SND/dubbing. If the speech is marked either as a radio call (prefix "r"), scream (prefix "s"), whisper ("w"), inner speech ("i") or megaphone ("m"), it must be located in the subdirectory r, s, w, i or m. File name must be prefix+number of the speech, like s1000.ogg etc.

If the engine cannot find the sound file, it will show just the text. For the lip sync you must have the correct engine files generated.

There is also a possibility to use the sayto function - just add #sayto side group memberid to the text. This is the identifier for the game describing to whom this line is addressed. If the speaker or listener are AI and they can, they will automatically look at each other.

For the description of the speech functions see here. How to handle speech during the game can be found here.

For creating modifications of the Vietcong, use text numbers from 50000 higher - do not touch the texts of original Vietcong unless you really need to. Just create the directory ini/txt/ame (or tee for teen version, or ger for german etc) and place there some file and fill it with the texts you want. Engine loads all texts placed in the directory (first from main CBF, than from addon CBF or local files) and overwrites all previous values - so if you want to change texts from the original vietcong, just place their id's and new values to your file, to be sure, name it Z_TEXTS.txt or something like that.


# The Level Script


## Overview


```c
Most important things first. Every level MUST have level script level.c located in it's data/scripts directory. It can be almost clean, but there should be at least few things prepared, like the initialization of the game sides and groups. The level.c must contain function int ScriptMain(s_SC_L_info *info). s_SC_L_info is described here. Pure level.c can be found in the SDK directory scripts/level scripts/pure_level.c. For description of other level scripts included in the SDK, see here.
```

Level script is usually used for the coordination of other scripts, it is also the script controlling the flow of the game. Lot of special callbacks are directed to the level script, as the finishing of the speech, usage of the radio, pointman handling etc.

Good idea is to use the gphase variable storing the actual phase of the level and at every change change also the global variable SGI_LEVELPHASE, for example with the macro like this:


```c
#define SetLevelPhase(newphase)\
{gphase=newphase; SC_sgi(SGI_LEVELPHASE,newphase);\
SC_Log(3,"Levelphase changed to %d",newphase);\
SC_Osi("Levelphase changed to %d",newphase);}
```

Other scripts can access this value and they can find out in what stage the game is. Level phase at 0 means the level script still hadn't time to organize itself. 1 means the level made basic initializations and is waiting for the next time tick, change to 2 or higher should happen only when was finished the initialization of other scripts and some values (like setting the AI) were changed.

The level script can be called by the engine in these situations: scene initialization, scene release, after the game load, timetick, usage of the radio, speech finished, view animation callback, event (ie some other script sent message to the level.c), interaction with the pointman, getting information about the pointman status, artillery usage, after finishing the music, after command from the music system to set new music, after pressing story skip button, after lightstick usage. The information about the type of the callback is defined in the message variable in the *info* structure.

Level script should return 1 if it handled the message or 0 if it didn't.

Sample simple level script with the comment can be found in the SDK directory scripts/levelscript/level.c.

For more information about the level scripts for the multiplayer missions see here.

At the same place you can find the sc_level.h containing various useful macros and functions.


## Level script messages

The information about the message is defined in the *info* structure passed to the function ScriptMain.


### SC_LEV_MES_ INITSCENE - Scene initialization

This is the first call the level script gets at the start of the scene, either with new game or after the load. No other script is initialized yet, keep that in mind! This callback is designed for these functions: SC_SetObjectScript (forcing script for the object), SC_PreloadBES (preloading bes objects for the equipments, see adding special equipment to players), SC_PreloadWeapon (preloading weapons for the faster initialization) and SC_PreloadSound (preloading sounds). You can also store the initial values of certain objects, but it's better to do so in the object script.


### SC_LEV_MES_RELEASE SCENE - Scene Release

This is the call to the level script at the release of the scene - closing engine, loading another mission etc. Just in case you need to move some object back. Again, it's better to do so in the object script.


### SC_LEV_MES_JUSTLOADED - After the game load

This is callback after the game was loaded from the saved game. You can use it to set things which are not saved, like particles and waypoint blockers.


### SC_LEV_MES_TIME - Time Tick

This is the most important callback to the level script. It is called after the initialization of the script in zero time and then always in the time the script will specify in the parameter info->next_exe_time. Script also sets the time from the last call in the info->elapsed_time, as the timing is not 100 percent complete.

In the absolutely first time tick you should set some basic things, you must especially initialize the sides and groups. Also it is good idea to prepare the follow order for the teams, set the global variables, set on or off the artillery support etc. Then you should wait at least one second (usually it's good idea to black the screen with the SC_FadeTo), check if the players are already created and then do some changes in the setting of the AI (if it wasn't already done in the player scripts). Then the script "just" controls the flow of the game.


### SC_LEV_MES_RADIOUSED - Usage of the Radio

This callback is initiated when the player uses the radio (after it was enabled with the function SC_Radio_Enable). There is a specified identifier (from the enabling function) in the param1 of the info structure - so the script can choose which radio communication should be used. For more info, see radio communication.


### SC_LEV_MES_SPEACHDONE - Speech Finished

This callback is initiated when the speech is finished and there was specified callback. For more information, see handling the speech. The id number of the callback is stored in the info->param1.

This callback is used for a lot of things, as most things during the game starts after some one says something, or when the radio communication ends. This is also the usual place where the autosaving takes the place (see saving the game). But be warned - as the engine saves the game in it's current status, after the loading of this autosave the callback will be initiated again, so you must keep the status in some variable. See more in the saving the game.


### SC_LEV_MES_VIEWANIMCALLBACK - View Animation finished

This callback is initiated when the view animation ends and it is used mostly for the creating of the cutscenes. See Working with the view animation. The id number of the callback is stored in the info->param1.


### SC_LEV_MES_EVENT - Message Sent by Other Script

Every time some script sends message to the script using the SC_LevScr_Event function, the message will be received in this callback. Messages are stored in the info->param1 and the info->param2 variables.


### SC_LEV_MES_POINTINTERACT - Interaction with the Pointman

Every time the player points at the pointman and presses the USE key, this message is sent to the level script. There is an information about the status of the pointman in the info->param1. It can be as follows:

0 - pointman is in hold or follow mode, default action is set to pointman mode

1 - pointman is leading the team, default action is hold pointman

2 - pointman either has no way defined, or he waits for other team members.

Variable info->param2 contains pointer to the pointman.

Script should return TRUE if it handled message or FALSE if it didn't.

For more information about the pointman see working with the pointman.


### SC_LEV_MES_POINTINTERACTINFO - Getting Information About the Pointman Status

Every time the player points at the pointman the game engine shows interaction text. Value of the text is set in this callback. Parameters sent to the script are the same as with SC_LEV_MES_POINTINTERACT message. Script should fill the correct information to the info->param3. Standard used text ids are:

2115 - to let pointman lead the team

2118 - to stop the pointman

2119 - to talk with the pointman

If the text id will be set to 1, no interaction text will be shown.

For more information about the pointman see working with the pointman.


### SC_LEV_MES_ARTILLERY - Artillery Usage

This message is invoked when player marks the artillery place for the bombardment (can be used to reduce number of possible attempts for example). The centre of the bombardment is in the variable info->param4.


### SC_LEV_MES_MUSICDONE - After Finishing the Music

After the music started with the SC_SND_MusicPlay function ends, it will call back to the script. The ID number of the music is in the info->param1.


### SC_LEV_MES_GETMUSIC - Command From the Music System

This is the callback from the music system when it requires the music data. Info->param1 contains the id of the requested music, info->param2 is used by the script to set the data. See working with the music system.


### SC_LEV_MES_STORYSKIP - After Pressing Story Skip Button

If the skip is enabled with the function SC_StorySkipEnable, this callback will be initiated every time player presses the enter, space bar or the esc key. This is used to skip the view animations, cut scenes etc. Don't forget to disable the skip button after handling it's usage!


### SC_LEV_MES_LIGHTSTICK_USED - After Light Stick Usage

This message is given to the script every time the player uses the light stick (so we could add comment to the one place in the tunnels :o)


## Initialization of the game sides and groups

As you can read in the overview of the AI, the Vietcong needs to have the sides and groups correctly set. Forgetting to set the groups and sides can even cause the game to crash!

Side 0 is used for the US, 1 for the Vietcong.

Sides are initialized with SC_InitSide function. Alternatively you can use the simpler way, macro from the sc_level.h InitSide. Sides 0 and 1 are enemies by default. If you will work with additional sides, you can set their status by the SC_SetSideAlly function.

Groups are smaller groups of the players. Usually the group 0 0 (ie side 0, group 0) is used for the player and his team. Definition of the group can be done with the SC_InitSideGroup function or alternatively with the macro from the sc_level.h InitGroup or InitGroup2.

Definition of the sides and groups should be done in the first time tick of the level script, later it's usually too late as the players are already being created. Be especially careful when adding new groups later - be sure to have enough groups for the side specified! (Adding more groups than the side can have can cause the game to crash).


## Setting the follow order

Follow order is used for the specified group and it controls how are the AI following each other and what are the distances between them. You will probably usually use this only for the player team. You can do this with the SC_Ai_SetPlFollow function. You must call this function twice, first for the pointman mode (when the players are following the pointman) and second for the follow mode when they are following the leader (usually the player character). Simple and quick way for the standard levels containing the complete team (6 people) is to use the SetFollowOrder() function defined in the sc_level.h header file. But if you will have different number of the soldiers, or you just don't like the way they are moving, you must modify this setting for yourself.


## Saving the game

For autosaving the game you must use the SC_MissionSave function or alternatively the SaveGame or SaveGame2 macro from the sc_level.h. Saves are using the standard text identifiers for the name and description of the saved game. Sometimes you may want to disable the quick saving feature, this can be done by the SC_EnableQuickSave function.

Saving the game takes some time, so it's better not to use the autosave during the fight. Common way to handle the autosave is to use it at the beginning of the level and than after each radio communication.

Note: If you will use the save during the speech callback, it will be invoked again after the load game, so you must use some variable to store the information if the save was already done, something like this:


```c
if (!savegame[info->param1]){
savegame[info->param1]=TRUE;
SaveGame(9116,9117);
}
```

Sc_level.h contains a definition of the array usable for this, the savegame array. It's size can be defined by adding the line


```c
#define SAVEGAMECOUNT number_of_saves
```

before including the sc_level.h.

See tutorial level script for more information.


## Objectives

Another thing which is usually controlled by the level script are the objectives - which are shown to player after the pressing the objective key (TAB by default). Information for the objectives is stored in the structure s_SC_Objective and updated with SC_SetObjectives or SC_SetObjectivesNoSound function.

Sc_level.h offers more user friendly system, containing of the set of objective functions Clear_Objectives, Add_Obj, Add_ObjNS, Complete_Obj, Fail_Obj and Get_Obj_Stat. You can just call the Add_Obj everytime you add a new objective and then use the Complete_Obj or Fail_Obj when it's status is changed.


# The Player Script


## Overview

The player script is used to control the players in the game, either human or AI. Each player in the game (except the multiplayer human players) must have the script. Scripts are assigned to players in the editor at the player properties, or you can create the player and assign script to him using the SC_MP_AddPlayerScript function (note: although this function is marked as a multiplayer function, it can be used in single player game also).

Player script is responsible for the creating the player, setting his properties and is used for controlling the player and interaction with the game. Although you can place almost everything in here, it's best to use the player script just for the handling of this one player and for more global things use the level script.

Player script can be called by engine with these callbacks: time tick, player was hit or killed, another script is sending the message to the player, player finished playing forced animation, getting information about interaction, interaction with the player, player fell out of the car, someone has shot near the player, player should go for the human player character. The information about the type of the callback is defined in the message variable in the *info* structure.

Script should return 1 if it handled the message or 0 if it didn't.

For information about how to handle various player situations see here. Player creation is described here.


## Player script messages

Information sent to the player script are stored in the s_SC_P_Info structure.


### SC_P_MES_TIME - time tick

At the first, the time tick is executed as soon as all scripts are created and the game starts. In first time tick the player script should create the player, then wait until the player is created and ready to go (you can use the SC_P_IsReady function to take the status of the player). Then the script should make changes to the setting of the player (it must be done after the player is created!), like changing it's values of the AI. Lot of scripts then don't need to work with this message anymore (like standard battle AI), but it is usually used for handling the player during the game.

Info->elapsed_time contains the information about the elapsed time from the last executed time tick. Script can set next execution time using the info->next_exe_time.


### SC_P_MES_HIT - player was hit

This message is invoked anytime the player's health was damaged somehow (unless the player was outright killed). This message can be used for guarding the health of the player and maybe to heal him, also it can be used to determine who is shooting at the player (to deal with situations like human player shooting at the innocent civilians). Info->param1 contains pointer at the shooter, but it can be zero sometimes, so do not forget to check the value for zero! If you want to check if the player was hit by human PC, you can use something like this:


```c
if (info->param1 == SC_PC_Get()) {do something about it}
```


### SC_P_MES_KILLED - player was killed

This message is almost the same one as SC_P_MES_HIT, but it is passed to script in the case the player was killed by the damage.


### SC_P_MES_EVENT - received message from other script

This message is passed to the script if other script used the SC_P_ScriptMessage to call the current script. info->param1 and info->param2 contains data sent to the script.


### SC_P_MES_DOANIMEND - player finished playing the animation

This message is invoked every time the player finishes playing the "forced" animation, ie the SC_P_DoAnim function was used for the current player. You can use this to create strings of various animations, to check if the player finished some animation like placing the explosive etc. You must handle the information about which animation is played by yourself (changing some variable every time you use the SC_P_DoAnim).


### SC_P_MES_INTERACT_GETTEXT - human player is pointing at the player

This message is invoked when the human player is near enough and looking directly to the player, unless this situation is already handled (for the pointman in the level script, for the medic or engineer or radioman if their special action is usable ). If the script changes value info->param1 from zero to any other number, this number will be used as an interaction text identifier and shown as "Press USE (the Enter key" + text stored at the identifier. After pressing the use the SP_P_MES_INTERACT_DO message will be sent to the script. If the info->param1 remains zero, nothing will happen if the player points at the player.


### SC_P_MES_INTERACT_DO - human player is using the interaction

This message will be invoked if the player script in the SC_P_MES_INTERACT_GETTEXT set the interaction text and human PC pressed the use key near the current player.


### SC_P_MES_DROPOUTCAR - player fell out of the car

This message will be sent to script if the current player sitting in the car or the ship fell down (the car crashed probably).


### SC_P_MES_SHOTAROUNDCALLBACK - some one is shooting around the player

This message will be invoked if someone shoots near the current character (the bullets are passing nearby) and if this callback was enabled with the SC_P_Ai_GetEnemyShotAround function.


### SC_P_MES_GOTOPC - player is sent to the human character

This message is used for the human player team and it is invoked when player uses the quick key (numpad 1-6) to call the character by his side.


## Creating the player

Players are created with the SC_P_Create function, all for the creation are stored in the s_SC_P_Create structure. Structure contains basic data about type of the player (human controlled or AI), identifiers (side, group, member id), name and icon of the player, ini filename containing data about the character model (see list of all ini files in the Vietcong/Fist Alpha), initial weapons and inventory items and information about gfx equipment. You must also specify the position for the player recover (where he will be placed in the scene). The info structure contains variable pos, which has the position taken from the player object in the editor, so unless you want to place the player on some specified place (in case the script is executed using the SC_MP_AddPlayerScript function), you can set this position to the info structure. More information about the values are described at the s_SC_P_Create description. You can also create the inactive player using the flag SC_P_CREATE_FL_INACTIVE. Inactive player will not participate in the game until enabled with SC_P_SetActive function.

*Equipment*

The information about the equipment (like hats, bags etc) are stored in the s_SC_P_Create->eqp and s_SC_P_Create->eqps. Total count of the equipment, including the weapon, special items (like radio) and special equipment may be 10, so it's best to add 8 maximum equipments during the character creation. The s_SC_P_Create->eqp is an array containing information about gfx item (the bes file) and the eqp file, which contains information about how the item is placed on the character body. Equipments are described in the ID postav a equipments.xls excel file. Note - you must have correct eqp file for the correct character model (especially for the head)! You can use two ways to set this data:

*By hand -* you can just add the data manually as you want, or you can use some predefined file. You can find them in the directory SDK/scripts/players/eqp. File us_equips.inc contains various versions of the equipment for the American characters, vc_equips.inc for the Vietnamese. File vcfa-equip.inc contains easy to use function used in the Fist Alpha for generating the correct equipment for the each character model and weapon he uses, use this for the reference.

*Automatic generation -* if you do not specify the equipment data (info->eqps = 0) and the autogeneration will not be disabled (using the flag SC_P_CREATE_FL_DISABLE_EQPGEN in the s_SC_P_Create->flags), the engine will choose some hat or other head equipment and add it to the player. As there is a possibility the Vietcong guerilla will be created with the US pilot helm, you should also fill the aeg_valid_head_bes array in the s_SC_P_Create with the identifiers of the valid head equipments. For example the VCAutoGenEqp.inc file in the SDK/scripts/players/eqp contains function GetVCEquip which will set the data according the current mission for the Vietcong/Fist Alpha. ID of the equipment can be found in the file ini/eqp.txt


## Various player scripts

You can find various complete scripts in the directory SDK/scripts/players. For their description, see here.


# The Dynamic Object Script


## Overview

Dynamic objects are everything which can be used, burned, destroyed, moved etc in the game except the players and the animals. Dynamic object must be created, exported and marked as such, unless you risk the crash of the game if you try to work with nondynamic object. Usage of the dynamic objects is slowing the game down, so keep their number low.

There are few quite specific types of the dynamic object scripts, these are: car scripts, ship scripts, helicopter scripts, and mounted weapon scripts. For various other dynamic scripts, see the example scripts in the directory SDK/scripts/objects.

Scripts can be added to the object with two possible ways:

A) The directory with the object file (.bes) contains script with the same name as the object, in this case will be the script loaded automatically. When changing the script with the game engine running, don't forget to reload these scripts with the reload wizard!

B) By forcing the script to the specific object in the scene initialization call to the level script with function SC_SetObjectScript - object will always use this specified script instead the existed one.

The information about the callback is stored in the s_SC_OBJ_info structure. Variable info->event_type contains the type of the message. The dynamic object script can be called in these situations: object is initializing, object is being released, the game was just loaded, time tick, object was hit, MP synchronization of the damage, object was used, mounted weapon has shot.


## Script messages


### SC_OBJ_INFO_EVENT_INIT - object initializing

This message is passed to the script during the initialization of the object. It can be used to store some initial values like current transformation of the object and for the initial settings.


### SC_OBJ_INFO_EVENT_RELEASE - object releasing

This message is passed to the script during the scene release. The script should return the object to it's initial place if it was moved through the script and release any data it created like object animations etc.


### SC_OBJ_INFO_EVENT_JUSTLOADED - saved game loaded

This message is passed to the script after the initialization of the scene and if the game was loaded from the saved game. Some values are NOT included in the saved game, so this callback must move the object at the specified place and change it's destructions. It should also restore the information about pointers to various nods and animation objects etc, as these are stored as a pointers and they no longer contain the correct value after the loading of the game.


### SC_OBJ_INFO_EVENT_DOTICK - time tick

This message is passed to the script each frame. Info->time contains time from the last execution. Time tick can be used for lot of things like animating or moving the object. If you want the "usable" object, you should use the SC_ACTIVE_Add function, which will add the interaction text for this object. For more information about using the object see here.


### SC_OBJ_INFO_EVENT_HIT - object hit

When the object will be hit by shot or the explosion, this message will be sent to the object script. info->hit_by contains information what caused the damage (it can be missile = normal shot, human PC shot or the explosion), info-> new_hp_obtained contains information about the overall damage the object has taken. Hiding or destroying the object usually happens in this callback.


### SC_OBJ_INFO_EVENT_SET - MP synchronization

This message is no longer supported and it's usage can cause the game to crash. This message was designed for the multiplayer - when the object is damaged, the server uses this message to synchronize it's damage handling in all client's scripts (for setting the correct destruction).


### SC_OBJ_INFO_EVENT_USED - object used

If the object was enabled for the using with SC_ACTIVE_Add function and the player pressed the USE key, this message will be passed to the script. For more information about usable objects see here.


### SC_OBJ_INFO_EVENT_MOUNTEDSHOT - mounted weapon shooting

This message is used for the mounted weapons - every time the weapon shots, this message is invoked. It can be used to add the particles and to eject the empty cartridge with the SC_FPV_FlyOffCartridge function.


## Moving the object

If you want to move some object, there are few possible ways to do so:

A) *Physical objects* - if it is dynamic object with the physics, it will fall/move by itself. You can just freeze it in the space and unfreeze it when you need the stone to fall etc. Freezing can be done with the SC_DOBJ_SetFrozenFlag function. Alternatively you can add the dynamics (speed, rotation) manually using the SC_NOD_AddDynamic function.

B) *Manual movement* - you can manually change the transformation of specified nod with the SC_NOD_SetTransform function. In this case you should remember to store the initial value of the object in the initialization and than move it to it's correct place during the release and after the loading the game! You can move, rotate or scale object using the transformation.

C) *Animating the object* - using the MAX exported animation MANM file, see here.

D) *Using the camera animation -* camera animations can be used not just for the movement of the view, but also for any other object. This can be done using the SC_NOD_SetFromANM function. See more in the description of the helicopter scripts. In this case you should store the original transformation of the object during the initialization and during the release/after load set the correct position, see B) *manual movement.*


## Hiding the object

If you don't want the object to be visible in the level (for example it will be there after something happens, like destroying some other object), you can do it two possible ways:

A) hiding the object, so it won't be rendered, can be used for any object as a way to fasten the game, this can be done with the SC_DUMMY_Set_DoNotRenHier or SC_DUMMY_Set_DoNotRenHier2 functions. Information about the rendering are not stored in the saved game, so you must always handle this way in the SC_OBJ_INFO_JUSTLOADED. Also keep in mind that the object is still physically there, it just won't be rendered, so if it has collisions, the player could bump into it!

B) Setting the destroyed variant of the dynamic object to zero. It will disappear completely. You can show it again with SC_NOD_ResetDSTR function.

C) Hiding the object under the scene - use SC_NOD_GetTransform to get the current transformation of the object. Substract 1000 from the z coordinate of the position and then set the transformation back with the SC_NOD_SetTransform.

Do not forget to handle the hiding in the initialization, release and after loaded callbacks of the script!


## Animating the object

If you just to want to simply move or rotate the object, use the manual transformations. If you want to make more complicated animations, you must animate the object in the 3DMAX and export the animation to the MANM file.

Function SC_MANM_Create is used to initialize the MANM animation, the SC_MANM_Release is used for it's release during the object release. MANM works with the array of nods. Position of the specific nods in the MANM can be found out using the SC_MANM_GetIndex function. Use the SC_MANM_GetLength function to get the length (time) of the animation. For the setting of the animation status use the SC_MANM_Set for all nods in the animation. Sample script with the MANM animation can be found here.


## Destroying the object

Destroying of the object can be done by few different ways. You can use particles to mask the destruction, then just hide the object and then maybe move some other on it's place, but the "clear way" to do so is create the object with the destroyed variants. These variants are linked to their master object and they are named with the "&" sign at the beginning. These objects are not used or rendered until you change the destruction properties of the master object with the SC_NOD_SetDSTR function. You can also switch the destruction object to zero, it will disappear completely. Reset to the first variant can be done with the SC_NOD_ResetDSTR function.

Do not forget to handle the destruction setting in the after load callback!

Sample script with the destructions can be found here.


## Using the object

If you want usable object, ie object player can point the cursor at and then use it pressing the USE key, you must add the object to the interaction texts buffer with function SC_ACTIVE_Add. Object closest to the player will write it's interaction text to the screen and will be called after player presses the USE key. If the player is currently looking at the object can be found out using the SC_DOBJ_CameraLooksAt or SC_DOBJ_CameraLooksAtCollision functions. Warning! The nod specified in the SC_DOBJ_CameraLooksAt MUST be dynamic NOD!

Sample script for the usable objects can be found here.


## Specific types of the dynamic scripts


### Car scripts

To create the car, you must have the model first :o). Actual creation of the car in the script is done by SC_CAR_Create function. Fill s_SC_Car_Init structure, and pass it to the SC_CAR_Create function. Then you must create wheels with SC_CAR_WheelAdd function, again, fill the s_SC_Car_AddWheel structure. And at last, add entry points for the players with SC_CAR_EntryAdd function with data stored in s_SC_Car_AddEntry structure. For more reference see description of the data structures or preferably see example script. This creation should happen in the SC_OBJ_INFO_EVENT_INIT callback.

You can also specify the air resistance for selected car with the SC_CAR_SetAirResistance function.

It's recommended to place the car script to the same place where it's bes is and with the same name, so it will be loaded automaticaly.

WARNING: CARS DO NOT WORK IN THE MULTIPLAYER!


### Ship scripts

Creation of the ship is in many ways similar to the creation of the cars. Fill the structure s_SC_Ship_Init with basic ship data, structure s_SC_PHS_IWantToFloat with float data and pass them to the function SC_SHIP_Create. Add entry points as with the car, but use the SC_SHIP_EntryAdd function.


### Helicopter scripts

Helicopter's are quite special thing in the Vietcong, helicopter like scripts are used for many other stuff, like preanimated tanks, fighters etc. Heli object (created with the SC_HELI_Create function, data are stored in the s_SC_Heli_Init structure) is basically just some object making a sound and if it is over some surface, it creates the dust.

For moving and animating the chopper you must use the camera view animations and SC_NOD_SetFromANM function. At each time tick just set the correct position and the helicopter will fly according to the animation.

Warning, if you will use more helicopters in one level, each must have it's unique motor sound, see more at the sample script.

If you want the flying object to be usable for the sitting inside, you must use the SC_HELI_EntryAdd function. Huey objects used in the Vietcong for the choppers has 16 defined sitting places - first six are used for the soldiers, who are going to SIT in the chopper (they start outside the chopper), second six pack is used for the soldiers who start in the chopper and will leave the chopper (this is used to ensure the animations for entering/leaving will fit). Sitting place number 13 and 14 are used for the pilots, 15 and 16 for the door gunners. For the door gunners, you must also enable their places to use as a mounted weapon with the SC_MWP_Create function.

Sample scripts includes chopper-ini.inc include file containing the ChopperInit function for creating the chopper, ChopperRelease for it's release and Rotors_Tick for handling the rotation of the rotors. Unless you need some specific chopper, you should use this file.

For how the information about how to use the vehicles including choppers with player characters, see here.


### Mounted weapons scripts

Mounted weapons are statical weapons placed in the scene or for example in the chopper. Creation of the MWP can be done by filling data structure s_SC_MWP_Create and using it in SC_MWP_Create function. This should be done in the SC_OBJ_INFO_EVENT_INIT callback of the dynamic script. You should also watch the SC_OBJ_INFO_EVENT_MOUNTEDSHOT message which is invoked any time player shoots - use this for creating particles, ejecting cartdriges etc. For more information see description of the s_SC_MWP_Create and example scripts.


# The Sound Script

The sound script is used for the setting of some of the sound data - usually for the setting of the ambient sound (SC_SND_Ambient_Play) and creating of the curve sounds (SC_SND_CreateCurveSound) for the sounds of the rivers and streams. It has only one message (SC_SOUND_MESSAGE_INIT) and is called only once at the beginning of the level. Sound script must be names sound.c and placed in the level directory data/Levelname/scripts. Sample sound scripts can be found in the directory SDK/scripts/sound. Information to the ScriptMain are stored in the structure s_SC_SOUND_info;


# The Weapon Script

There are two types of the weapon script - for the FPV and 3PV model. Models and scripts of the weapon should be placed in the subdirectory G/WEAPONS/nameofgun and they should be named nameofgun_3pv, nameofgun_fpv and nameofgun_stg (for the model lieing on the ground), with script names corresponding to the name of the model, so they can be loaded automatically. Note - setting of the weapon statistics is not done in the script, but is defined in the ini/weap.txt and ini/weap2.txt.

Weapon scripts are used for animating the weapon, adding particles and ejecting spent cartridges.

Important special function for all weapon scripts is SC_FPV_FlyOffCartridge function which uses the data structure s_SC_FlyOffCartridge - use this for ejecting spent cartriges out of the gun.


## FPV script

Information about the callback are passed to the function ScriptMain(s_SC_WEAP_info *info) in the s_SC_WEAP_info structure. Variable event_type contains information about the type of the callback. Weapon script is called for - initialization, release, time change, animation validate and when engines asks for the animation time.

For more information check example scripts.

Callbacks are:


### SC_WEAP_EVENTTYPE_INIT - initialization of the gun

Initialization is usually used only for loading the MANM animation and for hiding specific parts of the weapon (like bayonet).


### SC_WEAP_EVENTTYPE_RELEASE - release of the gun

This is called when the FPV weapon is released - at the end of the game. Use it to release allocated MANM animations.


### SC_WEAP_EVENTTYPE_SET - timetick

This is the time callback. Info structure contains variable anim_id, which explains, what the weapon is doing now. This callback is used to set the animations, to show the particles, play sound effects etc.


### SC_WEAP_EVENTTYPE_VALIDATEANIM - anim. Validation

This callback is used to validate the animation.


### SC_WEAP_EVENTTYPE_GETANIMTIME - getting animation time

Engine uses this callback to get the time of the current animation


## 3PV Script

3pv script is much simpler and is used for all weapons which player can see in the hand of the other players. They are used mostly for the sound effects, and ejecting cartridges, also for hiding/showing the bayonets. Data are passed in the structure s_SC_WEAP3pv_info, script can be called for the init, shot of the weapon, reload and for changing the state of the bayonet.

For more information check example scripts.

Callbacks are


### SC_WEAP3PV_EVENTTYPE_INIT - init of the weapon

Initialization stuff. For the weapons with bayonet you should hide or show the bayonet on the weapon according to the info->cur_bayonet variable.


### SC_WEAP3PV_EVENTTYPE_SHOT - weapon has shot

Weapon has shot - use for particles, special sounds and for ejecting the cartridges.


### SC_WEAP3PV_EVENTTYPE_RELOAD - weapon is being reloaded

Weapon is reloaded - use for sounds, maybe for throwing away spent magazines.


### SC_WEAP3PV_EVENTTYPE_SETBAYONET - change bayonet

Bayonet state was changed.


# The Multiplayer Script


## Overview

Multilplayer script is the heart of the multilplayer game - it defines and controls game rules, player respawning, it shows the icons and text information etc. Multiplayer script is running on each computer, but it contains server specific and client specific callbacks. Server specific callbacks including the time tick are used ONLY on the server machine. Client messages are used on ALL machines including the server.

Callbacks are used at - level preinitialization, level initialization, for the HUD rendering, for server and client timetick, map restart, changing of the rules, for the user message sent from the other script and for the server only messages about player killed, player requesting recover time and recover place.

Multiplayer scripts are usually placed in the directory ini/multiplayer/scripts as they are shared for various levels (each script is another type of the game), but they can be placed anywhere. To add or change multiplayer script to the mission, open or create map file *.tx3 in the directory ini/multilpayer/maps and add or change the `script line for your mission to `script ini\multiplayer\scripts\nameofyourscript.c. For the complete format of the map files see here.

For more information about creating the multiplayer scripts and game, see here.


## Multiplayer script messages

The information about the message and it's parameters are stored in the info structure.


### SC_NET_MES_LEVELINIT

This message is passed to the script every time the level initializes. Param1 can be either TRUE (this is the server script) or FALSE (this is the client script). Param2 is TRUE if this is first time init, FALSE if this is subsequent reinitialization (after the mission was restarted). This callback is used to set few basic settings, like which sides can be chosed by players with SC_MP_SRV_SetForceSide and SC_MP_SetChooseValidSides functions, for setting class limits with SC_MP_SRV_SetClassLimit function, for setting up the HUD (heads up display) with SC_MP_HUD_SetTabInfo function, and for various preloads and other script initialization.


### SC_NET_MES_RENDERHUD

This message is passed to the script every frame rendered and can be used to write to the HUD. If the param1 is TRUE, this is the script running on the dedicated server. This is usually used for writing simple text messages to the screen using SC_Fnt_WriteW function.


### SC_NET_MES_SERVER_TICK

This is the time tick for the server script. It's the heart of the multiplayer script - this is the place where the script controls the game, adds points, guards the time etc.


### SC_NET_MES_CLIENT_TICK

This is the time tick for the client script. It is called on each machine in the game including the server machine! It can be used to change the values of the HUD, playing sound effects, making some changes which are not shared automatically for all clients like gfx changing (hiding/showing flags for example), adding flags to player equipment etc.


### SC_NET_MES_SERVER_RECOVER_TIME

This is the request from the engine to the script to fill the fval1 with the recover time for the player with the pointer stored in the param1. For special cases you can use the SC_NET_SERVER_RECTIME_NEVER value (never recover the player) or SC_NET_SERVER_RECTIME_ENDOFROUND (recover at the end of the round). Param2 contains the information about the type of the recover, if 0 the player was just killed, if 1 the player just entered the game. Each human player sends this message after he is killed or he just joined the game.


### SC_NET_MES_SERVER_RECOVER_PLACE

This is the request from the engine for the recover place of the player specified by pointer in the param3. Param1 contains the side which will be used for the player after the recover. Recover place is filled to the param2 as a pointer to the structure s_SC_MP_Recover *. There is a simple function to help with this task -SC_MP_SRV_GetBestDMrecov.


### SC_NET_MES_SERVER_KILL

This is the information to the server script about death of player specified in the param1, param2 contains pointer to the player who made the kill. It can be used for scoring the points, or for example for dropping the flag to the ground.


### SC_NET_MES_MESSAGE

This is the message to the network script from other script using the SC_MP_ScriptMessage function. Param1 and param2 contains the specified parameters. This message is used ONLY on the client machine which used the SC_MP_ScriptMessage!


### SC_NET_MES_LEVELPREINIT

This is the level preinitialization message (the level was not loaded yet). Param1 contains the type of the end rule, param2 the end value. This message is invoked even before the level starts loading. It is usually used to set the type of the mission into the global variable, so level script can set some things (like hiding unused flags etc) after it's own initialization. This message is also used to enable or disable AI characters placed in the scene for cooperative modes of the game with the SC_MP_EnableBotsFromScene function.

End rule type can be:

SC_MP_ENDRULE_TIME - mission should end after the specified time.

SC_MP_ENDRULE_POINTS - mission should end after one side has specified points.


### SC_NET_MES_RESTARTMAP

This means the map will be restarted, used to clear statistics, end rules and for recovering the players.


### SC_NET_MES_RULESCHANGED

This is the message about changing of the rules. Param1 contains the type of the end rule, param2 the end value.

End rule type can be:

SC_MP_ENDRULE_TIME - mission should end after the specified time.

SC_MP_ENDRULE_POINTS - mission should end after one side has specified points.


# The Script Helpers


## Overview

The script helper is a sphere defined in the engine with the object script helper and it can have it's own script. Script helpers can be used for example to define simple stuff like burning sphere (anything entering the script helper will be set on fire), for informing the level script that someone entered the forbidden area etc. Script helper's script is called during the initialization of the scene, it's release and at specified time tick. Information to the ScriptMain are stored in the s_SC_ScriptHelper_info structure. Sample scripts can be found in the directory SDK/scripts/helpers.


## Script helper messages


### SC_SCRHELPER_EVENTTYPE_INIT - initialization of the helper

This message is passed to the script during the initialization of the scene and can be used for setting some initial data.


### SC_SCRHELPER_EVENTTYPE_RELEASE - release of the helper

This message is passed to the script just before the release of the scene.


### SC_SCRHELPER_EVENTTYPE_TIMETICK - time tick of the helper

This message is passed to the script at the execution of the level and then at the time specified. Structure info->elapsed_time contains information about the time elapsed from the last execution, info->next_exe_time can be set with the time for the next execution.


# The Unipage Scripts

Unipage scripts are special part of the scripts and they are used to show debriefing, documents, etc - see items in the bunkers before briefings, it's all unipages.

*Unipage scripts are not described in this version of the SDK.*


# Handling various situations and scripts

This chapter shows various ways how to work with game elements.


## Handling the speech

Description how the speech data are stored can be found here.

Speech can be either from the radio, or it can be done by some player character. As the speech is both played as a voiceover and shown as a subtitles, you should set for each player and the radio the distance for showing the text, good default setting is about 20 meters. Sometimes you will need to change this distance (for example when someone whispers, or if you want the subtitles shown during some cutscene shown too far from the speaking character. Radio subtitles hearing setting can be adjusted with the SC_RadioSetDist function, for the players you must use the SC_P_SetSpeachDist.

For the actual using of the speech you should use the SC_P_Speech2 or SC_P_SpeechMes2 function for the players or SC_SpeechRadio2 or SC_SpeechRadioMes2. The functions with mes (message) can be used to set the speech callback. As soon as the speech ends, the engine will send a callback to the level script. Those functions also use the time variable. Set the variable to the time to the actual execution of the speech (ie if you set the time variable to 2.5f, the speech will be played after 2.5 seconds. The value of the variable will be changed and it will contain the time from the calling of the function, when the speech will END, so this can be easily used to preprogram the whole dialogue, see here:


```c
float time=0;
SC_P_Speech2(SC_PC_Get(),1000,&time);
time+=0.5f;
SC_SpeechRadio2(1001,&time);
time+=0.5f;
SC_P_Speech2(SC_PC_Get(),1002,&time);
SC_SpeechRadio2(1003,&time);
```

This block of code will cause the engine to play the dialogue between the human PC and radio with half second pauses between all lines.

If you are not sure if the player can speak (he could still talk something) and you don't want the two sentences to overlap, you can use the SC_RadioGetWillTalk or SC_P_GetWillTalk function to get the time of how long the radio or player will be talking (this is counted from all the active speech sent to player/radio). If you want to know if the player is talking RIGHT NOW, you can use the SC_P_GetTalking function.

If you don't want the player to talk at all (including the engine screams and shouts), you can use the SC_P_DisableSpeaking function to disable the speaking. If you want to stop the speech of some specified player, radio or all speech, you can use the SC_P_RemoveAllSpeech or SC_P_RemoveAllSpeechEx functions. Extended version allows the removal even of the speech which already started to play.

For better visual experience from the dialogue of more characters you can add the sayto data to the text files. Sayto contains information about side/group/member identifier of the player who is listening to the speech. Both speaker and listener will face each other if possible (human PC will not move, impossible during combat etc). Sometimes you cannot use this feature (for example when the player sits on the chair and could rotate through the furniture, so you can disable it for the specified player with the function SC_P_Ai_EnableSayTo.

Sometimes, during the cutscenes, it's best to not use the speech played as a 3D sound from the players head, but rather "inside" the camera. This can be done by setting the speech system with SC_SpeechSet3Dto3Dincamera function. Radio speech can be forced to play as a 2d speech with the SC_RadioSet2D function.


## Working with the music

You can play the music with functions SC_SND_MusicPlay, SC_SND_MusicStop, SC_SND_MusicStopFade, SC_SND_MusicFadeVolume and watch level script callback SC_LEV_MES_MUSICDONE. Alternatively you can use the music system, which also handles fading of various sound players (so the music will play and volume of the nature will be silenced, after the end of the music the volume will fade back etc). Prepare music data in the s_MusicDef array. When you want to start specific type of the music, use function SC_AGS_Set and set it to the index in the array. Engine will then send the level script callback SC_LEV_MES_GETMUSIC. Set the info->param2 to pointer to the array item and set the info->param3 to 1 (which means the data are valid). See the level script callback for more information.


## Working with the view animation

For working with the view animations you can use SC_SetViewAnim and SC_SetViewAnimEx functions. Normal version of the function just switches camera to the selected frame of the animation, while extended version is for "linked" animations - animations linked to some moving object (for example for animations inside the chopper etc.) Animations can be created in the editor tool camera editor. You can specify a callback id in both functions (if 0, callback will not be used). If the callback ID is specified, after playing the camera animation to the selected frame, level script will receive callback SC_LEV_MES_VIEWANIMCALLBACK. So if you want to have a cutscene with four cameras, you can do it like this:

Start the cutscene somewhere in the code:


```c
SC_PC_SetControl(FALSE);
SC_SetViewAnim(CAMERA1,CAMERA1STARTFRAME,CAMERA1ENDFRAME,1);
```

Then modify the callback in the level script:


```c
case SC_LEV_MES_VIEWANIMCALLBACK: switch (info->param1){
case 1: SC_SetViewAnim(CAMERA2,CAMERA2STARTFRAME,CAMERA2ENDFRAME,2);
break;
case 2: SC_SetViewAnim(CAMERA3,CAMERA3STARTFRAME,CAMERA3ENDFRAME,3);
break;
case 3: SC_SetViewAnim(CAMERA4,CAMERA4STARTFRAME,CAMERA4ENDFRAME,4);
break;
case 4: SC_PC_SetControl(TRUE);
break;
}
```

Note: although the camera animation will be working even without SC_PC_SetControl, you should better use this function (it disables player's input). Callbacks are also usefull for synchronizing other events in the cut-scene, like playing animations of the characters etc.


## Radio communication

Radio communication is the essential part of the gameplay in the single player Vietcong - it gives you information about the game and it is also used for the autosaving. Radio can be either carried by human PC or by some other player, usually Defort. Simple messages from radio can be easily done with SC_SpeechRadio2 or SC_SpeechRadioMes2, see more at the speech chapter. If you want the AI radioman use the radio dialogue, you must use the SC_RadistBatch_Begin function. After this function all speeches sent to the engine are used as a radio communication, until you end the batch with the SC_RadistBatch_End. The radioman will crouch, he will take the receiver and talk until finished, he then puts the receiver away and gets back to his last task. Do not forget to stop him from moving with the SC_P_Ai_Stop function. Sample code for the radio man communication looks like this:


```c
float time=0;
dword radistid= SC_P_GetBySideGroupMember(0,0,4);
SC_RadistBatch_Begin();
SC_P_Speech2(radistid,1000);
time+=0.5f;
SC_SpeechRadio2(1001);
time+=0.5f;
SC_P_Speech2(radistid,1000);
SC_RadistBatch_End();
```

If you want to work with the human player radio using, you must use the SC_RadioBatch_Begin and SC_RadioBatch_End. You can use these functions anytime, but be sure that the radioman is close enough or the PC has the radio in the inventory. This works exactly as with the radioman's batch. For the player to see the blinking icon and had to switch to radio or interact with the radioman, use the SC_Radio_Enable function. This will cause the radio icon to blink and radioman running to player, if enabled. After the player switches to the radio or interacting with the pointman, the engine will send a message to the level script about the radio interaction. In this callback you should you the SC_RadioBatch_Begin etc.

If you want to use the autosave at this radio, you should use the last speech in it's message version (SC_SpeechRadioMes2 or SC_P_SpeechMes2) and in the speech finished callback save the game.

If you want to enable the skipping of the radio communication by pressing the use key, use the SC_PC_EnableRadioBreak function.

See more at the example scripts.


## Working with the particles

Particles are sprite effects used for the fire, shot effects, water, smoke and so on. Sometimes you will need to use the particles manually, for example for showing the smoke over the destroyed car etc. ID number of the particles can be found in the game engine in the particle editor. Manual using of the ptc in the script can be done with the SC_CreatePtc, SC_CreatePtc_Ext (which allows to change some particle parameters), SC_CreatePtcVec_Ext (same as previous, only in the space, not in some object) and SC_CreatePtcInNodSpace_Ext (this will create the particle in the space of the specified object, useful for moving stuff like jet fighters).


## Working with the sound

Most of the ingame sounds should be placed in the editor as events, but sometime you will need to play the sounds directly from the script.

There are two types of the sound - 2D and 3D.

2D sounds will be just played to the speakers, these can also be stereo. Use the SC_SND_PlaySound2D for playing 2D sounds.

3D sounds are player from some place, so you will hear them differently from different places. Use SC_SND_PlaySound3D (normal 3d sound), SC_SND_PlaySound3Dex (sound with timeout, will play after specified time), SC_SND_PlaySound3Dlink (will play sound linked to some moving object). You can also use the SC_SND_PlaySound3DSpec, SC_SND_PlaySound3DexSpec or SC_SND_PlaySound2DSpec if you want to use different sound players (there are few sound players in the game, specific for the game, nature, music etc.. sometimes you will need to play the sounds in other volume than all other sounds, normal sound functions plays this sound in the game sound player).

For the changing of volume of various sound players use the SC_FadeSoundPlayer function.

You can also manually change overall sound settings (usually done in the sound script).


## Working with the players


### How to get information about the players

Player can be identified by two ways: by pointer to it's object, which is stored in the dword variable. Most of the functions deal with this pointer, also the player script is passed this pointer. For the human player you can use the SC_PC_Get(), which will return the pointer to the human PC.

The other way is to use the identifier side/group/memberid, which should be unique for each player (by convention side 0 is US, 1 Vietcong, group 0/0 is the PC's team, the human PC himself is 0/0/0). You can use the SC_P_GetBySideGroupMember to acquire dword pointer to the specified player. In the multiplayer all PC's have identifier 255, group 0 and side 0 or 1.

If you want to get the information about the side from the pointer, you must use the SC_P_GetInfo. This function will fill the data structure containing the player's identifiers, and his health.

The player can be in the deactivated state - which means he doesn't move, isn't rendered, just he's there prepared. Active status can be changed with SC_P_SetActive, player can also be created inactive.

There is a set of function designed to get information about the position of the players and other various information. Most simple function is SC_P_GetPos (or it's special version valid only for the human PC - SC_PC_GetPos), which will return the position in the 3d space, where the legs of the AI touch the ground. SC_P_GetHeadPos can be used to get exact position of the players head (for the headshots :o), SC_P_GetRot will return the rotation of the player around the z axis. SC_P_GetDir will return the information about player "speed" - how he moves in axis, this can be used to get information if the player is stationary, or if he is moving, like in this function:


```c
BOOL P_IsMoving(dword pl_id){
c_Vector3 pos;
float len;

SC_P_GetDir(pl_id,&pos);
len = SC_VectorLen(&pos);
if (len>1.0f) return TRUE;
return FALSE;
}
```

One simple way to acquire information about the player's position is to use the SC_P_GetDistance, this function will return the distance between two specified players.

Changing of the players stance can be done by force also with SC_P_SetPhase, usually used for the cutscenes or forcing the human PC to change the stance. For the AI it's better to use AI functions to change the stance, SC_P_Ai_SetMovePos.


### Player animations

You can set the player (any player including human PC) force to do some specific animation with the SC_P_DoAnim or SC_P_DoAnimLooped. Looped version of the function will cause the animation playing for the infinite time until you change the animation with other use of the anim functions (you can switch the forced animation with using the SC_P_DoAnim with the parameter NUL). After finishing the animation the engine will send a message to the player script. Warning: use this only for the AI in the script mode, for the human player disable his control with SC_PC_EnableMovementAndLooking or with the SC_PC_SetControl function. If you forget, it is possible the player will play the animation, but he will still move/fight.


### Changing the AI settings

AI can work in two modes - battle or script. In the case of the script logic AI doesn't do anything unless specified in the script. Battle mode is classical fighting AI, it does what it deems necessary. Changing between the AI modes can be done with the SC_P_Ai_SetMode to either SC_P_AI_MODE_SCRIPT or SC_P_AI_MODE_BATTLE.

Basic AI battle properties can be changed using the SC_P_Ai_GetProps and SC_P_Ai_SetProps. Use SC_P_Ai_GetProps to acquire the actual data, change those you want and set them back with the SC_P_Ai_SetProps. For the information about what you can change this way see structure s_SC_P_AI_props.

Some of the properties to handle the grenade using of the AI can be set with SC_P_Ai_GetGrenateProps. Ai uses the grenades when it knows about some enemy for some time, but cannot hit him normally - ie enemy is sitting behind the obstacle.

Some other properties in the battle can be changed with the SC_P_Ai_SetBattleProps function.

AI works in two different modes - peace mode and battle mode.

*Peace mode* is case when there is no enemy around. AI can be set to either hold, follow or point mode with the function SC_P_Ai_SetPeaceMode. In follow or point mode it will follow the leader of the group, either the player 0 of the group (usually PC), or the player 1 - designated pointman by default. As soon as the AI sees/hears the enemy/is informed about him by other AI, it will switch to the battle mode. Special peace mode is SC_P_AI_PEACEMODE_SEARCHDEATHBODIES, this will cause the AI to look for the enemy bodies and check them.

*Battle mode* is the fight mode. Use the SC_P_Ai_SetBattleMode or SC_P_Ai_SetBattleModeExt function to change the behavior of the AI to hold (ai will stay mostly on the place), attack (ai will try to advance on the enemy positions), agressive attack (ai will storm the enemy positions), retreat (ai will try to move out from the enemy), follow (ai will try to follow the team leader), or go to place (ai will fight, but it will try to reach the specified place).

If you want to make AI move in specified way, you can use the SC_P_Ai_SetMoveMode for the run/walk and SC_P_Ai_SetMovePos for stand/crouch/lie. Be warned, this setting is always valid only for the AI in the script mode. AI in the battle mode will probably change the stance as soon as it thinks this is the wrong way. AI in the battle mode usually runs in the erected position or crouches behind the obstacle.


### How to make AI do something?

FIGHT

Making AI fight is simple - just be sure it has some weapons and use the SC_P_Ai_SetMode to set it into battle mode - AI will do it quite well by itself.

MOVE

If you want to move the AI on some specified place, just use the SC_P_Ai_Go. But be warned - AI set the battle mode and with some enemies nearby will probably forget about the moving and it will start to fight. To be sure the AI reaches some place, you should set it to the script mode and then periodically check if it reached the place. If you want some AI to move on some place and start to fight right there, just set it to the script mode, send it to the place and when it reaches the specified place, switch it to the battle mode. If you want the AI peacefully moving between some places, do it same way, but switch it to the battle mode as soon as it sees the enemy (use the SC_P_Ai_GetEnemies or SC_P_Ai_GetSureEnemies, or the SC_P_Ai_GetDanger).

SHOOT at the specified place

Use the SC_P_Ai_ShootAt function. Make sure the AI has weapon and ammo and it has shooting enabled with SC_P_Ai_EnableShooting. This works on 100 percent only in the script mode, in the battle mode there is a possibility AI will shoot at the enemy instead.

THROW a grenade

Use the SC_P_Ai_ThrowGrenade function. AI will try to throw the grenade on the specified place.

THROW a smoke grenade

This is bit more complicated as the smoke grenade is not the standard feature of the AI. Set the AI to the script mode and make it play the animation (somewhere in the player's script):


```c
SC_P_Ai_SetMode(info->pl_id, SC_P_AI_MODE_SCRIPT);
SC_P_Ai_Stop(info->pl_id);
SC_P_DoAnim(info->pl_id, "g\\characters\\anims\\A941_grnd_up_0.stg");
grenadeusing=1;
```

And add something like this code to the animation callback:


```c
case SC_P_MES_DOANIMEND: switch(grenadeusing){

case 1: SC_P_DoAnim(info->pl_id, "g\\characters\\anims\\A942_grnd_up_1.stg");
SC_P_GetPos(info->pl_id,&vec);
vec.z+=1;
movdir.z=startp.z-vec.z+1;
movdir.y=startp.y-vec.y;
movdir.x=startp.x-vec.x;
SC_Item_Create2(147,&vec,&movdir);
grenadeusing=0;
SC_P_Ai_SetMode(SC_P_AI_MODE_BATTLE);
break;
}
```

After the player finishes playing of the first part of the animation, SC_Item_Create2 will create the smoke grenade just before him and will throw towards to the specified place.


### Players and vehicles

Except for the helicopters the use of the vehicles in the Vietcong is limited. You can use the SC_P_SetToHeli/ SC_P_ExitHeli or SC_P_SetToShip/ SC_P_ExitShip or SC_P_SetToCar/ SC_P_Ai_StepOutCar for the immediate teleport to/from the vehicle, but only the choppers support actual getting in and out for the AI. This can be done with the SC_P_Ai_EnterHeli and SC_P_Ai_StepOutHeli functions. If the entry place of the vehicle has shooting enabled or mounted weapon linked, AI will use it and shoot if shooting is enabled.


### Adding special equipment to players

If you want the player to have some special equipment for a time during the game (like axe, which will be hided after the player gets to the fight, you can use SC_P_Link3pvEqp and SC_P_UnLink3pvEqp functions. Specified bes file must be preloaded during the initialization of the scene in the level script like this:


```c
SC_PreloadBES(1, "g\\weapons\\Vvh_Knife\\VvH_Knife_fpv.bes")
```

Macros for the preloading are specified in the example scripts.


### Waypoint blockers

If you don't want the AI go somewhere (for example there is a trap placed and AI has to wait until the human PC disables it, or for the locked/closed door), you can use the SC_Ai_Blocker_Add function to create spherical blocker which will disable all waypoints in it's radius. Do not forget to remove the blocker during the scene release (either in the level or object script) with the SC_Ai_Blocker_Remove! If you will remove the blocker during the game, use the SC_ClearImpossibleWayTargets as AI will store the impossible ways in special array, including possible way through the blocker.

If you want to AI move out from some place or stay of it (for example placed explosive), use the SC_Ai_FakeDanger function. This place will be than marked for a specified time as a live grenade place and all AI will do their best to stay away from the area.


### Working with the pointman

Pointman is specific and important part of the Vietcong single player game. Pointman is usually used only for the PC's team.

If you want to set the team to the pointman mode, you must use the


```c
SC_Ai_SetPeaceMode(0,0,SC_P_AI_PEACEMODE_POINT);
```

Side/group specification 0/0 is usually used for the PC's team, if the team is set to other group/side or if you want to use the pointman mode for other group, you must change the values. Stopping from the peacemode can be done with same function, just specify the hold or the follow mode.

To use the pointman, you must first set the follow properties, unless you have the default team without gaps in the member id's. Then you must specify the checkpoints the AI should visit on it's path. This can be done with SC_Ai_AddCheckPoint. Simple way to quickly define the path sc_level.h include file. Just place the

#define CHECKPOINTBASE "waypointname%d" before including the file (or use the default name "point". Name the waypoints in the level with "waypointname1" to "waypointnamexxx" (use as much waypoint as you want) and then you can use the ResetCheckPoints and AddCheckPoints functions - you will just specify the first and last number of the path used for the pointman's path and it will be set accordingly.

Handling the interaction with the pointman is usually done in the level script in the SC_LEV_MES_POINTINTERACTINFO and SC_LEV_MES_POINTINTERACT callbacks. In the SC_LEV_MES_POINTINTERACTINFO the engine asks the level script for the id of text to show as the interaction. As the interaction should be used only if both PC and pointman are not talking and there are no enemies nearby, you should check first if this is correct, you can use the PointTalkCheck macro from the sc_level.h.


```c
#define PointTalkCheck if (SC_P_Ai_GetEnemies(info->param2)||(SC_P_GetWillTalk(SC_PC_Get())>1)||(SC_P_GetWillTalk(SC_P_GetBySideGroupMember(0,0,1))>1)) \
{info->param3=1;return TRUE;}
```

If the PC or pointman are talking or if the pointman knows about some enemies nearby, the script will return the value 1 which means no interaction is possible.

Then you should choose which text will be shown, this can be done for example this way:


```c
switch (info->param1){
case 0: info->param3=2115; //to let pointman lead the team break;
case 1: info->param3=2118; //to stop the pointman break;
case 2: info->param3=2119; //to talk with the pointman break;
}
```

Warning, the status 2 usually means that the pointman is waiting with the rest of the team, but it can also mean that he has no other way defined, the checkpoints are already all visited. You should look for this case with the SC_Ai_GetCurCheckPoint function in the case 2: - if the function returns TRUE, there is probably something wrong, unless you have parts of the level without specified pointman path.

Actual interaction is done in the callback SC_LEV_MES_POINTINTERACT, this means player used the pointman. Actual simplest way to handle it is:


```c
switch (info->param1){
case 0: //go on SC_Ai_SetPeaceMode(0,0,SC_P_AI_PEACEMODE_POINT);
break;
case 1: //hold!!! SC_Ai_SetPeaceMode(0,0,SC_P_AI_PEACEMODE_HOLD);
break;
case 2: //he is waiting, do nothing break;
}
```

Actually the better way to do so is to use some speaking, so instead the setting of the peace mode you should add some simple dialogue ending with the speech message and set the point mode in the speech callback - look at the example scripts.

For better feel of the pointman leading you can use these functions:

SC_Ai_PointStopDanger - pointman will stop and look for the danger, all other team members will react slower

SC_Ai_StopDanger - all team members will be suddenly alerted

SC_Ai_SetPointmanNormalWalking - will enable normal walking, not the stealth slower one

SC_P_Ai_SetPointmanBreaks - this will enable occasional random pointman breaks - he will stop, look around and then he will continue forward.

If you want the team walk in the peace mode (ie led by pointman or player) like they were under attack, you can use the SC_Ai_FakeEnemy_Add function. This will tell the AI that on the specified place there could be enemy and they will try to stay in the cover. If you will use NULL for the fake enemy position, 0 for the number of danger spheres and for the sphere array, they will assume enemy is everywhere and they will move like under fire until you switch the fake enemy off with the SC_Ai_FakeEnemy_Remove.


# Creating single player missions

Vietcong currently doesn't support creating of one simple single player mission - you must create campaign (see here) with the one and only mission, or make it a quickfight. As for the actual creation of the mission - see here, tutorial on simple single player mission.


# Creating campaign

Creating campaing is quite simple :o). Just prepare all single missions which will be contained in the game and then create/modify file campaign.txt in the INI directory.


## Campaign txt format

Campaing.txt contains:

List of all scenes

Format is as follows:

MIS = [id] , [name id], [description id], [scene name.sco], [show in single mission]

*id *is numeric identifier, allways use one identifier for one mission! This is also used for thumb pictures which should be placed in the directory g/textures/thumbs/Thum*id.*bmp (Thumb63.BMP for id 63) *name_id* is text id for the name of the mission (shown in the single mission menu)

*description id* is text id for the mission description

*scene name* is link to the sco file like levels\BomberPilot\bomberpilot.sco

*show in...* can be either 0 or 1. If 1, the mission will be shown in the single mission menu. Use zero for debriefings etc.

So one mission line will look something like this:

MIS=52,53100,53101,levels\BomberPilot\bomberpilot.sco,1

List of all mission blocks

These are blocks of the missions loaded - like Bahnar Visit consisted of three 3canyons submissions and bahnar visit mission. This is used mainly for the special mission loaders and is specified as:

LEV= [id], [name id]

ID must be same as first mission in the block.

Loaders are located in the directory g/textures/loaders/loader*id*.dds - so for bomber pilot is the line

LEV=52,53100 BomberPilot

And the loader image is g/textures/loaders/loader52.dds.

Note DDS is direct draw surface file.


# Creating Multiplayer missions

There are few sources of the scripts available in the SDK in the directory scripts/MP scripts. Be sure to check them and look more closely at how it is done.

You can also look at the step by step MP scripting tutorial or cooperative scripting tutorial.


### Level Script for the MP missions

Level script for the MP missions are quite simple - they just need to handle few basic functions, most of the game is handled in the multiplayer script. Level script should initialize the game sides and also hide unnecessery GFX and initialize dynamic object scripts - most of the missions contain all flags, ammo crates etc for all modes, so you need to disable parts of the GFX you don't need according to the mission type. Mission type is specified in the global variable GVAR_MP_MISSIONTYPE (it is set in preinit callback of the MP script.

Sample level script can be found in the SDK directory scripts/MP scripts/level.c


### Multiplayer script

Only server machine gets the server messages, but it also gets the client messages, do not forget about it. Variables used in the server part of the script do NOT contain proper values for the client ticks, you must always synchronize them.


### Multiplayer script - messages for both server and client machines

These messages are sent on both client and server machines.

SC_NET_MES_LEVELPREINIT

In this callback you should set basic global variables, especially game type to GVAR_MP_MISSIONTYPE, and enable or disable AI characters with SC_MP_EnableBotsFromScene. You should also store the end rule and it's value here to some variable, as they are parsed as messages in this callback. This message is invoked as first, even before loading the level.

SC_NET_MES_LEVELINIT

This is the actual level initialization. Parameters specify if this is the server initialization and if it is first time init or if the mission was restarted. You should set some basic settings here, like class limit with SC_MP_SRV_SetClassLimit, valid sides with SC_MP_SetChooseValidSides and TAB info settings with SC_MP_HUD_SetTabInfo function.

For the first time init you should preload items (like items 145 and 146 - flags) with SC_Item_Preload. You should also get the position of the flags from the scene here.

Server should also get the recover places (simplest done with SC_NET_FillRecover).

SC_NET_MES_RESTARTMAP

This callback means the map was restarted - it should be used to clear statistics of the players etc.

SC_NET_MES_RULESCHANGED

This callback just sets the new end rules - store the values from the parameter.

SC_NET_MES_MESSAGE

This callback means some other script running on the same machine used the SC_MP_ScriptMessage function. This is used by the dynamic object scripts to inform the script about their usage, or by AI player scripts. Warning, this information is ALWAYS sent only to the one machine! This callback can be used to synchronize information about the event with all other clients a server via global variables.

SC_NET_MES_RENDERHUD

This message is used on all computers in the game everytime the engine renders a frame - it can be used to write some additional information on the screen.

SC_NET_MES_CLIENT_TICK

This is the time tick for the client. For a lot of game modes it can be void, usually it is used only for showing additional information like showing the icons with time etc. For the CTF mode it is also used to change equipment for the players carrying the flag - this is one of the things which are not synchronized automatically. Other possibilites for the client script is handling the dynamic objects (like hiding or showing specific things).


### Multiplayer script - server messages

These messages are sent ONLY to the server machine.

SC_NET_MES_SERVER_RECOVER_TIME

This is the request of the player for the recover time - how long it will have to wait before recovering itself. You can just simply set him some fixed value, but most modes use spawning of whole teams at once, so you may need to use some timers to get thing right. Do not forget that this message is used both when player is killed and when he joins the game for the first time!

SC_NET_MES_SERVER_RECOVER_PLACE

This message means player is trying to recover and it is asking where exactly it should recover. Server script must have prepared places for the recover and send him one suitable. You can use the SC_MP_SRV_GetBestDMrecov function for easy choosing of suitable place.

SC_NET_MES_SERVER_KILL

This mesage is sent to the server anytime someone dies. It can be used for counting the points for team games, or in the CTF mode for dropping the flag out of the player.

SC_NET_MES_SERVER_TICK

This is the most important part of the server script - it handles the rules of the game type, for example the end rules. What exactly is in this part of the script depends on the type of the game. For the deathmatch is just guarding of the end rule. For CTF it's much more complicated as the game itself can be in two states (waiting for more players and actual game), script must check if someone takes or places the flag, synchronize this information with clients etc. See example scripts.


### Dynamic objects in the MP

There are few uses for the dynamic objects in the multiplayer - ammo crates, bomb places, actually anything you want. Actual adding of the dynamic object must be done in the initscene callback of level script. Every computer in the game has it's own script running, so you must synchronize the results if it is for example the bomb place.

Most of the missions in the Vietcong contain the ammo crate - this is very simple script which will only add the crate as a clickable object for the player playing on his machine. If player uses the box, it will give him the ammunition with SC_P_AddAmmoNoGrenade(SC_PC_Get());

This is standard script is located in the ini/multiplayer/scripts/ and is called addammo_dobj.c - it can be assigned to any dynamic object.

For the ATG modes with bombing there is a script ini/multiplayer/scripts/atg_dobj.c which works essentially the same - it allows the object to be used and shows the interaction text according to the side of the player (if he is VC or US) and if the bomb is already placed, or can be placed. If player uses the object, DOBJ script will send a message to the MP script with SC_MP_ScriptMessage - MP script will then set the synchronized global variables for all clients informing them about the change.


### Using AI in the MP

To use AI in the MP, you must place the player objects in your map and assign them scripts, as you would do for the single player mission. BUT - you must use SC_MP_EnableBotsFromScene(TRUE) in the initialization of the MP script and you must remember that AI scripts are running only on the server machine. Scripts should not use functions like SC_PC_Get, SC_PC_GetPos etc, as this will allways feed the script with the value of server player.

Also - if the AI player dies, it WILL NOT be respawned by normal engine function - he will be dead until map restarts or when using SC_MP_RecoverAllAiPlayers function (this will recover ALL Ai player, including living one)- and he will be respawned with default values, so you should everytime when the mission restarts send message from server MP script to all AI scripts that the mission is being restarted, so they can reset their values. See examples.

If you want to respawn AI during the battle, you must use the function SC_MP_RecoverAiPlayer. Best way to handle this is to send mp script message when AI player dies and send in the MP script time to recover to the AI script. See bots appendix.

Sample scripts contains some generic COOP ai scripts, which can be used in any level. You may also look at the bot scripts in the bots appendix. Note - bots are not officially supported in the Vietcong, it's more a way to show you how it can be done.


### Finishing the level

When you have the scripts written for your map, just add mission with this script to a map ini file.


# Description of all types, structures and functions in the Vietcong


## Structures - for various 3d data


### c_Vector3 - 3D information data

Declaration:


```c
typedef struct {
float x,y,z;
}c_Vector3;
```

c_Vector3 is basic structure used for storing information about 3d position.


### s_sphere - 3D sphere data

Declaration:


```c
typedef struct{
c_Vector3 pos;
float rad;
}s_sphere;
```

Structure s_sphere is structure used for storing the information about the sphere placed in the game - it's position and radius.


## Structures - script info structures


### Structure s_SC_L_info - level script

Declaration:


```c
typedef struct{
dword message,param1,param2,param3;
float elapsed_time;
float next_exe_time;
c_Vector3 param4;
}s_SC_L_info;
```

This structure is used for storing the information sent to the level script. Message contains the information about what callback is sent, param1 - param3 contain specific parameters, param4 is used for the artillery callback. elapsed_time is the time from the last time execution of the script, next_exe_time is used to specify the time when the time tick of the script should be executed again.

*Type of the messages:*

SC_LEV_MES_TIME

The time tick. Parameters are not used

SC_LEV_MES_RADIOUSED

Radio was used, param1 contains id of the radio set in SC_Radio_Enable

SC_LEV_MES_SPEACHDONE

Speech finished playing, param1 contains id specified in the speech function. Warning, cannot be 0!

SC_LEV_MES_VIEWANIMCALLBACK

View animation executed with SC_SetViewAnim or SC_SetViewAnimEx finished playing, param1 contains defined callback id. Warning, callback ID cannot be 0!

SC_LEV_MES_EVENT

Some other script sent a message to the level script with the SC_LevScr_Event function. param1 and param2 contain values sent in the SC_LevScr_Event.

SC_LEV_MES_POINTINTERACT

Human PC used the interaction with the pointman. param1 contains status of the pointman (0 is in hold or follow mode, 1 is moving as a pointman, 2 is moving, but stays on the place, either waiting for the rest of the team or doesn't have the checkpoints specified). param2 contains player id (pointer) to the pointman player object.

If the script returns FALSE in this callback, the engine will do the default action.

SC_LEV_MES_POINTINTERACTINFO

PC aims a cursor to the pointman, engine is requesting the text id for the interaction text, this interaction text is filled to the param3. If the param3 is set to 1, no interaction text will be shown. param1 contains status of the pointman (0 is in hold or follow mode, 1 is moving as a pointman, 2 is moving, but stays on the place, either waiting for the rest of the team or doesn't have the checkpoints specified). param2 contains player id (pointer) to the pointman player object.

SC_LEV_MES_INITSCENE

Scene was loaded and is being initialized.

SC_LEV_MES_RELEASESCENE

The game scene is being closed and released.

SC_LEV_MES_ARTILLERY

Artillery support is used, the bombs are falling, param4 contains coordinates of the centre of the explosions.

SC_LEV_MES_LOUDSHOTCALLBACK

This is callback for the SC_GetLoudShot(). param1 - contains pl_id of player who has shot, param4 is the position of the shot

SC_LEV_MES_JUSTLOADED

The game was loaded from the savegame.

SC_LEV_MES_MUSICDONE

The music finished playing, param1 contains music id.

SC_LEV_MES_LIGHTSTICK_USED

Human PC used the lightstick.

SC_LEV_MES_STORYSKIP

Story skip was enabled with the SC_StorySkipEnable and PC pressed the ESC, SPACE or RETURN key.

SC_LEV_MES_GETMUSIC

Callback from the music system requesting setting of the new music. param1 contains the music id from the script, param2 is used to set the sound music id.

For more information about callbacks click on their ID or see here.


### Structure s_SC_P_info - player script

Declaration:


```c
typedef struct{
dword message,param1,param2;
dword pl_id;
void *pos;
float elapsed_time;
float next_exe_time;
}s_SC_P_info;
```

This is the structure containing data sent to the player script. pl_id contains the pointer to the player valid for the script, pos contains info about position of the player. Message, param1 and param2 contains information about the script call. Values elapsed_time and next_exe_time are used to set the next time for the time tick execution.

*Type of the messages:*

SC_P_MES_TIME

Time tick.

SC_P_MES_HIT

Player was hit. The param1 contains pl_id of shooter, but CAN BE 0 in some special cases, test the value for the zero before you will use it!

SC_P_MES_EVENT

Some other script sent a message to the player script using the SC_P_ScriptMessage. param1 and param2 contain the specified parameters.

SC_P_MES_DOANIMEND

Player finished playing of the forced animation from the SC_P_DoAnim function.

SC_P_MES_INTERACT_GETTEXT

Human PC is near the player and pointing at him, engine requests text id for the possible interaction. Text ID is set to the param1 in the script, if zero, no interaction will be possible.

SC_P_MES_INTERACT_DO

Interaction was enabled and PC used it.

SC_P_MES_DROPOUTCAR

The player fell out of the vehicle.

SC_P_MES_KILLED

Player was killed. The param1 contains pl_id of shooter, but CAN BE 0 in some special cases, test the value for the zero before you will use it!

SC_P_MES_SHOTAROUNDCALLBACK

Someone shoots near the player (the bullets are passing nearby) and this callback was enabled with the SC_P_Ai_GetEnemyShotAround function. param1 contains pl_id of the shooter.

SC_P_MES_GOTOPC

PC is using the quick key to call the player by his side. If the script leaves the param1 at zero, player will acknowledge the order and will run to the PC. 1 means the player will acknowledge the order, but the engine will not issue the order to move to PC. 2 will mean the engine does nothing.

For more information about player script messages see here.


### Structure s_SC_SOUND_info - sound script

Declaration:


```c
typedef struct{
dword message;
}s_SC_SOUND_info;
```

This structure is used for the sound script. Message can contain only SC_SOUND_MESSAGE_INIT - sound script is being initialized.


### Structure s_SC_ScriptHelper_info - script helper script

Declaration:


```c
typedef struct{
dword event_type;
s_sphere sph;
void *nod;
float elapsed_time;
float next_exe_time;
}s_SC_ScriptHelper_info;
```

This structure is used for storing the data for the callbacks to the script helper objects. Event_type contains type of the callback, sph is filled with the data valid for the script helper object (valid sphere), nod is the pointer to the object. Elapsed_time contains time from the last time tick, next_exe_time is used to set the time of the next time tick.

Types of the message:

SC_SCRHELPER_EVENTTYPE_INIT

Script helper is being initialized during the scene initialization.

SC_SCRHELPER_EVENTTYPE_RELEASE

Script helper is being released during the scene release.

SC_SCRHELPER_EVENTTYPE_TIMETICK

Time tick.


### Structure s_SC_OBJ_info - dynamic object script

Declaration:


```c
typedef struct{

dword event_type;
void *master_nod;
void *nod;
float new_hp_obtained;
dword hit_by;
c_Vector3 *world_pos;
c_Vector3 *world_dir;
float time;
}s_SC_OBJ_info;
```

This structure is used for storing the data for the callbacks to the object scripts. Event_type contains type of the callback, master_nod is the pointer at the master object (which has the script assigned to itself), nod is used for some callbacks as a specified subobject. If the message deals with the damage, new_hp_obtained contains the information about how much damage was already dealt to the object, hit_by can be either SC_OBJ_HIT_BY_MISSILE (object hit by generic shot), SC_OBJ_HIT_BY_EXPLOSION (object hit by the explosion) or SC_OBJ_HIT_BY_MISSILE_PC (object was hit by PC's shot). world_pos and world_dir contain the information about the world position and rotation of the object. Float variable time contains time in second from the last execution.

*Type of the messages:*

SC_OBJ_INFO_EVENT_HIT

The object was hit. Variable hit_by specifies type of the damage dealt, new_hp_obtained contains overall damage dealt to the object inluding this hit. nod is the pointer to the hit sub object.

SC_OBJ_INFO_EVENT_SET

This is callback for the multiplayer game for synchronization of the object status on all client machines. It has same specification as the SC_OBJ_INFO_EVENT_HIT.

SC_OBJ_INFO_EVENT_INIT

This is the callback during the scene initialization (after the level script received the init message, all object scripts receive theirs). This is useful for storing basic default information about the transformation of the object.

SC_OBJ_INFO_EVENT_DOTICK

This is the time tick of the object. Engine calls the object script time tick every frame, variable time contains time in seconds from the last execution.

SC_OBJ_INFO_EVENT_RELEASE

This callback is executed during the release of the game - useful for reseting the object to it's original transformation.

SC_OBJ_INFO_EVENT_USED

The object has enabled interaction with the SC_ACTIVE_Add function and was used by the PC.

SC_OBJ_INFO_EVENT_JUSTLOADED

This callback is executed just after the game was loaded from the saved game. Some of the data about objects are not stored, so this callback is usually used to set them correct, see example scripts.

SC_OBJ_INFO_EVENT_MOUNTEDSHOT

This is specific callback for the object defined as the mounted weapon platform - every time the player shoots, this message is sent to the script.


### Structure s_SC_NET_info - network script

Declaration:


```c
typedef struct{
dword message,param1,param2,param3;
float elapsed_time;
float fval1;
}s_SC_NET_info;
```

This structure is used to pass the data to the multiplayer network script. message contains type of the message, param1-param3 are dword parameters specific for each message, fval1 is float parameter variable, elapsed_time contains time from the last time tick. See here for details on each message here.

*Type of the messages:*

SC_NET_MES_UNDEFINED

Undefined message.

SC_NET_MES_LEVELINIT

This message is passed to the script every time the level initializes. Param1 can be either TRUE (this is the server script) or FALSE (this is the client script). Param2 is TRUE if this is first time init, FALSE if this is subsequent reinitialization.

SC_NET_MES_RENDERHUD

This message is passed to the script every frame rendered and it is used to write to the HUD. If the param1 is TRUE, this is the script running on the dedicated server.

SC_NET_MES_SERVER_TICK

This is the time tick for the server script.

SC_NET_MES_CLIENT_TICK

This is the time tick for the client script.

SC_NET_MES_SERVER_RECOVER_TIME

This is the request from the engine to the script to fill the fval1 with the recover time for the player with the pointer stored in the param1. For special cases you can use the SC_NET_SERVER_RECTIME_NEVER value (never recover the player) or SC_NET_SERVER_RECTIME_ENDOFROUND (recover at the end of the round). Param2 contains the information about the type of the recover, if 0 the player was just killed, if 1 the player just entered the game.

SC_NET_MES_SERVER_RECOVER_PLACE

This is the request from the engine for the recover place of the player specified by pointer in the param3. Param1 contains the side which will be used for the player after the recover. Recover place is filled to the param2 as a pointer to the structure s_SC_MP_Recover *.

SC_NET_MES_SERVER_KILL

This is the information to the server script about death of player specified in the param1, param2 contains pointer to the player who made the kill.

SC_NET_MES_MESSAGE

This is the message to the network script from other script using the SC_MP_ScriptMessage function. Param1 and param2 contains the specified parameters.

SC_NET_MES_LEVELPREINIT

This is the level preinitialization message (the level was not loaded yet). Param1 contains the value of the end rule, param2 the end value.

SC_NET_MES_RESTARTMAP

This means the map will be restarted, used to clear statistics, end rules and for recovering the players.

SC_NET_MES_RULESCHANGED

This is the message about changing of the rules.


### Structure s_SC_WEAP_info - weapon fpv script

Declaration:


```c
typedef struct{
dword event_type;
void *obj;
void *weap_type;
dword anim_id;
float anim_time;
float prev_time;
c_Vector3 pos;
dword cur_batch;
dword cur_ammo;
dword cur_phase;
float param1;
dword cur_bayonet;
dword weap_phase;
float step_time;
}s_SC_WEAP_info;
```

This structure contains data for calling weapon fpv script. Event type contains type of the event calling the script, it can be:

#define SC_WEAP_EVENTTYPE_SET 1

#define SC_WEAP_EVENTTYPE_INIT 2

#define SC_WEAP_EVENTTYPE_RELEASE 3

#define SC_WEAP_EVENTTYPE_VALIDATEANIM 4

#define SC_WEAP_EVENTTYPE_GETANIMTIME 5

For more information see weapon fpv script.


### Structure s_SC_WEAP3pv_info - weapon 3pv script

Declaration:


```c
typedef struct{
dword event_type;
void *obj;
void *weap_type;
dword cur_batch;
dword cur_ammo;
dword cur_phase;
dword pl_id;
dword cur_bayonet;
}s_SC_WEAP3pv_info;
```

This structure is used for 3pv weapon scripts.


## Structures - player data structures


### Structure s_SC_P_Create

Declaration:


```c
typedef struct{
dword type;
dword side;
dword group;
dword member_id;
dword name_nr;
dword debrief_group;
char *inifile;
void *recover_pos;
char *icon_name;

dword flags;

dword weap_knife;
dword weap_pistol;
dword weap_main1;
dword weap_main2;
dword weap_slot1;

dword weap_slot6;
dword weap_slot7;
dword weap_slot8;
dword weap_slot9;
dword weap_slot10;

dword force_sel_slot;
dword eqps;
s_SC_P_CreateEqp *eqp;

dword aeg_valid_head_bes[SC_P_CREATE_AEG_VALID_MAX];
dword aeg_valid_body_bes[SC_P_CREATE_AEG_VALID_MAX];

}s_SC_P_Create;
```

This structure is used for the player creation with SC_P_Create.

Type can be either SC_P_TYPE_PC (for the human PC) or SC_P_TYPE_AI. Side can be any created with the SC_InitSide, default values are SC_P_SIDE_US for the US soldier and SC_P_SIDE_VC for the VC soldier. Group and memberid are for the specification of the soldier, group must be created with the SC_InitSideGroup, memberid should be specific for each player.

Name_nr is text id of the players name.

debrief_group is used for the generation of the debriefing data, possible values are:

`SC_P_DEBRIEFGROUP_UNDEFINED` - undefined group.

*SC_P_DEBRIEFGROUP_SF*  - special forces/us soldier

`SC_P_DEBRIEFGROUP_LLDB` - LLDB soldier

`SC_P_DEBRIEFGROUP_CIDG` - CIDG trooper

`SC_P_DEBRIEFGROUP_CIVIL` - civilian

`SC_P_DEBRIEFGROUP_VC` - vietcong/nva soldier

inifilename is a pointer to the string containing the player model initialization file.

recover_pos is the position the player should be recovered at (the info structure contains default value).

icon_name is the name of the icon used to show the face of the soldier at the HUD.

Flags specify the type of the creation, possible values (combine them with the logical AND) are:

`SC_P_CREATE_FL_MP_RECOVER` - player is recovered by multiplayer script.

`SC_P_CREATE_FL_DISABLE_EQPGEN` - disables automatic equipment generation if the number of the equipment (eqps) is zero.

`SC_P_CREATE_FL_CROUCH` - player is created crouching.

`SC_P_CREATE_FL_INACTIVE` - create player as inactive.

`SC_P_CREATE_FL_FORCESELSLOT` - this is valid only for the PC, player will be created with selected weapon in slot specified in the value force_sel_slot.

Weap_knife, weap_pistol, weap_main1, weap_main2 and other weap_ variables are used to set the specified equipment.

Force_sel_slot is valid only if the flags contain SC_P_CREATE_FL_FORCESELSLOT, PC will be created with selected weapon set to the specified slot.

Eqps is the number of the equipment in the array s_SC_P_CreateEqp eqp.

aeg_valid_head_bes and aeg_valid_body_bes are used to specify the valid automatically generated equipment.

For more about the equipment of the player see here.


### Structure s_SC_P_CreateEqp

Declaration:


```c
typedef struct{
char *bes;
char *eqp;
}s_SC_P_CreateEqp;
```

This is the data structure used to store the data about equipment linked to the player. Bes is pointer to the string containing path to the bes gfx file, eqp is string with the path to the eqp file.


### Structure s_SC_P_SpecAnims

*Definition:*


```c
typedef struct{
char *sa[SC_PL_SA_MAX];
}s_SC_P_SpecAnims;
```

This data structure is used by the SC_P_SetSpecAnims function. It contains array of special animations for various situations, they are stored as the filename/path relative to the G\CHARACTERS\Anims\specmove\. NULL means no special animations will be used. Indexes in the array are:

`SC_PL_SA_STATIV` - special static animation for the player until he sees the enemy.

*SC_PL_SA_ENEMYSPOTTED -* this animation will be used to change from the special stativ to the system stativ.

*SC_PL_SA_WALK -* special animation used for the walking.

`SC_PL_SA_RUN` - special animation used for the running.

`SC_PL_SA_DEATH` - special death animation


### Structure s_SC_P_intel

Declaration:


```c
typedef struct{
dword intel[SC_P_INTEL_MAX];
}s_SC_P_intel;
```

This structure is used to store the data about the acquired intelligence documents for the functions SC_PC_SetIntel and SC_PC_GetIntel.


### Structure s_SC_P_getinfo

Declaration:


```c
typedef struct{
float cur_hp,max_hp;
dword side;
dword group;
dword member_id;
}s_SC_P_getinfo;
```

This data structure is used to acquire basic information about player with the SC_P_GetInfo function.

cur_hp contains current hit points of the player, max_hp is maximum hit points of the player. Side, group and memberid are unique identifiers of the player.


## Structures - AI data


### Structure s_SC_P_AI_props

Declaration:


```c
typedef struct{

float max_vis_distance;
float watchfulness_zerodist;
float watchfulness_maxdistance;
float boldness;
float coveramount;
float shoot_imprecision;
BOOL extend_searchway;
float shortdistance_fight;
float view_angle;
float view_angle_near;
float hear_imprecision;
float hear_distance_mult;
float hear_distance_max;
float grenade_min_distance;
float grenade_timing_imprecision;
float grenade_throw_imprecision;
float grenade_sure_time;)
float forget_enemy_mult;
float shoot_damage_mult;
BOOL disable_peace_crouch;
float peace_fakeenemy_run;
float peace_fakeenemy_phase;
float shoot_while_hidding;
float reaction_time;
float scout;
float berserk;
float aimtime_max;
float aimtime_canshoot;
float aimtime_rotmult;
float wounded_start_perc;
float wounded_aimtime_mult_max;
float wounded_shoot_imprec_plus;

}s_SC_P_AI_props;
```

This structure is used to store the basic AI properties for the functions SC_P_Ai_GetProps and SC_P_Ai_SetProps.

*max_vis_distance* - maximum visual distance the AI can see, if not specified, AI uses maximum visual distance specified for the level.

*watchfulness_zerodist* - how good is AI at recognizing the enemy at zero distance.

*watchfulness_maxdistance* - how good is AI at recognizing the enemy at maximum distance.

*boldness* - this is used to determine how bold is the AI when in cover and under fire. 0.5 is very cautious player, 2 is medium, 4 is high. 10 is almost suicidal, the AI will not give a damn if someone is shooting at him.

*coveramount* - how far the AI will run for cover compared to the distance to the closest enemy, default is 0.5.

*shoot_imprecision* - this is the imprecision of the AI shooting. 0 mean absolutely precise, 1 is about default, 2 or more means the AI is very imprecise.

*extend_searchway* - use the extended search way algorism? Usually used only for the PC team, more time consuming.

*shortdistance_fight* - use the short distance time? 1 means as much as possible, 0 never. Computing is very expensive, use about 0.2 for the enemies, 1 only for the PC team.

*view_angle* - view angle of the AI in radians, default is 2.5f.

*view_angle_near* - view angle for the close distances.

*hear_imprecision -* imprecision of the AI's hearing. 0 absolute hearing, 1 average, 5 very bad.

*hear_distance_mult* - hear distance multiplier - 0.5 is half, 2 is two times better.

*hear_distance_max* - maximum hearing distance.

*grenade_min_distance* - minimum distance AI will throw the grenade.

*grenade_timing_imprecision* - this is maximum time (will be randomized) between impact of the grenade and it's explosion.

*grenade_throw_imprecision* - imprecision of the grenade throwing. 0 perfect, 1 average, 2 quite bad.

*grenade_sure_time* - how long the AI will wait until it's sure the situation demands a grenade.

*forget_enemy_mult*  - how fast will the AI forgot the enemies it has no more contact? 1 is default, 0.5 means two times slower, 2 mean two times faster.

*shoot_damage_mult* - this is multiplier used for calculating the damage AI deals - for losers use 0.1 :)

*disable_peace_crouch -* this disables AI crouching in the peace mode.

*peace_fakeenemy_run* - this is used to set the movement type under the fake enemy situation. 1 means always run, 0 always walk, 0.5 use run/walk 1:1.

*peace_fakeenemy_phase* - same as previous, only for the stand/crouch.

*shoot_while_hidding* - if enabled the AI will shoot even when moving to the hide out.

*reaction_time* - this is the reaction time when first spotting the enemy. Default 0 for the US, 1 for the VC.

*scout -* sets if AI goes to check spotted first enemies (0-never, 1 - ever), default is 0.0f

berserk - used for AI in the attack mode, how often attack without covering, (0-never, 1 - ever), default is 0.0f

*aimtime_max* - maximum time for AI to take an aim, default 0.7 seconds

*aimtime_canshoot* - minimum time for AI to take an aim, default 0.1 seconds.

*aimtime_rotmult* - multiplier of the rotation speed when aiming, default 0.5 seconds.

*wounded_start_perc* - value of the current hp/max hp when the AI aiming starts to be worse

*wounded_aimtime_mult_max* - multiplier for the maximum aim time when hit points of the AI is zero.

*wounded_shoot_imprec_plus* - multiplier for the maximum aim imprecision when hit points of the AI is zero.


### Structure s_SC_P_Ai_BattleProps

Declaration:


```c
typedef struct{
float Position;
float Aim;
float Run;
}s_SC_P_Ai_BattleProps;
```

This data structure is used to set the battle properties of the AI with the SC_P_Ai_SetBattleProps function. Variables can have values from 0 to 1. Variable Position specifies which position should AI prefer in the battle (0 always stand, 1 always crouch), Aim specifies how much will the AI use the aiming (0 never, 1 always), Run is the preferred speed (0 always walk, 1 always run).


### Structure s_SC_P_Ai_Grenade

Declaration:


```c
typedef struct{
dword valid_uses; // default is 100 float use_interval; // default is 30.0f float cur_interval; // default is 0.0f
}s_SC_P_Ai_Grenade;
```

This structure is used for the functions SC_P_Ai_GetGrenateProps and SC_P_Ai_SetGrenateProps to modify the usage of the grenades by the AI. Valid_uses is the maximum number of use of the grenades, use_interval is minimum time interval between the usage of the grenade, cur_interval is decreasing by the engine when valid uses >0 (used to determine if the AI can throw the grenade).


### Structure s_SC_Ai_PlFollow

Declaration:


```c
typedef struct{
float min_dist,max_dist;
c_Vector3 follow_change;
}s_SC_Ai_PlFollow;
```

This structure is used to store data for the follow/point mode with the SC_Ai_SetPlFollow function. min_dist and max_dist are minimum and maximum distances from the previous player, follow_change is the positional change.


## Structures - dynamic object structures


### Structure s_SC_OBJ_dynamic

Declaration:


```c
typedef struct{
c_Vector3 velocity;
float rot_speed;
c_Vector3 rot_axis;
}s_SC_OBJ_dynamic;
```

This structure is used to set the dynamics to the dynamic object with the function SC_NOD_AddDynamic. velocity is a speed vector, rot_speed specifies the speed of the rotation while rot_axis specifies the rotation axis.


### Structure s_SC_NOD_transform

Declaration:


```c
typedef struct{
c_Vector3 loc;
c_Vector3 rot;
c_Vector3 scale;
}s_SC_NOD_transform;
```

This is the transformation data structure used for the SC_NOD_GetTransform and SC_NOD_SetTransform functions. loc is the location of the object, rot it's rotation and scale it's scale.


### Structure s_SC_Car_Init

Declaration:


```c
typedef struct{

void *master_nod;

void *steeringwheel_nod;
float steeringwheel_max_rot;

float steer_max;
float steer_speed;
float steer_backspeed;
float steer_curse[11];
float steer_max_mult_at10mpersec;
float steer_speed_mult_at10mpersec;
float steer_backspeed_mult_at10mpersec;

float eng_max_revs;
float eng_freewheel_revs; volnobehu float eng_revs_slowdown;
float eng_min_revs;
c_Vector3 eng_sound_pos;

float eng_freqmult_1,eng_freqmult_revs1;
float eng_freqmult_2,eng_freqmult_revs2;

dword eng_snd_id;

dword eng_val_steps;
float *eng_Nm;
float *eng_kW;
float *eng_sound_volume;

float trns_delay;
dword trns_gears;
float *trns_gear;

float brake_power;

}s_SC_Car_Init;
```

This function is used to initialize the car. See example scripts for more information.


### Structure s_SC_Car_AddWheel

Declaration:


```c
typedef struct{

c_Vector3 body_point;
c_Vector3 body_vector;
float spring_tmin;
float spring_tmax;
float spring_t;
float spring_absorber;
float spring_looser;
float spring_rate;
float wheel_radius;
float wheel_friction;
float wheel_aspd;
BOOL wheel_with_drive;
BOOL steering;
BOOL left_side;

float wheel_fr_min;
float wheel_fr_dspd;

float ptc_v0_mult;
float ptc_v1_mult;

}s_SC_Car_AddWheel;
```

This structure is used to initialize wheel on the car. See example scripts for more information.


### Structure s_SC_Car_AddEntry

Declaration:


```c
typedef struct{
dword function;
dword entry_name_nr;
dword exit_name_nr;
c_Vector3 entry;
float entry_dist;
c_Vector3 target;
c_Vector3 view;
float min_rx,max_rx;
float min_rz,max_rz;

float shoot_min_rz,shoot_max_rz;
dword switch_3pv_anim_dir;

char *stg_dir;
BOOL can_shoot;
BOOL disabled_for_PC;
float rz;

}s_SC_Car_AddEntry;
```

This structure is used to initialize entry point for the vehicle. See example scripts for more information.


### Structure s_SC_Ship_Init

Declaration:


```c
typedef struct{

void *master_nod;
float steer_max;
float steer_speed;
float steer_backspeed;

float eng_max_revs;
float eng_freewheel_revs;
float eng_revs_slowdown;

c_Vector3 eng_sound_pos;
c_Vector3 drive_pos;

float eng_freqmult_1,eng_freqmult_revs1;
float eng_freqmult_2,eng_freqmult_revs2;

dword eng_snd_id;

float power_front,power_back;

}s_SC_Ship_Init;
```

This structure is used to initilize the ship. See example scripts.


### Structure s_SC_PHS_IWantToFloat

Declaration:


```c
typedef struct{

c_Vector3 _env_normal;
c_Vector3 _hydI;
c_Vector3 _hydJ;
c_Vector3 _hydK;
float _CI;
float _CJ;
float _CK;
float _QR;
float _QI;
float _QJ;
float _QIJ;
float _FK;

}s_SC_PHS_IWantToFloat;
```

This structure is used to initilize float properties of the ship. See example scripts.


### Structure s_SC_Heli_Init

Declaration:


```c
typedef struct{

void *master_nod;
dword eng_snd_id;
dword snd2_id;
float snd2_turndown_dist;
float snd2_zerodist_volume;
dword flags;

}s_SC_Heli_Init;
```

This structure is used to initilize the helicopter.

*master_nod* is link to the nod which will be used as a chopper body

*eng_snd_id* is engine sound id, each chopper must have it's own sound (for possible id look in the examples)

*snd2_id* is secondary sound id (used for sound made by propeller)

*snd2_turndown_dist* is distance where secondary sound starts to fadeout

*snd2_zerodist_volume* is volume of the secondary sound at zero distance

*flags* are used to specify some special properties. Currently it may be either zero or SC_HELI_INIT_FL_DISABLE_GROUNDDUST - which means chopper will not create dust particles when near land (use for choppers landing in swamp areas etc).

For more information see example scripts.


### Structure s_SC_MWP_Create

Declaration:


```c
typedef struct{
dword weap_type;
dword use_info_txt_id;
dword exit_info_txt_id;
void *master_nod;
void *nod_base;
void *nod_rotate_x;
void *nod_rotate_z;
void *nod_rotate_last;
void *nod_fpv_camera;
void *nod_active_pos;
void *nod_muzzle;
void *nod_entry;
float active_rad;
float active_dist;
float rotate_zmin,rotate_zmax;
float rotate_xmin,rotate_xmax;
float rotate_speed;
float flash_rot_step;
dword link_at;
void *link_ptr;
dword link_entry_index;
char *anim_dir;

}s_SC_MWP_Create;
```

This structure is used to initialize mounted weapon from static dynamic object or vehicle.

See examples. Also see initialization of the MWP on the chopper.


## Structures - multiplayer data


### Structure s_SC_MP_EnumPlayers

Declaration:


```c
typedef struct{

dword id;
dword side;
dword status;
char *name;

}s_SC_MP_EnumPlayers;
```

This structure is used to enumerate all players in the game with the SC_MP_EnumPlayers function. id is the pointer to the player, side is the side, name is the name of the player. Value status is valid only on the server machine, it can be:

`SC_MP_P_STATUS_NOTINGAME` - player is not in the game

`SC_MP_P_STATUS_INGAME` - player is in the game

`SC_MP_P_STATUS_INGAMEDEATH` - player is dead


### Structure s_SC_MP_Recover

Declaration:


```c
typedef struct{
c_Vector3 pos;
float rz;
}s_SC_MP_Recover;
```

This structure is used to store the data about recover place. Vector pos is the position, rz is the rotation around the z axis.


### Structure s_SC_MP_hud

Declaration:


```c
typedef struct{

dword title;
BOOL use_sides;
BOOL disableUSside;
BOOL disableVCside;

dword side_name[2];
dword side_color[2];

dword pl_mask;
dword side_mask;
dword sort_by[5];

}s_SC_MP_hud;
```

This structure is used for the SC_MP_HUD_SetTabInfo function and is used to set what is shown on the screen when the player presses the MP info key (TAB by default).

*title* is the text identifier for the title of the window. Possible default values are:

1071 Vietcong: Capture the flag

1072 Vietcong: Assault Team Game

1048 Vietcong: ATG, search and destroy!

1179 Vietcong: Real War

1050 Vietcong: DeathMatch

1051 Vietcong: Team DeathMatch

1052 Vietcong: Last Man Standing is King of the jungle

1098 Vietcong: Cooperative

1083 Vietcong: Capture the Radio

1090 Vietcong: Save the Pilot

5100 TurnTable

*use_sides* can be used to enable or disable sorting the players by their side.

*disableUSside* or *disableVCside* can be set to TRUE if you do not want to list the players from US or VC side.

*side_name* is array with size 2 containg the text identifiers for the name of the sides (use 1010 and 1011 for default names).

*side_color* is the RGB color for the sides

*pl_mask* are the flags for what should be shown for the player. Use | operator for more flags. Flags can be:

SC_HUD_MP_PL_MASK_CLASS - show class

SC_HUD_MP_PL_MASK_POINTS - show points

SC_HUD_MP_PL_MASK_FRAGS - show frags

SC_HUD_MP_PL_MASK_KILLS - show kills

SC_HUD_MP_PL_MASK_DEATHS - show deaths

SC_HUD_MP_PL_MASK_PINGS - show ping|

*side_mask* is the mask for what to show for each side. Possible values are:

SC_HUD_MP_SIDE_MASK_POINTS - show points

SC_HUD_MP_SIDE_MASK_FRAGS - show frags

*sort_by* is the array with sort options for the players. Game will first sort the players according the value at the sort_by[0], then by sort_by[1] etc. Possible values are:

SC_HUD_MP_SORTBY_NONE - no sort

SC_HUD_MP_SORTBY_POINTS - sort by points

SC_HUD_MP_SORTBY_FRAGS - sort by frags

SC_HUD_MP_SORTBY_KILLS - sort by kills

SC_HUD_MP_SORTBY_DEATHS - sort by deaths

SC_HUD_MP_SORTBY_PINGS - sort by ping

You can also aply flag SC_HUD_MP_SORT_DOWNUP to any value with logical or operator and the sorting will be done from least size to highest.


### Structure s_SC_HUD_MP_icon

Declaration:


```c
typedef struct{
dword icon_id;
dword type;
int value;
dword color;
}s_SC_HUD_MP_icon;
```

This structure is used for showing various icons on the screen, not just for multiplayer, with SC_MP_SetIconHUD function. This structure is used to define one icon.

*icon_id -* index to the array of the icons

*type -* type of the icon, can be

SC_HUD_MP_ICON_TYPE_NONE - none

SC_HUD_MP_ICON_TYPE_NUMBER - number

SC_HUD_MP_ICON_TYPE_TIME - time

*value -* four bytes with the value of the icon

*color -* this is the ARGB color for the icon.


### Structure s_SC_MP_SRV_settings

Declaration:


```c
typedef struct{
dword coop_respawn_time;
dword coop_respawn_limit;
dword dm_weap_resp_time;
dword atg_class_limit[6];
}s_SC_MP_SRV_settings;
```

This data structure is used to acquire information about the server settings in the multiplayer game with the function SC_MP_GetSRVsettings.


### Structure s_SC_MP_SRV_AtgSettings

Declaration:


```c
typedef struct{
float ATG_round_time;
float tt_respawntime;
float tt_timelimit;
}s_SC_MP_SRV_AtgSettings;
```

This data structure is used to acquire information about the server settings for the ATG in the multiplayer game with the function SC_MP_SRV_GetAtgSettings.


## Structures - various data structures


### Structure s_SC_systime

Declaration:


```c
typedef struct{
int hours;
int minutes;
int seconds;
int msec;
}s_SC_systime;
```

This data structure is used to store the computer system time for the function SC_GetSystemTime.


### Structure s_SC_FpvMapSign

Declaration:


```c
typedef struct{
dword id;
dword color;
float scale;
c_Vector3 pos;
}s_SC_FpvMapSign;
```

This structure is used to place the signs on the FPV map with SC_MP_FpvMapSign_Set.

*id* is the identifier of the sign acquired with the SC_MP_FpvMapSign_Load function.

*color* is the ARGB color of the sign

*scale* is the scale of the sign (1 is default)

*pos* is the position for the sign in the scene.


### Structure s_SC_HUD_TextWrite

Declaration:


```c
typedef struct{
float fade_in_time;
float stay_in_time_begin;
float stay_in_time_end;
float fade_out_time;

float current_time;

dword font_id;
dword text_id;
dword color;

int alignx;
int aligny;

int max_num_lines;
float scale_ratio;

}s_SC_HUD_TextWrite;
```

This data structure is used for the showing of specific text on the screen (used in the outro of the Fist Alpha) with the function SC_HUD_TextWriterInit.

Text|_id is the text identifieer, font_id is the font identifier, color is used for the color of the text. Scale_ratio is used to scale the font, max_num_lines limits the maximum number of the lines. Alignx and aligny are used for the align of the text.

Fade_in_time is the time from the execution of the function when the text will start to fade in. stay_in_time_begin is the time when the text is clearly visible to the time stay_in_time_end. After this time mark the text will start to fade out up to the time fade_out_time. Starting time can be specified with the current_time.


### Structure s_SC_Objective

Declaration:


```c
typedef struct{
dword text_id;
dword status;
}s_SC_Objective;
```

This structure is used to set the ingame objectives with the SC_SetObjectives or SC_SetObjectivesNoSound. text_id is the identifier of the shown text, status can be:

*SC_OBJECTIVE_STATUS_VALID -* objective is valid

*SC_OBJECTIVE_STATUS_FAILED* - objective was failed

*SC_OBJECTIVE_STATUS_COMPLETE -* objective was completed


### Structure s_SC_initside

Declaration:


```c
typedef struct{
dword MaxHideOutsStatus;
dword MaxGroups;
}s_SC_initside;
```

This data structure is used for the SC_InitSide function to create the game side. MaxGroups contain the maximum number of the groups which will be in the side, MaxHideOutStatus is the number of the hideouts the side AI will remember.


### Structure s_SC_initgroup

Declaration:


```c
typedef struct{

dword SideId;
dword GroupId;
dword MaxPlayers;
float NoHoldFireDistance;
float follow_point_max_distance;

}s_SC_initgroup;
```

This data structure is used for the SC_InitSideGroup function to create the player group. SideId is the identifier of the side, GroupId of the creating group, MaxPlayers is maximum player who will be in the group. NoHoldFireDistance is the maximum distance from the enemy the AI will shoot. follow_point_max_distance is valid for the group in the pointman mode, it's the maximum distance between pointman and last member of the group, if the distance is bigger, the pointman will wait.


### Structure s_SC_SpeachBreakProps

*This structure is now obsolete and no longer used.*


### Structure s_SC_MissionSave

Declaration:


```c
typedef struct{
dword savename_id;
dword description_id;
BOOL disable_info;
}s_SC_MissionSave;
```

This data structure is used for the autosave with the function SC_MissionSave. savename_id and description_id are text ids for the name and description. disable_info is used to disable the saving of the actual screenshot to the save game.


### Structure s_SC_DebriefInfo

Declaration:


```c
typedef struct{

float missionTime;
dword difficulty;
dword missionStatus;
//friendly losses
dword SF;
dword LLDB;
dword CIDG;
dword Heli;
dword Jeep;
//statistics
dword VC;
dword Gaz;
dword Boobytrap;
dword Caches;
dword Tunnels;
dword Facilities;
dword Intelligence;
//personal statistics
dword Bangs;
dword Defort;
dword Hornster;
dword Nhut;
dword Bronson;
dword Crocker;

}s_SC_DebriefInfo;
```

This structure is used for storing and showing the debriefing information. It contains data about


### Structure s_SC_light

Declaration:


```c
typedef struct{
float r,g,b;
float rad;
c_Vector3 pos;

float time;
BOOL decrease_radius;
}s_SC_light;
```

This data structure is used for creating of the light with the function SC_CreateLight. R, g and b are used for the color, rad is radius of the light, pos is the centre of the light. Time specifies for how long the light will shine.


### Structure s_MusicDef

Declaration:


```c
typedef struct{

int musId;
int musVol;
float musFadeIn;
float musPlayTime;
float musFadeOut;
int heliVol;
int gameVol;
int natureVol;

}s_MusicDef;
```

This structure is used to set the music system in the level script callback SC_LEV_MES_GETMUSIC.

*musId -* id of the music

*musVol* - volume of the music

*musFadeIn -* how long will the music fade in

*musPlayTime -* how long will the music play

*musFadeOut* - how long will music fade out

*heliVol* - sets the helicopter sounds volume during music playing

*gameVol -* sets the game sounds volume during music playing

*natureVol -* sets the nature sounds volume during music playing


### Structure s_SC_BombInfo

Declaration:


```c
typedef struct{
dword chats[9];
dword radistmarks;
dword radiomarks;
}s_SC_BombInfo;
```

This data structure is used to set the single player radist chat with the artillery support with the function SC_SetBombInfo. Radistmarks and radiomarks are the first speech index for counting, array chat is filled with the speech data between the radioman and the artillery support. See example scripts.


### Structure s_SC_FlyOffCartridge

Declaration:


```c
typedef struct{
void *weap_type;
void *from;
c_Vector3 dir;
c_Vector3 add_rot;
}s_SC_FlyOffCartridge;
```

This data structure is used for the function SC_FPV_FlyOffCartridge. It will create cartridge model and eject it from the weapon.

*weap_type -* for mounted weapon it should be 1, for other weapons it should be info->weap_type

*from -* start vector of the cartridge

*dir -* direction vector

*add_rot -* rotation vector


## Functions - basic

These are the basic engine and C functions.


### int sprintf(char *, const char *, ...);

This is the standard sprintf function. Refer to the standard C help files.


### int swprintf(ushort *, ushort*, ...);

This is the standard sprintf function. Refer to the standard C help files.


### int rand(void);

This function returns the random integer number.


### float frnd(float max);

This function return random float number up to the specified maximum.


### float sqrt(float val);

This function returns the radix of the value.


### float fmod(float a, float b);

This function returns the remainder from division of the float numbers.


### float sin(float a);

This function returns the sinus of the value a.


### float cos(float a);

This function returns the sinus of the value a.


### float atan2(float y, float x);

This function returns the atan.


### ushort* SC_Wtxt(dword val);

This function will return pointer to the string from the text database with the specified id.


### BOOL SC_StringSame(char *a, char* b);

This function will compare two strings and return true if they are same.


### void SC_ZeroMem(void *ptr, dword size);

This function will fill the specified portion of the memory with zeroes. Used in the CLEAR macro.


### float SC_GetLineDist(c_Vector3 *pos, c_Vector3* line_a, c_Vector3 *line_b);

This function will return the distance of the vector pos from the line between vectors line_a and line_b.


### float SC_GetLineDistXY(c_Vector3 *pos, c_Vector3* line_a, c_Vector3 *line_b);

This function will return the distance of the vector pos from the line between vectors line_a and line_b limited to the 2d space (without z coordinate).


### BOOL SC_IsNear2D(c_Vector3 *a, c_Vector3* b, float dist);

This function will return TRUE if the vector a is at the distance dist from the vector b or closer, this function works only in the 2D space, no z coordinate.


### BOOL SC_IsNear3D(c_Vector3 *a, c_Vector3* b, float dist);

This function will return TRUE if the vector a is at the distance dist from the vector b or closer.


### float SC_2VectorsDist(c_Vector3 *a, c_Vector3* b);

This function returns the distance between vectors a and b.


### float SC_VectorLen(c_Vector3 *vec);

This function returns the length of the vector vec.


### float SC_VectorLen2(c_Vector3 *vec);

This function returns the (length of the vector vec)* (length of the vector vec).


### BOOL SC_SphereIsVisible(s_sphere *sph);

This function will return TRUE if at least part of the sphere sph is visible on the screen.


### void SC_GetPos_VecRz(void *cpos, c_Vector3* pos, float *rz);

This function will fill the vector pos with the world position according to the transformation cpos and rz with the z rotation value.


### ushort *SC_AnsiToUni(char* src, ushort *dest);

This function will convert ANSI text to UNICODE.


## Functions - the debug functions

These functions are used during the script debuging.


### void SC_message(char *txt,...);

This function will show the text with formated parameters in the dialog window.


### void SC_Log(dword level, char *txt, ...);

This function will write the text with formated parameters to the log file. Variable level is used to determine the value of the log, 0 is fatal error, 1 is error, 2 is warning, 3 is information.


### void SC_Osi(char *txt,...);

This function will show the text with formated parameters in the status line.


### BOOL SC_KeyJustPressed(dword id);

This function will return TRUE if the key (directinput codes) was just pressed.


### BOOL SC_KeyPressed(dword id);

This function will return TRUE if the key (directinput codes) was pressed.


## Functions - global variables

This set of functions is used to handle the engine global variables.


### void SC_sgi(dword id, int a);

This function will set the global variable id to the integer value a.


### int SC_ggi(dword id);

This function will return the integer value of the global variable id.


### void SC_sgf(dword id, float a);

This function will set the global variable id to the float value a.


### float SC_ggf(dword id);

This function will return the float value of the global variable id.


### void SC_MP_Gvar_SetSynchro(dword id);

This function will mark the global variable id as a MP synchronized - all changes to the global variable will be synchronized for all clients.


## Functions for the sound handling

These are the function used to handle the sound and music.


### void SC_SND_MusicPlay(dword MusicID, dword StartVolume );

This function will play the music MusicID with the volume StartVolume.


### void SC_SND_PlayMusic(dword music_id);

This is obsolete function and it should not be used.


### void SC_SND_MusicStop(dword MusicID );

This function will stop playing of the music MusicID.


### void SC_SND_MusicStopFade(dword MusicID, dword Time );

This function will fadeout the music MusicID in the Time and stop playing it.


### void SC_SND_MusicFadeVolume(dword MusicID, dword Volume, dword Time );

This function will fade the volume of the MusicID to the Volume in Time.


### dword SC_AGS_Set(dword val);

This function is used to execute the command val to the music system.


### BOOL SC_SND_SetEnvironment(dword env1_id, dword env2_id, float env_ratio);

This function will set the sound enviroment.


### void SC_SND_Ambient_Play(dword snd_id);

This function will start the ambient sound snd_id.


### void SC_SND_Ambient_Stop(void);

This function will stop the ambient soud.


### void SC_SND_SetHearableRatio(float Ratio);

This function will set the hearable ratio to the Ratio.


### void SC_SND_CreateCurveSound(char *anm_filename, dword snd_id, float max_play_dist, BOOL apply_env_volume);

This function will create the curve sound with sound snd_id to the cuve anm_filename, sound will be hear the to distance max_play_dist. If the apply_env_volume is TRUE, the enviroment sound volume will applied to the sound curve.


### void SC_FadeSoundPlayer(dword snd_player_id, float final_volume, float fade_time);

This function will fade the sound player snd_player_id to the final_volume in time fade_time.

Possible sound playr id are:

SC_SNDPLAYER_GAME - game sound effects

SC_SNDPLAYER_SPEECH - speech

SC_SNDPLAYER_HELI - helicopter sounds

SC_SNDPLAYER_BEEP - beep sounds

SC_SNDPLAYER_NATURE - nature sounds

SC_SNDPLAYER_SCRIPT0 - special script sounds

SC_SNDPLAYER_SCRIPT1 - special script sounds


### float SC_SND_GetSoundLen(dword snd_id);

This function will return the length of the sound snd_id in seconds.


### void SC_SND_PlaySound3D(dword snd_id, c_Vector3 *pos);

This function will start playing 3d sound snd_id from the position pos.


### void SC_SND_PlaySound3Dex(dword snd_id, c_Vector3 *pos, float* timeout);

This function will start playing 3d sound snd_id from the position pos in a time specified in the variable timeout and set the timeout to the time of the end of the sound from the time of the function call.


### void SC_SND_PlaySound2D(dword snd_id);

This function will start playing 2d sound snd_id.


### void SC_SND_PlaySound3Dlink(dword snd_id, void *nod, float* timeout);

This function will start playing 3d sound snd_id linked to the nod nod in a time specified in the variable timeout and set the timeout to the time of the end of the sound from the time of the function call.


### void SC_SND_PlaySound3Dpl(dword snd_id, dword pl_id, dword flags);

This function will play the sound linked to the player. Flags are obsolete and are not used.


### void SC_SND_PlaySound3DSpec(dword snd_id, c_Vector3 *pos, dword spec_id);

This function will start playing 3d sound snd_id from the position pos using the special sound player. Sound players can be:

SC_SNDPLAYER_GAME - game sound effects

SC_SNDPLAYER_SPEECH - speech

SC_SNDPLAYER_HELI - helicopter sounds

SC_SNDPLAYER_BEEP - beep sounds

SC_SNDPLAYER_NATURE - nature sounds

SC_SNDPLAYER_SCRIPT0 - special script sounds

SC_SNDPLAYER_SCRIPT1 - special script sounds


### void SC_SND_PlaySound3DexSpec(dword snd_id, c_Vector3 *pos, float* timeout, dword spec_id);

This function will start playing 3d sound snd_id from the position pos in a time specified in the variable timeout and set the timeout to the time of the end of the sound from the time of the function call. The sound will be played using the spec_id sound player, which can be:

SC_SNDPLAYER_GAME - game sound effects

SC_SNDPLAYER_SPEECH - speech

SC_SNDPLAYER_HELI - helicopter sounds

SC_SNDPLAYER_BEEP - beep sounds

SC_SNDPLAYER_NATURE - nature sounds

SC_SNDPLAYER_SCRIPT0 - special script sounds

SC_SNDPLAYER_SCRIPT1 - special script sounds


### void SC_SND_PlaySound2DSpec(dword snd_id, dword spec_id);

This function will start playing 2d sound snd_id using the sound player spec_id, which can be:

SC_SNDPLAYER_GAME - game sound effects

SC_SNDPLAYER_SPEECH - speech

SC_SNDPLAYER_HELI - helicopter sounds

SC_SNDPLAYER_BEEP - beep sounds

SC_SNDPLAYER_NATURE - nature sounds

SC_SNDPLAYER_SCRIPT0 - special script sounds

SC_SNDPLAYER_SCRIPT1 - special script sounds


## Functions for the objects

These are the basic functions used for handling the gfx objects.


### void *SC_NOD_Get(void* master_obj, char *obj_name);

This function will return the pointer to the sub object with name "obj_name" in the object master_nod. If the sub object cannot be found, error message dialog will be shown.


### void *SC_NOD_GetNoMessage(void* master_obj, char *obj_name);

This function will return the pointer to the sub object with name "obj_name" in the object master_nod.


### void *SC_NOD_GetNoMessage_Entity(char* obj_name);

This function will return the pointer to the entity "obj_name".


### void SC_NOD_GetTransform(void *obj,s_SC_NOD_transform* trans);

This function will fill the transformation of the nod obj to the specified trans.


### void SC_NOD_SetTransform(void *obj,s_SC_NOD_transform* trans);

This function will set the transformation of the nod obj according specified trans.


### void SC_NOD_Hide(void *obj, BOOL hide);

This function will hide the nod obj, used only in the FPV weapon scripts.


### void SC_NOD_GetPosInOtherSpace(void *other_nod, void* nod, c_Vector3 *vec);

This function will fill the vector vec with the position of the object nod in the space of the object other_nod.


### void SC_DUMMY_Set_DoNotRenHier(char *dummy_name, BOOL do_not_render_hiearchy);

This function will enable or disable rendering of the object dummy_name and all it's subobjects.


### void SC_DUMMY_Set_DoNotRenHier2(void *nod, BOOL do_not_render_hiearchy);

This function will enable or disable rendering of the object nod and all it's subobjects.


### void SC_EnableObjectScriptWhileUnipage(void *master_nod, BOOL enable);

This function will enable or disable execution of the script of the specified object master_nod during the unipage showing.


### char *SC_NOD_GetName(void* nod);

This function will return the pointer to the name of the object nod.


### void SC_NOD_GetPivotWorld(void *nod,c_Vector3* vec);

This function will set the pivot of the object nod to the vector vec.


### void SC_NOD_GetWorldPos(void *nod, c_Vector3* pos);

This function will set the world position of the object nod to the vector pos.


### float SC_NOD_GetWorldRotZ(void *nod);

This function will return the z rotation of the object nod.


### BOOL SC_NOD_GetCollision(void *master_nod, char* name, BOOL clear_it);

This function will return TRUE if the object named "name" in the object master_nod collided with something. If the clear_it is TRUE, the information about collision will be cleared.


### BOOL SC_NOD_GetCollision2(void *nod, BOOL clear_it);

This function will return TRUE if the object nod collided with something. If the clear_it is TRUE, the information about collision will be cleared.


### void SC_NOD_GetDummySph(void *master_nod, char* dummy_name, s_sphere *sph);

This function will fill the sphere sph with the dummy sphere of the subobject named dummy_name of the object master_nod.


## Functions for the dynamic objects

These functions are used to handle the dynamic objects.


### void SC_NOD_SetDSTR(void *nod, char* obj_name, char *dstr_name);

This function will set the destroyed variant of the subobject named obj_name in the object nod to the destruction object named dstr_name.


### void SC_NOD_ResetDSTR(void *nod, char* obj_name);

This function will reset the destroyed variant of the subobject named obj_name in the object nod to the default version.


### float SC_DOBJ_CameraLooksAt(void *nod, float max_dist);

This function will determine if the camera is looking at the specified nod to the maximum distance of max_dist. This function will ignore possible collision with other object standing in the way!


### float SC_DOBJ_CameraLooksAtCollision(void *nod, float max_dist);

This function will determine if the camera is looking at the specified nod to the maximum distance of max_dist.


### void SC_ACTIVE_Add(void *nod, float cur_dist, dword info_txt);

This object will mark the object nod as possible object for the interaction with the interaction text info_txt. Value cur_dist should contain the distance of the object to the player and it is used to determine which object can be used if there are more possibilites (closest one will be used);


### void SC_DOBJ_SetFrozenFlag(void *nod, BOOL frozen);

This function will set the frozen flag of the dynamic object nod to the frozen. Frozen dynamic object will not move untill collided with or further use of the SC_DOBJ_SetFrozenFlag.


### void SC_NOD_AddDynamic(void *master_nod, char* name, s_SC_OBJ_dynamic *info);

This function will add the dymanics specified in the s_SC_OBJ_dynamic info to the subobject named name in the object master_nod.


### BOOL SC_DOBJ_IsBurning(void *nod, float perc);

This function will return TRUE, if the dynamic object nod is burning at least from the perc percent.


### BOOL SC_DOBJ_IsBurning2(void *nod);

This function will return TRUE if the dynamic object nod is burning.


### void SC_DOBJ_StopBurning(void *nod, BOOL enable_future_burning);

This function will stop burning of the dynamic object nod. enable_future_burning should be set TRUE if you want the object to be able to burn again.


### void SC_DOBJ_ClearDamagedHP(void *nod);

This function will reset the damage of the dynamic object nod to zero.


### void SC_DOBJ_BurnCreateBlockers(void *nod, s_sphere* sph, dword items);

This function will create waypoint blockers enabled if the object nod will burn.Dara for blockers are stored in the array of spheres sph with item count of items.


## Functions for the objects - animations

This set of functions is used to handle the animations of the objects.


### dword SC_MANM_Create(char *filename);

This function will create the MANM animation from the file filename and returns pointer to the animation object.

For more about using the MANM animations see here.


### void SC_MANM_Release(dword manm_id);

This function will release the animation object from the memory, use the pointer acquired from the SC_MANM_Create.

For more about using the MANM animations see here.


### dword SC_MANM_GetIndex(dword manm_id, char *objname);

This function will return the index of the object named objname from the animation manm_id.

For more about using the MANM animations see here.


### void SC_MANM_Set(dword manm_id, dword manm_index, void *nod, float time);

This function will set the object nod according the animation manm_id with corresponding object index manm_index to the time time.

For more about using the MANM animations see here.


### float SC_MANM_GetLength(dword manm_id, dword manm_index);

This function will return the length of the MANM animation manm_id for the object indexed manm_index in seconds.

For more about using the MANM animations see here.


## Functions for the view animations

This set of functions is used to handle the view animations, used either for camera animation or for moving the object in the scene.


### void SC_SetViewAnim(char *anm_name, dword start_frame, dword end_frame, dword callback_id);

This function will start the camera view animation from file anm_name from the frame start_frame to the frame end_frame. After the animation ends, the level script will receive animation callback with the id callback_id.


### void SC_SetViewAnimEx(char *anm_name, dword start_frame, dword end_frame, dword callback_id, void* nod);

This function will start the camera view animation from file anm_name linked to the object nod from the frame start_frame to the frame end_frame. After the animation ends, the level script will receive animation callback with the id callback_id.


### void SC_NOD_SetFromANM(char *anm, float time, void* nod);

This function will set the object nod to the position and rotation specified in the animation in filename anm at the time time (in seconds).


### float SC_ANM_GetFrameTime(char *anm, int frame);

This function will return the time of the animation in the file *anm* at the frame *frame*.


### BOOL SC_NOD_GetPosFromANM(char *anm, float time, c_Vector3* pos);

This function will fill the vector *pos* with the position from the animation in file *anm* in the time *time.*


## Functions for the vehicles

These are the functions used to create and handle various vehicles.


### void *SC_CAR_Create(void* nod, s_SC_Car_Init *info);

This function will create the car from the object nod according to the data stored in the structure s_SC_Car_init *info*. The function will return the pointer to the created vehicle object.


### void SC_CAR_WheelAdd(void *car, void* nod, s_SC_Car_AddWheel *info);

This function will add a wheel object *nod* to the car object *car* with data specified at the structure s_SC_Car_AddWheel *info*. The function will return the pointer to the created vehicle object.


### void SC_CAR_EntryAdd(void *car, s_SC_Car_AddEntry* info);

This function will add an entry to the car object *car* with specified parameters from the structure s_SC_Car_AddEntry *info*.


### void SC_CAR_SetAirResistance(void *car, float a0, float a1, float a2);

This function will set the air resistance of the car *car* to values a0, a1 and a2.


### void *SC_SHIP_Create(void* nod, s_SC_Ship_Init *info, s_SC_PHS_IWantToFloat* finfo);

This function will create the ship from the object *nod* according to the parameters in the s_SC_Ship_Init *info* and with float values stored in the structure s_SC_PHS_IWantToFloar *finfo*. The function will return the pointer to the created vehicle object.


### void SC_SHIP_EntryAdd(void *ship, s_SC_Car_AddEntry* info);

This function will add the entry to the ship object *ship* according the data in the structure s_SC_Car_AddEntry *info*.


### void *SC_HELI_Create(void* nod, s_SC_Heli_Init *info);

This function will create the helicopter from the object nod according to the data stored in the structure s_SC_Heli_Init *info*. The function will return the pointer to the created vehicle object.


### void SC_HELI_EntryAdd(void *heli, s_SC_Car_AddEntry* info);

This function will add the entry to the helicopter object *heli* according the data in the structure s_SC_Car_AddEntry *info*.


### void SC_HELI_ChangeEntryStativ(void *heli, dword entry_index, char* stg_name);

This function will force the change of the animation stativ in the helicopter object *heli* on the entry index *entry_index* to the animation specified by filename *stg_name.*


## Functions for the weapons


### void SC_FPV_FlyOffCartridge(s_SC_FlyOffCartridge *info);

This function will eject the cartdrige from the weapon according the data set in the structure s_SC_FlyOffCartridge *info*.


### dword SC_MWP_Create(s_SC_MWP_Create *info);

This function will create the mounted weapon platform according the data stored in the s_SC_MWP_Create *info* structure.


### void SC_FPV_AttachMagazine(BOOL render);

This function will enable/disable rendering of the magazine in the FPV weapon script.


## Functions for the visual effects

These functions are used to work with the events and particles and some other engine gfx effects.


### void SC_EventImpuls(char *ev_name);

This function will send an impuls to the engine event object named *ev_name*. If the event is set to respond only to the impuls, it will be activated.


### void SC_EventEnable(char *ev_name, BOOL enable);

This function will enable or disable engine event object *ev_name*.


### void SC_SetMissileTrace(dword color, float alpha);

This function will set the missile tracers to color *color* with the alpha *alpha.*


### void SC_CreatePtc(dword id, c_Vector3 *vec);

This function will create the particle with identifier *id* at the position specified in the vector *vec.*


### void SC_CreatePtc_Ext(dword id, void *nod, float time, float interval, float scale, float time_mult);

This function will create the particle *id* at the position of the object *nod* for *time *times*, *with intervals* interval, *scaled to the* scale *and with the time multiplied by the* time_mult.*


### void SC_CreatePtcVec_Ext(dword id, c_Vector3 *vec, float time, float interval, float scale, float time_mult);

This function will create the particle *id* at the position *vec* for *time *times*, *with intervals* interval, *scaled to the* scale *and with the time multiplied by the* time_mult.*


### void SC_CreatePtcInNodSpace_Ext(dword id, void *nod, float time, float interval, float scale, float time_mult);

This function will create the particle *id* in the world of the object *nod* for *time *times*, *with intervals* interval, *scaled to the* scale *and with the time multiplied by the* time_mult.*


### void SC_Fnt_Write(float x, float y, char *txt, float scale, dword color);

This function will write the text *txt* at coordinates *xy*, using the system font with scale *scale* and color *color.* This function can be used only in the network script message SC_NET_MES_RENDERHUD.


### float SC_Fnt_GetWidth(char *txt, float scale);

This function will return the width in pixels of the text *txt* with system font of scale *scale.*


### void SC_Fnt_WriteW(float x, float y, ushort *txt, float scale, dword color);

This function will write the unicode text *txt* at coordinates *xy*, using the system font with scale *scale* and color *color.* This function can be used only in the network script message SC_NET_MES_RENDERHUD.


### float SC_Fnt_GetWidthW(ushort *txt, float scale);

This function will return the width in pixels of the unicode text *txt* with system font of scale *scale.*


### void SC_GetScreenRes(float *width, float* height);

This function will set the *width* and *height* to the actual screen resolution.


### void SC_SetSceneVisibilityMult(float vis_mult, float scene_fog_mult, float bckg_fog_mult);

This function will change the multipliers applied to the scene visibility settings.

*Vis_mult* is multiplier of the maximum visibility, *scene_fog_mult* and *bckg_fog_mult* are used to set the the fog and background fog.


### void SC_FadeTo(BOOL black, float time);

This function will cause the view to fade to black (if *black* is true) or to the full visibility in the time *time.*


### void SC_SwitchSceneSCS(char *fname, float time);

This function will fade the scene visual settings to the settings stored in the file *fname* in the time *time.*


### void SC_SetMovieBorders(BOOL set_on);

This function will cause the black "movie" borders on the top and bottom of the screen to appear or disappear.


### void SC_EnableBloodWhenHit(BOOL enable);

This function will enable or disable spray of the blood when some player is hit. For the most versions is this enabled for the default.


### void SC_CreateLight(s_SC_light *info);

This function will create the in game light according to the settings in the s_SC_light *info* structure.


### void SC_EnableCharacterLOD(BOOL enable);

This function will enable or disable usage of the level of details for the characters. By default the LODs are enabled.


### void SC_GetCameraPos(c_Vector3 *vec);

This function will get the world position of the current camera to the vector *vec.*


## Functions for handling the items

Items are weapons/grenades/ammo and other things in the engine. Engine uses special id to handle this items. For the list of the items see here.


### dword SC_Item_Create(dword id, c_Vector3 *vec);

This function will create the item with *id* on the position *vec* and will return the identifier of the item.


### dword SC_Item_Create2(dword id, c_Vector3 *vec, c_Vector3* movdir);

This function will create the item with *id* on the position *vec* with moving vector *movdir* and will return the identifier of the item.


### void SC_Item_Preload(dword id);

This function will preload the item id (so when the item is created, game won't stop for a while and load it's data).


### BOOL SC_Item_GetPos(dword netid, c_Vector3 *pos);

This function will get the position of the item with identifier *netid* and fill it to the position *pos.* The function returns TRUE if the engine found the specified object.


### dword SC_Item_Find(dword item_type);

This function will look for the item of specified type *item_type* and returns the identifier of the first found item.


### void SC_RemoveItems(s_sphere *area, dword item_type);

This function will remove all items of specified type *item_type­* from the area defined by sphere *area.*


## Function for handling the waypoints

These functions are used to work with the waypoints.


### BOOL SC_GetWp(char *wpname, c_Vector3* vec);

This function will set the position of the waypoint *wpname* to the vector *vec.* If the waypoint is found, it will return TRUE.


### BOOL SC_GetRndWp(s_sphere *sph, c_Vector3* wp);

This function will get the position of the random waypoint inside the sphere *sph* to the vector *vec.* If the waypoint is found, it will return TRUE.


### void SC_ClearImpossibleWayTargets(void);

This function will clear the list of the impossible ways (when using the waypoint blockers).


## Functions for handling the players

These are basic functions for creating and handling the players and groups.


### void SC_InitSide(dword id, s_SC_initside *init);

This function will initialize the side with the id *id* according to the data in the s_SC_initside *init.*


### void SC_SetSideAlly(dword s1, dword s2, float status);

This function will set the status between sides *s1* and *s2*. Status can be:

0 - the sides are neutral

1 - sides are allies

-1 - sides are enemies


### void SC_InitSideGroup(s_SC_initgroup *info);

This function will initialize player group according to the data in the structure s_SC_initgroup *info.*


### dword SC_P_Create(s_SC_P_Create *info);

This function will create the player according to the data in the structure s_SC_P_Create *info* and will return the pointer to the created player.


### void SC_P_ScriptMessage(dword pl_id, dword param1, dword param2);

This function will send the script message to the player *pl_id* with parameter *param1* and *param2*. Target player script will receive callback.


### void SC_P_DoKill(dword pl_id);

This function will kill the player *pl_id*.


### void SC_P_DoAnim(dword pl_id, char *filename);

This function will force the player *pl_id* to play the animation *filename.* When the *filename* is NULL, player will return to the normal animation.


### void SC_P_DoAnimLooped(dword pl_id, char *filename);

This function will force the player *pl_id* to play the animation *filename.* Animation will be looped infinitely until the script will use the function SC_P_DoAnim with the animation name NULL.


### void SC_P_Recover(dword pl_id, c_Vector3 *pos, float rz);

This function will recover (reincarnate :) player *pl_id* on the position *pos* with z rotation *rz.*


### void SC_P_Recover2(dword pl_id, c_Vector3 *pos, float rz, dword phase);

This function will recover (reincarnate :) player *pl_id* on the position *pos* with z rotation *rz* in the phase *phase.* Phase means the stance - 0 is standing player, 1 is crouching player.


### void SC_P_Release(dword pl_id);

This function will release the player *pl_id*. This function can be used ONLY in the level script!


## Functions for getting the info about players

These functions are used to acquire information about the players in the game.


### dword SC_GetGroupPlayers(dword side, dword group);

This function will return number of the players of side *side* in the group *group.*


### void SC_GetPls(s_sphere *sph, dword* list, dword *items);

This function will fill the *list* with the players found in the sphere sph and set the number of the players to *items*. *List* must be array and *items* must be set to the size of the array before calling the function.


### void SC_GetPlsInLine(c_Vector3 *pos, c_Vector3* dir, dword *list, dword* items);

This function will fill the *list* with the players found in line from the *pos* to *dir* and set the number of the players to *items*. *List* must be array and *items* must be set to the size of the array before calling the function.


### char *SC_P_GetName(dword pl_id);

This function will return the pointer to the name of the player *pl_id.*


### BOOL SC_P_GetActive(dword pl_id);

This function will return true if the player *pl_id* is active. Player can be set active/inactive with the function SC_P_SetActive.


### BOOL SC_P_IsReady(dword pl_id);

This function will return TRUE if the player *pl_id* is ready - he is created and alive.


### void SC_P_GetPos(dword pl_id, c_Vector3 *pos);

This function will return the position of the player *pl_id*  in the vector *pos.* Returned position is the place where player's legs touch the ground.


### float SC_P_GetRot(dword pl_id);

This function will return the z rotation of the player *pl_id.*


### void SC_P_GetHeadPos(dword pl_id, c_Vector3 *pos);

This function will return the position of the player *pl_id* 's head in the vector *pos.*


### void SC_P_GetDir(dword pl_id, c_Vector3 *dir);

This function will return direction of the movement of the player *pl_id*  in the vector *dir.*


### void SC_P_GetInfo(dword pl_id, s_SC_P_getinfo *info);

This function will will the information about he player *pl_id* to the structure s_SC_P_getinfo *info*.


### dword SC_GetNearestPlayer(c_Vector3 *vec, float* dist);

This function will return the pointer to the nearest player to the vector *vec,* value *dist* will be used to store the distance from the vector.


### dword SC_P_GetBySideGroupMember(dword iside, dword igroup, dword imember);

This function will return the pointer to the player specified by his side *iside,* group *igroup* and member id *imember.*


### float SC_P_GetPhase(dword pl_id);

This function will return the stance phase of the player *pl_id*. Return values are: 0 stand, 1 crouch, 2 lie.


### float SC_P_GetDistance(dword pl_id, dword to_pl_id);

This function will return the distance from the player *pl_id* to the player ­*to_pl_id.*


### void SC_P_WriteHealthToGlobalVar(dword pl_id, dword first_gvar);

This function will write the health of the player *pl_id* to the global variables starting at the *first_gvar.* Functions uses 2 variables. It's counterpart is SC_P_ReadHealthFromGlobalVar.


### BOOL SC_P_IsInSpecStativ(dword pl_id);

This function will return true if the player *pl_id*  is in the special stativ. See the function SC_P_SetSpecAnims.


### BOOL SC_P_UsesBinocular(dword pl_id);

This function will return true if the player *pl_id*  is using the binoculars.


## Functions for changing the parameters of players

These functions are used to set or change some parameters of the generic players.


### void SC_P_ChangeSideGroupMemId(dword pl_id, dword side, dword group, dword mem_id);

This function will force the change of the unique identifiers of the player *pl_id* to new *side, group* and *mem_id.* Useful when you need someone to become suddenly the enemy - just switch his side.


### void SC_P_SetForceClassName(dword pl_id, dword name_nr);

This function will force the class name of the player* pl_id *to the text identifier* name_nr. *By default the class names in the singleplayer are according to the member id:

SC_P_MEMBERID_CAPTAIN = 0 = "captain"

SC_P_MEMBERID_POINT = 1 = "pointman"

SC_P_MEMBERID_MEDIC = 2 = "medic"

SC_P_MEMBERID_DEMOLITION = 3 = "engineer"

SC_P_MEMBERID_RADIO = 4 = "radioman"

SC_P_MEMBERID_MACHINEGUN = 5 = "machine gunner"


### void SC_P_SetPos(dword pl_id, c_Vector3 *pos);

This function will teleport the player *pl_id* to the position *pos.*


### void SC_P_SetRot(dword pl_id, float rz);

This function will set the rotation around the z axis of the player *pl_id* to the *rz.*


### void SC_P_AddAttObj(dword pl_id, char *bes_name, char* eqp_name);

This function is obsolete, do not use it!


### void SC_P_SetHp(dword pl_id, float hp);

This function will set the hit points of the player *pl_id* to the value *hp.* WARNING - this can be used only for damaging the health and player script of *pl_id* will receive callback about hit.


### void SC_P_Heal(dword pl_id);

This function will heal some of the hit points of the player *pl_id.*


### void SC_P_SetActive(dword pl_id, BOOL active);

This function will set the player *pl_id* active/inactive. Inactive player is not rendered and not in the game for all means until being set active again.


### void SC_P_EnableLonelyWolfKiller(dword pl_id, float distance);

This function is used only for the PC and it means when the specified *pl_id* is farer then *distance* from the nearest ally, all enemies around are shooting much better and are causing greater damage. By default this feature is disabled.


### void SC_P_SetFaceStatus(dword pl_id, dword face_type, float time);

This function will set the face of the player *pl_id* for the time *time* to specified expression type.


### void SC_P_SetHandVariation(dword pl_id, dword hand_id, dword variation, float time);

This function will cause the hand *hand_id* (SC_P_HAND_LEFT or SC_P_HAND_RIGHT) of the player *pl_id* for the time *time* set to one of the variations:

SC_P_HANDVAR_DEFAULT, SC_P_HANDVAR_COUNT1, SC_P_HANDVAR_COUNT2, SC_P_HANDVAR_COUNT3, SC_P_HANDVAR_COUNT4, SC_P_HANDVAR_COUNT5, SC_P_HANDVAR_PALM, SC_P_HANDVAR_FIST, SC_P_HANDVAR_OK, SC_P_HANDVAR_FUCK, SC_P_HANDVAR_ARSCH.


### void SC_P_Link3pvEqp(dword pl_id, dword slot_id, dword plb_id, char *eqp_name);

This function will link special equipment with id *plb_id* with the eqp file named *eqp_name* on the slot *slot_id* of the player *pl_id. Plb_id* must be created with SC_PreloadBes.


### void SC_P_UnLink3pvEqp(dword pl_id, dword slot_id);

This function will unlink the special equipment from the slot *slot_id* of the player *pl_id.*


### void SC_P_SetSpecAnims(dword pl_id, s_SC_P_SpecAnims *info);

This function will set the special animations set in the structure s_SC_P_SpecAnims *info* for the player *pl_id.*


### void SC_P_SetPhase(dword pl_id, dword phase);

This function will set the stance phase of the player *pl_id* to *phase,* which can be either 0 for standing or 1 for crouching.


### void SC_P_DoHit(dword pl_id, dword area_id, float hp);

This function will hit the player *pl_id* to the area *area_id,* SC_P_MESH_AREA_BODYFRONT, SC_P_MESH_AREA_BODYBACK, SC_P_MESH_AREA_LEFTARM, SC_P_MESH_AREA_RIGHTARM, SC_P_MESH_AREA_LEFTLEG, SC_P_MESH_AREA_RIGHTLEG, or SC_P_MESH_AREA_HEAD) for the damage *hp.*


### void SC_P_SetRadarColor(dword pl_id, dword val);

This function will change the color of specified player *pl_id* on the PC's radar to the color value *val.*


### void SC_P_CloseEyes(dword pl_id, BOOL force_close);

This function will cause the player *pl_id* to close or open the eyes.


### void SC_P_EnableBinocular(dword pl_id, BOOL enable);

This function will enable or disable binoculars for the player *pl_id.*


### void SC_P_EnableHeadEqpFlyOff(dword pl_id, BOOL enable);

This function enables or disables posibility to shoot of the head gear from the player *pl_id.*


### void SC_P_EnableHitAnimations(dword pl_id, BOOL enable);

This function enables / disables playing the hit animations for the player *pl_id.*


### void SC_P_ReadHealthFromGlobalVar(dword pl_id, dword first_gvar);

This function will read the health of the player *pl_id* from the global variables starting at the *first_gvar.* Functions uses 2 variables. It's counterpart is SC_P_WriteHealthFromGlobalVar.


### void SC_P_SetLinkedView(dword pl_id, float rz, float rx);

This functions sets the linked view from the player *pl_id* with rotation values *rz* and *rx.*


## Functions for players and weapons

These are the functions for handling the weapons and inventories of the generic players.


### BOOL SC_P_GetWeapons(dword pl_id, s_SC_P_Create *info);

This function will return TRUE if it can write the information about the inventory of the player *pl_id* to the data structurue s_SC_P_Create *info.*


### BOOL SC_P_HasWeapon(dword pl_id, dword weap_type);

This function will return TRUE if the specified *pl_id* has weapon *weap_type.*


### BOOL SC_P_GetHasShoot(dword pl_id);

This function will return TRUE if the *pl_id* has shot from the last use of this function.


### dword SC_P_GetCurWeap(dword pl_id);

This function will return current selected weapon of the player *pl_id.*


### void SC_P_AddAllAmmo(dword pl_id);

This function will add all ammo to the player *pl_id* (including grenades if the player has at least one).


### void SC_P_AddAmmoNoGrenade(dword pl_id);

This function will add all ammo to the player *pl_id* except for the grenades.


### void SC_P_ChangeWeapon(dword pl_id, dword slot_id, dword weap_type);

This function will change the weapon in the slot *slot_id* of the player *pl_id* to the weapon *weap_type.*


### void SC_P_SetSelWeapon(dword pl_id, dword slot_id);

This function will change the selected weapon of the *pl_id* to the slot *slot_id.*


### void SC_P_SetNoAmmo(dword pl_id);

This function will remove all ammo from the player *pl_id.*


### void SC_P_SetAmmo(dword pl_id, dword ammo_type, dword amount);

This function sets the amount of the ammo *ammo_type* to the amount *amount* for the *pl_id.*


### void SC_P_WriteAmmoToGlobalVar(dword pl_id, dword first_gvar, dword last_gvar);

This function will write the amounts of the player's *pl_id* ammo to the global variables starting at the *first_gvar* to *last_gvar.* Minimum is 30 global variables. Counterpart of this function is SC_P_ReadAmmoFromGlobalVar.


### void SC_P_ReadAmmoFromGlobalVar(dword pl_id, dword first_gvar, dword last_gvar);

This function will read the amounts of the player's *pl_id* ammo from the global variables starting at the *first_gvar* to *last_gvar.* Minimum is 30 global variables. Counterpart of this function is SC_P_WriteAmmoFromGlobalVar.


### dword SC_P_GetAmmoInWeap(dword pl_id, dword slot_id);

This function will return the ammo count in the weapon in the slot *slot_id* of the player *pl_id.*


### void SC_P_SetAmmoInWeap(dword pl_id, dword slot_id, dword ammo);

This function will set the ammo count in the weapon in the slot *slot_id* of the player *pl_id* to the value *ammo.*


## Functions for the player - vehicle interaction

These functions are used for the interaction between players and vehicles.


### dword SC_P_IsInCar(dword pl_id);

This function return either NULL if player is not in the car, or the pointer to the car object.


### dword SC_P_IsInCarEx(dword pl_id, dword *entry_index);

This function return either NULL if player is not in the car, or the pointer to the car object. If the player is in the car, the entry_index is filled with the index of the entry point.


### dword SC_P_IsInHeli(dword pl_id);

This function return either NULL if player is not in the helicopter, or the pointer to the helicopter object.


### dword SC_P_IsInShip(dword pl_id);

This function return either NULL if player is not in the ship, or the pointer to the ship object.


### void SC_P_SetToHeli(dword pl_id, char *heli_name, dword entry_index);

This function will teleport the player *pl_id* to the helicopter named *heli_name* on the entry point with the index *entry_index.*


### void SC_P_ExitHeli(dword pl_id, c_Vector3 *new_pos);

This function will teleport the player *pl_id* out of the helicopter to the position in the *new_pos.*


### void SC_P_SetToShip(dword pl_id, char *ship_name, dword entry_index);

This function will teleport the player *pl_id* to the ship named *ship_name* on the entry point with the index *entry_index.*


### void SC_P_ExitShip(dword pl_id, c_Vector3 *new_pos);

This function will teleport the player *pl_id* out of the ship to the position in the *new_pos.*


### void SC_P_SetToCar(dword pl_id, char *car_name, dword entry_index);

This function will teleport the player *pl_id* to the car named *car_name* on the entry point with the index *entry_index.*


### void SC_P_SetToSceneMwp(dword pl_id, char *mwp_name);

This function will teleport the player *pl_id* to the mounted weapon platform named *mwp_name.*


### void SC_P_ExitSceneMwp(dword pl_id);

This function will teleport the player *pl_id* out of the mounted weapon.


## Functions for handling the human PC directly

This set of function are working directly with the human PC on actual machine.


### dword SC_PC_Get(void);

This function will return the pointer to the human PC. It CAN be zero sometimes - means human PC is not yet created or disabled.


### BOOL SC_PC_GetPos(c_Vector3 *pos);

This function will fill the position of the PC to the variable *pos.* It returns TRUE if the data in the *pos* are valid.


### void SC_PC_SetControl(BOOL user_control);

This function will enable or disable PC control. If set to FALSE, no input will be used to handle the player and the camera will be set to default location, unless changed with the view animation. It is enabled by default.


### void SC_PC_EnableMovementAndLooking(BOOL enable);

This function will enable or disable players movement and looking around - useful for fixing the player in one position. It is enabled by default.


### void SC_PC_EnableMovement(BOOL enable);

This function will enable or disable PC movement - he can still look around, but cannot move. It is enabled by default.


### void SC_PC_EnablePronePosition(BOOL enable);

This function is used to disable the prone position for the PC in some regions - underground for example. It is enabled by default.


### void SC_PC_EnableWeaponsUsing(BOOL enable);

This function enables or disables usage of the PC's weapon. It is enabled by default.


### void SC_PC_EnableExit(BOOL enable);

This function will enable or disable possibility of PC's exit from the vehicle. It is enabled by default.


### void SC_PC_EnableEnter(BOOL enable);

This function will enable or disable possibility of PC's enter to the vehicle. It is enabled by default.


### float SC_PC_PlayFpvAnim(char *filename);

This function will force the players hands to play selected FPV animation. Function will return the time to the end of the animation.


### float SC_PC_PlayFpvAnim2(char *filename, dword plb_id, char* eqp, char *anm);

This function will force the players hands to play selected FPV animation using the selected preloaded BES file *plb_id* attached with the equipment file *eqp* playing the animation *anm.* Function will return the time to the end of the animation.


### void SC_PC_PlayFpvLooped(char *filename);

This function will force the players hands to play looped selected FPV animation.


### void SC_PC_EnableFlashLight(BOOL enable);

This function will enable or disable usage of the flashlight for the player.


### void SC_PC_EnableHitByAllies(BOOL enable);

This function will enable or disable friendly fire for the PC. It is disabled by default.


### void SC_PC_EnablePickup(BOOL enable);

This function will enable or disable possibility of picking up objects for the PC. It is enabled by default.


### void SC_PC_SetIntel(s_SC_P_intel *info);

This function will set PC's intel from the data contained in the s_SC_P_intel *info.*


### void SC_PC_GetIntel(s_SC_P_intel *info);

This function will fill PC's intel to the data contained in the s_SC_P_intel *info.*


### float SC_GetPCZoom(void);

This function will return current zoom of the PC.


## Functions for handling the group AI

These functions are used to work with the group AI - for all AI members in the group.


### void SC_Ai_SetPlFollow(dword side, dword group, dword mode, s_SC_Ai_PlFollow *follow, dword* follow_order, dword *point_order, dword players);

This function is used to sed the follow/point mode for the specified side/group. For more info see here.


### void SC_Ai_SetShootOnHeardEnemyColTest(BOOL do_test);

This function is used for all AI characters in the level - if enabled, AI will shoot ONLY if the target is hittable - ie only if he is clearly visible, so no shooting to the tree behind which is the target hided. Use only in the underground or in the interior. By default it is set to FALSE.


### void SC_Ai_SetFormationType(dword side, dword group, dword type);

This function will set the formation type for the group. Now obsolete.


### void SC_Ai_SetFormationSize(dword side, dword group, float size);

This function will set the size of the formation for the group. Now obsolete.


### void SC_Ai_SetBattleMode(dword side, dword group, dword mode);

This function will set all AI players in the side/group to the specified mode. It can be:


```c
#define SC_P_AI_BATTLEMODE_HOLD 0
```

- hold position


```c
#define SC_P_AI_BATTLEMODE_ATTACK 1
```

- attack - try to advance on the enemy


```c
#define SC_P_AI_BATTLEMODE_RETREAT 2
```

- retreat - try to move out of the enemy


```c
#define SC_P_AI_BATTLEMODE_FOLLOW 4
```

- follow the team leader


```c
#define SC_P_AI_BATTLEMODE_ATTACKAGR 5
```

- aggresive attack

This mode is valid only in the battle - means AI knows about at least one enemy.


### void SC_Ai_SetBattleModeExt(dword size, dword group, dword battlemode, c_Vector3 *param);

This is the extended version of the SC_Ai+SetBattleMode function used for special battle move. It will set the specified side/group to the *battlemode*, usually used only for the SC_P_AI_BATTLEMODE_GOTO with the *param* holding the specified place.


```c
#define SC_P_AI_BATTLEMODE_HOLD 0
```

- hold position


```c
#define SC_P_AI_BATTLEMODE_ATTACK 1
```

- attack - try to advance on the enemy


```c
#define SC_P_AI_BATTLEMODE_RETREAT 2
```

- retreat - try to move out of the enemy


```c
#define SC_P_AI_BATTLEMODE_GOTO 3
```

- move under fire to the specified place


```c
#define SC_P_AI_BATTLEMODE_FOLLOW 4
```

- follow the team leader


```c
#define SC_P_AI_BATTLEMODE_ATTACKAGR 5
```

- aggresive attack

This mode is valid only in the battle - means AI knows about at least one enemy.


### void SC_Ai_SetPeaceMode(dword side, dword group, dword mode);

This function will set the specified peace mode for the specified side/group. Mode can be:


```c
#define SC_P_AI_PEACEMODE_HOLD 0
```

- hold position


```c
#define SC_P_AI_PEACEMODE_FOLLOW 1
```

- follow the team leader


```c
#define SC_P_AI_PEACEMODE_POINT 2
```

- pointman mode


```c
#define SC_P_AI_PEACEMODE_SEARCHDEATHBODIES 3
```

- searching the dead bodies.

This mode is valid only in the peace mode- means AI knows about no enemy.


### void SC_Ai_SetPointRuns(dword side, dword group, BOOL runs);

This function will enable runing for the pointman of the specified side/group. If TRUE, the pointman will run forward instead using slow walk. By default FALSE.


### void SC_Ai_ClearCheckPoints(dword side, dword group);

This function will clear the check points for the pointman of the specified side/group.


### void SC_Ai_AddCheckPoint(dword side, dword group, c_Vector3 *vec, dword flags);

This function will add the specified place *vec* to the list of the pointman's checkpoints for the specified side group. Possible flags are:


```c
#define SC_AI_CP_FL_NOSKIP 1
```

- do not skip the point, allways must visit it.


### BOOL SC_Ai_GetCurCheckPoint(dword side, dword group, c_Vector3 *vec);

This function will fill the *vec* with the current check point for the *side/group.* It will return FALSE, if there are no specified checkpoints left.


### void SC_Ai_PointStopDanger(dword side, dword group);

This function will make the pointman of the specified side/group to stop and look for the danger - just eye candy, nothing more.


### void SC_Ai_StopDanger(dword side, dword group, float stop_time);

This function will make whole group to stop and look for the danger for the time *stop_time.* Just eye candy, nothing more.


### void SC_Ai_SetStealthMode(dword side, dword group, BOOL stealth);

This function will set the stealth mode (shooting disabled until under fire) for the specified side/group to the TRUE or FALSE.


### void SC_Ai_SetStealthModeOff(dword side, dword group, float agressive_time);

This function will set the stealth mode OFF for the specified side/group for the time *agressive_time.*


### BOOL SC_Ai_GetStealthMode(dword side, dword group);

This function will return TRUE if the specified side/group is in the steath mode.


### void SC_Ai_EnableRelaxWalk(dword side, dword group, BOOL enable);

This function will enable or disable relaxed walk animation for the side/group in the peace mode. By default it is enabled.


### dword SC_Ai_Blocker_Add(s_sphere *sph);

This function will create the waypoint blocker specified in the sphere sph and returns pointer to the blocker object. You must remove the blocker each scene release and create it after load again!


### void SC_Ai_Blocker_Remove(dword blocker_id);

This function will remove the waypoint blocker created with the SC_Ai_Blocker_Add. Pointer MUST BE VALID!


### void SC_Ai_FakeEnemy_Add(dword side, dword group, c_Vector3 *fake_enemy, dword area_spheres, s_sphere* area_sphere);

This function will add the fake enemy (AI will move as under fire) for the specified side/group on the position *fake_enemy* (AI will think that there is an enemy on that place), fake enemy is valid if the AI is in one of the speheres specified in the sphere array *area_sphere* (size of the area is specified in the *area_spheres).* You can use zeros for the *fake_enemy, area_spheres* and *area_sphere -* in this case the AI will always move as under fire.


### void SC_Ai_FakeEnemy_Remove(dword side, dword group, c_Vector3 *fake_enemy);

This function will remove the fake enemy from the specified position (can be zero) for the side/group.


### void SC_Ai_FakeDanger(s_sphere *sph, float time);

This function will mark the specified place as the place of the danger for the *time.* AI will try to run away from this spot.


### void SC_Ai_SetGroupEnemyUpdate(dword side, dword group, BOOL enable);

This function will enable or disable informing of the other AI players in the same group about detected enemy. By default it's enabled.


### void SC_Ai_SetPointmanNormalWalking(dword side, dword group, BOOL normal);

This function will set the pointman peace mode walk of the pointman of the side/group to the normal standard animation.


## Functions for handling the individual AI

Warning - be sure to use the functions begining with the SC_P_Ai_ ONLY for the AI characters! Using these functions for the human PC will cause game to crash!


### void SC_P_Ai_GetEnemyShotAround(dword pl_id, float max_dist);

This function will enable using the shot around callback for the specified player - the AI script will receive callback any time some enemy shots near by (distance specified with the *max_dist)*.


### void SC_P_SetInvisibleForAi(dword pl_id, BOOL invisible);

This function will set the specified player invisible for all AI characters.


### BOOL SC_P_GetInvisibleForAi(dword pl_id);

This function will return if the specified *pl_id* is set as invisible for the AI.


### void SC_P_EnableSearchDeathBodies(dword pl_id, BOOL enable);

This function will enable searching the death bodies for the specified player.


### BOOL SC_P_Ai_CanSeePlayer(dword pl_id, dword target_id, float max_dist, dword need_points);

This function will return if the specified AI *pl_id* can see target player *target_id* up to the maximum distance *max_dist.* Value *need­_points* means how many points of the target player must be seen (ie only 1 - just head or one leg etc...).


### void SC_P_Ai_SetMode(dword pl_id, dword mode);

This function will set the target AI to:


```c
#define SC_P_AI_MODE_SCRIPT 0
```

- AI is controlled by the script


```c
#define SC_P_AI_MODE_BATTLE 1
```

- AI is controlled by the battle AI


### dword SC_P_Ai_GetMode(dword pl_id);

This function will return the mode of the target:


```c
#define SC_P_AI_MODE_SCRIPT 0
```

- AI is controlled by the script


```c
#define SC_P_AI_MODE_BATTLE 1
```

- AI is controlled by the battle AI


### void SC_P_Ai_SetBattleMode(dword pl_id, dword battlemode);

This function will set the battle mode of the AI to:


```c
#define SC_P_AI_BATTLEMODE_HOLD 0
```

- hold position


```c
#define SC_P_AI_BATTLEMODE_ATTACK 1
```

- attack - try to advance on the enemy


```c
#define SC_P_AI_BATTLEMODE_RETREAT 2
```

- retreat - try to move out of the enemy


```c
#define SC_P_AI_BATTLEMODE_FOLLOW 4
```

- follow the team leader


```c
#define SC_P_AI_BATTLEMODE_ATTACKAGR 5
```

- aggresive attack


### void SC_P_Ai_SetBattleModeExt(dword pl_id, dword battlemode, c_Vector3 *param);

This function is the extended version of the SC_P_Ai_SetBattleMode used for the battle move to the specified place:


```c
#define SC_P_AI_BATTLEMODE_HOLD 0
```

- hold position


```c
#define SC_P_AI_BATTLEMODE_ATTACK 1
```

- attack - try to advance on the enemy


```c
#define SC_P_AI_BATTLEMODE_RETREAT 2
```

- retreat - try to move out of the enemy


```c
#define SC_P_AI_BATTLEMODE_GOTO 3
```

- move under fire to the specified place


```c
#define SC_P_AI_BATTLEMODE_FOLLOW 4
```

- follow the team leader


```c
#define SC_P_AI_BATTLEMODE_ATTACKAGR 5
```

- aggresive attack


### dword SC_P_Ai_GetBattleMode(dword pl_id);

This function will return the battle mode of the specified AI:


```c
#define SC_P_AI_BATTLEMODE_HOLD 0
```

- hold position


```c
#define SC_P_AI_BATTLEMODE_ATTACK 1
```

- attack - try to advance on the enemy


```c
#define SC_P_AI_BATTLEMODE_RETREAT 2
```

- retreat - try to move out of the enemy


```c
#define SC_P_AI_BATTLEMODE_GOTO 3
```

- move under fire to the specified place


```c
#define SC_P_AI_BATTLEMODE_FOLLOW 4
```

- follow the team leader


```c
#define SC_P_AI_BATTLEMODE_ATTACKAGR 5
```

- aggresive attack


### void SC_P_Ai_SetPeaceMode(dword pl_id, dword peacemode);

This function will set the specified peace mode for the specified side/group. Mode can be:


```c
#define SC_P_AI_PEACEMODE_HOLD 0
```

- hold position


```c
#define SC_P_AI_PEACEMODE_FOLLOW 1
```

- follow the team leader


```c
#define SC_P_AI_PEACEMODE_POINT 2
```

- pointman mode


```c
#define SC_P_AI_PEACEMODE_SEARCHDEATHBODIES 3
```

- searching the dead bodies.

This mode is valid only in the peace mode- means AI knows about no enemy.


### dword SC_P_Ai_GetPeaceMode(dword pl_id);

This function returns the peace mode for the specified player *pl_id*. Mode can be:


```c
#define SC_P_AI_PEACEMODE_HOLD 0
```

- hold position


```c
#define SC_P_AI_PEACEMODE_FOLLOW 1
```

- follow the team leader


```c
#define SC_P_AI_PEACEMODE_POINT 2
```

- pointman mode


```c
#define SC_P_AI_PEACEMODE_SEARCHDEATHBODIES 3
```

- searching the dead bodies.


### dword SC_P_Ai_GetSpecTask(dword pl_id);

This function will return the special task mode (if any) of the *pl_id.*


### void SC_P_Ai_SetMoveMode(dword pl_id, dword mode);

This function will set the move mode of the *pl_id* to the specified mode. This is always valid only for the AI in the script mode! AI in the battle mode will soon change the move mode according it's own tastes. Possible modes are:


```c
#define SC_P_AI_MOVEMODE_WALK 0
```

- normal walk


```c
#define SC_P_AI_MOVEMODE_AIM 1
```

- walk and aim - slower


```c
#define SC_P_AI_MOVEMODE_RUN 2
```

- run


### void SC_P_Ai_SetMovePos(dword pl_id, dword pos);

This function will set the move position of the *pl_id* to the specified mode. This is always valid only for the AI in the script mode! AI in the battle mode will soon change the move position according it's own tastes. Possible positions are:


```c
#define SC_P_AI_MOVEPOS_STAND 0
```

- stand


```c
#define SC_P_AI_MOVEPOS_CROUCH 1
```

- crouch


```c
#define SC_P_AI_MOVEPOS_LIE 2
```

- lie


### void SC_P_Ai_EnableShooting(dword pl_id, BOOL enable);

This function will enable or disable the shooting for the specified AI. Enabled by default.


### void SC_P_Ai_Go(dword pl_id, c_Vector3 *vec);

This function will send the AI to the specified place *vec.* AI in the battle mode will move there, but it is possible it will change it's target in the battle! There is also a possibility the AI will block somewhere and it won't go - for the script mode you should check periodically if the AI is moving.


### void SC_P_Ai_Stop(dword pl_id);

This function will stop moving of the specified AI.


### void SC_P_Ai_GetProps(dword pl_id, s_SC_P_AI_props *props);

This function will get the properties of the AI and fill it in the s_SC_P_AI_props structure.


### void SC_P_Ai_SetProps(dword pl_id, s_SC_P_AI_props *props);

This function will set the properties of the AI according the data in the s_SC_P_AI_props structure.


### void SC_P_Ai_GetGrenateProps(dword pl_id, s_SC_P_Ai_Grenade *props);

This function will get the grenade usage properties of the AI and fill it in the s_SC_P_AI_Grenade structure.


### void SC_P_Ai_SetGrenateProps(dword pl_id, s_SC_P_Ai_Grenade *props);

This function will set the grenade usage properties of the AI according the data in the s_SC_P_AI_Grenade structure.


### dword SC_P_Ai_GetEnemies(dword pl_id);

This function will return the number of all enemies the AI knows about including the ones the AI is not sure about (just heard something).


### dword SC_P_Ai_GetSureEnemies(dword pl_id);

This function will return the number of all enemies the AI knows about and is sure these are the enemies (it sees them or saw them few moments ago).


### void SC_P_Ai_LookAt(dword pl_id, c_Vector3 *vec);

This function will order the AI to look at the specified vector. For AI in the battle mode it means it will take a look, but will probably face another direction soon.


### void SC_P_Ai_EnableSituationUpdate(dword pl_id, BOOL enable);

This function can be used to make the AI blind and deaf - if you will disable the situation update, the AI will not look around for the enemies.


### BOOL SC_P_Ai_KnowsAboutPl(dword pl_id, dword target_pl_id);

This function will return TRUE if the *pl_id* knows about *target_pl_id.*


### void SC_P_Ai_SetBattleProps(dword pl_id, s_SC_P_Ai_BattleProps *props);

This function is used to set the battle properties for the AI - see the data structure s_SC_P_Ai_BattleProps.


### BOOL SC_P_Ai_GetShooting(dword pl_id, dword *target_pl_id);

This function returns true if the pl_id is shooting. target_pl_id is used to store the id of the current target.


### float SC_P_Ai_GetDanger(dword pl_id);

This function returns the danger value of the *pl_id -* danger value means how many bullets are flying around - zero means no shots in the vicinity, 1 is some shot was nearby - the value is slowly degrading to the zero and is updated every time some shot passes the AI. If the AI is hit, the danger value is very high of course.

Can be used to determine if the AI is under fire.


### void SC_P_Ai_SetPreferedWeaponSlot(dword pl_id, dword slot);

This function will set the prefered weapon slot for the *pl_id.* Set to 1 for the pistol, 2 for the main gun.


### dword SC_P_Ai_GetPreferedWeaponSlot(dword pl_id);

This function will return the prefered weapon slot of the *pl_id.* 1 is the pistol, 2 is the main gun etc.


### void SC_P_Ai_ShootAt(dword pl_id, c_Vector3 *pos, float time);

This function will order the AI to shoot at the specified position *pos* for the time *time.* AI must have shooting enabled. If the AI is in the fight, it will probably shoot somewhere else.


### void SC_P_Ai_ForgetEnemies(dword pl_id);

This function will force the AI to forget about all enemies around - but it can detect them again seconds later!


### void SC_P_Ai_HideYourself(dword pl_id, c_Vector3 *danger_pos, float max_walk_dist);

This function will order the AI to try to hide from the danger at the *danger_pos* up to the maximum distance *max_walk_dist.*


### BOOL SC_P_Ai_LookingAt(dword pl_id, c_Vector3 *pos);

This function will return TRUE if the AI is facing the vector *pos.*


### void SC_P_Ai_ShouldLookAt(dword pl_id, c_Vector3 *pos, float time);

This function sets the AI to look at the specified place. AI will try to watch this place.


### void SC_P_Ai_SetStaticMode(dword pl_id, BOOL is_static);

This function can be used to set the AI to the static mode - it won't move, only change the position and shoot.


### BOOL SC_P_Ai_GetStaticMode(dword pl_id);

This function returns TRUE if the *pl_id* is in the static mode.


### BOOL SC_P_Ai_ThrowGrenade(dword pl_id, c_Vector3 *target, float explode_time);

This function will order the *pl_id* to throw the grenade to the *target.* Grenade will detonate in *explode_time* after the impact. Function will return TRUE if the AI threw the grenade, it can be impossible to throw the grenade at the specified place! AI must have grenades in its inventory.


### float SC_P_Ai_GetNearestEnemyDist(dword pl_id);

This function will return the distance to the nearest enemy of the *pl_id.*


### dword SC_P_Ai_GetNearestEnemy(dword pl_id);

This function will return the pointer to the nearest enemy of the *pl_id.*


### void SC_P_Ai_Script_WatchPlayer(dword pl_id, dword target_pl_id, float time);

This function will force the AI in the script mode to watch the target_pl_id for the specified time. Use the target_pl_id=0 and time=0 to turn this feature off.


### void SC_P_Ai_UpdateSituation(dword pl_id, dword target_pl_id, BOOL enable_se);

This function will update the information about the *target_pl_id* for the *pl_id* if enable_se == TRUE. Useful to inform the AI about the PC.


### void SC_P_Ai_JumpInNextFrame(dword pl_id);

This function will cause the AI to jump during the next time tick.


### void SC_P_Ai_SetIgnoreFlags(dword pl_id, dword flags);

This function is used to set the ignore flags for the *pl_id.* AI will ignore the targets according to the flags, it can be:


```c
#define SC_PL_AI_SIT_IFL_CAR 0x01 // ignore all players in cars
#define SC_PL_AI_SIT_IFL_HELI 0x02 // ignore all players in heli
#define SC_PL_AI_SIT_IFL_SHIP 0x04 // ignore all players in ship
#define SC_PL_AI_SIT_IFL_MWP 0x08 // ignore all players in using mwp
#define SC_PL_AI_SIT_IFL_S0G0 0x10 // ignore all players side 0, group 0
#define SC_PL_AI_SIT_IFL_S0G1 0x20
```

// ignore all players side 0, group 1


```c
#define SC_PL_AI_SIT_IFL_S0G2 0x40
```

// ignore all players side 0, group 2


```c
#define SC_PL_AI_SIT_IFL_S0G3 0x80
```

// ignore all players side 0, group 3


```c
#define SC_PL_AI_SIT_IFL_S1G0 0x0100
```

// ignore all players side 0, group 0


```c
#define SC_PL_AI_SIT_IFL_S1G1 0x0200
```

// ignore all players side 1, group 1


```c
#define SC_PL_AI_SIT_IFL_S1G2 0x0400
```

// ignore all players side 1, group 2


```c
#define SC_PL_AI_SIT_IFL_S1G3 0x0800
```

// ignore all players side 1, group 3


```c
#define SC_PL_AI_SIT_IFL_S2G0 0x1000
```

// ignore all players side 2, group 0


```c
#define SC_PL_AI_SIT_IFL_S2G1 0x2000
```

// ignore all players side 2, group 1


```c
#define SC_PL_AI_SIT_IFL_S2G2 0x4000
```

// ignore all players side 2, group 2


```c
#define SC_PL_AI_SIT_IFL_S2G3 0x8000
```

// ignore all players side 2, group 3


### dword SC_P_Ai_GetIgnoreFlags(dword pl_id);

This function will return the ignore flags of the *pl_id.* See the SC_P_Ai_SetIgnoreFlags.


### void SC_P_Ai_SetPointmanBreaks(dword pl_id, float min_interval, float max_interval);

This function will set the pointman breaks (how often will the leading pointman stop and look around) for the pointman *pl_id.* By default it is disabled.


### void SC_P_Ai_WalkThruAIs(dword pl_id, BOOL enable);

This function will enable/disable moving through the AI characters (ie no collisions) for the *pl_id.*


### void SC_P_Ai_SetMedicIngMaxActiveDist(dword pl_id, float distance);

This function will set the maximum distance of medic and engineer to move and carry their special task.


## Functions for handling the individual AI and vehicles


### void SC_P_Ai_EnterCar(dword pl_id, char *car_name, dword entry_function, s_sphere* enter_pos);

This function will cause the AI to run to the enter_pos and try to enter the car *car_name* using the entry function *entry_function.*


### void SC_P_Ai_StepOutCar(dword pl_id);

This function will make the AI step out of the car.


### void SC_P_Ai_EnterHeli(dword pl_id, char *heli_name, dword entry_function);

This function will make the AI to try to enter the helicopter *heli_name* using the specified entry type *entry_function.*


### void SC_P_Ai_StepOutHeli(dword pl_id);

This function will make the AI step out of the helicopter.


### void SC_P_Ai_Drive(dword pl_id, char *way_filename);

This function will tell the AI sitting in the car at the driver's position to drive according the path saved in the *way_filename.*


## Functions for the multiplayer game

These functions are used for the multiplayer game.


### void SC_MP_AddPlayerScript(char *filename);* This is obsolete no longer used function!*


### BOOL SC_MP_EnumPlayers(s_SC_MP_EnumPlayers *list, dword* items, dword side);

This function is used to enumerate the MP players. It returns TRUE if it was succesfull and the data are valid.

*list* is the array of the s_SC_MP_EnumPlayers, which will be filled with the data.

*items* is the pointer to the variable, which will be filled with number of enumerated players. Before calling this function, set it to the size of the array!

*side* is the identifier of the side, which should be enumerated. Use SC_MP_ENUMPLAYER_SIDE_ALL for all sides.


### BOOL SC_NET_FillRecover(s_SC_MP_Recover *recov, char* wpname);

This function will fill the variable s_SC_MP_Recover with data acquired from the waypoint named *wpname.*


### void SC_MP_RestartMission(void);

This function will cause the restart of the multiplayer game.


### void SC_MP_P_SetRecoverTime(dword pl_id, float time);

This function will set the recover time for the specified player with pointer *pl_id* to the *time.*


### dword SC_MP_P_GetAfterRecoverSide(dword pl_id);

This function will return what side will be the player *pl_id* after the next recover.


### dword SC_MP_P_GetClass(dword pl_id);

This function returns the actual class of the *pl_id.*


### dword SC_MP_P_GetAfterRecoverClass(dword pl_id);

This function returns the class of the *pl_id *after next recover*.*


### void SC_MP_SRV_SetForceSide(dword side);

Use to force all human players to be of specified side, or use 0xffffffff for any side.


### void SC_MP_SRV_SetClassLimit(dword class_id, dword limit);

This function will set the class limit of the class *class_id* to the *limit.*


### void SC_MP_SRV_SetClassLimitsForDM(void);

This function sets the class limits for the DeathMatch like game.


### dword SC_MP_SRV_GetBestDMrecov(s_SC_MP_Recover *list, dword items, float* no_recov_time, float max_recov_time);

This function will return the position in the array of recover places *list* with size *items,* with *no_recov_time* and *max_recov_time* which is usable for the recover of the player.


### void SC_MP_SRV_InitWeaponsRecovery(float time);

This function is used to set the recover time of the weapons placed manualy to the scene. Use 0 for immediate recover or any minus value to disable these weapons.


### void SC_MP_HUD_SetTabInfo(s_SC_MP_hud *info);

This function is used to set the MP info table to the data specified in the s_SC_MP_hud structure.


### void SC_MP_HUD_SelectPl(dword pl_id, dword color);

This function will cause the selected player *pl_id* to be visible on the HUD with ARGB color specified in the *color.*


### void SC_GameInfo(dword text_id, char *text);

This function should not be used - use SC_GameInfoW instead.


### void SC_GameInfoW(ushort *text);

This function will set the game info text shown on the screen to the *text.* Text is in the wide, unicode format.


### void SC_P_MP_AddPoints(dword pl_id, int val);

This function will add points *val* to the player *pl_id.*


### dword SC_MP_GetMaxPointsPl(int *points);

This function will return the pl_id of the player with most points, the points value will be filled to the *points* variable.


### dword SC_MP_GetMaxFragsPl(int *frags);

This function will return the pl_id of the player with most frags, the points value will be filled to the *frags* variable.


### dword SC_MP_GetHandleofPl(dword pl_id);

This function will return the multiplayer handle of the player *pl_id.*


### dword SC_MP_GetPlofHandle(dword pl_handle);

This function will return the pointer to the player with multiplayer handle *pl_handle.*


### void SC_MP_SRV_P_SetObtainedDamageMult(dword pl_id, float mult);

This function will set the damage multiplier to the player *pl_id,* to *mult.* 1 is normal, 2 is player takes twice as much damage, 0.5 takes only half of the damage.


### void SC_MP_SetSideStats(dword side, int frags, int points);

This function will set the status of the side *side* to *frags* and *points.*


### void SC_MP_ScriptMessage(dword param1, dword param2);

This function will send the script message to the multiplayer script running on the same machine as script using this function.


### void SC_MP_AllowStPwD(BOOL enable);

This function can be used to enable or disable switching between players after the death.


### void SC_MP_AllowFriendlyFireOFF(BOOL enable);

This function allows use of the friendly fire. Set TRUE for team based games, FALSE for death match like games*.*


### void SC_MP_SetIconHUD(s_SC_HUD_MP_icon *icon, dword icons);

This function will set the icons to be visible on the heads up display. icon is the pointer to the array of s_SC_HUD_MP_icon, *icons* is the size of the array.


### void SC_MP_SetInstantRecovery(BOOL enable);

This function can be used to allow instant recovery of the players.


### void SC_MP_SetItemsNoDisappear(BOOL nodisappear);

This function can be used to disable disappearing of the items (dropped guns)*.*


### void SC_MP_EnableBotsFromScene(BOOL enable);

This function will enable or disable creation of the AI characters from the player objects in the scene. FALSE by default*.*


### void SC_MP_SetChooseValidSides(dword mask);

This function will set the valid sides for the player to choose from. Use 0 for US only, 2 for VC, 3 for both.


### void SC_MP_EnableC4weapon(BOOL enable);

This function will enable the C4 weapon for the players. (For the ATG bomb games).


### void SC_MP_LoadNextMap(void);

This function will cause the engine to stop the current mission and load next from the server list.


### void SC_MP_SetTeamGame(BOOL teamgame);

This function is used to set the team game (use FALSE for deathmatch like games).


### void SC_MP_RecoverAllNoAiPlayers(void);

Valid only on the server, this function will cause forced recover of all human players in the game*.*


### void SC_MP_RecoverAllAiPlayers(void);

Valid only on the server, this function will cause forced recover of all AI players in the game*.*


### void SC_MP_EndRule_SetTimeLeft(float val, BOOL counting);

This function will set the information about the time left to the end of the game.


### void SC_MP_GetSRVsettings(s_SC_MP_SRV_settings *info);

This function will get the server settings and place them to the s_SC_MP_SRV_settings structure.


### BOOL SC_MP_SRV_P_SetSideClass(dword pl_id, dword side, dword class_id);

This function will set the class of the player *pl_id* to class *class_id* and will set him to the side *side*, valid only on the server.


### BOOL SC_MP_SRV_GetAutoTeamBalance(void);

This function will return TRUE, if the auto team balance is enabled on the server.


### int SC_MP_SRV_GetTeamsNrDifference(BOOL after_respawn);

This function will return the difference between the teams. If *after_respawn* is TRUE, the value will be valid after next respawn of the players.


### void SC_MP_SRV_DoExplosion(c_Vector3 *pos, dword type);

Valid only on the server, this function will create the explosion of *type* (0,1,2) on the position *pos*.


### void SC_MP_SRV_ClearPlsStats(void);

This function will clear the player statistics, valid only on the server.


### void SC_MP_SRV_InitGameAfterInactive(void);

This function will initialize game after being inactive (in the state "Waiting for more players", valid only on the server.


### BOOL SC_MP_GetAmmoBoxesEnabled(void);

This function will return TRUE, if the server has enabled ammo boxes.


### void SC_MP_SRV_GetAtgSettings(s_SC_MP_SRV_AtgSettings *info);

This function will get the ATG server settings and place them to the s_SC_MP_SRV_ATGsettings structure.


### void SC_MP_SetSpectatorCameras(char character);

This function will set the spectator camera to file character.


### void SC_MP_GetRecovers(dword type, s_SC_MP_Recover *list, dword* items);

This function will fill the array of s_SC_MP_Recover list with recovers of given type. Use *items* to specify the size of the array, function will return the number of the recover places.

Type can be:

#define SC_MP_RESPAWN_ALL 0 - all respawn points

#define SC_MP_RESPAWN_DM 1 - deathmatch

#define SC_MP_RESPAWN_WA 3

#define SC_MP_RESPAWN_WB 4

#define SC_MP_RESPAWN_WC 5

#define SC_MP_RESPAWN_WD 6

#define SC_MP_RESPAWN_WE 7

#define SC_MP_RESPAWN_WF 8

#define SC_MP_RESPAWN_CTF_US 9 - CTF for US

#define SC_MP_RESPAWN_COOP 10 -for cooperative mode

#define SC_MP_RESPAWN_ATG_US 11 -ATF for US

#define SC_MP_RESPAWN_ATG_PILOT 12 - ATG for pilot

#define SC_MP_RESPAWN_RW_US 13 - RW for US

#define SC_MP_RESPAWN_CTF_VC 14 - CTF for VC

#define SC_MP_RESPAWN_ATG_VC 15 - ATG for VC

#define SC_MP_RESPAWN_RW_VC 16 - RW for VC

#define SC_MP_RESPAWN_TT_DEF_0 17 - for TT defenders

#define SC_MP_RESPAWN_TT_DEF_1 18

#define SC_MP_RESPAWN_TT_DEF_2 19

#define SC_MP_RESPAWN_TT_DEF_3 20

#define SC_MP_RESPAWN_TT_DEF_4 21

#define SC_MP_RESPAWN_TT_ATT_1 22 - for TT attackers

#define SC_MP_RESPAWN_TT_ATT_2 23

#define SC_MP_RESPAWN_TT_ATT_3 24

#define SC_MP_RESPAWN_TT_ATT_4 25

#define SC_MP_RESPAWN_TT_ATT_5 26


### void SC_MP_RecoverPlayer(dword pl_id);

This function will instantly recover the player *pl_id.*


### void SC_MP_RecoverAiPlayer (dword pl_id, c_Vector3 *pos, float rz);

This function will recover AI player pl_id on the place pos with rotation rz. Note, this function is supported in the engine version 1.60 or higher!


### dword SC_MP_FpvMapSign_Load(char *fname);

This function will load the FPV map sign fname and return it's index.


### BOOL SC_MP_FpvMapSign_Unload(dword id);

This function will unload the FPV map sign with *id.*


### void SC_MP_FpvMapSign_Set(dword signs, s_SC_FpvMapSign *list);

This function will set the FPV map signs. Use *signs* to specify size of the array with signs stored in the s_SC_FpvMapSign structure *list*.


## Functions for handling the speech

These functions are used to handle the player speech.


### void SC_P_Speach(dword pl_id, dword speach_txt, dword snd_id, float *timeout);

This function will make the pl_id to say the text with id *speach_txt* and sound file with numeric id *snd_id.* timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end.

Obsolete function!


### void SC_P_SpeachMes(dword pl_id, dword speach_txt, dword snd_id, float *timeout, dword param);

This function will make the pl_id to say the text with id *speach_txt* and sound file with numeric id *snd_id.* timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end. After the playing of the speech the level script will receive the speech done message.

Obsolete function!


### void SC_P_SpeachRadio(dword pl_id, dword speach_txt, dword snd_id, float *timeout);

This function will make the radio on the pl_id to say the text with id *speach_txt* and sound file with numeric id *snd_id.* timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end.

Obsolete function!


### void SC_P_SetSpeachDist(dword pl_id, float max_dist_subtitle_write);

This function sets the maximum distance from the player pl_id to the camera position the subtitles will be shown on the screen.


### void SC_P_Speech2(dword pl_id, dword speech_txt, float *timeout);

This function will make the pl_id to say the speech with the id speech_txt.timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end. If the speech has only text data, engine will use apropriate time according to the length of the text.


### void SC_P_SpeechMes2(dword pl_id, dword speech_txt, float *timeout, dword param);

This function will make the pl_id to say the speech with the id speech_txt.timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end. If the speech has only text data, engine will use apropriate time according to the length of the text. After the playing of the speech the level script will receive the speech done message.


### void SC_P_SpeechMes3(dword pl_id, char *speech_str, float* timeout, dword param);

This function will make the pl_id to say (text only!) the *speech_str*.timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end. Engine will use apropriate time according to the length of the text. After the playing of the speech the level script will receive the speech done message.


### void SC_P_SpeechMes3W(dword pl_id, ushort *speech_str, float* timeout, dword param);

This function will make the pl_id to say (text only!) the *speech_str*.timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end. Engine will use apropriate time according to the length of the text. After the playing of the speech the level script will receive the speech done message.

This is the unicode version.


### void SC_P_SetChat(dword pl_id, float time);

This function will set the chat counter of the pl_id to *time* seconds. Chat counter is decreasing in the real time until it reaches the zero. This is obsolete function, but may be used for something.


### BOOL SC_P_CanChat(dword pl_id);

This function will return TRUE if the chat counter of the pl_id is zero. Obsolete.


### void SC_RadioSetDist(float max_dist_subtitle_write);

This function will set the maximum distance from the radio to the camera the subtitles will be shown.


### void SC_SpeachRadio(dword speach_txt, dword snd_id, float *timeout);

This function will make the radio to say the text with id *speach_txt* and sound file with numeric id *snd_id.* timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end.

Obsolete function!


### void SC_SpeachRadioMes(dword speach_txt, dword snd_id, float *timeout, dword param);

This function will make the radio to say the text with id *speach_txt* and sound file with numeric id *snd_id.* timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end. The level script will receive the speech done callback with the specified parameter.

Obsolete function!


### void SC_SpeechRadio2(dword speech_txt, float *timeout);

This function will make the radio to say the speech with the id speech_txt.timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end. If the speech has only text data, engine will use apropriate time according to the length of the text.


### void SC_SpeechRadioMes2(dword speech_txt, float *timeout, dword param);

This function will make the radio to say the speech with the id speech_txt.timeout should contain the time from now to the start of the speech and will be updated with the time when the speech will end. If the speech has only text data, engine will use apropriate time according to the length of the text. After the playing of the speech the level script will receive the speech done message.


### void SC_SpeechSet3Dto3Dincamera(BOOL incamera3D);

If incamera3D==TRUE, all speech will be 3D, but placed inside the camera.


### float SC_RadioGetWillTalk(void);

This function will return how long the radio will talk. If zero, there is currently no radio speech active.


### float SC_P_GetWillTalk(dword pl_id);

This function will return how long the *pl_id* will talk. If zero, there is currently no speech active for the *pl_id*.


### BOOL SC_P_GetTalking(dword pl_id);

This function returns TRUE if the pl_id is talking right now.


### void SC_P_RemoveAllSpeech(dword pl_id);

This function will remove all stacked speech for the selected pl_id (currently played speech will be finished normaly). If pl_id is zero, all speech will be removed, if 1, radio speech will be removed.


### void SC_P_RemoveAllSpeechEx(dword pl_id, BOOL include_active);

This function will remove all stacked speech for the selected pl_id (currently played speech will be finished normaly unles the *include_active==TRUE*). If pl_id is zero, all speech will be removed, if 1, radio speech will be removed.


### void SC_P_DisableSpeaking(dword pl_id, BOOL disable);

This function will disable/enable all speech for the pl_id, including system cries.


### void SC_P_Ai_EnableSayTo(dword pl_id, BOOL enable);

This function enables/disables sayto speech feature for the pl_id. For more info see here.


## Functions for controlling the game outcome


### void SC_MissionCompleted(void);

Mission will be completed - engine will show the sign MISSION COMPLETED and after few seconds releases the scene (and in the campaign mode loads next).


### void SC_MissionFailed(void);

Mission will be failed - MISSION FAILED will be shown, the screen will slowly fade out.


### void SC_MissionFailedEx(dword music_id, dword start_volume);

Mission will be failed - MISSION FAILED will be shown, the screen will slowly fade out. The music number *music­_id* will be played instead of the standard one.


### void SC_MissionFailedDeathPlayer(dword death_plid);

Mission will be failed and the camera will switch the 3PV view on the *death_plid* player.


### void SC_MissionDone(void);

Mission will be finished, but without showing the MISSION COMPLETED.


### void SC_TheEnd(void);

This function is same as the SC_MissionCompleted, but it will show "THE END" and will end the campaign game.


## Functions for the radio communication handling


### void SC_Radio_Enable(dword radio_id);

This function will enable the radio usage with the id *radio_id.* Info about the actual usage is passed to the level script.


### void SC_Radio_Disable(dword radio_id);

This function will disable the radio usage with the id *radio_id.*


### BOOL SC_Radio_Get(dword *radio_id);

This function will return TRUE if the radio is enabled and in this case will fill the *radio_id* with the current enabled ID.


### void SC_RadioBatch_Begin(void);

This function marks the begining of the radio comunication. All speech functions called after this fucntion and before the SC_RadioBatch_End will be marked as communication.


### void SC_RadioBatch_End(void);

This function marks the end of the radio comunication.


### void SC_RadistBatch_Begin(void);

This function marks the begining of the radio comunication for the AI radist. All speech functions called after this fucntion and before the SC_RadistBatch_End will be marked as communication.


### void SC_RadistBatch_End(void);

This function marks the end of the radio comunication for the AI radist.


### void SC_RadioSet2D(BOOL willbe2D);

This fucntion can be used to set all radio speech to be played as 2D.


### void SC_RadioSet3DButDistanceLimit(BOOL enable);

This fucntion can be used to set all radio speech to be played as 3D.


### void SC_RadioBreak_Set(s_SC_SpeachBreakProps *props);

This function is used to define the radio breaks. OBSOLETE!


### void SC_RadioBreak_Get(s_SC_SpeachBreakProps *props);

This function is used to define the radio breaks. OBSOLETE!


### void SC_P_Radio_Enable(dword pl_id, dword radio_id);

This function will enable the radio usage *radio_id* for the player *pl_id.*


### BOOL SC_P_Radio_Used(dword pl_id, dword radio_id);

This function will return TRUE if the *pl_id* used the radio usage.


### void SC_PC_EnableRadioBreak(BOOL enable);

This function enables radio breaks.


## Functions - saving the game


### void SC_MissionSave(s_SC_MissionSave *info);

This function is used for the autosaving - all data are stored in the s_SC_MissionSave structure.


### void SC_EnableQuickSave(BOOL enable);

This function enables/disables quick save. Enabled by default.


## Functions - various functions


### void SC_SetObjectScript(char *obj_name, char* script_name);

This function can be used to force the specific object script to the dynamic object during the scene initialization callback of the level script.


### void SC_DisplayBinocular(BOOL enable);

Enabled/disables displaying of the binocular.


### void SC_DeathCamera_Enable(BOOL enable);

Enabled/disables the death camera - after the mission failed.


### void SC_Set_GoToPC_snd(dword member_id, dword peace, dword agressive, dword stealth);

This function can be used to force change of the acknowledgments of the PC team AI members after the PC calls them with the quick key.


### void SC_Set_RadioMan_RunDist(float dist);

This function will set the maximal distance for the radist when the radio is enabled - if the radioman is too far from the PC, he will stay on his place.


### void SC_PreloadBES(dword id, char *bes_name);

This function is used to preload the special equipment for the players during the scene initialization callback of the level script. See here.


### void SC_PreloadWeapon(dword type, BOOL fpv_to);

This function will preload the selected weapon, if *fpv_to* == TRUE including the FPV model.


### void SC_PreloadSound(dword snd_id, BOOL is3D);

This function will preload the selected sound.


### void SC_LevScr_Event(dword param1, dword param2);

This function will send the message to the level script with the specified parameters.


### void SC_StorySkipEnable(BOOL enable);

This function will enable the "story skip" - pressing enter, space or esc will cause the story skip callback to the level script.


### void SC_SetObjectives(dword objectives, s_SC_Objective *objective, float force_display_time);

This function will set the objectives - *objectives* is the number of the s_SC_Objective items in the *objective* array.


### void SC_SetObjectivesNoSound(dword objectives, s_SC_Objective *objective, float force_display_time);

This function will set the objectives - *objectives* is the number of the s_SC_Objective items in the *objective* array. No sound will be played.


### BOOL SC_GetScriptHelper(char *name, s_sphere* sph);

This function will fill the *sph* with the size and position of the script helper *name.* It will return FALSE if the script helper doesnot exist.


### void SC_DoExplosion(c_Vector3 *pos, dword type);

This function will create the explosion (1 grenade, 2 grenade launcher, 3 mortar). Valid ONLY in the single player or on the server. There must be human PC object created!


### void SC_ArtillerySupport(BOOL enable);

Use this function to enable/disable artillery support.


### void SC_SetBombInfo(s_SC_BombInfo *info);

This function will set the radio communication for the artillery support. See s_SC_BombInfo structure.


### void SC_SetMapFpvModel(char *bes_filename);

This function will force the FPV map model to the specified *filename.*


### void SC_MakeBurning(s_sphere *sph);

This function will set everything in the sphere *sph* on fire. BURN!!!


### void SC_GetLoudShot(s_sphere *sph);

This function will enable the loud shot callback for the level script in the sphere sph.


### void SC_SetCommandMenu(dword text_id);

This function will disable the command menu (text_id is now unused).


### float SC_GetVisibility(void);

This function will return the visibility of the current scene.


### void SC_ShowHelp(dword *txt, dword texts, float time);

This function will show the game hint for the time *time.* Text id's are stored in the array *txt* with the size *texts.*


### void SC_SetAmmobagAmmo(dword ammo_type, BOOL enable);

This function can be used to change the types of the ammo in the ammobags - by default it contains only US type of ammo.


### void SC_ShowMovieInfo(dword *txt);

This function will type the movie style subtitles to the screen. txt is a pointer to the array with three text id. If the specified pointer is zero, the subtitles will be cleared.


### void SC_Debrief_Clear(void);

This function will clear the debriefing data for current mission.


### void SC_Debrief_Add(s_SC_DebriefInfo *add_info);

This function will add debriefing data to current data.


### void SC_Debrief_Get(s_SC_DebriefInfo *info);

This function will fill the data structure with current debriefing data.


### void SC_HUD_DisableRadar(BOOL disable);

This function will disable/enable the radar.


### void SC_HUD_RadarShowPlayer(dword pl_id, dword color);

This function will cause the player of *pl_id* to be shown on the radat with ARGB *color.*


### void SC_HUD_RadarShowPos(c_Vector3 *vec, dword color);

This function will show the position *vec* on the radar with ARGB *color*. Only one place can be visible at the time.


### void SC_HUD_TextWriterInit(s_SC_HUD_TextWrite *initdata);

This function will initialize text writer object (text shown on the screen) with data stored in the structure s_SC_HUD_TextWrite. There can be only one text writer active at one time.


### void SC_HUD_TextWriterRelease(float fade_out_time);

This function will release text writer object - it will fade out of the screen in specified time.


### void SC_CreateMissile(dword missile_id, dword author_pl_id, c_Vector3 *from, c_Vector3* at);

This function will create the missile shot *from* aiming *at. author_pl_id* must be valid player pointer!


### void SC_GetSystemTime(s_SC_systime *info);

This function will return the system time.


### void SC_Fauna_DoSoundAlert(c_Vector3 *pos);

This function will alert fauna from the place *pos.*


### void SC_Fauna_KillThemAll(s_sphere *sph);

This function will kill all the fauna in the specified sphere.


## Functions for the unipages


### void SC_UP_Open(dword what, dword level);

This function will open the unipage with id *what* with parameter *level.*


# Appendix A -sc_level.h - macro and functions for the level script

sc_level.h is simple set of macros, functions and other stuff useful for the level scripts.


## Macros


### InitSide(side,group,hideout)

This macro can be used to initialize the *side* with specified number of *groups* and *hideouts.*


### InitGroup(side,group,players)

This macro can be used to initialize the *group* of the *side* with max. number of *players.*


### InitGroup2(side,group,players,followdist)

This macro can be used to initialize the *group* of the *side* with max. number of *players* and follow distance in the formation of *followdist.*


### SaveGame(name,desc)

This function will autosave the game with the *name* and description *desc.*


### SaveGame2(name,desc)

This function will autosave the game with the *name* and description *desc.* No screenshot will be saved.


## Functions


### void SetFollowOrder();

This function will set the standard follow order of the player's team.


### void Clear_Objectives();

This function will clear the objectives.


### void Add_Obj(dword textid);

This function will add the objective *textid.*


### void Add_ObjNS(dword textid);

This function will add the objective *textid.* No sound will be played.


### void Complete_Obj(dword textid);

This function will mark the objective *textid* as completed.


### void Fail_Obj(dword textid);

This function will mark the objective *textid* as failed.


### int Get_Obj_Stat(dword textid);

This function will return the status of the objective *textid.*


## Predefined Variables

There are few predefined variables in the sc_level.h

*Dword gphase* stores the current phase of the level script.

*Dword pointstatus* is used to store the status of the pointman.

*s_SC_Objective Objectives[10]* is used to store the values of current objectives.

*int objcount* contains number of current objectives.

*BOOL savegame[SAVEGAMECOUNT]* contains information about saved games (which autosaves were already used).


# Appendix B - list of all example scripts and include files in the SDK


## Level scripts

Level scripts are in the SDK directory scripts/levelscripts

*Pure_level.c* - absolutely pure level.c, just with the definition of the scriptmain function and with switch for various level messages.

*Level.c* - very simple level script for the tutorial- see commentary inside.

*Sc_level.h* - simple library/include file for level scripts.


## Player scripts

All files are in SDK/scripts/players/:

*player.c -* sample human player script

*Bronson.c* - sample team member script

*teammate.inc* - include file used for the team members

*vc0.c and vc.inc* - sample of VC AI script


### Equipment handling include files

All files are in SDK/scripts/players/eqp:

*us_equips.inc* - this include file contains various versions of the equipment for the American character for use in the creation of the player.

*vc_equips.inc* - this include file contains various versions of the equipment for the Vietnamese character for use in the creation of the player.

*vcfa-equip.inc* - this include file contains set of functions which were used to set the equipment for the Vietnamese characters in the Fist Alpha.

*VCAutoGenEqp.inc* - this include file contains function for the setting data for the automatic equipment.


## Sound scripts

Sound scripts are in the SDK directory scripts/sound, there is only one very simple sound.c.


## Script helper scripts

Scripts are located in the SDK directory scripts/scr_helper

*scripthelper.c* - this is plain script, just definition of the main function.

*liedown.c -* this is sample script, which will force all AI characters entering it to crawl


## Dynamic object scripts

All scripts are located in the SDK directory scripts/objects

*Object.c* - this is plain basic object script, just definition

*Bird.c* - this script is used for small flying birds in some levels of the VC - just moves some DO on the animation path

*Doors.c* - simple script for doors with possibility to define few things

*Doorslocked.c* - same as above, only the doors will be locked until some other scripts enables them with the global variable

*Hitable.c* - very simple script - will send message to the level script after hit

*Usable.c* - script for usage - sends message to the level script when used

*Justdestruction.c* - sample of dynamic object with dynamic destructions

*Gaz_67.c -* sample of vehicle script

*Huey.c* - sample of the helicopter script


## Weapon scripts

All scripts are located in the SDK directory scripts/weapons

*VVH_M16_3pv.c* - sample script for the 3PV weapon

*VVH_M16_fpv.c* - sample script for the FPV weapon

*mounted_besa.c* - sample script for the mounted weapon (ZB37)


### Single player Tutorial scripts

*Level.c* - tutorial level.c

*Teammate.inc* - include file for the US team.

*Vc.inc* - include file for vietcongs.

*Player.c* - script for the human pc

*Bronson.c, Defort.c, Hornster.c, Joe_Crocker.c, Nhut.c* - team scripts with definitions for the include file

vc0.c, vc1.c, vc2.c - vietcong scripts with definitions for the include file


# Appendix C - list of all weapons in the Vietcong


## FPV Weapons and items

These are the ID of weapons and items player can have in his inventory and use them.

Weapons and inventory items are defined in the weap.txt file and weap2.txt file (for Fist Alpha) in the engine directory ini - for the definition see here. List of ID of weapons is:

VIETCONG(items.txt)

1 - M16 assault rifle

2 - AK47 assault rifle

4 - M1 garand sniper rifle

6 - PPS-41 submachinegun

7 - Colt M1911 pistol

8 - Tokarev pistol

9 - Makarov pistol

10 - Revolver .38

11 - Remmington shotgun

12 - Winchester sniper rifle

14 - SVD Dragunov sniper rifle

15 - SKS Simonov rifle

17 - M60 machinegun

18 - Degtarjev machinegun

19 - USM3 submachinegun

20 - M2C50 - heavy machine gun, used for mounted weapons on the chopper

21 - Thompson submachinegun

22 - S&W silenced pistol

23 - PPS-43 submachinegun

25 - M1 carabine

26 - Mosin Nagant rifle

27 - M79 grenade launcher

28 - double barelled shotgun

29 - US knife

30 - VC knife

50 - VC grenade

51 - Lightstick

52 - Booby trap

55 - C4 explosive

58 - FPV map

59 - US grenade

60 - Radio

61 - Ammobag

62 - medibag

63 - medikit

140 - mini radio

53,54,64-138 are intel items

Fist Alpha(items2.txt)

3 - Scorpion smg

5 - DP2 machinegun

13 - Tokarev SVT rifle

16 - Tokarev SVT sniper rifle

24 - M14 rifle

31 - M14 sniper rifle

32 - Sten SMG

33 - Machete

34 - BESA/ZB37 hmg for mounted weapon

49 - Claymore mine


## Stage weapons and items

Stage items is stuff placed in the level, either by designer, spawned by script or when the item fell (is thrown out) out of the player. These items are defined in the items.txt and items2.txt, for definition see here.

VIETCONG (items.txt)

1 - M16 assault rifle

2 - AK47 assault rifle

4 - M1 garand sniper rifle

6 - PPS-41 submachinegun

7 - Colt M1911 pistol

8 - Tokarev pistol

9 - Makarov pistol

10 - Revolver .38

11 - Remmington shotgun

12 - Winchester sniper rifle

14 - SVD Dragunov sniper rifle

15 - SKS Simonov rifle

17 - M60 machinegun

18 - Degtarjev machinegun

19 - USM3 submachinegun

21 - Thompson submachinegun

22 - S&W silenced pistol

23 - PPS-43 submachinegun

25 - M1 carabine

26 - Mosin Nagant rifle

27 - M79 grenade launcher

28 - double barelled shotgun

50 - VC grenade

55 - C4 explosive

59 - US grenade

60 - Radio

62 - medibag

63 - medikit

Ammo:

71 - M16 assault rifle

72 - AK47 assault rifle

74 - M1 garand sniper rifle

76 - PPS-41 submachinegun

77 - Colt M1911 pistol

78 - Tokarev pistol

79 - Makarov pistol

80 - Revolver .38

81 - Remmington shotgun

82 - Winchester sniper rifle

84 - SVD Dragunov sniper rifle

85 - SKS Simonov rifle

87 - M60 machinegun

88 - Degtarjev machinegun

89 - USM3 submachinegun

91 - Thompson submachinegun

92 - S&W silenced pistol

93 - PPS-43 submachinegun

95 - M1 carabine

96 - Mosin Nagant rifle

97 - M79 grenade launcher

98 - double barelled shotgun

128 - VC grenade

129 - US grenade

Specials:

136 - unlimited smoke grenade with particle 184

140 - red flare

141 - bag

142 - lightstick

143 - booby trap

144 - C4

145 - US flag

146 - VC flag

147 - smoke grenade

148 - shot from m79

149 - white flare

150-229 are intel items

FIST ALPHA (item2.txt)

3 - Scorpion smg

5 - DP2 machinegun

13 - Tokarev SVT rifle

16 - Tokarev SVT sniper rifle

24 - M14 rifle

31 - M14 sniper rifle

32 - Sten SMG

33 - bandage

AMMO:

41 - Scorpion smg

42 - DP2 machinegun

43 - Tokarev SVT rifle

44 - Tokarev SVT sniper rifle

45 - M14 rifle

46 - M14 sniper rifle

47 - Sten SMG

Specials:

137 - unlimited smoke grenade

138 - claymore switch

139 - claymore


# TUTORIAL A - creating simple multiplayer level

Creating basic multiplayer level is simple. First you need level of course. Feel free to use any of the levels in the game. This simple tutorial will deal ONLY with the scripting part of the MP game creation.

For basic MP level you will need just two scripts - level script and MP script.


### Level script

Level script for the MP is quite simple - you just need to initialize groups and sides. But if this level will be used for more types of the mission, you should hide unnecessery stuff like flags. VC contains simple include file used for almost all levels in VC - DEV/COMPILER/INC/mplevel.inc.

This include file contains functions:

InitScene

SetAmmoBoxes

DisableTT

DisableRW

DisableBedny (used for disabling ammo boxes)

Actual level script can be simple as this:


```c
#include <inc\sc_global.h>
#include <inc\mplevel.inc>

dword gphase = 0;


int ScriptMain(s_SC_L_info *info){
float fl;
int i;
s_SC_initside initside;
s_SC_initgroup initgroup;
c_Vector3 vec;
char txt[32];
s_SC_Ai_PlFollow follow[6];
dword follow_order[6];
dword point_order[6];
void *nod;


info->next_exe_time = 10.0f;


switch (info->message){

case SC_LEV_MES_INITSCENE:


InitScene(info);

// hide C4
nod = SC_NOD_Get(NULL,"c4");
if (nod) SC_DUMMY_Set_DoNotRenHier2(nod,TRUE);

SC_SetMapFpvModel("g\\weapons\\Vvh_map\\map_nvabaseMP.BES");
SC_ArtillerySupport(FALSE);


switch(SC_ggi(GVAR_MP_MISSIONTYPE)){

case GVAR_MP_MISSIONTYPE_RW: SC_sgf(400,15);
SC_sgf(401,5);
break;

case GVAR_MP_MISSIONTYPE_ATG: SC_SetObjectScript("bombplace","ini\\multiplayer\\scripts\\atg_dobj.c");
break;

case GVAR_MP_MISSIONTYPE_CTF: SC_sgf(400,25);
SC_sgf(401,5);
break;

}// switch(SC_ggi(GVAR_MP_MISSIONTYPE))


break;

case SC_LEV_MES_TIME:

switch (gphase){
case 0: //first time init
//various inits
CLEAR(initside);
CLEAR(initgroup);
initside.MaxHideOutsStatus = 64; //init sides and groups initside.MaxGroups = 8;
SC_InitSide(SC_P_SIDE_US,&initside);

initside.MaxHideOutsStatus = 64;
initside.MaxGroups = 8;
SC_InitSide(SC_P_SIDE_VC,&initside);

initgroup.SideId = SC_P_SIDE_US; //US a-team initgroup.GroupId = 0;
initgroup.MaxPlayers = 64;
SC_InitSideGroup(&initgroup);

initgroup.SideId = SC_P_SIDE_VC; //generic Vietcong initgroup.GroupId = 0;
initgroup.MaxPlayers = 64;
SC_InitSideGroup(&initgroup);

//for coop modes
initgroup.GroupId = 1;
initgroup.MaxPlayers = 8;
SC_InitSideGroup(&initgroup);

//
initgroup.GroupId = 2;
initgroup.MaxPlayers = 8;
SC_InitSideGroup(&initgroup);

//
initgroup.GroupId = 3;
initgroup.MaxPlayers = 12;
SC_InitSideGroup(&initgroup);

//
initgroup.GroupId = 4;
initgroup.MaxPlayers = 8;
SC_InitSideGroup(&initgroup);

//
initgroup.GroupId = 5;
initgroup.MaxPlayers = 4;
SC_InitSideGroup(&initgroup);


gphase=1;
break;
}// gphase switch
break;
}

return 1;

}// int ScriptMain(void)
```

Just create sides and groups, hide unnecessery stuff and set dynamic object scripts if they are used.


### Multiplayer script

MP script is bit more complicated, of course it depends on what you want to have there.

Essentially you need to handle all messages to the script.

Let's say you just want to recreate the team death match script.

Declaration of the variables

You will need just two global variables for the TDM - just for storing the score (frags), so assing id to them and make local variables:


```c
#define GVAR_SIDE0FRAGS 500
#define GVAR_SIDE1FRAGS 501
int gSideFrags[2] = {0,0};
int gCLN_SideFrags[2];
```

You will also need some recover variables:


```c
dword gRecs = 0;
s_SC_MP_Recover gRec[REC_MAX];
float gRecTimer[REC_MAX];
float gNextRecover = 0.0f;
```

And some variables for storing of the time, end rules and values etc:


```c
dword gEndRule;
dword gEndValue;
float gTime;
dword gPlayersConnected = 0;
```

For simplicity, prepare function for updating frags in global variables:


```c
void UpdateSideFrags(void){
SC_sgi(GVAR_SIDE0FRAGS,gSideFrags[0]);
SC_sgi(GVAR_SIDE1FRAGS,gSideFrags[1]);
}
```

SC_NET_MES_LEVELPREINIT

You need to set few thing before loading the level here:

Set global variable GVAR_MP_MISSIONTYPE to type of the mission (TDM)

Store end rule and end value from info->param and set global time to zero (declare all of those variables). As there will be no AI opponents, set them off.


```c
case SC_NET_MES_LEVELPREINIT: SC_sgi(GVAR_MP_MISSIONTYPE,GVAR_MP_MISSIONTYPE_TDM);
gEndRule = info->param1;
gEndValue = info->param2;
gTime = 0.0f;
SC_MP_EnableBotsFromScene(FALSE);
```

SC_NET_MES_LEVELINIT

Now actual initialization of the level. Set possible sides to all. For the TDM all players will start just with their pistol and grenades, so set class limit for the deathmatch.


```c
case SC_NET_MES_LEVELINIT:

SC_MP_SRV_SetForceSide(0xffffffff);
SC_MP_SetChooseValidSides(3);

SC_MP_SRV_SetClassLimitsForDM();


CLEAR(hudinfo);
hudinfo.title = 1051;
```

Now set the HUD.


```c
hudinfo.sort_by[0] = SC_HUD_MP_SORTBY_FRAGS;
hudinfo.sort_by[1] = SC_HUD_MP_SORTBY_KILLS;
hudinfo.sort_by[2] = SC_HUD_MP_SORTBY_DEATHS | SC_HUD_MP_SORT_DOWNUP;
hudinfo.sort_by[3] = SC_HUD_MP_SORTBY_PINGS | SC_HUD_MP_SORT_DOWNUP;

hudinfo.pl_mask = SC_HUD_MP_PL_MASK_FRAGS | SC_HUD_MP_PL_MASK_KILLS | SC_HUD_MP_PL_MASK_DEATHS;
hudinfo.use_sides = TRUE;
hudinfo.side_name[0] = 1010;
hudinfo.side_color[0] = 0x440000ff;
hudinfo.side_name[1] = 1011;
hudinfo.side_color[1] = 0x44ff0000;

hudinfo.side_mask = SC_HUD_MP_SIDE_MASK_FRAGS;


SC_MP_HUD_SetTabInfo(&hudinfo);
```

Set other stuff like friendly fire, disappearing of the items etc.


```c
SC_MP_AllowStPwD(TRUE);
SC_MP_AllowFriendlyFireOFF(TRUE);
SC_MP_SetItemsNoDisappear(FALSE);
```

If info->param2 is true, it's first time init and if param1 is true too, it's first time init for the server machine. So get settings from the server, synchronize variables used for frags and update them, then fill recover points.


```c
if (info->param2){

if (info->param1){
// it's server

SC_MP_GetSRVsettings(&SRVset);
SC_MP_SRV_InitWeaponsRecovery((float)SRVset.dm_weap_resp_time);

SC_MP_Gvar_SetSynchro(GVAR_SIDE0FRAGS);
SC_MP_Gvar_SetSynchro(GVAR_SIDE1FRAGS);
UpdateSideFrags();

gRecs = 0;


i = REC_MAX - gRecs;
SC_MP_GetRecovers(SC_MP_RESPAWN_DM,&gRec[gRecs],&i);
gRecs += i;

if (gRecs==0) SC_message("no recover place defined!");

CLEAR(gRecTimer);

}// if (info->param1)

}//if (info->param2)


break;// SC_NET_MES_LEVELINIT
```

SC_NET_MES_SERVER_RECOVER_TIME

Recover time is important :o) Everytime player connects to the game or is killed, his machine asks server for the recover time. If info->param2 is TRUE, it's first time connect, so just set it to some small value. If player was killed, set the time for longer.


```c
case SC_NET_MES_SERVER_RECOVER_TIME: if (info->param2){
info->fval1 = 0.1f;
}
else{
// killed
info->fval1 = 5;
}
break;
```

SC_NET_MES_SERVER_RECOVER_PLACE

Now the message asking for the recover place. As you already have initialized structure for the recovers, just set the data via pointer in the info->param2 for the desired place. For simplicity, use SC_MP_SRV_GetBestDMrecov function for finding the best place.


```c
case SC_NET_MES_SERVER_RECOVER_PLACE: precov = (s_SC_MP_Recover*)info->param2;
i = SC_MP_SRV_GetBestDMrecov(gRec,gRecs,gRecTimer,NORECOV_TIME);
gRecTimer[i] = NORECOV_TIME;
*precov = gRec[i];
break;
```

SC_NET_MES_RESTARTMAP

Map restarting. Clear frags time, player status and recover all players. Simple.


```c
case SC_NET_MES_RESTARTMAP: gTime = 0;
CLEAR(gSideFrags);
UpdateSideFrags();
SC_MP_SRV_ClearPlsStats();
SC_MP_SRV_InitGameAfterInactive();
SC_MP_RecoverAllNoAiPlayers();
break;
```

SC_NET_MES_RULESCHANGED

Rules were changed, so change them.


```c
case SC_NET_MES_RULESCHANGED: gEndRule = info->param1;
gEndValue = info->param2;
gTime = 0.0f;
break;
```

SC_NET_MES_SERVER_KILL

This message means someone was killed. So find out who was that and increase frags for his enemy or decrease for his team, if he killed himself.


```c
case SC_NET_MES_SERVER_KILL: SC_P_GetInfo(info->param1,&plinfo);
sideA = plinfo.side;
if (info->param2){
SC_P_GetInfo(info->param2,&plinfo);
sideB = plinfo.side;
}
else sideB = 0xffffffff;
if (sideA==sideB){
gSideFrags[sideB]--;
}
else{
if (sideB!=0xffffffff) gSideFrags[sideB]++; }
UpdateSideFrags();
break;// SC_NET_MES_SERVER_KILL
```

SC_NET_MES_CLIENT_TICK

Client tick is usually pretty simple. In the case of the TDM, you just need to show icons with actual frags. So get them from the global variables and show them.


```c
case SC_NET_MES_CLIENT_TICK: gCLN_SideFrags[0] = SC_ggi(GVAR_SIDE0FRAGS);
gCLN_SideFrags[1] = SC_ggi(GVAR_SIDE1FRAGS);
SC_MP_SetSideStats(0,gCLN_SideFrags[0],0);
SC_MP_SetSideStats(1,gCLN_SideFrags[1],0);
for (i=0;i<2;i++){
icon[i].type = SC_HUD_MP_ICON_TYPE_NUMBER;
icon[i].icon_id = 3*i;
icon[i].value = gCLN_SideFrags[i];
icon[i].color = 0xffffffff;
}
SC_MP_SetIconHUD(icon,2);
break;// SC_NET_MES_CLIENT_TICK
```

SC_NET_MES_SERVER_TICK

Server tick is usually the heart of the MP script. Here you watch time, scoring etc. For the TDM it's pretty simple. Check end rule, decrease recover timers and watch if there are any players in the game. If they are not, reset the game status.


```c
case SC_NET_MES_SERVER_TICK: switch(gEndRule){
case SC_MP_ENDRULE_TIME:

if (gPlayersConnected>0) gTime += time;
SC_MP_EndRule_SetTimeLeft(gTime,gPlayersConnected>0);

if (gTime>gEndValue){
SC_MP_LoadNextMap();
return TRUE;
}

break;

case SC_MP_ENDRULE_FRAGS: if (((gSideFrags[0]>0)&&(gSideFrags[0]>=gEndValue))
||((gSideFrags[1]>1)&&(gSideFrags[1]>=gEndValue))){
SC_MP_LoadNextMap();
return TRUE;
}
break;
default: SC_message("EndRule unsopported: %d",gEndRule);
break;
}

for (i=0;i<gRecs;i++)
gRecTimer[i] -= info->elapsed_time;
j = 64;
if (SC_MP_EnumPlayers(enum_pl,&j,SC_MP_ENUMPLAYER_SIDE_ALL)){
if ((j==0)&&((gSideFrags[0]+gSideFrags[1])!=0)){
gSideFrags[0] = 0;
gSideFrags[1] = 0;
UpdateSideFrags();
}// if ((side[0]+side[1])==0)
}
gPlayersConnected = j;
break;
```

Finished. For your scripts it will be probably bit trickier - take a look at the sample scripts how to do other stuff.

Or you can take a look at rather good tuturial from Genoil at the web adress http://www.doeds.com/egg/index.html. I admit it's much better than this one :o).


# TUTORIAL B - creating simple multiplayer cooperative level

Creating of classical coop mission is VERY simple, you don't need any scripting knowledge to do it :o). You can use standard coop script for the MP and use sample VC coop script. So what you need to do?

Load your level.

Now you need to create few player objects, everywhere you want to have VC. Save mission.

Copy vcbasic.inc and vcbasic.c from SDK directory scripts/MP scripts/Coop to the script directory of your level. Now take a look how many VC players you have - you will need copy of vcbasic.c for each one of them - so make a copies like vcbasic2.c, vcbasic3.c etc.

Assign each player object one script. Save your mission.

Now open all .c files. File contains some definitions, you can leave most of them as they are - if you don't mind that ALL VC will have AK and look the same. What you need to change is ID_GROUP and ID_MEMBERID.

ID_GROUP is ID of the group - if you have more VC at one place, it's usually good idea to have them in the same group. ID_MEMBERID must be different for all players in the group.

Now the coop mission should work, but all VC will look the same, have same weapons and all of them will stay on one place and will not walk around. But it's the basic, isn't it?


# TUTORIAL C - creating simple single player level


### Mission description

Let's say we have a very simple level - just piece of jungle, PC and his team will start on one side and have to destroy all three VC in the area and than exit the level on the other side. Level will start with simple radio comm, after killing all three VC another radio com will enable exit from the level.

Finished tutorial scripts are in the SDK/scripts/tutorial directory.


### Preliminatory work

First you need some level - any from the Vietcong will do. Open it in the editor, select all player objects and delete them. Rename the scene and it's sublevel directory and save it. Than place 6 player objects in the beginning of the level and three other somewhere accross the path. Choose some waypoint as the mission end and write it's name somewhere (or rename it).

Then define the path for the pointman. Choose some name (tutorial assumes the name POINTMANPATH# plus number) and start naming the waypoints you want pointman use (you can use just two, first and last) - fastest way to do so is select waypoint near the team and name it POINTMANPATH. Then select another and name it also POINTMANPATH - engine will automatically append the #number to it.

Save the scene.

Now prepare the texts - find them in the text database, or make your own. You will need texts for first and second radio communication, for the objectives, for the pointman interaction and for the scream of the player (when he kills last vietcong - this speech will enable the radio communication.


### Level script

Start with the level script. Copy the pure_level.c template from the SDK/scripts/levelscripts to the data script subdirectory of the level and rename it to the level.c. Also copy the library sc_level.h there.

Include the library to the level.c with line


```c
#include "sc_level.h"
```

Before it place some definitions:


```c
//number of the save games
#define SAVEGAMECOUNT 5

//unique numeric mission identifier - see sc_def.h
#define MISSION_IDENTIFICATOR 0

//set the base of the name for the pointman path
#define CHECKPOINTBASE "POINTMANPATH#%d"
```

To the ScriptMain add timetick handling:


```c
case SC_LEV_MES_TIME: if (!gphase) Levelnit(info);
else TimeTick(info);
break;
```

Now create void Levelnit(s_SC_L_info *info) function:


```c
void Levelnit(s_SC_L_info *info){
s_SC_initside initside;
s_SC_initgroup initgroup;

SC_sgi(SGI_CURRENTMISSION,MISSION_IDENTIFICATOR); //initialization of the global variable with the mission identifier

CLEAR(initside);
CLEAR(initgroup);

InitGlobals(); //initialize various global variables, clear objectives etc - see sc_level.h SetRadioProps(); //sets radio properties, only the visibility of the subtitles

InitSide(0,8,32); //initialization of the US SIDE InitSide(1,16,64); //initialization of the VC SIDE

InitGroup2(0,0,6,30) //team initialization, with follow distance 30 meters

InitGroup(1,0,16); //vietcong generic group initialization

SC_FadeTo(TRUE,0); //blackout the screen until the rest of the game initializes

//do some other initialization here
//for example taking positions of important places in the level
SC_GetWp("WayPoint#100",&levelexit);

SC_ArtillerySupport(FALSE); //disable arty support SC_Ai_EnableRelaxWalk(0,0,FALSE); //disable relaxed walk for the team SetFollowOrder(); //set standard follow order

ResetCheckPoints(1,10); //set the pointman path from the waypoint "POINTMANPATH1" to "POINTMANPATH10" including

SetLevelPhase(1); //switch level phase to 1 (both globalvar and local gphase)
nextex(0.5f); //set next execution time to 0.5 seconds
}
```

This function initializes various basic things, especially sides and groups for the players.

As we already know we will need to check if the player reached some special place, fill it's name to the levelexit variable (do not forget to declare it as a global variable). Function will also prepare the pointman's path, follow order of the team and various other settings.

Now create the TimeTick function. Time tick is driven by the gphase variable - variable contains info about what is currently happening in the level. Use the state 1 for the FirstTimeTick to start few things just after the mission start. In this case it will only initialize first radio communication


```c
void FirstTimeTick(s_SC_L_info *info){
float time;

SC_FadeTo(FALSE,0.5f); //unfade the screen from blackness.
//do some chitchat

time=1;
SC_RadioBatch_Begin(); //start radio comm SC_P_Speech2(SC_PC_Get(),50939,&time); //player says 50939 time+=0.5f; //small delay SC_SpeechRadio2(50940,&time); //radio says 50940 time+=0.5f; //small delay SC_P_SpeechMes2(SC_PC_Get(),50939,&time,1);//player says 50939, after finishing speech script will receive speech callback 2 SC_RadioBatch_End();
SetLevelPhase(2);
}
```

After the end of the communication the level script will receive the speech callback 1- we will handle this later. Now start the TimeTick function:


```c
void TimeTick(s_SC_L_info *info){
float time;
c_Vector3 vec;


switch (gphase){
case 1: if (!SC_PC_Get()) return; //if the player object was not initialized, something is wrong, return!
//you may also want to detect other created players
FirstTimeTick(info);
break;
```

The check for the value of SC_PC_Get() (pointer to the PC object) is just for case the game haven't initialized yet.

Now for the state 2. It will end just as all congs are dead. So prepare special function AllCongsDead() which will return TRUE if all congs are dead. Function is really simple:


```c
BOOL AllCongsDead(){
int i;
for (i=0;i<2;i++)
if (SC_P_IsReady(SC_P_GetBySideGroupMember(1,0,i))) return FALSE;
return TRUE;
}
```

Now add the state 2 to the TimeTick:


```c
case 2: if (AllCongsDead()){
timer=5; //they are all dead, so wait few seconds... SetLevelPhase(3);
}
break;
```

We don't want to player do something exact time the last cong hit the dirt, so declare global variable timer. Set it to five and add state 3, which will slowly decrement it till it reaches zero:


```c
case 3: timer-=info->elapsed_time;
if (timer<0){
//timer elapsed, so say something.
time=SC_P_GetWillTalk(SC_PC_Get()); //set the time to the time when pc stops talking SC_P_SpeechMes2(SC_PC_Get(),50939,&time,12);
//player says 50939, after finishing speech script will receive speech callback 2
SetLevelPhase(4);
}
break;
```

When the timer is zeroed, set local variable time to the end of the pc talk time (usually it will be zero, but just to be sure...) and make player say something - after speech the script will receive speech callback 12 - we will deal with it later. State 4 is just waiting till the player picks up the radio and finishes talking.


```c
case 4: //script waits until player finished radio comm. break;
```

Speech callback will switch the level phase to 5 after the radio comm, so now player can exit the level:


```c
case 5: //player can now exit the level SC_PC_GetPos(&vec); //get players position if (SC_IsNear2D(&vec,&levelexit,3)){ //is player maximum 3 meters from the level exit? SetLevelPhase(100);
SC_MissionDone(); //end mission
}
break;
```

We just need to take his position, compare it with the level exit. And if he is in desired radius, end the game. Blam.

Now next important thing, speech callback. We know we will use three callback - after the end of each radio comm and after the speech when all congs are dead. Also we will need one callback for the pointman handling. So let's create the SpeechDone(int param):


```c
void SpeechDone(int param){
//param contains id of the speech finished

switch(param){
case 1: //this is the end of the radio comm 1 (from the first time tick
//save the game - warning, after load this call will beexecuted again, so be sure to handle this situation
if (!savegame[param]) {
savegame[param]=TRUE; //this save is now used, want be repeated
//add some objectives
Add_Obj(54183);
Add_Obj(54184);
SaveGame(54201,54202);
}
break;
case 2: //this is the end of the radio comm 2 (see RadioUsed()
//save the game - warning, after load this call will beexecuted again, so be sure to handle this situation
if (!savegame[param]) {
savegame[param]=TRUE; //this save is now used, want be repeated SetLevelPhase(5); //for example, do what you want here SaveGame(54201,54202);
}
break;
case 12: //callback from the timetick - player said something, so for example enable the radio usage SC_Radio_Enable(2);
Complete_Obj(54183); //complete some objective break;
case 99: SC_Ai_SetPeaceMode(0,0,SC_P_AI_PEACEMODE_POINT);
break;
default: break;
}
}
```

Callback 1 and 2 are after the radio, so they are used for saving. First radio comm will also add some objectives. Second will switch the level gphase to 5.

Callback 12 is used to enable radio comm 2 and 99 is used to set the team forward in the point mode. Simple.

Now there are only two things missing - the radio communication and pointman interaction.


```c
void RadioUsed(int param){
float time;

time=SC_P_GetWillTalk(SC_PC_Get()); //set the time to the time when pc stops talking

//param contains id of the radio communication
switch(param){
case 2: //radio communication number 2 (enabled with SC_Radio_Enable(2);
SC_RadioBatch_Begin(); //start radio comm SC_P_Speech2(SC_PC_Get(),50939,&time); //player says 50939 time+=0.5f; //small delay SC_SpeechRadio2(50940,&time); //radio says 50940 time+=0.5f; //small delay SC_P_SpeechMes2(SC_PC_Get(),50939,&time,2);//player says 50939, after finishing speech script will receive speech callback 2 SC_RadioBatch_End();
break;
}
}
```

Radio is simple, pointman is bit more complicated. First you must create the info callback (the one engine sends with request what text to show?)


```c
BOOL PointInteractInfo(s_SC_L_info *info){
PointTalkCheck; //check if poitman can talk at all switch (info->param1){
case 0: info->param3=2115; //to let pointman lead the team break;
case 1: info->param3=2118; //to stop the pointman break;
case 2: info->param3=2119; //to talk with the pointman break;
}
return TRUE;
}
```


```c
Pointman can be in three states - leading team, holding position/following player or leading, but staying for some reason. Either he waits for more players or he has no path defined. In first case just play some speech (PC order, pointman acknowledgment) and after the speech ends and invokes the 99 speech callback, pointman will go forward (SC_Ai_SetPeaceMode(0,0,SC_P_AI_PEACEMODE_POINT);). If you want to stop him, just set the group ai to hold. Third case is more complicated. First use the SC_Ai_GetCurCheckPoint(0,0,&vec)to find out if he has the path defined - if it's ok, just say something. In the other case there's probably something wrong - maybe player already was on the last waypoint? This tutorial just does nothing in this case...
```


```c
BOOL PointInteract(s_SC_L_info *info){
c_Vector3 vec;
float time;

PointTalkCheck; //check if poitman can talk at all


time=SC_P_GetWillTalk(SC_PC_Get()); //set the time to the time when pc stops talking

switch (info->param1){
case 0: //pointman is in hold or follow mode - lead the team! SC_P_Speech2(SC_PC_Get(),51005,&time); //pc gives order time+=0.5f;
SC_P_SpeechMes2(info->param2,5410 + rand()%5,&time,99); //pointman responds with some random talk, finished with callback 99 break;
case 1: SC_Ai_SetPeaceMode(0,0,SC_P_AI_PEACEMODE_HOLD); //HOLD! break;
case 2: //pointman is leading, but stays on the place if (SC_Ai_GetCurCheckPoint(0,0,&vec)) //path is defined, so he is waiting for the others switch (rand()%4){
case 0: SC_P_Speech2(info->param2,5404,&time);
break;
case 1: SC_P_Speech2(info->param2,5408,&time);
break;
case 2: SC_P_Speech2(info->param2,5409,&time);
break;
case 3: SC_P_Speech2(info->param2,5418,&time);
break;
}
/* else DoSomeThing();
this means Pointman has no defined path */ break;
}
return TRUE;
}
```

So, level script is finished.


### Human PC script

Second create the player.c, which will handle the PC player. For our means it can be pretty simple. Just fill the data for the SC_P_Create function, add equipment from the us_equips.inc file and after the player was created set his speech distance to 20 meters.


```c
#include <inc\us_equips.inc>

dword gphase = 0;

void equipplayer(s_SC_P_CreateEqp *eqp, int* count){
Equip_BANGS_Full(eqp,count);
}

int ScriptMain(s_SC_P_info *info){
s_SC_P_Create pinfo;
s_SC_P_CreateEqp eqp[10];
c_Vector3 vec,pl_pos;
float time;
int eqpcount;


if (info->message!=SC_P_MES_TIME) return FALSE;
if (gphase==0){

CLEAR(pinfo);CLEAR(eqp);
pinfo.type = SC_P_TYPE_PC;
pinfo.side = SC_P_SIDE_US;
pinfo.group = 0;
pinfo.member_id = SC_P_MEMBERID_CAPTAIN;
pinfo.inifile = "ini\\players\\default_camo.ini";
pinfo.name_nr = 2500;

pinfo.weap_knife = 0;
pinfo.weap_pistol = 7;
pinfo.weap_main1 = 23;
pinfo.weap_main2 = 4;
pinfo.weap_slot1 = 59;

pinfo.recover_pos = info->pos;
equipplayer(eqp,&eqpcount);
pinfo.eqps = eqpcount;
pinfo.eqp=eqp;
info->pl_id = SC_P_Create(&pinfo);
gphase = 1;
}
info->next_exe_time = 0.1f;

if (!SC_P_IsReady(info->pl_id)){
info->next_exe_time = 0.01f;
return 1;
}

switch(gphase){
case 1: gphase = 2;
SC_P_SetSpeachDist(info->pl_id, 20.0f);
break;

}// switch(gphase)

return 1;

}
```


### Team scripts

As all team mates will be almost same (just different equipment and models), create simple include file teammate.inc. Place there just simple data definition for the SC_P_Create using defines (they will be defined later in the main script file). AI will be created with default values. In next time tick just set it to the battle mode and set it's speech distance.


```c
dword gphase = 0;
```


```c
int ScriptMain(s_SC_P_info *info){
s_SC_P_Create pinfo;
s_SC_P_CreateEqp eqp[10];
int eqpcount;


if (info->message!=SC_P_MES_TIME) return FALSE;

if (gphase==0){
CLEAR(pinfo);CLEAR(eqp);
pinfo.type = SC_P_TYPE_AI;
pinfo.side = SC_P_SIDE_US;
pinfo.group = 0;
pinfo.member_id = MEMBERID;
pinfo.inifile = INIFILENAME;
pinfo.name_nr = NAMENUMBER;
pinfo.icon_name = ICONNAME;


pinfo.weap_knife = PKNIFE;
pinfo.weap_pistol = PPISTOL;
pinfo.weap_main1 = 0;
pinfo.weap_main2 = PWEAPON2;
pinfo.weap_slot1= WEAPSLOT1;
pinfo.debrief_group=SC_P_DEBRIEFGROUP_SF;

pinfo.recover_pos = info->pos;
pinfo.flags=SC_P_CREATE_FL_DISABLE_EQPGEN;
equipplayer(eqp,&eqpcount);
pinfo.eqps = eqpcount;
pinfo.eqp=eqp;
info->pl_id = SC_P_Create(&pinfo);

gphase = 1;
}// if (gphase==0)


info->next_exe_time = 0.3f;

if (!SC_P_IsReady(info->pl_id)) return 0;

switch(gphase){
case 1: SC_P_Ai_SetMode(info->pl_id,SC_P_AI_MODE_BATTLE);
SC_P_Ai_EnableShooting(info->pl_id,TRUE);

SC_P_SetSpeachDist(info->pl_id, 20.0f);

gphase = 2;
break;
case 2: break;
}


return 1;

}
```

Now create main script files for all team members - or use already defined in the sdk/scripts/tutorial. Example of definition for the Hornster:


```c
#include <inc\us_equips.inc>


#define MEMBERID SC_P_MEMBERID_MACHINEGUN
#define INIFILENAME "ini\\players\\hornster.ini"
#define NAMENUMBER 2503
#define ICONNAME "hornsterico"

#define PKNIFE 0 //predefined weapons - gotta change !
#define PPISTOL 22
#define PWEAPON1 17
#define PWEAPON2 0
#define WEAPSLOT1 0


void equipplayer(s_SC_P_CreateEqp *eqp, int* count){
Equip_HORNSTER_Full(eqp,count);
}


#include "teammate.inc"
```

Team scripts are finished!


### Enemy Scripts

Esentially all VC will be the same, so once again create very simple include file vc.inc.


```c
#include <inc\sc_global.h>
#include <inc\sc_def.h>

#define GGROUP 0

dword gphase = 0;

int ScriptMain(s_SC_P_info *info){
s_SC_P_Create pinfo;
s_SC_P_CreateEqp eqp[10];


if (info->message!=SC_P_MES_TIME) return FALSE;

info->next_exe_time = 0.2f;

if (gphase==0){

CLEAR(pinfo);pinfo.type = SC_P_TYPE_AI;
pinfo.side = SC_P_SIDE_VC;
pinfo.group = GGROUP;
pinfo.member_id = MEMBERID;
pinfo.inifile = INIFILENAME;
pinfo.name_nr = 2506;
pinfo.icon_name = "nhut";


pinfo.weap_knife = 0;
pinfo.weap_pistol = 0;
pinfo.weap_main1 = PWEAPON1;
pinfo.weap_main2 = PWEAPON2;
pinfo.weap_slot1=PSLOT1;


pinfo.recover_pos = info->pos;
CLEAR(eqp);
pinfo.eqps = 0;
pinfo.eqp=eqp;

pinfo.debrief_group=SC_P_DEBRIEFGROUP_VC;


gphase = 1;
}// if (gphase==0)


if (!SC_P_IsReady(info->pl_id)) {
info->next_exe_time=0.05f;
return 0;
}


switch(gphase){
case 1:

SC_P_Ai_SetMode(info->pl_id,SC_P_AI_MODE_BATTLE);
SC_P_Ai_EnableShooting(info->pl_id,TRUE);
SC_P_SetSpeachDist(info->pl_id,30);
gphase = 2;
break;
case 2: break;

}
return 1;
}
```

Now just create vc0.c, vc1.c, vc2.c:

VC0.C:


```c
#define MEMBERID 0
#define INIFILENAME "ini\\players\\default_aiviet.ini"

#define PWEAPON1 2
#define PWEAPON2 0
#define PSLOT1 0

#include "vc.inc"
```

For other files just change the memberid to 1 and 2.

And the scripts are finished!


### Finishing level

Now just assing all scripts to the player objects... and try to play!
