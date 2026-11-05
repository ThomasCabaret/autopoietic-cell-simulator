"""One technical BI1 pilot at100; not a screening grid."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write
from scripts.campaign import prepare,export_recipe,status
from simulator.campaign_worker import execute
from experiments.prepare_boundary_transfer import scenario


def main():
    p=ROOT/'campaigns/boundary_pilot.json'
    write(p,dict(name='BI1P predeclared100-unit pilot',workers=1,checkpoint_seconds=30.,record_trajectory=False,
        tasks=[dict(scenario=scenario(0,'active',100.))],comparison_policy='BATCH_43_PLAN: mechanical feasibility, cost and local products only'))
    folder=prepare(p,ROOT/'outputs/boundary_pilots');recipe=ROOT/'research/campaign_recipes'/('BI1P_'+folder.name.removeprefix('campaign_'));export_recipe(folder,recipe)
    write(ROOT/'research/BATCH_43_PILOT.json',dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix()))
    execute(folder,'task0000');state=status(folder);r=read(folder/state['tasks'][0]['result']);m=r['metrics'];b=m['boundary']
    print(dict(folder=str(folder),elapsed_seconds=r['elapsed_seconds'],complete=state['counts']['complete'],
        L=m['lipids_formed'],invariant_failures=m['atom_port_invariant_failures'],
        final=b['history'][-1],ever_inserted=b['ever_inserted'],inside=b['ever_inserted_born_inside']))
    return folder


if __name__=='__main__':main()
