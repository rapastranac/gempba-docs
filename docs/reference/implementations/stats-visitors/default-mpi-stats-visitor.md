# `default_mpi_stats_visitor`

```cpp
#include <gempba/defaults/default_mpi_stats_visitor.hpp>  // included automatically via gempba.hpp
```

The built-in [`stats_visitor`](../../interfaces/stats-visitor.md) for the MPI scheduler stats. After calling `visit`, all fields are populated as plain public members.

## Fields

| Member | Type | Description |
|---|---|---|
| `received_task_count` | `std::size_t` | Tasks received from other processes |
| `sent_task_count` | `std::size_t` | Tasks sent to other processes |
| `total_requested_tasks` | `std::size_t` | Total tasks requested from the load balancer |
| `total_thread_requests` | `std::size_t` | Total times worker threads requested work |
| `idle_time` | `double` | Cumulative wall-clock time (ms) threads spent idle |
| `elapsed_time` | `double` | Total wall-clock time (ms) of the run |

## Usage

```cpp
// After the run completes, on rank 0:
scheduler->synchronize_stats();

auto stats_vec = scheduler->get_stats_vector();  // one entry per rank

for (std::size_t rank = 0; rank < stats_vec.size(); ++rank) {
    if (!stats_vec[rank]) continue;  // rank 0 (center) has no compute stats

    gempba::default_mpi_stats_visitor v;
    stats_vec[rank]->visit(&v);

    std::cout << "Rank " << rank << ":\n"
              << "  received:    " << v.received_task_count   << "\n"
              << "  sent:        " << v.sent_task_count        << "\n"
              << "  idle time:   " << v.idle_time              << " ms\n"
              << "  elapsed:     " << v.elapsed_time           << " ms\n";
}
```
