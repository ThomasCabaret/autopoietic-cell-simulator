# Lot38 — L3 : capture cohérente et départ construit détendu

4 novembre2026. L2 a terminé20/20 et refuse ses deux critères thermiques.
Ce lot compare deux causes identifiées, indépendamment de MIN1M toujours actif.
Pas de nouvelle protéine, taux, pas de temps ou thermostat ; aucune adoption MD2.

## Diagnostic préalable et hypothèses

Rejeu sélectionné L2 no_boost0 : énergie angulaire des F initialement droits
51,2 ; première capture à0,01 : +2,503 de potentiel, dont ressort+0,224 et
attraction libre supprimée+2,279. Une transition/trois atomes enregistrés,
énergie incluant64 atomes ; positions, vitesses, PRNG et chimie exactement
égaux au contrôle non instrumenté jusqu'à2. Ce n'est pas un bilan complet de chaleur.

1. **Préparation native** : construire les quatre F01 dans la géométrie qui
   satisfait déjà leurs ressorts et angles locaux (cos0,8), au lieu de partir
   droits. Supports et nourriture identiques, pas de tirage supplémentaire.
   Initialisation seulement, jamais relaxation pilotée dans la dynamique.
   Ne résout pas l'énergie de repliement de futurs F exprimés : celle-ci devra
   être mesurée dans le bain commun. Un départ construit détendu est autorisé.
2. **Courbure de capture assortie** : remplacer la raideur35 par E/largeur²,
   soit5,556 avec les paramètres actuels. C'est la courbure du potentiel gaussien
   libre à son minimum, aucune nouvelle constante indépendante. Réutiliser ce
   ressort dans la mécanique et dans ΔU. Les niveaux de potentiel restent ceux
   du helper cinétique : **pas** une continuité énergétique complète ni un
   équilibre détaillé. La capture/libération peut encore échanger de l'énergie.

Même porte L2 et contacts compatibles0 dans tous ces cas. La nouvelle loi de
capture est réutilisable en principe pour P/R mais ne l'est pas encore dans
MD2 : il faudra tester expression/activité sous une chimie réellement commune.
Motif et forces locaux inchangés ; seule préparation native lit le plan initial.

## Cohorte finie

Réutiliser les trois L2_combined comme référence raide/droite (sources figées).
Trois graines × préparation seule / courbure seule / combinaison / split /
no_boost / no_tool : **18 nouveaux essais**, t100, un travailleur, checkpoints30s,
plafond1h. No_tool48 billes vs64 ailleurs, tirages distincts. Les autres variantes
conservent nourriture, supports, vitesses initiales/PRNG, seuls R préparés déplacés
si pose native ; split conserve cette pose au départ, puis n'a plus les liens.

Mêmes alarmes prospectives que L2, sans les assouplir : combinaison≥4 L et≥2
produits par paire dans≥2 graines, contacts latéraux≥1 dans≥2 graines, médiane L
au-dessus des trois témoins ; aucune attribution catalytique sans outil/liens.
Les trois graines doivent garder moyenne T75–100 dans0,04–0,12 et P95 après5≤0,24.
Absence d'événement censurée100 ; analyse/arrêt automatiques dans tous les cas.
Pas de nouveau balayage ni poursuite conditionnelle au-delà de ce budget.

Valider le préfixe L2 par défaut exact avant réemploi des références. Contrôler
énergie initiale, force/courbure, variation locale exacte avec la raideur dérivée,
reprise et observation passive. Conserver tous les échecs et les anciennes recettes.
Si les critères passent, prochain contre-test : P/R et énergie de nouveaux F,
puis insertion/rétention avec barrière de segments ; ne pas cumuler séparément
une réussite L3 et MIN1M comme preuve d'une cellule renouvelée.
