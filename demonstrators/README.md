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
| `02_membrane.bat` | Des molécules isolées de deux billes s'associent en contours fermés, sans liens latéraux initiaux |
| `03_traduction.bat` | Une matrice G assemble une autre famille F de même séquence |
| `04_controle_sans_gene.bat` | Les mêmes composants d'expression sans squelette génétique initial : aucune ligation |
| `05_fragments_relecture.bat` | Relecture identifiée d'une réussite historique : cinq fragments forment une boucle de quinze unités |
| `06_tout_sans_interface.bat` | Les quatre premiers scénarios, sans rendu, avec vérification automatique des critères |
| `07_ruban_prepare.bat` | Contrôle historique : un ruban composite déjà polymérisé se courbe et ferme |
| `08_ligation_preparee.bat` | Prototype séparé : une chaîne préparée de trois billes rapproche des substrats pour plusieurs ligations avec libération |
| `09_expression_fonction.bat` | G fabrique une chaîne F composite, puis celle-ci soutient plusieurs ligations XY avec libération dans le même bain |
| `10_coexistence.bat` | G 001 est copié et traduit dans le même bain ; les F exprimés réalisent plusieurs opérations |
| `11_construction.bat` | Des P/R libres forment des dimères, puis G et F ; formation spontanée, pas encore pilotée par des outils |

Les trois premiers sont des **simulations en direct**, à graine fixée. Le quatrième
est aussi calculé en direct. Le cinquième lit une trajectoire archivée ; il ne
prétend pas reproduire cet assemblage avec la révision actuelle du moteur.
Les données ne sont pas livrées dans le dépôt ni le ZIP : si la trajectoire manque,
ce lanceur la reconstruit depuis les sources historiques et leur graine, puis
l'affiche. Ce premier lancement peut donc prendre plus de temps.

Le scénario membrane commence avec 36 dimères isolés et forme plusieurs contours ;
la rétention d'un contenu n'est pas encore testée. Le ruban préparé reste un contrôle
séparé. La traduction
est un templating direct G→F, sans ribosome, et ne prouve pas la fonction des F.
La copie utilise un cycle externe fixé à l'avance. Les compteurs excluent le gène
initial. Les séquences non orientées sont reconnues à inversion près.

Le scénario 09 intègre traduction et opération répétée avec les vrais F composites.
Il utilise une activation locale des sites par une liaison au squelette et des
précurseurs activés ; XY ne sert pas encore à fabriquer les composants. Le scénario
03 conserve sa configuration historique, dont les F n'ont pas cette activité.

Le scénario 10 réutilise une coopération locale, avec un seul port et la séquence
courte 001. Ses compteurs exigent de nouveaux G et F observés détachés ensemble.
La coexistence sur six symboles, la fabrication des composants et une membrane
commune restent ouvertes. Voir le bilan du lot 5 et PROJECT_HEALTH.md.

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

La membrane calcule 1000 unités de temps et a pris environ une à deux minutes
sur cette machine ; les trois autres scénarios avaient pris 13 à 31 secondes
chacun lors de la validation initiale. Le premier lancement peut être plus lent.
Ces durées ne sont pas garanties sur une autre machine.

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
