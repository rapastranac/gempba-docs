# `serial_runnable`

```cpp
#include <gempba/core/serial_runnable.hpp>  // included automatically via gempba.hpp
```

`serial_runnable` solves a problem that only appears in multiprocessing: your algorithm may call several different functions with different signatures. When a task crosses a process boundary, type information is gone. You cannot send a `std::function<void(int, Graph&, node)>` as-is. You can only send bytes.

The solution is type erasure. Each `serial_runnable` wraps one typed function and exposes only two things to the outside world:

```cpp
class serial_runnable {
public:
    virtual int get_id() const = 0;

    virtual std::optional<std::shared_future<task_packet>>
    operator()(node_manager& nm, const task_packet& task) = 0;
};
```

The scheduler maintains a map of `{ id -> serial_runnable }`. When a `task_packet` arrives, the scheduler looks up the ID, calls `operator()` on the matching runnable, and that is it. The runnable knows the actual function type internally (it captured it at construction), so it can deserialize the arguments from bytes, call the function, and serialize the result back. The scheduler never touches function types. It just routes bytes by ID.

## Creating a runnable for a void function

```cpp
// The deserializer reconstructs the argument tuple from incoming bytes
std::function<std::tuple<int, MyGraph>(task_packet)> deserializer = [](task_packet p) {
    return std::make_tuple(/* depth */, /* graph */);
};

auto runnable = gempba::mp::runnables::return_none::create<int, MyGraph>(
    MY_FUNCTION_ID,   // unique integer ID for this function
    &my_func,
    deserializer
);
```

## Creating a runnable for a non-void function

```cpp
std::function<std::tuple<int, MyGraph>(task_packet)> deserializer = /* ... */;

// The serializer converts the return value to bytes for the return trip
std::function<task_packet(MyResult)> serializer = [](MyResult r) {
    return task_packet{/* r serialized */};
};

auto runnable = gempba::mp::runnables::return_value::create<MyResult, int, MyGraph>(
    MY_FUNCTION_ID,
    &my_func,
    deserializer,
    serializer
);
```

## Registering runnables and starting the scheduler

Collect your runnables into a map and pass them to the scheduler's worker. The worker will block and process incoming tasks until the computation is complete:

```cpp
std::map<int, std::shared_ptr<gempba::serial_runnable>> runnables;
runnables[MY_FUNCTION_ID]    = runnable_a;
runnables[OTHER_FUNCTION_ID] = runnable_b;

// This blocks until the scheduler signals completion
s->worker_view().run(nm, runnables);
```

At runtime, when a `task_packet` arrives tagged with `MY_FUNCTION_ID`, the scheduler finds the matching `serial_runnable` and calls its `operator()`. All the template machinery (argument deserialization, function dispatch, result serialization) stays inside the concrete implementations in `detail/runnables/`. Nothing typed ever crosses a process boundary.
