from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

GAMES_FILE = PROCESSED_DIR / "steam_games_clean.csv"
GENRES_FILE = PROCESSED_DIR / "steam_game_genres.csv"


st.set_page_config(
    page_title="Analise de Jogos da Steam",
    page_icon="🎮",
    layout="wide",
)


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    games = pd.read_csv(GAMES_FILE, parse_dates=["release_date"])
    genres = pd.read_csv(GENRES_FILE)

    games["release_year"] = pd.to_numeric(games["release_year"], errors="coerce")
    games["price_usd"] = pd.to_numeric(games["price_usd"], errors="coerce")
    games["total_reviews"] = pd.to_numeric(games["total_reviews"], errors="coerce")
    games["positive_review_percentage"] = pd.to_numeric(
        games["positive_review_percentage"],
        errors="coerce",
    )

    return games, genres


def format_number(value: float) -> str:
    return f"{value:,.0f}".replace(",", ".")


def format_percent(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:.1f}%"


def format_currency(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"US$ {value:,.2f}"


def apply_filters(games: pd.DataFrame, genres: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros")

    min_year = int(games["release_year"].min())
    max_year = int(games["release_year"].max())
    selected_years = st.sidebar.slider(
        "Ano de lancamento",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )

    all_genres = sorted(genres["genre"].dropna().unique())
    selected_genres = st.sidebar.multiselect(
        "Generos",
        options=all_genres,
        default=[],
    )

    price_options = ["Todos", "Gratis", "Pagos"]
    price_filter = st.sidebar.radio("Tipo de preco", price_options, horizontal=True)

    min_reviews = st.sidebar.number_input(
        "Minimo de reviews",
        min_value=0,
        max_value=int(games["total_reviews"].max()),
        value=50,
        step=50,
    )

    filtered = games[
        games["release_year"].between(selected_years[0], selected_years[1])
        & (games["total_reviews"] >= min_reviews)
    ].copy()

    if selected_genres:
        selected_app_ids = genres.loc[
            genres["genre"].isin(selected_genres),
            "app_id",
        ].unique()
        filtered = filtered[filtered["app_id"].isin(selected_app_ids)]

    if price_filter == "Gratis":
        filtered = filtered[filtered["price_usd"] == 0]
    elif price_filter == "Pagos":
        filtered = filtered[filtered["price_usd"] > 0]

    return filtered


def show_overview(games: pd.DataFrame, genres: pd.DataFrame) -> None:
    total_games = len(games)
    total_reviews = games["total_reviews"].sum()
    avg_rating = games["positive_review_percentage"].mean()
    avg_price = games["price_usd"].mean()
    free_games = (games["price_usd"] == 0).sum()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Jogos", format_number(total_games))
    col2.metric("Reviews", format_number(total_reviews))
    col3.metric("Review positiva media", format_percent(avg_rating))
    col4.metric("Preco medio", format_currency(avg_price))
    col5.metric("Jogos gratis", format_number(free_games))

    st.divider()

    left, right = st.columns([1.4, 1])

    releases_by_year = (
        games.dropna(subset=["release_year"])
        .groupby("release_year", as_index=False)
        .agg(total_games=("app_id", "count"))
        .sort_values("release_year")
    )
    left.subheader("Evolucao dos lancamentos")
    left.line_chart(
        releases_by_year,
        x="release_year",
        y="total_games",
        height=330,
    )

    top_genres = (
        genres[genres["app_id"].isin(games["app_id"])]
        .groupby("genre", as_index=False)
        .agg(total_games=("app_id", "count"))
        .sort_values("total_games", ascending=False)
        .head(12)
    )
    right.subheader("Generos mais frequentes")
    right.bar_chart(
        top_genres,
        x="genre",
        y="total_games",
        height=330,
    )


def show_genres(games: pd.DataFrame, genres: pd.DataFrame) -> None:
    genre_ratings = (
        games.merge(genres, on="app_id", how="inner")
        .groupby("genre", as_index=False)
        .agg(
            total_games=("app_id", "count"),
            avg_rating=("positive_review_percentage", "mean"),
            avg_reviews=("total_reviews", "mean"),
        )
        .query("total_games >= 10")
        .sort_values("avg_rating", ascending=False)
        .head(20)
    )

    st.subheader("Generos com melhores avaliacoes")
    st.bar_chart(genre_ratings, x="genre", y="avg_rating", height=380)
    st.dataframe(
        genre_ratings.rename(
            columns={
                "genre": "Genero",
                "total_games": "Total de jogos",
                "avg_rating": "Media de reviews positivas",
                "avg_reviews": "Media de reviews",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def show_price_analysis(games: pd.DataFrame) -> None:
    price_df = games.copy()
    price_df["price_range"] = pd.cut(
        price_df["price_usd"].fillna(-1),
        bins=[-1, 0, 10, 30, 60, float("inf")],
        labels=[
            "Gratis",
            "Ate US$ 10",
            "US$ 10 a 29,99",
            "US$ 30 a 59,99",
            "US$ 60+",
        ],
        include_lowest=True,
    )

    price_summary = (
        price_df.groupby("price_range", observed=True, as_index=False)
        .agg(
            total_games=("app_id", "count"),
            avg_rating=("positive_review_percentage", "mean"),
        )
        .dropna()
    )

    left, right = st.columns(2)
    left.subheader("Avaliacao media por faixa de preco")
    left.bar_chart(price_summary, x="price_range", y="avg_rating", height=340)

    right.subheader("Quantidade de jogos por faixa de preco")
    right.bar_chart(price_summary, x="price_range", y="total_games", height=340)

    st.subheader("Preco versus avaliacao")
    scatter_df = price_df[
        ["price_usd", "positive_review_percentage", "total_reviews", "name"]
    ].dropna()
    st.scatter_chart(
        scatter_df,
        x="price_usd",
        y="positive_review_percentage",
        size="total_reviews",
        height=420,
    )


def show_developers(games: pd.DataFrame) -> None:
    developer_summary = (
        games.query("developer != 'Unknown'")
        .groupby("developer", as_index=False)
        .agg(
            total_games=("app_id", "count"),
            avg_rating=("positive_review_percentage", "mean"),
            total_reviews=("total_reviews", "sum"),
            avg_price=("price_usd", "mean"),
        )
        .sort_values(["total_games", "avg_rating"], ascending=False)
    )

    left, right = st.columns(2)
    top_volume = developer_summary.head(15)
    left.subheader("Desenvolvedoras com mais jogos")
    left.bar_chart(top_volume, x="developer", y="total_games", height=360)

    top_rating = (
        developer_summary.query("total_games >= 3")
        .sort_values("avg_rating", ascending=False)
        .head(15)
    )
    right.subheader("Melhores medias de avaliacao")
    right.bar_chart(top_rating, x="developer", y="avg_rating", height=360)

    st.subheader("Tabela de desenvolvedoras")
    st.dataframe(
        developer_summary.head(200).rename(
            columns={
                "developer": "Desenvolvedora",
                "total_games": "Total de jogos",
                "avg_rating": "Review positiva media",
                "total_reviews": "Total de reviews",
                "avg_price": "Preco medio",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def show_games_table(games: pd.DataFrame) -> None:
    st.subheader("Jogos filtrados")
    table = games[
        [
            "name",
            "release_year",
            "developer",
            "price_usd",
            "total_reviews",
            "positive_review_percentage",
        ]
    ].sort_values("total_reviews", ascending=False)
    st.dataframe(
        table.rename(
            columns={
                "name": "Jogo",
                "release_year": "Ano",
                "developer": "Desenvolvedora",
                "price_usd": "Preco USD",
                "total_reviews": "Total de reviews",
                "positive_review_percentage": "Reviews positivas (%)",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    st.title("Analise de Jogos da Steam")
    st.caption("Dashboard interativo em Streamlit criado como complemento de aprendizado. O dashboard principal planejado continua sendo em Power BI.")

    if not GAMES_FILE.exists() or not GENRES_FILE.exists():
        st.error(
            "Arquivos tratados nao encontrados. Execute `python -m src.run_pipeline` antes de abrir o app."
        )
        st.stop()

    games, genres = load_data()
    filtered_games = apply_filters(games, genres)

    if filtered_games.empty:
        st.warning("Nenhum jogo encontrado com os filtros atuais.")
        st.stop()

    tabs = st.tabs(
        [
            "Visao geral",
            "Generos",
            "Preco x avaliacao",
            "Desenvolvedoras",
            "Tabela",
        ]
    )

    with tabs[0]:
        show_overview(filtered_games, genres)

    with tabs[1]:
        show_genres(filtered_games, genres)

    with tabs[2]:
        show_price_analysis(filtered_games)

    with tabs[3]:
        show_developers(filtered_games)

    with tabs[4]:
        show_games_table(filtered_games)


if __name__ == "__main__":
    main()
