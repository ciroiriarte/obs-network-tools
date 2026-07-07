Name:           ttl
Version:        0.20.2
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
* Tue Jul 07 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.20.2-1
- Bump docker/setup-buildx-action from 3 to 4 (#86)
- Bump docker/metadata-action from 5 to 6 (#87)
- Bump docker/setup-qemu-action from 3 to 4 (#88)
- Bump docker/login-action from 3 to 4 (#89)
- Bump docker/build-push-action from 6 to 7 (#90)
- fix: PMTUD correlation, lock ordering, and enrichment dedup (#104)
- fix: harden unsafe socket code against alignment UB and bad cmsg (#102)
- fix: harden CLI validation against panics and port overflow (#99)
- fix: file security and output hygiene (#103)
- fix: prevent TUI panics on multi-byte input and edge cases (#100)
- fix: prevent arithmetic panics on clock jumps and oversized packets (#101)
- docs: add SAFETY comment to set_ip_hdrincl unsafe block (#111)
- Bump actions/checkout from 6 to 7 (#105)
- Bump actions/cache from 5 to 6 (#106)
- Bump anyhow from 1.0.102 to 1.0.103 (#107)
- Bump clap_complete from 4.6.5 to 4.6.7 (#108)
- Bump maxminddb from 0.28.1 to 0.29.0 (#109)
- test: cover multibyte settings cursor editing (#112)
- fix: propagate IPv6 scope_id through recv/bind paths (LAN-143) (#113)
- fix: parse IPv6 extension headers in quoted error payloads (LAN-144) (#114)
- fix: bound enrichment caches to prevent unbounded memory growth (LAN-145) (#115)
- fix: TUI async polling, replay validation, assert→Result (LAN-150, LAN-181) (#116)
- fix: populate response TTL on macOS/BSD IPv4 (1-byte IP_RECVTTL cmsg) (#117)
- refactor: use PMTUD_MARKER const for the payload marker write (#118)
- fix: cap export filename length to stay within NAME_MAX (#119)
- Bump version to v0.20.2

* Sun Jun 28 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.20.1-1
- Lead Homebrew install with core formula (brew install ttl)
- Bump quinn-proto to 0.11.15 to clear RUSTSEC-2026-0185
- Fix macOS single-hop traces: per-probe send sockets for ICMP/UDP/TCP (#12)
- Roadmap: track TTL send-path correctness follow-ups before next release
- Unify IPv4 send path on IP_HDRINCL (TTL in the IP header) (#12)
- IPv6: per-probe sockets on FreeBSD/NetBSD; remove inter-probe delay (#12)
- Bump version to v0.20.1

* Thu Jun 11 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.20.0-1
- Add Alpine Linux and NixOS install instructions to README
- Bump maxminddb from 0.27.3 to 0.28.1
- Bump clap_complete from 4.6.3 to 4.6.5
- Bump tokio from 1.52.1 to 1.52.3
- Bump serde_json from 1.0.149 to 1.0.150
- Bump getifs from 0.4.0 to 0.6.1
- Merge pull request #75 from lance0/dependabot/cargo/maxminddb-0.28.1
- Merge pull request #77 from lance0/dependabot/cargo/clap_complete-4.6.5
- Merge pull request #79 from lance0/dependabot/cargo/serde_json-1.0.150
- Merge pull request #80 from lance0/dependabot/cargo/getifs-0.6.1
- Merge pull request #78 from lance0/dependabot/cargo/tokio-1.52.3
- Add trace diffing (--diff) and streaming JSON output (--stream-json)
- Merge pull request #81 from lance0/diff-streaming
- Add daemon mode, Prometheus exporter, and official Dockerfile
- Merge pull request #82 from lance0/daemon-prometheus
- Publish multi-arch container images to GHCR on release
- Merge pull request #83 from lance0/ghcr-publish
- Add interactive target selection
- Merge pull request #84 from lance0/interactive-targets
- Use a radix trie for IX prefix lookup
- Merge pull request #85 from lance0/ix-radix-trie
- Bump version to v0.20.0

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
