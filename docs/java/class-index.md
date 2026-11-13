# Class Index

All public types in the `io.gempba` packages, grouped by role. Links go to the source on GitHub. Types marked **`gempba-mpi` only** ship only in the `gempba-mpi` artifact.

<table class="class-index">
  <thead>
    <tr><th>Class</th><th>Description</th></tr>
  </thead>
  <tbody>

    <!-- ── Entry point ────────────────────────────── -->
    <tr class="category"><td colspan="2">Entry point (<code>io.gempba</code>)</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/GemPBA.java"><code>GemPBA</code></a></td>
      <td>Static factories and entry points: <code>createLoadBalancer</code>, <code>createNodeManager</code>, <code>createSeedNode</code>, node creation, telemetry switches, stopping a run (<code>requestStop</code>, <code>isStopRequested</code>, <code>stopOnSignals</code>), <code>shutdown</code>. The same class in both artifacts, mirroring the C++ <code>gempba::</code> namespace</td>
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

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/RunOutcome.java"><code>RunOutcome</code></a></td>
      <td>How a run ended, as <code>Scheduler.run</code> returns it: <code>reason()</code>, <code>trigger()</code>, <code>signal()</code> and <code>isInterrupted()</code>, mirroring <code>gempba::run_outcome</code></td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/EndReason.java"><code>EndReason</code></a></td>
      <td>Whether a run completed or was interrupted (<code>COMPLETED</code> / <code>INTERRUPTED</code>), mirroring <code>gempba::end_reason</code></td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/StopTrigger.java"><code>StopTrigger</code></a></td>
      <td>What stopped a run (<code>NONE</code>, <code>CODE</code>, <code>SIGNAL</code>, <code>CONTROL</code>), mirroring <code>gempba::stop_trigger</code></td>
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
      <td>Task whose arguments are captured in the Java lambda closure; no serialization involved</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/ResultClosureTask.java"><code>ResultClosureTask&lt;R&gt;</code></a></td>
      <td>Closure task that returns a typed result, paired with a <code>Serializer</code> for retrieval via <code>Node.getResult()</code></td>
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

    <!-- ── Scheduling ─────────────────────────────── -->
    <tr class="category"><td colspan="2">Scheduling (<code>io.gempba.scheduler</code>)</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/scheduler/Scheduler.java"><code>Scheduler</code></a></td>
      <td>Handle to a C++ <code>gempba::scheduler</code>: <code>run</code>, <code>rankMe</code>, <code>worldSize</code>, <code>isRoot</code>, <code>barrier</code>, statistics and results. The built-in MPI ones come from <code>Mpi.createScheduler</code></td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/scheduler/SerialRunnable.java"><code>SerialRunnable</code></a></td>
      <td>Serializable task passed to <code>Scheduler.run</code> by integer ID; a rank that receives a task looks it up, deserialises the bytes and runs it</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/scheduler/SerialTask.java"><code>SerialTask</code></a></td>
      <td>Task body for a <code>SerialRunnable</code>; typically creates child nodes from deserialised arguments</td>
    </tr>

    <!-- ── MPI component ──────────────────────────── -->
    <tr class="category"><td colspan="2">MPI component, <code>gempba-mpi</code> only (<code>io.gempba.mpi</code>)</td></tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-mpi/io/gempba/mpi/Mpi.java"><code>Mpi</code></a></td>
      <td>The MPI component's calls, mirroring C++ <code>gempba::mpi</code>: <code>createScheduler(SchedulerTopology)</code></td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-mpi/io/gempba/mpi/SchedulerTopology.java"><code>SchedulerTopology</code></a></td>
      <td>MPI topology selection (<code>SEMI_CENTRALIZED</code> / <code>CENTRALIZED</code>), mirroring <code>gempba::mpi::scheduler_topology</code></td>
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
      <td>Extracts the right <code>natives/&lt;os&gt;-&lt;arch&gt;/</code> binary from the JAR and loads it at runtime</td>
    </tr>

    <tr>
      <td><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/internal/StopSignals.java"><code>StopSignals</code></a></td>
      <td>Lets <code>SIGINT</code> and <code>SIGTERM</code> stop a run gracefully inside a JVM, which handles both signals itself</td>
    </tr>

  </tbody>
</table>
