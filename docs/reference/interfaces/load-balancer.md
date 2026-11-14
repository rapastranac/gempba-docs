# `load_balancer`

```cpp
#include <gempba/core/load_balancer.hpp>  // included automatically via gempba.hpp
```

Abstract interface for thread-level work distribution within a single process. `node_manager` holds a pointer to one and routes all submission calls through it.

Built-in implementations: [Quasi-Horizontal](../implementations/load-balancers/quasi-horizontal.md) (recommended), [Work-Stealing](../implementations/load-balancers/work-stealing.md) (baseline).

---

## Related types

```cpp
enum balancing_policy { QUASI_HORIZONTAL, WORK_STEALING };   // gempba::balancing_policy, <gempba/utils/gempba_utils.hpp>
```
The built-in strategies, at namespace scope. Returned by `get_balancing_policy()` and passed to `create_load_balancer`.

---

## Member functions

### Configuration

```cpp
virtual void set_thread_pool_size(unsigned int size) = 0;
```
Set number of worker threads. Call before submitting any work.

---

### Task submission

```cpp
virtual bool try_local_submit(node& p_node) = 0;
```
Hand `p_node` to an idle pool thread. Returns `true` when it was handed off or discarded, or a balancer had already dispatched it; `false` when no thread was free, in which case the balancer has already run it on the calling thread.

```cpp
virtual void forward(node& p_node) = 0;
```
Execute `p_node` on the calling thread immediately.

```cpp
virtual bool try_remote_submit(node& p_node, int runnable_id) = 0;
```
Send `p_node` to another process through the scheduler, falling back to `try_local_submit` when no process is free. `runnable_id` selects the matching [`serial_runnable`](serial-runnable.md) on the remote side. Returns `true` when it was sent, discarded or already dispatched; `false` after the fallback. Throws without a scheduler, so it belongs to MPI programs.

```cpp
virtual std::future<std::any> force_local_submit(std::function<std::any()>&&) = 0;
```
Submit an arbitrary callable to the thread pool and return a future. Internal use only.

---

### Monitoring

```cpp
[[nodiscard]] virtual double       get_idle_time()            const = 0;
[[nodiscard]] virtual bool         is_done()                  const = 0;
[[nodiscard]] virtual std::size_t  get_thread_request_count() const = 0;
[[nodiscard]] virtual unsigned int get_thread_pool_size()     const = 0;
[[nodiscard]] virtual std::size_t  get_tasks_running_count()  const = 0;
```

`get_idle_time()`: cumulative wall-clock seconds the pool spent waiting for work, averaged per thread.  
`get_starved_idle_time()` / `get_imbalanced_idle_time()`: the part of that idle time spent while no task ran in the pool, and while other threads ran tasks; 0 for a balancer that doesn't split it.  
`get_spawn_rejected_pool_full_count()` / `get_spawn_remote_rejected_count()`: submissions that found the pool full, and remote submissions that found no process free.  
`is_done()`: `true` when queue is empty and all threads are idle.  
`get_thread_request_count()`: total tasks submitted since startup.  
`get_thread_pool_size()`: current worker-thread count in the pool.  
`get_tasks_running_count()`: tasks executing on the pool right now. Together with `get_thread_pool_size()` this is what [telemetry](../../telemetry/index.md) samples for the live rank frames.

---

### Synchronization

```cpp
virtual void wait() = 0;
```
Block until all queued and in-flight tasks complete.

---

### Per-thread root management

```cpp
virtual std::shared_ptr<std::shared_ptr<node_core>>
    get_root(std::thread::id thread_id) = 0;

virtual void set_root(std::thread::id thread_id,
                      std::shared_ptr<node_core>& root) = 0;
```
Hooks for tracking a per-thread root pointer (quasi-horizontal strategy). Provide no-op stubs if unused.

---

### Identification

```cpp
virtual balancing_policy get_balancing_policy() = 0;
```
Enum value identifying this strategy.

```cpp
virtual unsigned int generate_unique_id() = 0;
```
Monotonically increasing node ID. Called internally by node factory functions.

---

## Custom implementation

```cpp
class MyLoadBalancer : public gempba::load_balancer {
    // implement all pure virtuals above
};

auto* lb = gempba::create_load_balancer(std::make_unique<MyLoadBalancer>());
```

The BYO overload serves multithreading and MPI programs alike; your implementation holds the scheduler itself, if it uses one.

Study `quasi_horizontal_load_balancer` in `src/core/private/impl/load_balancing/` for the expected semantics of every tree navigation call before writing from scratch.
