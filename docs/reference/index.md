# API Reference

GemPBA's public surface is intentionally small.

## Facade and concrete types

|                                            | Purpose                                                                     |
|--------------------------------------------|-----------------------------------------------------------------------------|
| [`gempba`](defaults/gempba-hpp.md)         | The only header you need — facade, factory functions, global accessors      |
| [`node_manager`](defaults/node-manager.md) | Control panel: configure goal, submit work, wait, collect results           |
| [`node`](defaults/node.md)                 | Concrete final class — user-facing handle to a branch in the recursion tree |

## [Interfaces](interfaces/interfaces.md)

Pluggable contracts. Implement one to replace a built-in component.

|                                                    | Purpose                                                                   |
|----------------------------------------------------|---------------------------------------------------------------------------|
| [`node_core`](interfaces/node-core.md)             | Abstract node — owns an instance, tracks tree position, manages lifecycle |
| [`node_traits`](interfaces/node-traits.md)         | Full interface contract every node must satisfy                           |
| [`load_balancer`](interfaces/load-balancer.md) | Thread-level work distribution within a process                           |
| [`scheduler`](interfaces/scheduler.md)             | Process-level coordination — transport-agnostic IPC contract              |
| [`serial_runnable`](interfaces/serial-runnable.md) | Type erasure for functions crossing process boundaries                    |
| [`stats`](interfaces/stats.md)                     | Runtime metrics collection                                                |
| [`stats_visitor`](interfaces/stats-visitor.md)     | Format-agnostic readout of collected metrics                              |

## [Implementations](implementations/implementations.md)

Built-in concrete implementations of the above interfaces.

|                                                                               | Interface       | Notes                            |
|-------------------------------------------------------------------------------|-----------------|----------------------------------|
| [Quasi-Horizontal](implementations/load-balancers/quasi-horizontal.md)        | `load_balancer` | Recommended thread scheduler     |
| [Work-Stealing](implementations/load-balancers/work-stealing.md)              | `load_balancer` | Benchmarking baseline            |
| [MPI Semi-Centralized](implementations/schedulers/semi-centralized.md)        | `scheduler`     | Recommended process scheduler    |
| [MPI Centralized](implementations/schedulers/centralized.md)                  | `scheduler`     | Benchmarking baseline            |
| [Stats](implementations/stats/default-mpi-stats)                              | `stats`         | Default stats for mpi schedulers |
| [Stats Visitors](implementations/stats-visitors/default-mpi-stats-visitor.md) | `stats_visitor` | Built-in metric formatters       |
