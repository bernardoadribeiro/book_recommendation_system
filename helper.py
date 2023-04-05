import pandas as pd


def get_recommended_books(df:pd.DataFrame, user_id:int, n_books:int = None) -> list:
    """
        Returns `n_books` books recommended to the user
    """
     
     # find the user's Cluster
    user_cluster = df.loc[df['user_id'] == user_id, 'Cluster'].iloc[0]

    # Filter the books by the user's cluster, and select the top `n_books` books
    similar_users = df.loc[df['Cluster'] == user_cluster]
    livros_melhor_avaliados = similar_users.loc[similar_users['Book_Rating'] >= 4.0, 'ISBN'].unique()

    # If n_books isn't inputed, Returns all books that is recommended to the user
    if n_books is None:
        return livros_melhor_avaliados
    # In other case, return the n_books most voted of the user's cluster
    else:
        return livros_melhor_avaliados[:n_books]
