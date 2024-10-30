import numpy as np
import pandas as pd
import sys

# Espaço para variáveis globais
item_dict_norm = {}
user_dict_norm = {}

user_dict = {}
item_dict = {}


def process_files(files):
    for file in files:
        with open(file, "r") as input:
            content = input.read()

        modified_content = content.replace(":", ",")

        with open(file, "w") as output:
            output.write(modified_content)


def transform_dataframe(df_ratings):
    user_dict = {}
    item_dict = {}

    for _, row in df_ratings.iterrows():
        user = row["UserId"]
        item = row["ItemId"]
        rating = row["Rating"]

        if user not in user_dict:
            user_dict[user] = {}  # Inicializa o dicionário para o usuário

        user_dict[user][item] = rating  # Armazena a avaliação do usuário para o item

        if item not in item_dict:
            item_dict[item] = {}  # Inicializa o dicionário para o item

        item_dict[item][user] = rating  # Armazena a avaliação do usuário para o item

    return user_dict, item_dict


def mean_center_normalization(dict):
    normalizado = {}
    for usuario_item, avaliacoes in dict.items():
        media = sum(avaliacoes.values()) / len(avaliacoes)
        normalizado[usuario_item] = {
            item: nota - media for item, nota in avaliacoes.items()
        }
    return normalizado


def cosine_similarity(item1_ratings, item2_ratings):
    common_users = set(item1_ratings.keys()).intersection(set(item2_ratings.keys()))

    if len(common_users) == 0:
        return 0  # Se não houver usuários em comum, a similaridade é 0

    ratings1 = np.array([item1_ratings[user] for user in common_users])
    ratings2 = np.array([item2_ratings[user] for user in common_users])

    dot_product = np.dot(ratings1, ratings2)
    norm1 = np.linalg.norm(ratings1)
    norm2 = np.linalg.norm(ratings2)

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot_product / (norm1 * norm2)


def mean(ratings):
    aux = sum(ratings.values()) / len(ratings)
    return aux


def predict_rating(user, item):
    if user not in user_dict or item not in item_dict:
        aux = mean(item_dict.get(item, {}))
        return (
            aux  # Cold Start User ou "Cold Start Item", retorna a média das avaliações
        )

    # Guarda as avaliações do usuário "user"
    user_ratings = user_dict_norm[user]

    if item in user_ratings:
        return user_ratings[item]  # Se o usuário já avaliou o item, retorna a avaliação

    # Calcular similaridade entre o item desejado e os itens avaliados pelo usuário
    similarities = []
    ratings = []

    for rated_item in user_ratings:
        if rated_item in item_dict:
            similarity = cosine_similarity(
                item_dict_norm[rated_item], item_dict_norm.get(item, {})
            )
            similarities.append(similarity)
            ratings.append(user_ratings[rated_item])

    # Prever a nota como a média ponderada pelas similaridades
    if len(similarities) == 0 or sum(similarities) == 0:
        aux = mean(item_dict.get(item, {}))
        return (
            aux  # Se não houver similaridade suficiente, retorna a média das avaliações
        )

    return np.dot(similarities, ratings) / sum(similarities)


def main():
    global user_dict_norm
    global item_dict_norm
    global user_dict
    global item_dict

    # Verifica se os argumentos foram fornecidos corretamente
    if len(sys.argv) < 3:
        print("Uso: python3 main.py ratings.csv targets.csv > submission.csv")
        return

    files = [sys.argv[1], sys.argv[2]]
    process_files(files)

    df_ratings = pd.read_csv(files[0])
    df_targets = pd.read_csv(files[1])
    user_dict, item_dict = transform_dataframe(df_ratings)

    user_dict_norm = mean_center_normalization(user_dict)
    item_dict_norm = mean_center_normalization(item_dict)

    print("UserId:ItemId,Rating")
    for _, row in df_targets.iterrows():
        user = row["UserId"]
        item = row["ItemId"]
        predicted_rating = predict_rating(user, item)
        print(f"{user}:{item},{predicted_rating}")


if __name__ == "__main__":
    main()
