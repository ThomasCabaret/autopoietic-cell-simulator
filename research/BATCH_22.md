# Lot 22 — bilans complets et transfert du mouvement à la chimie

29 octobre 2026. P10 terminé10/10, MIX1 terminé10/10, MIX2 terminé18/18 ;
LT1 ajouté puis terminé6/6, sans erreur. **Aucune campagne de ce lot ne tourne
encore.** Deux pilotes LT1 à20 sont conservés séparément, hors des44 essais
principaux. Plan préalable : [BATCH_22_PLAN.md](BATCH_22_PLAN.md).

## Conclusion et décision

Le transport brownien pénalisait effectivement plusieurs objectifs. Langevin
gamma0,1,masse1 est un meilleur candidat que le défaut pour certains de ces
objectifs à coût réel mesuré. Son transfert aux réactions augmente la production
de séquences F complètes, mais **ne rétablit pas une amplification G fiable**.
L'audit des événements établit directement que les fragments G servent de
matrices concurrentes ; donner plus de nourriture ne corrige pas ce défaut.

Retenir Langevin comme candidat expérimental, sans changer le mouvement par
défaut ni les démos. Prochaine priorité : T9, finition/réutilisation des produits
et concurrence des matrices courtes. Ne pas relancer une grille inerte ni une
escalade de stocks pour éviter ce choix mécanistique. Aucun nouvel outil
moléculaire ajouté ; une éventuelle machine processive demanderait une proposition
avec mécanisme local, gène, expression et renouvellement, puis le feu vert
utilisateur. Aucun arbitrage utilisateur nécessaire pour clore ce diagnostic.

## P10 : la fidélité des symboles ne suffit pas

Un G0010110101 préparé,400 monomères composites G **ou**400 F, graines0/1/2,
T0,6,dt0,005,horizon3200, mêmes lois et cycle externe de libération200/15.
Deux bains séparés, sans membrane ni synthèse des monomères depuis la nourriture.

| À3200, graines0/1/2 | Nouvelles chaînes exactes | Fragments | Monomères libres |
| --- | --- | --- | --- |
| Copie G400 | 1/1/0 | 138/162/158 | 57/26/50 |
| Expression F400 | 1/3/1 | 30/32/36 | 272/258/272 |

Les fragments G sont surtout des dimères :100/136/142. À800, les nombres de
copies G sont déjà1/1/0 avec308/324/263 monomères encore libres. Le stock tardif
est donc un facteur aggravant, pas une explication suffisante du rendement.
Le témoin sélectionné G800,volume×2,graine0 ne donne qu'une nouvelle copie et
355 fragments ; G400 dilué donne2 copies,142 fragments et une seconde génération.
Ces témoins à une graine ne constituent pas une étude complète des concentrations.

Reconstruction des graphes **avant chaque tick de réaction**, à partir des
véritables arêtes sources des ligations :175/204,174/211,164/192 ligations G400
utilisent une matrice fragmentaire, soit82–86%. Le témoin G800 atteint348/383,
soit91%. Ce sont des actes observés, pas une causalité déduite des seuls stocks.
En expression F, aucune matrice fragmentaire : les produits F ne peuvent pas
devenir matrices dans ces lois. L'audit reproduit exactement le graphe final
des checkpoints et vérifie les symboles effectivement enregistrés.

Aucune séquence hors des sous-séquences du modèle, chaîne plus longue ou cycle
n'a été observé dans les recensements P10/LT1. **La reconnaissance stricte et
l'absence de canal de mutation sont imposées** : cela ne démontre pas un mécanisme
émergent de correction d'erreurs. Les liaisons initiales sont irréversibles ;
la survie du premier G ne prouve pas son entretien. Les produits incomplets
et leur amplification parasite restent le problème majeur.

## MIX1/MIX2 : distinguer les objectifs et le coût réel

MIX1 confirme, à froid, D≈0,00990 pour le centre d'un dimère idéal contre0,01
attendu. Les voisins se renouvellent vers360/420/420, l'occupation globale
vers3970/4430/4510. Les cœurs répulsifs ne freinent pas toutes les métriques de
la même façon : sans cœurs, dispersion globale plus lente mais davantage de
partenaires proches. Le remplissage d'une boîte ne mesure pas le mélange des
identités. Doubler la cadence de lecture des contacts change leur nombre
d'épisodes de50%, mais les partenaires distincts de3,1% et le temps-paire de0,08%.
Ne pas assimiler recroisements browniens et réactions indépendantes.

MIX2 utilise une nouvelle géométrie sans compression, identique pour ses modèles,
et200 dimères sans chimie. Médianes de secondes de calcul pour trois graines
froides, observateurs inclus, compilation initiale et écritures exclues :

| Premier seuil | Brownien | Langevin0,1 | DPD0,5 | DPD2 |
| --- | --- | --- | --- | --- |
| Renouvellement des voisins | 18,35 | 2,03 | 2,80 | 2,82 |
| Occupation spatiale | 170,04 | 3,64 | 2,66 | 2,45 |
| Perte de mémoire spatiale (MI) | 124,92 | 11,75 | 13,97 | 13,64 |

Langevin n'est pas meilleur sur chaque métrique : DPD occupe plus vite l'espace.
Le critère conjoint exige aussi une moyenne de50% des199 partenaires rencontrés,
tenue cinq observations. À froid, les candidats rapides restent **censurés à1600**
contre un témoin brownien allant à12000 ; aucun classement du mélange complet
n'est permis. À chaud, une seule graine atteint le critère conjoint en106,08s
brownien,31,08s Langevin et63,21s DPD : avantage Langevin≈3,4× dans ce cas.
Les charges concurrentes limitent la précision des comparaisons de coût.

Contrôles thermiques et mécaniques satisfaits dans MIX2 ; le contrôle gamma4
à diffusivité appariée n'offre pas un gain magique. Les contrôles dt0,01 à une
graine ne certifient pas la convergence : conserver0,005 pour le transfert.
DPD ajoute deux parcours de paires locales ; Langevin est plus simple et moins
coûteux pour plusieurs objectifs. Ce choix reste sélectionné sur MIX2.

## LT1 : contre-test réactif terminé

Seule différence physique avec les six références P10 : `mechanics` Langevin
gamma0,1,m1. Géométrie, température, stocks, réactions, pas et cycle conservés.
Vitesses Maxwell initialisées après les positions. Même graine ne signifie
pas même chemin aléatoire après ce changement de dynamique. Sources et scénarios
figés avant le calcul ; références browniennes réutilisées, pas recomptées.

| À3200, graines0/1/2 | P10 brownien : nouvelles exactes | LT1 Langevin : nouvelles exactes |
| --- | --- | --- |
| G10 | 1/1/0 | **2/0/3** |
| F10 | 1/3/1 | **7/7/6** |

Le tableau compte les séquences complètes présentes, même encore appariées.
Les G LT1 libres à la dernière observation sont1/0/3 ; les F le sont tous.

F10 progresse sur les trois graines ; les fragments F passent à25/21/22 et
les monomères libres à239/241/235. Ce sont des **séquences exprimées**, pas des
enzymes F10 dont la fonction serait démontrée. G reste en échec sur une graine,
avec133/134/140 polymères nouveaux, dont seulement2/0/3 exacts ;32/22/22
monomères libres à la fin. Les matrices fragmentaires soutiennent encore
68,5/86,1/64,3% des ligations G. Les générations complètes sont1/0/2.

Les premiers F complets et les G des deux essais réussis apparaissent à190 ;
l'absence de G graine1 est censurée à3200. Températures cinétiques échantillonnées
globales≈0,476–0,712 pour cible0,6 ; pas de réajustement global par l'observateur.
Coûts complets des travailleurs≈533–550s pour G,446–454s pour F, sous deux
travailleurs concurrents. Ces durées ne donnent pas un facteur d'accélération
apparié aux anciens P10. L'extension des liens d'appariement à longueur cible
nulle n'est pas assimilée à une lésion du squelette.

## Localité, logiciel et provenance

Zéro type, port, réaction, gène ou outil chimique supplémentaire. Langevin
ajoute une vitesse par bille, masse et frottement ; forces existantes locales,
bruit indépendant par bille et thermostat externe déclarés. Aucun déplacement
ou choix de réaction piloté par une molécule entière. Le coût DPD reste dans
MIX2 : pas de DPD réactif ajouté. Les classifications de fragments et séquences
sont des observations sans rétroaction.

Le moteur invalide le cache de force **après chaque tick réactif**, même sans
événement de ligation rapporté : appariement/libération peuvent changer les
forces. Audit thermique passif, checkpoints avec vitesses/PRNG, signature des
scénarios incluant le nouveau mouvement. Le préfixe brownien P10 à50 conserve
positions, PRNG et état chimique exactement ; six signatures physiques de démos
inchangées. Vérifications : **133 tests logiciels +7 tests historiques réussis**,
dont recalcul des forces, passivité, reprise et reconstruction des événements.

Recettes versionnées :

- P10 : `research/campaign_recipes/P10_20261029T120049792477Z`.
- MIX1 : `research/campaign_recipes/MIX1_20261029T123103222882Z`.
- MIX2 : `research/campaign_recipes/MIX2_20261029T132411069082Z`.
- LT1 : `research/campaign_recipes/LT1_20261029T172315655927Z` ; pilotes
  `LT1pilot_20261029T172036396166Z`.

Données locales préservées sous `outputs/campaigns/campaign_20261029T120049792477Z`,
`outputs/mixing_campaigns/campaign_20261029T123103222882Z`,
`outputs/motion_campaigns/campaign_20261029T132411069082Z` et
`outputs/transfer_campaigns/campaign_20261029T172315655927Z`.
Synthèse avec44 contrôles de sources/scénarios/analyses :
`outputs/reviews/completed_20261029T175433568977Z/review.json`, son `driver.py`,
`review.png` et `chemical_transfer.png`. Les scripts versionnés
`audit_polymer_lineage.py` et `review_completed_campaigns.py` permettent le
recalcul ; les données et figures restent locales ignorées par Git.

## Maturité, risques et prochain jalon

Progrès réel de transport et transfert partiel sous les mêmes lois réactives,
testées séparément. Aucune nouvelle preuve de couplage G/F/membrane dans un bain,
de synthèse des monomères, de fonction F10 ou de maintien cellulaire. Le transport
n'est plus une explication suffisante du défaut de copie. Le candidat génétique
reste fragile face aux fragments ; c'est un risque architectural sérieux,
pas une impossibilité de principe établie.

Prochain jalon borné : choisir un mécanisme local de finition/recyclage ou de
spécificité de matrice, avec témoins de séquestration des outils complets et
de parasites, puis tester la production libérée utile depuis un seul G long.
Après deux changements conceptuels sans transfert ni diagnostic nouveau,
réexaminer la représentation. Toute adoption de Langevin exige ensuite des
régressions membrane/catalyse à lois communes. Ni délai de cellule viable ni
demi-renouvellement en moins de dix heures ne sont estimables avec ces essais.
