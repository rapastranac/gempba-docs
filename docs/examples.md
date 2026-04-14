# Examples

The `examples/` directory of the [gempba repository](https://github.com/rapastranac/gempba) has complete, runnable programs. They double as templates: find the closest one to your use case, swap in your algorithm, and go.

For minimal reproducible examples as starting points, see the [GemPBA tester](https://github.com/rapastranac/gempba-tester) repository.

## Benchmarks

Synthetic binary tree traversal, no domain logic. Start here if you just want to see GemPBA running.

| File | Mode | Scheduler | Notes |
|---|---|---|---|
| `mt_benchmark.cpp` | Multithreading | n/a | Simplest possible setup. No MPI, no serialization. |
| `mp_benchmark.cpp` | Multiprocessing | Semi-centralized | Same traversal over MPI. Shows the center/worker split and stats collection. |

## Minimum Vertex Cover

A real combinatorial optimization problem on graphs, with pruning and result tracking. Use these as templates for your own branch-and-bound algorithm.

| File | Mode | Scheduler | Encoding | Notes |
|---|---|---|---|---|
| `mt_bitvect_opt_enc_semi.cpp` | Multithreading | n/a | Bitvector | Recommended starting point for MT. |
| `mp_bitvect_opt_enc_semi.cpp` | Multiprocessing | Semi-centralized | Bitvector | Recommended starting point for MP. |
| `mp_bitvect_opt_enc_central.cpp` | Multiprocessing | Centralized | Bitvector | Same as above, centralized topology. |
| `mt_graph_opt_enc_semi.cpp` | Multithreading | n/a | Graph class | Same problem, larger per-node payload. |
| `mt_graph_opt_enc_semi_non_void.cpp` | Multithreading | n/a | Graph class | Non-void recursive function variant. |
| `mp_bitvect_basic_enc_semi.cpp` | Multiprocessing | Semi-centralized | Bitvector (basic) | Older encoding, kept for comparison. |
| `mp_bitvect_basic_enc_central.cpp` | Multiprocessing | Centralized | Bitvector (basic) | Older encoding, centralized topology. |
