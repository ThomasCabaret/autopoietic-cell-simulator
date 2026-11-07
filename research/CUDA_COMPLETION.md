# Quand le portage CUDA est terminé

La référence de réception est CP1 en bain réactif, puis le scénario ouvert
de travail lorsqu'il est défini. Les anciens modes restent accessibles sur
CPU. Les limites de compatibilité sont visibles à la sélection du backend.

| Chantier | État au lot63 | Critère de clôture |
| --- | --- | --- |
| Voisinage, contacts, ressorts, angles et Langevin | Résidents en bain inerte, en copie réactive et dans CP1. | Mesurer à des densités représentatives. Contrôler le coût des cellules chargées et des recalculs spatiaux. |
| Forces propres à CP1 | Orientation, capture, barrière et ports libres, compétitifs et liés dans le pas résident. | Vérifier le débit et la stabilité aux densités et tailles représentatives. |
| Topologie dynamique et transferts | Mise à jour en copie, après naissance lipidique CP1 et avec entrées/sorties du banc ouvert. | Mesurer les synchronisations et réallocations à plusieurs tailles et flux, puis valider le scénario ouvert intégré. |
| Réactions et conflits | CP1 reste hybride. La capture indépendante a une tranche résidente avec propositions, réservation et commit. | Porter les deltas H/T, la capture coopérative et les transitions de copie et de faces. Vérifier les dépendances d'énergie et valider les effets de l'ordre d'arbitrage. |
| CPU et GPU de production | CPU Numba, noyau C++ optionnel, CUDA hybride et premier CP1 résident utilisable en CLI. | Optimiser les parcours et allocations dominants côté CPU et GPU. Exécuter les mêmes recettes depuis les entrées ordinaires. |
| Équivalence et mesure finale | Préfixes appariés et première mesure avec observateur à 302, 1 000 et 2 118 billes. Gain de 1,13× à 1,64× à 2 118. | Expliquer la dispersion, mesurer plusieurs graines et horizons prédéfinis, puis publier le débit complet. |

Une étape importante peut rester sur CPU si le profil inclut son coût
et ses transferts, et si la variante GPU n'améliore pas le débit ou rompt
le contrat des réactions. Pour chaque famille de forces et phase de tick,
consigner le backend, la part du temps, les données transférées et la
raison du choix. Refaire le profil après chaque portage majeur.

Le speedup de clôture est le temps CPU divisé par le temps GPU, à règles,
scénarios, horizons et cadence d'observation identiques. Publier plusieurs
tailles, un scénario réactif utile, le régime chaud, le coût du lancement
et la dispersion. Un essai intermédiaire sert à décider de l'architecture.
