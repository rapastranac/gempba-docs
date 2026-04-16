# `transmission_guard`

```cpp
#include <gempba/utils/transmission_guard.hpp>  // included automatically via gempba.hpp
```

`transmission_guard` is a RAII wrapper around a `std::unique_lock<std::mutex>`. It holds a mutex lock for exactly the duration of an IPC send, releasing it automatically on destruction.

Non-copyable. Movable.

```cpp
explicit transmission_guard(std::unique_lock<std::mutex>&& lock);
```

The lock is transferred into the guard on construction. When the guard goes out of scope — whether normally or by exception — the lock is released. This guarantees that the mutex protecting an outgoing transmission is always unlocked, even if the send throws.

Used internally by the scheduler worker's communication thread. Not intended for direct use in user code.
