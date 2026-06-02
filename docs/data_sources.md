# Fontes de Dados Candidatas

Este documento registra fontes candidatas para a base de dados do projeto.

## Criterios de escolha

A fonte ideal deve conter, no minimo:

- nome do jogo;
- data de lancamento;
- preco;
- genero;
- desenvolvedora;
- avaliacoes ou percentual de reviews positivas;
- quantidade de reviews, se disponivel.

## Opcoes iniciais

### Kaggle - Steam Games Dataset 2021-2025 (65k+)

Link: https://www.kaggle.com/datasets/jypenpen54534/steam-games-dataset-2021-2025-65k

Pontos fortes:

- recorte recente;
- possui campos como `appid`, `release_date`, `price`, `developer` e genero;
- bom para evolucao de lancamentos recentes.

Ponto de atencao:

- pode limitar analises historicas se o foco for somente 2021-2025.

### Kaggle - Steam Games Dataset

Link: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset

Pontos fortes:

- base ampla de jogos da Steam;
- possui preco, data de lancamento, desenvolvedoras e generos;
- boa candidata para analises gerais de catalogo.

Ponto de atencao:

- validar se os campos de avaliacao estao completos para as perguntas do projeto.

### Mendeley Data - Steam Games Metadata and Player Reviews (2020-2024)

Link: https://data.mendeley.com/datasets/jxy85cr3th/2

Pontos fortes:

- inclui metadados e reviews de jogadores;
- pode enriquecer analises de sentimento e volume de avaliacoes;
- fonte academica, interessante para documentacao.

Ponto de atencao:

- escopo temporal limitado entre 2020 e 2024.

## Recomendacao inicial

Comecar com uma base Kaggle ampla para construir o pipeline e o dashboard principal. Depois, se fizer sentido, usar uma fonte com reviews mais detalhadas para enriquecer a analise.
