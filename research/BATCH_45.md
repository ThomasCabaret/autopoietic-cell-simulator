# Lot45 — transfert observé, fermeture fragile et diagnostic local

5 novembre2026. [Plan](BATCH_45_PLAN.md) · [récupération CB1](BATCH_45_CB1_RECOVERY.json)
· [CX1](BATCH_45_RECIPES.json) · [CW1](BATCH_45_WIDE_RECIPES.json)
· [pilote large](BATCH_45_WIDE_PILOT.json) · [loupe](BATCH_45_LOUPE.json).

## CB1 terminé :9/9 sans erreur de simulation

Le rapport automatique échouait après les neuf calculs : `modeArgs` remis à
vide dans PowerShell perdait `--compact`, donc appelait le gate BI1. Wrapper
corrigé ; le driver déduit désormais l'analyse du gate du job, même si l'option
se perd. Deux régressions couvrent option perdue et contradiction explicite.

`recover_compact_report.py` a appelé **l'analyseur CB1 figé d'origine**, option
explicite, sans relancer les trajectoires. Erreur/état ancien archivés, neuf
hashes de résultats et toutes sources/manifeste inchangés. Rapport récupéré
`outputs/compact_transfer_followups/followup_20261105T092857284853Z/report_recovered_1.json`,
SHA256 `b9e80c46099b446f1d1ca8e0ead8fa4a9e220312bb6ccc9f385b567d2e9e2502`.
La provenance détaillée est conservée dans BATCH_45_CB1_RECOVERY.

| À2400, graines0/1/2 | Active | Sans L | Sans synthèse |
| --- | --- | --- | --- |
| Nouveaux G libérés |3 /10 /4|3 /1 /1|0 /0 /0|
| Nouveaux F libérés |4 /9 /1|3 /1 /0|0 /1 /0|
| L fabriqués |24 /23 /23|22 /21 /21|0 /0 /0|
| L via F entièrement alimentaires |2 /7 /0|—|0 /0 /0|
| Vrais L nés dedans puis insérés |0 /1 /0|0 /0 /0|0 /0 /0|
| Fermeture1800–2400 |0 /.9417 /0|sans objet|.9667 /.9625 /.9625|

Le L inséré en graine1 est réellement produit par un F entièrement reconstruit
depuis P/R : chaîne matérielle **nourriture→F exprimé→L→frontière** dans le même
bain. Une seule graine, pas robustesse ni maintien. Le F nouveau du témoin
sans synthèse provient de monomères F déjà préparés : il ne prouve pas de
reconstruction alimentaire ; le témoin interdit la synthèse des monomères,
pas l'expression depuis le stock composite initial.

Six conditions passent, deux refusées : fermeture tardive des trois actifs,
et insertion sur au moins deux graines. Aucun invariant violé, aucune traversée
liée observée pendant les périodes classifiables. Ces dernières ne couvrent
pas les longues ouvertures. Stocks H/T épuisés ou presque ; P/R encore variables.
Les médianes G/F sont préservées par rapport au noL de cette géométrie, mais
ne sont pas un maintien sous pertes ou flux. Le compactage a réduit un verrou
de dilution ; il ne résout pas la mécanique d'insertion.

## Une ouverture réelle, pas un artefact de labels

Première période invalide d'au moins10 unités :752,5/2129/882,5. Checkpoints
finaux : graine0 chaîne **ouverte54 L dont52 originaux**, graine2 chaîne ouverte49
dont43 originaux, plus fragment ouvert11. La graine1 finit en cycle simple53
dont52 originaux, aire213,879. Ce n'est donc pas seulement l'ancien seuil de
80% des têtes initiales qui rejette une membrane renouvelée. Critère inchangé.

Les échanges actifs sont5/2/4 ; temps admissibles croissants par rapport à BI1.
La première lésion durable0 suit le remplacement local234–235 par173–234 à752,11.
Un retour à753,16 est suivi du même déplacement à753,23. La simple proximité
temporelle motive une loupe et un témoin causal, pas une preuve suffisante.

## CL1 : six billes,650 frames, physique identique

Rejeu des sources CB1 figées jusqu'à758,11 ; capture751,61–758,11 de trois L,
atomes173/174/234/235/286/287. Un clone créé avant la fenêtre reste exactement
identique en positions, vitesses, chimie, PRNG et observations à la fin ; les
quatre historiques/événements observés reproduisent aussi le préfixe CB1.
483,062s de calcul, budget30min respecté. Sortie locale
`outputs/diagnostics/CL1_20261105T113223797972Z/report.json`.

| Échange | Variation du potentiel de ports | Barrière P/R |
| --- | ---: | ---: |
|752,11|+6,02430|0|
|753,16|+1,95871|0|
|753,23|−0,70271|0|

À T=.08, le premier saut vaut environ75 fois T. C'est une variation à positions
fixes, pas un bilan intégré de chaleur ; le core/axes ne changent pas à cet
instant. La règle d'échange est un helper non thermique déclaré : le saut
n'est pas une erreur d'intégration numérique. Les deux extrémités libres ont
q1,20476 immédiatement après, minimum .90503, puis8,81519 à758,11 ; seuil de
capture .0625. Aucun des594 échantillons où ces deux faces sont libres n'est
éligible à leur jonction. Le lien nouveau sollicite fortement la mécanique,
et le bassin des faces libérées est trop faible dans cette rencontre pour
les remettre en place. Généralisation à toute lésion encore à tester.

Premier lancement CL1 refusé avant le moindre pas : fichier archivé `inspect.py`
masquant le module standard Python. Sources/log d'échec conservés. Nouveau
répertoire, nom `lesion_probe.py`, statut d'échec explicite et sources vérifiées.
Aucune modification des sources chimiques, aucun retry d'une trajectoire choisie
selon son succès. Le défaut était dans le diagnostic avant initialisation.

## CX1 et CW1 : contrôles et une variante motivée

**CX1** : trois CB1 identiques avec seul taux d'échange mis à0, sources/graines/
stocks/horizon2400 figés. Trois références actives CB1 réutilisées, pas relancées.
Ce contrôle manque à CB1 (sans synthèse changeait aussi la matière). Budget3h,
deux travailleurs, checkpoints30s, rapport puis arrêt, aucune nouvelle loi.
Lecture intermédiaire : graines0/1 finies, G4/9,F7/12,L22/22, fermeture tardive
.9575/.9600, zéro insertion. Ce sont deux contrôles, pas un verdict à trois graines.

**CW1** : seul `dock_width` .3→.6. Le potentiel libre s'étend ; sa continuation
liée a une raideur dérivée divisée par4, sans nouveau taux ou paramètre mécanique
indépendant. Toutes les autres lois, bruit, pas, seuils, stocks et formes de
ports restent fixés. Espoir : amortir le saut et rendre accessible la jonction
des extrémités ; risques : liaisons trop souples, amas parasites, chaleur et
régression de débit. Pas un optimum établi, pas un nouvel outil ou helper.

Pilote CW1P100 graine0 :67,766s,3 L,94,5% de temps classifiable fermé, état final
fermé52 L/aire211,20, invariants0. Pas d'insertion ni preuve de renouvellement.
Le critère technique>=.8 annoncé avant le pilote passe. Trois suivis CW1 à2400
lancés,2 travailleurs/3h/checkpoints30s, comparaison aux mêmes références CB1.
Porte : stabilité et production préservées, plus insertion dans au moins2 graines.
Aucune promotion automatique ou garantie des contrôles noL/sans synthèse à.6.

Les premiers superviseurs figés gardent quelques textes génériques hérités dans
`scope` ; les variantes se définissent par leurs scénarios et leurs conditions
numériques explicites. Le collecteur courant précise ces textes sans changer
les seuils ou les échantillons. CX1 coupe l'échange ; CW1 le conserve et change
la largeur. Aucune nouvelle ablation noL/sans synthèse dans ces suivis.

## GUI et maturité

**Démos → Intégration compacte · défauts connus** expose les trois CB1,302 billes,
depuis leurs vrais états initiaux. Le raccourci « État actuel · bain intégré »
ouvre désormais cette scène en graine0 par convention : l'échec est visible.
Graine1 pour l'insertion unique ;0/2 pour les ouvertures persistantes. Fiches,
compteurs passifs et limites ne présentent pas cette porte refusée comme un
succès cellulaire. MIN1M et MX2 restent accessibles séparément.33 choix natifs
Qt/OpenGL vérifiés, lecture/pause/recommencement et positions égales au moteur.

Validation :**240 tests logiciels passent** (`outputs/batch45_final_tests.log`),
14 contrôles de registre/conception après mise à jour. Le vrai wrapper
PowerShell Review/Compact appelle désormais les huit conditions CB1 correctes.
Ces vérifications ne prouvent pas le succès des campagnes CX1/CW1 en cours.

Maturité : un transfert matériel jusqu'à la frontière est observé sur une graine,
mais pas de tenue robuste ou maintien. M-04 garde25 de preuve et passe au statut
conceptuel « draft » : les étapes locales sont maintenant observées, la robustesse
reste à établir. Protection/recyclage, régulation des polymères, information et
énergie sous flux restent des risques majeurs. Prochain jalon : CX1/CW1 complets,
sans nouvelle grille. Si élargir ne donne qu'une membrane stable sans transfert,
réexaminer le mécanisme et le coût énergétique plutôt qu'ajouter d'autres largeurs.

Suivi : `exchange_ablation_status.bat` / `wide_ports_status.bat`, arrêt/reprise
par les lanceurs associés. Aucun push, aucune donnée brute dans Git.
