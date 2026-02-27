#!/bin/bash
# update-nic-xray-version.sh
#
# Reads SCRIPT_VERSION (falling back to VERSION) from nic-xray.sh in the
# upstream repo and updates packages/nic-xray/_service with the new version.
# Run this whenever nic-xray.sh is updated upstream, then push to OBS.
#
# Usage:
#   ./scripts/update-nic-xray-version.sh [--push]
#
#   --push   also commit and push the updated package to OBS

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SERVICE_FILE="${REPO_ROOT}/packages/nic-xray/_service"
SCRIPT_URL="https://raw.githubusercontent.com/ciroiriarte/misc-scripts/main/nic-xray.sh"
OBS_PKG_DIR="/tmp/home:ciriarte:network-tools/nic-xray"

echo "Fetching nic-xray.sh from upstream..."
SCRIPT_CONTENT=$(curl -fsSL "${SCRIPT_URL}")

# Prefer SCRIPT_VERSION, fall back to VERSION
NEW_VERSION=$(echo "${SCRIPT_CONTENT}" | grep -E '^SCRIPT_VERSION=' | head -1 | cut -d'"' -f2)
if [[ -z "${NEW_VERSION}" ]]; then
    NEW_VERSION=$(echo "${SCRIPT_CONTENT}" | grep -E '^VERSION=' | head -1 | cut -d'"' -f2)
fi

if [[ -z "${NEW_VERSION}" ]]; then
    echo "ERROR: Could not find SCRIPT_VERSION or VERSION in nic-xray.sh" >&2
    exit 1
fi

echo "Detected script version: ${NEW_VERSION}"

# Read current version from _service
CURRENT_VERSION=$(grep '<param name="version">' "${SERVICE_FILE}" | head -1 | sed 's/.*<param name="version">\(.*\)<\/param>/\1/')
echo "Current package version: ${CURRENT_VERSION}"

if [[ "${NEW_VERSION}" == "${CURRENT_VERSION}" ]]; then
    echo "Version unchanged (${NEW_VERSION}). Nothing to do."
    exit 0
fi

echo "Updating _service: ${CURRENT_VERSION} -> ${NEW_VERSION}"
sed -i "s|<param name=\"version\">${CURRENT_VERSION}</param>|<param name=\"version\">${NEW_VERSION}</param>|" "${SERVICE_FILE}"

# Update changelogs
DATE_RPM=$(date -u "+%a %b %d %Y")
DATE_DEB=$(date -u "+%a, %d %b %Y %H:%M:%S +0000")

CHANGES_FILE="${REPO_ROOT}/packages/nic-xray/nic-xray.changes"
TMPFILE=$(mktemp)
cat > "${TMPFILE}" <<EOF
-------------------------------------------------------------------
${DATE_RPM} Ciro Iriarte <ciro.iriarte+software@gmail.com> - ${NEW_VERSION}-1

- Update to ${NEW_VERSION} (sync with SCRIPT_VERSION in nic-xray.sh)

EOF
cat "${CHANGES_FILE}" >> "${TMPFILE}"
mv "${TMPFILE}" "${CHANGES_FILE}"

DEB_CHANGELOG="${REPO_ROOT}/packages/nic-xray/debian.changelog"
TMPFILE=$(mktemp)
cat > "${TMPFILE}" <<EOF
nic-xray (${NEW_VERSION}-1) unstable; urgency=medium

  * Update to ${NEW_VERSION} (sync with SCRIPT_VERSION in nic-xray.sh)

 -- Ciro Iriarte <ciro.iriarte+software@gmail.com>  ${DATE_DEB}

EOF
cat "${DEB_CHANGELOG}" >> "${TMPFILE}"
mv "${TMPFILE}" "${DEB_CHANGELOG}"

echo "Updated:"
echo "  ${SERVICE_FILE}"
echo "  ${CHANGES_FILE}"
echo "  ${DEB_CHANGELOG}"

if [[ "${1:-}" == "--push" ]]; then
    echo ""
    echo "Pushing to OBS..."
    if [[ ! -d "${OBS_PKG_DIR}" ]]; then
        echo "OBS checkout not found at ${OBS_PKG_DIR}. Run: osc co home:ciriarte:network-tools" >&2
        exit 1
    fi
    cp "${REPO_ROOT}/packages/nic-xray/_service" "${OBS_PKG_DIR}/"
    cp "${REPO_ROOT}/packages/nic-xray/nic-xray.changes" "${OBS_PKG_DIR}/"
    cp "${REPO_ROOT}/packages/nic-xray/debian.changelog" "${OBS_PKG_DIR}/"
    cd "${OBS_PKG_DIR}"
    osc commit -m "Update nic-xray to ${NEW_VERSION}"
    echo "Pushed revision to OBS."
fi

echo ""
echo "Next steps:"
echo "  1. Review the changes"
echo "  2. Run with --push to commit to OBS, or manually:"
echo "     cp packages/nic-xray/* ${OBS_PKG_DIR}/"
echo "     cd ${OBS_PKG_DIR} && osc commit -m 'Update nic-xray to ${NEW_VERSION}'"
