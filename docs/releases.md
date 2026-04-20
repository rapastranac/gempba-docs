# Releases

---

## v3.1.0 <small>— April 19, 2026 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v3.1.0)</small>

macOS support, lint enforcement, code coverage, packaging, and portability fixes.

**Added**

- macOS CI pipeline (macOS 26) with OpenMPI
- Lint workflow: clang-format-21 check and clang-tidy-18 static analysis on every push and PR
- `scripts/lint.sh` — local lint helper with `--format-only`, `--tidy-only`, `--fix`, and `--jobs` flags
- Code coverage instrumentation and upload to Codecov
- CMake install rules, pkg-config file, CPack DEB packaging, and a GPG-signed APT repository
- MSYS2 PKGBUILD for Windows packaging
- CI publish jobs for both Ubuntu (`.deb`) and Windows (`.pkg.tar.zst`) on version tags

**Changed**

- Windows CI runner upgraded from 2022 to 2025
- `Queue` renamed to `queue` and wrapped in the `gempba` namespace
- Bundled spdlog replaced with system-installed spdlog
- CPM.cmake download hardened against silent corruption

**Fixed**

- Bug in `mpi_centralized_scheduler`
- Portability: removed `<bits/stdc++.h>`, gated `<stacktrace>` on `__has_include`, fixed `score` type-dispatch across platforms, dropped `-fconcepts`, gated `-rdynamic` and `stdc++exp` for non-Linux targets

**Removed**

- Private `node_manager` method that always returned zero

---

## v3.0.0 <small>— December 8, 2025 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v3.0.0)</small>

Ground-up architectural rewrite. Single-header facade, template-free nodes, fully pluggable subsystems.

**Added**

- Single-header facade: `#include <gempba/gempba.hpp>` replaces multi-step initialization
- Template-free node API — internal type erasure eliminates `Node<...>` and `ResultHolder<...>` from user code entirely
- Lazy node evaluation: arguments constructed only when `should_branch()` is called, avoiding allocation for pruned branches
- Visitor-based statistics system (`stats` / `stats_visitor` interfaces + `default_mpi_stats_visitor`)
- Pluggable architecture: every subsystem (scheduler, load balancer, node core, serial runnable, stats) replaceable via interface

**Changed**

- `branch_handler` → `node_manager`
- `mpi_scheduler` → `scheduler`, exposing `center_view()` and `worker_view()`
- Factory functions relocated to `gempba::mt::` (multithreading) and `gempba::mp::` (multiprocessing) namespaces
- `try_push_mt()` / `try_push_mp()` → `try_local_submit()` / `try_remote_submit()`

**Removed**

- `DLB_Handler` singleton
- `branch_handler` singleton
- `ResultHolder<>` template
- Manual virtual root linking (now handled automatically)

**Requirements**

- C++23

---

## v2.0.0 <small>— August 17, 2025 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v2.0.0)</small>

IPC data model overhaul. Raw-byte transport, new result and score types, naming cleanup.

**Added**

- `gempba::task_packet` — raw byte buffer replaces string-serialized IPC data
- `gempba::result` — dedicated type for shipping results across processes
- `gempba::score` — type-erased numeric, supports multiple primitive types (replaces `reference_value`)

**Changed**

- Classes, member functions, and member variables renamed per `.clang_tidy` conventions
- Schedulers now exchange raw bytes instead of serialized strings
- Fixed MPI communicator probing in centralized scheduler

**Build**

- Improved `CMakeLists` readability
- `openmpi` invocation now correctly bound to intended core count

---

## v1.1.0 <small>— August 4, 2025 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v.1.1.0)</small>

MPI scheduler cleanup and citation support.

**Added**

- Citation files (`CITATION.cff`)

**Changed**

- MPI scheduler communicator probing reorganized for correctness and readability
- `runCenter` and `runNode` refactored with `switch` statements for clarity

---

## v1.0.2 <small>— June 8, 2025 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v1.0.2)</small>

Improved external dependency integration and build ergonomics. No compatibility breaks.

**Added**

- [CPM](https://github.com/cpm-cmake/CPM.cmake) for external CMake dependency management
- Custom initial process topology injection via new scheduler method
- Macros now ship with defaults; consumer projects can override as needed

**Changed**

- GemPBA now straightforward to import as an external CMake dependency
- Macros renamed for clarity

**Fixed**

- Compilation errors in several examples

**Build**

- Improved `CMakeLists` readability
- Files reorganized

---

## v1.0.1 <small>— October 30, 2024 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v1.0.1)</small>

Project structure improvements and CI/CD setup. No compatibility breaks.

**Added**

- Common parent class for `MPI_Scheduler` and `MPI_Scheduler_Centralized`
- Common parent class for `ResultHolder`
- CI/CD pipeline triggered on merges to `main`
- Each example now builds as its own standalone executable, ensuring compile-time coverage on changes

**Fixed**

- Minor bugs related to macro usage

**Build**

- Project structure reorganized

---

## v1.0.0 <small>— April 9, 2024 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v1.0.0)</small>

Initial stable release.
