"""Reconstruct actual ligation supports from saved events, without rerunning dynamics."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status
from simulator.observations import components
from simulator.checkpoint import unpack


def reconstruct(config,events,final_edges,final_bits):
    c=config['chemistry'];target=c['sequence'];length=len(target)
    n=length+c['free_units']+c['function_units']
    if c['constructible'] or c['initial_assemblies'] or not c['template']:
        raise ValueError('Audit currently requires one prepared G and composite monomers')
    bits=[int(b) for b in target]+[int(c['alphabet'][i%len(c['alphabet'])]) for i in range(c['free_units'])]+[int(c['alphabet'][i%len(c['alphabet'])]) for i in range(c['function_units'])]
    if bits!=list(map(int,final_bits)):raise AssertionError('Unexpected symbol modification')
    edges={(i,i+1) for i in range(length-1)}
    counts=Counter();lengths=Counter();window=Counter();first_short=None
    for time,batch in itertools.groupby(events,key=lambda e:e['time']):
        # All sources refer to the graph at the beginning of this reaction tick.
        lookup={}
        for comp,order,cycle in components(n,edges):
            text=''.join(str(bits[q]) for q in order)
            kind=('initial' if set(range(length))<=comp else
                'exact_descendant' if not cycle and text in (target,target[::-1]) else 'fragment')
            for q in comp:lookup[q]=(comp,kind)
        new=[]
        for event in batch:
            source=tuple(sorted(event['source']));formed=tuple(sorted(event['formed']))
            if source not in edges or formed in edges or formed in new:
                raise AssertionError('Invalid pre-tick source or duplicate product edge')
            comp,kind=lookup[source[0]]
            if source[1] not in comp:raise AssertionError('Disconnected source')
            if sorted(bits[q] for q in source)!=sorted(bits[q] for q in formed):
                raise AssertionError('Symbol mismatch during ligation')
            counts[kind]+=1;lengths[str(len(comp))]+=1
            window[f'{int(time//200)}:{kind}']+=1
            if kind=='fragment' and first_short is None:first_short=float(time)
            new.append(formed)
        edges.update(new)
    if edges!={tuple(sorted(p)) for p in final_edges}:raise AssertionError('Final graph differs from event replay')
    total=sum(counts.values())
    return dict(ligations=total,by_template_kind=dict(counts),by_template_length=dict(lengths),
        fragment_supported_fraction=counts['fragment']/total if total else None,
        first_fragment_supported_ligation=first_short,windows=dict(window),
        scope='Actual source edge and pre-reaction-tick component. A fragment-supported ligation is direct evidence of templating by a fragment, not an inferred mutation rate. No simulation or feedback.')


def audit(folder):
    folder=Path(folder).resolve();manifest=validate(folder);snapshot=status(folder);rows=[]
    expected={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    for task,state in zip(manifest['tasks'],snapshot['tasks']):
        if state['phase']!='complete':raise ValueError('Wait for the full cohort')
        result=json.loads((folder/state['result']).read_text())
        if result['scenario']!=task['scenario'] or result['source_sha256']!=expected:
            raise AssertionError('Result provenance mismatch')
        with np.load(folder/state['checkpoint'],allow_pickle=False) as data:
            meta=json.loads(str(data['metadata']))
            if meta['source_sha256']!=expected or meta['config']!=task['scenario']:
                raise AssertionError('Checkpoint provenance mismatch')
            state_c=meta['chemistry']
            bits=unpack(meta['observer'])['last_bits']
        rows.append(dict(task=task['id'],name=task['label'],seed=task['scenario']['seed'],
            **reconstruct(task['scenario'],result['metrics']['events'],state_c['edges'],bits)))
    out=folder/'lineage_audit.json'
    report=dict(rows=rows,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),manifest_sha256=hashlib.sha256((folder/'manifest.json').read_bytes()).hexdigest())
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    (folder/'lineage_audit_driver.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps([dict(name=r['name'],seed=r['seed'],ligations=r['ligations'],supports=r['by_template_kind'],short_fraction=r['fragment_supported_fraction']) for r in rows]))
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path);a=p.parse_args();audit(a.folder)
