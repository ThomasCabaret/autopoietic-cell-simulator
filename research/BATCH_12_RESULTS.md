# G1 : insertion conservée, robustesse incomplète

27 octobre2026. Trois essais terminés à1500, zéro erreur. Recette figée :
[M1G1](campaign_recipes/M1G1_20261027T074404542747Z/manifest.json), code8d73330.
Post-traitement reproductible : `python experiments/analyze_batch12.py <campagne>`.
Sources, comptes de l'audit, historique primaire, durée et nombres d'échanges
vérifiés pour les trois essais ; données complètes conservées localement.

| Graine | Insérés / persistants10 | Fermée | Classable | Fuite observée | Échanges | Exposition brute / sous garde |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1 / 1 | 0,8404 | 0,9860 | 0/24 | 2 | 13,67 / 8,16 |
| 1 | 2 / 2 | 0,8414 | 0,9880 | 0/24 | 8 | 26,88 / 20,90 |
| 2 | 2 / 1 | 0,7587 | 0,9693 | 0/24 | 10 | 56,70 / 35,62 |

Premières insertions dans un contour fermé :290,5 /527,5 /340,5. Les expositions
sont des temps-face pré-réaction approximatifs, pas un risque intégré exact.
Les nombres persistants reposent sur l'échantillonnage0,5 et ne garantissent
pas l'absence d'ouverture intermédiaire. L'inconnu n'est jamais de la rétention.

Comparaison B ancien sur mêmes graines/horizon : fermeture0,5901/0,8051/0,8261,
insertions1/2/5. Le garde corrige fortement le pire essai0 mais dégrade la fermeture
de2 et réduit les insertions de ce dernier. Le critère conjoint reste2/3 dans les
deux variantes. Les PRNG divergent après un changement d'éligibilité : cette
comparaison limitée ne prouve pas une dominance ni une causalité universelle.

Conclusion : activité conservée sous le garde, nouvelle hypothèse non inhibitrice,
mais G1 n'est pas une membrane robuste validée. Les trois essais commencent
avec un anneau préparé ; ils ne prouvent pas son auto-assemblage initial à grande
taille. G/F, vraie nourriture et fabrication de L n'y sont pas présents.

Décision : conserver B et G1 comme références imparfaites, G1 comme banc d'essai
provisoire pour le transport. Ne pas ajouter un deuxième garde pour sauver le
seuil0,8. Tester maintenant le bain physique commun, les atomes P/R réels et les
états libres/liés ; si cela échoue, réexaminer la représentation avant réglage.
