# `stats`

```cpp
#include <gempba/stats/stats.hpp>  // included automatically via gempba.hpp
```

`stats` is the abstract interface for a single process's runtime metrics. It accumulates measurements during a run and exposes them through two visit overloads: a generic lambda-based one and a typed [`stats_visitor`](stats-visitor.md) one.

You do not construct `stats` objects directly. The scheduler owns one per process and returns them after the run. The center process can also collect stats from all workers via `scheduler::get_stats_vector()`.

## Contract

### Serialization

```cpp
[[nodiscard]] virtual task_packet serialize() const = 0;
```

Serializes the stats object into bytes for inter-process transfer. Called internally when the center gathers stats from all workers via `synchronize_stats()`.

### Labels

```cpp
[[nodiscard]] virtual std::vector<std::string> labels() const = 0;
```

Returns the names of all tracked fields in declaration order. Use this to enumerate available metrics without knowing the concrete type:

```cpp
for (const auto& label : stats_ptr->labels()) {
    std::cout << label << "\n";
}
// e.g.: received_task_count, sent_task_count, idle_time, elapsed_time, ...
```

### Visiting

```cpp
virtual void visit(std::function<void(const std::string&, std::any&&)> visitor) const = 0;
```

Calls `visitor` once per field, passing the field name and its value as `std::any`. The concrete stats type determines the actual type stored in each `any`. Use `std::any_cast<T>` to retrieve values:

```cpp
stats_ptr->visit([](const std::string& key, std::any&& value) {
    if (key == "idle_time")
        std::cout << "idle: " << std::any_cast<double>(value) << " ms\n";
    if (key == "received_task_count")
        std::cout << "received: " << std::any_cast<std::size_t>(value) << "\n";
});
```

```cpp
virtual void visit(stats_visitor* visitor) const = 0;
```

Dispatches to a typed [`stats_visitor`](stats-visitor.md). Prefer this over the lambda overload when you need a reusable, named readout object. The built-in implementation is [`default_mpi_stats_visitor`](../implementations/stats-visitors/default-mpi-stats-visitor.md).

## Custom implementation

Implement `stats` when writing a custom scheduler that tracks different or additional metrics:

```cpp
class MyStats : public gempba::stats {
public:
    std::size_t my_counter{};
    double      my_duration{};

    task_packet serialize() const override {
        // encode my_counter and my_duration into bytes
    }

    std::vector<std::string> labels() const override {
        return {"my_counter", "my_duration"};
    }

    void visit(std::function<void(const std::string&, std::any&&)> v) const override {
        v("my_counter", my_counter);
        v("my_duration", my_duration);
    }

    void visit(gempba::stats_visitor* v) const override {
        v->visit(*this);
    }
};
```

The string keys passed to the lambda visitor must be stable — they are the same strings a `stats_visitor` implementation uses to identify fields by name.
