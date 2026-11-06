# Fidélité à l'objectif : localité et risques de pilotage

Lot51 : zéro changement de loi, type, état, port, taux ou outil. La réduction
de quatre billes et la Hessienne d'un squelette complet sont des analyses
externes : ni angle préféré calculé, ni nombre51 par tour, ni vecteur propre
dans les forces ou réactions. `LipidGeometryAudit` lit des composants, cycles
et aires globalement mais ne les transmet jamais au hook. Échantillonnage
borné, une capture au premier témoin ; pas de PRNG/cache de voisins touché.
CR1 change horizon et observation, pas les règles physiques CP1/CH1. Le crible
automatique ne fait que classer les résultats/arrêter le lot, sans régler une
réaction ni une condition de simulation. Les helpers/cycles externes et leurs
limites énergétiques des candidats antérieurs restent déclarés.

Lot49 CF1 : ajout/retrait de contact = deux L/quatre billes et interactions
incidentelles à coupure existante ; barrière PR du seul segment modifié. Delta
et facteur thermique réutilisés, un choix de gate, zéro taux/type/port/gène/outil.
Pas de detailed balance globale. L'option none conserve les anciennes dynamiques.
CF1 pausé après contre-exemples, pas adopté. CP1 est un prototype statique :
chaque énergie de paire est normalisée par les scores des voisins de ses deux
ports. Charge de port<=1, cas binaire exact, aucun matching global, séquence,
origine ou agrégat. Le gradient nécessite les partitions de voisins ; le delta
de réaction futur doit inclure les termes affectés jusqu’au second rang spatial
et les partitions pouvant nécessiter le troisième. Ce surcoût de portée est
réel, borné indépendamment de la taille d’un agrégat ; aucune requête de contour.
Ce coût est déclaré avant intégration, pas remplacé par une énergie globale
pilotant une réaction. Aucune primitive biologique ou nouveau paramètre ajustable.
FS1 reconnaît motifs/flux globalement seulement pour observer des archives.

Lot48 RP1 : perte de squelette protégée par liaison (a,b), appariements
réciproques a–x/b–y et liaison(x,y), au plus4 composites/8 billes. Aucun test
séquence/longueur/gène/origine/stock/fonction. Pas d'identité d'agrégat, même
pour distinguer deux brins : le prédicat autorise les motifs satisfaisant ces
liens locaux. Quatre taux et facteur de protection conservés ; un choix de
prédicat alternatif, zéro type/port/gène/outil/constante nouvelle. Réutilisation
espérée pour duplex, non validée. Le garde P–R reste degré0 et ports libres.
Les labels de recyclage ne pilotent rien ; ancien défaut occupied exact sur
deux préfixes RV1. EL1 fait un bilan global d'observation de deux phases de
contact sur un bain sélectionné ; il n'ajoute aucun calcul d'énergie globale
aux réactions. Neighborhood d'analyse séparé, pas de PRNG ou cache dynamique
muté ; clone/préfixe devront être vérifiés. Le forcing périodique reste externe.

Lot47 : aucune loi chimique changée. GUI charge exactement les3 EG1,
les statistiques observées ne pilotent pas les réactions. RX1 encapsule les
appels existants de turnover, sans tirage supplémentaire, et lit leur journal
pour reconstruire le stade après rupture de squelette. Origine polymérisée,
intensités et occupations servent seulement à mesurer. États/RNG/observateurs
finaux exacts sur2 archives et passivité/reprise sur microcas. EN1 ne change
que la discrétisation mécanique ; cadences physiques et tous taux/potentiels
conservés. La piste de protection par appariement cohérent est un draft local,
pas une loi ajoutée ou un test de bonne séquence/fonction.

Lot46 EG1 : remplacement d'un contact entre trois composites L (six billes),
occupations de leurs ports et interactions spatiales incidentes à la coupure
existante1+4*dock_width. Ajouter la différence de barrière des deux segments
retiré/formé contre les atomes P/R axialement liés à portée. Aucun contour,
séquence, origine, succès ou stock global dans l'acceptation. Les recherches
numériques peuvent parcourir les tableaux mais seules ces interactions locales
contribuent. Le facteur exp(-deltaU/T) réutilise la température et les potentiels
existants ; un gate supplémentaire, zéro type/port/gène/outil/taux/constante.
Sa réutilisation dans d'autres transitions est espérée, pas démontrée. Le coût
informatique par proposition peut croître avec le bain et reste à mesurer sur
la cohorte. Ce n'est pas une preuve de bilan thermique global : ruptures, helpers
de synthèse et cycle externe gardent leur dette. Option none par défaut,
anciens préfixes physiques/RNG testés. Les statistiques ne pilotent pas les règles.
PI1 n'ajoute aucune dynamique : état préparé, ablations communes, audit passif.
Son précontrôle courant utilise le véritable prédicat GeneticAudit ; il ne
change pas le comportement pour rendre le test favorable.

Lot45 : zéro nouvelle primitive chimique. CL1 observe trois L/six billes,
650 frames et les variations de potentiel des contacts affectés ; clone et
préfixe archivés exacts. Aucune origine ou fermeture dans les forces. CX1 est
une ablation ; CW1 change une constante de portée/raideur existante, sans nouveau
helper/taux/gène. Le gate du job choisit l'analyse dans l'orchestration, jamais
une réaction. Les démos CB1 sont des états construits et des échecs documentés,
pas une preuve de cellule spontanée ou viable. Aucun outil d'insertion ajouté.

Lot44 CB1 : aucune loi dynamique ajoutée. Même capture coopérative,
barrière segmentaire locale et échanges ; géométrie short_length.92 au lieu de.98
explicitement différente.52 L sont construits, pas déclarés émergents. Zéro L
est une ablation d'initialisation, sans contour virtuel ni mur pour garder le
paquet. Observateurs/GUI lisent les types et vrais liens sans piloter la physique.
Le contrôle statique de trois L lit seulement leurs faces et leur occupation ;
il n'effectue ni insertion ni déplacement dynamique. La piste associative future
reste une hypothèse, pas une primitive cachée. Aucune nouvelle enzyme/gène.

Lot43 BI1 : seule extension dynamique, reprise du helper MD2 de barrière :
segment de deux têtes L +position d'un atome P/R dont le lien axial est occupé.
Trois positions dans la force, état local d'un lien avec partenaire supplémentaire ;
portée finie .55, forces réciproques aux extrémités. Zéro reconnaissance de
dimère/outil/contour complet. Rayon/raideur transférés .55/80, zéro nouvelle
enzyme/gène/type/port. La commutation du potentiel à la jonction P/R conserve
une dette énergétique explicite. L'anneau219 L et le paquet décalé sont un
départ construit, pas une auto-organisation démontrée. Les IDs d'origine,
contours et positions de naissance ne servent qu'aux observateurs. L'échantillon
déclenché par une naissance ne consomme pas de hasard et n'entre pas dans les
forces. Retrait de l'observation et reprise testés ; pilote100 sans nouvel outil.

Lot42 : coopération de capture sur motif de deux composites F directement
liés et deux ligands, six billes. Compatibilité matérielle déjà utilisée par
la jonction, aucun objectif de produit/chaîne complète, contour, information
d’origine ou concentration. Affinités dérivées de l’occupation, pas nouvel état
chimique mémorisé. Forces et captures partagent la condition ; delta H/T ajoute
seulement les voisins F directement liés aux sites libérés et leurs interactions
spatiales à portée existante. Zéro enzyme/gène/type/port/taux indépendant ajouté,
une condition locale en plus. Transition de potentiel : aide non thermodynamiquement
fermée. Loupe six billes/20 temps, contrôle exact40, sans feedback de l’observation.

Lot41 MX1 : mêmes captures locales saturables pour P/R/H/T, une seule mise
à jour par tick. Compatibilité des constituants et motifs de deux F directement
liés +deux ligands (six billes) pour catalyse ; aucune lecture de chaîne complète,
origine, protéine ou contour dans les réactions. Delta H/T limité aux forces
modifiées et à leurs rayons, comme L3. Les certificats d’outil entier/alimentaire
et contacts ultérieurs sont passifs. Test de retrait d’observateur exact.
Zéro nouvelle machine/gène/type/port/taux indépendant ; asymétrie de formation
P/R historique-H/T énergétique et ordre séquentiel déclarés. Pas de contrôle
par concentration ou de réparation pilotée globalement.

Lot40 CT1 : seule la raideur d'un ressort de capture déjà formé change,
calculée depuis E et largeur de la même attraction. Attraction tronquée à3largeurs,
formation de capture dans rayon0,25, états de sites saturables ; aucun nouveau
voisinage, retour observateur ou identité d'agrégat. Zéro type/port/état/taux/gène
ajouté. Option figée par scénario ; défaut35 conservé. La règle locale dérivée
ne garantit pas continuité de potentiel ou thermodynamique ; P/R garde sa
formation historique, pas la porte énergétique H/T. La GUI ne pilote aucune loi.

Lot38 : pose native uniquement dans le constructeur de F01 préparés, jamais
dans une réaction ou réparation. Ressort de capture dérivé E/largeur², même
stiffness dans les forces et ΔU ; aucune lecture biologique ni taux adapté aux
mesures. Diagnostic première capture passif exact, trois positions/un événement,
64 atomes pour l’énergie de contexte. Helpers de niveau de potentiel toujours
non calibrés ; P/R historique inchangé, L3 est une branche séparée.

Lot37 L2 : ΔU calculé seulement pour les termes modifiés dans les rayons des
forces (cores, capture, ports), plus un ressort axial. Indexation des liens
locaux, aucun potentiel total du bain, contour ou observateur dans la décision.
Les spectateurs distants n’affectent pas la porte ; comparaison mathématique
au potentiel complet réservée aux tests. Zéro protéine/gène supplémentaire.
Porte irréversible : ne garantit ni équilibre détaillé ni fermeture énergétique.

Lot36 L1 : motif catalytique six billes (deux F composites voisins, H,T),
occupation des ports et distances seulement. Les vrais liens H–T indexent les
ports MD2 ; aucune composante, contour ou séquence entière dans les réactions.
Les indices ne choisissent pas le partenaire. Helper : activation de répulsion
et ressort/ports au lien, énergie non calibrée et maintenant diagnostiquée.
La loupe première naissance lit les64 atomes pour les énergies, conserve seulement
six positions/un événement et ne change pas trajectoire/PRNG.195 tests passent,
MD2 exact sur trois préfixes ; L1 demeure séparé du candidat par défaut.

Lot35 MIN1M : aucun fichier du moteur ou des lois modifié. G01/F01 et
témoins changent uniquement l'initialisation sous MD2. Collecteur et GUI
reconnaissent des chaînes entières pour mesurer, jamais pour agir. Les nouveaux
compteurs lisent les supports réellement nés et leur activité antérieurement
certifiée ; ils n'ajoutent aucun tirage aléatoire ou retour vers la chimie.
Coût : zéro primitive/gène/outil/helper supplémentaire. Cycle externe conservé.

## MIN1D / MIN1R — observer puis tester un départ construit

La loupe parcourt des liens pour **choisir une observation** ; ces données ne
dirigent aucune réaction. Deux rejeux bit-exacts confirment sa passivité, avec
captures/état bornés et checkpointables. Aucun contour/gène entier n'est lu
par les lois. MIN1R change seulement les liens préparés du même outil F01,
avec témoins de mêmes atomes/symboles/positions/PRNG. Les critères de F entièrement
neuf et actif sont calculés après coup depuis les vrais IDs et événements.
Coût chimique nul, aucune machine supplémentaire, aucune particule créée/supprimée.

## MIN1 — contrôle de taille du même assembleur

Aucun hook ou observateur de simulation modifié : F01/F001/sites séparés sont
des initialisations sous les lois MD2, no_boost leur ablation annoncée. La
réaction lit toujours deux sites directement liés et deux ligands réels,
jamais taille ou séquence cible. Les séquences complètes ne servent qu'à la
préparation et à la mesure. La route préparé/exprimé→produit→usage est extraite
passivement des données existantes ; aucune rétroaction sur le bain.
Le plan/source/horizons/portes A/B sont figés avant calcul. Le draft H/T→L
n'est pas une loi ajoutée, ni une nouvelle machine autorisée implicitement.

## RV1 — pertes locales, sans recycleur biologique primitif

Sur un lien de squelette, deux supports voisins et leurs occupations directes
déterminent le taux G/F et le facteur de protection. Pour P–R : degré nul du
support, absence d'appariement et de ligand sur ce site. Voisinage borné par
les ports existants ; aucune lecture de chaîne, séquence, contour ou quantité
globale. Le degré est calculé depuis les liens locaux, pas depuis la longueur
du composant. L'information G/F vient du type élémentaire de support.

Coût : quatre taux et un facteur, zéro type/état physique/port/outil/gène/atome.
Les changements d'énergie du potentiel ne sont pas calibrés : helper cinétique
assumé. Positions/vitesses conservées ; vrais R avec symbole persistant. Les
journaux et labels de recyclage sont des sorties passives, jamais des gardes.
L'observateur peut reconnaître une chaîne cible mais n'en sauve aucune.
Les comparaisons sans observateur et les taux nuls sont exacts, reprise et
tree/brute contrôlés. Les scénarios à contacts préparés sont des contrôles
mécaniques, pas des preuves d'émergence. Voir BATCH_31.md.

Lot9,25 octobre2026. La cible est une implémentation locale de fonctions qui
n'ont de sens qu'à l'échelle des assemblages. Concevoir une chimie, fournir
énergie et conditions initiales ne dispense pas de cette contrainte.

## Ce qui invaliderait une démonstration

Lot26 GUI3 : les neuf scénarios actuels ont la signature exacte du manifeste
MD2. Aucun réglage pour améliorer le rendu, aucune trajectoire précalculée.
Les positions affichées correspondent exactement au moteur headless au même
pas, pause/lecture/reprise vérifiées ; les compteurs ne consomment pas de PRNG.
Les ensembles initiaux G/F/anneau servent à préparer et à mesurer, pas à guider
une réparation ou un choix de réaction. Les sondes inconnaissables affichent
« non classable ». Le cas dégradé est conservé dans le catalogue. Aucun ajout
de loi, helper, outil, gène ou coût causal ; même budget2118 du grand bain.
Les fonctions de contour et recensement final F restent purement analytiques.

Lot25 MD2 : potentiel harmonique sur deux ports de deux dimères explicitement
liés, quatre billes, Jacobien exact. Ne lit ni contour, composante, taille ou
rôle biologique. Remplace deux ressorts/quatre angles latéraux ; les rungs
internes restent. Coefficient dérivé de l'attraction libre existante, pas de
nouvelle constante fonctionnelle. Un choix de potentiel explicite, zéro nouvel
alphabet/état/port/gène/outil. Dissociation et échange restent actifs en transfert.
La coupure à10 du seul lien de la paire locale est un forçage externe déclaré,
fixé avant calcul, jamais une réaction décidée par les mesures. Les observateurs
et la porte entre expériences ne pilotent aucune trajectoire. Voir BATCH_25_PLAN.md.

Lot24 : aucun changement des forces/réactions de production. La loupe remplace
temporairement l'appel update_faces par un observateur qui appelle l'original
exactement une fois, sans tirage PRNG supplémentaire ; préfixes LT2 et tests de
passivité vérifiés. Son déclencheur temporel et ses identités de contact ne sont
jamais accessibles aux lois. Capture bornée à six molécules effectivement
sélectionnées, sous plafond24, de39,53 à45,53 ; classification des ruptures et
géométrie des ports uniquement en lecture. MD1 inclut deux ablations déclarées
de paramètres chimiques, conservées comme candidats séparés de diagnostic.
Langevin reste la base de travail ; aucune protéine ou fonction globale ajoutée.

Lot23 : extension du même Langevin aux membranes et au bain couplé, sans autre
force ou réaction. Audit thermique passif pour tous ces hooks ; le cache est
invalidé après chaque tick réactif. Tests de cache, passivité et reprise sur
les quatre hooks étendus. La classification des contours, produits utiles et
temps de premier événement reste exclusivement analytique. Les variantes GUI
ont des signatures distinctes, aucun succès emprunté aux sources historiques.
Masse/frottement et deux vitesses par bille sont le coût physique déjà déclaré ;
zéro type/port/état/gène supplémentaire, même budget de particules. Cycle et
thermostat externes conservés et déclarés ; aucune correction de température
depuis l'observateur. Voir BATCH_23_PLAN.md/BATCH_23.md.

État lot22 : [bilan complet](BATCH_22.md). Le candidat LT1 ajoute Langevin
au hook copy, sans lecture d'assemblage : vitesse et thermostat indépendant
par bille, forces existantes entre liens explicites et voisins de portée finie.
Le bruit thermique et le cycle externe de libération sont déclarés ; aucune
adaptation à une concentration, longueur ou performance mesurée. Coût : deux
coordonnées de vitesse par bille, masse/frottement et recalcul des forces après
chaque réaction, y compris les changements non rapportés comme événements.
Zéro nouvelle primitive chimique, état/port, gène ou protéine.

L'audit de filiation reconstruit a posteriori les composantes et séquences
avant chaque tick ; il lit les arêtes sources réellement enregistrées et vérifie
le checkpoint final. Ces identités et l'audit thermique ne pilotent aucune
force ou réaction. Les tests de passivité et reprise incluent vitesses et PRNG.
La stricte fidélité des symboles est une loi choisie ; l'absence d'erreurs
ponctuelles ne doit pas être présentée comme une correction émergente. Membrane
et chimie couplée non transférées à ce mouvement ; les démos gardent leur défaut.

### Critères généraux

- Lire une séquence, une longueur cible ou un génome entier pour déclencher
  copie, fin de copie, expression, repliement ou fonction enzymatique.
- Reconnaître une protéine/vésicule comme objet complet puis lui attribuer un
  comportement. Donner à une bille « enzyme N » toute sa fonction serait une
  autre façon de déplacer la réponse dans les primitives.
- Identifier un contour, son intérieur, son rayon/aire ou ses membres dans une
  règle, puis refermer, repousser le contenu, choisir une insertion ou transporter
  une molécule pour atteindre le résultat. Une pression globale de consigne serait
  également un pilotage, même calculée depuis les coordonnées.
- Faire une conversion/relocalisation externe d'un produit entre fabrication et
  usage, changer les lois au moment opportun ou corriger l'état depuis l'analyse.
- Programmer un calendrier de sauvetage ciblé sur les événements observés.
  Une condition externe fixée d'avance est une aide différente, à déclarer.
- Présenter un anneau préparé comme autoassemblé, une bille-sonde comme un gène
  réellement retenu, ou des mécanismes séparés comme une cellule intégrée.

Une interaction sur quatre/six billes liées, de portée et d'arité fixes, reste
locale si elle lit uniquement leurs attributs et liens voisins. Le fait que ce
motif contienne tout un petit dimère n'autorise pas une inspection arbitraire
d'une future macromolécule. Le coût du motif doit rester borné lorsque celle-ci
grandit. La localité ne suffit pas : une primitive spécifique par fonction peut
écrire implicitement le programme attendu. Mesurer réutilisation et complexité.

## Audit du code au départ du lot9

| Zone | Lecture dans la dynamique | Diagnostic et réserve |
| --- | --- | --- |
| `copy.py` | Reconnaisseurs liés, arêtes voisines et ports ; motif parallèle de ligation | Pas de séquence complète dans `react`/forces. `sequence` sert à l'initialisation ; l'observateur reconnaît les produits |
| `assembly.py`/`precursors.py` | Deux précurseurs, deux F voisins liés, six billes au total | Aide catalytique explicite ; pas de reconnaissance d'enzyme entière. Alphabet de précurseurs spécialisé et diversité limitée |
| `docking.py` | Deux H–T, leurs faces saturées, géométrie à quatre billes | Aucun contour ni taille souhaitée. Les longueurs locales induisent une courbure préférée ; ne pas régler celle-ci en ligne depuis un rayon global |
| `engine.py` | Voisins spatiaux, forces, diffusion, boîte imposée | Taille des tableaux et arbres spatiaux sont de l'infrastructure, pas une identité biologique. La boîte ne doit pas remplacer la membrane |
| `observations.py` | Graphes complets, séquences, provenance, contours | Autorisé pour mesurer uniquement. L'API donne des références vivantes : risque de rétroaction accidentelle à couvrir par tests |
| Cycle génétique | Temps uniforme, période et phase de déliaison | Forçage externe global réel, pas autonomie en bain stationnaire. Fixé avant les runs, sans consultation des copies ; étudier/ablate sa nécessité |

Les gardes « plus aucun précurseur disponible » peuvent accélérer le calcul si
elles ne changent aucune transition locale éligible. Les champs de rayon ou de
labels de départ sont permis dans le constructeur ; ils ne doivent pas réapparaître
dans les forces/réactions. Permuter les IDs ne doit pas changer une force physique.

## Obligations du lot9

MIX2 (lot21) : vitesses et masses locales ; forces conservatives existantes,
Langevin par bille, OU DPD sur deux billes proches seulement. Le thermostat de
paire lit position/vitesse relative et applique des impulsions opposées. Ni
agrégat, centre de masse, séquence ou but de mélange dans le mouvement. Pas de
soustraction globale de vitesse ou rescaling de température. L'observation
globale et les horloges de benchmark ne changent aucune transition. La force
mise en cache est limitée aux liens fixes du modèle mixing ; pas de transfert
automatique à une chimie réactive. Coût physique/numérique explicite dans BATCH_21_PLAN.md.

MIX1 (lot20) ajoute un hook de diagnostic mécanique sans réactions, utilisant
les mêmes noyaux, thermostat et parois. Les liaisons internes fixes exercent
leurs forces par paires ; aucune identité moléculaire globale ne décide un
déplacement. Centres de molécules, labels initiaux, clusters et MI sont lus
uniquement par l'observateur, avec PRNG d'analyse distinct et tests de passivité.
Le contrôle sans répulsion est explicite ; aucun ajout de forçage/inertie ni
réglage des conditions des démos. Ne pas présenter cet isolement comme une
nouvelle fonction émergente ou une chimie complète.

Ajout P10 (lot19,29 octobre2026) : `polymer_population.py` est un observateur
optionnel qui lit les composants, séquences complètes, identités initiales et
contacts pour les recenser. Ses données n'entrent ni dans les taux, ni dans les
forces, ni dans le PRNG. Aucun changement de loi ou de motif réactif ; portée
globale d'analyse déclarée, coût chimique nul. Tests d'identité dynamique et
de reprise exacte dans `tests/test_polymer_population.py`. Aucun ajout de
matière ou sauvetage d'une séquence selon les résultats observés.

Le grand anneau et les cohortes de sondes sont préparés et marqués seulement
pour analyse. Les contacts H–H/T–T de V8 se rompent/reforment sans reconnaître
leur composante. L'insertion est une observation après coup de nouvelles unités
dans un contour issu de l'anneau ; ce n'est jamais une opération du moteur.

Une barrière locale sur un lien de membrane peut repousser une sonde : deux
extrémités et une sonde, trois billes, force et réaction distribuées par gradient.
Elle doit exister aussi sur un fragment ouvert, agir des deux côtés et rester
indépendante de l'intérieur. Une sonde transparente est un contrôle physique,
pas une preuve que X/Y/Z et les vrais G/F passent/sont retenus comme souhaité.

Tests : gradient, moment/force totaux, arité indépendante de l'agrégat, modification
des seuls labels/rayon initiaux sans effet après préparation, arbre/exhaustif,
reprise, et trajectoire avec/sans observateur identique. Archiver échecs et helpers.

## Audit des ouvertures, lot11

`boundary_audit.py` lit composantes, IDs initiaux, extrémités et épisodes uniquement
après l'observateur. Aucune de ces informations n'est consultée par les forces
ou réactions. Il ne dessine pas de nouveau contour et ne corrige aucun état.
Les observations physiques antérieures, positions et PRNG restent identiques,
y compris dans le pilote comparé aux sources du lot9. Les extrémités proches
sont un diagnostic de géométrie, jamais une règle de refermeture ni une preuve
de confinement. Le coût ajouté est analytique, sans type/port/helper physique.

## Condition d'échange G1, lot12

`contact_exchange.py` peut lire les autres ports du partenaire libéré et de
l'arrivant. Si les deux sont occupés, le swap est interdit ; sinon ancien taux
et géométrie. Lecture bornée d'états de ports déjà existants sur trois dimères,
pas d'inspection de longueur, de composante ou de molécule biologique complète.
Un contact est remplacé par un contact, aucune fermeture ou relocation imposée.
Le prédicat est symétrique au swap ; cela ne prouve pas l'équilibre détaillé.

Coût : une condition/mode logique, zéro type, état mémorisé ou taux/rayon ajouté.
La chimie modifiée est déclarée G1 ; ne pas lui attribuer les réussites de B.
L'aide cinétique non thermique antérieure reste une dette énergétique explicite.
Le choix du mode est figé avant les essais et ne dépend jamais des observateurs.
## Contrat de reprise et bain J0

Voir [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) : la localité est nécessaire,
mais ne démontre ni minimalité ni richesse des assemblages.

J0 lit, pour chaque atome P/R, l'existence de son lien P–R saturé : deux atomes
réels. Cet état active son contact avec une bille L ou un segment H–H lié ;
la force de segment porte sur trois atomes et est symétrique dans l'espace.
Les listes d'atomes sont des index de types chimiques, jamais des composantes
biologiques. Aucun parcours de polymère ou contour ne dirige ces contacts.

Coût croisé : deux constantes de contact, rayon0,55 et raideur80, reprises aux
valeurs de la barrière existante, plus le prédicat libre/lié. Zéro élément,
outil ou gène ajouté aux six types hérités ; union non minimisée. La commutation
peut changer l'énergie : aide non calibrée déclarée. Température unique imposée.
Les tests couvrent observateur sans rétroaction, force de réaction sur L,
état de liaison, mêmes positions/PRNG après reprise, caches spatiaux séparés
et absence de parois internes. Les contours sont réservés aux mesures, qui
abandonnent les intervalles inconnus. Production de L par F non implémentée.

## GKA — observateur génétique

Le diagnostic lit les positions, états locaux et motifs d'appariement/ligation
existants, avec ses propres requêtes spatiales. Son état, ses fenêtres et ses
épisodes ne sont jamais lus par la chimie. Il remplace seulement le callable
par un wrapper passif qui appelle l'original une fois et retourne ses événements.
Pas de nouveau type/état/port physique ; aucun label de gène ou séquence cible
dans les filtres. Les tests vérifient positions, chimie et PRNG identiques,
y compris dans le hook couplé. Les sources historiques sont préservées.

## J2 — frontière d'environnement explicite

`world_box` ne sert qu'à initialiser la boîte globale d'un monde sans L et à
translater le paquet ; les forces réutilisent les mêmes murs du moteur sur
toutes les billes. Aucun contour, centre de gène ou concentration globale n'est
consulté pendant la dynamique. Coût : deux longueurs externes pour un contrôle,
zéro primitive chimique ni nouveau taux. Le défautNone est comparé exactement
au hook J1 archivé ; un override avec L est refusé. Le census post-hoc peut lire
le gène entier et des composants pour mesurer, jamais pour piloter les lois.

J3 conserve toutes les lois, hors ablation nommée du taux catalytique. Les
copies/positions initiales sont construites, sans recentrage ou mur dans la
cellule pendant la dynamique. Les parents G préparés sont reconnus uniquement
dans l'observateur de filiation, sans PRNG ni retour vers les réactions. Source
externe future au bord du monde déclarée dans OPEN_BOUNDARY.md, pas implémentée.

N1 ne change aucune règle locale : même état initial construit et toutes
sources simulator identiques à J3, dt divisé par2/4, réaction toujours5dt,
observation0,5. Le comparateur lit des chaînes entières et provenances seulement
après calcul ; aucun résultat ne modifie les trajectoires ou taux. Coût chimique
nul, un protocole numérique et ses alertes descriptives, pas un régulateur.

N2 ajoute uniquement une cadence numérique indépendante, transmise aux taux
locaux existants via l'intervalle du tick. Aucun voisinage, état ou type chimique
supplémentaire ; défaut5 exact vérifié. Le suivi conditionnel utilise des rapports
globaux pour choisir **une nouvelle expérience**, avec sources figées avant sa
trajectoire. C'est une intervention expérimentale externe, jamais une décision
de la cellule, une rétroaction dans ses réactions ou une preuve d'homéostasie.

## T9E — recapture d'extrémités F, candidat opt-in

`gf_end_capture=true` remplace degré(F)=0 par degré(F)<=1 sur les contacts G/F
et dispense ces contacts du XOR monomère. Le support reste G avec degré>0.
La coopération est évaluée sur les voisins directement liés au G, comme pour
un F monomère auparavant. Même reconnaissance0,3, états de saturation,
symboles, orientation, ports, taux et forces. Aucun test de longueur, séquence,
gène, outil entier, produit ou contour. Option absente/false garde la référence.
Coût : un choix de garde, zéro type/état physique/port/taux/helper/gène ajouté.
F interne de degré2 reste exclu, y compris si un observateur le juge incomplet.

Le recensement des sites F préparés et des degrés est purement passif ; il
ne parvient jamais au hook. Les contrôles idéaux conditionnent explicitement
un tirage accepté, sans prétendre mesurer une cinétique. La production garde
son PRNG normal. L'automate choisit entre essais sources figées, pas dans un bain.
Un F complet peut recapturer par ses bouts : mesurer sa séquestration est un
contre-test, pas un label de protection introduit dans les lois.

## CP1 dynamique — lot50

Un choix de potentiel sans constante supplémentaire. Les ports libres lisent les affinités à coupure spatiale existante ; le gradient inclut les partitions voisines. Le delta de contact touche deux L, celui d’échange trois ; les termes affectés au second rang requièrent des partitions jusqu’au troisième rang. La naissance H/T ajoute un L hypothétique et repondère aussi ses voisins. Aucun parcours de composant, contour, génome, origine ou label observateur dans ces décisions. Le calcul peut scanner les paires pour extraire ce voisinage borné ; une indexation globale ne devient pas une dépendance physique distante. Initialisation des dimères explicitement construite, conservation des atomes, aucune liaison latérale imposée. Contrôles delta local/global, perturbation distante, passivité et reprise exacts. Pas d’équilibre détaillé revendiqué.
