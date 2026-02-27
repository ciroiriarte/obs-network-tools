# obs-network-tools

Autonomous OBS packaging pipeline for network tools not commonly packaged by Linux distributions.

## Project Purpose

This repository contains OBS (Open Build Service) package definitions for various network diagnostic and benchmarking tools. Packages are built automatically when upstream releases a new version (via GitHub tags), and published to distribution repositories for easy installation via native package managers.

**OBS Project:** https://build.opensuse.org/project/show/home:ciriarte:network-tools

---

## Packages

| Package   | Description                                      | Upstream                                        |
|-----------|--------------------------------------------------|-------------------------------------------------|
| nic-xray  | Network interface diagnostic tool                | https://github.com/ciroiriarte/misc-scripts     |
| ttl       | Traceroute/mtr-style TUI (requires Rust ≥ 1.88) | https://github.com/lance0/ttl                  |
| xfr       | Network bandwidth testing TUI (requires Rust ≥ 1.88) | https://github.com/lance0/xfr             |

---

## Distributions Covered

| Distribution           | Repository alias        | Arch            | nic-xray | ttl | xfr |
|------------------------|-------------------------|-----------------|----------|-----|-----|
| openSUSE Leap 15.6     | openSUSE_Leap_15.6      | x86_64, aarch64 | ✓        | ✗ ¹ | ✗ ¹ |
| openSUSE Leap 16.0     | openSUSE_Leap_16.0      | x86_64, aarch64 | ✓        | ✓   | ✓   |
| openSUSE Tumbleweed    | openSUSE_Tumbleweed     | x86_64, aarch64 | ✓        | ✓   | ✓   |
| openSUSE Slowroll      | openSUSE_Slowroll       | x86_64, aarch64 | ✓        | ✓   | ✓   |
| Rocky Linux 9          | Rocky_9                 | x86_64, aarch64 | ✓        | ✓   | ✓   |
| Rocky Linux 10         | Rocky_10                | x86_64, aarch64 | ✓        | ✓   | ✓   |
| Ubuntu 22.04 LTS       | Ubuntu_22.04            | x86_64, aarch64 | ✓        | ✗ ¹ | ✗ ¹ |
| Ubuntu 24.04 LTS       | Ubuntu_24.04            | x86_64, aarch64 | ✓        | ✗ ¹ | ✗ ¹ |

¹ Requires Rust ≥ 1.88, which is not yet available in this distribution's standard
  repositories. Builds will automatically succeed once the distribution ships a
  compatible Rust version.

---

## Installing Packages

### openSUSE (zypper)

```bash
zypper addrepo https://download.opensuse.org/repositories/home:/ciriarte:/network-tools/openSUSE_Leap_16.0/ obs-network-tools
zypper refresh
zypper install nic-xray
```

Replace `openSUSE_Leap_16.0` with your distribution alias from the table above.

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
dnf install nic-xray
```

Replace `Rocky_9` with `Rocky_10` for Rocky Linux 10.

> **Note for Rocky Linux:** `lldpd` is available via EPEL. Enable it first:
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
├── CLAUDE.md                  # Project instructions
├── README.md                  # This file
├── scripts/
│   └── update-nic-xray-version.sh  # Manual version bump helper
└── packages/
    ├── nic-xray/
    │   ├── _service           # OBS service: auto-fetch from GitHub tags
    │   ├── nic-xray.spec      # RPM spec (openSUSE + Rocky Linux)
    │   ├── nic-xray.changes   # openSUSE changelog
    │   ├── nic-xray.8         # Man page (troff)
    │   ├── nic-xray.dsc       # Debian source package descriptor
    │   ├── debian.control     # Debian/Ubuntu package metadata
    │   ├── debian.changelog   # Debian/Ubuntu changelog
    │   └── debian.rules       # Debian build rules
    ├── ttl/
    │   ├── _service           # cargo_vendor (manual mode)
    │   ├── ttl-0.19.0.tar.gz  # Source tarball (committed)
    │   ├── vendor.tar.zst     # Vendored Rust dependencies
    │   ├── ttl.spec           # RPM spec (openSUSE + Rocky Linux)
    │   ├── ttl.changes        # openSUSE changelog
    │   ├── ttl.dsc            # Debian source package descriptor
    │   ├── debian.control     # Debian/Ubuntu package metadata
    │   ├── debian.changelog   # Debian/Ubuntu changelog
    │   ├── debian.rules       # Debian build rules
    │   └── debian.postinst    # Post-install: setcap cap_net_raw+ep
    └── xfr/
        ├── _service           # cargo_vendor (manual mode)
        ├── xfr-0.8.0.tar.gz   # Source tarball (committed)
        ├── vendor.tar.zst     # Vendored Rust dependencies
        ├── xfr.spec           # RPM spec (openSUSE + Rocky Linux)
        ├── xfr.changes        # openSUSE changelog
        ├── xfr.dsc            # Debian source package descriptor
        ├── debian.control     # Debian/Ubuntu package metadata
        ├── debian.changelog   # Debian/Ubuntu changelog
        └── debian.rules       # Debian build rules
```

---

## OBS Project Setup (one-time)

Create the OBS project and configure repositories. This can be done via the OBS web interface or via `osc`:

```bash
# Edit project metadata
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
    <!-- devel:languages:rust provides Rust >= 1.88 for packages that need it -->
    <path project="devel:languages:rust" repository="16.0"/>
    <path project="openSUSE:Leap:16.0" repository="standard"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
  <repository name="openSUSE_Leap_15.6">
    <!-- devel:languages:rust provides Rust >= 1.88 for packages that need it -->
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

### nic-xray (first-time setup)

```bash
osc co home:ciriarte:network-tools
mkdir -p home:ciriarte:network-tools/nic-xray
cp packages/nic-xray/* home:ciriarte:network-tools/nic-xray/
cd home:ciriarte:network-tools/nic-xray
osc add *
osc commit -m "Initial package"
```

### ttl (first-time setup)

`ttl` is a Rust binary. The vendor tarball (`vendor.tar.zst`) must be pre-built
and committed alongside the source tarball. To regenerate:

```bash
# Install Rust if needed: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
git clone --branch v0.19.0 https://github.com/lance0/ttl ttl-src
cd ttl-src && cargo vendor
mkdir -p .cargo
printf '[source.crates-io]\nreplace-with = "vendored-sources"\n\n[source.vendored-sources]\ndirectory = "vendor"\n' > .cargo/config.toml
cd ..
tar -czf ttl-0.19.0.tar.gz --exclude='.git' --exclude='vendor' --transform='s|^ttl-src|ttl-0.19.0|' ttl-src/
tar -I "zstd" -cf vendor.tar.zst -C ttl-src .cargo/config.toml vendor/
cp ttl-0.19.0.tar.gz vendor.tar.zst packages/ttl/

osc co home:ciriarte:network-tools
mkdir -p home:ciriarte:network-tools/ttl
cp packages/ttl/* home:ciriarte:network-tools/ttl/
cd home:ciriarte:network-tools/ttl
osc add *
osc commit -m "Initial package: ttl 0.19.0"
```

### Updating an existing package

```bash
cd home:ciriarte:network-tools/nic-xray
osc up
cp /path/to/obs-network-tools/packages/nic-xray/* .
osc commit -m "Update to version X.Y"
```

---

## How Auto-Rebuild Works

### nic-xray (fully autonomous)

Version tracking uses two layers:

**OBS source service (`_service`)**: When a commit is made to the OBS package, OBS automatically:
1. **Fetches source** — `tar_scm` clones `main` from the upstream repo at the version pinned in `_service`.
2. **Packages the source** — `recompress` produces a `.tar.gz` source archive.
3. **Injects the version** — `set_version` propagates the version into the spec and `.dsc` files.
4. **Rebuilds and publishes** — Packages are built for all configured distributions and published automatically.

**GitHub Actions workflow** (`.github/workflows/update-nic-xray.yml`) runs daily:
1. Fetches `nic-xray.sh` from `ciroiriarte/misc-scripts` on `main`.
2. Reads `SCRIPT_VERSION` (falling back to `VERSION`) from the script.
3. If the version changed, updates `_service`, `nic-xray.changes`, and `debian.changelog`.
4. Commits the changes to this repo and pushes the updated package to OBS.

When `nic-xray.sh` gets a new `SCRIPT_VERSION`, the pipeline triggers automatically with no manual steps required.

### ttl (semi-manual updates)

`ttl` uses a pre-committed source tarball + vendor tarball pattern (Rust offline builds):

1. A new upstream release is tagged at https://github.com/lance0/ttl
2. Maintainer runs: re-download source, re-run `cargo vendor`, update `vendor.tar.zst`
3. Commit updated `ttl-X.Y.Z.tar.gz`, `vendor.tar.zst`, spec, changelogs to OBS
4. OBS rebuilds and publishes automatically

The `_service` file documents that `cargo_vendor` must be re-run manually on version bumps.

### Required GitHub secret
Add `OBS_PASSWORD` to this repository's secrets (Settings → Secrets → Actions):

| Secret         | Value                        |
|----------------|------------------------------|
| `OBS_PASSWORD` | OBS account password for `ciriarte` |

### Manual version update
To update the version manually instead of waiting for the daily schedule:

```bash
# Update locally
./scripts/update-nic-xray-version.sh

# Or update and push to OBS in one step
./scripts/update-nic-xray-version.sh --push
```

Or trigger the GitHub Actions workflow manually from the Actions tab.

---

## Verification

After pushing to OBS, verify the builds:

```bash
# Check build results for all distros
osc results home:ciriarte:network-tools nic-xray

# Watch live build log (example: Tumbleweed x86_64)
osc buildlog home:ciriarte:network-tools nic-xray openSUSE_Tumbleweed x86_64
```

On each installed system:

```bash
# RPM (openSUSE / Rocky Linux)
rpm -qi nic-xray

# Deb (Ubuntu)
dpkg -s nic-xray

# Functional test
nic-xray --help
sudo nic-xray
```
