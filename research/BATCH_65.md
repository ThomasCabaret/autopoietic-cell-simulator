# Lot65 — Saturation par face et énergie de création par lots

## Hypothèse

Réduire la portée des calculs de réaction peut être plus utile que
reproduire sur GPU le parcours CPU actuel. La branche `saturated`
partage la géométrie, le score gaussien tronqué, la projection des
forces et les liaisons explicites des ports compétitifs. Elle remplace
la normalisation par arête par une énergie par face.

Si les voisins proposent des scores p dans [0,1], l'énergie d'une
face vaut −A/2 fois un moins le produit des (1−p). Une paire isolée
retrouve exactement la force et l'énergie précédentes. À plusieurs
voisins, la contribution de la face est bornée par A/2. Le champ
reste continu dans les positions, à topologie fixe. Aucun paramètre,
type, état de port ou helper ajouté. Le calcul ne lit que les
faces géométriquement voisines. La création ou suppression d'un
lien peut toujours changer l'énergie discrètement au tick, comme
avec la loi actuelle.

Le GPU réutilise la géométrie et la projection de force. Une seule
réduction par face remplace les deux réductions compétitives.
Pour une création H/T, on ajoute les facteurs du lipide proposé
aux produits des faces existantes, sans reconstruire un voisinage
de trois rangs. Pour un échange latéral, les énergies modifiées
sont sur les faces directement touchées et leurs voisines. Le
calcul de référence lit leurs contacts jusqu'au deuxième rang.
Le pilote CUDA évalue les énergies de créations indépendantes
à partir d'un instantané. L'arbitrage de créations concurrentes
et leurs autres contributions énergétiques restent à intégrer.

## Contrôles et débit

Les tests couvrent le cas binaire, le gradient en mélange encombré,
la création et l'échange contre l'énergie totale, et les forces
CPU/CUDA. Le crible d'énergie part de CH1 agrandi à 2 118 billes,
graine 1. On ouvre une liaison sur quatre et place 16 paires H/T
près de lipides pour obtenir des valeurs non nulles. Même géométrie
pour les deux lois. Médianes de cinq répétitions après échauffement.

| Contribution des ports pour 75 propositions, dont 15 non nulles | Temps |
| --- | ---: |
| Compétitif CPU, calcul local courant | 2,289 ms |
| Saturation par face CPU, produits réutilisés | 0,825 ms |
| Saturation par face CUDA, lot avec préparation et lecture | 0,705 ms |

Erreur absolue CPU/CUDA nulle sur ce crible. La différence maximale
entre lois est de 1,58 unité d'énergie sur les poses testées.
Le gain de 3,25× compare deux lois et deux backends sur cette
contribution. À loi saturée commune, le ratio CPU/CUDA est 1,17×
pour ce petit lot, transferts compris. Aucun facteur global
déduit de cette mesure.

Premier crible de mécanique et réactions complètes à 2 118 billes
avec observateur, 500 pas après échauffement, graine 1. Pour le
chemin résident avec réactions CPU, la mesure est de 2,07 s en
compétitif et 2,12 s en saturé. Le débit complet CUDA n'a donc
pas de gain mesuré dans cette comparaison courte. Le calcul par
lots des énergies est encore hors du scheduler de réaction.

## Crible d'assemblage depuis lipides isolés

CR1 graines 0 et 1, 52 lipides isolés, 20 unités, mêmes paramètres
et initialisations. Aucune fermeture observée sur cet horizon.

| Graine | Liens compétitif à 20 | Liens saturé à 20 | Plus grand groupe compétitif / saturé à 20 |
| ---: | ---: | ---: | ---: |
| 0 | 29 | 18 | 7 / 4 |
| 1 | 32 | 24 | 5 / 7 |

La variante s'assemble avec une cinétique différente. Ce crible
ne permet pas de conclure sur les vésicules à l'horizon CR1 de
8 000, ni sur l'insertion depuis l'intérieur. La variante reste
opt-in. Décision suivante : comparer les occasions et acceptations
de liaison dans la fenêtre courte et mettre à l'épreuve l'arbitrage
commun sur les créations. En parallèle, la loi de référence peut
être évaluée avec des sommes incrémentales sans changer sa chimie.
Choisir la loi à partir des comportements et du coût du pas complet.

```powershell
python -m experiments.compare_lipid_saturation
python -m experiments.benchmark_cp1_scaling --particles 2118 --port-potential saturated
```

Recettes CH1 et CR1 des lots62 et53. Noyaux et pilotes figés par
le commit. O-01 reste sous-cas. [Critères de clôture](CUDA_COMPLETION.md)
