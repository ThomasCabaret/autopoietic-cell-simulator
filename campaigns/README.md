# Campagnes différées

**Clôture lot22 —29 octobre2026** : P10 terminé10/10, MIX1 terminé10/10,
MIX2 terminé18/18, puis LT1 terminé6/6, sans erreur. Aucune de ces campagnes
n'est active. [Bilan scientifique et provenance](../research/BATCH_22.md).
Les sections de lancement ci-dessous conservent les protocoles historiques.

**LT1, transfert réactif Langevin**, plan `transfer.json`, deux travailleurs,
six essais G/F séparés, lois P10 inchangées :

- `transfer_status.bat` : statut et population, dossier `outputs/transfer_campaigns`.
- `analyze_transfer.bat` : rapport par la source d'analyse figée de la campagne.
- `stop_transfer.bat` / `resume_transfer.bat` : pause et reprise des essais inachevés.
- `start_transfer.bat` : nouvelle campagne, sans écraser les résultats achevés.

Recette conservée : `research/campaign_recipes/LT1_20261029T172315655927Z`.
Pour restaurer cette recette, passer `--output outputs/transfer_campaigns` au
contrôleur générique : il met à jour le pointeur de ce répertoire. Sans cette
option, le répertoire par défaut est `outputs/campaigns`.
Langevin reste expérimental sur `copy` ; membrane et démos restent browniennes.

## Protocoles antérieurs et commandes de reconstruction

**MIX2 — variantes de mouvement**, deux travailleurs,18 essais bornés :
`motion_status.bat`, `stop_motion.bat`, `resume_motion.bat`, `analyze_motion.bat`.
Nouveau lancement : `start_motion.bat`. Pointeur séparé `outputs/motion_campaigns`.
DPD est limité au banc non réactif ; Langevin a depuis été testé dans LT1.
Aucune modification des démos.
Rapport automatique de coût réel jusqu'aux seuils, contrôles de température
et de pas. Voir [protocole](../research/BATCH_21_PLAN.md) et [pilotes](../research/BATCH_21.md).

**MIX1 en parallèle de P10** :200 molécules dans une demi-boîte, mécanique seule,
sans réactions. Un travailleur, dix essais et contrôles, pointeur séparé sous
`outputs/mixing_campaigns`. `mixing_status.bat`, `stop_mixing.bat`,
`resume_mixing.bat`, `analyze_mixing.bat` ; lancement neuf `start_mixing.bat`.
Voir [protocole](../research/BATCH_20_PLAN.md) et [premiers résultats](../research/BATCH_20.md).
Ces commandes ne modifient pas la campagne P10 courante ni son pointeur.

**29 octobre 2026 — campagne courante P10** : dix essais de population depuis
un unique G de dix symboles, copie G seule ou expression F seule, monomères
composites abondants et témoins de volume/densité. Voir
[protocole](../research/BATCH_19_PLAN.md) et [lancement](../research/BATCH_19.md).
`population_status.bat` affiche le statut et le recensement progressif ; les
commandes habituelles stop/reprise ciblent la campagne courante. Le rapport
`population_analysis.md/json` est aussi généré automatiquement à la fin.
Pas de nouvelles lois ou protéines, ni de preuve d'intégration cellulaire.

La suite conditionnelle du lot18 surveille N1, en fait l'analyse complète puis
lance `cadence_controls.json` seulement si une alerte prospective concerne le
raffinement le plus fin. Six essais N2 maximum ; ensuite arrêt pour interprétation.
Voir [protocole](../research/BATCH_18_PLAN.md) et [méthode](../research/AUTOMATED_EXPLORATION.md).
`start_followup.bat`, `followup_status.bat`, `stop_followup.bat`, `resume_followup.bat`
gèrent ce suivi borné. Le statut donne N1 et N2 ; le pointeur de campagne courant
reste N1, la préparation de N2 utilise un répertoire séparé. Arrêter le suivi
met N2 en pause s'il est lancé ; N1 conserve ses propres commandes de pause/reprise.
Une erreur exige inspection, aucune relance automatique d'échec. Le suivi doit
être repris explicitement après redémarrage ; aucune exécution ordinateur éteint.
Analyse N2 : `python experiments/analyze_cadence_campaign.py DOSSIER_N2 --n1 DOSSIER_N1`.

Le plan courant `numerical_refinement.json` teste N1 : six bains J3 K16 avec L,
dt0,001/0,0005, graines0/1/2 à1200, référence dt0,002 réutilisée explicitement.
Même chimie, réaction5dt et observation0,5 ; raffinement conjoint, pas chemin
brownien commun. Voir [lot17](../research/BATCH_17_PLAN.md). Plusieurs heures
possibles. Analyse détaillée après achèvement :
`python experiments/analyze_numerical_campaign.py outputs/campaigns/campaign_IDENTIFIANT`.
Les alertes automatiques ne certifient pas la convergence sur trois graines.

Le plan historique `density_transfer.json` teste J3 : inventaires×1/8/16, avec/sans
L, trois graines à1200, plus3 ablations du boost àK16.21 tâches et deux travailleurs,
jusqu'à2118 billes, sources figées et checkpoints. Plusieurs heures possibles.
Terminé21/21, [résultats](../research/BATCH_16_RESULTS.md). Aucun flux externe encore implémenté.

Le plan historique `compartment_controls.json` teste J2 :12 témoins sans L,
mondes globaux90×90/8×6, préparé/délié et trois graines à1200. Paquets/RNG
initiaux identiques à translation près ; aucun mur interne dans une cellule.
Voir [lot15](../research/BATCH_15_PLAN.md) et ses résultats terminés12/12.

Le plan historique `constructed_tool.json` teste J1 à1200 : mêmes atomes et positions
avec un F001 lié ou délié, trois graines, avec/sans membrane, audit génétique.
Voir [protocole et limites](../research/BATCH_14_BOOTSTRAP.md). Outil initial
exclu des F nouveaux. Les12 essais sont terminés, bilan dans BATCH_14_BOOTSTRAP_RESULTS.md.

Le plan historique `genetic_kinetics.json` rejoue les six témoins génétiques J0 à400
avec `genetic_audit=true` : occasions, exclusions et occupations, sans changer
les lois. Voir [lot14](../research/BATCH_14_PLAN.md) et ses résultats.
Le suivi froid3200 n'est pas choisi ; J1 teste directement un départ construit.

Le plan historique `common_bath.json` teste J0 sur quatre conditions et trois graines
à400 ; voir le paragraphe lot13 ci-dessous.

Le plan historique `membrane_terminal_exchange.json` lance G1 sur trois graines à1500,
avec `terminal_exchange=true` et les diagnostics précédents. Comparaison aux six
témoins M1R conservés : aucun témoin recalculé inutilement. Le garde est une
nouvelle hypothèse de chimie locale, pas une amélioration déjà démontrée. Voir
[décisions](../research/BATCH_12_DECISIONS.md) et [résultats](../research/BATCH_12_RESULTS.md).

Le plan historique `membrane_robustness.json` compare B avec échange et son ablation
sans échange, sur les graines0/1/2 à1500, avec diagnostic des ouvertures. Les
lois restent celles du lot10 ; les nouveaux champs analytiques ne pilotent rien.
Deux travailleurs, checkpoints60s, aucune trajectoire dense. Voir
[lot11](../research/BATCH_11_PLAN.md).

Le plan historique `membrane_kinetics.json` compare deux candidats séparés, B et B sans
barrière de lien, chacun sur les graines0/1/2 jusqu'au temps simulé1500. Deux
travailleurs maximum ; données locales, trajectoires complètes désactivées.
Ce test complète le lot9 ; ce n'est pas une cellule G/F intégrée.

Depuis la racine Windows :

- `start_campaign.bat` : prépare une **nouvelle** campagne figée et lance un
  contrôleur caché. Refuse un doublon si la dernière campagne est encore active.
- `campaign_status.bat` : état, temps simulé, pas/s et estimation de durée restante.
- `stop_campaign.bat` : demande une pause avec sauvegarde ; attendre le statut
  `paused` et la fin du contrôleur avant de fermer la machine.
- `resume_campaign.bat` : reprend les tâches inachevées, garde les tâches terminées.
- `analyze_campaign.bat` : produit `analysis.md` et `analysis.json` dans le dossier
  de campagne. Les premières transitions absentes sont censurées à la durée finale.

Le dossier courant est écrit dans `outputs/campaigns/latest.txt`. Ces commandes
ne tournent pas lorsque l'ordinateur est éteint/en veille, ne configurent aucune
relance au démarrage et n'envoient aucune notification. Un arrêt brutal peut
perdre le travail depuis le dernier checkpoint (par défaut60 secondes réelles).
Chaque reprise conserve les anciens dossiers d'essai. Une erreur est visible
dans `tasks/taskXXXX/state.json` et `worker.log`, jamais convertie en échec chimique.
Un état `interrupted` signifie que le verrou du travailleur n'est plus actif.

Pour une campagne précise, ou un plan modifié :

```powershell
python scripts/campaign.py prepare campaigns/membrane_kinetics.json
python scripts/campaign.py run outputs/campaigns/campaign_IDENTIFIANT
python scripts/campaign.py status outputs/campaigns/campaign_IDENTIFIANT --json
python scripts/campaign.py stop outputs/campaigns/campaign_IDENTIFIANT
python scripts/campaign.py analyze outputs/campaigns/campaign_IDENTIFIANT
```

La commande `run` au premier plan occupe le terminal ; le lanceur Windows utilise
le même contrôleur dans un processus caché. `--retry-failed` autorise explicitement
une nouvelle tentative après erreur, depuis le checkpoint disponible. Inspecter
l'erreur avant de l'utiliser. Les lois et les sources figées ne changent pas.

Les recettes de campagne ne contiennent que manifeste, plan et sources exactes :

```powershell
python scripts/campaign.py export outputs/campaigns/campaign_IDENTIFIANT --output research/campaign_recipes/K1_IDENTIFIANT
python scripts/campaign.py restore research/campaign_recipes/K1_IDENTIFIANT
```

`restore` crée une nouvelle sortie sans résultats ni état de progression, puis
`resume_campaign.bat` lance la reconstruction. Aucune archive existante écrasée.
Les hashes du manifeste, du plan et des sources sont vérifiés avant le calcul.

## Interprétation des diagnostics

Pour la membrane, les occasions sont lues **avant chaque réaction**, sans PRNG
ni écriture dans la chimie : rencontres de molécules nouvelles/anciennes,
faces libres satisfaisant la capture, face ancienne occupée face à une nouvelle
libre satisfaisant l'échange. Les compteurs sont des temps-face approximatifs,
pas une intégrale exacte du risque : conflits séquentiels, échanges dans l'autre
sens et ruptures/reformations dans le même pas ne sont pas tous dénombrés.

Les contacts effectivement changés et échanges effectués sont comptés à part.
L'insertion fermée vient de l'observateur global, jamais des règles. Les fenêtres
temporelles montrent l'évolution des expositions ; les premières transitions
sont regroupées par lois/protocole/horizon identiques. Kaplan–Meier traite les
censures, mais trois graines ne donnent pas une estimation robuste. Les graines
dupliquées ne sont comptées qu'une fois dans les courbes. Aucun ajustement
stationnaire de taux ni conclusion automatique d'impossibilité. Les autres
hooks peuvent tourner, mais leur éligibilité chimique est marquée non mesurée.

## Diagnostic des ouvertures du lot11

Le champ de manifeste `boundary_audit: true` ajoute un observateur indépendant,
avec le même échantillonnage0,5 que les mesures précédentes. Il conserve
`boundary_audit.json` auprès du résultat, et les résumés dans `analysis.json`/
`analysis.md`. Ses états : fermé, ouvert classable, fragmentation, grand écart
terminal, aire faible, croisement, inconnu résiduel. Il ne crée pas d'enveloppe
pour les périodes inconnues et ne classe pas les sondes pendant celles-ci.

Les extrémités proches ne prouvent pas l'étanchéité ; les durées d'épisodes sont
échantillonnées, avec transitions entre images. L'association avec un échange
récent ne prouve pas que celui-ci cause l'ouverture. Après campagne :

```powershell
python experiments/analyze_batch11.py outputs/campaigns/campaign_IDENTIFIANT
```

Ce contrôle recoupe le census avec les historiques et compare B aux résultats
K1 quand leurs données locales sont disponibles. Il conserve sa source et son
empreinte dans une nouvelle sortie d'analyse. Les témoins sans échange ne sont
pas attendus avoir les fonctions d'insertion du candidat actif.

## Exposition du garde G1

Quand `terminal_exchange` est activé dans les lois, le diagnostic distingue le
temps-face géométriquement éligible brut de celui qui satisfait aussi le garde.
Le rapport les affiche séparément. Ces observations sont pré-réaction : les
ruptures, conflits et changements de disponibilité au cours du tick empêchent
d'en déduire un hazard exact. Une bonne fermeture sans insertion reste un échec
fonctionnel du candidat, même si les sondes restent dedans.
## Lot13 : bain commun J0

Le lancement par défaut utilise `common_bath.json` :12 essais à400, quatre
conditions × graines0/1/2, deux travailleurs. `coupled_bath` réunit les vraies
billes P/R et L dans un même espace, température et ordonnanceur. Les témoins
natif/froid restent des candidats thermiques distincts. Lire BATCH_13_PLAN.md
et DESIGN_PRINCIPLES.md avant toute comparaison. Les tableaux d'analyse affichent
les vrais produits catalysés/incorporés et les contacts/passages échantillonnés.
L'éligibilité catalytique complète n'est pas encore mesurée par KineticProbe ;
les tableaux historiques d'échange indiquent donc « non mesuré » pour J0.
Les plans de membrane précédents sont conservés, pas relancés par défaut.
