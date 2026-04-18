# Building from Source

## Ubuntu

```bash
git clone https://github.com/rapastranac/gempba.git
cd gempba
mkdir build && cd build
cmake ..
make -j$(nproc)
```

## Windows (MSYS2 / MinGW64)

Open an MSYS2 MinGW64 shell, then:

```bash
git clone https://github.com/rapastranac/gempba.git
cd gempba
mkdir build && cd build
cmake -G "MSYS Makefiles" ..
make -j$(nproc)
```

## CMake flags

By default the build enables examples and tests. The available flags are:

| Flag | Default | Description |
|---|---|---|
| `GEMPBA_MULTIPROCESSING` | `OFF` | Enable MPI support |
| `GEMPBA_BUILD_EXAMPLES` | `ON` | Build the example binaries |
| `GEMPBA_BUILD_TESTS` | `ON` | Build the test suite |
| `GEMPBA_DEV_MODE` | `OFF` | Enable developer-only checks |
| `GEMPBA_DEBUG_COMMENTS` | `OFF` | Extra runtime logging |

Pass any flag at configure time:

```bash
cmake -DGEMPBA_MULTIPROCESSING=ON -DCMAKE_BUILD_TYPE=Release ..
```

All binaries land in `bin/`.

## Running tests

```bash
ctest --output-on-failure
```

## Running examples

After building, the `scripts/` directory has ready-to-use launch scripts for each platform.

### Linux

Make the script executable if it is not already, then run it from the repo root:

```bash
chmod +x scripts/run.sh
./scripts/run.sh
```

### Windows (MSYS2)

The same shell script runs directly from an MSYS2 terminal:

```bash
./scripts/run.sh
```

Open [`scripts/run.sh`](https://github.com/rapastranac/gempba/blob/main/scripts/run.sh) to see the available scenarios and uncomment the one you want to run. Other scripts in the same folder cover benchmarking over a single input ([`run_benchmark.sh`](https://github.com/rapastranac/gempba/blob/main/scripts/run_benchmark.sh)) and batch runs over a directory of graph files ([`run_folder.sh`](https://github.com/rapastranac/gempba/blob/main/scripts/run_folder.sh)).
