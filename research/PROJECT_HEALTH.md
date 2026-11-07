# Santé du projet — actualisation du 7 novembre 2026

Lot58. Le transfert à une première chimie réactive confirme la faisabilité
de conserver le calendrier des ticks et la reprise. Les réactions CP1
occupent environ la moitié du profil court. Un gain sur la seule mécanique
ne clôt donc pas ce chantier. Les forces propres et la préparation des
réactions restent les risques de débit. [Critères de clôture](CUDA_COMPLETION.md)

Lot57. Gain de débit de la mécanique résidente mesuré à trois tailles de bain
inerte. Le transfert à CP1 dépend du coût des forces propres et du nombre de
synchronisations aux ticks chimiques. Exiger une mesure appariée du pas CP1
avant de modifier l'estimation d'effort ou d'investir dans un portage des
réactions. [Bilan du lot57](BATCH_57.md)

Lot56. Le passage des forces élémentaires par CUDA est vérifié sur un préfixe
CP1, avec reprise exacte sur la machine de test. Le pas hybride est plus lent
sur 302 billes. Le travail sur la résidence des données et le voisinage doit
donc précéder un investissement dans le portage de la chimie entière. Réévaluer
le débit sur une simulation avec forces supplémentaires et plusieurs tailles
de bain. Le lot technique n'ajoute aucune preuve de maintien cellulaire.
[Bilan du lot56](BATCH_56.md)

Réestimation après lot55, sans nouvelle fournée scientifique : **environ25
fournées restantes, plage18–35**, jusqu'à la préparation du premier test global
non naïf (pas sa réussite garantie). L'ancienne référence20/15–30 au lot46 a été
trop optimiste :9 lots techniques,11 avec les audits, ont été réalisés depuis
sans baisse du budget restant. Découpage et décompte traçable dans
[FORECAST_20261106](FORECAST_20261106.md). Recalibrer après3–4 véritables fournées.

Lot55 : progression de construction sans réglage supplémentaire de récupération.
OB1 lève le verrou technique d'un nombre variable de précurseurs avec bilan
ouvert exact ; ce n'est pas le transfert P/R ni le maintien de CP1. Les vingt
recommandations Astra sont triées ; les arguments sur instantané ne sont pas
transformés en preuves dynamiques. Deux à quatre interventions pour réévaluer
les décisions de représentation, bilan L et expressivité, sans délai de cellule
garanti. Si cette tranche ne mène pas à un couplage utile, revoir l'architecture
plutôt que multiplier les tests. [Vue courante](../CURRENT_STATUS.md).

Lot54 : progrès de compréhension, pas gain de viabilité. Les portes PT1/RF1
ont révélé des incompatibilités réelles avant transfert : ouverture ponctuelle,
perte de l'outil malgré gènes et substrat, recyclage strict absent et chaleur.
Récupération observée ailleurs montre une voie, sans garantie de robustesse.
FR1 est une unique hypothèse sur une horloge locale, pas une descente aveugle
de paramètres ; prochain horizon de décision six essais, puis interprétation
des contacts/ligation/catalyse. Si monomères survivent sans récupération, changer
le diagnostic et examiner la représentation plutôt que poursuivre les taux.
Pas de nouvel outil, dette thermique/énergie non masquée, CP1 inchangé. Diversité,
information et flux/régulation restent des risques ; aucune garantie de délai.
Voir [BATCH_54](BATCH_54.md).

Lot53 : étape mécanique franchie sans ajouter de règle : CR1 passe2/3
avec trois contours finaux. L'attente longue était informative ; ce résultat
ne garantit ni étanchéité ni maintien. Deux campagnes bornées et indépendantes
ouvrent les questions suivantes : rétention avec contrôle transparent, réemploi
de matière avec vraie activité01. Aucun lancement dépendant ou grille aveugle.
Le premier témoin RF1 a consommé presque tout son stock libre et n'a plus de
catalyse tardive : si cela persiste, la porte ne permettra pas d'attribuer une
inactivité à la perte des outils. Conserver cette limite, diagnostiquer avant
tout nouveau régime d'apport ; pas d'allongement automatique.
Prochain horizon : lecture PT1/RF1 puis un transfert ou diagnostic ciblé.
Diversité, information/protection et régulation/flux/export restent des risques
conceptuels ; aucun délai ou pourcentage global garanti. [Bilan53](BATCH_53.md).

Lot52 : progrès sans augmenter le coût chimique accepté : fermeture finale
depuis dimères isolés obtenue dans deux cas actuels, et inspection directe
des résultats longs dans la GUI. Le ralentissement collectif était une piste
utile, mais les épisodes intermittents et le cas tardif empêchent de conclure
robustesse ou étanchéité. La troisième graine reste nécessaire au crible.
Pas de nouvelle constante, machine ou allongement pour sauver un résultat.
Prochain horizon de décision : CR1 complet, puis un transfert ou diagnostic
ciblé, sans nouvel horizon automatique. Information, diversité des fonctions,
protection/régulation et flux/export restent des risques conceptuels ; pas
de nouveau pourcentage global ou délai garanti. Voir [BATCH_52](BATCH_52.md).

Audit de complexité du6 novembre2026 : petit alphabet, spécialisation encore
substantielle. CP1 intégré :6 atomes résolus,5 dimères,6 profils de liaison,
8 formules intrinsèques,10 transitions dirigées et12 conventions fonctionnelles
recensées parmi20 conditions nommées.27 entrées numériques configurées et28
contrôles fixes revus, plus3 externes ; aucune interprétation en degrés de
liberté indépendants. Ce coût n'a pas explosé au lot51 (observation seulement),
mais le nombre de fonctions génériques démontrées reste faible. Priorité de
conception : obtenir davantage par les assemblages, partager/simplifier les
gardes, éviter une nouvelle exception par fonction. Les rôles G/F, affinités de
capture et filtre énergétique sélectif sont des dettes explicites, pas des
garanties d'extensibilité. Aucun palier biologique relevé par l'audit.
Voir [inventaire et convention](CHEMISTRY_COMPLEXITY.md).

Lot51,6 novembre2026 : sain pour poursuivre la recherche, sans garantie de
convergence complète. Le jalon diagnostic fixé au lot50 est atteint : forme
locale et modes collectifs quantifiés, pas de nouvelle règle ou outil ajouté.
Le nombre51 par tour est dérivé des ports, jamais une cible dans la dynamique.
Un horizon8000 est justifié par le mode nu1890 mais ne garantit ni équilibre
du bain ni fermeture ; CR1 borné doit maintenant départager le mécanisme.
Le coût de calcul différé est séparé des interventions de conception. Prochain
jalon : lecture CR1, au plus une variante mécanique justifiée si nécessaire ;
si aucun mécanisme explicatif exploitable, revoir la représentation. Pas de
nouvel horizon à l'aveugle ou milliers de réglages. Diversité des fonctions,
information riche, protection/régulation et flux/export empêchent de déclarer
la faisabilité entière résolue. Aucun blocage de principe établi, aucune
estimation globale relevée. Les globalités observées ne pilotent aucune réaction.
Voir [BATCH_51](BATCH_51.md).

6 novembre2026, lot50 : deux jalons CP1 examinés. Intégration/gradient/delta
et coût local atteints ; la récupération sélectionnée de frontière passe,
mais l'assemblage fermé isolé échoue au critère final. Ce n'est plus un blocage
de liaison par millions de refus. CE1 montre des extrémités distantes même
pour52 unités : prochain jalon, au plus une intervention de diagnostic
géométrique/courbure et un petit contrôle ciblé avant nouvelle campagne longue.
Sans mécanisme explicatif exploitable, revoir la représentation plutôt que
des constantes. La lenteur seule reste une hypothèse, pas une conclusion.
Pas de blocage de principe établi ni garantie de quelques dizaines de lots :
diversité, protection, information et flux restent conceptuels. Pas de chiffre
global relevé. Supervision Windows récupérée sans relance ni modification des
sources physiques ;4/4 résultats CH1 et aucun calcul actif à la clôture.
Voir [BATCH_50](BATCH_50.md).

Lot49, réévaluation après le refus structurel CF1 : l'attraction additive
libre rend favorable l'accumulation de partenaires qu'une liaison exclut ensuite.
Des millions de refus et la perte de frontière justifient l'arrêt anticipé,
pas le reste des six essais. Coût réel du filtre et cohérence thermodynamique
locale étaient sous-estimés par les contrôles binaires/pilote court.
CP1 répond par une famille locale compétitive sans nouveau nombre, validée en
statique ; elle devra rester calculable et expressive. Ce n'est pas une solution
dynamique établie. Horizon décisif : au plus deux interventions de conception
(intégration du delta/forces, puis transfert contrôlé). Sans nouveau mécanisme
ou transfert à cet horizon, revoir la représentation plutôt que régler des taux.

Les estimations d'orientation40%/15–30 lots du lot46 ne deviennent pas plus
fiables : ce refus montre qu'une révision de loi peut encore être nécessaire.
Pas de nouveau chiffre global ni garantie de quelques dizaines de lots avant
CP1 dynamique et fermeture protection/flux/information. Pas de blocage de principe
établi : alternative explicite et testable, mais maintien non prêt. FS1 évite
un autre faux diagnostic : perdre F001 n'est pas perdre toute activité F01.
Le proxy de séquence reste refusé, ne pas le relaxer après lecture. Aucun calcul
actif à la clôture, données et checkpoints de CF1 conservés.

Lot48 : le refus EN1 empêche de considérer l'insertion comme robuste. Il ne
prouve ni impossibilité de principe ni biais systématique de dt sur3 trajectoires.
Deux échecs relèvent d'occasions absentes/défavorables ; le troisième chauffe
avant son premier échange tardif. Horizon décisif EL1 : bilan des transitions
hors échange, sans nouvelle constante. Si aucun mécanisme énergétique n'émerge,
réexaminer forces/cycles avant une retouche ou une cohorte supplémentaire.
Le front indépendant RP1 transforme le diagnostic RX1 en un seul garde local
alternatif, pas une suite de taux ; horizon3 graines1200. Si réemploi gagné
mais perte d'information/outils, pas de transfert et révision du compromis.
Protection de chaque espèce, répertoire fonctionnel, flux/export et information
riche restent des risques conceptuels. Estimation lot46 non relevée ;2 lots
supplémentaires jusqu'à réévaluation, ou immédiatement si EL1/RP1 révèlent un
refus structurel. Maintien non prêt, pas de blocage irréversible établi ou garantie
que tout sera résoluble par des réglages. Deux calculs bornés, deux décisions.

Lot47 : un risque d'intégration réduit sans nouvelle primitive : EG1 garde
production/insertion et stabilité dans le domaine déclaré. Prochain jalon EN1,
un raffinement mécanique commun, pas une recherche de constantes. Un refus
exigerait de distinguer aléa, cinétique de contacts et instabilité numérique.
RX1 exact sur2 cas sélectionnés réduit l'incertitude de protection/recyclage :
le maintien lié domine, pas la capture isolée. Une alternative locale bornée
est dessinée mais pas adoptée ; elle pourrait perdre les outils actifs ou
conserver les parasites appariés. Protection de chaque information, partage des
ressources, alimentation/export et diversité restent des risques conceptuels,
pas de simples ajustements garantis. Maintien non prêt. Ne pas relever le jugement
de planification du lot46 sur cette seule réussite ; le réévaluer dans3 lots ou
au prochain refus structurel. Aucun blocage de principe établi, aucune garantie
que la cible soit accessible sans revoir la représentation.

Lot46 : l'ablation CX1 isole une frontière productive stable, CW1 obtient
insertion2/3 mais échoue par chaleur/ouverture dans une graine. Une seule
intervention mécaniste EG1 traite le coût local de l'échange ; trois essais,
pas trois conceptions supplémentaires. Horizon décisif : cohorte2400. En cas
d'échec, interpréter ses propositions/refus et reconsidérer le mécanisme avant
une autre constante ; ne pas poursuivre une grille de largeurs. PI1 a été lancé
sans détecter d'abord une impossibilité statique de capture des produits. Cette
dépense évitable est conservée et entraîne un précontrôle du prédicat réel.
Le manque de rétroaction directe révèle un risque concret, sans établir une
impossibilité de maintien : bilan débit limité/pertes/export plausible, protection
et répartition par espèce encore ouvertes. Ne pas attendre EG1 pour les concevoir.

À la question précédente, estimation d'orientation communiquée : environ40%
(30–50) de préparation au premier test intégré non naïf, environ20 lots restants
(15–30 conditionnels). **Jugement de planification, pas score de preuve, probabilité
ou engagement** ; ne pas le calculer comme moyenne de la checklist. Réévaluation
après3–5 lots ou tout refus structurel. Ces bornes ne sont pas fiables tant que
protection/régulation, information, transport/export et bilan sous flux manquent.
Le présent lot ne justifie pas de les améliorer. Pas de blocage de principe établi,
pas d'assurance que tous les risques seront de simples réglages. Maintien non prêt.

Lot45 : CB1 donne un premier transfert complet jusqu'à la frontière1/3,
avec G/F nouveaux3/3, mais fermeture robuste refusée. Le diagnostic ne se limite
plus au score : six billes, saut +6.0243 et extrémités non capturables, clone
sans loupe exact. CX1 sépare l'effet de l'échange ; CW1 est une seule modification
de largeur motivée, pas une grille ou nouvelle enzyme. Horizon décisif : leurs
trois graines complètes. Deux contrôles CX1 stables sont intermédiaires.
Si CW1 ne donne que stabilité sans transfert, revoir le mécanisme/énergie,
pas d'autres largeurs successives. La correction de routage d'analyse réduit
un risque logiciel, pas un verrou biologique. Restent des inconnues importantes
sur protection/recyclage, régulation, information et diversité : pas de délai
ou de nombre de lots restants fiable, ni maintien global non naïf justifié.
Aucun blocage de principe établi ; le transfert1/3 n'exclut pas un futur blocage.

Lot44 : BI1 est un refus utile mais réel : aucune insertion ni nouveau G/F.
Le volume historique masque la fonction par dilution et faible accès ; le
contrôle local montre une pose admissible, sans attraction vers une face occupée.
CB1 est une intervention de dimensionnement, pas neuf nouvelles corrections :
neuf calculs figés avec témoin noL, aucun taux ou outil ajouté. Pilote stable au
sens temporel, endpoint ouvert conservé ; adaptation du garde technique tracée.
Horizon décisif : cohorte CB1. Si elle échoue sans L, revoir le bain avant la
membrane ; si productive sans insertion et exposition faible, une seule piste
associative locale à départager. Deux changements sans transfert ni diagnostic
nouveau imposent refonte. Le prochain test global non naïf reste prématuré ;
protection/régulation, information, flux et énergie empêchent un nombre fiable
de lots restants. Aucun blocage irréversible établi, pas de délai garanti.

Lot43 : le diagnostic de capture converge : MX2 passe les neuf conditions
sans troisième retouche, ni nouveau taux/outil. La médiane génétique remonte,
mais les activités individuelles ne sont pas toutes meilleures ; la matière
finie impose de ne pas confondre épuisement et régulation. Une intervention
d'intégration ajoute la frontière à la même chimie ; BI1 neuf essais automatisés,
pas neuf changements conceptuels. Le pilote mécanique est stable et produit
un L intérieur ; le prochain horizon décisif est la cohorte1200. Si insertion
absente, séparer transport/éligibilité/attente/instabilité puis loupe ciblée,
pas une grille à l'aveugle. Deux changements sans transfert ni diagnostic nouveau
imposeraient de revoir la représentation. Risques majeurs encore ouverts :
répertoire F, protection et recyclage, régulation des polymères, énergie sous
flux et information. Aucun blocage irréversible établi, aucun délai ou nombre
de lots restant fiable avant ces jalons. La cible est le maintien, pas la division.

Lot42 : progression par compréhension causale plutôt que réglage de score :
audit de stocks, temps et occupation, puis loupe bornée ; deux recaptures rapides
illustrent le piège local. La coopération proposée réemploie la compatibilité
de jonction, sans nouvelle enzyme ou constante. MX2 est le prochain horizon
décisif, avec référence longue et témoin noHT ; pas de promesse d’asymptote à2400.
Une nouvelle erreur de calibration pourrait masquer la fonction : déclarer les
occasions insuffisantes au lieu de condamner le modèle. Si le candidat n’apporte
ni débit commun ni diagnostic nouveau, revoir la capture plutôt qu’enchaîner une
grille. L’objectif reste le maintien construit sous pertes et perturbations ;
homéostasie/protection/export et énergie sous flux restent des risques conceptuels
importants. Pas de blocage irréversible établi ni de calendrier garanti.

Lot41 : un obstacle de transfert est réduit (CT1 garde les remplaçants actifs)
sans ignorer la baisse d’activité médiane. L’étape suivante devient un test
causal de concurrence, pas une grille de constantes : un pool de capture pour
P/R/H/T,12 essais/4h maximum. Un échec de F neuf→L peut aussi être un problème
d’ordre temporel/épuisement des stocks ; diagnostiquer avant de rejeter le modèle.
Le prochain horizon de réévaluation est MX1 complet. Si deux interventions
conceptuelles supplémentaires n’obtiennent ni transfert ni diagnostic nouveau,
réexaminer l’architecture. Pas de blocage irréversible établi ni de délai garanti ;
énergie sous flux, information riche, diversité et protection/homéostasie restent
des risques majeurs. Le code seul ne réduit pas leur dette de preuve.

Lot40 : le transfert matériel vers le bain membranaire est confirmé avec
témoins complets ; ce progrès réduit une vraie incertitude d'intégration et
devient inspectable. Prochain jalon falsifiable : CT1, une seule modification
de capture dérivée,9 essais automatiques. Si régression, comprendre la géométrie
des contacts avant autre constante ; si réussite, tester les sites communs en
compétition P/R/H/T. Ne pas investir d'emblée dans une cellule complète sur la
somme de deux bains incompatibles. Aucun blocage irréversible établi ; fermeture
énergétique sous flux, information, diversité F et protection/régulation des
polymères restent des risques majeurs. Pas de calendrier garanti. Deux changements
conceptuels sans transfert ni diagnostic nouveau imposent une révision du modèle.

Clôture39 : l’hypothèse d’horizon est soutenue dans les trois suivis exacts ;
pas besoin d’une troisième correction mécanique pour obtenir une queue froide.
Progrès causal réel, mais comparaisons L3 sélectionnées et stocks finis : le
prochain risque pertinent est le couplage P/R/H/T et la puissance en régime
alimenté. Attendre le dernier contrôle MIN1M pour clôturer son transfert.
La cible reste plausible sans garantie de délai ; pertes/protection de gènes,
diversité des outils, information riche et homéostasie restent ouverts.

Lot39 : ne pas confondre seuil tardif et équilibre mesuré. Les T L3 décroissent
encore et certains produits naissent jusqu’à98,51 ; trois horizons400 sont un
diagnostic de temps justifié avant d’accumuler des rustines. L3 reste refusé au
crible annoncé. Ce lot ajoute du calcul sélectionné, zéro intervention chimique.
Le critère décisif demeure le transfert sous une chimie commune, pas une somme
de petites réussites. Pas de délai ni de maintien promis ; régulation/énergie,
information et fabrication L intégrée restent les risques majeurs.

Lot38 : la démarche réduit une incertitude causale, pas seulement un score.
La chaleur sans synthèse est reliée à51,2 d’énergie de préparation F et une
transition de capture+2,503. L3 enlève une contrainte mécanique arbitraire et
compare un départ construit détendu, sans réglage de thermostat/taux. La pose
native ne protège pas les futurs F exprimés ; ce transfert est explicite.
Si L3 ne stabilise pas le pool, revoir les changements de potentiel plutôt
qu’ajouter des valeurs de raideur. MIN1M avance matériellement sur3 cas actifs,
proche de sa consigne tardive, mais maintien/pertes/L commun restent ouverts.

Lot37 : échec thermique conservé plutôt qu’un succès de débit surévalué.
Les ablations distinguent coût du contact et de la formation ; un transitoire
persiste sans aucune synthèse, ce qui motive un diagnostic de préparation/
capture. Une comparaison ciblée de deux mécanismes a réduit l’incertitude,
pas établi la viabilité. Interpréter avant retouches ; les risques de fermeture
énergétique, régulation, information et diversité restent ouverts.

Lot36 : une contribution indépendante a levé le verrou des queues préassignées
et réalisé H/T→L→association avec l'outil existant, sans nouvelle enzyme. Un
pilote ne clôt pas la voie : l'échauffement a une cause maintenant explicite,
activation brutale des contacts F/L et d'un axe tendu. La loupe donne une décision
de conception plutôt qu'une grille cinétique. Prochain jalon L1 : transition
compatible énergétiquement, puis témoins et concurrence P/R. Si deux retouches
n'apportent ni compatibilité ni diagnostic, réexaminer la représentation.
Les noyaux indexés restent réutilisables même en cas d'abandon L1. Aucun délai
cellulaire garanti, maintien/renouvellement sous pertes et information ouverts.

Lot35,4 novembre2026 : le jalon suivant confronte la même boucle matérielle
au bain membranaire, sans nouvelle primitive ni tuning.12 trajectoires automatiques,
un choix d'architecture initiale, pas12 corrections conceptuelles. Le plus petit
contre-exemple noL distingue une incompatibilité avec L d'une dilution/organisation
du grand bain ; positions initiales appariées mais vitesses/PRNG noL différents.
La démonstration MIN1R est maintenant directement inspectable par l'utilisateur.
Décision après cohorte entière : transfert puis L, ou diagnostic avant toute
retouche. Les risques L/répertoire, régulation/protection et information riche
restent structurels ; pas de délai garanti ni maintien autonome annoncé.

Cette évaluation vise la faisabilité globale et le volume du travail, pas le
nombre de simulations positives. Elle doit évoluer avec les résultats. La cible
est une cellule construite qui maintient et refabrique ses composants depuis
une nourriture simple, avec énergie externe déclarée. Apparition spontanée,
division et évolution ouverte ne sont pas des conditions ajoutées à cette cible.

Clôture MIN1R : boucler matériellement le même petit outil fonctionne3/3 avec
départ construit, sans nouvelle règle ; contrôle sans gène négatif3/3. Cela
réduit un vrai risque aval et donne un jalon de transfert concret, pas une
preuve de tout le réseau. Le départ délié réussit aussi2/3 : ne pas imposer
artificiellement la nécessité de la protéine préparée. Prochaine décision
sur membrane commune, puis L et renouvellement sous pertes/flux. Deux choix
de préparation et un diagnostic ont convergé localement, sans empilement de
primitives ; ni délai de cellule complète ni absence de futurs blocages garantie.

Lots33–34 : MIN1 B reste non robuste, sans F entier depuis nourriture. Deux
diagnostics sélectionnés et exactement passifs localisent une rareté de double
capture ; ils évitent une retouche prématurée des gardes. On distingue maintenant
amorçage sans outil et remplacement depuis un départ construit. MIN1R mesure
ce dernier avec9 essais, sans dette de primitives. Première graine montre un
vrai F neuf actif, témoin délié aussi : convergence locale plausible, pas viabilité
garantie. Prochain jalon borné : cohorte complète puis transfert avec membrane.
Si cette voie ne conserve pas un renouvellement utile, réexaminer capture,
compétition et représentation avant une grille. L et homéostasie demeurent des
risques structurels ; une petite boucle protéique ne les résout pas.

Lot32 : simplifier un mécanisme existant avant nouvelle loi. F01 suffit pour
la catalyse G/F préparée sur3 graines ; pas de dette de primitives/gène ajoutée.
La reconstruction courte doit être jugée par B9, après A12 gate passée ;
ce sont21 essais maximum, pas21 interventions conceptuelles. La voie vers L
a un draft local matériel : même co-recruteur, H/T libres, vrai lien puis
ports MD2 ; capture parasite/énergie/queue variable sont des obstacles explicites,
pas des opérations implicitement gratuites. La voie n'est pas implémentée.
Prochain jalon décisif : expression→produit utile sous MD2, puis construction L
et transfert sans changement des lois en aval. Un succès de gène2 ne résout
pas information riche, répertoire, pertes ou homéostasie. Pas de délai garanti.

B partiel : short graine0 exprime puis alimente G, graine1 aucun F nouveau ;
l'activité d'un outil préparé ne garantit pas son amorçage. Le départ sans F
de B est plus exigeant qu'une cellule construite déjà équipée : maintenir
cette distinction, sans supposer pour autant le renouvellement acquis. Avant
toute nouvelle grille, lire la cohorte et distinguer amorçage/renouvellement.

Lot31 : une intervention de conception RV1,16 essais maximum dont4 conditionnels,
pas16 corrections conceptuelles. Le débouché matériel est maintenant réalisable
localement dans un contrôle ; son efficacité et ses dégâts sur les fonctions
doivent être confrontés aux12 essais, puis au bain commun si la porte passe.
Ce progrès n'établit pas une homéostasie ni la possibilité certaine du maintien.
Risque de destruction des derniers gènes et risque I0/L encore ouverts.
Décision bornée A/B avant tout nouveau réglage ; si deux retouches ne donnent
ni transfert ni diagnostic, réexaminer représentation/protection plutôt que
prolonger une grille. Le moteur et le census restent réutilisables en cas d'échec.
Quelques dizaines de lots restent une hypothèse conditionnelle, sans garantie
de délai ; aucun résultat ici n'autorise à promettre la cellule en dix heures.

Clôture RV1 :12 essais complets, B4 économisé par la porte refusée. Le cycle
matériel transfère dans le petit bain full2/3, mais la protection n'offre pas
le réemploi attendu. Risque mieux localisé, pas une impossibilité de principe.
Ne pas masquer l'échec par le cumul de réactions, dominé en partie par des
cycles monomères. Le jalon matériel avance ; I0/L et le compromis pertes/
protection restent à éprouver avant un maintien intégré. Aucun calcul actif.

Lot30 : le registre42 points rend explicites les inconnues conceptuelles et
leurs dépendances. L'expressivité I0 et l'homéostasie des macromolécules sont des
risques structurels ouverts. Une famille qualitative de freinage/recyclage/
protection est identifiée, mais sa sélectivité et sa fermeture ne sont pas
établies ; le dernier gène perdu ne se récupère pas par un stock d'enzyme seul.
Ne pas transformer cette piste en certitude de viabilité ni en date d'achèvement.
La prochaine décision compare ces trous aux coûts d'un petit contre-test ;
les réglages peuvent attendre si leur réussite ne réduit aucun risque aval.
Les scores de preuve par sous-but ne sont pas une estimation du nombre de lots.

Lot29 : l'expressivité des assemblages devient le verrou conceptuel prioritaire.
Le candidat dispose d'un assembleur P/R générique et d'aides locales, mais pas
d'une sélectivité EN/EA/L programmable démontrée. Même une copie parfaite ne
résoudrait pas ce manque ; stabiliser toute la génétique d'abord serait un
investissement prématuré. Premier jalon : deux productions utiles distinctes
sous lois fixes, puis transfert expression→outil→produit utilisable et test L.
Comparer un noyau minimal à une extension fonctionnellement justifiée ; aucune
raison actuelle de prédire24 unités. Si chaque fonction exige une loi dédiée,
revoir l'alphabet/représentation plutôt qu'ajouter une longue série de correctifs.
Le moteur partagé et les références restent réutilisables en cas de refonte.

Lot28 : l'atlas rend visibles trois séquences fonctionnelles encore inconnues,
la fabrication L, le recyclage, les flux et l'homéostasie non réalisés. Il ne
réduit pas ces verrous à des corrections techniques certaines. La cible3 gènes
et24 bases/gène reste un dimensionnement conditionnel, pas une solution trouvée.
T9E achevé n'améliore pas le contrôle d'expression ; le suivi a épargné les
quatre transferts non justifiés. Interpréter ces motifs avant une seconde
modification conceptuelle. Ni nouvelle protéine ni campagne ajoutée pour la carte.

## Lecture finale LT2 et diagnostic MD1

Lot27 ajoute une intervention conceptuelle bornée T9E, motivée par le garde
qui interdit la recapture des fragments. Le contre-exemple aval (séquestration
des outils complets) est testé avant le grand bain, avec critères de transfert
programmés. Ni la petite boîte ni le contrôle idéal ne garantissent le maintien.
Le prochain horizon de décision est la cohorte A puis éventuellement B ; pas
de balayage indéfini. Si le motif ne transfère pas, distinguer accès/géométrie
et défaut de représentation avant une seconde retouche. Une machine processive
reste une option à proposer à l'utilisateur, pas un ajout déjà autorisé.
La correction IO Windows est technique, pas une avancée de chimie ; données
interrompues conservées. Aucun calendrier de cellule viable garanti.

Clôture MD2/lot26 :15 essais terminés sans erreur, démos actuelles source-exactes
et passivité graphique vérifiées. Amélioration nette de fermeture du grand bain,
mais F nouveau0/3 et un contrôle d'insertion encore dégradé. Recensement final :
194/191/204 monomères F actifs dans le monde,16 F complets préparés persistants,
4/5/5 nouveaux fragments F2, aucun F3 nouveau. Ce n'est pas une pénurie globale ;
l'accès local et l'éligibilité doivent être mesurés avant d'augmenter le stock.

La trajectoire de recherche est plus informative, sans nouveau helper ajouté
dans ce lot. Elle ne permet pas encore de réduire copie, diversité des fonctions,
synthèse L et homéostasie à une liste de corrections indépendantes certaines.
La viabilité dépend de leur réalisation et de leurs compatibilités. Division
reste reportée, sans l'ajouter comme condition actuelle.

Prochain jalon : motif local T9 autorisant la finition utile et préservant les
outils complets, avec témoin d'interférence et classification cinétique. Le cas
à sondes a une cible de loupe concrète autour de223,61 ; pas d'obstacle futur
volontairement ignoré. Les critères de réexamen après deux changements sans
transfert ni diagnostic nouveau restent applicables. Voir BATCH_25_RESULTS.md.

## Historique — MD2 en cours

Lot25 MD2 en cours : un remplacement de potentiel lié, dérivé des paramètres
de ports existants, évite d'empiler une force et une nouvelle raideur spécifique.
La porte locale passe, sans contre-exemple sur toutes les anciennes graines ;
les petites V8 commencent à transférer le motif. La santé reste conditionnelle
à l'insertion/rétention et au grand bain, pas au nombre de tests logiciels.
Une rigidification excessive ou une injection d'énergie lors des échanges est
un risque concret. Les15 essais figés sont le prochain horizon de décision,
sans grille supplémentaire automatique. Voir BATCH_25.md.

Un changement conceptuel mécanique depuis le diagnostic MD1, zéro nouvel outil
fonctionnel ou dépendance. Le budget de particules du bain cellulaire est
inchangé ; les534 billes des sondes sont un banc séparé. Si le second changement
conceptuel ne réduit plus l'incertitude ou n'apporte aucun transfert, revoir
la représentation avant de poursuivre. Aucun délai de cellule viable garanti.

LT2 terminé16/16. La régression membranaire intégrée0/1 est un risque concret
que les seuls succès micro auraient masqué. Le mouvement n'est pas rétrogradé
pour sauver des rendements : la priorité est la cohérence chimico-mécanique des
contacts. Les données de fermeture/insertion et d'usage réel des produits passent
avant le nombre de réactions ou le débit du moteur. Voir BATCH_23_RESULTS.md.

MD1 réduit l'incertitude : la première perte durable sélectionnée survient
sans étirement excessif, sur des ports déjà hors géométrie de recapture.
La loupe reproduit exactement LT2. Aucun blocage irréversible de principe établi ;
la correction doit encore préserver molécules libres, insertion et souplesse.
Pas de garantie que toutes les graines aient la même cause, pas de délai viable.

Volume borné : cinq essais courts et un rejeu de diagnostic. Prochain jalon
de conception MD2 : géométrie cohérente d'un contact, puis transfert. Après
deux changements conceptuels sans transfert ni diagnostic nouveau, revoir la
représentation. Ne pas ajouter une protéine ou une suite de frottements pour
éviter ce choix. T9 reste ensuite prioritaire. Aucun coût causal supplémentaire.

## Historique — transfert visuel et physique LT2 en cours

L'utilisateur demande le mouvement dans les démos et les cas actuels avant
de reprendre les priorités. Un seul transfert borné :16 essais automatiques,
aucune nouvelle conception chimique. Six références conservées, six candidats
visibles, mêmes positions initiales et lois ; conditions/risques explicités.
Les premiers transferts micro sont positifs mais à une graine. Le changement
de mouvement modifie les contacts et l'énergie : il reste une hypothèse physique,
pas une optimisation logicielle indépendante de la chimie.

L'échauffement initial mesuré et les écarts au pas fin ne doivent pas être
masqués. Aucune instabilité numérique dans les pilotes ; cela ne garantit
pas les membranes ou les fonctions à long terme. Le J3 intégré reste à lire
avec plusieurs graines avant adoption. Pas de promesse de temps de renouvellement.
Le résultat réutilisable est un comparateur visible et des recettes figées,
même si le mouvement échoue. Voir BATCH_23.md pour premiers résultats et sources.

Horizon de réévaluation : fin de ces16 tâches, sans grille de frottements
supplémentaire par défaut. Puis T9, concurrence et finition des fragments ;
les critères de révision après deux changements conceptuels sans transfert
restent applicables. Aucun nouveau gène/outil, ni coût de dépendance ajouté.

## Réévaluation après les44 essais P10/MIX1/MIX2/LT1

Les cohortes sont achevées et les résultats/sources vérifiés ; voir BATCH_22.md.
La progression est mesurable : gains de transport à coût réel, puis davantage
de F10 exacts sous les mêmes réactions (1/3/1 vers7/7/6). Il ne s'agit pas
d'une simple optimisation d'un banc inerte. En revanche G10 reste peu amplifié
(1/1/0 vers2/0/3), malgré un transport accru et des stocks initialement abondants.
L'audit établit le rôle de matrices concurrentes joué par les fragments.

Santé **conditionnelle** : l'instrumentation et les essais réduisent une
incertitude importante, mais le défaut génétique est structurel pour ce
candidat. Aucun blocage irréversible de principe établi ; aucune justification
non plus pour promettre une cellule viable après quelques réglages ou en un
nombre ferme de lots. Le renouvellement en moins de dix heures n'est pas déduit
des benchmarks inertes ou de ces rendements.

Prochain jalon décisif : un mécanisme local de finition/recyclage ou spécificité
qui favorise les copies longues libérées/réutilisables sans rendre les outils
complets indisponibles. Deux changements conceptuels sans transfert ni diagnostic
nouveau imposent de réexaminer alphabet/représentation. Les répétitions de graines
et les branches de paramètres sont des essais automatiques, pas des avancées de
conception. Pas de nouvelles grilles de densité ou de dynamique inerte par défaut.

Une machine processive est une alternative à discuter, pas une primitive magique
à introduire : coût gène/expression/renouvellement et feu vert utilisateur requis.
Avant adoption de Langevin, la membrane, la catalyse et le bain commun doivent
être testés sous ce mouvement. Ces incompatibilités possibles, la synthèse de L,
la diversité des outils et l'homéostasie restent ouvertes. Aucune nouvelle
dépendance causale ni aucun outil ajouté dans LT1. Le dépôt conserve les recettes
et les démos antérieures, donc le diagnostic est réutilisable si le candidat échoue.

## Historique — compromis mouvement/calcul MIX2 avant lecture de la cohorte

L'utilisateur autorise les variantes inertielles à coût borné. Deux familles
locales et un témoin brownien apparié sont comparés ; aucune nouvelle fonction
biologique ni règle propre à une molécule. La géométrie initiale sans compression
évite de confondre échauffement préparé et meilleur transport. L'ancien moteur
brownien reste le défaut et les sources des campagnes antérieures sont figées.

Pilotes : gain de renouvellement local plausible ; DPD plus rapide physiquement
mais souvent plus coûteux que Langevin pour ce seuil. Ne pas choisir avant les
objectifs conjoints, la cadence et les coûts. La grille de18 essais, deux
travailleurs, borne l'exploration automatique ; les paramètres physiques et
horizons sont déclarés. Réévaluer après cette cohorte, sans ajouter une série
indéfinie de paramètres. Une classe n'atteignant aucun meilleur compromis doit
être abandonnée ou revisitée conceptuellement, pas sauvée par une métrique unique.

Le risque aval demeure : des contacts plus courts peuvent dégrader les réactions,
une inertie excessive la membrane, et le thermostat les fonctions de repliement.
Un gain mécanique ne prouve pas un gain cellulaire. Aucun blocage irréversible
de principe établi et aucune garantie d'optimum ou de facteur10 donnée.

## Transport et mélange MIX1 — 29 octobre 2026

L'observation visuelle utilisateur motive un diagnostic de transport sans
réactions, en parallèle de P10. Le moteur est brownien suramorti : aucune
vitesse persistante. La diffusion du centre d'un assemblage idéal de b billes
identiques est mu*T/b ; le temps de relaxation spatiale croît comme L²/D.
Cette dépendance rend les grands espaces et grands polymères réellement risqués,
même avec un moteur rapide. Le réalisme hydrodynamique n'est pas acquis.

MIX1 sépare dispersion, mémoire des positions, voisins et contacts. Le premier
essai froid trouve des seuils descriptifs vers360 pour les voisins et3970 pour
l'occupation, sans preuve de réaction ou d'équilibre durable. Cohorte incomplète,
ni blocage irréversible ni absence de problème de transport établis. Les dimères
fixes sans affinités ne représentent pas une protéine piégée dans la chimie.
Les témoins idéaux/denses et de cadence doivent précéder toute correction.

Budget borné : dix essais, un travailleur MIX1 en plus des deux P10, statistiques
compactes et checkpoints. Prochain choix conceptuel après lecture de la cohorte :
mécanisme de mouvement ou accès chimique, sans augmenter aveuglément bruit,
mobilité ou dose. Une future convection/inertie serait une variante physique
déclarée avec régressions de réaction et de membrane, pas une accélération
technique déjà prouvée. Pas de nouvelle machine moléculaire autorisée ici.

## Jalons génétiques P10 — 29 octobre 2026

La demande utilisateur de population issue d'un seul G long est prioritaire
avant correction T9. Tester dix symboles, abondance finie et volume/densité
contrôlés réduit une incertitude qui menace toute fermeture causale. Deux
pilotes se terminent, la cohorte longue de dix essais est lancée ; pas de
conclusion favorable ou d'obstacle irréversible déduit de ces premiers instants.
Coût : un observateur passif optionnel, zéro primitive ou outil chimique.

Le budget est borné à16 cycles par essai, deux travailleurs ; débit initial
environ1000 pas/s pour820 billes, coût de l'ordre d'une heure pour la campagne,
révisable avec la croissance et les témoins1620 billes. Ce sont des essais
automatiques, pas dix changements conceptuels. Prochain point de décision :
distribution, amplification et réserve libre à800/1600/3200, puis choix T9
ou réexamen de la représentation. Ne pas compenser un rendement nul par une
suite sans fin de doses/horizons. Pas de nouvelles enzymes sans proposition
et feu vert utilisateur, conformément au contrat.

## Priorité d'ingénierie GUI1

GUI2 : le minimum demandé permet maintenant d'examiner le bain J3 dans la GUI,
avec trois graines, et trois mécanismes séparés. Entrées comparées aux recettes
préservées, démarrage/lecture/recommencement vérifiés ; pas de nouvelle campagne
longue ni preuve de viabilité. Le client présente aussi les compteurs primaires
hors structures préparées. La vidéo et les outils avancés sont explicitement
reportés par l'utilisateur et ne doivent pas devenir un obstacle au retour
visuel ou une raison d'accumuler de l'ingénierie avant de regarder la cellule.

29 octobre2026 : l'utilisateur demande l'interface finale dès maintenant afin
de contrôler visuellement les choix et de préparer à terme des animations.
Qt/OpenGL et séparation par processus évitent de dépendre du dessin Pygame
par bille ; les états sont copiés et les effets graphiques restent indépendants.
Le rendu synthétique100000 billes+99999 liens atteint≈38 images/s sur Intel UHD
en1080p, sans coût de simulation/IPC/sélection inclus. Ce n'est pas un budget
de renouvellement. Lecture des graphes O(E), copies IPC et sélection restent
des coûts à profiler aux grandes tailles, sans promesse de montée illimitée.

Le lot GUI1 livre un socle et des vérifications d'identité dynamique, pas une
nouvelle capacité chimique. GUI2 rend désormais les scénarios visibles sans
attendre relecture/vidéo, reportées pour spécification ; les fonctions manquantes
restent déclarées.
Les limites membranaires, T9, diversité et maintien restent identiques.

## Réévaluation courante après J3

Clôture lot18 : N1 achevé, pas d'alerte médiane déclenchant N2 mais baisse cumulée
et frontière fine1 dégradée conservées. L'analyse flexible complète le triage,
sans en réécrire les seuils. Diagnostic T9 nouveau : deux gardes distincts,
simple ablation monomère insuffisante, et recapture d'extrémités menaçant aussi
les outils complets. Piste bornée : cohérence d'appariements des voisins liés,
avec témoins de séquestration ; aucune solution encore testée. Revoir ce choix
après un seul lot de mécanisme et transfert, pas une accumulation d'exceptions.

Lot18 : N1 encore incomplet, aucune raison d'en changer le candidat. Le suivi
N1→analyse→N2 conditionnel automatise les transitions déjà calculables et borne
le coût à six essais supplémentaires. Cela évite une conversation par seuil ou
lancement sans résoudre automatiquement les choix de chimie. Le prochain point
d'interprétation reste T9 ou la résolution des contacts, après le diagnostic
numérique ; pas une succession indéfinie de raffinements. Aucune hausse de
maturité ni diminution démontrée du nombre de décisions conceptuelles restantes.

Progrès matériel : la hausse finie d'inventaire obtient un transfert utile dans
les trois bains K16, deux ont G nouveau, deux F nouveau et un F exprimé fabrique
des produits ensuite incorporés. Pas de primitive ajoutée. Le boost est utile
face à l'ablation ; le changement de milieu n'interdit donc pas tout couplage.
Cela réduit une incertitude d'intégration, sans valider le maintien : un F
nouveau au mieux pour seize préparés et seulement le gène001.

Risque structurel concret : les fragments F libérés ne peuvent pas se recapturer.
Ils restent minoritaires face aux monomères accumulés dans J3 ; ce n'est pas
une explication établie de tous les échecs. Piste : recapture/finition par motifs
de voisinage liés bornés, avec contrôle de séquestration et parasites ; pas
de lecture de chaîne complète. La température commune a permis un transfert
rare, mais ses résultats n'ont pas encore passé le contrôle numérique.

N1 est le prochain horizon : six calculs automatiques, aucune nouvelle loi,
référence J3 explicitement réutilisée. Si le raffinement dt/2→dt/4 dérive, isoler
les cadences ; sinon ouvrir un seul test T9 avec références d'intégration.
L'ajout d'affinités sans diagnostic ou de densités toujours plus grandes est
écarté. Aucun obstacle irréversible de principe établi, mais une refonte reste
possible pour les gènes longs, la diversité et la synthèse membranaire.

Poursuite justifiée, projet encore exploratoire. L'incertitude baisse, sans
justifier une promesse de convergence en quelques dizaines de lots. Plusieurs
grands jalons restent non réalisés : L fabriqué puis inséré, deuxième fonction
utile sous lois fixes, génome plus long, alimentation/export et homéostasie.
Le coût des essais temporels est de plusieurs heures, pas une estimation de
renouvellement cellulaire. Pas de probabilité défendable de finir sous dix heures.

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

## GKA — horizon de décision rapproché

Un petit nombre de sites s'apparient déjà à froid ; un simple « pas de rencontre »
ne suffit pas. GKA mesure admissibilité et occupation sans modifier le candidat.
Le prochain horizon est six rejeux400, puis une seule prolongation de toutes
les graines froides ou une intervention conceptuelle motivée. Aucun progrès de
fonction ajouté et aucune certitude sur la durée du renouvellement. Ne pas
transformer le scénario de coût1000–10000 unités en marge haute ou probabilité
de terminer sous dix heures : la cinétique et les fonctions aval restent inconnues.

## Décision après GKA

Six rejeux exacts, diagnostic nouveau : double appariement absent dans froid0/1,
une ligation sans trimer dans froid2. Pas de nouveau taux. La cible autorise
une cellule construite : tester un outil construit et son témoin délié est plus
direct que multiplier les attentes pour l'amorçage depuis seuls monomères.
Pilote positif pour activité3 contre0, incorporation absente : pas encore un
transfert. Douze tâches1200 doivent trancher expression/usage/confinement, sans
changer les lois. Santé : décision ciblée et zéro dette chimique ajoutée,
mais T9 et fabrication de L restent des obstacles prévisibles. Volume restant
et probabilité d'un renouvellement sous dix heures toujours non estimables.

## Réévaluation après J1 — stocks, environnement et homéostasie

J1 achevé12/12. Le transfert matériel froid préparé existe3/3 en petite boîte,
et un témoin délié produit un F actif ; ce risque thermique n'est donc pas une
interdiction structurelle générale. En revanche, aucun produit n'est incorporé
dans les6 bains membranaires. La membrane reste fragile et les contextes de
confinement diffèrent. Les réactions réussies isolées ne se composent pas encore.

Le census montre un obstacle plus précis : produits monomères disponibles mais
plus éloignés du gène, pas de fragments F déliés dans les bains. Une intervention
de diagnostic nouvelle réduit l'incertitude ; aucune nouvelle loi ni fonction.
J2 doit dire si le grand domaine suffit à produire cet échec sans L. Réévaluer
après les12 témoins, avant nouveau helper. Une récupération dans une petite
boîte externe ne démontrera pas la cellule ni une solution à sa dilution.

Le froid préparé1 consomme presque ses précurseurs (4 P et4 R restants) tout
en laissant34 monomères isolés : l'homéostasie ne découle pas de la catalyse.
HOMEOSTASIS.md fixe accumulation, extinctions et récupération comme obligations.
La réversibilité/recyclage et l'inhibition locale restent des pistes non testées,
avec coût/gènes à déclarer si nécessaires. Le renouvellement intégré, la synthèse
L, la longueur/multigène et le volume final de conception restent incertains.

## Réévaluation après J2

J2 terminé12/12 : le grand domaine sans L suffit à raréfier les incorporations,
le compact les retrouve3/3 chez les préparés, mais aucun nouveau G/F complet.
Le candidat n'est donc pas convergé. Une meilleure description du verrou est
acquise ; multiplier des réglages de docking ne répondrait pas à ce constat.

J3 est une seule intervention d'inventaire, avec18 comparaisons et3 ablations
automatiques, pas21 principes nouveaux. Il remplit davantage la frontière déjà
dimensionnée, avec contrôles sans L. Si même le budget proche de la cible échoue,
revoir la capture/finition avant un autre balayage de densité. La correction des
parents initiaux est une dette de mesure, pas une amélioration chimique.

La cible de flux externe est clarifiée : injection au bord, absorption à la
sortie, concentrations et gradients émergents. Les tables actuelles à capacité
fixe ne la permettent pas encore directement ; des IDs stables et entrées/sorties
cohérentes sont une évolution technique nécessaire, pas un argument de blocage
chimique de principe. Distinguer ce coût du mécanisme cellulaire. Maintien,
bibliothèque, information longue et synthèse de L restent à prouver ; ni nombre
fiable de lots restants ni probabilité de renouvellement sous dix heures.
