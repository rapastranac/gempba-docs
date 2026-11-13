# File Index

<div class="file-tree">

<div><span class="dn">[root]</span></div>
<div class="d1"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/config.h.in">config.h.in</a> <span class="file-desc">— template for CMake which configures the corresponding <code>config.h</code> file</span></div>

<br>

<div><span class="dn">bindings/</span> <span class="file-desc">— non-C++ front-ends; documented in the <a href="../../java/">Java</a> section</span></div>
<div class="d1"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/tree/main/bindings/java">java/</a> <span class="file-desc">— the <code>io.gempba</code> Maven binding (typed wrappers, NativeLoader, fat-JAR packaging)</span></div>
<div class="d1"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/tree/main/bindings/jni">jni/</a> <span class="file-desc">— JNI shim between the JVM and the C ABI; see <a href="../../java/how-it-works/">How it works</a></span></div>

<br>

<div><span class="dn">include/</span></div>
<div class="d1"><span class="tc">└── </span><span class="dn">gempba/</span></div>
<div class="d2"><span class="tc">├── </span><span class="dn">cabi/</span></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/cabi/gempba.h">gempba.h</a> <span class="file-desc">— stable C ABI over the full runtime; what the <a href="../../java/how-it-works/">Java binding</a> sits on</span></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/cabi/gempba_mpi.h">gempba_mpi.h</a> <span class="file-desc">— the C ABI's calls for the MPI component</span></div>
<div class="d2"><span class="tc">├── </span><span class="dn">core/</span></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/load-balancer/">load_balancer.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../defaults/node/">node.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/node-core/">node_core.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/node-traits/">node_traits.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/core/rank_role.hpp">rank_role.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/scheduler/">scheduler.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/core/scheduler_traits.hpp">scheduler_traits.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/serial-runnable/">serial_runnable.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/core/serializable.hpp">serializable.hpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="../../stopping-a-run/">stop.hpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">detail/</span></div>
<div class="d3"><span class="tc">├── </span><span class="dn">nodes/</span></div>
<div class="d4"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/detail/nodes/node_core_impl.hpp">node_core_impl.hpp</a></div>
<div class="d3"><span class="tc">└── </span><span class="dn">runnables/</span></div>
<div class="d4"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/detail/runnables/serial_runnable_non_void.hpp">serial_runnable_non_void.hpp</a></div>
<div class="d4"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/detail/runnables/serial_runnable_void.hpp">serial_runnable_void.hpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">mpi/</span> <span class="file-desc">— the MPI component's public headers</span></div>
<div class="d3"><span class="tc">└── </span><a href="../implementations/stats-visitors/default-mpi-stats-visitor/">default_mpi_stats_visitor.hpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">stats/</span></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/stats/">stats.hpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="../interfaces/stats-visitor/">stats_visitor.hpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">telemetry/</span> <span class="file-desc">— see the <a href="../../telemetry/">Telemetry</a> section</span></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/telemetry/frames.hpp">frames.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/telemetry/runtime_mode.hpp">runtime_mode.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/telemetry/telemetry_hub.hpp">telemetry_hub.hpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/telemetry/topology.hpp">topology.hpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">utils/</span></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/utils/gempba_utils.hpp">gempba_utils.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/queue/">queue.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/result/">result.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/score/">score.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/task-bundle/">task_bundle.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/task-packet/">task_packet.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/transmission-guard/">transmission_guard.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/tree/">tree.hpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/utils/utils.hpp">utils.hpp</a></div>
<div class="d2"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/export.h">export.h</a></div>
<div class="d2"><span class="tc">├── </span><a href="../defaults/gempba-hpp/">gempba.hpp</a></div>
<div class="d2"><span class="tc">├── </span><a href="../defaults/gempba-hpp/#the-mpi-component-gempbampihpp">mpi.hpp</a> <span class="file-desc">— the MPI component's entry point: <code>gempba::mpi::create_scheduler</code></span></div>
<div class="d2"><span class="tc">└── </span><a href="../defaults/node-manager/">node_manager.hpp</a></div>

<br>

<div><span class="dn">src/</span></div>
<div class="d1"><span class="tc">├── </span><span class="dn">core/</span> <span class="file-desc">— the core, <code>gempba::gempba</code>: libgempba</span></div>
<div class="d2"><span class="tc">├── </span><span class="dn">cabi/</span></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/cabi/gempba.cpp">gempba.cpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">component/</span> <span class="file-desc">— what a component may use from the core; a component installed as source ships these headers with its own</span></div>
<div class="d3"><span class="tc">├── </span><span class="dn">cabi/</span></div>
<div class="d4"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/component/cabi/internals.hpp">internals.hpp</a></div>
<div class="d3"><span class="tc">└── </span><span class="dn">impl/</span></div>
<div class="d4"><span class="tc">├── </span><span class="dn">telemetry/</span></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/component/impl/telemetry/rank_frame_codec.hpp">rank_frame_codec.hpp</a></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/component/impl/telemetry/telemetry_transport.hpp">telemetry_transport.hpp</a></div>
<div class="d4"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/component/impl/install_scheduler.hpp">install_scheduler.hpp</a></div>
<div class="d4"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/component/impl/stop_state.hpp">stop_state.hpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">gempba/</span></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/gempba/gempba.cpp">gempba.cpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/gempba/stop.cpp">stop.cpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">private/</span> <span class="file-desc">— the core's private headers</span></div>
<div class="d3"><span class="tc">└── </span><span class="dn">impl/</span></div>
<div class="d4"><span class="tc">├── </span><span class="dn">load_balancing/</span></div>
<div class="d5"><span class="tc">├── </span><a href="../implementations/load-balancers/quasi-horizontal/">quasi_horizontal_load_balancer.hpp</a></div>
<div class="d5"><span class="tc">└── </span><a href="../implementations/load-balancers/work-stealing/">work_stealing_load_balancer.hpp</a></div>
<div class="d4"><span class="tc">├── </span><span class="dn">nodes/</span></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/nodes/node_factory.hpp">node_factory.hpp</a></div>
<div class="d4"><span class="tc">└── </span><span class="dn">telemetry/</span></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/aggregator_tcp_server.hpp">aggregator_tcp_server.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/cgroup_memory.hpp">cgroup_memory.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/client_outbox.hpp">client_outbox.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/hwloc_probe.hpp">hwloc_probe.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/hwloc_probe_detail.hpp">hwloc_probe_detail.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/json_serializer.hpp">json_serializer.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/local_transport.hpp">local_transport.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/node_probe.hpp">node_probe.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/process_probe.hpp">process_probe.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/run_id.hpp">run_id.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/scheduler_clock.hpp">scheduler_clock.hpp</a></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/private/impl/telemetry/topology_builder.hpp">topology_builder.hpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">telemetry/</span></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/telemetry/aggregator_tcp_server.cpp">aggregator_tcp_server.cpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/telemetry/hwloc_probe.cpp">hwloc_probe.cpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/telemetry/json_serializer.cpp">json_serializer.cpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/telemetry/local_transport.cpp">local_transport.cpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/telemetry/node_probe.cpp">node_probe.cpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/telemetry/process_probe.cpp">process_probe.cpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/telemetry/telemetry_hub.cpp">telemetry_hub.cpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/telemetry/topology_builder.cpp">topology_builder.cpp</a></div>
<div class="d2"><span class="tc">└── </span><span class="dn">utils/</span></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/utils/logging.cpp">logging.cpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/utils/result.cpp">result.cpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/utils/task_packet.cpp">task_packet.cpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/core/utils/tree.cpp">tree.cpp</a></div>
<div class="d1"><span class="tc">└── </span><span class="dn">mpi/</span> <span class="file-desc">— the MPI component, <code>gempba::mpi</code>; it installs as source, compiled in the consumer's build</span></div>
<div class="d2"><span class="tc">├── </span><span class="dn">cabi/</span></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/mpi/cabi/gempba_mpi.cpp">gempba_mpi.cpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">private/</span> <span class="file-desc">— the MPI component's private headers</span></div>
<div class="d3"><span class="tc">└── </span><span class="dn">impl/</span></div>
<div class="d4"><span class="tc">├── </span><span class="dn">schedulers/</span></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/mpi/private/impl/schedulers/centralized_utils.hpp">centralized_utils.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="../implementations/stats/default-mpi-stats/">default_mpi_stats.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="../implementations/schedulers/centralized/">mpi_centralized_scheduler.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="../implementations/schedulers/semi-centralized/">mpi_semi_centralized_scheduler.hpp</a></div>
<div class="d5"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/mpi/private/impl/schedulers/stop_relay.hpp">stop_relay.hpp</a></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/mpi/private/impl/schedulers/termination_detector.hpp">termination_detector.hpp</a></div>
<div class="d4"><span class="tc">└── </span><span class="dn">telemetry/</span></div>
<div class="d5"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/mpi/private/impl/telemetry/mpi_transport.hpp">mpi_transport.hpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">schedulers/</span></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/mpi/schedulers/mpi_centralized_scheduler.cpp">mpi_centralized_scheduler.cpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/mpi/schedulers/mpi_semi_centralized_scheduler.cpp">mpi_semi_centralized_scheduler.cpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">telemetry/</span></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/mpi/telemetry/mpi_transport.cpp">mpi_transport.cpp</a></div>
<div class="d2"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/mpi/mpi.cpp">mpi.cpp</a></div>

</div>
