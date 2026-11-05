# Calibration des campagnes — stocks, espace, horloges et portée des conclusions

4 novembre2026, précision utilisateur. Ce contrat complète
[KINETICS_AND_PERFORMANCE.md](KINETICS_AND_PERFORMANCE.md) et
[AUTOMATED_EXPLORATION.md](AUTOMATED_EXPLORATION.md). Une durée humaine ou un
nombre de billes commode ne justifient pas un résultat négatif de mécanisme.

## Avant de lancer un calcul utile

1. **Question et conclusion permise.** Contrôle construit de règle, comparaison
   de débit à durée finie, ou recherche d’un régime durable ? Un contrôle forcé
   ne mesure pas une cinétique spontanée. Un crible opérationnel peut être
   utile sans garantir son horizon asymptotique ; le dire explicitement.
   **Précontrôle d'accessibilité avant campagne :** construire, lorsque possible,
   un contact orienté qui réalise le motif recherché et interroger le prédicat
   réel de la règle ou son audit partagé. Vérifier types, états, degrés, ports et
   options avant de régler concentrations et horizon. Une transition interdite
   par le modèle ne devient pas accessible par davantage de calcul. Ne pas
   recopier un prédicat approximatif dans le précontrôle. Lot46 : PI1 aurait dû
   être arrêté ainsi avant ses15 essais ; le garde courant bloque sa répétition.
2. **Bilan matière.** Types réellement disponibles, préassemblés, capturés,
   incorporés et détournés. Calculer la capacité stœchiométrique grossière du
   résultat recherché, avec la compétition pour les mêmes précurseurs. Un grand
   total de particules ne garantit pas l’abondance du type limitant.
3. **Concentrations et espace.** Rapporter nombre par aire en2D (volume en3D),
   géométrie, encombrement, frontières et localisation des réactifs. Séparer
   augmentation de stock à concentration constante et augmentation de densité.
4. **Horloges physiques.** Diffusion/mélange mesurés sur un cas proche lorsque
   disponibles ; sinon estimation idéale déclarée comme telle. Ajouter temps
   de persistance, cycles externes, capture/déliaison et libération. Un temps
   de mélange de billes libres ne vaut pas temps de rencontre d’agrégats réactifs.
5. **Occasions réellement testées.** Transport, accès aux sites, motif compatible,
   géométrie admissible, attente de réaction, stabilité/libération du produit.
   Des contacts fréquents ou une température correcte ne suffisent pas. Quand
   ces données manquent, déclarer la cause indéterminée et chercher une mesure
   ciblée plutôt qu’inférer une impossibilité.
   Pour des ports saturables, vérifier aussi les états avec partenaires concurrents :
   un test binaire peut préserver potentiel/force tout en masquant une attraction
   libre additive incompatible avec la liaison à un seul partenaire. Mesurer le
   coût de commutation et la fréquence des refus dans un motif peuplé avant une
   cohorte longue ; arrêter pour interprétation si ces refus dominent sans progrès.
6. **Horizon et contrôles figés.** Nombre de cycles ou cinétique de référence
   justifiant la durée ; fenêtres de stocks/production ; graines ; témoins
   pertinents ; budget et arrêt. Si un suivi est sélectionné après lecture,
   conserver le refus initial et annoncer le nouveau rôle/horizon avant calcul.

Il n’est pas obligatoire de multiplier les calculs pour remplir ce contrat.
Réutiliser inventaires, événements, checkpoints, résultats de transport et
calculs analytiques existants. Construire directement un mécanisme lorsque
sa nécessité est établie ; tester les propriétés qui pourraient le réfuter.
Une nouvelle campagne doit nommer la décision qu’elle éclairera.

## Rapport minimal à la remise de main

- Stocks réactifs initiaux et finaux, matière piégée/produite et données de
  disponibilité locale si nécessaires. Distinguer « non assemblé » de « libre
  de toute capture ». Les totaux globaux n’écartent pas une famine locale.
- Production par fenêtres temporelles et derniers événements ; conserver
  les absences censurées à l’horizon, sans les appeler taux nuls ou impossibilité.
- Occupations et contacts avec leur cadence, moment avant/après réaction et
  biais possibles. Pondérer par le temps les observations irrégulières.
- Critère initial inchangé, choix du suivi et limite de la conclusion.

Un temps de déliaison1/k n’est pas un temps d’évasion si le ligand peut être
recapturé. Les motifs productifs peuvent disparaître avant l’observation,
tandis que les mauvais persistent : une proportion de temps occupé ne mesure
pas la proportion des tentatives. Une intensité intégrée de réaction exige
ses conditions et conflits ; ne pas appliquer une borne Poisson à des contacts
corrélés et un bain non stationnaire sans justification.

## Application MX1 / MX2

`experiments/mixed_calibration.py` reconstitue les stocks depuis les vrais IDs
et événements conservatifs ; vérifie les liens finaux, calcule les concentrations,
fenêtres, derniers événements et occupations pondérées. Aucun nouveau pas de
simulation. Le collecteur MX2 l’exécute automatiquement pour chaque résultat.

MX1 commence dans une boîte12×9 avec P_G31/P_F30/R0 31/R1 30/H24/T24 libres
chimiquement, en plus des structures préparées. Il peut matériellement fournir
plusieurs copies G01 et F01, mais la capacité ne garantit pas leur cinétique.
À1200, mixed conserve des P/R et produit encore tard ; les témoins uncaptured
épuisent presque leurs P/R. Conclusion : débit génétique pénalisé dans ce domaine,
pas incapacité ou état stationnaire démontrés.

Le Langevin choisi a persistance10 et diffusivité idéale de bille libre0,8 ;
le mode lent idéal de densité sur12 vaut environ18,24 unités. Ce sont des repères
issus de l’intégrateur, pas des temps de mélange réactif mesurés. La rencontre
de tous les partenaires peut être bien plus longue. Les mesures MIX2 existent,
avec leurs propres tailles/conditions et censures ; pas de transfert automatique.
Le cycle de libération est200/15 : un pilote à100 précède sa première fenêtre
externe185, donc l’absence de copie libérée n’y est pas un échec établi.

MX2 conserve les stocks et porte toutes les comparaisons à2400, douze cycles,
pour tester à la fois le retard et une correction locale de capture. Les
références longues doivent retrouver l’intégralité des historiques/événements
observés de MX1 jusqu’à1200. La porte MX1 reste refusée.2400 ne devient pas
magiquement une preuve d’asymptote ; si la production reste tardive, le rapport
doit encore le dire. Aucun seuil d’arrêt adapté aux besoins de la cellule.

## Lien au premier test global non naïf

La cible utilisateur est une cellule construite, alimentée et capable de
maintenir ses populations/fonctions sous pertes et petites perturbations,
avec débouché des excédents et fragments. Avant ce test, chaque boucle requise
doit avoir un mécanisme local explicite et des indications de débit/ressources
compatibles avec ses pertes. Pas besoin d’avoir déjà prouvé la réussite globale,
mais aucune fonction indispensable ne doit être omise silencieusement.
Évaluer plusieurs renouvellements, absence de dérive et récupération, sans
promesse d’infinité ou reconstruction d’une information entièrement perdue.
