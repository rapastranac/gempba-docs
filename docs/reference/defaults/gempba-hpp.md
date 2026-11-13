# `gempba`

```cpp
#include <gempba/gempba.hpp>
```

This is the facade for the entire library. It exposes the global accessors and every factory function, and it is the only header a multithreading program needs. An MPI program also includes [`<gempba/mpi.hpp>`](#the-mpi-component-gempbampihpp) for its scheduler.

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

Returns a pointer to the active scheduler. Throws when none has been created, as in a multithreading program.

```cpp
scheduler* s = gempba::try_get_scheduler();
```

Non-throwing variant: returns `nullptr` when no scheduler has been created instead of throwing. Useful for read-only probes (telemetry uses it).

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

## Load balancer and node manager

```cpp
auto* lb = gempba::create_load_balancer(gempba::balancing_policy::QUASI_HORIZONTAL);
```

Create a load balancer using a built-in balancing policy. An MPI program passes its scheduler as well: `gempba::create_load_balancer(policy, scheduler)`.

```cpp
auto* lb = gempba::create_load_balancer(std::make_unique<MyLoadBalancer>());
```

Take ownership of a custom load balancer implementation. Your implementation holds the scheduler itself, if it uses one.

```cpp
auto& nm = gempba::create_node_manager(lb);
```

Create the node manager. One per process. An MPI program passes its scheduler as well: `gempba::create_node_manager(lb, scheduler)`.

---

## Nodes

```cpp
auto child = gempba::create_explicit_node<void>(
    *lb, parent, &my_func, std::make_tuple(args...)
);
```

Create a child node inside your recursive function. Arguments are captured eagerly. Note the node factories take the load balancer by reference, while `create_node_manager` takes it as a pointer.

```cpp
auto child = gempba::create_lazy_node<void>(
    *lb, parent, &my_func, args_initializer_fn
);
```

Lazy variant. Arguments are computed on demand, which is useful when preparing them is expensive and the branch might be pruned before it ever executes.

```cpp
auto child = gempba::create_explicit_node<void>(
    *lb, parent, &my_func,
    std::make_tuple(args...),
    args_serializer_fn,    // Args... -> task_packet
    args_deserializer_fn   // task_packet -> tuple<Args...>
);
```

Create a child node with serializers. An MPI program needs them, because a node that runs on another rank sends its arguments there as bytes. `create_lazy_node` takes the same pair after its initializer.

---

## The MPI component: `<gempba/mpi.hpp>`

```cpp
#include <gempba/mpi.hpp>
```

The schedulers that spread a run across MPI ranks. They come with the MPI component, so a program that includes this header links `gempba::mpi` (see [Installation](../../getting-started/installation.md#using-in-your-cmake-project-find_package)). Every rank runs the same setup.

```cpp
auto* s = gempba::mpi::create_scheduler(gempba::mpi::scheduler_topology::SEMI_CENTRALIZED);
```

Create a scheduler using a built-in topology, and install telemetry over MPI. Every rank calls it.

```cpp
auto* s = gempba::mpi::create_scheduler(std::make_unique<MyScheduler>());
```

Install a custom scheduler, which runs on MPI, and telemetry over MPI. Every rank calls it.

```cpp
auto* lb = gempba::create_load_balancer(gempba::balancing_policy::QUASI_HORIZONTAL, s);
auto& nm = gempba::create_node_manager(lb, s);
```

Pass the scheduler to the load balancer and the node manager.

```cpp
s->run(nm, runnables, std::move(seed));
```

Run this rank's part of the search. Every rank calls it with the same runnables, and it returns once the whole run has ended. Only the root, rank 0, passes the seed. It returns how the run ended; see [Stopping a run](#stopping-a-run).

```cpp
gempba::task_packet best = s->get_result();
```

The best result found across all ranks, once `run` has returned. Only the root may call it; any other rank throws.

```cpp
auto visitor = gempba::mpi::get_default_mpi_stats_visitor();
```

Returns the bundled [stats visitor](../implementations/stats-visitors/default-mpi-stats-visitor.md) for the MPI schedulers, ready to pass to the stats-collection API.

---

## Stopping a run

These come with `<gempba/core/stop.hpp>`, which this header includes. See [Stopping a Run](../../stopping-a-run.md) for how they fit together.

```cpp
gempba::request_stop();
```

Ask the run to stop. Returns at once and is safe from any thread. Nodes that haven't started are pruned from then on, nodes already running finish, and the run returns its best result so far. Under MPI every rank stops. The first stop wins, by any trigger, until `shutdown()`.

```cpp
bool stopping = gempba::stop_requested();
```

Whether a stop was requested since the last `shutdown()`, by any trigger. Long work inside one node can poll it to return early.

```cpp
gempba::stop_on_signals(false);
```

Whether `SIGINT` and `SIGTERM` stop the run gracefully instead of killing the process; on by default. While on, `create_node_manager` takes each of the two signals that nothing else handles yet, and `shutdown()` gives it back. A second `SIGINT` kills the process. Turning it off gives the signals back at once.

```cpp
gempba::run_outcome outcome = scheduler->run(nm, runnables, std::move(seed));
```

How the run ended, the same on every rank: `m_reason` (`end_reason::COMPLETED` or `INTERRUPTED`), `m_trigger` (`stop_trigger::NONE`, `CODE`, `SIGNAL` or `CONTROL`) and `m_signal`, the signal's number for a stop by signal. MPI programs only.

---

## Shutdown

```cpp
return gempba::shutdown();
```

Call at the end of `main()`. It destroys the scheduler, which finalizes MPI in an MPI program, so don't skip it there, and returns `EXIT_SUCCESS`. It also logs how a multithreading run ended, gives back the signals `create_node_manager` took, and clears the stop, so `stop_requested()` is `false` again.
