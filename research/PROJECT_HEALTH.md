# Santé du projet — 24 octobre 2026

Cette évaluation vise la faisabilité globale et le volume du travail, pas le
nombre de simulations positives. Elle doit évoluer avec les résultats. La cible
est une cellule construite qui maintient et refabrique ses composants depuis
une nourriture simple, avec énergie externe déclarée. Apparition spontanée,
division et évolution ouverte ne sont pas des conditions ajoutées à cette cible.

## Estimation avant le lot 5

**Poursuite justifiée, faisabilité complète encore conditionnelle.** Le lot 4
réduit un risque réel : les F fabriqués par traduction sont matériellement
utilisables, plusieurs fois, sans changement de représentation. L'angle ajouté
a pu être supprimé. Ce sont des signes de convergence ; le nombre de résultats
positifs ou la reproductibilité du logiciel ne suffiraient pas à les établir.

Je n'identifie pas de contradiction de principe avec les libertés accordées.
Cela ne signifie pas absence d'obstacle inconnu. Deux incertitudes majeures sont
déjà visibles : la constructibilité des composants et l'utilité nette des outils.
Elles doivent être testées avant d'accumuler d'autres fonctions accessoires.

| Risque en aval | Diagnostic actuel | Début de solution et test qui tranche |
| --- | --- | --- |
| Copie et traduction se bloquent | Échec observé dans le bain mixte à port unique | Deux faces locales du même dimère ; demander deux produits libérés ensemble et activité conservée |
| Composants impossibles à fabriquer dans la représentation actuelle | Les rungs et familles G/F sont assignés à l'initialisation ; XY ne peut pas devenir G/F par les lois actuelles | Passer à des billes persistantes et liens/états constructibles localement ; fabriquer un dimère puis l'incorporer réellement dans un polymère |
| Outils spectateurs sans effet utile | Les chaînes font des opérations, mais le fond spontané épuise aussi la nourriture | Réaction produisant un composant utilisable, comparaison de flux avec/sans outil, puis remplacement sous perte ; ne pas rebaptiser XY |
| Un helper ou type supplémentaire par fonction | Quelques helpers réutilisés ; diversité fonctionnelle non établie | Figer un alphabet et obtenir deux productions distinctes par assemblages différents, puis ablater les aides |
| Frontière incompatible avec alimentation et rétention | Contours V8 obtenus, fonction de barrière non testée | Matrice locale de perméabilité sélective autorisée ; mesurer passage et fuite avant intégration |
| Renouvellement impossible sans cycle global favorable | Cycle génétique externe et précurseurs activés fournis ; pas de régime maintenu | Fixer les apports externes, introduire pertes locales et vérifier un flux qui remplace les pièces ; bilan de matière et dépendances |
| Coût de calcul ou d'itération excessif | Petits bains seulement ; code réactif encore en partie Python | Mesurer le coût de bains intégrés avant balayage massif ; optimiser le moteur commun si ce coût domine |

La constructibilité est un **verrou de l'implémentation actuelle**, pas une
impossibilité physique prouvée : retoucher les concentrations ne peut pas la
résoudre. Il faudra une évolution explicite du modèle matériel et ses tests.
Elle peut invalider une partie des choix actuels ; préserver alors les principes
utiles, sans chercher à sauver chaque ligne du prototype.

## Volume et horizon de décision

Une intervention de conception modifie un principe ou une représentation ; un
lot peut contenir de nombreux essais automatiques sans compter chacun comme
une nouvelle idée. Le lot 4 comportait 53 dynamiques, quatre candidats principaux
et une simplification. Il ne démontre pas qu'il reste 53 étapes de conception.

Une trajectoire en quelques dizaines de lots reste **plausible pour le
démonstrateur minimal**, si une petite bibliothèque de lois suffit. Je ne peux
pas encore en faire une prévision crédible : nous ne connaissons ni le coût de
constructibilité ni celui de la diversité des fonctions. Il serait injustifié
de promettre un nombre précis de lots ou d'exclure tout changement de paradigme.

Chemin de travail limité à six obligations majeures : coexistence génétique ;
composant fabriqué et incorporé ; petite bibliothèque de productions compatibles ;
remplacement des outils ; frontière avec flux ; maintien intégré sous pertes.
Elles ne sont ni équivalentes en difficulté, ni six tickets d'implémentation
ordinaires. Les mécanismes de chaque étape restent à démontrer.

**Horizon de réévaluation : les trois prochains jalons E3, C3 et M0**, ou plus
tôt si une impasse réapparaît. C3 doit passer avant tout nouveau long catalogue
de comportements. À chaque lot : indiquer le risque réduit, les coûts ajoutés,
les régressions, ce qui reste sans mécanisme crédible et le prochain test décisif.

Réviser le candidat si deux tentatives de conception successives sur un verrou
n'apportent ni transfert ni diagnostic nouveau ; une exploration supplémentaire
doit alors avoir une hypothèse distincte. Si chaque fonction exige des règles
spécifiques, si les acquis ne se composent pas, ou si aucun flux utile n'apparaît,
redessiner l'alphabet/représentation et réévaluer le budget. Conserver les échecs.
Ce seuil sert à éviter l'acharnement ; il n'implique pas d'abandonner le projet
sans examiner une autre conception dans les libertés autorisées.

État chimique détaillé : [maturité](MATURITY.md), [priorités](PRIORITIES.md).

## Réévaluation après le lot 5

Un jalon d'intégration est franchi pour 001 : copie, expression et opération dans
le même bain sur trois graines. La coopération existante suffit ; la nouvelle
géométrie à deux faces n'est pas indispensable et perd une référence G seule.
Retenir la solution plus simple est un signe favorable de la démarche.

La généralisation à six symboles reste non résolue. Le protocole plus long ne
suffit pas et les polymères incomplets immobilisent une partie du stock. Ce
verrou pourrait coûter plusieurs interventions et compromettre une bibliothèque
de fonctions plus riche ; il ne doit pas être masqué par la réussite courte.
T9 fournit une piste de finition/recyclage local, non encore démontrée.

Le candidat final du lot ajoute zéro type et zéro état de site par rapport à
C2D : il réutilise E2. Il ne supprime pas les aides antérieures. Trente simulations
et trois erreurs d'étiquette ne sont pas trente progrès conceptuels : le gain
porte sur l'intégration et le choix entre trois hypothèses, avec un risque de
longueur explicitement restant. Les scénarios résolus ont permis de détecter
et conserver les trois erreurs ; leur générateur est corrigé et testé.

Mon jugement reste donc : recherche assez saine pour poursuivre, trajectoire
encore insuffisamment dé-risquée pour promettre quelques dizaines d'interventions.
Aucun obstacle irréversible de principe identifié ; en revanche, le modèle
matériel actuel doit évoluer. Pour C3, une piste concrète est un graphe de billes
persistantes où les liens choisissent localement les partenaires d'un composé,
et où G/F est un état constructible du lien, plutôt qu'une famille préassignée.
L'incorporation d'un premier dimère produit sera le test, pas le seul dessin
de cette représentation. M0 reste le jalon suivant de transport. Réévaluer la
trajectoire et son volume sur ces preuves, avant un catalogue de nouvelles fonctions.
