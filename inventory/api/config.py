import os
import json
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from loh_utils.databases.sql import PostgreSQL
from loh_utils.media.s3 import S3
from loh_utils.event_bus import RabbitMQ

load_dotenv()

DATABASE_URL: str = str(os.getenv("DATABASE_URL"))

RABBITMQ_HOST = str(os.getenv("RABBITMQ_HOST"))
RABBITMQ_PORT = str(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USERNAME = str(os.getenv("RABBITMQ_USERNAME"))
RABBITMQ_PASSWORD = str(os.getenv("RABBITMQ_PASSWORD"))

AWS_ACCESS_KEY_ID = str(os.getenv("AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = str(os.getenv("AWS_SECRET_ACCESS_KEY"))
S3_BUCKET_NAME = str(os.getenv("S3_BUCKET_NAME"))

INVENTORY_QUEUE = str(os.getenv("INVENTORY_QUEUE"))
AI_QUEUE = str(os.getenv("AI_QUEUE"))

db = PostgreSQL(database_url=DATABASE_URL)

event_bus = RabbitMQ(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    username=RABBITMQ_USERNAME,
    password=RABBITMQ_PASSWORD,
)

s3_obj = S3(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    bucket_name=S3_BUCKET_NAME,
)

doc_path = os.path.join(BASE, "documentation.json")
with open(doc_path, 'r') as file:
    documentation = json.load(file)
