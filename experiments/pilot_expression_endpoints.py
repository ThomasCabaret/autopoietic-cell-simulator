"""Two short end-to-end worker checks before T9E production; no biological claim."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_expression_campaign import small,transfer
from scripts.campaign import prepare,export_recipe
from scripts.expression_followup import collect
from simulator.campaign_io import write


def run():
    tasks=[]
    for cfg in (small(0,'end','tool'),transfer(0)):
        cfg.update(duration=1.,name=cfg['name']+'_pilot');tasks.append(dict(scenario=cfg))
    path=ROOT/'outputs/expression_pilot_plan.json'
    write(path,dict(name='T9E one-unit worker and audit pilot',workers=2,genetic_audit=True,
        checkpoint_seconds=30.,record_trajectory=False,tasks=tasks))
    folder=prepare(path,ROOT/'outputs/expression_pilots')
    export_recipe(folder,ROOT/'research/campaign_recipes'/('T9Epilot_'+folder.name.removeprefix('campaign_')))
    subprocess.run([sys.executable,str(folder/'runtime/campaign.py'),'run',str(folder)],cwd=folder,check=True)
    report=collect(folder);report['scope']='Two one-unit technical pilots; no biological evidence.'
    write(folder/'pilot_report.json',report);print(json.dumps(dict(folder=str(folder),tasks=len(report['rows']))))


if __name__=='__main__':run()
