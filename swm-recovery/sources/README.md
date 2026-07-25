# Authorized sources drop zone

Place only **explicitly authorized** SWM source materials here before
running Prompts 1–5.

## Active bundles

| Bundle | Focus | Index |
| --- | --- | --- |
| [`brand-assets/`](brand-assets/) | Logos & visuals (9 authorized Mac paths) | [AUTHORIZED_SOURCE_INDEX.md](brand-assets/AUTHORIZED_SOURCE_INDEX.md) |

Mac ingest helper (run locally):
`brand-assets/INGEST_FROM_MAC.sh`

Suggested layout:

```text
sources/
  <bundle>/
    SRC-...-<short-name>/
      SOURCE-META.md
      content/          # gitignored originals
```

Each `SOURCE-META.md` should record:

- Source Identifier
- File/Conversation Name
- Platform
- Date
- Author/System
- Version
- Exact Location
- Authorization note

Do not commit secrets, credentials, or private relationship / medical /
legal / crisis materials. `content/` is gitignored.

