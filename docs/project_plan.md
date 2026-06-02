# Plano do Projeto

## Tema

Analise de dados de jogos da Steam com foco em avaliacoes, preco, genero, desenvolvedoras e evolucao dos lancamentos.

## Hipoteses iniciais

- Generos diferentes podem ter padroes distintos de avaliacao.
- Jogos mais caros nao necessariamente possuem melhores notas.
- O volume de lancamentos cresceu com o tempo, especialmente apos a popularizacao de publicacao independente.
- Desenvolvedoras com muitos jogos podem ter desempenho medio diferente de estudios com poucos lancamentos.

## Etapas do projeto

### Concluido

1. Criar estrutura inicial do repositorio.
2. Documentar objetivo, perguntas de negocio e ferramentas.
3. Escolher fonte principal de dados.
4. Criar guia de download da base.
5. Criar pipeline Python para leitura e limpeza.
6. Corrigir leitura do CSV da FronkonGames.
7. Exportar dados tratados para `data/processed/`.
8. Criar banco SQLite.
9. Criar consultas SQL iniciais.
10. Gerar tabelas agregadas para Power BI.
11. Criar graficos exploratorios em Python.
12. Validar volume e consistencia dos dados tratados.

### Pendente

1. Construir dashboard no Power BI.
2. Salvar arquivo `.pbix` em `powerbi/`.
3. Extrair insights finais.
4. Atualizar README com prints, conclusoes e limitacoes.

## Colunas tratadas

Tabela `steam_games_clean.csv`:

- `app_id`;
- `name`;
- `release_date`;
- `release_year`;
- `developer`;
- `price_usd`;
- `positive_reviews`;
- `negative_reviews`;
- `total_reviews`;
- `positive_review_percentage`.

Tabela `steam_game_genres.csv`:

- `app_id`;
- `genre`.

## Cuidados de analise

- Separar jogos gratuitos de pagos.
- Tratar jogos com poucas avaliacoes para evitar distorcoes.
- Padronizar generos quando houver varios generos no mesmo campo.
- Nao subir o arquivo bruto para o GitHub.
- Documentar criterios de limpeza e filtros aplicados.
- No Power BI, usar filtros minimos de reviews para rankings mais confiaveis.

## Validacao atual

A execucao corrigida do pipeline gerou:

- 122.610 jogos tratados;
- 329.318 registros de jogo-genero;
- anos de lancamento entre 1997 e 2026;
- tabelas agregadas para generos, precos, lancamentos e desenvolvedoras.
