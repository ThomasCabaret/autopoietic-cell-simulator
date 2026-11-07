# État courant — 7 novembre 2026, lot57

Source courte de reprise. [Checklist](research/CELL_CHECKLIST_COMPACT.md),
[priorités](research/PRIORITIES.md), [décisions sur l'audit](research/ASTRA_REVIEW.md).

| Élément | État et portée |
| --- | --- |
| Chimie cellulaire de travail | CP1, recette CH1 `20261106T073608844143Z` ; aucune loi chimique modifiée au lot55 |
| Membrane depuis molécules isolées | CR1 terminé3/3 ; crible2/3 réussi à8000, sans synthèse alimentaire dans ce sous-bain |
| Insertion intégrée de référence | EG1 historique limité, non équivalent à CP1 ; EN1 au pas fin refusé |
| Rétention PT1 | 6/6 terminés, porte refusée ; ouverture de graphe finale dans une graine, fuite dynamique non démontrée |
| Recyclage RF1 | 9/9 terminés, deux protections refusées ; aucun réemploi strict incorporé, outil parfois perdu |
| Récupération FR1 | 6/6 terminés,0 erreur ; fast0/3, slow1/3 ; deux portes refusées. Pas de relance de taux |
| Transport ouvert OB1 | 6/6 terminés, bilan exact et vrais flux ; précurseurs seuls sous Langevin, hors CP1 |
| Calcul C++ et CUDA | CFN1 hybride vérifié sur un préfixe CP1. CRM1 résident accélère le bain de mélange Langevin sur la RTX 4060 Laptop. |
| Calculs actifs à cette clôture | Aucun ; CF1 conserve sa pause scientifique |
| Maintien intégré | Non démontré ; flux CP1, pertes compatibles, bilan L, information et diversité des outils restent ouverts |

L'audit Astra est conservé dans [son fichier original](RECOMMANDATIONS_GPT6_ASTRA.md).
La [revue](research/ASTRA_REVIEW.md) retient ses idées en précisant leurs limites.
Les vingt recommandations ne déclenchent pas vingt campagnes.

Prochaines décisions :

Le chantier demandé vise un calcul CUDA résident et une référence CPU
maintenue. Le prochain jalon technique est le transfert vers un préfixe
réactif avec mesure des synchronisations. Les décisions biologiques
ci-dessous restent nécessaires au premier test intégré. [Bilan du lot57](research/BATCH_57.md)

1. Fermer le bilan ouvert minimal du co-recruteur équipé, en choisissant la
   représentation d'atomes actifs/IDs et les sorties de matières, dont L.
2. Définir le test de renouvellement sous pertes partielles/redondance ; adapter
   provenance et observateurs réversibles avant de coupler à mixed_synthesis.
3. Dé-risquer l'expressivité : le canal de capture courant ne distingue pas PG/PF
   libres. Garder le polyvalent pour le premier maintien et concevoir une extension
   réutilisable ou une autre architecture avant toute recherche de sélectivité.

Visualisation : EG1 reste la démo intégrée historique recommandée, sous Langevin,
avec les limites EN1 affichées. CP1 se voit dans **Résultats locaux**. OB1 est
un diagnostic sans fenêtre, pas une nouvelle démo de cellule. Les anciennes
preuves et paliers du registre gardent leur candidat/domaines explicites.
