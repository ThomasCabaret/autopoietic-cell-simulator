# Lot25 — MD2, un même motif de ports pour contact libre et lié

Suite autorisée après MD1. Lot de mécanisme local puis transfert, sans protéine.
Langevin0,1,m1 conservé ; pas de baisse du bruit pour cacher la fragilité.

## Hypothèse et choix minimal

Le contact lié ancien maintient deux distances et quatre angles faibles, alors
que sa recapture libre exige deux ports H/T coïncidents. MD1 a montré un lien
presque au repos mais non recapturable. MD2 remplace ces distances/angles latéraux
par une continuation harmonique de la géométrie de ports déjà utilisée librement.
Les ressorts internes des dimères restent identiques.

Pour q=|portH_j-portH_i|²+|portT_j-portT_i|² :
U_libre=-epsilon[exp(-q/(2w²))-exp(-8)(9-q/(2w²))].
U_lié=-epsilon(1-9exp(-8))+epsilon(1-exp(-8))*q/(2w²).
Même valeur et même dérivée en q=0, même géométrie locale à quatre billes.
Force par Jacobien exact des ports. Aucune raideur indépendante ajoutée :
k=epsilon(1-exp(-8))/w². Deux ressorts latéraux/quatre angles supprimés par lien
dans ce candidat ; pas de double renforcement caché. Liaisons explicites seulement.

Option chimique bornée `bound_port_geometry=true`, absente par défaut pour
préserver les scénarios historiques. Zéro type, état, port, gène, outil ou
particule ajouté. Un choix de potentiel lié, réutilisant long/short/epsilon/w.
La réutilisation est testée sur petites membranes et grand bain ; pas une
preuve de généralité pour toutes les machines moléculaires.

Réactions, seuils, dissociation aléatoire0,02 du grand bain et échange0,2
inchangés. Les changements d'état peuvent encore changer l'énergie hors q=0 ;
aucune conservation thermochimique complète ni detailed balance revendiquée.
Température cinétique et stabilité à surveiller, pas de rescaling/clipping.

## Étape locale et porte automatique bornée

Vérifier gradient, force résultante et couple, continuité au contact idéal,
suppression des anciens termes et absence d'effet quand l'option est absente.
Trois graines0/1/2, paire de dimères initialement liée et alignée, ancien/nouveau
potentiel, T0,08,dt0,002,Langevin. Dissociation aléatoire désactivée **seulement
dans ce banc local** pour isoler la géométrie ; rupture par étirement conservée.
À10, couper le seul lien à heure fixe, perturbation externe déclarée identique
pour les deux candidats ; suivre la recapture jusqu'à12. Pas de déclencheur
piloté par un score, contour ou observation. Le nouveau lien doit rester libre
de se rompre et se reformer, pas devenir irréversible.

Porte fixée avant résultat : fraction d'échantillons liés compatibles avec
la capture>=90% pendant6–10 pour chacune des trois graines nouvelles, lien
encore présent juste avant la coupure, recapture en<=2 pour au moins2/3, aucune
instabilité numérique. Mesurer les anciennes références sans exiger leur échec.
Si échec, arrêter pour interprétation, pas de balayage automatique de raideurs.
Si réussite, préparer puis lancer la cohorte figée ci-dessous sans intervention
manuelle pour appliquer le seuil. Sources/rapports locaux conservés.

## Transfert figé,15 tâches au plus

- Petites V8 depuis36 dimères isolés, mêmes lois/conditions que LT2 sauf
  potentiel lié : trois graines nouvelles à1000, deux témoins anciens graines1/2.
  Témoin ancien graine0 LT2 réutilisé explicitement, pas nouvelle répétition.
- Grande membrane avec24 molécules libres internes et sondes retenues/perméables
  (24 chacune), même géométrie/lois L que J3 : ancien/nouveau sur graines0/1/2,
  horizon1200, six tâches. Ces bains L+sondes ne sont pas un circuit génétique.
- J3 intégré : nouveau potentiel sur trois graines à1200, plus graine0 au pas
  mécanique divisé par2, mêmes intervalles de réaction/observation, quatre tâches.
  Références anciennes LT2 réutilisées et identifiées, pas recalculées.

Total15, deux travailleurs, checkpoints30s, pas de trajectoires denses. Ordre :
V8, sondes, J3. Un seul candidat mécanique, mêmes parameters quelle que soit
la fonction ; différences thermiques/géométriques héritées de V8/J3 déclarées.
La porte locale ne sélectionne pas des graines favorables de la cohorte longue.

## Lecture et arrêt

Mesurer assemblage depuis molécules libres, fraction fermée sur grille régulière,
insertion réellement persistante, passages/étanchéité seulement quand classables,
activité et usage aval d'un F exprimé dans J3. Lire température et coût réel.
Un anneau préparé intact seul n'est pas un succès de transfert. Comparer les
contrôles fins sans conclure à la convergence sur une graine. Aucun ajustement
spécifique par fonction ni adoption globale automatique du candidat.

Une rigidification empêchant assemblage/croissance/insertion est un contre-exemple
qui oblige à interpréter le motif. Après cette cohorte, décision mécanique puis
retour T9 si transfert ; sinon reconsidérer la représentation après le second
changement conceptuel sans progrès. N'ajouter aucun outil fonctionnel sans
proposition et accord utilisateur. Les recettes/data anciennes sont préservées.
