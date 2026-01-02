import pandas as pd
from logic.trends import load_trends
from logic.expansion import expand_keywords
from logic.competition import get_domains, competition_level
from logic.questions import is_question
from config import MIN_TREND_SCORE

def run_pipeline(trends_path):
    trends = load_trends(trends_path)

    seeds = trends.iloc[:,0].dropna().tolist()
    longtails = expand_keywords(seeds)

    df = pd.DataFrame(longtails, columns=["keyword"])
    df["competition"] = ""
    df["question"] = ""
    df["safe_score"] = 0

    for i, row in df.iterrows():
        domains = get_domains(row["keyword"])
        comp = competition_level(domains)
        q = is_question(row["keyword"])

        df.at[i, "competition"] = comp
        df.at[i, "question"] = "YES" if q else "NO"

        score = 0
        if comp in ["VERY LOW", "LOW"]:
            score += 2
        if q:
            score += 1

        df.at[i, "safe_score"] = score

    output_path = "outputs/results.csv"
    df.sort_values("safe_score", ascending=False).to_csv(output_path, index=False)
    return output_path
