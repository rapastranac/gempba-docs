# Load Balancing

Both `gempba::mt` and `gempba::mp` support the same two built-in policies, selected via `gempba::balancing_policy`:

## `QUASI_HORIZONTAL` (recommended)

```cpp
auto* lb = gempba::mt::create_load_balancer(gempba::balancing_policy::QUASI_HORIZONTAL);
```

Understands the shape of the recursion tree. When a thread requests work, the load balancer traverses the tree upward from the current work front and preferentially offers tasks near the root — where each task will spawn the most downstream work. For branching algorithms where subtree sizes vary dramatically, this keeps CPU utilization significantly higher than naive work-stealing. This is the main algorithmic contribution of the original research.

## Work-stealing

```cpp
auto* lb = gempba::mt::create_load_balancer(gempba::balancing_policy::WORK_STEALING);
```

Takes the first available task from the queue. Simple to reason about, useful as a comparison baseline. Does not account for position in the tree.

## Bring your own

Both namespaces accept a `unique_ptr` to a custom load balancer that implements the required interface:

```cpp
auto* lb = gempba::mt::create_load_balancer(std::make_unique<MyLoadBalancer>());
```

See [`node_traits.hpp`](node-traits.md) for the interface your load balancer must program against.
