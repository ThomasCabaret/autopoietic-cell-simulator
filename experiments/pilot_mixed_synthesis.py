"""One fixed t10 technical pilot through the existing frozen campaign worker."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write
from scripts.campaign import prepare,export_recipe,status
from simulator.campaign_worker import execute
from experiments.prepare_mixed_synthesis import scenario


def main():
    plan=dict(name='MX1P technical pilot',workers=1,checkpoint_seconds=30.,record_trajectory=False,
        tasks=[dict(scenario=scenario(0,'mixed',10.))],comparison_policy='BATCH_41_PLAN fixed t10 technical check, not a productivity screen')
    p=ROOT/'campaigns/mixed_pilot.json';write(p,plan);folder=prepare(p,ROOT/'outputs/mixed_pilots')
    recipe=ROOT/'research/campaign_recipes'/('MX1P_'+folder.name.removeprefix('campaign_'));export_recipe(folder,recipe)
    write(ROOT/'research/BATCH_41_PILOT.json',dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix()))
    execute(folder,'task0000');s=status(folder);result=read(folder/s['tasks'][0]['result'])
    print(dict(folder=str(folder),complete=s['counts']['complete'],elapsed_seconds=result['elapsed_seconds'],
        lipids=result['metrics']['lipids_formed'],invariant_failures=result['metrics']['atom_port_invariant_failures']))
    return folder


if __name__=='__main__':main()
