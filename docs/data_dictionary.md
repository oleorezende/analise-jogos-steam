# Dicionario de Dados

Este dicionario descreve as colunas padronizadas geradas pelo pipeline.

## `games`

| Coluna | Tipo esperado | Descricao |
| --- | --- | --- |
| `app_id` | inteiro | Identificador unico do jogo na Steam. |
| `name` | texto | Nome do jogo. |
| `release_date` | data | Data de lancamento. |
| `release_year` | inteiro | Ano de lancamento extraido de `release_date`. |
| `developer` | texto | Desenvolvedora principal ou texto original da fonte. |
| `price_usd` | decimal | Preco em dolares. Jogos gratuitos devem ser 0. |
| `positive_reviews` | inteiro | Quantidade de avaliacoes positivas. |
| `negative_reviews` | inteiro | Quantidade de avaliacoes negativas. |
| `total_reviews` | inteiro | Soma ou total informado de avaliacoes. |
| `positive_review_percentage` | decimal | Percentual de avaliacoes positivas. |

## `game_genres`

| Coluna | Tipo esperado | Descricao |
| --- | --- | --- |
| `app_id` | inteiro | Identificador do jogo. |
| `genre` | texto | Genero individual do jogo. |

## Regras de limpeza

- Datas invalidas viram valores nulos.
- Precos como `Free`, `Free to Play` ou `Gratuito` viram 0.
- Jogos sem `app_id` ou sem `name` sao removidos.
- Generos separados por virgula, ponto e virgula ou barra vertical sao quebrados em linhas separadas.
- Quando `total_reviews` nao existe, ele e calculado pela soma de reviews positivas e negativas.
