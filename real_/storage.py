import logging
from pathlib import Path
from cloudstorage import get_driver_by_name

from real_ import config

logger = logging.getLogger()


class Storage:
    def __init__(self, dir_name=""):
        self.driver_cls = get_driver_by_name(config.STORAGE_TYPE)
        storage = self.driver_cls(
            key=config.STORAGE_KEY,
            secret=config.STORAGE_SECRET,
        )
        self.container = storage.create_container(
            f"actual_price_registration/{dir_name}"
        )

    def upload(self, filepath):
        self.container.upload_blob(filepath)


def save_to_storage(dir_name, filepath, content):
    logger.info("   step: save_to_storage")

    Path(config.STORAGE_ROOT_DIR).mkdir(parents=True, exist_ok=True)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        s = Storage(dir_name)
        s.upload(filepath)
    except Exception as e:
        logger.warning(f"   storage error: {repr(e)}")
