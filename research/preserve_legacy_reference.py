"""Preserve the selected temporary source reference, without executing it."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "temp"
DEST = ROOT / "research/legacy_reference"
selected = sorted((SOURCE / "src").glob("*.cpp")) + [SOURCE / name for name in (
    "README.md", "PATCHY_PARTICLES.md", "TEMPLATE_COPY_DEMO.md",
    "TEMPLATE_COPY_BENCHMARK.md", "WINDOWS_BUILD.md", "CMakeLists.txt",
    "CMakePresets.json", "vcpkg.json", "LICENSE",
    "life-emergence-patchy-particles.patch")]
records = []
for source in selected:
    relative = source.relative_to(SOURCE)
    target = DEST / "source" / relative
    if target.exists():
        if target.read_bytes() != source.read_bytes():
            raise FileExistsError(f"Refusing to replace a different archived file: {target}")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    records.append({"original_path": source.relative_to(ROOT).as_posix(),
                    "preserved_path": target.relative_to(ROOT).as_posix(),
                    "bytes": source.stat().st_size,
                    "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})

# Keep the observed parameter set, not the 2,372 particle records or RNG dump.
checkpoint = SOURCE / "particle_life.checkpoint"
parameters = {}
for line in checkpoint.read_text(encoding="utf-8").splitlines():
    key, _, value = line.partition(" ")
    if key == "particles":
        parameters["observed_particle_count"] = int(value)
        break
    if key == "rng_state":
        continue
    try:
        parameters[key] = json.loads(value)
    except json.JSONDecodeError:
        parameters[key] = value
parameters["source_sha256"] = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
parameters["scope"] = "Observed checkpoint parameters only; neither a particle snapshot nor a calibrated/default parameter set"
(DEST / "observed_checkpoint_parameters.json").write_text(json.dumps(parameters, indent=2), encoding="utf-8")
manifest = {"captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_directory": "temp", "scope": "Selected unmodified reference sources; not integrated or executed",
            "files": records,
            "not_present_in_supplied_tree": ["include/particle_life", "scripts", "external/vcpkg"],
            "not_copied": ["particle_life.checkpoint (parameters extracted separately)",
                           "smoke-test.csv", "imgui.ini", ".gitignore", ".gitmodules", "APPLY_PATCH_WINDOWS.md"],
            "build_status": "Not attempted: public headers are missing; patch contains partial header diffs only",
            "license": "Original MIT LICENSE preserved with source"}
(DEST / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps({"preserved_files": len(records), "preserved_source_bytes": sum(r["bytes"] for r in records),
                  "archive": str(DEST.relative_to(ROOT)), "temporary_source_modified": False}))
