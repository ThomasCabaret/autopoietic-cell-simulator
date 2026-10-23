"""Formal material/catalytic audit of candidate cell designs; not particle dynamics.

Named tools below are abstract functional roles, NOT particle types or a sequence
lookup table for the molecular simulator. Their physical realization is assumed.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FOOD = {"X", "Y", "Z", "fuel*"}


def add_mass(*terms):
    out = [0, 0, 0, 0]
    for count, mass in terms:
        out = [a + count * b for a, b in zip(out, mass)]
    return out


def build(name, one_family=False, promiscuous=False):
    masses = {"X": [1, 0, 0, 0], "Y": [0, 1, 0, 0], "Z": [0, 0, 1, 0],
              "fuel*": [0, 0, 0, 1], "waste": [0, 0, 0, 1], "M": [2, 0, 0, 0]}
    for atom in "XYZ":
        masses[atom + "*"] = masses[atom]
    families = ["R"] if one_family else ["G", "F"]
    for family in families:
        masses[family + "0"], masses[family + "1"] = [1, 1, 0, 0], [1, 0, 1, 0]
    roles = {"A": "001011", "R": "010010", "M": "011001"} if one_family else (
        {"A": "001011", "S": "010010"} if promiscuous else
        {"A": "001011", "G": "010010", "F": "101100", "M": "011001"})
    genes = {role: ("r" if one_family else "g") + role for role in roles}
    tools = {role: genes[role] if one_family else "p" + role for role in roles}
    information = "R" if one_family else "G"
    for role, seq in roles.items():
        masses[genes[role]] = add_mass((seq.count("0"), masses[information + "0"]),
                                      (seq.count("1"), masses[information + "1"]))
        masses[tools[role]] = masses[genes[role]]
    reactions = []

    def reaction(rid, reactants, products, catalysts, assumption):
        reactions.append({"id": rid, "reactants": reactants, "products": products,
                          "catalysts": catalysts, "physical_function_assumed": assumption})

    for atom in "XYZ":
        reaction("activate_" + atom, {atom: 1, "fuel*": 1}, {atom + "*": 1, "waste": 1},
                 [tools["A"]], "Sequence-defined aggregate activates generic food modules using external fuel")
    for family in families:
        assembler = tools["R"] if one_family else tools["S"] if promiscuous else tools[family]
        for bit, atom in [("0", "Y"), ("1", "Z")]:
            reaction("assemble_" + family + bit, {"X*": 1, atom + "*": 1}, {family + bit: 1},
                     [assembler], "Aggregate builds a chemically configured composite monomer from activated modules")
    reaction("assemble_M", {"X*": 2}, {"M": 1}, [tools["S"] if promiscuous else tools["M"]],
             "Aggregate builds a membrane unit; insertion and compartment function remain separate obligations")
    for role, seq in roles.items():
        reaction("copy_" + role, {information + "0": seq.count("0"), information + "1": seq.count("1")},
                 {genes[role]: 1}, [genes[role]], "Macro-description of bounded local copying; no whole-chain rule in the particle engine")
        if not one_family:
            reaction("express_" + role, {"F0": seq.count("0"), "F1": seq.count("1")},
                     {tools[role]: 1}, [genes[role]], "Expression yields this functional conformation; its catalytic activity is an unproved hypothesis")
    essentials = sorted(set(genes.values()) | set(tools.values()) | {"M"} |
                        {f + b for f in families for b in "01"})
    return {"id": name, "masses_XYZ_carrier": masses, "reactions": reactions,
            "genes": genes, "tools": tools, "sequences": roles, "families": families,
            "food": sorted(FOOD), "seeds": sorted(set(genes.values()) | set(tools.values())),
            "essential_species": essentials,
            "unproved_assumptions": [
                "Each named catalytic function is realized by a sequence-derived conformation, not by a new particle type",
                "Assembly produces the required bond states/ports from raw modules",
                "Fuel and waste can cross the compartment appropriately",
                "Copying/expression and functional folding are compatible in one bath",
                "Membrane production actually permits insertion, retention and continued renewal"] +
                (["One sequence-derived assembler supports G, F and M construction without uncontrolled cross-reactions"] if promiscuous else []) +
                (["The same RNA-like chain can alternate functional folding and templating without destructive competition"] if one_family else [])}


def reachable(model, seeds=True):
    available = set(model["food"]) | (set(model["seeds"]) if seeds else set())
    produced, enabled = set(), set()
    while True:
        old = set(available)
        for r in model["reactions"]:
            if set(r["reactants"]) | set(r["catalysts"]) <= available:
                enabled.add(r["id"])
                produced.update(r["products"])
                available.update(r["products"])
        if available == old:
            return produced, enabled


def audit(model):
    masses = model["masses_XYZ_carrier"]
    unbalanced = []
    for r in model["reactions"]:
        left = add_mass(*[(count, masses[s]) for s, count in r["reactants"].items()])
        right = add_mass(*[(count, masses[s]) for s, count in r["products"].items()])
        if left != right:
            unbalanced.append(r["id"])
    produced, enabled = reachable(model)
    missing = sorted(set(model["essential_species"]) - produced)
    catalysts = {s for r in model["reactions"] for s in r["catalysts"]}
    hidden = sorted(catalysts - produced - FOOD)
    forbidden = sorted(set(model["food"]) - FOOD)
    return {"formally_closed": not (unbalanced or missing or hidden or forbidden),
            "unbalanced_reactions": unbalanced, "not_regenerated": missing,
            "external_or_nonregenerated_catalysts": hidden, "forbidden_premade_food": forbidden,
            "enabled_reactions": sorted(enabled),
            "food_only_produces_tools": bool(set(model["tools"].values()) & reachable(model, seeds=False)[0]),
            "meaning": "Material consistency and conditional regenerability with constructed initial seeds; no kinetics, geometry, turnover or biological viability proven"}


def replacement_flux(model):
    # Explicit constructive stoichiometric budget: one new gene, one new tool,
    # one membrane unit. In a one-family design gene and tool are the same object.
    reactions = {r["id"]: r for r in model["reactions"]}
    flux = Counter({rid: 1 for rid in reactions if rid.startswith(("copy_", "express_"))})
    flux["assemble_M"] = 1
    demand = Counter()
    for rid, amount in list(flux.items()):
        demand.update({s: count * amount for s, count in reactions[rid]["reactants"].items()})
    for family in model["families"]:
        for bit in "01":
            flux["assemble_" + family + bit] = demand[family + bit]
    active_demand = Counter()
    for rid, amount in flux.items():
        active_demand.update({s: count * amount for s, count in reactions[rid]["reactants"].items() if s.endswith("*")})
    for atom in "XYZ":
        flux["activate_" + atom] = active_demand[atom + "*"]
    net = Counter()
    for rid, amount in flux.items():
        for s, count in reactions[rid]["products"].items():
            net[s] += count * amount
        for s, count in reactions[rid]["reactants"].items():
            net[s] -= count * amount
    expected = set(model["genes"].values()) | set(model["tools"].values()) | {"M"}
    assert all(net[s] == 1 for s in expected)
    assert all(v == 0 or s in expected | FOOD | {"waste"} for s, v in net.items())
    return {"reaction_flux": dict(flux), "food_consumed": {s: -net[s] for s in sorted(FOOD)},
            "new_material": {s: net[s] for s in sorted(expected)}, "waste_export": net["waste"],
            "scope": "One formal replacement batch at arbitrarily chosen six-symbol tool sequences; not an optimized or kinetic rate"}


def negative_controls(model):
    results = {}
    for tool in sorted(set(model["tools"].values())):
        broken = {**model, "reactions": [r for r in model["reactions"] if tool not in r["products"]]}
        result = audit(broken)
        assert not result["formally_closed"] and tool in result["not_regenerated"]
        results["remove_producer_" + tool] = result
    wrong = json.loads(json.dumps(model))
    rid = next(r for r in wrong["reactions"] if r["id"].startswith("assemble_") and "Y*" in r["reactants"])
    rid["reactants"] = {"X*": 1, "Z*": 1}
    result = audit(wrong)
    assert rid["id"] in result["unbalanced_reactions"]
    results["wrong_elemental_substrate"] = result
    premade = {**model, "food": model["food"] + [model["families"][0] + "0"]}
    result = audit(premade)
    assert result["forbidden_premade_food"]
    results["hidden_premade_feed"] = result
    return results


def main():
    models = [build("two_families_specialized"), build("two_families_promiscuous", promiscuous=True),
              build("one_family_RNA_like", one_family=True)]
    records = []
    for model in models:
        result = audit(model)
        assert result["formally_closed"]
        records.append({"model": model, "audit": result, "replacement_flux": replacement_flux(model),
                        "negative_controls": negative_controls(model)})
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out = ROOT / "research/abstract_runs" / ("C0_" + stamp)
    out.mkdir(parents=True)
    source = Path(__file__).read_bytes()
    (out / Path(__file__).name).write_bytes(source)
    evidence = {"branch": "C0", "kind": "formal_design_audit_not_molecular_simulation",
                "source_sha256": hashlib.sha256(source).hexdigest(), "models": records}
    (out / "result.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(json.dumps({"run": out.relative_to(ROOT).as_posix(), "models": [
        {"id": r["model"]["id"], "formally_closed": r["audit"]["formally_closed"],
         "tool_roles": len(r["model"]["tools"]), "fuel_for_one_replacement_batch": r["replacement_flux"]["food_consumed"]["fuel*"]}
        for r in records]}, indent=2))


if __name__ == "__main__":
    main()
