# `score`

```cpp
#include <gempba/utils/score.hpp>  // included automatically via gempba.hpp
```

`score` is a fixed-size, type-erased numeric value. It holds exactly one value of a supported numeric type in a 16-byte payload plus a 1-byte type tag, making it trivially copyable and safe for IPC transmission without serialization overhead.

It is the currency of the optimization objective: every call to `nm.set_score()`, `nm.try_update_result()`, and `nm.get_score()` works in terms of `score`.

```cpp
static_assert(sizeof(score) == 17);               // 1 byte tag + 16 byte payload
static_assert(std::is_trivially_copyable_v<score>);
static_assert(std::is_standard_layout_v<score>);
```

---

## `score_type`

```cpp
enum class score_type : std::uint8_t {
    I32, U_I32, I64, U_I64, F32, F64, F128
};
```

Identifies which numeric type a `score` holds. `F128` maps to `long double`.

---

## Construction

```cpp
template<typename T>
static constexpr score score::make(T value) noexcept;
```

Factory for all supported types. The template parameter is deduced — pass the value directly:

```cpp
auto s = gempba::score::make(42);      // score_type::I32
auto s = gempba::score::make(42u);     // score_type::U_I32
auto s = gempba::score::make(42LL);    // score_type::I64
auto s = gempba::score::make(3.14f);   // score_type::F32
auto s = gempba::score::make(3.14);    // score_type::F64
auto s = gempba::score::make(3.14L);   // score_type::F128
```

---

## Accessors

```cpp
template<typename T>
[[nodiscard]] T get() const;
```

Returns the stored value as `T`. Throws `std::runtime_error` if `T` does not match the stored type exactly.

```cpp
template<typename T>
[[nodiscard]] bool try_get(T& out) const noexcept;
```

Non-throwing variant. Returns `false` and leaves `out` unchanged if the type does not match.

```cpp
template<typename T>
[[nodiscard]] T get_loose() const noexcept;
```

Returns the stored value converted to `T` regardless of the stored type, using `static_cast`. Use when you need the value as a specific type for display or comparison and do not care about the original type.

```cpp
[[nodiscard]] std::string to_string() const noexcept;
```

Formats the stored value as a string using full precision for floating-point types.

---

## Comparison

```cpp
bool operator==(const score&) const;
auto operator<=>(const score&) const;
```

Full ordering. Comparison is done by converting both operands to `long double`, so values of different types compare naturally:

```cpp
gempba::score::make(10) < gempba::score::make(20.5)   // true
gempba::score::make(3)  == gempba::score::make(3.0f)  // true
```
