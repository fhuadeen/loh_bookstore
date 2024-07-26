import os
import sys
import asyncio

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import request, Flask
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_socketio import SocketIO
import websockets

from api.config import DATABASE_URL, db, documentation
from api.services import BookOMS


app = Flask(__name__)
app.config['DATABASE_URL'] = DATABASE_URL

socketio = SocketIO(app)

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

@app.route("/oms/orders/buy", methods=['POST'])
@swag_from(documentation[2])
def place_order():
    data = request.get_json()
    oms = BookOMS(db=db)
    return oms.place_order(data)

@app.route('/oms/orders/status/update', methods=['PATCH'])
@swag_from(documentation[3])
def update_order_status():
    data = request.get_json()

    oms = BookOMS(db=db)
    return oms.update_order_status(data)


if __name__ == '__main__':

    # create schemas if not exist.
    db.create_schemas(["oms_db"])

    # create tables in respective schemas if not exist
    db.create_specific_tables(tables=["orders"])

    # app.run(debug=True, port=5002)
    socketio.run(app, debug=True, host='localhost', port=5002)
