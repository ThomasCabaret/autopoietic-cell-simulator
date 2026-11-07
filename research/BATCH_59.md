# Lot59 — Capture et barrière sur la grille CUDA

Hypothèse de transfert. Les deux familles de forces peuvent relire la grille
existante et les états locaux connus au dernier tick. La capture exige un
site libre, un ligand libre, un symbole compatible et, quand la coopération
est active, le groupe matériel permis par les voisins liés. Le noyau lit des
masques dérivés de ces états. La barrière exige une liaison lipidique réelle
et une bille d'un rung P/R lié. Elle lit la distance à ce segment, puis
répartit la réaction sur les deux extrémités. Aucun contour ni label de
construction n'est lu. Les fonctions d'énergie des réactions restent sur CPU.

La capture est active dans le mode résident du modèle de copie catalysée,
avec actualisation des descripteurs après un tick. La barrière et la capture
coopérative CP1 sont vérifiées par instantané. Chaque thread écrit la force
de sa propre bille. La recherche de segments utilise la longueur maximale
du pas comme borne de voisinage, sans limiter la longueur physique. Une
liaison étirée peut élargir cette recherche. Mesurer la charge de cette
phase sur CP1 résident avant de décider si un index des segments est utile.

## Vérification

Scénario CH1 intégré graine 1, 302 billes. États produits par la référence
CPU, config inchangée. Forces maximales et écart absolu maximal par famille.

| Pas | Force capture | Force barrière | Écart capture | Écart barrière |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 2,768 | 0 | 4,45e-16 | 0 |
| 250 | 4,180 | 0 | 5,56e-17 | 0 |
| 1 250 | 1,785 | 0 | 2,23e-16 | 0 |
| 3 750 | 1,963 | 2,725 | 4,34e-19 | 0 |

Sur FR1 fast graine 0, copie catalysée en mode résident sur 1 000 pas.
État chimique et RNG identiques au CPU, écart de position nul et
écart de vitesse maximal de 1,12e-16. Ce préfixe n'a ni changement
d'occupation ni nouvelle liaison P/R. Le contrôle ciblé rapproche un
ligand et un site, augmente le taux de capture et désactive la formation
des rungs pour isoler le changement d'occupation. Il vérifie la parité
et la reprise avec le champ actif. Un autre contrôle place une bille
près du milieu d'un segment de longueur 12 pour exercer le voisinage
au-delà des cellules immédiatement adjacentes aux extrémités.

```powershell
python -m experiments.verify_resident_fields
python -m unittest tests.test_resident_motion -v
```

Les manifestes figés sont CH1 `20261106T073608844143Z` et FR1
`20261106T135511017624Z`. Le commit du lot conserve les noyaux et
le vérificateur. Aucune donnée de trajectoire ajoutée et aucun
changement de loi ou de preuve biologique. O-01 reste au palier sous-cas.

Décision. Porter les ports lipidiques libres, compétitifs et liés, puis
brancher les quatre familles de forces sur la mécanique résidente CP1.
La mesure du pas réactif complet et l'optimisation des ticks suivent.
[Critères de clôture](CUDA_COMPLETION.md)
