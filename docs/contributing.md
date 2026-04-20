# Contributing

## Reporting bugs and proposing features

Open a [GitHub Issue](https://github.com/rapastranac/gempba/issues) on the main repository. Search existing issues
before submitting to avoid duplicates. A good report includes a clear summary of the problem, what behavior you expected
and what you actually observed, and a minimal reproducible example where possible.

## Submitting changes

Fork the repository, create a branch, make your changes, and open a pull request against `main`.

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

If multiple iterations of work are needed on the same issue, append a short description of what that branch specifically
addresses:

```
8-reformat-interface-reference-pages-fix-anchors
```

Create the issue first if one does not exist, then open the branch with its number as the prefix.

### Commits

Keep commits atomic and buildable; each one should leave the project in a working state. Reference the issue number at
the start of the commit message:

```
#8 Reformat node_traits reference to table-driven style
```

Add tests for new functionality and update the documentation where relevant.

### Pull request

Open the PR against `main`. The title should describe what the change does. CI runs automatically on every push to the
branch and when the PR is opened; all checks must pass before merging.

## Coding style

Code style is enforced by **clang-format** and **clang-tidy**, both configured at the repository root.

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
CLANG_FORMAT=clang-format-21 CLANG_TIDY=clang-tidy-18 bash scripts/lint.sh
```

The first time the tidy step runs it configures CMake in `.build-lint/` to produce `compile_commands.json`. Subsequent
runs reuse that directory, so the configuration step is skipped unless you delete it.

## Continuous integration

CI runs on every push to `main` and to branches matching the `{NUMBER}-*` pattern, and on every pull request. The
following pipelines run in parallel:

| Pipeline     | Runner         |
|--------------|----------------|
| Ubuntu 24.04 | `ubuntu-24.04` |
| Windows 2025 | `windows-2025` |
| macOS 26     | `macos-26`     |
| Lint         | `ubuntu-24.04` |

The build pipelines install dependencies (Boost, spdlog, fmt, GoogleTest/GMock, and the platform MPI — OpenMPI on Linux
and macOS, MS-MPI via MSYS2 on Windows), build with CMake and Make, then run the full test suite via CTest. Flaky
tests (prefixed `FLAKY_`) are retried up to three times. A JUnit XML report is published as a workflow artifact after
each run.

The Lint pipeline runs clang-format-21 (format check) and clang-tidy-18 (static analysis) against all first-party
sources.

On a version tag (`v*`) or a pull request, an additional job builds and packages the library:

- **Ubuntu**: produces a `.deb` and publishes it to a GPG-signed APT repository hosted on GitHub Pages
- **Windows**: produces an MSYS2 package (`.pkg.tar.zst`)

## Project structure

See the [File Index](reference/file-index.md) for the full source layout. The top-level directories are:

| Directory         | Contents                                                            |
|-------------------|---------------------------------------------------------------------|
| `include/gempba/` | Public API headers                                                  |
| `private/impl/`   | Built-in implementations, not part of the public API                |
| `src/`            | Translation units                                                   |
| `tests/`          | Unit tests (GoogleTest)                                             |
| `examples/`       | Usage examples for multithreaded and multiprocessing configurations |
| `data/`           | Graph instance files used by the examples and benchmarks            |
| `scripts/`        | Run and benchmark helper scripts for Linux and Windows              |
