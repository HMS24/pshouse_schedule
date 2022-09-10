import os
import logging
from pathlib import Path
from datetime import datetime

import requests
from pyquery import PyQuery as pq

import pshouse_schedule.utils as utils
import pshouse_schedule.config as config
from pshouse_schedule.exceptions import NotUpdatedException

logger = logging.getLogger()


def fetch_deals():
    logger.info("   step: fetch_deals")

    try:
        if is_resource_updated() == False:
            raise NotUpdatedException("resources haven't been updated yet")

        return requests.get(
            url="https://plvr.land.moi.gov.tw//Download",
            params=dict(fileName="f_lvr_land_b.csv"),
            headers=utils.HEADERS,
        ).text
    except Exception as e:
        logger.warning(f"   fetch error: {repr(e)}")

        return None


def is_resource_updated():
    HISTORY_LIST_URL = "http://plvr.land.moi.gov.tw/DownloadHistory_ajax_list"

    history_page = requests.get(HISTORY_LIST_URL)
    doc = pq(history_page.text)

    offical_last_updated_date = (
        doc("table").eq(0)
        .children().eq(6)
        .children().eq(1)
        .text().strip().split(" ")[1]
    )

    csv_files = Path(config.STORAGE_ROOT_DIR).glob("*.csv")
    my_updated_list = [file.name[:8] for file in csv_files]

    if not my_updated_list:
        return True

    my_updated_list.sort(
        key=lambda date: datetime.strptime(date, "%Y%m%d"),
        reverse=True,
    )
    my_last_updated_date = my_updated_list[0]

    return offical_last_updated_date == my_last_updated_date
