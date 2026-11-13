# Building from Source

Build from source when a pre-built package is not an option — custom configure flags, an unsupported distro, or contributing back. For everyday use, prefer a [pre-built package](installation.md).

First install the [build dependencies](requirements.md) for your platform.

## Ubuntu / macOS

```bash
git clone https://github.com/rapastranac/gempba.git
cd gempba
cmake -B build                               # compiles the MPI component too; -DGEMPBA_BUILD_MPI=OFF needs no MPI
cmake --build build --parallel
sudo cmake --install build                   # optional: install system-wide
```

## Windows (MSYS2 / UCRT64)

Open an MSYS2 UCRT64 shell, then:

```bash
git clone https://github.com/rapastranac/gempba.git
cd gempba
cmake -B build -G Ninja
cmake --build build --parallel
```

Either way, the install ships the MPI component as source, so `find_package(gempba COMPONENTS mpi)` works against it once MPI is on the machine. `GEMPBA_BUILD_MPI` only decides whether this build compiles the component too, which gempba's own tests and the Java binding need.

## CMake flags

When GemPBA is the **root** project (you cloned and built it directly), it defaults to a developer build: the MPI component, hwloc and the tests are on, and with no `CMAKE_BUILD_TYPE` the build is `Debug`. As a **subproject** (pulled in via CPM/`add_subdirectory`), every flag defaults to `OFF` and you opt in to what you need.

| Flag | Root default | Description |
|---|---|---|
| `GEMPBA_BUILD_MPI` | `ON` | Compile the MPI component, `gempba::mpi`, in this build; needs MPI. The install ships its source either way |
| `GEMPBA_HWLOC` | `ON` | Use hwloc for the hardware-topology probe (telemetry) |
| `GEMPBA_BUILD_TESTS` | `ON` | Build the GoogleTest suite |
| `GEMPBA_MPI_INTEGRATION_TESTS` | `OFF` | Register the multi-rank MPI tests with CTest, which runs them under `mpiexec`; needs `GEMPBA_BUILD_TESTS` and `GEMPBA_BUILD_MPI` |
| `GEMPBA_DEBUG_COMMENTS` | `OFF` | Extra runtime logging |
| `GEMPBA_BUILD_JAVA_BINDING` | `OFF` | Build the Java JNI shared library (requires a JDK and `-DGEMPBA_JNI_CLASSIFIER=<os>-<arch>`) |

Pass any flag at configure time:

```bash
cmake -B build -DGEMPBA_BUILD_MPI=OFF -DGEMPBA_HWLOC=ON -DCMAKE_BUILD_TYPE=Release
```

!!! note "Tests and the MPI component"
    The MPI component's unit tests build only with `GEMPBA_BUILD_MPI=ON`; without it, the suite runs the core's tests alone.

## Running tests

```bash
ctest --test-dir build --output-on-failure
```

Flaky tests (prefixed `FLAKY_`) are retried automatically in CI.

## Running examples

Example programs no longer live in the gempba source tree — they moved to the sibling repository [**rapastranac/gempba-examples**](https://github.com/rapastranac/gempba-examples) (C++) and [**rapastranac/gempba-java-examples**](https://github.com/rapastranac/gempba-java-examples) (Java), where they consume GemPBA via `find_package(gempba)` exactly as a downstream user would. Clone one of those repos, install GemPBA (or point it at your build), and build the examples from there. See the [Examples](../examples.md) page for the catalog.
