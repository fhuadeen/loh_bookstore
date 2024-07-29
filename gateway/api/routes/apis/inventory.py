import os
import sys
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import request, Blueprint, jsonify
from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required

from api.config import INVENTORY_BASE_URL, documentation
from api.routes.network import make_request
from api.validators import validate

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

@inventory_bp.route("/books/create", methods=['PATCH'])
@jwt_required()
@swag_from(documentation[4])
def create_book():
    data = request.form.get('payload')

    if data:
        data = json.loads(data)
    else:
        return jsonify({"message": "In put Book form"}, 400)

    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}, 400)
    file = request.files["file"]

    res = make_request(
        url=f"{INVENTORY_BASE_URL}/products/books/create",
        headers=dict(request.headers),
        method=request.method,
        body=data,
        files={file.filename: file}
    )
    return jsonify(res.json()), 200
