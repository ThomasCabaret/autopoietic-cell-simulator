"""Static screening of composite particles; NOT an assembly dynamics simulator.

Run: python experiments/composite_geometry.py
Requires numpy and matplotlib. All energies are in kT and lengths in bead diameters.
Rigid configurations are a sampling approximation to strongly bonded scaffolds.
No aggregate-dependent force or reaction is used. No kinetic claim is made.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np


OUT = Path(__file__).resolve().parent / "results"
EPSILON = 2.5
WIDTH = 0.12
CORE = 1.0
CUTOFF = 1.5
# One fixed microscopic compatibility table throughout both experiments.
# N is inert, A and B attract; identical species never attract.
AFFINITY = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=float)
COLORS = ["#aeb9c6", "#168c99", "#df7947"]


def rotation(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s], [s, c]])


def scaffold(turn_degrees=0):
    """Nine preconstructed beads. Wedge changes positions, not bead types/laws."""
    t = np.tan(np.deg2rad(turn_degrees) / 2)
    points, types = [], []
    for y in (-1.2, 0.0, 1.2):
        for col in (-1, 0, 1):
            points.append([col * (1.6 - t * y), y])
            types.append(1 if col == -1 and y != 0 else
                         2 if col == 1 and y != 0 else 0)
    return np.array(points), np.array(types)


def cross_energy(moving, moving_types, fixed, fixed_types):
    """Sum isotropic bead-pair potentials, vectorized over poses.

    Hard disks: U=inf for r<1. A-B: -epsilon*exp(-((r-1)/width)^2)
    within cutoff; all other nonoverlapping pairs have zero energy.
    """
    distances = np.linalg.norm(moving[..., :, None, :] - fixed, axis=-1)
    compatible = AFFINITY[moving_types[:, None], fixed_types[None, :]]
    attraction = -EPSILON * np.exp(-((distances - CORE) / WIDTH) ** 2)
    energies = np.sum(np.where(distances <= CUTOFF, attraction, 0) * compatible,
                      axis=(-2, -1))
    return np.where(np.any(distances < CORE - 1e-9, axis=(-2, -1)),
                    np.inf, energies)


def docking_scan(points, types):
    """Translation and rotation grid on one side of a reference scaffold.

    This is a minimum-energy envelope, not an orientational free energy.
    It does NOT integrate translational entropy or include many-body competitors.
    """
    angles = np.arange(-90, 91, 1)
    gx = np.arange(2.60, 5.001, 0.04)
    gy = np.arange(-3.0, 3.001, 0.04)
    xx, yy = np.meshgrid(gx, gy)
    translations = np.column_stack([xx.ravel(), yy.ravel()])
    energies, poses = [], []
    for angle in angles:
        moved = points @ rotation(np.deg2rad(angle)).T
        candidates = moved[None, :, :] + translations[:, None, :]
        e = cross_energy(candidates, types, points, types)
        best = np.argmin(e)
        energies.append(float(e[best]))
        poses.append(translations[best].tolist())
    best = int(np.argmin(energies))
    return {"angles_deg": angles.tolist(), "minimum_energy_kT": energies,
            "best_angle_deg": int(angles[best]), "best_energy_kT": energies[best],
            "best_translation": poses[best],
            "translation_step": 0.04, "angle_step_deg": 1,
            "scope": "minimum over sampled right-side translations; no kinetics/free energy"}


def ideal_neighbor(points, turn_degrees):
    """A constructed matched-face pose, only used to illustrate a candidate chain."""
    a = np.deg2rad(turn_degrees)
    n = np.array([np.cos(a / 2), np.sin(a / 2)])
    translation = np.array([1.6, 0]) + n - rotation(a) @ np.array([-1.6, 0])
    return points @ rotation(a).T + translation, translation


def draw_beads(ax, points, types, alpha=1):
    for point, bead_type in zip(points, types):
        ax.add_patch(Circle(point, .5, facecolor=COLORS[bead_type],
                            edgecolor="white", linewidth=.7, alpha=alpha))
    ax.set_aspect("equal")


def weighted_pair_probability(points, types, spacing):
    """Equilibrium quadrature for two identical B substrates in a finite box.

    No reaction is simulated. The 'reactive' window is purely a distance test.
    Each B feels the sum of the same bead pair interactions with the scaffold.
    B-B only have hard-core exclusion. FFT performs the 4D pair integral.
    """
    # Fixed domain and volume in all controls; scaffold exclusion is included.
    xs = np.arange(-4.8, 4.80001, spacing)
    ys = np.arange(-4.8, 4.80001, spacing)
    xx, yy = np.meshgrid(xs, ys)
    grid = np.stack([xx, yy], axis=-1)
    if len(points):
        e = cross_energy(grid[..., None, :], np.array([2]), points, types)
    else:
        e = np.zeros_like(xx)
    weights = np.exp(-e)
    weights /= weights.sum()
    ny, nx = weights.shape
    # Linear (zero-padded), not periodic, autocorrelation.
    shape = (2 * ny - 1, 2 * nx - 1)
    ft = np.fft.rfftn(weights, s=shape, axes=(0, 1))
    corr = np.fft.fftshift(np.fft.irfftn(ft * ft.conj(), s=shape, axes=(0, 1)))
    dx = np.arange(-(nx - 1), nx) * spacing
    dy = np.arange(-(ny - 1), ny) * spacing
    r = np.hypot(dx[None, :], dy[:, None])
    allowed = r >= 1 - 1e-9
    reactive = allowed & (r <= 1.2 + 1e-9)
    normalization = float(corr[allowed].sum())
    return {"p_contact": float(corr[reactive].sum() / normalization),
            "allowed_pair_weight": normalization,
            "grid_spacing": spacing,
            "domain": [-4.8, 4.8, -4.8, 4.8],
            "reactive_distance_interval": [1, 1.2]}


def substrate_controls():
    points, _ = scaffold(0)
    # All nonempty controls have the SAME 9 positions and SAME composition: 2A+7N.
    # Only the placement of A among those positions changes.
    definitions = {"adjacent_top": (6, 7), "separated_top": (6, 8),
                   "opposite_faces": (1, 7)}
    controls = {}
    for name, indices in definitions.items():
        types = np.zeros(9, dtype=int)
        types[list(indices)] = 1
        controls[name] = (points, types)
    controls["inert_scaffold"] = (points, np.zeros(9, dtype=int))
    controls["empty_box"] = (np.empty((0, 2)), np.empty(0, dtype=int))
    return controls


def pocket_scaffold(separation):
    """Three A beads and two inert backstops; two exposed double-contact pockets.

    Geometry is prescribed, NOT obtained by folding or relaxation. All compared
    spacings have the same composition. No special 'pocket' force is introduced.
    """
    s = separation
    return (np.array([[-s, 0], [0, 0], [s, 0], [-s / 2, -.9], [s / 2, -.9]]),
            np.array([1, 1, 1, 0, 0]))


def numerical_checks():
    # Independent checks of hard core, compatibility, pair symmetry and zero-padding.
    a, b = np.array([[0., 0.]]), np.array([[1., 0.]])
    assert np.isclose(cross_energy(a, np.array([1]), b, np.array([2])), -EPSILON)
    assert np.isclose(cross_energy(a, np.array([1]), b, np.array([1])), 0)
    assert np.isinf(cross_energy(a, np.array([1]), .9 * b, np.array([2])))
    p, t = scaffold(30)
    q, _ = ideal_neighbor(p, 30)
    e = cross_energy(q, t, p, t)
    assert np.isclose(e, cross_energy(p, t, q, t))
    assert np.isclose(e, -2 * EPSILON)
    # Compare FFT contact probability with an explicit pair sum on a tiny grid.
    w = np.array([[.1, .2, .1], [.05, .3, .25]])
    shape = (3, 5)
    ft = np.fft.rfftn(w, s=shape, axes=(0, 1))
    corr = np.fft.fftshift(np.fft.irfftn(ft * ft.conj(), s=shape, axes=(0, 1)))
    kernel = np.hypot(np.arange(-2, 3)[None, :], np.arange(-1, 2)[:, None]) <= 1
    yy, xx = np.indices(w.shape)
    coords = np.column_stack([yy.ravel(), xx.ravel()])
    dist = np.linalg.norm(coords[:, None] - coords[None, :], axis=-1)
    direct = np.sum(w.ravel()[:, None] * w.ravel()[None, :] * (dist <= 1))
    assert np.isclose(corr[kernel].sum(), direct)


def main():
    global EPSILON
    OUT.mkdir(parents=True, exist_ok=True)
    numerical_checks()
    dock = {}
    for turn in (0, 30):
        points, types = scaffold(turn)
        dock[str(turn)] = docking_scan(points, types)
    controls = substrate_controls()
    contact = {}
    for name, (points, types) in controls.items():
        contact[name] = [weighted_pair_probability(points, types, h)
                         for h in (.08, .04)]
    for name, results in contact.items():
        for i, result in enumerate(results):
            result["relative_to_empty_box"] = result["p_contact"] / contact["empty_box"][i]["p_contact"]
            result["relative_to_inert_scaffold"] = result["p_contact"] / contact["inert_scaffold"][i]["p_contact"]

    # Explicit parameter sweep: every force uses the SAME epsilon at each setting.
    # This is not a stronger interaction applied selectively to an 'enzyme'.
    base_epsilon = EPSILON
    pockets = {}
    for epsilon in (2.5, 4., 5., 6.):
        EPSILON = epsilon
        pockets[str(epsilon)] = {}
        for separation in (1.1, 1.6):
            p, t = pocket_scaffold(separation)
            pockets[str(epsilon)][str(separation)] = [
                weighted_pair_probability(p, t, h) for h in (.04, .02, .01, .005)]
    EPSILON = base_epsilon
    pocket_empty_reference = weighted_pair_probability(
        np.empty((0, 2)), np.empty(0, dtype=int), .005)

    # A concrete failure of strict effective valence: a third aggregate can
    # attach to an already occupied corner. Pair attraction is NOT saturable.
    p, t = scaffold(0)
    q, _ = ideal_neighbor(p, 0)
    branch = p + np.array([3.2, 3.4])
    branch_energies = {"central_neighbor": float(cross_energy(q, t, p, t)),
                       "central_branch": float(cross_energy(branch, t, p, t)),
                       "neighbor_branch": float(cross_energy(branch, t, q, t))}

    data = {"model": {"epsilon_kT": EPSILON, "width": WIDTH, "diameter": CORE,
                       "cutoff": CUTOFF, "affinity": AFFINITY.tolist(),
                       "species_order": ["N", "A", "B"]},
            "docking": dock, "contact_probability": contact,
            "double_contact_pockets": pockets,
            "pocket_empty_reference": pocket_empty_reference,
            "branch_counterexample_pair_energies_kT": branch_energies,
            "limitations": ["Rigid preconstructed scaffolds, no folding or synthesis",
                            "Energy scan is not Brownian self-assembly",
                            "Contact probability is not a catalytic turnover rate",
                            "Isotropic attractions do not guarantee saturable aggregate valence",
                            "No product formation, release, energy flux or membrane",
                            "Finite box equilibrium quadrature, no claim of completeness"]}
    (OUT / "screening.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    for turn, color in [(0, "#168c99"), (30, "#df7947")]:
        ax = axes[0, 0 if turn == 0 else 1]
        p, t = scaffold(turn)
        q, _ = ideal_neighbor(p, turn)
        draw_beads(ax, p, t)
        draw_beads(ax, q, t)
        ax.set_xlim(-2.5, 6.8)
        ax.set_ylim(-2.2, 3.8)
        ax.set_title(f"Deux agregats construits : geometrie {turn} deg")
        ax.axis("off")
        ax.text(0, -.05, "A : turquoise | B : orange | N : gris\nPose construite ; pas une trajectoire d'assemblage",
                transform=ax.transAxes, fontsize=9)
        curve = dock[str(turn)]
        axes[1, 0].plot(curve["angles_deg"], curve["minimum_energy_kT"],
                        color=color, label=f"Geometrie {turn} deg")
    axes[1, 0].axhline(-EPSILON, ls=":", color="#626e7a", label="Un contact A-B optimal")
    axes[1, 0].set(xlabel="Rotation relative (degres)", ylabel="Energie minimale echantillonnee (kT)",
                    title="L'orientation preferee depend de l'agregat")
    axes[1, 0].legend(fontsize=9)
    names = list(controls)
    values = [contact[name][-1]["relative_to_empty_box"] for name in names]
    labels = ["2 sites\nvoisins", "2 sites\necartes", "2 sites\nopposes", "Support\ninerte", "Boite\nvide"]
    axes[1, 1].bar(labels, values, color=["#168c99", "#55acb4", "#df7947", "#aeb9c6", "#d6dce2"])
    axes[1, 1].axhline(1, color="#626e7a", ls=":")
    axes[1, 1].set(ylabel="P(contact) / P(contact dans la boite vide)",
                    title="Disposition des sites -> rencontre des substrats")
    for i, value in enumerate(values):
        axes[1, 1].text(i, value + .02, f"{value:.2f}", ha="center", fontsize=9)
    fig.suptitle("Criblage statique d'une chimie de particules composites\nMemes interactions isotropes A-B ; aucune regle d'enzyme ou de chaine", fontsize=14)
    fig.savefig(OUT / "geometry_screening.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 4, figsize=(12, 3.8), constrained_layout=True)
    for ax, name in zip(axes, list(controls)[:4]):
        points, types = controls[name]
        draw_beads(ax, points, types)
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.1, 2.4)
        ax.set_title(name.replace("_", " "))
        ax.axis("off")
    fig.suptitle("Controles : memes positions ; trois dispositions de 2 sites A parmi 9 billes")
    fig.savefig(OUT / "substrate_controls.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), constrained_layout=True)
    for ax, s in zip(axes[:2], (1.1, 1.6)):
        p, t = pocket_scaffold(s)
        draw_beads(ax, p, t)
        # Constructed illustrative substrate positions, NOT sampled trajectories.
        height = np.sqrt(1 - (s / 2) ** 2)
        draw_beads(ax, np.array([[-s / 2, height], [s / 2, height]]), np.array([2, 2]), .8)
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-1.7, 2.3)
        ax.set_title(f"Poches distantes de {s} diametre")
        ax.axis("off")
    ax = axes[2]
    for s, color in [(1.1, "#168c99"), (1.6, "#df7947")]:
        xs = [float(e) for e in pockets]
        ys = [pockets[e][str(s)][-1]["p_contact"] / pocket_empty_reference["p_contact"]
              for e in pockets]
        ax.plot(xs, ys, "o-", color=color, label=f"Espacement {s}")
    ax.axhline(1, color="#626e7a", ls=":")
    ax.set(xlabel="Attraction elementaire epsilon (kT)",
           ylabel="P(contact) / P(contact boite vide)", title="Effet de la geometrie et de l'affinite")
    ax.legend()
    fig.suptitle("Plusieurs contacts par substrat : un prealable possible a la catalyse\nScaffolds fixes ; calcul d'equilibre ; aucune reaction ni liberation de produit")
    fig.savefig(OUT / "pocket_screening.png", dpi=160)
    plt.close(fig)
    summary = {"docking": {k: {s: v[s] for s in ("best_angle_deg", "best_energy_kT")}
                            for k, v in dock.items()},
               "contact": {k: {"p": v[-1]["p_contact"],
                                "vs_empty": v[-1]["relative_to_empty_box"],
                                "vs_inert": v[-1]["relative_to_inert_scaffold"],
                                "coarse_vs_fine_relative_difference": abs(v[0]["p_contact"] / v[-1]["p_contact"] - 1)}
                           for k, v in contact.items()},
               "pockets": {e: {s: {"p": v[-1]["p_contact"],
                                     "last_refinement_relative_difference": abs(v[-2]["p_contact"] / v[-1]["p_contact"] - 1),
                                     "vs_empty": v[-1]["p_contact"] / pocket_empty_reference["p_contact"]}
                               for s, v in layouts.items()} for e, layouts in pockets.items()},
               "branch_counterexample_pair_energies_kT": branch_energies}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
