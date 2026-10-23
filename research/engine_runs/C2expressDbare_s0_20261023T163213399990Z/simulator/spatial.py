"""Deterministically ordered finite-range contacts, with a Verlet skin."""
import numpy as np
from scipy.spatial import cKDTree


class Neighborhood:
    def __init__(self, method="tree", skin=0.25):
        if method not in ("tree", "brute") or skin < 0:
            raise ValueError("spatial must be tree or brute, with nonnegative skin")
        self.method, self.skin = method, float(skin)
        self.cache = {}
        self.rebuilds = 0

    def pairs(self, points, radius, key="default"):
        points = np.asarray(points, dtype=float)
        old = self.cache.get(key)
        rebuild = (old is None or old[0].shape != points.shape or old[2] != radius)
        if not rebuild and len(points):
            rebuild = np.max(np.sum((points - old[0]) ** 2, axis=1)) > (self.skin / 2) ** 2
        if rebuild:
            reach = radius + self.skin
            if self.method == "tree":
                pairs = cKDTree(points).query_pairs(reach, output_type="ndarray")
            else:
                i, j = np.triu_indices(len(points), 1)
                keep = np.sum((points[j] - points[i]) ** 2, axis=1) <= reach ** 2
                pairs = np.column_stack((i[keep], j[keep]))
            pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
            if len(pairs):
                pairs = pairs[np.lexsort((pairs[:, 1], pairs[:, 0]))]
            self.cache[key] = (points.copy(), pairs, radius)
            self.rebuilds += 1
        pairs = self.cache[key][1]
        if not len(pairs):
            return pairs
        distance2 = np.sum((points[pairs[:, 1]] - points[pairs[:, 0]]) ** 2, axis=1)
        return pairs[distance2 < radius ** 2]
