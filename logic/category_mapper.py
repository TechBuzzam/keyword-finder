from config import CATEGORY_KEYWORDS


def map_category(keyword):
    """
    Maps a keyword to a StudyConcepts category based on keyword match.
    Returns category name or 'Uncategorized'.
    """
    k = keyword.lower()

    for category, words in CATEGORY_KEYWORDS.items():
        for w in words:
            if w in k:
                return category

    return "Uncategorized"
