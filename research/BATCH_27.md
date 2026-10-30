# Lot27 — T9E lancé, sans adoption dans les démos

[Plan et amendement technique](BATCH_27_PLAN.md). MD2/Langevin demeure la base
des neuf démos actuelles. T9E ne change ni bruit ni membrane et n'y est pas activé.
`visualizer.bat` → **Démos → État actuel · bain intégré** reste le choix principal.

## Progrès de conception et limites

Un seul nouveau choix local : les extrémités F peuvent recapturer G, sans lire
la longueur cible, une séquence entière ou l'identité d'un outil. Motif à deux
supports et leurs voisins directement liés, reconnaissance0,3. Zéro nouveau
type, port, taux, état physique, outil, gène ou particule. Le budget cellulaire
et le graphe causal restent inchangés. Le choix reste opt-in, expérimental.

Six contrôles à contacts idéaux, tirages conditionnés à accepter : l'ancien
garde apparie3/1/0 sites F pour monomères/F2/F3 ; T9E apparie3/3/2. F2 reçoit
effectivement sa liaison manquante seulement dans T9E. Ce n'est pas un résultat
cinétique ; la fixation des bouts d'un F3 complet confirme le risque d'interférence.
Sources et positions exactes conservées dans outputs/diagnostics/T9E_local_20261030T163016689411Z.

Audit passif enrichi : occasions G/F par degré F après géométrie, éligibilité,
exposition de sites préparés appariés, stocks libres/liés et ligation. Les
identités préparées ne parviennent jamais aux règles. Passivité et reprise
Langevin vérifiées, notamment PRNG, positions et liaisons identiques.

## Campagne conditionnelle

Job courant : outputs/expression_followups/followup_20261030T164244840888Z.
Deux travailleurs, checkpoints30s, phase A12 essais à1200 : ancien/T9E ×
graines0/1/2 × expression/outil préparé, chacun102 billes, T0,08, Langevin.
La petite boîte est un contrôle de mécanisme concentré, pas une cellule.

Le suivi calcule les rapports et décide lui-même selon les seuils prospectifs
du plan. Si finition améliorée sans forte interférence, phase B4 grands bains
MD2 (trois graines et un contrôle fin sélectionné),2118 billes, anciennes
références MD2 réutilisées. Sinon arrêt pour interprétation. Maximum16 essais
scientifiques et24h écoulées ; pas de nouvelle variante ou de retry implicite.
Toutes les sources et conditions des deux phases sont figées avant A.

- `expression_status.bat` : état, tâches, temps simulé et phase.
- `stop_expression.bat` : pause avec checkpoints, empêche la phase suivante.
- `resume_expression.bat` : reprise explicite après arrêt propre ; aucune tâche
  échouée n'est relancée automatiquement, plafond24h conservé.
- `report_0.json` et éventuellement `report_1.json` dans le job : résultats,
  provenance, expositions et raisons de sélection/refus. La sélection de B
  reste déclarée, pas une validation indépendante.

Premier job interrompu par WinError5 d'écriture du statut, sans tâche complète :
un échec technique et deux calculs partiels en pause, tous conservés. Le nouveau
job garde les critères chimiques ; seul le rename atomique Windows attend
brièvement en cas de verrou transitoire. Sept essais IO maximum puis erreur
propagée ; ce n'est pas un retry de simulation. La nouvelle orchestration
demande STOP au contrôleur en cas d'erreur. Deux pilotes techniques corrigés
(petit bain/grand bain à1) sont terminés sans erreur.

## Références et maturité

Les trois préfixes MD2 intégrés à5 sont exactement reproduits face aux sources
archivées : positions, liaisons, PRNG et état de mouvement. Catalogue21 entrées
recertifié sans modification des scénarios, seulement empreintes du code opt-in.
Le premier passage logiciel détectait ce verrou de catalogue, attendu après
changement de source ; les entrées sont réexaminées puis recertifiées.
Suite finale :154 tests réussis, y compris conflits de rename Windows,
reprise/passivité, porte de sélection/refus et contre-test d'outil complet.
Les deux premiers essais longs du job corrigé ont dépassé t690 sans erreur
au contrôle de remise de main ; ce statut provisoire n'est pas un bilan de cohorte.

Aucun gain de renouvellement en grand bain n'est encore établi pour T9E. Le
maintien cellulaire, les outils divers, la synthèse L et l'homéostasie restent
ouverts. Un diagnostic et un candidat local testable de plus, pas une fonction
autonome acquise. MD3 reste secondaire et non implémenté ; ne pas multiplier les
changements chimiques simultanés. Lire les cohortes et leurs gardes avant tout
réglage supplémentaire ou proposition d'une nouvelle machine moléculaire.
