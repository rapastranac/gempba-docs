# `gempba`

```cpp
#include <gempba/gempba.hpp>
```

This is the only header you need. It is the facade for the entire library. It exposes the global accessors, all factory functions, and the two namespaces you will use: `gempba::mt` for multithreading and `gempba::mp` for multiprocessing.

---

## Global accessors

These are how you reach the shared components from inside your algorithm, after they have been created in `main()`.

```cpp
load_balancer* lb = gempba::get_load_balancer();
```

Returns a pointer to the active load balancer.

```cpp
node_manager& nm = gempba::get_node_manager();
```

Returns a reference to the node manager.

```cpp
scheduler* s = gempba::get_scheduler();
```

Returns a pointer to the active scheduler. Multiprocessing only.

---

## Seed creation

```cpp
auto seed = gempba::create_seed_node<void>(*lb, &my_func, std::make_tuple(initial_args...));
```

Creates the root of your search tree for a void function. Has no parent node.

```cpp
auto seed = gempba::create_seed_node<MyReturnType>(*lb, &my_func, std::make_tuple(initial_args...));
```

Same for a non-void function.

---

## Multithreading: `gempba::mt`

```cpp
auto* lb = gempba::mt::create_load_balancer(gempba::balancing_policy::QUASI_HORIZONTAL);
```

Create a load balancer using a built-in balancing policy.

```cpp
auto* lb = gempba::mt::create_load_balancer(std::make_unique<MyLoadBalancer>());
```

Create a load balancer with a custom implementation.

```cpp
auto& nm = gempba::mt::create_node_manager(lb);
```

Create the node manager. One per process.

```cpp
auto child = gempba::mt::create_explicit_node<void>(
    lb, parent, &my_func, std::make_tuple(args...)
);
```

Create a child node inside your recursive function. Arguments are captured eagerly.

```cpp
auto child = gempba::mt::create_lazy_node<void>(
    lb, parent, &my_func, args_initializer_fn
);
```

Lazy variant. Arguments are computed on demand, which is useful when preparing them is expensive and the branch might be pruned before it ever executes.

---

## Multiprocessing: `gempba::mp`

Each process runs the setup code and branches on its role (center or worker).

```cpp
auto* s = gempba::mp::create_scheduler(gempba::mp::scheduler_topology::SEMI_CENTRALIZED);
```

Create a scheduler using a built-in topology.

```cpp
auto* s = gempba::mp::create_scheduler(std::make_unique<MyScheduler>());
```

Create a scheduler with a custom implementation.

```cpp
auto* lb = gempba::mp::create_load_balancer(
    gempba::balancing_policy::QUASI_HORIZONTAL,
    &s->worker_view()
);
```

Create a load balancer that is aware of the scheduler's worker interface.

```cpp
auto& nm = gempba::mp::create_node_manager(lb, &s->worker_view());
```

Create the node manager for worker processes.

```cpp
auto child = gempba::mp::create_explicit_node<void>(
    lb, parent, &my_func,
    std::make_tuple(args...),
    args_serializer_fn,    // Args... -> task_packet
    args_deserializer_fn   // task_packet -> tuple<Args...>
);
```

Create a child node with serializers. Required in multiprocessing mode because arguments cross process boundaries as bytes.

---

## Shutdown

```cpp
return gempba::shutdown();
```

Call at the end of `main()`. Finalizes the IPC backend (MPI by default) when multiprocessing is enabled and returns the correct exit code. Do not skip this if multiprocessing is on.
