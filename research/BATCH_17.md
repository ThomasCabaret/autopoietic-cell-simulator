# Lot17 — J3 analysé, N1 temporel

28 octobre2026. BATCH_16_RESULTS.md donne le bilan complet21/21 : le stock
dimensionné restaure du transfert utile dans un bain commun. Un F exprimé y
fabrique des produits ensuite utilisés, mais aucun essai ne cumule cela avec
nouveau G. Seize outils initiaux pour au mieux un nouveau F ; pas de maintien.

Choix prioritaire : vérifier la discrétisation avant de retoucher la finition
des fragments. N1 garde toutes les sources du simulateur, les lois résolues,
positions, liaisons et PRNG initiaux. Seuls dt et intervalle d'observation en
nombre de pas changent. Six tâches2118 billes à1200, graines0/1/2,
dt0,001/0,0005 ; réutilisation déclarée des trois témoins J3 àdt0,002.
Réactions toujours5dt : test de raffinement conjoint, pas effet mécanique isolé.
Mêmes graines ne signifient pas même chemin brownien après modification de dt.

Le générateur vérifie les six états initiaux, chimies et intervalles d'observation
identiques0,5. Le comparateur vérifie les hashes du simulateur, configurations,
résultats et vrais IDs de matière ; il conserve les lignes par graine et les
alertes prospectives de BATCH_17_PLAN.md. Trois graines et quelques chaînes
ne certifient pas une convergence même si les médianes ne déclenchent rien.

Pilote sélectionné dt0,0005,graine0,t2 :2118 billes, aucune erreur,3 dimères
catalysés, zéro incorporation ou chaîne nouvelle et zéro contact P/R–L.
Un démarrage technique, pas preuve de convergence ni rétention. Recette source
seule référencée par BATCH_17_PILOTS.json, données locales conservées.

Les voies de finition restent à étudier sans inspection de chaîne complète.
Les petits motifs liés pourraient permettre la recapture ; cette piste n'est
pas implémentée et devra contrôler l'agrégation parasite. Aucun nouveau gène
ou type ajouté ; frontière, L fabriqué, diversité et homéostasie restent ouverts.

Validation avant gel :91 tests logiciels et7 historiques passent. Les31 sources
`simulator/` sont byte-identiques à J3 ; rejeu de référence àt2 exactement
identique pour positions, état chimique et PRNG. Six états initiaux et leurs
intervalles vérifiés. Comparateur : contrôles de triage sans dérive, dérive
sur quatre grandeurs, transition vers zéro et cohorte incomplète vérifiés.

## Lancement figé

Campagne `campaign_20261028T073131539788Z`, code770d9b3, six tâches1200,
deux travailleurs, checkpoints60s. Recette source seule dans
`campaign_recipes/N1_20261028T073131539788Z`. Au premier contrôle : deux tâches
actives, quatre en attente, aucune erreur. Le pipeline d'analyse partielle
vérifie références, sources et configurations ; il indique correctement que
les cohortes ne sont pas achevées et ne certifie aucune convergence.

Suivi `campaign_status.bat`, pause `stop_campaign.bat`, reprise
`resume_campaign.bat`. Analyse détaillée :
`python experiments/analyze_numerical_campaign.py outputs/campaigns/campaign_20261028T073131539788Z`.
Les rapports complets restent locaux. Aucun résultat long anticipé.
Rechargement effectif des deux premiers checkpoints vérifié àt84,5 et85 :
continuité disponible, sans arrêt ni modification des travailleurs actifs.
