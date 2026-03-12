Name:           xfr
Version:        0.9.4
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
* Thu Mar 12 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.9.4-1
- Add --no-mdns flag to disable mDNS service registration (#41)
- Show delta retransmits in plain text interval reports (#36)
- Fix retransmit delta baseline during omit/quiet intervals, add no_mdns config support
- Bump version to v0.9.4

* Wed Mar 11 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.9.3-1
- Fix QUIC dual-stack, add server --bind, server random payloads (#38, #39, #34)
- Fix server random payload on single-port TCP reverse (#34)
- Bump version to v0.9.3

* Sat Mar 07 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.9.2-1
- Collapse v0.9.0 into v0.9.1 changelog (v0.9.0 was never released)
- Limit single-port handshake fanout, adapt server read timeout per peer (#32)
- Add acknowledgments for matttbe, update zero-copy roadmap
- Add --random flag for random payload data (#34)
- Default to random payloads, add --zeros opt-out (#34)
- Add fq_codel to namespace test qdiscs, document queue limitation (#32)
- Fix Windows build: gate pacing helper on linux (#37)
- Add Windows build fix to unreleased changelog (#37)
- Add early-exit summary and delta rtx to roadmap (#35, #36)
- Bump version to v0.9.2

* Fri Mar 06 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.9.1-1
- Add graceful shutdown send errors to roadmap polish items
- Add eget, AUR, and Terminal Trove to README
- Add pkgsrc to See Also section
- Add MPTCP support (--mptcp flag, Linux 5.6+)
- Fix review findings for MPTCP
- Update docs for MPTCP support
- Server auto-MPTCP: always try MPTCP listeners, silent fallback to TCP
- Fix MPTCP label, per-stream retransmit reporting, and teardown race
- Fix MPTCP fallback detection after error wrapping, document API break
- Add MPTCP to README headline
- Suppress expected teardown errors: peer-close near deadline, cancel
- Add ConnectionAborted to teardown classifier, suppression counters
- Fix stale docs: MPTCP usage section, comparison accuracy, resolved items
- Add MPTCP network namespace CI test
- Bump actions/download-artifact from 7 to 8
- Bump actions/upload-artifact from 6 to 7
- Fix JoinHandle panic (#24) and final TCP_INFO reporting (#26)
- Add sender-side TCP_INFO assertions to MPTCP CI test
- Clarify TCP Info labels, fix high stream count limit (#25, #26)
- Use kernel SO_MAX_PACING_RATE for TCP pacing on Linux (#30)
- Fix low-bitrate pacing and harden SO_MAX_PACING_RATE tests
- MPTCP support, kernel TCP pacing, teardown fixes (#24, #25, #26, #30)
- Merge pull request #27 from lance0/dependabot/github_actions/actions/download-artifact-8
- Merge pull request #28 from lance0/dependabot/github_actions/actions/upload-artifact-7
- Update dependencies (semver-compatible)
- Clarify kernel pacing MPTCP limitation and global bitrate behavior
- Bump version to v0.9.0
- Release v0.9.0
- Harden teardown for high stream counts, fix pacing rate width (#25, #32)
- Bump version to v0.9.1

* Thu Feb 27 2026 Ciro Iriarte <ciro.iriarte+software@gmail.com> - 0.8.0-1
- Initial package release
