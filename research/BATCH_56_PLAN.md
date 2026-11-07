# Lot56 — un noyau local commun pour C++ et CUDA

7 novembre 2026. Réorientation demandée vers l'exploitation du GPU. Le moteur
actuel est Python/Numba. Les sources C++ historiques sont archivées séparément.

CFN1 isole contacts, ressorts et angles dans une expression commune. Chaque
bille lit ses interactions incidentes et écrit sa propre somme. Le moteur garde
la sélection CPU de référence. Un scénario peut demander C++ ou CUDA pour cette
tranche. Les voisins, les forces spécifiques, le mouvement et les réactions
restent pris en charge par les composants existants du moteur dans cette tranche.

Simplification transférable. Les règles de copie consultent directement les
liaisons de chaque port. L'ordre des propositions, les tirages et les critères
géométriques servent de référence. Tester les anciens préfixes avant promotion.

Contrôles. Comparer les forces sur un état CP1, un préfixe intégré court et sa
reprise sur chaque backend. Mesurer séparément les forces avec transferts, les
forces sur un état déjà résident et le pas hybride complet. Le test résident
répète le même état jusqu'à cent fois pour mesurer le débit du noyau. Il ne
constitue pas une simulation de cent cellules.

La suite du portage dépend de ces mesures. La priorité de conception est de
garder les tableaux de particules, les forces et le voisinage compatibles avec
des données résidentes et une exécution par lots. Conserver le CPU comme oracle
et comme option utilisateur. Les règles chimiques et la cadence de réaction
restent la référence lors de toute comparaison d'implémentations.
