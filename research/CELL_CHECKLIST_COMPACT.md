# Checklist compacte — cellule construite maintenue

Révision 25 · revue 2026-11-06 · 43 sous-buts · CP1 inchangé, CR1 réussi ; PT1/RF1 complets refusés, diagnostics FA1 ; récupération FR1 en cours séparément

**Pourcentages = paliers de preuve**, pas effort accompli ni probabilité de réussite. Les plages indiquent min–max des sous-buts ; aucune moyenne globale.
0% non observé ·25% sous-cas ·50% séparé ·75% couplage partiel ·100% critère satisfait sur son domaine.
Concept : « à fermer » signale au moins un maillon essentiel manquant ; un draft décrit reste hypothétique.

| Domaine | Points | Concept | Preuve min–max | Trous conceptuels | Progrès du dernier lot |
| --- | ---: | --- | ---: | --- | --- |
| Lois et fonctions des outils | 3 | à fermer | 0–75% | F-01, F-02 | — |
| Fabrication N / A | 3 | à fermer | 25–75% | S-03 | — |
| Fabrication des lipides | 1 | à fermer | 25% | S-04 | — |
| Copie et information | 5 | à fermer | 0–75% | R-02, R-04, R-05 | — |
| Traduction et outils renouvelés | 5 | à fermer | 0–75% | T-02, T-04 | T-05 : Scénarios/audit/portes de récupération construits ;6 essais600,2 travailleurs/1h. Aucune preuve anticipée. |
| Membrane et insertion | 5 | à fermer | 25–75% | M-05 | M-03 : PT1 terminé6/6 : rétention encourageante, porte refusée car ouverture finale réelle dans une graine (51 liens/52 L). |
| Apports et transport | 3 | à fermer | 0–75% | E-03 | — |
| Énergie et retour des cycles | 2 | à fermer | 25% | Q-01, Q-02 | — |
| Déchets et recyclage | 4 | à fermer | 0–25% | W-02, W-03, W-04 | W-02 : RF1 terminé9/9 : pas de réincorporation stricte, deux protections refusées ; pas adoption dans CP1. |
| Homéostasie des petites espèces | 2 | drafts décrits | 0% | — | — |
| Homéostasie des polymères | 4 | à fermer | 0% | H-03, H-04, H-05, H-06 | H-06 : FA1 localise perte à96.99 sans retour ; récupération en27.23 observée ailleurs. FR1 lancé pour tester la survie des monomères. |
| Compatibilité et maintien | 4 | à fermer | 0–25% | C-01, C-03, C-04 | — |
| Calcul et observabilité | 2 | drafts décrits | 25–100% | — | — |

**Trous conceptuels prioritaires au présent bilan :**

- H-06, H-03, W-02, T-05 : Interpréter FR1 par exposition, reconstruction et activité avant nouveau taux ou transfert des pertes.
- M-03, M-05, F-02, R-05, H-04, E-01, W-01 : Maintenir ouverts transport/réparation et verrous conceptuels de diversité, information, régulation et flux.

Voir [draft des outils](FUNCTIONAL_MECHANISMS.md) et [homéostasie des polymères](MACROMOLECULE_HOMEOSTASIS.md).

[Détails, critères, dépendances, preuves et prochain test](CELL_CHECKLIST.md) · [Méthode et évolution](CONCEPT_FIRST.md).

Un75% peut être un couplage limité avec outil préparé ; aucun maintien durable implicite. Le100% logiciel concerne les références actuelles et ne valide aucune fonction biologique.
Cible hors périmètre : origine spontanée de la cellule, division cellulaire, immortalité ou survie infinie garantie, vidéo et relecture avancée.

Généré par `python experiments/cell_readiness.py build` depuis `cell_checklist.json`.
