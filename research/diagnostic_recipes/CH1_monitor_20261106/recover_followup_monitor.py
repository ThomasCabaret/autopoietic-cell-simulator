"""Attach an IO-retry monitor to a frozen job after a Windows read conflict.

No worker restart or frozen-file edit. Only orchestration JSON reads change;
the original deadline, step, chemistry, analysis and gates remain frozen.
"""
import argparse,hashlib,importlib,json,os,sys,time,traceback
from pathlib import Path


def retry_read(reader,path,default=None):
    for attempt in range(7):
        try:return reader(path,default)
        except PermissionError:
            if os.name!='nt' or attempt==6:raise
            time.sleep(.01*2**attempt)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--job',type=Path,required=True);a=p.parse_args()
    job=a.job.resolve();sys.path.insert(0,str(job/'runtime'))
    from scripts import campaign,expression_followup as controller,mechanism_followup as adapter
    from simulator.campaign_io import read,write,lock
    cfg=controller.validate_job(job)
    analysis=importlib.import_module('experiments.'+adapter.STUDIES[cfg['study']]['review'])
    # This overlay wraps file reads, not chemistry or checkpoint deserialization.
    campaign.read=lambda path,default=None:retry_read(read,path,default)
    controller.read=campaign.read
    with lock(job/'followup.lock'):
        state=campaign.read(job/'state.json')
        if state['phase']!='needs_attention' or 'PermissionError: [Errno 13]' not in state.get('error',''):
            raise ValueError('Only a recorded IO sharing-conflict failure may be attached')
        stamp=time.time_ns();audit=job/f'monitor_recovery_{stamp}.json'
        write(audit,dict(previous_state=state,source=str(Path(__file__).resolve()),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            job_sha256=controller.digest(job/'job.json'),scope=__doc__))
        state=dict(state);state.pop('error');state.update(phase='running_'+str(state['stage']),updated=time.time(),
            monitor_recovery=str(audit));write(job/'state.json',state)
        while True:
            try:phase=controller.step(job,analysis.collect,analysis.decide)
            except Exception:
                state=campaign.read(job/'state.json');state.update(phase='needs_attention',error=traceback.format_exc(),updated=time.time())
                write(job/'state.json',state);raise
            if phase in ('needs_attention','needs_interpretation','paused'):return
            time.sleep(15)


if __name__=='__main__':main()
