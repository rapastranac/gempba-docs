# Interfaces

These are the pluggable contracts of GemPBA. Each one defines what an implementation must do without prescribing how. You interact with them if you are replacing a built-in component with a custom one — a GPU-backed node, a domain-specific scheduling strategy.

| Interface | Purpose |
|---|---|
| [`node_core`](node-core.md) | The abstract node — owns an instance, tracks tree position, manages lifecycle |
| [`node_traits`](node-traits.md) | The full interface contract every node must satisfy |
| [`load_balancer`](load-balancer.md) | Thread-level work distribution within a process |
| [`scheduler`](scheduler.md) | Process-level coordination over MPI — every rank calls its `run` |
| [`serial_runnable`](serial-runnable.md) | Type erasure for functions that cross process boundaries |
| [`stats`](stats.md) | Runtime metrics collection |
| [`stats_visitor`](stats-visitor.md) | Format-agnostic readout of collected metrics |
