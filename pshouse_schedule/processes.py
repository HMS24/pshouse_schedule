import os
import json
import logging
import fnmatch
from datetime import datetime, date
from pathlib import Path

import pshouse_schedule.config as config

from pshouse_schedule import db
from pshouse_schedule.fetch import fetch_deals
from pshouse_schedule.parse import parse_deals_info, parse_incorrect_deals_info
from pshouse_schedule.load import load_into_database
from pshouse_schedule.storage import save_to_storage
from pshouse_schedule.exceptions import NotLoadedException
from pshouse_schedule.db.stores import Deal

logger = logging.getLogger()

RESOURCES_FOLDER = Path(config.STORAGE_ROOT_DIR)
RESOURCES_FOLDER.mkdir(parents=True, exist_ok=True)
CHECKED_FOLDER = RESOURCES_FOLDER.joinpath("checked")
CHECKED_FOLDER.mkdir(parents=True, exist_ok=True)


def crawl_deals():
    logger.info("start crawl_deals")

    content = fetch_deals()

    if content is None:
        return

    today = datetime.now().strftime("%Y%m%d")
    filepath = RESOURCES_FOLDER.joinpath(f"{today}_F_lvr_land_B.csv")

    save_to_storage(
        dirname=config.STORAGE_BUCKET_NAME,
        filepath=filepath,
        content=content,
    )

    deals, deals_need_checked = parse_deals_info(content)
    deals_need_checked = parse_incorrect_deals_info(deals_need_checked)

    load_into_database(deals)

    json_file = filepath.with_suffix(".json").name
    save_to_storage(
        dirname=config.STORAGE_BUCKET_NAME,
        filepath=CHECKED_FOLDER.joinpath(json_file),
        content=json.dumps(
            obj=deals_need_checked,
            indent=4,
            ensure_ascii=False,
        ).encode("utf-8"),
    )


def check_deals_crawled():
    logger.info("start check_deals_crawled")

    deal = Deal(db.session).last()

    if deal.created_at.date() != date.today():
        raise NotLoadedException("Deals haven't been loaded yet")


def create_history_deals():
    deal = Deal(db.session)

    try:
        deal.truncate()
    except Exception as e:
        pass
    else:
        HISTORY_CREATED_AT = datetime(2022, 1, 1)

        csv_files = [file for file in RESOURCES_FOLDER.glob("*.csv")]

        for filepath in csv_files:
            with open(filepath, "rb") as f:
                content = f.read()
                deals, deals_need_checked = parse_deals_info(content)
                deals_need_checked = parse_incorrect_deals_info(
                    deals_need_checked,
                )

            for deal in deals:
                deal["created_at"] = HISTORY_CREATED_AT

            load_into_database(deals)

            json_file = filepath.with_suffix(".json").name
            filepath = CHECKED_FOLDER.joinpath(json_file)

            with open(filepath, "wb") as f:
                content = json.dumps(
                    obj=deals_need_checked,
                    indent=4,
                    ensure_ascii=False,
                ).encode("utf-8")

                f.write(content)
