import sqlite3

import pandas as pd

from src.config import DATABASE_FILE, PROCESSED_DATA_DIR


POWERBI_EXPORTS = {
    "powerbi_genre_ratings.csv": """
        SELECT
            gg.genre,
            COUNT(*) AS total_games,
            ROUND(AVG(g.positive_review_percentage), 2) AS avg_positive_review_percentage,
            ROUND(AVG(g.total_reviews), 2) AS avg_total_reviews
        FROM games AS g
        JOIN game_genres AS gg
            ON g.app_id = gg.app_id
        WHERE g.total_reviews >= 50
        GROUP BY gg.genre
        HAVING COUNT(*) >= 10
        ORDER BY avg_positive_review_percentage DESC
    """,
    "powerbi_price_ranges.csv": """
        SELECT
            CASE
                WHEN price_usd = 0 THEN 'Free'
                WHEN price_usd < 10 THEN 'Under 10 USD'
                WHEN price_usd < 30 THEN '10 to 29.99 USD'
                WHEN price_usd < 60 THEN '30 to 59.99 USD'
                ELSE '60 USD or more'
            END AS price_range,
            COUNT(*) AS total_games,
            ROUND(AVG(positive_review_percentage), 2) AS avg_positive_review_percentage
        FROM games
        WHERE total_reviews >= 50
          AND price_usd IS NOT NULL
        GROUP BY price_range
        ORDER BY avg_positive_review_percentage DESC
    """,
    "powerbi_releases_by_year.csv": """
        SELECT
            release_year,
            COUNT(*) AS total_releases,
            ROUND(AVG(price_usd), 2) AS avg_price_usd,
            ROUND(AVG(positive_review_percentage), 2) AS avg_positive_review_percentage
        FROM games
        WHERE release_year IS NOT NULL
        GROUP BY release_year
        ORDER BY release_year
    """,
    "powerbi_top_developers.csv": """
        SELECT
            developer,
            COUNT(*) AS total_games,
            ROUND(AVG(price_usd), 2) AS avg_price_usd,
            ROUND(AVG(positive_review_percentage), 2) AS avg_positive_review_percentage,
            SUM(total_reviews) AS total_reviews
        FROM games
        WHERE developer IS NOT NULL
          AND developer <> 'Unknown'
        GROUP BY developer
        HAVING COUNT(*) >= 3
        ORDER BY total_games DESC, avg_positive_review_percentage DESC
    """,
    "powerbi_developer_ratings.csv": """
        SELECT
            developer,
            COUNT(*) AS total_games,
            ROUND(AVG(positive_review_percentage), 2) AS avg_positive_review_percentage,
            SUM(total_reviews) AS total_reviews
        FROM games
        WHERE developer IS NOT NULL
          AND developer <> 'Unknown'
          AND total_reviews >= 50
        GROUP BY developer
        HAVING COUNT(*) >= 3
        ORDER BY avg_positive_review_percentage DESC, total_reviews DESC
    """,
}


def main() -> None:
    if not DATABASE_FILE.exists():
        raise FileNotFoundError("SQLite database not found. Run `python -m src.build_database` first.")

    with sqlite3.connect(DATABASE_FILE) as connection:
        for filename, query in POWERBI_EXPORTS.items():
            output_path = PROCESSED_DATA_DIR / filename
            df = pd.read_sql_query(query, connection)
            df.to_csv(output_path, index=False)
            print(f"Saved Power BI table: {output_path}")


if __name__ == "__main__":
    main()
