"""RP1 strict useful-material screen, not homeostasis or lineage certification."""
from pathlib import Path
from statistics import median
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write


def decide(rows):
    if len(rows)!=3 or {r['seed'] for r in rows}!={0,1,2}:raise ValueError('Require three RP1 seeds')
    conditions=dict(invariants=all(r['invariant_failures']==0 and r['atoms']==150 for r in rows),
        genetic_survival=all(r['G_current']>=1 for r in rows),functional_present=median(r['F_current'] for r in rows)>=1,
        useful_reassembly=sum(r['polymer_reassemblies']>0 for r in rows)>=2,
        useful_reincorporation=sum(r['recycled_incorporations']>0 for r in rows)>=2)
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Three separate RV1 protection-variant cases. Current counts include prepared chains; '
            'two-real-atom lifecycle only, not expressed whole-tool renewal, homeostasis or compatibility with EG1.')


def collect(folder,require_complete=True):
    folder=Path(folder);manifest=validate(folder);s=status(folder);rows=[]
    if require_complete and (s['controller_active'] or s['counts']['complete']!=3):raise ValueError('Require inactive complete RP1')
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    for task,t in zip(manifest['tasks'],s['tasks']):
        if t['phase']!='complete':continue
        p=folder/t['result'];r=read(p);m=r['metrics'];last=m['final']
        if r['error'] or not r['completed'] or r['scenario']!=task['scenario'] or r['source_sha256']!=hashes:raise ValueError('RP1 provenance mismatch')
        rows.append(dict(seed=task['scenario']['seed'],label=task['label'],G_current=last['target_chains']['G'],
            F_current=last['target_chains']['F'],atoms=last['atoms'],invariant_failures=m['invariant_failures'],
            polymer_reassemblies=m['polymer_reassemblies'],recycled_incorporations=m['recycled_incorporations'],
            backbone_break=m['backbone_break'],rung_break=m['rung_break'],result_sha256=digest(p)))
    report=dict(rows=rows,counts=s['counts'],controller_active=s['controller_active'],
        decision=decide(rows) if len(rows)==3 else None,manifest_sha256=digest(folder/'manifest.json'))
    write(folder/'pair_protection_review.json',report);return report
