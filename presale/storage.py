import io
import logging
from pathlib import Path
from cloudstorage import get_driver_by_name

from presale import config

logger = logging.getLogger()


class Storage:
    def __init__(self, dirname=""):
        self.driver_cls = get_driver_by_name(config.STORAGE_TYPE)
        storage = self.driver_cls(
            key=config.STORAGE_KEY,
            secret=config.STORAGE_SECRET,
        )
        self.container = storage.create_container(
            f"actual_price_registration/{dirname}"
        )

    def upload(self, filepath_or_fileobj, **kwargs):
        self.container.upload_blob(filepath_or_fileobj, **kwargs)


def save_to_storage(dirname, filename, content, filepath=None):
    logger.info("   step: save_to_storage")

    Path(config.STORAGE_ROOT_DIR).mkdir(parents=True, exist_ok=True)

    try:
        filepath_or_fileobj = filepath if filepath else io.BytesIO(content)

        s = Storage(dirname)
        s.upload(
            filepath_or_fileobj=filepath_or_fileobj,
            blob_name=filename,
        )
    except Exception as e:
        logger.warning(f"   storage error: {repr(e)}")
