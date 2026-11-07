# Lot61 — Ticks lipidiques compilés et bain ouvert sur CUDA

## Ticks des faces

Hypothèse. Compiler le parcours des candidats et calculer les distances
axiales par lot peut réduire le coût CPU sans changer l'arbitrage.
La formation et l'échange partagent la projection géométrique existante et
une mesure de déformation axiale. La géométrie est réutilisée pendant un
tick lipidique. Près du seuil de rupture, la classification reprend
la norme scalaire de la référence. Le parcours compilé tire les permutations
et les essais dans l'ordre d'origine. Il suspend le parcours à chaque
proposition qui arrive à la décision CPU. L'occupation après acceptation
ou refus est relue en reprenant le parcours. Le gate d'énergie et les
conflits gardent leur sémantique. Aucun primitif, paramètre ou changement
de portée ajouté.

Empreinte identique sur 720 ticks appariés avec `dc81a32`, six graines,
ports additifs et compétitifs, sans et avec gate. 350 échanges, 302
ruptures, 175 acceptations et 950 refus énergétiques. L'empreinte inclut
liaisons, événements, valeurs des statistiques et état RNG de chaque tick.
Valeur SHA-256 `8f6be814add2de84432cd3a176795710bbc366ef14668bef07c10d198b107c35`.

## Bain ouvert

`open_bath` accepte la mécanique CUDA résidente sans paroi réfléchissante.
Le CPU conserve la source externe et la règle d'absorption. Aux
entrées et sorties, le moteur remappe l'état et invalide le graphe
lié aux anciens tableaux. Le coût des réallocations et des nouvelles
captures reste à mesurer à flux élevé. Une future capacité réservée
n'a de sens que si ce coût est mesuré comme dominant.

Le contrôle de quatre unités, depuis zéro bille, conserve le bilan
par espèce, le calendrier, les IDs, les événements d'entrée/sortie
et l'état RNG sur les modes CPU et GPU, avec et sans stérique.
La reprise CUDA depuis un checkpoint vide est exacte. Il s'agit
du banc de précurseurs seul. Le bain cellulaire ouvert n'est pas
validé par ce contrôle.

## Mesure intermédiaire

CH1 intégré graine 1, 302 billes. Trois fenêtres de 1 000 pas après
250 pas, sans observateur, RTX 4060 Laptop et i7-13700H. Mesure avant/après
optimisation du parcours, avec `dc81a32` comme référence avant.

| Chemin | Avant | Après |
| --- | ---: | ---: |
| CPU Numba, médiane | 1,121 s | 0,930 s |
| Mécanique CUDA résidente, médiane | 0,832 s | 0,692 s |
| Formation et échange de faces, profil du chemin résident | 0,413 s | 0,118 s |
| Ensemble des ticks, profil du chemin résident | 0,766 s | 0,465 s |

Le chemin CUDA met environ 17 % de temps en moins sur ce préfixe,
comme le chemin CPU. Le rapport CPU/CUDA après est **1,34×** à chaud.
Les phases de faces passent environ 3,5× plus vite dans le profil,
et les ticks représentent encore 61 % du temps profilé résident.
La formation des lipides, en particulier le calcul d'énergie H/T,
est maintenant le premier poste de réaction. Le temps d'attente
à la lecture CUDA reste à séparer du temps de transfert effectif.
Mesurer ces postes à plusieurs tailles avant de décider d'un autre
transfert GPU des réactions. O-01 reste sous-cas.

```powershell
python -m experiments.verify_face_proposals
python -m experiments.verify_resident_fields
python -m unittest tests.test_resident_motion -v
```

Pour la référence exacte des faces, exécuter le même script avec le
`simulator` de `dc81a32` sur le chemin Python. Le profil reprend la recette
CH1 et la commande du [lot60](BATCH_60.md). Journaux bruts locaux.
Aucune preuve biologique modifiée. [Critères de clôture](CUDA_COMPLETION.md)
