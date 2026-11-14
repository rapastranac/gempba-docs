# Installation

GemPBA is one library with multithreading built in, plus an optional **MPI component**:

- **The core** (`gempba`) uses all the cores of a **single machine**. No MPI to install, nothing to configure. If you are unsure, start here.
- **The MPI component** (`gempba-mpi`, the same name as the Java artifact) adds the schedulers that distribute work across **multiple machines/nodes** over MPI. Install it on top of the core when one machine is not enough. It installs as source: your build compiles it against the MPI on your machine (Open MPI, MPICH or MS-MPI), so one installation works with any of them.

A program uses the MPI component only when it asks for it (see [Using in your CMake project](#using-in-your-cmake-project-find_package)), so multithreading and MPI programs build side by side from the same installation.

---

## Ubuntu 24.04 (APT)

The `.deb` packages are built for Ubuntu 24.04 (noble) and live in a signed APT repository hosted at `https://rapastranac.github.io/gempba`. The repository serves the latest release; older `.deb`s stay attached to each [GitHub Release](https://github.com/rapastranac/gempba/releases). Register the repository and its signing key once per machine, then install:

```bash
# 1. Trust the GemPBA signing key (one-time)
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://rapastranac.github.io/gempba/gempba-archive-keyring.gpg \
  | sudo tee /etc/apt/keyrings/gempba.gpg > /dev/null

# 2. Register the repository (one-time)
echo "deb [signed-by=/etc/apt/keyrings/gempba.gpg] https://rapastranac.github.io/gempba noble main" \
  | sudo tee /etc/apt/sources.list.d/gempba.list > /dev/null
sudo apt update

# 3. Install
sudo apt install libgempba-dev          # the core
sudo apt install libgempba-mpi-dev      # the MPI component, as source; with libopenmpi-dev or libmpich-dev
```

`libgempba-mpi-dev` `Depends:` `libgempba-dev` of the same version, plus `libopenmpi-dev` (≥ 4.0) or `libmpich-dev`. Ubuntu 24.04's MPICH package starts every rank of a job alone ([Launchpad bug 2072338](https://bugs.launchpad.net/ubuntu/+source/mpich/+bug/2072338)), so use Open MPI there.

If you already have the repository registered and just want to pick up a new release:

```bash
sudo apt update && sudo apt upgrade libgempba-dev libgempba-mpi-dev
```

Alternatively, download the `.deb`s directly from the [Releases page](https://github.com/rapastranac/gempba/releases) and install them manually:

```bash
sudo dpkg -i libgempba-dev_<version>_amd64.deb
sudo dpkg -i libgempba-mpi-dev_<version>_amd64.deb   # the MPI component, if you need it
```

### Verify the installation

```bash
dpkg -s libgempba-dev | grep -E "Status|Version"
```

### Uninstall

```bash
sudo apt remove libgempba-dev libgempba-mpi-dev
```

Use `purge` instead of `remove` to also clear any leftover configuration files.

---

## Windows (MSYS2 / UCRT64)

GemPBA is in MSYS2's own UCRT64 repository. Install it from an MSYS2 UCRT64 shell:

```bash
pacman -S mingw-w64-ucrt-x86_64-gempba       # the core
pacman -S mingw-w64-ucrt-x86_64-gempba-mpi   # the MPI component, as source; brings the core and MS-MPI
```

`pacman -Syu` picks up new releases with the rest of your system.

Each [GitHub Release](https://github.com/rapastranac/gempba/releases) also carries the `.pkg.tar.zst` files, for a specific version or before MSYS2 has picked a release up. Their names carry the version, such as `mingw-w64-ucrt-x86_64-gempba-5.0.0-1-any.pkg.tar.zst`; install them with `pacman -U`:

```bash
pacman -U mingw-w64-ucrt-x86_64-gempba-<version>-any.pkg.tar.zst       # the core
pacman -U mingw-w64-ucrt-x86_64-gempba-mpi-<version>-any.pkg.tar.zst   # the MPI component, as source
```

Prefer to build from the `PKGBUILD` instead, in the same shell:

```bash
curl -LO https://raw.githubusercontent.com/rapastranac/gempba/main/packaging/msys2/PKGBUILD
MINGW_ARCH=ucrt64 makepkg-mingw -si
```

### Verify the installation

```bash
pacman -Qi mingw-w64-ucrt-x86_64-gempba
```

### Uninstall

```bash
pacman -R mingw-w64-ucrt-x86_64-gempba-mpi   # the MPI component, if installed
pacman -R mingw-w64-ucrt-x86_64-gempba       # the core
```

---

## macOS (Homebrew)

Install from the project's Homebrew tap:

```bash
brew tap rapastranac/gempba
brew install gempba       # the core
brew install gempba-mpi   # the MPI component, as source; installs gempba too
brew install open-mpi     # or mpich: the MPI your build compiles it against
```

---

## Java (Maven)

GemPBA is also a Maven dependency: `io.github.rapastranac:gempba`, or `gempba-mpi` for MPI, on Maven Central. See the dedicated **[Java section](../java/index.md)** for the dependency snippet, which MPI the JAR needs, and a full Quick Start.

---

## Using in your CMake project (find_package)

Once GemPBA is installed system-wide, wire it into your project. Ask for the core, and for the MPI component when a program uses MPI:

```cmake
find_package(gempba REQUIRED)                  # gempba::gempba, the core
find_package(gempba REQUIRED COMPONENTS mpi)   # adds gempba::mpi, compiled here against the MPI CMake finds

target_link_libraries(my_app PRIVATE gempba::gempba)
target_link_libraries(my_mpi_app PRIVATE gempba::mpi)   # brings gempba::gempba and MPI with it
```

libgempba is a shared library that keeps its own dependencies (spdlog, fmt, hwloc) inside, so a consumer needs only the C++ standard library, plus MPI for `gempba::mpi`. `gempba::mpi` is compiled in your build with your compiler, which must be compatible with the one that built libgempba, as for any C++ code that uses it. Each build directory compiles it against the MPI CMake finds there, so switching between MPIs takes another build directory, not a reinstall.

### Multithreading and MPI programs

The API is the same for every program. A multithreading program creates its load balancer and node manager from `<gempba/gempba.hpp>` alone:

```cpp
#include <gempba/gempba.hpp>

auto* lb = gempba::create_load_balancer(gempba::QUASI_HORIZONTAL);
auto& nm = gempba::create_node_manager(lb);
```

An MPI program first creates its scheduler from `<gempba/mpi.hpp>`, then passes it to both:

```cpp
#include <gempba/gempba.hpp>
#include <gempba/mpi.hpp>

auto* scheduler = gempba::mpi::create_scheduler(gempba::mpi::SEMI_CENTRALIZED);
auto* lb = gempba::create_load_balancer(gempba::QUASI_HORIZONTAL, scheduler);
auto& nm = gempba::create_node_manager(lb, scheduler);
```

The core and the MPI component link into one program together. The [Quick Start](../quick-start.md) builds a complete multithreading program and lists what an MPI one adds.

---

## Embedding via CPM (source builds)

For a source-level integration, create `external/CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.28)
include(FetchContent)

project(external)

set(CPM_DOWNLOAD_LOCATION "${CMAKE_BINARY_DIR}/cmake/CPM.cmake")
if (NOT (EXISTS ${CPM_DOWNLOAD_LOCATION}))
    message(STATUS "Downloading CPM.cmake")
    file(DOWNLOAD https://github.com/cpm-cmake/CPM.cmake/releases/latest/download/CPM.cmake ${CPM_DOWNLOAD_LOCATION})
endif ()
include(${CPM_DOWNLOAD_LOCATION})

CPMAddPackage(
    NAME gempba
    GITHUB_REPOSITORY rapastranac/gempba
    GIT_TAG v5.0.0
)

add_library(external INTERFACE)
target_link_libraries(external INTERFACE gempba)
```

Then in your root `CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.28)

project(your-project VERSION 1.0 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 23)

# GemPBA flags
set(GEMPBA_BUILD_MPI ON CACHE BOOL "" FORCE)        # compile gempba::mpi too (needs MPI); OFF builds the core alone
set(GEMPBA_HWLOC ON CACHE BOOL "" FORCE)            # hardware-topology probe (telemetry)
set(GEMPBA_DEBUG_COMMENTS OFF CACHE BOOL "" FORCE)  # (Optional) extra logging
add_subdirectory(external)

add_executable(main main.cpp)
target_link_libraries(main PUBLIC gempba::mpi)      # gempba::gempba for a multithreading program
```

For ready-to-clone consumer projects, see the [gempba-examples](https://github.com/rapastranac/gempba-examples) (C++) and [gempba-java-examples](https://github.com/rapastranac/gempba-java-examples) (Java) repositories.
