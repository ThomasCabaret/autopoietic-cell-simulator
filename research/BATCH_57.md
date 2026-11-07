# Lot57 — CRM1, mécanique Langevin résidente

7 novembre 2026. Hypothèse issue de CFN1. En gardant les données de la
mécanique sur le GPU pendant plusieurs pas, le coût des transferts peut
descendre sous le coût du pas CPU. Le bain inerte sépare ce problème
du coût et de l'ordre des réactions.

La grille 2D a pour maille la portée stérique maximale. Chaque bille lit
les neuf cellules voisines et évalue les distances réelles. Les billes
au-delà d'une paroi souple rejoignent une cellule de bord. Les listes de
cellule sont ordonnées par indice pour rendre les sommes reproductibles
malgré l'insertion atomique. Une bille lit ses ressorts et angles via
les mêmes expressions C++/CUDA que CFN1. Elle écrit sa propre force.
Le GPU applique le même pas Langevin en FP64. Le CPU fournit les mêmes
tirages, groupés par 25 pas. Aucun type, liaison, taux, contrôle global
de température ou critère de réaction ajouté. La grille ne consulte
aucun observateur ni identité moléculaire.

## Mesures sur RTX 4060 Laptop et i7-13700H

Médiane de trois fenêtres de 500 pas, après les 25 premiers pas.
Même état initial, même graine 43, même pas .002, même densité initiale,
même cadence d'observation de 25 pas, même lecteur léger. Les temps
comprennent le voisinage, les forces, l'intégration, les tirages,
les transferts et les lectures de l'observateur. Le ratio est le
temps CPU divisé par le temps GPU.

| Billes | CPU Numba | CPU C++ hybride | CUDA résident | Gain sur Numba | Gain sur C++ |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 302 | 44,57 ms | 113,63 ms | 27,05 ms | 1,65× | 4,20× |
| 3 000 | 321,56 ms | 447,98 ms | 70,04 ms | 4,59× | 6,40× |
| 12 000 | 1 304,46 ms | 1 470,21 ms | 363,67 ms | 3,59× | 4,04× |

Le mode C++ est le noyau des forces CFN1 et conserve sa préparation
Python/Numba. La référence de débit est le CPU Numba, le plus rapide
des deux sur ces mesures. Une première exécution du benchmark avait
donné respectivement 2,31×, 3,71× et 2,99× face à Numba. Retenir
l'ordre de grandeur en présence de cette variabilité.

Les ratios du tableau excluent la construction initiale. À 12 000 billes,
la préparation de géométrie prend de 6,2 à 6,5 s sur le CPU dans les trois
modes et domine un essai court. À 302 billes, le premier bloc GPU prend
62 ms après 182 ms de construction et d'ouverture CUDA dans le processus,
avec cache de compilation déjà alimenté. Les valeurs sont propres à cette
machine et à la cadence. Une observation à chaque pas réduit la quantité
de travail regroupable. Le benchmark ne mesure ni l'affichage ni les
statistiques coûteuses de l'observateur de mélange.

## Reproduction et décision

```powershell
python -m experiments.benchmark_resident_motion --cpp
python -m unittest tests.test_resident_motion -v
```

La recette, les résumés de temps et les empreintes de sources sont dans
[le relevé CRM1](BATCH_57_RESULTS.json). Les trajectoires et journaux
bruts restent locaux. Après 25 pas, l'écart maximum mesuré dans le
benchmark vaut 0 en position et au plus 2,23e-16 en vitesse. Un test sur
200 pas couvre contacts, parois et absence de stérique à une tolérance
absolue de 1e-12. La reprise CUDA après 63 pas est exacte, y compris
forces, vitesses, compteur et RNG. Un bloc instable conserve le dernier
état hôte validé.

Conserver le mode explicite `cuda-resident` pour `mixing` sous Langevin.
O-01 progresse dans le palier sous-cas. Aucun changement du palier
cellulaire. Les limites immédiates sont la préparation CPU, le coût
de tri dans une cellule très chargée et les synchronisations imposées
par les réactions. Le prochain jalon est un préfixe CP1 apparié incluant
les forces spécifiques et une topologie mise à jour aux ticks. Mesurer
alors le débit par pas et le coût des synchronisations avant de déplacer
le choix des réactions sur le GPU.
