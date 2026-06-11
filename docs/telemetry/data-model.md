# Data model

Telemetry is exposed two ways: as C++ frame structs (`<gempba/telemetry/frames.hpp>`, `topology.hpp`) for in-process consumers, and as a line-delimited **JSON broadcast** on the dashboard socket for everything else. Both carry the same information; this page describes what's in a frame so you can build a consumer.

Every frame is stamped with `TELEMETRY_SCHEMA_VERSION` (currently `1`), bumped on any layout change, so a consumer can guard against drift.

## The broadcast envelope

The center emits one JSON object per line per tick. Each line is a self-contained snapshot: the static topology plus the latest frame from every worker and host sentinel. Representative shape:

```json
{
  "ts": 1717180000123,
  "elapsed_seconds": 142,
  "topology": { "nodes": [ ... ], "identities": [ ... ] },
  "workers": [ { "worker_id": 0, "tasks_local_total": 8123, ... } ],
  "nodes":   [ { "sentinel_worker_id": 0, "logical_cores": 24, ... } ]
}
```

- `ts`: wall-clock milliseconds since the Unix epoch at emit time.
- `elapsed_seconds`: seconds since the run's telemetry came up.
- `topology`: the static snapshot (below); lets a consumer place numeric `worker_id`s onto hosts and hardware.
- `workers` / `nodes`: the latest per-worker and per-host samples.

JSON keys mirror the struct fields below (without the `m_` prefix).

## Worker frame

Per-worker sample, emitted on the worker cadence (default 500 ms). Counters are **cumulative since worker startup**, so a consumer computes deltas for rates.

| Field | Meaning |
|---|---|
| `worker_id`, `seq_no`, `worker_local_ms` | Identity, sequence number, and the worker's local clock at emit |
| `tasks_local_total` | Tasks dispatched to this worker's local thread pool |
| `tasks_sent_total` | Tasks sent to a remote worker (mutually exclusive with local) |
| `tasks_recv_total` | Tasks received from a remote worker |
| `tasks_running` | Tasks executing on the thread pool right now |
| `scheduler_pending_count` | Outstanding requests in the scheduler queue |
| `idle_microseconds_per_worker` | Cumulative pool idle time ÷ pool size |
| `process_cpu_pct`, `process_rss_bytes`, `process_threads` | Per-process CPU %, resident memory, thread count |
| `edges_out[dst]` | **Traffic matrix**: bytes and count sent to each destination `worker_id` |

The `edges_out` array is the raw material for a node-link graph of work flow between workers.

## Node (host) frame

Per-host sample, emitted by one **sentinel** worker per host on the node cadence (default 1000 ms): the host-wide signals that are not meaningful per-worker.

| Field | Meaning |
|---|---|
| `sentinel_worker_id`, `hostname`, `sentinel_local_ms` | Which worker speaks for the host, and when |
| `socket_count`, `logical_cores` | Host CPU layout |
| `sockets[]` | Per-socket `cpu_pct`, `mem_total_bytes`, `mem_used_bytes` |
| `mem_total_bytes`, `mem_avail_bytes` | Host memory |
| `net_aggregate` | `bytes_in/out`, `packets_in/out` (delta-able) |
| `disk_aggregate` | `read_bytes`, `write_bytes` (delta-able) |

## Topology snapshot

Captured once at startup and included in every broadcast. It is the map from the numeric `worker_id`s in the frames back to hosts and hardware.

- `nodes[]`, per host: `hostname`, the `worker_ids` it owns, its `sentinel_worker_id`, `sockets[]` (id, name, physical/logical cores, cpu-id list), and host totals.
- `identities[]`, per worker: `hostname`, `pid`, `primary_socket`, and `allowed_cpu_ids` (the CPU-affinity set, emitted as an array of logical CPU indices; the C++ struct field is the `m_allowed_cpu_mask` bitmap, which the serializer unpacks).

Hardware fields require an hwloc-enabled build; without it, core/socket counts are `0` and the rest of the frame is unaffected.

## Control messages (client → center)

The dashboard channel is bidirectional: a client can push control messages back to throttle the stream or reshape it live. See [Configuration](configuration.md#emission-cadence-and-live-control).

| `control_kind` | `value` |
|---|---|
| `SET_WORKER_INTERVAL_MS` | new worker cadence (ms) |
| `SET_NODE_INTERVAL_MS` | new node cadence (ms) |
| `BE_NODE_SENTINEL` | no value; promotes the target worker to host sentinel |

## Limits

- `MAX_WORKERS = 1024` sizes the worker-fanout and `edges_out` arrays.
- `MAX_SOCKETS = 8` is the per-host socket cap in a node frame.
