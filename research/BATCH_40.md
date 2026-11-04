# Lot40 — transfert membranaire confirmé et capture commune à l’essai

4 novembre2026. [Plan figé](BATCH_40_PLAN.md) · [recettes CT1](BATCH_40_RECIPES.json).

## MIN1M clos :12/12, aucune erreur, porte passée

Même chimie MD2,2118 billes, t1200. Architecture initiale G01/F01 courte,
pas de nouvelle loi. Rapport complet local :
`outputs/membrane_renewal_followups/followup_20261104T113752867767Z/report_0.json`,
SHA256 `a555531df299c5ee3b8ffed8ca409973bdf58d6facac798daac09dc0dcc69071`.
Reconstruction de tous les constituants composites de F, libération certifiée,
puis activité ultérieure : les F initiaux ou partiellement préparés sont exclus.

| Graine active | G nouveaux | F nouveaux | F entièrement alimentaires | Dont actifs | Opérations | Première activité | Membrane fermée, grille régulière |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|0|13|11|7|6|12|776,02|85,67%|
|1|10|11|6|4|6|606,11|85,63%|
|2|7|6|2|2|16|607,46|85,26%|

Les trois graines satisfont simultanément outil neuf actif et fermeture≥70%.
Nogene : aucun nouveau G/F sur les trois graines. La membrane des témoins
nogene1/2 tient moins bien (52,73%/29,53%) ; garder ces échecs visibles, sans
en déduire que la nouvelle expression cause à elle seule la tenue des active.
Split :0/0/4 F nouveaux, aucun entier alimentaire actif. NoL :4/3/1 F
entiers actifs ; positions/types P/R appariés, mais pas les vitesses/PRNG après
initialisation, car le nombre total de particules change. Aucun effet causal
quantitatif de la membrane estimé à partir de ces seules trois graines.

Températures cinétiques tardives900–1200 des active :0,0838/0,0835/0,0827
pour consigne0,08, contexte passif distinct de la porte figée. Cette réussite
établit **le transfert de la production de remplaçants avec membrane**.
Elle n’établit ni disparition/remplacement des enzymes initiales, ni maintien,
demi-renouvellement, synthèse L, alimentation ouverte ou homéostasie.

## Démo inspectable

`visualizer.bat` → **Démos → État actuel · bain intégré** ouvre maintenant
**Membrane et catalyseurs reconstruits · progrès actuel**, graine0. Les trois
graines sont au menu. Ce choix par défaut est une convention, pas une sélection
favorable. Même recette physique, simulation depuis t0 en pause, Langevin,
compteurs de matière entièrement neuve et activité ultérieure.27 choix au total,
MIN1R et MD2 précédents conservés. Aucune donnée expérimentale embarquée.

## CT1 : préalable ciblé à P/R/H/T

La capture H/T L3 utilisait k=E/largeur² ; P/R conservait35. La fonction de
calcul est maintenant commune et l’option existe aussi pour P/R. Aucun
changement par défaut et aucune promotion scientifique de cette option.
Même E, largeur et taux : zéro constante indépendante, type, port ou gène
ajouté. Les changements de potentiel lors de capture restent des helpers,
la formation P/R n’acquiert pas silencieusement la porte énergétique H/T.

Neuf essais CT1 sont lancés : legacy/matched/nogene×3,150 billes, t1200,
sources figées,2 travailleurs et budget2h. Pas de pose native, nouveau rôle,
H/T mélangé ou second tour automatique. Le crible exige outils entièrement
alimentaires actifs et préservation des copies/expressions, témoin négatif,
alarme grossière de coût. Statut : **capture_transfer_status.bat** ; pause et
reprise explicite par **stop_capture_transfer.bat** / **resume_capture_transfer.bat**.
Analyse automatique puis arrêt pour interprétation. Aucun résultat CT1 anticipé.

Première lecture partielle **2/9 terminés, zéro erreur** : legacy0 retrouve
G9/F11,10 F alimentaires dont5 actifs (12 opérations, première392,68) ; matched0
donne G9/F12,10 alimentaires dont1 actif (13 opérations, première191,27).
Temps de calcul222,7/221,6s sous charge partagée. Cela exclut la perte totale
du mécanisme dans ce premier cas, sans valider la porte, les témoins ou la
robustesse ; attendre les neuf résultats. Empreintes des résultats :
`455ca31ff215dbe42b968e2bdfdbffdc98b42a8407a0370efe11320641d8240e`
et `99ebadb32786faa83492405f389232830592d73ddc3f8b0d02be3575d24fdbc9`.

## Vérifications et maturité

210 tests logiciels passent. Les27 actions Qt/OpenGL natives ouvrent les bons
états à t0 ; pause/lecture/recommencement et égalité des images de positions
avec le moteur headless vérifiées, dont MIN1M. Capture d’interface inspectée.
Quatre rejeux aux sources archivées MIN1R/MIN1M/MD2/L3 à t5 retrouvent exactement
positions, liaisons, mécanique, vitesses, PRNG et caches, pas seulement les métriques.
Les tests couvrent le même k P/R-H/T, états initiaux appariés et reprise exacte.

T-05 passe50→75 (couplage limité avec membrane). S-04 reste25, maintien0.
Le projet réduit un risque d’intégration réel. Les principaux risques demeurent
la chimie commune et ses pièges, énergie sous flux, information riche,
diversité des fonctions, pertes/protection et homéostasie des polymères.
Prochain jalon : lire CT1, puis confronter P/R/H/T aux mêmes sites saturables
avec produits utilisables ; conserver une barrière segmentaire de rétention
indépendante des contacts F/L. Ne pas masquer une régression par une raideur
différente par substrat. Pas de promesse de délai ou de cellule viable.
