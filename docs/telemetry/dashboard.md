# Dashboard

!!! note "Roadmap"
    A first-class web dashboard for GemPBA telemetry is **planned**, and this page is where it will live. The streaming protocol it will consume (the loopback JSON channel and its live control messages) already exists and is stable, so the dashboard is a client on top of an established contract, not a change to the runtime.

## The vision

A browser dashboard that connects to a running GemPBA program (locally or through an SSH tunnel) and renders, in real time:

- **Cluster topology**: hosts, sockets, and the workers pinned to each, drawn from the topology snapshot.
- **Work-flow graph**: a node-link view of the worker-to-worker traffic matrix (`edges_out`), so you can *see* how tasks migrate and where the hot edges are.
- **Live counters**: per-worker task throughput, running tasks, scheduler backlog, and pool idle time; per-host CPU, memory, network, and disk.
- **Interactive control**: dial the emission cadence up or down, or promote a host sentinel, straight from the UI over the existing control channel.

## What works today

Everything the dashboard needs is already on the wire. Until the UI ships, you consume the same stream directly:

- **Live-tail** a run with the bundled scripts (see [Connecting](connecting.md)).
- **Build your own** consumer in any language: open the loopback TCP socket, read newline-delimited JSON, and render. The [Data model](data-model.md) is the full contract, including the client-to-center control messages a custom UI can push back.

Because the dashboard will be just another client of that same socket, anything you build against the stream today keeps working when the official dashboard lands.

## Following along

The dashboard will be developed in the open. Track progress and design discussion on the [GemPBA repository](https://github.com/rapastranac/gempba); this page will be updated with usage instructions and screenshots as it takes shape.
