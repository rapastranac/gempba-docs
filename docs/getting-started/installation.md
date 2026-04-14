# Installation

## Ubuntu (APT)

```bash
curl -fsSL https://rapastranac.github.io/gempba/pubkey.gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/gempba.gpg
echo "deb [signed-by=/etc/apt/keyrings/gempba.gpg] https://rapastranac.github.io/gempba stable main" \
  | sudo tee /etc/apt/sources.list.d/gempba.list
sudo apt-get update
sudo apt-get install libgempba-dev
```

## Windows (MSYS2 / MinGW64)

Download the latest `.pkg.tar.zst` from the [Releases page](https://github.com/rapastranac/gempba/releases), then:

```bash
pacman -U mingw-w64-x86_64-gempba-<version>-1-x86_64.pkg.tar.zst
```

## Using in your CMake project (find_package)

Once installed system-wide, wire GemPBA into your project:

```cmake
find_package(gempba REQUIRED)
target_link_libraries(your-target PRIVATE gempba::gempba)
```

## Embedding via CPM (recommended for source builds)

Create `external/CMakeLists.txt`:

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
set(GEMPBA_MULTIPROCESSING ON CACHE BOOL "" FORCE)  # Enable MPI support
set(GEMPBA_DEBUG_COMMENTS ON CACHE BOOL "" FORCE)   # (Optional) extra logging
set(GEMPBA_BUILD_EXAMPLES ON CACHE BOOL "" FORCE)   # (Optional) build examples
set(GEMPBA_BUILD_TESTS ON CACHE BOOL "" FORCE)      # (Optional) build tests
add_subdirectory(external)

target_link_libraries(main PUBLIC gempba::gempba)
```

For minimal reproducible examples you can use as starting points, see the [GemPBA tester](https://github.com/rapastranac/gempba-tester) repository.
