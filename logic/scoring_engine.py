import pandas as pd

from config import MIN_TREND_SCORE, MIN_FINAL_SCORE, WEIGHTS
from logic.trends_loader import load_trends
from logic.keyword_expander import expand_keywords
from logic.intent_filter import filter_educational, is_educational
from logic.competition_analyzer import analyze_competition
from logic.category_mapper import map_category


def run_pipeline(trends_csv_path):
    """
    Main pipeline:
    1. Load trends
    2. Filter seeds by trend
    3. Expand to long-tails
    4. Filter educational intent
    5. Analyze competition
    6. Score and rank
    7. Export CSV
    """

    # 1️⃣ Load Trends
    trends = load_trends(trends_csv_path)

    # 2️⃣ Filter trending seeds
    seeds = trends[trends["trend_score"] >= MIN_TREND_SCORE]["keyword"].tolist()

    if not seeds:
        raise ValueError("No keywords passed trend filter.")

    # 3️⃣ Expand into long-tail keywords
    expanded = expand_keywords(seeds)

    # 4️⃣ Filter educational keywords
    filtered = filter_educational(expanded)

    if not filtered:
        raise ValueError("No educational keywords found after filtering.")

    records = []

    # 5️⃣ Analyze each keyword
    for kw in filtered:
        comp = analyze_competition(kw)
        category = map_category(kw)

        # Score calculation
        score = 0

        if is_educational(kw):
            score += WEIGHTS["educational_intent"]

        # Question pattern bonus
        if kw.startswith(("what", "why", "how", "explain")):
            score += WEIGHTS["question_pattern"]

        # Competition score (0–4) mapped to weight
        score += comp["score"] * WEIGHTS["low_competition"] / 4

        # Title weakness proxy
        if comp.get("strong_sites", 0) == 0:
            score += WEIGHTS["weak_title_match"]

        # Short snippet proxy (weak content)
        if comp.get("forum_ratio", 0) > 0.5:
            score += WEIGHTS["short_snippet"]

        # Demand already filtered, give small bonus
        score += WEIGHTS["trend"]

        records.append({
            "keyword": kw,
            "category": category,
            "competition_score": comp["score"],
            "forum_ratio": comp.get("forum_ratio"),
            "strong_sites": comp.get("strong_sites"),
            "final_score": round(score, 2)
        })

    df = pd.DataFrame(records)

    # 6️⃣ Filter only high-opportunity keywords
    df = df[df["final_score"] >= MIN_FINAL_SCORE]

    # 7️⃣ Sort and export
    df = df.sort_values(by="final_score", ascending=False)

    output_path = "outputs/keyword_opportunities.csv"
    df.to_csv(output_path, index=False)

    return output_path
