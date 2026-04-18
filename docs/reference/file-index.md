# File Index

<div class="file-tree">

<div><span class="dn">[root]</span></div>
<div class="d1"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/config.h.in">config.h.in</a> <span class="file-desc">— template for CMake which configures the corresponding <code>config.h</code> file</span></div>

<br>

<div><span class="dn">include/</span></div>

<div class="d1"><span class="tc">└── </span><span class="dn">gempba/</span></div>

<div class="d2"><span class="tc">├── </span><span class="dn">core/</span></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/load-balancer/">load_balancer.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../defaults/node/">node.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/node-core/">node_core.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/node-traits/">node_traits.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/scheduler/">scheduler.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/core/scheduler_traits.hpp">scheduler_traits.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/serial-runnable/">serial_runnable.hpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/core/serializable.hpp">serializable.hpp</a></div>

<div class="d2"><span class="tc">├── </span><span class="dn">defaults/</span></div>
<div class="d3"><span class="tc">└── </span><a href="../implementations/stats-visitors/default-mpi-stats-visitor/">default_mpi_stats_visitor.hpp</a></div>

<div class="d2"><span class="tc">├── </span><span class="dn">detail/</span></div>
<div class="d3"><span class="tc">├── </span><span class="dn">nodes/</span></div>
<div class="d4"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/detail/nodes/node_core_impl.hpp">node_core_impl.hpp</a></div>
<div class="d3"><span class="tc">└── </span><span class="dn">runnables/</span></div>
<div class="d4"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/detail/runnables/serial_runnable_non_void.hpp">serial_runnable_non_void.hpp</a></div>
<div class="d4"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/detail/runnables/serial_runnable_void.hpp">serial_runnable_void.hpp</a></div>

<div class="d2"><span class="tc">├── </span><span class="dn">stats/</span></div>
<div class="d3"><span class="tc">├── </span><a href="../interfaces/stats/">stats.hpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="../interfaces/stats-visitor/">stats_visitor.hpp</a></div>

<div class="d2"><span class="tc">├── </span><span class="dn">utils/</span></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/queue/">Queue.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/utils/gempba_utils.hpp">gempba_utils.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/result/">result.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/score/">score.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/task-bundle/">task_bundle.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/task-packet/">task_packet.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/transmission-guard/">transmission_guard.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../utilities/tree/">tree.hpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/include/gempba/utils/utils.hpp">utils.hpp</a></div>

<div class="d2"><span class="tc">├── </span><a href="../defaults/gempba-hpp/">gempba.hpp</a></div>
<div class="d2"><span class="tc">└── </span><a href="../defaults/node-manager/">node_manager.hpp</a></div>

<br>

<div><span class="dn">private/</span></div>

<div class="d1"><span class="tc">└── </span><span class="dn">impl/</span></div>
<div class="d2"><span class="tc">├── </span><span class="dn">load_balancing/</span></div>
<div class="d3"><span class="tc">├── </span><a href="../implementations/load-balancers/quasi-horizontal/">quasi_horizontal_load_balancer.hpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="../implementations/load-balancers/work-stealing/">work_stealing_load_balancer.hpp</a></div>
<div class="d2"><span class="tc">├── </span><span class="dn">nodes/</span></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/private/impl/nodes/node_factory.hpp">node_factory.hpp</a></div>
<div class="d2"><span class="tc">└── </span><span class="dn">schedulers/</span></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/private/impl/schedulers/centralized_utils.hpp">centralized_utils.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../implementations/stats/default-mpi-stats/">default_mpi_stats.hpp</a></div>
<div class="d3"><span class="tc">├── </span><a href="../implementations/schedulers/centralized/">mpi_centralized_scheduler.hpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="../implementations/schedulers/semi-centralized/">mpi_semi_centralized_scheduler.hpp</a></div>

<br>

<div><span class="dn">src/</span></div>

<div class="d1"><span class="tc">├── </span><span class="dn">gempba/</span></div>
<div class="d2"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/gempba/gempba.cpp">gempba.cpp</a></div>
<div class="d1"><span class="tc">├── </span><span class="dn">schedulers/</span></div>
<div class="d2"><span class="tc">└── </span><span class="dn">mpi/</span></div>
<div class="d3"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/schedulers/mpi/mpi_centralized_scheduler.cpp">mpi_centralized_scheduler.cpp</a></div>
<div class="d3"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/schedulers/mpi/mpi_semi_centralized_scheduler.cpp">mpi_semi_centralized_scheduler.cpp</a></div>
<div class="d1"><span class="tc">└── </span><span class="dn">utils/</span></div>
<div class="d2"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/utils/result.cpp">result.cpp</a></div>
<div class="d2"><span class="tc">├── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/utils/task_packet.cpp">task_packet.cpp</a></div>
<div class="d2"><span class="tc">└── </span><a href="https://github.com/rapastranac/gempba/blob/main/src/utils/tree.cpp">tree.cpp</a></div>

</div>
