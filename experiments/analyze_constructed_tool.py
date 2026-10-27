"""Validate finished J1 tasks and inventory; incomplete cohorts stay explicit."""
import argparse,hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,read,write
from experiments.inventory_audit import census


def membrane_grid_metrics(history,interval,duration):
    grid=[h for h in history if abs(h['time']/interval-round(h['time']/interval))<1e-7]
    assert len(grid)==int(round(duration/interval))+1
    return dict(regular_grid_closed_fraction=sum(h['parent_closed'] for h in grid)/len(grid),
        regular_grid_envelope_fraction=sum(h['envelope_valid'] for h in grid)/len(grid),
        regular_grid_samples=len(grid),regular_grid_interval=interval)


def analyze(folder):
    folder=Path(folder).resolve();manifest=validate(folder);snapshot=status(folder)
    expected={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')};rows=[]
    for task,state in zip(manifest['tasks'],snapshot['tasks']):
        if state['phase']!='complete':continue
        r=read(folder/state['result']);cfg=r['scenario'];metrics=r['metrics'];m=metrics.get('genetics',metrics)
        assert r['completed'] and r['error'] is None and r['source_sha256']==expected
        assert cfg==task['scenario']
        a=read(folder/state['genetic_audit']);e=a['exposure']
        assert abs(a['observed_time']-cfg['duration'])<1e-6
        assert a['ligations']==m['ligation_events'] and a['assembled']==m['assembled_dimers'] and a['catalytic_assembled']==m['catalyzed_dimers']
        for prefix,target in [('recognition','recognition_near'),('ligation','ligation_double_paired')]:
            assert abs(sum(v for k,v in e.items() if k.startswith(prefix+'_blocked_') or k.startswith(prefix+'_eligible_'))-e.get(target,0.))<1e-6
        with np.load(folder/state['checkpoint'],allow_pickle=False) as z:
            meta=json.loads(str(z['metadata']));assert meta['source_sha256']==expected and meta['config']==cfg
            assert abs(meta['step']*cfg['engine']['dt']-cfg['duration'])<1e-8
            inv=census(cfg,meta['chemistry'],z['positions'])
        initial=sum(r>=0 for i,r in m['assembly_state']['rungs'])-m['assembled_dimers']
        assert initial+len(m['assembly_state']['events'])==inv['pools']['active_dimers']
        made={x['support'] for x in m['assembly_state']['events']};assert len(made)==m['assembled_dimers']
        assert set(map(int,m['assembly_incorporation_times']))<=made
        ch=meta['chemistry'].get('genetics',meta['chemistry'])
        for event in m['assembly_state']['events']:
            assert ch['assembly']['rungs'][event['support']][1]==event['recognizer']
        row=dict(task=task['id'],case=cfg['name'],seed=cfg['seed'],duration=cfg['duration'],
            catalyzed=m['catalyzed_dimers'],catalyzed_incorporated=m['catalyzed_incorporated'],
            expressed_catalyzed=m['expressed_catalyzed_dimers'],expressed_incorporated=m['expressed_catalyzed_incorporated'],
            G=m['detached_copy_sets_ever'],F=m['translated_detached_ever'],
            all_constructed_G=m['constructed_detached_G'],all_constructed_F=m['constructed_detached_F'],inventory=inv,
            genetic_exposure=e,source_and_census_verified=True)
        if metrics.get('membrane'):
            mm=metrics['membrane'];row['membrane']={k:mm[k] for k in ('parent_closed_fraction','envelope_valid_fraction','inserted_into_closed_parent_ever')}
            row['membrane'].update(membrane_grid_metrics(mm['history'],cfg['engine']['sample_every']*cfg['engine']['dt'],cfg['duration']))
        rows.append(row)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');out=folder/('inventory_analysis_'+stamp);out.mkdir()
    hashes={}
    for name in ('experiments/analyze_constructed_tool.py','experiments/inventory_audit.py','simulator/observations.py'):
        src=ROOT/name;target=out/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(src.read_bytes())
        hashes[name]=hashlib.sha256(src.read_bytes()).hexdigest()
    report=dict(campaign=str(folder),counts=snapshot['counts'],complete_cohort=len(rows)==len(manifest['tasks']),rows=rows,analysis_source_sha256=hashes)
    write(out/'report.json',report)
    for r in rows:
        p=r['inventory']['pools'];access=r['inventory']['free_monomer_access']
        print(json.dumps(dict(case=r['case'],seed=r['seed'],cat=r['catalyzed'],incorp=r['catalyzed_incorporated'],G=r['G'],F=r['F'],
            free_P=p['free_P_G']+p['free_P_F'],free_R=p['free_R0']+p['free_R1']+p['free_R2'],
            monomers={k:v['count'] for k,v in access.items()},median_gene_distance={k:v['median_distance'] for k,v in access.items()},
            fragment_F_units=r['inventory']['unpaired_non_target_F_units'])))
    print(str(out));return out


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path);a=p.parse_args();analyze(a.folder)
