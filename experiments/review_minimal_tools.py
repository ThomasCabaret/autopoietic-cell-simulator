"""Reproducible MIN1 summary and a curated figure, never a chemistry input."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.minimal_tool_followup import controller,collect,count,decide,expression_decision
from simulator.campaign_io import read,write


def review(figure=False):
    job=Path((ROOT/'outputs/minimal_tool_followups/latest.txt').read_text().strip())
    cfg=controller.validate_job(job);reports=[collect(Path(f),False) for f in cfg['campaigns']]
    if len(reports[0]['rows'])==12:reports[0]['decision']=decide(reports[0]['rows'])
    if len(reports[1]['rows'])==9:reports[1]['decision']=expression_decision(reports[1]['rows'])
    summary=[]
    for i,report in enumerate(reports):
        for r in report['rows']:
            summary.append(dict(label=r['label'],G_new=r['G'],F_new=r['F'],
                prepared=count(r),expressed=count(r,'expressed'),expressed_G_used=count(r,'expressed','G',True),
                expressed_F_used=count(r,'expressed','F',True),max_operations=r['flux']['max_operations']))
    value=dict(job=str(job),state=read(job/'state.json'),cohorts=reports,summary=summary)
    write(job/'review.json',value)
    lines=['# MIN1 — outils préparés puis expression','',
        'Compte rendu automatique : stocks fermés ; produits incorporés à un squelette, pas nécessairement à un outil complet.','',
        '| Essai | G nouveaux | F nouveaux | Produits par F préparé | Produits par F exprimé | G / F issus de F exprimés et utilisés |',
        '| --- | ---: | ---: | ---: | ---: | --- |']
    for r in summary:lines.append(f"| {r['label']} | {r['G_new']} | {r['F_new']} | {r['prepared']} | {r['expressed']} | {r['expressed_G_used']} / {r['expressed_F_used']} |")
    lines+=['','Les conditions initiales et inventaires complets figurent dans review.json ; une phase incomplète ne donne pas de décision.']
    (job/'review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if figure:
        a=reports[0]['rows']
        if len(a)!=12:raise ValueError('Curated figure requires all12 prepared-tool trials')
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        variants=('long','short','split','no_boost');names=('F001','F01 + F0 libre','Sites séparés','Sans bonus')
        colors=('#167d9a','#d58328','#7763a8');fig,axes=plt.subplots(1,2,figsize=(10,4.1))
        for ax,family,title in zip(axes,('G','F'),('Composites G fabriqués','Composites F fabriqués')):
            for seed,color in enumerate(colors):
                vals=[count(next(r for r in a if r['label']==f'MIN1_A_{v}_s{seed}'),family=family) for v in variants]
                ax.scatter(np.arange(4)+(seed-1)*.12,vals,color=color,s=45,label=f'Graine {seed}',zorder=3)
            ax.set_xticks(range(4),names,rotation=14);ax.set_title(title);ax.set_ylim(bottom=-1)
            ax.set_ylabel('Produits attribués aux outils préparés');ax.grid(axis='y',alpha=.2)
        axes[1].legend(frameon=False);fig.suptitle('MIN1 · MD2/Langevin, témoins et ablation · t400 · quatre outils préparés',fontsize=12)
        fig.text(.5,.015,'Stocks finis, mêmes 150 billes ; ni expression ni maintien démontrés par ce panneau.',ha='center',fontsize=9)
        fig.tight_layout(rect=(0,.05,1,.94));target=ROOT/'research/BATCH_32_PREPARED.png';fig.savefig(target,dpi=160);plt.close(fig)
        print(str(target))
    print(json.dumps(dict(state=value['state'],counts=[r['counts'] for r in reports],rows=summary,
        decisions=[r.get('decision') for r in reports]),indent=2));return value


if __name__=='__main__':review('--figure' in sys.argv)
