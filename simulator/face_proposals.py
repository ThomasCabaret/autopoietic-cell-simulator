"""Compiled traversal of local lipid-face proposals.

The caller owns acceptance and may mutate the passed occupancy arrays
between yields. The shared Generator advances in the original order.
"""
from numba import njit
import numpy as np


def stretched_pairs(pos, pairs, short, extension):
    """Batch the axial lengths and preserve the scalar rule at the cutoff."""
    n = len(pos)//2
    i, j = pairs.T
    heads = pos[j]-pos[i]
    tails = pos[n+j]-pos[n+i]
    strain = np.maximum(np.abs(np.sqrt(np.sum(heads*heads, axis=1))-1.),
                        np.abs(np.sqrt(np.sum(tails*tails, axis=1))-short))
    tolerance = 8*np.finfo(float).eps*max(1., abs(short), abs(extension))
    for row in np.flatnonzero(np.abs(strain-extension) <= tolerance):
        strain[row] = max(abs(np.linalg.norm(heads[row])-1.),
                          abs(np.linalg.norm(tails[row])-short))
    return strain > extension


@njit(cache=True, nogil=True)
def face_mismatch(head, tail, i, j, a, b):
    hx = head[j, b, 0]-head[i, a, 0]
    hy = head[j, b, 1]-head[i, a, 1]
    tx = tail[j, b, 0]-tail[i, a, 0]
    ty = tail[j, b, 1]-tail[i, a, 1]
    return (hx*hx+hy*hy)+(tx*tx+ty*ty)


@njit(cache=True, nogil=True)
def formation_proposals(candidates, head, tail, partners, rng, cutoff2, probability):
    for i, j in candidates:
        if j == partners[i, 0] or j == partners[i, 1]:
            continue
        for a in rng.permutation(2):
            b = 1-a
            if partners[i, a] >= 0 or partners[j, b] >= 0:
                continue
            if face_mismatch(head, tail, i, j, a, b) < cutoff2 and rng.random() < probability:
                yield i, j, a, b
                if partners[i, a] == j:
                    break


@njit(cache=True, nogil=True)
def exchange_proposals(candidates, stretched, head, tail, partners, partner_faces,
                       touched, rng, terminal, cutoff2, probability):
    for index, (x, y) in enumerate(candidates):
        for i, k in ((x, y), (y, x)):
            if k == partners[i, 0] or k == partners[i, 1]:
                continue
            for a in rng.permutation(2):
                b = 1-a
                j = partners[i, a]
                if j < 0 or partners[k, b] >= 0 or touched[i, a] or touched[k, b]:
                    continue
                old_face = partner_faces[i, a]
                if touched[j, old_face]:
                    continue
                if terminal and partners[j, 1-old_face] >= 0 and partners[k, 1-b] >= 0:
                    continue
                if stretched[index]:
                    continue
                q = face_mismatch(head, tail, i, k, a, b)
                if q >= cutoff2 or rng.random() >= probability:
                    continue
                yield i, k, a, b, j, old_face, q
                if partners[i, a] == k:
                    break
