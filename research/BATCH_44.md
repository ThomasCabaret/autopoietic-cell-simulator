# Lot44 — BI1 refusé, diagnostic d'accès et compartiment compact

5 novembre2026. [Plan](BATCH_44_PLAN.md) · [recettes CB1](BATCH_44_RECIPES.json)
· [pilote](BATCH_44_PILOT.json). Intégration et calibration ; aucun nouvel outil.

**Clôture ultérieure : CB1 terminé9/9, transfert unique et fermeture fragile ; voir [lot45](BATCH_45.md).**
Les états en cours ci-dessous sont historiques.

## BI1 :9/9 terminés sans erreur, insertion non démontrée

Rapport figé local
`outputs/boundary_transfer_followups/followup_20261105T063330030027Z/report_0.json`,
SHA256 `3aec01041253e3671ba2784ae4294a96465c8fa4fea6bb72683fd794be20c04b`.
Trois critères passent (invariants, fermeture tardive, témoin sans synthèse),
un est refusé : aucune insertion de L réellement né dedans sur les trois actifs.

| À1200, graines0/1/2 | Active | Sans échange | Sans synthèse |
| --- | --- | --- | --- |
| L fabriqués |3 /2 /7|4 /6 /8|0 /0 /0|
| Nouveaux G / F libérés |0 /0 /0 pour chacun|0 /0 /0 pour chacun|0 /0 /0 pour chacun|
| Insertion, même simple contact nouveau/ancien |0 /0 /0|0 /0 /0|0 /0 /0|
| Fermeture classifiable900–1200 |.8383 /.8617 /.8567|.8600 /.8717 /.8633|.8683 /.8483 /.8850|
| Traversées liées échantillonnées |0 /0 /0|0 /0 /0|0 /0 /0|

Une proximité n'est pas un contact chimique. Les références MX2 demeurent
validées dans leur boîte12×9 ; elles ne se transfèrent pas automatiquement
dans ce montage90×90. L'échec utile est conservé, pas requalifié en succès
par une courbe de fermeture. Les périodes non classables et l'échantillonnage
interdisent de conclure à une étanchéité continue.

## Audit sans simulation et contrôle local

`experiments/audit_boundary_access.py` vérifie le rapport figé, lit les stocks
et calcule un contrôle statique de trois L ; sortie locale
`outputs/diagnostics/BI1_access_20261105T092417089177Z/report.json`.

Actifs : P_G30/24/23, P_F29/24/28, R0 30/27/29, R1 29/21/22, H/T21/22/17
encore non assemblés. Aucune pénurie globale, mais la dilution/localisation
peut empêcher leur accès aux outils. Derniers P/R10,29/1193,06/859,83 ;
derniers L1127,01/122,82/489,09. Pas de plateau général ni temps infini déduit.

Les temps de paires proches sont280,26/508,41/1836,29, mais les temps de faces
éligibles à l'échange seulement0/.34/.78. Au taux .2, exposition pondérée
totale≈.224. Ce recensement pré-tick n'est pas l'intégrale exacte du hazard :
rupture/formation/capture se succèdent dans le tick. Aucun modèle Poisson,
probabilité d'échec ou taux stationnaire n'est inféré de ces nombres.
Le test d'insertion a reçu trop peu d'occasions pour condamner sa possibilité.

Trois L construits : une paire liée i–j et un entrant k décalé normalement du
site de j. À distance .5, q≈.5004 est admissible à l'échange .8², sans chevauchement
du core .4 ; le modèle n'interdit donc pas cette pose géométrique. L'énergie et
la force de docking libre sont pourtant0 le long des cinq poses étudiées :
les faces occupées ne captent pas l'entrant. C'est un motif local construit,
pas une insertion dynamique obtenue. Une attraction associative est une piste
future explicite ; aucun helper ni protéine d'insertion n'est ajouté dans ce lot.

## Avancement : CB1, un bain dimensionné pour les outils courts

Une frontière219 L avait été dimensionnée historiquement pour des outils plus
longs que les G01/F01 réellement utilisés ici. CB1 compare52 L construits,
rayon8, boîte22×22 et paquet12×9 centré : **302 billes**,198 sans L. La courbure
est choisie analytiquement, short_length=.92 contre.98 dans BI1 :
1−2*.65*sin(pi/52)≈.9215. C'est un paramètre chimique différent explicitement
déclaré, pas une comparaison de seules conditions initiales sous constantes
identiques. Tous les autres taux, capture, helpers, thermostat et pas sont fixés.

La concentration globale est16,74 fois supérieure à BI1 à stock identique,
encore4,48 fois inférieure à MX2 ; aire interne nominale≈201 contre≈3739.
Le mode de diffusion libre idéal sur22 vaut≈61,3, pas un temps mesuré des
agrégats. Les frontières n'imposent aucune concentration intérieure : P/R
libres et H/T peuvent toujours diffuser au-dehors. Le témoin noL rend possible
un diagnostic du débit génétique indépendamment de la présence de L ; tableau
de vitesses de taille différente, donc PRNG non apparié après initialisation.

Implémentation : le constructeur accepte explicitement zéro L pour ce témoin,
sans contour fictif ni barrière intérieure. Les observateurs savent laisser
la frontière absente inconnue. Mêmes moteur, ports et partenaires atomiques.
Coût : zéro type/port/gène/outil/loi chimique ; une option d'initialisation vide
et une adaptation de collecte. La variante .92 doit refaire ses preuves.

Pilote CB1P100,48,016s : **5 L**, aucun invariant violé,97,5% du temps échantillonné
fermé, zéro passage lié observé, T finale .07496, déplacement max .00773.
Six points invalides :9/12,5/15,5/32/34/100 ; le dernier point reste ouvert.
Le garde BI1 réutilisé refusait ce dernier point. Après inspection, le garde
CB1 prend la fraction temporelle>=.8 au lieu d'exiger une fermeture instantanée
finale. Cette adaptation post-pilote est tracée ; aucun recalcul ou allongement
pour obtenir un dernier point favorable. Critères de cohorte inchangés.

**CB1 lancé9 essais à2400**, active/noL/nosynthesis×3, deux travailleurs,
checkpoints30s/budget4h, rapport puis arrêt, aucune seconde phase ou grille.
Porte : invariants, fermeture tardive, insertion vraie dans>=2 actifs, G/F
préservés à moitié des médianes noL strictement positives, témoin sans synthèse
négatif. Lecture des stocks/occasions/fuites obligatoire quelle que soit la porte.
Statut `compact_transfer_status.bat` ; pause `stop_compact_transfer.bat`, reprise
explicite `resume_compact_transfer.bat`. Pas de promotion anticipée de CB1.

## Démos et documentation réalignées

Trois variantes MX2 validées ajoutées à **Démos → Chimie mixte · outils et lipides**,
graines0/1/2, recettes coopératives exactes à2400,198 billes, Langevin inchangé.
MIN1M reste le raccourci « État actuel · bain intégré » avec membrane préparée ;
MX2 n'en contient aucune. Les deux scènes répondent à des questions distinctes.
BI1 n'est pas présenté comme un succès ; CB1 reste en campagne.

L'adaptateur graphique distingue les vrais supports G/F et H/T du bain mixte ;
il ne les confond plus avec des sondes de membrane. Compteurs passifs ajoutés :
L fabriqués et part via F entièrement reconstruits. Flashes/suivi exploitent les
vraies liaisons, sans intervention sur la physique.30 choix au catalogue ;
guide actualisé avec les acquis et les échecs récents, historiques conservés.

M-04 est recalibré75→25 dans le registre actuel : l'ancien75 décrivait des L
**préparés** insérés dans MD2, alors que le critère exige depuis longtemps de
vrais L fabriqués. Le résultat historique reste valide et référencé ; sa portée
ne prouve pas le transfert visé. Ce changement corrige le classement de preuve,
pas une nouvelle exigence ni la disparition d'une observation MD2.

## Santé et prochain jalon

Validation :235 tests logiciels passent (`outputs/batch44_tests.log`),14 contrôles
de registre/conception après mise à jour, sept préfixes archivés identiques à5
(dont MX2 et BI1P). Les30 choix du menu natif Qt/OpenGL ont été ouverts ; MX2
est inclus dans lecture/pause/recommencement et comparaison des positions au
moteur sans interface, aucune erreur. Ces contrôles logiciels ne valident pas
la cohorte CB1 en cours.

L'incertitude a diminué (exposition et dilution identifiées), mais le transfert
cellulaire n'a pas progressé expérimentalement dans BI1. La prochaine décision
est CB1 complet : si la génétique reste faible sans L, revoir le transport et
le dimensionnement ; si l'accès membranaire est rare malgré un bain productif,
tester un mécanisme associatif local avant tout ajout d'enzyme. Deux changements
conceptuels sans transfert ni diagnostic nouveau imposent une refonte, pas une
grille de taux. Régulation/protection, information riche, flux et énergie restent
ouverts : aucun maintien, délai fiable ou absence de futur blocage garanti.
