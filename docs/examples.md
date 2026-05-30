# Examples

Working example programs live in the sibling repository [**rapastranac/gempba-examples**](https://github.com/rapastranac/gempba-examples). They consume GemPBA via `find_package(gempba)` exactly as a downstream user would, so they double as templates: find the closest one to your use case, swap in your algorithm, and go.

The tree is split by flavor — `multithreading/src/` and `multiprocessing/src/`. To build them, install GemPBA (see [Installation](getting-started/installation.md)) and build the example repo against it.

!!! info "Java examples"
    Java/Maven equivalents live in [**rapastranac/gempba-java-examples**](https://github.com/rapastranac/gempba-java-examples), organized into `multithreading/`, `multiprocessing/`, and `sequential/` Maven modules.

## Benchmarks

Synthetic binary tree traversal, no domain logic. Start here if you just want to see GemPBA running.

| File | Mode | Scheduler | Notes |
|---|---|---|---|
| `multithreading/src/benchmark.cpp` | Multithreading | n/a | Simplest possible setup. No MPI, no serialization. |
| `multiprocessing/src/benchmark.cpp` | Multiprocessing | Semi-centralized | Same traversal over MPI. Shows the center/worker split and stats collection. |

## Minimum Vertex Cover

A real combinatorial optimization problem on graphs, with pruning and result tracking. Use these as templates for your own branch-and-bound algorithm.

| File | Mode | Scheduler | Encoding | Notes |
|---|---|---|---|---|
| `multithreading/src/bitvect_opt_enc_semi.cpp` | Multithreading | n/a | Bitvector | Recommended starting point for MT. |
| `multiprocessing/src/bitvect_opt_enc_semi.cpp` | Multiprocessing | Semi-centralized | Bitvector | Recommended starting point for MP. |
| `multiprocessing/src/bitvect_opt_enc_central.cpp` | Multiprocessing | Centralized | Bitvector | Same as above, centralized topology. |
| `multithreading/src/graph_opt_enc_semi.cpp` | Multithreading | n/a | Graph class | Same problem, larger per-node payload. |
| `multithreading/src/graph_opt_enc_semi_non_void.cpp` | Multithreading | n/a | Graph class | Non-void recursive function variant. |
| `multiprocessing/src/bitvect_basic_enc_semi.cpp` | Multiprocessing | Semi-centralized | Bitvector (basic) | Older encoding, kept for comparison. |
| `multiprocessing/src/bitvect_basic_enc_central.cpp` | Multiprocessing | Centralized | Bitvector (basic) | Older encoding, centralized topology. |
