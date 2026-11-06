"""Opt-in local bond loss; the journal is output, never a reaction input.

Kinetic helper, not a detailed-balance thermodynamic model. No atom is removed
or moved. Only direct bond neighbors and occupied ports affect eligibility.
"""
import numpy as np
from .reference import degree


def paired_edge(c,a,b):
    """Four directly connected composites; no chain or sequence identity."""
    x,y=int(c.pairing[a]),int(c.pairing[b])
    return (x>=0 and y>=0 and c.pairing[x]==a and c.pairing[y]==b and
        tuple(sorted((x,y))) in c.edges)


class BondTurnover:
    def __init__(self, settings):
        self.settings = settings
        self.events = []

    def react(self, c, time, dt):
        rates = self.settings
        cat = c.assembly.catalyst
        occupied = c.pairing >= 0
        if cat is not None:
            occupied = occupied | (cat.site_bound >= 0)
        for a, b in sorted(c.edges):
            rate = rates['backbone_g' if c.families[a] == 0 else 'backbone_f']
            protected=paired_edge(c,a,b) if rates.get('protection_scope','occupied')=='paired_edge' else occupied[a] or occupied[b]
            if protected:
                rate *= rates['protection']
            if rate > 0 and c.rng.random() < -np.expm1(-rate * dt * 5):
                c.edges.remove((a, b))
                self.events.append(dict(kind='backbone_break',time=float(time),a=int(a),b=int(b)))
        deg = degree(c.n, c.edges)
        for s in np.flatnonzero((deg == 0) & ~occupied & (c.rungs[:,1] >= 0)):
            rate = rates['rung_g' if c.families[s] == 0 else 'rung_f']
            if rate > 0 and c.rng.random() < -np.expm1(-rate * dt * 5):
                r = int(c.rungs[s,1])
                c.rungs[s,1] = -1
                c.bits[s] = -1
                c.capacities[s] = 2
                self.events.append(dict(kind='rung_break',time=float(time),support=int(s),recognizer=r))
        if cat is not None:
            cat.refresh(c)

    def formed(self, c, time, assembly_start, ligations):
        for e in c.assembly.events[assembly_start:]:
            self.events.append(dict(e,kind='rung_form'))
        for e in ligations:
            a,b=e['formed']
            self.events.append(dict(kind='backbone_form',time=float(time),a=int(a),b=int(b),
                recognizers={str(int(q)):int(c.rungs[q,1]) for q in (a,b)}))
