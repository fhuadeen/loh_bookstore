import os
import json
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from loh_utils.databases.sql import PostgreSQL

load_dotenv()

DATABASE_URL: str = str(os.getenv("DATABASE_URL"))

RABBITMQ_HOST = str(os.getenv("RABBITMQ_HOST"))
RABBITMQ_PORT = str(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USERNAME = str(os.getenv("RABBITMQ_USERNAME"))
RABBITMQ_PASSWORD = str(os.getenv("RABBITMQ_PASSWORD"))

INVENTORY_QUEUE = str(os.getenv("INVENTORY_QUEUE"))

db = PostgreSQL(database_url=DATABASE_URL)

doc_path = os.path.join(BASE, "documentation.json")
with open(doc_path, 'r') as file:
    documentation = json.load(file)
