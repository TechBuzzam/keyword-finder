# -------------------------------
# StudyConcepts Keyword Finder Configuration
# -------------------------------

# 1️⃣ Educational intent patterns
EDUCATIONAL_PREFIXES = [
    "what is", "why", "how", "explain", "define", "difference between",
    "types of", "steps of", "importance of", "examples of"
]

EDUCATIONAL_KEYWORDS = [
    "definition", "explain", "steps", "types", "importance",
    "examples", "difference", "process", "function", "working", "mechanism"
]

# 2️⃣ Subject category mapping (StudyConcepts.in focus)
CATEGORY_KEYWORDS = {
    "Physics": ["force", "energy", "motion", "gravity", "electric", "current", "voltage", "wave", "optics", "quantum"],
    "Biology": ["cell", "dna", "photosynthesis", "respiration", "mitosis", "meiosis", "enzyme", "ecosystem"],
    "Environment": ["pollution", "climate", "greenhouse", "recycling", "biodiversity", "sustainability"],
    "Health": ["nutrition", "disease", "immunity", "vaccination", "virus", "bacteria", "hygiene"],
    "Astronomy": ["planet", "star", "galaxy", "black hole", "universe", "nebula", "telescope", "orbit"],
    "General Knowledge": ["history", "invention", "discovery", "capital", "constitution"]
}

# 3️⃣ Domains classification for competition analysis

FORUM_DOMAINS = [
    "quora.com", "reddit.com", "stackexchange.com", "superuser.com",
    "medium.com", "answers.yahoo.com"
]

STRONG_DOMAINS = [
    "wikipedia.org", "geeksforgeeks.org", "tutorialspoint.com",
    "w3schools.com", "ibm.com", "microsoft.com", "aws.amazon.com",
    "nasa.gov", "britannica.com"
]

# 4️⃣ Scoring thresholds

MIN_TREND_SCORE = 5           # Below this = no demand
MIN_FINAL_SCORE = 6           # Only show keywords >= this

# 5️⃣ Weights for scoring engine

WEIGHTS = {
    "educational_intent": 2,
    "question_pattern": 2,
    "low_competition": 3,
    "weak_title_match": 1,
    "short_snippet": 1,
    "trend": 2
}

# 6️⃣ SERP scraping limits
MAX_SERP_RESULTS = 10
