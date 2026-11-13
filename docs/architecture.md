# Architecture

GemPBA's architecture (introduced in v3.0 and carried forward since) has one guiding principle: the public API should be simple and template-free, while everything underneath should be pluggable.

The pluggable design is the core of it. Every major component is defined by an interface: the load balancer, the scheduler, the node implementation. You can replace any of them without touching user code. The default implementations cover the common cases. If you have specialized hardware or a domain-specific scheduling strategy, you implement the interface and plug it in. A custom scheduler runs on MPI, the one backend gempba ships.

What this means in practice for a user: you include one header, call a handful of factory functions, and wrap your recursive branches in nodes. The template machinery (function signature matching, IPC serialization, thread pool management) lives in `detail/` and stays there. You write zero templates. The load balancer does not know your function signatures. The scheduler does not know your argument types. Everything is decoupled through interfaces, which is exactly why it can be this clean from the outside.

Since v5.0, that surface is one library. The core, `gempba::gempba`, has multithreading built in, and the MPI component, `gempba::mpi`, adds the schedulers that spread a run across MPI ranks. Consumer code reads the same either way: an MPI program creates its scheduler with `gempba::mpi::create_scheduler(...)` and passes it to `gempba::create_load_balancer(...)` and `gempba::create_node_manager(...)`, and a multithreading program passes none. A program asks for the component with `find_package(gempba COMPONENTS mpi)`, and the core and the component link into one program together.

The runtime also carries a built-in [telemetry](telemetry/index.md) subsystem beneath the public API, and the whole runtime is additionally exposed through a stable C ABI (`<gempba/cabi/gempba.h>`, plus `<gempba/cabi/gempba_mpi.h>` for the MPI component), which is what the [Java binding](java/index.md) sits on.

The [API Reference](reference/index.md) section documents each public header and what it does.
