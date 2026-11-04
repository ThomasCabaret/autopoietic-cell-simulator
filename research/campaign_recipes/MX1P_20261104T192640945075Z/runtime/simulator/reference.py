"""Reference force formulas retained for gradient checks; no simulation loop."""
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

def port_sites(pos, rungs, edges, row, length):
    """Virtual localized ports fixed to a bead and its single rung neighbor."""
    n = len(rungs)
    offset, other = row * n, (1 - row) * n
    anchors, neighbors, signs = [], [], []
    for i in range(n):
        bonded = [b if a == i else a for a, b in edges if a == i or b == i]
        if len(bonded) >= 2:
            continue
        u = pos[other + i] - pos[offset + i]
        normal = u / np.linalg.norm(u)
        tangent = np.array([-normal[1], normal[0]])
        free = (-1, 1) if not bonded else (-1 if np.dot(pos[offset + bonded[0]] - pos[offset + i], tangent) > 0 else 1,)
        for sign in free:
            anchors.append(offset + i)
            neighbors.append(other + i)
            signs.append(sign)
    anchors, neighbors, signs = np.array(anchors, dtype=int), np.array(neighbors, dtype=int), np.array(signs)
    u = pos[neighbors] - pos[anchors]
    radius = np.maximum(np.linalg.norm(u, axis=1), 1e-8)
    normal = u / radius[:, None]
    tangent = np.column_stack([-normal[:, 1], normal[:, 0]])
    sites = pos[anchors] + signs[:, None] * (length / 2) * tangent
    return sites, anchors, neighbors, signs, normal, radius

def port_attraction(pos, rungs, edges, row, length, epsilon=.6, neighbors=None):
    """Gaussian attraction between free virtual sites, including exact torques.

    Virtual sites are geometric ports, not extra particles. The force is applied
    to the two real, directly bonded beads defining each port. Range is finite.
    """
    spatial = neighbors
    force = np.zeros_like(pos)
    sites, anchors, neighbors, signs, normal, radius = port_sites(pos, rungs, edges, row, length)
    if len(sites) < 2:
        return force
    if spatial is None:
        ii, jj = np.triu_indices(len(sites), 1)
    else:
        pairs = spatial.pairs(sites, .75, "virtual_ports"+str(row))
        ii, jj = pairs[:,0], pairs[:,1]
    allowed = anchors[ii] != anchors[jj]
    allowed &= np.array([tuple(sorted((int(anchors[a] % len(rungs)), int(anchors[b] % len(rungs))))) not in edges for a, b in zip(ii, jj)], dtype=bool)
    ii, jj = ii[allowed], jj[allowed]
    delta = sites[jj] - sites[ii]
    r2 = np.sum(delta ** 2, axis=1)
    strength = np.where(r2 < .75 ** 2, 2 * epsilon / .25 ** 2 * np.exp(-r2 / .25 ** 2), 0.)
    fs = strength[:, None] * delta
    site_force = np.zeros_like(sites)
    add_force(site_force, ii, fs)
    add_force(site_force, jj, -fs)
    # J^T F, followed by the derivative of vector normalization.
    jt_force = np.column_stack([site_force[:, 1], -site_force[:, 0]])
    perpendicular = jt_force - normal * np.sum(normal * jt_force, axis=1)[:, None]
    neighbor_force = (signs * length / (2 * radius))[:, None] * perpendicular
    add_force(force, neighbors, neighbor_force)
    add_force(force, anchors, site_force - neighbor_force)
    return force
