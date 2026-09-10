# Forensic archive runtime

Domain-neutral two-pass archive pipeline. A dummy LLM client ships so the
ledger can run offline. Swap that client for Anthropic, OpenAI, or Google
Vertex when you want live model calls.

**House:** This runtime lives with the recovery pipeline, not the
chefwho.codes site. Intended GitHub home and signup values:
[`../docs/RECOVERY_HOUSE.md`](../docs/RECOVERY_HOUSE.md).

**SWM is one profile**, not the product. Use `--profile swm` to apply
recovery-first addenda from the SWM extraction suite. The same runtime
packages any other authorized source with `--profile generic`.

## How to deploy this

### 1. Connect your API

`ForensicArchiver.primary_extraction_call` and
`ForensicArchiver.secondary_validation_call` already call an injected
`LLMClient`. The default is `DummyLLMClient`.

Swap the dummy by setting `FORENSIC_LLM_PROVIDER` or passing
`--provider`:

| Provider | Required env | Wrapper |
| --- | --- | --- |
| `dummy` | none | Offline stand-in (default) |
| `anthropic` | `ANTHROPIC_API_KEY` | `AnthropicLLMClient` |
| `openai` | `OPENAI_API_KEY` or `OPENAI_ACCESS_TOKEN` | `OpenAILLMClient` |
| `vertex` | `GOOGLE_CLOUD_PROJECT`, `VERTEX_ACCESS_TOKEN` | `VertexLLMClient` |

### OpenAI API overview

The OpenAI wrapper calls the HTTP API directly (no browser, no client-side
key). It follows the official overview:

- **Surface:** `POST /v1/responses` by default (`input` + optional
  `instructions`). Set `OPENAI_API_SURFACE=chat` only if you need Chat
  Completions.
- **Auth:** `Authorization: Bearer` from `OPENAI_API_KEY`, or a short-lived
  `OPENAI_ACCESS_TOKEN` from workload identity federation.
- **Org / project:** if the key can see more than one organization, set
  `OPENAI_ORGANIZATION` and `OPENAI_PROJECT`. Those become
  `OpenAI-Organization` and `OpenAI-Project`.
- **Request IDs:** each TEMP-ARC call sends `X-Client-Request-Id`
  (`{run_id}:primary` / `{run_id}:secondary`, ASCII, ≤512). The server
  `x-request-id` and rate-limit headers are stored in `archive.json` under
  `llm` and on `llm_calls` in the ledger. Log those IDs when you file a
  support ticket.
- **Storage:** `store` is `false` so prompts are not retained on OpenAI.
  Set `OPENAI_STORE=true` only if you want their stateful store.
- **Pin the model** (`OPENAI_MODEL=gpt-4.1-…`) if you need stable
  prompting between snapshots.

Do not put the key in frontend code. Keep custom header values under
60 KiB so the request stays inside the 64 KiB header budget.

To use your own wrapper, inject it:

```python
from forensic_archive import ForensicArchiver

archiver = ForensicArchiver(client=MyClient(), profile="swm")
archiver.run(source, output_dir)
```

`MyClient.complete(prompt, *, system=None, client_request_id=None) -> str`
is the only required method. Extra keywords may be ignored.

### 2. Adjust the prompt

`prompts/TEMP-ARC-002-secondary-validation.md` instructs the validator to
end with a JSON object whose `exclusions` value is an array. The Python
parser (`parse_exclusions`) reads that tail into the `exclusions`
variable. If you edit the prompt, keep that trailing JSON contract.

### 3. Database portability

SQLite stores the run in a single file, `forensic_archive.sqlite`, written
next to `archive.json`. Copy the whole output directory. The database is
the immutable ledger that records source hash, both LLM calls, inclusions,
exclusions, and the archive snapshot hash — proof of how the museum-quality
archive was generated. Tables reject `UPDATE` and `DELETE`.

Each run also writes an immutable snapshot at
`runs/<run_id>/archive.json`, plus `MANIFEST.json` and `SHA256SUMS`.
`python3 -m forensic_archive verify output/demo` recomputes those hashes
and fails closed if the package was tampered with.

## Run

```bash
cd forensic-archive
python3 -m forensic_archive archive fixtures/sample-source.md --output output/demo
python3 -m forensic_archive archive fixtures/swm-source.md --output output/swm --profile swm
python3 -m forensic_archive verify output/demo
```

## Tests

```bash
cd forensic-archive
pip install -r requirements-dev.txt
pytest
```
