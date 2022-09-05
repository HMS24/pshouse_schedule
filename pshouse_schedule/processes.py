import json
import logging
from datetime import datetime, date
from pathlib import Path

import pshouse_schedule.config as config

from pshouse_schedule import scheduler
from pshouse_schedule.fetch import fetch_deals
from pshouse_schedule.parse import parse_deals_info, parse_incorrect_deals_info
from pshouse_schedule.load import load_into_database, db
from pshouse_schedule.storage import save_to_storage
from pshouse_schedule.db.stores import Deal

logger = logging.getLogger()

OUTPUT_PATH = Path(config.STORAGE_ROOT_DIR)
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


def process_crawl_of_deals():
    logger.info("start process_crawl_of_deals")

    content = fetch_deals()

    if content is None:
        return

    today = datetime.now().strftime("%Y%m%d")
    save_to_storage(
        dirname=config.STORAGE_BUCKET_NAME,
        filepath=OUTPUT_PATH.joinpath(f"{today}_F_lvr_land_B.csv"),
        content=content,
    )

    deals, deals_need_checked = parse_deals_info(content)
    load_into_database(deals)

    deals_need_checked = parse_incorrect_deals_info(deals_need_checked)
    save_to_storage(
        dirname=config.STORAGE_BUCKET_NAME,
        filepath=OUTPUT_PATH.joinpath(f"{today}_F_lvr_land_B_need_check.json"),
        content=json.dumps(
            obj=deals_need_checked,
            indent=4,
            ensure_ascii=False,
        ).encode("utf-8"),
    )


def process_crawl_of_deals_check():
    logger.info("start process_crawl_of_deals_checked")

    deal = Deal(db.session).last()

    if deal.created_at.date() != date.today():
        raise Exception("Deals haven't been loaded yet")
