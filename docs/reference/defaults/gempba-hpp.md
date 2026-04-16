# `gempba`

```cpp
#include <gempba/gempba.hpp>
```

This is the only header you need. It is the facade for the entire library. It exposes the global accessors, all factory functions, and the two namespaces you will use: `gempba::mt` for multithreading and `gempba::mp` for multiprocessing.

## Global accessors

These are how you reach the shared components from inside your algorithm, after they have been created in `main()`:

```cpp
load_balancer* lb = gempba::get_load_balancer();
node_manager&  nm = gempba::get_node_manager();
scheduler*      s = gempba::get_scheduler();   // multiprocessing only
```

## Seed creation

The seed node is the root of your search tree. It has no parent, so it is created outside the recursive function:

```cpp
// void function
auto seed = gempba::create_seed_node<void>(*lb, &my_func, std::make_tuple(initial_args...));

// non-void function
auto seed = gempba::create_seed_node<MyReturnType>(*lb, &my_func, std::make_tuple(initial_args...));
```

## Multithreading: `gempba::mt`

```cpp
// Built-in policy
auto* lb = gempba::mt::create_load_balancer(gempba::balancing_policy::QUASI_HORIZONTAL);

// Or bring your own
auto* lb = gempba::mt::create_load_balancer(std::make_unique<MyLoadBalancer>());

// One node manager per process
auto& nm = gempba::mt::create_node_manager(lb);

// Inside your recursive function: create a node for each branch
auto child = gempba::mt::create_explicit_node<void>(
    lb, parent, &my_func, std::make_tuple(args...)
);

// Lazy variant: args are computed on demand, which is useful when preparing them
// is expensive and the branch might be pruned before it ever executes
auto child = gempba::mt::create_lazy_node<void>(
    lb, parent, &my_func, args_initializer_fn
);
```

## Multiprocessing: `gempba::mp`

Each process runs the setup code and branches on its role (center or worker):

```cpp
// Built-in scheduler topology
auto* s = gempba::mp::create_scheduler(gempba::mp::scheduler_topology::SEMI_CENTRALIZED);

// Or bring your own
auto* s = gempba::mp::create_scheduler(std::make_unique<MyScheduler>());

// Load balancer that knows about the scheduler
auto* lb = gempba::mp::create_load_balancer(
    gempba::balancing_policy::QUASI_HORIZONTAL,
    &s->worker_view()
);

// Node manager for workers
auto& nm = gempba::mp::create_node_manager(lb, &s->worker_view());

// Nodes need serializers because arguments cross process boundaries as bytes
auto child = gempba::mp::create_explicit_node<void>(
    lb, parent, &my_func,
    std::make_tuple(args...),
    args_serializer_fn,    // Args... -> task_packet
    args_deserializer_fn   // task_packet -> tuple<Args...>
);
```

## Shutdown

```cpp
return gempba::shutdown();
```

Call at the end of `main()`. It finalizes the IPC backend (MPI by default) when multiprocessing is enabled and returns the correct exit code. Do not skip this if multiprocessing is on.
