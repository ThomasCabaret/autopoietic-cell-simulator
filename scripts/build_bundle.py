"""Build a movable Windows source distribution without copying the environment."""
import hashlib
from datetime import datetime
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def main():
    verification=json.loads((ROOT/'research/ENGINE_VERIFICATION.json').read_text(encoding='utf-8'))
    files=set()
    for pattern in ('simulator/*.py','demonstrators/*.bat','demonstrators/*.md','demonstrators/configs/*.json'):
        files.update(ROOT.glob(pattern))
    files.update(ROOT.glob('visualizer/*.py'));files.update(ROOT.glob('visualizer/shaders/*'))
    files.update(ROOT/p for p in ('visualizer.bat','install_visualizer.bat','requirements-viewer.txt',
        'docs/VISUALIZER.md','experiments/smoke_visualizer.py','experiments/benchmark_visualizer.py'))
    files.update(ROOT/p for p in ('docs/DEMOS.md','demonstrators/catalog.json',
        'experiments/prepare_demo_catalog.py','experiments/smoke_demo_menu.py'))
    files.update(ROOT/p for p in ('README.md','SIMULATOR_ARCHITECTURE.md','requirements.txt',
        'CONTRIBUTING.md','GIT_SETUP.md','THIRD_PARTY_NOTICES.md',
        '.gitignore','.gitattributes','.editorconfig',
        'scripts/dispatch.py','scripts/launch.bat','scripts/reconstruct_experiment.py',
        'research/REPRODUCTION.md','research/ENGINE_MIGRATION.md','research/ENGINE_VERIFICATION.json',
        'research/BATCH_03.md','research/BATCH_03_RECIPES.json',
        'research/BATCH_03_MEMBRANES.png','research/BATCH_03_LIGATION.png',
        'research/BATCH_03_PLAN.md','research/MATURITY.md','research/PRIORITIES.md','research/MODEL.md'))
    files.update(ROOT/p for p in ('research/BATCH_04.md','research/BATCH_04_PLAN.md',
        'research/BATCH_04_DECISIONS.md','research/BATCH_04_RECIPES.json',
        'research/BATCH_04_CONTROLS.png','research/BATCH_04_COUPLING.png','research/BATCH_04_TOOL.png',
        '.agents/skills/local-chemistry-research/SKILL.md'))
    files.update(ROOT/p for p in ('research/BATCH_05.md','research/BATCH_05_PLAN.md',
        'research/BATCH_05_DECISIONS.md','research/BATCH_05_RECIPES.json',
        'research/BATCH_05_COEXISTENCE.png','research/PROJECT_HEALTH.md',
        'experiments/run_batch3.py','experiments/run_batch4.py','experiments/run_batch5.py',
        'experiments/make_batch3_report.py','experiments/make_batch4_report.py','experiments/make_batch5_report.py'))
    files.update(ROOT/p for p in ('AGENTS.md','RESEARCH_DIRECTION.md',
        'research/branches.json','research/LOG.md'))
    files.update(ROOT/p for p in ('research/BATCH_06.md','research/BATCH_06_PLAN.md',
        'research/BATCH_06_DECISIONS.md','research/BATCH_06_RECIPES.json',
        'research/BATCH_06_CONSTRUCTION.png','experiments/run_batch6.py','experiments/make_batch6_report.py'))
    files.update(ROOT/p for p in ('research/BATCH_07.md','research/BATCH_07_PLAN.md',
        'research/BATCH_07_RECIPES.json','research/minimal_cell_spec.json',
        'research/CELL_ARCHITECTURE.md','research/CELL_DEPENDENCIES.png',
        'research/CELL_INTERACTIONS.md','research/CELL_INTERACTIONS.png','research/CELL_SIZE.png',
        'research/INTEGRATION_TESTS.json','experiments/audit_cell_design.py','experiments/render_cell_design.py'))
    files.update(ROOT/p for p in ('research/BATCH_08.md','research/BATCH_08_PLAN.md',
        'research/BATCH_08_DECISIONS.md','research/BATCH_08_RECIPES.json',
        'research/BATCH_08_TRANSFER.png','research/BATCH_08_EXPRESSION.png',
        'experiments/run_batch8.py','experiments/make_batch8_report.py','experiments/audit_precursor_trace.py'))
    files.update(ROOT/p for p in ('research/BATCH_09.md','research/BATCH_09_PLAN.md',
        'research/BATCH_09_RECIPES.json','research/BATCH_09_MEMBRANE.png','research/LOCALITY_AUDIT.md',
        'research/KINETICS_AND_PERFORMANCE.md','experiments/run_batch9.py',
        'experiments/make_batch9_report.py','experiments/verify_batch9.py',
        'experiments/audit_membrane_exchange.py','experiments/profile_simulator.py','experiments/smoke_membrane_bath.py'))
    files.update(ROOT/p for p in ('scripts/campaign.py','scripts/campaign.ps1',
        'start_campaign.bat','campaign_status.bat','stop_campaign.bat','resume_campaign.bat','analyze_campaign.bat',
        'campaigns/README.md','campaigns/membrane_kinetics.json','research/BATCH_10_PLAN.md','research/BATCH_10.md'))
    files.update(ROOT/p for p in ('campaigns/membrane_robustness.json','research/BATCH_10_RESULTS.md',
        'research/BATCH_11_PLAN.md','research/BATCH_11.md','experiments/pilot_batch11.py','experiments/analyze_batch11.py'))
    files.update(ROOT/p for p in ('campaigns/membrane_terminal_exchange.json','research/BATCH_11_RESULTS.md',
        'research/BATCH_12_PLAN.md','research/BATCH_12.md','research/BATCH_12_DECISIONS.md',
        'experiments/trace_exchange_geometry.py','experiments/pilot_batch12.py'))
    files.update(ROOT/p for p in ('research/DESIGN_PRINCIPLES.md','research/BATCH_12_RESULTS.md',
        'research/BATCH_13_PLAN.md','research/BATCH_13.md','research/BATCH_13_PILOTS.json',
        'campaigns/common_bath.json','experiments/run_batch13.py','experiments/analyze_batch12.py'))
    files.update(ROOT/p for p in ('experiments/benchmark_cell_workload.py','research/NUMERICS_AND_RENEWAL.md'))
    files.update(ROOT/p for p in ('research/BATCH_14_PLAN.md','research/BATCH_14.md',
        'experiments/prepare_batch14.py','experiments/analyze_batch14.py','campaigns/genetic_kinetics.json'))
    files.update(ROOT/p for p in ('research/BATCH_14_RESULTS.md','research/BATCH_14_BOOTSTRAP.md',
        'research/BATCH_14_PILOTS.json','experiments/prepare_batch14_bootstrap.py','campaigns/constructed_tool.json'))
    files.update(ROOT/p for p in ('research/BATCH_14_BOOTSTRAP_RESULTS.md','research/BATCH_15_PLAN.md',
        'research/BATCH_15.md','research/HOMEOSTASIS.md','experiments/inventory_audit.py',
        'experiments/analyze_constructed_tool.py','experiments/prepare_compartment_controls.py',
        'campaigns/compartment_controls.json'))
    files.update(ROOT/p for p in ('research/BATCH_15_RESULTS.md','research/BATCH_16_PLAN.md',
        'research/BATCH_16.md','research/BATCH_16_PILOTS.json','research/OPEN_BOUNDARY.md',
        'experiments/prepare_density_campaign.py','campaigns/density_transfer.json'))
    files.update(ROOT/p for p in ('research/BATCH_16_RESULTS.md','research/BATCH_17_PLAN.md',
        'research/BATCH_17.md','research/BATCH_17_PILOTS.json','experiments/prepare_numerical_campaign.py',
        'experiments/analyze_numerical_campaign.py','campaigns/numerical_refinement.json'))
    files.update(ROOT/p for p in ('research/BATCH_17_RESULTS.md','research/BATCH_18_PLAN.md','research/BATCH_18.md',
        'research/BATCH_18_PILOTS.json','research/BATCH_18_FOLLOWUP.json','research/AUTOMATED_EXPLORATION.md',
        'experiments/prepare_cadence_campaign.py','experiments/analyze_cadence_campaign.py',
        'scripts/numerical_followup.py','scripts/numerical_followup.ps1',
        'start_followup.bat','followup_status.bat','stop_followup.bat','resume_followup.bat',
        'campaigns/cadence_controls.json'))
    files.add(ROOT/'experiments/diagnose_fragment_capture.py')
    files.update(p for p in (ROOT/'research/campaign_recipes').rglob('*') if p.is_file()
        and ('__pycache__' not in p.parts) and (p.suffix=='.py' or p.name in ('manifest.json','manifest.sha256','plan.json')))
    files.update(p for p in (ROOT/'research/legacy_reference').rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
    files.add(ROOT/'research/LEGACY_PROJECT_NOTES.md')
    folders=[ROOT/Path(p).parent for p in verification['validated_runs']]
    folders.append(ROOT/'research/runs/V6_s1_20261023T115206264055Z')
    batch=json.loads((ROOT/'research/BATCH_03_RECIPES.json').read_text(encoding='utf-8'))
    folders.extend(ROOT/Path(p).parent for p in batch['recipes'])
    batch4=json.loads((ROOT/'research/BATCH_04_RECIPES.json').read_text(encoding='utf-8'))
    folders.extend(ROOT/Path(p).parent for p in batch4['recipes'])
    batch5=json.loads((ROOT/'research/BATCH_05_RECIPES.json').read_text(encoding='utf-8'))
    folders.extend(ROOT/Path(p).parent for p in batch5['recipes'])
    batch6=json.loads((ROOT/'research/BATCH_06_RECIPES.json').read_text(encoding='utf-8'))
    folders.extend(ROOT/Path(p).parent for p in batch6['recipes'])
    batch7=json.loads((ROOT/'research/BATCH_07_RECIPES.json').read_text(encoding='utf-8'))
    folders.extend(ROOT/Path(p).parent for p in batch7['recipes'])
    batch8=json.loads((ROOT/'research/BATCH_08_RECIPES.json').read_text(encoding='utf-8'))
    folders.extend(ROOT/Path(p).parent for p in batch8['recipes'])
    batch9=json.loads((ROOT/'research/BATCH_09_RECIPES.json').read_text(encoding='utf-8'))
    folders.extend(ROOT/Path(p).parent for p in batch9['recipes'])
    folders.append(ROOT/'research/engine_runs/M1B0_exchange_geometry_s0_20261027T065021427657Z')
    folders.extend(ROOT/Path(p).parent for p in json.loads((ROOT/'research/BATCH_13_PILOTS.json').read_text(encoding='utf-8'))['recipes'])
    folders.extend(ROOT/Path(p).parent for p in json.loads((ROOT/'research/BATCH_14_PILOTS.json').read_text(encoding='utf-8'))['recipes'])
    folders.extend(ROOT/Path(p).parent for p in json.loads((ROOT/'research/BATCH_16_PILOTS.json').read_text(encoding='utf-8'))['recipes'])
    folders.extend(ROOT/Path(p).parent for p in json.loads((ROOT/'research/BATCH_17_PILOTS.json').read_text(encoding='utf-8'))['recipes'])
    folders.extend(ROOT/Path(p).parent for p in json.loads((ROOT/'research/BATCH_18_PILOTS.json').read_text(encoding='utf-8'))['recipes'])
    for folder in folders:
        files.update(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                     and (p.suffix=='.py' or p.name in ('config.json','scenario.json','recipe.json')))
    manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(files)}
    out=ROOT/f'deliverables/local_chemistry_simulator_{datetime.now():%Y%m%d_%H%M%S%f}.zip'
    out.parent.mkdir(parents=True,exist_ok=True)
    prefix='local_chemistry_simulator/'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(files): archive.write(p,prefix+p.relative_to(ROOT).as_posix())
        archive.writestr(prefix+'DISTRIBUTION_MANIFEST.json',json.dumps(manifest,indent=2))
    with zipfile.ZipFile(out) as archive:
        assert archive.testzip() is None
        assert all(hashlib.sha256(archive.read(prefix+name)).hexdigest()==digest for name,digest in manifest.items())
    print(json.dumps({'archive':str(out),'files':len(files),'bytes':out.stat().st_size,
                      'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'all_member_hashes_verified':True}))


if __name__=='__main__': main()
