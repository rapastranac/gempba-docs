# `node_core`

```cpp
#include <gempba/core/node_core.hpp>  // included automatically via gempba.hpp
```

Abstract base class for node implementations. Extends `node_traits<shared_ptr<node_core>>` — the implementation-layer handle type is a shared pointer. The default concrete class is `node_core_impl` in `detail/nodes/node_core_impl.hpp`.

`node` (the public handle) wraps a `shared_ptr<node_core>` and delegates every operation through it. Swapping the underlying `node_core` subclass changes behavior without touching user code.

---

## Interface

Implement every pure virtual method from [`node_traits`](node-traits.md) with `T = shared_ptr<node_core>`. No additional methods are declared beyond that contract.

---

## Custom implementation

```cpp
class MyNodeCore : public gempba::node_core {
    // implement all node_traits<shared_ptr<node_core>> pure virtuals
};

auto my_node = gempba::create_custom_node(std::make_unique<MyNodeCore>());
```

!!! warning
    Study `node_core_impl` before writing from scratch — pay attention to `should_branch()` (lazy argument initialization), `prune()` (child list cleanup), and the root-pointer semantics used by the quasi-horizontal load balancer.

Realistic reasons to subclass: GPU execution in `run()`, custom allocators, domain-specific serialization.
