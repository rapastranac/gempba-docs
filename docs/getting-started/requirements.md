# Requirements

| Dependency | Version | Notes |
|---|---|---|
| C++ compiler | C++23 | GCC 13+, Clang 17+, MSVC 19.38+ |
| CMake | ≥ 3.28 | |
| OpenMPI | ≥ 4.0 | Only for multiprocessing support |
| Boost | any recent | Optional — examples and tests only (fetched automatically by CPM) |
| GoogleTest | any recent | Optional — running tests only (fetched automatically by CPM) |

GemPBA uses [CPM.cmake](https://github.com/cpm-cmake/CPM.cmake) for some of its external dependencies, and expects others installed on the system:

- **spdlog** must be installed system-wide:
    - Ubuntu: `apt-get install libspdlog-dev`
    - MSYS2: `pacman -S mingw-w64-x86_64-spdlog`
- **BS_thread_pool** is fetched automatically by CPM — no action needed.

When building examples or tests, CPM also fetches Boost and GoogleTest automatically. No `apt install libboost-all-dev` hunting required.
