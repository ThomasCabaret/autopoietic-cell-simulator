# Simulateur de chimie locale

Le CPU (`numba`) est le mode de référence. Les options `cpp`, `cuda` et
`cuda-resident` sont explicites. Dans le bain CP1, la mécanique résidente tourne
sur GPU et les décisions de réaction restent sur CPU. [Guide CPU et CUDA](docs/COMPUTE_BACKENDS.md)

**Point d’arrêt du 7 novembre 2026**. La recherche et les campagnes sont en pause.
Le candidat CP1, le statut du portage et les résultats disponibles sont résumés
dans [CURRENT_STATUS.md](CURRENT_STATUS.md).

**État et sous-buts du projet** : [checklist compacte](research/CELL_CHECKLIST_COMPACT.md)
et [registre détaillé](research/CELL_CHECKLIST.md), avec sous-buts et dépendances.
`cell_status.bat` affiche le tableau ; source évolutive et paliers expliqués
dans [la méthodologie](research/CONCEPT_FIRST.md). Les scores décrivent les preuves,
pas un pourcentage global de cellule achevée.

**Coût des lois et cas particuliers** : [inventaire normalisé de la chimie](research/CHEMISTRY_COMPLEXITY.md).
Types, liens, transitions, conventions fonctionnelles, paramètres et helpers
du candidat intégré sont distingués des variantes historiques et des observateurs.

**Atlas du métabolisme visé** : double-cliquer sur `metabolism.bat`, ou ouvrir
[la planche SVG](docs/metabolism/metabolism.svg) / [la page navigable](docs/metabolism/index.html).
Trois gènes détaillés, apports, synthèses, copie, expression, membrane et déchets ;
la cible est distinguée des capacités actuelles. Sources modifiables et commande
de génération dans [docs/metabolism](docs/metabolism/README.md).

**Interface durable et démos du projet** : exécuter `install_visualizer.bat` une fois,
puis `visualizer.bat`. Fenêtre Qt, rendu OpenGL par lots, navigation, filtres,
sélection/suivi, transformations et export PNG. Elle démarre en pause après
ouverture d'un scénario. Choisir **Démos → Chimie actuelle · bain intégré CP1**
pour le candidat en cours, **Chimie actuelle · membrane depuis lipides libres**
pour rejouer l’expérience d’assemblage depuis son état initial, ou
**Démo intégrée · référence EG1** pour le prototype historique d’insertion.
[Catalogue et limites](docs/DEMOS.md)
Le bain MIN1M construit produit des catalyseurs entièrement refaits et actifs
avec membrane sur trois graines. Les enzymes initiales restent présentes et
les lipides sont préparés : le maintien sous pertes reste à établir.
La visualisation essentielle est disponible ; la vidéo et les outils avancés
seront spécifiés plus tard. [Guide de la GUI](docs/VISUALIZER.md).
Les lanceurs Pygame historiques ci-dessous sont conservés.

Pour voir les résultats CP1 calculés sur cette machine :
**Résultats locaux → Membrane assemblée · CP1 · graine 1 · terminé** montre
l’enceinte de 52 lipides à t = 8 000 en lecture seule, avec zoom, filtres et sélection.
Le menu utilise les fichiers de campagne locaux ignorés par Git.
**Fichier → Ouvrir un checkpoint local…** permet la reprise d’un état
calculé avec la version courante du moteur.

**Référence historique d’insertion**. **Démos → Intégration compacte ·
échanges stabilisés** montre les trois EG1,302 billes, avec vraie synthèse H/T.
« Démo intégrée · référence EG1 » ouvre la graine0 par convention. Insertion de L
fabriqués dans deux graines sur trois, tenue tardive94–95% et température
proche de la consigne dans les trois ; aucun maintien sous pertes ou flux ouvert.
CB1 et ses ouvertures restent au menu « défauts connus ». MIN1M et MX2 restent
accessibles séparément. EN1 est visible dans « contrôle au pas fin ».

Recherche : **CR1 terminé3/3, crible fixé réussi** sous les lois CP1 :
enceintes finales30/52/34 depuis dimères isolés, présence tardive>=50% sur2/3.
Les refus CC1/CH1 aux horizons courts restent conservés. Cela ne prouve pas
la rétention ou le maintien de la cellule. **PT1 et RF1 sont terminés, leurs cribles refusés** : une ouverture finale
empêche de conclure la rétention ; le recyclage ne maintient pas toujours
l'outil et n'établit pas le réemploi strict. **FR1 terminé6/6** : récupération
fast0/3 et slow1/3, deux portes refusées. OB1 terminé6/6 vérifie le transport ouvert
de précurseurs sans cellule ni transfert de pertes dans CP1.
État : `functional_recovery_status.bat`. Aucun changement des lois CP1.
Le catalogue propose 41 configurations au total. CF1 reste en pause scientifique.
[Lot54](research/BATCH_54.md) · [Checklist](research/CELL_CHECKLIST_COMPACT.md) ·
[Calibration](research/CAMPAIGN_CALIBRATION.md).

Un moteur CPU commun pour les campagnes sans fenêtre et les démonstrateurs
interactifs. Les lois de copie/expression et de membrane sont des modules séparés.

**Sous Windows :** installer Python 3.12, puis exécuter `demonstrators/installer.bat`
pour préparer les dépendances dans `.venv`. Ouvrir ensuite
[demonstrators](demonstrators/README.md) et double-cliquer sur `01_copie.bat`,
`02_membrane.bat` ou `03_traduction.bat`.

Pour une installation manuelle depuis la racine :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Les commandes Python ci-dessous s'exécutent avec cet environnement activé ou
avec son interpréteur `.venv\Scripts\python.exe`.

Les démonstrations en direct recalculent la dynamique. Le lanceur de fragments
indique explicitement une relecture de trajectoire historique.
La membrane s'assemble désormais depuis 36 molécules isolées de deux billes ;
le repliement d'un ruban déjà construit reste un contrôle séparé.

```powershell
python -m simulator --config demonstrators/configs/copy.json --gui
python -m simulator --config demonstrators/configs/copy.json --no-trajectory
python -m simulator --config demonstrators/configs/membrane.json --spatial brute
python -m simulator --resume outputs/nom_du_run/checkpoint.npz --gui
```

Les sorties vont dans `outputs/` : paramètres résolus, code exact et empreintes,
métriques, trajectoire si demandée et état de reprise complet. Fermer une fenêtre
conserve aussi l'état partiel. Le mode sans interface n'importe ni Pygame ni Matplotlib.
Les données restent locales et sont exclues de Git. Le dépôt conserve les entrées
et le code nécessaires pour les [reconstruire](research/REPRODUCTION.md).

- [Mode d'emploi des démonstrateurs](demonstrators/README.md)
- [Architecture, format et ajout de lois](SIMULATOR_ARCHITECTURE.md)
- [Validation de la migration](research/ENGINE_MIGRATION.md)
- [Lot 3 : assemblage membranaire et ligations géométriques](research/BATCH_03.md)
- [Lot 4 : expression puis opération répétée par les F composites](research/BATCH_04.md)
- [Lot 5 : copie, traduction et opération dans un même bain](research/BATCH_05.md)
- [Lot 6 : composants construits puis incorporés](research/BATCH_06.md)
- [Architecture intégrée : dépendances, interactions et budget de cellule](research/CELL_ARCHITECTURE.md)
- [Lot 7 : audit du réseau, risques et dimensionnement](research/BATCH_07.md)
- [Lot 8 : outil exprimé, fabrication de composants et copies](research/BATCH_08.md)
- [Santé du projet, risques et horizon de décision](research/PROJECT_HEALTH.md)
- [Maturité et fonctions encore manquantes](research/MATURITY.md)
- [Méthode et contributions](CONTRIBUTING.md)
- [Reconstruction des expériences sans données préembarquées](research/REPRODUCTION.md)
- [Initialisation Git et premier push](GIT_SETUP.md)

Le scénario `09_expression_fonction.bat` montre une chaîne F fabriquée depuis G
puis réutilisée pour plusieurs ligations. Les expériences restent des preuves
de principe : cellule viable, fabrication des composants et reconstruction des
outils ne sont pas démontrées.

Le [lot9](research/BATCH_09.md) teste une grande frontière préparée, la
sélectivité de sondes et une voie d'insertion locale encore rare. Démonstrateur13.
L'[audit de localité](research/LOCALITY_AUDIT.md) précise les raccourcis interdits
et les aides externes ; [cinétique et performance](research/KINETICS_AND_PERFORMANCE.md)
fixe les prochaines obligations de mesure et de calcul différé.

Les [campagnes différées](campaigns/README.md) disposent de lanceurs Windows :
`start_campaign.bat`, `campaign_status.bat`, `stop_campaign.bat`,
`resume_campaign.bat`, `analyze_campaign.bat`. Sources figées et reprise ; aucune
notification ni exécution pendant veille/extinction. Voir [lot10](research/BATCH_10.md).
