# `node_core.hpp`

```cpp
#include <gempba/core/node_core.hpp>  // included automatically via gempba.hpp
```

`node_core` is an abstract base class. It defines what a node actually does: execute a function, serialize its arguments for IPC, track its position in the tree (parent, children, siblings), and manage its lifecycle state.

The default implementation, `node_core_impl` in `detail/nodes/node_core_impl.hpp`, handles all of this. Most users never interact with `node_core` directly.

This header exists for advanced users who need custom node behavior. Realistic use cases:

- **GPU execution**: `run()` dispatches a kernel to the device instead of calling a CPU function
- **Custom memory**: non-standard allocators, memory-mapped argument storage, arena allocation
- **Specialized serialization**: a custom IPC protocol where Boost serialization is not appropriate

## Writing a custom implementation

Subclass `node_core` and implement every pure virtual method from `node_traits`. Then wrap it using `gempba::create_custom_node`:

```cpp
class MyNodeCore : public gempba::node_core {
public:
    void run() override {
        // dispatch to GPU, custom allocator, or whatever you need
    }

    void delegate_locally(load_balancer* lb) override { /* ... */ }
    void delegate_remotely(scheduler::worker* w, int id) override { /* ... */ }
    task_packet serialize() override { /* ... */ }
    void deserialize(const task_packet& p) override { /* ... */ }
    // ... and all remaining pure virtual methods from node_traits
};

auto my_node = gempba::create_custom_node(std::make_unique<MyNodeCore>());
```

!!! warning
    `node_core` requires implementing quite a few methods. Before starting, study `node_core_impl` to understand the expected semantics for each one.

`node_core` itself extends `node_traits<shared_ptr<node_core>>`, using shared pointers as the handle type for tree traversal at the implementation layer.
