# Plano do Dashboard Power BI

Este documento descreve a proxima etapa do projeto: criar o dashboard em Power BI usando os dados tratados em `data/processed/`.

## 1. Arquivos para importar

Importe estes CSVs no Power BI:

```text
data/processed/steam_games_clean.csv
data/processed/steam_game_genres.csv
data/processed/powerbi_genre_ratings.csv
data/processed/powerbi_price_ranges.csv
data/processed/powerbi_releases_by_year.csv
data/processed/powerbi_top_developers.csv
data/processed/powerbi_developer_ratings.csv
```

O arquivo bruto `data/raw/steam_games.csv` nao precisa ser importado no Power BI.

## 2. Modelo de dados

Tabelas principais:

- `steam_games_clean`: uma linha por jogo.
- `steam_game_genres`: uma linha por combinacao jogo-genero.

Relacao recomendada:

```text
steam_games_clean[app_id] 1 -> * steam_game_genres[app_id]
```

Direcao de filtro: unica, de `steam_games_clean` para `steam_game_genres`.

As tabelas `powerbi_*.csv` ja sao agregadas e podem ser usadas para visuais prontos, sem necessidade de relacao obrigatoria.

## 3. Medidas sugeridas

Crie estas medidas em DAX, se estiver usando as tabelas principais:

```DAX
Total Jogos = COUNTROWS(steam_games_clean)
```

```DAX
Total Reviews = SUM(steam_games_clean[total_reviews])
```

```DAX
Media Reviews Positivas = AVERAGE(steam_games_clean[positive_review_percentage])
```

```DAX
Preco Medio = AVERAGE(steam_games_clean[price_usd])
```

```DAX
Jogos Gratuitos =
COUNTROWS(
    FILTER(steam_games_clean, steam_games_clean[price_usd] = 0)
)
```

```DAX
Jogos Pagos =
COUNTROWS(
    FILTER(steam_games_clean, steam_games_clean[price_usd] > 0)
)
```

## 4. Pagina 1: Visao Geral

Objetivo: apresentar o tamanho e o perfil geral da base.

Cards sugeridos:

- Total Jogos;
- Total Reviews;
- Media Reviews Positivas;
- Preco Medio;
- Jogos Gratuitos;
- Jogos Pagos.

Graficos sugeridos:

- linha: `release_year` x quantidade de jogos;
- barras: top generos por quantidade;
- barras ou rosca: jogos gratuitos versus pagos;
- histograma ou colunas: distribuicao de preco.

## 5. Pagina 2: Avaliacoes por Genero

Objetivo: identificar generos com melhores avaliacoes.

Fonte recomendada:

```text
powerbi_genre_ratings.csv
```

Graficos sugeridos:

- barras horizontais: `genre` por `avg_positive_review_percentage`;
- barras: `genre` por `total_games`;
- dispersao: `total_games` x `avg_positive_review_percentage`.

Filtro recomendado:

- usar generos com quantidade minima de jogos para evitar distorcoes.

## 6. Pagina 3: Preco versus Avaliacao

Objetivo: analisar se jogos mais caros tendem a ter melhores avaliacoes.

Fonte recomendada:

```text
powerbi_price_ranges.csv
```

Graficos sugeridos:

- colunas: `price_range` por `avg_positive_review_percentage`;
- colunas: `price_range` por `total_games`;
- dispersao usando `steam_games_clean`: `price_usd` x `positive_review_percentage`.

Observacao:

- para dispersao, filtre jogos com `total_reviews >= 50`, pois jogos com poucas reviews podem distorcer a leitura.

## 7. Pagina 4: Evolucao dos Lancamentos

Objetivo: mostrar como o catalogo evoluiu ao longo do tempo.

Fonte recomendada:

```text
powerbi_releases_by_year.csv
```

Graficos sugeridos:

- linha: `release_year` x `total_releases`;
- linha secundaria: `release_year` x `avg_price_usd`;
- linha ou colunas: `release_year` x `avg_positive_review_percentage`.

## 8. Pagina 5: Desenvolvedoras

Objetivo: destacar desenvolvedoras com mais jogos ou melhores medias.

Fontes recomendadas:

```text
powerbi_top_developers.csv
powerbi_developer_ratings.csv
```

Graficos sugeridos:

- barras: top desenvolvedoras por `total_games`;
- barras: top desenvolvedoras por `avg_positive_review_percentage`;
- tabela: `developer`, `total_games`, `avg_price_usd`, `avg_positive_review_percentage`, `total_reviews`.

Filtro recomendado:

- manter quantidade minima de jogos ou reviews para evitar que estudios com poucos jogos liderem o ranking injustamente.

## 9. Arquivo final

Salve o dashboard em:

```text
powerbi/analise_jogos_steam.pbix
```

Esse arquivo sera o principal entregavel visual do projeto.

## 10. Proximos insights para documentar

Depois de construir o dashboard, documente no README:

- genero com melhor avaliacao media;
- faixa de preco com melhor avaliacao media;
- ano com maior volume de lancamentos;
- desenvolvedoras com maior volume de jogos;
- principais conclusoes e limitacoes da analise.
