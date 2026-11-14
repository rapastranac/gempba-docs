# MPI Semi-Centralized

```cpp
#include <gempba/mpi.hpp>

auto* s = gempba::mpi::create_scheduler(gempba::mpi::scheduler_topology::SEMI_CENTRALIZED);
```

Implements [`scheduler`](../../interfaces/scheduler.md). The recommended MPI scheduler. Uses MPI as the IPC transport: Open MPI, MPICH or MS-MPI, whichever your build compiles `gempba::mpi` against.

The coordinator (rank 0) maintains a lightweight state table — process statuses, process assignments, global best value — and pushes assignment signals proactively. It never holds or routes tasks. Workers exchange tasks directly with each other, point-to-point, after the coordinator has confirmed the destination is idle. This eliminates the bounce-back problem without making the coordinator a bottleneck.

For the full protocol walkthrough, message sequence diagrams, and comparison with the centralized topology, see [Scheduler Topologies](../../../scheduler-topologies.md).

## Inside the scheduler

<figure class="diagram">
--8<-- "assets/figures/scheduler-semi-centralized.svg"
</figure>

- **Rank 0** runs the coordinator loop on the thread that called `scheduler::run`. It holds the state table and the root of termination detection, and runs no search itself.
- **Every worker** splits the job between two kinds of thread. Pool threads run nodes; when the load balancer finds a spare node and the rank has a process waiting for work, `try_open_transmission_channel` succeeds and `force_push` puts the serialized task in a one-task outgoing slot. The **MPI thread**, the one that called `scheduler::run`, makes every MPI call: it probes the communicators in turn, runs each task it receives on the pool, sends the slot straight to the waiting process, proposes better scores, and acknowledges tasks.
- **Four communicators**, each an `MPI_Comm_dup` of `MPI_COMM_WORLD`, keep the traffic apart: tasks, states, acknowledgements and termination on one, assignments on another, scores on a third, and [telemetry](../../../telemetry/index.md) on its own.

---

## Coordinator responsibilities

- Maintain the authoritative process status table (`AVAILABLE`, `RUNNING`, `ASSIGNED`)
- Maintain the process assignment table (which idle process is waiting on which busy one)
- Maintain the global best value and broadcast updates to all workers
- Before the seed, send every worker its initial assignment: a binomial tree over ranks 1 to N-1, or the tree given to `set_custom_initial_topology`
- Seed the initial task to the first worker

The coordinator never holds a task queue. Its memory usage is independent of the number of pending tasks.

---

## Worker responsibilities

- Explore the search tree via the thread pool
- Notify the coordinator on state transitions (`RUNNING_STATE`, `AVAILABLE_STATE`)
- Send the highest-priority pending task directly to the assigned waiting process
- Update the local best value when the coordinator broadcasts a new global best

---

## When to use

Production. The semi-centralized scheduler is always at least as fast as the centralized one and scales better as the number of processes grows. Use [MPI Centralized](centralized.md) only for reproducing paper benchmarks.
