# Lot23 — Langevin dans les démos et transfert aux fonctions actuelles

30 octobre2026. Demande utilisateur : intégrer le candidat dans les microdémos
et les scènes actuelles, montrer son impact et l'enjeu avant de reprendre T9.
Lot de transfert, sans nouvelle loi chimique ni outil fonctionnel.

## Hypothèse, risque et comparaison

Le mouvement Langevin gamma0,1,m1 améliore des rencontres et des produits F
dans LT1. Il peut cependant altérer les durées de contact, le repliement des F,
les membranes et le transport du bain intégré. La localité/modularité du moteur
ne prouve pas cette compatibilité. Ne pas promouvoir le mouvement en défaut
universel avant les résultats. Les démos doivent montrer le candidat, y compris
ses échecs, à côté des références browniennes inchangées.

Étendre l'option racine mechanics aux hooks membrane,membrane_bath,coupled_bath,
avec les mêmes forces locales. Cache invalidé à chaque tick réactif même sans
événement rapporté. Aucun parcours de contour ou molécule dans la dynamique.
Température issue du bain ; thermostat externe indépendant par bille. Aucun
rescaling, clipping ou réglage par fonction. L'initialisation et les labels
restent séparés des réactions. Coût : vitesses et masse/frottement déjà présents,
audit passif étendu ; zéro espèce,port,état ou outil chimique supplémentaire.

## Budget figé : pilotes puis16 essais longs

Les six presets GUI existants sont les points de départ, sources historiques
préservées. Les trois microdémos sont copie T7, circuit C3B1 et molécules V8
isolées ; le bain J3 est proposé aux graines2/0/1. Pour chaque preset :
une référence brownienne recalculée et une variante Langevin0,1,m1. Même horizon,
température, dt, cadence de réaction et matériel initial.12 essais,2 travailleurs.
Les graines identiques appairent les conditions, pas les trajectoires aléatoires.
Choix des graines illustratif hérité du catalogue, pas sélection sur nouveau succès.

Ajouter quatre contrôles Langevin dt/2 : les trois microdémos et J3 graine2.
Doubler reaction_every et sample_every conserve leurs intervalles physiques.
Contrôles sélectionnés, pas preuve de convergence sur graines ou dt/4. Total16.
Ordre : six essais micro, trois contrôles fins micro, puis sept essais intégrés.
Deux pilotes préalables à5, membrane V8 et J3 graine2, sans dense trajectoire.
Arrêt pour interprétation si instabilité mécanique ou défaut de reprise ; pas
de réduction silencieuse de dt, de modification de loi ou de nouveau balayage.

Conserver l'état des campagnes, checkpoints30s, recettes sources figées et
rapport automatique progressif/final. Nouvel espace outputs/demo_motion_campaigns,
sans toucher aux anciens pointeurs. Aucun calcul dépend de la GUI.

## Mesures et décision

Lire nouveaux G/F complets libérés, activité d'un F exprimé, produits réellement
incorporés ; une chaîne préparée ou une réaction seule ne vaut pas renouvellement.
Pour V8 : contours et tailles depuis dimères isolés, fréquence sur grille
régulière et état final. Pour J3 : validité de frontière, incorporation des
molécules libres et transport échantillonné ; membrane initiale préparée.
Séparer inconnu/ouvert/fermé et censurer les non-événements à l'horizon.
Audit température/vitesse/déplacement sans rétroaction. Rapporter coût réel
complet des travailleurs, sans assimiler vitesse simulée et gain fonctionnel.

Comparer par preset, mouvement et pas. Une graine micro ne démontre pas la
robustesse. Exiger le transfert de fonction aval plutôt que l'addition de
réussites isolées ; ne pas masquer une régression par une correction de paramètres.
Le rapport s'arrête au constat : pas d'adoption ni correction automatique des lois.

GUI : conserver les six références et ajouter six variantes identifiées,
présentation adaptée sans emprunter un succès historique pour le candidat.
Afficher explicitement l'enjeu et les conditions. Vérifier pause, reprise,
signature, positions initiales appariées, passivité et checkpoint des hooks
étendus, notamment les vues des sous-chimies du bain intégré.

## Suite et santé

Une incompatibilité remet en question l'adoption générale de Langevin, pas
l'existence de la copie. Les références et outils d'analyse restent utilisables.
Après lecture des résultats, retour à T9 : finition/parasites. Une nouvelle
protéine exigerait une proposition chiffrée et le feu vert explicite ; aucune
n'est autorisée ou implémentée dans ce lot. Pas de nouvelle promesse de viabilité
ou de temps de renouvellement. Un lot de transfert borné,16 essais automatiques,
pas16 changements conceptuels.
