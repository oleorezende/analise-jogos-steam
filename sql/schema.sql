-- Esquema inicial para a base analitica de jogos da Steam.
-- Ajustar nomes e tipos conforme a fonte de dados escolhida.

CREATE TABLE IF NOT EXISTS games (
    app_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    release_date DATE,
    release_year INTEGER,
    developer TEXT,
    price_usd REAL,
    positive_reviews INTEGER,
    negative_reviews INTEGER,
    total_reviews INTEGER,
    positive_review_percentage REAL
);

CREATE TABLE IF NOT EXISTS game_genres (
    app_id INTEGER NOT NULL,
    genre TEXT NOT NULL,
    PRIMARY KEY (app_id, genre),
    FOREIGN KEY (app_id) REFERENCES games(app_id)
);
