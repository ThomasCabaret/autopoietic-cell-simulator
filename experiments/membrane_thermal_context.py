"""Post-hoc thermal context, separate from the frozen MIN1M decision criteria."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write
from scripts.campaign import validate,status,digest
from experiments.review_membrane_renewal import collect


def main():
    from scripts.membrane_renewal_followup import latest
    job=latest();folder=Path(read(job/'job.json')['campaigns'][0]);m=validate(folder);s=status(folder)
    evidence=collect(folder,False);verified={r['label']:r for r in evidence['rows']};rows=[]
    for task,state in zip(m['tasks'],s['tasks']):
        if state['phase']!='complete':continue
        path=folder/state['motion_audit'];h=read(path)['history'];limit=.75*task['scenario']['duration']
        late=[x['kinetic_temperature'] for x in h if x['time']>=limit]
        rows.append(dict(label=task['label'],mean_T_late=sum(late)/len(late),final_T=h[-1]['kinetic_temperature'],
            target_T=task['scenario']['chemistry']['temperature'],sampled_from=limit,samples=len(late),
            audit_sha256=digest(path),result_sha256=verified[task['label']]['result_sha256']))
    report=dict(counts=s['counts'],rows=rows,manifest_sha256=digest(folder/'manifest.json'),
        scope='Post-hoc thermal context, complete cases only. Last quarter of declared horizon; does not modify the frozen MIN1M screen.')
    write(folder/'thermal_context.json',report);print(json.dumps(report,indent=2))


if __name__=='__main__':main()
