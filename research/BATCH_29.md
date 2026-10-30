# Lot29 — expliciter les protéines, remettre I0 avant la copie

[Plan](BATCH_29_PLAN.md), [brouillon mécanistique](FUNCTIONAL_MECHANISMS.md).
Demande utilisateur : comprendre les fonctions possibles d'assemblages locaux,
leur mécanisme et leur renouvellement ; ne pas stabiliser la génétique en
supposant ce problème déjà résolu. Lot documentaire/conception, aucun essai,
nouvelle loi, protéine, gène ou primitive ajouté. Pas de campagne lancée.

## Conclusion de la lecture

Un rationnel existe : sites F qui co-recrutent des atomes libres, forces de
capture, motif catalytique borné à six billes, liaison réelle P–R et libération
du produit. Les preuves C3B1 sont conservées avec leur régime historique. Le
helper de taux est explicite ; l'activité n'est pas produite par la seule
géométrie. Le noyau utilise deux F voisins ; la chaîne001 n'est pas démontrée
minimale, et rien ne prédit24 unités.

L'audit du code actuel précise le manque d'expressivité : même catégorie pour
P_G/P_F et même catégorie pour R0/R1 dans la capture ; l'assembleur n'offre pas
de sélection EN/EA par sa séquence. Les possibilités d'angles dépendant des
symboles existent dans le moteur, mais MD2 pose les mêmes cosinus0,8 pour F0/F1,
sans préférences de flexion distinctes. Aucune fabrication L ni bibliothèque
de repliements fonctionnels sous ces lois communes. Source de lecture : HEAD
4345c8c, simulator/precursors.py, assembly.py, copy.py et scénario current_cell_s2.

Le brouillon décrit gabarit/pince de ligation, poche/repliement, charnière
mécanique, clivage/recyclage, transfert/insertion et marcheur processif. Pour
chaque famille : états/forces locaux, preuve ou hypothèse, échec possible et
test discriminant. Les effets collectifs peuvent se transmettre de voisin en
voisin ; aucune connaissance de la chaîne entière n'est permise. Helpers,
énergie et dépendances doivent rester explicites. Nouvelle machine soumise à
proposition/accord, pas implémentée au titre de cette discussion.

## Décision de priorité

I0 : choisir puis établir deux productions distinctes utilisables sous lois
fixes, ou justifier une architecture polyvalente dont les produits sont utiles.
Préparer les contrôles de sélectivité et d'interférences, puis transfert du
produit au processus suivant et expression de l'outil. Fabrication L comme
contre-test aval obligatoire. Reprendre la copie lorsqu'elle bloque le transfert
d'une fonction établie, pas une nouvelle grille génétique par défaut.

La longueur se déduit du mécanisme ; toute extension doit apporter quelque
chose de mesuré. Long filament de recrutement, pinces et travail mécanique
sont des pistes, pas un argument pour imposer24. Trois familles N/A/L n'impliquent
pas exactement trois protéines/gènes ; l'architecture reste conditionnelle.

## Correction de l'atlas et vérification

Révision02 : en-tête et gènes indiquent tailles inconnues ; séquences non
assignées ; brins schématisés interrompus plutôt que24 marques.24 et le total
nominal restent uniquement dans la comptabilité, aussi identifiée dans les
métadonnées et les sorties CLI. Les archives historiques sont conservées.
Sources, SVG/HTML et notes régénérés ; aucune configuration de simulation changée.

Neuf contrôles carte/audit réussis ; rendu SVG inspecté après régénération.
L'audit logiciel ne constitue pas une nouvelle preuve d'activité enzymatique.
Arbre, principes de conception, priorités, santé, maturité et journal mis à jour.
Maturité : prototype d'assembleur et couplages partiels, expressivité/fermeture
constructive encore ouvertes. Commit local, aucun push.
