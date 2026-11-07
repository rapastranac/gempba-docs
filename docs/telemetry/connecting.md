# Connecting to the stream

The aggregator (rank 0) broadcasts telemetry as **line-delimited JSON** over a loopback-only TCP socket (default `127.0.0.1:9000`). Any number of clients can connect and each receives the same stream. This page shows how to tail a local run. To watch a run on another machine, use the [GemPBA Dashboard](dashboard.md), which opens the SSH forward for you, jump host and MFA included.

GemPBA ships one helper script in the gempba repo's [`scripts/`](https://github.com/rapastranac/gempba/tree/main/scripts) directory, in both PowerShell and bash: `telemetry_view` (live-tail). Use the `.ps1` on Windows or the `.sh` on Linux/macOS.

## Local run

While a GemPBA program is running on your machine, tail its stream:

=== "PowerShell"
    ```powershell
    scripts\telemetry_view.ps1             # connects to 127.0.0.1:9000
    scripts\telemetry_view.ps1 -Port 9100  # if the run used a non-default port
    ```
=== "Bash"
    ```bash
    scripts/telemetry_view.sh              # connects to 127.0.0.1:9000
    scripts/telemetry_view.sh --port 9100  # if the run used a non-default port
    ```

`telemetry_view` prints **one row per rank**, each tagged with its role (coordinator or worker) and refreshed in place every interval: that rank's task counters, running tasks, thread count, CPU % and resident memory. While the run is paused it marks the paused stretch rather than blanking, and it prints each run marker as it arrives. The bash version shows times on macOS too. For the full payload (topology, the run setup and every per-rank field), pass `-Raw` / `--raw` to print pretty JSON instead.

!!! tip "Use `127.0.0.1`, not `localhost`"
    The aggregator binds IPv4 loopback. On Windows, `localhost` may resolve to IPv6 (`::1`) first and fail to connect, so always target `127.0.0.1`.

## Remote run

Reaching a run on another machine is the dashboard's job. The [GemPBA Dashboard](dashboard.md) opens the SSH forward itself, including the jump-host hop and the MFA prompt, with no scripts to run and no port to forward by hand. See the dashboard's [Connect](dashboard.md#connect) section for the direct-host and jump-host setups.

## Custom clients

Nothing about the protocol is tied to the helper script; it is just newline-delimited JSON on a TCP socket. Any language that can open a socket and split on newlines can consume it, or you can tail it by hand:

```bash
nc 127.0.0.1 9000          # or: socat - TCP:127.0.0.1:9000
nc 127.0.0.1 9000 | jq .   # pretty-print each frame
```

To consume a remote run from your own client, forward the port over SSH first (`ssh -L 9000:127.0.0.1:9000 user@host`, adding `-J user@login-node` for a jump host), then connect locally.

The [Data model](data-model.md) covers the JSON shape at a glance, and gempba's [`docs/telemetry/wire-format.md`](https://github.com/rapastranac/gempba/blob/main/docs/telemetry/wire-format.md) is the full field reference a custom consumer parses.
