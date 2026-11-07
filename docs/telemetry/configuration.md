# Configuring telemetry

Telemetry is **on by default** and needs no setup to start streaming. This page covers what you may want to change or add: whether it runs at all, which port the dashboard channel binds, how often frames are emitted, and the context you attach to a run.

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

The aggregator (rank 0) binds a loopback-only TCP server for the dashboard channel, at `127.0.0.1:9000` by default. Change it before the hub is installed:

=== "C++"

    ```cpp
    gempba::telemetry::configure_port(9100);   // must be called before the first node_manager / scheduler
    ```

=== "Java"

    ```java
    GemPBA.configureTelemetryPort(9100);       // available from v4.1.3, both flavors
    ```

The server binds **loopback only** by design; it is never exposed on a public interface. To reach it from another machine, use the [GemPBA Dashboard](dashboard.md), which opens the SSH forward for you (see [Connecting](connecting.md)).

!!! note "Example binaries expose `-telemetry_port`"
    The `gempba-examples` programs forward a `-telemetry_port <n>` command-line argument to `configure_port`. That flag is an example-binary convention, not part of the library API; in your own code, call `configure_port` directly.

## Emission cadence and live control

gempba v4.3.0 uses **one telemetry interval**. Rank frames, per-host (node) frames and the aggregator's broadcast all refresh on it: **500 ms** by default, clamped to 50–600000 ms. Change it in code, or **live from a connected client**, so a UI can throttle the stream without restarting the run.

A connected client writes control lines back on the same socket, one JSON object per line:

| Control line | Effect |
|---|---|
| `{"kind":"set_interval_ms","value":N}` | Set the interval to `N` ms, for rank frames, node frames and the broadcast alike. |
| `{"kind":"set_worker_interval_ms","value":N}` | The schema-1 name for the same thing; accepted until v5.0.0. |
| `{"kind":"set_node_interval_ms","value":N}` | Accepted and ignored since v4.3.0, now that node frames follow the one interval; removed in v5.0.0. |
| `{"kind":"pause"}` | Stop every rank sending frames. Counters keep counting, and the aggregator keeps sending a short `"paused":true` line so the run does not look lost. |
| `{"kind":"resume"}` | Resume at the current interval. |
| `{"kind":"snapshot"}` | Make every rank send one frame at once, whatever the interval and even while paused; the aggregator then broadcasts one full line. |
| `{"kind":"mark","label":"..."}` | Record a timestamped marker on the run, labelled as you choose. |

In code, the equivalent setter lives on the hub:

```cpp
auto* hub = gempba::telemetry::get();      // nullptr if telemetry is disabled
if (hub) {
    hub->set_interval_ms(250);             // rank frames, node frames and the broadcast
}
```

The in-process control enum is `control_kind::SET_INTERVAL_MS`. The old `set_worker_interval_ms()` and `control_kind::SET_WORKER_INTERVAL_MS` still compile, with a deprecation warning, and forward to these until v5.0.0; `set_node_interval_ms()` does nothing and is removed in v5.0.0.

A faster interval gives a more responsive dashboard at the cost of more frames on the wire; a slower one is cheaper for long unattended runs. Because the interval is client-controllable, a dashboard can dial it up while you are watching and back down when you are not.

## Annotating and marking a run

Two C++ calls attach context to a run, so the dashboard and any consumer can describe it and line events up against a timeline. Both reach the stream's `run` object (see [Data model](data-model.md)).

```cpp
gempba::telemetry::annotate_run("experiment", "bitset-v3");  // up to 8 key/value pairs
gempba::telemetry::mark_run("phase 2 started");              // a timestamped marker
```

- `annotate_run(key, value)` records up to **8** key/value strings (keys 1–32 bytes, values up to 64), shown under `run.annotations`. Set them before or during the run; setting a key again overwrites it.
- `mark_run(label)` records a timestamped marker under `run.markers`, tagged `source` `"code"` (labels 1–64 bytes, at most 32 per run). A connected client records one the same way with the `{"kind":"mark","label":"..."}` control line, tagged `source` `"dashboard"`.
