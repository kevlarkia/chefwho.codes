import json
import os
from datetime import datetime
from pathlib import Path

import google.generativeai as genai

from ai_news_scraper import fetch_hn_ai_stories
from gmail_draft_creator import create_gmail_draft

COOLDOWN_FILE = Path("feature_cooldowns.json")
DEFAULT_COOLDOWN_DAYS = 7
FORCE_EDITION_ENV = "FORCE_EDITION"
DRY_RUN_ENV = "DRY_RUN"
OFFLINE_DRY_RUN_ENV = "OFFLINE_DRY_RUN"
OUTPUT_DIR = Path("output")
MOCK_STORIES_PATH = Path("fixtures/mock_stories.json")

# Runs before final newsletter output is accepted.
BANNED_WORDS = [
    "slur-example-1",
    "slur-example-2",
    "clickbait",
]

EDITION_ROUTING = {
    0: "Monday Market Radar",
    2: "Wednesday Builder Brief",
    4: "Friday Frontier Signals",
}


def _now_local() -> datetime:
    """Local wall-clock time from OS timezone settings."""
    return datetime.now()


def _today_utc() -> datetime:
    # Kept for backward compatibility in case other modules call it.
    return datetime.utcnow()


def _is_truthy_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _load_cooldowns() -> dict[str, dict[str, str]]:
    if not COOLDOWN_FILE.exists():
        return {"last_used": {}}
    return json.loads(COOLDOWN_FILE.read_text(encoding="utf-8"))


def _save_cooldowns(data: dict[str, dict[str, str]]) -> None:
    COOLDOWN_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _days_since(date_str: str) -> int:
    previous = datetime.fromisoformat(date_str)
    return (_now_local() - previous).days


def _eligible_features(cooldowns: dict[str, dict[str, str]], candidates: list[str]) -> list[str]:
    last_used = cooldowns.get("last_used", {})
    eligible = []
    for feature in candidates:
        used_at = last_used.get(feature)
        if not used_at:
            eligible.append(feature)
            continue
        if _days_since(used_at) >= DEFAULT_COOLDOWN_DAYS:
            eligible.append(feature)
    return eligible


def _select_feature_for_today() -> str:
    candidates = [
        "Tooling Spotlight",
        "Founder Tactic",
        "Prompt Pattern",
        "AI Ops Shortcut",
        "Growth Experiment",
    ]

    cooldowns = _load_cooldowns()
    eligible = _eligible_features(cooldowns, candidates)

    # Fallback if all are in cooldown.
    if not eligible:
        eligible = candidates

    selected = eligible[0]
    cooldowns.setdefault("last_used", {})[selected] = _now_local().isoformat()
    _save_cooldowns(cooldowns)
    return selected


def _validate_content_filter(text: str) -> None:
    normalized = text.lower()
    hits = [w for w in BANNED_WORDS if w.lower() in normalized]
    if hits:
        raise ValueError(f"Content filter blocked output due to banned words: {hits}")


def _edition_for_today() -> str:
    """
    Returns the scheduled edition for today.
    If FORCE_EDITION env var is truthy, bypass schedule gate for test runs.
    """
    if _is_truthy_env(FORCE_EDITION_ENV):
        return "Forced Test Edition"

    weekday = _now_local().weekday()  # Monday=0 ... Sunday=6 (LOCAL TIME)
    if weekday not in EDITION_ROUTING:
        raise RuntimeError("Publishing is only scheduled for Monday/Wednesday/Friday.")
    return EDITION_ROUTING[weekday]


def _assemble_prompt(edition_name: str, feature: str, stories: list[dict[str, str]]) -> str:
    story_lines = "\n".join(f"- {s['title']} ({s['url']})" for s in stories)
    return f"""
You are writing the {edition_name} edition of Rose Rocket Engine.

Constraints:
- Keep output under 30,000 characters.
- Crisp, operator-focused insights.
- Include feature section: {feature}

Source stories:
{story_lines}

Output sections:
1) Opening hook
2) 3-5 curated story summaries
3) {feature}
4) Actionable takeaways
""".strip()


def _load_mock_stories() -> list[dict[str, str]]:
    if MOCK_STORIES_PATH.exists():
        data = json.loads(MOCK_STORIES_PATH.read_text(encoding="utf-8"))
        stories = data.get("stories", []) if isinstance(data, dict) else data
        if isinstance(stories, list) and stories:
            normalized = []
            for item in stories:
                if isinstance(item, dict) and "title" in item and "url" in item:
                    normalized.append({"title": str(item["title"]), "url": str(item["url"])})
            if normalized:
                return normalized

    return [
        {"title": "Open-source eval harnesses are becoming standard AI stack components", "url": "https://example.com/story/eval-harnesses"},
        {"title": "Founders adopt small-model routing to cut inference spend", "url": "https://example.com/story/model-routing"},
        {"title": "Structured output validation reduces production incident rates", "url": "https://example.com/story/structured-validation"},
        {"title": "Teams operationalize weekly prompt review rituals", "url": "https://example.com/story/prompt-rituals"},
        {"title": "LLM-powered triage assistants improve support response times", "url": "https://example.com/story/support-triage"},
    ]


def _generate_offline_newsletter_text(edition_name: str, feature: str, stories: list[dict[str, str]]) -> str:
    top = stories[:5]
    summaries = "\n".join(
        f"- **{s['title']}** — Practical signal for operators. Source: {s['url']}" for s in top
    )

    return f"""## {edition_name}

Quick offline simulation edition for local testing and prompt-tuning.

### Curated stories
{summaries}

### {feature}
Use a planner → executor prompt split in one workflow this week and compare output quality.

### Actionable takeaways
1. Automate one repeatable workflow to ~60% before human approval.
2. Add one feedback capture point to your core AI output.
3. Use model-tier routing to reduce latency/cost.
4. Validate structured outputs before downstream actions.
""".strip()


def generate_newsletter_text() -> str:
    edition_name = _edition_for_today()
    feature = _select_feature_for_today()

    if _is_truthy_env(OFFLINE_DRY_RUN_ENV):
        stories = _load_mock_stories()
        text = _generate_offline_newsletter_text(edition_name, feature, stories)
        _validate_content_filter(text)
        return text

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise OSError("Missing required environment variable: GEMINI_API_KEY")

    stories = fetch_hn_ai_stories(limit=10)

    if not stories:
        raise RuntimeError("No AI-related stories found on Hacker News.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = _assemble_prompt(edition_name, feature, stories)
    response = model.generate_content(prompt)
    text = response.text or ""

    if len(text) > 30000:
        text = text[:29900] + "\n\n[Truncated to remain under 30,000 characters]"

    _validate_content_filter(text)
    return text


def _save_dry_run_output(subject: str, body: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"newsletter-{_now_local().date().isoformat()}.md"
    path = OUTPUT_DIR / filename
    path.write_text(f"# {subject}\n\n{body}\n", encoding="utf-8")
    return path


def run() -> None:
    edition_name = _edition_for_today()
    body = generate_newsletter_text()

    subject = f"Rose Rocket Engine — {edition_name} — {_now_local().date().isoformat()}"

    if _is_truthy_env(OFFLINE_DRY_RUN_ENV):
        output_path = _save_dry_run_output(subject, body)
        print("OFFLINE_DRY_RUN enabled: skipping Gemini and Gmail API calls.")
        print(f"Saved output to: {output_path}")
        print("\n--- BEGIN NEWSLETTER ---\n")
        print(body)
        print("\n--- END NEWSLETTER ---")
        return

    if _is_truthy_env(DRY_RUN_ENV):
        output_path = _save_dry_run_output(subject, body)
        print("DRY_RUN enabled: skipping Gmail draft creation.")
        print(f"Saved output to: {output_path}")
        print("\n--- BEGIN NEWSLETTER ---\n")
        print(body)
        print("\n--- END NEWSLETTER ---")
        return

    draft_id = create_gmail_draft(subject=subject, body=body)
    print(f"Draft created successfully: {draft_id}")


if __name__ == "__main__":
    run()
