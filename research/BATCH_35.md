# Lot35 — transfert membranaire en cours et démonstration du progrès acquis

4 novembre2026. [Plan figé](BATCH_35_PLAN.md) · [recettes](BATCH_35_RECIPES.json).

MIN1R revérifié :9/9 terminés, zéro erreur, aucun travail ancien actif. Aucun
essai ancien relancé. Le progrès antérieur est désormais proposé dans la GUI :
**Démos → Catalyseurs reconstruits · progrès récent**, graines0/1/2, mêmes
scénarios/sources physiques que les expériences MIN1R validées.150 billes,
reconstruction complète10/10/10 F, activité ultérieure5/2/1. Aucun changement
de lois pour rendre le comportement plus visible. Départ t0, pas de trace rejouée.

Deux compteurs passifs affichent F entièrement refaits depuis nourriture et
ceux actifs après libération. Ils utilisent uniquement les preuves existantes :
chaînes complètes déjà certifiées libérées, vrais supports produits, naissances
avant activité. L'outil préparé est exclu, un F partiellement préparé aussi.
Le catalogue conserve la démo membranaire MD2 recommandée et les références
historiques ;24 choix, dont trois MIN1R ajoutés. MIN1M n'est pas encore promu.

## Prochaine incertitude testée

MIN1M :12 essais t1200, deux travailleurs, mêmes lois MD2,2118 billes avec L,
1632 sans L.16 G01 et16 F01 préparés ;128 composites initiaux, contre144 dans
le MD2 historique. Les stocks de supports restent432 G/384 F ; symboles
G0/G1 =216/216 contre224/208 historiquement, F0/F1 =192/192 inchangés. Le coût est un
changement d'architecture initiale, sans type/port/loi/taux/outil supplémentaire.
Split/nogene modifient seulement les liens. NoL conserve placements/types P/R,
mais le tableau de vitesses Langevin plus petit change le PRNG après préparation.
L'égalité de placements ne doit pas devenir une affirmation de trajectoires appariées.

Pilote technique graine0 à t2 : terminé sans erreur en4,77s de calcul (2118
billes,1000pas), huit composants catalysés, aucun nouveau F à ce court horizon.
Ce préfixe n'est ni la cinétique moyenne future, ni une validation de transfert.
Budget figé :12 tâches, checkpoints30s,24h maximum avant pause ; analyse et
crible automatiques puis arrêt quelle que soit la décision. Pas de grille de taux.

Au lancement :0/12 achevé, deux tâches actives, aucune erreur. Les temps/ETA
évoluent ; état vivant par **membrane_renewal_status.bat**, pause par
**stop_membrane_renewal.bat**, reprise explicite par **resume_membrane_renewal.bat**.
Après fin : `python scripts/membrane_renewal_followup.py review`.

## Maturité et prochaine décision

La reconstruction d'un outil entier puis actif est prouvée dans le petit bain
commun P/R ; son transfert avec L est en cours, pas encore acquis. L'enzyme
initiale reste présente. Aucun maintien sous pertes, synthèse L, homéostasie,
information riche ou répertoire de protéines distinctes n'est démontré.
La prochaine intervention lit le rapport complet et interprète le témoin noL :
si le transfert échoue, diagnostiquer accès local/dilution/interférences plutôt
que multiplier les réglages. Si réussi, la construction matérielle H/T→L
et sa vraie insertion devient prioritaire selon LIPID_CONSTRUCTION_DRAFT.md.

## Vérifications

Les24 actions du menu Qt/OpenGL ouvrent les bons états initiaux, en pause ;
lecture/pause/recommencement passent pour la nouvelle démo aussi. Les images
de la GUI ont été inspectées. Les positions affichées restent égales au moteur
headless au même pas. Les compteurs sur les trois checkpoints MIN1R finaux
retrouvent exactement10/10/10 F alimentaires et5/2/1 actifs. Test synthétique
négatif : matière partiellement préparée ou activité antérieure à sa construction
exclues, aucun état modifié par la lecture. Aucun fichier simulator modifié.

29 tests distincts passent : catalogue/recensement7, renouvellement initial3,
MIN1M3, registre8, architecture6 et porte RV1 existante2 (recouvrements entre
les deux invocations dédupliqués). Le critère MIN1M exige les deux
réussites dans les mêmes graines et le contrôleur s'arrête après la cohorte
même si le crible passe. Registre et vues générées vérifiés.
