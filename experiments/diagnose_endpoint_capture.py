"""Six ideal-contact controls for T9E; accepted draws are conditioned, not kinetics."""
import copy,hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.engine import Simulation
from simulator.spatial import Neighborhood
from simulator.genetic_audit import GeneticAudit
from experiments.prepare_expression_campaign import small
from experiments.diagnose_fragment_capture import CertainDraw


def run():
    rows=[]
    for variant in ('old','end'):
        for form in ('monomers','fragment01','complete001'):
            cfg=small(0,variant,'expression');g=cfg['chemistry']
            g.update(free_units=0,function_units=3,assembled_stock=True,
                initial_assemblies=[dict(family=1,sequence='001',backbone=False)])
            cfg['duration']=.01
            sim=Simulation(cfg);c=sim.chemistry
            c.pos[:3]=np.column_stack((np.arange(3)+2.,np.full(3,2.)))
            c.pos[3:6]=c.pos[:3]+[0.,.9]
            c.pos[6:9]=c.pos[:3]+[0.,.45];c.pos[9:12]=c.pos[3:6]-[0.,.45]
            if form!='monomers':c.edges.add((4,5))
            if form=='complete001':c.edges.add((3,4))
            before=copy.deepcopy(c.export());positions=c.pos.tolist();scan=GeneticAudit().scan(c,0.)
            c.rng=CertainDraw();events=c.react(0.,sim.dt,Neighborhood())
            paired=[int(i) for i in range(3,6) if c.pairing[i]>=0]
            expected=([3,5] if form=='complete001' else [3,4,5]) if variant=='end' else (
                [3,4,5] if form=='monomers' else [3] if form=='fragment01' else [])
            assert paired==expected
            if variant=='end':assert (3,4) in c.edges and (4,5) in c.edges
            if variant=='old' and form=='fragment01':assert (3,4) not in c.edges
            rows.append(dict(variant=variant,form=form,scenario=sim.config,initial_state=before,
                initial_positions=positions,pre_reaction_scan=scan,actual_F_sites_paired=paired,
                events=events,final_state=c.export()))
    out=ROOT/'outputs/diagnostics'/('T9E_local_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    hashes={}
    for src in list((ROOT/'simulator').glob('*.py'))+[Path(__file__),ROOT/'experiments/prepare_expression_campaign.py',ROOT/'experiments/diagnose_fragment_capture.py']:
        name=src.relative_to(ROOT).as_posix();dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(src.read_bytes());hashes[name]=hashlib.sha256(src.read_bytes()).hexdigest()
    report=dict(rows=rows,source_sha256=hashes,scope='Six explicitly prepared ideal contacts; draws conditioned to accept, '
        'one actual reaction tick, no integration or kinetic inference. Initialization and RNG override are diagnostics only, '
        'never the production campaign. Endpoints of a complete prepared F also bind: interference must be tested.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(folder=str(out),rows=[dict(variant=r['variant'],form=r['form'],paired=r['actual_F_sites_paired'],ligations=len(r['events'])) for r in rows])))
    return out


if __name__=='__main__':run()
