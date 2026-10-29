# Lot 19 — P10, population de copies et de produits d'expression

29 octobre 2026, demande utilisateur après examen visuel. Priorité : mesurer
la conservation d'une information plus longue avant de corriger T9. Lot de
diagnostic sous lois figées, sans nouvelle protéine ni helper chimique.

## Hypothèse et contre-exemple

L'appariement strict symbole à symbole n'assure pas un rendement global de
chaînes complètes. Tester si les fragments consomment la réserve, si les copies
exactes amplifient, si des séquences différentes apparaissent, et si le brin
initial reste un composant distinct. Ne compter ni les monomères ni les chaînes
préparées comme nouvelles copies. La conservation de ses liaisons est attendue
par construction : le squelette est irréversible dans ce candidat.

Le risque aval est direct : un génome non amplifié ou une expression dominée
par des fragments compromet tout renouvellement. La famille G/F et ses deux
symboles restent fixes. Seuls séquence, stock, taille de boîte et graine changent.
Un échec renseigne cette représentation ; aucune mutation de base par mauvaise
reconnaissance n'est possible dans les lois actuelles.

## Conditions fixées avant les calculs

- Une seule chaîne G `0010110101` (10 symboles, 5 de chaque), pas d'autre chaîne.
- **Copie seule** : 400 dimères G isolés, zéro F ; graines 0/1/2.
- **Expression seule** : 400 dimères F isolés, zéro G libre ; graines 0/1/2.
  Ce second bain teste le produit de traduction directe, pas l'amplification
  d'enzymes fonctionnelles ni leur repliement. Aucun F ne sert de matrice.
- Boîte réfléchissante 24×18, 410 dimères soit 820 billes. Capacité matérielle
  maximale de 40 nouvelles chaînes de 10, avant prise en compte des fragments.
- Témoin de réserve/volume : 800 monomères dans une boîte de surface doublée,
  même concentration nominale, une graine 0 pour chaque mode (1620 billes).
  Ce témoin ne prouve pas à lui seul l'absence d'encombrement et n'est pas une
  cohorte de robustesse ; la dilution des matrices nouvellement créées change.
- Après les pilotes, ajout prospectif de deux témoins de dilution avant la
  campagne principale : 400 monomères, surface doublée, graine 0 de chaque mode.
  Motif : environ 43–45% des supports touchent un cœur d'un autre composant à
  t=50 ; cela ne démontre pas un engorgement mais justifie de tester une densité
  divisée par deux. Transport et densité varient ensemble, sans changer les lois.
- Chimie et paramètres T7 de la démo : T=0,6, dt=0,005, réactions tous les 5 pas,
  cycle externe de période 200 dont 15 de libération, capture des monomères.
  Pas de membrane, de flux continu, de synthèse des dimères ni de dégradation.
- Horizon commun 3200 (16 cycles), dix tâches maximum, deux travailleurs.
  Instantanés de population tous les 10 temps simulés, checkpoints toutes les
  30 secondes réelles. Aucune trajectoire dense ni film enregistré.
- Deux pilotes séparés à 50, copie et expression graine 0, pour mesurer vitesse
  et fonctionnement des diagnostics. Ils sont conservés, sans être ajoutés aux
  résultats à 3200. Leur horizon est insuffisant pour conclure à l'amplification.

## Mesures et limites

Recensement complet par famille, topologie et séquence, identifiée à son inverse
pour les chaînes sans direction. Histogrammes de longueur dérivés du même
recensement. Distinguer total, entièrement détaché, nouveau et matériel initial.
Inclure monomères, fragments conformes à une sous-séquence, fragments autres,
chaînes exactes, chaînes de même longueur différentes, plus longues et cycles.
Vérifier le bilan de toutes les sous-unités à chaque instantané.

Mesurer les stocks libres de chaque symbole, les monomères non appariés, les
contacts de cœur entre composants distincts, la présence de chaque liaison
initiale et l'identité du composant initial. L'audit génétique existant distingue
contacts, gardes locales et ligations éligibles ; les expositions sont des
approximations avant réaction, sans rétroaction et sans hypothèse Poisson.

Rapporter les temps des premières copies observées comme échantillonnés et les
absences comme censurées. Les compteurs « apparus au moins une fois » existants
ne remplacent pas la population simultanément présente. Tous les essais restent
analysés, pas seulement une graine ayant produit des copies.

Comparer les cycles de libération 200,400,…,3200 et les quatre derniers cycles.
Une absence d'augmentation sur cette fenêtre est un plateau **observé**, pas une
preuve d'asymptote. Si moins de 50% des monomères d'un symbole restent libres,
signaler l'épuisement/piégeage et limiter toute conclusion « malgré abondance »
à la période précédente. Ne pas ajouter de matière pendant une trajectoire.
Le témoin doublé aide à interpréter ce cas sans cacher l'essai initial.

## Décision et budget

Mesurer le débit des pilotes après JIT avant de donner une durée réelle. Si
l'estimation dépasse 30 minutes par tâche, déclarer cette durée et conserver
les jalons 800/1600/3200 pour l'analyse progressive. L'horizon n'est pas allongé
selon le succès d'une graine ; pas de grille de réglages ou nouvelle loi dans
ce lot. Sources et recettes figées avant campagne, statut/reprise via les outils
existants. Après la cohorte, interprétation : problème de fragments, changement
de séquence/longueur, limitation d'accès ou fin de réserve. Aucun seuil ne crée
automatiquement une insertase, une polymérase ou une nouvelle règle.

Coût chimique ajouté : zéro. Coût logiciel : observateur passif optionnel de
population et analyse compacte ; conserver son code avec les recettes. Test
d'identité de dynamique/PRNG avec et sans observateur et reprise exacte exigés.
Les démonstrateurs doivent rester chargeables après actualisation explicite de
leurs empreintes de code : cette instrumentation n'en modifie pas les lois.
