# `Queue`

```cpp
#include <gempba/utils/Queue.hpp>  // included automatically via gempba.hpp
```

`Queue<T>` is a thread-safe FIFO queue. It wraps `std::queue<T>` with a `std::mutex`, making push, pop, and empty-check safe to call from multiple threads concurrently without external synchronization.

Sourced from [CTPL](https://github.com/vit-vit/CTPL) by Vitaliy Vitsentiy (Apache 2.0).

Used internally by the thread pool. Not intended for direct use in user code.

## Interface

```cpp
bool push(const T& value);   // always succeeds; returns true
bool pop(T& out);            // returns false if empty, otherwise pops front into out
bool empty();                // returns true if the queue has no elements
```

All three methods lock the internal mutex for their duration.
