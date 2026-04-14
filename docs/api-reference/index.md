# API Reference

GemPBA's public surface is intentionally small. You include one header and interact with
a handful of types.

| Header | Purpose |
|---|---|
| [`gempba.hpp`](gempba-hpp.md) | The only header you need — facade, factory functions, global accessors |
| [`node_manager.hpp`](node-manager.md) | Control panel: configure goal, submit work, wait, collect results |
| [`node.hpp`](node.md) | Handle to a branch in the recursion tree |
| [`node_core.hpp`](node-core.md) | Abstract base for custom node implementations (advanced) |
| [`node_traits.hpp`](node-traits.md) | The interface contract every node must satisfy |
| [`serial_runnable.hpp`](serial-runnable.md) | Type erasure for functions crossing process boundaries (multiprocessing) |
| [Load Balancing](load-balancing.md) | Available balancing policies |
