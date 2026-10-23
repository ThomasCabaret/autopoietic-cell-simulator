"""Collect immutable run references and scientific plots for research batch 2."""
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/BATCH_02.json"
if MANIFEST.exists():
    inputs = json.loads(MANIFEST.read_text(encoding="utf-8"))["dynamic_results"]
else:
    inputs = []
    for path in sorted((ROOT / "research/runs").glob("*/result.json")):
        result = json.loads(path.read_text(encoding="utf-8"))
        if "translated_chains_ever" in result.get("metrics", {}):
            inputs.append(path.relative_to(ROOT).as_posix())
records = [json.loads((ROOT / path).read_text(encoding="utf-8")) for path in inputs]


def find(case, seed):
    matches = [r for r in records if r["config"]["case"] == case and r["config"]["seed"] == seed and not r["error"]]
    assert len(matches) == 1, (case, seed, len(matches))
    return matches[0]


shape = {}
for case in ("E1zero", "E1alternating", "E1control"):
    values = [find(case, s)["metrics"]["functional_chain_shapes_final"][0]["end_to_end"] for s in (0, 1, 2)]
    shape[case] = {"end_to_end_by_seed": values, "mean": float(np.mean(values)), "sample_sd": float(np.std(values, ddof=1))}
summary = {"batch": 2, "dynamic_results": inputs,
           "formal_result": "research/abstract_runs/C0_20261023T131308019594Z/result.json",
           "new_dynamic_runs": len(records), "new_technical_errors": sum(bool(r["error"]) for r in records),
           "second_generation_detached_by_seed": [find("T7", s)["metrics"]["certified_detached_generation2"] for s in (0, 1, 2)],
           "native_geometry_control": shape,
           "maturity": "early partial proof: no demonstrated catalyst construction or causal material closure"}
interfaces = {}
for case, seed in [("E0mixed", 0), ("E2mixed", 0), ("E2mixed", 1)]:
    index = next(i for i, r in enumerate(records) if r["config"]["case"] == case and r["config"]["seed"] == seed)
    data = np.load((ROOT / inputs[index]).parent / "trajectory.npz")
    both = mismatch = 0
    for paired in data["pairing"]:
        for i in range(len(records[index]["config"]["sequence"]) - 1):
            a, b = paired[i], paired[i + 1]
            if a >= 0 and b >= 0:
                both += 1
                mismatch += int(data["families"][a] != data["families"][b])
    interfaces[f"{case}_seed{seed}"] = {"occupied_neighbor_observations": both,
                                       "mixed_incompatible_observations": mismatch,
                                       "fraction": mismatch / both if both else None,
                                       "scope": "Repeated correlated snapshots on the original gene, not independent trials"}
summary["incompatible_recruitment_interfaces"] = interfaces
MANIFEST.write_text(json.dumps(summary, indent=2), encoding="utf-8")

fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), constrained_layout=True)
x = np.arange(3)
axes[0].bar(x - .17, [find("T7", s)["metrics"]["detached_copy_sets_ever"] for s in (0, 1, 2)], width=.34, label="Copies completes liberees")
axes[0].bar(x + .17, summary["second_generation_detached_by_seed"], width=.34, label="Generation >= 2 certifiee")
axes[0].set(xticks=x, xticklabels=["Graine 0", "Graine 1", "Graine 2"], ylabel="Nombre de nouvelles chaines", title="T7 : une deuxieme generation observee")
axes[0].legend(fontsize=8)
cases = [("E0mixed", 0), ("E2mixed", 0), ("E2mixed", 1)]
axes[1].bar(x - .17, [find(c, s)["metrics"]["detached_copy_sets_ever"] for c, s in cases], width=.34, label="Copie G liberee", color="#306eaf")
axes[1].bar(x + .17, [find(c, s)["metrics"]["translated_detached_ever"] for c, s in cases], width=.34, label="Traduction F liberee", color="#9a4aa0")
axes[1].set(xticks=x, xticklabels=["Mixte simple\ngraine 0", "Cooperation\ngraine 0", "Cooperation\ngraine 1"], title="Le bain commun reste un verrou", ylabel="Produits complets observes")
axes[1].legend(fontsize=8)
axes[2].bar(x, [v["mean"] for v in shape.values()], yerr=[v["sample_sd"] for v in shape.values()], capsize=5,
            color=["#148e9c", "#df7947", "#9daab5"])
axes[2].set(xticks=x, xticklabels=["F:000000", "F:010101", "F:000000\nangle neutre"],
            ylabel="Distance entre extremites", title="Sequence -> geometrie, pas encore fonction")
fig.suptitle("Lot 2 : resultats dynamiques et contre-exemples\nPetits echantillons ; barres d'erreur = ecart-type sur 3 graines, pas une calibration du rendement", fontsize=13)
fig.savefig(ROOT / "research/BATCH_02.png", dpi=160)
print(json.dumps(summary, indent=2))
