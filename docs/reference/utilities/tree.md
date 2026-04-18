# `tree`

```cpp
#include <gempba/utils/tree.hpp>  // included automatically via gempba.hpp
```

`tree` is an index-based tree data structure. Nodes are stored in a flat `std::vector` and identified by integer index. Each node tracks its parent, left and right siblings, and an ordered child list, all via raw pointers into the same vector.

Used internally by the semi-centralized scheduler to represent the process assignment topology built during the startup phase. Not intended for direct use in user code.

Non-copyable. Movable.

---

## Constructors

```cpp
explicit tree(std::size_t size);
```

Pre-allocate `size` nodes, indexed `0 … size-1`.

```cpp
tree();
```

Construct an empty tree. Call `resize()` before accessing nodes.

```cpp
void resize(std::size_t size);
```

Append `size` additional nodes to the existing tree.

---

## Tree access

```cpp
tree_node& operator[](int index);
```

Returns a reference to the node at `index`.

```cpp
std::size_t size() const;
```

Returns the total number of nodes in the tree.

---

## `tree_node`

Each node exposes the following interface.

### Mutation

```cpp
void add_next(int child_index);
```

Append a child node by index.

```cpp
void pop_front();
```

Remove and unlink the first child.

```cpp
void release();
```

Detach this node from its parent.

```cpp
void clear();
```

Remove all children from this node.

### Query

```cpp
bool is_assigned() const;
```

Returns `true` if this node has a parent.

```cpp
bool has_next() const;
```

Returns `true` if this node has at least one child.

```cpp
int get_next() const;
```

Returns the index of the first child, or `-1` if there are none.

```cpp
int get_parent() const;
```

Returns the index of the parent node, or `-1` if this is a root node.

```cpp
int size() const;
```

Returns the number of direct children.

### Iteration

```cpp
for (int child_idx : tree[node_idx]) { /* ... */ }
```

Range-for over a node's direct children by index.

---

## Diagnostics

```cpp
std::string to_string() const;
```

Returns an indented text representation of the full tree. Useful for debugging topology issues.
