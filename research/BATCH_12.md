# Lot12 — échange sous condition locale de disponibilité

27 octobre2026. [Plan](BATCH_12_PLAN.md), [décisions et limites](BATCH_12_DECISIONS.md).
Les contrôles du lot11 sont analysés. Une trace des motifs à six billes sélectionnés
retrouve le préfixe ancien à800 et montre une différence d'occupation de port.
Le filtre géométrique est rejeté puisqu'il rejetterait aussi le cas productif.

G1 interdit la substitution si les autres ports du partenaire sortant et de
l'arrivant sont tous deux occupés ; même prédicat en sens inverse. Aucune règle
de contour, de molécule entière ou de réparation. Le taux0,2, la géométrie et les
forces de B ne changent pas. Un mode logique et une condition ajoutés, pas de
nouveau type/rayon/taux. Aide non thermique antérieure toujours déclarée.

67 tests logiciels et7 historiques passent. Le mode désactivé retrouve exactement
l'ancienne fonction et ses tirages ; le garde actif conserve remplacement local,
retour, valence, positions et reprise. Le diagnostic compte les expositions avant
et après garde sans changer les trajectoires. Les critères restent inchangés.

Le pilote sélectionné graine2 à150 n'a aucune insertion/échange malgré7,08 temps-
face sous garde. Ce résultat est conservé ; aucune efficacité n'est proclamée.
Trois répétitions jusqu'à1500, fixées avant calcul, sont nécessaires pour choisir.
Les six témoins M1R restent les comparaisons, sans les recalculer inutilement.

La recette du traceur conserve le code physique exact et le premier driver ;
le replay standard reconstruit les observations physiques, et le traceur courant
recalcule les géométries depuis les sources M1R versionnées. La recette du pilote
et celle de la campagne conservent aussi leurs sources exactes. Aucun résultat
brut ni checkpoint dans Git, aucune archive ancienne modifiée.

Maturité : une nouvelle hypothèse locale testable, pas un gain chimique acquis.
La voie B reste la référence d'insertion isolée ; G1 doit prouver qu'il conserve
cette fonction tout en évitant les défauts. Confinement réel, aliments/déchets,
production L et noyau G/F commun toujours ouverts. Aucun blocage de principe
établi ; réexaminer le mécanisme si cette intervention n'apporte aucun transfert
ni diagnostic nouveau, plutôt qu'ajouter des règles spécifiques successives.
