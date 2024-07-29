import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

load_dotenv()

NOTIFICATION_SERVER_HOST: str = str(os.getenv("NOTIFICATION_SERVER_HOST"))
