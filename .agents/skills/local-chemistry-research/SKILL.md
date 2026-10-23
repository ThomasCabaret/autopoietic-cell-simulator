---
name: local-chemistry-research
description: Explore and unify local artificial chemistries for copying, vesicles and functional polymers in this project, tracking hypotheses, evidence, compatibility and primitive complexity.
---

# Recherche de chimies locales

Le problème et sa définition se construisent ensemble. Partir d'une cellule,
d'un polymère ou de sous-unités préparés est autorisé. La priorité est de trouver
des lois réutilisables dont les assemblages portent les fonctions.

## Libertés du modèle

- Billes localisées, mais exclusion et superposition peuvent dépendre des types
  et états locaux. Aucune obligation de réalisme moléculaire ou de solvant explicite.
- Liaisons locales avec géométrie, saturation, rupture et profils d'interaction
  modifiés par l'occupation des ports ou l'état de voisins directement liés.
- Helpers et source d'énergie externe permis ; les déclarer et mesurer leur rôle.
- Petit alphabet réutilisable. Une fonction ne doit pas nécessiter un nouveau
  type représentant la molécule entière.
- Aucun test dynamique de cellule, contour fermé, génome complet, longueur cible,
  séquence entière ou rôle parent/copie. L'analyse peut les reconnaître après coup.

## Travail expérimental

### Exploration, unification et simplification

Pour chaque lot, annoncer dans le plan s'il explore un mécanisme, intègre des
mécanismes ou simplifie les lois, et quelle incertitude il doit résoudre. Les
prototypes séparés sont autorisés ; consigner leur écart au candidat commun et
le prochain test de transfert. Dès que plusieurs mécanismes ont une preuve
isolée, donner priorité à leur intégration avant d'accumuler d'autres fonctions
isolées, sauf obstacle documenté justifiant une nouvelle exploration.

Définir le candidat par son alphabet élémentaire, ses états et ports, les motifs
locaux autorisés, leurs paramètres, et les helpers ou apports d'énergie. Figer ce
jeu de lois pendant une campagne de comparaison et l'identifier par configuration
résolue et empreintes des sources. Une modification ouvre une variante tracée.
Un même code avec des tables, constantes ou options chimiques différentes ne
prouve pas un univers commun. Distinguer les changements de lois des changements
de séquence, connectivité ou conditions initiales sous ces mêmes lois. Déclarer
les conditions externes ; un cycle fourni doit être fixé avant le calcul.

Maintenir dans les plans/bilans une suite de référence de comportements chimiques
avec recettes, conditions, critères et contrôles ; les tests logiciels ne la
remplacent pas. Pour modifier un candidat commun, réévaluer les acquis concernés
sous les nouvelles lois et indiquer réussite, régression ou non testé. Rejouer
une ancienne archive vérifie sa reproductibilité, pas sa compatibilité avec les
lois actuelles. Ne pas masquer une régression par un réglage propre à chaque
fonction ou un assouplissement silencieux des critères. Une révision légitime
d'un critère doit être motivée et son effet sur les comparaisons explicité.

Évaluer la convergence à trois niveaux : mécanismes dans des modèles séparés ;
mécanismes sous les mêmes lois mais testés séparément ; coexistence et couplage
dans un même bain. Pour le couplage, vérifier qu'un produit fabriqué par un
mécanisme est réellement utilisable par le suivant, sans conversion externe ni
changement des lois entre fabrication et usage. Par exemple : chaîne F exprimée
depuis G puis opération chimique répétée. Une cellule ou des outils préparés
restent des départs autorisés, à distinguer de leur fabrication et renouvellement.
Un moteur partagé ou l'addition de réussites séparées ne vaut pas preuve de
compatibilité ; consigner aussi les interférences et transferts qui échouent.

Pour chaque ajout significatif, noter dans la branche ou le bilan son coût :
types primitifs, états/ports, nombre de partenaires du motif, paramètres
indépendants, helpers et dépendances externes. Distinguer ces primitives des
espèces composées obtenues par assemblage. Justifier l'ajout par le mécanisme
qu'il débloque et rechercher sa réutilisation dans d'autres fonctions ; un helper
spécifique reste une dette explicite, pas une primitive générale déjà validée.
Tester les retraits ou remplacements plus simples pertinents, avec les acquis
précédents comme contrôles. Privilégier les fonctions nouvelles obtenues en
changeant les assemblages sous des lois fixes. La localité seule ne garantit ni
la simplicité ni l'expressivité.

À la clôture, les priorités doivent nommer le prochain test d'intégration ou de
simplification, et la maturité préciser le niveau de compatibilité effectivement
observé. Compter les fonctions transférables et combinables ainsi que les
régressions, sans déduire la convergence du seul nombre de démonstrateurs.

### Hypothèses, essais et preuves

Reprendre `research/branches.json` et `research/LOG.md` avant d'explorer. Ajouter
une branche liée à son parent : hypothèse, changement minimal, résultat attendu,
contre-exemple recherché et preuve qui manque. Conserver les échecs.

Tester en priorité les deux familles demandées : copie d'information binaire
dans des polymères de sous-unités composites ; courbure, association et fermeture
de sous-unités composites en vésicules 2D. Chercher les primitives communes.

La cible élargie comprend aussi la traduction directe vers un second alphabet
de polymères fonctionnels, leur organisation dépendante de la séquence, et la
fabrication depuis la nourriture des monomères, composants de membrane et outils
qui permettent de refaire ces mêmes outils. Garder ouverte l'alternative d'un
seul alphabet jouant information et fonction ; deux familles sont la piste de
travail privilégiée, pas une conclusion déjà démontrée.

Travailler aussi au niveau abstrait : comparer de petits réseaux de cellule
causalement fermés, tout en marquant chaque fonction hypothétique. Une fermeture
de graphe ou un bilan de matière ne prouvent pas sa réalisation moléculaire.
Maintenir `research/PRIORITIES.md` et `research/MATURITY.md` avec le registre.

Pour chaque expérience, enregistrer configuration, graine, version/hash du code,
conditions initiales, métriques, trajectoire échantillonnée et conclusion. Donner
des contrôles qui distinguent le mécanisme proposé d'un résultat imposé par
l'initialisation, une attraction générique ou un critère de mesure avantageux.

Faire évoluer les critères lorsque l'expérience le justifie, en expliquant ce
qui a changé. Éviter de déclarer une piste validée sur un seul réglage ou une
seule graine ; chercher un contrôle négatif et une perturbation pertinente.

Séparer explicitement : dessin construit, criblage statique, dynamique, copie
partielle, copie complète, libération, réutilisation, fermeture depuis un fragment
préparé et assemblage depuis des sous-unités libres. Ne pas transformer une
observation favorable en preuve d'autonomie ou de fermeture constructive.

Lorsqu'une branche échoue, identifier le mécanisme probable et tester une
modification ciblée ou ouvrir une autre piste. Lorsque deux cibles minimales
fonctionnent, documenter leurs limites et proposer le prochain test qui pourrait
les réfuter avant de passer à la cellule complète.

Mettre à jour le registre, les priorités et le journal après les essais. À chaque
fin de lot, rendre un bilan utilisateur très bref, indiquant la maturité globale,
le progrès démontré et le verrou principal. La maturité vise une chimie commune
assez expressive pour membrane, copie, traduction et reconstruction de ses outils,
pas seulement deux démonstrations isolées. Éviter un pourcentage de maturité sans
calibration. Les futures recherches repartent de ces preuves.
