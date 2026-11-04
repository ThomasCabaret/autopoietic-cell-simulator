"""One predeclared100-unit MX2 pilot, not a calibration sweep."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write
from scripts.campaign import prepare,export_recipe,status
from simulator.campaign_worker import execute
from experiments.prepare_cooperative_synthesis import scenario


def main():
    p=ROOT/'campaigns/cooperative_pilot.json'
    write(p,dict(name='MX2P predeclared100-unit pilot',workers=1,checkpoint_seconds=30.,record_trajectory=False,
        tasks=[dict(scenario=scenario(0,'cooperative',100.))],comparison_policy='BATCH_42_PLAN: one technical/product pilot, no rate selection or long-run success claim'))
    folder=prepare(p,ROOT/'outputs/cooperative_pilots');recipe=ROOT/'research/campaign_recipes'/('MX2P_'+folder.name.removeprefix('campaign_'));export_recipe(folder,recipe)
    write(ROOT/'research/BATCH_42_PILOT.json',dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix()))
    execute(folder,'task0000');state=status(folder);r=read(folder/state['tasks'][0]['result']);m=r['metrics'];g=m['genetics']
    print(dict(folder=str(folder),elapsed_seconds=r['elapsed_seconds'],complete=state['counts']['complete'],
        G=g['detached_copy_sets_ever'],F=g['translated_detached_ever'],L=m['lipids_formed'],
        invariant_failures=m['atom_port_invariant_failures'],wrong_max=max(q['wrong_double_edges'] for q in m['history'])))
    return folder


if __name__=='__main__':main()
