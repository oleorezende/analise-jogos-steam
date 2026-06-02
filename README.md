# Analise de Jogos da Steam

Projeto de analise de dados sobre jogos da Steam, usando Python, SQL e Power BI.

## Objetivo

Investigar como genero, preco, avaliacoes, desenvolvedoras e ano de lancamento se relacionam no catalogo da Steam.

A ideia e construir um projeto de portfolio completo, com etapas claras de tratamento de dados, analise exploratoria, consultas SQL e dashboard final em Power BI.

## Perguntas de negocio

- Quais generos possuem as melhores avaliacoes?
- Existe relacao entre preco e nota dos jogos?
- Como os lancamentos evoluiram ao longo dos anos?
- Quais desenvolvedoras aparecem com maior frequencia ou melhor desempenho?
- Jogos gratuitos possuem avaliacoes diferentes dos jogos pagos?

## Ferramentas

- Python para limpeza, tratamento e analise exploratoria.
- SQL para modelagem e consultas analiticas.
- Power BI para visualizacao e storytelling dos resultados.

## Estrutura

```text
.
|-- data/
|   |-- raw/
|   |-- sample/
|   `-- processed/
|-- docs/
|-- notebooks/
|-- powerbi/
|-- reports/
|   `-- figures/
|-- sql/
|-- src/
|-- tests/
|-- README.md
`-- requirements.txt
```

## Fonte de dados

A fonte principal ainda sera definida. As candidatas estao documentadas em `docs/data_sources.md`.

Para executar o pipeline atual, coloque o arquivo CSV da base escolhida em:

```text
data/raw/steam_games.csv
```

Tambem existe uma amostra pequena em:

```text
data/sample/steam_games_sample.csv
```

Essa amostra serve apenas para testar o pipeline antes de baixar a base completa.

Colunas esperadas pelo pipeline:

- `appid`, `appID` ou `app_id`;
- `name`, `title` ou `game`;
- `release_date`;
- `developer` ou `developers`;
- `price`;
- `positive` e `negative`, quando disponiveis;
- `genres` ou `genre`.

## Como executar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute o pipeline completo:

```bash
python -m src.run_pipeline
```

Ou execute cada etapa separadamente:

```bash
python -m src.prepare_data
python -m src.build_database
python -m src.export_powerbi_tables
python -m src.create_visualizations
```

Execute os testes:

```bash
pytest
```

## Saidas geradas

- `data/processed/steam_games_clean.csv`
- `data/processed/steam_game_genres.csv`
- `data/processed/steam_games.sqlite`
- `data/processed/powerbi_genre_ratings.csv`
- `data/processed/powerbi_price_ranges.csv`
- `data/processed/powerbi_releases_by_year.csv`
- `reports/figures/genre_ratings.png`
- `reports/figures/price_ranges.png`
- `reports/figures/releases_by_year.png`

## Status

Projeto iniciado com estrutura, documentacao, pipeline em Python, modelo SQL, consultas analiticas, testes e geracao de graficos.

Proxima etapa: escolher a fonte definitiva, baixar a base e validar o pipeline com dados reais.
