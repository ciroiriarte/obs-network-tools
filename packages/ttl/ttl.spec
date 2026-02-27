Name:           ttl
Version:        0.19.0
Release:        1%{?dist}
Summary:        Network diagnostic tool — traceroute/mtr-style TUI with hop stats
License:        MIT OR Apache-2.0
URL:            https://github.com/lance0/ttl
Source0:        ttl-%{version}.tar.gz
Source1:        vendor.tar.zst

%if 0%{?suse_version}
BuildRequires:  cargo-packaging
BuildRequires:  rust >= 1.88
ExclusiveArch:  %{rust_arches}
%else
BuildRequires:  cargo
BuildRequires:  rust >= 1.88
ExclusiveArch:  x86_64 aarch64
%endif

%description
Network diagnostic tool that goes beyond traceroute: MTU discovery, NAT
detection, route flap alerts, IX identification, and more.

Provides a real-time TUI with hop statistics, multi-target tracing,
Paris/Dublin traceroute for ECMP path enumeration, ASN/GeoIP enrichment,
and scriptable JSON/CSV/text output.

Requires cap_net_raw capability (or root) for raw socket access.

%prep
%autosetup -a1 -p1 -n %{name}-%{version}

%build
%if 0%{?suse_version}
%{cargo_build}
%else
cargo build --release --offline --locked
%endif

%install
install -Dm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

%post
# Grant raw socket capability so the tool can run without sudo
if command -v setcap >/dev/null 2>&1; then
    setcap cap_net_raw+ep %{_bindir}/%{name} || true
fi

%postun
if [ $1 -eq 0 ] && command -v setcap >/dev/null 2>&1; then
    setcap -r %{_bindir}/%{name} 2>/dev/null || true
fi

%files
%doc README.md CHANGELOG.md
%license LICENSE-MIT LICENSE-APACHE
%{_bindir}/%{name}

%changelog
* Thu Feb 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.19.0-1
- Initial package release
