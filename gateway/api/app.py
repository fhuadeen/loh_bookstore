import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager

from api.config import DATABASE_URL, db, JWT_SECRET_KEY
from api.routes.apis.auth import auth_bp
from api.routes.apis.inventory import inventory_bp


def create_app():
    app = Flask(__name__)

    app.config['DATABASE_URL'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(inventory_bp, url_prefix='/products')

    return app

app = create_app()

# Initialize Swagger
swagger = Swagger(app)

# Initialize JWT
jwt = JWTManager(app)

@app.route('/')
def home():
    return 'Gateway api running'


if __name__ == '__main__':

    # create schemas if not exist
    db.create_schemas(["gateway_db", "oms_db", "inventory_db"])

    # create tables in respective schemas if not exist
    db.create_all_tables()

    app.run(debug=True, port=5000)
