# MPI Semi-Centralized

```cpp
auto* s = gempba::mp::create_scheduler(gempba::mp::scheduler_topology::SEMI_CENTRALIZED);
```

Implements [`scheduler`](interfaces/scheduler.md). The recommended multiprocessing scheduler. Uses OpenMPI as the IPC transport.

The center (rank 0) maintains a lightweight state table — process statuses, process assignments, global best value — and pushes assignment signals proactively. It never holds or routes tasks. Workers exchange tasks directly with each other, point-to-point, after the center has confirmed the destination is idle. This eliminates the bounce-back problem without making the center a bottleneck.

For the full protocol walkthrough, message sequence diagrams, and comparison with the centralized topology, see [Scheduler Topologies](scheduler-topologies.md).

## Center responsibilities

- Maintain the authoritative process status table (`AVAILABLE`, `RUNNING`, `ASSIGNED`)
- Maintain the process assignment table (which idle process is waiting on which busy one)
- Maintain the global best value and broadcast updates to all workers
- Seed the initial task to the first worker

The center never holds a task queue. Its memory usage is independent of the number of pending tasks.

## Worker responsibilities

- Explore the search tree via the thread pool
- Notify the center on state transitions (`started_running`, `available`)
- Send the highest-priority pending task directly to the assigned waiting process
- Update the local best value when the center broadcasts a new global best

## When to use

Production. The semi-centralized scheduler is always at least as fast as the centralized one and scales better as the number of processes grows. Use [MPI Centralized](centralized.md) only for reproducing paper benchmarks.
