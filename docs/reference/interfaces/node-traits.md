# `node_traits`

```cpp
#include <gempba/core/node_traits.hpp>  // included automatically via gempba.hpp
```

`node_traits<T>` is the abstract interface contract every node must satisfy. It is templated on `T`, the handle type used for tree navigation:

- `node_traits<node>` — satisfied by `node` (the user-facing concrete handle)
- `node_traits<shared_ptr<node_core>>` — satisfied by `node_core` (the implementation layer)

`node_traits` extends [`serializable`](#serializable), which contributes `serialize()` and `deserialize()`.

Load balancers and the scheduler program against `node_traits<node>`. They depend on no concrete class — only this contract.

## `node_state`

```cpp
enum node_state {
    UNUSED,                   // created, not yet submitted
    FORWARDED,                // executed on the current thread
    PUSHED,                   // handed to another thread within this process
    DISCARDED,                // pruned before it ran
    RETRIEVED,                // result collected
    SENT_TO_ANOTHER_PROCESS   // handed off to another process
};
```

## `serializable`

Inherited base. Required for nodes that cross process boundaries:

```cpp
virtual task_packet serialize()                      = 0;
virtual void        deserialize(const task_packet&)  = 0;
```

## Serialization hooks

```cpp
virtual void set_result_serializer(
    const std::function<task_packet(std::any)>& serializer) = 0;

virtual void set_result_deserializer(
    const std::function<std::any(task_packet)>& deserializer) = 0;
```

Attach serializer/deserializer for the return value of non-void functions. Called by the node factory functions when you supply these lambdas; not called directly.

## Lifecycle

```cpp
[[nodiscard]] virtual node_state get_state()  const = 0;
virtual void                     set_state(node_state) = 0;
[[nodiscard]] virtual bool       is_consumed() const = 0;
```

`is_consumed()` returns `true` when the node has been dispatched (forwarded, pushed, or sent to another process) and should no longer be touched by the caller.

```cpp
virtual bool should_branch() = 0;
```

Returns `true` if this branch is worth exploring. For **lazy nodes**, this is also the point where argument initialization happens: arguments are computed only if `should_branch()` is called, avoiding stack allocation of data that will be pruned before it is ever needed. Always call `should_branch()` before `run()` or `delegate_locally()`.

```cpp
virtual void prune() = 0;
```

Marks the node as `DISCARDED` and releases any held resources.

## Execution

```cpp
virtual void run() = 0;
```

Executes the underlying function on the calling thread.

```cpp
virtual void delegate_locally(load_balancer* lb) = 0;
```

Hands the node to `lb` for thread-level dispatch within this process.

```cpp
virtual void delegate_remotely(scheduler::worker* worker, int runner_id) = 0;
```

Serializes the node and sends it to another process via `worker`. `runner_id` identifies which [`serial_runnable`](serial-runnable.md) on the remote side will receive it.

## Result handling

```cpp
virtual void        set_result(const task_packet& result) = 0;
virtual task_packet get_result()                          = 0;
virtual std::any    get_any_result()                      = 0;
[[nodiscard]] virtual bool is_result_ready() const        = 0;
```

For non-void functions, the return value travels back as a serialized `task_packet` and is stored here. `get_any_result()` deserializes it to `std::any` for type-erased retrieval.

## Tree navigation

```cpp
virtual T get_root()                   = 0;
virtual void set_parent(const T&)      = 0;
[[nodiscard]] virtual T get_parent()   = 0;
```

```cpp
[[nodiscard]] virtual T get_leftmost_child()        = 0;
[[nodiscard]] virtual T get_second_leftmost_child() = 0;
virtual void remove_leftmost_child()                = 0;
virtual void remove_second_leftmost_child()         = 0;
```

```cpp
[[nodiscard]] virtual T get_leftmost_sibling() = 0;
[[nodiscard]] virtual T get_left_sibling()     = 0;
[[nodiscard]] virtual T get_right_sibling()    = 0;
```

`get_leftmost_sibling()` — returns `this` if it is already the leftmost child; otherwise returns the leftmost child of the parent.  
`get_left_sibling()` — the child immediately to the left in the parent's child list, or null if `this` is leftmost.  
`get_right_sibling()` — the child immediately to the right, or null if `this` is rightmost.

```cpp
[[nodiscard]] virtual int get_children_count() const = 0;
virtual void add_child(const T& child)               = 0;
virtual void remove_child(T& child)                  = 0;
```

```cpp
[[deprecated("Internal use only")]]
virtual std::list<T> get_children() = 0;
```

## Metadata (debugging)

```cpp
[[nodiscard]] virtual bool           is_dummy()        const = 0;
[[nodiscard]] virtual std::thread::id get_thread_id()  const = 0;
[[nodiscard]] virtual int            get_node_id()     const = 0;
[[nodiscard]] virtual int            get_forward_count() const = 0;
[[nodiscard]] virtual int            get_push_count()  const = 0;
```

- `is_dummy()` — `true` for placeholder nodes created without arguments (e.g. `create_dummy_node`).
- `get_node_id()` — unique within the owning thread; not globally unique.
- `get_forward_count()` and `get_push_count()` — should never exceed 1; useful for diagnosing double-dispatch bugs.
