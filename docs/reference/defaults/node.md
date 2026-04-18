# `node`

```cpp
#include <gempba/core/node.hpp>  // included automatically via gempba.hpp
```

`node` is a `final` class. You cannot inherit from it. Internally it holds a `shared_ptr<node_core>` and delegates every operation to the underlying implementation through composition. This is what makes the framework pluggable: you can replace `node_core` with a custom implementation without changing anything in user code or in `node` itself.

Because `node` is just a shared pointer wrapper, copying it is cheap and safe. Two copies of the same node refer to the same underlying branch in the tree.

`node` satisfies `node_traits<node>`, which is the contract that load balancers and the scheduler depend on. See [`node_traits`](../interfaces/node-traits.md) for the full interface.

---

## Factory functions

You do not construct nodes directly. Use the factory functions from `gempba.hpp`.

```cpp
auto left = gempba::mt::create_explicit_node<void>(
    lb, parent, &my_func, std::make_tuple(args...)
);
```

Create a child node inside your recursive function. Arguments are captured eagerly.

```cpp
auto child = gempba::mt::create_lazy_node<void>(
    lb, parent, &my_func, args_initializer_fn
);
```

Lazy variant. Arguments are computed on demand, useful when preparing them is expensive and the branch might be pruned before it executes.

```cpp
auto seed = gempba::create_seed_node<void>(*lb, &my_func, std::make_tuple(initial_args...));
```

Create the root of the search tree in `main()`. Has no parent node.

```cpp
auto dummy = gempba::create_dummy_node(*lb);
```

Create a placeholder node. Used when you need a root context without arguments.

---

## Function signature requirements

Every function you parallelize must follow this pattern:

```cpp
void my_func(std::thread::id tid, ArgType1 a, ArgType2 b, gempba::node parent);
```

For void functions. `std::thread::id` must be the first parameter and `gempba::node` must be the last. Your actual arguments go between them.

```cpp
MyResult my_func(std::thread::id tid, ArgType1 a, ArgType2 b, gempba::node parent);
```

For non-void functions. Same signature rules apply.

The `parent` node represents the current call in the tree. You use it to create child nodes for the next level of recursion.

---

## Null checks and copying

```cpp
if (left) { /* initialized */ }
if (left != nullptr) { /* same thing */ }
```

A default-constructed or moved-from node is null.

```cpp
gempba::node copy = left;
```

Cheap copy. Both `copy` and `left` refer to the same underlying `node_core`.

```cpp
if (left == right) { /* same underlying node_core */ }
```

Equality compares the underlying shared pointer.
