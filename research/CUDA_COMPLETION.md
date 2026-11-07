# Quand le portage CUDA est terminé

La référence de réception est CP1 en bain réactif, puis le scénario ouvert
de travail lorsqu'il est défini. Les anciens modes restent accessibles sur
CPU. Les limites de compatibilité sont visibles à la sélection du backend.

| Chantier | État au lot60 | Critère de clôture |
| --- | --- | --- |
| Voisinage, contacts, ressorts, angles et Langevin | Résidents en bain inerte, en copie réactive et dans CP1. | Mesurer à des densités représentatives. Contrôler le coût des cellules chargées et des recalculs spatiaux. |
| Forces propres à CP1 | Orientation, capture, barrière et ports libres, compétitifs et liés dans le pas résident. | Vérifier le débit et la stabilité aux densités et tailles représentatives. |
| Topologie dynamique et transferts | Mise à jour aux ticks validée en copie et après naissance lipidique en CP1. | Mesurer les synchronisations, réallocations et l'ajout/retrait de particules dans le scénario ouvert. |
| Réactions et conflits | CPU, ordre et tirages conservés. Les ticks occupent 72 % du profil court CP1 résident. | Mesurer séparément énumération, géométrie, énergie et résolution des conflits. Porter les phases régulières qui dominent encore. Justifier par des mesures les phases qui restent sur CPU. |
| CPU et GPU de production | CPU Numba, noyau C++ optionnel, CUDA hybride et premier CP1 résident utilisable en CLI. | Optimiser les parcours et allocations dominants côté CPU et GPU. Exécuter les mêmes recettes depuis les entrées ordinaires. |
| Équivalence et mesure finale | Préfixe CP1 apparié et reprise exacte du contrôle de naissance. | Bilan matière et enveloppes de résultats sur plusieurs graines et horizons prédéfinis. Mesure de bout en bout avec observateur et coût du démarrage déclaré. |

Une étape importante peut rester sur CPU si le profil inclut son coût
et ses transferts, et si la variante GPU n'améliore pas le débit ou rompt
le contrat des réactions. Pour chaque famille de forces et phase de tick,
consigner le backend, la part du temps, les données transférées et la
raison du choix. Refaire le profil après chaque portage majeur.

Le speedup de clôture est le temps CPU divisé par le temps GPU, à règles,
scénarios, horizons et cadence d'observation identiques. Publier plusieurs
tailles, un scénario réactif utile, le régime chaud, le coût du lancement
et la dispersion. Un essai intermédiaire sert à décider de l'architecture.
