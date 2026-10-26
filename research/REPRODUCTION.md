# Recettes versionnées, données locales

Le livrable est le code, les lois et les documents de recherche. Les trajectoires,
checkpoints, historiques d'événements et fichiers bruts `result.json` restent dans
le répertoire de travail et sont ignorés par Git. Aucun de ces fichiers locaux
n'est supprimé par cette politique.

Pour chaque essai retenu, le dépôt conserve uniquement :

- La configuration et la graine, dans `config.json` ou `scenario.json`.
- Les sources exactes ayant exécuté la simulation, avec leurs valeurs par défaut.
- `recipe.json` : type d'exécuteur, paramètres, versions numériques connues et
  empreintes SHA-256 de ces sources. Aucun historique de positions ou de résultats.
- Les conclusions et les figures de synthèse sélectionnées dans les notes de recherche.

Les 57 recettes initiales couvrent les anciens essais, les quatre démonstrateurs
migrés et l'audit abstrait. Quatre recettes signalent un incident d'initialisation,
pas une trajectoire physique ; le reconstructeur refuse de les traiter comme
une expérience ayant effectivement évolué.

## Reconstruire

Depuis la racine avec l'environnement de `requirements.txt` :

```powershell
python scripts/reconstruct_experiment.py research/runs/E1zero_s0_20261023T131018800276Z
python scripts/reconstruct_experiment.py research/engine_runs/Courbure_et_fermeture_membranaire_s0_20261023T140139844072Z
```

Les fichiers recalculés sont écrits dans `outputs/reconstructed/<identifiant>/`.
Choisir `--output autre_dossier_vide` pour une nouvelle reconstruction. Le programme
vérifie les empreintes, copie les sources dans ce dossier et les exécute dans un
processus isolé. Il ne remplace pas les données historiques locales. Selon le
type d'expérience, il régénère métriques, trajectoire et éventuellement checkpoint.
L'audit abstrait recrée ses résultats dans un sous-dossier de cette sortie.

Le lot7 utilise le type `cell_design_audit`, avec `config.json`, source exacte et
empreintes du code **et de la configuration**. Le même reconstructeur régénère
son `result.json` dans la sortie choisie ; aucune dynamique moléculaire n'est
effectuée. Voir `research/BATCH_07_RECIPES.json` et `experiments/audit_cell_design.py`.

La graine et le code identiques ne promettent pas une identité numérique entre
versions différentes de bibliothèques ou matériels. Les références numériques
connues sont dans la recette et l'environnement fixé dans `requirements.txt`.

Le démonstrateur `05_fragments_relecture.bat` utilise la trajectoire locale si elle
est présente ; sinon il la reconstruit d'abord depuis sa recette historique.
Le premier lancement après clonage peut donc demander un calcul complet.

## Ajouter une expérience

Après un essai local :

```powershell
python scripts/reconstruct_experiment.py chemin/du/run --export-recipe
```

Conserver sous `research/runs/` ou `research/engine_runs/` la recette, la configuration
et les sources correspondantes. Le fichier `.gitignore` sélectionne seulement ces
entrées ; les données d'exécution restent exclues. Ne pas modifier les sources
historiques en place. Les nouveaux travaux changent les sources courantes et
produisent de nouvelles recettes.

Le benchmark se reconstruit avec `python experiments/benchmark_engine.py` et le
criblage statique avec `python experiments/composite_geometry.py`. Leurs sorties
générées restent locales. Les ZIP de démonstration contiennent maintenant le
code et les recettes, sans données de simulation préembarquées.

## Lot9

`python experiments/run_batch9.py M1noBondBarrier --seed 0` utilise le moteur
courant. BATCH_09_RECIPES.json contient les24 recettes exactes. Le reconstructeur
partagé les régénère ; `python experiments/make_batch9_report.py` audite ensuite
les résultats locaux. `verify_batch9.py membrane`, `copy`, `reconstruct` vérifient
les références et tous leurs tableaux. `audit_membrane_exchange.py` trace les
deux événements archivés ; `smoke_membrane_bath.py` teste le rendu hors écran.

## Campagnes K1

Le plan, les commandes et la restauration source seule sont décrits dans
campaigns/README.md. Les recettes figées sont placées sous research/campaign_recipes/,
avec manifeste/plan/empreintes et runtime exact, sans données. Après restauration,
le contrôleur figé produit de nouvelles sorties. Le commit de développement est
aussi inscrit dans le manifeste ; les empreintes restent l'identité exacte des
sources exécutées.
