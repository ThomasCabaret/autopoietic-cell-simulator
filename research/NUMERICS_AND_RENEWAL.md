# Bruit, discrétisation et coût du renouvellement — 27 octobre2026

Réponse technique et ordre de grandeur, pas une nouvelle campagne chimique.
Les données brutes restent sous outputs/performance et outputs/campaigns.

## Ce que le moteur intègre

`reference.integrate` calcule, pour chaque bille et coordonnée :

`dx = mobilité × force × dt + sqrt(2 × mobilité × température × dt) × N(0,1)`.

Il n'y a pas de vitesse inertielle ni de solvant explicite. Le bruit et la
mobilité représentent un bain implicite ; une bille isolée diffuse sans collision
avec une autre bille simulée. Les atomes d'un composé reçoivent chacun ce bruit,
et les contraintes de leurs liens font émerger la dynamique du composé.
Température sans unité calibrée, pas une température en kelvins. Les helpers
activés/cycles externes empêchent de revendiquer un équilibre thermodynamique.

Le pas courant de J0 est0,002 ; les réactions sont actualisées tous les5 pas
(intervalle0,01). Leurs probabilités utilisent `1-exp(-taux×intervalle)` mais
cela n'élimine ni les erreurs d'intégration des positions ni les effets des
contacts manqués ou des transitions concurrentes dans cet intervalle.

Les tests existants vérifient forces, invariance arbre/brut, reprise et absence
de rétroaction de l'observation. **Aucune convergence chimique en dt n'est encore
démontrée.** Une trajectoire stable/reproductible n'est pas une telle preuve.
Voir le protocole ajouté à KINETICS_AND_PERFORMANCE.md avant toute accélération
par augmentation du pas. Les paramètres physiques doivent être testés à part.

## Charge cellulaire conditionnelle

Le budget C0B reste une hypothèse de longueurs/fonctions, pas un inventaire
validé dans J0. Petite cellule1020 billes avec environnement ; nominale2150
dans la cellule +256 dehors =2406 ; variante plus grande6292. J0 actuel588.
Les trois outils différents, leurs longueurs, leur renouvellement et la
fabrication de L par F ne sont pas encore réalisés ; le budget peut changer.

## Nouveau benchmark complet

Commande : `python experiments/benchmark_cell_workload.py`.
Un travailleur, sans rendu ni checkpoints disque pendant les chronos, observateurs
actifs, pas0,002,50 pas d'échauffement puis3 blocs de250. Forces, voisinages,
réactions, intégration et observations compris. Source figée et configurations
résolues dans `outputs/performance/cell_workload_20261027T115831264333Z`.

| Charge | Billes | Pas/s médian | Unités simulées/s réelle | Minutes pour1000 unités |
| --- | ---: | ---: | ---: | ---: |
| J0 actuel | 588 | 708 | 1,416 | 11,8 |
| Petite synthétique | 1020 | 705 | 1,411 | 11,8 |
| Nominale synthétique | 2406 | 315 | 0,629 | 26,5 |
| Grande synthétique | 6292 | 122 | 0,245 | 68,1 |

Les charges synthétiques contiennent des polymères préparés de12/24/48 unités,
des gènes et outils répétés et des précurseurs. Les séquences répétées ne sont
pas trois synthétases distinctes. Certains composants sont initialement hors
de la membrane ; densité, activité tardive et alimentation ne sont pas optimisées.
Ces segments courts sont des mesures de coût, pas une trajectoire stationnaire
de cellule complète, un optimum de concentration ou une preuve de viabilité.
Les valeurs ne sont pas une loi de coût linéaire en N.

Contrôle long réel : J0 avec588 billes a simulé400 unités en333,45/320,52/302,70s,
soit5,0–5,6min par essai avec deux travailleurs concurrents, checkpoints et analyse.
C'est cohérent en ordre de grandeur avec le benchmark court. L'affichage est
découplé et peut sauter des images ; son surcoût effectif n'a pas été mesuré ici.

## Grandeur cible et estimation conditionnelle

Mesurer le **temps réel de demi-renouvellement fonctionnel par famille** :
membrane, chacun des gènes, chacun des outils et stocks indispensables. Suivre
l'origine alimentaire et l'incorporation réelle ; ne compter ni produits libres
inutilisés, ni répétitions d'une même opération, ni simple dilution/croissance
comme remplacement. Maintenir l'inventaire/fonctionnalité et relever les pertes
des constituants initiaux. Une moyenne par bille serait dominée par la membrane
et pourrait masquer l'absence de renouvellement d'un outil indispensable.

Pour un apport externe fixé `c`, on cherche à minimiser le temps humain mesuré
`T50(c)` sous ces conditions de fonctionnement, pas seulement le temps simulé
ou le coût par pas. En ordre de grandeur `T50 ≈ tau50_sim / vitesse_sim`.
Balayer séparément débit/concentration, suivre la taille réelle du bain, les
déchets, séquestrations et stocks. Plus de nourriture peut aider, saturer ou
inhiber. Aucun optimum n'a encore été mesuré.

À2406 billes, **si** un demi-renouvellement demandait1000–10000 unités simulées,
le coût actuel serait environ27min–4h25, hors rendu. À6292 :1h08–11h21.
Le choix1000–10000 est un scénario de capacité de calcul, pas une mesure ni une
borne du demi-renouvellement. Aucun mécanisme actuel ne renouvelle toutes les
familles, notamment L : le T50 global n'est pas encore atteint/définissable
expérimentalement. La durée réelle pourrait dépasser ces scénarios.

## Premier constat thermique issu des essais J0 terminés

12/12 tâches achevées à400, sources figées vérifiées. Dans la petite boîte
native,0,6 donne un F détaché sur chacune des trois graines, dimères catalysés
1/1/18 ;0,08 donne0/0/0 F et0/0/0 dimère catalysé. Aucun composant catalysé
n'est incorporé dans ces essais à400. Le bain avec L à0,08 donne aussi0 F.
Les P/R libres ont des contacts avec L sur les trois graines et155/138/177
changements de côté échantillonnés ; aucun passage lié observé, avec exposition
liée nulle dans une graine et périodes inconnues présentes. Ni flux net ni
étanchéité générale n'en découlent.

C'est une sensibilité au bain **sur cet horizon**, pas une impossibilité à froid.
Diffusion ralentie, occupation trop longue et géométrie inéligible restent à
distinguer avant réglage ou allongement. Le renouvellement intégré reste absent.
