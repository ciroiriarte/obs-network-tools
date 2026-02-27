Name:           nic-xray
Version:        0
Release:        1%{?dist}
Summary:        Network interface diagnostic tool

License:        GPL-3.0-only
URL:            https://github.com/ciroiriarte/misc-scripts
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.8

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
install -Dm0644 %{SOURCE1} %{buildroot}%{_mandir}/man8/nic-xray.8

%files
%license LICENSE
%doc README.md
%{_bindir}/nic-xray
%{_mandir}/man8/nic-xray.8%{ext_man}

%changelog
* Thu Feb 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 1.4-1
- Update to 1.4 (sync with SCRIPT_VERSION in nic-xray.sh)
- Add man page

* Wed Feb 26 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 1.0-1
- Initial package release
