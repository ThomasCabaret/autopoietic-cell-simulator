# Lot63 — Premiers ticks de capture sans arbitrage CPU

## Hypothèse et méthode

Inspiré de la séparation entre propositions et opérations structurelles
d'[ALIEN](https://github.com/chrxh/alien/blob/develop/source/EngineKernels/ObjectConnectionProcessor.cuh#L1720).
Une grille résidente suffit à produire des propositions de capture locales.
Le premier crible isole la capture P/R indépendante de FR1. Les rungs
et les appariements préexistants restent en place. Les autres réactions
sont gelées. Le mouvement Langevin, les forces du moteur, l'attraction
libre et les ressorts de capture restent actifs. Aucun nouveau primitif
ni mécanisme chimique ajouté à CP1.

Trois phases CUDA. Libérer les sites selon leur taux. Chaque site libre
propose un ligand compatible dans le rayon local, avec un tirage et une
priorité par paire. Chaque ligand accepte la proposition de meilleure
priorité et les deux partenaires sont mis à jour réciproquement. Les
sites et ligands sont disjoints. Une liaison est lue par la mécanique
dès le pas suivant. Chaque graphe exécute 25 pas avec cinq ticks.
Le moteur partagé peut publier l'état après 250 pas, soit 50 ticks.
Les tirages Langevin sont encore préparés et chargés par blocs depuis
le CPU. Le bruit de réaction provient d'un compteur sur le GPU.

L'arbitrage est une variante expérimentale. Le site qui perd une
réservation attend le prochain tick. Le balayage CPU peut essayer
une autre paire dans le même tick. Les taux des rencontres isolées
sont conservés par construction, mais les taux effectifs sous
compétition et la fidélité sur les réactions couplées restent à
tester. Le test à deux sites et un ligand vérifie qu'un seul site
gagne, que les liens sont réciproques et que deux découpages
produisent la même trajectoire GPU. Ce prototype est accessible par
le pilote, sans changer le mode CP1 de production ni son format de
checkpoint.

## Mesure

RTX 4060 Laptop et i7-13700H. Trois fenêtres de 500 pas après 250 pas,
médiane, sans observateur. Dans le contrôle positif, des ligands
commencent près des sites et tous les sites ont une activité de un.
Ces conditions communes aux trois modes rendent les événements
observables pendant le court benchmark. Au réglage FR1 initial,
les occupations sont restées proches de zéro sur cet horizon.

| Billes | Graine | CPU | Hybride, réactions CPU | Capture résidente | Gain sur CPU | Gain sur hybride |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 150 | 0 | 97,48 ms | 81,42 ms | 36,30 ms | 2,69× | 2,24× |
| 2 118 | 0 | 691,66 ms | 182,73 ms | 69,66 ms | 9,93× | 2,62× |
| 2 118 | 1 | 720,53 ms | 179,69 ms | 63,20 ms | 11,40× | 2,84× |

À 2 118 billes, le GPU a enregistré 106 et 103 fixations, 27 et 25
libérations, et termine avec 79 et 78 sites occupés. La référence
CPU termine avec 80 et 79. Le bilan fixation/libération et la
réciprocité des liens sont vérifiés. Deux graines suffisent ici
pour établir que le prototype traite des événements actifs. Une
validation statistique des cinétiques nécessite davantage de cas.
Le facteur du CP1 complet reste celui mesuré au lot62.

## Complétion

- Mécanique de CP1 fermé et transport ouvert validés en CUDA résident.
- Capture indépendante portée avec arbitrage, mouvement et plusieurs
  ticks dans le même graphe. Capture coopérative encore à transférer.
- Restent la formation P/R et H/T avec leurs énergies, l'appariement
  et la ligation, les faces lipidiques et les conflits portant sur
  des états lus par les voisins. Le bruit mécanique doit passer sur
  GPU pour supprimer les chargements périodiques, puis les sorties
  et reprises du nouveau chemin doivent être vérifiées.
- Prochaine porte. Mesurer les deltas H/T par lots à la taille de
  2 118 billes, avec arbitrage qui tient compte des occupations et
  des dépendances de l'énergie compétitive. Comparer au CPU avant
  d'élargir le scheduler aux autres transitions.

```powershell
python -m experiments.probe_cuda_capture_ticks --active-control
python -m experiments.probe_cuda_capture_ticks --active-control --particles 2118 --seed 1
python -m unittest tests.test_resident_motion -v
```

Le scénario de base est FR1 `20261106T135511017624Z`. La recette et
les noyaux sont conservés par le commit. Journaux bruts locaux.
O-01 reste sous-cas. [Critères de clôture](CUDA_COMPLETION.md)
