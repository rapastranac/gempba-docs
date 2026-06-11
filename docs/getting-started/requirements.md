# Requirements

These requirements apply when **building GemPBA from source**. If you install a pre-built package (APT, MSYS2, Homebrew) or pull the Java JAR, the runtime dependencies are resolved for you — see [Installation](installation.md).

| Dependency | Version | Notes |
|---|---|---|
| C++ compiler | C++23 | GCC 13+, Clang 17+, AppleClang, MSVC 19.38+ |
| CMake | ≥ 3.28 | |
| hwloc | any recent | Hardware-topology probe used by telemetry (gated by `GEMPBA_HWLOC`, ON by default when gempba is the root project) |
| OpenMPI | ≥ 4.0 | Only for the multiprocessing (`mpi`) flavor |
| spdlog | any recent | Must be provided by the system since v3.1.0 |
| fmt | any recent | Pulled in alongside spdlog |
| Boost | any recent | Optional — tests only (fetched automatically by CPM) |
| GoogleTest | any recent | Optional — running tests only (fetched automatically by CPM) |
| JDK + Maven | JDK 25, Maven 3.9+ | Only for the Java binding |

GemPBA uses [CPM.cmake](https://github.com/cpm-cmake/CPM.cmake) to fetch some dependencies automatically. **BS_thread_pool**, **Boost**, and **GoogleTest** are among them — no action needed for those.

---

## Installing dependencies

### Ubuntu

```bash
sudo apt update
sudo apt install -y build-essential
sudo apt install -y cmake
sudo apt install -y libhwloc-dev
sudo apt install -y libopenmpi-dev   # multiprocessing flavor only
sudo apt install -y libspdlog-dev
sudo apt install -y libfmt-dev
```

If you plan to run the tests, also install Boost and GoogleTest:

```bash
sudo apt install -y libboost-all-dev
sudo apt install -y libgtest-dev
sudo apt install -y libgmock-dev
```

On Ubuntu, `libgtest-dev` ships the source only. You need to compile and install it before CMake can find it:

```bash
cd /usr/src/googletest
sudo cmake -S . -B build
sudo cmake --build build --target install
```

### Windows (MSYS2 / MinGW64)

Open an MSYS2 MinGW64 shell and run:

```bash
pacman -Syu
pacman -S base-devel
pacman -S mingw-w64-x86_64-toolchain
pacman -S mingw-w64-x86_64-cmake
pacman -S mingw-w64-x86_64-make
pacman -S mingw-w64-x86_64-hwloc
pacman -S mingw-w64-x86_64-msmpi    # multiprocessing flavor only
pacman -S mingw-w64-x86_64-spdlog
pacman -S mingw-w64-x86_64-fmt
```

If you plan to run the tests:

```bash
pacman -S mingw-w64-x86_64-boost
pacman -S mingw-w64-x86_64-gtest
```

### macOS (Homebrew)

```bash
brew install cmake
brew install hwloc
brew install open-mpi   # multiprocessing flavor only
brew install spdlog
brew install fmt
```

If you plan to run the tests:

```bash
brew install boost
brew install googletest
```
