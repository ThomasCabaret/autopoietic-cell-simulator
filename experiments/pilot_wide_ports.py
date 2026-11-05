"""CW1P one fixed100-unit technical test, before selected wider-port followups."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_exchange_ablation import scenario
from simulator.campaign_io import read,write
from scripts.campaign import prepare,export_recipe,status
from simulator.campaign_worker import execute
from experiments.mixed_calibration import weighted


def main():
    cfg=scenario(0,True);cfg['duration']=100.
    p=ROOT/'campaigns/wide_ports_pilot.json'
    write(p,dict(name='CW1P fixed100-unit wider-port pilot',workers=1,checkpoint_seconds=30.,record_trajectory=False,
        tasks=[dict(scenario=cfg)],comparison_policy='BATCH_45_PLAN: one predeclared technical pilot, no grid or rate change'))
    folder=prepare(p,ROOT/'outputs/wide_ports_pilots');recipe=ROOT/'research/campaign_recipes'/('CW1P_'+folder.name.removeprefix('campaign_'));export_recipe(folder,recipe)
    write(ROOT/'research/BATCH_45_WIDE_PILOT.json',dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix()))
    execute(folder,'task0000');state=status(folder);r=read(folder/state['tasks'][0]['result']);m=r['metrics'];b=m['boundary']
    print(dict(folder=str(folder),complete=state['counts']['complete'],elapsed=r['elapsed_seconds'],L=m['lipids_formed'],
        invariants=m['atom_port_invariant_failures'],valid_fraction=weighted(b['history'],'valid',0.,100.),
        final=b['history'][-1],inserted=b['ever_inserted_born_inside']))


if __name__=='__main__':main()
