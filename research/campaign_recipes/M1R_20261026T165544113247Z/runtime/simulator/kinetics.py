"""Read-only pre-reaction opportunity census; never used by chemical laws.

Exposure is a sampled face-time, NOT the exact integrated hazard: sequential
competition and changes inside a reaction tick can remove eligible candidates.
"""
import math
import numpy as np
from .docking import port_geometry,free_faces
from .spatial import Neighborhood


class KineticProbe:
    def __init__(self,config,state=None,window=25.):
        self.config=config;self.window=window;self.neighbors=Neighborhood()
        self.state=state or dict(version=1,last_time=None,windows={},first={},encountered={},ticks=0)

    def scan(self,c):
        if self.config['model']!='membrane_bath':return {}
        n=c.n;m=c.config['ring_units'];pos=c.pos[:2*n]
        pairs=self.neighbors.pairs(pos[:n],1.+4*c.config['dock_width'],'kinetic_contacts')
        pairs=pairs[(pairs[:,0]<m)&(pairs[:,1]>=m)]
        if not len(pairs):return dict(encounter_pairs=0,capture_faces=0,exchange_faces=0,units=[])
        i,k=pairs.T;free=free_faces(n,c.face_links)
        head,tail,_,_=port_geometry(pos,n,1.,c.short)
        linked={(a,b) for a,b,_,_ in c.face_links}
        unlinked=np.array([(int(a),int(b)) not in linked for a,b in pairs])
        strain=np.maximum(abs(np.linalg.norm(pos[k]-pos[i],axis=1)-1.),
                          abs(np.linalg.norm(pos[n+k]-pos[n+i],axis=1)-c.short))<=c.config['break_extension']
        capture=exchange=0
        for a in (0,1):
            b=1-a
            q=np.sum((head[k,b]-head[i,a])**2,axis=1)+np.sum((tail[k,b]-tail[i,a])**2,axis=1)
            capture+=int(np.count_nonzero(unlinked&free[i,a]&free[k,b]&(q<c.config['dock_capture']**2)))
            # Original occupied face, incoming free face. The reverse direction
            # would replace a contact of a new unit; report it separately later.
            exchange+=int(np.count_nonzero(unlinked&~free[i,a]&free[k,b]&strain&(q<c.config['contact_exchange_capture']**2)))
        return dict(encounter_pairs=len(pairs),capture_faces=capture,exchange_faces=exchange,
                    units=[int(x) for x in np.unique(k)])

    def attach(self,c):
        original=c.react
        def observed(time,dt,neighbors):
            before=self.scan(c)
            edges=set(c.face_links) if self.config['model']=='membrane_bath' else set()
            count=len(getattr(c,'exchange_events',[]))
            result=original(time,dt,neighbors)
            state=self.state;last=state['last_time'];span=0. if last is None else time-last
            key=str(int(math.floor(time/self.window)))
            w=state['windows'].setdefault(key,dict(start=int(key)*self.window,end=(int(key)+1)*self.window,
                observed_time=0.,encounter_pair_time=0.,capture_face_time=0.,exchange_face_time=0.,
                formed_contacts=0,broken_contacts=0,exchanges=0))
            w['observed_time']+=span
            for name in ('encounter_pairs','capture_faces','exchange_faces'):
                target={'encounter_pairs':'encounter_pair_time','capture_faces':'capture_face_time','exchange_faces':'exchange_face_time'}[name]
                w[target]+=span*before.get(name,0)
                if before.get(name,0)>0:state['first'].setdefault(name,float(time))
            for unit in before.get('units',[]):state['encountered'].setdefault(str(unit),float(time))
            if edges or self.config['model']=='membrane_bath':
                after=set(c.face_links);formed=len(after-edges);broken=len(edges-after)
                w['formed_contacts']+=formed;w['broken_contacts']+=broken
                if formed:state['first'].setdefault('formed_contact',float(time))
                m=c.config['ring_units']
                if any(i<m<=j for i,j,a,b in after-edges):state['first'].setdefault('new_old_contact',float(time))
            delta=len(getattr(c,'exchange_events',[]))-count;w['exchanges']+=delta
            if delta:state['first'].setdefault('exchange',float(time))
            state['last_time']=float(time);state['ticks']+=1
            return result
        c.react=observed

    def summary(self,time,metrics):
        first=self.state['first'];passages={}
        for name in ('encounter_pairs','capture_faces','exchange_faces','new_old_contact','exchange'):
            value=first.get(name);passages[name]=dict(time=value if value is not None else time,event=value is not None,
                measured=self.config['model']=='membrane_bath')
        history=metrics.get('history',[])
        insertion=next((float(h['time']) for h in history if h.get('inserted_now')),None)
        passages['closed_insertion']=dict(time=time if insertion is None else insertion,event=insertion is not None,
            measured=self.config['model']=='membrane_bath')
        windows=list(self.state['windows'].values())
        return dict(version=1,scope='Membrane pre-reaction original/new pair census; other hooks have no eligibility diagnostic',
            resolution='Every reaction tick; right-endpoint face-time approximation, no exact hazard or independence claim',
            sampled_until=time,first_passages=passages,encountered_new_units=len(self.state['encountered']),
            opportunity_totals={k:sum(w[k] for w in windows) for k in ('encounter_pair_time','capture_face_time','exchange_face_time','exchanges')},
            windows=windows,state=self.state,
            limitations='No-event passages are right-censored; sequential competition and reverse new-unit exchanges are not included in eligibility exposure; net contact changes can miss within-tick break/reform')
