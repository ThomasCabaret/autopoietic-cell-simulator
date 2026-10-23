"""Local bead mechanics and bounded reaction motifs for exploratory experiments.

No connected-component, sequence, contour or parent/copy test occurs here.
The fixed pairs of indices in `rungs` are actual initial scaffold bonds.
"""
from __future__ import annotations

import numpy as np


def add_force(force, indices, values):
    np.add.at(force, indices, values)


def mechanical_forces(pos, springs, angles, core, core_k=80.):
    """Springs (i,j,k,length), angles (i,j,k,stiffness,cos0), pair soft cores."""
    force = np.zeros_like(pos)
    delta = pos[:, None, :] - pos[None, :, :]
    distance = np.linalg.norm(delta, axis=-1)
    overlap = np.maximum(core - distance, 0)
    scale = core_k * overlap / np.maximum(distance, 1e-8)
    force += np.sum(scale[..., None] * delta, axis=1)
    if len(springs):
        a = np.asarray(springs)
        i, j = a[:, 0].astype(int), a[:, 1].astype(int)
        d = pos[j] - pos[i]
        r = np.linalg.norm(d, axis=1)
        f = (a[:, 2] * (r - a[:, 3]) / np.maximum(r, 1e-8))[:, None] * d
        add_force(force, i, f)
        add_force(force, j, -f)
    if len(angles):
        a = np.asarray(angles)
        i, j, k = [a[:, q].astype(int) for q in range(3)]
        u, v = pos[i] - pos[j], pos[k] - pos[j]
        lu = np.maximum(np.linalg.norm(u, axis=1), 1e-8)
        lv = np.maximum(np.linalg.norm(v, axis=1), 1e-8)
        nu, nv = u / lu[:, None], v / lv[:, None]
        c = np.sum(nu * nv, axis=1)
        scale = a[:, 3] * (c - a[:, 4])
        gu = (scale / lu)[:, None] * (nv - c[:, None] * nu)
        gv = (scale / lv)[:, None] * (nu - c[:, None] * nv)
        add_force(force, i, -gu)
        add_force(force, k, -gv)
        add_force(force, j, gu + gv)
    return force


def normals(pos, rungs):
    d = pos[rungs[:, 1]] - pos[rungs[:, 0]]
    return d / np.maximum(np.linalg.norm(d, axis=1), 1e-8)[:, None]


def opposite_force(pos, rungs, pairs, stiffness=8.):
    """A local four-bead orientation potential k*(1+n_i dot n_j)."""
    force = np.zeros_like(pos)
    if not pairs:
        return force
    pairs = np.asarray(pairs, dtype=int)
    a, b = pairs[:, 0], pairs[:, 1]
    d = pos[rungs[:, 1]] - pos[rungs[:, 0]]
    lengths = np.maximum(np.linalg.norm(d, axis=1), 1e-8)
    n = d / lengths[:, None]
    dot = np.sum(n[a] * n[b], axis=1)
    ga = (stiffness / lengths[a])[:, None] * (n[b] - dot[:, None] * n[a])
    gb = (stiffness / lengths[b])[:, None] * (n[a] - dot[:, None] * n[b])
    for indices, g in ((a, ga), (b, gb)):
        add_force(force, rungs[indices, 1], -g)
        add_force(force, rungs[indices, 0], g)
    return force


def local_port_free(i, j, positions, edges, capacity=2):
    """Two opposite ports, inspecting directly bonded neighbors only."""
    neighbors = [b if a == i else a for a, b in edges if a == i or b == i]
    if len(neighbors) >= capacity:
        return False
    d = positions[j] - positions[i]
    return all(np.dot(positions[k] - positions[i], d) < 0 for k in neighbors)


def degree(n, edges):
    result = np.zeros(n, dtype=int)
    for i, j in edges:
        result[i] += 1
        result[j] += 1
    return result


def integrate(pos, force, rng, dt, mobility, temperature, box=None):
    if box is not None:
        # Spatial walls, identical for all particles; no biological recruitment.
        force += 100 * (np.maximum(-pos, 0) - np.maximum(pos - box, 0))
    displacement = mobility * dt * force
    displacement += np.sqrt(2 * mobility * temperature * dt) * rng.normal(size=pos.shape)
    if not np.isfinite(displacement).all() or np.max(np.linalg.norm(displacement, axis=1)) > 1:
        raise FloatingPointError("Integrator unstable; reduce dt rather than clipping dynamics")
    return pos + displacement


def copying(config, seed, observer):
    """Composite support+recognition dimers; exact matching and local ligation.

    `observer` receives snapshots/events for analysis only and returns nothing.
    Sequence is used solely for initial atom types/connectivity.
    """
    rng = np.random.default_rng(seed)
    sequence = config.get("sequence", "001011")
    length = len(sequence)
    extra = config.get("free_units", 30)
    alphabet = config.get("alphabet", "01")
    bits = np.array([int(x) for x in sequence] + [int(alphabet[i % len(alphabet)]) for i in range(extra)])
    capacities = np.where(bits == config.get("caps_symbol", -1), 1, 2)
    n = len(bits)
    rungs = np.column_stack([np.arange(n), n + np.arange(n)])
    box = np.array(config.get("box", [10., 7.]))
    pos = np.empty((2 * n, 2))
    pos[:length, 0] = np.arange(length) + (box[0] - length + 1) / 2
    pos[:length, 1] = box[1] / 2 - .45
    pos[n:n + length] = pos[:length] + [0, .45]
    for i in range(length, n):
        for attempt in range(20000):
            candidate = rng.uniform([.6, .6], box - .6)
            if np.min(np.linalg.norm(pos[:i] - candidate, axis=1)) > config.get("initial_min_separation", .60):
                break
        else:
            raise RuntimeError("Initial packing jam: enlarge box or reduce initial minimum separation")
        pos[i] = candidate
        angle = rng.uniform(0, 2 * np.pi)
        pos[n + i] = candidate + .45 * np.array([np.cos(angle), np.sin(angle)])
    edges = {(i, i + 1) for i in range(length - 1)} if config.get("template", True) else set()
    pairing = np.full(n, -1, dtype=int)
    core = np.full((2 * n, 2 * n), .28)
    core[:n, :n] = .70
    core[n:, n:] = 0.  # Recognition beads can overlap; support beads cannot.
    np.fill_diagonal(core, 0)
    dt = config.get("dt", .005)
    duration = config.get("duration", 180.)
    check_every = 5
    sample_every = 100
    gate = config.get("activation", True)
    cycle = config.get("release", "cycle")
    period, release_time = config.get("period", 60.), config.get("release_time", 10.)
    springs, angles = [], []
    for step in range(int(round(duration / dt)) + 1):
        time = step * dt
        events = []
        if step % check_every == 0:
            interval = dt * check_every
            deg = degree(n, edges)
            nrm = normals(pos, rungs)
            release = cycle == "cycle" and time % period >= period - release_time
            for i in range(n):
                j = pairing[i]
                if j <= i:
                    continue
                rate = .003
                if gate and deg[i] == 0 and deg[j] == 0:
                    rate = 5.
                if release:
                    rate = 12.
                if cycle == "local" and deg[i] > 0 and deg[j] > 0:
                    rate = config.get("local_off_rate", .2)
                if rng.random() < -np.expm1(-rate * interval):
                    pairing[i] = pairing[j] = -1
            distances = np.linalg.norm(pos[n:, None] - pos[None, n:], axis=-1)
            candidates = np.argwhere(np.triu((distances < .3) & (bits[:, None] == bits[None, :]), 1))
            rng.shuffle(candidates)
            for i, j in candidates:
                if pairing[i] >= 0 or pairing[j] >= 0 or np.dot(nrm[i], nrm[j]) > -.5:
                    continue
                if release:
                    continue
                rate = 35. if not gate or deg[i] or deg[j] else .1
                if rng.random() < -np.expm1(-rate * interval):
                    pairing[i], pairing[j] = j, i
            # Symmetric completion: any existing edge can supply the parallel edge.
            for i, j in list(edges):
                a, b = pairing[i], pairing[j]
                if a < 0 or b < 0 or a == b:
                    continue
                pair = tuple(sorted((int(a), int(b))))
                if pair in edges or not config.get("ligation", True):
                    continue
                d = pos[b] - pos[a]
                distance = np.linalg.norm(d)
                if not .72 < distance < 1.28 or np.dot(nrm[a], nrm[b]) < .5:
                    continue
                if abs(np.dot(nrm[a], d)) > .5 * distance or abs(np.dot(nrm[b], d)) > .5 * distance:
                    continue
                if not local_port_free(a, b, pos, edges, capacities[a]) or not local_port_free(b, a, pos, edges, capacities[b]):
                    continue
                if rng.random() < -np.expm1(-config.get("ligation_rate", 12.) * interval):
                    edges.add(pair)
                    events.append({"source": (i, j), "formed": pair})
            springs = [(i, n + i, 180., .45) for i in range(n)]
            angles = []
            for i, j in edges:
                springs.append((i, j, 100., 1.))
                stiffness = config.get("backbone_angle", 5.)
                angles.extend([(n + i, i, j, stiffness, 0.), (n + j, j, i, stiffness, 0.)])
            for i in range(n):
                if pairing[i] > i:
                    springs.append((n + i, n + pairing[i], 80., 0.))
        if step % sample_every == 0 or events:
            observer(time, pos, edges, pairing, bits, events)
        if step == int(round(duration / dt)):
            break
        pairs = [(i, int(j)) for i, j in enumerate(pairing) if j > i]
        force = mechanical_forces(pos, springs, angles, core)
        force += opposite_force(pos, rungs, pairs)
        pos = integrate(pos, force, rng, dt, .25, .6, box)


def vesicle(config, seed, observer):
    """Coupled rows with differential bond lengths. No closure test in dynamics."""
    rng = np.random.default_rng(seed)
    n = config.get("units", 16)
    rungs = np.column_stack([np.arange(n), n + np.arange(n)])
    long, short = 1., config.get("short_length", .75)
    shaft = .65
    fragment = config.get("fragment_size", n)
    pos = np.empty((2 * n, 2))
    edges = [set(), set()]
    init = config.get("initial", "straight")
    for start in range(0, n, fragment):
        size = min(fragment, n - start)
        ids = np.arange(start, start + size)
        if init == "straight":
            x = (np.arange(size) - (size - 1) / 2) * (long + short) / 2
            head = np.column_stack([x, np.full(size, shaft / 2)])
            tail = head - [0, shaft]
        else:
            # Preformed fragments; no initial ring or coordinated arrangement.
            angle_step = 2 * np.arcsin((long - short) / (2 * shaft)) if long != short else .001
            angles0 = (np.arange(size) - (size - 1) / 2) * angle_step
            radius = long / (2 * np.sin(angle_step / 2))
            head = np.column_stack([radius * np.sin(angles0), radius * (np.cos(angles0) - 1)])
            tail = head - shaft * np.column_stack([np.sin(angles0), np.cos(angles0)])
            theta = rng.uniform(0, 2 * np.pi)
            rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
            center = rng.uniform(-4, 4, size=2)
            head, tail = head @ rot.T + center, tail @ rot.T + center
        pos[ids], pos[n + ids] = head, tail
        for i in range(start, start + size - 1):
            edges[0].add((i, i + 1))
            edges[1].add((i, i + 1))
    pos += rng.normal(scale=.015, size=pos.shape)
    core = np.full((2 * n, 2 * n), .40)
    np.fill_diagonal(core, 0)
    dt = config.get("dt", .002)
    duration = config.get("duration", 100.)
    springs, angles = [], []
    deg = [degree(n, e) for e in edges]
    for step in range(int(round(duration / dt)) + 1):
        time = step * dt
        if step % 5 == 0:
            nrm = normals(pos, rungs)
            for row, length in enumerate((long, short)):
                offset = row * n
                available = np.flatnonzero(degree(n, edges[row]) < 2)
                candidates = [(int(i), int(j)) for a, i in enumerate(available) for j in available[a + 1:]]
                if not config.get("bonding", True):
                    candidates = []
                rng.shuffle(candidates)
                for i, j in candidates:
                    if (i, j) in edges[row]:
                        continue
                    d = pos[offset + j] - pos[offset + i]
                    distance = np.linalg.norm(d)
                    if not length - .22 < distance < length + .22 or np.dot(nrm[i], nrm[j]) < .5:
                        continue
                    if abs(np.dot(nrm[i], d)) > .6 * distance or abs(np.dot(nrm[j], d)) > .6 * distance:
                        continue
                    rp = pos[offset:offset + n]
                    if not local_port_free(i, j, rp, edges[row]) or not local_port_free(j, i, rp, edges[row]):
                        continue
                    if rng.random() < -np.expm1(-25 * dt * 5):
                        edges[row].add((i, j))
            springs = [(i, n + i, 180., shaft) for i in range(n)]
            angles = []
            for row, length in enumerate((long, short)):
                offset, opposite = row * n, (1 - row) * n
                for i, j in edges[row]:
                    springs.append((offset + i, offset + j, 120., length))
                    angles.extend([(opposite + i, offset + i, offset + j, 1., 0.),
                                   (opposite + j, offset + j, offset + i, 1., 0.)])
            deg = [degree(n, e) for e in edges]
        if step % 200 == 0:
            observer(time, pos, edges)
        if step == int(round(duration / dt)):
            break
        force = mechanical_forces(pos, springs, angles, core)
        # Short-range attraction of exposed primitive row ports, not whole units.
        for row, length in enumerate((long, short)):
            ids = np.flatnonzero(deg[row] < 2) + row * n
            if len(ids) < 2:
                continue
            d = pos[ids][None, :, :] - pos[ids][:, None, :]
            r = np.linalg.norm(d, axis=-1)
            z = (r - length) / .25
            scale = np.where((r < length + .5) & (r > .1), config.get("end_attraction", 4.) * z / .25 * np.exp(-z ** 2) / np.maximum(r, 1e-8), 0)
            add_force(force, ids, np.sum(scale[..., None] * d, axis=1))
        pos = integrate(pos, force, rng, dt, .4, config.get("temperature", .06))
