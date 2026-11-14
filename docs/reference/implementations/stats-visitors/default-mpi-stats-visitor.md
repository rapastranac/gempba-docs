# `default_mpi_stats_visitor`

```cpp
#include <gempba/mpi/default_mpi_stats_visitor.hpp>  // included automatically via gempba/mpi.hpp
```

The built-in [`stats_visitor`](../../interfaces/stats-visitor.md) for the MPI scheduler stats. After calling `visit`, all fields are populated as plain public members. It reads the keys listed under [Default MPI stats](../stats/default-mpi-stats.md#keys), except `rank`.

---

## Fields

```cpp
std::size_t m_received_task_count;
```

Tasks the rank received from other ranks.

```cpp
std::size_t m_sent_task_count;
```

Tasks the rank sent to other ranks.

```cpp
std::size_t m_total_thread_requests;
```

Times the rank's pool threads asked the load balancer for work.

```cpp
double m_idle_time;
```

Seconds the rank's pool threads spent idle, per thread.

```cpp
double m_elapsed_time;
```

Seconds from the start of the rank's run to its end.

```cpp
std::size_t m_coordinator_messages_handled;
```

On the coordinator, rank 0: running and available reports, tasks in and out, score proposals and score broadcasts it handled. 0 on workers.

---

## Usage

```cpp
// After scheduler->run(...) returns, on every rank:
scheduler->synchronize_stats();   // collective

if (scheduler->is_root()) {
    auto stats_vec = scheduler->get_stats_vector();   // one entry per rank, rank 0 (the coordinator) first

    for (std::size_t rank = 0; rank < stats_vec.size(); ++rank) {
        gempba::default_mpi_stats_visitor v;
        stats_vec[rank]->visit(&v);

        std::cout << "Rank " << rank << ":\n"
                  << "  received:  " << v.m_received_task_count << "\n"
                  << "  sent:      " << v.m_sent_task_count     << "\n"
                  << "  idle time: " << v.m_idle_time           << " s per thread\n"
                  << "  elapsed:   " << v.m_elapsed_time        << " s\n";
    }
}
```
