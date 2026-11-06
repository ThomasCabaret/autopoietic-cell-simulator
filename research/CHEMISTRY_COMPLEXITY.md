# Complexité de la chimie — inventaire sémantique v1

Revue 2026-11-06 · candidat CP1 intégré (CH1), lois physiques inchangées par CR1.

**Diagnostic : alphabet petit, spécialisation déjà substantielle.** La localité est mieux
établie que la simplicité universelle ou la richesse fonctionnelle. Les chiffres suivants
sont une convention de description vérifiable, pas une entropie de Shannon, un nombre de
degrés de liberté indépendants ou une preuve de minimalité.

| Élément compté | Bain intégré CP1 | Isolé CR1 |
|---|---:|---:|
| Types élémentaires résolus | 6 | 2 |
| Dimères chimiques possibles | 5 | 1 |
| Familles de liaison/contact structurel | 6 | 2 |
| Rôles de ports | 6 | 2 |
| Formules de force/potentiel intrinsèques | 8 | 4 |
| Schémas de transition dirigés | 10 | 3 |

**20 conditions sémantiques nommées** :4 d’occupation/valence,4 structurelles et12
orientées vers une fonction. Elles sont partagées entre les schémas, pas additionnées une
fois par appel ou par combinaison de symboles. Leur découpage est explicite ci-dessous.

**27 entrées numériques configurées actives +28 contrôles numériques fixes recensés**,
plus3 contrôles d’environnement (période, fenêtre de relâchement, raideur des parois).
Deux entrées peuvent avoir la même valeur ; cela ne fait pas deux paramètres indépendants.
Les zéros d’interaction sont comptés dans la matrice de compatibilité, les epsilon numériques
et identifiants/index ne sont pas des paramètres chimiques. Les constantes dérivées ne sont
pas recomptées : raideur de capture, offset/raideur des ports, dénominateurs compétitifs.
Le registre des28 contrôles fixes est une première revue sémantique, pas une extraction
exhaustive de tous les littéraux Python.

## Ce que ces chiffres rendent visible

- Les six types sont PG, PF, R0, R1, H et T. On peut factoriser P/R/H/T avec
  un attribut G/F sur P et un symbole0/1 sur R ; les six combinaisons chimiques
  autorisées restent bien distinctes. G0/G1/F0/F1/L sont cinq dimères, pas cinq
  nouveaux atomes. Une chaîne, un gène et une vésicule ne sont pas de nouveaux types.
- Les six liaisons se ramènent à quatre connectivités si l’on identifie les deux
  axes PR/HT et les deux captures R–R/R–ligand. Leurs longueurs et conditions
  restent différentes : le décompte détaillé6 évite de cacher ces profils.
- Le moteur utilise4 classes de collision, différentes des6 types chimiques : P, R,
  H/T libres et H/T liés. Sur10 canaux non ordonnés,5 sont répulsifs et5 transparents.
  Trois distances positives seulement (.28,.4,.7), plus le cas transparent0.
  Un changement libre/lié est une véritable règle contextuelle.
- Huit formules intrinsèques couvrent plusieurs profils : le même ressort sert
  cinq rôles paramétrés (PR, HT, squelette, appariement, capture). L’angle a deux
  profils actifs, G à0 et F à.8. Les symboles F0/F1 ont actuellement la même
  préférence angulaire : bibliothèque de replis programmables non démontrée.
- La capture est mutualisée entre P/R et H/T, mais le code impose encore leur
  compatibilité et l’identité des sites F0/F1. Ce n’est pas une chimie indifférenciée.
- L’isolé CR1 a tous ses H/T déjà liés. Sans rupture axiale, la synthèse HT n’y
  est pas accessible : seulement formation, rupture et échange de contacts latéraux.
  Ses petits nombres ne décrivent donc pas le coût de la cellule intégrée.
- Les pertes/recyclages, régulations et outils distincts nécessaires au maintien
  ne sont pas tous intégrés. Le coût du système final n’est pas encore borné par cet inventaire.

## Principales dettes de spécialisation

Les rôles G et F sont attribués aux supports primitifs : seuls G peuvent fournir
la matrice, F–F ne s’apparient pas. F0 recrute les catégories P/H et F1 les
catégories R/T. Un motif local de deux sites voisins déclenche la catalyse ;
il n’y a pas de primitive représentant une protéine entière, mais cette grammaire
est choisie pour les fonctions recherchées. La coopération qui exclut les mélanges
P/R–H/T, les échanges terminaux et la barrière visant les PR assemblés sont aussi
des choix spécifiques. Le filtre énergétique traite HT/L différemment des PR.
Enfin, la libération périodique est un helper externe, pas une autonomie émergente.

## Comment comparer les prochaines variantes

Comparer le vecteur (atomes résolus, composites, profils de liaisons, ports, formules,
transitions, prédicats fonctionnels, contrôles numériques, forcing) sous cette même
convention. Donner les IDs ajoutés/retirés et leur réutilisation démontrée. Un nouveau
seuil par réaction ou une nouvelle affinité spécialisée augmente le coût même si le
nombre de particules reste fixe. Un passage gaussien→compétitif change une formule,
sans ajouter d’atome, mais augmente sa portée/coût : ces deux axes restent séparés.
Ne pas fusionner des lignes après coup pour faire baisser artificiellement le score.
Une nouvelle famille de fonctions obtenue par assemblage sous lois fixes constitue
la contrepartie recherchée ; compter les démos ou les lignes de code ne la remplace pas.

## Détail des primitives, transitions et conditions

### Types élémentaires

| ID | Définition | Détail | Source |
|---|---|---|---|
| PG | P support with G role |  | [assembly.py](../simulator/assembly.py), [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| PF | P support with F role |  | [assembly.py](../simulator/assembly.py), [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| R0 | Recognizer carrying symbol0 |  | [assembly.py](../simulator/assembly.py), [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| R1 | Recognizer carrying symbol1 |  | [assembly.py](../simulator/assembly.py), [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| H | Lipid head precursor |  | [assembly.py](../simulator/assembly.py), [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| T | Lipid tail precursor |  | [assembly.py](../simulator/assembly.py), [mixed_synthesis.py](../simulator/mixed_synthesis.py) |

### Dimères

| ID | Définition | Détail | Source |
|---|---|---|---|
| G0 | PG--R0 |  | [assembly.py](../simulator/assembly.py), [linked_lipids.py](../simulator/linked_lipids.py) |
| G1 | PG--R1 |  | [assembly.py](../simulator/assembly.py), [linked_lipids.py](../simulator/linked_lipids.py) |
| F0 | PF--R0 |  | [assembly.py](../simulator/assembly.py), [linked_lipids.py](../simulator/linked_lipids.py) |
| F1 | PF--R1 |  | [assembly.py](../simulator/assembly.py), [linked_lipids.py](../simulator/linked_lipids.py) |
| L | H--T |  | [assembly.py](../simulator/assembly.py), [linked_lipids.py](../simulator/linked_lipids.py) |

### Liaisons/contact

| ID | Définition | Détail | Source |
|---|---|---|---|
| PR | Axial P--R |  | [assembly.py](../simulator/assembly.py) |
| HT | Axial H--T |  | [lipid_synthesis.py](../simulator/lipid_synthesis.py) |
| BB | Backbone P--P, G or F |  | [copy.py](../simulator/copy.py) |
| PAIR | Recognizer R--R pairing |  | [copy.py](../simulator/copy.py) |
| CAP | F recognizer--free ligand capture |  | [precursors.py](../simulator/precursors.py) |
| LAT | Lateral four-bead L face contact |  | [docking.py](../simulator/docking.py) |

### Ports

| ID | Définition | Détail | Source |
|---|---|---|---|
| PRA | P/R axial partner | capacité 1 sur le porteur concerné | [assembly.py](../simulator/assembly.py) |
| HTA | H/T axial partner | capacité 1 sur le porteur concerné | [linked_lipids.py](../simulator/linked_lipids.py) |
| BBA | P backbone directions | capacité 2 sur le porteur concerné | [reference.py](../simulator/reference.py) |
| PAA | R pairing partner | capacité 1 sur le porteur concerné | [copy.py](../simulator/copy.py) |
| CAA | F recognizer ligand slot | capacité 1 sur le porteur concerné | [precursors.py](../simulator/precursors.py) |
| LAA | L lateral faces, two subpatches per face | capacité 2 sur le porteur concerné | [docking.py](../simulator/docking.py) |

### Formules intrinsèques

| ID | Définition | Détail | Source |
|---|---|---|---|
| CORE | Soft finite-range repulsion |  | [physics.py](../simulator/physics.py) |
| SPRING | Harmonic distance |  | [physics.py](../simulator/physics.py) |
| ANGLE | Cosine angular elasticity |  | [physics.py](../simulator/physics.py) |
| ORIENT | Antiparallel paired axes |  | [physics.py](../simulator/physics.py) |
| GAUSS | Saturable Gaussian ligand attraction |  | [precursors.py](../simulator/precursors.py) |
| FREE | Competitive free L port potential |  | [competitive_ports.py](../simulator/competitive_ports.py) |
| BOUND | Harmonic bound L port continuation |  | [docking.py](../simulator/docking.py) |
| BARRIER | Bound-segment repulsion against assembled P/R atoms |  | [mixed_boundary.py](../simulator/mixed_boundary.py) |

### Transitions dirigées

| ID | Définition | Détail | Source |
|---|---|---|---|
| CAP_ON | Capture a free precursor on F | G01, G02, S08, S09, S10 | [precursors.py](../simulator/precursors.py) |
| CAP_OFF | Release precursor from F | S08 | [precursors.py](../simulator/precursors.py) |
| PR_ON | Form P--R, release captured product | G01, G02, S11, S12 | [assembly.py](../simulator/assembly.py) |
| HT_ON | Form H--T, release captured product | G02, S11, S12, S16 | [lipid_synthesis.py](../simulator/lipid_synthesis.py) |
| PAIR_ON | Form R--R recognition pairing | G01, G02, S01, S02, S03, S04, S05 | [copy.py](../simulator/copy.py) |
| PAIR_OFF | Break R--R pairing | Horloge externe / état local | [copy.py](../simulator/copy.py) |
| BB_ON | Template the parallel backbone edge | G02, G03, G04, S06 | [copy.py](../simulator/copy.py) |
| LAT_ON | Form lateral L contact | G02, G04, S13, S16 | [docking.py](../simulator/docking.py) |
| LAT_OFF | Break lateral L contact | S16 | [docking.py](../simulator/docking.py) |
| LAT_EX | Replace one lateral partner by another | G02, G04, S13, S14, S16 | [contact_exchange.py](../simulator/contact_exchange.py) |

### Conditions partagées

| ID | Définition | Détail | Source |
|---|---|---|---|
| G01 | Composite axial presence exposes the recognizer and slots | occupancy | [assembly.py](../simulator/assembly.py), [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| G02 | Single occupied slot, pairing/capture mutual exclusion | occupancy | [copy.py](../simulator/copy.py), [precursors.py](../simulator/precursors.py) |
| G03 | At most two backbone neighbors, opposite directions | occupancy | [reference.py](../simulator/reference.py) |
| G04 | Exclude duplicate partner/contact and touched exchange faces | occupancy | [docking.py](../simulator/docking.py), [contact_exchange.py](../simulator/contact_exchange.py) |
| S01 | Equal binary symbol for template recognition | structural | [copy.py](../simulator/copy.py) |
| S02 | Forbid F--F recognition pairing | functional | [copy.py](../simulator/copy.py) |
| S03 | G--F capture requires linked G and free F monomer | functional | [copy.py](../simulator/copy.py) |
| S04 | Monomer-only XOR for capture | functional | [copy.py](../simulator/copy.py) |
| S05 | Neighboring template captures must have same incoming family | functional | [copy.py](../simulator/copy.py) |
| S06 | Only G--G source edges can template ligation | functional | [copy.py](../simulator/copy.py) |
| S07 | Native angle applies only to unpaired F | functional | [copy.py](../simulator/copy.py) |
| S08 | Linked F site fully active, isolated F site weakened | functional | [mixed_synthesis.py](../simulator/mixed_synthesis.py), [precursors.py](../simulator/precursors.py) |
| S09 | F0 recruits P/H; F1 recruits R/T | functional | [mixed_synthesis.py](../simulator/mixed_synthesis.py), [precursors.py](../simulator/precursors.py) |
| S10 | Neighbor captures require same P/R versus H/T group and complementary categories | functional | [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| S11 | Two recruited substrates accelerated only on adjacent F sites | structural | [assembly.py](../simulator/assembly.py), [lipid_synthesis.py](../simulator/lipid_synthesis.py) |
| S12 | Product whitelist: P--R and H--T, no cross-material product | functional | [assembly.py](../simulator/assembly.py), [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| S13 | Opposite L faces and coincident head/tail subpatches | structural | [docking.py](../simulator/docking.py) |
| S14 | Exchange requires at least one outer free face | structural | [contact_exchange.py](../simulator/contact_exchange.py) |
| S15 | L segment barrier targets assembled P/R, not free precursors | functional | [mixed_boundary.py](../simulator/mixed_boundary.py) |
| S16 | Energy gates on H/T and L transitions, historical P/R formation ungated | functional | [lipid_synthesis.py](../simulator/lipid_synthesis.py), [assembly.py](../simulator/assembly.py), [docking.py](../simulator/docking.py) |

### Registres d’état dérivés

| Registre | Valeurs |
|---|---|
| PR axial occupancy | free, bound |
| HT axial occupancy | free, bound |
| Two P backbone ports | none, one, two |
| R recognition partner | free, paired |
| F ligand capture | free, occupied |
| Two L lateral faces | 00, 01, 10, 11 |

Ces états concernent des porteurs différents ; leur produit cartésien ne décrit pas
un nombre d’espèces indépendant. Activité et repli dépendent d’occupations existantes,
pas de deux nouvelles molécules ou de labels de fonction entière.

### Contrôles numériques configurés

| ID | Quantité | Valeur | Source |
|---|---|---:|---|
| C00 | chemistry.temperature | 0.08 | [config.py](../simulator/config.py) |
| C01 | chemistry.rung_capture_radius | 0.58 | [config.py](../simulator/config.py) |
| C02 | chemistry.rung_formation_rate | 0.0001 | [config.py](../simulator/config.py) |
| C03 | chemistry.rung_catalytic_rate | 20.0 | [config.py](../simulator/config.py) |
| C04 | chemistry.food_binding_radius | 0.25 | [config.py](../simulator/config.py) |
| C05 | chemistry.food_binding_rate | 20.0 | [config.py](../simulator/config.py) |
| C06 | chemistry.food_unbinding_rate | 0.1 | [config.py](../simulator/config.py) |
| C07 | chemistry.food_ligand_energy | 2.0 | [config.py](../simulator/config.py) |
| C08 | chemistry.food_ligand_width | 0.6 | [config.py](../simulator/config.py) |
| C09 | chemistry.short_length | 0.92 | [config.py](../simulator/config.py) |
| C10 | chemistry.dock_width | 0.6 | [config.py](../simulator/config.py) |
| C11 | chemistry.dock_energy | 4.0 | [config.py](../simulator/config.py) |
| C12 | chemistry.dock_capture | 0.25 | [config.py](../simulator/config.py) |
| C13 | chemistry.dock_rate | 25.0 | [config.py](../simulator/config.py) |
| C14 | chemistry.bond_off_rate | 0.02 | [config.py](../simulator/config.py) |
| C15 | chemistry.break_extension | 0.35 | [config.py](../simulator/config.py) |
| C16 | chemistry.contact_exchange_rate | 0.2 | [config.py](../simulator/config.py) |
| C17 | chemistry.contact_exchange_capture | 0.8 | [config.py](../simulator/config.py) |
| C18 | chemistry.tool_lipid_contact | 0.0 | [config.py](../simulator/config.py) |
| C19 | chemistry.bound_barrier_radius | 0.55 | [config.py](../simulator/config.py) |
| C20 | chemistry.bound_barrier_stiffness | 80.0 | [config.py](../simulator/config.py) |
| C21 | chemistry.genetics.backbone_angle | 20.0 | [config.py](../simulator/config.py) |
| C22 | chemistry.genetics.ligation_rate | 12.0 | [config.py](../simulator/config.py) |
| C23 | chemistry.genetics.functional_cosines.0 | 0.8 | [config.py](../simulator/config.py) |
| C24 | chemistry.genetics.functional_cosines.1 | 0.8 | [config.py](../simulator/config.py) |
| C25 | mechanics.mass | 1.0 | [config.py](../simulator/config.py) |
| C26 | mechanics.damping | 0.1 | [config.py](../simulator/config.py) |

### Contrôles numériques fixes recensés

| ID | Quantité | Valeur | Source |
|---|---|---:|---|
| CORE_K | Soft core stiffness | 80.0 | [physics.py](../simulator/physics.py) |
| CORE_PP | P/P contact radius | 0.7 | [copy.py](../simulator/copy.py), [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| CORE_PR | P/R contact radius | 0.28 | [copy.py](../simulator/copy.py), [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| CORE_HTL | H/T/L contact radius | 0.4 | [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| PR_K | Axial PR stiffness | 180.0 | [copy.py](../simulator/copy.py) |
| PR_L | Axial PR length | 0.45 | [copy.py](../simulator/copy.py) |
| HT_K | Axial HT stiffness | 180.0 | [linked_lipids.py](../simulator/linked_lipids.py) |
| HT_L | Axial HT length | 0.65 | [linked_lipids.py](../simulator/linked_lipids.py) |
| BB_K | Backbone stiffness | 100.0 | [copy.py](../simulator/copy.py) |
| BB_L | Backbone length | 1.0 | [copy.py](../simulator/copy.py) |
| PAIR_K | Pairing spring stiffness | 80.0 | [copy.py](../simulator/copy.py) |
| PAIR_L | Pairing spring rest length | 0.0 | [copy.py](../simulator/copy.py) |
| ORIENT_K | Paired-axis orientation stiffness | 8.0 | [physics.py](../simulator/physics.py) |
| PAIR_R | Pairing capture radius | 0.3 | [copy.py](../simulator/copy.py) |
| PAIR_COS | Pairing maximum axis dot | -0.5 | [copy.py](../simulator/copy.py) |
| PAIR_ON_K | Supported pairing on rate | 35.0 | [copy.py](../simulator/copy.py) |
| PAIR_OFF_K | Basal pairing off rate | 0.003 | [copy.py](../simulator/copy.py) |
| PAIR_OFF_RELEASE | Forced release off rate | 12.0 | [copy.py](../simulator/copy.py) |
| WEAK_SITE | Isolated F activity multiplier | 0.002857142857142857 | [mixed_synthesis.py](../simulator/mixed_synthesis.py) |
| WEAK_OFF | Inactive-site off-rate floor | 5.0 | [precursors.py](../simulator/precursors.py) |
| LIG_MIN | Ligation min distance | 0.72 | [copy.py](../simulator/copy.py) |
| LIG_MAX | Ligation max distance | 1.28 | [copy.py](../simulator/copy.py) |
| LIG_COS | Ligation min relative-axis dot | 0.5 | [copy.py](../simulator/copy.py) |
| LIG_PROJ | Ligation max axial projection fraction | 0.5 | [copy.py](../simulator/copy.py) |
| G_COS | G backbone angle cosine | 0.0 | [copy.py](../simulator/copy.py) |
| L_LONG | L head port width | 1.0 | [docking.py](../simulator/docking.py) |
| CAP_CUT | Capture Gaussian cutoff in widths | 3.0 | [precursors.py](../simulator/precursors.py) |
| PORT_CUT | Port cutoff in squared-width energy coordinate | 8.0 | [competitive_ports.py](../simulator/competitive_ports.py) |

### Contrôles externes

| ID | Quantité | Valeur | Source |
|---|---|---:|---|
| PERIOD | External release period | 200.0 | [copy.py](../simulator/copy.py) |
| WINDOW | External release window | 15.0 | [copy.py](../simulator/copy.py) |
| WALL | Uniform soft wall stiffness | 100.0 | [motion.py](../simulator/motion.py) |

## Exclusions et limites

- PR/HT/backbone cleavage and recycling absent from this candidate.
- Second recognition face disabled.
- F end recapture variant disabled.
- Alternative functional three-center bend table empty.
- Old separate food ligation subsystem disabled.
- Local release alternative disabled.
- DPD thermostat disabled.
- Other registered hooks and historical additive potential excluded.
- Low pairing-on .1 and monomer-pair off5 code remain, but active monomer-only/no-cleavage grammar makes these contexts unreachable from the declared seed.

Le bain de Langevin, les parois et l’horloge externe sont explicitement distincts
des8 potentiels intrinsèques. Initialisations, observations, critères de réussite,
pas/caches/JIT, gardes de stabilité numérique et variantes historiques sont exclus
du compte chimique. Les coefficients des parois et de l’horloge restent déclarés.

Source structurée : [CHEMISTRY_COMPLEXITY.json](CHEMISTRY_COMPLEXITY.json).
Génération/vérification : `python experiments/chemical_complexity.py build` / `check`.
Les hashes invalident la fiche quand une source auditée change ; une revue sémantique
doit alors déterminer ce qui a réellement changé. Aucun test de ce registre ne pilote la simulation.
