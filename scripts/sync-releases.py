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


def demote_headings(body: str) -> str:
    """Convert markdown headings inside a release body to bold labels.

    The stitched page renders each body inside an admonition, but heading
    lines still register as document headings and leak into the site TOC.
    The house style for release sections is **Bold** labels; fenced code
    blocks are left untouched.
    """
    out, in_fence = [], False
    for ln in body.splitlines():
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", ln)
        if m and not in_fence:
            out.append(f"**{m.group(2)}**")
        else:
            out.append(ln)
    return "\n".join(out)


def to_section(name: str, body: str, expanded: bool) -> str:
    """Render one release as a version heading plus a pymdownx.details block.

    The "## vX.Y.Z" heading is what populates the page TOC (one entry per
    version) and gives each release a deep-linkable anchor. The release date
    moves into the admonition title; the GitHub link stays in the body.
    """
    m = re.search(r"v\d+\.\d+\.\d+", name)
    version = m.group(0) if m else name
    # strip the file's leading "# vX.Y.Z" heading — the version moves into the section heading
    body = re.sub(r"\A#\s+v[\d.]+\s*\n+", "", body)
    body = demote_headings(body)
    title = "Release notes"
    lines = body.splitlines()
    if lines:
        dm = re.match(r"<small>(.+?)\s*·\s*(\[GitHub[^\]]*\]\([^)]+\))</small>\s*$", lines[0].strip())
        if dm:
            title = dm.group(1)
            lines[0] = f"<small>{dm.group(2)}</small>"
            body = "\n".join(lines)
    indented = "\n".join("    " + ln if ln.strip() else "" for ln in body.rstrip().splitlines())
    marker = "???+" if expanded else "???"
    return f'## {version}\n\n{marker} note "{title}"\n\n{indented}'


parts = ["# Releases", ""]
for i, (name, body) in enumerate(items):
    parts += [to_section(name, body, expanded=(i == 0)), ""]

OUT.write_text("\n".join(parts), encoding="utf-8")
src = LOCAL if LOCAL else f"{REPO}@{BRANCH}:{SRC_DIR}"
print(f"wrote {OUT} ({len(items)} releases from {src})")
