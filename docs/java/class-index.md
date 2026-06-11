# Class Index

All public types in the `io.gempba` packages, grouped by role. Links go to the source on GitHub. Types marked **MP only** ship only in the `mp-mpi` classifier.

<table class="class-index">
  <thead>
    <tr><th>Class</th><th>Description</th></tr>
  </thead>
  <tbody>

    <!-- ── Entry point ────────────────────────────── -->
    <tr class="category"><td colspan="2">Entry point</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-multithreading/io/gempba/GemPBA.java"><code>GemPBA</code></a></td>
      <td>Static factories and entry points: <code>createLoadBalancer</code>, <code>createNodeManager</code>, <code>createSeedNode</code>, node creation, telemetry switches, <code>shutdown</code>. Each flavor ships its own variant of this class (<a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-multiprocessing/io/gempba/GemPBA.java">MP variant</a>), mirroring the C++ inline-namespace selection</td>
    </tr>

    <!-- ── Core handles ───────────────────────────── -->
    <tr class="category"><td colspan="2">Core handles (<code>io.gempba.core</code>)</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/core/LoadBalancer.java"><code>LoadBalancer</code></a></td>
      <td>Handle to a C++ <code>gempba::load_balancer</code>; created through <code>GemPBA.createLoadBalancer</code></td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/core/NodeManager.java"><code>NodeManager</code></a></td>
      <td>Handle to a C++ <code>gempba::node_manager</code>: goal and pool configuration, node submission, result tracking</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/core/Node.java"><code>Node</code></a></td>
      <td>One node in the search tree, mirroring <code>gempba::node</code>: submission handle and parent reference; type knowledge lives in the factory closures</td>
    </tr>

    <!-- ── Values ─────────────────────────────────── -->
    <tr class="category"><td colspan="2">Values (<code>io.gempba.value</code>)</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/Score.java"><code>Score</code></a></td>
      <td>Typed numeric score tracking the best result; built with <code>Score.make(...)</code></td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/ScoreType.java"><code>ScoreType</code></a></td>
      <td>Numeric representation for a <code>Score</code>, mirroring <code>gempba::score_type</code> (<code>I32</code>, <code>I64</code>, <code>F32</code>, <code>F64</code>)</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/Goal.java"><code>Goal</code></a></td>
      <td>Optimisation direction (<code>MAXIMISE</code> / <code>MINIMISE</code>), mirroring <code>gempba::goal</code></td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/BalancingPolicy.java"><code>BalancingPolicy</code></a></td>
      <td>Load-balancing strategy (<code>QUASI_HORIZONTAL</code> / <code>WORK_STEALING</code>), mirroring <code>gempba::balancing_policy</code></td>
    </tr>

    <!-- ── Task interfaces ────────────────────────── -->
    <tr class="category"><td colspan="2">Task functional interfaces (<code>io.gempba.task</code>)</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/NodeTask.java"><code>NodeTask&lt;Args,&nbsp;R&gt;</code></a></td>
      <td>User-supplied branch-and-bound task: <code>(threadId, args, node)</code> with a typed argument bundle and result</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/VoidNodeTask.java"><code>VoidNodeTask&lt;Args&gt;</code></a></td>
      <td>Convenience specialisation of <code>NodeTask</code> for void-returning tasks</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/ClosureTask.java"><code>ClosureTask</code></a></td>
      <td>MT-mode task whose arguments are captured in the Java lambda closure; no serialization involved</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/ResultClosureTask.java"><code>ResultClosureTask&lt;R&gt;</code></a></td>
      <td>MT-mode closure task that returns a typed result, paired with a <code>Serializer</code> for retrieval via <code>Node.getResult()</code></td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/Serializer.java"><code>Serializer&lt;A&gt;</code></a></td>
      <td>Converts a value to bytes for transport into the C++ <code>task_packet</code></td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/Deserializer.java"><code>Deserializer&lt;A&gt;</code></a></td>
      <td>Reconstructs a value from bytes received from the C++ <code>task_packet</code></td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/LazyArgsSupplier.java"><code>LazyArgsSupplier</code></a></td>
      <td>Argument initialiser for lazy nodes: return serialised bytes to run, or <code>null</code> to prune</td>
    </tr>

    <!-- ── Multiprocessing ────────────────────────── -->
    <tr class="category"><td colspan="2">Scheduling, MP only (<code>io.gempba.scheduler</code>)</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-multiprocessing/io/gempba/scheduler/Scheduler.java"><code>Scheduler</code></a></td>
      <td>Handle to a C++ <code>gempba::scheduler</code>; obtained from <code>GemPBA.createScheduler</code></td>
    </tr>
    <tr class="nested">
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-multiprocessing/io/gempba/scheduler/Scheduler.java"><code>Scheduler.Center</code></a></td>
      <td>Center-role view (rank 0): seeds the initial task and coordinates workers</td>
    </tr>
    <tr class="nested">
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-multiprocessing/io/gempba/scheduler/Scheduler.java"><code>Scheduler.Worker</code></a></td>
      <td>Worker-role view (non-zero ranks): runs the search and exchanges tasks</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-multiprocessing/io/gempba/scheduler/SchedulerTopology.java"><code>SchedulerTopology</code></a></td>
      <td>MPI topology selection (<code>SEMI_CENTRALIZED</code> / <code>CENTRALIZED</code>)</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-multiprocessing/io/gempba/scheduler/SerialRunnable.java"><code>SerialRunnable</code></a></td>
      <td>Serializable task registered on a <code>Scheduler.Worker</code> by integer ID for cross-rank dispatch</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-multiprocessing/io/gempba/scheduler/SerialTask.java"><code>SerialTask</code></a></td>
      <td>Task body for a <code>SerialRunnable</code>; typically creates child nodes from deserialised arguments</td>
    </tr>

    <!-- ── Stats ──────────────────────────────────── -->
    <tr class="category"><td colspan="2">Statistics (<code>io.gempba.stats</code>)</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/stats/RankStats.java"><code>RankStats</code></a></td>
      <td>Statistics for one MPI rank, collected after <code>Scheduler.synchronizeStats()</code></td>
    </tr>

    <!-- ── Internal ───────────────────────────────── -->
    <tr class="category"><td colspan="2">Internal (<code>io.gempba.internal</code>, not user-facing)</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/internal/GemPBANative.java"><code>GemPBANative</code></a></td>
      <td>The <code>native</code> method declarations behind every handle; loads the bundled library on first use</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/internal/NativeLoader.java"><code>NativeLoader</code></a></td>
      <td>Extracts the right <code>natives/&lt;os&gt;-&lt;arch&gt;/</code> binary from the fat JAR and loads it at runtime</td>
    </tr>

  </tbody>
</table>
