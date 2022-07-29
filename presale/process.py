import json
import logging

from presale.fetch import fetch_actual_price_registration
from presale.parse import parse_actual_price_registration
from presale.storage import save_to_storage
from presale.load import load_into_database

logger = logging.getLogger()


def process_actual_price_registration(year, season):
    logger.info("start process_actual_price_registration")

    content = fetch_actual_price_registration(year, season)

    if content is None:
        return

    save_to_storage(
        dirname=f"{year}_{season}",
        filename="F_lvr_land_B.csv",
        content=content,
    )

    info, need_checked = parse_actual_price_registration(content)
    load_into_database(info)

    save_to_storage(
        dirname=f"{year}_{season}",
        filename="F_lvr_land_B_need_checked.json",
        content=json.dumps(
            need_checked,
            indent=4,
            ensure_ascii=False,
        ).encode("utf-8"),
    )
