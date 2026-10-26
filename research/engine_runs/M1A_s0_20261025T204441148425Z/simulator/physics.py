"""Array kernels; no chemistry, aggregate labels, renderer or experiment logic."""
import numpy as np
from numba import njit


@njit(cache=True, nogil=True)
def force_kernel(pos, pairs, kinds, contact, springs, angles, core_k=80.):
    force = np.zeros_like(pos)
    for q in range(len(pairs)):
        i, j = pairs[q, 0], pairs[q, 1]
        dx, dy = pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1]
        r = np.sqrt(dx * dx + dy * dy)
        scale = core_k * max(contact[kinds[i], kinds[j]] - r, 0.) / max(r, 1e-8)
        force[i, 0] -= scale * dx
        force[i, 1] -= scale * dy
        force[j, 0] += scale * dx
        force[j, 1] += scale * dy
    for q in range(len(springs)):
        i, j = int(springs[q, 0]), int(springs[q, 1])
        dx, dy = pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1]
        r = np.sqrt(dx * dx + dy * dy)
        scale = springs[q, 2] * (r - springs[q, 3]) / max(r, 1e-8)
        force[i, 0] += scale * dx
        force[i, 1] += scale * dy
        force[j, 0] -= scale * dx
        force[j, 1] -= scale * dy
    for q in range(len(angles)):
        i, j, k = int(angles[q, 0]), int(angles[q, 1]), int(angles[q, 2])
        ux, uy = pos[i, 0] - pos[j, 0], pos[i, 1] - pos[j, 1]
        vx, vy = pos[k, 0] - pos[j, 0], pos[k, 1] - pos[j, 1]
        lu, lv = max(np.sqrt(ux*ux + uy*uy), 1e-8), max(np.sqrt(vx*vx + vy*vy), 1e-8)
        ux, uy, vx, vy = ux/lu, uy/lu, vx/lv, vy/lv
        c = ux*vx + uy*vy
        s = angles[q, 3] * (c - angles[q, 4])
        gx, gy = s/lu*(vx-c*ux), s/lu*(vy-c*uy)
        hx, hy = s/lv*(ux-c*vx), s/lv*(uy-c*vy)
        force[i, 0] -= gx
        force[i, 1] -= gy
        force[k, 0] -= hx
        force[k, 1] -= hy
        force[j, 0] += gx+hx
        force[j, 1] += gy+hy
    return force


@njit(cache=True, nogil=True)
def orientation_kernel(pos, rungs, pairs, stiffness=8.):
    force = np.zeros_like(pos)
    for q in range(len(pairs)):
        a, b = pairs[q, 0], pairs[q, 1]
        i, j = rungs[a, 0], rungs[a, 1]
        k, l = rungs[b, 0], rungs[b, 1]
        ux, uy = pos[j, 0]-pos[i, 0], pos[j, 1]-pos[i, 1]
        vx, vy = pos[l, 0]-pos[k, 0], pos[l, 1]-pos[k, 1]
        lu, lv = max(np.sqrt(ux*ux+uy*uy), 1e-8), max(np.sqrt(vx*vx+vy*vy), 1e-8)
        ux, uy, vx, vy = ux/lu, uy/lu, vx/lv, vy/lv
        c = ux*vx+uy*vy
        gx, gy = stiffness/lu*(vx-c*ux), stiffness/lu*(vy-c*uy)
        hx, hy = stiffness/lv*(ux-c*vx), stiffness/lv*(uy-c*vy)
        force[i, 0] += gx
        force[i, 1] += gy
        force[j, 0] -= gx
        force[j, 1] -= gy
        force[k, 0] += hx
        force[k, 1] += hy
        force[l, 0] -= hx
        force[l, 1] -= hy
    return force


@njit(cache=True, nogil=True)
def attraction_kernel(pos, pairs, length, strength):
    force = np.zeros_like(pos)
    for q in range(len(pairs)):
        i,j = pairs[q,0],pairs[q,1]
        dx,dy = pos[j,0]-pos[i,0],pos[j,1]-pos[i,1]
        r = np.sqrt(dx*dx+dy*dy)
        if r <= .1 or r >= length+.5:
            continue
        z = (r-length)/.25
        s = strength*z/.25*np.exp(-z*z)/r
        force[i,0] += s*dx
        force[i,1] += s*dy
        force[j,0] -= s*dx
        force[j,1] -= s*dy
    return force
