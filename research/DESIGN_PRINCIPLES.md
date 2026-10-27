# Contrat de conception — 27 octobre 2026

Ce contrat explicite l'intention de l'utilisateur pour toute reprise du dépôt.
Il complète la méthode de recherche, les contrats d'interaction et l'audit de
localité ; il ne constitue pas une preuve que le candidat actuel les satisfait.

## Faire émerger les fonctions

Une cellule initialement construite est autorisée. Les petites billes peuvent
se superposer sélectivement ; ports, liaisons et états locaux sont permis.
Le réalisme chimique n'est pas un objectif en soi. Les fonctions doivent cependant
résulter des assemblages, sans pilotage par leur signification biologique.

Est exclue une dynamique qui lit une séquence complète, un contour, une identité
de cellule/protéine ou un objectif global pour décider une réaction, réparer,
trier, déplacer ou diviser. Une portée spatiale courte ne suffit pas si un type
primitif contient déjà toute la fonction attendue. Un motif de taille bornée
et une occupation de liaison sont admissibles, avec leur coût déclaré.
Les labels d'initialisation, d'origine et de mesure ne dirigent jamais les lois.
Une observation globale peut mesurer un succès, pas le provoquer. Les cycles
et apports externes sont fixés et déclarés avant le calcul, sans adaptation
aux besoins détectés de la cellule.

## Ne pas confondre localité, simplicité et flexibilité

Trois propriétés distinctes doivent être évaluées : localité des lois,
coût des primitives/helpers, diversité des fonctions obtenues sous ces lois.
Une règle locale différente par démonstrateur peut respecter la première tout
en échouant aux deux autres. Un moteur modulaire facilite une refonte, mais
n'établit pas que les succès chimiques survivront à celle-ci.

La preuve recherchée de flexibilité est un transfert : modifier des séquences,
géométries ou connectivités, conserver alphabet/lois/paramètres et obtenir
plusieurs outils utiles dont les produits sont utilisables en aval. Mesurer
les interférences et les régressions. Séparer ce qui est testé, plausible et
incompatible dans la représentation actuelle. Une matrice de contacts ou un
helper spécifique reste une dette tant que sa réutilisation n'est pas établie.

## Anticiper les incompatibilités avant un gros investissement

Chaque plan indique :

1. Le verrou global réduit et la capacité aval susceptible d'être empêchée.
2. Le plus petit contre-exemple expérimental accessible : conditions thermiques
   communes, composants libres/assemblés, produit transféré, espèce étrangère,
   longueur ou flux. Des modèles sous des bains thermiques incompatibles ne sont
   pas intégrés parce qu'ils partagent un ordonnanceur.
3. Le coût ajouté et son domaine de réutilisation, démontré ou seulement supposé.
4. Le critère de rejet et l'horizon de décision ; deux changements conceptuels
   sans transfert ni diagnostic nouveau imposent de revoir le choix de modèle.

Conserver plusieurs options conceptuelles quand un verrou est structurel ;
inutile de multiplier des branches ou d'entretenir plusieurs moteurs. Préserver
sources, recettes et échecs permet de comparer une alternative sans sauver
artificiellement chaque détail de l'ancienne chimie.

La division cellulaire est un exemple futur : exclure une opération qui détecte
une cellule pour la couper, examiner plutôt croissance, forces locales,
constriction et renouvellement. Aucune capacité de division n'est démontrée,
et sa réalisation n'est pas requise pour le jalon actuel de maintien d'une
cellule construite. La flexibilité n'est pas une promesse d'évolution ouverte.

## Décisions et maturité

Les acquis à préserver sont des comportements sous un candidat identifié,
pas les lignes de code. Accepter une refonte si les fonctions ne se composent
pas, plutôt que multiplier les exceptions. Relever le coût en interventions
de conception, séparément des essais automatisés. Mettre à jour arbre,
priorités, maturité et santé ; annoncer honnêtement séparé, commun ou couplé.

## Homéostasie faible et maintien

Lire [HOMEOSTASIS.md](HOMEOSTASIS.md) avant d'introduire alimentation continue,
pertes ou régulation. Prévenir accumulation et extinctions irréversibles fait
partie de la cible, sans imposer une concentration exacte. Un nombre fixe de
billes, un réservoir épuisé ou une saturation de débit ne démontrent pas ce
maintien. Les rétroactions doivent être locales et leurs coûts comptés ; tester
les deux sens de perturbation et la récupération, sans réinjection d'un gène perdu.

Pour l'environnement final, voir OPEN_BOUNDARY.md : apport réglable au bord du
domaine extérieur et absorption des sorties. Le nombre total peut varier ; ne
pas substituer à ce flux une concentration imposée près de la vésicule ni une
compensation de ses déficits par un observateur. Gradients/pénuries sont à mesurer.
