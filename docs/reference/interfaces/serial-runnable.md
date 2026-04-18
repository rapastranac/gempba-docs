# `serial_runnable`

```cpp
#include <gempba/core/serial_runnable.hpp>  // included automatically via gempba.hpp
```

Type erasure for functions that cross process boundaries. Each `serial_runnable` wraps one typed function and exposes a uniform interface to the scheduler — bytes in, bytes out, routed by integer ID. The scheduler never touches function types.

---

## Member functions

```cpp
virtual int get_id() const = 0;
```
Unique integer identifying this function across all processes.

```cpp
virtual std::optional<std::shared_future<task_packet>>
operator()(node_manager& nm, const task_packet& task) = 0;
```
Deserialize arguments from `task`, call the wrapped function, return serialized result — or `std::nullopt` for void functions.

---

## Factory functions

### Void function

```cpp
auto runnable = gempba::mp::runnables::return_none::create<Arg1, Arg2, ...>(
    FUNCTION_ID,
    &my_func,
    deserializer   // std::function<std::tuple<Arg1, Arg2, ...>(task_packet)>
);
```

### Non-void function

```cpp
auto runnable = gempba::mp::runnables::return_value::create<ReturnType, Arg1, Arg2, ...>(
    FUNCTION_ID,
    &my_func,
    deserializer,  // std::function<std::tuple<Arg1, Arg2, ...>(task_packet)>
    serializer     // std::function<task_packet(ReturnType)>
);
```

---

## Registering runnables

```cpp
std::map<int, std::shared_ptr<gempba::serial_runnable>> runnables;
runnables[FUNCTION_ID]       = runnable_a;
runnables[OTHER_FUNCTION_ID] = runnable_b;

s->worker_view().run(nm, runnables);  // blocks until computation is complete
```

When a `task_packet` arrives tagged with `FUNCTION_ID`, the scheduler calls `operator()` on the matching runnable. All template machinery (deserialization, dispatch, serialization) stays inside `detail/runnables/` — nothing typed crosses a process boundary.
