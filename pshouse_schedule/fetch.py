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
    logger.info("PROCESS: crawl_deals, STEP: fetch_deals")

    try:
        if not have_resources_been_updated():
            return

        resp = requests.get(
            url="https://plvr.land.moi.gov.tw//Download",
            params=dict(fileName="f_lvr_land_b.csv"),
            headers=utils.HEADERS,
        )

        if resp.status_code == 404:
            raise Exception("File not found")

        return resp.text
    except Exception as e:
        logger.warning(
            f"PROCESS: crawl_deals, STEP: fetch_deals, EXCEPTION: fetch error, {repr(e)}")

        return


def have_resources_been_updated():
    HISTORY_LIST_URL = "http://plvr.land.moi.gov.tw/DownloadHistory_ajax_list"

    history_page = requests.get(HISTORY_LIST_URL)
    doc = pq(history_page.text)

    try:
        offical_last_updated_date = (
            doc("table")
            .eq(0)
            .children("tr:last-child")
            .children("td:nth-child(2)")
            .text()
            .strip()
            .split(" ")[1]
        )
    except AttributeError as e:
        # 新的一季，會把前期的列表清空
        logger.warning(
            f"PROCESS: crawl_deals, STEP: have_resources_been_updated, EXCEPTION: new season start, {repr(e)}")
        return True

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
