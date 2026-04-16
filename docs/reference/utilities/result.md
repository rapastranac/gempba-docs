# `result`

```cpp
#include <gempba/utils/result.hpp>  // included automatically via gempba.hpp
```

`result` pairs a [`score`](score.md) with a [`task_packet`](task-packet.md). It represents a candidate solution found during the search: the quality of the solution (`score`) and its serialized form (`task_packet`) ready for retrieval or transmission.

`node_manager` stores the best `result` seen so far and returns it after the run completes. In multiprocessing mode, the worker that found the best solution reports it to the center as a `result`; the center selects the overall best when collecting final answers.

## Construction

```cpp
result(const score& score, task_packet task_packet);
```

## Accessors

```cpp
[[nodiscard]] score       get_score()          const;
[[nodiscard]] task_packet get_task_packet()    const;
[[nodiscard]] int         get_score_as_integer() const;  // convenience: get_loose<int>()
```

## Sentinels and comparison

```cpp
static const result EMPTY;  // score -1, empty task_packet
```

`==` and `!=` compare both `score` and `task_packet`.
