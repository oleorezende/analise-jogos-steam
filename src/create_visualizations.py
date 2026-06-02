import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from src.config import (
    FIGURES_DIR,
    PROCESSED_STEAM_GAMES_FILE,
    PROCESSED_STEAM_GENRES_FILE,
)


sns.set_theme(style="whitegrid")


def save_genre_ratings_chart(games_df: pd.DataFrame, genres_df: pd.DataFrame) -> None:
    genre_ratings = (
        games_df.merge(genres_df, on="app_id", how="inner")
        .query("total_reviews >= 50")
        .groupby("genre", as_index=False)
        .agg(
            total_games=("app_id", "count"),
            avg_positive_review_percentage=("positive_review_percentage", "mean"),
        )
        .query("total_games >= 2")
        .sort_values("avg_positive_review_percentage", ascending=False)
        .head(10)
    )

    if genre_ratings.empty:
        return

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=genre_ratings,
        x="avg_positive_review_percentage",
        y="genre",
        color="#2f80ed",
    )
    plt.title("Top generos por percentual medio de reviews positivas")
    plt.xlabel("Reviews positivas (%)")
    plt.ylabel("Genero")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "genre_ratings.png", dpi=160)
    plt.close()


def save_price_ranges_chart(games_df: pd.DataFrame) -> None:
    price_df = games_df.query("total_reviews >= 50").copy()
    if price_df.empty:
        return

    price_df["price_range"] = pd.cut(
        price_df["price_usd"].fillna(-1),
        bins=[-1, 0, 10, 30, 60, float("inf")],
        labels=["Free", "Under 10 USD", "10 to 29.99 USD", "30 to 59.99 USD", "60 USD or more"],
        include_lowest=True,
    )

    price_summary = (
        price_df.groupby("price_range", observed=True, as_index=False)
        .agg(avg_positive_review_percentage=("positive_review_percentage", "mean"))
        .dropna()
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=price_summary,
        x="price_range",
        y="avg_positive_review_percentage",
        color="#27ae60",
    )
    plt.title("Media de reviews positivas por faixa de preco")
    plt.xlabel("Faixa de preco")
    plt.ylabel("Reviews positivas (%)")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "price_ranges.png", dpi=160)
    plt.close()


def save_releases_by_year_chart(games_df: pd.DataFrame) -> None:
    releases = (
        games_df.dropna(subset=["release_year"])
        .groupby("release_year", as_index=False)
        .agg(total_releases=("app_id", "count"))
        .sort_values("release_year")
    )

    if releases.empty:
        return

    plt.figure(figsize=(11, 6))
    sns.lineplot(data=releases, x="release_year", y="total_releases", marker="o", color="#eb5757")
    plt.title("Evolucao dos lancamentos por ano")
    plt.xlabel("Ano")
    plt.ylabel("Total de lancamentos")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "releases_by_year.png", dpi=160)
    plt.close()


def main() -> None:
    if not PROCESSED_STEAM_GAMES_FILE.exists() or not PROCESSED_STEAM_GENRES_FILE.exists():
        raise FileNotFoundError("Processed files not found. Run `python -m src.prepare_data` first.")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    games_df = pd.read_csv(PROCESSED_STEAM_GAMES_FILE)
    genres_df = pd.read_csv(PROCESSED_STEAM_GENRES_FILE)

    save_genre_ratings_chart(games_df, genres_df)
    save_price_ranges_chart(games_df)
    save_releases_by_year_chart(games_df)

    print(f"Saved figures to: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
