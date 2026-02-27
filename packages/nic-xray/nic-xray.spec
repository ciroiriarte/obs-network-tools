Name:           nic-xray
Version:        0
Release:        1%{?dist}
Summary:        Network interface diagnostic tool

License:        GPL-3.0-only
URL:            https://github.com/ciroiriarte/misc-scripts
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       ethtool
Requires:       iproute2
%if 0%{?rhel}
# lldpd is available via EPEL on Rocky Linux
Requires:       lldpd
%else
Requires:       lldpd
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

%files
%license LICENSE
%doc README.md
%{_bindir}/nic-xray

%changelog
* Wed Feb 26 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 1.0-1
- Initial package release
