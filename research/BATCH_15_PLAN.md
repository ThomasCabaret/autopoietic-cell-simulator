# Lot15 J2 — contrôler le domaine avant de changer la chimie

27 octobre2026. Lot d'intégration/diagnostic. J1 est terminé12/12 ; fabrication
à froid et transfert dans la petite boîte, aucun transfert dans les6 grands bains.
Les fragments F déliés non cibles sont absents des bains : T9 n'est pas encore
le diagnostic de ce verrou. Hypothèse principale : séparation spatiale/dilution.
Alternative : contacts/retention sélective et fragilité de L dégradent le transfert.

## Contraste figé

À partir des scénarios membranaires J1 conservés, retirer L à l'initialisation,
sans changer les lois P/R, le cycle200/15, température0,08, mobilité0,25 ou stocks.
Garder la même initialisation des P/R, y compris le PRNG hérité. Comparer monde
90×90 et monde8×6 : ce dernier est **le domaine entier sans membrane**, avec
les mêmes murs mécaniques100 que le moteur utilise déjà. Pas de mur interne
dans une cellule, pas de force liée à une identité génétique.

`world_box` est un réglage d'environnement à deux longueurs, réservé à L absent.
Par défautNone, le hook conserve exactement la dynamique J1 (test positions,
chimie et PRNG contre le hook archivé). Son ajout ne change aucune réaction.
Le compact translate simplement paquet et origine ; rungs, bits et PRNG initiaux
sont identiques aux grands mondes et aux bains J1 correspondants.

Quatre conditions open/compact × préparé/délié, graines0/1/2, horizon1200 fixé
avant résultats, deux travailleurs, checkpoints60s et audit génétique.12 essais
à102 billes. Contrôles initiaux des6 paires avant gel. Les résultats J1 originaux
restent associés à leurs propres sources ; aucune recette n'est remplacée.

Critères : flux catalysé **incorporé**, nouveaux G/F et actes de F exprimés,
occasions de ligation, stocks libres/assemblés et fragments. Déclarer les
régressions et censures ; pas de sélection d'une graine productive. Si open
échoue et compact fonctionne, le grand domaine suffit à expliquer un échec
sans L ; cela n'exclut pas un autre effet de L. Si open fonctionne et les bains
échouent, la frontière/transport devient plus directement suspecte. Ces témoins
ne sont pas un contrôle inerte parfait : L change aussi l'espace accessible.

Horizon de décision : cette cohorte, puis choix de concentration/organisation
ou diagnostic de frontière, avant un nouveau helper. Le prochain test devra
conserver les acquis sous mêmes lois et ne pas optimiser le stock global par
un compteur pilotant la chimie. Voir HOMEOSTASIS.md pour les obligations aval.

Coût physique : zéro élément, liaison, état, outil/gène ou taux ajouté ; un
réglage explicite de frontière externe pour le contrôle. Budget cellulaire C0B
inchangé. Les forces/réactions restent dans le moteur partagé, aucun scheduler
nouveau. Le census est un post-traitement, pas un mécanisme de régulation.
