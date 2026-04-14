# `node.hpp`

```cpp
#include <gempba/core/node.hpp>  // included automatically via gempba.hpp
```

`node` is a `final` class. You cannot inherit from it. Internally it holds a `shared_ptr<node_core>` and delegates every operation to the underlying implementation through composition. This is what makes the framework pluggable: you can replace `node_core` with a custom implementation without changing anything in user code or in `node` itself.

Because `node` is just a shared pointer wrapper, copying it is cheap and safe. Two copies of the same node refer to the same underlying branch in the tree.

## You do not construct nodes directly

Factory functions in `gempba.hpp` create them:

```cpp
// Inside your recursive function
auto left = gempba::mt::create_explicit_node<void>(
    lb, parent, &my_func, std::make_tuple(args...)
);

// In main(), to start the whole thing
auto seed = gempba::create_seed_node<void>(*lb, &my_func, std::make_tuple(initial_args...));

// A dummy node acts as a placeholder (used when you need a root context without arguments)
auto dummy = gempba::create_dummy_node(*lb);
```

## Function signature requirements

Every function you parallelize must follow this pattern:

```cpp
// void return
void my_func(std::thread::id tid, ArgType1 a, ArgType2 b, gempba::node parent);

// non-void return
MyResult my_func(std::thread::id tid, ArgType1 a, ArgType2 b, gempba::node parent);
```

`std::thread::id` must be first. `gempba::node` must be last. Your actual arguments go between them. The `parent` node represents the current call in the tree, and you use it to create child nodes for the next level of recursion.

## Null checks and copying

```cpp
if (left) { /* initialized */ }
if (left != nullptr) { /* same thing */ }

gempba::node copy = left;  // cheap copy, same shared_ptr underneath

if (left == right) { /* same underlying node_core */ }
```

`node` satisfies `node_traits<node>`, which is the contract that load balancers and the scheduler depend on. See [`node_traits.hpp`](node-traits.md) for the full interface.
