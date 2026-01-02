from config import EDUCATIONAL_PREFIXES, EDUCATIONAL_KEYWORDS


def is_educational(keyword):
    """
    Returns True if keyword matches educational intent.
    """
    k = keyword.lower().strip()

    # Check prefix patterns
    for prefix in EDUCATIONAL_PREFIXES:
        if k.startswith(prefix):
            return True

    # Check if contains educational keywords
    for word in EDUCATIONAL_KEYWORDS:
        if word in k:
            return True

    return False


def filter_educational(keywords):
    """
    Filters list of keywords to only educational ones.
    """
    return [k for k in keywords if is_educational(k)]
