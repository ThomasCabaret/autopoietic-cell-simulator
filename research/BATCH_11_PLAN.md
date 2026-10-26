# Lot11 — contrôles longs et diagnostic des ouvertures

26 octobre2026. Lot de diagnostic/unification des critères, **aucune nouvelle loi**.
Le lot10 obtient l'insertion B3/3 à1500, mais fermeture≥0,8 seulement2/3 et28%
de périodes non classables dans B0. Sans barrière de lien, pertes2–4/24 : conserver
la barrière de B comme référence. Blocage concret avant l'intégration G/F : le
confinement et la refermeture ne sont pas établis dans toutes les répétitions.

## Campagne figée

Six essais `campaigns/membrane_robustness.json` : graines0/1/2 à1500, contacts
associatifs B taux0,2 contre taux0, tout le reste identique.219 dimères en anneau
préparé,24 libres dans l'anneau intérieur de livraison,24 sondes repoussées et24
transparentes, soit534 billes. Barrière de lien k80/rayon0,55, géométrie H–H1 /
T–T0,98 / H–T0,65, docking4/largeur0,3, off0,02, température0,08 ; paramètres
du lot10 conservés. La suppression de l'échange est une ablation, pas une preuve
de chimie commune. Les deux groupes ont les mêmes états initiaux par graine ;
leurs tirages ultérieurs divergent, car les réactions partagent le PRNG physique.

Échantillonnage inchangé toutes0,5 unités. Le diagnostic est séparé de la chimie,
appelé après l'observateur existant. Classer fermé, ouvert classable, fragmentation
du parent, grand écart terminal, aire faible, croisement et inconnu résiduel.
Rapporter fraction originale dans la plus grande composante, nombre de fragments
et d'extrémités, distances entre extrémités, épisodes d'ouverture et périodes
inconnues. **Une paire d'extrémités proches n'est pas un joint étanche.** Aucun
contour virtuel nouveau ni classification des sondes dans les périodes inconnues.

Durées d'état par maintien de l'échantillon précédent ; frontières des épisodes
censurées dans l'intervalle entre images. Plus longue durée observée = dernière
image moins première image de même état, borne échantillonnée. Proximité d'une
ouverture avec un échange dans1/5/25 unités : descriptive, pas preuve causale.
Le contrôle sans échange et l'exposition réelle doivent précéder cette conclusion.

## Contrôles, critères et décision

- Vérifier géométrie synthétique : un anneau coupé en deux arcs avec extrémités
  proches reste non classable ; un grand arc ne devient pas un contour fictif.
- Mesures dynamiques, PRNG et observations anciennes inchangés avec/sans audit.
- Reprise au milieu du calcul identique, incluant épisodes et durées ; passage
  dans le worker figé et conservation des recettes. Un pilote B0 à150 doit
  retrouver les positions et métriques de sa référence du lot9.
- Ancien criblage maintenu : fermé≥0,8 et fuite observée≤0,05, avec fraction
  classable explicitement rapportée. Une forte fraction inconnue empêche de
  conclure à une rétention globale ; ne pas améliorer le score par une mesure
  qui refermerait artificiellement les fragments.

Deux travailleurs, checkpoints60s, aucune trajectoire dense. Les B sont rejoués
pour obtenir les nouveaux diagnostics absents des anciennes trajectoires non
enregistrées ; comparer aussi leurs résultats anciens sans modifier les archives.
Les témoins sans échange ne sont pas attendus produire des insertions : ils
isolent la robustesse spontanée, pas un succès fonctionnel de cellule.

Après analyse : si fragmentation et défauts existaient sans échange, travailler
la tenue/fermeture des contacts ; si l'échange les aggrave, travailler le chemin
local de refermeture. Si le problème est surtout topologique/analytique, mesurer
directement les fuites pendant les périodes inconnues avant de modifier les lois.
Ne pas ajouter d'insertase ni prolonger indéfiniment sans diagnostic neuf.

Coût primitif : zéro type, état physique, port, paramètre chimique ou aide ajouté.
Coût logiciel : diagnostics/stockage d'agrégats analytiques et reprise. Membrane
toujours séparée de G/F ; budget cible C0B et dépendances L/import/déchets inchangés.
L'intégration matérielle reste l'étape suivante ; horizon de réévaluation : ces
six résultats, pas un catalogue de nouvelles variantes.
