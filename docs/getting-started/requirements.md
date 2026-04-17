# Requirements

| Dependency | Version | Notes |
|---|---|---|
| C++ compiler | C++23 | GCC 13+, Clang 17+, MSVC 19.38+ |
| CMake | ≥ 3.28 | |
| OpenMPI | ≥ 4.0 | Only for multiprocessing support |
| spdlog | any recent | |
| fmt | any recent | |
| Boost | any recent | Optional — examples and tests only (fetched automatically by CPM) |
| GoogleTest | any recent | Optional — running tests only (fetched automatically by CPM) |

GemPBA uses [CPM.cmake](https://github.com/cpm-cmake/CPM.cmake) to fetch some dependencies automatically. **BS_thread_pool**, **Boost**, and **GoogleTest** are among them — no action needed for those.

---

## Installing dependencies

### Ubuntu

```bash
sudo apt-get update
sudo apt-get install -y build-essential
sudo apt-get install -y cmake
sudo apt-get install -y libopenmpi-dev
sudo apt-get install -y libspdlog-dev
sudo apt-get install -y libfmt-dev
```

If you plan to build the examples or tests, also install Boost and GoogleTest:

```bash
sudo apt-get install -y libboost-all-dev
sudo apt-get install -y libgtest-dev
sudo apt-get install -y libgmock-dev
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
pacman -S mingw-w64-x86_64-msmpi
pacman -S mingw-w64-x86_64-spdlog
pacman -S mingw-w64-x86_64-fmt
```

If you plan to build the examples or tests:

```bash
pacman -S mingw-w64-x86_64-boost
pacman -S mingw-w64-x86_64-gtest
```
