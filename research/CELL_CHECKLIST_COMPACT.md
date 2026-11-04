# Checklist compacte — cellule construite maintenue

Révision 5 · revue 2026-11-04 · 43 sous-buts · MD2 / Langevin inchangé ; MIN1R visible dans la GUI ; transfert membranaire MIN1M en cours

**Pourcentages = paliers de preuve**, pas effort accompli ni probabilité de réussite. Les plages indiquent min–max des sous-buts ; aucune moyenne globale.
0% non observé ·25% sous-cas ·50% séparé ·75% couplage partiel ·100% critère satisfait sur son domaine.
Concept : « à fermer » signale au moins un maillon essentiel manquant ; un draft décrit reste hypothétique.

| Domaine | Points | Concept | Preuve min–max | Trous conceptuels | Progrès du dernier lot |
| --- | ---: | --- | ---: | --- | --- |
| Lois et fonctions des outils | 3 | à fermer | 0–75% | F-01, F-02 | — |
| Fabrication N / A | 3 | à fermer | 25–75% | S-03 | — |
| Fabrication des lipides | 1 | à fermer | 0% | S-04 | — |
| Copie et information | 5 | à fermer | 0–75% | R-02, R-04, R-05 | — |
| Traduction et outils renouvelés | 5 | à fermer | 0–75% | T-02, T-04 | T-05 : MIN1M : transfert avec membrane en campagne,12 essais figés ; palier50 inchangé. |
| Membrane et insertion | 5 | à fermer | 25–75% | M-04, M-05 | — |
| Apports et transport | 3 | à fermer | 0–75% | E-03 | — |
| Énergie et retour des cycles | 2 | à fermer | 25% | Q-01, Q-02 | — |
| Déchets et recyclage | 4 | à fermer | 0–25% | W-02, W-03, W-04 | — |
| Homéostasie des petites espèces | 2 | drafts décrits | 0% | — | — |
| Homéostasie des polymères | 4 | à fermer | 0% | H-03, H-04, H-05, H-06 | — |
| Compatibilité et maintien | 4 | à fermer | 0–25% | C-01, C-03, C-04 | C-01 : Même petit outil dans2118 billes MD2, contrôles noL/split/nogene ; aucune preuve anticipée. |
| Calcul et observabilité | 2 | drafts décrits | 25–100% | — | O-02 : Trois démos MIN1R exactes ajoutées ; compteurs de F entièrement refaits et actifs,24 choix. |

**Trous conceptuels prioritaires au présent bilan :**

- F-01, F-02, S-04 : Fermer la famille de mécanismes pour des fonctions distinctes et la construction L.
- W-02, W-03, H-03, H-04, H-06 : Fermer régulation, recyclage/export et protection des polymères avant de supposer le maintien possible.

Voir [draft des outils](FUNCTIONAL_MECHANISMS.md) et [homéostasie des polymères](MACROMOLECULE_HOMEOSTASIS.md).

[Détails, critères, dépendances, preuves et prochain test](CELL_CHECKLIST.md) · [Méthode et évolution](CONCEPT_FIRST.md).

Un75% peut être un couplage limité avec outil préparé ; aucun maintien durable implicite. Le100% logiciel concerne les références actuelles et ne valide aucune fonction biologique.
Cible hors périmètre : origine spontanée de la cellule, division cellulaire, immortalité ou survie infinie garantie, vidéo et relecture avancée.

Généré par `python experiments/cell_readiness.py build` depuis `cell_checklist.json`.
