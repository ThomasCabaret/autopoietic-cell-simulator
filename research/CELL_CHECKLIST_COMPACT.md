# Checklist compacte — cellule construite maintenue

Révision 19 · revue 2026-11-05 · 43 sous-buts · EG1 limité ; CF1 pausé pour frustration des ports additifs ; CP1 statique concurrent et FS1 fonction/séquence

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
| Membrane et insertion | 5 | à fermer | 25–75% | M-05 | M-04 : CF1 perd la frontière dans deux préfixes ; preuve75 reste limitée à EG1 historique, pas de robustesse nouvelle. |
| Apports et transport | 3 | à fermer | 0–75% | E-03 | — |
| Énergie et retour des cycles | 2 | à fermer | 25% | Q-01, Q-02 | Q-01 : EL1 localise les commutations ; CF1 révèle la frustration, CP1 statique propose une loi à capacité bornée. |
| Déchets et recyclage | 4 | à fermer | 0–25% | W-02, W-03, W-04 | — |
| Homéostasie des petites espèces | 2 | drafts décrits | 0% | — | — |
| Homéostasie des polymères | 4 | à fermer | 0% | H-03, H-04, H-05, H-06 | H-06 : FS1 distingue disparition de F001 et activité F01 persistante ; pas de maintien acquis. |
| Compatibilité et maintien | 4 | à fermer | 0–25% | C-01, C-03, C-04 | — |
| Calcul et observabilité | 2 | drafts décrits | 25–100% | — | O-01 : Pause justifiée par millions de refus et coût ; aucune grille de taux supplémentaire. ; O-02 : Anciens préfixes exacts,39 démos recertifiées ; nouveaux résultats/provenances et checklist actualisés. |

**Trous conceptuels prioritaires au présent bilan :**

- F-01, F-02, S-04 : Fermer la famille de mécanismes pour des fonctions distinctes et la construction L.
- W-02, W-03, H-03, H-04, H-06 : Fermer régulation, recyclage/export et protection des polymères avant de supposer le maintien possible.

Voir [draft des outils](FUNCTIONAL_MECHANISMS.md) et [homéostasie des polymères](MACROMOLECULE_HOMEOSTASIS.md).

[Détails, critères, dépendances, preuves et prochain test](CELL_CHECKLIST.md) · [Méthode et évolution](CONCEPT_FIRST.md).

Un75% peut être un couplage limité avec outil préparé ; aucun maintien durable implicite. Le100% logiciel concerne les références actuelles et ne valide aucune fonction biologique.
Cible hors périmètre : origine spontanée de la cellule, division cellulaire, immortalité ou survie infinie garantie, vidéo et relecture avancée.

Généré par `python experiments/cell_readiness.py build` depuis `cell_checklist.json`.
