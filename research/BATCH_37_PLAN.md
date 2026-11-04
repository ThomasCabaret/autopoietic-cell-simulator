# Lot37 — L2 : contacts compatibles et formation à coût mécanique local

4 novembre2026. Exploration indépendante de MIN1M, qui garde ses sources figées.
Objectif : comparer deux corrections ciblées du saut de potentiel L1, sans
changer thermostat, vitesse, positions lors d'une réaction ou ajouter un outil.

## Changements bornés

1. Contacts compatibles : répulsion F/H–T identique avant/après naissance (zéro
   dans ce pool), plutôt qu'un passage0→0,55 au milieu des sites de capture.
   La superposition sélective est une liberté du projet. Cela ne prouve aucune
   rétention future des F : la barrière des segments membranaires devra être
   conservée/testée séparément lors du transfert ; aucune étanchéité L2 acquise.
2. Porte énergétique locale : calculer les seuls termes de potentiel modifiés
   par la naissance H–T et la libération des deux sites. Taux multiplié par
   exp(−max(ΔU,0)/T). Les positions et vitesses restent continues, les mouvements
   et la température de consigne0,08 restent inchangés. Ce n'est pas un bilan
   thermodynamique complet : réaction irréversible et captures/ports encore
   cinétiques, aucun fuel explicite ni équilibre détaillé garanti.

Calcul fini : cores des deux atomes à portée≤max(core), capture aux voisins
des deux ligands/sites libérés à≤3largeur, ressort axial à deux atomes, ports
du nouveau H–T aux seuls H–T dans1+4largeur. Aucun potentiel total du bain,
contour, identité d'agrégat, gène ou observateur ne décide. Indexation des liens
pour calcul vectoriel permise, chaque terme demeure local. Le voisinage spatial
peut contenir plusieurs particules : ne pas le prétendre limité à six billes.

Coût : option de loi énergétique, un coefficient de contact F/L déjà existant
mis à zéro dans la branche compatible ; zéro nouvel élément, port, état physique,
outil/gène ou valeur de taux. Compteurs d'exposition passifs seulement. ΔU calculé
depuis les mêmes potentiels que les forces, contrôlé contre leur variation exacte.
Les énergies cinétiques mesurées ne sont pas supposées égales à la consigne.

## Campagne prospective finie

Trois graines0/1/2, horizon100, mêmes64 atomes pour les quatre branches :
référence L1, porte seule, contact seul, combinaison. Ajouter à la combinaison
les témoins split, no_boost et no_tool. Split/no_boost gardent positions et PRNG
initial, no_tool retire16 billes F et a ses propres tirages ; pas de comparaison
de trajectoires appariées avec ce dernier. Réutiliser L1 référence0, recette
L1P_20261104T115550305191Z, au lieu de la refaire : **20 nouveaux essais maximum**.
Le rejeu de préfixe actuel/référence ancienne doit être exact avant ce réemploi.

Un travailleur en plus des deux MIN1M, checkpoints30s, plafond1h avant pause.
Sources, scénarios, critères et analyse figés avant calcul. Pas de grille de taux,
retry, deuxième phase ou promotion automatique. Rapport automatique puis arrêt.

Crible descriptif combiné : ≥4 L et≥2 produits par paire de sites dans≥2 graines,
≥1 contact latéral dans≥2 graines ; médiane L supérieure aux trois médianes des
témoins ; pas d'attribution catalytique dans no_tool/split. Pour les trois graines,
moyenne cinétique du dernier quart entre0,04 et0,12,95e percentile après5≤0,24.
Ces seuils sont des alarmes de transfert, pas une preuve d'isothermie ou viabilité.
No_boost peut garder une attribution de sites liés : tester son débit sans
assimiler cette étiquette à une accélération. Absence d'événement censurée à100.

Si la porte seule tue les naissances, vérifier les expositions pondérées avant
prolongation. Si seule la suppression de contact suffit, préférer sa simplicité
à la porte. Si la chaleur demeure malgré baisse du saut, diagnostiquer les
autres transitions (capture/ports) avant nouveau taux. Puis compétition P/R/H/T,
expression et insertion réelle ; aucune fonction de cellule complète déduite.
