import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from config import FORUM_DOMAINS

def get_domains(query):
    r = requests.post("https://html.duckduckgo.com/html/", data={"q": query})
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select(".result__a")
    return [urlparse(l["href"]).netloc.replace("www.", "") for l in links]

def competition_level(domains):
    if not domains:
        return "VERY LOW"
    forum_hits = sum(any(f in d for f in FORUM_DOMAINS) for d in domains)
    if forum_hits / len(domains) > 0.6:
        return "LOW"
    if len(domains) > 8:
        return "HIGH"
    return "MEDIUM"
