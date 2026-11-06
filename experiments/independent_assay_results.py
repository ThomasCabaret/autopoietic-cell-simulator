"""Common immutable-result checks for PT1/RF1, no chemistry decisions."""
from pathlib import Path
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read


def completed(folder,count,require_complete):
    folder=Path(folder);manifest=validate(folder);snap=status(folder);rows=[]
    if require_complete and (snap['controller_active'] or snap['counts']['complete']!=count):raise ValueError('Require inactive complete assay')
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    for task,state in zip(manifest['tasks'],snap['tasks']):
        if state['phase']!='complete':continue
        path=folder/state['result'];result=read(path)
        if result['error'] or not result['completed'] or result['scenario']!=task['scenario'] or result['source_sha256']!=hashes:raise ValueError('Independent assay provenance mismatch')
        motion=read(folder/state['motion_audit'])['history'];late=[q['kinetic_temperature'] for q in motion if q['time']>=.75*task['scenario']['duration']]
        rows.append((task,state,result,dict(label=task['label'],seed=task['scenario']['seed'],variant=task['label'][4:].rsplit('_s',1)[0],
            late_temperature=sum(late)/len(late),result_sha256=digest(path))))
    return folder,manifest,snap,rows
