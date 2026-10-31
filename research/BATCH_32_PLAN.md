# Lot32 — MIN1, taille mécanistique de l'assembleur existant

31 octobre2026. Simplification puis transfert sous les lois MD2/Langevin
inchangées. Le verrou I0 reste la diversité des productions et L ; la voie
polyvalente existante mérite un contre-test avant d'inventer une autre enzyme.
La fonction P/R existe déjà : F01 contre F001 est un contrôle de taille et de
connectivité de cet outil, pas l'ajout d'un outil fonctionnel supplémentaire.

Hypothèse : deux sites F0/F1 directement liés suffisent à fabriquer les deux
familles G/F, puis leur gène court s'exprime et ses produits alimentent les
polymères. Si la troisième unité n'aide pas cette fonction, la supprimer réduit
son coût matériel et le nombre d'étapes de copie/expression. Cela ne résout ni
copie de longs gènes ni répertoire programmable ni fabrication L.

## Coût, localité, témoins

Zéro type, état, port, loi, taux, outil biologique ou gène additionnel. Alphabet,
forces, activation, helper P/R, bruit et cycle200/15 de MD2 conservés. On change
seulement connectivité/longueur des assemblages et préparations. Le témoin sans
bonus est une ablation explicite de loi, jamais présenté comme le même candidat.
RV1 et T9E absents ; pas de séquence cible dans une réaction.

Analyse passive des événements existants : produits G0/G1/F0/F1, libération,
opérations répétées du même outil, produits incorporés et attribution à un F
préparé ou exprimé certifié **avant** l'opération. Aucune modification du moteur
ou enregistrement systématique de trajectoires nécessaire. Vérifier saturation,
symboles des vrais R, provenance, absence de double comptage et ordre temporel.

## Chaîne prospective bornée

A :12 essais, t400, trois graines0/1/2 × quatre préparations,150 billes,
boîte12×9, T0,08, m1/gamma0,1, dt0,002, réaction0,01, mesure0,5.
G001 initial non polymérisé et aucune arête G : pas d'expression dans ce test.
Quatre jeux de trois F préparés, même composition8 F0/4 F1, mêmes stocks libres :

- long : quatre F001 ;
- short : quatre F01 et quatre F0 libres ;
- split : les mêmes douze F séparés, aucun squelette ;
- no_boost : préparation short, bonus catalytique ramené au taux de fond0,0001.

Les positions des assemblages diffèrent car leur géométrie change ; ne pas
prétendre à des trajectoires initiales identiques. La préparation seule change
entre long/short/split ; no_boost est l'ablation annoncée.

Porte A complète uniquement : résultats/provenances valides ; médiane short
≥moitié de long et long non nul ; médiane short ≥5×max(1,médiane split,
médiane no_boost) ; chaque graine short produit au moins un G et un F ; dans
chaque graine short, un même outil préparé réalise au moins deux opérations.
Une porte passée sélectionne B ; aucune adoption automatique.

B :9 essais, t1200, mêmes lois/thermostat et150 billes : trois graines × gène
01, référence001, contrôle01 dépolymérisé. Quatre G initiaux par essai avec gène,
six F monomères001011, **aucune chaîne F initiale**. Fonction36 F ; G39 supports
dans chaque cas (free_units37 pour01,36 pour001). L'inventaire de symboles et
la fraction initialement assemblée sont publiés : même nombre de billes n'est
pas une identité de l'état initial. Le témoin01 sans gène garde les mêmes atomes
et symboles que01, arêtes G retirées seulement.

Critères B prospectifs pour interprétation, pas nouveau suivi automatique :
01 s'exprime puis catalyse et ses produits sont incorporés dans au moins2/3
graines ; au moins un produit G et un F issus de F exprimés incorporés dans
au moins2/3 ; contrôle sans gène sans F ni catalyse ; comparaison à001 entière.
Événements absents censurés à1200. Arrêt après B ou refus A, pas de grille.

Budget21 tâches maximum, deux travailleurs,24h, checkpoints30s, sources et
deux phases figées avant A ; arrêt/reprise explicites, pas de retry scientifique.
Réutiliser le gestionnaire et le superviseur existants. Rien n'est promu dans
les démos avant lecture et transfert dans le grand bain. Cette campagne teste
une fonction existante sous une architecture plus courte ; pas un nouveau
répertoire enzymatique. L reste le contre-exemple aval à fermer qualitativement.
