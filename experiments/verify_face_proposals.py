"""Fingerprint matched face ticks, including RNG and gated proposal statistics."""
import hashlib
import json

import numpy as np

from simulator.contact_exchange import exchange_faces
from simulator.docking import update_faces
from simulator.lipid_synthesis import DEFAULTS
from simulator.spatial import Neighborhood


def main():
    digest = hashlib.sha256()
    totals = dict(ticks=0, exchanges=0, broken=0, gate_accepted=0, gate_rejected=0)
    for potential in ('additive', 'competitive'):
        for gate in ('none', 'metropolis'):
            for seed in range(6):
                rng = np.random.default_rng(seed)
                perturb = np.random.default_rng(1000+seed)
                cfg = dict(DEFAULTS, free_port_potential=potential, terminal_exchange=bool(seed%2),
                           contact_update_gate=gate, contact_exchange_gate=gate,
                           dock_rate=150., bond_off_rate=25., contact_exchange_rate=90.,
                           dock_capture=.65, contact_exchange_capture=.8)
                template = np.array([[0., 0.], [1., 0.], [1., .3], [2., 0.], [3., .1]])
                links = [(0, 1, 1, 0)]
                neighbors = Neighborhood()
                for _ in range(30):
                    heads = template+perturb.normal(0., .12, template.shape)
                    tails = heads+[0., -.65]+perturb.normal(0., .03, template.shape)
                    pos = np.vstack((heads, tails))
                    update_stats = {k: dict(proposals=0, accepted=0, rejected=0,
                        positive_delta=0, sum_factor=0., sum_accepted_delta=0.,
                        min_delta=None, max_delta=None) for k in ('formation', 'breaking')}
                    exchange_stats = dict(proposals=0, accepted=0, rejected=0,
                        positive_delta=0, sum_positive_delta=0., sum_factor=0.,
                        min_delta=None, max_delta=None)
                    links, broken = update_faces(pos, links, cfg, rng, neighbors, .01,
                                                 stats=update_stats)
                    links, events = exchange_faces(pos, links, cfg, rng, neighbors, .01,
                                                   stats=exchange_stats)
                    row = dict(links=links, events=events, broken=broken, update=update_stats,
                               exchange=exchange_stats, rng=rng.bit_generator.state)
                    digest.update(json.dumps(row, sort_keys=True).encode())
                    totals['ticks'] += 1
                    totals['exchanges'] += len(events)
                    totals['broken'] += broken
                    gates = (*update_stats.values(), exchange_stats)
                    totals['gate_accepted'] += sum(g['accepted'] for g in gates)
                    totals['gate_rejected'] += sum(g['rejected'] for g in gates)
    print(json.dumps(dict(sha256=digest.hexdigest(), **totals)))


if __name__ == '__main__':
    main()
