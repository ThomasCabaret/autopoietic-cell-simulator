"""FS1: distinguish exact F001 target counts, local F01 motifs and actual flux.

Read-only analysis of completed RP1 with its own source-frozen checkpoint loader.
No new evolution, law, gate relaxation or whole-tool certificate is introduced.
"""
import hashlib,json,shutil,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write
from scripts.campaign import validate,digest

SNAPSHOT='''
import json,sys,numpy as np
from simulator.checkpoint import load
from simulator.turnover import paired_edge
s,_=load(sys.argv[1]);c=s.chemistry
mixed=[(a,b) for a,b in c.edges if c.families[a]==c.families[b]==1 and
    c.rungs[a,1]>=0 and c.rungs[b,1]>=0 and c.bits[a]!=c.bits[b]]
unpaired=[(a,b) for a,b in mixed if c.pairing[a]<0 and c.pairing[b]<0]
eligible=0;cat=c.assembly.catalyst
for a,b in unpaired:
    p,r=int(cat.site_bound[a]),int(cat.site_bound[b])
    if p>=c.n and 0<=r<c.n:p,r=r,p
    if 0<=p<c.n<=r and c.rungs[p,1]<0 and np.linalg.norm(c.pos[p]-c.pos[r])<c.config['rung_capture_radius']:
        eligible+=1
print(json.dumps(dict(mixed_symbol_F_edges=len(mixed),unpaired_mixed_symbol_F_edges=len(unpaired),
    current_double_captures_with_PR_geometry=eligible,coherently_protected_edges=sum(paired_edge(c,a,b) for a,b in c.edges))))
'''


def main():
    job=Path(read(ROOT/'research/BATCH_48_RP1_RECIPES.json')['job']);folder=Path(read(job/'job.json')['campaigns'][0]);manifest=validate(folder)
    state=read(job/'state.json');p=Path(state['report_0'])
    if digest(p)!=state['report_0_sha256']:raise ValueError('RP1 report changed')
    report=read(p)
    if read(job/'state.json')['phase']!='needs_interpretation':raise ValueError('Require completed RP1')
    out=ROOT/'outputs/diagnostics'/('FS1_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    rows=[];inputs=[]
    for task in manifest['tasks']:
        st=read(folder/'tasks'/task['id']/'state.json');result=folder/st['result'];ck=folder/st['checkpoint'];r=read(result);m=r['metrics']
        if digest(result)!=next(q['result_sha256'] for q in report['rows'] if q['label']==task['label']):raise ValueError('Result changed')
        snapshot=subprocess.run([sys.executable,'-c',SNAPSHOT,str(ck)],cwd=folder/'runtime',capture_output=True,text=True,check=True,timeout=90)
        counts=json.loads(snapshot.stdout);start=.75*task['scenario']['duration'];history=[q for q in m['history'] if q['time']>=start]
        first,last=history[0],history[-1]
        row=dict(seed=task['scenario']['seed'],label=task['label'],exact_F_target_final=last['target_chains']['F'],
            exact_F_target_late_min=min(q['target_chains']['F'] for q in history),exact_F_target_late_max=max(q['target_chains']['F'] for q in history),
            late_window=[first['time'],last['time']],late_catalyzed_formations=last['catalyzed_formations']-first['catalyzed_formations'],
            late_recycled_incorporations=last['recycled_incorporations']-first['recycled_incorporations'],**counts)
        rows.append(row);inputs.append(dict(task=task['id'],result_sha256=digest(result),checkpoint_sha256=digest(ck)))
    evidence=dict(rows=rows,reference_report_sha256=digest(p),manifest_sha256=digest(folder/'manifest.json'),inputs=inputs,
        scope='Current edge motifs may overlap and are potential co-recruiters, not whole proteins. Late catalytic events can be futile cycles. '
            'The original exact-F001 gate stays refused; no homeostasis, information preservation or mixed-bath survival claimed.')
    write(out/'report.json',evidence)
    recipe=ROOT/'research/diagnostic_recipes'/out.name;recipe.mkdir(parents=True)
    shutil.copyfile(Path(__file__),recipe/'audit_functional_survival.py')
    write(recipe/'recipe.json',dict(campaign=str(folder),manifest_sha256=digest(folder/'manifest.json'),inputs=inputs,source_sha256=digest(Path(__file__))))
    write(ROOT/'research/BATCH_49_FS1.json',dict(output=str(out),recipe=recipe.relative_to(ROOT).as_posix(),
        report_sha256=digest(out/'report.json'),source_sha256=digest(Path(__file__)),summary=evidence))
    print(json.dumps(dict(output=str(out),rows=rows)));return out


if __name__=='__main__':main()
