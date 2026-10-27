# Domaine extérieur alimenté par flux — cible, pas implémentation acquise

27 octobre2026, précision utilisateur. Vésicule construite initialement au centre
d'un domaine fini (carré en2D ; cube si un modèle3D est développé). Des précurseurs
arrivent au **bord du domaine extérieur**, diffusent normalement vers la cellule ;
des particules qui quittent ce domaine sont évacuées. Il n'est pas demandé de
maintenir le nombre total de particules constant dans le moteur final.

## Grandeurs distinctes

L'apport entrant est réglable par espèce, éventuellement suivant un calendrier
fixé avant essai. La sortie résulte de la diffusion à la frontière absorbante.
Le flux net vaut entrées moins sorties ; ni lui ni la concentration près de la
vésicule ne sont automatiquement imposés par le débit d'injection. Une forte
consommation peut produire une zone appauvrie et des gradients. Les mesurer,
ne pas réinjecter les manquants au voisinage de la cellule pour les supprimer.

La source/sortie est une condition d'environnement déclarée, pas un catalyseur
ou un mécanisme homéostatique cellulaire. Aucune identité de vésicule, contour,
espèce essentielle ou stock interne ne doit contrôler les créations/suppressions.
Des réglages humains en démonstration sont des forçages externes à enregistrer ;
un essai scientifique fixe son protocole, sans correction automatique cachée.
La source apporte uniquement les précurseurs déclarés : injecter des gènes ou
des outils complets pour compenser leurs pertes masquerait le renouvellement.

## Contrat à implémenter ultérieurement

- Arrivées selon un flux défini par unité de bord et de temps, positions locales
  au bord ou dans une couche d'entrée explicite. En brownien, injecter exactement
  sur une frontière absorbante pose un problème de retour immédiat : choisir et
  calibrer la convention/couche et son lien à dt, sans avantage numérique caché.
- Absorption liée à la position extérieure, jamais au rôle biologique. Nettoyer
  les liens incidents sans liens fantômes, conserver les IDs/origines pour la
  mesure et compter la matière perdue. La règle précise sur un composé partiellement
  sorti reste à fixer ; ne pas supprimer arbitrairement tout un agrégat biologique.
- Une séquence d'injection ou un PRNG extérieur enregistré permet de comparer des
  conditions sous le même apport, indépendamment des événements internes.
- Bilan par matière/type : stock courant = stock initial + matière injectée −
  matière exportée, en plus des transformations internes conservatrices. Rapporter
  tentatives, entrées effectives, sorties, temps de séjour et flux incorporé.
- Les structures actuelles P/R sont préallouées, avec indices de partenaires
  fixes. L'entrée/sortie demande une évolution technique des tables/IDs ou une
  réserve inactive correctement masquée. Un plafond de capacité épuisé invalide
  un essai ; il ne doit pas passer pour une régulation des concentrations.

Avant cellule : domaine vide pour mesurer transport et bilan, convergence avec
dt et convention de bord, puis consommateur local contrôlé et vésicule avec
consommation réelle. Vérifier gradient, pénurie et arrêt/reprise préprogrammés,
sans annoncer une concentration garantie. Le temps de diffusion dépend aussi
de la distance bord–vésicule et peut dominer l'arrivée utile ; aucun délai de
renouvellement ne se déduit du seul débit CPU ou d'injection.

État actuel : J0–J3 utilisent encore un inventaire fini et des murs extérieurs
mécaniques, pas cette frontière source/puits. La demande est préservée pour
l'étape d'alimentation ouverte ; ne pas la remplacer silencieusement par un
chemostat à concentration fixée. Priorité immédiate : coupler les fonctions.
Le nom historique « open » des témoins J2/J3 signifie grand domaine sans L :
il contient encore des murs mécaniques et aucune source/sortie de particules.
