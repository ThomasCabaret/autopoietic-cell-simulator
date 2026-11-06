# Lot53 — deux fronts indépendants, fermeture CR1 confirmée

6 novembre2026. [Plan préenregistré](BATCH_53_PLAN.md),
[preuves compactes](BATCH_53_RESULTS.json), [checklist](CELL_CHECKLIST_COMPACT.md).
La question est de réduire deux risques d'intégration pendant la fin CR1,
sans attendre ses résultats pour choisir des paramètres favorables.

## CR1 : trois calculs terminés, porte fixée réussie

| Graine | Cycle simple final | Aire | Présence macro6000–8000 | Premier échantillon macro |
|---|---:|---:|---:|---:|
| 0 | 30 L | 73,01 | 36,75% | 7205 |
| 1 | 52 L | 194,23 | 96,25% | 810 |
| 2 | 34 L | 92,38 | 94,00% | 4810 |

Trois cycles finaux, deux cas satisfaisant la présence tardive>=50% :
le crible CR1 passe, sans changer les seuils, les lois CP1 ou l'horizon8000.
Températures tardives.07972/.07921/.07956 ; ports valides, observation bornée
complète. Le refus individuel de graine0 reste visible. Ces suivis prolongent
les mêmes initialisations sélectionnées de CH1 ; pas trois validations indépendantes.
Les dimères H/T sont fournis isolés, sans liens latéraux préparés. Même loi L
que le candidat intégré, mais bain L seul : ni synthèse alimentaire, ni rétention
continue, ni cellule maintenue. Les refus aux horizons courts restent conservés.

RG1 a été régénéré avec les trois cas complets, sources et entrées figées dans
une nouvelle recette ; l'ancienne lecture à deux cas est conservée. La
[figure](BATCH_52_GEOMETRY.png) décrit une géométrie échantillonnée, pas des
temps de premier passage continus ou des nombres de ruptures chimiques.
Dans la GUI, **Résultats locaux → CP1 · graine1 · terminé** montre le vrai
checkpoint52 ; les deux autres résultats sont aussi disponibles localement.
Les39 presets historiques restent inchangés, sans promotion silencieuse CP1.

## PT1 : transport et rétention, indépendants de l'auto-assemblage

Une enceinte construite est un départ autorisé. Six essais : trois graines
appariées, barrière courante ou ablation transparente,52 L et96 atomes P/R,
soit200 atomes. Les18 dimères préparés donnent une cohorte assemblée de36
atomes ;60 atomes sont libres. Naissances et chimie P/R sont désactivées dans
les deux variantes, sans F, pour garder les cohortes fixes. La seule ablation
entre paires est la portée de barrière. Aucun contour observé ne dirige les forces.

Horizon300, un travailleur, budget2h. Les témoins doivent démontrer des sorties
avant de conclure à une rétention. Contour non classable signifie inconnu,
jamais zéro fuite. Les seuils de température, validité et fractions finales
sont dans le plan ; les traversées échantillonnées complètent ces fractions.
Ce test ne démontre pas l'export ouvert, le transport de toutes les futures
espèces ou une étanchéité permanente. Première paire complète : fractions
finales hors contour des atomes assemblés0/.389 (barrière/témoin), libres.583/.567.
Résultat partiel seulement ; aucun verdict de cohorte avant six cas.

## RF1 : recycler la fonction01 actuelle, pas seulement conserver son nom

Neuf essais : trois graines × pertes nulles / protection occupied / paired_edge.
Le stock et les lois génétiques sont ceux du candidat courant, séquence01,
150 atomes, dans un sous-bain P/R12×9 sans membrane. Les quatre G01, un F01 et
quatre monomères F préparés ne sont pas comptés comme fabrication émergente.
Les deux protections réemploient les pertes RV1 existantes : deux transitions,
quatre taux et un facteur déclarés. Aucun nouvel atome, lien, outil ou gène ;
ce helper n'est pas adopté dans CP1 et son énergie reste non fermée.

Horizon1200, un travailleur, budget2h ; six cycles externes fixés. Mesurer
séparément G01 exact, F01 exact, motifs F0–F1 non appariés même dans une chaîne
plus longue, catalyse tardive900–1200, réassemblage et réincorporation matérielle.
Chaque protection a une porte séparée ; aucun vainqueur ou transfert automatique.
Le refus RP1 sur001 est conservé. Perdre une chaîne cible n'établit pas à lui
seul l'extinction de toute fonction ; inversement, posséder un motif n'établit
pas son flux utile. Premier témoin sans pertes :13 G01/13 F01, mais catalyse
tardive nulle et seulement1 P/1 R libres à la fin. Il signale déjà une limite
possible d'exposition au substrat tardif, pas une extinction des outils.
Ne pas modifier le stock ou la fenêtre après lecture pour sauver la porte.

## Traçabilité, arrêt et prochain jalon

Recettes sources figées : [PT1](BATCH_53_PT1_RECIPES.json) et
[RF1](BATCH_53_RF1_RECIPES.json). Les campagnes se terminent par un rapport,
sans réglage, relance ni transfert automatique. Les sorties brutes et checkpoints
restent locaux, ignorés par Git. Statut : `selective_transport_status.bat` et
`functional_recycling_status.bat`. Chaque campagne est limitée à un travailleur
et deux heures ; CR1 est terminé, donc deux travailleurs scientifiques au plus.

Prévol : états appariés PT1, cohortes stables, témoin RF1 sans perte exactement
égal au moteur de référence, portes et lecture de vrais checkpoints courts.
Un oubli de factory d'observateur dans le premier micro-test PT1 a été corrigé
avant gel/lancement ; échec local conservé. Cinq tests ciblés puis **295 tests**
passent. Aucun fichier du simulateur ni preset GUI modifié dans ce lot.

Prochain choix après ces deux lectures : transférer le recyclage seulement si
la fonction utile persiste et si les mesures sont exposées ; sinon isoler
épuisement du stock, protection excessive ou perte d'information. Pour PT1,
une absence de sortie témoin ou une frontière inconnue appelle un diagnostic
d'exposition, pas une conclusion d'étanchéité. Ne pas lancer une cellule complète
pour contourner ces critères ni ajouter une protéine sans accord utilisateur.

Santé : progrès réel sur un verrou mécanique sans enrichir les lois. Restent
diversité fonctionnelle, information fiable, régulation/protection et flux/export.
M-01 reste au palier50 (sous-système), M-04 à75 pour EG1 limité historique,
maintien0. Pas de hausse anticipée pour PT1/RF1 ni de pourcentage global.
