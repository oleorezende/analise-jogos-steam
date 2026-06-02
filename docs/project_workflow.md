# Workflow do Projeto

Este documento explica o fluxo completo do projeto de analise de jogos da Steam.

## 1. Fonte de dados

A base principal usada e a Steam Games Dataset, criada por FronkonGames.

Links:

- Kaggle: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
- Hugging Face: https://huggingface.co/datasets/FronkonGames/steam-games-dataset

A base contem informacoes como:

- identificador do jogo na Steam;
- nome;
- data de lancamento;
- preco;
- avaliacoes positivas e negativas;
- desenvolvedoras;
- publicadoras;
- categorias;
- generos;
- tags.

## 2. Onde colocar a base bruta

Depois de baixar o CSV principal, renomeie o arquivo para:

```text
steam_games.csv
```

Coloque o arquivo em:

```text
data/raw/steam_games.csv
```

A pasta `data/raw/` e usada para dados brutos. Esses arquivos nao devem ser commitados no GitHub.

## 3. Por que o CSV bruto nao vai para o GitHub

O arquivo bruto fica fora do repositorio porque:

- pode ser pesado;
- pode mudar conforme a fonte atualiza;
- pertence a fonte original;
- pode ser baixado novamente pelos links documentados;
- manter o bruto fora do GitHub deixa o projeto mais limpo.

O `.gitignore` protege `data/raw/*` para evitar upload acidental do bruto.

## 4. Pipeline Python

O pipeline fica na pasta `src/`.

Arquivos principais:

- `src/prepare_data.py`: le a base bruta, corrige o cabecalho especifico da base FronkonGames e gera CSVs tratados.
- `src/clean_data.py`: padroniza nomes de colunas, trata precos, datas, reviews, desenvolvedoras e generos.
- `src/build_database.py`: cria banco SQLite com as tabelas tratadas.
- `src/export_powerbi_tables.py`: exporta tabelas agregadas para o Power BI.
- `src/create_visualizations.py`: gera graficos simples em Python.
- `src/run_pipeline.py`: executa todas as etapas em sequencia.

## 5. Correcao especifica da base FronkonGames

Durante o projeto foi identificado que o cabecalho do CSV da FronkonGames vem com uma coluna escrita como:

```text
DiscountDLC count
```

Mas os dados se comportam como se fossem duas colunas:

```text
Discount
DLC count
```

Por isso, `src/prepare_data.py` corrige esse cabecalho antes de carregar a base com pandas. Sem essa correcao, as colunas ficam deslocadas e o nome do jogo pode aparecer como data.

## 6. Como executar

Ative o ambiente virtual:

```bash
.venv\Scripts\activate
```

Instale as dependencias, se ainda nao estiverem instaladas:

```bash
pip install pandas numpy matplotlib seaborn sqlalchemy pytest
```

Execute o pipeline:

```bash
python -m src.run_pipeline
```

## 7. Arquivos gerados

Dados tratados:

- `data/processed/steam_games_clean.csv`
- `data/processed/steam_game_genres.csv`
- `data/processed/steam_games.sqlite`

Tabelas agregadas para Power BI:

- `data/processed/powerbi_genre_ratings.csv`
- `data/processed/powerbi_price_ranges.csv`
- `data/processed/powerbi_releases_by_year.csv`
- `data/processed/powerbi_top_developers.csv`
- `data/processed/powerbi_developer_ratings.csv`

Graficos Python:

- `reports/figures/genre_ratings.png`
- `reports/figures/price_ranges.png`
- `reports/figures/releases_by_year.png`

## 8. Validacao feita

A execucao corrigida gerou aproximadamente:

- 122.610 jogos tratados;
- 329.318 registros na tabela `steam_game_genres.csv`;
- lancamentos entre 1997 e 2026;
- 26 generos agregados em `powerbi_genre_ratings.csv`;
- 30 anos agregados em `powerbi_releases_by_year.csv`;
- 7.280 desenvolvedoras em `powerbi_top_developers.csv`.

## 9. Proxima etapa

A proxima etapa e construir o dashboard no Power BI usando os CSVs em `data/processed/`.

O roteiro do dashboard esta em:

```text
docs/powerbi_dashboard_plan.md
```
