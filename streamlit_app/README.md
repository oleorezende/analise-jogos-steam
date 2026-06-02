# Dashboard Streamlit

Dashboard interativo alternativo ao Power BI.

Esta versao foi criada para aprendizado e exploracao rapida dos dados com Python. A ideia principal do projeto continua sendo construir o dashboard final em Power BI.

## Como rodar

Ative o ambiente virtual:

```bash
.venv\Scripts\activate
```

Instale o Streamlit:

```bash
pip install streamlit
```

Execute o app:

```bash
streamlit run streamlit_app/app.py
```

O dashboard usa os arquivos tratados em:

```text
data/processed/steam_games_clean.csv
data/processed/steam_game_genres.csv
```

Se esses arquivos ainda nao existirem, rode antes:

```bash
python -m src.run_pipeline
```

## O que este app mostra

- indicadores gerais da base;
- filtros por ano, genero, preco e minimo de reviews;
- evolucao dos lancamentos;
- generos mais frequentes e melhor avaliados;
- relacao entre preco e avaliacao;
- desenvolvedoras com maior volume e melhores avaliacoes;
- tabela exploravel de jogos.
