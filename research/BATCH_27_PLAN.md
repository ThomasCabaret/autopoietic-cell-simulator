# Lot27 — T9E : recapture locale des extrémités F

Lot d'exploration mécanistique suivi d'un transfert conditionnel, pas adoption.
MD2/Langevin est la référence actuelle, démos GUI3 inchangées. Le diagnostic
du lot18 établit que retirer seulement monomer_only_capture ne permet pas de
recapturer F : un second garde impose degré(F)=0. MD2 laisse des F2 et beaucoup
de F monomères, sans F3 nouveau ; la pénurie globale n'explique pas ce résultat.

## Hypothèse et coût

T9E autorise un contact G/F sur un F d'au plus un voisin de squelette, donc
une extrémité ou un monomère. G doit toujours avoir un voisin. Le XOR monomère
ne s'applique plus à ces seuls contacts G/F ; G/G et tous les autres gardes
(symbole, orientation, saturation, précurseurs, coopération), taux et forces
restent fixes. Aucun accès à la longueur, séquence entière, parent, outil ou
produit. Rayon de reconnaissance0,3 et degrés des deux supports directement
liés : voisinage borné. Un choix discret opt-in, zéro type/port/état physique,
paramètre continu, particule, gène ou outil ajouté. Les F internes ne recapturent
pas : cette variante n'est pas une polymérase processive.

Fonction aval menacée : F complet peut aussi se fixer par ses extrémités et
perdre son activité. Le contrôle d'outil préparé est obligatoire. Réutilisation
espérée : finition aux bouts de chaînes de longueur variable ; non démontrée.
Si échec, conserver diagnostic, instrumentation et référence MD2 ; ne pas
empiler un garde de longueur ou une exception par séquence.

## Arbre borné, figé avant résultats

Phase A :12 essais à1200, deux travailleurs : ancien/T9E × trois graines0/1/2
× deux préparations. Chimie génétique MD2, température0,08 et Langevin m1/gamma0,1,
dt0,002, réaction0,01, observation0,5 ; petite boîte8×6, G001,24 G et24 F
disponibles, précurseurs constructibles, six F composites initiaux. Préparation
expression : six monomères001011 ; contrôle outil : F001 lié + monomères011.
Même inventaire initial, seule connectivité/préparation diffère entre contrôles.
Ces petites boîtes concentrées sont des mécanismes séparés sous les lois
génétiques communes, pas un modèle de cellule ni la preuve d'un transfert.

Audit passif des contacts par degré F, éligibilité, ligation, occupation des
sites F préparés et produits catalysés/incorporés. Comptages pré-réaction,
exposition approximative ; causes de rejet séquentielles, pas hazards exacts.
Pas de trajectoire complète. Données/checkpoints locaux, sources/recettes figées.

Porte prospective descriptive, uniquement après12 réussites techniques :

- expression : nouveau F libéré dans au moins2/3 T9E et médiane strictement
  supérieure à l'ancien ; médiane G libéré au moins celle de l'ancien ;
- contrôle outil : médiane des composants catalysés incorporés T9E au moins
  moitié de l'ancienne médiane, celle-ci strictement positive ; chaque T9E
  passe au plus50% du temps-site préparé F en appariement G/F ;
- les métriques requises doivent exister ; erreur, pause ou interruption
  arrêtent l'automate sans relance implicite.

Porte franchie : phase B4 essais seulement, grands bains MD2 graines0/1/2
et dt/2 graine0, même horizon1200, matière/conditions inchangées. Anciennes
références MD2 déjà terminées explicitement réutilisées, jamais refaites pour
gonfler les effectifs. Le contrôle fin conserve intervalles réaction/mesure.
Audit génétique aussi présent pour distinguer accès, gardes et ligation.
La membrane n'est pas modifiée ; mesurer maintien, G/F et produits réellement
incorporés. La convergence n'est pas prouvée par une seule graine fine.

Porte refusée : rapport de tous les essais et raisons, arrêt pour interprétation.
Pas de descente supplémentaire, nouvelle protéine ou balayage de taux implicite.
Phase B sélectionnée par A : exploration conditionnelle, pas validation indépendante.
Budget maximal16 essais, aucune duplication/retry automatique. Deux changements
conceptuels sans transfert ni réduction d'incertitude imposent réexamen du modèle.
Plafond24 heures écoulées depuis le premier lancement, attente incluse : demande
de pause avec checkpoint, arrêt du suivi, inspection explicite avant toute suite.

## Contrôles et restitution

Avant lancement : contacts idéaux monomère/F2/F3, conservation des autres
gardes et G/G, passivité RNG/positions, reprise des compteurs, porte acceptée
et refusée par tests, anciens scénarios inchangés avec option absente.
L'automate s'arrête après B pour décision scientifique. Vérifier fin de cohorte
et signatures avant analyse. Mettre à jour arbre, priorités, santé/maturité ;
ne pas présenter la préparation d'une campagne comme un succès chimique.

MD3 (loupe d'insertion) reste tracé mais différé : limiter la charge à deux
travailleurs et interpréter le verrou de renouvellement avant un autre changement.

## Amendement technique après lancement, critères scientifiques inchangés

Premier job T9E_20261030T163413128888Z : refus Windows de remplacement atomique
du statut de task0000 pendant une lecture concurrente, WinError5 (dernier statut t81).
Arrêt explicite, un échec technique et deux tâches partiellement calculées
puis mises en pause, zéro tâche complète. Toutes conservées avec checkpoints.
Le contrôleur historique continuait les tâches A après un échec ; le nouveau
suivi lui demande maintenant STOP en cas d'attention, sans lancer B.

Correction générique de `campaign_io.write` : sept tentatives maximum du seul
rename atomique sous Windows, attente totale0,63s, puis erreur persistante
propagée. Aucun pas de simulation ou essai réexécuté par cette transaction.
Tests conflit transitoire/persistant et deux nouveaux pilotes techniques.
Nouvelle cohorte explicitement préparée sous T9E_20261030T164244840888Z ; lois,
préparations, graines, horizons et porte inchangés. Pas de modification des
archives ni de sélection selon rendement. Budget scientifique16 maximum,
plus les3 tentatives techniques incomplètes précédentes, déclarées hors cohorte.
