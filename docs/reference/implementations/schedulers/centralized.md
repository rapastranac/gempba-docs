# MPI Centralized

```cpp
auto* s = gempba::multiprocessing::create_scheduler(gempba::multiprocessing::scheduler_topology::CENTRALIZED);
```

Implements [`scheduler`](../../interfaces/scheduler.md). An actively routing multiprocessing scheduler. Uses MPI as the IPC transport (OpenMPI on Linux/macOS, MS-MPI on Windows).

The coordinator (rank 0) is an active participant: workers send excess tasks to the coordinator, and the coordinator dispatches them to available workers. Every task handoff traverses the coordinator twice — once inbound, once outbound. At small process counts this is negligible; at scale the coordinator becomes a bottleneck.

For the full protocol walkthrough and comparison with the semi-centralized topology, see [Scheduler Topologies](../../../scheduler-topologies.md).

---

## Coordinator responsibilities

- Maintain a bounded task queue
- Maintain the process status table (`RUNNING`, `AVAILABLE`)
- Dispatch queued tasks to available workers
- Broadcast the global best value

The coordinator's task queue has a configurable capacity limit. When it is full, workers are signaled to stop sending tasks. When it falls below threshold, workers resume.

---

## Worker responsibilities

- Explore the search tree via the thread pool
- Send excess tasks to the coordinator when it is not full
- Accept tasks dispatched by the coordinator
- Update the local best value when the coordinator broadcasts a new global best

---

## When to use

Benchmarking and comparison only. The centralized topology exists to reproduce the experimental results from the original paper. For production use, prefer [MPI Semi-Centralized](semi-centralized.md).
