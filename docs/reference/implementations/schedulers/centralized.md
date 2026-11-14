# MPI Centralized

```cpp
#include <gempba/mpi.hpp>

auto* s = gempba::mpi::create_scheduler(gempba::mpi::scheduler_topology::CENTRALIZED);
```

Implements [`scheduler`](../../interfaces/scheduler.md). An actively routing MPI scheduler. Uses MPI as the IPC transport: Open MPI, MPICH or MS-MPI, whichever your build compiles `gempba::mpi` against.

The coordinator (rank 0) is an active participant: workers send excess tasks to the coordinator, and the coordinator dispatches them to available workers. Every task handoff traverses the coordinator twice — once inbound, once outbound. At small process counts this is negligible; at scale the coordinator becomes a bottleneck.

For the full protocol walkthrough and comparison with the semi-centralized topology, see [Scheduler Topologies](../../../scheduler-topologies.md).

---

## Coordinator responsibilities

- Maintain a bounded task queue
- Maintain the process status table (`RUNNING`, `AVAILABLE`)
- Dispatch queued tasks to available workers
- Broadcast the global best value

The coordinator's queue is bounded by compile-time limits: 1000 tasks per process, times the number of ranks, or 10 GB of memory. Past either one it broadcasts `CENTER_IS_FULL`, and workers run their tasks locally instead of sending them. Once the queue is below 80% of the task limit and memory below 90%, it broadcasts `CENTER_IS_FREE` and workers send again. It never rejects a task it has received.

---

## Worker responsibilities

- Explore the search tree via the thread pool
- Send excess tasks to the coordinator when it is not full
- Accept tasks dispatched by the coordinator
- Update the local best value when the coordinator broadcasts a new global best

---

## When to use

Benchmarking and comparison only. The centralized topology exists to reproduce the experimental results from the original paper. For production use, prefer [MPI Semi-Centralized](semi-centralized.md).
