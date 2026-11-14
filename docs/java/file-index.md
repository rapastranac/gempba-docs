# File Index

The Java binding lives in the gempba repo under `bindings/`. The shared source set (`java/`) is compiled into both artifacts, `gempba` and `gempba-mpi`; `java-mpi/` adds the `mpi` package to `gempba-mpi` only.

<div class="file-tree">

<div><span class="dn">bindings/</span></div>

<div class="d1"><span class="tc">├── </span><span class="dn">java/</span></div>
<div class="d2"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/pom.xml">pom.xml</a> <span class="file-desc">— Maven build: the <code>gempba</code> and <code>gempba-mpi</code> variants and the natives each JAR bundles</span></div>
<div class="d2"><span class="tc">└── </span><span class="dn">src/main/</span></div>

<div class="d3"><span class="tc">├── </span><span class="dn">java/io/gempba/</span> <span class="file-desc">— shared source set (both artifacts)</span></div>
<div class="d4"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/GemPBA.java">GemPBA.java</a> <span class="file-desc">— entry point and factories</span></div>
<div class="d4"><span class="tc">├── </span><span class="dn">core/</span></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/core/LoadBalancer.java">LoadBalancer.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/core/Node.java">Node.java</a></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/core/NodeManager.java">NodeManager.java</a></div>
<div class="d4"><span class="tc">├── </span><span class="dn">internal/</span></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/internal/GemPBANative.java">GemPBANative.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/internal/NativeLoader.java">NativeLoader.java</a></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/internal/StopSignals.java">StopSignals.java</a></div>
<div class="d4"><span class="tc">├── </span><span class="dn">scheduler/</span></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/scheduler/Scheduler.java">Scheduler.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/scheduler/SerialRunnable.java">SerialRunnable.java</a></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/scheduler/SerialTask.java">SerialTask.java</a></div>
<div class="d4"><span class="tc">├── </span><span class="dn">stats/</span></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/stats/RankStats.java">RankStats.java</a></div>
<div class="d4"><span class="tc">├── </span><span class="dn">task/</span></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/ClosureTask.java">ClosureTask.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/Deserializer.java">Deserializer.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/LazyArgsSupplier.java">LazyArgsSupplier.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/NodeTask.java">NodeTask.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/ResultClosureTask.java">ResultClosureTask.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/Serializer.java">Serializer.java</a></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/task/VoidNodeTask.java">VoidNodeTask.java</a></div>
<div class="d4"><span class="tc">└── </span><span class="dn">value/</span></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/BalancingPolicy.java">BalancingPolicy.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/EndReason.java">EndReason.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/Goal.java">Goal.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/RunOutcome.java">RunOutcome.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/Score.java">Score.java</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/ScoreType.java">ScoreType.java</a></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java/io/gempba/value/StopTrigger.java">StopTrigger.java</a></div>

<div class="d3"><span class="tc">└── </span><span class="dn">java-mpi/io/gempba/</span> <span class="file-desc">— <code>gempba-mpi</code> only</span></div>
<div class="d4"><span class="tc">└── </span><span class="dn">mpi/</span></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-mpi/io/gempba/mpi/Mpi.java">Mpi.java</a></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/java/src/main/java-mpi/io/gempba/mpi/SchedulerTopology.java">SchedulerTopology.java</a></div>

<div class="d1"><span class="tc">└── </span><span class="dn">jni/</span></div>
<div class="d2"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/bindings/jni/src/gempba_jni.cpp">src/gempba_jni.cpp</a> <span class="file-desc">— JNI shim between the JVM and the C ABI; see <a href="../how-it-works/">How it works</a></span></div>

<br>

<div><span class="dn">include/gempba/</span></div>
<div class="d1"><span class="tc">└── </span><span class="dn">cabi/</span></div>
<div class="d2"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/cabi/gempba.h">gempba.h</a> <span class="file-desc">— the C ABI the JNI shim calls into</span></div>
<div class="d2"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/cabi/gempba_mpi.h">gempba_mpi.h</a> <span class="file-desc">— the MPI component's C calls (<code>gempba_mpi_create_scheduler</code>), behind <code>Mpi.createScheduler</code></span></div>

</div>
