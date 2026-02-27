Name:           xfr
Version:        0.8.0
Release:        1%{?dist}
Summary:        Modern network bandwidth testing tool with TUI
License:        MIT OR Apache-2.0
URL:            https://github.com/lance0/xfr
Source0:        xfr-%{version}.tar.gz
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
Modern network bandwidth testing tool with a live terminal user interface.
A drop-in replacement for iperf3 with additional features:

- TCP, UDP, and QUIC protocol support
- Live TUI with real-time throughput visualization
- Multi-client server with rate limiting and ACL support
- Bidirectional and parallel stream testing
- Path MTU probing and configurable bitrate pacing
- JSON, CSV, and text output for scripting
- HMAC-SHA256 PSK authentication
- mDNS-based local server discovery
- Optional Prometheus metrics export

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
install -Dm0644 docs/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%files
%doc README.md CHANGELOG.md
%license LICENSE-MIT LICENSE-APACHE
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1%{ext_man}

%changelog
* Thu Feb 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.8.0-1
- Initial package release
