# Calcul CPU et CUDA

Le moteur sélectionne le calcul des contacts, ressorts et angles de base au
lancement d'une simulation. Chaque scénario peut définir
`"engine": {"force_backend": "cuda"}` ou utiliser `--force-backend` en ligne
de commande. Le checkpoint mémorise cette sélection et la reprend au chargement.
L'ouverture d'un scénario JSON dans la GUI utilise la sélection du scénario.

| Valeur | Calcul et installation |
| --- | --- |
| `numba` | Mode CPU de référence par défaut avec les dépendances ordinaires du projet |
| `cpp` | Noyau C++ partagé compilé au premier lancement avec `g++`. Définir `AUTOPOIETIC_CXX` pour choisir un compilateur compatible avec les options GNU. |
| `cuda` | Le même noyau compilé au premier lancement avec CuPy et NVRTC. La machine de validation utilise CuPy 13.3 et CUDA 12.5. |

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

Pour le moment, le moteur envoie les tableaux au GPU lors de chaque appel de
forces et récupère leur somme pour le pas CPU. Le benchmark mesure aussi un
noyau sur des tableaux déjà résidents. Le lot de cent états y répète un même
instantané. Voir les mesures et le périmètre dans [le bilan CFN1](../research/BATCH_56.md).
