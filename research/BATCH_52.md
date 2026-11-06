# Lot52 — premières enceintes CP1 et inspection des calculs longs

6 novembre2026. [Plan](BATCH_52_PLAN.md), [chronologie descriptive RG1](BATCH_52_GEOMETRY.json),
[figure](BATCH_52_GEOMETRY.png), [preuves compactes](BATCH_52_RESULTS.json).
L'utilisateur accepte l'inventaire CA1 comme coût de départ. Aucune loi,
constante, particule ou machine moléculaire ajoutée dans ce lot.

## Deux cas CR1 achevés, cohorte encore ouverte à cette lecture

| Cas8000 | Contour simple final | Aire | Fraction macro6000–8000 | Premier échantillon macro |
|---|---:|---:|---:|---:|
| graine0 | 30 L | 73,01 | .3675 | 7205 |
| graine1 | 52 L | 194,23 | .9625 | 810 |

Ports finaux valides, températures tardives.07972/.07921. Les deux enceintes
proviennent de dimères H/T isolés, sans liaison latérale préparée ni loi changée
depuis CP1. Le contour30 montre aussi que le résultat n'est pas une longueur
cible52 dictée par le moteur. Les52 dimères fournis bornent le stock disponible.
Même loi L du candidat intégré, mais bain réduit sans génétique ni autres
substrats : preuve de sous-système sous lois communes, pas cellule maintenue.

Graine0 ne passe pas la condition de présence tardive>=.5 ; graine1 la passe.
Le verdict2/3 reste indéterminé avant la fin de graine2. Aucun seuil relaxé,
horizon prolongé ou nouveau calcul lancé sur ces deux résultats sélectionnés.
Les refus CC1/CH1 aux horizons courts restent conservés.

RG1 exploite seulement les cas complets avec provenance vérifiée. Sur0–8000,
fractions macro observées.091875/.756875 et13/60 épisodes échantillonnés.
Leur nombre n'est pas un compteur de ruptures chimiques : il peut aussi refléter
une géométrie non simple ou les seuils de mesure. Les cycles entre deux
échantillons peuvent être manqués. Le témoin précoce810 puis l'état ouvert à1800
en graine1 illustrent pourquoi une image finale ne mesure pas le premier passage
ni la permanence. Les occasions de capture sont elles aussi échantillonnées,
pas une intensité exacte de réaction. Pas de causalité complète déduite.

## Construction : rouvrir et examiner un vrai résultat dans la GUI

Le client propose **Fichier → Ouvrir un checkpoint local…** et un menu
**Résultats locaux** qui résout les états CR1 présents sur la machine. Choisir
**CP1 · graine1 · terminé** pour voir l'enceinte52. Zoom, filtres, sélection,
suivi et export PNG existants restent disponibles ; la fiche précise qu'il
s'agit du sous-système L avec molécules fournies, sans maintien cellulaire.

L'import lit une fois le fichier source, vérifie version/empreintes du moteur
et configuration de la tâche, puis conserve une copie dans les sorties locales.
Les remplacements atomiques du checkpoint par la campagne ne modifient pas
cette copie. **Recommencer** revient au même état importé, jamais à un nouveau
checkpoint ou au départ t0. La source et les sorties scientifiques ne sont
pas réécrites. Une provenance d'import et les métadonnées des PNG sont conservées.
Un moteur incompatible est refusé ; aucun code d'archive n'est exécuté.

L'état apparaît en pause, à son vrai pas, sans flashes rétrospectifs inventés.
Un checkpoint final a atteint son horizon et n'a donc pas de lecture future
à dérouler. Les checkpoints partiels peuvent continuer jusqu'à leur horizon,
avec positions, vitesses, liaisons, PRNG et observateur principal exacts.
Ce n'est pas une relecture de trajectoire : les audits auxiliaires du protocole
de campagne ne sont pas automatiquement prolongés dans cette session visuelle.
Le scénario/version du moteur restent fixés, le rythme de présentation seul varie.

Le dépôt contient les références aux calculs, pas leurs checkpoints. Sans données
locales, le menu l'indique ; les39 presets historiques restent disponibles
depuis leurs états initiaux. Pas de promotion silencieuse du raccourci EG1.

## Vérification et santé

290 tests passent, dont les nouveaux tests de snapshot, refus de version/tâche,
original préservé et continuation exacte depuis un checkpoint malgré remplacement
de la source. Contrôle natif Qt/OpenGL : action fichier, pause au pas7,
recommencement depuis copie figée, continuation égale au headless et ouverture
des deux vrais checkpoints CR1 terminés. Les39 actions de démo sont vérifiées
nativement, lecture/pause/restart et états courts égaux au moteur pour les cas
de référence. Les instantanés ont été inspectés visuellement.

Avancement utile : une incertitude de fermeture diminue sous les mêmes lois,
et l'interface permet désormais d'inspecter directement la preuve locale.
La présence intermittente et la graine tardive interdisent de déclarer une
membrane robuste ou une étanchéité continue. Le candidat reste à éprouver en
bain mixte et sous perturbations. Diversité, information, protection/régulation
et flux/export restent conceptuellement ouverts. Le coût CA1 ne change pas.

Aucun palier biologique augmenté à cette lecture : M-01 reste50, preuve
séparée désormais aussi visible sous CP1 ; M-04 conserve75 EG1 limité,
maintien0. Prochain jalon : troisième résultat et porte CR1 figée, puis choix
de transfert/diagnostic selon le refus éventuel. Aucun nouveau réglage à l'aveugle.
Statut vivant : `competitive_relaxation_status.bat`.
