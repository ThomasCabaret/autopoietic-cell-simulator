"""One dispersed L1 pilot, bounded t100; preserve source recipes, not raw data."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve
from simulator.campaign_io import write
from scripts.campaign import prepare,export_recipe


def scenario():
    return resolve(dict(schema_version=1,model='lipid_synthesis',name='L1_dispersed_pilot_s0',branch='L1',
        seed=0,duration=100.,chemistry={},engine=dict(dt=.002,sample_every=250,reaction_every=5),
        mechanics=dict(motion='langevin',mass=1.,damping=.1)))


def main():
    # A single technical pilot, no screen, rate search or follow-up.
    p=ROOT/'campaigns/lipid_pilot.json'
    write(p,dict(name='L1 one dispersed technical pilot, not biological validation',workers=1,
        checkpoint_seconds=30.,record_trajectory=False,tasks=[dict(scenario=scenario())],
        comparison_policy='BATCH_36_PLAN: t100,seed0 only,prepared F01 and initially free H/T, '
            'same capture constants as MD2 but new ligand types. No P/R, membrane or expression. No follow-up.'))
    folder=prepare(p,ROOT/'outputs/lipid_pilots');recipe=ROOT/'research/campaign_recipes'/('L1P_'+folder.name.removeprefix('campaign_'))
    export_recipe(folder,recipe)
    write(ROOT/'research/BATCH_36_RECIPES.json',dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix(),plan='research/BATCH_36_PLAN.md'))
    print(folder)


if __name__=='__main__':main()
