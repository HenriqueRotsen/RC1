# Documentação do Código

## Descrição Geral

Este código implementa um sistema de recomendação baseado em filtragem colaborativa utilizando a similaridade de cosseno. Ele lê dados de avaliações de usuários sobre itens e prevê avaliações para um conjunto de itens alvo com base nas avaliações anteriores.

## Dependências

- `numpy`: Usado para operações matemáticas.
- `pandas`: Usado para manipulação de dados tabulares.
- `sys`: Usado para manipulação de argumentos de linha de comando.

## Estrutura do Código

### Variáveis Globais

- `item_dict_norm`: Dicionário que armazena as avaliações normalizadas por item.
- `user_dict_norm`: Dicionário que armazena as avaliações normalizadas por usuário.
- `user_dict`: Dicionário que armazena as avaliações por usuário.
- `item_dict`: Dicionário que armazena as avaliações por item.

### Funções

#### `process_files(files)`

Lê arquivos de entrada, substituindo os caracteres `:` por `,`, e grava as alterações nos mesmos arquivos.

**Parâmetros:**
- `files`: Lista de nomes de arquivos a serem processados.

#### `transform_dataframe(df_ratings)`

Transforma um DataFrame de avaliações em dois dicionários: um para usuários e outro para itens.

**Parâmetros:**
- `df_ratings`: DataFrame contendo colunas `UserId`, `ItemId` e `Rating`.

**Retorno:**
- Dois dicionários: `user_dict` e `item_dict`.

#### `mean_center_normalization(dict)`

Normaliza as avaliações subtraindo a média das avaliações de cada item.

**Parâmetros:**
- `dict`: Dicionário contendo as avaliações a serem normalizadas.

**Retorno:**
- Dicionário com as avaliações normalizadas.

#### `cosine_similarity(item1_ratings, item2_ratings)`

Calcula a similaridade entre duas listas de avaliações de itens utilizando a fórmula da similaridade de cosseno.

**Parâmetros:**
- `item1_ratings`: Dicionário de avaliações do primeiro item.
- `item2_ratings`: Dicionário de avaliações do segundo item.

**Retorno:**
- Similaridade entre os dois itens (float).

#### `mean(ratings)`

Calcula a média das avaliações.

**Parâmetros:**
- `ratings`: Dicionário contendo as avaliações.

**Retorno:**
- Média das avaliações (float).

#### `predict_rating(user, item)`

Prevê a avaliação de um usuário para um item específico.

**Parâmetros:**
- `user`: ID do usuário.
- `item`: ID do item.

**Retorno:**
- Avaliação prevista (float). Retorna a média das avaliações se o usuário ou item for desconhecido.

#### `main()`

Função principal que executa o fluxo do programa.

**Processo:**
1. Verifica se os argumentos necessários foram fornecidos.
2. Processa os arquivos de entrada.
3. Carrega as avaliações e os itens alvo em DataFrames.
4. Transforma os DataFrames em dicionários.
5. Normaliza os dicionários de avaliações.
6. Para cada item alvo, prevê e imprime a avaliação.

### Execução

O programa deve ser executado a partir da linha de comando com a seguinte sintaxe:

```bash
python3 main.py ratings.csv targets.csv > submission.csv
```

Onde:
- `ratings.csv` é o arquivo que contém as avaliações de usuários sobre itens.
- `targets.csv` é o arquivo que contém as avaliações a serem previstas.
- A saída será redirecionada para `submission.csv`, que conterá as previsões no formato `UserId:ItemId,Rating`.

## Considerações Finais

Este sistema de recomendação é uma implementação básica e pode ser aprimorado com técnicas de aprendizado de máquina ou algoritmos mais complexos. O tratamento de casos como usuários ou itens novos (cold start) é feito retornando a média das avaliações, mas outras abordagens podem ser exploradas.
