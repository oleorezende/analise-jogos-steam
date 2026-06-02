import ast
import re
from typing import Iterable

import pandas as pd


COLUMN_ALIASES = {
    "appid": "app_id",
    "app_id": "app_id",
    "name": "name",
    "title": "name",
    "game": "name",
    "release_date": "release_date",
    "releasedate": "release_date",
    "developer": "developer",
    "developers": "developer",
    "price": "price_usd",
    "price_usd": "price_usd",
    "positive": "positive_reviews",
    "positive_reviews": "positive_reviews",
    "positive_ratings": "positive_reviews",
    "negative": "negative_reviews",
    "negative_reviews": "negative_reviews",
    "negative_ratings": "negative_reviews",
    "reviews": "total_reviews",
    "total_reviews": "total_reviews",
    "genres": "genres",
    "genre": "genres",
}

REQUIRED_COLUMNS = ["app_id", "name"]


def normalize_column_name(column: str) -> str:
    column = column.strip()
    column = re.sub(r"[^0-9a-zA-Z]+", "_", column)
    column = re.sub(r"_+", "_", column).strip("_").lower()
    return COLUMN_ALIASES.get(column, column)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [normalize_column_name(column) for column in df.columns]
    return df


def ensure_required_columns(df: pd.DataFrame, required_columns: Iterable[str] = REQUIRED_COLUMNS) -> None:
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")


def parse_list_like(value) -> list[str]:
    if value is None:
        return []

    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    if pd.isna(value):
        return []

    value = str(value).strip()
    if not value:
        return []

    if value.startswith("[") and value.endswith("]"):
        try:
            parsed_value = ast.literal_eval(value)
            if isinstance(parsed_value, list):
                return [str(item).strip() for item in parsed_value if str(item).strip()]
        except (ValueError, SyntaxError):
            pass

    return [item.strip() for item in re.split(r"[,;|]", value) if item.strip()]


def clean_developer(value) -> str:
    developers = parse_list_like(value)
    if developers:
        return developers[0]
    return "Unknown"


def clean_price(value) -> float | None:
    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip().lower()
    if value in {"free", "free to play", "gratuito", ""}:
        return 0.0

    value = re.sub(r"[^0-9.,]", "", value)
    if not value:
        return None

    value = value.replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return None


def calculate_review_percentage(df: pd.DataFrame) -> pd.Series:
    if "positive_review_percentage" in df.columns:
        return pd.to_numeric(df["positive_review_percentage"], errors="coerce")

    if {"positive_reviews", "negative_reviews"}.issubset(df.columns):
        positive = pd.to_numeric(df["positive_reviews"], errors="coerce").fillna(0)
        negative = pd.to_numeric(df["negative_reviews"], errors="coerce").fillna(0)
        total = positive + negative
        return (positive / total * 100).where(total > 0)

    return pd.Series([None] * len(df), index=df.index, dtype="float64")


def clean_games(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    ensure_required_columns(df)

    df = df.drop_duplicates(subset=["app_id"]).copy()
    df["app_id"] = pd.to_numeric(df["app_id"], errors="coerce").astype("Int64")
    df["name"] = df["name"].astype(str).str.strip()

    if "developer" in df.columns:
        df["developer"] = df["developer"].apply(clean_developer)
    else:
        df["developer"] = "Unknown"

    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
        df["release_year"] = df["release_date"].dt.year.astype("Int64")
    else:
        df["release_date"] = pd.NaT
        df["release_year"] = pd.Series([None] * len(df), dtype="Int64")

    if "price_usd" in df.columns:
        df["price_usd"] = df["price_usd"].apply(clean_price)
    else:
        df["price_usd"] = None

    for column in ["positive_reviews", "negative_reviews", "total_reviews"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
        else:
            df[column] = pd.Series([None] * len(df), dtype="Int64")

    if df["total_reviews"].isna().all() and {"positive_reviews", "negative_reviews"}.issubset(df.columns):
        df["total_reviews"] = df["positive_reviews"].fillna(0) + df["negative_reviews"].fillna(0)

    df["positive_review_percentage"] = calculate_review_percentage(df).round(2)

    selected_columns = [
        "app_id",
        "name",
        "release_date",
        "release_year",
        "developer",
        "price_usd",
        "positive_reviews",
        "negative_reviews",
        "total_reviews",
        "positive_review_percentage",
        "genres",
    ]

    for column in selected_columns:
        if column not in df.columns:
            df[column] = None

    return df[selected_columns].dropna(subset=["app_id", "name"])


def split_genres(df: pd.DataFrame) -> pd.DataFrame:
    genre_rows = []

    for row in df[["app_id", "genres"]].itertuples(index=False):
        for genre in parse_list_like(row.genres):
            genre_rows.append({"app_id": int(row.app_id), "genre": genre})

    if not genre_rows:
        return pd.DataFrame(columns=["app_id", "genre"])

    return pd.DataFrame(genre_rows).drop_duplicates()
