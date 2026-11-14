# Scheduler Topologies

GemPBA's MPI component ships two scheduler topologies. The default recommendation is `SEMI_CENTRALIZED`.

```cpp
#include <gempba/mpi.hpp>

// Semi-centralized (recommended)
auto* semi = gempba::mpi::create_scheduler(gempba::mpi::scheduler_topology::SEMI_CENTRALIZED);

// Centralized (for comparison)
auto* central = gempba::mpi::create_scheduler(gempba::mpi::scheduler_topology::CENTRALIZED);
```

A program creates one of them. Either way, every rank calls `scheduler::run`, and rank 0 is the coordinator: it takes no part in the computation.

---

## Semi-Centralized (recommended)

### What the coordinator does, and does not do

The coordinator (rank 0) has a single responsibility: **knowing who is idle and assigning available workers to busy ones**. It never holds tasks, never routes tasks, and never participates in computation.

Before the seed, the coordinator sends every worker its initial list of **waiting processes**: a binomial tree over ranks 1 to N-1, or the tree given to `set_custom_initial_topology`. From then on, a worker reports `RUNNING_STATE` when it starts and `AVAILABLE_STATE` when it runs out of work:

- When a running worker has no waiting process, the coordinator gives it an available one.
- When a worker becomes available, the coordinator assigns it to a running worker, chosen at random among those that have none waiting.

Each assignment reaches the busy worker as a `NEXT_PROCESS` message, and the next time that worker has a spare subtask, it sends it **directly** to the waiting process.

The critical consequence: tasks only travel to workers the coordinator has confirmed are idle. This eliminates the bounce-back problem that plagues decentralized strategies, where a task sent to a peer may arrive after that peer has already received work from somewhere else and must reject it, wasting a full round-trip.

### Communication model

The coordinator never waits for a worker to query it: it **pushes** a message the moment a relevant state changes, a new best value or a worker assignment. Workers pick these messages up between tasks with a non-blocking probe (`MPI_Iprobe`), so they learn of an assignment without asking for one.

### Network topology

<figure class="diagram">
--8<-- "assets/figures/topology-semi-centralized.svg"
</figure>

### Protocol walkthrough

<figure class="diagram">
--8<-- "assets/figures/protocol-semi-centralized.svg"
</figure>

The heart of the strategy:

1. Worker 1 starts the seed already knowing its waiting processes, W2 and W3, so it sends its first spare subtasks **directly** to them. The coordinator is not involved in the data transfer.
2. When W3 runs out of work, it reports `AVAILABLE_STATE`. The coordinator assigns it to W2, a running worker with nobody waiting, with a `NEXT_PROCESS` signal: **no task payload crosses the coordinator**.
3. W2 sends its next spare subtask to W3, and the cascade goes on.

Because the coordinator's status table is the single source of truth, and W3 was confirmed available before W2 sends to it, the task is always accepted. No bounce-back.

### How the run ends

Termination is **exact**: there is no timeout and no quiet period. Both topologies detect it with **Dijkstra–Scholten** acknowledgements:

- Every task a rank sends, the seed included, raises that rank's **deficit** by one, and every acknowledgement (`TASK_RECEIVED`) lowers it.
- A rank that receives a task while it has no **parent** makes the sender its parent, and holds that acknowledgement back. Any other task is acknowledged at once.
- A rank acknowledges its parent only once it is **passive**, with no task left to run, and its deficit is zero. That clears its parent.
- Rank 0 never takes a parent. So when its deficit reaches zero, every task ever sent has finished: the search is over, provably.

Rank 0 then sends `TERMINATION` to every worker. The message says how many score updates and assignments that worker should still expect, so each worker reads the ones in flight before it leaves, and it carries the run's `run_outcome`, so every rank returns the same answer from `scheduler::run`. A stop request travels on the same acknowledgements, so it reaches rank 0 before the deficit can reach zero (see [Stopping a Run](stopping-a-run.md)).

---

## Centralized

The coordinator is an active participant: it maintains a **bounded task queue**. Workers send their spare subtasks to it, and it dispatches them to available workers, highest priority first. The priority is a cheap proxy computed from the task's bytes: the number of set bits in the packet plus the runnable id.

The queue is bounded by compile-time limits: 1000 tasks per process, times the number of ranks, or 10 GB of memory. Past either one, the coordinator broadcasts `CENTER_IS_FULL`, and workers run their spare subtasks locally instead of sending them. Once the queue is back below 80% of the task limit and memory below 90%, it broadcasts `CENTER_IS_FREE`, and workers send again. **The coordinator never rejects a task it has received**: the backpressure happens before the send. Because branching algorithms are exponential, though, the queue saturates quickly in practice, and most tasks never enter it, which undermines the priority-based selection that is the approach's main advantage.

<figure class="diagram">
--8<-- "assets/figures/protocol-centralized.svg"
</figure>

At small process counts the centralized topology performs comparably to semi-centralized. At scale, the coordinator becomes the bottleneck: every task handoff, regardless of which two workers are involved, must traverse the coordinator twice (inbound + outbound). This is the behavior the semi-centralized design was built to avoid.

The centralized scheduler ends the run the same way, once its deficit is zero **and** its queue is empty. It ignores `set_custom_initial_topology`, since no task goes from worker to worker.

The centralized scheduler is kept in the library for reproducing the paper's comparison experiments and benchmarking custom scheduling strategies.

---

## Decentralized

!!! info "Not available in GemPBA"
    This topology is not implemented in the library. It is described here as background so the design choices of the semi-centralized strategy can be understood in context.

There is no central coordinator. Available cores are organized into a **core-tree**: the parent of core *r* is *r* − 2<sup>⌊log<sub>2</sub> *r*⌋</sup>, so the root holds the full initial instance and each core requests work from its parent when it becomes idle. If the parent has a pending task it sends the highest-priority sub-instance from its own search tree; if it has nothing, the request fails and the child must retry with a different ancestor.

<figure class="diagram">
--8<-- "assets/figures/topology-decentralized.svg"
</figure>

**Advantages over centralized:** no single routing bottleneck; no synchronization needed; communication overhead is low since cores never route through a shared queue.

**Drawbacks:**

- **Failed work requests.** A core's view of its parent's availability is stale. By the time a request arrives, the parent may have already sent its last task elsewhere; the request fails and the core wastes a full round-trip retrying. Under difficult graphs this accounts for a large fraction of total communication.
- **Skewed core-tree.** The root has ~log *c* neighbours while most leaves have none. Subtrees at leaf cores rarely receive help; the root's subtree is over-assisted.
- **No global best value.** Each core tracks only its local best, which may lag the true global optimum and fail to prune branches as aggressively as a globally informed worker could.
- **No global task priority.** A core picks the highest-priority task in its *own* subtree, not across the whole search space.

**How semi-centralized addresses both extremes:**

GemPBA's semi-centralized topology removes the bottleneck of the centralized approach and the failed-request / stale-view problems of the decentralized approach:

| | Centralized | Decentralized | Semi-centralized |
|---|---|---|---|
| Coordinator bottleneck | <span style="color:#d32f2f">Yes</span> | <span style="color:#388e3c">No</span> | <span style="color:#388e3c">No</span> |
| Tasks traverse coordinator | <span style="color:#d32f2f">Yes</span> | <span style="color:#388e3c">No</span> | <span style="color:#388e3c">No</span> |
| Global best value | <span style="color:#388e3c">Yes</span> | <span style="color:#f57c00">Partial</span> | <span style="color:#388e3c">Yes</span> |
| Spare tasks kept local | <span style="color:#f57c00">Yes, while the queue is full</span> | <span style="color:#388e3c">No</span> | <span style="color:#388e3c">No</span> |
| Request failures | <span style="color:#388e3c">No</span> | <span style="color:#d32f2f">Yes</span> | <span style="color:#388e3c">No</span> |
| Task priority | <span style="color:#f57c00">Queue-limited</span> | <span style="color:#d32f2f">Local only</span> | <span style="color:#388e3c">Global</span> |

---

## Summary

| | Semi-Centralized | Centralized |
|---|---|---|
| Coordinator role | Assigns idle workers to busy ones | Active task router |
| Task path | Worker → Worker (direct) | Worker → Coordinator → Worker |
| Coordinator sends | Lightweight assignment signals | Full task payloads |
| Communication model | Push-based | Queue and dispatch, with full/free backpressure |
| Bounce-back | Eliminated | None: a full coordinator stops the sends instead |
| Termination | Exact: Dijkstra–Scholten acknowledgements | Exact: acknowledgements, once the queue is empty |
| Coordinator bottleneck | No | Yes, at scale |
| Recommended for | Production | Benchmarking |
