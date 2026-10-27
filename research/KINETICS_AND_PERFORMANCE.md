# Cinétique, campagnes différées et coût du moteur

Discussion du26 octobre2026, pendant la clôture du lot9. Ce document fixe la
suite méthodologique. Le lot10 implémente un premier gestionnaire figé/reprenable
et un diagnostic pré-réaction pour la membrane, voir [mode d'emploi](../campaigns/README.md).
L'analyse complète de tous les hooks et des risques exacts reste à faire.

## Absence observée et diagnostic cinétique

Le temps simulé, les rencontres et les occasions de réaction comptent ; le temps
humain devant le rendu ne détermine pas un échec. Enregistrer automatiquement :

- Horloges simulée/réelle, pas/s après échauffement, tailles et cadence d'observation.
- Premières rencontres, temps de contact, géométries éligibles et réactions locales.
- Nombre de partenaires disponibles, saturation, taux conditionnels et durée
  d'exposition admissible ; distinguer transport, accès, réaction et stabilité.
- Distribution des temps de premier passage, produits utilisables, durée de vie
  et stocks piégés, par graine et par fenêtre temporelle préfixée.
- Essais sans événement comme observations censurées à leur durée finale,
  jamais comme temps de passage infini ou démonstration d'impossibilité.

Une intensité locale connue permet de calculer l'exposition intégrée aux
transitions admissibles. Aucun événement avec presque aucune exposition signifie
« mécanisme peu testé », pas « réaction impossible ». Une estimation de taux ou
une borne Poisson exige des hypothèses de stationnarité/indépendance explicites ;
des contacts répétés corrélés et un bain qui s'épuise ne les satisfont pas d'office.
Ne pas ajuster une exponentielle à trois premières réussites en oubliant les censures.

Préfixer plusieurs horizons et contrôles positifs/négatifs. Prolonger les essais
comparables, conserver aussi les échecs aux horizons initiaux. Un allongement
prospectif doit porter sur toutes les graines retenues, ou être identifié comme
suivi exploratoire d'une graine favorable. Le lot9 prolonge précisément une
graine d'insertion favorable : cela ne mesure pas un taux de réussite à450.
Une cadence fine locale peut diagnostiquer des rencontres manquées sans stocker
toutes les positions ; changer l'observation ne doit changer ni PRNG ni transitions.

## Contrat des campagnes hors conversation

Un manifeste immuable doit fixer sources, lois, scénarios, graines, horizons,
contrôles et critères ; les sorties restent locales. Fournir un lancement Windows,
un suivi et un arrêt propre avec reprise. Les processus de calcul peuvent continuer
après la réponse, tant que la machine reste active ; aucune veille ou relance après
redémarrage ne doit être supposée. Limiter les travailleurs au matériel disponible.

Le suivi doit montrer tâches en attente/en cours/achevées/en erreur, progression
simulée, débit récent, dernier heartbeat et chemins des preuves. L'ETA reste une
estimation révisable. Écrire les états atomiquement ; un statut « en cours » ancien
n'est pas la preuve d'un processus vivant. Au retour, analyser sans dépendre du
contexte de la conversation et sans relancer les calculs déjà achevés.
Des checkpoints périodiques vérifiés doivent permettre de reprendre après arrêt
machine. Une notification n'existe que si elle a été configurée explicitement.

## Profilage indicatif actuel et accélération

`experiments/profile_simulator.py` reproduit un profil court sans observateur,
5000 pas après10 pas d'échauffement. Les premières mesures locales conservées
dans `outputs/performance/` donnent membrane534 :5,73s instrumentées, dont
3,99s dans les réactions et3,34s dans `update_faces`. Ce sont des temps inclusifs,
qui ne s'additionnent pas. Le test G/F102 donne2,66s et comporte encore du JIT ;
ce n'est pas un benchmark stabilisé. Le profilage surpondère aussi les appels
Python. Aucun facteur d'accélération n'est démontré par ces deux profils.

Les forces principales sont déjà compilées Numba et les voisins utilisent un
arbre avec peau de Verlet. La marge la plus visible est la réaction en Python,
les petits appels NumPy, les reconstructions des tableaux mécaniques et les
requêtes spatiales. Priorité : mesurer des segments stabilisés avec/sans analyse,
compiler les boucles et mettre à jour les structures seulement quand leurs liens
changent. Tester le coût à tailles représentatives et la concurrence des graines.

La machine expose une RTX4060 Laptop8Go. Les forces et voisinages locaux sont
compatibles avec une implémentation GPU ; ni localité ni émergence n'imposent le
CPU. En revanche, déplacer seulement les forces laisserait les réactions Python
et les transferts comme goulets. Pour obtenir un gain important, garder positions,
voisins et états réactifs sur le GPU, ou regrouper de nombreux bains indépendants.
Le [guide NVIDIA](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/) décrit
ces coûts de transfert et la limite donnée par la fraction séquentielle.

Les réactions concurrentes sur un port saturé demandent un arbitrage équivalent
au modèle, pas des écritures simultanées incontrôlées. Toute modification de
l'ordre stochastique, du PRNG ou de précision doit être déclarée et revalidée :
conservation, valence, forces, distributions cinétiques et références chimiques.
Une trajectoire GPU bit à bit identique n'est pas présumée. Ne pas obtenir un
« gain » en augmentant le pas, réduisant le bruit ou supprimant des interactions
sans étude de convergence et déclaration d'un changement numérique/chimique.

Un gain global×10 est une cible plausible à explorer, pas une promesse. Distinguer
temps d'une trajectoire, débit total de campagne et volume de données. Réévaluer
après profil stabilisé et une première optimisation CPU mesurée, avant un portage
GPU complet. Cette étape technique n'accroît pas la maturité chimique du projet.

## Robustesse numérique et vitesse fonctionnelle

Voir [équations, coûts et limites](NUMERICS_AND_RENEWAL.md). Séparer le pas de
temps, la cadence de réaction et les paramètres physiques (température, mobilité,
forces, taux). Une baisse de bruit change la chimie ; ce n'est pas une optimisation.

Avant de déclarer un mécanisme robuste numériquement, comparer dt,dt/2,dt/4
sous lois physiques figées, même horizon et cadence d'observation en temps
simulé. Examiner aussi l'intervalle de réaction5dt et ses conflits. Comparer
distributions cinétiques, fuites, produits utiles et erreurs avec incertitudes,
pas l'identité de trajectoires de même graine. Le bruit doit conserver son
échelle sqrt(dt) et les probabilités leur intervalle physique. Une convergence
de quelques forces ou une reprise exacte n'établit pas la convergence chimique.
Pour les paramètres physiques, rechercher un domaine de fonctionnement avec
perturbations modestes et non un point isolé ; déclarer les régressions.

La cible de performance est le temps **réel** pour renouveler les constituants
fonctionnels, chaque famille essentielle suivie séparément, tout en maintenant
l'inventaire et l'activité. Les produits doivent être incorporés ; une hausse
de stock, un déchet ou une chaîne inactive ne compte pas comme remplacement.
Rapporter également vitesse simulée, taille du bain, concentrations/apports,
contacts/éligibilité, température et surcoûts du rendu/checkpoint. Optimiser
l'apport à lois et précision numérique fixes ; ne pas accélérer les réactions
ou grossir dt pour améliorer artificiellement le score. Aucun optimum ni
demi-renouvellement cellulaire complet n'est encore mesuré.
