# Installation

GemPBA comes in two **flavors**, and which one you want depends on where your computation runs:

- **Multithreading (`mt`)** — the default. Uses all the cores of a **single machine**. No MPI to install, nothing to configure. If you are unsure, start here.
- **Multiprocessing (`mpi`; the Java artifact calls it `mp-mpi`)** — distributes work across **multiple machines/nodes** over MPI. Add it when one machine is not enough.

Both flavors can be installed side by side on **any** platform. You pick which one a program uses when you build *that* program (see [Selecting a flavor](#selecting-a-flavor)), not when you install.

!!! note "Where the API picks the flavor"
    Consumer code is identical regardless of flavor. The flavor is selected at `find_package` time, not at every call site.

---

## Ubuntu / Debian (APT)

The `.deb` packages live in a signed APT repository hosted at `https://rapastranac.github.io/gempba`. Register the repository and its signing key once per machine, then install:

```bash
# 1. Trust the GemPBA signing key (one-time)
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://rapastranac.github.io/gempba/gempba-archive-keyring.gpg \
  | sudo tee /etc/apt/keyrings/gempba.gpg > /dev/null

# 2. Register the repository (one-time)
echo "deb [signed-by=/etc/apt/keyrings/gempba.gpg] https://rapastranac.github.io/gempba stable main" \
  | sudo tee /etc/apt/sources.list.d/gempba.list > /dev/null
sudo apt update

# 3. Install the flavor(s) you need
sudo apt install libgempba-dev          # multithreading flavor (default)
sudo apt install libgempba-mpi-dev      # MPI flavor; depends on libgempba-dev
```

The two packages install side by side without conflict: `libgempba-mpi-dev` `Depends:` the base `libgempba-dev` plus `libopenmpi-dev`.

If you already have the repository registered and just want to pick up a new release:

```bash
sudo apt update && sudo apt upgrade libgempba-dev libgempba-mpi-dev
```

Alternatively, download the `.deb` directly from the [Releases page](https://github.com/rapastranac/gempba/releases) and install it manually:

```bash
sudo dpkg -i libgempba-dev_<version>_amd64.deb
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

## Windows (MSYS2 / MinGW64)

MSYS2 packages are attached to each GitHub Release rather than served from a custom pacman repository. Download the `.pkg.tar.zst` asset(s) for the flavor you want — their names carry the version (e.g. `mingw-w64-x86_64-gempba-4.1.1-1-any.pkg.tar.zst`) — from the [latest release](https://github.com/rapastranac/gempba/releases/latest), then install locally:

```bash
pacman -U mingw-w64-x86_64-gempba-<version>-any.pkg.tar.zst       # multithreading (default)
pacman -U mingw-w64-x86_64-gempba-mpi-<version>-any.pkg.tar.zst   # MPI; depends on the mt package above
```

If you installed from a local package and want to upgrade, download the new package and run the same command again.

Prefer to build from the `PKGBUILD` instead:

```bash
curl -LO https://raw.githubusercontent.com/rapastranac/gempba/main/packaging/msys2/PKGBUILD
makepkg -si
```

### Verify the installation

```bash
pacman -Qi mingw-w64-x86_64-gempba
```

### Uninstall

```bash
pacman -R mingw-w64-x86_64-gempba
```

---

## macOS (Homebrew)

Install from the project's Homebrew tap:

```bash
brew tap rapastranac/gempba
brew install gempba       # multithreading (default), or `brew install gempba-mpi` for MPI
```

To keep **both** flavors on one machine, install the second after unlinking the first, then point each project at the flavor it uses:

```bash
brew unlink gempba && brew install gempba-mpi
cmake -B build -DCMAKE_PREFIX_PATH=$(brew --prefix gempba)       # a project built against mt
cmake -B build -DCMAKE_PREFIX_PATH=$(brew --prefix gempba-mpi)   # a project built against mpi
```

---

## Java (Maven)

GemPBA is also a Maven dependency, published to GitHub Packages as a fat JAR (one per `mt` / `mp-mpi` flavor classifier). See the dedicated **[Java section](../java/index.md)** for the registry setup, authentication, dependency snippet, and a full Quick Start.

---

## Using in your CMake project (find_package)

Once GemPBA is installed system-wide, wire it into your project. The flavor is chosen via `COMPONENTS`:

```cmake
find_package(gempba REQUIRED)                  # default: mt
find_package(gempba REQUIRED COMPONENTS mt)    # explicit mt
find_package(gempba REQUIRED COMPONENTS mpi)   # mpi (requires libgempba-mpi-dev installed)

target_link_libraries(your-target PRIVATE gempba::gempba)
```

Both flavors export the same imported target `gempba::gempba`, so your link line never changes between modes. The `GEMPBA_MULTIPROCESSING` macro flows through the target's interface, and `<gempba/gempba.hpp>` exposes the matching API at compile time.

### Selecting a flavor

Consumer code is identical regardless of flavor. Write the short form:

```cpp
auto* lb = gempba::create_load_balancer(gempba::QUASI_HORIZONTAL /*, worker* if MP*/);
auto& nm = gempba::create_node_manager(lb /*, worker* if MP*/);
```

The explicit `gempba::multithreading::*` and `gempba::multiprocessing::*` qualifiers are also available for code that wants to be unambiguous.

!!! warning "One flavor per binary"
    The two flavors are **mutually exclusive within a single binary**: they share mode-agnostic top-level symbols (`gempba::shutdown`, `gempba::get_load_balancer`, …) and would ODR-clash at link time. `find_package(gempba COMPONENTS mt mpi)` is therefore rejected up front with a clear diagnostic. A project that genuinely needs both flavors — say, an MT debug runner and an MPI cluster runner — splits into two executables, each `find_package`-ing the flavor it needs.

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
    GIT_TAG main
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
set(GEMPBA_MULTIPROCESSING ON CACHE BOOL "" FORCE)  # ON = MPI flavor, OFF = multithreading
set(GEMPBA_HWLOC ON CACHE BOOL "" FORCE)            # hardware-topology probe (telemetry)
set(GEMPBA_DEBUG_COMMENTS OFF CACHE BOOL "" FORCE)  # (Optional) extra logging
add_subdirectory(external)

target_link_libraries(main PUBLIC gempba::gempba)
```

For ready-to-clone consumer projects, see the [gempba-examples](https://github.com/rapastranac/gempba-examples) (C++) and [gempba-java-examples](https://github.com/rapastranac/gempba-java-examples) (Java) repositories.
