Name:           switch-xray
Version:        0
Release:        1%{?dist}
Summary:        Switch port diagnostics and documentation via SNMP

License:        GPL-3.0-only
URL:            https://github.com/ciroiriarte/switch-xray
#Git-Clone:     https://github.com/ciroiriarte/switch-xray
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?rhel}
# Rocky Linux: net-snmp-utils provides snmpwalk, snmpbulkwalk, snmpget
Requires:       net-snmp-utils
%else
# openSUSE: net-snmp provides SNMP CLI tools
Requires:       net-snmp
%endif
# Optional: topology diagram generation
Recommends:     graphviz

%description
Queries network switches via SNMP to display port status, neighbor
information, VLAN assignments, and optionally generate topology diagrams.
Supports automatic switch discovery and documentation workflows.

%prep
%autosetup

%build
# nothing to build

%install
install -Dm0755 switch-xray.sh %{buildroot}%{_bindir}/switch-xray
install -Dm0644 man/man8/switch-xray.8 %{buildroot}%{_mandir}/man8/switch-xray.8
install -Dm0644 switch-xray.conf.example %{buildroot}%{_docdir}/%{name}/switch-xray.conf.example

%files
%license LICENSE
%doc README.md
%{_bindir}/switch-xray
%{_mandir}/man8/switch-xray.8%{ext_man}
%{_docdir}/%{name}/switch-xray.conf.example

%changelog
* Sun Mar 01 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 1.0.1-1
- Fix SNMP text value parsing and status colors

* Thu Feb 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 1.0-1
- Initial package release
