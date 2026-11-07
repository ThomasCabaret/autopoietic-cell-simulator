# Calcul CPU et CUDA

Le moteur sélectionne le backend mécanique au
lancement d'une simulation. Chaque scénario peut définir
`"engine": {"force_backend": "cuda"}` ou utiliser `--force-backend` en ligne
de commande. Le checkpoint mémorise cette sélection et la reprend au chargement.
L'ouverture d'un scénario JSON dans la GUI utilise la sélection du scénario.

| Valeur | Calcul et installation |
| --- | --- |
| `numba` | Mode CPU de référence par défaut avec les dépendances ordinaires du projet |
| `cpp` | Noyau C++ partagé compilé au premier lancement avec `g++`. Définir `AUTOPOIETIC_CXX` pour choisir un compilateur compatible avec les options GNU. |
| `cuda` | Le même noyau compilé au premier lancement avec CuPy et NVRTC. La machine de validation utilise CuPy 13.3 et CUDA 12.5. |
| `cuda-resident` | Voisinage, forces et intégration sur CUDA en Langevin pour `mixing`, `copy` sans substrats `food_pairs` ni double face, `mixed_synthesis` et le banc `open_bath`. Mêmes dépendances que `cuda`. |

Avec CUDA 12.x et un environnement Python qui requiert CuPy, suivre
[l'installation CuPy 13.3](https://docs.cupy.dev/en/v13.3.0/install.html).
La compilation initiale peut prendre quelques secondes. Le C++ réutilise sa
bibliothèque dans le répertoire temporaire. CuPy réutilise son cache de noyaux.
Dans un environnement qui restreint l'écriture des caches, choisir `TEMP` et
`CUPY_CACHE_DIR` dans un dossier de travail accessible. Une erreur de dépendance
interrompt la sélection explicite et indique sa cause.

```powershell
python -m simulator --config demonstrators/configs/demo_current_energy_s0.json --force-backend cpp --duration 1 --no-trajectory
python -m simulator --config demonstrators/configs/demo_current_energy_s0.json --force-backend cuda --duration 1 --no-trajectory
python -m experiments.benchmark_native_forces
```

Le noyau natif reçoit les positions et des tableaux d'interactions locales.
Chaque bille lit ses termes incidents dans un ordre fixé et écrit uniquement
sa propre somme. La compilation CUDA utilise la double précision et désactive
la contraction multiplication-addition. Les relations de liaisons et les
indices spatiaux sont fournis par l'appelant. Cette séparation permet de
choisir les stratégies de voisinage adaptées au matériel.

Le mode `cuda` envoie les tableaux au GPU lors de chaque appel de forces
et récupère leur somme pour le pas CPU. Son benchmark inclut un lot qui répète
un même instantané résident. [Bilan CFN1](../research/BATCH_56.md)

Le mode `cuda-resident` conserve les positions, vitesses, forces et liaisons
sur le GPU. Une grille régulière recense les voisins à chaque pas, puis chaque
bille accumule ses forces en parcourant les cellules adjacentes. Le GPU déroule
des blocs de 25 pas via un graphe CUDA. Les tirages Langevin proviennent du
même générateur CPU, par blocs. L'état est disponible côté CPU aux observations
et au retour de `Simulation.advance`, y compris pour écrire un checkpoint.
Les cadences courtes multiplient les synchronisations.
Sur les modèles réactifs pris en charge, les blocs sont bornés par les ticks de
réaction. Le CPU reçoit la géométrie et applique la chimie, puis le GPU
recalcule les forces avec la topologie et les appariements actualisés.

```powershell
python -m experiments.benchmark_resident_motion --cpp
```

Le benchmark compare le pas complet du bain inerte avec un observateur
léger, sur des dimères à densité initiale comparable. Les chiffres ne
s'appliquent qu'à cette charge. CP1 fonctionne également en CPU, en CUDA
hybride et en CUDA résident. [Bilan CRM1](../research/BATCH_57.md)

[Bilan du transfert réactif](../research/BATCH_58.md) et
[critères de fin de portage](../research/CUDA_COMPLETION.md).
Sur CP1, la mécanique résidente inclut la capture coopérative, la barrière
et les ports lipidiques. Les décisions de réaction restent sur CPU.
[Vérification et profil CP1](../research/BATCH_60.md)

Le banc `open_bath` conserve son calendrier de source et d'absorption CPU.
Il remappe les particules à chaque entrée/sortie et remet à jour les buffers
CUDA. [Vérification et profil du lot61](../research/BATCH_61.md)

Le benchmark réactif à la taille cible se lance avec
`python -m experiments.benchmark_cp1_scaling`. Il rapporte séparément le
temps du hook de réaction et le temps complet avec observateur.
[Résultats CP1 à 302, 1 000 et 2 118 billes](../research/BATCH_62.md)

Le pilote expérimental `python -m experiments.probe_cuda_capture_ticks --active-control`
exécute plusieurs ticks de capture P/R indépendante sur le GPU avec la
mécanique. Les autres réactions sont gelées. Le backend CP1 ordinaire
conserve les réactions CPU. [Périmètre et mesures](../research/BATCH_63.md)

L'option `--mixed` du pilote prend CH1 avec capture coopérative et
mécanique complète. Les autres transitions restent gelées.
[Périmètre et mesures coopératives](../research/BATCH_64.md)
