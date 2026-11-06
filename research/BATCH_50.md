# Lot50 — potentiel compétitif transféré au moteur

6 novembre2026. [Plan court](BATCH_50_PLAN.md), [suivi sélectionné](BATCH_50_HORIZON_PLAN.md),
[preuves compactes](BATCH_50_RESULTS.json). Intégration et simplification d'une
représentation, aucun nouveau type, gène ou outil fonctionnel.

## Loi et coût

CP1 devient une option `free_port_potential=competitive` du moteur partagé.
Le défaut `additive` conserve les références. Pour chaque contact libre e,
u est l'ancien potentiel tronqué, p=-u/A, S la somme des affinités incidentes :
E=sum(u_e/(1+S_i+S_j-2p_e)). A vient du puits existant, sans constante réglable
ajoutée. La capacité d'un port est bornée et le cas binaire reste exact.
La force dérive tout le potentiel, y compris les dénominateurs : une simple
pondération de forces binaires serait incorrecte.

Formation/rupture/échange lisent le delta dans un voisinage spatial borné :
termes modifiés jusqu'au second rang, partitions nécessitant le troisième.
Le motif initial touche deux L pour un contact, trois pour un échange.
La naissance H/T→L doit aussi repondérer les partitions des voisins : son
delta n'est pas seulement la somme des nouveaux puits. Aucun contour,
composant complet, origine alimentaire ou label d'observateur dans ces lois.
L'énergie libre/lié, les barrières P/R et les autres helpers restent déclarés ;
ce filtre n'établit pas une thermodynamique à équilibre détaillé.

Premier microbenchmark refusé : force15,4–16,2× et delta5,6–11,7× l'additif.
Allocations NumPy dans les boucles internes remplacées par des scalaires,
sans changer le résultat du noyau de référence (égalité exacte testée).
Dernier benchmark chaud : force1,81/1,85×, delta1,48/.97×, sur deux snapshots
CF1 conservés. C'est un coût local sélectionné, pas un facteur de vitesse de
cellule. Recettes et source non optimisée conservées ; premier échec non effacé.

## CC1 terminé : association réelle, fermeture encore fragile

Six essais à300, deux travailleurs, sources figées. Trois bains intégrés302
billes ; trois bains réduits104 billes,52 dimères H/T préparés indépendamment,
sans liaison latérale ni cycle initial. Ces dimères utilisent les atomes du
stock existant, aucun ajout de matière. Le sous-bain réduit partage les lois L
de l'intégré, mais retire P/R et outils : ce n'est pas une preuve de cohabitation
de toutes les fonctions dans les mêmes conditions.

| Cas | T tardive | Fermeture tardive | L fabriqués | Plus grand assemblage | Cycles finaux |
|---|---:|---:|---:|---:|---:|
| intégré0 | .08431 | 96,33% | 7 | 52 | 1 |
| intégré1 | .08824 | 43,47% | 10 | 28 | 0 |
| intégré2 | .08596 | 94,33% | 5 | 52 | 1 |
| isolé0 | .08644 | — | 0, tous préparés | 22 | 0 |
| isolé1 | .07791 | — | 0, tous préparés | 18 | 0 |
| isolé2 | .07982 | — | 0, tous préparés | 18 | 0 |

Ports finaux valides6/6, invariants intégrés0, température correcte6/6,
association isolée3/3. **Porte CC1 refusée** sur la fermeture intégrée graine1.
Les propositions de formation restent quelques centaines, et non des millions
de refus. Le défaut de frustration libre/lié est réduit dans ce domaine,
sans preuve générale. Aucun cycle isolé au dernier instant : association en
chaînes démontrée, vésicule depuis molécules isolées non démontrée sous CP1.
G/F nouveaux0 à300, hors porte fixée à cet horizon ; ne pas appeler cela une
preuve d'incapacité asymptotique, ni prétendre la production préservée.

## CH1 — suivi plus long, sélection explicite

Après interprétation des six résultats, quatre essais à1800 : trois isolés
et uniquement l'intégré1 ouvert. Lois, stocks, positions et cadences inchangés.
Le ralentissement idéal du centre de masse des chaînes (D≈.8/n billes) donne
une raison cinétique de prolonger ; il ne prédit ni fermeture ni stabilité.
Le plan précise le seuil de cycle simple/aire et la récupération intégrée.
Pas de premier passage mesuré : absence de témoin final n'exclut pas une
fermeture transitoire antérieure. Deux travailleurs/2h, checkpoints30s,
rapport puis arrêt, aucune exploration automatique supplémentaire.

Un conflit de lecture Windows a arrêté le superviseur, les travailleurs
continuant. Une surcouche archivée `recover_followup_monitor.py` réattache la
surveillance : retries bornés des lectures JSON seulement, ancien état d'erreur
conservé, sources figées et travailleurs inchangés, même échéance initiale.
Le contrôleur futur applique aussi cette protection. Ni tâche échouée relancée,
ni code physique modifié. État courant : `competitive_horizon_status.bat`.

**CH1 terminé4/4 avant clôture, porte refusée** sur les cycles isolés :

| Cas1800 | T tardive | Plus grand assemblage | Cycles simples finaux | G/F/L nouveaux |
|---|---:|---:|---:|---|
| isolé0 | .07893 | 30 | 0 | — |
| isolé1 | .07793 | 52 | 0 | — |
| isolé2 | .07975 | 34 | 0 | — |
| intégré1 sélectionné | .08370 | 56 | 1, aire250,55 | 2/5/22 |

L'intégré récupère94,33% de fermeture sur900–1800 : l'ouverture courte n'était
pas définitive dans cette trajectoire. Ce suivi sélectionné ne mesure pas une
robustesse générale ni un renouvellement ; ses outils initiaux restent fournis.
Les isolés s'associent davantage mais ne satisfont pas la fermeture finale.
**Aucun calcul actif à la clôture**, CF1 conserve sa pause scientifique.

## CE1 — observation finale motivée, pas une nouvelle campagne

Question : les bouts libres des chaînes isolées sont-ils simplement devant
une jonction admissible refusée ? Lecture passive des trois checkpoints finaux,
cinq paires d'extrémités seulement, sources d'analyse et moteur archivées.
Écart combiné des deux ports :12,68/12,83 ;17,70 ;36,77/22,00 pour un seuil.25.
Même la chaîne52 a ses bouts loin l'un de l'autre. Cela réfute une attente de
réaction sur une géométrie déjà admissible **à cet instant seulement** ; ni
historique des rencontres, ni causalité de rupture/absence de fermeture déduits.
La prochaine question est la courbure/souplesse des motifs liés et la formation
des configurations de fermeture, avant d'augmenter un horizon ou un taux.
[Source et valeurs](BATCH_50_CE1.json).

## Vérifications, démos et maturité

Gradient/capacité/binaire CP1 statique conservés ; nouveaux tests du delta local
contre potentiel complet (y compris troisième rang et ajout distant), naissance
H/T, passivité, checkpoint/reprise, stock préparé, portes et recettes CH1.
Sept préfixes historiques et deux préfixes compétitifs exacts. Les39 démos
natives ont été vérifiées et le catalogue recertifié ; elles restent EG1/EN1/CB1
sur leurs lois additives, explicitement représentatives du dernier candidat
visible, pas de CP1 en cours d'évaluation. Aucun résultat favorable inventé
dans la GUI. Vérifications finales consignées dans BATCH_50_RESULTS.json.
Suite finale :278 tests passent,39 démos natives vérifiées. Une première
exécution restreinte échouait sur les ACL des répertoires temporaires Windows ;
la reprise autorisée hors bac à sable passe. Ce refus d'IO n'est pas traité
comme un échec chimique. Les corrections de supervision ne modifient pas le moteur.
Une clarification finale de commentaire est suivie d'une régénération du
catalogue et11 contrôles passés. Les archives `diagnostic_recipes` reçoivent
la même protection Git des octets que `campaign_recipes` : les anciennes fins
de ligne sont conservées, sans changer le contenu scientifique ni ses hashes.

Aucun palier biologique relevé : M-01 conserve sa preuve historique séparée,
CP1 n'apporte ici qu'une association ; M-04 reste75 pour EG1 limité, refus EN1
et CC1 conservés ; C-02/Q-01 restent25, maintien intégré0. Information riche,
diversité de fonctions, protection/régulation de chaque espèce et flux/export
restent des gaps conceptuels. CH1 clos oriente maintenant vers la géométrie
des chaînes isolées ; la récupération intégrée sélectionnée ne relève aucun
palier. Pas de promesse que la suite soit seulement technique.
