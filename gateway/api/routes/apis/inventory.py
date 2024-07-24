import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import Flask, request, Blueprint, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required

from api.config import INVENTORY_BASE_URL, documentation
from api.services import UserAuth
from api.routes.network import make_request

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route("/books", methods=['GET'])
@swag_from(documentation[3])
@jwt_required()
def get_all_books():
    res = make_request(
        url=f"{INVENTORY_BASE_URL}/products/books",
        headers=dict(request.headers),
        method=request.method,
    )
    return jsonify(res.json()), 200

@inventory_bp.route("/books/<book_id>", methods=['GET'])
@jwt_required()
@swag_from(documentation[4])
def get_book_by_id(book_id):
    res = make_request(
        url=f"{INVENTORY_BASE_URL}/products/books/{book_id}",
        headers=dict(request.headers),
        method=request.method,
    )
    return jsonify(res.json()), 200
