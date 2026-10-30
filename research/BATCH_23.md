# Lot23 — comparaison Langevin des démos actuelles

**Clôture :16/16 terminés,0 erreur.** Voir [résultats complets](BATCH_23_RESULTS.md).
Deux graines intégrées montrent une forte perte de fermeture sous Langevin ;
la priorité du lot24 est désormais d'en diagnostiquer le mécanisme. Le bilan
partiel conservé ci-dessous ne vaut plus statut courant de la campagne.

30 octobre2026. [Plan préalable](BATCH_23_PLAN.md). Les six scènes historiques
restent disponibles et six variantes Langevin sont ajoutées, avec le même
matériel et les mêmes lois chimiques. La fiche expose l'enjeu et distingue
les résultats historiques des vérifications du nouveau mouvement.

Le mouvement demeure candidat expérimental. Ni adoption générale, ni nouveau
gène/outil, ni viabilité démontrée par l'ajout d'une entrée de menu. Comparaisons
sélectionnées depuis les démos existantes, pas nouvelles graines choisies après succès.

## Réalisation et vérification

Option mechanics étendue aux hooks membrane,membrane_bath,coupled_bath, même
ordonnanceur et mêmes forces locales. Aucun ajout de primitive chimique.
Cache invalidé après tous les ticks réactifs, y compris sans événement.
Les positions des sous-chimies du bain sont resynchronisées avant forces/réactions.
Audit cinétique thermique passif étendu ; checkpoints vitesses/PRNG conservés.
Six références aux signatures physiques inchangées, six variantes signées et
présentation distincte ; le défaut global reste brownien.

136 tests logiciels et7 historiques réussis. Nouveaux contrôles : cache versus
recalcul systématique, passivité des observateurs, reprise exacte sur quatre
hooks, conservation des intervalles physiques aux pas fins et analyse des
membranes sur grille régulière. Refus d'accès au répertoire temporaire du
bac à sable lors du premier passage ciblé : trace préservée, les12 tests ciblés
repassent avec les droits nécessaires ; suite complète ensuite en temporaire
local au workspace. Ce refus technique n'est pas une régression chimique.

Test natif Qt/OpenGL :12 entrées ouvertes en pause ; lecture/pause et
recommencement exact vérifiés pour J3 brownien et Langevin. Captures inspectées
sous outputs/demo_qa ; la fiche affiche l'enjeu et les conditions du candidat.
Ce contrôle court ne prouve pas les fonctions à l'horizon long.

## Pilotes et premiers résultats complets des microdémos

Deux pilotes à5 achevés2/2, sans erreur numérique. Maximum de déplacement par
pas :0,00722 pour V8 et0,00999 pour J3. Température cinétique globale V8
0,074–0,482 et J3 0,079–0,201, cible0,08 : **échauffement initial mesuré**,
pas de rescaling. Son origine détaillée n'est pas isolée ; association,
relaxation des états préparés et discrétisation restent à distinguer. Ne pas
déclarer le thermostat équilibré sur le seul fait que le calcul est fini.

Les six essais micro principaux sont achevés. Chaque scène ne représente
qu'une graine, héritée de la sélection illustrative historique :

| Scène, horizon | Brownien | Langevin0,1 |
| --- | --- | --- |
| T7 copie,800 | 1 nouveau G libéré | 1 nouveau G libéré |
| C3B1,1200 : G/F libérés | 2/3 | 4/5 |
| C3B1 : composants catalysés puis utilisés | 13 | 29 |
| C3B1 : dont produits de F exprimés puis utilisés | 13 | 19 |
| V8,1000 : première observation régulière d'un contour | 184 | 41 |
| V8 : fraction des observations régulières avec ≥1 contour | 81,5% | 94,5% |

V8 commence bien avec36 dimères isolés, sans liens latéraux. À la fin,
Brownien présente deux contours de10 et14 molécules, Langevin un contour de11.
Une apparition plus tôt ou une fraction accrue n'est donc pas une domination
sur chaque indicateur, ni la fermeture d'une grande cellule. Échantillonnage
régulier1 ; ouvertures entre images non exclues. Première libération T7 à185,5
dans les deux essais ; les cycles fournis influencent ce seuil.

Les températures tardives moyennes Langevin (dernier quart) valent≈0,603
pour T7 et0,604 pour C3B1, cible0,6. V8≈0,094 pour cible0,08, après un pic
précoce≈0,493. Le transitoire ne doit pas être caché ; ce bain réactif n'est
pas le gaz inerte de MIX2. Les thermostats, cycles et réactions sont inchangés
pendant chaque essai, sans retour des mesures vers les lois.

Contrôles fins sélectionnés : T7 dt/2 donne3 G contre1, C3B1 donne3G/3F,
14 composants catalysés utilisés, contre4G/5F et29 au pas de base.
Cadence réaction/observation physique conservée. La variabilité d'une seule
graine et le changement de trajectoire empêchent d'attribuer cette différence
à une dérive systématique ou de certifier la convergence. V8 au pas fin ferme
à91, avec90,0% d'observations régulières fermées et deux contours finaux12/10.
Température moyenne tardive≈0,0947, proche du pas de base≈0,0938 : l'excès
thermique ne disparaît pas avec ce seul raffinement et sa cause reste à isoler.
Le mécanisme d'assemblage subsiste, sans preuve de convergence quantitative.

**État à la remise de main :9/16 terminés,0 erreur ; les sept tâches J3
intégrées restent inachevées (deux en cours, cinq en attente).** Les trois
microcontrôles fins sont donc tous achevés. Ne pas confondre ce bilan partiel
avec la compatibilité intégrée complète.

## Campagne, traçabilité et suivi

Campagne LT2 :16 tâches, deux travailleurs, checkpoints30s et aucune trajectoire
dense. Résultats locaux :
`outputs/demo_motion_campaigns/campaign_20261030T065759494210Z`.
Pilotes : `outputs/demo_motion_pilots/campaign_20261030T065129203595Z`.
Recettes exportées sous `research/campaign_recipes/LT2_20261030T065759494210Z`
et `LT2pilot_20261030T065129203595Z`, avec manifestes, plan et sources exactes.
Les données brutes restent locales ignorées. Le rapport vérifie les sources,
scénarios et résultats, puis ne lit les métriques complètes qu'après achèvement
de chaque tâche. Les non-événements restent censurés à l'horizon.

`demo_motion_status.bat` donne statut et rapport ; `stop_demo_motion.bat` puis
`resume_demo_motion.bat` permettent la pause/reprise. `analyze_demo_motion.bat`
utilise la source d'analyse figée, également lancée automatiquement en fin de
campagne. Aucun nouveau balayage ou changement de loi ne sera déclenché.
Plusieurs heures possibles pour les bains J3 ; pas de calcul ordinateur éteint.

## Maturité, santé et priorité suivante

Transfert utile observé dans C3B1 : un F exprimé produit des composants qui
servent ensuite sous les mêmes lois. V8 et T7 restent des modèles distincts,
avec températures/géométries différentes ; leurs réussites ne se cumulent pas
en une cellule viable. Le verdict du bain intégré Langevin reste en attente.

La compatibilité du mouvement est une étape bornée, pas une nouvelle recherche
de paramètres. Ne pas annoncer une amélioration robuste des rendements à partir
de ces graines seules. Les écarts au pas fin et l'échauffement sont conservés
comme limites. À la fin de cette campagne, interpréter la compatibilité puis
reprendre T9/finition et concurrence des fragments longs ; aucune nouvelle
protéine sans proposition et accord utilisateur. Ce lot n'ajoute ni dépendance
causale ni particule au budget cellulaire initial.
