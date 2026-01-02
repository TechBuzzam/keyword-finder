import requests

def google_suggest(keyword):
    url = "https://suggestqueries.google.com/complete/search"
    params = {"client": "firefox", "q": keyword}
    return requests.get(url, params=params).json()[1]

def expand_keywords(seeds):
    expanded = set()
    for s in seeds:
        try:
            for k in google_suggest(s):
                expanded.add(k.lower())
        except:
            pass
    return list(expanded)
