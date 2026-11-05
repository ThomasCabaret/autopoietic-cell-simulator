# Lot49 — coût local de chaque transition de contact L

5 novembre2026. Intégration énergétique, pas nouveau thermostat ou outil.
Registre18/43 et dépendances relus : Q-01/C-02 bloquent M-04/M-05 ; protection,
répartition des polymères, information et diversité restent des gaps distincts.

## Résultats clos et décision

EL1 exact :2100–2200,1110 updates et5 échanges ; updates delta net565.8112,
dont ports560.7266 et barrière5.08455. Formations seules493 appels,+2629.0309 ;
ruptures seules534 appels,-2088.4552 ;83 appels mixtes. Chauffage d'abord des
atomes issus de nourriture H/T, puis de la frontière préparée. Échanges :-7.07554.
Ne pas confondre ce bilan de potentiel commuté et un bilan complet de chaleur,
ni corrélation et causalité. Le suivi CF1 est une intervention ciblée falsifiable.

RP1 refuse : G0014/3/6, F0011/0/0, réassemblages13/2/6, réincorporations3/0/1.
Pas de transfert vers EG1 et pas de nouvelle grille de taux. Examiner si le motif
protégé est accessible sous les captures actuelles avant autre variante. Piste
qualitative : protéger un motif actif cohérent plutôt que toute occupation,
mais son coût, sa réalisation et la protection de l'information restent ouverts.

## CF1 — formation/rupture et échange sous le même coût physique local

Réutiliser le delta de ports déjà implémenté pour un retrait/ajout facultatif
de contact. Deux L (quatre billes) et interactions incidentes à la même coupure ;
barrière P/R du seul segment retiré ou formé. Le remplacement garde ses trois L.
Le facteur thermique existant vaut1 pour deltaU<=0,exp(-deltaU/T) sinon.
Géométrie, taux de tentative, état libre/lié, température, bruit et cadences
inchangés. Aucun contour, agrégat complet, origine, objectif ou stock dans la règle.

Coût : une option de filtrage des updates de contacts, aucun paramètre numérique,
type, port, état, gène ou outil supplémentaire. Pas une thermodynamique complète :
taux on/off et leurs domaines ne sont pas rendus symétriques ; helpers P/R et
cycle externe restent explicites. Pas de correction rétroactive des positions.
Défaut none garde les préfixes/RNG historiques ; observer/checkpoint passifs.

Avant calcul long : delta exact et signe inverse avec voisins/PR ; refus d'une
hausse àT0, rupture descendante, formation de contact entre L libres àT>0 ;
callback obligatoire pour barrière, passivité/reprise et anciens préfixes.
Une formation sur contact construit n'est pas auto-assemblage d'une vésicule.
M-01 reste une preuve historique séparée ; pas adoption universelle de CF1.

Pilote : graine2 au pas fin,100 unités, invariants0, fermeture temporelle>=.8,
T75–100<=.12, propositions d'update>0. Si refus : rapport et arrêt, aucune relance.
Si passe et sources inchangées, préparer/lancer automatiquement la cohorte figée.
Le pilote ne démontre ni tenue tardive ni insertion.

Cohorte6 essais : mêmes recettes EG1/EN1,3 graines par pas jusqu'à2400, seul
contact_update_gate=metropolis ajouté. Références précédentes réutilisées et
hachées, pas nouveaux témoins noL/sans synthèse.2 travailleurs,3h, checkpoints30s.
Portes par pas : invariants0, fermeture tardive>=.8 et T<=.12 chaque graine,
insertion dans>=2 graines, médianes G/F/L positives et>=moitié de la référence
du même pas ; comptabilité des propositions. Rapport puis arrêt, aucun retry,
tuning, promotion de démo ou seconde phase automatique.

Si chaleur disparaît mais insertion aussi : distinguer coût des poses et accès,
ne pas modifier plusieurs taux. Si chaleur persiste : revenir au bilan des autres
transitions/forces. Si aucun progrès de mécanisme, revoir la représentation des
contacts avant une autre constante. Le moteur, le delta local et les contrôles
restent réutilisables si CF1 échoue. Pas de promesse de maintien ou d'homéostasie.


## Pivot déclaré après les premiers checkpoints CF1

Pause anticipée décidée avant la fin de cohorte : deux préfixes ont environ4M
propositions de formation refusées chacun, avec1/0 contacts restants pour75 L.
La majeure partie du budget est consommée sans perspective utile pour les quatre
autres essais. Garder ces préfixes censurés, les sources et le refus d'adoption ;
aucune porte de cohorte calculée sur un sous-ensemble.

CP1 sera un prototype statique seulement : attraction normalisée par concurrence
aux deux ports, potentiel/force binaires exactement préservés, charge de chaque
port<=1. Aucun nouveau nombre ajustable. Vérifier gradient analytique et exclusions.
Sur chacun des deux checkpoints pausés, choisir au plus12 formations admissibles
par mismatch croissant (mêmes contacts pour les deux potentiels), comparer deltas
et facteurs thermiques. Ce sondage sélectionné n'est ni distribution globale,
ni cinétique, ni preuve de vésicule ou de réussite d'une nouvelle chimie. Pas de
longue campagne avant cette vérification et un futur delta local adapté (énergies modifiées au second rang, partitions
pouvant nécessiter le troisième ; aucun calcul global de sens biologique).
