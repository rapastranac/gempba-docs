# Connecting to the stream

The center role broadcasts telemetry as **line-delimited JSON** over a loopback-only TCP socket (default `127.0.0.1:9000`). Any number of clients can connect and each receives the same stream. This page shows how to tail it locally and how to reach a remote rank.

GemPBA ships two PowerShell helpers, `telemetry_view.ps1` and `telemetry_tunnel.ps1`, in the gempba repo's [`scripts/`](https://github.com/rapastranac/gempba/tree/main/scripts) directory.

## Local run

While a GemPBA program is running on your machine, tail its stream:

```powershell
scripts\telemetry_view.ps1            # connects to 127.0.0.1:9000
scripts\telemetry_view.ps1 -Port 9100 # if the run used a non-default port
```

You get one formatted line per broadcast: time, elapsed, local/remote task counts, thread count, CPU %, RSS. For the full payload (topology and per-host fields included), pass `-Raw` to print pretty JSON instead:

```powershell
scripts\telemetry_view.ps1 -Raw
```

!!! tip "Use `127.0.0.1`, not `localhost`"
    The center binds IPv4 loopback. On Windows, `localhost` may resolve to IPv6 (`::1`) first and fail to connect, so always target `127.0.0.1`.

## Remote run (SSH tunnel)

Because the socket is loopback-only, you reach a remote rank by forwarding the port over SSH. `telemetry_tunnel.ps1` wraps the whole "open tunnel → wait → tail" flow into one command, then hands off to `telemetry_view.ps1`.

**Direct host** (a LAN box or anything you can `ssh` into):

```powershell
scripts\telemetry_tunnel.ps1 -SshHost me@my-server
```

**Through a jump host** (e.g. a cluster login/bastion node in front of the compute node running gempba). Find the node running **rank 0** yourself first (`squeue` on the login node, the first host in your job's node list), then pass it as `-SshHost` with the login node as `-JumpHost`:

```powershell
scripts\telemetry_tunnel.ps1 -SshHost me@compute-node -JumpHost me@login-node
```

Both accept `-LocalPort` / `-RemotePort` (default 9000 each); match `-RemotePort` to the port the run actually bound. Tearing the script down (Ctrl+C) closes the tunnel.

## Non-Windows / custom clients

The helpers are PowerShell, but nothing about the protocol is; it is just newline-delimited JSON on a TCP socket. From Linux/macOS you can reproduce the same thing by hand:

```bash
# Local
nc 127.0.0.1 9000        # or: socat - TCP:127.0.0.1:9000

# Remote: forward the port first, then connect locally
ssh -L 9000:127.0.0.1:9000 user@host    # add -J user@login for a jump host
nc 127.0.0.1 9000 | jq .                # pretty-print each frame
```

Any language that can open a TCP socket and split on newlines can consume the stream. See the [Data model](data-model.md) for the JSON shape, which is exactly what a custom dashboard would parse.
