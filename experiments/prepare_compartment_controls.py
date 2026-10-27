"""Matched membrane-free large/compact worlds; reaction laws stay frozen."""
import argparse,copy,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.engine import Simulation


def scenario(domain,prepared,seed=0,duration=1200.):
    if domain not in ('open','compact'):raise ValueError(domain)
    ref=json.loads((ROOT/'research/campaign_recipes/J1_20261027T144451586423Z/manifest.json').read_text(encoding='utf-8'))
    name='J1_bath_'+('prepared' if prepared else 'unlinked')
    cfg=copy.deepcopy(next(t['scenario'] for t in ref['tasks'] if t['scenario']['name']==name and t['scenario']['seed']==seed))
    cfg.update(name='J2_'+domain+'_'+('prepared' if prepared else 'unlinked'),branch='J2',duration=duration)
    cfg['chemistry']['include_membrane']=False
    cfg['chemistry']['world_box']=cfg['chemistry']['genetics']['box'] if domain=='compact' else None
    return cfg


def verify():
    rows=[]
    for prepared in (True,False):
        for seed in range(3):
            a=Simulation(scenario('open',prepared,seed,.02));b=Simulation(scenario('compact',prepared,seed,.02))
            shift=a.chemistry.box/2+np.asarray(a.config['chemistry']['packet_offset'])-b.chemistry.box/2
            np.testing.assert_allclose(a.chemistry.pos-shift,b.chemistry.pos,atol=1e-13)
            assert a.rng.bit_generator.state==b.rng.bit_generator.state
            assert a.chemistry.genetics.export()==b.chemistry.genetics.export()
            bath_cfg=copy.deepcopy(a.config);bath_cfg['chemistry']['include_membrane']=True
            bath=Simulation(bath_cfg)
            np.testing.assert_array_equal(a.chemistry.pos,bath.chemistry.pos[bath.chemistry.offset:])
            assert a.rng.bit_generator.state==bath.rng.bit_generator.state
            assert a.chemistry.genetics.export()==bath.chemistry.genetics.export()
            rows.append(dict(seed=seed,prepared=prepared,particles=102,translated_packet_and_rng_identical=True,matched_to_membrane_initial_packet=True))
    return rows


def plan():
    return dict(name='J2 matched large and compact boundary controls without L',workers=2,
        checkpoint_seconds=60,kinetic_window=25,record_trajectory=False,genetic_audit=True,
        comparison_policy='J1 reaction laws, T0.08 and feed inventories fixed. L removed; all-seed prepared/unlinked pairs, same initial PR packet/RNG up to translation. Rectangular whole-world walls are declared environmental controls, not cell mechanisms.',
        tasks=[dict(scenario=scenario(domain,prepared,seed)) for seed in range(3)
               for domain in ('open','compact') for prepared in (True,False)])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['verify','plan']);a=p.parse_args()
    if a.action=='verify':print(json.dumps(verify()))
    else:(ROOT/'campaigns/compartment_controls.json').write_text(json.dumps(plan(),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
