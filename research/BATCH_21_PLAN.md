# Lot 21 — MIX2, inertie et coût réel du mélange

29 octobre 2026, autorisation utilisateur de comparer les variantes proposées.
Priorité au compromis simplicité/coût/rencontres, pas à la seule vitesse
apparente ou au nombre de temps simulés. Suivre DESIGN_PRINCIPLES.md,
LOCALITY_AUDIT.md, KINETICS_AND_PERFORMANCE.md et AUTOMATED_EXPLORATION.md.
Ne changer aucune campagne déjà figée ni les lois des démonstrateurs.

## Variantes locales et coût

Le scheduler reste Simulation.advance. Le chemin brownien historique est gardé
sans nouveau tirage de PRNG. Les variantes inertielles sont limitées au hook
mixing non réactif ; un transfert à la chimie exigerait une étape distincte.

- **Langevin BAOAB** : vitesse par bille, masse1, forces conservatrices existantes,
  amortissement gamma et bruit OU équilibré à T. Un calcul de force par pas après
  initialisation, force conservatrice mise en cache (liens fixes uniquement).
- **DPD** : mêmes vitesses/masses et forces, thermostat radial de paires proches,
  cutoff1. Pour une paire de même masse, u relatif devient a*u+bruit, avec
  a=exp(-2*gamma*w²*h/m) et variance=(2*T/m)*(1-a²), w=1-r/cutoff.
  Les impulsions sont opposées. Deux demi-passes OU, ordre déterministe direct
  puis inverse, autour d'un pas velocity-Verlet. Une force conservatrice/pas,
  deux recherches de voisins et deux passages locaux de thermostat.
  Boucle compilée Numba ; pas de parcours de toutes les paires.

Aucun mouvement d'un agrégat identifié globalement, réinitialisation de vitesse,
recentrage ou rééchelonnement global de température. Les ressorts transmettent
les forces, le thermostat par paires conserve leur quantité de mouvement locale.
Le bruit/thermostat sont une aide physique déclarée, sans gène supplémentaire.
Coût de modèle : deux composantes de vitesse par bille, masse, amortissement ;
DPD ajoute un rayon et des interactions O(paires proches). Mesurer ce coût.

Références de définition : [Langevin](https://docs.lammps.org/fix_langevin.html),
[DPD](https://docs.lammps.org/pair_dpd.html). L'implémentation est locale au dépôt,
sans copie de LAMMPS. Les tests couvrent OU relatif, réciprocité, vol libre,
stabilité, passivité et reprise incluant vitesses/forces/PRNG.

## Départ et critères figés

200 dimères, boîte24×18, moitié gauche. Départ commun **sans chevauchement de
cœurs répulsifs**, pour éviter un faux gain inertiel dû à la détente d'une
compression préparée. Géométrie identique entre modèles d'une même graine ;
vitesses Maxwell identiques entre variantes inertielles. Le nouveau témoin
brownien est recalculé sous ces conditions. MIX1 reste une référence différente,
pas un contrôle parfaitement apparié. Les billes restent localisées ; pas de chimie.

Observations de contacts0,05 et statistiques2,5 pour tous ; mêmes rayons/grille,
MI, voisinage et conditions que MIX1. dt0,005, avec témoins dt0,01 déclarés.
Les D estimés sur courts incréments ne sont pas des D asymptotiques inertiels.

Après lecture des pilotes, avant les longs essais : l'occupation DPD peut
traverser la valeur uniforme puis dépasser0,6 alors que la mémoire spatiale
reste élevée. Ajouter prospectivement un indicateur conjoint : tous les seuils
occupation/voisins/MI/50% partenaires simultanément pendant cinq instantanés.
Conserver aussi chaque mesure séparée. Cela distingue passage d'un front et
mélange des identités ; pas de seuil révisé sur la campagne longue.

Pilotes figés : sept essais à100, graine0, brownien ; Langevin gamma4/0,1 ;
DPD gamma0,5/2 ; variantes rapides dt0,01. Conserver erreurs ou échecs.
Ils mesurent débit, température, état des ressorts et premiers seuils locaux.

Campagne principale bornée,18 essais maximum, deux travailleurs :

1. Froid T0,08 : brownien, Langevin gamma0,1 et DPD gamma0,5, graines0/1/2.
2. Témoin Langevin gamma4, graine0 : même D libre asymptotique que le brownien.
3. DPD gamma2, graines0/1/2 : sensibilité au thermostat, sans sélectionner une
   seule graine favorable.
4. dt0,01 pour Langevin0,1/DPD0,5, graine0 : contrôle de coût/numérique, pas une
   convergence générale validée sur cette seule paire.
5. T0,6, graine0 : brownien/Langevin0,1/DPD0,5, contrôle de compatibilité thermique.

Horizons12000 pour les témoins froids brownien et Langevin4 ;1600 pour les autres.
Ces horizons inégaux sont explicites : toutes les absences restent censurées,
aucune moyenne de temps de réussite en excluant les non-réussites. Préfixes
communs comparables ; pas d'extension automatique d'une graine sélectionnée.

## Rendement réel, décisions automatiques et limites

Enregistrer une horloge de calcul réelle par segment de250 pas, observations
comprises, sans coût des checkpoints. Rapporter aussi le temps total du travailleur.
Pour chaque seuil, donner une fourchette entre segments réels voisins, avec et
sans les premières2,5 unités simulées d'échauffement déclaré. Les seuils sont
échantillonnés à2,5 ; leur résolution physique limite aussi la précision.
Pas de conversion naïve par un débit unique sur une trajectoire entière.

Critères : seuils d'occupation, mémoire et voisins de MIX1, plus moyenne de50%
des199 autres molécules rencontrées au rayon0,3. Rapporter temps-paire et durées,
pas seulement contacts très brefs. Comparer paires traitées/pas, évaluations de
forces/pas, pas/s et déplacements par pas. Un gain de mélange doit survivre au
coût supplémentaire et au pas numérique requis. Pas de promesse d'optimum global.

Contrôle thermique descriptif après20 : min/max du T cinétique, signaler toute
sortie de[0,5T;2T]. Ce contrôle ne pilote pas le thermostat. Mesurer extension des
liens et max déplacement ; ne jamais écrêter un saut instable pour sauver un essai.
Un candidat rapide mais chaud, instable ou détruisant les structures ne gagne pas.

Le contrôleur déroule la grille bornée et génère son rapport sans intervention
manuelle par seuil. Le choix de physique reste à interpréter. Aucun nouveau
thermostat appliqué à la cellule pendant le lot. Prochain test aval après choix :
capture/orientation/ligation puis membrane sous ces lois, avant toute adoption.
Une rencontre géométrique n'est pas un produit chimique fonctionnel.

Campagnes et pointeur séparés sous outputs/motion_campaigns, checkpoints30s,
sources figées. Deux travailleurs nouveaux au maximum ; tenir compte des autres
jobs dans l'interprétation des temps réels. Pas de trajectoires denses ou vidéo.
