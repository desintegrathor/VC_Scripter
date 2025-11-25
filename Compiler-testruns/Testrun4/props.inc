// Propriétés du bot 
// Modifiable

// une valeur "float" cad à virgule doit être suivie d'un "f"

// frnd() est une fonction de random pour optenir un nombre aléatoire en 0 et le paramètre envoyé
// exemple : 0.1f + frnd(0.1f)
// cette fonction ne peut être utilisé dans les #define, vous devez les implanter dans le bot.inc

#define B_PVANGLE		3				// angle de vision du bot 				(en radian)
#define B_PVANGLENEAR	4				// 			"			  de près

#define B_BERSERK		0.1f			// % de chance que le bot attaque sans couverture : 0 jamais, 1 toujours
#define B_BERSERK_A		0.1f			// partie aléatoire

#define B_SCOUT			0.2f			// le bot avance-t-il vers l'ennemis : 0 jamais, 1 toujours		
#define B_SCOUT_A		0.5f			// partie aléatoire
										// Un Sniper n'est pas SCOUT par exemple !

#define B_MAXVISU		100				// Distance à laquelle un bot peut voir (en mètres)
#define B_HEARPREC		2.5f			// Qualité d'écoute du bot : 0 tout, 1 beaucoup, 4 sourd comme un pot
#define B_HEARDIST		50				// Distance max à laquelle un bot peu entendre
#define B_RUN			0.8f			// Lorsque le bot voie un ennemis : 0 marche, 1 cours, 0.5 50/50
#define B_PHASE			0.5f			// 		" pour debout/accroupi
