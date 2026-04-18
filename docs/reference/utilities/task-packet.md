# `task_packet`

```cpp
#include <gempba/utils/task_packet.hpp>  // included automatically via gempba.hpp
```

`task_packet` is a raw byte buffer — a `std::vector<std::byte>` with a richer construction interface. It is the wire format for everything that crosses a process boundary in GemPBA: serialized function arguments, serialized return values, and serialized results.

Your serializer lambdas produce `task_packet` values; your deserializer lambdas consume them:

```cpp
// Serializer: Args... → task_packet
auto serializer = [](const MyGraph& g, int depth) -> gempba::task_packet {
    std::vector<std::byte> buf = /* encode g and depth */;
    return gempba::task_packet{std::move(buf)};
};

// Deserializer: task_packet → tuple<Args...>
auto deserializer = [](const gempba::task_packet& p) {
    return std::make_tuple(/* decode graph */, /* decode depth */);
};
```

---

## Constructors

```cpp
explicit task_packet(std::vector<std::byte> data);
```

Move or copy construct from an existing byte vector.

```cpp
explicit task_packet(std::size_t size);
```

Allocate an uninitialized buffer of `size` bytes. Useful when writing directly into the buffer after construction.

```cpp
task_packet(const char* buffer, std::size_t size);
```

Copy `size` bytes from a raw C buffer.

```cpp
explicit task_packet(const std::string& str);
```

Copy the contents of a string into the buffer.

---

## Buffer access

```cpp
std::byte*       data() noexcept;
const std::byte* data() const noexcept;
```

Pointer to the underlying byte array.

```cpp
std::size_t size() const noexcept;
```

Number of bytes in the buffer.

```cpp
bool empty() const noexcept;
```

Returns `true` if the buffer contains no bytes.

Iterators (`begin()` / `end()`) are also provided for range-for loops over the byte sequence.

---

## Comparison

```cpp
bool operator==(const task_packet&) const;
bool operator!=(const task_packet&) const;
auto operator<=>(const task_packet&) const;
```

Lexicographic ordering, with size compared first.

```cpp
static const task_packet EMPTY;
```

Singleton empty buffer. Useful as a sentinel or default value.
