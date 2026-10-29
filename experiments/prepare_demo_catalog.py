"""Build reproducible GUI presets from preserved research inputs, not result data."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve


def signature(cfg):
    resolved=resolve(cfg)
    payload={k:resolved[k] for k in ('model','seed','duration','engine','chemistry')}
    if 'mechanics' in resolved:payload['mechanics']=resolved['mechanics']
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def origins():
    manifest='research/campaign_recipes/J3_20261027T192723206222Z/manifest.json'
    data=json.loads((ROOT/manifest).read_text(encoding='utf-8'))
    items=[]
    for seed in (2,0,1):
        task=next(t for t in data['tasks'] if t['label']=='J3_k16_bath' and t['scenario']['seed']==seed)
        items.append((f'integrated_s{seed}','integrated',f'Graine {seed}'+(' · transfert observé' if seed==2 else ''),
            copy.deepcopy(task['scenario']),manifest,task['id'],2118))
    for key,origin,beads in (
        ('material_cycle','research/engine_runs/C3Bexpress_s1_20261025T094654876859Z/scenario.json',102),
        ('binary_copy','research/engine_runs/Copie_binaire_composite_s0_20261023T140139872073Z/scenario.json',108),
        ('free_membrane','research/engine_runs/Vesicules_depuis_des_molecules_isolees_s0_20261023T153753630959Z/scenario.json',72)):
        cfg=json.loads((ROOT/origin).read_text(encoding='utf-8'))
        items.append((key,key,f"Graine {cfg['seed']}",cfg,origin,None,beads))
    return items


def descriptions():
    return [dict(id='integrated',title='Bain intégré actuel',level='Intégration partielle · priorité de lecture',
        summary='Membrane, gènes, outils et précurseurs dans un même bain.',
        prepared='219 molécules membranaires en anneau + 24 libres ; 16 G001 et 16 F001 déjà construits, 48 monomères F, précurseurs P/R libres. 2 118 billes au total.',
        observe='Voir la membrane et son contenu, zoomer sur une chaîne, suivre ses liaisons. Les outils fabriquent des composants ; leur incorporation et les nouvelles chaînes restent rares.',
        limits='La membrane est préparée et peut se dégrader. Ses molécules ne sont pas fabriquées. Stock de nourriture fini, sans apport continu, homéostasie ni cellule viable démontrés.',
        conditions='Température 0,08 ; cycle externe 200 / 15. Les trois graines sont celles de J3. La graine 2 est choisie pour montrer un outil exprimé produisant de la matière ensuite utilisée, pas pour établir une fréquence de réussite.',
        look='Commencer par la vue globale (F), puis zoomer au centre. Cliquer une bille et ouvrir l’onglet Explorer pour suivre son assemblage. À vitesse maximale, le calcul peut prendre plusieurs minutes ; aucune animation n’est précalculée.',
        evidence='research/BATCH_16_RESULTS.md'),
      dict(id='material_cycle',title='Copie, expression et fabrication',level='Sous-système séparé · bain chaud',
        summary='G → F exprimé → fabrication de composants → réutilisation.',
        prepared='Un G001 et six monomères F préparés ; les autres P et R sont libres. Aucun outil F complet n’est construit au départ. 102 billes.',
        observe='Les monomères s’organisent sur le gène. Après libération, un F exprimé peut catalyser l’assemblage de vrais P/R ; les produits peuvent entrer dans de nouvelles chaînes.',
        limits='Pas de membrane. Température différente du bain intégré : cette réussite séparée n’établit pas leur compatibilité complète. Ni alimentation continue ni renouvellement durable.',
        conditions='Température 0,6 ; cycle externe 200 / 15 ; graine 1 sélectionnée parmi les essais du lot 8 pour illustrer le transfert. Même scénario physique que l’essai archivé.',
        look='Laisser avancer au maximum, puis mettre en pause ou ralentir. Les compteurs distinguent les nouveaux produits des structures préparées ; les flashes montrent les changements de liens.',
        evidence='research/BATCH_08.md'),
      dict(id='binary_copy',title='Copie binaire seule · six symboles',level='Sous-système séparé · copie',
        summary='Un polymère 001011 recrute et relie des sous-unités composites.',
        prepared='Une chaîne de six dimères et 48 dimères monomères libres : 108 billes. Les dimères sont fournis, pas fabriqués dans cet essai.',
        observe='Suivre la chaîne initiale et ses partenaires. Les appariements positionnent les monomères ; de nouvelles liaisons forment des chaînes qui peuvent être libérées.',
        limits='Pas de traduction, de synthèse des dimères ou de membrane. La capacité à copier six symboles ici ne valide pas un génome long ou le circuit intégré.',
        conditions='Température 0,6 ; cycle externe 200 / 15 ; graine 0 du témoin T7 historique. La libération est aidée par le cycle fourni.',
        look='Passer en vitesse maximale jusqu’aux associations, puis ralentir et sélectionner la chaîne. Une copie complète exclut la chaîne initialement préparée.',
        evidence='research/ENGINE_MIGRATION.md'),
      dict(id='free_membrane',title='Petites membranes depuis molécules libres',level='Sous-système séparé · assemblage moléculaire',
        summary='36 molécules à deux billes, sans chaîne ou anneau préassemblé.',
        prepared='36 dimères H/T isolés et dispersés : 72 billes. Les liaisons internes des molécules existent déjà ; aucune liaison latérale initiale.',
        observe='Les molécules se rencontrent, forment des fragments et peuvent fermer de petits contours. Zoomer sur une extrémité pour voir association et rupture.',
        limits='Ces petites vésicules ne sont pas la grande membrane du bain intégré : géométrie et paramètres distincts. Pas de contenu cellulaire, de synthèse membranaire ou de rétention validés ici.',
        conditions='Température 0,08 ; graine 0 ; aucun ruban initial replié. Les lois restent celles de la référence V8 à petits contours.',
        look='Observer d’abord l’ensemble à vitesse maximale, puis ralentir lors de l’assemblage. Les contours fermés sont identifiés après coup, sans guider la dynamique.',
        evidence='research/BATCH_03.md')]


def build():
    variants=[]
    for key,demo,title,cfg,origin,task,beads in origins():
        cfg=resolve(cfg);path=f'demonstrators/configs/demo_{key}.json'
        (ROOT/path).write_text(json.dumps(cfg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        variants.append(dict(id=key,demo=demo,title=title,seed=cfg['seed'],config=path,beads=beads,
            source=origin,source_task=task,source_sha256=hashlib.sha256((ROOT/origin).read_bytes()).hexdigest(),
            dynamics_sha256=signature(cfg),view_speed=0.))
    from visualizer.demos import simulator_hashes
    catalog=dict(version=1,date='2026-10-29',recommended='integrated_s2',simulator_sha256=simulator_hashes(),
        policy='Live simulations from preserved initial inputs. Selected illustrative seeds, not a robustness claim. No trajectories/checkpoints bundled.',
        demos=descriptions(),variants=variants)
    (ROOT/'demonstrators/catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def verify():
    from visualizer.demos import DemoCatalog
    from simulator.engine import Simulation
    catalog=DemoCatalog();rows=[]
    for key,_,_,original,source,task,beads in origins():
        variant,info,cfg=catalog.get(key)
        assert signature(cfg)==signature(original)
        assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==variant['source_sha256']
        sim=Simulation(cfg)
        assert len(sim.chemistry.pos)==beads==variant['beads']
        if key.startswith('integrated'):
            assert sim.chemistry.offset==486 and sim.chemistry.genetics.n==816
        elif key=='free_membrane':assert all(not edges for edges in sim.chemistry.edges)
        rows.append(dict(id=key,beads=beads,source_dynamics_identical=True,temperature=cfg['chemistry']['temperature']))
    return rows


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['build','verify']);a=p.parse_args()
    if a.action=='build':build()
    else:print(json.dumps(verify()))
