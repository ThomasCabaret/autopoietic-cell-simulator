# Lot10 technique K1 — exposition cinétique et campagnes reprenables

26 octobre2026. Aucune nouvelle loi chimique. Hypothèse : une absence d'insertion
à150 peut résulter d'une faible exposition admissible ; augmenter uniquement le
temps CPU ne permet pas de choisir entre accès, taux et stabilité. Construire
une mesure sans rétroaction puis appliquer des horizons égaux à toutes les graines.

Plan `campaigns/membrane_kinetics.json` : B et B sans barrière de lien, paramètres
figés du lot9, graines0/1/2, horizon1500. Distinguer deux candidats : aucune
preuve de chimie commune ne résulte de leur utilisation du même moteur.

Critères descriptifs : première rencontre, première éligibilité de capture ou
d'échange, premier lien nouveau–ancien, premier contour incorporant un nouveau
dimère ; expositions par fenêtres25, échanges effectués et durées de persistance.
Rapporter fermé≥0,8 et fuite≤0,05 avec classabilité, sans changer les seuils du
lot9. Une réussite sur une seule graine n'est pas une robustesse3/3. Ne pas
interrompre une graine lente pour conserver seulement les bonnes.

Les expositions sont pré-réaction et approximatives, avec conflits locaux non
résolus dans le diagnostic. Elles ne constituent ni des essais indépendants ni
un taux exact. Les premiers passages sans événement sont censurés. Le budget de
calcul est six tâches sur deux processus, checkpoints60s, sans trajectoire dense.
Pas de réglage chimique automatique et pas de notification/scheduler externe.

Checks : aucune variation de trajectoire/PRNG avec diagnostic ; vraie géométrie
éligible ; reprise au milieu du calcul exacte avec expositions ; processus figé,
hash modifié refusé, recette source seule restaurée, pas de relance des terminés,
état interrompu distinct de processus actif, censure et regroupement des lois.

Décision après campagne : si l'exposition est quasi nulle, travailler l'accès
local ; si elle est suffisante sans échanges, examiner le taux/ordonnancement ;
si les produits apparaissent puis disparaissent, examiner la stabilité. Coupler
ensuite le candidat simplifié aux vrais constituants avant une insertase ou un
catalogue supplémentaire. I0 et T9 restent prioritaires. Optimisation CPU/GPU
différée jusqu'à un profil stabilisé ; aucun gain×10 revendiqué.
