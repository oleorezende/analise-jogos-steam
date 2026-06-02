import pandas as pd

from src.clean_data import clean_games, clean_price, parse_list_like, split_genres


def test_clean_price_handles_free_and_currency_text():
    assert clean_price("Free To Play") == 0.0
    assert clean_price("$19.99") == 19.99
    assert clean_price("R$ 10,50") == 10.50


def test_parse_list_like_handles_python_list_strings():
    assert parse_list_like("['Action', 'Indie']") == ["Action", "Indie"]
    assert parse_list_like("Action; Adventure") == ["Action", "Adventure"]


def test_clean_games_calculates_review_percentage_and_total_reviews():
    raw_df = pd.DataFrame(
        {
            "appID": [1],
            "name": ["Example Game"],
            "release_date": ["Jan 1, 2020"],
            "developers": ["['Example Studio']"],
            "price": ["Free"],
            "positive": [90],
            "negative": [10],
            "genres": ["['Action', 'Indie']"],
        }
    )

    cleaned_df = clean_games(raw_df)

    assert cleaned_df.loc[0, "app_id"] == 1
    assert cleaned_df.loc[0, "developer"] == "Example Studio"
    assert cleaned_df.loc[0, "price_usd"] == 0.0
    assert cleaned_df.loc[0, "total_reviews"] == 100
    assert cleaned_df.loc[0, "positive_review_percentage"] == 90.0


def test_split_genres_creates_one_row_per_genre():
    raw_df = pd.DataFrame(
        {
            "appID": [1],
            "name": ["Example Game"],
            "genres": ["['Action', 'Indie']"],
        }
    )

    genres_df = split_genres(clean_games(raw_df))

    assert genres_df.to_dict("records") == [
        {"app_id": 1, "genre": "Action"},
        {"app_id": 1, "genre": "Indie"},
    ]
