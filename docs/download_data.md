# Como Baixar a Base de Dados

## Opcao recomendada: FronkonGames Steam Games Dataset

A base recomendada para iniciar o projeto e a Steam Games Dataset, criada por FronkonGames.

Links:

- Kaggle: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
- Hugging Face: https://huggingface.co/datasets/FronkonGames/steam-games-dataset

Essa base e uma boa candidata porque possui campos como:

- `appID`;
- `name`;
- `release_date`;
- `price`;
- `positive`;
- `negative`;
- `developers`;
- `genres`.

## Passo a passo

1. Baixe a base pelo Kaggle ou Hugging Face.
2. Localize o arquivo tabular principal em formato CSV.
3. Renomeie o arquivo para `steam_games.csv`.
4. Coloque o arquivo em:

```text
data/raw/steam_games.csv
```

5. Execute:

```bash
python -m src.run_pipeline
```

## Teste rapido com a amostra

Antes de baixar a base completa, voce pode copiar o arquivo de amostra para a pasta `raw`:

```bash
copy data\sample\steam_games_sample.csv data\raw\steam_games.csv
```

Depois execute:

```bash
python -m src.run_pipeline
```

## Observacoes

- O arquivo completo da base nao deve ser commitado se for muito grande.
- Os CSVs tratados e o banco SQLite gerados em `data/processed/` podem ser recriados pelo pipeline.
- Se a fonte escolhida tiver nomes de colunas diferentes, ajuste os aliases em `src/clean_data.py`.
