# Work-Stealing

```cpp
auto* lb = gempba::mt::create_load_balancer(gempba::balancing_policy::WORK_STEALING);
```

Implements [`load_balancer`](../../interfaces/load-balancer.md). A deliberately simple strategy: tasks are pushed to the thread pool queue as they arrive, idle threads pick them up in order. No tree structure is inspected, no root pointer is maintained.

---

## Submission algorithm

When `try_local_submit` is called:

1. Attempts a non-blocking lock on the internal mutex.
2. Returns `false` immediately if the lock is unavailable or the pool is full.
3. Prunes the node and delegates it to a thread if `should_branch()` is true.

No root tracking. No sibling search. No root correction.

---

## Comparison with Quasi-Horizontal

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TD
    subgraph ws["Work-stealing: picks wherever available"]
        direction TB
        WR(("Root")):::rootws
        WR --> WA(" "):::nodews
        WR --> WB(" "):::nodews
        WA --> WA1(" "):::nodews
        WA --> WA2(" "):::nodews
        WA1 --> WA3(" "):::stolen
        WA1 --> WA4(" "):::stolen
        WA2 --> WA5(" "):::stolen
        WB --> WB1(" "):::stolen
        WB --> WB2(" "):::nodews
        WB2 --> WB3(" "):::stolen
        WB2 --> WB4(" "):::stolen
    end

    subgraph qh["Quasi-horizontal: pushes root-level nodes first"]
        direction TB
        QR(("Root")):::rootqh
        QR --> QA(" "):::pushed
        QR --> QB(" "):::pushed
        QA --> QA1(" "):::nodqh
        QA --> QA2(" "):::nodqh
        QA1 --> QA3(" "):::nodqh
        QA1 --> QA4(" "):::nodqh
        QA2 --> QA5(" "):::nodqh
        QB --> QB1(" "):::nodqh
        QB1 --> QB2(" "):::nodqh
        QB1 --> QB3(" "):::nodqh
    end

    classDef rootqh  fill:#b0bec5,color:#37474f,stroke:#000000
    classDef rootws  fill:#b0bec5,color:#37474f,stroke:#000000
    classDef pushed  fill:#1565c0,color:#fff,stroke:#000000
    classDef stolen  fill:#e65100,color:#fff,stroke:#000000
    classDef nodqh   fill:#eceff1,color:#546e7a,stroke:#000000
    classDef nodews  fill:#eceff1,color:#546e7a,stroke:#000000
```

**Blue (QH)** — root-level nodes pushed early; each carries a large subtree.  
**Orange (WS)** — typical steal targets near the leaves; little remaining work.

|                                     | Quasi-Horizontal | Work-Stealing |
|-------------------------------------|------------------|---------------|
| Per-thread root tracking            | <span style="color:#388e3c">Yes</span> | <span style="color:#d32f2f">No</span> |
| Root-level sibling spreading        | <span style="color:#388e3c">Yes</span> | <span style="color:#d32f2f">No</span> |
| Root correction after pruning       | <span style="color:#388e3c">Yes</span> | <span style="color:#d32f2f">No</span> |
| Overhead due to parallel requests   | <span style="color:#388e3c">Low</span> | <span style="color:#d32f2f">Very high</span> |
| CPU utilization on unbalanced trees | <span style="color:#388e3c">High</span> | <span style="color:#f57c00">High (excessive tasks)</span> |
| Use case                            | <span style="color:#388e3c">Production</span> | <span style="color:#f57c00">Benchmarking baseline</span> |

---

## When to use

Primarily as a **comparison baseline** — for reproducing the benchmarks from the original paper, or for sanity-checking whether the overhead of [Quasi-Horizontal](quasi-horizontal.md) is a net negative on a specific workload.

On uniformly balanced trees, work-stealing may perform comparably to quasi-horizontal. On the unbalanced trees characteristic of real branch-and-bound problems it loses ground: stolen tasks tend to be near the leaves, carrying little remaining work, so threads finish quickly and idle.
