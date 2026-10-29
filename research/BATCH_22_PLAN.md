# Lot 22 — bilans achevés et transfert cinétique vers la copie

29 octobre 2026. Demande utilisateur : lire l'état, agir selon les résultats,
solliciter un choix seulement si nécessaire. P10,MIX1,MIX2 sont achevés38/38.
Lot d'analyse puis contre-test d'intégration, pas une nouvelle recherche de
paramètres de mouvement. Sources anciennes et données conservées.

## Lecture des preuves avant décision

Vérifier les manifestes et sources des trois campagnes. Récapituler les dix
distributions P10 (séquences, longueurs, stocks, cycles, censures). Reconstituer
les arêtes depuis les événements de ligation, en utilisant le graphe **avant**
chaque tick de réaction ; comparer au graphe final du checkpoint et aux vrais
symboles conservés dans l'observateur. Cela distingue des matrices fragmentaires
réellement actives d'une simple corrélation avec l'accumulation de fragments.

MIX2 : comparer les trois graines froides par métrique et secondes de calcul ;
ne pas classer le mélange conjoint censuré à1600 comme plus lent que le témoin
allé jusqu'à12000. Conserver aussi le contrôle chaud et de pas, à une seule
graine. MIX1 : écart modèle idéal/avec cœurs et impact de cadence sur contacts,
sans interpréter le nombre de recroisements comme un taux de réaction.

## Décision ciblée LT1

Langevin gamma0,1,m=1,dt0,005 est retenu comme **candidat de transfert**, pas
adopté : coût inférieur à DPD pour plusieurs objectifs, gain chaud du mélange
conjoint, moins de primitives et pas de thermostat de paires. La séparation
entre rencontres et réactions reste le verrou aval. Ne pas multiplier les
benchmarks inertes avant de vérifier la fonction chimique.

Contre-test : le mouvement accéléré aide-t-il les copies complètes ou surtout
les matrices fragmentaires parasites ? Les résultats P10 montrent1/1/0 copies
G nouvelles pour400 monomères et une majorité de ligations sur fragments.
Ce test n'essaie pas encore de corriger T9 ni de créer une polymérase.

## Lois, configuration et budget figés

- Même P10 : un G0010110101,400 dimères G libres **ou**400 F libres,graines0/1/2.
  Deux bains séparés, sans membrane, sans fabrication P/R ni outil fonctionnel validé.
- T0,6,dt0,005,réactions tous les5 pas,cycle200/15,horizon3200. Rien changé dans
  les lois de reconnaissance, capture, ligation, capacité ou libération.
- Seul ajout explicite : `mechanics` Langevin gamma0,1,m1 ; les vitesses
  initiales Maxwell sont préparées après les positions. Géométrie et stock
  identiques à P10 ; ne pas substituer le départ sans compression de MIX2.
- Le brownien reste le défaut. Vérifier un préfixe P10 de50 bit-à-bit avec
  positions,PRNG et état chimique archivés avant de réutiliser ses références.
- Autoriser l'intégrateur pour le seul hook copy de ce test ; invalider la force
  en cache **à chaque tick de réaction**, y compris sans ligation rapportée,
  car appariement/déliaison changent les forces. Aucun cache de liens fixes
  réutilisé silencieusement pour la chimie.
- Deux pilotes à20,copy/expression graine0, puis six tâches à3200,deux travailleurs.
  Pas de variante DPD réactive, de nouveau gène ou de nouvelle protéine.
- Références P10 tasks0000–0005 réutilisées explicitement ; ne pas les relancer
  pour compter une nouvelle répétition. Modèle choisi à partir de MIX2 : suivi
  sélectionné, pas validation indépendante du choix de mouvement.

Mesures de population tous les10, audit génétique existant, audit thermique
passif tous les0,5,checkpoints30s,trajectoires denses désactivées. Initialisation
réactive éventuellement hors équilibre : lire température, extension et vitesse
avant de déclarer un gain. Pas de rescaling ou correction depuis les observateurs.

## Critères, interprétation et coût

Rapporter copies exactes détachées, génération, toutes les séquences/longueurs,
fraction de matière en fragments et monomères libres par symbole,aux temps800,
1600,3200 et par cycle. Censurer les non-événements et déclarer le seuil de
réserve <50% comme dans P10. Comparer supports de ligation depuis fragments
et depuis gènes complets ; stock accru ou réactions plus nombreuses seuls ne
constituent pas une amélioration. Mesurer le temps complet des travailleurs,
sans confondre temps simulé et coût réel.

Le coût ajouté est physique et logiciel : vitesse par bille et rafraîchissement
de forces aux ticks réactifs ; zéro alphabet,port ou réaction supplémentaire.
Tests : cache normal contre recalcul systématique, modifications non rapportées
dans react(),passivité,reprise positions/vitesses/PRNG,signature des scénarios
incluant mechanics. Maintenir les six démos avec signatures physiques inchangées.

Si le candidat ne conserve pas les réactions/stabilité, arrêter son transfert
pour interprétation. S'il accélère les parasites, traiter l'architecture de
copie/finition plutôt que donner plus de nourriture ou réoptimiser la diffusion.
Une éventuelle machine processive serait proposée séparément à l'utilisateur
avec son gène et renouvellement, et attendrait son feu vert. Pas de décision
d'ajouter cet outil dans ce lot.

Pointeur séparé outputs/transfer_campaigns,recettes figées et mêmes gestionnaires
de campagne. Le bilan doit préciser que même un succès de LT1 ne valide ni
membrane,ni chimie commune complète,ni maintien cellulaire.
