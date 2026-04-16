# Implementations

Built-in concrete implementations of GemPBA's pluggable interfaces. These are what you get out of the box. Each one can
be replaced by passing a custom implementation to the corresponding factory function.

## Load balancer

| Implementation                                         | Interface       | Notes                                                                                      |
|--------------------------------------------------------|-----------------|--------------------------------------------------------------------------------------------|
| [Quasi-Horizontal](load-balancers/quasi-horizontal.md) | `load_balancer` | Recommended. Pushes root-level work first to maximize CPU utilization on unbalanced trees. |
| [Work-Stealing](load-balancers/work-stealing.md)       | `load_balancer` | Baseline. Direct queue submission, no tree awareness.                                      |

## Scheduler

| Implementation                                         | Interface   | Transport | Notes                                                             |
|--------------------------------------------------------|-------------|-----------|-------------------------------------------------------------------|
| [MPI Semi-Centralized](schedulers/semi-centralized.md) | `scheduler` | OpenMPI   | Recommended. Center assigns workers; tasks travel point-to-point. |
| [MPI Centralized](schedulers/centralized.md)           | `scheduler` | OpenMPI   | Benchmarking only. All tasks route through the center.            |

## Stats

| Implementation                                  | Interface | Transport | Notes                                    |
|-------------------------------------------------|-----------|-----------|------------------------------------------|
| [Default MPI](stats/default-mpi-stats.md)       | `stats`   | OpenMPI   | Built-in metrics for MPI scheduler runs. |

## Stats visitors

| Implementation                                                | Interface       | Notes                        |
|---------------------------------------------------------------|-----------------|------------------------------|
| [Default MPI](stats-visitors/default-mpi-stats-visitor.md) | `stats_visitor` | Built-in readout formatters. |
