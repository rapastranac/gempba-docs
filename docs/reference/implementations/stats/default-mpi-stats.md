# Default MPI stats

```cpp
// src/mpi/private/impl/schedulers/default_mpi_stats.hpp: private to the MPI component
```

The built-in [`stats`](../../interfaces/stats.md) implementation for the MPI schedulers. Programs read it through [`default_mpi_stats_visitor`](../stats-visitors/default-mpi-stats-visitor.md) or the `visit` lambda below, not by including it. Every rank owns one during a run, rank 0 included. After `synchronize_stats()`, which every rank calls, rank 0 holds one instance per rank.

---

## Keys

`visit` hands over each value under these keys:

| Key | Type | Meaning |
|---|---|---|
| `rank` | `int` | The rank these stats belong to. |
| `received_task_count` | `std::size_t` | Tasks this rank received from other ranks. |
| `sent_task_count` | `std::size_t` | Tasks this rank sent to other ranks. |
| `total_thread_requests` | `std::size_t` | Times this rank's pool threads asked the load balancer for work. |
| `idle_time` | `double` | Seconds this rank's pool threads spent idle, per thread (`node_manager::get_idle_time()`). |
| `elapsed_time` | `double` | Seconds from the start of this rank's run to its end (`MPI_Wtime`). |
| `coordinator_messages_handled` | `std::size_t` | On the coordinator, rank 0: running and available reports, tasks in and out, score proposals and score broadcasts it handled. 0 on workers. |

Rank 0's entry is never empty: it holds the coordinator's own counts and elapsed time.

---

## Reading the stats

Use [`default_mpi_stats_visitor`](../stats-visitors/default-mpi-stats-visitor.md) to extract these fields after the run:

```cpp
scheduler->synchronize_stats();   // collective: every rank calls it

if (scheduler->is_root()) {
    auto stats_vec = scheduler->get_stats_vector();   // one entry per rank, rank 0 first

    for (std::size_t rank = 0; rank < stats_vec.size(); ++rank) {
        gempba::default_mpi_stats_visitor v;
        stats_vec[rank]->visit(&v);

        std::cout << "Rank " << rank << "\n"
                  << "  received:  " << v.m_received_task_count << "\n"
                  << "  sent:      " << v.m_sent_task_count     << "\n"
                  << "  idle time: " << v.m_idle_time           << " s per thread\n"
                  << "  elapsed:   " << v.m_elapsed_time        << " s\n";
    }
}
```

Alternatively, use the lambda overload to read values by key without a visitor:

```cpp
stats_vec[rank]->visit([](const std::string& key, std::any&& value) {
    if (key == "elapsed_time") {
        std::cout << "elapsed: " << std::any_cast<double>(value) << " s\n";
    }
});
```
