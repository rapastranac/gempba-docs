# `scheduler`

```cpp
#include <gempba/core/scheduler.hpp>  // included automatically via gempba.hpp
```

Abstract interface for process-level coordination. Defines the IPC contract without coupling to any specific transport (MPI, UPC++, etc.). Extends [`scheduler_traits`](#scheduler_traits), which is also the base of the two inner role classes `center` and `worker`.

Built-in implementations use OpenMPI. For protocol details see [Scheduler Topologies](../../scheduler-topologies.md).

---

## Factory

```cpp
auto* s = gempba::mp::create_scheduler(gempba::mp::scheduler_topology::SEMI_CENTRALIZED);
auto* s = gempba::mp::create_scheduler(std::make_unique<MyScheduler>());
```

| `scheduler_topology` | Description |
|---|---|
| `SEMI_CENTRALIZED` | Center assigns workers; tasks travel point-to-point. Recommended. |
| `CENTRALIZED` | All tasks route through the center. Benchmarking only. |

---

## `scheduler_traits` (shared base)

Available on `scheduler`, `scheduler::center`, and `scheduler::worker`.

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
This process's runtime metrics. Workers hold compute stats; the center's stats are empty.

---

## `scheduler` interface

### Role access

```cpp
virtual scheduler::center& center_view() = 0;
virtual scheduler::worker& worker_view() = 0;
```
Return the center-side or worker-side interface. Pass `worker_view()` to the load balancer and node manager factories.

---

### Configuration

```cpp
virtual void set_goal(goal, score_type) = 0;
```
Set optimization direction (`MAXIMISE`/`MINIMISE`) and score numeric type. Must match the goal set on `node_manager`.

```cpp
virtual void set_custom_initial_topology(tree&&) = 0;
```
Replace the default startup waiting list with a custom process assignment tree.

---

### Stats collection

```cpp
virtual void synchronize_stats() = 0;
```
Gather stats from all workers. Must be called by **all** processes after `run()` returns.

```cpp
[[nodiscard]] virtual std::vector<std::unique_ptr<stats>> get_stats_vector() const = 0;
```
One `stats` entry per rank. Index 0 (center) is empty. Call only on rank 0 after `synchronize_stats()`.

---

### Timing

```cpp
[[nodiscard]] virtual double elapsed_time() const = 0;
```
Wall-clock time (ms) from `worker_view().run()` call to return.

---

## `scheduler::center`

Role for rank 0, called after seeding the initial task.

```cpp
virtual void run(task_packet task, int runnable_id) = 0;
```
Seed `task` to the first worker tagged with `runnable_id`, then enter the coordination loop until all workers signal termination.

```cpp
virtual task_packet         get_result()      = 0;
virtual std::vector<result> get_all_results() = 0;
```
`get_result()` — single best result found across all workers.  
`get_all_results()` — one `result` per rank; index 0 (center) holds an empty `result`.

---

## `scheduler::worker`

Role for all non-zero ranks.

```cpp
virtual void run(node_manager& nm,
                 std::map<int, std::shared_ptr<serial_runnable>> runnables) = 0;
```
Block until center signals termination. Dispatch incoming `task_packet`s to matching [`serial_runnable`](serial-runnable.md)s by ID.

```cpp
virtual unsigned int force_push(task_packet&& task, int function_id) = 0;
```
Send a task directly to the next assigned waiting process, bypassing the pending-task queue. Returns the receiving rank.

```cpp
[[nodiscard]] virtual unsigned int next_process() const = 0;
```
Rank of the next process in the waiting list without consuming it.

```cpp
virtual std::optional<transmission_guard> try_open_transmission_channel() = 0;
```
Non-blocking lock on the outgoing transmission mutex. Returns `nullopt` if the channel is already in use.

---

## Custom implementation

```cpp
class MyWorker  : public gempba::scheduler::worker  { /* ... */ };
class MyCenter  : public gempba::scheduler::center  { /* ... */ };

class MyScheduler : public gempba::scheduler {
    gempba::scheduler::center& center_view() override { return center_; }
    gempba::scheduler::worker& worker_view() override { return worker_; }
    // implement remaining scheduler and scheduler_traits pure virtuals
private:
    MyCenter center_;
    MyWorker worker_;
};

auto* s = gempba::mp::create_scheduler(std::make_unique<MyScheduler>());
```
