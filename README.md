# obs-network-tools

[![update-nic-xray](https://github.com/ciroiriarte/obs-network-tools/actions/workflows/update-nic-xray.yml/badge.svg)](https://github.com/ciroiriarte/obs-network-tools/actions/workflows/update-nic-xray.yml)
[![update-ttl](https://github.com/ciroiriarte/obs-network-tools/actions/workflows/update-ttl.yml/badge.svg)](https://github.com/ciroiriarte/obs-network-tools/actions/workflows/update-ttl.yml)
[![update-xfr](https://github.com/ciroiriarte/obs-network-tools/actions/workflows/update-xfr.yml/badge.svg)](https://github.com/ciroiriarte/obs-network-tools/actions/workflows/update-xfr.yml)

Autonomous [OBS](https://build.opensuse.org/project/show/home:ciriarte:network-tools) packaging pipeline for network diagnostic and benchmarking tools not commonly packaged by Linux distributions. Packages are built and published automatically when upstream releases a new version — install them with your native package manager (`zypper`, `apt`, `dnf`).

## Table of Contents

- [Packages](#packages)
- [Supported Distributions](#supported-distributions)
- [Installation](#installation)
- [How Auto-Update Works](#how-auto-update-works)
- [Maintainer Guide](#maintainer-guide)
- [Repository Structure](#repository-structure)

## Packages

| Package | Description | Upstream |
|---------|-------------|----------|
| **nic-xray** | Ethernet physical connectivity diagnostic tool | [ciroiriarte/nic-xray](https://github.com/ciroiriarte/nic-xray) |
| **ttl** | Traceroute/mtr-style TUI (requires Rust >= 1.88) | [lance0/ttl](https://github.com/lance0/ttl) |
| **xfr** | Network bandwidth testing TUI (requires Rust >= 1.88) | [lance0/xfr](https://github.com/lance0/xfr) |

## Supported Distributions

| Distribution | Repository Alias | Arch | nic-xray | ttl | xfr |
|---|---|---|:---:|:---:|:---:|
| openSUSE Tumbleweed | `openSUSE_Tumbleweed` | x86_64, aarch64 | ✓ | ✓ | ✓ |
| openSUSE Slowroll | `openSUSE_Slowroll` | x86_64, aarch64 | ✓ | ✓ | ✓ |
| openSUSE Leap 16.0 | `openSUSE_Leap_16.0` | x86_64, aarch64 | ✓ | ✓ | ✓ |
| openSUSE Leap 15.6 | `openSUSE_Leap_15.6` | x86_64, aarch64 | ✓ | — | — |
| Rocky Linux 9 | `Rocky_9` | x86_64, aarch64 | ✓ | ✓ | ✓ |
| Rocky Linux 10 | `Rocky_10` | x86_64, aarch64 | ✓ | ✓ | ✓ |
| Ubuntu 22.04 LTS | `Ubuntu_22.04` | x86_64, aarch64 | ✓ | — | — |
| Ubuntu 24.04 LTS | `Ubuntu_24.04` | x86_64, aarch64 | ✓ | — | — |

> **Note:** `ttl` and `xfr` require Rust >= 1.88, which is not yet available in Leap 15.6 or Ubuntu repos. Builds will automatically succeed once a compatible Rust version ships.

## Installation

### openSUSE (zypper)

```bash
zypper addrepo https://download.opensuse.org/repositories/home:/ciriarte:/network-tools/openSUSE_Tumbleweed/ obs-network-tools
zypper refresh
zypper install nic-xray ttl xfr
```

Replace `openSUSE_Tumbleweed` with your [repository alias](#supported-distributions).

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

### Rocky Linux (dnf)

```bash
dnf config-manager --add-repo \
  https://download.opensuse.org/repositories/home:/ciriarte:/network-tools/Rocky_9/home:ciriarte:network-tools.repo
dnf install nic-xray ttl xfr
```

Replace `Rocky_9` with `Rocky_10` for Rocky Linux 10.

> **Note:** `nic-xray` depends on `lldpd`, available via EPEL:
> ```bash
> dnf install epel-release
> ```

## How Auto-Update Works

All three packages are fully autonomous — when upstream pushes a new tag, the pipeline picks it up within 24 hours with no manual steps.

### nic-xray

The GitHub Actions [workflow](.github/workflows/update-nic-xray.yml) runs daily and:

1. Queries the GitHub API for the latest tag on [ciroiriarte/nic-xray](https://github.com/ciroiriarte/nic-xray).
2. Compares with the current version in `nic-xray.changes`.
3. If changed: updates `_service`, changelogs, commits to this repo, and pushes to OBS.

OBS then runs its source services (`tar_scm` + `set_version` + `recompress`) to fetch, package, and build.

### ttl and xfr

Rust packages require pre-committed source and vendor tarballs because OBS build workers have no internet access. The GitHub Actions workflows ([ttl](.github/workflows/update-ttl.yml), [xfr](.github/workflows/update-xfr.yml)) run daily and:

1. Query the GitHub API for the latest tag on [lance0/ttl](https://github.com/lance0/ttl) or [lance0/xfr](https://github.com/lance0/xfr).
2. If changed: install Rust, clone at the new tag, run `cargo vendor`.
3. Build the source tarball and vendor archive (`vendor.tar.zst`).
4. Update spec, changelogs, commit to this repo, and push to OBS.

## Maintainer Guide

<details>
<summary><strong>Prerequisites</strong></summary>

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

</details>

<details>
<summary><strong>Required GitHub secrets</strong></summary>

Add these secrets to the repository (Settings > Secrets > Actions):

| Secret | Value |
|--------|-------|
| `OBS_PASSWORD` | OBS account password for `ciriarte` |

</details>

<details>
<summary><strong>OBS project setup (one-time)</strong></summary>

Create the OBS project and configure repositories:

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

</details>

<details>
<summary><strong>Deploying package changes to OBS</strong></summary>

**First-time setup (any package):**

```bash
osc co home:ciriarte:network-tools
mkdir -p home:ciriarte:network-tools/<package>
cp packages/<package>/* home:ciriarte:network-tools/<package>/
cd home:ciriarte:network-tools/<package>
osc add *
osc commit -m "Initial package"
```

**Updating an existing package:**

```bash
cd home:ciriarte:network-tools/<package>
osc up
cp /path/to/obs-network-tools/packages/<package>/* .
osc commit -m "Update to version X.Y"
```

</details>

<details>
<summary><strong>Manual version updates</strong></summary>

Version updates are normally handled automatically by GitHub Actions. To trigger an update immediately, run the workflow manually from the Actions tab.

**nic-xray** (local alternative):

```bash
./scripts/update-nic-xray-version.sh --push
```

**ttl / xfr** (fully manual, e.g. without GitHub Actions):

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

</details>

<details>
<summary><strong>Verification</strong></summary>

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

</details>

## Repository Structure

<details>
<summary>Click to expand</summary>

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

</details>

## License

This packaging pipeline is maintained by [Ciro Iriarte](mailto:ciro.iriarte+software@gmail.com). The packaged software is distributed under its respective upstream licenses.
