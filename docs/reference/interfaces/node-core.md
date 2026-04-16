# `node_core`

```cpp
#include <gempba/core/node_core.hpp>  // included automatically via gempba.hpp
```

`node_core` is the abstract base class for node implementations. It extends `node_traits<shared_ptr<node_core>>`, using shared pointers as the handle type for tree traversal at the implementation layer. The concrete default implementation, `node_core_impl`, lives in `detail/nodes/node_core_impl.hpp` and handles all standard cases.

`node` (the public handle) wraps a `shared_ptr<node_core>` and delegates every operation through it. Replacing `node_core` with a custom subclass changes the behavior of every `node` that wraps it, without touching user code or the `node` class itself.

## When to implement this

Most users never touch `node_core`. Realistic reasons to subclass:

- **GPU execution** — `run()` dispatches a kernel to the device rather than calling a CPU function
- **Custom memory** — non-standard allocators, memory-mapped argument storage, arena allocation
- **Custom serialization** — a domain-specific encoding that is more compact than the default Boost serialization

## Writing a custom implementation

Subclass `node_core` and implement every pure virtual method from `node_traits` (see [`node_traits`](node-traits.md) for the full list). Then wrap it with the custom-node factory:

```cpp
class MyNodeCore : public gempba::node_core {
public:
    // Execution
    void run() override { /* dispatch to GPU, custom allocator, etc. */ }
    void delegate_locally(gempba::load_balancer* lb) override { /* ... */ }
    void delegate_remotely(gempba::scheduler::worker* w, int id) override { /* ... */ }

    // Serialization
    gempba::task_packet serialize() override { /* ... */ }
    void deserialize(const gempba::task_packet& p) override { /* ... */ }
    void set_result_serializer(const std::function<gempba::task_packet(std::any)>& s) override { /* ... */ }
    void set_result_deserializer(const std::function<std::any(gempba::task_packet)>& d) override { /* ... */ }

    // Result handling
    void                set_result(const gempba::task_packet& r) override { /* ... */ }
    gempba::task_packet get_result() override { /* ... */ }
    std::any            get_any_result() override { /* ... */ }
    bool                is_result_ready() const override { /* ... */ }

    // Lifecycle
    bool           should_branch() override { /* ... */ }
    void           prune() override { /* ... */ }
    gempba::node_state get_state() const override { /* ... */ }
    void           set_state(gempba::node_state s) override { /* ... */ }
    bool           is_consumed() const override { /* ... */ }
    bool           is_dummy() const override { /* ... */ }

    // Tree navigation — all return shared_ptr<node_core>
    std::shared_ptr<node_core> get_root() override { /* ... */ }
    void set_parent(const std::shared_ptr<node_core>& p) override { /* ... */ }
    std::shared_ptr<node_core> get_parent() override { /* ... */ }
    std::shared_ptr<node_core> get_leftmost_child() override { /* ... */ }
    std::shared_ptr<node_core> get_second_leftmost_child() override { /* ... */ }
    void remove_leftmost_child() override { /* ... */ }
    void remove_second_leftmost_child() override { /* ... */ }
    std::shared_ptr<node_core> get_leftmost_sibling() override { /* ... */ }
    std::shared_ptr<node_core> get_left_sibling() override { /* ... */ }
    std::shared_ptr<node_core> get_right_sibling() override { /* ... */ }
    int  get_children_count() const override { /* ... */ }
    void add_child(const std::shared_ptr<node_core>& c) override { /* ... */ }
    void remove_child(std::shared_ptr<node_core>& c) override { /* ... */ }
    std::list<std::shared_ptr<node_core>> get_children() override { /* deprecated */ return {}; }

    // Metadata
    std::thread::id get_thread_id()     const override { /* ... */ }
    int             get_node_id()       const override { /* ... */ }
    int             get_forward_count() const override { /* ... */ }
    int             get_push_count()    const override { /* ... */ }
};

auto my_node = gempba::create_custom_node(std::make_unique<MyNodeCore>());
```

!!! warning
    `node_core` requires implementing a significant number of methods. Study `node_core_impl` in `detail/nodes/node_core_impl.hpp` to understand the expected semantics — particularly `should_branch()` (lazy argument initialization), `prune()` (child list cleanup), and the root-pointer semantics used by the quasi-horizontal load balancer — before starting from scratch.
