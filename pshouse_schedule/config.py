import os
from dotenv import load_dotenv

cwd = os.getcwd()
basedir = os.path.abspath(cwd)
dotenv_path = os.path.join(cwd, ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

STORAGE_ROOT_DIR = "./results"
STORAGE_BUCKET_NAME = "pshouse-schedule"
STORAGE_TYPE = os.getenv("STORAGE_TYPE") or "LOCAL"
STORAGE_KEY = os.getenv("STORAGE_KEY") or "./results"
STORAGE_SECRET = os.getenv("STORAGE_SECRET") or "test-secret"

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or \
    "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_ENGINE_OPTIONS = {
    "echo": os.getenv("SQL_ECHO") or False
}

SCHEDULER_TIMEZONE = "Asia/Taipei"
