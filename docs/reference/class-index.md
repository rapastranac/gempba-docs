# Class Index

All public types, grouped by role. They live in the `gempba` namespace, except `tree`, which is global.
<span class="abstract-badge">abstract</span> marks pure-virtual interfaces, and <span class="abstract-badge">private</span>
marks built-in implementations you reach through a factory rather than by including them.

<table class="class-index">
  <thead>
    <tr><th>Class</th><th>Description</th></tr>
  </thead>
  <tbody>

    <!-- ── Interfaces ─────────────────────────────── -->
    <tr class="category"><td colspan="2">Interfaces</td></tr>

    <tr>
      <td><a href="../interfaces/load-balancer/"><code>load_balancer</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Thread-level work distribution within a single process</td>
    </tr>

    <tr>
      <td><a href="../interfaces/node-core/"><code>node_core</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Base class for node implementations; handle type is <code>shared_ptr&lt;node_core&gt;</code></td>
    </tr>

    <tr>
      <td><a href="../interfaces/node-traits/"><code>node_traits&lt;T&gt;</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Full interface contract every node must satisfy; <code>T</code> is the handle type used for tree navigation</td>
    </tr>

    <tr>
      <td><a href="../interfaces/scheduler/#scheduler_traits-shared-base"><code>scheduler_traits</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Base of <code>scheduler</code>: barrier, rank, world size and this rank's stats</td>
    </tr>

    <tr>
      <td><a href="../interfaces/scheduler/"><code>scheduler</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Process-level coordination over MPI; every rank calls its <code>run</code>, and the root (rank 0) seeds the run and reads its results</td>
    </tr>

    <tr>
      <td><a href="../interfaces/serial-runnable/"><code>serial_runnable</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Type erasure for functions that cross process boundaries</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/core/serializable.hpp"><code>serializable</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Contract for objects that round-trip through a <code>task_packet</code>: <code>serialize()</code> / <code>deserialize()</code></td>
    </tr>

    <tr>
      <td><a href="../interfaces/stats/"><code>stats</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Runtime metrics collection for a single process</td>
    </tr>

    <tr>
      <td><a href="../interfaces/stats-visitor/"><code>stats_visitor</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Format-agnostic readout of collected metrics</td>
    </tr>

    <!-- ── Concrete types ────────────────────────── -->
    <tr class="category"><td colspan="2">Concrete types</td></tr>

    <tr>
      <td><a href="../defaults/node/"><code>node</code></a></td>
      <td>User-facing node handle — wraps <code>shared_ptr&lt;node_core&gt;</code>, cheap to copy</td>
    </tr>

    <tr>
      <td><a href="../defaults/node-manager/"><code>node_manager</code></a></td>
      <td>Control panel — load balancer facade, thread pool config, result tracking</td>
    </tr>

    <!-- ── Enums and outcomes ──────────────────────── -->
    <tr class="category"><td colspan="2">Enums and outcomes</td></tr>

    <tr>
      <td><a href="../../stopping-a-run/#in-code"><code>run_outcome</code></a></td>
      <td>How a run ended, as <code>scheduler::run</code> returns it: <code>m_reason</code>, <code>m_trigger</code>, <code>m_signal</code></td>
    </tr>

    <tr>
      <td><a href="../../stopping-a-run/#in-code"><code>end_reason</code></a></td>
      <td><code>COMPLETED</code> (the result is proven) or <code>INTERRUPTED</code> (the best found before a stop)</td>
    </tr>

    <tr>
      <td><a href="../../stopping-a-run/#in-code"><code>stop_trigger</code></a></td>
      <td>What stopped a run: <code>NONE</code>, <code>CODE</code>, <code>SIGNAL</code> or <code>CONTROL</code></td>
    </tr>

    <tr>
      <td><a href="../interfaces/scheduler/"><code>rank_role</code></a></td>
      <td>A rank's role in a scheduler: <code>COORDINATOR</code> or <code>WORKER</code></td>
    </tr>

    <tr>
      <td><a href="../interfaces/scheduler/#factory"><code>mpi::scheduler_topology</code></a></td>
      <td>The built-in MPI schedulers: <code>SEMI_CENTRALIZED</code> or <code>CENTRALIZED</code></td>
    </tr>

    <tr>
      <td><a href="../defaults/node-manager/"><code>goal</code></a></td>
      <td><code>MAXIMISE</code> or <code>MINIMISE</code></td>
    </tr>

    <tr>
      <td><a href="../interfaces/load-balancer/#related-types"><code>balancing_policy</code></a></td>
      <td><code>QUASI_HORIZONTAL</code> or <code>WORK_STEALING</code></td>
    </tr>

    <tr>
      <td><a href="../defaults/node-manager/"><code>score_type</code></a></td>
      <td>The numeric type behind a <code>score</code>: <code>I32</code>, <code>I64</code>, <code>F32</code>, <code>F64</code>, <code>F128</code> (and <code>U_I32</code>, <code>U_I64</code>)</td>
    </tr>

    <tr>
      <td><a href="../interfaces/node-traits/#member-types"><code>node_state</code></a></td>
      <td>Where a node is in its life: <code>UNUSED</code>, <code>FORWARDED</code>, <code>PUSHED</code>, <code>DISCARDED</code>, <code>RETRIEVED</code>, <code>SENT_TO_ANOTHER_PROCESS</code>, <code>RUNNING</code></td>
    </tr>

    <!-- ── Built-in implementations ─────────────── -->
    <tr class="category"><td colspan="2">Built-in implementations</td></tr>

    <tr>
      <td><a href="../implementations/stats/default-mpi-stats/"><code>default_mpi_stats</code></a> <span class="abstract-badge">private</span></td>
      <td>Built-in <code>stats</code> implementation for the MPI schedulers</td>
    </tr>

    <tr>
      <td><a href="../implementations/stats-visitors/default-mpi-stats-visitor/"><code>default_mpi_stats_visitor</code></a></td>
      <td>Built-in <code>stats_visitor</code> — typed field access for MPI stats</td>
    </tr>

    <tr>
      <td><a href="../implementations/load-balancers/quasi-horizontal/"><code>quasi_horizontal_load_balancer</code></a> <span class="abstract-badge">private</span></td>
      <td>Distributes work near the root first; recommended for unbalanced trees</td>
    </tr>

    <tr>
      <td><a href="../implementations/load-balancers/work-stealing/"><code>work_stealing_load_balancer</code></a> <span class="abstract-badge">private</span></td>
      <td>Naive FIFO thread scheduler — baseline / benchmarking only</td>
    </tr>

    <tr>
      <td><a href="../implementations/schedulers/semi-centralized/"><code>mpi_semi_centralized_scheduler</code></a> <span class="abstract-badge">private</span></td>
      <td>Tasks travel point-to-point between workers; recommended for production</td>
    </tr>

    <tr>
      <td><a href="../implementations/schedulers/centralized/"><code>mpi_centralized_scheduler</code></a> <span class="abstract-badge">private</span></td>
      <td>All tasks route through the coordinator — benchmarking only</td>
    </tr>

    <!-- ── Telemetry ──────────────────────────────── -->
    <tr class="category"><td colspan="2">Telemetry (see the <a href="../../telemetry/">Telemetry section</a>)</td></tr>

    <tr>
      <td><a href="../../telemetry/"><code>telemetry::telemetry_hub</code></a></td>
      <td>Process-wide telemetry hub: counters, probes, transport, and the dashboard server (the aggregator, rank 0)</td>
    </tr>

    <tr>
      <td><a href="../../telemetry/data-model/"><code>telemetry::rank_frame</code>, <code>node_frame</code>, <code>topology_snapshot</code></a></td>
      <td>The frame structs behind the live stream: per-rank counters, per-host stats, and the startup topology</td>
    </tr>

    <!-- ── C ABI ──────────────────────────────────── -->
    <tr class="category"><td colspan="2">C ABI</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/cabi/gempba.h"><code>gempba/cabi/gempba.h</code></a></td>
      <td>The <code>extern "C"</code> surface over the core: opaque handles, status codes, callbacks. The <a href="../../java/how-it-works/">Java binding</a> is its first consumer</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/cabi/gempba_mpi.h"><code>gempba/cabi/gempba_mpi.h</code></a></td>
      <td>The MPI component's C calls: <code>gempba_mpi_create_scheduler</code> and <code>gempba_scheduler_topology_t</code></td>
    </tr>

    <!-- ── Utilities ──────────────────────────────── -->
    <tr class="category"><td colspan="2">Utilities</td></tr>

    <tr>
      <td><a href="../utilities/queue/"><code>queue&lt;T&gt;</code></a></td>
      <td>Thread-safe FIFO queue the MPI schedulers use for outgoing tasks</td>
    </tr>

    <tr>
      <td><a href="../utilities/result/"><code>result</code></a></td>
      <td>Found solution: best <code>score</code> plus serialized data as <code>task_packet</code></td>
    </tr>

    <tr>
      <td><a href="../utilities/score/"><code>score</code></a></td>
      <td>17-byte type-erased numeric value for optimization goals; trivially copyable</td>
    </tr>

    <tr>
      <td><a href="../utilities/task-bundle/"><code>task_bundle</code></a></td>
      <td>IPC unit — <code>task_packet</code> plus integer routing ID</td>
    </tr>

    <tr>
      <td><a href="../utilities/task-packet/"><code>task_packet</code></a></td>
      <td>Byte buffer (<code>vector&lt;byte&gt;</code>) for serialized arguments and results</td>
    </tr>

    <tr>
      <td><a href="../utilities/transmission-guard/"><code>transmission_guard</code></a></td>
      <td>RAII lock for the outgoing IPC channel; released on destruction</td>
    </tr>

    <tr>
      <td><a href="../utilities/tree/"><code>tree</code></a> (global namespace)</td>
      <td>Index-based flat tree used for scheduler startup topology</td>
    </tr>

  </tbody>
</table>
