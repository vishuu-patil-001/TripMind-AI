#!/usr/bin/env bash
# Collects the static frontend into dist/ for Vercel.
#
# Only the frontend is copied, so the Python source, Dockerfile and compose
# files are never published to the CDN.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$ROOT/dist"

rm -rf "$DIST"
mkdir -p "$DIST/static"

cp "$ROOT/frontend/templates/index.html" "$DIST/index.html"
cp -r "$ROOT/frontend/static/." "$DIST/static/"

echo "built dist/:"
find "$DIST" -type f | sed "s|$DIST|  dist|"
