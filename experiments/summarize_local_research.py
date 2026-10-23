"""Build a read-only evidence index from all completed and interrupted runs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rows = []
for path in sorted((ROOT / "research/runs").glob("*/result.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    c, m = data["config"], data.get("metrics", {})
    rows.append({"case": c["case"], "seed": c["seed"], "duration": c.get("duration"),
                 "path": path.relative_to(ROOT).as_posix(), "error": data.get("error"),
                 "mode": c["mode"], "branch": c["branch"],
                 "complete": m.get("complete_copy_sets_ever"),
                 "detached": m.get("detached_copy_sets_ever"),
                 "copy_source_events": m.get("ligations_using_complete_copies"),
                 "closed": m.get("closed_sets_ever"),
                 "final_closed": m.get("final_closed"),
                 "largest_component": m.get("final_largest_component"),
                 "best_fragment": m.get("best_matching_fragment"),
                 "translated": m.get("translated_chains_ever"),
                 "translated_detached": m.get("translated_detached_ever"),
                 "certified_max_generation": m.get("certified_max_generation"),
                 "certified_detached_generation2": m.get("certified_detached_generation2"),
                 "code_sha256": data.get("source_sha256")})
(ROOT / "research/run_index.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
lines = ["# Registre des exécutions", "", "Les comptes sont des observations de ces essais, sans estimation générale de taux de réussite.",
         "Les conditions initiales et versions du code se lisent dans chaque résultat.", "",
         "| Cas | Graine | Durée | Copies complètes / libérées | Traductions complètes / libérées | Génération certifiée max. | Boucles observées | Preuve |",
         "| --- | ---: | ---: | --- | --- | ---: | ---: | --- |"]
for r in rows:
    link = r["path"].removeprefix("research/")
    if r["error"]:
        lines.append(f"| {r['case']} | {r['seed']} | {r['duration']} | Incident technique | — | — | — | [Détails]({link}) |")
    else:
        copy = f"{r['complete']} / {r['detached']}" if r["mode"] == "copy" else "—"
        closed = r["closed"] if r["closed"] is not None else "—"
        translated = f"{r['translated']} / {r['translated_detached']}" if r["translated"] is not None else "non mesuré"
        generation = r["certified_max_generation"] if r["certified_max_generation"] is not None else "non mesuré"
        lines.append(f"| {r['case']} | {r['seed']} | {r['duration']} | {copy} | {translated} | {generation} | {closed} | [Données]({link}) |")
(ROOT / "research/RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"registered_runs": len(rows), "technical_incidents": sum(bool(r["error"]) for r in rows),
                  "copy_runs": sum(r["mode"] == "copy" and not r["error"] for r in rows),
                  "membrane_runs": sum(r["mode"] == "vesicle" and not r["error"] for r in rows)}))
