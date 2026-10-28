"""T9 exact local-contact controls, not kinetics or a new chemistry candidate."""
import copy
import hashlib
import json
import sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.engine import Simulation
from simulator.genetic_audit import GeneticAudit
from simulator.spatial import Neighborhood
from experiments.prepare_numerical_campaign import scenario


class CertainDraw:
    """Condition on an accepted stochastic draw to test logical admissibility only."""
    def random(self):return 0.
    def shuffle(self,array):pass


def run():
    rows=[]
    for gate in (True,False):
        for form in ('monomers','fragment01','complete001'):
            g=copy.deepcopy(scenario(4,0)['chemistry']['genetics'])
            g.update(free_units=0,function_units=3,box=[8.,6.],assembled_stock=True,
                monomer_only_capture=gate,ligation=False,
                initial_assemblies=[dict(family=1,sequence='001',backbone=False)])
            raw=dict(schema_version=1,model='copy',seed=0,duration=.01,
                engine=dict(dt=.0005),chemistry=dict(g,temperature=.08))
            sim=Simulation(raw);c=sim.chemistry
            c.pos[:3]=np.column_stack((np.arange(3)+2.,np.full(3,2.)))
            c.pos[3:6]=c.pos[:3]+[0.,.9]
            c.pos[6:9]=c.pos[:3]+[0.,.45];c.pos[9:12]=c.pos[3:6]-[0.,.45]
            if form!='monomers':c.edges.add((4,5))
            if form=='complete001':c.edges.add((3,4))
            before=c.export();positions=c.pos.tolist()
            scan=GeneticAudit().scan(c,0.)
            c.rng=CertainDraw()
            # No integration or observer feedback. Exercise the actual rule once.
            c.react(0.,sim.dt,Neighborhood())
            paired=[int(i) for i in range(3,6) if c.pairing[i]>=0]
            assert paired==({'monomers':[3,4,5],'fragment01':[3],'complete001':[]}[form])
            rows.append(dict(monomer_only_capture=gate,form=form,scenario=sim.config,
                initial_state=before,initial_positions=positions,pre_reaction_scan=scan,
                actual_F_sites_paired=paired))
    out=ROOT/'outputs/diagnostics'/('T9_gates_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    out.mkdir(parents=True);sources={}
    for src in [Path(__file__)]+list((ROOT/'simulator').glob('*.py')):
        name=src.relative_to(ROOT).as_posix();dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(src.read_bytes());sources[name]=hashlib.sha256(src.read_bytes()).hexdigest()
    result=dict(rows=rows,source_sha256=sources,
        scope='Six constructed ideal-contact logical controls. Draws forced to accept, '
            'no integration or kinetic inference, no new chemistry or complete-chain recognition in dynamics. '
            'Turning off monomer gate alone cannot remove the independent GF family-degree block.')
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    for row in rows:print(row['monomer_only_capture'],row['form'],row['actual_F_sites_paired'])
    print(out);return out


if __name__=='__main__':run()
