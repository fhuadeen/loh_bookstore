import os
import json
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from loh_utils.databases.sql import PostgreSQL

load_dotenv()

DATABASE_URL: str = str(os.getenv("DATABASE_URL"))
TOKEN_EXPIRY_HOURS: str = str(os.getenv("TOKEN_EXPIRY_HOURS"))
JWT_SECRET_KEY: str = str(os.getenv("JWT_SECRET_KEY"))
INVENTORY_BASE_URL: str = str(os.getenv("INVENTORY_BASE_URL"))
OMS_BASE_URL: str = str(os.getenv("OMS_BASE_URL"))
AI_BASE_URL: str = str(os.getenv("AI_BASE_URL"))

db = PostgreSQL(database_url=DATABASE_URL)

doc_path = os.path.join(BASE, "documentation.json")
with open(doc_path, 'r') as file:
    documentation = json.load(file)
