# J1 terminé : activité froide, transfert limité et échec dans le grand bain

27 octobre2026.12/12 essais achevés à1200, sans erreur. Recette figée
[J1](campaign_recipes/J1_20261027T144451586423Z/manifest.json), code39fead3.
Post-traitement : `python experiments/analyze_constructed_tool.py <campagne>`.
Sources/scénarios, durées, événements et census génétique vérifiés ; chaque
nouveau lien P–R conserve ses vraies IDs et les inventaires totalisent102 billes
P/R dans les12 essais. L'outil initial n'est pas compté comme F nouveau.

| Condition | Dimères catalysés0/1/2 | Incorporés0/1/2 | G nouveaux0/1/2 | F nouveaux0/1/2 |
| --- | --- | --- | --- | --- |
| Petite boîte, préparé | 18 /38 /21 | 2 /5 /1 | 0 /1 /0 | 0 /0 /0 |
| Petite boîte, délié | 0 /18 /0 | 0 /1 /0 | 0 /0 /0 | 0 /1 /0 |
| Membrane, préparé | 13 /13 /11 | 0 /0 /0 | 0 /0 /0 | 0 /0 /0 |
| Membrane, délié | 0 /0 /0 | 0 /0 /0 | 0 /0 /0 | 0 /0 /0 |

Le témoin délié1 s'exprime en F : ses18 actes et son incorporation1 sont attribués
à un **outil exprimé**, pas au préparé. Il montre qu'à0,08 une expression suivie
d'activité et d'incorporation est possible dans la petite boîte, à cet horizon.
Ce n'est pas une réussite3/3, ni une propriété démontrée du bain membranaire.
Les préparés fabriquent des produits incorporables3/3 en petite boîte, mais
ne renouvellent aucun F complet pendant ces essais.

## Où reste la matière ?

Le census final sépare précurseurs libres, dimères isolés, chaînes compatibles
avec la cible et autres polymères. « Compatible » désigne la structure, pas une
activité prouvée. L'analyse est extérieure aux lois, sans avance de simulation.

- Préparé froid1 :38 dimères fabriqués, encore34 monomères isolés et seulement
  4 P +4 R libres ;5 composants catalysés incorporés,4 unités F dans des fragments
  déliés non cibles. Un grand nombre de produits ne ferme donc pas la boucle.
- Préparés membranaires :16/17/14 monomères isolés,29/28/31 P libres et autant
  de R libres. Aucune unité F dans un fragment délié non cible : la fragmentation
  n'explique pas cet échec de transfert dans les6 bains membranaires.
- Distance médiane finale des monomères G au gène initial :7,18/5,80/6,78 dans
  les bains préparés, contre2,88/2,70/3,82 dans les petites boîtes préparées.
  C'est un diagnostic spatial final, pas une mesure de taux ou une preuve causale.

J1 combine présence de L et changement du domaine disponible. Petite boîte8×6,
frontière d'aire environ3800 dans un monde90×90 : les102 billes génétiques ne
remplissent pas le budget cellulaire1712 intérieur. Les essais ne prouvent donc
pas que L inhibe directement la chimie. Le prochain témoin doit conserver le
même paquet/RNG et changer séparément confinement global et présence de L.

## La frontière reste fragile

Fermeture des bains préparés :0,842/0,608/0,650 ; fractions classables0,986/0,921/
0,902. Déliés :0,386/0,628/0,428, classables0,701/0,865/0,797. Ces résultats ne
démontrent ni rétention globale ni domination causale d'un état initial ; les
tirages divergent après changement de liens et la cohorte est petite. Ne pas
transformer les périodes inconnues en étanchéité. L'insertion de L n'est pas
sa fabrication par F, qui reste absente.

## Décision

Conserver les lois et tester J2, deux mondes sans L : grand90×90 et compact8×6,
chacun préparé/délié sur0/1/2 à1200. Même paquet initial à translation près,
mêmes vrais atomes et même PRNG initial ; les murs globaux sont un contrôle
explicite d'environnement, jamais une paroi cachée autour du gène dans la cellule.
Pas de recyclage ou de régulateur ajouté avant ce diagnostic. L'homéostasie faible
devient une obligation explicite, mais aucun régime de maintien n'est encore testé.
