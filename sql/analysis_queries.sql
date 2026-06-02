-- Consultas iniciais para as perguntas do projeto.
-- Ajustar filtros conforme a qualidade e cobertura da base escolhida.

-- 1. Generos com melhores avaliacoes.
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
ORDER BY avg_positive_review_percentage DESC;

-- 2. Relacao entre faixa de preco e avaliacao.
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
GROUP BY price_range
ORDER BY avg_positive_review_percentage DESC;

-- 3. Evolucao dos lancamentos por ano.
SELECT
    release_year,
    COUNT(*) AS total_releases,
    ROUND(AVG(price_usd), 2) AS avg_price_usd,
    ROUND(AVG(positive_review_percentage), 2) AS avg_positive_review_percentage
FROM games
WHERE release_year IS NOT NULL
GROUP BY release_year
ORDER BY release_year;
