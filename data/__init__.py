import pandas as pd
import sqlalchemy


def load_data():
    engine = sqlalchemy.create_engine('sqlite:///ratings.db')
    
    

    print('INFO: Data loaded in Database')
