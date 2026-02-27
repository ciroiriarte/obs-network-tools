# Purpose
* This process should build packages of network tools for Linux distributions
* These application are not generally packaged by distributions
* We want to facilitate installation via regular tooling (apt/dnf/zypper)

# Product
* The output of your work is to build an autonomous packaging pipeline in OBS (OBS should automatically rebuild & publish packages once new versions are released)
* If required, bash scripts can be prepared as byproduct to assist the main aim
* Supported architecture
  - x86_64: mandatory
  - arm64: optional, to be built if available for the linux distro at OBS.

# Packager
* Name: Ciro Iriarte
* Email: ciro.iriarte+software@gmail.com

# Enabler
* We'll use Open Build Service (OBS) available at https://build.opensuse.org/
* osc CLI client available for automation

# Scope

## Distributions
* openSUSE: Last 2 Leap releases, Tumbleweed, Slowroll
* Rocky Linux: Last 2 releases
* Ubuntu: Last 2 LTS releases

## Software
* nic-xray
  - Single script, part of https://github.com/ciroiriarte/misc-scripts (shared github repo with other misc scripts)
  - Discard unrelated scripts
  - Remove documentation not related to this script
* ttl
  Network diagnostic tool available at https://github.com/lance0/ttl (its own github repo)
* xfr
  Network benchmarking tool available at https://github.com/lance0/xfr (its own github repo)
  
# The repositories
* Must be built with OBS
* Must cover distributions in scope
* Must include all the information & structure expected by native packages
* zypper repos for openSUSE
* apt repos for Ubuntu
* yum/dnf repos for Rocky Linux
* Packages must include documentation
* Packages must handle dependencies
* Dependencies not present in the distribution should also be added to this repo as additional packages
* OBS project to be created is home:ciriarte:network-tools

# Reference Documentation
* OBS documentation available at https://openbuildservice.org/help/manuals/obs-user-guide/cha-obs-osc
* Packaging software with OBS: https://en.opensuse.org/Portal:Packaging
* openSUSE packaging
  https://en.opensuse.org/openSUSE:Packaging_guidelines
  https://en.opensuse.org/openSUSE:Packaging_Conventions_RPM_Macros
* Ubuntu/Debian builds: https://en.opensuse.org/openSUSE:Build_Service_Debian_builds
* Rocky Linux packaging: https://docs.rockylinux.org/10/guides/package_management/package_dev_start/

# Documentation
* As code or logic is built, document everything a user would need in README.md
