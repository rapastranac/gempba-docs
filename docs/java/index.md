# GemPBA for Java

GemPBA is a Maven dependency. Drop it into a `pom.xml`, write `import io.gempba.*`, and call the same scheduler family, load balancer, and node manager you would from C++ — just from Java this time. If you have a JVM pipeline, a Spark job, an Airflow operator, or an enterprise application where C++ was the wrong language but you still wanted GemPBA's scheduler, this is the bridge.

!!! info "Available from `v4.1.0`"
    The Java binding landed in `v4.1.0`. Earlier tags predate the publish flow and have no artifact on the registry.

## What you get

- **One fat JAR per flavor.** Each published JAR carries the native binaries for Linux, Windows, and macOS *inside the artifact*, under `natives/<os>-<arch>/`. A `NativeLoader` picks the right binary at runtime — no per-platform build dance, no classifier juggling, no `LD_LIBRARY_PATH` footnote. The same JAR runs unchanged on any supported platform.
- **Two flavors, one API.** Pick a classifier: `mt` (multithreading — self-contained, no MPI needed) or `mp-mpi` (multiprocessing — requires an MPI runtime on the host). The Java surface mirrors the C++ one: `GemPBA.createLoadBalancer(...)`, `GemPBA.createNodeManager(...)`, and so on.
- **Built on a stable C ABI.** Underneath the JNI layer sits an `extern "C"` surface (`<gempba/cabi/gempba.h>`) covering the full runtime. The Java binding is its first consumer; the same headers are what any future Python / Rust / .NET binding will sit on.

## Why you serialize arguments

C++ leans on templates to accept any task signature; Java can't, so the binding moves task arguments and results across the language boundary as **bytes** rather than typed values. You provide that translation as a `Serializer` / `Deserializer` pair when you seed the search — a small, honest tax for driving a native scheduler from the JVM.

In practice it is lighter than it sounds: on a single machine only the **seed** is serialized, because child nodes capture their arguments straight from the Java closure. See **[How it works](how-it-works.md)** for the full story — how GemPBA reuses its `task_packet` transport to make this work, and why the cost lands where it does.

## Supported platforms

The fat JAR bundles one architecture per OS:

| OS | Architecture |
|---|---|
| Linux | `x86_64` |
| Windows | `x86_64` |
| macOS | `aarch64` (Apple Silicon) |

## The `io.gempba` API at a glance

| Package | Key types |
|---|---|
| `io.gempba` | `GemPBA` — factories and entry points (`createLoadBalancer`, `createNodeManager`, `createSeedNode`, `shutdown`, …) |
| `io.gempba.core` | `LoadBalancer`, `NodeManager`, `Node` |
| `io.gempba.value` | `Score`, `ScoreType`, `Goal`, `BalancingPolicy` |
| `io.gempba.task` | `NodeTask`, `VoidNodeTask`, `Serializer`, `Deserializer` functional interfaces |
| `io.gempba.scheduler` | `Scheduler`, `SchedulerTopology`, `SerialRunnable` *(multiprocessing classifier only)* |
| `io.gempba.stats` | `RankStats` |

## Next steps

- **[Installation](installation.md)** — add the GitHub Packages registry, authenticate, and declare the dependency.
- **[Quick Start](quick-start.md)** — a complete multithreading program, walked through end to end.
- **[Examples](examples.md)** — the runnable `gempba-java-examples` catalog.
- **[How it works](how-it-works.md)** — how the binding leverages `task_packet` to bridge the JVM and the native runtime.
