# Lot31 — RV1, réversibilité locale et premier débouché des polymères

31 octobre2026. Exploration de W-02/W-03/H-06 : donner une réalisation testable
au cycle polymère→monomère→précurseurs→produit réutilisable, sans protéase ou
régulateur supplémentaire. La diversité I0/L reste un autre verrou ouvert.
Départ construit autorisé ; inventaires fermés ici, aucune homéostasie revendiquée.

## Candidat et budget de primitives

Option chimique explicite `bond_turnover`, absente par défaut. Rupture de liens
de squelette G–G/F–F avec deux taux selon familles chimiques élémentaires.
Rupture P–R seulement sur support sans voisin de squelette, sans appariement
et sans ligand capturé, avec deux autres taux G/F. Une protection locale peut
multiplier le taux de squelette lorsqu'un de ses deux supports est apparié ou
porte un ligand. Aucun nom de chaîne, séquence, longueur, contour ou score global.
Deux supports voisins et leurs occupations directes ; coût borné avec la chaîne.

Coût : quatre taux et un facteur de protection, zéro nouveau type, port, gène,
outil ou particule. Réutilise les liaisons/occupations existantes. Les positions,
vitesses et identités des atomes sont conservées. Changements d'énergie/affinité
non calibrés : helper cinétique de dissociation, pas un modèle thermodynamique
réversible équilibré. Le thermostat, l'activation et le cycle externe restent déclarés.

Le produit dissocié est un vrai P et un vrai R, donc peut redevenir nourriture
ou traverser la membrane via la loi libre/liée existante. Les catégories et
forces se mettent à jour depuis les liens. Aucune suppression de matière.

Risque aval décisif : détruire les derniers gènes/outils, piéger les fragments
ou créer un artefact d'observation. Garder les démos MD2 inchangées ; ne pas
promouvoir cette variante sans transfert et contrôle des régressions.

## Observation et vérifications avant campagne

Les anciens compteurs par ensemble d'IDs supposent des liens irréversibles :
ils ne certifient pas une naissance après recyclage. RV1 reçoit un recensement
passif dédié : états actuels G/F, distributions, ruptures/formations, matière
polymérisée réellement dissociée puis réassemblée/incorporée, bilans atomiques.
Aucun compteur ne dirige les lois. Pas de filiation ni de nouvelle enzyme
exprimée certifiée par ce seul recensement. Événements et sources conservés.

Contrôles : rupture G/F, protection par occupation seulement, dissociation des
monomères autorisée mais pas des squelettes/duplex occupés, vrai R relâché et
symbole retrouvé, changement de perméabilité, absence de suppression atomique,
pas de PRNG consommé à taux nuls, observateur passif, tree/brute et reprise
exacte. Comparaison sans option aux préfixes MD2 archivés ; réexaminer et
recertifier le catalogue, aucune chimie de démo retouchée.

## Exploration bornée, paramètres avant résultats

Phase A :12 essais, trois graines0/1/2 × quatre conditions, durée1200,
T0,08, Langevin m1/gamma0,1, dt0,002, réaction0,01, observation0,5.
Petit bain150 billes (G001 +36 G +36 F), quatre G001 et quatre F001 initiaux,
six F monomères001011, boîte12×9. Même matière et initialisation par paire.

1. `zero` : tous taux nuls (nouveau census, dynamique témoin inchangée).
2. `backbone` : squelette G0,00005/F0,001 ; P–R tous nuls ; protection1.
3. `full` : mêmes squelettes, P–R G0,001/F0,01 ; protection1.
4. `protected` : mêmes taux, protection0,05.

Ce sont témoins/ablations d'une famille, pas une grande grille d'optimisation.
Taux choisis pour rendre des pertes observables à1200, pas pour imposer un
stock cible. Ils ne lisent ni population ni succès. Les familles G/F désignent
leurs constituants chimiques, pas le rôle d'un agrégat.

Après la cohorte complète, porte prospective pour le seul `protected` :

- tous essais terminés et bilans valides ;
- ≥2/3 avec au moins une réassociation de précurseurs issus de matière polymérisée ;
- ≥2/3 avec réincorporation de cette matière dans un squelette ;
- chaque graine conserve au moins un G001 intact détaché à1200 ;
- médiane des formations catalysées ≥moitié de `zero`, médiane témoin >0.

Porte refusée : arrêt, conserver toutes les variantes pour interprétation.
Porte passée : quatre suivis MD2 intégrés (trois graines +dt/2 graine0,
intervalles réaction/mesure conservés), mêmes taux `protected`, horizon1200.
Anciennes références MD2 réutilisées ; aucun réglage silencieux des seuils.
Suivi sélectionné, pas validation indépendante ; aucune adoption automatique.
Budget16 tâches max, deux travailleurs,24h max ; pas de retry scientifique.
Sources et deux phases figées avant A ; statut/checkpoints et pause accessibles.

Critères de décision finaux : récupérer de la matière n'établit pas régulation
de population ni maintien des fonctions. Si les pertes empêchent le métabolisme,
diagnostiquer la protection et les fragments avant un nouveau balayage.
La synthèse L et l'export par bord restent non implémentés dans ce lot.
