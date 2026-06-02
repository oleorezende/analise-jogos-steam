from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_STEAM_GAMES_FILE = RAW_DATA_DIR / "steam_games.csv"
PROCESSED_STEAM_GAMES_FILE = PROCESSED_DATA_DIR / "steam_games_clean.csv"
PROCESSED_STEAM_GENRES_FILE = PROCESSED_DATA_DIR / "steam_game_genres.csv"
DATABASE_FILE = PROCESSED_DATA_DIR / "steam_games.sqlite"
