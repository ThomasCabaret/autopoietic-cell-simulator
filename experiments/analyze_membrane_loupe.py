"""Read bounded capture geometry: spring-length compatibility versus actual face capture."""
import argparse,hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.docking import port_geometry


def analyze(path):
    path=Path(path);raw=json.loads(path.read_text());cfg=json.loads((path.parent/'scenario.json').read_text())
    import simulator.docking as docking
    evidence=json.loads((path.parent/'result.json').read_text())
    geometry_hash=hashlib.sha256(Path(docking.__file__).read_bytes()).hexdigest()
    assert geometry_hash==evidence['source_sha256']['simulator/docking.py'],'Use the captured docking sources'
    m=cfg['chemistry']['membrane'];ids=raw['units'];i,j,a,b=raw['contact'];i=ids.index(i);j=ids.index(j)
    rows=[]
    for r in raw['frames']:
        head,tail,_,_=port_geometry(np.array(r['positions']),len(ids),1.,m['short_length'])
        q=float(np.sum((head[j,b]-head[i,a])**2)+np.sum((tail[j,b]-tail[i,a])**2))
        rows.append(dict(time=r['time'],q=q,capture_compatible=q<m['dock_capture']**2,
            attraction_active=q<16*m['dock_width']**2,
            bound=r['port_partners'][i][a]==raw['contact'][1],head_gap=r['head_gap'],tail_gap=r['tail_gap']))
    before=max((r for r in rows if r['time']<raw['trigger']),key=lambda r:r['time'])
    after=next(r for r in rows if r['time']>=raw['trigger'])
    report=dict(trigger=raw['trigger'],before=before,after=after,geometry_source_sha256=geometry_hash,
        capture_q_threshold=m['dock_capture']**2,attraction_q_cutoff=16*m['dock_width']**2,
        recapture_compatible_samples_after=sum(r['capture_compatible'] for r in rows if r['time']>=raw['trigger']),
        rebound_observed=any(r['bound'] for r in rows if r['time']>=raw['trigger']),rows=rows,
        input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scope='Geometry of the selected lost face pair only. Correct spring lengths do not imply that both docking ports overlap. No causal feedback, no new dynamics, no population-level rate inference.')
    out=path.parent/('analysis_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');(out/'driver.py').write_bytes(Path(__file__).read_bytes())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,1,figsize=(9,6),sharex=True,constrained_layout=True)
    t=[r['time'] for r in rows]
    axes[0].plot(t,[r['q'] for r in rows],label='Écart quadratique des ports')
    axes[0].axhline(report['capture_q_threshold'],ls='--',color='green',label='Limite de recapture')
    axes[0].axhline(report['attraction_q_cutoff'],ls=':',color='orange',label='Fin de l’attraction')
    axes[0].set(ylabel='q',yscale='log');axes[0].legend()
    axes[1].plot(t,[r['head_gap'] for r in rows],label='Distance H–H')
    axes[1].plot(t,[r['tail_gap'] for r in rows],label='Distance T–T');axes[1].legend()
    axes[1].set(xlabel='Temps simulé',ylabel='Distance')
    for ax in axes:ax.axvline(raw['trigger'],color='red',ls='--');ax.grid(alpha=.2)
    fig.suptitle('Contact47–48 : dissociation sans étirement excessif, ports déjà désalignés')
    fig.savefig(out/'geometry.png',dpi=150);plt.close(fig)
    print(json.dumps(dict(output=str(out),**{k:v for k,v in report.items() if k!='rows'})));return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('path',type=Path);a=p.parse_args();analyze(a.path)
