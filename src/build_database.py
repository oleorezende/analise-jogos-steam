import sqlite3

import pandas as pd

from src.config import (
    DATABASE_FILE,
    PROCESSED_STEAM_GAMES_FILE,
    PROCESSED_STEAM_GENRES_FILE,
)


def main() -> None:
    if not PROCESSED_STEAM_GAMES_FILE.exists() or not PROCESSED_STEAM_GENRES_FILE.exists():
        raise FileNotFoundError(
            "Processed files not found. Run `python -m src.prepare_data` first."
        )

    games_df = pd.read_csv(PROCESSED_STEAM_GAMES_FILE)
    genres_df = pd.read_csv(PROCESSED_STEAM_GENRES_FILE)

    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_FILE) as connection:
        games_df.to_sql("games", connection, if_exists="replace", index=False)
        genres_df.to_sql("game_genres", connection, if_exists="replace", index=False)

        connection.execute("CREATE INDEX IF NOT EXISTS idx_games_release_year ON games(release_year)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_games_price ON games(price_usd)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_genres_genre ON game_genres(genre)")

    print(f"Saved SQLite database: {DATABASE_FILE}")


if __name__ == "__main__":
    main()
