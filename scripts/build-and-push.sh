#!/usr/bin/env bash
# Build the ninecat images natively and push them to GHCR.
#
# Same images the CI workflow produces (.github/workflows/build.yml), but built
# locally on a native arm64 host (e.g. georgettarm) — much faster than the
# cold-cache GitHub-hosted build, and a fallback when Actions is unavailable.
#
# One-time auth (token needs write:packages):
#   gh auth refresh -h github.com -s write:packages
#   gh auth token | docker login ghcr.io -u pankgeorg --password-stdin
#
# Usage:
#   scripts/build-and-push.sh           # tags :latest and :sha-<short>
#   scripts/build-and-push.sh v0.2.2    # also tags :v0.2.2
set -euo pipefail

REGISTRY="ghcr.io/pankgeorg"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHA="$(git -C "$ROOT" rev-parse --short HEAD)"
EXTRA_TAG="${1:-}"

build_and_push() {
  local name="$1" ctx="$2" file="$3"
  local tags=(-t "$REGISTRY/$name:latest" -t "$REGISTRY/$name:sha-$SHA")
  [ -n "$EXTRA_TAG" ] && tags+=(-t "$REGISTRY/$name:$EXTRA_TAG")
  DOCKER_BUILDKIT=1 docker build -f "$ROOT/$file" "${tags[@]}" "$ROOT/$ctx"
  docker push "$REGISTRY/$name:latest"
  docker push "$REGISTRY/$name:sha-$SHA"
  [ -n "$EXTRA_TAG" ] && docker push "$REGISTRY/$name:$EXTRA_TAG"
}

build_and_push ninecat-py  backend backend/Dockerfile
build_and_push ninecat-web .       Dockerfile

echo "pushed $REGISTRY/ninecat-{py,web}:latest (+ :sha-$SHA${EXTRA_TAG:+ + :$EXTRA_TAG})"
