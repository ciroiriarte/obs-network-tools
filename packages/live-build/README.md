# live-build (co-packaged)

A current [live-build](https://salsa.debian.org/live-team/live-build) rebuilt
for the Debian/Ubuntu targets, because Ubuntu 22.04/24.04 ship a broken
`3.0~a57` fork. Dependency of `create-network-tshoot-livecd`.

The OBS package source (patched native `live-build_*+nt1.{tar.xz,dsc}`) is
committed directly to `home:ciriarte:network-tools/live-build`. It is a light
patch of Debian's source that drops the `po4a`/`devscripts` build-deps and the
translated-man-page step (po4a is in Ubuntu *universe*, unavailable in the OBS
build root); English man pages and all functionality are unchanged.

Regenerate and commit with [`refresh-source.sh`](./refresh-source.sh).
