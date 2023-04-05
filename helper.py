import pandas as pd


def get_recommended_books(df:pd.DataFrame, user_id:int, n_books:int = None) -> list:
    """ Retorna `n_books`Recomendação de livros para cada usuário.
        Returns a list of `ISBNs` of recommended books for a user.
    """
     
     # Encontra o cluster do usuário
    user_cluster = df.loc[df['user_id'] == user_id, 'Cluster'].iloc[0]

    # Filtra os usuários do mesmo cluster e seleciona os livros bem avaliados por eles
    similar_users = df.loc[df['Cluster'] == user_cluster]
    livros_melhor_avaliados = similar_users.loc[similar_users['Book_Rating'] >= 4.0, 'ISBN'].unique()

    # Se o número de livros recomendados não for especificado, retorna todos os livros bem avaliados
    if n_books is None:
        return livros_melhor_avaliados
    # Caso contrário, retorna os primeiros n livros da lista
    else:
        return livros_melhor_avaliados[:n_books]
