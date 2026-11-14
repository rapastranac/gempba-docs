# Data model

Telemetry is exposed two ways, and both carry the same information:

- **In process**, as C++ frame structs (`<gempba/telemetry/frames.hpp>`, `topology.hpp`) for a consumer compiled into the same binary, which reads them from the process's hub (`gempba::telemetry::get()`).
- **Over the socket**, as a line-delimited **JSON broadcast** on the dashboard channel, for everything else.

This page is a map of what a broadcast line carries. The authoritative, field-by-field reference, with each key's unit and the release that added it, every control line, the compatibility rules and every schema version, lives in gempba's [`docs/telemetry/wire-format.md`](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/wire-format.md). This page links there rather than keeping a second copy in sync.

## Schema 2

gempba sends **schema 2** from v4.3.0 on, v5.0.0 included: every line carries `"version": 2`. A consumer written against an older release reads that release's schema, which stays valid for it. wire-format.md lists [every schema version](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/wire-format.md#schema-versions), newest first, and the compatibility rules: a consumer ignores keys it does not know, and a renamed, removed or redefined key bumps `version`.

## What a line carries

The aggregator (rank 0) emits one JSON object per line, every telemetry interval. A full line is self-contained, so a client that connects late misses nothing but history:

- an **envelope**: `version`, `run_id`, `ts`, `elapsed_seconds`, `paused` and `final`, and on the final line `end`;
- the **topology**: each host, each rank's identity with its `role` (`coordinator` or `worker`), and a `run` object holding the run's setup, its annotations and its markers;
- **`ranks`**: the latest frame from every rank, whatever its role: task counters, where its pool threads' idle time went (starved versus imbalanced), scheduler timing, the cost of moving tasks, and an `edges_out` list of the ranks it sent tasks to;
- **`nodes`**: the latest per-host frame from each host's sentinel rank: CPU, memory, and the job's own memory within its cgroup.

While the run is paused, a line carries only the envelope header with `"paused": true`. The line sent at shutdown carries the run's totals and `"final": true`, and is the last before the aggregator closes the connection. From gempba v5.0.0, the final line also says how the run ended in `end`: `reason`, and for an interrupted run `trigger` and `signal`. A connection that closes without that final line was lost; see [Stopping a Run](../stopping-a-run.md#on-the-telemetry-stream). See [the full worked example and every field](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/wire-format.md#example).

## Controlling the stream

The socket is bidirectional: a client writes control lines back, one JSON object per line, to set the telemetry interval, to pause, resume, snapshot or mark the run, or, from gempba v5.0.0, to stop it. [Configuration](configuration.md#emission-cadence-and-live-control) covers them from the runtime side; wire-format.md gives [the exact lines a client sends](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/wire-format.md#control-lines).

## JSON keys versus C++ struct fields

The JSON keys and the C++ struct fields describe the same data, and since v5.0.0 they use the same words: the line's `rank` is `rank_frame`'s `m_rank`, and its `idle_microseconds_per_thread` is `m_idle_microseconds_per_thread`. They still **don't always share a name**. Read the wire names from wire-format.md and the struct names from the gempba headers; do not derive one from the other by stripping an `m_` prefix.

## Feeding telemetry from your own scheduler

A custom scheduler reaches this same stream through gempba's `record_*()` calls. gempba's [`docs/telemetry/custom-schedulers.md`](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/custom-schedulers.md) says what a custom scheduler must do for its runs to show up, and which call fills which key.
