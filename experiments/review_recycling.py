"""Read completed RV1 trials, explicitly distinguish partial cohorts from the gate."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import recycling_followup as followup
from scripts.campaign import validate,status
from simulator.campaign_io import read,write


def review(job):
    cfg=followup.controller.validate_job(job);cohorts=[]
    for folder in map(Path,cfg['campaigns']):
        manifest=validate(folder);s=status(folder);rows=[]
        for task,state in zip(manifest['tasks'],s['tasks']):
            if state['phase']!='complete':continue
            path=folder/state['result'];result=read(path)
            hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
            if result['source_sha256']!=hashes or result['scenario']!=task['scenario'] or result['error'] or not result['completed']:
                raise ValueError('Invalid completed result')
            g=result['metrics'].get('genetics',result['metrics']);h=g['history']
            samples=[]
            for frac in (.25,.5,.75,1.):
                t=frac*task['scenario']['duration'];sample=min(h,key=lambda x:abs(x['time']-t))
                samples.append({k:sample[k] for k in ('time','target_chains','free_P','active_rungs','backbone_break',
                    'rung_break','catalyzed_formations','polymer_reassemblies','recycled_incorporations')})
            rows.append(dict(label=task['label'],final=g['final'],invariant_failures=g['invariant_failures'],samples=samples,
                result_sha256=followup.digest(path),elapsed_seconds=result['elapsed_seconds']))
        cohorts.append(dict(name=manifest['name'],counts=s['counts'],rows=rows))
    result=dict(job=str(job),cohorts=cohorts,state=read(job/'state.json'),
        limitation='Only completed trajectories shown; incomplete cohort is not a gate decision. Prepared material included. '
                    'Time courses describe finite closed stock, not maintained homeostasis or generation lineage.')
    write(job/'review.json',result)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return result


if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    job=Path(sys.argv[1]) if len(sys.argv)>1 else Path((ROOT/'outputs/recycling_followups/latest.txt').read_text().strip())
    review(job)
