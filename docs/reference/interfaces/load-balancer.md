# `load_balancer`

```cpp
#include <gempba/core/load_balancer.hpp>  // included automatically via gempba.hpp
```

Abstract interface for thread-level work distribution within a single process. `node_manager` holds a pointer to one and routes all submission calls through it.

Built-in implementations: [Quasi-Horizontal](../implementations/load-balancers/quasi-horizontal.md) (recommended), [Work-Stealing](../implementations/load-balancers/work-stealing.md) (baseline).

---

## Member types

```cpp
enum balancing_policy { /* implementation-defined values */ };
```
Enum identifying the concrete strategy. Returned by `get_balancing_policy()`.

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
Attempt to push `p_node` to an idle thread. Returns `false` if pool is full — the caller must run the node inline.

```cpp
virtual void forward(node& p_node) = 0;
```
Execute `p_node` on the calling thread immediately.

```cpp
virtual bool try_remote_submit(node& p_node, int runnable_id) = 0;
```
Send `p_node` to another process via the wired-in scheduler. `runnable_id` selects the matching [`serial_runnable`](serial-runnable.md) on the remote side. Only meaningful in multiprocessing mode.

```cpp
virtual std::future<std::any> force_local_submit(std::function<std::any()>&&) = 0;
```
Submit an arbitrary callable to the thread pool and return a future. Internal use only.

---

### Monitoring

```cpp
[[nodiscard]] virtual double      get_idle_time()            const = 0;
[[nodiscard]] virtual bool        is_done()                  const = 0;
[[nodiscard]] virtual std::size_t get_thread_request_count() const = 0;
```

`get_idle_time()` — cumulative wall-clock milliseconds threads spent waiting for work.  
`is_done()` — `true` when queue is empty and all threads are idle.  
`get_thread_request_count()` — total tasks submitted since startup.

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

auto* lb = gempba::mt::create_load_balancer(std::make_unique<MyLoadBalancer>());
```

Study `quasi_horizontal_load_balancer` in `private/impl/load_balancing/` for the expected semantics of every tree navigation call before writing from scratch.
