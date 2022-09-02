import io
import json
import logging
from datetime import datetime
from pathlib import Path

import pshouse_schedule.config as config
from pshouse_schedule.fetch import fetch_deals
from pshouse_schedule.parse import parse_deals_info, parse_incorrect_deals_info
from pshouse_schedule.load import load_into_database
from pshouse_schedule.storage import save_to_storage

logger = logging.getLogger()


def process_crawl_of_deals():
    logger.info("start process_crawl_of_deals")

    content = fetch_deals()

    if content is None:
        logger.info("start process_crawl_of_deals return None")
        return

    today = str(datetime.now().date())
    save_to_storage(
        dirname=f"{today}",
        filepath=Path(config.STORAGE_ROOT_DIR).joinpath("F_lvr_land_B.csv"),
        content=io.BytesIO(content),
    )

    deals, deals_need_checked = parse_deals_info(content)
    load_into_database(deals)

    deals_need_checked = parse_incorrect_deals_info(deals_need_checked)
    save_to_storage(
        dirname=f"{today}",
        filepath=Path(config.STORAGE_ROOT_DIR).joinpath(
            "F_lvr_land_B_need_checked.json"),
        content=json.dumps(
            obj=deals_need_checked,
            indent=4,
            ensure_ascii=False,
        ).encode("utf-8"),
    )
