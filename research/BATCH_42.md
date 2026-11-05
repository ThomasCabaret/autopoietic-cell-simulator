# Lot42 — calibration explicitée et capture coopérative locale

4 novembre2026. [Plan](BATCH_42_PLAN.md) · [recettes](BATCH_42_RECIPES.json)
· [pilote](BATCH_42_PILOT.json) · [contrat de calibration](CAMPAIGN_CALIBRATION.md).

**Clôture ultérieure : MX2 terminé12/12, neuf conditions passent ; voir [lot43](BATCH_43.md).**
Les lectures intermédiaires ci-dessous sont conservées comme historique.

## Clôture MX1 et portée du résultat

12/12 achevés, aucune erreur. Rapport figé local
`outputs/mixed_synthesis_followups/followup_20261104T192816403023Z/report_0.json`,
SHA256 `c37c60954d8122f21927dfe9865292e62e51a90302f04fb858a5786710cb8807`.
Deux conditions refusées : médianes G/F au moins moitié du témoin uncaptured.
Six passent : référence noHT, usage et synthèse L dans mêmes bains, outils
entièrement alimentaires→L sur2/3, nogene, fausse catalyse, invariants.

| À1200, graines0/1/2 | Mixed | Uncaptured |
| --- | --- | --- |
| Nouveaux G libérés |0 /2 /0|7 /7 /12|
| Nouveaux F libérés |2 /5 /1|9 /9 /10|
| F entièrement alimentaires |2 /3 /0|6 /7 /8|
| L produits |9 /20 /8|0 /0 /0|
| L produits par F alimentaires |3 /4 /0|0 /0 /0|
| L neufs avec contact ultérieur |7 /16 /7|0 /0 /0|

Les outils initiaux demeurent ; pas de membrane cellulaire dans MX1. La
régression est réelle à conditions/horizon fixés, mais elle ne démontre pas
que les mêmes lois ne fonctionneraient jamais dans d’autres conditions.

## Audit sans nouveau calcul : stocks, temps et occupation

`experiments/mixed_calibration.py` lit les vrais événements et checkpoints,
vérifie la reconstruction des partenaires P/R finaux et pondère les occupations
par le temps entre observations irrégulières. Données locales sous
`outputs/diagnostics/MX1_calibration_20261104T201916618397Z`.

| Stock non assemblé final mixed | Graine0 | Graine1 | Graine2 |
| --- | ---: | ---: | ---: |
| P_G |28|16|22|
| P_F |20|12|24|
| R0 |26|14|24|
| R1 |22|14|22|
| H et T, chacun |15|4|16|

Les trois bains contiennent encore tous ces types de précurseurs. « Non
assemblé » inclut les atomes capturés : cela écarte une pénurie globale, pas
un manque local d’accès. Uncaptured finit avec0–1 P/R de chaque type, quasiment
épuisés. Ajouter simplement plus de réactifs n’est donc pas la correction
prioritaire justifiée pour mixed ; une exploration de densité peut rester utile
plus tard, séparée d’un changement de stock à concentration constante.

Sur900–1200, mixed forme encore5/9/3 composites P/R et6/6/4 L. Dernières
naissances PR1188,63/1188,53/1044,76 ; L1195,65/1197,08/1040,62. Le1200 n’est
pas un plateau. Les temps sans événement restent censurés. Les doubles motifs
croisés occupent99,6/98,1/99,1% du temps échantillonné des doubles occupations.
Ce n’est pas la fraction des tentatives : un couple productif disparaît vite
après réaction, contrairement à un couple inerte. La mesure motive un diagnostic,
pas un calcul de probabilité d’échec à partir de neuf couples de types.

Repères d’échelle issus du code : aire108 ; stocks initiaux P_G31/P_F30/R0 31/
R1 30/H24/T24, soit concentrations0,287/0,278/0,287/0,278/0,222/0,222 par aire.
Langevin masse1/damping0,1/T0,08 donne persistance10 et D libre asymptotique0,8.
Mode spatial lent idéal sur12≈18,24, **pas temps de mélange du bain réactif**.
Les données MIX2 mesurent effectivement voisinage/occupation/mémoire, avec des
conditions différentes et des censures. Aucune garantie universelle de mélange.
Cycle200/15 :1200 couvre six cycles ; pilote100 précède la fenêtre externe185.

## Loupe bornée : la déliaison n’est pas l’évasion

`experiments/inspect_mixed_capture.py` rejoue exactement les sources MX1.
Premier motif croisé à5,15, sites39/40, six billes fixes, fenêtre20,401 frames.
Deux déliaisons à12,67 et24,03, sans recapture dans le même tick ; mêmes atomes
revus liés au plus tard12,95 et24,75, soit0,28/0,72 après. Les bornes sont
échantillonnées à0,05, pas temps exacts d’événement. Cela soutient la persistance
par recapture dans cet exemple ; pas une fréquence générale ou piège éternel.
Le contrôle sans loupe retrouve positions, vitesses, chimie et PRNG bit à bit
jusqu’à40. Preuves locales conservées sous
`outputs/diagnostics/MX1_capture_loupe_20261104T202329133143Z`.

## Avancement : coopération de sites plutôt que nouveau taux

Option `capture_cooperativity` (défaut faux) : un premier ligand conserve son
affinité large. Lorsqu’un site directement lié est occupé, le recrutement et
l’attraction du voisin respectent la compatibilité P–R/H–T déjà nécessaire à
la jonction. Même règle pour substrats génétiques et lipidiques. Aucune identité
de protéine/gène, contour, origine ou concentration dans cette décision.

Coût : une condition coopérative locale, motif borné six billes, zéro nouveau
type, état chimique indépendant, port, gène, outil, taux ou constante numérique.
Ce helper change les commutations de potentiel ; il n’établit pas à lui seul
l’énergie fermée ou un répertoire de fonctions programmables. Delta H/T étendu
aux sites directement liés dont l’affinité change à la libération, avec leurs
voisins spatiaux dans les mêmes rayons. P/R garde son helper historique.
Forces et probabilités utilisent la même condition ; pas de suppression globale
des mauvais produits ou réparation selon un objectif. Pas nouvelle protéine.

Cinq contrôles de mécanisme passent : recrutement large/voisin compatible/
réouverture après libération ; mauvaise capture refusée sans supprimer d’atomes ;
forces réciproques et gradient ; delta exact incluant le voisin d’un site libéré ;
passivité, arbre/brute et reprise exacte. L’audit de stocks et la porte MX2 ont
leurs tests propres. Cinq préfixes archivés MIN1R/MIN1M/MD2/L3/MX1 àt5 sont
physiquement exacts quand l’option est désactivée ; seul le champ faux ajouté
à la configuration MX1 est normalisé pour la comparaison.
Suite complète :225 tests passent, dont reconstruction d’inventaires et porte
prospective. Les états initiaux des démos restent ceux validés de MIN1M ;
catalogue recertifié, sans adoption anticipée de MX2.

## Pilote et questions de MX2

Pilote unique coopératif graine0 à100,46,765s,198 billes :12 composites P/R,
5 L, zéro motif croisé observé, zéro invariant violé. Aucun G/F complet libéré
à cet horizon précédant la première fenêtre externe : pas de critère négatif
sur ces chaînes. T finale0,108, déplacement max par pas0,00761 ; pas preuve
d’isothermie alimentée, de viabilité ou de maintien. Aucun réglage sélectionné
dans une grille après ce pilote.

MX2 lancé12 essais, reference/cooperative/nogene/noHT×3, t2400, mêmes stocks,
2 travailleurs, checkpoints30s, budget4h, rapport puis arrêt. La référence
longue doit reproduire l’intégralité des historiques/événements MX1 jusqu’à1200.
Les anciens refus sont conservés. Tous les nouveaux cas sont au même horizon ;
ces références prolongées sont sélectionnées, pas répétitions indépendantes.
Rapport automatique avec stocks/fenêtres : délai, épuisement et effet de loi
deviennent lisibles ensemble. Statut **cooperative_synthesis_status.bat** ;
pause/reprise explicite par **stop_cooperative_synthesis.bat** /
**resume_cooperative_synthesis.bat**. Pas de deuxième phase, retry ou promotion.

Lecture intermédiaire des checkpoints, graine0 seulement : au même1200,
cooperative G5/F10/L24, dont1 L via F entièrement alimentaire ; reference
G0/F2/L9, dont3 L via F alimentaire. Les quatre historiques/événements reference
à1200 sont déjà égaux à MX1 après normalisation JSON (tuples/listes de la
mémoire et du fichier diffèrent sans changement scientifique). Les essais
continuent à2400 ; aucun verdict global, fréquence de réussite ou promotion
déduit de cette graine sélectionnée. Le nombre inférieur de L faits par F
alimentaires peut refléter leur arrivée après consommation H/T : le rapport
final doit lire ce transfert avec les stocks et leur chronologie.

Maturité : diagnostic de concurrence plus précis et candidat local construit,
pas de palier cellulaire accru par un pilote. Le transfert F alimentaire→L
existe sur2/3 MX1 mais le débit génétique reste insuffisant dans ce domaine.
Prochain jalon : interpréter MX2 et sa calibration, puis membrane renouvelée/
insertion. La cible reste le maintien sous pertes et perturbations ; homéostasie,
protection, export, alimentation ouverte et information utile restent ouverts.
