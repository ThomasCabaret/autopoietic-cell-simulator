# Template-copy demonstrator

This executable is deliberately separate from the main life-emergence simulator. It tests a minimal local exact-copy chemistry for short binary polymers.

## Model

- Every monomer carries a binary symbol, `0` or `1`.
- Strong directional left/right backbone bonds form polymers.
- A backbone monomer can capture one free monomer carrying the same symbol.
- Only monomers with no backbone bond can act as incoming copy substrates. Existing oligomers therefore do not bind across another template and jam it.
- Two captured monomers can form a backbone bond only when their two template partners are already adjacent in the parent chain.
- The capture phase allows pairing and templated ligation.
- The release phase breaks transverse pair bonds and pushes the two strands apart while leaving the backbone intact.
- A released daughter chain can act as a new template during the next capture phase.

All microscopic operations inspect only spatial neighbors, direct bond neighbors, or one template bond and its two paired substrates. The model never identifies a complete molecule or requests that a copy be completed.

## Build and run on Windows

After copying the differential archive over the repository root:

```powershell
cmake --preset windows-msvc-x64
cmake --build --preset windows-release
ctest --preset windows-release
```

Graphical demonstrator:

```powershell
.\scripts\run-template-copy.ps1
```

Headless monitored run:

```powershell
.\scripts\run-template-copy-headless.ps1
```

The headless executable prints the complete sequence census as `total/detached`. For example, `011010=6/4` means that six exact chains exist and four are no longer attached to another strand through template bonds.

## Tuned default experiment

- Initial template: `011010`
- Free monomers: 48 of symbol `0` and 48 of symbol `1`
- Periodic world: 100 x 60
- Capture phase: 12 simulated seconds
- Release phase: 4 simulated seconds
- Success milestone: four detached exact copies of the initial six-bit chain

The GUI reports total and detached exact chains, completed copies, chain lengths, and a sequence-by-sequence census.

Useful controls:

- `Reset experiment`: rebuild the selected template and monomer pool.
- `Force capture phase`: allow matching, alignment, and ligation.
- `Force release phase`: separate paired strands.
- `Capture duration` / `Release duration`: control the macroscopic cycle.
- `Capture noise` / `Release noise`: change molecular agitation.
- `Pair capture rate`, `Pair spring`, and `Pair alignment`: control template binding.
- `Ligation rate` and `Ligation angle tolerance`: control backbone construction.
- `Release pair break rate`: control strand separation.
- Left click in the world to add a free monomer of the selected symbol.

## Headless examples

Use a fixed sequence and write a CSV time series:

```powershell
.\build\windows-msvc-x64\Release\TemplateCopyHeadless.exe `
    --seed 5489 `
    --sequence 011010 `
    --target-exact 4 `
    --csv template-copy.csv
```

Generate a deterministic random six-bit sequence from the seed:

```powershell
.\build\windows-msvc-x64\Release\TemplateCopyHeadless.exe `
    --seed 42 `
    --random-sequence-length 6
```
