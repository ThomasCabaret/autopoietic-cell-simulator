# Priorités actuelles — I0 : mécanismes et diversité des outils

Lot62. À 2 118 billes, un facteur 10 ne peut venir du seul gain de
mécanique. Priorité aux deltas H/T par lots et à l'instrumentation du
coût par bloc. Puis réception à plusieurs graines. [Bilan](BATCH_62.md)

Lot61. Les faces coûtent environ 3,5× moins dans le profil. Priorité à
l'énergie des propositions H/T et aux mesures appariées à plusieurs tailles,
avec flux variable pour chiffrer le remappage. [Bilan](BATCH_61.md)

Lot60. CP1 calcule toutes ses forces en CUDA résident. Le profil place
72 % du coût aux ticks de réaction. Priorité à la géométrie et à
l'énumération des faces, en gardant l'ordre d'arbitrage. Puis mesurer
la taille, la cadence et le scénario ouvert. [Bilan](BATCH_60.md)

Lot59. Capture résidente en copie catalysée. Capture coopérative et
barrière CP1 comparées au CPU. Prochaine tranche sur les ports lipidiques
libres, compétitifs et liés, puis intégration dans le pas CP1 et profil.
[Bilan](BATCH_59.md)

Lot58. Interface CUDA validée sur la copie réactive restreinte, topologie
actualisée aux ticks. Priorité à la capture libre, aux ports lipidiques et
à la barrière de CP1, puis au profil des réactions sur le pas complet.
[Critères de clôture](CUDA_COMPLETION.md)

Lot57. CRM1 déplace le voisinage et l'intégration Langevin en CUDA pour le bain
inerte. Prochaine mesure décisive sur un préfixe CP1 avec forces propres et
topologie qui change aux ticks de réaction. Quantifier le coût des échanges
et de la cadence réelle avant de porter les réactions. [Bilan](BATCH_57.md)

Lot56. La piste CUDA est ouverte à la demande utilisateur. CFN1 a un noyau
commun C++/CUDA pour les forces élémentaires. Priorité technique au voisinage,
à l'intégration et aux forces spécifiques sur états résidents. Mesurer le pas
complet et le débit multi-bains face à la référence CPU. La convergence
biologique se juge toujours sur les mêmes critères. [Bilan](BATCH_56.md)

Lot55 : consulter [CURRENT_STATUS](../CURRENT_STATUS.md) et la
[revue Astra](ASTRA_REVIEW.md). FR1 terminé6/6, fast0/3/slow1/3 : refus maintenus,
pas de nouveau taux. OB1 ouvert sans chimie passe6/6 ; prochain transfert :
représentation P/R avec IDs/présence et provenance, bilan L, maintien équipé
redondant sous flux et pertes partielles. L'expressivité reste un choix conceptuel
à dé-risquer ; aucune nouvelle protéine ni sélectivité EN/EA supposée.
Les entrées de lots ci-dessous sont historiques, pas des statuts actifs.

Lot54 : **PT1/RF1 terminés, deux cribles refusés**. PT1 graine1 finit
en chaîne52 ouverte (51 liens), dernier contour valide299.5. RF1 : perte de
l'outil à96.99 sans retour dans graine1 malgré substrats ; récupération en27.23
dans un autre cas, pas de réincorporation stricte et défaut thermique tardif.
**FR1 lancé** :6 essais600, survie des monomères F .01/.001 après coupure
construite,2 travailleurs/1h, audit GF/ligation/catalyse. Lire avant transfert
des pertes dans CP1 ; pas de grille, nouvel outil ou relance des anciennes portes.
Le témoin RF1 épuisé n'autorise pas une conclusion d'extinction des outils.
Voir [BATCH_54](BATCH_54.md), `functional_recovery_status.bat`.
Les mentions « en cours » des lots antérieurs ci-dessous sont historiques.

Lot53 : **CR1 terminé3/3, crible réussi** : cycles30/52/34,
présence tardive.3675/.9625/.94, deux cas>=.5. Aucun seuil ou loi changé.
**PT1 et RF1 en cours**, indépendants :6 essais de transport appariés sur
enceinte construite et9 essais de recyclage de la fonction01 actuelle.
Un travailleur/2h chacun, rapport puis arrêt. Lire ces deux portes avant
transfert ; ne pas augmenter les taux ou adopter un helper sur résultats partiels.
PT1 doit avoir un témoin mobile ; RF1 doit avoir une exposition tardive utile,
sinon distinguer manque de substrat et défaut de fonction. Aucun nouveau gène.
GUI : les trois checkpoints CR1 sont inspectables via Résultats locaux.
Voir [BATCH_53](BATCH_53.md), `selective_transport_status.bat` et
`functional_recycling_status.bat`. Les entrées suivantes sont l'historique des lots.

Lot52 : CR1 **deux cas complets, troisième en cours** à la lecture RG1.
Enceintes simples finales30/52 L depuis dimères isolés, sous lois L inchangées ;
fractions macro tardives.3675/.9625, une seule passe la présence>=.5.
Attendre la troisième avant la porte figée2/3 ; pas de nouveau réglage/horizon.
GUI : **Résultats locaux → CP1 · graine1 · terminé** montre le vrai checkpoint52,
en pause avec zoom/filtres/suivi ; états locaux seulement, aucune trajectoire Git.
Import figé/version vérifiée, reprise physique exacte des checkpoints partiels.
Prochain jalon scientifique : fin CR1 puis transfert/diagnostic justifié selon
résultat. Le coût CA1 est accepté comme point de départ, delta chimique nul.
Voir [BATCH_52](BATCH_52.md), statut `competitive_relaxation_status.bat`.

Audit de complexité : conserver la priorité mécaniste CR1/fermeture ; pas de
nouvelle campagne ni de loi dans cet audit. Toute variante future doit donner
le delta d'atomes, profils de liens, transitions, conventions et contrôles
numériques de [CHEMISTRY_COMPLEXITY.md](CHEMISTRY_COMPLEXITY.md). Le petit
alphabet6 masque une grammaire encore spécialisée ; chercher réutilisation
par assemblage et simplification, surtout avant d'ajouter une fonction.

Lot51 : **BC1 clos**. Courbure locale correcte et souple : theta−.12292rad,
kappa2.35532, sd thermique harmonique.1843. Modes du squelette nu :52 L≈1890,
donc CH1 à1800 ne sépare pas confortablement cette échelle collective. Ce
n'est ni un temps de fermeture prédit ni une annulation du refus CH1.
**CR1 lancé**, mêmes trois initialisations isolées, mêmes lois/paramètres,
horizon8000,2 travailleurs/3h, observateur passif borné et rapport puis arrêt.
Lire `competitive_relaxation_status.bat`. Interpréter cycles finaux/durée
observée, bouts et températures ; pas d'allongement automatique ni refroidissement.
Si refus, une variante mécaniste justifiée au plus avant réexamen, pas grille.
GUI39 historique recertifiée, pas de promotion CP1. Diversité, information,
protection/régulation et flux/export restent des gaps. Voir [BATCH_51](BATCH_51.md).

Lot50 : **CP1 dynamique intégré**, forces/deltas/naissances cohérents,
coût force optimisé15–16×→1,81–1,85×. **CC1 clos6/6**, porte refusée :
température6/6, association3/3, mais intégré1 ouvert à froid. **CH1 clos4/4** :
intégré1 récupère94,33% de fermeture tardive, G2/F5/L22 ; isolés forment chaînes
30/52/34 mais aucun cycle final. Porte CH1 refusée sur fermeture isolée.
**CE1 passif** : les cinq paires d'extrémités finales sont loin du seuil.25,
même la chaîne52 ; pas une preuve d'absence d'occasions antérieures.
Prochain objectif : diagnostiquer courbure/flexibilité locale et chronologie
des rencontres/ruptures, d'abord sur instantanés et petits contrôles motivés.
Ne pas prolonger aveuglément ou augmenter les taux. Aucun calcul actif,
CF1 reste pausé. GUI39 additive EG1/EN1/CB1, CP1 non promu. Diversité,
information riche, protection/régulation et flux/export restent des gaps.
Voir [BATCH_50](BATCH_50.md).

Lot49 : **EL1 clos exact** localise surtout les apports des formations de
contacts, pas ceux des échanges filtrés. **RP1 refusé** sur la séquence cible,
mais FS1 constate encore motifs F01 et catalyse tardive : ne pas assimiler perte
F001 et extinction fonctionnelle. **CF1 en pause scientifique**, deux préfixes
1345/2033.5,4 essais non démarrés,~4M propositions chacun et1/0 contacts pour75 L.
Ne pas reprendre cette cohorte : attraction libre additive incompatible avec
liaison saturable, coût démesuré et perte de frontière. Aucun gate final calculé.
**CP1 statique** : potentiel compétitif à capacité locale bornée, binaire exact,
gradient vérifié ; sur les mêmes12 contacts sélectionnés par snapshot, coûts
médians209/99 deviennent−1.925/−1.697. Pas installé dans la simulation.
Prochain lot : intégrer le potentiel et son delta local : termes modifiés jusqu’au second rang,
partitions pouvant nécessiter le troisième ; vérifier coût, molécules L libres et insertion avant nouvelle
cohorte. Pas nouvelle constante, thermostat ou outil pour masquer cette dette.
Aucune campagne active ; GUI39 demeure sur les recettes EG1/EN1 historiques.

Lot48 : **EN1 clos3/3 refuse**, production conservée mais insertions0/0/2,
une graine chaude/ouverte. Ne pas sélectionner un dt favorable ni relancer des
graines pour sauver EG1. Deux graines sans face de capture admissible et sans
échange accepté ; interprétation cinétique, pas verdict numérique automatique.
**EL1 en cours**, rejeu EN1 s2, fenêtre2100–2200 : bilan des commutations de
contacts hors échange et partition thermique, source figée,2700s puis arrêt.
**RP1 en cours**, trois graines d'un même garde local
paired_edge, taux RV1 protected inchangés ;1 travailleur/1h puis rapport et arrêt.
Aucun transfert vers EG1 ni nouvelle enzyme. Lire contact_heat_status.bat et
pair_protection_status.bat. Décider après leurs rapports ; pas de grille de taux.
GUI39 montre les3 EN1 refusés et avertit dans la fiche EG1. Diversité, information,
protection/régulation et flux/export restent des risques conceptuels. Voir BATCH_48.

Lot47 : **EG1 clos3/3 passe** : tenue94–95%, température proche.08,
insertions1/0/2, production G/F/L conservée. GUI36 choix, nouveau raccourci EG1
« Intégration compacte · échanges stabilisés » ; CB1 et ses défauts conservés.
**EN1 en cours** : dt/2, mêmes cadences physiques de réaction/observation,
3 graines2400,2 travailleurs/3h, rapport puis arrêt. Lire exchange_refinement_status.bat.
Pas d'adoption générale ou de grille si refus : interpréter occasions et stocks.
**RX1 clos2/2 exacts** : protected retient les F déjà polymérisés liés94% du temps
contre74% full ; capture directe isolée négligeable dans ces trajectoires.
Prochain choix conceptuel : protection de liaison par appariement local cohérent
plutôt que toute occupation ; comparer ses risques outils actifs/fragments, sans
l'implémenter comme acquis ou transférer protected refusé. Débit/pertes/export,
répartition par espèce et protection de l'information restent des gaps. Voir BATCH_47.

Lot46 : **CX1 clos3/3 passe**, production avec frontière stable mais aucune
insertion. **CW1 clos3/3 refuse** :5/14 insertions sur2 graines, mais la troisième
chauffe (T tardive.3764) et s'ouvre. Pas d'autre grille de largeurs. **EG1 en cours**,
3 graines2400,2 travailleurs/3h : filtre énergétique local des échanges, mêmes
taux/bruit/largeur, pas de nouvel outil. Lire energy_exchange_status.bat ; rapport
puis arrêt, aucune adoption automatique. Si perte d'insertion ou chaleur persistante,
interpréter propositions/deltaU avant changement, revoir le mécanisme si nécessaire.
**PI1 clos15/15 refuse** : les produits F01 sont exclus de capture G–F par le degré
local ; un précontrôle bloque la répétition. Prochaine construction conceptuelle
indépendante : production saturée + pertes/recyclage/export avec protection de
chaque espèce, pas une inhibition présumée. H-03/H-04 restent gap. GUI CB1 inchangée
biologiquement,33 démos Langevin, limites visibles. Voir BATCH_46.

Lot45 : **CB1 clos9/9**, analyse récupérée sans recalcul après perte du
flag --compact. Une vraie chaîne nourriture→F entier→L→frontière est observée
en graine1 ; fermeture tardive0/.9417/0, porte refusée. Ne pas relancer CB1.
**CL1 terminé**, six billes : premier échange +6.0243 de potentiel de ports,
puis extrémités jamais éligibles à la jonction dans la fenêtre observée.
**CX1** trois contrôles sans échange en cours, deux finissent stables ;
**CW1** trois suivis dock_width.6 au lieu de.3, tout autre taux/bruit fixe,
pilote100 stable. Lire exchange_ablation_status.bat et wide_ports_status.bat.
Attendre ces comparaisons avant d'ajouter une loi ou un outil ; pas de grille
de largeurs. GUI désormais sur CB1 « Intégration compacte · défauts connus »,
graine0 par convention,33 choix et échecs visibles. Voir BATCH_45.

Lot44 : **BI1 terminé9/9, insertion refusée**, G/F0 dans tous les cas,
L actifs3/2/7 ; stocks restants et très faible exposition admissible. Ne pas
relancer BI1 ou augmenter un taux sans diagnostic. **CB1 lancé9 essais** :
frontière52 L dimensionnée pour outils courts,302 billes/boîte22, short_length.92
explicite, témoins noL/nosynthesis à2400. Lire compact_transfer_status.bat puis
stocks, occasions et taux de production. Si accès toujours faible dans un bain
productif, comparer un mécanisme associatif local ; pas d'insertase ajoutée.
GUI : MX2 validé désormais au menu « Chimie mixte · outils et lipides » ;
MIN1M reste la vue avec membrane. M-04 recalibré75→25, ancien75 concernait L
préparés. Voir BATCH_44 ; les états en cours ci-dessous sont historiques.

Lot43 : **MX2 clos12/12, neuf conditions passent**. Coopératif G12/13/14,
F14/12/15,L24/23/23 ; F alimentaires→L sur2/3, activité non uniformément
supérieure et stocks quasi épuisés. Ne pas relancer MX2. **BI1 lancé9 essais** :
vrais L fabriqués dans un paquet intérieur près d'une frontière construite219 L,
636 billes au total, même chimie/portage local. Pilote100 stable,1 L intérieur,
aucune insertion encore. Lire boundary_transfer_status.bat puis bilan stocks,
occasions de contact et contour ; si défaut, loupe motivée avant tout taux.
Après transfert : réparation/remplacement, flux ouvert et régulation/protection.
Les démos restent MIN1M validé ; aucun maintien anticipé. Voir BATCH_43.md.
Les mentions de campagnes en cours ci-dessous sont historiques.

Lot42 : **MX1 clos12/12, porte refusée G/F**, mais transfert F alimentaire→L
sur2/3. Audit : stocks P/R abondants restants et production tardive ; ne pas
conclure à une impossibilité ou augmenter aveuglément la nourriture. Loupe
sélectionnée : déliaison suivie de recapture rapide. **MX2 lancé12 essais**,
coopération locale et références au même horizon2400, sans nouveau taux/outil.
Lire cooperative_synthesis_status.bat puis rapport complet stocks/fenêtres/
préfixes ; pas de grille supplémentaire avant interprétation. Ensuite vrais
L→frontière et boucle de maintien sous pertes/perturbations. Suivre désormais
CAMPAIGN_CALIBRATION.md ; les états « MX1 en cours » ci-dessous sont historiques.

Lot41 : **CT1 clos9/9, porte passée**, mais activité non uniformément meilleure
(opérations médianes9→3). Ne pas relancer ni adopter globalement. **MX1 lancé12
essais** : un même pool de sites P/R/H/T et vrais produits, sans nouvelle protéine.
Lire mixed_synthesis_status.bat puis rapport complet. Chercher F entièrement
alimentaire→L→contact latéral dans les mêmes bains ; si absence, séparer stock
épuisé, capture bloquée et chimie inéligible avant réglage. Ensuite insertion/
rétention (barrière segmentaire distincte du core F/L) et pertes/flux. Les démos
restent MIN1M validé, pas MX1 en cours. Voir BATCH_41.md ; les états antérieurs
« CT1 en cours » ci-dessous sont historiques.

Lot40 : **MIN1M clos12/12, porte passée**. Les trois active refont des F
entiers actifs avec membrane ; témoins nogene négatifs. Démo désormais au menu,
par défaut graine0 conventionnelle. Ne pas relancer MIN1M ni les grilles L2/L3.
**CT1 lancé9 essais** : transférer la courbure de capture H/T à P/R avant le bain
mixte. Lire capture_transfer_status.bat et rapport automatique ; aucune adoption
avant interprétation. Ensuite compétition P/R/H/T et usage réel des produits,
barrière de rétention/insertion, énergie sous flux. Les états « en cours »
ci-dessous sont historiques. Voir BATCH_40.md ; pertes/homéostasie restent ouverts.

Clôture lot39 : L4 terminé3/3 sans erreur, préfixes exacts, refroidissement
après production (T350–400.076/.092/.077). Aucun nouveau calcul L4 ni autre
réglage thermique à lancer. L3 reste refusé à100 ; les suivis sont sélectionnés.
Priorité : dernier témoin MIN1M (11/12), clôture/visibilité du transfert validé,
puis vraie cohabitation P/R/H/T et produits L utilisables avec même capture.
Mesurer la puissance sous flux continu et le repliement de F nouvellement
exprimés ; une queue froide après stocks finis ne suffit pas.

Lot39 : L3 clos18/18, deux critères thermiques refusés ; ne pas changer de
raideur ni relancer sa grille. Trois suivis L4 à400 conservent les mêmes lois
et contrôlent leurs préfixes L3. Lire lipid_tail_status.bat puis rapport complet :
séparer transitoire productif/refroidissement et chaleur entretenue avant nouvelle
règle. MIN1M10/12 en cours, aucun échec ; attendre les deux derniers témoins.
Après ces lectures : compatibilité commune P/R/H/T, énergie de nouveaux F et
insertion/rétention. Une queue froide de stocks finis n’est pas l’homéostasie.

Lot38 en cours : L3 compare pose construite native et courbure de capture
dérivée du potentiel,18 nouveaux essais et3 références L2 réutilisées. Ne pas
changer les seuils thermiques de L2. Lire lipid_curvature_status.bat puis rapport
complet avant autre correction. MIN1M10/12 : trois active refont des outils
entiers actifs avec membrane, deux témoins restants. Pas de relance MIN1M/L2.
Après L3 : interpréter capture/énergie, puis tester une vraie chimie P/R/H/T
commune et l’insertion ; ne pas additionner des succès séparés en viabilité.

Lot37 clôturé : L2 terminé20/20 sans erreur, crible thermique refusé malgré
production19/21/21 et témoins négatifs. Ne pas relancer la grille ni promouvoir.
MIN1M9/12 en cours, zéro erreur, porte complète à attendre. Travail indépendant
justifié : séparer énergie de préparation F et transitions de capture avant
correction mécanique dérivée, sans nouvelle protéine ni changement de thermostat.

**Lot36, travail indépendant achevé : L1 fabrique H/T, avec dette thermique.**
Nouveau hook et vrais partenaires variables, même F01 préparé ; un pilote22
produits,16 contacts latéraux. La loupe première naissance localise +31,416 de
potentiel à positions inchangées, surtout core F/L et axe H–T : résoudre cette
transition avant une cohorte L1. Ne pas promouvoir ou relancer une grille de taux.
MIN1M continue avec ses sources figées ; lire son rapport complet en priorité
avant campagne longue. Ensuite L1 : coût énergétique local, contrôles dispersés,
compétition P/R/H/T et insertion. MD2 et démos gardent leurs lois antérieures.

**Lot35,4 novembre : MIN1M en cours,12 essais figés, aucune nouvelle loi.**
Lire membrane_renewal_status.bat et le rapport automatique avant une autre
campagne. Même boucle courte G01/F01 dans le bain MD2, avec noL/split/nogene.
Nouveaux F entièrement alimentaires actifs + tenue de membrane dans les mêmes
graines sont exigés. Arrêt après cohorte quelle que soit la porte, pas de grille.
Les progrès MIN1R acquis sont désormais visibles dans la GUI, trois graines.
Si transfert réussi : construction H/T→L et insertion sous lois communes ;
sinon diagnostic contacts/dilution/membrane. Pertes, homéostasie et information
riche restent des risques ouverts. Les clôtures ci-dessous sont historiques.

**Clôture MIN1R :9/9, zéro erreur, critères passés, aucun calcul actif.** Des
F01 entièrement refaits depuis nourriture sont actifs3/3 sous MD2 dans le
petit bain ; split réussit2/3, nogene négatif3/3. Prochain jalon : transférer
le même gène/outil court dans le bain membranaire MD2 sans nouvelles lois et
avec mesure de remplaçants entiers. Puis fabrication L selon le draft et
compatibilité pertes/flux, sans appeler maintien cette boucle en stocks fermés.
L'expressivité F-02 et l'information riche restent ouvertes. Voir BATCH_34.md.

Lots33–34 : MIN1 terminé21/21, B non robuste et aucun F entièrement refait.
Deux rejeux exacts avec loupe pointent la rareté du double motif F, pas une
ligation lente après ce motif. MIN1R compare maintenant départ avec un F01,
mêmes sites déliés et sans gène :9 essais figés, aucun changement de lois.
Première graine positive vers un F entièrement neuf actif ; lire toute la
cohorte via renewal_status.bat avant transfert au grand bain ou nouvelle loi.
T-05 distingue ce remplacement ponctuel de T-04, tous les outils de la cellule.
L/déchets/homéostasie/information riche restent ouverts. Aucun autre balayage
ni nouvelle machine ajouté. Les passages « B en cours » ci-dessous sont historiques.

Lot32 MIN1 : A12/12 achevé, zéro erreur, F01 préparé fabrique G/F sous les
lois MD2, plus petit que F001 ; témoins déliés/bonus ablaté négatifs. Porte
passée, B9 expression01/001/sans gène en cours. Lire minimal_tool_status.bat
et BATCH_32.md ; ne pas anticiper son transfert ou lancer une autre grille.
Après B, essai aval dans le grand bain si justifié et choix de voie L :
LIPID_CONSTRUCTION_DRAFT.md décrit réemploi du même co-recruteur H/T, ainsi
que ses incompatibilités possibles. Aucun nouveau rôle/gène ni synthèse L
adopté ; F-02 reste ouvert. RV1 conserve sa porte refusée.

**Clôture RV1 :12/12, zéro erreur, porte refusée, B4 non lancé, aucun calcul
actif.** Full prouve le chemin matière polymère→P/R→composite→squelette sur2/3
graines ; protected donne0 réincorporation stricte malgré survie G et activité.
Ne pas lancer B ou une grille de taux à la main. I0/diversité et L reste le
plus grand trou conceptuel, maintenant que le recyclage a une réalisation
locale. Si l'on reprend RV1, motiver une loupe/exposition des fragments et
mesurer le flux utile plutôt que le nombre de cycles monomères. Lire BATCH_31.md.

Historique du lancement lot31 : RV1 choisit le plus petit contre-test du débouché des polymères :
rupture de squelette puis dissociation locale P/R réutilisables. Implémentation
et trajet contrôlé testés ;12 comparaisons et4 transferts conditionnels figés,
superviseur actif, voir BATCH_31.md et recycling_status.bat. Ne pas changer
ses taux ni lancer une seconde grille avant lecture. Les démos restent MD2.
Lire A complète et sa porte, puis B seulement si justifié : matière réellement
réincorporée, gènes encore présents et catalyse préservée. Après cette décision,
revenir à I0/diversité et L ou motiver une loupe locale si le recyclage échoue.
Pas de nouvelle machine ; pas d'homéostasie ni d'export ouvert acquis.

Lot30 : choisir les prochains travaux depuis le [registre global](CELL_CHECKLIST_COMPACT.md)
et CONCEPT_FIRST.md, pas seulement le dernier test local.42 sous-buts et leurs
cycles de renouvellement sont explicités. Deux verrous conceptuels immédiats :
fonctions distinctes/fabrication L (F-01/F-02/S-04), et régulation des polymères
avec recyclage, débouché de matière et protection des gènes (W-02/W-03/H-03/H-04/H-06).
MACROMOLECULE_HOMEOSTASIS.md expose des familles de solutions et leurs échecs,
pas une solution déjà choisie. Pas de nouvelle campagne, protéase ou régulateur.
Chaque lot actualise les points affectés et ajoute ceux nouvellement découverts,
puis rend le tableau compact et le prochain test discriminant.

Lot29, priorité corrigée à la demande utilisateur : établir comment des petits
assemblages peuvent porter des fonctions différentes sous des lois communes,
avant de reprendre des réglages techniques de duplication. Lire
[FUNCTIONAL_MECHANISMS.md](FUNCTIONAL_MECHANISMS.md). Le co-recrutement P/R
existe, mais la capture actuelle ne distingue pas P_G/P_F ni R0/R1, L n'est
pas fabriqué et les préférences angulaires F0/F1 de MD2 sont identiques.
Un premier assembleur local ne suffit pas à prouver un répertoire d'outils.

1. I0 : choisir une famille de petits catalyseurs ou une architecture polyvalente
   avec deux productions distinctes utilisables, même alphabet/lois/énergie.
   Prévoir bon/mauvais produit, fond, turnover, libération et transfert réel.
2. Puis expression du même outil et usage de ses produits pour son renouvellement,
   avec le test aval de fabrication L. Les nouvelles machines nécessitent la
   proposition et l'accord prévus ; aucune n'est ajoutée dans ce lot de notes.
3. Reprendre T9 en obstacle d'intégration si la copie bloque une fonction déjà
   établie. Garder MD2 et les copies comme références, pas nouvelle grille ici.

Tailles des gènes/outils inconnues. Le mécanisme détermine leur dimension ;
24 reste un scénario de budget. Atlas corrigé, aucun changement du moteur.

## Historique avant recentrage fonctionnel

Lot28 documentaire : atlas généré disponible via metabolism.bat, trois gènes
visés et déchets/recyclage manquants explicités, aucune loi changée. T9E est
désormais terminé12/12 sans erreur dans la cohorte corrigée ; porte refusée
(F en expression non amélioré), quatre transferts non lancés, aucun calcul actif.
La prochaine recherche reste l'interprétation des contacts/ligations et de la
constructibilité sous T9, pas une nouvelle grille automatique. Voir BATCH_28.md.

## Historique du lancement T9E

Lot27 : T9E en cours sous lois figées,12 essais de finition/interférence puis
au plus4 transferts sélectionnés automatiquement. Ne pas modifier le candidat
en cours ni lancer une autre grille. Lire `expression_status.bat`, BATCH_27.md
et BATCH_27_PLAN.md. Erreur IO du premier job conservée, relance technique
explicite sous nouvelle recette ; aucun succès chimique déduit des pilotes.
Priorité immédiate : analyser A/porte/B puis décider, pas une intervention
manuelle entre les étapes calculables. Les démos restent MD2/Langevin.

MD2 terminé15/15,0 erreur. La fermeture du grand bain progresse sur trois
graines ; F nouveau reste nul, même complet encore apparié. Le stock global
de F composites monomères reste194/191/204 : ne pas supposer son épuisement,
ni confondre ce stock global avec l'accès local. Voir BATCH_25_RESULTS.md.

Lot26 : neuf presets MD2 exacts promus dans la GUI,12 références conservées,
21 choix natifs vérifiés. `visualizer.bat` → Démos → État actuel · bain intégré
ouvre la graine2 illustrative, avec ses limites affichées. Aucune nouvelle
loi ou campagne dans cette consolidation. Voir BATCH_26.md.

1. T9 : séparer rencontres, éligibilité G/F, attente de ligation et finition
   des fragments dans le bain actuel ; comparer les gardes locaux avec les
   outils complets pour éviter leur séquestration. Retirer le seul garde
   monomère n'avait pas résolu le garde indépendant degré(F)=0.
2. Réparation/insertion : garder le cas à sondes graine1, ouverture durable224
   après échange223,61 (association, pas causalité prouvée). Loupe localisable
   et comparaison des produits de l'échange, sans réparer un contour global.
3. Diversité des outils, fabrication de L et maintien avec flux/homéostasie :
   verrous de recherche toujours ouverts, pas simples tâches techniques garanties.

Langevin et les contacts MD2 sont la base explicite des nouveaux essais.
Anciennes recettes inchangées. Nouvelle machine fonctionnelle seulement après
proposition et accord utilisateur ; pas de nouveau gène par défaut.

## Historique avant lecture complète MD2

Lot25 : motif local cohérent implémenté, porte locale passée3/3, six témoins
conservés,15 essais de transfert lancés sous sources figées. Langevin et tous
les taux de réaction restent identiques. Suivi `coherent_contacts_status.bat` ;
voir [plan](BATCH_25_PLAN.md), [bilan](BATCH_25.md). Pas d'adoption générale avant
lecture de la cohorte, pas de balayage de raideur par fonction.

Les trois V8 nouvelles s'assemblent depuis molécules isolées ; continuité
observée accrue sur trois graines, première fermeture plus tardive sur une.
Les
sondes, insertion et trois bains J3 restent à lire. Priorité : vérifier que
le raccordement géométrique préserve échange/rétention et restaure le grand bain,
puis revenir à T9. Les réussites de paire préparée ne prouvent pas une membrane.
Aucun nouveau type/outil/gène, aucune nouvelle dépendance causale.

## Historique après MD1

LT2 achevé16/16,0 erreur. [Bilan complet](BATCH_23_RESULTS.md) : le grand bain
régresse dans deux graines, malgré les progrès micro. Langevin reste la base
de travail ; ne pas ralentir le mélange pour cacher les défauts des réactions.

Lot24 MD1 : cinq contrôles précoces à80 achevés5/5 sans erreur, plus une loupe passive sélectionnée.
Le contact qui ouvre durablement la graine0 se perd aléatoirement à40,53 avec
des longueurs presque au repos mais des ports déjà très désalignés : q1,28
contre seuil de recapture0,0625. Aucune recapture dans la fenêtre suivante.
Le problème identifié est une incohérence entre géométrie liée et capture libre.
Voir [plan](BATCH_24_PLAN.md), [diagnostic](BATCH_24.md),
`membrane_diagnostic_status.bat`. Aucun nouveau gène ou outil.

1. Tester un contact local cohérent MD2 après le bilan MD1, en
   réutilisant la géométrie H/T des ports. Ne pas rendre globalement les liens
   irréversibles sans tester échange/insertion et assemblage depuis molécules libres.
2. Transférer ce motif aux petites membranes et au grand bain, avec contrôles
   de pas et de renouvellement. Aucune conclusion à partir de la seule graine2.
3. Reprendre T9 : finition et concurrence des fragments, puis fonctions diverses
   et fermeture constructive. Nouvelle machine fonctionnelle soumise à proposition
   et accord utilisateur, jamais ajoutée par défaut.

## Historique — transfert LT2 avant lecture complète

30 octobre2026 : demande utilisateur de voir Langevin dans les microdémos et
les scènes actuelles. Douze choix GUI (six paires), conditions et enjeu explicites.
LT2 lancé16 essais, deux travailleurs, pointeur séparé demo_motion_campaigns.
Les six essais micro principaux et leurs trois contrôles fins sont achevés ;
les sept tâches J3 intégrées restent à lire.0 erreur au bilan9/16.
Voir [plan](BATCH_23_PLAN.md), [bilan progressif](BATCH_23.md),
`demo_motion_status.bat`. Pas d'adoption globale avant cette lecture.

Progrès sélectionnés : T7 conserve1 G libéré ; C3B1 passe2G/3F à4G/5F et13 à29
composants catalysés utilisés ; V8 ferme plus tôt sur cette graine. Écarts aux
pas fins et échauffement mesurés, pas de robustesse déduite d'une graine.
Ne pas changer les sources/lois du lot en cours. Aucun outil supplémentaire.
À la clôture, interprétation de compatibilité puis T9 ; pas de grille inerte
ou de réglages de rendement ajoutés automatiquement. Les références browniennes
restent accessibles et le défaut existant est conservé.

## État après LT1, avant la demande de transfert visuel

29 octobre2026, clôture lot22 : P10/MIX1/MIX2 achevés38/38, analysés avec
contrôle des sources ; LT1 achevé6/6, sans erreur. Aucune de ces campagnes
n'est encore active. Voir [bilan](BATCH_22.md) et [plan](BATCH_22_PLAN.md).

Langevin0,1,m1,dt0,005 est un candidat expérimental, pas le nouveau défaut.
Sous les réactions P10 inchangées, F10 exacts1/3/1 deviennent7/7/6, mais
G10 exacts1/1/0 deviennent2/0/3. Les fragments G sont de véritables matrices
concurrentes :82–86% des ligations du témoin,64–86% avec Langevin. Plus de
transport ou de stock seuls ne résolvent donc pas le verrou génétique.

1. Concevoir le prochain motif local T9 de finition/réutilisation ou de
   limitation des matrices courtes, avec ablation et contrôle de séquestration
   des outils complets. Pas d'accès à la longueur cible/séquence globale.
2. Test borné depuis un seul G long : copies exactes libérées et réutilisables,
   générations, consommation/parasites ; garder les vrais produits incomplets.
   Ne pas lancer une nouvelle grille de doses ou de mouvements inertes.
3. Avant adoption d'un mouvement : transfert membrane/catalyse et couplage
   sous lois communes. Les démos conservent leur brownien de référence.

Une nouvelle machine processive/polymerase peut être proposée, avec coût complet
gène/expression/renouvellement et solutions plus simples, mais attend le feu
vert utilisateur. Aucun nouvel outil n'est ajouté par défaut. Deux changements
conceptuels sans transfert ni diagnostic nouveau imposent une révision du modèle.

## Historique avant analyse des campagnes

29 octobre 2026 : variantes de mouvement autorisées. MIX2 compare Brownien,
Langevin inertiel et DPD sur coût réel par objectif, avec contrôles thermiques,
pas numérique et référence brownienne appariée. Voir BATCH_21_PLAN.md/BATCH_21.md.
Campagne bornée18 essais, deux travailleurs, pointeur séparé motion_campaigns.
Ne pas adopter un modèle sur un seul seuil local ni oublier le surcoût des
paires. Le choix scientifique attend la cohorte, puis les réactions/membrane
doivent être revalidées avant transfert. Les démos gardent leur chemin brownien.

## Priorités précédentes — MIX1 et P10

29 octobre 2026 : demande utilisateur de caractérisation de la dispersion et
du mélange sans chimie. MIX1 tourne séparément avec un travailleur,200 molécules
dans une moitié de boîte, deux températures, contrôles de répulsion, taille et
cadence. Voir BATCH_20_PLAN.md/BATCH_20.md ; suivi `mixing_status.bat`.
P10 continue avec son dossier et ses commandes propres, sans changement de lois.
Lire ces deux diagnostics avant de choisir une correction de transport ou T9.
Ne pas confondre remplissage global, renouvellement des voisins et contacts
chimiquement éligibles. Aucune inertie, convection ou nouvelle protéine ajoutée.

## P10, fidélité globale des populations

29 octobre 2026 : demande utilisateur prioritaire après examen de la copie.
Lot19 lancé : un seul G de dix symboles, stock abondant de dimères libres,
distribution complète des séquences et longueurs au fil du temps. Copie seule
et expression seule, trois graines chacune ; contrôles de réserve/volume et
de dilution, dix essais à3200. Voir BATCH_19_PLAN.md et BATCH_19.md.
Lire la cohorte avant de modifier T9 : abondance initiale ne garantit pas une
réserve libre tardive, et la fidélité locale stricte ne garantit pas l'amplification.
Aucune nouvelle protéine ou loi. La synthèse depuis P/R et la membrane restent
hors de ce diagnostic ; ne pas appeler ce lot une nouvelle cellule intégrée.

## Priorité précédente — examiner les démos du projet

29 octobre2026, précision utilisateur : le minimum de visualisation est suffisant
pour passer aux démos représentatives. GUI2 ajoute le catalogue : bain J3 intégré
à2118 billes (graines2/0/1), circuit matériel C3B1, copie T7 et membranes V8.
Voir ../docs/DEMOS.md. Chaque fiche distingue départ préparé, observation et
limites ; les paramètres physiques restent ceux des sources de recherche.

Vidéo/relecture avancée/courbes sont reportées et ne doivent plus retarder
l'examen du résultat global. Prochaine étape : retours visuels sur ces scènes,
puis reprise ciblée de la recherche (T9) selon les mécanismes observés. Aucune
nouvelle loi ou campagne chimique introduite dans ce lot de catalogue.

## Priorités de recherche précédentes — lot18

**Mise à jour de clôture : N1 achevé6/6**, voir BATCH_17_RESULTS.md. Pas d'alerte
médiane prospective, donc N2 ne doit pas être lancé par le suivi. La baisse
cumulée d'incorporation et une frontière fine dégradée empêchent de certifier
la convergence. Prochaine priorité T9 : recapture/finition avec témoin de
séquestration des outils complets. Le diagnostic exact des six motifs du lot18
montre que retirer le seul garde monomère ne débloque pas les fragments F.
Automatiser la comparaison bornée après choix de ce motif, pas sa conception.

## État au début du lot18

N1 reste en cours,2/6 achevés au premier contrôle, aucune erreur. Ne pas changer
ses lois, graines ou horizons. Le suivi AUTOMATED_EXPLORATION.md / BATCH_18_PLAN.md
attend la cohorte entière, analyse puis déclenche N2 seulement si l'alerte de
raffinement fin annoncée existe. N2 sépare cadence réaction/mécanique, six essais
au plus ; sinon arrêt pour choix T9. Aucun balayage de densité ajouté.

La mécanique reste au vrai dt ; reaction_every est une cadence numérique,
défaut5 exact à la référence. L'analyse des résultats anciens garde leurs
sources archivées. À la fin de N2 ou en absence d'alerte, décision mécanistique
et T9/finition avec contrôles de parasites ; pas d'autre grille par défaut.
Ne pas confondre gain d'automatisation et maturité chimique.

## Priorités lot17, historique

J3 terminé21/21. Bain K16 :331/401/313 actes catalytiques,18/18/26 produits
incorporés, G1/1/0 et F0/1/1 nouveaux libérés. F exprimé actif et produit utile
en graine2 ; pas de même essai réunissant nouveau G et cet usage aval. Voir
BATCH_16_RESULTS.md. La catalyse compte face à l'ablation, mais le renouvellement
reste rare et la membrane fragile. Aucune nouvelle grille de densités.

Priorité N1 : vérifier dt/2 puis dt/4 sous mêmes lois, même horizon1200,
grille d'observation0,5, référence J3 réutilisée. Six essais, réaction5dt :
convergence temporelle conjointe seulement. BATCH_17_PLAN.md fixe lecture et
alertes avant les nouveaux résultats. Ensuite T9/finition/recapture locale
avec contrôles de séquestration ; pas d'exception par séquence complète.

Synthèse L, bibliothèque distincte, génome long, flux externe et homéostasie
restent des verrous. Ni maintien ni durée de demi-renouvellement démontrés.

## Priorités lot16, historique

J2 achevé12/12 : compact préparé incorpore1/2/2, grand préparé0/0/1 ; aucun
G/F nouveau complet. Le domaine compte, sans être une solution suffisante.
Priorité J3 : inventaires construits×1/8/16 dans la vésicule réelle, appariés
sans L, et ablation du boost àK16.21 tâches1200, lois figées, mêmes trois graines.
Voir BATCH_16_PLAN.md. Exiger flux incorporé et nouveaux G/F ; copies initiales
et fonctions distinctes ne se confondent pas. Revoir les motifs si K16 échoue,
pas une nouvelle arborescence de densités.

La frontière alimentée au bord du monde est la cible décrite dans OPEN_BOUNDARY.md,
pas encore un mécanisme livré. Flux réglé n'implique pas concentration locale
fixée ; pas de plafond de particules final imposé. Maintien, dt, diversité et
synthèse de L restent ouverts, sans délai de renouvellement prédit.

## Priorités J2, historique

J1 terminé12/12 : incorporation froide préparée3/3 mais aucun F nouveau ; un
témoin délié exprime un F actif. Dans les6 bains : fabrication préparée13/13/11,
aucune incorporation et frontière fragile. Monomères présents mais plus éloignés
du gène, aucun fragment F délié non cible dans les bains. Ne pas accuser L ni
ajouter un recycleur avant contrôle spatial.

Priorité J2 : grands/petits mondes sans L, mêmes paquets/PRNG initiaux, préparé
et délié, trois graines à1200. Voir BATCH_15_PLAN.md. Décider ensuite entre
densité/organisation et effet de frontière. L'homéostasie faible est désormais
explicite dans HOMEOSTASIS.md ; inventaires bornés par un stock fini ne la
prouvent pas. T9, convergence dt, bibliothèque et production L restent requis.

## Priorités J1, historique

GKA terminé6/6 avec rejeu primaire exact. Deux froids n'ont aucun motif doublement
apparié observé ; le troisième forme une liaison, pas un F complet. Aucun taux
supplémentaire justifié. Cycle réel200/15 corrigé dans les anciennes notes.

Priorité J1 : outil initial construit contre même géométrie déliée, mêmes lois,
même quantité de matière, trois graines avec/sans membrane à1200. Pilote200 :
3 dimères contre0, aucune incorporation. Demander produit incorporé et nouveaux
F/G, distinguer F préparé et exprimé. Voir BATCH_14_BOOTSTRAP.md. Aucun suivi
froid3200 lancé. T9 si fragments ; sinon diagnostiquer dilution et transport
dans le bain, puis convergence dt et diversité/synthèse L sous lois communes.

## Phase de diagnostic GKA, historique

GKA : diagnostiquer la reconnaissance et la ligation à froid avant tout réglage.
Six témoins J0 natif/froid rejoués à400, instrumentation sans rétroaction,
comparaison exacte aux originaux. Plan BATCH_14_PLAN.md : distinguer occasions
rares, occupations, géométrie et attente réactive ; suivi froid3200 de toutes les
graines seulement si le diagnostic le justifie. Aucun nouveau helper chimique.

## Priorités du lot13, historique

G1 achevé et analysé : insertion1/2/2, fermeture0,840/0,841/0,759 ; critère
conjoint2/3, aucune dominance sur B. Voir BATCH_12_RESULTS.md. **Arrêter les
réglages isolés de membrane** et tester J0 : vrais P/R libres/liés, température
commune, contacts et produits incorporés, témoins natif/froid et sans frontière.
Le plan BATCH_13_PLAN.md fixe quatre conditions × trois graines à400.

Ensuite décider si le verrou est thermique, dilution/concentration, transport ou
construction. La fabrication de L par F et une seconde fonction sous lois fixes
restent les prochains tests d'expressivité ; J0 ne les implémente pas. Longueur,
multigène et remplacement durable ouverts. Lire DESIGN_PRINCIPLES.md avant
toute nouvelle loi : pas de nouveau garde par défaut ni de loi par fonction.

Mise à jour du bilan technique : J0 terminé12/12 à400, premiers F natifs3/3
contre0/3 à froid ; bain commun sans F ni incorporation. Voir NUMERICS_AND_RENEWAL.
Avant retouche ou prolongation : analyser les contacts/occupations et l'éligibilité
du génétique à froid pour distinguer temps d'attente et pièges. Programmer ensuite
la convergence en dt des mécanismes retenus ; elle n'est pas encore démontrée.

## Priorités avant analyse du lot12, historique

Trace M1G terminée et garde géométrique rejeté. Comparer maintenant G1, condition
symétrique sur deux occupations de ports, sur0/1/2 à1500 aux témoins M1R conservés.
Pilote court sans activité, occasions admissibles non nulles : aucun succès à
déclarer. Conserver activité d'insertion **et** confinement ; zéro insertion
est une régression même si les défauts disparaissent. Une seule variante figée,
puis décision de mécanisme, avant intégration matérielle G/F.

## Priorités après lot11, historique

M1R achevé6/6 et références B exactes. Les ruptures spontanées des témoins sont
brèves ; B0 présente un défaut prolongé entre une substitution et son inversion.
Voir [résultats](BATCH_11_RESULTS.md).

**Prochain test M1G :** tracer les participants/ports d'une substitution réussie
et d'une défectueuse, puis restreindre un motif strictement local seulement si
la trace le justifie. Garder fixation des lois, réversibilité, fonctions utiles,
mesures d'exposition et critères conjoints. L'intégration matérielle G/F reste
ensuite ; pas d'insertase gratuite ni de balayage de constantes sans diagnostic.

## Priorités après lot10, historique

Campagne K1 achevée6/6, [résultats](BATCH_10_RESULTS.md). Insertion B observée3/3
à1500 ; fermeture/rétention conjointes incomplètes. B simple perd2–4/24 sondes et
n'insère que1/3. Conserver la barrière de lien comme référence, sans prétendre
qu'elle suffit au maintien global.

1. **Robustesse membrane :** même horizon sans échange pour isoler ses effets,
   mesurer ouvertures/périodes inconnues, puis accès et refermeture. Demander
   insertion et confinement conjoints ; ne pas multiplier les helpers.
2. **Intégration matérielle :** transférer membrane et vrais précurseurs G/F vers
   des lois communes, tester cohabitation, états libre/lié et effets parasites,
   puis copie/expression confinées. Construction L et diversité I0/T9 ouvertes.

Pas de prochaine campagne lancée pendant ce débriefing. Optimisation CPU si le
coût d'intégration le justifie ; aucun besoin démontré de portage GPU immédiat.

## Priorités avant analyse du lot10, historique

Le [lot9](BATCH_09.md) réduit le risque de grande frontière : rétention sélective
sur sondes3/3 à150 sans barrière de lien, fuite1/24 à450 sur un suivi ; deux
insertions par échange local sur une seule graine. Membrane et G/F restent séparés.

**Prochain lot technique K1 :** campagne figée, état consultable, arrêt/reprise
et analyse cinétique des rencontres, éligibilité, premières transitions et essais
censurés. Puis M1B sur horizons comparables et transfert sans barrière de lien.
Profiler avant optimisation CPU, sans modifier les lois ; GPU après preuve de coût.
I0/alphabet commun et T9/multigène suivent. L'ancien plan est conservé ci-dessous
comme contexte du lot8, et non comme état des preuves du lot9.

## Plan avant le lot9

Le [lot8](BATCH_08.md) franchit C3B pour une fonction : F exprimé→composant
incorporé3/3, copie G entièrement issue de ses produits2/3, renouvellement de
F complets1/3. Conserver cette référence commune ; le passage à XYZ/isomères
est une option de conception, pas une obligation imposée par l'utilisateur.

**Prochain lot : M1/I2–I4**, pour réduire le risque aval de grande frontière,
échange/insertion depuis l'intérieur et fuites. Un départ membranaire construit
est permis. Ensuite comparer les alphabets réutilisables et I0, puis T9/I1.
Ne pas multiplier des variantes de capture après ce transfert fonctionnel.

Le [graphe intégré](CELL_ARCHITECTURE.md) et les [contrats](CELL_INTERACTIONS.md)
encadrent désormais les choix. Cible conditionnelle :3 gènes/3 outils,16 espèces
cibles, budget nominal2 406 billes. Ce ne sont pas des capacités moléculaires
validées. V8 préfère des anneaux trop petits pour ce contenu ; l'insertion dans
un anneau saturé et la perméabilité selon l'état lié/libre sont à démontrer.

Suivre la méthode [exploration, unification, simplification et santé](../.agents/skills/local-chemistry-research/SKILL.md).
Le [lot 6](BATCH_06.md) construit de vrais dimères puis les incorpore dans G/F.
Copie seule et expression seule passent3/3, coexistence courte2/3 ; aucun outil
n'a encore produit ces dimères. La référence active E3C du lot5 reste conservée.

1. **P0 — I0/choix d'alphabet et diversité utile.** Le transfert C3B est obtenu
   pour un assembleur polyvalent de vrais P/R. Comparer la réutilisation des
   quatre précurseurs à la variante XYZ et ses états de produit distincts,
   en comptant les ports, outils et gènes nécessaires pour fabriquer L aussi.
   Tester plusieurs fonctions transférables et les interactions étrangères,
   sans imposer artificiellement des monomères isomasses. Ne pas additionner
   des réussites de modèles distincts ni simplement renommer XY.
   Le même alphabet doit permettre plusieurs outils ; commencer les contrôles
   d'espèces étrangères avant d'élargir leurs fonctions. EN/EA/EL sont des rôles
   visés par la forme des chaînes, jamais des types ni une table de séquences.
   Le noyau P_G/P_F/R0/R1 ne constitue pas encore une chimie commune avec L ;
   déclarer cet écart matériel et tester la fabrication/compatibilité membranaire.
2. **P0 — T9/E3, longueur et fragments.** Au prochain test génétique, diagnostiquer
   les stocks piégés et comparer finition/recyclage local des fragments à la
   croissance de chaînes complètes. Contrôles sans renouvellement et stabilité
   des gènes/outils ; aucun critère dynamique de longueur cible. L'association
   prolongée seule échoue. Garder le couplage court comme référence, sans prétendre
   que 001 résout la capacité d'information riche.
3. **P0 — M1/I2–I4, frontière dimensionnée, insertion et flux.** Tester une grande
   frontière préparée à faible courbure avant l'intégration : nominal rayon34,4,
   environ219 L, contre rayon préféré1,53 pour V8curved. Mesurer échange local,
   arrivée de L depuis dedans, refermeture et fuite. Rétention et passage sous interactions
   locales dépendant de l'état de liaison, puis compatibilité avec le noyau commun. Les
   indices intérieur/extérieur restent analytiques. Ne pas exiger la formation
   spontanée de toute la cellule, dont l'initialisation construite est autorisée.
   Ne pas résoudre le blocage par un outil d'insertion gratuit : compter gI/EI
   et leur reconstruction si une insertase devient nécessaire.
4. **P1 — utilité et diversité.** Obtenir un flux de composant utile, comparé
   avec/sans outil, puis plusieurs productions par assemblages différents sous
   les mêmes lois. Les opérations XY et le comptage de co-capture ne prouvent
   pas ce bénéfice. Prévoir remplacement sous pertes et matière/fuel déclarés.
5. **P2 — minimalité et robustesse.** Étendre les graines seulement quand elles
   répondent à une question ; ablater les aides et mesurer le coût réactif avant
   une grande campagne. Ne pas ajouter une règle spécifique par fonction.

## Références à préserver ou à marquer comme régression

- C3B1 G001+six monomères F préparés, aucune chaîne F : F libérés1/3/1,
  composants par F certifiés34/40/24, incorporés3/13/7 ; G complets1/2/0 et
  F complets0/2/0 entièrement issus des produits certifiés. t1200, trois graines.
- Outil préparé C3B1 :22/24/23 dimères et G3/3/5. Sans capture ou sans taux
  accéléré, aucun produit dans la graine0. Délier l'outil initial n'est pas un
  contrôle sans enzyme permanent : la graine2 réexprime un F et se réactive.

- C3A P/R libres : G001 seuls3/5/2, F001 seuls4/4/4 libérés ; mêmes lois.
  Mixte G2/0/2 et F1/1/1, deux graines avec coexistence simultanée. Sans
  assemblage ou sans ligation : aucune chaîne nouvelle ; sans gène : aucune.
- C3A001011 G seuls48, graine0 : une copie. Deux bains mixtes longs n'ont aucun
  G/F complet ; expression longue pas encore retrouvée dans cette variante.
  Les paramètres/initialisations diffèrent du bain alimentaire préparé : pas
  d'attribution causale à la seule constructibilité.

- E3C 001, 24 G + 24 F + X/Y, t=800, graines 0/1/2 : G 3/2/2, F 3/2/3,
  coexistence détachée 3/3, maximum d'opérations par outil 2/3/2.
- C2D expression→opération, F seuls, graine 0 : deux F, trois opérations par
  outil. E3C retrouve exactement toutes ses métriques et tableaux.
- G seuls 001011, 48 G à t=800, graine 0 : une copie sous coopération ; point
  perdu avec deux faces. Ne pas cacher cette régression par un changement de graine.
- Sans gène, coopération et deux faces : aucune chaîne fabriquée ni opération
  certifiée ; conserver les produits spontanés comme tels.
- 001011 dans le bain mixte : aucune coexistence démontrée, même si la coopération
  exprime un F par essai. Ne pas agréger cette réussite et une copie d'un autre run.

L'[évaluation de santé](PROJECT_HEALTH.md) fixe l'horizon E3, C3, M0. E3 et C3A
sont partiellement franchis ; M1 est le prochain point de décision aval, sans
prétendre C3 entièrement clos ni la membrane compatible avec cette boucle.
Si les interventions cessent de réduire les risques, revoir le candidat et le
budget plutôt que multiplier les démonstrateurs. Données locales, commits locaux,
aucun push. Les échecs et trois erreurs d'étiquette restent dans les recettes.

## État après livraison technique K1

Contrôleur/mesures livrés et testés ; utiliser le plan B/Bsimple sur horizons égaux,
puis analyser les occasions de réaction, la fermeture, la persistance et la fuite.
La livraison technique n'autorise pas à déclarer M1B robuste. Les décisions I0/T9
et le transfert vers une chimie commune restent les suites scientifiques.

## Mise en œuvre du prochain test M1R

Le lot11 prépare B et sans échange au même horizon1500, avec diagnostic des
ouvertures et contrôle source-exact. Analyser ces six résultats avant tout
réglage chimique. Ensuite intégration de vrais précurseurs/composants G/F sous
lois communes ; si le diagnostic reste indécidable, mesurer directement les
fuites des périodes inconnues, plutôt que déclarer leur rétention.
