# Building from Source

```bash
git clone https://github.com/rapastranac/gempba.git
cd gempba
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)

# Run tests
ctest

# Run an example
./bin/mt_benchmark
```

Building GemPBA as the root project automatically enables examples and tests. All binaries land in `bin/`.
