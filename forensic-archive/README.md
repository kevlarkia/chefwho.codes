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
| `openai` | `OPENAI_API_KEY` | `OpenAILLMClient` |
| `vertex` | `GOOGLE_CLOUD_PROJECT`, `VERTEX_ACCESS_TOKEN` | `VertexLLMClient` |

To use your own wrapper, inject it:

```python
from forensic_archive import ForensicArchiver

archiver = ForensicArchiver(client=MyClient(), profile="swm")
archiver.run(source, output_dir)
```

`MyClient.complete(prompt, *, system=None) -> str` is the only required
method.

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
