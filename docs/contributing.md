# Contributing

## Reporting bugs and proposing features

Open a [GitHub Issue](https://github.com/rapastranac/gempba/issues) on the main repository. Search existing issues
before submitting to avoid duplicates. A good report includes a clear summary of the problem, what behavior you expected
and what you actually observed, and a minimal reproducible example where possible.

## Submitting changes

Pull the latest `main` before creating a branch. Fork the repository, create a branch, make your changes, and open a
pull request against `main`.

### Branch naming

Every branch must be tied to an issue. The branch name is derived directly from the issue title, converted to kebab-case
and prefixed with the issue number:

```
{issue-number}-{issue-title-in-kebab-case}
```

For example, an issue numbered 8 titled *"Reformat interface reference pages"* becomes:

```
8-reformat-interface-reference-pages
```

If multiple iterations of work are needed on the same issue, append a double dash followed by a short description of
what that iteration specifically addresses:

```
8-reformat-interface-reference-pages--fix-anchors
```

Create the issue first if one does not exist, then open the branch with its number as the prefix.

### Commits

Keep commits atomic — one logical unit per commit, never bundling unrelated changes. Every commit must leave the project
in a working state. Reference the issue number at the start of the commit message:

```
#8 Reformat node_traits reference to table-driven style
```

For multi-change commits, add a blank line after the title and describe each change as a bullet:

```
#8 Reformat node_traits reference to table-driven style

- Replace prose description with a two-column table
- Add anchor for each trait entry
```

Skip the body entirely for single-change commits.

If a bug is introduced in the current unmerged branch, fold the fix back into the commit that introduced it — do not add
a follow-up "fix" commit.

Add tests for new functionality and update the documentation where relevant.

### Pull request

Open the PR against `main`. The PR title must match the issue title verbatim. If the branch covers a specific iteration,
append an em-dash and a short iteration summary:

```
Reformat interface reference pages — fix anchors
```

CI runs automatically on every push to the branch and when the PR is opened; all checks must pass before merging. The
default merge strategy is a merge commit — do not squash or rebase.

Use the following structure for the PR description (omit **Tests** if there are none):

```
**Problem**
- What was broken or missing.

**Fix / Solution**
- What was changed and why (at the decision level, not line-by-line).

**Tests**
- What was tested and how.
```

## Coding style

Avoid code comments by default. A comment is only justified when the *why* cannot be inferred from the code itself: a
hidden constraint, a platform quirk, a non-obvious invariant, or a deliberate workaround. Never narrate what the code
does — well-named identifiers already do that. Rationale for workarounds or platform-specific decisions belongs in the
commit body or PR description.

Code style is also enforced by **clang-format** and **clang-tidy**, both configured at the repository root.

### Formatting (`.clang-format`)

Based on the LLVM style with the following key settings:

| Setting                           | Value                                      |
|-----------------------------------|--------------------------------------------|
| `IndentWidth`                     | 4                                          |
| `ColumnLimit`                     | 190                                        |
| `NamespaceIndentation`            | All                                        |
| `BreakBeforeBraces`               | Custom (Attach style)                      |
| `AlwaysBreakTemplateDeclarations` | Yes                                        |
| Include order                     | System headers first, then project headers |

Run clang-format before committing:

```bash
clang-format -i <file>
```

### Naming conventions (`.clang-tidy`)

All identifiers use `lower_case` except where noted:

| Identifier kind        | Case         | Prefix |
|------------------------|--------------|--------|
| Classes and structs    | `lower_case` |        |
| Functions              | `lower_case` |        |
| Parameters             | `lower_case` | `p_`   |
| Local variables        | `lower_case` | `v_`   |
| Member variables       | `lower_case` | `m_`   |
| Static local variables | `lower_case` | `v_`   |
| Enum constants         | `UPPER_CASE` |        |
| Macros                 | `UPPER_CASE` |        |

Short loop indices (`i`, `j`, `k`, `idx`, `it`, `iter`) are exempt from the `v_` prefix rule.

### Active check categories

The clang-tidy configuration enables a focused subset of checks:

- `bugprone-*` for common bug patterns, with a targeted exclusion list
- `modernize-*` for C++17/20 idioms (trailing return types and a few others are excluded)
- `performance-*` for performance anti-patterns
- `readability-*` for identifier naming, redundant code, and general clarity
- Selected rules from `cert-*`, `cppcoreguidelines-*`, `misc-*`, and `hicpp-*`

## Running lint locally

The repository ships a `scripts/lint.sh` helper that runs the same checks CI does. You need `clang-format` and
`clang-tidy` installed, plus CMake and the project dependencies so that a build can be configured to generate
`compile_commands.json`.

### Basic usage

```bash
# Run both clang-format (check) and clang-tidy
bash scripts/lint.sh

# Check formatting only
bash scripts/lint.sh --format-only

# Run static analysis only
bash scripts/lint.sh --tidy-only

# Apply clang-format changes and clang-tidy fixes in place
bash scripts/lint.sh --fix

# Control parallelism (defaults to nproc)
bash scripts/lint.sh --jobs 4
```

### Environment overrides

If your system has versioned binaries (e.g. `clang-format-21`), the script picks the highest available version
automatically. You can also pin them explicitly:

| Variable         | Default                        | Purpose                                           |
|------------------|--------------------------------|---------------------------------------------------|
| `CLANG_FORMAT`   | auto-detected `clang-format`   | Path to the clang-format binary                   |
| `CLANG_TIDY`     | auto-detected `clang-tidy`     | Path to the clang-tidy binary                     |
| `RUN_CLANG_TIDY` | auto-detected `run-clang-tidy` | Path to the run-clang-tidy helper                 |
| `BUILD_DIR`      | `<repo>/.build-lint`           | CMake build directory for `compile_commands.json` |

```bash
CLANG_FORMAT=clang-format-22 CLANG_TIDY=clang-tidy-22 bash scripts/lint.sh
```

The first time the tidy step runs it configures CMake in `.build-lint/` to produce `compile_commands.json`. Subsequent
runs reuse that directory, so the configuration step is skipped unless you delete it.

## Continuous integration

Workflows are split by trigger: `ci-*.yml` runs on pull requests and on pushes to `main` / branches matching the
`{NUMBER}-*` pattern, while `release-*.yml` runs on version tags (`v*`). Reusable building blocks (`_build-*.yml`) are
shared so the tag-time publish reuses the exact build path CI exercises. The CI pipelines run in parallel:

| Pipeline     | Runner         |
|--------------|----------------|
| Ubuntu 24.04 | `ubuntu-24.04` |
| Windows 2025 | `windows-2025` |
| macOS 26     | `macos-26`     |
| Java         | `ubuntu-24.04` |
| Lint         | `ubuntu-24.04` |

The C++ build pipelines install dependencies (hwloc, Boost, spdlog, fmt, GoogleTest/GMock, and the platform MPI —
OpenMPI on Linux and macOS, MS-MPI via MSYS2 on Windows), build with CMake across the `multiprocessing: [ON, OFF]`
matrix, then run the full test suite via CTest. Each PR also builds the [gempba-examples](https://github.com/rapastranac/gempba-examples)
tree against the freshly built library, so the install / `gempbaConfig.cmake` / exported-headers chain is exercised on
every change. Flaky tests (prefixed `FLAKY_`) are retried up to three times. A JUnit XML report is published as a
workflow artifact after each run.

The Lint pipeline runs clang-format-22 (format check) and clang-tidy-22 (static analysis) against all first-party
sources.

On a version tag (`v*`), the `release-*.yml` workflows build and publish packages for every flavor and platform:

- **Ubuntu**: `.deb` packages (`libgempba-dev`, `libgempba-mpi-dev`) published to a GPG-signed APT repository on GitHub Pages
- **Windows**: MSYS2 packages (`.pkg.tar.zst`) attached to the GitHub Release
- **macOS**: Homebrew formulae (`gempba`, `gempba-mpi`) pushed to the project's tap — built and `brew test`-ed on a real macOS runner first, so a non-installable formula blocks the release
- **Java**: fat JARs (`mt`, `mp-mpi` classifiers) published to GitHub Packages

## Project structure

See the [File Index](reference/file-index.md) for the full source layout. The top-level directories are:

| Directory         | Contents                                                            |
|-------------------|---------------------------------------------------------------------|
| `include/gempba/` | Public API headers                                                  |
| `private/impl/`   | Built-in implementations, not part of the public API                |
| `src/`            | Translation units                                                   |
| `tests/`          | Unit tests (GoogleTest)                                             |
| `bindings/`       | Non-C++ bindings — the stable C ABI (`jni/`) and the Java JNI layer (`java/`) |
| `packaging/`      | Packaging manifests (MSYS2 `PKGBUILD`, Homebrew formulae, `.deb` control) |
| `scripts/`        | Build, lint, telemetry, and JAR-build helper scripts                |

Runnable examples and their graph instance data now live in the sibling
[gempba-examples](https://github.com/rapastranac/gempba-examples) repository, not in this tree.
