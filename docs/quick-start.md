# Quick Start: Your First Parallel Algorithm

This walks through a complete multithreading program: a synthetic binary-tree traversal that counts leaves in parallel. It is a trimmed version of the benchmark from [gempba-examples](https://github.com/rapastranac/gempba-examples), and it uses the public API exactly as your own algorithm would. The same pattern works for any recursive branching algorithm.

First install GemPBA (see [Installation](getting-started/installation.md)). This example uses the multithreading (`mt`) flavor, so no MPI is needed.

## The shape of a GemPBA program

Every GemPBA program follows the same three beats:

1. **Set up** a load balancer and a node manager, and configure the goal.
2. **Seed** the recursion with a root node, then submit it.
3. **Wait** for completion and read the result back.

Your algorithm is the recursive function in the middle. GemPBA owns the thread pool, the work queue, and the best-result bookkeeping.

## The recursive task

GemPBA inserts itself into your recursion through a small set of parameter additions. The recipe:

1. Add `std::thread::id` as the first parameter and `gempba::node` as the last parameter of your function.
2. Create a node for each branch inside the function.
3. Submit one branch to the thread pool, forward the other on the current thread.

```cpp
#include <gempba/gempba.hpp>

#include <atomic>

std::atomic<int> leaf_count{0};

// 1. std::thread::id first, gempba::node last; your arguments in between
void explore(std::thread::id tid, int depth, int max_depth, gempba::node parent) {
    gempba::node_manager& nm = gempba::get_node_manager();
    gempba::load_balancer& lb = *gempba::get_load_balancer();

    if (depth == max_depth) {                       // leaf: record a result
        int count = ++leaf_count;
        nm.try_update_result(count, gempba::score::make(count));
        return;
    }

    // The seed arrives with no parent; substitute a dummy so children
    // always have an anchor in the tree
    gempba::node effective_parent = parent == nullptr ? gempba::create_dummy_node(lb) : parent;

    // 2. Create a node per branch. Template arguments: <Ret, Args...>,
    //    where Args are your parameters minus the thread id and the node.
    gempba::node left = gempba::create_explicit_node<void, int, int>(
        lb, effective_parent, &explore, std::make_tuple(depth + 1, max_depth));
    gempba::node right = gempba::create_explicit_node<void, int, int>(
        lb, effective_parent, &explore, std::make_tuple(depth + 1, max_depth));

    // 3. Hand one child to the pool, keep walking the other on this thread
    nm.try_local_submit(left);
    nm.forward(right);
}
```

The `try_local_submit` / `forward` pair is the idiom: offer one branch to the thread pool, recurse into the other yourself. The quasi-horizontal load balancer decides which pending work is most valuable to hand out.

## The driver

```cpp
#include <iostream>
#include <stdexcept>

int main() {
    constexpr int MAX_DEPTH = 16;   // 2^16 = 65,536 leaves; raise it to make the machine sweat

    // 1. Set up
    gempba::load_balancer* lb = gempba::create_load_balancer(gempba::balancing_policy::QUASI_HORIZONTAL);
    gempba::node_manager& nm = gempba::create_node_manager(lb);

    nm.set_goal(gempba::MAXIMISE, gempba::score_type::I32);   // maximise an int score
    nm.set_thread_pool_size(8);
    nm.set_score(gempba::score::make(0));                     // initial score

    // 2. Seed the recursion from depth 0
    gempba::node seed = gempba::create_seed_node<void, int, int>(
        *lb, &explore, std::make_tuple(0, MAX_DEPTH));

    const double start = nm.get_wall_time();
    if (!nm.try_local_submit(seed)) {
        throw std::runtime_error("unable to submit seed node");
    }

    // 3. Wait and read results
    nm.wait();
    const double elapsed = nm.get_wall_time() - start;

    std::cout << "Score: " << nm.get_score().to_string() << '\n';
    std::cout << "Elapsed: " << elapsed << " s\n";
    std::cout << "Pool idle time: " << nm.get_idle_time() << " s\n";
    std::cout << "Thread requests: " << nm.get_thread_request_count() << '\n';

    return gempba::shutdown();
}
```

!!! note "Short form vs explicit namespaces"
    In a consumer build, the installed flavor's namespace is `inline`, so `gempba::create_load_balancer(...)` resolves to `gempba::multithreading::create_load_balancer(...)` (or the `multiprocessing` variant in an MPI build). Write the short form, as above; reach for the explicit `gempba::multithreading::` / `gempba::multiprocessing::` qualifiers only when you want to be unambiguous.

## Run it

The two snippets above form a single `main.cpp`: the task first, the driver below it. Wire it into a CMake project (see [Installation](getting-started/installation.md#using-in-your-cmake-project-find_package)):

```cmake
find_package(gempba REQUIRED)
target_link_libraries(my_app PRIVATE gempba::gempba)
```

Build, run, and watch all eight workers light up. For the full, runnable version of this program (with per-node cost simulation and benchmark plumbing), see `multithreading/src/benchmark.cpp` in [gempba-examples](https://github.com/rapastranac/gempba-examples).

## What changes for multiprocessing

The MPI flavor keeps the same recursive-task shape and adds a scheduler:

- `gempba::create_scheduler(topology, timeout)` comes first, and the load balancer / node manager factories additionally take the scheduler's `worker` view: `gempba::create_load_balancer(policy, worker)`, `gempba::create_node_manager(lb, worker)`.
- Node factories take a serializer / deserializer pair so a task's arguments can travel between ranks as a `gempba::task_packet`.
- The program is launched under `mpiexec`.

See the `multiprocessing` tree in [gempba-examples](https://github.com/rapastranac/gempba-examples) for a full MP program, and [IPC Topologies](scheduler-topologies.md) for the scheduler layouts.
