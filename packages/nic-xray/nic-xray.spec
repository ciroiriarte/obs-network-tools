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

%description
Displays detailed information about physical network interfaces including
PCI slot, firmware versions, MAC, MTU, link status, speed/duplex,
bond/LAG membership, and LLDP peer information.

Includes the nic-health companion: read-only NIC hardware and data-path
health checks (PCIe link/AER, temperature, devlink health reporters, link
flaps, NVIDIA ConnectX counters, optional mstlink/mlxlink deep mode) with a
Nagios-compatible verdict.

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

%files
%license LICENSE
%doc README.md
%{_bindir}/nic-xray
%{_mandir}/man8/nic-xray.8%{ext_man}
%{_datadir}/bash-completion/completions/nic-xray
%{_bindir}/nic-health
%{_mandir}/man8/nic-health.8%{ext_man}
%{_datadir}/bash-completion/completions/nic-health

%changelog
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

* Thu Feb 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 2.1-1
- Refactor: nic-xray moved to own repository (github.com/ciroiriarte/nic-xray)
- Man page now sourced from upstream (man/man1/nic-xray.1, section 1)

* Thu Feb 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 1.4-1
- Update to 1.4 (sync with SCRIPT_VERSION in nic-xray.sh)
- Add man page
