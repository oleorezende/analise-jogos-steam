import pandas as pd

from src.clean_data import clean_games, split_genres
from src.config import (
    PROCESSED_STEAM_GAMES_FILE,
    PROCESSED_STEAM_GENRES_FILE,
    RAW_STEAM_GAMES_FILE,
)


def read_steam_games_csv(file_path):
    with open(file_path, encoding="utf-8") as file:
        header = file.readline().strip().split(",")

    fixed_columns = []
    for column in header:
        if column == "DiscountDLC count":
            fixed_columns.extend(["Discount", "DLC count"])
        else:
            fixed_columns.append(column)

    return pd.read_csv(file_path, header=0, names=fixed_columns)


def main() -> None:
    if not RAW_STEAM_GAMES_FILE.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {RAW_STEAM_GAMES_FILE}. "
            "Place the Steam dataset CSV at data/raw/steam_games.csv."
        )

    raw_df = read_steam_games_csv(RAW_STEAM_GAMES_FILE)
    games_df = clean_games(raw_df)
    genres_df = split_genres(games_df)

    PROCESSED_STEAM_GAMES_FILE.parent.mkdir(parents=True, exist_ok=True)
    games_df.drop(columns=["genres"]).to_csv(PROCESSED_STEAM_GAMES_FILE, index=False)
    genres_df.to_csv(PROCESSED_STEAM_GENRES_FILE, index=False)

    print(f"Saved games data: {PROCESSED_STEAM_GAMES_FILE}")
    print(f"Saved genres data: {PROCESSED_STEAM_GENRES_FILE}")


if __name__ == "__main__":
    main()
