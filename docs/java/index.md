---
description: GemPBA for Java parallelizes branching algorithms from the JVM, on threads and MPI. On Maven Central as io.github.rapastranac:gempba and gempba-mpi, with no repository or token, natives inside the JAR.
---

# GemPBA for Java

GemPBA's core is C++, for speed, and its Java API puts that same core in your JVM. It's on **Maven Central**, with no repository or token to configure:

```xml
<dependency>
  <groupId>io.github.rapastranac</groupId>
  <artifactId>gempba</artifactId>        <!-- or gempba-mpi -->
  <version>5.0.0</version>
</dependency>
```

Write `import io.gempba.*` and call the same load balancers, node manager and schedulers you would from C++, from Java this time. If you have a JVM pipeline, a Spark job, an Airflow operator, or an enterprise application where C++ was the wrong language but you still wanted GemPBA's scheduler, this is the bridge.

!!! info "On Maven Central from `v5.0.0`"
    The Java binding landed in `v4.1.0`. From `v5.0.0` it's on Maven Central as `io.github.rapastranac:gempba` and `gempba-mpi`, in the `io.gempba` packages.

## What you get

- **Natives inside the JAR.** Each published JAR carries the native binaries for Linux, Windows, and macOS *inside the artifact*, under `natives/<os>-<arch>/`. A `NativeLoader` picks the right binary at runtime — no per-platform build dance, no classifier juggling, no `LD_LIBRARY_PATH` footnote. The same JAR runs unchanged on any supported platform.
- **Two artifacts, one API.** Pick `gempba` (no MPI needed) or `gempba-mpi` (adds MPI schedulers, requires an MPI runtime on the host). The Java surface mirrors the C++ one: `GemPBA.createLoadBalancer(...)`, `GemPBA.createNodeManager(...)`, and so on.
- **Built on a C ABI.** Underneath the JNI layer sits an `extern "C"` surface (`<gempba/cabi/gempba.h>`, and `gempba_mpi.h` for MPI) covering the full runtime. The Java binding is its first consumer; the same headers are what any future Python / Rust / .NET binding will sit on.

## Why you serialize arguments

C++ leans on templates to accept any task signature; Java can't, so the binding moves task arguments and results across the language boundary as **bytes** rather than typed values. You provide that translation as a `Serializer` / `Deserializer` pair when you seed the search — a small, honest tax for driving a native scheduler from the JVM.

In practice it is lighter than it sounds: on a single machine only the **seed** is serialized, because child nodes capture their arguments straight from the Java closure. See **[How it works](how-it-works.md)** for the full story — how GemPBA reuses its `task_packet` transport to make this work, and why the cost lands where it does.

## Supported platforms

The JARs bundle one architecture per OS:

| OS | Architecture |
|---|---|
| Linux | `x86_64` |
| Windows | `x86_64` |
| macOS | `aarch64` (Apple Silicon) |

## The `io.gempba` API at a glance

For the complete catalog, see the [Class Index](class-index.md) and [File Index](file-index.md).

| Package | Key types |
|---|---|
| `io.gempba` | `GemPBA` — factories and entry points (`createLoadBalancer`, `createNodeManager`, `createSeedNode`, `requestStop`, `shutdown`, …) |
| `io.gempba.core` | `LoadBalancer`, `NodeManager`, `Node` |
| `io.gempba.value` | `Score`, `ScoreType`, `Goal`, `BalancingPolicy`, `RunOutcome`, `EndReason`, `StopTrigger` |
| `io.gempba.task` | `NodeTask`, `VoidNodeTask`, `Serializer`, `Deserializer` functional interfaces |
| `io.gempba.scheduler` | `Scheduler`, `SerialRunnable`, `SerialTask` |
| `io.gempba.mpi` | `Mpi`, `SchedulerTopology` *(`gempba-mpi` only)* |
| `io.gempba.stats` | `RankStats` |

## Next steps

- **[Installation](installation.md)** — declare the Maven Central dependency.
- **[Quick Start](quick-start.md)** — a complete multithreading program, walked through end to end.
- **[Examples](examples.md)** — the runnable `gempba-java-examples` catalog.
- **[Stopping a Run](../stopping-a-run.md)**: stop a run early, by signal, from code or from the dashboard, and read how it ended.
- **[How it works](how-it-works.md)** — how the binding leverages `task_packet` to bridge the JVM and the native runtime.
- **[Class Index](class-index.md)** / **[File Index](file-index.md)**: every public `io.gempba` type, and where it lives in the source tree.
