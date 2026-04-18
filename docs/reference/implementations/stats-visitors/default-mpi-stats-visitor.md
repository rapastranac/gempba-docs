# `default_mpi_stats_visitor`

```cpp
#include <gempba/defaults/default_mpi_stats_visitor.hpp>  // included automatically via gempba.hpp
```

The built-in [`stats_visitor`](../../interfaces/stats-visitor.md) for the MPI scheduler stats. After calling `visit`, all fields are populated as plain public members.

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
              << "  received:  " << v.received_task_count << "\n"
              << "  sent:      " << v.sent_task_count     << "\n"
              << "  idle time: " << v.idle_time           << " ms\n"
              << "  elapsed:   " << v.elapsed_time        << " ms\n";
}
```
