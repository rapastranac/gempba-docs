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

## Constructors

```cpp
explicit task_packet(std::vector<std::byte> data);   // move or copy from byte vector
explicit task_packet(std::size_t size);               // allocate uninitialized buffer
task_packet(const char* buffer, std::size_t size);    // copy from raw C buffer
explicit task_packet(const std::string& str);         // copy from string
```

## Buffer access

```cpp
std::byte*       data() noexcept;
const std::byte* data() const noexcept;
std::size_t      size() const noexcept;
bool             empty() const noexcept;
```

Iterators (`begin()` / `end()`) are also provided for range-for loops over the byte sequence.

## Comparison

`==`, `!=`, and `<=>` (lexicographic, size first) are all defined. `task_packet::EMPTY` is the singleton empty buffer.
