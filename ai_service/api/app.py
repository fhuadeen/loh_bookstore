import os
import sys
from multiprocessing import Process
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from flask import request, Flask
from flasgger import Swagger
from flasgger.utils import swag_from

from api.config import documentation
from api.services import AIService
from api.events import consume_embed_book_content


app = Flask(__name__)

# Initialize Swagger
swagger = Swagger(app)

@app.route('/')
def home():
    return 'AI api running'

@app.route("/book/summarise", methods=['POST'])
@swag_from(documentation[0])
def summarise_book():
    data = request.get_json()
    ai = AIService()
    return ai.summarise(data)


if __name__ == '__main__':

    # Start the RabbitMQ consumers
    consumer_processes = [
        Process(target=consume_embed_book_content),
    ]

    for i in consumer_processes:
        i.start()

    app.run(debug=True, port=5005)
