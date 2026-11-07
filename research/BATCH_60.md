# Lot60 — Ports mutualisés et premier CP1 résident

## Choix de factorisation

Les ports lipidiques partagent la géométrie de quatre billes et la projection
de deux forces de port sur les extrémités réelles. Cette projection est
commune aux ports libres, compétitifs et liés, en Numba comme en CUDA.
Le calcul libre conserve la dérivée du potentiel gaussien tronqué. Le calcul
lié utilise sa continuation harmonique. Le calcul compétitif ajoute deux
sommes locales par face et leur effet sur la dérivée. Le nombre de voisins
entre dans le résultat de ces sommes. Un simple changement de constante
ne reproduirait donc pas la compétition dans un mélange dense.

Les trois variantes CUDA partagent le calcul de géométrie, la projection
et la même grille que la capture et les contacts. La compétition fait
trois passes sur les candidats locaux et réutilise les tableaux par face.
L'additif exécute uniquement la passe finale. Les ports liés consultent
leur partenaire direct. Aucune approximation, constante de chimie, règle
de cellule ou requête d'agrégat ajoutée. Une abstraction unique pour
ressort, barrière et port compétitif n'éliminerait ni la projection
segment–particule ni les réductions de voisinage.

## Transfert

`mixed_synthesis` sous Langevin accepte `cuda-resident`. Le GPU calcule
toutes les forces mécaniques de CP1. Le CPU conserve la cadence, l'ordre
et les tirages des réactions. Les occupations, liaisons et types de billes
sont actualisés aux ticks. Les graphes CUDA sont réutilisés à dimensions
stables et recréés si des buffers de topologie changent de taille.

Sur CH1 intégré graine 1, les forces lipidiques concordent sur quatre
instantanés. La trajectoire appariée sur 3 750 pas conserve les liaisons
et le RNG, avec des écarts maximaux en fin de préfixe de 1,78e-14 en
position et 1,75e-13 en vitesse. Un contrôle avec deux voisins pour
une même face distingue effectivement compétitif et additif et vérifie
la force liée. Un autre force une naissance lipidique pour exercer la
mise à jour du type, des ressorts et des ports au tick, puis la reprise
CUDA exacte. Les contrôles construits n'ajoutent pas de preuve de
viabilité. La CLI exécute aussi la recette CH1 et écrit son checkpoint.

## Profil de décision

Sur 302 billes, RTX 4060 Laptop et i7-13700H, trois fenêtres de 1 000
pas après 250 pas, sans observateur. Numba 1,114 s et CUDA résident
0,916 s en médiane, soit **1,22× à chaud sur ce préfixe**. Dispersion
CPU 1,081–1,481 s, GPU 0,828–0,977 s. Mesure intermédiaire, hors
démarrage et avant optimisation des réactions. Dans le profil instrumenté,
0,740 s sur 1,028 s passent dans les réactions CPU. Les deux opérations
lipidiques de mise à jour et d'échange des faces prennent ensemble
environ 0,390 s. Elles deviennent le prochain goulot à décomposer en
géométrie, éligibilité et arbitrage.

```powershell
python -m experiments.verify_resident_fields
python -m unittest tests.test_resident_motion -v
```

Pour le profil, extraire la recette CH1 intégrée graine 1 comme au lot58,
puis passer `--backends numba cuda-resident --profile` à
`benchmark_reactive_motion`. La source et la recette sont traçables par le
commit du lot et le [manifest CH1](campaign_recipes/CH1_20261106T073608844143Z/manifest.json).
Journaux bruts locaux. O-01 reste au palier sous-cas. [Clôture CUDA](CUDA_COMPLETION.md)
