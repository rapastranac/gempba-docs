# `task_bundle`

```cpp
#include <gempba/utils/task_bundle.hpp>  // included automatically via gempba.hpp
```

`task_bundle` pairs a [`task_packet`](task-packet.md) with a `runnable_id`. It is the unit of inter-process task transfer: when a worker sends work to another process, it wraps the serialized arguments in a `task_bundle` so the receiving end knows which [`serial_runnable`](../interfaces/serial-runnable.md) to dispatch it to.

You do not construct `task_bundle` directly in normal use. Node factory functions and the scheduler produce and consume them internally.

## Construction

```cpp
explicit task_bundle(task_packet data, int runnable_id) noexcept;
```

## Accessors

```cpp
[[nodiscard]] task_packet get_task_packet()  const noexcept;
[[nodiscard]] int         get_runnable_id()  const noexcept;
[[nodiscard]] bool        empty()            const noexcept;
[[nodiscard]] std::size_t size()             const noexcept;  // delegates to task_packet::size()
```

`==` and `!=` compare both `runnable_id` and `task_packet`.
