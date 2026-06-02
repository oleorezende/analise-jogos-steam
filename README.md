# Analise de Jogos da Steam

Projeto de analise de dados sobre jogos da Steam, usando Python, SQL e Power BI.

## Objetivo

Investigar como genero, preco, avaliacoes, desenvolvedoras e ano de lancamento se relacionam no catalogo da Steam.

A ideia e construir um projeto de portfolio completo, com etapas claras de extracao manual da base, tratamento de dados, modelagem SQL, exportacao de tabelas analiticas e dashboard final em Power BI.

Tambem existe um dashboard complementar em Streamlit, criado para aprendizado e exploracao rapida dos dados com Python. O foco principal do projeto continua sendo Power BI.

## Perguntas de negocio

- Quais generos possuem as melhores avaliacoes?
- Existe relacao entre preco e nota dos jogos?
- Como os lancamentos evoluiram ao longo dos anos?
- Quais desenvolvedoras aparecem com maior frequencia ou melhor desempenho?
- Jogos gratuitos possuem avaliacoes diferentes dos jogos pagos?

## Fonte de dados

A base usada no projeto e a Steam Games Dataset, criada por FronkonGames.

Links:

- Kaggle: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
- Hugging Face: https://huggingface.co/datasets/FronkonGames/steam-games-dataset

O arquivo bruto deve ser baixado manualmente e salvo em:

```text
data/raw/steam_games.csv
```

O arquivo bruto nao deve ser commitado no GitHub. Ele e ignorado pelo `.gitignore` porque pode ser pesado e pertence a fonte original.

## Ferramentas

- Python para limpeza, padronizacao e exportacao dos dados.
- SQL/SQLite para modelagem e consultas analiticas.
- Streamlit para dashboard complementar de aprendizado.
- Power BI para visualizacao e storytelling dos resultados finais.

## Estrutura

```text
.
|-- data/
|   |-- raw/           # base bruta local, nao versionada
|   |-- sample/        # amostra pequena para testes
|   `-- processed/     # dados tratados e tabelas para Power BI
|-- docs/              # documentacao do projeto
|-- notebooks/         # analises exploratorias opcionais
|-- powerbi/           # arquivo .pbix e anotacoes do dashboard
|-- reports/figures/   # graficos gerados em Python
|-- sql/               # schema e consultas SQL
|-- src/               # pipeline Python
|-- streamlit_app/     # dashboard complementar em Streamlit
|-- tests/             # testes unitarios
|-- README.md
`-- requirements.txt
```

## Como executar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependencias principais:

```bash
pip install -r requirements.txt
```

Com o CSV bruto salvo em `data/raw/steam_games.csv`, execute o pipeline completo:

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

## Dashboard Streamlit

Para abrir o dashboard complementar em Streamlit:

```bash
streamlit run streamlit_app/app.py
```

Esse app usa os arquivos tratados em `data/processed/` e serve para exploracao interativa durante o aprendizado.

## Saidas geradas

Arquivos principais:

- `data/processed/steam_games_clean.csv`
- `data/processed/steam_game_genres.csv`
- `data/processed/steam_games.sqlite`

Tabelas prontas para Power BI:

- `data/processed/powerbi_genre_ratings.csv`
- `data/processed/powerbi_price_ranges.csv`
- `data/processed/powerbi_releases_by_year.csv`
- `data/processed/powerbi_top_developers.csv`
- `data/processed/powerbi_developer_ratings.csv`

Graficos gerados em Python:

- `reports/figures/genre_ratings.png`
- `reports/figures/price_ranges.png`
- `reports/figures/releases_by_year.png`

## Validacao atual

Na execucao com a base FronkonGames, o pipeline gerou:

- 122.610 jogos tratados;
- 329.318 linhas na tabela jogo-genero;
- anos de lancamento entre 1997 e 2026;
- tabelas agregadas para generos, faixas de preco, lancamentos por ano e desenvolvedoras.

## Documentacao

- `docs/download_data.md`: como baixar e posicionar a base.
- `docs/project_workflow.md`: fluxo completo do projeto.
- `docs/data_dictionary.md`: dicionario das tabelas tratadas.
- `docs/powerbi_dashboard_plan.md`: roteiro pratico do dashboard.
- `docs/data_sources.md`: fontes candidatas e justificativa.
- `streamlit_app/README.md`: como rodar o dashboard complementar.

## Status

Concluido:

- estrutura inicial do projeto;
- pipeline Python de limpeza;
- correcao de leitura do CSV da FronkonGames;
- exportacao de CSVs tratados;
- banco SQLite;
- consultas SQL;
- tabelas agregadas para Power BI;
- dashboard complementar em Streamlit;
- documentacao tecnica inicial.

Pendente:

- construir o dashboard no Power BI;
- salvar o arquivo `.pbix` em `powerbi/`;
- documentar os principais insights apos a criacao do dashboard.
