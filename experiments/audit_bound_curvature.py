"""BC1: derived four-bead bending energy and bounded passive CH1 snapshots."""
import hashlib,json,math,shutil,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import numpy as np
from simulator.docking import bound_port_force
from simulator.observations import components


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,data):Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')


def pair_pose(theta,axial=.65,long=1.,short=.92):
    u=np.array([[1.,0.],[np.cos(theta),np.sin(theta)]]);t=np.column_stack((-u[:,1],u[:,0]))
    d=(long+short)/4*(t[0]+t[1])-axial/2*(u[1]-u[0])
    heads=np.array([[0.,0.],d]);return np.vstack((heads,heads+axial*u))


def local_profile(theta,epsilon=4.,width=.6,axial=.65,long=1.,short=.92):
    k=epsilon*(1-np.exp(-8.))/width**2;difference=long-short
    offset=-epsilon*(1-9*np.exp(-8.));preferred=-2*np.arctan(difference/(2*axial))
    curvature=k*(axial**2+difference**2/4)/2
    energy=offset+k*(axial*np.sin(np.asarray(theta)/2)+difference/2*np.cos(np.asarray(theta)/2))**2
    return energy,float(preferred),float(curvature)


def statistics(values):
    values=np.asarray(values,dtype=float)
    return dict(count=len(values),mean=float(values.mean()),std=float(values.std()),
        q05=float(np.quantile(values,.05)),q50=float(np.median(values)),q95=float(np.quantile(values,.95))) if len(values) else dict(count=0)


def snapshot(folder,task,hashes):
    state=read(folder/'tasks'/task['id']/'state.json')
    if state['status']!='complete':raise ValueError('Require complete final checkpoint')
    path=folder/state['checkpoint']
    with np.load(path,allow_pickle=False) as data:
        meta=json.loads(str(data['metadata']));pos=data['positions'].copy()
    if meta['source_sha256']!=hashes or meta['config']!=task['scenario']:raise ValueError('Checkpoint source/config mismatch')
    for name in ('simulator/docking.py','simulator/observations.py'):
        if digest(ROOT/name)!=hashes[name]:raise ValueError('Static interpretation kernel changed')
    cfg=meta['config']['chemistry'];lipids=meta['chemistry']['lipids'];rungs=dict(lipids['rungs']);heads=sorted(rungs)
    lookup={h:i for i,h in enumerate(heads)};packed=pos[heads+[rungs[h] for h in heads]];n=len(heads)
    links=[(lookup[a],lookup[b],x,y) for a,b,x,y in lipids['links']]
    axes=packed[n:]-packed[:n];lengths=np.linalg.norm(axes,axis=1);u=axes/lengths[:,None];angles=[];strains=[]
    for i,j,a,b in links:
        if a==0:i,j=j,i
        cross=u[i,0]*u[j,1]-u[i,1]*u[j,0]
        angles.append(float(np.arctan2(cross,np.dot(u[i],u[j]))))
        strains.append(float(bound_port_force(packed,np.array([[i,j,1,0]],dtype=np.int64),1.,cfg['short_length'],cfg['dock_energy'],cfg['dock_width'])[1]
            +cfg['dock_energy']*(1-9*np.exp(-8.))))
    parts=list(components(n,{(a,b) for a,b,_,_ in links}));chains=[]
    for comp,order,cycle in parts:
        chosen=[angle for angle,(i,j,_,_) in zip(angles,links) if i in comp and j in comp]
        chains.append(dict(size=len(comp),cycle=bool(cycle),net_axis_turn=float(sum(chosen)),turns=float(sum(chosen)/(2*math.pi))))
    _,preferred,kappa=local_profile(0.,cfg['dock_energy'],cfg['dock_width'],short=cfg['short_length'])
    row=dict(label=task['label'],checkpoint_sha256=digest(path),atoms=len(pos),L=n,links=len(links),
        axial_length=statistics(lengths),signed_link_angle=statistics(angles),preferred_equal_axial_angle=preferred,
        harmonic_angular_sd=math.sqrt(cfg['temperature']/kappa),link_strain_energy=statistics(strains),chains=sorted(chains,key=lambda x:-x['size']))
    return row,dict(pos=pos,heads=heads,rungs=rungs,packed=packed,links=links,angles=angles,cfg=cfg)


def bare_modes(n,epsilon=4.,width=.6,short=.92,axial=.65,damping=.1,mass=1.,step=1e-5):
    """Bare open backbone linearization: excludes bath, walls and free ports."""
    from simulator.physics import force_kernel
    angle=local_profile(0.,epsilon,width,axial,short=short)[1]
    a=np.arange(n)*angle;u=np.column_stack((np.cos(a),np.sin(a)));t=np.column_stack((-u[:,1],u[:,0]));heads=np.zeros((n,2))
    for i in range(n-1):heads[i+1]=heads[i]+(1+short)/4*(t[i]+t[i+1])-axial/2*(u[i+1]-u[i])
    pos=np.vstack((heads,heads+axial*u));links=np.array([(i,i+1,1,0) for i in range(n-1)],dtype=np.int64)
    springs=np.array([(i,n+i,180.,axial) for i in range(n)],dtype=float)
    def force(p):
        f=bound_port_force(p,links,1.,short,epsilon,width)[0]
        f+=force_kernel(p,np.empty((0,2),dtype=np.int64),np.zeros(2*n,dtype=np.int64),np.zeros((1,1)),springs,np.empty((0,5)))
        return f
    hessian=np.empty((pos.size,pos.size))
    for k in range(pos.size):
        plus=pos.copy();minus=pos.copy();plus.flat[k]+=step;minus.flat[k]-=step
        hessian[:,k]=-(force(plus)-force(minus)).ravel()/(2*step)
    values=np.linalg.eigvalsh((hessian+hessian.T)/2);positive=values[values>1e-7]
    if sum(abs(values)<1e-7)!=3 or values[0]<-1e-7:raise ValueError('Unexpected bare backbone modes')
    lam=float(positive[0]);rate=(damping-math.sqrt(max(0.,damping**2-4*lam/mass)))/2
    return dict(units=n,rigid_zero_modes=3,minimum_eigenvalue=float(values[0]),softest_eigenvalue=lam,
        slowest_amplitude_envelope_time=1/rate,force_at_reference=float(np.linalg.norm(force(pos))),
        scope='Small perturbation of ideal open axial/bound backbone only. No nonlinear bath relaxation or closure-time prediction.')


def render(out,rows,raw):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,2,figsize=(11,11),layout='constrained')
    for ax,row,data in zip(axes.flat,rows,raw):
        pos=data['pos'];packed=data['packed'];n=len(packed)//2;occupied=set()
        ax.scatter(pos[:,0],pos[:,1],s=6,color='#9ba6b3',alpha=.18)
        for i,j,a,b in data['links']:
            ax.plot(packed[[i,j],0],packed[[i,j],1],color='#278c9b',lw=1.5);occupied.update(((i,a),(j,b)))
        ax.scatter(packed[:n,0],packed[:n,1],s=14,color='#168a91',zorder=3)
        for i in range(n):
            ax.plot(packed[[i,n+i],0],packed[[i,n+i],1],color='#ca9348',lw=.7,alpha=.7)
            if any((i,a) not in occupied for a in range(2)):
                ax.scatter(*packed[i],s=85,facecolors='none',edgecolors='#db4561',linewidths=1.5,zorder=4)
        ax.set(xlim=(-1,23),ylim=(-1,23),aspect='equal',title=row['label']+' · t=1800')
        ax.set_xlabel('Contours: links; pink rings: units with a free port')
    fig.suptitle('BC1 · final snapshots, no dynamics or geometry correction',fontsize=14)
    fig.savefig(out/'snapshots.png',dpi=140);plt.close(fig)
    cfg=raw[0]['cfg'];theta=np.linspace(-.8,.6,401);energy,pref,kappa=local_profile(theta,cfg['dock_energy'],cfg['dock_width'],short=cfg['short_length'])
    fig,ax=plt.subplots(figsize=(8,4),layout='constrained');minimum=-cfg['dock_energy']*(1-9*np.exp(-8.))
    ax.plot(theta,(energy-minimum)/cfg['temperature'],label='Two fixed-length dimers, translation minimized')
    ax.axvline(pref,color='#168a91',ls='--',label=f'preferred angle {pref:.3f} rad');ax.axvline(0.,color='grey',lw=.7)
    ax.axhline(1.,color='#db4561',ls=':',label='one target thermal-energy unit')
    ax.set(xlabel='Signed relative axis angle (rad)',ylabel='Excess local energy / target T',ylim=(0,8),title='BC1 · analytic local profile, not a whole-chain free energy')
    ax.legend(fontsize=8);fig.savefig(out/'profile.png',dpi=140);plt.close(fig)


def main():
    job=Path(read(ROOT/'research/BATCH_50_CH1_RECIPES.json')['job']);cfg=read(job/'job.json');folder=Path(cfg['campaigns'][0]);manifest=read(folder/'manifest.json')
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    rows=[];raw=[]
    for task in manifest['tasks']:
        row,data=snapshot(folder,task,hashes);rows.append(row);raw.append(data)
    cfg0=raw[0]['cfg'];theta=np.linspace(-math.pi,math.pi,257)
    analytic,preferred,kappa=local_profile(theta,cfg0['dock_energy'],cfg0['dock_width'],short=cfg0['short_length'])
    actual=np.array([bound_port_force(pair_pose(q,short=cfg0['short_length']),np.array([[0,1,1,0]]),1.,cfg0['short_length'],cfg0['dock_energy'],cfg0['dock_width'])[1] for q in theta])
    if not np.allclose(analytic,actual,rtol=0,atol=1e-12):raise ValueError('Derived profile disagrees with engine')
    straight=float(local_profile(0.,cfg0['dock_energy'],cfg0['dock_width'],short=cfg0['short_length'])[0]+cfg0['dock_energy']*(1-9*np.exp(-8.)))
    result=dict(rows=rows,local_profile=dict(preferred_angle=preferred,ideal_turn_count=2*math.pi/abs(preferred),
        bending_curvature=kappa,harmonic_angular_sd=math.sqrt(cfg0['temperature']/kappa),
        straight_excess_over_T=straight/cfg0['temperature'],engine_energy_max_error=float(np.max(np.abs(analytic-actual)))),
        bare_modes=[bare_modes(n,cfg0['dock_energy'],cfg0['dock_width'],cfg0['short_length']) for n in (12,22,34,52)],
        scope='Four selected final snapshots and exact pair reduction with fixed axial length. Not a chain free energy, time history, closure rate or causal attribution.')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');out=ROOT/'outputs/diagnostics'/('BC1_'+stamp);out.mkdir(parents=True)
    recipe=ROOT/'research/diagnostic_recipes'/('BC1_'+stamp);recipe.mkdir(parents=True)
    render(out,rows,raw);write(out/'report.json',result)
    for src in [Path(__file__),ROOT/'simulator/docking.py',ROOT/'simulator/observations.py',ROOT/'simulator/physics.py']:
        dest=recipe/src.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
    provenance=dict(job_sha256=digest(job/'job.json'),manifest_sha256=digest(folder/'manifest.json'),
        source_sha256={p.relative_to(recipe).as_posix():digest(p) for p in recipe.rglob('*.py')},result_sha256=digest(out/'report.json'))
    write(recipe/'recipe.json',provenance)
    previous=read(ROOT/'research/BATCH_51_BC1.json') if (ROOT/'research/BATCH_51_BC1.json').exists() else None
    write(ROOT/'research/BATCH_51_BC1.json',dict(output=str(out),recipe=recipe.relative_to(ROOT).as_posix(),summary=result,previous_attempt=previous,**provenance))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
