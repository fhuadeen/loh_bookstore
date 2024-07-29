import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import request, Blueprint, jsonify
from flasgger.utils import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity

from loh_utils.databases.sql import User

from api.config import AI_BASE_URL, db, documentation
from api.routes.network import make_request
from api.validators import validate, SummariseBookValidator

ai_bp = Blueprint('ai', __name__)


@ai_bp.route("book/summarise", methods=['POST'])
@jwt_required()
@swag_from(documentation[10])
def place_order():
    data = request.get_json()

    try:
        validated_data = validate(SummariseBookValidator, data)
    except Exception as err:
        return jsonify({"error": str(err)}), 400

    # get current user id
    current_user_username = get_jwt_identity()
    current_user: User = db.query(username=current_user_username)
    user_id = current_user.id

    validated_data["user_id"] = user_id

    res = make_request(
        url=f"{AI_BASE_URL}/oms/orders/buy",
        headers=dict(request.headers),
        method=request.method,
        body=validated_data,
    )
    return jsonify(res.json()), 200
