# Point d’arrêt — 7 novembre 2026, après le lot 65

Source courte de reprise. [Checklist](research/CELL_CHECKLIST_COMPACT.md),
[priorités](research/PRIORITIES.md), [décisions sur l'audit](research/ASTRA_REVIEW.md).

Le développement et les campagnes sont en pause. La référence de simulation
est le CPU (`numba`) avec Langevin pour les scènes courantes. Les 41 scénarios
du menu utilisent le CPU. La chimie CP1 conserve les ports compétitifs de CH1.
Les options de calcul `cpp`, `cuda` et `cuda-resident` se choisissent explicitement.
La loi lipidique `saturated` reste une variante expérimentale à activer séparément.

| Élément | État et portée |
| --- | --- |
| Chimie cellulaire de travail | CP1, recette CH1 `20261106T073608844143Z`, bain construit de 302 billes et membrane préparée |
| Membrane depuis molécules isolées | CR1 terminé3/3 ; crible2/3 réussi à8000, sans synthèse alimentaire dans ce sous-bain |
| Insertion intégrée de référence | EG1 historique limité, non équivalent à CP1 ; EN1 au pas fin refusé |
| Rétention PT1 | 6/6 terminés, porte refusée ; ouverture de graphe finale dans une graine, fuite dynamique non démontrée |
| Recyclage RF1 | 9/9 terminés, deux protections refusées ; aucun réemploi strict incorporé, outil parfois perdu |
| Récupération FR1 | 6/6 terminés,0 erreur ; fast0/3, slow1/3 ; deux portes refusées. Pas de relance de taux |
| Transport ouvert OB1 | 6/6 terminés, bilan exact et vrais flux ; précurseurs seuls sous Langevin, hors CP1 |
| Calcul CUDA de CP1 | Voisinage, forces et intégration sur GPU en mode résident. Les décisions de réaction du bain CP1 restent sur CPU. Les pilotes de capture et d’énergie lipidique par lots restent séparés de ce chemin. [Critères de clôture](research/CUDA_COMPLETION.md) |
| Calculs actifs à cette clôture | Aucun ; CF1 conserve sa pause scientifique |
| Maintien intégré | Non démontré ; flux CP1, pertes compatibles, bilan L, information et diversité des outils restent ouverts |

À 2 118 billes, le gain observé pour le pas CP1 complet avec observateur allait
de 1,13× à 1,64× sur les mesures exploratoires du lot 62. La variante saturée
n’a montré aucun gain sur le pas complet au lot 65. À t = 20, elle donne 18 et
24 liaisons latérales contre 29 et 32 pour la référence, sur deux graines.
La fermeture d’une vésicule et l’insertion restent à comparer à leurs horizons
utiles. [Mesures et recettes](research/BATCH_65.md)

## Reprise éventuelle

Le portage complet reste ouvert. Le prochain jalon porte sur l’arbitrage des
créations locales et la comparaison entre calcul compétitif incrémental et
variante saturée. Les décisions biologiques ci-dessous restent nécessaires
au premier test intégré de maintien.

1. Fermer le bilan ouvert minimal du co-recruteur équipé, en choisissant la
   représentation d'atomes actifs/IDs et les sorties de matières, dont L.
2. Définir le test de renouvellement sous pertes partielles/redondance ; adapter
   provenance et observateurs réversibles avant de coupler à mixed_synthesis.
3. Dé-risquer l'expressivité : le canal de capture courant ne distingue pas PG/PF
   libres. Garder le polyvalent pour le premier maintien et concevoir une extension
   réutilisable ou une autre architecture avant toute recherche de sélectivité.

## Voir l’état du projet

Lancer `visualizer.bat`. Les scènes en direct s’ouvrent en pause.

| Menu | Ce qui s’affiche |
| --- | --- |
| **Démos → Chimie actuelle · bain intégré CP1** | Le candidat courant, depuis le bain construit CH1. Le maintien et le renouvellement sous perturbation restent ouverts. |
| **Démos → Chimie actuelle · membrane depuis lipides libres** | Le départ CR1 avec 52 dimères isolés, à horizon long. |
| **Démos → Démo intégrée · référence EG1** | La référence historique intégrée de synthèse et d’insertion, avec les limites du contrôle au pas fin. |
| **Résultats locaux → Membrane assemblée · CP1 · graine 1 · terminé** | Le cycle de 52 lipides déjà calculé à t = 8 000, en lecture seule. Dépend des sorties locales. |

[Catalogue des démos](docs/DEMOS.md) · [Guide de la GUI](docs/VISUALIZER.md)
