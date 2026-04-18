# Class Index

All public types in the `gempba` namespace, grouped by role. <span class="abstract-badge">abstract</span> marks
pure-virtual interfaces.

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
      <td><a href="../interfaces/scheduler/"><code>scheduler</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Process-level IPC coordination — transport-agnostic contract</td>
    </tr>
    <tr class="nested">
      <td><a href="../interfaces/scheduler/#schedulercenter"><code>scheduler::center</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Seeds the initial task and coordinates workers (rank 0)</td>
    </tr>
    <tr class="nested">
      <td><a href="../interfaces/scheduler/#schedulerworker"><code>scheduler::worker</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Explores the search tree and exchanges tasks with other processes (non-zero ranks)</td>
    </tr>

    <tr>
      <td><a href="../interfaces/serial-runnable/"><code>serial_runnable</code></a>
        <span class="abstract-badge">abstract</span></td>
      <td>Type erasure for functions that cross process boundaries</td>
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

    <!-- ── Built-in implementations ─────────────── -->
    <tr class="category"><td colspan="2">Built-in implementations</td></tr>

    <tr>
      <td><a href="../implementations/stats/default-mpi-stats/"><code>default_mpi_stats</code></a></td>
      <td>Built-in <code>stats</code> implementation for the MPI schedulers</td>
    </tr>

    <tr>
      <td><a href="../implementations/stats-visitors/default-mpi-stats-visitor/"><code>default_mpi_stats_visitor</code></a></td>
      <td>Built-in <code>stats_visitor</code> — typed field access for MPI stats</td>
    </tr>

    <tr>
      <td><a href="../implementations/load-balancers/quasi-horizontal/"><code>quasi_horizontal_load_balancer</code></a></td>
      <td>Distributes work near the root first; recommended for unbalanced trees</td>
    </tr>

    <tr>
      <td><a href="../implementations/load-balancers/work-stealing/"><code>work_stealing_load_balancer</code></a></td>
      <td>Naive FIFO thread scheduler — baseline / benchmarking only</td>
    </tr>

    <tr>
      <td><a href="../implementations/schedulers/semi-centralized/"><code>mpi_semi_centralized_scheduler</code></a></td>
      <td>Tasks travel point-to-point between workers; recommended for production</td>
    </tr>

    <tr>
      <td><a href="../implementations/schedulers/centralized/"><code>mpi_centralized_scheduler</code></a></td>
      <td>All tasks route through the center — benchmarking only</td>
    </tr>

    <!-- ── Utilities ──────────────────────────────── -->
    <tr class="category"><td colspan="2">Utilities</td></tr>

    <tr>
      <td><a href="../utilities/queue/"><code>Queue&lt;T&gt;</code></a></td>
      <td>Thread-safe FIFO queue used internally by load balancers</td>
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
      <td><a href="../utilities/tree/"><code>tree</code></a></td>
      <td>Index-based flat tree used for scheduler startup topology</td>
    </tr>

  </tbody>
</table>
