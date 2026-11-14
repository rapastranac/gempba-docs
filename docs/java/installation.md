---
description: "Install GemPBA for Java from Maven Central: io.github.rapastranac:gempba for multithreading or gempba-mpi for MPI, with no repository or token to configure."
---

# Installation (Maven)

GemPBA's JARs are on Maven Central as two artifacts that share one API:

- `gempba`, whose native library has no MPI;
- `gempba-mpi`, which adds the `io.gempba.mpi` package for creating an MPI scheduler, and requires an MPI runtime on the host.

A program uses one or the other. Each JAR carries every supported OS's native binary, and the loader picks the right one at runtime.

!!! info "Available from `v5.0.0`"
    `v4.1.0` to `v4.4.0` are on GitHub Packages as `io.gempba:gempba` with the `mt` and `mp-mpi` classifiers, which needs a token with the `read:packages` scope.

## Requirements

- **Java 25** or newer, and **Maven 3.9+**
- Nothing else for the natives beyond the OS: Linux with glibc 2.28 or newer (such as RHEL 8), Windows 10 or newer, or macOS 14 or newer on Apple Silicon
- For `gempba-mpi` only: the MPI runtime its native library is built against, see [Which MPI](#which-mpi)

## Declare the dependency

No repository or token to configure:

```xml
<dependency>
  <groupId>io.github.rapastranac</groupId>
  <artifactId>gempba</artifactId>        <!-- or gempba-mpi -->
  <version>VERSION</version>
</dependency>
```

Then build:

```bash
mvn install
```

## Which MPI

A JAR has to carry its native library compiled, so unlike the C++ packages, `gempba-mpi` is built against one MPI per OS: Open MPI on Linux and macOS, MS-MPI on Windows. With another MPI only, such as MPICH, Intel MPI or Cray MPICH, its native library fails to load, and the error names the MPI it needs.

To use another MPI, build the native library against it on Linux, from the tag of your `gempba-mpi` version so it matches the JAR's classes. It needs a C++23 compiler, CMake, curl, Maven, a JDK and your MPI on `PATH`; on a cluster, load their modules first. `build_jar_host_linux.sh` builds the static hwloc, fmt and spdlog the library links, builds it against that MPI, names the MPI it found, and installs the JAR into `~/.m2`. Then pass the library with the `gempba.native.path` system property, which replaces the bundled one:

```bash
git clone --branch vVERSION https://github.com/rapastranac/gempba.git && cd gempba
bash scripts/build_jar_host_linux.sh MP
mpiexec -n 4 java -Dgempba.native.path=$PWD/bindings/java/src/main/resources/natives/linux-x86_64/gempba_jni.so -cp <classpath> <main class>
```

On macOS and Windows, `scripts/build_jar_macos.sh MP` and, in MSYS2's UCRT64 shell, `scripts/build_jar_windows.sh MP` build it against the MPI CMake finds; pass `natives/osx-aarch64/gempba_jni.dylib` or `natives/win-x86_64/gempba_jni.dll`.

!!! tip "Intel Macs"
    The JARs' macOS native is for Apple Silicon only. On an Intel Mac, `scripts/build_jar_macos.sh MT` (or `MP`) builds `natives/osx-x86_64/gempba_jni.dylib`; pass it with `-Dgempba.native.path`.

## Next

Head to the [Quick Start](quick-start.md) for a complete working program.
