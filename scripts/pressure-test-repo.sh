#!/usr/bin/env bash
# Lane: repo-pressure — cold-start truth vs AGENTS.md / CI / key paths.
# Exit 0 = PASS, non-zero = FAIL. Print findings to stdout.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0
infos=0

pass() { printf 'PASS  %s\n' "$1"; }
fail() { printf 'FAIL  %s\n' "$1"; failures=$((failures + 1)); }
info() { printf 'INFO  %s\n' "$1"; infos=$((infos + 1)); }

require_path() {
  local p="$1"
  if [[ -e "$ROOT/$p" ]]; then
    pass "exists: $p"
  else
    fail "missing: $p"
  fi
}

echo "=== repo-pressure ==="
echo "root: $ROOT"
echo

echo "-- required paths --"
REQUIRED_PATHS=(
  package.json
  AGENTS.md
  docs/SYSTEMS_HEALTH.md
  docs/audits/AUDIT_LOG_TEMPLATE.md
  docs/prompts/session-save-state.md
  docs/prompts/session-resume.md
  docs/prompts/systems-health-audit.md
  .env.example
  .github/workflows/ci.yml
)
for p in "${REQUIRED_PATHS[@]}"; do
  require_path "$p"
done

echo
echo "-- AGENTS.md repository-map paths --"
# Paths in the Repository map table (portable; no GNU awk required).
MAP_PATHS=()
while IFS= read -r line; do
  MAP_PATHS+=("$line")
done < <(
  awk '
    /^### Repository map$/ { in_map=1; next }
    in_map && /^### / { exit }
    in_map && /^\| `/ {
      line=$0
      sub(/^\| `/, "", line)
      sub(/`.*/, "", line)
      if (line != "") print line
    }
  ' AGENTS.md
)
if [[ ${#MAP_PATHS[@]} -eq 0 ]]; then
  fail "could not parse Repository map paths from AGENTS.md"
else
  for p in "${MAP_PATHS[@]}"; do
    if [[ "$p" == *"*"* ]]; then
      base="${p%%\**}"
      if [[ -d "$ROOT/$base" ]] || [[ -e "$ROOT/$base" ]]; then
        pass "map path (glob base): $p"
      else
        fail "map path missing (glob base): $p"
      fi
    else
      require_path "$p"
    fi
  done
fi

echo
echo "-- package.json scripts (AGENTS quality gates) --"
for script in lint typecheck build pressure-test; do
  if node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts['$script'] ? 0 : 1)"; then
    pass "package.json scripts.$script"
  else
    fail "package.json missing scripts.$script"
  fi
done

echo
echo "-- CI workflow jobs --"
CI_FILE=".github/workflows/ci.yml"
if grep -qE '^[[:space:]]*markdown-lint:' "$CI_FILE"; then
  pass "ci.yml job: markdown-lint"
else
  fail "ci.yml missing job: markdown-lint"
fi
if grep -qE '^[[:space:]]*workflow-lint:' "$CI_FILE"; then
  pass "ci.yml job: workflow-lint"
else
  fail "ci.yml missing job: workflow-lint"
fi

echo
echo "-- no competing systems-health docs at repo root --"
found_dup=0
for f in SYSTEMS_HEALTH.md SYSTEMS_HEALTH.mdc systems-health.md; do
  if [[ -e "$ROOT/$f" ]]; then
    fail "competing systems-health doc at repo root: $f (canonical is docs/SYSTEMS_HEALTH.md)"
    found_dup=1
  fi
done
if [[ "$found_dup" -eq 0 ]]; then
  pass "no SYSTEMS_HEALTH duplicate at repo root"
fi

echo
if [[ "$failures" -eq 0 ]]; then
  echo "Verdict: PASS ($infos info)"
  exit 0
fi
echo "Verdict: FAIL ($failures failure(s))"
exit 1
