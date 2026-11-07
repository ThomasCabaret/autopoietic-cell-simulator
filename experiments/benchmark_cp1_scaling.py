"""Measure complete reactive steps at CP1 and integrated-cell particle counts."""
import argparse
import copy
import json
import math
from statistics import median
from time import perf_counter

from simulator.engine import Simulation
from simulator.runner import make_observer
from experiments.verify_resident_fields import cp1_config


def scaled_cp1(count):
    """Keep the CH1 laws and approximately preserve areal and linear densities."""
    config = cp1_config()
    c = config['chemistry']
    g = c['genetics']
    boundary = c['initial_boundary']
    template = len(g['sequence'])
    inside = template+g['free_units']+g['function_units']+c['food_units']
    rim = boundary['units']
    scale = (math.sqrt(rim*rim+2*inside*count)-rim)/(2*inside)
    area = scale*scale
    boundary['units'] = round(rim*scale)
    boundary['radius'] *= scale
    boundary['packet_box'] = [length*scale for length in boundary['packet_box']]
    boundary['packet_offset'] = [length*scale for length in boundary['packet_offset']]
    c['box'] = [length*scale for length in c['box']]
    for key in ('free_units', 'function_units'):
        g[key] = round(g[key]*area)
    g['initial_assemblies'] *= max(1, round(area))
    c['food_units'] = count//2-template-g['free_units']-g['function_units']-boundary['units']
    return config


def measure(config, backend, steps, repeats):
    config = copy.deepcopy(config)
    config['engine']['force_backend'] = backend
    config['duration'] = (250+steps*repeats)*config['engine']['dt']
    start = perf_counter()
    sim = Simulation(config)
    count = len(sim.chemistry.pos)
    sim.listeners.append(make_observer(sim.config, False))
    init = perf_counter()-start
    start = perf_counter()
    sim.advance(250)
    warmup = perf_counter()-start
    reactions = 0.
    react = sim.chemistry.react

    def timed_react(*args):
        nonlocal reactions
        start = perf_counter()
        result = react(*args)
        reactions += perf_counter()-start
        return result

    sim.chemistry.react = timed_react
    times = []
    for _ in range(repeats):
        reactions = 0.
        start = perf_counter()
        sim.advance(steps)
        times.append(dict(wall_s=perf_counter()-start, reactions_s=reactions))
    return dict(backend=backend, particles=count, init_s=init, warmup_s=warmup,
                samples=times, wall_s=median(t['wall_s'] for t in times),
                reactions_s=median(t['reactions_s'] for t in times),
                births=len(sim.chemistry.births), exchanges=len(sim.chemistry.exchanges))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--particles', type=int, nargs='+', default=[302, 1000, 2118])
    parser.add_argument('--steps', type=int, default=500)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--port-potential', choices=['competitive', 'saturated'], default='competitive')
    args = parser.parse_args()
    if args.steps < 1 or args.repeats < 1 or any(n < 302 or n%2 for n in args.particles):
        parser.error('require positive windows/repeats and even particle counts >= 302')
    for count in args.particles:
        config = cp1_config() if count == 302 else scaled_cp1(count)
        config['chemistry']['free_port_potential'] = args.port_potential
        cpu = measure(config, 'numba', args.steps, args.repeats)
        cuda = measure(config, 'cuda-resident', args.steps, args.repeats)
        assert cpu['particles'] == cuda['particles'] == count
        print(json.dumps(dict(steps=args.steps, seed=config['seed'],
                              port_potential=args.port_potential, cpu=cpu, cuda=cuda,
                              speedup=cpu['wall_s']/cuda['wall_s'],
                              reaction_floor_bound=cpu['wall_s']/cuda['reactions_s'])), flush=True)


if __name__ == '__main__':
    main()
