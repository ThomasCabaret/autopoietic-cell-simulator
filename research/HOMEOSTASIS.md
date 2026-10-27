# Homéostasie faible : obligation de maintien, pas encore réalisée

27 octobre2026, intention précisée par l'utilisateur. Il ne faut pas une consigne
exacte pour chaque concentration, mais un domaine où les stocks fonctionnels
restent bornés et récupèrent après perturbation sans disparition irréversible
d'une fonction essentielle. La cible est une cellule construite ouverte en
matière/énergie, pas un réservoir fermé qui s'arrête faute de nourriture.

## Deux échecs à distinguer

1. Accumulation de produits, fragments, déchets ou catalyseurs qui augmente
   durablement la charge ou épuise les ressources d'une autre voie.
2. Chute sous un seuil de récupération : disparition de toutes les copies
   exploitables d'un gène, perte des outils permettant leur propre reconstruction,
   ou matière immobilisée dans des états inaccessibles sous les lois présentes.

Le nombre total de billes est actuellement fixe ; cela borne les stocks par
épuisement, sans prouver l'homéostasie. J1 contient en outre des assemblages P–R
et backbones sans voie de recyclage. Un stock de monomères non utilisés peut
augmenter alors que les outils ne sont pas renouvelés. Un fragment F délié ne
peut plus être recapturé comme monomère, mais certains fragments peuvent encore
catalyser : ne pas confondre piège de templating et inertie chimique absolue.

## Ordre de solutions à comparer

Examiner d'abord des mécanismes réutilisables : entrée/sortie selon gradients
locaux ; réactions réversibles et recyclage de matière ; consommation en aval.
Une consommation interne ne fait pas sortir la matière : pour une cellule de
taille bornée maintenue, les entrées doivent être compensées en moyenne par
des sorties réelles, après recyclage éventuel. Énergie et déchets sont comptés.

Une saturation enzymatique plafonne un débit, pas nécessairement un stock.
Si des produits s'accumulent encore, tester une inhibition **réversible** par
occupation locale d'un site réutilisable. Aucun `if concentration > seuil` dans
les lois. Ce mécanisme n'est pas implémenté par les captures P/R actuelles,
qui excluent les atomes déjà assemblés ; toute extension devra être déclarée,
comptée et comparée aux références. Une inhibition permanente serait un piège.

Pour l'extinction : redondance des templates, stabilité de liaisons et flux de
reconstruction supérieurs aux pertes. Une stabilité différente doit venir de
propriétés chimiques/motifs locaux, jamais d'un label « gène à protéger ». Avec
peu de copies et des pertes aléatoires, aucune immortalité n'est garantie. Si la
dernière information exploitable est perdue, ne pas la réinjecter silencieusement.
L'ajout d'un outil de recyclage/régulation implique son gène et son renouvellement.

## Ce qui devra être mesuré

Figer lois, apports et horizons puis perturber les stocks initiaux et les apports
(manque, excès, arrêt/reprise externes préprogrammés). Suivre chaque famille
essentielle, la matière, les concentrations et le volume, le flux effectivement
incorporé, les déchets exportés, les temps de récupération et les extinctions.
Les seuils/bandes et durées se déclarent avant les essais ; les absences restent
censurées. Aucun stock global mesuré ne pilote une réparation ou une production.

Compter séparément récupération après perturbation, maintien sous pertes et
survie sur un horizon fini ; un génome initial intact dans un modèle où aucun
backbone ne se dégrade ne prouve pas sa résistance à des pertes. La réussite
stationnaire doit concerner toutes les fonctions, pas une moyenne dominée par
les lipides. La croissance seule n'est pas un renouvellement.

État : obligation explicite et futurs tests, aucune homéostasie dynamique validée.
Avant de construire un régulateur, terminer le diagnostic J2 du transport/domaine.
