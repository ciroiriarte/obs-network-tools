#!/bin/bash
# refresh-source.sh — (re)generate the patched live-build source package that
# feeds the OBS package home:ciriarte:network-tools/live-build.
#
# WHY THIS PACKAGE EXISTS
#   Ubuntu 22.04 and 24.04 ship live-build 3.0~a57, an unmaintained fork that
#   cannot build a current image (it references Ubuntu 11.10 boot-splash theme
#   packages and rejects modern lb flags). create-network-tshoot-livecd needs a
#   current live-build, so we rebuild Debian's exact source for the Debian and
#   Ubuntu OBS targets. The epoch (1:) keeps it ahead of Ubuntu's 3.0~a57.
#
# WHY IT IS PATCHED (not an exact rebuild)
#   Debian's live-build Build-Depends on po4a, which lives in Ubuntu *universe*.
#   The OBS Ubuntu build root only exposes main, so an unmodified rebuild is
#   "unresolvable: nothing provides po4a" on Ubuntu. po4a is only used to build
#   *translated* man pages; the English man pages are static. This patch drops
#   the po4a/devscripts build-deps and the translated-man-page step, leaving all
#   functionality and the English man pages intact.
#
# USAGE
#   ./refresh-source.sh [UPSTREAM_VERSION]     # default below
#   Produces live-build_<ver>+nt1.{tar.xz,dsc} in the current directory, then:
#     osc co home:ciriarte:network-tools live-build
#     cp live-build_*+nt1.{tar.xz,dsc} <checkout>/ && cd <checkout>
#     osc addremove && osc ci -m "live-build <ver>+nt1"
set -euo pipefail

UPVER="${1:-20250505+deb13u1}"
NTVER="${UPVER}+nt1"
BASE="http://deb.debian.org/debian/pool/main/l/live-build"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo ":: Fetching Debian live-build ${UPVER} source..."
curl -fsSL -o "${WORK}/live-build_${UPVER}.tar.xz" "${BASE}/live-build_${UPVER}.tar.xz"
tar xf "${WORK}/live-build_${UPVER}.tar.xz" -C "${WORK}"
SRC="${WORK}/live-build"

echo ":: Applying patches (drop po4a/devscripts + translated man pages)..."
# Makefile: drop the translated-man-page build+install (po4a); keep English pages.
sed -i '/^\tmake -C manpages$/,/^\tdone$/d' "${SRC}/Makefile"
# control: drop po4a + devscripts build-deps.
sed -i 's/^Build-Depends: debhelper-compat (= 13), devscripts, gettext, po4a$/Build-Depends: debhelper-compat (= 13), gettext/' "${SRC}/debian/control"
# rules: drop the po4a manpages calls from override_dh_auto_install.
sed -i '/# Update manual pages first/d; /\$(MAKE) -C manpages update/d; /\$(MAKE) -C manpages build/d' "${SRC}/debian/rules"

echo ":: Prepending changelog entry ${NTVER}..."
cat > "${WORK}/entry" <<EOF
live-build (1:${NTVER}) unstable; urgency=medium

  * Rebuild for the home:ciriarte:network-tools OBS repository, providing a
    current live-build for Ubuntu 22.04/24.04 whose stock 3.0~a57 fork cannot
    build a modern image.
  * Drop po4a and devscripts build-deps and skip translated man pages: po4a is
    in Ubuntu universe, which is not available in the OBS build root. English
    man pages and all functionality are unaffected.

 -- Ciro Iriarte <ciro.iriarte+software@gmail.com>  Wed, 19 Aug 2026 20:00:00 -0500

EOF
cat "${SRC}/debian/changelog" >> "${WORK}/entry"
mv "${WORK}/entry" "${SRC}/debian/changelog"

echo ":: Building native source package..."
( cd "${WORK}" && dpkg-source -b live-build )
cp "${WORK}/live-build_${NTVER}.tar.xz" "${WORK}/live-build_${NTVER}.dsc" ./
echo ":: Done -> $(ls live-build_${NTVER}.tar.xz live-build_${NTVER}.dsc)"
