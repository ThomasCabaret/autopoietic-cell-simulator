"""Instrumented short B0 run versus immutable lot9 positions, RNG and metrics."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import prepare,run,read,write


if __name__=='__main__':
    original=ROOT/'research/engine_runs/M1exchange_s0_20261025T225915563115Z'
    recipe=read(original/'recipe.json')
    for name,digest in recipe['source_sha256'].items():
        assert hashlib.sha256((original/name).read_bytes()).hexdigest()==digest
    parent=ROOT/'outputs/batch11';parent.mkdir(parents=True,exist_ok=True)
    plan=parent/'pilot_plan.json'
    if plan.exists() and read(plan).get('tasks')!=[dict(scenario=recipe['scenario'])]:
        raise ValueError('Pilot plan differs; preserve it and choose another filename')
    write(plan,dict(name='Lot11 audit pilot',workers=1,boundary_audit=True,record_trajectory=False,
        checkpoint_seconds=60,tasks=[dict(scenario=recipe['scenario'])]))
    folder=prepare(plan,parent/'pilots');assert run(folder)==0
    state=read(folder/'tasks/task0000/state.json');actual=read(folder/state['result'])
    expected=read(original/'result.json');assert actual['metrics']==expected['metrics']
    with np.load(original/'checkpoint.npz') as x,np.load(folder/state['checkpoint']) as y:
        np.testing.assert_array_equal(x['positions'],y['positions'])
        a=json.loads(str(x['metadata']));b=json.loads(str(y['metadata']))
        assert a['rng']==b['rng'] and a['chemistry']==b['chemistry']
    audit=read(folder/state['boundary_audit'])
    proof=dict(original=original.relative_to(ROOT).as_posix(),new=folder.relative_to(ROOT).as_posix(),
        metrics_equal=True,positions_equal=True,rng_equal=True,chemistry_equal=True,
        audit={k:v for k,v in audit.items() if k!='state'})
    write(folder/'reference_comparison.json',proof)
    print(json.dumps(proof,ensure_ascii=False))
