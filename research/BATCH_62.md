# Lot62 — Mesure CP1 à la taille de la cellule et coût des propositions H/T

## Recette

Le test confronte l'hypothèse d'un gain CUDA qui augmente rapidement avec
le nombre de billes. CH1 intégré graine 1 à 302 billes sert de référence.
Pour 1 000 et 2 118 billes, la même chimie est utilisée. Le rayon, la boîte et
le paquet intérieur sont agrandis. Les stocks intérieurs suivent l'aire,
les unités lipidiques suivent le périmètre et les assemblages préparés sont
répliqués avec le stock. La recette à 2 118 billes reprend le nombre de
billes de l'intégration historique MIN1M. MIN1M tourne sous un autre hook
et le test agrandi est une charge CP1, sans preuve de maintien.

RTX 4060 Laptop et i7-13700H. Une graine, trois fenêtres de 500 pas après
250 pas, avec l'observateur CH1 sans sauvegarde de trajectoire. Le temps
de réaction est mesuré autour du hook réel. Le coût d'initialisation est
enregistré séparément. Les répétitions ne forment pas un intervalle
statistique sur la population de cellules.

## Décision de ce lot

Les paires géométriques de cœur et de capture sont indexées par incidence
une fois par tick. Une proposition H/T ne lit que les paires touchées,
dans l'ordre d'origine. Les valeurs identiques avant/après ne sont plus
recalculées. Pour les ports compétitifs, le voisinage et la géométrie
des lipides existants sont partagés entre propositions. Les arêtes du
lipide hypothétique sont fusionnées dans l'ordre lexicographique.
Après une naissance acceptée, la géométrie partagée est invalidée.
Les tirages, les états d'occupation et le gate restent ceux du moteur.

À 2 118 billes, le préfixe CPU de 1 750 pas conserve les positions,
l'état chimique, la mécanique et le RNG à l'identique du commit
`0ef6ce8`, avec trois naissances lipidiques.
Empreinte SHA-256 `903558938ede09fb7bbb4d6a61faa2d69dd8bbe8360f710dc5d909fe797ad4b9`.

## Débit complet

Médianes en secondes pour 500 pas. Le gain est CPU/CUDA.

| Billes | CPU avant | CUDA avant | CPU après | CUDA après | Gain après |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 302 | 0,469 | 0,339 | 0,454 | 0,319 | 1,43× |
| 1 000 | 1,399 | 1,094 | 1,238 | 0,842 | 1,47× |
| 2 118 | 3,008 | 2,473 | 2,267 | 2,004 | 1,13× |
| 2 118, répétition isolée | — | — | 2,281 | 1,390 | 1,64× |

La dispersion CUDA à 2 118 billes touche surtout la partie extérieure
au hook de réaction. Les deux médianes de réaction sont proches, 1,088 s
et 1,074 s. Le reste passe de 0,916 s à 0,316 s entre les deux essais.
Le profil inclut l'attente à la lecture CUDA. La cause précise de la
dispersion reste à isoler avant la mesure de réception.

Avec un CPU autour de 2,27 s, 10× exige environ 0,23 s sur GPU. Le seul
coût des réactions impose un plafond proche de 2,1× s'il reste inchangé,
même avec une mécanique gratuite. Dans la répétition la plus rapide, la
part extérieure aux réactions dépasse elle aussi 0,23 s. Le débit complet
à 2 118 billes ne montre donc pas de saut vers 10×. Cette cible demanderait
de réduire fortement à la fois la réaction et le coût par bloc.

Le profil instrumenté après optimisation compte 3 561 propositions H/T
sur 100 ticks. Le hook de réaction prend 1,499 s sur 1,803 s, dont 0,635 s
pour les deltas H/T et 0,241 s pour la contribution compétitive incluse.
Cette étape reste une cible de calcul par lots. L'ordre d'application
des propositions et les collisions d'occupation restent à préserver.

## Réception et estimation

Trois à cinq lots restants, quatre comme estimation centrale pour un
portage évalué à la taille cible. Porter ou écarter sur mesure les deltas
et candidats des réactions, réduire les attentes et la variabilité par
bloc, puis vérifier les deux modes sur plusieurs graines et tailles.
Le facteur de réception découlera de ces mesures. Obtenir 10× n'est
pas compris dans cette estimation d'effort.

```powershell
python -m experiments.benchmark_cp1_scaling
python -m experiments.benchmark_cp1_scaling --particles 2118
```

Pour le point avant, utiliser le même pilote avec le `simulator`
de `0ef6ce8`. Journaux bruts locaux. O-01 reste au palier sous-cas.
[Critères de clôture](CUDA_COMPLETION.md)
