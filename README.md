# Simulateur de chimie locale

**Atlas du métabolisme visé** : double-cliquer sur `metabolism.bat`, ou ouvrir
[la planche SVG](docs/metabolism/metabolism.svg) / [la page navigable](docs/metabolism/index.html).
Trois gènes détaillés, apports, synthèses, copie, expression, membrane et déchets ;
la cible est distinguée des capacités actuelles. Sources modifiables et commande
de génération dans [docs/metabolism](docs/metabolism/README.md).

**Interface durable et démos du projet** : exécuter `install_visualizer.bat` une fois,
puis `visualizer.bat`. Fenêtre Qt, rendu OpenGL par lots, navigation, filtres,
sélection/suivi, transformations et export PNG. Elle démarre en pause après
ouverture d'un scénario. Aller dans **Démos → État actuel · bain intégré**
pour la vue d'ensemble sous Langevin avec contacts cohérents MD2, ou choisir
**Membranes · molécules libres** pour un essai plus rapide. Les références
anciennes restent rangées séparément. [Catalogue et limites](docs/DEMOS.md).
Le bain courant est construit et son renouvellement reste incomplet : la
membrane progresse, mais aucun F nouveau complet n'a été observé dans MD2 à1200.
La visualisation essentielle est disponible ; la vidéo et les outils avancés
seront spécifiés plus tard. [Guide de la GUI](docs/VISUALIZER.md).
Les lanceurs Pygame historiques ci-dessous sont conservés.

Recherche en cours : campagne T9E de finition des fragments et d'interférence
avec les outils, suivie d'un transfert intégré conditionnel. État par
`expression_status.bat`, pause par `stop_expression.bat`. Cette variante reste
expérimentale ; les démos ci-dessus gardent MD2/Langevin. [Lot27](research/BATCH_27.md).

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
