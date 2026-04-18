# `stats_visitor`

```cpp
#include <gempba/stats/stats_visitor.hpp>  // included automatically via gempba.hpp
```

Abstract interface for reading out metrics from a [`stats`](stats.md) object. Decouples collection (what is measured) from presentation (how it is reported).

---

## Member functions

```cpp
virtual void visit(const stats&) = 0;
```
Called by `stats::visit(stats_visitor*)`. Map field names from the stats object to member variables or output targets of your choosing.

---

## Custom implementation

```cpp
class MyStatsVisitor : public gempba::stats_visitor {
public:
    std::size_t task_count{};
    double      idle_ms{};

    void visit(const gempba::stats& s) override {
        s.visit([this](const std::string& key, std::any&& value) {
            if (key == "received_task_count")
                task_count = std::any_cast<std::size_t>(value);
            else if (key == "idle_time")
                idle_ms = std::any_cast<double>(value);
        });
    }
};

MyStatsVisitor v;
stats_ptr->visit(&v);
```

Available field names depend on the concrete `stats` implementation. For the built-in MPI stats, see [`default_mpi_stats_visitor`](../implementations/stats-visitors/default-mpi-stats-visitor.md).
