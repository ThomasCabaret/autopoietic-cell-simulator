"""Bounded CFN1 comparison of the native force slice and the hybrid engine."""
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
from statistics import median
from time import perf_counter

import numpy as np

from simulator import checkpoint
from simulator.engine import Simulation
from simulator.native_forces import (
    _cuda_kernel,
    cpp_forces,
    cuda_forces,
    cuda_forces_device,
    pack_terms,
)
from simulator.physics import force_kernel


ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT/'research/campaign_recipes/CH1_20261106T073608844143Z/manifest.json'
LABEL = 'CH1_integrated_s1'
ENGINE_STEPS = 600


def seconds_per_call(call, repetitions, finish=lambda: None):
    call()
    finish()
    samples = []
    for _ in range(3):
        start = perf_counter()
        for _ in range(repetitions):
            call()
        finish()
        samples.append((perf_counter()-start)/repetitions)
    return median(samples)


def engine_config(backend):
    tasks = json.loads(RECIPE.read_text(encoding='utf-8'))['tasks']
    cfg = copy.deepcopy(next(t['scenario'] for t in tasks if t['label'] == LABEL))
    cfg['duration'] = ENGINE_STEPS*cfg['engine']['dt']
    if backend != 'numba':
        cfg['engine']['force_backend'] = backend
    return cfg


def compare_state(reference, trial):
    np.testing.assert_allclose(trial.chemistry.pos, reference.chemistry.pos, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(trial.motion.velocities, reference.motion.velocities, rtol=1e-12, atol=1e-12)
    if reference.chemistry.export() != trial.chemistry.export():
        raise AssertionError('Chemical state diverged on the comparison prefix')
    if reference.rng.bit_generator.state != trial.rng.bit_generator.state:
        raise AssertionError('Reaction/random stream diverged on the comparison prefix')
    return float(np.max(np.abs(trial.chemistry.pos-reference.chemistry.pos)))


def run():
    out = ROOT/'outputs/performance'/('CFN1_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    out.mkdir(parents=True)
    cp, _ = _cuda_kernel()
    baseline = Simulation(engine_config('numba'))
    baseline.advance(100)
    c = baseline.chemistry
    pairs = baseline.neighbors.pairs(c.pos, float(c.contact.max()), 'core')
    args = c.pos, pairs, c.kinds, c.contact, c.springs, c.angles
    expected = force_kernel(*args)
    rows = []
    for fn in (force_kernel, cpp_forces, cuda_forces):
        value = fn(*args)
        np.testing.assert_allclose(value, expected, rtol=1e-12, atol=1e-12)
        rows.append(dict(backend=fn.__name__, microseconds=1e6*seconds_per_call(lambda: fn(*args), 300),
                         max_force_error=float(np.max(np.abs(value-expected)))))

    device_terms = tuple(cp.asarray(x) for x in pack_terms(len(c.pos), *args[1:]))
    resident = []
    for batch in (1, 32, 100):
        positions = cp.asarray(np.repeat(c.pos[None, ...], batch, axis=0))
        forces = cp.empty_like(positions)
        def launch():
            cuda_forces_device(positions, device_terms, forces)
        microseconds = 1e6*seconds_per_call(launch, 600, cp.cuda.get_current_stream().synchronize)
        np.testing.assert_allclose(forces.get(), np.broadcast_to(expected, positions.shape),
                                   rtol=1e-12, atol=1e-12)
        resident.append(dict(batch=batch, microseconds=microseconds,
                             particles_per_call=batch*len(c.pos)))

    trajectories = []
    for backend in ('numba', 'cpp', 'cuda'):
        sim = Simulation(engine_config(backend))
        sim.advance(100)
        state = out/(backend+'.npz')
        checkpoint.save(state, sim)
        start = perf_counter()
        sim.advance(ENGINE_STEPS)
        elapsed = perf_counter()-start
        resumed, _ = checkpoint.load(state)
        resumed.advance(ENGINE_STEPS)
        np.testing.assert_array_equal(resumed.chemistry.pos, sim.chemistry.pos)
        np.testing.assert_array_equal(resumed.motion.velocities, sim.motion.velocities)
        if compare_state(sim, resumed) != 0:
            raise AssertionError('Same-backend checkpoint replay diverged')
        if backend == 'numba':
            reference = sim
        error = compare_state(reference, sim)
        trajectories.append(dict(backend=backend, seconds=elapsed, timed_steps=ENGINE_STEPS-100,
                                 max_position_error=error, exact_restart=True))
    props = cp.cuda.runtime.getDeviceProperties(cp.cuda.Device().id)
    result = dict(case=LABEL, recipe=RECIPE.relative_to(ROOT).as_posix(), particles=len(c.pos),
                  recipe_sha256=hashlib.sha256(RECIPE.read_bytes()).hexdigest(),
                  driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  pair_terms=len(pairs), spring_terms=len(c.springs), angle_terms=len(c.angles),
                  platform=platform.platform(), cupy=cp.__version__, gpu=props['name'].decode(),
                  runtime=cp.cuda.runtime.runtimeGetVersion(), snapshot_force_calls=rows,
                  resident_repeated_snapshot=resident, hybrid_prefix=trajectories,
                  source_sha256=checkpoint.source_hashes(),
                  scope='Core forces only. Resident batches repeat one snapshot, not integrated trajectories. '
                        'Hybrid engine retains CPU neighbor search, additional forces, integration and reactions.')
    (out/'driver.py').write_bytes(Path(__file__).read_bytes())
    (out/'report.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(output=str(out), **{k:v for k,v in result.items() if k!='source_sha256'}),
                     indent=2), flush=True)


if __name__ == '__main__':
    run()
