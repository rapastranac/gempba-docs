# GemPBA Documentation

MkDocs source for the [GemPBA](https://github.com/rapastranac/gempba) documentation
site, hosted at <https://rapastranac.github.io/gempba-docs/>.

## Local preview

The release notes page is stitched from per-version files under
[`docs/releases/`](https://github.com/rapastranac/gempba/tree/main/docs/releases) in
the gempba repo. Sync them before serving:

```bash
python scripts/sync-releases.py
pip install -r requirements.txt
mkdocs serve
```
