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

Précision utilisateur après LT2 : une cinétique de mélange efficace est une
base de travail fondamentale. L'accélération de réactions parasites révèle
un problème de chimie à résoudre ; ralentir le mouvement ne le résout pas.
Conserver les références historiques pour comparer, mais ne pas les utiliser
pour masquer un défaut révélé par le mouvement choisi. Distinguer l'instabilité
numérique, qui demande une correction technique, de la fragilité d'une structure
ou d'une sélectivité, qui demande un diagnostic et une conception locale.

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

La fonction des assemblages est un jalon central, pas une propriété supposée
pour après la stabilisation génétique. Lire FUNCTIONAL_MECHANISMS.md : avant
de multiplier des corrections de copie, établir une famille plausible puis
des productions distinctes et transférables sous lois fixes. Un seul assembleur
polyvalent et local ne prouve pas encore un répertoire programmable d'outils.
Un blocage de copie reprend la priorité s'il empêche le transfert d'une fonction
déjà établie. Déterminer les longueurs depuis les mécanismes, pas depuis les
cas de budget12/24/48 ; ces nombres ne deviennent jamais des cibles fonctionnelles
sans preuve. Toute unité supplémentaire doit avoir un rôle ou un avantage testé.

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

## Résoudre un verrou par un nouvel outil moléculaire

Précision utilisateur du 29 octobre 2026 : envisager explicitement plusieurs
voies face à un verrou identifié : améliorer un mécanisme local existant,
concevoir un nouvel assemblage fonctionnel sous les mêmes lois, ou réexaminer
la représentation. Ne pas supposer que toute difficulté doit être résolue par
une modification des lois générales. Une machine moléculaire peut réserver
une opération à ses contacts et éviter de perturber tout le bain.

Exemple hypothétique : un assemblage se lie localement à des composants de
membrane et à une molécule libre, favorise une transition de liaison, puis se
libère pour recommencer. Son activité doit provenir de ses constituants,
ports, géométrie et états locaux. Ne pas ajouter une primitive « insertase »
qui reconnaît une membrane entière et exécute son insertion. Une étiquette
de protéine, un gène complet ou un contour ne peut diriger la réaction.
Cette esquisse ne prouve pas que la chimie actuelle peut la réaliser.

Avant de proposer un outil supplémentaire, présenter :

- Le verrou et son diagnostic, les solutions plus simples considérées et le
  gain attendu par rapport à une modification des lois.
- Le mécanisme local envisagé, les primitives déjà disponibles et les ajouts
  éventuels ; distinguer nouvel assemblage et nouvelle loi.
- Le coût total : gène, expression, précurseurs, énergie, copies, transport,
  renouvellement et dépendances nécessaires pour refaire l'outil lui-même.
  Un gène supplémentaire n'impose pas nécessairement un nouvel alphabet.
- Les interférences possibles et le plus petit test discriminant : témoin
  sans outil ou avec assemblage inactif, libération et réutilisation, produit
  utile en aval, maintien des fonctions préexistantes dans le même bain.

Comparer la complexité totale et la fermeture causale, pas seulement le nombre
de règles ou la simplicité du démonstrateur isolé. Éviter une chaîne d'outils
auxiliaires dont chacun exige un outil supplémentaire non reconstruit.

**Suggérer cette option à l'utilisateur et attendre son feu vert avant de
mettre en œuvre un nouvel outil fonctionnel supplémentaire.** L'analyse
conceptuelle et la proposition sont encouragées ; elles ne valent pas
autorisation de l'ajouter. Cette décision utilisateur ne concerne pas les
contrôles ordinaires des outils déjà présents. Après accord, tracer la variante,
mettre à jour graphe causal, contrats d'interaction et budget de particules,
puis distinguer activité d'un outil préparé, fabrication et renouvellement.

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

## Automatiser les décisions calculables

Lire AUTOMATED_EXPLORATION.md. Les seuils, grilles bornées et contrôles enchaînés
dont la décision est formalisable sont exécutés par programme, avec leurs
budgets et critères figés. Garder l'interprétation pour les choix de lois,
représentations et incompatibilités. Le pilotage entre expériences reste externe
à la chimie ; aucune rétroaction d'un score global dans une trajectoire. Un
arbre sélectionné par les résultats est déclaré comme exploration, pas validation
indépendante. Ne pas automatiser une recherche illimitée qui repousse le jalon.

## Loupe microscopique motivée

Utiliser, au jugement de l'agent, une observation microscopique temporaire quand
une question de conception ou un comportement inattendu le justifie. Décrire
le mouvement ou l'enchaînement attendu à l'échelle de l'assemblage, puis cibler
la transition locale dont l'observation pourrait expliquer l'écart et orienter
une modification. La compréhension globale sert à concevoir les lois locales,
jamais à piloter les structures dans la dynamique.

Deux usages utiles : vérifier à la conception qu'une règle réalise le mécanisme
imaginé ; diagnostiquer ensuite pourquoi le comportement émergent ou la cinétique
globale s'en écarte. La cible peut être déterminée pendant le calcul, par exemple
autour de la première lésion. Borner le voisinage et la fenêtre temporelle,
motiver les données nécessaires et la décision qu'elles peuvent éclairer.
Voir KINETICS_AND_PERFORMANCE.md pour le contrat de capture.

Ce n'est ni un enregistrement systématique ni un passage obligé à chaque règle
ou lot. Une loupe sans question susceptible d'influencer la compréhension ou
la conception n'a pas de raison d'être activée. Arrêter ou réorienter le
diagnostic lorsqu'il a répondu à sa question ou n'apporte plus d'information.
