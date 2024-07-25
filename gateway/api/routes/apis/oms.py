import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import request, Blueprint, jsonify
from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity

from loh_utils.databases.sql import User

from api.config import OMS_BASE_URL, documentation, db
from api.routes.network import make_request

oms_bp = Blueprint('oms', __name__)

@oms_bp.route("/orders", methods=['GET'])
@swag_from(documentation[5])
@jwt_required()
def get_all_user_orders():

    # get current user id
    current_user_username = get_jwt_identity()
    current_user: User = db.query(username=current_user_username)
    user_id = current_user.id

    res = make_request(
        url=f"{OMS_BASE_URL}/oms/orders/{user_id}",
        headers=dict(request.headers),
        method=request.method,
    )
    return jsonify(res.json()), 200

@oms_bp.route("/orders/<order_id>", methods=['GET'])
@jwt_required()
@swag_from(documentation[6])
def get_book_by_id(order_id):

    # get current user id
    current_user_username = get_jwt_identity()
    current_user: User = db.query(username=current_user_username)
    user_id = current_user.id

    res = make_request(
        url=f"{OMS_BASE_URL}/oms/orders/{order_id}/{user_id}",
        headers=dict(request.headers),
        method=request.method,
    )
    return jsonify(res.json()), 200

@oms_bp.route("/orders/buy", methods=['POST'])
@jwt_required()
@swag_from(documentation[7])
def place_order():
    data = request.get_json()

    # get current user id
    current_user_username = get_jwt_identity()
    current_user: User = db.query(username=current_user_username)
    user_id = current_user.id

    data["user_id"] = user_id

    res = make_request(
        url=f"{OMS_BASE_URL}/oms/orders/buy",
        headers=dict(request.headers),
        method=request.method,
        body=data,
    )
    return jsonify(res.json()), 200


if __name__ == '__main__':

    # create schemas if not exist
    db.create_schemas(["oms_db"])

    # create tables in respective schemas if not exist
    db.create_specific_tables(tables=["orders"])

    app.run(debug=True, port=5002)
