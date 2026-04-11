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

%description
Displays detailed information about physical network interfaces including
PCI slot, firmware versions, MAC, MTU, link status, speed/duplex,
bond/LAG membership, and LLDP peer information.

%prep
%autosetup

%build
# nothing to build

%install
install -Dm0755 nic-xray.sh %{buildroot}%{_bindir}/nic-xray
install -Dm0644 man/man8/nic-xray.8 %{buildroot}%{_mandir}/man8/nic-xray.8
install -Dm0644 completions/nic-xray.bash %{buildroot}%{_datadir}/bash-completion/completions/nic-xray

%files
%license LICENSE
%doc README.md
%{_bindir}/nic-xray
%{_mandir}/man8/nic-xray.8%{ext_man}
%{_datadir}/bash-completion/completions/nic-xray

%changelog
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
