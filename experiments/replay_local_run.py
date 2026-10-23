"""Replay archived sources without overwriting any original result or trajectory."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def replay(folder):
    folder = Path(folder).resolve()
    evidence = json.loads((folder / "result.json").read_text(encoding="utf-8"))
    if evidence.get("error"):
        raise ValueError("This run recorded a technical incident, not a successful simulation")
    for name, expected in evidence["source_sha256"].items():
        if hashlib.sha256((folder / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Archived source hash mismatch: {name}")
    if evidence.get('format_version') == 2:
        import subprocess
        subprocess.run([sys.executable,str(folder/'replay.py')],cwd=folder,check=True)
        return
    dynamics = load("local_dynamics", folder / "local_dynamics.py")
    analysis = load("archived_analysis", folder / "run_local_research.py")
    config = evidence["config"]
    observer = analysis.CopyObserver(config) if config["mode"] == "copy" else analysis.VesicleObserver(config)
    (dynamics.copying if config["mode"] == "copy" else dynamics.vesicle)(config, config["seed"], observer)
    actual = observer.summary()
    # Compare the actual recorded metrics, not just an expected pass/fail flag.
    matches = json.dumps(actual, sort_keys=True) == json.dumps(evidence["metrics"], sort_keys=True)
    print(json.dumps({"archived_metrics_reproduced": matches,
                      "summary": {k: v for k, v in actual.items() if k not in ("history", "events")}}, indent=2))
    if not matches:
        raise AssertionError("Replay differs from archived observations")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    replay(parser.parse_args().folder)
