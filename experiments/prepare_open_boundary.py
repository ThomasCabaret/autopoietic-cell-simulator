"""OB1: bounded open precursor transport, same source calendar across dt pairs."""
from pathlib import Path
from simulator.campaign_io import write
from scripts.campaign import prepare,export_recipe,digest

ROOT=Path(__file__).resolve().parents[1]


def scenario(seed,dt):
    return dict(schema_version=1,model='open_bath',name=f'OB1_dt{dt}_s{seed}',branch='OB1',seed=seed,duration=80.,
        chemistry=dict(initial_counts=[0,0],influx_per_length=[.1,.1],source_seed=1701+seed,
            max_samples=512),engine=dict(dt=dt,reaction_every=round(.02/dt),sample_every=round(.2/dt)))


def plan():
    return dict(name='OB1 open precursor transport, fixed source/sink protocol',workers=2,
        checkpoint_seconds=30.,kinetic_window=20.,record_trajectory=False,
        tasks=[dict(scenario=scenario(s,dt)) for s in range(3) for dt in (.004,.002)],
        comparison_policy='BATCH_55_PLAN: three seeds x dt.004/.002,80 units; boundary interval.02 fixed, '
            'same source calendar within pair. No chemistry/cell. Bounded construction screen, not stationary-state or convergence proof.')


if __name__=='__main__':
    dest=ROOT/'outputs/open_boundary';dest.mkdir(parents=True,exist_ok=True)
    write(dest/'plan.json',plan());folder=prepare(dest/'plan.json',dest)
    recipe=ROOT/'research/campaign_recipes'/('OB1_'+folder.name.removeprefix('campaign_'))
    export_recipe(folder,recipe)
    import shutil
    for name in ('prepare_open_boundary.py','review_open_boundary.py'):
        shutil.copyfile(ROOT/'experiments'/name,recipe/name)
    write(ROOT/'research/BATCH_55_OB1_RECIPES.json',dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix(),
        manifest_sha256=digest(folder/'manifest.json'),analysis_sha256=digest(recipe/'review_open_boundary.py')))
    print(folder)
