# Quand le portage CUDA est terminé

La référence de réception est CP1 en bain réactif, puis le scénario ouvert
de travail lorsqu'il est défini. Les anciens modes restent accessibles sur
CPU. Les limites de compatibilité sont visibles à la sélection du backend.

| Chantier | État au lot61 | Critère de clôture |
| --- | --- | --- |
| Voisinage, contacts, ressorts, angles et Langevin | Résidents en bain inerte, en copie réactive et dans CP1. | Mesurer à des densités représentatives. Contrôler le coût des cellules chargées et des recalculs spatiaux. |
| Forces propres à CP1 | Orientation, capture, barrière et ports libres, compétitifs et liés dans le pas résident. | Vérifier le débit et la stabilité aux densités et tailles représentatives. |
| Topologie dynamique et transferts | Mise à jour en copie, après naissance lipidique CP1 et avec entrées/sorties du banc ouvert. | Mesurer les synchronisations et réallocations à plusieurs tailles et flux, puis valider le scénario ouvert intégré. |
| Réactions et conflits | CPU, parcours des faces compilés et empreinte des événements conservée. Les ticks occupent 61 % du profil court résident. | Séparer la préparation des propositions H/T, leur énergie et les conflits. Tester les phases régulières dominantes sur les tailles utiles. |
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
