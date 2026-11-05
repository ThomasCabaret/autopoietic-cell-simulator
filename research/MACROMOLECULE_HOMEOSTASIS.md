# Homéostasie des polymères — pistes locales, fermeture encore ouverte

## Actualisation lot47 — exposition des fragments mesurée, compromis encore ouvert

RX1 rejoue full/protected graine0 RV1 à1200 sous sources historiques, états,
RNG et observateurs exacts. F déjà polymérisés : temps encore lié73,65%/94,28%,
temps éligible P–R3741,53/640,81, intensité37,4153/6,4081. Capture directe de
ces F isolés :2,07/0,16 sites·temps ; mauvais candidat pour expliquer seul le
goulot. Ce sont deux histoires différentes sélectionnées, pas un effet causal
apparié. Le refus protected original et sa porte restent inchangés.

Piste qualitative suivante : protéger une liaison lorsque ses deux extrémités
sont appariées sur les deux extrémités d'une liaison voisine, plutôt que dès
qu'une extrémité est occupée par n'importe quel ligand. Motif borné de quatre
composites/huit billes, séquence/longueur/origine/fonction jamais interrogées.
Protéger ainsi les duplex de copie et laisser un squelette portant seulement
des substrats se renouveler serait une alternative sans nouvel outil ; elle
pourrait aussi détruire trop vite les outils ou préserver des fragments
appariés. Il faut comparer ces deux échecs avant adoption. Aucun nouveau garde,
taux ou mécanisme de régulation implémenté dans ce lot. H-03/H-04/H-06 restent
gap : accès au recyclage et protection de chaque espèce ne sont pas le même but.
Voir BATCH_47 et sa trace RX1, sans transférer la variante refusée vers EG1.

## Actualisation lot46 — rétroaction directe inaccessible dans le candidat

PI1 est terminé15/15 : aucun site G occupé par les F01 produits préparés,
pour4 ou16 outils dans chacune des trois graines. Ce n'est pas une limite de
temps ou de concentration : les règles communes ont monomer_only_capture et
pas gf_end_capture ; tous les F01 ont un degré de squelette1 et sont exclus
de cette capture. Les témoins F0/F1 déliés peuvent, eux, se fixer. Le précontrôle
orienté appelle maintenant GeneticAudit et refuse une répétition identique.
Ce constat aurait dû précéder le calcul ; les recettes originales sont conservées.
L'assay isolé ne mesure ni inhibition de débit ni maintien et ne change aucune loi.

Une alternative qualitative sans outil supplémentaire consiste à borner le débit
de naissance par l'accès local aux substrats et aux sites, tout en laissant des
pertes locales croître avec les liaisons exposées. Un débit saturé B et une perte
effective proportionnelle au stock D peuvent donner un bilan B−D borné ; ce bilan
est un raisonnement, jamais une mesure globale qui piloterait une réaction.
Les maillons à réaliser ensemble sont : approvisionnement externe fixé, production
concurrente, rupture/recyclage réel G/F, dissociation des composites en précurseurs
perméables et sortie au bord. RV1 étudie les pertes dans une autre variante,
pas leur compatibilité actuelle avec MX2/CB1. Il manque aussi un mécanisme qui
protège assez chaque information et conserve une répartition viable entre espèces.
Une borne sur la masse totale ne remplit pas cette exigence : tous les sites
peuvent être monopolisés par des fragments ou un seul gène. H-03/H-04 restent gap.

Ne pas activer gf_end_capture uniquement pour obtenir un frein sans examiner
copie, ligation parasite, piégeage et sélectivité. Si un outil de régulation devient
préférable, comparer ses coûts puis demander l'accord utilisateur avant ajout.
La cible part d'une cellule construite et redondante : aucune promesse de recréer
une séquence entièrement éteinte à partir d'aucune information restante.

Les paragraphes suivants gardent la genèse des pistes, pas une validation actuelle.

31 octobre2026. Sous-buts W-02/W-03/W-04 et H-03/H-04/H-06 du registre.
Pas de règle ni nouvelle machine implémentée. Le candidat actuel ne comporte
pas de recyclage des squelettes G/F ; aucun résultat d'homéostasie n'est revendiqué.

Dans l'architecture actuelle, l'information est portée par G et les outils par F ;
il n'y a pas de messager ARN séparé. Si un transcrit ou complexe durable est
introduit, ajouter son propre point de régulation/pertes au registre : le bilan
de G/F ne le couvre pas automatiquement.

## Pourquoi c'est un verrou distinct

Une petite espèce perméable peut diffuser vers un puits externe. Un gène ou
outil retenu ne bénéficie pas de cette évacuation. Ni une synthèse saturante
ni un stockage en complexes n'empêche nécessairement son accumulation totale.
Un inventaire fini empêche matériellement une explosion, mais peut seulement
finir en réservoir épuisé ou en fragments inertes. Ce n'est pas du maintien.

Il faut suivre séparément nombre/longueur des polymères, matière totale,
copies génétiques utilisables **par espèce**, outils actifs et occupés,
fragments, monomères et matière effectivement exportée. Les mauvais produits
ne disparaissent pas parce que les compteurs ne les comptent pas comme bons.

## Paquet qualitatif le plus simple à comparer

### A. Freiner la naissance par des interactions réversibles

Exemples de pistes : le produit occupe temporairement un site de synthèse ;
un outil ou une copie terminée se réassocie à des ports du template et limite
de nouveaux recrutements. Seuls contacts, symboles, occupations et géométrie
locaux interviennent, jamais un `if nombre_de_protéines > seuil`.

Un contact fréquent quand la population augmente peut rendre la rétroaction
effective sans mesure de concentration par la dynamique. Mais **l'inhibition
doit se réaliser moléculairement** et rester réversible. Les outils ne doivent
pas tous devenir indisponibles, ni les gènes immobilisés. Les fragments et
autres gènes peuvent imiter les mêmes contacts. La sélectivité de cette
rétroaction reste un trou conceptuel, pas une conséquence acquise de T9E.

Inhiber la fabrication de A peut contribuer à ralentir toutes les protéines,
mais ne garantit pas une bonne répartition entre enzymes ou entre gènes. Une
saturation fixe peut seulement plafonner une naissance encore supérieure aux pertes.

### B. Introduire une perte/recyclage local plutôt qu'effacer une chaîne

Première piste sans nouvel outil : réversibilité lente des liaisons de squelette,
ou érosion par des bouts libres. Taux selon nature chimique de la liaison,
occupation et voisins directement liés, jamais selon « bon gène », longueur
ou origine. Déplier/casser une chaîne n'efface pas ses billes.

Deux niveaux sont à distinguer :

1. Squelette G/F → fragments et monomères composites, encore retenus mais
   potentiellement réutilisables dans copie/expression.
2. Si un excès net doit sortir : dissociation de composites en précurseurs
   réellement perméables, puis diffusion à travers la membrane et absorption
   au bord extérieur. Cette seconde étape n'existe pas aujourd'hui.

Une autre piste est un assemblage catalysant un clivage local ; elle coûterait
un outil, son gène, sa synthèse, son énergie et son propre renouvellement.
Cette solution nécessite proposition et accord avant implémentation. Ne pas
supposer une protéase gratuite, ni un catalyseur distinguant globalement un
produit « à jeter ». Toute voie doit produire de vrais substrats réutilisables
avec leurs bons ports/états, pas seulement des morceaux de bonne composition.

### C. Protéger assez l'information et les outils utiles

Une famille G peut avoir des liaisons plus stables que F en vertu de sa chimie ;
une liaison peut être protégée par un appariement local ou un contact qui masque
son accès. Le repliement pourrait protéger certains sites d'un outil. Ce sont
des différences chimiques/de géométrie, jamais une exemption par nom de molécule.

Le compromis reste ouvert : une dégradation qui traite les fragments peut
détruire les derniers gènes avant leur copie ; une protection trop forte peut
préserver les parasites autant que les bons produits. La redondance atténue
un risque d'extinction, sans garantir de récupérer une information entièrement
perdue. Une forte stabilité seule ne régule pas le nombre de copies.

## Le raisonnement de bilan, sans le confondre avec une loi

Pour une classe de polymères P, une esquisse de bilan est :

```text
variation du stock P = naissance locale effective − perte/recyclage effectif
```

Une naissance qui diminue avec l'occupation par ses produits et une perte
qui augmente avec la quantité de matière exposée peuvent produire un régime
borné. Cela donne une famille d'architectures à rechercher, **pas** une loi
de simulation ni la preuve d'un point fixe viable pour toutes les espèces.
La fermeture des boucles et le couplage G/F/L peuvent encore rendre ce régime
inaccessible. Pour les gènes il faut aussi que la reconstruction dépasse les
pertes en régime pauvre, tant qu'une copie utilisable subsiste.

Les stocks bornés de chaque classe ne suffisent pas si toute la matière se
retrouve dans des fragments non fonctionnels. Réciproquement, mesurer beaucoup
d'outils actifs sur un court intervalle ne prouve pas une population bornée.

## Tests qui pourraient rejeter rapidement ces pistes

- Sous une alimentation au bord figée : excès initial de F puis manque de F,
  et mêmes perturbations séparées pour **chaque** gène. Suivre récupération,
  activité utile, encombrement, fragments et extinction, pas seulement total de billes.
- Sans inhibition / sans perte / sans protection : mêmes lois restantes,
  mêmes apports et matière ; distinguer plafond de naissance et stock stable.
- Mélanger outils, gènes et parasites : rechercher empoisonnement, capture
  croisée, surprotection des fragments et perte de la dernière information.
- Vérifier conservation de matière et réutilisation/évacuation effective après
  clivage. Seule une sortie par frontière peut retirer la matière du domaine.
- Annoncer avant calcul les bandes fonctionnelles, horizons de plusieurs
  renouvellements mesurés, perturbations et seuils d'extinction/censure.

Ces tests devront être chiffrés après choix du mécanisme. Au lot30, ni taux ni
protéine de recyclage n'était choisi. Priorité : fermeture qualitative inhibition +
pertes + protection + débouché des fragments, en parallèle de l'expressivité I0,
avant une coûteuse stabilisation de réplication qui ignorerait ce verrou.

## Premier candidat expérimental — RV1, lot31

Le plan BATCH_31_PLAN.md fige quatre variantes de pertes locales, dont une
dissociation P–R libérant la matière réelle et une protection par occupation.
Implémenté sous option séparée, sans protéase ou autre outil supplémentaire.
Le trajet contrôlé jusqu'au réemploi passe ; les12 essais normaux et les4
transferts conditionnels comparent sa cinétique et ses dégâts. Un census dédié
remplace la filiation irréversible. Ce candidat teste la partie pertes/débouché,
pas le freinage, la régulation des copies ou l'export par frontière ouverte.
Même une porte passée ne suffira donc pas à affirmer l'homéostasie.
