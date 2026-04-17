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

GemPBA uses [CPM.cmake](https://github.com/cpm-cmake/CPM.cmake) to fetch some dependencies automatically. **BS_thread_pool** is one of them — no action needed.
