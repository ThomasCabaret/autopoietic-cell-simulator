"""Bounded passive captures of actual double-paired F ligation motifs.

Observation only. Whole-graph searching chooses a diagnostic target; no output
of this module is supplied to forces, reactions, neighbors or the reaction RNG.
"""
import math
import numpy as np
from .reference import normals,local_port_free

DEFAULTS=dict(window=1.,interval=.02,radius=1.5,max_captures=2,max_particles=24,max_records=128)


def settings(raw):
    if not isinstance(raw,dict) or set(raw)-set(DEFAULTS):raise ValueError('Unknown ligation loupe setting')
    cfg={**DEFAULTS,**raw}
    for k in ('window','interval','radius'):
        if type(cfg[k]) not in (int,float) or not math.isfinite(cfg[k]) or cfg[k]<=0:
            raise ValueError('Loupe lengths/cadences must be finite and positive')
    for k,low,high in (('max_captures',1,8),('max_particles',8,64),('max_records',1,1024)):
        if type(cfg[k]) is not int or not low<=cfg[k]<=high:raise ValueError('Invalid bounded loupe budget')
    return cfg


class LigationLoupe:
    def __init__(self,config,state=None):
        cfg=settings(config)
        if state is not None and state['config']!=cfg:raise ValueError('Loupe configuration changed on resume')
        self.state=state if state is not None else dict(config=cfg,captures=[],seen=[],active=None,records=0,
            last_time=None,last_counts={},exposure={},first={})

    def before(self,c,time):
        state=self.state;cfg=state['config'];index=state['active']
        last=state['last_time']
        if last is not None:
            for key,value in state['last_counts'].items():
                state['exposure'][key]=state['exposure'].get(key,0.)+(time-last)*value
        counts=dict(single_F_edges=0,double_F_unlinked=0)
        for i,j in sorted(c.edges):
            if c.families[i]!=0 or c.families[j]!=0:continue
            a,b=int(c.pairing[i]),int(c.pairing[j])
            flags=[q>=0 and c.families[q]==1 for q in (a,b)]
            if sum(flags)==1:counts['single_F_edges']+=1
            if not all(flags) or tuple(sorted((a,b))) in c.edges:continue
            counts['double_F_unlinked']+=1
            reason=self.geometry(c,[int(i),int(j),a,b])['reason'];key='double_F_'+reason
            counts[key]=counts.get(key,0)+1
        for key,value in counts.items():
            if value>0:state['first'].setdefault(key,float(time))
        state.update(last_time=float(time),last_counts=counts)
        if index is not None:
            capture=state['captures'][index]
            if time>capture['start']+cfg['window']+1e-9:
                capture.update(end=float(time),end_reason='window');state['active']=None
        if state['records']>=cfg['max_records']:
            if state['active'] is not None:
                state['captures'][state['active']].update(end=float(time),end_reason='record_budget');state['active']=None
            return
        if state['active'] is None and len(state['captures'])<cfg['max_captures']:
            for i,j in sorted(c.edges):
                if c.families[i]!=0 or c.families[j]!=0:continue
                a,b=int(c.pairing[i]),int(c.pairing[j])
                if a<0 or b<0 or a==b or c.families[a]!=1 or c.families[b]!=1:continue
                key=[int(i),int(j),a,b]
                if tuple(sorted((a,b))) in c.edges or key in state['seen']:continue
                state['seen'].append(key);state['active']=len(state['captures'])
                state['captures'].append(dict(target=key,start=float(time),frames=[],outcomes=[],end=None,end_reason=None,last_pairing=[a,b]))
                break
        if state['active'] is None:return
        capture=state['captures'][state['active']]
        if capture['frames'] and time-capture['frames'][-1]['time']<cfg['interval']-1e-9:return
        capture['frames'].append(self.sample(c,time,capture['target']));state['records']+=1

    @staticmethod
    def geometry(c,target):
        i,j,a,b=target;active=c.rungs[:,1]>=0
        if not all(active[q] for q in target):return dict(reason='inactive',eligible=False)
        nrm=normals(c.pos,c.rungs[np.array(target)])
        d=c.pos[b]-c.pos[a];distance=float(np.linalg.norm(d))
        dot=float(nrm[2]@nrm[3]);skew=[float(abs(nrm[q]@d)/max(distance,1e-12)) for q in (2,3)]
        current=list(map(int,c.pairing[[i,j]]));reason='eligible'
        if current!=[a,b]:reason='partners_changed'
        elif tuple(sorted((a,b))) in c.edges:reason='already_linked'
        elif not c.config['ligation']:reason='disabled'
        elif c.families[a]!=c.families[b]:reason='family'
        elif not .72<distance<1.28:reason='distance'
        elif dot<.5:reason='orientation'
        elif max(skew)>.5:reason='skew'
        elif not local_port_free(a,b,c.pos,c.edges,c.capacities[a]) or not local_port_free(b,a,c.pos,c.edges,c.capacities[b]):reason='ports'
        return dict(reason=reason,eligible=reason=='eligible',pairing=current,distance=distance,
            product_normal_dot=dot,template_normal_dot=float(nrm[0]@nrm[1]),skew=skew,
            recognition_distances=[float(np.linalg.norm(c.pos[c.rungs[q,1]]-c.pos[c.rungs[p,1]]))
                for p,q in ((i,a),(j,b))])

    def sample(self,c,time,target):
        cfg=self.state['config'];core=sorted(set(target+[int(c.rungs[q,1]) for q in target if c.rungs[q,1]>=0]))
        dist=np.linalg.norm(c.pos[:,None,:]-c.pos[np.array(core)][None,:,:],axis=2).min(axis=1)
        near=[int(q) for q in np.argsort(dist,kind='stable') if dist[q]<=cfg['radius'] and q not in core]
        ids=core+near[:max(0,cfg['max_particles']-len(core))];chosen=set(ids)
        bonds={};boundary=0
        for kind,pairs in c.bonds().items():
            bonds[kind]=[[int(a),int(b)] for a,b in pairs if a in chosen and b in chosen]
            boundary+=sum((a in chosen)!=(b in chosen) for a,b in pairs)
        return dict(time=float(time),ids=ids,positions=np.round(c.pos[ids],7).tolist(),bonds=bonds,
            omitted_near=max(0,len(core)+len(near)-len(ids)),boundary_bonds=int(boundary),
            geometry=self.geometry(c,target))

    def after(self,c,time,events):
        state=self.state
        if state['active'] is None:return
        capture=state['captures'][state['active']];i,j,a,b=capture['target']
        formed=[e for e in events if 'formed' in e and tuple(sorted(e['formed']))==tuple(sorted((a,b)))]
        if formed and state['records']<state['config']['max_records']:
            capture['outcomes'].append(dict(time=float(time),kind='formed',events=formed))
            state['records']+=1
        current=list(map(int,c.pairing[[i,j]]))
        if current!=capture['last_pairing'] and state['records']<state['config']['max_records']:
            capture['outcomes'].append(dict(time=float(time),kind='pairing_changed',pairing=current));state['records']+=1
        capture['last_pairing']=current

    def summary(self,time):
        state=self.state
        return dict(records=state['records'],exposure=state['exposure'],first=state['first'],captures=[dict(target=x['target'],start=x['start'],end=x['end'],
            end_reason=x['end_reason'] or 'right_censored_at_horizon',frames=len(x['frames']),outcomes=x['outcomes']) for x in state['captures']],
            scope='First bounded distinct double-paired F motifs, selected diagnostics not frequency estimates. '
                'Frame geometry is pre-reaction; outcomes are actual subsequent reactions. Near particles can be truncated; '
                'outside forces not recorded. Exposure is left-held pre-reaction edge-time, not exact hazard. '
                'No observer feedback; no capture means no sampled pre-reaction target by the horizon.',horizon=float(time))
