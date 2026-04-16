# `load_balancer`

```cpp
#include <gempba/core/load_balancer.hpp>  // included automatically via gempba.hpp
```

`load_balancer` is the abstract interface for thread-level work distribution. It decides how pending branches are assigned to idle worker threads within a single process. You never call it directly in normal use — `node_manager` holds a pointer to one and delegates all submission calls through it.

This page documents the contract. For the built-in strategies that implement it, see [Quasi-Horizontal](../quasi-horizontal.md) and [Work-Stealing](../work-stealing.md).

## Contract

### Configuration

```cpp
virtual void set_thread_pool_size(unsigned int size) = 0;
```

Sets the number of worker threads. Call before submitting any work.

### Policy identification

```cpp
virtual balancing_policy get_balancing_policy() = 0;
```

Returns the `balancing_policy` enum value identifying this implementation. Useful when the load balancer is received as a pointer and you need to branch on strategy.

### Node ID generation

```cpp
virtual unsigned int generate_unique_id() = 0;
```

Returns a monotonically increasing identifier. Called internally by node factory functions to stamp each new node.

### Task submission

```cpp
virtual bool try_local_submit(node& p_node) = 0;
```

Attempts to push `p_node` to an idle thread. Returns `true` if a thread picked it up, `false` if the pool was full and the node was run inline. The implementation decides the scheduling policy — which thread, and what work to prioritize.

```cpp
virtual bool try_remote_submit(node& p_node, int runnable_id) = 0;
```

Attempts to send `p_node` to another process via the wired-in scheduler. `runnable_id` identifies which [`serial_runnable`](serial-runnable.md) on the remote side receives it. Only meaningful in multiprocessing mode.

```cpp
virtual void forward(node& p_node) = 0;
```

Executes `p_node` on the calling thread immediately. The implementation handles any post-execution bookkeeping (pruning, root correction) after the call returns.

```cpp
virtual std::future<std::any> force_local_submit(std::function<std::any()>&& fn) = 0;
```

Submits an arbitrary callable to the thread pool and returns a future. Used internally by the framework for result collection. Not intended for user code.

### Monitoring

```cpp
[[nodiscard]] virtual double       get_idle_time()            const = 0;
[[nodiscard]] virtual bool         is_done()                  const = 0;
[[nodiscard]] virtual std::size_t  get_thread_request_count() const = 0;
```

- `get_idle_time()` — cumulative wall-clock milliseconds that threads spent waiting for work.
- `is_done()` — `true` when the queue is empty and all threads are idle.
- `get_thread_request_count()` — total tasks submitted since startup.

### Synchronization

```cpp
virtual void wait() = 0;
```

Blocks until all queued and in-flight tasks complete. Delegated to by `node_manager::wait()`.

### Per-thread root management

```cpp
virtual std::shared_ptr<std::shared_ptr<node_core>>
    get_root(std::thread::id thread_id) = 0;

virtual void set_root(std::thread::id thread_id,
                      std::shared_ptr<node_core>& root) = 0;
```

Hooks for implementations that track a per-thread root pointer (quasi-horizontal). Implementations that do not use per-thread roots provide no-op stubs.

## Custom implementation

```cpp
class MyLoadBalancer : public gempba::load_balancer {
public:
    bool try_local_submit(gempba::node& p_node) override { /* ... */ }
    bool try_remote_submit(gempba::node& p_node, int id) override { /* ... */ }
    void forward(gempba::node& p_node) override { /* ... */ }

    void set_thread_pool_size(unsigned int size) override { /* ... */ }
    gempba::balancing_policy get_balancing_policy() override { /* ... */ }
    unsigned int generate_unique_id() override { /* ... */ }

    std::future<std::any> force_local_submit(std::function<std::any()>&& fn) override { /* ... */ }
    double       get_idle_time()            const override { /* ... */ }
    bool         is_done()                  const override { /* ... */ }
    std::size_t  get_thread_request_count() const override { /* ... */ }
    void         wait()                           override { /* ... */ }

    std::shared_ptr<std::shared_ptr<gempba::node_core>>
        get_root(std::thread::id id) override { return nullptr; }
    void set_root(std::thread::id id,
                  std::shared_ptr<gempba::node_core>& root) override {}
};

auto* lb = gempba::mt::create_load_balancer(std::make_unique<MyLoadBalancer>());
```

Your implementation navigates the recursion tree through [`node_traits`](node-traits.md). Study `quasi_horizontal_load_balancer` in `private/impl/load_balancing/` for the expected semantics of every tree navigation call before writing something from scratch.
