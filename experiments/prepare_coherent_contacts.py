"""MD2 one fixed bound-contact candidate, with reused references and15 transfer tasks."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve
from simulator.coupled_bath import membrane_config


def originals():
    data=json.loads((ROOT/'research/campaign_recipes/LT2_20261030T065759494210Z/manifest.json').read_text())
    return {t['label']:t['scenario'] for t in data['tasks']}


def candidate(cfg,enabled=True):
    cfg=copy.deepcopy(cfg)
    m=cfg['chemistry']['membrane'] if cfg['model']=='coupled_bath' else cfg['chemistry']
    if enabled:m['bound_port_geometry']=True
    return resolve(cfg)


def plan():
    data=originals();tasks=[]
    def add(cfg,label,preset,fine=False):
        cfg=copy.deepcopy(cfg);cfg.update(name=label,branch='MD2')
        if fine:
            cfg['engine']['dt']/=2;cfg['engine']['reaction_every']*=2;cfg['engine']['sample_every']*=2
        tasks.append(dict(scenario=cfg,preset=preset,comparison='fine' if fine else 'base'))
    for seed in range(3):
        cfg=copy.deepcopy(data['LT2_free_membrane_langevin']);cfg['seed']=seed
        add(candidate(cfg),f'MD2_free_new_s{seed}','free_new')
        if seed>0:add(cfg,f'MD2_free_old_s{seed}','free_old')
    for seed in range(3):
        base=data[f'LT2_integrated_s{seed}_langevin']
        m=membrane_config(base['chemistry']);m.update(retained_probes=24,permeable_probes=24)
        cfg=dict(schema_version=1,model='membrane_bath',seed=seed,duration=1200.,
            chemistry=m,engine=copy.deepcopy(base['engine']),mechanics=copy.deepcopy(base['mechanics']))
        for new in (False,True):add(candidate(cfg,new),f'MD2_probes_{"new" if new else "old"}_s{seed}','probes_new' if new else 'probes_old')
    for seed in range(3):
        cfg=candidate(data[f'LT2_integrated_s{seed}_langevin'])
        add(cfg,f'MD2_bath_new_s{seed}','bath_new')
        if seed==0:add(cfg,'MD2_bath_new_s0_fine','bath_new',fine=True)
    assert len(tasks)==15
    return dict(name='MD2 coherent bound/free contacts transfer',workers=2,checkpoint_seconds=30.,kinetic_window=50.,
        record_trajectory=False,demo_motion_report=True,
        comparison_policy='One fixed harmonic port continuation, no new independent stiffness. Existing off/exchange rates, temperature and Langevin retained. Free V8 and large J3 geometries remain distinct. Old free seed0 and old integrated seeds0/1/2 explicitly reused from LT2; no duplicate repetitions. New/old large probe baths matched; finest control selected seed0 only. No protein or observer feedback.',tasks=tasks)


if __name__=='__main__':
    p=ROOT/'campaigns/coherent_contacts.json';p.write_text(json.dumps(plan(),indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(p)
