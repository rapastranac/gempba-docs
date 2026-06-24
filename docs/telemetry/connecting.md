# Connecting to the stream

The center role broadcasts telemetry as **line-delimited JSON** over a loopback-only TCP socket (default `127.0.0.1:9000`). Any number of clients can connect and each receives the same stream. This page shows how to tail it locally and how to reach a remote rank.

GemPBA ships two helper scripts in the gempba repo's [`scripts/`](https://github.com/rapastranac/gempba/tree/main/scripts) directory, in both PowerShell and bash: `telemetry_view` (live-tail) and `telemetry_tunnel` (SSH tunnel plus tail). Use the `.ps1` on Windows or the `.sh` on Linux/macOS; they share the same workflow.

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

You get one formatted line per broadcast: time, elapsed, local/remote task counts, thread count, CPU %, RSS. For the full payload (topology and per-host fields included), pass `-Raw` / `--raw` to print pretty JSON instead.

!!! tip "Use `127.0.0.1`, not `localhost`"
    The center binds IPv4 loopback. On Windows, `localhost` may resolve to IPv6 (`::1`) first and fail to connect, so always target `127.0.0.1`.

## Remote run (SSH tunnel)

!!! tip "Prefer a GUI?"
    The [GemPBA Dashboard](dashboard.md) does all of this for you, including the jump-host hop and MFA, with no scripts. The `telemetry_tunnel` / `telemetry_view` helpers below are the headless path, for a terminal tail or a custom consumer.

Because the socket is loopback-only, you reach a remote rank by forwarding the port over SSH. `telemetry_tunnel` wraps the whole open-tunnel, wait, tail flow into one command and hands off to `telemetry_view`.

**Direct host** (a LAN box or anything you can `ssh` into):

=== "PowerShell"
    ```powershell
    scripts\telemetry_tunnel.ps1 -SshHost me@my-server
    ```
=== "Bash"
    ```bash
    scripts/telemetry_tunnel.sh --ssh-host me@my-server
    ```

**Through a jump host** (a cluster login/bastion node in front of the compute node running gempba). Pass the compute node running **rank 0** as the SSH host, with the login node as the jump host:

=== "PowerShell"
    ```powershell
    scripts\telemetry_tunnel.ps1 -SshHost me@compute-node -JumpHost me@login-node
    ```
=== "Bash"
    ```bash
    scripts/telemetry_tunnel.sh --ssh-host me@compute-node --jump-host me@login-node
    ```

!!! tip "Which host is rank 0?"
    You do not have to guess. The center (rank 0) prints its host the moment telemetry comes up:

    ```
    [2026-06-16 14:07:35.976] [info] telemetry listening on 127.0.0.1:9000 on host cn042
    ```

    The name after `on host` (here `cn042`) is what you pass as the SSH host. Where that line shows up depends on how the run was launched:

    - **Locally**: in your console, right there in the prompt. The center is your own machine, so you usually do not need a tunnel at all.
    - **SLURM**: in the job's stdout file (`slurm-<jobid>.out`, or whatever `--output` you set); `cat` it on the login node.
    - **Other launchers**: wherever that scheduler collects the job's stdout.

Jump-host mode **nests** the tunnel rather than using SSH `ProxyJump`: it forwards to the login node, then opens the final hop *from* the login node, so it rides the cluster's intra-cluster trust and works even when the login node enforces MFA (one prompt there, no compute-node password). The per-job compute-node host key is auto-trusted (`accept-new`). Full rationale: gempba's [`docs/remote-connection.md`](https://github.com/rapastranac/gempba/blob/main/docs/remote-connection.md).

Both ports default to 9000 (`-LocalPort` / `-RemotePort`, or `--local-port` / `--remote-port`); match the remote port to the one the run bound. Ctrl+C tears the tunnel down.

## Custom clients

Nothing about the protocol is tied to the helper scripts; it is just newline-delimited JSON on a TCP socket. Any language that can open a socket and split on newlines can consume it, or you can tail it by hand:

```bash
# Local
nc 127.0.0.1 9000        # or: socat - TCP:127.0.0.1:9000

# Remote: forward the port first, then connect locally
ssh -L 9000:127.0.0.1:9000 user@host    # add -J user@login for a jump host
nc 127.0.0.1 9000 | jq .                # pretty-print each frame
```

See the [Data model](data-model.md) for the JSON shape, which is exactly what a custom dashboard would parse.
