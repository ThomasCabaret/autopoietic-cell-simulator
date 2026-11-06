# Checklist compacte — cellule construite maintenue

Révision 20 · revue 2026-11-06 · 43 sous-buts · CP1 dynamique : CC1/CH1 clos, association mais fermeture isolée refusée ; récupération intégrée sélectionnée ; EG1 visible

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
| Membrane et insertion | 5 | à fermer | 25–75% | M-05 | M-01 : CH1 isolés1800 : chaînes30/52/34 sans cycle final ; CE1 extrémités hors capture. Preuve historique séparée inchangée. ; M-04 : CH1 intégré1 récupère94,33% tardif, G2/F5/L22 ; suivi sélectionné, pas robustesse/insertion/renouvellement démontrés. |
| Apports et transport | 3 | à fermer | 0–75% | E-03 | — |
| Énergie et retour des cycles | 2 | à fermer | 25% | Q-01, Q-02 | Q-01 : Gradient compétitif et delta3rangs y compris naissance H/T cohérents ; températures correctes6/6 à300, pas thermodynamique globale. |
| Déchets et recyclage | 4 | à fermer | 0–25% | W-02, W-03, W-04 | — |
| Homéostasie des petites espèces | 2 | drafts décrits | 0% | — | — |
| Homéostasie des polymères | 4 | à fermer | 0% | H-03, H-04, H-05, H-06 | — |
| Compatibilité et maintien | 4 | à fermer | 0–25% | C-01, C-03, C-04 | C-02 : Température CH1 correcte4/4 et récupération intégrée sélectionnée ; aucune convergence dt ou validation générale CP1. |
| Calcul et observabilité | 2 | drafts décrits | 25–100% | — | O-01 : Premier coût15–16× refusé puis force1,81–1,85×, delta1,48/.97× sur snapshots sélectionnés, source/échec conservés. ; O-02 : Préfixes7 historiques/2compétitifs exacts,39 démos natives ; surveillance IO récupérée sans modifier les lois figées. |

**Trous conceptuels prioritaires au présent bilan :**

- M-01, M-04, Q-01, C-02 : Diagnostiquer courbure/flexibilité et rencontres/ruptures sous CP1 avant autre horizon ou constante.
- F-02, R-05, H-03, H-04, E-01, W-01 : Gaps diversité, information riche, protection/régulation et flux/export inchangés.

Voir [draft des outils](FUNCTIONAL_MECHANISMS.md) et [homéostasie des polymères](MACROMOLECULE_HOMEOSTASIS.md).

[Détails, critères, dépendances, preuves et prochain test](CELL_CHECKLIST.md) · [Méthode et évolution](CONCEPT_FIRST.md).

Un75% peut être un couplage limité avec outil préparé ; aucun maintien durable implicite. Le100% logiciel concerne les références actuelles et ne valide aucune fonction biologique.
Cible hors périmètre : origine spontanée de la cellule, division cellulaire, immortalité ou survie infinie garantie, vidéo et relecture avancée.

Généré par `python experiments/cell_readiness.py build` depuis `cell_checklist.json`.
