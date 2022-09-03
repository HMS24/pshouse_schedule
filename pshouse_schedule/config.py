import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

STORAGE_ROOT_DIR = "./results"
STORAGE_BUCKET_NAME = "pshouse-schedule"
STORAGE_TYPE = os.getenv("STORAGE_TYPE") or "LOCAL"
STORAGE_KEY = os.getenv("STORAGE_KEY") or "./results"
STORAGE_SECRET = os.getenv("STORAGE_SECRET") or "test-secret"
