# Lot9 — grande frontière et fidélité aux lois locales

Clôture26 octobre2026.24 dynamiques achevées,586 empreintes sources et7904 images
auditées. [Recettes](BATCH_09_RECIPES.json), [plan](BATCH_09_PLAN.md),
[audit de localité](LOCALITY_AUDIT.md). Les données restent locales.

## Résultat et limites

219 dimères H–T préparés en anneau de rayon34,5,24 dimères libres et48 sondes :
534 billes. Ce bain réduit le risque de taille identifié au lot7 ; il ne contient
pas les quelque2406 billes du budget conditionnel de cellule. Ce n'est pas une
nouvelle preuve d'autoassemblage depuis molécules isolées : celle de V8 reste
distincte et à petite taille.

| Essai t150, graines0/1/2 | Fraction de contours fermés | Sorties observées des24 sondes internes |
| --- | --- | --- |
| A, barrière locale de lien | 0,841 / 0,837 / 0,857 | 0 / 0 / 0 |
| S, seuls contacts entre billes | 0,824 / 0,844 / 0,877 | 0 / 0 / 0 |
| Contrôle transparent | 0,841 / 0,821 / 0,857 | 12 / 14 / 10 |

Les sondes transparentes externes entrent aussi :10/12/16 dans S. La fraction
d'enveloppes classables est0,98–0,99. Absence de sortie observée n'est ni une
perméabilité nulle ni une preuve de rétention des vrais G/F. Àt450, S graine0
perd1/24 sonde ; fraction fermée0,844, classable0,987. La barrière portée par les
liens n'est pas indispensable au criblage testé. Sa suppression dans le candidat
d'échange reste à transférer, pas à supposer.

**Aucune insertion passive** dans les essais A, S, intérieur/extérieur/volume,
sans rupture thermique et géométrie sans courbure. La géométrie ancienne T–T0,65
fragmente le grand anneau : aucun contour parent classable. T–T1 maintient un
anneau préparé sur une graine ; formation libre à cette géométrie non établie.
Sans attraction, la frontière n'est classable que2,3% du temps : son zéro de
fuite ne compte pas comme rétention.

L'analyse échantillonnée de A0 retrouve21/24 molécules nouvelles à distance<2,2
du parent, mais aucun lien nouveau–ancien. Le minimum de décalage des ports vers
une face libre est1,658, au-dessus des captures0,25² et0,45² : problème d'accès
et de saturation plausible, pas preuve d'absence à tous les sous-pas.

## Variante B : échange associatif local

Un contact occupé peut changer de partenaire pour une face libre proche ; un
lien disparaît, un apparaît. Aucun déplacement ni fermeture automatique. Taux0,2,
capture0,8, extension≤0,35. Motif de trois dimères/six billes, sans type élémentaire
supplémentaire ni insertase primitive. Aide activée non thermique, sans bilan
énergétique calibré, désactivée par défaut.

Àt150, échanges0/0/2 et incorporations0/0/2. La graine2 reste sous le seuil initial
de fermeture0,8 :0,781, persistance maximale6, aucune sortie observée. Le suivi
**sélectionné** de cette graine àt450 obtient4 échanges, les mêmes deux IDs227/238
incorporés, persistance fermée10,5, fraction fermée0,821, aucune sortie observée.
L'extérieur graine0 ne donne aucun échange/insertion.

Ce suivi montre une voie locale possible, **pas une insertion robuste3/3**, ni
une estimation non biaisée de la réussite à450. Les ouvertures interrompent le
compteur de persistance ; il n'implique pas un suivi continu entre images.
Prochain : mêmes horizons sur toutes les graines, contacts admissibles/censures,
puis B sans barrière de lien et compatibilité avec les vrais composants.

## Localité, erreurs conservées et logiciel

Le pilote t10 avait compté six fausses sorties : une corde d'analyse de36 unités
fermait artificiellement un fragment ouvert. Sources et résultat conservés.
L'observation v2 ne ferme virtuellement qu'un écart≤2,5, sinon statut inconnu ;
les lois n'ont pas changé. Fermeture et classabilité sont séparées.

51 tests logiciels et7 historiques passent : gradient, forces/moments, échange
sur fragment ouvert des deux côtés, aucune relocalisation, valence, absence de
rétroaction de l'observateur/labels initiaux, permutation des IDs, arbre/exhaustif
et reprise exacte. Le traceur sur les sources B2 vérifie ses deux échanges et
retrouve positions, contacts et toutes métriques exactement. V8 et C3B1 retrouvent
tous leurs tableaux/métriques sous le moteur courant. Une reconstruction depuis
sources+recette de S0 retrouve également tous les tableaux/métriques.

Démo13=S0 ; travailleur graphique et headless identiques, rendu/relecture vérifiés
hors écran. Contacts parcimonieux :1,17Mo contre35,55Mo pour301 matrices à deux
rangées uint8 ; positions/checkpoints à compter séparément. Archives inchangées.

## Décision

Conserver S comme référence simple et B comme voie exploratoire d'insertion.
Ne pas ajouter d'insertase/gène sur cette seule preuve. La membrane reste séparée
de C3B1 ; ni fermeture physique de cellule, ni flux alimentaire réel, croissance
depuis L fabriqués ou maintenance ne sont démontrés. Cycle externe et helpers
spécialisés restent des dettes. Voir [cinétique/performance](KINETICS_AND_PERFORMANCE.md).
