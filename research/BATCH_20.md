# Lot 20 — MIX1, agitation mécanique mesurée sans réactions

29 octobre 2026. [Protocole](BATCH_20_PLAN.md). Demande utilisateur de séparer
diffusion dans l'espace, mémoire des identités et renouvellement des rencontres.
Le moteur brownien suramorti existant est conservé : pas de vitesse mémorisée,
ni convection. Nouveau hook de diagnostic, pas une nouvelle chimie candidate.

## Pilotes terminés

Deux essais de20 temps simulés,200 dimères soit400 billes dans la moitié gauche
d'une boîte24×18. Ressort et répulsion de G/F, sans affinité ni réaction.
Recette : `campaign_recipes/MIX1pilot_20261029T122635170202Z`.
Preuves locales : `outputs/mixing_pilots/campaign_20261029T122635170202Z`.

| Mesure à20 | T=0,08 | T=0,6 |
| --- | ---: | ---: |
| Temps réel du travailleur, initialisation comprise | 1,469s | 1,703s |
| D apparent court, loin des murs | 0,00984 | 0,07241 |
| D idéal du centre prédit | 0,01 | 0,075 |
| Molécules dans la moitié droite | 0% | 5,5% |
| Fraction brute des cinq voisins initiaux conservés | 0,603 | 0,224 |
| Partenaires uniques par molécule à rayon0,3 | 1,66 | 6,54 |

Le benchmark échauffé initial, hors archivage/checkpoint, donnait environ0,76s
pour20 ; ne pas le comparer aux temps complets de travailleur comme un gain
chimique. Les contacts recensent t=0 compris. Ils utilisent les reconnaisseurs,
sans condition de symbole, angle ou éligibilité réactionnelle. Leur nombre
n'est donc pas un rendement de réaction.

## Campagne longue figée et lancée

Recette : `campaign_recipes/MIX1_20261029T123103222882Z`.
Données : `outputs/mixing_campaigns/campaign_20261029T123103222882Z`.
Plan : `../campaigns/mixing.json`. Dix essais, un travailleur. P10 conserve
son propre pointeur `outputs/campaigns/latest.txt`, ses sources et travailleurs.
MIX1 a un pointeur séparé `outputs/mixing_campaigns/latest.txt`.

- `mixing_status.bat` : état des tâches et dernière statistique sauvegardée.
- `stop_mixing.bat` / `resume_mixing.bat` : pause propre et reprise explicite.
- `analyze_mixing.bat` : rapport et courbes progressifs. Analyse automatique
  également à la fin de la campagne, avec le script figé dans sa recette.

Sorties : `mixing_analysis.md/json/png`, ainsi que `mixing.json` par essai,
résultats et checkpoints. Aucune trajectoire dense, ni enregistrement vidéo.
Les processus continuent après la conversation si la machine reste active ;
pas de relance après arrêt supposée ni de notification configurée.

## Premier préfixe long — une graine froide, cohorte incomplète

| Temps simulé | Fraction à droite | Voisins initiaux conservés, brut | MI corrigée normalisée | Partenaires uniques, rayon0,3 |
| --- | ---: | ---: | ---: | ---: |
| 100 | 0,055 | 0,330 | 0,586 | 4,93 |
| 500 | 0,135 | 0,125 | 0,447 | 14,24 |
| 1000 | 0,210 | 0,062 | 0,333 | 22,09 |
| 2000 | 0,285 | 0,046 | 0,192 | 33,87 |
| 4000 | 0,415 | 0,033 | 0,091 | 52,98 |

Référence de hasard des voisins :5/199≈0,0251. Premiers passages descriptifs
de cette graine : excès de voisins<=0,1 à360 ; mémoire de position<=0,1 à3280 ;
occupation droite0,4–0,6 avec TV spatiale sous le seuil à3970. Ce ne sont ni
des temps moyens sur graines ni un certificat d'équilibre durable.
La référence multinomiale de TV utilise des points indépendants ; les centres
avec répulsion ne le sont pas. C'est un plancher descriptif, pas un test de
significativité de l'équilibre.

Le premier essai a depuis atteint12000, en370,25s de travailleur :48,5% à droite,
TV=0,060, rétention brute des voisins0,031 (hasard0,0251), MI corrigée0,0266,
et99,84 partenaires uniques moyens au rayon0,3. D court≈0,009903. Ce cas se
disperse et perd largement la mémoire initiale ; il ne représente ni trois
graines ni un bain chimique avec séquestration. Les autres tâches continuent.

Cette distinction réduit une ambiguïté de la lecture visuelle : les molécules
peuvent rencontrer de nouveaux voisins bien avant le remplissage global.
Elle ne permet pas de conclure que l'accès des vraies protéines/matrices dans
la membrane est suffisant. Les pièges chimiques ont été retirés et la grande
taille des polymères n'est pas testée ici. Le thermostat donne idéalement
D=mu*T/b pour b billes ; l'extrapolation en taille est un risque à traiter.

## Vérifications et prochaine décision

Six nouveaux tests : passivité exacte des positions/PRNG, reprise avec contacts
et MI, information/graphes contrôlés, absence de réactions et de dérive sans
bruit/forces, diffusion idéale du centre en1/b, campagne figée et rapport.
Les18 tests ciblés mélange/campagnes/catalogue passent ; la suite complète
de121 tests et les7 historiques passent. Les six scénarios GUI conservent
leurs signatures physiques ; leurs empreintes de code sont révisées pour
l'ajout du hook/observateur diagnostique uniquement.

À lire ensuite : trois graines froides/chaudes, contrôles idéaux et sensibilité
des rencontres à la cadence. Distinguer les temps locaux utiles des temps
globaux. Aucun choix d'inertie, convection, nouveau bruit ou nouvelle enzyme
effectué dans ce lot. Maturité chimique inchangée.
