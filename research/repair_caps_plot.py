"""Postprocess preserved data after the initial two-color plotter rejected a cap."""
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
from run_local_research import CopyObserver, plot_run

run = ROOT / "research/runs/T6caps_s1_20261023T114355856585Z"
config = json.loads((run / "config.json").read_text())
data = np.load(run / "trajectory.npz")
observer = CopyObserver(config)
observer.frames = data["positions"]
observer.times = data["times"]
observer.edges_frames = data["edges"]
alphabet = config.get("alphabet", "01")
observer.last_bits = np.array([int(s) for s in config["sequence"]] +
                              [int(alphabet[i % len(alphabet)]) for i in range(config["free_units"])])
observer.last_families = np.zeros(len(observer.last_bits), dtype=int)
plot_run(observer, config, run)
(run / "plot_repair.json").write_text(json.dumps({
    "reason": "Original rendering supported two colors; cap is a third recognition species. Numerical results were already saved.",
    "postprocessor_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "plotter_sha256": hashlib.sha256((ROOT / "experiments/run_local_research.py").read_bytes()).hexdigest(),
    "dynamics_rerun": False}, indent=2), encoding="utf-8")
print("Plot repaired from saved numerical data; dynamics unchanged")
