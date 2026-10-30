# Lot24 — clôture LT2 et diagnostic de la membrane sous Langevin

Demande : vérifier les essais puis continuer la priorité réelle. LT2 achevé16/16,
sans erreur. Ce lot est un diagnostic de transfert, pas une nouvelle protéine.
Langevin reste la base de travail : ne pas ralentir le mélange pour masquer
une chimie fragile. Les archives browniennes restent des témoins.

## Constat préalable et hypothèses

J3 : fractions de fermeture régulière browniennes≈73/79/79% pour graines0/1/2,
contre≈3/24/74% avec Langevin. Incorporation catalysée18/18/26 contre9/7/32.
Les deux membranes finales0/1 sont ouvertes. Le pas fin sur la seule graine2
ne répond pas au défaut de0/1. Aucun flux utile depuis un F exprimé dans le
nouveau bain intégré à l'horizon1200. Les microdémos positives ne compensent pas
ce constat. Les traversées pendant les états non classables restent inconnues.

Priorité : comprendre la perte de continuité du grand contour. Hypothèses
concurrentes : dissociation thermique prescrite puis éloignement des extrémités,
rupture mécanique par étirement, échange de partenaires, discrétisation ou
interférence du contenu. L'augmentation de rencontres n'est pas en soi un défaut.
Observer la première ouverture persistante de la graine0 vers41, sans réparation
globale ni reconnaissance de contour dans les lois.

## MD1, cinq contre-tests bornés

Même bain initial J3 graine0, horizon80, T0,08, deux travailleurs, checkpoints30s,
aucune trajectoire dense. Ordre : Langevin référence, Brownien référence,
Langevin sans dissociation aléatoire (bond_off_rate=0), Langevin sans échange
(contact_exchange_rate=0), Langevin au pas mécanique divisé par2 avec cadence
réaction/observation conservée. Sources/scénarios figés avant calcul.

Les deux ablations sont des lois distinctes de diagnostic, pas des corrections
adoptées. Zéro espèce, état, port ou outil supplémentaire. Mettre off_rate à0
ne supprime pas la rupture par étirement. Retirer échange peut empêcher l'insertion
et modifier la suite de tirages aléatoires : ne pas inférer une causalité unique
de la différence entre trajectoires. Le pas fin est un contrôle sélectionné,
pas une étude de convergence sur graines.

Mesurer continuité sur grille0,5, premières pertes, température cinétique,
incorporation et événements réellement nouveaux. Non-événement censuré à80 ;
une membrane fermée à80 n'est pas certifiée à1200. S'arrêter à cinq essais,
sans balayage de températures, bruit, mobilité ou forces.

## Loupe locale motivée, un seul rejeu sélectionné

Rejouer la référence Langevin graine0 jusqu'à80 avec le moteur archivé LT2.
Question : le premier épisode ouvert durable vers41 vient-il d'un contact
éloigné par étirement ou d'une perte stochastique suivie d'un échec de recapture ?
Observer l'appel update_faces sans changer son retour ni ses tirages. Classer
les pertes nettes par extension avant la réaction ; les ruptures immédiatement
réformées dans le même appel ne sont pas toutes identifiables par cette mesure.

Déclencheur : première perte nette après40,5 et avant41,5. Au plus24 molécules
membranaires près du contact, une unité simulée avant et cinq après, positions,
vitesses, occupations des ports et distances du contact perdu. Tampon précurseur
en mémoire borné ; aucune trace globale dense conservée. Au plus64 événements
détaillés dans40–43. Température/contacts globaux comme contexte, pas pilotage.
Vérifier le préfixe des historiques contre LT2 et la passivité sur un petit test.
Conserver sources, recette et hash avec la capture. Arrêter la capture après
la fenêtre ; poursuivre le rejeu uniquement pour comparer le préfixe à80.

## Décision et suite

Lire ensemble classification locale et ablations avant de sculpter une loi.
Une éventuelle correction devra préserver association de molécules isolées,
échange/insertion et perméabilité : ne pas rendre tous les liens irréversibles
pour faire réussir un contour préparé. Pas de nouvel outil sans accord explicite.
Si le diagnostic n'isole rien, le consigner ; pas de correction à l'aveugle.
Puis traiter le défaut membranaire identifié et revenir à T9/finition génétique.
La régression menace la fermeture matérielle et le maintien, pas l'existence
de principe du projet. Un jalon de diagnostic, cinq essais automatiques et un
rejeu instrumental sélectionné ; aucune promesse de cellule viable.
