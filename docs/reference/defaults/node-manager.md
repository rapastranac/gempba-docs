# `node_manager`

`node_manager` is a concrete class. It is intentionally not extensible: every user of GemPBA interacts with the same control interface, and there is no reason for different implementations. You get it from `gempba::get_node_manager()` or from the factory function.

Think of it as your algorithm's control panel: configure the goal, submit work, wait for completion, and collect the result.

## Setup

Call these before submitting any work:

```cpp
// Set the optimization direction and score representation type
nm.set_goal(gempba::goal::MAXIMISE, gempba::score_type::I32);
// or
nm.set_goal(gempba::goal::MINIMISE, gempba::score_type::F64);

// Set the initial best-known score (your algorithm improves from here)
nm.set_score(gempba::score::make(0));

// Set the number of worker threads
nm.set_thread_pool_size(std::thread::hardware_concurrency());
```

Available score types:

| Type | Use when |
|---|---|
| `I32` (default) | Integer scores, 32-bit range |
| `I64` | Integer scores, 64-bit range |
| `U_I32`, `U_I64` | Unsigned integer scores |
| `F32`, `F64`, `F128` | Floating point scores |

The score represents whatever "best" means for your problem: minimum cost, maximum coverage, shortest path length, fewest moves. You define the semantics.

## Submitting work

```cpp
// Push a node to the thread pool queue
// Returns false if no thread picked it up (it was resolved sequentially)
bool queued = nm.try_local_submit(node);

// Execute the node on the current thread immediately
nm.forward(node);

// (Multiprocessing) Send a node to another MPI rank
nm.try_remote_submit(node, runnable_id);

// Block until all work is complete
nm.wait();
```

The typical pattern inside a recursive function:

```cpp
void my_func(std::thread::id tid, /* your args */, gempba::node parent) {
    // ... create left and right nodes ...

    nm.try_local_submit(left);  // offer to the thread pool
    nm.forward(right);           // run this one on the current thread
}
```

`try_local_submit` either sends `left` to an idle thread or runs it locally if no thread is free. `forward` always runs on the current thread. The load balancer makes the actual scheduling decision.

## Updating results

When your algorithm finds a candidate solution, report it:

```cpp
// Pass the result by reference (not a literal) and its score
MyResult candidate = compute_candidate();
bool improved = nm.try_update_result(candidate, gempba::score::make(42));
```

`try_update_result` is thread-safe. It locks internally, compares the new score against the current best, and updates only if the new one is better according to the goal you set. Returns `true` if the update actually happened.

In multiprocessing mode, you also need a serializer so the result can be transmitted across process boundaries:

```cpp
std::function<task_packet(MyResult&)> serializer = [](MyResult& r) {
    return task_packet{/* r serialized */};
};

nm.try_update_result(candidate, new_score, serializer);
```

## Reading results

```cpp
// Best score seen so far (works in both mt and mp modes)
gempba::score best = nm.get_score();

// Multithreading: retrieve the actual result object
auto opt = nm.get_result<MyResult>();      // returns std::nullopt if not set

// Multiprocessing: retrieve result as raw bytes for deserialization
std::optional<result> raw = nm.get_result_bytes();
```

## Diagnostics

```cpp
double idle    = nm.get_idle_time();              // cumulative thread idle time (ms)
size_t reqs    = nm.get_thread_request_count();   // number of times threads requested work
int    rank    = nm.rank_me();                    // MPI rank (-1 if not in mp mode)
double elapsed = node_manager::get_wall_time();   // wall clock time
```

The idle time metric is useful for performance tuning. High idle time usually means the tree is too narrow at the top (not enough parallel work early on) or the branching factor drops off faster than threads can grab tasks.
