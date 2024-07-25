import os
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


doc_path = os.path.join(BASE, "documentation.json")
with open(doc_path, 'r') as file:
    documentation = json.load(file)
