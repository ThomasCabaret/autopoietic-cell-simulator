# Checklist compacte — cellule construite maintenue

Révision 13 · revue 2026-11-05 · 43 sous-buts · MIN1M visible ; MX2 clos12/12 portes passées ; BI1 vrais L vers frontière en campagne9 essais

**Pourcentages = paliers de preuve**, pas effort accompli ni probabilité de réussite. Les plages indiquent min–max des sous-buts ; aucune moyenne globale.
0% non observé ·25% sous-cas ·50% séparé ·75% couplage partiel ·100% critère satisfait sur son domaine.
Concept : « à fermer » signale au moins un maillon essentiel manquant ; un draft décrit reste hypothétique.

| Domaine | Points | Concept | Preuve min–max | Trous conceptuels | Progrès du dernier lot |
| --- | ---: | --- | ---: | --- | --- |
| Lois et fonctions des outils | 3 | à fermer | 0–75% | F-01, F-02 | — |
| Fabrication N / A | 3 | à fermer | 25–75% | S-03 | — |
| Fabrication des lipides | 1 | à fermer | 25% | S-04 | S-04 : L24/23/23, F alimentaires→L2/3 sous chimie commune ; BI1P1 L né dedans, pas insertion encore. |
| Copie et information | 5 | à fermer | 0–75% | R-02, R-04, R-05 | — |
| Traduction et outils renouvelés | 5 | à fermer | 0–75% | T-02, T-04 | — |
| Membrane et insertion | 5 | à fermer | 25–75% | M-04, M-05 | M-04 : Frontière construite219 L reliée au même bain (636 billes), observateur adsorption/insertion et BI1 neuf essais lancés. Aucun nouveau palier anticipé. |
| Apports et transport | 3 | à fermer | 0–75% | E-03 | — |
| Énergie et retour des cycles | 2 | à fermer | 25% | Q-01, Q-02 | — |
| Déchets et recyclage | 4 | à fermer | 0–25% | W-02, W-03, W-04 | — |
| Homéostasie des petites espèces | 2 | drafts décrits | 0% | — | — |
| Homéostasie des polymères | 4 | à fermer | 0% | H-03, H-04, H-05, H-06 | — |
| Compatibilité et maintien | 4 | à fermer | 0–25% | C-01, C-03, C-04 | C-01 : MX2 clos12/12 : neuf critères passent, médianes G13/F14 contre4/7 référence ; contribution des remplaçants non uniformément meilleure. ; C-02 : Stocks quasi épuisés dans MX2 ; nouveau diagnostic distingue dilution globale et paquet local, occasions pré-tick et naissance au même instant. |
| Calcul et observabilité | 2 | drafts décrits | 25–100% | — | O-02 : 232 tests passent ; six préfixes physiques archivés exacts àt5, dont BI1P. Démo validée conservée, nouveau candidat non promu. |

**Trous conceptuels prioritaires au présent bilan :**

- F-01, F-02, S-04 : Fermer la famille de mécanismes pour des fonctions distinctes et la construction L.
- W-02, W-03, H-03, H-04, H-06 : Fermer régulation, recyclage/export et protection des polymères avant de supposer le maintien possible.

Voir [draft des outils](FUNCTIONAL_MECHANISMS.md) et [homéostasie des polymères](MACROMOLECULE_HOMEOSTASIS.md).

[Détails, critères, dépendances, preuves et prochain test](CELL_CHECKLIST.md) · [Méthode et évolution](CONCEPT_FIRST.md).

Un75% peut être un couplage limité avec outil préparé ; aucun maintien durable implicite. Le100% logiciel concerne les références actuelles et ne valide aucune fonction biologique.
Cible hors périmètre : origine spontanée de la cellule, division cellulaire, immortalité ou survie infinie garantie, vidéo et relecture avancée.

Généré par `python experiments/cell_readiness.py build` depuis `cell_checklist.json`.
