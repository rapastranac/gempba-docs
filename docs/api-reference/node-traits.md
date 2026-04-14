# `node_traits.hpp`

```cpp
#include <gempba/core/node_traits.hpp>  // included automatically via gempba.hpp
```

`node_traits<T>` is the abstract interface that defines what every node must be able to do. It is templated on `T`, the handle type used for tree navigation:

- `node_traits<node>`: satisfied by `node` (the public API, handles passed by value)
- `node_traits<shared_ptr<node_core>>`: satisfied by `node_core` (the implementation layer)

Load balancers program against `node_traits<node>`. They do not depend on `node`, `node_core`, or any specific class. This is the core of the pluggable design: the load balancer does not know or care whether you are using the default `node_core_impl` or a custom GPU implementation. As long as the handle satisfies the contract, everything works.

## The contract

**Tree navigation** — used by the load balancer to understand the shape of the search:

```cpp
virtual T get_parent() = 0;
virtual T get_root() = 0;
virtual T get_leftmost_child() = 0;
virtual T get_second_leftmost_child() = 0;
virtual T get_leftmost_sibling() = 0;
virtual T get_left_sibling() = 0;
virtual T get_right_sibling() = 0;
virtual int get_children_count() const = 0;
```

**Lifecycle** — used by the load balancer to decide whether a node is worth taking:

```cpp
virtual node_state get_state() const = 0;
virtual void set_state(node_state) = 0;
virtual bool is_consumed() const = 0;
virtual bool should_branch() = 0;
virtual void prune() = 0;
```

**Execution** — how a node actually runs:

```cpp
virtual void run() = 0;
virtual void delegate_locally(load_balancer*) = 0;
virtual void delegate_remotely(scheduler::worker*, int runner_id) = 0;
```

**Serialization** — used when nodes travel across process boundaries:

```cpp
virtual task_packet serialize() = 0;
virtual void deserialize(const task_packet&) = 0;
virtual void set_result_serializer(...) = 0;
virtual void set_result_deserializer(...) = 0;
```

**Metadata** — mostly useful for debugging:

```cpp
virtual int get_node_id() const = 0;
virtual std::thread::id get_thread_id() const = 0;
virtual int get_forward_count() const = 0;
virtual int get_push_count() const = 0;
virtual bool is_dummy() const = 0;
```

You interact with this indirectly through `node` and `node_manager`. You only need to read this header directly if you are implementing a custom [`node_core`](node-core.md) or a custom load balancer.

## Node lifecycle states

```cpp
enum node_state {
    UNUSED,                   // just created, not yet submitted
    FORWARDED,                // executed on the current thread
    PUSHED,                   // sent to another thread within this process
    DISCARDED,                // pruned before it ran
    RETRIEVED,                // result was collected
    SENT_TO_ANOTHER_PROCESS   // handed off to another MPI rank
};
```
