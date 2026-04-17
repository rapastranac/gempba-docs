# `node_traits`

```cpp
#include <gempba/core/node_traits.hpp>  // included automatically via gempba.hpp
```

Abstract interface contract for all node types. Templated on `T` — the handle type used for tree navigation.

| Instantiation | Handle type |
|---|---|
| `node_traits<node>` | user-facing `node` handle |
| `node_traits<shared_ptr<node_core>>` | implementation layer |

Extends [`serializable`](#serializable). Load balancers and the scheduler program against `node_traits<node>` only.

---

## Member types

```cpp
enum node_state {
    UNUSED,
    FORWARDED,
    PUSHED,
    DISCARDED,
    RETRIEVED,
    SENT_TO_ANOTHER_PROCESS
};
```

---

## Member functions

### `serializable` (inherited)

```cpp
virtual task_packet serialize() = 0;
```
Serialize arguments to bytes for cross-process transfer.

```cpp
virtual void deserialize(const task_packet&) = 0;
```
Restore arguments from bytes on the receiving side.

```cpp
virtual void set_result_serializer(const std::function<task_packet(std::any)>&) = 0;
```
Attach serializer for the return value. Called by node factory functions — not called directly.

```cpp
virtual void set_result_deserializer(const std::function<std::any(task_packet)>&) = 0;
```
Attach deserializer for the return value. Called by node factory functions — not called directly.

---

### Lifecycle

```cpp
[[nodiscard]] virtual node_state get_state() const = 0;
```
Current dispatch state.

```cpp
virtual void set_state(node_state) = 0;
```
Set dispatch state.

```cpp
[[nodiscard]] virtual bool is_consumed() const = 0;
```
`true` when dispatched; caller must not reuse the node.

```cpp
virtual bool should_branch() = 0;
```
`true` if this branch is worth exploring. For lazy nodes, also triggers argument initialization — always call before `run()` or `delegate_locally()`.

```cpp
virtual void prune() = 0;
```
Mark as `DISCARDED`, release held resources.

---

### Execution

```cpp
virtual void run() = 0;
```
Execute underlying function on the calling thread.

```cpp
virtual void delegate_locally(load_balancer* lb) = 0;
```
Hand to `lb` for thread-level dispatch within this process.

```cpp
virtual void delegate_remotely(scheduler::worker* worker, int runner_id) = 0;
```
Serialize and send to another process via `worker`. `runner_id` selects the matching [`serial_runnable`](serial-runnable.md) on the remote side.

---

### Result handling

```cpp
virtual void set_result(const task_packet&) = 0;
```
Store serialized return value.

```cpp
virtual task_packet get_result() = 0;
```
Retrieve serialized return value.

```cpp
virtual std::any get_any_result() = 0;
```
Deserialize return value to `std::any`.

```cpp
[[nodiscard]] virtual bool is_result_ready() const = 0;
```
`true` if a result has been stored.

---

### Tree navigation

```cpp
virtual T get_root() = 0;
```
Root of this node's subtree.

```cpp
virtual void set_parent(const T&) = 0;
virtual T    get_parent() = 0;
```

```cpp
[[nodiscard]] virtual T get_leftmost_child() = 0;
[[nodiscard]] virtual T get_second_leftmost_child() = 0;
virtual void            remove_leftmost_child() = 0;
virtual void            remove_second_leftmost_child() = 0;
```

```cpp
[[nodiscard]] virtual T get_leftmost_sibling() = 0;
```
Returns `this` if already the leftmost child of its parent.

```cpp
[[nodiscard]] virtual T get_left_sibling() = 0;
```
Sibling immediately to the left; null if `this` is leftmost.

```cpp
[[nodiscard]] virtual T get_right_sibling() = 0;
```
Sibling immediately to the right; null if `this` is rightmost.

```cpp
[[nodiscard]] virtual int get_children_count() const = 0;
virtual void              add_child(const T& child) = 0;
virtual void              remove_child(T& child) = 0;
```

```cpp
[[deprecated("Internal use only")]]
virtual std::list<T> get_children() = 0;
```

---

### Metadata

```cpp
[[nodiscard]] virtual bool            is_dummy()          const = 0;
[[nodiscard]] virtual std::thread::id get_thread_id()     const = 0;
[[nodiscard]] virtual int             get_node_id()       const = 0;
[[nodiscard]] virtual int             get_forward_count() const = 0;
[[nodiscard]] virtual int             get_push_count()    const = 0;
```

`is_dummy()` — `true` for placeholder nodes created without arguments.  
`get_node_id()` — unique within the owning thread; not globally unique.  
`get_forward_count()` / `get_push_count()` — should never exceed 1; useful for diagnosing double-dispatch bugs.
