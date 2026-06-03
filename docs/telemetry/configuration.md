# Configuring telemetry

Telemetry is **on by default** and needs no setup to start streaming. This page covers the three things you may want to change: whether it runs at all, which port the dashboard channel binds, and how often frames are emitted.

## Turning it off (and on)

The kill switch is a process-local, sticky flag. Set it **before** the first `node_manager` / `scheduler` is created, i.e. before the hub is installed.

=== "C++"

    ```cpp
    #include <gempba/gempba.hpp>

    gempba::telemetry::disable();      // no hub is installed; no pump thread, no socket
    // ... create_load_balancer / create_node_manager / create_scheduler ...

    gempba::telemetry::enable();       // lift a prior disable
    bool on = gempba::telemetry::is_enabled();
    ```

=== "Java"

    ```java
    import io.gempba.GemPBA;

    GemPBA.disableTelemetry();
    // ... createLoadBalancer / createNodeManager ...

    GemPBA.enableTelemetry();
    boolean on = GemPBA.isTelemetryEnabled();
    ```

!!! warning "Set it symmetrically across all ranks"
    The flag is **process-local**. In `mp-mpi`, disabling telemetry on only *some* ranks will deadlock the still-enabled ranks during transport setup (the MPI transport sets up collectively). Call `disable()` on **every** rank, or none. The recommended pattern is to disable on all ranks before any `create_*` entry point.

## The dashboard port

The center role binds a loopback-only TCP server for the dashboard channel, at `127.0.0.1:9000` by default. Change it before the hub is installed:

```cpp
gempba::telemetry::configure_port(9100);   // must be called before the first node_manager / scheduler
```

The server binds **loopback only** by design; it is never exposed on a public interface. To reach it from another machine, tunnel over SSH (see [Connecting](connecting.md)).

!!! note "Example binaries expose `-telemetry_port`"
    The `gempba-examples` programs forward a `-telemetry_port <n>` command-line argument to `configure_port`. That flag is an example-binary convention, not part of the library API; in your own code, call `configure_port` directly.

## Emission cadence and live control

Each worker emits a frame on a cadence; defaults are **500 ms** for worker frames and **1000 ms** for per-host (node) frames. These can be changed in code, or **live from a connected client**: the dashboard channel accepts control messages so a UI can throttle the stream without restarting the run.

| Control | Effect |
|---|---|
| `SET_WORKER_INTERVAL_MS` | Reset the worker-frame cadence (fans out to all workers) |
| `SET_NODE_INTERVAL_MS` | Reset the node-frame cadence |
| `BE_NODE_SENTINEL` | Promote a worker to its host's sentinel, so it begins emitting node frames |

In code, the equivalent setters live on the hub:

```cpp
auto* hub = gempba::telemetry::get();      // nullptr if telemetry is disabled
if (hub) {
    hub->set_worker_interval_ms(250);
    hub->set_node_interval_ms(2000);
}
```

A faster cadence gives a more responsive dashboard at the cost of more frames on the wire; a slower cadence is cheaper for long unattended runs. Because the interval is client-controllable, a dashboard can dial it up while you are watching and back down when you are not.
