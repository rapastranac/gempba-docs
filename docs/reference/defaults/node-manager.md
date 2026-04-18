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

Push a node to the thread pool queue. Returns `false` if no idle thread picked it up and the node was resolved sequentially instead.

```cpp
nm.forward(node);
```

Execute the node on the current thread immediately. Even though this is a sequential call, wrapping the arguments in a node is not just boilerplate: the node stays registered in the exploration tree. If the library identifies an unresolved branch near the root of the current thread's subtree — one that was also handed to `forward` — it can push that root-level node to an idle thread before the current thread gets back to it. By the time the current thread reaches that node, it is already flagged as consumed or discarded, and the entire branch is skipped. This is the mechanism that keeps threads from redundantly exploring subtrees that another thread has already claimed, and it is central to the quasi-horizontal load balancing strategy described in the paper and thesis.

```cpp
nm.try_remote_submit(node, runnable_id);
```

Send a node to another IPC rank. Multiprocessing only.

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

Multiprocessing variant. Requires a serializer so the result can be transmitted across process boundaries:

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

Best score seen so far. Works in both multithreaded and multiprocessing modes.

```cpp
auto opt = nm.get_result<MyResult>();
```

Retrieve the actual result object. Returns `std::nullopt` if no result has been set. Multithreading only.

```cpp
std::optional<result> raw = nm.get_result_bytes();
```

Retrieve the result as raw bytes for deserialization. Multiprocessing only.

---

## Diagnostics

```cpp
double idle = nm.get_idle_time();
```

Cumulative time in milliseconds that threads spent idle waiting for work. High idle time usually means the tree is too narrow at the top, leaving threads with nothing to grab early on.

```cpp
std::size_t reqs = nm.get_thread_request_count();
```

Number of times threads requested work from the load balancer.

```cpp
int rank = nm.rank_me();
```

IPC rank of this process. Returns `-1` if not in multiprocessing mode.

```cpp
double elapsed = node_manager::get_wall_time();
```

Wall-clock time in milliseconds. Static method.
