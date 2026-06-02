# Plano do Projeto

## Tema

Analise de dados de jogos da Steam com foco em avaliacoes, preco, genero, desenvolvedoras e evolucao dos lancamentos.

## Hipoteses iniciais

- Generos diferentes podem ter padroes distintos de avaliacao.
- Jogos mais caros nao necessariamente possuem melhores notas.
- O volume de lancamentos cresceu com o tempo, especialmente apos a popularizacao de publicacao independente.
- Desenvolvedoras com muitos jogos podem ter desempenho medio diferente de estudios com poucos lancamentos.

## Etapas

1. Escolher e documentar a fonte de dados.
2. Baixar ou importar a base para `data/raw/`.
3. Criar script Python de limpeza e padronizacao.
4. Exportar dados tratados para `data/processed/`.
5. Modelar uma base SQL para consultas analiticas.
6. Criar consultas SQL para responder as perguntas principais.
7. Construir o dashboard no Power BI.
8. Documentar os principais insights no README.

## Colunas esperadas

- Nome do jogo.
- Data ou ano de lancamento.
- Genero ou lista de generos.
- Desenvolvedora.
- Preco.
- Avaliacao ou percentual de reviews positivas.
- Quantidade de avaliacoes.

## Cuidados de analise

- Separar jogos gratuitos de pagos.
- Tratar jogos com poucas avaliacoes para evitar distorcoes.
- Padronizar generos quando houver listas de generos no mesmo campo.
- Documentar criterios de limpeza e filtros aplicados.
