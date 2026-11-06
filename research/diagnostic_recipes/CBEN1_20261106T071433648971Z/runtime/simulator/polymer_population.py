"""Passive census of every polymer, including failed products and free stock.

Only the observer reads sequences, components and initial identities. No RNG,
reaction cache or dynamic parameter is accessed or modified here.
"""
from collections import Counter
import numpy as np
from scipy.spatial import cKDTree
from .observations import components


def canonical(sequence, cycle=False):
    if not cycle:
        return min(sequence, sequence[::-1])
    return min(s[i:]+s[:i] for s in (sequence, sequence[::-1]) for i in range(len(s)))


class PopulationAudit:
    def __init__(self, config, state=None, interval=10.):
        if config['model'] != 'copy':
            raise ValueError('Population audit currently requires the copy model')
        c = config['chemistry']
        if c.get('constructible') or c.get('food_pairs') or c.get('initial_assemblies'):
            raise ValueError('Population audit requires isolated prepared monomers and one initial strand')
        if interval <= 0:
            raise ValueError('Invalid population interval')
        self.target = c['sequence']
        self.interval = float(interval)
        self.duration = config['duration']
        self.box = c['box']
        self.state = state if state is not None else dict(version=1, snapshots=[],
            next_sample=0., last_time=None, ligations=0, symbol_mismatches=0,
            first_new_exact_G=None, first_new_exact_F=None)

    def __call__(self, time, pos, edges, pairing, bits, events, families=None,
                 food=None, copy_pairing=None):
        s = self.state
        for event in events:
            if 'source' not in event:
                continue
            s['ligations'] += 1
            source = sorted(int(bits[i]) for i in event['source'])
            product = sorted(int(bits[i]) for i in event['formed'])
            s['symbol_mismatches'] += source != product
        if time < s['next_sample']-1e-8 and time < self.duration-1e-8:
            return
        if s['last_time'] is not None and abs(time-s['last_time']) < 1e-8:
            return
        n = len(bits)
        if families is None:
            families = np.zeros(n, dtype=int)
        lengths = {f: Counter() for f in ('G', 'F')}
        stocks = {f: Counter() for f in ('G', 'F')}
        categories = {f: Counter() for f in ('G', 'F')}
        types = {}
        membership = np.full(n, -1, dtype=int)
        initial = set(range(len(self.target)))
        original_component = None
        comps = components(n, edges)
        for component_id, (comp, order, cycle) in enumerate(comps):
            ids = sorted(comp)
            membership[ids] = component_id
            if initial & comp:
                original_component = comp
            family = 'F' if families[ids[0]] else 'G'
            if any(families[q] != families[ids[0]] for q in ids):
                raise AssertionError('Mixed polymer family')
            if len(order) != len(comp):
                raise AssertionError('Nonlinear graph cannot be counted as a sequence')
            text = ''.join(str(int(bits[q])) for q in order)
            text = canonical(text, cycle)
            length = len(comp)
            topology = 'cycle' if cycle else 'open'
            key = (family, topology, text)
            row = types.setdefault(key, dict(family=family, topology=topology,
                sequence=text, length=length, count=0, new_count=0,
                detached_count=0, new_detached_count=0))
            new = not bool(initial & comp)
            detached = all(pairing[q] < 0 and (copy_pairing is None or copy_pairing[q] < 0) for q in ids)
            row['count'] += 1
            row['new_count'] += int(new)
            row['detached_count'] += int(detached)
            row['new_detached_count'] += int(new and detached)
            lengths[family][str(length)] += 1
            if length == 1:
                category = 'monomer'
                stocks[family][text] += 1
            elif cycle:
                category = 'cycle'
            elif text == canonical(self.target):
                category = 'exact'
                if new and detached and s['first_new_exact_'+family] is None:
                    s['first_new_exact_'+family] = float(time)
            elif length < len(self.target):
                category = 'short_matching' if (text in self.target or text[::-1] in self.target) else 'short_other'
            elif length == len(self.target):
                category = 'same_length_other'
            else:
                category = 'longer'
            categories[family][category+'_chains'] += 1
            categories[family][category+'_units'] += length
        rows = [types[k] for k in sorted(types)]
        if sum(r['length']*r['count'] for r in rows) != n:
            raise AssertionError('Population mass balance failed')
        # Independent spatial index; no engine neighbor cache is consulted.
        close = cKDTree(pos[:n]).query_pairs(.7, output_type='ndarray')
        cross = close[membership[close[:, 0]] != membership[close[:, 1]]]
        crowded = len(np.unique(cross)) if len(cross) else 0
        degree = Counter(q for edge in edges for q in edge)
        original_edges = all(tuple((i, i+1)) in edges for i in range(len(self.target)-1))
        record = dict(time=float(time), types=rows,
            length_distribution={f: dict(lengths[f]) for f in lengths},
            free_monomers_by_symbol={f: dict(stocks[f]) for f in stocks},
            unpaired_free_monomers={f: int(sum(int(families[q]) == i and degree[q] == 0 and pairing[q] < 0
                and (copy_pairing is None or copy_pairing[q] < 0) for q in range(n))
                ) for f, i in (('G', 0), ('F', 1))},
            categories={f: dict(categories[f]) for f in categories},
            original_backbone_present=bool(original_edges),
            original_still_separate=original_component == initial,
            original_component_length=len(original_component) if original_component is not None else 0,
            accounted_units=n, ligations=s['ligations'],
            symbol_mismatches=s['symbol_mismatches'],
            support_density=n/float(np.prod(self.box)),
            intercomponent_core_contacts=len(cross),
            fraction_supports_in_core_contact=crowded/n)
        s['snapshots'].append(record)
        s['last_time'] = float(time)
        s['next_sample'] = (int((time+1e-8)/self.interval)+1)*self.interval

    def latest(self):
        if not self.state['snapshots']:
            return None
        row = self.state['snapshots'][-1]
        return {k: row[k] for k in ('time', 'categories', 'free_monomers_by_symbol',
            'original_backbone_present', 'original_still_separate',
            'fraction_supports_in_core_contact', 'ligations')}

    def summary(self):
        return dict(target=self.target, interval=self.interval,
            convention='Unoriented sequences canonicalized by reversal; cycles also by rotation. Counts and first passages are sampled, not ever-made counts or exact reaction times.',
            limitations='Prepared composite monomers, finite reflecting box and fixed external release cycle. A close-core contact is an occupancy diagnostic, not proof of a transport bottleneck. No molecular point-mutation channel.',
            first_passages={f: dict(time=self.state['first_new_exact_'+f] if self.state['first_new_exact_'+f] is not None else self.state['last_time'],
                event=self.state['first_new_exact_'+f] is not None) for f in ('G', 'F')},
            state=self.state)
