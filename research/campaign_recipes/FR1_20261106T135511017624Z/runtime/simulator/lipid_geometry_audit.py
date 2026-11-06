"""Opt-in passive snapshots of L geometry, never exposed to chemical hooks."""
import math
import numpy as np
from .observations import components,area
from .membrane_bath import polygon_simple
from .docking import port_geometry,free_faces


def settings(raw):
    if not isinstance(raw,dict) or set(raw)-{'interval','min_units','min_area','max_samples'}:raise ValueError('Invalid lipid geometry observer settings')
    cfg=dict(interval=5.,min_units=26,min_area=.25*math.pi*8.325**2,max_samples=2001);cfg.update(raw)
    if type(cfg['interval']) not in (int,float) or not math.isfinite(cfg['interval']) or cfg['interval']<=0:raise ValueError('Invalid geometry interval')
    if type(cfg['min_area']) not in (int,float) or not math.isfinite(cfg['min_area']) or cfg['min_area']<0:raise ValueError('Invalid geometry area')
    if type(cfg['min_units']) is not int or cfg['min_units']<3 or type(cfg['max_samples']) is not int or not 2<=cfg['max_samples']<=10000:raise ValueError('Invalid geometry count budget')
    return cfg


class LipidGeometryAudit:
    def __init__(self,config,raw,state=None):
        self.config=config;self.settings=settings(raw)
        if config['model'] not in ('lipid_synthesis','mixed_synthesis'):raise ValueError('Geometry observer requires explicit L bonds')
        self.state=state if state is not None else dict(history=[],next_sample=0.,first_macro_sample=None,first_capture=None,dropped=0)

    def __call__(self,time,c,events):
        if time<self.state['next_sample']-1e-8 and time<self.config['duration']-1e-8:return
        if self.state['history'] and abs(self.state['history'][-1]['time']-time)<1e-8:return
        heads,ids,links=c.lipids.layout();n=len(heads);packed=c.pos[ids]
        h,t,_,_=port_geometry(packed,n,1.,c.config['short_length']);free=free_faces(n,links)
        parts=list(components(n,{(i,j) for i,j,_,_ in links}));cycles=[];nearest=None;eligible=0
        for comp,order,cycle in parts:
            if cycle and len(order)==len(comp):
                points=c.pos[[heads[i] for i in order]]
                if polygon_simple(points):cycles.append(dict(units=len(comp),area=float(area(points))))
            ends=[(i,a) for i in comp for a in range(2) if free[i,a]]
            for i,a in ends:
                for j,b in ends:
                    if i>=j or a==b:continue
                    q=float(np.sum((h[j,b]-h[i,a])**2)+np.sum((t[j,b]-t[i,a])**2))
                    nearest=q if nearest is None else min(nearest,q)
                    eligible+=int(q<c.config['dock_capture']**2)
        macro=any(q['units']>=self.settings['min_units'] and q['area']>=self.settings['min_area'] for q in cycles)
        row=dict(time=float(time),largest=max((len(q[0]) for q in parts),default=0),components=len(parts),simple_cycles=cycles,
            macro=bool(macro),self_capture_faces=eligible,min_self_port_mismatch=None if nearest is None else nearest**.5)
        if macro and self.state['first_macro_sample'] is None:
            self.state['first_macro_sample']=float(time)
            # One bounded coordinate capture, only L atoms at the first witness.
            self.state['first_capture']=dict(time=float(time),atom_ids=ids.tolist(),positions=packed.tolist(),links=links)
        if len(self.state['history'])<self.settings['max_samples']:self.state['history'].append(row)
        else:self.state['dropped']+=1
        interval=self.settings['interval'];self.state['next_sample']=(int((time+1e-8)/interval)+1)*interval

    def summary(self,horizon):
        first=self.state['first_macro_sample']
        return dict(settings=self.settings,**self.state,
            first_sampled_macro=dict(time=float(horizon) if first is None else first,event=first is not None),
            scope='Passive sampled geometry and endpoint opportunities, not exact reaction hazard or continuous first passage. '
                  'No sampled witness is right-censored for this sampled observable only; transient subinterval cycles may be missed.')
