from flask import Flask, abort, jsonify, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from helper import get_recommended_books



app = Flask(__name__)
app.app_context().push()
app.secret_key = 'something_secret'


""" Routes
"""
@app.route('/', methods=['GET'])
def hello():
    df_users = pd.read_csv('data/ratings_with_clusters.csv')
    user_ids = df_users['user_id'].unique().tolist()
    return render_template('index.html', users=user_ids)


@app.route('/users/', methods=['GET'])
def users():
    df_users = pd.read_csv('data/ratings_with_clusters.csv')
    user_ids = df_users['user_id'].unique().tolist()

    return jsonify(user_ids)

@app.route('/books/recommendation/', methods=['POST'])
def recommended_books():
    """
        Returns n_books books recommended to the user.

        - `user_id: <int>` ID of the user.
        - `n_books: <int>` Quantity of desired recommended books.
    """

    data = request.get_json()
    print(data)
    if not data:
        abort(400, 'No data provided.')
    
    user_id = int(data.get('user_id'))
    n_books = int(data.get('n_books'))+1

    df_books = pd.read_csv('data/books.csv')
    df_clusters = pd.read_csv('data/ratings_with_clusters.csv')

    if user_id not in df_clusters['user_id'].unique():
        abort(400, f"User ID {user_id} not found.")

    recommendations = get_recommended_books(df=df_clusters, user_id=user_id, n_books=n_books)

    result = []
    for isbn in recommendations:
        if isbn not in df_books['ISBN'].values:
            continue
        book = df_books[df_books['ISBN'] == isbn].iloc[0]
        book_info = {
            'ISBN': str(isbn),
            'Book_Title': book['Book_Title'],
            'Book_Author': book['Book_Author'],
            'Publisher': book['Publisher'],
            'Image_URL': book['Image_URL']
        }
        result.append(book_info)

    return jsonify(result)


# Start app
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        use_reloader=True,
        debug=True,
    )
