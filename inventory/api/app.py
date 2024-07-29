import os
import sys
from multiprocessing import Process
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import Flask, request, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from
from werkzeug.utils import secure_filename

from loh_utils.databases.sql import Book

from api.config import DATABASE_URL, db, documentation
from api.services import BooksInventory
from api.seed import seed_books_to_db
from api.consumers import consume_products_update


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

@app.route("/products/books/create", methods=["POST"])
@swag_from(documentation[2])
def create_book():
    data = request.form.get('payload')

    if data:
        data = json.loads(data)
    else:
        return jsonify({"message": "In put Book form"}, 400)

    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}, 400)
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}, 400)
    
    inventory = BooksInventory(db=db)
    return inventory.create_book(data, file)


if __name__ == '__main__':

    # create schemas if not exist
    db.create_schemas(["inventory_db"])

    # create tables in respective schemas if not exist
    db.create_specific_tables(tables=["books"])

    # seed data if not exist
    inv = BooksInventory(db=db)
    seed_books_to_db(num_books=30, book_model_obj=inv)

    # Start the RabbitMQ consumers
    consumer_processes = [
        Process(target=consume_products_update),
    ]

    for i in consumer_processes:
        i.start()

    app.run(debug=True, port=5001)
