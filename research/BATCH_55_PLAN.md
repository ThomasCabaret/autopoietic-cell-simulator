# Lot55 — reprise Astra et tranche de transport ouverte

Type : construction technique et contrôle de transfert, pas réglage chimique.
Hypothèse OB1 : le moteur commun peut recevoir/absorber des précurseurs sans
nombre fixe, avec IDs stables, apport indépendant des concentrations, bilan
par espèce et reprise exacte. Cela débloque les essais alimentés ultérieurs.

Contrat : carré2D, Langevin BAOAB existant, mêmes masse/amortissement/T ; aucun
mur réfléchissant. Absorption à la première mise à jour du bord observant un
centre hors du domaine. Sources Poisson stationnaires par longueur de bord ;
arrivées datées sur une horloge externe indépendante, injection à une profondeur
fixe et vitesses du bain. Le retard d'application est borné par la cadence de
réaction. Pas de concentration imposée ni de consommateur adaptatif.

Portée : précurseurs non liés seulement. Pas de membrane, G/F, réaction ou
nouveau catalyseur ; aucun transfert biologique acquis. Export de molécules
liées et migration des tableaux P/R restent à faire. Les lois CP1 sont inchangées.

Contrôles décisifs : bilan exact par type après entrées/sorties ; IDs jamais
recyclés ; survie des positions/vitesses des particules conservées au changement
de tableau ; bain vide ; arrêt sur plafond (jamais écrêtage régulateur) ; reprise
exacte et observation passive ; références fermées inchangées. La même horloge
source doit donner le même apport daté si dt ou cadence d'observation change.

Après microcontrôles, six essais bornés :3 graines ×dt.004/.002, intervalle de
bord.02 commun, horizon80, boîte8×6, deux précurseurs, débit.1 par longueur/type,
profondeur.3, T.08/gamma.1/m1, sans exclusion. Ce crible vérifie transport réel
et coût ; pas d'équilibre asymptotique ou de convergence certifiée sur3 graines.
Une comparaison de cadence du bord peut suivre seulement si son biais domine.
Sources/recettes gelées ; aucun essai biologique long ou réglage automatique.

Fonction aval menacée : homéostasie sous apport, export et remplacement. Ce qui
reste réutilisable si la chimie échoue : protocole de population, source/puits,
bilans et benchmark du transport. Arrêt pour interprétation à la fin du lot.
