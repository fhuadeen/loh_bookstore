import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import Flask, request, Blueprint
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required

from api.config import DATABASE_URL, db, documentation, JWT_SECRET_KEY
from api.services import UserAuth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
@swag_from(documentation[0])
def signup():
    data = request.get_json()

    auth = UserAuth(db=db)
    return auth.signup(data)

@auth_bp.route('/login', methods=['POST'])
@swag_from(documentation[1])
def login():
    data = request.get_json()

    auth = UserAuth(db=db)
    return auth.login(data)

# Get current user endpoint
@auth_bp.route('/users/me', methods=['GET'])
@jwt_required()
@swag_from(documentation[2])
def get_current_user():
    auth = UserAuth(db=db)
    return auth.get_current_user()
