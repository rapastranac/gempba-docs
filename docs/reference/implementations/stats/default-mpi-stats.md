# Default MPI stats

```cpp
#include <gempba/defaults/default_mpi_stats.hpp>  // included automatically via gempba.hpp
```

The built-in [`stats`](../../interfaces/stats.md) implementation for the MPI schedulers. An instance is owned by each worker process during a run. After `synchronize_stats()`, the center collects one instance from every rank.

## Fields

| Field | Type | Description |
|---|---|---|
| `received_task_count` | `std::size_t` | Tasks received from other processes |
| `sent_task_count` | `std::size_t` | Tasks sent to other processes |
| `total_requested_tasks` | `std::size_t` | Total tasks requested from the load balancer |
| `total_thread_requests` | `std::size_t` | Total times worker threads requested work |
| `idle_time` | `double` | Cumulative wall-clock time (ms) threads spent idle |
| `elapsed_time` | `double` | Total wall-clock time (ms) of the run |

## Reading the stats

Use [`default_mpi_stats_visitor`](../stats-visitors/default-mpi-stats-visitor.md) to extract these fields after the run:

```cpp
scheduler->synchronize_stats();

auto stats_vec = scheduler->get_stats_vector();

for (std::size_t rank = 0; rank < stats_vec.size(); ++rank) {
    if (!stats_vec[rank]) continue;

    gempba::default_mpi_stats_visitor v;
    stats_vec[rank]->visit(&v);

    std::cout << "Rank " << rank
              << "  received: "  << v.received_task_count << "\n"
              << "  sent: "      << v.sent_task_count     << "\n"
              << "  idle time: " << v.idle_time           << " ms\n"
              << "  elapsed: "   << v.elapsed_time        << " ms\n";
}
```

Alternatively, use the lambda overload to access fields directly without a visitor:

```cpp
stats_vec[rank]->visit([](const std::string& key, std::any&& value) {
    if (key == "elapsed_time")
        std::cout << "elapsed: " << std::any_cast<double>(value) << " ms\n";
});
```
