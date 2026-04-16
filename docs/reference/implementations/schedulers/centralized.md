# MPI Centralized

```cpp
auto* s = gempba::mp::create_scheduler(gempba::mp::scheduler_topology::CENTRALIZED);
```

Implements [`scheduler`](interfaces/scheduler.md). An actively routing multiprocessing scheduler. Uses OpenMPI as the IPC transport.

The center (rank 0) is an active participant: workers send excess tasks to the center, and the center dispatches them to available workers. Every task handoff traverses the center twice — once inbound, once outbound. At small process counts this is negligible; at scale the center becomes a bottleneck.

For the full protocol walkthrough and comparison with the semi-centralized topology, see [Scheduler Topologies](scheduler-topologies.md).

## Center responsibilities

- Maintain a bounded task queue
- Maintain the process status table (`RUNNING`, `AVAILABLE`)
- Dispatch queued tasks to available workers
- Broadcast the global best value

The center's task queue has a configurable capacity limit. When it is full, workers are signaled to stop sending tasks. When it falls below threshold, workers resume.

## Worker responsibilities

- Explore the search tree via the thread pool
- Send excess tasks to the center when it is not full
- Accept tasks dispatched by the center
- Update the local best value when the center broadcasts a new global best

## When to use

Benchmarking and comparison only. The centralized topology exists to reproduce the experimental results from the original paper. For production use, prefer [MPI Semi-Centralized](semi-centralized.md).
