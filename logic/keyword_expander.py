import requests
import time
from config import EDUCATIONAL_PREFIXES


SUGGEST_URL = "https://suggestqueries.google.com/complete/search"


def google_suggest(keyword):
    """
    Fetch Google autocomplete suggestions for a keyword.
    """
    try:
        params = {"client": "firefox", "q": keyword}
        r = requests.get(SUGGEST_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data[1] if len(data) > 1 else []
    except Exception:
        return []


def expand_with_templates(seed):
    """
    Expand keyword using predefined educational templates.
    """
    expanded = []
    for prefix in EDUCATIONAL_PREFIXES:
        expanded.append(f"{prefix} {seed}")
    return expanded


def expand_keywords(seed_keywords, delay=0.5):
    """
    Given a list of seed keywords, expand into long-tail keywords.
    """
    results = set()

    for seed in seed_keywords:
        seed = seed.strip().lower()

        # Add template-based expansions
        for k in expand_with_templates(seed):
            results.add(k)

        # Add Google Suggest expansions
        suggestions = google_suggest(seed)
        for s in suggestions:
            results.add(s.strip().lower())

        time.sleep(delay)  # be polite to Google

    return list(results)
