import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import Flask, request
from flasgger import Swagger
from flasgger.utils import swag_from

from api.config import documentation
from api.services import LoHstack


app = Flask(__name__)

# Initialize Swagger
swagger = Swagger(app)

@app.route('/')
def home():
    return 'Payment api running'

@app.route("/payment/pay", methods=['POST'])
@swag_from(documentation[0])
def make_payment():
    data = request.get_json()
    payment = LoHstack()
    return payment.pay(data)


if __name__ == '__main__':

    app.run(debug=True, port=5003)
