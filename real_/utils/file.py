from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from real_ import config


def extract_to(folderpath, content):
    Path(config.STORAGE_ROOT_DIR).mkdir(parents=True, exist_ok=True)

    with ZipFile(BytesIO(content), 'r') as zipf:
        zipf.extractall(folderpath)
