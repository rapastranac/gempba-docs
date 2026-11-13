# Requirements

These requirements apply when **building GemPBA from source**. If you install a pre-built package (APT, MSYS2, Homebrew) or pull the Java JAR, the runtime dependencies are resolved for you — see [Installation](installation.md).

| Dependency | Version | Notes |
|---|---|---|
| C++ compiler | C++23 | GCC 13+, Clang 17+, AppleClang, MSVC 19.38+ |
| CMake | ≥ 3.28 | |
| hwloc | any recent | Hardware-topology probe used by telemetry (gated by `GEMPBA_HWLOC`, ON by default when gempba is the root project) |
| pkg-config | any recent | Finds hwloc in the build |
| MPI | Open MPI ≥ 4.0, MPICH, or MS-MPI on Windows | Only for the MPI component: gempba's build with `GEMPBA_BUILD_MPI=ON`, the default, and programs that use `gempba::mpi` |
| spdlog | any recent | Build only; compiled into the library |
| fmt | any recent | Build only; compiled into the library |
| Boost | any recent | Optional — tests only |
| GoogleTest | any recent | Optional — running tests only |
| JDK + Maven | JDK 25, Maven 3.9+ | Only for the Java binding |

GemPBA uses [CPM.cmake](https://github.com/cpm-cmake/CPM.cmake) to fetch **BS_thread_pool** during the build — no action needed for it.

---

## Installing dependencies

### Ubuntu

```bash
sudo apt update
sudo apt install -y build-essential
sudo apt install -y cmake
sudo apt install -y libhwloc-dev
sudo apt install -y pkgconf
sudo apt install -y libopenmpi-dev   # the MPI component; not needed with -DGEMPBA_BUILD_MPI=OFF
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

### Windows (MSYS2 / UCRT64)

Open an MSYS2 UCRT64 shell and run:

```bash
pacman -Syu
pacman -S base-devel
pacman -S mingw-w64-ucrt-x86_64-toolchain
pacman -S mingw-w64-ucrt-x86_64-cmake
pacman -S mingw-w64-ucrt-x86_64-ninja
pacman -S mingw-w64-ucrt-x86_64-hwloc
pacman -S mingw-w64-ucrt-x86_64-pkgconf
pacman -S mingw-w64-ucrt-x86_64-msmpi    # the MPI component; not needed with -DGEMPBA_BUILD_MPI=OFF
pacman -S mingw-w64-ucrt-x86_64-spdlog
pacman -S mingw-w64-ucrt-x86_64-fmt
```

If you plan to run the tests:

```bash
pacman -S mingw-w64-ucrt-x86_64-boost
pacman -S mingw-w64-ucrt-x86_64-gtest
```

### macOS (Homebrew)

```bash
brew install cmake
brew install hwloc
brew install pkgconf
brew install open-mpi   # the MPI component; not needed with -DGEMPBA_BUILD_MPI=OFF
brew install spdlog
brew install fmt
```

If you plan to run the tests:

```bash
brew install boost
brew install googletest
```
