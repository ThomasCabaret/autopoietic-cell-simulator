"""Recover only CB1 analysis with its untouched frozen interpreter and sources."""
import argparse,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import expression_followup as controller
from simulator.campaign_io import read,write


def recover(job):
    cfg=controller.validate_job(job);snapshot=controller.status(job)
    if not cfg['gate'].startswith('CB1_') or snapshot['active'] or any(c['controller_active'] or c['counts']['complete']!=9 for c in snapshot['campaigns']):
        raise ValueError('Require complete inactive nine-case CB1')
    if snapshot['state']['phase']=='needs_interpretation':raise ValueError('Already analyzed; preserve existing report')
    folder=Path(cfg['campaigns'][0]);paths=list(folder.glob('tasks/*/attempts/*/result.json'))
    before={str(p):controller.digest(p) for p in paths}
    if len(before)!=9:raise ValueError('Require exactly nine successful result files')
    failure=job/'analysis_failure_before_recovery.json'
    if failure.exists():raise ValueError('Recovery already attempted; inspect before proceeding')
    write(failure,snapshot['state'])
    frozen=job/'runtime/scripts/boundary_transfer_followup.py'
    command=[sys.executable,str(frozen),'review','--job',str(job),'--compact']
    result=subprocess.run(command,cwd=job,text=True,capture_output=True,check=True)
    report=json.loads(result.stdout)
    if not all(r['label'].startswith('CB1_') for r in report['rows']):raise ValueError('Wrong recovered analysis')
    if before!={str(p):controller.digest(p) for p in paths}:raise ValueError('Simulation evidence changed')
    controller.validate_job(job)
    dest=job/'report_recovered_1.json';write(dest,report)
    state=snapshot['state'];error=state.pop('error',None)
    state.update(phase='needs_interpretation',updated=time.time(),report_0=str(dest),report_0_sha256=controller.digest(dest),
        prior_analysis_error=error,analysis_failure_archive=str(failure),
        reason='Recovered with original frozen CB1 analyzer and explicit --compact; no simulations rerun')
    write(job/'state.json',state)
    provenance=dict(job=str(job),report=str(dest),report_sha256=controller.digest(dest),
        archived_failure_sha256=controller.digest(failure),command=command,
        recovery_source_sha256=controller.digest(Path(__file__)),result_hashes_unchanged=before,
        original_runtime_sources_unchanged=True,decision=report['decision'])
    write(ROOT/'research/BATCH_45_CB1_RECOVERY.json',provenance)
    return provenance


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--job',type=Path);a=p.parse_args()
    job=a.job or Path((ROOT/'outputs/compact_transfer_followups/latest.txt').read_text().strip())
    print(json.dumps(recover(job),indent=2))
