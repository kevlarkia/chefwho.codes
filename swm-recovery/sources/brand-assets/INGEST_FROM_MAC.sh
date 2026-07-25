#!/usr/bin/env bash
# Run on the operator Mac from the repo root after pulling this branch.
# Copies authorized brand sources into gitignored content/ drop zones.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

copy_one() {
  local src="$1"
  local dest_dir="$2"
  mkdir -p "$dest_dir"
  if [[ -f "$src" ]]; then
    cp -p "$src" "$dest_dir/"
    echo "OK  -> $dest_dir/$(basename "$src")"
  else
    echo "MISS: $src"
  fi
}

copy_one \
  "/Users/fcaf/Downloads/SWM_Institutional_Documentation_Suite_v1.0/08_SWM_Brand_Standards_Manual_v1.0.md" \
  "$ROOT/SRC-BRAND-001-brand-standards-manual/content"

copy_one \
  "/Users/fcaf/Documents/AFSTYLE_BUSINESS_MASTER_ARCHIVE/90_SOURCE_PRESERVATION/Local_Files/Downloads/files 3/SWM-Setup-05-Trademark-Brand.pdf" \
  "$ROOT/SRC-BRAND-002-trademark-brand-pdf/content"

copy_one \
  "/Users/fcaf/Documents/AFSTYLE_BUSINESS_MASTER_ARCHIVE/90_SOURCE_PRESERVATION/Cursor/CURSOR_SOURCE_BUNDLE_2026-07-21/files/Library/Mobile Documents/com~apple~CloudDocs/SWM_Institutional_Documentation_Suite_v1.0/05_SWM_Investor_Pitch_Deck_v1.0.md" \
  "$ROOT/SRC-BRAND-003-investor-pitch-deck/content"

copy_one \
  "/Users/fcaf/Documents/AFSTYLE_BUSINESS_MASTER_ARCHIVE/90_SOURCE_PRESERVATION/Local_Files/Library/Mobile Documents/com~apple~CloudDocs/SWM_Institutional_Documentation_Suite_v1.0/02_SWM_Master_Business_Plan_v1.0.md" \
  "$ROOT/SRC-BRAND-004-master-business-plan/content"

copy_one \
  "/Users/fcaf/Documents/AFSTYLE_BUSINESS_MASTER_ARCHIVE/90_SOURCE_PRESERVATION/Cursor/CURSOR_SOURCE_BUNDLE_2026-07-21/files/Library/Mobile Documents/com~apple~CloudDocs/SWM Business OS v0.1 INTERNAL.pdf" \
  "$ROOT/SRC-BRAND-005-business-os-pdf/content"

copy_one \
  "/Users/fcaf/Documents/AFSTYLE_BUSINESS_MASTER_ARCHIVE/03_CORPORATE_AND_LEGAL/AFS-REC-000793_AFSTYLE_03_09_SWM_AI_Governance_Manual_v1.0_UNDATED_CANON-CANDIDATE_vUnknown.md" \
  "$ROOT/SRC-BRAND-006-ai-governance-manual/content"

copy_one \
  "/Users/fcaf/Downloads/_packages/afstyle-install-20260509-v1/SWM/SWM_EX002_INST-002_RPRT_20260509.docx" \
  "$ROOT/SRC-BRAND-007-ex002-report/content"

copy_one \
  "/Users/fcaf/Documents/Name Identity project/SWM-RECON-20260724-01-Consolidation/03_Additional_Local_SWM_Sources/from_Name_Identity_project/SWM-Universal-Recovery-Sweep-Prompt-v1.0.zip" \
  "$ROOT/SRC-BRAND-008-universal-recovery-sweep-zip/content"

copy_one \
  "/Users/fcaf/Documents/Name Identity project/SWM-RECON-20260724-01-Consolidation/03_Additional_Local_SWM_Sources/from_Downloads/SWM_Skills_Pack/swm-standing-rules.zip" \
  "$ROOT/SRC-BRAND-009-standing-rules-zip/content"

echo "Done. Re-run cloud extraction after syncing content/ into the agent workspace."
