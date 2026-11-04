# Lot42 — étalonner l’interprétation et corriger la capture croisée

4 novembre2026. Lot de diagnostic puis intégration/simplification. Registre43
sous-buts revu : C-01 bloque le débit commun avant S-04/insertion ; maintien,
protection/recyclage et homéostasie restent ouverts. Pas de nouvelle protéine.

## Preuves préalables et question de calibration

MX1 clos12/12, porte refusée pour G/F, les six autres conditions passent.
Audit sans nouveau calcul : stocks élémentaires reconstitués depuis IDs/événements
et vérifiés contre les vrais liens finaux. Mixed finit avec P_G28/16/22,
P_F20/12/24, R0 26/14/24, R1 22/14/22 ; H/T15/4/16 chacun. Pas de pénurie
globale de ces réactifs ; cela ne prouve pas leur disponibilité locale.
Les témoins uncaptured épuisent presque leurs P/R. Le dernier quart produit
encore PR5/9/3 et L6/6/4 :1200 ne mesure pas un plateau ou une impossibilité.
Les doubles motifs sont croisés sur99,6/98,1/99,1% de leur temps échantillonné.

Loupe passive sélectionnée : premier motif croisé, graine0, t5,15 ; six billes,
fenêtre20,401 images maximum500 ; contrôle physique/PRNG exact jusqu’à40.
Deux déliaisons observées, aucune recapture dans le même tick ; les mêmes atomes
sont néanmoins vus recapturés au plus tard0,28 et0,72 après. Ne pas transformer
ces deux exemples en fréquence générale. Le problème qualitatif est compatible
avec affinités indépendantes laissant persister deux ligands incompatibles.

## Changement minimal à tester

Option `capture_cooperativity` dans mixed_synthesis, fausse par défaut.
Un site F directement lié à un autre site déjà occupé ne recrute/attire que
des ligands compatibles avec celui-ci : P–R ou H–T. Le premier site conserve
ses affinités larges. Aucun nettoyage piloté, seuil de concentration, lecture
de gène/protéine ou choix de produit global. Motif borné à deux sites composites
liés et deux ligands (six billes) ; même table matérielle que la formation.

Coût : une nouvelle condition locale de coopération, zéro type/gène/outil,
port, taux ou constante numérique indépendante. Cette aide chimique n’est pas
gratuite : elle modifie les commutations d’affinité et leur potentiel. Employer
la même condition pour forces et capture ; delta H/T inclut les changements
d’affinité des voisins directement liés aux sites libérés. P/R garde son helper
historique ; pas de fermeture thermodynamique revendiquée. Ce n’est pas un
nouvel outil fonctionnel supplémentaire, mais une variante des lois communes.

Contrôles rapides construits : premier ligand large, voisin compatible admis,
croisé refusé ; force équilibrée/gradient, libération rouvrant les affinités,
delta exact avec un troisième site voisin, passivité/reprise/arbre-brute,
défaut historique et sources archivées inchangés. Aucun bonus cinétique modifié.

Pilote candidat graine0 à100, question technique et présence de production,
pas validation. Une seule option proposée, pas de grille. Si incohérence
mécanique ou invariants violés, corriger le code avant campagne, pas la chimie.

## MX2 : horizon et comparaison figés avant calcul

12 essais au plus : reference / cooperative / nogene / noHT, graines0/1/2,
**t2400**, mêmes stocks et boîte que MX1. Reference reprend les lois MX1 ;
les trois autres ont coopération. Deux travailleurs, checkpoints30s, plafond4h,
analyse puis arrêt quelle que soit la porte. Aucun retry, deuxième phase ou
promotion automatique. Les références longues sont des suivis sélectionnés
des graines MX1 ; pas des répétitions indépendantes ou une révision de sa porte.

Pourquoi doubler : douze cycles externes au lieu de six, production toujours
active dans le dernier quart MX1. Les fenêtres1200 et2400 distinguent retard,
épuisement et effet de loi ;2400 n’est pas une garantie d’asymptote. L’ancien
criblage1200 reste refusé. Même horizon pour comparer reference et cooperative.
Les stocks ne sont pas accrus : les bains mixed en conservaient beaucoup.
NoHT est un contrôle séparé, vitesse/PRNG non appariés au bain198 billes.

Porte prospective :

1. Cooperative : G et F médians≥moitié noHT au même horizon ; G médian>reference.
2. Dans≥2 mêmes graines cooperative : au moins un F entièrement alimentaire
   actif,≥4 L catalysés et un L neuf ayant un contact latéral ultérieur.
3. F entièrement alimentaires→L sur≥2 graines ; nogene aucun nouveau F ni
   attribution à un outil exprimé ; noHT aucun L catalysé ; invariants valides.
4. Temps échantillonné de doubles motifs croisés nul dans cooperative.

Rapporter aussi stocks typed, derniers quarts, thermique, coût mural, portée
de diffusion idéale versus rencontres effectives. La porte ne teste pas une
cellule avec membrane ou l’homéostasie. Si encore échec avec stocks abondants
et motifs corrigés, interpréter géométrie/exposition ; ne pas lancer une grille.
Si succès, retour au transfert membranaire et à la boucle de maintien définie
par l’utilisateur, sans promettre que le renouvellement sous pertes est acquis.
