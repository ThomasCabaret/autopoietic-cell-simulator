# Windows command-line build

The recommended Windows toolchain is Visual Studio 2022 Build Tools, not the Visual Studio IDE. It provides the MSVC compiler and Windows SDK without installing the full editor.

## Required tools

- Git
- CMake 3.24 or newer
- Visual Studio 2022 Build Tools with the C++ build-tools workload

vcpkg is kept under `external/vcpkg`; the bootstrap script initializes it and CMake installs only the libraries declared by `vcpkg.json`.

## Standard PowerShell workflow

From the repository root:

```powershell
.\scripts\bootstrap-vcpkg.ps1
cmake --preset windows-msvc-x64
cmake --build --preset windows-release
ctest --preset windows-release
.\build\windows-msvc-x64\Release\ParticleLife.exe --seed 5489
```

Equivalent convenience command:

```powershell
.\scripts\build.ps1 -Configuration Release
.\scripts\run-gui.ps1 -Configuration Release -Seed 5489
```

## Existing IDE workflows

The `CMakeLists.txt` is not tied to the preset. Visual Studio can open the repository folder directly and read `CMakePresets.json`. Existing command-line generator workflows remain valid, for example:

```powershell
cmake -S . -B build-vs2019 -G "Visual Studio 16 2019" -A x64
cmake --build build-vs2019 --config Release
```

The older plain workflow also remains valid when `external/vcpkg` is initialized:

```powershell
cmake -S . -B build
cmake --build build --config Release
```

CodeBlocks extra generators are still accepted by current CMake releases but are deprecated upstream. The source configuration does not prevent their use; they require a separately installed compatible compiler/toolchain.
