# Lot 21 — variantes de mouvement et coût cinétique réel

29 octobre 2026. [Protocole](BATCH_21_PLAN.md). L'utilisateur autorise Langevin
inertiel et DPD, sous condition de comparer le rendement réel au coût numérique.
Le chemin brownien des démos reste inchangé ; nouveaux intégrateurs limités
au banc sans réactions. Aucune nouvelle protéine ou modification de chimie.

## Pilotes figés, sept calculs achevés

200 dimères, même boîte et géométrie initiale par graine, sans compression des
cœurs. T0,08, masse1, durée100. Tous les calculs de pilote sont achevés sans
instabilité. Recette : `campaign_recipes/MIX2pilot_20261029T130411143886Z`.
Données locales : `outputs/motion_pilots/campaign_20261029T130411143886Z`.

| Variante | dt | Premier seuil voisins, temps simulé | Calcul réel après échauffement | T cinétique après20, min–max |
| --- | ---: | ---: | ---: | --- |
| Brownien | 0,005 | absent à100 | censuré à6,04s | sans vitesse explicite |
| Langevin gamma4 | 0,005 | absent à100 | censuré à5,90s | 0,071–0,088 |
| Langevin gamma0,1 | 0,005 | 57,5 | 2,72–2,81s | 0,069–0,089 |
| DPD gamma0,5 | 0,005 | 45 | 4,16–4,27s | 0,076–0,103 |
| DPD gamma2 | 0,005 | 42,5 | 3,44–3,60s | 0,073–0,107 |
| Langevin gamma0,1 | 0,01 | 57,5 | 1,31–1,40s | 0,071–0,086 |
| DPD gamma0,5 | 0,01 | 37,5 | 1,57–1,66s | 0,079–0,094 |

Une graine, horizon court et contexte de charge réel : pas un classement robuste.
Le seuil est l'excès de cinq voisins initiaux<=0,1, pas un taux de réaction.
Les deux horizons censurés ne sont pas des temps d'échec ou des réussites omises.
À dt0,005, DPD atteint ce seuil plus tôt en temps simulé mais coûte davantage
en calcul que Langevin0,1. Augmenter dt semble utile, sans preuve de convergence
sur cette seule paire. Les extensions maximales de liens échantillonnées restent
entre0,077 et0,086 dans les variantes inertielles de ces pilotes.

DPD passe tôt par une occupation presque uniforme puis dépasse0,6 dans la moitié
droite : la MI reste élevée à100. Ce passage ne suffit donc pas à affirmer un
mélange complet. L'indicateur conjoint tenu cinq instantanés est ajouté dans
le protocole **avant les longs essais**, sans retirer les mesures séparées.

Le contrôleur du pilote a fini ses sept tâches puis son impression console a
échoué sur le symbole « supérieur ou égal » non représentable en CP1252 Windows.
Les résultats/rapports JSON étaient écrits. Logs et source figée conservés ;
correction d'affichage ASCII dans le script de la campagne suivante, aucun
calcul ou résultat physique du pilote effacé ou remplacé.

## Coût court, séparé de la cinétique

Mesure série après500 pas d'échauffement, trois blocs de2000 pas, dt0,005.
Sources et configurations dans
`outputs/performance/motion_20261029T132229005798Z` (hashes correspondant au moteur
archivé avec la campagne principale).

| Variante | Pas/s sans observateur | Pas/s avec diagnostics |
| --- | ---: | ---: |
| Brownien | 10478 | 5847 |
| Langevin gamma4 | 8009 | 5083 |
| Langevin gamma0,1 | 7603 | 3666 |
| DPD gamma0,5 | 2916 | 2729 |
| DPD gamma2 | 3759 | 2657 |

Ces petits blocs de densité précoce et trajectoires différentes ne donnent pas
une loi universelle de coût ; d'autres jobs peuvent être actifs. L'algorithme
DPD traite environ1300 visites de paires par pas dans les pilotes (deux passes),
contre zéro thermostat de paires pour Langevin. Les trois chemins ont environ
une évaluation conservative/pas. Le vrai classement doit utiliser les horloges
mesurées **jusqu'aux objectifs**, pas les seuls pas/s de ce tableau.

## Campagne longue,18 essais bornés

Recette : `campaign_recipes/MIX2_20261029T132411069082Z`.
Données : `outputs/motion_campaigns/campaign_20261029T132411069082Z`.
Plan : `../campaigns/motion.json`. Deux travailleurs, modèles intercalés par
graine ; toutes les variantes déclarées sont conservées, aucune sélection de
paramètre automatique après résultat. Horizons inégaux12000/1600 explicitement
déclarés et censures préservées. Chaque résultat garde positions/vitesses/PRNG
et force en cache dans ses checkpoints ; pas de trajectoires denses.

- `motion_status.bat` : statut et coûts jusqu'aux premiers seuils sauvegardés.
- `stop_motion.bat` / `resume_motion.bat` : pause et reprise explicites.
- `analyze_motion.bat` : rapport et courbes progressifs ; génération également
  automatique à la fin de la campagne via son code figé.

Sorties : `motion_analysis.md/json/png`, données par essai `mixing.json` et
`performance.json`. L'horloge des segments inclut forces, thermostat, voisinages
et observations ; elle exclut l'I/O de sauvegarde. Le temps total du travailleur
est rapporté séparément. Les démonstrateurs gardent leur mouvement brownien
antérieur ; les variantes ne sont pas appliquées à leur chimie.

## Localité, tests et portée

Les forces de ressort et de cœur restent par paires ; les amortissements sont
par bille (Langevin) ou par paire locale (DPD). Aucun centre de molécule, séquence
ou identité d'agrégat dans l'intégrateur. Les composantes lues par les statistiques
ne pilotent ni vitesse ni température. DPD conserve la quantité de mouvement de
chaque paire thermalisée, mais la boîte peut exercer une force externe.

Tests : vol libre, OU relatif exact, non-amortissement d'une translation commune
par le thermostat de paire à T0, passivité, reprise bit-à-bit de positions,
vitesses, PRNG et force en cache, horloges/censures et campagne figée. Les tests
logiciels ne remplacent pas les contrôles thermiques et de pas de la campagne.
Les six démos gardent les mêmes signatures physiques ; catalogue révisé pour
les empreintes du moteur étendu.

La compatibilité avec capture, orientation, ligation, repliement et membrane
reste à tester avant adoption. Le choix de thermostat n'est pas fait. La maturité
chimique n'augmente pas par ces seuls diagnostics ; le prochain choix doit suivre
le gain cinétique réel, la stabilité et la simplicité, pas l'apparence du mouvement.

## Première comparaison longue, graine0 — cohorte incomplète

Les deux variantes rapides0 ont atteint1600 ; le témoin brownien a dépassé7900.
À dt0,005, les seuils mesurés sur ces préfixes donnent :

| Seuil, secondes de calcul après échauffement | Brownien | Langevin0,1 | DPD0,5 |
| --- | ---: | ---: | ---: |
| Renouvellement des voisins | 17,56–17,61 | 1,98–2,03 | 4,83–5,00 |
| Occupation presque uniforme | 119,01–119,05 | 3,60–3,63 | 4,48–4,66 |
| Perte de mémoire spatiale | 124,88–124,92 | 7,63–7,67 | 16,42–16,51 |

Ces gains concernent des seuils séparés, sur une seule graine et sous charge
réelle de machine variable. Aucun des trois préfixes n'a encore atteint le
critère conjoint avec50% des partenaires : ne pas présenter le tableau comme
un temps de mélange intégral ni un gain de réaction. Température inertielle
sur tout le parcours20–1600 : Langevin0,067–0,091 et DPD0,069–0,103, cible0,08.
Les autres graines et contrôles restent à lire. Courbes progressives dans
`outputs/motion_campaigns/campaign_20261029T132411069082Z/motion_analysis.png`.

Validation finale :127 tests logiciels et7 historiques passent ; six démos
vérifiées à signatures physiques inchangées. Les nouvelles recettes sont
validées par empreintes ; les données restent locales. Au dernier contrôle,
les anciennes campagnes P10 et MIX1 sont terminées10/10 sans erreur, sans
changement de leurs sources ; leur bilan complet reste à interpréter séparément.
