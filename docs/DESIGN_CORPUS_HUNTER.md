# Design corpus hunter

Cursor prompt for the operator Mac. It finds design material across lanes
and concepts, writes one manifest, and files it into one drawer.

A cloud agent that cannot read `/Users/fcaf` stops. It does not invent a
file list.

Ordinary housekeeping stays report-only. Moves and copies wait for a
later message that contains an exact phrase below.

## Consolidated space

`/Users/fcaf/Documents/AFSTYLE_BUSINESS_MASTER_ARCHIVE/Design_Corpus`

Lane folders use the existing lane names. Age does not split this drawer.
The age conveyor still governs every file this hunter does not accept.
Later housekeeping leaves `Design_Corpus` in place.

| Source | What the hunter does |
| --- | --- |
| Loose files on Desktop, Downloads, and Documents | Move into the corpus |
| `90_SOURCE_PRESERVATION`, Cursor source bundles, Cold Archive | Copy. The freezer stays in place |
| Live git working trees | Copy finished design files. Leave source code in the repo |
| iCloud or Drive placeholders that are not downloaded | Index the path. Do not force a download |
| Private, medical, crisis, tax, bank, and secret paths | Skip. Count them. Do not record the path |

`Design hunt: consolidate including frozen copies` is the only phrase that
moves files out of a preservation tree. Git working trees still stay in
place.

## How to run

1. Open this repository in Cursor on the Mac.
2. Run the command `design-corpus-hunter`, or paste the Prompt section
   into a new agent chat.
3. Read `Design_Corpus/_MANIFEST/summary-YYYY-MM-DD.md`.
4. Send `Design hunt: consolidate` to file a manifest that has no REVIEW
   rows.
5. Send `Design hunt: undo` to reverse the latest move log.

## What it searches

Local disks only. Synced iCloud and Google Drive folders count when they
are actually on the machine. The hunter does not log into Figma, Notion,
Canva, Slack, or mail.

Search roots, when they exist:

- `~/Desktop`, `~/Documents`, `~/Downloads`, `~/Pictures`
- `~/Library/CloudStorage`
- `~/Library/Mobile Documents/com~apple~CloudDocs`
- Mounted volumes under `/Volumes`, except Macintosh HD, Time Machine,
  and `com.apple*`

It skips dependency folders, `.git`, build output, mail, caches, Photos
libraries, and application bundles.

A file is in scope when any of these are true:

- It sits in a design folder (`design system`, `art direction`,
  `style guide`, `moodboard`, `logos`, `ui kit`, and the same family of
  names).
- The name matches a design phrase (logo, wordmark, mockup, wireframe,
  lookbook, brand guide, design tokens, visual identity).
- The extension is a design-source file (`.ai`, `.psd`, `.afdesign`,
  `.fig`, `.sketch`, `.svg` only with a design or concept signal, font
  files inside a design folder).
- Images and PDFs are included when the path also carries a design signal
  or a known concept. A random photo is left alone.

Known homes, included when the folder name is found anywhere under a
search root:

- `ChefWho_Design_System`
- `Esther_AI_Art_Direction`
- `Prompt_Library_2.5` (design files in that tree, not every prompt)
- `TRH_WTF_System` (design files in that tree, not the whole system)

Concept signals map to the existing lanes: ChefsWho.codes, Prompt Library
TRH, SWM Filings (Karina stays inside that lane), Rose Rocket. Esther and
anything else land in `Unmapped/<concept>`.

Folders named only `design`, `brand`, `figma`, `canva`, `framer`,
`webflow`, or `adobe` contribute visual files directly. Other files in
those folders stay REVIEW until a person sets a disposition.

Archives (`.zip`, `.dmg`, and the same family) and files over 2 GB stay
REVIEW. The apply step refuses to run while any REVIEW row remains.

## Prompt

```text
You are the Design Corpus Hunter for F.C Fernandez's Mac.

Begin a hunt reply with:
DESIGN CORPUS HUNT — MANIFEST ONLY

Begin a consolidate reply with:
DESIGN CORPUS CONSOLIDATE — FILING STARTED

Begin an undo reply with:
DESIGN CORPUS UNDO — RESTORE STARTED

If /Users/fcaf is not readable, stop after one sentence. Do not invent files.

Read docs/DESIGN_CORPUS_HUNTER.md and run only this script from the
repository root:

python3 docs/design_corpus_hunt.py hunt

The script is the search. Do not add a second crawl, and do not widen the
rules during the run.

Report the summary counts, the summary path, and up to 20 REVIEW paths.
Do not paste file contents. Do not print private paths. Do not commit the
corpus or the manifest into git.

Stop after the hunt. Filing happens only when a later user message is
exactly one of these phrases:

- Design hunt: consolidate
  Run: python3 docs/design_corpus_hunt.py apply --manifest <manifest> --confirm consolidate
  Use the manifest named in the summary. If REVIEW rows remain, list them
  and stop without applying.

- Design hunt: consolidate including frozen copies
  Same apply command, plus --include-frozen-moves.
  Git working trees still stay in place. The script enforces that.

- Design hunt: undo
  Run: python3 docs/design_corpus_hunt.py undo --corpus <Design_Corpus> --confirm undo

Leave Design_Corpus where it is. Do not split it by age.
```
