# Santé du projet —27 octobre2026

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

## Réévaluation après le lot 6

Le test matériel C3A est positif : des P/R indépendants construisent de vrais
dimères qui entrent dans des copies G et expressions F exactes,3/3 en bains
séparés et2/3 en bain mixte court. Une copie six symboles existe aussi dans un
essai G seul ; les deux bains mixtes longs restent sans produit exact. La piste
de représentation annoncée au lot5 a donc produit un transfert matériel en un
lot, avec un lien dynamique et deux constantes, sans nouveau type par fonction.
C'est un signe favorable pour le coût de conception, pas une extrapolation.

Le risque est déplacé, pas supprimé : P_G/P_F/R0/R1 sont une nourriture
spécialisée et le lien P–R se forme très vite spontanément. Aucun F n'en contrôle
la fabrication. C3A refuse encore l'ancien module X/Y à indices fixes ; les
preuves de fonction du lot5 ne s'additionnent donc pas à celles du lot6. La
fermeture matérielle reste absente et les supports élémentaires restent fournis.

Prochain test C3B : transférer les captures de C2D pour rapprocher un vrai P et
un vrai R, sous fond faible, puis incorporer le même produit. C'est un début
de solution concret au verrou de flux, non un mécanisme déjà testé. Mesurer
avec/sans outil et capture, séquestration et rendement utile ; si deux tentatives
de conception ne donnent ni transfert ni diagnostic neuf, revoir ce portage
plutôt qu'ajouter des règles spécifiques. T9 et M0 restent les jalons suivants.

Une intervention principale de représentation et19 dynamiques automatisées
ont réduit un obstacle réel ; pas19 inventions. Aucun nouveau blocage de principe
identifié. Santé toujours favorable à une poursuite ciblée, sans garantie sur
quelques dizaines de lots tant que flux utile, longueur et membrane ne sont
pas démontrés ensemble. Réévaluer après C3B, avant d'élargir les fonctions.

## Réévaluation après le lot 7 — audit d'intégration

Le graphe détaillé met désormais un coût et un test sur chaque dépendance :
3 gènes/3 synthétases obligatoires N/A/L,16 espèces cibles et environ2 406 billes
pour l'hypothèse nominale. Avec insertase,18 espèces et2 726 billes. Ces nombres
ne prédisent ni longueur fonctionnelle ni vitesse ; les budgets12/24/48 unités
par gène/outil bornent des hypothèses de travail, pas une incertitude statistique.

**Risque majeur V8 : courbure préférée et capacité requise ne concordent pas.**
Son rayon préféré1,53 (~12L) est bien inférieur au rayon nominal34,4 (~219L).
Il faut tester une géométrie plus souple/moins courbée ou son soutien par le
contenu ; le calcul ne prouve pas qu'un grand anneau contraint soit instable.
Ajouter des molécules ne démontre pas sa stabilité. Une frontière préparée est
permise : tester stabilité, insertion depuis dedans, refermeture et fuite à la
taille calculée. Une insertase éventuelle exige son propre gène et sa régénération.

**Risque biochimique central explicité : sélectivité plutôt que simple activité.**
EN et EA doivent créer des composés de même matière mais d'états différents,
sans enzymes primitives par fonction. Aucun mécanisme testé ne démontre encore
cette petite bibliothèque. La voie concrète consiste à des ports/états et
conformations locaux réutilisables, à évaluer dès C3B/I0. La compétition multigène,
les fragments et les produits parasites doivent être ajoutés aux essais sous
lois figées. À taille plus grande, l'import par surface peut aussi limiter la
demande volumique ; les taux manquent pour conclure.

Le lot apporte un cahier des charges plus réfutable et un audit à10 défauts,
aucun progrès dynamique supplémentaire. Les deux verrous majeurs ci-dessus sont
des insuffisances des candidats actuels, sans impossibilité de principe prouvée.
Le volume global reste non estimable de façon fiable : pas de promesse de quelques
dizaines de corrections. Horizon rapproché : I0/C3B et M1/I2–I4, puis I1/T9.
Si ces essais n'apportent ni transfert ni diagnostic nouveau après deux
interventions de conception, revoir les ports/la courbure avant de continuer.

## Réévaluation après le lot8

Un risque matériel réel diminue : un F exprimé fabrique des dimères utilisables,
avec incorporation sur trois graines et copie G complète issue de ces produits
sur deux. Une graine renouvelle aussi deux F complets. Le contrôle sans outil
reste presque sans produit, la capture sans accélération n'en donne aucun dans
l'essai testé. Une fonction utile est donc transférée sous des lois communes,
avec un helper nouveau déclaré plutôt qu'une cascade de changements par graine.

Le résultat reste court et finit avec des stocks fabriqués mais non incorporés.
La graine2 n'achève pas G malgré beaucoup de composants. Concurrence, fragments,
longueur et remplacement durable restent ouverts ; ni pertes ni alimentation
continue ni membrane n'ont été intégrées. La forte activité n'établit pas une
bibliothèque expressive. Les taux d'énergie ne sont pas calibrés : précurseurs
activés, cycle externe et accélération locale sont encore fournis.

Le schéma XYZ avec monomères N/A isomasses était une hypothèse du lot7, non une
contrainte utilisateur. L'assembleur observé est polyvalent depuis quatre
précurseurs. Comparer ce coût à celui de XYZ au lieu de considérer l'écart comme
une impossibilité artificielle ; aucun des deux n'a encore la production L et
les interactions de membrane sous les mêmes lois. Garder les comptes16/2406
comme budget du candidat C0B, pas comme taille finale promise du candidat C3B1.

Prochain test décisif M1 : grande frontière préparée, échange/insertion et fuite,
avant d'accumuler une nouvelle fonction chimique. I0/choix d'alphabet puis T9/I1
restent les autres risques. Aucun nouveau blocage de principe identifié ; le
transfert obtenu justifie une poursuite ciblée, sans estimation fiable du nombre
de lots restants. Une intervention de mécanisme et19 calculs, pas19 inventions.

Risque logiciel à traiter avant les grands bains : l'observateur stocke un graphe
dense par image. Pour1000 supports et2400 images, cela représente environ2,4Go
de matrices uint8 avant autres états. Stocker des arêtes parcimonieuses ou
désactiver les trajectoires en campagne évite cette dette sans changer les lois.
Les latences des petits runs concurrents ne sont pas un benchmark à2400 billes.

## Réévaluation après le lot9

Poursuite ciblée justifiée : le défaut de courbure aval est observé puis réduit
par une géométrie locale moins courbée. Une barrière de lien peut être retirée
du criblage de sondes. L'insertion a un début de solution à six billes, sans
contrôleur de contour ; elle reste rare et insuffisamment répliquée.24 calculs
ne sont pas24 interventions conceptuelles : géométrie, barrière ablatée et un
échange activé constituent les changements principaux.

Risques : accès aux faces saturées, fuite à longue durée, état réel libre/lié des
précurseurs, fabrication de L et compatibilité G/F. La perméabilité de sondes ne
résout pas ces transferts. Ne pas attribuer à B la simplification S sans test.
Si une insertase est requise, compter gI/EI et leur renouvellement. Richesse
génétique et diversité des catalyseurs restent non démontrées.

Aucun blocage de principe établi, aucun délai fiable en nombre de lots. Prochain
horizon : K1 cinétique/campagnes puis M1B simplifié/plusieurs graines, avant I0/T9.
Le suivi favorable B2 à450 est sélectionné : conclure3/3 serait un biais. Le coût
Python est une piste d'accélération, pas un facteur×10 mesuré. Le stockage
parcimonieux résout la dette des matrices denses pour ce hook seulement.

## Livraison technique K1

Le lot10 réduit le risque de faux échec par durée arbitraire : rencontres et
éligibilité sont instrumentées sans modifier les trajectoires. Les censures et
lois distinctes restent visibles. Les campagnes peuvent tourner hors conversation
et reprendre après interruption.58 tests+7 historiques, aucun gain chimique ni
débit×10 démontré. La campagne B/Bsimple doit maintenant dire si l'accès admissible
est réellement limitant ; ne pas convertir sa simple mise en route en preuve.
Éligibilité G/F, échantillonnage des conflits et coût du diagnostic restent à étendre.

## 2026-10-26 — debriefing K1 acheve

Six essais complets,168 empreintes et18006 observations verifiees. B insere1/2/5
dimeres a1500 : la duree150 masquait deux attentes longues. Fermeture au seuil
seulement2/3 et graine0 non classable28% du temps ; retention globale non prouvee.
B sans barriere de lien perd2-4/24 sondes, insertion0/1/0 : simplification refusee
pour ce couplage long. Beaucoup de rencontres, rares geometries admissibles.
Prochaines decisions : controle long sans echange et ouvertures, puis integration
avec vrais precurseurs/composants G/F sous lois communes. Aucun blocage de principe
etabli, volume restant incertain. Pas de nouvelle campagne pendant le debriefing.
Voir BATCH_10_RESULTS.md ; donnees locales preservees.

## Préparation M1R, lot11

L'audit permet désormais de distinguer une fragmentation du graphe d'un grand
écart terminal sans transformer l'inconnu en rétention. Le pilote source-exact
réduit le risque de mesure intrusive. Aucun progrès chimique revendiqué et
aucune nouvelle primitive. Les trois B sont rejoués parce que K1 n'enregistrait
pas ces diagnostics ni les positions complètes : coût justifié par une question
causale précise. Les trois témoins sans échange répondent au verrou manquant.

Horizon de décision : cette campagne, puis intégration G/F. Si elle ne localise
aucun défaut causal, ne pas multiplier des réglages de docking ; examiner le
critère topologique et une mesure physique indépendante des fuites. Le budget
et le chemin vers les aliments/outils réels restent conditionnels, aucun délai
en lots ni facteur d'accélération promis.

## 2026-10-27 — analyse M1R et trace locale M1G

Six controles completes, census et references B verifies exactement. Sans echange
la fermeture est0.844-0.851 avec peu de periodes inconnues ; B0 degrade surtout
apres787.56 jusque1236.11.897 images ont une extremite isolee au-dela1.35, contre
aucune avant/apres pour B0. Le defaut merite une intervention de motif local,
pas une pression globale ou une reinterpretation favorable du confinement.
Trace selectionnee B0 jusque800 sur sources figees, cas productif et cas
defectueux compares ; aucun filtre dans la dynamique a ce stade. Hypothese
disponibilite des faces a confirmer. Cout scientifique : diagnostic reduisant
un risque, pas nouveau modele viable. G/F et fabrication de L restent separes ;
aucun blocage de principe ni delai fiable en nombre de lots.

## Decision M1G1

La trace apporte un diagnostic neuf, pas un gain de viabilite. Un filtre
geometrique tentant est rejete ; une seule restriction locale symetrique est
retenue comme hypothese, en comptant sa complexite. La symetrie ne calibre
pas l energie. Le pilote sans activite reste visible et les occasions sous
garde sont mesurees pour eviter un faux succes par inhibition totale.
Horizon : trois essais longs comparables aux six temoins disponibles. Si la
fonction utile disparait ou si les defauts restent, revoir le mecanisme plutot
qu empiler des conditions. G/F, L, alimentation et renouvellement restent
ouverts ; pas de nombre fiable de lots restants ni nouveau blocage de principe.

## Lot13 — ne pas confondre correction et flexibilité

G1 conserve l'insertion3/3 mais ne domine pas B : fermeture2/3 au seuil, graine2
dégradée. Continuer à empiler des gardes spécialisés serait un risque de volume.
Décision : passer au test précoce de conditions communes J0, avec une dette
croisée libre/lié déclarée plutôt qu'un nouveau réglage de docking.

Le moteur accepte un bain commun vérifié ; les lois G/F étaient à0,6 et L à0,08.
J0 choisit explicitement0,08 et mesure ce changement avec témoins. La disparition
du petit confinement génétique peut diluer le stock : les témoins sans membrane
séparent ce risque de la température. Aucun résultat fonctionnel du bain commun
n'est encore acquis ; les pilotes courts sans rencontre ne permettent pas de
juger la cinétique. Réévaluation après la campagne400, avant autre helper.

Verrou structurel restant : les réactions actuelles ne fabriquent pas de L avec
F, et P–R/H–T n'ont pas la même géométrie. Les deux modules joints ne résolvent
pas cela. Une piste concrète est une seconde capture/assemblage depuis des
réactifs élémentaires avec produit de membrane utilisable, puis deux outils
sélectifs obtenus par assemblages sous les mêmes lois. Ce sera une évolution
matérielle déclarée, à comparer à un alphabet commun, pas un renommage de types.
La division reste une extension hypothétique, pas une exigence nouvelle.

Santé : poursuite justifiée par des tests réfutables, expressivité générale et
coût global non démontrés. Aucun obstacle irréversible établi ; ces verrous
pourraient cependant imposer une refonte. Contrat de reprise DESIGN_PRINCIPLES.md
désormais référencé par AGENTS.md et le skill.

## Bilan technique : précision et renouvellement

J0 est terminé12/12 à400. Les témoins froids n'expriment aucun F alors que les
trois témoins natifs en expriment un. Les contacts avec la frontière existent,
mais aucun flux incorporé ne ferme la boucle du bain commun. Le changement de
température est un risque observé sur cet horizon, sans diagnostic causal ni
preuve d'impossibilité. Ne pas masquer ce résultat par le benchmark logiciel.

Le coût de charges synthétiques à2406/6292 billes est accessible : environ
315/122 pas/s sans rendu, mais le temps biologique de demi-renouvellement reste
inconnu. Un scénario1000–10000 unités demanderait27min–4h25 à taille nominale ;
ce n'est ni une borne ni une prévision. La convergence en pas de temps est aussi
non démontrée. Prochain diagnostic : cinétique froide puis contrôle dt/dt2/dt4
sous mêmes lois, avant de compter sur un renouvellement rapide ou un gain GPU.
