# Démonstrateurs Windows

Garder ce dossier avec `simulator/`, `scripts/` et `requirements.txt`, ou extraire
le paquet complet fourni dans `deliverables/`. Ne pas lancer les fichiers dans
l'aperçu d'un ZIP Windows : extraire d'abord le dossier.

Python **3.12** doit être installé. Les dépendances sont présentes sur la machine
de développement. Ailleurs, double-cliquer une fois sur `installer.bat` ; cette
installation télécharge les paquets et les place dans `.venv` à la racine.
Les autres lanceurs n'installent rien et n'ont pas besoin du réseau.

| Fichier à double-cliquer | Ce qui est montré |
| --- | --- |
| `01_copie.bat` | Un polymère préparé copie sa séquence dans de nouveaux composants puis les libère |
| `02_membrane.bat` | Un ruban composite droit préparé se courbe et ferme ses deux rangées |
| `03_traduction.bat` | Une matrice G assemble une autre famille F de même séquence |
| `04_controle_sans_gene.bat` | Les mêmes composants d'expression sans squelette génétique initial : aucune ligation |
| `05_fragments_relecture.bat` | Relecture identifiée d'une réussite historique : cinq fragments forment une boucle de quinze unités |
| `06_tout_sans_interface.bat` | Les quatre premiers scénarios, sans rendu, avec vérification automatique des critères |

Les trois premiers sont des **simulations en direct**, à graine fixée. Le quatrième
est aussi calculé en direct. Le cinquième lit une trajectoire archivée ; il ne
prétend pas reproduire cet assemblage avec la révision actuelle du moteur.
Les données ne sont pas livrées dans le dépôt ni le ZIP : si la trajectoire manque,
ce lanceur la reconstruit depuis les sources historiques et leur graine, puis
l'affiche. Ce premier lancement peut donc prendre plus de temps.

La membrane commence comme ruban polymérisé, pas comme unités libres. La traduction
est un templating direct G→F, sans ribosome, et ne prouve pas la fonction des F.
La copie utilise un cycle externe fixé à l'avance. Les compteurs excluent le gène
initial. Les séquences non orientées sont reconnues à inversion près.

## Interface

- **Espace / Pause** : arrêter ou reprendre le calcul.
- **N / Un pas** : avancer d'un pas en restant en pause.
- **R / Recommencer** : nouvelle exécution avec la même graine et la même configuration.
- **Vitesse** : maximum CPU ou cadence plafonnée ; le pas physique reste identique.
- **S / Sauver**, puis **L / Charger** : sauvegarder et reprendre l'état complet.
- **F / Centrer**, molette et glissement : cadrage, zoom et déplacement.

Le rendu est limité à 30 images/s. Le travailleur peut effectuer beaucoup plus de
pas ; les réactions et le bruit ne dépendent pas du nombre d'images. Un premier
lancement peut compiler les noyaux CPU Numba pendant quelques secondes.

Les calculs validés ont pris environ 13 à 31 secondes chacun sur cette machine,
en lançant les quatre en parallèle, hors sauvegarde finale. Ce ne sont pas des
délais garantis sur une autre machine ; les paramètres simulés restent les mêmes.

À la fermeture, les résultats sont conservés dans `outputs/`, même si l'expérience
n'est pas terminée (`completed: false`). Un redémarrage conserve aussi l'ancien
résultat dans son dossier propre. En relecture, cliquer sur la barre temporelle
permet de se déplacer dans la trajectoire.

## Modifier et automatiser

Les fichiers `configs/*.json` sont autonomes et modifiables : graine, durée,
géométrie initiale, concentration, température, propriétés des liaisons exposées
par le module et choix du voisinage. Copier un fichier constitue un nouveau scénario.
Les métriques attendues servent uniquement à l'analyse finale, jamais aux réactions.

```powershell
python -m simulator --config demonstrators/configs/expression.json --seed 1
python -m simulator --config demonstrators/configs/membrane.json --gui
python -m simulator --replay-view chemin/vers/un_dossier_de_resultats
python chemin/vers/un_dossier_de_resultats/replay.py
```

La dernière commande recalcule depuis le code exact archivé et compare toutes
les métriques. Utiliser l'environnement Python indiqué par `requirements.txt`.
