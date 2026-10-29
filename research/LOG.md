# Journal de recherche

## 2026-10-23 — cadrage et premiers embranchements

Le point de départ peut être construit. L'utilisateur autorise explicitement la
superposition sélective, les liens avec propriétés et les interactions dépendant
de l'état lié/libre. Les deux cibles prioritaires sont la copie de séquences et
les vésicules, avec des fonctions portées par les assemblages.

Les criblages statiques antérieurs sont conservés dans `experiments/results/`.
Ils montrent une orientation effective et une préorganisation de substrats,
mais aussi un contre-exemple de valence : la même interface peut brancher.
Ils ne sont pas une simulation de copie ni de formation de vésicules.

Pistes ouvertes : molécules à deux billes (support et reconnaissance), copie
par complément de quadrilatères locaux ; activation d'un site par une liaison
voisine ; déliaison par cycle environnemental ou par changement local d'état ;
courbure de doubles rangées par incompatibilité de leurs longueurs préférées.

## 2026-10-23 — dynamique et arbre de recherche

Méthode enregistrée dans `.agents/skills/local-chemistry-research/SKILL.md`,
validée par le validateur de skills. Les sources et leurs SHA-256 sont archivés
par essai, avec graines, paramètres, résultats et trajectoires. Voir MODEL.md
pour les lois effectivement utilisées et RESULTS.md pour les preuves brutes.

### Copie

- T2 : fragments surtout dimériques, aucune copie complète jusqu'à t=480.
  L'allongement des extrémités initiales et les copies de fragments constituent
  des modes parasites observés. Les événements restent dans les résultats.
- T4 : exploration conjointe de la rigidité, concentration et durée d'association
  pour trouver un point de fonctionnement. Ce saut ne permet pas d'attribuer
  causalement l'amélioration à un seul paramètre.
- T4, séquence 001011 : une copie complète libérée dans chacune des graines
  0,1,2 à t=600. Deux graines ont un événement de ligation dont le support est
  une copie complète. Aucune seconde génération complète n'est démontrée.
- Contrôle T4permanent : copie complète mais non libérée dans la fenêtre testée.
  Contrôle T4negative sans polymère initial : aucune ligation. T4sequence copie
  aussi 010010 sans changement des règles. Ce sont des contrôles unitaires,
  pas des estimations statistiques de rendement.
- T5short : copie libérée de 0011. T6caps : copie libérée de 200112, où les deux
  2 sont des coiffes structurelles à un port ; le contenu informatif est 0011.
  Une amélioration du rendement grâce aux coiffes n'est pas encore établie.
- T4nogate retire seulement l'activation par voisin lié : aucune copie complète
  en graine 0 jusqu'à t=600, contre une copie libérée pour T4. Cela soutient le
  helper dans ce réglage ; une estimation de rendement demanderait plus de graines.
- T4local teste T3 sans cycle externe, avec un déliage accéléré quand les deux
  supports appariés sont polymérisés. Une copie complète et des ligations
  supplémentaires apparaissent, mais aucune copie complète totalement libérée
  n'est observée. La libération démontrée dépend donc encore du cycle externe.

### Membrane

- V0/V1 : le ruban initialement droit se courbe ; le contrôle à longueurs égales
  reste presque droit. Avec 16 sous-unités, une graine ferme et une autre ne
  ferme pas dans la fenêtre testée : le choix de la taille importe.
- V4 : 18 sous-unités déjà polymérisées, initialement droites, ferment pour les
  trois graines 0,1,2 à t=300. Les aires finales sont proches de 25. Le moteur
  n'a aucun critère de contour fermé ; celui-ci appartient à l'observateur.
- V2/V4fragments : fragments dispersés dans l'espace ouvert, associations
  partielles sans boucle. V5 teste une boîte finie, une température augmentée et
  une liaison coopérative des deux rangées ; il forme encore des amas déformés.
  Les images suggèrent des pièges dus à l'attraction isotrope des extrémités.
- V6 remplace cette attraction par des potentiels de ports orientés, avec
  forces et couples distribués aux deux billes liées définissant le port.
  Le gradient de ce nouveau potentiel passe une vérification par différences
  finies. V6, graine 1, assemble cinq fragments de trois sous-unités en une
  boucle fermée de 15 sous-unités, d'aire finale 16.93. La sixième pièce reste
  séparée. La graine 0 ne ferme pas ; V6free, graine 2, ne ferme pas non plus.
  L'assemblage depuis des fragments est donc démontré une fois mais reste fragile.

### État de fin de cette itération et prochains tests discriminants

La copie complète avec libération a un point de fonctionnement répété et deux
séquences testées ; la fermeture de rubans préparés a trois graines positives ;
l'assemblage depuis des fragments a une réussite et un échec sous le même réglage.
Le résultat le plus récent figure dans OVERVIEW.md et first_demonstrations.png.

Les quatre vérifications de forces/observateur passent. Le rejeu depuis les
sources archivées reproduit exactement toutes les métriques d'un ancien essai T2.
Les statuts ne supposent pas une chimie commune, une perméabilité, une mutation
fonctionnelle ou une lignée autonome qui ne sont pas encore démontrées.

Prochains tests utiles : dissociation réversible des interfaces mal enregistrées
de V6, au lieu d'ajouter une reconnaissance de contour ; compatibilité des deux
chimies dans un même bain ; copies complètes de deuxième génération et rendement
sous variations de longueur ; rétention différentielle de deux types de solutés.
L'expression de fonctions diverses par repliement reste un objectif distinct.

### Incidents techniques distingués des résultats physiques

Quatre essais denses ont été interrompus avant toute dynamique : le placement
aléatoire séquentiel demandait une distance minimale excessive et pouvait ne
jamais se terminer. Ces dossiers ont un statut d'incident, sans métriques
physiques. La préparation a une limite d'essais et une séparation initiale plus
petite, compatible avec les répulsions souples du modèle.

Un rendu T6caps a échoué après sauvegarde des données, car sa troisième couleur
n'était pas prévue. Le graphique est reconstruit depuis le NPZ, sans relancer
la dynamique, avec une trace séparée de cette correction.

## 2026-10-23 — revue du projet historique temporaire

Lecture du dossier `temp/` fourni par l'utilisateur. Aucune nouvelle simulation
n'est lancée pour cette revue ; les comptes d'essais et les résultats précédents
restent inchangés. Les performances annoncées dans le benchmark historique sont
rapportées comme documentation de ce projet, pas comme reproductions actuelles.

Les idées, le stack C++17/CMake/vcpkg/SFML/ImGui, l'organisation des couches et
les points de vigilance sont conservés dans `LEGACY_PROJECT_NOTES.md`. Une
sélection de 23 fichiers sources/documents/configurations, soit environ 261 ko,
est sauvegardée sans modification dans `legacy_reference/source/`, avec licence
et SHA-256. Les paramètres d'un checkpoint sont extraits séparément ; les
positions et l'état aléatoire de cet ancien essai ne sont pas recopiés.

L'extrait fourni ne contient pas les en-têtes, scripts et dépendances externes
référencés par sa construction. Le patch contient quelques différences d'en-têtes,
sans reconstituer l'ensemble. Aucune compilation ou validation native n'est annoncée.

Pistes ajoutées à l'arbre, toutes non testées : T7 (recrutement de monomères libres
seulement), T8 (séparation active locale), V7 (réversibilité des liens sous
contrainte), M0 (chimie protégée par perméabilité différentielle et limiteur),
W0 (architecture de moteur partagé). Leurs références pointent vers les fichiers
préservés ; la suite de la recherche ne dépend pas de la présence de `temp/`.

## 2026-10-23 — lot 2 : expression, deuxième génération, fermeture conditionnelle

### Cadrage et choix avant tests

L'utilisateur étend explicitement la cible à traduction, fonctions des chaînes,
fabrication des composants depuis la nourriture et régénération des outils.
L'alternative R, information et fonction dans un alphabet, reste ouverte. La
maturité demandée vise cette richesse commune. Méthode, PRIORITIES.md et
MATURITY.md sont actualisés en conséquence. Le dossier temporaire a été retiré ;
ses références préservées suffisent à poursuivre.

Choix : tester T7 isolément contre T4, E0/E1 pour expression et organisation,
et C0 pour ne pas oublier de dépendance dans la cellule. V7 est différé, car les
fonctions chimiques et leur reconstruction sont des trous de preuve plus larges.

### Tests, contrôles et conclusions

20 nouvelles dynamiques, zéro incident ; manifeste exact BATCH_02.json. Total :
52 dossiers, dont quatre incidents antérieurs sans dynamique. BATCH_02.md et
BATCH_02.png rassemblent les résultats ; aucun ancien essai n'est réécrit.

- T7, t=800, graines 0/1/2 : copies G complètes libérées 3/1/1 ; deuxièmes
  générations complètes certifiées 1/0/0. T4, même durée et graine 0 : une copie,
  aucune génération deux certifiée. Première preuve de possibilité, non robuste.
- L'observateur exige maintenant une filiation complète de toutes les liaisons
  depuis le même parent déjà complet, et non une simple ligation sur une copie.
  Ce test est analytique ; les forces n'ont pas accès aux générations.
- E0, pool F uniquement, 001011 graine 0 : deux F exacts et libérés. Contrôle
  sans gène : aucune ligation. Autre séquence 010010 graine 1 : deux F libérés.
- E1express, préférence native masquée localement pendant l'appariement : un F
  exact libéré. Neuf essais de forme sur chaînes préparées donnent des distances
  finales moyennes 3,235 (000000), 4,754 (010101), 5,010 (000000 sans préférence),
  trois graines par condition. Séquence→géométrie, aucune catalyse démontrée.
- E0mixed, 24 G + 24 F, graine 0 : aucun produit complet. Les voisins recrutés
  de familles incompatibles occupent 78,2 % des interfaces simultanément occupées
  échantillonnées sur le gène initial ; données temporelles corrélées.
- E2 teste seulement une coopération de type entre voisins directement liés.
  Interfaces incompatibles observées : zéro ; graine 0 un F complet libéré,
  graine 1 un G complet libéré. Aucun essai ne montre les deux. La coopération
  aide la cohérence du recrutement mais ne résout pas la coexistence.
- C0 : trois réseaux abstraits, bilans matière et flux de remplacement cohérents,
  quinze contrôles négatifs. Les outils restent des fonctions supposées ; aucune
  conclusion de catalyse, maintien dynamique ou fermeture physique n'en découle.
  Sources et résultats dans abstract_runs/C0_20261023T131308019594Z/.

### Décisions après tests et maturité

Maturité encore précoce : plusieurs étages sont maintenant démontrés séparément,
mais la richesse fonctionnelle et la fermeture matérielle restent ouvertes.
Ouvrir C1 (activité chimique répétée portée par une chaîne), E3 (deux faces pour
éviter la concurrence copie/expression) et T9 (contrôle local des parasites).
Ces trois branches sont proposées, non testées. C1/E3 deviennent P0 ; fabrication
des composants et T9 P1 ; V7/M0 P2. Les quatre outils abstraits de C0 sont une
liste explicite d'obligations expérimentales, pas des types à coder dans le moteur.

Validation : quatre tests mécaniques et trois tests de l'observateur passent.
Le rejeu d'E1zero, graine 0, depuis les sources archivées reproduit exactement
toutes ses métriques. Figure du lot inspectée visuellement. Les références et
SHA des essais sont vérifiés avant clôture du lot.

## 2026-10-23 — W0 : moteur commun et démonstrateurs Windows

Demande utilisateur : un simulateur réutilisable, rapide, avec interface ou sans,
lois modulaires, scénarios et lanceurs par clic. Choix Python/Numba/SciPy/Pygame,
déjà installés, pour conserver l'itération chimique. Le GPU est explicitement
différé ; les noyaux numériques et données sont séparés de l'interface et des hooks.

Les deux boucles actuelles sont remplacées par Simulation. Les anciens points
d'entrée délèguent ; les archives restent intactes. Copie/expression et membrane
ont des hooks distincts ; l'analyse ne fait pas partie des réactions. Voisinage
KD-tree avec cache et marge, filtre exact et paires triées ; référence exhaustive.
Les liens existants restent hors du filtre de contacts. Checkpoint complet avec
PRNG, horloge, liens et état des observations ; reprise à code identique.

Tests initiaux : deux erreurs d'adaptation des ports détectées et corrigées
(masquage du paramètre spatial, masque vide de type flottant). Les fichiers
temporaires Windows nécessitaient l'exécution autorisée des tests hors sandbox.
Ces incidents sont techniques, sans résultat chimique attribué.

Validation : neuf tests du moteur, quatre mécaniques et trois de l'observateur.
Arbre/exhaustif et reprise donnent des états et PRNG exactement égaux. Le test
SDL hors écran compare aussi travailleur graphique et exécution sans interface,
puis vérifie le dessin, la fermeture de fenêtre et la relecture. Captures inspectées.
Le lanceur Windows est essayé depuis un autre répertoire avec le contrôle court.

Quatre essais complets de migration, rangés à part dans engine_runs/ : T7 graine 0
à t=800, une copie G libérée, aucune génération deux certifiée ; V4 graine 0 à
t=300, boucle de 18 ; E0 graine 0 à t=600, un F libéré ; sans gène à t=600, zéro
ligation. Le parcours numérique change par rapport aux prototypes : les anciennes
trajectoires ne sont pas promises, notamment la deuxième génération T7 historique.
Le V6 favorable est fourni comme relecture identifiée, pas réussite migrée nouvelle.

Les configurations sont autonomes et les critères ne commandent pas la chimie.
Le paquet distribuable conserve code, configurations, lanceurs et enregistrements
nécessaires ; Python 3.12 reste requis. Sources, résultats et contrôles sont référencés
dans ENGINE_VERIFICATION.json ; architecture et limites dans ENGINE_MIGRATION.md.

Maturité : premier instrument commun utilisable sur les petits démonstrateurs ;
la chimie reste précoce. C1 et E3 restent les priorités de recherche. Le benchmark
porte sur répulsion + voisinage, pas sur tout le système réactif ni un GPU.

Clôture W0 : les seize tests repassent après les dernières modifications. Le
rejeu complet du V4 migré reproduit toutes les métriques ; les 52 anciennes archives
gardent leurs empreintes. Le ZIP est extrait et son lanceur testé depuis un autre
répertoire, contrôle sans gène court réussi. Les empreintes des membres du paquet
sont vérifiées. Le mode headless n'importe ni Pygame ni Matplotlib.

## 2026-10-23 — préparation du dépôt Git

À la demande de l'utilisateur, ajout des exclusions Python/Numba, environnements,
sorties locales, ZIP de livraison et réglages privés ; conservation des archives,
des figures et du skill de méthode. Ajout des attributs Git et règles d'éditeur,
du guide de premier commit/push, des contributions et de la notice du code tiers.
La licence historique reste à son emplacement ; aucune licence globale nouvelle
n'est choisie par cette opération.

Le moteur actuel contient cinq modules en CRLF et ses checkpoints identifient
les sources par leurs octets. Les sources du moteur et les archives sont donc
explicitement exemptées des conversions Git ; les lanceurs sont restitués en CRLF.
Vérification dans un dépôt temporaire ignoré sous outputs/ : 528 fichiers suivis,
environ 98 Mio, 461 blobs protégés identiques aux fichiers, checkout de contrôle
exact et diff --check propre. Les sorties, caches, ZIP et réglages locaux sont
exclus ; les trajectoires et la méthode de recherche sont incluses.

Le dépôt principal n'est pas initialisé, aucun commit ni push n'est exécuté.
Les commandes pour origin ThomasCabaret/autopoietic-cell-simulator sont fournies
dans GIT_SETUP.md. Aucun nouveau résultat chimique ni changement de maturité.

## 2026-10-23 — correction : données expérimentales séparées du dépôt

L'utilisateur précise que les données ne constituent pas le livrable : le dépôt
doit contenir les lois, le code, les papiers et de quoi reconstruire les expériences.
La politique précédente qui incluait toutes les trajectoires est remplacée.

`.gitignore` exclut désormais les NPZ/NPY, les résultats et images bruts des runs,
les sorties du criblage et du benchmark, en conservant uniquement configurations,
sources exactes et recettes dans les dossiers d'essais. Aucune donnée existante
n'est supprimée ou déplacée. 57 recettes légères sont extraites avec paramètres,
graines et empreintes du code ; quatre décrivent des incidents sans trajectoire.

Le reconstructeur exécute les sources archivées dans un processus isolé et écrit
dans outputs/. Le lanceur de fragments reconstruit son jeu de données s'il manque.
Le ZIP est également une distribution de code et de recettes sans données brutes.
La procédure de contribution et GIT_SETUP.md décrivent cette règle.

Validation dans un nouveau dépôt temporaire : 419 fichiers, environ 2,9 Mio,
aucune donnée brute suivie et toutes les recettes/sources requises incluses.
Ancien moteur, moteur partagé et audit abstrait ont été reconstruits depuis des
dossiers ne contenant que les entrées : mêmes métriques et tableaux enregistrés
que les originaux locaux. Aucun changement des lois ni de la maturité chimique.

## 2026-10-23 — lot 3 : molécules membranaires libres et opération géométrique

L'utilisateur distingue l'assemblage de molécules libres du repliement d'un ruban
préparé, autorise les commits locaux et réserve tous les pushes. Plan conservé
avant tests dans BATCH_03_PLAN.md ; règles durables dans AGENTS.md.

35 nouvelles dynamiques achevées, zéro incident. BATCH_03_RECIPES.json fige leurs
entrées et sources ; BATCH_03.md conserve réglages, résultats et limites. Les
trajectoires et données restent locales ignorées. Aucune ancienne source modifiée.

- V8 : nouveau contact coopératif de quatre billes sur faces saturables. Des
  dimères H-T isolés s'assemblent sans aucune liaison latérale initiale. Les essais
  à 24 molécules échouent, même prolongés. À 36 molécules, espacement 0,75 : trois
  graines ferment au moins une fois mais deux seulement à la fin. L'espacement
  0,65 donne des contours finaux 10+14 / 11 / 12+10 pour graines 0/1/2. Le scénario
  Windows utilise désormais ce départ libre ; l'ancien ruban devient contrôle 07.
- Contrôle à espacements égaux et densité égale : aucune fermeture, graine 0.
  Sans attraction, deux graines sur trois ferment ; sans rupture thermique,
  graine 0 ferme aussi. Ouvrir V9 pour minimalité : ces helpers ne sont pas
  nécessaires à toute réussite. V7 sur V6 reste distinct et non testé.
- La persistance suit le même ensemble de molécules : maxima 275/201/292,
  échantillonnés toutes les unités de temps. Aucune preuve d'étanchéité, de contenu
  retenu ni d'absence d'ouvertures entre images.
- C1 : prototype séparé, chaîne préparée de trois billes simples, angle local
  dépendant du symbole central. Ligation X+Y identique partout ; occupation du
  produit supprime la capture. 001 donne 3/6/2 ligations avec les deux substrats
  capturés, contre zéro pour 010 de même composition et pour les sites non reliés.
  Les produits totaux 3/7/4 contre 3/2/4 ne prouvent pas de gain robuste général.
  Le prototype n'utilise pas encore les F composites produits par traduction.
- Le compteur initial de co-capture exigeait le squelette ; recomptage uniforme
  des supports dans tous les événements, puis compteur clarifié. Validation
  actuelle graine 1 : 7 produits, 6 co-capturés, 6 soutenus par chaîne.
- Provenance : résultats et checkpoints hachent désormais les sources archivées
  au début, même si les fichiers de développement changent pendant un run.

Validation : 24 tests, égalité arbre/exhaustif et reprise pour les deux nouvelles
chimies, gradients et conservation ; interface hors écran et travailleur/headless.
Figures inspectées. Rejeu C1 complet depuis sources figées ; recettes vérifiées.
Maturité encore partielle : assemblage libre démontré, opération géométrique
répétée isolée ; transfert aux F exprimables et coexistence G/F prioritaires,
puis rétention membranaire et fabrication des composants/outils.

## 2026-10-23 — méthode durable : convergence des chimies

À la demande de l'utilisateur, la démarche discutée est inscrite dans le skill
de recherche et relayée par AGENTS.md et CONTRIBUTING.md. Les priorités actuelles
C1/E3 sont explicitement présentées comme tests de convergence.

La méthode impose d'identifier l'objectif du lot (exploration, intégration ou
simplification), de figer un candidat pendant les comparaisons et de tracer ses
variantes. Les bilans doivent conserver des références chimiques, signaler les
régressions et suivre le coût des types, états, ports, motifs et helpers ajoutés.
Les prototypes séparés restent autorisés avec obstacle et test de transfert
explicites. L'intégration devient prioritaire après les preuves isolées.

Trois niveaux sont distingués : modèles séparés, lois identiques testées
séparément, puis coexistence et couplage dans le même bain. Le transfert exige
qu'un produit fabriqué serve réellement au processus suivant sous les mêmes
lois. Une archive reproductible ou un moteur commun ne prouve pas ce transfert.
Les simplifications sont confrontées aux acquis précédents et les changements
de critères doivent être motivés.

Aucune nouvelle dynamique ni preuve chimique dans cette mise à jour documentaire ;
statuts des branches et maturité expérimentale inchangés.

## 2026-10-23 — lot 4 : intégration expression et opération répétée

Lot d'intégration selon la méthode adoptée : transfert C1 aux vraies sous-unités
composites F du hook copy, sans conversion ni second ordonnanceur. Plan avant
essais BATCH_04_PLAN.md ; arbre intermédiaire BATCH_04_DECISIONS.md.

53 dynamiques terminées, zéro incident de simulation ; recettes BATCH_04_RECIPES.json,
1007 empreintes vérifiées. Données complètes locales ignorées ; sources figées
et synthèses conservées. Aucun ancien essai réécrit.

C2A : une seule opération sur F préparé ; C2B réutilise les angles E1 et obtient
5/5/5 opérations préparées. Les supports étant surtout adjacents, C2C retire
l'angle ajouté : 3/4/5 opérations préparées, 3/4/4 pour la permutation de même
composition, zéro pour les sites libres à affinités identiques. Ni supériorité
de séquence ni repliement spécifique démontré. Le transfert aux composites
fonctionne et une primitive supplémentaire a été évitée.

Mais C2C exprimé ne fait que 1/1/0 opération sur chaîne exacte à t=800 ; les
monomères F consomment les substrats entre eux. Les pools de 6/12 F, graine 0
à t=1000, ne rétablissent pas la fonction. C2D réutilise une activation locale
par liaison au squelette pour les substrats : capture/attraction affaiblies sur
les F libres et déliaison accrue. Helper supplémentaire déclaré, pas une règle
de reconnaissance d'outil ou de séquence entière.

C2D 001, graines 0/1/2, G préparé et seulement des F monomères : 2/4/3 F exacts
libérés, dont une même chaîne par essai soutient 3/3/4 produits distincts après
traduction. G010 graine0 : trois F et deux opérations sur une même chaîne.
Sans gène, trois graines : aucun F et aucune co-capture, mais 7/7/8 produits
spontanés. Sans capture, graine0 : quatre F exacts, aucune opération soutenue.
Le bilan global de produits ne prouve donc pas encore une accélération utile.

Références réellement relancées sous D : copie G001011 une fois libérée ;
expression F001011 deux fois et F010010 trois fois. E3 n'est pas résolu : copie
et expression sont encore testées dans des bains distincts. Membrane séparée.
XY ne constitue pas un monomère utilisable ; ouvrir C3 et préserver C2D comme
référence du prochain candidat E3. Maturité : première intégration matérielle
expression→opération répétée, fermeture et richesse générale encore ouvertes.

28 tests passent, dont exclusivité des occupations, gradient, provenance,
arbre/exhaustif et reprise exacte avec activation. Interface hors écran ;
rejeux préparé et exprimé depuis les sources figées. Le premier essai des tests
a rencontré une restriction des fichiers temporaires Windows, puis relance
autorisée réussie ; cet incident n'est pas un échec chimique.

## 2026-10-24 — lot 5 : coexistence, simplification et santé

Demande utilisateur : estimer progression, obstacles en aval et volume des
interventions, puis poursuivre la priorité E3. Ajout PROJECT_HEALTH.md, méthode
de santé dans le skill et AGENTS.md. Évaluation conditionnelle, sans promesse
de délai ; C3 et M0 deviennent les tests de décision en aval d'E3.

30 dynamiques achevées, zéro erreur du moteur ; 596 empreintes de sources
vérifiées. Trois scénarios portent une étiquette longue mais ont réellement
001 : erreur du générateur détectée, entrées conservées, trois essais relancés
sur six symboles sous noms distincts. Générateur maintenant explicite et testé.

E3A à deux faces géométriques fonctionne pour001 : G4/5/3, F3/4/3, coexistence
détachée sur trois graines, max opérations par outil2/3/3. Mais six symboles
restent en fragments et G seul6 graine0 perd sa copie. Prolonger l'association
ne rétablit pas la coexistence longue. Les fragments F libérés ne sont plus
recrutables avec la règle monomères seuls : mécanisme probable à tester, pas
preuve causale. Le port unique sans coopération réussit lui-même une fois sur trois.

E3C réutilise E2 (coopération locale de famille) sous C2D, sans deuxième site :
G3/2/2, F3/2/3, coexistence détachée3/3, max opérations par outil2/3/2. Les trois
graines ont aussi un descendant G génération2 certifié, pour cette courte001.
Retenir cette simplification. Sous coopération, six symboles expriment un F par
graine0/1 mais aucune copie G ; le critère général demeure ouvert.

Les références G seuls6 et F seuls3 sont conservées sous coopération ; le F seul
retrouve exactement les métriques et tableaux C2D. Sans gène, aucune chaîne ni
opération soutenue, mais produits de bain conservés dans les résultats. Le
démonstrateur10 calcule la coexistence ; ses critères passent. Reconstitution
depuis les seules entrées : toutes métriques et trajectoires identiques.

33 tests (26 moteur/chimies, 4 mécaniques, 3 observateur), dont forces réfléchies,
moments, occupation des deux faces, arbre/exhaustif, reprise, détachement et
contrat des scénarios. Skill validé. Lecture des NPZ de synthèse optimisée en
chargeant les tableaux une fois ; cela ne change pas les observations physiques.
Sources historiques et données locales préservées, aucun push.

Maturité : trois fonctions intégrées sur une courte séquence ; constructibilité,
information plus longue, flux utile et membrane restent des risques. Poursuite
justifiée mais budget de quelques dizaines de lots non encore prévisible.
Prochain travail C3 : construire puis incorporer matériellement une première
sous-unité, avant davantage de comportements isolés.

## 2026-10-25 — lot 6 : construction et incorporation de dimères

Priorité C3A : une modification de représentation,19 dynamiques automatisées.
P/R sont des billes persistantes ; partenaires choisis par contact saturé, symbole
du vrai R, sites incomplets inactifs. Moteur partagé et CopyChemistry réutilisés.
Rayon0,58/taux20 figés ; ressources spécialisées activées, lien irréversible.
X/Y et faces doubles non portés et explicitement rejetés. Pas de catalyse par F
dans ce lot, pas de conversion de XY en monomère par étiquette.

G001 préparé et24 supports G +24R libres : copies construites libérées3/5/2.
24 supports F seuls : F construits libérés4/4/4. Mixte24G+24F+48R : G2/0/2,
F1/1/1 ; coexistence simultanée graines0/2, absente1. Formation24/24/24 ou48/48/48.
Sans formation : aucun dimère/chaîne ; sans ligation : dimères mais aucune chaîne ;
sans gène : aucune chaîne. Stock préparé sous mêmes lois : quatre copies G.
Pilote t80 conservé avec une copie encore liée, non compté comme réussite libérée.
Optimisation ultérieure : aucun tirage d'assemblage si tous les ports saturés,
ce qui préserve les RNG des préparés. Sources du pilote distinctes conservées.

Perturbation001011 :48G libres graine0 t800, un G construit libéré. Bain mixte
graines0/1 t1200 : aucune chaîne exacte libérée malgré48 dimères et32/35 supports
incorporés. Longueur/compétition restent ouvertes, aucune réussite généralisée.
Références E3C001 actif et G001011 seul relancées avec option désactivée :
toutes métriques et tous tableaux exactement identiques au lot5.

Audit indépendant399 empreintes,27 377 images matérielles, liens et symboles,
chronologie formation→incorporation, recensement des produits libérés. Reconstruction
depuis sources seules : toutes métriques/tableaux exacts. Démonstrateur11 avec
critères vérifiés et rendu/relecture des vrais rungs.38 tests passent :31 moteur,
4 mécaniques,3 observateur. Première invocation des deux anciens tests comme
modules inadaptée à leurs imports historiques ; scripts directs réussis ensuite.

Santé : progrès concret du noyau matériel, faisabilité globale encore conditionnelle.
C3A ne fabrique pas les pièces grâce aux outils et n'unifie pas encore leur activité.
Prochain C3B : capture P/R, catalyse sous fond faible, libération et incorporation
du même produit ; contrôles de flux. T9 et M0 restent des risques majeurs. Arbre,
priorités, maturité et bilan de santé actualisés. Données locales conservées,
code/recettes/documents versionnés, aucun push.

## 2026-10-25 — lot7 : architecture intégrée et risques précoces

Demande explicite : graphe causal clos, trois synthèses obligatoirement catalysées,
environnements, interactions parasites et insertion de membrane, inventaire et
nombre de billes. Reprise de C0 sans modifier son archive. Nouveau plan C0B à
3 gènes/3 synthétases ; énergie activée fournie, copie/traduction directes.
Les noms EN/EA/EL sont des rôles hypothétiques, pas des types du moteur.

CELL_ARCHITECTURE et trois figures actualisent dépendances ET, import/export,
matière, coûts d'insertion/activation optionnelles, inventaire et taille.16 espèces
cibles,4 sortes matérielles et des états/ports supplémentaires. Complexes et
parasites ne sont pas inclus dans16. Stocks explicites et longueurs supposées
12/24/48 donnent1 020/2 406/6 292 billes avec126/219/458 L de frontière. Le
nominal contient6 gènes et12 outils ; une insertase ajoute gI/EI et320 billes.

Écart majeur identifié analytiquement : V8curved préfère environ11,5 L et
rayon1,53, alors que le nominal demande rayon34,4. Pas de preuve d'instabilité
de toute grande frontière contrainte, mais augmenter units n'en valide aucune.
M1 devient P0 : faible courbure/souplesse, insertion depuis dedans, refermeture
et fuite. Sélectivité N/A de même matière, profils de contact selon liens, débit
surface/volume et extinction de gènes fragmentés deviennent des risques explicites.

Audit conditionnel conserve la matière et détecte10 défauts, dont voie sans
catalyseur, famille isomasse incorrecte, import/insertion/expression absents.
Six tests logiciels passent. Reconstruction source+configuration retrouve toutes
les valeurs ; recette avec hash des deux, nouveau type du reconstructeur partagé.
Résultat complet local, configuration/sources/recette archivées ; gitignore autorise
seulement le config JSON supplémentaire des audits. Aucun fichier historique modifié.

CELL_INTERACTIONS et INTEGRATION_TESTS définissent les criblages futurs I0–I8,
ajout de classes étrangères puis bain complet, concentrations et encombrement,
flux utilisable, séquestration, parasites et fuites. AGENTS impose leur mise à jour.
Maturité moléculaire inchangée : aucune nouvelle simulation n'est présentée comme
preuve. Santé et volume restent conditionnels ; prochaines décisions I0/C3B,
M1/I2–I4 et I1/T9. Arbre/priorités/maturité actualisés. Commit local, aucun push.

## 2026-10-25 — lot8 : composant catalysé puis incorporé

Priorité C3B1. Transfert des captures C2D aux vraies billes P/R de C3A, avec
un taux accéléré pour deux captures sur sites F voisins covalents. Alphabet
inchangé ; motif six billes, capture saturée, exclusion du templating et
libération par occupation du lien. L'aide cinétique reste déclarée et ablatée.
Initialisation explicite des assemblages, distincte des réactions et des outils
nouvellement exprimés. Moteur et ordonnanceur partagés conservés.

19 dynamiques achevées sans erreur ;437 empreintes sources et29 858 images
matérielles auditées. Outil préparé :22/24/23 dimères, G complets3/3/5. Outil
exprimé depuis G001 et six monomères F préparés :34/40/24 réactions certifiées,
3/13/7 produits incorporés. G entièrement issus de ces produits1/2/0, F0/2/0.
Une boucle courte est donc transférée sous mêmes lois ; renouvellement ponctuel
sur une graine, pas maintien sous pertes ni cellule complète.

Sans outil initial :1/0/0 dimère. Sans capture ou sans accélération : aucun,
graine0. Le contrôle délié graine2 réexprime un F puis se réactive : conserver
ce résultat et ajouter délié sans ligation, qui reste sans catalyse. Sans gène :
aucune opération. Ne pas effacer l'activation spontanée d'un contrôle évolutif.
Les deux références C3A et E3C retrouvent toutes métriques et tableaux exacts.

Traceur sur la graine1 :40 réactions locales vérifiées sur les sources figées,
captures réciproques, arête F, distance, vrai partenaire et libération ; mêmes
positions/rungs et métriques. Reconstruction source seule graine0 : tous tableaux
et métriques identiques. Le défaut de tri des clés numériques du comparateur
JSON a été corrigé sans modifier les archives. Test avec IDs9/15/26 ajouté ;
première assertion de test mal placée corrigée également. Version initiale du
traceur et source du traçage réussi conservées dans outputs avec hash. Les
nouveaux traçages utilisent une destination neuve/horodatée.

44 tests moteur/chimies/audit et7 contrôles historiques passent. Démonstrateur12
graine1 : critères vérifiés ; captures dessinées sur les vrais atomes. Travailleur
graphique et headless identiques sur le contrôle court, relecture vérifiée.
Le quota a interrompu la clôture, pas les calculs : reprise des preuves existantes.

Le schéma XYZ/isomères reste une option et non une exigence utilisateur. Comparer
à terme quatre précurseurs réutilisables et assembleur polyvalent en incluant L.
Architecture, interactions, arbre, priorités, maturité et santé actualisés.
Prochain M1 pour grande frontière/insertion/fuite avant de multiplier les réglages
de capture ; I0 et T9/multigène restent ouverts. Risque mémoire des graphes denses
à traiter avant les bains volumineux. Données locales préservées, aucun push.

## 2026-10-26 — lot9 : frontière dimensionnée et audit de localité

24 dynamiques,586 empreintes,7904 images auditées. Frontière219 dimères préparés,
24 libres,48 sondes :534 billes, pas la cellule2406. A et S sans barrière de lien
retiennent les sondes testées3/3 à150 ; contrôle transparent perd10–14/24. À450,
S0 perd1/24. Aucune insertion passive. B échange un contact local à six billes :
deux insertions sur graine2 seulement, persistance6 à150 puis10,5 à450 dans un
suivi sélectionné. Aucun taux de réussite3/3 à450 ni membrane commune G/F.

Pilote conservé avec erreur d'enveloppe : corde virtuelle36 donnant six fausses
sorties. Version2 classe inconnu les fragments à écart>2,5 ; lois inchangées.
51 tests moteur et7 historiques, deux régressions chimiques exactes, reconstruction
source seule et trace des deux échanges exacts. Interface et données parcimonieuses
validées. Démo13. Audit des risques de tricherie et limites des aides explicites.

L'interruption puis discussion utilisateur ouvrent K1 : campagnes différées,
reprise et diagnostic cinétique avant de juger les essais lents. Profil court :
réactions Python dominantes pour le bain membrane ; aucun facteur×10 revendiqué.
Arbre, priorités, maturité, santé et architecture actualisés. Aucun push.

## 2026-10-26 — lot10 technique K1 : exposition et campagnes différées

Contrôleur de campagnes et travailleurs sur Simulation.advance, sources figées,
verrous OS, statut atomique, arrêt/checkpoints/reprise, export/restauration source
seule. Aucun nouveau scheduler de réactions. Compteurs pré-réaction de rencontres
et faces admissibles pour membrane, sans PRNG ni écriture chimique ; fenêtres,
premiers passages censurés et Kaplan–Meier par lois/protocole/horizon.

58 tests logiciels et7 historiques passent. Reprise intermédiaire exacte, y
compris exposition, worker figé, pas de redémarrage des terminés, altération
refusée, ancienne trace «running» reconnue interrompue si verrou absent.
Les hazards exacts et l'éligibilité des autres hooks ne sont pas prétendus.

Plan B/Bsimple,3 graines chacun,t1500,2 travailleurs, checkpoint60s, sans trajectoire
complète. Recette de campagne à conserver ; analyse différée, aucune conclusion
chimique anticipée. Pas de GPU ajouté ni facteur×10 mesuré. Données locales,
commits locaux uniquement.

Campagne K1 effectivement lancee : campaign_20261026T102204813246Z, commit103dbbd,
six taches a1500, deux travailleurs actifs et quatre en attente au controle.
Recette source seule conservee ; aucune conclusion chimique avant analyse.
Lancement persistant hors bac a sable verifie apres controle Windows court.

## 2026-10-26 — debriefing K1 acheve

Six essais complets,168 empreintes et18006 observations verifiees. B insere1/2/5
dimeres a1500 : la duree150 masquait deux attentes longues. Fermeture au seuil
seulement2/3 et graine0 non classable28% du temps ; retention globale non prouvee.
B sans barriere de lien perd2-4/24 sondes, insertion0/1/0 : simplification refusee
pour ce couplage long. Beaucoup de rencontres, rares geometries admissibles.
Prochaines decisions : controle long sans echange et ouvertures, puis integration
avec vrais precurseurs/composants G/F sous lois communes. Aucun blocage de principe
etabli, volume restant incertain. Pas de nouvelle campagne pendant le debriefing.
Voir BATCH_10_RESULTS.md ; donnees locales preservees.

## 2026-10-26 — préparation lot11 M1R

Contrôles longs B versus échange désactivé,0/1/2,t1500. Même physique et même
initialisation que K1, barrière conservée. Nouveau BoundaryAudit analytique,
sans contour inventé ni rétroaction. États inconnus décomposés, épisodes et
extrémités mesurés ; pas d'inférence d'étanchéité depuis proximité géométrique.

63 tests+7 historiques passent ; reprise exacte avec audit, primaire inchangé.
Pilote B0 à150 : toutes positions, PRNG, chimie et métriques de la référence
lot9 exactes.301 échantillons,260 fermés,38 ouverts classables,2 grand écart,
1 fragmenté ;35 ouvertures observées avant le premier échange. Pas de conclusion
sur les défauts tardifs. Census vérifié, preuve et données dans outputs/batch11.

Plan/rapport/postprocesseur conservés. Six tâches longues à lancer après commit,
recette figée avant calcul. Aucune nouvelle loi, aucune fonction G/F intégrée.
Maturité inchangée ; décision après les contrôles, pas de helper supplémentaire.

Campagne M1R lancee : campaign_20261026T165544113247Z, code0850065,
six taches a1500, deux actives et quatre en attente au controle, aucune erreur.
Recettes source seule du pilote et du lot conservees ; resultats non analyses.

## 2026-10-27 — analyse M1R et trace locale M1G

Six controles completes, census et references B verifies exactement. Sans echange
la fermeture est0.844-0.851 avec peu de periodes inconnues ; B0 degrade surtout
apres787.56 jusque1236.11.897 images ont une extremite isolee au-dela1.35, contre
aucune avant/apres pour B0. Le defaut merite une intervention de motif local,
pas une pression globale ou une reinterpretation favorable du confinement.
Trace selectionnee B0 jusque800 sur sources figees, cas productif et cas
defectueux compares ; aucun filtre dans la dynamique a ce stade. Hypothese
disponibilite des faces a confirmer. Cout scientifique : diagnostic reduisant
un risque, pas nouveau modele viable. G/F et fabrication de L restent separes ;
aucun blocage de principe ni delai fiable en nombre de lots.

## 2026-10-27 — M1G1 apres trace locale

Trace B0 jusque800 exacte : deux evenements, arrivee libre puis arrivee deja
liee ailleurs. Garde geometrique rejete car il interdirait les deux. Ancien
driver et sources conserves, version portable releve les deux occupations.
Nouveau garde symetrique sur autres ports existants, aucun taux/rayon/type
ajoute. Pas de reparation automatique ni identite biologique. Premier test
mal calibre corrigé : autre reaction legitime, pas defaut de loi.
67 tests logiciels et7 historiques passent. Pilote choisi2 a150 sans echange
ni insertion, brut7.50 et sous garde7.08 temps-face : pas de succes affirme.
Trois graines a1500 prevues avant calcul, comparaison aux temoins M1R conserves.

Campagne G1 lancee : campaign_20261027T074404542747Z, code8d73330, trois
graines a1500, deux actives et une en attente, aucune erreur au controle.
Recette exacte preservee ; aucun succes chimique anticipe.

## 2026-10-27 — clôture G1 et intégration J0

G1 terminé3/3 à1500, sources/census/durées/échanges vérifiés. Insertion1/2/2,
persistants1/2/1, fermeture0,840/0,841/0,759. Aucune fuite observée,1,2–3,1%
d'inconnu. Critère conjoint2/3 comme B, aucun candidat dominant. Pas de nouveau
garde : priorité au transfert matériel, résultats dans BATCH_12_RESULTS.md.

AGENTS/skill renvoient au contrat DESIGN_PRINCIPLES : localité, simplicité,
expressivité distinctes ; incompatibilités aval à tester tôt ; modularité du code
sans garantie chimique ; division future sans priorité ajoutée. Exigences rendues
explicites pour toute reprise. Nouveau hook J0 dans le même ordonnanceur : P/R et
L mécaniquement couplés, contact selon lien local, température unique0,08,
mobilités héritées. Aucun transfert de matière par convertisseur externe.

Pilotes graine0 natif/froid60 et bain/sansL20 sans erreur ni réaction ; bain sans
contact encore. Résultats courts censurés, pas preuve d'inactivité. Plan quatre
conditions × trois graines à400 avant résultats. Réactions L et P/R encore
disjointes ; production L par F et diversité restent des verrous de représentation.

Campagne J0 lancée : campaign_20261027T113835658766Z, code55bcbf9,12 tâches
à400 sur sources figées, deux travailleurs. Recette source seule conservée.
73 tests uniques logiciels et7 historiques passent ; archive de distribution
avec hashes vérifiés. Aucun succès chimique attribué avant analyse du lot.

## 2026-10-27 — bilan numérique et ordre de grandeur demandé

J0 terminé12/12 sans erreur. Analyse figée et première lecture : F natif1/1/1,
froid0/0/0, bain0/0/0 à400 ; aucun produit catalysé incorporé dans les12 essais.
Contacts/passages libres3/3 ; aucun passage lié observé, exposition liée nulle
dans une graine. Pas de conclusion d'étanchéité ou d'impossibilité à froid.

Benchmark complet court reproductible ajouté, sources/configs brutes dans
outputs/performance/cell_workload_20261027T115831264333Z :588/1020/2406/6292
billes,708/705/315/122 pas/s, sans rendu. Charges longues préparées synthétiques,
pas trois synthétases ni une cellule viable. Équations et métrique T50 par famille
dans NUMERICS_AND_RENEWAL.md, protocole de convergence numérique ajouté à
KINETICS_AND_PERFORMANCE. Aucun T50 global mesuré ni optimum de nourriture.
Code chimique inchangé, pas de nouvelle campagne ; audit détaillé J0 restant.

## 2026-10-27 — démarrage GKA, diagnostic génétique

Priorité à l'incompatibilité froide, pas nouvelle fonction. Les anciens historiques
ont déjà des appariements, maxima4/2/4 sites à froid contre6/6/6 au chaud. Audit
pré-réaction ajouté sans PRNG ni retour vers les lois, avec census d'exclusions,
motifs de ligation et supports catalytiques. Six témoins natif/froid à400 prévus,
sources figées et comparaison exacte des métriques/positions/PRNG/chimie.
Suite ciblée6 tests positive ; suite complète d'abord bloquée par permissions
sur les répertoires temporaires du sandbox, relancée hors sandbox à code identique.
Aucune régression ou réussite chimique déduite de cette erreur d'environnement.
Relance complète :79 tests logiciels et7 historiques passent avant gel.

GKA campaign_20261027T122747493430Z achevé6/6, code0c08498. Toutes métriques,
positions, PRNG et chimie exactement conformes aux six témoins J0. Diagnostic :
zéro double appariement froid0/1 ; froid2 une liaison sans trimer. Correction
documentaire du cycle à200/15, toujours celui des recettes et calculs.

Décision J1 : départ construit avecF001 contre sa géométrie déliée, six dimères
F initiaux conservés. Six paires vérifiées : positions/PRNG/rungs/bits identiques,
deux liens seulement diffèrent. Pilotes0 à200 :3 catalysés contre0, aucune
incorporation ou nouveau F. Plan12 tâches1200 avec/sans membrane fixé avant
résultats, aucune nouvelle loi. Prolongation froide3200 non choisie maintenant.

J1 lancé : campaign_20261027T144451586423Z, code39fead3,12 tâches1200,
deux travailleurs, sources figées et recette versionnée. Tests79+7 et reprise
des13 contrôles campagne/couplage réussis. Aucun succès de transfert anticipé.

## 2026-10-27 — lot15, clôture J1 et contrôle spatial J2

Reprise avec6 J1 achevés ;12/12 terminés pendant le traitement, aucune erreur.
Census vérifié : hashes, événements, vraies IDs P/R, durées et102 billes P/R.
Préparés froids18/38/21 catalysés,2/5/1 incorporés ; G0/1/0 et F0/0/0.
Délié froid1 : F1,18 actes exprimés et1 incorporation. Bains préparés13/13/11,
zéro incorporation dans les6 bains, frontière encore fragile.

Le census distingue monomères éloignés et fragments ; zéro fragment F délié
non cible dans les bains. Choix J2 : séparer domaine global et présence de L,
pas nouvelle loi. Paquets/RNG vérifiés sur6 paires open/compact et contre les
bains J1. Réglage de frontière globale sans L seulement ; défaut exact au
hook J1 archivé.86 tests logiciels+7 historiques passent.

Homéostasie faible explicitée dans HOMEOSTASIS.md et contrat de reprise ; pas
de régulation implémentée ni essai de maintien revendiqué. Plan12 témoins J2
à1200 fixé avant résultats, sources à geler après commit, données locales.

J2 lancé : campaign_20261027T162612551317Z, codeb0e104a,12 témoins1200,
deux travailleurs et recipe source seule conservée. Pas de résultat anticipé.

## 2026-10-27 — lot16, J2 terminé et inventaire J3

J2 achevé12/12, sources et census vérifiés. Préparés ouverts10/14/22 catalysés,
0/0/1 incorporés ; compacts38/35/29 et1/2/2. Aucun G/F nouveau dans les12.
Choix J3 : inventaire construit×1/8/16, même chimie et mêmes gènes001, avec/sans
L, plus ablation du boostK16.21 tâches1200 prévues avant résultats. Paquets/PRNG
initiaux vérifiés sur9 paires et3 ablations, intérieur à la vésicule.

Observateur corrigé pour certifier tous les G préparés complets, auparavant
seul le premier ; cas simple exact à la référence. Census multi-template et
comparaison de membrane sur grille régulière pour éviter le biais des callbacks
de ligation. Source physique inchangée. Pilote K16,t2 :2118 billes, stable,
3 actes, aucune incorporation ou chaîne nouvelle, aucun contact avec L.

Demande utilisateur d'entrée/sortie au bord préservée dans OPEN_BOUNDARY.md :
flux réglable, pas de concentration interne garantie. Capacité dynamique des
tables/IDs encore à réaliser ; pas de source implémentée pendant ce lot.

J3 lancé : campaign_20261027T192723206222Z, code3d2cb79,21 tâches1200,
deux travailleurs, source figée et recette versionnée.91 tests logiciels et7
historiques passent ; données de campagne locales. Aucun succès long anticipé.

## 2026-10-28 — lot17, bilan J3 et contrôle temporel N1

J3 achevé21/21, aucune erreur ; sources, événements, matière et checkpoints
vérifiés. K16 avec L :331/401/313 catalysés,18/18/26 incorporés ; G1/1/0 et
F0/1/1 nouveaux, tous les G/F nouveaux de ces bains entièrement construits.
Un F exprimé effectue4 actes dont2 produits utilisés (graine2) ; graine1 G+F
sans activité de ce F observée. Aucun essai ne ferme tous ces critères ensemble.
Sans boost :0/1/0 actes, aucune incorporation/nouvelle chaîne.

Fermeture sur grille0,5 :0,732/0,791/0,786, pas de frontière robuste. Fragments
F déliés10/16/6 unités, stocks monomères élevés ; restriction de recapture
structurelle, sans démonstration de causalité dominante. Pas de nouveau balayage
de densité. N1 conserve la chimie et raffine dt/2,dt/4 avant une intervention
T9. Six essais à1200, trois témoins J3 réutilisés, réaction5dt et observation0,5.
Critères/alertes déclarés dans BATCH_17_PLAN.md avant nouveaux résultats.

Avant gel N1 :91 tests logiciels+7 historiques, six initialisations appariées
vérifiées,31 modules simulator byte-identiques à J3 et rejeu court exact.
Pilote finest dt0,0005,t2 :3 produits, aucun transfert/chaîne/contact avec L,
seulement démarrage technique. Zéro dette chimique ajoutée.

N1 lancé : campaign_20261028T073131539788Z, code770d9b3, six tâches1200,
deux travailleurs, recette source seule exportée. Premier statut : deux actifs,
quatre en attente, zéro erreur. Comparateur partiel exécuté : sources/candidats
cohérents, cohortes explicitement incomplètes, aucune convergence revendiquée.

## 2026-10-28 — lot18, exploration automatique bornée

État initial N1 :2 achevés,2 actifs,2 en attente, sans erreur. Résultats partiels
moyens277/335 actes,9/16 incorporés,G1/0,F0/2 ; pas de médiane de cohorte validée.
Demande utilisateur : programmer les décisions calculables et réserver
l'interprétation aux mécanismes. Contrat AUTOMATED_EXPLORATION.md référencé par
AGENTS et DESIGN_PRINCIPLES ; budgets, branches et échecs doivent rester tracés.

Préparation du suivi figé N1→analyse→N2 si alerte de niveau fin. Six essais
maximum supplémentaires, deux travailleurs après libération de N1, mêmes lois,
pas de nouvelle chimie automatique. N2 isole cadence réaction0,005/0,01 à
dt0,0005 ; défaut du moteur conservé exactement. Les deux premiers résultats
N1 étaient connus au choix de ce suivi, sélection déclarée, pas validation aveugle.

Pendant validation : N1 termine6/6. Rapport numerical_analysis_20261028T162258944076Z,
aucune alerte médiane, donc N2 non déclenché selon protocole. Au pas fin F1/1/1,
G0/0/0, actes exprimés3/2/0 dont1/0/0 produits utilisés ; frontière fine1
fermeture0,426/enveloppe0,703, événement gardé malgré médiane sans alerte.
Incorporation médiane18→16→12 : baisse cumulée33%, pas de certificat numérique.

Diagnostic T9_gates_20261028T171634136779Z : six contacts idéaux, un tick réel
conditionné sans intégration ; retirer monomer_only_capture laisse le blocage
F déjà lié par family_degree. Recapture des extrémités peut séquestrer les outils
complets aussi ; prochain motif à concevoir/tester avec ces deux contrôles.
99 tests logiciels+7 historiques passent ; pilote N2 every20,t2 stable,
2 produits, aucun transfert/chaîne/contact L. Aucun nouveau succès chimique.

Suivi figé followup_20261028T172046220951Z, code4fa4442, exécuté sur les vrais
résultats : needs_interpretation/run_N2=false, aucun travailleur N2 lancé.
Rapport/hash de décision archivés localement ; manifeste source BATCH_18_FOLLOWUP.
Recette N2 conditionnelle exportée, six tâches dormantes. Pas de campagne longue
active à la clôture ; prochaine étape de conception T9 avec contrôles outils.

## 2026-10-29 — méthode, loupe microscopique motivée

Demande utilisateur inscrite dans AGENTS, DESIGN_PRINCIPLES et
KINETICS_AND_PERFORMANCE : diagnostic temporaire, ciblé spatialement et dans
le temps, éventuellement déclenché par un événement. Usage au jugement de
l'agent pour vérifier un mécanisme à la conception ou expliquer un comportement
émergent inattendu, avec question, budget et décision motivés. Pas de capture
systématique ni de nouvel outil sans besoin. Observation passive, contexte et
reproductibilité préservés ; arrêter l'instrumentation sans supprimer les preuves.
Modification documentaire seulement, aucune simulation lancée, maturité chimique
et priorité T9 inchangées.

## 2026-10-29 — GUI1, interface durable prioritaire

Demande utilisateur : développer maintenant le client final d'exploration et
de futures animations de vulgarisation, avant nouvelle démo intégrée. Paquet
visualizer indépendant du moteur : Qt/PySide6 pour la fenêtre, ModernGL3.3 pour
le rendu instancié, processus propriétaire de la simulation, snapshots copiés.
Navigation, pause/pas/rythme sans modification de dt, opacités, sélection/suivi,
partenaires liés directs, flashes des transitions, journal et export PNG livrés.

La GUI est explicitement en cours de finition, pas déclarée terminée : relecture,
export vidéo, inspection de ports/contacts et regroupements moléculaires à venir,
courbes facultatives ensuite. Aucun nouveau candidat chimique ni démonstrateur
intégré créé. Les fichiers de recherche et recettes antérieurs sont préservés.

Sept tests de contrat passent : caméra, filtres/physique séparés, tampon d'événements,
sélection après rupture et processus réel pause/pas/rythme, positions/RNG exacts.
Test Qt/OpenGL natif passé, captures dans outputs/visualizer_qa ; test synthétique
Intel UHD1920×1080,100000 billes+99999 liens≈26,4ms, trois appels de rendu, sans
simulation/IPC/sélection. Sources et résultats bruts locaux, pas de hausse de
maturité chimique. Statut détaillé : docs/VISUALIZER.md.
Les attaches virtuelles historiques sont rendues à leur position réfléchie,
avec contrôle dédié ; aucun changement du moteur scientifique.
Validation finale :106 tests logiciels et7 historiques réussis, plus le test
Qt/OpenGL natif. Distribution source reconstruite avec vérification des hashes,
sans bibliothèques installées ni captures/résultats d'essais dans Git.
Limite explicitée : la comparaison de liens après chaque tick voit les
transitions entre ticks, pas tous les intermédiaires d'un même tick. Flux de
mutations natif prévu dans la finition, aucun événement intermédiaire inventé.

## 2026-10-29 — GUI2, catalogue des démos représentatives

L'utilisateur reporte vidéo et outils avancés : priorité au minimum visuel et
aux démos jouables maintenant. Catalogue versionné de quatre scènes scientifiques,
six préréglages : J3 K16 avec L, graines2/0/1 (2118 billes) ; circuit matériel
C3B1 graine1 (102) ; copie T7 graine0 (108) ; membrane V8 libre graine0 (72).
Les états initiaux résolus et signatures modèle/graine/horizon/moteur/chimie
correspondent aux entrées archivées ; aucune loi ou structure supplémentaire
imposée. J3 graine2 sélectionnée pour illustrer un transfert, pas une robustesse.

Menu Démos et fiche dédiée : matériel préparé, phénomène à observer, aides,
limitations et référence. Compteurs copiés des observateurs existants, nouveaux
G/F hors préparés, avec horloge de mesure passive. Lecture au maximum proposée
mais départ en pause ; ralentissement seulement du déroulement, jamais de dt.
Les sessions gardent leur configuration et leur fiche dans les sorties locales.

Tests des six états, des signatures et des compteurs réussis. Test natif Qt :
les six actions ouvrent les bons scénarios en pause ; lecture/pas/arrêt J3 et
recommencement retrouvent exactement l'état initial. Captures dans outputs/demo_qa.
Contrôle GUI court, pas de nouveau résultat chimique ou de campagne entière
réexécutée. Les dégradations et les capacités manquantes restent déclarées.
Validation finale :111 tests logiciels et7 historiques passent, ainsi que le
test natif des six choix. Les31 empreintes du moteur sont gardées au catalogue :
un changement de code demande une révision explicite avant de réutiliser les
étiquettes des démos. Aucun changement du paquet simulator ni données brutes
ajoutées au dépôt ; vidéo et fonctions avancées reportées.

### 29 octobre 2026 — option d'un nouvel assemblage fonctionnel

Précision méthodologique utilisateur : comparer une amélioration des lois à
un nouvel outil moléculaire assemblé, par exemple une insertase. Cette option
existait déjà dans CELL_ARCHITECTURE.md (EI/gI), sans réalisation démontrée.
DESIGN_PRINCIPLES.md impose désormais une proposition motivée : mécanisme local,
coût complet de reconstruction, alternatives et test discriminant. Attendre
le feu vert utilisateur avant sa mise en œuvre. AGENTS.md relaie cette règle ;
le skill de recherche impose déjà la lecture du contrat de conception.
Aucune nouvelle protéine, loi, campagne ou branche expérimentale introduite ;
priorités scientifiques et maturité inchangées.

### 29 octobre 2026 — lot19, P10 distribution complète des produits

Demande utilisateur : un brin de dix symboles, réserve abondante, observer toute
la population et non les seules copies réussies. BATCH_19_PLAN.md fixe le test.
Nouveau PopulationAudit optionnel et passif : séquences canoniques, longueurs,
stocks, produits nouveaux/libres, matériel initial et contacts de cœur.
Campagnes/sauvegarde/reprise réutilisées ; zéro nouvelle loi ou protéine.

Deux pilotes à50 terminés, environ1000 pas/s, fragments avec97% de monomères
encore libres et aucun exact à cette date. Pas d'échec définitif déduit.
Deux témoins dilués ajoutés prospectivement après observation de contacts de
cœur fréquents. Campagne P10 figée puis lancée en arrière-plan, dix essais à3200,
deux travailleurs, checkpoints30s, pas de trajectoire dense. Recettes de sources
préservées, voir BATCH_19.md ; priorités, arbre, santé et maturité actualisés.
À800, les deux premières graines G ont chacune un exact nouveau détaché contre
27/24 fragments, avec308/324 monomères libres sur400. Lecture intermédiaire,
cohorte incomplète ; pas de plateau final déclaré.115 tests logiciels et7
historiques passent après relance hors du bac à sable Windows qui bloquait
les écritures temporaires. Les recettes et contrôles de passivité sont conservés.
