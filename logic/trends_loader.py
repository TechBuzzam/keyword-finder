import pandas as pd


def load_trends(csv_path):
    """
    Loads Google Trends CSV and returns a DataFrame with:
    - keyword
    - trend_score (0-100)
    """

    df = pd.read_csv(csv_path)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Try to detect keyword column
    keyword_col = None
    for c in df.columns:
        if "query" in c or "keyword" in c or "topic" in c:
            keyword_col = c
            break

    if not keyword_col:
        raise ValueError("Could not detect keyword column in Trends CSV.")

    # Try to detect trend score column
    trend_col = None
    for c in df.columns:
        if "value" in c or "score" in c or "interest" in c:
            trend_col = c
            break

    if not trend_col:
        # Fallback: use first numeric column
        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) == 0:
            raise ValueError("Could not detect trend score column.")
        trend_col = numeric_cols[0]

    clean = df[[keyword_col, trend_col]].copy()
    clean.columns = ["keyword", "trend_score"]

    # Clean values
    clean["keyword"] = clean["keyword"].astype(str).str.strip().str.lower()
    clean["trend_score"] = pd.to_numeric(clean["trend_score"], errors="coerce").fillna(0)

    # Remove empty keywords
    clean = clean[clean["keyword"] != ""]

    return clean
