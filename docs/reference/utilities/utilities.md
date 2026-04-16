# Utilities

Supporting types used throughout GemPBA. Most of these appear in serializer and deserializer lambdas you write when wiring up multiprocessing nodes, or in result-handling code after a run completes.

| Type | Purpose |
|---|---|
| [`task_packet`](task-packet.md) | Raw byte buffer — serialized function arguments or return values |
| [`task_bundle`](task-bundle.md) | A `task_packet` tagged with a `runnable_id` for cross-process dispatch |
| [`score`](score.md) | Type-erased numeric value — carries the optimization objective |
| [`result`](result.md) | A found solution: pairs a `score` with a serialized `task_packet` |
| [`transmission_guard`](transmission-guard.md) | RAII lock held for the duration of an IPC send |
| [`tree`](tree.md) | Index-based tree used internally by the scheduler startup phase |
| [`Queue`](queue.md) | Thread-safe FIFO queue used internally by the thread pool |
