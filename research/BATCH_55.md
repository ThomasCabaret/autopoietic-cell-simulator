# Lot55 — audit trié et premier transport ouvert construit

6 novembre2026. [Plan](BATCH_55_PLAN.md), [revue Astra](ASTRA_REVIEW.md),
[état courant](../CURRENT_STATUS.md), [preuves compactes](BATCH_55_RESULTS.json),
[recette source OB1](BATCH_55_OB1_RECIPES.json).

## Reprise des résultats

FR1 est terminé6/6,0 erreur, contrôleur arrêté : fast0/3,slow1/3, deux portes
de récupération refusées. La durée de vie seule ne rend pas le redémarrage
robuste. Les données de co-occupation restent échantillonnées ; pas de nouvelle
grille de ligation ou de taux. La priorité de maintien repart d'un réseau équipé
et redondant, avec mesure de vrais remplaçants. CR1/PT1/RF1 restent clos et leurs
verdicts inchangés ; CF1 garde sa pause scientifique.

Les vingt recommandations sont examinées individuellement. Retenus : symétrie
des intrants avant exploration, bilans ouverts par matière, distinction entre
proxy et fonction, pertes/renouvellement calibrés par famille, observateurs bornés.
Nuance essentielle : le calcul de barrière au hiatus PT1 est statique et ne
démontre pas sa rétention dynamique. Différé : préassociation de reconnaissance,
nouvelle machine, refonte globale des journaux. Aucun nouvel outil fonctionnel.

## Construction OB1

`open_bath` utilise Simulation et le Langevin BAOAB existants. Les précurseurs
sortis sont absorbés ; des nouveaux arrivent au bord selon deux processus Poisson
fixes, à profondeur.3 dans une boîte8×6. T.08,masse1,gamma.1. Pas de mur réfléchi,
de chimie, de membrane ou de feedback du stock vers l'apport. Le calendrier
source et les vitesses d'entrée ont un PRNG indépendant du mouvement interne.

Les IDs sont monotones, distincts des indices de tableau. Le contrat de remappage
permet au moteur de garder exactement les vitesses des survivants et d'invalider
ses caches. Le bilan `initial + entré - sorti = présent` est suivi par espèce.
L'observation retient un nombre borné d'échantillons ; la chimie garde l'état
courant, pas un journal cumulatif. Plafond de capacité = erreur, jamais régulation.

Absorption et injection sont discrétisées à l'intervalle de bord.02. Une sortie
puis rentrée entre deux observations peut être manquée ; la convention n'est pas
un premier passage continu exact. Le raffinement du bord et la profondeur source
doivent être calibrés au transfert. Aucun état stationnaire n'est certifié.

## Six essais courts terminés, aucune campagne encore active

Trois graines ×dt.004/.002,80 unités, même intervalle de bord et même calendrier
d'apport dans chaque paire. Crible de construction réussi6/6 :

| Graine | Entrées P/R, mêmes aux deux dt | Sorties dt.004 | Sorties dt.002 | Population finale .004/.002 |
| --- | --- | --- | --- | --- |
| 0 | 222/238 | 200/211 | 199/212 | 49/49 |
| 1 | 244/233 | 226/204 | 218/205 | 47/54 |
| 2 | 225/213 | 194/194 | 195/185 | 50/58 |

Bilans exactement nuls dans les six essais, arrivée dans la moitié centrale,
empreintes source identiques dans chaque paire. Retard maximal d'injection
inférieur à.02. Les populations moyennes tardives sont51,1–58,5 ; des trajectoires
thermiques différentes empêchent d'attribuer l'écart à dt sur trois graines.
Temps réels1,2–3,0s par essai, sous deux travailleurs avec suite de tests concurrente,
hors démarrage du contrôleur ; pas une vitesse extrapolable à la cellule.

Les précurseurs sont deux classes de transport sans affinités. Cela ne prouve
pas une chimie commune ni l'alimentation du candidat CP1. Les tables P/R à
préfixes fixes, la provenance réversible et la sortie des molécules liées sont
les prochains travaux d'intégration. Le bilan d'excès L reste ouvert.

## Vérifications et coût

Cinq tests de population/source : reprise exacte avec RNG/vitesses/IDs/observateur,
observation passive et bornée, calendrier invariant aux cadences, conservation
des vitesses des survivants, bain vide, entrées/sorties et arrêt de capacité.
Trois références sélectionnées à5 unités (copy FR1, L isolés CH1, intégré CP1)
retrouvent exactement positions, ressorts, angles, état chimique, mouvement et RNG.
Ce sont des préfixes de non-régression, pas de nouvelles preuves longues.

La première suite304 a refusé sept usages du catalogue devenu périmé ; les297
autres passent. Après revue des chemins fermés et régénération, le catalogue est
recertifié :14 tests ciblés catalogue/population passent, couvrant les sept
refus initiaux. Le titre de menu devient
« Démo intégrée · référence EG1 », les mêmes39 presets gardent leurs lois.
Les18 contrôles supplémentaires du registre, des checkpoints et de la
visualisation passent aussi. Implémentation et recettes : commit `34dd9bc`.

Delta chimique CP1 :0. L'inventaire6 atomes/10 transitions/20 conditions est
inchangé ; seules les empreintes config/mouvement sont revues pour cette nouvelle
branche. OB1 ajoute un protocole externe (flux par espèce, profondeur, calendrier)
et un contrat technique de population, sans gene/catalyseur. Aucun résultat brut
ou checkpoint ajouté à Git ; sources et recettes figées seules sont conservées.

## Maturité et suite

E-01 :0→25, un sous-cas de transport ouvert. T-05 et H-06 n'avancent pas en preuve
biologique ; leur prochain test est recadré sur le maintien équipé. Maintien
intégré0. Le projet gagne un composant nécessaire réutilisable ; la diversité
fonctionnelle, l'information, le bilan L et le maintien restent des risques.

Prochain jalon : représentation P/R sous apport/sortie et provenance réversible,
puis réseau équipé sous flux et pertes partielles. En parallèle conceptuel,
choisir comment éprouver une seconde fonction par assemblage ; la symétrie
actuelle PG/PF interdit une sélectivité directe dans le canal de capture, pas
toute fonction future. Pas de nouvelle protéine sans proposition/accord.

Reproduction : restaurer la recette OB1 avec `scripts/campaign.py restore`,
lancer son `run`, puis `python -m experiments.review_open_boundary DOSSIER`.
Le générateur `python -m experiments.prepare_open_boundary` prépare un nouveau
dossier et une nouvelle recette. Il ne relance aucun résultat précédent.
