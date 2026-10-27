Name:           nic-xray
Version:        0
Release:        1%{?dist}
Summary:        Ethernet physical connectivity diagnostic tool

License:        GPL-3.0-only
URL:            https://github.com/ciroiriarte/nic-xray
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       ethtool
Requires:       lldpd
%if 0%{?rhel}
# Rocky Linux: iproute (provides /sbin/ip); lldpd via EPEL
Requires:       iproute
%else
# openSUSE: package is named iproute2
Requires:       iproute2
%endif
# Optional: graph generation feature
Recommends:     graphviz
# Optional: NIC vendor/model names (nic-xray --physical, nic-health)
Recommends:     pciutils
# Optional: nic-health -l deep on NVIDIA ConnectX (open-source mstlink)
Recommends:     mstflint

# Man pages are compressed by the build root policy; ext_man is a SUSE macro
%{!?ext_man:%global ext_man .gz}

# nic-report.py needs Python 3.9+: Leap 15's python3 is 3.6, so use its python311 there
%if 0%{?suse_version} && 0%{?suse_version} < 1600
%global fleet_python_pkg python311
%global fleet_python /usr/bin/python3.11
%global fleet_weasyprint python311-weasyprint
%else
%global fleet_python_pkg python3 >= 3.9
%global fleet_python /usr/bin/python3
%global fleet_weasyprint python3-weasyprint
%endif

%description
Displays detailed information about physical network interfaces including
PCI slot, firmware versions, MAC, MTU, link status, speed/duplex,
bond/LAG membership, and LLDP peer information.

Includes the nic-health companion: read-only NIC hardware and data-path
health checks (PCIe link/AER, temperature, devlink health reporters, link
flaps, NVIDIA ConnectX counters, optional mstlink/mlxlink deep mode) with a
Nagios-compatible verdict.

The fleet tools (nic-sweep, nic-report) for the operator host are in the
nic-xray-fleet package.

%package fleet
Summary:        Fleet sweep and multi-site report for nic-xray and nic-health
Requires:       %{name} = %{version}-%{release}
Requires:       jq
Requires:       /usr/bin/ssh
Requires:       %{fleet_python_pkg}
# Optional: nic-report -O pdf
Suggests:       %{fleet_weasyprint}

%description fleet
Operator-host tools for a fleet of nodes running nic-xray and nic-health.

nic-sweep runs nic-health (and nic-xray, when present) on many hosts over
SSH in parallel and stores the results per site and sweep. nic-report turns
one or more sweeps into a single- or multi-site report (Markdown, JSON, HTML,
PDF with WeasyPrint): baselines, outliers, patterns across sites, prioritised
recommendations from a rule catalog, sweep comparison, and an optional
checked AI-written summary.

%prep
%autosetup

%build
# nothing to build

%install
install -Dm0755 nic-xray.sh %{buildroot}%{_bindir}/nic-xray
install -Dm0644 man/man8/nic-xray.8 %{buildroot}%{_mandir}/man8/nic-xray.8
install -Dm0644 completions/nic-xray.bash %{buildroot}%{_datadir}/bash-completion/completions/nic-xray
install -Dm0755 nic-health.sh %{buildroot}%{_bindir}/nic-health
install -Dm0644 man/man8/nic-health.8 %{buildroot}%{_mandir}/man8/nic-health.8
install -Dm0644 completions/nic-health.bash %{buildroot}%{_datadir}/bash-completion/completions/nic-health
install -Dm0755 nic-sweep.sh %{buildroot}%{_bindir}/nic-sweep
install -Dm0644 man/man8/nic-sweep.8 %{buildroot}%{_mandir}/man8/nic-sweep.8
install -Dm0644 completions/nic-sweep.bash %{buildroot}%{_datadir}/bash-completion/completions/nic-sweep
install -Dm0755 nic-report.py %{buildroot}%{_bindir}/nic-report
sed -i '1s|^#!/usr/bin/env python3$|#!%{fleet_python}|' %{buildroot}%{_bindir}/nic-report
install -Dm0644 man/man8/nic-report.8 %{buildroot}%{_mandir}/man8/nic-report.8
install -Dm0644 completions/nic-report.bash %{buildroot}%{_datadir}/bash-completion/completions/nic-report
install -Dm0644 nic-report-rules.json %{buildroot}%{_datadir}/%{name}/nic-report-rules.json

%files
%license LICENSE
%doc README.md
%{_bindir}/nic-xray
%{_mandir}/man8/nic-xray.8%{ext_man}
%{_datadir}/bash-completion/completions/nic-xray
%{_bindir}/nic-health
%{_mandir}/man8/nic-health.8%{ext_man}
%{_datadir}/bash-completion/completions/nic-health

%files fleet
%license LICENSE
%doc README.md docs/design/nic-sweep.md
%{_bindir}/nic-sweep
%{_bindir}/nic-report
%{_mandir}/man8/nic-sweep.8%{ext_man}
%{_mandir}/man8/nic-report.8%{ext_man}
%{_datadir}/bash-completion/completions/nic-sweep
%{_datadir}/bash-completion/completions/nic-report
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/nic-report-rules.json

%changelog
* Tue Oct 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 2.14.0-1
- Add nic-xray-fleet subpackage: nic-sweep (fleet sweep over SSH) and
  nic-report (single- and multi-site reports, rule catalog in
  /usr/share/nic-xray)

* Tue Oct 20 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 2.11.1-1
- Fix nic-xray man page DROP indicator glyph (rendered empty)
- Ship nic-xray.sh with the executable bit set in the source tree
- Fix offline ISO builds on openSUSE Leap (tar missing before checkout)

* Tue Oct 20 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 2.11.0-1
- Add nic-health companion (/usr/bin/nic-health): read-only NIC hardware and data-path health checks with Nagios exit codes
- nic-health: PCIe link/AER, temperature, devlink health, link flaps, NVIDIA ConnectX (mlx5) counters, optional mstlink/mlxlink deep mode
- Add --virtual flag (VLAN/bridge/tap/VXLAN/... with MTU hierarchy) and bond MTU consistency check
- Add --cluster bond|nic for DOT diagrams; NIC vendor column; onboard NIC detection
- Fix SFF-8636 Rx power parsing on QSFP28, JSON control-character escaping, LACP check under mawk
- Fix bash completion for optional-value flags and for the packaged command name
- Recommends pciutils and mstflint

* Sat Apr 11 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 2.10.2-1
- Add physical topology flag (--physical/-p): NUMA, PCI slot, NIC vendor/model
- Add LLDP port description column
- Add Cisco ACI support via vendor TLVs
- Add bash completion (completions/nic-xray.bash)
- Display bandwidth metrics in bits/s (bps/Kbps/Mbps/Gbps)
- Document Juniper LLDP VLAN TLV limits and Apstra REST API workflow

* Fri Feb 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 2.1-1
- Refactor: nic-xray moved to own repository (github.com/ciroiriarte/nic-xray)
- Man page now sourced from upstream (man/man1/nic-xray.1, section 1)

* Fri Feb 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 1.4-1
- Update to 1.4 (sync with SCRIPT_VERSION in nic-xray.sh)
- Add man page
