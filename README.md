# obs-network-tools

Autonomous OBS packaging pipeline for network tools not commonly packaged by Linux distributions.

## Project Purpose

This repository contains OBS (Open Build Service) package definitions for various network diagnostic and benchmarking tools. Packages are built automatically when upstream releases a new version (via GitHub tags), and published to distribution repositories for easy installation via native package managers.

**OBS Project:** https://build.opensuse.org/project/show/home:ciriarte:network-tools

---

## Packages

| Package  | Description                                           | Upstream                                    |
|----------|-------------------------------------------------------|---------------------------------------------|
| nic-xray | Ethernet physical connectivity diagnostic tool        | https://github.com/ciroiriarte/nic-xray     |
| ttl      | Traceroute/mtr-style TUI (requires Rust ≥ 1.88)      | https://github.com/lance0/ttl               |
| xfr      | Network bandwidth testing TUI (requires Rust ≥ 1.88) | https://github.com/lance0/xfr               |

---

## Distributions Covered

| Distribution        | Repository alias    | Arch            | nic-xray | ttl | xfr |
|---------------------|---------------------|-----------------|----------|-----|-----|
| openSUSE Tumbleweed | openSUSE_Tumbleweed | x86_64, aarch64 | ✓        | ✓   | ✓   |
| openSUSE Slowroll   | openSUSE_Slowroll   | x86_64, aarch64 | ✓        | ✓   | ✓   |
| openSUSE Leap 16.0  | openSUSE_Leap_16.0  | x86_64, aarch64 | ✓        | ✓   | ✓   |
| openSUSE Leap 15.6  | openSUSE_Leap_15.6  | x86_64, aarch64 | ✓        | ✗ ¹ | ✗ ¹ |
| Rocky Linux 9       | Rocky_9             | x86_64, aarch64 | ✓        | ✓   | ✓   |
| Rocky Linux 10      | Rocky_10            | x86_64, aarch64 | ✓        | ✓   | ✓   |
| Ubuntu 22.04 LTS    | Ubuntu_22.04        | x86_64, aarch64 | ✓        | ✗ ¹ | ✗ ¹ |
| Ubuntu 24.04 LTS    | Ubuntu_24.04        | x86_64, aarch64 | ✓        | ✗ ¹ | ✗ ¹ |

¹ Requires Rust ≥ 1.88, which is not yet available in this distribution's standard
  repositories. Builds will automatically succeed once the distribution ships a
  compatible Rust version.

---

## Installing Packages

### openSUSE (zypper)

```bash
zypper addrepo https://download.opensuse.org/repositories/home:/ciriarte:/network-tools/openSUSE_Tumbleweed/ obs-network-tools
zypper refresh
zypper install nic-xray ttl xfr
```

Replace `openSUSE_Tumbleweed` with your distribution alias from the table above.

### Ubuntu (apt)

```bash
echo "deb https://download.opensuse.org/repositories/home:/ciriarte:/network-tools/Ubuntu_24.04/ ./" \
  | sudo tee /etc/apt/sources.list.d/obs-network-tools.list
curl -fsSL "https://download.opensuse.org/repositories/home:/ciriarte:/network-tools/Ubuntu_24.04/Release.key" \
  | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/obs-network-tools.gpg
sudo apt update
sudo apt install nic-xray
```

Replace `Ubuntu_24.04` with `Ubuntu_22.04` for Ubuntu 22.04 LTS.

> **Note:** `ttl` and `xfr` are not available on Ubuntu (Rust ≥ 1.88 not yet in distro repos).

### Rocky Linux (dnf)

```bash
dnf config-manager --add-repo \
  https://download.opensuse.org/repositories/home:/ciriarte:/network-tools/Rocky_9/home:ciriarte:network-tools.repo
dnf install nic-xray ttl xfr
```

Replace `Rocky_9` with `Rocky_10` for Rocky Linux 10.

> **Note for Rocky Linux:** `lldpd` is available via EPEL. Enable it before installing `nic-xray`:
> ```bash
> dnf install epel-release
> ```

---

## Prerequisites (for maintainers)

Install and configure the `osc` CLI client:

```bash
# openSUSE
zypper install osc

# Ubuntu/Debian
apt install osc

# Configure credentials
osc config https://api.opensuse.org
# Enter your OBS username and password when prompted
```

---

## Repository Structure

```
obs-network-tools/
├── CLAUDE.md                       # Project instructions for Claude Code
├── README.md                       # This file
├── .github/workflows/
│   ├── update-nic-xray.yml         # Daily: detect new tag, update changelogs, push to OBS
│   ├── update-ttl.yml              # Daily: detect new tag, vendor deps, rebuild tarballs, push to OBS
│   └── update-xfr.yml              # Daily: detect new tag, vendor deps, rebuild tarballs, push to OBS
├── scripts/
│   └── update-nic-xray-version.sh  # Manual alternative to the nic-xray workflow above
└── packages/
    ├── nic-xray/
    │   ├── _service           # tar_scm: fetch pinned tag from github.com/ciroiriarte/nic-xray
    │   ├── nic-xray.spec      # RPM spec (openSUSE + Rocky Linux)
    │   ├── nic-xray.changes   # openSUSE changelog
    │   ├── nic-xray.dsc       # Debian source package descriptor
    │   ├── debian.control     # Debian/Ubuntu package metadata
    │   ├── debian.changelog   # Debian/Ubuntu changelog
    │   └── debian.rules       # Debian build rules
    ├── ttl/
    │   ├── _service           # cargo_vendor (manual mode, documents vendoring requirement)
    │   ├── ttl-0.19.0.tar.gz  # Source tarball (committed)
    │   ├── vendor.tar.zst     # Vendored Rust dependencies (includes .cargo/config.toml)
    │   ├── ttl.spec           # RPM spec (openSUSE + Rocky Linux)
    │   ├── ttl.changes        # openSUSE changelog
    │   ├── ttl.dsc            # Debian source package descriptor
    │   ├── debian.control     # Debian/Ubuntu package metadata
    │   ├── debian.changelog   # Debian/Ubuntu changelog
    │   ├── debian.rules       # Debian build rules
    │   └── debian.postinst    # Post-install: setcap cap_net_raw+ep
    └── xfr/
        ├── _service           # cargo_vendor (manual mode, documents vendoring requirement)
        ├── xfr-0.8.0.tar.gz   # Source tarball (committed)
        ├── vendor.tar.zst     # Vendored Rust dependencies (includes .cargo/config.toml)
        ├── xfr.spec           # RPM spec (openSUSE + Rocky Linux)
        ├── xfr.changes        # openSUSE changelog
        ├── xfr.dsc            # Debian source package descriptor
        ├── debian.control     # Debian/Ubuntu package metadata
        ├── debian.changelog   # Debian/Ubuntu changelog
        └── debian.rules       # Debian build rules
```

---

## OBS Project Setup (one-time)

Create the OBS project and configure repositories via `osc`:

```bash
osc meta prj -e home:ciriarte:network-tools
```

Use the following project metadata XML:

```xml
<project name="home:ciriarte:network-tools">
  <title>Network Tools</title>
  <description>Packaging pipeline for network diagnostic and benchmarking tools</description>
  <person userid="ciriarte" role="maintainer"/>
  <repository name="openSUSE_Tumbleweed">
    <path project="openSUSE:Factory" repository="snapshot"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
  <repository name="openSUSE_Slowroll">
    <path project="openSUSE:Slowroll" repository="standard"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
  <repository name="openSUSE_Leap_16.0">
    <!-- devel:languages:rust provides Rust >= 1.88 for ttl and xfr -->
    <path project="devel:languages:rust" repository="16.0"/>
    <path project="openSUSE:Leap:16.0" repository="standard"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
  <repository name="openSUSE_Leap_15.6">
    <path project="devel:languages:rust" repository="15.6"/>
    <path project="openSUSE:Leap:15.6" repository="standard"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
  <repository name="Rocky_9">
    <path project="RockyLinux:9" repository="standard"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
  <repository name="Rocky_10">
    <path project="RockyLinux:10" repository="standard"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
  <repository name="Ubuntu_22.04">
    <path project="Ubuntu:22.04" repository="standard"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
  <repository name="Ubuntu_24.04">
    <path project="Ubuntu:24.04" repository="standard"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
</project>
```

---

## Deploying Package Changes to OBS

### First-time setup (any package)

```bash
osc co home:ciriarte:network-tools
mkdir -p home:ciriarte:network-tools/<package>
cp packages/<package>/* home:ciriarte:network-tools/<package>/
cd home:ciriarte:network-tools/<package>
osc add *
osc commit -m "Initial package"
```

### Updating an existing package

```bash
cd home:ciriarte:network-tools/<package>
osc up
cp /path/to/obs-network-tools/packages/<package>/* .
osc commit -m "Update to version X.Y"
```

### ttl and xfr version bumps (Rust packages)

Version updates are handled automatically by the GitHub Actions workflows. To trigger
an update immediately without waiting for the daily schedule, run the workflow manually
from the Actions tab in GitHub.

For a fully manual update (e.g., on a machine without GitHub Actions), the steps are:

```bash
# Example: updating ttl to v0.20.0
git clone --branch v0.20.0 https://github.com/lance0/ttl ttl-src
cd ttl-src && cargo vendor
mkdir -p .cargo
printf '[source.crates-io]\nreplace-with = "vendored-sources"\n\n[source.vendored-sources]\ndirectory = "vendor"\n' \
  > .cargo/config.toml
cd ..
tar -czf ttl-0.20.0.tar.gz --exclude='.git' --exclude='vendor' \
  --transform='s|^ttl-src|ttl-0.20.0|' ttl-src/
tar -I "zstd" -cf vendor.tar.zst -C ttl-src .cargo/config.toml vendor/
cp ttl-0.20.0.tar.gz vendor.tar.zst packages/ttl/
# Then update ttl.spec (Version, %changelog), ttl.dsc, ttl.changes, debian.changelog
# and commit to git + OBS
```

The same pattern applies to `xfr` (substitute `xfr` and `github.com/lance0/xfr`).

---

## How Auto-Rebuild Works

### nic-xray (fully autonomous)

**OBS source service (`_service`)**: On every OBS commit, OBS automatically:
1. **Fetches source** — `tar_scm` clones the pinned tag (`revision`) from `github.com/ciroiriarte/nic-xray`.
2. **Packages the source** — `recompress` produces a `.tar.gz` archive.
3. **Injects the version** — `set_version` propagates the version into the spec and `.dsc` files.
4. **Rebuilds and publishes** — Packages are built for all configured distributions.

**GitHub Actions workflow** (`.github/workflows/update-nic-xray.yml`) runs daily at 06:00 UTC:
1. Queries the GitHub releases API for the latest tag on `ciroiriarte/nic-xray`.
2. Compares with the current version in `nic-xray.changes`.
3. If changed: updates `_service` (`version` and `revision`), `nic-xray.changes`, and `debian.changelog`.
4. Commits to this repo and pushes the updated files to OBS, triggering a rebuild.

When a new tag is pushed to `github.com/ciroiriarte/nic-xray`, the pipeline picks it up within 24 hours with no manual steps required.

### ttl and xfr (fully autonomous)

Rust packages require pre-committed source and vendor tarballs because OBS build workers
have no internet access. The GitHub Actions workflows handle this automatically:

**GitHub Actions workflows** (`.github/workflows/update-ttl.yml` / `update-xfr.yml`) run daily:
1. Query the GitHub releases/tags API for the latest version on `lance0/ttl` or `lance0/xfr`.
2. Compare with the current version in `ttl.changes` / `xfr.changes`.
3. If changed: install Rust, clone at the new tag, run `cargo vendor`.
4. Build the source tarball (`ttl-X.Y.Z.tar.gz`) and vendor archive (`vendor.tar.zst`).
5. Update spec `Version:`, `%changelog`, `.dsc`, `.changes`, and `debian.changelog`.
6. Commit all changes to this repo and push updated files to OBS, triggering a rebuild.

When a new tag is pushed to `github.com/lance0/ttl` or `github.com/lance0/xfr`, the pipeline
picks it up within 24 hours with no manual steps required.

The `_service` file in each Rust package documents the vendoring requirement; it runs no
server-side OBS logic but is required for the build scheduler to dispatch jobs correctly.

### Required GitHub secrets

Add these secrets to this repository (Settings → Secrets → Actions):

| Secret         | Value                               |
|----------------|-------------------------------------|
| `OBS_PASSWORD` | OBS account password for `ciriarte` |

### Manual version update for nic-xray

To update immediately instead of waiting for the daily schedule:

```bash
# Update locally and push to OBS
./scripts/update-nic-xray-version.sh --push
```

For ttl or xfr, trigger the corresponding GitHub Actions workflow manually from the Actions tab.

---

## Verification

After pushing to OBS, verify the builds:

```bash
# Check build results
osc results home:ciriarte:network-tools nic-xray
osc results home:ciriarte:network-tools ttl
osc results home:ciriarte:network-tools xfr

# Watch live build log (example: Tumbleweed x86_64)
osc buildlog home:ciriarte:network-tools nic-xray openSUSE_Tumbleweed x86_64
```

On each installed system:

```bash
# RPM (openSUSE / Rocky Linux)
rpm -qi nic-xray

# Deb (Ubuntu)
dpkg -s nic-xray

# Functional tests
sudo nic-xray
ttl --help
xfr --help
```
