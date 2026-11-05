# Lot47 — insertion stabilisée et diagnostic du turnover protégé

5 novembre2026. [Plan](BATCH_47_PLAN.md), [preuves compactes](BATCH_47_RESULTS.json),
[checklist](CELL_CHECKLIST_COMPACT.md). Aucun changement des lois chimiques.

## EG1 complet : la porte limitée passe

| Graine | G / F / L nouveaux | L nés dedans insérés | Fermeture tardive | T tardive | Échanges acceptés / refusés |
| --- | --- | --- | --- | --- | --- |
| 0 | 9 /7 /23 | 1 | 94,48 % | .08492 | 6 /16 |
| 1 | 2 /9 /23 | 0 | 94,67 % | .08255 | 1 /7 |
| 2 | 8 /9 /24 | 2 | 94,50 % | .08893 | 10 /15 |

Invariants0 et toutes les conditions préannoncées satisfaites. Ce résultat réduit
le défaut thermique observé dans CW1 sans supprimer toute insertion. Aucun
tirage apparié après divergence ni preuve que le filtre explique seul chaque
différence de débit. Le gate refuse les hausses de potentiel avec ses mêmes
potentiels/température ; pas de nouveau thermostat, taux ou outil.

Les trois bains conservent des outils initiaux et des stocks finis. Aucun L
fabriqué par F entièrement alimentaire n'est inséré dans cette cohorte : le
transfert complet unique de CB1 n'est pas reproduit ici. Fermeture échantillonnée
94–95 % n'est pas étanchéité continue ; zéro traversée liée observée ne comble
pas les périodes non classables. Pas de perturbation, alimentation/export,
renouvellement ou homéostasie démontrés.

M-04 passe sous-cas25→couplage75 **pour l'insertion de L réellement fabriqués
dans un bain productif avec tenue tardive et deux graines positives**, pas pour
la réparation M-05 ou le maintien C-04. La preuve historique CB1 et les échecs
restent visibles. Aucun autre palier biologique augmenté.

## GUI : résultat actuel reproductible

**Démos → Intégration compacte · échanges stabilisés** propose les trois EG1
exacts,302 billes, mêmes états initiaux et lois que les essais. Le raccourci
« État actuel · bain intégré » ouvre la graine0 par convention, sans sélectionner
la meilleure trajectoire. Première insertion classée vers1108 dans cette graine.
La graine1 sans insertion reste incluse ; CB1 est conservé sous « défauts connus ».
36 choix au total, tous sous leurs conditions déclarées ; les anciennes références
browniennes restent distinctes. Les compteurs passifs montrent propositions,
acceptations et refus du filtre local. Aucun résultat précalculé ou feedback.

## RX1 complet : le blocage précède surtout la dissociation P–R

Deux rejeux sélectionnés de RV1 graine0, full/protected, horizon1200, sous leurs
sources archivées. Le wrapper observe chaque appel de turnover sans modifier
son ordre ou ses tirages. La rupture P–R est mesurée après les véritables ruptures
de squelette du même appel : pas une approximation fondée sur le seul degré
avant réaction. Les occupations qui se recouvrent restent aussi disponibles.
Labels « déjà polymérisé » limités à l'observation et alimentés par le journal.

Les deux états finaux, vitesses, chimie, RNG et résumés d'observateur sont
**exacts par rapport aux archives**. Passivité et reprise contrôlées sur microcas.
Fenêtres50, tableaux d'expositions/intensités, checkpoints ; aucun film de
positions. Ensemble local≈2,82 Mo, dont sources de sonde et checkpoints.

| Mesure, F déjà polymérisés | full | protected |
| --- | --- | --- |
| Part du temps encore lié au squelette | 73,65 % | 94,28 % |
| Temps éligible à dissociation P–R | 3741,53 sites·temps | 640,81 sites·temps |
| Intensité conditionnelle correspondante | 37,4153 | 6,4081 |
| Ruptures P–R sur supports déjà polymérisés, G et F réunis | 39 | 8 |
| Réassemblages avec deux atomes recyclés | 13 | 0 |
| Réincorporations de ces composites | 3 | 0 |

Le blocage par capture directe d'un F isolé déjà polymérisé ne représente que
2,07 et0,16 sites·temps respectivement. Ce n'est donc pas le goulot principal
de ces deux trajectoires. Les populations labellisées et leurs histoires
diffèrent : les fractions ne sont pas un effet causal apparié par molécule.
Intensités cumulées ne signifient ni indépendance des événements ni taux
stationnaires. Les pertes de squelette passent de15 à3 événements ; cela
concorde avec une forte protection des liaisons occupées, sans attribuer tout
l'échec de réemploi à cette seule cause.

**Décision :** ne pas régler les captures et ne pas transférer protected refusé
vers EG1. Une piste locale à comparer ultérieurement serait de protéger une
liaison par un appariement cohérent de ses deux extrémités sur une liaison
voisine, plutôt que par n'importe quelle occupation à une extrémité. Motif
borné de quatre composites/huit billes, aucun nom de gène, longueur ou fonction.
Cela pourrait conserver un duplex en cours de copie tout en exposant des outils
portant seulement des substrats. Ce n'est pas une loi ajoutée : elle pourrait
aussi détruire trop vite les outils actifs ou protéger des fragments appariés.
Protection, partage par espèce et information restent des gaps, sans nouvelle
protéine gratuite. L'alternative débit limité/pertes/export reste à fermer.

## EN1 lancé : vérifier la sensibilité au pas mécanique

Trois nouvelles graines sélectionnées, mêmes recettes EG1, dt divisé par deux
et nombres de pas entre réactions/observations doublés. Donc mêmes cadences
physiques et mêmes lois, positions/vitesses/RNG initiaux exacts ; trajectoires
ensuite différentes. Porte inchangée de stabilité/insertion/débit, références
EG1 réutilisées. Deux travailleurs,3h, checkpoints30s, rapport puis arrêt.
Voir BATCH_47_EN1_RECIPES.json et `exchange_refinement_status.bat`.
Pas de conclusion anticipée ou preuve de convergence à partir de trois graines.

## Validation et maturité

249 tests du passage complet passent ; quatre contrôles ciblés passent ensuite,
dont deux nouveaux pour EN1 (initialisation/cadences et refus des cas thermiques
ou sans insertion). Un lancement ciblé dans le sandbox Windows a échoué à créer
son temporaire ; relance autorisée réussie, pas défaut chimique. La GUI native
Qt/OpenGL valide les36 choix, lecture/pause/recommencement et positions égales
au moteur sans interface, y compris EG1. Registre et vues régénérés.

Un obstacle d'intégration réduit, un goulot de recyclage localisé. Aucune preuve
de maintien global ; les risques de diversité des fonctions, information riche,
protection/régulation et alimentation/export restent majeurs. Prochain jalon :
EN1 complet et conception d'un compromis local de protection ; pas une grille
de taux ni une cellule complète présentée comme prête.
