# `stats_visitor`

```cpp
#include <gempba/stats/stats_visitor.hpp>  // included automatically via gempba.hpp
```

`stats_visitor` is the abstract interface for reading out metrics from a [`stats`](stats.md) object. It has a single pure virtual method:

```cpp
virtual void visit(const stats& stats) = 0;
```

The implementation calls `stats.visit(lambda)` internally and maps each field by key name to a member variable or output target of its choosing. This decouples collection (what is measured) from presentation (how it is reported).

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
```

Pass a pointer to your visitor to `stats::visit(stats_visitor*)`:

```cpp
MyStatsVisitor v;
stats_ptr->visit(&v);
std::cout << "tasks received: " << v.task_count << "\n";
std::cout << "idle time:      " << v.idle_ms << " ms\n";
```

The key names available depend on the concrete `stats` implementation in use. For the built-in MPI stats, see the field list in [`default_mpi_stats_visitor`](../implementations/stats-visitors/default-mpi-stats-visitor.md).
