#!/bin/bash
# update-nic-xray-version.sh
#
# Reads the latest release tag from github.com/ciroiriarte/nic-xray and
# updates packages/nic-xray/_service, nic-xray.changes, and debian.changelog.
#
# The GitHub Actions workflow (.github/workflows/update-nic-xray.yml) runs
# this logic daily. Use this script to trigger a manual update instead.
#
# Usage:
#   ./scripts/update-nic-xray-version.sh [--push]
#
#   --push   also commit and push the updated package to OBS

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SERVICE_FILE="${REPO_ROOT}/packages/nic-xray/_service"
OBS_PKG_DIR="/tmp/home:ciriarte:network-tools/nic-xray"

echo "Fetching latest release from github.com/ciroiriarte/nic-xray..."
LATEST_JSON=$(curl -fsSL \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/ciroiriarte/nic-xray/releases/latest")

TAG_NAME=$(echo "${LATEST_JSON}" | python3 -c \
    "import sys, json; print(json.load(sys.stdin)['tag_name'])")
NEW_VERSION="${TAG_NAME#v}"

if [[ -z "${NEW_VERSION}" ]]; then
    echo "ERROR: Could not determine latest version from GitHub releases" >&2
    exit 1
fi

echo "Latest upstream release: ${TAG_NAME} (version ${NEW_VERSION})"

# Read current version from _service
CURRENT_VERSION=$(grep '<param name="version">' "${SERVICE_FILE}" | head -1 \
    | sed 's/.*<param name="version">\(.*\)<\/param>/\1/')
echo "Current package version: ${CURRENT_VERSION}"

if [[ "${NEW_VERSION}" == "${CURRENT_VERSION}" ]]; then
    echo "Version unchanged (${NEW_VERSION}). Nothing to do."
    exit 0
fi

echo "Updating: ${CURRENT_VERSION} -> ${NEW_VERSION}"

sed -i "s|<param name=\"version\">${CURRENT_VERSION}</param>|<param name=\"version\">${NEW_VERSION}</param>|" "${SERVICE_FILE}"
sed -i "s|<param name=\"revision\">v${CURRENT_VERSION}</param>|<param name=\"revision\">v${NEW_VERSION}</param>|" "${SERVICE_FILE}"

DATE_RPM=$(date -u "+%a %b %d %Y")
DATE_DEB=$(date -u "+%a, %d %b %Y %H:%M:%S +0000")

CHANGES_FILE="${REPO_ROOT}/packages/nic-xray/nic-xray.changes"
TMPFILE=$(mktemp)
cat > "${TMPFILE}" <<EOF
-------------------------------------------------------------------
${DATE_RPM} Ciro Iriarte <ciro.iriarte+software@gmail.com> - ${NEW_VERSION}-1

- Update to ${NEW_VERSION}

EOF
cat "${CHANGES_FILE}" >> "${TMPFILE}"
mv "${TMPFILE}" "${CHANGES_FILE}"

DEB_CHANGELOG="${REPO_ROOT}/packages/nic-xray/debian.changelog"
TMPFILE=$(mktemp)
cat > "${TMPFILE}" <<EOF
nic-xray (${NEW_VERSION}-1) unstable; urgency=medium

  * Update to ${NEW_VERSION}

 -- Ciro Iriarte <ciro.iriarte+software@gmail.com>  ${DATE_DEB}

EOF
cat "${DEB_CHANGELOG}" >> "${TMPFILE}"
mv "${TMPFILE}" "${DEB_CHANGELOG}"

echo "Updated: _service, nic-xray.changes, debian.changelog"

if [[ "${1:-}" == "--push" ]]; then
    echo ""
    echo "Pushing to OBS..."
    if [[ ! -d "${OBS_PKG_DIR}" ]]; then
        echo "OBS checkout not found at ${OBS_PKG_DIR}. Run: osc co home:ciriarte:network-tools" >&2
        exit 1
    fi
    cp "${REPO_ROOT}/packages/nic-xray/_service" \
       "${REPO_ROOT}/packages/nic-xray/nic-xray.changes" \
       "${REPO_ROOT}/packages/nic-xray/debian.changelog" \
       "${OBS_PKG_DIR}/"
    cd "${OBS_PKG_DIR}"
    osc commit -m "Update nic-xray to ${NEW_VERSION}"
    echo "Pushed to OBS."
fi

echo ""
echo "Next steps (if not using --push):"
echo "  cp packages/nic-xray/_service packages/nic-xray/*.changes packages/nic-xray/debian.changelog \\"
echo "     ${OBS_PKG_DIR}/"
echo "  cd ${OBS_PKG_DIR} && osc commit -m 'Update nic-xray to ${NEW_VERSION}'"
