# Quick Start: Your First Parallel Algorithm

Here is the minimal code to parallelize a branching algorithm. The example explores a binary tree to depth 5 (2^5 = 32 leaves, manageable without melting your laptop). The same pattern works for any recursive algorithm.

The recipe is always three additions:

1. Add `std::thread::id` as the first parameter and `gempba::node` as the last parameter of your function
2. Create nodes for each branch inside the function
3. Submit one branch to the thread pool queue, forward the other on the current thread

```cpp
#include <gempba/gempba.hpp>
#include <iostream>

// 1. Add std::thread::id and gempba::node to the signature
void explore(std::thread::id tid, int depth, gempba::node parent) {
    auto& nm = gempba::get_node_manager();
    auto& lb = *gempba::get_load_balancer();

    if (depth == 0) {
        int result = 1;
        nm.try_update_result(result, gempba::score::make(1));
        return;
    }

    // 2. Create nodes for each branch
    auto left = gempba::mt::create_explicit_node<void>(
        lb, parent, &explore, std::make_tuple(depth - 1)
    );
    auto right = gempba::mt::create_explicit_node<void>(
        lb, parent, &explore, std::make_tuple(depth - 1)
    );

    // 3. Submit one to the thread pool, run the other here
    nm.try_local_submit(left);
    nm.forward(right);
}

int main() {
    auto* lb = gempba::mt::create_load_balancer(gempba::balancing_policy::QUASI_HORIZONTAL);
    auto& nm = gempba::mt::create_node_manager(lb);

    nm.set_goal(gempba::goal::MAXIMISE, gempba::score_type::I32);
    nm.set_thread_pool_size(4);
    nm.set_score(gempba::score::make(0));

    // Kick off the search from depth 5
    auto seed = gempba::create_seed_node<void>(*lb, &explore, std::make_tuple(5));
    nm.try_local_submit(seed);
    nm.wait();

    std::cout << "Done! Explored the tree in parallel." << std::endl;
    return gempba::shutdown();
}
```

That is the whole pattern. Your algorithm stays almost unchanged. GemPBA inserts itself through the node parameters and manages all the scheduling. Check the [Examples](examples.md) page for production-ready code with multiprocessing, result tracking, and serialization.
