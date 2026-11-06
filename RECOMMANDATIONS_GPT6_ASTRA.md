# Recommandations GPT-6 Astra — audit critique du projet

Audit commencé le 6 novembre 2026, à la demande de Thomas Cabaret.
**État : audit terminé le 6 novembre 2026, sur le périmètre décrit ci-dessous.**
Ce document a été sauvegardé progressivement, constat par constat, pour rester
exploitable en cas d'interruption. Base de code examinée : commit `99de030`.
Il s'agit de recommandations, pas de modifications adoptées de la chimie.

## Lecture rapide pour la reprise

**Avis général : poursuivre, mais rééquilibrer les priorités.** Le projet a
produit des mécanismes locaux et des transferts matériels réels. Je n'ai pas
trouvé, dans les chemins courants examinés, de contrôleur reconnaissant la
cellule ou sa séquence entière pour la faire réussir. En revanche, une chimie
expressive et une cellule entretenue ne sont pas encore ramenées à une liste
de simples réglages techniques. Plusieurs difficultés restantes sont des choix
de représentation, de bilan ouvert et de maintien de l'information.

| Décision importante | Recommandations |
| --- | --- |
| Distinguer cellule minimale et richesse de fonctions ; tester tôt cette dernière | ASTRA-01, 02, 17 |
| Revenir au maintien équipé et redondant ; ne pas exiger le redémarrage depuis zéro enzyme | ASTRA-03, 14 |
| Construire l'environnement ouvert et fermer aussi le bilan des lipides | ASTRA-06, 09, 13 |
| Mesurer le confinement et le remplacement, pas seulement la fermeture du graphe initial | ASTRA-04, 05, 08, 16 |
| Traiter la finition et la compétition des séquences au-delà de `01` | ASTRA-10, 13 |
| Déclarer aides externes, énergie et vraies horloges de renouvellement | ASTRA-07, 11, 18, 19 |
| Rendre le présent lisible et la télémétrie soutenable dans la durée | ASTRA-12, 15 |

Deux constatations particulièrement discriminantes : **P_G/P_F sont
indiscernables pour la capture/formation actuelle** (ASTRA-17), donc une recherche
de séquences ne peut pas y créer une sélectivité absente des interactions ;
**le cas PT1 ouvert conserve une barrière répulsive à travers son petit hiatus**
à géométrie gelée (ASTRA-16), donc son refus topologique ne diagnostique pas une
fuite. Ces conclusions appellent des actions très différentes.

FR1 est maintenant terminé : **6/6, zéro erreur, deux portes refusées** ;
aucune campagne ni nouvelle loi n'a été lancée par cet audit.

## Mandat et convention de lecture

Cible : une cellule construite, entretenue par des assemblages de particules
sous des lois locales réutilisables, avec alimentation, renouvellement et
récupération après des perturbations non nulles. Ni origine spontanée, ni
division, ni fidélité à la biochimie terrestre ne sont des prérequis.

L'audit distingue : violation de localité ; spécialisation excessive mais
locale ; lacune de preuve ; défaut d'essai ; priorité discutable. Une critique
de résultat ne vaut pas diagnostic établi de sa cause. Les recommandations
ne modifient pas les lois et n'autorisent pas l'ajout d'un nouvel outil.

Chaque item reçoit un identifiant stable, une priorité, des sources du dépôt,
un constat et une action. P0 : risque de viser le mauvais problème ou de
construire sur une hypothèse structurelle fausse. P1 : action scientifique ou
méthodologique importante au prochain jalon concerné. P2 : amélioration utile
différable. Ces vingt items ne sont pas vingt prérequis ni vingt campagnes.
Plusieurs risques figurent déjà dans les documents : l'audit recommande surtout
de les rendre décisifs dans les choix, et précise quelques nouveaux contre-exemples.

## Constats persistés

### ASTRA-01 — P0 : la localité est réelle, l'expressivité reste le risque central

**Établi.** Le moteur courant ne demande pas le nom d'une protéine entière pour
réagir. Mais F0 recrute les catégories P/H, F1 les catégories R/T ; deux sites
voisins liés déclenchent un taux catalytique20 contre0.0001 au fond. Les F0/F1
ont tous deux la même préférence angulaire0.8. Le même motif01 porte l'essentiel
de la fonction démontrée. Cela constitue une catalyse assistée par un motif
local, avec une indirection d'assemblage réelle mais étroite. Cela ne démontre
pas un alphabet permettant une bibliothèque de machines programmables.

**Risque.** Confondre « aucun détecteur global » et « fonctions suffisamment
émergentes ». Les incompatibilités sont aussi résolues par des conventions
explicites : seuls G templent, F–F ne s'apparient pas, les captures voisines
doivent être de groupes matériels compatibles. Ces aides sont admissibles
si déclarées, mais l'audit de localité ne doit pas les blanchir en preuve de
généralité. Aucun motif local interdit n'est identifié ici ; la dette est
la part de la fonction déjà fournie par les primitives.

**Action.** Faire un jalon d'expressivité falsifiable : sous une unique table
de lois gelée, comparer deux assemblages construits ayant des sélectivités
ou actions différentes, puis vérifier un produit réutilisable en aval. Ne pas
exiger leur expression génétique dès ce premier test de capacité. Si aucune
paire utile n'est concevable avec l'alphabet courant, réviser cet alphabet
avant de perfectionner pendant des lots son seul motif01. Éviter l'alternative
inverse consistant à ajouter une primitive spécialisée pour chaque enzyme.
Toute nouvelle machine nécessite toujours l'accord utilisateur prévu au dépôt.

Sources : `research/FUNCTIONAL_MECHANISMS.md` §§2–4,
`simulator/precursors.py::PrecursorCapture`, `simulator/assembly.py::react`,
`simulator/mixed_synthesis.py::MixedCapture`, `research/CHEMISTRY_COMPLEXITY.md`.

### ASTRA-02 — P0 : expliciter deux jalons distincts, cellule minimale et chimie expressive

**Constat.** Une cellule maintenue par un seul co-recruteur polyvalent peut être
un excellent premier résultat. Elle ne répond pas entièrement à l'ambition
initiale de composés portant des fonctions variées. Inversement, trois enzymes
spécialisées ne sont pas une nécessité mathématique du maintien. Le schéma
historique à trois gènes et la réduction actuelle à01 ne doivent pas servir
alternativement de définition implicite du succès.

**Action.** Déclarer deux contrats : (A) cellule construite à réseau minimal
maintenu, même avec une catalyse polyvalente ; (B) démonstration que la famille
de lois peut produire plusieurs fonctions par assemblage. Écrire explicitement
quelles exigences utilisateur sont satisfaites par chaque jalon. Ne pas
retarder A pour une bibliothèque arbitrairement riche, mais obtenir tôt une
preuve peu coûteuse de B pour éviter qu'A repose sur une représentation sans
extension plausible. Le nombre de gènes et leurs longueurs résultent de ce
choix, pas d'un budget historique ou d'une analogie avec la biologie.

Sources : `RESEARCH_DIRECTION.md`, `research/FUNCTIONAL_MECHANISMS.md`,
`research/minimal_cell_spec.json`, `research/cell_checklist.json` F-02/T-04/C-04.

### ASTRA-03 — P1 : ne pas faire du réamorçage depuis zéro outil un prérequis du maintien

**Établi.** FR1 part sans aucun F polymère. C'est plus sévère qu'une cellule
construite qui entretient plusieurs copies d'un outil. La perte du dernier
catalyseur d'un réseau autocatalytique peut rendre la récupération très lente
même si une population équipée serait viable. Son échec est instructif,
mais n'invalide pas à lui seul le projet demandé.

**Résultat lu pendant cet audit.** FR1 est terminé6/6 : fast réussit0/3,
slow1/3 (F01 observé à157.8,52 formations catalysées ultérieures) ; les deux
portes2/3 sont refusées, sans erreur d'exécution. Le compte rendu antérieur
« en cours » est périmé. L'hypothèse de durée de vie contribue peut-être,
mais ne rend pas l'amorçage robuste sur ce domaine.

**Solution simple à ne pas oublier.** La redondance initiale est autorisée.
Tester d'abord le renouvellement d'une population de plusieurs outils, puis
la suppression d'une fraction définie de cette population, sans retirer le
dernier exemplaire par principe. Déterminer le nombre de copies à partir du
rapport naissance/perte mesuré. Une garantie de récupération après disparition
de toute information correspondante serait impossible sans une autre source
de cette information ; ne pas l'ajouter implicitement au cahier des charges.

**Garde-fou.** Une grande population initiale ne doit pas masquer l'absence de
renouvellement : marquer passivement l'ancien matériel et observer son
remplacement fonctionnel sur plusieurs temps caractéristiques. Le réamorçage
reste un test de bassin de récupération, secondaire au maintien équipé.

Sources : `research/BATCH_54_PLAN.md`, `research/CONCEPT_FIRST.md` (amorçage),
`research/BATCH_54_FR1_RECIPES.json` ; rapport final local FR1
`outputs/functional_recovery_mechanism_followups/followup_20261106T135511017624Z/report_0.json`
(SHA256 `178721433e553bd0daa199658162bb6502bf4ba7e399e2c8993a7da4479e56ce`).

### ASTRA-04 — P1 : le recyclage strict actuel peut fabriquer un faux échec

**Établi dans le code.** `RecyclingObserver` exige, pour compter un
`polymer_reassembly`, que les DEUX atomes P et R aient été libérés de matière
polymérisée, puis réassemblés ensemble. Il faut ensuite une incorporation dans
un squelette pour compter `recycled_incorporations`. Une coupure de squelette
suivie de la réutilisation du composite intact, ou le remplacement d'un seul
de ses atomes, n'est donc pas un succès de ce compteur.

**Problème de priorité.** Démontrer que la matière peut revenir jusqu'aux
précurseurs est utile pour l'export et la fermeture des voies. Mais imposer
ce trajet maximal à toute preuve de renouvellement peut faire travailler sur
une exigence artificielle. Une cellule peut réutiliser des monomères intacts ;
le renouvellement d'une fonction ne requiert pas que chaque liaison axiale
soit détruite à chaque cycle.

**Action.** Conserver le compteur strict sous son nom explicite et ajouter
trois observations distinctes : réemploi d'un composite issu d'un polymère ;
flux de remplacement des atomes/composites du stock initial vers des outils
actifs ; libération de matière réellement perméable et son export. Définir
pour chaque obligation de fermeture lequel de ces trajets est nécessaire.
Ne pas requalifier RF1 en réussite, mais ne plus interpréter son zéro strict
comme « aucun renouvellement matériel possible ».

Sources : `simulator/recycling_observations.py::observe_assembly`,
`research/MACROMOLECULE_HOMEOSTASIS.md`, bilans RF1/FA1 du lot54.

### ASTRA-05 — P1 : une porte binaire n'est pas un diagnostic scientifique

**Établi.** PT1 échoue notamment parce qu'une chaîne52 a51 liens à l'instant
final300, après un contour valide à299.5. RF1 exigeait une catalyse tardive
positive dans un témoin sans pertes qui a presque épuisé son stock. Ces refus
sont correctement conservés, mais ils agrègent absence de preuve, limite du
protocole et défaillance fonctionnelle.

**Action.** Donner aux conclusions trois états : satisfait sur le domaine ;
contre-exemple fonctionnel observé ; non concluant faute d'exposition ou de
mesure. Conserver en parallèle le booléen prospectif initial. Pour la membrane,
préférer comme obligation biologique une borne de perte de contenu et un temps
de réparation à une fermeture topologique à un instant arbitraire. Une ouverture
brève n'est pas automatiquement fatale ; sa tolérance doit être mesurée.
Pour un stock fermé, mesurer le débit pendant une fenêtre où le substrat reste
disponible ; une fenêtre tardive fixe ne suffit pas si cette disponibilité
disparaît. Pour le maintien, passer ensuite à un apport externe déclaré.

**Garde-fou.** Ne jamais inventer un intérieur pendant les ouvertures, ni
choisir après coup un instant final favorable. Préfixer couverture des mesures,
pertes tolérées, fenêtres et perturbations. Une modification de critère ouvre
un nouveau protocole ; elle ne change pas le verdict historique.

Sources : `experiments/review_selective_transport.py::decide`,
`experiments/review_functional_recycling.py::decide`, `simulator/mixed_boundary.py::BoundaryObserver`,
`research/BATCH_54.md`.

### ASTRA-06 — P0 : l'environnement ouvert ne peut plus rester une annexe indéfiniment

**Établi.** Les essais courants ont des stocks finis et des murs mécaniques.
La source/absorption au bord est décrite, mais pas implémentée. Une grande
partie des questions d'homéostasie et d'export dépend pourtant de ce choix.
Les tableaux d'atomes P/R restent structurés par un nombre fixe de supports.

**Risque.** Régler des pertes, une inhibition ou un bilan de production dans
un monde fermé puis découvrir que le régime ouvert ne possède pas le même
équilibre. À l'inverse, déclarer un stock borné parce que tous les précurseurs
ont été consommés n'est pas le maintien demandé.

**Action.** Construire prochainement une tranche technique minimale source/puits
au bord, indépendamment de la cellule : IDs stables, création/destruction de
précurseurs libres seulement dans une couche extérieure, bilan exact de matière,
injection stochastique à loi fixée et absorption des sorties. Une réserve de
places inactive peut servir de première implémentation si elle est exclue de
tous les voisins, forces et observateurs, et si sa saturation invalide l'essai.
Ne pas réinjecter au voisinage d'un catalyseur ou selon les concentrations
intracellulaires mesurées. Éprouver d'abord un bain simple, puis le réseau
autocatalytique équipé ; la membrane peut venir après ce bilan ouvert.

Cette construction peut avancer en parallèle conceptuellement aux diagnostics
de récupération. Elle réduit un risque d'architecture concret, contrairement
à une nouvelle série de réglages d'un réservoir fermé.

Sources : `research/OPEN_BOUNDARY.md`, `research/HOMEOSTASIS.md`,
`simulator/copy.py::__init__`, `simulator/assembly.py`, checklist E-01/W-01.

### ASTRA-07 — P1 : l'autonomie doit être définie avec ses aides externes

**Établi.** La libération périodique utilise `time % period` dans les règles
d'appariement, avec des taux modifiés pendant une fenêtre commune. C'est un
forçage externe global explicite, pas un feedback reconnaissant la cellule.
Le projet autorise des helpers et une alimentation énergétique : son usage
n'est donc pas automatiquement une tricherie. En revanche, dire sans réserve
« toutes les fonctions sont locales et autonomes » serait trop fort.

**Action.** Distinguer une cellule entretenue sous un protocole externe fixé
d'une cellule sous environnement stationnaire. Pour le premier jalon, garder
éventuellement l'horloge, en l'affichant dans la démo et le bilan. Tester au
moins que les fonctions peuvent cohabiter sous la même période et avec des
événements démarrant à des phases diverses. Ne pas laisser chaque sous-fonction
hériter d'un cycle différent puis additionner ses réussites. Si l'objectif
ultérieur exige une alimentation stationnaire, la libération locale reste
un jalon explicite, sans obligation d'ajouter immédiatement une nouvelle protéine.

Sources : `simulator/copy.py::react`, `research/FUNCTIONAL_MECHANISMS.md`,
`research/LOCALITY_AUDIT.md`, `research/CHEMISTRY_COMPLEXITY.md`.

### ASTRA-08 — P1 : l'observateur de membrane ne peut pas mesurer son renouvellement complet

**Établi dans le code.** `BoundaryObserver` ne reconnaît une enveloppe que si
elle contient au moins80% des têtes de la membrane initiale, avec une aire
minimale liée au rayon initial. Ce choix est raisonnable pour étudier l'insertion
dans une membrane préparée. Il devient incompatible avec une preuve de
renouvellement prolongé : une enveloppe fonctionnelle qui remplace plus de20%
de ses constituants initiaux peut être rejetée par construction.

Ce n'est **pas une tricherie dynamique** : ces identités restent dans l'analyse.
C'est une limite de mesure, actuellement correctement annoncée dans son champ
`scope`, à ne pas propager à l'essai de cellule entretenue.

**Action.** Conserver cet observateur pour les comparaisons historiques ; créer
pour le maintien un suivi passif de l'enveloppe par continuité spatiale/topologique
et confinement du contenu, indépendant de la conservation des IDs initiaux.
Déclarer les ambiguïtés de fusion, fragmentation et ouverture. Compter séparément
matière initiale, matière nouvelle et qualité de confinement. Un contrôle
analytique simple est une enveloppe géométriquement identique dont les IDs sont
progressivement remplacés : sa fonction ne doit pas disparaître de la mesure.
Ne jamais utiliser ce suivi global pour réparer ou guider les réactions.

Sources : `simulator/mixed_boundary.py::BoundaryObserver.observe` et `summary`,
notamment le seuil `len(real & original) < .8 * len(original)`.

### ASTRA-09 — P0 : fermer le bilan des lipides, pas seulement celui des protéines

**Établi.** Dans `LinkedLipids`, H–T se forme mais ne se dissocie jamais.
Les ruptures et échanges concernent les contacts latéraux entre ces dimères.
Le turnover P/R ne fournit donc pas de voie de recyclage des lipides. Le bain
actuel ferme ce bilan par épuisement du stock H/T, pas par homéostasie.

**Conséquence conditionnelle, mais stricte.** Dans un futur bain alimenté,
si la production moyenne de L reste positive et qu'aucun L ne sort ni ne se
décompose, leur nombre croît. Une production lente ou saturée ne résout pas ce
bilan. Cela ne démontre pas que la chimie est condamnée : le détachement puis
l'export de L intact est une autre solution possible, à caractériser réellement.
Il n'est pas obligatoire de casser chaque lipide en atomes pour renouveler une
membrane ; il faut une voie de sortie de sa matière excédentaire.

**Action prioritaire de conception.** Écrire, pour le candidat effectivement
simulé, les entrées/sorties et puits irréversibles de chaque matière (P_G, P_F,
R0/R1, H/T), y compris agrégats et produits parasites. Comparer explicitement :
détachement/export de L intact ; dissociation locale H–T suivie de sortie des
précurseurs ; inhibition réversible de production combinée à des pertes réelles.
Éprouver le cas d'excès, pas seulement une lésion à combler. Aucun besoin de
nouvelle enzyme ne doit être présumé avant cette comparaison.

La suppression au bord doit être définie indépendamment du rôle biologique,
avec traitement local des liens sortants. La première tranche source/puits
limitée aux précurseurs d'ASTRA-06 est un test technique, **pas** une solution
complète pour L. Ne pas confondre insertion, croissance, remplacement matériel
et maintien à taille bornée. Vérifier également qu'une membrane qui s'agrandit
reste dans le domaine de courbure permettant son confinement.

Sources : `simulator/linked_lipids.py::bind`, `react`, `springs` ;
`simulator/mixed_synthesis.py::react` ; `research/OPEN_BOUNDARY.md`,
`research/HOMEOSTASIS.md`. Le graphe conditionnel `minimal_cell_spec.json`
ne remplace pas ce bilan de la chimie actuelle.

### ASTRA-10 — P0 : `01` évite précisément le problème de finition de l'information

**Établi.** L'appariement exige l'égalité exacte des symboles ; les substitutions
par mauvais appariement sont donc interdites par la loi. C'est une simplification
locale acceptable, mais une fidélité parfaite à ce niveau n'est pas un résultat
expérimental. Le risque pertinent est ailleurs : fragments, mauvais assemblages,
compétition et perte des séquences utiles. Le motif `01` n'a qu'une liaison à
fabriquer ; il ne teste pas la reprise d'une copie partielle déjà polymérisée.

Le garde `monomer_only_capture`, et le garde G/F distinct, bloquent justement
cette reprise dans le candidat courant. Les fragments G peuvent encore servir
de matrices ; les fragments F peuvent conserver des motifs catalytiques. Ainsi
une activité chimique persistante peut coexister avec une information appauvrie.
P10 a déjà observé des fragments abondants ; T9E a essayé une recapture de bouts
sans restaurer l'expression complète. Ce verrou est connu, **pas résolu** par
la réussite ultérieure du dimère.

**Action.** Conserver `01` comme boucle minimale de maintenance, mais établir
prochainement un contrat d'information sur quelques séquences distinctes de
plusieurs symboles, sous les mêmes lois et avec census exhaustif. Choisir les
longueurs à partir des assemblages envisagés ; aucune obligation de revenir
immédiatement à dix ou vingt-quatre bases. Observer remplacement des matrices,
produits F utilisables et distribution des parasites, pas seulement copies
exactes cumulées. Séparer fidélité par contact, fidélité de chaîne et persistance
de l'information sur plusieurs générations.

**Familles à départager avant réglage.** (a) Finition par recapture locale,
avec discrimination géométrique/conformationnelle des outils terminés ; cela
demande de traiter leur séquestration, et ne se réduit pas à retirer un garde.
(b) Assemblage processif/nucleation depuis un bout et progression par contacts
voisins, dont arrêt/libération reconnaissent un port terminal local. Un outil
supplémentaire pour cela est une option à proposer avec son coût et à faire
approuver, pas à installer silencieusement. Ni « longueur cible » ni reconnaissance
du gène complet dans les lois. Un contrôle local préparé peut réfuter ces
esquisses bien avant une nouvelle amplification longue.

Sources : `simulator/copy.py::react`, `research/BATCH_18.md`,
`research/BATCH_19.md`, `research/BATCH_27.md`, `research/BATCH_28.md`.

### ASTRA-11 — P1 : unifier le contrat énergétique sans imposer du réalisme inutile

**Établi.** CP1 a corrigé une incompatibilité réelle : attractions libres
additives face à des liaisons saturables. Le potentiel compétitif possède une
dérivée incluant la concurrence et un delta local ; cette correction est une
bonne décision de représentation, à conserver. Ce n'est pas un matching global
de membrane : les dépendances sont bornées en voisinages de contact.

En revanche, le filtre énergétique H–T et celui des contacts L ne couvrent
pas toute la chimie. Les formations P–R, appariements, ligations, pertes et
changements d'angles associés à l'occupation peuvent commuter des potentiels
sans ce même traitement. `MixedSynthesisObserver.summary` le signale pour P/R.
La température cinétique moyenne proche de la cible n'est pas un bilan de ces
commutations ; elle peut cacher des événements locaux ou l'action du thermostat.

**Action.** Tenir une petite table des transitions : potentiel changé, travail
externe implicite/explicite, énergie retirée au thermostat, retour possible,
et choix cinétique assumé. Instrumenter seulement les transitions suspectes,
par sommes et extrêmes locaux, avant d'introduire un correctif. Une formation
P–R près d'un segment active notamment sa répulsion de confinement : cette
contribution mérite un contrôle de transfert lorsqu'on couple pertes et membrane.

**Ne pas surcorriger.** L'utilisateur autorise une pseudo-chimie aidée et un
apport externe. Il n'est pas nécessaire de construire un ATP, un solvant explicite
ou d'imposer l'équilibre détaillé à toute réaction pour atteindre la cible.
Un réservoir énergétique idéal fixé peut être une hypothèse déclarée. Un filtre
`exp(-deltaU/T)` sur des réactions irréversibles ne prouve pas à lui seul une
thermodynamique complète ; inversement, une règle entraînée localement n'est
pas automatiquement une tricherie. L'obligation est un fonctionnement stable,
composable et sans réparation centrale, avec un coût de helpers visible.

Sources : `simulator/competitive_ports.py`, `simulator/transition_energy.py`,
`simulator/assembly.py`, `simulator/copy.py::_finish`, `simulator/mixed_boundary.py`,
`simulator/motion.py`, lots49–50.

### ASTRA-12 — P1 avant les essais ouverts longs : borner la mémoire et le coût de l'observation

**Établi dans le code, coût futur à mesurer.** Plusieurs objets gardent tout
l'historique en mémoire (`assembly.events`, `turnover.events`, `births`, histories).
`CopyObserver.observe_assembly` reparcourt/copie la liste cumulée des formations
à chaque observation ; les checkpoints sérialisent l'état complet des observateurs
et les journaux exportés par la chimie. Désactiver les trajectoires ne supprime
pas ces accumulations. Avec une activité durable et une cadence fixe, ces
parcours/copies peuvent cumuler un coût quadratique en durée, même à population
physique bornée. Les stocks fermés actuels masquent en partie ce cas.

**Action.** Avant une démonstration de maintien longue, séparer état physique,
état minimal des observateurs et journal append-only sur disque local. Garder
des compteurs incrémentaux, fenêtres bornées et marqueurs de provenance par
atome/lien ; conserver le journal complet comme preuve hors Git. Un checkpoint
référence des segments et offsets vérifiés au lieu de recopier systématiquement
toute l'histoire. Les loupes restent temporaires ; aucune suppression des preuves
existantes pour économiser de la place.

Un benchmark utile mesure le coût d'un même intervalle au début et après une
histoire synthétique longue, à état physique comparable. Vérifier reprise exacte
et absence d'effet sur la dynamique. Cela est plus directement utile qu'un
portage GPU tant que les tableaux d'IDs, l'alimentation et la télémétrie changent.
Il ne faut pas promettre un coût constant ou « quelques pourcents » sans cette
mesure sur l'architecture finale.

Sources : `simulator/observations.py::CopyObserver.observe_assembly`,
`simulator/recycling_observations.py`, `simulator/mixed_synthesis.py`,
`simulator/checkpoint.py::save`.

### ASTRA-13 — P0 pour plusieurs gènes : la coexistence n'est pas fournie par un bilan de masse borné

**Risque conceptuel reconnu mais encore ouvert.** Une ressource commune et
des pertes peuvent borner la masse totale sans maintenir chacune des informations
nécessaires. Les petits fragments peuvent consommer les mêmes monomères et
servir de matrices ; un gène peut monopoliser la réplication. La production
d'outils bénéficie au bain commun et ne garantit pas, à elle seule, le retour
du gène devenu rare. Le candidat à un seul motif `01` ne teste pas cette question.

**Action de conception.** Pour deux séquences nécessaires et leurs fragments,
écrire les signes des rétroactions attendues : quand l'une devient rare,
qu'est-ce qui augmente son gain net *par copie restante* ? Quand elle devient
abondante, qu'est-ce qui le diminue ? Faire ce raisonnement avec les contacts
réels autorisés, en tenant compte de PI1 : le produit F actuel ne peut pas
simplement réoccuper G comme inhibiteur. Une borne `B - delta*N` ne résout le
problème que si la dépendance de B aux matrices, ressources et compétiteurs
est explicitée. Un petit modèle cinétique de décision est utile ici, clairement
séparé de la simulation particulaire et jamais utilisé pour la contrôler.

**Options à comparer.** Stabilité différentielle locale + redondance peuvent
suffire au premier horizon fini, sans système de régulation élaboré. Au-delà,
examiner une inhibition réversible suffisamment sélective, une limitation locale
du templating par occupation, ou une architecture qui réduit le nombre de gènes
indispensables. Chaque option doit affronter les fragments et les interactions
croisées ; « ajouter un inhibiteur » n'est pas un mécanisme fermé. Une fonction
supplémentaire requiert la proposition et l'accord déjà prévus.

Ne pas transformer ce point en exigence d'immortalité : avec des pertes
stochastiques et un inventaire fini, la perte de la dernière copie reste possible.
Le contrat réaliste est une durée de survie, plusieurs renouvellements et une
récupération de perturbations laissant de l'information exploitable, sur toutes
les trajectoires prévues, pas seulement celles qui survivent. Cette limite doit
rester distincte d'un défaut systématique de coexistence.

Sources : `research/HOMEOSTASIS.md`, `research/MACROMOLECULE_HOMEOSTASIS.md`,
`simulator/copy.py::react`, points R-05/H-03/H-04/H-06 du registre.

### ASTRA-14 — P1 : FR1 invite à diagnostiquer la co-occupation, pas à augmenter la ligation

**Lecture supplémentaire des données existantes, sans nouvelle simulation.**
Les audits FR1 donnent, en moyenne temporelle sur600 :

| Variante/graine | F composites actifs | F monomères appariés | Double appariement sur un lien G, exposition échantillonnée |
| --- | ---: | ---: | ---: |
| fast/0 | 1,016 | 0,193 | 0 |
| slow/0 | 6,000 | 1,184 | 0 |
| fast/1 | 1,505 | 0,509 | 0 |
| slow/1 | 14,615 | 1,153 | 550,11 |
| fast/2 | 0,416 | 0 | 0 |
| slow/2 | 5,164 | 1,424 | 0 |

La stabilisation des monomères les conserve bien dans slow/0 et slow/2,
sans double appariement observé. Elle n'est donc pas suffisante sur cet horizon.
Le cas slow/1 ayant réussi accumule ensuite surtout du double appariement
**déjà ligaturé** (549,20 d'exposition), à distinguer d'occasions de nouvelle
ligation (0,23). L'exposition brute aux doubles ne mesure pas un flux productif.

Ce type de blocage avait déjà été identifié dans MIN1 au lot33 : une capture
sans obtention de la seconde, suivie du choix justifié d'un départ équipé au
lot34. Les lois/pertes ne sont pas identiques, mais cette mémoire doit orienter
la reprise ; ne pas redécouvrir ce diagnostic par défaut à chaque nouvelle série.

**Décision suggérée.** Si l'on poursuit le diagnostic du redémarrage sévère,
examiner la répartition des captures F0/F1 entre les quatre matrices G01,
leur résidence et la phase de libération. Des F peuvent être présents mais
répartis sur des matrices différentes. C'est une hypothèse géométrique/cinétique,
pas une cause démontrée. Un petit contrôle de co-occupation, puis au besoin une
loupe sur les captures dans un échec slow, est plus informatif qu'un nouveau
balayage du taux de ligation. Ne pas augmenter encore la durée de vie libre
sans question nouvelle. ASTRA-03 demeure : ce redémarrage depuis zéro outil
ne doit pas bloquer tout le travail de maintien équipé.

**Limite essentielle.** `GeneticAudit` observe avant le tick réactionnel ; les
captures puis ligations peuvent survenir dans ce même tick. Zéro ici signifie
zéro **observé à cette cadence**, pas impossibilité d'une transition. Ses rejets
sont séquentiels, ses compteurs de paires sont nets, et son exposition n'est pas
l'intégrale exacte du hazard. Pour une décision fondée sur les occasions rares,
un compteur placé dans la vraie branche de réaction, passif et sans tirage RNG,
évite cette ambiguïté et la duplication des prédicats dans l'audit.

Sources : les six `genetic_audit.json` de
`outputs/functional_recovery_mechanism_followups/followup_20261106T135511017624Z/A/campaign_20261106T135511306553Z/tasks/*/attempts/*/`,
champs `exposure / observed_time` et `exposure.ligation_*` ;
`simulator/genetic_audit.py::scan`, `integrate`, `attach`.

### ASTRA-15 — P1 : une seule vue du présent, sans effacer l'historique

**Établi.** Les fichiers de priorités/maturité/architecture accumulent les
comptes rendus successifs ; leurs précautions sont souvent bonnes, mais la reprise
demande de reconstruire quel « actuel » s'applique. Le75% de M-04 reste attaché
à EG1, tandis que le candidat mécanique courant est CP1. La GUI appelle encore
EG1 « État actuel · bain intégré », en conservant correctement ses limites et
EN1. L'atlas `metabolism_map.json` date du30 octobre : sa rubrique `current`
décrit MD2 sans F nouveau complet et une synthèse L non acquise, alors que des
transferts plus récents existent. Ce sont des décalages concrets, pas des preuves
frauduleuses, mais ils favorisent une impression de cumul entre chimies.

**Action.** Ajouter une vue courte faisant autorité : candidat, hash/recette,
capacités sous ses lois, preuves héritées à revalider, gaps, campagnes réellement
actives et trois prochaines décisions. Garder les comptes rendus dans leur
historique, avec liens ; éviter de recopier chaque lot en tête de dix documents.
Le registre doit distinguer « meilleure preuve historique » de « preuve sous
le candidat courant ». Les paliers sont déjà annoncés comme ordinaux : afficher
leurs mots (sous-cas, séparé, couplé, cible) en première lecture réduirait le
risque de lire75% comme trois quarts du travail accompli.

La GUI peut légitimement proposer une ancienne démo robuste, une variante en
travail et un échec instructif ; les nommer ainsi. Le nombre de presets n'est
pas un indicateur d'avancement. Mettre l'atlas à jour avec deux graphes ou couches
clairement distincts : architecture cible conditionnelle et réactions réellement
réalisées par le candidat actuel, y compris retours/exports manquants. Ne pas
dessiner trois enzymes distinctes comme découvertes ni cacher l'intérêt du
co-recruteur polyvalent actuel.

Les résultats finaux FR1 lus pendant cet audit sont conservés ici ; les mentions
FR1 « en cours » des documents du lot54 correspondent à leur date de clôture.
La prochaine reprise doit les réconcilier avant de lancer un suivi.

Sources : `README.md`, `research/PRIORITIES.md`, `research/MATURITY.md`,
`research/CELL_CHECKLIST_COMPACT.md`, `research/metabolism_map.json`.

### ASTRA-16 — P1 : une chaîne ouverte peut encore faire une barrière physique fermée

**Constat plus précis sur PT1, complément à ASTRA-05.** La répulsion membranaire
est une distance à un **segment épais**, extrémités comprises, avec rayon0,55.
Dans le cas final ouvert PT1/barrier/1, les deux bouts sont distants de0,63854,
donc nettement moins que deux rayons (1,10). Les zones répulsives de leurs
segments incidents se recouvrent malgré l'absence du dernier lien.

À géométrie gelée, pour une bille P/R retenue passant sur l'intervalle entre
ces bouts, la seule contribution des deux segments est minorée par
`k * (r - d/2)^2 ≈ 4,259`, avec k=80 ; soit environ53 fois T=0,08. La borne
vient de la distance à chaque segment, au plus égale à celle de son extrémité,
et du minimum de la somme des deux pénalités quadratiques sur cet intervalle.
Ce n'est **pas** un temps d'évasion calculé : la membrane bouge, les potentiels
alentour comptent et une ouverture ultérieure plus large reste possible.

**Conséquence.** L'état `final_contour_valid=false` est un défaut du critère
topologique strict, pas une preuve de trou perméable dans cette géométrie.
Ne pas lancer des modifications de chimie pour éliminer ce seul booléen avant
d'avoir vérifié le confinement effectif. Les données actuelles gardent leur
verdict prospectif refusé ; elles n'autorisent pas non plus à déclarer la
rétention démontrée durant les intervalles non mesurés.

**Alternative simple.** Dans le prochain protocole, mesurer pertes réelles et
résidence de cohortes, avec couverture temporelle annoncée, et distinguer
cycle de liaisons, barrière géométrique/énergétique et confinement observé.
Un diagnostic passif du champ répulsif autour d'une ouverture suffit pour
choisir le bon critère ; aucun contour virtuellement refermé ne doit être
réinjecté dans les forces ni servir à inventer des traversées non observées.

Sources : `simulator/membrane_bath.py::barrier_force`,
`simulator/mixed_boundary.py::segment_forces`,
`research/BATCH_54_FA1.json` (`endpoint_gap=0.6385412276550136`).
Calcul analytique de cet audit, aucune nouvelle trajectoire.

### ASTRA-17 — P0 si l'on vise EN/EA distincts : une symétrie interdit leur sélectivité directe actuelle

**Déduction des règles, plus forte qu'une absence de succès.** Pour le
co-recrutement de précurseurs libres, P_G et P_F ont la même catégorie de capture0,
la même classe mécanique P, la même masse/mobilité pertinente et le même groupe
de coopération. La formation P–R emploie les mêmes prédicats et taux pour les
deux. Dans un même voisinage avant formation, échanger les étiquettes G/F de
deux supports libres ne change donc ni leur capture ni leur propension de jonction.
La différence de famille devient pertinente dans les processus aval.

**Conséquence précise.** Changer uniquement la séquence ou la forme d'un outil F
ne peut pas lui donner une préférence chimique intrinsèque pour la jonction
P_G–R plutôt que P_F–R **dans ce canal, à environnement/abondance égaux**.
Des stocks différents, des pertes différentes après formation ou une consommation
aval différente peuvent modifier les populations ; ils ne constituent pas
cette sélectivité de synthétase. Ce raisonnement ne prétend pas interdire toute
diversité de fonction, ni la distinction géométrique P/R versus H/T.

**Décision.** Si l'on conserve le co-recruteur polyvalent comme architecture
minimale, cette symétrie est utile et ne demande aucune correction. Si EN et EA
distincts redeviennent une obligation, ne pas lancer une recherche de séquences
sur cet alphabet d'interactions inchangé : rendre une différence de précurseur
accessible à une interaction élémentaire réutilisable, ou changer l'architecture
de produits/ports. Compter cette extension et ses effets croisés, puis chercher
la sélectivité par assemblage. Éviter une table « cette enzyme produit N ».

Plus généralement, des arguments de symétrie, de valence et de conservation
peuvent éliminer des branches sans simulation. Ici, l'identité matérielle G/F
existe déjà mais ne participe pas à la décision locale de capture/formation :
plus de calcul ne peut inventer la discrimination manquante.

Sources : `simulator/precursors.py::refresh`, `react`,
`simulator/mixed_synthesis.py::MixedCapture`, matrice `contact`,
`simulator/assembly.py::react`, `simulator/motion.py`.

### ASTRA-18 — P1 : calibrer aussi l'horloge des pertes et du remplacement

**Calcul direct sur les taux RF1/FR1.** Une liaison G a un taux de rupture
5e-5, multiplié par0,05 lorsqu'elle est protégée. Les demi-vies caractéristiques
de sa première rupture sont donc environ13 863 unités sans protection et
277 259 avec protection permanente. À1200, la probabilité de première rupture
d'une telle liaison est comprise entre environ0,30% et5,82%, selon son exposition
à la protection. Ce sont des repères de hazard, pas des bornes déterministes
sur une petite population ni le temps de renouvellement de tous les atomes.

**Conséquence.** La survie de plusieurs G01 pendant RF1 ne démontre pas leur
renouvellement ni une récupération après pertes substantielles. Le critère est
un garde utile, mais il peut passer simplement parce que presque aucune liaison
initiale G n'a été attaquée. Le vrai remplacement matériel demande encore les
étapes aval et peut être plus lent. Un nombre fixe de cycles externes ou une
durée jugée longue pour F n'est pas forcément long pour G.

**Action.** Pour chaque famille, annoncer séparément temps de production,
perte, remplacement et exposition effective aux perturbations. Définir les
essais de maintien en nombre de renouvellements utiles, avec budget de calcul
compatible. Pour diagnostiquer la récupération sans attendre une rare perte
naturelle, appliquer une petite lésion externe préprogrammée, conserver de la
redondance et mesurer la réparation ; déclarer ce test forcé distinct du
renouvellement spontané. Ne pas accélérer les pertes juste pour faire un joli
T50, ni diminuer encore les pertes pour masquer une incapacité à reconstruire.

Le délai humain reste `temps simulé requis / débit effectif`, propre à chaque
famille et à l'activité du bain. Les anciens scénarios de quelques heures ne
bornent pas ces temps, et aucun engagement « moins de dix heures » ne découle
de la vitesse des microdémos ou de ces calculs.

Sources : `experiments/prepare_functional_recycling.py::RATES`,
`simulator/turnover.py::react`, `research/NUMERICS_AND_RENEWAL.md`.

### ASTRA-19 — P1 avant validation du candidat : deux cadences numériques, pas une

**Établi.** Le moteur sépare maintenant pas mécanique et intervalle réactionnel.
EN1 raffine le premier en conservant le second. N1 avait raffiné les deux dans
une chimie brownienne historique. Aucun de ces résultats ne suffit à certifier
la convergence de toutes les réactions du candidat CP1 avec pertes et flux.

`1-exp(-k*Delta)` donne la bonne probabilité pour un événement isolé à hazard
constant ; cela ne rend pas exact l'enchaînement discret rupture → capture →
formation → appariement → ligation. Des motifs apparaissent/disparaissent dans
un tick, et l'ordre peut compter lorsque plusieurs canaux se concurrencent.
Avec k=35 et Delta=0,01, la probabilité conditionnelle est déjà environ0,295.
Ce chiffre n'établit pas un défaut, mais justifie de ne pas assimiler l'intervalle
réactionnel à une limite continue acquise.

**Action proportionnée.** Lorsqu'un mécanisme utile est établi, vérifier sur un
petit motif représentatif le raffinement de chaque cadence séparément, puis
sur un bain réellement actif la stabilité des observables qui portent la décision.
Conserver taux, température, concentrations et protocoles externes en unités
simulées. Une autre trajectoire ou un booléen différent sur trois graines ne
prouve pas à lui seul un biais de discrétisation : comparer distributions et
effets d'une ampleur pertinente. Ne pas financer une convergence exhaustive
d'une architecture encore conceptuellement incomplète.

Conserver Langevin comme base décidée avec l'utilisateur. Une accélération des
réactions parasites révèle un problème chimique ; revenir à une mauvaise
diffusion pour le cacher ne le résout pas. Le bon indicateur de performance est
le flux fonctionnel/renouvellement par temps réel, avec validité numérique,
et non le nombre de pas ou de rencontres brutes par seconde.

Sources : `simulator/engine.py::prepare`, `simulator/copy.py::react`,
`research/BATCH_17.md`, `research/BATCH_18.md`, `research/BATCH_48.md`,
`research/NUMERICS_AND_RENEWAL.md`.

### ASTRA-20 — P2, option ciblée : favoriser la rencontre orientée avant d'inventer une machine

**Observation de code.** Le couple d'orientation de `CopyChemistry.extra_forces`
agit sur les paires déjà appariées. Dans le chemin courant, les reconnaisseurs
R de composites libres n'ont pas d'attraction de reconnaissance avant capture ;
la réaction attend proximité et orientation compatibles. À l'inverse, les
précurseurs bénéficient d'une attraction avant capture sur F. Une cinétique
lente d'appariement peut donc venir d'une petite zone de capture admissible,
pas d'une diffusion insuffisante ni d'un taux de ligation trop petit.

**Piste non testée, à envisager seulement si le diagnostic le justifie.** Une
préassociation faible, locale, orientée et saturable entre ports de reconnaissance
compatibles pourrait augmenter les occasions sans ajouter de protéine. Elle doit
partager la cohérence libre/lié apprise avec CP1 : pas une attraction additive
illimitée suivie d'une liaison exclusive. Vérifier libération, faux partenaires,
fragments et coût de calcul ; conserver le cycle externe déclaré. Compter les
paramètres/termes nouveaux, et préférer leur réutilisation à une exception dédiée
au « deuxième monomère de la bonne copie ».

Un motif à quelques composites peut décider si la préassociation améliore la
capture réutilisable ou crée un piège, avant une campagne en bain. Cela reste
une alternative de mécanisme, **pas** une solution démontrée ni une demande de
la coder maintenant. La redondance initiale et le départ équipé doivent être
examinés d'abord pour le jalon de maintien (ASTRA-03).

Sources : `simulator/copy.py::extra_forces`, `simulator/physics.py::orientation_kernel`,
`simulator/precursors.py`, `simulator/competitive_ports.py`.

## Couverture et clôture

L'examen couvre architecture cible et candidat réel, copie/traduction, capture
et synthèse P/R/H/T, pertes et recyclage, ports L compétitifs, transport,
observateurs, cadences mécaniques/réactionnelles, checkpoints, protocoles et
présentation de maturité. Résultats lus : notamment CR1, PT1, RF1, FR1 et leurs
diagnostics, avec retours aux lots de conception pertinents. Aucune nouvelle
trajectoire n'a été nécessaire pour les constats enregistrés.

Ce n'est pas une vérification formelle exhaustive de tout le dépôt ni une
certification de tous les scénarios historiques, de la GUI ou des performances.
Les recommandations conceptuelles restent à discuter/tester ; les déductions
analytiques sont limitées aux règles et hypothèses indiquées.

## Ordre de travail suggéré, sans multiplier les chantiers

1. **Reprise courte : fermer les décisions de périmètre et de mesure.** Lire
   FR1 terminé, conserver les refus, rapprocher son diagnostic de MIN1/lot33.
   Définir le jalon de maintien équipé avec renouvellement matériel et pertes
   tolérées. Corriger la vue du présent. Décrire une paire d'assemblages pour
   éprouver l'expressivité ; si elle impose un outil supplémentaire, présenter
   le mécanisme/coût à l'utilisateur avant implémentation. Ce travail conceptuel
   ne nécessite pas une nouvelle grande cohorte.
2. **Construction indépendante : une vraie alimentation ouverte minimale.**
   Adapter IDs/présence atomique et source/puits au bord dans le moteur partagé,
   avec bilans et télémétrie bornée. Tester un bain simple puis le réseau équipé,
   à lois déclarées, sans attendre la récupération depuis zéro outil. Exposer
   les chemins de sortie de toutes les matières ; décider celui des lipides.
3. **Couplage utile : flux, pertes et remplaçants fonctionnels.** Départ redondant,
   suivi du matériel initial, absence d'épuisement artificiel, perturbation
   limitée et récupération. Le transport membranaire se juge sur pertes/résidence,
   pas sur un lien manquant à l'instant final. Ne pas transférer RF1 par simple
   option : la configuration mixed exclut actuellement `bond_turnover`, et
   l'observateur de provenance irréversible doit être adapté avant ce couplage.
4. **Validation ciblée et information.** Sur un candidat utile, contrôler les
   deux cadences et quelques nouvelles graines selon la variance observée ;
   tester plusieurs séquences pertinentes et leur compétition. Automatiser les
   suites dont les décisions sont calculables, avec arrêt pour interprétation
   si la cause change. Ne pas relancer les mêmes graines jusqu'à une réussite.

Ces blocs définissent des décisions et constructions, pas une estimation de
quatre lots jusqu'à une cellule viable. Les priorités conceptuelles peuvent
invalider un bloc avant calcul. Faire un point après deux à quatre interventions
substantives : au moins une incertitude structurelle doit avoir été levée et
un couplage utile doit s'être rapproché. Sinon, discuter une représentation
alternative au lieu de prolonger une chaîne de réglages locaux.

## Ce qu'il faut préserver

- Le moteur commun, le découplage graphique, les recettes figées, les reprises
  exactes et les données locales conservées : ils rendent cet audit possible.
- La distinction déjà explicite entre initialisation construite, synthèse réelle,
  produit utilisé, maintien et récupération ; les labels de provenance passifs.
- Les bons changements de mécanisme : saturation réelle des sites, capture
  partagée entre matières, potentiel compétitif CP1, simplification de l'outil
  quand sa fonction ne demande pas une longue chaîne.
- Langevin et la franchise sur les échecs ; pas de retour à un mauvais mélange,
  pas de suppression des variantes refusées pour embellir la démonstration.

Le principal correctif n'est pas une nouvelle couche de procédures. Il est de
faire porter les prochaines décisions sur **expressivité, bilan ouvert et
remplacement effectif**, en laissant de côté les échecs de proxy qui ne montrent
pas encore un défaut de fonction. Pas de preuve de cul-de-sac irréversible du
projet ; pas de preuve non plus que tout le reste sera du simple ajustement.
