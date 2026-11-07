# Lot58 — Le premier bain réactif sur la mécanique résidente

Objectif de transfert. Vérifier que les graphes CUDA survivent aux ticks de
chimie, avec synchronisation à la cadence de référence et invalidation des
forces même quand aucun événement public n'est émis. Le modèle de copie
sans champ de capture ni double face isole le coût de cette interface.
Tester l'orientation d'un couple de rungs, les changements de liaisons,
la reproductibilité après reprise et les événements du préfixe CPU/GPU.
Les forces et la cadence chimique restent celles du scénario.

Vérifier en parallèle où CP1 passe son temps. L'orientation est réutilisable
par CP1. Ses champs libres, ports et barrière restent des tests de transfert.
Le crible doit révéler tôt si la préparation et les synchronisations
annulent l'avantage du calcul résident entre ticks.

## Résultats

- Copie Langevin LT2, graine 0, 108 billes. Après 1 000 pas, deux nouvelles
  liaisons de squelette et six sites appariés. CPU et CUDA ont le même
  état chimique et le même RNG. Les écarts maximaux mesurés sont de
  4,11e-13 en position et de 3,13e-12 en vitesse. La reprise CUDA après
  507 pas restitue exactement positions, vitesses, forces, chimie et RNG.
- Le GPU conserve positions, vitesses et forces entre ticks. Les termes
  mécaniques sont reconditionnés seulement quand la topologie change.
  Le graphe est réutilisé tant que les adresses des buffers et dimensions
  restent stables. L'orientation lit deux rungs appariés, le CPU garde les
  réactions. Une copie contiguë publie positions, vitesses, forces et
  stabilité ensemble. Aucun nouveau primitif ou paramètre de chimie.
- Sur CP1, CH1 intégré graine 1, les propositions H/T réutilisent deux
  listes géométriques pendant le même tick. Occupations, catégories et
  énergie continuent d'être lues au moment de chaque proposition.
  Le profil apparié passe de 7 184 à 6 800 appels au voisinage par
  1 000 pas. Les médianes globales de 1,225 s et 1,202 s restent trop
  proches au vu de la dispersion pour conclure à un gain de débit CPU.
  Les réactions prennent 0,764 s sur 1,570 s dans le profil courant.
  Porter uniquement la mécanique laisse donc une part importante du coût.

Le crible sur le modèle de copie donne 168,76 ms CPU et 123,48 ms CUDA
pour 1 000 pas, soit 1,37× à chaud. Trois fenêtres après 250 pas,
sans observateur, RTX 4060 Laptop et i7-13700H. C'est une mesure de
l'interface aux ticks, sans les champs de capture, ports et barrière
du bain cellulaire. Aucune mesure finale de speedup CP1.

```powershell
python -m experiments.benchmark_reactive_motion demonstrators/configs/demo_binary_copy_langevin.json --backends numba cuda-resident
python -m unittest tests.test_resident_motion -v
```

Pour le profil CP1, extraire le champ `scenario` de la tâche
`CH1_integrated_s1` dans le [manifest CH1](campaign_recipes/CH1_20261106T073608844143Z/manifest.json)
et passer le JSON à `benchmark_reactive_motion --profile`. La référence
avant optimisation est le commit `753d949`. Journaux bruts locaux.

Décision. Prochaine tranche sur la capture libre et la barrière
segment–particule, suivie des ports lipidiques. Après la mécanique CP1,
profiler séparément la préparation et l'arbitrage des réactions.
O-01 reste au palier sous-cas. [Critères de clôture](CUDA_COMPLETION.md)
