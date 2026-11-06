"""FA1: bounded offline reconstruction of PT1/RF1, with final-state checks."""
import hashlib,json,shutil
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from experiments.independent_assay_results import completed
from simulator.checkpoint import load
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.observations import components,area
from simulator.membrane_bath import polygon_simple
ROOT=Path(__file__).resolve().parents[1]


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def journal(c,events,final):
    edges=set(c.edges);rungs=c.rungs.copy();bits=c.bits.copy();rows=[];losses=[];births=[]
    def motifs():return sum(c.families[a]==c.families[b]==1 and bits[a]>=0 and bits[b]>=0 and bits[a]!=bits[b] for a,b in edges)
    count=int(motifs());last_time=0.;absent_time=0.;first_loss=None;first_return=None
    for e in events:
        t=e['time']
        if t<last_time:raise ValueError('Journal not chronological')
        if count==0:absent_time+=t-last_time
        kind=e['kind']
        if kind=='backbone_break':edges.remove(tuple(sorted((e['a'],e['b']))))
        elif kind=='backbone_form':edges.add(tuple(sorted((e['a'],e['b']))))
        elif kind=='rung_break':rungs[e['support'],1]=-1;bits[e['support']]=-1
        elif kind=='rung_form':
            rungs[e['support'],1]=e['recognizer'];bits[e['support']]=e['symbol']
            births.append(dict(time=t,family='G' if c.families[e['support']]==0 else 'F',catalyzed=bool(e.get('catalyzed',False))))
        else:raise ValueError(kind)
        after=int(motifs())
        if count and not after:
            item=dict(time=t,event=e,active_F0=int(np.count_nonzero((c.families==1)&(bits==0))),active_F1=int(np.count_nonzero((c.families==1)&(bits==1))))
            losses.append(item)
            if first_loss is None:first_loss=t
        if not count and after and first_loss is not None and first_return is None:first_return=t
        if after!=count:rows.append(dict(time=t,motifs=after,event=kind))
        count=after;last_time=t
    if count==0:absent_time+=final.config['duration']-last_time
    np.testing.assert_array_equal(rungs,final.chemistry.rungs)
    np.testing.assert_array_equal(bits,final.chemistry.bits)
    if edges!=final.chemistry.edges:raise ValueError('Final edges do not match journal')
    return dict(final_state_reconstructed=True,first_structural_loss=first_loss,first_structural_return=first_return,
        final_structural_motifs=count,time_without_structural_motif=absent_time,motif_changes=rows,
        loss_events=losses,formations={f:sum(x['family']==f for x in births) for f in ('G','F')},
        formations_before_first_loss={f:sum(x['family']==f and (first_loss is None or x['time']<=first_loss) for x in births) for f in ('G','F')},
        scope='Exact bond journal reconstruction, not pairing/capture exposure or a complete molecular lineage. Absence of return is censored at horizon.')


def analyze():
    rows={};inputs={}
    for tag,stem,n in [('PT1','selective_transport',6),('RF1','functional_recycling',9)]:
        desc=read(ROOT/f'research/BATCH_53_{tag}_RECIPES.json');job=Path(desc['job']);cfg=read(job/'job.json');folder=Path(cfg['campaigns'][0])
        state=read(job/'state.json');report=Path(state['report_0'])
        if digest(report)!=state['report_0_sha256']:raise ValueError('Final report changed')
        _,manifest,snapshot,entries=completed(folder,n,True)
        inputs[str(report.relative_to(ROOT))]=digest(report);results=[]
        for task,s,r,row in entries:
            ck=folder/s['checkpoint'];sim,obs=load(ck,make_observer);c=sim.chemistry
            inputs[str(ck.relative_to(ROOT))]=digest(ck);inputs[str((folder/s['result']).relative_to(ROOT))]=digest(folder/s['result'])
            if tag=='RF1':
                initial=Simulation(task['scenario']);row.update(journal(initial.chemistry,c.turnover.events,sim))
                row.update(targets_final=r['metrics']['final']['target_chains'],reassemblies=r['metrics']['polymer_reassemblies'],reincorporations=r['metrics']['recycled_incorporations'])
            else:
                heads=sorted(c.lipids.rungs);ix={h:i for i,h in enumerate(heads)};edges={(ix[a],ix[b]) for a,b,_,_ in c.lipids.links}
                comps=[]
                for comp,order,cycle in components(len(heads),edges):
                    pts=c.pos[[heads[x] for x in order]]
                    comps.append(dict(units=len(comp),cycle=bool(cycle),area=float(area(pts)),simple=bool(polygon_simple(pts)),
                        endpoint_gap=None if cycle else float(np.linalg.norm(pts[-1]-pts[0]))))
                hist=obs.boundary_state['history']
                row.update(lateral_links=len(edges),components=comps,last_valid_sample=max((h['time'] for h in hist if h['valid']),default=None),
                    final_valid=hist[-1]['valid'],sampled_crossings=obs.boundary_state['crossings'])
            results.append(row)
        rows[tag]=dict(decision=read(report)['decision'],rows=results)
    return dict(analysis=rows,inputs=inputs)


def main():
    result=analyze();stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out=ROOT/'outputs/diagnostics'/('FA1_'+stamp);out.mkdir(parents=True)
    result['scope']='Offline final reports/checkpoints/journals, no dynamics or changed gates.'
    write(out/'report.json',result)
    recipe=ROOT/'research/diagnostic_recipes'/('FA1_'+stamp);recipe.mkdir(parents=True)
    sources=[Path(__file__),ROOT/'experiments/independent_assay_results.py']
    for src in sources:
        dest=recipe/src.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
    record=dict(inputs=result['inputs'],sources={str(p.relative_to(ROOT)):digest(p) for p in sources},
        engine_sources={str(p.relative_to(ROOT)):digest(p) for p in (ROOT/'simulator').glob('*.py')})
    write(recipe/'recipe.json',record)
    write(ROOT/'research/BATCH_54_FA1.json',dict(output=str(out),recipe=recipe.relative_to(ROOT).as_posix(),
        report_sha256=digest(out/'report.json'),**result))
    print(json.dumps(dict(output=str(out),recipe=str(recipe))))


if __name__=='__main__':main()
