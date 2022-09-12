import json
import logging
from pathlib import Path
from datetime import (
    datetime,
    date,
)

import pshouse_schedule.config as config

from pshouse_schedule import db
from pshouse_schedule.fetch import fetch_deals
from pshouse_schedule.parse import parse_deals_info, parse_incorrect_deals_info
from pshouse_schedule.load import load_into_database
from pshouse_schedule.storage import save_to_storage
from pshouse_schedule.utils import generate_saved_filename
from pshouse_schedule.db.stores import Deal
from pshouse_schedule.exceptions import (
    NotLoadedException,
    NotUpdatedException,
)

logger = logging.getLogger()

RESOURCES_FOLDER = Path(config.STORAGE_ROOT_DIR)
RESOURCES_FOLDER.mkdir(parents=True, exist_ok=True)
CHECK_FOLDER = RESOURCES_FOLDER.joinpath("check")
CHECK_FOLDER.mkdir(parents=True, exist_ok=True)


def crawl_deals():
    logger.info("PROCESS: crawl_deals")

    content = fetch_deals()

    if not content:
        return

    filepath = RESOURCES_FOLDER.joinpath(generate_saved_filename())
    save_to_storage(
        dirname=config.STORAGE_BUCKET_NAME,
        filepath=filepath,
        content=content,
    )

    deals, deals_need_checked = parse_deals_info(content)
    load_into_database(deals)

    if not deals_need_checked:
        return

    deals_need_checked = parse_incorrect_deals_info(deals_need_checked)
    json_file = filepath.with_suffix(".json").name
    save_to_storage(
        dirname=config.STORAGE_BUCKET_NAME,
        filepath=CHECK_FOLDER.joinpath(json_file),
        content=json.dumps(
            obj=deals_need_checked,
            indent=4,
            ensure_ascii=False,
        ),
    )


def check_deals_crawled():
    logger.info("PROCESS: check_deals_crawled")

    filepath = RESOURCES_FOLDER.joinpath(generate_saved_filename())
    if not filepath.exists():
        raise NotUpdatedException("Resources haven't been updated yet")

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
            filepath = CHECK_FOLDER.joinpath(json_file)

            with open(filepath, "wb") as f:
                content = json.dumps(
                    obj=deals_need_checked,
                    indent=4,
                    ensure_ascii=False,
                ).encode("utf-8")

                f.write(content)
