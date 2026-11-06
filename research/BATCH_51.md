# Lot51 — courbure correcte, relaxation collective lente

6 novembre2026. [Plan](BATCH_51_PLAN.md), [BC1 et provenance](BATCH_51_BC1.json),
[plan CR1](BATCH_51_RELAXATION_PLAN.md). Aucune loi chimique changée.
Le progrès est un diagnostic mécanique et un observateur temporel réutilisable.

## Diagnostic qualitatif et quantitatif

Les quatre instantanés CH1 sont lus sans faire évoluer ni restaurer leurs
checkpoints sous un moteur différent ; empreintes source/configuration
contrôlées, noyaux d'interprétation identiques. [Vue générée](BATCH_51_GEOMETRY.png).
Deux arcs, une spirale52 et deux longues chaînes peu courbées expliquent mieux
les bouts distants que le seul nombre de produits. Ce sont des états finaux,
pas leur histoire ni une attribution causale complète.

Pour deux dimères liés de longueur axiale r, les ports de largeur l et s et
une translation minimisée, le potentiel du moteur se réduit exactement à :

`E(theta) = E0 + k [r sin(theta/2) + (l-s)/2 cos(theta/2)]²`

avec `k=epsilon(1-exp(-8))/width²`, `E0=-epsilon(1-9exp(-8))`.
Le minimum `theta*=-2 atan((l-s)/(2r))` et la courbure du puits
`kappa=k(r²+(l-s)²/4)/2` sont dérivés, jamais lus par la dynamique.
Accord sur257 angles avec le noyau : erreur maximale2.7e-15 ; contrôles de
longueurs, signe, force au minimum et dérivée seconde. [Profil](BATCH_51_PROFILE.png).

Paramètres CP1 : l1/s.92/r.65, epsilon4/width.6/T.08. Angle préféré−.12292rad,
soit environ51,1 unités par tour. Écart angulaire harmonique local attendu
sqrt(T/kappa)=.18430rad, supérieur à l'angle préféré ; rendre une paire droite
coûte seulement.222T après translation. La préférence de courbure existe,
mais reste souple. Les écarts-types angulaires finaux mesurés.169–.204rad
sont cohérents en ordre de grandeur, sans établir un équilibre thermique
indépendant ni une loi statistique de chaîne entière.

## Une échelle de temps collective manquait

Hessienne numérique du squelette idéal ouvert, ressorts axiaux180 et contacts
liés uniquement. Trois modes rigides nuls, aucune instabilité significative ;
forces au point de référence<7e-13. La masse1 et damping.1 sont ceux de CH1.
Le ralentissement des petites perturbations donne :

| Nombre de L | Temps d'enveloppe du mode le plus lent |
|---:|---:|
| 12 | 20 |
| 22 | 39 |
| 34 | 348 |
| 52 | 1890 |

Les parois, contacts libres, réactions, grandes déformations et croissance
ne sont pas inclus. **Ce n'est pas un temps de fermeture prédit.** Cela rend
cependant1800 peu informatif pour exclure une relaxation lente52, surtout si
la chaîne s'est assemblée tard. Une bonne diffusion des monomères ne calibre
pas les mouvements collectifs des longues chaînes. Le refus CH1 reste conservé.

## Construction : observateur passif et CR1 borné

`LipidGeometryAudit` est optionnel dans le gestionnaire commun. Il échantillonne
taille, cycles simples/aires, écart des bouts et géométries libres de capture,
avec premier témoin macroscopique échantillonné. Aucun PRNG ou cache du moteur
touché ; aucune donnée renvoyée à la chimie. Une seule capture L au premier
témoin,104 billes dans CR1, historique borné et compteur de troncature.
État sauvegardé/repris dans les checkpoints ; passivité et reprise testées.
Les occasions sont géométriques/échantillonnées, pas une intensité chimique
exacte ; des cycles entre échantillons peuvent échapper à l'observation.

CR1 reprend les trois initialisations isolées à8000, mêmes lois et paramètres,
deux travailleurs/3h, checkpoints30s. Critères fixés avant lancement : ports
finaux valides, historique complet,T tardive<=.12 ; au moins2/3 avec enceinte
simple finale>=26L/aire>=54,43 et fraction macroscopique observée>=.5 sur6000–8000.
8000 représente≈4,2 temps du mode nu52, sans garantie d'équilibration du bain.
Rapport puis arrêt, aucun allongement/réglage automatique. Lire
`competitive_relaxation_status.bat`, arrêter/reprendre via les lanceurs associés.
Pas de nouvelle preuve biologique anticipée ; suivi sélectionné, pas cohorte
indépendante. Le témoin intégré CH1 n'est pas répété sans question nouvelle.

## Santé et fidélité à l'objectif

L'avancement est sain sous surveillance : une hypothèse structurelle testée,
un défaut de calibration identifié, aucun nouvel outil/règle pour forcer une
forme, pas de grille de constantes. La loi compétitive reste bornée spatialement.
Le cercle51, les composants, cycles et modes collectifs sont calculés uniquement
pour analyser et préparer des expériences, jamais dans les forces/réactions.
L'état initial construit et les helpers déjà déclarés ne deviennent pas des
preuves d'émergence, d'autonomie ou de thermodynamique complète.

Ce jugement n'est pas une garantie : diversité des fonctions par assemblage,
information riche, protection/régulation de chaque espèce et flux/export sont
encore des gaps. La localité ne suffit pas à les résoudre. Prochain jalon :
interpréter CR1, puis au plus une variante mécaniste justifiée si nécessaire ;
si aucune explication exploitable, revoir la représentation. Pas de promesse
de calendrier ni de « tout est désormais technique ».

Aucun palier biologique augmenté : M-01 historique séparé50, M-04 couplage
limité EG1 seul75, C-02/Q-01 sous-cas25, maintien0. La GUI reste39 scènes sur
leurs lois historiques ; catalogue recertifié, nouvelle chimie non promue.
Vérifications et statut des calculs à la clôture : [preuves compactes](BATCH_51_RESULTS.json).
