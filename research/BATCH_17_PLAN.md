# Lot17 N1 — contrôle numérique du bain intégré

28 octobre2026. Validation de l'intégration, aucune exploration d'une nouvelle
loi. J3 démontre du transfert utile mais peu de chaînes complètes. La stabilité
numérique est un prérequis pour modifier la capture/finition T9 sur ces résultats.
Capacité aval menacée : copie/expression/transport dans une cellule renouvelée.
Contre-exemple le moins coûteux à ce stade : mêmes bains construits, temps plus
fin ; pas de portage GPU ou mécanisme supplémentaire avant cette vérification.

## Protocole figé avant les nouveaux résultats

Réutiliser les trois J3 K16 avec L, graines0/1/2 à1200, dt0,002. Ne pas les
compter comme nouvelles réplications. Six nouvelles tâches : dt0,001 puis
0,0005 sur les mêmes graines à1200.2118 billes, mêmes lois résolues, positions,
liaisons, PRNG initiaux, T0,08, cycle externe200/15, énergie/aides identiques.
Les pas de bruit suivent déjà sqrt(dt). Les trajectoires de même graine ne
partagent pas un chemin brownien : comparer cohortes, pas différences appariées
comme si elles étaient des mesures communes. Aucun changement d'alphabet,
primitive, état, paramètre chimique, gène, outil ou interaction.

Cadence réaction existante5dt :0,01/0,005/0,0025. C'est un raffinement temporel
**conjoint mécanique/réactions**, pas une identification de leur effet séparé.
Observation primaire0,5 à chaque niveau, fenêtre cinétique25, audit génétique,
checkpoints60s, deux travailleurs et aucune trajectoire dense. Les expositions
pré-réaction restent approximatives et changent de résolution avec le tick.
La cadence de réaction indépendante demandera un contrôle séparé si nécessaire.

Conserver la référence J3 et vérifier que les modules physiques/réactifs de la
recette N1 ont exactement les mêmes hashes. Un rejeu court de la référence doit
également préserver positions, PRNG et états. Pas de correction silencieuse
des anciennes sources ni de prolongation de graines sélectionnées.

## Lecture et décision préannoncées

Relever catalyse par outil initial, produits incorporés par gène initial,
G/F libérés et entièrement construits, activité utile des F exprimés, occasions
génétiques, stocks/fragments, contacts/passages et fractions de membrane sur
grille régulière. Le rapport automatique conserve chaque graine et indique
la provenance des témoins réutilisés.

Alertes descriptives sur médianes entre niveaux successifs : catalyse par outil
ou incorporation par gène varie de plus de30% (zéro/non-zéro signalé) ; fermeture
varie de plus de0,10 ou enveloppe classable de plus de0,05 en valeur absolue.
Ces seuils sont un triage annoncé après connaissance de J3, avant N1 ; ni test
statistique ni certificat de convergence. Trois graines et rares G/F complets
ne suffiront pas à garantir leur convergence, même sans alerte de médiane.
Une erreur mécanique, masse incohérente ou incompatibilité de sources invalide
le calcul ; aucun échec technique converti en échec chimique.

Si une dérive importante persiste entre dt/2 et dt/4, séparer l'intégration de
la cadence réaction et revoir les contacts avant T9. Sinon, décider le test
minimal de recapture/finition de fragments sous les lois les plus stables,
avec contrôles de séquestration/collage parasite, de copie/expression existantes
et d'usage des produits. Ne pas ajouter une loi qui reconnaît un fragment
« incomplet » par sa séquence ou sa longueur globale. La préparation d'un
fragment est autorisée pour un contrôle, pas comptée comme fonction émergente.

Un seul jalon numérique, six essais automatiques. Coût de conception chimique
nul ; coût de calcul potentiellement plusieurs heures, six fois
le nombre total de pas des trois témoins J3 pour les six tâches
nouvelles (facteurs2+4 =6 fois, soit7 fois en incluant la référence). Le temps
réel dépend des motifs tardifs, audits et contention ; consulter le statut.
Synthèse L, bibliothèque, génome long, flux externe et homéostasie toujours ouverts.
