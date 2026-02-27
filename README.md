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

---

## Distributions Covered

| Distribution           | Repository alias        | Arch           |
|------------------------|-------------------------|----------------|
| openSUSE Leap 15.5     | openSUSE_Leap_15.5      | x86_64, aarch64 |
| openSUSE Leap 15.6     | openSUSE_Leap_15.6      | x86_64, aarch64 |
| openSUSE Tumbleweed    | openSUSE_Tumbleweed     | x86_64, aarch64 |
| openSUSE Slowroll      | openSUSE_Slowroll       | x86_64, aarch64 |
| Rocky Linux 9          | Rocky_9                 | x86_64, aarch64 |
| Rocky Linux 10         | Rocky_10                | x86_64, aarch64 |
| Ubuntu 22.04 LTS       | Ubuntu_22.04            | x86_64, aarch64 |
| Ubuntu 24.04 LTS       | Ubuntu_24.04            | x86_64, aarch64 |

---

## Installing Packages

### openSUSE (zypper)

```bash
zypper addrepo https://download.opensuse.org/repositories/home:/ciriarte:/network-tools/openSUSE_Leap_15.6/ obs-network-tools
zypper refresh
zypper install nic-xray
```

Replace `openSUSE_Leap_15.6` with your distribution alias from the table above.

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
└── packages/
    └── nic-xray/
        ├── _service           # OBS service: auto-fetch from GitHub tags
        ├── nic-xray.spec      # RPM spec (openSUSE + Rocky Linux)
        ├── nic-xray.changes   # openSUSE changelog
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
  <repository name="openSUSE_Leap_15.5">
    <path project="openSUSE:Leap:15.5" repository="standard"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
  <repository name="openSUSE_Leap_15.6">
    <path project="openSUSE:Leap:15.6" repository="standard"/>
    <arch>x86_64</arch>
    <arch>aarch64</arch>
  </repository>
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

### First-time setup

```bash
# Check out the OBS project locally
osc co home:ciriarte:network-tools

# Create the package directory and copy files
mkdir -p home:ciriarte:network-tools/nic-xray
cp packages/nic-xray/* home:ciriarte:network-tools/nic-xray/

cd home:ciriarte:network-tools/nic-xray
osc add *
osc commit -m "Initial package"
```

### Updating an existing package

```bash
cd home:ciriarte:network-tools/nic-xray
osc up

# Copy updated files from this repository
cp /path/to/obs-network-tools/packages/nic-xray/* .

osc commit -m "Update to version X.Y"
```

---

## How Auto-Rebuild Works

Version tracking uses two layers:

### 1. OBS source service (`_service`)
When a commit is made to the OBS package, OBS automatically:
1. **Fetches source** — `tar_scm` clones `main` from the upstream repo at the version pinned in `_service`.
2. **Packages the source** — `recompress` produces a `.tar.gz` source archive.
3. **Injects the version** — `set_version` propagates the version into the spec and `.dsc` files.
4. **Rebuilds and publishes** — Packages are built for all configured distributions and published automatically.

### 2. GitHub Actions workflow (version bump)
The workflow at `.github/workflows/update-nic-xray.yml` runs daily and on demand:
1. Fetches `nic-xray.sh` from `ciroiriarte/misc-scripts` on `main`.
2. Reads `SCRIPT_VERSION` (falling back to `VERSION`) from the script.
3. If the version changed, updates `_service`, `nic-xray.changes`, and `debian.changelog`.
4. Commits the changes to this repo and pushes the updated package to OBS.

This means: when `nic-xray.sh` gets a new `SCRIPT_VERSION`, the pipeline triggers automatically with no manual steps required.

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
