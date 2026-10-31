"""Passive final-state screen; snapshots are not an integrated kinetic audit."""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
# Load checkpoints with their exact archived simulator, even if current
# observation code has evolved since MIN1. No physical trajectory is advanced.
_index=json.loads((ROOT/'research/BATCH_32_RECIPES.json').read_text(encoding='utf-8'))
_job=json.loads((Path(_index['job'])/'job.json').read_text(encoding='utf-8'))
sys.path.insert(0,str(Path(_job['campaigns'][1])/'runtime'))
from simulator.campaign_io import read,write
from simulator import checkpoint
from simulator.reference import normals
from simulator.genetic_audit import GeneticAudit
from scripts.minimal_tool_followup import controller
from scripts.campaign import status,validate


def inspect():
    job=Path((ROOT/'outputs/minimal_tool_followups/latest.txt').read_text().strip());cfg=controller.validate_job(job)
    folder=Path(cfg['campaigns'][1]);manifest=validate(folder);snap=status(folder);rows=[]
    for task,state in zip(manifest['tasks'],snap['tasks']):
        if state['phase']!='complete':continue
        path=folder/state['result'];sim,_=checkpoint.load(path.parent/'checkpoint.npz');c=sim.chemistry
        active=c.rungs[:,1]>=0;nrm=np.zeros((c.n,2));nrm[active]=normals(c.pos,c.rungs[active])
        edges=[]
        for a,b in sorted(c.edges):
            if c.families[a]!=0:continue
            i,j=map(int,c.pairing[[a,b]])
            edges.append(dict(source=[a,b],template_normal_dot=float(nrm[a]@nrm[b]),paired=[i,j],
                pair_families=[int(c.families[q]) if q>=0 else None for q in (i,j)],
                product_distance=float(np.linalg.norm(c.pos[j]-c.pos[i])) if i>=0 and j>=0 else None,
                product_normal_dot=float(nrm[i]@nrm[j]) if i>=0 and j>=0 else None))
        rows.append(dict(label=task['label'],final_scan=GeneticAudit().scan(c,sim.time),edges=edges))
    report=dict(rows=rows,scope='Final snapshots only, after external release at1200; not evidence of exposure or causal history.')
    write(job/'endpoint_inspection.json',report);print(json.dumps(report,indent=2));return report


if __name__=='__main__':inspect()
