# Fidélité à l'objectif : localité et risques de pilotage

Lot9,25 octobre2026. La cible est une implémentation locale de fonctions qui
n'ont de sens qu'à l'échelle des assemblages. Concevoir une chimie, fournir
énergie et conditions initiales ne dispense pas de cette contrainte.

## Ce qui invaliderait une démonstration

- Lire une séquence, une longueur cible ou un génome entier pour déclencher
  copie, fin de copie, expression, repliement ou fonction enzymatique.
- Reconnaître une protéine/vésicule comme objet complet puis lui attribuer un
  comportement. Donner à une bille « enzyme N » toute sa fonction serait une
  autre façon de déplacer la réponse dans les primitives.
- Identifier un contour, son intérieur, son rayon/aire ou ses membres dans une
  règle, puis refermer, repousser le contenu, choisir une insertion ou transporter
  une molécule pour atteindre le résultat. Une pression globale de consigne serait
  également un pilotage, même calculée depuis les coordonnées.
- Faire une conversion/relocalisation externe d'un produit entre fabrication et
  usage, changer les lois au moment opportun ou corriger l'état depuis l'analyse.
- Programmer un calendrier de sauvetage ciblé sur les événements observés.
  Une condition externe fixée d'avance est une aide différente, à déclarer.
- Présenter un anneau préparé comme autoassemblé, une bille-sonde comme un gène
  réellement retenu, ou des mécanismes séparés comme une cellule intégrée.

Une interaction sur quatre/six billes liées, de portée et d'arité fixes, reste
locale si elle lit uniquement leurs attributs et liens voisins. Le fait que ce
motif contienne tout un petit dimère n'autorise pas une inspection arbitraire
d'une future macromolécule. Le coût du motif doit rester borné lorsque celle-ci
grandit. La localité ne suffit pas : une primitive spécifique par fonction peut
écrire implicitement le programme attendu. Mesurer réutilisation et complexité.

## Audit du code au départ du lot9

| Zone | Lecture dans la dynamique | Diagnostic et réserve |
| --- | --- | --- |
| `copy.py` | Reconnaisseurs liés, arêtes voisines et ports ; motif parallèle de ligation | Pas de séquence complète dans `react`/forces. `sequence` sert à l'initialisation ; l'observateur reconnaît les produits |
| `assembly.py`/`precursors.py` | Deux précurseurs, deux F voisins liés, six billes au total | Aide catalytique explicite ; pas de reconnaissance d'enzyme entière. Alphabet de précurseurs spécialisé et diversité limitée |
| `docking.py` | Deux H–T, leurs faces saturées, géométrie à quatre billes | Aucun contour ni taille souhaitée. Les longueurs locales induisent une courbure préférée ; ne pas régler celle-ci en ligne depuis un rayon global |
| `engine.py` | Voisins spatiaux, forces, diffusion, boîte imposée | Taille des tableaux et arbres spatiaux sont de l'infrastructure, pas une identité biologique. La boîte ne doit pas remplacer la membrane |
| `observations.py` | Graphes complets, séquences, provenance, contours | Autorisé pour mesurer uniquement. L'API donne des références vivantes : risque de rétroaction accidentelle à couvrir par tests |
| Cycle génétique | Temps uniforme, période et phase de déliaison | Forçage externe global réel, pas autonomie en bain stationnaire. Fixé avant les runs, sans consultation des copies ; étudier/ablate sa nécessité |

Les gardes « plus aucun précurseur disponible » peuvent accélérer le calcul si
elles ne changent aucune transition locale éligible. Les champs de rayon ou de
labels de départ sont permis dans le constructeur ; ils ne doivent pas réapparaître
dans les forces/réactions. Permuter les IDs ne doit pas changer une force physique.

## Obligations du lot9

Le grand anneau et les cohortes de sondes sont préparés et marqués seulement
pour analyse. Les contacts H–H/T–T de V8 se rompent/reforment sans reconnaître
leur composante. L'insertion est une observation après coup de nouvelles unités
dans un contour issu de l'anneau ; ce n'est jamais une opération du moteur.

Une barrière locale sur un lien de membrane peut repousser une sonde : deux
extrémités et une sonde, trois billes, force et réaction distribuées par gradient.
Elle doit exister aussi sur un fragment ouvert, agir des deux côtés et rester
indépendante de l'intérieur. Une sonde transparente est un contrôle physique,
pas une preuve que X/Y/Z et les vrais G/F passent/sont retenus comme souhaité.

Tests : gradient, moment/force totaux, arité indépendante de l'agrégat, modification
des seuls labels/rayon initiaux sans effet après préparation, arbre/exhaustif,
reprise, et trajectoire avec/sans observateur identique. Archiver échecs et helpers.

## Audit des ouvertures, lot11

`boundary_audit.py` lit composantes, IDs initiaux, extrémités et épisodes uniquement
après l'observateur. Aucune de ces informations n'est consultée par les forces
ou réactions. Il ne dessine pas de nouveau contour et ne corrige aucun état.
Les observations physiques antérieures, positions et PRNG restent identiques,
y compris dans le pilote comparé aux sources du lot9. Les extrémités proches
sont un diagnostic de géométrie, jamais une règle de refermeture ni une preuve
de confinement. Le coût ajouté est analytique, sans type/port/helper physique.

## Condition d'échange G1, lot12

`contact_exchange.py` peut lire les autres ports du partenaire libéré et de
l'arrivant. Si les deux sont occupés, le swap est interdit ; sinon ancien taux
et géométrie. Lecture bornée d'états de ports déjà existants sur trois dimères,
pas d'inspection de longueur, de composante ou de molécule biologique complète.
Un contact est remplacé par un contact, aucune fermeture ou relocation imposée.
Le prédicat est symétrique au swap ; cela ne prouve pas l'équilibre détaillé.

Coût : une condition/mode logique, zéro type, état mémorisé ou taux/rayon ajouté.
La chimie modifiée est déclarée G1 ; ne pas lui attribuer les réussites de B.
L'aide cinétique non thermique antérieure reste une dette énergétique explicite.
Le choix du mode est figé avant les essais et ne dépend jamais des observateurs.
## Contrat de reprise et bain J0

Voir [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) : la localité est nécessaire,
mais ne démontre ni minimalité ni richesse des assemblages.

J0 lit, pour chaque atome P/R, l'existence de son lien P–R saturé : deux atomes
réels. Cet état active son contact avec une bille L ou un segment H–H lié ;
la force de segment porte sur trois atomes et est symétrique dans l'espace.
Les listes d'atomes sont des index de types chimiques, jamais des composantes
biologiques. Aucun parcours de polymère ou contour ne dirige ces contacts.

Coût croisé : deux constantes de contact, rayon0,55 et raideur80, reprises aux
valeurs de la barrière existante, plus le prédicat libre/lié. Zéro élément,
outil ou gène ajouté aux six types hérités ; union non minimisée. La commutation
peut changer l'énergie : aide non calibrée déclarée. Température unique imposée.
Les tests couvrent observateur sans rétroaction, force de réaction sur L,
état de liaison, mêmes positions/PRNG après reprise, caches spatiaux séparés
et absence de parois internes. Les contours sont réservés aux mesures, qui
abandonnent les intervalles inconnus. Production de L par F non implémentée.
