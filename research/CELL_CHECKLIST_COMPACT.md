# Checklist compacte — cellule construite maintenue

Révision 17 · revue 2026-11-05 · 43 sous-buts · EG1 insertion/tenue limitée confirmées, GUI36 ; RX1 recyclage diagnostiqué ; EN1 dt/2 en cours

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
| Membrane et insertion | 5 | à fermer | 25–75% | M-05 | M-04 : 25→75 : L fabriqués insérés2/3 avec tenue tardive/température3/3, domaine EG1 limité. |
| Apports et transport | 3 | à fermer | 0–75% | E-03 | — |
| Énergie et retour des cycles | 2 | à fermer | 25% | Q-01, Q-02 | — |
| Déchets et recyclage | 4 | à fermer | 0–25% | W-02, W-03, W-04 | W-02 : RX1 exact : F déjà polymérisés liés74%/94% du temps full/protected ; accès aux pertes localisé, preuve reste25. |
| Homéostasie des petites espèces | 2 | drafts décrits | 0% | — | — |
| Homéostasie des polymères | 4 | à fermer | 0% | H-03, H-04, H-05, H-06 | H-06 : Goulot de protection clarifié ; alternative locale décrite, gap/proof0 conservés. |
| Compatibilité et maintien | 4 | à fermer | 0–25% | C-01, C-03, C-04 | C-02 : EN1 dt/2 lancé, cadence physique chimie/observation fixe ; pas de résultat anticipé. |
| Calcul et observabilité | 2 | drafts décrits | 25–100% | — | O-02 : GUI36 choix,3 EG1 exacts, compteurs passifs d’échange, CB1 conservé. |

**Trous conceptuels prioritaires au présent bilan :**

- F-01, F-02, S-04 : Fermer la famille de mécanismes pour des fonctions distinctes et la construction L.
- W-02, W-03, H-03, H-04, H-06 : Fermer régulation, recyclage/export et protection des polymères avant de supposer le maintien possible.

Voir [draft des outils](FUNCTIONAL_MECHANISMS.md) et [homéostasie des polymères](MACROMOLECULE_HOMEOSTASIS.md).

[Détails, critères, dépendances, preuves et prochain test](CELL_CHECKLIST.md) · [Méthode et évolution](CONCEPT_FIRST.md).

Un75% peut être un couplage limité avec outil préparé ; aucun maintien durable implicite. Le100% logiciel concerne les références actuelles et ne valide aucune fonction biologique.
Cible hors périmètre : origine spontanée de la cellule, division cellulaire, immortalité ou survie infinie garantie, vidéo et relecture avancée.

Généré par `python experiments/cell_readiness.py build` depuis `cell_checklist.json`.
