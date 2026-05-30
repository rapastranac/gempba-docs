# Installation (Maven)

GemPBA's JARs are published to [GitHub Packages](https://github.com/rapastranac/gempba/packages/3043052), one fat JAR per flavor classifier: `mt` (multithreading) and `mp-mpi` (multiprocessing — requires an MPI runtime on the host).

!!! info "Available from `v4.1.0`"
    Earlier tags predate the publish flow and have no artifact on the registry.

## Requirements

- **JDK 25**
- **Maven 3.9+**
- For the `mp-mpi` classifier only: an MPI runtime on the host (MS-MPI / OpenMPI / MPICH)

## 1. Add the registry

Declare the GitHub Packages repository in your `pom.xml`:

```xml
<repositories>
  <repository>
    <id>github-gempba</id>
    <url>https://maven.pkg.github.com/rapastranac/gempba</url>
  </repository>
</repositories>
```

## 2. Authenticate

GitHub Packages requires a token even for public packages. Create a Personal Access Token at [github.com/settings/tokens](https://github.com/settings/tokens) with the **`read:packages`** scope, then add it to `~/.m2/settings.xml`:

```xml
<settings>
  <servers>
    <server>
      <id>github-gempba</id>
      <username>YOUR_GITHUB_USERNAME</username>
      <password>YOUR_PAT</password>
    </server>
  </servers>
</settings>
```

The server `<id>` **must** match the repository `<id>` from step 1 (`github-gempba`).

## 3. Declare the dependency

Pick the classifier for the flavor you want:

```xml
<dependency>
  <groupId>io.gempba</groupId>
  <artifactId>gempba</artifactId>
  <version>VERSION</version>
  <classifier>mt</classifier>          <!-- or mp-mpi -->
</dependency>
```

That's it — no platform-specific profiles or OS classifiers. The fat JAR carries every supported OS's native binary and the loader picks the right one at runtime.

## 4. Build

```bash
mvn install
```

!!! tip "Resolving from a fork or mirror"
    The [gempba-java-examples](https://github.com/rapastranac/gempba-java-examples) parent POM resolves `io.gempba:gempba` from `rapastranac/gempba` by default. To point at a fork or org mirror without editing the POM, override the owner property: `mvn install -Dgempba.github.owner=my-org` (or set `gempba.github.owner` in a `settings.xml` profile).

## Next

Head to the [Quick Start](quick-start.md) for a complete working program.
