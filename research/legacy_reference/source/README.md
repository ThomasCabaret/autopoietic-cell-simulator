# Life Emergence

Life Emergence is a minimalist two-dimensional artificial-life simulation in which local particle interactions can produce autopoietic vesicles able to form, grow, repair, and divide.

The model is deliberately abstract. It is not intended to reproduce a specific real chemistry; it is a computational proof of concept for studying how compartmentalization, autocatalytic reactions, and local mechanics can combine into life-like dynamics.

## Relationship to the original project

This repository is the cleaned and modular continuation of the original [SimulationSkeleton](https://github.com/ThomasCabaret/SimulationSkeleton) project.

The original research prototype concentrated the simulation, rendering, controls, and experiment logic in a single `main.cpp`. That version demonstrated the scientific idea and produced the results described in the publication, but it was difficult to scale, test, or run reproducibly.

Life Emergence keeps the same current particle model and parameterization as closely as practical while reorganizing the software around a reusable simulation core. The executable is still named `ParticleLife` for compatibility with the previous project.

## Scientific model

The current implementation contains five particle types:

- `F`: precursor or food particle
- `A`: catalyst
- `B`: intermediary reactant
- `S`: polar surfactant particle forming membranes
- `L`: experimental reaction limiter

The core autocatalytic chemistry is based on two local reactions:

1. A precursor is converted into an intermediary in the presence of a catalyst.
2. A precursor and an intermediary are converted into a catalyst and a surfactant.

Surfactant particles have position, velocity, orientation, and angular velocity. Their anisotropic local interaction favors slightly curved side-by-side aggregates. These aggregates can close into vesicles. Vesicles containing a suitable internal reaction set can consume incoming precursors, produce new surfactants, grow, become mechanically unstable, divide, and repair the resulting daughter membranes.

The current simulator intentionally preserves several prototype semantics, including immediate first-eligible reaction ordering and the existing Brownian-motion scaling. These aspects may be revised later, but they are not changed as part of this cleanup.

## Main changes from SimulationSkeleton

- The single source file was split into a small set of focused headers and source files.
- The simulation core no longer depends on SFML or ImGui.
- Particles are stored contiguously in `std::vector<Particle>`.
- A uniform spatial grid reduces local-neighbor searches from an all-pairs scan in normal operation.
- The original brute-force neighbor search remains available as a reference mode.
- A regression executable compares the spatial grid against brute force for 2,000 deterministic steps, including particles placed on positive and negative cell boundaries.
- Random seeds are explicit and reproducible.
- The simulator can run interactively or without a graphical interface.
- Checkpoints store the simulation parameters, particles, step index, seed, and full pseudo-random generator state.
- CSV metrics can be generated during interactive or headless runs.
- CMake presets provide a straightforward Windows command-line build while the regular generator-independent CMake workflow remains supported.

## Repository layout

```text
include/particle_life/
    Public simulation interfaces

src/simulation.cpp
    Particle dynamics, local chemistry, and integration

src/spatial_grid.cpp
    Uniform-grid neighbor acceleration structure

src/interactive_main.cpp
    SFML and Dear ImGui interactive viewer

src/headless_main.cpp
    Deterministic command-line runner

src/spatial_grid_regression_main.cpp
    Spatial-grid versus brute-force regression test

scripts/
    PowerShell helpers for vcpkg, build, and execution
```

## Windows requirements

A full Visual Studio IDE is not required. The supported lightweight command-line setup is:

- Git
- CMake 3.24 or newer
- Visual Studio 2022 Build Tools
- MSVC x64/x86 C++ build tools
- A Windows 10 or Windows 11 SDK

SFML, Dear ImGui, and ImGui-SFML are installed through the repository vcpkg submodule and `vcpkg.json` manifest.

## Clone

```powershell
git clone --recursive https://github.com/ThomasCabaret/life-emergence.git
cd life-emergence
```

When updating an existing clone, also update submodules:

```powershell
git pull --recurse-submodules
git submodule update --init --recursive
```

## Configure, build, test, and run on Windows

From the repository root in PowerShell:

```powershell
.\scripts\bootstrap-vcpkg.ps1
cmake --preset windows-msvc-x64
cmake --build --preset windows-release
ctest --preset windows-release
.\build\windows-msvc-x64\Release\ParticleLife.exe --seed 5489
```

The first CMake configuration installs the dependencies declared in `vcpkg.json` and may take several minutes. Later builds reuse the local vcpkg binary cache.

The convenience build script performs bootstrap, configuration, compilation, and regression testing:

```powershell
.\scripts\build.ps1 -Configuration Release
.\scripts\run-gui.ps1 -Configuration Release -Seed 5489
```

## Generic CMake workflows

The project is not tied to the supplied preset. Once `external/vcpkg` has been initialized, the traditional workflow remains available:

```powershell
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Visual Studio can also open the repository directory directly as a CMake project. Generated Visual Studio projects and solutions should not be committed.

## Interactive controls

- Left click: enable or disable a precursor source at the cursor
- Left-button drag: pan the view
- Mouse wheel: zoom
- `F`, `A`, `B`, `S`, `L`: spawn one particle of the selected type
- `C`: enable or disable the temporary centering force
- `R`: remove all particles
- `Space`: pause or resume the simulation

The Dear ImGui panel exposes the physical parameters, neighbor-search mode, checkpoint controls, and current population statistics.

### Interactive command-line options

```text
--seed N
--load FILE
--checkpoint FILE
--metrics FILE
--metrics-every N
```

Example:

```powershell
.\build\windows-msvc-x64\Release\ParticleLife.exe `
    --seed 5489 `
    --checkpoint run.checkpoint `
    --metrics run.csv `
    --metrics-every 100
```

## Headless execution

The headless executable runs the same simulation core without SFML or ImGui:

```powershell
.\build\windows-msvc-x64\Release\ParticleLifeHeadless.exe `
    --seed 5489 `
    --steps 10000 `
    --initial-f 600 `
    --initial-a 1 `
    --metrics metrics.csv `
    --metrics-every 100
```

Available options can be listed with:

```powershell
.\build\windows-msvc-x64\Release\ParticleLifeHeadless.exe --help
```

Useful headless features include:

- explicit initial populations for all particle types;
- periodic particle sources with configurable type, position, period, and lifetime;
- unrestricted maximum-speed execution or optional real-time pacing;
- spatial-grid or `--brute-force` neighbor search;
- checkpoint loading and periodic checkpoint saving;
- reproducible CSV metrics.

## Reproducing the original demonstrations

### Vesicle formation

1. Start the interactive program.
2. Click to enable a precursor source.
3. Let the population reach approximately 600 green precursor particles.
4. Click again to stop the source.
5. Press `A` once to introduce a catalyst.

The reaction chain can produce surfactants that aggregate into vesicles, some of which may trap active reactants.

### Vesicle growth and reproduction

1. Enable `Destroy at boundary` in the GUI.
2. Set the Brownian speed to zero.
3. Spawn roughly 30 surfactants with `S`.
4. Use `C` temporarily to help form a centered vesicle, then disable centering.
5. Spawn one catalyst with `A` inside the vesicle.
6. Click away from the vesicle to enable a precursor source.

A successful vesicle can consume precursors, grow, divide, and repair its daughter membranes.

These are stochastic demonstrations. A fixed seed makes the pseudo-random sequence reproducible, but interactive timing and input remain part of the experiment.

## Current limitations and direction

The current model still separates spontaneous vesicle formation and sustained reproduction into two practical demonstrations. A major next step is to place both dynamics in one persistent environment, for example through spatially heterogeneous reaction zones, precursor recycling, environmental flows, or an external degradation mechanism that favors protected chemistry inside vesicles.

Further planned work includes larger simulations, automated vesicle and lineage measurements, richer artificial chemistry, and mechanisms capable of heritable fitness variation.

## Publication

The scientific model is described in:

Thomas Cabaret, **“Emergence of autopoietic vesicles able to grow, repair and reproduce in a minimalist particle system”**, ALIFE 2024.

Official paper: <https://direct.mit.edu/isal/proceedings-pdf/isal2024/36/27/2461081/isal_a_00743.pdf>

A condensed demonstration video is linked from the paper and the historical repository.

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE).
