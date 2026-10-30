"""Audit completed LT2 and render the functional regression, not just motion speed."""
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status


def verify_completed(folder,count):
    folder=Path(folder)
    manifest=validate(folder);s=status(folder)
    assert s['counts']['complete']==count and not s['controller_active']
    report=json.loads((folder/'demo_motion_analysis.json').read_text())
    assert report['complete_cohort']
    assert report['analysis_sha256']==manifest['source_sha256']['demo_motion_report.py']
    expected={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    for task,state,row in zip(manifest['tasks'],s['tasks'],report['rows']):
        p=folder/state['result'];r=json.loads(p.read_text())
        assert r['completed'] and not r['error'] and r['scenario']==task['scenario']
        assert r['source_sha256']==expected
        assert hashlib.sha256(p.read_bytes()).hexdigest()==row['result_sha256']
    return manifest,s,report


def main():
    folder=ROOT/'outputs/demo_motion_campaigns/campaign_20261030T065759494210Z'
    manifest,s,report=verify_completed(folder,16)
    out=ROOT/'outputs/reviews'/('LT2_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    selected=[r for r in report['rows'] if r['preset'].startswith('integrated')]
    (out/'summary.json').write_text(json.dumps(dict(rows=selected,all16_results_verified=True,
        manifest_sha256=hashlib.sha256((folder/'manifest.json').read_bytes()).hexdigest(),
        analysis_sha256=report['analysis_sha256']),indent=2)+'\n',encoding='utf-8')
    (out/'driver.py').write_bytes(Path(__file__).read_bytes())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,axes=plt.subplots(2,2,figsize=(11,7),constrained_layout=True)
    keys=('regular_parent_closed_fraction','catalyzed_incorporated','detached_copy_sets_ever','translated_detached_ever')
    titles=('Grande membrane : fraction fermée, grille0,5','Composants catalysés puis utilisés','Nouveaux G complets libérés','Nouveaux F complets libérés')
    for ax,key,title in zip(axes.flat,keys,titles):
        for offset,motion,label in ((-.18,'brownian','Brownien'),(.18,'langevin','Langevin0,1')):
            values=[next(r['metrics'][key] for r in selected if r['seed']==seed and r['motion']==motion and r['comparison']=='base') for seed in range(3)]
            ax.bar(np.arange(3)+offset,values,width=.36,label=label)
        ax.set(title=title,xlabel='Graine');ax.set_xticks([0,1,2]);ax.grid(axis='y',alpha=.2)
        if key.startswith('regular'):ax.set_ylim(0,1)
    axes[0,0].legend();fig.suptitle('LT2 achevé : amélioration des microdémos, fragilité du bain intégré')
    fig.savefig(out/'functional_transfer.png',dpi=150);plt.close(fig)
    print(json.dumps(dict(output=str(out),verified=16)))


if __name__=='__main__':main()
