# `tree`

```cpp
#include <gempba/utils/tree.hpp>  // included automatically via gempba.hpp
```

`tree` is an index-based tree data structure. Nodes are stored in a flat `std::vector` and identified by integer index. Each node tracks its parent, left and right siblings, and an ordered child list, all via raw pointers into the same vector.

Used internally by the semi-centralized scheduler to represent the process assignment topology built during the startup phase (`buildWaitingList`). Not intended for direct use in user code.

Non-copyable. Movable.

## Construction

```cpp
explicit tree(std::size_t size);  // pre-allocate size nodes, indexed 0 … size-1
tree();                           // empty; use resize() before accessing nodes
void resize(std::size_t size);    // append size additional nodes
```

## Node access

```cpp
tree_node& operator[](int index);
std::size_t size() const;
```

`tree_node` exposes:

```cpp
void add_next(int child_index);    // append a child
void pop_front();                  // remove and unlink the first child
void release();                    // detach this node from its parent
void clear();                      // remove all children

bool is_assigned() const;          // true if this node has a parent
bool has_next() const;             // true if this node has at least one child
int  get_next() const;             // index of first child, or -1
int  get_parent() const;           // index of parent, or -1
int  size() const;                 // number of direct children
```

Iteration over a node's children:

```cpp
for (int child_idx : tree[node_idx]) { /* ... */ }
```

## Diagnostics

```cpp
std::string to_string() const;  // indented text representation of the full tree
```
