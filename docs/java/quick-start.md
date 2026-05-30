# Quick Start (Java)

This walks through a complete multithreading program: a synthetic binary-tree traversal that counts leaves in parallel. It is a trimmed version of the `synthetic_void` example from [gempba-java-examples](https://github.com/rapastranac/gempba-java-examples), and it uses the public `io.gempba` API exactly as your own algorithm would.

First make sure the dependency resolves — see [Installation](installation.md). This example uses the `mt` classifier, so no MPI runtime is needed.

## The shape of a GemPBA program

Every GemPBA program follows the same three beats:

1. **Set up** a load balancer and a node manager, and configure the goal.
2. **Seed** the recursion with a root node, then submit it.
3. **Wait** for completion and read the result back.

Your algorithm is the recursive function in the middle. GemPBA owns the thread pool, the work queue, and the best-result bookkeeping.

## The recursive task

The task receives the worker thread id, your arguments, and the current `Node`. It does its per-node work, creates child nodes, and dispatches them back to the pool. Here the "work" is just a synthetic busy-wait; the leaf count is reported as the score.

```java
import io.gempba.GemPBA;
import io.gempba.core.LoadBalancer;
import io.gempba.core.Node;
import io.gempba.core.NodeManager;
import io.gempba.value.Score;

import java.util.concurrent.atomic.AtomicLong;

public class Benchmark {
    private final NodeManager nm;
    private final LoadBalancer lb;
    private final AtomicLong leafCount = new AtomicLong(0);

    public Benchmark(NodeManager nm, LoadBalancer lb) {
        this.nm = nm;
        this.lb = lb;
    }

    public void explore(long threadId, int depth, int maxDepth, Node parent) {
        if (depth == maxDepth) {                       // leaf: record a result
            int count = (int) leafCount.incrementAndGet();
            nm.tryUpdateResult(count, Score.make(count));
            return;
        }

        // A non-null parent threads provenance through the load balancer.
        Node vParent = (parent == null) ? GemPBA.createDummyNode(lb) : parent;

        Node left  = GemPBA.createExplicitNode(lb, vParent,
                (tid, node) -> explore(tid, depth + 1, maxDepth, node));
        Node right = GemPBA.createExplicitNode(lb, vParent,
                (tid, node) -> explore(tid, depth + 1, maxDepth, node));

        nm.tryLocalSubmit(left);   // hand one child to the pool
        nm.forward(right);         // recurse into the other on this thread
    }
}
```

The `tryLocalSubmit` / `forward` pair is the idiom: offer one branch to the thread pool, keep walking the other yourself. The quasi-horizontal load balancer decides which pending work is most valuable to hand out.

## The driver

```java
import io.gempba.GemPBA;
import io.gempba.core.LoadBalancer;
import io.gempba.core.Node;
import io.gempba.core.NodeManager;
import io.gempba.task.Deserializer;
import io.gempba.task.Serializer;
import io.gempba.task.VoidNodeTask;
import io.gempba.value.BalancingPolicy;
import io.gempba.value.Goal;
import io.gempba.value.Score;
import io.gempba.value.ScoreType;

public class Main {
    private static final int MAX_DEPTH = 20;

    // The seed's Integer argument has to cross into native C++ code, so it is
    // converted to raw bytes on the way in and back to an int on the way out.
    // Child nodes never need this — see "How it works" for why.
    private static final Serializer<Integer> intToBytes =
            v -> new byte[]{(byte) (v >> 24), (byte) (v >> 16), (byte) (v >> 8), v.byteValue()};
    private static final Deserializer<Integer> bytesToInt =
            b -> ((b[0] & 0xFF) << 24) | ((b[1] & 0xFF) << 16) | ((b[2] & 0xFF) << 8) | (b[3] & 0xFF);

    static void main() throws InterruptedException {
        // 1. Set up
        LoadBalancer lb = GemPBA.createLoadBalancer(BalancingPolicy.QUASI_HORIZONTAL);
        NodeManager  nm = GemPBA.createNodeManager(lb);

        nm.setGoal(Goal.MAXIMISE, ScoreType.I32);   // maximise an int score
        nm.setThreadPoolSize(8);
        nm.setScore(Score.make(0));                  // initial score

        Benchmark benchmark = new Benchmark(nm, lb);

        // 2. Seed the recursion. The two translators above carry the seed's
        //    starting argument across the JNI boundary.
        Node seed = GemPBA.createSeedNode(lb,
                (VoidNodeTask<Integer>) (tid, depth, node) ->
                        benchmark.explore(tid, depth, MAX_DEPTH, node),
                0,             // initial argument: starting depth
                intToBytes,    // Integer -> byte[]  (crossing into C++)
                bytesToInt);   // byte[]  -> Integer (crossing back)

        double start = NodeManager.getWallTime();
        if (!nm.tryLocalSubmit(seed)) {
            throw new RuntimeException("unable to submit seed node");
        }

        // 3. Wait and read results
        nm.waitForCompletion();
        double elapsed = NodeManager.getWallTime() - start;

        System.out.printf("Score: %s%n", nm.getScore());
        System.out.printf("Elapsed: %.6f s%n", elapsed);
        nm.<Integer>getResult().ifPresent(r -> System.out.printf("Result: %d%n", r));

        GemPBA.shutdown();
    }
}
```

!!! question "Why the `intToBytes` / `bytesToInt` translators?"
    They are the seed argument's passage into native code. Java cannot generate a typed native call the way C++ templates do, so GemPBA's Java binding moves a task's payload across the boundary as bytes. Only the **seed** needs them here — the child nodes capture their arguments straight from the Java closure. See [How it works](how-it-works.md) for the full story.

!!! note "Java 25 entry point"
    The example uses the instance `void main()` form finalized in **Java 25** (no `String[] args`, no `public static`). The binding targets JDK 25.

## Run it

```bash
mvn -pl mutithreading exec:java -Dexec.mainClass=io.gempba.mt.synthetic_void.Main
```

Or, in IntelliJ IDEA, open the project's `pom.xml`, let Maven resolve, and hit the green ▶ next to `main`.

## What changes for multiprocessing

The `mp-mpi` classifier adds the `io.gempba.scheduler` package (`Scheduler`, `SchedulerTopology`, `SerialRunnable`) and an MP-specific `GemPBA` factory surface, and the program is launched under `mpiexec`. The recursive-task shape stays the same. See the `multiprocessing` module in [gempba-java-examples](https://github.com/rapastranac/gempba-java-examples) for a full MP program and its launcher.
