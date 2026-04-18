# `stats`

```cpp
#include <gempba/stats/stats.hpp>  // included automatically via gempba.hpp
```

Abstract interface for a single process's runtime metrics. The scheduler owns one instance per process and returns it after the run. Not constructed directly.

---

## Member functions

```cpp
[[nodiscard]] virtual task_packet serialize() const = 0;
```
Serialize metrics to bytes for inter-process transfer. Called internally by `synchronize_stats()`.

```cpp
[[nodiscard]] virtual std::vector<std::string> labels() const = 0;
```
Names of all tracked fields in declaration order.

```cpp
virtual void visit(std::function<void(const std::string&, std::any&&)>) const = 0;
```
Call visitor once per field with field name and value as `std::any`. Use `std::any_cast<T>` to retrieve typed values.

```cpp
virtual void visit(stats_visitor*) const = 0;
```
Dispatch to a typed [`stats_visitor`](stats-visitor.md).

---

## Usage

```cpp
// Lambda visitor
stats_ptr->visit([](const std::string& key, std::any&& value) {
    if (key == "idle_time")
        std::cout << std::any_cast<double>(value) << " ms\n";
    if (key == "received_task_count")
        std::cout << std::any_cast<std::size_t>(value) << "\n";
});

// Typed visitor
MyStatsVisitor v;
stats_ptr->visit(&v);
```

---

## Custom implementation

```cpp
class MyStats : public gempba::stats {
public:
    std::size_t my_counter{};
    double      my_duration{};

    task_packet serialize() const override { /* encode fields */ }

    std::vector<std::string> labels() const override {
        return {"my_counter", "my_duration"};
    }

    void visit(std::function<void(const std::string&, std::any&&)> v) const override {
        v("my_counter", my_counter);
        v("my_duration", my_duration);
    }

    void visit(gempba::stats_visitor* v) const override { v->visit(*this); }
};
```

Key names passed to the lambda visitor must be stable — `stats_visitor` implementations identify fields by those strings.
