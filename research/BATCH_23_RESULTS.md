# LT2 achevé — transfert fonctionnel et régression de la grande membrane

Les16 essais sont terminés, sans erreur ni contrôleur actif. Sources/scénarios
et hashes des16 résultats vérifiés par `experiments/review_langevin_transfer.py`.
La source du rapport automatique correspond au manifeste figé. Voir BATCH_23_PLAN.md
pour les critères fixés avant calcul. Les conclusions micro du lot23 restent
valides dans leur domaine ; elles ne suffisent pas pour le grand bain.

## Bain intégré J3, horizon1200, ordre des graines0/1/2

| Mesure | Brownien | Langevin0,1,m1 |
| --- | --- | --- |
| Fraction régulière de membrane fermée | 73,2 / 79,1 / 78,6% | **2,6 / 23,6 / 74,2%** |
| Composants catalysés | 331 / 401 / 313 | 356 / 348 / 361 |
| Catalysés puis incorporés | 18 / 18 / 26 | **9 / 7 / 32** |
| Nouveaux G complets libérés | 1 / 1 / 0 | 0 / 0 / 1 |
| Nouveaux F complets libérés | 0 / 1 / 1 | 0 / 1 / 0 |
| Produits de F exprimés puis utilisés | 0 / 0 / 2 | **0 / 0 / 0** |
| L libres insérés avec persistance≥10 | 5 / 3 / 2 | 0 / 0 / 1 |

Mesures de fermeture sur grille0,5, avec tous les états inconnus conservés.
Les deux membranes finales0/1 sont ouvertes sous Langevin ; les trois références
browniennes finissent fermées. La graine0 Langevin entre dans un épisode
continûment non fermé de41 à1200. Les variations de rendement ne sont donc pas
une domination de tous les critères par le nouveau mouvement. Trois graines
restent un petit échantillon, mais le défaut0/1 est un problème réel à diagnostiquer.

Le nombre brut de passages des composants libres augmente fortement dans les
périodes classables. On ne doit pas utiliser les périodes de frontière inconnue
pour compter des fuites ou déduire la rétention finale : les compteurs internes
peuvent garder leur dernière valeur connue. Aucun maintien démontré.

Le contrôle fin sélectionné sur graine2 (dt0,001, même intervalle de réaction)
donne1G/2F,22 composants catalysés utilisés,3 produits par F exprimés mais0
utilisé ; fermeture74,9% contre74,2% au pas de base. Il ne répond pas au défaut
des graines0/1 et n'établit pas la convergence.

Températures cinétiques tardives moyennes Langevin≈0,0904–0,0922 pour cible0,08,
avec pics précoces≈0,20–0,21. Le contrôle fin graine2 reste≈0,0907. Aucune
normalisation globale effectuée. La réactivité et la préparation peuvent échanger
de l'énergie ; leur contribution n'est pas isolée par ce simple audit.

## Décision

Langevin reste la base de travail choisie avec l'utilisateur. Ne pas ralentir
le mélange pour cacher les défauts chimiques révélés. Conserver les anciennes
recettes browniennes comme témoins et les variantes GUI sans renommer leurs
résultats historiques. Aucun défaut logiciel d'intégration établi par LT2.

La priorité devient la continuité/recapture du grand contour sous ce mouvement,
avant T9 : un bain qui se disperse brouille l'interprétation de ses rendements.
MD1, lot24, teste dissociation aléatoire, rupture par étirement, échange et pas
numérique ; loupe passive sur la première ouverture durable. Dans LT2 graine0,
les seuls échanges acceptés sont à1195,59/1196,44, bien après la dégradation
vers41 : **un échange accepté ne peut pas déclencher cette première dégradation**.
L'ablation de la routine d'échange peut cependant changer la suite du PRNG,
donc sa différence de trajectoire seule ne constituerait pas une preuve causale.

## Provenance et maturité

Recette et données : BATCH_23.md. Synthèse locale vérifiée :
`outputs/reviews/LT2_20261030T110228432285Z/summary.json`, son driver et
`functional_transfer.png`. Aucun résultat brut ajouté à Git.

Gain des microdémos et du transfert C3B1 démontré à graines sélectionnées ;
compatibilité intégrée insuffisante. La chimie du grand bain reste distincte
des petits contours V8. La régression n'est pas une impossibilité de principe
de la cellule ; elle invalide l'affirmation que le mouvement préserve déjà
tous les acquis. Aucun gène/outil nouveau, aucun changement du budget initial
de particules, aucune promesse de délai de renouvellement.
