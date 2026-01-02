import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from config import FORUM_DOMAINS, STRONG_DOMAINS, MAX_SERP_RESULTS


DUCKDUCKGO_URL = "https://html.duckduckgo.com/html/"


def fetch_serp(query):
    """
    Fetch top SERP results from DuckDuckGo.
    Returns list of dicts: {domain, title, snippet}
    """
    try:
        r = requests.post(DUCKDUCKGO_URL, data={"q": query}, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        for res in soup.select(".result")[:MAX_SERP_RESULTS]:
            a = res.select_one(".result__a")
            s = res.select_one(".result__snippet")

            if not a:
                continue

            link = a.get("href", "")
            title = a.text.strip()
            snippet = s.text.strip() if s else ""

            domain = urlparse(link).netloc.replace("www.", "")

            results.append({
                "domain": domain,
                "title": title,
                "snippet": snippet
            })

        return results

    except Exception:
        return []


def analyze_competition(query):
    """
    Returns a dict of competition signals and opportunity score (0–4).
    """
    results = fetch_serp(query)
    domains = [r["domain"] for r in results]

    if not results:
        return {"score": 4, "reason": "no_results"}

    forum_hits = sum(any(f in d for f in FORUM_DOMAINS) for d in domains)
    strong_hits = sum(any(s in d for s in STRONG_DOMAINS) for d in domains)
    diversity = len(set(domains))
    total = len(domains)

    # Signal 1: Few results
    score = 0
    if total <= 3:
        score += 2
    elif total <= 7:
        score += 1

    # Signal 2: Weak competitors (forums)
    if forum_hits / total > 0.5:
        score += 1

    # Signal 3: Few strong authoritative sites
    if strong_hits == 0:
        score += 1

    return {
        "score": score,  # 0 (hard) → 4 (easy)
        "total_results": total,
        "forum_ratio": round(forum_hits / total, 2),
        "strong_sites": strong_hits,
        "diversity": diversity
      }
