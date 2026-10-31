# Lot34 — MIN1R, renouvellement depuis un départ construit

Décision après MIN1 achevé21/21 et les deux rejeux MIN1D exacts : le cas01
négatif n'offre aucun motif F doublement apparié observé avant tick à1200.
Le positif attend916,28 puis lie en0,12. Modifier les gardes de ligation serait
prématuré. La rareté de l'amorçage depuis six monomères ne teste pas directement
le maintien d'une cellule déjà équipée, départ explicitement autorisé.

Test : un seul F01 préparé favorise-t-il la fabrication des monomères puis sa
propre reconstruction fonctionnelle depuis les vrais atomes alimentaires ?
Même MD2/Langevin que MIN1 : aucune loi, type, port, taux, aide, outil ou gène
supplémentaire. C'est le même assemblage fonctionnel, dans un état initial construit.

## Cohorte figée avant ses résultats

Neuf essais : trois graines0/1/2 × préparations active/split/nogene, t1200,
150 billes, boîte12×9, dt0,002, réaction0,01, observation0,5, T0,08, masse1,
damping0,1 et cycle200/15. Pertes RV1 et recapture T9E absentes.

- active : quatre G01 construits ; un F01 construit et quatre F monomères0011.
- split : mêmes billes, symboles, positions et PRNG initiaux, seul le lien du
  F01 retiré. Aucun F polymérisé au départ.
- nogene : comme active, mais tous les liens G retirés. Pas d'information
  réinjectée ; mesure si une nouvelle chaîne F peut être comptée à tort.

Les trois préparations ont même matière et14 composites initiaux. Un outil
construit consomme deux des six F déjà préparés, pas un ajout d'atomes ou de
nourriture. Aucun remodelage pendant le calcul. En dehors du retrait de liens,
les tableaux initiaux sont exactement égaux et vérifiés avant lancement.

## Critères prospectifs, arrêt et limites

Pour active, dans au moins2/3 graines :

1. Un nouveau F01 libéré entièrement constitué de composites fabriqués depuis
   P/R initialement libres (`constructed_detached_F`), outil initial exclu.
2. Un tel F entièrement nouveau réalise au moins une opération catalytique
   réelle **après** sa construction/expression. Vérifier ses IDs et les temps
   des produits, pas seulement un nombre de F exacts ou des opérations de l'ancien.

Contrôle nogene : aucun F nouveau et aucun F entièrement nouveau actif. Comparer
tous les split, y compris leurs réussites possibles. Formation et incorporation
des produits G/F, copie, stocks finaux et consommations sont aussi publiés.
Une incorporation quelconque n'est pas un outil refait ; les deux conditions
ci-dessus sont distinctes. Absences censurées à1200, pas impossibilités.

Budget9 tâches, deux travailleurs, checkpoints30s ; aucun suivi ou balayage
automatique au-delà de cette cohorte. Les diagnostics33 sont terminés avant
son lancement. Pas de nouveau système énergétique, bord ouvert ou homéostasie
revendiquée. Succès éventuel = renouvellement ponctuel du même outil dans un
petit bain sous lois communes, pas maintien intégré avec membrane ou information
riche. Échec : analyser amorçage vs accès/production/usage avant de changer les lois.
