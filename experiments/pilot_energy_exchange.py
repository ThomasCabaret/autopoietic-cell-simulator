"""EG1P100 technical and thermal pilot; no tuning or resampled success."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_energy_exchange import scenario
from simulator.campaign_io import read,write
from scripts.campaign import prepare,export_recipe,status
from simulator.campaign_worker import execute
from experiments.mixed_calibration import weighted


def main():
    path=ROOT/'campaigns/energy_exchange_pilot.json'
    write(path,dict(name='EG1P fixed100-unit pilot',workers=1,checkpoint_seconds=30.,record_trajectory=False,
        tasks=[dict(scenario=scenario(0,100.))],comparison_policy='BATCH_46_PLAN technical pilot: fixed gate, no retry/grid'))
    folder=prepare(path,ROOT/'outputs/energy_exchange_pilots');recipe=ROOT/'research/campaign_recipes'/('EG1P_'+folder.name.removeprefix('campaign_'));export_recipe(folder,recipe)
    write(ROOT/'research/BATCH_46_EG1_PILOT.json',dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix()))
    execute(folder,'task0000');state=status(folder);r=read(folder/state['tasks'][0]['result']);m=r['metrics']
    temp=read(folder/state['tasks'][0]['motion_audit'])['history'];late=[q['kinetic_temperature'] for q in temp if q['time']>=75.]
    print(dict(campaign=str(folder),elapsed=r['elapsed_seconds'],L=m['lipids_formed'],invariants=m['atom_port_invariant_failures'],
        valid_fraction=weighted(m['boundary']['history'],'valid',0.,100.),late_T=sum(late)/len(late),gate=m['exchange_gate_stats']))


if __name__=='__main__':main()
