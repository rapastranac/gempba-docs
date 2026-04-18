# `transmission_guard`

```cpp
#include <gempba/utils/transmission_guard.hpp>  // included automatically via gempba.hpp
```

`transmission_guard` is a RAII wrapper around a `std::unique_lock<std::mutex>`. It holds a mutex lock for exactly the duration of an IPC send, releasing it automatically on destruction.

Non-copyable. Movable.

Used internally by the scheduler worker's communication thread. Not intended for direct use in user code.

---

## Constructor

```cpp
explicit transmission_guard(std::unique_lock<std::mutex>&& lock);
```

Takes ownership of `lock`. The mutex is released automatically when the guard is destroyed, whether by normal scope exit or exception. This guarantees that the mutex protecting an outgoing transmission is always unlocked, even if the send throws.
