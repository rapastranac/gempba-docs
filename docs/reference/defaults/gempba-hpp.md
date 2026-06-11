# `gempba`

```cpp
#include <gempba/gempba.hpp>
```

This is the only header you need. It is the facade for the entire library. It exposes the global accessors, all factory functions, and the two flavor namespaces: `gempba::multithreading` and `gempba::multiprocessing`.

!!! note "Short form"
    In a consumer build, the installed flavor's namespace is `inline`, so you can drop the qualifier and write `gempba::create_load_balancer(...)`, `gempba::create_node_manager(...)`, and so on. This page uses the explicit form so each function's flavor is unambiguous.

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

```cpp
scheduler* s = gempba::try_get_scheduler();
```

Non-throwing variant: returns `nullptr` when no scheduler has been created instead of throwing. Multiprocessing only. Useful for read-only probes (telemetry uses it).

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

## Mode-agnostic factories

```cpp
auto* lb = gempba::create_load_balancer(std::make_unique<MyLoadBalancer>());
```

Take ownership of a custom load balancer implementation. This overload lives at the top level and behaves identically in MT and MP builds, since the worker pointer (when relevant) is part of the caller-provided instance.

---

## Multithreading: `gempba::multithreading`

```cpp
auto* lb = gempba::multithreading::create_load_balancer(gempba::balancing_policy::QUASI_HORIZONTAL);
```

Create a load balancer using a built-in balancing policy.

```cpp
auto& nm = gempba::multithreading::create_node_manager(lb);
```

Create the node manager. One per process.

```cpp
auto child = gempba::multithreading::create_explicit_node<void>(
    *lb, parent, &my_func, std::make_tuple(args...)
);
```

Create a child node inside your recursive function. Arguments are captured eagerly. Note the node factories take the load balancer by reference, while `create_node_manager` takes it as a pointer.

```cpp
auto child = gempba::multithreading::create_lazy_node<void>(
    *lb, parent, &my_func, args_initializer_fn
);
```

Lazy variant. Arguments are computed on demand, which is useful when preparing them is expensive and the branch might be pruned before it ever executes.

---

## Multiprocessing: `gempba::multiprocessing`

Each process runs the setup code and branches on its role (center or worker).

```cpp
auto* s = gempba::multiprocessing::create_scheduler(gempba::multiprocessing::scheduler_topology::SEMI_CENTRALIZED);
```

Create a scheduler using a built-in topology.

```cpp
auto* s = gempba::multiprocessing::create_scheduler(std::make_unique<MyScheduler>());
```

Create a scheduler with a custom implementation.

```cpp
auto* lb = gempba::multiprocessing::create_load_balancer(
    gempba::balancing_policy::QUASI_HORIZONTAL,
    &s->worker_view()
);
```

Create a load balancer that is aware of the scheduler's worker interface.

```cpp
auto& nm = gempba::multiprocessing::create_node_manager(lb, &s->worker_view());
```

Create the node manager for worker processes.

```cpp
auto visitor = gempba::multiprocessing::get_default_mpi_stats_visitor();
```

Returns the bundled [stats visitor](../implementations/stats-visitors/default-mpi-stats-visitor.md) for the MPI schedulers, ready to pass to the stats-collection API.

```cpp
auto child = gempba::multiprocessing::create_explicit_node<void>(
    *lb, parent, &my_func,
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
