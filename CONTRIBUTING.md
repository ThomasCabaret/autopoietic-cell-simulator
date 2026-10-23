# Contribuer et conserver les preuves

Ces instructions concernent le dépôt source complet, et non seulement le paquet
de démonstration destiné à l'exécution.

Utiliser Python 3.12 et les versions de `requirements.txt`. Le moteur partagé est
dans `simulator/` ; les règles chimiques se trouvent dans ses modules et les
scénarios JSON dans `demonstrators/configs/`. Voir `SIMULATOR_ARCHITECTURE.md`.

## Vérification des changements

```powershell
python -m unittest discover -s tests -v
python experiments/test_local_mechanics.py
python experiments/test_research_observers.py
python experiments/smoke_viewer.py
```

Le dernier contrôle utilise le pilote SDL hors écran. Il n'ouvre pas de fenêtre
sur le bureau. Pour un changement graphique, vérifier aussi le démonstrateur
en direct sur la plateforme visée.

## Données et provenance

- Versionner le code, les lois, les configurations, les notes et l'arbre de
  recherche, ainsi que les figures de synthèse sélectionnées pour ces notes.
- Garder les données d'expériences sur le disque de travail, hors Git : trajectoires,
  checkpoints, résultats bruts, historiques d'événements et images de chaque run.
- Dans les dossiers d'essais, versionner uniquement les sources exactes,
  `config.json` / `scenario.json` et `recipe.json`. Ne pas réécrire ces entrées
  historiques ; leurs empreintes portent sur les octets, fins de ligne comprises.
- Enregistrer les explorations dans `outputs/`, puis conserver les entrées d'un
  essai utile avec la procédure de [reconstruction](research/REPRODUCTION.md).
- Mettre à jour `research/branches.json`, `LOG.md`, `PRIORITIES.md` et `MATURITY.md`
  lorsque les résultats ou les décisions de recherche changent. Conserver les échecs.
- Les `.npz` et `.npy` sont toujours exclus. Un clone reconstruit les données
  nécessaires depuis les recettes ; il n'a pas besoin de les télécharger.

Les ZIP distribuables sont reconstruits par `python scripts/build_bundle.py` et
restent dans `deliverables/`, ignoré par Git. Ils peuvent être joints séparément
à une livraison ; ils contiennent les sources et les recettes, sans données brutes.

`.gitattributes` fixe les fins de ligne usuelles et celles des lanceurs Windows,
mais conserve aussi les octets des modules `simulator/` : leurs empreintes identifient
la révision des checkpoints actuels. Les archives restent intactes. Ne pas lancer de formatage global sur ces
archives. Vérifier `git diff --check` et `git status` avant un commit.

## Code de référence tiers

La licence MIT du code historique conservé dans `research/legacy_reference/source/`
est reproduite à son emplacement d'origine. Voir `THIRD_PARTY_NOTICES.md`.
Aucune nouvelle licence globale n'est choisie par cette préparation Git.
