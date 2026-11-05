# Lot49 — le filtre révèle une attraction libre non saturable

5 novembre2026. [Plan et pivot](BATCH_49_PLAN.md), [preuves compactes](BATCH_49_RESULTS.json).
La progression est un diagnostic structurel et un prototype statique vérifié,
pas une nouvelle cellule fonctionnelle. Aucun outil/gène supplémentaire.

## EL1 clos et interprété

Clone et préfixes observés exacts. Sur2100–2200,1110 updates ajoutent565,8112
de potentiel net : ports560,7266, barrière5,08455. Les5 échanges filtrés retirent
7,07554. Parmi les updates :493 formations seules,+2629,0309 ;534 ruptures seules,
−2088,4552 ;83 mixtes. La nourriture H/T devenue L chauffe avant les L initiaux.
Ce bilan de potentiel commuté n'est pas un bilan total de chaleur ni une preuve
que chaque fraction de chauffe vient de ce seul mécanisme.

## CF1 construit, puis arrêté pour interprétation

Le delta de ports existant accepte désormais un ajout ou retrait de contact,
avec sa barrière P/R locale. Une formation/rupture lit deux L/quatre billes,
leurs faces et interactions incidentes à coupure existante ; un échange trois L.
Même facteur thermique, température et taux de tentative ; une option
contact_update_gate, aucun nouveau nombre/type/port/état/gène/outil. Pas de
thermodynamique globale : taux on/off et domaines géométriques non symétrisés,
helpers P/R et forcing externe conservés. Défaut none reste historique.

Contrôles : delta local égal au potentiel complet, signe inverse, refus montant
àT0 et rupture descendante, liaison possible entre L libres àT>0 ; barrière
obligatoire, passivité et reprise exactes. Le premier oracle de test ne gérait
pas le tableau de segments vide : forme(0,2) corrigée, pas de loi changée.
Sept préfixes historiques restent exacts ; comparer cela à la compatibilité,
pas à une adoption des nouvelles lois dans ces références.

Pilote100 fin/s2 passe : fermeture89,75%,T75–100=.08421,4 L produits ; formation
298 propositions/118 acceptations, rupture118/118. Cohorte6 à2400 lancée
automatiquement après provenance/gates du pilote, deux travailleurs et3h.

**Pause scientifique anticipée, non prévue dans l'arbre automatique initial.**
Deux préfixes à1345 et2033,5, quatre essais non démarrés ; aucun essai complet,
aucune porte de cohorte calculée. Environ4 millions de propositions par préfixe
pour quelques centaines de formations acceptées ; seulement1/0 contacts latéraux
restent pour75 L, contours non valides. Le coût et la perte de structure justifient
de ne pas consommer le reste du budget. Checkpoints/sources/échecs conservés.
Il ne faut pas reprendre CF1 sans décision nouvelle ni appeler les préfixes une
cohorte terminée. Le pilote binaire/court était insuffisant pour ce mécanisme.

Le filtre expose une incohérence de représentation : une face libre accumule les
puits attractifs de plusieurs partenaires, alors que sa liaison les exclut tous
sauf un. Former une liaison supprime donc plusieurs attractions et coûte cher.
Le modèle peut condenser en agrégat de L libres et rendre leur liaison très
défavorable. Changer le taux ou réchauffer ne résout pas cette incompatibilité.

## CP1 : alternative compétitive, statique seulement

Pour chaque interaction de ports libre e=(i,j), noter u_e le potentiel historique
tronqué, A sa profondeur au contact, p_e=−u_e/A, et S_i la somme des p autour
du port i. Le prototype décrit :

```text
D_e = 1 + S_i + S_j − 2 p_e
E_libre = somme_e u_e / D_e
```

Un port ne peut recevoir plus d'une unité d'affinité : D_e>=S_i implique
Σ_incident p_e/D_e<=1. Pour une paire isolée D_e=1 : potentiel et force historiques
exacts. Aucun nombre ajustable nouveau ; la valence1 est celle du port existant.
Le gradient inclut les dérivées des dénominateurs, pas seulement une pondération
des forces de paires. Normalisation par voisinages finis, aucun appariement
optimal global ou identité d'agrégat. Une réaction future devra inclure les
partitions affectées des voisins, jusqu'à deux rangs pour les termes d’énergie modifiés ; leurs partitions
non pré-calculées peuvent requérir le troisième rang. La portée effective
reste bornée indépendamment du nombre de L, mais ce surcoût de voisinage est réel.

Le code `experiments/competitive_port_potential.py` **n'est pas branché dans
le moteur**. Tests : conservation du cas binaire, dérivées finies de toutes les
coordonnées en motif peuplé, force résultante nulle, capacité<=1 et exclusions
des ports occupés/partenaires. Le coût dynamique et la simplicité du delta local
restent à vérifier. Réutilisation pour d'autres sites espérée, pas établie.

Comparaison statique sélectionnée :12 formations admissibles de moindre mismatch
sur chacun des deux checkpoints CF1 pausés, mêmes contacts pour les deux modèles.
Le terme lié et la barrière sont identiques ; seul le potentiel libre est changé.

| Snapshot | Contacts admissibles | Delta additif médian | Delta compétitif médian | Delta compétitif<=0 |
| --- | --- | --- | --- | --- |
| s0 | 206 | 209,09 | −1,925 | 12/12 sélectionnés |
| s1 | 131 | 99,09 | −1,697 | 11/12 sélectionnés |

Charges maximales de ports.728/.713. Cela étaye le mécanisme du blocage dans
ces poses ; ce n'est ni une distribution globale, ni une cinétique, ni une preuve
d'auto-assemblage ou d'insertion. Recette/source du premier sondage conservées,
données détaillées locales, résumé compact. Prochaine étape : delta local exact
et intégration au moteur commun, petit test de coût/assemblage avant nouvelle
cohorte longue. Ne pas empiler une autre constante si cette famille échoue.

## RP1 et FS1 : séquence cible perdue, catalyse pas entièrement éteinte

RP1 terminé3/3 refuse sa porte : G0014/3/6,F0011/0/0 ; réassemblages13/2/6,
réincorporations3/0/1, invariants0. Aucun transfert. La condition nommée
functional_present comptait en fait la séquence cible F001, un proxy conservateur.
Le refus initial et les recettes ne sont pas réécrits.

FS1 lit les checkpoints avec leur chargeur archivé, sans évolution. Il reste
8/1/1 liens F0–F1 non appariés et42/31/18 formations catalysées entre900 et1200.
La graine1 ne contient aucun F001 dans toute cette fenêtre. Perte de F001 ne
signifie donc pas disparition de toute activité de co-recrutement. Les motifs
peuvent se recouvrir, être fragments et générer des cycles futiles : ni protéines
entières renouvelées, ni préservation d'information, ni homéostasie démontrées.
Au dernier instant, aucun double recrutement géométriquement admissible ou
liaison protégée cohérente n'est présent ; cet instant ne décrit pas les durées.

Conséquence conceptuelle : suivre séparément séquences génétiques, pool fonctionnel
par motifs/activité, et flux matériel utile. Ne pas ajouter une protection d'outil
sur la seule absence d'un ancien proxy ; le candidat cellulaire emploie déjà F01.
La checklist garde les gaps de protection/régulation et le refus RP1, sans les
transformer en impossibilité de maintien. CONCEPT_FIRST et calibration actualisés.

## Validation, GUI et maturité

262 tests du premier passage passent, puis3 tests statiques CP1 ; le passage
final réussit **265 tests** (`outputs/batch49_tests_final.log`).39 démos natives
vérifiées, mêmes recettes et limites EG1/EN1. Ni CF1 ni CP1 promus dans la GUI.
Un contrôle ciblé supplémentaire confirme qu'un timeout du pilote demande
la pause des travailleurs et ne lance pas la cohorte, sans retry caché.
Registre19,43 IDs stables ; aucun palier biologique augmenté. M-04 garde75
uniquement pour le domaine EG1 historique, C-02/Q-01 restent25, maintien0.

Le risque contact libre/lié est désormais explicite et possède une alternative
mathématique locale testée statiquement. Son efficacité en dynamique reste inconnue.
Diversité, information, protection/régulation et alimentation/export restent des
risques majeurs. Aucun blocage de principe établi, pas de calendrier garanti.
**Aucun calcul ne tourne à la clôture : CF1 en pause, EL1/RP1/FS1/CP1 terminés.**
