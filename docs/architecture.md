# The v3.0 Architecture

The v3.0 redesign has one guiding principle: the public API should be simple and template-free, while everything underneath should be pluggable.

The pluggable architecture is the core innovation of this release. Every major component is defined by an interface: the load balancer, the scheduler, the node implementation. You can replace any of them without touching user code. The default implementations cover the common cases. If you have specialized hardware, a custom IPC transport, or a domain-specific scheduling strategy, you implement the interface and plug it in.

What this means in practice for a user: you include one header, call a handful of factory functions, and wrap your recursive branches in nodes. The template machinery (function signature matching, IPC serialization, thread pool management) lives in `detail/` and stays there. You write zero templates. The load balancer does not know your function signatures. The scheduler does not know your argument types. Everything is decoupled through interfaces, which is exactly why it can be this clean from the outside.

The [API Reference](reference/index.md) section documents each public header and what it does.
