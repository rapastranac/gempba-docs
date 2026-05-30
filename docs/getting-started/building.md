# Building from Source

Build from source when a pre-built package is not an option — custom configure flags, an unsupported distro, or contributing back. For everyday use, prefer a [pre-built package](installation.md).

First install the [build dependencies](requirements.md) for your platform.

## Ubuntu / macOS

```bash
git clone https://github.com/rapastranac/gempba.git
cd gempba
cmake -B build -DGEMPBA_MULTIPROCESSING=ON   # ON = MPI flavor, OFF = multithreading
cmake --build build --parallel
sudo cmake --install build                   # optional: install system-wide
```

## Windows (MSYS2 / MinGW64)

Open an MSYS2 MinGW64 shell, then:

```bash
git clone https://github.com/rapastranac/gempba.git
cd gempba
cmake -B build -G "MSYS Makefiles" -DGEMPBA_MULTIPROCESSING=ON
cmake --build build --parallel
```

## CMake flags

When GemPBA is the **root** project (you cloned and built it directly), it defaults to a multiprocessing developer build with tests enabled. As a **subproject** (pulled in via CPM/`add_subdirectory`), every flag defaults to `OFF` and you opt in to what you need.

| Flag | Root default | Description |
|---|---|---|
| `GEMPBA_MULTIPROCESSING` | `ON` | `ON` = MPI (`mpi`) flavor, `OFF` = multithreading (`mt`) flavor |
| `GEMPBA_HWLOC` | `ON` | Use hwloc for the hardware-topology probe (telemetry) |
| `GEMPBA_BUILD_TESTS` | `ON` | Build the GoogleTest suite |
| `GEMPBA_DEV_MODE` | `ON` | Developer-only checks; required to build the tests |
| `GEMPBA_DEBUG_COMMENTS` | `OFF` | Extra runtime logging |
| `GEMPBA_BUILD_JAVA_BINDING` | `OFF` | Build the Java JNI shared library (requires a JDK and `-DGEMPBA_JNI_CLASSIFIER=<os>-<arch>`) |

Pass any flag at configure time:

```bash
cmake -B build -DGEMPBA_MULTIPROCESSING=ON -DGEMPBA_HWLOC=ON -DCMAKE_BUILD_TYPE=Release
```

!!! note "Tests require dev mode"
    The test suite uses the explicit `gempba::multithreading::*` / `gempba::multiprocessing::*` forms, so it builds only with `GEMPBA_DEV_MODE=ON`, and the multiprocessing tests additionally require `GEMPBA_MULTIPROCESSING=ON`. Both are on by default for a root build.

## Running tests

```bash
ctest --test-dir build --output-on-failure
```

Flaky tests (prefixed `FLAKY_`) are retried automatically in CI.

## Running examples

Example programs no longer live in the gempba source tree — they moved to the sibling repository [**rapastranac/gempba-examples**](https://github.com/rapastranac/gempba-examples) (C++) and [**rapastranac/gempba-java-examples**](https://github.com/rapastranac/gempba-java-examples) (Java), where they consume GemPBA via `find_package(gempba)` exactly as a downstream user would. Clone one of those repos, install GemPBA (or point it at your build), and build the examples from there. See the [Examples](../examples.md) page for the catalog.
