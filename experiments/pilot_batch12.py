"""Selected short positive-control seed for the frozen terminal-exchange variant."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import prepare,run,read,write


if __name__=='__main__':
    plan=read(ROOT/'campaigns/membrane_terminal_exchange.json')
    plan['name']='M1G1 selected pilot seed2';plan['workers']=1
    plan['tasks']=[plan['tasks'][2]];plan['tasks'][0]['scenario']['duration']=150.
    parent=ROOT/'outputs/batch12';parent.mkdir(parents=True,exist_ok=True)
    path=parent/'pilot_plan.json'
    if path.exists() and read(path)!=plan:raise ValueError('Preserve prior pilot plan; use a new filename')
    write(path,plan);folder=prepare(path,parent/'pilots');assert run(folder)==0
    state=read(folder/'tasks/task0000/state.json');r=read(folder/state['result']);k=read(folder/state['kinetics'])
    print(json.dumps(dict(folder=str(folder),metrics={key:r['metrics'].get(key) for key in
        ('parent_closed_fraction','envelope_valid_fraction','retained_escape_fraction','inserted_into_closed_parent_ever','contact_exchanges')},
        exposure=k['opportunity_totals']),ensure_ascii=False))
