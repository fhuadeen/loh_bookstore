import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import Flask
from flasgger import Swagger
from flasgger.utils import swag_from

from api.config import DATABASE_URL, db, documentation
from api.services import BookOMS


app = Flask(__name__)
app.config['DATABASE_URL'] = DATABASE_URL

# Initialize Swagger
swagger = Swagger(app)

@app.route('/')
def home():
    return 'OMS api running'

@app.route("/oms/orders/<user_id>", methods=['GET'])
@swag_from(documentation[0])
def get_all_user_orders(user_id):
    oms = BookOMS(db=db)
    return oms.get_orders(user_id=user_id)

@app.route("/oms/orders/<order_id>/<user_id>", methods=['GET'])
@swag_from(documentation[1])
def get_book_by_id(order_id, user_id):
    oms = BookOMS(db=db)
    return oms.get_order_by_id(order_id=order_id, user_id=user_id)


if __name__ == '__main__':

    # create schemas if not exist
    db.create_schemas(["oms_db"])

    # create tables in respective schemas if not exist
    db.create_specific_tables(tables=["orders"])

    app.run(debug=True, port=5002)
