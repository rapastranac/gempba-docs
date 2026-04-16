# `scheduler`

```cpp
#include <gempba/core/scheduler.hpp>  // included automatically via gempba.hpp
```

`scheduler` is the abstract interface for process-level coordination. It defines the contract between the framework and the IPC transport underneath; how the initial task is seeded, how work is distributed, how the global best value propagates, and how termination is detected. The interface says nothing about MPI, UPC++, or any specific framework; that is an implementation concern.

`scheduler` extends [`scheduler_traits`](#scheduler_traits), which is also the base of the two inner role classes `center` and `worker`. All three share the same process-identity and synchronization methods.

The built-in implementations use OpenMPI. For their protocol details see [Scheduler Topologies](../../scheduler-topologies.md).

## Factory

```cpp
// Built-in topology
auto* s = gempba::mp::create_scheduler(gempba::mp::scheduler_topology::SEMI_CENTRALIZED);

// Bring your own implementation
auto* s = gempba::mp::create_scheduler(std::make_unique<MyScheduler>());
```

`scheduler_topology`:

| Value | Description |
|---|---|
| `SEMI_CENTRALIZED` | Center assigns workers; tasks travel point-to-point. Recommended. |
| `CENTRALIZED` | All tasks route through the center. Benchmarking only. |

## `scheduler_traits`

Both `scheduler` and its inner `center` / `worker` classes inherit from `scheduler_traits`. These methods are available on all three:

```cpp
virtual void barrier() = 0;
```
Global synchronization point — blocks until all processes reach this call.

```cpp
[[nodiscard]] virtual int rank_me()    const = 0;
[[nodiscard]] virtual int world_size() const = 0;
```
Process identity within the communicator. Rank 0 is the center.

```cpp
[[nodiscard]] virtual std::unique_ptr<stats> get_stats() const = 0;
```
Returns this process's runtime metrics as a [`stats`](stats.md) object. Workers hold compute stats (tasks sent/received, idle time, elapsed time); the center's stats are empty.

## `scheduler` interface

### Role access

```cpp
virtual scheduler::center& center_view() = 0;
virtual scheduler::worker& worker_view() = 0;
```

Returns the center-side or worker-side interface. Pass `worker_view()` to the load balancer and node manager factories.

### Configuration

```cpp
virtual void set_goal(goal goal, score_type type) = 0;
```

Sets the optimization direction (`MAXIMISE` or `MINIMISE`) and the numeric type of the score. Must match the goal set on `node_manager`.

```cpp
virtual void set_custom_initial_topology(tree&& topology) = 0;
```

Replaces the default startup waiting list with a custom process assignment tree. Only needed when the default `buildWaitingList` strategy is insufficient for your workload.

### Timing

```cpp
[[nodiscard]] virtual double elapsed_time() const = 0;
```

Wall-clock time (ms) from when `worker_view().run()` was called to when it returned.

### Stats collection

```cpp
virtual void synchronize_stats() = 0;
```

Gathers stats from all worker processes. Must be called by **all** processes after `run()` returns. After this call, `get_stats_vector()` is valid on rank 0.

```cpp
[[nodiscard]] virtual std::vector<std::unique_ptr<stats>> get_stats_vector() const = 0;
```

Returns one `stats` entry per rank. Index 0 (the center) holds an empty entry. Call only on rank 0, and only after `synchronize_stats()`.

## `scheduler::center`

The center role. Rank 0 calls these after seeding the initial task.

```cpp
virtual void run(task_packet task, int runnable_id) = 0;
```

Seeds the computation: sends `task` tagged with `runnable_id` to the first worker, then enters the coordination loop. Blocks until all workers signal termination.

```cpp
virtual task_packet         get_result()     = 0;
virtual std::vector<result> get_all_results() = 0;
```

`get_result()` — the single best result found across all workers.  
`get_all_results()` — one `result` entry per rank; index 0 (the center) holds an empty `result`.

## `scheduler::worker`

The worker role. All non-zero ranks call these inside their exploration loop.

```cpp
virtual void run(node_manager& nm,
                 std::map<int, std::shared_ptr<serial_runnable>> runnables) = 0;
```

Blocks until the center signals termination. Receives incoming `task_packet`s, dispatches each to the matching [`serial_runnable`](serial-runnable.md) by ID, and handles all IPC with the center.

```cpp
virtual unsigned int force_push(task_packet&& task, int function_id) = 0;
```

Sends a task directly to the next assigned waiting process, bypassing the normal pending-task queue. Returns the rank of the process that received it.

```cpp
[[nodiscard]] virtual unsigned int next_process() const = 0;
```

Returns the rank of the next process in the worker's waiting list, without consuming it.

```cpp
virtual std::optional<transmission_guard> try_open_transmission_channel() = 0;
```

Attempts a non-blocking lock on the outgoing transmission mutex. Returns a [`transmission_guard`](../utilities/transmission-guard.md) holding the lock on success, or `std::nullopt` if the channel is already in use. The guard releases the mutex on destruction.

## Custom scheduler

```cpp
class MyWorker : public gempba::scheduler::worker {
public:
    void run(gempba::node_manager& nm,
             std::map<int, std::shared_ptr<gempba::serial_runnable>> runnables) override { /* IPC loop */ }
    unsigned int force_push(gempba::task_packet&& task, int id) override { /* ... */ }
    unsigned int next_process() const override { /* ... */ }
    std::optional<gempba::transmission_guard> try_open_transmission_channel() override { /* ... */ }

    // scheduler_traits
    void barrier() override { /* ... */ }
    int  rank_me()    const override { /* ... */ }
    int  world_size() const override { /* ... */ }
    std::unique_ptr<gempba::stats> get_stats() const override { /* ... */ }
};

class MyCenter : public gempba::scheduler::center {
public:
    void run(gempba::task_packet task, int runnable_id) override { /* seed + coord loop */ }
    gempba::task_packet         get_result()      override { /* ... */ }
    std::vector<gempba::result> get_all_results() override { /* ... */ }

    // scheduler_traits
    void barrier() override { /* ... */ }
    int  rank_me()    const override { /* ... */ }
    int  world_size() const override { /* ... */ }
    std::unique_ptr<gempba::stats> get_stats() const override { /* ... */ }
};

class MyScheduler : public gempba::scheduler {
public:
    gempba::scheduler::center& center_view() override { return center_; }
    gempba::scheduler::worker& worker_view() override { return worker_; }

    void   set_goal(gempba::goal g, gempba::score_type t) override { /* ... */ }
    void   set_custom_initial_topology(gempba::tree&& t) override { /* ... */ }
    double elapsed_time() const override { /* ... */ }
    void   synchronize_stats() override { /* ... */ }
    std::vector<std::unique_ptr<gempba::stats>> get_stats_vector() const override { /* ... */ }

    // scheduler_traits
    void barrier() override { /* ... */ }
    int  rank_me()    const override { /* ... */ }
    int  world_size() const override { /* ... */ }
    std::unique_ptr<gempba::stats> get_stats() const override { /* ... */ }

private:
    MyCenter center_;
    MyWorker worker_;
};

auto* s = gempba::mp::create_scheduler(std::make_unique<MyScheduler>());
```
