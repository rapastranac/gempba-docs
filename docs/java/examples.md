# Java Examples

Runnable, consumer-side examples live in [**rapastranac/gempba-java-examples**](https://github.com/rapastranac/gempba-java-examples) — the Java mirror of the C++ [gempba-examples](https://github.com/rapastranac/gempba-examples) repo. Each example exercises the public `io.gempba` API exactly as a real downstream project would.

## Modules

| Module | Contents |
|---|---|
| `commons` | Variant-agnostic helpers (busy-wait, jitter, deterministic noise). |
| `sequential` | Plain-Java reference oracles. No GemPBA dependency. |
| `mutithreading` | GemPBA MT examples. Self-contained — no external runtime needed. |
| `multiprocessing` | GemPBA MP examples. Require an MPI runtime (MS-MPI / OpenMPI / MPICH). |

Examples live as sibling sub-packages under `io.gempba.<module>`, one per variant:

```
mutithreading/src/main/java/io/gempba/mt/
  synthetic_void/        # synthetic-tree benchmark, framework Score path
  synthetic_leafsum/     # synthetic-tree benchmark, typed Node#getResult() path
```

## Building

Requires **JDK 25** and **Maven 3.9+**, plus the GitHub Packages authentication described in [Installation](installation.md). Then, from the repo root:

```bash
mvn install
```

## Running

The simplest path is to open the root `pom.xml` in **IntelliJ IDEA**, let Maven resolve, and run any `Main` class with the green ▶ gutter icon.

From the command line (MT / sequential):

```bash
mvn -pl sequential   exec:java -Dexec.mainClass=io.gempba.seq.synthetic_void.Main
mvn -pl mutithreading exec:java -Dexec.mainClass=io.gempba.mt.synthetic_void.Main
```

!!! warning "Multiprocessing must run under mpiexec"
    MP examples must be launched under `mpiexec`/`mpirun`, not plain `java`. The repo ships platform-matched launchers:

    ```bash
    ./multiprocessing/run.ps1 synthetic_void -n 4   # Windows
    ./multiprocessing/run.sh  synthetic_void -n 4   # Linux / macOS
    ```

    where the first argument is the sub-package name under `io.gempba.mp` and `-n` is the number of ranks.
