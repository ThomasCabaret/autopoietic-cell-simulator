"""One CB1 technical pilot at100, no parameter sweep."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write
from scripts.campaign import prepare,export_recipe,status
from simulator.campaign_worker import execute
from experiments.prepare_compact_transfer import scenario


def main():
    p=ROOT/'campaigns/compact_pilot.json'
    write(p,dict(name='CB1P predeclared100-unit pilot',workers=1,checkpoint_seconds=30.,record_trajectory=False,
        tasks=[dict(scenario=scenario(0,'active',100.))],comparison_policy='BATCH_44_PLAN: mechanical feasibility and cost, not expression success'))
    folder=prepare(p,ROOT/'outputs/compact_pilots');recipe=ROOT/'research/campaign_recipes'/('CB1P_'+folder.name.removeprefix('campaign_'));export_recipe(folder,recipe)
    write(ROOT/'research/BATCH_44_PILOT.json',dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix()))
    execute(folder,'task0000');state=status(folder);r=read(folder/state['tasks'][0]['result']);m=r['metrics'];b=m['boundary']
    from experiments.mixed_calibration import weighted
    print(dict(folder=str(folder),elapsed_seconds=r['elapsed_seconds'],complete=state['counts']['complete'],L=m['lipids_formed'],
        invariant_failures=m['atom_port_invariant_failures'],valid_fraction=weighted(b['history'],'valid',0.,100.),
        final=b['history'][-1],inserted=b['ever_inserted_born_inside']))
    return folder


if __name__=='__main__':main()
