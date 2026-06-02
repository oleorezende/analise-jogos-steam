# Como Baixar a Base de Dados

## Fonte recomendada

A base recomendada para este projeto e a Steam Games Dataset, criada por FronkonGames.

Links:

- Kaggle: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
- Hugging Face: https://huggingface.co/datasets/FronkonGames/steam-games-dataset

A base foi escolhida porque contem os campos necessarios para o projeto:

- `AppID`;
- `Name`;
- `Release date`;
- `Price`;
- `Positive`;
- `Negative`;
- `Developers`;
- `Genres`.

## Passo a passo

1. Baixe a base pelo Kaggle ou Hugging Face.
2. Localize o arquivo CSV principal da base.
3. Renomeie o arquivo para:

```text
steam_games.csv
```

4. Coloque o arquivo em:

```text
data/raw/steam_games.csv
```

5. Execute o pipeline:

```bash
python -m src.run_pipeline
```

## Resultado esperado

Depois da execucao, os arquivos tratados serao criados em:

```text
data/processed/
```

Arquivos principais:

- `steam_games_clean.csv`;
- `steam_game_genres.csv`;
- `powerbi_genre_ratings.csv`;
- `powerbi_price_ranges.csv`;
- `powerbi_releases_by_year.csv`;
- `powerbi_top_developers.csv`;
- `powerbi_developer_ratings.csv`.

## Observacao sobre o cabecalho da base

Na versao usada durante o projeto, o cabecalho do CSV possui uma coluna chamada:

```text
DiscountDLC count
```

Na pratica, essa informacao precisa ser lida como duas colunas:

```text
Discount
DLC count
```

O arquivo `src/prepare_data.py` ja corrige isso automaticamente. Essa correcao e importante porque, sem ela, as colunas ficam deslocadas e os dados tratados ficam errados.

## O que subir no GitHub

Pode subir:

```text
data/processed/steam_games_clean.csv
data/processed/steam_game_genres.csv
data/processed/powerbi_*.csv
```

Nao subir:

```text
data/raw/steam_games.csv
```

Motivo: o arquivo bruto e grande, pertence a fonte original e pode ser baixado novamente pelos links acima.

## Teste rapido com a amostra

Antes de baixar a base completa, voce pode copiar o arquivo de amostra para a pasta `raw`:

```bash
copy data\sample\steam_games_sample.csv data\raw\steam_games.csv
```

Depois execute:

```bash
python -m src.run_pipeline
```
