# Lot64 — Capture coopérative résidente en mécanique CP1

## Mécanisme

Extension de RCT1. Après les libérations, un noyau recalcule les groupes
matériels admissibles pour chaque site à partir des occupations de ses
voisins directement liés. Les candidats utilisent ce masque et le
symbole du site. La réservation par ligand conserve un seul gagnant.
L'application des réservations lit aussi les propositions gagnantes
des sites adjacents. Deux sites voisins ne peuvent valider ensemble
des ligands de groupes différents ou de même symbole. La priorité
départage les réservations incompatibles. Les masques sont recalculés
avant que le champ de capture et les ressorts soient réévalués.

La grille, le mouvement et toutes les forces mécaniques de CH1
restent actifs. Ce pilote maintient les autres transitions gelées.
Le CPU ne décide pas à chaque tick. Aucun nouveau primitif, règle
de reconnaissance ou label d'agrégat ajouté à CP1.

La décision lit un instantané de réservations. Un candidat peut être
écarté par un voisin mieux classé qui perd lui-même ailleurs. Comme
dans RCT1, le candidat écarté attend un tick. C'est une différence
d'arbitrage à caractériser par rapport à l'ordre séquentiel CPU.
La garantie actuelle porte sur la validité locale des liens, et sur
le respect des conditions du champ, avec un contrôle de réciprocité
et un bilan des fixations et libérations.

## Contrôles

Deux sites liés ayant des symboles différents, avec deux ligands
distincts et initialement à portée. Les deux liaisons se forment
quand les groupes concordent. Une seule se forme dans le témoin
à groupes différents. Les masques CUDA concordent avec
`MixedCapture.binding_allowed` pour l'occupation résultante.
Le contrôle RCT1 à deux sites pour un ligand conserve un seul
gagnant et le découpage des blocs ne change pas le résultat.

## Mesure

CH1, tranche de capture avec contrôle actif, RTX 4060 Laptop et i7-13700H.
Ligands rapprochés et pleine activité des sites dans les trois modes.
Médiane de trois fenêtres de 500 pas après 250 pas, sans observateur.
Les valeurs GPU et CPU ont leurs propres tirages de réaction.

| Billes | Graine | CPU | Hybride, capture CPU | Capture CUDA | Gain sur CPU | Gain sur hybride |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 302 | 1 | 285,24 ms | 109,88 ms | 62,42 ms | 4,57× | 1,76× |
| 2 118 | 1 | 1 120,76 ms | 244,74 ms | 94,28 ms | 11,89× | 2,60× |
| 2 118 | 2 | 1 141,53 ms | 245,21 ms | 90,15 ms | 12,66× | 2,72× |

À 2 118 billes, 65 et 66 fixations, 18 et 16 libérations, puis
47 et 50 sites occupés sur CUDA. Le CPU termine à 51 et 52.
Ce crible vérifie l'activité, les invariants et le débit. La
cinétique comparée sous compétition reste à établir sur un ensemble
prédéfini plus large. Le gain de CP1 complet reste celui du lot62.

## Complétion

Capture indépendante et coopérative sur GPU dans le pilote, ainsi
que l'effet des liaisons sur le mouvement. CP1 ordinaire reste
hybride. Priorité à la formation H/T avec le delta énergétique
compétitif. Puis P/R, appariement, ligation, faces et échanges,
bruit mécanique et état résident de reprise, et réception complète.
Estimation centrale de six lots, plage cinq à huit, pour ce
périmètre entièrement résident. Elle suppose un arbitrage local
qui passe les contrôles scientifiques. Aucun gain final imposé.

```powershell
python -m experiments.probe_cuda_capture_ticks --mixed --active-control --seed 1
python -m experiments.probe_cuda_capture_ticks --mixed --active-control --particles 2118 --seed 2
python -m unittest tests.test_resident_motion -v
```

La recette CH1 et la mise à l'échelle sont celles du lot62. Le code
du pilote et les noyaux sont figés par le commit. Journaux bruts locaux.
O-01 reste sous-cas. [Critères de clôture](CUDA_COMPLETION.md)
