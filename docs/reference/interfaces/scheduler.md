# `scheduler`

```cpp
#include <gempba/core/scheduler.hpp>  // included automatically via gempba.hpp
```

Abstract interface for process-level coordination. Every rank holds one scheduler and calls its [`run`](#running-a-search); rank 0, the root, seeds the run and reads its results. Extends [`scheduler_traits`](#scheduler_traits-shared-base).

Built-in implementations use MPI (OpenMPI on Linux/macOS, MS-MPI on Windows) and come with the MPI component, `gempba::mpi`. A custom scheduler is installed with `gempba::mpi::create_scheduler`, which also sets up telemetry over MPI, so it runs on MPI too. For protocol details see [Scheduler Topologies](../../scheduler-topologies.md).

---

## Factory

```cpp
#include <gempba/mpi.hpp>

auto* s = gempba::mpi::create_scheduler(gempba::mpi::scheduler_topology::SEMI_CENTRALIZED);
auto* s = gempba::mpi::create_scheduler(std::make_unique<MyScheduler>());
```

| `scheduler_topology` | Description |
|---|---|
| `SEMI_CENTRALIZED` | The coordinator assigns workers; tasks travel point-to-point. Recommended. |
| `CENTRALIZED` | All tasks route through the coordinator. Benchmarking only. |

---

## `scheduler_traits` (shared base)

The base of `scheduler`.

```cpp
virtual void barrier() = 0;
```
Global synchronization point — blocks until all processes reach this call.

```cpp
[[nodiscard]] virtual int rank_me()    const = 0;
[[nodiscard]] virtual int world_size() const = 0;
```
Process identity within the communicator. Rank 0 is the root; in the built-in schedulers it is also the coordinator.

```cpp
[[nodiscard]] virtual std::unique_ptr<stats> get_stats() const = 0;
```
This process's runtime metrics. Workers hold compute stats; the coordinator holds its own counts and elapsed time.

---

## `scheduler` interface

### Configuration

```cpp
virtual void set_goal(goal, score_type) = 0;
```
Set optimization direction (`MAXIMISE`/`MINIMISE`) and score numeric type. Must match the goal set on `node_manager`.

```cpp
virtual void set_custom_initial_topology(tree&&) = 0;
```
Replace the default startup waiting list, a binomial tree over the workers, with a custom process assignment tree. The semi-centralized scheduler uses it; the centralized one, where every task goes through the coordinator, ignores it.

---

### Running a search

```cpp
run_outcome run(node_manager& nm,
                std::map<int, std::shared_ptr<serial_runnable>> runnables,
                std::optional<task_bundle> seed = std::nullopt);
```
Run this rank's part of the search. Every rank calls it with the same runnables, and it returns once the whole run has ended, with how it ended, the same on every rank; the root also logs it (see [Stopping a Run](../../stopping-a-run.md#reading-how-it-ended)). Only the root passes the seed; a root without one, or another rank with one, throws `std::invalid_argument`. Incoming `task_packet`s are dispatched to the matching [`serial_runnable`](serial-runnable.md) by ID.

```cpp
[[nodiscard]] task_packet         get_result();
[[nodiscard]] std::vector<result> get_all_results();
```
`get_result()` — single best result found across all ranks.  
`get_all_results()` — each rank's best result, indexed by rank and empty where a rank found none.  
Both are for the root once `run` has returned; any other rank throws `std::logic_error`.

```cpp
[[nodiscard]] bool is_root() const;
```
Whether this rank is the root, rank 0.

---

### Task transfer

```cpp
virtual unsigned int force_push(task_packet&& task, int function_id) = 0;
```
Hand `task` to another rank, to run under the runnable `function_id`. Returns the receiving rank.

```cpp
virtual std::optional<transmission_guard> try_open_transmission_channel() = 0;
```
Non-blocking lock on the outgoing transmission mutex. Returns `nullopt` if the channel is already in use, and in the built-in schedulers also when there is nowhere to send: the semi-centralized one has no waiting process assigned to this rank, or the centralized coordinator is full.

---

### Stats collection

```cpp
virtual void synchronize_stats() = 0;
```
Gather every rank's stats on rank 0. Collective: **every** rank calls it after `run()` returns.

```cpp
[[nodiscard]] virtual std::vector<std::unique_ptr<stats>> get_stats_vector() const = 0;
```
One `stats` entry per rank, index 0 included: the coordinator's own counts and elapsed time. Call only on rank 0 after `synchronize_stats()`.

---

### Timing

```cpp
[[nodiscard]] virtual double elapsed_time() const = 0;
```
Wall-clock seconds from run start to termination.

---

### Monitoring

```cpp
[[nodiscard]] virtual std::size_t get_pending_request_count() const = 0;
```
Outstanding requests in the scheduler queue: the centralized coordinator's queued tasks, and always 0 for the semi-centralized scheduler, which queues none. Sampled by [telemetry](../../telemetry/index.md) for the rank frames.

---

## Custom implementation

```cpp
class MyScheduler : public gempba::scheduler {
    // implement the remaining scheduler and scheduler_traits pure virtuals
protected:
    gempba::run_outcome do_run(gempba::node_manager& nm,
                               std::map<int, std::shared_ptr<gempba::serial_runnable>> runnables,
                               std::optional<gempba::task_bundle> seed) override;
    gempba::task_packet do_get_result() override;
    std::vector<gempba::result> do_get_all_results() override;
};

auto* s = gempba::mpi::create_scheduler(std::make_unique<MyScheduler>());
```

`run`, `get_result` and `get_all_results` check the caller's rank, then call these. `do_run` is this rank's part of the run, with `seed` set exactly on the root, and returns the same `run_outcome` on every rank. gempba's [`custom-schedulers.md`](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/custom-schedulers.md) lists what a custom scheduler must do to feed telemetry and to take part in a stop.
