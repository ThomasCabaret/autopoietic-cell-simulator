# Campagnes différées

Le plan courant `membrane_terminal_exchange.json` lance G1 sur trois graines à1500,
avec `terminal_exchange=true` et les diagnostics précédents. Comparaison aux six
témoins M1R conservés : aucun témoin recalculé inutilement. Le garde est une
nouvelle hypothèse de chimie locale, pas une amélioration déjà démontrée. Voir
[décisions](../research/BATCH_12_DECISIONS.md). `start_campaign.bat` utilise ce plan.

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
