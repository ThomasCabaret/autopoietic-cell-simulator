# Lot41 — capture transférable, bain concurrent P/R/H/T construit

**Clôture MX1 au lot42 :12/12 achevés, zéro erreur, porte refusée.** Deux
critères G/F échouent ; les six autres passent, dont F alimentaires→L sur2/3.
G nouveaux0/2/0, F2/5/1, L9/20/8. Le refus vaut le domaine/horizon1200,
pas impossibilité : stocks P/R encore présents et production tardive.
Voir [BATCH_42.md](BATCH_42.md) pour l’audit de calibration et la suite.
Les lectures partielles ci-dessous restent historiques.

4 novembre2026. [Plan](BATCH_41_PLAN.md) · [recettes MX1](BATCH_41_RECIPES.json)
· [pilote](BATCH_41_PILOT.json) · [comparaison CT1](BATCH_41_CT1.png).

## CT1 terminé9/9 : porte passée, sans supériorité uniforme

Aucun travail CT1 actif, aucune erreur. Le rapport figé local
`outputs/capture_transfer_followups/followup_20261104T174449362677Z/report_0.json`
a pour SHA256 `f26858ce5d378065b5cc84fc22130f0fa8cc68fcf7b6194320fa4119bc36ef7e`.
Les six critères annoncés passent. Résultats par graines0/1/2 :

| Mesure à1200 | Capture35, référence recalculée | Capture E/largeur² |
| --- | --- | --- |
| G nouveaux libérés |9 /12 /8|9 /9 /7|
| F nouveaux libérés |11 /13 /12|12 /10 /11|
| F entièrement alimentaires |10 /10 /10|10 /8 /9|
| Dont actifs ensuite sur P/R |5 /2 /1|1 /2 /2|
| Opérations de ces F |12 /9 /9|13 /2 /3|
| Première activité |392,68 /192,14 /395,92|191,27 /759,51 /396,19|

Sans gène, aucun nouveau F sur les trois graines. Le temps médian de calcul
218,6→219,5s ne révèle pas de surcoût massif dans ce crible concurrent ; pas
un benchmark précis. La médiane d’opérations baisse9→3 : le critère exigeait
la persistance du transfert, pas une activité strictement supérieure. Avec
trois graines et stocks finis, ne conclure ni à une amélioration uniforme,
ni à une équivalence statistique ou à une vitesse de renouvellement durable.

**Décision :** la courbure commune ne détruit pas la boucle courte ; passer
à la concurrence réelle, sans adopter globalement cette branche dans MD2.
CT1 ne contenait aucun H/T ; la réussite ne prouve pas leur compatibilité.

## Avancement fonctionnel : un seul registre de capture

Nouveau hook opt-in `mixed_synthesis`, même moteur Simulation et Langevin.
Le registre de sites F est unique pour les vrais P/R/H/T. Un adaptateur permet
à CopyChemistry de lire ces occupations sans doubler les forces, ressorts ou
tirages de capture. Les nouveaux F exprimés possèdent les mêmes sites que
les F préparés. Les vrais liens H–T activent les ports MD2 de LinkedLipids.
Le motif P–T/H–R peut bloquer temporairement un site, mais ne produit rien ;
libération au taux commun, aucun nettoyage global ou tri par identité biologique.

Coût : aucun nouveau rôle, gène, type élémentaire, port, taux ou constante
numérique indépendante. Même F01 et six types matériels P_G/P_F/R0/R1/H/T.
Ajout d’une compatibilité de matériaux à une capture commune et du raccord
logiciel ; l’occupation H/T et la porte énergétique locale sont celles de L3.
L’ordre séquentiel et la formation P/R historique sont conservés/déclarés.
Cette asymétrie de formation et les changements de potentiels restent une
dette énergétique. « Un bain commun » ne signifie pas équilibre thermodynamique.
Pas de nouvelle protéine à autoriser ni de modification de scénario en réaction
à des mesures ; l’observateur est passif.

Les mesures distinguent : produits lipidiques catalysés ; outil F préparé,
exprimé ou entièrement alimentaire à une observation antérieure ; contact
latéral ultérieur d’un L neuf ; occupation génétique/lipidique et doubles motifs
de matériaux incompatibles. Échantillonnage0,5, qui peut sous-compter les épisodes
brefs. Pas d’exposition intégrée exacte revendiquée ni de trajectoire systématique.

## Pilote puis campagne MX1

Pilote technique mixed0,198 billes, t10 : fini en3,157s, zéro erreur de bilan
atomique/ports, aucun L à cet horizon. Tardif à ce très court horizon T≈0,129,
maximum0,223 ; pas preuve d’isothermie. Énergie de préparation F non détendue
ici. Aucune retouche après ce résultat, aucun taux ni thermostat changé.
Recette MX1P préservée, SHA résultat
`8ec7d86598b1ad0b355f5aeafbaacbccd55ed4d1e9479f40bcdf87adc9f4d18a`.

**MX1 lancé :12 essais**, mixed/uncaptured/noHT/nogene×3, t1200,2 travailleurs,
checkpoints30s, budget4h puis pause.198 billes,150 sans H/T ; aucun L initial,
4 G01 et1 F01 préparés. Sources et critères figés avant calcul, aucun second
tour automatique. Statut **mixed_synthesis_status.bat**, pause/reprise par
**stop_mixed_synthesis.bat** / **resume_mixed_synthesis.bat**. Rapport automatique
puis arrêt pour interprétation, même en cas de porte favorable.

La porte cherche un F entièrement alimentaire qui catalyse réellement H/T,
et des L neufs qui s’associent, dans les mêmes bains où la génétique fonctionne.
Le témoin uncaptured conserve les mêmes H/T mais enlève leur capture (fond H–T
conservé) ; c’est une ablation de loi. NoHT reproduit la référence génétique
mais a un tableau de vitesses plus court : pas une trajectoire initialement
appariée au cas mixed. Nogene garde les atomes et retire seulement les liens G.

### Première lecture partielle2/12 — aucune erreur

| Cas graine0 | G/F neufs | F alimentaires, actifs P/R | L catalysés | L depuis F alimentaires | L neufs avec contact ultérieur |
| --- | --- | --- | ---: | ---: | ---: |
|mixed|0 /2|2, dont1 actif|9|3 (2 outils distincts)|7|
|uncaptured|7 /9|6, dont1 actif|0|0|0|

Premier transfert F alimentaire→L à879,83 ; première opération P/R d’un de
ces F à1188,63. Même F reconstruit n’est pas garanti pour ces deux premières
dates : ce sont deux statistiques de population. Aucun invariant de matière/
ports violé. Température tardive0,0888/0,0887, maximum0,223/0,236.
Occupation moyenne sampled mixed :1,322 sites H/T et1,333 P/R ; doubles
motifs croisés1554 unités-arête-temps échantillonnées, contre0 en uncaptured.
Ce proxy peut sous-compter les contacts brefs ; il n’établit pas à lui seul
la causalité de la baisse génétique. Coût420,5/256,1s sous charge concurrente,
alarme descriptive, pas benchmark isolé.

**Interprétation provisoire :** le chemin matière P/R→F entier exprimé→L est
observé dans ce premier bain, avec association aval, mais forte pénalité sur
la génétique. Attendre les trois graines et témoins avant décision et diagnostic
supplémentaire ; pas d’adoption ou changement de seuil. Le rapport/resultat mixed
est hashé `6079316a900dd1be4a641bdf3b0ea1ec0f8c9256a9be3f027f087d53ad5ad709`.

Un éventuel échec peut provenir de stocks H/T épuisés avant l’arrivée des outils
neufs : relier les naissances aux stocks avant de conclure à une incapacité.
Ne pas déclarer un blocage structurel depuis la seule absence d’un événement.
La porte/horizon restent inchangés ; ce diagnostic éventuel sera séparé.

## Validation, visibilité et limites

Contrôles mécanistes : mêmes sites libèrent H/T puis catalysent P/R, mauvais
couple effectivement capturé sans produit, partenaires H/T non prescrits,
aucun déplacement à la réaction, delta local exact avec attractions génétiques,
capture comptée une fois, reprise exacte et observation passive, arbre/brute.
Sans H/T, positions/vitesses/PRNG/bonds égaux à CT1 dans les trois préfixes testés.
Le calcul local ΔU n’interroge ni contour, ni composante, ni séquence complète.
Les certificats de provenance ne dirigent aucune réaction.

Les quatre préfixes archivés MIN1R/MIN1M/MD2/L3 restent exactement reproduits
àt5 (état physique, PRNG, vitesses et caches). Catalogue GUI recertifié : les
27 démos gardent leur dynamique et MIN1M reste la scène recommandée ; MX1
n’est pas promu avant résultats. Les documents et le registre sont actualisés.
**218 tests finaux passent**, ainsi que les27 actions Qt/OpenGL, lecture/pause/
recommencement et égalité des positions GUI/headless. Les premiers refus de
répertoires temporaires Windows dans le sandbox et l’empreinte intermédiaire
de catalogue périmée sont conservés dans les journaux locaux ; rerun hors
sandbox et recertification effectués avant cette validation finale.

**Maturité :** capture commune étudiée séparément, concurrence implémentée et
en campagne ; aucun nouveau palier biologique obtenu par le code seul. S-04
reste25%, T-05 garde75 pour MIN1M, maintien0. Après MX1 : insertion/rétention
avec barrière segmentaire indépendante du core F/L, énergie sous flux, pertes
et protection. Information riche, diversité des fonctions et homéostasie des
polymères restent des risques majeurs. Pas de garantie de délai ou de viabilité.
