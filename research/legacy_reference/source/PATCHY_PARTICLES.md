# Patch-particle demonstrator

This patch adds a new particle type, `P`, without changing the legacy `S`
surfactant model.

A `P` particle has one saturable left site and one saturable right site. A right
site can bind only a free left site on a nearby `P` particle. Existing bonds are
stored by stable particle identifier, while the spatial grid is used only to
find new local contacts and non-bonded repulsion contacts.

The model has no vesicle identifier, no loop detector, no inside/outside test
and no target global shape. Chains and closed loops can only result from local
association, local bond mechanics and a preferred turn angle between adjacent
monomers.

## First interactive test

1. Select `Closed reflecting box` or `Periodic wrap` as the boundary mode.
2. Clear the world with `R`.
3. Open `Patch monomers P` and click `Spawn P batch`. A few hundred particles
   are enough for a first test; a denser population associates faster.
4. Let the simulation run and inspect the bond count and the blue bond lines.
5. Raise `P temperature` to several units to agitate the particles and increase
   thermal dissociation.
6. While the material is dissociated, change `P preferred turn angle`.
7. Lower `P temperature` again and observe the new assembly regime.

The `P` key spawns one patch monomer. The click source can also be changed to
`P - patch monomer` in the GUI.

## Main controls

- `P preferred turn angle`: local angular increment along a chain. Larger
  absolute values generally favor smaller closed loops. Reversing the sign
  reverses the preferred curvature orientation.
- `P bond length`: preferred distance between adjacent monomer centers.
- `P capture radius`: maximum mismatch between two free patch positions when a
  bond is created.
- `P capture angle`: angular tolerance for association.
- `P bond stiffness`: translational spring stiffness of an existing bond.
- `P bending stiffness`: strength with which a bond approaches the preferred
  turn angle.
- `P bond damping`: relative linear and angular damping across a bond.
- `P break distance`: site separation at which a bond breaks mechanically.
- `P break angle`: angular error at which a bond breaks mechanically.
- `P core repulsion radius/strength`: non-bonded exclusion between patch
  particles. Saturated membranes therefore do not acquire arbitrary extra
  neighbors when they touch.
- `P temperature`: random force and torque applied to patch particles.
- `P thermal break rate`: how strongly temperature causes stochastic bond
  dissociation.

`Break all P bonds` provides an immediate manual reset. `Reset P defaults`
restores the demonstrator values.

## Boundary modes

- `Legacy soft containment`: preserves the historical containing-force model.
- `Destroy outside`: preserves the former open/destructive boundary behavior.
- `Closed reflecting box`: particles reflect from the walls.
- `Periodic wrap`: positions and interactions use periodic minimum-image
  geometry. The spatial grid also searches across periodic seams.

## Scope of the demonstrator

The initial values are only a usable exploration point, not calibrated physical
constants. They produce reversible polymers and can produce closed cycles, but
the exact yield depends strongly on density, integration settings and annealing
history. The point of the GUI is to locate useful regimes before deciding which
parts of the model deserve a more formal treatment.

Nesting is permitted by the local rules because a monomer whose left and right
sites are occupied cannot bind a third membrane. This patch does not add a
special nesting detector or guarantee that nested loops will arise frequently
from a random initial state.

Checkpoint format version 2 stores particle identifiers, patch bonds, patch
parameters and boundary mode. Version 1 checkpoints from the clean refactor are
still accepted; their particles are assigned identifiers when loaded.
