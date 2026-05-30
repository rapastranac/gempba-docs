# How the binding works

GemPBA's scheduler, load balancer, and thread pool all run in native C++. The Java binding doesn't reimplement any of that — it is a typed front-end that calls into the native runtime and lets the runtime call back. The single idea that makes that round trip possible is a type GemPBA already had for an entirely different reason: **`task_packet`**.

## Bytes, not types

In C++, GemPBA leans on templates: your task can have any argument types, and the compiler bakes a concrete, fully typed function for each one. Java has no equivalent — generics are erased at runtime, and there is no way to synthesize a native call to fit arbitrary JVM types.

So the binding stops trying to move *typed arguments* across the language boundary and moves *bytes* instead. `task_packet` is the buffer those bytes ride in.

The elegant part is that this buffer was not invented for Java. GemPBA already used `task_packet` to ship a node's payload **between MPI ranks**, where work genuinely has to leave one process as raw bytes and be reconstructed in another. The Java binding simply reuses that same channel: whenever a task's argument or result crosses between the JVM and native code, it travels as a `task_packet`. Nothing about the transport is Java-specific — it's the same packet, pointed at a new destination.

## What crosses, and when

You supply two small functions when you seed the search — a `Serializer` (your argument → bytes) and a `Deserializer` (bytes → your argument). That pair is the only translation the binding needs.

- **Into native code.** The seed's argument is serialized into a `task_packet` and handed to the runtime. When a worker thread later runs the task, the binding feeds the packet back through your `Deserializer` and calls your code.
- **Back out.** A result that has to cross back travels as bytes too, reconstructed through a `Deserializer` on arrival.
- **Children stay home (multithreading).** A child node created inside a running task captures its arguments in the Java closure — they're already on the JVM heap, so no packet is built. Only the **seed** makes the initial crossing.
- **Children travel (multiprocessing).** When work is distributed across processes, a child may be dispatched to another rank — and there the `task_packet` does its original job, carrying the node's payload over the wire.

That asymmetry is the whole cost model: on one machine you pay the serialization tax once, for the seed; across machines you pay it wherever work actually moves — which is exactly where `task_packet` was always meant to be paid.

## The price in practice

So what does the serialization tax actually cost? Below is the same synthetic benchmark — a binary tree of depth 25 (**33,554,432** leaves) with identical per-node work — run in C++ and in Java on one 24-core machine (no SMT). The multithreading runs use a single 24-thread pool; the multiprocessing runs use 7 MPI ranks (6 workers × 4 threads + 1 center, semi-centralized) so both modes field the same 24 worker threads.

| Mode | Layout | C++ | Java | Java vs C++ |
|---|---|---|---|---|
| Multithreading | 1 process × 24 threads | 142.07 s | 141.47 s | −0.4 % (par) |
| Multiprocessing | 6 × 4 workers + 1 center | 201.76 s | 214.29 s | +6.2 % |

All four runs returned the identical result — a leaf count of **33,554,432** — so each walked exactly the same tree. The time difference is binding overhead and nothing else.

The shape is what you would hope for. On a single machine the overhead vanishes into measurement noise — Java came in a hair *ahead* of C++ on this run, which is just another way of saying the two are indistinguishable. Across processes, where every task handed to another rank is genuinely serialized and shipped, the cost becomes visible but stays in single digits, around 6 %. You pay essentially nothing to stay on one machine, and a small, bounded premium for the one operation that inherently needs serialization: moving work between processes.

!!! note "About these numbers"
    Single representative runs at depth 25 with the semi-centralized scheduler, on one host. Per-rank elapsed times were tightly clustered (the load was well balanced), and the workload is compute-heavy by design, so it reflects a realistic job rather than a micro-benchmark. Expect variation with per-node cost, topology, and hardware.

## The same code scales from one machine to many

Here is the part worth internalizing: the `Serializer` / `Deserializer` pair you write for a single-machine (`mt`) program is *exactly* what a distributed (`mp-mpi`) program needs — because under the hood it is the same `task_packet` doing the same job, only travelling farther.

So the habit you build on day one is the habit that scales. Your MT code already speaks in serializable arguments; when a problem outgrows one machine you switch the dependency classifier to `mp-mpi`, launch under `mpiexec`, and the task logic you already wrote keeps working. There is no rewrite, no second mental model, no "now go serialize everything" migration — you did that part from the start, almost without noticing. The serialization step you paid for on a single machine *is* your upgrade path: going distributed becomes a configuration change, not a port — and, as the numbers above show, one that costs only a few percent.

## Going deeper

This page is the idea, not the wiring. For the detailed architecture — the JNI layer, the stable C ABI the binding sits on, handle ownership, and how a native worker thread calls back into the JVM — see the **[GemPBA DeepWiki](https://deepwiki.com/rapastranac/gempba)**.

!!! note
    The DeepWiki is auto-generated and may briefly lag the latest release; it refreshes periodically.
