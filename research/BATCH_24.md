# Lot24 — diagnostic local de la grande membrane, après LT2

30 octobre2026.

LT2 est achevé16/16, sans erreur. [Résultats complets](BATCH_23_RESULTS.md),
[plan du présent lot](BATCH_24_PLAN.md). Langevin reste la base de travail,
sans ralentir le mélange pour cacher un défaut chimique. Aucun nouvel outil
moléculaire ni changement de l'alphabet, des ports ou du budget de particules.

## Décision de priorité

La régression intégrée est suffisamment importante pour précéder T9 : fermeture
Langevin2,6/23,6/74,2% contre73,2/79,1/78,6% sur graines0/1/2. Les rendements
de fabrication seuls ne mesurent donc pas un gain cellulaire. Un bain dont
la membrane s'ouvre compromet l'interprétation des renouvellements génétiques.
Cela n'établit pas une impossibilité de principe de l'univers chimique.

## Loupe : contact47–48 de la graine0

Rejeu sélectionné jusqu'à80 avec les sources archivées de LT2. Les historiques
membrane et génétique et les événements génétiques reproduisent **exactement**
leurs préfixes LT2, sans tirage ou rétroaction de la loupe. Tests de passivité
positions/vitesses/PRNG/liens et de budget local réussis2/2.

La première perte nette dans la fenêtre40,5–41,5 survient à40,53, contact
47–48, faces0/1. Au moment de la perte :

- extension maximale des deux distances de squelette0,02375, bien inférieure
  au seuil de rupture mécanique0,35 : **dissociation aléatoire**, pas rupture
  par étirement ;
- distances H–H≈1,024 et T–T≈0,987, proches des repos1 et0,98 ;
- pourtant écart quadratique des ports q≈1,278, contre q<0,0625 requis pour
  recapture. Juste avant la rupture, q≈1,267 alors que le lien existe encore ;
- aucune observation compatible avec la recapture, ni reformation de ce lien,
  dans les cinq unités suivantes. À45,5 les distances atteignent≈2,86/2,92.

Le défaut observé n'est donc pas seulement « moins de rencontres » : un contact
lié peut dériver loin de la géométrie que son état libre exige pour se relier.
La mécanique liée maintient surtout les distances avec des angles faibles ;
la capture libre exige la coïncidence de deux ports. La dissociation laisse
alors deux faces peu attractives et non capturables, qui finissent par s'éloigner.
L'analyse géométrique utilise le même port_geometry et vérifie son hash contre
la source capturée ; pas une approximation dessinée a posteriori.

Six molécules seulement ont été retenues dans le rayon local, sous le plafond24,
avec601 instantanés (une unité avant, cinq après, cadence0,01) et au plus64
événements détaillés. Température et occupations de ports servent de contexte.
La température membranaire près de la rupture est≈0,118 ; son rôle causal
indépendant n'est pas isolé. Sur le rejeu complet,367 ruptures sont rapportées
par la règle,308 pertes nettes classées aléatoires ; une rupture suivie d'une
reformation dans le même appel n'est pas toujours identifiable par différence.
Ne pas interpréter ces nombres comme une fréquence universelle du mécanisme.

Les échanges acceptés du même essai LT2 n'arrivent qu'après1195 : ils ne
peuvent pas déclencher l'ouverture vers41. Leur routine consomme toutefois du
PRNG même sans échange accepté ; l'ablation change donc les trajectoires.

## MD1 : cinq contre-tests à80

Même bain initial graine0, aucun nouvel objet. Les ablations ne sont pas des
corrections adoptées. Langevin de référence, Brownien témoin, suppression de
la seule dissociation aléatoire, suppression de l'échange, et pas mécanique
divisé par2 en conservant la cadence physique des réactions/observations.

**Les cinq essais sont terminés5/5, sans erreur ni contrôleur actif.**

| Variante à80, graine0 sélectionnée | Fraction régulière fermée |
| --- | --- |
| Langevin de référence | 38,5% |
| Brownien témoin | 79,5% |
| Langevin sans dissociation aléatoire | 100% |
| Langevin sans routine d'échange | 75,8% |
| Langevin au pas mécanique divisé par2 | 79,5% |

Le pas fin change aussi la trajectoire et les tirages rencontrés : son résultat
seul ne permet ni d'exclure un effet numérique ni de l'établir comme cause
principale. L'incompatibilité de géométrie reste directement mesurée dans le
contact sélectionné ; sa prévalence et son amélioration aux pas fins restent
à valider. Ces horizons courts ne certifient ni survie à1200 ni insertion durable.

Le témoin sans échange n'autorise pas une explication causale par un échange
accepté : il n'y en avait déjà aucun avant80 dans la référence. Le résultat
souligne la variabilité entre chemins aléatoires et la fragilité du candidat.
En revanche supprimer la perte aléatoire prévient ce mode de rupture précoce ;
cela ne prouve pas que rendre les contacts durables partout soit une bonne
solution pour l'assemblage, l'insertion ou le renouvellement.

## Suite concrète et critères de transfert

Priorité MD2 : rendre cohérentes les géométries des contacts liés et libres.
Piste : réutiliser le même motif local à quatre billes H/T pour stabiliser
l'orientation d'un contact lié, plutôt que conserver deux exigences indépendantes
ou supprimer toute réversibilité. Une simplification de la dissociation imposée
reste une alternative à comparer, pas un acquis. Aucun port ne reconnaît une
membrane entière, aucun contrôleur ne répare un contour global.

Avant campagne longue : montrer sur un contact local que le motif corrige
le désalignement tout en gardant rupture/échange accessibles. Puis transférer
à des molécules initialement isolées, insertion depuis l'intérieur et grand
bain sous lois figées, avec ablations et contrôles de pas. Si deux modifications
conceptuelles n'apportent ni transfert ni diagnostic nouveau, réexaminer la
représentation. T9, copie longue/finition, reste la priorité suivante ; aucune
nouvelle protéine sans proposition et accord utilisateur.

## Provenance, incidents techniques et maturité

Campagne locale : `outputs/membrane_diagnostic_campaigns/campaign_20261030T105849083917Z`,
recette `research/campaign_recipes/MD1_20261030T105849083917Z`. Contrôleur/source
figés, checkpoints30s, deux travailleurs, rapport automatique, cohorte5/5 vérifiée.
Plus aucun essai de LT2/MD1 n'est actif à la remise de main. Suivi
`membrane_diagnostic_status.bat`, pause/reprise par les wrappers correspondants.
Le premier contrôleur lancé dans le bac à sable a été arrêté sans essai produit ;
reprise hors bac autorisée, traces conservées. Pas un échec chimique ni un nouvel essai.

Capture locale : `outputs/membrane_loupes/MD1_selected_loupe_s0_20261030T110121719037Z`,
avec scénario, moteur archivé, résultat, driver, loupe.json et ses hashes.
Analyse : `analysis_20261030T110837878776Z/report.json` et `geometry.png` dans
ce dossier ; sources d'analyse versionnées dans experiments/. Synthèse LT2
source-vérifiée : `outputs/reviews/LT2_20261030T110228432285Z`.
Recettes et hashes de drivers : BATCH_24_RECIPES.json ; copies exactes des
sources sous `research/abstract_runs/MD1_loupe_20261030T110121719037Z`.
Les données brutes et figures restent locales ignorées par Git.

Maturité : diagnostic mécanique/chimique concret obtenu, pas encore de correction
validée. Le maintien et la fermeture constructive complète restent ouverts.
Ce lot comprend cinq essais automatiques et un seul rejeu instrumental sélectionné,
pas une nouvelle grille de paramètres ni un nouveau mécanisme biologique.
