# Homéostasie des polymères — pistes locales, fermeture encore ouverte

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

Ces tests devront être chiffrés après choix du mécanisme. Ni taux ni protéine
de recyclage n'est choisi ici. Priorité : fermeture qualitative inhibition +
pertes + protection + débouché des fragments, en parallèle de l'expressivité I0,
avant une coûteuse stabilisation de réplication qui ignorerait ce verrou.
