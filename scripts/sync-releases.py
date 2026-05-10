#!/usr/bin/env python3
"""Stitch per-version release notes from gempba/docs/releases/ into docs/releases.md.

Env overrides:
  GEMPBA_LOCAL  if set, read from this local folder instead of GitHub
  GEMPBA_REPO   default rapastranac/gempba
  GEMPBA_BRANCH default main
  GITHUB_TOKEN  optional, required for private repos
"""
import json
import os
import re
import urllib.request
from pathlib import Path

LOCAL = os.environ.get("GEMPBA_LOCAL")
REPO = os.environ.get("GEMPBA_REPO", "rapastranac/gempba")
BRANCH = os.environ.get("GEMPBA_BRANCH", "main")
TOKEN = os.environ.get("GITHUB_TOKEN")
SRC_DIR = "docs/releases"
OUT = Path(__file__).resolve().parent.parent / "docs" / "releases.md"


def version_key(name: str) -> tuple[int, int, int]:
    m = re.search(r"v(\d+)\.(\d+)\.(\d+)", name)
    return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)


def fetch(url: str) -> str:
    req = urllib.request.Request(url)
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as r:
        return r.read().decode("utf-8")


def load_entries() -> list[tuple[str, str]]:
    """Return [(name, body), ...] for every release-notes-v*.md in the source."""
    if LOCAL:
        root = Path(LOCAL)
        names = [p.name for p in root.iterdir()
                 if p.name.startswith("release-notes-v") and p.suffix == ".md"]
        return [(n, (root / n).read_text(encoding="utf-8")) for n in names]
    api = f"https://api.github.com/repos/{REPO}/contents/{SRC_DIR}?ref={BRANCH}"
    entries = json.loads(fetch(api))
    return [(e["name"], fetch(e["download_url"])) for e in entries
            if e["name"].startswith("release-notes-v") and e["name"].endswith(".md")]


items = sorted(load_entries(), key=lambda kv: version_key(kv[0]), reverse=True)


def to_collapsible(name: str, body: str, expanded: bool) -> str:
    """Wrap one release file as a pymdownx.details block."""
    m = re.search(r"v\d+\.\d+\.\d+", name)
    version = m.group(0) if m else name
    # strip the file's leading "# vX.Y.Z" heading — the version moves into the summary
    body = re.sub(r"\A#\s+v[\d.]+\s*\n+", "", body)
    indented = "\n".join("    " + ln if ln.strip() else "" for ln in body.rstrip().splitlines())
    marker = "???+" if expanded else "???"
    return f'{marker} note "{version}"\n\n{indented}'


parts = ["# Releases", ""]
for i, (name, body) in enumerate(items):
    parts += [to_collapsible(name, body, expanded=(i == 0)), ""]

OUT.write_text("\n".join(parts), encoding="utf-8")
src = LOCAL if LOCAL else f"{REPO}@{BRANCH}:{SRC_DIR}"
print(f"wrote {OUT} ({len(items)} releases from {src})")
