---
description: GemPBA's v5 architecture. One C++ core with multithreading built in, an MPI component compiled against your MPI, one scheduler::run entry point on every rank, exact termination, and a Java API on Maven Central.
---

# Architecture

GemPBA is a high-performance C++ core with a Java API and a C ABI on top. Since v3.0 it has followed one guiding principle: the public API should be simple and template-free, while everything underneath should be pluggable. v5.0.0 takes that to the packaging and the entry point: one library, one way to start a run, and MPI only when you ask for it.

## One core, plus a component

<figure class="diagram">
--8<-- "assets/figures/architecture-v4-v5.svg"
</figure>

Up to v4, you chose a **flavor** when you built gempba: multithreading or MPI, each with its own namespace (`gempba::multithreading`, `gempba::multiprocessing`) and its own library, and one program could never use both. v5 replaces the flavors with **one core**, `gempba::gempba`, which has multithreading built in: the nodes, the node manager, the load balancers, the thread pool, the `scheduler` interface, telemetry and the C ABI. The **MPI component**, `gempba::mpi`, adds the schedulers that spread a run across MPI ranks, and a program asks for it with `find_package(gempba COMPONENTS mpi)`. Multithreading and MPI programs build side by side from one installation, and the calls read the same in both: an MPI program creates its scheduler with `gempba::mpi::create_scheduler(...)` and passes it to `gempba::create_load_balancer(...)` and `gempba::create_node_manager(...)`, and a multithreading program passes none.

The core is a shared library, `libgempba.so.5` on Linux and `libgempba.dll` on Windows. It exports only its public API: spdlog and fmt are compiled into it, hwloc is a private dependency it loads at run time, and its public headers include only the C++ standard library. Your build looks for nothing else.

## MPI, built against yours

<figure class="diagram">
--8<-- "assets/figures/architecture-mpi-component.svg"
</figure>

The MPI component installs as **source**. `find_package(gempba COMPONENTS mpi)` compiles it in your build into a static `gempba::mpi`, against the MPI CMake finds there: Open MPI, MPICH or MS-MPI. Before v5, each package's MPI part was compiled against one MPI and worked only with it. Two things follow:

- Your compiler must be compatible with the one that built libgempba.
- Switching MPIs takes another build directory, not a reinstall.

The Java artifacts can't compile anything on your machine, so `gempba-mpi`'s bundled native targets one MPI per OS, Open MPI on Linux and macOS and MS-MPI on Windows, and `-Dgempba.native.path` loads one you built against another (see [Which MPI](java/installation.md#which-mpi)).

## One entry point on every rank

<figure class="diagram">
--8<-- "assets/figures/architecture-one-entry-point.svg"
</figure>

Every rank calls the same function, `scheduler::run`, and only rank 0 passes the seed:

```cpp
#include <gempba/gempba.hpp>
#include <gempba/mpi.hpp>

auto* scheduler = gempba::mpi::create_scheduler(gempba::mpi::SEMI_CENTRALIZED);
auto* lb        = gempba::create_load_balancer(gempba::QUASI_HORIZONTAL, scheduler);
auto& nm        = gempba::create_node_manager(lb, scheduler);

std::optional<gempba::task_bundle> seed;
if (scheduler->is_root()) {
    seed.emplace(seed_packet, runnable_id);          // rank 0 only
}
const gempba::run_outcome outcome = scheduler->run(nm, runnables, std::move(seed));

if (scheduler->is_root()) {
    gempba::task_packet best = scheduler->get_result();
}
return gempba::shutdown();
```

`run` throws `std::invalid_argument` if rank 0 passes no seed or another rank passes one, and `get_result()` and `get_all_results()` throw `std::logic_error` off rank 0. The built-in schedulers keep rank 0 as their coordinator, out of the computation; a [custom scheduler](reference/interfaces/scheduler.md#custom-implementation) implements the protected `do_run`, `do_get_result` and `do_get_all_results`. Java has the same shape: `Scheduler.run(nm, runnables, seed, seedRunnableId)` on rank 0 and `run(nm, runnables)` elsewhere.

## Exact termination

An MPI run ends **exactly when its work is done**, with no timeout and no quiet period to wait out. Since v4.3.0, both schedulers detect termination with **Dijkstra–Scholten** acknowledgements: every task sent is acknowledged, a rank acknowledges the task that woke it only once its own work and everything it sent are finished, and rank 0, which never waits on anyone, knows the search is over when its last acknowledgement arrives. So a run can't end early with a task in flight, or late because a message was slow. [How the run ends](scheduler-topologies.md#how-the-run-ends) walks through it, and v5.0.0 removed the old timeout parameter from `create_scheduler`.

## How a run ends

<figure class="diagram">
--8<-- "assets/figures/architecture-run-ends.svg"
</figure>

A run can also be stopped early, from code, by a signal or from a dashboard, and it says which of the three ways it ended. [Stopping a Run](stopping-a-run.md) covers each trigger in C++ and Java.

## Pluggable underneath

Every major component is defined by an interface: the load balancer, the scheduler, the node implementation. You can replace any of them without touching user code. The default implementations cover the common cases; if you have specialized hardware or a domain-specific scheduling strategy, you implement the interface and plug it in. A custom scheduler runs on MPI, the one backend gempba ships.

What this means in practice: a multithreading program includes one header, `<gempba/gempba.hpp>`, and an MPI program adds `<gempba/mpi.hpp>`. You call a handful of factory functions and wrap your recursive branches in nodes, naming your function's types when you create one. The template machinery (function signature matching, IPC serialization, thread pool management) lives in `detail/` and stays there. The load balancer does not know your function signatures. The scheduler does not know your argument types. Everything is decoupled through interfaces, which is exactly why it can be this clean from the outside.

## Telemetry, the C ABI and Java

The runtime carries a built-in [telemetry](telemetry/index.md) subsystem beneath the public API, which the [GemPBA Dashboard](telemetry/dashboard.md) reads live. The whole runtime is also exposed through a C ABI, `<gempba/cabi/gempba.h>` plus `<gempba/cabi/gempba_mpi.h>` for the MPI component, and the [Java API](java/index.md) sits on it: the same core, from the JVM, on Maven Central.

The [API Reference](reference/index.md) section documents each public header and what it does.
