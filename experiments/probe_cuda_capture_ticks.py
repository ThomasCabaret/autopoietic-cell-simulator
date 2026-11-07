"""Run the capture-only slice of FR1 without host arbitration between ticks."""
import argparse
import copy
import json
import math
from pathlib import Path
from statistics import median
from time import perf_counter

import numpy as np

from simulator.engine import Simulation
from simulator.resident_fields import CaptureField
from simulator.resident_motion import ResidentLangevinMotion, _grid


ROOT = Path(__file__).resolve().parents[1]


class CaptureTickMotion(ResidentLangevinMotion):
    """Experimental scheduler adapter. Other chemical reactions are frozen."""

    def __init__(self, sim):
        super().__init__(sim.chemistry, np.random.default_rng(), sim.config['mechanics'],
                         'copy', sim.reaction_every)
        # Simulation has already drawn the initial velocities.
        self.velocities = sim.motion.velocities
        self.block_steps = 5*sim.reaction_every
        self.cadence = sim.reaction_every
        self.seed = np.uint64(sim.config['seed'])

    def _upload(self, c, dt):
        super()._upload(c, dt)
        cap = c.assembly.catalyst
        occupancy = np.full(len(c.pos), -1, dtype=np.int64)
        sites = np.flatnonzero(cap.site_bound >= 0)
        site_atoms = c.rungs[sites, 1]
        ligand_atoms = cap.site_bound[sites]
        occupancy[site_atoms] = ligand_atoms
        occupancy[ligand_atoms] = site_atoms
        self.partner = self.cp.asarray(occupancy)
        self.claims = self.cp.empty(len(occupancy), dtype=self.cp.uint64)
        self.tick = self.cp.zeros(1, dtype=self.cp.uint64)
        self.counts = self.cp.zeros(2, dtype=self.cp.uint64)
        self.capture = CaptureField(self.cp, c, cap, self.partner)
        sites, ligands, _ = self.capture.descriptors
        if c.config.get('capture_cooperativity') or np.any((sites[:, 0] >= 0) & (ligands[:, 0] >= 0)):
            raise ValueError('Capture probe requires independent, disjoint sites and ligands')
        cfg = c.config
        self.params = tuple(map(np.float64, (
            cfg['food_binding_radius'], dt*self.cadence,
            cfg['food_binding_rate'], cfg['food_unbinding_rate'])))

    def _update_topology(self, c):
        if self.topology is None:
            super()._update_topology(c)

    def _react_device(self):
        release, propose, commit = self.kernels[13:]
        sites, ligands, activity = self.capture.buffers
        radius, interval, on_rate, off_rate = self.params
        blocks = _grid(self.count)
        release(blocks, (128,), (self.count, sites, activity, self.partner, self.claims,
                                  self.tick, self.seed, interval, off_rate, self.counts))
        propose(blocks, (128,), (
            self.device[0], self.count, sites, ligands, activity, self.partner,
            self.claims, self.tick, self.seed, radius, interval, on_rate,
            self.heads, self.next, self.width, self.nx, self.ny))
        commit(blocks, (128,), (self.count, self.claims, self.partner, self.tick, self.counts))

    def _launch_steps(self, steps):
        if steps % self.cadence:
            raise ValueError('The capture probe advances in whole reaction intervals')
        super()._launch_steps(steps, self._react_device, self.cadence)


def capture_scenario(particles, seed=0):
    path = ROOT/'research/campaign_recipes/FR1_20261106T135511017624Z/manifest.json'
    cfg = json.loads(path.read_text(encoding='utf-8'))['tasks'][0]['scenario']
    cfg['seed'] = seed
    c = cfg['chemistry']
    base = len(c['sequence'])+c['free_units']+c['function_units']
    area = particles/(2*base)
    c['box'] = [x*math.sqrt(area) for x in c['box']]
    c['free_units'] = round(c['free_units']*area)
    c['function_units'] = particles//2-len(c['sequence'])-c['free_units']
    c['initial_assemblies'] *= max(1, round(area))
    return cfg


def capture_sim(config, cuda, hybrid=False):
    cfg = copy.deepcopy(config)
    cfg['engine']['force_backend'] = 'cuda-resident' if cuda or hybrid else 'numba'
    sim = Simulation(cfg)
    c = sim.chemistry
    cap = c.assembly.catalyst
    # Keep the prepared scaffold and pairing; exclude all other transitions.
    c._finish(sim.dt, sim.neighbors, [])
    scaffold = c.springs.copy()
    if cuda:
        def quiet(*_):
            return []
        c.react = sim.resident_react = quiet
        sim.motion = CaptureTickMotion(sim)
        c.motion_state = sim.motion
    else:
        def capture_only(time, dt, neighbors):
            cap.react(c, dt, neighbors)
            springs = np.asarray(cap.springs(c), dtype=float).reshape(-1, 4)
            c.springs = np.concatenate((scaffold, springs))
            return []
        c.react = capture_only
    # Both backends make their first capture decision after the first interval.
    sim.prepared = True
    return sim


def occupancy(sim, cuda):
    c = sim.chemistry
    cap = c.assembly.catalyst
    if cuda:
        partner = sim.motion.partner.get()
        live = np.flatnonzero(partner >= 0)
        assert np.all(partner[live] < len(partner))
        np.testing.assert_array_equal(partner[partner[live]], live)
        sites = live[cap.owners[live] >= 0]
        assert len(live) == 2*len(sites)
        np.testing.assert_array_equal(cap.categories[partner[sites]], c.bits[cap.owners[sites]])
        return len(sites)
    return int(np.count_nonzero(cap.site_bound >= 0))


def seed_contacts(c):
    """Place compatible ligands near pre-existing sites, for a positive control."""
    cap = c.assembly.catalyst
    for bit in (0, 1):
        sites = np.flatnonzero((cap.owners >= 0) & (c.bits[np.maximum(cap.owners, 0)] == bit))
        ligands = np.flatnonzero(cap.categories == bit)
        count = min(len(sites), len(ligands))
        c.pos[ligands[:count]] = c.pos[sites[:count]]+[.12, .07]


def measure(particles, steps, seed, cuda, active_control, hybrid=False):
    config = capture_scenario(particles, seed)
    if active_control:
        config['chemistry']['food_activation'] = False
    sim = capture_sim(config, cuda, hybrid)
    if active_control:
        seed_contacts(sim.chemistry)
    sim.advance(250)
    samples = []
    counts = []
    for _ in range(3):
        start = perf_counter()
        sim.advance(steps)
        samples.append(perf_counter()-start)
        counts.append(occupancy(sim, cuda))
    result = dict(times_s=samples, median_s=median(samples), occupied=counts)
    if cuda:
        assert int(sim.motion.tick.get()[0]) == sim.step_index//sim.reaction_every
        result['bindings'], result['releases'] = map(int, sim.motion.counts.get())
        assert result['bindings']-result['releases'] == counts[-1]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--particles', type=int, nargs='+', default=[150, 2118])
    parser.add_argument('--steps', type=int, default=500)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--active-control', action='store_true',
                        help='place nearby ligands and use full site activity')
    args = parser.parse_args()
    if args.steps <= 0 or args.steps % 25 or any(n < 150 or n%2 for n in args.particles):
        parser.error('require steps in positive multiples of 25 and even counts >= 150')
    for count in args.particles:
        cpu = measure(count, args.steps, args.seed, False, args.active_control)
        hybrid = measure(count, args.steps, args.seed, False, args.active_control, hybrid=True)
        cuda = measure(count, args.steps, args.seed, True, args.active_control)
        print(json.dumps(dict(particles=count, steps=args.steps, seed=args.seed,
                              active_control=args.active_control, cpu=cpu, hybrid=hybrid, cuda=cuda,
                              speedup=cpu['median_s']/cuda['median_s'])), flush=True)


if __name__ == '__main__':
    main()
