# `task_bundle`

```cpp
#include <gempba/utils/task_bundle.hpp>  // included automatically via gempba.hpp
```

`task_bundle` pairs a [`task_packet`](task-packet.md) with a `runnable_id`. It is the unit of inter-process task transfer: when a worker sends work to another process, it wraps the serialized arguments in a `task_bundle` so the receiving end knows which [`serial_runnable`](../interfaces/serial-runnable.md) to dispatch it to.

You do not construct `task_bundle` directly in normal use. Node factory functions and the scheduler produce and consume them internally.

---

## Constructor

```cpp
explicit task_bundle(task_packet data, int runnable_id) noexcept;
```

Takes ownership of a serialized argument buffer and associates it with the ID of the runnable that should receive it on the remote end.

---

## Accessors

```cpp
[[nodiscard]] task_packet get_task_packet() const noexcept;
```

Returns the serialized argument buffer.

```cpp
[[nodiscard]] int get_runnable_id() const noexcept;
```

Returns the ID of the target [`serial_runnable`](../interfaces/serial-runnable.md).

```cpp
[[nodiscard]] bool empty() const noexcept;
```

Returns `true` if the contained `task_packet` is empty.

```cpp
[[nodiscard]] std::size_t size() const noexcept;
```

Number of bytes in the contained `task_packet`. Delegates to `task_packet::size()`.

---

## Comparison

```cpp
bool operator==(const task_bundle&) const;
bool operator!=(const task_bundle&) const;
```

Compare both `runnable_id` and `task_packet`.
