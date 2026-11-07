# Data model

Telemetry is exposed two ways, and both carry the same information:

- **In process**, as C++ frame structs (`<gempba/telemetry/frames.hpp>`, `topology.hpp`) for a consumer compiled into the same binary, such as a custom `telemetry_transport`.
- **Over the socket**, as a line-delimited **JSON broadcast** on the dashboard channel, for everything else.

This page is a map of what a broadcast line carries. The authoritative, field-by-field reference, with each key's unit and the release that added it, every control line, the compatibility rules and every schema version, lives in gempba's [`docs/telemetry/wire-format.md`](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/wire-format.md). This page links there rather than keeping a second copy in sync.

## Schema 2

gempba v4.3.0 sends **schema 2**: every line carries `"version": 2`. A consumer written against an older release reads that release's schema, which stays valid for it. wire-format.md lists [every schema version](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/wire-format.md#schema-versions), newest first, and the compatibility rules: a consumer ignores keys it does not know, and a renamed, removed or redefined key bumps `version`.

## What a line carries

The aggregator (rank 0) emits one JSON object per line, every telemetry interval. A full line is self-contained, so a client that connects late misses nothing but history:

- an **envelope**: `version`, `run_id`, `ts`, `elapsed_seconds`, `paused` and `final`;
- the **topology**: each host, each rank's identity with its `role` (`coordinator` or `worker`), and a `run` object holding the run's setup, its annotations and its markers;
- **`ranks`**: the latest frame from every rank, whatever its role: task counters, where its pool threads' idle time went (starved versus imbalanced), scheduler timing, the cost of moving tasks, and an `edges_out` list of the ranks it sent tasks to;
- **`nodes`**: the latest per-host frame from each host's sentinel rank: CPU, memory, and the job's own memory within its cgroup.

While the run is paused, a line carries only the envelope header with `"paused": true`. The line sent at shutdown carries the run's totals and `"final": true`, and is the last before the aggregator closes the connection. See [the full worked example and every field](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/wire-format.md#example).

## Controlling the stream

The socket is bidirectional: a client writes control lines back, one JSON object per line, to set the telemetry interval or to pause, resume, snapshot or mark the run. [Configuration](configuration.md#emission-cadence-and-live-control) covers them from the runtime side; wire-format.md gives [the exact lines a client sends](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/wire-format.md#control-lines).

## JSON keys versus C++ struct fields

The JSON keys and the C++ struct fields describe the same data but **do not always share a name**. Since gempba's one-vocabulary change the wire says `rank` where the C++ struct still says worker, and the old struct names stay until v5.0.0 removes them: the line's `rank` is the struct's `m_worker_id`, the line's `idle_microseconds_per_thread` is `m_idle_microseconds_per_worker`, and so on. Read the wire names from wire-format.md and the struct names from the gempba headers; do not derive one from the other by stripping an `m_` prefix.

## Feeding telemetry from your own scheduler

A custom scheduler reaches this same stream through gempba's `record_*()` calls. gempba's [`docs/telemetry/custom-schedulers.md`](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/custom-schedulers.md) says what a custom scheduler must do for its runs to show up, and which call fills which key.
