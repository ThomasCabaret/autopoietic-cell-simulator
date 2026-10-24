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
    for folder in folders:
        files.update(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                     and (p.suffix=='.py' or p.name in ('config.json','scenario.json','recipe.json')))
    manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(files)}
    out=ROOT/f'deliverables/local_chemistry_simulator_{datetime.now():%Y%m%d}.zip'
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
