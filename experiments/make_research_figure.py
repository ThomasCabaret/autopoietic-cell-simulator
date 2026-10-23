"""Illustrate measured states from archived trajectories, without rerunning physics."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
copy_dir = ROOT / "research/runs/T4_s0_20261023T114355798586Z"
vesicle_dir = ROOT / "research/runs/V6_s1_20261023T115206264055Z"
c = json.loads((copy_dir / "result.json").read_text())
v = json.loads((vesicle_dir / "result.json").read_text())
ct, vt = np.load(copy_dir / "trajectory.npz"), np.load(vesicle_dir / "trajectory.npz")
target = c["config"]["sequence"]
bits = np.array([int(x) for x in target] + [i % 2 for i in range(c["config"]["free_units"])])
copy_ids = np.array(c["metrics"]["complete_sets"][0])
seed_ids = np.arange(len(target))
selected = np.concatenate([seed_ids, copy_ids])
fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
for ax, metric, title in zip(axes[0], ("complete_ever", "detached_ever"),
                             ("Copie complete observee", "Copie liberee observee")):
    index = next(i for i, h in enumerate(c["metrics"]["history"]) if h[metric])
    if metric == "detached_ever":
        # Show a later point in the same release phase to allow diffusion.
        # Pairing formation is disabled throughout this fixed external phase.
        period = c["config"].get("period", 60.)
        phase_end = (np.floor(ct["times"][index] / period) + 1) * period
        index = int(np.argmin(abs(ct["times"] - (phase_end - 1))))
    p, mat = ct["positions"][index], ct["edges"][index]
    n = len(p) // 2
    ax.scatter(p[:n, 0], p[:n, 1], color="#d8dce1", s=7)
    for ids, color in ((seed_ids, "#306eaf"), (copy_ids, "#9a4aa0")):
        for i in ids:
            ax.plot(p[[i, n + i], 0], p[[i, n + i], 1], color=color, lw=1)
            ax.scatter(*p[i], color=color, s=25)
            ax.scatter(*p[n + i], color=["#148e9c", "#df7947"][bits[i]], s=35)
        for i, j in np.argwhere(np.triu(mat, 1)):
            if i in ids and j in ids:
                ax.plot(p[[i, j], 0], p[[i, j], 1], color=color, lw=2)
    relevant = p[np.concatenate([selected, n + selected])]
    lo, hi = relevant.min(axis=0) - .5, relevant.max(axis=0) + .5
    ax.set_xlim(lo[0], hi[0])
    ax.set_ylim(lo[1], hi[1])
    ax.set_aspect("equal")
    ax.set_title(f"{title}, t={ct['times'][index]:.1f}")
    ax.set_xlabel("Support initial : bleu | nouvelle chaine : violet")
for ax, index, title in zip(axes[1], (0, -1), ("Fragments composites disperses", "Assemblage en boucle de 15 sous-unites")):
    p, mat = vt["positions"][index], vt["edges"][index]
    n = len(p) // 2
    for i in range(n):
        ax.plot(p[[i, n + i], 0], p[[i, n + i], 1], color="#aab5bf", lw=1)
    for row, color in ((0, "#148e9c"), (1, "#df7947")):
        for i, j in np.argwhere(np.triu(mat[row], 1)):
            ax.plot(p[[row * n + i, row * n + j], 0], p[[row * n + i, row * n + j], 1], color=color, lw=1.8)
        ax.scatter(p[row * n:(row + 1) * n, 0], p[row * n:(row + 1) * n, 1], color=color, s=25)
    ax.set_aspect("equal")
    ax.set_title(f"{title}, t={vt['times'][index]:.0f}")
    ax.set_xlabel("Deux types de liaisons laterales : longueurs preferees differentes")
fig.suptitle("Deux premieres demonstrations dynamiques de chimies composites\nEtats issus de trajectoires archivees ; temps et longueurs sans dimension", fontsize=14)
fig.savefig(ROOT / "research/first_demonstrations.png", dpi=160)
print("Saved research/first_demonstrations.png")
