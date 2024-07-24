import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import Flask
from flasgger import Swagger
from flasgger.utils import swag_from

from loh_utils.databases.sql import Book

from api.config import DATABASE_URL, db, documentation
from api.services import BooksInventory
from api.seed import seed_books_to_db


app = Flask(__name__)
app.config['DATABASE_URL'] = DATABASE_URL

# Initialize Swagger
swagger = Swagger(app)

@app.route('/')
def home():
    return 'Inventory api running'

@app.route("/products/books", methods=['GET'])
@swag_from(documentation[0])
def get_all_books():
    inventory = BooksInventory(db=db)
    return inventory.get_books()

@app.route("/products/books/<book_id>", methods=['GET'])
@swag_from(documentation[1])
def get_book_by_id(book_id):
    inventory = BooksInventory(db=db)
    return inventory.get_book_by_id(book_id=book_id)


if __name__ == '__main__':

    # create schemas if not exist
    db.create_schemas(["inventory_db"])

    # create tables in respective schemas if not exist
    db.create_specific_tables(tables=["books"])

    # seed data if not exist
    inv = BooksInventory(db=db)
    seed_books_to_db(num_books=30, book_model_obj=inv)

    app.run(debug=True, port=5001)
