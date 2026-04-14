# Scheduler Topologies

GemPBA ships with two scheduler topologies for multiprocessing. The default recommendation is `SEMI_CENTRALIZED`. The `CENTRALIZED` topology is included for comparison.

```cpp
// Semi-centralized (recommended)
auto* s = gempba::mp::create_scheduler(gempba::mp::scheduler_topology::SEMI_CENTRALIZED);

// Centralized (for comparison)
auto* s = gempba::mp::create_scheduler(gempba::mp::scheduler_topology::CENTRALIZED);
```

## Semi-Centralized (recommended)

Rank 0 acts as a coordinator that routes tasks between workers but does not participate in computation. Workers request work from the center when their queues run dry. This keeps the coordinator lightweight and scales better as the number of worker ranks grows.

## Centralized

The center takes a more active role in routing decisions. At small process counts it can perform comparably, but it becomes a bottleneck at scale because all task routing goes through a single point. It is kept in the library primarily as a baseline for the performance comparisons in the original paper.

If you are not sure which to use, go with `SEMI_CENTRALIZED`. The centralized scheduler is there when you need to reproduce the paper's comparison experiments or benchmark your own scheduling strategy against it.
