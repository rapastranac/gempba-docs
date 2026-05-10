# Releases

???+ note "v3.1.0"

    <small>April 19, 2026 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v3.1.0)</small>

    macOS support, system packaging (`.deb`, MSYS2, signed APT repo), and cross-platform portability fixes.

    **Breaking changes**

    - `gempba::Queue` renamed to `gempba::queue` (header moved to `include/gempba/utils/queue.hpp`) — update any direct uses
    - Bundled `spdlog` removed; consumers must now provide a system-installed `spdlog` (and `fmt`) via `find_package`
    - `GEMPBA_*` build options (`GEMPBA_MULTIPROCESSING`, `GEMPBA_BUILD_TESTS`, `GEMPBA_BUILD_EXAMPLES`, `GEMPBA_DEBUG_COMMENTS`, `GEMPBA_DEV_MODE`) now honor `-D` overrides when used as a subproject — previously hard-coded values shadowed user input

    **Added**

    - macOS officially supported (Apple Silicon, AppleClang/libc++, Homebrew Boost 1.90)
    - Debian/Ubuntu `.deb` packages (`libgempba-dev`) published on tagged releases
    - Signed APT repository at `apt-repo/` with `pubkey.gpg` for `apt-get install libgempba-dev`
    - MSYS2 `PKGBUILD` at `packaging/msys2/` for `mingw64` / `ucrt64` / `clang64` builds, with a Windows CI publish job producing `.pkg.tar.zst` artifacts
    - CMake install rules and `gempbaConfig.cmake` — consumers can now `find_package(gempba 3.1.0 REQUIRED)` and link `gempba::gempba`
    - pkg-config file (`gempba.pc`) for non-CMake build systems
    - `scripts/update-pkgbuild.sh` to regenerate `pkgver` and `sha256` for MSYS2 packagers

    **Changed**

    - README rewritten and trimmed; full reference moved to the [docs site](https://rapastranac.github.io/gempba-docs/)
    - Build/run scripts relocated under `scripts/` (`build_linux.sh`, `build_windows.sh`, `run.sh`, etc.); old top-level `linux_build.sh` / `win_build.sh` removed
    - `-rdynamic` is now applied only on Linux Debug builds (no longer leaks into Release or non-Linux targets)
    - CPM.cmake download hardened against silent corruption

    **Fixed**

    - `mpi_centralized_scheduler`: misplaced parenthesis in the `MPI_Wtime`/`diff_time` comparison broke the rate-limit on "center queue full" notifications, causing repeated worker contacts every loop iteration instead of at most once per second
    - `<bits/stdc++.h>` removed from `node_manager.hpp` — header now compiles on libc++ / AppleClang / MSVC
    - C++23 `<stacktrace>` gated on `__has_include` so libc++ targets without it still build
    - `gempba::score` type-dispatch, comparison, and `to_string` made portable across `long double` ABIs
    - Dropped `-fconcepts` (legacy GCC flag) and gated `stdc++exp` for non-Linux toolchains
    - `BS_thread_pool` include directory now propagated so private headers compile against installed packages
    - `<gempba/config.h>` resolves correctly in all build layouts (now generated into `build/gempba/`)

    **Removed**

    - Private `node_manager` method that always returned zero (worker view returns zero directly)

??? note "v3.0.0"

    <small>April 19, 2026 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v3.0.0)</small>

    The largest release in the project's history: a ground-up redesign that replaces the heavy template-driven API with a single-header `gempba::` facade. `branch_handler` becomes `node_manager`, the entire pre-v3 surface (`result_holder`, `dynamic_load_balancer_handler`, `Pool`, `args_handler`, all `*2`-suffixed members) is removed, and the public surface is reorganized under `include/gempba/`.

    **Breaking changes**

    - `gempba::branch_handler` renamed to `gempba::node_manager` (class and header) — the main user-facing class
    - `gempba::ResultHolder` / `gempba::result_holder` removed entirely; use `gempba::node` instead — function signatures no longer take a holder template
    - `gempba::DLB_Handler` / `gempba::dynamic_load_balancer_handler` removed; use `gempba::load_balancer` (interface) and the new `create_load_balancer` factories
    - `gempba::Pool` and `gempba::args_handler` removed
    - All `*2`-suffixed members removed: `is_done2`, `wait2`, `get_balancing_policy2`, plus `*2` variants in MPI schedulers
    - `node_manager::lock()` / `unlock()` removed
    - `node_manager` member renames: `try_push_mp` → `try_remote_submit`, `try_push_mt` → `try_local_submit`, `force_push` → `force_local_submit`, `push_multiprocess` / `push_multithreading` → `send`, `WTime` → `get_wall_time`, `try_top_holder` → `try_push_root_level_holder_remotely`, `pass_mpi_scheduler` → `pass_scheduler`
    - Identifier renames on the public surface: `load_balancing_strategy` → `balancing_policy`, `print_mpi_debug_comments` → `print_ipc_debug_comments`, `FUNCTION_ARGS` → `TASK`, `gbitset` → `G_BITSET`, "reference value" → `score` throughout MPI schedulers
    - `mpi_scheduler` renamed to `mpi_semi_centralized_scheduler`
    - `scheduler` members supplanted by `scheduler::worker` / `scheduler::center` views: `fetch_solution`, `fetch_result_vector`, `next_process`, `push`, `run_node`, `run_center`, `try_open_transmission_channel`, `close_transmission_channel`
    - `scheduler::get_total_requests` removed (now sourced from the new stats interface)
    - C++23 enforced in CMake (`CMAKE_CXX_STANDARD 23`, `CMAKE_CXX_STANDARD_REQUIRED ON`, extensions off); C++20 compilers are no longer supported
    - `BS::thread_pool` is now an external dependency; consumers using CPM mirror it automatically, manual integrations must add it
    - `GEMPBA_*` compile definitions on the `gempba` target are now `PRIVATE` instead of `PUBLIC`
    - Public headers reorganized under `include/gempba/` (`core/`, `utils/`, `stats/`, `defaults/`, `detail/`); legacy `include/utils/...` paths are gone
    - Legacy `.csv` / `.dat` raw printing removed from examples; CSV log is now opt-in and off by default

    **Added**

    - Single-header facade `#include <gempba/gempba.hpp>` exposing `gempba::` factories
    - `gempba::node` — lightweight, copyable, template-free node handle (replaces `result_holder`)
    - `gempba::shutdown()` for explicit, controlled global cleanup
    - `gempba::node_manager` factories: `multithreading::create_node_manager(load_balancer*)` and `multiprocessing::create_node_manager(load_balancer*, scheduler::worker*)`
    - `gempba::load_balancer` public interface with two stock implementations: `quasi_horizontal_load_balancer` (recommended) and `work_stealing_load_balancer`
    - `multithreading::create_load_balancer(balancing_policy)` and `multiprocessing::create_load_balancer(balancing_policy, scheduler::worker*)` factories, plus a BYO-implementation overload
    - `gempba::scheduler` public interface with `scheduler::worker` and `scheduler::center` views, `scheduler_traits`, and `multiprocessing::create_scheduler(scheduler_topology, timeout)` (`SEMI_CENTRALIZED`, `CENTRALIZED`)
    - `gempba::node_core` extension point (`include/gempba/core/node_core.hpp`) plus `node_traits` and the `detail/nodes/node_core_impl.hpp` template implementation
    - `gempba::stats` and `gempba::stats_visitor` interfaces; `default_mpi_stats_visitor` for the bundled MPI schedulers (visitor pattern, string-keyed metrics)
    - `gempba::serial_runnable` interface with `serial_runnable_void` / `serial_runnable_non_void` impls and `runnables::return_none::create` / `runnables::return_value::create` helpers for MP task dispatch
    - `gempba::serializable` interface to split serialization responsibilities out of node trace
    - `gempba::task_bundle` and `gempba::transmission_guard` utilities under `include/gempba/utils/`
    - `invokable` C++23 concept that enforces task signatures of the form `Ret(std::thread::id, Args..., node)`
    - `gempba::score` extended with `uint32_t` and `int64_t` so it can carry `std::size_t` and other common types; spaceship `operator<=>` on `task_packet`
    - `utils::log_and_throw` (replaces direct `spdlog::throw_spdlog_ex`) with C++23 `<stacktrace>` integration
    - Generated `gempba/config.h` (from `config.h.in`) so IDEs see the build flags
    - Multi-processing and multi-threading benchmark cases
    - One-call Windows and Linux build scripts and helpers to run all graphs in a directory

    **Changed**

    - Module renames swept the codebase to snake_case: `BranchHandler` → `branch_handler` (then `node_manager`), `ThreadPool` → `thread_pool`, `DLB` → `dynamic_load_balancer`, `MPI_Modules` → `schedulers`, `Resultholder` → `result_holder` (then removed)
    - `gempba::score` now has unsigned 32/64 specializations; `score::make(...)` accepts `std::size_t`
    - Schedulers now receive their timeout at construction (`create_scheduler(topology, timeout)`)
    - `default_mpi_stats_visitor` lives in the `defaults` module and is exposed via `multiprocessing::get_default_mpi_stats_visitor()`
    - Internal `spdlog::info` calls demoted to `spdlog::debug`
    - `#ifdef GEMPBA_DEBUG_COMMENTS` replaced with `#if GEMPBA_DEBUG_COMMENTS` (matches the new `cmakedefine01`)
    - README rewritten for v3.0 (facade pattern, extensible architecture, updated requirements, Windows added to supported platforms)

    **Fixed**

    - Race condition that could let a worker thread throw
    - Edge case in node pruning (children weren't cleared on prune)
    - Critical guard fix in `quasi_horizontal_load_balancer`

    **Build**

    - C++23 enforced (`CMAKE_CXX_STANDARD_REQUIRED ON`, `CMAKE_CXX_EXTENSIONS OFF`)
    - Links `stdc++exp` on non-MSVC for C++23 `<stacktrace>` support
    - New `GEMPBA_DEV_MODE` toggle in the root `CMakeLists.txt` (auto-on when gempba is the root project)
    - `GEMPBA_*` target flags scoped to `PRIVATE` (no longer leaks to consumers)
    - `BS::thread_pool` added via CPM (`rapastranac/thread-pool`); `argparse` moved to `examples/external` since it's only used by examples
    - `GIT_SHALLOW TRUE` set on CPM external clones
    - Per-test discovery in CTest (`gtest_discover_tests`) and a separate test-artifact publish job in CI; `FLAKY_` test-name convention for flaky cases
    - Dropped redundant `git install` step from CI

??? note "v2.1.1"

    <small>September 1, 2025 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v2.1.1)</small>

    Single-fix patch release for the centralized MPI scheduler.

    **Fixed**

    - `mpi_centralized_scheduler` worker `probe_reference_value_comm()` was probing `REFVAL_PROPOSAL_TAG` (the worker-to-center tag) instead of `REFVAL_UPDATE_TAG`, so global reference-value updates broadcast by the center were never picked up by workers — leaving them with stale bounds and exploring branches that should have been pruned ([#55](https://github.com/rapastranac/gempba/pull/55))

??? note "v2.1.0"

    <small>August 23, 2025 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v2.1.0)</small>

    Source-level Windows support, alongside a dedicated Windows CI pipeline.

    **Added**

    - Windows build support: GemPBA now compiles on Windows with MSVC
    - `run.ps1` PowerShell launcher at the repo root for running multiprocessing (`mpiexec.exe`) and multithreading example binaries on Windows
    - Windows CI workflow (`.github/workflows/c-cpp-windows.yml`) building on Windows Server 2022, with a matching status badge in the README

    **Changed**

    - `centralized_utils.hpp` now defines `NOMINMAX`, `WIN32_LEAN_AND_MEAN`, and `RPC_NO_WINDOWS_H` before including `windows.h` to avoid `std::byte` ambiguity and `min`/`max` macro clashes against `<windows.h>`
    - `score::make` factory dispatches by integral size (`int32_t`/`int64_t`) instead of exact type, so scores constructed from `long` and other platform-dependent integer widths behave the same on Windows and Linux
    - Ubuntu workflow renamed from `c-cpp.yml` to `c-cpp-ubuntu.yml` (Ubuntu 24.04); README badge updated accordingly
    - `args_handler.hpp` switched to angle-bracket includes and replaced `std::forward<nullptr_t>(nullptr)` with a plain `nullptr` argument for portability

    **Fixed**

    - Corrected the closing namespace comment in `args_handler.hpp` (`} // namespace gempba`)

    **Build**

    - Test executable renamed from `all_tests.out` to `all_tests` (drops the Linux-style suffix so the same target name works on Windows)

??? note "v2.0.0"

    <small>August 17, 2025 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v2.0.0)</small>

    Major release: new `gempba::score`, `gempba::task_packet`, and `gempba::result` public types replace string-based transport and the `int` reference value, alongside a sweeping `clang-tidy` rename of the public API (`BranchHandler` → `branch_handler`, `MPI_Scheduler` → `mpi_scheduler`, `SchedulerParent` → `scheduler_parent`, etc.).

    **Breaking changes**

    - `gempba::BranchHandler` → `gempba::branch_handler`; `getInstance()` → `get_instance()`; `try_push_MT` → `try_push_mt`; member methods renamed per `.clang-tidy` (e.g. `refValue()` is gone — use `get_score().get<T>()`)
    - `gempba::MPI_Scheduler` → `gempba::mpi_scheduler`; `gempba::MPI_SchedulerCentralized` → `gempba::mpi_centralized_scheduler` (header `MPI_Scheduler_Centralized.hpp` → `mpi_centralized_scheduler.hpp`)
    - `gempba::SchedulerParent` → `gempba::scheduler_parent`; `fetchSolution()` → `fetch_solution()` now returns `task_packet` instead of `std::string`; `fetchResVec()` → `fetch_result_vector()` returns `std::vector<gempba::result>` instead of `std::vector<std::pair<int, std::string>>`; `push()` now takes a `task_packet&&` instead of `std::string`
    - `branch_handler::set_score` / `get_score` / `set_goal` and the `gempba::result` constructor: `int` reference value replaced with `gempba::score`. `set_goal` now takes a `gempba::goal` enum plus `gempba::score_type` (was a `bool`)
    - `hold_solution` removed — replaced by `try_update_result(solution, score)`: type-safe, parameters reordered, default parameter dropped, returns `bool` indicating whether the update happened
    - `update_reference_value` → `try_update_reference_value`; further renamed to `try_update_reference_value_and_invalidate_result` to reflect that it now clears any cached result when the score changes
    - `score::get_loose` removed — use `score::to_string` (logs print the value with its real underlying type) or the typed `score::get<T>()` accessor
    - `set_ref_val_strategy_lookup` → `scheduler_parent::set_goal`; `lookup_strategy` parameter → `goal` enum
    - `EMPTY_RESULT` constant removed — use `result::EMPTY`
    - `m_reference_value` member of `gempba::result` renamed to `m_score`; scheduler members `m_ref_value_global` → `m_global_reference_value` (and corresponding communicator member)
    - Examples no longer accept the `THREADS_PER_TASK` argument on the command line
    - `GEMPBA_MULTIPROCESSING` is now a value macro (`0`/`1`), no longer a bare definition — examples and downstream consumers must use `#if GEMPBA_MULTIPROCESSING` instead of `#ifdef`

    **Added**

    - `gempba::task_packet` (`include/utils/ipc/task_packet.hpp`) — raw-byte transport that replaces serialized `std::string` in the scheduler API; serializers now return `task_packet`
    - `gempba::result` (`include/utils/ipc/result.hpp`) — bundles a `score` plus `task_packet` for shipping solutions between ranks
    - `gempba::score` (`include/utils/ipc/score.hpp`) and `gempba::score_type` enum (`I32`, `I64`, `F32`, `F64`, `F128`) — multi-primitive score support, formerly the integer-only `reference_value` (suggested by @Manuel-GithubAccount in [#29](https://github.com/rapastranac/gempba/issues/29))
    - `gempba::goal` enum to replace the previous boolean min/max strategy flag
    - `score::make` factory and `score::to_string` for type-aware logging
    - README "Concepts" section documenting `goal`, `score`, and `score_type`

    **Changed**

    - Schedulers now exchange raw bytes (`task_packet`) instead of serialized strings end-to-end through `branch_handler` and `scheduler_parent`
    - `mpi_scheduler` and `mpi_centralized_scheduler` made structurally parallel: shared `should_broadcast` logic, `utils::diff_time` adopted in both, analogous global-reference-value checks
    - `handle_full_messaging` → `monitor_and_notify_center_status`
    - Most `GEMPBA_DEBUG_COMMENTS` macro sites replaced with a single utility method
    - README updated for all renamed identifiers and the new `try_update_result` / `score` usage
    - `batch.sh` → `run.sh`

    **Fixed**

    - Communicator probing in `mpi_centralized_scheduler` (matching the fix already in `mpi_scheduler`)
    - `openmpi` invocation now binds processes to the intended number of cores
    - A `try_update_result` path that wasn't actually updating the stored reference value
    - `GEMPBA_MULTIPROCESSING` checks ([#49](https://github.com/rapastranac/gempba/issues/49)): switched from `#ifdef` to `#if`, and the macro is now injected as an explicit `0`/`1` value so non-MP examples see it defined as false rather than undefined

    **Build**

    - `CMakeLists.txt` project version bumped to `2.0.0`
    - `examples/CMakeLists.txt`: defines `GEMPBA_MULTIPROCESSING=1` for `mp_*` examples and `GEMPBA_MULTIPROCESSING=0` for the rest (previously only the `mp_*` side was defined)

??? note "v1.1.0"

    <small>August 4, 2025 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v.1.1.0)</small>

    Citation metadata, a refreshed README, and dependency-management changes that consumers need to mirror.

    > The git tag is `v.1.1.0` (extra dot — original spelling preserved). Everywhere else the version is referred to as `v1.1.0`.

    **Added**

    - `CITATION.cff` and `CITATION.bib` at the repo root for academic citation
    - README sections for Requirements, Platforms, Dependency Management, Copyright and citing
    - `FUNCTION_ARGS` tag for routing serialized function arguments separately from other messages
    - `REFERENCE_VAL_PROPOSAL` and `REFERENCE_VAL_UPDATE` tags (split from the former single reference-value tag)

    **Changed**

    - Inter-process tags in `MPI_Modules/MPI_Scheduler.hpp` are now an `enum tags { ... }` (`CENTER_NODE`, `RUNNING_STATE`, `ASSIGNED_STATE`, `AVAILABLE_STATE`, `TERMINATION`, `REFERENCE_VAL_PROPOSAL`, `REFERENCE_VAL_UPDATE`, `NEXT_PROCESS`, `HAS_RESULT`, `NO_RESULT`, `FUNCTION_ARGS`) replacing the previous `#define` macros (`STATE_RUNNING`, `STATE_ASSIGNED`, `STATE_AVAILABLE`, `TERMINATION_TAG`, `REFVAL_UPDATE_TAG`, `NEXT_PROCESS_TAG`, `HAS_RESULT_TAG`, `NO_RESULT_TAG`); consumers relying on the old macro names must rename to the enum values
    - README installation walkthrough moved above the description; CMake snippet now sets `GEMPBA_MULTIPROCESSING`, `GEMPBA_DEBUG_COMMENTS`, `GEMPBA_BUILD_EXAMPLES`, `GEMPBA_BUILD_TESTS` cache variables and links `gempba::gempba`

    **Fixed**

    - `examples/include/VertexCover.hpp` include switched from `fmt/core.h` to `<format>` (matches the C++20 toolchain)

    **Build**

    - CMake project version bumped to `1.1.0`
    - `spdlog` removed from core CMake: `find_package(spdlog REQUIRED)` and `spdlog::spdlog` link are gone; consumers add it via CPM in `external/CMakeLists.txt` (pinned to `gabime/spdlog@1.15.1`, built static)
    - `argparse` CPM entry rewritten in long form (`NAME argparse / GITHUB_REPOSITORY p-ranav/argparse / VERSION 3.0`); `external_libs` now also exports `spdlog`
    - `examples/CMakeLists.txt` sets `Boost_USE_STATIC_LIBS ON` so Boost is linked statically into the example binaries

??? note "v1.0.2"

    <small>June 8, 2025 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v1.0.2)</small>

    Easier external integration: GemPBA is now a consumable CMake library with a `gempba::gempba` target, a hook to inject a custom initial process topology, and CPM-based dependency fetch.

    **Added**

    - `gempba::gempba` ALIAS target so consumers can `target_link_libraries(... gempba::gempba)`
    - `SchedulerParent::set_custom_initial_topology(tree&&)` to inject a custom initial process topology
    - New CMake options `GEMPBA_BUILD_TESTS` and `GEMPBA_BUILD_EXAMPLES` (default `OFF` when used as a subproject)
    - New CMake options `GEMPBA_MULTIPROCESSING` and `GEMPBA_DEBUG_COMMENTS` to drive compile-time macros from the build
    - `wall_time`, `diff_time`, `shift_left` utility functions in `utils/utils.hpp`
    - `build_topology` extracted from `MPI_Scheduler` into `utils/utils.hpp`
    - Public `tree` type at `include/utils/tree.hpp` (replaces `MPI_Modules/Tree.hpp`)
    - README section documenting CPM-based integration into a downstream project
    - Filename is now included in "file not found" exception messages

    **Changed**

    - GemPBA now builds as a CMake library; examples and tests are separate subprojects gated by the new options
    - Public include roots are `${workspace}/include` and `${workspace}/GemPBA`, exported via `target_include_directories` (`BUILD_INTERFACE`)
    - Macro renames: `MULTIPROCESSING_ENABLED` → `GEMPBA_MULTIPROCESSING`; `DEBUG_COMMENTS` → `GEMPBA_DEBUG_COMMENTS` (consumers must update guards and `target_compile_definitions`)
    - `BranchHandler` API renamed to snake_case: `setLookupStrategy` → `set_lookup_strategy`, `setLoadBalancingStrategy` → `set_load_balancing_strategy`, `getLoadBalancingStrategy` → `get_load_balancing_strategy`
    - Enum types renamed: `LookupStrategy` → `lookup_strategy`, `LoadBalancingStrategy` → `load_balancing_strategy` (enumerator names like `MAXIMISE`, `MINIMISE`, `QUASI_HORIZONTAL` are unchanged)
    - `scheduler_parent.hpp` now includes `<mpi.h>` (was `mpi/mpi.h`); fixes builds on MPI distributions that don't expose the `mpi/` prefix
    - `argparse` is now fetched via [CPM](https://github.com/cpm-cmake/CPM.cmake) instead of `FetchContent_Declare`
    - Verbose `spdlog::info` calls in production code demoted to `spdlog::debug`
    - Project version bumped to 1.0.2; release built against C++23 (`CMAKE_CXX_STANDARD 23`)
    - Default build type is `Debug` when GemPBA is the root project, inherited from the parent otherwise
    - README rewritten with shields.io markdown badges; licence and version badges fixed

    **Removed**

    - `Boost` (`system`, `serialization`, `fiber`) is no longer linked or required by the library target; consumers no longer need to provide it
    - `GTest` is no longer required to build the library; it is now only needed when `GEMPBA_BUILD_TESTS=ON`
    - Legacy headers `GemPBA/MPI_Modules/Tree.hpp`, `GemPBA/utils/Queue.hpp`, `GemPBA/utils/utils.hpp` (replaced by their counterparts under `include/utils/`)

    **Fixed**

    - Source-file detection in the root `CMakeLists.txt`
    - Hard-coded `-O0` debug flags and `add_definitions(-DDEBUG_COMMENTS)` no longer leak into Release builds; flags are now per-configuration via generator expressions

    **Build**

    - `clang-tidy` and `clang-format` configurations added at the repo root
    - `.vs/` and `CMakeSettings.json` added to `.gitignore`

??? note "v1.0.1"

    <small>October 30, 2024 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v1.0.1)</small>

    Restructured layout, C++23 build, typed strategy enums, and a scheduler base class so the semicentralized and centralized schedulers can coexist.

    **Added**

    - `gempba::SchedulerParent` (`MPI_Modules/scheduler_parent.hpp`) — common abstract base for `MPI_Scheduler` and the centralized scheduler so both can be instantiated independently
    - `gempba::ResultHolderParent` (`Resultholder/ResultHolderParent.hpp`) — non-template base for `ResultHolder` so virtual interfaces no longer leak template parameters
    - `gempba::LoadBalancingStrategy` enum (`QUASI_HORIZONTAL`, `WORK_STEALING`) and `gempba::LookupStrategy` enum (`MAXIMISE`, `MINIMISE`) in `utils/gempba_utils.hpp`
    - `BranchHandler::setLoadBalancingStrategy` / `getLoadBalancingStrategy`
    - `BranchHandler::setLookupStrategy(gempba::LookupStrategy)` — typed replacement for the string-keyword setter
    - `BranchHandler::getWorldRank`
    - `DLB_Handler::getRoot(int threadId)`
    - `THIRD-PARTY-LICENSES` file with CPTL credits (Apache 2.0)

    **Changed**

    - C++ standard bumped to C++23 (`CMAKE_CXX_STANDARD 23`); minimum CMake bumped to 3.28
    - Project layout reorganized: per-example executables under `bin/`, examples and tests in dedicated trees, headers under `GemPBA/utils/` (was `GemPBA/Utils/`)
    - Build now produces one executable per file under `examples/`; sources matching `mp_*` get `-DMULTIPROCESSING_ENABLED` automatically
    - The library is now built as a CMake target named `gempba` (was a single `a.out` executable)
    - `MPI_ENABLED` compile macro renamed to `MULTIPROCESSING_ENABLED`
    - `R_SEARCH` macro removed; load-balancing strategy is now a runtime enum on `BranchHandler` (so misuse becomes a compile error rather than a silent macro miss)
    - Centralized scheduler class renamed from `GemPBA::MPI_Scheduler` (in `MPI_Scheduler_Centralized.hpp`) to `gempba::MPI_SchedulerCentralized`, allowing both schedulers to be linked into the same binary
    - Public namespace renamed from `GemPBA` to `gempba` (all classes and free functions moved)
    - `MPI_Scheduler::rank_me`, `elapsedTime`, `getWorldSize`, `tasksRecvd`, `tasksSent`, `nextProcess` are now `const`; `runNode` signature changed to take `std::function` callbacks (no longer a templated lambda accepting a `serializer`)
    - `SchedulerParent::getTotalRequests` returns `size_t` (was `double` on the prior centralized scheduler)
    - Input data directory renamed from `input/` to `data/`
    - Logging migrated from `fmt` to `spdlog` (which uses fmt internally); debug prints go through `utils::print_mpi_debug_comments`
    - README updated for the new namespace, strategy enums, and centralized-scheduler usage

    **Removed**

    - `BranchHandler::setRefValStrategyLookup(std::string)` — replaced by `setLookupStrategy(gempba::LookupStrategy)`
    - `R_SEARCH` compile-time flag

    **Build**

    - Root `CMakeLists.txt` rewritten: `find_package(spdlog REQUIRED)` and `find_package(GTest REQUIRED)` added; resources globbed recursively
    - `fmt` dropped as a direct FetchContent dependency (pulled in transitively via spdlog)
    - `argparse` FetchContent pin bumped from v2.9 to v3.0
    - Boost components `system`, `serialization`, `fiber` linked per-target via imported `Boost::*` targets instead of `CMAKE_EXE_LINKER_FLAGS`
    - Tests promoted to a top-level `tests/` subdirectory with its own CMake project, linking GTest/GMock and Boost; `enable_testing()` and `add_test` registered
    - New `.github/workflows/c-cpp.yml` CI pipeline triggered on pushes/merges to `main`
    - Executable output directory moved to `${CMAKE_SOURCE_DIR}/bin`

    **Fixed**

    - CMake resource discovery now recurses into subdirectories
    - OpenMP made visible to the test target
    - spdlog fetch / link wiring corrected
    - Several macro-guarded code paths that broke when `MPI_ENABLED` was off

??? note "v1.0.0"

    <small>April 9, 2024 · [GitHub ↗](https://github.com/rapastranac/gempba/releases/tag/v1.0.0)</small>

    Initial stable release of GemPBA — a generic message-passing branch-and-bound framework for distributed C++ workloads.
