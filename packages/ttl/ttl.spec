Name:           ttl
Version:        0.19.1
Release:        1%{?dist}
Summary:        Network diagnostic tool — traceroute/mtr-style TUI with hop stats
License:        MIT OR Apache-2.0
URL:            https://github.com/lance0/ttl
#Git-Clone:     https://github.com/lance0/ttl.git
Source0:        ttl-%{version}.tar.gz
Source1:        vendor.tar.zst

%if 0%{?suse_version}
BuildRequires:  cargo-packaging
BuildRequires:  rust >= 1.88
Requires(post): permissions
Recommends:     bash-completion
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
%if 0%{?suse_version}
%{cargo_install}
%else
install -Dm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
%endif

%if 0%{?suse_version}
%check
%{cargo_test}
%endif

%if 0%{?suse_version}
%verifyscript
%verify_permissions -e %{_bindir}/%{name}

%post
%set_permissions %{_bindir}/%{name}
%else
%post
# Grant raw socket capability so the tool can run without sudo
if command -v setcap >/dev/null 2>&1; then
    setcap cap_net_raw+ep %{_bindir}/%{name} || true
fi

%postun
if [ $1 -eq 0 ] && command -v setcap >/dev/null 2>&1; then
    setcap -r %{_bindir}/%{name} 2>/dev/null || true
fi
%endif

%files
%doc README.md CHANGELOG.md
%license LICENSE-MIT LICENSE-APACHE
%if 0%{?suse_version}
%verify(not mode caps) %attr(0755,root,root) %caps(cap_net_raw,cap_net_admin=ep) %{_bindir}/%{name}
%else
%{_bindir}/%{name}
%endif

%changelog
* Sun May 03 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.19.1-1
- Bump actions/download-artifact from 7 to 8
- Update quinn-proto to fix RUSTSEC-2026-0037
- Fix FreeBSD CI: install ca_root_nss before fetching crates
- Bump socket2 from 0.6.2 to 0.6.3
- Bump tokio from 1.49.0 to 1.50.0
- Bump libc from 0.2.182 to 0.2.183
- Merge pull request #59 from lance0/dependabot/cargo/socket2-0.6.3
- Merge pull request #58 from lance0/dependabot/cargo/tokio-1.50.0
- Merge pull request #60 from lance0/dependabot/cargo/libc-0.2.183
- Merge pull request #55 from lance0/dependabot/github_actions/actions/download-artifact-8
- Bump actions/upload-artifact from 6 to 7
- Merge pull request #56 from lance0/dependabot/github_actions/actions/upload-artifact-7
- Update aws-lc-sys and rustls-webpki to fix security advisories
- Update rustls-webpki to fix RUSTSEC-2026-0098/0099
- Update rustls-webpki to fix RUSTSEC-2026-0104
- Fix clippy 1.95 lints: collapsible_match and unnecessary_sort_by
- Upgrade hickory-resolver to 0.26 to fix RUSTSEC-2026-0118/0119
- Restore Google DNS fallback when system resolver build fails
- Merge pull request #71 from lance0/hickory-0.26-upgrade
- Bump softprops/action-gh-release from 2 to 3
- Merge pull request #69 from lance0/dependabot/github_actions/softprops/action-gh-release-3
- Bump toml from 0.9 to 1.x
- Fix platform-specific clippy warnings
- Merge pull request #72 from SSakutaro/fix/macos-clippy-warnings
- Run clippy on macOS and FreeBSD CI jobs
- Add pre-commit hooks for fmt, clippy, and test
- Lead with cargo install for prek in CONTRIBUTING
- Gate DGRAM ICMP socket helpers off FreeBSD/NetBSD
- Merge pull request #73 from lance0/prek-setup
- Doc sweep before v0.19.1 ship
- Bump version to v0.19.1

* Thu Feb 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.19.0-1
- Initial package release
