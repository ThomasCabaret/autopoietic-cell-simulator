"""Post-hoc material routes from existing irreversible P/R event evidence.

No extra simulation recording. Reject turnover, which requires its own lifecycle
observer. Never infer useful flux merely from a high catalytic-event total.
"""
from collections import Counter


def routes(result):
    cfg=result['scenario'];g=cfg['chemistry'].get('genetics',cfg['chemistry'])
    if 'bond_turnover' in g:raise ValueError('Irreversible route census cannot certify recycled material')
    m=result['metrics'].get('genetics',result['metrics'])
    assembly=m['assembly_state'];events=assembly['catalytic_events']
    rungs=assembly['rungs'];bits=assembly['atom_bits'];n=len(rungs)
    families=[g['seed_family']]*len(g['sequence'])+[0]*g['free_units']+[1]*g['function_units']
    incorporated={int(k):v for k,v in m['assembly_incorporation_times'].items()}
    seen=set();made=Counter();used=Counter();tools=Counter();first={};products=[]
    for e in events:
        s=int(e['support']);r=int(e['recognizer'])
        if s in seen:raise ValueError('Duplicate support birth in irreversible evidence')
        seen.add(s)
        if not n<=r<2*n or int(bits[r-n])!=e['symbol'] or rungs[s][1]!=r:
            raise ValueError('Product atom identity/symbol mismatch')
        kind=e['chain_kind'] if e['chain_kind'] is not None else ('unattributed' if e['catalyzed'] else 'background')
        if kind in ('prepared','expressed'):
            if not e['catalyzed'] or not e['chain'] or not set(e['catalytic_support'])<=set(e['chain']):
                raise ValueError('Attribution not supported by real catalytic sites')
            tools[(kind,tuple(e['chain']))]+=1
        product=('G' if families[s]==0 else 'F')+str(e['symbol'])
        made[(kind,product)]+=1;use=incorporated.get(s)
        if use is not None:
            if use<e['time']:raise ValueError('Incorporation precedes product birth')
            used[(kind,product)]+=1
        for key,time in ((kind+'_formation',e['time']),(kind+'_incorporation',use)):
            if time is not None:first[key]=min(first.get(key,time),time)
        products.append(dict(support=s,recognizer=r,origin=kind,product=product,birth=e['time'],incorporation=use))
    def table(counter):
        return {origin:{p:int(counter[(origin,p)]) for p in ('G0','G1','F0','F1','G2','F2')}
                for origin in ('prepared','expressed','unattributed','background')}
    return dict(formed=table(made),incorporated=table(used),first=first,
        max_operations={k:max((v for (kind,_),v in tools.items() if kind==k),default=0) for k in ('prepared','expressed')},
        products=products,scope='Actual atom products and incorporation into any backbone; not full new functional chains or homeostasis. '
            'Origin is the existing passive observer attribution established before operation; no turnover supported.')


def inventory(config):
    from simulator.initial import groups
    g=config['chemistry'].get('genetics',config['chemistry']);seq=g['sequence'];alphabet=g['alphabet']
    symbols=list(map(int,seq))+[int(alphabet[i%len(alphabet)]) for i in range(g['free_units'])]+[
        int(alphabet[i%len(alphabet)]) for i in range(g['function_units'])]
    for group in groups(g):
        for q,b in zip(group['units'],group['sequence']):symbols[q]=int(b)
    families=[g['seed_family']]*len(seq)+[0]*g['free_units']+[1]*g['function_units']
    count=Counter(('G' if f==0 else 'F')+str(b) for f,b in zip(families,symbols))
    active=set(range(len(seq)))|{q for group in groups(g) for q in group['units']}
    return dict(beads=2*len(symbols),symbols=dict(count),initial_composites=len(active))
