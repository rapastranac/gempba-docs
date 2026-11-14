# `queue`

```cpp
#include <gempba/utils/queue.hpp>  // not included by gempba.hpp
```

`queue<T>` is a thread-safe FIFO queue. It wraps `std::queue<T>` with a `std::mutex`, making push, pop, and empty-check safe to call from multiple threads concurrently without external synchronization.

Sourced from [CTPL](https://github.com/vit-vit/CTPL) by Vitaliy Vitsentiy (Apache 2.0).

Used internally by the MPI schedulers for their outgoing tasks. Not intended for direct use in user code.

---

## Interface

```cpp
bool push(const T& value);
```

Adds `value` to the back of the queue. Always succeeds; returns `true`.

```cpp
bool pop(T& out);
```

Removes the front element into `out`. Returns `false` if the queue is empty, leaving `out` unchanged.

```cpp
bool empty();
```

Returns `true` if the queue contains no elements.

All three methods lock the internal mutex for their duration.
