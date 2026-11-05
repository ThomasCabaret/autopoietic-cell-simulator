"""PI1 product/template occupancy assay with common birth-disabled laws."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve
from simulator.mixed_synthesis import genetics_config
from simulator.campaign_io import read
REFERENCE=ROOT/'research/campaign_recipes/CW1_20261105T115432485306Z'
CASES=dict(zero=(0,False),linked4=(4,True),split4=(4,False),linked16=(16,True),split16=(16,False))


def scenario(seed,variant):
    count,linked=CASES[variant]
    old=next(t['scenario'] for t in read(REFERENCE/'manifest.json')['tasks'] if t['scenario']['seed']==seed)
    g=genetics_config(old['chemistry'])
    g.update(sequence='01',seed_family=0,template=True,free_units=0,function_units=2*count,
        assembled_stock=True,ligation=False,rung_formation_rate=0.,rung_catalytic_rate=0.,
        initial_assemblies=[dict(family=1,sequence='01',backbone=linked) for _ in range(count)])
    return resolve(dict(schema_version=1,model='copy',name=f'PI1_{variant}_s{seed}',branch='PI1',
        seed=seed,duration=400.,chemistry=g,mechanics=copy.deepcopy(old['mechanics']),engine=copy.deepcopy(old['engine'])))


def plan():
    if not preflight()['linked16']['eligible_GF']:
        raise ValueError('Product rebinding is excluded by the local family/degree gate; do not repeat PI1 concentrations before a new mechanism')
    return dict(name='PI1 existing F-product binding to a prepared gene',workers=2,checkpoint_seconds=30.,
        kinetic_window=25.,record_trajectory=False,genetic_audit=True,
        tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in CASES],
        comparison_policy='BATCH_46_PLAN:15 fixed occupancy assays at400, no L/HT, all precursors '
            'assembled, ligation/PR formation disabled in every case.0/4/16 F01 and split controls. '
            'Same genetic mechanics/capture/cycle22x22, no new chemical helper. Linked/split have '
            'matched initial coordinates/velocities/RNG; counts differ in the titration. '
            'Binding is not evidence of homeostasis, net inhibition, selectivity or loss protection.')


def preflight():
    """Construct an oriented contact and ask the actual existing audit, no dynamics."""
    from simulator.engine import Simulation
    from simulator.genetic_audit import GeneticAudit
    rows={}
    for name in CASES:
        if name=='zero':continue
        cfg=scenario(0,name);c=Simulation(cfg).chemistry;n=c.n
        c.pos[0]=[1.5,1.5];c.pos[n]=[1.5,1.95]
        c.pos[1]=[2.5,1.5];c.pos[n+1]=[2.5,1.95]
        c.pos[2]=[1.5,2.4];c.pos[n+2]=[1.5,1.95]
        c.pos[3]=[2.5,2.4];c.pos[n+3]=[2.5,1.95]
        audit=GeneticAudit().scan(c,0.)
        rows[name]=dict(eligible_GF=audit['recognition_eligible_GF'],
            blocked_family_degree=audit.get('recognition_blocked_family_degree',0),
            geometric_product_contacts=audit.get('recognition_GF_geometric_F_degree_1',0),
            gf_end_capture=cfg['chemistry'].get('gf_end_capture',False))
    return rows


if __name__=='__main__':
    from simulator.campaign_io import write
    result=dict(cases=preflight(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scope='Constructed oriented contacts, actual GeneticAudit predicate; no time evolution, production or regulation proof.')
    write(ROOT/'research/BATCH_46_PI1_PREFLIGHT.json',result);print(json.dumps(result,indent=2))
