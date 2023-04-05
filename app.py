from flask import Flask, abort, jsonify, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import sqlalchemy
from data import load_data
from helper import get_recommended_books

# Import routes (to register blueprints)
# from routes import books


app = Flask(__name__)
app.app_context().push()
app.secret_key = 'something_secret'

""" Database Setup
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db, directory='./migrations')

from sqlalchemy_serializer import SerializerMixin

class Books(db.Model, SerializerMixin):
    ISBN = db.Column(db.Integer, primary_key=True)
    Book_Title = db.Column(db.String)
    Book_Author = db.Column(db.String)
    Year_Of_Publication = db.Column(db.Integer)
    Publisher = db.Column(db.String)
    Image_URL = db.Column(db.String)
    Clusters = db.Column(db.Integer)


# engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI']) 
# df_book = pd.read_csv('data/books.csv')
# df_book.to_sql('books', engine, if_exists='append')
# df_clus = pd.read_csv('data/ratings_with_clusters.csv')
# df_clus.to_sql('books', engine, if_exists='append')

""" Routes
"""
@app.route('/', methods=['GET'])
def hello():
    df_users = pd.read_csv('data/ratings_with_clusters.csv')

    user_ids = df_users['user_id'].unique().tolist()
    return render_template('index.html', user_ids=user_ids)

@app.route('/books', methods=['GET'])
def books():
    return render_template('books/index.html')

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
    
    user_id = data['user_id']
    n_books = data['n_books']

    df_books = pd.read_csv('data/books.csv')
    df_clusters = pd.read_csv('data/ratings_with_clusters.csv')

    recommendations = get_recommended_books(df=df_clusters, user_id=user_id, n_books=n_books)

    result = []
    for isbn in recommendations:
        book = df_books[df_books['ISBN'] == isbn].iloc[0]
        book_info = {
            'ISBN': str(isbn),
            'Book_Title': book['Book_Title'],
            'Book_Author': book['Book_Author'],
            'Publisher': book['Publisher'],
            'Image_URL': book['Image_URL']
        }
        result.append(book_info)

    return result


# Start app
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        use_reloader=True,
        debug=True,
    )

# Register routes
# app.register_blueprint(books.books_bp, url_prefix='/')


# Import database models from models
# from models import Books