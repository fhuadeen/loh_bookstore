import os
import json
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from loh_utils.databases.sql import PostgreSQL

load_dotenv()


RABBITMQ_HOST = str(os.getenv("RABBITMQ_HOST"))
RABBITMQ_PORT = str(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USERNAME = str(os.getenv("RABBITMQ_USERNAME"))
RABBITMQ_PASSWORD = str(os.getenv("RABBITMQ_PASSWORD"))

AI_QUEUE = str(os.getenv("AI_QUEUE"))

AWS_ACCESS_KEY_ID = str(os.getenv("AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = str(os.getenv("AWS_SECRET_ACCESS_KEY"))
S3_BUCKET_NAME = str(os.getenv("S3_BUCKET_NAME"))

OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))

doc_path = os.path.join(BASE, "documentation.json")
with open(doc_path, 'r') as file:
    documentation = json.load(file)
