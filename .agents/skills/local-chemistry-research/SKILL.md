---
name: local-chemistry-research
description: Explore local artificial chemistries for composite molecular template copying and vesicles in this project, preserving a branching record of hypotheses, runs, failures and evidence.
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
