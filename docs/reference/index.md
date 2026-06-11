# API Reference

GemPBA's public surface is intentionally small.

!!! tip "Not writing C++?"
    This section documents the C++ API, but the same runtime is also a Maven dependency: the [**Java**](../java/index.md) section covers the `io.gempba` surface, installation, and a full quick start. The two APIs mirror each other (`create_load_balancer` becomes `createLoadBalancer`, and so on), so this reference doubles as the conceptual map for Java readers.

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
| [Stats](implementations/stats/default-mpi-stats.md)                           | `stats`         | Default stats for MPI schedulers |
| [Stats Visitors](implementations/stats-visitors/default-mpi-stats-visitor.md) | `stats_visitor` | Built-in metric formatters       |

## Telemetry

The runtime carries a built-in telemetry subsystem under `include/gempba/telemetry/` (`telemetry_hub`, frame and topology structs, transports). It has its own documentation section rather than per-header reference pages: see [Telemetry](../telemetry/index.md) for the concepts, [Configuration](../telemetry/configuration.md) for the runtime API (`disable`/`enable`, `configure_port`, cadence control), and [Data model](../telemetry/data-model.md) for the frame contract.

## C ABI

`<gempba/cabi/gempba.h>` exposes the full runtime as a stable `extern "C"` surface: opaque handles, status codes, and callback registration. It exists so non-C++ front-ends can drive GemPBA; the [Java binding](../java/how-it-works.md) is its first consumer. For a code-level walkthrough, the [GemPBA DeepWiki](https://deepwiki.com/rapastranac/gempba) covers it in depth.
