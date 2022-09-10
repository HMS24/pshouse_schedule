import logging
from cloudstorage import get_driver_by_name
from cloudstorage.exceptions import NotFoundError

import pshouse_schedule.config as config

logger = logging.getLogger()


class Storage:
    def __init__(self, dirname=""):
        self.driver_cls = get_driver_by_name(config.STORAGE_TYPE)
        storage = self.driver_cls(
            key=config.STORAGE_KEY,
            secret=config.STORAGE_SECRET,
        )
        try:
            self.container = storage.get_container(dirname)
        except NotFoundError:
            self.container = storage.create_container(dirname)

    def upload(self, filepath):
        self.container.upload_blob(filepath)


def save_to_storage(dirname, filepath, content):
    logger.info("   step: save_to_storage")

    try:
        with open(filepath, "w", encoding="utf-8-sig") as f:
            f.write(content)

        s = Storage(dirname)
        s.upload(filepath)
    except Exception as e:
        logger.warning(f"   storage error: {repr(e)}")
