"""Read-only boundary diagnostics at observer samples, never a repair controller.

Fragment topology and nearby endpoints are reported without inventing a contour
or classifying probes during unknown periods. Existing observer metrics stay intact.
"""
import numpy as np
from .observations import components,area
from .membrane_bath import polygon_simple


class BoundaryAudit:
    def __init__(self,config,primary,state=None):
        if config['model']!='membrane_bath':raise ValueError('Boundary audit requires membrane_bath')
        self.config=config;self.primary=primary
        self.n=config['chemistry']['units'];self.m=config['chemistry']['ring_units']
        self.state=state if state is not None else dict(version=1,last_time=None,last_kind=None,
            state_time={},sample_counts={},episodes=[],history=[],openings=[],previous_contacts=[])

    def __call__(self,time,pos,edges,links,exchange_events=None):
        sample=self.primary.history[-1]
        if sample['time']!=time:raise ValueError('Primary observer must precede boundary audit')
        parent=[]
        for comp,order,cycle in components(self.n,edges[0]):
            original=sum(i<self.m for i in comp)
            if original:parent.append((original,len(comp),order,cycle,comp))
        largest=max(parent,key=lambda c:(c[0],c[1]))
        original,_,order,cycle,comp=largest
        points=pos[order];endpoint_gap=float(np.linalg.norm(points[-1]-points[0])) if len(order)>1 and not cycle else None
        if sample['parent_closed']:kind='closed'
        elif sample['envelope_valid']:kind='open_classifiable'
        elif original<.8*self.m:kind='fragmented_parent'
        elif endpoint_gap is not None and endpoint_gap>2.5:kind='long_endpoint_gap'
        elif area(points)<.5*self.primary.initial_area:kind='low_area'
        elif not polygon_simple(points):kind='self_intersection'
        else:kind='other_unknown'
        degree=np.zeros(self.n,dtype=np.int64)
        for i,j in edges[0]:degree[i]+=1;degree[j]+=1
        endpoints=[i for _,_,_,_,members in parent for i in members if degree[i]==1]
        nearest_min=nearest_max=None
        if len(endpoints)>1:
            p=pos[endpoints];d=np.linalg.norm(p[:,None]-p[None,:],axis=2)
            np.fill_diagonal(d,np.inf);nearest=d.min(axis=1)
            nearest_min=float(nearest.min());nearest_max=float(nearest.max())
        st=self.state;last=st['last_time'];previous=st['last_kind']
        if last is not None:
            if time<last:raise ValueError('Boundary sample time moved backwards')
            st['state_time'][previous]=st['state_time'].get(previous,0.)+time-last
        st['sample_counts'][kind]=st['sample_counts'].get(kind,0)+1
        if previous!=kind:
            st['episodes'].append(dict(kind=kind,first_sample=float(time),last_sample=float(time),samples=1))
        else:
            st['episodes'][-1]['last_sample']=float(time);st['episodes'][-1]['samples']+=1
        if previous=='closed' and kind!='closed':
            last_exchange=exchange_events[-1]['time'] if exchange_events else None
            st['openings'].append(dict(time=float(time),kind=kind,
                preceding_exchange_age=None if last_exchange is None else float(time-last_exchange)))
        contacts=set(edges[0]);old={tuple(e) for e in st['previous_contacts']}
        st['history'].append(dict(time=float(time),kind=kind,largest_original_fraction=original/self.m,
            parent_components=len(parent),parent_endpoints=len(endpoints),largest_endpoint_gap=endpoint_gap,
            nearest_endpoint_min=nearest_min,nearest_endpoint_max=nearest_max,
            net_formed_since_sample=len(contacts-old) if last is not None else 0,
            net_broken_since_sample=len(old-contacts) if last is not None else 0))
        st['previous_contacts']=[list(e) for e in sorted(contacts)]
        st['last_time']=float(time);st['last_kind']=kind

    def summary(self):
        st=self.state;total=sum(st['state_time'].values());longest={}
        for e in st['episodes']:
            longest[e['kind']]=max(longest.get(e['kind'],0.),e['last_sample']-e['first_sample'])
        unknown={k:v for k,v in st['sample_counts'].items() if k not in ('closed','open_classifiable')}
        ages=[e['preceding_exchange_age'] for e in st['openings'] if e['preceding_exchange_age'] is not None]
        return dict(version=1,samples=len(st['history']),sampled_until=st['last_time'],state_time=st['state_time'],
            state_time_fraction={k:v/total for k,v in st['state_time'].items()} if total else {},
            sample_counts=st['sample_counts'],unknown_reason_samples=unknown,
            longest_observed_span_by_state=longest,closed_to_nonclosed_samples=len(st['openings']),
            openings_with_preceding_exchange_within={str(t):sum(age<=t for age in ages) for t in (1.,5.,25.)},
            limitations='Sampled graph/envelope diagnosis only; endpoint proximity is not a seal. State-time uses previous sample; transitions interval-censored. No probe classification during unknown periods. Exchange proximity is not causality.',
            state=st)
