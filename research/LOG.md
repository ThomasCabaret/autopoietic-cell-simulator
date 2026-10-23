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
