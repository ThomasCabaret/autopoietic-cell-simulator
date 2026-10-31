# Lot31 — pertes locales, recyclage matériel et comparaison RV1

31 octobre2026. [Plan figé](BATCH_31_PLAN.md), [recettes](BATCH_31_RECIPES.json),
[checklist avec progrès](CELL_CHECKLIST_COMPACT.md). Candidat exploratoire ;
MD2/Langevin reste la référence et les démos actuelles restent inchangées.

**Bilan final :12/12 terminés, zéro erreur, aucun calcul encore actif.** Porte
RV1 refusée automatiquement ; les quatre transferts MD2 restent non lancés.
Le recyclage matériel fonctionne dans un petit bain mais son compromis avec
la protection n'est pas validé. Aucune adoption dans les démos.

## Ce qui est implémenté

Option `chemistry.bond_turnover`, aussi accessible dans la génétique du bain
couplé. Chaque lien G–G/F–F peut se rompre ; un appariement ou un ligand sur
l'un des deux sites peut réduire son taux. Un composite P–R sans voisin de
squelette, appariement ni ligand peut ensuite se dissocier. Aucun parcours de
chaîne, longueur, nom de gène ou objectif de population dans ces décisions.
Les atomes gardent positions, vitesses, identités et symbole du R réel.

Les précurseurs récupérés sont les entrées déjà reconnues par l'assembleur
P/R. Leur profil membranaire redevient celui des atomes libres par le mécanisme
libre/lié existant ; aucun test « déchet » et aucune suppression de matière.
Quatre taux et un facteur de protection ; aucun nouveau type, port, gène,
outil ou particule. Les commutations de potentiel ne sont pas calibrées en
énergie : aide cinétique déclarée, pas thermodynamique à bilan détaillé.

Un census passif dédié remplace les compteurs de filiation irréversible pour
ce candidat. Il suit les ruptures/formations dans leur ordre réel, les deux
IDs P/R effectivement libérés puis réassemblés, et leur réincorporation dans
un squelette. Le stock courant **inclut** les structures préparées et est
présenté comme tel dans la GUI. Pas de « nouveau F exprimé » ni de génération
certifiée déduits d'un recyclage d'IDs. Les états de l'observateur sont repris
sur checkpoint ; ses labels ne sont jamais lus par les réactions.

## Vérifications et portée

Six tests RV1 : validation de configuration ; taux nuls sans changement des
positions/PRNG/chimie ; protection locale et dissociation des atomes ; contrôle
géométrique du trajet polymère→P/R→composite à partenaire R échangé→ligation
templée réelle ; observateur passif/tree-brute/reprise/relecture ; profil
membranaire et observer imbriqué. Le contrôle géométrique place les contacts
et augmente les probabilités pour isoler le mécanisme : **ce n'est pas une
cinétique spontanée ni un succès de campagne**.

Comparaison indépendante aux sources MD2 archivées : préfixes t5 des trois
graines intégrées, positions/liaisons/PRNG/mouvement exactement identiques
sans option RV1. Catalogue recertifié sans changer ses21 entrées/scénarios.
Suite complète172 tests passée, puis contrôle ciblé de la colonne progrès
ajouté. Une première suite a rencontré des refus d'accès au dossier temporaire
du sandbox Windows ; relance hors sandbox réussie. Aucun correctif de chimie
pour masquer cet incident technique. Les tests de porte prospective couvrent
aussi le refus, les critères de matière/survie/activité et le passage sans
double lancement ; les anciens tests du superviseur restent passants.

## Campagne achevée et décision

RV1 A :12 tâches,150 billes, quatre préparations G001 et quatre F001 plus
monomères, quatre variantes ×3 graines, t1200. Sources et phase B figées avant
lancement. Deux travailleurs ; checkpoints30s, budget24h, pas de retry
scientifique. Le superviseur est réellement lancé hors sandbox en arrière-plan.

La porte attend **toute** la cohorte : réassemblage puis réincorporation dans
au moins2/3 graines protégées, conservation d'un G001 détaché dans chacune,
activité médiane au moins moitié du témoin non nul et invariants valides.
Si elle passe, B lance3 bains MD2 et un contrôle dt/2 ; sinon arrêt pour
interprétation. Pas de balayage supplémentaire ou d'adoption automatique.

```powershell
recycling_status.bat
python experiments/review_recycling.py
python experiments/audit_recycling_material.py
stop_recycling.bat
resume_recycling.bat
```

`cell_status.bat` donne la checklist ; `start_recycling.bat` prépare une
**nouvelle** campagne et refuse de doubler une campagne encore active.
Les résultats/checkpoints/journaux restent locaux dans outputs ; les deux
recettes conservent configurations, graines et sources, sans données brutes.
Le rapport de revue indique les seules trajectoires terminées et ne prend
aucune décision sur une cohorte partielle. Les lectures ci-dessous conservent
la trace des interprétations intermédiaires ; la cohorte finale fait foi.

Première lecture partielle :2/12 terminés, zéro erreur, full/protected graine0
en cours. À t1200, zero graine0 a7 G001 et5 F001 courants,38 formations
catalysées ; backbone graine0 a3 G001 et0 F001,43 formations catalysées,
14 ruptures et0 dissociation. Dans ce dernier cas,18 F monomères et9 F dimères
remplacent les F001. Invariants valides et150 billes dans les deux essais.
Le cumul d'activité ne signale donc pas à lui seul la disparition finale
des outils complets. Zéro réassemblage recyclé est attendu dans ces deux
ablations sans dissociation. Une graine ne démontre pas un effet robuste ;
aucune décision de porte anticipée à cette première lecture. Un F2 peut encore
catalyser : disparition de F001 n'est pas synonyme d'absence de toute activité.

Lecture suivante10/12 : full graine0 produit13 réassemblages dont les deux
atomes ont été libérés de matière polymérisée et3 réincorporations de ces
composites ; full graine1 en produit3, sans réincorporation de composites à
deux atomes recyclés. Protected graines0/1 :0/0 pour ces deux critères stricts,
malgré103/157 formations catalysées et4/6 G001 courants. La libération de matière
existe :3/2 supports précédemment polymérisés dissociés au moins une fois.
Leurs réassemblages avec un partenaire neuf existent aussi, sans incorporation
observée de ces produits. Ce n'est donc ni « toute la matière est bloquée »
ni un maintien établi. La porte reste inchangée, la troisième graine finit.

Audit passif motivé : reconstruire la topologie depuis les seules transitions
du checkpoint pour distinguer le cycle de monomères jamais polymérisés du
recyclage réel. Les topologies finales sont exactement retrouvées sur les dix
essais et les métriques strictes recoupent le census indépendant. Les instantanés
montrent des F2 encore occupés, mais ne donnent pas l'exposition intégrée aux
ruptures protégées. Ne pas attribuer causalement tout l'échec à cette occupation.
L'audit distingue P seul/R seul/deux atomes recyclés ; le seuil prospectif
exige les deux et n'est pas assoupli après lecture.

### Résultat final, graines0 /1 /2

| Variante | G001 courants | F001 courants | Formations catalysées | Réassemblages deux atomes recyclés | Réincorporations de ces composites |
| --- | --- | --- | --- | --- | --- |
| zero | 7 /6 /6 | 5 /8 /5 | 38 /41 /41 | 0 /0 /0 | 0 /0 /0 |
| backbone | 3 /4 /3 | 0 /1 /1 | 43 /44 /43 | 0 /0 /0 | 0 /0 /0 |
| full | 4 /5 /5 | 1 /0 /1 | 186 /161 /150 | 13 /3 /9 | 3 /0 /1 |
| protected | 4 /6 /4 | 2 /4 /6 | 103 /157 /151 | 0 /0 /1 | 0 /0 /0 |

Stocks courants initiaux inclus ; événements de réassemblage/réincorporation,
pas nombre de chaînes ni de générations. Les douze bilans restent valides,
150 billes conservées. Le contrôle de topologie et le recoupement indépendant
des compteurs sont exacts sur12/12 checkpoints finaux.

Le candidat **full** réincorpore des composites dont les deux atomes viennent
de polymères dans2/3 graines ; cela donne un chemin local réel, sans montage
de contacts ni nouveau taux après observation. La variante **protected** ne
réincorpore aucun composite à deux atomes recyclés : les deux seuils de matière
sont refusés. Survie des G001, catalyse médiane et invariants passent. La porte
ne sélectionne pas rétroactivement full et n'est pas assouplie.

Nuance : protected graine2 réincorpore un composite contenant seulement un R
recyclé. Zéro au critère strict ne signifie donc pas absence de tout recyclage.
L'audit complet distingue les deux cas. Le nombre de formations catalysées
augmente beaucoup, mais une grande partie vient de cycles de monomères jamais
polymérisés : ce cumul ne prouve ni production utile ni homéostasie. F2 peut
rester actif ; la fidélité d'un outil complet et son activité sont distinctes.

Prochain contre-test motivé, avant de modifier les taux : mesurer l'exposition
locale des fragments à la rupture et à la recapture, et le flux **utile** de
matière recyclée, pas seulement le nombre de formations. Une protection
indifférenciée peut préserver outils et fragments ; les instantanés ne suffisent
pas à établir cette causalité. Le recyclage a désormais une famille mécaniste
concrète ; I0/diversité des productions et L reste le plus grand trou conceptuel.

## Décision et maturité

W-02/W-03 passent de0 à25% : mécanisme et trajet matériel contrôlés, pas preuve
de dégradation sélective ni d'évacuation intégrée. H-06 reste0 : un garde de
protection fonctionne, la survie des informations rares reste à tester.
Homéostasie petites/grandes espèces inchangée0 : un inventaire fini ne la
prouve jamais. Fonctions distinctes, synthèse L et renouvellement F intégré
restent les autres risques ouverts. Aucune nouvelle protéine n'est proposée
ou ajoutée silencieusement.

Le lot réduit une inconnue concrète — comment rendre la matière composite
réutilisable — et fournit son contre-test aval avant intégration. Il ne prouve
pas que les pertes seront compatibles avec le réseau utile. Revenir à la
diversité fonctionnelle I0 ou au diagnostic ciblé des fragments, sans nouvelle
grille automatique ni transfert du candidat refusé. La protection, le maintien
et l'expressivité restent des verrous de recherche, pas des tâches garanties.
