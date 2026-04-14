# GemPBA

[![C/C++ CI (Ubuntu 24.04)](https://github.com/rapastranac/gempba/actions/workflows/c-cpp-ubuntu.yml/badge.svg)](https://github.com/rapastranac/gempba/actions/workflows/c-cpp-ubuntu.yml)
[![C/C++ CI (Windows 2022)](https://github.com/rapastranac/gempba/actions/workflows/c-cpp-windows.yml/badge.svg)](https://github.com/rapastranac/gempba/actions/workflows/c-cpp-windows.yml)
![GitHub License](https://img.shields.io/github/license/rapastranac/gempba)
![GitHub Release](https://img.shields.io/github/v/release/rapastranac/gempba)

**GemPBA** is a hybrid parallelization framework for branching algorithms. It supports:

- **Multithreading** — multiple worker threads within a single process
- **Multiprocessing** — work distributed across multiple processes (OpenMPI by default, but pluggable)
- **Hybrid** — multiple threads per process, spread across multiple nodes

There are two main research contributions baked into the framework.

The first is the **Quasi-Horizontal Load Balancing** strategy. Standard work-stealing treats all pending tasks equally. Quasi-horizontal balancing understands the shape of your recursion tree and selects work near the root, where each task will spawn the most downstream work. For branching algorithms where subtree sizes vary dramatically, this makes a significant difference in CPU utilization.

The second is the **Semi-Centralized Scheduler**. Distributing work across processes sounds straightforward until you hit the rejected task problem: a worker receives a task, but by the time it arrives the worker is already busy and has to bounce it back to the sender. Do this naively and you spend more time rerouting work than doing it. The semi-centralized design avoids this by keeping a lightweight center that never holds tasks itself but maintains global priority awareness. The center always knows which worker is idle and routes tasks directly there, eliminating the bounce-back problem without becoming a bottleneck.

For the full performance analysis and formal description, see:

- [MSc. Thesis](http://hdl.handle.net/11143/18687)
- [Paper in Parallel Computing](https://doi.org/10.1016/j.parco.2023.103024)

## Platforms

- Linux
- Windows

## Requirements

| Dependency | Version | Notes |
|---|---|---|
| C++ compiler | C++23 | GCC 13+, Clang 17+, MSVC 19.38+ |
| CMake | ≥ 3.28 | |
| OpenMPI | ≥ 4.0 | Only for multiprocessing support |
| Boost | any recent | Optional — examples and tests only |
| GoogleTest | any recent | Optional — running tests only |
