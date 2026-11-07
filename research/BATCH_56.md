# Lot56 — première tranche C++ et CUDA

7 novembre 2026. [Plan](BATCH_56_PLAN.md), [mesures compactes](BATCH_56_RESULTS.json),
[utilisation](../docs/COMPUTE_BACKENDS.md).

Le noyau commun CFN1 calcule les forces de contact, ressort et angle à partir
de tableaux d'interactions. Les relations incidentes sont rangées par bille.
Chaque sortie appartient à un seul thread CUDA. La somme locale suit l'ordre
de la référence, en double précision. Les chemins C++ et CUDA compilent les
mêmes expressions. La référence Numba reste sélectionnée par défaut.

Dans la copie, deux décisions consultent les voisins liés sans reparcourir
toutes les liaisons. La table d'adjacence est construite au début du tick après
les éventuelles pertes, puis mise à jour après chaque ligation acceptée.
Les propositions conservent leur ordre. Le delta du registre chimique est
nul. La limite du voisinage et les critères de réaction ont le même sens.

Le crible compare un instantané CP1 de 302 billes et 600 pas sur le cas
CH1_integrated_s1. Les forces, positions, vitesses, état chimique et PRNG
concordent sur ce préfixe. Chaque backend reprend exactement son propre
checkpoint sur cette machine. Les préfixes CPU archivés FR1, CH1 isolé et
CH1 intégré sont aussi reproduits exactement à 5 unités simulées.
La commande ordinaire du simulateur a été vérifiée en C++ et CUDA.
La suite de 304 tests passe.

## Lecture des mesures

Sur la RTX 4060 Laptop, la simulation hybride effectue une copie vers le GPU
et un retour vers le CPU à chaque évaluation. Le cas CP1 court est plus lent
qu'en Numba. Le C++ comprend lui aussi le coût de préparation des listes
incidentes à chaque évaluation. Ces chemins servent de référence au portage.

| Mesure | Numba | C++ | CUDA |
| --- | ---: | ---: | ---: |
| Appel complet des forces sur un instantané, µs | 2,8 | 97,9 | 747 |
| 500 pas intégrés après 100 pas d'échauffement, s | 0,72 | 0,64 | 0,94 |

Les appels de forces sont les médianes de trois séries. Les temps du pas
intégré sont trois exécutions individuelles, une par backend. L'ordre Numba/C++
a varié entre deux relevés. À cette échelle, le coût hybride est le résultat
à retenir pour décider de la prochaine étape de portage.

Le test résident soumet des lots de 1, 32 et 100 répétitions du même état.
Le lot de 100 évalue les forces élémentaires sur 30 200 billes au total.
Le nombre de billes est réparti entre bains indépendants, avec listes
incidentes et positions déjà chargées. Ce test mesure un noyau, tandis
que le préfixe hybride inclut voisinage, forces supplémentaires, réactions
et mouvement. Les mesures du préfixe excluent rendu et observateurs.
Les temps par appel résident sont de 47 µs pour un état, 108 µs pour 32
et 178 µs pour 100.

## Décision suivante

Garder la sélection par scénario et les contrôles croisés. La prochaine
tranche de portage doit grouper les pas mécaniques sur données résidentes et
comparer la recherche de voisins sur ces données. Les forces des ports,
des captures et de la membrane restent sur CPU. Il faut les inclure pour
mesurer le gain sur un bain CP1 complet. Un arbitre parallèle de réactions
nécessitera une comparaison des cinétiques s'il modifie l'ordre effectif.

CFN1 ajoute une preuve logicielle au sous-cas O-01. L'homéostasie, les flux
dans CP1 et la stabilité à long terme restent des objectifs biologiques à
traiter. Les mesures sont reproductibles avec
`python -m experiments.benchmark_native_forces` et la recette CH1 enregistrée.
