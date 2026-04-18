# `result`

```cpp
#include <gempba/utils/result.hpp>  // included automatically via gempba.hpp
```

`result` pairs a [`score`](score.md) with a [`task_packet`](task-packet.md). It represents a candidate solution found during the search: the quality of the solution and its serialized form ready for retrieval or transmission.

`node_manager` stores the best `result` seen so far and returns it after the run completes. In multiprocessing mode, the worker that found the best solution reports it to the center as a `result`; the center selects the overall best when collecting final answers.

---

## Constructor

```cpp
result(const score& score, task_packet task_packet);
```

Construct from a quality value and its associated serialized solution.

---

## Accessors

```cpp
[[nodiscard]] score get_score() const;
```

Returns the quality value of this solution.

```cpp
[[nodiscard]] task_packet get_task_packet() const;
```

Returns the serialized form of the solution.

```cpp
[[nodiscard]] int get_score_as_integer() const;
```

Convenience wrapper around `score::get_loose<int>()`. Useful for quick comparisons when the score type is known to be integral.

---

## Sentinels and comparison

```cpp
static const result EMPTY;
```

Represents the absence of a solution. Has a score of -1 and an empty `task_packet`. Used as the initial value before any solution is found.

```cpp
bool operator==(const result&) const;
bool operator!=(const result&) const;
```

Compare both `score` and `task_packet`.
