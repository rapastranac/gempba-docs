# Stopping a Run

A run usually ends when the search space is exhausted. From gempba v5.0.0 you can also stop it early and keep the best result found so far, and the run says how it ended.

## How a run ends

A run ends in one of three ways:

| End | What happened | The result |
|---|---|---|
| **Completed** | The whole search space was explored. | Proven. |
| **Interrupted** | A stop ended the run early. The stop came from a **signal** (`SIGINT` or `SIGTERM`), from **the stop call** in your code, or from **the dashboard**. | The best one found before the stop, not a proven one. |
| **Lost** | The run was killed without warning: `SIGKILL`, a crash or a node failure. | None: the program dies before returning one. |

A completed or interrupted run says how it ended, as [Reading how it ended](#reading-how-it-ended) shows. A lost run can't, and that silence is what tells you it was lost.

## What a stop does

- From the stop on, nodes that haven't started are pruned. Nodes already running finish their own work, and the run then returns its best result so far.
- Under MPI, every rank stops, even ranks that saw no signal. A worker that sees the stop tells the root, and the root tells every worker. Every rank returns the same outcome.
- The first stop wins, whatever triggered it, until `gempba::shutdown()`. Later stops change nothing.
- A stop doesn't cut a node short. If one node runs for a long time, poll `gempba::stop_requested()` (Java: `GemPBA.isStopRequested()`) inside it and return early once it's `true`.

## Stopping it

### With a signal

Signals stop the run gracefully **by default**. `create_node_manager` takes `SIGINT` and `SIGTERM`, and `shutdown` gives them back:

- **Ctrl+C** (`SIGINT`) once stops the run gracefully. A second Ctrl+C kills the process, in case the wind-down takes too long. In Java, the second one goes to the JVM's own handler, which shuts the JVM down as usual.
- **`SIGTERM`** stops the run gracefully, and further `SIGTERM`s don't kill it. This is the signal a batch scheduler sends, so a job that hits its time limit ends interrupted rather than lost; see [On a Slurm cluster](#on-a-slurm-cluster).
- In C++, gempba takes only a signal that nothing handles yet. If your program installed its own handler first, gempba leaves the signal to it, and that signal won't stop the run gracefully.

To keep the signals' default behavior, which kills the process, turn this off. Call it before `create_node_manager` to keep gempba from taking them, or later to give them back at once:

```cpp
gempba::stop_on_signals(false);
```

```java
GemPBA.stopOnSignals(false);
```

### From your code

Call the stop from any thread, for example from a watchdog that enforces a time budget. It returns at once:

```cpp
#include <gempba/gempba.hpp>

gempba::request_stop();                 // stop the run, from any thread

if (gempba::stop_requested()) {         // inside a long node: return early
    return;
}
```

```java
import io.gempba.GemPBA;

GemPBA.requestStop();                   // stop the run, from any thread

if (GemPBA.isStopRequested()) {         // inside a long node: return early
    return;
}
```

`stop_requested()` stays `true` from the first stop, by any trigger, until `shutdown()`.

### From the dashboard

A telemetry client can stop the run with the `stop` control line on the dashboard socket; the [GemPBA Dashboard](telemetry/dashboard.md)'s **Stop the run** sends it. Because any user on the host can reach that socket, the line carries a token, and the run stops only when the token matches the `GEMPBA_STOP_TOKEN` environment variable the run was started with:

```bash
export GEMPBA_STOP_TOKEN=pick-your-own   # set before starting the program
```

```json
{"kind":"stop","token":"pick-your-own"}
```

A run started without `GEMPBA_STOP_TOKEN` refuses every stop line, and a stop line with another token is refused too. Each refusal logs a warning:

```text
telemetry: refused a stop line: this run has no GEMPBA_STOP_TOKEN
telemetry: refused a stop line with the wrong token
```

The example repositories' cluster jobs export `GEMPBA_STOP_TOKEN=${GEMPBA_STOP_TOKEN:-s3cret}`, so their runs take the dashboard's stop out of the box. The token you set in your own environment overrides that default.

## Reading how it ended

### In code

Under MPI, `scheduler::run` returns how the run ended, the same on every rank:

```cpp
const gempba::run_outcome outcome = scheduler->run(nm, runnables, std::move(seed));

if (outcome.m_reason == gempba::end_reason::INTERRUPTED) {
    // the result is the best one found before the stop, not a proven one
}
```

| Field | Values |
|---|---|
| `m_reason` | `end_reason::COMPLETED` or `end_reason::INTERRUPTED` |
| `m_trigger` | `stop_trigger::NONE` for a completed run; otherwise `CODE` (`request_stop()`), `SIGNAL` (`SIGINT` or `SIGTERM`) or `CONTROL` (a stop line) |
| `m_signal` | The signal's number when `m_trigger` is `SIGNAL`; `0` otherwise |

In Java, `Scheduler.run` returns the same thing as an `io.gempba.value.RunOutcome` record, with `reason()` (`EndReason`), `trigger()` (`StopTrigger`), `signal()` and `isInterrupted()`:

```java
RunOutcome outcome = sched.run(nm, runnables, seed, seedRunnableId);

if (outcome.isInterrupted()) {
    // the result is the best one found before the stop, not a proven one
}
```

A multithreading run has no scheduler, so nothing returns an outcome. Check `gempba::stop_requested()` (Java: `GemPBA.isStopRequested()`) after the wait and before `shutdown()`: `true` means a stop cut the run short.

### In the log

gempba logs one line when the run ends: under MPI the root rank logs it when `scheduler::run` returns, and a multithreading run logs it at `shutdown()`. A completed run logs at `info`:

```text
gempba: run completed: the whole search space was explored, so the result is proven
```

An interrupted run logs a warning that names what stopped it:

```text
gempba: run interrupted by SIGTERM: the result is the best one found before the stop, not a proven one
```

| Stopped by | The warning says |
|---|---|
| Ctrl+C | `run interrupted by SIGINT (Ctrl+C)` |
| `SIGTERM` | `run interrupted by SIGTERM` |
| The stop call | `run interrupted by gempba::request_stop()`, from Java's `GemPBA.requestStop()` too |
| The dashboard | `run interrupted from the dashboard`, after `telemetry: a dashboard client stopped the run` |

### On the telemetry stream

At shutdown the aggregator sends a final line, marked `"final":true`, then closes the connection. That line says how the run ended in `end`:

```json
"end":{"reason":"interrupted","trigger":"signal","signal":"SIGTERM"}
```

- `reason` is `"completed"` or `"interrupted"`.
- An interrupted run adds `trigger`: `"code"`, `"signal"` or `"control"`.
- A stop by signal adds `signal`, its name, such as `"SIGINT"` or `"SIGTERM"`.

A multithreading run has no scheduler, so its `end` comes from whether a stop was requested: `"completed"`, or `"interrupted"` with the stop's trigger. Under MPI, `end` is absent when the scheduler didn't report how the run ended, for example when it threw. A connection that closes **without** a final line was lost. The full field reference is in gempba's [`wire-format.md`](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/wire-format.md); [Data model](telemetry/data-model.md) maps it.

## On a Slurm cluster

When a job reaches its time limit, Slurm sends `SIGTERM` to the job's processes, then `SIGKILL` once the cluster's `KillWait` has passed, often 30 seconds. gempba takes that `SIGTERM` as a stop, but the run has only those seconds to wind down. If its running nodes take longer, the job is killed and the run is lost.

Ask Slurm to send `SIGTERM` earlier with `--signal`, giving the run time to end interrupted, with its best result, its log line and its final telemetry line:

```bash
#SBATCH --signal=TERM@<seconds>   # SIGTERM <seconds> before the time limit
```

- Choose `<seconds>` longer than your longest node takes to finish. Slurm may send the signal up to 60 seconds earlier than asked.
- Launch the program with `srun`, as the examples do, so the signal reaches every rank. Leave out the `B:` prefix: `--signal=B:TERM@…` signals only the batch script's shell, not the program.

To stop a running job gracefully by hand, send it `SIGTERM` alone instead of cancelling it outright:

```bash
scancel --signal=TERM <jobid>
```

## Writing your own scheduler

A custom scheduler takes part in the stop too: it polls `gempba::stop_requested()`, tells the other ranks, and returns the same `run_outcome` from `do_run` on every rank. gempba's [`custom-schedulers.md`](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/custom-schedulers.md#stopping-early) lists what it must do.
