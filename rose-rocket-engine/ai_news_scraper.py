import requests
from bs4 import BeautifulSoup

HN_BASE_URL = "https://news.ycombinator.com"

DEFAULT_AI_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "llm",
    "gpt",
    "gemini",
    "openai",
    "anthropic",
    "deepmind",
    "transformer",
    "machine learning",
]


def _normalize(text: str) -> str:
    return (text or "").strip().lower()


def _contains_ai_keyword(text: str, keywords: list[str]) -> bool:
    haystack = _normalize(text)
    return any(_normalize(k) in haystack for k in keywords)


def fetch_hn_ai_stories(limit: int = 15, keywords: list[str] = None) -> list[dict[str, str]]:
    """
    Scrape Hacker News front page and return stories matching AI-related keywords.

    Returns a list of dicts:
    {
      "title": <story title>,
      "url": <external url or HN item link>,
      "source": "Hacker News"
    }
    """
    keywords = keywords or DEFAULT_AI_KEYWORDS
    response = requests.get(HN_BASE_URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("tr.athing")

    results = []
    for row in rows:
        title_link = row.select_one("span.titleline > a")
        if not title_link:
            continue

        title = title_link.get_text(strip=True)
        href = title_link.get("href", "")

        # Normalize relative HN links to absolute links
        if href.startswith("item?id="):
            href = f"{HN_BASE_URL}/{href}"
        elif href.startswith("/"):
            href = f"{HN_BASE_URL}{href}"

        if _contains_ai_keyword(title, keywords) or _contains_ai_keyword(href, keywords):
            results.append(
                {
                    "title": title,
                    "url": href,
                    "source": "Hacker News",
                }
            )

        if len(results) >= limit:
            break

    return results
