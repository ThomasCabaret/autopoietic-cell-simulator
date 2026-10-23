"""Run a registered research case and preserve config, evidence and code hashes."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time as walltime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from local_dynamics import copying, vesicle

ROOT = Path(__file__).resolve().parents[1]


def components(n, edges):
    adj = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    seen, result = set(), []
    for i in range(n):
        if i in seen:
            continue
        stack, comp = [i], set()
        while stack:
            j = stack.pop()
            if j in comp:
                continue
            comp.add(j)
            stack.extend(adj[j])
        seen.update(comp)
        ends = [j for j in comp if len(adj[j]) == 1]
        order = []
        if len(comp) == 1:
            order = [i]
        elif ends or all(len(adj[j]) == 2 for j in comp):
            current, previous = min(ends) if ends else min(comp), -1
            while current not in order:
                order.append(current)
                nxt = [j for j in adj[current] if j != previous]
                if not nxt:
                    break
                previous, current = current, nxt[0]
        result.append((comp, order, bool(not ends and len(comp) >= 3)))
    return result


def simple_polygon(points):
    for i in range(len(points)):
        a, b = points[i], points[(i + 1) % len(points)]
        for j in range(i + 2, len(points)):
            if i == 0 and j == len(points) - 1:
                continue
            c, d = points[j], points[(j + 1) % len(points)]
            cross = lambda u, v: u[0] * v[1] - u[1] * v[0]
            if cross(b - a, c - a) * cross(b - a, d - a) < 0 and cross(d - c, a - c) * cross(d - c, b - c) < 0:
                return False
    return True


def area(points):
    return .5 * abs(np.sum(points[:, 0] * np.roll(points[:, 1], -1) - points[:, 1] * np.roll(points[:, 0], -1)))


class CopyObserver:
    def __init__(self, config):
        self.target = config.get("sequence", "001011")
        self.initial_count = len(self.target)
        self.complete, self.detached = set(), set()
        self.history, self.frames, self.times, self.edges_frames = [], [], [], []
        self.pairing_frames = []
        self.events = []
        self.new_source_events = self.complete_source_events = 0
        self.best_partial = 0
        self.translated, self.translated_detached = set(), set()
        self.edge_parent = {}
        self.certified = {tuple(range(self.initial_count)): 0} if config.get("template", True) and config.get("seed_family", 0) == 0 else {}
        self.last_shapes = []

    def __call__(self, time, pos, edges, pairing, bits, events, families=None):
        if families is None:
            families = np.zeros(len(bits), dtype=int)
        comp_list = components(len(bits), edges)
        active_full = set()
        for comp, order, cycle in comp_list:
            if order and not cycle and all(families[i] == 0 for i in comp):
                text = "".join(str(int(bits[i])) for i in order)
                if text in (self.target, self.target[::-1]):
                    active_full.add(tuple(sorted(comp)))
        # Only a previously observed, still complete parent can certify ancestry.
        prior = {key: gen for key, gen in self.certified.items() if key in active_full}
        for event in events:
            source = event["source"]
            parents = [key for key in prior if all(i in key for i in source)]
            self.edge_parent[tuple(sorted(event["formed"]))] = parents[0] if len(parents) == 1 else None
        correct_now = []
        self.last_shapes = []
        for comp, order, cycle in comp_list:
            if order and len(order) > 1 and all(families[i] == 1 for i in comp):
                p = pos[order]
                self.last_shapes.append({"sequence": "".join(str(int(bits[i])) for i in order),
                                         "contains_initial_material": any(i < self.initial_count for i in comp),
                                         "units": len(comp),
                                         "end_to_end": float(np.linalg.norm(p[-1] - p[0])),
                                         "radius_of_gyration": float(np.sqrt(np.mean(np.sum((p - p.mean(axis=0)) ** 2, axis=1))))})
            if not order or cycle or any(i < self.initial_count for i in comp):
                continue
            text = "".join(str(int(bits[i])) for i in order)
            if not all(families[i] == families[order[0]] for i in comp):
                raise AssertionError("Mixed chemical backbones violate family compatibility")
            if families[order[0]] == 1:
                if text in (self.target, self.target[::-1]):
                    key = tuple(sorted(comp))
                    self.translated.add(key)
                    if all(pairing[i] < 0 for i in comp):
                        self.translated_detached.add(key)
                continue
            if text in self.target or text[::-1] in self.target:
                self.best_partial = max(self.best_partial, len(text))
            if text in (self.target, self.target[::-1]):
                key = tuple(sorted(comp))
                self.complete.add(key)
                correct_now.append(comp)
                parents = [self.edge_parent.get(tuple(sorted((order[q], order[q + 1]))))
                           for q in range(len(order) - 1)]
                if parents and parents[0] in prior and all(p == parents[0] for p in parents):
                    self.certified.setdefault(key, prior[parents[0]] + 1)
                if all(pairing[i] < 0 for i in comp):
                    self.detached.add(key)
        for e in events:
            source = e["source"]
            if all(i >= self.initial_count for i in source):
                self.new_source_events += 1
            if any(all(i in comp for i in source) for comp in correct_now):
                self.complete_source_events += 1
            self.events.append({"time": time, **e})
        if not self.times or time - self.times[-1] >= .49:
            self.times.append(time)
            self.frames.append(pos.copy())
            self.pairing_frames.append(pairing.copy())
            mat = np.zeros((len(bits), len(bits)), dtype=np.uint8)
            for i, j in edges:
                mat[i, j] = mat[j, i] = 1
            self.edges_frames.append(mat)
            self.history.append({"time": time, "edges": len(edges),
                                 "paired_sites": int(np.count_nonzero(pairing >= 0)),
                                 "complete_ever": len(self.complete), "detached_ever": len(self.detached),
                                 "translated_ever": len(self.translated), "translated_detached_ever": len(self.translated_detached),
                                 "certified_max_generation": max(self.certified.values(), default=0)})
        self.last_bits = bits.copy()
        self.last_families = families.copy()

    def summary(self):
        return {"complete_copy_sets_ever": len(self.complete), "detached_copy_sets_ever": len(self.detached),
                "complete_sets": sorted(self.complete), "detached_sets": sorted(self.detached),
                "best_matching_fragment": self.best_partial,
                "ligation_events": len(self.events), "ligations_using_new_chains": self.new_source_events,
                "ligations_using_complete_copies": self.complete_source_events,
                "translated_chains_ever": len(self.translated),
                "translated_detached_ever": len(self.translated_detached),
                "translated_sets": sorted(self.translated),
                "certified_generations": [{"units": list(key), "generation": gen} for key, gen in sorted(self.certified.items()) if gen > 0],
                "certified_max_generation": max(self.certified.values(), default=0),
                "certified_detached_generation2": sum(key in self.detached and gen >= 2 for key, gen in self.certified.items()),
                "ancestry_criterion": "Every backbone edge comes from the same previously complete still-intact parent; observation only",
                "functional_chain_shapes_final": self.last_shapes,
                "sequence_convention": "unoriented chain: sequence identified up to reversal",
                "history": self.history, "events": self.events}


class VesicleObserver:
    def __init__(self, config):
        self.n = config.get("units", 16)
        self.frames, self.times, self.edges_frames, self.history = [], [], [], []
        self.closed_sets = set()

    def __call__(self, time, pos, edges):
        closed = []
        largest, turns = 0, []
        tail_edges = set(edges[1])
        for comp, order, cycle in components(self.n, edges[0]):
            largest = max(largest, len(comp))
            if len(order) >= 3:
                d = np.diff(pos[order], axis=0)
                turns.extend(np.arctan2(d[:-1, 0] * d[1:, 1] - d[:-1, 1] * d[1:, 0],
                                       np.sum(d[:-1] * d[1:], axis=1)).tolist())
            matching = all(tuple(sorted((order[i], order[(i + 1) % len(order)]))) in tail_edges
                           for i in range(len(order))) if cycle else False
            if cycle and matching and simple_polygon(pos[order]) and simple_polygon(pos[self.n + np.array(order)]):
                a = area(pos[order])
                if a > 1:
                    closed.append({"units": len(comp), "area": a})
                    self.closed_sets.add(tuple(sorted(comp)))
        mat = np.zeros((2, self.n, self.n), dtype=np.uint8)
        for row in (0, 1):
            for i, j in edges[row]:
                mat[row, i, j] = mat[row, j, i] = 1
        self.times.append(time)
        self.frames.append(pos.copy())
        self.edges_frames.append(mat)
        self.history.append({"time": time, "closed": closed, "largest_head_component": largest,
                             "mean_signed_turn_deg": float(np.rad2deg(np.mean(turns))) if turns else 0.,
                             "head_edges": len(edges[0]), "tail_edges": len(edges[1])})

    def summary(self):
        return {"closed_sets_ever": len(self.closed_sets), "closed_sets": sorted(self.closed_sets),
                "final_closed": self.history[-1]["closed"],
                "final_largest_component": self.history[-1]["largest_head_component"],
                "final_mean_signed_turn_deg": self.history[-1]["mean_signed_turn_deg"],
                "history": self.history}


def plot_run(observer, config, out):
    indices = np.linspace(0, len(observer.frames) - 1, 4, dtype=int)
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.5), constrained_layout=True)
    all_pos = np.concatenate(observer.frames)
    lo, hi = all_pos.min(axis=0) - .5, all_pos.max(axis=0) + .5
    for ax, index in zip(axes, indices):
        p = observer.frames[index]
        n = len(p) // 2
        for i in range(n):
            ax.plot(p[[i, n + i], 0], p[[i, n + i], 1], color="#bbc4cc", lw=.7)
        mat = observer.edges_frames[index]
        if config["mode"] == "copy":
            for i, j in np.argwhere(np.triu(mat, 1)):
                ax.plot(p[[i, j], 0], p[[i, j], 1], color="#617889", lw=1.5)
            ax.scatter(p[:n, 0], p[:n, 1], c=np.array(["#718594", "#9a4aa0"])[observer.last_families], s=15)
            ax.scatter(p[n:, 0], p[n:, 1], c=np.array(["#148e9c", "#df7947", "#8d75bb"])[observer.last_bits], s=18)
        else:
            for row in (0, 1):
                for i, j in np.argwhere(np.triu(mat[row], 1)):
                    a, b = row * n + i, row * n + j
                    ax.plot(p[[a, b], 0], p[[a, b], 1], color=["#148e9c", "#df7947"][row], lw=1.8)
            ax.scatter(p[:n, 0], p[:n, 1], color="#148e9c", s=20)
            ax.scatter(p[n:, 0], p[n:, 1], color="#df7947", s=20)
        ax.set_title(f"t = {observer.times[index]:.1f}")
        ax.set_xlim(lo[0], hi[0])
        ax.set_ylim(lo[1], hi[1])
        ax.set_aspect("equal")
    fig.suptitle(f"{config['case']} | graine {config['seed']} | {config['mode']} | conditions initiales : {config.get('initial', 'polymere + monomeres libres')}")
    fig.savefig(out / "trajectory.png", dpi=140)
    plt.close(fig)


def run(case, seed, duration=None, overrides=None):
    cases = json.loads((ROOT / "research/cases.json").read_text(encoding="utf-8"))
    config = {**cases[case], **(overrides or {}), "case": case, "seed": seed}
    if duration is not None:
        config["duration"] = duration
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out = ROOT / "research/runs" / f"{case}_s{seed}_{stamp}"
    out.mkdir(parents=True, exist_ok=False)
    source_files = [Path(__file__), Path(__file__).with_name("local_dynamics.py")]
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files}
    # Preserve exact sources as well as hashes: future edits do not erase provenance.
    for path in source_files:
        (out / path.name).write_bytes(path.read_bytes())
    (out / "replay.py").write_text(
        "import json\nfrom pathlib import Path\n"
        "from run_local_research import CopyObserver, VesicleObserver\n"
        "from local_dynamics import copying, vesicle\n"
        "c=json.loads(Path(__file__).with_name('config.json').read_text(encoding='utf-8'))\n"
        "o=CopyObserver(c) if c['mode']=='copy' else VesicleObserver(c)\n"
        "(copying if c['mode']=='copy' else vesicle)(c,c['seed'],o)\n"
        "print(json.dumps(o.summary(),indent=2))\n", encoding="utf-8")
    (out / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    observer = CopyObserver(config) if config["mode"] == "copy" else VesicleObserver(config)
    start = walltime.perf_counter()
    error = None
    try:
        (copying if config["mode"] == "copy" else vesicle)(config, seed, observer)
    except (FloatingPointError, RuntimeError) as exc:
        error = str(exc)
    elapsed = walltime.perf_counter() - start
    metrics = observer.summary() if observer.frames else {}
    evidence = {"config": config, "source_sha256": hashes, "numpy": np.__version__,
                "elapsed_seconds": elapsed, "error": error, "metrics": metrics}
    (out / "result.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    if observer.frames:
        extra = {"pairing": np.array(observer.pairing_frames), "recognition_types": observer.last_bits,
                 "families": observer.last_families} if config["mode"] == "copy" else {}
        np.savez_compressed(out / "trajectory.npz", positions=np.array(observer.frames),
                            times=np.array(observer.times), edges=np.array(observer.edges_frames), **extra)
        plot_run(observer, config, out)
    compact = {k: v for k, v in metrics.items() if k not in ("history", "events", "complete_sets", "detached_sets", "closed_sets", "translated_sets", "certified_generations", "functional_chain_shapes_final", "ancestry_criterion")}
    print(json.dumps({"run": str(out.relative_to(ROOT)), "error": error, "elapsed": elapsed, **compact}), flush=True)
    return evidence, out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("case")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--duration", type=float)
    parser.add_argument("--overrides", type=Path)
    args = parser.parse_args()
    overrides = json.loads(args.overrides.read_text(encoding="utf-8")) if args.overrides else None
    run(args.case, args.seed, args.duration, overrides)
