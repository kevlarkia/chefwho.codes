#!/usr/bin/env bash
# Copy mirrored Rose Rocket Engine files into an upstream checkout.
set -euo pipefail

MIRROR_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="${1:-}"

if [[ -z "${TARGET_ROOT}" ]]; then
  echo "Usage: $0 /path/to/rose-rocket-engine" >&2
  exit 2
fi

if [[ ! -d "${TARGET_ROOT}" ]]; then
  echo "Target directory does not exist: ${TARGET_ROOT}" >&2
  exit 1
fi

if [[ ! -f "${TARGET_ROOT}/rose_rocket_engine.py" ]]; then
  echo "Target does not look like rose-rocket-engine: ${TARGET_ROOT}" >&2
  exit 1
fi

rsync -a \
  --exclude 'UPSTREAM_APPLY.md' \
  --exclude 'scripts/' \
  --exclude 'patches/' \
  --exclude 'output/' \
  --exclude '.venv/' \
  --exclude '__pycache__/' \
  --exclude '.pytest_cache/' \
  --exclude '.ruff_cache/' \
  --exclude 'feature_cooldowns.json' \
  "${MIRROR_ROOT}/" "${TARGET_ROOT}/"

echo "Synced mirror -> ${TARGET_ROOT}"
echo "Review with: git -C ${TARGET_ROOT} status"
