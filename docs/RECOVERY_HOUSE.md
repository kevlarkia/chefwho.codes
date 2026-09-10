# Recovery pipeline house

The recovery pipeline is **not** part of the chefwho.codes personal site.
It gets its own GitHub house. This file is the filled signup record plus
the inventory of what moves.

**Status:** Documented 2026-09-10. Org not created in-repo yet. Trees still
live in `kevlarkia/chefwho.codes` until the house exists and the transfer
runs.

## What the house holds

| Path in this repo today | Role in the house |
| --- | --- |
| `swm-recovery/` | SWM extraction suite (prompts, registers, runs, sources, Cursor plugin) |
| `forensic-archive/` | Dual-pass TEMP-ARC runtime + `forensic_archive.sqlite` ledger |
| `docs/RECOVERY_HOUSE.md` | This record (moves with the house) |

SWM is one profile of the archive runtime, not the whole house.

## What stays in chefwho.codes

| Path | Role |
| --- | --- |
| `app/`, `content/`, `lib/` | Personal site |
| `rose-rocket-engine/` | Newsletter mirror (separate product) |
| Site docs (`POLICIES.md`, `SYSTEMS_HEALTH.md`, rebuild/migration plans) | Site + SWa Works planning |

Existing enterprise **SWa Works** (`https://github.com/enterprises/swa-works`)
and org **Chefwho.Codes** stay the site container. They are not the recovery
house.

## GitHub signup values

The GitHub form that was open is **Enterprise Managed Users** (a new
enterprise that provisions member accounts from an IdP). That is heavier
than a normal organization. Prefer a **standard organization** under
existing SWa Works if the goal is only a separate house for these trees.
Use the same names either way.

| Field | Value |
| --- | --- |
| House type (preferred) | Standard GitHub Organization under SWa Works |
| House type (form that was open) | Enterprise Managed Users (separate enterprise) |
| Data hosting | Host on GitHub.com without data residency |
| Display name | SWa Works Managed |
| URL slug | `swa-works-managed` |
| URL | `https://github.com/enterprises/swa-works-managed` (EMU) or `https://github.com/swa-works-managed` (standard org) |
| Username shortcode (EMU only, permanent) | `swa` |
| Setup admin (EMU only) | `swa_admin` |
| Member handle example (EMU only) | `clinton_swa` |
| Industry | Software / internet |
| Number of employees | 0–50 |
| Country / Region | United States of America |
| Identity provider | Microsoft Entra ID if `af.style` is on Microsoft 365; otherwise Custom or other |
| Do not pick | Okta, PingFederate (unless already in production) |
| Admin name | F.C Fernandez |
| Admin work email | `clinton@af.style` |
| Trial notice | Check if starting a GitHub trial |
| Customer agreement | Check if the admin can accept for the org |
| Marketing emails | Leave unchecked |

If slug `swa-works-managed` is taken, use `swaworks-emu` (EMU) or
`swa-recovery` (standard org).

## After the house exists

1. Create an empty repo in the new house (suggested name: `recovery-pipeline`).
2. Move `swm-recovery/` and `forensic-archive/` there. Keep history if
   practical (`git subtree` or `git filter-repo`).
3. Point this repo at the new home with a short stub README in each old
   path.
4. Update `AGENTS.md` in both repos in the same change.

Until that transfer, treat the two trees as **guests** in chefwho.codes.
