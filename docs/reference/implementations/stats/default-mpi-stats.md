# Default MPI stats

```cpp
#include <gempba/defaults/default_mpi_stats.hpp>  // included automatically via gempba.hpp
```

The built-in [`stats`](../../interfaces/stats.md) implementation for the MPI schedulers. An instance is owned by each worker process during a run. After `synchronize_stats()`, the center collects one instance from every rank.

---

## Fields

```cpp
std::size_t received_task_count;
```

Tasks received from other processes during the run.

```cpp
std::size_t sent_task_count;
```

Tasks sent to other processes during the run.

```cpp
std::size_t total_requested_tasks;
```

Total tasks requested from the load balancer over the course of the run.

```cpp
std::size_t total_thread_requests;
```

Total number of times worker threads requested work from the load balancer.

```cpp
double idle_time;
```

Cumulative wall-clock time in milliseconds that threads spent idle waiting for work.

```cpp
double elapsed_time;
```

Total wall-clock time in milliseconds of the run.

---

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
