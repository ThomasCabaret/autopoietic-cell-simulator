# Checklist compacte — cellule construite maintenue

Révision 31 · revue 2026-11-07 · 43 sous-buts · CP1 avec référence CPU et mécanique CUDA résidente vérifiée sur un préfixe

**Pourcentages = paliers de preuve**, pas effort accompli ni probabilité de réussite. Les plages indiquent min–max des sous-buts ; aucune moyenne globale.
0% non observé ·25% sous-cas ·50% séparé ·75% couplage partiel ·100% critère satisfait sur son domaine.
Concept : « à fermer » signale au moins un maillon essentiel manquant ; un draft décrit reste hypothétique.

| Domaine | Points | Concept | Preuve min–max | Trous conceptuels | Progrès du dernier lot |
| --- | ---: | --- | ---: | --- | --- |
| Lois et fonctions des outils | 3 | à fermer | 0–75% | F-01, F-02 | — |
| Fabrication N / A | 3 | à fermer | 25–75% | S-03 | — |
| Fabrication des lipides | 1 | à fermer | 25% | S-04 | — |
| Copie et information | 5 | à fermer | 0–75% | R-02, R-04, R-05 | — |
| Traduction et outils renouvelés | 5 | à fermer | 0–75% | T-02, T-04 | — |
| Membrane et insertion | 5 | à fermer | 25–75% | M-05 | — |
| Apports et transport | 3 | à fermer | 25–75% | E-03 | — |
| Énergie et retour des cycles | 2 | à fermer | 25% | Q-01, Q-02 | — |
| Déchets et recyclage | 4 | à fermer | 0–25% | W-02, W-03, W-04 | — |
| Homéostasie des petites espèces | 2 | drafts décrits | 0% | — | — |
| Homéostasie des polymères | 4 | à fermer | 0% | H-03, H-04, H-05, H-06 | — |
| Compatibilité et maintien | 4 | à fermer | 0–25% | C-01, C-03, C-04 | — |
| Calcul et observabilité | 2 | drafts décrits | 25–100% | — | O-01 : Mécanique CP1 résidente intégrée, reprise exacte sur naissance contrôlée et goulot réactionnel localisé. |

**Trous conceptuels prioritaires au présent bilan :**

- E-01, W-01, W-02, T-05, H-06, M-05 : Fermer représentation/flux/bilan L puis maintien équipé ; ne pas confondre récupération depuis zéro outil et renouvellement.
- F-02, R-05, T-04, H-04 : Dé-risquer expressivité et information : symétrie PG/PF dans le canal actuel, finition et coexistence encore ouvertes.

Voir [draft des outils](FUNCTIONAL_MECHANISMS.md) et [homéostasie des polymères](MACROMOLECULE_HOMEOSTASIS.md).

[Détails, critères, dépendances, preuves et prochain test](CELL_CHECKLIST.md) · [Méthode et évolution](CONCEPT_FIRST.md).

Un75% peut être un couplage limité avec outil préparé ; aucun maintien durable implicite. Le100% logiciel concerne les références actuelles et ne valide aucune fonction biologique.
Cible hors périmètre : origine spontanée de la cellule, division cellulaire, immortalité ou survie infinie garantie, vidéo et relecture avancée.

Généré par `python experiments/cell_readiness.py build` depuis `cell_checklist.json`.
