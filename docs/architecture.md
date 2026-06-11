# Architecture

GemPBA's architecture (introduced in v3.0 and carried forward since) has one guiding principle: the public API should be simple and template-free, while everything underneath should be pluggable.

The pluggable design is the core of it. Every major component is defined by an interface: the load balancer, the scheduler, the node implementation. You can replace any of them without touching user code. The default implementations cover the common cases. If you have specialized hardware, a custom IPC transport, or a domain-specific scheduling strategy, you implement the interface and plug it in.

What this means in practice for a user: you include one header, call a handful of factory functions, and wrap your recursive branches in nodes. The template machinery (function signature matching, IPC serialization, thread pool management) lives in `detail/` and stays there. You write zero templates. The load balancer does not know your function signatures. The scheduler does not know your argument types. Everything is decoupled through interfaces, which is exactly why it can be this clean from the outside.

Since v4.0, the same surface is delivered in two flavors. The `gempba::multithreading` and `gempba::multiprocessing` namespaces expose flavor-specific factories, and the installed flavor's namespace is `inline`, so consumer code reads identically in both: `gempba::create_load_balancer(...)`, `gempba::create_node_manager(...)`. The flavor is picked at `find_package` time, not at every call site.

The runtime also carries a built-in [telemetry](telemetry/index.md) subsystem beneath the public API, and the whole runtime is additionally exposed through a stable C ABI (`<gempba/cabi/gempba.h>`), which is what the [Java binding](java/index.md) sits on.

The [API Reference](reference/index.md) section documents each public header and what it does.
