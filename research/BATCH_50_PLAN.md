# Lot50 — intégrer CP1 et vérifier sa dynamique avant nouvelle cohorte longue

6 novembre2026. Intégration et test discriminant, sans nouveau gène/outil.
Registre19/43 relu : Q-01/C-02 et M-01/M-04 bloquent le transfert ; les gaps
de diversité, information, protection/régulation et flux restent ouverts.
CF1 reste pausé, aucune reprise ou suppression de ses données.

## Changement figé

Intégrer le potentiel compétitif CP1 dans les forces L, le delta des contacts
(formation/rupture/échange) et celui de naissance H/T. Une naissance peut modifier
les partitions des ports voisins : ne pas additionner seulement la nouvelle paire.
Option free_port_potential=competitive, défaut additive bit-compatible. Aucun
nouveau nombre ajustable/type/port/gène/outil ; un choix de famille de potentiel.
Coût : partitions locales et portée effective jusqu'à trois rangs de contacts.
Le delta lit un patch spatial de trois rangs, pas une énergie globale ni un contour.
Ces rangs sont bornés indépendamment du nombre de particules/longueur de chaînes.

Préconditions : force/gradient et binaire CP1 ; delta exact contre potentiel
complet pour ajout/retrait/échange/naissance, cas de concurrence et bords de patch ;
particules éloignées sans effet ; passivité/reprise ; références historiques.
Mesurer après compilation force et delta sur snapshots CF1 : coût médian<=5×
la référence additive au même état, sans en déduire vitesse cellulaire globale.
Si coût excessif, optimiser l'implémentation à lois identiques avant campagne.

## Test d'assemblage depuis molécules isolées et panel court

Ajouter une initialisation explicite de dimères H/T indépendants dans le stock
existant. Aucun lien latéral initial, pas de contour ou de chaîne préparée ;
positions/orientations générées avant simulation et archivées. Cette facilité
d'initialisation ne crée pas de loi dynamique ou de reconnaissance d'agrégat.

CC1 panel6 :3 bains intégrés à300 (3 graines EG1, même matériel), et3 sous-bains
sans outils/P/R contenant52 L isolés à300. Mêmes lois et paramètres L que le bain
intégré ; helper barrière P/R non exercé quand P/R absent. Distinguer ce sous-bain
du couplage et ne pas appeler une association une vésicule. Nouveaux lipides du
bain intégré restent de vrais produits H/T, pas les dimères préparés du contrôle.

Critères préannoncés : invariants0 ; intégré fermeture150–300>=.8 et T225–300<=.12
chaque graine ; contrôle isolé au moins4 L dans un composant lié et des contacts
nouveaux dans chaque graine, T225–300<=.12. Rapporter cycles fermés, distributions
des tailles, propositions/refus, stocks et derniers événements. Pas de gate
G/F à300 avant calibration de leurs cycles. Pas de maintien ou succès d'insertion
tardive déduit de ces critères courts.

Deux travailleurs, budget1h/checkpoints30s, recettes figées, rapport puis arrêt.
Pas de réglage, retry ou cohorte longue automatique : le premier comportement
dynamique de cette famille requiert interprétation mécaniste, même si la porte
courte passe. Ne pas promouvoir de GUI avant résultats. Si le potentiel empêche
l'assemblage ou reste trop coûteux, reconsidérer la famille plutôt qu'un taux.

Fonctions aval menacées : croissance/réparation depuis L fabriqués et coexistence
avec génétique. Si échec, kernel/delta/localité et initialisation restent réutilisables.
Portée non testée : membrane depuis précurseurs intégralement renouvelés, tous
gènes, pertes, apport/export et homéostasie. Aucun nouveau palier anticipé.
