import json
import logging
import datetime

from presale.crawlers.fetch import (
    fetch_actual_price_registration,
    fetch_actual_price_registration_by_year_season,
)
from presale.crawlers.parse import (
    parse_actual_price_registration,
    parse_problem_actual_price_registration,
)
from presale.crawlers.storage import save_to_storage
from presale.crawlers.load import load_into_database

logger = logging.getLogger()


def process_actual_price_registration():
    logger.info("start process_actual_price_registration")

    content = fetch_actual_price_registration()

    if content is None:
        return

    today = str(datetime.datetime.now().date())
    save_to_storage(
        dirname=f"{today}",
        filename="F_lvr_land_B.csv",
        content=content,
    )

    info, need_checked = parse_actual_price_registration(content)
    load_into_database(info)

    need_checked = parse_problem_actual_price_registration(need_checked)
    save_to_storage(
        dirname=f"{today}",
        filename="F_lvr_land_B_need_checked.json",
        content=json.dumps(
            obj=need_checked,
            indent=4,
            ensure_ascii=False,
        ).encode("utf-8"),
    )


def process_actual_price_registration_by_year_season(year, season):
    logger.info("start process_actual_price_registration_by_year_season")

    content = fetch_actual_price_registration_by_year_season(year, season)

    if content is None:
        return

    save_to_storage(
        dirname=f"{year}_{season}",
        filename="F_lvr_land_B.csv",
        content=content,
    )

    _, need_checked = parse_actual_price_registration(content)
    need_checked = parse_problem_actual_price_registration(need_checked)

    save_to_storage(
        dirname=f"{year}_{season}",
        filename="F_lvr_land_B_need_checked.json",
        content=json.dumps(
            obj=need_checked,
            indent=4,
            ensure_ascii=False,
        ).encode("utf-8"),
    )
