# Brouillon — ce qu'un assemblage fonctionnel pourrait faire

30 octobre2026, lot29. Priorité de conception I0. Ce document distingue les
mécanismes existants des hypothèses ; il ne déclare aucune nouvelle loi adoptée
et ne constitue pas une autorisation d'ajouter une machine moléculaire.

## 1. Quel problème faut-il résoudre ?

La cellule cible doit fabriquer les **trois familles de petits constituants** :
N0/N1, A0/A1 et L. Cela représente cinq produits cibles, pas trois molécules
uniques. Les gènes et outils sont ensuite des polymères de ces constituants.
Copie et expression impliquent elles aussi ligation, sélection, finition et
libération ; elles ne sont pas des opérations gratuites exécutées par le logiciel.

Les trois rôles EN/EA/EL sont des obligations abstraites de production, pas une
preuve qu'il faut exactement trois protéines distinctes. Un assembleur polyvalent
pourrait réduire ce nombre si ses produits utiles et ses interférences le
permettent ; une machine supplémentaire pourrait l'augmenter, avec son gène et
son renouvellement. Aucun des deux changements n'est implémenté ici.

**Aucun rationnel mécanistique ne justifie actuellement24 unités.** Cette
valeur n'est qu'un cas de budget. Pour une jonction simple, commencer par des
petits assemblages ; accroître la longueur seulement si un gain mesuré de
sélectivité, recrutement, géométrie, libération ou coordination le nécessite.
Les longueurs des outils et de leurs gènes peuvent différer entre rôles. Avec
le transfert un symbole→un monomère F actuellement envisagé, la longueur de
l'outil détermine celle de son gène ; elle n'est pas déduite d'avance d'un budget.

## 2. Ce qui existe réellement : un petit assembleur à deux sites

Sources : [precursors.py](../simulator/precursors.py),
[assembly.py](../simulator/assembly.py), [copy.py](../simulator/copy.py),
[preuves et ablations C3B1](BATCH_08.md).

1. Chaque unité F composite porte un site. F0 capte un P libre ; F1 un R libre.
   Attraction locale, saturation d'un site et d'un atome, puis liaison temporaire.
2. Les liaisons/forces réelles rapprochent les précurseurs ; une formation P–R
   exige encore leur proximité effective (rayon0,58 dans la référence).
3. Si les deux précurseurs sont tenus par deux F **directement liés**, le taux
   de jonction passe du fond0,0001 au taux20. Motif borné à six billes : deux
   F composites et deux précurseurs. Aucun nom d'enzyme ou séquence entière.
4. Le P–R formé conserve ses vrais atomes ; le symbole vient de R. La nouvelle
   occupation le retire des précurseurs capturables et libère les sites F.

Le noyau du motif mobilise seulement deux F voisins. L'outil001 de trois F
n'est pas démontré minimal ; la présence d'un motif admissible dans F2 ne
garantit pas qu'il soit dynamiquement efficace. Le lien entre sites, leur
géométrie et l'occupation ont un effet réel, avec libération et usages répétés.

C3B1 a montré F exprimé→dimères fabriqués→produits incorporés sous ses lois,
dans son régime historique. Cela n'est pas une preuve de renouvellement viable
sous MD2/Langevin : ses grands bains ne produisent pas de F nouveau complet.

### Limites importantes du prototype

- Le bonus de taux est un **helper local explicite**. Ce n'est pas une baisse
  de barrière dérivée du seul potentiel géométrique. L'ablation historique
  sans ce bonus ne construisait pas les produits dans l'essai testé.
- Les catégories de capture regroupent P_G/P_F d'une part, R0/R1 d'autre part.
  Le même motif fabrique donc des dimères des deux familles. Changer la séquence
  F ne fournit pas aujourd'hui un commutateur démontré EN contre EA.
- Les monomères G et F sont spécialisés matériellement dans le candidat actuel.
  Ils ne sont pas encore les deux états N/A d'un alphabet XYZ commun imaginés
  par le cahier des charges C0B. La construction des constituants L n'existe pas.
- Le moteur permet des préférences d'angles locales et un masquage par l'état
  d'appariement. Mais MD2 utilise les mêmes cosinus0,8 pour F0 et F1, et aucun
  functional_bend_cosines distinct : pas de bibliothèque de repliements
  séquence→fonction démontrée sous ces paramètres communs.

Nous avons donc un mécanisme de co-recrutement/ligation et un premier transfert,
**pas encore une famille de protéines programmables et composables**. La
localité de ce premier outil ne suffit pas à prouver l'expressivité du paradigme.

## 3. Familles de mécanismes compatibles avec la localité

| Famille | Réalisation locale envisageable | Situation actuelle | Risque / test décisif |
| --- | --- | --- | --- |
| Petit gabarit ou pince de ligation | Affinités de sites et géométrie mettent deux réactifs en contact ; motif local favorise un lien ; produit perd son affinité | Co-recrutement, jonction et libération prototypés avec helper | Produire sélectivement deux produits utiles avec des assemblages différents et exactement les mêmes lois |
| Repliement et poche | Types/ports et angles locaux imposent des préférences ; contacts à courte portée stabilisent une conformation ; la séquence organise les sites | Potentiels d'angle disponibles, pas de famille de poches validée dans le candidat commun | Comparer forme, occupation, taux et mauvais substrats ; une jolie forme sans flux utile n'est pas une enzyme |
| Pince à charnière / travail mécanique | Fixation d'un ligand change localement un angle, une affinité ou une longueur de liaison ; les forces se propagent dans la chaîne | Hypothèse, pas un moteur exprimé démontré | Montrer déplacement/effort utile, libération et retour ; compter énergie et vérifier le cycle complet |
| Clivage et recyclage | Deux sites imposent une contrainte sur une liaison précise, ou un voisinage catalytique facilite sa rupture ; fragments se libèrent | Non implémenté pour recycler G/F/L | Ne pas détruire indifféremment gènes, outils et nourriture ; vérifier bilan et réutilisation des produits |
| Transfert/insertion | Contacts locaux avec un composant libre et une liaison cible favorisent un échange, puis libération | Insertion L par échange existe ; aucune insertase protéique construite | Tester insertion ET confinement, coût gène/outil si une machine devient nécessaire |
| Marcheur processif sur polymère | Captures réversibles voisines, occupation locale des ports et cycle énergétique permettent des étapes répétées | Hypothèse, aucune polymérase ajoutée | Départ/arrêt par motifs locaux, pas de longueur cible connue ; produire et renouveler le marcheur lui-même |

Ces familles ne nécessitent pas une fonction « active » décidée par le programme
pour la chaîne entière. La conformation instantanée, les liaisons et les sites
occupés portent l'état ; des forces et transitions élémentaires font le reste.
Nous n'avons pas prouvé que **l'alphabet actuel** permet toutes ces familles.
Une extension de ports, états ou potentiels reste un candidat à comptabiliser,
pas une capacité déjà acquise du moteur.

### Exemple de cycle local à chercher pour une pince

```text
site libre + substrat proche → liaison locale
liaison locale → préférence angulaire locale modifiée
forces entre voisins → rapprochement des deux substrats
ports réactifs proches → transition de liaison admise
produit lié → affinité modifiée → libération
sites libres → retour de la géométrie → nouveau cycle
```

La chaîne n'« apprend » jamais que les deux extrémités ont attrapé les bons
réactifs. Chaque événement est local ; une information entre extrémités ne
peut se transmettre que par des interactions physiques ou changements d'état
successifs effectivement simulés. Un cycle moteur/pompe devrait avoir un budget
énergétique déclaré : couplage à une ressource activée ou forçage externe assumé.
Le bruit thermique seul ne sera pas déclaré source illimitée de travail dirigé.

Pour la jonction actuelle, ressources activées et cycle de déliaison restent
des aides externes. Ne pas les requalifier en autonomie énergétique ou cycle
enzymatique local déjà construit. Le bilan E/W du schéma est une autre hypothèse.

## 4. Comment obtenir des fonctions différentes sans tricher ?

Une voie à étudier est la **géométrie et les ports du produit** : deux modes
de liaison élémentaires génériques conduisent à N ou A selon les ports qui
se rencontrent et leurs états. Un assemblage privilégie une pose, un autre
l'autre ; le moteur n'interroge pas un label EN/EA pour choisir le produit.
Autre voie : utiliser des affinités élémentaires distinctes pour des précurseurs
matériellement distincts. Ce choix est plus proche de P_G/P_F actuels mais son
coût d'alphabet et son transfert vers L doivent être comparés explicitement.

Cela ne signifie pas que le mécanisme est trouvé. En particulier, choisir les
trois productions dans trois tables de réactions propres à chaque démonstration
échouerait à l'objectif de fonctions nouvelles sous lois communes.

Une règle catalytique sur un petit motif peut être un helper admissible, avec
son coût et ses ressources. Une nouvelle bille-type « enzyme N » qui exécute
toute la synthèse, une lecture de séquence entière ou un switch de tous les
angles de la chaîne quand un score global est bon seraient exclus.

## 5. Pourquoi de plus longues chaînes pourraient servir — sans les présupposer

Sites de capture éloignés, maintien d'une pose précise, plusieurs étapes de
liaison, libération sélective, ancrage et couplage mécanique peuvent demander
des unités supplémentaires. Un filament pourrait aussi augmenter une zone
de recrutement, comme proposé par l'utilisateur. Mais une longue chaîne peut
diffuser/relaxer plus lentement, piéger des substrats et ne pas ramener ses prises
au site actif. Il faut mesurer le gain net par coût réel de simulation et par
coût de synthèse, pas invoquer un effet de ratissage pour justifier vingt unités.

La longueur ne doit pas augmenter le nombre de voisins lus par une réaction.
Le travail mécanique collectif d'un assemblage peut, lui, résulter d'une suite
de forces locales sur de nombreuses unités. La division reste un stress-case
futur, pas une raison de gonfler les synthétases de base aujourd'hui.

## 6. Fermeture et nouvel ordre des jalons

**I0 devient prioritaire avant une nouvelle optimisation T9 de duplication.**
Premier jalon de décision : choisir une petite famille d'assemblages capable
de deux productions **distinctes et utilisables**, sous alphabet, lois,
paramètres thermiques et aides figés. EN/EA sélectifs ou un assembleur polyvalent
dont tous les produits sont utiles sont deux architectures à comparer, pas deux
succès à additionner. La capacité à fabriquer L reste un test aval obligatoire.

Protocole à concevoir avant tout lancement :

1. Décrire la pose/chaîne d'événements attendue pour un assemblage court ;
   comparer la solution la plus petite à une extension justifiée par une fonction.
2. Avec assemblages construits, mesurer bons/mauvais produits, turnover,
   libération, bruit de fond, saturation et outils étrangers dans un même bain.
   Témoins sans outil, sites déliés, séquence/connectivité modifiée et helper ablaté.
3. Vérifier que les produits rentrent réellement dans le processus suivant,
   sans conversion externe ou changement des règles. Une classe déclarée N ne suffit pas.
4. Exprimer le même assemblage depuis son gène, puis retrouver son activité
   et la fabrication des composants nécessaires à son propre renouvellement.
5. Transférer à la membrane et à l'alphabet commun ; compter chaque gène,
   matière, apport d'énergie, déchet, recyclage et compétition supplémentaires.

Si le seul moyen d'obtenir une seconde fonction est une nouvelle règle dédiée
à cette fonction, revoir la représentation avant de stabiliser toute la copie.
Si, au contraire, la copie empêche de renouveler un outil **fonctionnellement
établi**, le diagnostic génétique redevient l'obstacle d'intégration prioritaire.
Les références actuelles sont conservées. Aucun nouvel essai ou outil n'est
lancé ici. Une machine supplémentaire fera l'objet d'une proposition et de
l'accord utilisateur déjà prévu par DESIGN_PRINCIPLES.md.
