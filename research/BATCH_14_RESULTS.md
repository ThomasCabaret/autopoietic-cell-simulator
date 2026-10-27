# GKA : accès simultané rare, pas réaction élémentaire absente

27 octobre2026. Six témoins natif/froid rejoués à400 sans changer les lois,
recette [GKA](campaign_recipes/GKA_20261027T122747493430Z/manifest.json), code0c08498.
`experiments/analyze_batch14.py` vérifie sources, durée, conservation des census,
nombres d'événements puis **toutes** les métriques primaires, positions finales,
PRNG et état chimique contre J0. Six comparaisons exactes. Données préservées
dans outputs/campaigns/campaign_20261027T122747493430Z ; dernier post-traitement
complet post_analysis_20261027T123208528833Z.79 tests logiciels+7 historiques.

| Bain / graine | Paires génétiques formées nettes* | Temps-paire G–F | Double appariement | Ligation F admissible | Liaisons de polymère | F nouveaux libérés |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Natif0 | 8 | 686,31 | 160,18 | 0,12 | 2 | 1 |
| Froid0 | 5 | 479,82 | 0 | 0 | 0 | 0 |
| Natif1 | 4 | 269,78 | 6,40 | 0,09 | 2 | 1 |
| Froid1 | 2 | 147,83 | 0 | 0 | 0 | 0 |
| Natif2 | 7 | 430,52 | 10,02 | 0,05 | 2 | 1 |
| Froid2 | 2 | 193,97 | 22,73 | 0,13 | 1 | 0 |

*Les changements nets comptent toutes les paires génétiques ; le natif2 inclut
aussi des paires G–G. Les autres cinq essais n'ont pas de paire G–G observée.
Les expositions sont pré-réaction, par maintien à gauche entre ticks, en
temps-motif. Ni risques exacts ni causes indépendantes. Une ligation créée
immédiatement après capture peut ne pas apparaître dans le census pré-tick.

Dans les froids0/1, des sites sont occupés mais aucune paire de sites voisins
d'une arête G n'est simultanément occupée dans les observations pré-tick.
Le problème n'est donc pas simplement un taux de ligation trop faible dans une
géométrie déjà présente. Le froid2 produit une liaison F : l'étape chimique
fonctionne une fois, sans compléter un trimer. Après libération, les fragments
F liés ne peuvent pas être recapturés comme monomères par les règles actuelles :
T9 reste un risque structurel, pas encore la cause de tous ces échecs.

Les paires nettes durent au maximum115,61–176,01 à froid,176,52–184,16 au chaud.
Le cycle effectif est **200/15**, soit185 unités de capture et15 de libération.
Les anciennes notes lot13/plan14 mentionnaient60/10 à tort : les scénarios figés
et le moteur ont toujours utilisé200/15. Documentation corrigée ; aucune donnée
ni ancienne recette modifiée.400 couvre seulement deux cycles complets.

Conclusion : rareté de l'occupation simultanée établie dans deux témoins froids,
fragment incomplet dans le troisième ; pas de preuve d'impossibilité à froid ni
d'une solution par simple attente. Pas de nouveau taux, motif ou règle ajouté.

## Décision : tester une cellule déjà outillée

Une prolongation froide3200 reste une option de cinétique, non choisie maintenant.
Le test qui rapproche davantage de la cible autorisée est l'amorçage par un
outil F001 construit. Comparer F001 lié et les mêmes trois dimères placés de
la même façon sans leurs deux liens ; garder trois autres monomères F011.
Ainsi les six dimères initiaux et leurs symboles restent identiques à J0.
Ce n'est ni une enzyme primitive ni une nouvelle loi, seulement un départ
construit permis. L'outil préparé est exclu des F nouveaux et du renouvellement.

Tester froid en petite boîte et bain commun, trois graines chacun et témoin
délié pour chacun, horizon1200 fixé avant résultats :12 tâches. Mesurer fabrication
répétée, incorporation, G/F nouveaux dont provenance exprimée ; conserver le
contrôle délié même s'il finit par s'outiller lui-même. Aucun succès d'amorçage
n'établira la reconstruction durable, la diversité ou la synthèse de L par F.
