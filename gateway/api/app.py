import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, jwt_required

from api.config import DATABASE_URL, db, documentation, JWT_SECRET_KEY
from api.services import UserAuth

app = Flask(__name__)
app.config['DATABASE_URL'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

# Initialize Swagger
swagger = Swagger(app)

# Initialize JWT
jwt = JWTManager(app)

@app.route('/')
def home():
    return 'App running'

@app.route('/auth/signup', methods=['POST'])
@swag_from(documentation[0])
def signup():
    data = request.get_json()

    auth = UserAuth(db=db)
    return auth.signup(data)

@app.route('/auth/login', methods=['POST'])
@swag_from(documentation[1])
def login():
    data = request.get_json()

    auth = UserAuth(db=db)
    return auth.login(data)

# Get current user endpoint
@app.route('/user/me', methods=['GET'])
@jwt_required()
@swag_from(documentation[2])
def get_current_user():
    auth = UserAuth(db=db)
    return auth.get_current_user()


if __name__ == '__main__':

    # create schemas if not exist
    db.create_schemas(["oms_db", "inventory_db"])

    # create tables in respective schemas if not exist
    db.create_all_tables()

    app.run(debug=True)
