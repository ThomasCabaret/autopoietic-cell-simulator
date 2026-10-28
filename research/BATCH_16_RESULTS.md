# J3 terminé — 28 octobre 2026

21/21 tâches à1200, aucune erreur. Code figé3d2cb79 ; recette source seule
`campaign_recipes/J3_20261027T192723206222Z`. Analyse contrôlée :
`outputs/campaigns/campaign_20261027T192723206222Z/inventory_analysis_20261028T063510463575Z`.
Sources, scénarios, temps, comptes de réactions, partitions d'exclusions,
checkpoint final et identités des P/R réellement incorporés vérifiés sur21 tâches.
Reproduire avec `experiments/analyze_constructed_tool.py`, puis l'analyse figée
`scripts/campaign.py analyze`. Résultats bruts conservés localement.

## Résultats sur graines0/1/2

| Inventaire / milieu | Dimères catalysés | Catalysés incorporés | G nouveaux libérés | F nouveaux libérés |
|---|---|---|---|---|
| K1 sans L |6/11/13|0/0/0|0/0/0|0/0/0|
| K1 avec L |8/10/11|0/2/0|0/0/0|0/0/0|
| K8 sans L |146/164/161|12/7/6|1/0/0|0/1/1|
| K8 avec L |153/139/154|5/13/7|0/0/0|0/0/0|
| K16 sans L |328/326/331|11/28/20|1/0/0|0/1/2|
| K16 avec L |331/401/313|18/18/26|1/1/0|0/1/1|
| K16 avec L sans boost |0/1/0|0/0/0|0/0/0|0/0/0|

K16 avec L :20,69/25,06/19,56 actes catalytiques par outil initial ;
1,125/1,125/1,625 composants catalysés incorporés par gène initial. Seize
exemplaires préparés du même G001/F001, pas seize fonctions différentes.
Chaque G nouveau des bains K16 et chaque F nouveau des bains K16 sont entièrement
issus de dimères construits. Cela ne signifie pas que tous sont issus d'outils
exprimés, ni que la chaîne entière est renouvelée continuellement.

La graine1 du bain K16 obtient conjointement G1 et F1 nouveaux, mais aucun acte
catalytique attribué à ce F exprimé à1200. La graine2 produit un F exprimé qui
effectue4 opérations, dont2 produits réellement incorporés, sans nouveau G.
La chaîne matérielle G→F exprimé→construction→usage est donc observée dans
le bain membranaire, mais aucun essai ne réunit tous les critères de la boucle
complète avec nouveau G et activité aval d'un F renouvelé. Ne pas réunir les
résultats de graines différentes pour revendiquer cette fermeture.

K8 sans L : F exprimés16/1 actes en graines1/2, aucun produit de ces actes
incorporé ; F complets encore partiellement préparés. Les témoins sans boost
échouent sur les trois graines : l'accélération catalytique a une contribution
utile dans ce régime ; le fond seul n'y substitue pas le flux observé.

## Frontière et limites

Comparaison sur grille régulière0,5 (2401 points, callbacks de ligation exclus
du poids supplémentaire) : K16 avec L fermeture0,732/0,791/0,786, enveloppe
classable0,915/0,979/0,978 ; insertions L6/3/2. La frontière n'est donc toujours
pas robuste. Contacts échantillonnés P/R libres avec L5096/5259/3198 ; liés473/38/1.
Passages observés libres123/168/88, liés0/0/0. Très faible exposition liée,
notamment graine2, et périodes inconnues : zéro passage lié n'est pas une
preuve de rétention globale. Ces L étaient préparés, pas synthétisés par F.

Au terme des bains K16 :193/229/170 monomères G et192/209/188 monomères F ;
314/252/335 P libres et autant de R. Pas d'épuisement global expliquant seul
le rendement faible. Unités F en fragments non cibles entièrement déliés10/16/6,
contre0/2/0 dans l'ablation. Des fragments peuvent encore catalyser : pas tous
des déchets inertes. Les lois interdisent leur recapture génétique (F de degré
non nul), sans permettre encore d'attribuer tous les échecs à ce garde.
Temps cumulés d'éligibilité de ligation F0,44/0,67/0,77, G0,29/0,32/0,70 :
motifs complets encore rares malgré les stocks. Ces expositions pré-tick ne
sont pas des hazards exacts, l'ordre des réactions change les motifs au sein
d'un tick. Les absences à1200 restent censurées, jamais impossibilités.

## Décision

Une augmentation finie d'inventaire retrouve du transfert utile et de nouvelles
chaînes dans un bain commun, sans nouvelle loi. Ce n'est pas une convergence
du maintien : au mieux un F nouveau pour seize préparés dans les bains K16.
Pas de nouveau balayage de densités. T9/finition est désormais un risque concret,
mais modifier ce garde avant contrôle numérique risquerait de régler un artefact.
Prochaine campagne N1 : même chimie, dt/2 et dt/4, horizon1200 et grille0,5,
référence J3 réutilisée explicitement. Puis décider finition/recapture locale,
sans lecture de chaîne complète ni taux ajusté pour chaque fonction.
