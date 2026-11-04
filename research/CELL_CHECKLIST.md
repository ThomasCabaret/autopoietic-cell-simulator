# Checklist détaillée — critères et dépendances

Revue 2026-11-04 · révision7. Source : [cell_checklist.json](cell_checklist.json).
[Tableau compact](CELL_CHECKLIST_COMPACT.md) · [Échelle et méthode](CONCEPT_FIRST.md).

Les dépendances ci-dessous sont les capacités requises à terme, pas un ordre acyclique de codage. Les cycles de renouvellement sont intentionnels. Une condition initiale construite peut amorcer un sous-cas sans fermer ces cycles.

## Lois et fonctions des outils

<a id="F-01"></a>
### F-01 — Alphabet, ports et lois réutilisables

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Un petit jeu fixe de primitives construit tous les constituants et admet les fonctions requises sans règle par enzyme.

**Draft local :** Comparer alphabet P/R+L et modes de liaison/ports génériques ; garder l’identité des fonctions hors des primitives.

**Manque / limite :** Unification matérielle et coût des états N/A/L encore indéterminés.

**Dépend de :** — · **Pour renouveler :** —

**Portée des preuves :** Union de modules locaux, pas alphabet commun constructible complet.

**Références :** [research/FUNCTIONAL_MECHANISMS.md](../research/FUNCTIONAL_MECHANISMS.md), [research/LOCALITY_AUDIT.md](../research/LOCALITY_AUDIT.md), [research/BATCH_32.md](../research/BATCH_32.md)

**Prochain test / décision :** Chercher un second produit utile puis L sous exactement les mêmes lois.

<a id="F-02"></a>
### F-02 — Fonctions distinctes depuis les assemblages

**Concept : esquisse à fermer · Preuve : 0% (non observé).**

**Aboutissement :** Des assemblages différents donnent des productions distinctes utiles dans un bain commun, avec sélectivité mesurée.

**Draft local :** Disposer des sites/ports et des géométries qui favorisent différentes poses de réaction.

**Manque / limite :** Aucun couple EN/EA sélectif ni constructeur L sous une chimie fixe ; un assembleur polyvalent ne suffit pas.

**Dépend de :** [F-01](#F-01), [F-03](#F-03) · **Pour renouveler :** [T-04](#T-04)

**Portée des preuves :** Un seul motif P/R, pas bibliothèque sélective.

**Références :** [research/FUNCTIONAL_MECHANISMS.md](../research/FUNCTIONAL_MECHANISMS.md), [research/BATCH_32.md](../research/BATCH_32.md)

**Prochain test / décision :** Concevoir le motif minimal et son mauvais produit discriminant avant campagne.

<a id="F-03"></a>
### F-03 — Capture, catalyse, libération et réutilisation

**Concept : draft décrit · Preuve : 75% (couplage partiel).**

**Aboutissement :** L’outil réalise des cycles utiles répétés sans être consommé, empoisonné ou alimenté par un bonus caché.

**Draft local :** Sites saturables voisins recrutent deux réactifs ; jonction locale et changement d’affinité libèrent le produit.

**Manque / limite :** Helper de taux explicite ; généralisation aux autres réactions et sélectivité non démontrées.

**Dépend de :** [F-01](#F-01), [Q-01](#Q-01) · **Pour renouveler :** [T-04](#T-04)

**Portée des preuves :** MD2 avec outils préparés et MIN1R petit bain avec remplaçants entièrement reconstruits actifs3/3 ; un seul assembleur P/R, pas maintien cellulaire.

**Références :** [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md), [research/BATCH_08.md](../research/BATCH_08.md), [research/BATCH_32.md](../research/BATCH_32.md), [research/BATCH_34.md](../research/BATCH_34.md)

**Prochain test / décision :** Lire MIN1 B complet, comparer produits effectivement utilisés des F exprimés, puis transfert dans le grand bain.

## Fabrication N / A

<a id="S-01"></a>
### S-01 — Précurseurs vers monomères génétiques

**Concept : draft décrit · Preuve : 75% (couplage partiel).**

**Aboutissement :** Les monomères G/N fabriqués depuis la nourriture déclarée entrent dans des copies utilisables avec le débit requis.

**Draft local :** Un motif de capture favorise une liaison entre un support génétique libre et un reconnaisseur réel.

**Manque / limite :** Nourriture spécialisée P_G ; spécification XYZ et outil sélectif restent ouverts.

**Dépend de :** [F-01](#F-01), [F-03](#F-03), [E-03](#E-03), [Q-01](#Q-01) · **Pour renouveler :** [T-04](#T-04)

**Portée des preuves :** MD2 : produits catalysés incorporés dans G/F, seulement régime fini et courtes séquences.

**Références :** [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md), [simulator/assembly.py](../simulator/assembly.py)

**Prochain test / décision :** Tracer la matière jusqu’aux copies puis renouveler le catalyseur sous les mêmes lois.

<a id="S-02"></a>
### S-02 — Précurseurs vers monomères fonctionnels

**Concept : draft décrit · Preuve : 75% (couplage partiel).**

**Aboutissement :** Les monomères F/A fabriqués entrent dans des outils actifs avec un débit suffisant pour renouveler les capacités.

**Draft local :** Même assembleur P/R sur support fonctionnel ; le R donne le symbole réellement incorporé.

**Manque / limite :** Spécialisation P_F et absence de F nouveau complet dans le grand bain MD2.

**Dépend de :** [F-01](#F-01), [F-03](#F-03), [E-03](#E-03), [Q-01](#Q-01) · **Pour renouveler :** [T-04](#T-04)

**Portée des preuves :** Fabrication et incorporation partielle dans F sous MD2 ; aucune fermeture de renouvellement.

**Références :** [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md), [simulator/assembly.py](../simulator/assembly.py)

**Prochain test / décision :** Vérifier que les produits atteignent un outil complet puis actif, pas un stock de fragments.

<a id="S-03"></a>
### S-03 — État chimique correct et transfert du produit

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Chaque produit est utilisable directement dans l’étape aval sans conversion ni retouche des lois.

**Draft local :** Les ports et états de liaison du produit déterminent ses interactions et son usage suivant.

**Manque / limite :** Transfert P/R partiel connu ; états communs N/A/L et toutes les chaînes aval manquent.

**Dépend de :** [F-01](#F-01), [S-01](#S-01), [S-02](#S-02), [S-04](#S-04) · **Pour renouveler :** —

**Portée des preuves :** C3B1 transfère un sous-réseau ; union finale non testée.

**Références :** [research/BATCH_08.md](../research/BATCH_08.md), [research/CELL_INTERACTIONS.md](../research/CELL_INTERACTIONS.md)

**Prochain test / décision :** Tester le même produit synthétisé dans la réaction suivante, avec mauvais état isomasse.

## Fabrication des lipides

<a id="S-04"></a>
### S-04 — Nourriture vers lipides polaires

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Des L fabriqués localement depuis les intrants déclarés s’insèrent et renouvellent la frontière.

**Draft local :** L1 implémente H/T libres captés par le F01 existant, lien axial physique saturé et ports MD2 indexés par vrais partenaires. Voie H/T séparée ; P/R+H/T reste un draft.

**Manque / limite :** Saut de potentiel et échauffement identifiés ; compatibilité capture/état lié, compétition P/R/H/T, expression et insertion cellulaire non établies. C0B/XYZ distinct.

**Dépend de :** [F-01](#F-01), [F-02](#F-02), [F-03](#F-03), [E-03](#E-03), [Q-01](#Q-01) · **Pour renouveler :** [T-04](#T-04)

**Portée des preuves :** Un pilote L1 à100,64 billes :22 H–T, tous catalysés,16 contacts latéraux ; jusqu’à8 produits par paire de sites. Une graine sans contrôles dispersés, température cinétique nettement supérieure à la consigne. MD2 fournit toujours L préparés.

**Références :** [research/FUNCTIONAL_MECHANISMS.md](../research/FUNCTIONAL_MECHANISMS.md), [research/CELL_ARCHITECTURE.md](../research/CELL_ARCHITECTURE.md), [research/BATCH_32.md](../research/BATCH_32.md), [research/LIPID_CONSTRUCTION_DRAFT.md](../research/LIPID_CONSTRUCTION_DRAFT.md), [research/BATCH_36.md](../research/BATCH_36.md), [research/BATCH_37.md](../research/BATCH_37.md)

**Prochain test / décision :** Traiter le coût local de la transition L1 puis témoins no_tool/split/no_boost et thermique ; ensuite compétition P/R et insertion des vrais produits, sans conversion externe.

**Progrès du dernier lot :** L2 :19/21/21 L avec contrôle combiné, témoins négatifs ; critères thermiques refusés, palier25 inchangé.

## Copie et information

<a id="R-01"></a>
### R-01 — Reconnaissance et alignement des bases

**Concept : draft décrit · Preuve : 75% (couplage partiel).**

**Aboutissement :** Les bonnes unités s’apparient localement et permettent les ligations dans les conditions communes.

**Draft local :** Symboles, orientation, saturation de sites et voisinage lié contrôlent appariement et ligation.

**Manque / limite :** Sélectivité en mélange long et cadence numérique à vérifier ; concordance des symboles est une loi choisie.

**Dépend de :** [F-01](#F-01), [S-01](#S-01), [E-02](#E-02), [Q-01](#Q-01) · **Pour renouveler :** —

**Portée des preuves :** Copies G001 ponctuelles dans le bain MD2.

**Références :** [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md), [simulator/copy.py](../simulator/copy.py)

**Prochain test / décision :** Mesurer contacts admissibles, mauvais appariements et ligations utiles en mélange.

<a id="R-02"></a>
### R-02 — Finition, bouts et parasites de copie

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Des chaînes de la longueur fonctionnelle sont terminées sans domination de fragments ni allongements parasites.

**Draft local :** Pistes de finition par occupations locales des bouts, recapture ou processivité ; aucune longueur cible lue.

**Manque / limite :** Motif efficace non choisi ; les fragments sont de vrais concurrents et T9E n’améliore pas l’expression.

**Dépend de :** [R-01](#R-01), [S-01](#S-01), [E-02](#E-02) · **Pour renouveler :** —

**Portée des preuves :** Contrôles de garde et fragments observés, pas solution générique.

**Références :** [research/BATCH_22.md](../research/BATCH_22.md), [research/BATCH_27.md](../research/BATCH_27.md), [research/FUNCTIONAL_MECHANISMS.md](../research/FUNCTIONAL_MECHANISMS.md)

**Prochain test / décision :** Localiser l’échec de finition avant de choisir une règle ou proposer une machine.

<a id="R-03"></a>
### R-03 — Libération et descendants réutilisables

**Concept : draft décrit · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Des copies complètes libérées servent elles-mêmes de matrices sur plusieurs générations pertinentes.

**Draft local :** Liaisons d’appariement réversibles ou cycle externe déclaré ; produits conservent leurs ports.

**Manque / limite :** Le cycle externe est une aide ; amplification de longue séquence et réutilisation robuste non obtenues.

**Dépend de :** [R-02](#R-02), [Q-02](#Q-02) · **Pour renouveler :** —

**Portée des preuves :** Courtes copies et filiation observées ; population longue dominée par fragments.

**Références :** [research/BATCH_22.md](../research/BATCH_22.md), [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md)

**Prochain test / décision :** Suivre générations complètes et réserves sans confondre fragments templants et descendants utiles.

<a id="R-04"></a>
### R-04 — Cohabitation de tous les gènes

**Concept : esquisse à fermer · Preuve : 0% (non observé).**

**Aboutissement :** Chaque gène nécessaire est copié dans le même bain sans extinction relative ni chimères envahissantes.

**Draft local :** Brins séparés, plusieurs copies, reconnaissance locale et partage des ressources.

**Manque / limite :** Pas de séquences fonctionnelles distinctes ni de mécanisme de répartition validé.

**Dépend de :** [R-03](#R-03), [R-05](#R-05), [S-01](#S-01), [C-01](#C-01), [H-04](#H-04) · **Pour renouveler :** —

**Portée des preuves :** MD2 ne contient qu’une séquence001 en plusieurs exemplaires.

**Références :** [research/CELL_ARCHITECTURE.md](../research/CELL_ARCHITECTURE.md), [research/INTEGRATION_TESTS.json](../research/INTEGRATION_TESTS.json)

**Prochain test / décision :** Concevoir le plus petit mélange de gènes distincts avec diagnostics de compétition.

<a id="R-05"></a>
### R-05 — Conservation de l’information riche

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Séquences et longueurs utiles restent présentes sur le domaine de maintien, erreurs et chimères comptées.

**Draft local :** Sélectivité de motifs et cinétiques locales ; aucun tri selon séquence entière par la dynamique.

**Manque / limite :** Fidélité de population, recyclage des parasites et prévention de dérive non fermés.

**Dépend de :** [R-01](#R-01), [R-02](#R-02), [W-04](#W-04), [H-06](#H-06) · **Pour renouveler :** —

**Portée des preuves :** Recensements P10/LT1 montrent fragments et limites ; pas preuve d’information stable.

**Références :** [research/BATCH_22.md](../research/BATCH_22.md), [simulator/polymer_population.py](../simulator/polymer_population.py)

**Prochain test / décision :** Suivre toutes les chaînes par type et longueur sur un horizon fixé, sans filtrage favorable.

## Traduction et outils renouvelés

<a id="T-01"></a>
### T-01 — Transfert G vers chaîne F

**Concept : draft décrit · Preuve : 50% (test séparé).**

**Aboutissement :** Chaque séquence fonctionnelle code sa chaîne F avec le bon ordre sous les lois du bain commun.

**Draft local :** Recrutement local des monomères F sur G et ligation sur motifs voisins.

**Manque / limite :** Un symbole pour un monomère envisagé ; diversité et longueurs réelles non établies.

**Dépend de :** [R-01](#R-01), [S-02](#S-02), [F-01](#F-01) · **Pour renouveler :** —

**Portée des preuves :** MIN1R sous MD2 sans membrane :11/13/12 F01 nouveaux avec outil construit ; MIN1 sans F initial reste fragile. Aucune capacité générale de traduction longue démontrée.

**Références :** [research/BATCH_08.md](../research/BATCH_08.md), [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md), [research/BATCH_32.md](../research/BATCH_32.md), [research/BATCH_33.md](../research/BATCH_33.md), [research/BATCH_34.md](../research/BATCH_34.md)

**Prochain test / décision :** Transférer le gène01/outilF01 au bain avec membrane et comparer aux préparations MD2 ; préserver le test d’information riche.

<a id="T-02"></a>
### T-02 — Libération, conformation et état actif

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** La chaîne traduite se libère et atteint une géométrie fonctionnelle au lieu de rester attachée ou agrégée.

**Draft local :** Occupation d’appariement modifie les préférences locales ; les forces réorganisent la chaîne après libération.

**Manque / limite :** Pas de répertoire de repliements ; mêmes préférences angulaires F0/F1 dans MD2.

**Dépend de :** [T-01](#T-01), [F-02](#F-02), [Q-02](#Q-02), [C-01](#C-01) · **Pour renouveler :** —

**Portée des preuves :** Un outil court historique, pas famille commune de conformations.

**Références :** [research/FUNCTIONAL_MECHANISMS.md](../research/FUNCTIONAL_MECHANISMS.md), [simulator/copy.py](../simulator/copy.py)

**Prochain test / décision :** Comparer la pose attendue et les événements locaux, puis activité après expression.

<a id="T-03"></a>
### T-03 — Outil exprimé vers métabolisme utile

**Concept : draft décrit · Preuve : 75% (couplage partiel).**

**Aboutissement :** Un outil nouvellement exprimé fabrique un produit effectivement utilisé dans la même chimie.

**Draft local :** Même géométrie et ports pour outil préparé ou exprimé ; provenance identifiée seulement par l’observateur.

**Manque / limite :** Transfert historique limité à un outil ; grand bain actuel sans nouveau F complet.

**Dépend de :** [T-02](#T-02), [S-03](#S-03), [F-03](#F-03) · **Pour renouveler :** —

**Portée des preuves :** MIN1R :30 F entièrement refaits depuis nourriture sur3 graines active,8 de ces remplaçants catalysent30 opérations ; boucle locale sous mêmes lois, sans membrane ni pertes.

**Références :** [research/BATCH_08.md](../research/BATCH_08.md), [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md), [research/BATCH_32.md](../research/BATCH_32.md), [research/BATCH_33.md](../research/BATCH_33.md), [research/BATCH_34.md](../research/BATCH_34.md)

**Prochain test / décision :** Vérifier le même remplacement entier actif dans le bain avec L, puis sous pertes et flux déclarés.

<a id="T-04"></a>
### T-04 — Renouvellement de tous les outils

**Concept : esquisse à fermer · Preuve : 0% (non observé).**

**Aboutissement :** Toute capacité nécessaire, y compris un éventuel régulateur/recycleur, est refabriquée et active depuis la nourriture.

**Draft local :** Gènes distincts et chaîne de fabrication fermée, départ construit pour amorcer les cycles.

**Manque / limite :** Outils sélectifs et dépendances des nouvelles aides non réalisés ; pas de machine gratuite.

**Dépend de :** [T-03](#T-03), [R-04](#R-04), [S-01](#S-01), [S-02](#S-02), [S-04](#S-04), [Q-01](#Q-01), [T-05](#T-05) · **Pour renouveler :** —

**Portée des preuves :** Aucune fermeture complète des rôles EN/EA/EL.

**Références :** [research/CELL_ARCHITECTURE.md](../research/CELL_ARCHITECTURE.md), [research/FUNCTIONAL_MECHANISMS.md](../research/FUNCTIONAL_MECHANISMS.md)

**Prochain test / décision :** Tracer chaque outil ajouté jusqu’à son propre renouvellement avant adoption.

<a id="T-05"></a>
### T-05 — Production de remplaçants fonctionnels du co-recruteur

**Concept : draft décrit · Preuve : 50% (test séparé).**

**Aboutissement :** Des F entièrement reconstruits depuis la nourriture maintiennent la fonction lors de pertes déclarées du stock initial, avec témoins et transfert aux conditions requises.

**Draft local :** Un F construit fabrique P/R composites ; leur expression sur G produit un F dont chaque composite vient de nourriture, puis ses deux sites catalysent à nouveau.

**Manque / limite :** Production de remplaçants seulement : ancien F non retiré ici, maintien sous pertes/membrane, énergie et robustesse de population non établis. Tous les autres outils relèvent de T-04.

**Dépend de :** [T-03](#T-03), [S-02](#S-02), [S-03](#S-03) · **Pour renouveler :** [R-01](#R-01), [S-01](#S-01), [Q-01](#Q-01)

**Portée des preuves :** MIN1R9/9 terminé : active10/10/10 F entièrement refaits dont5/2/1 actifs ; split3/5/0 dont1/3/0 actifs ; nogene négatif3/3. Pas membrane/pertes/régime ouvert.

**Références :** [research/BATCH_34.md](../research/BATCH_34.md), [research/BATCH_34_PLAN.md](../research/BATCH_34_PLAN.md), [research/BATCH_35.md](../research/BATCH_35.md), [research/BATCH_37.md](../research/BATCH_37.md)

**Prochain test / décision :** Lire MIN1M complet et son crible de coexistence membrane / nouveau F entier actif ; puis pertes réelles et maintien.

**Progrès du dernier lot :** MIN1M9/12 achevés sans erreur ; deux graines active ont de vrais F neufs actifs, cohorte incomplète.

## Membrane et insertion

<a id="M-01"></a>
### M-01 — Assemblage depuis molécules L isolées

**Concept : draft décrit · Preuve : 50% (test séparé).**

**Aboutissement :** Des L individuels s’associent sans ruban préparé sous les mêmes lois que la frontière utile.

**Draft local :** Ports latéraux orientés et géométrie locale liée/libre cohérente.

**Manque / limite :** Petites V8 et grandes frontières ont encore des paramètres géométriques différents ; L ne sont pas fabriqués.

**Dépend de :** [F-01](#F-01), [S-04](#S-04) · **Pour renouveler :** —

**Portée des preuves :** V8 MD2 s’assemble à partir de dimères isolés sur trois graines, bain séparé.

**Références :** [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md)

**Prochain test / décision :** Transférer aux L réellement fabriqués et à la géométrie commune requise.

<a id="M-02"></a>
### M-02 — Frontière dimensionnée pour le contenu

**Concept : draft décrit · Preuve : 75% (couplage partiel).**

**Aboutissement :** Une frontière contenant l’inventaire fonctionnel reste intègre sans petits bourgeons dominants ni fuite fatale.

**Draft local :** Courbure et souplesse issues des ports/liaisons locaux, départ en grande frontière permis.

**Manque / limite :** Inventaire cible inconnu, longueurs non trouvées ; trois bains ne prouvent pas robustesse générale.

**Dépend de :** [M-01](#M-01), [C-02](#C-02), [E-03](#E-03) · **Pour renouveler :** —

**Portée des preuves :** MD2 grand bain2118 billes, membrane préparée, fermeture partielle.

**Références :** [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md)

**Prochain test / décision :** Tester l’inventaire réellement nécessaire, ouvertures et charge sans consigne de contour.

<a id="M-03"></a>
### M-03 — Perméabilité et rétention sélectives

**Concept : draft décrit · Preuve : 75% (couplage partiel).**

**Aboutissement :** Apports et petits déchets passent tandis que stocks utiles sont retenus sans adsorption nuisible.

**Draft local :** Profil d’interaction dépend de l’état local P–R ; répulsion contre billes et segments L réels.

**Manque / limite :** Helper libre/lié explicite ; fuites et périodes de frontière inconnue, déchets futurs non transférés.

**Dépend de :** [F-01](#F-01), [M-02](#M-02) · **Pour renouveler :** —

**Portée des preuves :** P/R libres/liés dans MD2 et sondes séparées ; pas étanchéité garantie.

**Références :** [research/LOCALITY_AUDIT.md](../research/LOCALITY_AUDIT.md), [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md)

**Prochain test / décision :** Comparer passages réels par classe et état en conservant les périodes non classables.

<a id="M-04"></a>
### M-04 — Insertion depuis dedans et refermeture

**Concept : esquisse à fermer · Preuve : 75% (couplage partiel).**

**Aboutissement :** Des L nouvellement fabriqués à l’intérieur intègrent la frontière avec insertion et confinement conjoints.

**Draft local :** Échange de contacts latéraux locaux, puis relaxation mécanique ; une insertase serait une autre option payante.

**Manque / limite :** L actuellement préparés ; une graine à sondes reste dégradée, mécanisme de réparation à diagnostiquer.

**Dépend de :** [S-04](#S-04), [M-02](#M-02), [M-03](#M-03) · **Pour renouveler :** —

**Portée des preuves :** Insertions rares de L préparés dans MD2 ; pas circuit synthèse L→membrane.

**Références :** [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md)

**Prochain test / décision :** Analyser l’échange défectueux puis transférer de vrais L synthétisés, sans réparer un contour.

<a id="M-05"></a>
### M-05 — Réparation et remplacement de frontière

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Les pertes et lésions sont compensées sans empêcher l’échange ni provoquer croissance incontrôlée.

**Draft local :** Recapture réversible, échanges et flux équilibrés de constituants L.

**Manque / limite :** Réparation sous pertes, synthèse et recyclage L non fermés.

**Dépend de :** [M-04](#M-04), [H-05](#H-05), [Q-01](#Q-01) · **Pour renouveler :** [S-04](#S-04)

**Portée des preuves :** Contacts cohérents et recaptures locales, pas maintien de frontière renouvelée.

**Références :** [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md), [research/HOMEOSTASIS.md](../research/HOMEOSTASIS.md)

**Prochain test / décision :** Lésion locale prédéfinie avec nouveaux L, mesurer récupération et matière renouvelée.

## Apports et transport

<a id="E-01"></a>
### E-01 — Source et puits au bord extérieur

**Concept : draft décrit · Preuve : 0% (non observé).**

**Aboutissement :** Injection et absorption au bord conservatrices, flux réglables et nombres variables sans sauvetage interne.

**Draft local :** Création de précurseurs dans une couche de bord, diffusion puis absorption lors de la sortie.

**Manque / limite :** Convention de bord, tables dynamiques/IDs et calibration non implémentés.

**Dépend de :** [F-01](#F-01), [O-02](#O-02) · **Pour renouveler :** —

**Portée des preuves :** Les bains actuels sont finis et à murs mécaniques.

**Références :** [research/OPEN_BOUNDARY.md](../research/OPEN_BOUNDARY.md)

**Prochain test / décision :** Boîte sans cellule : flux, bilan matière, retour immédiat au bord et raffinement en dt.

<a id="E-02"></a>
### E-02 — Mélange et rencontres de toutes les classes

**Concept : draft décrit · Preuve : 75% (couplage partiel).**

**Aboutissement :** Les espèces et agrégats atteignent leurs partenaires assez vite en temps réel sans déstabiliser les fonctions.

**Draft local :** Langevin inertiel local, forces transmises entre voisins liés, index spatial partagé.

**Manque / limite :** Les rencontres de la future bibliothèque et le coût d’un renouvellement complet restent inconnus.

**Dépend de :** [F-01](#F-01), [C-02](#C-02) · **Pour renouveler :** —

**Portée des preuves :** Langevin transféré à MD2, benchmarks de mélange séparés.

**Références :** [research/BATCH_22.md](../research/BATCH_22.md), [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md)

**Prochain test / décision :** Mesurer contacts utiles par classe et durée, pas seulement dispersion spatiale.

<a id="E-03"></a>
### E-03 — Alimentation accessible et encombrement

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Le flux arrivant effectivement aux sites couvre les besoins sans dilution, adsorption ou surcharge incompatibles.

**Draft local :** Diffusion depuis le bord, consommation locale ; gradients admis et mesurés.

**Manque / limite :** Dimensionnement du domaine et régime de flux utile non établis pour la cellule cible.

**Dépend de :** [E-01](#E-01), [E-02](#E-02), [M-03](#M-03), [O-01](#O-01) · **Pour renouveler :** —

**Portée des preuves :** Stocks et transport de bains fermés observés ; aucun apport ouvert.

**Références :** [research/OPEN_BOUNDARY.md](../research/OPEN_BOUNDARY.md), [research/KINETICS_AND_PERFORMANCE.md](../research/KINETICS_AND_PERFORMANCE.md)

**Prochain test / décision :** Comparer flux entrants utiles, besoins et crowding à lois/précision fixées.

## Énergie et retour des cycles

<a id="Q-01"></a>
### Q-01 — Énergie, activation et aides déclarées

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Chaque cycle est alimenté par une ressource ou un forçage explicite avec bilan, aides et déchets cohérents.

**Draft local :** Choisir ressources activées ou protocole externe figé ; ne pas inventer une autonomie énergétique.

**Manque / limite :** E/W de C0B n’est pas le moteur ; travail du cycle et transitions d’affinité non calibrés.

**Dépend de :** [F-01](#F-01), [E-01](#E-01), [W-01](#W-01) · **Pour renouveler :** —

**Portée des preuves :** Thermostat, activation et cycle externes déclarés ; bilan énergétique complet absent.

**Références :** [research/CELL_ARCHITECTURE.md](../research/CELL_ARCHITECTURE.md), [research/LOCALITY_AUDIT.md](../research/LOCALITY_AUDIT.md), [research/BATCH_36.md](../research/BATCH_36.md), [research/BATCH_37.md](../research/BATCH_37.md)

**Prochain test / décision :** Établir le budget du motif retenu, puis ablater l’aide sans masquer un apport.

**Progrès du dernier lot :** Variation locale d’énergie vérifiée ; naissance H–T seule ne ferme pas le bilan capture/repliement.

<a id="Q-02"></a>
### Q-02 — Retour local et disponibilité après cycle

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Les outils/templates redeviennent utilisables sans reset global dépendant du succès observé.

**Draft local :** Libération par états locaux de liaison et affinités ; cycle imposé seulement s’il est fixé et déclaré.

**Manque / limite :** Pas de cycle local générique testé pour toute la future bibliothèque ; aide périodique encore présente.

**Dépend de :** [Q-01](#Q-01), [F-03](#F-03) · **Pour renouveler :** —

**Portée des preuves :** Libération de produit locale connue, libération génétique aidée par cycle externe.

**Références :** [research/FUNCTIONAL_MECHANISMS.md](../research/FUNCTIONAL_MECHANISMS.md), [research/BATCH_08.md](../research/BATCH_08.md)

**Prochain test / décision :** Observer un cycle complet capture→produit→libération→réutilisation et compter ses ressources.

## Déchets et recyclage

<a id="W-01"></a>
### W-01 — Petits déchets vers l’extérieur

**Concept : draft décrit · Preuve : 0% (non observé).**

**Aboutissement :** Les espèces de déchet produites passent puis quittent réellement le domaine sans intoxiquer les sites.

**Draft local :** Déchets libres peu affins diffusent à travers la frontière puis vers le puits extérieur.

**Manque / limite :** Pas de W réel ni de sortie ouverte ; affinités et gradients à choisir.

**Dépend de :** [E-01](#E-01), [M-03](#M-03), [Q-01](#Q-01) · **Pour renouveler :** —

**Portée des preuves :** Sondes perméables ne prouvent pas l’export d’un déchet métabolique.

**Références :** [research/OPEN_BOUNDARY.md](../research/OPEN_BOUNDARY.md), [research/CELL_INTERACTIONS.md](../research/CELL_INTERACTIONS.md)

**Prochain test / décision :** Produire le déchet dans la cellule puis mesurer export, stock et inhibition.

<a id="W-02"></a>
### W-02 — Clivage des polymères et récupération

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Chaînes usées/parasites donnent de vrais monomères réutilisables sans détruire le réseau utile.

**Draft local :** RV1 : taux locaux de rupture G/F sur chaque lien de squelette, protection par appariement ou ligand sur un des deux sites.

**Manque / limite :** Les pertes peuvent détruire les outils et derniers gènes ; sélectivité utile et maintien non démontrés.

**Dépend de :** [F-01](#F-01), [Q-01](#Q-01), [H-06](#H-06) · **Pour renouveler :** [T-04](#T-04)

**Portée des preuves :** Ruptures locales sous quatre variantes x3 graines ; full réincorpore des composites recyclés2/3, protected0/3. Pas de dégradation sélective ni de validation intégrée.

**Références :** [research/MACROMOLECULE_HOMEOSTASIS.md](../research/MACROMOLECULE_HOMEOSTASIS.md), [research/BATCH_31.md](../research/BATCH_31.md)

**Prochain test / décision :** Mesurer exposition locale des fragments et flux utile, pas cycles de formation ; aucune grille ni transfert automatique après refus.

<a id="W-03"></a>
### W-03 — Débouché de la matière composite excédentaire

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** La matière retenue peut être recyclée utilement ou rendue perméable puis exportée en excès.

**Draft local :** RV1 dissocie un P–R isolé, non apparié et sans ligand ; P/R physiques demeurent disponibles à la catalyse, avec leurs symboles et vitesses.

**Manque / limite :** Réemploi sous mouvement normal, évacuation effective et récupération d’un excès retenu non démontrés ; aucun bord ouvert.

**Dépend de :** [W-02](#W-02), [W-01](#W-01), [M-03](#M-03) · **Pour renouveler :** —

**Portée des preuves :** Vrais atomes conservés ; full réincorpore des composites à deux atomes issus de polymères2/3 graines, protected0/3 ; recyclage partiel d’un R observé. Pas de sortie ouverte ou de robustesse intégrée.

**Références :** [research/MACROMOLECULE_HOMEOSTASIS.md](../research/MACROMOLECULE_HOMEOSTASIS.md), [simulator/assembly.py](../simulator/assembly.py), [research/BATCH_31.md](../research/BATCH_31.md)

**Prochain test / décision :** Distinguer cycle futile, piégeage de fragments et réemploi productif ; transférer seulement un candidat justifié sans assouplir la porte RV1.

<a id="W-04"></a>
### W-04 — Pièges, agrégats et parasites

**Concept : esquisse à fermer · Preuve : 0% (non observé).**

**Aboutissement :** Les réactions hors voie ne capturent pas irréversiblement matière, outils ou information essentielle.

**Draft local :** Liaisons/accessibilités réversibles et compétition locale ; aucun tri par identité de bon produit.

**Manque / limite :** Parasites templants et agrégats peuvent être aussi protégés que les bons produits.

**Dépend de :** [C-01](#C-01), [W-02](#W-02), [W-03](#W-03), [R-05](#R-05) · **Pour renouveler :** —

**Portée des preuves :** Fragments/pièges recensés comme échecs ; aucun mécanisme de récupération étayé.

**Références :** [research/BATCH_22.md](../research/BATCH_22.md), [research/HOMEOSTASIS.md](../research/HOMEOSTASIS.md)

**Prochain test / décision :** Introduire des produits hors voie et mesurer extinction, libération et retour de matière.

## Homéostasie des petites espèces

<a id="H-01"></a>
### H-01 — Stocks de petites espèces bornés

**Concept : draft décrit · Preuve : 0% (non observé).**

**Aboutissement :** Chaque précurseur/monomère reste dans un domaine fonctionnel sous alimentation ouverte, même en excès.

**Draft local :** Consommation aval, export des espèces perméables et inhibition réversible par occupation de produit.

**Manque / limite :** Les rétroactions de produit ne sont pas implémentées ; saturation de débit seule insuffisante.

**Dépend de :** [E-01](#E-01), [W-01](#W-01), [W-03](#W-03), [F-03](#F-03) · **Pour renouveler :** —

**Portée des preuves :** Un inventaire fermé et fini ne démontre pas l’homéostasie.

**Références :** [research/HOMEOSTASIS.md](../research/HOMEOSTASIS.md)

**Prochain test / décision :** Excès initial et hausse d’apport figée : vérifier bornes, bilan et activité, avec ablations.

<a id="H-02"></a>
### H-02 — Récupération après pénurie de petites espèces

**Concept : draft décrit · Preuve : 0% (non observé).**

**Aboutissement :** Après un manque annoncé, les pools et flux utiles reviennent sans injection interne d’outils ou de gènes.

**Draft local :** Apport externe rétabli, outils encore actifs et réserves convertibles reprennent la production.

**Manque / limite :** Domaine de récupération et coûts de réserve non mesurés.

**Dépend de :** [H-01](#H-01), [E-03](#E-03), [T-04](#T-04) · **Pour renouveler :** —

**Portée des preuves :** Aucun essai de récupération sous source/puits réels.

**Références :** [research/HOMEOSTASIS.md](../research/HOMEOSTASIS.md)

**Prochain test / décision :** Arrêt/reprise externe préprogrammé, stocks bas, puis délai de reprise et pertes irréversibles.

## Homéostasie des polymères

<a id="H-03"></a>
### H-03 — Protéines/polymères F : population bornée et active

**Concept : esquisse à fermer · Preuve : 0% (non observé).**

**Aboutissement :** Production et pertes de chaque classe F s’équilibrent sans accumulation ni perte d’activité essentielle.

**Draft local :** Frein réversible de l’expression/production de A, combiné au recyclage local et à une protection suffisante.

**Manque / limite :** Sélectivité de la rétroaction et conservation des outils utiles non résolues ; séquestrer ne retire pas la matière.

**Dépend de :** [T-04](#T-04), [W-02](#W-02), [W-03](#W-03), [Q-02](#Q-02), [H-01](#H-01) · **Pour renouveler :** —

**Portée des preuves :** Aucune régulation ni turnover de population F démontré.

**Références :** [research/MACROMOLECULE_HOMEOSTASIS.md](../research/MACROMOLECULE_HOMEOSTASIS.md)

**Prochain test / décision :** Surplus puis manque de chaque outil ; suivre activité, nombre/longueur, matière et retour au régime.

<a id="H-04"></a>
### H-04 — Chaque gène : copies bornées et exploitables

**Concept : esquisse à fermer · Preuve : 0% (non observé).**

**Aboutissement :** Chaque espèce de gène persiste en copies utilisables bornées avec renouvellement et faible risque d’extinction annoncé.

**Draft local :** Frein de copie par contacts réversibles et renouvellement lent de liaisons accessibles ; redondance.

**Manque / limite :** Inhiber sans bloquer les matrices, éliminer sans perdre le dernier gène : compromis non fermé.

**Dépend de :** [R-04](#R-04), [R-05](#R-05), [W-02](#W-02), [H-06](#H-06), [H-01](#H-01) · **Pour renouveler :** —

**Portée des preuves :** Stabilité des backbones initiaux n’est pas homéostasie génétique.

**Références :** [research/MACROMOLECULE_HOMEOSTASIS.md](../research/MACROMOLECULE_HOMEOSTASIS.md)

**Prochain test / décision :** Perturber séparément chaque population de gènes ; mesurer reprise, parasites et extinction.

<a id="H-05"></a>
### H-05 — Population L et taille de frontière bornées

**Concept : esquisse à fermer · Preuve : 0% (non observé).**

**Aboutissement :** Les L libres/insérés et l’aire accessible restent compatibles avec le contenu sans croissance ou effondrement incontrôlés.

**Draft local :** Insertion, dissociation et production modulée par contacts locaux, sans consigne globale de rayon.

**Manque / limite :** Pas de production/perte équilibrées de L ni de recyclage compatible avec la barrière.

**Dépend de :** [S-04](#S-04), [M-04](#M-04), [W-03](#W-03), [H-01](#H-01) · **Pour renouveler :** —

**Portée des preuves :** Un anneau initial stable ne démontre pas ce bilan.

**Références :** [research/HOMEOSTASIS.md](../research/HOMEOSTASIS.md), [research/CELL_ARCHITECTURE.md](../research/CELL_ARCHITECTURE.md)

**Prochain test / décision :** Excès/déficit de L et perte locale sous production réelle ; suivre frontière et confinement.

<a id="H-06"></a>
### H-06 — Protection, redondance et extinction

**Concept : esquisse à fermer · Preuve : 0% (non observé).**

**Aboutissement :** Les perturbations prévues ne font pas perdre irréversiblement une information/capacité essentielle à fréquence inacceptable.

**Draft local :** RV1 compare taux G/F différents et protection des liens dont un site est directement apparié/occupé ; redondance initiale explicite.

**Manque / limite :** Pas de mécanisme sélectif sûr ni de garantie sur un stock rare ; toute dernière information perdue reste perdue.

**Dépend de :** [R-05](#R-05), [W-02](#W-02), [T-04](#T-04) · **Pour renouveler :** —

**Portée des preuves :** Protected conserve4/6/4 G001 à1200, mais réincorporation stricte0/0/0 ; quatre copies initiales, pas test de dernier gène ni de récupération sous perturbation.

**Références :** [research/HOMEOSTASIS.md](../research/HOMEOSTASIS.md), [research/MACROMOLECULE_HOMEOSTASIS.md](../research/MACROMOLECULE_HOMEOSTASIS.md), [research/BATCH_31.md](../research/BATCH_31.md)

**Prochain test / décision :** Diagnostiquer le compromis local et mesurer les faibles effectifs seulement après un réemploi utile sous protection.

## Compatibilité et maintien

<a id="C-01"></a>
### C-01 — Interactions et non-interactions en mélange

**Concept : esquisse à fermer · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Réactions utiles et flux persistent ; collisions parasites restent réversibles ou récupérables sur le domaine visé.

**Draft local :** Affinités/ports locaux sélectifs, états liés masquant les sites ; tester les classes étrangères ensemble.

**Manque / limite :** Contrats globaux EN/EA/EL et nouveaux produits non validés ; pas d’orthogonalité acquise.

**Dépend de :** [F-02](#F-02), [R-04](#R-04), [T-04](#T-04), [M-03](#M-03), [W-04](#W-04) · **Pour renouveler :** —

**Portée des preuves :** Cohabitation d’un sous-réseau MD2, pas de toutes les fonctions.

**Références :** [research/CELL_INTERACTIONS.md](../research/CELL_INTERACTIONS.md), [research/INTEGRATION_TESTS.json](../research/INTEGRATION_TESTS.json), [research/BATCH_35.md](../research/BATCH_35.md)

**Prochain test / décision :** Ajouter les espèces étrangères avec témoin d’encombrement et suivre séquestration, bons/mauvais produits.

<a id="C-02"></a>
### C-02 — Régime physique commun et robustesse numérique

**Concept : draft décrit · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Mêmes lois/température/mouvement pour les fonctions ; résultats compatibles sous raffinement et perturbations annoncés.

**Draft local :** Paramètres figés, contrôle dt/cadence, thermique et fonctions utiles ; index spatial sans feedback.

**Manque / limite :** Raffinements sélectionnés ne prouvent pas convergence globale, futurs assemblages non transférés.

**Dépend de :** [F-01](#F-01), [E-02](#E-02), [O-02](#O-02) · **Pour renouveler :** —

**Portée des preuves :** N1/LT2/MD2 caractérisent des écarts et régressions ; pas certification complète.

**Références :** [research/KINETICS_AND_PERFORMANCE.md](../research/KINETICS_AND_PERFORMANCE.md), [research/BATCH_25_RESULTS.md](../research/BATCH_25_RESULTS.md)

**Prochain test / décision :** Figer horizon et observable physique puis comparer dt, cadence et petites perturbations.

<a id="C-03"></a>
### C-03 — Fermeture fonctionnelle et matérielle complète

**Concept : esquisse à fermer · Preuve : 0% (non observé).**

**Aboutissement :** Tous les composants et outils requis sont réellement fabriqués et utilisables, sans dépendance interne préparée non renouvelée.

**Draft local :** Départ construit amorce les cycles ; les fabrications/expressions se soutiennent ensuite sous une même chimie.

**Manque / limite :** Le graphe C0B se ferme sous hypothèses, pas les mécanismes réels ; nouveaux aides possibles encore non payés.

**Dépend de :** [F-02](#F-02), [S-03](#S-03), [T-04](#T-04), [M-05](#M-05), [Q-01](#Q-01), [W-03](#W-03) · **Pour renouveler :** —

**Portée des preuves :** Audit de graphe conditionnel seulement, pas résultat moléculaire complet.

**Références :** [research/CELL_ARCHITECTURE.md](../research/CELL_ARCHITECTURE.md), [research/FUNCTIONAL_MECHANISMS.md](../research/FUNCTIONAL_MECHANISMS.md)

**Prochain test / décision :** Supprimer chaque fonction en contrôle et démontrer les dépendances par matière effectivement renouvelée.

<a id="C-04"></a>
### C-04 — Cellule maintenue avec renouvellement

**Concept : esquisse à fermer · Preuve : 0% (non observé).**

**Aboutissement :** Sur horizon et perturbations fixés, toutes les fonctions et populations utiles restent bornées, récupèrent et se renouvellent depuis les apports.

**Draft local :** Combiner mécanismes fermés et flux ouverts, puis mesurer chaque famille essentielle et ses pertes.

**Manque / limite :** Plusieurs mécanismes conceptuels et moléculaires restent ouverts ; aucune estimation de délai ou de nombre de lots garantie.

**Dépend de :** [C-03](#C-03), [C-01](#C-01), [C-02](#C-02), [H-01](#H-01), [H-02](#H-02), [H-03](#H-03), [H-04](#H-04), [H-05](#H-05), [H-06](#H-06), [E-03](#E-03), [W-01](#W-01), [O-01](#O-01), [O-02](#O-02) · **Pour renouveler :** —

**Portée des preuves :** Pas de cellule autopoïétique maintenue démontrée ; division hors périmètre.

**Références :** [research/PROJECT_HEALTH.md](../research/PROJECT_HEALTH.md), [research/HOMEOSTASIS.md](../research/HOMEOSTASIS.md)

**Prochain test / décision :** Annoncer plusieurs temps de renouvellement, domaine d’apport, perturbations et critères par espèce.

## Calcul et observabilité

<a id="O-01"></a>
### O-01 — Coût réel et capacité du simulateur

**Concept : draft décrit · Preuve : 25% (sous-cas étayé).**

**Aboutissement :** Le moteur contient l’inventaire utile et simule les renouvellements à un coût compatible avec les campagnes et la visualisation.

**Draft local :** Moteur partagé, arbres spatiaux, profilage et mesures par objectif utile plutôt que vitesse brute.

**Manque / limite :** Taille réelle des outils et temps de renouvellement complet inconnus ; pas de promesse inférieure à dix heures.

**Dépend de :** [E-02](#E-02), [C-02](#C-02) · **Pour renouveler :** —

**Portée des preuves :** Benchmarks et scènes2118 billes, pas renouvellement cellulaire chronométré.

**Références :** [research/KINETICS_AND_PERFORMANCE.md](../research/KINETICS_AND_PERFORMANCE.md)

**Prochain test / décision :** Mesurer temps réel par remplacement utile et coût du flux, sans grossir dt ni ralentir la chimie.

<a id="O-02"></a>
### O-02 — Observation passive, reproductibilité et inspection

**Concept : draft décrit · Preuve : 100% (critère satisfait).**

**Aboutissement :** Cas de référence inspectables avec source figée, état/reprise, mesures passives et distinction préparé/nouveau.

**Draft local :** Observateurs séparés du moteur, checkpoints/PRNG, catalogues vérifiés, campagnes et captures ciblées.

**Manque / limite :** À réévaluer pour toute nouvelle observable ou nouveau mécanisme ; pas de vidéo/relecture avancée exigée ici.

**Dépend de :** — · **Pour renouveler :** —

**Portée des preuves :** Fonction logicielle validée pour les références présentes, pas pour toutes les futures chimies.

**Références :** [research/BATCH_26.md](../research/BATCH_26.md), [research/BATCH_27.md](../research/BATCH_27.md), [research/BATCH_31.md](../research/BATCH_31.md), [research/BATCH_32.md](../research/BATCH_32.md), [research/BATCH_33.md](../research/BATCH_33.md), [research/BATCH_35.md](../research/BATCH_35.md), [research/BATCH_36.md](../research/BATCH_36.md)

**Prochain test / décision :** Conserver les contrôles sans observateur, reprise exacte et signatures à chaque changement concerné.

## Évolution conservée

- Révision1 (2026-10-31) : Demande utilisateur : inventaire conceptuel complet, interdépendances, homéostasie des polymères et compte rendu calibré par lot ; aucune nouvelle preuve dynamique.
- Révision2 (2026-10-31) : RV1 réalise clivage/dissociation et réemploi spontané dans2/3 petits bains full ;12 essais achevés, porte protected refusée, aucun transfert ou maintien. W-02/W-03 sous-cas25%, H-06 inchangé0%. Colonne progrès ajoutée.
- Révision3 (2026-10-31) : MIN1 simplifie l’outil P/R existant à deux unités sous lois MD2 : A12/12 et porte passée ; expression B9 en cours. Draft matériel L ajouté, aucune nouvelle fonction intégrée ou hausse de score anticipée.
- Révision4 (2026-10-31) : MIN1 clos, deux rejeux exacts et loupe bornée ; MIN1R9/9 passe avec F entièrement neufs actifs3/3, sans loi ajoutée. T-05 ajouté puis séparé50%, T-01 court50%, T-03 couplage limité75%. Membrane/L/pertes/information riche restent ouverts.
- Révision5 (2026-11-04) : MIN1M12 essais de transfert sous lois MD2 lancés, aucun résultat final anticipé. MIN1R validé ajouté aux démos avec recensement matériel passif ; pas de changement de palier.
- Révision6 (2026-11-04) : Lot36 indépendant : vrai H/T variable et ports MD2 dans nouveau hook L1. Pilote unique22 produits,16 contacts, sans P/R ni expression ; dette thermique et saut de potentiel première naissance identifiés par loupe passive. S-04 sous-cas séparé25%, aucun maintien ou transfert membranaire anticipé.
- Révision7 (2026-11-04) : Clôture lot37 après interruption :20 nouveaux essais L2 et référence réutilisée, production utile mais deux alarmes thermiques. Aucun palier augmenté. MIN1M9/12, porte non évaluée.
