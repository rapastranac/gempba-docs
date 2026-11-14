# `node_manager`

`node_manager` is a concrete class. It is intentionally not extensible: every user of GemPBA interacts with the same control interface, and there is no reason for different implementations. You get it from `gempba::get_node_manager()` or from the factory function.

Think of it as your algorithm's control panel: configure the goal, submit work, wait for completion, and collect the result.

---

## Setup

```cpp
nm.set_goal(gempba::goal::MAXIMISE, gempba::score_type::I32);
nm.set_goal(gempba::goal::MINIMISE, gempba::score_type::F64);
```

Set the optimization direction and the numeric type used to represent scores. Call before submitting any work. Available score types:

```cpp
enum class score_type : std::uint8_t {
    I32, U_I32, I64, U_I64, F32, F64, F128
};
```

`set_goal` accepts `I32`, `I64`, `F32`, `F64` and `F128`. `U_I32` and `U_I64` are in the enum, but `set_goal` has no starting score for them and throws.

`I32` is the default. The score represents whatever "best" means for your problem: minimum cost, maximum coverage, shortest path length. You define the semantics. `F128` maps to `long double`.

```cpp
nm.set_score(gempba::score::make(0));
```

Set the initial best-known score. Your algorithm improves from this value.

```cpp
nm.set_thread_pool_size(std::thread::hardware_concurrency());
```

Set the number of worker threads.

---

## Submitting work

```cpp
bool queued = nm.try_local_submit(node);
```

Hand a node to a pool thread. Returns `true` when it was handed off or discarded, including earlier by the balancer; `false` when no thread was free and it ran on the calling thread instead.

```cpp
nm.forward(node);
```

Execute the node on the current thread immediately. Even though this is a sequential call, wrapping the arguments in a node is not just boilerplate: the node stays registered in the exploration tree. If the library identifies an unresolved branch near the root of the current thread's subtree, a node still `UNUSED`, it can push that root-level node to an idle thread before the current thread gets back to it. By the time the current thread reaches that node, it is already flagged as consumed or discarded, and the entire branch is skipped. This is the mechanism that keeps threads from redundantly exploring subtrees that another thread has already claimed, and it is central to the quasi-horizontal load balancing strategy described in the paper and thesis.

```cpp
nm.try_remote_submit(node, runnable_id);
```

Send a node to another rank, falling back to `try_local_submit` when no rank is free. Returns `true` when the node was sent or discarded, or had already been dispatched; `false` after the fallback. MPI programs only: it needs a scheduler.

```cpp
nm.wait();
```

Block until all work is complete. Mainly to be used in the main thread after submitting the initial node(s). Worker threads should not call this, as they are expected to keep processing work until the entire tree is done.

The typical pattern inside a recursive function:

```cpp
void my_func(std::thread::id tid, /* your args */, gempba::node parent) {
    // ... create left and right nodes ...

    nm.try_local_submit(left);  // offer to the thread pool
    nm.forward(right);          // run this one on the current thread
}
```

`try_local_submit` either sends `left` to an idle thread or runs it locally if no thread is free. `forward` always runs on the current thread. The load balancer makes the actual scheduling decision.

---

## Updating results

```cpp
bool improved = nm.try_update_result(candidate, gempba::score::make(42));
```

Report a candidate solution found by your algorithm. Thread-safe. Compares the new score against the current best and updates only if the new one is better according to the goal you set. Returns `true` if the update happened.

```cpp
nm.try_update_result(candidate, new_score, serializer);
```

MPI variant. Requires a serializer so the result can be transmitted across process boundaries:

```cpp
std::function<task_packet(MyResult&)> serializer = [](MyResult& r) {
    return task_packet{/* r serialized */};
};
```

---

## Reading results

```cpp
gempba::score best = nm.get_score();
```

Best score seen so far. Works in multithreading and MPI programs alike.

```cpp
auto opt = nm.get_result<MyResult>();
```

Retrieve the result object stored by the first `try_update_result` overload, as a multithreading program does. Returns `std::nullopt` if no result has been set.

```cpp
std::optional<result> raw = nm.get_result_bytes();
```

Retrieve the result stored as bytes by the serializer overload, as an MPI program does on each rank. Across ranks, read [`scheduler::get_result()`](../interfaces/scheduler.md) on rank 0.

---

## Diagnostics

```cpp
double idle = nm.get_idle_time();
```

Seconds the pool threads spent idle waiting for work, per thread. High idle time usually means the tree is too narrow at the top, leaving threads with nothing to grab early on.

```cpp
std::size_t reqs = nm.get_thread_request_count();
```

Number of times threads requested work from the load balancer.

```cpp
int rank = nm.rank_me();
```

This process's rank. Returns `-1` without a scheduler, as in a multithreading program.

```cpp
double elapsed = node_manager::get_wall_time();
```

Wall-clock time in seconds since the epoch; subtract two readings for an elapsed time. Static method.

```cpp
bool done = nm.is_done();
```

Whether the pool has no task left, queued or running, without blocking as `wait()` does.

```cpp
std::future<std::any> f = nm.force_local_submit([] { return std::any{}; });
```

Queue a plain function on the pool, whether or not a thread is free, and get its future. It counts as a thread request.

```cpp
gempba::balancing_policy policy = nm.get_balancing_policy();
unsigned int id = nm.generate_unique_id();
```

The load balancer's policy, and a fresh id from it. `set_balancing_policy()` only records a value on the node manager and doesn't change the balancer; pick the policy with `create_load_balancer`.
