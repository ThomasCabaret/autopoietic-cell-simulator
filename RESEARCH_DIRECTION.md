# Rechercher une chimie dont les fonctions appartiennent aux assemblages

Outil de travail actuel : [simulateur et lancement des démonstrateurs](README.md),
[architecture du moteur partagé](SIMULATOR_ARCHITECTURE.md),
[validation de migration](research/ENGINE_MIGRATION.md).

État courant : [maturité](research/MATURITY.md), [bilan du lot 6](research/BATCH_06.md),
[priorités et décisions](research/PRIORITIES.md),
[architectures de fermeture conditionnelle](research/CELL_ARCHITECTURE.md).

Suite dynamique de cette première exploration : [journal](research/LOG.md),
[modèles et helpers](research/MODEL.md), [registre des essais](research/RESULTS.md).
La méthode réutilisable est dans `.agents/skills/local-chemistry-research/SKILL.md`.

Le lot 3 obtient des contours membranaires depuis des dimères isolés sur trois
graines et des ligations répétées préorganisées par une petite chaîne préparée.
Ce dernier prototype reste distinct des F composites exprimés : le transfert
dans une chimie commune et la reconstruction des outils demeurent les verrous.
Le lot 4 réalise ensuite ce transfert : sous C2D, des F composites exprimés depuis
G soutiennent plusieurs ligations par une même chaîne sur trois graines. Il manque
encore des produits incorporables, la coexistence copie/expression et la membrane
dans ce même univers. L'activation alimentaire est un helper explicite.
Le lot 5 réunit ensuite copie, traduction et opération sur 001, en réutilisant
la coopération locale plutôt que de rendre obligatoires deux faces. La longueur
six ne donne pas encore cette coexistence. L'[évaluation de santé](research/PROJECT_HEALTH.md)
priorise désormais la constructibilité des composants, puis fragments et transport.
Le lot6 construit des dimères depuis P/R libres puis les incorpore dans G et F.
La formation reste spontanée ; l'activité des outils n'est pas encore portée
sur ces précurseurs. Le transfert catalytique C3B est la prochaine décision.
Les propositions et criblages ci-dessous conservent le cadrage historique ;
les preuves actuelles et priorités sont dans les documents liés ci-dessus.

Référence complémentaire conservée après revue du dossier temporaire :
[idées et architecture de l'ancien moteur](research/LEGACY_PROJECT_NOTES.md).

## Cadrage corrigé

Le point de départ autorisé est une cellule construite : membrane, contenus et
organisation initiale peuvent être préparés. L'apparition spontanée de cette
cellule depuis une soupe n'est pas un objectif. La définition du système minimal
et sa réalisation sont deux parties du même travail de recherche ; les seuils de
réussite se préciseront avec les expériences.

Le verrou prioritaire est l'**indirection entre particules et fonctions**. Il faut
un petit alphabet de composants et des lois locales fixes permettant de
construire des assemblages dont la forme, la connectivité et les états mécaniques
produisent des interactions effectives et des fonctions nouvelles. La cellule
devra transformer des ressources en ces assemblages et remplacer ses composants.
La réparation intervient dans ce fonctionnement ; elle n'impose pas de rechercher
l'origine spontanée de la cellule.

Au cadrage initial, seule la note TeX était disponible. Un ancien projet fourni
ensuite dans un dossier temporaire a été examiné et ses éléments utiles préservés
dans `research/legacy_reference/` ; la recherche n'en dépend plus.

## Hypothèse de travail

**Une chimie de petits assemblages déformables, à contacts courts, réversibles et
potentiellement multivalents.** La géométrie fait office de programme : elle rend
certains contacts simultanés possibles, en masque d'autres, rapproche des
substrats ou transmet une contrainte à une liaison.

Par exemple, un contact faible A-B peut être insuffisant pour maintenir une
association. Deux ou trois contacts compatibles disposés sur une même interface
peuvent stabiliser une orientation particulière. Deux interfaces opposées
peuvent favoriser une chaîne ; leur angle peut favoriser une chaîne courbe.
Cela reste une hypothèse d'assemblage à vérifier avec les concurrents possibles.

La composition et la disposition ne remplissent pas le même rôle : un même
ensemble de composants peut présenter deux faces opposées, deux faces inclinées,
une poche, ou des sites exposés sans coopération. Aucune de ces organisations ne
doit devenir un nouveau type reconnu par le moteur.

### Trois mécanismes à combiner

1. **Reconnaissance et valence par géométrie.** Plusieurs contacts faibles et une
   enveloppe stérique sélectionnent les partenaires et leur orientation. Des
   ports saturables peuvent faire partie des primitives. Ils ne suffisent pas,
   à eux seuls, à assurer une valence précise à l'assemblage entier.
2. **Catalyse par préorganisation et contrainte.** Un assemblage rapproche et
   oriente des réactifs, ou stabilise une configuration intermédiaire. Une loi
   locale de réaction reste identique dans le bain et près de l'assemblage.
   L'assemblage augmente sa fréquence effective sans test « enzyme présente ».
3. **Libération par couplage local.** La formation d'une liaison peut changer la
   géométrie, saturer un port auparavant disponible ou modifier un état local.
   Il faut mesurer la sortie du produit et la disponibilité du catalyseur pour
   un nouveau cycle. Une simple adsorption forte ne constitue pas ce résultat.

Le premier mécanisme paraît le plus accessible. Le troisième risque de devenir
le verrou suivant : les contacts qui capturent bien un substrat peuvent aussi
retenir son produit. Une source d'énergie externe ou des précurseurs activés
restent des simplifications autorisées, à décrire explicitement.

## Criblages numériques réalisés

Script : `experiments/composite_geometry.py`. Résultats complets :
`experiments/results/screening.json`. Exécution :

```powershell
python experiments/composite_geometry.py
```

Dépendances utilisées : Python 3.12, NumPy 2.0.2, Matplotlib 3.10.0.

### Modèle effectivement calculé

Trois espèces seulement : N inerte, A et B complémentaires. Toutes les billes
ont un diamètre de 1. Leur potentiel est isotrope : exclusion dure pour une
distance inférieure à 1 ; attraction A-B de la forme
`-epsilon * exp(-((r - 1)/0.12)^2)` jusqu'à une distance de 1.5 ; zéro autrement.
La même table d'interactions est utilisée partout. Les énergies sont exprimées
en unités kT. Quand epsilon est balayé, il change pour toutes les interactions
élémentaires du calcul, sans distinction de rôle moléculaire.

Les supports sont des configurations construites et maintenues fixes. Ce sont
des approximations d'assemblages fortement liés pour un **criblage statique**.
Les ressorts, le repliement, la synthèse et la diffusion des assemblages ne sont
pas simulés. Leur géométrie est prescrite ; obtenir ces formes depuis un alphabet
fixe de liaisons reste donc à démontrer.

### 1. L'orientation effective dépend de l'assemblage

Deux agrégats de neuf billes ont chacun deux A sur leur face gauche et deux B sur
leur face droite. Je compare une forme rectangulaire et une forme en coin.
Composition, potentiels et force d'attraction élémentaire restent identiques.

Avec epsilon = 2.5, le minimum du balayage translation/rotation est :

| Forme construite | Rotation relative préférée échantillonnée | Énergie |
| --- | ---: | ---: |
| Rectangulaire | 0° | -5 kT |
| Coin de 30° | 30° | environ -5 kT |
| Un contact élémentaire A-B isolé | pas d'orientation privilégiée | -2.5 kT |

L'interaction entre assemblages devient directionnelle alors que chaque
attraction élémentaire est isotrope. Le balayage est limité aux translations
d'un côté du support et aux angles de -90° à 90°, par pas de 1° ; la translation
est discrétisée par pas de 0.04 diamètre. Il fournit une enveloppe de minima
d'énergie, **pas une énergie libre ni une trajectoire d'autoassemblage**.

### 2. Contre-exemple : directionnalité ne signifie pas valence contrôlée

Dans ce même modèle, après le double contact entre deux agrégats, un troisième
peut encore se fixer à un coin déjà utilisé. Une configuration explicite donne
-5 kT pour la première interface et -2.5 kT supplémentaires pour cette branche,
sans recouvrement ni répulsion avec le voisin.

Le modèle isotrope actuel **ne garantit donc pas des chaînes sans branchements**.
Il faut tester des contacts saturables, des protections stériques et/ou davantage
de contacts faibles par interface. Une règle globale imposant « deux voisins
maximum par molécule » masquerait précisément le problème recherché.

### 3. Deux sites adhésifs isolés ne suffisent pas ici

Deux substrats B sont placés à l'équilibre dans un même domaine fini, de
9.6 x 9.6 diamètres. Ils interagissent avec un support, et s'excluent mutuellement.
La grandeur mesurée est la probabilité que leur distance soit entre 1 et 1.2.
Il n'y a pas encore de réaction chimique.

Sur un support de neuf billes, je place deux sites A à trois dispositions
différentes, à composition et positions des billes identiques. Avec epsilon =
2.5, les probabilités sont proches de 1.45 à 1.47 %, contre 1.49 % sur le même
support entièrement inerte. Ce test ne montre **aucune amélioration utile**.
Le simple encombrement du support explique déjà une partie du contact observé.
Les variations de la dernière discrétisation sont de l'ordre de 1 % relatif ;
les petites différences entre dispositions ne constituent pas un effet robuste.

### 4. Des poches à contacts multiples donnent un effet géométrique

Autre support construit, toujours avec les mêmes potentiels : trois A alignés,
espacés de s, et deux N derrière eux. Deux cavités exposées permettent chacune à
un B de faire simultanément deux contacts A-B. Je compare s = 1.1 et s = 1.6,
sans changer la composition ni introduire de loi de poche ou de catalyse.

À epsilon = 5, la probabilité de proximité des deux substrats est d'environ :

| Disposition | Probabilité de distance dans [1, 1.2] |
| --- | ---: |
| Poches rapprochées, s = 1.1 | 15.5 % |
| Poches écartées, s = 1.6 | 2.3 % |
| Boîte vide | 1.3 % |

Ce sont des probabilités à l'équilibre, conditionnées à l'absence de recouvrement
des deux substrats. Le calcul intègre leurs positions par quadrature et
autocorrélation FFT avec remplissage de zéros, sans condition périodique.
Le passage d'un pas spatial de 0.01 à 0.005 change le premier résultat d'environ
3 % relatif et le second de moins de 1 %. Le script conserve aussi les pas plus
grossiers et un balayage de epsilon = 2.5, 4, 5, 6. Les poches ont peu d'effet à
2.5 ; leur gain dépend donc aussi du régime d'affinité, pas de la forme seule.

Le contraste entre les deux dispositions soutient la piste d'une fonction
géométrique à l'échelle d'un agrégat. Il ne mesure ni vitesse de réaction, ni
orientation réactive, ni renouvellement du catalyseur. L'attraction renforcée
peut poser un problème de piégeage du produit. Il n'y a donc **pas encore de
démonstration de catalyse**.

### Vérifications du calcul

Le script vérifie l'exclusion, la table de compatibilité, la symétrie de
l'énergie entre partenaires et l'énergie d'une interface construite. Il compare
aussi l'intégrale FFT à une somme directe indépendante sur un petit exemple.
Le raffinement spatial vérifie la sensibilité des probabilités à la grille.

## Ce que je propose de construire ensuite

La prochaine unité de travail devrait être un petit moteur de billes mobiles
avec liaisons locales et déformations, avant toute intégration cellulaire. Il
devrait ne connaître que des types élémentaires, positions, ports, états locaux
et liaisons. Les identités d'agrégats seraient réservées à l'analyse a posteriori.

Il faut figer un alphabet et les paramètres élémentaires, puis obtenir trois
objets par leur composition et leur connectivité :

1. Un sous-ensemble qui s'associe en chaîne avec une valence effective contrôlée,
   en présence de collisions concurrentes. Mesurer les branches et pièges, pas
   seulement illustrer la chaîne désirée.
2. Une variante qui modifie l'angle ou masque une interface, sans modifier les
   lois du moteur. Cela teste le transfert de fonction par architecture.
3. Un assemblage qui accélère une même réaction locale sur plusieurs cycles,
   avec produit libéré. Le comparer à ses composants séparés et à une variante
   de même composition mais de géométrie différente.

Dans cette étape, on peut toujours préparer les assemblages initiaux. En
revanche, on doit vérifier que leurs liaisons locales les maintiennent sans
contrainte rigide globale. Les longueurs et angles de liaison ne devront pas
être retouchés individuellement pour attribuer une fonction à chaque objet :
leurs valeurs devront découler d'un petit alphabet fixe.

Ensuite seulement, une synthèse guidée par un polymère devra produire ces mêmes
objets à partir des ressources. Le couplage avec la cellule viendra après ce
passage de la composition à la fonction et son renouvellement matériel.

La « complétude » recherchée peut d'abord être une **fermeture constructive pour
une bibliothèque de fonctions essentielles** : avec les ressources et les
opérations disponibles, le système peut refaire ses propres pièces. Il n'est
pas nécessaire de démontrer une universalité mathématique pour ce premier but.
Les criblages présents ne démontrent pas encore cette fermeture.

## Travaux voisins utilisés pour orienter la recherche

- Muñoz-Basagoiti, Rivoire et Zeravcic, *Catalysis from the bottom-up* (prépublication,
  2022), https://arxiv.org/abs/2211.12107 : un catalyseur dimérique conçu à partir
  de particules peut accélérer la coupure d'une liaison. C'est une référence
  particulièrement pertinente pour la catalyse par géométrie et contrainte.
  Les calculs ci-dessus sont un modèle exploratoire distinct, pas une
  reproduction de leurs résultats.
- Sacanna et al., *Lock and key colloids* (Nature, 2010),
  https://www.nature.com/articles/nature08906 : reconnaissance et assemblage
  réversibles par complémentarité de forme. Cette référence motive l'examen
  d'enveloppes stériques et de poches.
- Zeravcic et Brenner, *Spontaneous emergence of catalytic cycles with colloidal
  spheres* (PNAS, 2017), https://pmc.ncbi.nlm.nih.gov/articles/PMC5410808/ :
  templating entre agrégats avec interactions dépendant du temps. Leur
  implémentation déclenche la dissociation en fonction du nombre de liaisons du
  réseau ; ce mécanisme ne serait pas admissible tel quel sous la contrainte de
  localité de notre note.

Ces références rendent des mécanismes particuliers plausibles ; elles
n'établissent pas que le petit alphabet recherché suffira à une cellule viable.
